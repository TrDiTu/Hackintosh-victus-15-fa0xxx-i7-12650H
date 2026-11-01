#!/usr/bin/env python3
"""Snapshot ONE complete EFI build into <project>/snapshots (max 3, rotating, known-good protected).

Usage (from the project root):
  python3 .claude/skills/efi-snapshot/scripts/snapshot.py --label wifi-touchpad --note "..." --ocvalidate-result "0 errors" --dry-run
  python3 .claude/skills/efi-snapshot/scripts/snapshot.py --label wifi-touchpad --note "..." --ocvalidate-result "0 errors"
  python3 .claude/skills/efi-snapshot/scripts/snapshot.py --source /media/me/EFI/EFI --label usb-before-deploy
  python3 .claude/skills/efi-snapshot/scripts/snapshot.py --mark-known-good build-02     (ONLY when the user asks)

Exit codes: 0 ok (or identical snapshot already exists), 1 error, 3 oldest snapshot is known-good (ask the user).
"""
import argparse
import plistlib
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "tools" / "lib"))
import efikit  # noqa: E402
import smbios  # noqa: E402

NAME_RE = re.compile(r"^build-(\d+)-")


def list_snapshots(snap_root):
    if not snap_root.is_dir():
        return []
    items = [d for d in snap_root.iterdir() if d.is_dir() and NAME_RE.match(d.name)]
    return sorted(items, key=lambda d: int(NAME_RE.match(d.name).group(1)))


def load_manifest(d):
    p = d / "MANIFEST.json"
    return efikit.read_json(p) if p.is_file() else None


def write_manifest(d, m):
    efikit.write_json(d / "MANIFEST.json", m)
    lines = [
        "# " + m["name"], "",
        "- created: " + m["created"],
        "- label: " + m["label"],
        "- known-good: " + ("true" if m.get("knownGood") else "false"),
        "- tree-sha256: " + m["treeHash"],
        "- config.plist sha256: " + m["configSha256"],
        "- ocvalidate: " + m["ocvalidate"],
        "", "## Notes / changes vs previous build", m.get("note", ""),
        "", "## Kexts",
    ] + ["- " + k for k in m.get("kexts", [])]
    (d / "MANIFEST.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def kext_list(efi):
    out = []
    kdir = efi / "OC" / "Kexts"
    if kdir.is_dir():
        for k in sorted(kdir.glob("*.kext")):
            ver = "?"
            ip = k / "Contents" / "Info.plist"
            try:
                with open(ip, "rb") as f:
                    ver = str(plistlib.load(f).get("CFBundleShortVersionString", "?"))
            except Exception:
                pass
            out.append(k.name + " " + ver)
    return out


def ignore(_dir, names):
    return [n for n in names if n in efikit.IGNORE_NAMES or n.startswith("._")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", default=None)
    ap.add_argument("--source", default=None)
    ap.add_argument("--label", default="build")
    ap.add_argument("--note", default="")
    ap.add_argument("--ocvalidate-result", default="not-run")
    ap.add_argument("--mark-known-good", default=None)
    ap.add_argument("--max", type=int, default=3)
    ap.add_argument("--strip-smbios", action="store_true", help="replace serial/MLB/UUID/ROM with placeholders in the copy")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    root = Path(a.workspace).resolve() if a.workspace else efikit.project_root_from(__file__)
    snap_root = root / "snapshots"
    existing = list_snapshots(snap_root)

    if a.mark_known_good:
        target = next((d for d in existing if d.name.startswith(a.mark_known_good + "-")), None)
        if not target:
            print("ERROR: snapshot '%s' not found" % a.mark_known_good)
            return 1
        m = load_manifest(target)
        m["knownGood"] = True
        if a.dry_run:
            print("DRY-RUN: would mark %s known-good" % target.name)
            return 0
        write_manifest(target, m)
        efikit.append_build_log(root, "Marked %s as known-good (user request)" % target.name)
        print("OK: %s marked known-good" % target.name)
        return 0

    src = Path(a.source).resolve() if a.source else root / "EFI"
    if not (src / "OC" / "config.plist").is_file():
        print("ERROR: not an EFI folder (missing OC/config.plist): %s" % src)
        return 1

    th = efikit.tree_hash(src)
    if a.strip_smbios:
        # hash of the stripped form, computed on a scratch copy so duplicates are detected correctly
        scratch = root / "_cache" / "stage" / "snapshot-strip"
        if scratch.exists():
            shutil.rmtree(scratch)
        shutil.copytree(src, scratch / "EFI", ignore=ignore)
        smbios.strip(scratch / "EFI" / "OC" / "config.plist")
        th = efikit.tree_hash(scratch / "EFI")
        src_copy = scratch / "EFI"
    else:
        src_copy = src
    for d in existing:
        m = load_manifest(d)
        if m and m.get("treeHash") == th:
            print("SKIP: identical to existing snapshot %s. No new snapshot created." % d.name)
            return 0

    to_remove = []
    if len(existing) >= a.max:
        to_remove = existing[: len(existing) - a.max + 1]
        for d in to_remove:
            m = load_manifest(d)
            if m and m.get("knownGood"):
                print("STOP: oldest snapshot %s is marked known-good. Ask the user before deleting anything." % d.name)
                return 3

    counter_file = snap_root / "_counter.txt"
    max_existing = max([int(NAME_RE.match(d.name).group(1)) for d in existing] or [0])
    counter = 0
    if counter_file.is_file():
        try:
            counter = int(counter_file.read_text().strip())
        except ValueError:
            counter = 0
    nxt = max(max_existing, counter) + 1
    safe_label = re.sub(r"[^A-Za-z0-9_\-]", "-", a.label)
    stamp = efikit.now_iso().replace("-", "").replace(":", "").replace("T", "-")
    name = "build-%02d-%s-%s" % (nxt, stamp, safe_label)
    dest = snap_root / name
    if not efikit.is_within(dest, snap_root):
        print("ERROR: unsafe destination %s" % dest)
        return 1

    manifest = {
        "build": nxt, "name": name, "created": efikit.now_iso(), "label": a.label, "note": a.note,
        "treeHash": th, "configSha256": efikit.file_sha256(src_copy / "OC" / "config.plist").upper(),
        "smbiosStripped": bool(a.strip_smbios),
        "ocvalidate": a.ocvalidate_result, "kexts": kext_list(src), "knownGood": False,
    }

    if a.dry_run:
        print("DRY-RUN: would create %s and rotate out: %s" % (name, ", ".join(d.name for d in to_remove) or "nothing"))
        return 0

    snap_root.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src_copy, dest / "EFI", ignore=ignore)
    if efikit.tree_hash(dest / "EFI") != th:
        shutil.rmtree(dest)
        print("ERROR: verification failed, snapshot removed.")
        return 1
    write_manifest(dest, manifest)
    counter_file.write_text(str(nxt))
    efikit.append_build_log(root, "Created %s (tree %s, ocvalidate: %s)" % (name, th[:12], a.ocvalidate_result))
    print("OK: created %s" % name)

    for d in to_remove:
        if not efikit.is_within(d, snap_root) or d == snap_root:
            print("ERROR: refusing to delete outside snapshots: %s" % d)
            return 1
        shutil.rmtree(d)
        efikit.append_build_log(root, "Rotated out (deleted) oldest snapshot %s" % d.name)
        print("Rotated out: %s" % d.name)
    return 0


if __name__ == "__main__":
    try:
        rc = main()
    except Exception as e:  # keep the exit-code contract
        print("ERROR: %s" % e)
        rc = 1
    finally:
        _scratch = efikit.project_root_from(__file__) / "_cache" / "stage" / "snapshot-strip"
        if _scratch.exists():
            shutil.rmtree(_scratch, ignore_errors=True)
    sys.exit(rc)
