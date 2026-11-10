# WEX-NULLMOTH-RUNBOOK — thử WhateverXe + NullMoth trên volume dự phòng (build-55)

Người dùng yêu cầu 2026-11-10 01:23. Nhánh `whateverxe-dual-gpu`. **Thử nghiệm**, chỉ trên volume APFS dự phòng.

## Kỳ vọng (nói trước)
- WhateverXe 0.8.0 nhiều khả năng **từ chối tăng tốc iGPU 46A3** của máy này: i915 báo VCS2-only (`available engines: 41003`),
  giống issue #76 (ProfileMismatch → software rendering). Panel có thể chỉ chạy framebuffer không tăng tốc, hoặc đen.
- Mục tiêu đo được: (1) AGDP có gắn vào framebuffer Intel khi dGPU sống không; (2) NullMoth có nhận RTX 3050 Ti `25A0`, Metal 3 trên dGPU, HDMI.
- Không có XE-PM/HybridPM → CPU chậm hơn build-48 (không quan trọng cho phép thử này).

## Quy tắc an toàn
- USB build-55 **chỉ dùng để boot volume dự phòng**. Volume chính boot từ ổ trong (ESP = build-47) như cũ.
  Boot volume chính bằng build-55: không có NootedGreen → stack JN không chạy; không hỏng dữ liệu nhưng đừng làm.
- Không dùng app 1401 (nó tự sửa OpenCore).
- Đường lui: rút USB, boot ổ trong.

## build-55 so với build-54
| Mục | build-54 | build-55 |
|---|---|---|
| Kext đồ hoạ | WhateverGreen 1.7.1 + NootedGreen v13 | **WhateverXe 0.8.0 RELEASE** (b00t0x) |
| AMFIPass | không | **1.4.1 Mod** (b00t0x, `extras/` @88d64a3, sha256 71f41de4…6250) |
| iGPU DeviceProperties | spoof `9A49` + ig-platform-id + force-online… | chỉ `framebuffer-patch-enable`, `framebuffer-stolenmem 0000C003` (60 MB), `enable-max-pixel-clock-override`, `built-in` (theo README WhateverXe; không spoof) |
| Kernel/Block IONDRVSupport | có | **bỏ** (khucxtriendev không chặn; WhateverXe có thể cần framebuffer firmware khi từ chối 46A3) |
| SIP | 0x0A13 | **0x0A53** (⊇ 0x803 WhateverXe, ⊇ 0x0A43 NullMoth) |
| boot-args | NootedGreen… | `-v keepsyms=1 debug=0x100 -allow3d -disablegfxfirmware -igfxdvmt amfi_get_out_of_my_way=0x1 amfi=0x80 ipc_control_port_options=0 nvfb=1 nvaccel=1 nvfbheads=4 -nvkmsnosmooth itlwm_he=1` |
| dGPU | sống, hiện trong IOKit | như cũ |

## Bước trên MÁY B
1. **Volume dự phòng** có macOS 26.7.1 (25G241) — đúng bản này (Graphics 0.4.1 nhận bản cùng họ Tahoe ≥ 26.7, nhưng giữ 25G241 để so sánh).
   Không cập nhật macOS.
2. Boot vào macOS **volume dự phòng** bằng cách đã dùng lúc cài nó (ổ trong build-47 có dGPU tắt — an toàn nhất; hoặc USB build-55),
   rồi tải và kiểm (pkg/AuxKC phải cài khi đang chạy chính volume đó, không cài chéo từ volume chính):
   ```
   cd ~/Downloads
   curl -LO https://github.com/b00t0x/WhateverXe-Graphics/releases/download/v0.4.1/WhateverXe-Graphics-0.4.1.pkg
   shasum -a 256 WhateverXe-Graphics-0.4.1.pkg     # 7f7ce3b924ad421cff0c4f30534598858474b8c9539c4b889a461bc1d5fed02c
   curl -LO https://github.com/nullmoth/nvidia-macos-driver/releases/download/v2.8.1/nullmoth-nvidia-2.8.1.tar.gz
   shasum -a 256 nullmoth-nvidia-2.8.1.tar.gz      # 1aa25a7f0ae28a27e77e1a761420cef9655af8b2b8effc1433142d1071795df8
   ```
3. Cài WhateverXe-Graphics (pkg cài vào `/Library`, rebuild AuxKC; không sửa System/SIP/EFI):
   ```
   sudo installer -pkg WhateverXe-Graphics-0.4.1.pkg -target /
   ```
4. Cài NullMoth (README "Install — by hand"):
   ```
   tar -xzf nullmoth-nvidia-2.8.1.tar.gz && cd pkgroot
   shasum -a 256 -c SHA256SUMS
   sudo ./install.sh
   ```
   Mọi dòng phải `OK`. Nếu System Settings → Privacy & Security hỏi cho phép extension: cho phép.
5. Cắm màn hình HDMI (nếu có) **trước khi** bật máy. Tắt máy, cắm USB, boot **USB build-55**, chọn **volume dự phòng**.
6. Vào được desktop thì gửi:
   ```
   system_profiler SPDisplaysDataType
   ioreg -lw0 -r -c AppleGraphicsDevicePolicy | grep -E 'class|IOProviderClass' | head
   ioreg -lw0 | grep -iE 'N97GTReadout|N97FramebufferStartAccepted|N97NativePreflight|N97GTTopologyReady|WEXDisplay13AGDCGuardReady' | head -20
   kextstat 2>/dev/null | grep -iE 'WhateverXe|NVRM|NVAccel|NVRMFB|AMFIPass|AGDP|GraphicsDevicePolicy'
   log show --last boot --style compact | grep -iE 'WEX|WhateverXe|NVRM' | head -80 > ~/b55-boot.txt
   ```
   Panic/treo: rút USB, boot ổ trong, gửi `.panic` mới (+ ảnh/video màn hình `-v`).
7. Gỡ (nếu cần, trên volume dự phòng): `sudo ./uninstall.sh` của NullMoth; `sudo bash uninstall.sh` của WhateverXe-Graphics.
