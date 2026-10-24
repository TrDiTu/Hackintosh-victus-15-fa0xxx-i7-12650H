import os, plistlib

sample_path = '_cache/OpenCore-1.0.8/Docs/Sample.plist'
with open(sample_path, 'rb') as f:
    cfg = plistlib.load(f)

# === ACPI ===
cfg['ACPI']['Add'] = [
    {'Path': 'SSDT-PLUG-ALT.aml', 'Enabled': True, 'Comment': 'Alder Lake-H CPU power management'},
    {'Path': 'SSDT-RTCAWAC.aml', 'Enabled': True, 'Comment': 'Enable RTC, disable AWAC (STAS=1)'},
    {'Path': 'SSDT-EC.aml', 'Enabled': True, 'Comment': 'Fake EC device for macOS'},
    {'Path': 'SSDT-USBX.aml', 'Enabled': True, 'Comment': 'USB power limits'},
    {'Path': 'SSDT-GPI0.aml', 'Enabled': True, 'Comment': 'Enable GPIO controller'},
    {'Path': 'SSDT-dGPU-Off.aml', 'Enabled': True, 'Comment': 'Disable RTX 3050 Ti via _OFF'},
    {'Path': 'SSDT-SBUS.aml', 'Enabled': True, 'Comment': 'SMBus support'},
    {'Path': 'SSDT-MCHC.aml', 'Enabled': True, 'Comment': 'MCHC controller'}
]

cfg['ACPI']['Delete'] = []
cfg['ACPI']['Patch'] = [
    {
        'Base': '',
        'BaseSkip': 0,
        'Comment': 'Fix HP Real-Time Clock Power Loss (005) Post Error',
        'Count': 0,
        'Enabled': True,
        'Find': bytes.fromhex('4701700070000108'),
        'Limit': 0,
        'Mask': b'',
        'OemTableId': b'',
        'Replace': bytes.fromhex('4701700070000102'),
        'ReplaceMask': b'',
        'Skip': 0,
        'TableLength': 0,
        'TableSignature': b''
    },
    {
        'Base': '',
        'BaseSkip': 0,
        'Comment': 'GPI0 _STA to XSTA Rename',
        'Count': 1,
        'Enabled': True,
        'Find': bytes.fromhex('145F535441'),
        'Limit': 0,
        'Mask': b'',
        'OemTableId': b'',
        'Replace': bytes.fromhex('1458535441'),
        'ReplaceMask': b'',
        'Skip': 0,
        'TableLength': 0,
        'TableSignature': bytes.fromhex('44534454')
    }
]

cfg['ACPI']['Quirks'] = {
    'FadtEnableReset': False,
    'NormalizeHeaders': False,
    'RebaseRegions': False,
    'ResetHwSig': False,
    'ResetLogoStatus': True,
    'SyncTableIds': False
}

# === Booter ===
cfg['Booter']['MmioWhitelist'] = []
cfg['Booter']['Patch'] = []
cfg['Booter']['Quirks'] = {
    'AllowRelocationBlock': True,
    'AvoidRuntimeDefrag': True,
    'ClearTaskSwitchBit': False,
    'DevirtualiseMmio': True,
    'DisableSingleUser': False,
    'DisableVariableWrite': False,
    'DiscardHibernateMap': False,
    'EnableSafeModeSlide': True,
    'EnableWriteUnprotector': False,
    'FixupAppleEfiImages': True,
    'ForceBooterSignature': False,
    'ForceExitBootServices': False,
    'ProtectMemoryRegions': False,
    'ProtectSecureBoot': False,
    'ProtectUefiServices': True,
    'ProvideCustomSlide': True,
    'ProvideMaxSlide': 0,
    'RebuildAppleMemoryMap': True,
    'ResizeAppleGpuBars': 0,
    'SetupVirtualMap': True,
    'SignalAppleOS': False,
    'SyncRuntimePermissions': True
}

# === DeviceProperties ===
cfg['DeviceProperties']['Add'] = {
    'PciRoot(0x0)/Pci(0x1,0x0)/Pci(0x0,0x0)': {
        'acpi-wake-type': bytes.fromhex('01000000'),
        'disable-gpu': bytes.fromhex('01000000')
    },
    'PciRoot(0x0)/Pci(0x2,0x0)': {
        'AAPL,ig-platform-id': bytes.fromhex('0000499A'),
        'AAPL,slot-name': 'built-in',
        'built-in': bytes.fromhex('00'),
        'complete-modeset': bytes.fromhex('01000000'),
        'device-id': bytes.fromhex('499A0000'),
        'enable-max-pixel-clock-override': bytes.fromhex('01000000'),
        'force-online': bytes.fromhex('01000000'),
        'framebuffer-patch-enable': bytes.fromhex('01000000'),
        'hda-gfx': 'onboard-1',
        'model': 'Intel Iris Xe Graphics',
        'rps-control': bytes.fromhex('01000000')
    },
    'PciRoot(0x0)/Pci(0x1f,0x3)': {
        'layout-id': bytes.fromhex('0B000000')
    }
}
cfg['DeviceProperties']['Delete'] = {}

# === Kernel ===
kernel_kexts = [
    ('Lilu.kext', 'Contents/MacOS/Lilu', 'Lilu patch engine'),
    ('VirtualSMC.kext', 'Contents/MacOS/VirtualSMC', 'SMC emulator'),
    ('CpuTopologyRebuild.kext', 'Contents/MacOS/CpuTopologyRebuild', 'Alder Lake 6P+4E CPU topology'),
    ('WhateverGreen.kext', 'Contents/MacOS/WhateverGreen', 'Graphics patches & TGL spoof'),
    ('AppleALC.kext', 'Contents/MacOS/AppleALC', 'ALC245 audio patch'),
    ('RestrictEvents.kext', 'Contents/MacOS/RestrictEvents', 'SMBIOS & revcpu'),
    ('BrightnessKeys.kext', 'Contents/MacOS/BrightnessKeys', 'Brightness keys'),
    ('ECEnabler.kext', 'Contents/MacOS/ECEnabler', 'EC0_ field size fix'),
    ('NVMeFix.kext', 'Contents/MacOS/NVMeFix', 'NVMe APST management'),
    ('RealtekRTL8111.kext', 'Contents/MacOS/RealtekRTL8111', 'Realtek Gigabit Ethernet'),
    ('SMCBatteryManager.kext', 'Contents/MacOS/SMCBatteryManager', 'Battery management'),
    ('SMCProcessor.kext', 'Contents/MacOS/SMCProcessor', 'CPU sensor'),
    ('USBToolBox.kext', 'Contents/MacOS/USBToolBox', 'USB host controller mapping'),
    ('UTBDefault.kext', '', 'USB default injector'),
    ('VoodooPS2Controller.kext', 'Contents/MacOS/VoodooPS2Controller', 'PS/2 controller'),
    ('VoodooPS2Controller.kext/Contents/PlugIns/VoodooPS2Keyboard.kext', 'Contents/MacOS/VoodooPS2Keyboard', 'PS/2 keyboard'),
    ('VoodooI2C.kext/Contents/PlugIns/VoodooI2CServices.kext', 'Contents/MacOS/VoodooI2CServices', 'VoodooI2C services'),
    ('VoodooI2C.kext/Contents/PlugIns/VoodooGPIO.kext', 'Contents/MacOS/VoodooGPIO', 'GPIO controller'),
    ('VoodooI2C.kext/Contents/PlugIns/VoodooInput.kext', 'Contents/MacOS/VoodooInput', 'Input aggregator'),
    ('VoodooI2C.kext', 'Contents/MacOS/VoodooI2C', 'VoodooI2C core'),
    ('VoodooI2CHID.kext', 'Contents/MacOS/VoodooI2CHID', 'ELAN0788 HID trackpad'),
    ('itlwm.kext', 'Contents/MacOS/itlwm', 'Intel Wi-Fi AX211/AX210'),
    ('IntelBluetoothFirmware.kext', 'Contents/MacOS/IntelBluetoothFirmware', 'Intel BT firmware'),
    ('IntelBTPatcher.kext', 'Contents/MacOS/IntelBTPatcher', 'Intel BT patcher'),
    ('BlueToolFixup.kext', 'Contents/MacOS/BlueToolFixup', 'Bluetooth fixup for modern macOS')
]

cfg['Kernel']['Add'] = []
for bp, ep, comment in kernel_kexts:
    cfg['Kernel']['Add'].append({
        'Arch': 'Any',
        'BundlePath': bp,
        'Comment': comment,
        'Enabled': True,
        'ExecutablePath': ep,
        'MaxKernel': '',
        'MinKernel': '',
        'PlistPath': 'Contents/Info.plist'
    })

cfg['Kernel']['Block'] = []
cfg['Kernel']['Emulate'] = {
    'Cpuid1Data': bytes.fromhex('55060A00000000000000000000000000'),
    'Cpuid1Mask': bytes.fromhex('FFFFFFFF000000000000000000000000'),
    'DummyPowerManagement': False,
    'MaxKernel': '',
    'MinKernel': ''
}
cfg['Kernel']['Force'] = []
cfg['Kernel']['Patch'] = []
cfg['Kernel']['Quirks'] = {
    'AppleCpuPmCfgLock': True,
    'AppleXcpmCfgLock': True,
    'AppleXcpmExtraMsrs': False,
    'AppleXcpmForceBoost': False,
    'CustomPciSerialDevice': False,
    'CustomSMBIOSGuid': True,
    'DisableIoMapper': True,
    'DisableIoMapperMapping': False,
    'DisableLinkeditJettison': True,
    'DisableRtcChecksum': True,
    'ExtendBTFeatureFlags': False,
    'ExternalDiskIcons': False,
    'ForceAquantiaEthernet': False,
    'ForceSecureBootScheme': False,
    'IncreasePciBarSize': False,
    'LapicKernelPanic': True,
    'LegacyCommpage': False,
    'PanicNoKextDump': True,
    'PowerTimeoutKernelPanic': True,
    'ProvideCurrentCpuInfo': True,
    'SetApfsTrimTimeout': -1,
    'ThirdPartyDrives': False,
    'XhciPortLimit': False
}
cfg['Kernel']['Scheme'] = {
    'CustomKernel': False,
    'FuzzyMatch': True,
    'KernelArch': 'Auto',
    'KernelCache': 'Auto'
}

# === Misc ===
cfg['Misc']['BlessOverride'] = []
cfg['Misc']['Boot'] = {
    'ConsoleAttributes': 0,
    'HibernateMode': 'None',
    'HibernateSkipsPicker': False,
    'HideAuxiliary': False,
    'InstanceIdentifier': '',
    'LauncherOption': 'Disabled',
    'LauncherPath': 'Default',
    'PickerAttributes': 17,
    'PickerAudioAssist': False,
    'PickerMode': 'Builtin',
    'PickerVariant': 'Auto',
    'PollAppleHotKeys': True,
    'ShowPicker': True,
    'TakeoffDelay': 0,
    'Timeout': 5
}
cfg['Misc']['Debug'] = {
    'AppleDebug': True,
    'ApplePanic': True,
    'DisableWatchDog': True,
    'DisplayDelay': 0,
    'DisplayLevel': 2147483714,
    'LogModules': '*',
    'SysReport': False,
    'Target': 67
}
cfg['Misc']['Entries'] = []
cfg['Misc']['Security'] = {
    'AllowSetDefault': True,
    'ApECID': 0,
    'AuthRestart': False,
    'BlacklistAppleUpdate': True,
    'DmgLoading': 'Signed',
    'EnablePassword': False,
    'ExposeSensitiveData': 6,
    'HaltLevel': 2147483648,
    'PasswordHash': b'',
    'PasswordSalt': b'',
    'ScanPolicy': 0,
    'SecureBootModel': 'Disabled',
    'Vault': 'Optional'
}
cfg['Misc']['Serial'] = {
    'Custom': {
        'BaudRate': 115200,
        'ClockRate': 1843200,
        'DetectCable': False,
        'ExtendedTxFifoSize': 64,
        'FifoControl': 7,
        'LineControl': 7,
        'PciDeviceInfo': bytes.fromhex('FF'),
        'RegisterAccessWidth': 8,
        'RegisterBase': 0,
        'RegisterStride': 1,
        'UseHardwareFlowControl': False,
        'UseMmio': False
    },
    'Init': False,
    'Override': False
}
cfg['Misc']['Tools'] = []

# === NVRAM ===
cfg['NVRAM']['Add'] = {
    '4D1EDE05-38C7-4A6A-9CC6-4BCCA8B38C14': {
        'DefaultBackgroundColor': bytes.fromhex('00000000')
    },
    '4D1FDA02-38C7-4A6A-9CC6-4BCCA8B30102': {
        'rtc-blacklist': b'',
        'revcpu': 1,
        'revcpuname': '10-Core Intel Core i7-12650H'
    },
    '7C436110-AB2A-4BBB-A880-FE41995C9F82': {
        'boot-args': '-v debug=0x100 keepsyms=1 -lilubetaall amfi=0x80 -vi2c-force-polling -wegnoegpu alcid=11',
        'csr-active-config': bytes.fromhex('EF0F0000'),
        'prev-lang:kbd': 'en-US:0',
        'run-efi-updater': 'No'
    }
}
cfg['NVRAM']['Delete'] = {
    '4D1EDE05-38C7-4A6A-9CC6-4BCCA8B38C14': ['DefaultBackgroundColor'],
    '4D1FDA02-38C7-4A6A-9CC6-4BCCA8B30102': ['rtc-blacklist', 'revcpu', 'revcpuname'],
    '7C436110-AB2A-4BBB-A880-FE41995C9F82': ['boot-args', 'csr-active-config']
}
cfg['NVRAM']['LegacyOverwrite'] = False
cfg['NVRAM']['LegacySchema'] = {}
cfg['NVRAM']['WriteFlash'] = True

# === PlatformInfo ===
cfg['PlatformInfo']['Automatic'] = True
cfg['PlatformInfo']['CustomMemory'] = False
cfg['PlatformInfo']['Generic'] = {
    'AdviseFeatures': False,
    'MaxBIOSVersion': False,
    'MLB': 'CHANGE_ME_MLB',
    'ProcessorType': 0,
    'ROM': bytes.fromhex('112233445566'),
    'SpoofVendor': True,
    'SystemMemoryStatus': 'Auto',
    'SystemProductName': 'MacBookPro16,2',
    'SystemSerialNumber': 'CHANGE_ME_SERIAL',
    'SystemUUID': ''
}
cfg['PlatformInfo']['UpdateDataHub'] = True
cfg['PlatformInfo']['UpdateNVRAM'] = True
cfg['PlatformInfo']['UpdateSMBIOS'] = True
cfg['PlatformInfo']['UpdateSMBIOSMode'] = 'Custom'
cfg['PlatformInfo']['UseRawUuidEncoding'] = False

# === UEFI ===
cfg['UEFI']['APFS'] = {
    'EnableJumpstart': True,
    'GlobalConnect': False,
    'HideVerbose': False,
    'JumpstartHotPlug': False,
    'MinDate': -1,
    'MinVersion': -1
}
cfg['UEFI']['AppleInput'] = {
    'AppleEvent': 'Builtin',
    'CustomDelays': False,
    'GraphicsInputMirroring': True,
    'KeyInitialDelay': 50,
    'KeySubsequentDelay': 5,
    'PointerDwellClickTimeout': 0,
    'PointerDwellDoubleClickTimeout': 0,
    'PointerDwellRadius': 0,
    'PointerPollMask': -1,
    'PointerPollMax': 80,
    'PointerPollMin': 10,
    'PointerSpeedDiv': 1,
    'PointerSpeedMul': 1
}
cfg['UEFI']['Audio'] = {
    'AudioCodec': 0,
    'AudioDevice': 'PciRoot(0x0)/Pci(0x1f,0x3)',
    'AudioOutMask': 1,
    'AudioSupport': False,
    'DisconnectHda': False,
    'MaximumGain': -15,
    'MinimumAssistGain': -30,
    'MinimumAudibleGain': -55,
    'PlayChime': 'Auto',
    'ResetTrafficClass': False,
    'SetupDelay': 0
}
cfg['UEFI']['ConnectDrivers'] = True
cfg['UEFI']['Drivers'] = [
    {'Path': 'OpenRuntime.efi', 'Enabled': True, 'Arguments': '', 'Comment': 'OpenRuntime runtime services', 'HideVerbose': False, 'LoadEarly': False},
    {'Path': 'HfsPlus.efi', 'Enabled': True, 'Arguments': '', 'Comment': 'HFS+ filesystem driver', 'HideVerbose': False, 'LoadEarly': False},
    {'Path': 'ResetNvramEntry.efi', 'Enabled': True, 'Arguments': '', 'Comment': 'Reset NVRAM entry in picker', 'HideVerbose': False, 'LoadEarly': False}
]
cfg['UEFI']['Input'] = {
    'KeyFiltering': False,
    'KeyForgetThreshold': 5,
    'KeySupport': True,
    'KeySupportMode': 'Auto',
    'KeySwap': False,
    'PointerSupport': False,
    'PointerSupportMode': 'ASUS',
    'TimerResolution': 50000
}
cfg['UEFI']['Output'] = {
    'ClearScreenOnModeSwitch': False,
    'ConsoleFont': '',
    'ConsoleMode': '',
    'DirectGopRendering': False,
    'ForceResolution': False,
    'GopBurstMode': False,
    'GopPassThrough': 'Disabled',
    'IgnoreTextInGraphics': False,
    'InitialMode': 'Auto',
    'ProvideConsoleGop': True,
    'ReconnectGraphicsOnConnect': False,
    'ReconnectOnResChange': False,
    'ReplaceTabWithSpace': False,
    'Resolution': 'Max',
    'SanitiseClearScreen': False,
    'TextRenderer': 'BuiltinGraphics',
    'UgaPassThrough': False,
    'UIScale': 0
}
cfg['UEFI']['ProtocolOverrides'] = {
    'AppleAudio': False,
    'AppleBootPolicy': False,
    'AppleDebugLog': False,
    'AppleEg2Info': False,
    'AppleFramebufferInfo': False,
    'AppleImageConversion': False,
    'AppleImg4Verification': False,
    'AppleKeyMap': False,
    'AppleRtcRam': False,
    'AppleSecureBoot': False,
    'AppleSmcIo': False,
    'AppleUserInterfaceTheme': False,
    'DataHub': False,
    'DeviceProperties': False,
    'FirmwareVolume': True,
    'HashServices': False,
    'OSInfo': False,
    'PciIo': False,
    'UnicodeCollation': False
}
cfg['UEFI']['Quirks'] = {
    'ActivateHpetSupport': False,
    'DisableSecurityPolicy': False,
    'EnableVectorAcceleration': True,
    'EnableVmx': False,
    'ExitBootServicesDelay': 0,
    'ForceOcWriteFlash': False,
    'ForgeUefiSupport': False,
    'IgnoreInvalidFlexRatio': False,
    'ReleaseUsbOwnership': True,
    'ReloadOptionRoms': False,
    'RequestBootVarRouting': True,
    'ResizeGpuBars': 0,
    'ResizeUsePciRbIo': False,
    'ShimRetainProtocol': False,
    'TscSyncTimeout': 0,
    'UnblockFsConnect': True
}
cfg['UEFI']['ReservedMemory'] = []
cfg['UEFI']['Unload'] = []

# Write config.plist
with open('EFI/OC/config.plist', 'wb') as f:
    plistlib.dump(cfg, f)

print('Updated EFI/OC/config.plist with Alder Lake CPUID spoof and HP fixes.')
