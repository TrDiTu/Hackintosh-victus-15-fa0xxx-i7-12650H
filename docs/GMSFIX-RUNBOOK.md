> **Cập nhật 2026-11-05:** các patch gộp v1–v6 đã xoá khỏi `patches/`. Cài mới: dùng **`patches/nootedgreen-gmsfix-v7-jn6f03560.patch`** áp lên JN `6f03560`. Chuỗi `vN-to-vM` chỉ dành cho source đã áp các bản trước.

# GMSFIX-RUNBOOK — build NootedGreen có patch GMSFIX trên MÁY B

Mục đích: sửa lỗi driver TGL giải mã stolen memory 60 MB (GMS 0xFE) thành 8128 MB → panic `IGAccelTask::withOptions` CR2 0xc78.
Phân tích: `docs/GRAPHICS-PANIC-ANALYSIS.md`. Patch: `patches/nootedgreen-gmsfix-jn6f03560.patch`
(sha256 `94a0ffa9bcc372b21f59abd022122a82ab10f2ccd41a41327e2b4a81844192d8`).

Chỉ build lại **NootedGreen.kext**. KHÔNG chạy `install.sh` (user-space JN 6f03560 đang cài giữ nguyên). Không cần SIP/AMFI khác.

## Bước 0 — Boot MÁY B bằng build-10 (USB hiện tại, không spoof)

## Bước 1 — Đưa file patch sang MÁY B
Chép `patches/nootedgreen-gmsfix-jn6f03560.patch` từ MÁY A sang MÁY B (ví dụ bạn tự chép vào gốc USB MACEFI, ngoài thư mục `EFI`, rồi copy về `~/`). Kiểm:
```
shasum -a 256 ~/nootedgreen-gmsfix-jn6f03560.patch
```
Phải ra `94a0ffa9bcc372b21f59abd022122a82ab10f2ccd41a41327e2b4a81844192d8`.

## Bước 2 — Áp patch và build
```
cd ~/xe-stack
git rev-parse HEAD                      # phải là 6f03560ef9694f9826caae15624d4a6cb1bf9ffc
git status --short                      # phải trống (chưa sửa gì)
git apply --check ~/nootedgreen-gmsfix-jn6f03560.patch && git apply ~/nootedgreen-gmsfix-jn6f03560.patch
git status --short                      # 3 file M: kern_gen11.cpp, kern_green.cpp, kern_green.hpp
zsh build-nootedgreen.sh                # in "built .../build/NootedGreen.kext"
md5 -q build/NootedGreen.kext/Contents/MacOS/NootedGreen
shasum -a 256 build/NootedGreen.kext/Contents/MacOS/NootedGreen
strings build/NootedGreen.kext/Contents/MacOS/NootedGreen | grep -c GMSFIX     # phải > 0
```
Gửi Claude toàn bộ output. Chép **cả thư mục** `~/xe-stack/build/NootedGreen.kext` vào gốc USB MACEFI (ngoài `EFI`).

Nếu `git apply --check` báo lỗi: dừng, gửi output (không sửa tay).
Gỡ patch sau này: `cd ~/xe-stack && git apply -R ~/nootedgreen-gmsfix-jn6f03560.patch`.

## Bước 3 — Claude dựng build-19 `gmsfix` = build-17 + kext mới (boot-args giữ 224 ký tự), validate, snapshot, hỏi trước khi ghi USB.

## Bước 4 — Boot build-19 và thu bằng chứng
Quay video/chụp màn hình verbose, tìm các dòng:
- `XeNG GMSFIX: GMS=0xfe real=60 MB (Apple would use 8128 MB) patch=OK` — patch đã áp.
- `XeNG GMSFIX diag[1]: fbreg=… mm=… seg=0x… range=0x…+0x…` — kỳ vọng `seg=0x3c00000` (60 MB). Nếu `fbreg=1` thì driver đi nhánh khác (stolenMemInfo) → báo Claude.
- `XeNG GMSFIX diag: IGAccelTask::withOptions returned NULL` — còn lỗi ở bước sau.

Nếu panic: boot build-10, chép `.panic` mới vào `logs/`. Nếu vào desktop:
```
log show --last boot --predicate 'eventMessage CONTAINS "GMSFIX"'
kmutil showloaded | grep -iE 'nootedgreen|hookcase|AppleIntelTGL'
ioreg -rc IntelAccelerator -d1 | grep -E 'xe-topo|rowchk'
system_profiler SPDisplaysDataType
```
+ Wi-Fi / Ethernet / touchpad còn chạy không.

## Nếu GMSFIX không giúp → F2 (hook `IOPCIDevice::extendedConfigRead16` trả GMS dạng 32 MB) — Claude viết patch mới.

## v2 (2026-11-03) — thêm vá framebuffer TGL
Lý do: `docs/GRAPHICS-PANIC-ANALYSIS.md` §7. Trên MÁY B source đã có v1 → áp **bản tăng thêm**:
`patches/nootedgreen-gmsfix-v1-to-v2.patch` (sha256 `61023788c037bc87ca761465173a13fb79efba21014c6c2e449dd9ff667659ae`).
(Bản gộp áp lên JN gốc: `patches/nootedgreen-gmsfix-v2-jn6f03560.patch`, sha256 `afe104ba41638a450dcac504218d543740f26f7196b392c13669923c7a2a335a`.)
```
shasum -a 256 ~/patches/nootedgreen-gmsfix-v1-to-v2.patch
cd ~/xe-stack
git status --short                      # 3 file M (v1 đang áp)
git apply --check ~/patches/nootedgreen-gmsfix-v1-to-v2.patch && git apply ~/patches/nootedgreen-gmsfix-v1-to-v2.patch
zsh build-nootedgreen.sh
md5 -q build/NootedGreen.kext/Contents/MacOS/NootedGreen
shasum -a 256 build/NootedGreen.kext/Contents/MacOS/NootedGreen
strings build/NootedGreen.kext/Contents/MacOS/NootedGreen | grep -c GMSFIX     # phải = 7
```
Rồi thay `NootedGreen.kext` ở gốc USB MACEFI bằng bản mới. Khi boot (build-20), tìm trong verbose:
`XeNG GMSFIX fb-patch: real=60 MB patch=OK`, `XeNG GMSFIX fb: FBController::start ret=1 stolen(0xde4)=0x3c00000`,
và KHÔNG còn `Could not register with IOFB!`. Nếu ret=0: tìm dòng `Insufficient stolen memory`.

## v3 (2026-11-04) — thêm PAVPFIX
Lý do: `docs/GRAPHICS-PANIC-ANALYSIS.md` §8. Source trên MÁY B đang là v2 → áp bản tăng thêm
`patches/nootedgreen-gmsfix-v2-to-v3.patch` (sha256 `4e8b081e291f4b5c24f3b63bd381656d9947ac3afa490bb36ad1f60537652efe`).
(Bản gộp áp lên JN gốc: `patches/nootedgreen-gmsfix-v3-jn6f03560.patch`, sha256 `3ad3a3d6aa996ea88a1ef212946e5969cb3271ef2717e52fcf65cf1220ecc2c8`.)
```
shasum -a 256 ~/patches/nootedgreen-gmsfix-v2-to-v3.patch
cd ~/xe-stack
git apply --check ~/patches/nootedgreen-gmsfix-v2-to-v3.patch && git apply ~/patches/nootedgreen-gmsfix-v2-to-v3.patch
zsh build-nootedgreen.sh
md5 -q build/NootedGreen.kext/Contents/MacOS/NootedGreen
shasum -a 256 build/NootedGreen.kext/Contents/MacOS/NootedGreen
strings build/NootedGreen.kext/Contents/MacOS/NootedGreen | grep -c -E 'GMSFIX|PAVPFIX'     # phải = 9
```
Thay `NootedGreen.kext` ở gốc USB. Verbose build-21: `XeNG PAVPFIX: patch=OK`.

## v4 (2026-11-05) — CURDIAG (chỉ chẩn đoán con trỏ, không đổi hành vi)
Source trên MÁY B đang là v3 → áp `patches/nootedgreen-gmsfix-v3-to-v4.patch` (sha256 `63427e0cff66f57c31fbaa2bc9da0f37e5f075b7693935a9a0d84f945ed2be44`).
(Bản gộp trên JN gốc: `patches/nootedgreen-gmsfix-v4-jn6f03560.patch`, sha256 `718b1a26f8e5f6b02c6e28bafc57bbd5c0be1313542df7d3ae7baba6cb539413`.)
```
shasum -a 256 ~/patches/nootedgreen-gmsfix-v3-to-v4.patch
cd ~/xe-stack
git apply --check ~/patches/nootedgreen-gmsfix-v3-to-v4.patch && git apply ~/patches/nootedgreen-gmsfix-v3-to-v4.patch
zsh build-nootedgreen.sh
md5 -q build/NootedGreen.kext/Contents/MacOS/NootedGreen
shasum -a 256 build/NootedGreen.kext/Contents/MacOS/NootedGreen
strings build/NootedGreen.kext/Contents/MacOS/NootedGreen | grep -c -E 'GMSFIX|PAVPFIX|CURDIAG'     # phải = 10
```
Thay `NootedGreen.kext` ở gốc USB. Sau khi boot build-23, rê chuột, đổi hình con trỏ (ô chữ, nút), rồi:
`ioreg -rc IntelAccelerator -d1 | grep xe-cur`

## v5 (2026-11-05) — CURDIAG2 (so ảnh con trỏ CPU ghi vs phần cứng đọc; chỉ chẩn đoán)
Source trên MÁY B đang là v4 → áp `patches/nootedgreen-gmsfix-v4-to-v5.patch` (sha256 `42a828b1cbf757dbd7367a78c8f729e9969356839e987abbd9f1aea1ebcaf4a8`).
(Bản gộp trên JN gốc: `patches/nootedgreen-gmsfix-v5-jn6f03560.patch`, sha256 `6c2b1fed4389c666cc7927c74d8c001a9b6c4536d765686503617cb711031ddb`.)
```
shasum -a 256 ~/patches/nootedgreen-gmsfix-v4-to-v5.patch
cd ~/xe-stack
git apply --check ~/patches/nootedgreen-gmsfix-v4-to-v5.patch && git apply ~/patches/nootedgreen-gmsfix-v4-to-v5.patch
zsh build-nootedgreen.sh
md5 -q build/NootedGreen.kext/Contents/MacOS/NootedGreen
strings build/NootedGreen.kext/Contents/MacOS/NootedGreen | grep -c -E 'xe-cur-rows|xe-cur-pte'     # phải >= 3
```
Sau khi boot: `ioreg -rc IntelAccelerator -d1 | grep xe-cur` (cần `rows-cpu`, `rows-gpu`, `diff`, `pte0..3`, `gaddr`, `stolenoff`).

## v6 (2026-11-05) — CURDIAG3 (fence + segment; chỉ chẩn đoán)
Source trên MÁY B đang là v5 → áp `patches/nootedgreen-gmsfix-v5-to-v6.patch` (sha256 `34e37ed6816193e15ca98f25da62afd9dbbb95e1a9ebe018b35ab288b9e199f9`).
(Gộp: `patches/nootedgreen-gmsfix-v6-jn6f03560.patch`, sha256 `6c62bcd82f4df1925934dd9d1b4e13d0013ea5c19ea4b1db1825d5c7eb111081`.)
```
cd ~/xe-stack && git apply --check ~/patches/nootedgreen-gmsfix-v5-to-v6.patch && git apply ~/patches/nootedgreen-gmsfix-v5-to-v6.patch
zsh build-nootedgreen.sh && md5 -q build/NootedGreen.kext/Contents/MacOS/NootedGreen
strings build/NootedGreen.kext/Contents/MacOS/NootedGreen | grep -c -E 'xe-fence|xe-mm-'     # phải >= 7
```
Sau khi boot: `ioreg -rc IntelAccelerator -d1 | grep -E 'xe-cur|xe-fence|xe-mm|xe-acc'`

## v7 (2026-11-05) — FENCEFIX (sửa con trỏ)
Source trên MÁY B đang là v6 → áp `patches/nootedgreen-gmsfix-v6-to-v7.patch` (sha256 `26e41045cc65385fbbce81a7ceaae7f7794b23c70244e99903cc3a50c518b81d`).
(Gộp: `patches/nootedgreen-gmsfix-v7-jn6f03560.patch`, sha256 `1ecd5bb01879de1f347a0d2dd5f5b05cd460a4235432748f7a67365f760b4ee6`.)
```
cd ~/xe-stack && git apply --check ~/patches/nootedgreen-gmsfix-v6-to-v7.patch && git apply ~/patches/nootedgreen-gmsfix-v6-to-v7.patch
zsh build-nootedgreen.sh && md5 -q build/NootedGreen.kext/Contents/MacOS/NootedGreen
strings build/NootedGreen.kext/Contents/MacOS/NootedGreen | grep -c -E 'FENCEFIX|xe-fencefix'     # phải >= 3
```
Sau khi boot: con trỏ phải lành; `ioreg -rc IntelAccelerator -d1 | grep -E 'xe-fence|xe-cur-ctl'` → `xe-fencefix-n` ≥ 1, `xe-fencefix-end` = 0x3bff000 (62910464), `xe-fence-hit` = 255.

## v8 — XE-HWPAUTO (2026-11-06, người dùng duyệt): HWP desired = 0 (xung tự chủ)
Chỉ sửa `src/NootedGreen/kern_xepm.cpp`: sysctl `debug.xepm.hwpauto` (0/1, đổi trực tiếp, root) + boot-arg `ngreenpmauto=1`;
khi bật, `xpSetMult` xoá trường desired (bit 16–23 của MSR 0x774) sau mỗi lần XCPM ghi. Mặc định TẮT → kext v8 chạy y hệt v7.
Kiểm trên MÁY A: `git apply --check` sạch (v7→v8 và base→v8); `clang++ -fsyntax-only` (MacKernelSDK 3f75008 + Lilu 0249c3a): 0 lỗi, cảnh báo y như v7.
```
cd ~/xe-stack
git apply --check ~/patches/nootedgreen-gmsfix-v7-to-v8.patch && git apply ~/patches/nootedgreen-gmsfix-v7-to-v8.patch
zsh build-nootedgreen.sh
md5 -q build/NootedGreen.kext/Contents/MacOS/NootedGreen
shasum -a 256 build/NootedGreen.kext/Contents/MacOS/NootedGreen
strings build/NootedGreen.kext/Contents/MacOS/NootedGreen | grep -c HWPAUTO     # phải > 0
```
(`~/xe-stack` phải đang ở v7. Nếu không chắc: dùng bản gộp `nootedgreen-gmsfix-v8-jn6f03560.patch` trên cây JN 6f03560 sạch.)
Chép `build/NootedGreen.kext` vào gốc USB MACEFI (ngoài `EFI`) → Claude dựng build-36 = build-35 + kext v8.
Thử: `sudo sysctl -w debug.xepm.hwpauto=1` → `XEFREQ_SAMPLES=1 ./xe-freq 1 30` + Geekbench 7; so với `hwpauto=0`.

## v9 — nâng stack lên JN `24450b4` + giải phóng boot-args (2026-11-06, người dùng duyệt 19:49)
Lý do: GB7 GPU treo ở Feature Matching trên build-37 (BUILD-LOG). JN `24450b4` có libxedrv v21–v24 (compute được xếp thứ tự
với render/blit, barrier compute hoạt động, sửa blur) + kernel XE-PORTGUARD, XE-AUXBL, XE-HWCAPS114C (JN ghi "testing").
Patch: `patches/nootedgreen-gmsfix-v9-jn24450b4.patch` (sha256 `3685fa72fadfde9dc077c5f1ab2b738732003adccf18ca4321e3776eaa33cf0a`)
= v8 áp lên JN 24450b4 + `-ngreenpm` mặc định HWPAUTO bật và C8/C10 tắt (bỏ được ` ngreenpmcst=0 ngreenpmauto=1`, 29 ký tự).
Hai boot-arg đó vẫn ghi đè được (`ngreenpmauto=0`, `ngreenpmcst=1`).
Kiểm trên MÁY A: `git apply --check` sạch trên JN 24450b4; `clang++ -fsyntax-only` 0 lỗi, số cảnh báo bằng JN gốc. Chưa build/chạy.

Lần này chạy **`install.sh`** (khác v1–v8): libxedrv là user-space, chỉ cài lại mới có tác dụng. `install.sh` build kext từ
chính cây `~/xe-stack` → **phải áp patch trước**. Nó chỉ ghi vào `/Library/GPUBundles` và `/Library/Extensions`, không đụng
root patch OCLP (Wi-Fi/Audio nằm ở volume hệ thống). Boot bằng build-37 (đang chạy stack) để `install.sh` vào chế độ update.

Bước 0 — sao lưu (để quay về):
```
cp -R /Library/GPUBundles ~/xe-backup-GPUBundles-6f03560
mkdir -p ~/xe-backup-LE-6f03560 && cp -R /Library/Extensions/AppleIntelTGL* /Library/Extensions/AppleIntelGraphicsShared.bundle /Library/Extensions/HookCase.kext ~/xe-backup-LE-6f03560/
cd ~/xe-stack && git rev-parse HEAD && git diff > ~/xe-stack-v8-local.diff && git status --short
```
`git rev-parse` phải ra `6f03560…`; `git status` chỉ có 4 file M của v8 (kern_gen11.cpp, kern_green.cpp, kern_green.hpp, kern_xepm.cpp).

Bước 1 — đổi source sang 24450b4 + v9 (chép `patches/nootedgreen-gmsfix-v9-jn24450b4.patch` vào `~/patches/`):
```
shasum -a 256 ~/patches/nootedgreen-gmsfix-v9-jn24450b4.patch     # 3685fa72…cf0a
cd ~/xe-stack
git checkout -- src/NootedGreen
git fetch origin && git checkout 24450b476d7ca025b83c85d7b8362caf3234d2f2
git rev-parse HEAD                                                 # 24450b476d7c…
git apply --check ~/patches/nootedgreen-gmsfix-v9-jn24450b4.patch && git apply ~/patches/nootedgreen-gmsfix-v9-jn24450b4.patch
git status --short                                                 # 4 file M như trên
```
Bước 2 — xem kiểm tra, rồi build + cài:
```
zsh install.sh --check       # phải: macOS 25G241, device-id 9A49, NootedGreen loaded, "Mode: update"
zsh install.sh               # build NootedGreen + HookCase + Metal driver/libxedrv/shader compiler, cài (sudo)
md5 -q build/NootedGreen.kext/Contents/MacOS/NootedGreen
shasum -a 256 build/NootedGreen.kext/Contents/MacOS/NootedGreen
strings build/NootedGreen.kext/Contents/MacOS/NootedGreen | grep -c -E 'HWPAUTO|PORTGUARD|GMSFIX'   # phải > 0
```
**Không làm theo phần cuối của `install.sh`** (mount `disk0s1` và chép kext vào ESP): ESP chỉ được sửa từ Linux.
Chép cả thư mục `build/NootedGreen.kext` vào gốc USB MACEFI (ngoài `EFI`), gửi Claude output các lệnh trên.
Lỗi ở bất kỳ bước nào → dừng, gửi output (không sửa tay).

Bước 3 — Claude dựng **build-38** = build-37 + kext v9, boot-args bỏ ` ngreenpmcst=0 ngreenpmauto=1` (255 → 226), validate, snapshot,
hỏi trước khi ghi USB. Sau `install.sh`, lần vào macOS kế tiếp phải boot **build-38 từ USB** — không boot ESP ổ trong (còn build-37,
kext v8): user-space 24450b4 + kernel v8 là tổ hợp chưa ai thử. Vào CachyOS ở giữa thì không sao.

Bước 4 — kiểm sau boot build-38:
```
kmutil showloaded | grep -iE 'nootedgreen|hookcase'
system_profiler SPDisplaysDataType | grep -i metal
sysctl debug.xepm.hwpauto debug.xepm.cst debug.xepm.route     # 1 / 0 / 1 (không còn boot-arg)
ioreg -rc IntelAccelerator -d1 | grep -E 'xe-topo|xe-fencefix-n|xe-rowchk-post'
sudo dmesg | grep -E 'PORTGUARD|HWCAPS' | head
```
Rồi chạy lại GB7 GPU **sau khi lưu hết việc đang làm** (vẫn có thể treo).

Quay về: boot build-37 (USB) → `cd ~/xe-stack && git checkout -- src/NootedGreen && git checkout 6f03560ef9694f9826caae15624d4a6cb1bf9ffc
&& git apply ~/xe-stack-v8-local.diff && zsh install.sh` (cài lại user-space 6f03560), hoặc chép lại thư mục sao lưu ở Bước 0 (sudo).
Tắt riêng từng sửa của libxedrv không cần cài lại: tạo `/private/var/tmp/xedrv.off` chứa `o` (bỏ xếp thứ tự compute), `b` (bỏ barrier), `x` (bỏ sửa blur).

## v10 — mặc định cho máy này, bỏ 5 boot-arg (2026-11-06, người dùng đề xuất 21:34)
Chỉ sửa `src/NootedGreen/kern_gen11.cpp`, 4 chỗ — khi KHÔNG có boot-arg thì dùng giá trị của máy này (boot-arg vẫn ghi đè):
topology 64 EU / L3 6 (`gTopoSs` 8, `gTopoL3` 6; ghi cứng, không đọc fuse — JN ghi rằng đọc fuse lúc boot làm treo boot),
`ngreenV142` = 3, `ngreenblmax` = 17741, `ngreen-dmc` = `adlp`. Giải phóng 72 ký tự boot-args (235 → 163).
Patch: `patches/nootedgreen-gmsfix-v9-to-v10.patch` (sha256 `9599beee000c1386fe1228fddfc6a96601300abf1d856739a75e7192fb0c6b6d`);
gộp trên JN 24450b4: `patches/nootedgreen-gmsfix-v10-jn24450b4.patch` (sha256 `1b232960e5e954a805295bc22392a63533c0227f7d412c68f9ef91eeb5180567`).
Kiểm trên MÁY A: apply-check sạch; `clang++ -fsyntax-only` kern_gen11 0 lỗi, 21 cảnh báo = JN gốc. Chưa build/chạy.
```
cd ~/xe-stack
git rev-parse HEAD                     # 24450b476d7c…
shasum -a 256 ~/patches/nootedgreen-gmsfix-v9-to-v10.patch     # 9599beee…6b6d
git apply --check ~/patches/nootedgreen-gmsfix-v9-to-v10.patch && git apply ~/patches/nootedgreen-gmsfix-v9-to-v10.patch
zsh build-nootedgreen.sh
md5 -q build/NootedGreen.kext/Contents/MacOS/NootedGreen
shasum -a 256 build/NootedGreen.kext/Contents/MacOS/NootedGreen
strings build/NootedGreen.kext/Contents/MacOS/NootedGreen | grep -c -E 'HWPAUTO|PORTGUARD|GMSFIX'   # như v9 (11)
```
Chỉ build lại kext (`build-nootedgreen.sh`), **không** cần `install.sh` (user-space không đổi). Chép `build/NootedGreen.kext` vào gốc USB MACEFI.

Cùng lúc (cho G3, vô hại khi chưa có `-ngreengva` — plugin không được dùng): build + cài plugin VA (JN INSTALL "Hardware video decode"):
```
zsh macos/vadriver/build-vadriver.sh build/deps/NootedGreen/sle_Internal/sle
sudo rm -rf /Library/GPUBundles/AppleIntelTGLGraphicsVADriver.bundle
sudo ditto macos/out/AppleIntelTGLGraphicsVADriver.bundle /Library/GPUBundles/AppleIntelTGLGraphicsVADriver.bundle
```
build-41 = build-39 + kext v10 + boot-args 163 (bỏ `ngreen-eu=64 ngreen-l3=6 ngreenblmax=17741 ngreen-dmc=adlp ngreenV142=3`).
Kiểm sau boot (phải y như build-39): `ioreg -rc IntelAccelerator -d1 | grep xe-topo` = 16390; độ sáng tối đa đúng; con trỏ, Metal 2, Wi-Fi.
build-42 = build-41 + ` -ngreengva` nối cuối (174 ký tự, trong 228) → G3.

## v11 — XE-PAVPCTX, thử tạo context PAVP (2026-11-06, người dùng: "thử patch11 đi"; THỬ NGHIỆM)
Mục tiêu: G3. Không có context PAVP (`accel+0x1278`) → không PAVPFIX thì panic lúc boot (build-43), có PAVPFIX thì giải mã panic NULL+0x284 (build-42).
v11 bật `accel+0x1300` bit 3 ngay trước `IntelAccelerator::startGraphicsEngine` (điều kiện tạo context PAVP, theo ghi chú PAVPFIX) — **chỉ khi có boot-arg `-ngreenpavpctx`**; không có cờ thì kext chạy y như v10. PAVPFIX vẫn bật.
Chẩn đoán: `ioreg -rc IntelAccelerator -d1 | grep xe-pavp` → `xe-pavp-1300-pre/-post`, `xe-pavp-ctx` (1 = đã tạo); dmesg `XeNG PAVPCTX`.
Giả thuyết CHƯA XÁC MINH: (a) Apple có thể tính lại 0x1300 trong `startGraphicsEngine` → không tác dụng (`xe-pavp-ctx` 0); (b) BIOS HP khoá PAVP → tạo context có thể treo/panic lúc boot; (c) panic giải mã có thể không do PAVP.
Patch: `patches/nootedgreen-gmsfix-v10-to-v11.patch` (sha256 `37e4c6bf9cdf5987879136adb824dfdb291f82b78aeb556ac2a78161253e8a24`);
gộp trên JN 24450b4: `patches/nootedgreen-gmsfix-v11-jn24450b4.patch` (sha256 `050dab16036d0a221d89ac4845d45270a357a8677a9cd44b59d94133e98fddcc`).
Kiểm MÁY A: apply-check sạch; `clang++ -fsyntax-only` 0 lỗi, 21 cảnh báo = JN gốc. Chưa build/chạy.
```
cd ~/xe-stack
shasum -a 256 ~/patches/nootedgreen-gmsfix-v10-to-v11.patch     # 37e4c6bf…8a24
git apply --check ~/patches/nootedgreen-gmsfix-v10-to-v11.patch && git apply ~/patches/nootedgreen-gmsfix-v10-to-v11.patch
zsh build-nootedgreen.sh
md5 -q build/NootedGreen.kext/Contents/MacOS/NootedGreen
shasum -a 256 build/NootedGreen.kext/Contents/MacOS/NootedGreen
strings build/NootedGreen.kext/Contents/MacOS/NootedGreen | grep -c PAVPCTX     # phải > 0
```
Chỉ build lại kext. Chép `build/NootedGreen.kext` vào gốc USB MACEFI.
- build-44 = build-41 + kext v11 + `-ngreenpavpctx` (178 ký tự): chỉ kiểm boot + `xe-pavp-ctx`. Lỗi → build-41.
- build-45 = build-44 + `-ngreengva` (189): chỉ khi build-44 boot ổn và `xe-pavp-ctx` = 1.

## v12 — XE-PCIMATCH: personality IntelAccelerator chỉ khớp GPU Intel (2026-11-10, nhánh `whateverxe-dual-gpu`)
Mục tiêu: để dGPU sống (cho NullMoth/HDMI) mà iGPU không panic. Nguyên nhân panic build-49/50 (CHƯA XÁC MINH runtime):
`Gen11::injectAcceleratorPersonality` đăng ký `IntelAccelerator` với `IOPCIClassMatch 0x03000000&0xff000000` và **không** lọc vendor
(personality gốc của kext TGL đã bị `install-macos.sh` giới hạn ở `0x9a498086`) → khi dGPU còn trong IOKit, IntelAccelerator khởi động trên
card NVIDIA, `IGAccelTask::withOptions` thất bại → panic NULL+0xc78. build-51 (dGPU có điện, Lilu `disable-gpu` terminate khỏi IOKit) boot bình thường, Metal 2.
v12 thêm `IOPCIPrimaryMatch 0x00008086&0x0000ffff` (IOPCIFamily AND với ClassMatch). Không đổi gì khác; không boot-arg.
Patch: `patches/nootedgreen-v12-pcimatch.patch` (sha256 `02a677ae74027d5f12806df96920a1e5d13b1c864695ad63681c9feb2117898b`),
áp được trên cây v10 **hoặc** v11 (đã kiểm `git apply --check` cả hai). Kiểm MÁY A: `clang++ -fsyntax-only` 0 lỗi, 76 cảnh báo = v10 gốc. Chưa build/chạy.
```
cd ~/xe-stack
shasum -a 256 ~/patches/nootedgreen-v12-pcimatch.patch     # 02a677ae…898b
git apply --check ~/patches/nootedgreen-v12-pcimatch.patch && git apply ~/patches/nootedgreen-v12-pcimatch.patch
zsh build-nootedgreen.sh
md5 -q build/NootedGreen.kext/Contents/MacOS/NootedGreen
shasum -a 256 build/NootedGreen.kext/Contents/MacOS/NootedGreen
strings build/NootedGreen.kext/Contents/MacOS/NootedGreen | grep -c '0x00008086&0x0000ffff'     # phải = 1
```
Chỉ build lại kext. Chép `build/NootedGreen.kext` vào gốc USB MACEFI.
- build-52 = build-51 + kext v12, **bỏ** `disable-gpu` (dGPU sống và hiện trong IOKit; = cấu hình build-50 + kext v12), giữ `-v`.
  Kiểm: boot không panic; `ioreg -lw0 | grep -iE 'de10'` có NVIDIA; `ioreg -rc IntelAccelerator -d1 | grep -c IOClass` = 1 (chỉ iGPU). Panic → build-51.

## v13 — XE-AGDCSTUB: callback AGDC rỗng khi AGDP không gắn (2026-11-10, nhánh `whateverxe-dual-gpu`)
Panic build-52/53 (WindowServer, RIP 0): `IOFramebuffer::newUserClient` → `IOFramebuffer::open` → `AppleIntelFramebuffer::enableController+0x1356`
→ `AppleIntelBaseController::CallBackAGDC(4, …)` → `callq *0x1c00(controller)` = NULL (disassemble FB TGL 16.0 UUID B96A8448 + IOGraphicsFamily KDK 25G241, khớp UUID panic).
Con trỏ `controller+0x1c00` (ref `+0x1c08`) = 0 trong `AppleIntelBaseController::start`, chỉ được gán ở `RegisterAGDCCallback` (gọi từ `IntelFBClientControl::doAttribute`,
tức AppleGraphicsDevicePolicy). Log: build-47 AGDP gắn vào `IntelFBClientControl` 40 ms sau FB; build-52 không có dòng AGDP/displaypolicyd nào trong 13 s sau FB → không ai đăng ký.
Lý do AGDP không gắn khi dGPU hiện: CHƯA XÁC MINH. Cùng con trỏ được gọi không kiểm NULL ở `validateDetailedTiming` (event 0xa) và `setupDisplayTiming` (0xc); kết quả là bool.
v13 route 3 hàm đó: nếu `+0x1c00` = 0 thì gán stub trả 0 (= nhánh Apple dùng khi AGDC không xác nhận: "AGDC detailed timing validation failed - assuming valid timing";
`enableController` bỏ qua kết quả). AGDP đăng ký sau sẽ ghi đè stub. Tắt: `-ngreennoagdcstub`. Log: `XeNG AGDCSTUB: armed 1`, `… stub installed`, `… event N -> 0`.
Patch: `patches/nootedgreen-v12-to-v13-agdcstub.patch` (sha256 `70adc2e39e599d25411db8aa22a4ead4d635b26b6840722139bb55f208e6179d`), áp trên cây v10+v11+v12 (đã kiểm).
Kiểm MÁY A: `clang++ -fsyntax-only` 0 lỗi, 76 cảnh báo = gốc; 3 symbol có trong FB TGL (local `t`). Chưa build/chạy.
```
cd ~/xe-stack
shasum -a 256 ~/patches/nootedgreen-v12-to-v13-agdcstub.patch     # 70adc2e3…179d
git apply --check ~/patches/nootedgreen-v12-to-v13-agdcstub.patch && git apply ~/patches/nootedgreen-v12-to-v13-agdcstub.patch
zsh build-nootedgreen.sh
md5 -q build/NootedGreen.kext/Contents/MacOS/NootedGreen
shasum -a 256 build/NootedGreen.kext/Contents/MacOS/NootedGreen
strings build/NootedGreen.kext/Contents/MacOS/NootedGreen | grep -c AGDCSTUB     # phải >= 3
```
- build-54 = build-53 + kext v13. Kiểm: boot vào desktop; `dmesg | grep AGDCSTUB` (stub installed khi dGPU hiện); de10 trong ioreg; IntelAccelerator = 1. Lỗi → build-51.
