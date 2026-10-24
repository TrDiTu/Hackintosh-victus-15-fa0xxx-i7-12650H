# Touchpad ELAN0788 — 2026-10-25

## Kết quả máy B

**Đã deploy:** người dùng xác nhận ghi USB; build-10 đã lên G:\EFI lúc 2026-10-25 01:47:29 qua usb-deploy-guard, hash cây `2e5c3fc66324` khớp workspace. Chờ kiểm thử touchpad trên máy B; trạng thái chờ xác nhận ghi dưới đây là lịch sử.

**Trạng thái chuẩn bị mới nhất:** người dùng đã duyệt thử fork trên Tahoe. Build `build-10-20261025-014543-touchpad-adl-driver` đã thay core/plugins/HID; không đổi config.plist, ACPI hay thành phần khác. efi-validate: 0 lỗi, 0 cảnh báo, ocvalidate đã chạy; báo cáo `docs/validation/validate-20261025-014527.md`. Giữ build-09 để rollback. USB đã dry-run đúng G: MACEFI FAT32 2,99 GB; đang chờ xác nhận ghi build-10. Các dòng ứng viên/chờ duyệt phía dưới là lịch sử trước khi duyệt thử.

Người dùng xác nhận build-09 boot thành công; touchpad và âm thanh chưa hoạt động.
Ưu tiên touchpad. Chưa có IORegistry hoặc log VoodooI2C của lần boot này.

## Bằng chứng và giới hạn

- `docs/hw-dump/lspci-nnk.txt`: I2C0 tại 00:15.0, PCI 8086:51E8.
- `docs/hw-dump/i2c-devices.txt`: ELAN0788:00, PNP0C50, Linux i2c_hid_acpi.
- DSDT thật HPQOEM/8A4F: `\_SB.PC00.I2C0`, `_ADR=0x00150000`; touchpad `TPD0` có `_CID=PNP0C50`, địa chỉ I2C 0x15, tốc độ 400000 Hz, HID descriptor address 1.
- Giải mã trong `_cache/acpi/DSDT.dsl`: I2C0 dòng 12213; GPI0 dòng 13823; TPD0 dòng 73909. DSDT có external methods chưa resolve đầy đủ; không biên dịch lại hoặc thay DSDT gốc.
- Kext đang dùng thực tế là VoodooI2C **2.9.1**, không phải 2.8 như ma trận cũ. IOPCIMatch của bản này không khớp 8086:51E8; DeviceProperties cũng chưa có override cho I2C0. Đây là lỗi matching xác định được từ cấu hình tĩnh, cần IORegistry để xác nhận trạng thái attach trên máy B.
- TPD0 `_CRS` chỉ trả `SBFI` (interrupt, thiếu I2cSerialBus) nếu OSYS < 0x07DC. Giá trị OSYS thực tế trên macOS chưa biết; chưa tự thêm XOSI hoặc override `_CRS`.
- Patch GPI0 hiện tại có đúng một match trong DSDT gốc, nằm ở phương thức GPI0._STA. Chưa có lý do sửa patch này.

## Phương án thử được chuẩn bị

Thay bộ VoodooI2C/VoodooI2CHID và plugin đi kèm bằng release **3.0.0 của lzhoang2801/VoodooI2C**. Giữ polling, các SSDT, boot-args và IntelBTPatcher tắt như build-09. Không spoof PCI ID, không đổi audio hoặc đồ họa. Thử driver trước; chỉ sửa ACPI tiếp nếu log cho thấy tài nguyên touchpad bị thiếu.

- Release chính tác giả fork: https://github.com/lzhoang2801/VoodooI2C/releases/tag/3.0.0
- PR lên upstream, đang mở/chưa merge lúc kiểm tra: https://github.com/VoodooI2C/VoodooI2C/pull/586
- License: GPL-3.0. Đây là fork, không phải release mới của upstream VoodooI2C.
- Archive tải vào `_cache/downloads/VoodooI2C-lzhoang2801-3.0.0-RELEASE.zip`.
- SHA256: `703a21ef1d7bafb47a774ce28020b9eeae4ead6c2bc78f82899c43daae56cc36`.
- Release tag là 3.0.0 nhưng tên zip và CFBundleVersion vẫn 2.9.1; phải phân biệt bằng nguồn/hash.
- Đã kiểm tra plist trong archive: personality AlderLake chứa `0x51e88086&0xFFFCFFFF`, clock 133 MHz; plugin GPIO có INTC1055. Phù hợp ID bộ điều khiển máy B.
- **CHƯA XÁC MINH TAHOE** cho fork này. Issue upstream 582 nói tới Tahoe với VoodooI2C 2.9.1 nhưng dùng HID tự sửa trên máy khác; không dùng làm chứng minh fork hỗ trợ máy B.
- Rủi ro: không attach, panic, lỗi wake hoặc gesture. Chưa đưa ứng viên vào EFI; chờ người dùng duyệt ngoại lệ thử nghiệm theo AGENTS.md §4 và driver-vetting.
- Kiểm tra chuẩn bị: CRC toàn bộ archive đạt; 5 plist của bộ core/plugin/HID đọc được, không thiếu phụ thuộc ngoài Apple trong bộ này. Hash toàn bộ EFI workspace vẫn khớp snapshot build-09. Script thu log dùng LF; chưa chạy trên máy B.
- Rollback: snapshot `build-09-20261025-010852-disable-intelbtpatcher` đã được người dùng báo boot thành công, chưa gán cờ known-good.

## Kiểm thử trên máy B

1. Sau khi duyệt, dựng/validate/snapshot bản thử và deploy qua usb-deploy-guard theo phạm vi được duyệt.
2. Boot macOS; thử di chuyển, click, tap, cuộn hai ngón. Báo riêng từng chức năng.
3. Nếu vẫn không hoạt động, chạy `bash collect-touchpad.sh` trong Terminal trên máy B (script ở `tools/collect-touchpad.sh`, chép sang máy B bằng phương tiện người dùng chọn). Mang thư mục kết quả về `logs/`. Không chạy script này trên máy A.
4. Nếu có panic, mang báo cáo mới về và quay lại build-09. Nếu ổn, kiểm tra restart và sleep/wake.
5. Âm thanh xử lý sau touchpad. Chưa bắt đầu XeGfx: cần xác nhận EFI nền ổn định và yêu cầu mở Giai đoạn B theo AGENTS.md §6.
