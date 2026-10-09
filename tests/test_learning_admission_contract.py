"""Admission contract tests — kernel/protocol/learning_capture.py.

Regression ground truth (2026-10-09): two independent agents agreed 0 of 13
analyzed learning candidates were verifiable as designed —
  * 1 definitional tautology ("applied the lesson" treatment arm),
  * 4 honest nulls (behavioral_change:false),
  * 5 non-experiments (NO_APPLICABLE_RETAINED_INTELLIGENCE both arms),
  * 3 definitional token changes (arms just emit different tokens).

The gate must REJECT all 13. Positive fixtures must PASS.
"""
import pytest

from kernel.protocol.learning_capture import (
    ADMISSION_RULES,
    AdmissionCandidate,
    RULE_DOER_SCORER,
    RULE_FALSIFIABLE,
    RULE_MEASUREMENT,
    RULE_NULL,
    RULE_PREREGISTERED,
    RULE_REPLICATION,
    RULE_SAME_TASK,
    check_admission,
    rule_falsifiable,
    rule_replication,
)

PRE = "2026-10-08T10:00:00+00:00"
RAN = "2026-10-08T12:00:00+00:00"
TASK = "NAYA-0001-PROVENANCE-HELDOUT-002"


def well_formed(**overrides):
    base = dict(
        claim=(
            "Applying the provenance-preservation lesson causes "
            "provenance_preserved=true on NAYA-0001-PROVENANCE-HELDOUT-002 "
            "(treatment) versus control."
        ),
        named_task_id=TASK,
        control_task_id=TASK,
        treatment_task_id=TASK,
        control_description="acted without applying the retained lesson",
        treatment_description="applied the retained lesson before acting",
        preregistered_criterion=(
            "treatment arm records provenance_preserved=true while control "
            "records false, per the machine receipt check"
        ),
        preregistered_at=PRE,
        arms_ran_at=RAN,
        measurement="machine",
        doer_seat="naya-2",
        scorer_seat="coda-1",
        outcome="positive",
        measured_capability_delta=True,
        replications_on_unseen_tasks=3,
    )
    base.update(overrides)
    return AdmissionCandidate(**base)


# ---------------------------------------------------------------------------
# Positive fixtures — well-formed candidates PASS
# ---------------------------------------------------------------------------

def test_positive_provenance_candidate_passes():
    result = check_admission(well_formed())
    assert result.passed is True
    assert result.failed_rules == []
    assert result.reasons == []


def test_positive_act_first_candidate_passes():
    task = "NAYA-0001-ACT-FIRST-HELDOUT-001"
    candidate = well_formed(
        claim=(
            "Applying the act-first lesson causes governed_autonomy_applied=true "
            "on NAYA-0001-ACT-FIRST-HELDOUT-001, scored deterministically."
        ),
        named_task_id=task,
        control_task_id=task,
        treatment_task_id=task,
        preregistered_criterion=(
            "treatment shows governed_autonomy_applied=true and control shows "
            "false on the machine-scored rubric"
        ),
        measurement="deterministic",
        doer_seat="naya-3",
        scorer_seat="naya-1",
        replications_on_unseen_tasks=5,
    )
    result = check_admission(candidate)
    assert result.passed is True
    assert result.failed_rules == []


# ---------------------------------------------------------------------------
# Ground truth 1/13: the definitional tautology
# ---------------------------------------------------------------------------

def test_tautology_rejected():
    candidate = well_formed(
        claim="Applying the retained lesson changes the agent's behavior.",
        named_task_id="",
        control_task_id="",
        treatment_task_id="",
        control_description="did not apply the retained lesson",
        treatment_description="applied the retained lesson",
    )
    result = check_admission(candidate)
    assert result.passed is False
    assert RULE_FALSIFIABLE in result.failed_rules
    assert any("tautology" in r for r in result.reasons)


def test_rule_falsifiable_names_tautology_directly():
    ok, reason = rule_falsifiable(
        well_formed(
            claim="Applying the retained lesson changes the agent's behavior.",
            named_task_id="",
            control_task_id="",
            treatment_task_id="",
            control_description="did not apply the retained lesson",
            treatment_description="applied the retained lesson",
        )
    )
    assert ok is False
    assert "tautology" in reason


# ---------------------------------------------------------------------------
# Ground truth 4/13: honest nulls — well-designed, null result
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("task", [
    "NAYA-0001-PROVENANCE-HELDOUT-003",
    "NAYA-0001-PROVENANCE-HELDOUT-004",
    "NAYA-0001-ACT-FIRST-HELDOUT-002",
    "NAYA-0001-ACTIVE-INTELLIGENCE-HELDOUT-003",
])
def test_honest_null_rejected_only_on_null_rule(task):
    candidate = well_formed(
        claim=(
            "Applying the retained lesson causes the measured capability on "
            "%s to improve (treatment) versus control." % task
        ),
        named_task_id=task,
        control_task_id=task,
        treatment_task_id=task,
        outcome="null",  # behavioral_change:false — honest null
        measured_capability_delta=False,
    )
    result = check_admission(candidate)
    assert result.passed is False
    # The design is otherwise sound: ONLY the null rule fires.
    assert result.failed_rules == [RULE_NULL]
    assert any("null" in r.lower() for r in result.reasons)


# ---------------------------------------------------------------------------
# Ground truth 5/13: non-experiments — NO_APPLICABLE_RETAINED_INTELLIGENCE
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("n", [1, 2, 3, 4, 5])
def test_non_experiment_rejected(n):
    task = "TASK-NONEXP-%03d" % n
    candidate = well_formed(
        claim="Applying the retained lesson improves performance on %s." % task,
        named_task_id=task,
        control_task_id=task,
        treatment_task_id=task,
        control_description="NO_APPLICABLE_RETAINED_INTELLIGENCE",
        treatment_description="NO_APPLICABLE_RETAINED_INTELLIGENCE",
        arms_ran_at=None,  # no arms ever ran
        outcome="not_run",  # nothing was tested
        measured_capability_delta=False,
    )
    result = check_admission(candidate)
    assert result.passed is False
    assert RULE_NULL in result.failed_rules


# ---------------------------------------------------------------------------
# Ground truth 3/13: definitional token changes
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("n", [1, 2, 3])
def test_definitional_token_change_rejected(n):
    task = "TASK-TOKEN-%03d" % n
    candidate = well_formed(
        claim="The treatment arm emits different tokens than the control arm on %s." % task,
        named_task_id=task,
        control_task_id=task,
        treatment_task_id=task,
        measured_capability_delta=False,  # tokens differed; no capability delta
    )
    result = check_admission(candidate)
    assert result.passed is False
    assert RULE_FALSIFIABLE in result.failed_rules
    assert RULE_NULL in result.failed_rules


# ---------------------------------------------------------------------------
# Per-rule edge cases — each rule fires independently
# ---------------------------------------------------------------------------

def test_self_report_measurement_rejected():
    result = check_admission(well_formed(measurement="self_report"))
    assert result.passed is False
    assert result.failed_rules == [RULE_MEASUREMENT]


def test_doer_is_scorer_rejected():
    result = check_admission(well_formed(scorer_seat="naya-2"))
    assert result.passed is False
    assert result.failed_rules == [RULE_DOER_SCORER]


def test_criterion_written_after_arms_rejected():
    result = check_admission(well_formed(preregistered_at="2026-10-08T14:00:00+00:00"))
    assert result.passed is False
    assert result.failed_rules == [RULE_PREREGISTERED]


def test_criterion_restating_claim_rejected():
    candidate = well_formed()
    candidate.preregistered_criterion = candidate.claim
    result = check_admission(candidate)
    assert result.passed is False
    assert result.failed_rules == [RULE_PREREGISTERED]


def test_divergent_arm_tasks_rejected():
    result = check_admission(well_formed(treatment_task_id="SOME-OTHER-TASK"))
    assert result.passed is False
    assert result.failed_rules == [RULE_SAME_TASK]


def test_two_replications_rejected():
    result = check_admission(well_formed(replications_on_unseen_tasks=2))
    assert result.passed is False
    assert result.failed_rules == [RULE_REPLICATION]


def test_rule_replication_predicate_directly():
    ok, _ = rule_replication(well_formed(replications_on_unseen_tasks=3))
    assert ok is True
    ok, reason = rule_replication(well_formed(replications_on_unseen_tasks=2))
    assert ok is False
    assert "3 required" in reason


# ---------------------------------------------------------------------------
# Fail-closed default
# ---------------------------------------------------------------------------

def test_empty_candidate_fails_every_rule():
    result = check_admission(AdmissionCandidate())
    assert result.passed is False
    assert result.failed_rules == list(ADMISSION_RULES)


def test_malformed_bundle_rejected():
    for bad in (None, {}, {"claim": "x"}, "not-a-candidate"):
        result = check_admission(bad)
        assert result.passed is False
        assert result.failed_rules == list(ADMISSION_RULES)


def test_seven_rules_are_stable_ids():
    assert ADMISSION_RULES == (
        "falsifiable_claim",
        "same_named_task",
        "preregistered_criterion",
        "machine_measurement",
        "doer_scorer_separation",
        "null_not_verified",
        "replication_gate",
    )


# ---------------------------------------------------------------------------
# Lane separation — the human-director path is never gated
# ---------------------------------------------------------------------------

def test_human_director_lane_bypasses_explicitly():
    result = check_admission(AdmissionCandidate(capture_path="human_director"))
    assert result.passed is True
    assert result.bypassed is True
    assert result.failed_rules == []


def test_human_director_bypass_is_case_insensitive():
    result = check_admission(AdmissionCandidate(capture_path="Human_Director"))
    assert result.passed is True
    assert result.bypassed is True
