# REPLAN — WhateverXe (iGPU) + NullMoth (dGPU) theo mẫu khucxtriendev

Nhánh `whateverxe-dual-gpu` (tách từ `nvidia-gpu` @369263c, 2026-11-09).
**P0 người dùng duyệt 2026-11-09:** thử WhateverXe, dùng volume APFS thứ hai, ưu tiên độ ổn định iGPU. CLAUDE.md §0 đã ghi chú nhánh này.

## Kết quả P1 (2026-11-09) — WhateverXe KHÔNG ĐẠT cho 46A3 của máy này (chi tiết DRIVER-MATRIX X1–X4)
- i915 trên máy: `available engines: 41003` → RCS0, BCS0, **VCS2**, VECS0 (VCS2-only).
- WhateverXe 0.8.0 `decodeADLPGT` chỉ nhận video mask 1 hoặc 5. Issue #76 (46A3 rev 0x0C, VCS2-only, Tahoe, WEX 0.8.0): ProfileMismatch → không tăng tốc;
  ép nhận → **treo cứng**. Không có báo cáo Metal nào trên 46A3. Maintainer chưa trả lời.
- Với ưu tiên "ổn định iGPU", **không dựng build-51**. Kết quả dự kiến chỉ là FB không tăng tốc, hoặc treo nếu ép.
- Hướng còn lại cho dual-GPU: giữ NootedGreen, tìm nguyên nhân panic CR2 0xc78 khi dGPU sống (build-49/50). NullMoth issue #428 có người chạy
  NootedGreen + NullMoth song song → panic không phải giới hạn chung của NootedGreen. Theo dõi WhateverXe #76.
- Phần dưới (§1–§7) là phân tích ban đầu, giữ để tham khảo.

## 1. Repo tham chiếu đã đọc
khucxtriendev/irisxegraphic-i712800h-efi @8714a85 (2026-11-07, release EFI v1.0.1), clone bằng `tools/clone_ref.py`
vào `_cache/refs/khucxtriendev`. Máy: ThinkPad P1 Gen 5, i7-12800H, iGPU `8086:46A6` (96 EU), dGPU RTX A1000 `10DE:25B9`.

Tác giả báo (chưa kiểm chứng độc lập):
- Panel trong chạy trên iGPU bằng **WhateverXe** (fork của tác giả, 0.7.0) + gói user-space **WhateverXe-Graphics 0.4.0**
  + `impostor.dylib` của JulioNectar. "Metal 2 / Metal 3".
- HDMI chạy trên dGPU bằng **NullMoth nvidia-macos-driver** (Metal 3). Hai GPU chạy cùng lúc.
- Không có sleep/wake. HDMI phải cắm trước khi bật máy. Hệ chạy thử: README nói Sequoia 15.x và Tahoe; fork WhateverXe ghi Sequoia 15.8.x (24H232).

Cấu hình EFI (đọc từ `EFI/OC/config.plist`):
- **Không spoof device-id iGPU. Không SSDT tắt dGPU.** dGPU chỉ có `acpi-wake-type = 1`.
- iGPU `PciRoot(0x0)/Pci(0x2,0x0)`: `framebuffer-patch-enable` 1, `framebuffer-stolenmem` `0000C003` (60 MB), EDID override, `enable-backlight-registers-fix`.
- Kext đồ hoạ/PM: WhateverXe (không có WhateverGreen, không có NootedGreen), AMFIPass 1.4.1, **HybridPM** (XE-PM tách thành kext riêng,
  Thatisjigen, TSNPL 1.0), CpuTopologyRebuild, SMCNvidiaGPU (NullMoth).
- boot-args: `-allow3d -disablegfxfirmware -igfxdvmt -wex-reset-recover -wex-scanout-coherent -wex-hidpi-dbuf amfi_get_out_of_my_way=0x1 amfi=0x80 ipc_control_port_options=0 -hpm -hpmbeta hpmd3=1 hpmepp=128 hpmpl1=45 nvfb=1 nvaccel=1 nvfbheads=4 -nvkmsnosmooth nvfbhidpi=1 …`
- SIP `0x0A43`, SMBIOS `MacBookPro16,2` (giống dự án), BIOS "Hybrid Graphics".

## 2. WhateverXe upstream (b00t0x) — đọc README/docs ngày 2026-11-09
- WhateverXe: BSD-3-Clause, bản mới nhất **0.8.0**. Dẫn xuất từ WhateverGreen → **không chạy chung với WhateverGreen**.
- `docs/device-selection.md`: ID có backend gồm `46A0`–`46A3`, `46A6`, `46A8`… **Đã kiểm trên phần cứng: chỉ Alder Lake-H 96 EU.**
  `46A3` (GT1, 64 EU — máy này) thuộc nhóm "expected to work, untested". → CHƯA XÁC MINH, rủi ro lớn nhất.
- macOS: Tahoe **26.7 trở lên**; "Sequoia and Tahoe accept compatible updates within their OS family" (Graphics 0.4.1). 25G241 = 26.7.1 → trong phạm vi.
- Kiểm hồi quy upstream có: Metal, OpenGL, **OpenCL**, **H.264 encode/decode, HEVC decode** (đúng các thứ dự án đang thiếu: G3 giải mã video đã dừng vì panic).
  Metal family: không ghi.
- Yêu cầu: `-allow3d -disablegfxfirmware`; DVMT cố định 60 MB → `-igfxdvmt` + `framebuffer-patch-enable` + `framebuffer-stolenmem 0000C003`
  (máy này: stolen đo được 60 MB, BIOS không có tuỳ chọn DVMT → khớp). Không cần spoof device-id. SIP `0x803` ("Full SIP is unsupported").
  **AMFIPass 1.4.1 "Mod"** (bản sửa, "upstream AMFIPass is not a substitute") → nguồn phải kiểm định riêng.
  README upstream: `amfi=0x80`, `ipc_control_port_options=0` không cần (khucxtriendev vẫn dùng — có thể do NullMoth).
- WhateverXe-Graphics (.pkg): cài vào `/Library` + rebuild AuxKC, không sửa System/snapshot, không cần OCLP/KDK.
  **Chứa payload dẫn xuất từ driver Apple đã sửa** (license BSD-2 chỉ áp cho công cụ đóng gói). → Chỉ người dùng tự cài trên MÁY B;
  không đưa vào repo/EFI (CLAUDE.md §4: không phân phối binary Apple).
- Vấn đề đã biết: DP cắm lại có thể đen/treo; App Store video có thể treo GPU (Sequoia); sleep "experimental" (0.8.0).

Không lấy binary từ EFI của khucxtriendev (không phải release chính thức). Bản vá của fork (`whateverxe_thinkpad_p1_gen5.patch`)
chỉ sửa trường hợp GOP 6-bpc của panel BOE ThinkPad; panel Victus chưa biết bpc lúc GOP → dùng upstream 0.8.0 trước.

## 3. Vì sao đáng thử: nút thắt hiện tại của nhánh `nvidia-gpu`
- build-49/50: **chỉ riêng việc để dGPU sống** (bỏ SSDT-DGPU-OFF + `disable-gpu`, chưa có driver NVIDIA) làm stack
  NootedGreen + TGL panic lúc khởi tạo (CR2 0xc78, `IOAcceleratorFamily2` ← TGL ← NootedGreen). Chưa có cách sửa.
- khucxtriendev chạy dGPU sống + driver NVIDIA với WhateverXe trên cùng đời CPU (ADL-H) và cùng chip dGPU (GA107: A1000 `25B9` ~ 3050 Ti `25A0`).
  → Đổi driver iGPU có thể tránh đúng panic này. CHƯA XÁC MINH trên 46A3.
- Thêm: WhateverXe có thể mở lại G3 (giải mã video) và OpenCL. Không hứa Metal 3 trên iGPU (upstream không ghi).

## 4. Cái giá / rủi ro
| Mục | Hệ quả |
|---|---|
| 46A3 64 EU chưa ai kiểm | Có thể không có tăng tốc, GPU hang, panic. Có thể cần topology như `ngreen-eu=64`; WhateverXe không có cờ tương tự (CHƯA XÁC MINH) |
| Mất NootedGreen + patch dự án v10 | Mất GMSFIX/FENCEFIX (sửa lỗi riêng của TGL trên máy này — WhateverXe có thể không cần, CHƯA XÁC MINH) và **XE-PM/XE-HWPAUTO** (CPU 92 % Linux). Thay bằng HybridPM: không chắc có HWPAUTO → CPU có thể tụt về ~54 % |
| User-space trên MÁY B | Stack JN (libxedrv, `/Library/GPUBundles`) và WhateverXe-Graphics cùng đụng bundle TGL → phải gỡ một bên. Quay về build-48 cần cài lại stack JN |
| AMFIPass Mod + SIP 0x803 | Bật lại AMFIPass (build-47 đã bỏ). Nguồn "Mod" chưa kiểm định. Hệ quả bảo mật như trước |
| dGPU luôn bật (NullMoth không có RTD3/GC6) | Nghỉ tăng W, pin, nhiệt. Có thể "armed-only": `/Library/GPUBundles/nvmtl-allow.txt` = `!*` (khucxtriendev) |
| NullMoth Ampere | Tác giả: Ampere "Pending"; 3050 Laptop có báo lag/treo (#486) |
| Không sleep, HDMI chỉ cold-plug | Như khucxtriendev |
| License | WhateverXe BSD-3; HybridPM TSNPL 1.0; NullMoth PolyForm NC 1.0 → chỉ dùng cá nhân, phi lợi nhuận |

## 5. Đề xuất cách thử an toàn: **volume APFS thứ hai trên MÁY B**
Cài thêm macOS 26.7.1 (25G241) vào volume APFS mới cùng container (người dùng làm, theo `macos-install-runbook`).
Mỗi volume có `/Library` riêng → stack JN trên volume hiện tại không bị đụng. Picker OpenCore chọn volume.
EFI thử nghiệm chỉ trên USB; ESP ổ trong giữ build-47/48. (Dung lượng trống ổ MÁY B: CHƯA BIẾT — người dùng kiểm.)

## 6. Kế hoạch theo bước (mỗi bước một thay đổi, có điểm dừng)
- **P0 — Người dùng quyết định:** (a) có đổi hướng thử WhateverXe không; (b) volume thứ hai hay thay thế tại chỗ; (c) sửa CLAUDE.md §0.
- **P1 — Kiểm định** (`driver-vetting`, `release-fetch`, ghi DRIVER-MATRIX/SOURCES): WhateverXe 0.8.0, WhateverXe-Graphics 0.4.1
  (chỉ đọc mô tả, người dùng tự tải trên MÁY B), AMFIPass 1.4.1 Mod (tìm nguồn chính thức), HybridPM (Thatisjigen), NullMoth (D1 đã có). Dừng chờ duyệt.
- **P2 — build-51 `wex-igpu`** = build-48 (dGPU TẮT như cũ) − WhateverGreen − NootedGreen + WhateverXe + HybridPM + AMFIPass Mod;
  thuộc tính iGPU 60 MB; boot-args `-allow3d -disablegfxfirmware -igfxdvmt` + HybridPM; SIP `0x803`. Trên volume mới: cài WhateverXe-Graphics → kiểm
  `system_profiler SPDisplaysDataType`, Metal, 144 Hz, độ sáng, GPU hang (đọc log), Geekbench 7 CPU/GPU, công suất nghỉ.
  **Cổng:** không có tăng tốc ổn định trên 46A3 → dừng, soạn issue cho b00t0x, giữ hướng JN.
- **P3 — build-52 `wex-dgpu-on`** = build-51 + dGPU sống (SSDT-DGPU-OFF tắt, không `disable-gpu`), chưa driver NVIDIA. Tương đương phép thử build-50.
  Không panic → nút thắt build-49/50 được gỡ.
- **P4 — build-53 `wex-nullmoth`** = build-52 + boot-args NullMoth; người dùng cài NullMoth (pkg chính thức, không dùng app 1401), cắm HDMI trước khi bật máy.
  Kiểm HDMI, Metal 3 trên dGPU, armed-only, công suất nghỉ.
- **P5 — So sánh với build-48** (CPU, Metal, nghỉ W, độ ổn định, HDMI, giải mã video) → người dùng chọn hướng chính.

Đường lui suốt quá trình: build-48 ★ trên ESP ổ trong + volume macOS hiện tại; `config-install.plist`.

## 7. Câu hỏi cho người dùng
1. Thử WhateverXe thay NootedGreen (chấp nhận rủi ro mất XE-PM HWPAUTO)?
2. Có chỗ cho volume APFS thứ hai (~40 GB) trên MÁY B không?
3. Mục tiêu ưu tiên: HDMI (dGPU) hay giải mã video/ổn định iGPU?
