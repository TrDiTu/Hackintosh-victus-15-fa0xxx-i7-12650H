# WhateverXe 0.7.0-katana-r7 (tự build)

- Fork https://github.com/TrDiTu/WhateverXe nhánh `katana-46a3`, commit `4853f8f738306ce7e22b7057486cc70a589e8288`; gốc tag 0.7.0 `d0b7fb6` (BSD-3-Clause).
- CI run 42816038634 (https://github.com/TrDiTu/WhateverXe/actions/runs/42816038634): 203 test pass.
- So với r6: trên máy VCS2-only thay `IGInterruptBridge::readAndClearVCSInterrupts` bằng hàm kiểu i915 (chỉ chọn engine có bit trong
  GT_INTR_DW1, chờ identity hợp lệ tới ~100 µs, ánh xạ theo LUT của driver, xoá identity). Lý do: r6 đo được ngắt VCS2 tới (1757 lần) nhưng
  driver gốc không đặt bit nào cho VCS2. Bộ đếm `WEXVCSDiag` mở rộng: [28]/[29] VCS2 hợp lệ/timeout, [32] identity VCS2 cuối, [34] số poll lớn nhất.
- SHA-256:
  - 8a3c8686aacc035f4240fc569e41cb7ae585596e8a0de42cfbce79a06e8388f3  WhateverXe-0.7.0-DEBUG.zip
  - cc00fe0b363fc0a8aba3b814db363e71bf3ad8e1906a65a3d5a04b7c7ec12b3e  WhateverXe-0.7.0-RELEASE.zip
