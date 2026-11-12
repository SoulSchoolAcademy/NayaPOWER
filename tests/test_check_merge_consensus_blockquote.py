"""Regression tests: consensus gate blockquote hardening.

Director finding on PR #2808's post-landing violation proof (2026-10-21):
the blockquote hole in `tools/check_merge_consensus.py` was STILL LIVE at
tip — #2808 never touched the gate. A GitHub blockquote (`> ...`) is how the
reply-to-comment button quotes someone else's words: it is a MENTION of an
approval, never the commenter's own USE declaration. The mention-vs-use
hardening covered backtick/double-quote/single-quote/curly-quote spans but
never the blockquote form, so quoting "[NAYA EPSILON · REVIEW] APPROVED" in
a `>` block satisfied the review requirement as if Epsilon had approved.

These tests pin the corrected predicate: blockquote paragraphs (including
lazy continuations, which GitHub still renders as quoted) are stripped
before the mention-vs-use analysis, and Path B seat attribution runs on the
stripped text.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

from check_merge_consensus import _looks_like_review, _strip_blockquotes, seat_of

EPSILON = "ac4878f8283606a60cbbad3ad7437a8b9a70a433"


def test_blockquoted_approval_is_not_a_review():
    """The core hole: a comment that only QUOTES an approval in a
    blockquote is not the commenter's own verdict declaration."""
    assert not _looks_like_review(
        "> [NAYA EPSILON · REVIEW] APPROVED\n\n"
        "Just quoting the above for reference — I have not reviewed this PR."
    )


def test_nested_blockquote_approval_is_not_a_review():
    assert not _looks_like_review(">> [NAYA DELTA · REVIEW] APPROVED\n\nreplying up-thread")


def test_lazy_continuation_stays_quoted():
    """GitHub renders lazy continuations (no `>` marker, same paragraph)
    inside the quote — an attack cannot evade the strip by dropping the
    marker on the second line."""
    assert not _looks_like_review(
        "> [NAYA EPSILON · REVIEW] APPROVED\n"
        "continuing the same quoted paragraph without a marker\n\n"
        "My own words, no verdict."
    )


def test_self_quote_does_not_manufacture_a_review():
    """The exploit shape: the PR author quotes another seat's approval and
    claims consensus. The quoted seat must never count as reviewer."""
    body = ("> [NAYA DELTA · REVIEW] APPROVED\n\n"
            "Replying to Delta's review — merging per their approval.")
    assert not _looks_like_review(body)


def test_quoted_seat_not_attributed_as_reviewer():
    """When a comment carries both a quote and a genuine approval, the
    reviewer is the seat that genuinely approved — never the quoted seat."""
    body = ("> [NAYA EPSILON · REVIEW] APPROVED\n\n"
            "[NAYA DELTA · REVIEW] APPROVED — my own independent review.")
    assert _looks_like_review(body)
    assert seat_of(_strip_blockquotes(body)) == "Naya Delta"


def test_genuine_approval_beside_blockquote_still_counts():
    """P-014: the fix walks the real path. A plain-text approval keeps
    counting even when the comment also quotes something."""
    assert _looks_like_review(
        "> [NAYA EPSILON · REVIEW] APPROVED\n\n"
        "[NAYA DELTA · REVIEW] APPROVED — independent review of this PR."
    )


def test_blockquoted_hold_is_not_a_veto():
    """Symmetric with approval: a quoted HOLD is a mention, not the
    commenter's verdict — it must not veto a genuine approval."""
    assert _looks_like_review(
        "[NAYA THETA · REVIEW] APPROVED — looks good.\n\n"
        "> [NAYA ALPHA - REVIEW] HOLD"
    )


def test_strip_blockquotes_unit():
    assert _strip_blockquotes("own\n\n> quoted\n> more\n\nown2") == "own\n\n\nown2"
    assert _strip_blockquotes(None) == ""
    assert _strip_blockquotes("") == ""
    assert _strip_blockquotes("> only quotes\n> here") == ""
    assert _strip_blockquotes("no quotes here") == "no quotes here"
