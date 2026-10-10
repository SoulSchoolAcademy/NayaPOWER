#!/usr/bin/env python3
"""Persona preflight check for the SELF node.

Operational binding for the persona identity contract
(``BRAIN/03-KERNEL/NODES/SELF/0003-PERSONA-IDENTITY-CONTRACT-V1.md``,
CANDIDATE): every run loads the canonical persona object through
``kernel/persona_loader`` and asserts the coherence invariants mechanically.

Exit codes mirror the contract's failure states:
  0 = PASS -- canonical source loads, all pins hold, seat stays a designation.
  1 = FAIL -- a coherence invariant was violated (someone moved a pin).
  2 = HALT -- the canonical source is missing or unreadable. Per the contract
      the caller must halt identity presentation, never improvise a persona.

Emits a single machine-readable receipt JSON object on stdout on PASS;
human-readable diagnostics on stderr on FAIL/HALT.

Canonical source resolution order:
  1. ``--canonical PATH`` flag
  2. ``PERSONA_PREFLIGHT_CANONICAL`` environment variable
  3. ``<repo-root>/BRAIN/04-INTELLIGENCE/OBJECTS/NAYA-PERSONA-V1.json``
     where repo-root is the parent of this script's ``tools/`` directory.

This check is wired into the kernel-tests CI gate (``python -m pytest -q``
runs ``tests/test_persona_preflight.py``), so every tip must satisfy it.
It never claims RATIFIED status: only Shawn ratifies.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOLS_DIR.parent
sys.path.insert(0, str(REPO_ROOT))

from kernel.persona_loader import (  # noqa: E402
    PersonaIdentity,
    PersonaSourceMissing,
    load_persona,
    normalize_dictation_name,
    present_identity,
)

DEFAULT_CANONICAL = (
    REPO_ROOT / "BRAIN/04-INTELLIGENCE/OBJECTS/NAYA-PERSONA-V1.json"
)

# Coherence pins asserted by the preflight. These mirror the canonical object
# but are written out explicitly so that a drift between the object and the
# check is itself a loud, reviewable diff.
_EXPECTED_NAME = "Naya"
_EXPECTED_CHARACTER_PREFIX = "AI operating partner"
_EXPECTED_TONE = (
    "warm",
    "direct",
    "enthusiastic",
    "truthful",
    "practical",
    "clear",
)
_EXPECTED_SEAT_MARKER = "naya-1..naya-5"
_EXPECTED_CANONICAL_STATUSES = ("CANDIDATE", "RATIFIED")
_PREFLIGHT_SEAT = "naya-4"


def resolve_canonical(cli_path: str | None) -> Path:
    if cli_path:
        return Path(cli_path)
    env_path = os.environ.get("PERSONA_PREFLIGHT_CANONICAL")
    if env_path:
        return Path(env_path)
    return DEFAULT_CANONICAL


def repo_sha() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=15,
        )
        if out.returncode == 0:
            return out.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        pass
    return "unknown"


def check(persona: PersonaIdentity) -> list[str]:
    """Return a list of violated invariants; empty means PASS."""
    violations: list[str] = []
    if persona.name != _EXPECTED_NAME:
        violations.append(
            f"name pin moved: expected {_EXPECTED_NAME!r}, got {persona.name!r}"
        )
    if not persona.character.startswith(_EXPECTED_CHARACTER_PREFIX):
        violations.append(
            "character pin moved: does not start with "
            f"{_EXPECTED_CHARACTER_PREFIX!r}"
        )
    if tuple(persona.tone) != _EXPECTED_TONE:
        violations.append(
            f"tone pin moved: expected {_EXPECTED_TONE!r}, got {tuple(persona.tone)!r}"
        )
    if _EXPECTED_SEAT_MARKER not in persona.seat_semantics:
        violations.append(
            "seat_semantics pin moved: seat designations no longer enumerated"
        )
    if persona.canonical_status not in _EXPECTED_CANONICAL_STATUSES:
        violations.append(
            f"canonical_status unknown: {persona.canonical_status!r} "
            f"(expected one of {_EXPECTED_CANONICAL_STATUSES!r})"
        )
    # The seat must never be absorbed into durable identity: the presentation
    # renders it strictly as a role designation.
    sample = present_identity(persona, seat=_PREFLIGHT_SEAT)
    if _PREFLIGHT_SEAT not in sample or "not my identity" not in sample:
        violations.append(
            "seat absorption detected: presentation does not keep the seat "
            "as a role designation"
        )
    # Dictation rule: transcription variants resolve to Naya when addressed to
    # her, and are never treated as a rename otherwise.
    if normalize_dictation_name("Maya", addressed_to_naya=True) != "Naya":
        violations.append("dictation rule broken: 'Maya' did not resolve to Naya")
    if normalize_dictation_name("Maya", addressed_to_naya=False) != "Maya":
        violations.append(
            "dictation rule overreach: resolved 'Maya' when not addressed to Naya"
        )
    return violations


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="SELF persona preflight check")
    parser.add_argument(
        "--canonical",
        default=None,
        help="path to the canonical persona object JSON",
    )
    args = parser.parse_args(argv)

    canonical = resolve_canonical(args.canonical)
    try:
        persona = load_persona(canonical)
    except PersonaSourceMissing as exc:
        print(
            f"HALT: canonical persona source missing/unreadable: {exc}",
            file=sys.stderr,
        )
        print(
            "HALT: identity presentation must stop here; "
            "never improvise a persona from memory.",
            file=sys.stderr,
        )
        return 2

    violations = check(persona)
    if violations:
        print("FAIL: persona coherence invariants violated:", file=sys.stderr)
        for v in violations:
            print(f"  - {v}", file=sys.stderr)
        if persona.conflicts:
            print("logged conflicts (canonical won):", file=sys.stderr)
            for c in persona.conflicts:
                print(
                    f"  - {c.source}: {c.field} rejected {c.rejected_value!r}",
                    file=sys.stderr,
                )
        return 1

    receipt = {
        "check": "persona_preflight",
        "version": 1,
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "repo_sha": repo_sha(),
        "canonical": str(canonical),
        "result": "PASS",
        "name": persona.name,
        "tone": list(persona.tone),
        "canonical_status": persona.canonical_status,
        "conflicts_logged": len(persona.conflicts),
        "conflicts": [
            {"source": c.source, "field": c.field, "rejected_value": c.rejected_value}
            for c in persona.conflicts
        ],
        "presentation_sample": present_identity(persona, seat=_PREFLIGHT_SEAT),
        "ratified_claim": False,
        "note": "CANDIDATE contract; only Shawn ratifies.",
    }
    print(json.dumps(receipt, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
