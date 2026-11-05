#!/usr/bin/env bash
# map-usb-linux.sh — collect USB port data for a macOS USB map (UTBMap) from Linux.
# RUN ON THE TARGET LAPTOP (machine B) under Linux. NOT on the Claude Code machine.
# Read-only: reads /sys only (lspci for names). Writes one report file in the current directory.
#
# Why this works: every xHCI root-hub port in sysfs links to its ACPI node (firmware_node). That node's
# `adr` is the ACPI _ADR = the port number macOS / USBToolBox use (UTBMap "port"). Linux also pairs the
# USB2 (HS) and USB3 (SS) halves of one physical connector through `peer`.
#
# Usage:
#   bash map-usb-linux.sh            # interactive: plug a device into one port at a time
# For each physical port: plug a USB 3 stick -> Enter -> type a label (e.g. "left-front-A");
# then plug a USB 2 device (mouse/keyboard) into the SAME port -> Enter -> same label.
# For the USB-C port also try the stick in both orientations. Empty label + Enter = finish.

set -u
OUT="usb-map-$(date +%Y%m%d-%H%M%S).txt"

table() {
  for p in /sys/bus/usb/devices/usb*/*-0:1.0/usb*-port*; do
    [ -e "$p" ] || continue
    port=$(basename "$p")                       # usbB-portN
    bus=${port#usb}; bus=${bus%%-port*}; n=${port##*-port}
    hcd=$(readlink -f "/sys/bus/usb/devices/usb$bus/..")
    pci=$(basename "$hcd")
    ids="$(cat "$hcd/vendor" 2>/dev/null | sed 's/0x//'):$(cat "$hcd/device" 2>/dev/null | sed 's/0x//')"
    speed_hub=$(cat "/sys/bus/usb/devices/usb$bus/speed" 2>/dev/null)
    fw="$p/firmware_node"
    apath=$(cat "$fw/path" 2>/dev/null || echo -)
    adr=$(cat "$fw/adr" 2>/dev/null || echo -)
    ctype=$(cat "$p/connect_type" 2>/dev/null || echo -)
    peer=$(basename "$(readlink -f "$p/peer" 2>/dev/null)" 2>/dev/null); [ -n "$peer" ] || peer=-
    dev="/sys/bus/usb/devices/$bus-$n"
    if [ -e "$dev/idVendor" ]; then
      att="$(cat "$dev/idVendor"):$(cat "$dev/idProduct") speed=$(cat "$dev/speed") $(cat "$dev/product" 2>/dev/null | tr ' ' '_')"
    else
      att="-"
    fi
    printf '%s pci=%s %s hub=%sMbps port=%s adr=%s acpi=%s type=%s peer=%s dev=%s\n' \
      "$port" "$pci" "$ids" "$speed_hub" "$n" "$adr" "$apath" "$ctype" "$peer" "$att"
  done | sort -V
}

{
  echo "# map-usb-linux.sh $(date -Is)"
  echo "## xHCI controllers"
  lspci -nn 2>/dev/null | grep -i -E 'usb|thunderbolt' || echo "lspci not available"
  echo "## baseline (nothing plugged by you)"
  table
} > "$OUT"
echo "Baseline saved to $OUT"

prev=$(table)
while true; do
  read -r -p "Plug a device into ONE port, then type its label (empty = finish): " label
  [ -n "$label" ] || break
  sleep 2
  cur=$(table)
  {
    echo "## step: $label"
    diff <(echo "$prev") <(echo "$cur") | grep '^>' | sed 's/^> //' || true
  } | tee -a "$OUT"
  prev=$cur
done

{ echo "## final"; table; } >> "$OUT"
echo "Done. Send $OUT to Claude."
