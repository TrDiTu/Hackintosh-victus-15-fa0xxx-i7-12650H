---
name: driver-vetting
description: Find and vet macOS drivers/kexts/SSDTs/patches for EVERY device of the target laptop (by real Hardware ID) and record them in docs/DRIVER-MATRIX.md and docs/SOURCES.md. Use when choosing any kext, adding a driver to the EFI, when the user says "tìm driver", "kext", "AirportItlwm", "Wi-Fi", "VoodooI2C", "touchpad", "audio", "Bluetooth", "driver matrix", or when a device does not work. Enforces official-source, license and macOS 26 Tahoe evidence checks.
---

# driver-vetting

Mục tiêu: tìm driver cho TẤT CẢ thiết bị, nhưng chỉ cho vào EFI những driver đủ bằng chứng và được người dùng duyệt.

## Đầu vào
`docs/MACHINE-ANALYSIS.md` (từ `hw-dump-reader`). Làm việc theo Hardware ID thực của máy đích,
không áp cấu hình mẫu của máy khác.

## Quy trình cho MỖI thiết bị
1. Ghi thiết bị + Hardware ID (VEN/DEV/SUBSYS hoặc ACPI ID).
2. Tìm ứng viên (chỉ đọc): repo chính thức của kext, tài liệu OpenCore/Dortania, các nguồn trong `docs/REFERENCES.md`,
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
- **Wi-Fi Intel AX210 → kgp-macPro/AirportItlwm-Tahoe** (người dùng chọn, đã thử và báo hoạt động ổn):
  - AX210 `8086:2725` là adapter tham chiếu duy nhất được repo kiểm định vật lý; card khác không mặc định được hỗ trợ.
  - Dùng đúng asset release (không dùng bản CI "NOT PHYSICALLY VALIDATED" hay alpha/beta), giữ nguyên tên bundle,
    executable, identifier; kiểm SHA-256 và UUID theo README/INSTALL.md của repo.
  - Repo **cần root patch OCLP** (Modern Wireless, qua fork OCLP-CustoMac) — ghi rõ vào DRIVER-MATRIX và kế hoạch cài.
    Root patch đụng tới hệ thống (SIP/AMFI, snapshot hệ thống): phải đánh giá tương tác với stack đồ họa NootedGreen ở
    Giai đoạn B trước khi áp dụng cả hai.
  - `DisableIoMapper`: `false` cho cấu hình AppleVTD, `true` cho cấu hình thường — chọn theo INSTALL.md và BIOS VT-d.
  - Bản kiểm định nêu trong README: 26.6.2 (25G83), phạm vi hẹp hơn trên 26.7 (25G229); **chưa nêu 25G241** → ghi
    "người dùng đã thử" kèm build và phiên bản người dùng cung cấp, hoặc "CHƯA XÁC MINH 25G241".
  - AirDrop/Continuity Camera/Personal Hotspot không hỗ trợ theo README. Chỉ dùng một biến thể AirportItlwm.
  - Giấy phép GPL-2.0. Không dùng itlwm/HeliPort song song.
  - Wi-Fi chưa có trong Recovery/installer → cài bằng bộ cài offline; mạng lúc cài và lúc root patch dùng Ethernet RTL8111.
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

## Nguồn tham chiếu cùng dòng máy (R1)
Với mỗi thiết bị, xem repo R1 (`docs/REFERENCES.md`) có kext/cấu hình tương ứng không, và ghi vào DRIVER-MATRIX
(cột Bằng chứng) dưới dạng mức B: "R1 dùng X trên Sequoia", kèm link file. Đó KHÔNG phải bằng chứng Tahoe và KHÔNG thay thế
checklist kiểm định: kext vẫn phải lấy từ release chính thức, có license, và có bằng chứng Tahoe riêng.

## Ứng viên riêng cho dòng HP Victus (chỉ là gợi ý, phải kiểm chứng)
Lấy từ nguồn tầng thấp (power418, T3-1) và kinh nghiệm chung, KHÔNG phải bằng chứng:
- Lỗi POST "Real-Time Clock Power Loss (005)" sau khi khởi động lại từ macOS: patch ACPI RTC + quirk `DisableRtcChecksum`.
  Xác minh bằng DSDT thật (vùng RTC) trước khi dùng.
- `ECEnabler` cho trường EC 16-bit (pin): kiểm DSDT có trường EC > 8 bit không.
- ALC245: chọn layout-id từ danh sách chính thức của AppleALC cho codec `0x10EC0245`, thử lần lượt; ghi kết quả loa/jack/mic.
- Touchpad ELAN0788: VoodooI2C + VoodooI2CHID; thử ngắt GPIO trước (cần SSDT-GPI0 theo DSDT), `-vi2c-force-polling` là dự phòng.
- Wi-Fi: kgp-macPro/AirportItlwm-Tahoe theo yêu cầu người dùng. Panic Skywalk mà khucxtriendev ghi nhận là với một bản
  AirportItlwm khác (AirportItlwm-Tahoe 2.4.0); vẫn theo dõi dấu hiệu tương tự trong log.
- Card reader RTS5288 (`10EC:5228`): khả năng cao "KHÔNG CÓ DRIVER"; xác minh trước khi kết luận.
