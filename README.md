# Bộ kit Codex — EFI OpenCore (macOS 26 Tahoe) + XeGfx

## Cấu trúc (chép vào thư mục gốc workspace của Codex trên MÁY A)
```
<workspace>/
├─ AGENTS.md                    quy tắc cứng (Codex tự đọc)
├─ PROMPT.md                    prompt khởi động (dán vào Codex)
├─ laptop-specs.md              (của bạn) cấu hình laptop
├─ config.toml.example          mẫu sandbox (chép vào ~/.codex/config.toml)
├─ tools/dump-laptop.ps1        chạy trên LAPTOP ĐÍCH (MÁY B)
├─ docs/STATE.md                bộ nhớ giữa các phiên
└─ .agents/skills/              8 skill (vị trí có thể khác tuỳ phiên bản Codex: đối chiếu tài liệu)
   ├─ hw-dump-reader   driver-vetting   ssdt-authoring   log-analysis   xegfx-runbook
   └─ efi-validate   efi-snapshot   usb-deploy-guard     (có script PowerShell)
```
