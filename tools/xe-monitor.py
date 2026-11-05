#!/usr/bin/env python3
"""xe-monitor.py — CPU and iGPU monitor for the Victus on macOS (RUN ON MACHINE B, not on the Claude Code machine).

Read-only. Python 3 standard library (Xcode Command Line Tools python3). No root needed.

Sources:
- `sysctl debug.xepm.sensors` from NootedGreen JN @6f03560 (kern_xepm.cpp, always registered, no -ngreenpm needed):
  per-core temperature (TjMax - IA32_THERM_STATUS), core type (P/E from CPUID 0x1A), package temperature, and RAPL
  energy counters: package (MSR 0x611), IA cores (0x639), GT = iGPU (0x641). Power = energy delta / time.
- `ioreg -r -c IntelAccelerator -d 1 -a`: the accelerator's PerformanceStatistics (utilization, memory).

Usage:
  python3 xe-monitor.py                 # print one line per second
  python3 xe-monitor.py -i 2 -o run.csv # every 2 s, also write a CSV (for benchmark runs)
  python3 xe-monitor.py --gpu-keys      # list the iGPU PerformanceStatistics keys this driver exposes
Stop with Ctrl+C; a min/avg/max summary is printed.
"""
import argparse
import csv
import plistlib
import struct
import subprocess
import sys
import time

# struct XpSensors { uint32 ver, ncpu, tjmax, pkg; uint8 core[32], type[32]; uint32 eunit, pad; uint64 epkg, eia, egt; }
FMT = "<4I32s32s2I3Q"
SIZE = struct.calcsize(FMT)  # 112
CORE_P, CORE_E = 0x40, 0x20
GPU_KEYS = ("Device Utilization %", "Renderer Utilization %", "Tiler Utilization %", "GPU Activity(%)",
            "In use system memory", "Alloc system memory")


def read_sensors():
    raw = subprocess.run(["sysctl", "-b", "debug.xepm.sensors"], capture_output=True).stdout
    if len(raw) < SIZE:
        sys.exit("debug.xepm.sensors not available (%d bytes). Is NootedGreen JN @6f03560 loaded?" % len(raw))
    ver, ncpu, tjmax, pkg, core, typ, eunit, _pad, epkg, eia, egt = struct.unpack(FMT, raw[:SIZE])
    n = min(ncpu, 32)
    p = [core[i] for i in range(n) if typ[i] == CORE_P]
    e = [core[i] for i in range(n) if typ[i] == CORE_E]
    return {"pkg_c": pkg, "p_max_c": max(p) if p else None, "e_max_c": max(e) if e else None,
            "tjmax": tjmax, "unit": 1.0 / (1 << eunit), "e": (epkg, eia, egt), "t": time.monotonic()}


def read_gpu():
    out = subprocess.run(["ioreg", "-r", "-c", "IntelAccelerator", "-d", "1", "-a"], capture_output=True).stdout
    try:
        nodes = plistlib.loads(out) if out else []
    except Exception:
        return {}
    for node in nodes if isinstance(nodes, list) else [nodes]:
        stats = node.get("PerformanceStatistics")
        if isinstance(stats, dict):
            return stats
    return {}


def watts(a, b):
    dt = b["t"] - a["t"]
    out = []
    for x, y in zip(a["e"], b["e"]):
        d = (y - x) % (1 << 32)  # 32-bit RAPL counters wrap
        out.append(d * a["unit"] / dt if dt > 0 else 0.0)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--interval", type=float, default=1.0)
    ap.add_argument("-o", "--csv")
    ap.add_argument("--gpu-keys", action="store_true")
    a = ap.parse_args()

    if a.gpu_keys:
        for k, v in sorted(read_gpu().items()):
            print("%s = %s" % (k, v))
        return

    cols = ["time", "pkg_W", "cpu_W", "igpu_W", "pkg_C", "pcore_max_C", "ecore_max_C", "gpu_util_pct", "gpu_mem_MB"]
    w = None
    if a.csv:
        f = open(a.csv, "w", newline="")
        w = csv.writer(f)
        w.writerow(cols)
    print("  ".join("%10s" % c for c in cols[1:]))
    rows = []
    prev = read_sensors()
    try:
        while True:
            time.sleep(a.interval)
            cur = read_sensors()
            pw, cw, gw = watts(prev, cur)
            g = read_gpu()
            util = g.get("Device Utilization %", g.get("GPU Activity(%)"))
            mem = g.get("In use system memory")
            mem_mb = round(mem / 1048576, 1) if isinstance(mem, int) else None
            row = [round(pw, 2), round(cw, 2), round(gw, 2), cur["pkg_c"], cur["p_max_c"], cur["e_max_c"], util, mem_mb]
            print("  ".join("%10s" % ("-" if v is None else v) for v in row), flush=True)
            if w:
                w.writerow([time.strftime("%H:%M:%S")] + row)
                f.flush()
            rows.append(row)
            prev = cur
    except KeyboardInterrupt:
        pass
    if rows:
        print("\nsummary over %d samples (min / avg / max)" % len(rows))
        for i, name in enumerate(cols[1:]):
            vals = [r[i] for r in rows if isinstance(r[i], (int, float))]
            if vals:
                print("  %-12s %8.1f %8.1f %8.1f" % (name, min(vals), sum(vals) / len(vals), max(vals)))


if __name__ == "__main__":
    main()
