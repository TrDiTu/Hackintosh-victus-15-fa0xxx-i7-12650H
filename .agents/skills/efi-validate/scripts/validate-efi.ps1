# validate-efi.ps1 - Static checks for an OpenCore EFI folder + runs ocvalidate if available.
# ASCII only on purpose (Windows PowerShell 5.1).
#
# Usage (from workspace root):
#   powershell -File .\.agents\skills\efi-validate\scripts\validate-efi.ps1
#   powershell -File .\.agents\skills\efi-validate\scripts\validate-efi.ps1 -EfiPath .\EFI -OcValidate .\tools\OpenCore-1.0.x\Utilities\ocvalidate\ocvalidate.exe
#
# Writes: docs\validation\validate-<timestamp>.md and docs\validation\latest.json
# Exit code: 0 = no errors, 1 = errors found.

[CmdletBinding()]
param(
    [string]$Workspace = (Get-Location).Path,
    [string]$EfiPath,
    [string]$OcValidate
)

$ErrorActionPreference = 'Stop'
$script:Errors = New-Object System.Collections.Generic.List[string]
$script:Warnings = New-Object System.Collections.Generic.List[string]
$script:Infos = New-Object System.Collections.Generic.List[string]
function Add-Err([string]$m)  { $script:Errors.Add($m) }
function Add-Warn([string]$m) { $script:Warnings.Add($m) }
function Add-Info([string]$m) { $script:Infos.Add($m) }

function Get-TreeHash([string]$Root) {
    $rootFull = (Resolve-Path -LiteralPath $Root).Path.TrimEnd('\')
    $ignore = @('.DS_Store', 'Thumbs.db', 'desktop.ini')
    $lines = New-Object System.Collections.Generic.List[string]
    Get-ChildItem -LiteralPath $rootFull -Recurse -File -Force |
        Where-Object { $ignore -notcontains $_.Name } |
        ForEach-Object {
            $rel = $_.FullName.Substring($rootFull.Length).TrimStart('\').Replace('\', '/').ToLowerInvariant()
            $h = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash
            $lines.Add($rel + '|' + $h)
        }
    $arr = $lines.ToArray()
    [Array]::Sort($arr, [StringComparer]::Ordinal)
    $text = $arr -join "`n"
    $sha = [System.Security.Cryptography.SHA256]::Create()
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($text)
    return (($sha.ComputeHash($bytes) | ForEach-Object { $_.ToString('x2') }) -join '')
}

function Load-Plist([string]$Path) {
    $settings = New-Object System.Xml.XmlReaderSettings
    $settings.DtdProcessing = [System.Xml.DtdProcessing]::Ignore
    $settings.XmlResolver = $null
    $reader = [System.Xml.XmlReader]::Create($Path, $settings)
    try {
        $doc = New-Object System.Xml.XmlDocument
        $doc.XmlResolver = $null
        $doc.Load($reader)
    }
    finally { $reader.Close() }
    return $doc
}

function Get-Val($dictNode, [string]$key) {
    if ($null -eq $dictNode) { return $null }
    return $dictNode.SelectSingleNode("key[text()='" + $key + "']/following-sibling::*[1]")
}

function Get-Scalar($node) {
    if ($null -eq $node) { return $null }
    if ($node.Name -eq 'true') { return $true }
    if ($node.Name -eq 'false') { return $false }
    return $node.InnerText
}

function ConvertTo-Table($dictNode) {
    $t = @{}
    if ($null -eq $dictNode) { return $t }
    foreach ($k in $dictNode.SelectNodes('key')) {
        $t[$k.InnerText] = $k.SelectSingleNode('following-sibling::*[1]')
    }
    return $t
}

function Test-Enabled($table) {
    if (-not $table.ContainsKey('Enabled')) { return $true }
    return ((Get-Scalar $table['Enabled']) -eq $true)
}

try {
    $Workspace = (Resolve-Path -LiteralPath $Workspace).Path.TrimEnd('\')
    if (-not $EfiPath) { $EfiPath = Join-Path $Workspace 'EFI' }
    if (-not (Test-Path -LiteralPath $EfiPath)) { throw "EFI folder not found: $EfiPath" }
    $EfiPath = (Resolve-Path -LiteralPath $EfiPath).Path.TrimEnd('\')
    $oc = Join-Path $EfiPath 'OC'

    # ---- 1. Structure ----
    foreach ($rel in @('BOOT\BOOTx64.efi', 'OC\OpenCore.efi', 'OC\config.plist')) {
        if (-not (Test-Path -LiteralPath (Join-Path $EfiPath $rel))) { Add-Err "Missing required file: $rel" }
    }
    foreach ($rel in @('OC\Drivers', 'OC\Kexts', 'OC\ACPI')) {
        if (-not (Test-Path -LiteralPath (Join-Path $EfiPath $rel))) { Add-Warn "Folder missing: $rel (ok only if unused)" }
    }

    $cfgPath = Join-Path $oc 'config.plist'
    $root = $null
    if (Test-Path -LiteralPath $cfgPath) {
        try {
            $doc = Load-Plist $cfgPath
            $root = $doc.SelectSingleNode('/plist/dict')
            if ($null -eq $root) { Add-Err 'config.plist: cannot find root <dict>' }
        }
        catch { Add-Err ("config.plist is not valid XML plist: " + $_.Exception.Message) }
    }

    if ($null -ne $root) {
        # ---- 2. ACPI ----
        $referenced = @{}
        $acpiAdd = Get-Val (Get-Val $root 'ACPI') 'Add'
        if ($acpiAdd) {
            foreach ($e in $acpiAdd.SelectNodes('dict')) {
                $t = ConvertTo-Table $e
                $p = Get-Scalar $t['Path']
                if (-not $p) { continue }
                $referenced[$p.ToLowerInvariant()] = $true
                if (Test-Enabled $t) {
                    if (-not (Test-Path -LiteralPath (Join-Path $oc ('ACPI\' + $p)))) { Add-Err "ACPI/Add enabled but file missing: OC\ACPI\$p" }
                }
            }
        }
        if (Test-Path -LiteralPath (Join-Path $oc 'ACPI')) {
            foreach ($f in (Get-ChildItem -LiteralPath (Join-Path $oc 'ACPI') -File -Filter '*.aml')) {
                if (-not $referenced.ContainsKey($f.Name.ToLowerInvariant())) { Add-Warn "File in OC\ACPI not referenced by config.plist: $($f.Name)" }
            }
        }

        # ---- 3. Kernel/Add (order, files, dependencies, MaxKernel) ----
        $kernelAdd = Get-Val (Get-Val $root 'Kernel') 'Add'
        $kextRef = @{}
        $order = New-Object System.Collections.Generic.List[object]
        if ($kernelAdd) {
            $idx = 0
            foreach ($e in $kernelAdd.SelectNodes('dict')) {
                $t = ConvertTo-Table $e
                $bundle = Get-Scalar $t['BundlePath']
                if (-not $bundle) { continue }
                $kextRef[$bundle.ToLowerInvariant()] = $true
                $enabled = Test-Enabled $t
                if (-not $enabled) { $idx++; continue }

                $bdir = Join-Path $oc ('Kexts\' + $bundle)
                if (-not (Test-Path -LiteralPath $bdir)) { Add-Err "Kernel/Add enabled but bundle missing: OC\Kexts\$bundle"; $idx++; continue }

                $exec = Get-Scalar $t['ExecutablePath']
                if ($exec -and -not (Test-Path -LiteralPath (Join-Path $bdir $exec))) { Add-Err "ExecutablePath missing for ${bundle}: $exec" }
                $plistRel = Get-Scalar $t['PlistPath']
                if (-not $plistRel) { $plistRel = 'Contents/Info.plist' }
                $ipath = Join-Path $bdir $plistRel
                if (-not (Test-Path -LiteralPath $ipath)) { Add-Err "PlistPath missing for ${bundle}: $plistRel" }

                $maxk = Get-Scalar $t['MaxKernel']
                if ($maxk) {
                    $major = 0
                    $first = ($maxk -split '\.')[0]
                    if ([int]::TryParse($first, [ref]$major) -and $major -lt 25) {
                        Add-Warn "$bundle has MaxKernel=$maxk which excludes macOS 26 Tahoe (Darwin 25) - it will not load there."
                    }
                }
                $mink = Get-Scalar $t['MinKernel']
                if ($mink) {
                    $minor = 0
                    $firstMin = ($mink -split '\.')[0]
                    if ([int]::TryParse($firstMin, [ref]$minor) -and $minor -gt 25) {
                        Add-Warn "$bundle has MinKernel=$mink which is newer than Tahoe (Darwin 25)."
                    }
                }

                $bid = ''
                $deps = @()
                if (Test-Path -LiteralPath $ipath) {
                    try {
                        $idoc = Load-Plist $ipath
                        $iroot = $idoc.SelectSingleNode('/plist/dict')
                        $bidNode = Get-Val $iroot 'CFBundleIdentifier'
                        if ($bidNode) { $bid = $bidNode.InnerText }
                        $libs = Get-Val $iroot 'OSBundleLibraries'
                        if ($libs) { foreach ($k in $libs.SelectNodes('key')) { $deps += $k.InnerText } }
                    }
                    catch { Add-Warn "Cannot parse Info.plist of ${bundle}: $($_.Exception.Message)" }
                }
                $order.Add([pscustomobject]@{ Index = $idx; Bundle = $bundle; BundleId = $bid; Deps = $deps })
                $idx++
            }

            $idToIndex = @{}
            foreach ($o in $order) { if ($o.BundleId) { $idToIndex[$o.BundleId] = $o.Index } }
            foreach ($o in $order) {
                foreach ($d in $o.Deps) {
                    if ($d -like 'com.apple.*') { continue }
                    if (-not $idToIndex.ContainsKey($d)) {
                        Add-Err "$($o.Bundle) depends on '$d' but no enabled kext in Kernel/Add provides it."
                    }
                    elseif ($idToIndex[$d] -gt $o.Index) {
                        Add-Err "Load order: $($o.Bundle) (position $($o.Index)) must come AFTER its dependency '$d' (position $($idToIndex[$d]))."
                    }
                }
            }
            $dupes = $order | Group-Object Bundle | Where-Object { $_.Count -gt 1 }
            foreach ($g in $dupes) { Add-Warn "Duplicate enabled kext entry: $($g.Name)" }
        }
        if (Test-Path -LiteralPath (Join-Path $oc 'Kexts')) {
            foreach ($k in (Get-ChildItem -LiteralPath (Join-Path $oc 'Kexts') -Directory -Filter '*.kext')) {
                if (-not $kextRef.ContainsKey($k.Name.ToLowerInvariant())) { Add-Warn "Kext in OC\Kexts not referenced by config.plist: $($k.Name)" }
            }
        }

        # ---- 4. UEFI/Drivers ----
        $drvRef = @{}
        $drivers = Get-Val (Get-Val $root 'UEFI') 'Drivers'
        $runtimeOn = $false
        if ($drivers) {
            foreach ($e in $drivers.SelectNodes('*')) {
                $name = $null
                $enabled = $true
                if ($e.Name -eq 'string') { $name = $e.InnerText }
                elseif ($e.Name -eq 'dict') {
                    $t = ConvertTo-Table $e
                    $name = Get-Scalar $t['Path']
                    $enabled = Test-Enabled $t
                }
                if (-not $name) { continue }
                $drvRef[$name.ToLowerInvariant()] = $true
                if ($enabled) {
                    if ($name -ieq 'OpenRuntime.efi') { $runtimeOn = $true }
                    if (-not (Test-Path -LiteralPath (Join-Path $oc ('Drivers\' + $name)))) { Add-Err "UEFI/Drivers enabled but file missing: OC\Drivers\$name" }
                }
            }
        }
        if (-not $runtimeOn) { Add-Err 'OpenRuntime.efi is not enabled in UEFI/Drivers (required).' }
        if (Test-Path -LiteralPath (Join-Path $oc 'Drivers')) {
            foreach ($f in (Get-ChildItem -LiteralPath (Join-Path $oc 'Drivers') -File -Filter '*.efi')) {
                if (-not $drvRef.ContainsKey($f.Name.ToLowerInvariant())) { Add-Warn "Driver in OC\Drivers not referenced by config.plist: $($f.Name)" }
            }
        }

        # ---- 5. Misc/Tools ----
        $tools = Get-Val (Get-Val $root 'Misc') 'Tools'
        if ($tools) {
            foreach ($e in $tools.SelectNodes('dict')) {
                $t = ConvertTo-Table $e
                $p = Get-Scalar $t['Path']
                if ($p -and (Test-Enabled $t) -and -not (Test-Path -LiteralPath (Join-Path $oc ('Tools\' + $p)))) {
                    Add-Err "Misc/Tools enabled but file missing: OC\Tools\$p"
                }
            }
        }

        # ---- 6. Facts to report (no secrets printed) ----
        $misc = Get-Val $root 'Misc'
        $sbm = Get-Scalar (Get-Val (Get-Val $misc 'Security') 'SecureBootModel')
        Add-Info ("Misc/Security/SecureBootModel = " + $sbm)
        $dbgTarget = Get-Scalar (Get-Val (Get-Val $misc 'Debug') 'Target')
        Add-Info ("Misc/Debug/Target = " + $dbgTarget)
        $nvram = Get-Val (Get-Val $root 'NVRAM') 'Add'
        $bootArgs = $null
        if ($nvram) {
            $bootArgs = Get-Scalar (Get-Val (Get-Val $nvram '7C436110-AB2A-4BBB-A880-FE41995C9F82') 'boot-args')
        }
        Add-Info ("NVRAM boot-args = " + $bootArgs)

        $gen = Get-Val (Get-Val $root 'PlatformInfo') 'Generic'
        if ($gen) {
            foreach ($k in @('SystemProductName', 'SystemSerialNumber', 'MLB', 'SystemUUID')) {
                $v = Get-Scalar (Get-Val $gen $k)
                if ($k -eq 'SystemProductName') { Add-Info ("PlatformInfo SystemProductName = " + $v); continue }
                if ([string]::IsNullOrWhiteSpace($v) -or $v -like 'CHANGE_ME*') {
                    Add-Info "PlatformInfo $k = PLACEHOLDER (user must generate with macserial before real use)"
                }
                else {
                    Add-Warn "PlatformInfo $k contains a real-looking value (not printed). Do NOT copy it into logs, manifests or repos."
                }
            }
        }
    }

    # ---- 7. ocvalidate ----
    $ocvRan = $false
    $ocvExit = $null
    $ocvLines = @()
    if (-not $OcValidate) {
        $toolsDir = Join-Path $Workspace 'tools'
        if (Test-Path -LiteralPath $toolsDir) {
            $found = @(Get-ChildItem -LiteralPath $toolsDir -Recurse -Filter 'ocvalidate.exe' -ErrorAction SilentlyContinue)
            if ($found.Count -gt 0) { $OcValidate = $found[0].FullName }
            if ($found.Count -gt 1) { Add-Warn ("Multiple ocvalidate.exe found; using " + $OcValidate + ". It must match the OpenCore.efi version.") }
        }
    }
    if ($OcValidate -and (Test-Path -LiteralPath $OcValidate)) {
        $ocvLines = @(& $OcValidate $cfgPath 2>&1 | ForEach-Object { $_.ToString() })
        $ocvExit = $LASTEXITCODE
        $ocvRan = $true
        if ($ocvExit -ne 0) { Add-Err ("ocvalidate reported issues (exit code " + $ocvExit + "). See report for full output.") }
    }
    else {
        Add-Err 'ocvalidate.exe not found. Download the official OpenCore release that matches OpenCore.efi into tools\ and re-run. Result is UNVERIFIED without it.'
    }

    # ---- Report ----
    $treeHash = Get-TreeHash $EfiPath
    $valDir = Join-Path $Workspace 'docs\validation'
    New-Item -ItemType Directory -Path $valDir -Force | Out-Null
    $stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
    $report = New-Object System.Collections.Generic.List[string]
    $report.Add('# EFI validation report')
    $report.Add('')
    $report.Add('- time: ' + (Get-Date -Format 's'))
    $report.Add('- efi: ' + $EfiPath)
    $report.Add('- tree-sha256: ' + $treeHash)
    $report.Add('- errors: ' + $script:Errors.Count + ', warnings: ' + $script:Warnings.Count)
    $report.Add('- ocvalidate: ' + $(if ($ocvRan) { 'ran, exit ' + $ocvExit } else { 'NOT RUN' }))
    $report.Add('')
    $report.Add('## Errors')
    if ($script:Errors.Count -eq 0) { $report.Add('(none)') } else { foreach ($m in $script:Errors) { $report.Add('- ' + $m) } }
    $report.Add('')
    $report.Add('## Warnings')
    if ($script:Warnings.Count -eq 0) { $report.Add('(none)') } else { foreach ($m in $script:Warnings) { $report.Add('- ' + $m) } }
    $report.Add('')
    $report.Add('## Info')
    foreach ($m in $script:Infos) { $report.Add('- ' + $m) }
    $report.Add('')
    $report.Add('## ocvalidate output')
    $report.Add('```')
    foreach ($l in $ocvLines) { $report.Add($l) }
    $report.Add('```')
    ($report -join "`r`n") | Out-File -LiteralPath (Join-Path $valDir ('validate-' + $stamp + '.md')) -Encoding utf8

    $latest = [ordered]@{
        time = (Get-Date -Format 's'); efiPath = $EfiPath; treeHash = $treeHash
        errors = $script:Errors.Count; warnings = $script:Warnings.Count
        ocvalidateRan = $ocvRan; ocvalidateExit = $ocvExit
    }
    ($latest | ConvertTo-Json) | Out-File -LiteralPath (Join-Path $valDir 'latest.json') -Encoding utf8

    Write-Host ("Validated: " + $EfiPath)
    Write-Host ("Errors: " + $script:Errors.Count + "  Warnings: " + $script:Warnings.Count + "  ocvalidate: " + $(if ($ocvRan) { 'ran' } else { 'NOT RUN' }))
    foreach ($m in $script:Errors) { Write-Host ("  [ERROR] " + $m) }
    foreach ($m in $script:Warnings) { Write-Host ("  [WARN]  " + $m) }
    Write-Host ("Report: docs\validation\validate-" + $stamp + '.md')
    if ($script:Errors.Count -gt 0) { exit 1 }
    exit 0
}
catch {
    Write-Host ("FATAL: " + $_.Exception.Message)
    exit 1
}
