# WhateverXe 0.7.0-katana-r3 (tự build)

- Fork https://github.com/TrDiTu/WhateverXe nhánh `katana-46a3`, commit `4c3be80b9c47772a5e33f29eb55b0b49a6927570`; gốc tag 0.7.0 `d0b7fb6` (BSD-3-Clause).
- CI run 42800957857 (https://github.com/TrDiTu/WhateverXe/actions/runs/42800957857): 203 test pass.
- So với r2 thêm: ép nhánh "PAVP tắt" trong `IntelAccelerator::PAVPCommandCallback` (đường ADL-P/N), kiểm mẫu đúng 1 lần
  trong 0x180 byte đầu hàm; kết quả ở ioreg `WEXPAVPDisabledPath`. Lý do: panic build-61 NULL+0xB8 (`logs/Kernel-2026-11-10-173420.panic`).
  Viết lại theo kiểu WEX từ phân tích của chính dự án (PAVPFIX); không chép mã NootedGreen.
- Gồm r2 (VBT panel), patch #35, cờ `-wex-adlp-allow-vcs2`.
- SHA-256:
  - 9581289a279b5e71aab4de188a77422085c45ebde13f1bae1dca0cf344fe42e8  WhateverXe-0.7.0-DEBUG.zip
  - fa7561a2432dccde206c9eaf3cdcabcd4346e835592df7245a18e7daf98c0c86  WhateverXe-0.7.0-RELEASE.zip
