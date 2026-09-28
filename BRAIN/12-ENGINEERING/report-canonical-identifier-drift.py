#!/usr/bin/env python3
"""Report drift in NayaPOWER's canonical identifiers.

WHY THIS IS A REPORT AND NOT A TEST
-----------------------------------
Three separate things are currently broken by the same root cause:

  * `learning-influence-experiment` (live job) fails on a hardcoded learning_id
  * `tests/test_learning_promotion_workflow.py` asserts an id no workflow contains
  * `tests/test_live_fresh_lesson_intelligence_commit.py` fails for an unrelated reason

All of them trace to the same thing: canonical identifiers (OWNER_ID, LEARNING_ID,
grant ids) are DUPLICATED by hand across edge-function source, CI workflows and
tests, with no single source of truth, and they have already drifted apart.

Resolving that requires an OWNER decision - which identifier is canonical - and it
is emphatically not mine to make. Adding a third failing test would be a third
symptom of a problem that already has two; it would not add information, and it
would make `main` look worse without making anyone closer to a fix.

So this is a diagnostic. It exits 0. It enumerates the WHOLE set, names every
occurrence with file and line, states which identifiers disagree, and prints the
one-sentence decision each owner needs to make.

It is deliberately a report rather than a gate, for the same reason a drift
DETECTOR for edge functions is a gate but this is not: for functions, drift is
mechanically decidable (does the deployed artifact match canonical source?). For
identifiers, the canonical VALUE is a human decision, and no detector can infer it.

Usage:
  python BRAIN/12-ENGINEERING/report-canonical-identifier-drift.py
Exit codes: 0 always - this reports, it does not gate.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TESTS = REPO / "tests"
WORKFLOWS = REPO / ".github" / "workflows"
FUNCTIONS = REPO / "supabase" / "functions"

UUID = re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b")
# A nil UUID is a deliberate placeholder, not a real identifier.
PLACEHOLDERS = {"00000000-0000-0000-0000-000000000000"}


def _occurrences() -> dict:
    """Every hardcoded UUID, keyed by identifier -> list of (layer, file, line)."""
    found: dict = {}
    for path in sorted(TESTS.glob("*.py")):
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for m in UUID.findall(line):
                if m not in PLACEHOLDERS:
                    found.setdefault(m, []).append(("test", path.relative_to(REPO).as_posix(), i))
    for path in sorted(WORKFLOWS.glob("*.yml")):
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for m in UUID.findall(line):
                if m not in PLACEHOLDERS:
                    found.setdefault(m, []).append(("workflow", path.relative_to(REPO).as_posix(), i))
    for path in sorted(FUNCTIONS.rglob("index.ts")):
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for m in UUID.findall(line):
                if m not in PLACEHOLDERS:
                    found.setdefault(m, []).append(("function", path.relative_to(REPO).as_posix(), i))
    return found


def _layers(occurrences: list) -> set:
    return {layer for layer, _, _ in occurrences}


def main() -> int:
    found = _occurrences()
    print("=" * 78)
    print("CANONICAL IDENTIFIER DRIFT REPORT")
    print("=" * 78)
    print(f"  identifiers hardcoded across tests/, workflows/ and edge functions: {len(found)}")
    total = sum(len(v) for v in found.values())
    print(f"  total occurrences: {total}")
    print()

    problems: list = []
    for ident, occ in sorted(found.items()):
        layers = _layers(occ)
        print(f"  {ident}")
        print(f"      layers: {', '.join(sorted(layers))}   occurrences: {len(occ)}")
        for layer, f, line in occ:
            print(f"        {layer:9} {f}:{line}")
        # An identifier asserted by a test but present in NO workflow cannot be
        # satisfied by a live run: the runtime has no way to produce it.
        if "test" in layers and "workflow" not in layers and "function" not in layers:
            problems.append((ident, "asserted by a test but declared in no workflow and no edge function"))
        print()

    if problems:
        print("-" * 78)
        print("DRIFT DETECTED")
        for ident, why in problems:
            print(f"  {ident}: {why}")
        print("-" * 78)
        print()
        print("OWNER DECISIONS REQUIRED (these are not a tester's to make):")
        for ident, _ in problems:
            print(f"  1. Which identifier is canonical for this concept - {ident}, or the one the")
            print("     live workflow actually uses?")
            print("  2. Once chosen, it should be declared ONCE and referenced everywhere")
            print("     (edge-function constant, workflow env, test import) rather than copied.")
        print()
        print("Do NOT 'fix' this by editing an expected value to match current runtime output.")
        print("That converts a real drift into a passing test, which is the failure mode this")
        print("project has been guarding against all along.")
    else:
        print("No drift detected.")

    print()
    print("This report always exits 0. It is a diagnostic, not a gate: the canonical VALUE is a")
    print("human decision, and no detector can infer it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
