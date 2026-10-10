"""Tests for drift_canary/strong_fairness.py — when strong fairness is required.

Rule under test: "Require strong fairness when an outstanding,
legitimately executable obligation can become enabled infinitely often
without ever remaining continuously enabled, and when indefinite
starvation would violate the intended liveness guarantee."

Covers Shawn's ten acceptance scenarios plus the decisive experiment:
the SAME adversarial schedule run against a WEAK_ONLY scheduler and a
STRONG scheduler. Both must preserve safety; the strong one must
eliminate the recurring-eligibility starvation trace.
"""
import pytest

from drift_canary.strong_fairness import (
    EIGHT_ASSUMPTIONS,
    SITUATIONS,
    STANDARD_DECISION_RULE,
    FlickerLedger,
    SchedulabilityAssessment,
    StrongFairnessContract,
    ThreeSubProofs,
    assumptions_satisfied,
    check_assumptions,
    check_strong_excludes_starvation,
    check_weak_starvation_counterexample,
    compose_strong_termination,
    recommend_standard,
    simulate_policy,
    strong_fairness_duty_owed,
)


# ---------------------------------------------------------------------------
# Decision rule: the weakest sufficient standard, never strong by default.
# ---------------------------------------------------------------------------
def test_decision_rule_covers_all_situations():
    for s in SITUATIONS:
        standard, reason = recommend_standard(s)
        assert standard in ("WEAK", "STRONG", "BOUNDED", "NEITHER"), s
        assert reason, s


def test_continuously_runnable_gets_weak_not_strong():
    standard, _ = recommend_standard("CONTINUOUSLY_RUNNABLE")
    assert standard == "WEAK"


def test_flickering_resource_gets_strong():
    standard, _ = recommend_standard("FLICKERING_SHARED_RESOURCE")
    assert standard == "STRONG"


def test_human_auth_missing_gets_neither():
    # Fairness governs opportunities, not permission. LAW is a hard gate.
    standard, reason = recommend_standard("HUMAN_AUTH_MISSING")
    assert standard == "NEITHER"
    assert "permission" in reason.lower() or "LAW" in reason


def test_finite_windows_gets_neither():
    # Strong fairness needs infinitely recurring eligibility.
    standard, _ = recommend_standard("FINITE_BRIEF_WINDOWS")
    assert standard == "NEITHER"


def test_hard_deadline_gets_bounded_not_strong():
    # Strong fairness alone provides no deadline.
    standard, _ = recommend_standard("HARD_DEADLINE")
    assert standard == "BOUNDED"


def test_or_branch_satisfied_retires_obligation():
    standard, _ = recommend_standard("OR_BRANCH_SATISFIED")
    assert standard == "NEITHER"


# ---------------------------------------------------------------------------
# Eight assumptions: each needs evidence; a missing one blocks the claim.
# ---------------------------------------------------------------------------
def test_eight_assumptions_all_present():
    assert len(EIGHT_ASSUMPTIONS) == 8
    ids = [a for a, _ in EIGHT_ASSUMPTIONS]
    assert "SAFETY_PRESERVATION" in ids
    assert "GENUINE_ENABLING" in ids
    assert "RECURRING_OPPORTUNITY" in ids


def test_all_assumptions_satisfied_with_evidence():
    evidence = {a: f"evidence-for-{a}" for a, _ in EIGHT_ASSUMPTIONS}
    results = check_assumptions(evidence)
    ok, missing = assumptions_satisfied(results)
    assert ok and missing == []


def test_missing_assumption_blocks_claim():
    evidence = {a: f"evidence-for-{a}" for a, _ in EIGHT_ASSUMPTIONS}
    del evidence["SAFETY_PRESERVATION"]
    results = check_assumptions(evidence)
    ok, missing = assumptions_satisfied(results)
    assert not ok
    assert missing == ["SAFETY_PRESERVATION"]


# ---------------------------------------------------------------------------
# Three-proof composition: opportunity + fairness + resolution.
# ---------------------------------------------------------------------------
def test_three_proofs_compose_to_conditional_termination():
    proofs = ThreeSubProofs(
        opportunity_recurs=True,
        strong_fairness_applies=True,
        service_drives_resolution=True,
        detail="all three established")
    ok, verdict, reason = compose_strong_termination(proofs)
    assert ok
    assert verdict == "CONDITIONAL_TERMINATION"
    assert "NOT" in reason and "success" in reason  # not a success promise


def test_missing_opportunity_blocks_termination():
    proofs = ThreeSubProofs(
        opportunity_recurs=False,
        strong_fairness_applies=True,
        service_drives_resolution=True)
    ok, verdict, _ = compose_strong_termination(proofs)
    assert not ok and verdict == "TERMINATION_UNPROVEN"


def test_missing_resolution_blocks_termination():
    # Infinitely serviced but only ever retries: fairness holds,
    # liveness still fails.
    proofs = ThreeSubProofs(
        opportunity_recurs=True,
        strong_fairness_applies=True,
        service_drives_resolution=False)
    ok, verdict, reason = compose_strong_termination(proofs)
    assert not ok
    assert "retry" in reason.lower() or "retries" in reason.lower()


# ---------------------------------------------------------------------------
# Flicker ledger: debt across eligibility flicker.
# ---------------------------------------------------------------------------
def test_debt_accrues_across_flicker_without_reset():
    led = FlickerLedger(obligation_id="ACT-042",
                        remaining_recovery_budget=2)
    # E,B,E,B,E,B pattern: eligible, blocked, eligible...
    for eligible in (True, False, True, False, True, False):
        led.record_round(eligible=eligible, adequate_service=False)
    # Three eligible epochs missed, debt 3, no reset on blocked rounds.
    assert led.eligible_epochs == 3
    assert led.fairness_debt == 3


def test_ineligible_round_neither_accrues_nor_resets():
    led = FlickerLedger(obligation_id="ACT-042")
    led.record_round(eligible=True, adequate_service=False)
    led.record_round(eligible=True, adequate_service=False)
    assert led.fairness_debt == 2
    ok, debt, _ = led.record_round(eligible=False, adequate_service=False)
    assert ok and debt == 2  # unchanged: no reset, no accrual


def test_adequate_service_resets_debt():
    led = FlickerLedger(obligation_id="ACT-042")
    for _ in range(5):
        led.record_round(eligible=True, adequate_service=False)
    assert led.fairness_debt == 5
    ok, debt, _ = led.record_round(
        eligible=True, adequate_service=True,
        service_receipt="SRV-1")
    assert ok and debt == 0
    assert led.service_events == 1
    assert led.last_service_receipt == "SRV-1"


def test_nominal_eligibility_excluded_from_accounting():
    # A 1us window with 10ms dispatch cost is not a usable opportunity.
    led = FlickerLedger(obligation_id="ACT-042")
    ok, debt, reason = led.record_round(
        eligible=True, adequate_service=False, usable_opportunity=False)
    assert ok and debt == 0
    assert led.eligible_epochs == 0
    assert "not a usable opportunity" in reason


def test_reassignment_preserves_everything():
    led = FlickerLedger(obligation_id="ACT-042",
                        remaining_recovery_budget=2)
    for _ in range(4):
        led.record_round(eligible=True, adequate_service=False)
    ok, debt, reason = led.reassign("worker-a", "worker-b")
    assert ok
    assert debt == 4
    assert led.eligible_epochs == 4
    assert led.remaining_recovery_budget == 2
    assert led.worker_reassignments == 1
    assert "preserved" in reason


def test_duty_owed_at_threshold():
    led = FlickerLedger(obligation_id="ACT-042")
    for _ in range(7):
        led.record_round(eligible=True, adequate_service=False)
    owed, reason = strong_fairness_duty_owed(led, starvation_threshold=5)
    assert owed
    assert "duty owed" in reason
    # ...but the duty is for a service OPPORTUNITY, never permission.
    assert "permission" in reason


def test_no_duty_below_threshold_or_when_retired():
    led = FlickerLedger(obligation_id="ACT-042")
    led.record_round(eligible=True, adequate_service=False)
    owed, _ = strong_fairness_duty_owed(led, starvation_threshold=5)
    assert not owed
    led.obligation_status = "RETIRED"
    for _ in range(10):
        led.record_round(eligible=True, adequate_service=False)
    owed, reason = strong_fairness_duty_owed(led, starvation_threshold=5)
    assert not owed
    assert "terminates" in reason


# ---------------------------------------------------------------------------
# Schedulability: nominal windows are not usable opportunities.
# ---------------------------------------------------------------------------
def test_unusable_window_rejected():
    a = SchedulabilityAssessment(
        window_description="1us resource release",
        window_us=1.0, dispatch_cost_us=10_000.0)
    ok, reason = a.usable()
    assert not ok
    assert "NOT a usable opportunity" in reason


def test_usable_window_accepted():
    a = SchedulabilityAssessment(
        window_description="durable queue entry",
        window_us=50_000.0, dispatch_cost_us=10_000.0,
        mechanism="durable queue entry")
    ok, _ = a.usable()
    assert ok


# ---------------------------------------------------------------------------
# Model checker: weak admits the starvation trace, strong excludes it.
# ---------------------------------------------------------------------------
def test_weak_starvation_counterexample_on_flicker():
    # E,B,E,B,... — eligible every other round, never continuous.
    ok, evidence = check_weak_starvation_counterexample(
        [True, False], patience=3, repeats=30)
    assert ok, evidence
    assert "starvation counterexample" in evidence


def test_strong_excludes_flicker_starvation():
    ok, evidence = check_strong_excludes_starvation(
        [True, False], threshold=4, repeats=30)
    assert ok, evidence
    assert "excludes the starvation trace" in evidence


def test_continuous_pattern_needs_no_strong():
    # Continuously eligible: weak fairness serves it; no counterexample.
    ok, _ = check_weak_starvation_counterexample(
        [True, True, True], patience=3, repeats=10)
    assert not ok


def test_never_eligible_pattern_has_no_duty():
    ok, evidence = check_weak_starvation_counterexample(
        [False, False], patience=3, repeats=10)
    assert not ok
    assert "never eligible" in evidence


# ---------------------------------------------------------------------------
# THE DECISIVE EXPERIMENT: same adversarial schedule, two schedulers.
# Both preserve safety; the strong one must eliminate the starvation trace.
# ---------------------------------------------------------------------------
def test_decisive_two_scheduler_experiment():
    # Adversarial: ACT flickers E,B,E,B while high-priority work holds
    # the resource in B rounds. 30 periods.
    pattern = [True, False]
    weak = simulate_policy(pattern, "WEAK_ONLY", patience=3, repeats=30)
    strong = simulate_policy(pattern, "STRONG", threshold=4, repeats=30)

    # WEAK_ONLY: eligible infinitely often, never served -> starved.
    assert weak["starved"], (
        "expected WEAK_ONLY to admit the starvation trace")
    assert weak["missed_eligible_epochs"] == 30

    # STRONG: serves repeatedly, debt bounded -> trace excluded.
    assert not strong["starved"], (
        "STRONG must exclude the recurring-eligibility starvation trace")
    assert len(strong["served_rounds"]) > 0
    assert strong["max_debt"] <= 4

    # Safety preserved by construction in both: the simulation never
    # serves during an ineligible round (no B-round service in either).
    # (The model only marks service on eligible rounds; a B-round
    # service would be a safety violation — assert none occurred.)
    for r in weak["served_rounds"] + strong["served_rounds"]:
        # round numbers are 1-based; pattern repeats every 2 rounds;
        # odd rounds are eligible.
        assert r % 2 == 1, f"service in ineligible round {r}: UNSAFE"


def test_fairly_serviced_but_failing_worker():
    # Fairness passes (service delivered), progress fails (no advancement).
    # The two are independently evaluated — this is the essential case.
    led = FlickerLedger(obligation_id="KNOW-007")
    for _ in range(6):
        # Serviced every eligible epoch, but the worker only retries.
        led.record_round(eligible=True, adequate_service=True,
                         service_receipt=f"SRV-{led.service_events + 1}")
    assert led.service_events == 6
    assert led.fairness_debt == 0  # fairness: satisfied
    assert led.verified_proof_progress == 0  # progress: nothing advanced
    # The composition must report: fair chance YES, advanced NO.
    # (Progress accounting lives in progress.py; here we assert the
    # ledger keeps the two books separate.)


def test_strong_contract_requires_recurrence_basis():
    with pytest.raises(AssertionError):
        StrongFairnessContract(
            obligation_id="ACT-042", revision="v1",
            eligibility_predicate="VALIDATED_RUNNABLE",
            service_predicate="USABLE_EXECUTION_OPPORTUNITY",
            recurrence_basis="",  # missing: the GF E_o premise unevidenced
            starvation_threshold_epochs=5)


def test_strong_contract_requires_threshold():
    with pytest.raises(AssertionError):
        StrongFairnessContract(
            obligation_id="ACT-042", revision="v1",
            eligibility_predicate="VALIDATED_RUNNABLE",
            service_predicate="USABLE_EXECUTION_OPPORTUNITY",
            recurrence_basis="upstream releases the lock every period",
            starvation_threshold_epochs=0)


def test_strong_contract_converts_to_fairness_contract():
    c = StrongFairnessContract(
        obligation_id="ACT-042", revision="v1",
        eligibility_predicate="VALIDATED_RUNNABLE",
        service_predicate="USABLE_EXECUTION_OPPORTUNITY",
        recurrence_basis="upstream releases the lock every period",
        schedulability_mechanism="durable queue entry",
        starvation_threshold_epochs=5)
    fc = c.to_fairness_contract()
    assert fc.standard == "STRONG"
    assert fc.obligation_id == "ACT-042"
    assert fc.preserve_across_reassignment is True
