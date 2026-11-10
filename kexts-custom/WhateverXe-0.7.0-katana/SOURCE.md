# WhateverXe 0.7.0 + issue #35 + cờ VCS2 (bản tự build)

- Nguồn: fork https://github.com/TrDiTu/WhateverXe nhánh `katana-46a3`, commit `71cfd0533735c9f743295f2ddd167f255299b18d`.
- Gốc: b00t0x/WhateverXe tag `0.7.0` = `d0b7fb6275ca51fde088fa7e91595462bd457ec9` (BSD-3-Clause).
- Build: GitHub Actions run 42791539485 (https://github.com/TrDiTu/WhateverXe/actions/runs/42791539485),
  workflow `ci.yml` gốc (macos-15-intel, MacKernelSDK @05094e5, Lilu 1.7.2), CPU tests 203 pass / 0 fail.
- Thay đổi so với 0.7.0 (`katana-46a3-vs-0.7.0.diff`):
  1. Patch issue #35 `WEX-0.7.0-katana-fixes.patch` (sha256 `b66300c341c18d3db9273e260d7134defbdefe1699ab40619402f1b94f38db68`):
     VBT giữ child đầu tiên mỗi DDI; eDP port mode 0 lúc handoff; CDCLK khởi động nguội.
  2. Cờ thử nghiệm `-wex-adlp-allow-vcs2` (mặc định TẮT): `decodeADLPGT` nhận video mask 4 (chỉ VCS2, fuse
     `0x000E00FB` của máy này). Không có cờ → vẫn ProfileMismatch như 0.7.0. Issue #76 báo ép như vậy → treo cứng.
  3. Test cập nhật theo hành vi VBT mới; CI build thêm nhánh `katana-46a3`.
- Bundle: `org.b00t0x.WhateverXe` 0.7.0, cần Lilu ≥ 1.2.0 (OSBundleLibraries).
- SHA-256:
  - 23e688de95d391f60ef5a06a0268e4cd6c2e1c671c95b53926e742151c4dab83  WhateverXe-0.7.0-DEBUG.zip
  - 536cd7dce0e019e5fdbfb01a2e74e968db8c16084acd60ec6ed667c742cd7ca8  WhateverXe-0.7.0-RELEASE.zip
