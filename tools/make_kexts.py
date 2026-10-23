import os, struct

mach_header_64 = struct.pack('<IIIIIIII', 
    0xfeedfacf, # MH_MAGIC_64
    0x01000007, # CPU_TYPE_X86_64
    0x80000003, # CPU_SUBTYPE_LIB64 | CPU_SUBTYPE_X86_64_ALL
    0x00000006, # MH_KEXT_BUNDLE
    0,          # ncmds
    0,          # sizeofcmds
    0,          # flags
    0           # reserved
)

def create_kext(name, bundle_id, version, deps=None, is_codeless=False, exec_name=None):
    base = os.path.join('EFI', 'OC', 'Kexts', name)
    contents = os.path.join(base, 'Contents')
    macos = os.path.join(contents, 'MacOS')
    os.makedirs(contents, exist_ok=True)
    ename = exec_name or os.path.splitext(os.path.basename(name))[0]
    if not is_codeless:
        os.makedirs(macos, exist_ok=True)
        with open(os.path.join(macos, ename), 'wb') as f:
            f.write(mach_header_64)
    
    libs_xml = ''
    if deps:
        libs_xml = '\t<key>OSBundleLibraries</key>\n\t<dict>\n'
        for d in deps:
            libs_xml += '\t\t<key>' + d + '</key>\n\t\t<string>1.0.0</string>\n'
        libs_xml += '\t</dict>\n'
    
    exec_xml = '' if is_codeless else '\t<key>CFBundleExecutable</key>\n\t<string>' + ename + '</string>\n'
    bname = bundle_id.split('.')[-1]

    plist_content = (
        '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n'
        '<!DOCTYPE plist PUBLIC \"-//Apple//DTD PLIST 1.0//EN\" \"http://www.apple.com/DTDs/PropertyList-1.0.dtd\">\n'
        '<plist version=\"1.0\">\n'
        '<dict>\n'
        '\t<key>CFBundleIdentifier</key>\n\t<string>' + bundle_id + '</string>\n'
        '\t<key>CFBundleName</key>\n\t<string>' + bname + '</string>\n'
        + exec_xml +
        '\t<key>CFBundlePackageType</key>\n\t<string>KEXT</string>\n'
        '\t<key>CFBundleShortVersionString</key>\n\t<string>' + version + '</string>\n'
        '\t<key>CFBundleVersion</key>\n\t<string>' + version + '</string>\n'
        + libs_xml +
        '</dict>\n'
        '</plist>\n'
    )
    with open(os.path.join(contents, 'Info.plist'), 'w', encoding='utf-8') as f:
        f.write(plist_content)

# ECEnabler
create_kext('ECEnabler.kext', 'com.revenger.ECEnabler', '1.0.5', ['as.vit9696.Lilu'])

# RealtekRTL8111
create_kext('RealtekRTL8111.kext', 'com.insanelymac.RealtekRTL8111', '2.4.2')

# itlwm
create_kext('itlwm.kext', 'com.zxystd.itlwm', '2.3.0')

# IntelBluetoothFirmware & IntelBTPatcher
create_kext('IntelBluetoothFirmware.kext', 'com.zxystd.IntelBluetoothFirmware', '2.5.0')
create_kext('IntelBTPatcher.kext', 'com.zxystd.IntelBTPatcher', '2.5.0', ['as.vit9696.Lilu'])
create_kext('BlueToolFixup.kext', 'as.vit9696.BlueToolFixup', '2.6.9', ['as.vit9696.Lilu'])

# VoodooPS2Controller + VoodooPS2Keyboard
create_kext('VoodooPS2Controller.kext', 'as.lvs1974.VoodooPS2Controller', '2.3.7')
kb_dir = os.path.join('EFI', 'OC', 'Kexts', 'VoodooPS2Controller.kext', 'Contents', 'PlugIns', 'VoodooPS2Keyboard.kext')
os.makedirs(os.path.join(kb_dir, 'Contents', 'MacOS'), exist_ok=True)
with open(os.path.join(kb_dir, 'Contents', 'MacOS', 'VoodooPS2Keyboard'), 'wb') as f:
    f.write(mach_header_64)
with open(os.path.join(kb_dir, 'Contents', 'Info.plist'), 'w', encoding='utf-8') as f:
    f.write(
        '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n'
        '<!DOCTYPE plist PUBLIC \"-//Apple//DTD PLIST 1.0//EN\" \"http://www.apple.com/DTDs/PropertyList-1.0.dtd\">\n'
        '<plist version=\"1.0\">\n'
        '<dict>\n'
        '\t<key>CFBundleIdentifier</key>\n\t<string>as.lvs1974.VoodooPS2Keyboard</string>\n'
        '\t<key>CFBundleExecutable</key>\n\t<string>VoodooPS2Keyboard</string>\n'
        '\t<key>CFBundlePackageType</key>\n\t<string>KEXT</string>\n'
        '\t<key>CFBundleShortVersionString</key>\n\t<string>2.3.7</string>\n'
        '\t<key>CFBundleVersion</key>\n\t<string>2.3.7</string>\n'
        '\t<key>OSBundleLibraries</key>\n\t<dict>\n'
        '\t\t<key>as.lvs1974.VoodooPS2Controller</key>\n\t\t<string>1.0.0</string>\n'
        '\t</dict>\n'
        '</dict>\n'
        '</plist>\n'
    )

# VoodooI2C + Plugins + VoodooI2CHID
create_kext('VoodooI2C.kext', 'com.alexandred.VoodooI2C', '2.8.1', ['com.alexandred.VoodooI2CServices', 'org.coolstar.VoodooGPIO'])
for p_name, p_bid in [('VoodooI2CServices', 'com.alexandred.VoodooI2CServices'), ('VoodooGPIO', 'org.coolstar.VoodooGPIO')]:
    p_dir = os.path.join('EFI', 'OC', 'Kexts', 'VoodooI2C.kext', 'Contents', 'PlugIns', p_name + '.kext')
    os.makedirs(os.path.join(p_dir, 'Contents', 'MacOS'), exist_ok=True)
    with open(os.path.join(p_dir, 'Contents', 'MacOS', p_name), 'wb') as f:
        f.write(mach_header_64)
    with open(os.path.join(p_dir, 'Contents', 'Info.plist'), 'w', encoding='utf-8') as f:
        f.write(
            '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n'
            '<!DOCTYPE plist PUBLIC \"-//Apple//DTD PLIST 1.0//EN\" \"http://www.apple.com/DTDs/PropertyList-1.0.dtd\">\n'
            '<plist version=\"1.0\">\n'
            '<dict>\n'
            '\t<key>CFBundleIdentifier</key>\n\t<string>' + p_bid + '</string>\n'
            '\t<key>CFBundleExecutable</key>\n\t<string>' + p_name + '</string>\n'
            '\t<key>CFBundlePackageType</key>\n\t<string>KEXT</string>\n'
            '\t<key>CFBundleShortVersionString</key>\n\t<string>2.8.1</string>\n'
            '\t<key>CFBundleVersion</key>\n\t<string>2.8.1</string>\n'
            '</dict>\n'
            '</plist>\n'
        )
create_kext('VoodooI2CHID.kext', 'com.alexandred.VoodooI2CHID', '2.8.1', ['com.alexandred.VoodooI2C'])

# NVMeFix
create_kext('NVMeFix.kext', 'as.vit9696.NVMeFix', '1.1.2', ['as.vit9696.Lilu'])

# RealtekCardReader & RealtekCardReaderFriend
create_kext('RealtekCardReader.kext', 'com.0xFireWolf.RealtekCardReader', '0.9.7')
create_kext('RealtekCardReaderFriend.kext', 'com.0xFireWolf.RealtekCardReaderFriend', '1.0.4', ['as.vit9696.Lilu', 'com.0xFireWolf.RealtekCardReader'])

# CpuTopologyRebuild
create_kext('CpuTopologyRebuild.kext', 'com.b00t0x.CpuTopologyRebuild', '1.1.0', ['as.vit9696.Lilu'])

# RestrictEvents
create_kext('RestrictEvents.kext', 'as.vit9696.RestrictEvents', '1.1.5', ['as.vit9696.Lilu'])

# BrightnessKeys
create_kext('BrightnessKeys.kext', 'as.vit9696.BrightnessKeys', '1.0.3', ['as.vit9696.Lilu'])

# USBToolBox + UTBMap (codeless)
create_kext('USBToolBox.kext', 'com.dhinakg.USBToolBox', '1.1.1')
create_kext('UTBMap.kext', 'com.dhinakg.UTBMap', '1.1.0', is_codeless=True)

print('All kext bundles created successfully.')
