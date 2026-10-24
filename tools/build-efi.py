import os, shutil

# Create directory structure
base_dirs = [
    'EFI/BOOT',
    'EFI/OC/ACPI',
    'EFI/OC/Drivers',
    'EFI/OC/Kexts',
    'EFI/OC/Resources/Audio',
    'EFI/OC/Resources/Font',
    'EFI/OC/Resources/Image',
    'EFI/OC/Resources/Label'
]

for d in base_dirs:
    os.makedirs(d, exist_ok=True)

# 1. Copy Boot and OpenCore binaries
oc_src = '_cache/OpenCore-1.0.8/X64/EFI'
shutil.copy2(os.path.join(oc_src, 'BOOT/BOOTx64.efi'), 'EFI/BOOT/BOOTx64.efi')
shutil.copy2(os.path.join(oc_src, 'OC/OpenCore.efi'), 'EFI/OC/OpenCore.efi')

# 2. Copy Drivers
drivers = ['OpenRuntime.efi', 'ResetNvramEntry.efi']
for drv in drivers:
    src = os.path.join(oc_src, 'OC/Drivers', drv)
    if os.path.exists(src):
        shutil.copy2(src, os.path.join('EFI/OC/Drivers', drv))

# HfsPlus.efi / OpenHfsPlus.efi
hfs_src = '_cache/refs/victus-15-fa0xxx-hackintosh/EFI/OC/Drivers/HfsPlus.efi'
if os.path.exists(hfs_src):
    shutil.copy2(hfs_src, 'EFI/OC/Drivers/HfsPlus.efi')

# 3. Copy SSDTs
ssdt_files = [
    ('docs/acpi-src/SSDT-dGPU-Off.aml', 'EFI/OC/ACPI/SSDT-dGPU-Off.aml'),
    ('docs/acpi-src/SSDT-RTCAWAC.aml', 'EFI/OC/ACPI/SSDT-RTCAWAC.aml'),
    ('docs/acpi-src/SSDT-EC.aml', 'EFI/OC/ACPI/SSDT-EC.aml'),
    ('docs/acpi-src/SSDT-USBX.aml', 'EFI/OC/ACPI/SSDT-USBX.aml'),
    ('docs/acpi-src/SSDT-GPI0.aml', 'EFI/OC/ACPI/SSDT-GPI0.aml'),
    ('_cache/refs/victus-15-fa0xxx-hackintosh/EFI/OC/ACPI/SSDT-PLUG-ALT.aml', 'EFI/OC/ACPI/SSDT-PLUG-ALT.aml'),
    ('_cache/refs/victus-15-fa0xxx-hackintosh/EFI/OC/ACPI/SSDT-SBUS.aml', 'EFI/OC/ACPI/SSDT-SBUS.aml'),
    ('_cache/refs/victus-15-fa0xxx-hackintosh/EFI/OC/ACPI/SSDT-MCHC.aml', 'EFI/OC/ACPI/SSDT-MCHC.aml'),
]

for src, dst in ssdt_files:
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f'Copied SSDT: {os.path.basename(dst)}')

# 4. Copy Kexts
kext_map = [
    # Lilu
    ('_cache/extracted/Lilu-1.7.2-RELEASE/Lilu.kext', 'EFI/OC/Kexts/Lilu.kext'),
    # VirtualSMC
    ('_cache/extracted/VirtualSMC-1.3.8-RELEASE/Kexts/VirtualSMC.kext', 'EFI/OC/Kexts/VirtualSMC.kext'),
    ('_cache/extracted/VirtualSMC-1.3.8-RELEASE/Kexts/SMCBatteryManager.kext', 'EFI/OC/Kexts/SMCBatteryManager.kext'),
    ('_cache/extracted/VirtualSMC-1.3.8-RELEASE/Kexts/SMCProcessor.kext', 'EFI/OC/Kexts/SMCProcessor.kext'),
    # WhateverGreen
    ('_cache/extracted/WhateverGreen-1.7.1-RELEASE/WhateverGreen.kext', 'EFI/OC/Kexts/WhateverGreen.kext'),
    # AppleALC
    ('_cache/extracted/AppleALC-1.9.8-RELEASE/AppleALC.kext', 'EFI/OC/Kexts/AppleALC.kext'),
    # NVMeFix
    ('_cache/extracted/NVMeFix-1.1.3-RELEASE/NVMeFix.kext', 'EFI/OC/Kexts/NVMeFix.kext'),
    # RealtekRTL8111
    ('_cache/extracted/RealtekRTL8111-V3.0.0/RealtekRTL8111-V3.0.0/Release/RealtekRTL8111.kext', 'EFI/OC/Kexts/RealtekRTL8111.kext'),
    # itlwm
    ('_cache/extracted/itlwm_v2.3.0_stable.kext/itlwm.kext', 'EFI/OC/Kexts/itlwm.kext'),
    # IntelBluetooth
    ('_cache/extracted/IntelBluetooth-v2.4.0/IntelBluetoothFirmware.kext', 'EFI/OC/Kexts/IntelBluetoothFirmware.kext'),
    ('_cache/extracted/IntelBluetooth-v2.4.0/IntelBTPatcher.kext', 'EFI/OC/Kexts/IntelBTPatcher.kext'),
    # BlueToolFixup (from BrcmPatchRAM)
    ('_cache/extracted/BrcmPatchRAM-2.7.2-RELEASE/BlueToolFixup.kext', 'EFI/OC/Kexts/BlueToolFixup.kext'),
    # VoodooPS2Controller
    ('_cache/extracted/VoodooPS2Controller-2.3.7-RELEASE/VoodooPS2Controller.kext', 'EFI/OC/Kexts/VoodooPS2Controller.kext'),
    # VoodooI2C
    ('_cache/extracted/VoodooI2C-2.9.1-RELEASE/VoodooI2C.kext', 'EFI/OC/Kexts/VoodooI2C.kext'),
    ('_cache/extracted/VoodooI2C-2.9.1-RELEASE/VoodooI2CHID.kext', 'EFI/OC/Kexts/VoodooI2CHID.kext'),
    # CpuTopologyRebuild
    ('_cache/extracted/CpuTopologyRebuild-2.0.2-RELEASE/CpuTopologyRebuild.kext', 'EFI/OC/Kexts/CpuTopologyRebuild.kext'),
    # RestrictEvents
    ('_cache/extracted/RestrictEvents-1.1.6-RELEASE/RestrictEvents.kext', 'EFI/OC/Kexts/RestrictEvents.kext'),
    # BrightnessKeys
    ('_cache/extracted/BrightnessKeys-1.0.3-RELEASE/BrightnessKeys.kext', 'EFI/OC/Kexts/BrightnessKeys.kext'),
    # ECEnabler
    ('_cache/extracted/ECEnabler-1.0.6-RELEASE/ECEnabler.kext', 'EFI/OC/Kexts/ECEnabler.kext'),
    # USBToolBox + UTBDefault
    ('_cache/extracted/USBToolBox-1.2.0-RELEASE/USBToolBox.kext', 'EFI/OC/Kexts/USBToolBox.kext'),
    ('_cache/refs/victus-15-fa0xxx-hackintosh/EFI/OC/Kexts/UTBDefault.kext', 'EFI/OC/Kexts/UTBDefault.kext'),
]

for src, dst in kext_map:
    if os.path.exists(src):
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        print(f'Copied Kext: {os.path.basename(dst)}')
    else:
        print(f'MISSING KEXT SOURCE: {src}')

print('\nEFI tree assembled successfully.')
