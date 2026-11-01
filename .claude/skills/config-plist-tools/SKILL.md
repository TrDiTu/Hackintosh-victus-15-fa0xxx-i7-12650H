---
name: config-plist-tools
description: Read, edit and diff OpenCore config.plist safely - typed set/get/delete, adding or reordering Kernel/Add entries, editing boot-args word by word, and structured diffs that match kexts/SSDTs/drivers by name and mask serials. Use for EVERY change to EFI/OC/config.plist (never hand-edit the XML), and whenever comparing our config with a reference config (JulioNectar, cheseecake, khucxtriendev, the Victus R1 repo, config-install.plist vs config.plist), or when the user says "sửa config", "thêm kext", "boot-args", "quirk", "so sánh config", "diff".
---

# config-plist-tools

## Sửa `config.plist` — `plist_edit.py`
```
E=.claude/skills/config-plist-tools/scripts/plist_edit.py
python3 $E get  'Kernel/Quirks/DisableIoMapper'
python3 $E set  'Kernel/Quirks/DisableIoMapper' false --type bool --dry-run
python3 $E set  'DeviceProperties/Add/{PciRoot(0x0)/Pci(0x2,0x0)}/device-id' 499A0000 --type data
python3 $E append Kernel/Add --json '{"Arch":"x86_64","BundlePath":"Lilu.kext","Comment":"","Enabled":true,"ExecutablePath":"Contents/MacOS/Lilu","MaxKernel":"","MinKernel":"","PlistPath":"Contents/Info.plist"}'
python3 $E move 'Kernel/Add[BundlePath=VirtualSMC.kext]' --to 1
python3 $E bootarg-add -wegnoegpu      |   python3 $E bootarg-remove -v
python3 $E set ... --file EFI/OC/config-install.plist        (sửa file config khác)
```
Quy tắc:
- Luôn chạy `--dry-run` trước, đọc phần thay đổi, rồi mới chạy thật. Mỗi thay đổi thật tự ghi vào `docs/BUILD-LOG.md`.
- Phân đoạn có `/` đặt trong `{}`; chọn phần tử mảng bằng `[3]` hoặc `[BundlePath=Lilu.kext]`.
- `set` từ chối key chưa tồn tại (thường là gõ sai, ví dụ `DisableIOMapper`) và từ chối đổi kiểu dữ liệu. Chỉ dùng
  `--create` khi Configuration.pdf của đúng phiên bản OpenCore xác nhận key đó; ghi lý do vào BUILD-LOG.
- Mục `Kernel/Add` mới: đủ trường như Sample.plist của bản OpenCore đang dùng (Arch, BundlePath, Comment, Enabled,
  ExecutablePath, MaxKernel, MinKernel, PlistPath). Kext không có executable (ví dụ plugin chỉ có Info.plist) để
  `ExecutablePath` rỗng. Chuỗi `"hex:..."` trong JSON được chuyển thành data.
- Không ghi serial/MLB/UUID/ROM thật (script từ chối) → xem `smbios-secrets`.
- Sau một loạt sửa: `efi-validate`.

## So sánh — `plist_diff.py`
```
D=.claude/skills/config-plist-tools/scripts/plist_diff.py
python3 $D EFI/OC/config.plist _cache/refs/<repo>/EFI/OC/config.plist --markdown > docs/diffs/ours-vs-<repo>.md
python3 $D A.plist B.plist --only Kernel/Quirks --only Booter/Quirks --only DeviceProperties
```
- Kext/SSDT/driver/patch được so theo tên (BundlePath/Path/Comment), có báo đổi thứ tự; serial bị che.
- Dùng khi: phân tích 14 key của repo Victus (R1), đối chiếu với config của JulioNectar/cheseecake ở Giai đoạn B,
  so `config-install.plist` với `config.plist`. Mỗi khác biệt định đưa vào config của mình phải có lý do và nguồn trong
  BUILD-LOG; không chép nguyên config của máy khác.
- Lưu kết quả diff trong `docs/diffs/` (không chứa serial vì đã che).
