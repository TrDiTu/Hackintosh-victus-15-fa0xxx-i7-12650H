# WhateverXe 0.7.0-katana-r5 (tự build)

- Fork https://github.com/TrDiTu/WhateverXe nhánh `katana-46a3`, commit `0d0c3f1bed5fdb1b066a3523792d9569b03d0846`; gốc tag 0.7.0 `d0b7fb6` (BSD-3-Clause).
- CI run 42808459666 (https://github.com/TrDiTu/WhateverXe/actions/runs/42808459666): 203 test pass.
- So với r4 thêm (ROADMAP G5): máy VCS2-only → vá `g_cInitGfxHwCtxParamsForVideoMedia` của AppleIntelTGLGraphics từ type 3/instance 0
  sang type 4/instance 2 (VCS2, `0x1D0000`), kiểm đủ 12 byte gốc; vá OK thì giữ video phần cứng, lỗi thì tắt như r4.
  ioreg: `WEXVCS2Media`, `WEXHardwareVideoDisabled`.
- Gồm r4, r3 (PAVP), r2 (VBT panel), patch #35, cờ `-wex-adlp-allow-vcs2`.
- SHA-256:
  - f1c28b8584be6838e84cf939a8ff59e970930ef800cb06fb455aea79143ceba1  WhateverXe-0.7.0-DEBUG.zip
  - d5d30e1b3b82e2c17cd56d4c01f8be518177fecbefcc04e697ef9d6677694fc9  WhateverXe-0.7.0-RELEASE.zip
