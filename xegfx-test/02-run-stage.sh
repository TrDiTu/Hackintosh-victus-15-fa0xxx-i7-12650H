#!/bin/bash
# 02-run-stage.sh
# Kich hoat va chay tung stage cua XeGfx (Stage 1 -> 4)
# Cu phap: sudo bash 02-run-stage.sh <1|2|3|4>
set -euo pipefail

STAGE="${1:-}"
if [ -z "$STAGE" ] || [[ ! "$STAGE" =~ ^[1-4]$ ]]; then
    echo "Cu phap su dung: sudo bash $0 <stage_number>"
    echo "Vi du: sudo bash $0 1    (Chay Stage 1: Shim state & memory self-test)"
    echo "       sudo bash $0 2    (Chay Stage 2: Read-only GPU probe)"
    echo "       sudo bash $0 3    (Chay Stage 3: Newbus & DMA)"
    echo "       sudo bash $0 4    (Chay Stage 4: DRM / i915 init - display off)"
    exit 1
fi

[ "$(id -u)" = 0 ] || { echo "Loi: Vui long chay voi quyen root: sudo bash $0 $STAGE" >&2; exit 1; }

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
LOG_DIR="${SCRIPT_DIR}/logs"
mkdir -p "${LOG_DIR}"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
LOG_FILE="${LOG_DIR}/stage${STAGE}-${TIMESTAMP}.log"

echo "=== BAT DAU KIEM THU XEGFX STAGE ${STAGE} ==="
echo "Ghi log tai: ${LOG_FILE}"

# 1. Kiem tra va load kext neu chua nạp
if ! kextstat | grep -q "org.watchthelight.XeGfx"; then
    echo "[+] XeGfx chua duoc nap. Dang chay: kmutil load -b org.watchthelight.XeGfx ..."
    kmutil load -b org.watchthelight.XeGfx || {
        echo "Loi: kmutil load that bai. Kiem tra xem da chay 01-install-xegfx.sh va reboot chua." >&2
        exit 1
    }
    sleep 1
fi

# 2. Xac nhan sysctl debug.xegfx_stage da san sang
if ! sysctl debug.xegfx_stage >/dev/null 2>&1; then
    echo "Loi: sysctl debug.xegfx_stage chua ton tai sau khi load kext." >&2
    exit 1
fi

CURRENT_STAGE=$(sysctl -n debug.xegfx_stage)
echo "[+] Trạng thái stage hien tai: ${CURRENT_STAGE}"

# Kiem tra thu tu tuan tu: khong duoc chay stage N neu chua qua stage N-1
if [ "$STAGE" -gt 1 ] && [ "$CURRENT_STAGE" -lt "$((STAGE - 1))" ]; then
    echo "Loi: Ban phai hoan thanh va pass Stage $((STAGE - 1)) truoc khi chay Stage ${STAGE}!" >&2
    echo "Vui long chay theo thu tu: 1 -> 2 -> 3 -> 4" >&2
    exit 1
fi

# 3. Kich hoat chay stage
echo "[+] Dang thuc thi: sysctl -w debug.xegfx_stage=${STAGE} ..."
sysctl -w debug.xegfx_stage="${STAGE}" || {
    echo "Canh bao: sysctl tra ve ma loi (co the do stage failed)" >&2
}

sleep 1

# 4. Thu thap ket qua
{
    echo "=========================================================="
    echo "XEGFX RUN REPORT - STAGE ${STAGE} - $(date)"
    echo "=========================================================="
    echo ""
    echo "--- 1. STAGE & RESULTS ---"
    echo "debug.xegfx_stage: $(sysctl -n debug.xegfx_stage 2>/dev/null || echo 'err')"
    echo "debug.xegfx_results (hex):"
    sysctl -b debug.xegfx_results 2>/dev/null | xxd || sysctl debug.xegfx_results || true
    echo ""

    if [ "$STAGE" -eq 2 ]; then
        echo "--- 2. IOREG XeGfxResident & XeGfxProbe ---"
        ioreg -p IOService -n XeGfxResident -l || echo "XeGfxResident not found"
        echo ""
    fi

    echo "--- 3. DRIVER CONSOLE OUTPUT (debug.xegfx_log) ---"
    sysctl -b debug.xegfx_log 2>/dev/null || echo "debug.xegfx_log empty or failed"
    echo ""

    echo "--- 4. RECENT SYSTEM LOGS ---"
    dmesg | tail -n 50 || true
    echo ""
} > "${LOG_FILE}"

echo "=== HOAN TAT STAGE ${STAGE} ==="
echo "Ket qua da duoc ghi vao: ${LOG_FILE}"
echo ""
echo "Tieu chi danh gia:"
echo "- Stage 1: debug.xegfx_results = 1 (pass, khong phai -12)"
echo "- Stage 2: debug.xegfx_results = 1, XeGfxProbe xuat hien trong IORegistry"
echo "- Stage 3: debug.xegfx_results = 1, newbus nhan dien Intel GPU"
echo "- Stage 4: debug.xegfx_results = 1, i915 khoi tao ma khong lam den/soc man hinh"
echo ""
echo "Vui long copy file ${LOG_FILE} hoac noi dung ve cho Codex phan tich truoc khi chay stage tiep theo!"