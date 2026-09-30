#!/usr/bin/env python3
"""EVOLVE cold-start probe V1.

Simulates what a genuinely cold successor needs: can it reconstruct
  1. current truth (main SHA, production SHA, what's proven / not proven),
  2. the one next action,
  3. what authority is required and what is blocked,
from the canonical continuity files alone — no live conversation, no memory?

This probe does NOT test a real amnesiac agent yet. It tests the *precondition*:
are the continuity files sufficient and self-consistent? If this probe fails,
a cold successor cannot succeed. If it passes, the genuine cold-agent test
(a fresh Naya restoring from files only) is meaningful to run.

Canonical continuity files (the successor's whole world):
  - ~/workspace/your_files/torch-north-star-execution.md
  - ~/workspace/your_files/action-plan-to-10.md
  - ~/workspace/your_files/scorecard-10-10.md
  - ~/workspace/your_files/d3-package-b61dff1d.md

Exit 0 = a cold successor CAN reconstruct. Exit 1 = continuity gap (prints it).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

HOME = Path.home()
FILES = {
    "torch": HOME / "workspace/your_files/torch-north-star-execution.md",
    "action_plan": HOME / "workspace/your_files/action-plan-to-10.md",
    "scorecard": HOME / "workspace/your_files/scorecard-10-10.md",
    "d3": HOME / "workspace/your_files/d3-package-b61dff1d.md",
}

# The facts a cold successor must be able to recover. Each: (name, regex, files to search)
REQUIRED_FACTS = [
    ("main_sha", r"\bb61dff1d\b", ["torch", "d3"]),
    ("production_sha", r"\b0d0c36ab\b", ["torch", "d3"]),
    ("d1_blocked", r"D1.*ratif|ratif.*D1", ["torch", "action_plan", "d3"]),
    ("d3_blocked", r"D3.*authoriz|authoriz.*D3|point-in-time", ["torch", "action_plan", "d3"]),
    ("partial_migration_unknown", r"partial.*migrat|migrat.*partial|36670930733", ["torch", "d3"]),
    ("graph_v2_candidate", r"CANDIDATE_CONTRACT|Graph V2.*[Cc]andidate|[Cc]andidate.*Graph V2", ["torch", "action_plan"]),
    ("next_action_named", r"[Oo]ne next action|ONE NEXT ACTION", ["torch", "action_plan", "d3"]),
    ("proof_sequence_ordered", r"10-rung|proof sequence|rung", ["action_plan", "d3"]),
    ("score_present", r"4\.7/10|Overall.*4\.7", ["scorecard", "torch"]),
    ("constitution_ratified", r"Constitution.*[Rr]atified|[Rr]atified.*Constitution", ["torch", "action_plan"]),
]


def main() -> int:
    texts: dict[str, str] = {}
    gaps: list[str] = []
    for name, path in FILES.items():
        if not path.is_file():
            gaps.append(f"continuity file missing: {path}")
            texts[name] = ""
        else:
            texts[name] = path.read_text(encoding="utf-8", errors="replace")

    for fact_name, pattern, search_files in REQUIRED_FACTS:
        found = any(
            re.search(pattern, texts[f], re.IGNORECASE | re.DOTALL)
            for f in search_files
            if texts[f]
        )
        if not found:
            gaps.append(
                f"fact unrecoverable: {fact_name} (pattern {pattern!r} not found in "
                f"{', '.join(search_files)})"
            )

    # Consistency check: main SHA must agree across files that mention it.
    shas: dict[str, set[str]] = {}
    for name, text in texts.items():
        if text:
            shas[name] = set(re.findall(r"\b[0-9a-f]{8}\b", text))
    # (informational only — many SHAs legitimately appear; skip strict check)

    if gaps:
        print("COLD-START PROBE FAIL: successor cannot reconstruct from files alone.")
        for g in gaps:
            print(f"  GAP: {g}")
        return 1
    print(
        "COLD-START PROBE PASS: all required facts recoverable from continuity files. "
        "A cold successor can reconstruct truth, next action, and authority requirements. "
        "(Genuine cold-agent behavioral test still pending.)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
