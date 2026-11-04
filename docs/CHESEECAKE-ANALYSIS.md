# CHESEECAKE-ANALYSIS — Plan v4 (`docs/PLAN-cheseecake-46A3.md`)

## §A — Phase 0: đóng hướng JN và kiểm H1 (boot-args bị cắt) — 2026-11-03

### A.1 Panic graphics-v3 (build-16, `ngreenSched=5`)
- File: `logs/Kernel-2026-11-02-200211.panic` (người dùng chép 2026-11-03 01:44).
- Chữ ký **giống hệt** graphics-v1 và graphics-r3: page fault CR2 `0xc78`,
  `IOAccelTask::release+0x95 ← IGAccelTask::withOptions+0x3e ← NootedGreen Gen11::igAccelTaskWithOptions+0x18 ← IOGraphicsAccelerator2::start+0x15e1 ← IntelAccelerator::start+0x212 ← Gen11::start+0x1f74`.
- Uptime 51,88 s (v1 54,46 s; r3 54,39 s). NootedGreen UUID `822E1982-…` = v1 (JN d805e6a6); r3 là `E01F4502-…` (khucx R3).
- AppleIntelTGLGraphics 16.0.2 UUID `BA3AA1C0-…`, HookCase 8.0.1 — giống các lần trước.

### A.2 Độ dài boot-args
| Build | Độ dài trong config | Kernel thấy (dòng `Boot args` của .panic) | Phần bị mất |
|---|---|---|---|
| build-12 v1 / build-14 v2 / build-15 r3 | 291 | 255 (v1, r3; v2 không có .panic) | `=3 gfxrst=1 ngreen-eu=64 ngreen-l3=6` → còn `ngreenV142` không giá trị |
| build-16 v3 | 291 | 255 | `reen-eu=64 ngreen-l3=6 ngreenSched=5` (`ngreenSched=4→5` bị `bootarg-add` đưa xuống cuối) |
| build-10 nền | 70 | — | — |

Giới hạn:
- **255 ký tự**: đo trực tiếp từ 3 file .panic. CHƯA XÁC MINH là boot.efi/XNU cắt hay chỉ panic report in tối đa 255 — nhưng không ảnh hưởng kết luận vì cả hai đều ≥ phần bị mất.
- **~228 ký tự**: JN `docs/KERNEL-PATCHES.md` L19 ("Lilu truncates boot-args at about 228 characters"), `docs/EXPERIMENTS.md` #7 L135, `docs/HISTORY.md` L45; cheseecake `docs/PORT-I3-1220P.md` L102. Người dùng xác nhận 228 (2026-11-03). Chưa đọc source Lilu (chưa clone). Các cờ dạng `-xxx` của NootedGreen đọc qua `checkKernelArgument` (Lilu); `ngreen-eu`, `ngreen-l3`, `ngreen-dmc`, `ngreenV142`, `ngreenSched` đọc qua `PE_parse_boot_argn` (XNU). → Đặt mục tiêu **toàn chuỗi ≤ 228**.

### A.3 Kết luận H1: **XÁC NHẬN**
- NootedGreen chỉ đọc topology từ boot-args (`kern_gen11.cpp` L34–35, không có DeviceProperty thay thế); mặc định `gTopoSs = 12, gTopoL3 = 8` (L28) = 96 EU.
  ⇒ Cả 4 build JN/R3 đều chạy **topology 96 EU, L3 8** trên GPU 64 EU.
- `ngreenSched` vô tác dụng dù có nhận được: JN `docs/EXPERIMENTS.md` #27 — `-disablegfxfirmware` ép scheduler 5. ⇒ v3 thực chất không thử gì mới.
- v1/v2/r3 nhận `ngreenV142` không có `=3`: giá trị XNU gán cho tham số số không có `=` — CHƯA XÁC MINH (mặc định code cho GPU spoof là 1, `kern_gen11.cpp` L291). v3 nhận đủ `ngreenV142=3`.
- Chưa chứng minh được topology sai là nguyên nhân panic `IGAccelTask::withOptions`. JN #13 nghi topology/GTT/scheduler — đây là test rẻ nhất còn lại của hướng JN.

### A.4 Đề xuất rút ngắn boot-args (CHỜ NGƯỜI DÙNG DUYỆT — CLAUDE.md §10: đổi boot-args đồ họa)
Chuỗi đề xuất, **224 ký tự**, tham số đồ họa đứng đầu (nếu còn bị cắt thì mất phần debug ở cuối trước):
```
ngreen-eu=64 ngreen-l3=6 -ngreentglwithgfx -allow3d -disablegfxfirmware ngreen-dmc=adlp ngreenV142=3 -ngreenv189 -ngreenkeepefi -ngreenxefix -ngreenfixbootmode amfi_get_out_of_my_way=1 -amfipassbeta -v keepsyms=1 debug=0x100
```
| Thay đổi | Tiết kiệm | Lý do / bằng chứng | Rủi ro |
|---|---|---|---|
| Bỏ `ngreenSched=4` | 14 | Bị `-disablegfxfirmware` ghi đè (JN EXPERIMENTS #27) | Không |
| Bỏ `IGLogLevel=3` | 13 | Chỉ là mức log của driver Apple (JN CATALOG L997) | Mất log driver TGL; có thể thêm lại nếu còn chỗ |
| Bỏ `gfxrst=1` | 9 | WhateverGreen: tránh stall khi WindowServer mở framebuffer (JN EXPERIMENTS L398–400) — sau điểm panic | Có thể stall ~20 s ở WindowServer nếu vượt qua được panic |
| `-vi2c-force-polling` → DeviceProperty `PciRoot(0x0)/Pci(0x15,0x0)` `force-polling` | 20 | VoodooI2C `VoodooI2CDeviceNub.cpp` L236–237, **có trong tag 3.0.0 của fork lzhoang2801** (bản đang dùng): `pci_device->getProperty("force-polling") != nullptr`. I2C0 = 00:15.0 `8086:51E8` (lspci L29), TPD0 nằm dưới I2C0 | Thấp; nếu touchpad mất → kiểm `ioreg` property trên 00:15.0 |
| Bỏ `-wegnoegpu` | 11 | Trùng tác dụng với `disable-gpu` trên `PciRoot(0x0)/Pci(0x1,0x0)/Pci(0x0,0x0)` (vẫn giữ) + SSDT-DGPU-OFF | Thấp; CHƯA XÁC MINH trên máy — kiểm `ioreg` không thấy NVIDIA |
| **Không** đổi `amfi_get_out_of_my_way=1` → `amfi=0x80` | (16) | Không có nguồn xác nhận hai tham số tương đương | — |

So với dự định ban đầu của graphics-v1: biến **có chủ đích** là topology `ngreen-eu=64 ngreen-l3=6` (lần đầu thực sự tới kernel). Các thay đổi còn lại được chọn để không ảnh hưởng đường khởi tạo bộ tăng tốc; vẫn ghi rõ vì đây không phải "một thay đổi" thuần.

Base đề xuất cho build-17 `jn-topo`: build-16 (NootedGreen JN d805e6a6 — user-space JN 6f03560 đang cài trên MÁY B khớp kext này), thay boot-args + thêm `force-polling`.

### A.5 Kiểm sau boot build-17 (người dùng chạy trên MÁY B)
- Nếu panic: boot build-10, chép `.panic`; so dòng `Boot args` phải đủ 224 ký tự, kết thúc bằng `debug=0x100`.
- Nếu vào desktop:
```
sysctl kern.bootargs
kmutil showloaded | grep -iE 'nootedgreen|hookcase|AppleIntelTGL'
ioreg -rc IntelAccelerator -d1 | grep -E 'xe-topo|rowchk'      # kỳ vọng xe-topo = 16390 (64<<8 | 6)
ioreg -r -n I2C0 -d1 | grep force-polling ; log show --last boot | grep -i 'Forced polling'
system_profiler SPDisplaysDataType
```

### A.6 Kết quả build-17 `jn-topo` (2026-11-03)
- `.panic` 02:20:26: `Boot args` = đúng chuỗi 224 ký tự → topology và mọi cờ đã tới kernel.
- Chữ ký **không đổi** so với v1 (CR2 0xc78, `IOAccelTask::release+0x95 ← IGAccelTask::withOptions+0x3e`, ~53 s).
- JN áp `ngreen-eu/l3` cả ở byte patch lúc nạp (`kern_gen11.cpp` L2344–2346: `r3b[28]`, `r3bbb[4]`) và runtime `getGPUInfo` (L6508–6519) → H2 (JN chỉ đổi runtime) **bác bỏ** với JN; vẫn cần so cách cheseecake làm (Phase 1).
- ⇒ H1 đúng (args từng bị cắt) nhưng sửa H1 không hết panic. Theo Plan v4 §10: còn thử cheseecake k1/k2 trước khi dừng hướng TGL.

## §B — Phase 1: so source cheseecake @7881587 ↔ JN @6f03560 (2026-11-03, chỉ đọc)

### B.1 Phạm vi khác biệt (`src/NootedGreen`)
- Chỉ 5 file khác; gần như toàn bộ ở `kern_gen11.cpp` (~1100 dòng `<>`), còn lại 1–5 dòng. JN có thêm `kern_xepm.cpp` (`-ngreenpm`).
- Chiều khác biệt: **cheseecake là JN cũ hơn** (tách trước 21–22/10) + đổi topology. Gần như mọi hunk là code JN thêm sau: XE-RC6FW (route `IntelAccelerator::SafeForceWake`, mặc định bật), XE-GPUREC, XE-IDLEBOUND, VADIAG/CSBRESYNC, BOOTDIAG, rowchk, GVAID/GVAHEVC, auxbl.

### B.2 Đường lỗi (`IntelAccelerator::start → IGAccelTask::withOptions`)
- `Gen11::igAccelTaskWithOptions`: **giống hệt từng dòng** giữa hai fork.
- Code chỉ-JN chạy trước điểm panic: route SafeForceWake (L2101–2127), `xeGpuRecInstall` (L2130), `xeRc6FwStart` (L5673, chỉ hẹn watchdog sau 5 s). Panic này đã có ở upstream sgiammori (#12, #16) và JN #24 **trước khi** các phần này tồn tại → khó là nguyên nhân.

### B.3 H2 — topology lúc nạp: **BÁC BỎ**
| | Byte patch lúc nạp (`r3bbb[4]` = SS, `r3b[28]` = L3) | `getGPUInfo` runtime | Boot-arg |
|---|---|---|---|
| JN (build-17, `ngreen-eu=64 ngreen-l3=6`) | 8 SS, L3 6 (L2344–2346) | 8 SS × 8 EU = 64, L3 6 | `ngreen-eu`, `ngreen-l3` |
| cheseecake mặc định | 8 SS, L3 8 (cố định, L1985–1990) | 8 × 8 = 64, L3 8 | `ngreensubslices`, `ngreenmaxeu`, `ngreenl3banks` (JN bỏ qua tên này và ngược lại) |
- ⇒ build-17 đã chạy **cùng topology với cheseecake**, chỉ khác L3 (6 vs 8).
- DSS không liên tục (mask 0x33): **cả hai** thay `popcount(subsliceMask)*2` bằng hằng số, không đọc mask/fuse.

### B.4 Ghim binary ↔ source
- Release **build-18** (pre-release, 2026-10-31) target = `7881587` = đúng commit đã clone. build-17 (`161c353`) khác `7881587` chỉ ở `.gitignore` (GitHub compare) → cùng source.
- Asset build-18 `NootedGreen.kext.zip` digest `sha256:d4f81283f14abc77e78d5b7b776799085f5d27ae129292e28d543115769cfbd0`. **Đề xuất dùng build-18** thay build-17 của Plan v4 (khớp clone, mới hơn).

### B.5 Installer / user-space
- Cùng driver TGL sgiammori `95f8189`; spoof 9A49 chỉ là cảnh báo ở cả hai. `AAPL,ig-platform-id` cheseecake `0x9A490000` = data `0000499A` đang dùng.
- `macos/` khác: `libxedrv.m`, `mtl17-patches.json`, `patch-mtl17.py`, script build/cài; JN có thêm `vadriver`, `install-release.sh`. cheseecake `--uninstall` không gỡ HookCase.
- User-space chỉ chạy sau khi kernel qua được `IntelAccelerator::start` → không ảnh hưởng câu hỏi của k1.

### B.6 Kết luận (nói thẳng)
Khác biệt có thể đổi được panic `IGAccelTask::withOptions` là **rất ít**: code trên đường lỗi giống hệt, topology đã trùng ở build-17. Thứ k1 còn kiểm được: (a) bỏ toàn bộ code chỉ-JN (RC6FW, GPUREC…), (b) L3 8 thay 6. **Kỳ vọng k1 vượt panic: thấp.** Vẫn đáng một lần boot theo Plan v4 §10 (tiêu chí dừng).

### B.7 Đề xuất build-19 `chese-k1` (Phase 3)
- = build-17 với **MỘT thay đổi**: binary `NootedGreen.kext` → cheseecake release build-18. Boot-args giữ nguyên 224 ký tự (`ngreen-eu/l3` bị cheseecake bỏ qua, vô hại; topology = 8/8/L3 8).
- Giữ user-space JN trên MÁY B (như test R3).
- Cần người dùng duyệt: tải asset **pre-release** (`release-fetch --allow-prerelease`), ghi SOURCES.md.
