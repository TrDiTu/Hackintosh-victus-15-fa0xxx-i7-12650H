# ROADMAP — mục tiêu sau build-37 (người dùng đặt 2026-11-06)

Nền: build-37 known-good (CPU 92 % / 95 % Linux). Mọi bằng chứng dưới đây lấy từ JulioNectar @6f03560 (bản đang cài trên
MÁY B, `_cache/refs/juliornectar`) trừ khi ghi khác. Mỗi bước: một thay đổi, đo, ghi BUILD-LOG/PERFORMANCE.

## Ràng buộc chung: boot-args đã đầy (255/255)
Mọi mục cần boot-arg mới (`-ngreengva`, `ngreengtfreq=`, `gfxrst=1`) đều cần chỗ. Hướng: **patch v9** — `-ngreenpm` tự bật
HWPAUTO và tắt C8/C10 (bỏ ` ngreenpmcst=0 ngreenpmauto=1`, giải phóng 29 ký tự). Làm trước tiên khi cần chỗ.
- **2026-11-06 19:49: patch v9 đã viết** (`patches/nootedgreen-gmsfix-v9-jn24450b4.patch`, trên JN 24450b4) → build-38 boot-args 226.
  Chờ kext từ MÁY B (GMSFIX-RUNBOOK §v9). Sau build-38 còn 29 ký tự tới 255: đủ ` gfxrst=1` (9) + ` -ngreengva` (11). Nhưng cờ đọc
  bằng `checkKernelArgument` (bản sao Lilu ~228) phải nằm trong 228 ký tự đầu → chèn gần đầu chuỗi, không nối cuối.

## G1 — Hiệu năng iGPU — ⏸ BỎ QUA (người dùng 2026-11-06 20:52; GB7 GPU treo ở Feature Matching, xem BUILD-LOG 20:35) (Metal ~1094 vs Vulkan Linux ~9xxx)
- Lưu ý so sánh: GB7 Metal (macOS) và GB7 Vulkan (Linux) là hai API/backend khác nhau → chỉ là chỉ báo thô. OpenCL không có
  trên iGPU này ở macOS (người dùng, 2026-11-06), Geekbench macOS không có Vulkan → Metal vs Vulkan là mốc duy nhất; theo dõi
  cải thiện bằng chính điểm Metal giữa các build.
- JN: XE-GTFREQ — iGPU từng kẹt 100 MHz; sàn mặc định 1500 MHz (`ngreengtfreq=MHz`, 0 = tắt); dưới tải ~1300 MHz do giới hạn
  PL4/IccMax gói (`GT_PERF_LIMIT_REASONS` bit 8). Máy này: iGPU tối đa ~13 W lúc GB7 Metal (PERFORMANCE.md).
- Bước 1: đo xung GT thật lúc GB7 Metal (dòng `XeNG CS … gtf=` trong `dmesg` 10 phút đầu sau boot; `xe-monitor.py` igpu_W).
- **2026-11-06: GB7 GPU treo ở Feature Matching** (GPU reset → stamp CCS mồ côi → WindowServer watchdog; BUILD-LOG). Nghi libxedrv v20;
  JN HEAD `24450b4` có libxedrv v21 (compute barrier/thứ tự). → **người dùng duyệt nâng lên JN `24450b4` (19:49)**; patch v9 + runbook
  xong, chờ MÁY B chạy `install.sh` + build kext → build-38. Không chạy GB7 GPU trên build-37.
- Bước 2: tuỳ kết quả — sàn `ngreengtfreq`, topology/L3, scheduler (`ngreenSched`); so điểm Metal trước/sau.

## G2 — Vulkan ✅
- JN: **Vulkan 1.4 qua MoltenVK** (LunarG Vulkan SDK), không cần sửa code; `vulkaninfo` thấy GPU, `vkcube` chạy trên GPU.
- Bước: cài Vulkan SDK (LunarG, bản chính thức) trên MÁY B → `vulkaninfo --summary`, `vkcube`. Hiệu năng bị giới hạn bởi Metal (G1).
- **Kết quả 2026-11-06 (build-37):** SDK 1.4.363.1, `VK_DRIVER_FILES=…/MoltenVK_icd.json` → `vulkaninfo`: GPU0 `Intel(R) TGL Unknown`,
  0x9a49, INTEGRATED_GPU, MoltenVK 1.4.2, apiVersion 1.4.357. Cảnh báo layer trùng (SDK cài cả `~/VulkanSDK` lẫn `/usr/local`) và lỗi
  validation `LayeredApiProperties` của vulkaninfo — vô hại. `vkcube` chạy. **G2 XONG.**

## G3 — Giải mã video phần cứng — ❌ DỪNG (build-42 giải mã panic NULL+0x284; build-43 không PAVPFIX panic boot; build-44 v11 tạo context PAVP panic boot NULL+0x30 — nghi PAVP cần Intel ME; BUILD-LOG 23:32)
- JN: **H.264 giải mã trên GPU** (bit-exact) cho app dùng VideoToolbox; cần boot-arg `-ngreengva` + plugin VA đã vá
  (`macos/vadriver/build-vadriver.sh`, build từ bundle TGL 16.0.32 trên máy). HEVC: có patch (XE-GVAHEVC) nhưng là phần
  nghiên cứu. Không có `-ngreengva` thì XE-NOGVA ẩn giải mã phần cứng → phần mềm.
- Rủi ro: PAVPFIX của dự án (tắt nhánh PAVP) và GMS 60 MB khác máy JN — CHƯA XÁC MINH tương tác. Cần chỗ boot-args (v9).

## G4 — Thời gian khởi động — ✅ build-39 `gfxrst=1`: picker → đăng nhập 38 s → 23 s (nháy đen ngắn chấp nhận được; `gfxrst=4` thử ở build-40: không nhanh hơn, hình xấu hơn → bỏ). Còn có thể: `Misc/Boot/Timeout` 5 s
- Đo trước: OpenCore picker `Timeout` = 5 s; XE-PM áp dụng ở 20 s/60 s (không chặn boot). Cần mốc: bấm giờ từ nút nguồn →
  picker → logo → màn hình đăng nhập (và `log show --last boot` mốc kernel → loginwindow).
- JN: `gfxrst=1` (WhateverGreen ngừng chép framebuffer boot; ~18 s ở 3840×2400, 1080p ít hơn) + OpenCore `Resolution=Max`.
- Ứng viên khác: giảm `Timeout` OpenCore, `ShowPicker`, kext không cần thiết. Cần chỗ boot-args cho `gfxrst=1` (v9).

## Thứ tự đề xuất
1. G2 (không đổi EFI) và đo G1 bước 1 (không đổi EFI).
2. Patch v9 (giải phóng boot-args) → build mới.
3. G4 `gfxrst=1` (rẻ, đo được ngay), rồi G3 `-ngreengva` + plugin VA, rồi G1 bước 2.

## Ghi chú G3 (2026-11-06): `-ngreengva` đọc bằng `checkKernelArgument` (Lilu, 228) → không nối cuối được. Build G3 phải đổi thứ tự:
đưa các tham số `PE_parse_boot_argn` (`ngreen-eu`, `ngreen-l3`, `ngreenblmax`, `ngreenV142`, `ngreen-dmc`, `gfxrst`) ra sau cờ Lilu.
Cần thêm plugin VA build trên MÁY B (`macos/vadriver/build-vadriver.sh`, chép vào `/Library/GPUBundles`). FairPlay (Apple Music/TV+) hỏng khi có `-ngreengva` (JN #11); Safari vẫn giải mã CPU.
