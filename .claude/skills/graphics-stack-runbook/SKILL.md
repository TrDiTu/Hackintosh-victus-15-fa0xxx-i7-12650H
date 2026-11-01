---
name: graphics-stack-runbook
description: Plan and run Phase B - Metal acceleration for the Alder Lake-P iGPU 8086:46A3 (64 EU) using the JulioNectar NootedGreen stack (Apple TGL 16.0.32 driver + modified NootedGreen + libxedrv), with cheseecake's 64 EU port and khucxtriendev as references. Use only after the user wrote "EFI nền đã ổn định, bắt đầu tăng tốc đồ họa", or when the user asks about NootedGreen, device-id 9A49 spoof, install.sh, iGPU topology/EU/L3 banks, DVMT/stolen memory, or Metal on the iGPU.
---

# graphics-stack-runbook

## Cổng chặn
Chưa có câu xác nhận của người dùng ("EFI nền đã ổn định, bắt đầu tăng tốc đồ họa") → chỉ trả lời câu hỏi chung, không sửa EFI.

## Sự thật cần giữ (đọc lại bản mới nhất của repo trước khi dựa vào)
- Kết quả tốt nhất có bằng chứng: desktop/app tăng tốc Metal (family Mac2/Common3). **Không Metal 3**, không system sleep,
  không màn hình ngoài, không OpenGL phần cứng, AMFI phải hạ (`amfi_get_out_of_my_way=1` trong cấu hình của các repo),
  có thể GPU hang/panic.
- Bản vá được kiểm tra trên **macOS 26.7.1 (25G241)**. Bản khác → có thể hỏng; tắt tự động cập nhật.
- 46A3 = **64 EU**. Mặc định của JulioNectar là 96 EU → sai topology gây lỗi hình/treo.

## Pha 6 — Chuẩn bị (`docs/GRAPHICS-PLAN.md`, DỪNG chờ duyệt)
1. Clone bằng `python3 tools/clone_ref.py --url <url>`: JulioNectar (T1-1), cheseecake (T1-2), khucxtriendev (T2-1). Ghi commit vào kế hoạch.
2. Đọc: README, CHANGELOG, `docs/INSTALL.md`, `docs/STATUS.md`, `docs/KERNEL-PATCHES.md` của JulioNectar;
   `docs/PORT-I3-1220P.md` của cheseecake; issue #16, #24 của JulioNectar.
3. **Chọn fork NootedGreen**, so sánh: (a) JulioNectar + boot-arg topology; (b) cheseecake (64 EU sẵn). Tiêu chí: commit
   mới, có hỗ trợ ghi đè topology, có Actions build, khoảng cách với upstream. Ghi lý do.
4. **Topology**: lấy số DSS/subslice/EU/L3 bank thật từ `docs/hw-dump/` (Linux `i915_sseu_status`/`sseu_topology`) hoặc
   từ tester cùng máy. Tìm **tên boot-arg chính xác trong source của fork đã chọn** (grep `PE_parse_boot_argn`/`checkKernelArgument`).
   Không dùng tên boot-arg của fork khác. Ghi cách kiểm tra sau boot (`ioreg -rc IntelAccelerator -d1 | grep xe-topo` theo
   README JulioNectar).
5. **DVMT/stolen memory**: ghi giá trị thật (dump Linux: dmesg "stolen"). BIOS HP có thể ẩn DVMT. Đánh dấu rủi ro panic
   `IOAccelTask::release` (issue #24/#16) và cách thu log nếu gặp.
6. **DeviceProperties iGPU** `PciRoot(0x0)/Pci(0x2,0x0)`: `device-id` = `499A0000`, `AAPL,ig-platform-id` = `0000499A`
   (theo README cheseecake/issue #24, kiểm lại với config hiện tại của repo). Các thuộc tính khác lấy từ config.plist của repo
   đã chọn, mỗi key ghi nguồn + lý do; bỏ key riêng Dell/ThinkPad.
7. **boot-args**: lấy từ `EFI/OC/config.plist` hiện tại của repo đã chọn, lọc theo máy tôi. Ví dụ quan sát được trong issue #24
   (một người dùng, commit 2026-10-27) — CHỈ để đối chiếu, không chép:
   `IGLogLevel=3 -ngreentglwithgfx -allow3d -disablegfxfirmware ngreen-dmc=adlp -ngreenv189 -ngreenkeepefi -ngreenxefix
   -ngreenfixbootmode amfi_get_out_of_my_way=1 ngreenSched=4 ngreenV142=3 gfxrst=1 -wegnoegpu alcid=11`.
   `alcid=11` là của máy khác, không dùng. Thêm `-v keepsyms=1` cho các lần test đầu.
8. **Không** thêm `-ngreenpm` (XE-PM) ở lần đầu; thử sau khi ổn định, có bản EFI dự phòng.
9. **Tương tác với root patch OCLP của Wi-Fi** (AirportItlwm-Tahoe cần root patch Modern Wireless): kiểm tra thứ tự áp dụng
   (root patch trước hay sau `install.sh`), yêu cầu SIP/AMFI của cả hai, và việc cập nhật/áp lại patch có ghi đè file của
   nhau không. Nếu tài liệu hai bên không trả lời được, đề xuất thử trên bản sao lưu và ghi "CHƯA XÁC MINH".
10. Liệt kê những gì người dùng mất: SIP/AMFI hạ, không sleep, HDMI chết (đã chết do dGPU), cập nhật macOS có thể làm hỏng stack.

## Pha 7 — Runbook (`docs/GRAPHICS-RUNBOOK.md`) và EFI tăng tốc
Runbook cho người dùng chạy trên MÁY B (macOS 25G241 đã cài; install.sh cần mạng: Ethernet hoặc Wi-Fi AirportItlwm-Tahoe):
1. Sao lưu EFI đang boot; giữ USB có EFI nền.
2. `xcode-select --install`; clone repo đã chọn vào ổ APFS.
3. `zsh install.sh --check` → gửi kết quả cho Claude. Chỉ sau khi Claude xem → `zsh install.sh`.
4. Chép `build/NootedGreen.kext` (bản build trên chính máy đó, hoặc bản release của fork đã chọn) về MÁY A để Claude đưa vào EFI.
5. Không chạy `make-efi.sh`. Gỡ: `zsh install.sh --uninstall`.

Phía Claude (MÁY A):
- Thêm `NootedGreen.kext` (và kext phụ thuộc theo hướng dẫn của repo) vào `EFI/OC/Kexts`, DeviceProperties, boot-args.
- Giữ `config-install.plist` (không spoof, không NootedGreen) để quay về; trong runbook ghi cách đổi config.
- `efi-validate` → `efi-snapshot` (build mới, nhãn `graphics-v1`) → `usb-deploy-guard`.

## Pha 8 — Vòng test (`docs/GRAPHICS-PROGRESS.md`)
Kiểm tra sau boot (người dùng chạy, gửi kết quả):
- `kmutil showloaded | grep -iE 'nootedgreen|hookcase'`
- `ioreg -rc IntelAccelerator -d1` (topology, rowchk... theo README)
- `system_profiler SPDisplaysDataType`; ảnh màn hình About This Mac; panic report nếu có (`/Library/Logs/DiagnosticReports`).
Quy tắc: mỗi lần đổi **một** tham số; build mới khi đổi; ghi kết quả. Lỗi khởi tạo → quay về `config-install.plist`.
Dấu hiệu đã biết → xem `log-analysis`.

## Tuyên bố trung thực
Không nói "Metal hoạt động" khi chưa có kext đã load + Metal device trong `system_profiler` + người dùng xác nhận giao diện
mượt. Không bao giờ nói "Metal 3".
