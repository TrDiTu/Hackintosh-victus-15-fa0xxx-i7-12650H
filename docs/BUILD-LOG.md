# BUILD-LOG — quyết định theo bản build

## Build 1 (đang dựng, 2026-11-02) — EFI nền Giai đoạn A, macOS 26.7.1 (25G241)

### SSDT (nguồn `docs/acpi-src/*.dsl`, biên dịch `iasl 20251212 -ve`: 0 lỗi)
Bằng chứng lấy từ DSDT/SSDT thật của máy (BIOS F.34, giải mã ở `_cache/acpi/`). Không chép AML/DSL của R1/JulioNectar/khucxtriendev.

| SSDT | Mục đích | Bằng chứng | Nguồn mẫu |
|---|---|---|---|
| SSDT-PLUG-ALT | Tạo đối tượng `Processor()` CP00..CP63 (chỉ Darwin) + `plugin-type=1` cho CP00; DSDT khai báo CPU dạng `Device (PRxx)` ACPI0007 (DSDT.dsl:30320, 64 cái) | 64 cảnh báo iasl "Legacy Processor() keyword" — dự kiến | Nguyên văn mẫu OpenCore 1.0.8 (BSD-3-Clause) |
| SSDT-EC-USBX | Thiết bị `EC` giả + `USBX`; giữ nguyên EC thật `\_SB.PC00.LPCB.EC0_` | acpi-devices.csv; không có `Device (EC)`/`USBX` sẵn | Mẫu OpenCore, đổi đường dẫn PC00.LPCB |
| SSDT-AWAC | `STAS = 1` khi Darwin → RTC bật, AWAC tắt | DSDT.dsl:2592 / 8477 / 87084 | Mẫu OpenCore SSDT-AWAC-DISABLE |
| SSDT-XOSI | macOS trả lời `_OSI("Windows 2018.2")` → OSYS 0x07E2 ≥ 0x07DC để `TPD0._CRS` trả tài nguyên ngắt chuẩn | DSDT.dsl:27932–27998; `TPD0._CRS` | Tự viết (danh sách chuỗi đúng DSDT, có `"Windows 2017.2 "` dấu cách cuối) |
| SSDT-DGPU-OFF | `PEGP._INI` gọi `PEGP._OFF` → `PEG1.PXP._OFF` khi Darwin | SSDT14.dsl:174/584, SSDT4.dsl:3615/3952–3966; PEGP chưa có `_INI` | Tự viết theo mẫu skill |
| SSDT-SBUS-MCHC | Thêm `MCHC` và `SBUS.BUS0` | DSDT.dsl:10058; không có MCHC/BUS0 | Mẫu OpenCore, PCI0→PC00, bỏ DVL0 |

**KHÔNG viết:**
- SSDT-GPI0: `GPI0._STA` trả 0x0F trừ khi `GPHD=1` (DSDT.dsl:13978–13986); Linux đo status 15 → GPHD=0 → không cần.
- SSDT-USB-Reset (refs có): chưa có lý do trên máy này; xét lại khi map USB.
- Patch RTC POST 005: chỉ khi gặp lỗi.

**ACPI/Patch đi kèm XOSI** (thêm bằng config-plist-tools): Find `5F4F5349` (`_OSI`) → Replace `584F5349` (`XOSI`), `TableSignature` = `44534454` (DSDT),
Count 0 (cả 16 chỗ đều ở DSDT: 15 lời gọi + 1 `CondRefOf(\_OSI)` → thành `CondRefOf(\XOSI)`, vẫn đúng vì XOSI có định nghĩa).
- 2026-11-02T01:38:11 plist_edit bootarg-add -vi2c-force-polling (config.plist)
- 2026-11-02T01:38:12 plist_edit bootarg-add -wegnoegpu (config.plist)
- 2026-11-02T01:38:43 plist_edit bootarg-add -vi2c-force-polling (config.plist)
- 2026-11-02T01:38:43 plist_edit bootarg-add -wegnoegpu (config.plist)
- 2026-11-02T01:38:44 plist_edit delete ACPI/Add[0] (config.plist)
- 2026-11-02T01:38:44 plist_edit delete ACPI/Add[0] (config.plist)
- 2026-11-02T01:38:44 plist_edit delete ACPI/Add[0] (config.plist)
- 2026-11-02T01:38:44 plist_edit delete ACPI/Add[0] (config.plist)
- 2026-11-02T01:38:44 plist_edit delete ACPI/Add[0] (config.plist)
- 2026-11-02T01:38:45 plist_edit delete ACPI/Add[0] (config.plist)
- 2026-11-02T01:38:45 plist_edit delete ACPI/Add[0] (config.plist)
- 2026-11-02T01:38:45 plist_edit delete ACPI/Add[0] (config.plist)
- 2026-11-02T01:38:45 plist_edit delete ACPI/Add[0] (config.plist)
- 2026-11-02T01:38:45 plist_edit delete ACPI/Add[0] (config.plist)
- 2026-11-02T01:38:45 plist_edit delete ACPI/Add[0] (config.plist)
- 2026-11-02T01:38:45 plist_edit delete ACPI/Add[0] (config.plist)
- 2026-11-02T01:38:45 plist_edit delete ACPI/Add[0] (config.plist)
- 2026-11-02T01:38:45 plist_edit delete ACPI/Add[0] (config.plist)
- 2026-11-02T01:38:45 plist_edit delete ACPI/Add[0] (config.plist)
- 2026-11-02T01:38:45 plist_edit delete ACPI/Add[0] (config.plist)
- 2026-11-02T01:38:45 plist_edit delete ACPI/Delete[0] (config.plist)
- 2026-11-02T01:38:45 plist_edit delete ACPI/Delete[0] (config.plist)
- 2026-11-02T01:38:45 plist_edit delete ACPI/Patch[0] (config.plist)
- 2026-11-02T01:38:45 plist_edit delete ACPI/Patch[0] (config.plist)
- 2026-11-02T01:38:45 plist_edit delete ACPI/Patch[0] (config.plist)
- 2026-11-02T01:38:46 plist_edit delete Kernel/Add[0] (config.plist)
- 2026-11-02T01:38:46 plist_edit delete Kernel/Add[0] (config.plist)
- 2026-11-02T01:38:46 plist_edit delete Kernel/Add[0] (config.plist)
- 2026-11-02T01:38:46 plist_edit delete Kernel/Add[0] (config.plist)
- 2026-11-02T01:38:46 plist_edit delete Kernel/Add[0] (config.plist)
- 2026-11-02T01:38:46 plist_edit delete Kernel/Add[0] (config.plist)
- 2026-11-02T01:38:46 plist_edit delete Kernel/Add[0] (config.plist)
- 2026-11-02T01:38:46 plist_edit delete Kernel/Add[0] (config.plist)
- 2026-11-02T01:38:46 plist_edit delete Kernel/Add[0] (config.plist)
- 2026-11-02T01:38:46 plist_edit delete Kernel/Add[0] (config.plist)
- 2026-11-02T01:38:46 plist_edit delete Kernel/Add[0] (config.plist)
- 2026-11-02T01:38:46 plist_edit delete Kernel/Add[0] (config.plist)
- 2026-11-02T01:38:46 plist_edit delete Kernel/Add[0] (config.plist)
- 2026-11-02T01:38:46 plist_edit delete Kernel/Add[0] (config.plist)
- 2026-11-02T01:38:46 plist_edit delete Kernel/Add[0] (config.plist)
- 2026-11-02T01:38:46 plist_edit delete Kernel/Add[0] (config.plist)
- 2026-11-02T01:38:47 plist_edit delete Kernel/Add[0] (config.plist)
- 2026-11-02T01:38:47 plist_edit delete Kernel/Add[0] (config.plist)
- 2026-11-02T01:38:47 plist_edit delete Kernel/Block[0] (config.plist)
- 2026-11-02T01:38:47 plist_edit delete Kernel/Block[0] (config.plist)
- 2026-11-02T01:38:47 plist_edit delete Kernel/Force[0] (config.plist)
- 2026-11-02T01:38:47 plist_edit delete Kernel/Force[0] (config.plist)
- 2026-11-02T01:38:47 plist_edit delete Kernel/Patch[0] (config.plist)
- 2026-11-02T01:38:47 plist_edit delete Kernel/Patch[0] (config.plist)
- 2026-11-02T01:38:47 plist_edit delete Kernel/Patch[0] (config.plist)
- 2026-11-02T01:38:47 plist_edit delete Kernel/Patch[0] (config.plist)
- 2026-11-02T01:38:47 plist_edit delete Kernel/Patch[0] (config.plist)
- 2026-11-02T01:38:47 plist_edit delete Kernel/Patch[0] (config.plist)
- 2026-11-02T01:38:47 plist_edit delete Kernel/Patch[0] (config.plist)
- 2026-11-02T01:38:47 plist_edit delete Kernel/Patch[0] (config.plist)
- 2026-11-02T01:38:47 plist_edit delete Kernel/Patch[0] (config.plist)
- 2026-11-02T01:38:47 plist_edit delete Kernel/Patch[0] (config.plist)
- 2026-11-02T01:38:48 plist_edit delete Kernel/Patch[0] (config.plist)
- 2026-11-02T01:38:48 plist_edit delete Kernel/Patch[0] (config.plist)
- 2026-11-02T01:38:48 plist_edit delete Kernel/Patch[0] (config.plist)
- 2026-11-02T01:38:48 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:48 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:48 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:48 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:48 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:48 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:48 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:48 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:48 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:48 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:48 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:48 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:48 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:49 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:49 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:49 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:49 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:49 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:49 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:49 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:49 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:49 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:49 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:49 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:49 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:49 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:49 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:49 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:49 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:49 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:49 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:50 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:50 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:50 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:50 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:50 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:50 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:50 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:50 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:50 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:50 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:50 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:50 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:50 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:50 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:50 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:50 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:50 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:50 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:50 plist_edit delete UEFI/Drivers[0] (config.plist)
- 2026-11-02T01:38:51 plist_edit delete Misc/Entries[0] (config.plist)
- 2026-11-02T01:38:51 plist_edit delete Misc/Tools[0] (config.plist)
- 2026-11-02T01:38:51 plist_edit delete Misc/Tools[0] (config.plist)
- 2026-11-02T01:38:51 plist_edit delete Misc/Tools[0] (config.plist)
- 2026-11-02T01:38:51 plist_edit delete DeviceProperties/Add/{PciRoot(0x0)/Pci(0x1b,0x0)} (config.plist)
- 2026-11-02T01:38:51 plist_edit append to ACPI/Add: Path=SSDT-PLUG-ALT.aml (config.plist)
- 2026-11-02T01:38:51 plist_edit append to ACPI/Add: Path=SSDT-EC-USBX.aml (config.plist)
- 2026-11-02T01:38:51 plist_edit append to ACPI/Add: Path=SSDT-AWAC.aml (config.plist)
- 2026-11-02T01:38:51 plist_edit append to ACPI/Add: Path=SSDT-XOSI.aml (config.plist)
- 2026-11-02T01:38:51 plist_edit append to ACPI/Add: Path=SSDT-DGPU-OFF.aml (config.plist)
- 2026-11-02T01:38:51 plist_edit append to ACPI/Add: Path=SSDT-SBUS-MCHC.aml (config.plist)
- 2026-11-02T01:38:51 plist_edit append to ACPI/Patch: Comment=_OSI to XOSI (DSDT only, 16 hits) - requires SSDT-XOSI (config.plist)
- 2026-11-02T01:38:51 plist_edit set Booter/Quirks/DevirtualiseMmio = True (config.plist)
- 2026-11-02T01:38:51 plist_edit set Booter/Quirks/EnableWriteUnprotector = False (config.plist)
- 2026-11-02T01:38:51 plist_edit set Booter/Quirks/ProtectUefiServices = True (config.plist)
- 2026-11-02T01:38:51 plist_edit set Booter/Quirks/RebuildAppleMemoryMap = True (config.plist)
- 2026-11-02T01:38:51 plist_edit set Booter/Quirks/SetupVirtualMap = False (config.plist)
- 2026-11-02T01:38:51 plist_edit set Booter/Quirks/SyncRuntimePermissions = True (config.plist)
- 2026-11-02T01:38:52 plist_edit set DeviceProperties/Add/{PciRoot(0x0)/Pci(0x2,0x0)}/AAPL,ig-platform-id = <data 0000499A> (config.plist)
- 2026-11-02T01:38:52 plist_edit set DeviceProperties/Add/{PciRoot(0x0)/Pci(0x2,0x0)}/device-id = <data 499A0000> (config.plist)
- 2026-11-02T01:38:52 plist_edit set DeviceProperties/Add/{PciRoot(0x0)/Pci(0x2,0x0)}/framebuffer-patch-enable = <data 01000000> (config.plist)
- 2026-11-02T01:38:52 plist_edit set DeviceProperties/Add/{PciRoot(0x0)/Pci(0x2,0x0)}/force-online = <data 01000000> (config.plist)
- 2026-11-02T01:38:52 plist_edit set DeviceProperties/Add/{PciRoot(0x0)/Pci(0x2,0x0)}/complete-modeset = <data 01000000> (config.plist)
- 2026-11-02T01:38:52 plist_edit set DeviceProperties/Add/{PciRoot(0x0)/Pci(0x2,0x0)}/enable-max-pixel-clock-override = <data 01000000> (config.plist)
- 2026-11-02T01:38:52 plist_edit set DeviceProperties/Add/{PciRoot(0x0)/Pci(0x2,0x0)}/rps-control = <data 01000000> (config.plist)
- 2026-11-02T01:38:52 plist_edit set DeviceProperties/Add/{PciRoot(0x0)/Pci(0x2,0x0)}/AAPL,slot-name = 'built-in' (config.plist)
- 2026-11-02T01:38:52 plist_edit set DeviceProperties/Add/{PciRoot(0x0)/Pci(0x2,0x0)}/built-in = <data 00> (config.plist)
- 2026-11-02T01:38:52 plist_edit set DeviceProperties/Add/{PciRoot(0x0)/Pci(0x1,0x0)/Pci(0x0,0x0)}/disable-gpu = <data 01000000> (config.plist)
- 2026-11-02T01:38:52 plist_edit append to Kernel/Add: BundlePath=Lilu.kext (config.plist)
- 2026-11-02T01:38:52 plist_edit append to Kernel/Add: BundlePath=VirtualSMC.kext (config.plist)
- 2026-11-02T01:38:52 plist_edit append to Kernel/Add: BundlePath=SMCProcessor.kext (config.plist)
- 2026-11-02T01:38:52 plist_edit append to Kernel/Add: BundlePath=ECEnabler.kext (config.plist)
- 2026-11-02T01:38:52 plist_edit append to Kernel/Add: BundlePath=SMCBatteryManager.kext (config.plist)
- 2026-11-02T01:38:52 plist_edit append to Kernel/Add: BundlePath=WhateverGreen.kext (config.plist)
- 2026-11-02T01:38:52 plist_edit append to Kernel/Add: BundlePath=RestrictEvents.kext (config.plist)
- 2026-11-02T01:38:52 plist_edit append to Kernel/Add: BundlePath=CpuTopologyRebuild.kext (config.plist)
- 2026-11-02T01:38:52 plist_edit append to Kernel/Add: BundlePath=NVMeFix.kext (config.plist)
- 2026-11-02T01:38:53 plist_edit append to Kernel/Add: BundlePath=BrightnessKeys.kext (config.plist)
- 2026-11-02T01:38:53 plist_edit append to Kernel/Add: BundlePath=RealtekRTL8111.kext (config.plist)
- 2026-11-02T01:38:53 plist_edit append to Kernel/Add: BundlePath=AirportItlwm.kext (config.plist)
- 2026-11-02T01:38:53 plist_edit append to Kernel/Add: BundlePath=XHCI-ADL-Injector.kext (config.plist)
- 2026-11-02T01:38:53 plist_edit append to Kernel/Add: BundlePath=USBToolBox.kext (config.plist)
- 2026-11-02T01:38:53 plist_edit append to Kernel/Add: BundlePath=UTBDefault.kext (config.plist)
- 2026-11-02T01:38:53 plist_edit append to Kernel/Add: BundlePath=VoodooPS2Controller.kext (config.plist)
- 2026-11-02T01:38:53 plist_edit append to Kernel/Add: BundlePath=VoodooPS2Controller.kext/Contents/PlugIns/VoodooPS2Keyboard.kext (config.plist)
- 2026-11-02T01:38:53 plist_edit append to Kernel/Add: BundlePath=VoodooI2C.kext/Contents/PlugIns/VoodooGPIO.kext (config.plist)
- 2026-11-02T01:38:53 plist_edit append to Kernel/Add: BundlePath=VoodooI2C.kext/Contents/PlugIns/VoodooI2CServices.kext (config.plist)
- 2026-11-02T01:38:53 plist_edit append to Kernel/Add: BundlePath=VoodooI2C.kext/Contents/PlugIns/VoodooInput.kext (config.plist)
- 2026-11-02T01:38:53 plist_edit append to Kernel/Add: BundlePath=VoodooI2C.kext (config.plist)
- 2026-11-02T01:38:53 plist_edit append to Kernel/Add: BundlePath=VoodooI2CHID.kext (config.plist)
- 2026-11-02T01:38:53 plist_edit set Kernel/Emulate/Cpuid1Data = <data 55060A00000000000000000000000000> (config.plist)
- 2026-11-02T01:38:53 plist_edit set Kernel/Emulate/Cpuid1Mask = <data FFFFFFFF000000000000000000000000> (config.plist)
- 2026-11-02T01:38:53 plist_edit set Kernel/Quirks/AppleXcpmCfgLock = True (config.plist)
- 2026-11-02T01:38:53 plist_edit set Kernel/Quirks/DisableIoMapper = True (config.plist)
- 2026-11-02T01:38:53 plist_edit set Kernel/Quirks/ProvideCurrentCpuInfo = True (config.plist)
- 2026-11-02T01:38:54 plist_edit set Kernel/Quirks/PanicNoKextDump = True (config.plist)
- 2026-11-02T01:38:54 plist_edit set Kernel/Quirks/PowerTimeoutKernelPanic = True (config.plist)
- 2026-11-02T01:38:54 plist_edit set Misc/Boot/HideAuxiliary = False (config.plist)
- 2026-11-02T01:38:54 plist_edit set Misc/Boot/PollAppleHotKeys = True (config.plist)
- 2026-11-02T01:38:54 plist_edit set Misc/Debug/AppleDebug = True (config.plist)
- 2026-11-02T01:38:54 plist_edit set Misc/Debug/ApplePanic = True (config.plist)
- 2026-11-02T01:38:54 plist_edit set Misc/Debug/DisableWatchDog = True (config.plist)
- 2026-11-02T01:38:54 plist_edit set Misc/Security/AllowSetDefault = True (config.plist)
- 2026-11-02T01:38:54 plist_edit set Misc/Security/ScanPolicy = 0 (config.plist)
- 2026-11-02T01:38:54 plist_edit set Misc/Security/SecureBootModel = 'Disabled' (config.plist)
- 2026-11-02T01:38:54 plist_edit set Misc/Security/Vault = 'Optional' (config.plist)
- 2026-11-02T01:38:54 plist_edit bootarg-add debug=0x100 (config.plist)
- 2026-11-02T01:38:54 plist_edit bootarg-add -vi2c-force-polling (config.plist)
- 2026-11-02T01:38:54 plist_edit bootarg-add -wegnoegpu (config.plist)
- 2026-11-02T01:38:54 plist_edit set NVRAM/Add/7C436110-AB2A-4BBB-A880-FE41995C9F82/prev-lang:kbd = <data 656E2D55533A30> (config.plist)
- 2026-11-02T01:38:54 plist_edit set NVRAM/Add/4D1FDA02-38C7-4A6A-9CC6-4BCCA8B30102/revpatch = 'cpuname' (config.plist)
- 2026-11-02T01:38:54 plist_edit set NVRAM/Add/4D1FDA02-38C7-4A6A-9CC6-4BCCA8B30102/revcpuname = 'Intel Core i7-12650H' (config.plist)
- 2026-11-02T01:38:54 plist_edit set NVRAM/Add/4D1FDA02-38C7-4A6A-9CC6-4BCCA8B30102/revcpu = 1 (config.plist)
- 2026-11-02T01:38:55 plist_edit set PlatformInfo/Generic/SystemProductName = 'MacBookPro16,2' (config.plist)
- 2026-11-02T01:38:55 plist_edit set PlatformInfo/Generic/SystemSerialNumber = <masked> (config.plist)
- 2026-11-02T01:38:55 plist_edit set PlatformInfo/Generic/MLB = <masked> (config.plist)
- 2026-11-02T01:38:55 plist_edit append to UEFI/Drivers: Path=OpenRuntime.efi (config.plist)
- 2026-11-02T01:38:55 plist_edit append to UEFI/Drivers: Path=OpenHfsPlus.efi (config.plist)
- 2026-11-02T01:38:55 plist_edit append to UEFI/Drivers: Path=ResetNvramEntry.efi (config.plist)
- 2026-11-02T01:38:55 plist_edit set UEFI/Quirks/ReleaseUsbOwnership = True (config.plist)
- 2026-11-02T01:39:05 plist_edit append to NVRAM/Delete/4D1FDA02-38C7-4A6A-9CC6-4BCCA8B30102: item (config.plist)
- 2026-11-02T01:39:05 plist_edit append to NVRAM/Delete/4D1FDA02-38C7-4A6A-9CC6-4BCCA8B30102: item (config.plist)
- 2026-11-02T01:39:05 plist_edit append to NVRAM/Delete/4D1FDA02-38C7-4A6A-9CC6-4BCCA8B30102: item (config.plist)
- 2026-11-02T01:39:05 plist_edit append to NVRAM/Delete/7C436110-AB2A-4BBB-A880-FE41995C9F82: item (config.plist)
- 2026-11-02T01:39:05 plist_edit append to NVRAM/Delete/7C436110-AB2A-4BBB-A880-FE41995C9F82: item (config.plist)

### config.plist (từ `Docs/Sample.plist` của OpenCore 1.0.8; sửa bằng `plist_edit.py`)
Nguồn quyết định: DRIVER-MATRIX đã duyệt, Dortania (Alder Lake laptop), config-install.plist của JulioNectar (T1, cấu hình KHÔNG tăng tốc), dữ kiện dump của máy.
- Xoá mọi mục mẫu (ACPI/Add|Delete|Patch, Kernel/Add|Block|Force|Patch, UEFI/Drivers, Misc/Entries|Tools, DP Pci(0x1b,0x0)).
- ACPI: 6 SSDT ở trên + patch `_OSI`→`XOSI` chỉ trên DSDT.
- Booter/Quirks: DevirtualiseMmio, ProtectUefiServices, RebuildAppleMemoryMap, SyncRuntimePermissions = true; EnableWriteUnprotector, SetupVirtualMap = false (Dortania ADL/JulioNectar).
- Kernel/Emulate: Cpuid1Data `55060A00…`/Mask `FFFFFFFF…` (spoof Comet Lake theo Dortania cho Alder Lake). ProvideCurrentCpuInfo = true (CPU lai).
- Kernel/Quirks: AppleXcpmCfgLock = true (CFG Lock bật, MSR 0xE2 bit15 = 1 trong dump); PanicNoKextDump, PowerTimeoutKernelPanic = true.
- **DisableIoMapper = true** (đổi so với ghi chú DRIVER-MATRIX `false`): INSTALL.md AirportItlwm-Tahoe — cấu hình "conventional" `true` là cấu hình KGP vẫn khuyên dùng và đã PASS trên 25G83; đường AppleVTD (`false`) đòi xác minh AppleVTD chạy thật và "không suy ra một quirk là đủ cho máy tuỳ ý" → chọn ít rủi ro cho build đầu. RealtekRTL8111 3.0.0 chạy được cả hai.
- Kernel/Add (22 mục, thứ tự): Lilu → VirtualSMC → SMCProcessor → ECEnabler → SMCBatteryManager → WhateverGreen → RestrictEvents → CpuTopologyRebuild → NVMeFix → BrightnessKeys → RealtekRTL8111 → AirportItlwm → XHCI-ADL-Injector → USBToolBox → UTBDefault → VoodooPS2Controller → VoodooPS2Keyboard (KHÔNG nạp VoodooInput/Mouse/Trackpad của PS2) → VoodooGPIO → VoodooI2CServices → VoodooInput (của VoodooI2C) → VoodooI2C → VoodooI2CHID. Không có AppleALC/Bluetooth (người dùng tạm bỏ qua).
- XHCI-ADL-Injector.kext: tự viết, chỉ Info.plist, 1 personality `0x51ed8086` → `AppleUSBXHCISPT` (IOProbeScore 900). Thay cho XHCI-unsupported (không có release).
- UTBDefault: map tạm (mở mọi cổng) để người dùng chạy công cụ USBToolBox trên MÁY B → thay bằng UTBMap.kext.
- DeviceProperties iGPU `PciRoot(0x0)/Pci(0x2,0x0)`: spoof TGL `device-id 499A0000`, `AAPL,ig-platform-id 0000499A`, `framebuffer-patch-enable`, `force-online`, `complete-modeset`, `enable-max-pixel-clock-override`, `rps-control`, `AAPL,slot-name`, `built-in` — **chép theo config-install.plist (không tăng tốc) của JulioNectar**; Tahoe không có driver TGL/ADL nên Giai đoạn A chỉ có framebuffer không tăng tốc. CHƯA XÁC MINH trên máy này. Không thêm `model`, `hda-gfx` (không có audio).
- dGPU `PciRoot(0x0)/Pci(0x1,0x0)/Pci(0x0,0x0)` (01:00.0 dưới 00:01.0): `disable-gpu` + boot-arg `-wegnoegpu` — dự phòng cho SSDT-DGPU-OFF.
- boot-args: `-v keepsyms=1 debug=0x100 -vi2c-force-polling -wegnoegpu`. **Không** hạ AMFI. Polling touchpad là dự phòng an toàn (JulioNectar install config cũng dùng); bỏ cờ này để thử ngắt GPIO sau khi touchpad chạy.
- csr-active-config giữ `00000000` (SIP bật). Root patch Wi-Fi (OCLP-CustoMac) sẽ cần hạ SIP — làm ở bước runbook, cần người dùng đồng ý.
- NVRAM: `prev-lang:kbd` = `en-US:0`; RestrictEvents `revpatch=cpuname`, `revcpuname="Intel Core i7-12650H"`, `revcpu=1`; thêm các khoá này vào NVRAM/Delete.
- Misc/Security: SecureBootModel Disabled (cần cho root patch OCLP), Vault Optional, ScanPolicy 0, AllowSetDefault true. Misc/Boot: HideAuxiliary false, PollAppleHotKeys true. Misc/Debug: AppleDebug, ApplePanic, DisableWatchDog = true; Target 3.
- PlatformInfo: MacBookPro16,2; placeholder `CHANGE_ME_SERIAL`/`CHANGE_ME_MLB`/UUID 0. **ROM vẫn là giá trị mẫu `112233445566` của Sample.plist**: `plist_edit.py` từ chối cả ROM toàn 0 (guard chỉ nhận placeholder dạng chuỗi, ROM là data) — lỗi nhỏ của công cụ, chưa sửa.
- UEFI/Drivers: OpenRuntime, OpenHfsPlus (bản OpenCore, không dùng HfsPlus.efi của Apple), ResetNvramEntry. ReleaseUsbOwnership = true.

### Validate
- `efi-validate` 2026-11-02T01:39:18: 0 lỗi, 0 cảnh báo; ocvalidate 1.0.8 "No issues found" (docs/validation/validate-20261102T013918.md).
- 2026-11-02T01:40:07 Created build-01-20261102-014007-base-a1 (tree 7a5cf1515de4, ocvalidate: 0 errors, 0 warnings)
- 2026-11-02T01:47:41 plist_edit delete DeviceProperties/Add/{PciRoot(0x0)/Pci(0x2,0x0)} (config.plist)
- 2026-11-02T01:47:42 plist_edit set PlatformInfo/Generic/ROM = <masked> (config.plist)

## Build 2 (2026-11-02) — sửa build-01 theo PROMPT.md sau khi rà toàn bộ workspace
- **Gỡ spoof iGPU** (`DeviceProperties/Add/PciRoot(0x0)/Pci(0x2,0x0)`, 9 khoá): PROMPT.md Pha 2 yêu cầu Giai đoạn A "không spoof, không NootedGreen, chỉ framebuffer firmware". Build-01 đã trái yêu cầu này.
- **ROM** = 6 byte 0 (placeholder chuẩn của `smbios.py`). Build-01 để `112233445566` → `usb-deploy-guard` sẽ từ chối tiêm SMBIOS.
- Sửa `plist_edit.py` `guard_secret`: chấp nhận data toàn byte 0 là placeholder (trùng định nghĩa `tools/lib/smbios.is_placeholder`); giá trị thật vẫn bị chặn (đã thử `112233445577` → ERROR).
- Thêm `EFI/OC/config-install.plist` giống hệt `config.plist` (PROMPT.md Pha 3, đường lui cho Giai đoạn B).
- Thêm `docs/GPU-STRATEGY.md` (PROMPT.md Pha 2).
- Giữ nguyên: SSDT, kext, quirk, boot-args, dGPU `disable-gpu` + `-wegnoegpu`.
- 2026-11-02T01:48:22 Created build-02-20261102-014822-base-a2-nospoof (tree 219fb63c2131, ocvalidate: 0 errors, 0 warnings)
- 2026-11-02T01:53:08 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree f76a0fae1d13, verified)
- 2026-11-02T01:56:55 plist_edit set Misc/Debug/Target = 67 (config.plist)
- 2026-11-02T01:56:55 plist_edit set Misc/Debug/DisplayLevel = 2147483714 (config.plist)

## Build 3 (2026-11-02) — bản CHẨN ĐOÁN cho lỗi treo ở OpenCore (build-02)
- Người dùng báo: build-02 "bị treo ở OpenCore nhưng không có log". Build-02 dùng OpenCore RELEASE + `Misc/Debug/Target 3` → không ghi file log.
- Thay `BOOTx64.efi`, `OpenCore.efi`, `OpenRuntime.efi`, `OpenHfsPlus.efi`, `ResetNvramEntry.efi` bằng bản **DEBUG** của OpenCore 1.0.8
  (`OpenCore-1.0.8-DEBUG.zip`, release chính thức, ghi ở SOURCES.md; giải nén riêng vào `extracted-debug/`).
- `Misc/Debug/Target` 3 → **67** (bật log + màn hình + ghi file `opencore-YYYY-MM-DD-HHMMSS.txt` vào gốc phân vùng EFI chứa OpenCore = MACEFI).
- `Misc/Debug/DisplayLevel` → **2147483714** (0x80000042: ERROR + WARN + INFO). AppleDebug/ApplePanic/DisableWatchDog đã bật từ build-01.
- KHÔNG đổi kext/SSDT/quirk/boot-args → lần treo tiếp theo vẫn phản ánh đúng cấu hình build-02.
- `config-install.plist` chép lại giống hệt.
- 2026-11-02T01:57:08 Created build-03-20261102-015708-debug-a3 (tree 2fa322c6b9da, ocvalidate: 0 errors, 0 warnings)
- 2026-11-02T01:58:52 plist_edit set Booter/Quirks/SetupVirtualMap = True (config.plist)

## Build 4 (2026-11-02) — thử sửa treo `EXITBS:START` (build-02/03)
- Người dùng: treo sau khi chọn ổ macOS, dòng cuối `EXITBS:START`, không có verbose kernel.
- Bằng chứng: R1 (cùng board 8A4F, BIOS khác có thể) dùng `Booter/Quirks/SetupVirtualMap = true` và tới được Recovery GUI (mức B).
  nullmoth/1401 #97 (ADL-H + 46A3 + RTX 3050, PEG1.PEGP, cùng chữ ký treo) không ghi cách sửa; đã loại trừ ở đó: patch topology XNU, bỏ CpuTopologyRebuild, bỏ disable-gpu iGPU.
- Thay đổi DUY NHẤT so với build-03: `SetupVirtualMap` false → **true**. Vẫn là OpenCore DEBUG + Target 67 (ghi `opencore-*.txt` lên MACEFI).
- Ứng viên tiếp theo nếu vẫn treo (chưa áp dụng, mỗi lần một thay đổi): `Cpuid1Data/Mask` kiểu JulioNectar (EBX[23:16]=0x80), `ResizeAppleGpuBars`, `-igfxvesa`, xem log debug.
- 2026-11-02T01:58:52 Created build-04-20261102-015852-exitbs-svm-a4 (tree 4a0869faa85c, ocvalidate: 0 errors, 0 warnings)
- 2026-11-02T01:58:52 Rotated out (deleted) oldest snapshot build-01-20261102-014007-base-a1
- 2026-11-02T02:00:22 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 92de4061e75e, verified)
- 2026-11-02T02:14:21 plist_edit set Misc/Debug/Target = 3 (config.plist)
- 2026-11-02T02:14:21 plist_edit set Misc/Debug/DisplayLevel = 2147483650 (config.plist)

## Kết quả build-04 (2026-11-02)
- Người dùng: **"hoạt động rồi"** — build-04 qua được `EXITBS:START` trên MÁY B. Nguyên nhân treo của build-02/03: `Booter/Quirks/SetupVirtualMap = false`.
  Chưa có chi tiết thiết bị nào hoạt động (chờ TEST-PLAN). Log debug của lần boot này chưa đọc được (USB chưa mount trên MÁY A).

## Build 5 (2026-11-02) — RELEASE + SetupVirtualMap=true
- Theo yêu cầu người dùng "quay về build release": BOOTx64.efi, OpenCore.efi, OpenRuntime/OpenHfsPlus/ResetNvramEntry → bản RELEASE 1.0.8 (giống build-02, đã so `cmp`).
- `Misc/Debug/Target` 67 → 3, `DisplayLevel` → 2147483650 (giá trị Sample.plist).
- So với build-02: chỉ khác `Booter/Quirks/SetupVirtualMap = true` (đã kiểm bằng plist_diff + diff -rq).
- 2026-11-02T02:14:34 Created build-05-20261102-021434-release-svm-a5 (tree 6e9f06993652, ocvalidate: 0 errors, 0 warnings)
- 2026-11-02T02:14:34 Rotated out (deleted) oldest snapshot build-02-20261102-014822-base-a2-nospoof
- 2026-11-02T02:19:47 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 37ec6ee94ea2, verified)

## Log OpenCore DEBUG của lần boot build-04 (opencore-2026-11-01-190124.txt, lưu ở `_cache/logs/`)
- Mọi kext `Prelinked injection ... Success`, **trừ AirportItlwm**: `OCAK: com.apple.iokit.IO80211FamilyLegacy not in Boot KC, using kernel stub for symbol-only deps` →
  `OCAK: Vtable patching failed for kext com.zxystd.AirportItlwm` → `Invalid Parameter`. ⇒ **Wi-Fi không nạp được** với EFI hiện tại.
  Nguyên nhân: AirportItlwm-Tahoe phụ thuộc `IO80211FamilyLegacy` (môi trường Wi-Fi Ventura do OCLP-CustoMac khôi phục), không có trong Boot KC. Cần nghiên cứu cách OCLP-CustoMac cung cấp (INSTALL.md).
- `OCAK: [OK] Patch success com.apple.iokit.IOPCIFamily AppleIoMapper` (DisableIoMapper=true có tác dụng). `Prelinked status - Success`. Các dòng `OCBP ... Not Found` là quét phân vùng bình thường.
- RealtekRTL8111.kext tự báo `v3.0.4` trong Info.plist dù release tag là v3.0.0 (bản phát hành chính thức, đã kiểm digest).

## Ghi build-05 lên USB (2026-11-02): MACEFI `/dev/sdb3`, tree 37ec6ee94ea2, kiểm hash OK, SMBIOS thật tiêm.
- 2026-11-02T02:26:44 plist_edit append to Kernel/Add: BundlePath=AMFIPass.kext (config.plist)
- 2026-11-02T02:26:44 plist_edit append to Kernel/Add: BundlePath=IOSkywalkFamily.kext (config.plist)
- 2026-11-02T02:26:44 plist_edit append to Kernel/Add: BundlePath=IO80211FamilyLegacy.kext (config.plist)
- 2026-11-02T02:26:44 plist_edit append to Kernel/Add: BundlePath=IO80211FamilyLegacy.kext/Contents/PlugIns/AirPortBrcmNIC.kext (config.plist)
- 2026-11-02T02:26:44 plist_edit move Kernel/Add[BundlePath=AMFIPass.kext] to position 11 (config.plist)
- 2026-11-02T02:26:44 plist_edit move Kernel/Add[BundlePath=IOSkywalkFamily.kext] to position 12 (config.plist)
- 2026-11-02T02:26:44 plist_edit move Kernel/Add[BundlePath=IO80211FamilyLegacy.kext] to position 13 (config.plist)
- 2026-11-02T02:26:44 plist_edit move Kernel/Add[BundlePath=IO80211FamilyLegacy.kext/Contents/PlugIns/AirPortBrcmNIC.kext] to position 14 (config.plist)
- 2026-11-02T02:26:44 plist_edit append to Kernel/Block: Identifier=com.apple.iokit.IOSkywalkFamily (config.plist)
- 2026-11-02T02:26:44 plist_edit bootarg-add -amfipassbeta (config.plist)
- 2026-11-02T02:26:44 plist_edit set NVRAM/Add/7C436110-AB2A-4BBB-A880-FE41995C9F82/csr-active-config = <data 03080000> (config.plist)

## Kết quả build-05 (người dùng, 2026-11-02): "tất cả đều hoạt động" (bàn phím, touchpad, Ethernet, pin, dGPU tắt, USB, khởi động lại). `csrutil status`: enabled. Wi-Fi: không (dự kiến, xem log build-04).

## Build 6 (2026-11-02) — Wi-Fi AirportItlwm-Tahoe theo môi trường OCLP-CustoMac (người dùng duyệt đề xuất cuối DRIVER-MATRIX)
- Kext mới (từ `payloads/` của kgp-macPro/OCLP-CustoMac @ f2bbcef, git blob khớp, SHA-256 ở SOURCES.md):
  AMFIPass 1.4.1 (Min 20.0.0, cần Lilu), IOSkywalkFamily 1.2.0 (Min 23.0.0), IO80211FamilyLegacy 1.0.0 (Min 23.0.0), plugin AirPortBrcmNIC **tắt** (chỉ Broadcom).
  Giá trị MinKernel/thứ tự theo `payloads/Config/config.plist` + `efi_builder/networking/wireless.py` L55–58.
- Thứ tự: … RealtekRTL8111 → AMFIPass → IOSkywalkFamily → IO80211FamilyLegacy → (AirPortBrcmNIC tắt) → AirportItlwm → …
- Kernel/Block: `com.apple.iokit.IOSkywalkFamily`, Strategy Exclude, MinKernel 23.0.0 (chặn bản gốc Tahoe).
- boot-args thêm `-amfipassbeta` (README OCLP-CustoMac: cấu hình đã kiểm định, không cần `amfi=0x80`).
- **SIP hạ: `csr-active-config` 00000000 → 03080000** (giá trị OCLP-CustoMac `efi_builder/security.py` L56). Hệ quả bảo mật (người dùng đã đồng ý): AMFI được AMFIPass vượt, SIP không còn bảo vệ hệ thống/kext; cập nhật macOS xoá root patch.
- Còn lại giữ nguyên build-05. Root patch "Modern Wireless" phải chạy bằng app OCLP-CustoMac 3.0.3 trên MÁY B SAU khi boot build-06.
- 2026-11-02T02:27:25 Created build-06-20261102-022725-wifi-oclp-a6 (tree 502748b82578, ocvalidate: 0 errors, 0 warnings)
- 2026-11-02T02:27:25 Rotated out (deleted) oldest snapshot build-03-20261102-015708-debug-a3
- 2026-11-02T02:29:15 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 07ef92da3544, verified)
- 2026-11-02T02:29:26 Marked build-05-20261102-021434-release-svm-a5 as known-good (user request)

## 2026-11-02: build-06 ghi lên MACEFI (tree 07ef92da3544, kiểm hash OK). Người dùng đánh dấu **build-05 known-good**.
- 2026-11-02T02:34:47 plist_edit set Kernel/Quirks/DisableIoMapper = False (config.plist)

## Build 7 (2026-11-02) — AppleVTD: DisableIoMapper = false
- Người dùng chỉ ra INSTALL.md AirportItlwm-Tahoe: "The AppleVTD-capable qualification used OpenCore Kernel → Quirks → DisableIoMapper=false".
- Đánh giá lại README: AppleVTD (`false`) = "FULL PHYSICAL + RUNTIME PASS; release gate" trên 25G83 có runtime capture, và là cấu hình DUY NHẤT có PASS bổ sung trên 26.7 (25G229, gần 25G241 nhất);
  `true` chỉ "KGP-controlled / USER-OBSERVED" trên 25G83. VT-d bật trong BIOS (dump DMAR); RealtekRTL8111 3.0.0 hỗ trợ AppleVTD trên Tahoe (release notes).
- Thay đổi DUY NHẤT so với build-06: `Kernel/Quirks/DisableIoMapper` true → **false**. Quay lại: build-06 (true) hoặc build-05 (known-good).
- Kiểm trên MÁY B: `ioreg -r -c AppleVTD -l -w0`, `ioreg -r -c AppleVTDDeviceMapper -l -w0` (INSTALL.md) — AppleVTD phải hiện.
- 2026-11-02T02:34:48 Created build-07-20261102-023448-applevtd-a7 (tree d38d6e280fc1, ocvalidate: 0 errors, 0 warnings)
- 2026-11-02T02:34:48 Rotated out (deleted) oldest snapshot build-04-20261102-015852-exitbs-svm-a4
- 2026-11-02T02:35:50 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 619fc844aeb2, verified)

## 2026-11-02: build-07 ghi lên MACEFI (tree 619fc844aeb2, kiểm hash OK; USB DisableIoMapper=False).
- 2026-11-02T02:45:06 plist_edit set Kernel/Quirks/DisableIoMapper = True (config.plist)

## Kết quả build-07 (người dùng, 2026-11-02)
- `csrutil status`: unknown (Apple Internal / Kext Signing / Filesystem Protection disabled) → csr 0x803 có hiệu lực.
- Wi-Fi: công tắc bật/tắt được (AirportItlwm đã nạp) nhưng **không thấy mạng**. **Ethernet KHÔNG hoạt động** (build-05 thì có).
- Nhận định (CHƯA XÁC MINH, chưa có log): AppleVTD (`DisableIoMapper=false`) làm hỏng DMA của thiết bị PCIe trên máy này (cả RTL8111 lẫn AX210).
  Chưa rõ người dùng đã root patch Modern Wireless chưa (Ethernet hỏng → khó tải OCLP-CustoMac).
- Thử đối chứng: quay về **build-06** (DisableIoMapper=true, còn lại giống build-07). EFI dự án đặt lại `DisableIoMapper=true` → giống hệt snapshot build-06 (diff -rq rỗng).

## Đính chính 2026-11-02 (người dùng): **Ethernet KHÔNG hoạt động ở MỌI build** (kể cả build-05; báo "tất cả hoạt động" trước đó là nhầm).
- Giả thuyết "AppleVTD làm hỏng Ethernet" (mục kết quả build-07) **không còn căn cứ**. Wi-Fi không quét được mạng: nguyên nhân CHƯA XÁC ĐỊNH (chưa rõ đã root patch chưa).
- build-05 known-good: đúng với mọi thành phần **trừ Ethernet và Wi-Fi**.
- Bằng chứng Ethernet: Mieze issue #96 (macOS 26.3.1): "V3.0.0 DO not work ... but V2.4.2 can work" (status inactive, không IP — trùng triệu chứng);
  Mieze trả lời #93: Tahoe đổi AppleVTD, có thể phải tắt; rollback IOSkywalkFamily (cho Wi-Fi) "may cause my drivers to fail with AppleVTD".
  Chip máy: 10ec:8168 rev 0x16 (lspci); dump không có dòng dmesg r8169 → chưa biết tên chip đúng.
- Đề xuất build-08 (chờ duyệt): = build-06 (DisableIoMapper=true) + RealtekRTL8111 **2.4.2** (release chính thức Mieze, không AppleVTD).
- 2026-11-02T02:50:48 plist_edit set Kernel/Add[BundlePath=AirportItlwm.kext]/Comment = 'AirportItlwm-Tahoe 1.1.0-beta.1 ZC28-SERVICE (kgp-macPro) - AX210 25G241 conventional' (config.plist)
- 2026-11-02T02:50:48 plist_edit set Kernel/Add[BundlePath=RealtekRTL8111.kext]/Comment = 'RealtekRTL8111 2.4.2 (Mieze) - no AppleVTD, needs DisableIoMapper=true' (config.plist)

## Build 8 (2026-11-02) — Ethernet RTL8111 2.4.2 + AirportItlwm-Tahoe 1.1.0-beta.1 ZC28 (người dùng duyệt cả hai)
- RealtekRTL8111 v3.0.0 → **2.4.2** (release chính thức Mieze 2021-05-06; không có digest GitHub/hash tác giả → chỉ HTTPS; SHA-256 tự tính ở SOURCES.md). Lý do: Mieze #96.
- AirportItlwm-Tahoe 1.0.0 → **1.1.0-beta.1, biến thể B1-ZC28-SERVICE** (prerelease, người dùng yêu cầu "thử beta"; `--allow-prerelease`; zip SHA-256 khớp giá trị tác giả `e7d5c0ef…e31d`).
  Lý do chọn ZC28: `ZC28_CONVENTIONAL_ANALYSIS.txt` — chạy trên **AX210, macOS 26.7.1 (25G241), DMA Mode 1 (conventional = DisableIoMapper=true)**; "ZC28 is the first suggested campaign".
  Executable SHA-256 `c48b9a0a018e86f572a65166750f383f571133de5de4b9e7578e42129a1a1185` (khớp tài liệu tác giả), UUID tác giả ghi `469CBE97-EEB4-3084-99C4-433E73F4FC23` (kiểm bằng dwarfdump trên macOS).
  Yêu cầu môi trường (README_START_HERE): OCLP-CustoMac 3.0.3 + Skywalk replacement + AMFIPass/-amfipassbeta — đã có từ build-06. Có Info.plist khớp `0x27258086`.
  Không chạy `SETUP_AirportItlwm_Beta.command` (script của repo khác, dành cho macOS; người dùng tự quyết).
- Giữ: DisableIoMapper=true, IOSkywalkFamily/IO80211FamilyLegacy/Block/AMFIPass, SIP 0x803. Hai thay đổi trong một build theo yêu cầu người dùng → nếu một trong hai hỏng, tách ra ở build sau.
- 2026-11-02T02:52:25 Created build-08-20261102-025225-rtl242-zc28-a8 (tree 25bff1c5e4d6, ocvalidate: 0 errors, 0 warnings)
- 2026-11-02: người dùng cho xoá snapshot build-07 (AppleVTD) thủ công để giữ build-05 known-good; build-08 snapshot.
- 2026-11-02: người dùng chọn xoá thủ công snapshot build-06 để usb-deploy-guard sao lưu EFI build-07 trên USB (known-good build-05 là bản cũ nhất chặn xoay vòng).
- 2026-11-02T02:53:50 Created build-09-20261102-025350-usb-before-deploy (tree d38d6e280fc1, ocvalidate: n/a (existing USB content))
- 2026-11-02T02:54:25 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 3d36fd90ae3d, verified)

## Kết quả build-08 (người dùng, 2026-11-02)
- **Ethernet: có IP** (RealtekRTL8111 2.4.2) → xác nhận 3.0.0 là nguyên nhân Ethernet hỏng ở build-01…07.
- **Wi-Fi: hoạt động** sau khi chạy OpenCore-Patcher (OCLP-CustoMac 3.0.3) Post-Install Root Patch (Modern Wi-Fi) — AirportItlwm-Tahoe 1.1.0-beta.1 ZC28, DisableIoMapper=true.
- Chưa kiểm: Wi-Fi sau 3 lần khởi động lại, ổn định dài, sleep/wake; output kmutil/ioreg (POSTINSTALL-RUNBOOK §1 bước 7).
- Ghi nhớ: cập nhật macOS sẽ xoá root patch Wi-Fi → phải chạy lại OpenCore-Patcher.

## Kiểm tra Wi-Fi build-08 trên MÁY B (người dùng gửi output, 2026-11-02; MAC không ghi lại)
- `kmutil showloaded`: IOSkywalkFamily (1.0, bản Ventura từ EFI), AMFIPass (1.4.1), IO80211FamilyLegacy (1200.12.2b1), **com.zxystd.AirportItlwm (1.0.0) UUID 469CBE97-EEB4-3084-99C4-433E73F4FC23** = UUID tác giả ghi cho ZC28 → đúng binary.
- `ioreg AirportItlwm`: registered/matched/active, `IOLinkStatus=3` (có link), `IOModel=iwlwifi-ty-a0-gf-a0-68.ucode`, `IO80211Family.BuildTag=IO80211Legacy_kexts-111.7`.
- `ifconfig -l`: lo0 gif0 stf0 XHC13 XHC20 en1 en0 awdl0 utun0-3 → Wi-Fi en0, awdl0 có.
- `ioreg AppleVTD` / `AppleVTDDeviceMapper`: rỗng — dự kiến với DisableIoMapper=true (conventional; tác giả ZC28 conventional cũng rỗng).
- Còn lại: khởi động lại 3 lần, `networkQuality`, sleep/wake (chưa kiểm).
- 2026-11-02T03:21:27 Marked build-08-20261102-025225-rtl242-zc28-a8 as known-good (user request)

## 2026-11-02 — build-08 KNOWN-GOOD (người dùng)
- Người dùng: khởi động lại 3 lần, Wi-Fi và Ethernet vẫn hoạt động; đã tắt tự động cập nhật macOS.
- Đánh dấu **build-08-20261102-025225-rtl242-zc28-a8 known-good**. Theo yêu cầu người dùng, xoá snapshot build-05 (known-good cũ, không có Ethernet/Wi-Fi).
- Snapshot còn: build-08 (known-good), build-09 (sao lưu EFI build-07 AppleVTD từ USB).
- 2026-11-02T03:36:59 plist_edit append to Kernel/Add: BundlePath=UTBMap.kext (config.plist)
- 2026-11-02T03:36:59 plist_edit delete Kernel/Add[BundlePath=UTBDefault.kext] (config.plist)
- 2026-11-02T03:37:00 plist_edit move Kernel/Add[BundlePath=UTBMap.kext] to position 18 (config.plist)

## Build 10 (2026-11-02) — USB map
- Người dùng tạo `UTBMap.kext` bằng USBToolBox (đặt ở gốc MACEFI). Bản gốc lưu `_cache/user-inputs/UTBMap-original.kext`.
- Nội dung: controller `XHCI` (IONameMatch), 5 cổng: HS01 port1 USB3(3), HS02 port2 USB3(3), HS03 port4 TypeC(9), HS04 port6, HS05 port7.
- **Sửa duy nhất**: HS04 (port 6 = camera `30C9:0069`) và HS05 (port 7 = Bluetooth `8087:0032`) UsbConnector 0 → **255 (Internal)** — theo lsusb dump (Bus 003 Port 006/007).
- Thiếu cổng SS (USB 3, PCH có 4 cổng SS) → USB 3 chạy tốc độ USB 2. Không tự thêm (không biết ánh xạ vật lý) → DEFERRED D3.
- Kernel/Add: thêm `UTBMap.kext` (không executable) ngay sau USBToolBox.kext; **gỡ UTBDefault.kext** (entry + file).
- Thêm `docs/DEFERRED.md` (các phần bỏ qua tạm).
- 2026-11-02: xoá snapshot build-09 (sao lưu tự động EFI build-07 AppleVTD đã bỏ) — Claude tự quản lý build theo ủy quyền người dùng.
- 2026-11-02T03:37:40 Created build-10-20261102-033740-usbmap-a10 (tree 3bd727bba335, ocvalidate: 0 errors, 0 warnings)
- 2026-11-02T03:37:43 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 1acd4c7be7ec, verified)
- 2026-11-02: build-10 ghi lên MACEFI (tree 1acd4c7be7ec, kiểm hash OK).

## Kết quả build-10 (người dùng, 2026-11-02)
- Camera không hoạt động (ghi DEFERRED D13). Còn lại ổn. Người dùng viết câu cổng: "EFI nền đã ổn định, bắt đầu tăng tốc đồ hoạ" → **mở Giai đoạn B**.
- `config-install.plist` (cấu hình không tăng tốc để quay về) = config build-10.
- 2026-11-02T15:01:32 plist_edit set DeviceProperties/Add/{PciRoot(0x0)/Pci(0x2,0x0)}/AAPL,ig-platform-id = <data 0000499A> (config.plist)
- 2026-11-02T15:01:32 plist_edit set DeviceProperties/Add/{PciRoot(0x0)/Pci(0x2,0x0)}/device-id = <data 499A0000> (config.plist)
- 2026-11-02T15:01:32 plist_edit set DeviceProperties/Add/{PciRoot(0x0)/Pci(0x2,0x0)}/framebuffer-patch-enable = <data 01000000> (config.plist)
- 2026-11-02T15:01:32 plist_edit set DeviceProperties/Add/{PciRoot(0x0)/Pci(0x2,0x0)}/force-online = <data 01000000> (config.plist)
- 2026-11-02T15:01:32 plist_edit set DeviceProperties/Add/{PciRoot(0x0)/Pci(0x2,0x0)}/complete-modeset = <data 01000000> (config.plist)
- 2026-11-02T15:01:32 plist_edit set DeviceProperties/Add/{PciRoot(0x0)/Pci(0x2,0x0)}/rps-control = <data 01000000> (config.plist)
- 2026-11-02T15:01:33 plist_edit set DeviceProperties/Add/{PciRoot(0x0)/Pci(0x2,0x0)}/enable-max-pixel-clock-override = <data 01000000> (config.plist)
- 2026-11-02T15:01:33 plist_edit set DeviceProperties/Add/{PciRoot(0x0)/Pci(0x2,0x0)}/AAPL,slot-name = 'built-in' (config.plist)
- 2026-11-02T15:01:33 plist_edit set DeviceProperties/Add/{PciRoot(0x0)/Pci(0x2,0x0)}/built-in = <data 00> (config.plist)
- 2026-11-02T15:01:33 plist_edit set NVRAM/Add/7C436110-AB2A-4BBB-A880-FE41995C9F82/csr-active-config = <data 130A0000> (config.plist)

## Build 11 — `graphics-prep` (2026-11-02, Giai đoạn B Pha 7) — người dùng duyệt GRAPHICS-PLAN cả 4 mục, đã sao lưu MÁY B
- = build-10 + DeviceProperties `PciRoot(0x0)/Pci(0x2,0x0)`: `device-id 499A0000`, `AAPL,ig-platform-id 0000499A`, `framebuffer-patch-enable`, `force-online`,
  `complete-modeset`, `rps-control`, `enable-max-pixel-clock-override` (01000000), `AAPL,slot-name built-in`, `built-in 00` (theo JN config.plist @6f03560; bỏ `model`, `hda-gfx`).
- `csr-active-config` 03080000 → **130A0000** (0x0A13, JN/khucx; chứa mọi bit 0x803).
- KHÔNG NootedGreen, KHÔNG thêm boot-arg đồ họa/AMFI (giống config-install của JN lúc cài). Mục đích duy nhất: chạy `install.sh` (L86–87 cần device-id 9A49).
- `config-install.plist` GIỮ NGUYÊN = config build-10 (không spoof, SIP 0x803) làm đường lui — từ build này hai file khác nhau có chủ đích.
- Runbook: `docs/GRAPHICS-RUNBOOK.md`.
- 2026-11-02T15:02:11 Created build-11-20261102-150211-graphics-prep-b11 (tree cfe24be8a5a6, ocvalidate: 0 errors, 0 warnings)
- 2026-11-02T15:03:53 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 98f0ac7e3104, verified)
- 2026-11-02: build-11 graphics-prep ghi lên MACEFI (tree 98f0ac7e3104, kiểm hash OK; USB device-id 499a0000, csr 130a0000).

## Kết quả build-11 graphics-prep (người dùng, 2026-11-02 15:08) — TREO ở verbose
- Ảnh: `logs/20261102_150831.jpg`. Dòng cuối: `KextLog: Loading Aux KC from file /Library/KernelCollections/AuxiliaryKernelExtensions.kc` → `Collection UUID matches with loaded KCs.` → đứng.
  Trước đó bình thường: RealtekRTL8111 link up en1, itlwm setPOWER + awdl0 (Wi-Fi), không panic. Có `disallowing unsupported code signature page shift: 14 / unable to create a validated cs_blob object: 85` (AMFI, ghi nhận).
- Nhận định (CHƯA XÁC MINH): AuxKC còn kext TGL/HookCase từ lần cài stack trước trên MÁY B (bộ nhớ .remember cho thấy các phiên trước từng chạy NootedGreen) →
  spoof 9A49 làm framebuffer/accelerator TGL khớp và chạy KHÔNG có NootedGreen → treo (đúng cảnh báo JN INSTALL.md L136–140). Sai sót kế hoạch: không kiểm AuxKC trước khi spoof.
- Hành động: EFI dự án về build-10 (config.plist = config-install.plist; diff -rq với snapshot build-10 rỗng; validate 0/0) để người dùng vào lại macOS và kiểm `/Library/Extensions`.
- 2026-11-02T15:13:32 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 1acd4c7be7ec, verified)
- 2026-11-02 15:13: ghi lại build-10 (EFI nền) lên MACEFI sau sự cố build-11.
- 2026-11-02 15:24: máy B đã gỡ stack cũ (install.sh --uninstall, sạch). EFI dự án đặt lại = build-11 graphics-prep (diff rỗng, validate 0/0); chờ ghi USB.
- 2026-11-02T15:25:22 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 98f0ac7e3104, verified)
- 2026-11-02 15:25: build-11 graphics-prep ghi lại lên MACEFI (thiết bị nay là /dev/sdc3, cùng USB 29,3 GB Ventoy/VTOYEFI/MACEFI; tree 98f0ac7e3104, kiểm hash OK).
- 2026-11-02T15:46:56 plist_edit append to Kernel/Add: BundlePath=NootedGreen.kext (config.plist)
- 2026-11-02T15:46:56 plist_edit move Kernel/Add[BundlePath=NootedGreen.kext] to position 6 (config.plist)
- 2026-11-02T15:46:57 plist_edit bootarg-add -- (config.plist)
- 2026-11-02T15:47:10 plist_edit bootarg-remove -- (config.plist)
- 2026-11-02T15:47:18 plist_edit bootarg-add IGLogLevel=3 (config.plist)
- 2026-11-02T15:47:18 plist_edit bootarg-add -ngreentglwithgfx (config.plist)
- 2026-11-02T15:47:18 plist_edit bootarg-add -allow3d (config.plist)
- 2026-11-02T15:47:18 plist_edit bootarg-add -disablegfxfirmware (config.plist)
- 2026-11-02T15:47:18 plist_edit bootarg-add ngreen-dmc=adlp (config.plist)
- 2026-11-02T15:47:18 plist_edit bootarg-add -ngreenv189 (config.plist)
- 2026-11-02T15:47:18 plist_edit bootarg-add -ngreenkeepefi (config.plist)
- 2026-11-02T15:47:18 plist_edit bootarg-add -ngreenxefix (config.plist)
- 2026-11-02T15:47:18 plist_edit bootarg-add -ngreenfixbootmode (config.plist)
- 2026-11-02T15:47:18 plist_edit bootarg-add amfi_get_out_of_my_way=1 (config.plist)
- 2026-11-02T15:47:18 plist_edit bootarg-add ngreenSched=4 (config.plist)
- 2026-11-02T15:47:18 plist_edit bootarg-add ngreenV142=3 (config.plist)
- 2026-11-02T15:47:19 plist_edit bootarg-add gfxrst=1 (config.plist)
- 2026-11-02T15:47:19 plist_edit bootarg-add ngreen-eu=64 (config.plist)
- 2026-11-02T15:47:19 plist_edit bootarg-add ngreen-l3=6 (config.plist)

## Build 12 — `graphics-v1` (2026-11-02, Giai đoạn B Pha 7)
- MÁY B: `install.sh` (JN 6f03560) first install OK — bundle 95f8189, build NootedGreen/HookCase/Metal driver/libxedrv/compiler, cài /Library. NootedGreen md5 **d805e6a6bd0d3f794c3f248e7097dca0**.
- NootedGreen.kext lấy từ gốc USB (người dùng chép), md5 khớp; lưu `_cache/user-inputs/NootedGreen-d805e6a6.kext`. Kernel/Add ngay sau WhateverGreen, MinKernel 25.0.0 (như JN).
- boot-args = nền (`-v keepsyms=1 debug=0x100 -vi2c-force-polling -wegnoegpu -amfipassbeta`) + GRAPHICS-PLAN §7:
  `IGLogLevel=3 -ngreentglwithgfx -allow3d -disablegfxfirmware ngreen-dmc=adlp -ngreenv189 -ngreenkeepefi -ngreenxefix -ngreenfixbootmode amfi_get_out_of_my_way=1 ngreenSched=4 ngreenV142=3 gfxrst=1 ngreen-eu=64 ngreen-l3=6`.
  (Lỗi thao tác đã sửa: lần đầu thêm nhầm một boot-arg `--`, đã gỡ.)
- Giữ: spoof 9A49, SIP 0x0A13, AMFIPass. `config-install.plist` = build-10 (không spoof) — đường lui an toàn.
- Snapshot: xoá build-11 graphics-prep — từ nay boot bản đó NGUY HIỂM (máy đã có TGL, bản đó không NootedGreen).
- 2026-11-02T15:47:37 Created build-12-20261102-154737-graphics-v1-b12 (tree 605dc525ea4b, ocvalidate: 0 errors, 0 warnings)
- 2026-11-02 15:48: người dùng yêu cầu xoá snapshot build-08 (known-good) thay vì build-10 → không còn snapshot known-good; đường lui: build-10 + config-install trong build-12.
- 2026-11-02T15:49:09 Created build-13-20261102-154909-usb-before-deploy (tree cfe24be8a5a6, ocvalidate: n/a (existing USB content))
- 2026-11-02T15:49:09 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 20a1e0ca0217, verified)
- 2026-11-02 15:49: build-12 graphics-v1 ghi lên MACEFI (/dev/sdc3, tree 20a1e0ca0217, kiểm hash OK; NootedGreen md5 d805e6a6 trên USB). Sao lưu USB cũ (build-11) = snapshot build-13.
- 2026-11-02T15:54:20 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 1acd4c7be7ec, verified)
- 2026-11-02 15:54: graphics-v1 KERNEL PANIC (người dùng). Ghi lại build-10 lên MACEFI (tree 1acd4c7be7ec) để lấy log panic.
- 2026-11-02T16:00:12 plist_edit set DeviceProperties/Add/{PciRoot(0x0)/Pci(0x1,0x0)/Pci(0x0,0x0)}/class-code = <data FFFFFFFF> (config.plist)

## Phân tích panic graphics-v1 (logs/Kernel-2026-11-02-155553.panic, uptime 54 s)
- `CR2 0xc78`, page fault; backtrace: `IOAccelTask::release+0x95 ← AppleIntelTGLGraphics IGAccelTask::withOptions+0x3e ← NootedGreen Gen11::igAccelTaskWithOptions+0x18
  ← IOGraphicsAccelerator2::start+0x15e1 ← IntelAccelerator::start+0x212 ← NootedGreen Gen11::start+0x1f74`. **Trùng chữ ký JN issue #24** (ADL-H + RTX 3060; đóng, không bản sửa).
- Hook JN `igAccelTaskWithOptions` (kern_gen11.cpp L6758–6815) chỉ xử lý khi hàm gốc TRẢ VỀ NULL; panic xảy ra BÊN TRONG hàm gốc → không có boot-arg né.
- Khác biệt với máy ADL-H + NVIDIA chạy được (khucxtriendev): dGPU `class-code FFFFFFFF` (roadmap-igpu.md L164/261) và NootedGreen R3 riêng (md5 5aacdaa5 ≠ JN 57294a16).

## Build 14 — `graphics-v2` (2026-11-02): = build-12 + dGPU `class-code = FFFFFFFF` (MỘT thay đổi; plist_diff 1 khác biệt)
- `PciRoot(0x0)/Pci(0x1,0x0)/Pci(0x0,0x0)`: `disable-gpu 01000000` + `class-code FFFFFFFF` (theo khucxtriendev). Giả thuyết độ tin cậy THẤP.
- Snapshot: xoá build-13 (sao lưu build-11 graphics-prep — nguy hiểm khi đã cài TGL).
- 2026-11-02T16:00:38 Created build-14-20261102-160038-graphics-v2-b14 (tree db869f375dc9, ocvalidate: 0 errors, 0 warnings)
- 2026-11-02T16:02:55 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 9032f77c1502, verified)
- 2026-11-02 16:02: build-14 graphics-v2 ghi lên MACEFI (/dev/sdc3).
- 2026-11-02 16:03: người dùng tăng giới hạn snapshot 3 → 10 (snapshot.py default --max 10; CLAUDE.md §3, efi-snapshot SKILL.md, PROMPT.md cập nhật).
- 2026-11-02 16:08: graphics-v2 panic (người dùng). Ghi lại build-10 lên MACEFI để lấy .panic.
- 2026-11-02T16:10:49 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 1acd4c7be7ec, verified)
- 2026-11-02 16:10: build-10 ghi lên MACEFI (/dev/sdc3, tree 1acd4c7be7ec, kiểm hash OK).
- 2026-11-02T16:22:52 plist_edit set Kernel/Add[BundlePath=NootedGreen.kext]/Comment = 'NootedGreen R3 (khucxtriendev release v3.0-booted, sha256 6b99b13c) - thu nghiem A1' (config.plist)

## Build 15 — `graphics-r3` (2026-11-02, hướng A người dùng chọn): = build-12 graphics-v1 + **NootedGreen R3** (khucxtriendev release v3.0-booted, sha256 6b99b13c)
- MỘT biến so với graphics-v1 (panic #24): binary NootedGreen. Config chỉ đổi Comment (plist_diff). Không `class-code` (để so trực tiếp với v1).
- User-space trên MÁY B vẫn là JN 6f03560 (không cài lại) — A1 chỉ kiểm phần kernel vượt qua `IntelAccelerator::start` hay không.
- 2026-11-02T16:23:14 Created build-15-20261102-162313-graphics-r3-b15 (tree 64c78317e2f1, ocvalidate: 0 errors, 0 warnings)
- 2026-11-02T16:33:47 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 11e814e4a8f4, verified)
- 2026-11-02 16:33: người dùng duyệt G1 (NootedGreen R3). build-15 graphics-r3 ghi lên MACEFI (/dev/sdd3, tree 11e814e4a8f4, kiểm hash OK; NootedGreen sha256 6b99b13c trên USB).
- 2026-11-02T16:43:40 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 1acd4c7be7ec, verified)
- 2026-11-02 16:43: graphics-r3 panic. Ghi lại build-10 lên MACEFI (/dev/sde3) để lấy .panic.

## Kết luận tạm Giai đoạn B (2026-11-02 16:47)
- 3 lần thử (graphics-v1 JN NootedGreen; graphics-v2 + class-code; graphics-r3 NootedGreen R3 khucx) đều hỏng tại `IGAccelTask::withOptions` khi `IntelAccelerator::start` (panic CR2 0xc78 / treo cứng), uptime ~54 s.
- NootedGreen khác nhau không đổi kết quả → nguyên nhân nằm trong khởi tạo memory manager của driver TGL trên nền tảng này; trùng JN #24 (không có bản sửa). Đề xuất dừng Giai đoạn B hoặc thu log sâu / liên hệ khucxtriendev.
- An ninh: video verbose có in khoá phiên WPA của AirportItlwm — không chia sẻ công khai.
- 2026-11-02T16:58:23 plist_edit bootarg-remove ngreenSched=4 (config.plist)
- 2026-11-02T16:58:23 plist_edit bootarg-add ngreenSched=5 (config.plist)

## Build 16 — `graphics-v3` (2026-11-02): = build-12 graphics-v1 (NootedGreen JN d805e6a6) + `ngreenSched=4` → **`ngreenSched=5`** (MỘT thay đổi)
- Lý do: JN #13 nghi đường scheduler; CATALOG.md L711/933: 3=GuC (tắt vì -disablegfxfirmware), 4=IGScheduler4 (config JN), 5=host-preemptive = mặc định code cho GPU spoof.
- Người dùng: không gửi issue/bình luận upstream.
- 2026-11-02T16:58:40 Created build-16-20261102-165840-graphics-v3-sched5-b16 (tree a61c761357c4, ocvalidate: 0 errors, 0 warnings)
- 2026-11-02T17:01:07 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 9a5eaaf386eb, verified)
- 2026-11-02 17:00: build-16 graphics-v3 ghi lên MACEFI (/dev/sdb3).
- 2026-11-03T00:58:04 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 1acd4c7be7ec, verified)
- 2026-11-03 00:57: build-16 graphics-v3 (ngreenSched=5) PANIC (người dùng; chưa có .panic). Ghi build-10 (snapshot, validate 0/0) lên MACEFI /dev/sdb3, tree 1acd4c7be7ec, kiểm hash OK; USB cũ trùng snapshot build-16. Ghi chú: MANIFEST build-10 có knownGood=true nhưng log không có dòng đánh dấu.
- 2026-11-03 01:20: người dùng thay CLAUDE.md bằng Plan v3 (IntelIGPU-Tahoe, 25G83). Phase 0 viết docs/feasibility.md: binary Apple TGL không khớp hash (chặn), GFX0/46A3 rev0c OK, 25G83 có trên catalog Apple (140-93587). Không đổi EFI/USB.
- 2026-11-03 01:36: người dùng khôi phục CLAUDE.md (hướng JN) và thêm Plan v4 `docs/PLAN-cheseecake-46A3.md` (thay Plan v3).

## Phân tích panic graphics-v3 + boot-args bị cắt (2026-11-03, Plan v4 Phase 0)
- `logs/Kernel-2026-11-02-200211.panic`: cùng chữ ký v1 (CR2 0xc78, `IGAccelTask::withOptions` ← `IntelAccelerator::start`), uptime 51,88 s, NootedGreen UUID 822E1982 (JN d805e6a6).
- **Boot-args config 291 ký tự, kernel thấy 255** (cả 3 .panic). `ngreen-eu=64 ngreen-l3=6` bị mất ở MỌI build đồ họa (12, 14, 15, 16); `ngreenSched=5` bị mất ở build-16; `ngreenV142=3` mất `=3` ở 12/14/15.
  ⇒ Các build trước đều chạy topology mặc định 96 EU / L3 8. Giới hạn Lilu ~228 ký tự (JN KERNEL-PATCHES L19, cheseecake PORT L102; người dùng xác nhận).
- Lỗi kế hoạch (Claude): GRAPHICS-PLAN không kiểm độ dài boot-args; `plist_edit bootarg-add` nối vào cuối chuỗi nên tham số mới luôn rơi vào vùng bị cắt.
- Đề xuất boot-args 224 ký tự + `force-polling` DeviceProperty (VoodooI2C 3.0.0 L236–237): `docs/CHESEECAKE-ANALYSIS.md` §A.4. Người dùng duyệt 2026-11-03 01:54 ("dựng đi").
- 2026-11-03T01:54:36 plist_edit set DeviceProperties/Add/{PciRoot(0x0)/Pci(0x15,0x0)}/force-polling = <data 01000000> (config.plist)
- 2026-11-03T01:54:36 plist_edit set NVRAM/Add/7C436110-AB2A-4BBB-A880-FE41995C9F82/boot-args = 'ngreen-eu=64 ngreen-l3=6 -ngreentglwithgfx -allow3d -disablegfxfirmware ngreen-dmc=adlp ngreenV142=3 -ngreenv189 -ngreenkeepefi -ngreenxefix -ngreenfixbootmode amfi_get_out_of_my_way=1 -amfipassbeta -v keepsyms=1 debug=0x100' (config.plist)
- 2026-11-03T01:54:55 Created build-17-20261103-015455-jn-topo-b17 (tree 21662eaeaea7, ocvalidate: docs/validation/latest.json)

## Build 17 — `jn-topo` (2026-11-03, Plan v4 sau H1): = build-16 + boot-args 224 ký tự + `force-polling`
- NootedGreen JN d805e6a6 (khớp user-space JN 6f03560 đang cài trên MÁY B), spoof 9A49, SIP 0x0A13, AMFIPass, dGPU `disable-gpu` + SSDT-DGPU-OFF — giữ nguyên.
- boot-args (224 ≤ 228): `ngreen-eu=64 ngreen-l3=6 -ngreentglwithgfx -allow3d -disablegfxfirmware ngreen-dmc=adlp ngreenV142=3 -ngreenv189 -ngreenkeepefi -ngreenxefix -ngreenfixbootmode amfi_get_out_of_my_way=1 -amfipassbeta -v keepsyms=1 debug=0x100`.
- Bỏ: `ngreenSched` (bị `-disablegfxfirmware` ghi đè), `IGLogLevel=3`, `gfxrst=1`, `-wegnoegpu` (trùng `disable-gpu`), `-vi2c-force-polling` → DeviceProperty `PciRoot(0x0)/Pci(0x15,0x0)` `force-polling = 01000000` (VoodooI2C 3.0.0 `VoodooI2CDeviceNub.cpp` L236–237; tạo bằng `--create`: DeviceProperties/Add nhận đường dẫn thiết bị tuỳ ý).
- Biến chủ đích: topology 64 EU / L3 6 lần đầu tới kernel. `config-install.plist` = build-10 (plist_diff 0). efi-validate 0/0 (validate-20261103T015443.md).
- Chưa ghi USB.
- 2026-11-03T01:57:05 Created build-18-20261103-015705-usb-before-deploy (tree c11c827fc985, ocvalidate: n/a (existing USB content))
- 2026-11-03T01:57:10 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 694ef920f83a, verified)
- 2026-11-03 01:57: build-17 jn-topo ghi lên MACEFI (/dev/sdc3, tree 694ef920f83a, kiểm hash OK; USB boot-args 224 ký tự, force-polling 01000000, NootedGreen md5 d805e6a6). Nội dung USB cũ (build-10) được usb-deploy-guard tự sao lưu thành snapshot build-18 usb-before-deploy.
- 2026-11-03T02:18:42 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 1acd4c7be7ec, verified)
- 2026-11-03 02:17: **build-17 jn-topo PANIC** (người dùng; chờ .panic). Ghi build-10 (snapshot, validate 0/0 validate-20261103T021734.md) lên MACEFI /dev/sdc3 bằng `--source`, tree 1acd4c7be7ec, kiểm hash OK; USB cũ trùng snapshot build-17 (không tạo snapshot mới). Còn sót thư mục `Kexts/NootedGreen.kext` chỉ chứa 6 file AppleDouble `._*` (macOS tạo khi mount USB) — không có trong config, vô hại.

## Kết quả build-17 jn-topo (2026-11-03 02:20): PANIC, cùng chữ ký v1
- `logs/Kernel-2026-11-03-022026.panic`: boot-args kernel thấy = 224 ký tự, đủ toàn bộ (H1 đã sửa xong). CR2 0xc78 `IGAccelTask::withOptions` ← `IntelAccelerator::start`, uptime 52,77 s.
- Kết luận: topology sai (96 EU mặc định) **không** phải nguyên nhân panic. 5 lần thử hướng JN (v1, v2, r3, v3, jn-topo) cùng một lỗi.
- HookCase UUID mới D2496A3A (người dùng chạy lại install.sh cùng commit 6f03560); driver TGL UUID BA3AA1C0 không đổi.

## F1 — patch GMSFIX cho NootedGreen (2026-11-03, người dùng duyệt)
- Gốc panic (H3): `docs/GRAPHICS-PANIC-ANALYSIS.md`. Patch `patches/nootedgreen-gmsfix-jn6f03560.patch` (3 file, 53 dòng +): lưu kích thước stolen thật (trước sàn 128 MB) + mã GMS; LookupPatch thay `movzwl/and 0xff00/shl 0x11` (duy nhất, file offset 0xec02 của TGL le) bằng `movl $real,%r14d`; log `XeNG GMSFIX` + diag trước `IGAccelTask::withOptions`. Tắt: `-ngreennogmsfix`.
- Kiểm trên MÁY A: `git apply --check` sạch trên JN 6f03560; `clang++ -fsyntax-only` (MacKernelSDK @3f75008 + Lilu 1.7.2 DEBUG headers) 0 lỗi, số cảnh báo bằng bản gốc. Chưa link/chạy.
- Runbook build trên MÁY B: `docs/GMSFIX-RUNBOOK.md`. EFI/USB chưa đổi (USB = build-10).
- 2026-11-03T03:10:27 plist_edit set Kernel/Add[BundlePath=NootedGreen.kext]/Comment = 'NootedGreen JN 6f03560 + GMSFIX patch (md5 ec1ea837)' (config.plist)
- 2026-11-03T03:10:39 Created build-19-20261103-031039-gmsfix-b19 (tree c77eb1bd6405, ocvalidate: docs/validation/latest.json)

## Build 19 — `gmsfix` (2026-11-03): = build-17 + NootedGreen có patch GMSFIX (MỘT thay đổi: binary kext)
- Kext build trên MÁY B (`build-nootedgreen.sh`, JN 6f03560 + `patches/nootedgreen-gmsfix-jn6f03560.patch`): md5 `ec1ea837b66462419f28e51b687584dc`, sha256 `40059b2d4d15f81a06000f871888b4f1b6974d85bfbac88efe567f3dea8922dc`; 4 chuỗi `XeNG GMSFIX`; Info.plist/CodeResources giống bản d805e6a6. Lưu `_cache/user-inputs/NootedGreen-gmsfix-ec1ea837.kext` (bỏ file `._*`).
- Config: chỉ đổi Comment của NootedGreen. Boot-args giữ 224 ký tự. `config-install.plist` = build-10 (plist_diff 0). efi-validate 0/0 (validate-20261103T031033.md).
- Chưa ghi USB.
- 2026-11-03T03:12:34 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree dc173a4bb907, verified)
- 2026-11-03 03:12: build-19 gmsfix ghi lên MACEFI (/dev/sdc3, tree dc173a4bb907, kiểm hash OK; USB boot-args 224, NootedGreen md5 ec1ea837). USB cũ trùng snapshot build-10 → không tạo snapshot mới.
- 2026-11-03T03:41:45 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 1acd4c7be7ec, verified)
- 2026-11-03 03:41: ghi lại build-10 lên MACEFI (tree 1acd4c7be7ec) để lấy log lần boot treo của build-19.
- 2026-11-03T04:03:25 plist_edit set Kernel/Add[BundlePath=NootedGreen.kext]/Comment = 'NootedGreen JN 6f03560 + GMSFIX v2 (accel+FB, md5 ffd0dc36)' (config.plist)
- 2026-11-03T04:03:34 Created build-20-20261103-040334-gmsfix2-b20 (tree f1b57ae16085, ocvalidate: docs/validation/latest.json)

## Build 20 — `gmsfix2` (2026-11-03): = build-19 + NootedGreen GMSFIX v2 (MỘT thay đổi: binary kext)
- Kext build trên MÁY B (v1 + `patches/nootedgreen-gmsfix-v1-to-v2.patch`): md5 `ffd0dc3617d3d351b5a69ca3b35ff193`, sha256 `de8b558c5dd8bf8cb96aa5d15660879dc49d2eddf096469069b76aeb8ff3888b`, 7 chuỗi GMSFIX; khớp gốc USB. Lưu `_cache/user-inputs/NootedGreen-gmsfix2-ffd0dc36.kext`.
- Config chỉ đổi Comment; boot-args 224; efi-validate 0/0 (validate-20261103T040325.md). Chưa ghi USB.
- 2026-11-03T04:04:08 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 160e61bac2f4, verified)
- 2026-11-03 04:04: build-20 gmsfix2 ghi lên MACEFI (/dev/sdc3, kiểm hash OK; NootedGreen md5 ffd0dc36, boot-args 224).
- 2026-11-04T21:25:07 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 1acd4c7be7ec, verified)
- 2026-11-04 21:24: **build-20 gmsfix2 PANIC** (người dùng; chờ .panic/video). Ghi lại build-10 lên MACEFI (/dev/sdb3, tree 1acd4c7be7ec, kiểm hash OK).
- 2026-11-04T21:30:25 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 160e61bac2f4, verified)
- 2026-11-04 21:31: ghi lại build-20 gmsfix2 lên MACEFI (/dev/sdb3, kiểm hash OK) để người dùng boot lại và thu .panic/video (lần panic trước chưa lấy được log).
- 2026-11-04T21:41:05 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 1acd4c7be7ec, verified)
- 2026-11-04 21:39: build-20 boot lần 2 (người dùng) → ghi lại build-10 lên MACEFI (/dev/sdb3, tree 1acd4c7be7ec, kiểm hash OK) để lấy .panic/video.
- 2026-11-04T22:06:35 plist_edit set Kernel/Add[BundlePath=NootedGreen.kext]/Comment = 'NootedGreen JN 6f03560 + GMSFIX v3 (accel+FB+PAVP, md5 f7e42c77)' (config.plist)
- 2026-11-04T22:06:48 Created build-21-20261104-220648-gmsfix3-b21 (tree 4abc53ab2c4b, ocvalidate: docs/validation/latest.json)

## Build 21 — `gmsfix3` (2026-11-04): = build-20 + NootedGreen GMSFIX v3 (MỘT thay đổi: binary kext)
- Kext build trên MÁY B (v2 + `patches/nootedgreen-gmsfix-v2-to-v3.patch`): md5 `f7e42c7733a638f8c36c61788f957f7b`, sha256 `1dd6b1c0ea8f2e361f8cf4ad66cd7535bc1428622dee6dc4f6b5c3b635fec5e5`, 9 chuỗi GMSFIX|PAVPFIX; khớp gốc USB. Lưu `_cache/user-inputs/NootedGreen-gmsfix3-f7e42c77.kext`.
- Config chỉ đổi Comment; boot-args 224; efi-validate 0/0 (validate-20261104T220635.md). Chưa ghi USB.
- 2026-11-05T01:52:46 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree d7995d0b2d69, verified)
- 2026-11-05 01:53: build-21 gmsfix3 ghi lên MACEFI (/dev/sdb3, kiểm hash OK; NootedGreen md5 f7e42c77, boot-args 224).
- 2026-11-05 02:06: **build-21 gmsfix3 BOOT VÀO DESKTOP, Metal 2** (người dùng: kmutil, system_profiler, xe-topo=16390). Lỗi: con trỏ chuột render sai.
- 2026-11-05T02:19:27 Marked build-21-20261104-220648-gmsfix3-b21 as known-good (user request)
- 2026-11-05T02:19:34 plist_edit set NVRAM/Add/7C436110-AB2A-4BBB-A880-FE41995C9F82/boot-args = 'ngreen-eu=96 ngreen-l3=6 -ngreentglwithgfx -allow3d -disablegfxfirmware ngreen-dmc=adlp ngreenV142=3 -ngreenv189 -ngreenkeepefi -ngreenxefix -ngreenfixbootmode amfi_get_out_of_my_way=1 -amfipassbeta -v keepsyms=1 debug=0x100' (config.plist)
- 2026-11-05T02:19:50 Xoá thủ công snapshot build-12-20261102-154737-graphics-v1-b12 (người dùng chọn khi duyệt build-22; snapshot.py không xoay vòng qua known-good build-10)
- 2026-11-05T02:19:50 Created build-22-20261105-021950-eu96-b22 (tree cf86bdc2e91e, ocvalidate: docs/validation/latest.json)

## Build 22 — `eu96` (2026-11-05): = build-21 + `ngreen-eu=64` → `ngreen-eu=96` (MỘT thay đổi, người dùng duyệt)
- Mục đích: thử H5 — lỗi vẽ con trỏ (blit 3D) do DSS không liên tục (mask 0x33); 96 EU = 12 SS = 6 DSS phủ chỉ số DSS 4,5. Kỳ vọng `xe-topo` = 24582.
- Boot-args vẫn 224 ký tự; plist_diff 1 khác biệt; efi-validate 0/0 (validate-20261105T021934.md). Chưa ghi USB.
- Người dùng đánh dấu **build-21 known-good** (02:19). Snapshot build-12 xoá thủ công (người dùng chọn).
- 2026-11-05T02:23:55 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 1f817846ec5e, verified)
- 2026-11-05 02:23: build-22 eu96 ghi lên MACEFI (/dev/sdc3, tree 1f817846ec5e, kiểm hash OK; boot-args 224 bắt đầu ngreen-eu=96; NootedGreen md5 f7e42c77). USB cũ trùng snapshot build-21 → không tạo snapshot.
- 2026-11-05T02:52:08 Xoá thủ công snapshot build-14-20261102-160038-graphics-v2-b14 (người dùng yêu cầu, để có chỗ cho build-23)
- 2026-11-05T02:52:15 plist_edit set Kernel/Add[BundlePath=NootedGreen.kext]/Comment = 'NootedGreen JN 6f03560 + GMSFIX v4 (accel+FB+PAVP+CURDIAG, md5 a88784e7)' (config.plist)
- 2026-11-05T02:52:29 Created build-23-20261105-025229-curdiag-b23 (tree b6062a4ae3d3, ocvalidate: docs/validation/latest.json)

## Build 23 — `curdiag` (2026-11-05): = build-21 + NootedGreen GMSFIX v4 (MỘT thay đổi so với build-21: binary kext)
- Kext build trên MÁY B (v3 + `patches/nootedgreen-gmsfix-v3-to-v4.patch`): md5 `a88784e768fda98afcf9ecc5a6748749`, sha256 `42748e715146faa7c644ab9b7a0194f9fb2d9209a34d1de15dc9137af8ded2d8`, 10 chuỗi GMSFIX|PAVPFIX|CURDIAG. Lưu `_cache/user-inputs/NootedGreen-gmsfix4-a88784e7.kext`.
- Dựng từ snapshot build-21 (bỏ `ngreen-eu=96` của build-22). Config chỉ đổi Comment; boot-args 224 (`ngreen-eu=64`); efi-validate 0/0 (validate-20261105T025215.md). Chưa ghi USB.
- 2026-11-05T02:53:06 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 3d568db93f0e, verified)
- 2026-11-05 02:53: build-23 curdiag ghi lên MACEFI (/dev/sdc3, kiểm hash OK; NootedGreen md5 a88784e7, boot-args 224 ngreen-eu=64).
- 2026-11-05T03:11:59 Xoá thủ công snapshot build-15-20261102-162313-graphics-r3-b15 (người dùng yêu cầu, để có chỗ cho build-24)
- 2026-11-05T03:12:00 plist_edit set Kernel/Add[BundlePath=NootedGreen.kext]/Comment = 'NootedGreen JN 6f03560 + GMSFIX v5 (accel+FB+PAVP+CURDIAG2, md5 ff5f164d)' (config.plist)
- 2026-11-05T03:12:11 Created build-24-20261105-031211-curdiag2-b24 (tree 4c6ebfc8e689, ocvalidate: docs/validation/latest.json)

## Build 24 — `curdiag2` (2026-11-05): = build-21 + NootedGreen GMSFIX v5 (MỘT thay đổi so với build-21: binary kext)
- Kext build trên MÁY B (v4 + `patches/nootedgreen-gmsfix-v4-to-v5.patch`): md5 `ff5f164d222f7b05e6776e1d6ebda745`, sha256 `969cb735d086bee55668a005146763b7aa1bd82d297919a564abf0d8de0ccd89`; 3 chuỗi xe-cur-rows/pte, 10 marker. Lưu `_cache/user-inputs/NootedGreen-gmsfix5-ff5f164d.kext`.
- Config chỉ đổi Comment; boot-args 224 (`ngreen-eu=64`); efi-validate 0/0 (validate-20261105T031200.md). Chưa ghi USB.
- 2026-11-05T03:13:25 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 10df3020393e, verified)
- 2026-11-05 03:13: build-24 curdiag2 ghi lên MACEFI (/dev/sdb3, kiểm hash OK; NootedGreen md5 ff5f164d, boot-args 224).
- 2026-11-05T03:25:08 Xoá thủ công snapshot build-16-20261102-165840-graphics-v3-sched5-b16 (cũ nhất không phải known-good; đã đề xuất cho build-25)
- 2026-11-05T03:25:08 plist_edit set Kernel/Add[BundlePath=NootedGreen.kext]/Comment = 'NootedGreen JN 6f03560 + GMSFIX v6 (accel+FB+PAVP+CURDIAG3, md5 23c15958)' (config.plist)
- 2026-11-05T03:25:26 Created build-25-20261105-032526-curdiag3-b25 (tree 2d96b070d6a8, ocvalidate: docs/validation/latest.json)

## Build 25 — `curdiag3` (2026-11-05): = build-21 + NootedGreen GMSFIX v6 (MỘT thay đổi so với build-21: binary kext)
- Kext build trên MÁY B (v5 + `patches/nootedgreen-gmsfix-v5-to-v6.patch`): md5 `23c15958f79cd9662bf6e4c091c37b0d`, sha256 `f7c3c2fb1e42b9338ca3699f11a8b4ac0b0d5f23ce06e7024b676fffea2aaaee`; 8 chuỗi xe-fence/xe-mm. Lưu `_cache/user-inputs/NootedGreen-gmsfix6-23c15958.kext`.
- Config chỉ đổi Comment; boot-args 224 (`ngreen-eu=64`); efi-validate 0/0 (validate-20261105T032508.md). Chưa ghi USB.
- 2026-11-05T03:25:58 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree f26b4de8c3e1, verified)
- 2026-11-05 03:26: build-25 curdiag3 ghi lên MACEFI (/dev/sdc3, kiểm hash OK; NootedGreen md5 23c15958, boot-args 224).
- 2026-11-05T03:38:58 Xoá thủ công snapshot build-17-20261103-015455-jn-topo-b17 (cũ nhất không phải known-good; đã báo trước khi dựng build-26)
- 2026-11-05T03:38:58 plist_edit set Kernel/Add[BundlePath=NootedGreen.kext]/Comment = 'NootedGreen JN 6f03560 + GMSFIX v7 (accel+FB+PAVP+FENCEFIX+diag, md5 3a823f7c)' (config.plist)
- 2026-11-05T03:38:58 Created build-26-20261105-033858-fencefix-b26 (tree c69972f2ffb4, ocvalidate: docs/validation/latest.json)

## Build 26 — `fencefix` (2026-11-05): = build-21 + NootedGreen GMSFIX v7 (MỘT thay đổi so với build-21: binary kext)
- Kext build trên MÁY B (v6 + `patches/nootedgreen-gmsfix-v6-to-v7.patch`): md5 `3a823f7c48d61dc8a237e1753fa84939`, sha256 `fb48e1fcb57e0d643fbc3bbf4781ed775022401fa54fa4d8d3cf2181ecd3e844`; 3 chuỗi FENCEFIX. Lưu `_cache/user-inputs/NootedGreen-gmsfix7-3a823f7c.kext`.
- Sửa con trỏ: cắt fence X-tile của framebuffer về cuối stolen (60 MB). Config chỉ đổi Comment; boot-args 224; efi-validate 0/0 (validate-20261105T033858.md). Chưa ghi USB.
- 2026-11-05T03:40:11 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree ec52c24ce4df, verified)
- 2026-11-05 03:40: build-26 fencefix ghi lên MACEFI (/dev/sdb3, kiểm hash OK; NootedGreen md5 3a823f7c, boot-args 224).
- 2026-11-05 03:42: **build-26 fencefix: con trỏ chuột hiển thị đúng** (người dùng).

## Dọn repo + README (2026-11-05, người dùng duyệt)
- Thêm `README.md` (trạng thái, cấu hình, 5 lỗi đã sửa + nguyên nhân, cài đặt, ghi công/giấy phép).
- Xoá: thư mục rác `{tools,docs,.agents` (rỗng, do lỗi brace expansion), `logs/Retired` (rỗng), file tạm phân tích của Claude trong `_cache/` (khung video, ảnh crop, bản nháp patch).
- Xoá (người dùng chọn): 4 video `logs/*.mp4` (chứa khoá WPA), `logs/b19-log.txt`, `logs/gv2-log.txt`, 9 `shutdown_stall_*`, 2 `WindowServer_*.diag`; patch gộp v1–v6 (giữ gộp v7 + chuỗi tăng thêm); 39 báo cáo validate cũ (giữ 3 mới nhất + latest.json).
- `.gitignore`: thêm `logs/*.mp4` và kext Apple `IOSkywalkFamily.kext`, `IO80211FamilyLegacy.kext` trong EFI.
- Không đụng: `.claude/worktrees/` (có nhánh `claude/do-not-touch-this`), `_cache/refs`, `_cache/downloads`, `snapshots/`, các docs cũ, file `.panic`, ảnh.
- 2026-11-05T03:47:56 .gitignore: thêm .claude/worktrees/ (người dùng yêu cầu).
- 2026-11-05T19:34:40 Created build-26-20261105-193440-fencefix-restored (tree c69972f2ffb4, ocvalidate: 0 errors, 0 warnings (validate-20261105T193419.md))

## Dựng lại dự án từ USB (2026-11-05 19:30, người dùng: "mất hết thư mục dự án cũ")
- Thư mục dự án là bản clone mới từ git: mất mọi file trong `.gitignore` — `_cache/` (refs, downloads, acpi, user-inputs với các bản NootedGreen cũ), `snapshots/` (gồm known-good build-10, build-21), `docs/hw-dump/`, `docs/MACHINE-ANALYSIS.md`, `docs/GRAPHICS-PANIC-ANALYSIS.md`, `docs/validation/`, `config/usb-mount.txt`, 2 kext Apple trong EFI.
- So với USB MACEFI (build-26): `config.plist` chỉ khác 4 trường SMBIOS (đúng — serial chỉ tiêm lúc ghi USB); `config-install.plist` 0 khác biệt; NootedGreen md5 `3a823f7c` khớp; thiếu `IOSkywalkFamily.kext`, `IO80211FamilyLegacy.kext`.
- Tải lại 2 zip từ OCLP-CustoMac @ f2bbcef (`_cache/downloads/oclp-customac-f2bbcef/`): SHA-256 khớp SOURCES.md; giải nén giống hệt bản trên USB → chép vào `EFI/OC/Kexts/`. `diff -rq` EFI dự án ↔ USB: chỉ còn `config.plist` (SMBIOS) và file `._*` của macOS.
- efi-validate 0/0 (validate-20261105T193419.md). `snapshots/_counter.txt` đặt tay = 25 (bộ đếm cũ đã mất) để snapshot mang số 26. Snapshot `build-26-…-fencefix-restored`: tree **c69972f2ffb4 = đúng tree build-26 gốc** → giống từng byte.
- Không khôi phục được: snapshot build-10/21 (known-good), binary NootedGreen cũ (build-21 có thể build lại trên MÁY B từ `patches/` v3), hw-dump, DSDT giải mã, repo tham chiếu (clone lại bằng `tools/clone_ref.py` khi cần). Đường lui hiện có: `EFI/OC/config-install.plist` (= cấu hình build-10).
- `config/usb-mount.txt` = `/run/media/cyra/MACEFI`.
- 2026-11-05T19:37:49 Marked build-26-20261105-193440-fencefix-restored as known-good (user request)
- 2026-11-05T19:39:15 plist_edit append to Kernel/Add: BundlePath=IntelBluetoothFirmware.kext (config.plist)
- 2026-11-05T19:39:15 plist_edit append to Kernel/Add: BundlePath=IntelBTPatcher.kext (config.plist)
- 2026-11-05T19:39:15 plist_edit append to Kernel/Add: BundlePath=BlueToolFixup.kext (config.plist)
- 2026-11-05T19:39:15 plist_edit move Kernel/Add[BundlePath=IntelBluetoothFirmware.kext] to position 17 (config.plist)
- 2026-11-05T19:39:15 plist_edit move Kernel/Add[BundlePath=IntelBTPatcher.kext] to position 18 (config.plist)
- 2026-11-05T19:39:15 plist_edit move Kernel/Add[BundlePath=BlueToolFixup.kext] to position 19 (config.plist)
- 2026-11-05T19:39:15 plist_edit set NVRAM/Add/7C436110-AB2A-4BBB-A880-FE41995C9F82/bluetoothExternalDongleFailed = <data 00> (config.plist)
- 2026-11-05T19:39:15 plist_edit set NVRAM/Add/7C436110-AB2A-4BBB-A880-FE41995C9F82/bluetoothInternalControllerInfo = <data 0000000000000000000000000000> (config.plist)
- 2026-11-05T19:39:16 plist_edit append to NVRAM/Delete/7C436110-AB2A-4BBB-A880-FE41995C9F82: item (config.plist)
- 2026-11-05T19:39:16 plist_edit append to NVRAM/Delete/7C436110-AB2A-4BBB-A880-FE41995C9F82: item (config.plist)

## Build 27 — `bluetooth` (2026-11-05): = build-26 + Bluetooth AX210 (DRIVER-MATRIX #8, người dùng duyệt 2026-11-05)
- Người dùng đánh dấu build-26 (bản dựng lại) **known-good** trước khi dựng build-27.
- Kext (release-fetch, SOURCES.md): IntelBluetoothFirmware + IntelBTPatcher **2.5.3** (fork lshbluesky; Info.plist có personality `IntelBluetoothFirmware_0032` = AX210 `8087:0032`) và BlueToolFixup **2.7.2** (acidanthera/BrcmPatchRAM; chỉ chép BlueToolFixup). IntelBluetoothInjector KHÔNG dùng (không dùng cho Monterey+).
- Kernel/Add vị trí 17–19, ngay sau AirportItlwm: IntelBluetoothFirmware → IntelBTPatcher → BlueToolFixup (IntelBTPatcher và BlueToolFixup cần Lilu, Lilu ở vị trí 0).
- NVRAM/Add `7C436110-…`: `bluetoothExternalDongleFailed` = `00`, `bluetoothInternalControllerInfo` = 14 byte `00`; thêm cả hai vào NVRAM/Delete.
- **Không** thêm `-btlfxallowanyaddr`: boot-args đang 224 ký tự, thêm thì thành 243 > 228 (giới hạn Lilu) → cờ bị cắt. Chỉ xét nếu Bluetooth không bật được, khi đó bỏ `debug=0x100` để có chỗ.
- `config-install.plist` giữ nguyên (đường lui không tăng tốc, không Bluetooth). Cổng BT HS05 (port 7, Internal 255) đã có trong UTBMap từ build-10.
- plist_diff với build-26: 3 kext + 2 NVRAM Add + 2 NVRAM Delete (+ dịch thứ tự các kext sau). efi-validate 0/0 (validate-20261105T193921.md). Chưa ghi USB.
- 2026-11-05T19:39:37 Created build-27-20261105-193937-bluetooth (tree dd2423579245, ocvalidate: 0 errors, 0 warnings (validate-20261105T193921.md))
- 2026-11-05T19:44:38 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 6efedd66b725, verified)
- 2026-11-05 19:44: build-27 bluetooth ghi lên MACEFI (/dev/sdb3, kiểm hash OK). SMBIOS thật được tiêm: người dùng tự tạo lại file secrets từ config trên USB (Claude không đọc giá trị). Nội dung USB cũ trùng snapshot build-26 → không tạo snapshot mới.

## Kết quả build-27 bluetooth (người dùng, 2026-11-05 19:55)
- `kmutil showloaded`: IntelBTPatcher 2.5.3, BlueToolFixup 2.7.2, IntelBluetoothFirmware 2.5.3 đều nạp.
- `system_profiler SPBluetoothDataType`: controller **State: On**, Transport USB, Chipset THIRD_PARTY_DONGLE, Firmware v12490 (firmware đã tải), dịch vụ HFP/AVRCP/A2DP/HID/LEA/GATT. Địa chỉ MAC không ghi lại.
- Chưa kiểm: ghép thiết bị (BLE, issue #514), ổn định sau nhiều lần khởi động.
- 19:58 người dùng: "không tìm được device nào". `nvram`: `bluetoothExternalDongleFailed`=%00, `bluetoothInternalControllerInfo`=14×%00 (có hiệu lực); boot-args 224 đủ. Log bluetoothd 5 phút: không có lỗi; nhiều dòng `Server.LE.Scan decryptProximityPairingPayload` (nhận gói quảng bá BLE của thiết bị Apple xung quanh) và advertise "with error (null)" → **radio và quét BLE hoạt động**. Nghi vấn: thiết bị thử không ở chế độ ghép đôi, hoặc quét Classic (inquiry) lỗi. Chưa đổi boot-args (A/B chờ kết quả thử lại).
- Log lọc inquiry/discover (cửa sổ 3 phút): lần quét cuối dừng lúc 19:57:32 (`CBStackClassicScanner Scan stopped`, `Bluetooth scan completed`, `Inquiry state changed: Off`) — quét Classic chạy và kết thúc **không có lỗi HCI**; dòng mức Error `notifyDiscoverabiltyChanged: 0` chỉ là thông báo trạng thái. Log không cho biết số thiết bị tìm thấy; sau 19:57:32 không có lần quét nào → chưa có lần thử với thiết bị ở chế độ ghép đôi trong log.
- 20:00 `log stream` lúc mở Bluetooth Settings: quét Classic `ScanStarted … BT_SUCCESS`, chạy 20:00:12→24 (12 s) và 20:00:54→56 (2 s); **không có kết quả inquiry Classic nào**. Thiết bị duy nhất "found" = iPhone13,2 cùng tài khoản iCloud (`Hidden BLEPaired CloudPaired`, RSSI −56, nhận qua quảng bá BLE) — macOS ẩn thiết bị này khỏi danh sách. Lỗi lặp lại: `Server.LE.Scan addScanFilterByUUID failed 0x1812` (0x1812 = dịch vụ HID-over-GATT) kèm `supportedADVBuffers:0` → bộ lọc quét phần cứng cho chuột/bàn phím BLE không cài được; ảnh hưởng tới việc phát hiện BLE HID CHƯA XÁC MINH.
- 20:08 người dùng: **"bluetooth hoạt động rồi"** (ghép được thiết bị). Không cần `-btlfxallowanyaddr`, không dựng build-28 cho Bluetooth.

## Độ sáng (D11) — chẩn đoán 2026-11-05 20:11 (build-27)
- `ioreg -p IODeviceTree | grep PNLF|APP0002`: **rỗng** → firmware F.34 không có PNLF. Class count `AppleBacklightDisplay=0`, `IOBacklightDisplay=0`, `AppleDisplay=1` → macOS coi panel là màn hình không có đèn nền điều chỉnh → không có thanh độ sáng. `IODisplayParameters` có `bklt` 0..65535 (framebuffer). Log kernel: `[IGFB][ERROR] hwGetCRTC: EFI using a different backlight frequency`; không có dòng `bl hw=` của XE-BLR.
- Kế hoạch build-28: thêm `SSDT-PNLF` tối giản (`docs/acpi-src/SSDT-PNLF.dsl`): `\_SB.PC00.GFX0.PNLF`, `_HID APP0002`, `_CID "backlight"`, `_UID 0x13`, `_STA` 0x0B chỉ Darwin; không `_INI`, không ghi thanh ghi PWM (cấu trúc giống SSDT-PNLF của JN — đã xem bằng hexdump; mẫu OpenCore 1.0.8 bị loại vì `_INI` ghi LEVW/LEVX và với ID 9A49 rơi vào nhánh Skylake PWMMAX 0x56c). Không thêm patch PNLF→XNLF (không có gì để đổi tên). Chưa thêm `ngreenblmax` (một thay đổi mỗi build; boot-args 224).
- Chờ: (1) xác nhận đường dẫn `\_SB.PC00.GFX0` trên MÁY B (dump DSDT cũ đã mất); (2) `iasl` trên MÁY A (không còn sau khi mất thư mục/hệ thống) — người dùng cài.
- 2026-11-05T20:14:09 plist_edit append to ACPI/Add: Path=SSDT-PNLF.aml (config.plist)

## Build 28 — `pnlf` (2026-11-05): = build-27 + SSDT-PNLF (MỘT thay đổi)
- Người dùng xác nhận đường dẫn iGPU trên MÁY B: `IOACPIPlane:/_SB/PC00@0/GFX0@20000` → `\_SB.PC00.GFX0` đúng. `iasl` 20251212 (người dùng cài lại trên MÁY A).
- `docs/acpi-src/SSDT-PNLF.dsl` → `EFI/OC/ACPI/SSDT-PNLF.aml` (139 byte; `iasl -ve` 0 lỗi/0 cảnh báo; dịch ngược khớp nguồn). ACPI/Add thêm cuối danh sách (không phụ thuộc SSDT khác). `_OSI` trong SSDT không bị patch XOSI (patch chỉ áp DSDT).
- Boot-args giữ 224 (chưa `ngreenblmax`). `config-install.plist` không đổi. efi-validate 0/0 (validate-20261105T201409.md).
- Kiểm trên MÁY B: `ioreg -lw0 -p IODeviceTree | grep -i APP0002`; class `AppleBacklightDisplay` = 1; thanh độ sáng trong Control Center/System Settings; kéo hết dải xem đèn nền có tối→sáng tối đa không (nếu chỉ ~50% → build sau thêm `ngreenblmax`).
- 2026-11-05T20:14:18 Created build-28-20261105-201417-pnlf (tree b1a42bc030ec, ocvalidate: 0 errors, 0 warnings (validate-20261105T201409.md))
- 2026-11-05T20:15:27 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 4ede6cbe9e0d, verified)
- 2026-11-05 20:20 kết quả build-28 (người dùng): `APP0002` có trong IODeviceTree, `AppleBacklightDisplay=1`, **thanh độ sáng hoạt động** nhưng mức tối đa tối hơn bình thường.
- `dmesg` (XeNG CS, slider tối đa): `bl hw=96000 apple=0 fw=0 duty=17741 max=17741 out=17741` → macOS không ghi chu kỳ (apple=0) nên XE-BLR không rescale; đầu ra 17741/96000 ≈ 18,5 % PWM. Trùng số đo của JN (HISTORY.md, XPS). Mã XE-BLR @6f03560 (`kern_gen11.cpp`): `out = duty × hw / ngreenblmax`, kẹp ở hw.
- Đề xuất build-29 (chờ duyệt — boot-args đồ hoạ): thêm `ngreenblmax=17741` (đầu ra tối đa = 96000 = 100 %), bỏ `debug=0x100` và `keepsyms=1` (phương án A); chuỗi mới 219 ký tự.
- 2026-11-05 20:15: build-28 pnlf ghi lên MACEFI (/dev/sdb3, tree 4ede6cbe9e0d, kiểm hash OK, SMBIOS thật). USB cũ trùng snapshot build-27 → không tạo snapshot mới.
- 2026-11-05T20:24:03 plist_edit set NVRAM/Add/7C436110-AB2A-4BBB-A880-FE41995C9F82/boot-args = 'ngreen-eu=64 ngreen-l3=6 ngreenblmax=17741 -ngreentglwithgfx -allow3d -disablegfxfirmware ngreen-dmc=adlp ngreenV142=3 -ngreenv189 -ngreenkeepefi -ngreenxefix -ngreenfixbootmode amfi_get_out_of_my_way=1 -amfipassbeta -v' (config.plist)

## Build 29 — `blmax` (2026-11-05): = build-28 + boot-args độ sáng (người dùng duyệt 20:23)
- boot-args (219 ký tự): `ngreen-eu=64 ngreen-l3=6 ngreenblmax=17741 -ngreentglwithgfx -allow3d -disablegfxfirmware ngreen-dmc=adlp ngreenV142=3 -ngreenv189 -ngreenkeepefi -ngreenxefix -ngreenfixbootmode amfi_get_out_of_my_way=1 -amfipassbeta -v`.
- Thêm `ngreenblmax=17741` (duty tối đa đo được; XE-BLR: đầu ra = duty × 96000 / 17741 → 100 % ở mức tối đa). Bỏ `debug=0x100`, `keepsyms=1` (giới hạn 228): panic sẽ tự khởi động lại, `.panic` không có tên hàm — khi cần gỡ panic, thêm lại tạm thời.
- plist_diff với build-28: 1 khác biệt (boot-args). efi-validate 0/0 (validate-20261105T202403.md).
- Kiểm trên MÁY B: slider tối đa = sáng như bình thường; `sudo dmesg | grep -a 'bl hw' | tail -1` phải có `out=96000` (hoặc gần) khi slider tối đa.
- 2026-11-05T20:24:12 Created build-29-20261105-202412-blmax (tree 42b04e74d767, ocvalidate: 0 errors, 0 warnings (validate-20261105T202403.md))
- 2026-11-05T20:24:20 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree a6513c2bd81b, verified)
- 2026-11-05 20:24: build-29 blmax ghi lên MACEFI (/dev/sdb3, kiểm hash OK, SMBIOS thật).
- 2026-11-05 20:28: **build-29: độ sáng hoạt động** (người dùng: slider đủ dải, sáng tối đa đúng).

## Audio ALC245 (D1, DRIVER-MATRIX #14/#15) — kiểm định lại 2026-11-05 20:30
- AppleALC 1.9.8 (mới nhất) có 3 layout cho codec ALC245: 11 (soto2080, Lenovo), 12 (Lenovo), 13 (lunjielee, HP Omen 2020). Không có layout cho HP 8A4F → thử 13 trước (HP), rồi 11, 12.
- OCLP-CustoMac @ f2bbcef (`_cache/refs/oclp-customac`): `sys_patch/patchsets/hardware/misc/modern_audio.py` — root patch **Modern Audio** chép `AppleHDA.kext` bản "26.0 Beta 1" vào `/System/Library/Extensions` (tải về MÁY B qua OCLP, Claude không phân phối binary Apple); `requires_kernel_debug_kit` = True. `root_selection.py`: Modern Wi-Fi và Modern Audio là hai tuỳ chọn, **mặc định chọn cả hai** → có thể AppleHDA đã được cài cùng lần root patch Wi-Fi (CHƯA XÁC MINH, chờ kiểm trên MÁY B).
- SimpleHDA vẫn loại (không license, chứa binary Apple). Boot-args 219 → `alcid=` sẽ chạm 228 → dùng DeviceProperty `layout-id` (cần đường dẫn PCI của HDA thật).
- 2026-11-05T20:32:32 plist_edit append to Kernel/Add: BundlePath=AppleALC.kext (config.plist)
- 2026-11-05T20:32:32 plist_edit move Kernel/Add[BundlePath=AppleALC.kext] to position 7 (config.plist)
- 2026-11-05 20:31 người dùng duyệt #14 (AppleALC) và #15 (root patch Modern Audio OCLP, KHÔNG SimpleHDA). AppleALC 1.9.8 tải (release-fetch, digest OK), chép `AppleALC.kext` (không AppleALCU) vào EFI, Kernel/Add vị trí 7 (sau WhateverGreen, NootedGreen; cần Lilu). **Build-30 đang dựng dở**: còn thiếu DeviceProperty `layout-id` — chờ đường dẫn PCI của HDA từ MÁY B. Chưa snapshot.
- 2026-11-05T20:33:51 plist_edit set DeviceProperties/Add/{PciRoot(0x0)/Pci(0x1f,0x3)}/layout-id = <data 0D000000> (config.plist)

## Build 30 — `audio` (2026-11-05): = build-29 + AppleALC 1.9.8 + `layout-id` 13 (DRIVER-MATRIX #14/#15 duyệt 20:31)
- MÁY B (20:33): `AppleHDA.kext` **không có**; OCLP plist chỉ có "Modern Wireless"; HDA = `IOACPIPlane:/_SB/PC00@0/HDAS@1f0003` → DeviceProperties `PciRoot(0x0)/Pci(0x1f,0x3)` `layout-id` = `0D000000` (13, HP Omen 2020 — cùng hãng; dự phòng 11, 12).
- AppleALC.kext Kernel/Add vị trí 7 (sau NootedGreen). Boot-args không đổi (219). plist_diff với build-29: +AppleALC, +DeviceProperty HDA (còn lại là dịch thứ tự). efi-validate 0/0 (validate-20261105T203352.md).
- KDK 25G241 có trên dortania/KdkSupportPkg (OCLP-CustoMac `kdk_handler.py` dùng manifest này). Root patch Modern Audio cần Revert + patch lại cả Wi-Fi + Audio: `docs/POSTINSTALL-RUNBOOK.md` §5 (viết lại).
- 2026-11-05T20:34:32 Created build-30-20261105-203431-audio (tree 2b7dda3187b0, ocvalidate: 0 errors, 0 warnings (validate-20261105T203352.md))
- 2026-11-05T20:36:09 Marked build-29-20261105-202412-blmax as known-good (user request)
- 2026-11-05T20:36:14 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree ed52c66ef74a, verified)
- 2026-11-05 20:36: người dùng đánh dấu **build-29 known-good**. build-30 audio ghi lên MACEFI (/dev/sdb3, kiểm hash OK, SMBIOS thật); chờ root patch Modern Audio trên MÁY B (POSTINSTALL-RUNBOOK §5).
- 2026-11-05 20:49 (build-30, sau root patch Modern Wi-Fi + Modern Audio): `AppleHDA.kext` có trong /S/L/E; nạp: AppleALC 1.9.8, AppleHDAController 600.2, AppleHDA 600.2, AppleHDAHardwareConfigDriver 600.2. Chưa có kết quả loa/jack/mic, Wi-Fi, Metal.
- 2026-11-05T20:54:11 plist_edit set DeviceProperties/Add/{PciRoot(0x0)/Pci(0x1f,0x3)}/layout-id = <data 0B000000> (config.plist)
- 2026-11-05 20:53 kết quả layout 13 (người dùng): Output "Internal Speakers" có nhưng **không có tiếng**; jack 3,5 mm nhận tai nghe nhưng **tiếng nhỏ, chỉ kênh trái**; **không có Input device**. Wi-Fi, Metal, độ sáng vẫn bình thường sau Revert + patch lại → root patch không ảnh hưởng stack đồ hoạ.

## Build 31 — `alc11` (2026-11-05): = build-30, `layout-id` 13 → **11** (MỘT thay đổi; theo kế hoạch đã duyệt 13 → 11 → 12)
- 2026-11-05T20:54:12 Created build-31-20261105-205412-alc11 (tree 2c547662d582, ocvalidate: 0 errors, 0 warnings (validate-20261105T205411.md))
- `layout-id` = `0B000000`. efi-validate 0/0 (validate-20261105T205411.md). Snapshot build-31. Chưa ghi USB (USB chưa mount). Root patch không cần làm lại khi đổi layout.
- 2026-11-05T20:55:47 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree a204c4d89952, verified)
- 2026-11-05 20:55: build-31 alc11 ghi lên MACEFI (/dev/sdb3, kiểm hash OK, SMBIOS thật).
- 2026-11-05 21:08 kết quả build-31 layout 11 (người dùng): **loa trong có tiếng, mic trong hoạt động**; tai nghe 3,5 mm vẫn chỉ kênh trái — người dùng nghi tiếp xúc jack/tai nghe, chấp nhận bỏ qua (CHƯA XÁC MINH là phần cứng hay layout). Audio coi là xong với layout 11.
- 2026-11-05T21:09:41 Marked build-31-20261105-205412-alc11 as known-good (user request)
- 2026-11-05 21:09: người dùng đánh dấu **build-31 known-good**.
- 2026-11-05 21:10: commit 17e0396 trên nhánh `bt-backlight-audio` (EFI build-31 + docs; không gồm `.claude/settings.json`, `AGENTS.md`). SMBIOS trong commit là placeholder (đã kiểm).
- 2026-11-05 21:29: người dùng báo **camera HP Wide Vision HD (`30C9:0069`) hoạt động** trên build-31 (driver UVC sẵn có; không thay đổi EFI). DEFERRED D13 đóng. Lý do build-10 không chạy: CHƯA XÁC MINH.
- 2026-11-05T21:36:04 plist_edit delete DeviceProperties/Add/{PciRoot(0x0)/Pci(0x15,0x0)} (config.plist)
- 2026-11-05 21:35: người dùng thử display sleep/wake (`pmset displaysleepnow`) trên build-31: **hoạt động**, con trỏ không vỡ lại → rủi ro "FENCEFIX mất sau wake" đóng.

## Build 32 — `tp-gpio` (2026-11-05): = build-31, gỡ `force-polling` khỏi I2C0 (DEFERRED D7, người dùng yêu cầu)
- Xoá `DeviceProperties/Add/PciRoot(0x0)/Pci(0x15,0x0)` (chỉ có `force-polling = 01000000`, thêm ở build-17). Boot-args không có `-vi2c-force-polling` từ build-17 → VoodooI2C 3.0.0 (fork lzhoang2801) sẽ thử ngắt GPIO: `TPD0._CRS` trả GpioInt qua `\_SB.GPI0` (INTC1055) khi OSYS ≥ 0x07DC — SSDT-XOSI đã bảo đảm (build-01).
- Mục đích: bớt đánh thức CPU (pin). Rủi ro: ngắt không đến → touchpad đơ/giật; VoodooI2C có thể tự lùi về polling. Đường lui: build-31 (known-good).
- plist_diff với build-31: 1 khác biệt. efi-validate 0/0 (validate-20261105T213604.md).
- Kiểm trên MÁY B: touchpad chạy mượt, cử chỉ 2–3 ngón; `log show --last boot --predicate 'process == "kernel"' | grep -i -E 'VoodooI2C|VoodooGPIO' | grep -i -E 'interrupt|polling|gpio|pin' | head -20`.
- 2026-11-05T21:36:20 Created build-32-20261105-213620-tp-gpio (tree 0819a543fd2a, ocvalidate: 0 errors, 0 warnings (validate-20261105T213604.md))

## Build 33 — `usbmap-ss` (2026-11-05): = build-32 + UTBMap có cổng USB 3 (DEFERRED D3)
- Dữ liệu: `docs/hw-dump/usb-map-20261105-220220.txt` (người dùng chạy `tools/map-usb-linux.sh` trên Linux MÁY B). Cổng gốc PCH xHCI `8086:51ED` (`\_SB.PC00.XHCI.RHUB`): `adr` sysfs = `_ADR` = số cổng macOS; `peer` ghép HS↔SS do firmware cung cấp.
- Thực tế: USB-A trái = HS02 (2) + SS02 (0x0E); USB-A phải = HS01 (1) + SS01 (0x0D); USB-C = HS04 (4) trên PCH, phần USB 3 thuộc controller TB4 `8086:461E` (`TXHC.SS01`, 20 Gbps) — KHÔNG map (D4, chưa có hỗ trợ/kiểm chứng). HS06 camera, HS07 Bluetooth (type "not used" = nội bộ). USR1/USR2, HS03/05/08–10, SS03/04 không dùng.
- UTBMap mới (`EFI/OC/Kexts/UTBMap.kext/Contents/Info.plist`, sửa bằng plistlib — không phải config.plist): HS01 3, HS02 3, HS04 9 (Type-C), HS06 255, HS07 255, SS01 3, SS02 3; `port-count` 0x0E. Đổi tên cổng theo ACPI (bản cũ đặt HS03/HS04/HS05 cho port 4/6/7 — địa chỉ giữ nguyên).
- Hạn chế: thiết bị thử trên Linux là USB 2.0 (480 Mbps) → nửa SS chưa có lần cắm thật; dựa vào `peer` của firmware. Kiểm trên macOS bằng thiết bị USB 3: `system_profiler SPUSBDataType` phải báo tối đa 5/10 Gb/s.
- `tools/map-usb-linux.sh`: sửa cột `peer` in chữ "peer" khi cổng không có cặp.
- Một thay đổi so với build-32 (UTBMap). Build-32 (touchpad GPIO) chưa test riêng — nếu touchpad lỗi trên build-33: build-34 = build-33 + `force-polling` lại. efi-validate 0/0 (validate-20261105T220932.md).
- 2026-11-05T22:09:48 Created build-33-20261105-220948-usbmap-ss (tree 26106d86cb52, ocvalidate: 0 errors, 0 warnings (validate-20261105T220932.md))
- 2026-11-05T22:12:06 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 4d83b78c4251, verified)
- 2026-11-05 22:11: build-33 usbmap-ss (gồm thay đổi build-32) ghi lên MACEFI (/dev/sdb3, kiểm hash OK, SMBIOS thật).
- 2026-11-05T22:17:58 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 0bead3b402f3, verified)
- 2026-11-05 22:18: người dùng sửa SMBIOS (bộ cũ lỗi) trong file secrets; ghi lại build-33 lên MACEFI với SMBIOS mới (/dev/sdb3, kiểm hash OK). EFI dự án không đổi (vẫn placeholder).
- 2026-11-05 22:25 kết quả build-33 (MÁY B): class count `AppleUSB30XHCIPort` = **3** (build-27: 1) → SS01/SS02 của UTBMap đã có hiệu lực; `AppleUSB20XHCIPort` = 5. **TXHC (TB4 `8086:461E`) đã được `AppleUSBXHCIPCI` gốc của macOS nhận** (`TXHC@0d000000`, active) → phần USB 3 của cổng USB-C (`TXHC.SS01`) có thể đã chạy sẵn, không cần map (UTBMap chỉ khớp `XHCI`). `system_profiler SPUSBDataType` rỗng: macOS 26 dùng `SPUSBHostDataType`. Log VoodooI2C/VoodooGPIO rỗng (bản release ít log) → chế độ touchpad chưa xác định từ log.
- 2026-11-05 22:27: người dùng: touchpad trên build-33 mượt như trước, cử chỉ bình thường → giữ không `force-polling` (D7 đóng). Tốc độ USB 3 thực tế chưa đo.
- 2026-11-05 22:30: dựng lại `docs/MACHINE-ANALYSIS.md` (hw-dump-reader) từ dump 21:47; giải mã ACPI vào `_cache/acpi/`.
- 2026-11-05 22:38: bắt đầu D6 (boot không cần USB). Viết lại POSTINSTALL-RUNBOOK §4: kiểm ESP, sao lưu, chép EFI từ USB, tạo mục boot (có cách dùng Linux live). Chờ người dùng gửi `diskutil list` và nội dung ESP.
- 2026-11-05 22:45: ESP `disk0s1` có Limine (CachyOS) → chỉ chép `EFI/OC` từ USB (build-33). `efibootmgr -c` trên CachyOS tạo **Boot0001 "OpenCore"** `HD(1,GPT,460c0790-…)/\EFI\OC\OpenCore.efi`; BootOrder `0001,0000,0003,0004,0005` (0000 = Limine `\EFI\limine\limine_x64.efi`, 0003 = "Solid State Disk" fallback, 0004/0005 = USB). Firmware Timeout 0. Chờ: khởi động không USB. Phát hiện: `PNLF` trong DSDT là trường 16-bit (DSDT:8810), không phải thiết bị → không dùng patch PNLF→XNLF. RAM 24 GB chạy 2400 MT/s.
- 2026-11-05 21:24: push nhánh `bt-backlight-audio` lên origin (đầu 475e5d7: EFI build-31 + docs + README). Không push `main` (người dùng: không push lên main).
- 2026-11-05 22:50–23:16: boot OpenCore từ ESP lỗi "Plist …VoodooPS2Keyboard.kext\Contents\Info.plist is missing … Halting on critical error" sau 2 lần chép từ macOS (`cp -R`, rồi `ditto --norsrc --noextattr`; `diff` đều báo giống hệt). Chép lại bằng `cp -r` trên CachyOS (ESP mount `/boot`, USB `sda3` ro) → **boot từ ổ trong thành công** (người dùng). D6 xong. Nghi driver FAT của firmware đọc sai mục do msdosfs của macOS ghi — CHƯA XÁC MINH.
- 2026-11-05 23:25: thêm `tools/xe-monitor.py` (đọc debug.xepm.sensors: nhiệt P/E/gói + RAPL gói/IA/GT; ioreg IntelAccelerator; CSV) và `docs/PERFORMANCE.md` (vòng đo nền build-33; XE-PM `-ngreenpm` là ứng viên đầu, cần bỏ `-v` để vừa 228).
- 2026-11-06 00:05: số đo nền build-33 (Geekbench 7: single 1076, multi 5837, GPU 1094; nghỉ 7,4 W) ghi vào docs/PERFORMANCE.md. Nhận định: P-core không turbo ở single-core, nghỉ cao → ứng viên XE-PM.
- 2026-11-06 00:07 **kernel panic** (build-33, boot từ ESP, uptime 52 phút): `Panicked task: pid 3710: powermetrics`, page fault CR2 `0xc` (NULL), RIP trong `AppleIntelTGLGraphicsFramebuffer` +0xBC88F (frame kế +0xBC8F1, +0x3B1AB, +0xE758E/+0xE79AC/+0xE7A2B), gọi từ `AppleGraphicsDeviceControl` 8.1.12. Kích hoạt bởi `sudo powermetrics --samplers cpu_power` (Claude đề nghị chạy; output bị cắt đúng lúc). Không có tên hàm vì đã bỏ `keepsyms=1` (build-29). → Cấm `powermetrics` trên stack này (PERFORMANCE.md). `xe-monitor.py`: khoá iGPU thật là `Device Utilization %` (driver để 0 kể cả khi tải) và `gartUsedBytes`; dùng `igpu_W` làm chỉ báo tải.
- powermetrics trước panic: trung bình 1,7–2,5 GHz, một mẫu 3,58 GHz; không xác định được đó là lúc single-core.
- 2026-11-06 00:13: người dùng xác nhận không có panic nào khác ngoài lần 00:07 (powermetrics) → không có panic ngẫu nhiên trên build-33.
- 2026-11-06T00:13:59 plist_edit set NVRAM/Add/7C436110-AB2A-4BBB-A880-FE41995C9F82/boot-args = 'ngreen-eu=64 ngreen-l3=6 ngreenblmax=17741 -ngreenpm -ngreentglwithgfx -allow3d -disablegfxfirmware ngreen-dmc=adlp ngreenV142=3 -ngreenv189 -ngreenkeepefi -ngreenxefix -ngreenfixbootmode amfi_get_out_of_my_way=1 -amfipassbeta' (config.plist)

## Build 34 — `xepm` (2026-11-06): = build-33 + XE-PM (người dùng duyệt 00:13)
- boot-args (226 ký tự): `ngreen-eu=64 ngreen-l3=6 ngreenblmax=17741 -ngreenpm -ngreentglwithgfx -allow3d -disablegfxfirmware ngreen-dmc=adlp ngreenV142=3 -ngreenv189 -ngreenkeepefi -ngreenxefix -ngreenfixbootmode amfi_get_out_of_my_way=1 -amfipassbeta`. Thêm `-ngreenpm`, bỏ `-v` (vừa giới hạn 228).
- XE-PM (NootedGreen JN @6f03560 `kern_xepm.cpp`, đã có trong kext md5 3a823f7c): sau 20 s — route HWP (hàm XCPM tại `_xcpm_enable_pstate_ctrs+0x1190`, chỉ khi prologue + chỗ ghi khớp byte, 25G241), EPP 0, tắt EE turbo, bật C8/C10 trong `_xcpm_cstate_table`, D3hot cho thiết bị PCI không driver. PL1 giữ của BIOS (không `ngreenpm=W`). Tắt riêng C-state: `ngreenpmcst=0`.
- Lý do: số nền build-33 (single 1076, nghỉ 7,4 W) — PERFORMANCE.md. plist_diff với build-33: 1 khác biệt. efi-validate 0/0 (validate-20261106T001359.md).
- Kiểm trên MÁY B: `sysctl debug.xepm.route debug.xepm.hwp debug.xepm.cst debug.xepm.d3 debug.xepm.eet_off` (route phải = 1); `dmesg | grep 'XeNG PM'`; Geekbench 7 CPU + nghỉ 2 phút với `xe-monitor.py` (KHÔNG powermetrics).
- 2026-11-06T00:14:11 Created build-34-20261106-001411-xepm (tree 358dede24487, ocvalidate: 0 errors, 0 warnings (validate-20261106T001359.md))
- 2026-11-06T00:15:06 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree ac70ed69431c, verified)
- 2026-11-06 00:15: build-34 xepm ghi lên MACEFI (/dev/sdb3, kiểm hash OK, SMBIOS thật). ESP ổ trong vẫn build-33.
- 2026-11-06 00:22 build-34 trên MÁY B: `debug.xepm` route 1, hwp 1, cst 1, d3 2, eet_off 1; dmesg `XeNG PM: profile on: HWP rescale 1 (route 1), EPP 0, EE turbo off 1, C8/C10 1, D3 2, PL1 0 W (0x0)` → XE-PM áp dụng đủ (PL1 không đổi, đúng ý). Chờ số đo.
- 2026-11-06 00:40: thêm `tools/xe-freq.c` — đo xung thực trong user space bằng chuỗi ADD phụ thuộc (1 chu kỳ/lệnh trên Golden Cove và Gracemont), thay powermetrics. Biên dịch + chạy thử trên MÁY A chỉ để kiểm công cụ.
- 2026-11-06 00:45 build-34 `logs/gb7-new.csv` (GB7 CPU): công suất IA ở pha tải nhẹ (2–30 W) avg 12,8 / p90 21,9 W (build-33: 7,4 / 11,3) → P-core lên turbo cao hơn; gói avg 21,9 W, max 64,9 W; P-core avg 66 °C, max 83 °C. Người dùng bỏ đo nghỉ. Chờ điểm GB7.
- 2026-11-06 00:46: điểm GB7 build-34: single 1220 (+13 %), multi 5476 (−6 %) so với build-33 (1076 / 5837). Ghi PERFORMANCE.md.
- 2026-11-06 00:50: xe-freq lần 1 trên MÁY B cho 8–24 GHz (sai): đồng hồ CLOCK_MONOTONIC_RAW nhảy nấc ~8 ms, mẫu chỉ ~50 ms. Sửa: mach_absolute_time, mẫu ~1 s, in bước đồng hồ.
- 2026-11-06 00:52: xe-freq bản mach_absolute_time trên MÁY B: timer step 17 ns (đồng hồ ổn) nhưng vẫn 6–27 GHz → chuỗi `add $imm` bị Golden Cove gộp ở renamer (>1 lệnh/chu kỳ). Sửa: chuỗi ADD thanh ghi–thanh ghi với hạng tử đọc lúc chạy. Bản 1 (`clock_gettime`) sai vì mẫu ngắn, không phải đồng hồ hệ thống.
- 2026-11-06 00:54: powermetrics (người dùng chấp nhận rủi ro) lúc single-core build-34: nhân bận nhất 3,9–4,43 GHz, gói 21–26 W. Ghi PERFORMANCE.md.
- 2026-11-06 01:02 build-34, tải đều 16 luồng `yes` + powermetrics: 10 CPU hiển thị đều 3,94–4,04 GHz, gói ~67 W → không có nhân kẹt xung dưới tải đều; các nhân 0,7–1,1 GHz lúc GB7 multi là pha ít luồng. Điểm lạ: powermetrics chỉ in 10 CPU (mong đợi 16) — đang kiểm sysctl hw.*.
- 2026-11-06 01:03: sysctl MÁY B: hw.ncpu 16, physicalcpu 6, logicalcpu 16, core_count 16, thread_count 16, perflevel0.logicalcpu 16 → macOS dùng đủ 16 luồng.
- 2026-11-06 01:13: build-34 + sysctl debug.xepm.epp=128: GB7 1222 / 5378 → EPP không ảnh hưởng multi. Tiếp: tách hwp / cst bằng sysctl.
- 2026-11-06T02:28:21 plist_edit set NVRAM/Add/7C436110-AB2A-4BBB-A880-FE41995C9F82/boot-args = 'ngreen-eu=64 ngreen-l3=6 ngreenblmax=17741 -ngreenpm -ngreentglwithgfx -allow3d -disablegfxfirmware ngreen-dmc=adlp ngreenV142=3 -ngreenv189 -ngreenkeepefi -ngreenxefix -ngreenfixbootmode amfi_get_out_of_my_way=1 -amfipassbeta ngreenpmcst=0' (config.plist)
- 2026-11-06 02:14: build-34 + sysctl debug.xepm.cst=0: GB7 single 1176, multi 7114 → C8/C10 là nguyên nhân multi giảm. (debug.xepm.hwp chưa thử: lần đầu báo unknown oid vì máy boot build-33 từ ổ trong.)

## Build 35 — `xepm-nocst` (2026-11-06): = build-34 + `ngreenpmcst=0` (người dùng duyệt 02:28)
- boot-args 240 ký tự, thêm `ngreenpmcst=0` ở CUỐI. Giới hạn ~228 là bản sao boot-args của Lilu (`checkKernelArgument`: `-ngreenpm`, `-amfipassbeta`… — `-amfipassbeta` kết thúc ở 226, vẫn trong 228); `ngreenpmcst` đọc bằng `PE_parse_boot_argn` của kernel (`kern_xepm.cpp:221`), kernel nhận tới 255. CHƯA XÁC MINH trên máy.
- XE-PM giữ HWP rescale, EPP 0, EE turbo off, D3; bỏ C8/C10 (bảng C-state gốc XCPM). plist_diff với build-34: 1 khác biệt. efi-validate 0/0 (validate-20261106T022822.md).
- Kiểm: `sysctl debug.xepm.cst` = 0, `debug.xepm.route` = 1, dmesg `C8/C10 0`; Wi-Fi còn (AMFIPass/-amfipassbeta). Lỗi → build-34.
- 2026-11-06T02:28:35 Created build-35-20261106-022835-xepm-nocst (tree 35c3e6125686, ocvalidate: 0 errors, 0 warnings (validate-20261106T022822.md))
- 2026-11-06T02:33:01 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 13d19b792cc0, verified)
- 2026-11-06 02:33: build-35 xepm-nocst ghi lên MACEFI (/dev/sdb3, kiểm hash OK, SMBIOS thật).
- 2026-11-06 02:37 build-35 trên MÁY B: sysctl debug.xepm.route 1, cst 0 → `ngreenpmcst=0` (vị trí 227–240) được kernel đọc; Wi-Fi còn (-amfipassbeta không bị cắt). dmesg không còn dòng 'XeNG PM' (bộ đệm bị log 'XeNG CS' đẩy ra).
- 2026-11-06 02:47: so GB7 macOS (~1200/7100) với Linux cùng máy (~2xxx/2xxxx): kiểm CPUID trên macOS — có AVX1.0, FMA, AVX2, BMI1/2, SHA, AES, VAES, GFNI → không phải thiếu tập lệnh. Đang kiểm đồng hồ (TSC) và xe-freq hai hệ.
- 2026-11-06 02:54: TSC đúng (2,688 GHz, sleep 30 = 30,04 s). xe-freq 1 luồng: Linux 4503/4640/4681, macOS build-35 1502/3365/4586 MHz → luồng không giữ được xung cao. Thêm XEFREQ_SAMPLES để in từng mẫu.
- 2026-11-06 03:08: GB7 trên CachyOS cùng máy: single 2195, multi 10101 (mốc). macOS 1176/7114 = 54 %/70 %.
- 2026-11-06 03:11: xe-freq từng mẫu trên macOS: 1389–4679 MHz liên tục. Thêm theo dõi loại nhân/APIC id vào xe-freq.
- 2026-11-06 03:22: xe-freq theo dõi nhân: Linux 1 nhân/4662 MHz; macOS 2–16 nhân/giây, E-core 1 %, xung giảm theo số lần đổi nhân → nút thắt single-core là chuyển nhân của scheduler. Đề xuất thử ctrsmt=off qua NVRAM.
- 2026-11-06 03:40: patch NootedGreen v8 XE-HWPAUTO (`patches/nootedgreen-gmsfix-v7-to-v8.patch`, gộp `…-v8-jn6f03560.patch`): sysctl debug.xepm.hwpauto / boot-arg ngreenpmauto=1 → HWP desired = 0. Mặc định tắt. git apply --check sạch; clang++ -fsyntax-only 0 lỗi (MacKernelSDK 3f75008, Lilu 0249c3a). Chờ người dùng build trên MÁY B (GMSFIX-RUNBOOK §v8).
- 2026-11-06T03:42:01 plist_edit set Kernel/Add[BundlePath=NootedGreen.kext]/Comment = 'NootedGreen JN 6f03560 + GMSFIX v8 (accel+FB+PAVP+FENCEFIX+XE-HWPAUTO, md5 5f88ee88)' (config.plist)

## Build 36 — `hwpauto` (2026-11-06): = build-35 + NootedGreen v8 (MỘT thay đổi: binary kext; người dùng duyệt v8 03:36)
- Kext build trên MÁY B (v7 + `patches/nootedgreen-gmsfix-v7-to-v8.patch`): md5 `5f88ee8829e51ebfee93665ff6b3f850`, sha256 `cb4b975faae087fb31aba86877eebbdd9c10ecf903ff2a5621642e2d7afed5bf`; chuỗi HWPAUTO 1, GMSFIX/FENCEFIX 8; Info.plist giống bản v7. Lưu `_cache/user-inputs/NootedGreen-v8-5f88ee88.kext`.
- Boot-args không đổi (240, có `ngreenpmcst=0`); XE-HWPAUTO mặc định TẮT → bật thử bằng `sudo sysctl -w debug.xepm.hwpauto=1`. Config chỉ đổi Comment. efi-validate 0/0 (validate-20261106T034201.md).
- 2026-11-06T03:42:59 Xoá thủ công snapshot build-27-20261105-193937-bluetooth (người dùng duyệt; cũ nhất không phải known-good, để có chỗ cho build-36)
- 2026-11-06T03:43:00 Created build-36-20261106-034300-hwpauto (tree 68c31dc0f0d4, ocvalidate: 0 errors, 0 warnings (validate-20261106T034201.md))
- 2026-11-06T03:43:17 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree edb09afd9f88, verified)
- 2026-11-06 03:43: build-36 hwpauto ghi lên MACEFI (/dev/sdb3, kiểm hash OK, SMBIOS thật).
- 2026-11-06 03:48: build-36 + ctrsmt=off (NVRAM còn): xe-freq hwpauto 0/1 = 4391/4376 MHz → HWPAUTO không tác dụng đo được. Kết quả xe-freq lệch lớn giữa các lần cùng cấu hình (3462 vs 4380).
- 2026-11-06 04:05: GB7 build-36: ctrsmt=off+hwpauto=0 → 10xx/5xxx; ctrsmt=off+hwpauto=1 → 1927/9338 (88 %/92 % Linux). Đề xuất build-37: ctrsmt=off vào NVRAM/Add + ngreenpmauto=1.
- 2026-11-06T04:22:36 plist_edit set NVRAM/Add/7C436110-AB2A-4BBB-A880-FE41995C9F82/boot-args = 'ngreen-eu=64 ngreen-l3=6 ngreenblmax=17741 -ngreenpm -ngreentglwithgfx -allow3d -disablegfxfirmware ngreen-dmc=adlp ngreenV142=3 -ngreenv189 -ngreenkeepefi -ngreenxefix -ngreenfixbootmode amfi_get_out_of_my_way=1 -amfipassbeta ngreenpmcst=0 ngreenpmauto=1' (config.plist)
- 2026-11-06 04:22: GB7 build-36 topology mặc định: hwpauto=1 → 2030/9646 (92 %/95 % Linux); hwpauto=0 → 1191/5637. ctrsmt=off kém hơn → bỏ (người dùng đã xoá NVRAM ctrsmt).

## Build 37 — `hwpauto-on` (2026-11-06): = build-36 + `ngreenpmauto=1`
- boot-args **255 ký tự** (đúng giới hạn kernel đã thấy ở build-12): `… -amfipassbeta ngreenpmcst=0 ngreenpmauto=1`. `ngreenpmauto` đọc bằng `PE_parse_boot_argn` (patch v8). Bị cắt → chỉ mất HWPAUTO (hậu quả nhẹ); khi đó làm patch v9 bật HWPAUTO theo `-ngreenpm`.
- Không thêm `ctrsmt` (mặc định tốt hơn `off`). plist_diff với build-36: 1 khác biệt. efi-validate 0/0 (validate-20261106T042236.md).
- Kiểm: `sysctl debug.xepm.hwpauto` = 1 ngay sau boot (không cần sysctl -w); GB7 ≈ 2030 / 9646.
- 2026-11-06T04:24:17 Xoá thủ công snapshot build-28-20261105-201417-pnlf (người dùng duyệt; cũ nhất không phải known-good, chỗ cho build-37)
- 2026-11-06T04:24:17 Created build-37-20261106-042417-hwpauto-on (tree 7dd9eda153e3, ocvalidate: 0 errors, 0 warnings (validate-20261106T042236.md))
- 2026-11-06T04:25:11 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 5ee312dbe66b, verified)
- 2026-11-06 04:24: build-37 hwpauto-on ghi lên MACEFI (/dev/sdb3, kiểm hash OK, SMBIOS thật).
- 2026-11-06 04:28 build-37 trên MÁY B: sysctl hwpauto 1, cst 0, route 1 → boot-args 255 ký tự được kernel đọc đủ (ngreenpmauto=1 ở vị trí cuối). Người dùng chép build-37 sang ESP ổ trong (từ CachyOS).
- 2026-11-06 04:35: cập nhật README (build-37, hiệu năng, boot-args 255 + hai giới hạn Lilu/kernel, lỗi #8–#10, cảnh báo powermetrics/chép ESP, tools), SOURCES (patch v8 + kext v8), STATE, PERFORMANCE (bảng tóm tắt), DEFERRED D11.
- 2026-11-06T04:39:32 Marked build-37-20261106-042417-hwpauto-on as known-good (user request)
- 2026-11-06T04:39:32 Marked build-37 known-good (người dùng).
- 2026-11-06 04:40: người dùng đặt mục tiêu mới → docs/ROADMAP.md (G1 iGPU, G2 Vulkan, G3 HW decode, G4 boot time). JN 6f03560 có sẵn XE-GTFREQ (ngreengtfreq), -ngreengva + macos/vadriver, Vulkan qua MoltenVK, gfxrst=1.
- 2026-11-06 05:01: G2 Vulkan — MoltenVK thấy iGPU (Intel(R) TGL, 0x9a49, Vulkan 1.4.357, MoltenVK 1.4.2). Ghi ROADMAP.
- 2026-11-06 05:02: vkcube chạy → G2 Vulkan xong (README thêm dòng Vulkan).

## GPU treo khi chạy Geekbench 7 GPU — bài Feature Matching (2026-11-06 16:3x–17:07, build-37)
- Triệu chứng (người dùng): iGPU < 1 W ở Feature Matching, > 30 phút không qua; máy gần như không dùng được. `pkill` Geekbench → màn hình đứng, bàn phím còn.
- ioreg: `xe-rec-resets 1`, `sibrestores 1`, `sibreplays 1`, `rcu 1`, `exfix 2`, `recoveryCount 0` → một lần GPU treo thật, XE-GPUREC (v2, có trong JN 6f03560) đã reset + bật lại CCS.
- kernel log từ trước 16:36:28 tới 17:03, mỗi ~5 s: `checkGPUProgress() - Signaling hardware error on channel 30` → `GPURestartSkipped stampIdx=30` → `no channel associated with stamp_idx 30` → stamp 30 (dải 24–31, kênh CCS) mồ côi, không bao giờ trả về; Geekbench chờ mãi; CPU 93 % idle.
- `logs/WindowServer-2026-11-06-170608.ips` (bug_type 409, WATCHDOG): "unresponsive work processor(s): WindowServer main thread", 80 s không check-in (sau pkill).
- `logs/Kernel_2026-11-06-170747_…gpuRestart` (Intel GPU Hang Summary): **BCS ring "Appears hung"** (HEAD 0xd4, TAIL 0xd8, lệnh cuối `0x13004103` MI_FLUSH_DW), RCS/CCS ring idle, stamp idx 32 submitted 5 / returned 3. → hậu quả sau pkill (blit của WindowServer), không phải lần treo gốc.
- Lần treo gốc trong Feature Matching chưa có log (dmesg đã trôi, dòng XeNG GPUREC đầu tiên không bắt được).
- Nghi nguyên nhân gốc (CHƯA XÁC MINH): libxedrv v20 của JN 6f03560 — JN HEAD `24450b4` (libxedrv **v21**, 2026-10-28) sửa "compute work ordered against render/blit, and working compute barriers" (serial compute encoder bỏ qua `memoryBarrierWithScope:` → dispatch đọc dữ liệu chưa ghi). Feature Matching = chuỗi compute dispatch.
- Patch dự án v8 áp lên JN HEAD bằng `patch --fuzz=3`: 7 hunk kern_gen11.cpp khớp (hunk 1 fuzz 2, cần soát), 3 file còn lại sạch.
- Tạm thời: KHÔNG chạy Geekbench 7 GPU trên build-37.

## Nâng stack lên JN 24450b4 + patch v9 (2026-11-06 19:49, người dùng duyệt)
- Người dùng: "duyệt nâng lên commit mới nhất của JN. đồng thời viết patch". `clone_ref.py --update`: JN HEAD vẫn là `24450b4` (2026-11-03), là commit duy nhất sau 6f03560.
- 6f03560→24450b4: libxedrv v21 (compute xếp thứ tự với render/blit bằng MTLSharedEvent; serial compute encoder → concurrent + barrier trước mỗi dispatch), v23 (sửa ô vuông blur khi hover, chỉ WindowServer), v24 (công tắc `/private/var/tmp/xedrv.off`: `o`/`b`/`x`); kernel: XE-PORTGUARD (route `AppleIntelPort::probePortState`, bật mặc định trên đường spoof, tắt `-ngreennoportguard`), XE-AUXBL khi thanh ghi PWM period = 0 (chỉ khi có `ngreenauxbl=N` — dự án không dùng), XE-HWCAPS114C (chỉ tác dụng khi 0x114c = 0). Tất cả JN ghi "testing".
- Patch v9 `patches/nootedgreen-gmsfix-v9-jn24450b4.patch` (sha256 3685fa72…cf0a): v8 áp bằng `patch --fuzz=3` — kern_gen11 hunk 1 fuzz 2 (JN chèn XE-PORTGUARD ngay sau `gTopoTc`; khối CURDIAG/FENCEFIX của dự án nằm sau XE-PORTGUARD, vẫn phạm vi file), 6 hunk còn lại chỉ lệch dòng; không .rej; không trùng route (PORTGUARD route probePortState, dự án route hwSetCursorImage). Thêm: `xePmInstall` mặc định `ngreenpmauto`=1, `ngreenpmcst`=0 (boot-arg vẫn ghi đè).
- Kiểm MÁY A: `git apply --check` sạch trên JN 24450b4; `clang++ -fsyntax-only` (MacKernelSDK 3f75008, Lilu 0249c3a) kern_gen11/kern_green/kern_xepm: 0 lỗi, cảnh báo 21/18/0 = JN gốc. Chưa build/chạy.
- Runbook: GMSFIX-RUNBOOK §v9 (lần này chạy `install.sh` để cài libxedrv mới; sao lưu /Library trước; không chép ESP từ macOS). DRIVER-MATRIX G2b, SOURCES.
- Kế hoạch build-38 = build-37 + kext v9 + boot-args bỏ ` ngreenpmcst=0 ngreenpmauto=1` (255 → 226). Chờ kext từ MÁY B.
- 2026-11-06T20:12:50 plist_edit bootarg-remove ngreenpmcst=0 (config.plist)
- 2026-11-06T20:12:50 plist_edit bootarg-remove ngreenpmauto=1 (config.plist)
- 2026-11-06T20:12:50 plist_edit set Kernel/Add[BundlePath=NootedGreen.kext]/Comment = 'NootedGreen JN 24450b4 + patch v9 (GMSFIX accel+FB+PAVP+FENCEFIX+XE-HWPAUTO default on, md5 7f51634a)' (config.plist)

## Build 38 — `jn24450b4-v9` (2026-11-06): = build-37 + NootedGreen JN 24450b4 + patch v9; boot-args bỏ ` ngreenpmcst=0 ngreenpmauto=1`
- Người dùng trên MÁY B: `~/xe-stack` → 24450b4 + v9, `install.sh --check` qua hết (Mode: update, 25G241, 9A49, NootedGreen loaded), `install.sh` đã cài user-space 24450b4 (libxedrv v21–v24).
- Kext: md5 `7f51634a8e8c5e122009d5653e1ed2a7`, sha256 `68a44a3a49ec8abb37398347a092bda69f9d3e60832d51288426b2111558e29a` (khớp bản trên USB); `strings | grep -c 'HWPAUTO|PORTGUARD|GMSFIX'` = 11; Info.plist giống bản v8. Lưu `_cache/user-inputs/NootedGreen-v9-7f51634a.kext`.
- boot-args 255 → **226** (cờ Lilu `-amfipassbeta` giờ kết thúc ở 226, trong 228). HWPAUTO/C8-C10 nay là mặc định của v9.
- plist_diff với build-37: 2 khác biệt (Comment NootedGreen, boot-args). efi-validate 0/0 (validate-20261106T201258.md).
- Kiểm sau boot: `sysctl debug.xepm.hwpauto debug.xepm.cst debug.xepm.route` = 1/0/1; Metal; `dmesg | grep PORTGUARD`; Wi-Fi còn. Lỗi → build-37 (lưu ý: user-space đã là 24450b4; quay hẳn về → GMSFIX-RUNBOOK §v9 "Quay về").
- 2026-11-06T20:13:28 Xoá thủ công snapshot build-30-20261105-203431-audio (người dùng duyệt; cũ nhất không phải known-good, chỗ cho build-38)
- 2026-11-06T20:13:28 Created build-38-20261106-201328-jn24450b4-v9 (tree e88df0f328fe, ocvalidate: 0 errors, 0 warnings (validate-20261106T201258.md))
- 2026-11-06T20:15:43 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 82ca41d345a9, verified)
- 2026-11-06T20:15 build-38 jn24450b4-v9 ghi lên MACEFI (/dev/sdb3, kiểm hash OK, tree 82ca41d345a9, SMBIOS thật).
- 2026-11-06 20:19 build-38 trên MÁY B (boot USB): NootedGreen + HookCase nạp, Metal 2; sysctl debug.xepm hwpauto 1 / cst 0 / route 1 → mặc định v9 hoạt động khi không có boot-arg; xe-topo 16390, xe-fencefix-n 3, xe-rowchk-post 0xffffffffffffc000 (16 bit thấp 0xc000, đúng theo JN). dmesg không có PORTGUARD/HWCAPS (HWCAPS chỉ log khi 0x114c = 0; PORTGUARD có thể bị đẩy khỏi buffer) → kiểm bằng log show. Chờ GB7 GPU.
- 2026-11-06 20:21 `log show --last boot`: 0 dòng XeNG (cả CURDIAG/GMSFIX đã biết là có) → IOLog của NootedGreen không vào unified log; trạng thái XE-PORTGUARD (armed) không kiểm được qua log, chỉ qua dmesg sớm. Không chặn test. Dòng HWCAPS Apple: DualSubSliceCountFuse 0x33, 64 EU, Sku 2 → fuse đúng, XE-HWCAPS114C không tác dụng (đúng dự kiến).
- 2026-11-06 20:26 build-38 GB7 GPU: VẪN kẹt ở Feature Matching (iGPU 0,1–0,2 W), xe-rec-resets 1, recoveryCount 0 → giả thuyết libxedrv v20 BỊ BÁC BỎ (libxedrv v24 cùng triệu chứng). JN STATUS.md: triệu chứng stamp CCS 24–31 'no channel associated' = CCS mất cấu hình sau reset domain render (XE-GPUREC v2 xử lý RCU_MODE); JN không công bố kết quả GB GPU. Đang thu: xe-rec-* đầy đủ, .gpuRestart đầu tiên, log AppleIntelTGLGraphics (vào được unified log).

## Phân tích GB7 GPU treo trên build-38 (2026-11-06 20:35; `logs/gb7/`)
- Dòng thời gian (`restart-log.txt`, `log show --last boot`): 20:25:01.550 `checkGPUProgress` báo lỗi **cùng lúc** kênh 1 (stamp 1, RCS) và kênh 29 (stamp 29, dải CCS 24–31). 20:25:04 Apple restart kênh 1 (`GPURestartBegin/End stampIdx=1`) → đây là lần reset XE-GPUREC đếm (`xe-rec-resets` 1, `xe-rec-last` 0x40005D10 = own RCS, ret 1, kick 0, did 0xD: khôi phục CCS + replay CCS + RCU_MODE; CCS HWS_PGA 0x40005xxx). Ngay sau đó stamp 29: `GPURestartSkipped` / `no channel associated with stamp_idx 29` mỗi ~5 s tới khi tắt máy (70 lần). Không có reset nào khác.
- → Bài Feature Matching treo **cả RCS lẫn CCS**. Reset miền render chỉ phục hồi kênh RCS; stamp CCS đang chạy bị phần cứng bỏ, replay của XE-GPUREC không trả nó về và CCS không còn context hoạt động → Apple không restart được kênh → Geekbench chờ mãi. Khác với lỗi JN đã sửa (CCS bị tắt sau reset): ở đây RCU_MODE đã bật lại (`xe-rec-rcu` 1, `exfix` 2) mà stamp vẫn mồ côi. Nguyên nhân treo gốc trong shader/compute: CHƯA XÁC MINH.
- Giả thuyết libxedrv v20 bị bác bỏ (v24 cùng triệu chứng).
- `.gpuRestart` 17:07, 17:32, 20:03:46, 20:17:17: **giống hệt nhau** (BCS ring treo HEAD 0xd4 / TAIL 0xd8, `MI_FLUSH_DW` 0x13004103, context ID 5, stamp 32 submitted 5 / returned 3), xảy ra ~30–60 s sau mỗi lần boot; Apple tự phục hồi (BCS ngoài miền render, XE-GPUREC không đếm). Lỗi riêng, lặp mỗi boot, chưa thấy hậu quả. 20:25 không có file `.gpuRestart` (DumpGPURestart bị sandbox chặn `CrashReporterSupportHelper`).
- `.gpuRestart` 19:51: `mediaanalysisd` (JN STATUS: tác nhân treo hay gặp nhất; `launchctl disable gui/$UID/com.apple.mediaanalysisd`).
- `Kernel-2026-11-06-200320.panic`: page fault trong **AirportItlwm** (Wi-Fi) — không liên quan GPU; ghi riêng.
- 2026-11-06T20:37:42 Marked build-38-20261106-201328-jn24450b4-v9 as known-good (user request)
- 2026-11-06T20:44 build-38 đánh dấu known-good (người dùng). XE-GPUREC v3: DỪNG, chưa viết patch.
- 2026-11-06T20:53:10 plist_edit bootarg-add gfxrst=1 (config.plist)

## Build 39 — `gfxrst` (2026-11-06, ROADMAP G4; người dùng: "bỏ qua G1, tiếp tục G3 và G4"): = build-38 + `gfxrst=1`
- Bằng chứng: JN CHANGELOG 2026-10-21 / STATUS "Boot screen": `Resolution=Max` + `gfxrst=1` bỏ ~18 s chép framebuffer boot (3840×2400). WhateverGreen 1.7.1 `kern_weg.cpp:101` đọc `gfxrst` bằng `PE_parse_boot_argn` (giới hạn kernel 255, không phải bản sao Lilu 228); mặc định iGPU = `FB_COPY` (2), `1` = `FB_RESET`. Dự án đã có `Resolution=Max`.
- Panel 1920×1080 = 22 % số pixel của 3840×2400 → ước tiết kiệm ~4 s (CHƯA XÁC MINH, phải đo).
- boot-args 226 → 235 (nối cuối; `-amfipassbeta` vẫn kết thúc ở 226 ≤ 228). efi-validate 0/0 (validate-20261106T205310.md).
- Cần đo cùng cách trên build-38 và build-39 (ROADMAP G4).
- 2026-11-06T21:00:07 Xoá thủ công snapshot build-32-20261105-213620-tp-gpio (người dùng duyệt; chỗ cho build-39)
- 2026-11-06T21:00:07 Created build-39-20261106-210007-gfxrst (tree ded3ee3a7014, ocvalidate: 0 errors, 0 warnings (validate-20261106T205310.md))
- 2026-11-06 21:07 Mốc G4 build-38 (boot USB): bấm giờ picker OpenCore → màn hình đăng nhập **38 s** (người dùng). kern.boottime 21:05:52.606 → loginwindow 'Login Window Application Started' 21:05:57.481 (+4,9 s), WindowServer dòng đầu 21:05:57.236 (+4,6 s). Khoảng kernel→loginwindow ngắn bất thường so với 38 s → phần lớn thời gian nằm trước mốc kern.boottime hoặc sau loginwindow (CHƯA XÁC MINH).
- 2026-11-06T21:10:35 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 1b21524cc8e5, verified)
- 2026-11-06T21:10 build-39 gfxrst ghi lên MACEFI (/dev/sdb3, kiểm hash OK, SMBIOS thật).
- 2026-11-06 21:12 build-39 đo G4: picker → đăng nhập **23 s** (build-38: 38 s; -15 s, lớn hơn ước 4 s). Log: system boot 21:11:46.000 → WindowServer có token loginwindow 21:12:00.718 (+14,7 s) → ~8 s trước kernel (picker + OpenCore + boot.efi). Màn hình nháy đen ngắn khi framebuffer khởi tạo (FB_RESET xoá console thay vì chép logo) — đúng dự kiến của gfxrst=1.
- 2026-11-06T21:16:08 plist_edit bootarg-remove gfxrst=1 (config.plist)
- 2026-11-06T21:16:08 plist_edit bootarg-add gfxrst=4 (config.plist)
- 2026-11-06T21:20:54 Xoá thủ công snapshot build-33-20261105-220948-usbmap-ss (người dùng duyệt; chỗ cho build-40)

## Build 40 — `gfxrst4` (2026-11-06, thử nghiệm G4; người dùng: "thử build 40, tệ quá thì về build 39"): = build-39, `gfxrst=1` → `gfxrst=4`
- Mục tiêu: bỏ nháy đen của FB_RESET mà giữ tốc độ. `4` = `FB_NONE` (WhateverGreen không chép, không xoá). Có thể lộ rác hình ở lần đặt chế độ đầu; XE-BOOTHOLD (JN) giữ plane + đèn nền tắt tới khi ring WindowServer quay vòng — CHƯA XÁC MINH có che được không.
- boot-args 235 (không đổi độ dài). efi-validate 0/0 (validate-20261106T211609.md). Lùi: build-39.
- 2026-11-06T21:20:55 Created build-40-20261106-212055-gfxrst4 (tree 20efbf85549f, ocvalidate: 0 errors, 0 warnings (validate-20261106T211609.md))
- 2026-11-06T21:26:31 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree eb8c609f3dca, verified)
- 2026-11-06T21:26 build-40 gfxrst4 ghi lên MACEFI (/dev/sdb3, kiểm hash OK, SMBIOS thật).
- 2026-11-06T21:30:05 plist_edit bootarg-remove gfxrst=4 (config.plist)
- 2026-11-06T21:30:05 plist_edit bootarg-add gfxrst=1 (config.plist)
- 2026-11-06 21:29 build-40 trên MÁY B: không nhanh hơn build-39, hình lúc boot khó chịu hơn (người dùng); Wi-Fi OK ở cả build-39 và 40. → **Giữ `gfxrst=1` (build-39).** `EFI/` dự án quay về build-39 (plist_diff 0 khác biệt; snapshot SKIP trùng build-39). Chờ cắm USB để ghi lại build-39.

## Patch v10 (2026-11-06 21:45; người dùng hỏi "sao không patch để ngreen-eu/ngreen-l3 mặc định 64 và 6")
- `kern_gen11.cpp`: mặc định khi không có boot-arg = giá trị máy này: `gTopoSs` 12→8, `gTopoL3` 8→6 (xeTopoArgs, dòng 28), `getV142SubmitBlitMode` → 3, `blmax` 0→17741, `dmcArg` ""→"adlp". Boot-arg vẫn ghi đè. Không dò fuse (JN dòng 23–25: đọc fuse lúc boot làm treo boot). Đã soát: `gTopoSs/gTopoL3` dùng trực tiếp (patch r3b/r3bbb dòng 2606, initHardwareCaps 6847), không có chỗ coi 12/8 là "không ghi đè" (chỉ nhãn log "(default)"). `ngreenblmax`, `ngreen-dmc`, `ngreen-eu`, `ngreen-l3` chỉ đọc ở 1 chỗ mỗi cái.
- Patch: `patches/nootedgreen-gmsfix-v9-to-v10.patch` (sha256 9599beee…6b6d), gộp `…-v10-jn24450b4.patch` (sha256 1b232960…0567). apply-check sạch; clang++ -fsyntax-only 0 lỗi, 21 cảnh báo = JN gốc.
- Kế hoạch: build-41 = build-39 + kext v10 + boot-args 235 → 163; build-42 = + `-ngreengva` (G3). Runbook GMSFIX-RUNBOOK §v10 (gồm build plugin VA cùng lúc).
- (Ghi chú) Thư mục scratch bị xoá khi phiên khôi phục; cây v10 dựng lại từ JN 24450b4 + v9 + 4 thay thế (mỗi chuỗi khớp đúng 1 lần).
- 2026-11-06T22:09:07 plist_edit bootarg-remove ngreen-eu=64 (config.plist)
- 2026-11-06T22:09:07 plist_edit bootarg-remove ngreen-l3=6 (config.plist)
- 2026-11-06T22:09:07 plist_edit bootarg-remove ngreenblmax=17741 (config.plist)
- 2026-11-06T22:09:07 plist_edit bootarg-remove ngreen-dmc=adlp (config.plist)
- 2026-11-06T22:09:07 plist_edit bootarg-remove ngreenV142=3 (config.plist)
- 2026-11-06T22:09:07 plist_edit set Kernel/Add[BundlePath=NootedGreen.kext]/Comment = 'NootedGreen JN 24450b4 + patch v10 (v9 + defaults 64EU/L3 6, V142 3, blmax 17741, dmc adlp; md5 eb2d2843)' (config.plist)

## Build 41 — `v10-defaults` (2026-11-06): = build-39 + NootedGreen v10; boot-args bỏ `ngreen-eu=64 ngreen-l3=6 ngreenblmax=17741 ngreen-dmc=adlp ngreenV142=3`
- Kext build trên MÁY B (`~/xe-stack` v9 + `nootedgreen-gmsfix-v9-to-v10.patch`): md5 `eb2d28435631595d630ed5fa9a241250`, sha256 `bc3b8ea293ba4a9836275a5845b92a756e8810a14f8cacbd0e222a6ef1c733cb` (khớp bản trên USB); strings HWPAUTO|PORTGUARD|GMSFIX = 11; Info.plist như v9. Lưu `_cache/user-inputs/NootedGreen-v10-eb2d2843.kext`.
- boot-args 235 → **163**. plist_diff với build-39: 2 khác biệt (Comment, boot-args). efi-validate 0/0 (validate-20261106T220908.md).
- Kiểm: phải y như build-39 — `xe-topo` 16390, độ sáng tối đa, con trỏ, Metal 2, Wi-Fi, `sysctl debug.xepm.hwpauto/cst` 1/0.
- 2026-11-06T22:09:46 Xoá thủ công snapshot build-34-20261106-001411-xepm (người dùng duyệt; chỗ cho build-41)
- 2026-11-06T22:09:46 Created build-41-20261106-220946-v10-defaults (tree ed250ffb6334, ocvalidate: 0 errors, 0 warnings (validate-20261106T220908.md))
- 2026-11-06T22:09:51 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 4f653f06cdc4, verified)
- 2026-11-06T22:09 build-41 v10-defaults ghi lên MACEFI (/dev/sdb3, kiểm hash OK, SMBIOS thật).
- 2026-11-06 22:12 build-41 trên MÁY B: xe-topo 16390, xe-fencefix-n 3, hwpauto 1 / cst 0, Metal 2 → mặc định v10 đúng khi không có boot-arg. Plugin VA CHƯA cài (/Library/GPUBundles không có VADriver). Chờ: độ sáng/con trỏ/Wi-Fi.
- 2026-11-06 22:14 build-41: độ sáng, con trỏ, Wi-Fi bình thường (người dùng). Plugin VA đã cài trên MÁY B (người dùng).
- 2026-11-06T22:14:58 plist_edit bootarg-add -ngreengva (config.plist)

## Build 42 — `gva` (2026-11-06, ROADMAP G3): = build-41 (known-good chưa đánh dấu) + `-ngreengva`
- JN STATUS: H.264 giải mã phần cứng (VDBOX, bit-exact so với giải mã phần mềm) với `-ngreengva` + plugin VA vá; HEVC: XE-GVAHEVC (`IOGVAHEVCDecode`=2) + sửa HCP trong plugin. NootedGreen tự đặt `hwgva-id`/IOVARendererID (XE-GVAID) khi có cờ. FairPlay hỏng (JN #11); Safari vẫn giải mã CPU.
- `-ngreengva` đọc bằng `checkKernelArgument` (Lilu) → nối cuối, kết thúc ở 174 ≤ 228. boot-args 163 → 174. efi-validate 0/0 (validate-20261106T221459.md).
- Plugin VA đã cài trên MÁY B (`/Library/GPUBundles/AppleIntelTGLGraphicsVADriver.bundle`, người dùng 22:14).
- Rủi ro CHƯA XÁC MINH: PAVPFIX của dự án (tắt nhánh PAVP) với đường giải mã; stolen 60 MB.
- 2026-11-06T22:16:11 Marked build-41-20261106-220946-v10-defaults as known-good (user request)
- 2026-11-06T22:16:11 Xoá thủ công snapshot build-35-20261106-022835-xepm-nocst (người dùng duyệt; chỗ cho build-42)
- 2026-11-06T22:16:11 Created build-42-20261106-221611-gva (tree d3c96a1d1ea6, ocvalidate: 0 errors, 0 warnings (validate-20261106T221459.md))
- 2026-11-06T22:23:17 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree f00197872b84, verified)
- 2026-11-06T22:23 build-42 gva ghi lên MACEFI (/dev/sdb3, kiểm hash OK, SMBIOS thật).
- 2026-11-06 22:25 build-42 trên MÁY B: VTIsHardwareDecodeSupported H264 true, HEVC true (VideoToolbox báo có bộ giải mã phần cứng). Chưa thử giải mã thật.

## build-42 `gva`: 2 kernel panic (2026-11-06 22:31 / 22:33; `logs/Kernel-2026-11-06-223132.panic`, `…223332.panic`)
- **Panic 1 (22:31:32, uptime 7,7 s, kernel_task):** `divide error` trong `com.xxxxx.driver.AppleIntelTGLGraphicsFramebuffer` (+0x6c0c7), gọi từ NootedGreen `fbTimingsWorker(void*, void*)+0x145` (thread call của `-ngreenfixbootmode`, gọi `hwCRTCToIODetailedTimingInformation` sớm lúc boot). JN đã chặn một số chia (p->0x164 = 0) nhưng lần này vẫn có phép chia cho 0 khác / chạy đua lúc boot. Lần đầu thấy; không liên quan rõ tới `-ngreengva`. Tần suất: 1 lần. CHƯA XÁC MINH.
- **Panic 2 (22:33:32, uptime 86 s, `VTDecoderXPCService` pid 787 — lúc phát video):** page fault CR2 `0x284` (NULL+0x284) trong `com.xxxxx.driver.AppleIntelTGLGraphics` (+0x3a217), ngăn xếp từ NootedGreen `Gen11::IGHardwareContextwithOptions+0x24` → `IGHardwareContextinitWithOptions+0x21` → hàm gốc của Apple. → Tạo hardware context cho bộ giải mã video làm panic.
- Giả thuyết (CHƯA XÁC MINH): PAVPFIX của dự án ép nhánh "PAVP disabled" vì context PAVP (`accel+0x1278`) không được tạo trên máy này; context giải mã video có thể tham chiếu context PAVP đó → NULL+0x284. Máy JN (giải mã H.264 chạy) không cần PAVPFIX.
- Quyết định đề xuất: **quay về build-41** (không `-ngreengva`) — mọi giải mã phần cứng (QuickTime, Photos, thumbnail Finder) đều có thể kích hoạt panic 2. G3 tạm dừng.
- 2026-11-06T22:45:13 plist_edit bootarg-remove -ngreengva (config.plist)
- 2026-11-06T22:47:08 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 4f653f06cdc4, verified)
- 2026-11-06T22:47 Quay về build-41 (người dùng): bỏ `-ngreengva`, plist_diff với build-41 = 0, ghi MACEFI (/dev/sdb3, kiểm hash OK). G3 tạm dừng.
- 2026-11-06 22:51 build-41 boot lại trên MÁY B: nvram boot-args = 163 ký tự đúng build-41 (không -ngreengva); VTIsHardwareDecodeSupported H264 false, HEVC false → giải mã quay về phần mềm (XE-NOGVA), đúng dự kiến.
- 2026-11-06T22:52:53 plist_edit bootarg-add -ngreengva (config.plist)
- 2026-11-06T22:52:54 plist_edit bootarg-add -ngreennopavpfix (config.plist)
- 2026-11-06T22:54:29 Xoá thủ công snapshot build-36-20261106-034300-hwpauto (người dùng duyệt; chỗ cho build-43)

## Build 43 — `gva-nopavp` (2026-11-06, người dùng: "thử -ngreengva với -ngreennopavpfix"): = build-41 + `-ngreengva -ngreennopavpfix`
- Kiểm giả thuyết panic 2 của build-42 (NULL+0x284 khi tạo context giải mã ← PAVPFIX). Cả hai cờ đọc bằng `checkKernelArgument` → nối cuối, kết thúc ở 191 ≤ 228. boot-args 163 → 191. efi-validate 0/0 (validate-20261106T225254.md).
- Rủi ro: không PAVPFIX → có thể quay lại panic `PAVPCommandCallback` CR2 0xb8 lúc `startGraphicsEngine` (build-20/21). Lùi: ghi lại build-41 lên USB từ Linux (ESP ổ trong còn build-37).
- 2026-11-06T22:54:29 Created build-43-20261106-225429-gva-nopavp (tree 9da654d0f7d2, ocvalidate: 0 errors, 0 warnings (validate-20261106T225254.md))
- 2026-11-06T22:54:30 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 6b233893684b, verified)
- 2026-11-06T22:54 build-43 gva-nopavp ghi lên MACEFI (/dev/sdb3, kiểm hash OK, SMBIOS thật).
- 2026-11-06T22:58:12 plist_edit bootarg-remove -ngreennopavpfix (config.plist)
- 2026-11-06T22:58:12 plist_edit bootarg-remove -ngreengva (config.plist)
- 2026-11-06T22:58:26 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 4f653f06cdc4, verified)
- 2026-11-06 22:58 build-43 trên MÁY B: **panic** (người dùng: "có vẻ như panic rồi"; chưa có file `.panic`). → Tắt PAVPFIX không dùng được trên máy này (khớp panic PAVPCommandCallback cũ, CHƯA XÁC MINH vì chưa có log). Quay về build-41: plist_diff = 0, ghi MACEFI (/dev/sdb3, kiểm hash OK). G3 dừng: cần PAVPFIX để boot, nhưng với PAVPFIX thì tạo context giải mã panic NULL+0x284.
- 2026-11-06 23:02 Xác nhận panic build-43: `logs/Kernel-2026-11-06-225630.panic` và `…230004.panic` (2 lần boot, boot-args có `-ngreengva -ngreennopavpfix`), cả hai giống hệt: uptime ~14 s, kernel_task, page fault **CR2 0xb8** (RAX/RBX/RCX = 0) trong `com.xxxxx.driver.AppleIntelTGLGraphics` +0x29dc7 = `IntelAccelerator::PAVPCommandCallback` (0x29c50 theo ghi chú PAVPFIX) +0x177, gọi từ NootedGreen trong lúc start. Đúng panic PAVPFIX đã sửa (context PAVP `accel+0x1278` NULL). → **PAVPFIX bắt buộc trên máy này.** G3 dừng hẳn với stack hiện tại.
- 2026-11-06 23:12 build-41 dùng thường (App Store, Photos, YouTube trên Chrome), xe-monitor 201 mẫu: igpu_W min/avg/max 0,0/0,4/2,8; cpu_W 2,5/13,7/43,4; pkg 8,0/20,5/53,0 W. Không có xe-rec-resets (chưa reset), dmesg không có checkGPUProgress/GPURestart, không .gpuRestart mới → GPU làm việc bình thường; iGPU thấp vì tải compositing nhẹ; CPU cao do giải mã video phần mềm (không có HW decode).

## Patch v11 XE-PAVPCTX (2026-11-06 23:20; người dùng: "thử patch11 đi")
- Wrapper `Gen11::startGraphicsEngine` (route có sẵn của JN, V163): nếu không phải TGL thật và có `-ngreenpavpctx` → `accel+0x1300 |= 0x8` trước khi gọi hàm gốc; sau đó ghi ioreg `xe-pavp-1300-pre/-post`, `xe-pavp-ctx` + IOLog `XeNG PAVPCTX`. Dựa hoàn toàn trên ghi chú PAVPFIX (2026-11-04) của dự án; không phân tích thêm binary Apple. PAVPFIX giữ nguyên.
- Patch `nootedgreen-gmsfix-v10-to-v11.patch` (sha256 37e4c6bf…8a24), gộp `…-v11-jn24450b4.patch` (sha256 050dab16…ddcc); apply-check sạch; syntax 0 lỗi, 21 cảnh báo.
- Kế hoạch: build-44 (kext v11 + `-ngreenpavpctx`) → kiểm boot + `xe-pavp-ctx`; rồi build-45 (+ `-ngreengva`). Lùi: build-41.
- 2026-11-06T23:22:38 plist_edit bootarg-add -ngreenpavpctx (config.plist)
- 2026-11-06T23:22:38 plist_edit set Kernel/Add[BundlePath=NootedGreen.kext]/Comment = 'NootedGreen JN 24450b4 + patch v11 (v10 + XE-PAVPCTX opt-in -ngreenpavpctx; md5 5adbfbb7)' (config.plist)
- 2026-11-06T23:23:14 Xoá thủ công snapshot build-39-20261106-210007-gfxrst (người dùng duyệt; chỗ cho build-44)

## Build 44 — `pavpctx` (2026-11-06): = build-41 + NootedGreen v11 + `-ngreenpavpctx`
- Kext v11 build trên MÁY B: md5 `5adbfbb74709d48e50674299b0b8e729`, sha256 `7b6aee4a7f42a3b8ba3b29d9911a8a2087c38244dd1448afd01f36b3296e6291` (khớp USB); strings PAVPCTX = 1; Info.plist như v10. Lưu `_cache/user-inputs/NootedGreen-v11-5adbfbb7.kext`.
- boot-args 163 → 178 (`-ngreenpavpctx` là cờ Lilu, kết thúc ở 178 ≤ 228). efi-validate 0/0 (validate-20261106T232238.md).
- Kiểm: boot được không; `ioreg … grep xe-pavp` (`xe-pavp-ctx` 1?); `dmesg | grep PAVP`. Lỗi → build-41.
- 2026-11-06T23:23:14 Created build-44-20261106-232314-pavpctx (tree 504a24139653, ocvalidate: 0 errors, 0 warnings (validate-20261106T232238.md))
- 2026-11-06T23:23:22 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 7c084247530d, verified)
- 2026-11-06T23:23 build-44 pavpctx ghi lên MACEFI (/dev/sdb3, kiểm hash OK, SMBIOS thật).
- 2026-11-06 23:28 build-44 trên MÁY B: **panic lúc boot** (`logs/Kernel-2026-11-06-232542.panic`, uptime 7,9 s, kernel_task): page fault **CR2 0x30** trong `com.xxxxx.driver.AppleIntelTGLGraphics` +0x13e80, ngăn xếp: NootedGreen `Gen11::start+0x1f94` → `Gen11::startGraphicsEngine+0x308` (lời gọi hàm gốc) → Apple (+0x2514b, +0x28f6f, +0x13e80). → Bật `accel+0x1300` bit 3 làm `startGraphicsEngine` đi đường tạo PAVP nhưng thiếu điều kiện khác (con trỏ NULL+0x30) → **v11 thất bại.** G3 dừng hẳn; còn hướng issue cho JN. Quay về build-41.
- 2026-11-06T23:29:00 plist_edit bootarg-remove -ngreenpavpctx (config.plist)
- 2026-11-06T23:29:00 plist_edit set Kernel/Add[BundlePath=NootedGreen.kext]/Comment = 'NootedGreen JN 24450b4 + patch v10 (v9 + defaults 64EU/L3 6, V142 3, blmax 17741, dmc adlp; md5 eb2d2843)' (config.plist)
- 2026-11-06 23:32 Phân tích panic build-44 (người dùng: "phân tích panic và lên kế hoạch patch mới, không cần ghi lại USB"):
  - Chắc chắn: panic nằm **bên trong hàm gốc** `IntelAccelerator::startGraphicsEngine` (khung NG `startGraphicsEngine+0x308` = ngay sau lời gọi hàm gốc), lúc 7,9 s, đọc trường +0x30 của một con trỏ NULL. Không có `-ngreenpavpctx` thì cùng kext/boot-args không panic (build-41). → Bit 3 của `accel+0x1300` đúng là mở đường tạo PAVP, nhưng đường đó cần một đối tượng không tồn tại trên máy này.
  - Giả thuyết (CHƯA XÁC MINH): đối tượng thiếu là giao diện tới Intel ME/CSE — JN #11: plugin VA báo "ME not loaded" và FairPlay không chạy; PAVP phần cứng cần phiên với ME, mà macOS trên máy này không có driver ME (HECI). Nếu đúng thì **không thể tạo context PAVP thật**, và mọi cách bật PAVP đều sẽ panic.
  - Hệ quả cho G3: chỉ còn hướng làm cho đường tạo context giải mã **không cần** context PAVP (panic NULL+0x284). Muốn làm phải biết hàm tạo context của Apple đọc gì từ context PAVP — việc này cần phân tích mã máy driver của Apple; Claude không làm được trong dự án này (lần thử 2026-11-06 20:4x bị bộ lọc an toàn chặn). → chuyển cho JN (issue) hoặc người có công cụ RE.
  - Kế hoạch patch mới khả thi (không cần phân tích driver Apple): **v12 chẩn đoán + an toàn**: (1) trong wrapper `IGHardwareContextinitWithOptions` có sẵn của NootedGreen, nếu `accel+0x1278` NULL và lời gọi đến từ client video thì trả lỗi thay vì gọi hàm gốc → VideoToolbox lùi về giải mã phần mềm, không panic; (2) ghi `params`/loại context ra ioreg để đính kèm issue. Không đem lại giải mã phần cứng; chỉ cho phép để `-ngreengva` mà không panic (vô ích nếu không có HW decode) → **giá trị thấp, chưa làm**.
  - Trạng thái: USB = build-44 (panic lúc boot, người dùng chưa cho ghi lại); `EFI/` dự án = build-41 (plist_diff 0, kext v10).
- 2026-11-06 23:40 Người dùng đo build-41: dùng thường pkg avg 20,6 W (CPU 13,7, iGPU 0,39); nghỉ 52 s pkg avg 11,7 / med 9,7 / min 7,9 W (CPU med 3,9 W). Ghi PERFORMANCE.md; CSV chép vào logs/*-build41.csv.
- 2026-11-06 23:44 Đo nghỉ A/B/C (cst, EPP): đều ~8 W → giữ mặc định v9 (cst 0, EPP 0). Ghi PERFORMANCE.md.
- 2026-11-07T00:12:21 plist_edit set Kernel/Add[BundlePath=AirportItlwm.kext]/Comment = 'AirportItlwm-Tahoe v2.4.0-alpha (laobamac/itlwm 7204c69, official release) - native IO80211Family/IOSkywalkFamily, no Modern Wireless root patch' (config.plist)
- 2026-11-07T00:12:22 plist_edit set Kernel/Add[BundlePath=AirportItlwm.kext]/MinKernel = '25.0.0' (config.plist)
- 2026-11-07T00:12:22 plist_edit set Kernel/Add[BundlePath=AirportItlwm.kext]/MaxKernel = '25.99.99' (config.plist)
- 2026-11-07T00:12:22 plist_edit set Kernel/Add[BundlePath=IOSkywalkFamily.kext]/Enabled = False (config.plist)
- 2026-11-07T00:12:22 plist_edit set Kernel/Add[BundlePath=IO80211FamilyLegacy.kext]/Enabled = False (config.plist)
- 2026-11-07T00:12:29 plist_edit set Kernel/Block[0]/Enabled = False (config.plist)

## Build 45 — `wifi-laobamac` (2026-11-07 00:12; người dùng: "thử đổi sang driver wifi của JN", duyệt DRIVER-MATRIX W-alt 00:10): = build-41 + Wi-Fi laobamac
- `release-fetch`: laobamac/itlwm `v2.4.0-alpha` (pre-release, người dùng yêu cầu), asset `AirportItlwm-Tahoe-v2.4.0-RELEASE-alpha-7204c69.zip`, sha256 A5D098E6…FCF9 khớp GitHub digest. Info.plist: `com.zxystd.AirportItlwm` 2.4.0, phụ thuộc `com.apple.iokit.IO80211Family` + `IOSkywalkFamily` gốc, có ID `0x27258086` (AX210). JN dùng bản tự build `738d4c6` — dự án dùng release chính thức.
- config (plist_diff với build-41, 6 khác biệt): AirportItlwm Comment + MinKernel 25.0.0 / MaxKernel 25.99.99 (như JN); `IOSkywalkFamily.kext`, `IO80211FamilyLegacy.kext` Enabled=false; Block `com.apple.iokit.IOSkywalkFamily` Enabled=false. Giữ AMFIPass/`-amfipassbeta` (root patch Modern Audio), `DisableIoMapper` true. Chưa thêm `itlwm_he=1`.
- efi-validate 0/0 (validate-20261107T001229.md). Runbook MÁY B: POSTINSTALL-RUNBOOK §6 (Revert root patch, áp lại chỉ Modern Audio).
- 2026-11-07T00:13:33 Xoá thủ công snapshot build-40-20261106-212055-gfxrst4 (người dùng duyệt; chỗ cho build-45)
- 2026-11-07T00:13:33 Created build-45-20261107-001333-wifi-laobamac (tree 28037590c2c7, ocvalidate: 0 errors, 0 warnings (validate-20261107T001229.md))
- 2026-11-07T00:17:08 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree be02082846cc, verified)
- 2026-11-07T00:17 build-45 wifi-laobamac ghi lên MACEFI (/dev/sdb3, kiểm hash OK, SMBIOS thật).
- 2026-11-07T00:21 build-45 trên MÁY B: Wi-Fi hoạt động (người dùng). Chưa có output kmutil / chưa rõ đã Revert root patch Modern Wi-Fi chưa.
- 2026-11-07 00:25 Audio không root patch: người dùng chọn **VoodooHDA** (thay SimpleHDA — không license + binary Apple). `release-fetch` CloverHackyColor/VoodooHDA `Release368` (3.6.8, bản ổn định), sha256 9AAA01B2…ADB0 khớp digest; `org.voodoo.driver.VoodooHDA`, phụ thuộc IOAudioFamily → cài `/Library/Extensions` trên MÁY B (Dortania), không đổi EFI. DRIVER-MATRIX #15b, POSTINSTALL-RUNBOOK §7.
- 2026-11-07T00:29:46 plist_edit set Kernel/Add[BundlePath=IOSkywalkFamily.kext]/Enabled = False (config-install.plist)
- 2026-11-07T00:29:46 plist_edit set Kernel/Add[BundlePath=IO80211FamilyLegacy.kext]/Enabled = False (config-install.plist)
- 2026-11-07T00:29:46 plist_edit set Kernel/Block[0]/Enabled = False (config-install.plist)
- 2026-11-07T00:29:46 plist_edit set Kernel/Add[BundlePath=AirportItlwm.kext]/MinKernel = '25.0.0' (config-install.plist)
- 2026-11-07T00:29:46 plist_edit set Kernel/Add[BundlePath=AirportItlwm.kext]/MaxKernel = '25.99.99' (config-install.plist)
- 2026-11-07T00:29:46 plist_edit set Kernel/Add[BundlePath=AirportItlwm.kext]/Comment = 'AirportItlwm-Tahoe v2.4.0-alpha (laobamac/itlwm 7204c69, official release) - native IO80211Family/IOSkywalkFamily, no Modern Wireless root patch' (config-install.plist)
- 2026-11-07 00:29 MÁY B (build-45): Revert root patch OCLP xong; **VoodooHDA 3.6.8 hoạt động** (người dùng: "ổn định hơn root patching"); Wi-Fi laobamac hoạt động. → Máy **không còn root patch nào**.
- 2026-11-07 00:30 `config-install.plist` (cấu hình dự phòng không tăng tốc) vẫn bơm IOSkywalkFamily/IO80211FamilyLegacy + Block Skywalk gốc → không hợp với AirportItlwm laobamac. Sửa giống `config.plist` (6 mục: 2 kext + Block Enabled=false, AirportItlwm MinKernel 25.0.0 / MaxKernel 25.99.99, Comment). efi-validate 0/0 (validate-20261107T002946.md). → build-46 (chỉ khác build-45 ở config-install.plist).
- 2026-11-07T00:34:42 Marked build-45-20261107-001333-wifi-laobamac as known-good (user request)
- 2026-11-07T00:34:42 Xoá thủ công snapshot build-42-20261106-221611-gva (người dùng duyệt; chỗ cho build-46). build-45 đánh dấu known-good (người dùng).
- 2026-11-07T00:34:42 Created build-46-20261107-003442-config-install-wifi (tree 1e857ce7d220, ocvalidate: 0 errors, 0 warnings (validate-20261107T002946.md))
- 2026-11-07T00:35:52 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 4d8c13b03131, verified)
- 2026-11-07T00:35 build-46 config-install-wifi ghi lên MACEFI (/dev/sdb3, kiểm hash OK, SMBIOS thật).
- 2026-11-07T00:39:05 plist_edit set Kernel/Add[BundlePath=AMFIPass.kext]/Enabled = False (config.plist)
- 2026-11-07T00:39:05 plist_edit bootarg-remove -amfipassbeta (config.plist)
- 2026-11-07T00:39:05 plist_edit bootarg-add itlwm_he=1 (config.plist)

## Build 47 — `wifi6-noamfipass` (2026-11-07 00:39; người dùng: "bật wifi 6 và bỏ amfipass"): = build-46 + `itlwm_he=1`, AMFIPass tắt
- `itlwm_he`: laobamac `AirportItlwm/AirportItlwmV2.cpp:335` (7204c69) `PE_parse_boot_argn("itlwm_he")` == 1 → `IEEE80211_F_HEON`; chuỗi có trong binary Tahoe. README laobamac: HE tắt mặc định trên macOS 26, bật bằng `itlwm_he=1`.
- AMFIPass + `-amfipassbeta` chỉ phục vụ root patch OCLP (W4), máy không còn root patch; AMFI vẫn tắt bằng `amfi_get_out_of_my_way=1` (stack đồ hoạ cần). `AMFIPass.kext` Enabled=false (file giữ để lùi). JN không dùng AMFIPass.
- boot-args 163 → 160. plist_diff với build-46: 2 khác biệt. efi-validate 0/0 (validate-20261107T003905.md). Hai thay đổi trong một build theo yêu cầu người dùng; lỗi → build-46, rồi tách từng cái.
- Lỗi công cụ: `plist_edit.py bootarg-remove/bootarg-add --dry-run` GHI THẬT vào config (lần chạy thật sau đó báo "No change"/ERROR). Kết quả cuối vẫn đúng (kiểm bằng plist_diff). Cần sửa script.
- 2026-11-07T00:39:54 Xoá thủ công snapshot build-43-20261106-225429-gva-nopavp (người dùng duyệt; chỗ cho build-47)
- 2026-11-07T00:39:54 Created build-47-20261107-003954-wifi6-noamfipass (tree 0974eff308b3, ocvalidate: 0 errors, 0 warnings (validate-20261107T003905.md))
- 2026-11-07T00:39:57 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 3780be079449, verified)
- 2026-11-07T00:39 build-47 wifi6-noamfipass ghi lên MACEFI (/dev/sdb3, kiểm hash OK, SMBIOS thật).
- 2026-11-07T00:43 build-47 trên MÁY B: hoạt động (người dùng: "được rồi"). Người dùng sẽ chép EFI sang ESP ổ trong.
- 2026-11-07T00:49:05 plist_edit delete Kernel/Add[BundlePath=IO80211FamilyLegacy.kext/Contents/PlugIns/AirPortBrcmNIC.kext] (config.plist)
- 2026-11-07T00:49:05 plist_edit delete Kernel/Add[BundlePath=IO80211FamilyLegacy.kext] (config.plist)
- 2026-11-07T00:49:05 plist_edit delete Kernel/Add[BundlePath=IOSkywalkFamily.kext] (config.plist)
- 2026-11-07T00:49:05 plist_edit delete Kernel/Add[BundlePath=AMFIPass.kext] (config.plist)
- 2026-11-07T00:49:06 plist_edit delete Kernel/Block[Identifier=com.apple.iokit.IOSkywalkFamily] (config.plist)
- 2026-11-07T00:49:06 plist_edit delete Kernel/Add[BundlePath=IO80211FamilyLegacy.kext/Contents/PlugIns/AirPortBrcmNIC.kext] (config-install.plist)
- 2026-11-07T00:49:06 plist_edit delete Kernel/Add[BundlePath=IO80211FamilyLegacy.kext] (config-install.plist)
- 2026-11-07T00:49:06 plist_edit delete Kernel/Add[BundlePath=IOSkywalkFamily.kext] (config-install.plist)
- 2026-11-07T00:49:06 plist_edit delete Kernel/Add[BundlePath=AMFIPass.kext] (config-install.plist)
- 2026-11-07T00:49:06 plist_edit delete Kernel/Block[Identifier=com.apple.iokit.IOSkywalkFamily] (config-install.plist)
- 2026-11-07T00:49:06 plist_edit bootarg-remove -amfipassbeta (config-install.plist)
- 2026-11-07T00:51:18 Xoá thủ công snapshot build-44-20261106-232314-pavpctx (người dùng duyệt; chỗ cho build-48)

## Build 48 — `cleanup` (2026-11-07 00:49; người dùng: "dọn dẹp file rồi push"): = build-47, gỡ hẳn mục đã tắt
- `config.plist` + `config-install.plist`: xoá Kernel/Add `AMFIPass.kext`, `IOSkywalkFamily.kext`, `IO80211FamilyLegacy.kext` (+ plugin AirPortBrcmNIC), Kernel/Block `com.apple.iokit.IOSkywalkFamily`; `config-install.plist` bỏ `-amfipassbeta`. Xoá thư mục ba kext khỏi `EFI/OC/Kexts`. Lúc chạy giống build-47 (các mục đã Enabled=false). plist_diff với build-47: 5 mục xoá + đổi chỉ số (thứ tự tương đối giữ nguyên). efi-validate 0/0 (validate-20261107T004906.md); ocvalidate config-install: No issues.
- Sửa `plist_edit.py`: `bootarg-*` với từ bắt đầu bằng `-` chèn `--` trước từ đó nên `--dry-run`/`--file` phía sau thành tham số vị trí → dry-run ghi thật. Nay `--` + từ đặt cuối argv. Kiểm: 3 lệnh dry-run trên bản sao không đổi hash.
- build-48 ★ known-good (người dùng: "giữ build 48 known good"). USB và ESP hiện là build-47 (chạy giống hệt).
- 2026-11-07T00:51:18 Created build-48-20261107-005118-cleanup (tree e891efd83a8e, ocvalidate: 0 errors, 0 warnings (validate-20261107T004906.md))
- 2026-11-07T00:51:18 Marked build-48-20261107-005118-cleanup as known-good (user request)
- 2026-11-07T00:51 Marked build-48 known-good (người dùng).
- 2026-11-07T00:57 Đánh giá nullmoth/nvidia-macos-driver cho RTX 3050 Ti (người dùng hỏi): ghi DRIVER-MATRIX D1 (ỨNG VIÊN). Đính chính: trước đó Claude nói sai rằng Ampere chưa từng có driver macOS.
- 2026-11-07T01:06:19 plist_edit append to Kernel/Add: BundlePath=AMFIPass.kext (config.plist)
- 2026-11-07T01:06:19 plist_edit move Kernel/Add[BundlePath=AMFIPass.kext] to position 1 (config.plist)
- 2026-11-07T01:06:19 plist_edit set ACPI/Add[Path=SSDT-DGPU-OFF.aml]/Enabled = False (config.plist)
- 2026-11-07T01:06:19 plist_edit delete {DeviceProperties}/Add/{PciRoot(0x0)/Pci(0x1,0x0)/Pci(0x0,0x0)} (config.plist)
- 2026-11-07T01:06:19 plist_edit set NVRAM/Add/7C436110-AB2A-4BBB-A880-FE41995C9F82/csr-active-config = <data 530A0000> (config.plist)
- 2026-11-07T01:06:19 plist_edit set NVRAM/Add/7C436110-AB2A-4BBB-A880-FE41995C9F82/boot-args = '-ngreenpm -ngreentglwithgfx -allow3d -disablegfxfirmware -ngreenv189 -ngreenkeepefi -ngreenxefix -ngreenfixbootmode amfi_get_out_of_my_way=1 -amfipassbeta gfxrst=1 itlwm_he=1 nvfb=1 nvaccel=1 nvfbheads=4 -nvkmsnosmooth amfi=0x80 ipc_control_port_options=0' (config.plist)

## Branch `nvidia-gpu` (2026-11-07 01:05; người dùng: "tạo một build để thử nghiệm, đồng thời tạo branch làm việc khác liên quan tới nvidia-gpu")
- Worktree `.claude/worktrees/nvidia-gpu`, nhánh `nvidia-gpu` tách từ `bt-backlight-audio` @5f37564 (build-48). Symlink dùng chung: `_cache`, `snapshots`, `config/usb-mount.txt`, `docs/hw-dump`, `docs/MACHINE-ANALYSIS.md`. **Thiếu `secrets/smbios.json`** (Claude không được tạo) → người dùng tự tạo trước khi ghi USB.
- Đọc NullMoth v2.7.2 (clone `_cache/refs/nullmoth-nvidia` @18ba05f): LICENSE = **PolyForm Noncommercial 1.0.0**. `package/install.sh`: cài NVRM/NVAccel/NVRMFB/NVRMAGDC vào `/Library/Extensions`, bundle vào `/Library/GPUBundles`, firmware GSP `/Library/NullMoth/nvfw`; dựng lại Auxiliary KC từ toàn bộ `/Library/Extensions` (gồm TGL/HookCase/VoodooHDA); **trên macOS ≥ 26 tự thêm `NMXAudio.kext`** nếu có bộ điều khiển HDA (không có cờ tắt) → đụng VoodooHDA; `CHECK=1` chỉ dựng thử KC. Boot guard: tắt driver sau 2 lần khởi động không bật màn hình (máy muxless: rủi ro, CHƯA XÁC MINH). Cờ `nvfb/nvaccel/nvfbheads/-nvkmsnosmooth` đọc bằng `PE_parse_boot_argn`.

## Build 49 — `nvidia-try` (nhánh `nvidia-gpu`): = build-48 + điều kiện OpenCore của NullMoth
- `SSDT-DGPU-OFF.aml` Enabled=false; xoá DeviceProperties `PciRoot(0x0)/Pci(0x1,0x0)/Pci(0x0,0x0)` (`disable-gpu`); AMFIPass.kext (từ snapshot build-47) bật lại, đặt sau Lilu; `csr-active-config` 0x0A13 → **0x0A53** (chứa 0x0A43 theo README); boot-args 160 → **255**: `… amfi_get_out_of_my_way=1 -amfipassbeta gfxrst=1 itlwm_he=1 nvfb=1 nvaccel=1 nvfbheads=4 -nvkmsnosmooth amfi=0x80 ipc_control_port_options=0` (`-amfipassbeta` kết thúc ở 154 ≤ 228). SecureBootModel đã Disabled.
- plist_diff với build-48: 5 khác biệt. efi-validate 0/0 (validate-20261107T010620.md). Runbook: `docs/NVIDIA-RUNBOOK.md`.
- Bảo mật: SIP thêm 0x40 (CSR_ALLOW_UNRESTRICTED_NVRAM: ghi NVRAM không giới hạn), AMFI vẫn tắt + `amfi=0x80`. Lùi: build-48.
- 2026-11-07T01:08:59 Xoá thủ công snapshot build-46-20261107-003442-config-install-wifi (người dùng duyệt; chỗ cho build-49). Quy tắc mới (người dùng): được xoá snapshot known-good đã cũ hơn 5 bản so với build mới nhất.
- 2026-11-07T01:08:59 Created build-49-20261107-010859-nvidia-try (tree 347f3e5b4a67, ocvalidate: 0 errors, 0 warnings (validate-20261107T010620.md))
- 2026-11-07T01:12:37 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 3a0106f9c7a9, verified)
- 2026-11-07T01:12 build-49 nvidia-try ghi lên MACEFI (/dev/sdb3, kiểm hash OK, SMBIOS thật). ESP ổ trong vẫn build-47 (đường lui không cần USB).
- 2026-11-07 01:17 build-49 trên MÁY B (chưa cài NullMoth): **panic lúc boot** (`logs/Kernel-2026-11-07-011600.panic`, uptime 6,9 s, kernel_task): page fault **CR2 0xc78**, RAX/RDI = 0, trong `com.apple.iokit.IOAcceleratorFamily2` +0x39117 ← `com.xxxxx.driver.AppleIntelTGLGraphics` +0x7882 ← NootedGreen (kext v10, UUID E6C3625D) +0x16f23. → Cùng dấu hiệu panic cũ `IOAccelTask::release ← IGAccelTask::withOptions` (H3, GMSFIX sửa ở build-19). Không có driver NVIDIA → do **để dGPU sống** (bỏ SSDT-DGPU-OFF + `disable-gpu`), hoặc AMFIPass/SIP/boot-args mới (khó hơn).
- Giả thuyết (CHƯA XÁC MINH): (H1) dGPU bật làm đổi cách cấp phát vùng PCI (BAR lớn của dGPU) → aperture/GTT của iGPU khác → bộ quản lý bộ nhớ iGPU khởi tạo thất bại, triệu chứng giống GMS sai; (H2) GMSFIX không áp (`stolen_real_size` = 0) khi có 2 GPU. NootedGreen đọc GGC từ `devInfo->videoBuiltin` (kern_green.cpp:270) nên H2 ít khả năng.
- 2026-11-07T01:19:07 plist_edit set ACPI/Add[Path=SSDT-DGPU-OFF.aml]/Enabled = False (config.plist)
- 2026-11-07T01:19:07 plist_edit delete DeviceProperties/Add/{PciRoot(0x0)/Pci(0x1,0x0)/Pci(0x0,0x0)} (config.plist)
- 2026-11-07T01:19:07 plist_edit bootarg-add -v (config.plist)

## Build 50 — `dgpu-on-diag` (nhánh `nvidia-gpu`): = build-48 + chỉ để dGPU sống + `-v`
- Tách nguyên nhân panic build-49: `SSDT-DGPU-OFF.aml` Enabled=false, xoá `disable-gpu`; KHÔNG AMFIPass, SIP giữ 0x0A13, không cờ NullMoth. `-v` để chụp dòng `XeNG GMSFIX: GMS=… real=… patch=…` / `diag[1] … seg=…` trước panic. boot-args 162. plist_diff với build-48: 3 khác biệt. efi-validate 0/0 (validate-20261107T011908.md).
- Panic giống build-49 → do dGPU sống; không panic → do AMFIPass/SIP/cờ NullMoth.
- 2026-11-07T01:19:25 Xoá snapshot known-good build-26-20261105-193440-fencefix-restored theo quy tắc người dùng (known-good cũ hơn 5 bản; chỗ cho build-50)
- 2026-11-07T01:19:25 Created build-50-20261107-011925-dgpu-on-diag (tree 0cfe830a32e8, ocvalidate: 0 errors, 0 warnings (validate-20261107T011908.md))
- 2026-11-07T01:20:05 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree d4e40b1a279f, verified)
- 2026-11-07T01:20 build-50 dgpu-on-diag ghi lên MACEFI (/dev/sdb3, kiểm hash OK, SMBIOS thật).
- 2026-11-07 01:25 build-50 trên MÁY B: **panic giống hệt** build-49 (`logs/Kernel-2026-11-07-012310.panic`: CR2 0xc78, cùng địa chỉ `IOAcceleratorFamily2` +0x39117 ← TGL +0x7882; uptime 34 s do `-v`). → **Chỉ riêng việc để dGPU sống (bỏ SSDT-DGPU-OFF + `disable-gpu`) đã làm iGPU panic lúc khởi tạo**; AMFIPass/SIP/cờ NullMoth không liên quan. Driver NullMoth chưa từng được nạp.
- Video verbose (`logs/20261107_012132.mp4`, 720p): dòng `XeNG GMSFIX` không đọc được (chữ chồng do cuộn). Đọc được: AGPM "Key Does not Exist, use KSMCPStatesEGPU for External GPU" — macOS coi dGPU là GPU ngoài.
- Linux (`docs/hw-dump/lspci-nnvv.txt`, dGPU bật): iGPU BAR0 0x6102000000 (16M), BAR2 0x4000000000 (256M); dGPU BAR1 **4 GB, Resizable BAR đang bật** (hỗ trợ 64M–4G). BAR do firmware gán lúc POST (trước SSDT `_OFF`) → giả thuyết H1 (đổi layout PCI) yếu đi. Nguyên nhân thật: CHƯA XÁC MINH (có thể driver TGL đi nhánh "nhiều GPU / GPU ngoài").
- 2026-11-07 01:40 Video 4K build-50 (`logs/20261107_013000.mp4`, OCR + đọc tay):
  - t≈29 s: `XeNG GMSFIX: GMS=0xfe real=60 MB (Apple would use 8128 MB) patch=OK`, `XeNG PAVPFIX: patch=OK` → **H2 bác bỏ** (GMSFIX vẫn áp khi có dGPU).
  - t≈34 s (ngay trước panic): `XeNG GMSFIX diag[1]: fbreg=1 mm=<ptr> seg=0x3d95000 range=0x3d95000+0xc26b000` — **y hệt build-25 chạy tốt** (`fbreg=1`, seg 0x3D95000 sau cửa sổ FB; seg+size = 0x10000000 = aperture 256 MB) → vùng nhớ GPU của bộ tăng tốc đúng → **H1 bác bỏ**. Trước đó: `[IGPU] Forced to use Host Preemptive Scheduler`, `Multi-Context (Compute Command Streamer) Enabled`; sau đó HWCAPS.
  - → `IGAccelTask::withOptions` thất bại vì lý do khác (không phải stolen/aperture) chỉ khi dGPU sống. Tìm tiếp cần phân tích bên trong driver TGL của Apple (ngoài khả năng của dự án) → **hướng NVIDIA dừng ở đây**; còn: báo issue JN/NullMoth (#428 có máy chạy NootedGreen + dGPU).
- 2026-11-07 01:50 Đánh giá **watchthelight-labs/WTLIntelGfx** (XeGfx; người dùng hỏi; CLAUDE.md §0: "Không dùng WTLIntelGfx/XeGfx làm driver"). Clone `_cache/refs/wtlintelgfx` @ff64f83. README (2026-10-28/31): i915 (FreeBSD drm-kmod) chạy trong XNU + Mesa ANV + plugin Metal/accelerator fork từ NullMoth; **chạy** trên Arrow Lake 7D67 (Tahoe 26.7.1/26.7.2) và Meteor Lake (tester); **46A3: stage 1–3 qua (tester TrDiTu = người dùng), stage 4 panic PCH lookup — sửa ở 0.0.47; các stage sau cần GuC firmware riêng cho Alder Lake** (release chỉ link `mtl_guc_70.bin`). Thay thế NootedGreen (không chạy song song trên cùng iGPU). Release chỉ pre-release (0.0.45–0.0.47), "still a test driver", 1 panic mở (I-116). License hỗn hợp: shim BSD-2, plugin/accelerator PolyForm Noncommercial, translator LGPL-3.0. → **Không khả thi để dùng hằng ngày**; chỉ có thể tiếp tục vai trò tester (kext không tự nạp lúc boot, chạy theo stage bằng sysctl).
- 2026-11-07 01:55 Người dùng chỉ ra: NullMoth yêu cầu `gfxrst=4` khi có WhateverGreen (README:129, TROUBLESHOOTING:56 — panic `IOFramebuffer::postOpen`/`memcpy` khi màn hình NVIDIA mở), mâu thuẫn với `gfxrst=1` của JN/G4. Quyết định: nhánh chính giữ `gfxrst=1`; nhánh `nvidia-gpu` sẽ dùng `gfxrst=4`. Lưu ý: panic build-49/50 (CR2 0xc78 trong `IGAccelTask`, 7–34 s, chưa có driver NVIDIA) là lỗi khác, ở đường khởi tạo bộ tăng tốc iGPU, không phải panic `postOpen` này. Thêm: README NullMoth thử với SMBIOS có GPU rời (`iMacPro1,1`), dự án dùng `MacBookPro16,2`.
- 2026-11-09T23:41:10 plist_edit set DeviceProperties/Add/{PciRoot(0x0)/Pci(0x1,0x0)/Pci(0x0,0x0)}/disable-gpu = <data 01000000> (config.plist)
- 2026-11-09T23:41:30 Created build-51-20261109-234130-dgpu-powered-hidden (tree 56cd46e12be1, ocvalidate: 0 errors, 0 warnings (validate-20261109T234113.md))

## 2026-11-09 — nhánh `whateverxe-dual-gpu`: thử WhateverXe → không đạt; quay lại điều tra panic dGPU-sống với NootedGreen
- khucxtriendev @8714a85 chuyển sang WhateverXe + NullMoth. Kiểm định (DRIVER-MATRIX X1–X4): máy VCS2-only (`available engines: 41003`) → WhateverXe 0.8.0
  từ chối (issue #76, cùng 46A3: ProfileMismatch, ép thì treo cứng). Người dùng chọn hướng: giữ NootedGreen, điều tra panic build-49/50.
- Ký hiệu panic build-50 (kext v10 eb2d2843, `llvm-nm`): NootedGreen +0x16f23 = `Gen11::igAccelTaskWithOptions+0x73` (ngay sau khi gọi hàm gốc),
  +0x1fb04 = `Gen11::start+0x1f94`. Lỗi nằm trong `IGAccelTask::withOptions` gốc (TGL +0x7882 → IOAcceleratorFamily2 +0x39117, NULL+0xc78):
  task init thất bại rồi release (cùng chữ ký JN #13/#24, sgiammori #12 — các issue này dGPU tắt/không có, nghi `newAddressRangeAllocatorForTask` trả NULL).
  Không issue nào gắn chữ ký này với dGPU.
- NullMoth match dGPU theo `IOPCIClassMatch 0x03000000&0xff000000` → không thể dùng NullMoth nếu đổi `class-code` dGPU.
- build-49/50 đổi cùng lúc 2 thứ (SSDT-DGPU-OFF tắt + xoá `disable-gpu`). Tách: build-51 chỉ để dGPU có điện, vẫn `disable-gpu`.

## Build 51 — `dgpu-powered-hidden` (nhánh `whateverxe-dual-gpu`): = build-50 + `disable-gpu` lại
- So build-48: SSDT-DGPU-OFF Enabled=false, boot-args thêm `-v` (2 khác biệt). `disable-gpu` = <01000000> ở `PciRoot(0x0)/Pci(0x1,0x0)/Pci(0x0,0x0)` như build-48.
- Kết quả đọc: không panic → panic do dGPU **được IOKit/driver Apple nhìn thấy** (không phải do có điện); panic → do dGPU có điện (phần cứng/ACPI/PCIe).
- efi-validate 0/0 (validate-20261109T234113.md).
- 2026-11-09T23:41 Xoá snapshot known-good build-29-20261105-202412-blmax theo quy tắc người dùng (known-good cũ hơn 5 bản; chỗ cho build-51).
- 2026-11-09T23:41:30 Created build-51-20261109-234130-dgpu-powered-hidden. Chưa ghi USB (chờ người dùng).
- 2026-11-09T23:44:38 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree d75b3580ea22, verified)
- 2026-11-09 23:44 build-51 dgpu-powered-hidden ghi lên MACEFI (/dev/sdb3, tree d75b3580ea22, kiểm hash OK, SMBIOS thật). ESP ổ trong vẫn build-47.
- 2026-11-10 00:21 build-51 trên MÁY B: **boot vào desktop, không panic**, `Intel HD Graphics TGL CRB`, Metal 2. `ioreg`: dưới `PEG1` không còn thiết bị, không có `de10` → Lilu `disable-gpu` đã terminate dGPU khỏi IOKit (`DeviceInfo::processSwitchOff`, `requestTerminate`/`terminate`; không tắt điện). Đo nghỉ không dùng được (`mds_stores` 103 % CPU; `pkg_W` không gồm dGPU).
- → Panic build-49/50 do dGPU **hiện trong IOKit**, không do có điện. Nguyên nhân tìm được (đọc mã, CHƯA XÁC MINH runtime): NootedGreen `Gen11::injectAcceleratorPersonality` (kern_gen11.cpp, JN 24450b4) đăng ký `IntelAccelerator` chỉ với `IOPCIClassMatch 0x03000000&0xff000000`, không lọc vendor → khớp cả RTX 3050 Ti. Kext TGL gốc đã giới hạn `0x9a498086` (JN `install-macos.sh:22`).
- Patch **v12 XE-PCIMATCH** `patches/nootedgreen-v12-pcimatch.patch` (sha256 02a677ae…898b): thêm `IOPCIPrimaryMatch 0x00008086&0x0000ffff`. Áp được trên v10 và v11; syntax 0 lỗi, cảnh báo = v10. Hướng dẫn: GMSFIX-RUNBOOK §v12. Chờ người dùng build kext trên MÁY B → build-52.
- 2026-11-10T00:30:30 plist_edit delete DeviceProperties/Add/{PciRoot(0x0)/Pci(0x1,0x0)/Pci(0x0,0x0)} (config.plist)
- 2026-11-10T00:30:34 plist_edit set Kernel/Add[BundlePath=NootedGreen.kext]/Comment = 'NootedGreen JN 24450b4 + patch v10 + v11 (opt-in, tắt) + v12 XE-PCIMATCH (md5 24b8d331)' (config.plist)
- 2026-11-10T00:30:45 plist_edit set Kernel/Add[BundlePath=NootedGreen.kext]/Comment = 'NootedGreen JN 24450b4 + patch v10 + v11 (opt-in, off) + v12 XE-PCIMATCH (md5 24b8d331)' (config.plist)
- 2026-11-10T00:31:10 Created build-52-20261110-003110-v12-dgpu-visible (tree 545553b032bd, ocvalidate: 0 errors, 0 warnings (validate-20261110T003045.md))

## Build 52 — `v12-dgpu-visible` (nhánh `whateverxe-dual-gpu`): = build-50 + kext v12
- Kext do người dùng build trên MÁY B (cây v10 + v11 + v12): md5 `24b8d331fb10285a5f668cb62811303a`, sha256 `57133c462a59b9314e24502f88da14b430bcb0e2057fd43a54403e70d9bdafb2`;
  chuỗi `0x00008086&0x0000ffff` 1, `PAVPCTX` 1 (v11 chỉ chạy khi có `-ngreenpavpctx` — không có trong boot-args); Info.plist giống v10. Lưu `_cache/user-inputs/NootedGreen-v12-24b8d331.kext`.
- Config: xoá lại `disable-gpu` (dGPU sống và hiện trong IOKit), SSDT-DGPU-OFF tắt, `-v` → plist_diff với build-50: chỉ Comment. efi-validate 0/0 (validate-20261110T003045.md;
  lần đầu lỗi vì Comment có ký tự không phải ASCII — ocvalidate cấm).
- Kiểm: boot không panic; `ioreg -lw0 | grep -i de10` thấy NVIDIA; `ioreg -rc IntelAccelerator -d1 | grep -c '"IOClass"'` = 1. Panic → build-51.
- 2026-11-10T00:31 Xoá snapshot known-good build-31-20261105-205412-alc11 theo quy tắc người dùng (cũ hơn 5 bản; chỗ cho build-52).
- 2026-11-10T00:31:10 Created build-52-20261110-003110-v12-dgpu-visible. Chờ duyệt ghi USB.
- 2026-11-10T00:32:23 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree f3099e87a754, verified)
- 2026-11-10 00:32 build-52 v12-dgpu-visible ghi lên MACEFI (/dev/sdb3, tree f3099e87a754, kiểm hash OK, SMBIOS thật). ESP ổ trong vẫn build-47.
- 2026-11-10T00:45:40 plist_edit append to Kernel/Block: Identifier=com.apple.iokit.IONDRVSupport (config.plist)
- 2026-11-10T00:45:58 Created build-53-20261110-004558-block-ondrv (tree 36b902683268, ocvalidate: 0 errors, 0 warnings (validate-20261110T004540.md))
- 2026-11-10 00:33 build-52 trên MÁY B: **hết panic 0xc78** (`V501[1]: initWithOptions … ret=1`, `XeNG POOL[1] init`) → v12 sửa đúng chỗ. Treo ở verbose (Caps Lock chết) do panic mới
  (`logs/Kernel-2026-11-10-003901.panic` ở nhánh nvidia-gpu, uptime 37 s, **WindowServer**): page fault RIP 0 (gọi con trỏ hàm NULL) ← `AppleIntelTGLGraphicsFramebuffer` +0x54d3e ← `IOGraphicsFamily` +0x19f81/+0x10255.
- Log (`build52-boot.log`): dGPU được IOPCIFamily công bố (`1:0:0 (0x10de:0x25a0)`, HDA `0x10de:0x2291`); **`IONDRVFramebuffer` published** (chỉ ở build-52, không có ở boot build-47 cùng file)
  → framebuffer firmware của Apple gắn vào dGPU không driver; WindowServer gặp 2 framebuffer → panic trong FB TGL (cơ chế cụ thể CHƯA XÁC MINH). `Insufficient stolen memory` (FBMemMgr_Init) có ở cả hai boot → không liên quan.
- NullMoth README/HOW-IT-WORKS yêu cầu sẵn `Kernel → Block com.apple.iokit.IONDRVSupport Exclude` ("otherwise the firmware framebuffer takes display index 0").

## Build 53 — `block-ondrv` (nhánh `whateverxe-dual-gpu`): = build-52 + Block IONDRVSupport
- Một thay đổi: `Kernel/Block` thêm `com.apple.iokit.IONDRVSupport` Exclude. efi-validate 0/0 (validate-20261110T004540.md).
- Rủi ro: kext phụ thuộc IONDRVSupport không nạp (AGPM có — thấy trong `kextstat` build-51); FB TGL không phụ thuộc (panic build-52). Panic/không boot → build-51.
- 2026-11-10T00:46 Xoá snapshot known-good build-37-20261106-042417-hwpauto-on theo quy tắc người dùng (chỗ cho build-53).
- 2026-11-10T00:46:37 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree a3d50279bc38, verified)
- 2026-11-10 00:47 build-53 block-ondrv ghi lên MACEFI (/dev/sdb3, tree a3d50279bc38, kiểm hash OK, SMBIOS thật). ESP ổ trong vẫn build-47.
- 2026-11-10 00:48 build-53 trên MÁY B: **panic giống hệt build-52** (`Kernel-2026-11-10-004839.panic`, nhánh nvidia-gpu: WindowServer, RIP 0 ← FB TGL +0x54d3e ← IOGraphicsFamily +0x19f81/+0x10255, uptime 40 s).
  → Chặn IONDRVSupport không đổi gì (hoặc chưa có tác dụng — chưa có log kiểm). Kết luận chắc: dGPU hiện trong IOKit → FB TGL gọi con trỏ hàm NULL khi WindowServer mở FB.
  Bước tiếp: người dùng chép binary FB TGL + IOGraphicsFamily (KDK 25G241) để disassemble hai địa chỉ (chỉ phân tích trong `_cache/`, không phân phối) + `log show` build-53.
- 2026-11-10 01:0x Disassemble (binary người dùng chép từ MÁY B vào `_cache/user-inputs/b53/`, UUID khớp panic; chỉ phân tích, không phân phối):
  IOGraphicsFamily +0x10255 = `IOFramebuffer::newUserClient+0x187`, +0x19f81 = `IOFramebuffer::open+0x60b`; FB TGL +0x54d3e = `AppleIntelFramebuffer::enableController+0x1356`
  ngay sau `CallBackAGDC(4, fb)` → `callq *0x1c00(controller)` không kiểm NULL (RAX 0x90f = mặt nạ sự kiện, khớp panic). `+0x1c00` chỉ gán ở `RegisterAGDCCallback` (AGDP qua IntelFBClientControl).
  build-47: AGDP gắn 40 ms sau FB; build-52: không có AGDP/displaypolicyd trong 13 s sau FB → callback NULL. Log build-53 không lưu được lần boot panic.
- Patch **v13 XE-AGDCSTUB** `patches/nootedgreen-v12-to-v13-agdcstub.patch` (sha256 70adc2e3…179d): stub trả 0 khi callback trống ở enableController/validateDetailedTiming/setupDisplayTiming.
  Syntax 0 lỗi. GMSFIX-RUNBOOK §v13. Chờ người dùng build → build-54 (= build-53 + kext v13).
- 2026-11-10T01:07:34 plist_edit set Kernel/Add[BundlePath=NootedGreen.kext]/Comment = 'NootedGreen JN 24450b4 + patch v10 + v11 (opt-in, off) + v12 PCIMATCH + v13 AGDCSTUB (md5 58678f8b)' (config.plist)
- 2026-11-10T01:08:26 Created build-54-20261110-010825-agdcstub (tree 6fa16421fc42, ocvalidate: 0 errors, 0 warnings (validate-20261110T010734.md))

## Build 54 — `agdcstub` (nhánh `whateverxe-dual-gpu`): = build-53 + kext v13
- Kext người dùng build trên MÁY B (v10+v11+v12+v13): md5 `58678f8bb0bede716b074b590e0a7e14`, sha256 `5a5960e6ca1bc33ff3c81a5d07fdf7238209bc3b208ca0a998e5aeab6d0a164c`;
  chuỗi `XeNG AGDCSTUB` 3, PCIMATCH 1, PAVPCTX 1; Info.plist giống v10. (Lần build đầu md5 3497cdb1 thiếu v13 — patch chưa được áp; đã build lại.) Lưu `_cache/user-inputs/NootedGreen-v13-58678f8b.kext`.
- Config: chỉ đổi Comment so với build-53 (giữ Block IONDRVSupport, dGPU hiện, `-v`). efi-validate 0/0 (validate-20261110T010734.md).
- Kiểm: vào desktop; `log show --last boot | grep AGDCSTUB` (armed 1; "stub installed" nếu AGDP không gắn); de10 trong ioreg; IntelAccelerator = 1. Lỗi → build-51.
- 2026-11-10T01:07 Xoá snapshot known-good build-38-20261106-201328-jn24450b4-v9 theo quy tắc người dùng (chỗ cho build-54).
- 2026-11-10T01:09:08 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 8ce46b9312f2, verified)
- 2026-11-10 01:09 build-54 agdcstub ghi lên MACEFI (/dev/sdb3, kiểm hash OK, SMBIOS thật). ESP ổ trong vẫn build-47.
- 2026-11-10 01:11 build-54 trên MÁY B: **hết panic gọi NULL** (v13 có tác dụng), panic mới (`logs/Kernel-2026-11-10-011108.panic`, nhánh này; WindowServer, uptime 38 s): **divide error** ở
  `AppleIntelBaseController::setupPipeWatermarks+0xaa` ← `SetupParams` ← `hwSetMode` ← `AppleIntelFramebuffer::setDisplayMode` ← `IOFramebuffer::doSetDisplayMode` (WindowServer đặt mode).
  Số chia = `adjustPixelClockForWatermarks()/1e6` → pixel clock 0. Nguyên nhân: event 0xc ở `setupDisplayTiming` là `kAGDCRegisterLinkModesetCallback` — AGDC phải trả true + chỉ số link;
  stub trả 0 → "kAGDCRegisterLinkModesetCallback failed", hàm thoát sớm, cấu hình link không có → pixel clock 0. → **AGDP làm việc thật khi đặt mode; stub không thay được.**
  Cần tìm vì sao AppleGraphicsDevicePolicy không gắn vào IntelFBClientControl khi dGPU hiện. Xin AppleGraphicsControl.kext (KDK) + ioreg AGDP từ build-47.
- 2026-11-10T01:25:04 plist_edit delete Kernel/Add[BundlePath=NootedGreen.kext] (config.plist)
- 2026-11-10T01:25:04 plist_edit delete Kernel/Add[BundlePath=WhateverGreen.kext] (config.plist)
- 2026-11-10T01:25:04 plist_edit append to Kernel/Add: BundlePath=AMFIPass.kext (config.plist)
- 2026-11-10T01:25:04 plist_edit append to Kernel/Add: BundlePath=WhateverXe.kext (config.plist)
- 2026-11-10T01:25:09 plist_edit move Kernel/Add[BundlePath=AMFIPass.kext] to position 1 (config.plist)
- 2026-11-10T01:25:09 plist_edit move Kernel/Add[BundlePath=WhateverXe.kext] to position 5 (config.plist)
- 2026-11-10T01:25:19 plist_edit delete DeviceProperties/Add/{PciRoot(0x0)/Pci(0x2,0x0)} (config.plist)
- 2026-11-10T01:25:19 plist_edit set DeviceProperties/Add/{PciRoot(0x0)/Pci(0x2,0x0)}/framebuffer-patch-enable = <data 01000000> (config.plist)
- 2026-11-10T01:25:19 plist_edit set DeviceProperties/Add/{PciRoot(0x0)/Pci(0x2,0x0)}/framebuffer-stolenmem = <data 0000C003> (config.plist)
- 2026-11-10T01:25:19 plist_edit set DeviceProperties/Add/{PciRoot(0x0)/Pci(0x2,0x0)}/enable-max-pixel-clock-override = <data 01000000> (config.plist)
- 2026-11-10T01:25:19 plist_edit set DeviceProperties/Add/{PciRoot(0x0)/Pci(0x2,0x0)}/built-in = <data 00> (config.plist)
- 2026-11-10T01:25:19 plist_edit delete Kernel/Block[Identifier=com.apple.iokit.IONDRVSupport] (config.plist)
- 2026-11-10T01:25:19 plist_edit set NVRAM/Add/7C436110-AB2A-4BBB-A880-FE41995C9F82/boot-args = '-v keepsyms=1 debug=0x100 -allow3d -disablegfxfirmware -igfxdvmt amfi_get_out_of_my_way=0x1 amfi=0x80 ipc_control_port_options=0 nvfb=1 nvaccel=1 nvfbheads=4 -nvkmsnosmooth itlwm_he=1' (config.plist)
- 2026-11-10T01:25:19 plist_edit set NVRAM/Add/7C436110-AB2A-4BBB-A880-FE41995C9F82/csr-active-config = <data 530A0000> (config.plist)
- 2026-11-10T01:26:55 Created build-55-20261110-012655-wex-nullmoth (tree 0639135856ce, ocvalidate: 0 errors, 0 warnings (validate-20261110T012543.md))

## Build 55 — `wex-nullmoth` (nhánh `whateverxe-dual-gpu`): WhateverXe + NullMoth cho volume dự phòng
- Người dùng (2026-11-10 01:23): "hãy test WhateverXe + nullmoth trên volume dự phòng" — duyệt đưa X1 (WhateverXe 0.8.0) + X3 (AMFIPass 1.4.1 Mod) vào EFI để thử,
  dù DRIVER-MATRIX X1 = KHÔNG ĐẠT (dự kiến 46A3 VCS2-only bị từ chối như issue #76). Không HybridPM (X4, không release).
- release-fetch: WhateverXe-0.8.0-RELEASE.zip sha256 5B71E14C…8E4B (GitHub digest); AMFIPass-v1.4.1-Mod-RELEASE.zip @WhateverXe-Graphics 88d64a3 sha256 71F41DE4…6250 (khớp số repo công bố). SOURCES.md.
- Config (từ build-54): gỡ WhateverGreen + NootedGreen; thêm AMFIPass (sau Lilu) + WhateverXe (MinKernel 20.0.0); iGPU chỉ `framebuffer-patch-enable`, `framebuffer-stolenmem 0000C003`,
  `enable-max-pixel-clock-override`, `built-in` (không spoof); bỏ Block IONDRVSupport; SIP 0x0A53; boot-args 183 ký tự (WhateverXe + NullMoth + `-v keepsyms=1 debug=0x100`, `itlwm_he=1`).
  WhateverXe 0.8.0 không có `disable-agdc` (thuộc tính WhateverGreen); có `WEXDisplay13AGDCGuardReady` (tự bảo vệ CallBackAGDC). efi-validate 0/0 (validate-20261110T012543.md).
- 2026-11-10T01:26 Xoá snapshot known-good build-41-20261106-220946-v10-defaults theo quy tắc người dùng (chỗ cho build-55). Created build-55-20261110-012655-wex-nullmoth.
- Hướng dẫn MÁY B: `docs/WEX-NULLMOTH-RUNBOOK.md` (WhateverXe-Graphics 0.4.1 pkg sha256 7f7ce3b9…c02c, NullMoth v2.8.1 tar.gz sha256 1aa25a7f…5df8, cài trên volume dự phòng). Chờ duyệt ghi USB.
- 2026-11-10T01:29:11 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 2d03b2bba732, verified)
- 2026-11-10 01:29 build-55 wex-nullmoth ghi lên MACEFI (/dev/sdb3, kiểm hash OK, SMBIOS thật). Người dùng: volume dự phòng đã cài 26.7.1; có màn hình HDMI. ESP ổ trong vẫn build-47.
- 2026-11-10 01:35 MÁY B (volume dự phòng): WhateverXe-Graphics 0.4.1 cài OK (sha256 khớp). NullMoth 2.8.1 sha256 khớp; `install.sh` lần đầu (boot ổ trong build-47, dGPU tắt) dừng "STOP: no NVIDIA GPU found on PCI".
- 2026-11-10 01:37 boot USB build-55 → **vào desktop với dGPU hiện trong IOKit, không panic** (khác hướng NootedGreen); `install.sh` OK ("NVIDIA GPU present"), backup `/Library/NullMoth/backup-20261110-013738.TvFelH`.
  **Volume dự phòng chạy macOS 26.7.2** (không phải 25G241 như CLAUDE.md ghim; người dùng tưởng 26.7.1). WhateverXe (Tahoe ≥ 26.7) và NullMoth hỗ trợ; kết quả không so trực tiếp với volume chính. Chờ reboot + kiểm.
- 2026-11-10T01:52:32 plist_edit bootarg-add -nvrmnogo (config.plist)
- 2026-11-10T01:52:47 Created build-56-20261110-015247-nvrmnogo (tree d52ee23319ec, ocvalidate: 0 errors, 0 warnings (validate-20261110T015232.md))
- 2026-11-10 01:40 boot USB build-55 (sau khi cài NullMoth) trên volume dự phòng: **treo cứng** (Caps Lock chết, >5 phút; ảnh `logs/20261110_014012.jpg`). NVRM khởi động tốt: `RmInitAdapter succeeded`,
  `PASS 2 REACHED … GSP-RM is running`, GA107, VRAM 4096 MB, BAR1 4096 MB. NVRM-fb thấy HDMI (`connected 1 edid 384 B`), mode 1920x1080@60; dòng cuối `console range BEFORE allocating: 0x4000000000 ..`
  (= BAR2 iGPU → console boot trên panel iGPU). Theo mã NVRMFB (clone 18ba05f, có thể khác 2.8.1): ngay sau đó, vì fIndex 0, NVRMFB tắt console kernel (`kPEDisableScreen`) rồi cấp phát vùng scanout
  → verbose không hiện thêm → chưa biết điểm treo. HDMI có tín hiệu, đen. Không có panic log (treo cứng). Volume dự phòng boot bằng build-47 đứng ở logo (dự kiến); volume chính boot bình thường.
- `nvidia-macos-driver` repo nguồn chưa có tag v2.8.1 (clone_ref --ref v2.8.1 vẫn ở 18ba05f).

## Build 56 — `nvrmnogo`: = build-55 + `-nvrmnogo`
- NVRM nạp nhưng không tự `go(2)` (README: "idles until `nvrmctl go <pass>`"). Mục đích: (1) vào desktop trên iGPU/WhateverXe khi NullMoth có mặt, đọc trạng thái WEX + AGDP;
  (2) khởi động NVIDIA bằng tay để khoanh điểm treo. efi-validate 0/0 (validate-20261110T015232.md). boot-args 193 ký tự.
- 2026-11-10T01:53 Xoá snapshot known-good build-45-20261107-001333-wifi-laobamac theo quy tắc người dùng (chỗ cho build-56).
- 2026-11-10T01:53:25 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 9610b68e8781, verified)
- 2026-11-10 01:54 build-56 nvrmnogo ghi lên MACEFI (/dev/sdb3, kiểm hash OK, SMBIOS thật).
- 2026-11-10 01:56 build-56 trên MÁY B (volume dự phòng 26.7.2): **vào desktop**. iGPU: `Kernel Extension Info: No Kext Loaded`, VRAM 7 MB, `N97GTTopologyReady = No`, `N97NativePreflight = No`,
  `N97GTReadout` status 4 với fuse `0x000E00FB` → video mask 4 (VCS2-only) = **WhateverXe từ chối iGPU, đúng như issue #76** → panel không tăng tốc. dGPU RTX 3050 Ti hiện trong SPDisplays;
  NVRM/NVRMFB/NVAccel/NVRMAGDC 2.8.1 đã nạp, `nvrm-autogo = off (-nvrmnogo)`; AppleGraphicsDevicePolicy nạp; AMFIPass 1.4.1 + WhateverXe 0.8.0 nạp. `nvrmctl` không có trong gói.
- `tools/nvrm-go.c`: gọi NVRMUserClient selector 0 (`sGo`, 1 scalar = pass), như `nvrmctl go <pass>` (NVRM.cpp:1978, go() đòi root cho pass mới).
- 2026-11-10 02:0x Đọc fork khucxtriendev/WhateverXe @32228ed (clone `_cache/refs/khucxtriendev-wex`) và b00t0x/WhateverXe 0.8.0 @db438fd (`_cache/refs/b00t0x-wex`): bản vá của khucxtriendev
  (`THINKPAD_P1_GEN5_PATCH_GUIDE.md`, `whateverxe_thinkpad_p1_gen5.patch`) chỉ sửa hiển thị (GOP 6-bpc, bỏ lỗi Type-C khi có eDP, đọc thanh ghi pipe). Máy họ 46A6 96 EU có VCS0 → qua kiểm GT gốc.
  `decodeADLPGT` (`video!=1 && video!=5` → false) giống hệt trong fork và 0.8.0 → không ai sửa chỗ chặn 46A3 VCS2-only. Issue #76: ép nhận mask 4 → treo cứng khi accelerator start.
  Giả thuyết (CHƯA XÁC MINH): NootedGreen chạy được trên 46A3 VCS2-only vì XE-NOGVA ẩn giải mã phần cứng → driver Apple không dùng VCS0. Đề xuất: dừng WhateverXe cho iGPU; quay lại NootedGreen.
  Quan sát build-56: AppleGraphicsDevicePolicy có nạp khi NullMoth (NVRMAGDC) có mặt → thử NullMoth trên volume chính + build-54 (giả thuyết).
- 2026-11-10T02:05:54 plist_edit set Kernel/Add[BundlePath=NootedGreen.kext]/Enabled = False (config.plist)
- 2026-11-10T02:05:54 plist_edit delete DeviceProperties/Add/{PciRoot(0x0)/Pci(0x2,0x0)}/device-id (config.plist)
- 2026-11-10T02:05:54 plist_edit delete DeviceProperties/Add/{PciRoot(0x0)/Pci(0x2,0x0)}/AAPL,ig-platform-id (config.plist)
- 2026-11-10T02:05:54 plist_edit delete Kernel/Block[Identifier=com.apple.iokit.IONDRVSupport] (config.plist)
- 2026-11-10T02:06:22 plist_edit set NVRAM/Add/7C436110-AB2A-4BBB-A880-FE41995C9F82/boot-args = '-allow3d -disablegfxfirmware amfi_get_out_of_my_way=1 gfxrst=1 itlwm_he=1 -v' (config.plist)
- 2026-11-10T02:07:34 Created build-57-20261110-020734-nm-install (tree 4e78e1b5699a, ocvalidate: 0 errors, 0 warnings (validate-20261110T020622.md))
- 2026-11-10 02:02 build-56: `nvrm-go 1` → 0x0, `nvrm-go 2` → 0x0, **không treo** khi khởi động GPU bằng tay sau khi vào desktop → treo lúc boot gắn với auto-go sớm (console boot còn trên iGPU). Trạng thái HDMI sau go: chưa có.
- 2026-11-10 02:05 Người dùng: "quay lại NootedGreen với nullmoth trong volume chính". `install.sh` NullMoth bắt buộc thấy `vendor-id <de100000>` trên PCI (install.sh:146, không có cờ bỏ qua) →
  cần build cài đặt riêng: dGPU hiện nhưng không bật bộ tăng tốc TGL (tránh panic AGDP).

## Build 57 — `nm-install` (chỉ dùng một lần để cài NullMoth trên volume chính)
- Từ build-54: NootedGreen Enabled=false; xoá spoof iGPU (`device-id`, `AAPL,ig-platform-id`) → kext TGL (IOPCIPrimaryMatch 0x9a498086) không khớp → panel chạy framebuffer firmware;
  xoá Block IONDRVSupport (cần cho framebuffer firmware); boot-args bỏ cờ ngreen: `-allow3d -disablegfxfirmware amfi_get_out_of_my_way=1 gfxrst=1 itlwm_he=1 -v`. dGPU sống, hiện. efi-validate 0/0 (validate-20261110T020622.md).
- 2026-11-10T02:06 Xoá snapshot build-49-20261107-010859-nvidia-try (không known-good, thử nghiệm thất bại đã thay thế); giữ build-47 (known-good, trên ESP).
- 2026-11-10T02:08:00 plist_edit append to Kernel/Add: BundlePath=AMFIPass.kext (config.plist)
- 2026-11-10T02:08:00 plist_edit move Kernel/Add[BundlePath=AMFIPass.kext] to position 1 (config.plist)
- 2026-11-10T02:08:00 plist_edit set NVRAM/Add/7C436110-AB2A-4BBB-A880-FE41995C9F82/csr-active-config = <data 530A0000> (config.plist)
- 2026-11-10T02:08:00 plist_edit set NVRAM/Add/7C436110-AB2A-4BBB-A880-FE41995C9F82/boot-args = '-ngreenpm -ngreentglwithgfx -allow3d -disablegfxfirmware -ngreenv189 -ngreenkeepefi -ngreenxefix -ngreenfixbootmode amfi_get_out_of_my_way=1 gfxrst=4 itlwm_he=1 -v amfi=0x80 ipc_control_port_options=0 nvfb=1 nvaccel=1 nvfbheads=4 -nvkmsnosmooth -nvrmnogo' (config.plist)
- 2026-11-10T02:08:22 Created build-58-20261110-020822-ng-nullmoth (tree 6af66caed391, ocvalidate: 0 errors, 0 warnings (validate-20261110T020800.md))

## Build 58 — `ng-nullmoth`: = build-54 (NootedGreen v13, dGPU hiện, Block IONDRVSupport, `-v`) + điều kiện NullMoth
- AMFIPass 1.4.1 Mod sau Lilu (NullMoth README yêu cầu AMFIPass); SIP 0x0A53 (⊇ 0x0A43); boot-args thêm `amfi=0x80 ipc_control_port_options=0 nvfb=1 nvaccel=1 nvfbheads=4 -nvkmsnosmooth -nvrmnogo`,
  `gfxrst=1` → `gfxrst=4` (NullMoth README:129 khi có WhateverGreen). boot-args **254 ký tự**; cờ Lilu kết thúc ở 115 (< 228). efi-validate 0/0 (validate-20261110T020800.md).
- Câu hỏi: khi NullMoth có mặt (NVRMAGDC), AGDP có gắn vào framebuffer Intel không → hết panic chia 0 (build-54)? `-nvrmnogo` để tách: desktop trước, `nvrm-go 1/2` sau.
- 2026-11-10T02:08 Xoá snapshot build-50-20261107-011925-dgpu-on-diag (không known-good, đã thay thế). Created build-58. EFI dự án đưa về build-57 để ghi USB trước.
- 2026-11-10T02:09:45 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 9524f9eaaed5, verified)
- 2026-11-10 02:10 build-57 nm-install ghi lên MACEFI (/dev/sdb3, kiểm hash OK, SMBIOS thật). Dùng để cài NullMoth trên volume chính.
- 2026-11-10 02:13 MÁY B volume chính (26.7.1), boot USB build-57: `ioreg` de10 = 2 (GPU + HDA); NullMoth 2.8.1 `install.sh` OK ("NVIDIA GPU present"), backup `/Library/NullMoth/backup-20261110-021310.AbUevu`.
  NOTE của script: thiếu `nvfb=1`, `nvaccel=1`, `gfxrst=4` (đúng — build-57 không có; build-58 có).
- `NMXAudio.kext` (NullMoth tự cài trên macOS 26): `IOPCIClassMatch 0x04030000&0xffff0000`, không lọc vendor → tranh HDA Intel với VoodooHDA → chuyển sang `/Library/NullMoth/NMXAudio.kext.disabled`,
  dựng lại AuxKC theo lệnh kmutil của `uninstall.sh:71` ra file `.new`, kiểm NMXAudio = 0, rồi thay. AuxKC mới: NVRM, NVAccel, NVRMFB, NVRMAGDC 2.8.1, VoodooHDA 3.6.8, HookCase 8.0.1, AppleIntelTGLGraphics 16.0.2, AppleIntelTGLGraphicsFramebuffer 16.0.0.
- 2026-11-10T02:17:59 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 83ab0e6623bc, verified)
- 2026-11-10 02:18 build-58 ng-nullmoth ghi lên MACEFI (/dev/sdb3, kiểm hash OK, SMBIOS thật).
- 2026-11-10 02:20 build-58 trên MÁY B (volume chính): **panic giống build-54** (`logs/Kernel-2026-11-10-022221.panic`: WindowServer, divide error FB TGL +0x732a2 setupPipeWatermarks ← NootedGreen +0xd8fe, uptime 37,7 s).
  `logs/b58-boot.txt` không chứa lần boot build-58 (log mất do panic); các dòng từ 02:22:22 là boot build-47 sau đó: AGDP gắn vào IntelFBClientControl bình thường, NVRMAGDC nạp ("idle until sysctl debug.nvrmfb_agdc=1")
  → volume chính có NullMoth vẫn boot build-47 được. **Giả thuyết "NullMoth có mặt thì AGDP gắn" sai.**
- Tham khảo WhateverXe 0.8.0 (`kern_xe.cpp:8246-8288`, BSD-3, chỉ đọc ý tưởng): không giả lập AGDP; chặn `AppleIntelFramebuffer::newUserClient` type 0 bằng `kIOReturnNotReady` tới khi controller có callback AGDC
  (để WindowServer thử lại; tránh IOG đánh dấu FB chết khi enableController lỗi); `CallBackAGDC` trả NotReady cho thông báo khi chưa có receiver. Đề xuất v14 XE-AGDCWAIT (chẩn đoán): áp ý tưởng đó vào NootedGreen
  → không panic → SSH lấy ioreg AGDP/IntelFBClientControl/GPUWrangler khi dGPU hiện. Chờ người dùng chọn (v14 hay dừng, về build-48).

## Build 59 — `wex070-katana` (2026-11-10 16:45): = build-56 + WhateverXe 0.8.0 → **0.7.0-katana** (MỘT thay đổi: binary kext)
- Người dùng 16:44: "dựng efi đi, volume dự phòng hạ về 0.4.0". Kế hoạch: `docs/PLAN-wex-46a3.md`; log: `docs/wex-46a3/LOG.md` (thư mục chính).
- EFI = snapshot build-56 `nvrmnogo` (vào desktop trên volume dự phòng) chép nguyên; chỉ thay `WhateverXe.kext` bằng bản RELEASE
  tự build (fork `TrDiTu/WhateverXe` `katana-46a3`, CI run 42791539485, zip sha256 `536cd7dc…7ca8`, binary md5 `eb7bccb2`).
  Gồm patch issue #35 (VBT, eDP port mode 0, CDCLK nguội) + cờ opt-in `-wex-adlp-allow-vcs2` (KHÔNG bật trong build này).
- Config không đổi so với build-56: boot-args 193 (`-v keepsyms=1 debug=0x100 -allow3d -disablegfxfirmware -igfxdvmt …
  -nvrmnogo`), SIP 0x0A53, `framebuffer-stolenmem` 0000C003, SSDT-DGPU-OFF tắt, AMFIPass 1.4.1 Mod (blob giống tag v0.4.0).
- Dự kiến: `N97GTReadout` vẫn status 4 (máy VCS2-only). Mục đích lần này: xem patch #35 có cho `N97FBBootHandoff` Complete,
  panel 1920×1080 qua FB WEX không. Lần sau (build-60) mới thêm `-wex-adlp-allow-vcs2` — có thể treo cứng (#76).
- MÁY B: volume dự phòng hạ WhateverXe-Graphics 0.4.1 → **0.4.0** (`WhateverXe-Graphics-0.4.0.pkg`, sha256 `7a1b5015…9510`).
- efi-validate: 0 lỗi, 0 cảnh báo, ocvalidate chạy (`docs/validation/validate-20261110T164537.md`).
- 2026-11-10T16:45:59 Created build-59-20261110-164559-wex070-katana (tree 1f9baf291713, ocvalidate: docs/validation/validate-20261110T164537.md)
- 2026-11-10T16:45:59 Rotated out (deleted) oldest snapshot build-47-20261107-003954-wifi6-noamfipass
- 2026-11-10T16:56:45 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 345d7b0cc8ba, verified)
  USB MACEFI (`/dev/sdb3`) ghi build-59 lúc 16:56 (tree 345d7b0cc8ba, md5 kext khớp `eb7bccb2`).
- 2026-11-10T17:01:28 plist_edit bootarg-add -wex-adlp-allow-vcs2 (config.plist)

## Build 60 — `vcs2` (2026-11-10 17:01): = build-59 + boot-arg `-wex-adlp-allow-vcs2` (MỘT thay đổi; người dùng duyệt 17:01)
- Lý do: build-59 dừng ở `N97GTReadout` status 4 (fuse `0x000E00FB`, chỉ VCS2) → FB/accelerator WEX không khởi động
  (`docs/wex-46a3/LOG.md` 16:59). Cờ cho `decodeADLPGT` nhận video mask 4. Rủi ro: issue #76 báo treo cứng khi ép.
- boot-args 214 ký tự (< 228). efi-validate 0/0 (`docs/validation/validate-20261110T170128.md`).
- MÁY B: volume dự phòng đã hạ WhateverXe-Graphics về 0.4.0 (17:00).
- 2026-11-10T17:04:35 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree a8b171194850, verified)
- USB MACEFI (`/dev/sdb3`) ghi build-60 lúc 17:03 (tree a8b171194850). Snapshot build-60 CHƯA tạo: xoay vòng chạm build-48 known-good, chờ người dùng chọn xoá build-51 hay build-48.

## Build 61 — `wex-r2-vbtpanel` (2026-11-10 17:26): = build-60 + WhateverXe 0.7.0-katana **r2** (MỘT thay đổi: binary kext; người dùng duyệt 17:25)
- r2 (fork `katana-46a3`, CI run 42797617881, zip sha256 `a5e0910e…fdbd`, binary md5 `6616a629`): sửa đọc VBT panel —
  chọn eDP DDI A khi VBT khai báo eDP ở A và B; nhận `panel_type` 0xFF như loại 0 khi 16 mục đồng nhất. Nguyên nhân và kiểm offline:
  `docs/wex-46a3/LOG.md` 17:10–17:25 (thư mục chính). Mục tiêu: `WEXDisplay13BootReady`=Yes, FB TGL khởi động.
- Boot-args giữ nguyên build-60 (214 ký tự, có `-wex-adlp-allow-vcs2`). efi-validate 0/0 (`docs/validation/validate-20261110T172623.md`).
- Snapshot: người dùng xoá build-51 (không known-good) để giữ build-48 known-good. Bộ đếm snapshot đặt tên `build-60-20261110-172633-wex-r2-vbtpanel` (= build-61 trong log này) vì build-60 `vcs2` chưa từng snapshot; build-60 `vcs2` = build-59 snapshot + boot-arg `-wex-adlp-allow-vcs2`.
- 2026-11-10T17:26:33 Created build-60-20261110-172633-wex-r2-vbtpanel (tree e71333c674d6, ocvalidate: docs/validation/validate-20261110T172623.md)
- 2026-11-10T17:30:03 Created build-61-20261110-173003-usb-before-deploy (tree 35d4e46f8b86, ocvalidate: n/a (existing USB content))
- 2026-11-10T17:30:03 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 81a890490df6, verified)
- Người dùng xoá thêm build-52 (17:28). Ghi USB MACEFI (`/dev/sdb3`) 17:30, hash khớp (tree 81a890490df6, kext md5 `6616a629`). Sao lưu USB cũ (build-60 `vcs2`) thành snapshot `build-61-20261110-173003-usb-before-deploy` (serial đã gỡ). Lưu ý tên: snapshot `build-60-…-wex-r2-vbtpanel` = build-61 (r2); snapshot `build-61-…-usb-before-deploy` = build-60 `vcs2`.

## Build 62 — `wex-r3-pavp` (2026-11-10 17:52): = build-61 + WhateverXe 0.7.0-katana **r3** (MỘT thay đổi: binary kext; người dùng duyệt 17:52)
- Lý do: build-61 panic `PAVPCommandCallback+0x177` CR2 0xb8 trong `startGraphicsEngine` (`logs/b61/Kernel-2026-11-10-173420.panic`).
- r3 (CI run 42800957857, zip sha256 `fa7561a2…0c86`, binary md5 `ef097eaf`): `je`→`jmp` sang nhánh "PAVP tắt" trong
  `PAVPCommandCallback` (kiểm mẫu đúng 1 lần; ioreg `WEXPAVPDisabledPath`). Mất phát video DRM phần cứng (như PAVPFIX của NootedGreen).
- Boot-args giữ nguyên (214, có `-wex-adlp-allow-vcs2`). efi-validate 0/0 (`docs/validation/validate-20261110T175213.md`).
- Người dùng xoá snapshot build-53, build-54 (không known-good) để có chỗ.
- 2026-11-10T17:52:23 Created build-62-20261110-175223-wex-r3-pavp (tree b135c31fea33, ocvalidate: docs/validation/validate-20261110T175213.md)
- 2026-11-10T17:53:13 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 5e58af37b14f, verified)
- Ghi USB MACEFI (`/dev/sdb3`) 17:53, hash khớp (tree 5e58af37b14f, kext md5 `ef097eaf`); bản cũ trên USB trùng snapshot build-60-…-wex-r2-vbtpanel → không sao lưu thêm.

## Build 63 — `wex-r4-novideo` (2026-11-10 18:19): = build-62 + WhateverXe 0.7.0-katana **r4** (MỘT thay đổi: binary kext; người dùng duyệt 18:19)
- Lý do: build-62 đã tăng tốc (FB TGL + IntelAccelerator + Metal, VRAM 1536 MB) nhưng panic `VTDecoderXPCService` NULL+0x284
  khi mở System Settings (`logs/b62/`). r4 (CI run 42804853728, zip sha256 `8e83c589…f7ff`, binary md5 `4b8b18b7`): VCS2-only →
  không giải mã/mã hoá video phần cứng (`WEXHardwareVideoDisabled`). Nghiên cứu VCS2: ROADMAP G5.
- Boot-args giữ nguyên (214). efi-validate 0/0 (`docs/validation/validate-20261110T181928.md`).
- 2026-11-10T18:19:46 Created build-63-20261110-181946-wex-r4-novideo (tree e20580747647, ocvalidate: docs/validation/validate-20261110T181928.md)
- 2026-11-10T18:21:02 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 848cfcbae83d, verified)
- Ghi USB MACEFI (`/dev/sdb3`) 18:20, hash khớp (tree 848cfcbae83d, kext md5 `4b8b18b7`).
- 2026-11-10 18:32 Người dùng: build-63 ổn (System Settings, YouTube không panic) → **★ known-good**. build-48 vẫn known-good, KHÔNG được xoá (người dùng: bản ổn định nhất).

## Build 64 — `wex-r5-vcs2media` (2026-11-10 18:45): = build-63 ★ + WhateverXe 0.7.0-katana **r5** (MỘT thay đổi: binary kext; người dùng duyệt 18:32)
- r5 (CI run 42808459666, zip sha256 `d5d30e1b…fc9`, binary md5 `f9a7f64a`): vá params VideoMedia của AppleIntelTGLGraphics sang VCS2
  (type 4 / instance 2) → thử giải mã video phần cứng (ROADMAP G5). ioreg `WEXVCS2Media`, `WEXHardwareVideoDisabled`.
- Rủi ro: treo GPU/panic khi phát video. Đường lui: build-63 ★.
- Boot-args giữ nguyên (214). efi-validate 0/0 (`docs/validation/validate-20261110T184213.md`).
- Người dùng xoá snapshot build-55 (18:44).
- 2026-11-10T18:46:10 Created build-64-20261110-184610-wex-r5-vcs2media (tree de60a622ad77, ocvalidate: docs/validation/validate-20261110T184213.md)
- 2026-11-10T18:48:11 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 53ebf5c35329, verified)
- Ghi USB MACEFI (`/dev/sdb3`) 18:47, hash khớp (tree 53ebf5c35329, kext md5 `f9a7f64a`).

## Build 65 — `wex-r6-vcsdiag` (2026-11-10 19:15): = build-64 + WhateverXe 0.7.0-katana **r6** (MỘT thay đổi: binary kext; người dùng: "tiếp tục G5")
- r6 (CI run 42813262332, zip sha256 `d06c4996…f235`, binary md5 `ce67501b`): r5 + bộ đếm chẩn đoán (chỉ đọc) cho ngắt/hoàn tất VCS
  (ioreg `WEXVCSDiag`, `WEXVCSDiagRouted`). Mục tiêu: biết vì sao giải mã VCS2 ~1 s/khung.
- Boot-args giữ nguyên (214). efi-validate 0/0 (`docs/validation/validate-20261110T191852.md`).
- 2026-11-10T19:19:54 Created build-65-20261110-191954-wex-r6-vcsdiag (tree 446262cf2284, ocvalidate: docs/validation/validate-20261110T191852.md)
- 2026-11-10T19:19:55 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 705a8142e3b3, verified)
- Người dùng xoá snapshot build-56 (19:19). Snapshot build-65; ghi USB MACEFI (`/dev/sdb3`) 19:20, hash khớp (tree 705a8142e3b3, kext md5 `ce67501b`).

## Build 66 — `wex-r7-vcsirq` (2026-11-10 20:25): = build-65 + WhateverXe 0.7.0-katana **r7** (MỘT thay đổi: binary kext; người dùng duyệt 19:27)
- r7 (CI run 42816038634, zip sha256 xem `kexts-custom/WhateverXe-0.7.0-katana-r7/SOURCE.md`, binary md5 `cb4403c2`): thay
  `IGInterruptBridge::readAndClearVCSInterrupts` trên máy VCS2-only bằng hàm kiểu i915 (chọn đúng engine, chờ identity ~100 µs).
  Lý do: build-65 đo được ngắt VCS2 tới nhưng driver gốc không nhận → giải mã ~1 s/khung. Bộ đếm `WEXVCSDiag` mở rộng.
- Rủi ro: hàm chạy trong đường ngắt GPU → treo/panic. Lùi: build-63 ★. Boot-args giữ nguyên (214).
- Người dùng xoá snapshot build-57 (19:27). efi-validate 0/0 (`docs/validation/validate-20261110T202439.md`).
- 2026-11-10T20:24:53 Created build-66-20261110-202453-wex-r7-vcsirq (tree 007bedb3f761, ocvalidate: docs/validation/validate-20261110T202439.md)
- 2026-11-10T20:26:00 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree e5e76b951987, verified)
- Ghi USB MACEFI (`/dev/sdb3`) 20:25, hash khớp, kext md5 `cb4403c2`.
- 2026-11-10 20:29 Test MÁY B: giải mã H.264 phần cứng qua VCS2 chạy (3 ms/khung, 0 bỏ) — `logs/b66/b66-diag.txt`.
- 2026-11-10T21:06:02 plist_edit append to Kernel/Add: BundlePath=HybridPM.kext (config.plist)
- 2026-11-10T21:06:02 plist_edit move Kernel/Add[BundlePath=HybridPM.kext] to position 1 (config.plist)

## Build 67 — `hybridpm` (2026-11-10 21:06): = build-66 + **HybridPM 1.0.0** (MỘT thay đổi: thêm kext; người dùng duyệt 21:03)
- Lý do: build-66 GB7 CPU 999/4658, xung nhân max 3673 MHz (turbo bị XCPM giới hạn; NootedGreen sửa bằng XE-PM nhưng WEX không có).
- HybridPM (DRIVER-MATRIX X4; TSNPL 1.0; tự build @23c4537, binary sha256 `9f65958f…`) thêm ở Kernel/Add vị trí 1 (sau Lilu).
  Mặc định áp profile ở 20 s/60 s; hook XCPM kiểm byte trên 25G332. Không thêm boot-arg (214). Không có HWPAUTO như patch v8.
- Rủi ro: panic/treo do hook XCPM hoặc ghi MSR. Lùi: build-66 (snapshot) / build-63 ★. efi-validate 0/0 (`docs/validation/validate-20261110T210602.md`).
- 2026-11-10T21:08:22 Created build-67-20261110-210822-hybridpm (tree 12a921f89065, ocvalidate: pass)
- 2026-11-10T21:08:37 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree cd1e12556742, verified)
- 2026-11-10T21:09 Snapshot build-58 `ng-nullmoth` đã xoá (người dùng duyệt) để chừa chỗ build-67. build-67 ghi USB `/dev/sdb3` MACEFI, tree cd1e12556742, hash khớp.
- 2026-11-10T21:20 build-67 test (`logs/b67/`): HybridPM áp profile (hwp=1, epp=96, eet_off=1, cst=1, route=1). powermetrics GB7 CPU so với build-66: xung từng nhân tối đa 3673 → **4615 MHz** (p95 4540), xung TB hệ thống lúc tải 1805 → 2348 MHz (max 3083 → 4332), công suất gói lúc tải TB 33.7 → 31.8 W (max 57.8 → 62.6 W), nhiệt Nominal. Turbo CPU đã chạy. Điểm GB7 build-67: **1176 single / 4888 multi** (build-66: 999 / 4658; +17.7% / +4.9%).
- 2026-11-10T21:25 Người dùng xác nhận PL1 thực của máy = 45 W (Intel: base 45 W, max turbo 115 W, min assured 35 W). Khớp b67: tải đa nhân TB 49.9 W. Chưa biết 45 W nằm ở MSR 0x610 hay MCHBAR 0x59A0 (HybridPM `hpmpl1` chỉ ghi MCHBAR, tối đa 64 W).
- 2026-11-10T21:26:32 plist_edit bootarg-add NVRAM/Add/7C436110-AB2A-4BBB-A880-FE41995C9F82/boot-args (config.plist)
- 2026-11-10T21:26:43 plist_edit bootarg-remove NVRAM/Add/7C436110-AB2A-4BBB-A880-FE41995C9F82/boot-args (config.plist)
- 2026-11-10T21:26:43 plist_edit bootarg-add hpmpl1=55 (config.plist)
- 2026-11-10T21:27 **build-68 `hpmpl1-55`** = build-67 + boot-arg `hpmpl1=55` (HybridPM ghi PL1 55 W vào MCHBAR 0x59A0; thử xem PL1 45 W của HP nằm ở MCHBAR hay MSR 0x610). Boot-args 224 ký tự. validate 0/0 (`docs/validation/validate-20261110T212648.md`). Snapshot chờ người dùng chọn bản xoá (đủ 10). Lưu ý: lần chạy bootarg-add đầu sai cú pháp (chèn chuỗi path), đã gỡ ngay — config cuối đúng.
- 2026-11-10T21:28:00 Created build-68-20261110-212800-hpmpl1-55 (tree 584477bf57eb, ocvalidate: pass)
- 2026-11-10T21:28:10 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree dd03ee0759a7, verified)
- 2026-11-10T21:28 Snapshot build-59 đã xoá (người dùng duyệt); snapshot build-68 tạo; build-68 ghi USB /dev/sdb3 MACEFI, hash khớp. Chờ `logs/b68/`.
- 2026-11-10T21:31 build-68: `pl1_w 55`, `pl1_set 440` (= 55 W × 8) — MCHBAR không khoá, đã ghi 55 W. Chờ GB7 + powermetrics xem MSR 0x610 có giữ 45 W không.
- 2026-11-10T21:36 So với volume chính (build-37/48, NootedGreen XE-PM: GB7 2030/9646, PERFORMANCE.md): volume dự phòng thiếu 2 thứ đã đo là quyết định — XE-HWPAUTO (HWP desired=0; 1191/5637 → 2030/9646) và tắt C8/C10 (multi +22 %). HybridPM 1.0.0 không có HWPAUTO và mặc định cst=1. PL1 45 W không phải nút thắt chính (build-33 gói lên 73 W lúc GB7). Đề xuất: thử `sysctl -w debug.hybridpm.cst=0`; sau đó port HWPAUTO vào fork HybridPM.
- 2026-11-10T21:40 **build-69 `hwpauto`** = build-68 + HybridPM fork `victus` @6ddb23d (thêm XE-HWPAUTO từ patch v8: xoá HWP desired, mặc định BẬT vì boot-args 224/228; tắt bằng `hpmauto=0` / `sysctl debug.hybridpm.hwpauto=0`). CI run 42836259880, binary sha256 c6067942…2baa. Người dùng duyệt ("thêm HWPAUTO đi"). validate 0/0 (`docs/validation/validate-20261110T214027.md`). Snapshot chờ chọn bản xoá.
- 2026-11-10T21:43:36 Created build-69-20261110-214336-hwpauto (tree 8da95b473db2, ocvalidate: pass)
- 2026-11-10T21:44:06 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree 0fd9aac92026, verified)
- 2026-11-10T21:43 Snapshot build-60 đã xoá (người dùng duyệt); snapshot build-69 tạo; build-69 ghi USB /dev/sdb3 MACEFI, hash khớp. Chờ `logs/b69/`.
- 2026-11-10T21:52 build-69: người dùng báo "đã ổn" (CPU), không gửi log/điểm. Tiếp: GB7 GPU treo ở Recognition (b66).
- 2026-11-10T22:00 Phân tích GB7 GPU treo (build-66, `logs/b66/`): powermetrics GPU Active 100 % liên tục từ 20:52:46 (sau pha ~70–80 %), watchdog WindowServer 20:53:45 ("Display … not ready … GPU Busy: SurfaceID 9/3"), lần 2 lúc 20:54:25, GPU vẫn 100 % → GPU treo cứng, khôi phục không thành. Spindump: `IGAccelEventMachine` ở `IGAccelEventMachine::eventTimeout(int)+0x70` → `IGScheduler5::checkForProgress(IGHwCsType)+0xa4` (TGL BA3AA1C0); geekbench_avx2 chờ Metal. Cùng chữ ký WEX issue #44 (TGL-H, cùng offset) và #40; #25 (ADL-N, WEX 0.7.0 + Graphics 0.4.0): Geekbench Metal treo CCS, reset không khôi phục — chưa có bản sửa upstream. Volume chính (NootedGreen) chạy hết GB7 GPU (1094). Chưa loại trừ r5–r7 (VCS2/ngắt) — đề xuất chạy GB7 GPU trên build-63 ★ (không có r5–r7) + thu `ioreg -l | grep TGLRecovery` và `*.gpuRestart`.
- 2026-11-10T22:05 Người dùng: bỏ qua GB7 Metal; cài Vulkan + sửa NVIDIA. Hiện trạng NVIDIA (volume dự phòng, NullMoth 2.8.1): auto-go lúc boot → treo cứng (build-55, không có panic log); `-nvrmnogo` + `nvrm-go 1/2` tay → không treo (build-56), HDMI chưa kiểm. NullMoth v2.9 (2026-11-10) có sửa cho laptop lai panel trên iGPU (#516), GSP kẹt, mode set lỗi lúc boot; có `nmhybrid` (thử nghiệm, tắt mặc định). Viết `docs/NVIDIA-VULKAN-STEPS.md`: A Vulkan SDK, B cập nhật 2.9 (tắt lại NMXAudio), C `nvrm-go` tay trên build-69. Chờ `logs/b70/`.
- 2026-11-10T22:16 MÁY B volume dự phòng: NullMoth cập nhật 2.9 xong — kextstat: NVRMFB/NVRMAGDC/NVRM/NVAccel (2.9), VoodooHDA 3.6.8, không có NMXAudio. Tiếp: `nvrm-go 1/2` tay (build-69, `-nvrmnogo`).
- 2026-11-10T22:20 build-69 + NullMoth 2.9, sau `nvrm-go` tay: SPDisplays có 2 GPU — Intel UHD 46a3 Metal 2 (panel trong 1920×1080 @144 Hz, Main), **NVIDIA RTX 3050 Ti 25a0 Metal 4**, VRAM 4 GB, PCIe x8; không treo/panic. Dưới NVIDIA không có màn hình nào (HDMI: chưa biết có cắm không).
- 2026-11-10T22:27 `logs/b70/` (build-69 + NullMoth 2.9): **Vulkan OK** — SDK 1.4.363.1, MoltenVK 1.4.2, GPU `Intel(R) TGL Unknown` (lỗi nạp `libvulkan_kosmickrisp.dylib` arm64: vô hại; vulkaninfo chụp trước `nvrm-go` nên chưa có NVIDIA). NVIDIA sau `nvrm-go` tay (22:19–22:20): NVRMFB thấy HDMI (dpy 0x100, connector 0x1), `head 0 lit again -> ok 1 rc 0`, `first accepted primary flip on head 0`, nhưng `fb0 connect notify: nothing registered yet` ×2 → framebuffer xuất hiện sau khi WindowServer đã chạy, không ai nhận → SPDisplays không có màn hình dưới NVIDIA, HDMI không có desktop. Boot kế (22:23, `-nvrmnogo`, không go): `heads_published 0`; `boot guard: start 1 without a display so far (the driver turns itself off after 2)`; NVAccel headless check 60 s → "MetalPluginName restored WITHOUT arming". Kết luận: HDMI cần auto-go lúc boot → đề xuất build-70 bỏ `-nvrmnogo` (chờ duyệt). Backup NullMoth: `/Library/NullMoth/backup-20261110-221213.xsyZF3`.
- 2026-11-10T22:28:06 plist_edit bootarg-remove -nvrmnogo (config.plist)
- 2026-11-10T22:28:06 Created build-70-20261110-222806-nvrm-autogo (tree bb8744300fdb, ocvalidate: pass)
- 2026-11-10T22:28:20 Deployed EFI to /run/media/cyra/MACEFI/EFI (tree af6cb8084147, verified)
- 2026-11-10T22:28 **build-70 `nvrm-autogo`** = build-69 bỏ `-nvrmnogo` (NullMoth 2.9 tự go(2) lúc boot, để NVRMFB có trước WindowServer → HDMI). Người dùng duyệt. boot-args 214 ký tự. validate 0/0 (`docs/validation/validate-20261110T222806.md`). Snapshot build-61 đã xoá (người dùng duyệt); snapshot build-70 tạo; ghi USB /dev/sdb3 MACEFI, hash khớp. Rủi ro: 2.8.1 auto-go treo cứng (build-55). Lùi: build-69. Chờ `logs/b71/`.
- 2026-11-10T22:32 build-70 trên MÁY B: boot OK, **không treo** (auto-go 2.9), panel trong bình thường, âm thanh bình thường, **HDMI không có hình**. Chờ `logs/b71/` để biết lý do (boot guard / headless check / mode set).
- 2026-11-10T22:36 `logs/b71/` (build-70, NullMoth 2.9, auto-go): NVRM `auto-go: go(2) -> 0x0`, `PASS 2 REACHED`, 4 nub NVRMDisplay published; nhưng **NVRMFB và NVAccel không chạy** sau khi claim (không có dòng `NVRM-fb`, không có sysctl `debug.nvaccel_*`/`nvrmfb_*`, SPDisplays NVIDIA "Metal 2" thay vì Metal 4); `auto-go: heads published mask 0x0 … after 20 s`, `accelerator level 1 NEVER took after 11 tries`, `nvrm-display = heads 0x0 accel 0 agdc -99 k5 -99 iop -99`, `boot hold RELEASED (display PARTIAL)`. Đầu boot: `boot guard: start 2 without a display so far (the driver turns itself off after 2)`. Nguồn 2.7.2 (`kexts/NVRM/nvrm_off.h`): NVRAM `nullmoth-nv-starts` đếm số lần start chưa bật được màn hình; đủ 2 → driver tắt như `-nvoff`. Hai lần đếm: boot 22:23 (`-nvrmnogo`, không go) và 22:29. Giả thuyết (khớp log, CHƯA XÁC MINH trên 2.9): bộ đếm = 2 làm NVRMFB/NVAccel tắt ngay trong boot này. Thử: xoá `nullmoth-nv-starts`, boot lại build-70.
- 2026-11-10T22:48 **build-70 hoạt động** (người dùng: "hoạt động rồi") sau khi xoá NVRAM `nullmoth-nv-starts` và boot lại: HDMI có hình qua NullMoth 2.9. Chưa có `logs/b72/` trên MÁY A → chi tiết (Metal 4, heads) CHƯA XÁC MINH bằng log. Người dùng yêu cầu cập nhật tài liệu và push. Không commit: `logs/b54/AppleGraphicsControl.kext` (binary Apple), `EFI/OC/Kexts/AMFIPass.kext` (không có giấy phép phân phối).
- 2026-11-10T23:55 README viết lại toàn bộ cho nhánh WhateverXe (build-70); `docs/ROADMAP.md` đổi sang hướng WEX (W1–W13), roadmap JN cũ chuyển thành `docs/ROADMAP-JN.md` (người dùng yêu cầu).
- 2026-11-11T00:54 Người dùng báo (không có log trên MÁY A): HybridPM fork @6ddb23d (XE-HWPAUTO) → **GB7 CPU 2035 / 9320** (trước HWPAUTO 1176 / 4888; không HybridPM 999 / 4658; NootedGreen XE-PM build-37 2030 / 9646; Linux 2195 / 10101 → 93 % / 92 %). **GB7 OpenCL trên iGPU: 7598** (stack NootedGreen trước đây không có OpenCL trên iGPU; GB7 Metal vẫn treo ở Recognition). Volume dự phòng từ nay là volume duy nhất (người dùng 00:46); nhánh WEX đã gộp vào `main`; nhánh `bt-backlight-audio` đổi tên `jn-driver` (= build-48).
- 2026-11-11T14:11:49 plist_edit set PlatformInfo/Generic/ProcessorType = 3841 (config.plist)
