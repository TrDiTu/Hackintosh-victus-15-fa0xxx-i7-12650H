#!/usr/bin/env bash
# dump-laptop.sh
# RUN ON THE TARGET LAPTOP (machine B) under Linux (a live USB is fine). NOT on the Codex machine.
# Read-only: it only reads /sys, /proc and runs lspci/lsusb/etc. It never writes outside the output folder.
# Run as root so the ACPI tables and PCI details are readable:
#   sudo bash dump-laptop.sh            -> creates ./hw-dump
#   sudo bash dump-laptop.sh /path/out  -> creates /path/out
# Then copy the folder to <workspace>/docs/hw-dump/ on the machine that runs Codex.
#
# Privacy: serial numbers, UUIDs, MAC addresses, EDID serials and the Windows OEM key table (MSDM) are
# deliberately NOT collected.

set -u
OUT="${1:-./hw-dump}"
mkdir -p "$OUT/acpi"

have() { command -v "$1" >/dev/null 2>&1; }
is_root() { [ "$(id -u)" -eq 0 ]; }
rd() { cat "$1" 2>/dev/null; }

if ! is_root; then
  echo "WARNING: not running as root. ACPI tables, DMI memory info and some PCI details will be missing."
  echo "         Re-run with: sudo bash $0"
fi

# ---------- system / BIOS (DMI, no serial/UUID) ----------
{
  for f in sys_vendor product_name product_version product_family product_sku board_vendor board_name board_version bios_vendor bios_version bios_date bios_release; do
    if [ -r "/sys/class/dmi/id/$f" ]; then printf '%s: %s\n' "$f" "$(rd /sys/class/dmi/id/$f)"; fi
  done
  if [ -d /sys/firmware/efi ]; then echo "boot_mode: UEFI"; else echo "boot_mode: legacy BIOS"; fi
  . /etc/os-release 2>/dev/null && echo "running_os: ${PRETTY_NAME:-unknown}"
  echo "kernel: $(uname -r)"
  if have mokutil; then echo "secure_boot: $(mokutil --sb-state 2>&1 | head -n 1)"; fi
} > "$OUT/system.txt"

# ---------- CPU / memory ----------
if have lscpu; then lscpu > "$OUT/cpu.txt" 2>&1; else grep -m1 'model name' /proc/cpuinfo > "$OUT/cpu.txt"; fi
{
  grep -E 'MemTotal|SwapTotal' /proc/meminfo
  if is_root && have dmidecode; then
    echo "---- dmidecode -t memory (serial/asset/part filtered) ----"
    dmidecode -t memory 2>/dev/null | grep -viE 'serial|asset tag|part number'
  fi
} > "$OUT/memory.txt"

# ---------- PCI / USB ----------
if have lspci; then
  lspci -nnk > "$OUT/lspci-nnk.txt" 2>&1
  lspci -nnvv 2>&1 | grep -vi 'serial number' > "$OUT/lspci-nnvv.txt"
fi
if have lsusb; then
  { lsusb; echo; lsusb -t; } > "$OUT/lsusb.txt" 2>&1
fi

# ---------- ACPI devices (name, HID, status, bound driver, namespace path) ----------
{
  echo "name,hid,status,driver,path"
  for d in /sys/bus/acpi/devices/*; do
    [ -e "$d" ] || continue
    n=$(basename "$d")
    hid=$(rd "$d/hid")
    st=$(rd "$d/status")
    drv=""
    if [ -L "$d/driver" ]; then drv=$(basename "$(readlink "$d/driver")"); fi
    p=$(rd "$d/path")
    echo "$n,$hid,$st,$drv,$p"
  done
} > "$OUT/acpi-devices.csv"

# ---------- I2C / HID / input (trackpad, keyboard) ----------
{
  for d in /sys/bus/i2c/devices/*; do
    [ -e "$d" ] || continue
    drv=""
    if [ -L "$d/driver" ]; then drv=$(basename "$(readlink "$d/driver")"); fi
    echo "$(basename "$d") name=$(rd "$d/name") modalias=$(rd "$d/modalias") driver=$drv"
  done
} > "$OUT/i2c-devices.txt"
{
  for d in /sys/bus/hid/devices/*; do
    [ -e "$d" ] || continue
    echo "== $(basename "$d")"
    grep -E '^(HID_ID|HID_NAME|DRIVER)=' "$d/uevent" 2>/dev/null
  done
} > "$OUT/hid-devices.txt"
grep -vE '^U: Uniq' /proc/bus/input/devices > "$OUT/input-devices.txt" 2>/dev/null

# ---------- Display / GPU connectors / backlight ----------
{
  for c in /sys/class/drm/card*-*; do
    [ -e "$c" ] || continue
    echo "== $(basename "$c") status=$(rd "$c/status") enabled=$(rd "$c/enabled")"
    head -n 5 "$c/modes" 2>/dev/null
    if [ -s "$c/edid" ] && have edid-decode; then
      edid-decode "$c/edid" 2>/dev/null | grep -viE 'serial'
    fi
  done
  echo "== backlight"
  for b in /sys/class/backlight/*; do
    [ -e "$b" ] || continue
    echo "$(basename "$b") max_brightness=$(rd "$b/max_brightness") type=$(rd "$b/type")"
  done
} > "$OUT/display.txt"

# ---------- Audio codec ----------
{
  rd /proc/asound/cards
  for c in /proc/asound/card*/codec#*; do
    [ -e "$c" ] || continue
    echo "== $c"
    head -n 20 "$c"
  done
} > "$OUT/audio.txt"
for c in /proc/asound/card*/codec#*; do
  [ -e "$c" ] || continue
  cat "$c" > "$OUT/audio-codec-full-$(echo "$c" | tr '/#' '__').txt" 2>/dev/null
done

# ---------- Storage / network / power / sensors ----------
{
  have lsblk && lsblk -d -o NAME,MODEL,SIZE,TRAN,ROTA
  for n in /sys/class/nvme/nvme*; do
    [ -e "$n" ] || continue
    echo "$(basename "$n") model=$(rd "$n/model") firmware=$(rd "$n/firmware_rev")"
  done
} > "$OUT/storage.txt" 2>&1
{
  for n in /sys/class/net/*; do
    [ -e "$n/device" ] || continue
    drv=""
    if [ -L "$n/device/driver" ]; then drv=$(basename "$(readlink "$n/device/driver")"); fi
    echo "$(basename "$n") vendor=$(rd "$n/device/vendor") device=$(rd "$n/device/device") subsys_vendor=$(rd "$n/device/subsystem_vendor") subsys_device=$(rd "$n/device/subsystem_device") driver=$drv"
  done
} > "$OUT/network.txt"
{
  for p in /sys/class/power_supply/*; do
    [ -e "$p" ] || continue
    echo "$(basename "$p") type=$(rd "$p/type") manufacturer=$(rd "$p/manufacturer") model=$(rd "$p/model_name") technology=$(rd "$p/technology")"
  done
  for h in /sys/class/hwmon/*; do
    [ -e "$h" ] || continue
    echo "hwmon $(basename "$h") name=$(rd "$h/name")"
  done
} > "$OUT/power-sensors.txt"
lsmod > "$OUT/lsmod.txt" 2>&1

# ---------- Firmware options visible from Linux ----------
{
  echo "# VT-d / IOMMU hints from the kernel log"
  dmesg 2>/dev/null | grep -iE 'DMAR|IOMMU' | head -n 20
  echo
  echo "# CFG Lock (MSR 0xE2, bit 15 set = locked). Needs root + msr-tools."
  if is_root && have rdmsr; then
    modprobe msr 2>/dev/null
    echo "MSR 0xE2 = $(rdmsr -p0 0xe2 2>&1)"
  else
    echo "not available (install msr-tools and run as root to read it)"
  fi
} > "$OUT/firmware-options.txt"

# ---------- ACPI tables (binary). MSDM/SLIC are skipped on purpose (Windows OEM key). ----------
if is_root && [ -d /sys/firmware/acpi/tables ]; then
  for t in /sys/firmware/acpi/tables/*; do
    [ -f "$t" ] || continue
    b=$(basename "$t")
    case "$b" in MSDM|SLIC) continue ;; esac
    cp "$t" "$OUT/acpi/$b.aml" 2>/dev/null
  done
  if [ -d /sys/firmware/acpi/tables/dynamic ]; then
    for t in /sys/firmware/acpi/tables/dynamic/*; do
      [ -f "$t" ] || continue
      b=$(basename "$t")
      cp "$t" "$OUT/acpi/dyn-$b.aml" 2>/dev/null
    done
  fi
else
  echo "ACPI tables were not copied (need root)." > "$OUT/acpi/NOT-COPIED.txt"
fi

cat > "$OUT/README.txt" <<EOF
Created: $(date -Is)
Script: dump-laptop.sh (read-only; no serial/UUID/MAC/EDID-serial; MSDM/SLIC skipped)
Format: linux
Next: copy this folder to <workspace>/docs/hw-dump/ on the machine that runs Codex.
Decompile ACPI later with iasl (done by Codex via the ssdt-authoring skill), not here.
EOF

if [ -n "${SUDO_USER:-}" ]; then chown -R "$SUDO_USER" "$OUT" 2>/dev/null; fi
echo "Done. Output: $OUT"
echo "Copy the folder to <workspace>/docs/hw-dump/ on the Codex machine."
