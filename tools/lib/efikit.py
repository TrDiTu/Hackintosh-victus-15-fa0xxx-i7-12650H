"""Shared helpers for the EFI kit scripts (Python 3.8+, standard library only)."""
import datetime
import hashlib
import json
import os
from pathlib import Path

IGNORE_NAMES = {".DS_Store", "Thumbs.db", "desktop.ini"}


def project_root_from(script_file):
    """<root>/.claude/skills/<skill>/scripts/<script>.py -> <root>; <root>/tools/<x>.py -> <root>."""
    p = Path(script_file).resolve()
    for parent in p.parents:
        if (parent / "CLAUDE.md").is_file() and (parent / ".claude").is_dir():
            return parent
    return Path.cwd().resolve()


def tree_hash(root):
    """Content hash of a directory: sorted 'relpath(lowercase, /)|sha256' lines, hashed again."""
    root = Path(root)
    lines = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in (".git",)]
        for name in filenames:
            if name in IGNORE_NAMES or name.startswith("._"):
                continue
            full = Path(dirpath) / name
            rel = full.relative_to(root).as_posix().lower()
            lines.append(rel + "|" + file_sha256(full).upper())
    lines.sort()
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()


def file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def now_iso():
    return datetime.datetime.now().replace(microsecond=0).isoformat()


def append_build_log(root, line):
    log = Path(root) / "docs" / "BUILD-LOG.md"
    log.parent.mkdir(parents=True, exist_ok=True)
    if not log.exists():
        log.write_text("# BUILD-LOG\n", encoding="utf-8")
    with open(log, "a", encoding="utf-8") as f:
        f.write("- " + now_iso() + " " + line + "\n")


def is_within(child, parent):
    child = Path(child).resolve()
    parent = Path(parent).resolve()
    return child == parent or parent in child.parents


def read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
