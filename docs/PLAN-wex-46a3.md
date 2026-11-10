# Kế hoạch: Tăng tốc iGPU 46A3 bằng WhateverXe 0.7.0 + patch #35

> Dành cho Claude Code. Đọc toàn bộ file này trước khi làm. Làm theo từng giai đoạn, dừng ở các điểm **[DỪNG — hỏi người dùng]**.

## Bối cảnh

- Máy: HP Victus 15-fa0xxx, i7-12650H, iGPU `8086:46A3` (Alder Lake-H UHD, 64 EU), dGPU NVIDIA, macOS 26 Tahoe.
- Repo EFI: `TrDiTu/Hackintosh-victus-15-fa0xxx-i7-12650H` (repo hiện tại). EFI được build trên máy Linux này rồi ghi ra USB.
- Bản WhateverXe (WEX) chính thức chưa chạy được trên 46A3: macOS kẹt ở framebuffer GOP, VRAM 7 MB, không có Metal.
- Issue https://github.com/b00t0x/WhateverXe/issues/35 (MSI Katana GF76, **cùng CPU i7-12650H, cùng 46A3 rev 0x0C**, Optimus không MUX) đã chỉ ra 3 lỗi chặn, mỗi lỗi sửa 1 dòng, trên WEX 0.7.0 commit `d0b7fb6`. Sau khi vá: màn trong 1920x1080, IntelAccelerator attach, Metal, VRAM 1536 MB.
- **Không** dùng WEX 0.8.0: issue #76 cho thấy 0.8.0 chặn accelerator trên 46A3 (48 EU) vì `ProfileMismatch`; bản 64 EU chưa rõ.
- **Không** dùng fork TigerShota/WhateverXe (chỉ dành cho i5-12450H 48 EU).

## Nguyên tắc

1. Làm trên branch mới `wex-46a3`. Không sửa `main` cho tới khi người dùng xác nhận chạy được.
2. Không đụng phần đang chạy tốt: Wi-Fi (kgp-macPro/AirportItlwm-Tahoe), Bluetooth, USB map, input.
3. WhateverGreen và WhateverXe **không được bật cùng lúc**. Các kext iGPU cũ (NootedGreen đã vá, IntelIGPU-Tahoe, stack JulioNectar, XeGfx/WTLIntelGfx) phải **tắt** (`Enabled=false`), không xoá, để còn quay lại.
4. Mọi thay đổi `config.plist` phải chạy `ocvalidate` (đúng phiên bản OpenCore đang dùng) và báo kết quả.
5. Không đọc/in nội dung thư mục `secrets/`.
6. Ghi lại mọi việc đã làm vào `docs/wex-46a3/LOG.md`.

---

## Giai đoạn 0 — Khảo sát repo (chỉ đọc)

1. Đọc `CLAUDE.md`, `PROMPT.md`, `README-SETUP.md`, `config/`, `tools/`, `docs/`.
2. Xác định và ghi vào `docs/wex-46a3/audit.md`:
   - Phiên bản OpenCore, đường dẫn `config.plist`, cách build/ghi USB hiện tại (script nào trong `tools/`).
   - Danh sách `Kernel > Add` (thứ tự, Enabled), đặc biệt Lilu, WhateverGreen, NootedGreen, các kext iGPU khác, AMFIPass, kext NVIDIA (NullMoth nếu có).
   - `boot-args`, `csr-active-config`, `SecureBootModel`, SMBIOS model.
   - `DeviceProperties` của `PciRoot(0x0)/Pci(0x2,0x0)` (device-id spoof, framebuffer patch…).
   - Có SSDT tắt dGPU chưa; có `SSDT-PNLF` chưa.
3. Báo tóm tắt cho người dùng. **[DỪNG — hỏi người dùng]** nếu có gì khác với giả định trong file này.

## Giai đoạn 1 — Build WhateverXe 0.7.0 + patch #35

WEX chỉ build được trên macOS (Xcode CLT, Python 3.9+, MacKernelSDK, Lilu dev headers). Máy này là Linux nên dùng **GitHub Actions runner macOS**.

1. **[DỪNG — hỏi người dùng]** trước khi fork/push lên GitHub. Sau khi đồng ý:
   ```bash
   gh repo fork b00t0x/WhateverXe --clone --remote
   cd WhateverXe
   git checkout -b katana-46a3 d0b7fb6275ca51fde088fa7e91595462bd457ec9
   ```
2. Lấy patch gốc từ issue #35:
   `https://github.com/user-attachments/files/34389603/WEX-0.7.0-katana-fixes.patch`
   Lưu vào `patches/WEX-0.7.0-katana-fixes.patch`, chạy `git apply --check` rồi `git apply`.
   Nếu không tải được hoặc không apply sạch, sửa tay đúng 3 chỗ (đối chiếu nội dung issue #35):
   - `WhateverXe/kern_vbt.hpp`, trong `parse()`: thay
     `if(r.present&(1U<<d)){r.status=Status::Conflict;return r;}`
     bằng
     `if(r.present&(1U<<d))continue; // keep first child per DDI, like Linux i915`
   - `WhateverXe/kern_xe.cpp`, `XE::display13SSTPort()`: chấp nhận port mode 0 (`field<uint32_t>(p,0x550)==0`) cho cổng panel Combo (`config[0]<3` và `s->adlnOutputWiring.panel&(1U<<config[0])`) tại thời điểm handoff.
   - `WhateverXe/kern_xe.cpp`, `XE::adlnSetDualClock()`: sau `ready=…adlnWorkLoopTryClose(loop);`, nếu `!ready && !active` thì đặt `ready=true; evidence[8]=2;` (cold CDCLK start, không có pipe nào chạy).
   Commit với message tham chiếu issue #35.
3. Workflow CI:
   - Trước tiên xem `.github/workflows/` trong repo WEX. Nếu đã có workflow build, dùng lại (chỉ thêm trigger cho branch `katana-46a3` và upload artifact).
   - Nếu không có, tạo `.github/workflows/build.yml` chạy trên `macos-latest`:
     - Bootstrap MacKernelSDK và Lilu dev (theo cách các plugin acidanthera làm, ví dụ `Lilu/Scripts/bootstrap.sh --sdk`), đặt `MacKernelSDK/` và `Lilu.kext/` ở thư mục gốc repo, hoặc truyền `--sdk`/`--lilu`.
     - Chạy `python3 tools/build.py --release` và `python3 tools/test.py`.
     - Build thêm bản DEBUG (để chẩn đoán).
     - Upload artifact: RELEASE zip, DEBUG zip, kèm `git log -1` và `git diff d0b7fb6`.
4. **[DỪNG — hỏi người dùng]** trước khi push và chạy workflow. Theo dõi run, nếu lỗi build thì đọc log, sửa, chạy lại. Báo kết quả test.
5. Tải artifact về, kiểm tra `Info.plist` (CFBundleIdentifier, version), lưu vào `kexts-custom/WhateverXe-0.7.0-katana/` trong repo EFI kèm `SOURCE.md` ghi commit + run ID.

**Phương án dự phòng:** nếu Actions không dùng được, viết `tools/build-wex-on-mac.sh` để người dùng tự chạy trên chính Hackintosh (máy vẫn boot được khi chưa tăng tốc).

## Giai đoạn 2 — Tích hợp vào EFI (branch `wex-46a3`)

Cấu hình tham chiếu là bản đã chạy trong issue #35. Gộp vào config hiện tại, **giữ** các boot-args/kext khác đang cần.

1. **Kexts**
   - Thêm `WhateverXe.kext` (bản RELEASE vừa build) ngay **sau Lilu**.
   - Dùng **AMFIPass 1.4.1 Mod** từ `b00t0x/WhateverXe-Graphics` (`extras/AMFIPass-v1.4.1-Mod-RELEASE.zip`). Tắt AMFIPass gốc nếu có; không load cả hai.
   - Lilu ≥ 1.7.2 (issue #35 dùng 1.7.3).
   - Tắt (Enabled=false): WhateverGreen, NootedGreen, mọi kext iGPU thử nghiệm khác.
   - Kext NVIDIA (NullMoth): tắt ở lần test đầu.
2. **boot-args** — thêm (không trùng lặp):
   `-allow3d -disablegfxfirmware -igfxdvmt keepsyms=1 debug=0x100 -lilubetaall -amfipassbeta`
   Gỡ các boot-arg chỉ phục vụ hướng iGPU cũ (ghi rõ từng cái trong LOG.md).
3. **csr-active-config** = `03080000` (0x803).
4. **SecureBootModel** = `Disabled`.
5. **DeviceProperties** `PciRoot(0x0)/Pci(0x2,0x0)`:
   - **Xoá** mọi `device-id` spoof cũ, `AAPL,ig-platform-id`, `AAPL,GfxYTile` và các patch framebuffer cũ (ghi lại giá trị cũ).
   - Nếu DVMT Pre-Allocated cố định 60 MB (Victus thường như vậy; hỏi người dùng nếu chưa chắc), thêm:
     - `framebuffer-patch-enable` = Data `01000000`
     - `framebuffer-stolenmem` = Data `0000C003`
6. **ACPI**: đảm bảo có `SSDT-PNLF` (độ sáng). Bật SSDT tắt dGPU cho lần test đầu nếu repo đã có.
7. **SMBIOS**: issue #35 dùng `MacBookPro16,2`. Nếu repo đang dùng model MacBookPro16,x khác thì giữ nguyên và ghi chú; không đổi serial.
8. Chạy `ocvalidate`, sửa hết lỗi. Build EFI bằng script hiện có. Tạo thêm entry/USB dự phòng với EFI cũ (hoặc giữ thư mục `EFI-backup-<ngày>`).
9. **[DỪNG — hỏi người dùng]** trước khi ghi USB.

## Giai đoạn 3 — Việc người dùng làm trong macOS

Viết `docs/wex-46a3/MACOS-STEPS.md` (tiếng Việt, ngắn gọn) gồm:

1. Boot bằng EFI mới.
2. Cài **WhateverXe Graphics 0.4.0** pkg (bản khớp với 0.7.0 trong issue #35, không dùng 0.4.1), từ https://github.com/b00t0x/WhateverXe-Graphics/releases/tag/v0.4.0 , rồi khởi động lại.
3. Lệnh kiểm tra:
   ```bash
   system_profiler SPDisplaysDataType | grep -Ei "VRAM|Metal|Chipset"
   ioreg -l | grep -E "IntelAccelerator|N97NativeStartAllowed|N97FBBootHandoff|N97FramebufferStartAccepted|WhateverXeFirmwarePorts"
   log show --last boot --predicate 'sender CONTAINS "WhateverXe"' | tail -200
   ```
   Thành công khi: VRAM ~1536 MB, có Metal, có IntelAccelerator, `N97FBBootHandoff` Complete.
4. Nếu repo WEX có script chẩn đoán (ví dụ `wex-diag.sh` trong `tools/`), hướng dẫn chạy và gửi file report.
5. Gỡ bỏ / quay lại: cách gỡ Graphics pkg theo README của WhateverXe-Graphics, và boot EFI dự phòng.

## Giai đoạn 4 — Xử lý theo kết quả

Người dùng sẽ gửi lại output/log. Đối chiếu theo các mốc trong issue #35:

| Triệu chứng | Lỗi tương ứng |
|---|---|
| `WhateverXeFirmwarePorts status=7`, `N97NativeRoutingUnavailable=Yes` | Patch 1 (VBT) chưa vào |
| `N97FBBootHandoff` NotReady, bootPath=0 | Patch 2 (port mode 0) chưa vào hoặc wiring khác |
| Đèn nền đổi khi boot rồi màn đen, log `FB0: Hardware mode set failed` | Patch 3 (CDCLK) |
| `N97GTReadout status=4 (ProfileMismatch)` | Vấn đề GT profile như #76 / #24 — dừng, báo người dùng |

Nếu đổi sang bản DEBUG để lấy log, nhớ quay lại RELEASE khi xong.

## Giai đoạn 5 (sau khi iGPU ổn định) — dGPU NVIDIA

Chỉ làm khi người dùng yêu cầu. Issue #35 cho biết cùng build này vẫn chạy khi bật dGPU với driver NullMoth và `gfxrst=4`. Bật SSDT dGPU lại, bật NullMoth, thêm `gfxrst=4`, test riêng từng thay đổi.

## Khi xong

- Merge `wex-46a3` vào `main` chỉ khi người dùng xác nhận.
- Gợi ý người dùng comment kết quả (HP Victus 15-fa0xxx, 64 EU) vào issue #35 để maintainer có thêm dữ liệu.
