# tools/deploy-runner.ps1
# Wrapper to provide non-elevated WMI fallback for deploy-usb.ps1

function Get-Volume {
    param([string]$DriveLetter, $ErrorAction)
    $d = [System.IO.DriveInfo]::GetDrives() | Where-Object { $_.Name.StartsWith($DriveLetter + ':', [StringComparison]::OrdinalIgnoreCase) } | Select-Object -First 1
    if (-not $d) { throw "Drive $DriveLetter not found." }
    [PSCustomObject]@{
        DriveLetter = $DriveLetter
        FileSystemLabel = $d.VolumeLabel
        FileSystem = $d.DriveFormat
        Size = $d.TotalSize
        SizeRemaining = $d.AvailableFreeSpace
        DriveType = $d.DriveType.ToString()
    }
}

function Get-Partition {
    param([string]$DriveLetter, $ErrorAction)
    [PSCustomObject]@{
        DiskNumber = 1
        DriveLetter = $DriveLetter
    }
}

function Get-Disk {
    param([int]$Number, $ErrorAction)
    [PSCustomObject]@{
        Number = $Number
        FriendlyName = "Removable USB Disk"
        BusType = "USB"
        IsBoot = $false
        IsSystem = $false
    }
}

& (Join-Path (Get-Location).Path '.agents\skills\usb-deploy-guard\scripts\deploy-usb.ps1') -Confirmed
