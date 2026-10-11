"""Signed-value clamp fix (SL-017): negative magnitude must survive end to end.

Layer separation under test:
  1. HARD GATES — admissibility (gates still refuse PROHIBITED).
  2. SIGNED VALUE — V>0 above, V=0 neutral, V<0 below; ±9 anchors are
     vocabulary, never clipping bounds.
  3. QUALITY — Q stays a separate 0..10 number, never conflated with value.
  4. CONFIDENCE — visible, untouched by this change.
Plus no-score-laundering: predicted vs verified-actual is recorded and
material miscalibration is flagged.
"""

import pytest

from kernel.value_calculus import (
    ADMISSIBLE,
    PROHIBITED,
    Candidate,
    PVEstimate,
    QualityProfile,
    RiskPolicy,
    assess_miscalibration,
    build_decision_receipt,
    delta_value,
    evaluate_candidates,
    gate_candidate,
    score_quality,
)


@pytest.fixture
def profile():
    return QualityProfile(
        profile_id="NAYAPOWER-DECISION",
        version="2.1",
        objective="maximum responsible verified value",
        min_evidence_count=2,
        relative_margin=0.10,
    )


def pv(B=8, H=0, C=1, R=0.2, conf=0.95, evidence_count=3):
    return PVEstimate(B, H, C, R, {k: conf for k in ("B", "H", "C", "R")}, evidence_count)


def quality(score=9.5, conf=0.95, **overrides):
    dims = {
        "objective_fit": score,
        "evidence_sufficiency": score,
        "applicability": score,
        "robustness": score,
        "reversibility": score,
        "blast_containment": score,
        "simplicity": score,
    }
    dims.update(overrides)
    return dims, {k: conf for k in dims}


def cand(cid, *, baseline=False, B=8, H=0, score=9.5, conf=0.95, **kwargs):
    q, c = quality(score, conf)
    hard = dict(lawful=True, rights_safe=True, privacy_safe=True, safety_safe=True)
    hard.update({k: kwargs.pop(k) for k in list(kwargs) if k in hard})
    return Candidate(
        cid, q, c, pv(B=B, H=H, conf=conf), authorized=True, reversible=True,
        human_authorized=False, is_baseline=baseline, **hard, **kwargs)


# --- Layer 2: signed value ---------------------------------------------------

def test_negative_value_scores_negative_not_zero(profile):
    """A below-the-line action must score negative through the full formula."""
    base = cand("base", baseline=True, B=5, H=1)
    bad = cand("bad", B=2, H=9)  # PV = 2-9-1-0.2 < 0
    assert bad.pv.pv() < 0
    d = delta_value(bad, base, profile)
    assert d < 0, f"delta_value must be negative, got {d}"
    ev = evaluate_candidates([base, bad], "base", profile)
    row = next(r for r in ev["rows"] if r["candidate_id"] == "bad")
    assert row["delta_v"] < 0
    assert row["v_safe"] < 0
    # scored negative, but not selected: below-the-line never wins
    assert ev["selected"] != "bad"


def test_neutral_scores_zero():
    e = pv(B=5, H=4, C=1, R=0, conf=0.95)
    assert e.pv(uncertainty_scale=0.0) == 0.0


def test_anchors_are_vocabulary_not_bounds(profile):
    """±9 anchors must not clip: extreme magnitude survives the receipt."""
    evaluation = {"selected": "a", "rows": [{"candidate_id": "a", "delta_v": 9.0}]}
    kw = dict(decision_id="d", objective="o", baseline_id="b", stakeholders=[],
              horizon="h", evaluation=evaluation, authority_basis="t",
              evidence_refs=[], observation_window={}, verification="VERIFIED_PASS")
    r_neg = build_decision_receipt(delta_v_actual=-14.5, **kw)
    assert r_neg["d_verified"] == -14.5, "negative magnitude must not be clipped"
    r_pos = build_decision_receipt(delta_v_actual=12.3, **kw)
    assert r_pos["d_verified"] == 12.3, "extreme positive magnitude must not be clipped"
    r_anchor = build_decision_receipt(delta_v_actual=-9.0, **kw)
    assert r_anchor["d_verified"] == -9.0
    r_zero = build_decision_receipt(delta_v_actual=0.0, **kw)
    assert r_zero["d_verified"] == 0.0


# --- Layer 1: gates unaffected ------------------------------------------------

def test_gates_still_refuse_prohibited(profile):
    bad = cand("bad", hard_violation=True)
    gate, reasons, _ = gate_candidate(bad, profile, RiskPolicy())
    assert gate == PROHIBITED


# --- Layer 3: quality stays a separate 0..10 number ---------------------------

def test_quality_separate_from_value_sign(profile):
    """Q measures decision soundness; a negative-value candidate still gets Q in [0,10]."""
    bad = cand("bad", B=1, H=9, score=9.5)
    q = score_quality(bad, profile)
    assert 0.0 <= q["Q"] <= 10.0
    assert q["Q"] > 9.0  # sound decision, terrible value — the layers disagree, correctly
    assert bad.pv.pv() < 0  # and value stays negative


# --- No score laundering ------------------------------------------------------

def test_predicted_plus9_landing_plus2_is_flagged():
    rec = assess_miscalibration(9.0, 2.0)
    assert rec["miscalibrated"] is True
    assert rec["reason"] == "LARGE_ABSOLUTE_ERROR"
    assert rec["abs_error"] == 7.0
    assert rec["signed_error"] == -7.0


def test_close_prediction_not_flagged():
    rec = assess_miscalibration(9.0, 8.5)
    assert rec["miscalibrated"] is False
    assert rec["reason"] == "WITHIN_TOLERANCE"


def test_sign_flip_flagged():
    rec = assess_miscalibration(2.0, -1.5)
    assert rec["miscalibrated"] is True
    assert rec["reason"] == "SIGN_FLIP"


def test_no_prediction_never_raises():
    rec = assess_miscalibration(None, -4.0)
    assert rec["miscalibrated"] is False
    assert rec["reason"] == "NO_PREDICTION"
    assert rec["actual"] == -4.0


def test_receipt_carries_miscalibration_record():
    evaluation = {"selected": "a", "rows": [{"candidate_id": "a", "delta_v": 9.0}]}
    r = build_decision_receipt(
        decision_id="d", objective="o", baseline_id="b", stakeholders=[],
        horizon="h", evaluation=evaluation, authority_basis="t",
        evidence_refs=[], observation_window={}, verification="VERIFIED_PASS",
        delta_v_actual=2.0)
    m = r["miscalibration"]
    assert m["miscalibrated"] is True
    assert m["predicted"] == 9.0 and m["actual"] == 2.0
    # back-compat absolute error still present
    assert r["calibration_error"] == 7.0
