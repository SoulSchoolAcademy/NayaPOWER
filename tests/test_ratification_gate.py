"""Battery for the ratification gate (Naya 5, 2026-10-13).

The incident: #2550's title claimed "Shawn RATIFIED" from encouragement.
The law: a claimed "Shawn said" can NEVER upgrade a verdict.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from ratification_gate import (ratify, describe, RATIFIED, NOT_RATIFIED,
                               CANDIDATE, NEEDS_SHAWN, RATIFICATION_BAR)


def test_seven_with_looks_good_is_not_ratified():
    v, reasons = ratify(score=7.0, protocol_green=True,
                        claimed_word="The word! :)")
    assert v == NOT_RATIFIED, (v, reasons)
    assert any("encouragement never ratifies" in r for r in reasons)


def test_claimed_word_never_upgrades():
    # Even with every citation, 7/10 stays NOT_RATIFIED.
    v, _ = ratify(score=7.0, protocol_green=True,
                  claimed_word="Shawn said ratified", content_hash="abc123")
    assert v == NOT_RATIFIED


def test_nine_five_auto_ratifies_without_his_word():
    v, reasons = ratify(score=9.6, protocol_green=True)
    assert v == RATIFIED, (v, reasons)
    assert any("not needed" in r for r in reasons)


def test_qualifying_score_without_protocol_is_candidate():
    v, _ = ratify(score=9.6, protocol_green=False)
    assert v == CANDIDATE


def test_unscored_cannot_ratify():
    v, reasons = ratify(score=None, claimed_word="looks great")
    assert v == CANDIDATE, (v, reasons)
    assert any("never measured" in r for r in reasons)


def test_nonscorable_needs_his_word():
    v, _ = ratify(scorable=False)
    assert v == NEEDS_SHAWN
    v, reasons = ratify(scorable=False, claimed_word="yes, do it",
                        content_hash="deadbeef")
    assert v == RATIFIED, (v, reasons)
    assert any("deadbeef" in r for r in reasons)


def test_nonscorable_word_without_hash_is_not_enough():
    v, reasons = ratify(scorable=False, claimed_word="sure")
    assert v == NEEDS_SHAWN, (v, reasons)


def test_explicit_override_is_recorded_not_casual():
    v, reasons = ratify(score=7.0, explicit_override=True,
                        content_hash="abc123",
                        claimed_word="I am overriding the bar for this")
    assert v == RATIFIED, (v, reasons)
    assert any("EXPLICIT override" in r for r in reasons)


def test_override_without_hash_does_not_ratify():
    v, _ = ratify(score=7.0, explicit_override=True)
    assert v == NOT_RATIFIED


def test_bar_is_nine_five():
    assert RATIFICATION_BAR == 9.5


def test_describe_renders():
    line = describe(ratify(score=7.0, claimed_word="nice"))
    assert line.startswith("NOT_RATIFIED"), line
