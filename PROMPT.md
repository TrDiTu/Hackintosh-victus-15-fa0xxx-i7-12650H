Bạn đang làm việc trong workspace của tôi. Đọc `AGENTS.md` và `docs/STATE.md` trước, tuân thủ nghiêm
mọi quy tắc trong đó (hai máy khác nhau, chỉ ghi trong workspace và G:\, snapshot theo bản build tối đa 3,
dùng các skill trong `.agents/skills/`).

## Mục tiêu
Xây dựng EFI OpenCore cho laptop của tôi (MÁY B, mô tả trong `laptop-specs.md`),
target macOS 26 Tahoe, theo hai giai đoạn:

**Giai đoạn A: EFI nền hoàn chỉnh (không có XeGfx).** Tìm driver cho TẤT CẢ thiết bị trên máy,
dựng EFI boot ổn định, để mọi thiết bị hoạt động tới mức tối đa mà cộng đồng đã chứng minh được trên Tahoe.
Bắt buộc có: Wi-Fi bằng itlwm + HeliPort, touchpad/bàn phím hoạt động.

**Giai đoạn B: Thử nghiệm XeGfx** (chỉ sau khi tôi xác nhận Giai đoạn A ổn định).
Mục tiêu dài hạn: Metal 3 trên iGPU Intel Xe.

## Bối cảnh bắt buộc phải đọc
1. `laptop-specs.md`. (Có sẵn)
2. https://github.com/watchthelight-labs/XeGfx — README, `docs/HOW-IT-WORKS.md`, `CONTRIBUTING.md`, các issue
   đang mở. Ghi nhớ: XeGfx là WIP và CHƯA điều khiển được GPU; kext KHÔNG load lúc boot (cài vào
   auxiliary kernel collection, `kmutil load`, chạy từng stage qua `debug.xegfx_stage`); khuyến nghị BIOS
   Hybrid; build phải làm trên macOS (Codex chỉ viết hướng dẫn). Mốc test phần cứng duy nhất của dự án là
   Lenovo Legion 5 15IAX10 (Arrow Lake-HX) trên Tahoe 26.7.1.
3. Các dự án trong README XeGfx liên quan đến đời iGPU của tôi (WhateverXe, NootedGreen,
   JulioNectar/Hackintosh-XPS13Plus-IrisXe-Tahoe, IntelIGPU-Tahoe, VedCloud/Meteor-Lake..., nmx-intel,
   LunarBridge, WhateverGreen, OpenCorePkg).
4. OpenCore Install Guide (Dortania) và Configuration.pdf đúng phiên bản OpenCore sẽ dùng.

## Quy trình (dừng và báo cáo sau mỗi pha; cập nhật `docs/STATE.md` sau mỗi pha)

### GIAI ĐOẠN A

**Pha 0 — Kiểm kê phần cứng** (skill `hw-dump-reader`)
- Nếu `docs/hw-dump/` chưa có hoặc thiếu: hướng dẫn tôi chạy `tools/dump-laptop.ps1` trên MÁY B, và hướng
  dẫn dump DSDT/SSDT khi cần. DỪNG chờ dữ liệu. KHÔNG dump phần cứng của máy đang chạy Codex.
- Khi đủ dữ liệu: lập danh sách MỌI thiết bị kèm Hardware ID (CPU/chipset, iGPU, dGPU, màn hình, Wi-Fi,
  Bluetooth, Ethernet, audio codec, mic, touchpad, bàn phím/phím Fn, SSD/NVMe, card reader, camera, vân tay,
  USB/Type-C/Thunderbolt, EC/pin, quạt/sensor, TPM, ALS/accelerometer, I2C/GPIO) + BIOS options liên quan
  (CFG Lock, VT-d, Above 4G, chế độ GPU, DVMT, Secure Boot). Ghi vào `docs/MACHINE-ANALYSIS.md`.
- Liệt kê thông tin còn thiếu và hỏi tôi.

**Pha 1 — Tìm driver cho TẤT CẢ thiết bị** (skill `driver-vetting`)
- Tìm rộng mọi driver/kext/SSDT/patch khả thi cho từng thiết bị theo Hardware ID thực của máy tôi.
- Lập `docs/DRIVER-MATRIX.md` và `docs/SOURCES.md` theo mẫu trong skill. Gợi ý nhóm cần xét (phải xác minh
  từng cái, không mặc định): Wi-Fi (itlwm + HeliPort), Bluetooth, touchpad/bàn phím, audio, Ethernet,
  card reader, NVMe, USB map, EC/pin, nhiệt/quạt, phím độ sáng/Fn, power management, sleep/wake, camera,
  nhóm kext nền (Lilu, VirtualSMC, WhateverGreen...).
- Ghi chú trung thực cho tôi: Intel Wi-Fi không chạy trong Recovery nên cần bộ cài macOS offline; itlwm hiện
  ra như card Ethernet (không AirDrop/Handoff/Continuity); nêu cách mang HeliPort vào máy sau khi cài.
- DỪNG, trình bảng cho tôi duyệt. Không dựng EFI trước khi tôi duyệt.

**Pha 2 — Chiến lược GPU** (`docs/GPU-STRATEGY.md`; dùng `ssdt-authoring` nếu cần SSDT)
- Đời iGPU của tôi có trong danh sách mục tiêu XeGfx không, đang ở mốc nào.
- So sánh các hướng cho EFI nền (có nguồn, xét riêng Tahoe): (a) tận dụng driver Apple kiểu WhateverXe/
  NootedGreen, (c) framebuffer an toàn không tăng tốc làm đường lui; ghi chú hướng (b) XeGfx + NvGfx dành
  cho Giai đoạn B. Kết luận trung thực: Metal 3 hiện có đạt được trên máy tôi không, cần gì để đạt.
- **dGPU:** xác định model và có driver Tahoe không (kèm nguồn). Không có driver → vô hiệu hoá theo thứ tự:
  (1) tuỳ chọn BIOS (không dùng chế độ chỉ-dGPU), (2) SSDT tắt nguồn dGPU viết từ DSDT thật của máy tôi,
  (3) WhateverGreen `disable-gpu`/`-wegnoegpu` làm lớp dự phòng. Báo tôi nếu cổng HDMI/USB-C/DP đi qua dGPU.
- Cấu hình phải giữ iGPU điều khiển màn hình nội bộ và ở trạng thái XeGfx stage 2 (đọc-chỉ) còn đọc được.

**Pha 3 — Dựng EFI nền**
- Tạo `EFI/{BOOT,OC}` với OpenCore ổn định mới nhất hỗ trợ Tahoe (xác minh bằng release notes).
- SMBIOS được Tahoe hỗ trợ, hợp CPU của tôi, chỉ placeholder. Chỉ thêm driver đã được tôi duyệt (DÙNG).
- Cấu hình ban đầu ưu tiên an toàn: debug target bật, SecureBootModel Disabled, không patch ngoài danh sách
  đã dẫn nguồn.
- Chạy skill `efi-validate`, sửa mọi lỗi/cảnh báo. Khi EFI hoàn chỉnh: báo cáo, rồi tạo `build-01` bằng
  `efi-snapshot`. Không snapshot từng bước nhỏ.

**Pha 4 — Kế hoạch test** (`docs/TEST-PLAN.md`)
- Thứ tự: boot installer → cài macOS (bộ cài offline) → từng nhóm thiết bị trong DRIVER-MATRIX
  (pass/fail riêng) → sleep/wake → khởi động lại nhiều lần. Kèm cách thu log và cách quay về snapshot.
- Mục "sẵn sàng cho XeGfx": ghi lại `ioreg`/PCI của iGPU và trạng thái màn hình làm mốc so sánh.
- Rà soát config.plist theo checklist (ACPI, Booter, DeviceProperties, Kernel, Misc, NVRAM, PlatformInfo, UEFI).

**Pha 5 — Triển khai USB (CHỈ khi tôi xác nhận)** (skill `usb-deploy-guard`)
- Chạy chế độ thử trước, hiển thị thông tin USB cho tôi, chờ xác nhận rồi mới ghi thật.
- Sau đó lặp: tôi test trên MÁY B → gửi log → bạn phân tích (`log-analysis`) và sửa EFI. Tạo build mới
  (`build-02`, `build-03`...) khi một vòng sửa kết thúc bằng EFI hoàn chỉnh qua `efi-validate`;
  MANIFEST ghi lỗi nào của build trước được xử lý.

### CỔNG CHẶN
Dừng hoàn toàn. Chỉ sang Giai đoạn B khi tôi viết: "EFI nền đã ổn định, bắt đầu XeGfx". Khi đó tóm tắt
thiết bị nào còn lỗi và rủi ro khi thêm XeGfx.

### GIAI ĐOẠN B — XeGfx (skill `xegfx-runbook`, `log-analysis`)
- **Pha 6:** đọc lại tài liệu và issue mới nhất của XeGfx (trạng thái có thể đã đổi), viết
  `docs/XEGFX-RUNBOOK.md` và script trong `xegfx-test/`. Nếu XeGfx đòi thay đổi EFI: thay đổi tối thiểu,
  validate, báo lý do, tạo build mới.
- **Pha 7:** tôi chạy từng stage trên macOS và gửi log; bạn phân tích, kết luận, rồi mới đề xuất stage kế.
  Ghi `docs/XEGFX-PROGRESS.md`. Nếu thất bại: đối chiếu issue/tài liệu, đề xuất tinh chỉnh
  `debug.xegfx_env`, hoặc soạn sẵn nội dung báo cáo issue (không tự gửi).
- Không tuyên bố Metal 3 hoạt động trừ khi log và test của tôi chứng minh ở mức X5/X6 trở lên.

## Đầu ra mong đợi
`EFI/`, `G:\EFI` (sau khi tôi duyệt), `docs/` (STATE, MACHINE-ANALYSIS, DRIVER-MATRIX, GPU-STRATEGY, SOURCES,
TEST-PLAN, BUILD-LOG, và ở Giai đoạn B: XEGFX-RUNBOOK, XEGFX-PROGRESS), `snapshots/` (tối đa 3),
`xegfx-test/`. Báo cáo cuối mỗi giai đoạn: đã làm gì, chưa xác minh gì, rủi ro, việc tôi cần tự làm.

## Điều cấm
- Khẳng định thiết bị/Metal 3 hoạt động khi chưa có bằng chứng thật từ máy tôi.
- Ghi ngoài workspace và G:\; ghi lên G:\ mà không qua `usb-deploy-guard`.
- Đưa driver chưa được duyệt hoặc binary nguồn không chính thức vào EFI.
- Bịa thông số; thiếu thì ghi "CHƯA XÁC MINH".
- Bắt đầu Giai đoạn B khi chưa có xác nhận của tôi; đưa XeGfx.kext vào EFI.

Bắt đầu: đọc AGENTS.md và docs/STATE.md, rồi làm Pha 0 và dừng báo cáo cho tôi.
