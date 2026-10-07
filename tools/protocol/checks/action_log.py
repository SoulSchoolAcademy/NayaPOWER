#!/usr/bin/env python3
"""SN-0575 — Fix It First, Report After.  +  SN-DONT-WAIT — Don't Wait, Just Do.

SN-0575: "If broken within authority, fix first, report after.
           Never ask 'should I fix this?'"
SN-DONT-WAIT: "If blocked on a stalled seat, do it yourself. Do it right.
           Record it. Report it."

Validates an action record for a fix-it-first repair or a stalled-lane
takeover. The hard line: touching a protected gate without Shawn's explicit
approval fails, no matter how good the fix was. Value never creates authority.

Input record:
    {
      "action": "<what was done>",
      "kind": "repair" | "takeover",
      "what_was_broken": "<description of the breakage or stall>",
      "authority_basis": "<law id, grant id, or standing authorization cited>",
      "what_was_done": "<description of the fix/action>",
      "verification": "<how the fix was verified to work>",
      "reported_to": "<feed, issue, or surface where it was reported>",
      "protected_gate_touched": false,
      "shawn_approval": "<required iff protected_gate_touched>",
      // takeover-only:
      "original_owner": "<seat that owned the stalled work>",
      "owner_notified": true,
      "stall_evidence": "<why the lane was considered stalled>"
    }

Checks:
  1. All core fields present and non-empty.
  2. kind is "repair" or "takeover".
  3. authority_basis cites something (law id / grant); "I felt like it" fails.
  4. verification present — a fix without verification is a claim (Evidence Law).
  5. reported_to present — "report after" is part of the law, not optional.
  6. If protected_gate_touched: shawn_approval required, else FAIL (hard line).
  7. If kind == "takeover": original_owner and owner_notified required, plus
     stall_evidence (take over stalled work, never active work).

Usage:
    python3 tools/protocol/checks/action_log.py \
        --record '{"action": "...", ...}' [--json]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks import emit, fail, load_record, result  # noqa: E402

CORE_FIELDS = ["action", "what_was_broken", "authority_basis",
               "what_was_done", "verification", "reported_to"]


def _nonempty(v) -> bool:
    return isinstance(v, str) and bool(v.strip())


def check(record: dict) -> dict:
    reasons: list[str] = []
    details: dict = {"laws": ["SN-0575", "SN-DONT-WAIT"]}
    action = record.get("action") or "(unnamed action)"
    details["action"] = action

    kind = record.get("kind")
    if kind not in ("repair", "takeover"):
        return fail(f"{action}: kind must be 'repair' or 'takeover', got {kind!r}", details)
    details["kind"] = kind
    reasons.append(f"kind: {kind}")

    missing = [f for f in CORE_FIELDS if not _nonempty(record.get(f))]
    if missing:
        return fail(f"{action}: missing required fields: {missing}", details)
    reasons.append("all core fields present (broken, basis, done, verified, reported)")

    basis = record["authority_basis"]
    if len(basis.strip()) < 4:
        return fail(f"{action}: authority_basis too vague to audit: {basis!r}", details)
    reasons.append(f"authority basis cited: {basis.strip()[:80]}")
    details["authority_basis"] = basis.strip()

    if record.get("protected_gate_touched"):
        approval = record.get("shawn_approval")
        if not _nonempty(approval):
            return fail(
                f"{action}: protected gate touched WITHOUT Shawn's explicit approval — "
                "HARD FAIL. Value never creates authority. Revert and escalate.",
                details,
            )
        reasons.append("protected gate touched WITH Shawn's approval on record")
        details["shawn_approval"] = approval.strip()
    else:
        reasons.append("no protected gate touched")

    if kind == "takeover":
        owner = record.get("original_owner")
        if not _nonempty(owner):
            return fail(f"{action}: takeover without named original_owner", details)
        if record.get("owner_notified") is not True:
            return fail(
                f"{action}: takeover of {owner}'s work without owner_notified=true — "
                "take over stalled work, tell the owner, never silently",
                details,
            )
        stall = record.get("stall_evidence")
        if not _nonempty(stall):
            return fail(
                f"{action}: takeover without stall_evidence — "
                "never take over ACTIVE work; document why the lane was stalled",
                details,
            )
        reasons.append(f"takeover of stalled work owned by {owner}; owner notified")
        details["original_owner"] = owner.strip()

    reasons.append(f"{action}: fix-it-first / take-over record complete — fix stood, report filed")
    return result(True, reasons, details)


def main() -> int:
    parser = argparse.ArgumentParser(description="SN-0575 / SN-DONT-WAIT action-log check")
    parser.add_argument("--record", required=True,
                        help="JSON action record (or @file)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()
    try:
        record = load_record(args.record)
    except Exception as e:
        return emit(fail(f"unparseable record: {e}", {"laws": ["SN-0575"]}), args.json)
    return emit(check(record), args.json)


if __name__ == "__main__":
    sys.exit(main())
