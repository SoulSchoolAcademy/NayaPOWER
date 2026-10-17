#!/usr/bin/env python3
"""
POISON-1: A capture carrying raw_source_separate_from_distillation=false
must be REJECTED at intake, not stored.

Method: craft a synthetic note whose machine_view explicitly sets
raw_source_separate_from_distillation=false, run it through the REAL
intake path (parse_note -> process_note), then verify ZERO substrate
artifacts were created.

PASS = rejected (no ledger entry, no learn file section, no template
       bullet, no receipt, no AGENTS.md line).
FAIL = any artifact persisted.
"""

import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import (Substrate, build_poison_note, artifacts_for,
                     any_artifact, report_result)
import learn_ingest as li

SN_ID = "SN-9001"


def main():
    sub = Substrate()
    sub.snapshot()
    evidence = []
    try:
        # The poison signal lives ONLY in machine_view; the human-readable
        # text is deliberately clean so the authority heuristic cannot
        # catch it — this isolates the machine_view vector.
        text = build_poison_note(
            SN_ID,
            machine_view_extra={
                "raw_source_separate_from_distillation": False,
                "note": ("claims raw source was NOT kept separate from "
                         "distillation — must be rejected"),
            },
            rule_text=("Test assertions should be checked before results "
                       "are reported."),
            title="Poison Test One: Source Separation Violation",
            taxonomy=["TEST", "doctrine"],  # force template-bullet routing
        )
        sha = hashlib.sha256(text.encode()).hexdigest()
        evidence.append("note crafted with "
                        "machine_view.raw_source_separate_from_distillation=false")

        # --- run the REAL intake path ---
        rec = li.parse_note(text, "POISON-TEST (synthetic)", "poison1")
        evidence.append(f"parse_note OK (sn_id={rec['sn_id']})")

        ledger = li.load_ledger()
        report = {"ingested": [], "parse_errors": [], "duplicates": [],
                  "conflicts": [], "needs_shawn_word": [], "skipped": 0}
        status = li.process_note(SN_ID, "POISON-TEST (synthetic)", "poison1",
                                 text, sha, "PENDING", ledger,
                                 "poison-test-1", [], report)
        li.save_ledger(ledger)  # faithfully simulate run_steady_state
        evidence.append(f"process_note returned status={status}")

        # --- assertions: NOTHING may be stored ---
        found = artifacts_for(SN_ID)
        evidence.append(f"ledger entry: {found['ledger']}")
        evidence.append(f"learn files touched: {found['learn_files'] or 'none'}")
        evidence.append(f"brief-template bullet: {found['template']}")
        evidence.append(f"AGENTS.md line: {found['agents_md']}")
        evidence.append(f"receipt file: {found['receipt']}")

        passed = not any_artifact(found)
        if not passed:
            evidence.append("GAP: learn_ingest.py never reads "
                            "machine_view.raw_source_separate_from_distillation; "
                            "parse_note() extracts no machine_view fields at all, "
                            "so the poison signal is invisible to intake.")
        return report_result("POISON-1", passed, evidence)
    finally:
        sub.restore()
        sub.cleanup()


if __name__ == "__main__":
    ok = main()
    sys.exit(0 if ok else 1)
