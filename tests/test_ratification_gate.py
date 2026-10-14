"""Battery for the ratification gate (Naya 5, 2026-10-13;
repaired 2026-10-14 after Naya 3's P0 adversarial finding).

The incident: #2550's title claimed "Shawn RATIFIED" from encouragement.
The law: a claimed "Shawn said" can NEVER upgrade a verdict.
The repair: the gate no longer accepts words at all — code cannot
authenticate a human. Naya 3's three adversarial inputs are regression
tests below: the word paths are GONE, not guarded.
"""

import sys
from itertools import product
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from ratification_gate import (ratify, attest_ratification, describe,
                               RATIFIED, NOT_RATIFIED, CANDIDATE,
                               NEEDS_SHAWN, RATIFICATION_BAR)


def test_seven_is_not_ratified():
    v, _ = ratify(score=7.0, protocol_green=True)
    assert v == NOT_RATIFIED


def test_word_path_is_gone_not_guarded():
    # Naya 3's A1: a claimed word + content hash minted RATIFIED.
    # The parameter no longer exists — TypeError, not a verdict.
    with pytest.raises(TypeError):
        ratify(scorable=False, claimed_word="yeah sure, ship it",
               content_hash="deadbeef")


def test_override_flag_is_gone_not_guarded():
    # Naya 3's A2: explicit_override=True minted RATIFIED on a 4.0.
    with pytest.raises(TypeError):
        ratify(score=4.0, protocol_green=False, explicit_override=True,
               content_hash="deadbeef")


def test_no_input_combination_mints_ratified_except_math():
    # Adversarial sweep: RATIFIED is reachable ONLY via
    # scorable + score >= 9.5 + protocol green. Everything else —
    # every score, every flag combination — must not ratify.
    for score, green, scorable in product(
            [None, 0.0, 4.0, 9.4, 9.5, 10.0], [False, True], [False, True]):
        v, reasons = ratify(score=score, protocol_green=green,
                            scorable=scorable)
        expect = (scorable and score is not None
                  and score >= RATIFICATION_BAR and green)
        assert (v == RATIFIED) == expect, (score, green, scorable, v, reasons)


def test_nine_five_auto_ratifies_without_his_word():
    v, reasons = ratify(score=9.6, protocol_green=True)
    assert v == RATIFIED, (v, reasons)
    assert any("not needed" in r for r in reasons)


def test_qualifying_score_without_protocol_is_candidate():
    v, _ = ratify(score=9.6, protocol_green=False)
    assert v == CANDIDATE


def test_unscored_cannot_ratify():
    v, reasons = ratify(score=None)
    assert v == CANDIDATE, (v, reasons)
    assert any("never measured" in r for r in reasons)


def test_nonscorable_needs_shawn_and_names_the_path():
    v, reasons = ratify(scorable=False)
    assert v == NEEDS_SHAWN, (v, reasons)
    assert any("attest_ratification" in r for r in reasons)
    assert any("never a" in r and "quoted string" in r for r in reasons)


def test_attestation_requires_exact_content():
    with pytest.raises(ValueError, match="content_hash"):
        attest_ratification(content_hash="", evidence_ref="6158000001",
                            attested_by="Shawn")


def test_attestation_requires_checkable_evidence_not_quotes():
    with pytest.raises(ValueError, match="evidence_ref"):
        attest_ratification(content_hash="deadbeef", evidence_ref="",
                            attested_by="Shawn")
    # A bare quoted string is not evidence either — but the type system
    # can't tell; the contract is documented and the attester is named.


def test_attestation_requires_a_named_attester():
    with pytest.raises(ValueError, match="attested_by"):
        attest_ratification(content_hash="deadbeef",
                            evidence_ref="6158000001", attested_by="")


def test_attestation_returns_record_not_verdict():
    rec = attest_ratification(content_hash="deadbeef",
                              evidence_ref="6158000001",
                              attested_by="Shawn")
    assert rec["attestation"] == "RATIFICATION_ATTESTED"
    assert rec["content_hash"] == "deadbeef"
    assert rec["evidence_ref"] == "6158000001"
    assert rec["attested_by"] == "Shawn"
    # The gate never consumes this: ratify() has no attestation input.
    import inspect
    assert "attest" not in inspect.signature(ratify).parameters


def test_bar_is_nine_five():
    assert RATIFICATION_BAR == 9.5


def test_describe_renders():
    line = describe(ratify(score=7.0))
    assert line.startswith("NOT_RATIFIED"), line
