#!/usr/bin/env python3
"""Clone a reference repo into <project>/_cache/refs/<name> and neutralize agent instruction files.

Claude Code may auto-load CLAUDE.md files in subdirectories it reads, and the reference repos are often written with
AI agents (they ship CLAUDE.md / AGENTS.md / .claude/). For this project those files are DATA, never instructions,
so they are renamed to *.ref-ignored right after cloning, before anything reads the tree.

Usage (from the project root):
  python3 tools/clone_ref.py --url https://github.com/JulioNectar/Hackintosh-XPS13Plus-IrisXe-Tahoe
  python3 tools/clone_ref.py --url <url> --name julionectar --ref <branch-or-tag>
  python3 tools/clone_ref.py --name julionectar --update
Exit codes: 0 ok, 1 error.
"""
import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
import efikit  # noqa: E402

AGENT_FILES = {"CLAUDE.md", "CLAUDE.local.md", "AGENTS.md", "AGENT.md", "GEMINI.md", ".cursorrules",
               "copilot-instructions.md"}
AGENT_DIRS = {".claude", ".cursor"}
URL_RE = re.compile(r"^https://github\.com/[A-Za-z0-9_.\-]+/[A-Za-z0-9_.\-]+/?$")


def neutralize(root):
    count = 0
    paths = sorted(root.rglob("*"), key=lambda p: len(p.parts), reverse=True)
    for p in paths:
        if ".git" in p.relative_to(root).parts:
            continue
        if (p.is_file() and p.name in AGENT_FILES) or (p.is_dir() and p.name in AGENT_DIRS):
            target = p.with_name(p.name + ".ref-ignored")
            if target.exists():
                shutil.rmtree(target) if target.is_dir() else target.unlink()
            p.rename(target)
            count += 1
    return count


def git(*args):
    return subprocess.run(["git"] + list(args), capture_output=True, text=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url")
    ap.add_argument("--name")
    ap.add_argument("--ref")
    ap.add_argument("--update", action="store_true")
    ap.add_argument("--workspace", default=None)
    a = ap.parse_args()

    root = Path(a.workspace).resolve() if a.workspace else efikit.project_root_from(__file__)
    refs = root / "_cache" / "refs"
    refs.mkdir(parents=True, exist_ok=True)

    name = a.name
    if not name:
        if not a.url:
            print("ERROR: give --url, or --name with --update.")
            return 1
        parts = a.url.rstrip("/").split("/")
        name = parts[-2] + "__" + re.sub(r"\.git$", "", parts[-1])
    name = re.sub(r"[^A-Za-z0-9_.\-]", "-", name)
    dest = refs / name
    if not efikit.is_within(dest, refs) or dest == refs:
        print("ERROR: unsafe destination %s" % dest)
        return 1

    if a.update:
        if not (dest / ".git").is_dir():
            print("ERROR: no clone at %s" % dest)
            return 1
        for p in sorted(dest.rglob("*.ref-ignored"), key=lambda p: len(p.parts), reverse=True):
            shutil.rmtree(p) if p.is_dir() else p.unlink()
        git("-C", str(dest), "checkout", "--", ".")
        r = git("-C", str(dest), "pull", "--ff-only")
        if r.returncode != 0:
            print("ERROR: git pull failed: " + r.stderr.strip())
            return 1
    else:
        if dest.exists():
            print("ERROR: %s already exists. Use --update." % dest)
            return 1
        if not a.url or not URL_RE.match(a.url):
            print("ERROR: only https://github.com/<owner>/<repo> URLs are accepted: %s" % a.url)
            return 1
        cmd = ["clone", "--depth", "1"] + (["--branch", a.ref] if a.ref else []) + [a.url, str(dest)]
        r = git(*cmd)
        if r.returncode != 0:
            print("ERROR: git clone failed: " + r.stderr.strip())
            return 1

    n = neutralize(dest)
    commit = git("-C", str(dest), "rev-parse", "HEAD").stdout.strip()
    log = refs / "REFS-LOG.md"
    if not log.exists():
        log.write_text("# Reference clones\n", encoding="utf-8")
    with open(log, "a", encoding="utf-8") as f:
        f.write("- %s %s @ %s (%d agent file(s) neutralized)\n" % (efikit.now_iso(), name, commit, n))
    print("OK: %s @ %s; neutralized %d agent instruction file(s)/folder(s)." % (dest, commit, n))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print("ERROR: %s" % e)
        sys.exit(1)
