Đọc `CLAUDE.md`, `docs/STATE.md` và `docs/REFERENCES.md` trước, tuân thủ mọi quy tắc trong đó.

## Mục tiêu
Xây dựng EFI OpenCore cho laptop của tôi (MÁY B: HP Victus 15-fa0xxx, mô tả trong `laptop-specs.md` và `docs/hw-dump/`),
target macOS 26.7.1 (25G241), theo hai giai đoạn:

**Giai đoạn A — EFI nền (không tăng tốc đồ họa):** driver cho TẤT CẢ thiết bị, boot ổn định. <br>
Đề xuất: Wi-Fi bằng **kgp-macPro/AirportItlwm-Tahoe**, touchpad ELAN0788 (I2C) và bàn phím PS/2, dGPU tắt nguồn, iGPU hiển thị qua
framebuffer firmware.

**Giai đoạn B — Tăng tốc Metal cho iGPU 46A3** theo stack JulioNectar (NootedGreen + driver TGL 16.0.32), dùng
khucxtriendev và cheseecake (port 64 EU) làm tham chiếu. Mục tiêu thực tế: giao diện tăng tốc Metal. Metal 3 không nằm
trong khả năng của hướng này.

## Quy trình (dừng và báo cáo sau mỗi pha; cập nhật `docs/STATE.md`)

### GIAI ĐOẠN A
**Pha 0 — Kiểm kê** (`hw-dump-reader`)
- Thiếu `docs/hw-dump/`: hướng dẫn tôi chạy `tools/dump-laptop.sh` (Linux live USB, ưu tiên, có DSDT và dữ liệu topology
  iGPU) hoặc `tools/dump-laptop.ps1` trên MÁY B. DỪNG chờ.
- Có dữ liệu: viết `docs/MACHINE-ANALYSIS.md`, đối chiếu với R1 (repo Victus cùng board 8A4F). Chỉ ra mâu thuẫn trong
  `laptop-specs.md` (ví dụ ghi "GT2 Iris Xe" nhưng 46A3 là GT1 UHD 64 EU; Wi-Fi ghi AX211/AX210 nhưng ID 2725 là AX210).

**Pha 1 — Driver cho mọi thiết bị** (`driver-vetting`)
- Lập `docs/DRIVER-MATRIX.md` + `docs/SOURCES.md`. Xét các ứng viên đặc thù HP Victus trong REFERENCES (lỗi RTC 005,
  ECEnabler, layout-id ALC245, `-vi2c-force-polling`) như gợi ý cần kiểm chứng.
- Wi-Fi: dùng kgp-macPro/AirportItlwm-Tahoe theo yêu cầu. Đọc README + INSTALL.md mới nhất của repo, ghi phiên bản
  release đã kiểm định (không dùng bản CI/alpha), SHA-256 và UUID theo hướng dẫn của repo. Lưu ý: repo cần root patch
  "Modern Wireless" của OCLP (bản fork OCLP-CustoMac) và chọn `DisableIoMapper` theo cấu hình AppleVTD hoặc thường. Hỏi tôi
  phiên bản/cấu hình tôi đã chạy thử, rồi ghi vào DRIVER-MATRIX là "người dùng đã thử".
- Nhắc tôi: Wi-Fi chưa chạy trong Recovery/installer (root patch chỉ áp dụng sau khi cài) → cần bộ cài offline 25G241;
  Ethernet RTL8111 là đường mạng lúc cài và lúc áp root patch.
- DỪNG chờ tôi duyệt.

**Pha 2 — Chiến lược GPU cho EFI nền** (`docs/GPU-STRATEGY.md`, `ssdt-authoring`)
- dGPU: tắt nguồn bằng SSDT viết từ DSDT thật (đường dẫn PEG/PEGP xác minh trên DSDT của tôi); dự phòng `disable-gpu`
  /`-wegnoegpu`. Nêu rõ HDMI sẽ không dùng được.
- iGPU ở Giai đoạn A: không spoof, không NootedGreen, chỉ framebuffer firmware. Ghi lại kế hoạch cho Giai đoạn B nhưng
  chưa áp dụng.

**Pha 3 — Dựng EFI nền**: OpenCore ổn định mới nhất hỗ trợ Tahoe (tải bằng `release-fetch`, dựng `config.plist` từ
Sample.plist bằng `config-plist-tools`); SMBIOS placeholder (`smbios-secrets`); chỉ driver đã duyệt;
`efi-validate` sạch → báo cáo → `efi-snapshot` (`build-01`). Đặt tên config chính là `config.plist`, lưu thêm bản
`config-install.plist` giống hệt (dùng làm đường lui ở Giai đoạn B).

**Pha 4 — Kế hoạch test và cài đặt** (`docs/TEST-PLAN.md`, `macos-install-runbook`): trước tiên giải quyết cách lấy bộ cài
**đúng 25G241** từ máy Linux (DỪNG, trình lựa chọn cho tôi); rồi installer → cài macOS → từng nhóm thiết bị → khởi động
lại nhiều lần; sau cài: chặn cập nhật, serial, root patch Wi-Fi.
Thêm mục "mốc trước tăng tốc": `ioreg` iGPU, độ phân giải, `pmset -g`, thông tin stolen memory nếu đọc được.

**Pha 5 — USB** (`usb-deploy-guard`, chỉ khi tôi xác nhận; hỏi tôi đường dẫn mount của USB) → vòng lặp test/log/sửa (`log-analysis`), build mới khi
một vòng sửa xong.

### CỔNG CHẶN
Chỉ sang Giai đoạn B khi tôi viết: "EFI nền đã ổn định, bắt đầu tăng tốc đồ họa".

### GIAI ĐOẠN B (`graphics-stack-runbook`, `log-analysis`)
**Pha 6 — Chuẩn bị**: đọc lại README/CHANGELOG/docs/issues mới nhất của JulioNectar, cheseecake, khucxtriendev.
Viết `docs/GRAPHICS-PLAN.md`: chọn fork NootedGreen, topology cho 64 EU (tên boot-arg phải đọc từ đúng source của fork
đã chọn), DVMT/stolen memory, boot-args, DeviceProperties spoof, rủi ro. DỪNG chờ tôi duyệt.

**Pha 7 — Runbook và EFI tăng tốc**: viết `docs/GRAPHICS-RUNBOOK.md` cho tôi chạy trên MÁY B (`install.sh --check`,
`install.sh`, mang `NootedGreen.kext` vừa build về). Claude tạo `config.plist` tăng tốc, giữ `config-install.plist`,
validate, snapshot build mới.

**Pha 8 — Vòng test**: tôi gửi log; phân tích theo các dấu hiệu lỗi đã biết; mỗi lần đổi một tham số; ghi
`docs/GRAPHICS-PROGRESS.md`. Không tuyên bố "Metal hoạt động" khi chưa có `kmutil`, `ioreg` và kết quả test của tôi.

## Đầu ra
`EFI/`, `<usb-mount>/EFI` (sau khi duyệt), `docs/` (STATE, MACHINE-ANALYSIS, DRIVER-MATRIX, SOURCES, GPU-STRATEGY, TEST-PLAN,
BUILD-LOG, GRAPHICS-PLAN, GRAPHICS-RUNBOOK, GRAPHICS-PROGRESS), `snapshots/` (tối đa 10).

Bắt đầu: đọc các file nêu trên, tóm tắt hiện trạng, rồi làm Pha 0.
