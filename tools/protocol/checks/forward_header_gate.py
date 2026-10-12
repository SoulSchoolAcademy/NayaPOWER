#!/usr/bin/env python3
"""LEARN machine gate — forward-dated header check.

Lesson machine-forced: the 04:40Z LEARN compounding audit (9.2/10, #2154 comment
6117962334) found the "never forward-date headers" lesson NOT COMPOUNDED:
~71 first-line instances of sign-in/out/audit/report headers claiming an
estimated or future timestamp since 00:00Z, 8 of them AFTER the lesson was
filed (including the lesson's own enacter). Self-reports of the slip are
compounding; the behavior is not. No machine was built for it — this is it.

This gate FAILS any lane-feed header whose claimed UTC timestamp is later than
the comment's actual `created_at` plus a 60-second grace. Examples of the
failure shape this gate was built for (verbatim, tonight, comment ID = fixture):

  - "## [Naya 5 | BUILDER | scorecard 2026-10-12 04:38 UTC]" posted
    2026-10-12T04:35:28Z (comment 6117821928) -> header ~152s early -> FAIL
  - "[NAYA 5] SIGN-OUT - gamma lane #1715 - Naya Mu (Human Value) -
    2026-10-12 ~04:52 UTC" posted 2026-10-12T04:42:18Z (comment 6117884246)
    -> header ~582s early -> FAIL
  - "## [NAYA 5 · VALIDATOR | sign-out 2026-10-12 04:52 UTC] Layer 2
    fix-pass #4" posted 2026-10-12T04:40:06Z (comment 6117864326)
    -> header ~714s early -> FAIL

Honest headers pass: "**[NAYA · VALIDATOR | sign-in 2026-10-12 04:49 UTC]**"
posted 2026-10-12T04:48:48Z (comment 6117945693) is 12s early -> within the
60s grace -> PASS. A header that echoes the post's own created_at passes.

Detection rule (precise)
------------------------
Input record: {"claim_text": "<header text>", "posted_at": "<ISO-8601 Z>"}.
`posted_at` is the comment's ground-truth created_at; without it the gate
fails closed (nothing to judge against).

 1. Scan the FIRST FIVE LINES of claim_text for timestamps explicitly marked
    as UTC: "~04:52 UTC", "2026-10-12 04:52 UTC", "04:52Z". An optional "~"
    prefix and optional "YYYY-MM-DD " date prefix are accepted.
 2. A timestamp without a date prefix is anchored to posted_at's calendar
    date (UTC). If the anchored time lands more than 12 hours after
    posted_at, it is read as the previous day (midnight-boundary wrap, so a
    "23:58 UTC" header posted at 00:03Z is not misjudged).
 3. FAIL when header_time > posted_at + 60 seconds. The 60s grace absorbs
    second-level round-up ("04:49 UTC" posted at 04:48:48Z), not minute-level
    estimation.

What this gate does NOT claim (honest limits — D32)
---------------------------------------------------
  - It does NOT catch relative evasions: "shortly", "in a few minutes",
    "EOD", "soon", "almost done" carry no digits and pass silently. A
    deliberately phrased evasion is outside this gate's pattern.
  - It does NOT judge timestamps without an explicit UTC/Z marker: "04:52"
    alone may be any timezone, and this gate refuses to guess.
  - It does NOT scan past the first five lines: future times mentioned
    deeper in the body (e.g. a scheduled meeting) are not header claims.
  - It does NOT judge past-dated timestamps (an event under-reported by
    minutes is a different failure shape, out of scope).
  - It does NOT verify that the claimed minute matches the real event time
    to the second: the 60s grace is deliberate forgiveness, so "04:49 UTC"
    posted 04:48:48Z passes. Minutes of drift are the target, not seconds.
  - A header with NO timestamp at all passes ("gate does not apply") — the
    law punishes forward-dating, not missing headers.

Where this gate fires
---------------------
  1. Worker self-check before posting: run your sign-in/out/audit/report
     header through this gate BEFORE posting it on a lane feed.
         python3 tools/protocol/checks/forward_header_gate.py \\
             --record '{"claim_text": "<your header>", "posted_at": "<created_at>"}'
  2. Dispatcher tick: scan new lane-feed headers with the gate before
     accepting them as lane state; a FAIL means the header is inadmissible
     until corrected (post the real created_at minute).
  3. CI: the regression tests in tests/test_protocol_law_checks.py
     (test_forward_header_gate_*) run on every PR via pytest. The gate has
     no fixed artifact in CI — it fires on header text at the two points
     above.

Usage:
    python3 tools/protocol/checks/forward_header_gate.py \\
        --record '{"claim_text": "...", "posted_at": "2026-10-12T04:35:28Z", "source_ref": "lane-1713:<comment-id>"}' [--json]

Exit codes: 0 = PASS (no forward-dated header, or no UTC timestamp claimed);
1 = FAIL (header claims a future timestamp).
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks import emit, fail, load_record, result  # noqa: E402

LAW = "LEARN-FORWARD-HEADER"
GRACE = timedelta(seconds=60)
HEADER_LINES = 5

# "~04:52 UTC" / "2026-10-12 04:52 UTC" / "04:52Z" / "~03:10Z".
# The explicit UTC/Z marker is REQUIRED: without it the timezone is unknown
# and this gate refuses to guess (documented limit).
HEADER_TS_RE = re.compile(
    r"(?i)(?:^|[^\d:.])"                      # boundary before the time
    r"(~)?"                                   # optional estimate marker
    r"(?:(\d{4}-\d{2}-\d{2})[ T])?"           # optional date prefix
    r"(\d{1,2}):(\d{2})"                      # HH:MM
    r"(?:\s*(UTC|Z|utc))"                     # REQUIRED timezone marker
)

ISO_TS_RE = re.compile(
    r"(\d{4}-\d{2}-\d{2})[T ](\d{2}):(\d{2})(?::(\d{2}))?Z"
)


def parse_posted_at(raw: str) -> datetime:
    """Parse the ground-truth post timestamp. Raises ValueError on garbage."""
    m = ISO_TS_RE.search(raw.strip())
    if not m:
        raise ValueError(f"posted_at is not a Z-suffixed ISO timestamp: {raw!r}")
    return datetime(int(m.group(1)[0:4]), int(m.group(1)[5:7]), int(m.group(1)[8:10]),
                    int(m.group(2)), int(m.group(3)),
                    int(m.group(4) or 0), tzinfo=timezone.utc)


def header_times(line: str, posted: datetime) -> list[tuple[datetime, str]]:
    """All UTC-marked timestamps claimed by one header line, anchored."""
    hits: list[tuple[datetime, str]] = []
    for m in HEADER_TS_RE.finditer(line):
        date_part, hh, mm = m.group(2), int(m.group(3)), int(m.group(4))
        if hh > 23 or mm > 59:
            continue  # not a real time, skip rather than misjudge
        if date_part:
            claimed = datetime(int(date_part[0:4]), int(date_part[5:7]),
                               int(date_part[8:10]), hh, mm, tzinfo=timezone.utc)
        else:
            claimed = posted.replace(hour=hh, minute=mm, second=0, microsecond=0)
            if claimed - posted > timedelta(hours=12):
                # Midnight-boundary wrap: "23:58 UTC" posted at 00:03Z is
                # yesterday's 23:58, not a future claim.
                claimed -= timedelta(days=1)
        hits.append((claimed, m.group(0).strip()[:64]))
    return hits


def check(record: dict) -> dict:
    reasons: list[str] = []
    details: dict = {"law": LAW}

    claim = record.get("claim_text")
    if not isinstance(claim, str) or not claim.strip():
        return fail("claim_text is missing or empty: nothing to judge, fail closed",
                    details)
    if "\x00" in claim:
        return fail("claim_text contains NUL bytes: refusing binary input", details)

    posted_raw = record.get("posted_at")
    if not isinstance(posted_raw, str) or not posted_raw.strip():
        return fail("posted_at is missing or empty: no ground truth to judge "
                    "the header against, fail closed", details)
    try:
        posted = parse_posted_at(posted_raw)
    except ValueError as e:
        return fail(f"posted_at unparseable: {e}", details)

    source = record.get("source_ref")
    if source:
        details["source_ref"] = source

    lines = claim.splitlines()[:HEADER_LINES]
    offenders: list[tuple[int, str, int]] = []
    for lineno, line in enumerate(lines, start=1):
        for claimed, quote in header_times(line, posted):
            drift = int((claimed - posted).total_seconds())
            if drift > int(GRACE.total_seconds()):
                offenders.append((lineno, quote, drift))

    if not offenders:
        reasons.append("no forward-dated UTC timestamp in the header "
                       f"(first {HEADER_LINES} lines): gate does not apply or PASS")
        return result(True, reasons, details)

    details["offenders"] = [
        {"line": n, "quote": q, "drift_seconds": d} for n, q, d in offenders
    ]
    quotes = "; ".join(f"L{n}: {q} (+{d}s)" for n, q, d in offenders)
    return fail(
        f"REJECTED: header claims a future timestamp (the 04:40Z audit's "
        f"NOT-COMPOUNDED finding: ~71 forward-dated headers since 00:00Z). "
        f"A header must state the time of posting, never an estimated future "
        f"time. Offending: {quotes}. Correct the header to the created_at "
        f"minute and re-post.", details)


def main() -> int:
    parser = argparse.ArgumentParser(description="forward-dated header gate")
    parser.add_argument("--record", required=True,
                        help="JSON claim record (or @file) with claim_text + posted_at")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()
    try:
        record = load_record(args.record)
    except Exception as e:
        return emit(fail(f"unparseable record: {e}", {"law": LAW}), args.json)
    return emit(check(record), args.json)


if __name__ == "__main__":
    sys.exit(main())
