# GRAPHICS-RUNBOOK — Giai đoạn B, chạy trên MÁY B (macOS 26.7.1 / 25G241)

Kế hoạch đã duyệt: `docs/GRAPHICS-PLAN.md` (2026-11-02). Repo stack: **https://github.com/JulioNectar/Hackintosh-XPS13Plus-IrisXe-Tahoe @ `6f03560`**.
Claude chỉ viết các bước; bạn tự chạy trên MÁY B và gửi kết quả. **Không chạy `make-efi.sh`** (sinh serial mới, đăng xuất iCloud).

## Đường lui (đọc trước)
- `EFI/OC/config-install.plist` trên USB = EFI nền build-10 (KHÔNG spoof, KHÔNG NootedGreen, SIP 0x803). An toàn kể cả khi đã cài driver TGL
  (driver TGL không khớp 46A3 thật khi không spoof).
- Cách boot bằng nó: Claude ghi lại EFI nền (build-10, snapshot) lên USB. (OpenCore không chọn được config lúc boot.)
- Gỡ stack: `zsh install.sh --uninstall` trong thư mục clone, rồi boot EFI nền.
- Đã sao lưu toàn bộ MÁY B (người dùng xác nhận 2026-11-02).

## Bước 0 — Dọn stack cũ (BẮT BUỘC: build-11 treo vì còn kext TGL + HookCase từ lần thử trước)
Boot EFI nền build-10 (không spoof). Trên MÁY B:
```
xcode-select -p || xcode-select --install
cd ~ && [ -d xe-stack ] || git clone https://github.com/JulioNectar/Hackintosh-XPS13Plus-IrisXe-Tahoe.git xe-stack
cd ~/xe-stack && git checkout 6f03560ef9694f9826caae15624d4a6cb1bf9ffc
zsh install.sh --uninstall          # hỏi mật khẩu; xoá bundle TGL, xe.bundle, kext TGL + HookCase, rồi kmutil load -z
```
Kiểm còn sót không (gửi Claude toàn bộ output):
```
ls /Library/Extensions
ls /Library/GPUBundles 2>/dev/null
ls -d /System/Library/Caches/xe.bundle 2>/dev/null
```
- Nếu còn mục lạ liên quan đồ họa (vd. `NootedGreen*`, `XeGfx*`, `WTLIntelGfx*`, `AppleIntelTGL*` tên khác): **chưa xoá tay**, gửi Claude danh sách trước.
- Khởi động lại (vẫn build-10), xác nhận vào được desktop, Wi-Fi/Ethernet còn chạy. Sau đó Claude ghi lại build-11 và tiếp Bước 1.

## Bước 1 — Boot `graphics-prep` (build-11)
EFI = build-10 + spoof iGPU 9A49 + SIP `0x0A13`. **Chưa có NootedGreen → chưa tăng tốc** (giao diện vẫn như trước).
1. Boot MÁY B bằng USB. Kiểm:
   ```
   csrutil status
   ioreg -r -c IOPCIDevice -n IGPU -d 1 | grep -E '"device-id"|ig-platform'
   ```
   Kỳ vọng: device-id `<499a0000>`. Wi-Fi + Ethernet vẫn chạy (ghi lại).
2. Nếu treo/không vào được desktop: dừng, chụp màn hình, báo Claude (quay về EFI nền).

## Bước 2 — Chuẩn bị và kiểm tra (chưa cài gì)
```
xcode-select --install                       # Command Line Tools (một lần)
cd ~ && git clone https://github.com/JulioNectar/Hackintosh-XPS13Plus-IrisXe-Tahoe.git xe-stack
cd ~/xe-stack && git checkout 6f03560ef9694f9826caae15624d4a6cb1bf9ffc
zsh install.sh --check
```
- Clone vào ổ **APFS** (thư mục home là được) — install.sh từ chối ổ khác.
- **Gửi toàn bộ output `--check` cho Claude.** Kỳ vọng: x86_64 ✓, macOS 25G241 ✓, Command Line Tools ✓, "GPU presented as Tiger Lake (device-id 9A49)" ✓,
  "NootedGreen is not loaded (fine for a first install…)" ⚠ (bình thường lần đầu).
- **Không chạy `zsh install.sh` (không `--check`) cho tới khi Claude xem kết quả.**

## Bước 3 — Cài (chỉ sau khi Claude duyệt Bước 2)
```
cd ~/xe-stack && zsh install.sh
```
- Script tải NootedGreen upstream @ 95f8189 (driver bundle TGL 16.0.32 của Apple), build NootedGreen.kext + HookCase.kext + Metal driver/libxedrv,
  cài vào `/Library/Extensions`, `/Library/GPUBundles`, `/System/Library/Caches/xe.bundle`, hỏi mật khẩu một lần.
- System Settings › Privacy & Security: cho phép extension nếu được hỏi.
- **SAU KHI CÀI: KHÔNG khởi động lại bằng `graphics-prep`** (đã có TGL + spoof mà thiếu NootedGreen = rủi ro, INSTALL.md L136–140).
- Gửi Claude: output cuối của install.sh (dòng md5 NootedGreen), và chép **`~/xe-stack/build/NootedGreen.kext`** (cả thư mục) sang MÁY A,
  ví dụ vào gốc USB MACEFI (ngoài thư mục EFI).
- Kiểm Wi-Fi vẫn chạy trước khi tắt máy (root patch OCLP + install.sh: tương tác CHƯA XÁC MINH).

## Bước 4 — Claude dựng `graphics-v1`
graphics-prep + NootedGreen.kext (sau WhateverGreen, MinKernel 25.0.0) + boot-args đồ họa:
`IGLogLevel=3 -ngreentglwithgfx -allow3d -disablegfxfirmware ngreen-dmc=adlp -ngreenv189 -ngreenkeepefi -ngreenxefix -ngreenfixbootmode
amfi_get_out_of_my_way=1 ngreenSched=4 ngreenV142=3 gfxrst=1 ngreen-eu=64 ngreen-l3=6` (cộng boot-args nền). Validate → snapshot → ghi USB.

## Bước 5 — Kiểm sau boot graphics-v1 (gửi Claude)
```
kmutil showloaded | grep -iE 'nootedgreen|hookcase|AppleIntelTGL'
ioreg -rc IntelAccelerator -d1 | grep -E 'xe-topo|rowchk'      # xe-topo kỳ vọng 16390
system_profiler SPDisplaysDataType
ls -t /Library/Logs/DiagnosticReports/ | head                    # panic nếu có
```
+ ảnh About This Mac, cảm nhận giao diện (mượt/giật/lỗi hình), Wi-Fi/Ethernet/touchpad còn chạy không.
Panic hoặc treo khi khởi tạo (đặc biệt `IOAccelTask::release`, issue #24): chụp màn hình, lấy file `.panic`, báo Claude → quay về EFI nền.
