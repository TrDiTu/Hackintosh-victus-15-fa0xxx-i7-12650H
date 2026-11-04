#!/usr/bin/env bash
# dump-igpu-stolen.sh — CHỈ ĐỌC. Chạy trên MÁY B (Victus) dưới Linux, KHÔNG chạy trên MÁY A.
# Mục đích: đo stolen memory / DVMT thật của iGPU 8086:46A3 (00:02.0).
# Cách chạy:  sudo bash dump-igpu-stolen.sh      (cần root để đọc config space > 64 byte và dmesg)
# Kết quả:    ./igpu-stolen-dump.txt  -> chép vào docs/hw-dump/ trên MÁY A.
# Script không ghi vào thiết bị, không sửa cấu hình; chỉ đọc và in.
set -u
OUT="${1:-./igpu-stolen-dump.txt}"
BDF="00:02.0"

sec() { printf '\n===== %s =====\n' "$1"; }
run() { printf '$ %s\n' "$*"; "$@" 2>&1 || printf '(lệnh lỗi hoặc không có quyền: mã %s)\n' "$?"; }

{
  echo "dump-igpu-stolen $(date -Is) kernel=$(uname -r)"
  [ "$(id -u)" -eq 0 ] || echo "CẢNH BÁO: không chạy bằng root, nhiều mục sẽ trống."

  sec "1. Nhận diện iGPU"
  run lspci -s "$BDF" -nn

  sec "2. dmesg: stolen / GSM / graphics memory (i915)"
  dmesg 2>&1 | grep -i -E "stolen|graphics memory|\bgsm\b|dsm|i915.*(memory|stolen)|GTT|ggtt" | head -40

  sec "3. Thanh ghi cấu hình PCI (đọc bằng setpci)"
  if command -v setpci >/dev/null 2>&1; then
    GGC=$(setpci -s "$BDF" 50.w 2>&1)   # GMCH Graphics Control (GGC)
    BDSM=$(setpci -s "$BDF" 5C.l 2>&1)    # BDSM kiểu cũ (gen9/10); gen11+ thường = 0
    BDSM64=$(setpci -s "$BDF" C0.l 2>&1)  # BDSM gen11+ (Alder Lake: offset 0xC0, bit0 = lock)
    echo "GGC    (0x50, word)  = $GGC"
    echo "BDSM   (0x5C, dword) = $BDSM"
    echo "BDSM64 (0xC0, dword) = $BDSM64"
    # Ghi chú: trên 46A3 offset 0x70 là PCIe Capability, KHÔNG phải BGSM.
    if [[ "$GGC" =~ ^[0-9a-fA-F]{4}$ ]]; then
      v=$((16#$GGC))
      gms=$(( (v >> 8) & 0xFF ))   # trường GMS bit 15:8
      ggms=$(( (v >> 6) & 0x3 ))   # trường GGMS bit 7:6
      echo "GMS  (bit 15:8) = 0x$(printf '%02x' "$gms")"
      echo "GGMS (bit 7:6)  = $ggms  (GTT = $(( ggms == 0 ? 0 : (1 << ggms) )) MB)"
      if   [ "$gms" -le 16 ];  then echo "-> DVMT Pre-Allocated (gen9+, GMS<=0x10) = $(( gms * 32 )) MB  [GIẢI MÃ SUY RA, cần đối chiếu dmesg]"
      elif [ "$gms" -ge 240 ]; then echo "-> GMS 0xF0..0xFF (gen9+) = $(( (gms - 239) * 4 )) MB  [GIẢI MÃ SUY RA, cần đối chiếu dmesg]"
      else echo "-> GMS=0x$(printf '%02x' "$gms") ngoài các dải đã biết: KHÔNG tự suy, chép nguyên giá trị về."; fi
    fi
  else
    echo "Không có setpci (gói pciutils)."
  fi

  sec "4. lspci -vv -xxx (64 byte đầu + vùng mở rộng)"
  run lspci -s "$BDF" -vv -xxx

  sec "5. /proc/iomem (vùng Graphics / stolen)"
  grep -i -E "graphics|stolen|00:02|i915" /proc/iomem 2>&1 | head -20

  sec "6. i915 debugfs (nếu có)"
  for f in /sys/kernel/debug/dri/0/i915_gem_objects /sys/kernel/debug/dri/0/i915_gem_stolen; do
    [ -r "$f" ] && { echo "--- $f"; head -20 "$f"; }
  done
  [ -d /sys/kernel/debug/dri ] || echo "(debugfs chưa mount hoặc không có DRI)"

  sec "7. Tuỳ chọn firmware liên quan (nếu hệ thống cho phép)"
  ls /sys/firmware/efi/efivars 2>/dev/null | grep -i -E "igd|dvmt|gfx|intelsetup" | head -10
  echo "(Ghi chú: BIOS HP không có menu DVMT, nên giá trị thật thường do firmware cố định.)"
} > "$OUT" 2>&1

echo "Xong. Kết quả: $OUT"
echo "Chép file này sang MÁY A vào docs/hw-dump/ rồi báo lại."
