# ROADMAP — mục tiêu sau build-37 (người dùng đặt 2026-11-06)

Nền: build-37 known-good (CPU 92 % / 95 % Linux). Mọi bằng chứng dưới đây lấy từ JulioNectar @6f03560 (bản đang cài trên
MÁY B, `_cache/refs/juliornectar`) trừ khi ghi khác. Mỗi bước: một thay đổi, đo, ghi BUILD-LOG/PERFORMANCE.

## Ràng buộc chung: boot-args đã đầy (255/255)
Mọi mục cần boot-arg mới (`-ngreengva`, `ngreengtfreq=`, `gfxrst=1`) đều cần chỗ. Hướng: **patch v9** — `-ngreenpm` tự bật
HWPAUTO và tắt C8/C10 (bỏ `ngreenpmcst=0 ngreenpmauto=1`, giải phóng 30 ký tự). Làm trước tiên khi cần chỗ.

## G1 — Hiệu năng iGPU (Metal ~1094 vs Vulkan Linux ~9xxx)
- Lưu ý so sánh: GB7 Metal (macOS) và GB7 Vulkan (Linux) là hai API/backend khác nhau → chỉ là chỉ báo thô. Mốc tốt hơn:
  GB7 **OpenCL** trên cả hai hệ (macOS vẫn có OpenCL) — CHƯA đo.
- JN: XE-GTFREQ — iGPU từng kẹt 100 MHz; sàn mặc định 1500 MHz (`ngreengtfreq=MHz`, 0 = tắt); dưới tải ~1300 MHz do giới hạn
  PL4/IccMax gói (`GT_PERF_LIMIT_REASONS` bit 8). Máy này: iGPU tối đa ~13 W lúc GB7 Metal (PERFORMANCE.md).
- Bước 1: đo xung GT thật lúc GB7 Metal (dòng `XeNG CS … gtf=` trong `dmesg` 10 phút đầu sau boot; `xe-monitor.py` igpu_W).
- Bước 2: tuỳ kết quả — sàn `ngreengtfreq`, topology/L3, scheduler (`ngreenSched`), so OpenCL macOS vs Linux.

## G2 — Vulkan
- JN: **Vulkan 1.4 qua MoltenVK** (LunarG Vulkan SDK), không cần sửa code; `vulkaninfo` thấy GPU, `vkcube` chạy trên GPU.
- Bước: cài Vulkan SDK (LunarG, bản chính thức) trên MÁY B → `vulkaninfo --summary`, `vkcube`. Hiệu năng bị giới hạn bởi Metal (G1).

## G3 — Giải mã video phần cứng
- JN: **H.264 giải mã trên GPU** (bit-exact) cho app dùng VideoToolbox; cần boot-arg `-ngreengva` + plugin VA đã vá
  (`macos/vadriver/build-vadriver.sh`, build từ bundle TGL 16.0.32 trên máy). HEVC: có patch (XE-GVAHEVC) nhưng là phần
  nghiên cứu. Không có `-ngreengva` thì XE-NOGVA ẩn giải mã phần cứng → phần mềm.
- Rủi ro: PAVPFIX của dự án (tắt nhánh PAVP) và GMS 60 MB khác máy JN — CHƯA XÁC MINH tương tác. Cần chỗ boot-args (v9).

## G4 — Thời gian khởi động
- Đo trước: OpenCore picker `Timeout` = 5 s; XE-PM áp dụng ở 20 s/60 s (không chặn boot). Cần mốc: bấm giờ từ nút nguồn →
  picker → logo → màn hình đăng nhập (và `log show --last boot` mốc kernel → loginwindow).
- JN: `gfxrst=1` (WhateverGreen ngừng chép framebuffer boot; ~18 s ở 3840×2400, 1080p ít hơn) + OpenCore `Resolution=Max`.
- Ứng viên khác: giảm `Timeout` OpenCore, `ShowPicker`, kext không cần thiết. Cần chỗ boot-args cho `gfxrst=1` (v9).

## Thứ tự đề xuất
1. G2 (không đổi EFI) và đo G1 bước 1 (không đổi EFI).
2. Patch v9 (giải phóng boot-args) → build mới.
3. G4 `gfxrst=1` (rẻ, đo được ngay), rồi G3 `-ngreengva` + plugin VA, rồi G1 bước 2.
