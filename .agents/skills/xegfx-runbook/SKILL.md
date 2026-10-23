---
name: xegfx-runbook
description: Prepare the staged XeGfx test runbook (Phase B) for the user to run on the macOS laptop - build from the NvGfx xe branch, install the kext, run stages 1-4 via debug.xegfx_stage, collect logs, roll back. Use ONLY after the user has written that the base EFI is stable and XeGfx may start ("EFI nền đã ổn định, bắt đầu XeGfx"), or when the user asks about XeGfx, Metal 3 on the Xe iGPU, kmutil load, debug.xegfx_stage, X1-X7 milestones.
---

# xegfx-runbook

## Cổng chặn
Không dùng skill này (kể cả viết runbook) cho đến khi người dùng viết rõ: "EFI nền đã ổn định, bắt đầu XeGfx".
Trước đó chỉ được trả lời câu hỏi chung về XeGfx.

## Nguyên tắc
- Codex KHÔNG chạy được bất kỳ lệnh nào trên macOS/MÁY B. Chỉ VIẾT runbook/script, người dùng chạy,
  Codex phân tích log (`log-analysis`).
- XeGfx là WIP; trạng thái thay đổi nhanh. LUÔN đọc lại README, `docs/`, `CONTRIBUTING.md` và issue đang mở của
  https://github.com/watchthelight-labs/XeGfx trước khi viết runbook, và ghi ngày đọc + commit vào runbook.
  Không dựa vào trí nhớ về lệnh/tham số; chép đúng từ tài liệu mới nhất.
- Không đưa XeGfx.kext vào EFI: kext được thiết kế KHÔNG load lúc boot.

## Điểm cốt lõi đã biết từ README (xác minh lại với bản mới nhất)
- Mốc: X1 compiles · X2 links · X3 loads · X4 GT up · X5 ANV · X6 desktop · X7 others. Tại thời điểm viết kit
  này dự án mới tới X3 (đang chờ test phần cứng) và CHƯA điều khiển được GPU; chỉ một máy test được ghi nhận.
- Cơ chế an toàn: personality chỉ khớp sau khi `kmutil load -b org.watchthelight.XeGfx`; chạy từng stage qua
  `sysctl debug.xegfx_stage` (1 shim state; 2 đọc-chỉ GPU và xuất `XeGfxProbe`; 3 newbus/DMA; 4 init drm/i915 với
  display i915 tắt, rồi kiểm tra panel còn scan-out); watchdog `debug.xegfx_wdog` panic chủ ý khi treo;
  `debug.xegfx_log`, `debug.xegfx_results`, `debug.xegfx_env` để thu log và đặt tunable.
- Build: trên macOS (Xcode Command Line Tools, Python 3, sparse clone ở `~/src/xe-src`: linux, freebsd, drm-kmod,
  linux-firmware), khuyến nghị build từ NvGfx branch `xe` (`build/nvgfx/build_xegfx.sh`). Cài vào auxiliary kernel
  collection bằng `sudo tools/install.sh` (gỡ bằng `XEGFX_MODE=uninstall`).
- Khuyến nghị: BIOS chế độ Hybrid để iGPU điều khiển màn hình.

## Nội dung `docs/XEGFX-RUNBOOK.md` (viết theo tài liệu mới nhất)
1. **Tiền điều kiện:** EFI nền ổn định (`known-good` đã đánh dấu), bản sao lưu dữ liệu, BIOS Hybrid, phiên bản
   macOS Tahoe và SIP/secure boot theo yêu cầu của tài liệu (không đoán), cách thu mốc "trước XeGfx"
   (`ioreg`, ảnh chụp trạng thái màn hình).
2. **Build** trên macOS; kiểm tra kết quả build (các bước check KPI/shadow/kcabi mà script báo).
3. **Cài kext** và xác minh đã cài mà CHƯA load.
4. **Stage 1 → 4**, mỗi stage: lệnh chính xác từ tài liệu, thời gian chờ, tiêu chí pass/fail, lệnh thu log
   (`debug.xegfx_log`, `debug.xegfx_results`, registry `XeGfxProbe`), hành động khi panic/treo
   (máy khởi động lại vào hệ thống không load XeGfx; lưu panic report).
5. **Gỡ/rollback:** gỡ kext, quay về EFI `known-good` bằng snapshot.
6. **Mẫu gửi log** cho Codex (những gì cần dán, che serial/UUID).

## Thay đổi EFI cho XeGfx
Chỉ khi tài liệu XeGfx đòi hỏi (boot-args, DeviceProperties, SSDT) mà EFI nền chưa có: thay đổi tối thiểu, ghi lý do
và nguồn, `efi-validate`, rồi `efi-snapshot` thành build mới. Không sửa trực tiếp bản `known-good`.

## Vòng lặp
Người dùng chạy một stage → gửi log → Codex phân tích → kết luận → mới đề xuất stage kế. Không nhảy stage.
Ghi tiến độ vào `docs/XEGFX-PROGRESS.md` và `docs/STATE.md`.

## Tuyên bố trung thực
- Không nói "Metal 3 hoạt động" nếu chưa có log và test của người dùng chứng minh ở mức X5/X6 trở lên.
- Không hứa thời điểm XeGfx đạt Metal 3. Có thể đề xuất báo issue/đóng góp test cho dự án (soạn sẵn, người dùng gửi).
