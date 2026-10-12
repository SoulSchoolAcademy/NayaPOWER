#!/usr/bin/env python3
"""Dry-run receipt: replay Battery D's recorded borderline case through the
variance-first triage.

Input: tools/learn/fixtures/battery_d_TR-8DB748.json (ground truth from the
2026-10-12 Battery D run + rubric-sharpening probe).
Expected: READER_VARIANCE -- the disagreement dissolves on a cold re-read,
so no instrument change is warranted. The item is NOT re-graded.

Exit 0 iff the verdict matches the fixture's expected_verdict.
Exit 1 on any mismatch or triage refusal (that would itself be evidence).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from triage_disagreement import (  # noqa: E402
    DisagreementRecord,
    ReadRequest,
    TriageError,
    Vote,
    append_ledger,
    clear_frozen_rubrics,
    register_frozen_rubric,
    triage_disagreement,
)

FIXTURE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "fixtures", "battery_d_TR-8DB748.json")
DEFAULT_LEDGER = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "ledger.jsonl")


def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--ledger", default=DEFAULT_LEDGER,
                    help="JSONL ledger to append the verdict to "
                    "(default: tools/learn/ledger.jsonl). Pass '' to skip.")
    args = ap.parse_args(argv)

    clear_frozen_rubrics()
    fx = json.load(open(FIXTURE))
    sha = register_frozen_rubric(fx["record"]["rubric_id"], fx["rubric_text"])
    record = DisagreementRecord(
        item_id=fx["record"]["item_id"],
        cell=fx["record"]["cell"],
        rubric_id=fx["record"]["rubric_id"],
        rubric_sha256=sha,  # the frozen instrument; fixture carries no magic hash
        votes=[Vote(**v) for v in fx["record"]["votes"]],
    )
    fresh = [Vote(**v) for v in fx["fresh_votes"]]
    it = iter(fresh)

    def replay(req: ReadRequest) -> Vote:
        # Information-isolation check: the reader seam must never see the
        # original votes. Enforced mechanically here, asserted again in tests.
        assert not hasattr(req, "original_votes"), "reader seam contaminated"
        return next(it)

    try:
        verdict = triage_disagreement(
            record, replay, n_readers=len(fresh),
            item_text=fx["item_text"], rubric_text=fx["rubric_text"],
            evidence_extra={"dry_run": "battery-D-TR-8DB748-replay-2026-10-12"},
        )
    except TriageError as e:
        print(f"DRY-RUN FAILED: triage refused: {e}", file=sys.stderr)
        return 1

    print(verdict.to_json())
    if verdict.verdict != fx["expected_verdict"]:
        print(f"DRY-RUN MISMATCH: got {verdict.verdict}, expected "
              f"{fx['expected_verdict']}", file=sys.stderr)
        return 1
    if verdict.verdict == "READER_VARIANCE" and verdict.evidence.get("instrument_change") is not None:
        print("DRY-RUN MISMATCH: READER_VARIANCE must carry no instrument change",
              file=sys.stderr)
        return 1
    if args.ledger:
        append_ledger(args.ledger, verdict)
        print(f"ledger <- {args.ledger}", file=sys.stderr)
    print(f"DRY-RUN OK: {record.item_id}/{record.cell} -> {verdict.verdict} "
          f"(fresh readers unanimous: {verdict.fresh_unanimous})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
