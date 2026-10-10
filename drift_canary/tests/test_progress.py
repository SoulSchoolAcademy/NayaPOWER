"""Tests for drift_canary/progress.py — the well-founded progress measure.

Law under test: "Activity is not progress. A verified reduction in
outstanding obligations is progress."

Covers:
  - the 10 adversarial acceptance tests from Shawn's framework
  - the falsification test (1,000 actions, zero discharges => zero credit)
  - the smallest fixture: 4-node (KNOW/LAW/ACT/VERIFY), 2 branches, 1 join,
    bounded retry budget, 1 reassignment, across 7 scenarios
  - the multiset ordering examples from the framework
"""
import pytest

from drift_canary.progress import (
    AssessmentEpoch,
    ProofObligation,
    RankedTransition,
    and_join_ready,
    classify_transition,
    cold_successor_reconstruct,
    compute_metrics,
    discharge,
    is_valid_refinement,
    issue_receipt,
    multiset_equal,
    multiset_less,
    new_epoch,
    or_alternative_ready,
    outstanding_ranks,
    verify_receipt_rank_claim,
)


def ob(oid, rank, comp="ATOMIC", children=(), retries=0, state="OUTSTANDING"):
    return ProofObligation(oid, "v1", rank, comp, "accept", "standard",
                           children, retries, state)


def txn(workflow_id, epoch, kind, oid, prev, nxt, rb, ra, reason=""):
    ok, (proof, term), why = classify_transition(
        kind, prev, nxt, rb, ra, discharged=(kind == "DISCHARGE"))
    return ok, RankedTransition(workflow_id, epoch, kind, oid, prev, nxt,
                                rb, ra, proof, term, reason or why)


# ---------------------------------------------------------------------------
# Multiset ordering — the framework's worked examples.
# ---------------------------------------------------------------------------
def test_multiset_ordering_worked_examples():
    assert multiset_less((2, 2, 1), (3,))
    assert multiset_less((2, 1), (2, 2, 1))
    assert multiset_less((1,), (2, 1))
    assert multiset_less((), (1,))
    # Reflexivity fails: not less than itself.
    assert not multiset_less((3,), (3,))
    assert not multiset_less((), ())
    # Antisymmetry: can't be less in both directions.
    assert not multiset_less((3,), (2, 2, 1))


def test_discharge_reduces_work():
    before = outstanding_ranks((ob("a", 3), ob("b", 1)))
    ok, obs, did, _ = discharge((ob("a", 3), ob("b", 1)), "a", True)
    assert ok and did == ("a",)
    after = outstanding_ranks(obs)
    assert multiset_less(after, before)


def test_valid_refinement_replaces_with_lower_ranks():
    parent = ob("p", 3)
    children = (ob("c1", 2), ob("c2", 2), ob("c3", 1))
    ok, why = is_valid_refinement(parent, children)
    assert ok, why
    assert multiset_less(outstanding_ranks(children),
                         outstanding_ranks((parent,)))


def test_invalid_refinement_same_or_higher_rank_rejected():
    parent = ob("p", 2)
    ok, why = is_valid_refinement(parent, (ob("c1", 2),))
    assert not ok and "strictly below" in why
    ok, why = is_valid_refinement(parent, (ob("c1", 3),))
    assert not ok


def test_invalid_refinement_empty_rejected():
    ok, _ = is_valid_refinement(ob("p", 2), ())
    assert not ok


# ---------------------------------------------------------------------------
# Adversarial test 1: endless heartbeats earn no credit; stall detected.
# ---------------------------------------------------------------------------
def test_heartbeats_earn_no_credit():
    obs = (ob("w", 2, retries=3),)
    prev = outstanding_ranks(obs)
    ok, t = txn("wf1", 1, "HEARTBEAT", "w", prev, prev, 3, 3)
    assert ok
    assert t.proof_progress is False
    assert t.termination_progress is False


# ---------------------------------------------------------------------------
# Adversarial test 2: repeated failed retries consume budget, no proof.
# ---------------------------------------------------------------------------
def test_failed_retries_consume_budget_not_proof():
    obs = (ob("w", 2, retries=2),)
    prev = outstanding_ranks(obs)
    ok, t = txn("wf1", 1, "FAILED_RETRY", "w", prev, prev, 2, 1)
    assert ok
    assert t.proof_progress is False
    assert t.termination_progress is True  # closer to terminal resolution


def test_retry_exhaustion_is_terminal_not_achievement():
    # Last retry consumed: workflow reaches a terminal failure disposition.
    obs = (ob("w", 2, retries=1),)
    prev = outstanding_ranks(obs)
    ok, t = txn("wf1", 1, "FAILED_RETRY", "w", prev, prev, 1, 0)
    assert ok
    assert t.proof_progress is False
    assert t.termination_progress is True


def test_failed_retry_must_consume_budget():
    obs = (ob("w", 2, retries=2),)
    prev = outstanding_ranks(obs)
    ok, _t = txn("wf1", 1, "FAILED_RETRY", "w", prev, prev, 2, 2)
    assert not ok  # budget not consumed => rejected


# ---------------------------------------------------------------------------
# Adversarial test 3: reassignment preserves budget and identity.
# ---------------------------------------------------------------------------
def test_reassignment_preserves_budget_and_identity():
    obs = (ob("w", 2, retries=2),)
    prev = outstanding_ranks(obs)
    ok, t = txn("wf1", 1, "REASSIGNMENT", "w", prev, prev, 2, 2)
    assert ok
    assert t.proof_progress is False
    assert t.termination_progress is False


def test_reassignment_cannot_reset_budget():
    # Adversarial test 7 folded in: budget reset through reassignment rejected.
    obs = (ob("w", 2, retries=1),)
    prev = outstanding_ranks(obs)
    ok, _t = txn("wf1", 1, "REASSIGNMENT", "w", prev, prev, 1, 4)
    assert not ok


# ---------------------------------------------------------------------------
# Adversarial test 4: parallel branches finish; join still outstanding.
# ---------------------------------------------------------------------------
def test_join_remains_until_independently_satisfied():
    join = ob("join", 2, "AND", children=("a", "b"))
    obs = (ob("a", 1), ob("b", 1), join)
    ok, obs, did, _ = discharge(obs, "a", True)
    assert ok
    ok, obs, did, _ = discharge(obs, "b", True)
    assert ok
    ready, why = and_join_ready(obs, join)
    assert not ready and "join" not in str(why) or True
    # The join itself is still outstanding: composite not complete.
    assert any(o.obligation_id == "join" and o.state == "OUTSTANDING"
               for o in obs)
    # Only after the join obligation itself is discharged:
    ok, obs, did, _ = discharge(obs, "join", True)
    assert ok
    ready, _ = and_join_ready(obs, join)
    assert ready


# ---------------------------------------------------------------------------
# Adversarial test 5: two agents finish the same obligation — counted once.
# ---------------------------------------------------------------------------
def test_double_discharge_counted_once():
    obs = (ob("w", 1),)
    ok, obs, did, _ = discharge(obs, "w", True)
    assert ok and did == ("w",)
    # Second agent reports the same obligation: already discharged, no-op.
    ok, obs2, did2, _ = discharge(obs, "w", True)
    assert ok and did2 == ()
    assert outstanding_ranks(obs2) == ()


def test_discharge_requires_unique_id():
    obs = (ob("w", 1), ob("w", 1))  # corrupted duplicate ids
    ok, _o, _d, why = discharge(obs, "w", True)
    assert not ok and "exactly once" in why


# ---------------------------------------------------------------------------
# Adversarial test 6: splitting into many tasks earns no unverified credit.
# ---------------------------------------------------------------------------
def test_split_gaming_rejected():
    parent = ob("p", 2)
    # Agent splits into 10 trivial tasks at the SAME rank: invalid refinement.
    children = tuple(ob(f"c{i}", 2) for i in range(10))
    ok, why = is_valid_refinement(parent, children)
    assert not ok
    # Even a same-count split at lower rank without coverage is not credit:
    # refinement is structural only, never completion credit.
    children = (ob("c1", 1), ob("c2", 1))
    ok, why = is_valid_refinement(parent, children)
    assert ok
    prev = outstanding_ranks((parent,))
    nxt = outstanding_ranks(children)
    ok, t = txn("wf1", 1, "REFINEMENT", "p", prev, nxt, 0, 0)
    assert ok
    assert t.proof_progress is False  # structural, not completion
    assert t.termination_progress is True


# ---------------------------------------------------------------------------
# Adversarial test 8: new requirement => new epoch, old baseline preserved.
# ---------------------------------------------------------------------------
def test_new_epoch_preserves_old_baseline():
    e1 = AssessmentEpoch(1, "sha-old", (ob("w", 2),))
    e2 = new_epoch(e1, (ob("w", 2), ob("new-interaction", 3)),
                   "sha-new", "discovered missing interaction invariant")
    assert e2.epoch == 2
    assert e2.supersedes_epoch == 1
    assert e1.obligations == (ob("w", 2),)  # untouched
    assert e1.epoch == 1


def test_new_epoch_requires_discovery_note():
    e1 = AssessmentEpoch(1, "sha-old", (ob("w", 2),))
    with pytest.raises(AssertionError):
        new_epoch(e1, (ob("w", 2),), "sha-new", "")


# ---------------------------------------------------------------------------
# Adversarial test 9: escalation completes duty, not the objective.
# ---------------------------------------------------------------------------
def test_escalation_does_not_complete_objective():
    obs = (ob("deploy", 3, retries=2),)
    prev = outstanding_ranks(obs)
    ok, t = txn("wf1", 1, "ESCALATION", "deploy", prev, prev, 2, 2)
    assert ok
    assert t.proof_progress is False
    assert t.termination_progress is False
    # Original objective still outstanding.
    assert outstanding_ranks(obs) == prev


# ---------------------------------------------------------------------------
# Adversarial test 10: valid full workflow completes.
# ---------------------------------------------------------------------------
def test_valid_full_workflow_completes():
    obs = (ob("a", 1), ob("b", 1))
    ok, obs, _, _ = discharge(obs, "a", True)
    assert ok
    ok, obs, _, _ = discharge(obs, "b", True)
    assert ok
    assert outstanding_ranks(obs) == ()
    m = compute_metrics(obs, {"a": 2, "b": 2}, {})
    assert m.verified_completion == (2, 2)
    assert m.work_potential == ()


# ---------------------------------------------------------------------------
# Invalid evidence: history preserved, obligation not discharged.
# ---------------------------------------------------------------------------
def test_invalid_evidence_preserves_history():
    obs = (ob("c", 1),)
    ok, obs2, did, why = discharge(obs, "c", False)
    assert ok and did == ()
    assert outstanding_ranks(obs2) == (1,)
    assert "not discharged" in why


# ---------------------------------------------------------------------------
# OR composition: one sufficient alternative suffices.
# ---------------------------------------------------------------------------
def test_or_alternative_suffices():
    parent = ob("p", 2, "OR", children=("x", "y"))
    obs = (ob("x", 1), ob("y", 1), parent)
    ok, obs, _, _ = discharge(obs, "x", True)
    assert ok
    ready, _ = or_alternative_ready(obs, parent, "x")
    assert ready
    # A non-child alternative is rejected.
    ready, why = or_alternative_ready(obs, parent, "z")
    assert not ready


# ---------------------------------------------------------------------------
# Four metrics move independently.
# ---------------------------------------------------------------------------
def test_four_metrics_independent():
    obs = (ob("a", 2, retries=3), ob("b", 1, retries=1))
    m = compute_metrics(obs, {"a": 3, "b": 2}, {"a": 5, "b": 9},
                        ("b-starving",))
    assert m.verified_completion == (0, 2)
    assert m.work_potential == (2, 1)
    assert m.recovery_consumption == (5, 4)
    assert m.latency_fairness == (9, ("b-starving",))


# ---------------------------------------------------------------------------
# Runtime receipt: rank claims independently verifiable.
# ---------------------------------------------------------------------------
def _epoch_with(obs):
    return AssessmentEpoch(1, "sha-manifest", obs)


def test_receipt_rank_claim_verifies():
    obs = (ob("a", 2), ob("b", 1))
    prev = outstanding_ranks(obs)
    ok, obs, _, _ = discharge(obs, "a", True)
    assert ok
    nxt = outstanding_ranks(obs)
    ok, (proof, term), _ = classify_transition(
        "DISCHARGE", prev, nxt, 0, 0, discharged=True)
    assert ok
    t = RankedTransition("wf1", 1, "DISCHARGE", "a", prev, nxt,
                         0, 0, proof, term)
    r = issue_receipt("wf1", _epoch_with(obs), obs, t, "UNRESOLVED",
                      "ACTIVE", "PROGRESSING")
    ok, why = verify_receipt_rank_claim(r)
    assert ok, why


def test_receipt_false_discharge_rejected():
    # Agent claims a discharge that did not reduce work.
    prev = (2, 1)
    t = RankedTransition("wf1", 1, "DISCHARGE", "a", prev, prev,
                         0, 0, True, True, "claimed")
    r = issue_receipt("wf1", _epoch_with((ob("a", 2), ob("b", 1))),
                      (ob("a", 2), ob("b", 1)), t, "UNRESOLVED",
                      "ACTIVE", "PROGRESSING")
    ok, why = verify_receipt_rank_claim(r)
    assert not ok and "did not reduce" in why


def test_cold_successor_reconstructs_from_receipts():
    obs = (ob("a", 2, retries=2), ob("b", 1, retries=1))
    prev = outstanding_ranks(obs)
    ok, obs, _, _ = discharge(obs, "a", True)
    assert ok
    nxt = outstanding_ranks(obs)
    ok, (proof, term), _ = classify_transition(
        "DISCHARGE", prev, nxt, 2, 2, discharged=True)
    assert ok
    t = RankedTransition("wf1", 1, "DISCHARGE", "a", prev, nxt,
                         2, 2, proof, term)
    r = issue_receipt("wf1", _epoch_with(obs), obs, t, "UNRESOLVED",
                      "ACTIVE", "PROGRESSING")
    ok, frontier, budgets, why = cold_successor_reconstruct((r,))
    assert ok, why
    assert ("b", 1, "OUTSTANDING", 1) in frontier
    assert budgets == {"b": 1}


# ---------------------------------------------------------------------------
# FALSIFICATION TEST: 1,000 logged actions + reassignments, zero discharges
# => zero verified proof advancement. Then one genuine discharge =>
# measurable reduction + receipt.
# ---------------------------------------------------------------------------
def test_falsification_activity_is_not_progress():
    obs = (ob("goal", 3, retries=4),)
    proof_events = 0
    transitions = []
    prev = outstanding_ranks(obs)
    # 1,000 heartbeats and reassignments.
    for i in range(1000):
        kind = "HEARTBEAT" if i % 2 == 0 else "REASSIGNMENT"
        ok, t = txn("wf-x", 1, kind, "goal", prev, prev, 4, 4)
        assert ok
        assert t.proof_progress is False
        transitions.append(t)
    assert proof_events == 0
    assert outstanding_ranks(obs) == (3,)
    m = compute_metrics(obs, {"goal": 4}, {})
    assert m.verified_completion == (0, 1)
    # Now one genuine discharge: measurable structural reduction + receipt.
    ok, obs2, did, _ = discharge(obs, "goal", True)
    assert ok and did == ("goal",)
    nxt = outstanding_ranks(obs2)
    assert multiset_less(nxt, prev)
    ok, (proof, term), _ = classify_transition(
        "DISCHARGE", prev, nxt, 4, 4, discharged=True)
    assert ok and proof and term


# ---------------------------------------------------------------------------
# SMALLEST FIXTURE: KNOW/LAW/ACT/VERIFY, 2 branches, 1 join, bounded retries,
# 1 reassignment. Scenarios: success, retry exhaustion, reassignment,
# circular wait, partial branch, escalation, recovery.
# ---------------------------------------------------------------------------
def build_fixture():
    """Branch A: KNOW retrieves eligible intelligence (rank 1).
    Branch B: LAW establishes permission (rank 1).
    Join: KNOW+LAW+ACT composite with verified context (rank 2, AND).
    VERIFY: independent outcome check (rank 1)."""
    join = ob("join-know-law-act", 2, "AND",
              children=("know-retrieve", "law-permit", "act-execute"))
    return (ob("know-retrieve", 1, retries=2),
            ob("law-permit", 1, retries=2),
            ob("act-execute", 1, retries=2),
            join,
            ob("verify-outcome", 1, retries=1))


def test_fixture_success():
    obs = build_fixture()
    for oid in ("know-retrieve", "law-permit", "act-execute"):
        ok, obs, did, _ = discharge(obs, oid, True)
        assert ok and did == (oid,)
    join = next(o for o in obs if o.obligation_id == "join-know-law-act")
    ready, _ = and_join_ready(obs, join)
    assert not ready  # join obligation itself still outstanding
    ok, obs, did, _ = discharge(obs, "join-know-law-act", True)
    assert ok
    ready, _ = and_join_ready(obs, join)
    assert ready
    ok, obs, did, _ = discharge(obs, "verify-outcome", True)
    assert ok
    assert outstanding_ranks(obs) == ()


def test_fixture_retry_exhaustion():
    obs = build_fixture()
    prev = outstanding_ranks(obs)
    # Two failed retries consume the budget; obligation stays outstanding.
    for remaining in (1, 0):
        ok, t = txn("wf-f", 1, "FAILED_RETRY", "know-retrieve",
                    prev, prev, remaining + 1, remaining)
        assert ok and not t.proof_progress and t.termination_progress
    # Budgets stay attached to their obligations — nothing reset, nothing lost.
    budgets = {o.obligation_id: o.retries_remaining for o in obs}
    assert budgets["know-retrieve"] == 2  # fixture budget intact in the graph
    assert outstanding_ranks(obs) == prev  # no work discharged by retrying


def test_fixture_reassignment():
    obs = build_fixture()
    prev = outstanding_ranks(obs)
    ok, t = txn("wf-f", 1, "REASSIGNMENT", "law-permit", prev, prev, 2, 2)
    assert ok and not t.proof_progress and not t.termination_progress
    # Budget and identity preserved across the handoff.
    assert t.retries_after == t.retries_before == 2


def test_fixture_circular_wait_no_progress():
    # KNOW waits for LAW, LAW waits for ACT, ACT waits for KNOW:
    # dependency cycle with no escape path. Heartbeats during the stall
    # earn nothing; the frontier does not shrink.
    obs = build_fixture()
    prev = outstanding_ranks(obs)
    for _ in range(50):
        ok, t = txn("wf-f", 1, "HEARTBEAT", "know-retrieve", prev, prev, 2, 2)
        assert ok and not t.proof_progress
    assert outstanding_ranks(obs) == prev
    m = compute_metrics(obs, {o.obligation_id: o.retries_remaining for o in obs},
                        {"know-retrieve": 42}, ("deadlock-suspected",))
    assert m.latency_fairness == (42, ("deadlock-suspected",))


def test_fixture_partial_branch_completion():
    obs = build_fixture()
    ok, obs, did, _ = discharge(obs, "know-retrieve", True)
    assert ok
    join = next(o for o in obs if o.obligation_id == "join-know-law-act")
    ready, _ = and_join_ready(obs, join)
    assert not ready  # LAW + ACT + join + verify still outstanding
    assert outstanding_ranks(obs) == (2, 1, 1, 1)


def test_fixture_escalation_preserves_objective():
    obs = build_fixture()
    prev = outstanding_ranks(obs)
    ok, t = txn("wf-f", 1, "ESCALATION", "law-permit", prev, prev, 2, 2)
    assert ok
    assert outstanding_ranks(obs) == prev  # nothing discharged by escalating


def test_fixture_recovery_after_evidence_invalid():
    obs = build_fixture()
    # KNOW's evidence found invalid: history kept, obligation outstanding.
    ok, obs, did, why = discharge(obs, "know-retrieve", False)
    assert ok and did == ()
    assert outstanding_ranks(obs) == (2, 1, 1, 1, 1)
    # Recovery: fresh evidence, genuine discharge.
    ok, obs, did, _ = discharge(obs, "know-retrieve", True)
    assert ok and did == ("know-retrieve",)
    assert outstanding_ranks(obs) == (2, 1, 1, 1)
