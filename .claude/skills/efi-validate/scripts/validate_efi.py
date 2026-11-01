#!/usr/bin/env python3
"""Static checks for an OpenCore EFI folder, plus ocvalidate when available.

Usage (from the project root):
  python3 .claude/skills/efi-validate/scripts/validate_efi.py
  python3 .claude/skills/efi-validate/scripts/validate_efi.py --efi EFI --ocvalidate tools/OpenCore-1.0.x/Utilities/ocvalidate/ocvalidate.linux

Writes docs/validation/validate-<time>.md and docs/validation/latest.json.
Exit code: 0 = no errors, 1 = errors found.
"""
import argparse
import os
import plistlib
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "tools" / "lib"))
import efikit  # noqa: E402

NVRAM_GUID = "7C436110-AB2A-4BBB-A880-FE41995C9F82"
TAHOE_DARWIN = 25


class Report:
    def __init__(self):
        self.errors, self.warnings, self.infos = [], [], []

    def err(self, m):
        self.errors.append(m)

    def warn(self, m):
        self.warnings.append(m)

    def info(self, m):
        self.infos.append(m)


def load_plist(path):
    with open(path, "rb") as f:
        return plistlib.load(f)


def enabled(entry):
    return bool(entry.get("Enabled", True)) if isinstance(entry, dict) else True


def kernel_major(v):
    try:
        return int(str(v).split(".")[0])
    except ValueError:
        return None


def find_ocvalidate(root, given):
    if given:
        return Path(given)
    tools = root / "tools"
    if not tools.is_dir():
        return None
    cands = sorted(tools.rglob("ocvalidate.linux")) or [p for p in sorted(tools.rglob("ocvalidate")) if p.is_file()]
    return cands[0] if cands else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", default=None)
    ap.add_argument("--efi", default=None)
    ap.add_argument("--ocvalidate", default=None)
    a = ap.parse_args()

    root = Path(a.workspace).resolve() if a.workspace else efikit.project_root_from(__file__)
    efi = Path(a.efi).resolve() if a.efi else root / "EFI"
    r = Report()
    if not efi.is_dir():
        print("FATAL: EFI folder not found: %s" % efi)
        return 1
    oc = efi / "OC"

    # 1. structure
    for rel in ("BOOT/BOOTx64.efi", "OC/OpenCore.efi", "OC/config.plist"):
        if not (efi / rel).is_file():
            r.err("Missing required file: " + rel)
    for rel in ("OC/Drivers", "OC/Kexts", "OC/ACPI"):
        if not (efi / rel).is_dir():
            r.warn("Folder missing: %s (ok only if unused)" % rel)

    cfg = None
    if (oc / "config.plist").is_file():
        try:
            cfg = load_plist(oc / "config.plist")
        except Exception as e:
            r.err("config.plist is not a valid plist: %s" % e)

    order = []
    boot_args = ""
    if isinstance(cfg, dict):
        # 2. ACPI
        referenced = set()
        for e in cfg.get("ACPI", {}).get("Add", []) or []:
            p = e.get("Path")
            if not p:
                continue
            referenced.add(p.lower())
            if enabled(e) and not (oc / "ACPI" / p).is_file():
                r.err("ACPI/Add enabled but file missing: OC/ACPI/" + p)
        if (oc / "ACPI").is_dir():
            for f in sorted((oc / "ACPI").glob("*.aml")):
                if f.name.lower() not in referenced:
                    r.warn("File in OC/ACPI not referenced by config.plist: " + f.name)

        # 3. Kernel/Add
        kref = set()
        for idx, e in enumerate(cfg.get("Kernel", {}).get("Add", []) or []):
            bundle = e.get("BundlePath")
            if not bundle:
                continue
            kref.add(bundle.lower())
            if not enabled(e):
                continue
            bdir = oc / "Kexts" / bundle
            if not bdir.is_dir():
                r.err("Kernel/Add enabled but bundle missing: OC/Kexts/" + bundle)
                continue
            exe = e.get("ExecutablePath")
            if exe and not (bdir / exe).is_file():
                r.err("ExecutablePath missing for %s: %s" % (bundle, exe))
            ipath = bdir / (e.get("PlistPath") or "Contents/Info.plist")
            if not ipath.is_file():
                r.err("PlistPath missing for %s: %s" % (bundle, e.get("PlistPath")))
            mx, mn = kernel_major(e.get("MaxKernel", "")), kernel_major(e.get("MinKernel", ""))
            if e.get("MaxKernel") and mx is not None and mx < TAHOE_DARWIN:
                r.warn("%s has MaxKernel=%s which excludes macOS 26 Tahoe (Darwin 25)." % (bundle, e["MaxKernel"]))
            if e.get("MinKernel") and mn is not None and mn > TAHOE_DARWIN:
                r.warn("%s has MinKernel=%s which is newer than Tahoe (Darwin 25)." % (bundle, e["MinKernel"]))
            bid, deps = "", []
            if ipath.is_file():
                try:
                    info = load_plist(ipath)
                    bid = info.get("CFBundleIdentifier", "")
                    deps = list((info.get("OSBundleLibraries") or {}).keys())
                except Exception as ex:
                    r.warn("Cannot parse Info.plist of %s: %s" % (bundle, ex))
            order.append({"index": idx, "bundle": bundle, "id": bid, "deps": deps})

        id_to_index = {o["id"]: o["index"] for o in order if o["id"]}
        for o in order:
            for d in o["deps"]:
                if d.startswith("com.apple."):
                    continue
                if d not in id_to_index:
                    r.err("%s depends on '%s' but no enabled kext in Kernel/Add provides it." % (o["bundle"], d))
                elif id_to_index[d] > o["index"]:
                    r.err("Load order: %s (position %d) must come AFTER its dependency '%s' (position %d)."
                          % (o["bundle"], o["index"], d, id_to_index[d]))
        seen = {}
        for o in order:
            seen[o["bundle"]] = seen.get(o["bundle"], 0) + 1
        for b, n in seen.items():
            if n > 1:
                r.warn("Duplicate enabled kext entry: " + b)
        if (oc / "Kexts").is_dir():
            for k in sorted((oc / "Kexts").glob("*.kext")):
                if k.name.lower() not in kref:
                    r.warn("Kext in OC/Kexts not referenced by config.plist: " + k.name)

        # 4. UEFI/Drivers
        dref, runtime_on = set(), False
        for e in cfg.get("UEFI", {}).get("Drivers", []) or []:
            name = e if isinstance(e, str) else e.get("Path")
            if not name:
                continue
            dref.add(name.lower())
            if enabled(e):
                if name.lower() == "openruntime.efi":
                    runtime_on = True
                if not (oc / "Drivers" / name).is_file():
                    r.err("UEFI/Drivers enabled but file missing: OC/Drivers/" + name)
        if not runtime_on:
            r.err("OpenRuntime.efi is not enabled in UEFI/Drivers (required).")
        if (oc / "Drivers").is_dir():
            for f in sorted((oc / "Drivers").glob("*.efi")):
                if f.name.lower() not in dref:
                    r.warn("Driver in OC/Drivers not referenced by config.plist: " + f.name)

        # 5. Misc/Tools
        misc = cfg.get("Misc", {})
        for e in misc.get("Tools", []) or []:
            p = e.get("Path")
            if p and enabled(e) and not (oc / "Tools" / p).is_file():
                r.err("Misc/Tools enabled but file missing: OC/Tools/" + p)

        # 6. facts (no secrets printed)
        r.info("Misc/Security/SecureBootModel = %s" % misc.get("Security", {}).get("SecureBootModel"))
        r.info("Misc/Debug/Target = %s" % misc.get("Debug", {}).get("Target"))
        boot_args = str(cfg.get("NVRAM", {}).get("Add", {}).get(NVRAM_GUID, {}).get("boot-args", ""))
        r.info("NVRAM boot-args = " + boot_args)

        gen = cfg.get("PlatformInfo", {}).get("Generic", {})
        if gen:
            r.info("PlatformInfo SystemProductName = %s" % gen.get("SystemProductName"))
            for k in ("SystemSerialNumber", "MLB", "SystemUUID"):
                v = str(gen.get(k, "") or "")
                if not v or v.startswith("CHANGE_ME") or v.strip("0-") == "":
                    r.info("PlatformInfo %s = PLACEHOLDER (user must generate with macserial)" % k)
                else:
                    r.warn("PlatformInfo %s contains a real-looking value (not printed). Keep it out of logs and repos." % k)

        igpu = cfg.get("DeviceProperties", {}).get("Add", {}).get("PciRoot(0x0)/Pci(0x2,0x0)")
        if igpu:
            r.info("iGPU DeviceProperties keys = " + ", ".join(sorted(igpu.keys())))
            for k in ("device-id", "AAPL,ig-platform-id"):
                v = igpu.get(k)
                if isinstance(v, (bytes, bytearray)):
                    r.info("iGPU %s = %s" % (k, v.hex().upper()))
        else:
            r.info("iGPU DeviceProperties: none (no spoof; expected for the base / install config)")
        if "ngreen" in boot_args.lower() and not any(o["bundle"].lower().startswith("nootedgreen") for o in order):
            r.warn("boot-args contain ngreen* flags but NootedGreen.kext is not enabled in Kernel/Add.")

    # 7. ocvalidate
    ocv = find_ocvalidate(root, a.ocvalidate)
    ocv_ran, ocv_exit, ocv_out = False, None, ""
    if ocv and ocv.is_file():
        if not os.access(ocv, os.X_OK):
            r.err("ocvalidate is not executable: %s (chmod +x it)" % ocv)
        else:
            try:
                p = subprocess.run([str(ocv), str(oc / "config.plist")], capture_output=True, text=True, timeout=120)
                ocv_ran, ocv_exit, ocv_out = True, p.returncode, (p.stdout + p.stderr)
                if p.returncode != 0:
                    r.err("ocvalidate reported issues (exit code %d). See report." % p.returncode)
            except OSError as e:
                r.err("Cannot run %s: %s (use ocvalidate.linux from the matching OpenCore release)" % (ocv, e))
    else:
        r.err("ocvalidate not found. Put the OpenCore release that matches OpenCore.efi in tools/ "
              "(Utilities/ocvalidate/ocvalidate.linux). Result is UNVERIFIED without it.")

    th = efikit.tree_hash(efi)
    vdir = root / "docs" / "validation"
    vdir.mkdir(parents=True, exist_ok=True)
    stamp = efikit.now_iso().replace(":", "").replace("-", "")
    report = [
        "# EFI validation report", "",
        "- time: " + efikit.now_iso(), "- efi: " + str(efi), "- tree-sha256: " + th,
        "- errors: %d, warnings: %d" % (len(r.errors), len(r.warnings)),
        "- ocvalidate: " + ("ran, exit %s" % ocv_exit if ocv_ran else "NOT RUN"),
        "", "## Errors"] + (["- " + m for m in r.errors] or ["(none)"]) + [
        "", "## Warnings"] + (["- " + m for m in r.warnings] or ["(none)"]) + [
        "", "## Info"] + ["- " + m for m in r.infos] + [
        "", "## ocvalidate output", "```", ocv_out.rstrip(), "```"]
    (vdir / ("validate-%s.md" % stamp)).write_text("\n".join(report) + "\n", encoding="utf-8")
    efikit.write_json(vdir / "latest.json", {
        "time": efikit.now_iso(), "efiPath": str(efi), "treeHash": th,
        "errors": len(r.errors), "warnings": len(r.warnings),
        "ocvalidateRan": ocv_ran, "ocvalidateExit": ocv_exit,
    })

    print("Validated: %s" % efi)
    print("Errors: %d  Warnings: %d  ocvalidate: %s" % (len(r.errors), len(r.warnings), "ran" if ocv_ran else "NOT RUN"))
    for m in r.errors:
        print("  [ERROR] " + m)
    for m in r.warnings:
        print("  [WARN]  " + m)
    print("Report: docs/validation/validate-%s.md" % stamp)
    return 1 if r.errors else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print("FATAL: %s" % e)
        sys.exit(1)
