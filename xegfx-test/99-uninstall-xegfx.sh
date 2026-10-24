#!/bin/bash
# 99-uninstall-xegfx.sh
# Go bo hoan toan XeGfx khoi Auxiliary Kernel Collection va /Library/Extensions
# Chay voi sudo tren macOS (May B)
set -euo pipefail

EXT="/Library/Extensions"
KC="/Library/KernelCollections/AuxiliaryKernelExtensions.kc"
K="/System/Library/Kernels/kernel"
KARG=(--allow-missing-kdk)
[ -f "$K" ] && KARG+=(--kernel "$K")
KB="/System/Library/KernelCollections/BootKernelExtensions.kc"
KS="/System/Library/KernelCollections/SystemKernelExtensions.kc"

[ "$(id -u)" = 0 ] || { echo "Loi: Vui long chay voi sudo: sudo bash $0" >&2; exit 1; }

echo "=== GO BO XEGFX KHOI HE THONG ==="

# 1. Xoa kext khoi /Library/Extensions
rm -rf "$EXT/XeGfx.kext" "$EXT/XeGfxAccel.kext" "$EXT/NMIntelFB.kext" "$EXT/XeGfxAGDC.kext"
echo "[+] Da xoa cac kext XeGfx khoi $EXT"

# 2. Build lai collection sach
NEW="$KC.xegfx-clean"
rm -f "$NEW"
echo "[+] Dang build lai Auxiliary Kernel Collection sach..."
kmutil create -n boot sys "${KARG[@]}" -B "$KB" -S "$KS" --repository "$EXT" -a x86_64 "$NEW" 2>&1 || {
    echo "Loi: kmutil create that bai" >&2
    exit 1
}

mv -f "$NEW" "$KC"
echo "=== HOAN TAT GO BO ==="
echo "XeGfx da duoc go sach khoi he thong. Vui long reboot de ap dung."