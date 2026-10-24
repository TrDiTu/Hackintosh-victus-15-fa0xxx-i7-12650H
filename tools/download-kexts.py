import os, hashlib

os.makedirs('_cache/downloads', exist_ok=True)

downloads = [
    ('Lilu', 'https://github.com/acidanthera/Lilu/releases/download/1.7.2/Lilu-1.7.2-RELEASE.zip'),
    ('VirtualSMC', 'https://github.com/acidanthera/VirtualSMC/releases/download/1.3.8/VirtualSMC-1.3.8-RELEASE.zip'),
    ('WhateverGreen', 'https://github.com/acidanthera/WhateverGreen/releases/download/1.7.1/WhateverGreen-1.7.1-RELEASE.zip'),
    ('AppleALC', 'https://github.com/acidanthera/AppleALC/releases/download/1.9.8/AppleALC-1.9.8-RELEASE.zip'),
    ('NVMeFix', 'https://github.com/acidanthera/NVMeFix/releases/download/1.1.3/NVMeFix-1.1.3-RELEASE.zip'),
    ('BrcmPatchRAM', 'https://github.com/acidanthera/BrcmPatchRAM/releases/download/2.7.2/BrcmPatchRAM-2.7.2-RELEASE.zip'),
    ('VoodooPS2', 'https://github.com/acidanthera/VoodooPS2/releases/download/2.3.7/VoodooPS2Controller-2.3.7-RELEASE.zip'),
    ('RestrictEvents', 'https://github.com/acidanthera/RestrictEvents/releases/download/1.1.6/RestrictEvents-1.1.6-RELEASE.zip'),
    ('BrightnessKeys', 'https://github.com/acidanthera/BrightnessKeys/releases/download/1.0.3/BrightnessKeys-1.0.3-RELEASE.zip'),
    ('ECEnabler', 'https://github.com/averycblack/ECEnabler/releases/download/1.0.6/ECEnabler-1.0.6-RELEASE.zip'),
    ('CpuTopologyRebuild', 'https://github.com/b00t0x/CpuTopologyRebuild/releases/download/2.0.2/CpuTopologyRebuild-2.0.2-RELEASE.zip'),
    ('RealtekRTL8111', 'https://github.com/Mieze/RTL8111_driver_for_OS_X/releases/download/v3.0.0/RealtekRTL8111-V3.0.0.zip'),
    ('itlwm', 'https://github.com/OpenIntelWireless/itlwm/releases/download/v2.3.0/itlwm_v2.3.0_stable.kext.zip'),
    ('HeliPort', 'https://github.com/OpenIntelWireless/HeliPort/releases/download/v1.5.0/HeliPort.dmg'),
    ('IntelBluetooth', 'https://github.com/OpenIntelWireless/IntelBluetoothFirmware/releases/download/v2.4.0/IntelBluetooth-v2.4.0.zip'),
    ('VoodooI2C', 'https://github.com/VoodooI2C/VoodooI2C/releases/download/v2.9.1/VoodooI2C-2.9.1-RELEASE.zip'),
    ('USBToolBox', 'https://github.com/USBToolBox/kext/releases/download/1.2.0/USBToolBox-1.2.0-RELEASE.zip')
]

results = []
for name, url in downloads:
    filename = url.split('/')[-1]
    dest = os.path.join('_cache/downloads', filename)
    if not os.path.exists(dest):
        print(f'Downloading {name}...')
        cmd = f'curl.exe -sL "{url}" -o "{dest}"'
        ret = os.system(cmd)
        if ret != 0:
            print(f'Failed to download {name}')
            continue
    with open(dest, 'rb') as f:
        h = hashlib.sha256(f.read()).hexdigest()
    sz = os.path.getsize(dest)
    print(f'{name:22} | {filename:35} | {sz:10} B | {h}')
    results.append((name, filename, sz, h))

print('\nCompleted all downloads. Count:', len(results))
