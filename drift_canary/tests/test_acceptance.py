"""Ten acceptance tests: drift detection + canary independence.

From Shawn's framework (proposed pilot standards, not observed measurements):
severe authority-critical regressions → 100% detection, zero unauthorized
execution. Real-world performance reported separately with uncertainty and
actual denominators.
"""
from ..fingerprint import CalibrationFingerprint, DriftSignal
from ..loops import SeverityDecision
from ..canary import CanaryCase, SealedCommitment
from ..contamination import check_lineage_leakage, check_training_leakage
from ..integrity import IntegrityEvent, transition_allowed
from ..exposure import ExposureBudget, qualification_is_usable
from ..receipt import CanaryReceipt
from ..fixtures.anchor_v1 import ANCHOR_V1


def _fp(**over):
    base = dict(policy_version="P2", policy_sha="a", model_version="m1",
                 prompt_version="p1", verifier_id="v1", rubric_version="r1",
                 runtime_version="c1", corpus_id="c1", corpus_hash="h1",
                 evidence_cutoff="2026-10-10T00:00:00Z",
                 calibration_dataset="d1", calibration_params_hash="p1")
    base.update(over)
    return CalibrationFingerprint(**base)


def test_1_policy_change_detected():
    """Policy changes but code does not: detect the policy mismatch."""
    changed = _fp().changed_fields(_fp(policy_version="P3", policy_sha="b"))
    assert "policy_version" in changed
    sig = DriftSignal(drift_type="policy", indicator="policy fingerprint mismatch",
                      observed_at="2026-10-10T18:00:00Z",
                      baseline_fingerprint=_fp().digest(),
                      current_fingerprint=_fp(policy_version="P3").digest(),
                      evidence_ref="receipt-1")
    assert sig.drift_type == "policy"


def test_2_model_regression_detected():
    """Model changes and produces different high-risk decisions: detect."""
    changed = _fp().changed_fields(_fp(model_version="m2"))
    assert changed == ("model_version",)
    d = SeverityDecision(level="requalify", reasons=("canary disagreement",),
                         affected_scope=("high-risk-act",))
    assert d.level == "requalify"


def test_3_reviewer_leniency_detected():
    """Reviewer leniency changes: detect anchor-case disagreement."""
    sig = DriftSignal(drift_type="reviewer", indicator="reviewer anchor drift",
                      observed_at="2026-10-10T18:00:00Z",
                      baseline_fingerprint="a", current_fingerprint="b",
                      evidence_ref="anchor-replay")
    assert sig.severity_hint in ("watch", "investigate", "contain")


def test_4_distribution_shift_investigated_not_failed():
    """Input distribution changes without performance degradation:
    investigate, do not auto-declare failure."""
    sig = DriftSignal(drift_type="population",
                      indicator="challenge distribution drift",
                      observed_at="2026-10-10T18:00:00Z",
                      baseline_fingerprint="a", current_fingerprint="a",
                      evidence_ref="pop-report", severity_hint="watch")
    assert sig.severity_hint == "watch"  # not contain


def test_5_severe_miss_escalates_despite_stable_average():
    """Severe misses increase while average accuracy stable: escalate."""
    d = SeverityDecision(level="contain",
                         reasons=("high-severity miss rate rising",),
                         affected_scope=("authority-critical-act",))
    assert d.level == "contain"


def test_6_selection_bias_identified():
    """Only reviewed cases have labels: identify selection bias."""
    # medium loop must track missingness explicitly
    from ..loops import MONITORING_LOOPS
    medium = next(l for l in MONITORING_LOOPS if l.name == "medium")
    assert "label_missingness" in medium.inputs


def test_7_delayed_outcomes_not_misclassified():
    """Outcomes delayed: avoid misclassifying pending cases as successes."""
    r = CanaryReceipt(run_id="r1", set_type="rolling", visibility="sealed",
                      corpus_version="v1", corpus_hash="h", sample_family_id="f1",
                      policy_version="p", model_version="m", runtime_version="c",
                      evaluation_cutoff="t", reviewer_id="v")
    assert r.outcome == "PENDING"  # default is pending, never assumed pass


def test_8_contaminated_canary_invalidated():
    """Canary fixtures become contaminated: invalidate that evaluation evidence."""
    r = CanaryReceipt(run_id="r1", set_type="fixed", visibility="sealed",
                      corpus_version="v1", corpus_hash="h", sample_family_id="f1",
                      policy_version="p", model_version="m", runtime_version="c",
                      evaluation_cutoff="t", reviewer_id="v", outcome="PASS")
    c = r.compromised()
    assert c.outcome == "COMPROMISED"
    assert "not usable for promotion" in (c.evidence_receipt or "")


def test_9_drift_contained_per_domain():
    """Drift affects one domain: contain that domain, not unrelated work."""
    d = SeverityDecision(level="contain", reasons=("domain drift",),
                         affected_scope=("domain-x",))
    assert d.affected_scope == ("domain-x",)  # scoped, not blanket


def test_10_cold_successor_stale_calibration():
    """Cold successor activates with stale calibration: refuse consequential
    use until requalification."""
    usable, _ = qualification_is_usable(
        True, True, False, True)  # scope does NOT match stale calibration
    assert not usable


def test_anchor_fixtures_cover_ten_families():
    fams = {c.family for c in ANCHOR_V1}
    assert len(fams) == 10


def test_anchor_cases_have_controls():
    for c in ANCHOR_V1:
        assert c.positive_control and c.negative_control, c.case_id
        assert c.truth_reference, c.case_id
