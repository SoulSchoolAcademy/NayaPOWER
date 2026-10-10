#!/usr/bin/env python3
"""Amendment-record loader (validator) for Operating Code V2's Amendment Path.

V2 (BRAIN/01-GOVERNANCE/0008-OPERATING-CODE-V2.ai.md, AMENDMENT PATH):

    "Amendments come through Shawn's authority only. Propose the change,
     score it, post the receipt. The loader refuses invalid amendment records."

This file IS that loader. It is a VALIDATOR ONLY: it judges whether an
amendment record is well-formed and authorized. It never amends anything,
never edits any constitutional text, and never flips any ratification
status. Loading a record = checking it, nothing more.

An amendment record is a JSON object with exactly these required fields:

    what_changed           (str, non-empty)  what the proposal changes
    provision              (str, non-empty)  which provision is amended
    proposed_text          (str, non-empty)  the proposed new/replacement text
    score                  (number, 0..10)   the score under score-fill-ship
    scorecard_receipt_ref  (str, non-empty)  where the scorecard receipt lives
                                             (e.g. "#1354 comment 6098808557")
    proposer               (str, non-empty)  who proposes the change
    authorization          (object)          Shawn's authority marker:
                           authorization.authority        == "Shawn"
                           authorization.authorization_ref (str, non-empty)
                           a concrete receipt of his authorization
                           (comment id, directive reference, verbatim
                           directive, ...)

Extra fields are allowed and ignored (the schema may grow). Unknown fields
never cause a refusal.

Refusal is mechanical and FAIL CLOSED: any missing, mis-typed, empty, or
out-of-range field refuses the record. The refusal always carries a NAMED
reason; the loader never raises a raw crash on bad input.

Named refusal reasons:
    MALFORMED_JSON       the input file is not parseable JSON
    NOT_AN_OBJECT        top-level JSON value is not an object
    MISSING_FIELD:<f>    required field <f> is absent
    BAD_TYPE:<f>         field <f> has the wrong type
                         (includes score given as bool or string)
    EMPTY_FIELD:<f>      string field <f> is empty or blank
    SCORE_OUT_OF_RANGE   score is not a number in [0, 10]
    MISSING_AUTHORIZATION no authorization marker on the record at all
    BAD_AUTHORITY        authorization.authority is not Shawn's authority
    BAD_AUTHORIZATION_REF authorization marker carries no concrete receipt

Usage:
    python3 tools/amendment_loader.py <record.json>
        Exit 0: ACCEPT. Exit 1: REFUSE (named reason printed).
        Exit 2: usage / input error (unreadable file, malformed JSON).

    python3 tools/amendment_loader.py --json <record.json>
        Print a machine verdict {"accepted": ..., "reason": ..., "detail": ...}.

Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

V2_SOURCE = "BRAIN/01-GOVERNANCE/0008-OPERATING-CODE-V2.ai.md (AMENDMENT PATH)"

# Required content fields, in the order they are checked. The authorization
# marker is validated separately after these (absence of the whole marker is
# its own named reason, per V2: amendments come through his authority only).
REQUIRED_FIELDS = (
    "what_changed",
    "provision",
    "proposed_text",
    "score",
    "scorecard_receipt_ref",
    "proposer",
)

# Named refusal reasons.
MALFORMED_JSON = "MALFORMED_JSON"
NOT_AN_OBJECT = "NOT_AN_OBJECT"
MISSING_AUTHORIZATION = "MISSING_AUTHORIZATION"
BAD_AUTHORITY = "BAD_AUTHORITY"
BAD_AUTHORIZATION_REF = "BAD_AUTHORIZATION_REF"
SCORE_OUT_OF_RANGE = "SCORE_OUT_OF_RANGE"


def _refuse(reason: str, detail: str = "") -> "Verdict":
    return Verdict(accepted=False, reason=reason, detail=detail)


class Verdict:
    """The outcome of validating one amendment record. Never raises."""

    __slots__ = ("accepted", "reason", "detail")

    def __init__(self, accepted: bool, reason: str | None = None, detail: str = ""):
        self.accepted = accepted
        self.reason = reason
        self.detail = detail

    def to_dict(self) -> dict:
        return {"accepted": self.accepted, "reason": self.reason, "detail": self.detail}

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"Verdict(accepted={self.accepted!r}, reason={self.reason!r})"


def _is_nonempty_str(value: object) -> bool:
    return isinstance(value, str) and value.strip() != ""


def _check_authorization(record: dict) -> "Verdict | None":
    """Validate the authorization marker. Returns None when it passes."""
    auth = record.get("authorization")
    if auth is None:
        return _refuse(
            MISSING_AUTHORIZATION,
            "V2 Amendment Path: amendments come through Shawn's authority only; "
            "the record carries no authorization marker.",
        )
    if not isinstance(auth, dict):
        return _refuse(
            f"BAD_TYPE:authorization",
            "authorization must be an object with authority + authorization_ref.",
        )
    authority = auth.get("authority")
    if not _is_nonempty_str(authority) or authority.strip().lower() != "shawn":
        return _refuse(
            BAD_AUTHORITY,
            "V2 Amendment Path: amendments come through Shawn's authority only; "
            f"authorization.authority is {authority!r}, not Shawn.",
        )
    ref = auth.get("authorization_ref")
    if not _is_nonempty_str(ref):
        return _refuse(
            BAD_AUTHORIZATION_REF,
            "authorization marker names Shawn but carries no concrete receipt "
            "(authorization_ref must be a non-empty reference to his authorization).",
        )
    return None


def validate(record: object) -> Verdict:
    """Validate an amendment record against V2's Amendment Path.

    Never raises on invalid content: every invalid record yields a Verdict
    with accepted=False and a named reason. Programmer errors (e.g. passing
    a file path instead of parsed content) are still refused mechanically,
    not with a traceback.
    """
    if not isinstance(record, dict):
        return _refuse(
            NOT_AN_OBJECT,
            "an amendment record must be a JSON object at the top level.",
        )

    for field in REQUIRED_FIELDS:
        if field not in record:
            return _refuse(
                f"MISSING_FIELD:{field}",
                f"required field {field!r} is absent.",
            )

    for field in ("what_changed", "provision", "proposed_text",
                  "scorecard_receipt_ref", "proposer"):
        value = record[field]
        if not isinstance(value, str):
            return _refuse(
                f"BAD_TYPE:{field}",
                f"field {field!r} must be a string, got {type(value).__name__}.",
            )
        if value.strip() == "":
            return _refuse(
                f"EMPTY_FIELD:{field}",
                f"field {field!r} must not be empty or blank.",
            )

    score = record["score"]
    # bool is a subclass of int; True/False are not scores.
    if isinstance(score, bool) or not isinstance(score, (int, float)):
        return _refuse(
            "BAD_TYPE:score",
            f"field 'score' must be a number in [0, 10], got {type(score).__name__}.",
        )
    if not 0 <= score <= 10:
        return _refuse(
            SCORE_OUT_OF_RANGE,
            f"field 'score' must be in [0, 10] (score-fill-ship scale), got {score!r}.",
        )

    auth_verdict = _check_authorization(record)
    if auth_verdict is not None:
        return auth_verdict

    return Verdict(accepted=True)


class LoaderError(Exception):
    """Input-level failure (unreadable file, malformed JSON). Carries a named reason."""

    def __init__(self, reason: str, detail: str = ""):
        super().__init__(detail or reason)
        self.reason = reason
        self.detail = detail


def load_record(path: str | Path) -> dict:
    """Read and parse an amendment record file. Raises LoaderError, never a raw crash."""
    path = Path(path)
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise LoaderError("UNREADABLE_FILE", f"cannot read {path}: {exc}") from exc
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise LoaderError(
            MALFORMED_JSON, f"{path} is not parseable JSON: {exc}"
        ) from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate an amendment record against Operating Code V2's Amendment Path."
    )
    parser.add_argument("record", help="path to the amendment record JSON file")
    parser.add_argument(
        "--json", action="store_true",
        help="print the verdict as JSON instead of a human line",
    )
    args = parser.parse_args(argv)

    try:
        record = load_record(args.record)
    except LoaderError as exc:
        verdict = _refuse(exc.reason, exc.detail)
        return _emit(verdict, as_json=args.json, exit_code=2)

    verdict = validate(record)
    return _emit(verdict, as_json=args.json, exit_code=0 if verdict.accepted else 1)


def _emit(verdict: Verdict, *, as_json: bool, exit_code: int) -> int:
    if as_json:
        print(json.dumps(verdict.to_dict(), indent=2))
    elif verdict.accepted:
        print("ACCEPT: amendment record is valid under V2's Amendment Path.")
    else:
        line = f"REFUSE [{verdict.reason}]"
        if verdict.detail:
            line += f": {verdict.detail}"
        print(line)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
