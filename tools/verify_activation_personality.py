#!/usr/bin/env python3
"""Verify the Active Awesomeness activation wiring.

Checks, against a repository tree:
  1. The canonical personality pointer exists and is well-formed
     (BRAIN/03-KERNEL/0005-AWESOME-CODE-PROFILE-POINTER-V1.json).
  2. The Core Code lines in the pointer are self-consistent with their SHA-256.
  3. NAYA-ACTIVATION/KERNEL/PERSONALITY.md exists and contains the Core Code
     lines verbatim (byte-identical).
  4. Fail-closed resolution: CANDIDATE -> core code only (pass, explicit mode);
     RATIFIED -> ratified_profile must resolve, version and SHA-256 must match.
  5. Optionally (--receipt PATH): an activation receipt's `personality` block
     must agree with the pointer (core_code_sha256 match; profile fields match
     pointer status; no claimed ratified profile while pointer is CANDIDATE).

Exit 0 = all checks pass. Exit 1 = any failure, with FAIL: reason on stdout.
No network, no writes, no credentials.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

POINTER_REL = Path("BRAIN/03-KERNEL/0005-AWESOME-CODE-PROFILE-POINTER-V1.json")
PERSONALITY_REL = Path("NAYA-ACTIVATION/KERNEL/PERSONALITY.md")
VALID_STATUSES = {"CANDIDATE", "RATIFIED"}


def fail(reason: str) -> int:
    print(f"FAIL: {reason}")
    return 1


def canonical_core_code_bytes(lines: list[str]) -> bytes:
    return ("\n".join(lines) + "\n").encode("utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Verify activation personality wiring.")
    ap.add_argument("--repo", default=None, help="Repository root (default: inferred).")
    ap.add_argument("--receipt", default=None, help="Activation receipt JSON to validate.")
    args = ap.parse_args()

    repo = Path(args.repo) if args.repo else Path(__file__).resolve().parents[1]
    pointer_path = repo / POINTER_REL
    if not pointer_path.is_file():
        return fail(f"pointer missing: {POINTER_REL}")

    try:
        pointer = json.loads(pointer_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        return fail(f"pointer unreadable: {e}")

    status = pointer.get("status")
    if status not in VALID_STATUSES:
        return fail(f"pointer status unknown or missing: {status!r} (expected one of {sorted(VALID_STATUSES)})")

    core = pointer.get("core_code") or {}
    lines = core.get("lines")
    if not isinstance(lines, list) or not lines or not all(isinstance(l, str) for l in lines):
        return fail("pointer core_code.lines missing or malformed")
    digest = hashlib.sha256(canonical_core_code_bytes(lines)).hexdigest()
    if digest != core.get("sha256"):
        return fail("pointer core_code sha256 does not match recomputation from lines")

    personality_path = repo / PERSONALITY_REL
    if not personality_path.is_file():
        return fail(f"activation personality doc missing: {PERSONALITY_REL}")
    try:
        personality_text = personality_path.read_text(encoding="utf-8")
    except OSError as e:
        return fail(f"personality doc unreadable: {e}")
    for line in lines:
        if line not in personality_text:
            return fail(f"personality doc missing Core Code line verbatim: {line!r}")

    ratified = pointer.get("ratified_profile")
    if status == "RATIFIED":
        if not isinstance(ratified, dict):
            return fail("pointer is RATIFIED but ratified_profile is null or malformed")
        prof_rel = ratified.get("path")
        if not prof_rel:
            return fail("ratified_profile.path missing")
        prof_path = repo / prof_rel
        if not prof_path.is_file():
            return fail(f"ratified profile file missing: {prof_rel}")
        actual = hashlib.sha256(prof_path.read_bytes()).hexdigest()
        if actual != ratified.get("sha256"):
            return fail(
                f"ratified profile sha256 mismatch for {prof_rel}: "
                f"expected {ratified.get('sha256')}, got {actual}"
            )
        mode = f"RATIFIED profile {ratified.get('id')} v{ratified.get('version')}"
    else:
        if ratified is not None:
            return fail("pointer is CANDIDATE but ratified_profile is set")
        mode = "CANDIDATE (core code only)"

    if args.receipt:
        receipt_path = Path(args.receipt)
        try:
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as e:
            return fail(f"receipt unreadable: {e}")
        block = receipt.get("personality")
        if not isinstance(block, dict):
            return fail("receipt has no personality block")
        if block.get("core_code_sha256") != core.get("sha256"):
            return fail("receipt core_code_sha256 does not match pointer")
        if block.get("profile_status") != status:
            return fail(
                f"receipt profile_status {block.get('profile_status')!r} "
                f"does not match pointer status {status!r}"
            )
        if status == "CANDIDATE":
            if block.get("profile_sha256") not in (None, "") or block.get("profile_version") not in (None, ""):
                return fail("receipt claims a ratified profile while pointer is CANDIDATE")
        else:
            if block.get("profile_sha256") != ratified.get("sha256") or block.get("profile_version") != ratified.get("version"):
                return fail("receipt profile version/sha256 does not match pointer's ratified profile")

    print(f"PASS: activation personality wiring OK [{mode}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
