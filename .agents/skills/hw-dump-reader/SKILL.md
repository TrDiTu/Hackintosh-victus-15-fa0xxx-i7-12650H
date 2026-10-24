---
name: hw-dump-reader
description: Read and sanity-check the hardware dump of the TARGET laptop (docs/hw-dump/, produced on machine B by tools/dump-laptop.sh under Linux or tools/dump-laptop.ps1 under Windows) together with laptop-specs.md, detect missing data, and write docs/MACHINE-ANALYSIS.md. Use at the start of the project, whenever the user mentions hardware inventory, "phần cứng", "Hardware ID", "kiểm kê", "dump", lspci, DSDT/SSDT, or before choosing any driver. NEVER dump hardware from the machine running Codex.
---

# hw-dump-reader

Codex chạy trên MÁY A; laptop đích là MÁY B. Dữ liệu phần cứng chỉ đến từ `laptop-specs.md` và
`docs/hw-dump/`. Không chạy lệnh nhận diện phần cứng trên máy hiện tại để "bù" dữ liệu thiếu.

## Bước 0 — Nhận diện định dạng dump
- Có `README.txt` ghi `Format: linux` hoặc có `lspci-nnk.txt` → **dump Linux** (ưu tiên, vì có DSDT/SSDT đi kèm).
- Có `pnp-devices.csv` → **dump Windows**.
- Có cả hai → dùng cả hai, đối chiếu chéo; Linux là nguồn chính cho ACPI/I2C, Windows cho tên thiết bị Windows.
- Linux driver (`iwlwifi`, `r8169`, `btusb`...) và ghi chú "supported" trong `laptop-specs.md` chỉ là GỢI Ý,
  không phải bằng chứng macOS hỗ trợ. Việc đó thuộc `driver-vetting`.

## Bước 1 — Kiểm tra dữ liệu có đủ không

**Dump Linux** cần có: `system.txt`, `cpu.txt`, `memory.txt`, `lspci-nnk.txt`, `lspci-nnvv.txt`, `lsusb.txt`,
`acpi-devices.csv` (cột name,hid,status,driver,path), `i2c-devices.txt`, `hid-devices.txt`, `input-devices.txt`,
`display.txt`, `audio.txt` (+ `audio-codec-full-*.txt`), `storage.txt`, `network.txt`, `power-sensors.txt`,
`firmware-options.txt`, và thư mục `acpi/` có `DSDT.aml` + các `SSDT*.aml`.

**Dump Windows** cần có: `system.txt`, `bios.txt`, `cpu.txt`, `gpu.txt`, `disks.txt`, `network.txt`, `monitors.txt`,
`pnp-devices.csv` (Class, Name, Status, InstanceId, HardwareIds, CompatibleIds, Location), `acpi-devices.csv`,
`pnp-key-classes.csv`. DSDT/SSDT phải dump riêng vào `acpi/`.

Phát hiện bất thường (báo cho người dùng, không đoán):
- `system.txt` (Manufacturer/Model, `product_name`/`board_name`) không khớp laptop trong `laptop-specs.md`
  → DỪNG, hỏi lại: có thể dump nhầm máy.
- `acpi/NOT-COPIED.txt` tồn tại hoặc thiếu `DSDT.aml` → chưa chạy bằng root; yêu cầu chạy lại với `sudo`.
- Thiếu Hardware ID cho Wi-Fi, Bluetooth, touchpad, audio, iGPU, dGPU, NVMe, card reader.
- Touchpad I2C: tìm trong `acpi-devices.csv`/`i2c-devices.txt` thiết bị dạng `ELAN*`, `SYNA*`, `MSFT0001`...
  và đường dẫn ACPI (`path`) của nó (ví dụ `\_SB_.PC00.I2C0.TPD0`). Nếu không thấy → hỏi người dùng.
- Bàn phím PS/2 và touchpad phải được ghi nhận RIÊNG (giao tiếp khác nhau).
- `firmware-options.txt`: không có MSR 0xE2 hoặc chưa đọc được → ghi "cần người dùng kiểm tra CFG Lock trong BIOS".
- Thiết bị trạng thái lỗi/không có driver bound vẫn phải ghi lại.

Nếu thiếu: nêu chính xác file/thông tin cần, hướng dẫn người dùng chạy lại script trên MÁY B, rồi DỪNG chờ.
(DSDT trên Windows: SSDTTime/acpidump; hoặc bản OpenCore debug với `Misc > Debug > SysReport`.)

## Bước 2 — Phân loại thiết bị
- **Linux:** `lspci -nnk` cho `[vendor:device]` và driver; `Subsystem:` nằm trong `lspci-nnvv.txt`.
  USB (Bluetooth, camera, vân tay) từ `lsusb.txt` dạng `ID vvvv:pppp`.
  Codec audio từ `audio.txt`/`audio-codec-full-*` (Vendor Id, Subsystem Id) để chọn layout-id sau này.
- **Windows:** tiền tố `HardwareIds` (`PCI\VEN_xxxx&DEV_xxxx&SUBSYS_...`, `USB\VID_xxxx&PID_xxxx`, `ACPI\xxxx`).

Lập nhóm: CPU/chipset · iGPU · dGPU · màn hình/panel · Wi-Fi · Bluetooth · Ethernet · audio (codec + controller) ·
mic · touchpad · bàn phím/Fn · SSD/NVMe · card reader · camera · vân tay · USB/Type-C/Thunderbolt · EC/pin ·
sensor/ALS/accelerometer · I2C/GPIO controller · TPM.
Mỗi thiết bị ghi: tên, ID đầy đủ (VEN:DEV + subsystem hoặc VID:PID hoặc ACPI HID), nguồn (file/dòng).
Chú ý mâu thuẫn giữa `laptop-specs.md` và dump (ví dụ ghi AX211 nhưng ID là `8086:2725`): nêu rõ, hỏi người dùng.

## Bước 3 — Ghi `docs/MACHINE-ANALYSIS.md`
Gồm: tóm tắt máy (model, CPU, đời iGPU), bảng thiết bị, BIOS (CFG Lock, VT-d, Above 4G, chế độ GPU, DVMT,
Secure Boot — từ dump nếu có, nếu không thì "cần người dùng kiểm tra"), các cổng xuất hình đi qua dGPU
(nếu có thể suy ra), danh sách THÔNG TIN CÒN THIẾU, và các điểm nghi ngờ.
Đánh dấu "CHƯA XÁC MINH" cho mọi suy đoán. Không đưa serial/UUID/MAC vào tài liệu.

## Bước 4
Cập nhật `docs/STATE.md`, trình tóm tắt 5–10 dòng cho người dùng và hỏi các thông tin còn thiếu.
Đây là đầu vào của `driver-vetting`.

## Đối chiếu với máy tham chiếu (R1)
Đọc `docs/REFERENCES.md`. Nếu repo R1 đã được clone vào `_cache/refs/`: so `scan/Report.json` và ACPI dump của repo với dump của
người dùng. Ghi vào MACHINE-ANALYSIS: board ID có thật sự giống (`8A4F`) không, khác biệt CPU/dGPU/BIOS, thiết bị ACPI nào
trùng tên/đường dẫn và nào khác. Dữ liệu của máy người dùng luôn thắng khi có khác biệt.
