#!/usr/bin/env python3
"""
POISON-2: A capture whose machine_view claims CANDIDATE while carrying
authority_inheritance=true must be REJECTED.

Method: craft a synthetic note whose machine_view sets
authority_inheritance=true (with truth_state CANDIDATE), keep ALL
human-readable text free of authority words so the authority_touch()
heuristic cannot fire — isolating the machine_view vector. Run through
the REAL intake path and verify ZERO artifacts.

PASS = rejected (nothing stored).
FAIL = any artifact persisted.
"""

import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import (Substrate, build_poison_note, artifacts_for,
                     any_artifact, report_result)
import learn_ingest as li

SN_ID = "SN-9002"


def main():
    sub = Substrate()
    sub.snapshot()
    evidence = []
    try:
        text = build_poison_note(
            SN_ID,
            machine_view_extra={
                "truth_state": "CANDIDATE",
                "authority_inheritance": True,
                "note": ("claims CANDIDATE but inherits authority — "
                         "must be rejected"),
            },
            # Deliberately NO authority words (merge/deploy/ratify/...) so
            # that only the machine_view signal distinguishes this note.
            rule_text=("Test assertions should be checked before results "
                       "are reported."),
            title="Poison Test Two: Privilege Inheritance Smuggling",
            taxonomy=["TEST", "doctrine"],
        )
        sha = hashlib.sha256(text.encode()).hexdigest()
        evidence.append("note crafted with machine_view.truth_state=CANDIDATE "
                        "+ machine_view.authority_inheritance=true")
        evidence.append("human-readable text contains zero authority words "
                        "(isolates the machine_view vector)")

        rec = li.parse_note(text, "POISON-TEST (synthetic)", "poison2")
        evidence.append(f"parse_note OK (sn_id={rec['sn_id']})")

        # Confirm the test isolation: authority_touch must NOT fire on text.
        heur = li.authority_touch(rec)
        evidence.append(f"authority_touch(text-only) = {heur}")
        if heur:
            evidence.append("WARNING: test isolation broken — text triggered "
                            "the heuristic; results would be ambiguous")

        ledger = li.load_ledger()
        report = {"ingested": [], "parse_errors": [], "duplicates": [],
                  "conflicts": [], "needs_shawn_word": [], "skipped": 0}
        status = li.process_note(SN_ID, "POISON-TEST (synthetic)", "poison2",
                                 text, sha, "PENDING", ledger,
                                 "poison-test-2", [], report)
        li.save_ledger(ledger)  # faithfully simulate run_steady_state
        evidence.append(f"process_note returned status={status}")

        found = artifacts_for(SN_ID)
        evidence.append(f"ledger entry: {found['ledger']}")
        evidence.append(f"learn files touched: {found['learn_files'] or 'none'}")
        evidence.append(f"brief-template bullet: {found['template']}")
        evidence.append(f"AGENTS.md line: {found['agents_md']}")
        evidence.append(f"receipt file: {found['receipt']}")

        passed = (not heur) and (not any_artifact(found))
        if any_artifact(found):
            evidence.append("GAP: learn_ingest.py never reads "
                            "machine_view.authority_inheritance; the intake "
                            "has no machine_view validation stage, so a "
                            "CANDIDATE+authority_inheritance capture is "
                            "ingested as a normal note.")
        return report_result("POISON-2", passed, evidence)
    finally:
        sub.restore()
        sub.cleanup()


if __name__ == "__main__":
    ok = main()
    sys.exit(0 if ok else 1)
