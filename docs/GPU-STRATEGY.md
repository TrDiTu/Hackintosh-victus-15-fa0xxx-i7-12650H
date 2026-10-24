# GPU-STRATEGY — Chiến lược Xử lý Đồ hoạ (iGPU & dGPU) trên HP Victus 15-fa0xxx

*Dự án: Hackintosh macOS 26 Tahoe trên nền tảng Intel Alder Lake-H*  
*Giai đoạn áp dụng: Giai đoạn A — Dựng EFI nền ổn định (CHƯA dùng XeGfx)*

---

## 1. Mục tiêu chiến lược (Giai đoạn A)

1. **Hiển thị giao diện người dùng hoàn chỉnh:** Màn hình laptop nội bộ (eDP panel 1920×1080) phải khởi động trực tiếp vào giao diện đồ họa (macOS Recovery GUI và macOS Installer), vượt qua điểm nghẽn đóng băng màn hình đen kinh điển `IOConsoleUsers: gIOScreenLockState 3`.
2. **Triệt để ngắt nguồn dGPU không tương thích:** Vô hiệu hóa hoàn toàn card đồ họa rời NVIDIA GeForce RTX 3050 Ti ở mức ACPI để tiết kiệm pin (tránh lãng phí 15–25W điện năng tiêu thụ ngầm), giảm nhiệt độ máy và loại bỏ triệt để nguy cơ kernel panic khi Sleep / Wake.
3. **Tuân thủ nghiêm ngặt cổng chặn an toàn:** **TUYỆT ĐỐI KHÔNG nạp `XeGfx.kext` vào EFI** trong Giai đoạn A. Chỉ tập trung tối đa vào độ ổn định của hệ thống trước khi bước sang giai đoạn thử nghiệm tăng tốc đồ hoạ chuyên sâu (Giai đoạn B).

---

## 2. Phân tích hiện trạng phần cứng đồ hoạ (Máy B)

| Thuộc tính | Đồ hoạ tích hợp (iGPU) | Đồ hoạ rời (dGPU) |
|---|---|---|
| **Tên vi xử lý đồ họa** | Intel Alder Lake-P GT1 UHD Graphics (64 EUs) | NVIDIA GeForce RTX 3050 Ti Mobile [GA107M] |
| **PCI Hardware ID** | Vendor: `0x8086`, Device: `0x46A3`, Rev: `0x0C` | Vendor: `0x10DE`, Device: `0x25A0`, Rev: `0xA1` |
| **PCI Subsystem ID** | `103C:8A4F` (HP) | `103C:8A4F` (HP) |
| **Đường dẫn PCI Bus** | `PciRoot(0x0)/Pci(0x2,0x0)` | `PciRoot(0x0)/Pci(0x1,0x0)/Pci(0x0,0x0)` |
| **Đường dẫn ACPI** | `\_SB.PC00.GFX0` | `\_SB.PC00.PEG1.PEGP` |
| **Cổng kết nối vật lý** | Điều khiển trực tiếp màn hình laptop eDP panel 1080p | Kết nối cứng (hard-wired) tới cổng HDMI ngoài |
| **Trạng thái driver macOS** | Không có driver gốc của Apple cho Gen 12 Alder Lake | Không có bất kỳ driver macOS nào cho kiến trúc Ampere |

---

## 3. Chiến lược iGPU: Giả lập Tiger Lake (0x9A49 Spoof)

### 3.1. Cơ sở kỹ thuật
Apple ngừng ra mắt máy Mac chạy vi xử lý Intel sau thế hệ thứ 10 (Comet Lake / Ice Lake), chỉ hỗ trợ một phần mã driver của Tiger Lake (Gen 11 / Xe-LP) trong các bản dựng thử nghiệm nội bộ. Vi kiến trúc Intel Gen 12 (Alder Lake-P GT1/GT2) có tập lệnh ISA đồ hoạ tương tự vi kiến trúc Gen 11 (Tiger Lake GT2).

Bằng cách sử dụng kext **`WhateverGreen.kext`** để giả lập mã thiết bị Alder Lake `0x46A3` thành Tiger Lake `0x9A49`, macOS sẽ nhận diện iGPU như một chip Iris Xe thế hệ 11, khởi tạo framebuffer và tải giao diện đồ hoạ WindowServer một cách mượt mà.

### 3.2. Bảng cấu hình DeviceProperties chi tiết cho `PciRoot(0x0)/Pci(0x2,0x0)`

Dưới đây là 11 khóa thuộc tính bắt buộc, đã được chứng minh thực tế và kiểm chứng thành công trên mẫu tham chiếu R1:

| Tên thuộc tính (Property Key) | Kiểu dữ liệu | Giá trị Hex / Chuỗi | Ý nghĩa kỹ thuật & Giải thích |
|---|---|---|---|
| `device-id` | Data | `<49 9A 00 00>` | Giả lập Device ID thành `0x9A49` (Intel Tiger Lake-LP GT2 Iris Xe Graphics). |
| `AAPL,ig-platform-id` | Data | `<00 00 49 9A>` | Khởi tạo framebuffer profile cho Tiger Lake Mobile (ID: `0x9A490000`). |
| `framebuffer-patch-enable` | Data | `<01 00 00 00>` | Kích hoạt chu trình can thiệp và vá các kết nối đầu ra màn hình của WhateverGreen. |
| `force-online` | Data | `<01 00 00 00>` | Ép pipeline hiển thị coi màn hình eDP luôn kết nối, không chờ tín hiệu handshake EDID. |
| `complete-modeset` | Data | `<01 00 00 00>` | Buộc hệ điều hành thiết lập lại chế độ hiển thị trọn vẹn thay vì kế thừa framebuffer của UEFI GOP (nguyên nhân chính gây đen màn hình). |
| `enable-max-pixel-clock-override`| Data | `<01 00 00 00>` | Vượt qua giới hạn xung nhịp pixel mặc định của driver, hỗ trợ độ phân giải 1080p ổn định. |
| `rps-control` | Data | `<01 00 00 00>` | Cho phép điều khiển trạng thái năng lượng kết xuất (Render Power States) của iGPU. |
| `hda-gfx` | String | `onboard-1` | Định danh kênh âm thanh số gắn liền với bộ điều khiển đồ hoạ tích hợp. |
| `built-in` | Data | `<00>` | Khai báo thiết bị PCIe nội bộ bắt buộc đối với nhân đồ hoạ tích hợp. |
| `AAPL,slot-name` | String | `built-in` | Gán nhãn nhận diện vị trí khe cắm nội bộ cho macOS System Profiler. |
| `model` | String | `Intel Iris Xe Graphics` | Tên hiển thị mỹ quan trong mục *About This Mac*. |

---

## 4. Chiến lược dGPU: Vô hiệu hoá Triệt để (Power Down via ACPI)

### 4.1. Nguy cơ khi để dGPU hoạt động tự do
1. **Tiêu hao năng lượng:** RTX 3050 Ti tiêu thụ 15W đến 30W ở chế độ chờ (idle) nếu không được quản lý năng lượng, khiến máy nóng ran và pin cạn kiệt chỉ sau 45–60 phút.
2. **Mất ổn định hệ thống:** Driver không tồn tại khiến kernel macOS liên tục thăm dò các thanh ghi PCI không phản hồi, gây treo máy hoặc panic ngẫu nhiên khi vào chế độ ngủ (Sleep).

### 4.2. Phương thức vô hiệu hoá ACPI (`SSDT-dGPU-Off.aml`)
Dựa trên phân tích bảng ACPI `DSDT.aml` và `SSDT14.aml` của Máy B:
- Đường dẫn thiết bị: `\_SB.PC00.PEG1.PEGP`
- Phương thức ngắt nguồn gốc tồn tại trong BIOS: `\_SB.PC00.PEG1.PEGP._OFF()`
- **Giải pháp SSDT:** Xây dựng bảng `SSDT-dGPU-Off.aml` định nghĩa phương thức `_INI` dưới khối `\_SB.PC00.PEG1.PEGP`. Khi kiểm tra `_OSI("Darwin")` trả về đúng, phương thức sẽ ngay lập tức thực thi lệnh `_OFF()` để cắt điện hoàn toàn bus PCIe `01:00.0`.
- **Bổ trợ:** Thêm boot-arg `-wegnoegpu` trong NVRAM để WhateverGreen bỏ qua card rời nếu có xung đột phát sinh.

### 4.3. Ảnh hưởng đến cổng xuất hình ngoài (HDMI)
- **Thực tế phần cứng:** Cổng HDMI vật lý ở cạnh máy được đấu dây trực tiếp (hard-wired) vào RTX 3050 Ti GA107M.
- **Hệ quả ở Giai đoạn A:** Khi dGPU bị ngắt nguồn, **cổng HDMI sẽ hoàn toàn không hoạt động**. Mọi nhu cầu hiển thị ngoài tạm thời chưa khả dụng cho đến khi thử nghiệm các giải pháp DisplayPort qua USB-C hoặc chuyển sang Giai đoạn B.

---

## 5. Ranh giới an toàn trước Giai đoạn B (XeGfx Gate)

```
+-----------------------------------------------------------------------------------+
|                           RANH GIỚI BẮT BUỘC (STAGE GATE)                         |
+-----------------------------------------------------------------------------------+
|  [Giai đoạn A: EFI nền hoàn chỉnh]                                                 |
|  - iGPU: Chạy Tiger Lake Spoof (0x9A49) — Hiển thị mượt 1080p, không có Metal 3    |
|  - dGPU: Ngắt nguồn ACPI hoàn toàn                                                |
|  - XeGfx.kext: TUYỆT ĐỐI KHÔNG NẠP VÀO EFI                                       |
|                                                                                   |
|         ↓ (Chỉ chuyển tiếp khi Người dùng xác nhận:                               |
|            "EFI nền đã ổn định, bắt đầu XeGfx")                                   |
|                                                                                   |
|  [Giai đoạn B: XeGfx Metal Acceleration]                                          |
|  - Stage 1: Kiểm tra môi trường & công cụ biên dịch XeGfx trên macOS             |
|  - Stage 2: Nạp kext động qua kextload ở userspace (KHÔNG nhét vào OpenCore)     |
|  - Stage 3: Phân tích log XeGfx debug & đánh giá mức tăng tốc Metal               |
+-----------------------------------------------------------------------------------+
```
