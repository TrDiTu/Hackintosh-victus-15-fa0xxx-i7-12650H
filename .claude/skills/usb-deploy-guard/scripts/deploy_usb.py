#!/usr/bin/env python3
"""Safely mirror <project>/EFI to <usb-mount>/EFI on Linux.

Step 1 (dry run, default):  python3 .claude/skills/usb-deploy-guard/scripts/deploy_usb.py --mount /media/me/EFI
Step 2 (real write):        ... deploy_usb.py --mount /media/me/EFI --confirmed   (ONLY after the user approved step 1)
The mount path may also be stored (one line) in config/usb-mount.txt.

Enforced here:
  - the mount path is an actual mount point whose disk is USB / removable / hotplug;
  - no partition of that disk is mounted at /, /boot, /boot/efi, /home, /usr, /var, or holds the project;
  - writes only inside <mount>/EFI; never formats, partitions, mounts or unmounts anything; no sudo;
  - a clean, up-to-date efi-validate result for exactly this EFI content is required;
  - an existing OpenCore EFI on the USB is snapshotted first (efi-snapshot);
  - the copy is verified by tree hash;
  - if secrets/smbios.json exists, serials are injected into a temporary staged copy only (project EFI keeps
    placeholders), the staged copy is written to the USB and deleted; values are never printed.
Exit codes: 0 ok, 1 error, 4 validation gate failed, 5 existing <mount>/EFI needs user attention, 6 snapshot blocked.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "tools" / "lib"))
import efikit  # noqa: E402
import smbios  # noqa: E402

SYSTEM_MOUNTS = {"/", "/boot", "/boot/efi", "/efi", "/home", "/usr", "/var"}


def run_json(cmd):
    out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def truthy(v):
    return v is True or str(v).lower() in ("1", "true")


def disk_info(source):
    """Return (partition, parent_disk) dicts from lsblk for a block device path."""
    cols = "NAME,PATH,PKNAME,TYPE,TRAN,RM,HOTPLUG,SIZE,MODEL,LABEL,FSTYPE,MOUNTPOINTS"
    try:
        part = run_json(["lsblk", "-J", "-b", "-o", cols, source])["blockdevices"][0]
    except subprocess.CalledProcessError:
        cols = cols.replace("MOUNTPOINTS", "MOUNTPOINT")
        part = run_json(["lsblk", "-J", "-b", "-o", cols, source])["blockdevices"][0]
    pk = part.get("pkname")
    disk = part
    if pk:
        disk = run_json(["lsblk", "-J", "-b", "-o", cols, "/dev/" + pk])["blockdevices"][0]
    return part, disk


def mountpoints_of(dev):
    mps = dev.get("mountpoints")
    if mps is None:
        mps = [dev.get("mountpoint")]
    out = [m for m in (mps or []) if m]
    for ch in dev.get("children", []) or []:
        out += mountpoints_of(ch)
    return out


def file_map(root):
    m = {}
    if not root.is_dir():
        return m
    for dirpath, _dirs, files in os.walk(root):
        for n in files:
            if n in efikit.IGNORE_NAMES or n.startswith("._"):
                continue
            p = Path(dirpath) / n
            m[p.relative_to(root).as_posix().lower()] = p
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", default=None)
    ap.add_argument("--mount", default=None)
    ap.add_argument("--source", default=None)
    ap.add_argument("--confirmed", action="store_true")
    ap.add_argument("--no-smbios", action="store_true", help="deploy placeholders even if secrets/smbios.json exists")
    a = ap.parse_args()

    root = Path(a.workspace).resolve() if a.workspace else efikit.project_root_from(__file__)
    mount = a.mount
    if not mount:
        cfg = root / "config" / "usb-mount.txt"
        if cfg.is_file():
            mount = cfg.read_text(encoding="utf-8").strip()
    if not mount:
        print("ERROR: no USB mount path. Ask the user for it, pass --mount or write config/usb-mount.txt.")
        return 1
    mount = os.path.realpath(mount)

    # ---- identify the USB ----
    if not os.path.ismount(mount):
        print("ERROR: %s is not a mount point. Ask the user to mount the USB's FAT32 partition." % mount)
        return 1
    if mount in SYSTEM_MOUNTS:
        print("ERROR: %s is a system mount. Refusing." % mount)
        return 1
    fm = run_json(["findmnt", "-J", "-n", "-o", "TARGET,SOURCE,FSTYPE", "--mountpoint", mount])["filesystems"][0]
    source = fm["source"]
    if not source.startswith("/dev/"):
        print("ERROR: mount source %s is not a block device. Refusing." % source)
        return 1
    part, disk = disk_info(source)
    is_usb = disk.get("tran") == "usb" or truthy(disk.get("rm")) or truthy(disk.get("hotplug"))
    if not is_usb:
        print("ERROR: %s is not on a USB/removable disk (tran=%s, rm=%s). Refusing."
              % (source, disk.get("tran"), disk.get("rm")))
        return 1
    proj_mount = run_json(["findmnt", "-J", "-n", "-o", "TARGET", "-T", str(root)])["filesystems"][0]["target"]
    disk_mps = set(mountpoints_of(disk))
    bad = (disk_mps & SYSTEM_MOUNTS) | ({proj_mount} & disk_mps)
    if bad:
        print("ERROR: that disk also holds system or project mounts (%s). Refusing." % ", ".join(sorted(bad)))
        return 1

    size_gb = round(int(disk.get("size") or 0) / 1e9, 2)
    print("=== TARGET USB (show this to the user) ===")
    print("Mount      : " + mount)
    print("Partition  : %s  label=%s  fs=%s" % (source, part.get("label"), fm.get("fstype")))
    print("Disk       : /dev/%s  model=%s  size=%s GB  tran=%s  removable=%s"
          % (disk.get("name"), (disk.get("model") or "").strip(), size_gb, disk.get("tran"), disk.get("rm")))
    try:
        st = shutil.disk_usage(mount)
        print("Free (GB)  : %.2f" % (st.free / 1e9))
    except OSError:
        pass
    if fm.get("fstype") != "vfat":
        print("WARNING: filesystem is not FAT (vfat). Most UEFI firmware boots OpenCore from FAT32 only.")
    print("==========================================")

    # ---- source + validation gate ----
    src = Path(a.source).resolve() if a.source else root / "EFI"
    if not efikit.is_within(src, root):
        print("ERROR: source must be inside the project.")
        return 1
    if not (src / "OC" / "config.plist").is_file():
        print("ERROR: source is not an EFI folder (OC/config.plist missing).")
        return 1
    th = efikit.tree_hash(src)
    latest = root / "docs" / "validation" / "latest.json"
    if not latest.is_file():
        print("GATE: no validation result. Run efi-validate first.")
        return 4
    lj = efikit.read_json(latest)
    if not lj.get("ocvalidateRan"):
        print("GATE: ocvalidate did not run in the last validation.")
        return 4
    if int(lj.get("errors", 1)) != 0:
        print("GATE: last validation has %s error(s)." % lj.get("errors"))
        return 4
    if lj.get("treeHash") != th:
        print("GATE: EFI changed since the last validation. Re-run efi-validate.")
        return 4
    print("Gate OK: validation is clean and matches the EFI content.")

    # ---- SMBIOS staging ----
    secrets_file = root / "secrets" / "smbios.json"
    stage_root = root / "_cache" / "stage" / "deploy"
    if stage_root.exists():
        shutil.rmtree(stage_root)
    if secrets_file.is_file() and not a.no_smbios:
        try:
            sec = smbios.load_secrets(secrets_file)
        except Exception as e:
            print("ERROR: secrets/smbios.json invalid: %s" % e)
            return 1
        shutil.copytree(src, stage_root / "EFI")
        try:
            smbios.inject(stage_root / "EFI" / "OC" / "config.plist", sec)
        except Exception as e:
            shutil.rmtree(stage_root, ignore_errors=True)
            print("ERROR: SMBIOS injection refused: %s" % e)
            return 1
        src = stage_root / "EFI"
        th = efikit.tree_hash(src)
        print("SMBIOS   : injected from secrets/smbios.json into a staged copy (values not shown).")
    else:
        print("SMBIOS   : placeholders (no secrets/smbios.json). Boots fine; iCloud/iMessage will not work.")

    dest = Path(mount) / "EFI"
    if not efikit.is_within(dest, mount):
        print("ERROR: unsafe destination.")
        return 1
    dest_files = file_map(dest)
    dest_is_oc = (dest / "OC" / "config.plist").is_file() or "oc/config.plist" in dest_files
    if dest_files and not dest_is_oc:
        print("%s exists with %d file(s) but is not an OpenCore EFI. Ask the user. Nothing was changed." % (dest, len(dest_files)))
        return 5

    src_files = file_map(src)
    to_copy = [k for k, p in src_files.items()
               if k not in dest_files or efikit.file_sha256(p) != efikit.file_sha256(dest_files[k])]
    to_delete = [k for k in dest_files if k not in src_files]

    if not a.confirmed:
        print("")
        print("DRY RUN - nothing written. %d file(s) to copy/update, %d to delete under %s:" % (len(to_copy), len(to_delete), dest))
        for k in sorted(to_copy):
            print("  + " + k)
        for k in sorted(to_delete):
            print("  - " + k)
        print("Show the USB info above to the user. After they approve, re-run with --confirmed.")
        return 0

    # ---- snapshot existing USB EFI ----
    if dest_is_oc:
        snap = root / ".claude" / "skills" / "efi-snapshot" / "scripts" / "snapshot.py"
        rc = subprocess.run([sys.executable, str(snap), "--workspace", str(root), "--source", str(dest),
                             "--strip-smbios",
                             "--label", "usb-before-deploy", "--note", "Automatic backup of USB EFI before deploy (serials stripped)",
                             "--ocvalidate-result", "n/a (existing USB content)"]).returncode
        if rc != 0:
            print("Snapshot step returned %d. Not writing to USB." % rc)
            return 6

    # ---- mirror ----
    for k in sorted(to_copy):
        s = src_files[k]
        d = dest_files.get(k) or (dest / s.relative_to(src))
        if not efikit.is_within(d, dest):
            print("ERROR: unsafe path %s" % d)
            return 1
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(s, d)
    for k in sorted(to_delete):
        p = dest_files[k]
        if not efikit.is_within(p, dest):
            print("ERROR: unsafe delete %s" % p)
            return 1
        p.unlink()
    for dirpath, dirs, files in os.walk(dest, topdown=False):
        if dirpath != str(dest) and not os.listdir(dirpath) and efikit.is_within(dirpath, dest):
            os.rmdir(dirpath)
    os.sync()

    if efikit.tree_hash(dest) != th:
        print("ERROR: verification FAILED: USB EFI differs from source.")
        return 1
    efikit.append_build_log(root, "Deployed EFI to %s (tree %s, verified)" % (dest, th[:12]))
    print("OK: %s matches the deployed content (tree %s). Unmount/eject the USB before unplugging." % (dest, th[:12]))
    return 0


if __name__ == "__main__":
    try:
        rc = main()
    except Exception as e:
        print("ERROR: %s" % e)
        rc = 1
    finally:
        _stage = efikit.project_root_from(__file__) / "_cache" / "stage" / "deploy"
        if _stage.exists():
            shutil.rmtree(_stage, ignore_errors=True)  # the staged copy holds serials: never keep it
    sys.exit(rc)
