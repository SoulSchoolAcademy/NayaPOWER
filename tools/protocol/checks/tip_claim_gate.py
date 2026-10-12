#!/usr/bin/env python3
"""SN-0493 companion gate — tip-claim evidence check (Law-12-style mechanical gate).

Lesson machine-forced: the 22:17Z lesson "API-confirm the tip; `git ls-remote`
lies on this VM" (Iota's 02:16Z cold-successor battery, 4/5 reproduce: probe 3
POSTED "TIP MOVED" on ls-remote authority because no canonical record
prescribed otherwise — the lesson was habit-held, not machine-held).

This gate REJECTS any tip-moved/tip-stable claim whose only cited evidence
is `git ls-remote` on this VM. The claim must name its API confirmation
(e.g. "API-confirmed via GET /repos/.../git/ref/heads/main").

What counts as a claim
----------------------
A non-negated line that BOTH asserts a tip verdict (moved/stable/unmoved/
unchanged/has moved/redetermined) AND cites `ls-remote`. The gate fires at
the claim level (whole artifact text): it FAILS only when at least one such
line exists AND no line anywhere in the claim names an API confirmation.

What counts as API confirmation (any one, anywhere in the claim text)
---------------------------------------------------------------------
  - "API-confirmed" / "API confirmed"
  - "Git Data API"
  - "api.github.com"
  - a ref endpoint path: /git/ref/heads/ or /git/refs/heads/
  - "gh-api GET" (this VM's API read path)

What the gate does NOT do
-------------------------
  - It does not resolve the tip itself. Tip resolution is tip_freshness.py's
    job; this gate judges the CLAIM's cited evidence, not the SHA.
  - It does not reject claims that never make a tip verdict, or that cite
    ls-remote only historically ("ls-remote lies on this VM" is context,
    not a verdict).
  - It does not exempt on vague authority ("server truth", "verified"):
    the claim must NAME the API confirmation.
  - Bare SHA assertions without a moved/stable verdict word are out of
    scope (documented boundary, not an oversight).
  - Heuristic boundaries (honest limits): the verdict word must sit within
    ~40 chars after "tip" on the same line as the ls-remote citation, and
    the verdict is detected in tip-before-verdict order ("TIP MOVED",
    "tip unmoved"). A deliberately long-winded or reversed phrasing can
    evade the pattern — the gate targets the evidenced failure shapes
    (the compact claims workers actually post), not adversarial prose.

Where this gate fires
---------------------
  1. Worker self-check before posting: run your sign-in/out text through
     this gate BEFORE claiming the tip moved (or didn't) on a lane feed.
         python3 tools/protocol/checks/tip_claim_gate.py \
             --record '{"claim_text": "<your tip claim>"}'
  2. Dispatcher tick: scan new lane-feed tip claims with the gate before
     accepting them as lane state; a FAIL means the claim is inadmissible
     until re-resolved via the API.
  3. CI: the regression tests in tests/test_protocol_law_checks.py
     (test_tip_claim_gate_*) run on every PR via kernel-tests.yml's
     `python -m pytest -q`. The gate has no fixed artifact in CI — it
     fires on claim text at the two points above.

Usage:
    python3 tools/protocol/checks/tip_claim_gate.py \
        --record '{"claim_text": "...", "source_ref": "lane-1713:<comment-id>"}' [--json]

Exit codes: 0 = PASS (claim names API confirmation, or makes no
ls-remote-backed tip verdict); 1 = FAIL (ls-remote-only tip claim).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks import emit, fail, load_record, result  # noqa: E402

LAW = "SN-0493"

# A tip verdict: the word "tip" followed (within ~40 chars) by a verdict word.
# "moved?" covers both "moved" and the common "did not move" phrasing —
# a stability claim is a verdict too ("tip did not move" asserts stability).
TIP_VERDICT_RE = re.compile(
    r"(?i)\btip\b.{0,40}\b(moved?|stable|unmoved|unchanged|movement|has\s+moved|redetermined)\b"
)
LS_REMOTE_RE = re.compile(r"(?i)\bls-remote\b")

# Markers that name an API confirmation. The claim must name one.
API_CONFIRM_RES = [
    re.compile(r"(?i)\bapi[- ]?confirmed\b"),
    re.compile(r"(?i)\bgit\s+data\s+api\b"),
    re.compile(r"(?i)\bapi\.github\.com\b"),
    re.compile(r"(?i)/git/refs?/heads/"),
    re.compile(r"(?i)\bgh-api\s+GET\b"),
]

# Clause-scoped negation (mirrors tools/learning/error_signal_loop.py):
# a negated mention is an honest denial, not a violation.
NEGATION_RE = re.compile(
    r"(?i)\b(no|not|never|none|without|zero|"
    r"don'?t|doesn'?t|didn'?t|can'?t|cannot|won'?t|"
    r"isn'?t|aren'?t|wasn'?t|weren'?t|shouldn'?t|"
    r"wouldn'?t|couldn'?t)\b")
_CLAUSE_SPLIT_RE = re.compile(r"[;,.:!?()\[\]]")


def negated_before_match(line: str, match_start: int, window: int = 40) -> bool:
    """True when a negation word scopes over the match: the last clause of
    the `window` characters before the match contains a negation word."""
    before = line[max(0, match_start - window):match_start]
    clause = _CLAUSE_SPLIT_RE.split(before)[-1]
    return NEGATION_RE.search(clause) is not None


def verdict_lines(lines: list[str]) -> list[tuple[int, str]]:
    """Lines making an ls-remote-backed tip verdict (non-negated).

    Returns [(line_no, quote), ...].
    """
    hits: list[tuple[int, str]] = []
    for lineno, line in enumerate(lines, start=1):
        vm = TIP_VERDICT_RE.search(line)
        if not vm:
            continue
        if not LS_REMOTE_RE.search(line):
            continue
        if negated_before_match(line, vm.start()):
            continue
        hits.append((lineno, line.strip()[:240]))
    return hits


def names_api_confirmation(lines: list[str]) -> bool:
    """True when any line names an API confirmation for the tip."""
    return any(p.search(line) for line in lines for p in API_CONFIRM_RES)


def check(record: dict) -> dict:
    reasons: list[str] = []
    details: dict = {"law": LAW}

    claim = record.get("claim_text")
    if not isinstance(claim, str) or not claim.strip():
        return fail("claim_text is missing or empty: nothing to judge, fail closed",
                    details)
    if "\x00" in claim:
        return fail("claim_text contains NUL bytes: refusing binary input", details)

    lines = claim.splitlines()
    source = record.get("source_ref")
    if source:
        details["source_ref"] = source

    verdicts = verdict_lines(lines)
    if not verdicts:
        reasons.append("no ls-remote-backed tip verdict found: gate does not apply")
        return result(True, reasons, details)

    details["verdict_lines"] = [{"line": n, "quote": q} for n, q in verdicts]

    if names_api_confirmation(lines):
        reasons.append(
            "claim cites ls-remote for a tip verdict but ALSO names an API "
            "confirmation: admissible")
        return result(True, reasons, details)

    quotes = "; ".join(f"L{n}: {q}" for n, q in verdicts)
    return fail(
        f"REJECTED: tip verdict cites only `git ls-remote` on this VM "
        f"(ls-remote lies here — 22:17Z lesson). The claim must name its API "
        f"confirmation (e.g. 'API-confirmed via GET .../git/ref/heads/main'). "
        f"Offending: {quotes}",
        details,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="SN-0493 tip-claim evidence gate")
    parser.add_argument("--record", required=True,
                        help="JSON claim record (or @file) with claim_text")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()
    try:
        record = load_record(args.record)
    except Exception as e:
        return emit(fail(f"unparseable record: {e}", {"law": LAW}), args.json)
    return emit(check(record), args.json)


if __name__ == "__main__":
    sys.exit(main())
