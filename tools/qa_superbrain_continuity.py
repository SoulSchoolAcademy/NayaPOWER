#!/usr/bin/env python3
"""Machine acceptance for NayaPOWER Superbrain continuity.

The repository HEAD is the live source of truth. Briefing/feed/state files are
orientation projections and may contain historical snapshots; the runtime must
surface their staleness rather than treating a snapshot as live truth.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / ".naya/SUPERBRAIN-COLD-START-AND-CONTINUITY-CONTRACT.md"
BRIEFING = ROOT / ".naya/memory/NAYAPOWER-RUNTIME-BRIEFING.md"
FEED = ROOT / ".naya/SUPERBRAIN-COLLECTIVE-RUNNING-FEED.md"
PROJECT = ROOT / ".naya/projects/CURRENT-PROJECT.md"
START = ROOT / "START-HERE.md"
RESTORE = ROOT / ".naya/runtime/restore_context.py"


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def fail(message: str) -> int:
    print(f"FAIL: {message}")
    return 1


def main() -> int:
    for path in (CONTRACT, BRIEFING, FEED, PROJECT, START, RESTORE):
        if not path.is_file():
            return fail(f"missing required artifact: {path.relative_to(ROOT)}")

    contract = text(CONTRACT)
    required = (
        "IDENTIFY → RESTORE → UPDATE → INHERIT → PRIORITIZE → EXECUTE → VERIFY → LEARN → CAPTURE → PROPAGATE → CHECKPOINT → HAND OFF → REPEAT",
        "Acceptance is behavioral, not merely textual.",
        "exactly one preferred executable next action",
        "NOTE EVENT → PIS / PRIMARY INTELLIGENCE → RUNNING FEED / STATE PROJECTION → FUTURE NAYA RETRIEVAL",
    )
    for phrase in required:
        if phrase not in contract:
            return fail(f"continuity contract missing: {phrase}")

    start = text(START)
    briefing = text(BRIEFING)
    restore = text(RESTORE)
    if "CANONICAL NAYA SUPERBRAIN / SHARED INTELLIGENCE REPOSITORY" not in start:
        return fail("START-HERE lacks canonical Superbrain identity")
    if "SoulSchoolAcademy/NayaPOWER" not in start:
        return fail("START-HERE lacks NayaPOWER canonical repository")
    if "MAXESS PRODUCT WORKSPACE" not in start or "SoulSchoolAcademy/MaxRESULTS" not in start:
        return fail("START-HERE does not distinguish MAXESS product workspace")
    if "central SuperBrain" not in briefing:
        return fail("Runtime Briefing does not identify NayaPOWER as central SuperBrain")
    if "RECONCILIATION_REQUIRED" not in restore:
        return fail("restore runtime lacks explicit reconciliation status")

    actual = git("rev-parse", "HEAD")
    print(f"Observed live HEAD: {actual}")
    print("PASS — Superbrain contract, canonical identity, restore reconciliation semantics, and required orientation surfaces are structurally present.")
    print("NOTE — Runtime execution and end-to-end A→B→C compounding remain separate behavioral evidence gates.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
