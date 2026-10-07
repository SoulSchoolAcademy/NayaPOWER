#!/usr/bin/env python3
"""SN-0526 — Quality Before Speed.

"No deliverable below 9/10 reaches Shawn. Build -> Verify -> Scorecard -> Gate -> Deliver."

Validates a deliverable record before it may be presented as done.
Every stage must have evidence; a missing stage fails the gate.

Input record:
    {
      "deliverable": "<name/description>",
      "build_evidence": "<commit sha, branch, or artifact reference>",
      "verification_evidence": "<test run, drill result, or verifier reference>",
      "scorecard": {"score": 9.2, "scorer": "<named human or seat>"},
      "gates": [{"name": "<gate>", "result": "pass"}, ...]
    }

Checks:
  1. build_evidence present and non-empty.
  2. verification_evidence present and non-empty (implemented != verified).
  3. scorecard.score is numeric and >= 9.0.
  4. scorecard.scorer is a named identity (anonymous scores are not scores).
  5. gates: at least one gate listed, every listed gate result == "pass".

Note: SN-0526 is CANDIDATE (awaiting ratification) in the manifest. The 9.0
bar is enforced as written; the law's status is reported in details so
consumers know the enforcement basis.

Usage:
    python3 tools/protocol/checks/quality_gate.py \
        --record '{"deliverable": "...", ...}' [--json]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks import emit, fail, load_record, result  # noqa: E402

QUALITY_BAR = 9.0


def check(record: dict) -> dict:
    reasons: list[str] = []
    details: dict = {"law": "SN-0526", "law_status": "CANDIDATE", "bar": QUALITY_BAR}

    deliverable = record.get("deliverable") or "(unnamed)"
    details["deliverable"] = deliverable

    build = record.get("build_evidence")
    if not build or not str(build).strip():
        return fail(f"{deliverable}: build_evidence missing — nothing was built, nothing to gate",
                    details)
    reasons.append("build evidence present")

    verification = record.get("verification_evidence")
    if not verification or not str(verification).strip():
        return fail(f"{deliverable}: verification_evidence missing — implemented != verified",
                    details)
    reasons.append("verification evidence present")

    scorecard = record.get("scorecard")
    if not isinstance(scorecard, dict):
        return fail(f"{deliverable}: scorecard missing or malformed — no receipt, no delivery",
                    details)
    score = scorecard.get("score")
    if not isinstance(score, (int, float)) or isinstance(score, bool):
        return fail(f"{deliverable}: scorecard.score not numeric: {score!r}", details)
    if score < QUALITY_BAR:
        return fail(
            f"{deliverable}: score {score} < bar {QUALITY_BAR} — goes back, never forward",
            {**details, "score": score},
        )
    scorer = scorecard.get("scorer")
    if not scorer or not str(scorer).strip():
        return fail(f"{deliverable}: scorecard.scorer unnamed — anonymous scores are not scores",
                    {**details, "score": score})
    reasons.append(f"scorecard {score} >= {QUALITY_BAR} by {scorer}")
    details.update({"score": score, "scorer": scorer})

    gates = record.get("gates")
    if not isinstance(gates, list) or not gates:
        return fail(f"{deliverable}: gates list missing/empty — no gate, no delivery", details)
    failed_gates = [
        g.get("name", "?") for g in gates
        if not isinstance(g, dict) or g.get("result") != "pass"
    ]
    if failed_gates:
        return fail(f"{deliverable}: gates not passing: {failed_gates}", details)
    reasons.append(f"{len(gates)} gate(s) all pass")
    details["gates_passed"] = len(gates)

    reasons.append(f"{deliverable}: BUILD -> VERIFY -> SCORECARD -> GATE complete — may deliver")
    return result(True, reasons, details)


def main() -> int:
    parser = argparse.ArgumentParser(description="SN-0526 quality gate check")
    parser.add_argument("--record", required=True,
                        help="JSON deliverable record (or @file)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()
    try:
        record = load_record(args.record)
    except Exception as e:
        return emit(fail(f"unparseable record: {e}", {"law": "SN-0526"}), args.json)
    return emit(check(record), args.json)


if __name__ == "__main__":
    sys.exit(main())
