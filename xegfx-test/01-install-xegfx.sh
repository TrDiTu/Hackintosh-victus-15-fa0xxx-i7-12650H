#!/bin/bash
# 01-install-xegfx.sh
# Cai dat XeGfx.kext vao /Library/Extensions va build lai AuxiliaryKernelExtensions.kc
# Chay bang sudo tren macOS (May B). Khong load kext luc boot.
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
KEXT_SRC="${SCRIPT_DIR}/XeGfx.kext"
EXT="/Library/Extensions"
KC="/Library/KernelCollections/AuxiliaryKernelExtensions.kc"
K="/System/Library/Kernels/kernel"
KARG=(--allow-missing-kdk)
[ -f "$K" ] && KARG+=(--kernel "$K")
KB="/System/Library/KernelCollections/BootKernelExtensions.kc"
KS="/System/Library/KernelCollections/SystemKernelExtensions.kc"

[ "$(id -u)" = 0 ] || { echo "Loi: Vui long chay script voi sudo: sudo bash $0" >&2; exit 1; }
[ -d "${KEXT_SRC}" ] || { echo "Loi: Khong tim thay ${KEXT_SRC}" >&2; exit 1; }

echo "=== CAI DAT XEGFX VAO AUXILIARY KERNEL COLLECTION ==="

# 1. Sao luu AuxKC hien tai
BK="/Library/XeGfx/backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BK"
[ -f "$KC" ] && cp -p "$KC" "$BK/"
echo "[+] Da tao backup tai: $BK"

# 2. Liet ke danh sach kext thu ba hien co trong AuxKC de dam bao khong bi mat
OLD=$(kmutil inspect -a x86_64 -A "$KC" 2>/dev/null | awk -F'\t' '$1 ~ /^[a-z]+\.[A-Za-z0-9.-]+$/ && $1 !~ /^com\.apple\./ && $1 != "org.watchthelight.XeGfx" && $1 != "org.watchthelight.XeGfxAccel" && $1 != "com.nullmoth.NMIntelFB" && $1 != "org.watchthelight.XeGfxAGDC" {print $1}' || true)

# 3. Copy XeGfx.kext vao /Library/Extensions
rm -rf "$EXT/XeGfx.kext.new"
ditto "$KEXT_SRC" "$EXT/XeGfx.kext.new"
chown -R root:wheel "$EXT/XeGfx.kext.new"
chmod -R 755 "$EXT/XeGfx.kext.new"
rm -rf "$EXT/XeGfx.kext"
mv "$EXT/XeGfx.kext.new" "$EXT/XeGfx.kext"
echo "[+] Da sao chep XeGfx.kext vao $EXT/XeGfx.kext voi quyen root:wheel"

# 4. Build AuxKC moi
NEW="$KC.xegfx-new"
rm -f "$NEW"
echo "[+] Dang build collection moi..."
kmutil create -n boot sys "${KARG[@]}" -B "$KB" -S "$KS" --repository "$EXT" -a x86_64 "$NEW" -z "$BK/kmutil.log" 2>&1 || {
    cat "$BK/kmutil.log" || true
    echo "Loi: kmutil create that bai" >&2
    exit 1
}

# 5. Kiem tra tinh toan ven cua collection moi
INS=$(kmutil inspect -a x86_64 -A "$NEW" 2>/dev/null) || { echo "Loi: kmutil inspect that bai" >&2; exit 1; }
printf '%s\n' "$INS" | grep -q '^org.watchthelight.XeGfx[[:space:]]' || { echo "Loi: XeGfx thieu trong collection moi" >&2; exit 1; }

for b in $OLD; do
    printf '%s\n' "$INS" | grep -q "^$b[[:space:]]" || { echo "Canh bao: $b thieu trong collection moi" >&2; exit 1; }
done

mv -f "$NEW" "$KC"
echo "=== HOAN TAT CAI DAT ==="
echo "XeGfx.kext da duoc them vao Auxiliary Kernel Collection."
echo "CHU Y: XeGfx duoc thiet ke de KHONG tu dong load luc boot."
echo "Vui long khoi dong lai may (Reboot) de macOS nhan dien collection moi."
echo "Sau khi reboot, chay script 02-run-stage.sh de bat dau thu nghiem tung stage."