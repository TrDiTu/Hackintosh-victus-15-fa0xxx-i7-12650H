# snapshot.ps1 - Snapshot ONE complete EFI build into <workspace>\snapshots (max 3, rotating).
# ASCII only on purpose (Windows PowerShell 5.1 reads BOM-less UTF-8 as ANSI).
#
# Usage (run from workspace root):
#   .\.agents\skills\efi-snapshot\scripts\snapshot.ps1 -Label "wifi-touchpad" -Note "itlwm + VoodooI2C" -OcValidateResult "0 errors" -WhatIf
#   .\.agents\skills\efi-snapshot\scripts\snapshot.ps1 -Label "wifi-touchpad" -Note "..." -OcValidateResult "0 errors"
#   .\.agents\skills\efi-snapshot\scripts\snapshot.ps1 -MarkKnownGood build-02      (ONLY when the user explicitly asks)
#
# Exit codes: 0 ok (or duplicate skipped), 1 error, 3 oldest snapshot is known-good (ask the user).

[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [string]$Workspace = (Get-Location).Path,
    [string]$Source,
    [string]$Label = 'build',
    [string]$Note = '',
    [string]$OcValidateResult = 'not-run',
    [string]$MarkKnownGood,
    [int]$MaxSnapshots = 3
)

$ErrorActionPreference = 'Stop'

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

function Get-PlistString([string]$Path, [string]$Key) {
    if (-not (Test-Path -LiteralPath $Path)) { return '' }
    $t = Get-Content -LiteralPath $Path -Raw
    $m = [regex]::Match($t, '<key>' + [regex]::Escape($Key) + '</key>\s*<string>([^<]*)</string>')
    if ($m.Success) { return $m.Groups[1].Value }
    return ''
}

function Write-ManifestFiles([string]$Dir, $m) {
    ($m | ConvertTo-Json -Depth 5) | Out-File -LiteralPath (Join-Path $Dir 'MANIFEST.json') -Encoding utf8
    $kx = @()
    foreach ($k in $m.kexts) { $kx += ('- ' + $k) }
    $kg = 'false'
    if ($m.knownGood) { $kg = 'true' }
    $md = @(
        ('# ' + $m.name),
        '',
        ('- created: ' + $m.created),
        ('- label: ' + $m.label),
        ('- known-good: ' + $kg),
        ('- tree-sha256: ' + $m.treeHash),
        ('- config.plist sha256: ' + $m.configSha256),
        ('- ocvalidate: ' + $m.ocvalidate),
        '',
        '## Notes / changes vs previous build',
        $m.note,
        '',
        '## Kexts',
        ($kx -join "`r`n")
    ) -join "`r`n"
    $md | Out-File -LiteralPath (Join-Path $Dir 'MANIFEST.md') -Encoding utf8
}

function Add-BuildLog([string]$Line) {
    $log = Join-Path $Workspace 'docs\BUILD-LOG.md'
    $dir = Split-Path $log -Parent
    if (-not (Test-Path -LiteralPath $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
    if (-not (Test-Path -LiteralPath $log)) { '# BUILD-LOG' | Out-File -LiteralPath $log -Encoding utf8 }
    Add-Content -LiteralPath $log -Value ('- ' + (Get-Date -Format 's') + ' ' + $Line)
}

try {
    $Workspace = (Resolve-Path -LiteralPath $Workspace).Path.TrimEnd('\')
    $snapRoot = Join-Path $Workspace 'snapshots'
    if (-not (Test-Path -LiteralPath $snapRoot)) {
        if ($PSCmdlet.ShouldProcess($snapRoot, 'Create snapshots folder')) {
            New-Item -ItemType Directory -Path $snapRoot -Force | Out-Null
        }
    }

    $existing = @()
    if (Test-Path -LiteralPath $snapRoot) {
        $existing = @(Get-ChildItem -LiteralPath $snapRoot -Directory |
            Where-Object { $_.Name -match '^build-(\d+)-' } |
            Sort-Object { [int](($_.Name -replace '^build-(\d+)-.*$', '$1')) })
    }

    # ---- Mode: mark known-good (user-requested only) ----
    if ($MarkKnownGood) {
        $target = $existing | Where-Object { $_.Name -like ($MarkKnownGood + '-*') } | Select-Object -First 1
        if (-not $target) { throw "Snapshot '$MarkKnownGood' not found in $snapRoot" }
        $mf = Join-Path $target.FullName 'MANIFEST.json'
        $m = Get-Content -LiteralPath $mf -Raw | ConvertFrom-Json
        $m.knownGood = $true
        if ($PSCmdlet.ShouldProcess($target.FullName, 'Mark known-good')) {
            Write-ManifestFiles $target.FullName $m
            Add-BuildLog ("Marked " + $target.Name + " as known-good (user request)")
        }
        Write-Host ("OK: " + $target.Name + " marked known-good")
        exit 0
    }

    # ---- Source ----
    if (-not $Source) { $Source = Join-Path $Workspace 'EFI' }
    if (-not (Test-Path -LiteralPath $Source)) { throw "Source not found: $Source" }
    $Source = (Resolve-Path -LiteralPath $Source).Path.TrimEnd('\')
    if (-not (Test-Path -LiteralPath (Join-Path $Source 'OC\config.plist'))) {
        throw "Source does not look like an EFI folder (missing OC\config.plist): $Source"
    }

    $treeHash = Get-TreeHash $Source

    # ---- Duplicate check ----
    foreach ($d in $existing) {
        $mf = Join-Path $d.FullName 'MANIFEST.json'
        if (Test-Path -LiteralPath $mf) {
            $em = Get-Content -LiteralPath $mf -Raw | ConvertFrom-Json
            if ($em.treeHash -eq $treeHash) {
                Write-Host ("SKIP: identical to existing snapshot " + $d.Name + " (tree hash match). No new snapshot created.")
                exit 0
            }
        }
    }

    # ---- Rotation pre-check (before copying anything) ----
    $toRemove = @()
    if ($existing.Count -ge $MaxSnapshots) {
        $toRemove = @($existing | Select-Object -First ($existing.Count - $MaxSnapshots + 1))
        foreach ($d in $toRemove) {
            $mf = Join-Path $d.FullName 'MANIFEST.json'
            if (Test-Path -LiteralPath $mf) {
                $em = Get-Content -LiteralPath $mf -Raw | ConvertFrom-Json
                if ($em.knownGood) {
                    Write-Host ("STOP: oldest snapshot " + $d.Name + " is marked known-good. Ask the user before deleting anything.")
                    exit 3
                }
            }
        }
    }

    # ---- Next number (monotonic) ----
    $counterFile = Join-Path $snapRoot '_counter.txt'
    $maxExisting = 0
    foreach ($d in $existing) {
        $n = [int](($d.Name -replace '^build-(\d+)-.*$', '$1'))
        if ($n -gt $maxExisting) { $maxExisting = $n }
    }
    $counter = 0
    if (Test-Path -LiteralPath $counterFile) {
        $raw = (Get-Content -LiteralPath $counterFile -Raw).Trim()
        $tmp = 0
        if ([int]::TryParse($raw, [ref]$tmp)) { $counter = $tmp }
    }
    $next = [Math]::Max($maxExisting, $counter) + 1
    $safeLabel = ($Label -replace '[^A-Za-z0-9_\-]', '-')
    $name = ('build-{0:D2}-{1}-{2}' -f $next, (Get-Date -Format 'yyyyMMdd-HHmmss'), $safeLabel)
    $dest = Join-Path $snapRoot $name

    # Safety: destination must be inside <workspace>\snapshots
    if (-not $dest.StartsWith($snapRoot + '\', [StringComparison]::OrdinalIgnoreCase)) { throw "Unsafe destination: $dest" }

    $kexts = @()
    $kextDir = Join-Path $Source 'OC\Kexts'
    if (Test-Path -LiteralPath $kextDir) {
        foreach ($k in (Get-ChildItem -LiteralPath $kextDir -Directory -Filter '*.kext')) {
            $ver = Get-PlistString (Join-Path $k.FullName 'Contents\Info.plist') 'CFBundleShortVersionString'
            if (-not $ver) { $ver = '?' }
            $kexts += ($k.Name + ' ' + $ver)
        }
    }
    $cfgHash = (Get-FileHash -LiteralPath (Join-Path $Source 'OC\config.plist') -Algorithm SHA256).Hash

    $manifest = [ordered]@{
        build = $next; name = $name; created = (Get-Date -Format 's'); label = $Label
        note = $Note; treeHash = $treeHash; configSha256 = $cfgHash
        ocvalidate = $OcValidateResult; kexts = @($kexts); knownGood = $false
    }

    if ($PSCmdlet.ShouldProcess($dest, 'Create snapshot')) {
        New-Item -ItemType Directory -Path $dest -Force | Out-Null
        $copyDest = Join-Path $dest 'EFI'
        & robocopy $Source $copyDest /E /NFL /NDL /NJH /NJS /NP /XF .DS_Store Thumbs.db desktop.ini | Out-Null
        if ($LASTEXITCODE -ge 8) { throw "robocopy failed with code $LASTEXITCODE" }

        $copyHash = Get-TreeHash $copyDest
        if ($copyHash -ne $treeHash) { throw 'Verification failed: snapshot hash differs from source.' }

        Write-ManifestFiles $dest ([pscustomobject]$manifest)
        Set-Content -LiteralPath $counterFile -Value $next
        Add-BuildLog ("Created " + $name + " (tree " + $treeHash.Substring(0, 12) + ", ocvalidate: " + $OcValidateResult + ")")
        Write-Host ("OK: created " + $name)

        foreach ($d in $toRemove) {
            $full = $d.FullName
            if (-not $full.StartsWith($snapRoot + '\', [StringComparison]::OrdinalIgnoreCase)) { throw "Refusing to delete outside snapshots: $full" }
            Remove-Item -LiteralPath $full -Recurse -Force
            Add-BuildLog ("Rotated out (deleted) oldest snapshot " + $d.Name)
            Write-Host ("Rotated out: " + $d.Name)
        }
    }
    else {
        Write-Host ("WHATIF: would create " + $name + " and rotate out: " + (($toRemove | ForEach-Object { $_.Name }) -join ', '))
    }
    exit 0
}
catch {
    Write-Host ("ERROR: " + $_.Exception.Message)
    exit 1
}
