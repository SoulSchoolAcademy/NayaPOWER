#!/usr/bin/env python3
"""PR-body rung of the merge receipt gate (Lane 9, t922 rebuild).

Verifies that a PR body's SCORECARD-RECEIPT-PIN block pins the EXACT merge
head SHA. Blocks four failure modes:
  MISSING  - no receipt-pin block in the PR body
  TAMPERED - block present but fields malformed or empty
  STALE    - pinned SHA != the expected merge head SHA
  FUTURE   - decided_at is dated later than now (+skew): the receipt cannot
             have been posted yet, so it certifies nothing (Judge wave-216)

Usage:
    python3 tools/check_scorecard_receipt_pin.py <expected-head-sha> [pr-body-file]
    cat pr-body.md | python3 tools/check_scorecard_receipt_pin.py <expected-head-sha>
    python3 tools/check_scorecard_receipt_pin.py <expected-head-sha> pr-body.md \
        --pr-state-out /tmp/pr-state.json

Exit 0 + JSON verdict on pass, exit 1 + JSON verdict on fail, exit 2 on
usage/input errors. With --pr-state-out <path> on a PASS, also writes the
gate-consumable pr_state JSON ({"head_sha": ..., "receipt_pin": {...}})
so the P12 rung (tools/auto_merge_gate.py --p12-only) can re-verify the pin.

Receipt-pin block format (case-sensitive header, key: value lines, blank line
or next '##' header ends the block):

    ## SCORECARD-RECEIPT-PIN
    merge_head_sha: <40 lowercase hex chars>
    decided_by: <seat name>
    decided_at: <ISO-8601 timestamp>
    board_comment_id: <digits>

Mechanism pair: this script is the PR-body rung; the gate-side check is P12
in tools/auto_merge_gate.py (may_auto_merge). Wiring documented in
docs/merge-receipt-gate-wiring.md.

NAMED HOLE (2026-10-11): no cryptographic signature verification of the pin -
tamper detection here is field-integrity only (40-hex shape, non-empty
attribution, parseable timestamp, decided_at not future-dated since 2026-10-16).
A signing key is a protected-ops decision and belongs to Shawn's gate.
STILL OPEN: CI wiring as a blocking check + Shawn's required-check click -
readiness is documented, the click is his.
"""

import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone

BLOCK_HEADER = "## SCORECARD-RECEIPT-PIN"
FULL_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
REQUIRED_KEYS = ("merge_head_sha", "decided_by", "decided_at", "board_comment_id")

# Judge wave-216 (2026-10-16, L300/L316 class): a receipt timestamped in the
# future passed the mechanical gate on shape alone (#2682's future-dated
# receipt). Temporal honesty now fails closed. Naive timestamps are read as
# UTC; a small skew absorbs CI clock drift without opening the hole.
# Overridable at runtime for CI clock weirdness: RECEIPT_PIN_FUTURE_SKEW_SECONDS.
def _skew_seconds():
    try:
        return max(0, int(os.environ.get("RECEIPT_PIN_FUTURE_SKEW_SECONDS", "300")))
    except ValueError:
        return 300


FUTURE_SKEW_SECONDS = _skew_seconds()


def _extract_pin_block(body):
    """Return the dict of key/value lines under the first pin header, or None."""
    lines = body.splitlines()
    in_block = False
    fields = {}
    for line in lines:
        stripped = line.strip()
        if not in_block:
            if stripped == BLOCK_HEADER:
                in_block = True
            continue
        if stripped == "" or stripped.startswith("## "):
            break
        if ":" in stripped:
            key, _, value = stripped.partition(":")
            fields[key.strip()] = value.strip()
    return fields if in_block else None


def _parse_ts(value):
    try:
        dt = datetime.fromisoformat(value)
        return dt
    except (ValueError, TypeError):
        return None


def _is_future_dated(dt, now, skew_seconds=FUTURE_SKEW_SECONDS):
    """True when the receipt claims a decision later than now (+skew).

    A future-dated decided_at cannot be a real posted receipt — temporal
    dishonesty fails closed (Judge wave-216, L300/L316 class).
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt > now + timedelta(seconds=skew_seconds)


def check_pin(body, expected_head_sha):
    """Return (verdict, reason). verdict is 'PASS' or a failure class."""
    if not isinstance(expected_head_sha, str) or not FULL_SHA_RE.match(expected_head_sha):
        return "INPUT_ERROR", "expected-head-sha must be 40 lowercase hex chars"
    fields = _extract_pin_block(body or "")
    if fields is None:
        return "MISSING", "no '## SCORECARD-RECEIPT-PIN' block in PR body"
    for key in REQUIRED_KEYS:
        if not fields.get(key):
            return "TAMPERED", "pin block missing or empty field '%s'" % key
    pinned = fields["merge_head_sha"]
    if not FULL_SHA_RE.match(pinned):
        return "TAMPERED", "merge_head_sha malformed (must be 40 lowercase hex chars)"
    if pinned != expected_head_sha:
        return "STALE", (
            "pinned SHA %s... != expected head %s... (head moved - re-score on the current head)"
            % (pinned[:12], expected_head_sha[:12])
        )
    decided = _parse_ts(fields["decided_at"])
    if decided is None:
        return "TAMPERED", "decided_at not a parseable ISO-8601 timestamp"
    if _is_future_dated(decided, datetime.now(timezone.utc)):
        return "FUTURE", (
            "decided_at %s is later than now (+%ds skew) - the receipt cannot "
            "have been posted yet (temporal dishonesty fails closed)"
            % (fields["decided_at"], FUTURE_SKEW_SECONDS)
        )
    if not re.fullmatch(r"\d+", fields["board_comment_id"]):
        return "TAMPERED", "board_comment_id must be digits (receipt must be posted)"
    return "PASS", "pin valid: receipt certifies exact merge head %s" % expected_head_sha


def main(argv):
    pr_state_out = None
    args = list(argv[1:])
    if "--pr-state-out" in args:
        idx = args.index("--pr-state-out")
        if idx != len(args) - 2:
            print(
                "usage: python3 tools/check_scorecard_receipt_pin.py "
                "<expected-head-sha> [pr-body-file] [--pr-state-out <path>]",
                file=sys.stderr,
            )
            return 2
        pr_state_out = args.pop(idx + 1)
        args.pop(idx)
    if len(args) not in (1, 2):
        print(
            "usage: python3 tools/check_scorecard_receipt_pin.py "
            "<expected-head-sha> [pr-body-file] [--pr-state-out <path>]",
            file=sys.stderr,
        )
        return 2
    expected = args[0]
    try:
        if len(args) == 2:
            with open(args[1], "r", encoding="utf-8") as fh:
                body = fh.read()
        else:
            body = sys.stdin.read()
    except OSError as exc:
        print(json.dumps({"verdict": "INPUT_ERROR", "reason": str(exc)}))
        return 2
    verdict, reason = check_pin(body, expected)
    print(json.dumps({"verdict": verdict, "reason": reason}))
    if verdict == "PASS" and pr_state_out:
        fields = _extract_pin_block(body or "")
        pr_state = {
            "head_sha": expected,
            "receipt_pin": {"merge_head_sha": fields["merge_head_sha"]},
        }
        try:
            with open(pr_state_out, "w", encoding="utf-8") as fh:
                json.dump(pr_state, fh, indent=2)
        except OSError as exc:
            print(json.dumps({"verdict": "INPUT_ERROR", "reason": str(exc)}))
            return 2
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
