# STATE — bộ nhớ giữa các phiên (Claude Code cập nhật cuối mỗi phiên/pha)

- Cập nhật lần cuối: 2026-11-09 23:40
- **2026-11-09 — nhánh `whateverxe-dual-gpu`** (worktree `.claude/worktrees/whateverxe-dual-gpu`, tách từ `nvidia-gpu`): đề xuất lên lại kế hoạch theo
  khucxtriendev @8714a85 (WhateverXe cho iGPU + NullMoth cho dGPU/HDMI). `docs/REPLAN-WHATEVERXE.md`. P0 duyệt (thử WhateverXe, volume APFS thứ hai,
  ưu tiên ổn định iGPU); CLAUDE.md §0 ghi chú nhánh. **P1: WhateverXe KHÔNG ĐẠT** — máy VCS2-only (`available engines: 41003`), WEX 0.8.0 từ chối
  (issue #76: ProfileMismatch, ép thì treo cứng). DRIVER-MATRIX X1–X4. Người dùng chọn: giữ NootedGreen, điều tra panic dGPU-sống (vẫn tạo volume dự phòng). **build-51 `dgpu-powered-hidden`** (= build-50 + `disable-gpu`)
  dựng xong, validate 0/0, snapshot, **đã ghi USB 23:44**; test 2026-11-10: boot OK, Metal 2 → panic do dGPU hiện trong IOKit. Nguyên nhân: personality
  IntelAccelerator của NootedGreen không lọc vendor. **Patch v12 XE-PCIMATCH** viết xong (GMSFIX-RUNBOOK §v12) — kext v12 nhận (md5 24b8d331); build-52 (dGPU hiện + v12): hết panic 0xc78, panic mới ở WindowServer (FB TGL gọi NULL; IONDRVFramebuffer gắn vào dGPU).
  **build-53 `block-ondrv`** (= build-52 + Block IONDRVSupport, theo README NullMoth) đã ghi USB 00:47; **panic giống build-52**. Disassemble: FB TGL gọi callback AGDC NULL (AGDP không gắn khi dGPU hiện).
  **Patch v13 XE-AGDCSTUB** viết xong (GMSFIX-RUNBOOK §v13) — kext v13 nhận (md5 58678f8b); **build-54 `agdcstub`** (USB 01:09): hết panic NULL, panic chia 0 ở setupPipeWatermarks (AGDC modeset không có) → cần biết vì sao AGDP không gắn khi dGPU hiện; chờ AppleGraphicsControl.kext từ KDK. USB đang build-53 (không boot được); ổ trong build-47.
  Người dùng chọn thử WhateverXe + NullMoth trên volume dự phòng: **build-55 `wex-nullmoth`** đã ghi USB 01:29; vào desktop với dGPU hiện (không panic); NullMoth 2.8.1 đã cài; volume dự phòng = macOS 26.7.2 (không phải 25G241); sau cài NullMoth: treo cứng lúc NVRM-fb cấp phát scanout (console tắt). **build-56 `nvrmnogo`** (USB 01:54): vào desktop; WhateverXe từ chối iGPU (VCS2-only, không tăng tốc); NVRM nạp chờ go → go 1/2 OK không treo. Người dùng chọn NootedGreen + NullMoth trên volume chính → **build-57 `nm-install`** (cài NullMoth; USB 02:10) ; NullMoth cài trên volume chính (NMXAudio gỡ khỏi AuxKC); **build-58 `ng-nullmoth`** (USB 02:18): panic chia 0 như build-54 → AGDP vẫn không gắn khi dGPU hiện. Đề xuất v14 XE-AGDCWAIT (chẩn đoán, ý tưởng từ WhateverXe) hoặc dừng về build-48 — chờ người dùng; MÁY B làm theo `docs/WEX-NULLMOTH-RUNBOOK.md`.
  Ghi nhớ cho hướng NootedGreen: WhateverXe có guard AGDC riêng (`WEXDisplay13AGDCGuardReady`); WhateverGreen có `disable-agdc`.
- **2026-11-10 22:48:** **build-70 `nvrm-autogo` CHẠY** (người dùng xác nhận "hoạt động rồi"; chưa có `logs/b72/`): volume dự phòng 26.7.2 = iGPU 46A3 WhateverXe r7 (Metal, H.264 VCS2) + HybridPM/HWPAUTO + NullMoth 2.9 (RTX 3050 Ti, HDMI). Điều kiện: xoá NVRAM `nullmoth-nv-starts` sau khi boot guard đếm đủ 2 (`docs/NVIDIA-VULKAN-STEPS.md` §D). Chưa kiểm: ổn định nhiều lần boot, sleep, HEVC, GB7 GPU Metal (treo, bỏ qua). Chưa known-good. Nhánh đã commit + push.
- **2026-11-10 22:28:** Volume dự phòng: Vulkan SDK OK; NullMoth 2.9 cài xong; `nvrm-go` tay → RTX 3050 Ti Metal 4, HDMI bật head nhưng WindowServer không nhận (fb xuất hiện sau WS). **build-70 `nvrm-autogo`** (= build-69 bỏ `-nvrmnogo`) ghi USB 22:28, chờ `logs/b71/`. Lùi: build-69 (snapshot). Snapshot build-61 đã xoá.
- **2026-11-10 22:05:** build-69 CPU ổn (người dùng). GB7 GPU Metal treo (WEX #25/#44, chưa có sửa) — BỎ QUA theo người dùng. Việc mới: Vulkan SDK + NullMoth 2.9 + `nvrm-go` tay trên volume dự phòng theo `docs/NVIDIA-VULKAN-STEPS.md`; chờ `logs/b70/`. Sau đó build-70 bỏ `-nvrmnogo`.
- **2026-11-10 21:43:** **build-69 `hwpauto`** (= build-68 + HybridPM fork @6ddb23d có XE-HWPAUTO, mặc định bật) ghi USB 21:43, chờ `logs/b69/` (GB7 CPU; thêm lần `cst=0`). build-68: `pl1_set 440` (PL1 55 W ghi được ở MCHBAR). Snapshot build-58/59/60 đã xoá.
- **2026-11-10 21:28:** build-67 test: turbo chạy (max 4615 MHz), GB7 CPU 1176/4888 (build-66: 999/4658); đa nhân giới hạn PL1 45 W của HP. **build-68 `hpmpl1-55`** (= build-67 + `hpmpl1=55`) ghi USB 21:28, chờ `logs/b68/`. Snapshot build-58/59 đã xoá. Dùng hằng ngày: build-63 ★ hoặc build-67.
- **2026-11-10 21:09:** **build-67 `hybridpm`** (= build-66 + HybridPM 1.0.0 @23c4537, sửa turbo CPU: GB7 CPU trên build-66 chỉ max 3673 MHz) đã snapshot (xoá snapshot build-58) và ghi USB 21:09. Chờ `logs/b67/` (GB7 CPU + powermetrics + `sysctl debug.hybridpm`). GB7 GPU treo ở Recognition (WindowServer watchdog) — để sau. Dùng hằng ngày: build-63 ★.
- **2026-11-10 20:29:** **build-66 (r7): giải mã H.264 phần cứng qua VCS2 chạy** (3 ms/khung, 0 bỏ) trên volume dự phòng. Chờ test HEVC/ổn định; chưa known-good. Dùng hằng ngày: build-63 ★ hoặc build-66 nếu ổn.
- **2026-11-10 19:20:** build-64: giải mã VCS2 chạy nhưng ~1 s/khung (giật). **build-65** (= build-64 + r6 bộ đếm `WEXVCSDiag`) đã ghi USB, chờ `logs/b65/`. Dùng hằng ngày: build-63 ★.
- **2026-11-10 18:47:** **build-64** (= build-63 ★ + kext r5: params VideoMedia → VCS2) đã ghi USB, chờ test giải mã video. Lùi: build-63 ★.
- **2026-11-10 18:32:** **build-63 ★ known-good** (volume dự phòng 25G332: WEX 0.7.0-katana r4, Metal, VRAM 1536 MB, không video phần cứng). G5 (giải mã VCS2): disassemble xong, đề xuất r5 (params VideoMedia type 4/instance 2) — chờ người dùng duyệt.
- **2026-11-10 18:20:** build-62 ĐÃ TĂNG TỐC (FB TGL + IntelAccelerator + Metal, VRAM 1536 MB) trên volume dự phòng; panic giải mã video (VCS0 không có). **build-63** (= build-62 + kext r4, tắt video phần cứng) đã ghi USB 18:20, chờ test. ROADMAP G5: nghiên cứu VCS0→VCS2, chờ người dùng chép `AppleIntelTGLGraphics.kext` vào `logs/b62/tgl-driver/` (không commit binary Apple).
- **2026-11-10 17:53:** build-61 panic PAVPCommandCallback NULL+0xb8 (accelerator đã start). Sửa fork r3 (ép nhánh PAVP tắt, CI 42800957857). **build-62** (= build-61 + kext r3) đã ghi USB 17:53, chờ test MÁY B. Volume dự phòng đã lên 26.7.2 (25G332) — giữ, tắt tự cập nhật.
- **2026-11-10 17:30:** build-60 test: GT Complete nhưng FB không khởi động — VBT có eDP ở A+B và panel_type 0xFF → WEX bỏ panel. Sửa fork (r2, CI 42797617881). **build-61** (= build-60 + kext r2; snapshot tên `build-60-…-wex-r2-vbtpanel`) đã ghi USB 17:30. Chờ test MÁY B. Snapshot build-51/52 đã xoá; build-48 known-good giữ (người dùng: bản ổn định nhất, không xoá).
- **2026-11-10 17:03:** build-59 test: VBT #35 OK (FirmwarePorts status 1), GT ProfileMismatch → FB/accel WEX không chạy. **build-60 `vcs2`** (= build-59 + `-wex-adlp-allow-vcs2`) đã ghi USB 17:03; snapshot build-60 chưa tạo (chờ chọn xoá build-51 hay build-48 known-good). Chờ test MÁY B.
- **2026-11-10 16:46 — PLAN-wex-46a3:** build-59 `wex070-katana` (= build-56 + WhateverXe 0.7.0 tự build: patch #35 + cờ opt-in `-wex-adlp-allow-vcs2`, fork TrDiTu/WhateverXe `katana-46a3`) validate 0/0, snapshot; **đã ghi USB 16:56** (USB trước đó = build-58). MÁY B: volume dự phòng ĐÃ hạ WhateverXe-Graphics về 0.4.0 (17:00), theo `docs/wex-46a3/MACOS-STEPS.md` (thư mục chính). Dự kiến vẫn ProfileMismatch (VCS2-only); build-60 = +cờ VCS2.
- **Giai đoạn B — ĐÃ CÓ TĂNG TỐC (Metal 2).** Build mới nhất: **build-48 `cleanup`** ★ known-good (= build-47 + gỡ hẳn AMFIPass/Skywalk/IO80211Legacy). USB và ESP ổ trong = build-47 (chạy giống hệt build-48).
  1920×1080 @ 144 Hz, `xe-topo` 16390 (64 EU / L3 6). Hoạt động: Wi-Fi, Ethernet, touchpad (GPIO), Bluetooth, độ sáng, loa/mic,
  display sleep/wake, Vulkan (MoltenVK). Geekbench 7 CPU **2030 / 9646** (92 %/95 % Linux). Boot picker → đăng nhập **23 s**.
- **Không còn root patch OCLP** (2026-11-07): Wi-Fi = laobamac AirportItlwm-Tahoe v2.4.0-alpha (IO80211Family/IOSkywalkFamily gốc),
  audio = VoodooHDA 3.6.8 trong `/Library/Extensions` (MÁY B). AMFIPass đã bỏ (build-47); Wi-Fi 6 `itlwm_he=1`.
- Stack trên MÁY B: JulioNectar **@24450b4** (user-space) + NootedGreen JN + **patch v10** (kext md5 `eb2d2843`): GMSFIX, GMSFIX-FB,
  PAVPFIX, FENCEFIX, CURDIAG, XE-HWPAUTO; v9 mặc định XE-PM; v10 mặc định 64 EU/L3 6, V142 3, blmax 17741, dmc adlp.
  Plugin VA trong `/Library/GPUBundles` (không dùng khi thiếu `-ngreengva`).
- macOS 26.7.1 (25G241). Không cập nhật (phá stack đồ hoạ; AirportItlwm laobamac chỉ nạp Darwin 25).
- **Quy tắc boot-args**: kernel nhận ≤ 255 ký tự; bản sao của Lilu (`checkKernelArgument`) chỉ ~228 → cờ Lilu phải nằm trong 228 ký tự
  đầu; cờ đọc bằng `PE_parse_boot_argn` được tới 255. `bootarg-add` nối vào cuối → luôn kiểm độ dài/vị trí. build-48: 160.
- MÁY A (Claude Code) và MÁY B (Victus) là hai máy khác nhau, dùng chung một bản CachyOS. Chép EFI sang ESP chỉ từ Linux.
- USB EFI: phân vùng MACEFI (FAT32, 3 GB, USB 29,3 GB cùng Ventoy), mount `/run/media/cyra/MACEFI`; tên thiết bị đổi mỗi lần cắm
  (`/dev/sdb3` / `/dev/sdc3`) — luôn xác nhận qua `usb-deploy-guard`.
- Làm việc trong worktree `.claude/worktrees/bt-backlight-audio` (nhánh `bt-backlight-audio`; `EFI/` ở đây = build-46 = build-45 + config-install sửa).
  Các file gitignored (`_cache/`, `docs/hw-dump/`, …) nằm ở thư mục chính; worktree dùng symlink. Docs ở worktree mới hơn `main`.

## Việc tiếp theo / người dùng cần làm
- **ROADMAP (2026-11-06) kết thúc:** G1 hiệu năng iGPU ⏸ bỏ qua (GB7 GPU treo ở Feature Matching: render + compute cùng treo, stamp
  CCS 29 mồ côi sau reset; XE-GPUREC v3 không làm). G2 Vulkan ✅. G3 giải mã video ❌ dừng (build-42 `-ngreengva`: panic NULL+0x284
  trong `VTDecoderXPCService`; build-43 thêm `-ngreennopavpfix`: panic `PAVPCommandCallback` CR2 0xb8 lúc boot → PAVPFIX bắt buộc).
  G4 boot time ✅ build-39 `gfxrst=1` (38 → 23 s; `gfxrst=4` thử ở build-40, bỏ).
- **ĐANG THỬ (23:16): patch v11 XE-PAVPCTX** (opt-in `-ngreenpavpctx`, tạo context PAVP để G3 không panic) — kext v11 md5 5adbfbb7; build-44 (+`-ngreenpavpctx`) ghi USB 23:24 → **panic lúc boot** (NULL+0x30 trong `startGraphicsEngine` gốc) → v11 thất bại. **USB đang là build-44 (không boot được)**; `EFI/` = build-41. Kế hoạch: BUILD-LOG 23:32 (G3 cần phân tích driver Apple → issue cho JN) → build-45 (+`-ngreengva`).
- **XONG 2026-11-07:** build-45 Wi-Fi laobamac + VoodooHDA → không root patch (POSTINSTALL-RUNBOOK §6, §7). build-45 ★ known-good; build-46 (config-install sửa) ghi USB 00:35. build-47 (`itlwm_he=1`, AMFIPass tắt) OK trên MÁY B, người dùng chép sang ESP; build-48 dọn dẹp ★. **Nhánh `nvidia-gpu` (worktree riêng): build-49 thử NullMoth NVIDIA driver — `docs/NVIDIA-RUNBOOK.md`.**
- **Người dùng cần:** (1) chép build-41 (hoặc build-45 nếu ổn) sang ESP ổ trong (từ Linux). Tuỳ chọn: soạn issue cho JN (GB7 hang, panic giải mã).
- Lỗi phụ đã thấy: BCS treo `MI_FLUSH_DW` ~30–60 s sau mỗi boot (Apple tự phục hồi); panic chia 0 trong `fbTimingsWorker`
  (`-ngreenfixbootmode`) 1 lần lúc boot build-42; panic AirportItlwm 20:03:20 1 lần; `mediaanalysisd` gây GPU reset 19:51.
- Không chạy Geekbench 7 GPU; không bật `-ngreengva`.
- known-good hiện có: build-26, 29, 31, 37, 38, 41, 45, **48**. Đường lui: build-45 → build-41 (cần root patch Modern Wi-Fi + Audio) → `config-install.plist`.
- Quyết định trước khi đẩy repo public: EFI chứa kext không có license (ECEnabler, USBToolBox, RTL8111) — xem mục Rủi ro.
- Còn hoãn (`docs/DEFERRED.md`): sleep/wake hệ thống, tai nghe chỉ kênh trái (D14).

## Quy tắc người dùng đặt
- **`powermetrics` được phép dùng lại** (người dùng 2026-11-10 20:44; panic 2026-11-06 chỉ xảy ra 1 lần). Trên stack WEX đây là công cụ đo công suất/nhiệt chính (`xe-monitor.py` cần sysctl của NootedGreen).
- **build-48 (known-good) KHÔNG BAO GIỜ được xoá** — bản ổn định nhất (người dùng 2026-11-10 17:25, nhắc lại 18:32).
- **Snapshot (2026-11-07):** được xoá snapshot known-good đã cũ hơn 5 bản so với build mới nhất (ví dụ build mới nhất 49 → known-good ≤ 44). Vẫn báo người dùng khi xoá.
- **KHÔNG đọc lịch sử commit của repo này** (git log/show/các commit cũ). Chỉ dùng trạng thái hiện tại + `docs/hw-dump/` + repo tham chiếu.

## Đã được người dùng duyệt
- 2026-11-02 GRAPHICS-PLAN: fork JulioNectar @6f03560 + ngreen-eu=64 ngreen-l3=6; SIP 0x0A13 + amfi_get_out_of_my_way=1 (chấp nhận mất sleep/màn hình ngoài, rủi ro panic); trình tự graphics-prep → install.sh → graphics-v1; máy B đã sao lưu
- 2026-11-02 DRIVER-MATRIX: dùng tất cả trừ audio (#14,#15) và Bluetooth (#8) — tạm BỎ QUA; ECEnabler/USBToolBox/RTL8111 không có license → chấp nhận dùng cá nhân; XHCI-unsupported → tự viết injector chỉ Info.plist
- 2026-11-02 Wi-Fi build-06: dùng payloads OCLP-CustoMac (IOSkywalkFamily, IO80211FamilyLegacy, AMFIPass — không phải release asset, binary Apple không commit), SIP 0x803 + AMFIPass (người dùng đồng ý hệ quả bảo mật)
- 2026-11-02 touchpad: dùng fork lzhoang2801/VoodooI2C 3.0.0 (bản 2.9.1 chính thức không có 51E8)
- 2026-11-03 F1: vá NootedGreen (GMSFIX…), build kext trên MÁY B; F2 nếu F1 thất bại (không cần)
- 2026-11-05 build-21 known-good; xoá snapshot 12, 14, 15 (người dùng), 16, 17 (xoay vòng, đã báo)
- 2026-11-05 dọn repo: xoá video `logs/*.mp4`, log cũ, patch gộp v1–v6, validate cũ; `.gitignore` thêm video + kext Apple + `.claude/worktrees/`

## Quyết định quan trọng
- Dump phần cứng nhận ngày 2026-11-01; phân tích ở `docs/MACHINE-ANALYSIS.md`.
- Dữ kiện đã xác nhận từ dump: board 8A4F, BIOS F.34, iGPU 46A3 = GT1 UHD **64 EU** (4 DSS, mask 0x33), Wi-Fi = AX210,
  audio ALC245, touchpad ELAN0788 (I2C0.TPD0), dGPU tại `\_SB_.PC00.PEG1.PEGP`, **CFG Lock đang bật**, VT-d đang bật.

## Cập nhật 2026-11-02 (người dùng trả lời + giải mã ACPI)
- Người dùng: `iasl` đã cài (20251212); `laptop-specs.md` đã sửa (46A3 64 EU, AX210); BIOS: **không có** Above 4G Decoding, **không có**
  DVMT Pre-Allocated; Secure Boot = Disabled; stolen memory thật = không rõ; **L3 bank = 6**; panel 144 Hz.
- Giải mã ACPI vào `_cache/acpi-src/` (DSDT.dsl + SSDT*.dsl). Lưu ý: `iasl -d DSDT.aml` phải chạy riêng, nạp kèm SSDT báo AE_ALREADY_EXISTS (`PEGP._S0W`).
- dGPU: `\_SB.PC00.PEG1.PEGP` (ADR 0x00010000/0), DSDT chỉ khai báo rỗng; `_PS0/_PS3/_OFF/_DSM` nằm ở SSDT14 (và SSDT11 `SGPO`, SSDT16 `L23D/DL23`).
  `_OFF` gọi `\_SB.PC00.PEG1.PXP._OFF` nếu có (`CondRefOf`); chưa thấy định nghĩa `PXP_` trong DSDT/SSDT đã dump → đường tắt dGPU CHƯA XÁC MINH.
- Touchpad: `\_SB.PC00.I2C0.TPD0`, `_HID` ban đầu MSFT1234 → `_INI` đổi thành ELAN0788; I2C 0x15 @ 400 kHz (0x61A80);
  `_CRS`: OSYS < 0x07DC (không phải Win10+) trả về chỉ SBFI (ngắt APIC), ngược lại tuỳ TPDM (0 = GpioInt qua `\_SB.GPI0`). GPI0 `_HID` = INTC1055 (hoặc PNP0C02 nếu GPHD=1).
  → macOS báo OSYS thấp nên nhiều khả năng cần SSDT-XOSI/SSDT-GPI0 hoặc chế độ polling của VoodooI2C; CHƯA XÁC MINH trên máy thật.
- Repo clone: victus-r1 (sulthonuladib/victus-15-fa0xxx-hackintosh) @ e3802fa; AGENTS.md đã đổi thành `*.ref-ignored`. Có `scan/ACPI` để đối chiếu.

## Pha 1 — 2026-11-02
- `docs/DRIVER-MATRIX.md` lập xong (23 thiết bị + 7 SSDT). Chưa tải binary, chưa có `EFI/`, `docs/SOURCES.md` chưa tạo (tạo khi `release-fetch`).
- Phát hiện chính: Tahoe gỡ AppleHDA (audio cần SimpleHDA — không license, chứa binary Apple — hoặc root patch OCLP); IntelBluetoothFirmware upstream 2.4.0
  lỗi với `8087:0032` trên Tahoe, chỉ fork lshbluesky 2.5.2 có bằng chứng; AirportItlwm-Tahoe v1.0.0 chưa kiểm định 25G241; VoodooI2C 2.9.1 có 51E8 + INTC1055;
  RTS5228 KHÔNG CÓ DRIVER; ECEnabler/SimpleHDA/USBToolBox/RTL8111 không có SPDX license trên GitHub; refs dùng kext nightly (không theo).

## Tải binary — 2026-11-02 (release-fetch, ghi ở docs/SOURCES.md, Used in EFI = not yet)
- OpenCore 1.0.8, Lilu 1.7.2, VirtualSMC 1.3.8, CpuTopologyRebuild 2.0.2, RestrictEvents 1.1.6, WhateverGreen 1.7.1, AirportItlwm-Tahoe v1.0.0
  (zip/exec/Info.plist khớp README), RealtekRTL8111 v3.0.0, NVMeFix 1.1.3, VoodooI2C 2.9.1, VoodooPS2 2.3.7, BrightnessKeys 1.0.3, USBToolBox 1.2.0, ECEnabler 1.0.6.
- Ghi chú công cụ: `release-fetch` cần `GITHUB_TOKEN`; dùng `export GITHUB_TOKEN="$(gh auth token)"` trong lệnh (không lưu, không in). Không có token → 403 rate limit.

## Pha 2 — 2026-11-02
- 6 SSDT tự viết từ DSDT thật (`docs/acpi-src/`, iasl 0 lỗi): PLUG-ALT, EC-USBX, AWAC, XOSI (+patch `_OSI`→`XOSI` chỉ DSDT), DGPU-OFF (`PEGP._INI`→`PEGP._OFF`→`PEG1.PXP._OFF`, SSDT4:3615), SBUS-MCHC. Không cần SSDT-GPI0.
- Đính chính: VoodooI2C 2.9.1 chính thức không có 51E8 → fork lzhoang2801 3.0.0 (người dùng duyệt).
- `_cache/acpi-src` đổi tên thành `_cache/acpi` (theo skill ssdt-authoring).
- Lỗi công cụ ghi nhận: `plist_edit.py` guard từ chối ROM toàn 0 (ROM là data) → ROM giữ mẫu 112233445566.

## Rà soát workspace 2026-11-02 (theo yêu cầu người dùng)
- Đã đọc: PROMPT.md, README-SETUP.md, .claude/settings.json, REFERENCES.md, các SKILL.md liên quan, deploy_usb.py, tools/lib/smbios.py, .remember/.
- Sai sót phát hiện & sửa ở build-02: spoof iGPU (trái PROMPT Pha 2), thiếu GPU-STRATEGY.md, thiếu config-install.plist, ROM mẫu chặn tiêm SMBIOS.
- Còn thiếu theo PROMPT.md: Pha 4 (`docs/INSTALL-RUNBOOK.md`, `docs/POSTINSTALL-RUNBOOK.md`, TEST-PLAN đầy đủ + "mốc trước tăng tốc", cách lấy bộ cài 25G241).
- Git: settings.json chặn `git push`; `.gitignore` đã có `.claude/worktrees/` (2026-11-05). EFI/ chứa kext không có license (ECEnabler, USBToolBox, RTL8111) — cân nhắc trước khi đưa lên repo public.

## Bản build
- Mới nhất: **build-43 `gva-nopavp`** (thử, panic). Đang dùng: **build-41 `v10-defaults`** ★ (USB). `EFI/` ở worktree = build-41.
- Snapshot 10/10 (`snapshots/`): build-26★, 29★, 31★, 37★, 38★, 39, 40, 41★, 42, 43. Bản cũ nhất không known-good: build-39.
  `snapshot.py` không tự bỏ qua known-good khi xoay vòng → khi đầy phải xoá tay bản cũ nhất không known-good (hỏi người dùng).
- Đường lui: build-41 → build-38 → `EFI/OC/config-install.plist` (không tăng tốc).

## Repo tham chiếu đã clone (tên @ commit)
- victus-r1 @ e3802fa94ea26f6616d6ad87e494120bd407ab60
- cheseecake (cheseecake/i3-1220p-macos-gpu) @ 788158727daf9ec546888910e7eb9c9028d9d944
- juliornectar (JulioNectar/Hackintosh-XPS13Plus-IrisXe-Tahoe; tên thư mục gõ nhầm) @ 24450b476d7ca025b83c85d7b8362caf3234d2f2 (cập nhật 2026-11-06; MÁY B cài 24450b4 từ 20:12)
- khucxtriendev (khucxtriendev/irisxegraphic-i712800h-efi) @ 26ee7f337831bc8c225dfcdfeb609bba444ac31e
- sgiammori-nootedgreen (sgiammori/NootedGreen) @ 95f81898be65cb9f7b3d370ca78054be4cc8a62d (2026-11-06; chứa bundle driver Apple 16.0.32 — chỉ dùng tra symbol cho log panic, không phân phối)

## Rủi ro / CHƯA XÁC MINH đang mở
- FENCEFIX sau display sleep/wake hoặc đổi chế độ màn hình (fence có thể bị ghi lại từ giá trị cache của FB).
- Ổn định dài hạn của stack (GPU hang ngẫu nhiên đã được JN ghi nhận); chưa chạy tải nặng.
- PAVPFIX tắt đường PAVP → không phát được video có DRM.
- Kext không có SPDX license trong EFI: ECEnabler, USBToolBox, RTL8111 (chấp nhận dùng cá nhân; cân nhắc trước khi public).
- Patch NootedGreen là sửa đổi theo Thou Shalt Not Profit 1.0 — chỉ phi lợi nhuận.

## Đã giải quyết (tham khảo)
- Boot-args bị cắt ở 255 (Lilu ~228) → rút còn 224 (H1).
- Panic `IGAccelTask::withOptions` CR2 0xc78 → GMSFIX (GMS 0xFE giải mã sai) (H3).
- Panic WindowServer `getAttributeExt+0x25` → GMSFIX-FB (H4). Panic `PAVPCommandCallback` CR2 0xb8 → PAVPFIX.
- Con trỏ vỡ → FENCEFIX (fence X-tile 64 MB tràn qua stolen 60 MB). Bác bỏ: topology/DSS (H5), băng thông 144 Hz (H7), stride (H6), lệch trang GGTT.
- Stolen memory đo được 60 MB (GGC 0xFEC1); dGPU tắt bằng SSDT-DGPU-OFF hoạt động (build-05); touchpad chạy polling (`force-polling` trên I2C0).
