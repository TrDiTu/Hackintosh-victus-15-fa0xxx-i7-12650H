# Bộ kit Claude Code — EFI OpenCore + tăng tốc iGPU (HP Victus 15-fa0xxx, macOS 26.7.1)

MÁY A (chạy Claude Code): **Linux**. MÁY B: laptop Victus. USB ghi EFI cắm vào MÁY A, bạn tự mount.

## Cấu trúc
```
<project>/
├─ CLAUDE.md                     quy tắc cứng, Claude Code tự nạp mỗi phiên
├─ PROMPT.md                     tin nhắn đầu tiên
├─ laptop-specs.md               (của bạn) cấu hình laptop
├─ secrets/smbios.json.example   mẫu serial: BẠN tự tạo secrets/smbios.json; Claude bị cấm đọc
├─ .gitignore                    loại secrets/, _cache/, snapshots/, hw-dump khỏi git
├─ config/usb-mount.txt.example  mẫu: một dòng là đường dẫn mount USB (Claude tạo usb-mount.txt khi bạn cho đường dẫn)
├─ .claude/
│  ├─ settings.json              quyền: hỏi trước lệnh ghi/xoá, cấm sudo và lệnh đĩa
│  └─ skills/                    12 skill
│     ├─ hw-dump-reader  driver-vetting  ssdt-authoring  log-analysis
│     ├─ graphics-stack-runbook  macos-install-runbook  smbios-secrets
│     └─ efi-validate  efi-snapshot  usb-deploy-guard  release-fetch  config-plist-tools   (script Python)
├─ tools/
│  ├─ dump-laptop.sh             chạy trên LAPTOP (Linux live USB, sudo) — ưu tiên
│  ├─ dump-laptop.ps1            chạy trên LAPTOP nếu laptop dùng Windows
│  ├─ clone_ref.py               clone repo tham khảo, vô hiệu hoá CLAUDE.md/AGENTS.md trong đó
│  └─ lib/efikit.py              hàm dùng chung
└─ docs/
   ├─ STATE.md                   bộ nhớ giữa các phiên
   └─ REFERENCES.md              nguồn tham chiếu theo tầng tin cậy
```

## Chuẩn bị trên MÁY A
- Cần `python3` (3.8+), `git`, `lsblk`/`findmnt` (util-linux). Tự cài `iasl` (gói `acpica-tools` hoặc `iasl`) khi tới bước SSDT;
  Claude không dùng `sudo`.
- Tải bản release OpenCore cùng phiên bản sẽ dùng, đặt vào `tools/`; `chmod +x .../Utilities/ocvalidate/ocvalidate.linux`.

## Các bước
1. Giải nén vào thư mục dự án, `cd` vào đó, chạy `claude`. Gõ `/permissions` để kiểm tra quy tắc đã nạp.
2. Trên LAPTOP: boot Linux live USB, `sudo bash dump-laptop.sh`, chép thư mục `hw-dump` vào `<project>/docs/hw-dump/`.
3. Sửa `laptop-specs.md`: iGPU `46A3` là GT1 UHD Graphics 64 EU; Wi-Fi `8086:2725` là AX210. Ghi thêm phiên bản
   AirportItlwm-Tahoe và cấu hình bạn đã chạy thử (macOS build, `DisableIoMapper`, root patch OCLP).
4. Dán nội dung `PROMPT.md` làm tin nhắn đầu tiên.
   (Muốn tránh giới hạn API GitHub khi tải kext: `export GITHUB_TOKEN=...` token chỉ đọc, trước khi chạy `claude`.)
5. Khi tới bước ghi USB: cắm USB vào MÁY A, mount phân vùng FAT32 (trình quản lý file thường tự mount vào
   `/media/<user>/<LABEL>`), báo đường dẫn cho Claude. Nếu Claude không ghi được vào đó, gõ `/add-dir <đường dẫn>`.

## Lưu ý
- `settings.json` là lớp bảo vệ thứ hai, không tuyệt đối: quy tắc Bash so khớp theo mẫu và có thể bị lách; quy tắc
  Read/Edit không chặn lệnh shell. Đọc kỹ mỗi lần Claude xin quyền, nhất là lệnh có `--confirmed`.
- Script ghi USB tự kiểm tra ổ là USB/removable và không chứa `/`, `/boot`, `/home` hay thư mục dự án, nhưng bạn vẫn
  phải tự xác nhận đúng USB ở bước chạy thử.
- Script dump Linux không thu serial/UUID/MAC và bỏ qua bảng ACPI `MSDM`/`SLIC` (khoá Windows OEM).
- Serial: tự sinh bằng `macserial`/GenSMBIOS và điền `secrets/smbios.json`; đừng dán serial vào cuộc trò chuyện. Không có
  file này thì USB nhận placeholder (vẫn boot, chỉ thiếu iCloud/iMessage).
- `known-good`: khi một bản build chạy tốt, nói với Claude "đánh dấu build-NN known-good".
- Giai đoạn B và root patch Wi-Fi chạy trên chính laptop (macOS); Claude chỉ viết runbook và phân tích log.
