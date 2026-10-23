# STATE — bộ nhớ giữa các phiên (Codex cập nhật cuối mỗi phiên/pha)

- Cập nhật lần cuối: 2026-10-24
- Giai đoạn / Pha hiện tại: Giai đoạn A, Pha 0 (Kiểm kê phần cứng — Đang chờ dữ liệu dump từ MÁY B)
- Đang chờ: Người dùng chạy tools/dump-laptop.ps1 và trích xuất DSDT/SSDT trên MÁY B, chép vào docs/hw-dump/ và docs/hw-dump/acpi/

## Đã được người dùng duyệt
- (chưa có)

## Quyết định quan trọng
- Khởi tạo bảng phân tích sơ bộ docs/MACHINE-ANALYSIS.md từ laptop-specs.md; đánh dấu CHƯA XÁC MINH cho các thiết bị cần dump thực tế.
- Xác định kiến trúc: CPU Alder Lake-H i7-12650H + iGPU Iris Xe 8086:46A3 + dGPU RTX 3050 Ti Mobile 10DE:25A0.
- dGPU phải vô hiệu hoá bằng SSDT (chờ DSDT thật để tìm phương thức _OFF); cổng HDMI dự kiến ngắt tín hiệu khi dGPU tắt.
- iGPU chạy chế độ hiển thị cơ bản trong Giai đoạn A (VESA framebuffer); không inject XeGfx vào EFI.
- Bắt buộc chuẩn bị bộ cài macOS 26 Tahoe offline vì Wi-Fi Intel AX211 không dùng được trong Recovery.

## Bản build
- Mới nhất: (chưa có)
- known-good: (chưa có)

## Việc người dùng cần làm
1. Chạy tools/dump-laptop.ps1 bằng PowerShell (Administrator) trên MÁY B, chép thư mục kết quả vào docs/hw-dump/.
2. Trích xuất DSDT và các bảng SSDT gốc trên MÁY B (bằng SSDTTime hoặc acpidump), chép vào docs/hw-dump/acpi/.
3. Kiểm tra các mục BIOS trên MÁY B: Tắt Secure Boot, Tắt Fast Boot, đảm bảo chế độ ổ đĩa là AHCI (không bật Intel RST/VMD), giữ chế độ GPU Hybrid.

## Rủi ro / CHƯA XÁC MINH đang mở
- Chưa có file DSDT gốc để xác định đường dẫn ACPI chính xác của dGPU và GPIO Pinning cho trackpad ELAN0788.
- Chưa có USB dump để map topology cổng USB (camera, bluetooth, type-C).
- Cổng HDMI ngoài nối dGPU nên sẽ không xuất hình khi dGPU bị ngắt nguồn trong macOS.
