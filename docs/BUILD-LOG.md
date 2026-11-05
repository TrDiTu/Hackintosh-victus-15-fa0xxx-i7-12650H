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
