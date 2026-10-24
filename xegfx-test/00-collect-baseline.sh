#!/bin/bash
# 00-collect-baseline.sh
# Thu thap thong so he thong mac dinh truoc khi thu nghiem XeGfx (Giai doan B)
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
LOG_DIR="${SCRIPT_DIR}/logs"
mkdir -p "${LOG_DIR}"

TIMESTAMP=$(date +%Y%m%d-%H%M%S)
OUT_FILE="${LOG_DIR}/baseline-${TIMESTAMP}.txt"

echo "=== DANG THU THAP BASELINE LOGS ==="
echo "Output: ${OUT_FILE}"

{
    echo "=========================================================="
    echo "BASELINE SYSTEM REPORT - $(date)"
    echo "=========================================================="
    echo ""
    echo "--- 1. MACOS VERSION ---"
    sw_vers
    uname -a
    echo ""

    echo "--- 2. BOOT ARGS ---"
    nvram boot-args 2>/dev/null || echo "Cannot read boot-args"
    echo ""

    echo "--- 3. LOADED THIRD-PARTY KEXTS ---"
    kextstat | grep -v "com.apple" || echo "No third-party kexts"
    echo ""

    echo "--- 4. PCI DISPLAY / GPU DEVICES ---"
    system_profiler SPPCIDataType 2>/dev/null || echo "SPPCIDataType failed"
    echo ""

    echo "--- 5. IOREG GFX0 / DISPLAY CONTROLLER ---"
    ioreg -l -p IODeviceTree | grep -A 30 -i "GFX0" || echo "GFX0 not found in IODeviceTree"
    echo ""

    echo "--- 6. FRAMEBUFFER / DISPLAY SERVICE ---"
    ioreg -rc AppleIntelFramebuffer 2>/dev/null || echo "AppleIntelFramebuffer not found"
    ioreg -rc IONDRVFramebuffer 2>/dev/null || echo "IONDRVFramebuffer not found"
    echo ""

    echo "--- 7. POWER ASSERTIONS & DGPU STATUS ---"
    pmset -g assertions
    echo ""
    ioreg -p IODeviceTree -l | grep -i "PEGP" || echo "PEGP (dGPU) not active"
    echo ""
} > "${OUT_FILE}"

echo "=== HOAN TAT BASELINE REPORT ==="
echo "Ket qua da luu tai: ${OUT_FILE}"