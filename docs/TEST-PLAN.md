# TEST-PLAN — kiểm tra trên MÁY B (người dùng chạy, mang kết quả về)

## Build 1 — SSDT
| SSDT | Lệnh trên macOS (MÁY B) | Kỳ vọng |
|---|---|---|
| SSDT-PLUG-ALT | `sysctl machdep.cpu.thread_count`; `ioreg -l -p IODeviceTree \| grep -m3 plugin-type` | 16 luồng; `plugin-type = 1` trên CP00 |
| SSDT-EC-USBX | `ioreg -l -p IODeviceTree \| grep -E "ACID0001\|USBX"` | Có thiết bị EC (ACID0001) và USBX |
| SSDT-AWAC | `ioreg -l \| grep -i -E "PNP0B00\|AppleRTC"` ; khởi động lại 2 lần | RTC có, không mất giờ; BIOS không báo lỗi RTC |
| SSDT-XOSI | `ioreg -l -p IODeviceTree -n TPD0` ; VoodooI2C log: `log show --last boot \| grep -i voodooi2c` | TPD0 có tài nguyên ngắt; touchpad nhận (GPIO hoặc polling) |
| SSDT-DGPU-OFF | `ioreg -l \| grep -i -A3 "PEGP"`; theo dõi nhiệt/pin (`pmset -g batt`) | dGPU không còn xuất hiện/hoạt động; máy mát hơn |
| SSDT-SBUS-MCHC | `kextstat \| grep -i smbus` | `AppleSMBusController` / `AppleSMBusPCI` đã nạp |

## Build-02 — lần boot đầu trên MÁY B (macOS 25G241 đã cài sẵn)
USB: phân vùng MACEFI (`/dev/sdb3` khi cắm ở MÁY A), EFI tree `f76a0fae1d13`, SMBIOS thật đã tiêm vào `config.plist` trên USB.

### Trước khi boot
1. Unmount/eject USB trên MÁY A rồi mới rút.
2. BIOS MÁY B: Secure Boot = Disabled (đã xác nhận). Không có Above 4G / DVMT trong BIOS. Không chọn chế độ chỉ-dGPU.
3. Chọn boot từ USB (phím F9 trên HP) → OpenCore picker → chọn ổ macOS.

### Lưu ý về cài đặt có sẵn
- EFI này để **SIP bật (`csr-active-config 00000000`) và AMFI bật**. Nếu bản macOS đang cài đã được root patch (Wi-Fi OCLP) hoặc còn kext cũ trong
  `/Library/Extensions` từ các lần thử trước, có thể: Wi-Fi không lên, hoặc boot dừng lâu. Đó là thông tin cần ghi lại, không phải lỗi EFI chắc chắn.
- Boot verbose (`-v`): nếu treo, **chụp ảnh màn hình** dòng cuối (OpenCore RELEASE với `Target 3` không ghi log ra file).

### Kiểm tra sau khi vào desktop (ghi kết quả từng dòng)
| Nhóm | Lệnh / thao tác | Kỳ vọng |
|---|---|---|
| Build | `sw_vers` ; `nvram boot-args` ; `csrutil status` | 25G241; boot-args khớp EFI |
| Kext nạp | `kmutil showloaded --list-only \| grep -v com.apple` | Lilu, VirtualSMC, VoodooI2C*, VoodooPS2*, RealtekRTL8111, AirportItlwm, USBToolBox, ECEnabler... |
| Bàn phím | gõ thử, phím Fn sáng/tối | Gõ được |
| Touchpad | di chuột, click, cuộn 2 ngón | Hoạt động (polling) |
| Ethernet | `ifconfig en0` / có IP | Có mạng |
| Wi-Fi | menu Wi-Fi, `ioreg -r -c AirportItlwm -l -w0 \| head` | Ghi lại có/không (phụ thuộc root patch + SIP) |
| dGPU tắt | `ioreg -l \| grep -i -A2 PEGP` ; `system_profiler SPDisplaysDataType` | Không thấy NVIDIA |
| iGPU | `system_profiler SPDisplaysDataType` ; độ phân giải | 1920×1080, không tăng tốc (dự kiến) |
| Pin | biểu tượng pin, `pmset -g batt` | Hiện % pin (ECEnabler + SMCBatteryManager) |
| CPU | `sysctl machdep.cpu.brand_string machdep.cpu.thread_count` | 16 luồng |
| USB | cắm USB vào từng cổng | Ghi cổng nào nhận |
| Ổn định | khởi động lại 3 lần | Lần nào cũng vào desktop |
| RTC | sau restart, BIOS có báo lỗi 005 không | Không lỗi |

### Mốc trước tăng tốc (lưu lại để so sánh ở Giai đoạn B)
```
ioreg -l -w0 -p IOService -n IGPU > ~/igpu-baseline.txt 2>&1
ioreg -l -w0 | grep -i -E "AAPL,ig-platform-id|device-id|IOFramebuffer" > ~/igpu-props.txt
system_profiler SPDisplaysDataType > ~/displays.txt
pmset -g > ~/pmset.txt ; pmset -g batt >> ~/pmset.txt
log show --last boot --predicate 'process == "kernel"' | grep -i -E "voodoo|airport|itlwm|igpu|framebuffer|panic" > ~/kernel-boot.txt
```
Mang các file này + ảnh màn hình (nếu treo) về MÁY A.
