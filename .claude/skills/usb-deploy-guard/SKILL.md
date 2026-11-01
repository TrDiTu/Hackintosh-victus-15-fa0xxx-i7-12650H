---
name: usb-deploy-guard
description: The ONLY allowed way to write the EFI to the USB stick on this Linux machine. Verifies the given mount point is a FAT partition on a USB/removable disk that holds no system or project mounts, requires a clean efi-validate result, backs up the existing USB EFI via efi-snapshot, mirrors the project EFI into <mount>/EFI only, and verifies by hash. Use whenever the user says "ghi lên USB", "deploy", "copy EFI sang USB", "cập nhật USB", or whenever anything needs to be written to the USB.
---

# usb-deploy-guard

Thao tác nguy hiểm duy nhất của dự án. Không bao giờ tự `cp`/`rsync`/`rm` vào USB, không `sudo`,
không `mount`/`umount`/`mkfs`/`dd`/`parted`.

## Đường dẫn USB
- Người dùng tự cắm và mount phân vùng FAT32 của USB, rồi cho Claude đường dẫn (ví dụ `/media/<user>/<LABEL>`).
- Hỏi đường dẫn ở lần ghi đầu tiên; lưu một dòng vào `config/usb-mount.txt`. Mỗi lần ghi sau vẫn hiển thị thông tin USB
  để người dùng xác nhận (đường dẫn mount có thể đổi khi cắm lại).
- Nếu Claude Code không có quyền ghi vào đường dẫn đó, nhờ người dùng thêm thư mục bằng `/add-dir <đường dẫn>` hoặc vào
  `additionalDirectories` trong `.claude/settings.local.json`.

## Quy trình (2 bước, bắt buộc có xác nhận của người dùng)
**Bước 1 — chạy thử (mặc định, không ghi gì):**
```
python3 .claude/skills/usb-deploy-guard/scripts/deploy_usb.py --mount <đường dẫn>
```
In thông tin USB (thiết bị, nhãn, filesystem, model, dung lượng, loại bus) và danh sách file sẽ thêm/sửa/xoá.
HIỂN THỊ cho người dùng, DỪNG, chờ xác nhận rõ ràng ("đúng USB, ghi đi").

**Bước 2 — ghi thật (chỉ sau khi người dùng xác nhận):**
```
python3 .claude/skills/usb-deploy-guard/scripts/deploy_usb.py --mount <đường dẫn> --confirmed
```

## Script tự kiểm tra
- Đường dẫn phải là mount point thật; nguồn phải là `/dev/...`; đĩa cha phải là USB, removable hoặc hotplug (`lsblk`).
- Từ chối nếu đĩa đó có phân vùng mount tại `/`, `/boot`, `/boot/efi`, `/efi`, `/home`, `/usr`, `/var` hoặc chứa thư mục dự án.
- Cảnh báo nếu filesystem không phải vfat.
- Cổng validation: `docs/validation/latest.json` 0 lỗi, `ocvalidate` đã chạy, hash trùng nội dung EFI hiện tại.
- `<mount>/EFI` có OpenCore → snapshot qua `efi-snapshot` (bỏ qua nếu trùng bản đã có); có file lạ không phải EFI → dừng (5).
- Chỉ ghi/xoá bên trong `<mount>/EFI`, `sync`, rồi so hash nguồn và đích.

## Mã thoát
0 xong · 1 lỗi/từ chối · 4 chưa qua cổng validation · 5 `<mount>/EFI` có nội dung lạ · 6 snapshot bị chặn (ví dụ known-good).
Gặp 4 → chạy `efi-validate`. Gặp 1 (từ chối USB), 5 hoặc 6 → báo người dùng, không tìm đường vòng.

## Sau khi ghi
- Nhắc người dùng unmount/eject trước khi rút. Cập nhật `docs/STATE.md`.
- USB cắm vào máy A khi ghi; sau đó cắm sang laptop để test.

## Không làm
- Không nới lỏng kiểm tra bằng cách sửa script hay `latest.json`. Không ghi ngoài `<mount>/EFI`.
