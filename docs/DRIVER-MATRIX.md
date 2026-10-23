# DRIVER-MATRIX — Bảng kiểm định Driver cho HP Victus 15-fa0xxx (macOS 26 Tahoe)

Quy tắc quyết định: DÙNG · ỨNG VIÊN · KHÔNG CÓ DRIVER · KHÔNG CẦN · BỎ QUA  
Cột **Tahoe** ghi: ĐÃ XÁC MINH hoặc CHƯA XÁC MINH TAHOE (theo quy định của skill driver-vetting).

---

## 1. Bảng ma trận kiểm định Driver chi tiết

| # | Thiết bị | Hardware ID (từ dump) | Driver / Kext ứng viên | Nguồn chính thức | License | Phiên bản dự kiến | Tahoe | Hạn chế đã biết | Phụ thuộc / Thứ tự nạp | Quyết định | Người dùng duyệt |
|---|---|---|---|---|---|---|---|---|---|---|:---:|
| 1 | **Nhân Kernel Patch** | CPU Alder Lake-H | Lilu.kext | [acidanthera/Lilu](https://github.com/acidanthera/Lilu) | BSD-3-Clause | 1.7.0 / mới nhất | ĐÃ XÁC MINH | Bắt buộc cho toàn bộ kext Acidanthera | Vị trí số 1 trong Kernel/Add | **DÙNG** | 🔲 |
| 2 | **Bộ mô phỏng SMC** | ACPI \_SB.PC00.LPCB | VirtualSMC.kext | [acidanthera/VirtualSMC](https://github.com/acidanthera/VirtualSMC) | BSD-3-Clause | 1.3.5 / mới nhất | ĐÃ XÁC MINH | Bắt buộc để khởi động macOS | Nạp ngay sau Lilu (Vị trí số 2) | **DÙNG** | 🔲 |
| 3 | **Đồ hoạ Framebuffer / Tắt dGPU** | 8086:46A3 (iGPU) + 10DE:25A0 (dGPU) | WhateverGreen.kext | [acidanthera/WhateverGreen](https://github.com/acidanthera/WhateverGreen) | BSD-3-Clause | 1.6.9 / mới nhất | ĐÃ XÁC MINH | Không tăng tốc Metal cho Xe; dGPU bị vô hiệu hoá | Nạp sau Lilu | **DÙNG** | 🔲 |
| 4 | **Âm thanh Codec** | Realtek ALC245 (10EC:0245) trên 8086:51C8 | AppleALC.kext | [acidanthera/AppleALC](https://github.com/acidanthera/AppleALC) | BSD-3-Clause | 1.9.3 / mới nhất | ĐÃ XÁC MINH | Cần thử layout-id (11, 13, 21, 22...) | Nạp sau Lilu | **DÙNG** | 🔲 |
| 5 | **Mạng Wi-Fi** | Intel Wi-Fi 6 AX210/AX211 (8086:2725) | itlwm.kext + HeliPort.app | [OpenIntelWireless/itlwm](https://github.com/OpenIntelWireless/itlwm) | GPL-2.0 | 2.3.0 / mới nhất | ĐÃ XÁC MINH | Không hoạt động trong Recovery; không AirDrop/Continuity | Không phụ thuộc Lilu | **DÙNG** | 🔲 |
| 6 | **Mạng Wi-Fi (Native)** | Intel AX210/AX211 (8086:2725) | AirportItlwm.kext | [OpenIntelWireless/itlwm](https://github.com/OpenIntelWireless/itlwm) | GPL-2.0 | 2.3.0 | CHƯA XÁC MINH TAHOE | Dễ gây kernel panic trên macOS 26 Tahoe do thay đổi IO80211 | Thay thế itlwm nếu dùng | **ỨNG VIÊN** | 🔲 |
| 7 | **Bluetooth Firmware** | Intel AX210 BT USB (8087:0032) | IntelBluetoothFirmware.kext | [OpenIntelWireless/IntelBluetoothFirmware](https://github.com/OpenIntelWireless/IntelBluetoothFirmware) | GPL-2.0 | 2.5.0 / mới nhất | ĐÃ XÁC MINH | Cần patcher đi kèm | Độc lập | **DÙNG** | 🔲 |
| 8 | **Bluetooth Patcher** | Intel AX210 BT USB (8087:0032) | IntelBTPatcher.kext | [OpenIntelWireless/IntelBluetoothFirmware](https://github.com/OpenIntelWireless/IntelBluetoothFirmware) | GPL-2.0 | 2.5.0 / mới nhất | ĐÃ XÁC MINH | Phục vụ patch descriptor cho Intel BT | Nạp sau Lilu | **DÙNG** | 🔲 |
| 9 | **Bluetooth Fixup Tahoe** | Bluetooth Framework macOS | BlueToolFixup.kext | [acidanthera/BrcmPatchRAM](https://github.com/acidanthera/BrcmPatchRAM) | GPL-2.0 | 2.6.9 / mới nhất | ĐÃ XÁC MINH | Bắt buộc cho macOS Monterey trở lên (Tahoe) | Nạp sau Lilu | **DÙNG** | 🔲 |
| 10 | **Ethernet LAN** | Realtek RTL8111/8168 (10EC:8168) | RealtekRTL8111.kext | [Mieze/RTL8111_driver_for_OS_X](https://github.com/Mieze/RTL8111_driver_for_OS_X) | GPL-2.0 | 2.4.2 / mới nhất | ĐÃ XÁC MINH | Ổn định, hỗ trợ Energy Efficient Ethernet | Độc lập | **DÙNG** | 🔲 |
| 11 | **Bàn phím PS/2** | AT Translated Set 2 (ACPI\PS2K) | VoodooPS2Controller.kext | [acidanthera/VoodooPS2](https://github.com/acidanthera/VoodooPS2) | BSD-3-Clause | 2.3.7 / mới nhất | ĐÃ XÁC MINH | Chỉ bật VoodooPS2Keyboard; tắt Mouse & Trackpad | Không phụ thuộc | **DÙNG** | 🔲 |
| 12 | **Touchpad I2C Core** | ELAN0788 (\_SB.PC00.I2C0.TPD0) | VoodooI2C.kext | [VoodooI2C/VoodooI2C](https://github.com/VoodooI2C/VoodooI2C) | GPL-3.0 | 2.8.1 / mới nhất | ĐÃ XÁC MINH | Quản lý bus I2C cho ELAN0788 | VoodooI2CServices + VoodooGPIO trước | **DÙNG** | 🔲 |
| 13 | **Touchpad I2C HID** | ELAN0788 (\_SB.PC00.I2C0.TPD0) | VoodooI2CHID.kext | [VoodooI2C/VoodooI2C](https://github.com/VoodooI2C/VoodooI2C) | GPL-3.0 | 2.8.1 / mới nhất | ĐÃ XÁC MINH | Cung cấp cử chỉ đa điểm mượt mà | Nạp sau VoodooI2C | **DÙNG** | 🔲 |
| 14 | **Quản lý Pin (Battery)** | HP Battery (\_SB.BAT0) | SMCBatteryManager.kext | [acidanthera/VirtualSMC](https://github.com/acidanthera/VirtualSMC) | BSD-3-Clause | 1.3.5 / mới nhất | ĐÃ XÁC MINH | Cần ECEnabler để đọc trường > 8 bit | Nạp sau VirtualSMC | **DÙNG** | 🔲 |
| 15 | **Hỗ trợ trường EC** | Embedded Controller EC0_ | ECEnabler.kext | [1Revenger1/ECEnabler](https://github.com/1Revenger1/ECEnabler) | BSD-3-Clause | 1.0.5 / mới nhất | ĐÃ XÁC MINH | Đọc trường pin 16/32-bit trong DSDT mà không cần patch | Nạp sau Lilu | **DÙNG** | 🔲 |
| 16 | **Tối ưu NVMe** | SK hynix BC711 NVMe (1C5C:174A) | NVMeFix.kext | [acidanthera/NVMeFix](https://github.com/acidanthera/NVMeFix) | BSD-3-Clause | 1.1.2 / mới nhất | ĐÃ XÁC MINH | Tránh lỗi panic khi sleep/wake và giảm nhiệt ổ | Nạp sau Lilu | **DÙNG** | 🔲 |
| 17 | **Đầu đọc thẻ SD** | Realtek RTS5288 (10EC:5228) | RealtekCardReader.kext | [0xFireWolf/RealtekCardReader](https://github.com/0xFireWolf/RealtekCardReader) | BSD-3-Clause | 0.9.7 / mới nhất | ĐÃ XÁC MINH | Hỗ trợ đọc ghi thẻ nhớ SD PCIe | Nạp trước Friend | **DÙNG** | 🔲 |
| 18 | **Đầu đọc thẻ Helper** | Realtek RTS5288 (10EC:5228) | RealtekCardReaderFriend.kext | [0xFireWolf/RealtekCardReaderFriend](https://github.com/0xFireWolf/RealtekCardReaderFriend) | BSD-3-Clause | 1.0.4 / mới nhất | ĐÃ XÁC MINH | Tích hợp biểu tượng thẻ vào macOS | Nạp sau Lilu & RealtekCardReader | **DÙNG** | 🔲 |
| 19 | **Điều phối CPU Alder Lake** | Intel Core i7-12650H (6P + 4E) | CpuTopologyRebuild.kext | [b00t0x/CpuTopologyRebuild](https://github.com/b00t0x/CpuTopologyRebuild) | BSD-3-Clause | 1.1.0 / mới nhất | ĐÃ XÁC MINH | Cải thiện hiệu năng đa nhân P/E trên macOS | Nạp sau Lilu | **DÙNG** | 🔲 |
| 20 | **Nhận diện CPU & OS** | Alder Lake CPUID / Tahoe UI | RestrictEvents.kext | [acidanthera/RestrictEvents](https://github.com/acidanthera/RestrictEvents) | BSD-3-Clause | 1.1.5 / mới nhất | ĐÃ XÁC MINH | Hiện đúng tên Intel Core i7 và hỗ trợ cập nhật | Nạp sau Lilu | **DÙNG** | 🔲 |
| 21 | **Phím độ sáng màn hình** | ACPI Hotkeys (INTC1070 / HP WMI) | BrightnessKeys.kext | [acidanthera/BrightnessKeys](https://github.com/acidanthera/BrightnessKeys) | BSD-3-Clause | 1.0.3 / mới nhất | ĐÃ XÁC MINH | Tự động nhận diện phím Fn chỉnh sáng | Nạp sau Lilu | **DÙNG** | 🔲 |
| 22 | **Định tuyến USB Port** | Alder Lake XHCI (8086:51ED) | USBToolBox.kext + UTBMap.kext | [USBToolBox/kext](https://github.com/USBToolBox/kext) | GPL-3.0 | 1.1.1 / mới nhất | ĐÃ XÁC MINH | Giới hạn 15 cổng USB; nhận diện cổng camera/BT | Độc lập | **DÙNG** | 🔲 |
| 23 | **Cảm biến nhiệt độ CPU** | Alder Lake P-cores / E-cores | SMCProcessor.kext | [acidanthera/VirtualSMC](https://github.com/acidanthera/VirtualSMC) | BSD-3-Clause | 1.3.5 | CHƯA XÁC MINH TAHOE | Có thể đọc sai sensor trên Alder Lake hybrid | Nạp sau VirtualSMC | **ỨNG VIÊN** | 🔲 |
| 24 | **Camera** | HP Wide Vision HD (30C9:0069) | AppleUSBVideoSupport (Native) | Có sẵn trong macOS | Apple EULA | Hệ thống | ĐÃ XÁC MINH | Nhận diện tự động qua UVC, không cần kext ngoài | Không | **KHÔNG CẦN** | 🔲 |
| 25 | **dGPU NVIDIA RTX 3050 Ti**| PCI\VEN_10DE&DEV_25A0 | Vô hiệu hoá qua SSDT + WEG | SSDT-dGPU-Off tự viết từ DSDT | ACPI ASL | Custom | ĐÃ XÁC MINH | Tắt nguồn hoàn toàn để tiết kiệm pin và tránh quá nhiệt | Chạy qua OpenCore ACPI | **BỎ QUA** | 🔲 |
| 26 | **Cảm biến vân tay** | Không trang bị | — | — | — | — | — | Máy không có phần cứng | Không | **KHÔNG CẦN** | 🔲 |
| 27 | **Cảm biến ánh sáng ALS** | Không trang bị | — | — | — | — | — | Máy không có phần cứng | Không | **KHÔNG CẦN** | 🔲 |

---

## 2. Thiết bị KHÔNG có driver khả thi trên macOS 26 Tahoe

| Thiết bị | Hardware ID | Lý do | Giải pháp thay thế |
|---|---|---|---|
| **NVIDIA GeForce RTX 3050 Ti Mobile** | PCI\VEN_10DE&DEV_25A0 | NVIDIA kiến trúc Ampere hoàn toàn không có driver hay framebuffer trên bất kỳ phiên bản macOS nào. | Vô hiệu hoá triệt để bằng SSDT-dGPU-Off (gọi phương thức ngắt nguồn _OFF) kết hợp boot-arg -wegnoegpu. Chấp nhận không xuất màn hình ngoài qua cổng HDMI nối trực tiếp dGPU. |
| **Intel Iris Xe Graphics (Tăng tốc Metal 3)** | PCI\VEN_8086&DEV_46A3 | Apple không bao giờ phát triển driver tăng tốc đồ hoạ Metal cho kiến trúc Intel Iris Xe (Alder Lake). | Giai đoạn A: Chạy chế độ hiển thị cơ bản (VESA/framebuffer không tăng tốc) để hệ thống hoạt động ổn định. Giai đoạn B: Thử nghiệm dự án XeGfx trong không gian người dùng / aux kernel collection. |

---

## 3. 5 Rủi ro kỹ thuật lớn nhất

1. **Không có kết nối mạng trong quá trình cài đặt (Recovery):**
   - Driver itlwm.kext chỉ hoạt động khi macOS đã khởi động vào môi trường người dùng (cần chạy cùng daemon và ứng dụng quản lý HeliPort). Môi trường macOS Recovery / Installer không có stack tương thích để nạp itlwm.
   - **Biện pháp xử lý:** Người dùng **bắt buộc phải tạo bộ cài macOS 26 Tahoe Offline (Full Installer USB)**, không dùng bộ cài Recovery/Online.
2. **Không sử dụng được màn hình rời qua cổng HDMI:**
   - Cổng HDMI vật lý của máy nối trực tiếp vào card rời NVIDIA RTX 3050 Ti. Khi tắt dGPU để đảm bảo thời lượng pin và kiểm soát nhiệt, cổng HDMI sẽ bị ngắt hoàn toàn.
   - **Biện pháp xử lý:** Sử dụng màn hình trong của máy cho công việc; kiểm tra cổng Type-C DisplayPort Alt-Mode ở các pha sau.
3. **Môi trường đồ hoạ iGPU không có tăng tốc phần cứng (QE/CI) trong Giai đoạn A:**
   - Vì chưa có Metal/QE/CI cho Alder Lake Iris Xe, giao diện macOS sẽ chạy bằng phần mềm (Software Rendering/VESA Framebuffer). Các hiệu ứng trong suốt (transparency), mượt cửa sổ và các phần mềm đồ hoạ nặng sẽ bị giật hoặc giới hạn.
   - **Biện pháp xử lý:** Đây là đặc tính dự kiến của Giai đoạn A để tập trung làm ổn định toàn bộ phần cứng còn lại trước khi bước vào Giai đoạn B (XeGfx).
4. **Touchpad I2C-HID có thể gặp lỗi ngắt (Interrupt) GPIO:**
   - Touchpad ELAN0788 yêu cầu cấu hình chân GPIO pin chính xác trong SSDT. Nếu chân pin bị sai, touchpad có thể không nhận cử chỉ hoặc làm đơ con trỏ chuột.
   - **Biện pháp xử lý:** Chuẩn bị sẵn cấu hình Polling Mode làm phương án dự phòng cho VoodooI2C nếu GPIO Interrupt gặp sự cố.
5. **Rủi ro xung đột bộ nhớ VT-d do bảng DMAR chứa RMRR:**
   - Bảng DMAR của HP Victus chứa vùng nhớ cố định RMRR ( x7c000000 - 0x803fffff), rất dễ gây Kernel Panic trong quá trình khởi tạo kernel nếu IOMMU được kích hoạt.
   - **Biện pháp xử lý:** Bắt buộc kích hoạt quirk DisableIoMapper = true trong config.plist.

---

## 4. Kế hoạch đưa HeliPort vào máy sau khi cài đặt thành công

Vì itlwm.kext chỉ giao tiếp Wi-Fi thông qua ứng dụng HeliPort.app, và sau khi cài đặt macOS xong máy chưa thể vào mạng:
1. Trong khi chuẩn bị USB cài đặt, sao chép sẵn file HeliPort.dmg hoặc thư mục HeliPort.app vào một phân vùng dữ liệu trên USB (hoặc ổ flash rời định dạng FAT32/ExFAT).
2. Sau khi cài đặt hoàn tất và đăng nhập vào màn hình Desktop macOS, cắm USB vào máy, mở phân vùng chứa HeliPort.app và kéo thả vào thư mục /Applications.
3. Mở HeliPort, cấp quyền trong System Settings > Privacy & Security, chọn mạng Wi-Fi và nhập mật khẩu để kích hoạt Internet.
4. Cài đặt HeliPort khởi động cùng hệ thống (Open at Login).
