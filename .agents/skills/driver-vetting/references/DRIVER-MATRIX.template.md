# DRIVER-MATRIX (mẫu — Codex sao chép sang docs/DRIVER-MATRIX.md rồi điền)

Quyết định: `DÙNG` · `ỨNG VIÊN` · `KHÔNG CÓ DRIVER` · `KHÔNG CẦN` · `BỎ QUA`
Cột "Tahoe" ghi: `ĐÃ XÁC MINH (link)` hoặc `CHƯA XÁC MINH`.

| # | Thiết bị | Hardware ID (từ dump) | Driver ứng viên | Nguồn chính thức | License | Phiên bản | Tahoe | Hạn chế đã biết | Phụ thuộc / thứ tự | Quyết định | Người dùng duyệt |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | (vd. Wi-Fi) | PCI\VEN_xxxx&DEV_xxxx&SUBSYS_xxxx | itlwm + HeliPort | (URL repo/release) | | | | | | | ☐ |
| 2 | (vd. Touchpad) | ACPI\xxxxxxxx | VoodooI2C + VoodooI2CHID | | | | | | VoodooI2C trước HID | | ☐ |

## Thiết bị KHÔNG có driver khả thi
| Thiết bị | Hardware ID | Lý do | Giải pháp thay thế |
|---|---|---|---|

## 5 rủi ro lớn nhất
1.
2.
3.
4.
5.

---

# SOURCES (mẫu — docs/SOURCES.md)

| Thành phần | Phiên bản | URL release chính thức | File | SHA256 | Ngày tải | Dùng trong EFI? |
|---|---|---|---|---|---|---|
| OpenCorePkg | | | | | | |
| ocvalidate (cùng bản OpenCore) | | | | | | |
