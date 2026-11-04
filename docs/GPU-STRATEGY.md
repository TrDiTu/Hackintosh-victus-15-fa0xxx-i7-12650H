# GPU-STRATEGY — EFI nền (Giai đoạn A) và kế hoạch Giai đoạn B

Lập 2026-11-02. Máy: HP Victus 15-fa0xxx (8A4F, BIOS F.34), i7-12650H. Nguồn dữ kiện: `docs/hw-dump/`, `_cache/acpi/` (DSDT/SSDT giải mã).

## 1. dGPU NVIDIA RTX 3050 Ti (`10DE:25A0`, audio `10DE:2291`) — TẮT
- macOS không có driver Ampere → không dùng được. **HDMI không dùng được** trong macOS (HDMI nối vào dGPU; `HDMI-A-1` thuộc card NVIDIA trong dump).
- Vị trí: PCI `01:00.0` dưới root port `00:01.0` = ACPI `\_SB.PC00.PEG1.PEGP` (DSDT.dsl:6285, `_ADR` 0).
- **Cách chính — SSDT-DGPU-OFF** (`docs/acpi-src/SSDT-DGPU-OFF.dsl`): `PEGP._INI` (chỉ Darwin) gọi `PEGP._OFF` (SSDT14.dsl:584), hàm này gọi
  PowerResource `\_SB.PC00.PEG1.PXP._OFF` (SSDT4.dsl:3615; `PEG1._PR0/_PR3 = {PXP}`, SSDT4.dsl:3952–3966).
- **Dự phòng**: DeviceProperties `PciRoot(0x0)/Pci(0x1,0x0)/Pci(0x0,0x0)` → `disable-gpu = 01000000` và boot-arg `-wegnoegpu` (WhateverGreen).
  Hai lớp này chỉ ẩn thiết bị khỏi macOS; tắt nguồn thật là việc của SSDT.
- Kiểm tra trên MÁY B: xem `docs/TEST-PLAN.md` (ioreg PEGP, nhiệt độ/pin). Chưa xác minh SSDT tắt nguồn thật cho tới khi người dùng test.
- BIOS: không dùng chế độ chỉ-dGPU (iGPU phải điều khiển panel). Dump cho thấy eDP đang ở iGPU.

## 2. iGPU UHD 64 EU (`8086:46A3`) ở Giai đoạn A — CHỈ FRAMEBUFFER FIRMWARE
- Theo `PROMPT.md` Pha 2: **không spoof, không NootedGreen**. `config.plist` build-02 **không có** DeviceProperties cho `PciRoot(0x0)/Pci(0x2,0x0)`
  (build-01 có spoof `9A49` chép từ config-install của JulioNectar — đã gỡ vì trái yêu cầu này).
- macOS 26 không có driver cho 46A3 → hiển thị bằng GOP/framebuffer của firmware (1920×1080), **không tăng tốc**, không chỉnh độ sáng phần cứng
  được đảm bảo, không màn hình ngoài.
- Rủi ro: nếu WindowServer treo/màn hình đen khi không có framebuffer driver, các phương án thử (mỗi lần một thay đổi, cần người dùng duyệt) là
  `-igfxvesa` (WhateverGreen: tắt tăng tốc Intel) hoặc chỉ định `AAPL,ig-platform-id` — **chưa áp dụng**.
- Dữ kiện đã đo cho Giai đoạn B: 1 slice, 4 DSS (mask 0x33), 64 EU; **L3 bank = 6** (người dùng cung cấp); **stolen memory 60 MB** tại 0x7C800000
  (GGC 0xFEC1, `docs/hw-dump/igpu-stolen-dump.txt`); BAR0 16 MB, aperture 256 MB; DMC adlp v2.20, GuC 70.49.4; panel 1080p **144 Hz** (người dùng).

## 3. Kế hoạch Giai đoạn B (CHƯA áp dụng — chỉ sau câu "EFI nền đã ổn định, bắt đầu tăng tốc đồ họa")
- Stack JulioNectar (driver TGL 16.0.32 + NootedGreen + libxedrv), tham chiếu cheseecake (64 EU) và khucxtriendev (ADL-H + NVIDIA).
- Sẽ cần: spoof `device-id 9A49` / `AAPL,ig-platform-id` theo fork đã chọn, topology 64 EU / 6 L3 (tên boot-arg đọc từ source fork), hạ AMFI/SIP,
  `install.sh` chạy trên MÁY B. Giữ `config-install.plist` (bản nền này) để quay về.
- Rủi ro lớn nhất: panic `IOAccelTask::release` trên ADL-H có dGPU (JulioNectar #24, #16); tương tác với root patch Wi-Fi OCLP chưa ai ghi nhận.
- Chi tiết sẽ viết trong `docs/GRAPHICS-PLAN.md` (Pha 6).
