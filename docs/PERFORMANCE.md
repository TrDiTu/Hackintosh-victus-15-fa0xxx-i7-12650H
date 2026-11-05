# PERFORMANCE — đo CPU và iGPU trên macOS (MÁY B)

Mục tiêu: có số đo nền (baseline) trước, rồi mỗi lần chỉnh chỉ đổi MỘT thứ và đo lại cùng cách.

## Công cụ
| Việc | Công cụ | Ghi chú |
|---|---|---|
| Nhiệt độ P/E-core, gói; công suất gói / nhân CPU / **iGPU** | `tools/xe-monitor.py` | Đọc `sysctl debug.xepm.sensors` của NootedGreen JN @6f03560 (luôn có, không cần `-ngreenpm`) + `ioreg` IntelAccelerator. `python3 xe-monitor.py -i 1 -o <tên>.csv` |
| Xung CPU | `sudo powermetrics --samplers cpu_power -i 1000 -n 10` | Dòng "System Average frequency" và từng CPU |
| Mức dùng iGPU | Activity Monitor › Window › GPU History; `python3 xe-monitor.py --gpu-keys` | Driver TGL giả lập: khoá nào có thì dùng khoá đó |
| Benchmark CPU | Geekbench 6 (CPU), Cinebench 2024 (CPU, chạy 10 phút để thấy giới hạn nhiệt/PL1) | |
| Benchmark iGPU | Geekbench 6 (GPU, **Metal**) | ⚠️ Tải GPU nặng chưa từng chạy trên stack này: có thể GPU hang/panic. Lưu việc đang làm trước |

## Vòng đo nền (build-33, chưa chỉnh gì)
Cắm sạc, đóng app khác, chờ máy nghỉ 2 phút sau khi boot. Mỗi bước chạy `xe-monitor.py` song song và lưu CSV.
1. **Nghỉ** 2 phút → `idle.csv` (công suất gói lúc nghỉ, nhiệt).
2. **Geekbench 6 CPU** → điểm single/multi + `gb6-cpu.csv`. Trong lúc chạy single-core: 1 lần `powermetrics` (xung 1 nhân tối đa).
3. **Cinebench 2024 CPU, Minimum Test Duration 10 phút** → điểm + `cb24.csv` (công suất bền vững = PL1, nhiệt, có bị hạ xung).
4. **Geekbench 6 GPU (Metal)** → điểm + `gb6-gpu.csv` (công suất iGPU, mức dùng).
Gửi Claude: các điểm số, 4 file CSV (hoặc phần summary cuối mỗi lần chạy), kết quả `powermetrics`.

## Hướng cải thiện sẽ xét sau khi có số nền (CHƯA LÀM, mỗi mục một build, cần duyệt)
- **XE-PM** (`-ngreenpm`, có sẵn trong NootedGreen JN @6f03560 — `kern_xepm.cpp`, kiểm byte-for-byte trên 25G241): sửa
  turbo P-core (XCPM ghi giới hạn HWP sai trên CPU lai), bật C8/C10 lúc nghỉ, EPP. JN đo trên i7-1360P: single-core +33 %,
  multi +16 %, nghỉ 4,6 → 3,3 W. i7-12650H (6P+4E, H-series) CHƯA có báo cáo. Boot-args 219 + 10 = 229 > 228 → phải bỏ `-v`
  (còn 226). PL1: giữ của BIOS (`-ngreenpm`), không đặt `ngreenpm=W` khi chưa đo nhiệt.
- iGPU: xem mức dùng/công suất GT lúc benchmark để biết GPU có lên xung không (dữ liệu XE-GTF `gtf=` trong `dmesg` `XeNG CS`).
