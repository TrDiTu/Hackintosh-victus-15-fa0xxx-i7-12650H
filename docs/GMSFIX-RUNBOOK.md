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
