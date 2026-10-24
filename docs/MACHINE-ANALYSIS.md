# MACHINE-ANALYSIS — Phân tích chi tiết phần cứng Máy B (HP Victus 15-fa0xxx)

*Ngày lập: 2026-10-24*  
*Mục tiêu: macOS 26 Tahoe (Darwin 25)*  
*Nguồn dữ liệu: laptop-specs.md, docs/hw-dump/ (trích xuất trực tiếp trên Máy B chạy CachyOS Linux x86_64).*

---

## 1. Tổng quan hệ thống Máy B

| Thành phần | Thông số chi tiết từ phần cứng thực tế (Máy B) |
|---|---|
| **Dòng máy / Model** | HP Victus by HP Gaming Laptop 15-fa0xxx |
| **SKU / Board ID** | SKU: `68Y11UA#ABA` — Board ID: `8A4F` (Version 37.56) |
| **BIOS Version / Date** | AMI UEFI `F.34` (Release: `03/19/2026`, Release ver: `15.34`) |
| **CPU** | Intel Core i7-12650H (Alder Lake-H / Alder Lake-P, 10 nhân: 6P + 4E, 16 luồng, stepping 3, microcode `0x43b`) |
| **Bộ nhớ RAM** | 24 GB DDR4 (1×16 GB G.Skill 3200 running @ 2400 MT/s + 1×8 GB OSCOO 2400 MT/s, Dual Channel 2400 MT/s) |
| **Đồ hoạ tích hợp (iGPU)** | Intel UHD / Iris Xe Graphics Alder Lake-P GT1 (`8086:46A3`, rev `0x0c`), kết nối eDP panel CMN1521 1920×1080 |
| **Đồ hoạ rời (dGPU)** | NVIDIA GeForce RTX 3050 Ti Mobile [GA107M] (`10DE:25A0`, rev `a1`, Ampere Optimus, subsystem `103C:8A4F`) |
| **Âm thanh (Audio)** | Realtek ALC245 (`10EC:0245`, subsystem `103C:8A4F`) trên Intel PCH-P HD Audio (`8086:51C8`) + NVIDIA HDMI (`10DE:2291`) |
| **Mạng không dây (Wi-Fi)** | Intel Wi-Fi 6 AX211 / AX210 160MHz (`8086:2725`, subsystem `8086:0024`) |
| **Bluetooth** | Intel AX210 / AX211 Bluetooth qua giao tiếp USB trong (`8087:0032`, Bus 003 Port 007) |
| **Mạng có dây (Ethernet)** | Realtek RTL8111/8168 PCI Express Gigabit Ethernet (`10EC:8168`, subsystem `103C:8A4F`) |
| **Ổ cứng lưu trữ (NVMe)** | SK hynix BC711 NVMe SSD 256GB (`1C5C:174A`, model `HFM256GD3JX013N`, firmware `HPS1`) |
| **Đầu đọc thẻ (Card Reader)** | Realtek RTS5288 PCIe SD UHS-I Card Reader (`10EC:5228`, subsystem `103C:8A4F`) |
| **Thiết bị nhập liệu (Input)** | Bàn phím PS/2 (`HPQ8001` / `AT Translated Set 2`) + Touchpad ELAN I2C HID (`04F3:321A`, `ELAN0788`) |
| **Camera & Cảm biến** | HP Wide Vision HD Camera UVC USB (`30C9:0069`); Không có cảm biến vân tay (Fingerprint); Không ALS rời |

---

## 2. Bảng kiểm kê chi tiết linh kiện & Đường dẫn phần cứng (Hardware ID Matrix)

| Nhóm thiết bị | Tên thiết bị / Model | Hardware ID (VEN:DEV / Subsystem) | ACPI Path / PCI Path | Driver Linux hiện tại | Trạng thái hỗ trợ trên macOS (Tahoe) | Ghi chú kỹ thuật |
|---|---|---|---|---|---|---|
| **CPU** | Intel Core i7-12650H | Family 6, Model 154 (`0x9A`), Step 3 | `\_SB.PR00` → `\_SB.PR15` | `intel_idle`, `coretemp` | Cần `SSDT-PLUG-ALT` + `CpuTopologyRebuild.kext` | Hybrid 6P+4E (16T). Cần SMBIOS `MacBookPro16,2` hoặc `MacBookPro16,4`. |
| **iGPU** | Intel Alder Lake-P GT1 | `8086:46A3` (Subsys `103C:8A4F`, Rev `0x0c`) | `\_SB.PC00.GFX0`<br>`PciRoot(0x0)/Pci(0x2,0x0)` | `i915` (CachyOS) | Spoof Tiger Lake (`0x9A49`) qua WhateverGreen (Giai đoạn A) | Màn hình eDP 1080p CMN1521. Chạy GUI recovery & VESA/TGL cơ bản. Giai đoạn B mới xét XeGfx. |
| **dGPU** | NVIDIA GeForce RTX 3050 Ti | `10DE:25A0` (Subsys `103C:8A4F`, Rev `a1`) | `\_SB.PC00.PEG1.PEGP`<br>`PciRoot(0x0)/Pci(0x1,0x0)/Pci(0x0,0x0)` | `nvidia` | **Không hỗ trợ macOS** — Cần vô hiệu hoá ở Giai đoạn A | Kiến trúc Ampere không có driver trên macOS. Tắt để tiết kiệm pin và tránh panic. |
| **dGPU Audio** | NVIDIA GA107 HDA | `10DE:2291` (Subsys `103C:8A4F`, Rev `a1`) | `\_SB.PC00.HDAS`<br>`PciRoot(0x0)/Pci(0x1,0x0)/Pci(0x0,0x1)` | `snd_hda_intel` | Vô hiệu hoá cùng dGPU | Gắn với cổng HDMI ngoài. |
| **HD Audio** | Intel Alder Lake PCH-P HDA | `8086:51C8` (Subsys `103C:8A4F`) | `\_SB.PC00.HDAS`<br>`PciRoot(0x0)/Pci(0x1f,0x3)` | `sof-audio-pci-intel-tgl` | Hỗ trợ qua `AppleALC.kext` | Điều khiển Realtek ALC245. |
| **Audio Codec** | Realtek ALC245 | Codec `10EC:0245` (Subsys `103C:8A4F`) | Node 0x14 (Spk), Node 0x21 (HP), Node 0x19 (Mic) | `snd_soc_avs` / ALSA | Hỗ trợ qua `AppleALC.kext` (layout-id: 11, 13, 21...) | Combo jack 3.5mm (Headphone out, Mic in) + Loa tích hợp. |
| **Wi-Fi** | Intel Wi-Fi 6E AX210/AX211 | `8086:2725` (Subsys `8086:0024`) | `\_SB.PC00.RP07.PXSX`<br>`PciRoot(0x0)/Pci(0x1c,0x6)/Pci(0x0,0x0)` | `iwlwifi` | Hỗ trợ tốt qua **`itlwm.kext` + HeliPort** | Theo yêu cầu PROMPT.md: dùng itlwm + HeliPort để kết nối Wi-Fi ổn định trên Tahoe. |
| **Bluetooth** | Intel AX210 Bluetooth USB | `8087:0032` (USB Interface) | `\_SB.PC00.XHCI.RHUB.HS07` (Bus 003 Port 007) | `btusb` | Hỗ trợ qua `IntelBluetoothFirmware.kext` + `BlueToolFixup.kext` | Tahoe yêu cầu BlueToolFixup cập nhật mới nhất. |
| **Ethernet** | Realtek RTL8111/8168 GBE | `10EC:8168` (Subsys `103C:8A4F`, Rev `0x16`) | `\_SB.PC00.RP09.PXSX`<br>`PciRoot(0x0)/Pci(0x1c,0x7)/Pci(0x0,0x0)` | `r8169` | Hỗ trợ hoàn hảo qua `RealtekRTL8111.kext` | Native-like stability cho kết nối mạng có dây. |
| **NVMe SSD** | SK hynix BC711 256GB | `1C5C:174A` (Model `HFM256GD3JX013N`, FW `HPS1`) | `\_SB.PC00.PEG0.PEGP`<br>`PciRoot(0x0)/Pci(0x6,0x0)/Pci(0x0,0x0)` | `nvme` | Hỗ trợ tốt qua `NVMeFix.kext` | Không bị lỗi freeze TRIM như Samsung PM9A1, quản lý nguồn tốt. |
| **Card Reader**| Realtek RTS5288 PCIe SD | `10EC:5228` (Subsys `103C:8A4F`, Rev `0x01`) | `\_SB.PC00.RP05.PXSX`<br>`PciRoot(0x0)/Pci(0x1c,0x0)/Pci(0x0,0x0)` | `rtsx_pci` | Hỗ trợ qua `RealtekCardReader.kext` + `RealtekCardReaderFriend.kext` | Đọc thẻ SD UHS-I. |
| **Bàn phím** | HP Standard PS/2 Keyboard | ACPI HID: `HPQ8001` (PNP `0001:0001`) | `\_SB.PC00.LPCB.PS2K` | `atkbd` / `i8042` | Hỗ trợ tốt qua `VoodooPS2Controller.kext` | Cần `VoodooPS2Keyboard.kext` và `BrightnessKeys.kext` cho phím Fn/độ sáng. |
| **Touchpad** | ELAN I2C HID Multi-touch | HID `04F3:321A`, ACPI HID `ELAN0788` | `\_SB.PC00.I2C0.TPD0` | `i2c_hid_acpi`, `hid-multitouch` | Hỗ trợ qua `VoodooI2C.kext` + `VoodooI2CHID.kext` | Chạy ở chế độ Polling qua boot-arg `-vi2c-force-polling` (đã kiểm chứng trên R1). |
| **Camera** | HP Wide Vision HD Camera | USB VID:PID `30C9:0069` | `\_SB.PC00.XHCI.RHUB.HS06` (Bus 003 Port 006) | `uvcvideo` | **Native (UVC OOB)** | Nhận diện camera FaceTime/PhotoBooth tiêu chuẩn qua USB mapping. |
| **USB Host #1**| Intel Alder Lake PCH xHCI | `8086:51ED` (Subsys `103C:8A4F`) | `\_SB.PC00.XHCI`<br>`PciRoot(0x0)/Pci(0x14,0x0)` | `xhci_hcd` | Hỗ trợ qua `USBToolBox.kext` + `UTBMap.kext` (hoặc `USBMap.kext`) | Cần map 15 port giới hạn trên macOS. |
| **USB Host #2**| Alder Lake Thunderbolt 4 | `8086:461E` (Rev `0x02`) | `\_SB.PC00.TXHC`<br>`PciRoot(0x0)/Pci(0xd,0x0)` | `xhci_hcd` | Hỗ trợ nhận diện cổng Type-C/USB-C | Điều khiển các cổng Type-C mặt bên. |
| **EC / Pin** | HP Embedded Controller / Li-ion | ACPI `PNP0C09` (`EC0_`), `PNP0C0A` (`BAT0`) | `\_SB.PC00.LPCB.EC0_`<br>`\_SB.BAT0` | `battery`, `ac` | Hỗ trợ qua `VirtualSMC.kext` + `SMCBatteryManager.kext` + `ECEnabler.kext` | Đọc phần trăm pin, trạng thái sạc và nhiệt độ ACPI. |
| **Đồng hồ RTC**| ACPI AWAC / RTC | ACPI HID `ACPI000E` (`AWAC`), `PNP0B00` (`RTC_`) | `\_SB.AWAC`<br>`\_SB.PC00.LPCB.RTC_` | `rtc_cmos` | Cần `SSDT-RTCAWAC.aml` | DSDT có cờ `STAS`. `SSDT-RTCAWAC` gán `STAS = 1` để bật `RTC_` và tắt `AWAC`. |
| **GPIO Controller**| Intel Alder Lake GPIO | ACPI HID `INTC1055` | `\_SB.GPI0` | `pinctrl_alderlake` | Cần `SSDT-GPI0.aml` | Kích hoạt controller GPIO cho touchpad và sensor. |
| **TPM** | TPM 2.0 Device | ACPI HID `MSFT0101` | `\_SB.TPM_` | `tpm_crb` | Không cần driver trên macOS | Không ảnh hưởng đến macOS boot. |
| **Vân tay** | Không trang bị | Không tìm thấy | N/A | N/A | Không có | Xác nhận không có thiết bị vân tay trên model này. |

---

## 3. Cấu hình BIOS & Trạng thái Firmware

Dựa trên phân tích từ `firmware-options.txt`, ACPI tables và nhật ký kernel CachyOS:

1. **VT-d (Intel Virtualization for Directed I/O):**
   * Bảng `DMAR` tồn tại tại địa chỉ `0x6e9ad000` (kích thước 136 bytes).
   * Kernel log: `DMAR-IR: Enabled IRQ remapping in x2apic mode`, `DMAR: Skip IOMMU disabling for graphics`.
   * **Khuyến nghị cho OpenCore:** Bật `Kernel > Quirks > DisableIoMapper = False` kết hợp với boot-arg hoặc xóa DMAR reserved memory nếu cần; an toàn nhất lúc đầu là để `DisableIoMapper = False` hoặc `True` tùy thuộc vào `VT-d` trong BIOS.
2. **Above 4G Decoding:**
   * Trong R1 (cùng BIOS F.34), Above 4G Decoding được mặc định bật (`Enabled`).
   * **Khuyến nghị OpenCore:** Bật `Booter > Quirks > EnableWriteUnprotector = False`, `RebuildAppleMemoryMap = True`, `SetupVirtualMap = True`.
3. **CFG Lock (MSR 0xE2):**
   * Chưa đọc được giá trị thanh ghi trực tiếp (do thiếu tool msr-tools trên môi trường live).
   * **Khuyến nghị OpenCore:** Bật an toàn `AppleCpuPmCfgLock = True` và `AppleXcpmCfgLock = True` trong `Kernel > Quirks` để chống kernel panic khởi động nếu BIOS khóa MSR 0xE2.
4. **DVMT Pre-Allocated:**
   * Laptop HP thường cố định DVMT ở mức 32MB hoặc 64MB trong BIOS không cho chỉnh.
   * Cần cấu hình framebuffer patch (`framebuffer-fbmem` / `framebuffer-stolenmem`) nếu DVMT < 64MB.
5. **Secure Boot:**
   * BẮT BUỘC TẮT (`Disabled`) trong BIOS khi cài đặt và boot OpenCore.
6. **Chế độ GPU (Optimus / Hybrid):**
   * Giữ nguyên chế độ Hybrid (iGPU lái eDP panel). Không chuyển sang chế độ dGPU-only trong BIOS (vì dGPU không hỗ trợ macOS).

---

## 4. Đối chiếu toàn diện giữa Máy B và Reference R1 (`victus-15-fa0xxx-hackintosh`)

| Hạng mục so sánh | Repo tham chiếu R1 (`sulthonuladib`) | Máy B của tôi (Target Machine) | Ý nghĩa kỹ thuật & Điều chỉnh cần thiết |
|---|---|---|---|
| **Board ID & BIOS** | Board `8A4F`, BIOS `F.34` (Release `03/19/2026`) | Board `8A4F`, BIOS `F.34` (Release `03/19/2026`) | **Trùng khớp 100%**. Kiến trúc bo mạch chủ, bảng ACPI, đường dẫn PCIe cơ bản hoàn toàn giống nhau. |
| **CPU Model** | Core i7-12700H (14C/20T: 6P + 8E) | Core i7-12650H (10C/16T: 6P + 4E) | Cùng vi kiến trúc Alder Lake-H. Khác số lượng E-cores (4E vs 8E). Cả hai đều dùng chung giải pháp `SSDT-PLUG-ALT` + `CpuTopologyRebuild.kext`. |
| **iGPU Device ID** | `8086:46A6` (GT2 Iris Xe, 96 EU) | `8086:46A3` (GT1 UHD Graphics, 64 EU) | Khác Device ID nhưng cùng vi kiến trúc Gen 12 (Alder Lake-P). Đều áp dụng công thức Tiger Lake spoof (`0x9A49`) qua `WhateverGreen` thành công. |
| **dGPU Model** | NVIDIA RTX 3050 Mobile (`10DE:25A2`) | NVIDIA RTX 3050 Ti Mobile (`10DE:25A0`) | Đều là Ampere Mobile (GA107), chung đường dẫn ACPI `\_SB.PC00.PEG1.PEGP`. Đều không có driver macOS → Vô hiệu hóa ở Giai đoạn A. |
| **Wi-Fi Chipset** | MediaTek MT7921 (`14C3:7961`) — *Hạn chế* | **Intel Wi-Fi 6 AX211 / AX210** (`8086:2725`) | **Máy B vượt trội**: Wi-Fi Intel được hỗ trợ chính thức bởi `itlwm.kext` + ứng dụng `HeliPort`, không cần driver thử nghiệm như MTK. |
| **Bluetooth Chipset**| MediaTek MT7921 Bluetooth USB (`13D3:3567`) | **Intel AX210 Bluetooth USB** (`8087:0032`) | **Máy B vượt trội**: Được hỗ trợ ổn định bằng `IntelBluetoothFirmware.kext` + `BlueToolFixup.kext`. |
| **Ổ cứng NVMe** | Samsung PM9A1 (`144D:A80A`) | **SK hynix BC711 256GB** (`1C5C:174A`) | R1 gặp lỗi TRIM timeout nặng với PM9A1 (phải đặt `SetApfsTrimTimeout = 0`). Máy B dùng Hynix BC711 chạy mượt với `NVMeFix.kext`. |
| **Audio Codec** | Realtek ALC245 (chưa hoàn thiện trên R1) | Realtek ALC245 (`10EC:0245`) đầy đủ dump | Đã trích xuất đầy đủ Pin Complex (Node 0x14 loa, Node 0x21 tai nghe, Node 0x19 mic). Dùng AppleALC layout-id thích hợp. |
| **Bàn phím & Touchpad**| PS/2 Keyboard + ELAN I2C Trackpad (`04F3:321A`) | PS/2 Keyboard + ELAN I2C Trackpad (`04F3:321A`) | **Trùng khớp 100%**. Hoạt động tốt với `VoodooPS2Controller` + `VoodooI2C` (với `-vi2c-force-polling`). |
| **Target OS** | macOS 15 Sequoia (Darwin 24) | **macOS 26 Tahoe (Darwin 25)** | Cần chú ý tính tương thích của Lilu, AppleALC, VoodooI2C và BlueToolFixup trên phiên bản macOS Tahoe mới. |

---

## 5. Danh sách thông tin cần hỏi / Xác nhận từ người dùng

1. **Tùy chọn BIOS Setup:**
   * Trong menu BIOS (F10 khi khởi động), bạn đã tắt **Secure Boot** chưa?
   * Có tùy chọn **CFG Lock** hoặc **VT-d** trong BIOS không? *(Nếu BIOS HP bị ẩn, OpenCore sẽ bật quirk bù đắp).*
2. **Kế hoạch phân vùng ổ đĩa:**
   * Ổ SK hynix BC711 (256GB) hiện đang cài CachyOS. Bạn dự định cài macOS Tahoe song song (dual boot) hay dùng một ổ đĩa riêng / phân vùng riêng?
   * *Khuyến cáo an toàn:* Không format hay xoá phân vùng Linux khi chưa sao lưu.

---

## 6. Đề xuất sơ bộ cho Pha 1 (Driver Vetting)

Dựa trên bảng phân tích phần cứng Máy B:
1. **Core Kexts:** `Lilu`, `VirtualSMC`, `WhateverGreen`, `AppleALC`, `CpuTopologyRebuild`, `RestrictEvents`.
2. **Sensors / EC:** `SMCBatteryManager`, `SMCProcessor`, `ECEnabler` (cho EC HP `EC0_`).
3. **Storage:** `NVMeFix.kext`.
4. **Input:** `VoodooPS2Controller` (Keyboard), `VoodooI2C` + `VoodooI2CHID` + `VoodooGPIO` (Touchpad ELAN0788).
5. **Network:** `RealtekRTL8111.kext` (LAN), `itlwm.kext` + `HeliPort.app` (Wi-Fi Intel AX211/AX210).
6. **Bluetooth:** `IntelBluetoothFirmware.kext` + `BlueToolFixup.kext` (v2.6.9+ tương thích Tahoe).
7. **ACPI Hotpatches cần thiết:**
   * `SSDT-EC.aml` (Fake EC device)
   * `SSDT-PLUG-ALT.aml` (Cấu hình CPU Alder Lake `_SB.PR00`)
   * `SSDT-RTCAWAC.aml` (Sửa xung nhịp AWAC thành RTC, set `STAS = 1`)
   * `SSDT-USB-Reset.aml` & `SSDT-USBX.aml` (Cấp nguồn USB)
   * `SSDT-GPI0.aml` (Kích hoạt GPIO cho touchpad)
   * `SSDT-dGPU-Off.aml` (Vô hiệu hoá dGPU RTX 3050 Ti qua method `_OFF` tại `\_SB.PC00.PEG1.PEGP`)
