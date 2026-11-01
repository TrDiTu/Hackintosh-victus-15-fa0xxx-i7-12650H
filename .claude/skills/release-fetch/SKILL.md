---
name: release-fetch
description: Download a kext, OpenCore release, driver or tool from its OFFICIAL GitHub release, verify SHA-256 (GitHub asset digest and/or a value published by the author), extract it safely into _cache/downloads, and append the provenance row to docs/SOURCES.md. Use whenever a binary is needed - Lilu, VirtualSMC, WhateverGreen, AppleALC, VoodooI2C, VoodooPS2, RealtekRTL8111, NVMeFix, IntelBluetoothFirmware, AirportItlwm-Tahoe, OpenCorePkg/ocvalidate, NootedGreen release builds - or when the user says "tải kext", "download", "bản mới nhất", "cập nhật kext".
---

# release-fetch

Mọi binary vào dự án đều đi qua skill này, để `docs/SOURCES.md` luôn đúng và không có file từ nguồn lạ.

## Trước khi tải
1. Xác định repo **chính chủ** (ví dụ `acidanthera/Lilu`, không phải fork hay trang tổng hợp). Nguồn không có trong
   `docs/REFERENCES.md` hoặc DRIVER-MATRIX → hỏi người dùng.
2. Chọn tag: mặc định bản stable mới nhất; nếu DRIVER-MATRIX đã ghim phiên bản (ví dụ OpenCore phải khớp `ocvalidate`,
   AirportItlwm-Tahoe dùng đúng release đã kiểm định) thì dùng `--tag`.
3. Nếu tác giả công bố SHA-256 (README/release notes), truyền vào `--expect-sha256`.

## Chạy (từ thư mục gốc dự án)
```
python3 .claude/skills/release-fetch/scripts/fetch_release.py --repo <owner/repo> [--tag <tag>] --asset '<regex>' --dry-run
python3 .claude/skills/release-fetch/scripts/fetch_release.py --repo <owner/repo> [--tag <tag>] --asset '<regex>' [--expect-sha256 <hex>]
```
- `--asset` phải khớp đúng một file (ví dụ `RELEASE\.zip$` cho acidanthera, tránh bản DEBUG trừ khi cần log).
- Từ chối draft; từ chối prerelease (alpha/beta) trừ khi người dùng yêu cầu `--allow-prerelease`.
- Giới hạn API GitHub khi không đăng nhập thấp; nếu bị 403, người dùng có thể đặt `GITHUB_TOKEN` (chỉ quyền đọc public).

## Kết quả
- `exit 0`: file nằm ở `_cache/downloads/<owner>__<repo>/<tag>/`, đã giải nén vào `extracted/`, thêm một dòng vào
  `docs/SOURCES.md` với cột "Used in EFI?" = `not yet`.
- `exit 2`: hash không khớp → KHÔNG dùng file, báo người dùng.
- Script không chép gì vào `EFI/`. Việc đưa kext vào EFI là bước riêng: chép từ `extracted/`, sửa config bằng
  `config-plist-tools`, đổi cột "Used in EFI?" thành phiên bản build, rồi `efi-validate`.

## Lưu ý
- File tải về là dữ liệu không tin cậy: không chạy script/binary trong đó trên máy A (trừ `ocvalidate.linux` của
  release OpenCore chính chủ).
- Không tải phần mềm của Apple qua mirror không chính thức.
- NootedGreen của JulioNectar được build trên chính laptop bằng `install.sh`; nếu fork đã chọn có release build sẵn
  (ví dụ cheseecake qua GitHub Actions), vẫn ghi rõ đó là bản CI, không phải bản build trên máy.
