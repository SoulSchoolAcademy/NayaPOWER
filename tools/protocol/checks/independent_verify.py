#!/usr/bin/env python3
"""SN-IV-DEFAULT — Independent Verification by Default.

"A defended 7.5 beats a wished 9.0."

Any scorecard claiming 9.0 or higher must carry a validator receipt from a
DIFFERENT seat — stating what was checked, an independent score, and a pass
verdict — or the claim fails the gate. Below 9.0, triple self-validation
suffices (see builder_scorer_loop); this gate does not apply there.

The validator is the seat that did NOT build the work. Same-seat validation
is theater: it fails. A validator who scores below 9.0 disagrees with the
claim and blocks it — the builder fixes and re-verifies, or lowers the claim.

This is the complement to builder_scorer_loop.py: that check verifies the
builder's three-round receipt; this check verifies a different seat looked.

Input record:
    {
      "claim": "<what is claimed — PR, branch, artifact>",
      "claimed_score": 9.2,
      "builder": "<seat that built it>",
      "validator": "<a DIFFERENT seat>",
      "validator_checked": ["<what the validator actually checked>", ...],
      "validator_score": 9.0,
      "validator_verdict": "PASS",
      "validator_evidence": "<receipt — tests re-run, diff reviewed, ...>"
    }

Checks:
  1. Record is a dict; claim named; claimed_score is a finite number in [0, 10].
  2. claimed_score < 9.0 -> PASS (gate not applicable; self-validation suffices).
  3. claimed_score >= 9.0 requires ALL of:
     a. validator named and non-empty — anonymous validation is not validation.
     b. validator != builder (normalized case/whitespace-insensitive) —
        you cannot verify yourself.
     c. validator_checked is a non-empty list of non-empty strings —
        the validator must say what they checked.
     d. validator_score is a finite number in [0, 10].
     e. validator_verdict == "PASS" — any other verdict blocks the claim.
     f. validator_score >= 9.0 — a validator scoring below 9.0 disagrees;
        the 9.0+ claim is not sustained.

Fail-closed: malformed input fails with a specific reason.
The check verifies compliance; it never grants authority.

Honest bounds (plain English): this gate verifies the RECEIPT's shape —
a named different seat, a non-empty checked-list, an independent score,
and a pass verdict. What it cannot catch: a validator who colludes with
the builder (social, not mechanical); seat-identity spoofing via homoglyphs
or near-identical display names (caught by seat-tagged identity, not string
comparison); a validator who checked the wrong things thoroughly. The gate
makes theater structurally harder: a 9.0+ claim with no independent eyes on
it fails automatically, every time.

Usage:
    python3 tools/protocol/checks/independent_verify.py \
        --record '{"claim": "...", "claimed_score": 9.2, ...}' [--json]
"""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks import emit, fail, load_record, result  # noqa: E402

IV_BAR = 9.0


def _is_number(x) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def _finite_score(x) -> bool:
    return _is_number(x) and math.isfinite(float(x)) and 0.0 <= float(x) <= 10.0


def _norm_seat(s) -> str:
    # Remove ALL whitespace and lowercase: "NAYA 5", "naya  5", "naya5"
    # are the same seat. A validator cannot dodge the same-seat rule
    # with a space.
    return "".join(str(s).split()).lower()


def check(record: dict) -> dict:
    reasons: list[str] = []
    details: dict = {"law": "SN-IV-DEFAULT"}

    if not isinstance(record, dict):
        return fail("record must be a JSON object — fail-closed", details)

    claim = record.get("claim")
    if not claim or not str(claim).strip():
        return fail(
            "claim unnamed — a validator receipt for 'something' is not a receipt",
            details,
        )
    claim = str(claim).strip()
    details["claim"] = claim

    claimed = record.get("claimed_score")
    if not _finite_score(claimed):
        return fail(
            f"{claim}: claimed_score must be a finite number in [0, 10], "
            f"got {claimed!r} — no number, no claim",
            details,
        )
    claimed = float(claimed)
    details["claimed_score"] = claimed

    builder = record.get("builder")
    if not builder or not str(builder).strip():
        return fail(
            f"{claim}: builder unnamed — anonymous work carries no receipt",
            details,
        )
    builder = str(builder).strip()
    details["builder"] = builder

    if claimed < IV_BAR:
        reasons.append(
            f"claimed {claimed} < {IV_BAR}: gate not applicable — "
            "triple self-validation suffices below 9.0"
        )
        reasons.append(f"{claim}: independent-verification gate PASS (not required)")
        return result(True, reasons, details)

    # --- 9.0+ claim: validator receipt is mandatory ---
    reasons.append(f"claimed {claimed} >= {IV_BAR}: independent receipt required")

    validator = record.get("validator")
    if not validator or not str(validator).strip():
        return fail(
            f"{claim}: claims {claimed} with no validator receipt — "
            "a wished 9.0 is not a defended 9.0",
            details,
        )
    validator = str(validator).strip()
    details["validator"] = validator

    if _norm_seat(validator) == _norm_seat(builder):
        return fail(
            f"{claim}: validator {validator!r} is the builder — "
            "you cannot verify yourself",
            details,
        )
    reasons.append(f"validator {validator!r} is a different seat from builder {builder!r}")

    checked = record.get("validator_checked")
    if not isinstance(checked, list) or not checked:
        return fail(
            f"{claim}: validator_checked missing or empty — "
            "the validator must say what they checked",
            details,
        )
    bad_items = [c for c in checked if not isinstance(c, str) or not c.strip()]
    if bad_items:
        return fail(
            f"{claim}: validator_checked must be a non-empty list of "
            "non-empty strings — what did they actually check?",
            details,
        )
    reasons.append(f"validator checked {len(checked)} item(s)")
    details["validator_checked"] = [c.strip() for c in checked]

    vscore = record.get("validator_score")
    if not _finite_score(vscore):
        return fail(
            f"{claim}: validator_score must be a finite number in [0, 10], "
            f"got {vscore!r} — the validator must score independently",
            details,
        )
    vscore = float(vscore)
    details["validator_score"] = vscore

    verdict = record.get("validator_verdict")
    if verdict != "PASS":
        return fail(
            f"{claim}: validator verdict is {verdict!r}, not PASS — "
            "the claim is blocked until the validator passes it",
            details,
        )
    reasons.append("validator verdict: PASS")

    if vscore < IV_BAR:
        return fail(
            f"{claim}: validator scored {vscore} < {IV_BAR} — "
            "the validator disagrees with the 9.0+ claim; "
            "fix and re-verify, or lower the claim",
            details,
        )
    reasons.append(f"validator independent score {vscore} sustains the claim")

    evidence = record.get("validator_evidence")
    if evidence and str(evidence).strip():
        details["validator_evidence"] = str(evidence).strip()
        reasons.append("validator evidence attached")

    reasons.append(f"{claim}: 9.0+ claim independently verified — gate PASS")
    return result(True, reasons, details)


def main() -> int:
    parser = argparse.ArgumentParser(description="SN-IV-DEFAULT independent verification gate")
    parser.add_argument("--record", required=True,
                        help="JSON claim record (or @file)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()
    try:
        record = load_record(args.record)
    except Exception as e:
        return emit(fail(f"unparseable record: {e}", {"law": "SN-IV-DEFAULT"}), args.json)
    return emit(check(record), args.json)


if __name__ == "__main__":
    sys.exit(main())
