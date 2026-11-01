#!/usr/bin/env python3
"""Download ONE asset from an official GitHub release, verify it, extract it safely and record provenance.

Usage (from the project root):
  python3 .claude/skills/release-fetch/scripts/fetch_release.py --repo acidanthera/Lilu --asset 'RELEASE\\.zip$' --dry-run
  python3 .claude/skills/release-fetch/scripts/fetch_release.py --repo acidanthera/Lilu --asset 'RELEASE\\.zip$'
  python3 .claude/skills/release-fetch/scripts/fetch_release.py --repo acidanthera/OpenCorePkg --tag 1.0.8 --asset 'RELEASE\\.zip$'
  python3 .claude/skills/release-fetch/scripts/fetch_release.py --repo kgp-macPro/AirportItlwm-Tahoe --tag v1.0.0 --asset '\\.zip$' \\
          --expect-sha256 <value published in the repo README>

Outputs: _cache/downloads/<owner>__<repo>/<tag>/<asset>, extracted to .../extracted/, one row appended to docs/SOURCES.md.
Nothing is copied into EFI/ by this script: putting a kext in the EFI is a separate, reviewed step.
Exit codes: 0 ok, 1 error, 2 verification failed (download kept for inspection, not recorded).
"""
import argparse
import hashlib
import json
import os
import re
import sys
import urllib.request
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "tools" / "lib"))
import efikit  # noqa: E402

API = "https://api.github.com/repos/%s/releases/%s"
REPO_RE = re.compile(r"^[A-Za-z0-9_.\-]+/[A-Za-z0-9_.\-]+$")


def http_json(url):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "efi-kit"})
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        req.add_header("Authorization", "Bearer " + tok)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def download(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": "efi-kit", "Accept": "application/octet-stream"})
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(req, timeout=300) as r, open(dest, "wb") as f:
        while True:
            chunk = r.read(1024 * 1024)
            if not chunk:
                break
            f.write(chunk)


def pick_asset(release, pattern):
    rx = re.compile(pattern)
    hits = [a for a in release.get("assets", []) if rx.search(a.get("name", ""))]
    return hits


def safe_extract(zpath, out):
    """Extract a zip refusing absolute paths, '..', and symlinks. Returns list of extracted names."""
    out = out.resolve()
    names = []
    with zipfile.ZipFile(zpath) as z:
        infos = z.infolist()
        for info in infos:  # validate everything first, extract nothing if any entry is unsafe
            name = info.filename
            mode = (info.external_attr >> 16) & 0o170000
            if mode == 0o120000:
                raise ValueError("zip contains a symlink: %s" % name)
            target = (out / name).resolve()
            if name.startswith("/") or "\\" in name or ".." in Path(name).parts or not efikit.is_within(target, out):
                raise ValueError("unsafe path in zip: %s" % name)
        for info in infos:
            z.extract(info, out)
            names.append(info.filename)
    return names


def record_source(root, row):
    p = root / "docs" / "SOURCES.md"
    if not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("# SOURCES\n\n| Component | Version | Release URL | File | SHA256 | Date | Verification | Used in EFI? |\n"
                     "|---|---|---|---|---|---|---|---|\n", encoding="utf-8")
    with open(p, "a", encoding="utf-8") as f:
        f.write("| " + " | ".join(row) + " |\n")


def run(a, root, release=None, asset_file=None):
    if not REPO_RE.match(a.repo):
        print("ERROR: --repo must be owner/name")
        return 1
    if release is None:
        which = "latest" if not a.tag else "tags/" + a.tag
        release = http_json(API % (a.repo, which))
    tag = release.get("tag_name", "?")
    if release.get("draft"):
        print("ERROR: release %s is a draft." % tag)
        return 1
    if release.get("prerelease") and not a.allow_prerelease:
        print("ERROR: release %s is a prerelease (alpha/beta). Use a stable release, or --allow-prerelease only if the user asked." % tag)
        return 1
    hits = pick_asset(release, a.asset)
    if len(hits) != 1:
        print("ERROR: asset pattern %r matched %d assets in %s: %s" % (a.asset, len(hits), tag,
              ", ".join(x.get("name", "") for x in release.get("assets", []))))
        return 1
    asset = hits[0]
    rel_url = release.get("html_url", "https://github.com/%s/releases/tag/%s" % (a.repo, tag))
    base = root / "_cache" / "downloads" / a.repo.replace("/", "__") / re.sub(r"[^A-Za-z0-9_.\-]", "-", tag)
    dest = base / asset["name"]
    print("Release : %s %s (%s)" % (a.repo, tag, release.get("published_at", "?")))
    print("Asset   : %s (%s bytes)" % (asset["name"], asset.get("size", "?")))
    print("URL     : %s" % rel_url)
    if a.dry_run:
        print("DRY-RUN: would download to %s" % dest)
        return 0

    if asset_file:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(Path(asset_file).read_bytes())
    else:
        download(asset["browser_download_url"], dest)
    sha = efikit.file_sha256(dest)
    checks = []
    digest = (asset.get("digest") or "")
    if digest.startswith("sha256:"):
        if digest.split(":", 1)[1].lower() != sha.lower():
            print("VERIFY FAILED: SHA-256 differs from the digest GitHub publishes for this asset. Not recorded.")
            return 2
        checks.append("GitHub asset digest")
    if a.expect_sha256:
        if a.expect_sha256.lower() != sha.lower():
            print("VERIFY FAILED: SHA-256 differs from --expect-sha256. Not recorded.")
            return 2
        checks.append("expected SHA-256")
    if not checks:
        checks.append("none available (record only)")

    extracted = []
    if dest.suffix.lower() == ".zip":
        out = base / "extracted"
        extracted = safe_extract(dest, out)
        found = sorted({n.split(".kext/")[0] + ".kext" for n in extracted if ".kext/" in n} |
                       {n for n in extracted if n.lower().endswith((".efi", ".aml"))})
        print("Extracted to %s" % out)
        for n in found[:40]:
            print("  " + n)
    record_source(root, [a.repo, tag, rel_url, asset["name"], sha.upper(), efikit.now_iso()[:10], "; ".join(checks), "not yet"])
    print("OK: %s sha256=%s verification=%s" % (dest, sha.upper(), "; ".join(checks)))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--tag", default=None)
    ap.add_argument("--asset", required=True, help="regex matched against asset names; must match exactly one")
    ap.add_argument("--expect-sha256", default=None)
    ap.add_argument("--allow-prerelease", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--workspace", default=None)
    a = ap.parse_args()
    root = Path(a.workspace).resolve() if a.workspace else efikit.project_root_from(__file__)
    return run(a, root)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print("ERROR: %s" % e)
        sys.exit(1)
