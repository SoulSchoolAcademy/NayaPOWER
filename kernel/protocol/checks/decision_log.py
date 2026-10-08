#!/usr/bin/env python3
"""SN-0522 — Self-Governing Intelligence.

"For admissible decisions, run the Value Calculus, pick the highest score,
act. Never ask A/B/C. Never wait."

Validates a decision record: the math must be visible, the winner must be
the math's winner (or an explicit override), and authority must have been
checked before acting.

Input record:
    {
      "decision": "<what was decided>",
      "options": [{"id": "a", "description": "..."}, {"id": "b", ...}],
      "scores": {"a": 7.5, "b": 8.2},          # total per option (see scorecard.py for dimensions)
      "winner": "b",
      "override_rationale": "<only if winner is not the top scorer>",
      "authority": {
        "admissible": true,
        "protected_gate_hit": false,
        "gates_checked": ["GATE-1", "GATE-2", "GATE-3", "GATE-4", "GATE-5"]
      },
      "decided_at": "<ISO-8601 timestamp>",
      "decider": "<seat or agent id>"
    }

Checks:
  1. >= 2 options considered (a single option is not a decision).
  2. Every option has a numeric score.
  3. winner is one of the options.
  4. winner == argmax(scores), unless override_rationale is present and non-empty.
  5. authority block present; all five gates listed as checked.
  6. If protected_gate_hit: the only admissible outcomes are refusal/escalation
     (winner must be "refuse" or "escalate", or action must be "none").
  7. decided_at and decider present (decisions expire; anonymous decisions are void).

Usage:
    python3 kernel/protocol/checks/decision_log.py \
        --record '{"decision": "...", ...}' [--json]
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks import emit, fail, load_record, result  # noqa: E402

REQUIRED_GATES = {"GATE-1", "GATE-2", "GATE-3", "GATE-4", "GATE-5"}
REFUSAL_WINNERS = {"refuse", "escalate", "none", "ask"}


def _is_number(x) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def check(record: dict) -> dict:
    reasons: list[str] = []
    details: dict = {"law": "SN-0522"}
    decision = record.get("decision") or "(unnamed decision)"
    details["decision"] = decision

    options = record.get("options")
    if not isinstance(options, list) or len(options) < 2:
        return fail(f"{decision}: fewer than 2 options considered — not a decision, a default",
                    details)
    opt_ids = [o.get("id") for o in options if isinstance(o, dict) and o.get("id")]
    if len(opt_ids) != len(options):
        return fail(f"{decision}: every option needs an id", details)
    reasons.append(f"{len(options)} options considered")

    scores = record.get("scores")
    if not isinstance(scores, dict):
        return fail(f"{decision}: scores missing — the math must be visible", details)
    unscored = [oid for oid in opt_ids if not _is_number(scores.get(oid))]
    if unscored:
        return fail(f"{decision}: options without numeric scores: {unscored}", details)
    reasons.append("all options scored")

    winner = record.get("winner")
    if winner not in opt_ids:
        return fail(f"{decision}: winner {winner!r} is not one of the options {opt_ids}", details)

    top = max(opt_ids, key=lambda oid: scores[oid])
    top_score = scores[top]
    if winner != top:
        override = record.get("override_rationale")
        if not override or not str(override).strip():
            return fail(
                f"{decision}: winner {winner!r} (score {scores[winner]}) is not the top scorer "
                f"{top!r} (score {top_score}) and no override_rationale given — "
                "the math decides unless an explicit reason overrides it",
                {**details, "top_scorer": top, "top_score": top_score},
            )
        reasons.append(f"winner {winner!r} overrides top scorer {top!r} with rationale")
        details["override"] = True
    else:
        reasons.append(f"winner {winner!r} is the top scorer ({top_score}) — math decides")
    details.update({"winner": winner, "winner_score": scores[winner]})

    authority = record.get("authority")
    if not isinstance(authority, dict):
        return fail(f"{decision}: authority block missing — authority was not checked", details)
    checked = set(authority.get("gates_checked") or [])
    missing_gates = sorted(REQUIRED_GATES - checked)
    if missing_gates:
        return fail(f"{decision}: protected gates not checked: {missing_gates}", details)
    reasons.append("all five protected gates checked")
    details["gates_checked"] = sorted(checked)

    if authority.get("protected_gate_hit"):
        if winner not in REFUSAL_WINNERS and not authority.get("shawn_approval"):
            return fail(
                f"{decision}: protected gate hit but winner is {winner!r} with no shawn_approval — "
                "fail closed: refuse or escalate",
                details,
            )
        reasons.append("protected gate hit handled: refused/escalated or Shawn-approved")
        details["gate_hit_handled"] = True

    decided_at = record.get("decided_at")
    if not decided_at:
        return fail(f"{decision}: decided_at missing — decisions expire, timestamp required",
                    details)
    try:
        datetime.fromisoformat(str(decided_at).replace("Z", "+00:00"))
    except ValueError:
        return fail(f"{decision}: decided_at not ISO-8601: {decided_at!r}", details)
    reasons.append("timestamp present (SN-0493: re-check freshness before acting)")

    decider = record.get("decider")
    if not decider or not str(decider).strip():
        return fail(f"{decision}: decider unnamed — anonymous decisions are void", details)
    reasons.append(f"decider: {decider}")
    details["decider"] = decider

    reasons.append(f"{decision}: decision log complete — may act")
    return result(True, reasons, details)


def main() -> int:
    parser = argparse.ArgumentParser(description="SN-0522 decision-log check")
    parser.add_argument("--record", required=True,
                        help="JSON decision record (or @file)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()
    try:
        record = load_record(args.record)
    except Exception as e:
        return emit(fail(f"unparseable record: {e}", {"law": "SN-0522"}), args.json)
    return emit(check(record), args.json)


if __name__ == "__main__":
    sys.exit(main())
