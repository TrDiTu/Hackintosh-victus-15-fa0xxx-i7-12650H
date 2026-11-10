# WhateverXe 0.7.0-katana-r2 (tự build)

- Fork https://github.com/TrDiTu/WhateverXe nhánh `katana-46a3`, commit `70809f705b26c8999b33bebc3478f2d9e3d90dad`; gốc tag 0.7.0 `d0b7fb6` (BSD-3-Clause).
- CI run 42797617881 (https://github.com/TrDiTu/WhateverXe/actions/runs/42797617881): 203 test pass.
- So với r1 (run 42791539485) thêm sửa VBT panel cho Victus: chọn eDP DDI A khi VBT khai báo eDP ở cả A và B;
  nhận `panel_type` 0xFF (chọn theo EDID PnP) như loại 0 chỉ khi 16 mục VBT đồng nhất (đúng với VBT máy này).
- Vẫn gồm patch #35 và cờ opt-in `-wex-adlp-allow-vcs2`.
- SHA-256:
  - 34658daebd6ac36441af5d4757af69dcb5e291b1158b4eb17df409b126d454ee  WhateverXe-0.7.0-DEBUG.zip
  - a5e0910e1fe163a531fe83c630a05b8284ea1d2869f4d1ef35dc85db38c1cdfd  WhateverXe-0.7.0-RELEASE.zip
