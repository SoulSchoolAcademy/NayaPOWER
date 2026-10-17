"""Tests for tools/post_conformance_scan.py — advisory only, no network."""

import os
import sys

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_REPO_ROOT, "tools"))

from post_conformance_scan import (  # noqa: E402
    detect_level,
    render_markdown,
    scan,
)


RECEIPT_POST = """[RECEIPT] wave-191 fold — Naya Verity Narzan

WHO: Naya Verity Narzan
NUTSHELL: re-verified the CV battery at the new tip
WHAT: ran the four CV suites plus the completeness gate
EVIDENCE: tip ba6263870425 via git ls-remote; 54 pytest + 23 node assertions green
SCORE: 9.0/10 — why not 10: B-40 HMAC still Shawn-gated, #2498 still open
CONNECTS: truth-builder run 20261015-0341; live plan STEP -1
NEEDS: different-seat IV on the conformance-scan PR
"""

PULSE_POST = """[PULSE] truth lane heartbeat
WHO: Naya 5
MISSION: TRUTH to 10/10
STATUS: scanning
TRUTH: CV battery green at tip ba6263870425
SCORE: 9.0/10 — holding, B-40 unkeyed seal tracked not fixed
BLOCKER: none
NEXT: ship the conformance scan PR
SOURCE: worktree ~/workspace/truth-verify-ba626387
"""

PROSE_POST = """Quick note — the dispatcher fired w191 at 03:50Z, all five lanes
claimed. Nothing truth-relevant in the claims; the CV battery stays green
at tip ba6263870425. See #2537 for the fold.
"""

BAD_RECEIPT = """[RECEIPT] vague update
just did some stuff, everything is fine, trust me
"""


def test_detect_level_bracket_tag():
    assert detect_level(RECEIPT_POST) == "RECEIPT"
    assert detect_level(PULSE_POST) == "PULSE"


def test_detect_level_labeled_line():
    body = "Level: EVENT\n" + "x\n" * 20
    assert detect_level(body) == "EVENT"


def test_detect_level_none_for_prose():
    assert detect_level(PROSE_POST) is None


def test_detect_level_ignores_late_mention():
    # A level word buried deep is not a declaration.
    body = "\n".join(f"line {i}" for i in range(20)) + "\nreceipt stuff\n"
    assert detect_level(body) is None


def test_scan_grades_only_declared():
    comments = [
        {"id": 1, "user": {"login": "naya"}, "body": RECEIPT_POST},
        {"id": 2, "user": {"login": "naya"}, "body": PROSE_POST},
        {"id": 3, "user": {"login": "naya"}, "body": BAD_RECEIPT},
    ]
    report = scan(comments)
    assert report["scanned"] == 3
    assert report["graded"] == 2
    assert report["skipped_undeclared"] == 1
    assert report["passed"] == 1
    assert report["flagged"] == 1
    assert report["conformance_rate"] == 0.5


def test_scan_empty_window():
    report = scan([])
    assert report["conformance_rate"] is None
    assert report["graded"] == 0


def test_render_markdown_advisory_language():
    report = scan([{"id": 1, "user": {"login": "naya"},
                   "body": RECEIPT_POST}])
    md = render_markdown(report, "o/r", "2537")
    assert "Advisory only" in md
    assert "never fails, never posts, never writes" in md
    assert "100%" in md


def test_render_markdown_names_flagged():
    comments = [{"id": 99, "user": {"login": "someone"}, "body": BAD_RECEIPT}]
    md = render_markdown(scan(comments), "o/r", "2537")
    assert "## Flagged posts" in md
    assert "comment 99" in md
    assert "someone" in md
