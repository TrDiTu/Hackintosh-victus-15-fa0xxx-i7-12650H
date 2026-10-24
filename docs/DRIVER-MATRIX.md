# DRIVER-MATRIX — Ma trận kiểm định Driver cho Laptop HP Victus 15-fa0xxx

*Mục tiêu: macOS 26 Tahoe (Darwin 25)*  

## Cập nhật touchpad 2026-10-25 (thay thế kết luận cũ)

- **ĐÃ DUYỆT THỬ NGHIỆM:** người dùng trả lời "Duyệt thử bản này trên Tahoe". Cho phép ngoại lệ thiếu bằng chứng Tahoe cho fork release 3.0.0; đã thay core/plugins/HID trong build-10. Tương thích thực tế vẫn CHƯA XÁC MINH. Các dòng chờ duyệt bên dưới là lịch sử.
- Build-09 boot thành công nhưng touchpad và âm thanh không hoạt động. Kext hiện tại là VoodooI2C 2.9.1, thiếu match PCI 8086:51E8. Rút lại khẳng định R1 đã chứng minh touchpad/Tahoe hoạt động và polling chắc chắn giải quyết lỗi.
- **ỨNG VIÊN, chờ duyệt thử nghiệm:** [lzhoang2801/VoodooI2C release 3.0.0](https://github.com/lzhoang2801/VoodooI2C/releases/tag/3.0.0), GPL-3.0, CFBundleVersion vẫn 2.9.1. Có match I2C 8086:51E8, GPIO INTC1055 và HID PNP0C50. **CHƯA XÁC MINH TAHOE**, chưa đưa vào EFI. Hash và giới hạn trong `TOUCHPAD-ANALYSIS-20261025.md` và `SOURCES.md`.
- Giữ Services / GPIO / VoodooInput trước VoodooI2C, rồi VoodooI2CHID; chỉ một VoodooInput. Chờ duyệt ngoại lệ thử nghiệm cho bản fork này theo AGENTS.md §4.

*Trạng thái: Đang chờ Người dùng duyệt trước khi tải binary hoặc nạp vào EFI.*

Quy ước Quyết định:
- `DÙNG`: Đã kiểm định đầy đủ, có nguồn chính thức, khuyến nghị nạp vào EFI.
- `ỨNG VIÊN`: Cần thử nghiệm thêm trong quá trình boot.
- `KHÔNG CÓ DRIVER`: Phần cứng không được macOS hỗ trợ (vô hiệu hoá hoặc bỏ qua).
- `KHÔNG CẦN`: Thiết bị ACPI/System không cần kext riêng.
- `VÔ HIỆU HOÁ`: Cần tắt bằng SSDT/boot-arg để tránh lỗi và hao pin.

---

## 1. Ma trận kiểm định Driver chi tiết

| # | Nhóm thiết bị | Hardware ID (từ dump thực tế) | Driver / Kext ứng viên | Nguồn chính thức | License | Phiên bản khuyến nghị | Tahoe (macOS 26) | Hạn chế đã biết | Phụ thuộc & Thứ tự nạp | Quyết định | Duyệt |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **Core Patcher** | N/A (Hệ thống) | `Lilu.kext` | [acidanthera/Lilu](https://github.com/acidanthera/Lilu/releases) | BSD-3-Clause | 1.6.8 / 1.6.9 | CHƯA XÁC MINH (cần boot-arg `-lilubetaall`) | Cần cờ beta trên Darwin 25 | **Nạp đầu tiên (thứ tự 1)** | `DÙNG` | 🔲 |
| 2 | **SMC Emulator** | ACPI `AppleSMC` | `VirtualSMC.kext` | [acidanthera/VirtualSMC](https://github.com/acidanthera/VirtualSMC/releases) | APSL-2.0 | 1.3.4 | CHƯA XÁC MINH (chạy qua Lilu) | Cần thiết để boot | **Nạp ngay sau Lilu (thứ tự 2)** | `DÙNG` | 🔲 |
| 3 | **Đồ hoạ iGPU** | `8086:46A3` (Alder Lake-P GT1) | `WhateverGreen.kext` + DeviceProperties | [acidanthera/WhateverGreen](https://github.com/acidanthera/WhateverGreen/releases) | GPL-2.0 | 1.6.8 | ĐÃ XÁC MINH một phần (TGL spoof hoạt động trên R1) | Chưa có Metal 3 tăng tốc đồ hoạ 3D ở Giai đoạn A; chạy GUI qua VESA/TGL frame | Phụ thuộc Lilu; nạp sau VirtualSMC | `DÙNG` | 🔲 |
| 4 | **Đồ hoạ dGPU** | `10DE:25A0` (RTX 3050 Ti Mobile) | `SSDT-dGPU-Off.aml` | Tự biên dịch ACPI | Open Source | N/A | Hoàn toàn vô hiệu hoá | dGPU tắt hoàn toàn; cổng HDMI ngoài không xuất hình | Gọi `_OFF` tại `\_SB.PC00.PEG1.PEGP` | `VÔ HIỆU HOÁ` | 🔲 |
| 5 | **Mạng Wi-Fi** | `8086:2725` (Intel AX210/AX211) | `itlwm.kext` + `HeliPort.app` | [OpenIntelWireless/itlwm](https://github.com/OpenIntelWireless/itlwm/releases) | GPL-2.0 / BSD | 2.3.0 | CHƯA XÁC MINH TAHOE (hoạt động tốt qua IOEthernet) | Không hỗ trợ AirDrop/Continuity gốc; cần app HeliPort; không có mạng trong Recovery offline | Nạp độc lập (không phụ thuộc Lilu) | `DÙNG` | 🔲 |
| 6 | **Bluetooth** | USB `8087:0032` (Intel AX210 BT) | `IntelBluetoothFirmware.kext` + `BlueToolFixup.kext` | [OpenIntelWireless](https://github.com/OpenIntelWireless/IntelBluetoothFirmware/releases), [acidanthera/BrcmPatchRAM](https://github.com/acidanthera/BrcmPatchRAM/releases) | GPL-2.0 | IBF 2.4.0, BTF 2.6.9 | CHƯA XÁC MINH TAHOE (BlueToolFixup cập nhật cho modern bluetoothd) | Cần sleep/wake test | BlueToolFixup nạp sau Lilu | `DÙNG` | 🔲 |
| 7 | **Mạng LAN** | `10EC:8168` (Realtek RTL8111) | `RealtekRTL8111.kext` | [Mieze/RTL8111_driver_for_OS_X](https://github.com/Mieze/RTL8111_driver_for_OS_X/releases) | GPL-2.0 | 2.4.2 | ĐÃ XÁC MINH (R1 dùng ổn định trên Sequoia) | Không có hạn chế lớn | Nạp độc lập | `DÙNG` | 🔲 |
| 8 | **Âm thanh** | `10EC:0245` (Realtek ALC245) | `AppleALC.kext` | [acidanthera/AppleALC](https://github.com/acidanthera/AppleALC/releases) | BSD-3-Clause | 1.9.2 | CHƯA XÁC MINH TAHOE (cần layout-id: 11, 13, 21...) | Có thể cần tinh chỉnh combo jack | Phụ thuộc Lilu; nạp sau Lilu | `DÙNG` | 🔲 |
| 9 | **Bàn phím PS/2** | ACPI `HPQ8001` (PS2K) | `VoodooPS2Controller.kext` (`VoodooPS2Keyboard`) | [acidanthera/VoodooPS2](https://github.com/acidanthera/VoodooPS2/releases) | GPL-2.0 | 2.3.6 | ĐÃ XÁC MINH (R1 hoạt động tốt) | Tắt plugin Mouse và Trackpad trong kext để tránh xung đột với I2C | Nạp độc lập | `DÙNG` | 🔲 |
| 10 | **Touchpad I2C** | ACPI `ELAN0788` (`04F3:321A`) | `VoodooI2C.kext` + `VoodooI2CHID.kext` | [VoodooI2C/VoodooI2C](https://github.com/VoodooI2C/VoodooI2C/releases) | GPL-3.0 | 2.8 | ĐÃ XÁC MINH (R1 hoạt động với `-vi2c-force-polling`) | Cần boot-arg polling để tránh lỗi ngắt GPIO trên HP | Thứ tự: `VoodooI2CServices` → `VoodooGPIO` → `VoodooI2C` → `VoodooI2CHID` | `DÙNG` | 🔲 |
| 11 | **Phím sáng Fn** | ACPI Hotkeys | `BrightnessKeys.kext` | [acidanthera/BrightnessKeys](https://github.com/acidanthera/BrightnessKeys/releases) | BSD-2-Clause | 1.0.3 | ĐÃ XÁC MINH (R1 dùng tốt) | Không có | Phụ thuộc Lilu | `DÙNG` | 🔲 |
| 12 | **Quản lý Pin** | ACPI `PNP0C0A` (`BAT0`), `EC0_` | `SMCBatteryManager.kext` + `ECEnabler.kext` | VirtualSMC Plugins, [1Revenger1/ECEnabler](https://github.com/1Revenger1/ECEnabler/releases) | APSL-2.0 / BSD | SMCBat 1.3.4, ECEnabler 1.0.5 | ĐÃ XÁC MINH (R1 dùng tốt) | Không có | Phụ thuộc VirtualSMC | `DÙNG` | 🔲 |
| 13 | **Cảm biến CPU** | Alder Lake CPU | `SMCProcessor.kext` | VirtualSMC Plugins | APSL-2.0 | 1.3.4 | ĐÃ XÁC MINH | Không có | Phụ thuộc VirtualSMC | `DÙNG` | 🔲 |
| 14 | **CPU Topology** | Alder Lake-H (6P + 4E) | `CpuTopologyRebuild.kext` | [b00t0x/CpuTopologyRebuild](https://github.com/b00t0x/CpuTopologyRebuild/releases) | BSD-3-Clause | 1.1.0 | ĐÃ XÁC MINH (R1 dùng tốt) | Giúp macOS điều phối chính xác P-core và E-core | Phụ thuộc Lilu | `DÙNG` | 🔲 |
| 15 | **SMBIOS Patch** | CPU & Model check | `RestrictEvents.kext` | [acidanthera/RestrictEvents](https://github.com/acidanthera/RestrictEvents/releases) | BSD-3-Clause | 1.1.4 | ĐÃ XÁC MINH (R1 dùng tốt) | Bỏ qua cảnh báo bộ nhớ và định danh CPU Alder Lake | Phụ thuộc Lilu | `DÙNG` | 🔲 |
| 16 | **Ổ cứng NVMe** | `1C5C:174A` (SK hynix BC711) | `NVMeFix.kext` | [acidanthera/NVMeFix](https://github.com/acidanthera/NVMeFix/releases) | BSD-3-Clause | 1.1.2 | ĐÃ XÁC MINH | Tối ưu hóa APST quản lý năng lượng NVMe | Phụ thuộc Lilu | `DÙNG` | 🔲 |
| 17 | **Đầu đọc thẻ SD** | `10EC:5228` (Realtek RTS5288) | `RealtekCardReader.kext` + `Friend` | [0xFireWolf/RealtekCardReader](https://github.com/0xFireWolf/RealtekCardReader/releases) | BSD-2-Clause | 0.9.7 | CHƯA XÁC MINH TAHOE | Đọc thẻ PCIe SD | Nạp sau Lilu | `ỨNG VIÊN` | 🔲 |
| 18 | **Camera UVC** | USB `30C9:0069` | Native macOS UVC driver | Apple Native | Apple | N/A | ĐÃ XÁC MINH | Chỉ cần ánh xạ cổng USB (HS06) chính xác | Không cần kext riêng | `KHÔNG CẦN` | 🔲 |
| 19 | **USB Controller**| `8086:51ED` (PCH xHCI) | `USBToolBox.kext` + `UTBMap.kext` | [USBToolBox](https://github.com/USBToolBox/kext/releases) | BSD-3-Clause | 1.1.1 | ĐÃ XÁC MINH | Giới hạn 15 cổng USB của macOS | Nạp độc lập | `DÙNG` | 🔲 |

---

## 2. Thiết bị KHÔNG có driver khả thi (Cần vô hiệu hoá / Bỏ qua)

| Thiết bị | Hardware ID | Lý do kỹ thuật | Giải pháp xử lý |
|---|---|---|---|
| **dGPU NVIDIA RTX 3050 Ti Mobile** | `10DE:25A0` (GA107M) | Kiến trúc Ampere không có bất kỳ driver hoặc Metal support nào trên macOS. | Vô hiệu hoá hoàn toàn bằng ACPI `SSDT-dGPU-Off.aml` (gọi method `_OFF` tại `\_SB.PC00.PEG1.PEGP`). Tránh hao pin và lỗi sleep. |
| **NVIDIA HD Audio Controller** | `10DE:2291` | Nằm trên bo dGPU, phục vụ xuất âm thanh qua cổng HDMI ngoài. | Tự động tắt cùng dGPU khi ngắt nguồn PCIe bus `01:00.0`. |
| **Cổng xuất hình ngoài HDMI** | Physical HDMI Port | Nối trực tiếp bằng dây cứng (hard-wired) vào dGPU NVIDIA RTX 3050 Ti. | **Không thể xuất hình ngoài qua HDMI** ở Giai đoạn A. Màn hình ngoài chỉ có thể thử nghiệm qua Type-C (DP Alt Mode trên iGPU) nếu phần cứng hỗ trợ. |
| **Cảm biến vân tay** | Không trang bị | Phần cứng không có module vân tay. | Không áp dụng. |

---

## 3. Top 5 Rủi ro kỹ thuật lớn nhất

1. **Tính tương thích của Lilu & Kexts trên macOS 26 Tahoe (Darwin 25):**  
   *Tahoe là hệ điều hành rất mới.* Mọi kext dựa trên Lilu (`WhateverGreen`, `AppleALC`, `BlueToolFixup`, `CpuTopologyRebuild`) bắt buộc phải dùng boot-arg `-lilubetaall` để ép Lilu hook vào kernel Tahoe.
2. **Wi-Fi Intel AX211/AX210 trong môi trường cài đặt:**  
   `itlwm.kext` không chạy được trong môi trường macOS Recovery gốc. Do đó, bắt buộc phải dùng **bộ cài macOS Offline (Full Installer)** và chép ứng dụng `HeliPort.app` vào bộ cài/USB để mở mạng sau khi cài xong.
3. **Cơ chế hiển thị iGPU Tiger Lake Spoof:**  
   iGPU Alder Lake không có driver gốc. Việc spoof sang Tiger Lake (`0x9A49`) giúp màn hình eDP 1080p khởi động được GUI, nhưng chưa có tăng tốc đồ hoạ Metal 3 ở Giai đoạn A. Tốc độ khung hình giao diện có thể giật nhẹ trước khi sang Giai đoạn B (XeGfx).
4. **Xung đột Touchpad I2C & Ngắt GPIO:**  
   Bộ điều khiển GPIO trên laptop HP Alder Lake thường gặp lỗi định tuyến ngắt (Interrupt Pinning). Cần duy trì boot-arg `-vi2c-force-polling` như R1 đã chứng minh để touchpad nhận diện mượt mà mà không làm treo hệ thống.
5. **Cài song song (Dual Boot) với CachyOS trên cùng ổ 256GB:**  
   Ổ cứng SK hynix 256GB dung lượng tương đối khiêm tốn. Khi chia phân vùng APFS cạnh phân vùng Linux EXT4/BTRFS, nếu thao tác nhầm có thể làm hỏng bootloader GRUB/systemd-boot của Linux. Cần hướng dẫn kỹ người dùng chỉ co giãn phân vùng chứ không xoá bảng phân vùng.
