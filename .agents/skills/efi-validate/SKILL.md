---
name: efi-validate
description: Validate an OpenCore EFI folder before snapshotting or writing to USB - checks required files, config.plist references vs real files, kext load order and dependencies, MaxKernel vs macOS 26 Tahoe (Darwin 25), unreferenced files, placeholder SMBIOS, and runs ocvalidate. Use whenever you finished editing EFI/config.plist/kexts/SSDTs, before efi-snapshot, before usb-deploy-guard, or when the user says "kiểm tra EFI", "validate", "ocvalidate", "check config.plist".
---

# efi-validate

Kiểm tra tĩnh bản EFI. Máy kiểm tra bắt lỗi file thiếu/sai thứ tự chính xác hơn con người.

## Chạy (từ thư mục gốc workspace)
```
powershell -File .\.agents\skills\efi-validate\scripts\validate-efi.ps1
```
Tuỳ chọn: `-EfiPath <thư mục EFI>`, `-OcValidate <đường dẫn ocvalidate.exe>`.

Script ghi `docs/validation/validate-<time>.md` (báo cáo đầy đủ) và `docs/validation/latest.json`
(`usb-deploy-guard` dùng file này làm điều kiện ghi USB). Exit 0 = không lỗi, exit 1 = có lỗi.

## Script kiểm tra những gì
- File bắt buộc: `BOOT\BOOTx64.efi`, `OC\OpenCore.efi`, `OC\config.plist` (đọc được như plist XML).
- ACPI/Kernel/UEFI Drivers/Misc Tools: mọi mục đang bật phải có file thật; `OpenRuntime.efi` phải bật.
- Kext: tồn tại `ExecutablePath`/`PlistPath`; phụ thuộc trong `OSBundleLibraries` (bỏ qua `com.apple.*`) phải
  được bật và nằm TRƯỚC kext phụ thuộc; cảnh báo `MaxKernel` loại trừ Tahoe (Darwin 25).
- File "mồ côi" trong `OC\ACPI`, `OC\Kexts`, `OC\Drivers` không được config tham chiếu.
- SMBIOS: chỉ báo PLACEHOLDER hay "giá trị thật" (không in giá trị). Giá trị thật → cảnh báo.
- In ra SecureBootModel, Debug Target, boot-args để rà soát.
- Chạy `ocvalidate` (tự tìm `tools\**\ocvalidate.exe`, hoặc truyền `-OcValidate`).

## Xử lý kết quả
1. Mọi `[ERROR]` phải sửa, rồi chạy lại cho tới khi 0 lỗi.
2. Với `[WARN]`: xem từng cái, sửa hoặc ghi lý do chấp nhận vào `docs/BUILD-LOG.md`.
3. `ocvalidate.exe` phải cùng phiên bản với `OpenCore.efi`. Lấy từ release chính thức của OpenCorePkg
   (ghi vào `docs/SOURCES.md`), đặt trong `tools/`. Không có ocvalidate → kết quả coi như CHƯA XÁC MINH.
4. `ocvalidate` có thể phàn nàn về PlatformInfo khi dùng placeholder `CHANGE_ME_*`: đó là dự kiến cho đến
   khi người dùng sinh SMBIOS thật bằng macserial. Ghi rõ trong báo cáo, đừng tự bịa giá trị.
5. Chỉ khi 0 lỗi mới được `efi-snapshot` và sau đó `usb-deploy-guard`. Truyền tóm tắt kết quả cho
   `-OcValidateResult` của snapshot (ví dụ `0 errors, 3 warnings`).

## Giới hạn (nói thẳng với người dùng)
- Script không thay thế việc đọc `Configuration.pdf`. Nó không biết patch/quirk có đúng cho máy hay không.
- "Validate sạch" ≠ "boot được" ≠ "thiết bị hoạt động". Chỉ test thật trên MÁY B mới chứng minh.
