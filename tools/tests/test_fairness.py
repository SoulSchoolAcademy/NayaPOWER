#!/usr/bin/env python3
"""Tests for the Fairness & Liveness gate — Group 5 (Fairness & Liveness), D58-D65.

Every test uses REAL asserts. The negative-control test (test_19) sabotages
the classifier to always pass and asserts the starvation test then FAILS —
proving the suite is not theater. If sabotage does not break the test, the
test is vacuous and must be rewritten, never weakened.
"""

import json
import os
import sys
import tempfile

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fairness_eligibility import (
    EligibilityProver,
    PredicateRegistry,
    WorkItem,
    VERDICT_LEVELS,
    _pred_evidence_key_true,
)
from fairness_debt import FairnessDebtLedger, MISSING_EVIDENCE_WIDEN_FACTOR
from fairness_invariants import (
    classify_cycle,
    SchedulerHarness,
    RoundRobinScheduler,
    WeakFairnessBreakingScheduler,
    StrongFairnessBreakingScheduler,
    NoProgressScheduler,
    WorkloadItem,
    InvariantChecker,
    TickLedger,
    LiveTraceReader,
    MergeLivenessTracker,
    PRRecord,
    DIAGNOSTICS,
)


def _registry():
    reg = PredicateRegistry()
    reg.register("has_approval", _pred_evidence_key_true("approval"))
    reg.register("tests_green", _pred_evidence_key_true("tests_green"))
    return reg


def _always_enabled(tick):
    return True


def _intermittent(tick):
    return tick % 2 == 0


# ---------------------------------------------------------------------------
# Eligibility prover (D26 Link 1)
# ---------------------------------------------------------------------------

def test_01_eligible_item_proven_eligible_with_evidence():
    prover = EligibilityProver(_registry())
    item = WorkItem("w1", ["has_approval", "tests_green"])
    v = prover.prove(item, {"approval": True, "tests_green": True}, "win-1")
    assert v.eligible is True
    assert v.missing == []
    assert v.verdict_level in VERDICT_LEVELS


def test_02_ineligible_item_names_missing_requirement():
    prover = EligibilityProver(_registry())
    item = WorkItem("w2", ["has_approval", "tests_green"])
    v = prover.prove(item, {"approval": True}, "win-1")
    assert v.eligible is False
    assert v.missing == ["tests_green"]


def test_03_prover_overrides_scheduler_claim_from_evidence():
    """Independence: scheduler claims eligible, evidence says otherwise."""
    prover = EligibilityProver(_registry())
    item = WorkItem("w3", ["has_approval"], scheduler_claim=True)
    v = prover.prove(item, {}, "win-1")  # no approval in evidence
    assert v.eligible is False
    assert v.claim_contradicted is True


def test_04_prover_overrides_false_negative_claim():
    """Independence, other direction: scheduler claims ineligible, evidence proves eligible."""
    prover = EligibilityProver(_registry())
    item = WorkItem("w4", ["has_approval"], scheduler_claim=False)
    v = prover.prove(item, {"approval": "signed-off"}, "win-1")
    assert v.eligible is True
    assert v.claim_contradicted is True


# ---------------------------------------------------------------------------
# Debt ledger (D26 Link 2)
# ---------------------------------------------------------------------------

def test_05_debt_accrues_per_unserved_window():
    ledger = FairnessDebtLedger(base_bound=3)
    ledger.record_window("w1", {"a"}, set())
    ledger.record_window("w2", {"a"}, set())
    st = ledger.check("a")
    assert st.debt == 2
    assert st.violated is False  # 2 <= 3


def test_06_service_resets_debt():
    ledger = FairnessDebtLedger(base_bound=3)
    ledger.record_window("w1", {"a"}, set())
    ledger.record_window("w2", {"a"}, set())
    ledger.record_window("w3", {"a"}, {"a"})
    st = ledger.check("a")
    assert st.debt == 0
    assert st.violated is False


def test_07_starvation_beyond_bound_produces_witness():
    ledger = FairnessDebtLedger(base_bound=2)
    for i in range(4):
        ledger.record_window(f"w{i}", {"victim"}, set())
    st = ledger.check("victim")
    assert st.violated is True
    assert st.witness is not None
    assert st.witness.item_id == "victim"
    assert st.witness.debt == 4
    assert st.witness.bound == 2
    assert st.witness.window_start == "w0"
    assert st.witness.window_end == "w3"


def test_08_missing_evidence_widens_bound_not_debt():
    ledger = FairnessDebtLedger(base_bound=2)
    ledger.record_window("w1", {"a"}, set(), evidence_present=False)
    ledger.record_window("w2", {"a"}, set(), evidence_present=False)
    st = ledger.check("a")
    # No debt accrued from unknown windows; bound widened 2 -> 4 -> 8.
    assert st.debt == 0
    assert st.widenings == 2
    assert st.bound == 2 * (MISSING_EVIDENCE_WIDEN_FACTOR ** 2)
    assert st.violated is False
    assert st.verdict_level == "FAIRNESS_QUALIFIED_WITH_ASSUMPTIONS"


# ---------------------------------------------------------------------------
# Broken schedulers through the harness (GAP-3: schedulers, not traces)
# ---------------------------------------------------------------------------

def _workload(victim_mode="always"):
    items = [
        WorkloadItem("alpha", _always_enabled),
        WorkloadItem("beta", _always_enabled),
    ]
    if victim_mode == "always":
        items.append(WorkloadItem("victim", _always_enabled))
    elif victim_mode == "intermittent":
        items.append(WorkloadItem("victim", _intermittent))
    elif victim_mode == "no_progress":
        items.append(WorkloadItem("victim", _always_enabled, makes_progress=False))
    return items


def test_09_wf_breaker_classified_by_behavior():
    harness = SchedulerHarness()
    result = harness.run(WeakFairnessBreakingScheduler("victim"),
                         _workload("always"), ticks=12)
    c = harness.classify_item(result, "victim")
    assert c.diagnostic == "WF_VIOLATION", c.explanation


def test_10_sf_breaker_classified_sf_only():
    harness = SchedulerHarness()
    result = harness.run(StrongFairnessBreakingScheduler("victim"),
                         _workload("intermittent"), ticks=12)
    c = harness.classify_item(result, "victim")
    assert c.diagnostic == "SF_ONLY_VIOLATION", c.explanation


def test_11_no_progress_scheduler_named_correctly():
    harness = SchedulerHarness()
    result = harness.run(NoProgressScheduler(),
                         _workload("no_progress"), ticks=12)
    c = harness.classify_item(result, "victim")
    assert c.diagnostic == "PROGRESS_ON_SERVICE_VIOLATION", c.explanation


def test_12_fair_scheduler_reaches_correct_progress():
    harness = SchedulerHarness()
    result = harness.run(RoundRobinScheduler(), _workload("always"), ticks=30)
    for item in ("alpha", "beta", "victim"):
        c = harness.classify_item(result, item)
        assert c.diagnostic == "CORRECT_PROGRESS", (item, c.explanation)


# ---------------------------------------------------------------------------
# Full-state invariants
# ---------------------------------------------------------------------------

def test_13_invariant_checker_catches_starvation():
    ledger = FairnessDebtLedger(base_bound=1)
    ledger.record_window("w1", {"s"}, set())
    ledger.record_window("w2", {"s"}, set())
    checker = InvariantChecker()
    viols = checker.check({"debt_ledger": ledger})
    kinds = [v.kind for v in viols]
    assert "STARVATION" in kinds


def test_14_invariant_checker_catches_dependency_order():
    checker = InvariantChecker()
    viols = checker.check({
        "dependencies": {"deploy": ["tests"]},
        "resolved": set(),          # tests NOT resolved
        "serviced": {"deploy"},     # but deploy was serviced
    })
    kinds = [v.kind for v in viols]
    assert "DEPENDENCY_ORDER" in kinds
    assert viols[0].witness["unresolved_dep"] == "tests"


def test_15_invariant_checker_catches_deadlock_cycle():
    checker = InvariantChecker()
    viols = checker.check({
        "dependencies": {"a": ["b"], "b": ["a"]},
        "waiting": {"a", "b"},
        "serviced": set(),
        "resolved": set(),
    })
    kinds = [v.kind for v in viols]
    assert "DEADLOCK_CYCLE" in kinds


def test_16_no_false_deadlock_when_member_progresses():
    checker = InvariantChecker()
    viols = checker.check({
        "dependencies": {"a": ["b"], "b": ["a"]},
        "waiting": {"a", "b"},
        "serviced": {"a"},   # a is being serviced -> not a deadlock
        "resolved": set(),
    })
    assert all(v.kind != "DEADLOCK_CYCLE" for v in viols)


# ---------------------------------------------------------------------------
# Tick ledger (GAP-4: independent observation)
# ---------------------------------------------------------------------------

def test_17_missed_tick_is_missing_opportunity_not_worker_fault():
    ledger = TickLedger()
    ledger.expect("tick-1", "2026-10-11T00:00:00Z", "worker-a")
    ledger.expect("tick-2", "2026-10-11T00:15:00Z", "worker-a")
    ledger.observe("tick-1", "2026-10-11T00:00:01Z")
    report = ledger.liveness_report()
    assert report["all_ticks_observed"] is False
    assert len(report["missed"]) == 1
    assert report["missed"][0]["tick_id"] == "tick-2"
    assert "Link 1" in report["note"]


# ---------------------------------------------------------------------------
# Live trace reader (GAP-2: live traces, not fixtures)
# ---------------------------------------------------------------------------

def test_18_live_trace_reader_feeds_classifier():
    reader = LiveTraceReader()
    lines = []
    for t in range(6):
        lines.append(json.dumps({"tick": t, "item_id": "x", "enabled": True,
                                 "serviced": False, "rank_before": [2],
                                 "rank_after": [2]}))
    with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as f:
        f.write("\n".join(lines))
        path = f.name
    try:
        trace = reader.read(path)
        assert trace["live"] is True
        states = reader.to_cycle_states(trace, "x")
        c = classify_cycle(states, live=True)
        assert c.diagnostic == "WF_VIOLATION"
    finally:
        os.unlink(path)


# ---------------------------------------------------------------------------
# Negative control: sabotage must break the suite (no theater)
# ---------------------------------------------------------------------------

def test_19_negative_control_sabotaged_gate_fails():
    """Sabotage the classifier to always PASS; the starvation scenario must
    then FAIL to be classified — proving the tests are not vacuous."""
    import fairness_invariants as fi
    real_classify = fi.classify_cycle

    def always_pass(cycle_states, live=False):
        return fi.Classification("CORRECT_PROGRESS", "sabotaged",
                                 "MODEL_CHECK_PASSED_IN_SCOPE", live)

    fi.classify_cycle = always_pass
    try:
        harness = SchedulerHarness()
        result = harness.run(WeakFairnessBreakingScheduler("victim"),
                             _workload("always"), ticks=12)
        c = harness.classify_item(result, "victim")
        # Under sabotage, the WF violation is mislabeled CORRECT_PROGRESS.
        # The REAL assertion (diagnostic == WF_VIOLATION) must therefore fail.
        with pytest.raises(AssertionError):
            assert c.diagnostic == "WF_VIOLATION"
    finally:
        fi.classify_cycle = real_classify
    # And with the real classifier restored, the honest assertion holds.
    c2 = harness.classify_item(result, "victim")
    assert c2.diagnostic == "WF_VIOLATION"


# ---------------------------------------------------------------------------
# Verdict levels (GAP-5: never collapse)
# ---------------------------------------------------------------------------

def test_20_every_verdict_names_a_level():
    prover = EligibilityProver(_registry())
    v = prover.prove(WorkItem("w", ["has_approval"]), {"approval": 1}, "win")
    assert v.verdict_level in VERDICT_LEVELS

    ledger = FairnessDebtLedger()
    ledger.record_window("w1", {"a"}, {"a"})
    assert ledger.check("a").verdict_level in VERDICT_LEVELS

    c = classify_cycle([{"enabled": True, "serviced": True,
                         "rank_before": [2], "rank_after": [1],
                         "terminal": False}])
    assert c.verdict_level in VERDICT_LEVELS
    assert c.diagnostic in DIAGNOSTICS


# ---------------------------------------------------------------------------
# Merge liveness (GAP-6: liveness, not just safety)
# ---------------------------------------------------------------------------

def test_21_merge_tracker_names_review_starvation():
    tracker = MergeLivenessTracker(starvation_bound_hours=72.0)
    pr = PRRecord(pr_number=9999,
                  review_requested_at="2026-10-01T00:00:00Z",
                  first_review_at=None,
                  resolved_at=None)
    v = tracker.check(pr, "2026-10-11T00:00:00Z")  # 10 days later
    assert v.link1_opportunity is True
    assert v.link2_fair_service is False
    assert v.starved is True
    assert v.starvation_witness["pr"] == 9999
    assert v.verdict_level in VERDICT_LEVELS


def test_22_merge_tracker_recognizes_completed_workflow():
    tracker = MergeLivenessTracker()
    pr = PRRecord(pr_number=9998,
                  review_requested_at="2026-10-10T00:00:00Z",
                  first_review_at="2026-10-10T01:00:00Z",
                  resolved_at="2026-10-10T02:00:00Z",
                  resolution="merged")
    v = tracker.check(pr, "2026-10-11T00:00:00Z")
    assert v.link1_opportunity and v.link2_fair_service and v.link3_progress
    assert v.starved is False
    assert v.verdict_level == "WORKFLOW_COMPLETED_IN_SCOPE"


def test_23_merge_tracker_no_opportunity_is_not_starvation():
    tracker = MergeLivenessTracker()
    pr = PRRecord(pr_number=9997, review_requested_at=None,
                  first_review_at=None, resolved_at=None)
    v = tracker.check(pr, "2026-10-11T00:00:00Z")
    assert v.link1_opportunity is False
    assert v.starved is False  # no opportunity => not a starvation fault
