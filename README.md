# Hackintosh HP Victus 15-fa0xxx (i7-12650H, UHD 64 EU + RTX 3050 Ti) — macOS 26 Tahoe with WhateverXe and NullMoth

OpenCore EFI for the **HP Victus 15-fa0xxx** (board `8A4F`, i7-12650H, iGPU `8086:46A3` Alder Lake-P UHD 64 EU,
dGPU RTX 3050 Ti `10DE:25A0`) running **macOS 26.7.2 Tahoe (25G332)**.

The iGPU uses [WhateverXe](https://github.com/b00t0x/WhateverXe) and the dGPU uses the
[NullMoth NVIDIA driver](https://github.com/nullmoth/nvidia-macos-driver). This is the project's current setup. It is still experimental and has not been through long-term testing.

The project's earlier route (NootedGreen and the JulioNectar stack, dGPU off, macOS 26.7.1, build-48) is no longer installed or maintained on the laptop. Its EFI, patches and documentation are kept in the [`jn-driver`](../../tree/jn-driver) branch.

## Summary

This iGPU has **only VCS2**: the GT fuse reports video mask 4, and VCS0 is fused off. Stock WhateverXe rejects such
parts (`ProfileMismatch`, upstream issue #76), so the panel runs without acceleration. A self-built fork
([TrDiTu/WhateverXe](https://github.com/TrDiTu/WhateverXe), branch `katana-46a3`, based on tag 0.7.0) adds:

- an opt-in flag, `-wex-adlp-allow-vcs2`;
- a VBT fix for the eDP panel;
- a PAVP-disabled path;
- two patches that move Apple's Tiger Lake media path from VCS0 to VCS2.

Result: Metal acceleration on the internal panel (1920×1080 @ 144 Hz), **H.264 hardware decode on VCS2**, the
RTX 3050 Ti visible to macOS with **HDMI output**, and CPU performance close to Linux (Geekbench 7 2035 / 9320) through HybridPM plus an XE-HWPAUTO port.

Not working: the Geekbench 7 Metal GPU run on the iGPU (hangs in Feature Matching) and DRM video.

Untested: HEVC, long-term stability.

## Status (build-70, 2026-11-10)

| Item | Status |
|---|---|
| Boots macOS 26.7.2 (25G332) | ✅ |
| **iGPU `46A3` acceleration** | ✅ Metal 2, 1536 MB VRAM, internal panel at 1920×1080 @ 144 Hz (WhateverXe 0.7.0-katana r7 + WhateverXe-Graphics 0.4.0) |
| **H.264 hardware decode** | ✅ on VCS2: 1080p at 3 ms per frame, 0 dropped frames (build-66). HEVC and encode are untested |
| **dGPU RTX 3050 Ti** | ✅ NullMoth 2.9 detects the GPU with 4 GB VRAM; System Information reported Metal 4 when the GPU was started by hand |
| **HDMI** (wired to the dGPU) | ✅ shows a picture on build-70 (confirmed by the owner; no log saved in the repo yet) |
| **CPU performance** | ✅ Geekbench 7 **2035 / 9320** with HybridPM and XE-HWPAUTO (build-70), about 93 % / 92 % of Linux on the same laptop (2195 / 10101). Before HybridPM: 999 / 4658; HybridPM without XE-HWPAUTO: 1176 / 4888 |
| **iGPU compute (Geekbench 7 OpenCL)** | ✅ **7598** on the iGPU (reported by the owner; no log saved in the repo) |
| **iGPU compute (Geekbench 7 Metal)** | ❌ hangs in the Feature Matching workload, and the watchdog restarts WindowServer. Same pattern as WhateverXe #25, #40 and #44 |
| Vulkan | ✅ MoltenVK 1.4.2 (LunarG SDK 1.4.363.1) sees the iGPU |
| Audio (ALC245) | ✅ VoodooHDA 3.6.8 in `/Library/Extensions`; NullMoth's `NMXAudio.kext` must be disabled |
| DRM video (FairPlay/PAVP) | ❌ the PAVP path is forced off to avoid a panic |
| Sleep/wake | ❌ not working |
| Wi-Fi AX210, Bluetooth, Ethernet, keyboard, touchpad, USB, camera, battery | Same kexts and settings as the earlier NootedGreen setup, where they worked; not rechecked one by one with this setup |


The build marked as known-good is **build-63** (Metal on the iGPU, software video decode, dGPU not started).

## Warnings — read before use

- These config and drivers are only used for the **HP Victus 15 fa0xxx with an i7-12650H**
- **Lowered security.** SIP is `0x0A53` and AMFI is off (`amfi_get_out_of_my_way=0x1`, `amfi=0x80`, AMFIPass).
  Unsigned kexts and binaries can run.
- **Experimental.** GPU hangs, hard freezes and kernel panics are possible. Keep a way back: the non-accelerated EFI
  (`EFI/OC/config-install.plist`) and a snapshot of the last EFI that booted.
- **Do not update macOS** without checking first. WhateverXe-Graphics, HybridPM's XCPM hook and NullMoth are all tied
  to the macOS build.
- The EFI in this repo uses **placeholder SMBIOS values** (`CHANGE_ME_*`). Generate your own serials and never commit
  real ones.
- The repo **does not contain** `AMFIPass.kext` (it has no redistribution license) or any Apple binaries. The EFI here
  is therefore one kext short of the running setup; get AMFIPass as described in [`docs/SOURCES.md`](docs/SOURCES.md).


## Hardware

| | |
|---|---|
| Laptop | HP Victus 15-fa0xxx, board `8A4F`, BIOS F.34 |
| CPU | Intel Core i7-12650H (6P + 4E, 16 threads), PL1 45 W |
| iGPU | `8086:46A3` rev 0c, UHD 64 EU (1 slice, 4 DSS with mask `0x33`, 6 L3 banks), fixed 60 MB DVMT. GT fuse `0x000E00FB`: **VCS2 only**, VCS0 is fused off |
| dGPU | `10DE:25A0` RTX 3050 Ti (Ampere GA107, 4 GB); wired to HDMI port |
| Display | eDP 1920×1080 144 Hz on the iGPU |
| Wi-Fi / BT | Intel AX210 `8086:2725` / `8087:0032` |
| Ethernet | Realtek RTL8111 `10EC:8168` |
| Touchpad | ELAN0788 (I2C) |
| Audio | Realtek ALC245 |

Details: [`laptop-specs.md`](laptop-specs.md) (in Vietnamese).

## Why a WhateverXe fork is needed

Stock WhateverXe reads the GT fuses and accepts only parts with VCS0 (video mask 1 or 5). This laptop reports mask 4,
so it is rejected. The fork [TrDiTu/WhateverXe](https://github.com/TrDiTu/WhateverXe), branch `katana-46a3` (based on tag 0.7.0, BSD-3-Clause), adds these changes in order:

| Revision | Change | Result on this laptop |
|---|---|---|
| r1 | VBT patch from issue #35 and the opt-in flag `-wex-adlp-allow-vcs2` | Passes the fuse check |
| r2 | VBT: prefer eDP on DDI A, accept `panel_type` 0xFF | The framebuffer starts and the internal panel lights up |
| r3 | Force the "PAVP disabled" path in `PAVPCommandCallback` | No more NULL+0xb8 panic; **Metal works** (build-62) |
| r4 | VCS2-only parts: hide hardware video decode | No more `VTDecoderXPCService` panic (build-63, stable) |
| r5 | Point the Apple driver's VideoMedia parameters at VCS2 (type 4, instance 2) | Decode runs, but at about 1 s per frame |
| r6 | Diagnostic counters for VCS interrupts | VCS2 interrupts arrive, but the driver does not pick them up |
| r7 | Replace the VCS interrupt read with one that follows Linux i915 | **H.264 at 3 ms per frame** (build-66) |

Each revision has its zip, SHA-256 and source notes in [`kexts-custom/`](kexts-custom/). The history and measurements are in [`docs/BUILD-LOG.md`](docs/BUILD-LOG.md) (build-59 to build-70, in Vietnamese).

CPU: [HybridPM](https://github.com/Thatisjigen/HybridPM) corrects XCPM's HWP limits on hybrid CPUs. The fork [TrDiTu/HybridPM](https://github.com/TrDiTu/HybridPM), branch `victus`, adds **XE-HWPAUTO** (HWP desired = 0, so each core picks its own clock). It is on by default; turn it off with `hpmauto=0` or
`sudo sysctl -w debug.hybridpm.hwpauto=0`.

## EFI configuration (build-70)

- **OpenCore 1.0.8**, SMBIOS `MacBookPro16,2`.
- **SSDTs** (written from this laptop's DSDT, sources in [`docs/acpi-src/`](docs/acpi-src/)): PLUG-ALT, EC-USBX, AWAC,
  XOSI, SBUS-MCHC, PNLF. `SSDT-DGPU-OFF` is **disabled** (the dGPU must stay powered).
- **Kexts:** Lilu, **HybridPM** (fork), **AMFIPass** (not in the repo), VirtualSMC (+SMCProcessor, SMCBatteryManager),
  ECEnabler, **WhateverXe** (fork r7), AppleALC, RestrictEvents, CpuTopologyRebuild, NVMeFix, BrightnessKeys,
  RealtekRTL8111, AirportItlwm (laobamac), IntelBluetoothFirmware + IntelBTPatcher, BlueToolFixup, XHCI-ADL-Injector,
  USBToolBox + UTBMap, VoodooPS2, VoodooI2C + VoodooI2CHID.
- **iGPU:** no device-id spoof. Only `framebuffer-patch-enable`, `framebuffer-stolenmem` = `0000C003` (60 MB),
  `enable-max-pixel-clock-override` and `built-in`.
- **dGPU:** no `disable-gpu`.
- **boot-args** (214 characters):
  ```
  -v keepsyms=1 debug=0x100 -allow3d -disablegfxfirmware -igfxdvmt amfi_get_out_of_my_way=0x1 amfi=0x80 ipc_control_port_options=0 nvfb=1 nvaccel=1 nvfbheads=4 -nvkmsnosmooth itlwm_he=1 -wex-adlp-allow-vcs2 hpmpl1=55
  ```

  | Arguments | Purpose |
  |---|---|
  | `-allow3d -disablegfxfirmware -igfxdvmt -wex-adlp-allow-vcs2` | WhateverXe |
  | `amfi=0x80 ipc_control_port_options=0 nvfb=1 nvaccel=1 nvfbheads=4 -nvkmsnosmooth` | NullMoth |
  | `hpmpl1=55` | HybridPM sets PL1 to 55 W in MCHBAR; whether it takes effect has not been measured |
  | `itlwm_he=1` | Wi-Fi 6 |
  | `-v keepsyms=1 debug=0x100` | Diagnostics; can be removed |

  Lilu keeps only about the first 228 characters for flags read with `checkKernelArgument`.

## Installation (outline)

If the laptop already has a working macOS install, try this on a separate APFS volume first.

1. Install macOS 26 Tahoe with the non-accelerated EFI (rename `EFI/OC/config-install.plist` to `config.plist`).
   BIOS: Secure Boot off.
2. In macOS, install **WhateverXe-Graphics 0.4.0** (the `.pkg` from b00t0x's releases; SHA-256
   `7a1b5015b3e6e8b522f26c25df85c313471c9142564a0b57356cddd2c88b9510`). It installs the Tiger Lake driver into `/Library`.
3. Install **VoodooHDA 3.6.8** into `/Library/Extensions` for audio.
4. Install **NullMoth 2.9** with `install.sh` (run it with `CHECK=1` first). Then **disable `NMXAudio.kext`** and rebuild
   the AuxKC before restarting — see [`docs/NVIDIA-VULKAN-STEPS.md`](docs/NVIDIA-VULKAN-STEPS.md) (in Vietnamese).
   Do not use the 1401 app: it edits OpenCore on its own.
5. Copy `AMFIPass.kext` into `EFI/OC/Kexts/`, put your own SMBIOS values into `config.plist`, and boot with this
   repo's EFI.
6. If HDMI stays dark and System Information lists the NVIDIA card as "Metal 2", NullMoth's boot guard has switched the
   display part off. Clear its counter and restart:
   ```bash
   sudo nvram -d 7C436110-AB2A-4BBB-A880-FE41995C9F82:nullmoth-nv-starts
   ```
7. (Optional) Vulkan: install the LunarG Vulkan SDK and check it with `vulkaninfo --summary` and `vkcube`.

The earlier experimental steps (build-55) are in [`docs/WEX-NULLMOTH-RUNBOOK.md`](docs/WEX-NULLMOTH-RUNBOOK.md).

## Next steps

[`docs/ROADMAP.md`](docs/ROADMAP.md): stability testing of build-70, a new CPU measurement, sleep/wake, HEVC and encode,
`nmhybrid`, porting the patches to WhateverXe 0.8.x and sending them upstream. The older roadmap for the JulioNectar
route is in [`docs/ROADMAP-JN.md`](docs/ROADMAP-JN.md).

## Repository layout

Most documents under `docs/` are written in Vietnamese.

| Path | Contents |
|---|---|
| `EFI/` | Current OpenCore EFI (build-70), placeholder SMBIOS, no AMFIPass |
| `config/`| Config USB path |
| `kexts-custom/` | Self-built WhateverXe 0.7.0-katana r1–r7 and HybridPM: zips, SHA-256, source notes, diff against the upstream tag |
| `docs/STATE.md`, `docs/BUILD-LOG.md` | Current state and the log of every build |
| `docs/ROADMAP.md` | Plan for the WhateverXe route |
| `docs/NVIDIA-VULKAN-STEPS.md`, `docs/WEX-NULLMOTH-RUNBOOK.md` | Steps to run on the laptop for NullMoth, Vulkan and WhateverXe |
| `docs/DRIVER-MATRIX.md`, `docs/SOURCES.md` | Vetted drivers, sources, versions, SHA-256 |
| `docs/PERFORMANCE.md` | CPU and iGPU measurements from the earlier NootedGreen setup (the comparison baseline) |
| `docs/acpi-src/` | SSDT sources |
| `patches/` | NootedGreen patches from the earlier setup (not used by the current EFI) |
| `secrets/` | SMBIOS information example, use your own information and change it to `smbios.json`  |
| `logs/` | Panic reports and logs used for analysis |
| `tools/` | Hardware dump and USB mapping scripts, `xe-monitor.py`, `xe-freq.c`, `nvrm-go.c` (starts the NVIDIA GPU by hand) |
| `.claude/` | Skills and rules used by Claude Code while developing this project |

## Credits and licenses

- [b00t0x/WhateverXe](https://github.com/b00t0x/WhateverXe) and WhateverXe-Graphics — the iGPU driver (BSD-3-Clause; derived from acidanthera/vit9696's WhateverGreen). The fork in this repo keeps the same license.
- [nullmoth/nvidia-macos-driver](https://github.com/nullmoth/nvidia-macos-driver) — the NVIDIA driver (PolyForm
  Noncommercial 1.0.0, non-commercial use only). This repo contains no NullMoth binaries.
- [Thatisjigen/HybridPM](https://github.com/Thatisjigen/HybridPM) — derived from XE-PM by [JulioNectar](https://github.com/JulioNectar/Hackintosh-XPS13Plus-IrisXe-Tahoe), under the **Thou Shalt Not Profit
  License 1.0**; the fork with XE-HWPAUTO is under the same license.
- [acidanthera](https://github.com/acidanthera) (OpenCore, Lilu, VirtualSMC, AppleALC and others),
  [laobamac/itlwm](https://github.com/laobamac/itlwm), [CloverHackyColor/VoodooHDA](https://github.com/CloverHackyColor/VoodooHDA),
  [Mieze](https://github.com/Mieze/RTL8111_driver_for_OS_X), [lzhoang2801/VoodooI2C](https://github.com/lzhoang2801/VoodooI2C),
  [b00t0x/CpuTopologyRebuild](https://github.com/b00t0x/CpuTopologyRebuild), [USBToolBox](https://github.com/USBToolBox/kext),
  [averycblack/ECEnabler](https://github.com/averycblack/ECEnabler),
  [lshbluesky/IntelBluetoothFirmware](https://github.com/lshbluesky/IntelBluetoothFirmware).
- References: [khucxtriendev](https://github.com/khucxtriendev/irisxegraphic-i712800h-efi) (ThinkPad P1 Gen 5 with
  WhateverXe) and Linux i915 (Gen12 engine layout and GT interrupt handling).
- This repo does not distribute Apple binaries. The Tiger Lake driver is installed on your machine by the
  WhateverXe-Graphics package.
