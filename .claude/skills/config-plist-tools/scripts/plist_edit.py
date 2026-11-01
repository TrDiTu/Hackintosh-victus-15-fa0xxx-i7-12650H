#!/usr/bin/env python3
"""Safe, logged edits of EFI/OC/config.plist (never hand-edit the XML).

Path syntax: segments separated by '/'. Wrap a segment containing '/' in braces. Select array items by index [3]
or by field [BundlePath=Lilu.kext].
  Kernel/Quirks/DisableIoMapper
  NVRAM/Add/{7C436110-AB2A-4BBB-A880-FE41995C9F82}/boot-args
  DeviceProperties/Add/{PciRoot(0x0)/Pci(0x2,0x0)}/device-id
  Kernel/Add[BundlePath=VoodooI2CHID.kext]/Enabled

Commands (add --dry-run to preview; every real change is appended to docs/BUILD-LOG.md):
  get    PATH
  set    PATH --type bool|int|str|data|real VALUE        (data = hex, e.g. 499A0000; key must exist unless --create)
  delete PATH
  append PATH --json '{"BundlePath": "Lilu.kext", "Enabled": true, ...}'   (strings "hex:ABCD" become data)
  move   PATH --to N                                       (reorder an array item, e.g. kext load order)
  bootarg-add  WORD    /  bootarg-remove WORD             (edit boot-args word by word)
Option --file (default EFI/OC/config.plist). Serial/MLB/UUID/ROM cannot be set to real values here (see smbios-secrets).
Exit codes: 0 ok, 1 error.
"""
import argparse
import json
import plistlib
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[4] / "tools" / "lib"))
sys.path.insert(0, str(HERE.parent))
import efikit  # noqa: E402
import plist_diff  # noqa: E402

NVRAM_GUID = "7C436110-AB2A-4BBB-A880-FE41995C9F82"
SECRET_KEYS = plist_diff.SECRET_KEYS
SEG_RE = re.compile(r"\{([^}]*)\}|([^/\[\]{}]+)|\[([^\]]*)\]")


def parse_path(path):
    segs = []
    pos = 0
    while pos < len(path):
        if path[pos] == "/":
            pos += 1
            continue
        m = SEG_RE.match(path, pos)
        if not m:
            raise ValueError("bad path near: " + path[pos:])
        if m.group(1) is not None:
            segs.append(("key", m.group(1)))
        elif m.group(2) is not None:
            segs.append(("key", m.group(2)))
        else:
            sel = m.group(3)
            if sel.isdigit():
                segs.append(("idx", int(sel)))
            elif "=" in sel:
                f, v = sel.split("=", 1)
                segs.append(("sel", (f, v)))
            else:
                raise ValueError("bad selector [%s]" % sel)
        pos = m.end()
    return segs


def step(node, seg, create=False):
    kind, val = seg
    if kind == "key":
        if not isinstance(node, dict):
            raise KeyError("not a dict at '%s'" % val)
        if val not in node:
            if create:
                node[val] = {}
            else:
                raise KeyError("missing key '%s'" % val)
        return node, val
    if not isinstance(node, list):
        raise KeyError("not an array for selector")
    if kind == "idx":
        if val >= len(node):
            raise KeyError("index %d out of range" % val)
        return node, val
    f, v = val
    hits = [i for i, x in enumerate(node) if isinstance(x, dict) and str(x.get(f)) == v]
    if len(hits) != 1:
        raise KeyError("selector [%s=%s] matched %d items" % (f, v, len(hits)))
    return node, hits[0]


def resolve(root, segs, create_parents=False):
    node = root
    for seg in segs[:-1]:
        parent, k = step(node, seg, create=create_parents)
        node = parent[k]
    return node


def convert(t, raw):
    if t == "bool":
        if raw.lower() not in ("true", "false", "1", "0", "yes", "no"):
            raise ValueError("bool expects true/false")
        return raw.lower() in ("true", "1", "yes")
    if t == "int":
        return int(raw, 0)
    if t == "real":
        return float(raw)
    if t == "data":
        return bytes.fromhex(raw.replace(" ", ""))
    return raw


def hexify(o):
    if isinstance(o, str) and o.startswith("hex:"):
        return bytes.fromhex(o[4:])
    if isinstance(o, dict):
        return {k: hexify(v) for k, v in o.items()}
    if isinstance(o, list):
        return [hexify(v) for v in o]
    return o


def guard_secret(segs, value):
    if segs and segs[-1][0] == "key" and segs[-1][1] in SECRET_KEYS:
        if not (isinstance(value, str) and (value.startswith("CHANGE_ME") or value.strip("0-") == "")):
            raise ValueError("refusing to write a real-looking %s into the project EFI; use smbios-secrets" % segs[-1][1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["get", "set", "delete", "append", "move", "bootarg-add", "bootarg-remove"])
    ap.add_argument("path")
    ap.add_argument("value", nargs="?")
    ap.add_argument("--type", default="str", choices=["bool", "int", "str", "data", "real"])
    ap.add_argument("--json", default=None)
    ap.add_argument("--to", type=int, default=None)
    ap.add_argument("--file", default=None)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--create", action="store_true", help="allow set to create a missing key/parents")
    argv = sys.argv[1:]
    if len(argv) >= 2 and argv[0] in ("bootarg-add", "bootarg-remove") and argv[1].startswith("-"):
        argv = [argv[0], "--", argv[1]] + argv[2:]  # boot-args such as -wegnoegpu look like options
    a = ap.parse_args(argv)

    root_dir = efikit.project_root_from(__file__)
    f = Path(a.file).resolve() if a.file else root_dir / "EFI" / "OC" / "config.plist"
    with open(f, "rb") as fh:
        data = plistlib.load(fh)
    with open(f, "rb") as fh:
        before = plistlib.load(fh)

    if a.cmd in ("bootarg-add", "bootarg-remove"):
        word = a.path
        nv = data.setdefault("NVRAM", {}).setdefault("Add", {}).setdefault(NVRAM_GUID, {})
        words = str(nv.get("boot-args", "")).split()
        key = word.split("=")[0]
        if a.cmd == "bootarg-add":
            words = [w for w in words if w.split("=")[0] != key] + [word]
        else:
            if key not in [w.split("=")[0] for w in words]:
                print("ERROR: boot-arg %s not present" % key)
                return 1
            words = [w for w in words if w.split("=")[0] != key]
        nv["boot-args"] = " ".join(words)
        desc = "%s %s" % (a.cmd, word)
    else:
        segs = parse_path(a.path)
        if a.cmd == "get":
            parent = resolve(data, segs)
            p, k = step(parent, segs[-1])
            v = p[k]
            last = segs[-1][1] if segs[-1][0] == "key" else None
            print(plist_diff.fmt(v, last) if not isinstance(v, (str, int, float, bool)) or last in SECRET_KEYS else repr(v))
            return 0
        if a.cmd == "set":
            if a.value is None:
                print("ERROR: set needs a value")
                return 1
            val = convert(a.type, a.value)
            guard_secret(segs, val)
            parent = resolve(data, segs, create_parents=a.create)
            if segs[-1][0] == "key":
                if segs[-1][1] not in parent and not a.create:
                    print("ERROR: key '%s' does not exist (typo?). Check Configuration.pdf; use --create only for a key that is "
                          "really new in this OpenCore version." % segs[-1][1])
                    return 1
                old = parent.get(segs[-1][1])
                if old is not None and type(old) is not type(val):
                    print("ERROR: type mismatch: existing %s, new %s. Use the matching --type." % (type(old).__name__, type(val).__name__))
                    return 1
                parent[segs[-1][1]] = val
            else:
                p, k = step(parent, segs[-1])
                p[k] = val
            desc = "set %s = %s" % (a.path, plist_diff.fmt(val, segs[-1][1] if segs[-1][0] == "key" else None))
        elif a.cmd == "delete":
            parent = resolve(data, segs)
            p, k = step(parent, segs[-1])
            del p[k]
            desc = "delete %s" % a.path
        elif a.cmd == "append":
            if not a.json:
                print("ERROR: append needs --json")
                return 1
            item = hexify(json.loads(a.json))
            parent = resolve(data, segs)
            p, k = step(parent, segs[-1])
            if not isinstance(p[k], list):
                print("ERROR: %s is not an array" % a.path)
                return 1
            p[k].append(item)
            desc = "append to %s: %s" % (a.path, plist_diff.key_of(item) or "item")
        elif a.cmd == "move":
            if a.to is None:
                print("ERROR: move needs --to")
                return 1
            parent = resolve(data, segs)
            if not isinstance(parent, list):
                print("ERROR: move needs an array item path")
                return 1
            _, i = step(parent, segs[-1])
            item = parent.pop(i)
            parent.insert(a.to, item)
            desc = "move %s to position %d" % (a.path, a.to)

    changes = []
    plist_diff.diff(before, data, "", changes)
    for op, p, va, vb in changes:
        print("%s %s: %s -> %s" % (op, p, va if va is not None else "(absent)", vb if vb is not None else "(absent)"))
    if not changes:
        print("No change.")
        return 0
    if a.dry_run:
        print("DRY-RUN: not written.")
        return 0
    tmp = f.with_suffix(".plist.tmp")
    with open(tmp, "wb") as fh:
        plistlib.dump(data, fh, fmt=plistlib.FMT_XML, sort_keys=False)
    with open(tmp, "rb") as fh:
        plistlib.load(fh)  # re-parse before replacing
    tmp.replace(f)
    efikit.append_build_log(root_dir, "plist_edit %s (%s)" % (desc, f.name))
    print("OK: written %s" % f)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print("ERROR: %s" % e)
        sys.exit(1)
