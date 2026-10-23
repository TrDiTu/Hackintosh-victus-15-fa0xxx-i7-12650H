---
name: usb-deploy-guard
description: The ONLY allowed way to write the EFI to the USB drive G:\. Verifies G: is a USB/removable non-system disk, requires a clean efi-validate result, backs up the existing G:\EFI via efi-snapshot, mirrors the workspace EFI to G:\EFI only, and verifies by hash. Use whenever the user says "ghi lên USB", "deploy", "copy EFI sang G:", "cập nhật USB", or whenever anything needs to be written to G:\.
---

# usb-deploy-guard

Thao tác nguy hiểm duy nhất của dự án. Không bao giờ tự `robocopy`/`Copy-Item`/`Remove-Item` lên `G:\`.

## Quy trình (2 bước, bắt buộc có xác nhận của người dùng)

**Bước 1 — chạy thử (mặc định, không ghi gì):**
```
powershell -File .\.agents\skills\usb-deploy-guard\scripts\deploy-usb.ps1
```
- Script in thông tin USB (label, dung lượng, loại bus, filesystem) và kết quả kiểm tra cổng validation.
- HIỂN THỊ cho người dùng: tên/label/dung lượng của `G:` và danh sách thay đổi dự kiến.
- DỪNG, chờ người dùng xác nhận rõ ràng ("đúng USB, ghi đi").

**Bước 2 — ghi thật (chỉ sau khi người dùng xác nhận):**
```
powershell -File .\.agents\skills\usb-deploy-guard\scripts\deploy-usb.ps1 -Confirmed
```

## Script tự kiểm tra
- Chỉ nhận ổ `G`. Từ chối ổ hệ thống/boot hoặc ổ không phải USB/removable.
- Cổng validation: `docs/validation/latest.json` phải 0 lỗi, `ocvalidate` đã chạy, và hash trùng đúng nội dung
  EFI hiện tại (sửa EFI sau lần validate → phải validate lại).
- `G:\EFI` hiện có: nếu là OpenCore EFI → snapshot qua `efi-snapshot` (bỏ qua nếu trùng bản đã có);
  nếu chứa file lạ không phải EFI → dừng (exit 5), hỏi người dùng.
- Ghi bằng `robocopy /MIR` CHỈ vào `G:\EFI`, rồi so hash nguồn và đích.

## Mã thoát
0 xong · 1 lỗi · 4 chưa qua cổng validation · 5 `G:\EFI` có nội dung lạ · 6 snapshot bị chặn (ví dụ known-good).
Gặp 4 → chạy `efi-validate`. Gặp 5 hoặc 6 → hỏi người dùng, không tìm đường vòng.

## Sau khi ghi
- Nhắc người dùng "Safely Remove" USB trước khi rút.
- Cập nhật `docs/STATE.md` (đã triển khai build nào lên USB).
- Nhắc: USB phải cắm vào MÁY A khi ghi; sau đó người dùng cắm sang laptop để test.

## Không làm
- Không format, repartition, đổi label, chạy diskpart/Clear-Disk. Không ghi ngoài `G:\EFI`
  (ngoại lệ `G:\XeGfx-test` chỉ khi người dùng yêu cầu rõ và không dùng script này).
- Không nới lỏng cổng kiểm tra bằng cách sửa script hay `latest.json` bằng tay.
