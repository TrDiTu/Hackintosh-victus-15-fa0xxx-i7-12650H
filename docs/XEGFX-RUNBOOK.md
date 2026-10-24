# XEGFX-RUNBOOK — Hướng Dẫn Thử Nghiệm Từng Bước Driver Đồ Hoạ XeGfx (Giai Đoạn B)

*Mục tiêu: Đánh giá khả năng tương thích của driver XeGfx trên iGPU Intel Alder Lake-P GT1 (`8086:46A3`) của HP Victus 15-fa0xxx, chạy macOS 26 Tahoe.*  
*Tài liệu tham chiếu chính thức: [watchthelight-labs/XeGfx](https://github.com/watchthelight-labs/XeGfx)*  
*Commit xác minh: `78db6fceab4a6d50c3072c12e5ea89688f281d26` (2026-10-24 12:05:27 -0400)*  
*Ngày đọc & đối chiếu tài liệu: 2026-10-25*  
*Bản phát hành chính thức: XeGfx `v0.0.38` (SHA256: `10FA402C966CB60F444C026FB9EC6E73C6C6467A13D2742A5E08BB6007899A87`)*  

---

## 1. Nguyên Tắc An Toàn Cốt Lõi

1. **Kext XeGfx TUYỆT ĐỐI KHÔNG nạp lúc boot:**
   - Kext không nằm trong EFI và không có PCI personality khớp tự động khi khởi động.
   - Kext chỉ nằm trong Auxiliary Kernel Collection (`/Library/Extensions`) và chỉ được kích hoạt bằng lệnh thủ công: `kmutil load -b org.watchthelight.XeGfx`.
2. **Cơ chế tự phục hồi sau sự cố:**
   - Nếu trong quá trình chạy một stage xảy ra lỗi, kernel panic hoặc đứng máy: Bộ đếm thời gian (Watchdog `debug.xegfx_wdog`, mặc định 60 giây) sẽ chủ động kích hoạt panic để ghi dump và khởi động lại.
   - Khi máy khởi động lại, XeGfx **hoàn toàn không được nạp**, hệ thống tự động trở về giao diện macOS bình thường với EFI nền `build-10` đã kiểm định.
3. **Thực hiện tuần tự Stage 1 $\rightarrow$ 4:**
   - Tuyệt đối không nhảy cóc qua các stage. Mỗi stage cần được người dùng chạy, thu thập log mang về cho Codex phân tích trước khi quyết định chạy stage tiếp theo.

---

## 2. Tiền Điều Kiện Trước Khi Thử Nghiệm

1. **EFI Nền Ổn Định:**
   - Bản EFI hiện tại: `build-10` (đã đánh dấu `known-good: true` sau khi người dùng xác nhận touchpad và các tính năng cơ bản hoạt động ổn định).
2. **Cấu hình BIOS:**
   - Card đồ hoạ: Duy trì chế độ **Hybrid** (màn hình nội bộ eDP 1080p do iGPU điều khiển).
   - Secure Boot: `Disabled`.
3. **Bảo mật macOS (SIP & Secure Boot):**
   - Đã cấu hình trong EFI: `csr-active-config` = `0x0FEF` (cho phép tải kext ngoài AuxKC), `SecureBootModel` = `Disabled`, `DisableIoMapper` = `true`.
4. **Thu thập Baseline Log (Mốc đối chiếu ban đầu):**
   - Chạy script baseline trên Máy B:
     ```bash
     bash xegfx-test/00-collect-baseline.sh
     ```
   - Kết quả sẽ được ghi vào thư mục `xegfx-test/logs/baseline-*.txt`.

---

## 3. Cài Đặt XeGfx Vào Auxiliary Kernel Collection

*Lưu ý: Thư mục `xegfx-test` đã có sẵn binary chính thức `XeGfx.kext` (v0.0.38).*

1. Mở Terminal trên Máy B trong thư mục `xegfx-test/`:
2. Chạy lệnh cài đặt:
   ```bash
   sudo bash 01-install-xegfx.sh
   ```
   *Quá trình này sẽ:*
   - Sao lưu Auxiliary Kernel Collection hiện tại vào `/Library/XeGfx/backup-...`.
   - Copy `XeGfx.kext` vào `/Library/Extensions` với quyền `root:wheel`.
   - Tạo lại `AuxiliaryKernelExtensions.kc` mới có chứa `org.watchthelight.XeGfx`.
3. **Khởi động lại máy (Reboot):**
   - Sau khi script báo hoàn tất, khởi động lại macOS để kernel nhận diện collection mới.
   - Sau khi boot vào lại Desktop, mở Terminal kiểm tra xem kext đã cài nhưng CHƯA load:
     ```bash
     kextstat | grep -i "xegfx"
     ```
     *(Kết quả phải là TRỐNG — kext chưa được nạp, màn hình hoạt động bình thường)*.

---

## 4. Trình Tự Kiểm Thử Từng Stage (Stage 1 $\rightarrow$ 4)

### Stage 1: Kiểm thử Shim State & Vmap Memory Path
- **Mục đích:** Khởi tạo lớp tương thích FreeBSD kernel trên XNU (threads, locks, UMA, VM pages, taskqueues) và kiểm tra khả năng map bộ nhớ kernel (`xg_vm_vmap_selftest`).
- **Lệnh thực thi:**
  ```bash
  sudo bash xegfx-test/02-run-stage.sh 1
  ```
- **Thời gian chờ:** ~5 – 10 giây (watchdog: 60s).
- **Tiêu chuẩn Đạt (Pass):**
  - Exit code 0, không panic.
  - `debug.xegfx_results` trả về `1` (pass). Không gặp mã lỗi `-12` (vmap failure).
- **Thu thập log:** Mang file log `xegfx-test/logs/stage1-*.log` về cho Codex.

---

### Stage 2: Read-Only Probe Phần Cứng iGPU
- **Mục đích:** Đọc thông số phần cứng iGPU ở chế độ CHỈ ĐỌC (PCI ID, BAR sizes, GMD_ID, stolen-memory base, pipe A registers, GGTT entry) và xuất dictionary `XeGfxProbe` vào IORegistry. Hoàn toàn không ghi đè thanh ghi hay khởi tạo bộ nhớ đồ hoạ.
- **Lệnh thực thi:**
  ```bash
  sudo bash xegfx-test/02-run-stage.sh 2
  ```
- **Thời gian chờ:** ~5 – 10 giây.
- **Tiêu chuẩn Đạt (Pass):**
  - Màn hình laptop giữ nguyên hiển thị bình thường, không giật hay đổi màu.
  - `debug.xegfx_results` trả về `1`.
  - Kiểm tra entry IORegistry có chứa đầy đủ thông số GPU:
    ```bash
    ioreg -p IOService -n XeGfxResident -l
    ```
- **Thu thập log:** Ghi nhận dictionary `XeGfxProbe` và gửi log `xegfx-test/logs/stage2-*.log` cho Codex.

---

### Stage 3: Khởi Tạo Newbus & Lớp DMA
- **Mục đích:** Xây dựng cây newbus trên toàn bộ bus PCI, liên kết với thiết bị đồ họa Intel (`8086:46A3`), chuẩn bị các tag DMA và cấu hình ngắt MSI.
- **Lệnh thực thi:**
  ```bash
  sudo bash xegfx-test/02-run-stage.sh 3
  ```
- **Thời gian chờ:** ~5 – 10 giây.
- **Tiêu chuẩn Đạt (Pass):**
  - `debug.xegfx_results` trả về `1`.
  - Newbus gán thành công driver `vgapci0` vào GPU Intel mà không động chạm tới card NVIDIA RTX 3050 Ti đã tắt.
- **Thu thập log:** Gửi log `xegfx-test/logs/stage3-*.log` cho Codex.

---

### Stage 4: Khởi Tạo Driver DRM & i915 (Display Disabled)
- **Mục đích:** Kích hoạt các SYSINIT của drm, TTM, dma-buf và i915 core. Display của i915 được TẮT (`compat.linuxkpi.i915_disable_display=1`) để không tranh chấp với framebuffer của firmware/macOS; kiểm tra bộ nhớ stolen và scan-out của panel.
- **Lệnh thực thi:**
  ```bash
  sudo bash xegfx-test/02-run-stage.sh 4
  ```
- **Thời gian chờ:** ~15 – 30 giây.
- **Tiêu chuẩn Đạt (Pass):**
  - i915 core khởi tạo thành công, nhận diện GT và engine.
  - Màn hình laptop không bị đen, không bị sọc hình hay treo cứng.
  - `debug.xegfx_results` trả về `1`.
- **Thu thập log:** Gửi file log `xegfx-test/logs/stage4-*.log` cho Codex phân tích.

---

## 5. Kế Hoạch Ứng Cứu & Gỡ Bỏ (Rollback Plan)

1. **Khi gặp Kernel Panic hoặc Treo Máy:**
   - Nhấn giữ nút Nguồn để tắt máy, sau đó bật lại máy.
   - Do XeGfx không nạp lúc boot, máy sẽ khởi động bình thường vào Desktop macOS.
   - Vào thư mục `/Library/Logs/DiagnosticReports/`, tìm file `Kernel-YYYY-MM-DD-*.panic` mới nhất, chép ra để gửi cho Codex phân tích nguyên nhân bằng skill `log-analysis`.
2. **Gỡ bỏ hoàn toàn XeGfx khỏi hệ thống:**
   - Chạy script gỡ bỏ:
     ```bash
     sudo bash xegfx-test/99-uninstall-xegfx.sh
     ```
   - Khởi động lại máy.
3. **Phục hồi EFI:**
   - Thư mục EFI hoàn toàn không bị thay đổi trong quá trình thử nghiệm XeGfx, bản snapshot `build-10` luôn sẵn sàng dự phòng.

---

## 6. Mẫu Báo Cáo Log Cho Người Dùng Gửi Codex

Khi hoàn thành mỗi stage hoặc gặp sự cố, người dùng dán kết quả theo định dạng sau:

```text
=== BÁO CÁO KẾT QUẢ XEGFX ===
Stage vừa chạy: [1 / 2 / 3 / 4]
Trạng thái màn hình: [Bình thường / Chớp nháy / Đen màn hình / Treo]
Kết quả sysctl:
- debug.xegfx_stage: ...
- debug.xegfx_results: ...
Nội dung 10-20 dòng cuối từ stageX-*.log (hoặc đính kèm file):
...
(Đã kiểm tra không chứa Serial/MLB/UUID thật)
```