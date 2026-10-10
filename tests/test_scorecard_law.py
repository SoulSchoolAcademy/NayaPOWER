"""Tests for kernel/scorecard_law.py — Operating Code V2 §1.1.

Run: python -m pytest tests/test_scorecard_law.py -q   (from repo root)
"""

import pytest

from kernel.scorecard_law import (
    AUTHORITY_HUMAN_ONLY_GATE,
    DECIDE_NO_CLEAR_WINNER,
    DECIDE_NO_GATE_PASSERS,
    DECIDE_WINNER_FAILED_GATE,
    DECIDE_WINNER_NOT_ENUMERATED,
    DECIDE_WINNER_NOT_HIGHEST,
    ENUMERATE_DUPLICATE_ID,
    ENUMERATE_MISSING_ID,
    ENUMERATE_OPTIONS_NOT_LIST,
    ENUMERATE_TOO_FEW_OPTIONS,
    GATE_FAILED,
    GATE_NOT_BOOLEAN,
    NEEDS_AUTHORITY,
    NO_DECISION,
    PROCEED,
    RECEIPT_MISSING_STEP,
    RECEIPT_NOT_POSTED,
    SCORE_DIMENSION_OUT_OF_RANGE,
    SCORE_MISSING_DIMENSION,
    SCORE_NON_NUMERIC_DIMENSION,
    SCORE_OPTION_NOT_SCORED,
    ENGINE_ID,
    GATE_FIELDS,
    HUMAN_ONLY_GATES,
    SCORE_DIMENSIONS,
    STEPS,
    build_receipt,
    receipt_summary,
    run_scorecard,
    validate_receipt,
)


def dims(**overrides):
    base = {
        "mission_alignment": 8.0,
        "value_produced": 8.0,
        "consequences": 8.0,
        "collective_impact": 8.0,
        "risk": 8.0,
        "reversibility": 8.0,
    }
    base.update(overrides)
    return base


def gates(**overrides):
    base = {"reversible": True, "no_major_damage": True, "positive_forward_effect": True}
    base.update(overrides)
    return base


def full_kwargs(a="merge", b="hold", **kw):
    k = {
        "option_ids": [a, b],
        "scores": {a: dims(value_produced=9.0), b: dims(value_produced=5.0)},
        "gates": {a: gates(), b: gates()},
        "decision_id": "SC-TEST-1",
        "decided_by": "naya-4",
        "decided_at": "2026-10-10T15:00:00Z",
        "receipt_posted_comment_id": 6098821717,
    }
    k.update(kw)
    return k


# ---- Step 1: ENUMERATE -------------------------------------------------------


def test_enumerate_happy_path_proceeds():
    r = run_scorecard(**full_kwargs())
    assert r.verdict == PROCEED
    assert r.winner_id == "merge"
    assert r.totals["merge"] > r.totals["hold"]
    assert r.killed_by_gate == {}
    assert r.receipt["engine"] == ENGINE_ID


def test_enumerate_requires_at_least_two_options():
    r = run_scorecard(option_ids=["only"], scores={}, gates={})
    assert r.verdict == NO_DECISION
    assert any(ENUMERATE_TOO_FEW_OPTIONS in x for x in r.reasons)


def test_enumerate_rejects_missing_ids():
    r = run_scorecard(option_ids=["a", ""], scores={}, gates={})
    assert r.verdict == NO_DECISION
    assert any(ENUMERATE_MISSING_ID in x for x in r.reasons)


def test_enumerate_rejects_duplicate_ids():
    r = run_scorecard(option_ids=["a", "a"], scores={}, gates={})
    assert r.verdict == NO_DECISION
    assert any(ENUMERATE_DUPLICATE_ID in x for x in r.reasons)


def test_enumerate_rejects_non_list():
    r = run_scorecard(option_ids="merge", scores={}, gates={})
    assert r.verdict == NO_DECISION
    assert any(ENUMERATE_OPTIONS_NOT_LIST in x for x in r.reasons)


# ---- Step 2: SCORE -----------------------------------------------------------


def test_score_requires_every_option_scored():
    k = full_kwargs()
    del k["scores"]["hold"]
    r = run_scorecard(**k)
    assert r.verdict == NO_DECISION
    assert any(SCORE_OPTION_NOT_SCORED in x for x in r.reasons)


def test_score_rejects_missing_dimension():
    k = full_kwargs()
    bad = dims()
    del bad["risk"]
    k["scores"]["hold"] = bad
    r = run_scorecard(**k)
    assert r.verdict == NO_DECISION
    assert any(SCORE_MISSING_DIMENSION in x for x in r.reasons)


def test_score_rejects_non_numeric_dimension():
    k = full_kwargs()
    k["scores"]["hold"] = dims(risk="high")
    r = run_scorecard(**k)
    assert r.verdict == NO_DECISION
    assert any(SCORE_NON_NUMERIC_DIMENSION in x for x in r.reasons)


def test_score_rejects_boolean_dimension():
    k = full_kwargs()
    k["scores"]["hold"] = dims(risk=True)
    r = run_scorecard(**k)
    assert any(SCORE_NON_NUMERIC_DIMENSION in x for x in r.reasons)


def test_score_rejects_out_of_range_dimension():
    k = full_kwargs()
    k["scores"]["hold"] = dims(value_produced=11)
    r = run_scorecard(**k)
    assert any(SCORE_DIMENSION_OUT_OF_RANGE in x for x in r.reasons)


def test_six_v2_dimensions_are_the_law():
    assert SCORE_DIMENSIONS == (
        "mission_alignment",
        "value_produced",
        "consequences",
        "collective_impact",
        "risk",
        "reversibility",
    )


# ---- Step 3: GATE — gates run before scores are read -------------------------


def test_gate_failure_kills_highest_scoring_option():
    # "merge" scores 60/60 but fails the reversibility gate: it must lose.
    k = full_kwargs(
        scores={
            "merge": dims(value_produced=10, mission_alignment=10, consequences=10,
                           collective_impact=10, risk=10, reversibility=10),
            "hold": dims(),
        },
        gates={"merge": gates(reversible=False), "hold": gates()},
    )
    r = run_scorecard(**k)
    assert r.verdict == PROCEED
    assert r.winner_id == "hold"
    assert r.killed_by_gate["merge"] == ["reversible"]
    assert any(GATE_FAILED in x for x in r.reasons)


def test_gate_requires_booleans():
    k = full_kwargs(gates={"merge": gates(reversible="yes"), "hold": gates()})
    r = run_scorecard(**k)
    assert r.verdict == NO_DECISION
    assert any(GATE_NOT_BOOLEAN in x for x in r.reasons)


def test_all_options_killed_is_no_decision():
    k = full_kwargs(gates={"merge": gates(reversible=False), "hold": gates(no_major_damage=False)})
    r = run_scorecard(**k)
    assert r.verdict == NO_DECISION
    assert any(DECIDE_NO_GATE_PASSERS in x for x in r.reasons)
    assert r.winner_id is None


# ---- V2 §1.3: a score never grants permission --------------------------------


def test_authority_override_needs_shawn_despite_highest_score():
    k = full_kwargs(authority_flags={"production_db": True})
    r = run_scorecard(**k)
    assert r.verdict == NEEDS_AUTHORITY
    assert r.winner_id is None
    assert any(AUTHORITY_HUMAN_ONLY_GATE in x for x in r.reasons)


def test_no_authority_flags_proceeds():
    k = full_kwargs(authority_flags={"production_db": False, "workflows": False})
    assert run_scorecard(**k).verdict == PROCEED


def test_human_only_gates_match_v2():
    assert set(HUMAN_ONLY_GATES) == {
        "constitutional_ratification",
        "production_dispatch",
        "production_db",
        "workflows",
        "credentials_money",
        "destructive_irreversible",
        "authority_consent_security",
    }


# ---- Step 4: DECIDE ----------------------------------------------------------


def test_tie_is_no_decision_not_a_coin_flip():
    k = full_kwargs(scores={"merge": dims(), "hold": dims()})
    r = run_scorecard(**k)
    assert r.verdict == NO_DECISION
    assert r.winner_id is None
    assert any(DECIDE_NO_CLEAR_WINNER in x for x in r.reasons)


def test_deterministic_tiebreak_documented_by_id_order():
    # exact-equal totals tie; ids sorted in the reason, reproducible.
    k = full_kwargs(scores={"merge": dims(), "hold": dims()})
    r = run_scorecard(**k)
    assert "['hold', 'merge']" in r.reasons[0]


# ---- Step 5: RECEIPT — no receipt, no action ---------------------------------


def test_receipt_has_all_five_steps():
    r = run_scorecard(**full_kwargs())
    for step in ("step1_enumerate", "step2_score", "step3_gate", "step4_decide", "step5_receipt"):
        assert step in r.receipt
    assert r.receipt["step4_decide"]["winner"] == "merge"
    assert r.receipt["step5_receipt"]["receipt_posted_comment_id"] == 6098821717


def test_receipt_round_trip_validates():
    r = run_scorecard(**full_kwargs())
    ok, reasons = validate_receipt(r.receipt)
    assert ok, reasons


def test_validate_receipt_rejects_winner_not_enumerated():
    r = run_scorecard(**full_kwargs())
    r.receipt["step4_decide"]["winner"] = "phantom"
    ok, reasons = validate_receipt(r.receipt)
    assert not ok
    assert any(DECIDE_WINNER_NOT_ENUMERATED in x for x in reasons)


def test_validate_receipt_rejects_gate_failed_winner():
    k = full_kwargs(gates={"merge": gates(reversible=False), "hold": gates()})
    r = run_scorecard(**k)
    assert r.winner_id == "hold"
    # tamper: claim the gate-killed option won anyway
    r.receipt["step4_decide"]["winner"] = "merge"
    ok, reasons = validate_receipt(r.receipt)
    assert not ok
    assert any(DECIDE_WINNER_FAILED_GATE in x for x in reasons)


def test_validate_receipt_rejects_non_highest_winner():
    r = run_scorecard(**full_kwargs())
    r.receipt["step4_decide"]["winner"] = "hold"
    ok, reasons = validate_receipt(r.receipt)
    assert not ok
    assert any(DECIDE_WINNER_NOT_HIGHEST in x for x in reasons)


def test_validate_receipt_rejects_unposted_receipt():
    r = run_scorecard(**full_kwargs(receipt_posted_comment_id=None))
    ok, reasons = validate_receipt(r.receipt)
    assert not ok
    assert any(RECEIPT_NOT_POSTED in x for x in reasons)


def test_validate_receipt_rejects_missing_step():
    r = run_scorecard(**full_kwargs())
    del r.receipt["step3_gate"]
    ok, reasons = validate_receipt(r.receipt)
    assert not ok
    assert any(RECEIPT_MISSING_STEP in x for x in reasons)


def test_validate_receipt_rejects_non_object():
    ok, reasons = validate_receipt("not-a-receipt")
    assert not ok
    assert reasons


# ---- Plain-meaning summary (V2 §2) --------------------------------------------


def test_receipt_summary_plain_words():
    r = run_scorecard(**full_kwargs())
    assert "merge" in receipt_summary(r)
    r2 = run_scorecard(**full_kwargs(authority_flags={"credentials_money": True}))
    assert "SHAWN" in receipt_summary(r2)
    r3 = run_scorecard(option_ids=["x"], scores={}, gates={})
    assert "NO DECISION" in receipt_summary(r3)


def test_build_receipt_is_deterministic():
    a = build_receipt("D", ["x", "y"], {}, {}, PROCEED, "x", [], "n", "t", 1)
    b = build_receipt("D", ["x", "y"], {}, {}, PROCEED, "x", [], "n", "t", 1)
    assert a == b
    assert list(a) == ["engine", "engine_version", "decision_id", "decided_by", "decided_at",
                       "step1_enumerate", "step2_score", "step3_gate", "step4_decide", "step5_receipt"]
