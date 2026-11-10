# WhateverXe 0.7.0-katana-r4 (tự build)

- Fork https://github.com/TrDiTu/WhateverXe nhánh `katana-46a3`, commit `7d73efa572698b5b5d31b286bc5b42f97aec0647`; gốc tag 0.7.0 `d0b7fb6` (BSD-3-Clause).
- CI run 42804853728 (https://github.com/TrDiTu/WhateverXe/actions/runs/42804853728): 203 test pass.
- So với r3 thêm: máy VCS2-only (video mask 4) → giữ `IOVARendererID` gốc (AppleGVA từ chối) và gỡ các khoá IOGVA → không giải mã
  video phần cứng (ioreg `WEXHardwareVideoDisabled`). Lý do: panic build-62 `VTDecoderXPCService` →
  `IGHardwareCommandStreamer5::setWorkQueueBinding` NULL+0x284 (driver Apple gắn ring media vào VCS0, máy chỉ có VCS2).
- Gồm r3 (PAVP), r2 (VBT panel), patch #35, cờ `-wex-adlp-allow-vcs2`.
- SHA-256:
  - f77c0be58d12869e4380536f963099c0bcaadcf27480306e4a3f5dfa25effdc5  WhateverXe-0.7.0-DEBUG.zip
  - 8e83c5892beaf475efcff74ae48db49bb2908afde61b937ee84a0b9bc27af7ff  WhateverXe-0.7.0-RELEASE.zip
