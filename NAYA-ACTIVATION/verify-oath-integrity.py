#!/usr/bin/env python3
"""Oath integrity check — any seat can run this. (Shawn's 10-point plan, item 8.)

Verifies the oath + doctrine on GitHub main still match the canonical bytes
Shawn ratified. Any change that does not carry Shawn's word is flagged.

Usage:
    python3 NAYA-ACTIVATION/verify-oath-integrity.py [--ref <ref>] [--json]

Exit 0 = integrity holds: every file present, every hash matches.
Exit 1 = DRIFT DETECTED — the canonical text changed without ratification.
Exit 2 = NOT_ON_MAIN or SOURCE_UNREACHABLE — integrity is UNPROVEN, never
         mistaken for PASS. A missing file is never a passing check.

The canonical hashes below are pinned at ratification. To re-pin after a
Shawn-ratified change: update CANONICAL and record his word in the log.
"""
from __future__ import annotations
import argparse
import base64
import hashlib
import json
import sys
import urllib.request

OWNER, REPO = "SoulSchoolAcademy", "NayaPOWER"

# Pinned at PR #2535 merge (Shawn's word, 2026-10-13). Re-pin ONLY on his word.
CANONICAL = {
    "NAYA-ACTIVATION/OATH-OF-THE-NAYA-V1.md":
        "2f944ed99811de5cf506c5c78d1927b6b3bbbcf14be6e435a9260fb6cf75d9a0",
    "CONSTITUTION/NAYA-DOCTRINE-V1.md":
        "3196514104365dafbed09b000fe3ceb085d45e3becb5b554c08750db96391958",
    "CONSTITUTION/naya-doctrine.json":
        "ece56b147338ed9b4606d88bbf2a32659f3b3dd6c1746040103519638afb4b0c",
}

API = "https://api.github.com/repos/{o}/{r}/contents/{p}?ref={ref}"


def fetch(path: str, ref: str) -> bytes | None:
    url = API.format(o=OWNER, r=REPO, p=path, ref=ref)
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github.raw"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read()
    except Exception as e:
        if "404" in str(e):
            return None
        raise


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", default="main")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    results, drift, missing = [], False, False
    for path, pinned in CANONICAL.items():
        try:
            body = fetch(path, args.ref)
        except Exception:
            results.append({"path": path, "status": "SOURCE_UNREACHABLE"})
            if not args.json:
                print(f"SOURCE_UNREACHABLE  {path}")
            return 2
        if body is None:
            missing = True
            results.append({"path": path, "status": "NOT_ON_MAIN",
                            "note": "oath not yet deployed — integrity UNPROVEN, not passing"})
            if not args.json:
                print(f"NOT_ON_MAIN       {path}  (integrity UNPROVEN — exit 2, never PASS)")
            continue
        digest = hashlib.sha256(body).hexdigest()
        if digest == pinned:
            results.append({"path": path, "status": "PASS"})
            if not args.json:
                print(f"PASS              {path}")
        else:
            drift = True
            results.append({"path": path, "status": "DRIFT",
                            "expected": pinned[:12], "actual": digest[:12],
                            "note": "canonical text changed — ratification required"})
            if not args.json:
                print(f"DRIFT             {path}  expected {pinned[:12]} got {digest[:12]}")

    if args.json:
        print(json.dumps({"ref": args.ref,
                          "integrity": "DRIFT" if drift else ("UNPROVEN" if missing else "HOLD"),
                          "files": results}, indent=2))
    if drift:
        return 1
    if missing:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
