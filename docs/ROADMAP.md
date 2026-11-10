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

## G5 — Giải mã video phần cứng trên WhateverXe (VCS0 → VCS2) — ✅ H.264 chạy ở build-66 (2026-11-10 20:29); HEVC/ổn định CHƯA KIỂM
- Bối cảnh: nhánh `whateverxe-dual-gpu`, WEX 0.7.0-katana (fork `TrDiTu/WhateverXe` `katana-46a3`) đã tăng tốc Metal ở build-62
  (VRAM 1536 MB). Fuse máy này: video mask 4 = **chỉ VCS2** (`fuses[4]=0x000E00FB`); VCS0 bị tắt.
- Lỗi: driver Apple TGL (UUID `BA3AA1C0`) gắn ring media vào VCS0 → `IGHardwareCommandStreamer5::setWorkQueueBinding` NULL+0x284
  trong `VTDecoderXPCService` (`logs/b62/Kernel-2026-11-10-175834.panic`). Cùng triệu chứng G3 (NootedGreen `-ngreengva`, build-42).
  r4 tắt giải mã phần cứng (`WEXHardwareVideoDisabled`) để hệ thống ổn định.
- Hướng: vá driver dùng VCS2 thay VCS0 — MMIO base (VCS0 `0x1C0000` → VCS2 `0x1D0000`, theo bố trí Gen12 của i915; CHƯA XÁC MINH
  với driver Apple), engine ID/class instance, bit ngắt, chỗ tạo command streamer và scheduler bind. Linux i915 dùng VCS2 bình thường.
- Bước 1 (cần người dùng): chép `AppleIntelTGLGraphics.kext` của gói WhateverXe-Graphics 0.4.0 từ volume dự phòng vào `logs/b62/`
  (chỉ phân tích trên MÁY A, không commit, không phân phối binary Apple).
- Bước 2: disassemble — tìm nơi tạo `IGHardwareCommandStreamer5` cho VCS0, bảng engine, `IGScheduler5::bind`, HuC/firmware media
  (với `-disablegfxfirmware`). Kết luận khả thi/không trước khi viết patch.
- Rủi ro: treo cứng (issue #76 khi ép VCS2-only), panic, có thể mất nhiều ngày và có thể không làm được. Không ai có bằng chứng
  giải mã phần cứng trên iGPU VCS2-only trong macOS.
- Ảnh hưởng nếu không làm: giải mã phần mềm (i7-12650H đủ cho 1080p/4K H.264/HEVC), tốn CPU/pin hơn; DRM phần cứng đã mất do PAVP.
- **2026-11-10 18:40 — kết quả disassemble** (`AppleIntelTGLGraphics` của WhateverXe-Graphics 0.4.0, UUID `BA3AA1C0`, sha256
  `567511be…496e`; lưu `_cache/apple-bin/` — gitignored, không commit):
  - `kIGHwCsDesc` (0xd1c60 và 0xd4200, mục 0x79 byte): type 3 = VCS0 `0x1C0000` fuse bit 0x1; **type 4 = VCS2 `0x1D0000` fuse bit 0x4**;
    type 5 = VECS `0x1C8000`. Driver đã hỗ trợ VCS2 (TGL GT2 có VD0 + VD2).
  - `IntelAccelerator::getGPUInfo` lọc mặt nạ engine `accel+0x1300` bằng fuse `0x9140` (đảo, `&0xF00FF`). Máy này `0x000E00FB` → `0x10004`
    → bỏ type 3, **giữ type 4 và 5**. `IGScheduler5::initWithAccelerator` tạo streamer cho mọi bit → có streamer VCS2.
  - Lỗi: `g_cInitGfxHwCtxParamsForVideoMedia` (0xbe8a0) = `03 00 08 00 01 00 00 00 | 00 00 00 00` → type 3, instance (`ctx+0x74`) 0.
    `IGHardwareRingBufferMedia::init` hỗ trợ instance 2 (`0x1D0244`/`0x1D003C`, `_vcs2ResetRegisters`). `IGScheduler5::bind` lấy
    `sched+0xca0+8*type` → type 3 NULL → panic NULL+0x284.
  - Bản vá đề xuất (r5): đổi params thành type **4**, instance **2** (2 trường, dữ liệu hằng). Thanh ghi VCS0 hardcode chỉ còn trong hàm
    dump/chẩn đoán (`dumpRegistersVCS`, `gatherKeyRingData`) và `startGraphicsEngine` (3 chỗ, CHƯA xem kỹ); `determinePowerDomain` theo dải
    địa chỉ (VCS2 CHƯA XÁC MINH). HuC/firmware media với `-disablegfxfirmware`: CHƯA XÁC MINH. Rủi ro: treo GPU/panic khi giải mã.
- **2026-11-10 kết quả:** r5 (params VideoMedia → VCS2) + r7 (thay `readAndClearVCSInterrupts`, xử lý ngắt VCS2 kiểu i915) →
  build-66: H.264 1080p 3 ms/khung, 0 khung bỏ. r5 một mình: ~1 s/khung (ngắt VCS2 tới nhưng driver gốc không nhận; r6 đo).
  Còn lại: HEVC, phát lâu, sleep/wake, mã hoá phần cứng (quay màn hình) — chưa thử.

## G6 — dGPU RTX 3050 Ti + HDMI (NullMoth) trên volume dự phòng — ✅ chạy ở build-70 (2026-11-10 22:48, người dùng xác nhận)
- NullMoth 2.9 + WhateverXe r7: GPU tự khởi động lúc boot (không `-nvrmnogo`), HDMI có hình, panel trong trên iGPU.
- Bài học: `nvrm-go` tay sau khi vào desktop không cho HDMI (WindowServer không nhận framebuffer muộn); boot với `-nvrmnogo`
  làm boot guard đếm → đủ 2 thì NVRMFB/NVAccel tắt; xoá NVRAM `nullmoth-nv-starts` rồi boot lại.
- Còn lại: nhiều lần boot, sleep/wake, rút-cắm HDMI, công suất nghỉ khi dGPU sống, `nmhybrid` (thử nghiệm của 2.9: render NVIDIA, hiện trên panel iGPU).
- GB7 GPU Metal trên iGPU WhateverXe: treo ở Recognition (WEX #25/#44) — BỎ QUA (người dùng 2026-11-10 22:02).

