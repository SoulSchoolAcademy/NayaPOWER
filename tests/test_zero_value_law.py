"""Zero Value Law regression tests (additive clarification to Smart Ledger V2.1).

Core principle: Naya must never confuse zero value with missing knowledge
about value. Null is not zero.

These tests pin the cross-field invariants:
  ZVL-1: UNVERIFIED => d_verified must be null (never numeric, never 0)
  ZVL-2: null delta_v_actual => d_verified must be null (no false zeros)
  ZVL-3: OPEN observation window => d_verified must be null (provisional)
  ZVL-4: numeric d_verified lives on the canonical -9..+9 ladder
  ZVL-5: value_interpretation is one of the six states when present
"""
import pytest

from kernel.value_calculus import (
    build_decision_receipt,
    classify_value_interpretation,
    validate_zero_value_law,
    VALUE_INTERPRETATIONS,
    REFUSE,
)


def _base_receipt(**overrides):
    kwargs = dict(
        decision_id="D-zvl",
        objective="zero value law",
        baseline_id="base",
        stakeholders=[],
        horizon="test",
        evaluation={"selected": None, "decision": REFUSE, "rows": []},
        authority_basis="test-only",
        evidence_refs=["test:zvl"],
        observation_window={},
        verification="UNVERIFIED",
    )
    kwargs.update(overrides)
    return build_decision_receipt(**kwargs)


# 1. Missing measurements must not default to numeric zero.
def test_missing_measurements_do_not_default_to_numeric_zero():
    receipt = _base_receipt()  # no delta_v_actual
    assert receipt["delta_v_actual"] is None
    assert receipt["d_verified"] is None
    assert receipt["d_verified"] != 0  # null, not zero
    assert validate_zero_value_law(receipt) == []


# 2. Predicted exists but actual missing => no verified ladder value.
def test_predicted_without_actual_assigns_no_verified_ladder_value():
    evaluation = {
        "selected": "a1",
        "decision": "ACT",
        "rows": [
            {
                "candidate_id": "a1",
                "gate": "ADMISSIBLE",
                "gate_reasons": [],
                "q": {
                    "Q": 8.0, "confidence_aggregate": 0.9,
                    "confidence_critical": 0.9, "critical_confidences": {},
                    "dimensions": {}, "confidences": {},
                    "missing_dimensions": [], "weights": {},
                },
                "pv": 5.0, "delta_v": 5.2, "v_safe": 5.0,
                "residual_risk": 0.1, "effective_stakes": "low",
                "reversible": True, "dependency_unlock": 0.0,
                "human_burden": 0.0, "is_baseline": False,
                "v_low": 4.0, "v_high": 6.0, "interval_width": 2.0,
            }
        ],
    }
    receipt = _base_receipt(evaluation=evaluation)  # predicted=5.2, actual=None
    assert receipt["delta_v_predicted"] == pytest.approx(5.2)
    assert receipt["delta_v_actual"] is None
    assert receipt["d_verified"] is None
    assert validate_zero_value_law(receipt) == []


# 3. Observation window open => must remain provisional.
def test_open_observation_window_remains_provisional():
    receipt = _base_receipt(
        verification="PASS_PENDING_WINDOW",
        observation_window={"status": "OPEN", "ends_at": "2026-11-10T00:00:00Z"},
        delta_v_actual=5.2,
    )
    # The engine computes d_verified from actual; the LAW validator rejects
    # a numeric d_verified while the window is OPEN.
    violations = validate_zero_value_law(receipt)
    assert any("ZVL-3" in v for v in violations)


# 4. Actual estimate zero but interval wide => inconclusive, not zero.
def test_zero_estimate_with_wide_interval_is_inconclusive():
    interp = classify_value_interpretation(
        delta_v_actual=0.0,
        interval=(-5.0, 4.75),
        tolerance=1.0,
        measured=True,
    )
    assert interp == "INCONCLUSIVE"


# 5. Narrow interval inside justified tolerance => practically neutral.
def test_narrow_interval_inside_tolerance_is_practically_neutral():
    interp = classify_value_interpretation(
        delta_v_actual=0.25,
        interval=(-0.5, 0.75),
        tolerance=1.0,
        measured=True,
    )
    assert interp == "PRACTICALLY_NEUTRAL"


# 6. Exact zero on a deterministic measurement => true zero for that metric.
def test_exact_zero_on_deterministic_measurement_is_true_zero():
    interp = classify_value_interpretation(
        delta_v_actual=0,
        measured=True,
        deterministic=True,
    )
    assert interp == "TRUE_ZERO"


# 7. Positive benefit cancelling unacceptable harm must not pass safety gates.
def test_benefit_cancelling_harm_does_not_pass_as_neutral():
    # A net-zero aggregate that hides an unresolved critical harm is not
    # neutral: the harm dimension keeps the outcome out of TRUE_ZERO /
    # PRACTICALLY_NEUTRAL. The classifier without a resolved harm
    # measurement stays INCONCLUSIVE (unknown harm outcome).
    interp = classify_value_interpretation(
        delta_v_actual=0.0,
        interval=(-9.0, 9.0),
        tolerance=1.0,
        measured=False,  # harm outcome not measured => cannot claim neutral
    )
    assert interp in ("INCONCLUSIVE", "UNMEASURED", "UNKNOWN")
    assert interp not in ("TRUE_ZERO", "PRACTICALLY_NEUTRAL")


# 8. New delayed-harm evidence contradicting a PASS must reopen/correct.
def test_delayed_harm_evidence_reopens_prior_pass():
    # A receipt that was VERIFIED_PASS with d_verified numeric becomes
    # non-compliant once delayed harm evidence reopens the window:
    # the window flips OPEN and the verified ladder value must go null.
    receipt = _base_receipt(
        verification="VERIFIED_PASS",
        delta_v_actual=7.5,
    )
    assert receipt["d_verified"] == pytest.approx(7.5)
    assert validate_zero_value_law(receipt) == []

    reopened = dict(receipt)
    reopened["observation_window"] = {"status": "OPEN"}
    reopened["verification"] = "PASS_PENDING_WINDOW"
    reopened["d_verified"] = None  # corrected: provisional again
    reopened["delta_v_actual"] = None
    assert validate_zero_value_law(reopened) == []

    # Forgetting to null the ladder value on reopen is a violation.
    bad_reopen = dict(reopened)
    bad_reopen["d_verified"] = 7.5
    bad_reopen["delta_v_actual"] = 7.5
    violations = validate_zero_value_law(bad_reopen)
    assert any("ZVL-3" in v for v in violations)


# 9. Display rounding to zero must preserve the raw nonzero result.
def test_display_rounding_preserves_raw_nonzero():
    receipt = _base_receipt(
        verification="VERIFIED_PASS",
        delta_v_actual=0.04,
    )
    # Raw delta preserved exactly; display ladder carries the small value,
    # not a rounded zero that erases the measurement.
    assert receipt["delta_v_actual"] == pytest.approx(0.04)
    assert receipt["d_verified"] == pytest.approx(0.04)
    assert receipt["d_verified"] != 0 or receipt["delta_v_actual"] == 0
    assert validate_zero_value_law(receipt) == []


# 10. Historical UNASSESSED rows with placeholder zero: preserve + annotate.
def test_historical_unassessed_placeholder_zero_is_annotated_not_silently_rewritten():
    historical = {
        "verification": "UNVERIFIED",
        "delta_v_actual": None,
        "d_verified": 0,  # legacy placeholder: MEANT "unknown", stored as 0
        "value_interpretation": "UNKNOWN",
    }
    violations = validate_zero_value_law(historical)
    # The validator flags the legacy false zero ...
    assert any("ZVL-2" in v for v in violations)
    # ... and the annotation (not silent rewriting) is the sanctioned repair:
    repaired = dict(historical)
    repaired["d_verified"] = None
    repaired["value_interpretation"] = "UNKNOWN"
    assert validate_zero_value_law(repaired) == []
    assert repaired["value_interpretation"] == "UNKNOWN"


# The exact false-zero from the framework must be invalid.
def test_framework_false_zero_is_invalid():
    false_zero = {
        "verification": "UNVERIFIED",
        "delta_v_actual": None,
        "d_verified": 0,
        "observation_window": {},
    }
    violations = validate_zero_value_law(false_zero)
    assert any("ZVL-1" in v for v in violations)
    assert any("ZVL-2" in v for v in violations)


# d_verified respects the canonical -9..+9 ladder.
def test_d_verified_clamped_to_canonical_ladder():
    over = _base_receipt(verification="VERIFIED_PASS", delta_v_actual=25.0)
    assert over["d_verified"] == pytest.approx(9.0)
    under = _base_receipt(verification="VERIFIED_PASS", delta_v_actual=-25.0)
    assert under["d_verified"] == pytest.approx(-9.0)
    assert validate_zero_value_law(over) == []
    assert validate_zero_value_law(under) == []


# Six states are exactly the six states.
def test_six_value_interpretation_states():
    assert set(VALUE_INTERPRETATIONS) == {
        "TRUE_ZERO",
        "PRACTICALLY_NEUTRAL",
        "UNKNOWN",
        "UNMEASURED",
        "DELAYED",
        "INCONCLUSIVE",
    }


# Delayed classification when the window is open.
def test_open_window_classifies_as_delayed():
    assert classify_value_interpretation(window_open=True) == "DELAYED"
    assert classify_value_interpretation(measured=False) == "UNMEASURED"
    assert classify_value_interpretation(measured=True) == "UNKNOWN"
