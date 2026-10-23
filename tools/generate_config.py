import plistlib, os

sample_path = r'D:\OpenCore-1.0.8-RELEASE\Docs\Sample.plist'
with open(sample_path, 'rb') as f:
    config = plistlib.load(f)

# 1. ACPI
config['ACPI']['Add'] = [
    {
        'Comment': 'Enable RTC / Legacy Clock',
        'Enabled': True,
        'Path': 'SSDT-AWAC.aml'
    },
    {
        'Comment': 'Disable RTX 3050 Ti Mobile dGPU',
        'Enabled': True,
        'Path': 'SSDT-dGPU-Off.aml'
    },
    {
        'Comment': 'Fake EC and USB Power on Alder Lake PC00',
        'Enabled': True,
        'Path': 'SSDT-EC-USBX.aml'
    },
    {
        'Comment': 'Alder Lake 16-thread XCPM Power Management',
        'Enabled': True,
        'Path': 'SSDT-PLUG-ALT.aml'
    },
    {
        'Comment': 'Internal Display Backlight Control for PC00.GFX0',
        'Enabled': True,
        'Path': 'SSDT-PNLF.aml'
    },
    {
        'Comment': 'SMBus and Memory Controller for PC00',
        'Enabled': True,
        'Path': 'SSDT-SBUS-MCHC.aml'
    }
]
config['ACPI']['Delete'] = []
config['ACPI']['Patch'] = []

# 2. Booter
booter_quirks = config['Booter']['Quirks']
booter_quirks['AvoidRuntimeDefrag'] = True
booter_quirks['DevirtualiseMmio'] = True
booter_quirks['EnableSafeModeSlide'] = True
booter_quirks['EnableWriteUnprotector'] = False
booter_quirks['ProtectMemoryRegions'] = False
booter_quirks['ProtectSecureBoot'] = False
booter_quirks['ProtectUefiServices'] = False
booter_quirks['ProvideCustomSlide'] = True
booter_quirks['ProvideMaxSlide'] = 0
booter_quirks['RebuildAppleMemoryMap'] = True
booter_quirks['SetupVirtualMap'] = True
booter_quirks['SignalAppleOS'] = False
booter_quirks['SyncRuntimePermissions'] = True

# 3. DeviceProperties
config['DeviceProperties']['Add'] = {
    'PciRoot(0x0)/Pci(0x1,0x0)/Pci(0x0,0x0)': {
        'disable-gpu': bytes([0x01, 0x00, 0x00, 0x00])
    },
    'PciRoot(0x0)/Pci(0x2,0x0)': {
        'AAPL,ig-platform-id': bytes([0x00, 0x00, 0xA5, 0x3E]),
        'device-id': bytes([0xA3, 0x46, 0x00, 0x00]),
        'framebuffer-patch-enable': bytes([0x01, 0x00, 0x00, 0x00]),
        'framebuffer-stolenmem': bytes([0x00, 0x00, 0x30, 0x01])
    },
    'PciRoot(0x0)/Pci(0x1f,0x3)': {
        'layout-id': bytes([0x0B, 0x00, 0x00, 0x00])
    }
}
config['DeviceProperties']['Delete'] = {}

# 4. Kernel Add
kext_entries = [
    # Core
    ('Lilu.kext', 'Contents/MacOS/Lilu', 'Contents/Info.plist', True, 'Arbitrary kext and kernel patcher'),
    ('VirtualSMC.kext', 'Contents/MacOS/VirtualSMC', 'Contents/Info.plist', True, 'SMC emulator'),
    ('CpuTopologyRebuild.kext', 'Contents/MacOS/CpuTopologyRebuild', 'Contents/Info.plist', True, 'Alder Lake P/E core topology optimization'),
    ('RestrictEvents.kext', 'Contents/MacOS/RestrictEvents', 'Contents/Info.plist', True, 'Suppress unwanted events and fix CPU display'),
    ('WhateverGreen.kext', 'Contents/MacOS/WhateverGreen', 'Contents/Info.plist', True, 'Graphics driver and dGPU disabler'),
    ('AppleALC.kext', 'Contents/MacOS/AppleALC', 'Contents/Info.plist', True, 'Audio support for ALC245'),
    ('SMCBatteryManager.kext', 'Contents/MacOS/SMCBatteryManager', 'Contents/Info.plist', True, 'Battery management'),
    ('SMCProcessor.kext', 'Contents/MacOS/SMCProcessor', 'Contents/Info.plist', True, 'CPU temperature sensor'),
    ('ECEnabler.kext', 'Contents/MacOS/ECEnabler', 'Contents/Info.plist', True, 'Embedded Controller 8+ bit field support'),
    ('NVMeFix.kext', 'Contents/MacOS/NVMeFix', 'Contents/Info.plist', True, 'NVMe power management for SK hynix BC711'),
    # Network
    ('RealtekRTL8111.kext', 'Contents/MacOS/RealtekRTL8111', 'Contents/Info.plist', True, 'Realtek PCIe Gigabit Ethernet'),
    ('itlwm.kext', 'Contents/MacOS/itlwm', 'Contents/Info.plist', True, 'Intel Wi-Fi 6 AX211/AX210 driver'),
    ('IntelBluetoothFirmware.kext', 'Contents/MacOS/IntelBluetoothFirmware', 'Contents/Info.plist', True, 'Intel Bluetooth firmware loader'),
    ('IntelBTPatcher.kext', 'Contents/MacOS/IntelBTPatcher', 'Contents/Info.plist', True, 'Intel Bluetooth patcher'),
    ('BlueToolFixup.kext', 'Contents/MacOS/BlueToolFixup', 'Contents/Info.plist', True, 'Bluetooth stack fixup for Monterey and newer'),
    # Input & Controls
    ('BrightnessKeys.kext', 'Contents/MacOS/BrightnessKeys', 'Contents/Info.plist', True, 'ACPI brightness Fn keys support'),
    ('RealtekCardReader.kext', 'Contents/MacOS/RealtekCardReader', 'Contents/Info.plist', True, 'Realtek RTS5288 PCIe Card Reader driver'),
    ('RealtekCardReaderFriend.kext', 'Contents/MacOS/RealtekCardReaderFriend', 'Contents/Info.plist', True, 'Realtek Card Reader companion'),
    ('VoodooPS2Controller.kext', 'Contents/MacOS/VoodooPS2Controller', 'Contents/Info.plist', True, 'PS/2 controller for built-in keyboard'),
    ('VoodooPS2Controller.kext/Contents/PlugIns/VoodooPS2Keyboard.kext', 'Contents/MacOS/VoodooPS2Keyboard', 'Contents/Info.plist', True, 'PS/2 keyboard plugin'),
    ('VoodooI2C.kext/Contents/PlugIns/VoodooI2CServices.kext', 'Contents/MacOS/VoodooI2CServices', 'Contents/Info.plist', True, 'I2C core services'),
    ('VoodooI2C.kext/Contents/PlugIns/VoodooGPIO.kext', 'Contents/MacOS/VoodooGPIO', 'Contents/Info.plist', True, 'GPIO controller driver'),
    ('VoodooI2C.kext', 'Contents/MacOS/VoodooI2C', 'Contents/Info.plist', True, 'VoodooI2C core for ELAN0788 trackpad'),
    ('VoodooI2CHID.kext', 'Contents/MacOS/VoodooI2CHID', 'Contents/Info.plist', True, 'VoodooI2C HID satellite'),
    ('USBToolBox.kext', 'Contents/MacOS/USBToolBox', 'Contents/Info.plist', True, 'USB port management'),
    ('UTBMap.kext', '', 'Contents/Info.plist', True, 'Custom USB map table')
]

config['Kernel']['Add'] = [
    {
        'Arch': 'Any',
        'BundlePath': k[0],
        'Comment': k[4],
        'Enabled': k[3],
        'ExecutablePath': k[1],
        'MaxKernel': '',
        'MinKernel': '',
        'PlistPath': k[2]
    }
    for k in kext_entries
]
config['Kernel']['Block'] = []
config['Kernel']['Force'] = []
config['Kernel']['Patch'] = []

# Kernel Quirks
k_quirks = config['Kernel']['Quirks']
k_quirks['AppleCpuPmCfgLock'] = True
k_quirks['AppleXcpmCfgLock'] = True
k_quirks['AppleXcpmExtraMsrs'] = False
k_quirks['AppleXcpmForceBoost'] = False
k_quirks['CustomPciSerialDevice'] = False
k_quirks['CustomSMBIOSGuid'] = False
k_quirks['DisableIoMapper'] = True
k_quirks['DisableIoMapperMapping'] = False
k_quirks['DisableLinkeditJettison'] = True
k_quirks['DisableRtcChecksum'] = False
k_quirks['ExtendBTFeatureFlags'] = False
k_quirks['ExternalDiskIcons'] = False
k_quirks['ForceAquantiaEthernet'] = False
k_quirks['ForceSecureBootScheme'] = False
k_quirks['IncreasePciBarSize'] = False
k_quirks['LapicKernelPanic'] = False
k_quirks['LegacyCommpage'] = False
k_quirks['PanicNoKextDump'] = True
k_quirks['PowerTimeoutKernelPanic'] = True
k_quirks['ProvideCurrentCpuInfo'] = True
k_quirks['SetApfsTrimTimeout'] = -1
k_quirks['ThirdPartyDrives'] = False
k_quirks['XhciPortLimit'] = False

# 5. Misc
misc_debug = config['Misc']['Debug']
misc_debug['AppleDebug'] = True
misc_debug['ApplePanic'] = True
misc_debug['DisableWatchDog'] = True
misc_debug['DisplayDelay'] = 0
misc_debug['DisplayLevel'] = 2147483650
misc_debug['LogModules'] = '*'
misc_debug['SysReport'] = False
misc_debug['Target'] = 67

misc_sec = config['Misc']['Security']
misc_sec['AllowSetDefault'] = True
misc_sec['AuthRestart'] = False
misc_sec['BlacklistAppleUpdate'] = True
misc_sec['DmgLoading'] = 'Signed'
misc_sec['ExposeSensitiveData'] = 6
misc_sec['ScanPolicy'] = 0
misc_sec['SecureBootModel'] = 'Disabled'
misc_sec['Vault'] = 'Optional'

misc_boot = config['Misc']['Boot']
misc_boot['HibernateMode'] = 'None'
misc_boot['PickerMode'] = 'Builtin'
misc_boot['ShowPicker'] = True
misc_boot['Timeout'] = 5

config['Misc']['Tools'] = [
    {
        'Arguments': '',
        'Auxiliary': True,
        'Comment': 'UEFI Shell',
        'Enabled': True,
        'Flavour': 'OpenShell:UEFIShell:Shell',
        'FullNvramAccess': False,
        'Name': 'OpenShell',
        'Path': 'OpenShell.efi',
        'RealPath': False,
        'TextMode': False
    }
]

# 6. NVRAM
config['NVRAM']['Add']['7C436110-AB2A-4BBB-A880-FE41995C9F82'] = {
    'boot-args': '-v keepsyms=1 debug=0x100 -wegnoegpu revpatch=auto,sbvmm,cpuname alcid=11',
    'csr-active-config': bytes([0x00, 0x00, 0x00, 0x00]),
    'prev-lang:kbd': 'en-US:0',
    'run-efi-updater': 'No'
}

# 7. PlatformInfo
config['PlatformInfo']['Generic'] = {
    'AdviseFeatures': False,
    'MLB': 'CHANGE_ME_MLB',
    'MaxBIOSVersion': False,
    'ProcessorType': 0,
    'ROM': bytes([0x11, 0x22, 0x33, 0x44, 0x55, 0x66]),
    'SpoofVendor': True,
    'SystemMemoryStatus': 'Auto',
    'SystemProductName': 'MacBookPro16,1',
    'SystemSerialNumber': 'CHANGE_ME_SERIAL',
    'SystemUUID': ''
}
config['PlatformInfo']['Automatic'] = True
config['PlatformInfo']['UpdateDataHub'] = True
config['PlatformInfo']['UpdateNVRAM'] = True
config['PlatformInfo']['UpdateSMBIOS'] = True
config['PlatformInfo']['UpdateSMBIOSMode'] = 'Create'

# 8. UEFI
config['UEFI']['Drivers'] = [
    {
        'Arguments': '',
        'Comment': 'OpenRuntime',
        'Enabled': True,
        'HideVerbose': False,
        'LoadEarly': False,
        'Path': 'OpenRuntime.efi'
    },
    {
        'Arguments': '',
        'Comment': 'HFS+ File System Driver',
        'Enabled': True,
        'HideVerbose': False,
        'LoadEarly': False,
        'Path': 'OpenHfsPlus.efi'
    },
    {
        'Arguments': '',
        'Comment': 'Reset NVRAM entry in boot menu',
        'Enabled': True,
        'HideVerbose': False,
        'LoadEarly': False,
        'Path': 'ResetNvramEntry.efi'
    },
    {
        'Arguments': '',
        'Comment': 'Toggle SIP entry in boot menu',
        'Enabled': True,
        'HideVerbose': False,
        'LoadEarly': False,
        'Path': 'ToggleSipEntry.efi'
    }
]

uefi_quirks = config['UEFI']['Quirks']
uefi_quirks['ActivateHpetSupport'] = False
uefi_quirks['EnableVectorAcceleration'] = True
uefi_quirks['ReleaseUsbOwnership'] = True
uefi_quirks['RequestBootVarRouting'] = True
uefi_quirks['UnblockFsConnect'] = False

out_path = r'EFI\OC\config.plist'
with open(out_path, 'wb') as f:
    plistlib.dump(config, f, sort_keys=False)

print('config.plist written successfully to', out_path)
