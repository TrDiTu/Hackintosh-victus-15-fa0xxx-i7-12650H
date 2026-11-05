# POSTINSTALL-RUNBOOK — sau khi cài (MÁY B, macOS 26.7.1 / 25G241)

Claude chỉ viết các bước; người dùng tự làm trên MÁY B và báo lại. Nguồn: README OCLP-CustoMac (đọc 2026-11-02, commit f2bbcef; mục "Root Patch Selection" L120–146; baseline DisableIoMapper=true L387),
INSTALL.md AirportItlwm-Tahoe 1.0.0, release https://github.com/kgp-macPro/OCLP-CustoMac/releases/tag/v3.0.3.

## 0. Chặn cập nhật macOS (làm trước)
System Settings › General › Software Update › Automatic Updates: tắt mọi mục tải/cài. Cập nhật sẽ xoá root patch và có thể làm hỏng EFI/stack sau này.
Ghi lại: `sw_vers` (phải là 25G241).

## 1. Wi-Fi AirportItlwm-Tahoe (cần EFI build-06 trở lên; build-07 = AppleVTD, `DisableIoMapper=false`)
Build-06 đã có trong EFI: AMFIPass 1.4.1 + `-amfipassbeta`, IOSkywalkFamily 1.2.0, IO80211FamilyLegacy 1.0.0, Block IOSkywalkFamily, AirportItlwm-Tahoe 1.0.0,
SIP hạ `csr-active-config 03080000`. **Hệ quả bảo mật:** SIP không còn bảo vệ hệ thống, AMFI bị AMFIPass vượt; cập nhật macOS xoá root patch.

1. Boot MÁY B bằng USB build-08 (RTL8111 2.4.2 + AirportItlwm 1.1.0-beta.1 ZC28). Mạng: dùng Ethernet (Wi-Fi chưa chạy trước khi patch).
2. Kiểm tra SIP đã hạ: `csrutil status` → phải KHÔNG còn "enabled" (thường "unknown (Custom Configuration)"). Nếu vẫn "enabled": tắt máy, trong OpenCore
   chọn "Reset NVRAM" một lần, boot lại, kiểm tra lại.
3. Tải `OpenCore-Patcher.pkg` từ release v3.0.3 ở trên (chỉ trang release chính thức). Kiểm tra:
   `shasum -a 256 ~/Downloads/OpenCore-Patcher.pkg` → phải là `97dcc3f225bdf3f0cf88e15efb4b02ce956b7202f8f5e4fd5e7eece76d2cffa3`.
4. Cài pkg: gói **chỉ cài app** `OpenCore-Patcher.app` vào `/Applications` (không có lựa chọn patch trong trình cài — bình thường).
   Mở `/Applications/OpenCore-Patcher.app`. Nếu Gatekeeper chặn: README cho phép `xattr -cr` trên gói chính chủ đã kiểm SHA-256; không tắt Gatekeeper toàn hệ thống.
   **Không** dùng "Build and Install OpenCore" (EFI do dự án quản lý).
5. Chọn **Post-Install Root Patch** → màn hình **Root Patch Selection** (`[✓] Modern Wi-Fi`, `[✓] Modern Audio`, `[ ] Manually select Kernel Debug Kit`):
   giữ **Modern Wi-Fi**, BỎ chọn **Modern Audio**. Nếu các ô chỉ đọc (máy đã có root patch cũ): ghi lại lựa chọn đang áp dụng; muốn đổi → Revert Root Patches → khởi động lại → patch lại.
   Hộp thoại "Pre-Update Resource Preparation": chọn **Cancel** (hoặc **Review Root Patches** để về màn hình chọn).
6. Start Root Patching → nhập mật khẩu → chờ xong → khởi động lại (vẫn qua USB build-08).
7. Kiểm tra (INSTALL.md AirportItlwm-Tahoe), chụp/chép kết quả:
   ```
   kmutil showloaded --list-only | grep -i -E "AirportItlwm|IO80211|Skywalk|AMFIPass"
   ioreg -r -c AirportItlwm -l -w0 | head -40
   ifconfig -l
   ioreg -r -c AppleVTD -l -w0 | head -20          # build-07: AppleVTD phải có
   ioreg -r -c AppleVTDDeviceMapper -l -w0 | head -20
   ```
   Menu Wi-Fi có hiện mạng, kết nối được, bật/tắt Wi-Fi lại được, khởi động lại 3 lần vẫn có Wi-Fi.
8. Thất bại: Ethernet vẫn dùng được. Gửi về: kết quả bước 7, `log show --last boot | grep -i -E "airportitlwm|80211|skywalk|amfi" | tail -200`.
   Quay lại: OCLP-CustoMac có "Revert Root Patches"; EFI quay về build-05 (snapshot).

## Trạng thái (2026-11-02)
- §0 chặn cập nhật: **xong**. §1 Wi-Fi: **xong** (build-08 known-good; 3 lần khởi động lại OK).

## 2. USB map — VIỆC CÒN LẠI BẮT BUỘC của Giai đoạn A
Hiện EFI dùng `UTBDefault.kext` (mở mọi cổng, vượt giới hạn 15 cổng của macOS) — chỉ để map. Cần thay bằng `UTBMap.kext` riêng của máy.
Công cụ: USBToolBox tool (MIT) https://github.com/USBToolBox/tool — README khuyên chạy trên **Windows** (đoán loại cổng, ghép companion port);
bản macOS thiếu hai tính năng đó. Bản cuối có `macOS.zip` là **0.1.1**; bản 0.2 chỉ có Windows. Release cũ, không có digest SHA-256.

**Cách A (khuyên dùng) — Windows hoặc Windows PE** (Ventoy trên USB của bạn có thể boot ISO Windows PE; README: Shift+F10 trong WinPE để mở cmd):
1. Tải `Windows.exe` (0.2) từ trang release chính thức, chạy.
2. Chọn **Discover Ports**. Cắm lần lượt **một thiết bị USB 2.0 và một thiết bị USB 3.x vào TỪNG cổng** (cả 2 chiều nếu là USB-C), chờ hiện tên rồi rút.
3. Chọn cổng: giữ các cổng ngoài, **cổng Bluetooth nội bộ** (`8087:0032`) và **camera** (`30C9:0069`) — hai cổng này để kiểu `Internal` (255). Tổng ≤ 15 cổng / controller.
4. **Build kext** → dùng kiểu **USBToolBox** (cần `USBToolBox.kext`, đã có trong EFI). Kết quả: `UTBMap.kext`.
5. Chép `UTBMap.kext` vào `docs/hw-dump/` trên MÁY A (hoặc chỗ khác trong dự án) rồi báo Claude.

**Cách B — macOS (25G241, build-08)**: tải `macOS.zip` (0.1.1), giải nén, chạy từ Terminal; làm như bước 2–5. Tự đặt loại cổng
(USB-A 3.x = `USB3`, USB-C = `TypeC+Sw`/`TypeC`, nội bộ = `Internal`). Chưa có báo cáo bản 0.1.1 chạy trên Tahoe → CHƯA XÁC MINH.

Claude sẽ: thêm `UTBMap.kext`, tắt `UTBDefault.kext`, validate, snapshot, ghi USB. Kiểm sau đó: mọi cổng nhận thiết bị, camera và (sau này) Bluetooth vẫn thấy.

## 3. Kiểm tra thêm (ghi lại, không bắt buộc sửa)
- **Sleep/wake**: Apple menu › Sleep, chờ 1 phút, mở lại. Ghi: có thức dậy không, màn hình/touchpad/Wi-Fi có lại không. Giai đoạn B sẽ KHÔNG có sleep
  (giới hạn stack đồ họa), nên đây chỉ là mốc so sánh. Nếu treo/khởi động lại → gửi `pmset -g log | tail -100`.
- **Độ sáng màn hình** (phím Fn), **pin** sau 30 phút dùng (`pmset -g batt`), **nhiệt độ/quạt** (dGPU phải tắt).
- **Mốc trước tăng tốc** (TEST-PLAN.md): chạy 5 lệnh ở cuối TEST-PLAN, chép file về MÁY A.

## 4. Boot không cần USB (tuỳ chọn, build-08 đã known-good)
1. Trên macOS: `diskutil list` → tìm phân vùng **EFI** của ổ trong (thường `disk0s1`). `sudo diskutil mount disk0s1`.
2. Xem nội dung `/Volumes/EFI/EFI`. **Nếu có `EFI/Microsoft` (Windows)**: KHÔNG xoá, KHÔNG ghi đè `EFI/BOOT/BOOTx64.efi` của Windows — báo Claude trước.
   Nếu ESP trống / chỉ có EFI cũ của bạn: sao lưu thư mục đó ra Desktop trước.
3. Chép **nguyên thư mục `EFI` từ USB MACEFI** (đã có SMBIOS thật) sang ESP: chỉ thêm `EFI/OC` và `EFI/BOOT` (nếu không đụng Windows).
4. BIOS HP (F10): thêm mục boot trỏ tới `\EFI\OC\OpenCore.efi` (hoặc `\EFI\BOOT\BOOTx64.efi`) và đặt lên đầu — tên mục trong BIOS HP: CHƯA XÁC MINH,
   ghi lại tên bạn thấy. Giữ USB MACEFI làm dự phòng.
5. Lần sau Claude cập nhật EFI: vẫn ghi lên USB trước, test, rồi bạn tự chép sang ESP.

## 5. Audio ALC245 (build-30, người dùng duyệt 2026-11-05)
EFI build-30 đã có AppleALC 1.9.8 + `layout-id` 13 trên `PciRoot(0x0)/Pci(0x1f,0x3)` (HDAS). AppleALC **không ra tiếng** khi chưa có AppleHDA
(Tahoe đã gỡ; máy hiện chỉ có root patch "Modern Wireless").
1. Boot build-30. Kiểm: `kmutil showloaded | grep -i AppleALC` (phải có). Wi-Fi vẫn chạy như cũ.
2. Cắm Ethernet (KDK ~1 GB tải qua mạng). Mở **OpenCore-Patcher (OCLP-CustoMac 3.0.3)** → Post-Install Root Patch.
3. Nếu danh sách chỉ đọc (đã có root patch): **Revert Root Patches** → khởi động lại (vẫn bằng build-30; Wi-Fi tạm mất, dùng Ethernet) →
   mở lại OCLP → Post-Install Root Patch.
4. Chọn **cả hai**: Modern Wi-Fi **và** Modern Audio. OCLP tự tải KDK **25G241** (có trên KdkSupportPkg) → Start Root Patching → khởi động lại.
5. Kiểm và gửi Claude:
   ```
   ls -d /System/Library/Extensions/AppleHDA.kext
   kmutil showloaded | grep -i -E 'AppleHDA|AppleALC'
   ioreg -lw0 -p IOService | grep -E '"layout-id"|AppleHDAController' | head
   ```
   Thử: loa trong, jack tai nghe (cắm/rút có tự chuyển không), mic trong (System Settings → Sound → Input).
6. Không có tiếng / thiếu loa/jack/mic → báo Claude thử layout 11, rồi 12 (chỉ đổi `layout-id`, không cần root patch lại).
- Hệ quả: thêm một vòng root patch (snapshot hệ thống ghi lại; cập nhật macOS xoá cả Wi-Fi lẫn Audio). Stack đồ hoạ cài ở `/Library` (AuxKC) không bị Revert đụng tới — CHƯA XÁC MINH, kiểm Metal sau bước 4.
- HDMI audio không có (HDMI nối dGPU).

## 6. Tuỳ chọn — Bluetooth AX210 (đã tạm bỏ qua)
- Ứng viên: IntelBluetoothFirmware/IntelBTPatcher **fork lshbluesky 2.5.2** + BlueToolFixup 2.7.2 + NVRAM `bluetoothExternalDongleFailed`/`bluetoothInternalControllerInfo`
  + `-btlfxallowanyaddr` (DRIVER-MATRIX #8). Bản upstream 2.4.0 lỗi với `8087:0032` trên Tahoe. Cần cổng BT nội bộ có trong USB map → **làm sau §2**.

## 7. Trước Giai đoạn B
- Sao lưu toàn bộ (Time Machine hoặc ảnh ổ). Stack đồ họa và root patch đều sửa hệ thống; Giai đoạn B: không sleep, không màn hình ngoài, có thể GPU hang/panic.
- Chỉ bắt đầu khi bạn viết đúng câu: **"EFI nền đã ổn định, bắt đầu tăng tốc đồ họa"**.
