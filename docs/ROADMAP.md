# ROADMAP — hướng WhateverXe (nhánh `whateverxe-dual-gpu`)

Nền: **build-70** (2026-11-10) trên volume dự phòng, macOS 26.7.2 (25G332). iGPU `8086:46A3` chạy bằng WhateverXe
0.7.0-katana r7 (fork `TrDiTu/WhateverXe`, nhánh `katana-46a3`) + WhateverXe-Graphics 0.4.0; dGPU RTX 3050 Ti chạy bằng
NullMoth 2.9; CPU dùng HybridPM có XE-HWPAUTO (fork `TrDiTu/HybridPM`, nhánh `victus`).
Mỗi bước: một thay đổi, đo, ghi `BUILD-LOG.md`. Roadmap cũ theo stack JulioNectar/NootedGreen (G1–G4): `ROADMAP-JN.md`.

Ràng buộc chung: boot-args đang 214 ký tự; cờ đọc bằng `checkKernelArgument` (Lilu) phải nằm trong ~228 ký tự đầu.

## Đã xong

| Mục | Kết quả | Build |
|---|---|---|
| W1 — Tăng tốc Metal trên iGPU VCS2-only | Metal 2, VRAM 1536 MB, 1920×1080 @ 144 Hz. Cần cờ `-wex-adlp-allow-vcs2` (fuse video mask 4: chỉ có VCS2), sửa VBT eDP (r2), ép nhánh PAVP tắt (r3) | 62, ★63 |
| W2 — Giải mã H.264 phần cứng trên VCS2 | 1080p 3 ms/khung, 0 khung bỏ. r5 đổi tham số VideoMedia của driver Apple sang VCS2 (type 4, instance 2); r7 thay hàm đọc ngắt VCS bằng bản kiểu i915 | 66 |
| W3 — Turbo CPU | HybridPM: xung một nhân 3673 → 4615 MHz, GB7 999 / 4658 → 1176 / 4888 (build-67). Thêm XE-HWPAUTO và PL1 55 W (build-68, 69): người dùng báo ổn, chưa có điểm | 67–69 |
| W4 — Vulkan | LunarG SDK 1.4.363.1, MoltenVK 1.4.2 thấy iGPU | 69 |
| W5 — dGPU + HDMI | NullMoth 2.9 tự khởi động GPU lúc boot, HDMI có hình (người dùng xác nhận, chưa có log) | 70 |

Chi tiết W2 (kết quả disassemble driver Apple, từng bản r5–r7): mục G5 trong `ROADMAP-JN.md`. Chi tiết W5: `NVIDIA-VULKAN-STEPS.md`.

## Việc tiếp theo, theo thứ tự đề xuất

1. **W6 — Ổn định build-70.** Nhiều lần khởi động liên tiếp, dùng hằng ngày, rút-cắm HDMI. Thu `logs/b72/` (SPDisplays, `nvrm-display`,
   `debug.nvaccel_heads_*`). Đạt thì người dùng mới đánh dấu known-good. Lùi: build-63 ★ (không HDMI, không giải mã phần cứng).
2. **W7 — Đo lại CPU trên build-70 — ✅ 2026-11-11: GB7 2035 / 9320 (HybridPM + XE-HWPAUTO; người dùng báo).** Còn lại: GB7 CPU + `powermetrics` với HWPAUTO; thử `debug.hybridpm.cst=0` (C8/C10 tắt). Mốc: volume chính
   (NootedGreen XE-PM) 2030 / 9646. Xem PL1 55 W có hiệu lực hay MSR `0x610` vẫn giữ 45 W.
3. **W8 — Sleep/wake.** Chưa kiểm trên nhánh này. WhateverXe issue #86 báo treo khi vào sleep trên Tiger Lake; NullMoth 2.9 có sửa
   WindowServer treo sau display sleep. Thử display sleep trước, rồi system sleep.
4. **W9 — Video còn lại.** HEVC, phát lâu, mã hoá phần cứng (quay màn hình). NullMoth 2.9 có NVENC/NVDEC cho Ampere — chưa thử.
5. **W10 — `nmhybrid`** (thử nghiệm của NullMoth 2.9, tắt mặc định): render trên NVIDIA, hiện trên panel của iGPU. Chỉ thử sau W6.
6. **W11 — Công suất nghỉ và pin khi dGPU sống.** Trước đây ~8 W với dGPU tắt (nhánh chính); chưa đo trên build-70.
7. **W12 — Lên WhateverXe 0.8.x.** Chuyển các bản vá r1–r7 sang 0.8.0 (cùng `decodeADLPGT`, chưa ai sửa chỗ chặn VCS2-only), rồi
   gửi upstream: cờ VCS2-only + bản vá VCS2 media/ngắt (issue #76).
8. **W13 — Đưa sang volume chính.** Chỉ khi W6 đạt và người dùng đồng ý: volume chính đang là 26.7.1 + NootedGreen (build-48 ★).

## Hoãn / bỏ qua

- **GB7 GPU (Metal) trên iGPU:** treo ở bài Recognition — GPU bận 100 %, `IGAccelEventMachine::eventTimeout` →
  `IGScheduler5::checkForProgress`, WindowServer watchdog, khôi phục không thành (`logs/b66`). Cùng chữ ký WhateverXe #44, #40, #25;
  upstream chưa có bản sửa. Người dùng bỏ qua 2026-11-10. Chưa loại trừ ảnh hưởng của r5–r7 (thử trên build-63 nếu quay lại).
- **Video DRM (FairPlay/PAVP):** r3 ép nhánh PAVP tắt để không panic `PAVPCommandCallback`. Không có kế hoạch.
- **Đầu đọc thẻ RTS5228:** không có driver (`DEFERRED.md`).

## Rủi ro đã biết

- Boot bằng build có `-nvrmnogo` (56–69) làm boot guard của NullMoth đếm; đủ 2 lần thì NVRMFB/NVAccel tắt. Sửa: xoá NVRAM
  `nullmoth-nv-starts` (`NVIDIA-VULKAN-STEPS.md` §D).
- `install.sh` của NullMoth cài `NMXAudio.kext`, tranh bộ điều khiển HDA với VoodooHDA → phải tắt lại sau mỗi lần cập nhật.
- macOS 26.7.2 không phải bản ghim của dự án (25G241); WhateverXe-Graphics 0.4.0 và hook XCPM của HybridPM đã chạy trên 25G332.
