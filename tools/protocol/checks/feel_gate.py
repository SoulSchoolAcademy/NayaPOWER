#!/usr/bin/env python3
"""The Shawn Feel Gate — would this feel like 9.0 in his hands?

Shawn's directive (2026-10-11): "A claimed 9.0 that doesn't feel like 9.0 in
use gets the model revisited." Build it like it's your home.

This check runs before any 9.0+ claim is presented as final. Tests prove the
code works; scorecards prove the math; the Feel Gate proves the human
experience. Feel cannot be fully automated — so this gate is a required
human attestation, mechanically enforced: the builder must answer each feel
question honestly, and a different seat must confirm the attestation.

The six feel questions (each grounded in Shawn's exact words):

  first_read   — "Would a non-technical human understand this on first read?"
                 (Smart Note test: "If Shawn has to ask 'what does that mean?',
                 the output failed.")
  no_surprises — "Does it do what it says, with no unexpected behavior?"
  smooth       — "Is the experience smooth, not janky? Does using it feel good?"
  world_ready  — "Would Shawn be proud to show this to the world?"
                 (The Usefulness Gate: "If you wouldn't give it to the world,
                 don't give it to me.")
  true_words   — "Is every word true? Nothing inflated, nothing manufactured?"
                 ("True words, not fewer words." / "A number without provenance
                 is a lie with formatting.")
  bullseye     — "Is this the most intelligent version of this thing — or just
                 a working version?" (Always the most intelligent thing.)

Input record:
    {
      "deliverable": "<name/description>",
      "claimed_score": 9.2,
      "feel": {
        "first_read":   {"answer": "yes", "note": "<one-line evidence>"},
        "no_surprises": {"answer": "yes", "note": "..."},
        "smooth":       {"answer": "no",  "note": "...", "remediation": "..."},
        "world_ready":  {"answer": "yes", "note": "..."},
        "true_words":   {"answer": "yes", "note": "..."},
        "bullseye":     {"answer": "yes", "note": "..."}
      },
      "builder": "<seat or agent id>",
      "validator": "<different seat or agent id>",
      "validator_confirms": true
    }

Checks:
  1. deliverable present and non-empty.
  2. claimed_score numeric. If >= 9.0, a feel attestation is REQUIRED —
     a 9.0+ claim with no attestation fails outright. Below 9.0 the gate is
     not required, but a present attestation is still validated.
  3. All six feel questions answered with "yes"/"no" and a real evidence
     note (at least 10 chars — a one-word note is not evidence).
  4. Every "no" carries a real remediation (at least 10 chars) — an
     unaddressed "no" fails. (Honest "no + plan" passes; silent "no" does not.)
  5. builder and validator are named identities and DIFFERENT seats.
  6. validator_confirms is true.

Fail-closed: malformed input, missing answers, builder == validator, or an
unconfirmed attestation all fail with a specific reason.

Honesty boundary (stated plainly): this gate enforces the ATTESTATION —
every question answered, every "no" remediated, a different seat confirmed.
It cannot verify sincerity. A builder who lies on all six questions with
plausible notes will pass the structure. Catching that is the validator's
job, and ultimately Shawn's feel test in use. The gate makes dishonesty
require a conspiracy, not a shortcut.

Usage:
    python3 tools/protocol/checks/feel_gate.py \
        --record '{"deliverable": "...", ...}' [--json]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks import emit, fail, load_record, result  # noqa: E402

FEEL_QUESTIONS = [
    ("first_read", "Would a non-technical human understand this on first read?"),
    ("no_surprises", "Does it do what it says, with no unexpected behavior?"),
    ("smooth", "Is the experience smooth, not janky? Does using it feel good?"),
    ("world_ready", "Would Shawn be proud to show this to the world?"),
    ("true_words", "Is every word true? Nothing inflated, nothing manufactured?"),
    ("bullseye", "Is this the most intelligent version of this thing — or just a working version?"),
]
FEEL_KEYS = [k for k, _ in FEEL_QUESTIONS]
FEEL_BAR = 9.0
NOTE_MIN_LEN = 10  # a one-word note is not evidence; one line of it is


def _is_number(x) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def _nonempty_str(x) -> bool:
    return isinstance(x, str) and bool(x.strip())


def _evidence_note(x) -> bool:
    """A note counts as evidence only if it says something real."""
    return _nonempty_str(x) and len(x.strip()) >= NOTE_MIN_LEN


def check(record: dict) -> dict:
    reasons: list[str] = []
    details: dict = {"law": "FEEL-GATE", "bar": FEEL_BAR}

    if not isinstance(record, dict):
        return fail("record must be a JSON object", details)

    deliverable = record.get("deliverable")
    if not _nonempty_str(deliverable):
        return fail("deliverable missing or empty — the gate cannot judge "
                    "an unnamed claim", details)
    details["deliverable"] = deliverable.strip()

    score = record.get("claimed_score")
    if not _is_number(score):
        return fail(f"{deliverable}: claimed_score missing or not numeric — "
                    "the gate cannot judge a scoreless claim", details)
    details["claimed_score"] = score
    requires_feel = score >= FEEL_BAR

    feel = record.get("feel")
    if feel is None:
        if requires_feel:
            return fail(
                f"{deliverable}: claims {score} (>= {FEEL_BAR}) with no feel "
                "attestation — a 9.0+ claim that hasn't passed the Feel Gate "
                "is not a 9.0", details)
        reasons.append(f"score {score} < {FEEL_BAR}: feel attestation not required")
        return result(True, reasons, details)

    if not isinstance(feel, dict):
        return fail(f"{deliverable}: feel attestation must be a JSON object", details)
    reasons.append("feel attestation present")

    # All six questions answered with yes/no + evidence note.
    for key, question in FEEL_QUESTIONS:
        entry = feel.get(key)
        if not isinstance(entry, dict):
            return fail(f"{deliverable}: feel question '{key}' missing — "
                        f"unanswered: {question}", details)
        answer = entry.get("answer")
        if answer not in ("yes", "no"):
            return fail(f"{deliverable}: feel question '{key}' answer must be "
                        "'yes' or 'no', got {answer!r}", details)
        note = entry.get("note")
        if not _evidence_note(note):
            return fail(f"{deliverable}: feel question '{key}' needs a real "
                        f"evidence note (at least {NOTE_MIN_LEN} chars) — an "
                        "answer without evidence is a wish", details)
        if answer == "no":
            remediation = entry.get("remediation")
            if not _evidence_note(remediation):
                return fail(f"{deliverable}: feel question '{key}' answered 'no' "
                            f"with no real remediation (at least {NOTE_MIN_LEN} "
                            "chars) — name the fix or the claim cannot stand",
                            details)
            reasons.append(f"{key}: no — remediation named")
        else:
            reasons.append(f"{key}: yes")
    details["feel_keys"] = FEEL_KEYS

    # Builder attests; a DIFFERENT seat confirms.
    builder = record.get("builder")
    validator = record.get("validator")
    if not _nonempty_str(builder):
        return fail(f"{deliverable}: builder unnamed — anonymous attestation "
                    "is not attestation", details)
    if not _nonempty_str(validator):
        return fail(f"{deliverable}: validator unnamed — the builder cannot "
                    "confirm their own feel", details)
    if builder.strip() == validator.strip():
        return fail(f"{deliverable}: builder and validator are the same seat "
                    f"({builder.strip()}) — feel needs a second pair of eyes", details)
    reasons.append(f"builder {builder.strip()} attested; validator "
                   f"{validator.strip()} is a different seat")

    if record.get("validator_confirms") is not True:
        return fail(f"{deliverable}: validator_confirms is not true — the "
                    "validator has not confirmed the attestation", details)
    reasons.append("validator confirmed the attestation")

    details["builder"] = builder.strip()
    details["validator"] = validator.strip()
    return result(True, reasons, details)


def main() -> int:
    parser = argparse.ArgumentParser(description="The Shawn Feel Gate")
    parser.add_argument("--record", required=True,
                        help="JSON record or @filepath")
    parser.add_argument("--json", action="store_true",
                        help="emit full JSON result")
    args = parser.parse_args()
    try:
        record = load_record(args.record)
    except (ValueError, json.JSONDecodeError, OSError) as exc:
        return emit(fail(f"could not load record: {exc}"), args.json)
    return emit(check(record), args.json)


if __name__ == "__main__":
    sys.exit(main())
