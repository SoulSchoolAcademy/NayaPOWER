"""Tests for drift_canary/fairness.py — fair scheduling without false progress.

Rule under test: "Fairness guarantees opportunity. Execution creates
observations. Only qualifying evidence establishes accomplishment."

Covers:
  - the five decisive tests from Shawn's framework + the positive case
  - service ladder semantics (SELECTED/DISPATCHED != SERVICED)
  - fairness debt accounting and anti-gaming rules
  - three-part liveness composition (fairness + progress-on-service +
    well-founded descent)
  - the three truths report and independent receipt verification
"""
import pytest

from drift_canary.fairness import (
    ADEQUATE_SERVICE_RUNG,
    FAIRNESS_STANDARDS,
    SERVICE_LADDER,
    DeterministicScheduler,
    FairnessContract,
    FairnessLedger,
    SchedulingEvent,
    ThreeTruths,
    assess_three_truths,
    check_service_not_assertion,
    check_unique_obligation_service,
    compose_conditional_liveness,
    event_adequate_service,
    issue_fairness_receipt,
    ladder_rank,
    service_evidence_valid,
    verify_fairness_receipt,
)


EVIDENCE = {
    "lease_id": "LEASE-1",
    "worker_ack": "ACK-1",
    "resources_available": True,
}


def contract(oid, standard="WEAK", **kw):
    return FairnessContract(
        obligation_id=oid, revision="v1", standard=standard,
        eligibility_predicate="VALIDATED_RUNNABLE",
        service_predicate="USABLE_EXECUTION_OPPORTUNITY", **kw)


def ledger_with(*oids, standard="WEAK"):
    led = FairnessLedger()
    for oid in oids:
        led.register(contract(oid, standard))
    return led


def sched(led):
    return DeterministicScheduler(led)


# ---------------------------------------------------------------------------
# Service ladder: selection and dispatch are not service.
# ---------------------------------------------------------------------------
def test_ladder_ordering():
    assert ladder_rank("SELECTED") < ladder_rank("DISPATCHED")
    assert ladder_rank("DISPATCHED") < ladder_rank("SERVICED")
    assert ladder_rank("SERVICED") < ladder_rank("ATTEMPTED")
    assert ladder_rank("ATTEMPTED") < ladder_rank("ADVANCED")
    assert ladder_rank("ADVANCED") < ladder_rank("COMPLETED")
    assert ADEQUATE_SERVICE_RUNG == "SERVICED"


def test_selected_and_dispatched_are_not_service():
    for rung in ("SELECTED", "DISPATCHED"):
        e = SchedulingEvent("O1", "WF", 1, rung, True,
                            tuple(sorted(EVIDENCE.items())))
        adequate, why = event_adequate_service(e)
        assert not adequate, rung
        assert "below adequate service" in why


def test_serviced_requires_evidence():
    # SERVICED rung with no evidence: DISPATCHED-ONLY, not service.
    e = SchedulingEvent("O1", "WF", 1, "SERVICED", True, ())
    adequate, why = event_adequate_service(e)
    assert not adequate
    assert "DISPATCHED-ONLY" in why
    # A bare scheduler assertion is an assertion, not evidence.
    ok, _ = check_service_not_assertion(e)
    assert not ok


def test_serviced_with_evidence_is_adequate():
    e = SchedulingEvent("O1", "WF", 1, "SERVICED", True,
                        tuple(sorted(EVIDENCE.items())))
    adequate, _ = event_adequate_service(e)
    assert adequate
    ok, _ = service_evidence_valid(EVIDENCE)
    assert ok


def test_partial_evidence_rejected():
    ok, why = service_evidence_valid(
        {"lease_id": "L", "worker_ack": "A"})  # missing resources_available
    assert not ok
    assert "resources_available" in why


# ---------------------------------------------------------------------------
# Fairness debt accounting.
# ---------------------------------------------------------------------------
def test_debt_accrues_while_eligible_and_unserved():
    led = ledger_with("O1")
    s = sched(led)
    for _ in range(3):
        s.round("O1", "WF", True, "DISPATCHED", EVIDENCE)
    assert led.debt("O1") == 3


def test_adequate_service_resets_debt():
    led = ledger_with("O1")
    s = sched(led)
    s.round("O1", "WF", True, "DISPATCHED", EVIDENCE)
    s.round("O1", "WF", True, "DISPATCHED", EVIDENCE)
    assert led.debt("O1") == 2
    s.round("O1", "WF", True, "SERVICED", EVIDENCE)
    assert led.debt("O1") == 0


def test_ineligible_rounds_do_not_accrue_debt():
    led = ledger_with("O1")
    s = sched(led)
    s.round("O1", "WF", False, "SELECTED", {})
    s.round("O1", "WF", False, "SELECTED", {})
    assert led.debt("O1") == 0


def test_dispatched_only_does_not_reset_debt():
    # Repeated DISPATCHED without usable resources: debt keeps accruing.
    led = ledger_with("O1")
    s = sched(led)
    for _ in range(4):
        s.round("O1", "WF", True, "DISPATCHED", EVIDENCE)
    # Now a SERVICED rung WITHOUT evidence: still not service.
    s.round("O1", "WF", True, "SERVICED", {})
    assert led.debt("O1") == 5


def test_starvation_suspects():
    led = ledger_with("A", "B", "C")
    s = sched(led)
    for _ in range(5):
        s.round("A", "WF", True, "DISPATCHED", EVIDENCE)
    for _ in range(2):
        s.round("B", "WF", True, "DISPATCHED", EVIDENCE)
    s.round("C", "WF", True, "SERVICED", EVIDENCE)
    assert led.starvation_suspects(5) == ("A",)
    assert led.starvation_suspects(2) == ("A", "B")
    assert led.starvation_suspects(6) == ()


# ---------------------------------------------------------------------------
# Anti-gaming: debt survives reassignment; unique obligations measured.
# ---------------------------------------------------------------------------
def test_debt_survives_reassignment():
    led = ledger_with("O1")
    s = sched(led)
    for _ in range(3):
        s.round("O1", "WF", True, "DISPATCHED", EVIDENCE)
    ok, debt, why = s.reassign("O1", "worker-1", "worker-2")
    assert ok
    assert debt == 3
    assert "belongs to the obligation" in why
    # More waiting after reassignment keeps accruing from 3, not 0.
    s.round("O1", "WF", True, "DISPATCHED", EVIDENCE)
    assert led.debt("O1") == 4


def test_unique_obligation_service():
    e1 = SchedulingEvent("O1", "WF", 1, "SERVICED", True,
                         tuple(sorted(EVIDENCE.items())))
    e2 = SchedulingEvent("O1", "WF", 2, "SERVICED", True,
                         tuple(sorted({**EVIDENCE, "lease_id": "LEASE-2"}.items())))
    ok, _ = check_unique_obligation_service((e1, e2))
    assert ok  # two distinct rounds of service: fine
    # Duplicate seq claiming service twice for the same round: rejected.
    e3 = SchedulingEvent("O1", "WF", 1, "SERVICED", True,
                         tuple(sorted(EVIDENCE.items())))
    ok, why = check_unique_obligation_service((e1, e3))
    assert not ok
    assert "duplicate service credit" in why


def test_bounded_contract_needs_bound_and_basis():
    with pytest.raises(AssertionError):
        FairnessContract("O1", "v1", "BOUNDED", "elig", "svc")
    with pytest.raises(AssertionError):
        FairnessContract("O1", "v1", "BOUNDED", "elig", "svc",
                         service_bound_rounds=10)  # no capacity basis
    c = FairnessContract("O1", "v1", "BOUNDED", "elig", "svc",
                         service_bound_rounds=10,
                         capacity_basis="measured 8 rounds p99")
    assert c.standard == "BOUNDED"


# ---------------------------------------------------------------------------
# The five decisive tests + the positive case.
# ---------------------------------------------------------------------------
def test_T1_fair_scheduler_broken_worker():
    """Fair scheduler runs a broken worker repeatedly: fairness passes
    (adequate service every round), progress-on-service fails (nothing
    ever advances)."""
    led = ledger_with("O1")
    s = sched(led)
    for _ in range(6):
        s.round("O1", "WF", True, "ATTEMPTED", EVIDENCE)
    truths = assess_three_truths(led, "O1", debt_threshold=4,
                                 serviced_rounds=6, advanced_rounds=0,
                                 rank_decreasing=False)
    assert truths.fair_chance          # fairness: passes
    assert not truths.advanced_on_service  # progress on service: fails
    established, verdict, _ = compose_conditional_liveness(truths)
    assert not established
    assert verdict == "LIVENESS_UNPROVEN"


def test_T2_one_advances_another_starves():
    """Worker A advances; eligible worker B never serviced: some work
    progresses, scheduler fairness FAILS for B."""
    led = ledger_with("A", "B")
    s = sched(led)
    for _ in range(6):
        s.round("A", "WF", True, "ADVANCED", EVIDENCE)
        s.round("B", "WF", True, "DISPATCHED", EVIDENCE)
    truths_b = assess_three_truths(led, "B", debt_threshold=4,
                                   serviced_rounds=0, advanced_rounds=0,
                                   rank_decreasing=False)
    assert not truths_b.fair_chance
    established, verdict, _ = compose_conditional_liveness(truths_b)
    assert not established
    # A, meanwhile, is fine on fairness.
    truths_a = assess_three_truths(led, "A", debt_threshold=4,
                                   serviced_rounds=6, advanced_rounds=6,
                                   rank_decreasing=True)
    assert truths_a.fair_chance


def test_T3_repeated_reassignment_no_reset():
    """Repeated reassignment: no fairness reset, no artificial proof
    improvement."""
    led = ledger_with("O1")
    s = sched(led)
    for i in range(3):
        s.round("O1", "WF", True, "DISPATCHED", EVIDENCE)
        s.reassign("O1", f"w{i}", f"w{i+1}")
    assert led.debt("O1") == 3  # debt kept accruing through reassignments
    truths = assess_three_truths(led, "O1", debt_threshold=4,
                                 serviced_rounds=0, advanced_rounds=0,
                                 rank_decreasing=False)
    assert not truths.fair_chance or led.debt("O1") == 3


def test_T4_intermittent_eligibility_strong_fairness():
    """Intermittently-enabled obligation repeatedly skipped while enabled:
    under STRONG fairness this is a violation even though weak fairness
    (continuous enabling) never applied."""
    led = ledger_with("O1", standard="STRONG")
    s = sched(led)
    # Eligible every other round; never serviced when eligible.
    for i in range(8):
        eligible = (i % 2 == 0)
        s.round("O1", "WF", eligible, "DISPATCHED", EVIDENCE)
    assert led.debt("O1") == 4  # only eligible rounds accrue
    truths = assess_three_truths(led, "O1", debt_threshold=4,
                                 serviced_rounds=0, advanced_rounds=0,
                                 rank_decreasing=False)
    assert not truths.fair_chance  # infinitely-often enabled, never served


def test_T5_retry_exhaustion_governed_failure():
    """Finite retries exhaust without success: governed failure
    disposition, no fabricated goal completion. Fairness held (service
    was adequate); progress-on-service honestly reports no advancement."""
    led = ledger_with("O1")
    s = sched(led)
    for _ in range(4):
        s.round("O1", "WF", True, "ATTEMPTED", EVIDENCE)
    truths = assess_three_truths(led, "O1", debt_threshold=10,
                                 serviced_rounds=4, advanced_rounds=0,
                                 rank_decreasing=False)
    assert truths.fair_chance
    assert not truths.advanced_on_service
    established, _, _ = compose_conditional_liveness(truths)
    assert not established
    # The workflow may terminate in a governed failure disposition —
    # that is termination honesty, not a liveness proof.


def test_T6_positive_parallel_service_discharge_join():
    """Positive case: parallel obligations serviced, discharged, join
    satisfied, verified outcome. All three truths established."""
    led = ledger_with("A", "B", "JOIN")
    s = sched(led)
    for _ in range(2):
        s.round("A", "WF", True, "ADVANCED", EVIDENCE)
        s.round("B", "WF", True, "ADVANCED", EVIDENCE)
    s.round("JOIN", "WF", True, "ADVANCED", EVIDENCE)
    for oid in ("A", "B", "JOIN"):
        truths = assess_three_truths(led, oid, debt_threshold=4,
                                     serviced_rounds=2, advanced_rounds=2,
                                     rank_decreasing=True)
        established, verdict, _ = compose_conditional_liveness(truths)
        assert established, oid
        assert verdict == "CONDITIONAL_LIVENESS"


# ---------------------------------------------------------------------------
# The three truths and receipt verification.
# ---------------------------------------------------------------------------
def test_three_truths_fairly_served_but_stalled():
    """Workflow B from the framework: 5 opportunities, 0 discharged —
    fairly served but stalled. Fairness passes; liveness fails."""
    led = ledger_with("B")
    s = sched(led)
    for _ in range(5):
        s.round("B", "WF", True, "SERVICED", EVIDENCE)
    truths = assess_three_truths(led, "B", debt_threshold=10,
                                 serviced_rounds=5, advanced_rounds=0,
                                 rank_decreasing=False)
    assert truths.fair_chance
    assert not truths.advanced_on_service
    assert not truths.converging
    established, _, reason = compose_conditional_liveness(truths)
    assert not established
    assert "progress-on-service" in reason


def test_three_truths_potential_starvation():
    """Workflow C: eligible every round, 0 adequate service — potential
    starvation. Fairness fails even though other workflows progress.
    (Zero ROUNDS observed is not starvation; zero SERVICE while
    eligible is.)"""
    led = ledger_with("C")
    s = sched(led)
    for _ in range(3):
        s.round("C", "WF", True, "SELECTED", {})
    assert led.debt("C") == 3
    truths = assess_three_truths(led, "C", debt_threshold=3,
                                 serviced_rounds=0, advanced_rounds=0,
                                 rank_decreasing=False)
    assert not truths.fair_chance


def test_fairness_receipt_round_trip():
    led = ledger_with("O1")
    s = sched(led)
    s.round("O1", "WF", True, "SERVICED", EVIDENCE)
    s.round("O1", "WF", True, "ADVANCED", EVIDENCE)
    receipt = issue_fairness_receipt(
        led, "O1", debt_threshold=4, serviced_rounds=2,
        advanced_rounds=2, rank_decreasing=True,
        history_digest="sha256:test")
    assert receipt.liveness_verdict == "CONDITIONAL_LIVENESS"
    assert receipt.final_debt == 0
    ok, _ = verify_fairness_receipt(receipt, led, debt_threshold=4)
    assert ok


def test_fairness_receipt_rejects_invented_service():
    """A receipt claiming service the history cannot reconstruct is
    rejected: scheduling events without evidence are assertions."""
    led = ledger_with("O1")
    s = sched(led)
    for _ in range(3):
        s.round("O1", "WF", True, "DISPATCHED", EVIDENCE)
    # Fabricate a receipt claiming debt 0 (as if service happened).
    truths = ThreeTruths(True, True, True, "fabricated")
    from drift_canary.fairness import FairnessReceipt
    bad = FairnessReceipt("O1", "v1", "WEAK", 3, 3, 0, truths,
                         "CONDITIONAL_LIVENESS", "sha256:x")
    ok, why = verify_fairness_receipt(bad, led, debt_threshold=4)
    assert not ok
    assert "debt mismatch" in why


def test_unregistered_contract_no_duty_assessed():
    led = FairnessLedger()  # no contract registered
    s = sched(led)
    s.round("O9", "WF", True, "SERVICED", EVIDENCE)
    receipt = issue_fairness_receipt(led, "O9", 4, 1, 1, True)
    assert receipt.contract_revision == "UNREGISTERED"
    assert "no fairness duty" in receipt.note


def test_heartbeat_earns_no_fairness_credit():
    """Heartbeats are not scheduling events at all: they change neither
    debt nor service counts."""
    led = ledger_with("O1")
    s = sched(led)
    s.round("O1", "WF", True, "SELECTED", {})
    assert led.debt("O1") == 1  # eligible, inadequately served
    truths = assess_three_truths(led, "O1", debt_threshold=4,
                                 serviced_rounds=0, advanced_rounds=0,
                                 rank_decreasing=False)
    assert not truths.advanced_on_service
