# DRIVER-MATRIX — HP Victus 15-fa0xxx (board 8A4F), macOS 26.7.1 (25G241), Giai đoạn A (EFI nền)

- Lập: 2026-11-02 (Pha 1, `driver-vetting`). **Người dùng duyệt thêm 2026-11-02:** #11 dùng **fork lzhoang2801/VoodooI2C 3.0.0** thay bản 2.9.1 chính thức.
- **Người dùng duyệt 2026-11-02:** "Audio và bluetooth tạm thời có thể bỏ qua 1 bên. còn lại hãy dùng." → audio (#14, #15) và Bluetooth (#8) = BỎ QUA tạm thời; mọi dòng khác = DÙNG (☑). Chưa tải binary nào, chưa có gì trong `EFI/`.
- Quyết định: `DÙNG` (đề xuất, đạt checklist trừ ô "người dùng duyệt") · `ỨNG VIÊN` (thiếu bằng chứng / vướng license / cần người dùng chọn) ·
  `KHÔNG CÓ DRIVER` · `KHÔNG CẦN` · `BỎ QUA`.
- Phiên bản = **release chính thức mới nhất trên GitHub tại 2026-11-02** (đã tra qua GitHub API). Các repo tham chiếu (JulioNectar, khucxtriendev, R1)
  dùng bản nightly/CI mới hơn (Lilu 1.7.3, VirtualSMC 1.3.9, WEG 1.7.2, NVMeFix 1.1.4, RestrictEvents 1.1.7, VoodooPS2 2.3.8...), **không phải release** → không dùng.
- Ký hiệu bằng chứng Tahoe: **[RN]** = release notes/changelog chính thức ghi macOS 26; **[JN]** = JulioNectar (T1, XPS 13 Plus, 26.7.1) có kext này trong EFI;
  **[KX]** = khucxtriendev (T2, P1 Gen 5, 26.7.1); **[R1]** = sulthonuladib (cùng board 8A4F, Tahoe, nhưng README ghi phần lớn "not verified"; Wi-Fi/BT là MediaTek, khác máy này).
  [JN]/[KX]/[R1] là bằng chứng mức B (máy khác / phiên bản kext khác), không thay checklist.
- Repo tham chiếu: `_cache/refs/juliornectar` @ 6f03560, `_cache/refs/khucxtriendev` @ 26ee7f3, `_cache/refs/victus-r1` @ e3802fa.

## A. Nhóm nền

| # | Thiết bị | Hardware ID | Driver | Nguồn chính thức | License | Phiên bản | Tahoe | Hạn chế đã biết | Phụ thuộc / thứ tự | Quyết định | Duyệt |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Bootloader | — | OpenCore (+ `ocvalidate` cùng bản) | github.com/acidanthera/OpenCorePkg/releases/tag/1.0.8 | BSD-3-Clause | 1.0.8 (2026-09-27) | ĐÃ XÁC MINH [RN] 1.0.5 "Fixed kext injection compatibility issues with macOS 26", 1.0.7 XhciPortLimit Tahoe | — | — | DÙNG | ☑ |
| 2 | Nền kext | — | Lilu | github.com/acidanthera/Lilu/releases/tag/1.7.2 | BSD-3-Clause | 1.7.2 (2026-03-20) | ĐÃ XÁC MINH [RN] 1.7.1 "Allow loading on macOS 26 without -lilubetaall"; [JN][KX] | — | Nạp đầu tiên | DÙNG | ☑ |
| 3 | SMC giả lập | — | VirtualSMC + SMCProcessor + SMCSuperIO + SMCBatteryManager | github.com/acidanthera/VirtualSMC/releases/tag/1.3.8 | BSD-3-Clause | 1.3.8 (2026-09-27) | ĐÃ XÁC MINH [RN] 1.3.7 "constants for macOS 26"; [JN][KX] | SMCBatteryManager cần EC đọc được trường 16-bit (xem #22) | Lilu → VirtualSMC → plugin SMC | DÙNG | ☑ |
| 4 | CPU lai 6P+4E | i7-12650H (fam 6 model 154) | CpuTopologyRebuild | github.com/b00t0x/CpuTopologyRebuild/releases/tag/2.0.2 | BSD-3-Clause | 2.0.2 (2025-02-11) | CHƯA XÁC MINH bằng RN; [JN][KX][R1] cùng 2.0.2 trên Tahoe | Release trước Tahoe; tuỳ chọn (tối ưu topology), không bắt buộc để boot | Lilu → CpuTopologyRebuild | DÙNG | ☑ |
| 5 | Hạn chế sự kiện / sửa tên CPU | — | RestrictEvents | github.com/acidanthera/RestrictEvents/releases/tag/1.1.6 | BSD-3-Clause | 1.1.6 (2025-07-07) | ĐÃ XÁC MINH [RN] "constants for macOS 26"; [JN][KX] | Cần boot-arg/NVRAM `revpatch`/`revblock` cụ thể — chọn lúc viết config | Lilu → RestrictEvents | DÙNG | ☑ |
| 6 | iGPU (EFI nền, không tăng tốc) | `8086:46A3` | WhateverGreen | github.com/acidanthera/WhateverGreen/releases/tag/1.7.1 | BSD-3-Clause | 1.7.1 (2026-09-27) | ĐÃ XÁC MINH [RN] 1.7.0 "constants for macOS 26"; [JN][KX][R1] | macOS không có driver Alder Lake 46A3; Giai đoạn A chỉ có framebuffer không tăng tốc. Cách hiển thị ở Giai đoạn A (spoof/không spoof, `-igfxvesa`?) **CHƯA XÁC MINH** → quyết định khi viết config | Lilu → WEG | DÙNG | ☑ |

## B. Thiết bị

| # | Thiết bị | Hardware ID | Driver | Nguồn chính thức | License | Phiên bản | Tahoe | Hạn chế đã biết | Phụ thuộc / thứ tự | Quyết định | Duyệt |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 7 | Wi-Fi Intel AX210 | `PCI\VEN_8086&DEV_2725&SUBSYS_00248086` | AirportItlwm-Tahoe (kgp-macPro) + **root patch OCLP-CustoMac (Modern Wireless)** | github.com/kgp-macPro/AirportItlwm-Tahoe/releases/tag/v1.0.0 | GPL-2.0 | v1.0.0 (2026-09-14). Zip SHA-256 (GitHub digest) `1b97713c…8c5f`; executable `1202ec9b…5811`, Info.plist `05f027cc…c288`, LC_UUID `7039DFF1-232B-3697-8E6E-8EE505044F28` (README). **Đã kiểm 2026-11-02:** zip, executable, Info.plist khớp README (LC_UUID chưa kiểm — cần `dwarfdump` trên macOS) | ĐÃ XÁC MINH 25G83 (26.6.2) đầy đủ, 25G229 (26.7) phạm vi hẹp — **25G241: người dùng xác minh trên máy này (2026-11-02)**; phiên bản kext người dùng đã thử chưa ghi, EFI dùng v1.0.0 | Không AirDrop/Continuity Camera/Personal Hotspot; không có Wi-Fi trong Recovery/installer (dùng Ethernet); cần SIP/AMFI hạ cho root patch; cập nhật macOS xoá root patch. Không dùng bản 1.2.0 Alpha/CI. Không dùng itlwm/HeliPort song song | build-01 dùng `DisableIoMapper=true` (cấu hình conventional, KGP khuyên dùng; lý do ở BUILD-LOG); `false` (AppleVTD) để thử sau | DÙNG | ☑ |
| 8 | Bluetooth Intel AX210 (USB) | `USB\VID_8087&PID_0032` | **Phương án 1:** IntelBluetoothFirmware + IntelBTPatcher **2.5.3 (fork lshbluesky)** + BlueToolFixup | github.com/lshbluesky/IntelBluetoothFirmware/releases/tag/v2.5.3 ; BlueToolFixup: github.com/acidanthera/BrcmPatchRAM/releases/tag/2.7.2 | GPL-3.0 ; GPL-2.0 | 2.5.3 (2026-11-03; 2.5.3 chỉ thêm firmware cho 8087:0033, Info.plist vẫn có personality `_0032`) ; 2.7.2 (2026-03-20) | Fork: RN "cài trên Tahoe 26 giống Sequoia"; BrcmPatchRAM [RN] "bluetoothd patches for macOS 26"; [JN][KX] dùng fork 2.5.1. Issue gốc #513 đúng `8087:0032` lỗi trên Tahoe với 2.4.0; báo cáo sửa được trên **25G241** (AX201) bằng fork 2.5.1 + NVRAM `bluetoothExternalDongleFailed`/`bluetoothInternalControllerInfo` + `-btlfxallowanyaddr` | Bản upstream OpenIntelWireless 2.4.0 (2024) **không chạy trên Tahoe** theo #505/#513 → phải chọn fork (khác tác giả upstream). Lỗi ghép BLE AX210 (#514). Cần cold boot | Lilu → BlueToolFixup; IntelBluetoothFirmware → IntelBTPatcher; BT phải nằm trong USB map (cổng nội bộ, `UsbConnector=255`) | **DÙNG** (người dùng duyệt 2026-11-05, build-27; chưa thêm `-btlfxallowanyaddr` vì boot-args 224/228) | ☑ |
| 9 | Ethernet | `PCI\VEN_10EC&DEV_8168&SUBSYS_8A4F103C` | RealtekRTL8111 (Mieze) | github.com/Mieze/RTL8111_driver_for_OS_X/releases/tag/v3.0.0 | **Không có file license** (repo và zip, kiểm 2026-11-02); người dùng chấp nhận dùng cá nhân | v3.0.0 (2025-12-24) | ĐÃ XÁC MINH [RN] "Added support for AppleVTD under Tahoe" | R1 dùng bản cũ 2.4.2 (không có AppleVTD) — không chép | Không cần Lilu | DÙNG | ☑ |
| 10 | NVMe SK hynix BC711 | `PCI\VEN_1C5C&DEV_174A` | NVMeFix | github.com/acidanthera/NVMeFix/releases/tag/1.1.3 | LICENSE.txt của repo: "Copyright (c) 2019, acidanthera" (BSD-style; zip không kèm license) | 1.1.3 (2025-07-07) | ĐÃ XÁC MINH [RN] "constants for macOS 26"; [JN][KX] | Chỉ cải thiện quản lý nguồn/APST; NVMe vẫn chạy bằng driver Apple nếu bỏ | Lilu → NVMeFix | DÙNG | ☑ |
| 11 | Touchpad ELAN0788 (I2C-HID) | `ACPI\ELAN0788` tại `\_SB.PC00.I2C0.TPD0` (addr 0x15, 400 kHz); controller I2C `8086:51E8`; GPIO `INTC1055` | VoodooI2C + VoodooI2CHID (fork lzhoang2801) | github.com/lzhoang2801/VoodooI2C/releases/tag/3.0.0 | GPL-3.0 |  3.0.0 (2026-10-24) | CHƯA XÁC MINH bằng RN (release trước Tahoe); [JN][KX][R1] cùng 2.9.1 trên Tahoe | **ĐÍNH CHÍNH 2026-11-02:** Info.plist của bản 2.9.1 CHÍNH THỨC **KHÔNG có** `0x51e88086` (chỉ 02e8/06e8/34e8/9d60/9de8/a160/a368); bản "2.9.1" trong R1/JN/KX là bản đã sửa (SHA khác bản chính thức) → dùng fork lzhoang2801 3.0.0 (GPL-3.0, tác giả PR upstream #586 "Add Tiger/Alder/Raptor Lake support", release 2026-10-24, asset `VoodooI2C-2.9.1-RELEASE.zip` sha256 `703a21ef…cc36`; Tahoe CHƯA XÁC MINH bằng RN). VoodooGPIO có `INTC1055`. `_CRS` của TPD0 chỉ trả GpioInt khi OSYS ≥ Win10 và TPDM=0 → cần SSDT-XOSI/GPI0 (#S3). PR #586 (ADL/TGL GPIO, merge 2026-10-24) chưa có release. Lỗi wake #582 | Lilu không cần; VoodooI2C (kèm VoodooGPIO, VoodooI2CServices, **VoodooInput**) → VoodooI2CHID | DÙNG | ☑ |
| 12 | Bàn phím PS/2 | `ACPI\HPQ8001` tại `\_SB.PC00.LPCB.PS2K` | VoodooPS2Controller (chỉ Keyboard) | github.com/acidanthera/VoodooPS2/releases/tag/2.3.7 | LICENSE.md của repo: Apple Public Source License (zip không kèm license) | 2.3.7 (2024-12-03) | CHƯA XÁC MINH bằng RN; [JN][KX][R1] dùng 2.3.8 (nightly) trên Tahoe | **Tắt** plugin VoodooInput/VoodooPS2Mouse/Trackpad của VoodooPS2 để không trùng VoodooInput của VoodooI2C | VoodooPS2Controller → VoodooPS2Keyboard | DÙNG | ☑ |
| 13 | Phím độ sáng | Intel HID `INTC1070` / EC | BrightnessKeys | github.com/acidanthera/BrightnessKeys/releases/tag/1.0.3 | BSD-3-Clause | 1.0.3 (2023-04-03) | CHƯA XÁC MINH bằng RN; [JN][KX][R1] trên Tahoe | Có thể cần patch `_Qxx` của EC; độ sáng phụ thuộc framebuffer (Giai đoạn A có thể không chỉnh được) | Lilu → BrightnessKeys | DÙNG | ☑ |
| 14 | Audio Realtek ALC245 | codec `0x10EC0245`, subsys `0x103C8A4F`; HDA `8086:51C8` | AppleALC (layout-id thử 11 → 12 → 13) **+ khôi phục AppleHDA** | github.com/acidanthera/AppleALC/releases/tag/1.9.8 | BSD-3-Clause | 1.9.8 (2026-09-27) | AppleALC [RN] 1.9.5 "constants for macOS 26". **Tahoe đã gỡ AppleHDA** (R1 README) → AppleALC một mình không ra tiếng | Layout ALC245 chính thức: 11 (Lenovo/soto2080), 12 (Lenovo), 13 (HP Omen 2020). Chưa có layout cho HP 8A4F. Không có HDMI audio (HDMI ở dGPU) | Lilu → AppleALC → (SimpleHDA) | **DÙNG** (người dùng duyệt 2026-11-05; **layout 11** (build-31: loa + mic OK, tai nghe chỉ kênh trái); layout 13 hỏng (loa câm, không mic)) | ☑ |
| 15 | Khôi phục AppleHDA trên Tahoe | — | **Root patch Modern Audio của OCLP-CustoMac 3.0.3** (`modern_audio.py`, AppleHDA 26.0 Beta 1, cần KDK); SimpleHDA bị loại | github.com/laobamac/SimpleHDA/releases/tag/v1.0.0 | **KHÔNG khai báo license** ("All rights reserved") | v1.0.0 (2026-10-14) | RN: "khôi phục AppleHDA gốc trên Tahoe qua OpenCore, cần Lilu ≥ 1.7.1, AppleALC, `keepsyms=1`"; [KX] dùng với ALC287 | **Gói chứa `AppleHDA.kext` gốc của Apple** → không được commit vào repo (repo đang public) — vi phạm §4 "không phân phối binary của Apple". Không license → không đạt checklist | Lilu → AppleALC → SimpleHDA | **DÙNG root patch OCLP** (người dùng duyệt 2026-11-05; SimpleHDA KHÔNG dùng) | ☑ |
| 15b | Audio ALC245 không root patch (thay #15) | codec `0x10EC0245`, HDA `8086:51C8` | **VoodooHDA 3.6.8** (CloverHackyColor) cài vào `/Library/Extensions` trên MÁY B (không qua EFI) | github.com/CloverHackyColor/VoodooHDA/releases/tag/Release368 — `VoodooHDA.kext-368.zip`, sha256 `9aaa01b245f4827b2de5edfdc028700b9bc8823f03bfb1daf280b8571f88adb0` (GitHub digest) | BSD-2-Clause | 3.6.8 (2026-09-18, bản ổn định; 3.7.1-alpha bỏ qua) | Dortania Tahoe guide (cập nhật 2026-03-15): cách thay AppleHDA, `/Library/Extensions` + duyệt trong Privacy & Security, cần SIP hạ (dự án `0x0A13` đã đủ); repo sửa prefpane cho Tahoe (#19, #20, 03/2026); báo cáo cộng đồng chạy trên Tahoe. ALC245 cụ thể: CHƯA XÁC MINH | Chất lượng có thể kém AppleHDA; prefpane không có trong asset 3.6.8 (tuỳ chọn); phụ thuộc IOAudioFamily (không nạp được trong Boot KC → không tiêm qua OpenCore); không dùng song song AppleHDA (Revert root patch Modern Audio) | **DÙNG** (MÁY B 00:29: hoạt động, ổn định hơn root patch — người dùng) | Người dùng 2026-11-07 00:23 ("dùng VoodooHDA đi") |
| 16 | USB map | xHCI PCH `8086:51ED`; TB4 USB `8086:461E` | USBToolBox.kext + UTBMap.kext (người dùng tạo bằng công cụ USBToolBox trên MÁY B) | github.com/USBToolBox/kext/releases/tag/1.2.0 | **Không có file license** (repo và zip, kiểm 2026-11-02); người dùng chấp nhận dùng cá nhân | 1.2.0 (2025-06-13) | ĐÃ XÁC MINH một phần: [RN] "Tahoe support (WIP)"; maintainer (issue #15, 2025-11-10) "not needed with 1.2.0"; [JN][KX][R1] | Cần map ≤ 15 cổng; map phải làm trên MÁY B | — | DÙNG | ☑ |
| 17 | xHCI không được macOS nhận | `8086:51ED` | XHCI-unsupported (codeless injector) | Gốc RehabMan/OS-X-USB-Inject-All — **không có GitHub release** | NOASSERTION | — (refs dùng 0.9.2) | [JN][KX][R1] có trong EFI Tahoe; Info.plist có `0x51ed8086` | Không có binary release chính thức → đề xuất **tự viết injector chỉ có Info.plist** (không có code) theo đúng nội dung, hoặc kiểm xem USBToolBox có tự attach không | — | DÙNG | ☑ |
| 18 | Camera HP Wide Vision HD | `USB\VID_30C9&PID_0069` (UVC) | Driver UVC có sẵn của macOS | — | — | — | **Hoạt động** trên build-31 (người dùng, 2026-11-05) | Chỉ chạy nếu cổng camera có trong USB map | USB map | KHÔNG CẦN | ☑ |
| 19 | Card reader Realtek | `PCI\VEN_10EC&DEV_5228&SUBSYS_8A4F103C` | RealtekCardReader (0xFireWolf) | github.com/0xFireWolf/RealtekCardReader | BSD-3-Clause | 0.9.7 (2022) | — | README: RTS5228 **"Not Yet"** (chưa hỗ trợ) | — | KHÔNG CÓ DRIVER | ☑ |
| 20 | dGPU RTX 3050 Ti | `PCI\VEN_10DE&DEV_25A0` (+ audio `10DE:2291`) tại `\_SB.PC00.PEG1.PEGP` | — (tắt nguồn bằng SSDT, #S5) | — | — | — | — | macOS không có driver Ampere. Không HDMI | — | BỎ QUA/VÔ HIỆU HOÁ | ☑ |
| 21 | iGPU tăng tốc Metal | `8086:46A3` (64 EU, 6 L3 bank, stolen 60 MB) | NootedGreen (JulioNectar stack) | — | Thou Shalt Not Profit 1.0 | — | — | **Giai đoạn B**, chưa xét ở đây | — | BỎ QUA (Giai đoạn A) | ☑ |
| 22 | EC / pin | `PNP0C09` tại `\_SB.PC00.LPCB.EC0_`; DSDT có trường EC 16-bit (`BADC`,`BFCC`,`MBCV`,`MBRM`,`MCUR`) và 256-bit (`SMD0`) | ECEnabler | github.com/averycblack/ECEnabler/releases/tag/1.0.6 (repo 1Revenger1/ECEnabler đã chuyển sang đây) | **Không có file license** (repo và zip, kiểm 2026-11-02); người dùng chấp nhận dùng cá nhân | 1.0.6 (2025-07-06) | ĐÃ XÁC MINH [RN] "Update max kernel constant to Tahoe"; [KX][R1] | Không license → không đạt checklist; phương án khác: patch ACPI tách trường 16-bit (cách cũ, nhiều patch) | Lilu → ECEnabler → SMCBatteryManager | DÙNG | ☑ |
| 23 | Vân tay / ALS / cảm biến | — | — | — | — | — | — | Dump không phát hiện | — | KHÔNG CẦN | ☑ |

## C. SSDT cần viết (từ DSDT thật bằng `ssdt-authoring`, KHÔNG chép AML của R1)

| # | SSDT | Lý do (từ DSDT/SSDT của máy) | Trạng thái |
|---|---|---|---|
| S1 | SSDT-PLUG-ALT (hoặc tương đương cho CPU lai) | Alder Lake; R1 dùng `SSDT-PLUG-ALT` | DÙNG (viết bằng ssdt-authoring) — xác minh cách khai báo CPU trong DSDT |
| S2 | SSDT-EC-USBX | EC thật tên `EC0_` (không phải `EC`) → cần thiết bị `EC` giả + USBX cấp điện USB | DÙNG (viết bằng ssdt-authoring) |
| S3 | SSDT-XOSI / SSDT-GPI0 (touchpad) | `TPD0._CRS` trả GpioInt chỉ khi `OSYS ≥ 0x07DC` và `TPDM == 0`; GPI0 `_HID` = INTC1055 (PNP0C02 nếu `GPHD=1`) | DÙNG (viết bằng ssdt-authoring) |
| S4 | SSDT-AWAC (RTC) | DSDT có biến `STAS`, `AWAC` status 15, `RTC_` status 0 | DÙNG (viết bằng ssdt-authoring) |
| S5 | SSDT-dGPU-OFF | `PEG1.PEGP._OFF` (SSDT14) gọi `PEG1.PXP._OFF` qua `CondRefOf`; chưa thấy `PXP_` được định nghĩa trong bảng đã dump → đường tắt **CHƯA XÁC MINH** | DÙNG (viết bằng ssdt-authoring) — cần đọc thêm SSDT14/16 |
| S6 | SSDT-MCHC / SSDT-SBUS | SMBus `8086:51A3` | DÙNG (viết bằng ssdt-authoring) |
| S7 | Patch RTC lỗi POST 005 (HP) | Gợi ý tầng thấp (T3-1), chưa có bằng chứng trên máy | CÓ ĐIỀU KIỆN — chỉ viết nếu gặp lỗi POST 005 sau khi khởi động lại từ macOS |

## Thiết bị KHÔNG có driver khả thi
| Thiết bị | Hardware ID | Lý do | Giải pháp thay thế |
|---|---|---|---|
| Card reader RTS5228 | `10EC:5228` | RealtekCardReader ghi "Not Yet" | Đầu đọc thẻ USB |
| dGPU RTX 3050 Ti | `10DE:25A0` | Không có driver NVIDIA Ampere cho macOS | Tắt nguồn (S5); dùng iGPU |
| HDMI | (nối dGPU) | Đi qua dGPU | Không có; USB-C/DP (iGPU) chưa xác minh |

## 5 rủi ro lớn nhất
1. **Audio trên Tahoe**: AppleHDA đã bị gỡ; con đường duy nhất có bằng chứng (SimpleHDA) không có license và chứa binary Apple; root patch AppleHDA của OCLP chồng thêm lên root patch Wi-Fi và stack đồ họa → có thể phải chấp nhận không có audio, hoặc dùng audio USB.
2. **Bluetooth AX210 trên Tahoe**: upstream 2.4.0 lỗi đúng với `8087:0032` (#513); chỉ có fork lshbluesky + NVRAM workaround, chưa có báo cáo trên chính AX210 + 25G241.
3. **Wi-Fi + root patch**: AirportItlwm-Tahoe chưa kiểm định 25G241; root patch OCLP-CustoMac yêu cầu hạ SIP/AMFI và sẽ tương tác với stack NootedGreen ở Giai đoạn B (chưa ai ghi nhận); cập nhật macOS xoá patch.
4. **Tắt dGPU**: phương thức `PXP_._OFF` chưa tìm thấy → nếu SSDT tắt nguồn sai, dGPU vẫn tốn pin/nóng hoặc gây treo; repo JulioNectar ghi nhận panic `IOAccelTask::release` trên Alder Lake-H có dGPU (#24, #16).
5. **Touchpad và kext phát hành trước Tahoe**: VoodooI2C 2.9.1, VoodooPS2 2.3.7, CpuTopologyRebuild 2.0.2, BrightnessKeys 1.0.3 không có release notes cho Tahoe; chỉ có bằng chứng gián tiếp từ repo tham chiếu dùng bản nightly. Thêm: ECEnabler, SimpleHDA, RealtekRTL8111, USBToolBox không khai báo license SPDX → phải đọc license trong gói trước khi `DÙNG`.

## Người dùng cần quyết định (đã trả lời 2026-11-02: (a) dùng tất cả trừ audio/BT; (b),(c) bỏ qua tạm thời; (d) dùng ECEnabler; (e) Wi-Fi đã xác minh 25G241 (người dùng))
- (a) Duyệt từng dòng (đánh ☑) hoặc nói "duyệt tất cả dòng DÙNG".
- (b) Bluetooth: chấp nhận fork lshbluesky 2.5.2? (upstream không chạy trên Tahoe)
- (c) Audio: bỏ audio ở Giai đoạn A / dùng SimpleHDA cục bộ (không commit, chỉ trên USB) / root patch AppleHDA của OCLP?
- (d) ECEnabler không có license: chấp nhận dùng cá nhân, hay patch ACPI tách trường?
- (e) Ghi phiên bản AirportItlwm-Tahoe + build macOS bạn đã thử Wi-Fi.

## ĐỀ XUẤT build-06 — sửa Wi-Fi (CHỜ NGƯỜI DÙNG DUYỆT, 2026-11-02)
Bằng chứng: log OpenCore DEBUG build-04 — `IO80211FamilyLegacy not in Boot KC` → `Vtable patching failed for kext com.zxystd.AirportItlwm` → AirportItlwm không nạp.
OCLP-CustoMac (kgp-macPro, cùng tác giả AirportItlwm-Tahoe) dựng EFI Modern Wireless như sau (`opencore_legacy_patcher/efi_builder/networking/wireless.py` L55–58,
`payloads/Config/config.plist`, `constants.py` L85/86/103):

| # | Thành phần | Nguồn | Phiên bản | License | Ghi chú |
|---|---|---|---|---|---|
| W1 | IOSkywalkFamily.kext (Ventura, đã vá) | github.com/kgp-macPro/OCLP-CustoMac `payloads/Kexts/Wifi/IOSkywalkFamily-v1.2.0.zip` | 1.2.0 | NOASSERTION; **chứa binary Apple** | MinKernel 23.0.0; nạp trước IO80211FamilyLegacy |
| W2 | IO80211FamilyLegacy.kext (Ventura) | `payloads/Kexts/Wifi/IO80211FamilyLegacy-v1.0.0.zip` | 1.0.0 | NOASSERTION; **chứa binary Apple** | MinKernel 23.0.0; plugin AirPortBrcmNIC KHÔNG bật (chỉ Broadcom) |
| W3 | Kernel/Block `com.apple.iokit.IOSkywalkFamily` | config mẫu OCLP | — | — | Strategy Exclude, MinKernel 23.0.0 |
| W4 | AMFIPass.kext + boot-arg `-amfipassbeta` | `payloads/Kexts/Acidanthera/AMFIPass-v1.4.1-RELEASE.zip` | 1.4.1 | NOASSERTION | README OCLP-CustoMac: cấu hình đã kiểm định; `amfi=0x80` không cần |
| W5 | Root patch "Modern Wireless" bằng app OCLP-CustoMac 3.0.3 (người dùng chạy trên MÁY B) | release OCLP-CustoMac | 3.0.3 | — | cần SIP hạ khi patch; cập nhật macOS xoá patch |
| W-alt | **laobamac/itlwm AirportItlwm-Tahoe v2.4.0-alpha** (thay W1–W5 + AirportItlwm kgp) | github.com/laobamac/itlwm/releases/tag/v2.4.0-alpha — asset `AirportItlwm-Tahoe-v2.4.0-RELEASE-alpha-7204c69.zip` (digest sha256 `a5d098e6752592435c021aa6e8d08c64ee6aab9f2786660a6c72d7af1218fcf9`, pre-release) | v2.4.0-alpha (7204c69) | GPL-2.0 | Bằng chứng: JN dùng trên 25G241 (CHANGELOG 2026-10-22, bản tự build từ commit `738d4c6` — dự án KHÔNG dùng binary của JN), Wi-Fi gốc của Tahoe (IO80211Family/IOSkywalkFamily của hệ thống) → **không cần root patch Modern Wireless, không cần IOSkywalkFamily/IO80211FamilyLegacy + Block**; `itlwm_he=1` bật tốc độ Wi-Fi 6. Máy JN là XPS 13 Plus (card khác AX210) → AX210 `8086:2725` + bản 2.4.0 trên Tahoe: CHƯA XÁC MINH. khucxtriendev từng ghi panic Skywalk với AirportItlwm-Tahoe 2.4.0 | Hạn chế: alpha; không AirDrop/AWDL, không WPA3-only; MinKernel 25 / MaxKernel 25.99.99. Đổi cần: OCLP-CustoMac Revert (mất cả Modern Audio) rồi chỉ áp lại **Modern Audio**; gỡ W1–W3; giữ AMFIPass (W4) cho root patch Audio | **DÙNG** từ build-45 (Wi-Fi chạy trên MÁY B 2026-11-07 00:20) | Người dùng 2026-11-07 00:10 |

Vướng quy tắc cần người dùng quyết: (a) nguồn là thư mục `payloads/` trong repo chính chủ, **không phải release asset** (CLAUDE.md §4 yêu cầu release chính thức);
(b) W1/W2 là binary Apple — chỉ dùng trên USB của người dùng, **không commit**; (c) hạ AMFI bằng AMFIPass và hạ SIP cho root patch (CLAUDE.md §6: hệ quả bảo mật — kext/binary không ký có thể chạy; cập nhật macOS xoá root patch).
Thứ tự Kernel/Add dự kiến: … RealtekRTL8111 → AMFIPass → IOSkywalkFamily → IO80211FamilyLegacy → AirportItlwm → …
Bonus: OCLP-CustoMac còn có root patch **Modern Audio / AppleHDA** (đường audio có nguồn chính chủ, thay SimpleHDA) — để sau.

## Trạng thái thực tế trên MÁY B (cập nhật 2026-11-02, build-08)
| # | Thiết bị | Driver đang dùng | Kết quả người dùng |
|---|---|---|---|
| 7 | Wi-Fi AX210 | AirportItlwm-Tahoe **1.1.0-beta.1 ZC28-SERVICE** + IOSkywalkFamily 1.2.0 + IO80211FamilyLegacy 1.0.0 + AMFIPass 1.4.1 + root patch OCLP-CustoMac 3.0.3 (Modern Wi-Fi), DisableIoMapper=true, SIP 0x803 | **Hoạt động** (bản 1.0.0 trong build-07 thì không thấy mạng — chưa root patch lúc đó, chưa tách được nguyên nhân) |
| 9 | Ethernet RTL8111 rev 0x16 | RealtekRTL8111 **2.4.2** (thay 3.0.0) | **Hoạt động** (có IP); 3.0.0 không hoạt động ở mọi build |
| 11 | Touchpad | VoodooI2C 3.0.0 (lzhoang2801), polling | Hoạt động (build-05) |
| 12 | Bàn phím | VoodooPS2 2.3.7 | Hoạt động (build-05) |
| 20 | dGPU | SSDT-DGPU-OFF + disable-gpu + -wegnoegpu | Người dùng báo "hoạt động" (build-05) |
| 22 | Pin/EC | ECEnabler + SMCBatteryManager | Hoạt động (build-05) |
| 8 | Bluetooth | — | DÙNG từ build-27 (2026-11-05) |
| 14, 15 | Audio | — | build-30 → build-44: AppleALC 1.9.8 + root patch Modern Audio (OCLP). **Từ 2026-11-07: VoodooHDA (#15b), không root patch** |

## Giai đoạn B — kiểm định NootedGreen R3 (khucxtriendev) — CHỜ NGƯỜI DÙNG DUYỆT (2026-11-02)
| # | Thành phần | Nguồn | Phiên bản / hash | License | Bằng chứng Tahoe | Hạn chế | Quyết định | Duyệt |
|---|---|---|---|---|---|---|---|---|
| G1 | NootedGreen R3 (fork khucxtriendev của stack JulioNectar) | github.com/khucxtriendev/irisxegraphic-i712800h-efi/releases/tag/v3.0-booted (`P1-Gen5-20261025-r3-booted.zip`, digest `ab9a9e9c…7a96` khớp) | binary sha256 `6b99b13c5ca22f73…` = SHA256SUMS.json của release; nguồn `vendor/iris-xe` (gốc sgiammori 95f8189, có `ngreen-eu`/`ngreen-l3`) | NootedGreen TSNPL 1.0 (`vendor/iris-xe/src/LICENSE-NootedGreen`); repo không có license gốc | Mức B: tác giả tự báo boot + Metal PASS 25G241 trên ADL-H 46A6 96 EU + RTX A1000 | build cho 96 EU; hook `IGRangeAllocator::initWithRange` (đặt chỗ GGTT 16–160 MiB) chưa xác minh runtime theo chính tác giả; user-space JN đang cài khác R3 (thử A1 chỉ đổi kext) | DÙNG (thử A1) — người dùng duyệt 2026-11-02 | ☑ |

## Giai đoạn B — NootedGreen JN + patch GMSFIX (người dùng duyệt F1, 2026-11-03)
| # | Thành phần | Nguồn | Phiên bản / hash | License | Bằng chứng | Hạn chế | Quyết định | Duyệt |
|---|---|---|---|---|---|---|---|---|
| G2 | NootedGreen JN + `patches/nootedgreen-gmsfix-jn6f03560.patch` (tự viết) | JulioNectar/Hackintosh-XPS13Plus-IrisXe-Tahoe @ `6f03560` + patch dự án (hiện dùng **v7** `patches/nootedgreen-gmsfix-v7-jn6f03560.patch`, sha256 `1ecd5bb0…4ee6`; v1 sha256 `94a0ffa9…92d8` đã xoá khỏi repo) | build trên MÁY B bằng `build-nootedgreen.sh`; md5/sha256 ghi khi nhận kext | Thou Shalt Not Profit 1.0 (patch là sửa đổi phi lợi nhuận, chỉ dùng cá nhân; không phân phối binary) | Phân tích tĩnh `docs/GRAPHICS-PANIC-ANALYSIS.md`; `clang -fsyntax-only` 0 lỗi, không thêm cảnh báo | Giả thuyết H3 CHƯA XÁC MINH runtime; tắt bằng `-ngreennogmsfix`; nếu thất bại → F2 | DÙNG (build-19 → build-26; v7 trong build-26) | Người dùng 2026-11-03 ("theo F1 đi, nếu không được thì sang F2") |
| G2b | NootedGreen JN **24450b4** + `patches/nootedgreen-gmsfix-v9-jn24450b4.patch` (tự viết) | JulioNectar/Hackintosh-XPS13Plus-IrisXe-Tahoe @ `24450b4` (2026-11-03) + patch v9 (sha256 `3685fa72…cf0a`). Cùng commit: user-space libxedrv v21–v24 (thứ tự compute/render, barrier compute, sửa blur) cài bằng `install.sh` | build + cài trên MÁY B (GMSFIX-RUNBOOK §v9); md5/sha256 ghi khi nhận kext | Thou Shalt Not Profit 1.0 (như G2) | v8 áp lên 24450b4: 1 hunk fuzz 2 (chỉ do JN chèn XE-PORTGUARD sau `gTopoTc`, khối dự án vẫn ở phạm vi file), không trùng route với XE-PORTGUARD/XE-HWCAPS114C; `clang++ -fsyntax-only` 0 lỗi, số cảnh báo bằng JN gốc. JN đánh dấu các mục mới là "testing" | Lý do: GB7 GPU treo ở Feature Matching trên build-37 (nghi libxedrv v20, CHƯA XÁC MINH). XE-PORTGUARD mới bật mặc định trên đường spoof (tắt: `-ngreennoportguard`); tắt từng sửa libxedrv: `XE_COMPUTE_NATIVO=1`, `XE_BARREIRA_NATIVA=1` | CHỜ KEXT (build-38) | Người dùng 2026-11-06 19:49 ("duyệt nâng lên commit mới nhất của JN") |



## Cập nhật 2026-11-07: không còn root patch OCLP
- Wi-Fi: W1–W5 (IOSkywalkFamily/IO80211FamilyLegacy Ventura, Block Skywalk, root patch Modern Wireless) **thay bằng W-alt** (laobamac AirportItlwm-Tahoe v2.4.0-alpha). W1–W3 để Enabled=false trong `config.plist` và `config-install.plist` cho đường lui; AirportItlwm kgp 1.1.0-beta.1 không còn trong EFI (snapshot build-44 trở về trước).
- Audio: #15 (root patch Modern Audio) **thay bằng #15b** (VoodooHDA 3.6.8 trong `/Library/Extensions`). AppleALC + `layout-id` 11 còn trong EFI nhưng không tác dụng (không có AppleHDA).
- AMFIPass + `-amfipassbeta` (W4): chỉ phục vụ root patch → có thể bỏ; CHƯA làm (thay đổi riêng, cần thử).
