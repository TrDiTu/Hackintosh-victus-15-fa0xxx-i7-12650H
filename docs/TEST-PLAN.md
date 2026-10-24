# TEST-PLAN — Kế hoạch Kiểm thử EFI Nền (HP Victus 15-fa0xxx)

*Mục tiêu: Đánh giá độ ổn định của EFI nền `build-01` trên target macOS 26 Tahoe (Giai đoạn A)*  
*Quy tắc: Không ghi đè hay làm hỏng phân vùng CachyOS Linux hiện có.*

---

## 1. Chuẩn bị Trước khi Boot

1. **Sinh số Serial SMBIOS (Bắt buộc):**
   * Chạy công cụ `tools/macserial.exe` trên Máy A:
     ```powershell
     tools\macserial.exe -m MacBookPro16,2 -g -n 1
     ```
   * Mở file `EFI/OC/config.plist` (hoặc trên USB sau khi deploy) và thay thế:
     * `CHANGE_ME_SERIAL` $\rightarrow$ SerialNumber vừa sinh
     * `CHANGE_ME_MLB` $\rightarrow$ Board Serial (MLB) vừa sinh
     * `00000000-0000-0000-0000-000000000000` $\rightarrow$ sinh UUID mới (hoặc dùng `[guid]::NewGuid().ToString()`)
2. **Bộ cài macOS Tahoe Offline:**
   * Do `itlwm.kext` không hỗ trợ tải dữ liệu qua Recovery online, người dùng cần chuẩn bị bộ cài macOS Tahoe đầy đủ (Full Installer) trên phân vùng thứ hai của USB hoặc cài qua công cụ tạo bộ cài offline.
   * Sao chép ứng dụng `_cache/downloads/HeliPort.dmg` vào một USB phụ hoặc phân vùng dữ liệu để cài đặt sau khi vào Desktop.
3. **Cấu hình BIOS Máy B:**
   * Nhấn `F10` khi khởi động để vào BIOS Setup:
     * **Secure Boot:** Chuyển sang `Disabled`.
     * **Fast Boot:** Chuyển sang `Disabled` (nếu có).
     * **Card đồ hoạ:** Giữ nguyên chế độ Hybrid (không chọn dGPU-only).

---

## 2. Trình tự Kiểm thử Từng bước (Step-by-Step Test Sequence)

### Giai đoạn 1: Khởi động Bộ cài & Cài đặt Hệ điều hành
- [ ] **Test 1.1: Boot OpenCore Picker**
  - Cắm USB vào cổng USB 3.0 bên phải, nhấn `F9` để chọn boot từ USB (UEFI OpenCore).
  - *Tiêu chuẩn Đạt:* OpenCore Picker hiển thị rõ ràng các phân vùng (Install macOS, CachyOS, Reset NVRAM).
- [ ] **Test 1.2: Vượt qua Kernel & Handover đồ hoạ**
  - Chọn `Install macOS`. Dòng log verbose (`-v`) chạy mượt, không bị đứng tại `ACPI Error`, `PCI Configuration Begin` hoặc `IOConsoleUsers: gIOScreenLockState 3`.
  - *Tiêu chuẩn Đạt:* Màn hình laptop eDP 1080p sáng lên và chuyển thành công vào giao diện đồ họa Recovery GUI của macOS.
- [ ] **Test 1.3: Thao tác Bàn phím & Touchpad trong Bộ cài**
  - Kiểm tra di chuyển con trỏ bằng Touchpad ELAN và gõ phím trong Terminal.
  - *Tiêu chuẩn Đạt:* Touchpad rê mượt (nhờ polling `-vi2c-force-polling`), phím gõ nhận ký tự bình thường.
- [ ] **Test 1.4: Phân vùng ổ cứng an toàn (Disk Utility)**
  - Mở `Disk Utility` $\rightarrow$ `View` $\rightarrow$ `Show All Devices`.
  - **CHÚ Ý CỰC KỲ QUAN TRỌNG:** Tuyệt đối **KHÔNG chọn Erase cả ổ cứng** `SK hynix BC711` (vì đang chứa hệ điều hành Linux CachyOS).
  - Chọn phân vùng trống đã thu nhỏ trước đó hoặc bấm dấu `+` để thêm một phân vùng APFS mới (đặt tên ví dụ: `Macintosh HD`).
  - *Tiêu chuẩn Đạt:* Phân vùng APFS được tạo mà không ảnh hưởng tới các phân vùng EXT4/BTRFS của Linux.
- [ ] **Test 1.5: Tiến hành Cài đặt macOS**
  - Chạy `Install macOS`, chọn phân vùng APFS vừa tạo. Máy sẽ tự khởi động lại 2–3 lần.
  - *Tiêu chuẩn Đạt:* Hoàn tất thiết lập ban đầu (Setup Assistant) và vào màn hình Desktop chính.

---

### Giai đoạn 2: Kiểm tra Độc lập Từng nhóm Thiết bị (DRIVER-MATRIX Pass/Fail)

| Nhóm thiết bị | Thiết bị & Driver | Phương pháp kiểm tra thực tế trên Máy B | Tiêu chí Đạt (Pass) |
|---|---|---|---|
| **Đồ hoạ iGPU** | Alder Lake GT1 (`WhateverGreen`, TGL 0x9A49) | Vào *About This Mac* $\rightarrow$ Displays. | Nhận diện 1920×1080, màu sắc chuẩn, không sọc hình. |
| **Đồ hoạ dGPU** | RTX 3050 Ti (`SSDT-dGPU-Off`) | Chạy terminal: `ioreg -p IODeviceTree -l \| grep -i PEGP`. | Không thấy node driver NVIDIA gắn vào; máy mát, quạt chạy êm. |
| **Bàn phím & Fn** | HP PS/2 (`VoodooPS2Keyboard` + `BrightnessKeys`) | Gõ văn bản; nhấn phím Fn chỉnh sáng màn hình (F2/F3). | Bàn phím nhạy, thanh trượt độ sáng màn hình phản hồi mượt. |
| **Touchpad I2C** | ELAN0788 (`VoodooI2C` + `VoodooI2CHID`) | Thao tác 1 ngón, 2 ngón cuộn trang trong Safari, chạm click. | Con trỏ rê chính xác, cuộn 2 ngón mượt mà. |
| **Mạng có dây** | Realtek RTL8111 (`RealtekRTL8111.kext`) | Cắm dây cáp mạng LAN RJ45 vào cổng mạng. | Nhận diện cổng Ethernet, có IP và truy cập web tốc độ cao. |
| **Mạng Wi-Fi** | Intel AX211/AX210 (`itlwm` + `HeliPort`) | Mở ứng dụng `HeliPort.app`, quét mạng Wi-Fi và nhập mật khẩu. | Kết nối thành công mạng Wi-Fi, ping ổn định. |
| **Bluetooth** | Intel AX210 USB (`IntelBluetoothFirmware` + `BlueToolFixup`) | Mở System Settings $\rightarrow$ Bluetooth; kết nối tai nghe hoặc chuột. | Bật/Tắt Bluetooth bình thường, ghép nối và truyền âm thanh ổn định. |
| **Âm thanh (Audio)**| Realtek ALC245 (`AppleALC` layout-id 11) | Mở YouTube hoặc file nhạc; cắm jack tai nghe 3.5mm; thử ghi âm mic. | Loa trong phát rõ, tự chuyển khi cắm tai nghe, mic thu âm tốt. |
| **Pin & Quản lý nguồn**| HP EC / Battery (`SMCBatteryManager` + `ECEnabler`) | Rút sạc AC; cắm sạc AC; quan sát biểu tượng pin trên thanh menu. | Hiện chính xác phần trăm pin, nhận diện trạng thái Đang sạc / Dùng pin. |
| **Ổ cứng NVMe** | SK hynix BC711 (`NVMeFix.kext`) | Mở System Information $\rightarrow$ NVMExpress. | Nhận diện đúng model NVMe, không có lỗi I/O stall. |
| **Camera** | HP Wide Vision HD (`AppleUSBHost`) | Mở ứng dụng Photo Booth hoặc FaceTime. | Camera hiển thị hình ảnh rõ nét không cần cài kext ngoài. |

---

### Giai đoạn 3: Kiểm thử Chế độ Ngủ (Sleep / Wake) & Khởi động lại
- [ ] **Sleep Test:**
  - Bấm Apple Menu $\rightarrow$ `Sleep` (hoặc gập nắp màn hình).
  - *Quan sát:* Màn hình tắt, đèn bàn phím tắt, đèn báo nguồn nhấp nháy chậm (trạng thái Deep Sleep S3/Modern Standby).
- [ ] **Wake Test:**
  - Nhấn phím cách hoặc mở nắp màn hình.
  - *Tiêu chuẩn Đạt:* Màn hình sáng lại trong vòng 1–2 giây, bàn phím và touchpad hoạt động ngay lập tức, Wi-Fi tự kết nối lại.
- [ ] **Reboot Test (Kiểm tra lỗi HP 005):**
  - Khởi động lại máy 3 lần liên tiếp.
  - *Tiêu chuẩn Đạt:* Không xuất hiện thông báo lỗi `CMOS Reset 005` của BIOS HP khi bật lại máy.

---

## 3. Thu thập Dữ liệu & Mốc đối chiếu cho XeGfx (Giai đoạn B)

Sau khi EFI nền đạt toàn bộ các bài kiểm tra trên, người dùng chạy các lệnh sau trong Terminal macOS và lưu kết quả vào thư mục `logs/` làm **mốc so sánh (baseline)** trước khi bắt đầu thử nghiệm XeGfx:

```bash
# 1. Trạng thái iGPU và Display Framebuffer
ioreg -l -p IODeviceTree | grep -A 20 -i "GFX0" > logs/baseline-ioreg-igpu.txt

# 2. Toàn bộ cây thiết bị PCI
lspci -nnvv > logs/baseline-lspci.txt 2>/dev/null || system_profiler SPPCIDataType > logs/baseline-pci.txt

# 3. Trạng thái các kext đã nạp
kextstat | grep -v "com.apple" > logs/baseline-kextstat.txt

# 4. Kiểm tra ngắt nguồn dGPU
pmset -g assertions > logs/baseline-power.txt
```

---

## 4. Kế hoạch Hoàn tác (Rollback Plan)

Nếu gặp sự cố không thể boot vào macOS:
1. Giữ nguyên USB dự phòng hoặc bản snapshot `snapshots/build-01-...`.
2. Có thể chọn phân vùng `CachyOS` trong OpenCore Picker (hoặc qua menu `F9` của laptop) để khởi động lại vào Linux bình thường.
3. Khi gặp kernel panic: OpenCore đã bật `Target = 67` và `debug=0x100 keepsyms=1`, file nhật ký panic sẽ được lưu tự động trên thư mục gốc của USB (`opencore-YYYY-MM-DD-*.txt`). Người dùng sao chép file này sang Máy A để phân tích bằng skill `log-analysis`.
