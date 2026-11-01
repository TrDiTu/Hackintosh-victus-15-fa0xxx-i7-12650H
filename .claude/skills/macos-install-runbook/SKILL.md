---
name: macos-install-runbook
description: Plan and write the runbooks the user follows on the laptop to install and keep macOS 26.7.1 (25G241) - getting installer media from a Linux machine, BIOS settings, first boot with the base EFI, OCLP root patch for the AirportItlwm-Tahoe Wi-Fi, blocking macOS updates, moving OpenCore from USB to the internal ESP, and USB port mapping. Use for Phase 4-5 and before Phase B, or when the user says "cài macOS", "bộ cài", "installer", "recovery", "macrecovery", "root patch", "OCLP", "cập nhật macOS", "chặn update", "boot không cần USB", "USB map".
---

# macos-install-runbook

Claude chạy trên MÁY A (Linux) và chỉ VIẾT runbook. Mọi bước trên laptop do người dùng làm và báo lại.
Kết quả: `docs/INSTALL-RUNBOOK.md` (Giai đoạn A) và `docs/POSTINSTALL-RUNBOOK.md`. Đọc lại tài liệu nguồn mới nhất
trước khi viết, ghi ngày và link.

## 1. Bộ cài macOS — vấn đề cần giải trước (DỪNG, trình lựa chọn cho người dùng)
Yêu cầu: đúng **26.7.1 (25G241)**, vì stack đồ họa được kiểm tra trên build này, trong khi Apple đã có bản mới hơn
(WTLIntelGfx ghi nhận 26.7.2 / 25G332).
- Hỏi người dùng trước: đã có sẵn bộ cài hoặc bản cài nào chưa (họ đã chạy thử AirportItlwm-Tahoe trên build nào?),
  có máy Mac thật hoặc máy macOS nào để dùng `createinstallmedia` không.
- Nghiên cứu (ghi nguồn) và so sánh các cách, nêu rõ cách nào **ghim được build**:
  - Recovery online từ Linux bằng `macrecovery.py` trong `Utilities/macrecovery/` của release OpenCore (Dortania có
    hướng dẫn "Making the installer in Linux"). Cài qua mạng: cần Ethernet RTL8111 hoạt động trong recovery. Thường cài
    bản Apple đang phát hành → **có thể không ra 25G241**: phải xác minh trước.
  - Full installer `InstallAssistant.pkg` đúng build lấy từ catalog chính thức của Apple (công cụ như gibMacOS), rồi tạo
    USB cài bằng `createinstallmedia` trên một máy macOS. Không dùng mirror/ISO không chính thức.
  - Cách tạo USB từ Linux mà repo R1 (sulthonuladib, `tools/make-1401-stick.sh`) và nullmoth/1401 dùng: chỉ đọc để hiểu,
    không chạy script đó trên máy A khi chưa được người dùng đồng ý.
- Nếu không lấy được 25G241: ghi rõ hệ quả (stack đồ họa có thể không chạy; JulioNectar chỉ kiểm tra trên 25G241) và để
  người dùng quyết định.

## 2. Runbook cài đặt (Giai đoạn A, `docs/INSTALL-RUNBOOK.md`)
- BIOS: liệt kê thiết lập cần đổi theo MACHINE-ANALYSIS (Secure Boot tắt, chế độ ổ là AHCI/không VMD nếu có tuỳ chọn,
  không chọn chế độ chỉ-dGPU). Thiết lập không thấy trong BIOS HP → ghi "không có tuỳ chọn", không đoán.
- Sao lưu: dữ liệu và EFI/phân vùng Windows nếu dual boot; cách phân vùng cho macOS (APFS, GUID) — không xoá nhầm
  phân vùng khác; người dùng tự quyết.
- Lần boot đầu: dùng EFI nền (`config.plist` = `config-install.plist`), `-v keepsyms=1 debug=0x100`, OpenCore DEBUG.
  Cách chụp log (`Misc/Debug/Target`, file `opencore-*.txt` trên USB) để mang về cho `log-analysis`.
- Mạng lúc cài: Ethernet. Wi-Fi chưa có (root patch chỉ làm sau khi cài).

## 3. Sau khi cài (`docs/POSTINSTALL-RUNBOOK.md`)
Thứ tự đề xuất, mỗi bước có cách kiểm tra và cách quay lại:
1. **Chặn cập nhật macOS tự động** (System Settings › General › Software Update › Automatic Updates: tắt các mục tải và
   cài). Cập nhật sẽ làm mất root patch và có thể phá stack đồ họa. Ghi build hiện tại (`sw_vers`).
2. **Serial**: người dùng tạo `secrets/smbios.json` theo `smbios-secrets`, Claude ghi lại USB.
3. **Wi-Fi AirportItlwm-Tahoe**: theo INSTALL.md của kgp-macPro (bản đọc mới nhất): đúng release asset, `DisableIoMapper`
   theo cấu hình đã chọn, root patch Modern Wireless bằng fork OCLP được repo chỉ định. Ghi trạng thái SIP/AMFI mà root
   patch yêu cầu. Kiểm: Wi-Fi menu, kết nối, khởi động lại 3 lần. Thất bại → Ethernet vẫn dùng được, gửi log.
4. **USB map**: hướng dẫn người dùng map cổng (ví dụ USBToolBox) trên laptop; Claude đưa kext map vào EFI qua
   `config-plist-tools`, validate, build mới.
5. **Boot không cần USB** (chỉ khi người dùng muốn và EFI nền đã `known-good`): chép EFI vào ESP của ổ trong, giữ
   USB làm dự phòng; không động vào EFI của Windows (`EFI/Microsoft`). Người dùng tự làm, Claude chỉ viết các bước.
6. Trước Giai đoạn B: sao lưu toàn bộ (Time Machine hoặc ảnh ổ) — stack đồ họa và root patch đều sửa hệ thống.

## 4. Giữ hệ thống ổn định
- Mỗi lần người dùng muốn cập nhật macOS: dừng, kiểm tra JulioNectar/cheseecake và AirportItlwm-Tahoe đã hỗ trợ build
  mới chưa, ghi kế hoạch áp lại root patch và `install.sh`.
- Ghi mọi thay đổi trên laptop vào `docs/BUILD-LOG.md` (người dùng báo lại).
