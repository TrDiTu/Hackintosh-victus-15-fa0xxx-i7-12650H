# PERFORMANCE — đo CPU và iGPU trên macOS (MÁY B)

Mục tiêu: có số đo nền (baseline) trước, rồi mỗi lần chỉnh chỉ đổi MỘT thứ và đo lại cùng cách.

## Công cụ
| Việc | Công cụ | Ghi chú |
|---|---|---|
| Nhiệt độ P/E-core, gói; công suất gói / nhân CPU / **iGPU** | `tools/xe-monitor.py` | Đọc `sysctl debug.xepm.sensors` của NootedGreen JN @6f03560 (luôn có, không cần `-ngreenpm`) + `ioreg` IntelAccelerator. `python3 xe-monitor.py -i 1 -o <tên>.csv` |
| Xung CPU | ⛔ **KHÔNG dùng `powermetrics`** | 2026-11-06 00:07: `powermetrics --samplers cpu_power` gây kernel panic (NULL trong framebuffer TGL qua AppleGraphicsDeviceControl). Dùng công suất IA của `xe-monitor.py` làm chỉ báo |
| Mức dùng iGPU | Activity Monitor › Window › GPU History; `python3 xe-monitor.py --gpu-keys` | Driver TGL giả lập: khoá nào có thì dùng khoá đó |
| Benchmark CPU | Geekbench 7 (CPU), Cinebench 2024 (CPU, chạy 10 phút để thấy giới hạn nhiệt/PL1) | |
| Benchmark iGPU | Geekbench 7 (GPU, **Metal**) | ⚠️ Tải GPU nặng chưa từng chạy trên stack này: có thể GPU hang/panic. Lưu việc đang làm trước |

## Vòng đo nền (build-33, chưa chỉnh gì)
Cắm sạc, đóng app khác, chờ máy nghỉ 2 phút sau khi boot. Mỗi bước chạy `xe-monitor.py` song song và lưu CSV.
1. **Nghỉ** 2 phút → `idle.csv` (công suất gói lúc nghỉ, nhiệt).
2. **Geekbench 7 CPU** → điểm single/multi + `gb7-cpu.csv`. Trong lúc chạy single-core: 1 lần `powermetrics` (xung 1 nhân tối đa).
3. **Cinebench 2024 CPU, Minimum Test Duration 10 phút** → điểm + `cb24.csv` (công suất bền vững = PL1, nhiệt, có bị hạ xung).
4. **Geekbench 7 GPU (Metal)** → điểm + `gb7-gpu.csv` (công suất iGPU, mức dùng).
Gửi Claude: các điểm số, 4 file CSV (hoặc phần summary cuối mỗi lần chạy), kết quả `powermetrics`.

## Hướng cải thiện sẽ xét sau khi có số nền (CHƯA LÀM, mỗi mục một build, cần duyệt)
- **XE-PM** (`-ngreenpm`, có sẵn trong NootedGreen JN @6f03560 — `kern_xepm.cpp`, kiểm byte-for-byte trên 25G241): sửa
  turbo P-core (XCPM ghi giới hạn HWP sai trên CPU lai), bật C8/C10 lúc nghỉ, EPP. JN đo trên i7-1360P: single-core +33 %,
  multi +16 %, nghỉ 4,6 → 3,3 W. i7-12650H (6P+4E, H-series) CHƯA có báo cáo. Boot-args 219 + 10 = 229 > 228 → phải bỏ `-v`
  (còn 226). PL1: giữ của BIOS (`-ngreenpm`), không đặt `ngreenpm=W` khi chưa đo nhiệt.
- iGPU: xem mức dùng/công suất GT lúc benchmark để biết GPU có lên xung không (dữ liệu XE-GTF `gtf=` trong `dmesg` `XeNG CS`).

## Kết quả đo nền — build-33 (2026-11-05 23:26 → 00:00, cắm sạc)
| Bài | Điểm | Công suất gói (avg / p95 / max) | CPU (IA) | iGPU (GT) | Nhiệt P / E max |
|---|---|---|---|---|---|
| Nghỉ 2 phút | — | 7,4 / 8,8 / 11,9 W | 1,6 W | 0 W | 57 / 49 °C |
| Geekbench 7 CPU | **single 1076, multi 5837** | 17,8 / 52,8 / 73,2 W | max 65,7 W | — | 88 / 79 °C |
| Geekbench 7 GPU (Metal) | **1094** (không panic) | 14,0 / 25,4 / 44,6 W | — | avg 2,7, p95 11,5, max 12,9 W | 67 / 60 °C |
Nguồn: `logs/idle.csv`, `logs/gb7-cpu.csv`, `logs/gb7-gpu.csv` (thư mục chính).

Nhận định:
- **Single-core thấp**: suốt phần single-core (~23:27–23:31) công suất nhân CPU chỉ 3–8 W (gói 10–15 W); một P-core
  Alder Lake-H chạy turbo đầy thường cần nhiều hơn hẳn → P-core không lên turbo. 1076 còn thấp hơn số "trước XE-PM" của JN
  trên i7-1360P U-series (1269). Khớp lỗi XCPM giới hạn HWP trên CPU lai mà XE-PM sửa. Thiếu `powermetrics` để xác nhận xung — CHƯA XÁC MINH.
- **Multi-core**: gói lên tới 73 W, nhiệt 88 °C → giới hạn công suất/nhiệt của BIOS cho phép tải nặng; ngắn hạn không phải nút thắt.
- **Nghỉ 7,4 W** khá cao (nhân CPU chỉ 1,6 W; phần còn lại là uncore/SA) → gợi ý không vào C-state sâu (C8/C10), cũng là việc XE-PM xử lý.
- **iGPU**: có tải thật (GT tới ~13 W). `gpu_util_pct` luôn 0 và `gpu_mem_MB` trống: driver TGL không có khoá
  `Device Utilization %`/`In use system memory` → cần `python3 xe-monitor.py --gpu-keys` để chọn khoá đúng.
