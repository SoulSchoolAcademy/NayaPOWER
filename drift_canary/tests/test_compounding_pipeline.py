"""Tests for the compounding intelligence pipeline.

Encodes Shawn's canonical diagrams as executable specs:
- The_compounding_process.svg: 10 stages
- Experiment outcomes chart: correct > control > wrong
- process_smart_flow.svg: independent observation required
- Process_flow.svg: self-reinforcing error guard
"""
import sys
sys.path.insert(0, "drift_canary")

from compounding_pipeline import (
    EvidenceFamily,
    ExperimentArms,
    MeasureVerdict,
    PipelineState,
    ProofReceipt,
    Stage,
    measure_lesson,
    run_pipeline,
    self_reinforcing_error_guard,
    verify_independent,
)


def test_shawn_chart_ordering():
    """Shawn's experiment chart: correct (88%) > control (65%) > wrong (60%)."""
    arms = ExperimentArms(control_rate=0.65, treatment_rate=0.88, wrong_lesson_rate=0.60)
    assert measure_lesson(arms) == MeasureVerdict.LESSON_IMPROVES


def test_wrong_lesson_beats_control_is_inconclusive():
    """If the wrong lesson outperforms control, the data is suspect."""
    arms = ExperimentArms(control_rate=0.60, treatment_rate=0.65, wrong_lesson_rate=0.80)
    assert measure_lesson(arms) == MeasureVerdict.INCONCLUSIVE


def test_harmful_lesson_blocked():
    """A lesson that degrades below control must not promote."""
    arms = ExperimentArms(control_rate=0.65, treatment_rate=0.50, wrong_lesson_rate=0.40)
    assert measure_lesson(arms) == MeasureVerdict.LESSON_HARMS


def test_neutral_lesson_not_promoted():
    """No meaningful separation → neutral, not promoted."""
    arms = ExperimentArms(control_rate=0.65, treatment_rate=0.66, wrong_lesson_rate=0.64)
    assert measure_lesson(arms) == MeasureVerdict.LESSON_NEUTRAL


def test_invalid_rates_inconclusive():
    """Rates outside [0,1] are invalid input, not evidence."""
    arms = ExperimentArms(control_rate=1.5, treatment_rate=0.88, wrong_lesson_rate=0.60)
    assert measure_lesson(arms) == MeasureVerdict.INCONCLUSIVE


def test_same_family_repetition_not_independent():
    """process_smart_flow.svg: Naya 2 + Naya 5 repeating claim A = one family."""
    evidence = [EvidenceFamily.SAME_FAMILY, EvidenceFamily.SAME_FAMILY]
    assert verify_independent(evidence) is False


def test_independent_observation_qualifies():
    """process_smart_flow.svg: observation B breaks the single-family trap."""
    evidence = [EvidenceFamily.SAME_FAMILY, EvidenceFamily.INDEPENDENT_OBSERVATION]
    assert verify_independent(evidence) is True


def test_self_reinforcing_error_guard_fires():
    """Process_flow.svg: repeated without independent evidence → block."""
    assert self_reinforcing_error_guard(repeat_count=3, independent_evidence=False) is True
    assert self_reinforcing_error_guard(repeat_count=3, independent_evidence=True) is False
    assert self_reinforcing_error_guard(repeat_count=1, independent_evidence=False) is False


def test_full_pipeline_promotes_good_lesson():
    """Happy path: all 10 stages, ends at COLD_REUSE."""
    arms = ExperimentArms(control_rate=0.65, treatment_rate=0.88, wrong_lesson_rate=0.60)
    evidence = [EvidenceFamily.INDEPENDENT_OBSERVATION]
    state, verdict = run_pipeline(arms, evidence)
    assert verdict == MeasureVerdict.LESSON_IMPROVES
    assert state.stage == Stage.COLD_REUSE
    assert state.blocked_reason is None
    assert len(state.history) == 9  # advanced through 9 transitions


def test_pipeline_blocks_on_self_reinforcement():
    """Pipeline blocks immediately on the error loop, before MEASURE."""
    arms = ExperimentArms(control_rate=0.65, treatment_rate=0.88, wrong_lesson_rate=0.60)
    state, verdict = run_pipeline(arms, [EvidenceFamily.SAME_FAMILY], repeat_count=5)
    assert verdict is None
    assert state.blocked_reason is not None
    assert "self-reinforcing" in state.blocked_reason


def test_pipeline_blocks_when_lesson_harms():
    """Pipeline blocks at MEASURE when treatment < control."""
    arms = ExperimentArms(control_rate=0.65, treatment_rate=0.50, wrong_lesson_rate=0.40)
    evidence = [EvidenceFamily.INDEPENDENT_OBSERVATION]
    state, verdict = run_pipeline(arms, evidence)
    assert verdict == MeasureVerdict.LESSON_HARMS
    assert state.stage == Stage.MEASURE
    assert state.blocked_reason is not None


def test_pipeline_blocks_without_independent_evidence():
    """Pipeline blocks at VERIFY on single-family evidence."""
    arms = ExperimentArms(control_rate=0.65, treatment_rate=0.88, wrong_lesson_rate=0.60)
    state, verdict = run_pipeline(arms, [EvidenceFamily.SAME_FAMILY])
    assert verdict == MeasureVerdict.LESSON_IMPROVES  # measure passed
    assert state.stage == Stage.VERIFY  # blocked here
    assert "independent" in state.blocked_reason


def test_proof_receipt_schema():
    """System Intelligence Review §8: interaction proof receipt fields."""
    r = ProofReceipt(
        interaction_id="INT-KNOW-LAW-ACT-001",
        participants=("KNOW", "LAW", "ACT"),
        invariant="learning_cannot_override_authority",
        preconditions=("lesson_applicable", "law_receipt_current"),
        environment_sha="exact-tested-sha",
        positive_test="RECEIPT-POS",
        negative_test="RECEIPT-NEG",
        independent_verification="PENDING",
    )
    assert r.qualification == "NOT_YET_ESTABLISHED"
    assert len(r.participants) == 3
