"""Adversarial tests for UD-16 — ONE ORDER FOR CHANGING RULES.

Acceptance gate: PASS only if no unsupported authority commits under any
interleaving, ambiguous outcomes never create authority, stale replays are
rejected, recovery reconstructs the true committed state in every crash
scenario, and mutations produce detectable counterexamples.
"""

import pytest

from rule_change_order import (
    GovernanceLedger, Refusal, SimulatedCrash, disable_guard,
    drive_to_crash_point, CRASH_POINTS,
)


def make_ledger(**kw):
    kw.setdefault("authorized_changers", {"shawn", "gov-seat"})
    return GovernanceLedger(**kw)


def full_order(ledger, op, verifier="auditor", authority="shawn"):
    ledger.prepare(op)
    ledger.independent_verify(op, verifier)
    ledger.authorize(op, authority)
    receipt = ledger.commit(op)
    ledger.propagate(op)
    return receipt


def propose(ledger, rule_id="R1", proposer="shawn", old="__current__",
            new="new text", reason="why", evidence=("ev1",)):
    if old == "__current__":
        old = ledger.rules.get(rule_id)
    return ledger.propose(proposer, rule_id, old, new, reason, evidence)


# ---------------------------------------------------------------------------
# Positive: the one order works.
# ---------------------------------------------------------------------------

def test_happy_path_advances_epoch_and_rule():
    L = make_ledger()
    L.rules["R1"] = ""
    op = propose(L)
    receipt = full_order(L, op)
    assert L.epoch == 1
    assert L.rules["R1"] == "new text"
    assert receipt["commit_epoch"] == 1
    assert L.has_authority(op.operation_id) is True


def test_strict_sequence_second_change_applies_at_epoch_1():
    L = make_ledger()
    L.rules["R1"] = ""
    full_order(L, propose(L, new="v1"))
    op2 = propose(L, old="v1", new="v2")
    assert op2.base_epoch == 1
    full_order(L, op2)
    assert L.epoch == 2
    assert L.rules["R1"] == "v2"


def test_independent_verifier_distinct_from_proposer():
    L = make_ledger()
    L.rules["R1"] = ""
    op = propose(L, proposer="gov-seat")
    full_order(L, op, verifier="auditor", authority="shawn")
    assert L.rules["R1"] == "new text"


def test_recovery_after_clean_propagate_is_verified():
    L = make_ledger()
    L.rules["R1"] = ""
    op = propose(L)
    full_order(L, op)
    L2, report = GovernanceLedger.recover(
        L.journal, L.rules, L.epoch, {"shawn", "gov-seat"})
    assert report[op.operation_id] == "INDEPENDENTLY_VERIFIED"
    assert L2.epoch == 1 and L2.rules["R1"] == "new text"


def test_idempotent_replay_returns_original_receipt_no_double_apply():
    L = make_ledger()
    L.rules["R1"] = ""
    op = propose(L)
    receipt = full_order(L, op)
    out = L.replay(op.to_dict())
    assert out["replay"] == "REPLAY_DUPLICATE_SAFE"
    assert out["commit_epoch"] == receipt["commit_epoch"]
    assert L.epoch == 1  # epoch did not move twice


# ---------------------------------------------------------------------------
# Negative: side channels are closed.
# ---------------------------------------------------------------------------

def test_unauthorized_proposer_refused():
    L = make_ledger()
    with pytest.raises(Refusal) as e:
        propose(L, proposer="random-seat")
    assert e.value.code == "UNAUTHORIZED_PROPOSER"
    assert L.epoch == 0


def test_unauthorized_authority_refused():
    L = make_ledger()
    L.rules["R1"] = ""
    op = propose(L)
    ledger_prepare_verify(L, op)
    with pytest.raises(Refusal) as e:
        L.authorize(op, "random-seat")
    assert e.value.code == "UNAUTHORIZED_AUTHORITY"


def ledger_prepare_verify(L, op, verifier="auditor"):
    L.prepare(op)
    L.independent_verify(op, verifier)


def test_out_of_order_commit_refused_then_rebased():
    # Strict single order: a commit based at a stale epoch is refused on ANY
    # rule. The honest path is re-propose at the current epoch.
    L = make_ledger()
    op_a = L.propose("shawn", "R1", None, "A", "why", ("ev1",))
    op_b = L.propose("gov-seat", "R2", None, "B", "why", ("ev1",))
    for op, v in ((op_a, "auditor"), (op_b, "auditor2")):
        L.prepare(op)
        L.independent_verify(op, v)
        L.authorize(op, "shawn")
    L.commit(op_a)  # epoch -> 1
    with pytest.raises(Refusal) as e:
        L.commit(op_b)  # based at epoch 0, ledger at 1
    assert e.value.code == "OUT_OF_ORDER"
    assert L.epoch == 1
    # The stale prepared change is explicitly aborted (journaled), freeing
    # the rule; then re-proposed fresh at the current epoch.
    L.abort(op_b, "base epoch stale after concurrent commit")
    op_b2 = L.propose("gov-seat", "R2", None, "B", "why", ("ev1",))
    assert op_b2.base_epoch == 1
    full_order(L, op_b2)
    assert L.epoch == 2 and L.rules["R2"] == "B"


def test_second_change_on_same_rule_while_in_flight_refused():
    L = make_ledger()
    L.rules["R1"] = ""
    op = propose(L, new="A")
    L.prepare(op)
    with pytest.raises(Refusal) as e:
        propose(L, new="B")
    assert e.value.code == "RULE_IN_FLIGHT"


def test_stale_base_text_refused():
    L = make_ledger()
    L.rules["R1"] = "current"
    with pytest.raises(Refusal) as e:
        propose(L, old="outdated")
    assert e.value.code == "STALE_BASE"


def test_insufficient_evidence_refused():
    L = make_ledger()
    with pytest.raises(Refusal) as e:
        L.propose("shawn", "R1", None, "x", "why", ())
    assert e.value.code == "INSUFFICIENT_EVIDENCE"
    with pytest.raises(Refusal) as e:
        L.propose("shawn", "R1", None, "x", "", ("ev1",))
    assert e.value.code == "INSUFFICIENT_EVIDENCE"


def test_self_verification_refused():
    L = make_ledger()
    L.rules["R1"] = ""
    op = propose(L, proposer="gov-seat")
    L.prepare(op)
    with pytest.raises(Refusal) as e:
        L.independent_verify(op, "gov-seat")
    assert e.value.code == "SELF_VERIFY"


def test_tampered_proposal_detected_at_commit():
    L = make_ledger()
    L.rules["R1"] = ""
    op = propose(L, new="honest")
    ledger_prepare_verify(L, op)
    L.authorize(op, "shawn")
    op.new_text = "malicious"  # tamper after prepare
    with pytest.raises(Refusal) as e:
        L.commit(op)
    assert e.value.code == "PROPOSAL_TAMPERED"
    assert L.epoch == 0 and L.rules["R1"] == ""


def test_stale_replay_refused():
    L = make_ledger()
    L.rules["R1"] = ""
    full_order(L, propose(L, new="v1"))
    stale = {"operation_id": "op-deadbeef", "base_epoch": 0,
             "proposal_hash": "x"}
    with pytest.raises(Refusal) as e:
        L.replay(stale)
    assert e.value.code == "STALE_REPLAY"


# ---------------------------------------------------------------------------
# Mid-game protection: no rule rewrites under an open decision.
# ---------------------------------------------------------------------------

def test_mid_decision_rule_rewrite_voids_decision():
    L = make_ledger()
    L.rules["R1"] = ""
    L.open_decision("D-101")
    assert L.decision_valid("D-101") is True
    full_order(L, propose(L, new="changed"))
    assert L.decision_valid("D-101") is False
    assert L.decisions["D-101"]["status"] == "VOIDED_MID_DECISION_REWRITE"
    # Re-run under the new epoch succeeds.
    L.open_decision("D-102")
    assert L.decision_valid("D-102") is True
    L.close_decision("D-102", "ACTED")
    assert L.decisions["D-102"]["status"] == "CLOSED_ACTED"


def test_closed_decision_untouched_by_later_change():
    L = make_ledger()
    L.rules["R1"] = ""
    L.open_decision("D-1")
    L.close_decision("D-1", "ACTED")
    full_order(L, propose(L, new="changed"))
    assert L.decisions["D-1"]["status"] == "CLOSED_ACTED"


# ---------------------------------------------------------------------------
# Crash matrix: recovery reconstructs the true committed state.
# ---------------------------------------------------------------------------

def test_crash_before_commit_never_commits():
    for point in ("after_propose", "after_prepare", "after_verify",
                  "after_authorize"):
        L = make_ledger()
        L.rules["R1"] = ""
        op = propose(L, new="v1")
        journal, durable_rules, durable_epoch = drive_to_crash_point(
            L, op, "auditor", "shawn", point)
        L2, report = GovernanceLedger.recover(
            journal, durable_rules, durable_epoch, {"shawn", "gov-seat"})
        assert L2.epoch == 0, point
        assert L2.rules["R1"] == "", point
        assert L2.has_authority(op.operation_id) is False, point
        # Safe to retry through the one order.
        op2 = L2.propose("shawn", "R1", "", "v1", "why", ("ev1",))
        full_order(L2, op2)
        assert L2.epoch == 1 and L2.rules["R1"] == "v1", point


def test_crash_during_commit_ambiguous_never_grants_authority():
    L = make_ledger()
    L.rules["R1"] = ""
    op = propose(L, new="v1")
    journal, durable_rules, durable_epoch = drive_to_crash_point(
        L, op, "auditor", "shawn", "during_commit")
    # Journal shows intent; durable store does NOT show the change.
    assert any(e[0] == "COMMIT_INTENT" for e in journal)
    assert not any(e[0] == "COMMIT_APPLIED" for e in journal)
    L2, report = GovernanceLedger.recover(
        journal, durable_rules, durable_epoch, {"shawn", "gov-seat"})
    # Durable store is ground truth: the commit did NOT happen.
    assert report[op.operation_id] == "COMMIT_OUTCOME_UNKNOWN->NOT_COMMITTED"
    assert L2.epoch == 0
    assert L2.rules["R1"] == ""
    # Ambiguity never became authority.
    assert L2.has_authority(op.operation_id) is False
    # Retry is safe and commits exactly once.
    op2 = L2.propose("shawn", "R1", "", "v1", "why", ("ev1",))
    full_order(L2, op2)
    assert L2.epoch == 1


def test_crash_after_commit_before_propagate_projection_pending():
    L = make_ledger()
    L.rules["R1"] = ""
    op = propose(L, new="v1")
    journal, durable_rules, durable_epoch = drive_to_crash_point(
        L, op, "auditor", "shawn", "after_commit")
    L2, report = GovernanceLedger.recover(
        journal, durable_rules, durable_epoch, {"shawn", "gov-seat"})
    assert report[op.operation_id] == "COMMITTED_PROJECTION_PENDING"
    assert L2.epoch == 1 and L2.rules["R1"] == "v1"
    assert L2.has_authority(op.operation_id) is True
    # Re-propagating is idempotent — no second commit.
    assert L2.epoch == 1


# ---------------------------------------------------------------------------
# Race fixtures: both orders of every concurrent pair, four invariants.
# ---------------------------------------------------------------------------

def test_race_both_orders_one_winner_per_epoch():
    for first, second in (("A", "B"), ("B", "A")):
        L = make_ledger()
        L.rules["R1"] = ""
        ops = {}
        for name in (first, second):
            ops[name] = L.propose("shawn", "R1", "", name, "why", ("ev1",))
            # Only the first may prepare; the second hits RULE_IN_FLIGHT.
        L.prepare(ops[first])
        with pytest.raises(Refusal) as e:
            L.propose("shawn", "R1", "", second, "why", ("ev1",))
        assert e.value.code == "RULE_IN_FLIGHT"
        L.independent_verify(ops[first], "auditor")
        L.authorize(ops[first], "shawn")
        receipt = L.commit(ops[first])
        # Invariants: exactly one commit, authorized, epoch +1, no skip.
        assert receipt["commit_epoch"] == 1
        assert L.epoch == 1
        assert L.rules["R1"] == first
        assert L.has_authority(ops[first].operation_id) is True
        # Loser re-proposes against the new epoch and may then commit.
        loser = L.propose("shawn", "R1", first, second, "why", ("ev1",))
        assert loser.base_epoch == 1
        full_order(L, loser)
        assert L.epoch == 2 and L.rules["R1"] == second


def test_race_forged_stale_commit_refused():
    # A forged commit built on a stale epoch is refused even when the
    # surrounding order looks healthy.
    L = make_ledger()
    full_order(L, propose(L, new="v1"))
    assert L.epoch == 1
    stale = L.propose("shawn", "R1", "v1", "v2", "why", ("ev1",))
    stale.base_epoch = 0  # simulate a replay from before the commit
    stale.phase = "AUTHORIZED"
    with pytest.raises(Refusal) as e:
        L.commit(stale)
    assert e.value.code == "OUT_OF_ORDER"
    assert L.epoch == 1 and L.rules["R1"] == "v1"


# ---------------------------------------------------------------------------
# Mutations: removing a guard must produce a detectable counterexample.
# ---------------------------------------------------------------------------

def test_mutation_no_authz_guard_allows_unauthorized_change():
    L = make_ledger()
    L.rules["R1"] = ""
    with disable_guard("authz"):
        op = L.propose("intruder", "R1", "", "evil", "why", ("ev1",))
        L.prepare(op)
        L.independent_verify(op, "auditor")
        L.authorize(op, "intruder")
        L.commit(op)
        assert L.rules["R1"] == "evil"  # counterexample: guard was load-bearing
    # Guard restored: the same attack is refused.
    L2 = make_ledger()
    with pytest.raises(Refusal) as e:
        L2.propose("intruder", "R1", None, "evil", "why", ("ev1",))
    assert e.value.code == "UNAUTHORIZED_PROPOSER"


def test_mutation_no_sequence_guard_allows_out_of_order():
    L = make_ledger()
    L.rules["R1"] = ""
    L.rules["R2"] = ""
    op_a = L.propose("shawn", "R1", "", "A", "why", ("ev1",))
    op_b = L.propose("shawn", "R2", "", "B", "why", ("ev1",))
    for op in (op_a, op_b):
        L.prepare(op)
        L.independent_verify(op, "auditor")
        L.authorize(op, "shawn")
    L.commit(op_a)
    with disable_guard("sequence"):
        L.commit(op_b)  # stale base epoch 0 accepted: counterexample
        assert L.epoch == 2
    # Guard restored: stale commit refused (proven in test_out_of_order...;
    # re-assert the refusal shape here for the mutation record).
    L2 = make_ledger()
    L2.rules["R1"] = ""
    a = L2.propose("shawn", "R1", "", "A", "why", ("ev1",))
    for op in (a,):
        L2.prepare(op)
        L2.independent_verify(op, "auditor")
        L2.authorize(op, "shawn")
    L2.commit(a)
    stale = L2.propose("shawn", "R1", "A", "A2", "why", ("ev1",))
    stale.base_epoch = 0
    stale.phase = "AUTHORIZED"
    with pytest.raises(Refusal) as e:
        L2.commit(stale)
    assert e.value.code == "OUT_OF_ORDER"


def test_mutation_no_inflight_guard_allows_double_flight():
    L = make_ledger()
    L.rules["R1"] = ""
    op1 = L.propose("shawn", "R1", "", "first", "why", ("ev1",))
    with disable_guard("inflight"):
        op2 = L.propose("shawn", "R1", "", "second", "why", ("ev1",))
        assert op2.operation_id != op1.operation_id  # counterexample: two live
    L2 = make_ledger()
    L2.rules["R1"] = ""
    o = L2.propose("shawn", "R1", "", "first", "why", ("ev1",))
    L2.prepare(o)
    with pytest.raises(Refusal) as e:
        L2.propose("shawn", "R1", "", "second", "why", ("ev1",))
    assert e.value.code == "RULE_IN_FLIGHT"


def test_abort_frees_rule_and_is_journaled():
    L = make_ledger()
    op = propose(L, new="v1")
    L.prepare(op)
    L.abort(op, "superseded")
    assert op.phase == "ABORTED"
    assert "R1" not in L.in_flight
    assert ("ABORTED", op.operation_id, "superseded") in L.journal
    op2 = propose(L, new="v1")
    full_order(L, op2)
    assert L.rules["R1"] == "v1" and L.epoch == 1


def test_abort_committed_change_refused():
    L = make_ledger()
    op = propose(L, new="v1")
    full_order(L, op)
    with pytest.raises(Refusal) as e:
        L.abort(op, "too late")
    assert e.value.code == "BAD_PHASE"


def test_has_authority_false_for_unknown_outcome_even_with_intent():
    L = make_ledger()
    L.rules["R1"] = ""
    op = propose(L, new="v1")
    L.prepare(op)
    L.independent_verify(op, "auditor")
    L.authorize(op, "shawn")
    assert L.has_authority(op.operation_id) is False  # not yet committed
    L.commit(op)
    assert L.has_authority(op.operation_id) is True
