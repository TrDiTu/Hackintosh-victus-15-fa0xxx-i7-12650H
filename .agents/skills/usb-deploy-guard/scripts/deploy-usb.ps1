# deploy-usb.ps1 - Safely deploy <workspace>\EFI to G:\EFI.
# ASCII only on purpose (Windows PowerShell 5.1).
#
# Step 1 (dry run, default):  powershell -File .\.agents\skills\usb-deploy-guard\scripts\deploy-usb.ps1
# Step 2 (real write):        ... deploy-usb.ps1 -Confirmed        (ONLY after the user approved the USB shown in step 1)
#
# Hard rules enforced here:
#   - Only drive letter G is accepted.
#   - G: must be a USB/removable disk, never the system/boot disk.
#   - Only writes inside G:\EFI. Never formats or touches partitions.
#   - Requires a clean, up-to-date efi-validate result for exactly this EFI content.
#   - Snapshots the existing G:\EFI first (efi-snapshot) when it holds an EFI.
#   - Verifies the copy by tree hash.
# Exit codes: 0 ok, 1 error, 4 validation gate failed, 5 existing G:\EFI needs user attention, 6 snapshot blocked.

[CmdletBinding()]
param(
    [string]$Workspace = (Get-Location).Path,
    [string]$Source,
    [string]$DriveLetter = 'G',
    [switch]$Confirmed
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

function Add-BuildLog([string]$Line) {
    $log = Join-Path $Workspace 'docs\BUILD-LOG.md'
    $dir = Split-Path $log -Parent
    if (-not (Test-Path -LiteralPath $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
    if (-not (Test-Path -LiteralPath $log)) { '# BUILD-LOG' | Out-File -LiteralPath $log -Encoding utf8 }
    Add-Content -LiteralPath $log -Value ('- ' + (Get-Date -Format 's') + ' ' + $Line)
}

try {
    $Workspace = (Resolve-Path -LiteralPath $Workspace).Path.TrimEnd('\')
    $letter = $DriveLetter.TrimEnd(':').ToUpperInvariant()
    if ($letter -ne 'G') { throw "Only drive G is allowed (got '$DriveLetter')." }
    if ($env:SystemDrive.TrimEnd(':').ToUpperInvariant() -eq $letter) { throw 'G: is the system drive. Refusing.' }

    # ---- Identify the volume / disk ----
    $vol = Get-Volume -DriveLetter $letter -ErrorAction Stop
    $part = Get-Partition -DriveLetter $letter -ErrorAction Stop
    $disk = Get-Disk -Number $part.DiskNumber -ErrorAction Stop
    if ($disk.IsBoot -or $disk.IsSystem) { throw 'G: is on a boot/system disk. Refusing.' }
    $isUsb = ($disk.BusType -eq 'USB') -or ($vol.DriveType -eq 'Removable')
    if (-not $isUsb) { throw ("G: is not a USB/removable disk (BusType=" + $disk.BusType + "). Refusing.") }

    Write-Host '=== TARGET USB (show this to the user) ==='
    Write-Host ("Drive      : " + $letter + ':')
    Write-Host ("Label      : " + $vol.FileSystemLabel)
    Write-Host ("FileSystem : " + $vol.FileSystem)
    Write-Host ("Size (GB)  : " + [Math]::Round($vol.Size / 1GB, 2))
    Write-Host ("Free (GB)  : " + [Math]::Round($vol.SizeRemaining / 1GB, 2))
    Write-Host ("Disk       : " + $disk.FriendlyName + "  (disk #" + $disk.Number + ", bus " + $disk.BusType + ")")
    if ($vol.FileSystem -ne 'FAT32') { Write-Host 'WARNING: filesystem is not FAT32. Most UEFI firmware boots OpenCore from FAT32 only.' }
    Write-Host '=========================================='

    # ---- Source ----
    if (-not $Source) { $Source = Join-Path $Workspace 'EFI' }
    if (-not (Test-Path -LiteralPath $Source)) { throw "Source not found: $Source" }
    $Source = (Resolve-Path -LiteralPath $Source).Path.TrimEnd('\')
    if (-not $Source.StartsWith($Workspace + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Source must be inside the workspace.' }
    if (-not (Test-Path -LiteralPath (Join-Path $Source 'OC\config.plist'))) { throw 'Source is not an EFI folder (OC\config.plist missing).' }

    $dest = $letter + ':\EFI'   # fixed destination, never anything else
    $srcHash = Get-TreeHash $Source

    # ---- Validation gate ----
    $latestPath = Join-Path $Workspace 'docs\validation\latest.json'
    if (-not (Test-Path -LiteralPath $latestPath)) { Write-Host 'GATE: no validation result. Run efi-validate first.'; exit 4 }
    $latest = Get-Content -LiteralPath $latestPath -Raw | ConvertFrom-Json
    if (-not $latest.ocvalidateRan) { Write-Host 'GATE: ocvalidate did not run in the last validation.'; exit 4 }
    if ([int]$latest.errors -ne 0) { Write-Host ('GATE: last validation has ' + $latest.errors + ' error(s).'); exit 4 }
    if ($latest.treeHash -ne $srcHash) { Write-Host 'GATE: EFI changed since the last validation. Re-run efi-validate.'; exit 4 }
    Write-Host 'Gate OK: validation is clean and matches the EFI content.'

    $destExists = Test-Path -LiteralPath $dest
    if ($destExists) {
        $destFiles = @(Get-ChildItem -LiteralPath $dest -Recurse -File -Force -ErrorAction SilentlyContinue)
        if ($destFiles.Count -gt 0 -and -not (Test-Path -LiteralPath (Join-Path $dest 'OC\config.plist'))) {
            Write-Host ("G:\EFI exists with " + $destFiles.Count + " file(s) but is not an OpenCore EFI. Ask the user what to do. Nothing was changed.")
            exit 5
        }
    }

    if (-not $Confirmed) {
        Write-Host ''
        Write-Host 'DRY RUN - nothing written. Planned changes (robocopy list-only):'
        & robocopy $Source $dest /MIR /L /FFT /NJH /NJS /NP /XF .DS_Store Thumbs.db desktop.ini
        Write-Host ''
        Write-Host 'Show the USB info above to the user. After they approve, re-run with -Confirmed.'
        exit 0
    }

    # ---- Snapshot the existing G:\EFI (only if it holds an EFI) ----
    if ($destExists -and (Test-Path -LiteralPath (Join-Path $dest 'OC\config.plist'))) {
        $snap = Join-Path $Workspace '.agents\skills\efi-snapshot\scripts\snapshot.ps1'
        if (-not (Test-Path -LiteralPath $snap)) { throw 'efi-snapshot script not found; cannot back up existing G:\EFI.' }
        & $snap -Workspace $Workspace -Source $dest -Label 'usb-before-deploy' -Note 'Automatic backup of G:\EFI before deploy' -OcValidateResult 'n/a (existing USB content)'
        if ($LASTEXITCODE -ne 0) { Write-Host ('Snapshot step returned ' + $LASTEXITCODE + '. Not writing to USB.'); exit 6 }
    }

    # ---- Write ----
    & robocopy $Source $dest /MIR /FFT /R:2 /W:2 /NFL /NDL /NJH /NP /XF .DS_Store Thumbs.db desktop.ini
    if ($LASTEXITCODE -ge 8) { throw ('robocopy failed with code ' + $LASTEXITCODE) }

    # ---- Verify ----
    $dstHash = Get-TreeHash $dest
    if ($dstHash -ne $srcHash) { throw 'Verification FAILED: G:\EFI hash differs from source.' }
    Add-BuildLog ('Deployed EFI to G:\EFI (tree ' + $srcHash.Substring(0, 12) + ', verified)')
    Write-Host ('OK: G:\EFI matches the workspace EFI (tree ' + $srcHash.Substring(0, 12) + '). Safely eject the USB before unplugging.')
    exit 0
}
catch {
    Write-Host ('ERROR: ' + $_.Exception.Message)
    exit 1
}
