---
name: efi-snapshot
description: Create a snapshot of one COMPLETE EFI build (max 10, rotating, known-good protected). Use whenever an EFI build just passed efi-validate, the user says "snapshot", "lưu bản build", "backup EFI", "tạo build mới", or before overwriting the USB EFI. Do NOT use for each small driver/config tweak while a build is still in progress.
---

# efi-snapshot

Snapshot gắn với MỘT BẢN BUILD EFI hoàn chỉnh, không gắn với từng lần sửa nhỏ.

## Khi nào dùng
- EFI vừa hoàn chỉnh và `efi-validate` báo 0 lỗi → tạo build mới.
- Một vòng "người dùng test → gửi log → sửa" kết thúc bằng EFI hoàn chỉnh mới.
- `usb-deploy-guard` gọi để lưu EFI hiện có trên USB (chỉ khi nội dung khác mọi snapshot).
- KHÔNG dùng cho các sửa dở dang giữa chừng.

## Cách dùng (chạy từ thư mục gốc dự án)
1. Xem trước: `python3 .claude/skills/efi-snapshot/scripts/snapshot.py --label "<nhãn-ngắn>" --note "<thay đổi so với build trước, lỗi nào đã xử lý>" --ocvalidate-result "<kết quả efi-validate>" --dry-run`
2. Chạy thật: bỏ `--dry-run`.
3. Đọc kết quả:
   - `SKIP: identical ...` → EFI trùng một snapshot có sẵn, không tạo thêm. Bình thường.
   - `STOP: oldest snapshot ... known-good` (exit 3) → DỪNG, hỏi người dùng. Không tự xoá.
   - `OK: created build-NN-...` → xong. Script tự ghi `docs/BUILD-LOG.md`, kiểm hash sau khi chép,
     và xoá snapshot cũ nhất nếu vượt 3.
4. Cập nhật `docs/STATE.md` (build mới nhất).

## Snapshot EFI hiện có trên USB
`--source <mount>/EFI --label usb-before-deploy` (thường do `usb-deploy-guard` tự gọi). Bỏ qua nếu trùng một snapshot.

## Đánh dấu known-good
CHỈ khi người dùng yêu cầu rõ ràng: `--mark-known-good build-NN`. Không bao giờ tự đánh dấu.

## Quy tắc cứng
- Chỉ ghi/xoá bên trong `<workspace>\snapshots\`. Script từ chối đường dẫn ngoài phạm vi.
- Tối đa 10 (người dùng đổi từ 3, 2026-11-02). Không sửa tay MANIFEST hay thư mục snapshot ngoài script.
- Mỗi snapshot có `MANIFEST.md/.json`: thay đổi, danh sách kext + phiên bản, SHA256 config.plist,
  kết quả ocvalidate, cờ known-good. Không ghi serial/MLB/UUID thật vào `--note`.
