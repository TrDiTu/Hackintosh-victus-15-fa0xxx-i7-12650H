# HybridPM (tự build)

- Nguồn: https://github.com/Thatisjigen/HybridPM @ `23c4537ab971367ac9e37758ada4f9bbffc7b952` (không có release), giấy phép TSNPL 1.0
  (dẫn xuất `kern_xepm.cpp` của JulioNectar @99631db2). Fork https://github.com/TrDiTu/HybridPM nhánh `victus` chỉ thêm workflow CI.
- Build: GitHub Actions run 42830446513 (https://github.com/TrDiTu/HybridPM/actions/runs/42830446513), `bash build.sh` gốc
  (MacKernelSDK 3f75008, Lilu 1.7.2 DEBUG SDK, SOURCE_DATE_EPOCH cố định), 13 cảnh báo biên dịch (shadow/sign-conversion/deprecated).
- SHA-256: zip `756c37f55dc50f0d86c6c6d403a7a757f01a9d22a20cf2672a9e8657047a016b`; binary `9f65958fdc8f2c715b4322deea3c4667996919d0076d3dd3cfe3e1ddc57b4cd9`.
- Bundle `org.anv1552.HybridPM` 1.0.0, cần Lilu ≥ 1.2.0. Mặc định áp profile (HWP units P-core, EPP 96, tắt EE turbo, C-state C8/C10)
  ở 20 s và 60 s; hook XCPM chỉ khi kernel khớp byte (25G241, 25G332). `-nohpm` tắt.
