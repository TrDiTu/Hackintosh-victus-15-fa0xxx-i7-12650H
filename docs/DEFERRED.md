# DEFERRED — các phần đang tạm bỏ qua (người dùng: "sẽ quay lại sau")

Lập 2026-11-02, sau build-10. Mỗi mục: trạng thái, vì sao chưa làm, việc cần làm khi quay lại, tài liệu/bằng chứng.

| # | Hạng mục | Trạng thái hiện tại | Việc cần làm khi quay lại | Tham chiếu |
|---|---|---|---|---|
| D1 | ~~**Audio ALC245**~~ XONG build-31 (layout 11 + root patch Modern Audio) (`10EC0245`, subsys `103C8A4F`) | Không có driver trong EFI (người dùng bỏ qua). Tahoe đã gỡ AppleHDA | AppleALC 1.9.8 + `layout-id` thử 11 → 12 → 13; root patch **Modern Audio / AppleHDA** của OCLP-CustoMac (cần KDK đúng 25G241). Máy đã có root patch Wi-Fi → Revert → khởi động lại → patch lại Wi-Fi + Audio. Không dùng SimpleHDA (không license, chứa binary Apple) | DRIVER-MATRIX #14/#15; POSTINSTALL-RUNBOOK §5 |
| D2 | ~~**Bluetooth AX210**~~ XONG build-27 (`8087:0032`) | Không có driver (bỏ qua). Cổng BT đã có trong USB map (HS05, port 7, Internal 255) | IntelBluetoothFirmware + IntelBTPatcher **fork lshbluesky 2.5.2** (upstream 2.4.0 lỗi trên Tahoe, issue #505/#513) + BlueToolFixup 2.7.2 + NVRAM `bluetoothExternalDongleFailed`=00, `bluetoothInternalControllerInfo`=14×00 + `-btlfxallowanyaddr`; cold boot | DRIVER-MATRIX #8; POSTINSTALL-RUNBOOK §6 |
| D3 | **USB 3 (cổng SS)** | **build-33**: UTBMap thêm SS01 (0x0D) + SS02 (0x0E) ghép HS01/HS02 (dữ liệu Linux `usb-map-20261105-220220.txt`) | Chờ kiểm trên macOS bằng thiết bị USB 3 thật (lần đo Linux chỉ có USB 2.0) | BUILD-LOG build-33 |
| D4 | **USB-C phần USB 3 / Thunderbolt 4** (`8086:461E`, `TXHC.SS01` adr 2, 20 Gbps) | USB-C chỉ có HS04 (USB 2) trên PCH; phần SS nằm ở controller TB4, chưa map | Cần xác minh macOS có nhận controller 461E không (`ioreg -p IOService -c AppleUSBXHCI`) rồi mới map | BUILD-LOG build-33 |
| D5 | **Sleep/wake** | Chưa kiểm | Thử theo POSTINSTALL-RUNBOOK §3, gửi `pmset -g log`. Giai đoạn B dự kiến không có sleep | POSTINSTALL-RUNBOOK §3 |
| D6 | ~~**Boot không cần USB**~~ | **XONG 2026-11-05**: `EFI/OC` (build-33) trên ESP `nvme0n1p1` cạnh Limine; Boot0001 "OpenCore" đứng đầu BootOrder. Chép từ Linux, không từ macOS | — | POSTINSTALL-RUNBOOK §4 |
| D7 | ~~**Touchpad ngắt GPIO**~~ | **XONG build-32/33** — người dùng: mượt như polling, cử chỉ bình thường (2026-11-05). Chế độ thực tế (ngắt hay VoodooI2C tự lùi polling) CHƯA XÁC MINH qua log | — | BUILD-LOG build-32 |
| D8 | **AppleVTD** (`DisableIoMapper=false`) | Đang `true` (conventional, baseline OCLP-CustoMac). Build-07 thử `false`: Wi-Fi không thấy mạng (lúc đó chưa root patch) → chưa kết luận | Chỉ thử lại nếu cần; RTL8111 2.4.2 không hỗ trợ AppleVTD → phải đổi driver Ethernet trước | BUILD-LOG build-07/08 |
| D9 | **Card reader RTS5228** | KHÔNG CÓ DRIVER (RealtekCardReader: "Not Yet") | Theo dõi 0xFireWolf/RealtekCardReader | DRIVER-MATRIX #19 |
| D10 | **HDMI / màn hình ngoài** | Không dùng được (HDMI nối dGPU; dGPU tắt) | Không có hướng giải quyết trong macOS | GPU-STRATEGY §1 |
| D11 | **Độ sáng, pin dài hạn, nhiệt** | Người dùng báo pin hoạt động; chưa đo dài hạn | Kiểm theo POSTINSTALL-RUNBOOK §3 | — |
| D12 | **Công cụ**: `plist_edit.py` guard ROM (đã sửa); `snapshot.py` không bỏ qua known-good khi xoay vòng | Người dùng chọn xoá snapshot thủ công khi cần | Có thể sửa snapshot.py để xoay vòng bỏ qua known-good (cần người dùng đồng ý) | BUILD-LOG |
| D13 | ~~**Camera HP Wide Vision HD**~~ (`30C9:0069`, UVC) | **XONG** — người dùng báo hoạt động trên build-31 (2026-11-05 21:29); không đổi EFI riêng cho camera. Build-10 từng báo không chạy: nguyên nhân khác biệt CHƯA XÁC MINH (cổng HS04 port 6 = Internal 255 có trong UTBMap từ build-10) | — | BUILD-LOG |
| D14 | ~~**Tai nghe 3,5 mm chỉ kênh trái**~~ | **Đóng — lỗi phần cứng** (cổng jack): người dùng thử trên Linux cùng máy, vẫn lệch (2026-11-05). Không liên quan layout | — | — |
