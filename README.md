# Hackintosh HP Victus 15-fa0xxx (i7-12650H, UHD 64 EU) — macOS 26 Tahoe có tăng tốc Metal

EFI OpenCore và các bản vá NootedGreen cho **HP Victus 15-fa0xxx** (board `8A4F`, i7-12650H, iGPU `8086:46A3`
Alder Lake-P GT1 UHD 64 EU, RTX 3050 Ti tắt) chạy **macOS 26.7.1 Tahoe (25G241)** với **tăng tốc Metal 2** trên iGPU.

> **English TL;DR.** OpenCore EFI + NootedGreen patches for an HP Victus 15-fa0xxx (i7-12650H, Alder Lake-P
> UHD `46A3` 64 EU, fixed 60 MB DVMT) on macOS 26.7.1 (25G241), based on the
> [JulioNectar](https://github.com/JulioNectar/Hackintosh-XPS13Plus-IrisXe-Tahoe) Tiger Lake driver stack.
> The well-known boot panic `IOAccelTask::release ← IGAccelTask::withOptions` (CR2 0xc78, JN #13/#24) is caused by
> Apple's TGL driver decoding **GGC.GMS 0xF0–0xFE (4 MB units) as 32 MB units** — 60 MB becomes 8128 MB, the GPU VA
> range is invalid and `IGAccelTask::initAllocators` fails. The same misdecode exists in the TGL framebuffer.
> Four small patches fix it on this machine (see [Root causes](#các-lỗi-đã-sửa-và-nguyên-nhân)):
> GMSFIX (accelerator), GMSFIX-FB (framebuffer), PAVPFIX and FENCEFIX. Result: desktop with Metal 2,
> 1920×1080 @ 144 Hz. If your laptop has a fixed DVMT below 64 MB and the same panic, these patches are likely relevant.
> Bluetooth, brightness (SSDT-PNLF + `ngreenblmax=17741`), audio (AppleALC layout 11 + OCLP Modern Audio) and the webcam also work.

## Trạng thái (build-31, 2026-11-05)

| Hạng mục | Trạng thái |
|---|---|
| Khởi động macOS 26.7.1 (25G241) | ✅ |
| **Tăng tốc đồ hoạ iGPU** | ✅ **Metal 2**, 1920×1080 @ 144 Hz, 64 EU (`xe-topo` 16390), con trỏ hiển thị đúng |
| Wi-Fi Intel AX210 | ✅ AirportItlwm-Tahoe 1.1.0-beta.1 (ZC28) + root patch OCLP-CustoMac |
| Ethernet RTL8111 | ✅ RealtekRTL8111 **2.4.2** (bản 3.0.0 không chạy trên máy này) |
| Bàn phím PS/2, touchpad ELAN0788 (I2C, polling) | ✅ |
| Bluetooth AX210 | ✅ IntelBluetoothFirmware 2.5.3 (fork lshbluesky) + BlueToolFixup |
| Độ sáng màn hình | ✅ thanh trượt đủ dải (SSDT-PNLF + `ngreenblmax=17741`) |
| Audio ALC245 | ✅ loa, mic trong (AppleALC layout 11 + root patch Modern Audio); ⚠️ tai nghe 3,5 mm chỉ kênh trái do lỗi cổng jack của máy (Linux cũng bị) |
| Pin, nhiệt độ CPU, phím độ sáng | ✅ |
| USB (cổng HS) | ✅ USB 3 đang chạy tốc độ USB 2 (chưa map cổng SS) |
| dGPU RTX 3050 Ti | ⛔ tắt bằng SSDT (macOS không có driver); **HDMI không dùng được** (nối vào dGPU) |
| Camera HP Wide Vision HD (`30C9:0069`) | ✅ driver UVC có sẵn của macOS |
| Đầu đọc thẻ RTS5228 | ❌ không có driver — xem [`docs/DEFERRED.md`](docs/DEFERRED.md) |
| Sleep, màn hình ngoài, video có DRM (PAVP) | ❌ không hỗ trợ với stack này |
| Metal 3 | ❌ không đạt được với driver Tiger Lake |

Display sleep/wake hoạt động. Chưa kiểm kỹ: chạy tải nặng lâu.

## Cảnh báo — đọc trước khi dùng

- **Bảo mật hạ thấp:** SIP `0x0A13`, AMFI tắt (`amfi_get_out_of_my_way=1`) + AMFIPass. Chỉ dùng trên máy cá nhân.
- **Không cập nhật macOS.** Stack đồ hoạ và root patch Wi-Fi + Audio gắn với đúng 25G241; cập nhật sẽ làm hỏng cả ba.
- Có thể gặp GPU hang / kernel panic. Luôn giữ một EFI không tăng tốc để quay về (`EFI/OC/config-install.plist`
  hoặc build nền).
- **Tránh System Settings › Displays** và đổi profile màu (từng gây panic với stack JulioNectar). Đổi độ phân giải /
  tần số quét bằng `tools/xe-res` của JulioNectar.
- EFI trong repo dùng **SMBIOS giả** (`CHANGE_ME_*`). Tự sinh serial riêng; không bao giờ commit serial thật.
- EFI cần các kext Wi-Fi của OCLP-CustoMac (`IOSkywalkFamily`, `IO80211FamilyLegacy`) — đây là binary của Apple,
  **lấy từ [kgp-macPro/OCLP-CustoMac](https://github.com/kgp-macPro/OCLP-CustoMac)**, không phân phối lại.

## Phần cứng

| | |
|---|---|
| Máy | HP Victus 15-fa0xxx, board `8A4F`, BIOS F.34 |
| CPU | Intel Core i7-12650H (6P + 4E, 16 luồng) |
| iGPU | `8086:46A3` rev 0c, UHD 64 EU (1 slice, 4 DSS mask `0x33`, L3 6 bank), **DVMT cố định 60 MB** (GGC `0xFEC1`, GMS `0xFE`) |
| dGPU | `10DE:25A0` RTX 3050 Ti (`\_SB.PC00.PEG1.PEGP`) |
| Màn hình | eDP 1920×1080 144 Hz trên iGPU |
| Wi-Fi / BT | Intel AX210 `8086:2725` / `8087:0032` |
| Ethernet | Realtek RTL8111 `10EC:8168` |
| Touchpad | ELAN0788 (I2C0 `8086:51E8`) |
| SSD | SK hynix BC711 256 GB |

| Audio | Realtek ALC245 (subsys `103C8A4F`), HDA `\_SB.PC00.HDAS` = `PciRoot(0x0)/Pci(0x1f,0x3)` |

Chi tiết: [`laptop-specs.md`](laptop-specs.md).

## Cấu hình EFI (build-31)

- **OpenCore 1.0.8**, SMBIOS `MacBookPro16,2`.
- **SSDT** (tự viết từ DSDT của máy, nguồn ở [`docs/acpi-src/`](docs/acpi-src/)): PLUG-ALT, EC-USBX, AWAC, XOSI
  (+ patch `_OSI`→`XOSI`), **DGPU-OFF** (tắt RTX 3050 Ti), SBUS-MCHC, **PNLF** (thiết bị đèn nền dưới `PC00.GFX0`;
  firmware không có sẵn, thiếu nó macOS không hiện thanh độ sáng).
- **Kext:** Lilu, VirtualSMC (+SMCProcessor, SMCBatteryManager), ECEnabler, WhateverGreen, **NootedGreen (bản vá)**,
  AppleALC 1.9.8, RestrictEvents, CpuTopologyRebuild, NVMeFix, BrightnessKeys, RealtekRTL8111 2.4.2, AMFIPass, IOSkywalkFamily,
  IO80211FamilyLegacy, AirportItlwm-Tahoe, IntelBluetoothFirmware + IntelBTPatcher 2.5.3 (fork lshbluesky),
  BlueToolFixup 2.7.2, XHCI-ADL-Injector (tự viết, chỉ Info.plist cho `8086:51ED`),
  USBToolBox + UTBMap, VoodooPS2 (bàn phím), VoodooI2C 3.0.0 (fork lzhoang2801) + VoodooI2CHID.
- **iGPU:** spoof Tiger Lake `device-id 9A49`, `AAPL,ig-platform-id 0x9A490000` (theo JulioNectar).
  **dGPU:** `disable-gpu` + SSDT. **Touchpad:** property `force-polling` trên I2C0. **Audio:** `layout-id` 11 trên
  `PciRoot(0x0)/Pci(0x1f,0x3)`. **Bluetooth:** NVRAM `bluetoothExternalDongleFailed`, `bluetoothInternalControllerInfo`.
- **Quirk đáng chú ý:** `SetupVirtualMap = true` (thiếu nó máy treo ở `EXITBS:START`), `AppleXcpmCfgLock`
  (CFG Lock bật, BIOS không có tuỳ chọn), `DisableIoMapper = true`, `ProvideCurrentCpuInfo`.
- **boot-args** (219 ký tự — Lilu cắt ở ~228, phải đặt tham số đồ hoạ lên đầu):
  ```
  ngreen-eu=64 ngreen-l3=6 ngreenblmax=17741 -ngreentglwithgfx -allow3d -disablegfxfirmware ngreen-dmc=adlp ngreenV142=3 -ngreenv189 -ngreenkeepefi -ngreenxefix -ngreenfixbootmode amfi_get_out_of_my_way=1 -amfipassbeta -v
  ```
  `keepsyms=1 debug=0x100` đã bỏ để có chỗ cho `ngreenblmax`; khi cần gỡ panic thì thêm lại tạm thời.

## Các lỗi đã sửa và nguyên nhân

Các bản vá nằm trong [`patches/`](patches/), áp lên source NootedGreen của JulioNectar @ `6f03560`.
Bản dùng hiện tại: **`patches/nootedgreen-gmsfix-v7-jn6f03560.patch`** (gồm cả các log chẩn đoán).
Diễn biến và số đo từng bước: [`docs/BUILD-LOG.md`](docs/BUILD-LOG.md) (build-12 → build-26).

| # | Triệu chứng | Nguyên nhân | Bản vá |
|---|---|---|---|
| 1 | Boot-args `ngreen-*` không có tác dụng | Chuỗi 291 ký tự bị cắt (Lilu ~228) | Rút còn 224 ký tự, tham số đồ hoạ lên đầu |
| 2 | Panic `IOAccelTask::release ← IGAccelTask::withOptions`, CR2 `0xc78`, ~54 s | Driver TGL (`IGMemoryManager::initSegments`) giải mã GMS `0xFE` thành 8128 MB (đơn vị 32 MB) thay vì 60 MB (đơn vị 4 MB của Gen9+) → dải VA GPU sai → `initAllocators` thất bại | **GMSFIX**: thay phép giải mã bằng kích thước stolen thật |
| 3 | Panic WindowServer `IOFramebuffer::getAttributeExt+0x25` (NULL) | Framebuffer TGL (`FBMemMgr_Init`) cũng giải mã sai (→ 4032 MB) nên không đăng ký `AppleIntelFramebufferController`; accelerator chạy "standalone" | **GMSFIX-FB**: vá tương tự trong framebuffer |
| 4 | Panic `IntelAccelerator::PAVPCommandCallback`, CR2 `0xb8` | BIOS bật PAVP (MMIO `0x1082C0`) nhưng context PAVP không được tạo → NULL | **PAVPFIX**: luôn đi nhánh "PAVP tắt" (mất phát video DRM) |
| 5 | Con trỏ chuột vỡ thành các dải | Fence X-tile của framebuffer dài 64 MB (theo bảng Apple) tràn qua stolen 60 MB, phủ lên buffer con trỏ ở ngay sau stolen | **FENCEFIX**: cắt cuối fence về cuối vùng stolen |
| 6 | Không có thanh độ sáng | Firmware không có thiết bị `PNLF` (`APP0002`) → macOS gắn `AppleDisplay` thay vì `AppleBacklightDisplay` | **SSDT-PNLF** tối giản (không ghi thanh ghi PWM) |
| 7 | Độ sáng tối đa chỉ ~18,5 % | macOS không ghi chu kỳ PWM (`bl hw=96000 apple=0`), duty tối đa 17741 đi thẳng ra phần cứng | Boot-arg `ngreenblmax=17741` (XE-BLR có sẵn trong NootedGreen của JulioNectar) |

Tất cả các bản vá đều tắt được bằng boot-arg (`-ngreennogmsfix`, `-ngreennopavpfix`, `-ngreennofencefix`).
Giá trị chẩn đoán xem bằng `ioreg -rc IntelAccelerator -d1 | grep -E 'xe-cur|xe-fence|xe-mm'`.

## Cài đặt (tóm tắt)

1. Cài macOS 26.7.1 (25G241) bằng EFI **không tăng tốc** (`EFI/OC/config-install.plist` → đổi tên thành `config.plist`).
   BIOS: Secure Boot tắt, không dùng chế độ chỉ-dGPU.
2. Root patch bằng OCLP-CustoMac 3.0.3, chọn **Modern Wireless** và **Modern Audio** (cần KDK 25G241, OCLP tự tải) —
   [`docs/POSTINSTALL-RUNBOOK.md`](docs/POSTINSTALL-RUNBOOK.md) §1 và §5.
3. Cài stack đồ hoạ JulioNectar @ `6f03560` (`zsh install.sh`, cần spoof `9A49` lúc cài) —
   [`docs/GRAPHICS-RUNBOOK.md`](docs/GRAPHICS-RUNBOOK.md).
4. Áp bản vá và build NootedGreen trên chính máy đó —
   [`docs/GMSFIX-RUNBOOK.md`](docs/GMSFIX-RUNBOOK.md):
   ```
   cd ~/xe-stack && git apply nootedgreen-gmsfix-v7-jn6f03560.patch && zsh build-nootedgreen.sh
   ```
   rồi chép `build/NootedGreen.kext` vào `EFI/OC/Kexts/`.
5. Tự điền SMBIOS (serial, MLB, UUID, ROM) vào `config.plist` của bạn.

## Cấu trúc repo

| Đường dẫn | Nội dung |
|---|---|
| `EFI/` | EFI OpenCore hiện tại (build-31), SMBIOS giả |
| `patches/` | Bản vá NootedGreen (gộp `vN-jn6f03560`, tăng thêm `vN-to-vM`) |
| `docs/STATE.md`, `docs/BUILD-LOG.md` | Trạng thái và nhật ký từng bản build |
| `docs/GRAPHICS-PROGRESS.md` | Tiến trình thử đồ hoạ |
| `docs/DRIVER-MATRIX.md`, `docs/SOURCES.md` | Driver đã kiểm định, nguồn, phiên bản, SHA-256 |
| `docs/*-RUNBOOK.md` | Hướng dẫn chạy trên laptop |
| `docs/acpi-src/` | Mã nguồn SSDT |
| `tools/` | Script dump phần cứng (chạy trên laptop), ocvalidate |
| `.claude/` | Skill/quy tắc cho Claude Code dùng khi phát triển dự án |

## Ghi công và giấy phép

- [JulioNectar/Hackintosh-XPS13Plus-IrisXe-Tahoe](https://github.com/JulioNectar/Hackintosh-XPS13Plus-IrisXe-Tahoe) —
  stack đồ hoạ (driver TGL 16.0.32, NootedGreen bản sửa, libxedrv). Các bản vá trong `patches/` là sửa đổi của
  **NootedGreen** ([sgiammori/NootedGreen](https://github.com/sgiammori/NootedGreen)), theo giấy phép
  **Thou Shalt Not Profit License 1.0** — chỉ dùng phi lợi nhuận.
- [acidanthera](https://github.com/acidanthera) (OpenCore, Lilu, VirtualSMC, WhateverGreen, …),
  [kgp-macPro](https://github.com/kgp-macPro) (AirportItlwm-Tahoe, OCLP-CustoMac),
  [Mieze](https://github.com/Mieze/RTL8111_driver_for_OS_X), [lzhoang2801/VoodooI2C](https://github.com/lzhoang2801/VoodooI2C),
  [b00t0x](https://github.com/b00t0x/CpuTopologyRebuild), [USBToolBox](https://github.com/USBToolBox/kext),
  [averycblack/ECEnabler](https://github.com/averycblack/ECEnabler),
  [lshbluesky/IntelBluetoothFirmware](https://github.com/lshbluesky/IntelBluetoothFirmware) (fork của OpenIntelWireless).
- Tham khảo: [cheseecake/i3-1220p-macos-gpu](https://github.com/cheseecake/i3-1220p-macos-gpu),
  [khucxtriendev/irisxegraphic-i712800h-efi](https://github.com/khucxtriendev/irisxegraphic-i712800h-efi),
  [sulthonuladib/victus-15-fa0xxx-hackintosh](https://github.com/sulthonuladib/victus-15-fa0xxx-hackintosh).
- Repo này không phân phối binary của Apple. Driver Tiger Lake do `install.sh` của JulioNectar tải về trên máy bạn;
  `AppleHDA.kext` do OCLP-CustoMac cài khi root patch Modern Audio.
