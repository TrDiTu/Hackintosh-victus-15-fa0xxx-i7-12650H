# XEGFX-PROGRESS — Theo Dõi Tiến Độ Thử Nghiệm Driver Đồ Hoạ XeGfx

*Mục tiêu phần cứng: Intel UHD / Iris Xe Graphics Alder Lake-P GT1 (`8086:46A3`)*  
*Target OS: macOS 26 Tahoe (Darwin 25)*  
*XeGfx Version: `0.0.38` (Commit `78db6fceab4a6d50c3072c12e5ea89688f281d26`)*  

---

## 1. Bảng Trạng Thái Tiến Độ Từng Stage

| Stage | Nội dung kiểm thử | Trạng thái hiện tại | Bằng chứng / Log | Vấn đề / Ghi chú | Kết luận |
|---|---|---|---|---|---|
| **Pha 6** | Chuẩn bị môi trường & Runbook | **HOÀN TẤT** | `docs/XEGFX-RUNBOOK.md`, bộ script `xegfx-test/` | XeGfx 0.0.38 đã được tải và kiểm tra hash SHA256. | Đã sẵn sàng thử nghiệm |
| **Stage 1** | Shim state & Vmap memory path | **CHỜ CHẠY** | Chưa có | Cần chạy `02-run-stage.sh 1` sau khi install và reboot | Chưa đánh giá |
| **Stage 2** | Read-only GPU probe (`XeGfxProbe`) | **CHỜ CHẠY** | Chưa có | Đọc PCI ID `8086:46A3`, BARs, stolen memory | Chưa đánh giá |
| **Stage 3** | Newbus & DMA layer | **CHỜ CHẠY** | Chưa có | Gán driver `vgapci0`, DMA tags | Chưa đánh giá |
| **Stage 4** | DRM & i915 init (Display off) | **CHỜ CHẠY** | Chưa có | Kiểm tra i915 core, giữ nguyên display scan-out | Chưa đánh giá |
| **Stage 5** | Engine request test | **CHƯA MỞ** | Chưa có | Yêu cầu Stage 4 pass hoàn toàn | Chưa đánh giá |
| **Stage 6** | GPU compute dword write/read | **CHƯA MỞ** | Chưa có | Yêu cầu Stage 5 pass hoàn toàn | Chưa đánh giá |
| **Stage 7** | XeGfxAccel / Desktop composite | **CHƯA MỞ** | Chưa có | Cần Mesa ANV và Metal plugin | Chưa đánh giá |

---

## 2. Nhật Ký Chi Tiết Từng Lần Chạy

### Pha 6: Khởi tạo Giai đoạn B (2026-10-25)
- Người dùng gửi câu lệnh chính thức kích hoạt Giai đoạn B: `"EFI nền đã ổn định, bắt đầu XeGfx"`.
- Snapshot `build-10` được xác nhận là mốc `known-good: true` của EFI nền.
- Đã đọc và xác minh tài liệu mới nhất từ GitHub XeGfx (commit `78db6fceab4a6d50c3072c12e5ea89688f281d26`, 2026-10-24).
- Soạn thảo `docs/XEGFX-RUNBOOK.md` và hoàn thiện bộ script tự động hóa trong `xegfx-test/`:
  - `00-collect-baseline.sh`: Thu thập thông số baseline của macOS trước khi cài XeGfx.
  - `01-install-xegfx.sh`: Cài đặt XeGfx vào Auxiliary Kernel Collection với cơ chế backup an toàn.
  - `02-run-stage.sh`: Kích hoạt và nạp từng stage (1 $\rightarrow$ 4), thu thập kết quả và driver logs.
  - `99-uninstall-xegfx.sh`: Gỡ bỏ hoàn toàn XeGfx và khôi phục collection sạch.
- Đã tải binary chính thức `XeGfx-0.0.38.zip`, kiểm tra mã băm SHA256 `10FA402C966CB60F444C026FB9EC6E73C6C6467A13D2742A5E08BB6007899A87` và cập nhật vào `docs/SOURCES.md`.