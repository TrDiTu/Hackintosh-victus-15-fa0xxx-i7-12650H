# Plan v4: cheseecake/i3-1220p-macos-gpu on the HP Victus 15 (46A3, 64 EU)

> For Claude Code on MÁY A. Save as `docs/PLAN-CHESEECAKE.md` and point to it from `CLAUDE.md`
> (or merge it into `CLAUDE.md`). If the original `CLAUDE.md` held project rules (snapshots, release
> policy, security), restore them: this plan only adds to them and section 1 summarises them.
> Supersedes Plan v3 (IntelIGPU-Tahoe, blocked at Phase 0, see `docs/feasibility.md`).

---

## 0. Situation (from the project files, 2026-11-03)

| Item | State |
|---|---|
| MÁY B | HP Victus 15-fa0xxx (8A4F, BIOS F.34), i7-12650H, iGPU `8086:46A3` rev 0c, macOS **26.7.1 (25G241)** |
| iGPU facts | 1 slice, **4 DSS, mask 0x33 (DSS 0,1,4,5: not contiguous)**, 16 EU/DSS = 64 EU; L3 = 6 (user-provided, not cross-checked); stolen **60 MB fixed** @0x7C800000; BAR2 aperture 256 MB @0x4000000000; panel eDP 1080p (144 Hz user-reported); `intel_backlight` max 96000 |
| dGPU | RTX 3050 Ti off: SSDT-DGPU-OFF + `disable-gpu` + `-wegnoegpu` (WhateverGreen stays) |
| USB MACEFI | **build-10** (known-good, no spoof). `config-install.plist` = build-10 |
| MÁY B software | **JulioNectar user-space stack @6f03560 is still installed** (TGL kexts + HookCase in `/Library/Extensions`, bundles, `xe.bundle`). Root patch Wi-Fi (OCLP-CustoMac 3.0.3) applied |
| JN track result | 4 builds (v1 JN kext, v2 +class-code, r3 khucx kext, v3 `ngreenSched=5`): all panic/hang in `IGAccelTask::withOptions ← IntelAccelerator::start`, CR2 0xc78, ~54 s. graphics-v3 `.panic` **not collected yet** |
| Refs cloned | `_cache/refs/cheseecake` @7881587, `_cache/refs/juliornectar` @6f03560, `_cache/refs/khucxtriendev` @26ee7f3 |

### What cheseecake is (and how far to trust it)
- A JulioNectar fork ported to i3-1220P (`46B3`, 64 EU, 4 DSS) on 25G241. Main logic change: `NumSubSlices` 12 → 8 in two places (load-time byte patch `f3bbb/r3bbb` → IGAccelDevice+0x1158, and runtime `getGPUInfo()`). Overrides: `ngreensubslices`, `ngreenmaxeu`, `ngreenl3banks`. Default L3 = **8**.
- **Credibility is low.** Its `docs/STATUS.md` describes a 3840×2400 panel and SoundWire RT714/RT1316 audio, which is the XPS 13 Plus (copied from JN), and `PORT-I3-1220P.md` lists EU count, L3 and RP0 as UNVERIFIED. No stars, no external testers, no published Metal result on an i3-1220P. Treat it as an experiment, not a known-good stack.
- Prebuilt CI pre-releases exist (Build 12, 16, 17; Build 17 = commit `161c353`, 2026-10-22) with `NootedGreen.kext.zip` and `IrisXe-i3-1220P-tahoe.zip`.

### Two hypotheses this plan tests, in order of cost
- **H1: boot-args were truncated (cheapest, check first).** cheseecake's port guide says "Lilu truncates at ~228 chars — keep it short". The graphics-v1 boot-args string is about 290 characters, and `ngreenSched`, `ngreen-eu=64`, `ngreen-l3=6` sit at the very end. If the limit is real, NootedGreen may never have seen the topology or scheduler args: every JN build ran as 96 EU, and the `ngreenSched=5` test changed nothing. **UNVERIFIED**: confirm or refute from source and logs before booting anything.
- **H2: the load-time subslice byte patch differs.** cheseecake changes the byte patch at load as well as the runtime override. If JN's `ngreen-eu=64` only changes the runtime fields, the driver could start with 12 SS baked in. **UNVERIFIED**: decide from the two source trees.

## 1. Rules (project rules carried over + this plan)

1. **One change per build.** Every build: snapshot (max 10), `efi-validate` (ocvalidate 0 errors / 0 warnings), log to `BUILD-LOG.md` and `GRAPHICS-PROGRESS.md`, deploy only through the USB deploy guard. Next number is **build-17**.
2. **Claude Code writes runbook steps; the user runs them on MÁY B** and returns output. Claude Code never assumes a result.
3. Ask the user before: writing the USB, using a pre-release or non-release asset, any change to SIP/AMFI, uninstalling/installing a graphics stack on MÁY B.
4. **Never boot a spoofed EFI without NootedGreen while TGL kexts are installed** (build-11 hang, JN INSTALL.md). Before every spoofed build, confirm what is installed on MÁY B.
5. Never commit Apple binaries, real SMBIOS, or verbose videos (they contain WPA session keys from itlwm).
6. Don't read this project's own git history (user rule). Reference repos are fine.
7. Don't post upstream unless the user asks (user declined for JN #13). Drafts stay in `docs/`.
8. Mark every claim not checked on this machine as **CHƯA XÁC MINH**.

---

## 2. Phase 0 — Close out the JN track and test H1 (no boot, no USB write)

1. Ask the user to boot build-10 and copy the graphics-v3 `.panic` (+ `log show --last boot` of the panicked boot, if any) into `logs/`. Compare its signature with graphics-v1.
2. **Boot-arg length.**
   - Compute the exact length of the boot-args in build-12/14/15/16.
   - Find the real limit in source: Lilu's boot-arg handling (`checkKernelArgument` / its buffer) in the Lilu version NootedGreen links against, and NootedGreen's own `PE_parse_boot_argn` calls. Record file and line. If it's the XNU limit instead, record that.
   - Search existing evidence for what NootedGreen actually received: `logs/gv2-log.txt`, the `.panic` files, video frames already transcribed. Look for `getGPUInfo`, `subslices`, `totalEU`, `xe-topo`, `ngreenSched`/scheduler type, or any line proving an end-of-string arg was parsed.
   - Result: **H1 confirmed / refuted / undecided**, with evidence.
3. Write `docs/CHESEECAKE-ANALYSIS.md` §A with the above.

**If H1 is confirmed:** stop and report to the user first. The cheapest next test is then **a JN build with the same args reordered so `ngreen*` come first** (one change vs graphics-v1), before any fork swap. Let the user choose between that and continuing to Phase 1.

## 3. Phase 1 — Source analysis (no boot)

Compare `_cache/refs/cheseecake/src/NootedGreen` with `_cache/refs/juliornectar/src/NootedGreen`:

1. Full diff, classified: (a) topology, (b) code on the failing path (`IntelAccelerator::start`, `igAccelTaskWithOptions`, GTT/GGTT/stolen-memory setup, scheduler selection), (c) everything else. Note which side is newer: cheseecake forked an older JN.
2. **H2:** for each tree, how the subslice count reaches IGAccelDevice+0x1158 (byte patch `f3bbb`) and the `getGPUInfo()` fields (0x1158/0x1124/0x116c). Does JN's `ngreen-eu=64` change the load-time byte? Does cheseecake's override? Result: H2 confirmed / refuted.
3. Exact boot-arg names each tree parses for topology, scheduler, DMC and backlight (`ngreen-eu`/`ngreen-l3` vs `ngreensubslices`/`ngreenmaxeu`/`ngreenl3banks`), and whether the other fork's names are silently ignored.
4. How each tree handles **non-contiguous DSS** (mask 0x33): does either read fuses/masks or assume DSS 0..N-1? (The i3-1220P mask is unknown; ours is 0,1,4,5.)
5. Pin the binary to the source: confirm `src/` is identical between Build 17's commit `161c353` and the cloned `7881587` (ref repo history is allowed). If not, list what differs.
6. Compare `install.sh` / `macos/` of both repos: TGL bundle source commit (both should be sgiammori `95f8189`), HookCase build/install, Metal driver patches, libxedrv version, and whether cheseecake's installer requires the `9A49` spoof at install time (JN does, install.sh L86–87). Also read the Release zip's `install.command`.

Write `docs/CHESEECAKE-ANALYSIS.md` §B with a one-paragraph verdict: **can these differences plausibly change the `IGAccelTask::withOptions` panic?** Proceed to Phase 2 either way (the test costs one reboot), but state the expectation honestly.

## 4. Phase 2 — Get the cheseecake kext (user approval)

Option A (preferred, matches the source pinned in Phase 1.5): Release **Build 17** `NootedGreen.kext.zip`. It is a pre-release CI asset → needs user approval. Record URL, GitHub digest, SHA-256 of the zip and of `Contents/MacOS/NootedGreen` in `SOURCES.md`.
Option B: user builds on MÁY B: clone cheseecake at the pinned commit, `zsh build-nootedgreen.sh`, return `build/NootedGreen.kext` + its md5/SHA-256 via the USB root.

Do **not** use the Release `IrisXe-i3-1220P-tahoe.zip` installer yet (Phase 5).

## 5. Phase 3 — build-17 `chese-k1`: kernel-only test

Same idea as the R3 test: swap only the kernel side, keep JN user-space installed.

- Base: build-12 graphics-v1 (spoof 9A49, SIP 0x0A13, AMFIPass, dGPU `disable-gpu`, **no** `class-code`).
- `NootedGreen.kext` → cheseecake binary (same Kernel/Add position: right after WhateverGreen, MinKernel 25.0.0).
- boot-args: rebuild the string from scratch:
  - **graphics args first** (cheseecake's documented set): `-ngreentglwithgfx -allow3d -disablegfxfirmware ngreen-dmc=adlp ngreenSched=4 ngreenV142=3 -ngreenv189 -ngreenkeepefi -ngreenxefix -ngreenfixbootmode amfi_get_out_of_my_way=1 IGLogLevel=3 msgbuf=400000`
  - then base: `-v keepsyms=1 debug=0x100 -vi2c-force-polling -wegnoegpu -amfipassbeta`
  - **omit** `ngreen-eu`/`ngreen-l3` (JN names), `ngreenblmax=48000` (their panel), `gfxrst=1` (not in cheseecake's set); topology = cheseecake defaults (8 SS × 8 EU, L3 8)
  - total must be **under the limit found in Phase 0**; if it isn't, drop `IGLogLevel=3` and `msgbuf` first, never the AMFI/Wi-Fi/touchpad args. Record the final length in BUILD-LOG.
- Runbook for MÁY B: boot; if it reaches the desktop, return:
  ```
  sysctl kern.bootargs
  kmutil showloaded | grep -iE 'nootedgreen|hookcase|AppleIntelTGL'
  log show --last boot --predicate 'eventMessage CONTAINS "ngreen"' | grep -E 'platform|getGPUInfo'
  ioreg -rc IntelAccelerator -d1 | grep -iE 'xe-topo|EU|slice'
  system_profiler SPDisplaysDataType
  ```
  Expect `getGPUInfo: subslices=8 ... totalEU=64` and `platform: isRealTGL=0 ... dmcIsAdlp=1`. Mismatched JN user-space may give artifacts or a missing Metal device; that's acceptable at this step. The question is only whether `IntelAccelerator::start` survives.
- On panic: user boots build-10, collects `.panic`; compare with the JN signature (same function/offset/CR2 = same bug).

## 6. Phase 4 — Topology variants (one per build, only if k1 reached the desktop or panicked differently)

- build-18 `chese-k2`: k1 + `ngreenl3banks=6` (measured value; JN confirmed wrong L3 causes artifacts on 80 EU).
- If k1 and k2 both panic with the JN signature: **stop the NootedGreen/TGL track** (section 10).

## 7. Phase 5 — Switch user-space to cheseecake (only after a kernel build reaches the desktop)

Kernel and user-space must come from the same fork. Safe order (mirrors the build-11 lesson):
1. Boot **build-10** (no spoof). In the JN clone on MÁY B: `zsh install.sh --uninstall`. Return `ls /Library/Extensions`, `ls /Library/GPUBundles`, `ls -d /System/Library/Caches/xe.bundle`.
2. Build **`chese-prep`**: build-10 + spoof + SIP 0x0A13, no NootedGreen. Safe only because nothing TGL is installed now. Skip this build if Phase 1.6 shows cheseecake's installer doesn't need the spoof.
3. On MÁY B: run cheseecake's installer (source `zsh install.sh --check`, then `zsh install.sh`, or the Release `install.command`, per Phase 1.6 and the user's choice). **Do not reboot `chese-prep` afterwards.** Return output + the kext it built.
4. Build **`chese-v1`** = best kernel build from Phase 3/4 with the kext matching the installed user-space. Boot.
5. Verify: Metal in `system_profiler SPDisplaysDataType`, About This Mac, translucent Dock, smoothness, Wi-Fi/Ethernet/touchpad still working.

## 8. Phase 6 — Polish (one change per build)

- Resolution: `tools/xe-res`. **Avoid System Settings › Displays** and colour-profile changes (both panic upstream).
- Brightness: try `ngreenblmax=96000` (from Linux `intel_backlight` max; CHƯA XÁC MINH) or `xe-brilho`.
- Hardware video decode is off in this fork; use Chrome per its docs.
- `-ngreenpm` only if Phase 1 shows the fork has it.

## 9. Evidence after every boot

Result category (no picker / stuck / panic / blue or black screen / desktop) · `sysctl kern.bootargs` · newest `.panic` · the `ngreen` log lines above · photo of the last verbose lines (keep videos private: WPA keys) · Wi-Fi/Ethernet/touchpad state.

## 10. Exit criteria and fallback

- **Success:** `chese-v1` desktop on Metal, stable for 30 minutes. Mark known-good, update `STATE.md`, `GRAPHICS-PROGRESS.md`.
- **Stop:** the JN signature persists after (a) H1 fixed (args verifiably parsed) and (b) cheseecake k1/k2. Then the TGL-driver path is blocked on this platform for now. Options for the user, unranked:
  1. IntelIGPU-Tahoe: blocked on Apple TGL binaries matching SHA-256 (`docs/feasibility.md`). Only path forward is asking the author.
  2. WhateverXe: `docs/REFERENCES.md` (2026-11-01) says Big Sur/TGL/ADL-N only, while release 0.6.0/0.6.1 (26–27 Oct) notes claim ADL-H/P/U and experimental eDP. **Re-read the current README and releases before considering it.**
  3. Stay on build-10 without acceleration.
- In every case, restore MÁY B to a clean state with `install.sh --uninstall` from whichever stack is installed, while booted on build-10.

---

## Kickoff prompt

```
Read docs/PLAN-CHESEECAKE.md, STATE.md and GRAPHICS-PROGRESS.md. Follow section 1.
Do Phase 0 only: tell me what I need to copy from MÁY B, compute the boot-args
lengths, find the real boot-arg limit in Lilu/NootedGreen source, search the
existing logs for proof of which args NootedGreen parsed, and write
docs/CHESEECAKE-ANALYSIS.md §A. Don't build or write the USB. Stop and report H1.
```
