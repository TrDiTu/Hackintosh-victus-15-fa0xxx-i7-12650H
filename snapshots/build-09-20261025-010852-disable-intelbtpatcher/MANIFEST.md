# build-09-20261025-010852-disable-intelbtpatcher

- created: 2026-10-25T01:08:52
- label: disable-intelbtpatcher
- known-good: true
- tree-sha256: 8fd1301031e6cbf0875bb7dfd6906ac1d89a67cb9eadb26b6e1efdd48f3f9ce2
- config.plist sha256: B40EEA9F7292AFA1C961D064E2B0A1B033BB71205E153ED0010F360B3F617694
- ocvalidate: 0 errors, 0 warnings; ocvalidate ran

## Notes / changes vs previous build
Disable IntelBTPatcher only: five UVCAssistant IOGMD panics implicate its USB request hook. Bluetooth may regress; boot success unverified.

## Kexts
- AppleALC.kext 1.9.8
- BlueToolFixup.kext 2.7.2
- BrightnessKeys.kext ?
- CpuTopologyRebuild.kext 2.0.2
- ECEnabler.kext 1.0.6
- IntelBluetoothFirmware.kext 2.4.0
- IntelBTPatcher.kext 2.4.0
- itlwm.kext 2.3.0
- Lilu.kext 1.7.2
- NVMeFix.kext 1.1.3
- RealtekRTL8111.kext 2.4.2
- RestrictEvents.kext 1.1.6
- SMCBatteryManager.kext 1.3.8
- SMCProcessor.kext 1.3.8
- USBToolBox.kext ?
- UTBDefault.kext 1.0
- VirtualSMC.kext 1.3.8
- VoodooI2C.kext 2.9.1
- VoodooI2CHID.kext 1.0
- VoodooPS2Controller.kext 2.3.7
- WhateverGreen.kext 1.7.1
