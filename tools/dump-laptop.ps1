# dump-laptop.ps1
# CHAY TREN LAPTOP DICH (MAY B), khong chay tren may Codex.
# Chi doc thong tin. Khong ghi serial/UUID cua may. Ket qua nam trong thu muc .\hw-dump
# Cach chay: PowerShell (nen chay "Run as administrator" de day du hon):
#   powershell -ExecutionPolicy Bypass -File .\dump-laptop.ps1
# Sau do chep thu muc hw-dump vao <workspace>\docs\hw-dump\ tren may chay Codex.

$ErrorActionPreference = 'Continue'
$out = Join-Path (Get-Location).Path 'hw-dump'
New-Item -ItemType Directory -Path $out -Force | Out-Null

function Save-Text($name, $obj) {
    $obj | Format-List * | Out-String -Width 300 | Out-File -FilePath (Join-Path $out $name) -Encoding utf8
}

Save-Text 'system.txt'  (Get-CimInstance Win32_ComputerSystem | Select-Object Manufacturer, Model, SystemFamily, SystemSKUNumber)
Save-Text 'bios.txt'    (Get-CimInstance Win32_BIOS | Select-Object Manufacturer, SMBIOSBIOSVersion, ReleaseDate)
Save-Text 'baseboard.txt' (Get-CimInstance Win32_BaseBoard | Select-Object Manufacturer, Product, Version)
Save-Text 'cpu.txt'     (Get-CimInstance Win32_Processor | Select-Object Name, Manufacturer, NumberOfCores, NumberOfLogicalProcessors)
Save-Text 'memory.txt'  (Get-CimInstance Win32_PhysicalMemory | Select-Object Manufacturer, Capacity, Speed, SMBIOSMemoryType)
Save-Text 'gpu.txt'     (Get-CimInstance Win32_VideoController | Select-Object Name, PNPDeviceID, AdapterRAM, DriverVersion, CurrentHorizontalResolution, CurrentVerticalResolution, CurrentRefreshRate)
Save-Text 'disks.txt'   (Get-CimInstance Win32_DiskDrive | Select-Object Model, InterfaceType, Size, PNPDeviceID)
Save-Text 'network.txt' (Get-CimInstance Win32_NetworkAdapter | Where-Object { $_.PNPDeviceID -like 'PCI*' -or $_.PNPDeviceID -like 'USB*' } | Select-Object Name, PNPDeviceID)
Save-Text 'battery.txt' (Get-CimInstance Win32_Battery | Select-Object Name, DeviceID, Chemistry)

# Man hinh: hang, ten, nam san xuat (khong lay serial)
try {
    $mons = Get-CimInstance -Namespace root\wmi -ClassName WmiMonitorID -ErrorAction Stop | ForEach-Object {
        $mfg  = -join ($_.ManufacturerName | Where-Object { $_ -ne 0 } | ForEach-Object { [char]$_ })
        $name = -join ($_.UserFriendlyName | Where-Object { $_ -ne 0 } | ForEach-Object { [char]$_ })
        $code = -join ($_.ProductCodeID | Where-Object { $_ -ne 0 } | ForEach-Object { [char]$_ })
        [pscustomobject]@{ Manufacturer = $mfg; Name = $name; ProductCode = $code; YearOfManufacture = $_.YearOfManufacture; InstanceName = $_.InstanceName }
    }
    Save-Text 'monitors.txt' $mons
} catch { "Khong doc duoc WmiMonitorID: $($_.Exception.Message)" | Out-File (Join-Path $out 'monitors.txt') -Encoding utf8 }

# Toan bo thiet bi dang hien dien kem Hardware ID / Compatible ID
$rows = New-Object System.Collections.Generic.List[object]
$devs = Get-PnpDevice -PresentOnly -ErrorAction SilentlyContinue
$i = 0
foreach ($d in $devs) {
    $i++
    if (($i % 50) -eq 0) { Write-Host ("Dang doc thiet bi {0}/{1}" -f $i, @($devs).Count) }
    $hw = ''
    $cid = ''
    $loc = ''
    try { $hw  = (Get-PnpDeviceProperty -InstanceId $d.InstanceId -KeyName 'DEVPKEY_Device_HardwareIds'   -ErrorAction Stop).Data -join ' | ' } catch {}
    try { $cid = (Get-PnpDeviceProperty -InstanceId $d.InstanceId -KeyName 'DEVPKEY_Device_CompatibleIds' -ErrorAction Stop).Data -join ' | ' } catch {}
    try { $loc = (Get-PnpDeviceProperty -InstanceId $d.InstanceId -KeyName 'DEVPKEY_Device_LocationInfo'  -ErrorAction Stop).Data } catch {}
    $rows.Add([pscustomobject]@{
        Class = $d.Class; Name = $d.FriendlyName; Status = $d.Status
        InstanceId = $d.InstanceId; HardwareIds = $hw; CompatibleIds = $cid; Location = $loc
    })
}
$rows | Export-Csv -Path (Join-Path $out 'pnp-devices.csv') -NoTypeInformation -Encoding UTF8

# Mot so nhom hay can (de Codex doc nhanh)
$rows | Where-Object { $_.InstanceId -like 'ACPI\*' } | Export-Csv (Join-Path $out 'acpi-devices.csv') -NoTypeInformation -Encoding UTF8
$rows | Where-Object { $_.Class -in @('Net','Bluetooth','HIDClass','Media','Camera','Image','SCSIAdapter','USB','System','Biometric','SecurityDevices','Sensor') } |
    Export-Csv (Join-Path $out 'pnp-key-classes.csv') -NoTypeInformation -Encoding UTF8

# Ghi chu
@"
Tao luc: $(Get-Date -Format s)
Script: dump-laptop.ps1 (chi doc, khong serial/UUID)
Luu y: DSDT/SSDT khong nam trong script nay. Dump rieng bang SSDTTime/acpidump, hoac dung OpenCore
Misc > Debug > SysReport tren ban OpenCore debug, roi chep vao docs\hw-dump\acpi\.
"@ | Out-File (Join-Path $out 'README.txt') -Encoding utf8

Write-Host "Xong. Chep thu muc hw-dump vao <workspace>\docs\hw-dump\ tren may chay Codex."
