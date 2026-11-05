# PERFORMANCE — đo CPU và iGPU trên macOS (MÁY B)

Mục tiêu: có số đo nền (baseline) trước, rồi mỗi lần chỉnh chỉ đổi MỘT thứ và đo lại cùng cách.

## Công cụ
| Việc | Công cụ | Ghi chú |
|---|---|---|
| Nhiệt độ P/E-core, gói; công suất gói / nhân CPU / **iGPU** | `tools/xe-monitor.py` | Đọc `sysctl debug.xepm.sensors` của NootedGreen JN @6f03560 (luôn có, không cần `-ngreenpm`) + `ioreg` IntelAccelerator. `python3 xe-monitor.py -i 1 -o <tên>.csv` |
| Xung CPU | `tools/xe-freq.c` (`clang -O2 -o xe-freq xe-freq.c -lpthread`; `./xe-freq` = 1 luồng, `./xe-freq 16` = toàn bộ). ⛔ **KHÔNG dùng `powermetrics`** | 2026-11-06 00:07: `powermetrics --samplers cpu_power` gây kernel panic (NULL trong framebuffer TGL qua AppleGraphicsDeviceControl). Dùng công suất IA của `xe-monitor.py` làm chỉ báo |
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

## Build-34 — XE-PM (`-ngreenpm`, PL1 của BIOS), 2026-11-06 00:37
| | build-33 | build-34 | Chênh |
|---|---|---|---|
| Geekbench 7 single-core | 1076 | **1220** | +13 % |
| Geekbench 7 multi-core | 5837 | **5476** | −6 % |
| Công suất IA pha tải nhẹ (avg / p90) | 7,4 / 11,3 W | 12,8 / 21,9 W | |
| Gói max / P-core max | 73,2 W / 88 °C | 64,9 W / 83 °C | |
Một lần chạy mỗi bên → chưa biết dao động giữa các lần (multi của Geekbench thường lệch vài %). Single-core tăng ít hơn JN (+33 %).
Giả thuyết multi giảm (CHƯA XÁC MINH): pha single-core tiêu nhiều năng lượng hơn nên ngân sách PL2/tau cạn sớm hơn khi vào multi
(gói max thấp hơn 8 W); hoặc chỉ là dao động. Thử được mà không cần build mới: XE-PM có sysctl đổi trực tiếp
`debug.xepm.hwp` (0/1), `debug.xepm.epp` (0–255), `debug.xepm.cst` (0/1).
- `powermetrics` lúc GB7 single-core (build-34, người dùng chấp nhận rủi ro panic): nhân bận nhất 3,9–4,43 GHz trung bình mỗi giây
  (nominal 2680 MHz; spec turbo 4,7 GHz), luồng nhảy giữa CPU 1/3/4, gói 21–26 W → turbo đã vượt mức ~3,8 GHz. Khoảng cách
  tới 4,7 GHz: nghi do chỉ 1–2 "favored core" lên 4,7 và scheduler macOS chuyển luồng qua lại (CHƯA XÁC MINH).
- `tools/xe-freq.c`: bản `add $imm` cho số sai (Golden Cove gộp chuỗi cộng hằng ở renamer); bản ADD thanh ghi chưa kiểm trên MÁY B.
- Tải đều 16 luồng (`yes`) trên build-34: mọi CPU hiển thị 3,94–4,04 GHz, gói ~67 W → không có nhân kẹt xung. Các nhân 0,7–1,1 GHz
  lúc GB7 multi là pha ít luồng của Geekbench. `sysctl`: hw.ncpu = logicalcpu = thread_count = 16, **physicalcpu = 6**
  (CpuTopologyRebuild), perflevel0 = 16 luồng (macOS không tách P/E). powermetrics chỉ in 10 CPU = giới hạn hiển thị.
- Kết luận build-34: XE-PM có lợi cho single-core (+13 %, 4,43 GHz); multi −6 % chưa tách được khỏi dao động (1 lần chạy).
- `debug.xepm.epp=128` (sysctl, build-34): GB7 single 1222, multi **5378** → EPP không phải nguyên nhân; về lại EPP 0.
  Multi thấp ở 2 lần chạy (5476, 5378) so với build-33 (5837, 1 lần) → khó chỉ là dao động.
- `debug.xepm.cst=0` (sysctl, build-34): GB7 single **1176**, multi **7114** (+22 % so build-33, +30 % so build-34 mặc định) → C8/C10
  của XE-PM làm giảm multi-core. → build-35 `ngreenpmcst=0`.
- So với Linux cùng máy (GB7 ~2xxx / 2xxxx): CPUID trên macOS đủ AVX/AVX2/FMA/BMI2/SHA/VAES; TSC 2,688 GHz, `sleep 30` = 30,04 s → đồng hồ đúng.
  `xe-freq` (ADD thanh ghi, 1 luồng, mẫu 1 s): **Linux 4503 / 4640 / 4681 MHz** (min/avg/max, khớp turbo 4,7) — **macOS build-35 1502 / 3365 / 4586 MHz**.
  → CPU lên được ~4,6 GHz nhưng luồng không giữ được tốc độ (avg 72 % Linux). Nghi: luồng bị xếp lên E-core (CpuTopologyRebuild coi E-core là
  luồng SMT của P-core), chuyển nhân, hoặc XCPM hạ HWP desired. CHƯA XÁC MINH — cần xem từng mẫu (`XEFREQ_SAMPLES=1 ./xe-freq 1 30`).
- **Mốc Linux (CachyOS, cùng máy, 2026-11-06): GB7 single 2195, multi 10101.** macOS tốt nhất hiện tại (XE-PM, C8/C10 tắt): 1176 / 7114
  = **54 % / 70 %**. Single-core hụt nhiều nhất → khớp xe-freq (luồng đơn không giữ xung).
- `XEFREQ_SAMPLES=1 ./xe-freq 1 30` trên macOS build-35: 30 mẫu trải liên tục **1389–4679 MHz** (avg 3364), không thành hai mức P/E
  → trong mỗi giây luồng chỉ chạy nhanh một phần thời gian. xe-freq thêm cột E-core% (CPUID 0x1A) và số nhân đã chạy qua (x2APIC, CPUID 0x0B).
- **Nguyên nhân single-core thấp (2026-11-06 03:22, xe-freq có theo dõi nhân):** Linux — luồng ở yên **1 nhân**, 4662 MHz, E-core 0 %.
  macOS build-35 — luồng đi qua **2–16 nhân mỗi giây**, E-core chỉ 1 % trung bình; xung tỉ lệ nghịch số nhân (2–4 nhân ≈ 4550 MHz,
  12–16 nhân 2000–3800 MHz). → bộ lập lịch XNU chuyển luồng liên tục giữa các P-core (nhân mới còn xung thấp, cache lạnh), không phải E-core.
  Nghi: topology SMT giả của CpuTopologyRebuild mặc định (6c/16t). Thử `ctrsmt=off` qua NVRAM (CHƯA XÁC MINH).
