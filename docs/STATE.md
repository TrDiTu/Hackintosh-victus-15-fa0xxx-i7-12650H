# STATE — bộ nhớ giữa các phiên (Codex cập nhật cuối mỗi phiên/pha)
## Trạng thái hiện hành — 2026-10-25 (thay thế kết luận cũ bên dưới)
- Đã mở CỔNG CHẶN Giai đoạn B (XeGfx) ngày 2026-10-25 sau khi người dùng gửi chính xác lệnh: "EFI nền đã ổn định, bắt đầu XeGfx". Bản snapshot build-10 là mốc known-good: true của EFI nền.
- Hoàn tất Pha 6 (Chuẩn bị & Runbook XeGfx): Đã đọc commit 78db6fceab4a6d50c3072c12e5ea89688f281d26 mới nhất của XeGfx (2026-10-24); tải và thẩm định release chính thức XeGfx 0.0.38 (SHA256 10fa402c966cb60f444c026fb9ec6e73c6c6467a13d2742a5e08bb6007899a87). Đã soạn docs/XEGFX-RUNBOOK.md, docs/XEGFX-PROGRESS.md và 4 helper scripts trong xegfx-test/.
- XeGfx.kext TUYỆT ĐỐI KHÔNG đưa vào EFI; EFI build-10 giữ nguyên.
- Pha 7 (Vòng lặp Stage 1 -> 4): Đang chờ người dùng chạy 00-collect-baseline.sh và 01-install-xegfx.sh trên Máy B, reboot, sau đó kích hoạt thử Stage 1 bằng 02-run-stage.sh 1 và gửi log về cho Codex.
- Người dùng xác nhận build-10 trên Máy B "đã hoạt động ổn, đủ điều kiện để chuyển sang giai đoạn tiếp theo". Touchpad ELAN0788 với bộ điều khiển Alder Lake LPSS I2C (8086:51E8) đã hoạt động qua VoodooI2C fork v3.0.0. Đang chờ làm rõ bước tiếp theo: hoàn thiện nốt âm thanh Realtek ALC245 (layout-id 11/13/21) và thu thập baseline logs trên macOS, hay mở Giai đoạn B. Cổng chặn XeGfx tiếp tục đóng theo AGENTS.md §6 cho đến khi người dùng gửi chính xác lệnh: "EFI nền đã ổn định, bắt đầu XeGfx" và xác nhận đánh dấu known-good cho build-10.

- Đã deploy build-10 lên G:\EFI ngày 2026-10-25 01:47:29 sau khi người dùng xác nhận ghi USB. usb-deploy-guard kiểm tra đúng MACEFI FAT32 2,99 GB, hash cây đích khớp workspace `2e5c3fc66324`. EFI cũ khớp snapshot build-09 nên không tạo backup trùng; giữ build-08/09/10. Chờ người dùng Safely Remove USB, boot máy B và thử touchpad (di chuyển, click/tap, cuộn hai ngón). Nếu lỗi, thu log bằng tools/collect-touchpad.sh; nếu panic, lấy báo cáo mới và quay lại build-09. Âm thanh chưa sửa; Giai đoạn B chưa mở. Các dòng chờ ghi USB phía dưới là lịch sử đã được thay thế.
- Người dùng đã duyệt thử fork VoodooI2C trên Tahoe. Workspace build-10 (`build-10-20261025-014543-touchpad-adl-driver`) thay riêng VoodooI2C/core/plugins và HID bằng release 3.0.0 của lzhoang2801. Không đổi config/ACPI/audio; IntelBTPatcher vẫn tắt. Validate 0 lỗi/0 cảnh báo, ocvalidate ran, report validate-20261025-014527.md. Snapshot hiện giữ build-08/09/10; build-09 để rollback, chưa gán known-good. USB G: MACEFI FAT32 2,99 GB đã dry-run; đang hỏi xác nhận ghi build-10 qua usb-deploy-guard. Chưa có test touchpad trên máy B; âm thanh chờ, Giai đoạn B chưa mở. Các dòng chờ duyệt driver phía dưới được thay thế.
- Người dùng báo touchpad và âm thanh chưa hoạt động, ưu tiên sửa touchpad. Kext VoodooI2C 2.9.1 hiện tại thiếu match I2C0 8086:51E8. Đã tải/kiểm tra fork lzhoang2801 release 3.0.0 (CFBundleVersion 2.9.1), có đúng I2C/GPIO ID; CHƯA XÁC MINH TAHOE. Đang hỏi duyệt ngoại lệ thử nghiệm theo AGENTS.md §4; chưa sửa EFI/USB. Xem docs/TOUCHPAD-ANALYSIS-20261025.md và tools/collect-touchpad.sh. USB vẫn build-09. Sau duyệt: thay bộ kext, validate/snapshot, deploy theo phạm vi duyệt; nếu không attach thu IORegistry trước khi sửa ACPI. Âm thanh chờ sau touchpad; Giai đoạn B chưa mở.
- Kết quả mới nhất: người dùng xác nhận "đã boot thành công rồi" sau deploy build-09. Ghi nhận boot thành công trên máy B; chưa xác nhận cụ thể Desktop/Setup Assistant, chức năng thiết bị hoặc sleep/wake. Giai đoạn A tiếp tục kiểm thử. Giữ IntelBTPatcher tắt; chưa đánh dấu snapshot known-good vì người dùng chưa yêu cầu. Bước tiếp: xác nhận màn hình hiện tại, kiểm tra touchpad, bàn phím, LAN/Wi-Fi, âm thanh và Bluetooth, sau đó restart/sleep-wake. Giai đoạn B vẫn đóng. Kết quả này thay thế các dòng chờ boot build-09 bên dưới.
- Đã deploy build-09 (IntelBTPatcher Enabled=false) lên G:\EFI lúc 2026-10-25 01:09:50 theo yêu cầu người dùng, qua usb-deploy-guard sau dry run. USB MACEFI FAT32 2.99 GB, hash cây khớp workspace `8fd1301031e6`. EFI cũ khớp snapshot build-07 nên không tạo backup trùng; vẫn giữ 3 snapshot build-07/08/09. Chờ boot Macintosh HD trên máy B: kiểm tra còn panic UVCAssistant/IOGMD hay không và có vào GUI không. Bluetooth có thể không hoạt động. Mọi dòng phía dưới nói USB vẫn là build-07/chờ deploy là lịch sử đã được thay thế.
- Cập nhật panic: đã đọc cả 5 Kernel-2026-10-24-*.panic. Cùng lỗi IOGMD not wired, task UVCAssistant, IntelBTPatcher 2.4 newHostDeviceRequest/readBytes trong backtrace. Nguồn chính thức v2.4.0 khớp đường gọi. Boot-args trong các báo cáo thuộc các biến thể cũ, không khớp chính xác build-07. Chưa kết luận nguyên nhân mọi lần treo GUI.
- Workspace mới tắt riêng IntelBTPatcher (Enabled=false); giữ file để hoàn tác, không đổi boot-args hay đồ họa. Kiểm định 0 lỗi/0 cảnh báo, ocvalidate đã chạy (validate-20261025-010833.md). Xem docs/PANIC-ANALYSIS-20261025.md. Bluetooth có thể mất chức năng; cần test máy B.
- Snapshot mới build-09 (disable-intelbtpatcher); hiện giữ build-07, build-08, build-09 sau xoay vòng build-06. USB vẫn là build-07 theo lần deploy cuối. Chờ duyệt deploy bản tắt IntelBTPatcher; chưa ghi USB trong lượt phân tích panic này. Các trạng thái cũ phía dưới chỉ là lịch sử.
- Log tiếp theo nhận sau deploy build-07: ACMTRM enrollment pending, AMFI `[non-fatal]`, AppleKeyStore session uid -1 và MACF denial cho contextstored, network interface attach/enable. Theo trình tự hội thoại đây là lần thử sau deploy; boot-args thực tế chưa được thu. Chưa có bằng chứng GUI thành công hoặc panic; bỏ -igfxvesa chưa cho thấy giải quyết triệu chứng. Bước tiếp là Recovery trên máy B: liệt kê volume và DiagnosticReports của WindowServer/loginwindow/Setup Assistant, xác định phiên bản hệ điều hành đã cài. Không sửa EFI thêm từ log này. Các dòng ghi 'chưa test' bên dưới là lịch sử trước khi nhận log này.
- Đã deploy build-07 lên G:\EFI lúc 2026-10-25 00:52:55 qua usb-deploy-guard sau chạy thử. USB MACEFI, FAT32, 2.99 GB, disk #2 bus USB. Hash cây đích khớp workspace: `b676dcb35d8d`. Chỉ cập nhật config.plist bỏ `-igfxvesa`; chờ test máy B.
- Log mới nhất người dùng gửi: `AppleKeyStoreUserClient failed MACF` lặp lại cho `contextstored`, `unexpected session uid: -1` và AMFI `[non-fatal]` cho systemkeychain/Core-Audio-Driver-Service. Chưa xác nhận build/boot-args thực tế của lần này; không gán kết quả cho build-07 vì chưa deploy trong phiên. Đoạn log không có panic hay báo cáo WindowServer; chưa xác định nguyên nhân treo. Đang chờ xác nhận USB đã cập nhật và trạng thái màn hình.
- Giai đoạn A: người dùng xác nhận hotfix AMFI vẫn dừng ở verbose hơn 5 phút, dòng cuối `set CameraAssistantBundleID: com.apple.cmio.uvcassistantextension`. CHƯA vào Setup Assistant/Desktop. Recovery từng vào GUI. Bàn phím/LAN được báo hoạt động; touchpad không hoạt động.
- Nguyên nhân treo CHƯA XÁC MINH. Rút lại các khẳng định trước về AMFI đã sửa xong, DriverKit chặn WindowServer và connector ảo gây timeout. `IOVersatile` lỗi dependency chưa được chứng minh vô hại; `GTrace` không chứng minh GUI hoạt động.
- Người dùng duyệt sửa tiếp. Workspace chỉ bỏ `-igfxvesa` để thử đối chứng với hotfix AMFI; giữ các cấu hình khác. Không áp dụng `0x9A490004`, connector/VRAM patch vì thiếu bằng chứng. Bỏ cờ này không tạo driver hỗ trợ Tiger Lake/Alder Lake hay Metal.
- Bản thử mới: `build-07-20261025-004429-no-igfxvesa-test`. Kiểm định tĩnh 0 lỗi, 0 cảnh báo, ocvalidate đã chạy; báo cáo `docs/validation/validate-20261025-004414.md`. Chưa test trên máy B.
- Snapshot hiện có: `build-06-20261025-001435-usb-before-deploy`, `build-07-20261025-004429-no-igfxvesa-test`, `build-08-20261025-005254-usb-before-deploy`. Build-08 là backup USB trước deploy, không phải bản thử mới hơn build-07. Script đã xoay vòng build-05; không đánh dấu known-good.
- Người dùng cần Safely Remove USB, cắm vào máy B, boot USB OpenCore rồi chọn Macintosh HD; báo kết quả GUI hoặc log cuối. Các log gửi trước deploy này chưa phải bằng chứng test build-07.
- Bước tiếp: test bản thử sau deploy; nếu vẫn treo, thu DiagnosticReports của WindowServer/loginwindow và phiên bản/build macOS từ Recovery trên máy B. Không tiếp tục đoán platform-id/boot-arg. Giai đoạn B vẫn đóng.

## Lịch sử trước lần test mới — các kết luận nguyên nhân/thành công đã rút lại

- Cập nhật lần cuối: 2026-10-25
- Giai đoạn / Pha hiện tại: Giai đoạn A — Đã deploy hotfix AMFI lên USB G:\ → Chờ người dùng boot kiểm thử trên MÁY B

- Đang chờ: Người dùng cắm USB vào MÁY B, boot OpenCore → chọn Macintosh HD → xác nhận có vào được Setup Assistant / Desktop

## Đã được người dùng duyệt
- Kiểm kê phần cứng Pha 0 (docs/MACHINE-ANALYSIS.md).
- Ma trận driver Pha 1 (docs/DRIVER-MATRIX.md), Chiến lược hoạ (docs/GPU-STRATEGY.md) và Nguồn (docs/SOURCES.md).
- Xác nhận: Vượt qua lỗi EXITBS:START, hiển thị màn hình eDP 1080p và boot thành công macOS GUI!
- macOS đã cài đặt xong lên phân vùng Macintosh HD (APFS) trên ổ NVMe.
- Duyệt sửa boot-arg amfi=0x80 → amfi_get_out_of_my_way=0x1 để sửa lỗi treo DriverKit/WindowServer.

## Build hiện tại trên USB
- **build-04 hotfix** (tree 17e7915b2ba7): boot-args đổi mfi=0x80 → mfi_get_out_of_my_way=0x1. Mọi thứ khác giữ nguyên.

## Snapshots hiện có (3/3)
1. uild-04-20261024-192302-build-03
2. uild-05-20261024-221513-build-04
3. uild-06-20261025-001435-usb-before-deploy

## Vấn đề đã xác định từ log MÁY B (boot lần trước, build-04 cũ)
1. **AMFI chặn DriverKit** → disallowing unsupported code signature page shift: 14, unable to create a validated cs_blob object: 85 → ĐÃ SỬA bằng mfi_get_out_of_my_way=0x1
2. **IOVersatile crash loop** → kext Apple Silicon, bình thường trên Hackintosh, không gây treo
3. **SMCProcessor: failed to find compatible processor** → Alder Lake không được nhận diện, không ảnh hưởng boot
4. **Touchpad không hoạt động** → có thể do AMFI chặn HID → cần xác minh lại sau hotfix
5. **Bàn phím hoạt động** ✅, **LAN hoạt động** ✅

## Việc người dùng cần làm
1. An toàn eject USB từ MÁY A
2. Cắm USB vào MÁY B, boot OpenCore → chọn **Macintosh HD**
3. Quan sát: verbose text chạy → chờ tối đa 5 phút → có vào Setup Assistant/Desktop không?
4. Nếu vào được: kiểm tra touchpad, Wi-Fi (HeliPort), âm thanh, pin
5. Nếu vẫn treo: chụp/ghi lại 5 dòng cuối trên màn hình, mang về cho Codex
