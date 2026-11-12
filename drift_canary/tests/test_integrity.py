"""Tests: integrity lifecycle, exposure budgets, recovery contract."""
from ..integrity import (
    transition_allowed, IntegrityEvent, INTEGRITY_TRANSITIONS,
    COMPROMISE_MECHANISMS, REPLACEMENT_STEPS,
)
from ..exposure import ExposureBudget, qualification_is_usable, SEPARABLE_FACTS


def test_sealed_never_regained():
    # No transition leads back to sealed (except suspect->sealed = cleared).
    for prior, dests in INTEGRITY_TRANSITIONS.items():
        if prior != "suspect":
            assert "sealed" not in dests, f"{prior} must not return to sealed"


def test_suspect_can_clear_or_confirm():
    assert transition_allowed("suspect", "sealed")
    assert transition_allowed("suspect", "compromised")


def test_compromised_cannot_silently_recover():
    assert not transition_allowed("compromised", "sealed")
    assert not transition_allowed("compromised", "suspect")


def test_retired_is_terminal():
    assert INTEGRITY_TRANSITIONS["retired"] == ()


def test_four_mechanisms():
    assert len(COMPROMISE_MECHANISMS) == 4


def test_integrity_event_rejects_bad_operation():
    try:
        IntegrityEvent(event_id="e1", operation="nuke",
                       canary_set_id="s1")
    except AssertionError:
        return
    raise AssertionError("bad operation must be rejected")


def test_seven_replacement_steps():
    assert len(REPLACEMENT_STEPS) == 7
    assert any("NOT paraphrases" in s for s in REPLACEMENT_STEPS)
    assert any("linked to" in s for s in REPLACEMENT_STEPS)


def test_exposure_budget_exceeded():
    b = ExposureBudget(set_id="s1", max_adaptive_rounds=3)
    for _ in range(4):
        b.record_adaptive_round()
    exceeded, reasons = b.exceeded()
    assert exceeded and reasons
    assert b.requires_fresh_qualification()


def test_exposure_budget_clean():
    b = ExposureBudget(set_id="s1")
    b.record_adaptive_round(feedback_bits=8)
    assert not b.exceeded()[0]


def test_answer_disclosure_always_exceeds():
    b = ExposureBudget(set_id="s1", max_answer_disclosures=0)
    b.record_adaptive_round(answer_disclosure=True)
    assert b.exceeded()[0]


def test_recovery_contract_all_four():
    ok, _ = qualification_is_usable(True, True, True, True)
    assert ok


def test_recovery_contract_any_failure():
    for i in range(4):
        args = [True] * 4
        args[i] = False
        ok, reason = qualification_is_usable(*args)
        assert not ok and reason


def test_three_separable_facts():
    assert len(SEPARABLE_FACTS) == 3
