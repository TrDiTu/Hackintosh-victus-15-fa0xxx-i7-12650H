# AGENTS.md — Dự án EFI OpenCore cho laptop (macOS 26 Tahoe)

Đọc file này và `docs/STATE.md` ở đầu MỖI phiên làm việc, trước khi làm bất cứ việc gì.

## 1. Hai máy khác nhau (quan trọng)
- Codex chạy trên MÁY A (máy này). Laptop đích (MÁY B) là máy khác. Codex không truy cập được máy B.
- Tuyệt đối không dùng lệnh nhận diện phần cứng trên máy A để suy ra cấu hình máy B.
- Nguồn dữ liệu phần cứng duy nhất: `laptop-specs.md` và các file trong `docs/hw-dump/`
  (do người dùng dump trên máy B rồi chép vào). Thiếu dữ liệu → liệt kê rõ và hỏi, không đoán.
- Mọi lệnh cần chạy trên máy B (dump phần cứng, dump DSDT, test EFI, build/chạy XeGfx trên macOS)
  chỉ được VIẾT thành hướng dẫn/script cho người dùng tự chạy.
- Vòng làm việc: Codex viết EFI → người dùng ghi lên USB → test trên máy B → người dùng mang log về.

## 2. Phạm vi ghi/xoá (BẮT BUỘC)
- ĐƯỢC GHI/TẠO/XOÁ: chỉ trong thư mục workspace và ổ USB `G:\`.
- MỌI vị trí khác (C:\, Documents, Downloads, AppData, ổ khác...): CHỈ ĐỌC.
  Không ghi, xoá, đổi tên, hay cài phần mềm ra ngoài.
- File tải về, repo clone → `_cache/`; công cụ portable → `tools/`. Không chạy installer ghi ra ngoài workspace.
- Trên `G:\`: chỉ ghi trong `G:\EFI` (và `G:\XeGfx-test` nếu người dùng yêu cầu). Không format,
  repartition, hay chạy lệnh đĩa (diskpart, format, Clear-Disk...).
- Mọi thao tác ghi lên `G:\` đi qua skill `usb-deploy-guard`. Không tự `robocopy`/`Copy-Item` lên `G:\`.
- Cần ghi ngoài phạm vi: DỪNG và hỏi, không tìm đường vòng.

## 3. Snapshot theo BẢN BUILD (tối đa 3)
- "Một bản build" = một EFI hoàn chỉnh đã qua `efi-validate` không lỗi. Snapshot tạo MỘT LẦN khi build
  xong (skill `efi-snapshot`), KHÔNG tạo cho từng lần thêm/sửa driver nhỏ lẻ.
- Trong lúc dựng dở, sửa tự do trên `EFI/` của workspace, nhưng ghi mọi quyết định vào `docs/BUILD-LOG.md`.
- Tối đa 3 snapshot trong `snapshots/`. Tạo cái thứ 4 → xoá cái cũ nhất, chỉ trong `snapshots/`.
  Bản có `known-good: true` trong manifest thì KHÔNG tự xoá: dừng và hỏi.
- Chỉ người dùng mới được yêu cầu đánh dấu `known-good`.

## 4. Nguồn tham khảo & kiểm định driver
- Nguồn nền: các dự án trong README của https://github.com/watchthelight-labs/XeGfx và tài liệu
  trong chính repo đó. Được tìm rộng thêm (chỉ đọc) trên web/GitHub để tìm driver cho từng thiết bị.
- Một driver chỉ vào EFI khi đã qua skill `driver-vetting` VÀ người dùng duyệt trong `docs/DRIVER-MATRIX.md`.
  Binary chỉ lấy từ release chính thức; ghi URL, phiên bản, SHA256 vào `docs/SOURCES.md`.
- Dự án "chỉ học hỏi": lấy ý tưởng/kết luận, không chép code. Tôn trọng license.
- Không bịa PCI ID, HID, patch, boot-arg hay kết quả test. Không chắc → ghi "CHƯA XÁC MINH".

## 5. An toàn
- Không đưa SMBIOS serial/MLB/UUID thật vào log, manifest, repo hay câu trả lời. Dùng placeholder
  `CHANGE_ME_*` và nhắc người dùng tự sinh bằng macserial.
- Không bật SecureBootModel/đổi SIP/NVRAM kiểu không hoàn tác mà không hỏi.
- Phân biệt: "kext đã inject" ≠ "thiết bị hoạt động" ≠ "ổn định qua sleep/wake" ≠ "Metal 3 hoạt động".
  Chỉ người dùng xác nhận sau khi test trên máy B. Không tuyên bố "hỗ trợ Metal 3" khi chưa có bằng chứng.
- Không đưa XeGfx.kext vào EFI (dự án thiết kế để KHÔNG load lúc boot).
- BIOS: không dùng chế độ chỉ-dGPU. Giữ Hybrid/iGPU điều khiển màn hình nội bộ.

## 6. Cổng chặn trước XeGfx
- KHÔNG bắt đầu Giai đoạn B (XeGfx) cho đến khi người dùng viết rõ: "EFI nền đã ổn định, bắt đầu XeGfx".
- Trong Giai đoạn B đi tuần tự stage 1 → 4, mỗi stage cần log từ người dùng trước khi đề xuất stage kế.

## 7. Bộ nhớ giữa các phiên: `docs/STATE.md`
- Cuối MỖI phiên (và sau mỗi pha) cập nhật `docs/STATE.md`: pha hiện tại, đã duyệt gì, đang chờ gì,
  quyết định quan trọng, build mới nhất, việc người dùng cần làm.
- Đầu phiên mới: đọc `docs/STATE.md`, `docs/BUILD-LOG.md`, rồi tóm tắt 3–5 dòng cho người dùng và tiếp tục.

## 8. Skills (trong `.agents/skills/`)
| Việc | Skill |
|---|---|
| Đọc/kiểm tra dữ liệu phần cứng, viết MACHINE-ANALYSIS | `hw-dump-reader` |
| Tìm & kiểm định driver, lập DRIVER-MATRIX/SOURCES | `driver-vetting` |
| Viết/biên dịch SSDT (tắt dGPU, GPIO touchpad...) | `ssdt-authoring` |
| Kiểm tra EFI trước khi snapshot hoặc ghi USB | `efi-validate` |
| Snapshot một bản build | `efi-snapshot` |
| Ghi EFI lên `G:\` | `usb-deploy-guard` |
| Phân tích log OpenCore/panic/XeGfx từ người dùng | `log-analysis` |
| Runbook thử XeGfx (Giai đoạn B) | `xegfx-runbook` |
Script chạy từ thư mục gốc workspace. Chạy `-WhatIf` hoặc chế độ thử trước khi chạy thật nếu skill có.

## 9. Cách làm việc
- Làm từng bước nhỏ, báo cáo ngắn. Dừng ở các điểm chờ duyệt đã nêu trong prompt (đặc biệt DRIVER-MATRIX
  và trước khi ghi USB).
- Thiếu thông tin trong `laptop-specs.md` → hỏi, không đoán.
