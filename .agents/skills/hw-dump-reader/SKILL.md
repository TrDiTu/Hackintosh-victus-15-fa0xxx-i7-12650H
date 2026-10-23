---
name: hw-dump-reader
description: Read and sanity-check the hardware dump of the TARGET laptop (docs/hw-dump/ produced by tools/dump-laptop.ps1 on machine B) together with laptop-specs.md, detect missing data, and write docs/MACHINE-ANALYSIS.md. Use at the start of the project, whenever the user mentions hardware inventory, "phần cứng", "Hardware ID", "kiểm kê", "dump", DSDT/SSDT, or before choosing any driver. NEVER dump hardware from the machine running Codex.
---

# hw-dump-reader

Codex chạy trên MÁY A; laptop đích là MÁY B. Dữ liệu phần cứng chỉ đến từ `laptop-specs.md` và
`docs/hw-dump/`. Không chạy lệnh nhận diện phần cứng trên máy hiện tại để "bù" dữ liệu thiếu.

## Bước 1 — Kiểm tra dữ liệu có đủ không
Kiểm tra `docs/hw-dump/` có: `system.txt`, `bios.txt`, `cpu.txt`, `gpu.txt`, `disks.txt`, `network.txt`,
`monitors.txt`, `pnp-devices.csv` (cột Class, Name, Status, InstanceId, HardwareIds, CompatibleIds, Location),
`acpi-devices.csv`, `pnp-key-classes.csv`.

Phát hiện bất thường (báo cho người dùng, không đoán):
- `system.txt` có Manufacturer/Model khớp laptop đích không? Nếu dữ liệu trông như máy khác (ví dụ khác
  hãng/model so với `laptop-specs.md`) → DỪNG, hỏi lại: có thể dump nhầm máy.
- Thiếu Hardware ID cho Wi-Fi, Bluetooth, touchpad, audio, iGPU, dGPU, NVMe, card reader.
- Không có thiết bị ACPI I2C/HID cho touchpad (ví dụ `ACPI\ELAN*`, `ACPI\SYNA*`, `ACPI\MSFT0001`...).
- Thiết bị trạng thái `Error`/`Unknown` (có thể là thiết bị chưa có driver Windows, vẫn cần ghi lại).
- Thiếu DSDT/SSDT (`docs/hw-dump/acpi/`). Cần khi viết SSDT tắt dGPU, GPIO touchpad (skill `ssdt-authoring`).

Nếu thiếu: viết danh sách chính xác file/thông tin cần, hướng dẫn người dùng chạy lại trên MÁY B,
rồi DỪNG chờ. Cách lấy DSDT/SSDT (do người dùng chạy trên MÁY B): SSDTTime hoặc acpidump trên Windows/Linux,
hoặc bản OpenCore debug với `Misc > Debug > SysReport` (kết quả nằm trong `SysReport` của phân vùng EFI).

## Bước 2 — Phân loại thiết bị
Từ `pnp-devices.csv` lọc theo `Class` và tiền tố `HardwareIds` (`PCI\VEN_xxxx&DEV_xxxx`, `USB\VID_xxxx&PID_xxxx`,
`ACPI\xxxx`, `HDAUDIO\...`). Lập nhóm: CPU/chipset · iGPU · dGPU · màn hình/panel · Wi-Fi · Bluetooth (thường là USB)
· Ethernet · audio (codec + controller) · mic · touchpad · bàn phím/Fn · SSD/NVMe · card reader · camera ·
vân tay · USB/Type-C/Thunderbolt · EC/pin · sensor/ALS/accelerometer · I2C/GPIO controller · TPM.
Với mỗi thiết bị ghi: tên, Hardware ID đầy đủ, nguồn (file/dòng).

## Bước 3 — Ghi `docs/MACHINE-ANALYSIS.md`
Gồm: tóm tắt máy (model, CPU, đời iGPU), bảng thiết bị, BIOS (CFG Lock, VT-d, Above 4G, chế độ GPU, DVMT,
Secure Boot, nếu `laptop-specs.md`/dump có cho biết, nếu không thì liệt kê "cần người dùng kiểm tra"),
danh sách THÔNG TIN CÒN THIẾU, và các điểm nghi ngờ. Đánh dấu "CHƯA XÁC MINH" cho mọi suy đoán.
Không đưa serial/UUID vào tài liệu.

## Bước 4
Cập nhật `docs/STATE.md`, trình tóm tắt 5–10 dòng cho người dùng và hỏi các thông tin còn thiếu.
Đây là đầu vào của `driver-vetting`.
