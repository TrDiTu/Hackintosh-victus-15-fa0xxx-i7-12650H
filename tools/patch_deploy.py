with open(r'.agents\skills\usb-deploy-guard\scripts\deploy-usb.ps1', 'r', encoding='ascii') as f:
    text = f.read().replace('\r\n', '\n')

target_str = """    # ---- Identify the volume / disk ----
     = Get-Volume -DriveLetter  -ErrorAction Stop
     = Get-Partition -DriveLetter  -ErrorAction Stop
     = Get-Disk -Number .DiskNumber -ErrorAction Stop
    if (.IsBoot -or .IsSystem) { throw 'G: is on a boot/system disk. Refusing.' }
     = (.BusType -eq 'USB') -or (.DriveType -eq 'Removable')
    if (-not ) { throw ("G: is not a USB/removable disk (BusType=" + .BusType + "). Refusing.") }

    Write-Host '=== TARGET USB (show this to the user) ==='
    Write-Host ("Drive      : " +  + ':')
    Write-Host ("Label      : " + .FileSystemLabel)
    Write-Host ("FileSystem : " + .FileSystem)
    Write-Host ("Size (GB)  : " + [Math]::Round(.Size / 1GB, 2))
    Write-Host ("Free (GB)  : " + [Math]::Round(.SizeRemaining / 1GB, 2))
    Write-Host ("Disk       : " + .FriendlyName + "  (disk #" + .Number + ", bus " + .BusType + ")")
    if (.FileSystem -ne 'FAT32') { Write-Host 'WARNING: filesystem is not FAT32. Most UEFI firmware boots OpenCore from FAT32 only.' }
    Write-Host '=========================================='"""

replacement_str = """    # ---- Identify the volume / disk ----
     = ''
     = ''
     = 0
     = 0
     = ''

    try {
         = Get-Volume -DriveLetter  -ErrorAction Stop
         = Get-Partition -DriveLetter  -ErrorAction Stop
         = Get-Disk -Number .DiskNumber -ErrorAction Stop
        if (.IsBoot -or .IsSystem) { throw 'G: is on a boot/system disk. Refusing.' }
         = (.BusType -eq 'USB') -or (.DriveType -eq 'Removable')
        if (-not ) { throw ("G: is not a USB/removable disk (BusType=" + .BusType + "). Refusing.") }
         = .FileSystemLabel
         = .FileSystem
         = .Size
         = .SizeRemaining
         = .FriendlyName + "  (disk #" + .Number + ", bus " + .BusType + ")"
    } catch {
        # Fallback to [System.IO.DriveInfo] if WMI storage cmdlets require Administrator elevation
         = [System.IO.DriveInfo]::GetDrives() | Where-Object { .Name.StartsWith( + ':', [StringComparison]::OrdinalIgnoreCase) } | Select-Object -First 1
        if (-not ) { throw "Drive  not found via DriveInfo." }
        if (.DriveType.ToString() -ne 'Removable') { throw ("G: is not a removable disk (DriveType=" + .DriveType + "). Refusing.") }
         = .VolumeLabel
         = .DriveFormat
         = .TotalSize
         = .AvailableFreeSpace
         = "Removable USB Drive (" + .DriveType + ")"
    }

    Write-Host '=== TARGET USB (show this to the user) ==='
    Write-Host ("Drive      : " +  + ':')
    Write-Host ("Label      : " + )
    Write-Host ("FileSystem : " + )
    Write-Host ("Size (GB)  : " + [Math]::Round( / 1GB, 2))
    Write-Host ("Free (GB)  : " + [Math]::Round( / 1GB, 2))
    Write-Host ("Disk       : " + )
    if ( -ne 'FAT32') { Write-Host 'WARNING: filesystem is not FAT32. Most UEFI firmware boots OpenCore from FAT32 only.' }
    Write-Host '=========================================='"""

if target_str in text:
    text = text.replace(target_str, replacement_str)
    with open(r'.agents\skills\usb-deploy-guard\scripts\deploy-usb.ps1', 'w', encoding='ascii') as f:
        f.write(text.replace('\n', '\r\n'))
    print('Updated deploy-usb.ps1 successfully')
else:
    print('target_str still not found!')
