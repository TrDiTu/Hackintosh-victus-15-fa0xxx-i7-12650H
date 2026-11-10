# Hackintosh HP Victus 15-fa0xxx (i7-12650H, UHD 64 EU) — macOS 26.7.1 (25G241) with Metal acceleration

OpenCore EFI and NootedGreen patches for the **HP Victus 15-fa0xxx** (board `8A4F`, i7-12650H, iGPU `8086:46A3`
Alder Lake-P GT1 UHD 64 EU, RTX 3050 Ti switched off) running **macOS 26.7.1 Tahoe (25G241)** with
**Metal 2 acceleration** on the iGPU.

This is the `main` branch: the stable route, built on the
[JulioNectar](https://github.com/JulioNectar/Hackintosh-XPS13Plus-IrisXe-Tahoe) Tiger Lake driver stack. The
[`whateverxe-dual-gpu`](../../tree/whateverxe-dual-gpu) branch is an experimental alternative that uses WhateverXe for
the iGPU and the NullMoth driver for the RTX 3050 Ti (HDMI output, H.264 hardware decode, macOS 26.7.2).

## Summary

The well-known boot panic `IOAccelTask::release ← IGAccelTask::withOptions` (CR2 `0xc78`, JulioNectar #13 and #24) has
a specific cause on this laptop. Apple's Tiger Lake driver decodes **GGC.GMS values 0xF0–0xFE in 32 MB units**, but on
Gen9 and later they are 4 MB units. The 60 MB of stolen memory becomes 8128 MB, the GPU virtual address range is
invalid, and `IGAccelTask::initAllocators` fails. The Tiger Lake framebuffer has the same decoding error.

Four small patches fix it here (see [Problems fixed and their causes](#problems-fixed-and-their-causes)): GMSFIX
(accelerator), GMSFIX-FB (framebuffer), PAVPFIX and FENCEFIX. If your laptop has a fixed DVMT below 64 MB and shows the
same panic, these patches are likely relevant.

What you get:

- A desktop with Metal 2 at 1920×1080 @ 144 Hz.
- Wi-Fi 6, Bluetooth, brightness control, audio, webcam, touchpad gestures and battery status.
- **No OCLP root patch** since build-45.
- CPU performance at 92 % / 95 % of Linux on the same laptop: Geekbench 7 **2030 / 9646** against 2195 / 10101, up
  from 1076 / 5837, through NootedGreen XE-PM and a new **XE-HWPAUTO** patch.
- Boot picker to login window in 23 s.

Not working: hardware video decode, the Geekbench 7 GPU run (hangs in Feature Matching), system sleep, external
displays and DRM video. Metal 3 is not reachable on this route.

## Status (build-48, 2026-11-07)

| Item | Status |
|---|---|
| Boots macOS 26.7.1 (25G241) | ✅ |
| **iGPU acceleration** | ✅ **Metal 2**, 1920×1080 @ 144 Hz, 64 EU (`xe-topo` 16390), correct cursor |
| Wi-Fi Intel AX210 | ✅ **laobamac AirportItlwm-Tahoe v2.4.0-alpha** (as used by JulioNectar), **Wi-Fi 6** (`itlwm_he=1`). It uses Tahoe's own IO80211Family/IOSkywalkFamily, so **no root patch is needed**. No AirDrop/AWDL, no WPA3-only networks |
| Ethernet RTL8111 | ✅ RealtekRTL8111 **2.4.2** (3.0.0 does not work on this laptop) |
| PS/2 keyboard, ELAN0788 touchpad (I2C, GPIO interrupt) | ✅ multi-touch gestures |
| Bluetooth AX210 | ✅ IntelBluetoothFirmware 2.5.3 (lshbluesky fork) + BlueToolFixup |
| Screen brightness | ✅ full-range slider (SSDT-PNLF + `ngreenblmax=17741`) |
| Audio ALC245 | ✅ **VoodooHDA 3.6.8** in `/Library/Extensions`, **no root patch**; the owner finds it more stable than AppleHDA through a root patch. ⚠️ The 3.5 mm jack plays the left channel only, a hardware fault of this unit (Linux shows it too) |
| Battery, CPU temperature, brightness keys | ✅ |
| **CPU performance** | ✅ Geekbench 7 **2030 / 9646** = 92 % / 95 % of Linux on the same laptop (XE-PM + XE-HWPAUTO; 1076 / 5837 before) — [`docs/PERFORMANCE.md`](docs/PERFORMANCE.md) |
| iGPU (Geekbench 7 Metal) | ⚠️ 1094 once (build-33). Since build-37 the **Feature Matching** workload hangs the GPU (render and compute both hang, and the compute stamp never returns after the reset), so the run cannot finish — [`docs/BUILD-LOG.md`](docs/BUILD-LOG.md) |
| Boot time | ✅ picker to login window in **23 s** (38 s before) with `gfxrst=1`; the screen blanks briefly while the driver starts |
| Vulkan | ✅ Vulkan 1.4 through **MoltenVK** (LunarG Vulkan SDK; `vulkaninfo` sees the iGPU, `vkcube` runs). No geometry shaders, no float64 |
| USB | ✅ both USB-A ports have USB 3 (SS01/SS02, mapped from Linux with `tools/map-usb-linux.sh`). USB-C runs through the TB4 controller that macOS detects itself (speed not measured) |
| Booting without the USB stick | ✅ OpenCore on the NVMe ESP, next to Limine (CachyOS) — [`docs/POSTINSTALL-RUNBOOK.md`](docs/POSTINSTALL-RUNBOOK.md) §4 |
| dGPU RTX 3050 Ti | ⛔ switched off by an SSDT; **HDMI is unusable** because it is wired to the dGPU. The `whateverxe-dual-gpu` branch runs it with the NullMoth driver |
| HP Wide Vision HD camera (`30C9:0069`) | ✅ macOS's built-in UVC driver |
| RTS5228 card reader | ❌ no driver — see [`docs/DEFERRED.md`](docs/DEFERRED.md) |
| Hardware video decode (H.264/HEVC) | ❌ `-ngreengva` panics at NULL+0x284 in `VTDecoderXPCService` when the decode context is created. Turning PAVPFIX off to test panics at boot (`PAVPCommandCallback`). Video is decoded on the CPU |
| Sleep, external displays, DRM video (PAVP) | ❌ not supported by this stack |

Display sleep and wake work. Minor faults seen so far:

- The blit engine (BCS) hangs about 30–60 s after each boot; macOS recovers on its own.
- One divide-by-zero panic in `fbTimingsWorker` (`-ngreenfixbootmode`) at boot.

## Warnings — read before use

- **Lowered security.** SIP is `0x0A13` and AMFI is off (`amfi_get_out_of_my_way=1`; the graphics stack needs it).
  Use this on a personal machine only.
- **Do not update macOS.** The graphics stack is tied to exactly 25G241 (the laobamac Wi-Fi kext loads only on
  Darwin 25); an update can break it.
- GPU hangs and kernel panics are possible. Always keep a non-accelerated EFI to fall back to
  (`EFI/OC/config-install.plist` or a base build).
- The EFI in this repo uses **placeholder SMBIOS values** (`CHANGE_ME_*`). Generate your own serials and never commit
  real ones.
- Since build-48 the EFI contains no OCLP-CustoMac kexts (`IOSkywalkFamily`, `IO80211FamilyLegacy`, `AMFIPass`):
  Wi-Fi and audio need no root patch.

## Hardware

| | |
|---|---|
| Laptop | HP Victus 15-fa0xxx, board `8A4F`, BIOS F.34 |
| CPU | Intel Core i7-12650H (6P + 4E, 16 threads) |
| iGPU | `8086:46A3` rev 0c, UHD 64 EU (1 slice, 4 DSS with mask `0x33`, 6 L3 banks), **fixed 60 MB DVMT** (GGC `0xFEC1`, GMS `0xFE`) |
| dGPU | `10DE:25A0` RTX 3050 Ti (`\_SB.PC00.PEG1.PEGP`) |
| Display | eDP 1920×1080 144 Hz on the iGPU |
| Wi-Fi / BT | Intel AX210 `8086:2725` / `8087:0032` |
| Ethernet | Realtek RTL8111 `10EC:8168` |
| Touchpad | ELAN0788 (I2C0 `8086:51E8`) |
| SSD | SK hynix BC711 256 GB |
| Audio | Realtek ALC245 (subsystem `103C8A4F`), HDA `\_SB.PC00.HDAS` = `PciRoot(0x0)/Pci(0x1f,0x3)` |

Details: [`laptop-specs.md`](laptop-specs.md) (in Vietnamese).

## EFI configuration (build-48)

- **OpenCore 1.0.8**, SMBIOS `MacBookPro16,2`.
- **SSDTs** (written from this laptop's DSDT, sources in [`docs/acpi-src/`](docs/acpi-src/)): PLUG-ALT, EC-USBX, AWAC,
  XOSI (with the `_OSI`→`XOSI` patch), **DGPU-OFF** (powers the RTX 3050 Ti off), SBUS-MCHC and **PNLF**. PNLF adds a
  backlight device under `PC00.GFX0`; the firmware has none, and without it macOS shows no brightness slider.
- **Kexts:** Lilu, VirtualSMC (+SMCProcessor, SMCBatteryManager), ECEnabler, WhateverGreen, **NootedGreen (patched)**,
  AppleALC 1.9.8, RestrictEvents, CpuTopologyRebuild, NVMeFix, BrightnessKeys, RealtekRTL8111 2.4.2,
  **AirportItlwm-Tahoe v2.4.0-alpha (laobamac)**, IntelBluetoothFirmware + IntelBTPatcher 2.5.3 (lshbluesky fork),
  BlueToolFixup 2.7.2, XHCI-ADL-Injector (written for this project; Info.plist only, for `8086:51ED`),
  USBToolBox + UTBMap (HS01/02/04/06/07 + SS01/02), VoodooPS2 (keyboard), VoodooI2C 3.0.0 (lzhoang2801 fork) +
  VoodooI2CHID.
- **Device properties:**

  | Device | Setting |
  |---|---|
  | iGPU | Spoofed as Tiger Lake: `device-id 9A49`, `AAPL,ig-platform-id 0x9A490000` (as JulioNectar does) |
  | dGPU | `disable-gpu` plus the SSDT |
  | Touchpad | GPIO interrupt (`TPD0._CRS` returns GpioInt thanks to SSDT-XOSI; no `force-polling`) |
  | Audio | `layout-id` 11 on `PciRoot(0x0)/Pci(0x1f,0x3)` |
  | Bluetooth | NVRAM `bluetoothExternalDongleFailed`, `bluetoothInternalControllerInfo` |

- **CPU (NootedGreen XE-PM, `-ngreenpm`):** corrects HWP turbo on hybrid CPUs, sets EPP 0, turns energy-efficient turbo
  off, and puts PCI devices without a driver into D3. Since patch v9, `-ngreenpm` also turns **XE-HWPAUTO** on and keeps
  XCPM's original C-state table (C8/C10 lower the multi-core score), so `ngreenpmauto=1 ngreenpmcst=0` are no longer
  needed; both can still be overridden. CpuTopologyRebuild stays at its default (6 cores / 16 threads; `ctrsmt=off`
  measured worse). PL1 stays at the BIOS value.
- **Notable quirks:** `SetupVirtualMap = true` (without it the laptop hangs at `EXITBS:START`), `AppleXcpmCfgLock`
  (CFG Lock is on and the BIOS has no option for it), `DisableIoMapper = true`, `ProvideCurrentCpuInfo`.
- **boot-args** (160 characters):
  ```
  -ngreenpm -ngreentglwithgfx -allow3d -disablegfxfirmware -ngreenv189 -ngreenkeepefi -ngreenxefix -ngreenfixbootmode amfi_get_out_of_my_way=1 gfxrst=1 itlwm_he=1
  ```
  - `itlwm_he=1` turns Wi-Fi 6 (802.11ax) on in the laobamac AirportItlwm; it is off by default.
  - `gfxrst=1` (WhateverGreen) clears the boot screen instead of copying it through slow memory, which saves 15 s.
  - Patch v10 builds this laptop's values in as defaults: **64 EU / 6 L3 banks** topology, `ngreenV142=3`,
    `ngreenblmax=17741` and `ngreen-dmc=adlp` (hard-coded, the fuses are not read). The boot-args of the same names
    still override them.
  - Two length limits apply. **Lilu keeps only about the first 228 characters** for flags read with
    `checkKernelArgument` (`-ngreen*` and similar). **The kernel keeps 255** for parameters read with
    `PE_parse_boot_argn` (`gfxrst`, `itlwm_he`, `ngreen-eu` and similar). Check the position when you add a flag.

## Problems fixed and their causes

The patches are in [`patches/`](patches/) and apply to JulioNectar's NootedGreen source at **`24450b4`** (since
build-38; `6f03560` before that). The one in use is **`patches/nootedgreen-gmsfix-v10-jn24450b4.patch`**: v8, plus the
XE-PM defaults of v9, plus the machine defaults of v10, including the diagnostic logging. The v8 patch for JulioNectar
`6f03560` is kept as `patches/nootedgreen-gmsfix-v8-jn6f03560.patch`. The history and the measurement for each step are
in [`docs/BUILD-LOG.md`](docs/BUILD-LOG.md) (build-12 to build-43, in Vietnamese).

| # | Symptom | Cause | Fix |
|---|---|---|---|
| 1 | `ngreen-*` boot-args have no effect | The 291-character string was cut off (Lilu keeps about 228) | Shortened to 224 characters, graphics parameters first |
| 2 | Panic `IOAccelTask::release ← IGAccelTask::withOptions`, CR2 `0xc78`, at about 54 s | The TGL driver (`IGMemoryManager::initSegments`) decodes GMS `0xFE` as 8128 MB (32 MB units) instead of 60 MB (the 4 MB units of Gen9+). The GPU VA range is wrong and `initAllocators` fails | **GMSFIX**: replace the decode with the real stolen-memory size |
| 3 | WindowServer panic `IOFramebuffer::getAttributeExt+0x25` (NULL) | The TGL framebuffer (`FBMemMgr_Init`) makes the same decoding error (4032 MB), so `AppleIntelFramebufferController` is never registered and the accelerator runs "standalone" | **GMSFIX-FB**: the same fix in the framebuffer |
| 4 | Panic `IntelAccelerator::PAVPCommandCallback`, CR2 `0xb8` | The BIOS enables PAVP (MMIO `0x1082C0`) but no PAVP context is created, so a pointer is NULL | **PAVPFIX**: always take the "PAVP disabled" path (DRM video playback is lost) |
| 5 | The mouse cursor breaks up into bands | The framebuffer's X-tile fence is 64 MB long (per Apple's table). It runs past the 60 MB of stolen memory and covers the cursor buffer placed right after it | **FENCEFIX**: cut the fence at the end of the stolen region |
| 6 | No brightness slider | The firmware has no `PNLF` device (`APP0002`), so macOS attaches `AppleDisplay` instead of `AppleBacklightDisplay` | A minimal **SSDT-PNLF** (it writes no PWM registers) |
| 7 | Maximum brightness is only about 18.5 % | macOS does not write the PWM period (`bl hw=96000 apple=0`), so its maximum duty of 17741 goes straight to the hardware | `ngreenblmax=17741` (XE-BLR, already in JulioNectar's NootedGreen; the default since v10, no boot-arg needed) |
| 8 | Geekbench 7 at only about 54 % of Linux; P-cores stuck near 3.8 GHz | XCPM writes wrong HWP limits on hybrid CPUs | `-ngreenpm` (JulioNectar's XE-PM): single-core +13 % |
| 9 | Multi-core drops when XE-PM is on | The C8/C10 states that XE-PM enables | `ngreenpmcst=0`: multi-core 5476 → 7114 |
| 10 | Single-core still about 54 % of Linux; a single thread loses clock speed in bursts | XNU moves the thread across several P-cores. Each time, XCPM writes a low HWP "desired" value for the new core and raises it only at the next control period | **XE-HWPAUTO** (patch v8): desired = 0, so each core picks its own clock. Geekbench 7 1191 / 5637 → **2030 / 9646** |
| 11 | boot-args full at 255, no room for a new flag | Every tweak was a boot-arg | **v9**: `-ngreenpm` defaults to HWPAUTO on and C8/C10 off. **v10**: the laptop's topology/V142/blmax/dmc values become defaults. 255 → 163 characters |
| 12 | 38 s boot | WhateverGreen copies the boot screen (FB_COPY) through uncached memory by default | `gfxrst=1` (as JulioNectar does): 23 s |

Every patch can be turned off with a boot-arg (`-ngreennogmsfix`, `-ngreennopavpfix`, `-ngreennofencefix`). XE-HWPAUTO
can be switched live with `sudo sysctl -w debug.xepm.hwpauto=0|1`. Diagnostic values:
`ioreg -rc IntelAccelerator -d1 | grep -E 'xe-cur|xe-fence|xe-mm'`.

## Installation (outline)

1. Install macOS 26.7.1 (25G241) with the **non-accelerated** EFI (rename `EFI/OC/config-install.plist` to
   `config.plist`). BIOS: Secure Boot off.
2. **No root patch is needed.** Wi-Fi works at once with the laobamac AirportItlwm in the EFI. For audio, install
   VoodooHDA 3.6.8 into `/Library/Extensions` and approve it in Privacy & Security —
   [`docs/POSTINSTALL-RUNBOOK.md`](docs/POSTINSTALL-RUNBOOK.md) §7. The older route through OCLP-CustoMac Modern
   Wireless and Modern Audio is in §1, §5 and §6.
3. Install the JulioNectar graphics stack at `24450b4` (`zsh install.sh`; the `9A49` spoof must be active during
   the install). Apply the patch before running it, because `install.sh` also builds NootedGreen —
   [`docs/GRAPHICS-RUNBOOK.md`](docs/GRAPHICS-RUNBOOK.md).
4. Apply the patch and build NootedGreen on the laptop itself — [`docs/GMSFIX-RUNBOOK.md`](docs/GMSFIX-RUNBOOK.md):
   ```
   cd ~/xe-stack && git checkout 24450b476d7ca025b83c85d7b8362caf3234d2f2 && git apply nootedgreen-gmsfix-v10-jn24450b4.patch && zsh build-nootedgreen.sh
   ```
   Then copy `build/NootedGreen.kext` into `EFI/OC/Kexts/`.
5. Put your own SMBIOS values (serial, MLB, UUID, ROM) into your `config.plist`.
6. (Optional) To boot without the USB stick, copy `EFI/OC` to the internal drive's ESP **from Linux** and create the
   boot entry with `efibootmgr` — [`docs/POSTINSTALL-RUNBOOK.md`](docs/POSTINSTALL-RUNBOOK.md) §4.

The runbooks under `docs/` are written in Vietnamese.

## Repository layout

| Path | Contents |
|---|---|
| `EFI/` | Current OpenCore EFI (build-48), placeholder SMBIOS |
| `patches/` | NootedGreen patches (cumulative `vN-jn24450b4` / `vN-jn6f03560`, incremental `vN-to-vM`) |
| `docs/STATE.md`, `docs/BUILD-LOG.md` | Current state and the log of every build |
| `docs/GRAPHICS-PROGRESS.md` | Progress of the graphics work |
| `docs/PERFORMANCE.md` | CPU and iGPU measurements, comparison with Linux, each improvement step |
| `docs/ROADMAP.md` | Goals after build-37 (G1–G4) and their results |
| `logs/` | Panic and GPU restart reports (serials removed) used for analysis |
| `docs/DRIVER-MATRIX.md`, `docs/SOURCES.md` | Vetted drivers, sources, versions, SHA-256 |
| `docs/*-RUNBOOK.md` | Step-by-step guides to run on the laptop |
| `docs/acpi-src/` | SSDT sources |
| `tools/` | Hardware dump and USB port mapping (run under Linux on the laptop); `xe-monitor.py` (CPU and iGPU temperature and power) and `xe-freq.c` (real clock speed, core type) run on macOS; ocvalidate |
| `.claude/` | Skills and rules used by Claude Code while developing this project |

## Credits and licenses

- [JulioNectar/Hackintosh-XPS13Plus-IrisXe-Tahoe](https://github.com/JulioNectar/Hackintosh-XPS13Plus-IrisXe-Tahoe) —
  the graphics stack (TGL driver 16.0.32, the modified NootedGreen, libxedrv). The patches in `patches/` modify
  **NootedGreen** ([sgiammori/NootedGreen](https://github.com/sgiammori/NootedGreen)) and are under the
  **Thou Shalt Not Profit License 1.0** — non-profit use only.
- [acidanthera](https://github.com/acidanthera) (OpenCore, Lilu, VirtualSMC, WhateverGreen and others),
  [laobamac/itlwm](https://github.com/laobamac/itlwm) (AirportItlwm-Tahoe 2.4.0),
  [CloverHackyColor/VoodooHDA](https://github.com/CloverHackyColor/VoodooHDA),
  [kgp-macPro](https://github.com/kgp-macPro) (AirportItlwm-Tahoe 1.x and OCLP-CustoMac, used up to build-44),
  [Mieze](https://github.com/Mieze/RTL8111_driver_for_OS_X), [lzhoang2801/VoodooI2C](https://github.com/lzhoang2801/VoodooI2C),
  [b00t0x](https://github.com/b00t0x/CpuTopologyRebuild), [USBToolBox](https://github.com/USBToolBox/kext),
  [averycblack/ECEnabler](https://github.com/averycblack/ECEnabler),
  [lshbluesky/IntelBluetoothFirmware](https://github.com/lshbluesky/IntelBluetoothFirmware) (a fork of OpenIntelWireless).
- References: [cheseecake/i3-1220p-macos-gpu](https://github.com/cheseecake/i3-1220p-macos-gpu),
  [khucxtriendev/irisxegraphic-i712800h-efi](https://github.com/khucxtriendev/irisxegraphic-i712800h-efi),
  [sulthonuladib/victus-15-fa0xxx-hackintosh](https://github.com/sulthonuladib/victus-15-fa0xxx-hackintosh).
- This repo does not distribute Apple binaries. The Tiger Lake driver is downloaded on your own machine by
  JulioNectar's `install.sh`.
