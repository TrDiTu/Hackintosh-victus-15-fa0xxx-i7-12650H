# DEFERRED — các phần đang tạm bỏ qua (người dùng: "sẽ quay lại sau")

Lập 2026-11-02, sau build-10. Mỗi mục: trạng thái, vì sao chưa làm, việc cần làm khi quay lại, tài liệu/bằng chứng.

| # | Hạng mục | Trạng thái hiện tại | Việc cần làm khi quay lại | Tham chiếu |
|---|---|---|---|---|
| D1 | ~~**Audio ALC245**~~ XONG build-31 (layout 11 + root patch Modern Audio) (`10EC0245`, subsys `103C8A4F`) | Không có driver trong EFI (người dùng bỏ qua). Tahoe đã gỡ AppleHDA | AppleALC 1.9.8 + `layout-id` thử 11 → 12 → 13; root patch **Modern Audio / AppleHDA** của OCLP-CustoMac (cần KDK đúng 25G241). Máy đã có root patch Wi-Fi → Revert → khởi động lại → patch lại Wi-Fi + Audio. Không dùng SimpleHDA (không license, chứa binary Apple) | DRIVER-MATRIX #14/#15; POSTINSTALL-RUNBOOK §5 |
| D2 | ~~**Bluetooth AX210**~~ XONG build-27 (`8087:0032`) | Không có driver (bỏ qua). Cổng BT đã có trong USB map (HS05, port 7, Internal 255) | IntelBluetoothFirmware + IntelBTPatcher **fork lshbluesky 2.5.2** (upstream 2.4.0 lỗi trên Tahoe, issue #505/#513) + BlueToolFixup 2.7.2 + NVRAM `bluetoothExternalDongleFailed`=00, `bluetoothInternalControllerInfo`=14×00 + `-btlfxallowanyaddr`; cold boot | DRIVER-MATRIX #8; POSTINSTALL-RUNBOOK §6 |
| D3 | **USB 3 (cổng SS)** | UTBMap chỉ có 5 cổng HS (map trên macOS không ghép được companion) → thiết bị USB 3 chạy tốc độ USB 2. PCH xHCI có 4 cổng SS (lsusb: Bus 004, 4p 10 Gb/s) | Map lại bằng USBToolBox **Windows.exe 0.2** trên Windows/WinPE (ghép companion), giữ HS04/HS05 = 255 | POSTINSTALL-RUNBOOK §2; BUILD-LOG build-10 |
| D4 | **Controller USB Thunderbolt 4** (`8086:461E`) | Không có trong map; chưa kiểm cổng USB-C/TB nào thuộc controller này | Xác định khi map lại trên Windows | MACHINE-ANALYSIS §2 |
| D5 | **Sleep/wake** | Chưa kiểm | Thử theo POSTINSTALL-RUNBOOK §3, gửi `pmset -g log`. Giai đoạn B dự kiến không có sleep | POSTINSTALL-RUNBOOK §3 |
| D6 | **Boot không cần USB** | Chưa làm (OpenCore chạy từ USB MACEFI) | Chép EFI sang ESP ổ trong, thêm mục boot BIOS HP; cẩn thận `EFI/Microsoft` | POSTINSTALL-RUNBOOK §4 |
| D7 | **Touchpad ngắt GPIO** | Đang chạy bằng polling (`-vi2c-force-polling`) — hoạt động | Tuỳ chọn: bỏ cờ polling để thử ngắt GPIO (fork lzhoang2801 có INTC1055; SSDT-XOSI đã có) — tiết kiệm pin hơn | BUILD-LOG build-01; DRIVER-MATRIX #11 |
| D8 | **AppleVTD** (`DisableIoMapper=false`) | Đang `true` (conventional, baseline OCLP-CustoMac). Build-07 thử `false`: Wi-Fi không thấy mạng (lúc đó chưa root patch) → chưa kết luận | Chỉ thử lại nếu cần; RTL8111 2.4.2 không hỗ trợ AppleVTD → phải đổi driver Ethernet trước | BUILD-LOG build-07/08 |
| D9 | **Card reader RTS5228** | KHÔNG CÓ DRIVER (RealtekCardReader: "Not Yet") | Theo dõi 0xFireWolf/RealtekCardReader | DRIVER-MATRIX #19 |
| D10 | **HDMI / màn hình ngoài** | Không dùng được (HDMI nối dGPU; dGPU tắt) | Không có hướng giải quyết trong macOS | GPU-STRATEGY §1 |
| D11 | **Độ sáng, pin dài hạn, nhiệt** | Người dùng báo pin hoạt động; chưa đo dài hạn | Kiểm theo POSTINSTALL-RUNBOOK §3 | — |
| D12 | **Công cụ**: `plist_edit.py` guard ROM (đã sửa); `snapshot.py` không bỏ qua known-good khi xoay vòng | Người dùng chọn xoá snapshot thủ công khi cần | Có thể sửa snapshot.py để xoay vòng bỏ qua known-good (cần người dùng đồng ý) | BUILD-LOG |
| D13 | ~~**Camera HP Wide Vision HD**~~ (`30C9:0069`, UVC) | **XONG** — người dùng báo hoạt động trên build-31 (2026-11-05 21:29); không đổi EFI riêng cho camera. Build-10 từng báo không chạy: nguyên nhân khác biệt CHƯA XÁC MINH (cổng HS04 port 6 = Internal 255 có trong UTBMap từ build-10) | — | BUILD-LOG |
| D14 | **Tai nghe 3,5 mm chỉ kênh trái** (layout 11, build-31) | Người dùng nghi tiếp xúc jack/tai nghe, chấp nhận bỏ qua (2026-11-05) | Thử cùng tai nghe trên thiết bị khác hoặc Linux/Windows trên MÁY B: nếu cũng lệch → phần cứng; nếu đủ 2 bên → thử layout 12 | BUILD-LOG build-31 |
