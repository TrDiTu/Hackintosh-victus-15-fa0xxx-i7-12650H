---
name: ssdt-authoring
description: Author, compile and wire custom ACPI SSDTs for the target laptop from its REAL DSDT - e.g. powering off an unsupported dGPU, enabling the GPIO/I2C controller for a touchpad, EC, backlight, CPU power management. Use whenever the task needs an SSDT or ACPI patch, when the user says "SSDT", "DSDT", "ACPI", "tắt dGPU", "GPIO", "touchpad I2C", "iasl", or when a sample SSDT from another machine is about to be reused.
---

# ssdt-authoring

SSDT phải viết từ DSDT thật của MÁY B. SSDT/patch mẫu của máy khác = rủi ro treo máy hoặc không có tác dụng.

## Điều kiện
- Có DSDT/SSDT thật trong `docs/hw-dump/acpi/` (do người dùng dump trên MÁY B). Chưa có → dừng, hướng dẫn
  người dùng dump (SSDTTime/acpidump, hoặc OpenCore debug `SysReport`), chờ.
- Có `iasl` bản portable chính thức (ACPICA) trong `tools/` (ghi nguồn + SHA256 vào `docs/SOURCES.md`).
  Chưa có và chưa được phép tải → hỏi người dùng.

## Quy trình
1. **Xác định mục tiêu** từ `MACHINE-ANALYSIS.md`/`DRIVER-MATRIX.md` (ví dụ: tắt dGPU, GPIO cho VoodooI2C,
   EC giả, PNLF, CPU PM). Mỗi SSDT một mục đích, ghi lý do vào `docs/BUILD-LOG.md`.
2. **Tìm đối tượng ACPI thật:** giải mã DSDT/SSDT thành `.dsl` (`iasl -d`) trong `_cache/acpi/` (không ghi vào
   `docs/hw-dump/`). Tìm đúng đường dẫn thiết bị bằng Hardware ID/ACPI ID (`_HID`, `_ADR`, `_CID`).
   Ghi lại đường dẫn tìm được và dòng nguồn trong DSDT làm bằng chứng.
3. **Viết SSDT** dạng `External(...)` + `Scope(...)`, bọc điều kiện `If (_OSI ("Darwin"))` khi phù hợp, kiểm tra
   `CondRefOf` trước khi gọi phương thức không chắc tồn tại. Đặt tên file mô tả, `OEM ID/Table ID` rõ ràng.
4. **Biên dịch:** `iasl -ve SSDT-XXX.dsl` → phải 0 lỗi; xem lại cảnh báo. Giữ `.dsl` trong `docs/acpi-src/`,
   `.aml` vào `EFI/OC/ACPI/`.
5. **Nối vào config.plist:** thêm vào `ACPI/Add` (Enabled), kiểm tra thứ tự nếu có phụ thuộc. Nếu cần đổi tên
   (`ACPI/Patch`), ghi rõ Find/Replace/OemTableId/TableLength để tránh đổi nhầm bảng.
6. Chạy `efi-validate`. Ghi vào `docs/TEST-PLAN.md` cách kiểm tra SSDT có tác dụng trên MÁY B
   (ví dụ `ioreg`, trạng thái dGPU, kext Voodoo nhận thiết bị).

## Mẫu gợi ý (minh hoạ cấu trúc, KHÔNG sao chép nguyên văn; đường dẫn là placeholder)
Tắt nguồn dGPU khi boot macOS, theo kiểu gọi `_OFF` của chính thiết bị đó:
```asl
DefinitionBlock ("", "SSDT", 2, "HACK", "DGPUOFF", 0x00000000)
{
    External (_SB_.PCI0.<DGPU_PATH>, DeviceObj)
    External (_SB_.PCI0.<DGPU_PATH>._OFF, MethodObj)

    Scope (\_SB.PCI0.<DGPU_PATH>)
    {
        Method (_INI, 0, NotSerialized)
        {
            If (_OSI ("Darwin"))
            {
                If (CondRefOf (\_SB.PCI0.<DGPU_PATH>._OFF))
                {
                    \_SB.PCI0.<DGPU_PATH>._OFF ()
                }
            }
        }
    }
}
```
Mọi mẫu khác (GPIO, EC, PNLF) phải đối chiếu tài liệu OpenCore/Dortania đúng phiên bản và DSDT thật trước khi dùng.
Nếu không tìm được phương thức `_OFF` hợp lệ: dùng phương án dự phòng trong `GPU-STRATEGY.md`
(tuỳ chọn BIOS hoặc `disable-gpu` của WhateverGreen).

## Không làm
- Không dùng SSDT mẫu của máy khác khi chưa đối chiếu DSDT thật. Không đoán đường dẫn ACPI.
- Không sửa DSDT gốc của máy; chỉ thêm SSDT/patch qua OpenCore.
- Không tuyên bố SSDT "hoạt động" cho tới khi người dùng test trên MÁY B và báo kết quả.

## Dùng R1 làm tham khảo, không làm thay thế
Có thể đọc SSDT/ACPI dump của repo R1 (`docs/REFERENCES.md`) để biết dòng máy này thường cần xử lý gì (ví dụ đường dẫn
dGPU/touchpad). Nhưng vẫn phải xác minh đường dẫn trên DSDT thật của người dùng (BIOS F.34 có thể khác bản của R1),
tự viết SSDT và không chép nguyên file `.aml`/`.dsl` của repo.
