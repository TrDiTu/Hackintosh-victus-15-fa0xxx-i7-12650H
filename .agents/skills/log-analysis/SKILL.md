---
name: log-analysis
description: Analyze logs the user brings back from the target laptop - OpenCore debug log, boot failure photos/text, kernel panic reports, kext load errors, dmesg/ioreg output, and XeGfx outputs (debug.xegfx_log, debug.xegfx_results, XeGfxProbe). Use whenever the user pastes or drops a log, says "bị treo", "panic", "không boot", "log", "lỗi", "stage fail", or reports that a device does not work after testing a build.
---

# log-analysis

Codex không chạy được trên MÁY B. Mọi bằng chứng đến từ log người dùng mang về. Phân tích có kỷ luật, không đoán.

## Quy trình
1. **Xác định đầu vào:** loại log, thời điểm (picker / kernel boot / sau khi vào macOS / sau sleep), build nào
   (`build-NN`), thay đổi nào so với lần test trước. Thiếu thì hỏi đúng thứ cần (ví dụ: ảnh dòng cuối trước khi treo,
   `boot-args` đang dùng, phiên bản OpenCore).
2. **Trích bằng chứng:** nêu các dòng log cụ thể (ngắn) làm cơ sở. Không kết luận khi không có dòng log đỡ.
3. **Phân loại nguyên nhân** theo giai đoạn:
   - Trước kernel (OpenCore/EFI): lỗi nạp driver `.efi`, ACPI/SSDT không nạp, Booter quirk, thiếu OpenRuntime,
     lỗi đọc config (lệch phiên bản ocvalidate).
   - Kernel/kext: kext không load (thiếu phụ thuộc, `MaxKernel`, sai thứ tự, chữ ký/prelink), panic có backtrace
     (ghi kext/hàm đầu stack), treo sau dòng nào.
   - Sau khi vào macOS: thiết bị không nhận (đối chiếu Hardware ID với DRIVER-MATRIX), sleep/wake lỗi, USB map.
   - XeGfx: xem mục dưới.
4. **Đối chiếu nguồn:** issue/tài liệu của kext hoặc dự án liên quan (có link). Không có bằng chứng → ghi
   "giả thuyết, CHƯA XÁC MINH" và nêu cách kiểm chứng.
5. **Đề xuất sửa nhỏ nhất:** một thay đổi mỗi lần nếu có thể, giải thích vì sao và rủi ro. Ghi vào
   `docs/BUILD-LOG.md`. Khi sửa xong thành EFI hoàn chỉnh → `efi-validate` → `efi-snapshot` (build mới).
6. Cập nhật `docs/STATE.md`: kết quả test của build này, lỗi còn mở.

## Mẫu báo cáo
```
Build: build-NN | Giai đoạn lỗi: ... | Triệu chứng: ...
Bằng chứng: "<dòng log ngắn>" (file/dòng)
Nguyên nhân khả dĩ (xếp theo xác suất, kèm mức tin cậy): 1) ... 2) ...
Cách kiểm chứng: ...   Đề xuất sửa: ...   Rủi ro: ...
```

## Log XeGfx (Giai đoạn B)
- Nguồn: `sysctl debug.xegfx_results` (kết quả từng stage), `debug.xegfx_log` (64 KiB log cuối của driver),
  registry `XeGfxProbe` (ID, BAR, GMD_ID, stolen-memory base, pipe A, GGTT entry, PCH watchdog).
- Kiểm tra theo trình tự: stage đã chạy có `pass`? watchdog `debug.xegfx_wdog` có kích hoạt (panic chủ ý)?
  Panic report nằm ở stage nào? So `XeGfxProbe` với mốc "sẵn sàng cho XeGfx" trong `docs/TEST-PLAN.md`
  (màn hình/pipe A còn scan-out như trước?).
- Đối chiếu README/issue/docs của XeGfx và các dự án liên quan (VedCloud, nmx-intel, JulioNectar...) cho triệu
  chứng tương tự. Đề xuất tinh chỉnh `debug.xegfx_env` chỉ khi tài liệu dự án nêu tham số đó.
- Chỉ đề xuất stage kế tiếp khi stage hiện tại đã có log kết quả từ người dùng và đạt tiêu chí.
- Nếu nghi lỗi của XeGfx: soạn sẵn nội dung báo cáo issue (log, máy, build, bước tái hiện, đã thử gì).
  KHÔNG tự gửi; người dùng quyết định.

## Không làm
- Không tuyên bố đã sửa khi chưa có test mới của người dùng. Không yêu cầu người dùng đăng serial/UUID
  (che chúng trong log nếu thấy). Không suy diễn nguyên nhân từ log không liên quan.
