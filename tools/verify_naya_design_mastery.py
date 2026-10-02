#!/usr/bin/env python3
"""Structural integrity gate for the proposed Naya Design Mastery OS.

This gate verifies the design operating system is internally coherent enough to
review. It does NOT measure beauty and does NOT promote the system to canonical.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "NAYA-ACTIVATION" / "DESIGN" / "MASTERY"

REQUIRED = [
    "00-NAYA-DESIGN-MASTERY-CONSTITUTION-V1.md",
    "01-NAYA-SIGNATURE-LANGUAGE-V1.md",
    "02-NAYA-AUTONOMOUS-DESIGN-LOOP-V1.md",
    "03-NAYA-DESIGN-QUALIFICATION-V1.md",
    "04-NAYA-DESIGN-GYM-V1.md",
    "05-DESIGN-SOURCE-CONVERGENCE-V1.md",
    "06-DESIGN-MASTERY-100-ACTION-PLAN-V1.md",
    "07-NAYA-PAGE-BUILD-RECIPE-V1.md",
    "08-DESIGN-EVIDENCE-PACKAGE-TEMPLATE-V1.md",
    "NAYA-DESIGN-MASTERY-V1.json",
    "GOLD-STANDARD-REGISTRY-V1.json",
]

EXPECTED_DIAGNOSTICS = [f"Q{i:02d}_" for i in range(1, 21)]
EXPECTED_MATURITY = [f"M{i}" for i in range(7)]

def error(msg: str, errors: list[str]) -> None:
    errors.append(msg)

def main() -> int:
    errors: list[str] = []

    for name in REQUIRED:
        if not (BASE / name).is_file():
            error(f"missing required mastery artifact: {name}", errors)

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1

    machine = json.loads((BASE / "NAYA-DESIGN-MASTERY-V1.json").read_text(encoding="utf-8"))
    registry = json.loads((BASE / "GOLD-STANDARD-REGISTRY-V1.json").read_text(encoding="utf-8"))

    if machine.get("status") != "HUMAN_DIRECTOR_DIRECTED_PROPOSED_CANONICAL":
        error("machine contract must remain PROPOSED until ratified", errors)

    files = machine.get("canonical_files", {})
    for _, rel in files.items():
        p = ROOT / rel
        if not p.is_file():
            error(f"machine contract references missing file: {rel}", errors)

    diagnostics = machine.get("diagnostic_lenses", [])
    if len(diagnostics) != 20:
        error(f"expected 20 design diagnostic lenses, got {len(diagnostics)}", errors)
    for prefix in EXPECTED_DIAGNOSTICS:
        if not any(x.startswith(prefix) for x in diagnostics):
            error(f"missing diagnostic prefix {prefix}", errors)

    levels = machine.get("maturity_levels", {})
    if sorted(levels.keys()) != EXPECTED_MATURITY:
        error(f"maturity levels must be M0..M6, got {sorted(levels.keys())}", errors)

    loops = machine.get("loops", {})
    for name in ("generation", "quality", "completion", "learning"):
        if not loops.get(name):
            error(f"missing non-empty loop: {name}", errors)

    if "Project-specific scorecard remains authoritative" not in machine.get("canonical_scorecard_rule", ""):
        error("machine contract must explicitly preserve project-specific scorecard authority", errors)

    if "Do not self-declare mastery" not in machine.get("mastery_claim_rule", ""):
        error("machine contract must prohibit self-declared mastery", errors)

    constitution = (BASE / "00-NAYA-DESIGN-MASTERY-CONSTITUTION-V1.md").read_text(encoding="utf-8")
    law_count = len(re.findall(r"^## LAW\s+\d+\s+—", constitution, flags=re.MULTILINE))
    if law_count < 20:
        error(f"constitution expected at least 20 explicit laws, found {law_count}", errors)

    if "SELF-BUILD DOES NOT MEAN SELF-AUTHORIZE" not in constitution:
        error("constitution missing autonomy/authority boundary", errors)
    if "COMPLETE PRODUCT BEFORE SCREENSHOT SUCCESS" not in constitution:
        error("constitution missing whole-product completion law", errors)
    if "SIGNATURE IS GRAMMAR, NOT SKIN" not in constitution:
        error("constitution missing signature grammar law", errors)

    actions = (BASE / "06-DESIGN-MASTERY-100-ACTION-PLAN-V1.md").read_text(encoding="utf-8")
    numbered = set(int(n) for n in re.findall(r"^(\d+)\.", actions, flags=re.MULTILINE))
    missing_actions = [n for n in range(1, 101) if n not in numbered]
    if missing_actions:
        error(f"100-action roadmap missing actions: {missing_actions}", errors)

    allowed_states = set(registry.get("entry_states", []))
    required_states = {"REFERENCE_FLOOR", "CANDIDATE", "GOLD_ACCEPTED", "ANTI_EXAMPLE", "SUPERSEDED"}
    if allowed_states != required_states:
        error(f"gold registry states mismatch: {allowed_states}", errors)

    for entry in registry.get("entries", []):
        if entry.get("state") == "GOLD_ACCEPTED" and not entry.get("evidence_refs"):
            error(f"GOLD_ACCEPTED entry {entry.get('id')} has no evidence_refs", errors)
        source = entry.get("source_ref")
        if source and not (ROOT / source).exists():
            error(f"registry entry {entry.get('id')} references missing source: {source}", errors)

    convergence = (BASE / "05-DESIGN-SOURCE-CONVERGENCE-V1.md").read_text(encoding="utf-8")
    for pr in ("#1281", "#1285", "#1294", "#1306", "#1308", "#1309", "#1310"):
        if pr not in convergence:
            error(f"convergence report missing reviewed lane {pr}", errors)

    print("NAYA DESIGN MASTERY OS: STRUCTURALLY CONSISTENT" if not errors else "NAYA DESIGN MASTERY OS: FAIL")
    if errors:
        for item in errors:
            print(" -", item)
        return 1

    print(f"Required artifacts: {len(REQUIRED)}")
    print(f"Constitution laws: {law_count}")
    print(f"Diagnostic lenses: {len(diagnostics)}")
    print("Roadmap actions: 100")
    print("Gold accepted examples:", sum(1 for x in registry.get("entries", []) if x.get("state") == "GOLD_ACCEPTED"))
    print("NOTE: structural consistency is not visual/design qualification.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
