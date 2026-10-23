# STATE — bộ nhớ giữa các phiên (Codex cập nhật cuối mỗi phiên/pha)

- Cập nhật lần cuối: 2026-10-24
- Giai đoạn / Pha hiện tại: Giai đoạn A, Pha 5 (Triển khai USB & Kiểm thử thực tế) — Đã ghi EFI thành công lên G:\EFI, CHỜ KẾT QUẢ BOOT TỪ MÁY B
- Đang chờ: Người dùng boot thử USB trên MÁY B theo docs/TEST-PLAN.md và phản hồi kết quả / log lỗi (nếu có)

## Đã được người dùng duyệt
- Hoàn thành Pha 0: Xác minh 100% ID phần cứng và đường dẫn ACPI từ MÁY B vào docs/MACHINE-ANALYSIS.md
- Hoàn thành Pha 1: Duyệt danh sách driver docs/DRIVER-MATRIX.md
- Hoàn thành Pha 2: Xác lập GPU-STRATEGY và phương án SSDT tắt dGPU
- Hoàn thành Pha 3: Dựng thành công EFI build-01 (qua efi-validate 0 lỗi và tạo snapshot build-01)
- Hoàn thành Pha 4: Lập kế hoạch kiểm thử docs/TEST-PLAN.md (5 giai đoạn kiểm thử, cách thu log, rollback)
- Hoàn thành Pha 5 (Triển khai): Người dùng đã duyệt ổ USB ("đúng USB, ghi đi"), skill usb-deploy-guard đã ghi thật thành công vào G:\EFI và đối chiếu mã băm khớp 100%.

## Quyết định quan trọng
- Đã triển khai EFI hoàn chỉnh sang `G:\EFI`:
  + Cổng validation: Đạt chuẩn (0 lỗi, 0 cảnh báo, ocvalidate hoàn tất, treeHash khớp build-01: `e22679c6d824bbfd603b069d1ec3d9508026c1d8822852a629ff4413cf23b234`).
  + Ổ đích: Drive `G:`, Label `MACEFI`, FileSystem `FAT32`, Removable USB.
  + Thư mục bộ cài `G:\com.apple.recovery.boot` được giữ nguyên vẹn 100%.
  + Thao tác ghi được thực hiện an toàn qua skill `usb-deploy-guard` (robocopy mirror + đối chiếu SHA256 tree hash).
  + Debug logging được bật (Target 67) để ghi log OpenCore ra file trên USB nếu boot thất bại.

## Bản build
- Mới nhất: build-01-20261024-041414-base-tahoe (treeHash: `e22679c6d824bbfd603b069d1ec3d9508026c1d8822852a629ff4413cf23b234`)
- known-good: (chưa có — chờ người dùng test trên Máy B)

## Việc người dùng cần làm
1. **Safely Remove (Eject) USB** an toàn trên MÁY A trước khi rút ra.
2. Cắm dây mạng LAN vào MÁY B (để tải gói cài đặt qua card Realtek RTL8111 nếu bộ cài yêu cầu kết nối mạng).
3. Kiểm tra cài đặt BIOS trên MÁY B (HP Victus 15):
   - Secure Boot: **Disabled**
   - Fast Boot: **Disabled**
   - VMD / Intel RST: Đảm bảo chạy chế độ **AHCI** (hoặc Native NVMe)
   - Chế độ đồ họa: **Hybrid / Dynamic** (KHÔNG chọn Discrete Only / dGPU Only)
   - VT-d: Bật bình thường (EFI đã có `DisableIoMapper = true` xử lý RMRR)
4. Cắm USB vào cổng USB-A bên trái/phải của MÁY B.
5. Bật máy, nhấn liên tục **F9** (Boot Menu của HP) -> Chọn USB UEFI (thường có tên dạng UEFI: USB... hoặc tên nhãn USB).
6. Tại menu OpenCore:
   - Chọn mục **Reset NVRAM** đầu tiên (để xoá sạch NVRAM cũ), máy sẽ tự khởi động lại.
   - Nhấn tiếp F9 -> Chọn lại USB UEFI -> Chọn **macOS Base System (External)** hoặc bộ cài.
7. Theo dõi màn hình verbose (chữ chạy):
   - Nếu vào được Recovery / Trình cài đặt macOS: Báo lại để tiếp tục kiểm tra bàn phím, touchpad, mạng.
   - Nếu bị đứng (freeze) hoặc kernel panic: Rút USB, cắm lại vào MÁY A, gửi file log `opencore-YYYY-MM-DD-HHMMSS.txt` trên thư mục gốc của USB (hoặc chụp ảnh màn hình dừng) cho Codex phân tích.

## Rủi ro / CHƯA XÁC MINH đang mở
- Cổng HDMI ngoài không xuất hình do dGPU RTX 3050 Ti bị tắt.
- iGPU Iris Xe chạy basic framebuffer không tăng tốc 3D (QE/CI) trong Giai đoạn A.
