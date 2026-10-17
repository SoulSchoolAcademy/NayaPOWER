"""Regression tests: the merge-consensus gate's 12-lane seat forms.

Gap-t1442 follow-up (2026-10-12): both 9.0 scorecards on PR #2453 carried
'[LANE N · Naya Name]' tags the gate's seat regex could not parse, so
scorer_seat stayed None and the 2-seat bar could never flip green. The gate's
seat model predated the 12-lane system. These tests pin the fix: both lane
tag forms parse, the legacy 'Naya [1-5]' form still parses, and the
author-seat declaration check runs at brief time via --self-test-pr-body.
"""
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from check_merge_consensus import (  # noqa: E402
    author_seat_of,
    seat_of,
)

GATE = str(ROOT / "tools" / "check_merge_consensus.py")

# ---------------------------------------------------------------------------
# seat_of: scorecard tags
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "text,expected",
    [
        # The two 12-lane tag forms (gap-t1442).
        ("## SCORECARD [LANE 1 · Naya Verity] head: abc123", "Lane 1 (Naya Verity)"),
        ("## SCORECARD [LANE 8 · Naya Sentinel] verdict: 9.0/10", "Lane 8 (Naya Sentinel)"),
        ("Honest scorecard: 9.4/10\nSeat: Lane 12 (Naya Herald)", "Lane 12 (Naya Herald)"),
        # Separator variants seen / tolerated in the wild.
        ("[LANE 3 - Naya Judge] APPROVED", "Lane 3 (Naya Judge)"),
        ("[LANE 5 — Naya Seeker] verdict: 9.2/10", "Lane 5 (Naya Seeker)"),
        ("[lane 9 / naya sage] 9.0/10", "Lane 9 (Naya Sage)"),
        # Lane boundaries: 1 and 12 are valid; 0 and 13 are not.
        ("[LANE 1 · Naya Verity]", "Lane 1 (Naya Verity)"),
        ("[LANE 12 · Naya Herald]", "Lane 12 (Naya Herald)"),
        # Legacy forms still parse exactly as before.
        ("Seat: Naya 5", "Naya 5"),
        ("scorecard by Naya 1, 9.0/10", "Naya 1"),
        ("Seat: Naya Epsilon", "Naya Epsilon"),
        ("reviewed by naya kappa", "Naya Kappa"),
    ],
)
def test_seat_of_parses_lane_and_legacy_forms(text, expected):
    assert seat_of(text) == expected


@pytest.mark.parametrize(
    "text",
    [
        "[LANE 0 · Naya Verity]",    # lane number out of range
        "[LANE 13 · Naya Herald]",   # lane number out of range
        "[LANE 8 · Naya Nova]",      # unknown lane-agent name
        "[LANE · Naya Sentinel]",    # missing lane number
        "Seat: Naya 8",              # legacy numeric only goes 1-5
        "no seat tag here at all",
    ],
)
def test_seat_of_rejects_bad_forms(text):
    assert seat_of(text) is None


def test_lane_tag_does_not_shadow_numeric_seat():
    """When both a legacy numeric tag and a lane tag appear, the legacy
    form keeps its existing precedence (first match wins, as before)."""
    assert seat_of("Seat: Naya 2 — [LANE 8 · Naya Sentinel]") == "Naya 2"


# ---------------------------------------------------------------------------
# author_seat_of: the declaration check
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "body,expected",
    [
        ("Seat: Naya 5\n\nBody text.", "Naya 5"),
        ("Seat: Naya Epsilon\n\nBody text.", "Naya Epsilon"),
        ("Seat: Lane 8 (Naya Sentinel)\n\nBody text.", "Lane 8 (Naya Sentinel)"),
        ("seat: lane 1 (naya verity)", "Lane 1 (Naya Verity)"),
        # Incidental mentions still do not count as declarations.
        ("The Naya 1 judge will review this.", None),
        ("[LANE 8 · Naya Sentinel] built this", None),
    ],
)
def test_author_seat_of(body, expected):
    assert author_seat_of(body) == expected


def test_author_declaration_still_rejects_first_incidental_mention():
    """The #2373 dogfood case: a body that mentions Naya 1 in prose before
    declaring Seat: Naya 5 attributes authorship to Naya 5, not Naya 1."""
    body = "the Naya 1 judge must score this.\n\nSeat: Naya 5"
    assert author_seat_of(body) == "Naya 5"


# ---------------------------------------------------------------------------
# --self-test-pr-body: the brief-time declaration check
# ---------------------------------------------------------------------------


def _run_self_test_pr_body(body_text):
    draft = ROOT / "tmp-self-test-pr-body.md"
    try:
        draft.write_text(body_text, encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, GATE, "--self-test-pr-body", str(draft)],
            capture_output=True, text=True, timeout=30,
        )
    finally:
        draft.unlink(missing_ok=True)
    return proc


def test_self_test_pr_body_accepts_lane_declaration():
    proc = _run_self_test_pr_body("Seat: Lane 8 (Naya Sentinel)\n\nWork done.")
    assert proc.returncode == 0
    assert "AUTHOR-SEAT SELF-TEST PASSED" in proc.stdout
    assert "Lane 8 (Naya Sentinel)" in proc.stdout


def test_self_test_pr_body_rejects_missing_declaration():
    proc = _run_self_test_pr_body("Some work happened.\n\nNo declaration.")
    assert proc.returncode == 1
    assert "AUTHOR-SEAT SELF-TEST FAILED" in proc.stdout
    assert "Seat: Lane 8 (Naya Sentinel)" in proc.stdout


def test_self_test_pr_body_usage_error():
    proc = subprocess.run(
        [sys.executable, GATE, "--self-test-pr-body"],
        capture_output=True, text=True, timeout=30,
    )
    assert proc.returncode == 2
    assert "usage" in proc.stderr
