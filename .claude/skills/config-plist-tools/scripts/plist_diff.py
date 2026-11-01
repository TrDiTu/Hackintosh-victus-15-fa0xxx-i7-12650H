#!/usr/bin/env python3
"""Structured diff of two OpenCore config.plist files (or any plists).

Arrays of dicts are matched by a natural key instead of by position:
  Kernel/Add|Block|Force -> BundlePath (or Identifier), ACPI/Add -> Path, UEFI/Drivers -> Path,
  ACPI/Patch, Kernel/Patch, Booter/Patch -> Comment, Misc/Tools|Entries -> Path.
Serial-like PlatformInfo values are masked (never printed).

Usage:
  python3 .claude/skills/config-plist-tools/scripts/plist_diff.py A.plist B.plist
  python3 .claude/skills/config-plist-tools/scripts/plist_diff.py A.plist B.plist --only Kernel/Quirks --only DeviceProperties
  python3 .claude/skills/config-plist-tools/scripts/plist_diff.py A.plist B.plist --markdown > docs/diffs/ours-vs-julionectar.md
Exit code: 0 identical, 1 differences, 2 error.
"""
import argparse
import plistlib
import sys

SECRET_KEYS = {"SystemSerialNumber", "MLB", "SystemUUID", "ROM", "BoardSerialNumber", "ChassisSerialNumber",
               "ProcessorType_Serial"}
KEY_FIELDS = ("BundlePath", "Identifier", "Path", "Comment")


def fmt(v, key=None):
    if key in SECRET_KEYS:
        return "<masked>"
    if isinstance(v, (bytes, bytearray)):
        return "<data " + v.hex().upper() + ">"
    if isinstance(v, dict):
        return "{dict %d keys}" % len(v)
    if isinstance(v, list):
        return "[array %d items]" % len(v)
    return repr(v)


def key_of(item):
    if isinstance(item, dict):
        for f in KEY_FIELDS:
            if item.get(f):
                return "%s=%s" % (f, item[f])
    return None


def diff(a, b, path, out, last_key=None):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            p = path + "/" + k if path else k
            if k not in a:
                out.append(("+", p, None, fmt(b[k], k)))
            elif k not in b:
                out.append(("-", p, fmt(a[k], k), None))
            else:
                diff(a[k], b[k], p, out, k)
        return
    if isinstance(a, list) and isinstance(b, list):
        ka, kb = [key_of(x) for x in a], [key_of(x) for x in b]
        if all(ka) and all(kb) and len(set(ka)) == len(ka) and len(set(kb)) == len(kb):
            ia, ib = {k: i for i, k in enumerate(ka)}, {k: i for i, k in enumerate(kb)}
            for k in ka + [k for k in kb if k not in ia]:
                p = "%s[%s]" % (path, k)
                if k not in ib:
                    out.append(("-", p, "(entry removed)", None))
                elif k not in ia:
                    out.append(("+", p, None, "(entry added)"))
                else:
                    if ia[k] != ib[k]:
                        out.append(("~", p + " (order)", "position %d" % ia[k], "position %d" % ib[k]))
                    diff(a[ia[k]], b[ib[k]], p, out)
            return
        for i in range(max(len(a), len(b))):
            p = "%s[%d]" % (path, i)
            if i >= len(a):
                out.append(("+", p, None, fmt(b[i])))
            elif i >= len(b):
                out.append(("-", p, fmt(a[i]), None))
            else:
                diff(a[i], b[i], p, out)
        return
    if a != b or type(a) is not type(b):
        if last_key in SECRET_KEYS:
            out.append(("~", path, "<masked>", "<masked> (differs)"))
        else:
            out.append(("~", path, fmt(a, last_key), fmt(b, last_key)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("a")
    ap.add_argument("b")
    ap.add_argument("--only", action="append", default=[], help="path prefix to keep, e.g. Kernel/Quirks")
    ap.add_argument("--markdown", action="store_true")
    a = ap.parse_args()
    try:
        with open(a.a, "rb") as f:
            pa = plistlib.load(f)
        with open(a.b, "rb") as f:
            pb = plistlib.load(f)
    except Exception as e:
        print("ERROR: %s" % e)
        return 2
    out = []
    diff(pa, pb, "", out)
    if a.only:
        out = [d for d in out if any(d[1].startswith(p) for p in a.only)]
    if a.markdown:
        print("# plist diff\n\n- A: `%s`\n- B: `%s`\n- differences: %d\n" % (a.a, a.b, len(out)))
        print("| | Path | A | B |\n|---|---|---|---|")
        for op, p, va, vb in out:
            print("| %s | `%s` | %s | %s |" % (op, p, (va or "").replace("|", "\\|"), (vb or "").replace("|", "\\|")))
    else:
        for op, p, va, vb in out:
            print("%s %s\n    A: %s\n    B: %s" % (op, p, va if va is not None else "(absent)", vb if vb is not None else "(absent)"))
        print("%d difference(s)" % len(out))
    return 1 if out else 0


if __name__ == "__main__":
    sys.exit(main())
