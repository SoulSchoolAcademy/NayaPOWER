"""Regression tests: scorecard-leg blockquote hardening (mixed form).

VERIFY's different-seat scorecard of PR #2877 (9.2 HOLD, issue #2793
scorecard comment) proved the review leg was cured by #2877 but the
SCORECARD leg was not: `_looks_like_scorecard` never stripped blockquotes
and the Requirement-2 scan attributed the seat on unstripped text, so a
comment that QUOTES another seat's scorecard (score + seat inside `>`
lines) and adds one plain `head:` line naming the exact head satisfied
the scorecard requirement as if the quoted seat had scored this head.
The unified paperwork gate's `_scorecard_for_current_head` read the same
unstripped body through the consensus helpers — same mixed-form exposure
on the live paperwork surface.

These tests pin the cure on both gates: blockquote paragraphs are
stripped before the scorecard analysis, seat attribution runs on the
stripped text, and a genuine plain-text scorecard — including one posted
beside a quote — still counts.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

from check_merge_consensus import _looks_like_scorecard, _strip_blockquotes, seat_of
import check_unified_pr_paperwork as unified

HEAD = "3e35516787f4b1b2bf9793e9a685ad056a25265e"
AUTHOR = "Naya Resolve"

MIXED = (
    "> ## SCORECARD — Naya Clarity\n"
    "> Honest scorecard: 9.6/10\n"
    "> [NAYA CLARITY]\n"
    f"head: {HEAD}\n"
)

FULLY_QUOTED = (
    "> ## SCORECARD — Naya Clarity\n"
    "> Honest scorecard: 9.6/10\n"
    f"> head: {HEAD}\n"
    "> [NAYA CLARITY]\n"
)

PLAIN = (
    "## SCORECARD — Naya Clarity\n"
    "Honest scorecard: 9.6/10\n"
    f"head: {HEAD}\n"
    "[NAYA CLARITY]\n"
)

GENUINE_BESIDE_QUOTE = (
    "> ## SCORECARD — Naya Clarity\n"
    "> Honest scorecard: 9.6/10\n"
    "\n"
    "## SCORECARD — my own, Naya Verity\n"
    "Honest scorecard: 9.7/10\n"
    f"head: {HEAD}\n"
    "[NAYA VERITY]\n"
)


def test_mixed_form_quoted_scorecard_is_not_a_scorecard():
    """The scored hole: quoted score/seat + one plain head line."""
    assert not _looks_like_scorecard(MIXED, HEAD)


def test_mixed_form_quoted_seat_is_not_the_scorer():
    """Requirement-2 attribution runs on stripped text (review-leg parity)."""
    assert seat_of(_strip_blockquotes(MIXED)) is None


def test_fully_quoted_scorecard_is_not_a_scorecard():
    assert not _looks_like_scorecard(FULLY_QUOTED, HEAD)


def test_lazy_continuation_score_line_stays_quoted():
    body = (
        "> ## SCORECARD — Naya Clarity\n"
        "Honest scorecard: 9.6/10\n"
        "\n"
        f"head: {HEAD}\n"
    )
    assert not _looks_like_scorecard(body, HEAD)


def test_plain_scorecard_still_counts():
    assert _looks_like_scorecard(PLAIN, HEAD)
    assert seat_of(_strip_blockquotes(PLAIN)) == "Naya Clarity"


def test_genuine_scorecard_beside_quote_still_counts():
    """P-014: the fix walks the real path — quoting an earlier scorecard
    must not veto the commenter's own plain-text scorecard below it."""
    assert _looks_like_scorecard(GENUINE_BESIDE_QUOTE, HEAD)
    assert seat_of(_strip_blockquotes(GENUINE_BESIDE_QUOTE)) == "Naya Verity"


def test_unified_mixed_form_does_not_satisfy_scorecard_leg():
    comments = [{"body": (
        "> Seat: Naya Clarity\n"
        "> Honest scorecard: 9.6/10\n"
        f"head: {HEAD}\n"
    )}]
    ok, _detail = unified._scorecard_for_current_head(
        comments, HEAD, AUTHOR, 9.5, tier="A")
    assert not ok


def test_unified_plain_scorecard_still_satisfies():
    comments = [{"body": (
        "Seat: Naya Clarity\n"
        "## SCORECARD\n"
        "Honest scorecard: 9.6/10\n"
        f"head: {HEAD}\n"
    )}]
    ok, _detail = unified._scorecard_for_current_head(
        comments, HEAD, AUTHOR, 9.5, tier="A")
    assert ok
