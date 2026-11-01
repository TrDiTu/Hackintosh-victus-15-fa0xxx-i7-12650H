"""SMBIOS secret handling. Values are never printed or logged."""
import json
import plistlib
import re
from pathlib import Path

SECRET_FIELDS = ("SystemSerialNumber", "MLB", "SystemUUID", "ROM")
UUID_RE = re.compile(r"^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}$")
PLACEHOLDERS = {"SystemSerialNumber": "CHANGE_ME_SERIAL", "MLB": "CHANGE_ME_MLB",
                "SystemUUID": "00000000-0000-0000-0000-000000000000", "ROM": bytes(6)}


def is_placeholder(key, v):
    if v is None:
        return True
    if isinstance(v, (bytes, bytearray)):
        return not any(v)
    s = str(v)
    return s == "" or s.startswith("CHANGE_ME") or s.strip("0-") == ""


def load_secrets(path):
    """Return dict of validated secrets, or raise ValueError with a message that contains no values."""
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    missing = [k for k in SECRET_FIELDS + ("SystemProductName",) if not d.get(k)]
    if missing:
        raise ValueError("secrets file is missing: " + ", ".join(missing))
    for k in SECRET_FIELDS:
        if is_placeholder(k, d[k]):
            raise ValueError("secrets file still has a placeholder for " + k)
    if not UUID_RE.match(d["SystemUUID"]):
        raise ValueError("SystemUUID is not a UUID")
    rom = d["ROM"].replace(":", "").replace("-", "")
    if not re.fullmatch(r"[0-9A-Fa-f]{12}", rom):
        raise ValueError("ROM must be 12 hex digits (6 bytes)")
    if not (10 <= len(d["SystemSerialNumber"]) <= 14):
        raise ValueError("SystemSerialNumber length looks wrong (expected ~12)")
    if not (13 <= len(d["MLB"]) <= 20):
        raise ValueError("MLB length looks wrong (expected ~17)")
    out = dict(d)
    out["ROM"] = bytes.fromhex(rom)
    return out


def inject(config_path, secrets):
    """Write secrets into PlatformInfo/Generic of a config.plist copy. Refuses if the copy is not placeholder-only."""
    with open(config_path, "rb") as f:
        cfg = plistlib.load(f)
    gen = cfg.get("PlatformInfo", {}).get("Generic")
    if gen is None:
        raise ValueError("config has no PlatformInfo/Generic")
    if gen.get("SystemProductName") != secrets["SystemProductName"]:
        raise ValueError("SystemProductName in config differs from the one the serials were generated for")
    for k in SECRET_FIELDS:
        if not is_placeholder(k, gen.get(k)):
            raise ValueError("project config already holds a real-looking %s; it must keep placeholders" % k)
        gen[k] = secrets[k]
    with open(config_path, "wb") as f:
        plistlib.dump(cfg, f, fmt=plistlib.FMT_XML, sort_keys=False)


def strip(config_path):
    """Replace secret fields with placeholders. Returns number of fields replaced."""
    with open(config_path, "rb") as f:
        cfg = plistlib.load(f)
    gen = cfg.get("PlatformInfo", {}).get("Generic")
    n = 0
    if gen:
        for k in SECRET_FIELDS:
            if k in gen and not is_placeholder(k, gen[k]):
                gen[k] = PLACEHOLDERS[k]
                n += 1
    if n:
        with open(config_path, "wb") as f:
            plistlib.dump(cfg, f, fmt=plistlib.FMT_XML, sort_keys=False)
    return n
