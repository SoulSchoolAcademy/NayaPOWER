"""Tests: contamination checks + evaluation firewall rules."""
from ..contamination import (
    check_training_leakage, check_feedback_leakage, check_lineage_leakage,
    check_temporal_leakage, check_evaluator_contamination,
    run_all_contamination_checks,
)
from ..canary import FIREWALL_RULES, CANARY_FAMILIES


def test_training_leakage_detected():
    v = check_training_leakage(
        accessible_paths=("/repo/eval/ANS-001-answers.json", "/repo/kernel/x.py"),
        sealed_ids=("ANS-001",))
    assert not v.passed and "ANS-001" in v.detail


def test_training_leakage_clean():
    v = check_training_leakage(accessible_paths=("/repo/kernel/x.py",),
                               sealed_ids=("ANS-001",))
    assert v.passed


def test_feedback_leakage_bounded():
    v = check_feedback_leakage(feedback_rounds=3, max_detail_per_round=8)
    assert v.passed


def test_feedback_leakage_exceeded():
    v = check_feedback_leakage(feedback_rounds=20, max_detail_per_round=64)
    assert not v.passed


def test_lineage_leakage_shared_family():
    v = check_lineage_leakage(("fam-a", "fam-b", "fam-a"))
    assert not v.passed


def test_lineage_leakage_disjoint():
    v = check_lineage_leakage(("fam-a", "fam-b", "fam-c"))
    assert v.passed


def test_temporal_leakage_future_evidence():
    v = check_temporal_leakage(case_decision_time="2026-10-01T00:00:00Z",
                               newest_evidence_time="2026-10-10T00:00:00Z")
    assert not v.passed


def test_temporal_leakage_clean():
    v = check_temporal_leakage(case_decision_time="2026-10-10T00:00:00Z",
                               newest_evidence_time="2026-10-01T00:00:00Z")
    assert v.passed


def test_evaluator_contamination_exposed():
    v = check_evaluator_contamination(True, False, False)
    assert not v.passed


def test_evaluator_contamination_blind():
    v = check_evaluator_contamination(False, False, False)
    assert v.passed


def test_all_five_checks_run():
    verdicts = run_all_contamination_checks(
        accessible_paths=("/repo/kernel/x.py",), sealed_ids=("ANS-001",),
        feedback_rounds=2, max_detail_per_round=8,
        case_families=("fam-a", "fam-b"),
        case_decision_time="2026-10-10T00:00:00Z",
        newest_evidence_time="2026-10-01T00:00:00Z",
        reviewer_saw_builder_conclusion=False,
        reviewer_saw_prior_judgments=False, reviewer_knew_treatment=False)
    assert len(verdicts) == 5
    assert all(v.passed for v in verdicts)


def test_ten_canary_families_defined():
    assert len(CANARY_FAMILIES) == 10


def test_firewall_rules_present():
    assert len(FIREWALL_RULES) >= 5
    assert any("COMPROMISED" in r for r in FIREWALL_RULES)
