---
name: driver-vetting
description: Find and vet macOS drivers/kexts/SSDTs/patches for EVERY device of the target laptop (by real Hardware ID) and record them in docs/DRIVER-MATRIX.md and docs/SOURCES.md. Use when choosing any kext, adding a driver to the EFI, when the user says "tìm driver", "kext", "itlwm", "HeliPort", "VoodooI2C", "touchpad", "audio", "Bluetooth", "driver matrix", or when a device does not work. Enforces official-source, license and macOS 26 Tahoe evidence checks.
---

# driver-vetting

Mục tiêu: tìm driver cho TẤT CẢ thiết bị, nhưng chỉ cho vào EFI những driver đủ bằng chứng và được người dùng duyệt.

## Đầu vào
`docs/MACHINE-ANALYSIS.md` (từ `hw-dump-reader`). Làm việc theo Hardware ID thực của máy đích,
không áp cấu hình mẫu của máy khác.

## Quy trình cho MỖI thiết bị
1. Ghi thiết bị + Hardware ID (VEN/DEV/SUBSYS hoặc ACPI ID).
2. Tìm ứng viên (chỉ đọc): repo chính thức của kext, tài liệu OpenCore/Dortania, các dự án trong README của XeGfx,
   issue tracker, báo cáo người dùng trên máy tương tự. Ghi nhiều ứng viên nếu có.
3. Kiểm định từng ứng viên theo checklist ở dưới.
4. Quyết định một trong: `DÙNG` / `ỨNG VIÊN` (chưa đủ chứng cứ) / `KHÔNG CÓ DRIVER` / `KHÔNG CẦN` / `BỎ QUA`.
5. Ghi vào `docs/DRIVER-MATRIX.md` (mẫu: `references/DRIVER-MATRIX.template.md`) và binary vào `docs/SOURCES.md`.

## Checklist kiểm định (tất cả phải đạt mới được `DÙNG`)
- [ ] **Nguồn chính thức:** repo/release của chính tác giả. Không repack, không link tải lạ, không file ẩn danh.
- [ ] **License rõ ràng** và tương thích với việc dùng cá nhân; ghi loại license.
- [ ] **Tương thích macOS 26 Tahoe có bằng chứng** (release notes, issue, báo cáo kèm link). Chỉ có bằng chứng cho
      macOS đời cũ → `CHƯA XÁC MINH TAHOE`, trạng thái tối đa là `ỨNG VIÊN`.
- [ ] **Khớp phần cứng:** Hardware ID của máy nằm trong danh sách hỗ trợ (hoặc có bằng chứng chạy trên chip tương đương).
- [ ] **Phiên bản cụ thể** + SHA256 của file đã tải.
- [ ] **Hạn chế đã biết** ghi rõ (tính năng không dùng được, lỗi sleep/wake...).
- [ ] **Phụ thuộc & thứ tự nạp** (Lilu, VirtualSMC, VoodooI2C trước VoodooI2CHID...).
- [ ] **Người dùng đã duyệt** dòng đó trong DRIVER-MATRIX.

## Lưu ý theo nhóm (gợi ý để xác minh, KHÔNG phải sự thật mặc định)
- **Wi-Fi Intel → itlwm + HeliPort:** kiểm tra model có trong danh sách hỗ trợ của itlwm. Nó hiện ra như card
  Ethernet nên AirDrop/Handoff/Continuity không dùng được. Intel Wi-Fi không chạy trong Recovery → cần bộ cài
  macOS offline; HeliPort phải được mang vào máy sau khi cài (lúc đó chưa có mạng). Phương án dự phòng:
  USB Wi-Fi/tethering.
- **Touchpad:** I2C-HID → VoodooI2C + VoodooI2CHID (có thể cần SSDT/GPIO, polling hay interrupt); PS/2 →
  VoodooPS2. Bàn phím có thể khác giao tiếp với touchpad. Dùng DSDT thật (`ssdt-authoring`).
- **Bluetooth:** thường là USB; cần firmware/fixup phù hợp. Kiểm tra bằng chứng riêng cho Tahoe.
- **Audio:** codec + layout; cần bằng chứng cho đúng codec.
- **USB:** cần map cổng; ghi kế hoạch map (người dùng chạy công cụ trên máy đích).
- **NVMe, EC/pin, quạt/nhiệt, card reader, camera, vân tay, ALS:** xét từng cái; nếu không có driver → ghi
  `KHÔNG CÓ DRIVER` rõ ràng thay vì bỏ trống.
- **dGPU không có driver:** quyết định `BỎ QUA/VÔ HIỆU HOÁ`, phương án theo `GPU-STRATEGY.md`.
- **Nhóm nền:** Lilu, VirtualSMC, WhateverGreen và các plugin cần thiết.

## Kết thúc
- Trình toàn bộ DRIVER-MATRIX cho người dùng, kèm 5 rủi ro lớn nhất, và DỪNG chờ duyệt.
- Không đưa kext chưa `DÙNG` vào `EFI/`. Ứng viên thì chỉ ghi vào bảng.
- Cập nhật `docs/STATE.md`.

## Không làm
- Không bịa Hardware ID, tên kext, phiên bản hay bằng chứng tương thích. Không chắc → `CHƯA XÁC MINH`.
- Không tải binary từ nguồn không chính thức. Không chép code từ dự án chỉ dành cho "học hỏi".
