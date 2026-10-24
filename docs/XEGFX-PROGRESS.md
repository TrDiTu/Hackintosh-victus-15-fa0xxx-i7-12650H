# XEGFX-PROGRESS — Theo Dõi Tiến Độ Thử Nghiệm Driver Đồ Hoạ XeGfx

*Mục tiêu phần cứng: Intel UHD / Iris Xe Graphics Alder Lake-P GT1 (`8086:46A3`)*  
*Target OS: macOS 26 Tahoe (Darwin 25, build 25G241, Darwin 25.6.0)*  
*XeGfx Version: `0.0.38` (Commit `78db6fceab4a6d50c3072c12e5ea89688f281d26`)*  

---

## 1. Bảng Trạng Thái Tiến Độ Từng Stage

| Stage | Nội dung kiểm thử | Trạng thái hiện tại | Bằng chứng / Log | Vấn đề / Ghi chú | Kết luận |
|---|---|---|---|---|---|
| **Pha 6** | Chuẩn bị môi trường & Runbook | **HOÀN TẤT** | `docs/XEGFX-RUNBOOK.md`, bộ script `xegfx-test/` | XeGfx 0.0.38 đã được nạp AuxKC an toàn | Đã sẵn sàng |
| **Stage 1** | Shim state & Vmap memory path | **PASS (ĐẠT)** | `logs/stage1-20261025-030650.log` | `debug.xegfx_results` = 1, `vmap selftest 0`, không crash | **VƯỢT QUA** |
| **Stage 2** | Read-only GPU probe (`XeGfxProbe`) | **PASS (ĐẠT)** | `logs/stage2-20261025-031101.log` | `debug.xegfx_results` = 1, `XeGfxProbe` xuất đủ BARs, pipe-a-lit=1, boot-fb-size=8294400 | **VƯỢT QUA** |
| **Stage 3** | Newbus & DMA layer | **PASS (ĐẠT)** | `logs/stage3-20261025-031302.log` | `debug.xegfx_results` = 1, Newbus gắn `vgapci0` -> `drmn0`, DMA vật lý chuẩn | **VƯỢT QUA** |
| **Stage 4** | DRM & i915 init (Display off) | **PANIC (DỪNG)** | `logs/Kernel-2026-10-25-032317.panic` | Page fault `CR2: 0x0` tại `_xg_vsnprintf` trong `_intel_detect_pch` -> `_lkpi_pci_get_class` | **LỖI UPSTREAM XEGFX** |
| **Stage 5** | Engine request test | **ĐÓNG** | N/A | Dừng lại ở Stage 4 do lỗi PCH probe | Chưa thể thực hiện |
| **Stage 6** | GPU compute dword write/read | **ĐÓNG** | N/A | Dừng lại ở Stage 4 | Chưa thể thực hiện |
| **Stage 7** | XeGfxAccel / Desktop composite | **ĐÓNG** | N/A | Dừng lại ở Stage 4 | Chưa thể thực hiện |

---

## 2. Nhật Ký Chi Tiết Từng Lần Chạy

### Pha 6: Khởi tạo Giai đoạn B (2026-10-25)
- Cổng chặn mở; snapshot `build-10` cố định mốc `known-good: true`.
- Tải release chính thức `XeGfx-0.0.38.zip`, tạo runbook và helper scripts.

### Baseline Analysis (2026-10-25 03:02:40)
- Log: `logs/baseline-20261025-030240.txt`. Màn hình chạy trên `.Display_boot` 1080p, dGPU tắt.

### Pha 7 — Stage 1 Run (2026-10-25 03:06:50)
- Log: `logs/stage1-20261025-030650.log`. Results: `0x00000001` (PASS). `vmap selftest 0`.

### Pha 7 — Stage 2 Run (2026-10-25 03:11:01)
- Log: `logs/stage2-20261025-031101.log`. Results: `[Stage 1: 1, Stage 2: 1]` (PASS).
- `XeGfxProbe` đọc trọn vẹn thông số iGPU: `8086:9A49`, revision 12, BAR0 16MB, BAR2 256MB, Pipe A lit, 1080p framebuffer.

### Pha 7 — Stage 3 Run (2026-10-25 03:13:02)
- Log: `logs/stage3-20261025-031302.log`. Results: `[Stage 1: 1, Stage 2: 1, Stage 3: 1]` (PASS).
- Newbus & DMA khởi tạo chính xác: `hostb0` (`8086:4649`), `vgapci0` (`8086:9a49`), `drmn0`.

### Pha 7 — Stage 4 Run & Phân Tích Kernel Panic (2026-10-25 03:23:17)
- Log: `logs/Kernel-2026-10-25-032317.panic`.
- **Hiện tượng:** Máy mất phản hồi khi kích hoạt `sysctl debug.xegfx_stage=4` do kernel trap.
- **Loại Panic:** `Kernel trap at 0xffffff7faeffcad5, type = 14=page fault, CR2: 0x0000000000000000`.
- **Dấu vết Backtrace:**
  - `_xegfx_stage_sysctl` $\rightarrow$ `_xg_start_stage(4)` $\rightarrow$ `_i915kms_evh`
  - $\rightarrow$ `_i915_driver_probe` (i915 bắt đầu probe phần cứng GPU)
  - $\rightarrow$ `_intel_detect_pch` (tìm kiếm chipset PCH để nhận diện nền tảng)
  - $\rightarrow$ `_lkpi_pci_get_class` (LinuxKPI tìm thiết bị ISA/LPC bridge `8086:5182`)
  - $\rightarrow$ `_kobject_init_and_add` $\rightarrow$ `_kobject_set_name_vargs`
  - $\rightarrow$ `_xg_vsnprintf + 0x45` (CR2 = 0x0; dereference NULL format string trong `xg_has_pext`).
- **Nguyên nhân kỹ thuật cốt lõi:**
  1. Trong hàm `intel_detect_pch`, driver i915 gọi `pci_get_class(PCI_CLASS_BRIDGE_ISA << 8, NULL)` để quét chipset Alder Lake PCH (`8086:5182`).
  2. LinuxKPI cố gắng đăng ký kobject cho thiết bị này và gọi hàm định dạng chuỗi `xg_vsnprintf` với con trỏ định dạng chuỗi `fmt = NULL`.
  3. Hàm `xg_has_pext(fmt)` trong `shim/src/xnu/xg_kext.cpp` duyệt chuỗi bằng vòng lặp `for (; *f; f++)` mà không kiểm tra điều kiện `f != nullptr`, dẫn đến truy cập vào địa chỉ 0x0 gây ra kernel panic ngay lập tức.
- **Phục hồi an toàn:** Kext XeGfx không nạp lúc boot nên khi khởi động lại, máy trở về giao diện macOS bình thường, không tổn hại hệ điều hành hay phân vùng đĩa.