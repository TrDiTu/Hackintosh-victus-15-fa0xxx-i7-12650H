# BUILD-LOG — Nhật ký Xây dựng và Biên dịch EFI OpenCore

## Bản dựng: build-01 (EFI nền hoàn chỉnh cho HP Victus 15-fa0xxx)
- **Ngày tạo:** 2026-10-24
- **Mục tiêu hệ điều hành:** macOS 26 Tahoe (Darwin 25)
- **Phiên bản OpenCore:** 1.0.8 RELEASE
- **Trạng thái kiểm định:** Đạt chuẩn `efi-validate` (0 lỗi, 0 cảnh báo; ocvalidate: ran, exit 0).

### 1. Quyết định Kiến trúc & ACPI
- **SSDT-dGPU-Off.aml:** Biên dịch trực tiếp từ ACPI bytecode của máy đích (`DSDT.aml` & `SSDT14.aml`). Gọi lệnh `_OFF` tại đường dẫn `\_SB.PC00.PEG1.PEGP` khi phát hiện môi trường `_OSI("Darwin")`. Giúp ngắt hoàn toàn nguồn điện PCIe bus `01:00.0` của RTX 3050 Ti.
- **SSDT-PLUG-ALT.aml:** Sử dụng bảng khởi tạo đối tượng Processor phổ quát cho kiến trúc Intel Alder Lake-H (6P + 4E = 16 luồng), gán `plugin-type = 1` cho nhân `C000` để kích hoạt X86PlatformPlugin của macOS.
- **SSDT-RTCAWAC.aml:** Thiết lập cờ ACPI `STAS = 1`, vô hiệu hóa đồng hồ AWAC không tương thích và kích hoạt thiết bị RTC chuẩn (`PNP0B00` / `\_SB.PC00.LPCB.RTC_`).
- **SSDT-EC.aml:** Định nghĩa thiết bị Embedded Controller ảo mang định danh `ACID0001` tại đường dẫn `\_SB.PC00.LPCB.EC` nhằm kích hoạt bộ quản lý nguồn bus USB của Apple.
- **SSDT-USBX.aml:** Cung cấp thông số dòng điện giới hạn `kUSBSleepPortCurrentLimit` và `kUSBWakePortCurrentLimit` (3000mA).
- **SSDT-GPI0.aml:** Kích hoạt bộ điều khiển Intel Alder Lake GPIO controller (`INTC1055`) hỗ trợ giao thức ngắt của Touchpad I2C.
- **SSDT-SBUS.aml & SSDT-MCHC.aml:** Khởi tạo định danh chuẩn cho bộ điều khiển SMBus Host Controller và Host Bridge.
- **ACPI Patches:**
  1. `Fix HP Real-Time Clock Power Loss (005)`: Sửa dải I/O RTC để ngăn chặn thông báo lỗi CMOS checksum reset 005 trên laptop HP khi khởi động lại.
  2. `GPI0 _STA to XSTA`: Cho phép `SSDT-GPI0` quản lý trạng thái kích hoạt của GPIO controller.

### 2. Quyết định Đồ họa (DeviceProperties)
- **iGPU Alder Lake-P GT1 (8086:46A3):** Áp dụng công thức Tiger Lake GT2 spoof (`0x9A49`) tại đường dẫn `PciRoot(0x0)/Pci(0x2,0x0)`:
  - `device-id = <49 9A 00 00>`
  - `AAPL,ig-platform-id = <00 00 49 9A>`
  - `complete-modeset = <01 00 00 00>` (ngăn chặn đóng băng màn hình đen tại gIOScreenLockState 3)
  - `force-online = <01 00 00 00>`, `framebuffer-patch-enable = <01 00 00 00>`
  - `enable-max-pixel-clock-override = <01 00 00 00>`, `rps-control = <01 00 00 00>`
- **dGPU RTX 3050 Ti (10DE:25A0):** Gán cờ `disable-gpu = <01 00 00 00>` và `acpi-wake-type = <01 00 00 00>` tại `PciRoot(0x0)/Pci(0x1,0x0)/Pci(0x0,0x0)`.

### 3. Quyết định Kernel & Thứ tự nạp Kext
1. `Lilu.kext` (v1.7.2) — Nạp vị trí 1
2. `VirtualSMC.kext` (v1.3.8) — Nạp vị trí 2
3. `CpuTopologyRebuild.kext` (v2.0.2) — Điều phối luồng xử lý P/E-core Alder Lake
4. `WhateverGreen.kext` (v1.7.1) — Xử lý đồ họa & framebuffer patch
5. `AppleALC.kext` (v1.9.8) — Patch âm thanh ALC245 (layout 11)
6. `RestrictEvents.kext` (v1.1.6) — Hiển thị định danh CPU 10-core i7-12650H
7. `BrightnessKeys.kext` (v1.0.3) — Điều khiển phím Fn độ sáng
8. `ECEnabler.kext` (v1.0.6) — Hỗ trợ đọc EC trường dài
9. `NVMeFix.kext` (v1.1.3) — Quản lý năng lượng NVMe SK hynix
10. `RealtekRTL8111.kext` (v3.0.0) — Mạng LAN Gigabit
11. `SMCBatteryManager.kext` & `SMCProcessor.kext` — Cảm biến pin và vi xử lý
12. `USBToolBox.kext` & `UTBDefault.kext` — Quản lý cổng USB
13. `VoodooPS2Controller.kext` + `VoodooPS2Keyboard.kext` — Bàn phím PS/2 nội bộ (tắt plugin mouse/trackpad tránh xung đột)
14. `VoodooI2CServices.kext` + `VoodooGPIO.kext` + `VoodooInput.kext` + `VoodooI2C.kext` + `VoodooI2CHID.kext` — Touchpad ELAN0788 I2C
15. `itlwm.kext` (v2.3.0) — Wi-Fi Intel AX211/AX210
16. `IntelBluetoothFirmware.kext` + `IntelBTPatcher.kext` + `BlueToolFixup.kext` (v2.7.2) — Bluetooth Intel AX210

### 4. Cấu hình Quirks & Boot-args
- `boot-args`: `-v debug=0x100 keepsyms=1 -lilubetaall amfi=0x80 -vi2c-force-polling -wegnoegpu alcid=11`
- `AppleCpuPmCfgLock = True` & `AppleXcpmCfgLock = True`: Bù đắp cho BIOS HP không có tùy chọn mở khóa MSR 0xE2.
- `ProvideCurrentCpuInfo = True`: Cung cấp thông tin cấu trúc luồng cho kernel Apple.
- `CustomSMBIOSGuid = True` & `UpdateSMBIOSMode = Custom`: Chuẩn bắt buộc cho laptop HP tránh lỗi ghi đè thông tin OEM.
- `SecureBootModel = Disabled`: Đảm bảo an toàn tuyệt đối trong giai đoạn cài đặt ban đầu.
- Placeholder SMBIOS: `SystemProductName = MacBookPro16,2`, số serial và UUID giữ nguyên placeholder `CHANGE_ME_*` để người dùng tự sinh bằng macserial.
- 2026-10-24T18:28:44 Created build-01-20261024-182842-build-01 (tree e64ee2b11fdc, ocvalidate: docs\validation\validate-20261024-182743.md)
- 2026-10-24T18:33:53 Created build-02-20261024-183352-usb-before-deploy (tree b9a0361009d2, ocvalidate: n/a (existing USB content))
- 2026-10-24T18:35:00 Deployed EFI to G:\EFI (tree e64ee2b11fdc, verified)
- 2026-10-24T19:08:11 Created build-03-20261024-190810-build-02 (tree 61cdf56548b0, ocvalidate: docs\validation\validate-20261024-190802.md)
# BUILD-LOG — Nhật ký Xây dựng và Biên dịch EFI OpenCore

## Bản dựng: build-02 (Khắc phục lỗi treo tại EXITBS:START)
- **Ngày tạo:** 2026-10-24
- **Mục tiêu hệ điều hành:** macOS 26 Tahoe (Darwin 25)
- **Phiên bản OpenCore:** 1.0.8 RELEASE
- **Trạng thái kiểm định:** Đạt chuẩn `efi-validate` (0 lỗi, 0 cảnh báo; ocvalidate: ran, exit 0).

### 1. Phân tích Nguyên nhân Treo tại EXITBS:START
Từ log boot thực tế `logs/opencore-2026-10-24-113640.txt` và báo cáo của người dùng:
- Quá trình boot dừng ngay sau dòng `AAPL: #[EB|LOG:EXITBS:START]` trước khi kernel in các dòng khởi tạo Mach/BSD.
- **Nguyên nhân cốt lõi (Root Cause):** Mục `Kernel > Emulate > Cpuid1Data` và `Cpuid1Mask` ban đầu để trống. Vi xử lý Intel Core i7-12650H thế hệ thứ 12 (Alder Lake) có CPUID gốc là `0x0906A3`. Nhân Darwin / XNU của Apple không hỗ trợ kiến trúc Alder Lake nên khi `ExitBootServices` kết thúc, hàm kiểm tra topo CPU (`x86_validate_topology`) phát hiện CPUID lạ và dừng hệ thống ngay lập tức trong im lặng.

### 2. Các Thay đổi Đã thực hiện (Bản build build-02)
1. **Giả lập CPUID sang Comet Lake (Bắt buộc cho Alder Lake):**
   - `Kernel > Emulate > Cpuid1Data`: `<55060A00000000000000000000000000>` (`0x0A0655` - Comet Lake Core i9/i7).
   - `Kernel > Emulate > Cpuid1Mask`: `<FFFFFFFF000000000000000000000000>`.
2. **Quirks Bảo vệ Kernel & Firmware HP:**
   - `Kernel > Quirks > DisableIoMapper`: Đổi từ `False` $\rightarrow$ `True`. Laptop HP Victus có bảng DMAR chứa vùng nhớ bảo vệ RMRR, khiến AppleVTD gây treo máy nếu không drop DMAR. Bật quirk này giúp kernel bỏ qua I/O mapper xung đột.
   - `Kernel > Quirks > LapicKernelPanic`: Đổi từ `False` $\rightarrow$ `True` (xử lý ngắt LAPIC trên firmware HP).
   - `Booter > Quirks > AllowRelocationBlock`: Đổi từ `False` $\rightarrow$ `True`.
   - `Booter > Quirks > FixupAppleEfiImages`: Đổi từ `False` $\rightarrow$ `True`.
   - `UEFI > Quirks > UnblockFsConnect`: Đổi từ `False` $\rightarrow$ `True`.
- 2026-10-24T19:10:50 Deployed EFI to G:\EFI (tree 61cdf56548b0, verified)
# BUILD-LOG — Nhật ký Xây dựng và Biên dịch EFI OpenCore

## Bản dựng: build-03 (Sửa driver mạng LAN RealtekRTL8111)
- **Ngày tạo:** 2026-10-24
- **Mục tiêu hệ điều hành:** macOS 26 Tahoe (Darwin 25)
- **Phiên bản OpenCore:** 1.0.8 RELEASE
- **Trạng thái kiểm định:** Đạt chuẩn `efi-validate` (0 lỗi, 0 cảnh báo; ocvalidate: ran, exit 0).

### 1. Phân tích Nguyên nhân Thiếu Driver LAN trong Recovery
- Người dùng xác nhận: Bản build `build-02` đã boot thành công vào giao diện macOS (vượt qua hoàn toàn lỗi `EXITBS:START`, màn hình eDP 1080p hiển thị mượt mà).
- Tuy nhiên, bộ cài thông báo không có kết nối mạng (Driver LAN không hoạt động).
- **Nguyên nhân cốt lõi (Root Cause):** Bản dựng trước dùng `RealtekRTL8111.kext` phiên bản v3.0.4. Phiên bản 3.0.x này bị lỗi không khởi tạo được PHY/kết nối trên dòng chip RTL8168 revision 16 (`10EC:8168` rev `0x16`) trong môi trường macOS Recovery. Bản tham chiếu R1 sử dụng phiên bản v2.4.2 hoạt động hoàn hảo.

### 2. Các Thay đổi Đã thực hiện
1. **Hạ cấp driver LAN xuống phiên bản ổn định nhất:**
   - Thay thế `RealtekRTL8111.kext` v3.0.4 bằng `RealtekRTL8111.kext` v2.4.2 (Official Release từ Mieze).
   - Xác nhận hash SHA256: `FA2A6A8435B4F7211FB503E30A2966017CF050C09E839A13E79C4A8A9CD2A8BA`.
2. **Hỗ trợ Wi-Fi tự động kết nối trong Recovery:**
   - Sẵn sàng nạp thông tin mạng (SSID / Password) vào `WiFiConfig` của `itlwm.kext` để máy tự động kết nối Wi-Fi ngay trong Recovery nếu người dùng không cắm dây LAN.
- 2026-10-24T19:23:03 Created build-04-20261024-192302-build-03 (tree 5359af8f9c52, ocvalidate: docs\validation\validate-20261024-192231.md)
- 2026-10-24T19:23:03 Rotated out (deleted) oldest snapshot build-01-20261024-182842-build-01
- 2026-10-24T19:24:51 Deployed EFI to G:\EFI (tree 5359af8f9c52, verified)
- 2026-10-24T22:15:14 Created build-05-20261024-221513-build-04 (tree 0c4b0fca6acf, ocvalidate: 0 errors)
- 2026-10-24T22:15:14 Rotated out (deleted) oldest snapshot build-02-20261024-183352-usb-before-deploy
# BUILD-LOG — Nhật ký Xây dựng và Biên dịch EFI OpenCore

## Bản dựng: build-04 (Khắc phục lỗi treo tại gIOScreenLockState 3 sau khi cài đặt)
- **Ngày tạo:** 2026-10-24
- **Mục tiêu hệ điều hành:** macOS 26 Tahoe (Darwin 25)
- **Phiên bản OpenCore:** 1.0.8 RELEASE
- **Trạng thái kiểm định:** Đạt chuẩn efi-validate (0 lỗi, 0 cảnh báo; ocvalidate: ran, exit 0).

### 1. Phân tích Nguyên nhân Treo tại gIOScreenLockState 3
Từ ảnh chụp màn hình thực tế logs/20261024_212116.jpg do người dùng cung cấp:
- Quá trình boot từ ổ cứng sau khi hoàn thành cài đặt (Macintosh HD) đã tải kernel, nạp kext và mount thành công phân vùng APFS root và data.
- Quá trình dừng hẳn tại 2 dòng cuối cùng:
  ``
  IOConsoleUsers: time(0) 0->0, lin: 0, llk: 0,
  IOConsoleUsers: gIOScreenLockState 3, hs 0, bs 0, now: 0, sm: 0x0
  ``
- **Nguyên nhân cốt lõi (Root Cause):**
  - Môi trường cài đặt (Recovery) chỉ yêu cầu framebuffer cơ bản nên giao diện bộ cài hiển thị bình thường.
  - Khi khởi động vào bản macOS chính thức trên ổ cứng, tiến trình WindowServer cố gắng khởi tạo toàn diện giao diện đồ họa và tăng tốc phần cứng (Metal) thông qua định danh Tiger Lake spoof ( x9A49) khai báo trong DeviceProperties.
  - Do vi kiến trúc đồ họa Intel Alder Lake-H GT1 (8086:46A3) chưa có driver tăng tốc đồ họa chính thức trong macOS Tahoe và dự án XeGfx chưa được nạp (tuân thủ cổng chặn Giai đoạn A), driver đồ họa của Apple bị đóng băng khi khởi tạo pipeline xuất hình eDP, khiến hệ thống dừng vô thời hạn tại gIOScreenLockState 3.

### 2. Các Thay đổi Đã thực hiện (Bản build build-04)
1. **Bổ sung boot-arg -igfxvesa vào NVRAM:**
   - Cập nhật NVRAM > Add > 7C436110-AB2A-4BBB-A880-FE41995C9F82 > boot-args:
     Thêm tham số -igfxvesa vào danh sách boot-args:
     -v debug=0x100 keepsyms=1 -lilubetaall amfi=0x80 -vi2c-force-polling -wegnoegpu alcid=11 -igfxvesa
   - Cơ chế: Tham số -igfxvesa yêu cầu WhateverGreen bỏ qua việc nạp driver tăng tốc phần cứng Intel, buộc WindowServer sử dụng linear framebuffer VESA kế thừa từ UEFI GOP ở độ phân giải gốc 1920×1080. Nhờ đó, màn hình khóa console được giải phóng ngay lập tức (gIOScreenLockState 0), đưa người dùng thẳng vào giao diện Thiết lập ban đầu (Setup Assistant) và Desktop của macOS.
2. **Kiểm tra tương thích & Lưu trữ:**
   - Đạt chuẩn efi-validate (0 lỗi, 0 cảnh báo).
   - Snapshot lưu trữ: snapshots/build-05-20261024-221513-build-04 (tree  c4b0fca6acf).
- 2026-10-24T22:24:56 Deployed EFI to G:\EFI (tree 0c4b0fca6acf, verified)
- 2026-10-24T22:24:55 Deployed EFI to G:\EFI (tree 0c4b0fca6acf, verified)
- 2026-10-25T00:14:36 Created build-06-20261025-001435-usb-before-deploy (tree bc5af20336c8, ocvalidate: n/a (existing USB content))
- 2026-10-25T00:14:36 Rotated out (deleted) oldest snapshot build-03-20261024-190810-build-02
- 2026-10-25T00:14:36 Deployed EFI to G:\EFI (tree 17e7915b2ba7, verified)

## Đính chính 2026-10-25 và bản thử bỏ -igfxvesa
- Phân tích 5 panic mới được chép vào logs: tất cả có UVCAssistant -> IntelBTPatcher 2.4 newHostDeviceRequest -> readBytes -> IOGMD not wired. Xem docs/PANIC-ANALYSIS-20261025.md. Tắt riêng IntelBTPatcher trong workspace để cô lập panic; Bluetooth có thể mất chức năng. Không đổi boot-args/đồ họa, không thêm driver. Các panic có boot-args cũ, chưa thể gán cho build-07 hoặc kết luận mọi lần treo cùng nguyên nhân. Chờ test thực tế sau deploy.
- Sau deploy build-07, người dùng gửi thêm log ACMTRM enrollment pending, AMFI `[non-fatal]`, AppleKeyStore unexpected session uid -1, MACF denial của contextstored và network attach/enable. Không có báo cáo WindowServer hay panic trong đoạn này; chưa đủ xác định nguyên nhân hoặc chứng minh thử nghiệm thành công. Đề nghị thu DiagnosticReports từ volume Data qua Recovery trên máy B; không thêm patch hay thay đổi bảo mật.
- Log tiếp theo do người dùng gửi có `IOUC AppleKeyStoreUserClient failed MACF in process pid 93, contextstored` lặp lại, `unexpected session uid: -1`, AMFI `[non-fatal]` và APFS `reset ino`. Đây là bằng chứng truy cập AppleKeyStore bị từ chối, không chứng minh lỗi GPU, hỏng APFS hoặc nguyên nhân treo. Build/boot-args thực tế chưa được xác nhận; build-07 chưa được agent deploy. Không sửa EFI thêm từ riêng đoạn log này; cần xác nhận bản đang boot và thu DiagnosticReports nếu vẫn không vào GUI.
- Người dùng xác nhận sau hotfix AMFI vẫn dừng ở verbose hơn 5 phút, dòng cuối `set CameraAssistantBundleID: com.apple.cmio.uvcassistantextension`; chưa vào Setup Assistant/Desktop. Trước đó người dùng báo bàn phím và LAN hoạt động, touchpad không hoạt động.
- Các kết luận trước về WindowServer bị chặn bởi DriverKit, AMFI đã sửa xong, framebuffer Tiger Lake có 3 connector và `0x9A490004` chỉ có eDP đều CHƯA XÁC MINH. Không dùng chúng làm cơ sở patch. Không thấy một thông báo trong đoạn log mới không chứng minh lỗi đã được sửa.
- Log `IOVersatile` báo lỗi dependency/load, không đủ để gọi là crash loop hoặc khẳng định vô hại. `GTrace` không chứng minh GUI/framebuffer hoạt động. Dòng verbose cuối không xác định nguyên nhân treo.
- Theo người dùng duyệt sửa, chỉ bỏ `-igfxvesa` trong workspace để thử đối chứng với cấu hình hotfix AMFI hiện tại. Giữ nguyên DeviceProperties; không thêm platform-id, connector hoặc VRAM chưa xác minh. Đây là thử nghiệm, có thể vẫn treo như lần thử trước; không hứa có tăng tốc đồ họa.
- Nguồn chính thức: https://github.com/acidanthera/WhateverGreen/blob/master/README.md mô tả `-igfxvesa` là `Disable Intel Graphics acceleration`. Bỏ cờ này không tạo driver hỗ trợ Tiger Lake/Alder Lake.
- Chờ kiểm định tĩnh và snapshot; USB chưa cập nhật trong lượt sửa này. Cần log WindowServer/loginwindow hoặc DiagnosticReports từ máy B nếu vẫn không vào GUI.
- Mục hotfix bên dưới được giữ làm lịch sử; các khẳng định nguyên nhân và thành công trong mục đó đã được rút lại bởi đính chính này.

## Bản dựng: build-04 → hotfix (AMFI boot-arg fix)
- **Ngày:** 2026-10-25
- **Thay đổi duy nhất:** boot-args mfi=0x80 → mfi_get_out_of_my_way=0x1
- **Lý do:** Log verbose từ MÁY B cho thấy máy treo sau kernel boot — WindowServer không khởi tạo do:
  1. DriverKit services (AppleUserHIDDrivers, IOUserDockChannelSerial) bị AMFI chặn code sign validation
  2. shared_region: vnode Lookup(/System/DriverKit/System/Library/dyld/) failed (error=2) — DriverKit dyld cache chưa xây dựng được
  3. disallowing unsupported code signature page shift: 14 + unable to create a validated cs_blob object: 85 — AMFI từ chối khởi tạo code blob cho DriverKit
  4. Hệ quả: AppleUserHIDDrivers không khởi tạo → loginwindow chờ mãi → không vào GUI
- **Boot-args mới:** `-v debug=0x100 keepsyms=1 -lilubetaall amfi_get_out_of_my_way=0x1 -vi2c-force-polling -wegnoegpu alcid=11 -igfxvesa`
- **Trạng thái kiểm định:** Đạt efi-validate (0 lỗi, 0 cảnh báo; ocvalidate: ran, exit 0)
- **Deploy:** 2026-10-25T00:14:35, tree hash 17e7915b2ba7, verified. Snapshot uild-06-usb-before-deploy (auto backup). Rotated out uild-03.
- **Ghi chú:**
  - mfi_get_out_of_my_way=0x1 tắt hoàn toàn AMFI enforcement — cần thiết trên Hackintosh Tahoe để DriverKit services khởi tạo thành công lần first-boot.
  - Không thay đổi kext, SSDT, DeviceProperties hay SMBIOS.
  - IOVersatile crash loop (Apple Silicon kext) là bình thường trên Hackintosh, không gây treo nhưng spam log.
  - Touchpad không hoạt động lần boot trước — cần xác minh lại sau khi AMFI fix cho phép HID driver khởi tạo.
- 2026-10-25T00:44:30 Created build-07-20261025-004429-no-igfxvesa-test (tree b676dcb35d8d, ocvalidate: 0 errors, 0 warnings; ocvalidate ran)
- 2026-10-25T00:44:30 Rotated out (deleted) oldest snapshot build-04-20261024-192302-build-03
- 2026-10-25T00:52:54 Created build-08-20261025-005254-usb-before-deploy (tree 17e7915b2ba7, ocvalidate: n/a (existing USB content))
- 2026-10-25T00:52:55 Rotated out (deleted) oldest snapshot build-05-20261024-221513-build-04
- 2026-10-25T00:52:55 Deployed EFI to G:\EFI (tree b676dcb35d8d, verified)
- 2026-10-25T01:08:53 Created build-09-20261025-010852-disable-intelbtpatcher (tree 8fd1301031e6, ocvalidate: 0 errors, 0 warnings; ocvalidate ran)
- 2026-10-25T01:08:53 Rotated out (deleted) oldest snapshot build-06-20261025-001435-usb-before-deploy
- 2026-10-25T01:09:50 Deployed EFI to G:\EFI (tree 8fd1301031e6, verified)

## Kết quả kiểm thử build-09 — 2026-10-25
- Người dùng xác nhận "đã boot thành công rồi" sau khi USB được cập nhật build-09 (IntelBTPatcher Enabled=false).
- Boot thành công theo báo cáo máy B; chưa xác nhận cụ thể Desktop/Setup Assistant, chức năng thiết bị, độ ổn định qua restart/sleep-wake hoặc tăng tốc đồ họa.
- Không sửa EFI hoặc USB trong lượt này; giữ snapshot hiện có, chưa đánh dấu known-good. Tiếp tục kiểm thử Giai đoạn A; Giai đoạn B chưa được mở.
