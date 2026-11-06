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
> Bluetooth, brightness (SSDT-PNLF + `ngreenblmax=17741`), audio (VoodooHDA 3.6.8 in /Library/Extensions) and the webcam also work.
> **No OCLP root patch** since build-45: Wi-Fi uses laobamac AirportItlwm-Tahoe v2.4.0-alpha on Tahoe's own IO80211Family/Skywalk.
> **CPU performance:** NootedGreen XE-PM plus a new **XE-HWPAUTO** patch (HWP desired = 0, autonomous clock; v8) raise
> Geekbench 7 from 1076 / 5837 to **2030 / 9646** — 92 % / 95 % of Linux on the same laptop (2195 / 10101).
> Current build-41: JulioNectar `24450b4` + project patch **v10** (machine defaults built in, boot-args 163 chars),
> WhateverGreen `gfxrst=1` cuts boot from 38 s to 23 s. Not working: hardware video decode (`-ngreengva` panics in
> `VTDecoderXPCService`; turning PAVPFIX off panics at boot) and the Geekbench 7 GPU run (hangs in Feature Matching).

## Trạng thái (build-48, 2026-11-07)

| Hạng mục | Trạng thái |
|---|---|
| Khởi động macOS 26.7.1 (25G241) | ✅ |
| **Tăng tốc đồ hoạ iGPU** | ✅ **Metal 2**, 1920×1080 @ 144 Hz, 64 EU (`xe-topo` 16390), con trỏ hiển thị đúng |
| Wi-Fi Intel AX210 | ✅ **laobamac AirportItlwm-Tahoe v2.4.0-alpha** (theo JulioNectar), **Wi-Fi 6** (`itlwm_he=1`): dùng IO80211Family/IOSkywalkFamily gốc của Tahoe, **không cần root patch**; không AirDrop/AWDL, không WPA3-only |
| Ethernet RTL8111 | ✅ RealtekRTL8111 **2.4.2** (bản 3.0.0 không chạy trên máy này) |
| Bàn phím PS/2, touchpad ELAN0788 (I2C, ngắt GPIO) | ✅ cử chỉ đa điểm |
| Bluetooth AX210 | ✅ IntelBluetoothFirmware 2.5.3 (fork lshbluesky) + BlueToolFixup |
| Độ sáng màn hình | ✅ thanh trượt đủ dải (SSDT-PNLF + `ngreenblmax=17741`) |
| Audio ALC245 | ✅ **VoodooHDA 3.6.8** trong `/Library/Extensions`, **không cần root patch**; ổn định hơn AppleHDA qua root patch (người dùng). ⚠️ tai nghe 3,5 mm chỉ kênh trái do lỗi cổng jack của máy (Linux cũng bị) |
| Pin, nhiệt độ CPU, phím độ sáng | ✅ |
| **Hiệu năng CPU** | ✅ Geekbench 7 **2030 / 9646** = 92 % / 95 % Linux cùng máy (XE-PM + XE-HWPAUTO; trước đó 1076 / 5837) — [`docs/PERFORMANCE.md`](docs/PERFORMANCE.md) |
| iGPU (Geekbench 7 Metal) | ⚠️ 1094 một lần (build-33); từ build-37 bài **Feature Matching** treo GPU (render + compute cùng treo, stamp compute không trả về sau reset) → không chạy được hết — [`docs/BUILD-LOG.md`](docs/BUILD-LOG.md) |
| Thời gian khởi động | ✅ picker → màn hình đăng nhập **23 s** (trước 38 s) nhờ `gfxrst=1`; màn hình nháy đen ngắn lúc driver khởi tạo |
| Vulkan | ✅ Vulkan 1.4 qua **MoltenVK** (LunarG Vulkan SDK; `vulkaninfo` thấy iGPU, `vkcube` chạy) — không geometry shader, không float64 |
| USB | ✅ 2 cổng USB-A có USB 3 (SS01/SS02, map từ Linux bằng `tools/map-usb-linux.sh`); USB-C qua controller TB4 do macOS tự nhận (chưa đo tốc độ) |
| Boot không cần USB | ✅ OpenCore trên ESP ổ NVMe, cạnh Limine (CachyOS) — [`docs/POSTINSTALL-RUNBOOK.md`](docs/POSTINSTALL-RUNBOOK.md) §4 |
| dGPU RTX 3050 Ti | ⛔ tắt bằng SSDT (macOS không có driver); **HDMI không dùng được** (nối vào dGPU) |
| Camera HP Wide Vision HD (`30C9:0069`) | ✅ driver UVC có sẵn của macOS |
| Đầu đọc thẻ RTS5228 | ❌ không có driver — xem [`docs/DEFERRED.md`](docs/DEFERRED.md) |
| Giải mã video phần cứng (H.264/HEVC) | ❌ `-ngreengva`: panic NULL+0x284 trong `VTDecoderXPCService` khi tạo context giải mã; tắt PAVPFIX để thử thì panic lúc boot (`PAVPCommandCallback`) — video giải mã bằng CPU |
| Sleep, màn hình ngoài, video có DRM (PAVP) | ❌ không hỗ trợ với stack này |
| Metal 3 | ❌ không đạt được với driver Tiger Lake |

Display sleep/wake hoạt động. Lỗi phụ đã thấy: engine blit (BCS) treo ~30–60 s sau mỗi lần boot (macOS tự phục hồi);
một lần panic chia cho 0 trong `fbTimingsWorker` (`-ngreenfixbootmode`) lúc boot.

## Cảnh báo — đọc trước khi dùng

- **Bảo mật hạ thấp:** SIP `0x0A13`, AMFI tắt (`amfi_get_out_of_my_way=1`, stack đồ hoạ cần). Chỉ dùng trên máy cá nhân.
- **Không cập nhật macOS.** Stack đồ hoạ gắn với đúng 25G241 (Wi-Fi laobamac chỉ nạp trên Darwin 25); cập nhật có thể làm hỏng.
- Có thể gặp GPU hang / kernel panic. Luôn giữ một EFI không tăng tốc để quay về (`EFI/OC/config-install.plist`
  hoặc build nền).
- **Không chạy `powermetrics`** khi cần ổn định: nó từng gây kernel panic trong framebuffer TGL (NULL qua `AppleGraphicsDeviceControl`). Đo xung bằng `tools/xe-freq.c`, nhiệt/công suất bằng `tools/xe-monitor.py`.
- **Chép EFI sang ESP ổ trong từ Linux**, không từ macOS: bản chép bằng macOS làm OpenCore báo thiếu `Info.plist` của kext lồng trong `PlugIns`.
- **Tránh System Settings › Displays** và đổi profile màu (từng gây panic với stack JulioNectar). Đổi độ phân giải /
  tần số quét bằng `tools/xe-res` của JulioNectar.
- EFI trong repo dùng **SMBIOS giả** (`CHANGE_ME_*`). Tự sinh serial riêng; không bao giờ commit serial thật.
- Từ build-48 EFI không còn kext nào của OCLP-CustoMac (`IOSkywalkFamily`, `IO80211FamilyLegacy`, `AMFIPass`): Wi-Fi và audio không cần root patch.

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

## Cấu hình EFI (build-48)

- **OpenCore 1.0.8**, SMBIOS `MacBookPro16,2`.
- **SSDT** (tự viết từ DSDT của máy, nguồn ở [`docs/acpi-src/`](docs/acpi-src/)): PLUG-ALT, EC-USBX, AWAC, XOSI
  (+ patch `_OSI`→`XOSI`), **DGPU-OFF** (tắt RTX 3050 Ti), SBUS-MCHC, **PNLF** (thiết bị đèn nền dưới `PC00.GFX0`;
  firmware không có sẵn, thiếu nó macOS không hiện thanh độ sáng).
- **Kext:** Lilu, VirtualSMC (+SMCProcessor, SMCBatteryManager), ECEnabler, WhateverGreen, **NootedGreen (bản vá)**,
  AppleALC 1.9.8, RestrictEvents, CpuTopologyRebuild, NVMeFix, BrightnessKeys, RealtekRTL8111 2.4.2,
  **AirportItlwm-Tahoe v2.4.0-alpha (laobamac)**, IntelBluetoothFirmware + IntelBTPatcher 2.5.3 (fork lshbluesky),
  BlueToolFixup 2.7.2, XHCI-ADL-Injector (tự viết, chỉ Info.plist cho `8086:51ED`),
  USBToolBox + UTBMap (HS01/02/04/06/07 + SS01/02), VoodooPS2 (bàn phím), VoodooI2C 3.0.0 (fork lzhoang2801) + VoodooI2CHID.
- **iGPU:** spoof Tiger Lake `device-id 9A49`, `AAPL,ig-platform-id 0x9A490000` (theo JulioNectar).
  **dGPU:** `disable-gpu` + SSDT. **Touchpad:** ngắt GPIO (`TPD0._CRS` trả GpioInt nhờ SSDT-XOSI; không dùng `force-polling`). **Audio:** `layout-id` 11 trên
  `PciRoot(0x0)/Pci(0x1f,0x3)`. **Bluetooth:** NVRAM `bluetoothExternalDongleFailed`, `bluetoothInternalControllerInfo`.
- **CPU (NootedGreen XE-PM, `-ngreenpm`):** sửa turbo HWP trên CPU lai, EPP 0, tắt EE turbo, D3 cho thiết bị PCI không driver;
  từ patch v9, `-ngreenpm` tự bật **XE-HWPAUTO** và giữ bảng C-state gốc của XCPM (C8/C10 làm multi-core giảm) —
  không cần `ngreenpmauto=1 ngreenpmcst=0` nữa (vẫn ghi đè được).
  CpuTopologyRebuild để mặc định (6 nhân / 16 luồng; `ctrsmt=off` đo được kém hơn). PL1 giữ của BIOS.
- **Quirk đáng chú ý:** `SetupVirtualMap = true` (thiếu nó máy treo ở `EXITBS:START`), `AppleXcpmCfgLock`
  (CFG Lock bật, BIOS không có tuỳ chọn), `DisableIoMapper = true`, `ProvideCurrentCpuInfo`.
- **boot-args** (160 ký tự):
  ```
  -ngreenpm -ngreentglwithgfx -allow3d -disablegfxfirmware -ngreenv189 -ngreenkeepefi -ngreenxefix -ngreenfixbootmode amfi_get_out_of_my_way=1 gfxrst=1 itlwm_he=1
  ```
  `itlwm_he=1` bật Wi-Fi 6 (802.11ax) trong AirportItlwm laobamac (mặc định tắt).
  Patch v10 ghi sẵn giá trị của máy này làm mặc định: topology **64 EU / L3 6**, `ngreenV142=3`, `ngreenblmax=17741`,
  `ngreen-dmc=adlp` (ghi cứng, không đọc fuse; boot-arg cùng tên vẫn ghi đè). `gfxrst=1` (WhateverGreen) xoá màn hình boot
  thay vì chép nó qua vùng nhớ chậm: −15 s.
  Hai giới hạn: **Lilu chỉ giữ ~228 ký tự đầu** cho cờ đọc bằng `checkKernelArgument` (`-ngreen*`…), còn
  **kernel giữ 255** cho tham số đọc bằng `PE_parse_boot_argn` (`gfxrst`, `itlwm_he`, `ngreen-eu`…). Thêm cờ mới thì kiểm vị trí.

## Các lỗi đã sửa và nguyên nhân

Các bản vá nằm trong [`patches/`](patches/), áp lên source NootedGreen của JulioNectar @ **`24450b4`** (từ build-38; trước đó `6f03560`).
Bản dùng hiện tại: **`patches/nootedgreen-gmsfix-v10-jn24450b4.patch`** (v8 + mặc định XE-PM của v9 + mặc định máy của v10;
gồm cả các log chẩn đoán). Bản v8 cho JN `6f03560` vẫn giữ: `patches/nootedgreen-gmsfix-v8-jn6f03560.patch`.
Diễn biến và số đo từng bước: [`docs/BUILD-LOG.md`](docs/BUILD-LOG.md) (build-12 → build-43).

| # | Triệu chứng | Nguyên nhân | Bản vá |
|---|---|---|---|
| 1 | Boot-args `ngreen-*` không có tác dụng | Chuỗi 291 ký tự bị cắt (Lilu ~228) | Rút còn 224 ký tự, tham số đồ hoạ lên đầu |
| 2 | Panic `IOAccelTask::release ← IGAccelTask::withOptions`, CR2 `0xc78`, ~54 s | Driver TGL (`IGMemoryManager::initSegments`) giải mã GMS `0xFE` thành 8128 MB (đơn vị 32 MB) thay vì 60 MB (đơn vị 4 MB của Gen9+) → dải VA GPU sai → `initAllocators` thất bại | **GMSFIX**: thay phép giải mã bằng kích thước stolen thật |
| 3 | Panic WindowServer `IOFramebuffer::getAttributeExt+0x25` (NULL) | Framebuffer TGL (`FBMemMgr_Init`) cũng giải mã sai (→ 4032 MB) nên không đăng ký `AppleIntelFramebufferController`; accelerator chạy "standalone" | **GMSFIX-FB**: vá tương tự trong framebuffer |
| 4 | Panic `IntelAccelerator::PAVPCommandCallback`, CR2 `0xb8` | BIOS bật PAVP (MMIO `0x1082C0`) nhưng context PAVP không được tạo → NULL | **PAVPFIX**: luôn đi nhánh "PAVP tắt" (mất phát video DRM) |
| 5 | Con trỏ chuột vỡ thành các dải | Fence X-tile của framebuffer dài 64 MB (theo bảng Apple) tràn qua stolen 60 MB, phủ lên buffer con trỏ ở ngay sau stolen | **FENCEFIX**: cắt cuối fence về cuối vùng stolen |
| 6 | Không có thanh độ sáng | Firmware không có thiết bị `PNLF` (`APP0002`) → macOS gắn `AppleDisplay` thay vì `AppleBacklightDisplay` | **SSDT-PNLF** tối giản (không ghi thanh ghi PWM) |
| 7 | Độ sáng tối đa chỉ ~18,5 % | macOS không ghi chu kỳ PWM (`bl hw=96000 apple=0`), duty tối đa 17741 đi thẳng ra phần cứng | `ngreenblmax=17741` (XE-BLR có sẵn trong NootedGreen của JulioNectar; từ v10 là mặc định, không cần boot-arg) |
| 8 | Geekbench 7 chỉ ~54 % Linux; P-core kẹt ~3,8 GHz | XCPM ghi giới hạn HWP sai trên CPU lai | `-ngreenpm` (XE-PM của JulioNectar): single +13 % |
| 9 | Multi-core giảm khi bật XE-PM | C8/C10 do XE-PM bật | `ngreenpmcst=0`: multi 5476 → 7114 |
| 10 | Single-core vẫn ~54 % Linux; luồng đơn tụt xung theo từng đợt | XNU chuyển luồng qua nhiều P-core; mỗi lần XCPM ghi HWP "desired" thấp cho nhân mới, chỉ nâng ở chu kỳ điều khiển sau | **XE-HWPAUTO** (patch v8): desired = 0 → nhân tự chọn xung; Geekbench 7 1191 / 5637 → **2030 / 9646** |
| 11 | boot-args đầy 255, không thêm được cờ mới | Mỗi tinh chỉnh là một boot-arg | **v9**: `-ngreenpm` mặc định HWPAUTO bật, C8/C10 tắt; **v10**: mặc định topology/V142/blmax/dmc của máy → 255 → 163 |
| 12 | Khởi động 38 s | WhateverGreen mặc định chép màn hình boot (FB_COPY) qua vùng nhớ không cache | `gfxrst=1` (theo JulioNectar): 23 s |

Tất cả các bản vá đều tắt được bằng boot-arg (`-ngreennogmsfix`, `-ngreennopavpfix`, `-ngreennofencefix`); XE-HWPAUTO đổi trực tiếp bằng `sudo sysctl -w debug.xepm.hwpauto=0|1`.
Giá trị chẩn đoán xem bằng `ioreg -rc IntelAccelerator -d1 | grep -E 'xe-cur|xe-fence|xe-mm'`.

## Cài đặt (tóm tắt)

1. Cài macOS 26.7.1 (25G241) bằng EFI **không tăng tốc** (`EFI/OC/config-install.plist` → đổi tên thành `config.plist`).
   BIOS: Secure Boot tắt, không dùng chế độ chỉ-dGPU.
2. **Không cần root patch.** Wi-Fi chạy ngay bằng AirportItlwm laobamac trong EFI. Audio: cài VoodooHDA 3.6.8 vào
   `/Library/Extensions` và duyệt trong Privacy & Security — [`docs/POSTINSTALL-RUNBOOK.md`](docs/POSTINSTALL-RUNBOOK.md) §7
   (đường cũ bằng OCLP-CustoMac Modern Wireless + Modern Audio: §1, §5, §6).
3. Cài stack đồ hoạ JulioNectar @ `24450b4` (`zsh install.sh`, cần spoof `9A49` lúc cài; áp patch trước khi chạy vì
   `install.sh` build cả NootedGreen) —
   [`docs/GRAPHICS-RUNBOOK.md`](docs/GRAPHICS-RUNBOOK.md).
4. Áp bản vá và build NootedGreen trên chính máy đó —
   [`docs/GMSFIX-RUNBOOK.md`](docs/GMSFIX-RUNBOOK.md):
   ```
   cd ~/xe-stack && git checkout 24450b476d7ca025b83c85d7b8362caf3234d2f2 && git apply nootedgreen-gmsfix-v10-jn24450b4.patch && zsh build-nootedgreen.sh
   ```
   rồi chép `build/NootedGreen.kext` vào `EFI/OC/Kexts/`.
5. Tự điền SMBIOS (serial, MLB, UUID, ROM) vào `config.plist` của bạn.
6. (Tuỳ chọn) Boot không cần USB: chép `EFI/OC` vào ESP ổ trong **từ Linux**, tạo mục boot bằng `efibootmgr` —
   [`docs/POSTINSTALL-RUNBOOK.md`](docs/POSTINSTALL-RUNBOOK.md) §4.

## Cấu trúc repo

| Đường dẫn | Nội dung |
|---|---|
| `EFI/` | EFI OpenCore hiện tại (build-48), SMBIOS giả |
| `patches/` | Bản vá NootedGreen (gộp `vN-jn24450b4` / `vN-jn6f03560`, tăng thêm `vN-to-vM`) |
| `docs/STATE.md`, `docs/BUILD-LOG.md` | Trạng thái và nhật ký từng bản build |
| `docs/GRAPHICS-PROGRESS.md` | Tiến trình thử đồ hoạ |
| `docs/PERFORMANCE.md` | Số đo CPU/iGPU, so với Linux, từng bước cải thiện |
| `docs/ROADMAP.md` | Mục tiêu sau build-37 (G1–G4) và kết quả |
| `logs/` | Panic / GPU restart report (che serial) dùng để phân tích |
| `docs/DRIVER-MATRIX.md`, `docs/SOURCES.md` | Driver đã kiểm định, nguồn, phiên bản, SHA-256 |
| `docs/*-RUNBOOK.md` | Hướng dẫn chạy trên laptop |
| `docs/acpi-src/` | Mã nguồn SSDT |
| `tools/` | Dump phần cứng và map cổng USB (Linux của laptop); `xe-monitor.py` (nhiệt/công suất CPU, iGPU) và `xe-freq.c` (xung thực, loại nhân) chạy trên macOS; ocvalidate |
| `.claude/` | Skill/quy tắc cho Claude Code dùng khi phát triển dự án |

## Ghi công và giấy phép

- [JulioNectar/Hackintosh-XPS13Plus-IrisXe-Tahoe](https://github.com/JulioNectar/Hackintosh-XPS13Plus-IrisXe-Tahoe) —
  stack đồ hoạ (driver TGL 16.0.32, NootedGreen bản sửa, libxedrv). Các bản vá trong `patches/` là sửa đổi của
  **NootedGreen** ([sgiammori/NootedGreen](https://github.com/sgiammori/NootedGreen)), theo giấy phép
  **Thou Shalt Not Profit License 1.0** — chỉ dùng phi lợi nhuận.
- [acidanthera](https://github.com/acidanthera) (OpenCore, Lilu, VirtualSMC, WhateverGreen, …),
  [laobamac/itlwm](https://github.com/laobamac/itlwm) (AirportItlwm-Tahoe 2.4.0), [CloverHackyColor/VoodooHDA](https://github.com/CloverHackyColor/VoodooHDA),
  [kgp-macPro](https://github.com/kgp-macPro) (AirportItlwm-Tahoe 1.x, OCLP-CustoMac — dùng tới build-44),
  [Mieze](https://github.com/Mieze/RTL8111_driver_for_OS_X), [lzhoang2801/VoodooI2C](https://github.com/lzhoang2801/VoodooI2C),
  [b00t0x](https://github.com/b00t0x/CpuTopologyRebuild), [USBToolBox](https://github.com/USBToolBox/kext),
  [averycblack/ECEnabler](https://github.com/averycblack/ECEnabler),
  [lshbluesky/IntelBluetoothFirmware](https://github.com/lshbluesky/IntelBluetoothFirmware) (fork của OpenIntelWireless).
- Tham khảo: [cheseecake/i3-1220p-macos-gpu](https://github.com/cheseecake/i3-1220p-macos-gpu),
  [khucxtriendev/irisxegraphic-i712800h-efi](https://github.com/khucxtriendev/irisxegraphic-i712800h-efi),
  [sulthonuladib/victus-15-fa0xxx-hackintosh](https://github.com/sulthonuladib/victus-15-fa0xxx-hackintosh).
- Repo này không phân phối binary của Apple. Driver Tiger Lake do `install.sh` của JulioNectar tải về trên máy bạn.
