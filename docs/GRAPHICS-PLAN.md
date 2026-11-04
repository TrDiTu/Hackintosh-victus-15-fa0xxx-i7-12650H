# GRAPHICS-PLAN — Giai đoạn B: tăng tốc Metal cho iGPU 46A3 

Lập 2026-11-02 (Pha 6). Cổng chặn đã mở: người dùng viết "EFI nền đã ổn định, bắt đầu tăng tốc đồ hoạ".
EFI nền: build-08 **known-good**, build-10 (= build-08 + USB map) đang trên USB. `config-install.plist` = config build-10 (KHÔNG spoof, KHÔNG NootedGreen).

## 0. Kết quả có thể đạt — nói thẳng
- Tốt nhất có bằng chứng: giao diện/app tăng tốc **Metal (family Mac2/Common3)**. **KHÔNG Metal 3**, không OpenGL phần cứng.
- **Mất**: system sleep (stack không hỗ trợ), màn hình ngoài (đã mất do HDMI ở dGPU), SIP hạ thêm (0x0A13), **AMFI tắt hẳn** (`amfi_get_out_of_my_way=1`),
  có thể GPU hang / kernel panic. Cập nhật macOS (khác 25G241) sẽ làm hỏng stack và root patch Wi-Fi.
- Chưa ai báo chạy trên **46A3 (UHD 64 EU)** với stack này. Gần nhất: i5-1240P 46A6 80 EU (#16, chạy), i3-1220P 46B3 64 EU (cheseecake, chạy bằng fork riêng),
  i7-12800H 46A6 + NVIDIA (khucxtriendev, chạy). i7-12700H 46A6 + RTX 3060 (#24) **panic, không có cách sửa**.

## 1. Nguồn đã đọc (clone bằng tools/clone_ref.py)
| Repo | Commit | Vai trò |
|---|---|---|
| JulioNectar/Hackintosh-XPS13Plus-IrisXe-Tahoe | 6f03560 (code mới nhất 2026-10-27) | **stack chọn** |
| cheseecake/i3-1220p-macos-gpu | 7881587 | so sánh 64 EU |
| khucxtriendev/irisxegraphic-i712800h-efi | 26ee7f3 | ADL-H + NVIDIA đã chạy |
Đọc: JN README, CHANGELOG, docs/INSTALL.md, docs/STATUS.md, KERNEL-PATCHES.md, install.sh, `src/NootedGreen/kern_gen11.cpp`; cheseecake docs/PORT-I3-1220P.md; JN issue #16, #24.

## 2. Chọn fork NootedGreen: **JulioNectar (bản chính)**
| Tiêu chí | JulioNectar | cheseecake |
|---|---|---|
| Ghi đè topology | `ngreen-eu=48/64/80/96`, `ngreen-l3=2..16 (chẵn)` — `kern_gen11.cpp` L26–36 | `ngreensubslices`, `ngreenmaxeu`, `ngreenl3banks` — L6024–6026; mặc định 8 SS/64 EU nhưng **L3 = 8** |
| Code mới nhất | 2026-10-27 | commit cuối 2026-10-31 chỉ `.gitignore`; nhánh port từ JN cũ hơn |
| Bằng chứng ADL | #16 i5-1240P 46A6 chạy (`ngreen-eu=80 ngreen-l3=6`) | i3-1220P 46B3 64 EU |
| Tính năng thêm | `-ngreenpm`, `ngreenauxbl`, rowchk… | ít hơn |
Lý do: JN hỗ trợ 64 EU qua boot-arg; JN chứng minh **L3 sai gây lỗi hình** (80 EU: 6 bank, fuse `0x9118`) — máy này đo được **6 L3 bank** (người dùng), cheseecake để 8.
NootedGreen được **build trên MÁY B** bằng `install.sh` (upstream sgiammori/NootedGreen @ `95f8189` + patch JN), license "Thou Shalt Not Profit 1.0".

## 3. Topology (dữ kiện thật)
- Linux `gt0/sseu_topology` (docs/hw-dump/igpu-topology.txt): 1 slice, 4 DSS, mask **0x33** (DSS 0,1,4,5), 16 EU/DSS = **64 EU**. L3 bank = **6** (người dùng cung cấp).
- Boot-arg: **`ngreen-eu=64 ngreen-l3=6`** → JN dựng 8 SS × 8 EU, L3 6. JN không đọc fuse; steering MCR ở DSS0 (có mặt ở máy này — mask bit0 = 1).
- Kiểm sau boot: `ioreg -rc IntelAccelerator -d1 | grep xe-topo` → kỳ vọng **16390** (= 64<<8 | 6 = 0x4006).
- Rủi ro CHƯA XÁC MINH: mask DSS không liên tục (0,1,4,5) — JN đánh số SS liên tục; nếu lỗi hình → thử `ngreen-l3=8` (một thay đổi/lần) và báo.

## 4. Stolen memory / DVMT
- Đo được: **60 MB** tại 0x7C800000 (GGC 0xFEC1, BDSM 0x7C800001 locked) — `docs/hw-dump/igpu-stolen-dump.txt`. BIOS HP không có DVMT → không đổi được.
- Rủi ro panic `IOAccelTask::release ← IGAccelTask::withOptions ← IntelAccelerator::start` (#24, ADL-H + RTX 3060, đóng không có bản sửa; người báo nghi stolen/DVMT).
  Nếu gặp: chụp màn hình panic, lấy `/Library/Logs/DiagnosticReports/*.panic`, quay về `config-install.plist`.

## 5. DeviceProperties iGPU `PciRoot(0x0)/Pci(0x2,0x0)`
Lấy từ `EFI/OC/config.plist` của JN (trùng khucxtriendev, R1):
| Key | Giá trị | Ghi chú |
|---|---|---|
| `device-id` | `499A0000` | spoof TGL 9A49 (bắt buộc: install.sh L86–87, driver TGL) |
| `AAPL,ig-platform-id` | `0000499A` | |
| `framebuffer-patch-enable`, `force-online`, `complete-modeset`, `rps-control`, `enable-max-pixel-clock-override` | `01000000` | JN/khucx; max-pixel-clock cho panel 144 Hz (CHƯA XÁC MINH ở 144 Hz) |
| `AAPL,slot-name` = `built-in`, `built-in` = `00` | | |
| **Bỏ** `model` ("Intel Iris Xe Graphics" — máy này là UHD), **bỏ** `hda-gfx` (không HDMI audio) | | |
dGPU: giữ `disable-gpu` + `-wegnoegpu` + SSDT-DGPU-OFF (khucx thêm `class-code ffffffff` — chưa cần).

## 6. Kext & thứ tự
- `NootedGreen.kext` (bản build trên MÁY B), **ngay sau WhateverGreen**, `MinKernel 25.0.0` (như JN). Phụ thuộc Lilu.
- `HookCase.kext` và các kext/bundle TGL của Apple **không vào EFI** — install.sh cài vào `/Library/Extensions`, `/Library/GPUBundles`, `/System/Library/Caches/xe.bundle`.

## 7. boot-args đề xuất cho `graphics-v1`
Giữ của EFI nền: `-v keepsyms=1 debug=0x100 -vi2c-force-polling -wegnoegpu -amfipassbeta`
Thêm từ JN `config.plist` (đã lọc): `IGLogLevel=3 -ngreentglwithgfx -allow3d -disablegfxfirmware ngreen-dmc=adlp -ngreenv189 -ngreenkeepefi -ngreenxefix
-ngreenfixbootmode amfi_get_out_of_my_way=1 ngreenSched=4 ngreenV142=3 gfxrst=1` + **`ngreen-eu=64 ngreen-l3=6`**.
**Không thêm** lần đầu: `ngreenpm=22`/`-ngreenpm` (skill: thử sau khi ổn định), `ngreenblmax=17777` (giá trị PWM panel Dell, JN HISTORY L884), `alcid=11`,
cờ riêng ThinkPad của khucx (`-xenobb -ngreennoblr -ngreenv99g ngreengtfreq=1400`).

## 8. SIP / AMFI (cần người dùng đồng ý)
- SIP: hiện `03080000` (0x803, OCLP). JN/khucx dùng **`130A0000` (0x0A13)** = 0x803 + `CSR_ALLOW_UNAPPROVED_KEXTS` (0x200) + 0x10. 0x0A13 chứa mọi bit 0x803 → đề xuất **0x0A13**.
- AMFI: thêm `amfi_get_out_of_my_way=1` (JN/khucx). Hiện có AMFIPass + `-amfipassbeta` (OCLP-CustoMac). Dùng cả hai: CHƯA XÁC MINH có xung đột không
  (AMFI tắt hẳn thì AMFIPass thừa) → giữ cả hai ở lần đầu; nếu lỗi, thử bỏ một trong hai (mỗi lần một thay đổi).

## 9. Tương tác với root patch Wi-Fi (OCLP-CustoMac Modern Wi-Fi) — CHƯA XÁC MINH
- JN chạy Wi-Fi **không** root patch (INSTALL.md L270) → chưa ai thử kết hợp. Root patch sửa snapshot hệ thống; install.sh ghi `/Library/*` + `/System/Library/Caches/xe.bundle` và rebuild AuxKC (`kmutil load -z`).
- Thứ tự đề xuất: root patch đã có → chạy install.sh SAU. Nếu sau này phải root patch lại (OCLP), chạy lại `install.sh` sau đó. Kiểm Wi-Fi sau mỗi bước.
- Phải sao lưu (Time Machine / ảnh ổ) trước install.sh.

## 10. Trình tự an toàn (Pha 7)
1. **Sao lưu toàn bộ** MÁY B. Giữ USB build-10 (nền) — `config-install.plist` không spoof là đường lui an toàn kể cả khi đã cài TGL (driver TGL không khớp 46A3 thật).
2. **EFI `graphics-prep`** (Claude dựng) = build-10 + spoof 9A49 (mục 5) + SIP 0x0A13, **chưa có NootedGreen**, boot-args nền. Chỉ để chạy install.sh
   (install.sh L86–87: không spoof thì framebuffer kext bị bỏ khỏi AuxKC).
3. Trên MÁY B (boot `graphics-prep`): `xcode-select --install`; clone JN @ `6f03560` vào ổ APFS; `zsh install.sh --check` → gửi kết quả cho Claude.
4. Claude xem xong → `zsh install.sh` → **KHÔNG khởi động lại bằng `graphics-prep`** (INSTALL.md L136–140: đã cài TGL mà spoof không NootedGreen = rủi ro);
   chép `build/NootedGreen.kext` sang MÁY A.
5. Claude dựng **`graphics-v1`** = graphics-prep + NootedGreen + boot-args mục 7 → validate → snapshot → ghi USB. Boot thử.
6. Lỗi khởi tạo → boot `config-install.plist` (đổi tên trong OpenCore hoặc Claude ghi build nền lại). Gỡ stack: `zsh install.sh --uninstall`.
**Không chạy `make-efi.sh`** (sinh serial mới).

## 11. Kiểm tra sau boot graphics-v1 (Pha 8)
`kmutil showloaded | grep -iE 'nootedgreen|hookcase'` · `ioreg -rc IntelAccelerator -d1 | grep -E 'xe-topo|rowchk'` · `system_profiler SPDisplaysDataType` ·
About This Mac · panic report nếu có. Mỗi lần đổi **một** tham số, mỗi lần một build. Không tuyên bố "Metal hoạt động" khi chưa có đủ kext + Metal device + người dùng xác nhận.

## Cần người dùng quyết
1. Duyệt chọn fork **JulioNectar** + `ngreen-eu=64 ngreen-l3=6`.
2. Đồng ý **SIP 0x0A13** và **AMFI tắt hẳn** (`amfi_get_out_of_my_way=1`) cùng các mất mát ở mục 0.
3. Đồng ý trình tự mục 10 (EFI `graphics-prep` trung gian).
4. Xác nhận đã/sẽ sao lưu toàn bộ MÁY B trước install.sh.
