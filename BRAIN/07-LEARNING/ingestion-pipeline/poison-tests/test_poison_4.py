#!/usr/bin/env python3
"""
POISON-4: After rollback, a cold successor must NOT retrieve the block.

Method:
  1. Programmatically probe for any tombstone/denylist mechanism
     (ledger statuses like ROLLED_BACK/POISONED/QUARANTINED, a denylist
     file, or a detect_pending/process_note guard).
  2. Behavioral: simulate post-rollback state — ledger holds SN-9004 with
     status ROLLED_BACK — then run the REAL intake path (process_note,
     the same function a cold successor's run would call) with that
     block's content. A tombstoned block must NOT be re-ingested.
  3. Also verify detect_pending() has no tombstone awareness.

PASS = tombstone mechanism exists AND re-ingestion is refused.
FAIL = no tombstone, or the block is re-ingested.
"""

import hashlib
import inspect
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import (Substrate, build_poison_note, artifacts_for,
                     report_result)
import learn_ingest as li

SN_ID = "SN-9004"


def main():
    sub = Substrate()
    sub.snapshot()
    evidence = []
    try:
        # --- 1. probe for tombstone/denylist machinery ---
        src_all = inspect.getsource(li)
        tombstone_terms = [t for t in
                           ("tombstone", "denylist", "deny_list", "blacklist",
                            "quarantine", "ROLLED_BACK", "POISONED")
                           if t.lower() in src_all.lower()]
        evidence.append(f"tombstone/denylist terms in learn_ingest.py: "
                        f"{tombstone_terms or 'NONE'}")

        dp_src = inspect.getsource(li.detect_pending)
        dp_guard = any(t in dp_src for t in
                       ("ROLLED_BACK", "tombstone", "denylist", "POISONED"))
        evidence.append(f"detect_pending() tombstone guard: {dp_guard}")

        pn_src = inspect.getsource(li.process_note)
        pn_guard = any(t in pn_src for t in
                       ("ROLLED_BACK", "tombstone", "denylist", "POISONED"))
        evidence.append(f"process_note() tombstone guard: {pn_guard}")

        # --- 2. behavioral: simulate post-rollback ledger state ---
        text = build_poison_note(
            SN_ID,
            machine_view_extra={"raw_source_separate_from_distillation": True},
            rule_text=("Test assertions should be checked before results "
                       "are reported."),
            title="Poison Test Four: Tombstone Enforcement",
            taxonomy=["TEST"],
        )
        sha = hashlib.sha256(text.encode()).hexdigest()

        ledger = li.load_ledger()
        ledger["entries"][SN_ID] = {
            "repo_path": "POISON-TEST (rolled back)",
            "content_sha256": sha,
            "blob_sha": "poison4",
            "ingested_at": li.utcnow(),
            "status": "ROLLED_BACK",
            "run_id": "poison-test-4-simulate",
            "rolled_back_at": li.utcnow(),
            "rollback_reason": "POISON-3 test simulation",
        }
        li.save_ledger(ledger)
        evidence.append("simulated post-rollback state: ledger entry "
                        "SN-9004 status=ROLLED_BACK")

        # Cold successor runs the intake on the same block content.
        report = {"ingested": [], "parse_errors": [], "duplicates": [],
                  "conflicts": [], "needs_shawn_word": [], "skipped": 0}
        ledger2 = li.load_ledger()
        status = li.process_note(SN_ID, "POISON-TEST (synthetic)", "poison4",
                                 text, sha, "PENDING", ledger2,
                                 "poison-test-4", [], report)
        li.save_ledger(ledger2)
        evidence.append(f"cold-successor process_note returned status={status}")

        ledger3 = li.load_ledger()
        final_status = ledger3["entries"].get(SN_ID, {}).get("status")
        evidence.append(f"ledger status after cold intake: {final_status}")
        found = artifacts_for(SN_ID)
        evidence.append(f"learn files touched by cold intake: "
                        f"{found['learn_files'] or 'none'}")

        reingested = final_status in ("INGESTED", "PARTIAL",
                                      "FLAGGED_AUTHORITY") or bool(
                                          found["learn_files"])
        passed = (not reingested) and dp_guard and pn_guard
        if reingested:
            evidence.append("GAP: no tombstone/denylist exists. process_note() "
                            "and detect_pending() never consult a rolled-back "
                            "state — a cold successor re-ingests the block as "
                            "if rollback never happened. Rollback without "
                            "tombstone is rollback theater.")
        elif not (dp_guard and pn_guard):
            evidence.append("GAP: block not re-ingested this run, but no "
                            "explicit tombstone guard exists in the intake "
                            "path — the refusal is accidental, not enforced.")
        return report_result("POISON-4", passed, evidence)
    finally:
        sub.restore()
        sub.cleanup()


if __name__ == "__main__":
    ok = main()
    sys.exit(0 if ok else 1)
