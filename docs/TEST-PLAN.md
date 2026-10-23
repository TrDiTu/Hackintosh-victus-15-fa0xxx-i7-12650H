# TEST-PLAN — Kế hoạch kiểm thử EFI OpenCore trên MÁY B (HP Victus 15-fa0xxx)

*Mục tiêu: Đưa macOS 26 Tahoe lên HP Victus 15-fa0xxx, kiểm thử toàn diện từng thiết bị phần cứng, đảm bảo hệ thống ổn định trước khi bước sang Giai đoạn B (XeGfx).*

---

## 1. Chuẩn bị trước khi khởi động

### 1.1. Sinh bộ số serial SMBIOS cho MÁY B
Trong EFI/OC/config.plist, các trường số serial đang để giá trị giữ chỗ CHANGE_ME_*. Trước khi cài đặt, bạn nên sinh bộ số serial riêng cho model MacBookPro16,1:
- Chạy lệnh sau trên máy A:
  `powershell
  tools\macserial.exe -m MacBookPro16,1 -g -n 1
  `
- Kết quả trả về dạng: Model | SerialNumber | BoardSerial (MLB) | SmUUID
- Nhập các giá trị này vào mục PlatformInfo > Generic trong file config.plist của bạn:
  - SystemSerialNumber: Thay thế CHANGE_ME_SERIAL
  - MLB: Thay thế CHANGE_ME_MLB
  - SystemUUID: Điền mã UUID vừa sinh (dạng XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX)
*(Lưu ý: Không gửi serial thật lên commit Git hoặc chia sẻ công khai).*

### 1.2. Kiểm tra lại thiết lập BIOS (Nhấn F10 khi bật máy)
- **Chế độ đồ hoạ:** Đảm bảo là **Hybrid / Optimus** (TUYỆT ĐỐI KHÔNG chọn dGPU-only / Discrete).
- **Secure Boot:** **Disabled** (Bắt buộc).
- **Fast Boot:** **Disabled**.
- **Chế độ ổ cứng (SATA/NVMe):** **AHCI** (Tắt Intel VMD / Intel RST nếu có).
- **Khởi động từ USB:** Bật USB Boot trong mục Boot Options.

---

## 2. Quy trình kiểm thử tuần tự theo từng giai đoạn

`
[Khởi động USB] ──► [Boot Installer] ──► [Cài đặt macOS] ──► [Test từng thiết bị] ──► [Test Sleep/Wake] ──► [Sẵn sàng XeGfx]
`

### Giai đoạn 1: Khởi động USB & Môi trường cài đặt (Installer)
1. Cắm USB cài đặt vào cổng USB-A của HP Victus.
2. Bật máy, nhấn liên tục phím **F9** để mở Boot Menu của HP.
3. Chọn dòng **UEFI: USB Drive...** (hoặc tên USB của bạn).
4. Menu OpenCore xuất hiện: Chọn mục **Install macOS Tahoe** (hoặc macOS Recovery).
5. **Quan sát verbose:** Dòng chữ chạy trên màn hình. Do đã bật -v và Target = 67:
   - Nếu khởi động thành công: Chữ dừng lại và chuyển sang giao diện cài đặt macOS đồ hoạ ở độ phân giải 1920x1080.
   - Nếu treo (hang/panic): Ghi nhận dòng lỗi cuối cùng và chụp ảnh màn hình lại.

---

### Giai đoạn 2: Phân vùng ổ đĩa & Cài đặt hệ điều hành
1. Tại màn hình cài đặt, chọn **Disk Utility** $\rightarrow$ Continue.
2. Bấm vào View ở góc trên bên trái, chọn **Show All Devices**.
3. Chọn ổ SSD **SK hynix BC711 NVMe SSD 256GB** (hoặc phân vùng bạn dành riêng cho macOS).
4. Bấm **Erase**:
   - **Name:** Macintosh HD (hoặc tên tuỳ ý).
   - **Format:** APFS.
   - **Scheme:** GUID Partition Map.
5. Đóng Disk Utility, chọn **Install macOS Tahoe** và làm theo hướng dẫn.
6. **Lưu ý quá trình cài đặt:**
   - Máy sẽ tự động khởi động lại từ 2 đến 3 lần.
   - Mỗi lần máy khởi động lại: Nhấn **F9**, chọn lại USB, và trong menu OpenCore chọn phân vùng mang tên **macOS Installer** (hoặc tên ổ cứng bạn vừa đặt) cho tới khi vào được màn hình thiết lập ban đầu (Setup Assistant).
   - Bạn có thể cắm trực tiếp dây mạng LAN vào cổng RJ45 (Realtek RTL8111) để có mạng Internet ngay trong lúc cài đặt.

---

### Giai đoạn 3: Bảng kiểm thử chức năng từng nhóm thiết bị (Pass / Fail Matrix)

Sau khi tạo tài khoản và vào màn hình Desktop chính của macOS, bạn hãy kiểm tra lần lượt từng mục sau:

| # | Nhóm phần cứng | Thao tác kiểm tra thực tế | Tiêu chí ĐẠT (Pass) | Trạng thái ghi nhận |
|---|---|---|---|:---:|
| 1 | **Màn hình nội bộ** | Quan sát giao diện Desktop, chỉnh độ phân giải trong System Settings. | Hiển thị đúng 1920x1080 gốc, màn hình sáng rõ, không sọc hình. | 🔲 Pass / 🔲 Fail |
| 2 | **Bàn phím PS/2** | Mở TextEdit hoặc Terminal, gõ tất cả các phím chữ, số, phím mũi tên. | Toàn bộ phím phản hồi chính xác, không bị dính phím. | 🔲 Pass / 🔲 Fail |
| 3 | **Phím Fn chỉnh sáng** | Bấm phím F2 / F3 (hoặc Fn+F2/Fn+F3) chỉnh độ sáng màn hình. | Thanh trượt độ sáng macOS xuất hiện và độ sáng thay đổi mượt mà. | 🔲 Pass / 🔲 Fail |
| 4 | **Touchpad ELAN0788** | Rê chuột 1 ngón, click chuột trái/phải; thử cuộn 2 ngón và vuốt 3 ngón. | Chuột di chuyển mượt mà, hỗ trợ cử chỉ đa điểm mượt mà. | 🔲 Pass / 🔲 Fail |
| 5 | **Mạng có dây (LAN)** | Cắm dây cáp mạng vào cổng RJ45 bên cạnh máy. | System Settings > Network hiện cổng Ethernet màu xanh, lướt web bình thường. | 🔲 Pass / 🔲 Fail |
| 6 | **Mạng Wi-Fi (itlwm)** | Mở file HeliPort.dmg từ USB, kéo HeliPort.app vào /Applications, mở app. | Biểu tượng Wi-Fi xuất hiện trên menu bar, quét thấy mạng và kết nối Internet tốt. | 🔲 Pass / 🔲 Fail |
| 7 | **Bluetooth (AX210)** | Mở System Settings > Bluetooth, dò tìm thiết bị xung quanh. | Bật/tắt Bluetooth bình thường, kết nối thử tai nghe/chuột BT thành công. | 🔲 Pass / 🔲 Fail |
| 8 | **Âm thanh (ALC245)** | Mở YouTube hoặc file nhạc nghe thử loa ngoài và cắm tai nghe 3.5mm. | Loa ngoài kêu rõ, cắm tai nghe tự chuyển kênh, micro thu âm hoạt động. | 🔲 Pass / 🔲 Fail |
| 9 | **Quản lý Pin & Sạc** | Rút sạc nguồn kiểm tra phần trăm pin; cắm sạc lại quan sát biểu tượng. | Phần trăm pin hiển thị đúng và nhảy số sạc khi cắm nguồn adapter. | 🔲 Pass / 🔲 Fail |
| 10 | **Ổ cứng NVMe SK hynix**| Tải Blackmagic Disk Speed Test chạy thử đo tốc độ đọc/ghi. | Tốc độ đạt chuẩn PCIe NVMe, nhiệt độ ổ đĩa ổn định, không đơ lag. | 🔲 Pass / 🔲 Fail |
| 11 | **Đầu đọc thẻ SD** | Cắm thử thẻ nhớ SD vào khe đọc thẻ bên cạnh máy. | Thẻ nhớ xuất hiện trên Finder, đọc ghi file bình thường. | 🔲 Pass / 🔲 Fail |
| 12 | **Camera HD** | Mở ứng dụng Photo Booth hoặc FaceTime. | Camera HP Wide Vision sáng đèn và hiển thị hình ảnh bình thường. | 🔲 Pass / 🔲 Fail |
| 13 | **Nhiệt độ & Quạt** | Sử dụng máy 15-20 phút, sờ vào khu vực bản lề và nghe tiếng quạt. | Máy ấm nhẹ, quạt quay êm, card rời RTX 3050 Ti đã ngắt điện hoàn toàn. | 🔲 Pass / 🔲 Fail |

---

### Giai đoạn 4: Kiểm thử Sleep / Wake & Ổn định dài hạn

1. **Thử nghiệm Sleep (Ngủ):**
   - Bấm vào biểu tượng Apple góc trái màn hình $\rightarrow$ Chọn **Sleep** (hoặc gập nắp máy).
   - Quan sát đèn báo nguồn bên cạnh máy: Đèn chuyển sang nhấp nháy chậm (thở) hoặc tắt hẳn, quạt ngừng quay hoàn toàn.
2. **Thử nghiệm Wake (Thức giấc):**
   - Nhấn phím cách (Space) hoặc mở nắp máy.
   - Màn hình phải bật sáng trở lại ngay lập tức, chuột và bàn phím phản hồi bình thường, kết nối mạng LAN/Wi-Fi tự phục hồi trong vòng 3-5 giây.
3. **Thử nghiệm Reboot & Shutdown liên tục:**
   - Khởi động lại (Restart) máy 3 lần.
   - Tắt hẳn máy (Shut Down) 2 lần.
   - Đảm bảo máy tắt nguồn dứt khoát, không bị treo ở màn hình đen trước khi tắt hẳn.

---

## 3. Cách thu thập log & Phương án phục hồi (Rollback)

### 3.1. Thu thập OpenCore Boot Log
- Do cấu hình Target = 67, mỗi lần khởi động OpenCore sẽ tự động tạo một file log dạng:
  EFI/opencore-YYYY-MM-DD-HHMMSS.txt trên phân vùng EFI của USB.
- Nếu xảy ra lỗi boot: Bạn cắm USB sang máy tính khác, mở phân vùng EFI và lấy file text mới nhất này gửi cho tôi phân tích.

### 3.2. Thu thập Kernel Panic Log
- Nếu gặp lỗi Kernel Panic sau khi đã vào macOS:
  - Khởi động lại máy vào macOS.
  - Mở Terminal chạy lệnh:
    `ash
    sudo dmesg > ~/Desktop/dmesg.txt
    `
  - Hoặc vào thư mục /Library/Logs/DiagnosticReports/, copy file có đuôi .panic ra USB.

### 3.3. Cách quay về Snapshot đã lưu (Rollback)
- Nếu một bản chỉnh sửa sau này gặp lỗi không boot được:
  - Bạn chỉ cần xoá thư mục EFI trên USB và chép lại thư mục EFI nằm trong:
    snapshots\build-01-20261024-041414-base-tahoe\EFI\
  - USB sẽ lập tức quay trở lại trạng thái của bản build gốc sạch sẽ nhất.

---

## 4. Mục "Sẵn sàng cho XeGfx" (Baseline Logging)

Trước khi chuyển sang Giai đoạn B (thử nghiệm kext XeGfx), bạn hãy mở Terminal trên macOS và chạy 2 lệnh sau để lưu lại thông số nền làm mốc đối chiếu:
`ash
# 1. Lưu lại cấu trúc cây thiết bị IORegistry của hệ thống
ioreg -l -p IODeviceTree > ~/Desktop/ioreg-baseline.txt

# 2. Lưu lại thông số nhận diện màn hình và iGPU hiện tại
system_profiler SPDisplaysDataType > ~/Desktop/displays-baseline.txt
`
*(File này sẽ giúp chúng ta đối chiếu xem XeGfx Stage 2 đọc thanh ghi có làm thay đổi hay xung đột với framebuffer nội bộ hay không).*

---

## 5. Bảng rà soát cấu hình config.plist (Validation Checklist)

- [x] **ACPI:** Đầy đủ 6 SSDT (SSDT-dGPU-Off, SSDT-AWAC, SSDT-EC-USBX, SSDT-PLUG-ALT, SSDT-PNLF, SSDT-SBUS-MCHC).
- [x] **Booter:** Bật AvoidRuntimeDefrag, DevirtualiseMmio, RebuildAppleMemoryMap, SetupVirtualMap.
- [x] **DeviceProperties:** Tắt dGPU RTX 3050 Ti (disable-gpu = 1), cấu hình framebuffer iGPU cơ bản và layout-id = 11 cho ALC245.
- [x] **Kernel Add:** 22 kexts sắp xếp đúng thứ tự phụ thuộc phân tầng (Lilu đứng đầu).
- [x] **Kernel Quirks:** Bật ProvideCurrentCpuInfo, DisableIoMapper, AppleCpuPmCfgLock, AppleXcpmCfgLock.
- [x] **Misc:** Debug Target = 67, SecureBootModel = Disabled, Vault = Optional.
- [x] **NVRAM:** boot-args có -v debug=0x100 -wegnoegpu revpatch=auto,sbvmm,cpuname alcid=11.
- [x] **PlatformInfo:** Model MacBookPro16,1, Generic update mode.
- [x] **UEFI:** Driver OpenRuntime.efi, OpenHfsPlus.efi, ResetNvramEntry.efi, ToggleSipEntry.efi.
