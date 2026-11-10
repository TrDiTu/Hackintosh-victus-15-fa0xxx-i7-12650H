# HybridPM + XE-HWPAUTO (tự build)

- Nguồn: fork https://github.com/TrDiTu/HybridPM nhánh `victus` @ `6ddb23d64773f5fe8ce403725662af1d57fc5679`
  = Thatisjigen/HybridPM @23c4537 + workflow CI + XE-HWPAUTO (port từ patch v8 NootedGreen của dự án, `docs/GMSFIX-RUNBOOK.md` §v8).
  Giấy phép TSNPL 1.0 (giữ nguyên; header file ghi rõ thay đổi).
- Thay đổi: `xpSetMult` xoá trường desired (bit 16–23 MSR 0x774) khi `gXpAuto`; mặc định BẬT (boot-args đã gần 228 ký tự);
  tắt bằng boot-arg `hpmauto=0` hoặc `sudo sysctl -w debug.hybridpm.hwpauto=0` (trực tiếp). Log profile thêm `HWPAUTO %d`.
- Kiểm MÁY A: `clang++ -fsyntax-only` (MacKernelSDK + Lilu SDK local): 0 lỗi, 2 cảnh báo có sẵn.
- Build: GitHub Actions run 42836259880 (https://github.com/TrDiTu/HybridPM/actions/runs/42836259880), 13 cảnh báo (như bản gốc).
- SHA-256: zip `d7ea9cc9a09b9be5eb52c86033d8332ea30d71b956a293e300e7d694c8e412ed`;
  binary `c606794284dc8be3aa4042b0258b15a73336a2aaefa6246211ce16690fa72baa`.
