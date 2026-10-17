"""Regression tests for NAYA-ZERO-VALUE-LAW-V1 (PROPOSED, NOT RATIFIED).

The ten required regression tests from the build spec, plus the exact gap case.
All must be green. One failure = the law's machinery is not proven.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from zero_value_law import (
    classify_zero,
    validate_receipt,
    reconsider_prior,
    annotate_historical,
    audit_null_discipline,
    TRUE_ZERO, PRACTICALLY_NEUTRAL, UNKNOWN, UNMEASURED, DELAYED,
    INCONCLUSIVE, BASELINE_ZERO, ROUNDED_DISPLAY_ZERO,
    NULL_ACTUAL_WITH_VERIFIED_VALUE, VERIFIED_VALUE_WITHOUT_VERIFICATION,
    ZERO_WITHOUT_ESTABLISHMENT, PRACTICAL_NEUTRALITY_NEEDS_EPSILON,
    INTERPRETATION_VALUE_MISMATCH, ROUNDED_ZERO_NEEDS_RAW,
    PREDICTED_IS_NOT_VERIFIED, HARM_UNRESOLVED_BLOCKS_NEUTRAL,
)

EPS = {"value": 1.0, "version": "eps-v1", "justification": "domain materiality study 2026-10"}

passed = []
failed = []


def check(name, cond, detail=""):
    (passed if cond else failed).append(name)
    print(("PASS " if cond else "FAIL ") + name + ((" — " + detail) if detail and not cond else ""))


# Test 1: Missing measurements must not default to numeric zero.
r = classify_zero(assessment_state="UNASSESSED", measurement_performed=False)
check("T1a unmeasured-not-zero", r["interpretation"] == UNMEASURED)
v = validate_receipt({"verification": "UNVERIFIED", "delta_v_actual": None,
                      "d_verified": 0, "evidence_refs": []})
check("T1b missing-measurement-zero-refused", not v["ok"] and NULL_ACTUAL_WITH_VERIFIED_VALUE in v["refusals"])

# Test 2: Predicted exists, actual missing → must not assign verified ladder value.
v = validate_receipt({"verification": "UNVERIFIED", "delta_v_predicted": 5.2,
                      "delta_v_actual": None, "d_verified": None, "evidence_refs": []})
check("T2a predicted-stays-unverified", v["ok"] and v["notes"] and "null discipline" in v["notes"][-1])
v = validate_receipt({"verification": "UNVERIFIED", "delta_v_predicted": 5.2,
                      "delta_v_actual": None, "d_verified": 5.2, "evidence_refs": []})
check("T2b prediction-laundered-into-verified-refused",
      not v["ok"] and PREDICTED_IS_NOT_VERIFIED in v["refusals"])

# Test 3: Observation window still open → stays provisional.
r = classify_zero(assessment_state="ASSESSED", verification="PASS_PENDING_WINDOW",
                  actual_value=5.2, evidence_refs=["e1"],
                  observation_window={"status": "OPEN", "ends_at": "2026-11-10T00:00:00Z"})
check("T3 window-open-stays-delayed", r["interpretation"] == DELAYED)

# Test 4: Actual estimate zero but interval wide → INCONCLUSIVE.
r = classify_zero(assessment_state="ASSESSED", interval=[-5.0, 5.0], epsilon=EPS,
                  evidence_refs=["e1"])
check("T4 wide-interval-inconclusive", r["interpretation"] == INCONCLUSIVE)

# Test 5: Narrow interval inside justified tolerance → PRACTICALLY_NEUTRAL.
r = classify_zero(assessment_state="ASSESSED", interval=[-0.5, 0.5], epsilon=EPS,
                  evidence_refs=["e1"])
check("T5a narrow-interval-practically-neutral", r["interpretation"] == PRACTICALLY_NEUTRAL)
r = classify_zero(assessment_state="ASSESSED", interval=[-0.5, 0.5],
                  epsilon={"value": 1.0}, evidence_refs=["e1"])  # no version/justification
check("T5b neutrality-without-epsilon-refused",
      r["interpretation"] == INCONCLUSIVE and r["refusal"] == PRACTICAL_NEUTRALITY_NEEDS_EPSILON)

# Test 6: Exact zero on deterministic measurement → TRUE_ZERO for that metric.
r = classify_zero(assessment_state="VERIFIED_VALUE", verification="VERIFIED_PASS",
                  deterministic=True, actual_value=0, evidence_refs=["count-e1"])
check("T6a deterministic-exact-zero", r["interpretation"] == TRUE_ZERO)
r = classify_zero(assessment_state="ASSESSED", deterministic=True, actual_value=0,
                  evidence_refs=[])
check("T6b exact-zero-without-evidence-refused",
      r["refusal"] == ZERO_WITHOUT_ESTABLISHMENT)

# Test 7: Positive benefit vs unacceptable stakeholder harm → gates hold.
r = classify_zero(assessment_state="ASSESSED", interval=[4.0, 7.0], epsilon=EPS,
                  evidence_refs=["e1"], unresolved_harm=True)
check("T7 harm-blocks-neutral",
      r["interpretation"] == INCONCLUSIVE and r["refusal"] == HARM_UNRESOLVED_BLOCKS_NEUTRAL)

# Test 8: New delayed-harm evidence contradicts earlier PASS → reopen.
prior = {"verification": "VERIFIED_PASS", "delta_v_actual": 5.2, "d_verified": 5.2,
         "observation_window": {"status": "CLOSED"}}
out = reconsider_prior(prior, ["harm-study-1"], delayed_harm=True)
check("T8a delayed-harm-reopens", out["reopened"] and out["new_verification"] == "ESCALATE"
      and out["value_interpretation"] == INCONCLUSIVE)
out = reconsider_prior(prior, ["confirming-study-1"], contradicts=False)
check("T8b non-contradicting-evidence-no-reopen", not out["reopened"])

# Test 9: Display rounding → raw preserved, raw governs.
r = classify_zero(assessment_state="ASSESSED", display_rounded=True, raw_value=0.4,
                  evidence_refs=["e1"])
check("T9a rounded-display-zero", r["interpretation"] == ROUNDED_DISPLAY_ZERO
      and r["raw_value"] == 0.4)
v = validate_receipt({"verification": "VERIFIED_PASS", "delta_v_actual": 0.4,
                      "delta_v_actual_raw": 0.4, "d_verified": 0.4,
                      "value_interpretation": ROUNDED_DISPLAY_ZERO, "evidence_refs": ["e1"]})
check("T9b rounded-receipt-keeps-raw", v["ok"])
v = validate_receipt({"verification": "VERIFIED_PASS", "delta_v_actual": 0.4,
                      "d_verified": 0.4, "value_interpretation": ROUNDED_DISPLAY_ZERO,
                      "evidence_refs": ["e1"]})
check("T9c rounded-without-raw-refused", not v["ok"] and ROUNDED_ZERO_NEEDS_RAW in v["refusals"])

# Test 10: Historical UNASSESSED rows with placeholder zero → annotate, never rewrite.
row = {"decision_id": "d-101", "assessment_state": "UNASSESSED",
       "delta_v_actual": 0, "d_verified": 0}
ann = annotate_historical(row)
check("T10a history-preserved", row["d_verified"] == 0 and "value_interpretation" not in row)
check("T10b placeholder-annotated",
      ann["value_interpretation"] == UNKNOWN and "HISTORICAL_PLACEHOLDER_ZERO" in ann["historical_annotation"])

# The exact gap case from the spec.
v = validate_receipt({"verification": "UNVERIFIED", "delta_v_actual": None, "d_verified": 0})
check("GAP unverified-null-actual-with-zero-verified-refused",
      not v["ok"]
      and NULL_ACTUAL_WITH_VERIFIED_VALUE in v["refusals"]
      and VERIFIED_VALUE_WITHOUT_VERIFICATION in v["refusals"])

# Baseline zero: self-comparison.
r = classify_zero(assessment_state="ASSESSED", baseline_self_compare=True, evidence_refs=["def"])
check("BASELINE self-comparison-zero", r["interpretation"] == BASELINE_ZERO)

# Unknown-family interpretations must not carry a verified value.
v = validate_receipt({"verification": "VERIFIED_PASS", "delta_v_actual": 3.0, "d_verified": 3.0,
                      "value_interpretation": UNKNOWN, "evidence_refs": ["e1"]})
check("R5 unknown-with-verified-value-refused",
      not v["ok"] and INTERPRETATION_VALUE_MISMATCH in v["refusals"])

# Null discipline audit: this module must be clean of null->0 coercions.
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "zero_value_law.py")).read()
findings = audit_null_discipline(src)
check("NULLDISC module-clean", findings == [], str(findings))

# A healthy verified receipt passes.
v = validate_receipt({"verification": "VERIFIED_PASS", "delta_v_predicted": 5.2,
                      "delta_v_actual": 5.0, "d_verified": 5.0,
                      "value_interpretation": PRACTICALLY_NEUTRAL,
                      "epsilon": EPS, "evidence_refs": ["e1"]})
check("HEALTHY verified-receipt-passes", v["ok"], str(v["refusals"]))

print("\n%d passed, %d failed" % (len(passed), len(failed)))
if failed:
    print("FAILED:", failed)
    sys.exit(1)
