# NVIDIA-RUNBOOK — thử NullMoth NVIDIA driver cho RTX 3050 Ti (branch `nvidia-gpu`, THỬ NGHIỆM)

Mục tiêu: Metal 3 trên dGPU cho app tự chọn dGPU, và cổng HDMI (nối vào dGPU). **Panel trong vẫn chạy trên iGPU**
(NootedGreen): máy là muxless, driver không có bộ chuyển màn hình Optimus (`docs/CARD-SUPPORT.md` của NullMoth).
Nguồn: github.com/nullmoth/nvidia-macos-driver, release **v2.7.2** (2026-11-05), PolyForm Noncommercial 1.0.0
(dùng cá nhân được). Ampere (RTX 30) trên máy thật: "Pending" theo tác giả. Đánh giá đầy đủ: `docs/DRIVER-MATRIX.md` (D1).

Đường lui: **build-48** (known-good, dGPU tắt). Không dùng app 1401 (nó tự sửa OpenCore).

## Build-49 (EFI) — đã đổi so với build-48
| Mục | build-48 | build-49 | Lý do |
|---|---|---|---|
| `SSDT-DGPU-OFF.aml` | bật | **tắt** | dGPU phải sống |
| DeviceProperties `PciRoot(0x0)/Pci(0x1,0x0)/Pci(0x0,0x0)` `disable-gpu` | có | **xoá** | như trên |
| `AMFIPass.kext` + `-amfipassbeta` | không | **có** | README NullMoth yêu cầu |
| `csr-active-config` | `0x0A13` | **`0x0A53`** | phải chứa `0x0A43` (README) |
| boot-args | 160 | **255** (đầy) | thêm `nvfb=1 nvaccel=1 nvfbheads=4 -nvkmsnosmooth amfi=0x80 ipc_control_port_options=0` (đều đọc bằng `PE_parse_boot_argn`) |

`SecureBootModel` đã là `Disabled`. Resizable BAR: tác giả khuyên bật; BIOS HP có tuỳ chọn không — CHƯA XÁC MINH.

## Bước 1 — boot build-49, CHƯA cài driver
Mục đích: biết riêng ảnh hưởng của việc để dGPU sống.
```
system_profiler SPDisplaysDataType | grep -i -E 'Chipset|Metal|Vendor'
ioreg -r -c IOPCIDevice -d1 | grep -i -A2 '"vendor-id" = <de100000>' | head
kmutil showloaded --list-only | grep -i -E 'TGL|HookCase|AirportItlwm|voodoo|AMFIPass'
```
Rồi đo công suất nghỉ 2 phút (`python3 xe-monitor.py -o ~/idle-dgpu-on.csv`). So với ~8 W (dGPU tắt).
Panic / không boot → build-48, gửi `.panic`.

## Bước 2 — cài driver (MÁY B, cần mạng)
Cắm màn hình HDMI nếu có: driver có "boot guard" tự tắt sau 2 lần khởi động liền không bật được màn hình;
trên máy muxless mà không có HDMI có thể bị tắt (CHƯA XÁC MINH).
```
cd ~/Downloads
curl -fLO https://github.com/nullmoth/nvidia-macos-driver/releases/download/v2.7.2/nullmoth-nvidia-2.7.2.tar.gz
curl -fLO https://github.com/nullmoth/nvidia-macos-driver/releases/download/v2.7.2/SHA256SUMS.txt
shasum -a 256 -c SHA256SUMS.txt --ignore-missing
tar -xzf nullmoth-nvidia-2.7.2.tar.gz && cd pkgroot
shasum -a 256 -c SHA256SUMS
sudo CHECK=1 ./install.sh
```
`CHECK=1` chỉ kiểm (dựng thử kernel collection, không đổi gì). Gửi output cho Claude. Chỉ khi PASS:
```
sudo ./install.sh
```
**Đừng khởi động lại ngay.** Trên macOS 26, `install.sh` tự cài thêm **`NMXAudio.kext`** (driver HD Audio của họ),
sẽ tranh bộ điều khiển âm thanh với VoodooHDA. Giữ VoodooHDA (đã chạy tốt) → gỡ NMXAudio rồi dựng lại Auxiliary KC:
```
sudo rm -rf /Library/Extensions/NMXAudio.kext
sudo kmutil create -n aux --volume-root / --allow-missing-kdk --kernel /System/Library/Kernels/kernel \
  -B /System/Library/KernelCollections/BootKernelExtensions.kc -S /System/Library/KernelCollections/SystemKernelExtensions.kc \
  --repository /Library/Extensions -A /Library/KernelCollections/AuxiliaryKernelExtensions.kc -z
sudo shutdown -r now
```
macOS hỏi duyệt kext → System Settings › Privacy & Security › Allow → khởi động lại lần nữa.

## Bước 3 — kiểm
```
kmutil showloaded | grep -i -E 'nullmoth|TGL|HookCase|voodoo'
system_profiler SPDisplaysDataType | grep -i -E 'Chipset|Metal'
ioreg -rc IntelAccelerator -d1 | grep xe-topo
```
Mong: hai GPU trong System Information; Intel vẫn Metal 2 và vẫn điều khiển panel; NVIDIA báo Metal 3.
Kiểm: âm thanh (VoodooHDA), Wi-Fi, HDMI (nếu có), công suất nghỉ, nhiệt.

## Gỡ
NullMoth có "Remove NVIDIA driver" trong 1401; bằng tay:
```
sudo rm -rf /Library/Extensions/{NVRM,NVAccel,NVRMFB,NVRMAGDC}.kext /Library/GPUBundles/{NVMTLDriver.bundle,NVIDIAShared.bundle,nvmtl,nvmtl-allow.txt} /Library/NullMoth
sudo kmutil create … (như trên) && sudo shutdown -r now
```
rồi boot build-48.
