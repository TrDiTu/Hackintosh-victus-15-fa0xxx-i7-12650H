#!/bin/bash
# Run on machine B in macOS. Collect only input-device diagnostics.
set -u
if [ "$(uname -s)" != Darwin ]; then
    echo "Run this script on the target laptop in macOS."
    exit 1
fi
out="${1:-$PWD/touchpad-$(date +%Y%m%d-%H%M%S)}"
mkdir -p "$out" || exit 1
sw_vers > "$out/macos.txt"
sysctl -n kern.bootargs > "$out/boot-args.txt" 2>&1
for name in I2C0 TPD0 GPI0; do
    ioreg -r -l -w0 -n "$name" > "$out/ioreg-$name.txt" 2>&1
done
kmutil showloaded 2>&1 | grep -Ei 'Voodoo|error|denied' > "$out/loaded-input-kexts.txt"
/usr/bin/log show --last boot --style compact \
    --predicate 'process == "kernel" AND (eventMessage CONTAINS[c] "VoodooI2C" OR eventMessage CONTAINS[c] "VoodooGPIO" OR eventMessage CONTAINS[c] "ELAN0788")' \
    > "$out/input-kernel-log.txt" 2>&1
echo "Diagnostics: $out"
echo "Copy this directory back into the project's logs directory."
