# MÁY B — Vulkan SDK + NullMoth 2.9 trên volume dự phòng (build-69)

Chỉ làm trên **volume dự phòng** (26.7.2), boot bằng USB build-69 (`-nvrmnogo`: driver NVIDIA nạp nhưng chưa khởi động GPU).
Đường lui: build-63 ★ / ổ trong (volume chính). Không dùng app 1401 (nó tự sửa OpenCore).

## A. Vulkan (MoltenVK, như G2 trên volume chính)
1. Tải LunarG Vulkan SDK cho macOS từ https://vulkan.lunarg.com/sdk/home (volume chính đã dùng 1.4.363.1), cài vào `~/VulkanSDK`.
2. Kiểm:
   ```bash
   source ~/VulkanSDK/*/setup-env.sh
   mkdir -p ~/b70
   vulkaninfo --summary > ~/b70/vulkaninfo.txt 2>&1
   vkcube
   ```
   Mong: GPU Intel hiện trong `vulkaninfo`, `vkcube` quay. (Sau bước C: thêm GPU NVIDIA.)

## B. Cập nhật NullMoth 2.8.1 → 2.9
Lý do: 2.9 sửa việc giữ boot trên laptop lai có panel nối iGPU (#516), GSP kẹt, mode set lỗi lúc boot.
```bash
cd ~/Downloads
curl -fLO https://github.com/nullmoth/nvidia-macos-driver/releases/download/v2.9/nullmoth-nvidia-2.9.tar.gz
shasum -a 256 nullmoth-nvidia-2.9.tar.gz
# phải ra: b624bf07c78cea03043e096383d5c8b01e4fb2c804a6ba377a4e66a2566422ef
rm -rf pkgroot && tar -xzf nullmoth-nvidia-2.9.tar.gz && cd pkgroot
shasum -a 256 -c SHA256SUMS
sudo CHECK=1 ./install.sh 2>&1 | tee ~/b70/nm-check.txt
```
`CHECK=1` chỉ kiểm. Chỉ khi không báo lỗi:
```bash
sudo ./install.sh 2>&1 | tee ~/b70/nm-install.txt
```
**Chưa khởi động lại.** `install.sh` cài lại `NMXAudio.kext` (lần trước nó làm mất tiếng). Tắt nó rồi dựng lại AuxKC:
```bash
sudo mv /Library/Extensions/NMXAudio.kext /Library/NullMoth/NMXAudio.kext.disabled-2.9
sudo kmutil create -n aux --volume-root / --allow-missing-kdk --kernel /System/Library/Kernels/kernel \
  -B /System/Library/KernelCollections/BootKernelExtensions.kc -S /System/Library/KernelCollections/SystemKernelExtensions.kc \
  --repository /Library/Extensions -A /Library/KernelCollections/AuxiliaryKernelExtensions.kc -z 2>&1 | tee ~/b70/kmutil.txt
sudo shutdown -r now
```
Nếu `kmutil` báo lỗi: đừng khởi động lại, gửi `~/b70/kmutil.txt`.

## C. Khởi động GPU NVIDIA bằng tay (vẫn build-69)
Cắm HDMI trước khi bật máy. Vào desktop, kiểm tiếng, rồi:
```bash
kextstat 2>/dev/null | grep -i -E 'NVRM|NVAccel|NMX|VoodooHDA' > ~/b70/kexts.txt
sudo ./nvrm-go 1; echo "go1=$?"
sudo ./nvrm-go 2; echo "go2=$?"
sleep 20
system_profiler SPDisplaysDataType > ~/b70/displays.txt
vulkaninfo --summary > ~/b70/vulkaninfo-nv.txt 2>&1
log show --last 5m --predicate 'sender CONTAINS "NVRM" OR sender CONTAINS "NVAccel"' | tail -300 > ~/b70/nvrm.txt
```
(`nvrm-go` = công cụ đã build hôm 2026-11-10 từ `tools/nvrm-go.c`.)
Ghi lại: HDMI có hình không, panel trong còn bình thường không.
Panic/treo: boot lại build-69 (không chạy `nvrm-go`), chép `/Library/Logs/DiagnosticReports/*.panic` mới vào `~/b70/`.

Chép `~/b70` vào `logs/b70/`. Nếu C ổn → build-70 bỏ `-nvrmnogo` (GPU tự khởi động lúc boot).

## D. Kết quả (2026-11-10) và boot guard
- B xong: kext NVIDIA 2.9, VoodooHDA còn, không NMXAudio. A xong: MoltenVK 1.4.2 thấy GPU Intel.
- C (`nvrm-go` tay): RTX 3050 Ti Metal 4, nhưng HDMI không có desktop (`fb0 connect notify: nothing registered yet`) → cần auto-go lúc boot.
- **build-70** (bỏ `-nvrmnogo`): lần đầu NVRMFB/NVAccel không chạy vì boot guard đã đếm 2 lần (`boot guard: start 2 without a display so far`).
  Xoá bộ đếm rồi boot lại → **HDMI hoạt động** (người dùng xác nhận):
  ```bash
  sudo nvram -d 7C436110-AB2A-4BBB-A880-FE41995C9F82:nullmoth-nv-starts
  sudo shutdown -r now
  ```
- Đừng boot bằng build có `-nvrmnogo` nữa (mỗi lần như vậy tính một lần "không có màn hình"). Nếu NVIDIA lại hiện "Metal 2" và HDMI tối: chạy lại hai lệnh trên.

