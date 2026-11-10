# WhateverXe 0.7.0-katana-r6 (tự build, chẩn đoán)

- Fork https://github.com/TrDiTu/WhateverXe nhánh `katana-46a3`, commit `d7dc5c5ba717f33ac51966eb003e0e1238903062`; gốc tag 0.7.0 `d0b7fb6` (BSD-3-Clause).
- CI run 42813262332 (https://github.com/TrDiTu/WhateverXe/actions/runs/42813262332): 203 test pass.
- So với r5 thêm (chỉ đo, không đổi hành vi): route `IGInterruptBridge::readAndClearVCSInterrupts`, `IGScheduler5::notify`,
  `IGScheduler5::checkForProgress`, `IGHardwareCommandStreamer5::enableStampInterrupt` → bộ đếm 40×u64 ở ioreg `WEXVCSDiag`
  (bố cục trong comment mã nguồn), `WEXVCSDiagRouted`.
- SHA-256:
  - 6bf9107f0e1dd3d66cfd3a713fc43433e27685010f02e2d78c1d5977c81dba31  WhateverXe-0.7.0-DEBUG.zip
  - d06c4996de04d87d1606a48a5303c0fd093a200baab339d0e5172769f839f235  WhateverXe-0.7.0-RELEASE.zip
