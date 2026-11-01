---
name: smbios-secrets
description: How real SMBIOS identity (serial, MLB, SystemUUID, ROM) reaches the USB without ever entering the project EFI, logs, snapshots or the conversation - the user keeps them in secrets/smbios.json, usb-deploy-guard injects them into a temporary staged copy at deploy time, and USB backups are stripped. Use when the user asks about serials, SMBIOS, macserial/GenSMBIOS, PlatformInfo, iCloud/iMessage/App Store sign-in, "Apple ID", or when changing SystemProductName.
---

# smbios-secrets

## Nguyên tắc
- EFI trong dự án (`EFI/OC/config.plist`) luôn giữ placeholder: `CHANGE_ME_SERIAL`, `CHANGE_ME_MLB`,
  UUID toàn số 0, ROM 6 byte 0. `plist_edit.py` từ chối ghi giá trị thật.
- Giá trị thật chỉ nằm trong `secrets/smbios.json` do **người dùng** tạo. Claude **không đọc, không in, không sửa,
  không sao chép** file này (bị chặn trong `.claude/settings.json`; cũng không dùng `cat`/`grep`/`python` để đọc nó).
- Không bao giờ hỏi người dùng dán serial vào cuộc trò chuyện. Nếu người dùng lỡ dán, nhắc họ rằng nên sinh bộ mới.

## Hướng dẫn người dùng (Claude chỉ đưa hướng dẫn, người dùng tự làm)
1. Chọn `SystemProductName` khớp với config (hiện các repo tham chiếu dùng `MacBookPro16,2`; kiểm lại trong
   GPU-STRATEGY/GRAPHICS-PLAN trước khi chốt).
2. Sinh serial bằng `macserial` (có trong `Utilities/macserial/` của release OpenCore) hoặc GenSMBIOS, chạy trên máy của
   người dùng. Kiểm tra serial chưa được dùng (trang kiểm tra bảo hành của Apple phải báo "không hợp lệ").
3. ROM: thường lấy 6 byte địa chỉ MAC của card Ethernet RTL8111 (`ip link` trên Linux của laptop), viết 12 chữ số hex.
4. `cp secrets/smbios.json.example secrets/smbios.json`, điền giá trị, giữ nguyên `SystemProductName`.
5. Không chạy `make-efi.sh` hay công cụ nào tự sinh serial trong repo tham khảo.

## Cách hoạt động
- `usb-deploy-guard` (khi có `secrets/smbios.json`): chép EFI vào `_cache/stage/deploy/`, tiêm 4 trường vào bản tạm,
  ghi bản tạm lên USB, kiểm hash, **xoá bản tạm**. Không in giá trị. `--no-smbios` để ghi placeholder.
- Script từ chối nếu: file thiếu trường hoặc còn placeholder, UUID/ROM sai định dạng, `SystemProductName` trong file khác
  config (serial gắn với model), hoặc config dự án lại chứa giá trị thật.
- Sao lưu EFI đang có trên USB → snapshot chạy với `--strip-smbios` (thay bằng placeholder). Khôi phục từ snapshot rồi
  ghi lại thì serial được tiêm lại.
- Đổi `SystemProductName` → người dùng phải sinh bộ serial mới cho model đó.

## Lưu ý
- Placeholder vẫn boot bình thường; chỉ iCloud/iMessage/App Store là không dùng được. Giai đoạn đầu có thể ghi placeholder.
- `efi-validate` báo "real-looking value" nếu config dự án chứa giá trị thật → sửa lại thành placeholder ngay.
