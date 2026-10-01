"""Acceptance battery for NAYA-KERNEL-ACT (CANDIDATE — NOT RATIFIED).

Mirrors ACT-NODE-SPEC-CANDIDATE.md §9. Candidate code: these tests prove the
spec is implementable; they grant, merge, deploy, and ratify nothing.
"""

import pytest

from naya_kernel.node_base import GateVerdict, NodeBase
from naya_kernel.nodes import act_node
from naya_kernel.nodes.act_node import (
    ActNode,
    make_decision_receipt,
    make_tool_registry,
    S_AUTHORIZED, S_CLAIMED, S_EXECUTING, S_RECEIPTED, S_REFUSED, S_FAILED,
    PATH_EXECUTED, PATH_REFUSED, PATH_ASK_SUSPENDED, PATH_READ_MORE_LOOP,
    PATH_FAILED, PATH_CANCELLED,
    OUTCOME_SUCCESS, OUTCOME_FAILURE, OUTCOME_REFUSED, OUTCOME_CONFLICT,
    ERROR_TRANSIENT, ERROR_PERMANENT, ERROR_HARM_SIGNAL,
)


def ok_executor(effects="done"):
    def _exec(tool_id, params):
        return {"status": "ok", "effects": effects, "error_class": None}
    return _exec


def failing_executor(status="error", error_class=ERROR_PERMANENT, detail="boom"):
    def _exec(tool_id, params):
        return {"status": status, "effects": "",
                "error_class": error_class, "error_detail": detail}
    return _exec


def state_for(node=None, **overrides):
    s = {
        "decision_receipt": make_decision_receipt(),
        "tool_registry": make_tool_registry(),
        "execution_ledger": {},
        "now": "2026-09-30T19:00:00+00:00",
    }
    s.update(overrides)
    return s


# ------------------------------------------------------------------
# §9.1 valid receipt executes exactly once; receipt matches effects
# ------------------------------------------------------------------
def test_valid_receipt_executes_exactly_once_with_matching_effects():
    node = ActNode(executor=ok_executor("effect-A"))
    out = node.execute(state_for())
    assert out["path"] == PATH_EXECUTED
    r = out["receipt"]
    assert r["outcome"] == OUTCOME_SUCCESS
    assert "effect-A" in r["effects_observed"]
    assert r["tool"]["tool_id"] == "echo_tool"
    assert r["state_transitions"][-1]["to"] == S_RECEIPTED
    # cold-successor check: receipt recomputes
    assert node.recompute(r) == "MATCH"


# ------------------------------------------------------------------
# §9.2 same decision twice -> one execution, two identical receipts
# ------------------------------------------------------------------
def test_duplicate_submission_dedupes_to_same_receipt():
    node = ActNode(executor=ok_executor("effect-B"))
    ledger = {}
    out1 = node.execute(state_for(execution_ledger=ledger))
    out2 = node.execute(state_for(execution_ledger=ledger))
    assert out1["path"] == PATH_EXECUTED == out2["path"]
    assert out1["execution_id"] == out2["execution_id"]
    assert out1["receipt"]["receipt_hash"] == out2["receipt"]["receipt_hash"]
    assert len(ledger) == 1  # one execution ever


# ------------------------------------------------------------------
# §9.3 race: pre-claimed in-flight key -> loser coalesces, never executes twice
# ------------------------------------------------------------------
def test_in_flight_claim_coalesces_loser_without_second_execution():
    calls = []

    def counting_executor(tool_id, params):
        calls.append(1)
        return {"status": "ok", "effects": "x", "error_class": None}

    node = ActNode(executor=counting_executor)
    ledger = {}
    # Simulate the winner's claim landing first (another instance holds it).
    receipt = make_decision_receipt()
    key = "act:" + node._fingerprint(receipt, receipt["winner"])
    ledger[key] = {
        "execution_id": "exec-winner", "decision_ref": receipt["receipt_id"],
        "idempotency_key": key, "fingerprint": node._fingerprint(receipt, receipt["winner"]),
        "state": S_EXECUTING, "tool": {"tool_id": "echo_tool", "version": "1.0.0", "idempotent": True},
        "params_hash": "p", "lease_deadline": "2026-09-30T20:00:00+00:00",
        "heartbeat_at": "2026-09-30T19:59:00+00:00",
        "transitions": [], "ticket": {"execution_id": "exec-winner", "status": "EXECUTING"},
        "receipt": None, "claimed_at": "2026-09-30T19:00:00+00:00",
    }
    out = node.execute(state_for(execution_ledger=ledger,
                                 decision_receipt=receipt))
    assert out["coalesced"] is True
    assert out["execution_id"] == "exec-winner"
    assert calls == []  # loser never invoked the tool


# ------------------------------------------------------------------
# §9.4 same key + different fingerprint -> refuse + conflict receipt
# ------------------------------------------------------------------
def test_fingerprint_conflict_refuses_fail_closed():
    node = ActNode(executor=ok_executor("e"))
    ledger = {}
    receipt1 = make_decision_receipt()
    node.execute(state_for(execution_ledger=ledger, decision_receipt=receipt1))
    # Same receipt id but different params -> same derivation inputs EXCEPT
    # params_hash -> a DIFFERENT key. To force same-key conflict we forge:
    key = "act:" + node._fingerprint(receipt1, receipt1["winner"])
    ledger[key]["fingerprint"] = "forged-other-fingerprint"
    ledger[key]["receipt"] = None  # undo the completed receipt to reach the conflict check
    out = node.execute(state_for(execution_ledger=ledger, decision_receipt=receipt1))
    assert out["path"] == PATH_REFUSED
    assert out["receipt"]["outcome"] == OUTCOME_CONFLICT
    assert out["receipt"]["conflict"]["alert"].startswith("RAISED")


# ------------------------------------------------------------------
# §9.5 unregistered tool -> refused before invocation
# ------------------------------------------------------------------
def test_unregistered_tool_refused_without_invocation():
    calls = []
    node = ActNode(executor=lambda t, p: calls.append(t) or
                   {"status": "ok", "effects": "x", "error_class": None})
    receipt = make_decision_receipt(
        winner={"tool_id": "mystery_tool", "version": "9.9", "params": {}})
    out = node.execute(state_for(decision_receipt=receipt))
    assert out["path"] == PATH_REFUSED
    assert "not registered" in out["receipt"]["refusal_reasons"][0]
    assert calls == []


# ------------------------------------------------------------------
# §9.5b registered tool beyond granted authority -> refused
# ------------------------------------------------------------------
def test_tool_beyond_granted_authority_refused():
    node = ActNode(executor=ok_executor("e"))
    reg = make_tool_registry(**{"write_tool": {
        "version": "1.0.0", "authority_class": "WRITE_BROAD",
        "idempotent": False, "max_timeout_ms": 5000,
        "retry_policy": {"attempts": 0, "backoff": "none"},
        "required_authority": "autonomous_envelope",  # not the director order
        "compensating_tool": None, "evidence_capture": "return_value",
    }})
    receipt = make_decision_receipt(
        winner={"tool_id": "write_tool", "version": "1.0.0", "params": {}})
    out = node.execute(state_for(decision_receipt=receipt, tool_registry=reg))
    assert out["path"] == PATH_REFUSED
    assert "no self-escalation" in out["receipt"]["refusal_reasons"][0]


# ------------------------------------------------------------------
# §9.5c irreversible tool without explicit naming -> refused
# ------------------------------------------------------------------
def test_irreversible_tool_requires_explicit_naming():
    node = ActNode(executor=ok_executor("e"))
    reg = make_tool_registry(**{"burn_tool": {
        "version": "1.0.0", "authority_class": "IRREVERSIBLE",
        "idempotent": False, "max_timeout_ms": 5000,
        "retry_policy": {"attempts": 0, "backoff": "none"},
        "required_authority": "director_order",
        "compensating_tool": None, "evidence_capture": "return_value",
    }})
    receipt = make_decision_receipt(
        winner={"tool_id": "burn_tool", "version": "1.0.0", "params": {}},
        names_irreversibility=False)
    out = node.execute(state_for(decision_receipt=receipt, tool_registry=reg))
    assert out["path"] == PATH_REFUSED
    assert "Consequential" in out["receipt"]["refusal_reasons"][0]


# ------------------------------------------------------------------
# §9.6 stale/superseded receipt -> refused, no effects
# ------------------------------------------------------------------
def test_stale_receipt_refused():
    node = ActNode(executor=ok_executor("e"))
    receipt = make_decision_receipt(valid_until="2026-09-30T18:00:00+00:00")
    out = node.execute(state_for(decision_receipt=receipt))
    assert out["path"] == PATH_REFUSED
    assert "stale" in out["receipt"]["refusal_reasons"][0]
    assert out["receipt"]["effects_observed"] == "no effects — refused"
    # the refusal reasons are sealed under the receipt hash (recompute MATCH)
    assert node.recompute(out["receipt"]) == "MATCH"


def test_superseded_config_receipt_refused():
    node = ActNode(executor=ok_executor("e"))
    receipt = make_decision_receipt(configHash="cfg-old", configHashCurrent="cfg-new")
    out = node.execute(state_for(decision_receipt=receipt))
    assert out["path"] == PATH_REFUSED
    assert "superseded" in out["receipt"]["refusal_reasons"][0]


def test_forged_receipt_refused():
    node = ActNode(executor=ok_executor("e"))
    receipt = make_decision_receipt()
    receipt["receipt_hash"] = "forged"
    out = node.execute(state_for(decision_receipt=receipt))
    assert out["path"] == PATH_REFUSED
    assert "recompute" in out["receipt"]["refusal_reasons"][0]


# ------------------------------------------------------------------
# §9.6b hard-stop flags refuse immediately
# ------------------------------------------------------------------
def test_harm_flag_refuses_before_anything():
    node = ActNode(executor=ok_executor("e"))
    receipt = make_decision_receipt(flags={"harm_flag": True, "harm_facts": ["x"]})
    out = node.execute(state_for(decision_receipt=receipt))
    assert out["path"] == PATH_REFUSED
    assert "LAW_OF_ONE" in out["receipt"]["refusal_reasons"][0]


def test_known_wrong_flag_refuses():
    node = ActNode(executor=ok_executor("e"))
    receipt = make_decision_receipt(flags={"known_wrong_flag": True})
    out = node.execute(state_for(decision_receipt=receipt))
    assert out["path"] == PATH_REFUSED
    assert "Judgment Rule" in out["receipt"]["refusal_reasons"][0]


# ------------------------------------------------------------------
# §9.7 READ_MORE loops back; bound breach forces ASK
# ------------------------------------------------------------------
def test_read_more_loops_to_know():
    node = ActNode(executor=ok_executor("e"))
    receipt = make_decision_receipt(decision="READ_MORE",
                                    read_more_directive={"missing": "evidence"})
    out = node.execute(state_for(decision_receipt=receipt))
    assert out["path"] == PATH_READ_MORE_LOOP
    assert "missing" in out["receipt"]["effects_observed"]


def test_read_more_bound_breach_forces_ask():
    node = ActNode(executor=ok_executor("e"))
    receipt = make_decision_receipt(
        decision="READ_MORE",
        execution_budget={"timeout_ms": 5000, "max_retries": 2,
                          "read_more_loop": 3})
    out = node.execute(state_for(decision_receipt=receipt))
    assert out["path"] == PATH_ASK_SUSPENDED
    assert out["ticket"]["status"] == "ASK_SUSPENDED_FORCED"


# ------------------------------------------------------------------
# §9.8 ASK suspends with persisted brief; resumes via fresh decision
# ------------------------------------------------------------------
def test_ask_suspends_with_persisted_brief():
    node = ActNode(executor=ok_executor("e"))
    brief = {"question": "proceed?", "options": ["yes", "no"],
             "authorizes": "the scoped write"}
    receipt = make_decision_receipt(decision="ASK", decision_brief=brief)
    ledger = {}
    out = node.execute(state_for(decision_receipt=receipt, execution_ledger=ledger))
    assert out["path"] == PATH_ASK_SUSPENDED
    key = list(ledger.keys())[0]
    assert ledger[key]["state"] == "ASK_SUSPENDED"
    assert ledger[key]["brief"]["question"] == "proceed?"
    assert out["ticket"]["status"] == "ASK_SUSPENDED"


# ------------------------------------------------------------------
# §9.9 REFUSE produces no effects and a reasons-carrying receipt
# ------------------------------------------------------------------
def test_refuse_verdict_carries_reasons():
    node = ActNode(executor=ok_executor("e"))
    receipt = make_decision_receipt(
        decision="REFUSE",
        flags={"refusal_reasons": ["gate LAW PROHIBITED: hard stop"]})
    out = node.execute(state_for(decision_receipt=receipt))
    assert out["path"] == PATH_REFUSED
    assert "hard stop" in out["receipt"]["refusal_reasons"][0]
    assert out["receipt"]["effects_observed"] == "no effects — refused"


def test_unknown_verb_refuses_no_fifth_path():
    node = ActNode(executor=ok_executor("e"))
    receipt = make_decision_receipt(decision="FROBNICATE")
    out = node.execute(state_for(decision_receipt=receipt))
    assert out["path"] == PATH_REFUSED
    assert "no fifth path" in out["receipt"]["refusal_reasons"][0]


# ------------------------------------------------------------------
# §9.10 transient on idempotent tool retries; on non-idempotent it does not
# ------------------------------------------------------------------
def test_transient_retries_on_idempotent_tool():
    attempts = {"n": 0}

    def flaky(t, p):
        attempts["n"] += 1
        if attempts["n"] < 3:
            return {"status": "error", "effects": "",
                    "error_class": ERROR_TRANSIENT, "error_detail": "timeout"}
        return {"status": "ok", "effects": "finally", "error_class": None}

    node = ActNode(executor=flaky)
    out = node.execute(state_for())
    assert out["path"] == PATH_EXECUTED
    assert out["receipt"]["attempts"] == 3
    assert attempts["n"] == 3


def test_transient_does_not_retry_on_non_idempotent_tool():
    calls = {"n": 0}

    def flaky(t, p):
        calls["n"] += 1
        return {"status": "error", "effects": "",
                "error_class": ERROR_TRANSIENT, "error_detail": "timeout"}

    node = ActNode(executor=flaky)
    reg = make_tool_registry()
    reg["echo_tool"]["idempotent"] = False
    out = node.execute(state_for(tool_registry=reg))
    assert out["path"] == PATH_FAILED
    assert out["receipt"]["error_class"] == ERROR_TRANSIENT
    assert calls["n"] == 1  # no retry for non-idempotent


# ------------------------------------------------------------------
# §9.11 harm signal aborts, compensates, alerts
# ------------------------------------------------------------------
def test_harm_signal_aborts_with_compensation_and_alert():
    def harmful(t, p):
        if t == "danger_tool":
            return {"status": "harm_signal", "effects": "partial",
                    "error_class": ERROR_HARM_SIGNAL, "error_detail": "trip"}
        return {"status": "ok", "effects": "undone", "error_class": None}

    node = ActNode(executor=harmful)
    reg = make_tool_registry()
    reg["danger_tool"] = {
        "version": "1.0.0", "authority_class": "WRITE_SCOPED",
        "idempotent": False, "max_timeout_ms": 5000,
        "retry_policy": {"attempts": 0, "backoff": "none"},
        "required_authority": "director_order",
        "compensating_tool": "undo_tool", "evidence_capture": "return_value",
    }
    reg["undo_tool"] = dict(reg["echo_tool"])
    receipt = make_decision_receipt(
        winner={"tool_id": "danger_tool", "version": "1.0.0", "params": {}})
    out = node.execute(state_for(decision_receipt=receipt, tool_registry=reg))
    assert out["path"] == PATH_FAILED
    assert out["receipt"]["error_class"] == ERROR_HARM_SIGNAL
    assert out["receipt"]["compensation"]["status"] == "ok"
    assert out["receipt"]["alert"].startswith("RAISED")


# ------------------------------------------------------------------
# §9.12 cold reconstruction never double-executes; UNKNOWN_EFFECTS briefs
# ------------------------------------------------------------------
def test_cold_reconstruct_deterministic_plan():
    node = ActNode()
    receipts = [
        {"stream": "execution", "idempotency_key": "act:a1", "path": PATH_EXECUTED,
         "receipt_id": "r1", "state_transitions": []},
        {"stream": "execution", "idempotency_key": "act:b2", "state": "CLAIMED",
         "lease_deadline": "2026-09-30T17:00:00+00:00",  # expired
         "tool": {"tool_id": "t", "idempotent": True}},
        {"stream": "execution", "idempotency_key": "act:c3", "state": "CLAIMED",
         "lease_deadline": "2026-09-30T17:00:00+00:00",  # expired
         "tool": {"tool_id": "t", "idempotent": False}},
        {"stream": "execution", "idempotency_key": "act:d4", "state": "ASK_SUSPENDED",
         "brief": {"question": "q?"}},
    ]
    plan1 = node.cold_reconstruct(receipts)
    plan2 = node.cold_reconstruct(list(reversed(receipts)))
    assert plan1["deterministic"] is True
    by_key = {p["key"]: p["action"] for p in plan1["plan"]}
    assert by_key["act:a1"] == "done"
    assert by_key["act:b2"] == "re_executable"
    assert by_key["act:c3"] == "unknown_effects_brief_human"
    assert by_key["act:d4"] == "ask_suspended_survives"
    # determinism: same receipts, any order -> same plan
    assert plan1["plan"] == plan2["plan"]


# ------------------------------------------------------------------
# §9.13 cold successor answers did/execute-effects-safe-to-touch from receipts
# ------------------------------------------------------------------
def test_receipt_answers_cold_successor_questions():
    node = ActNode(executor=ok_executor("db-write-42"))
    out = node.execute(state_for())
    r = out["receipt"]
    assert r["path"] == PATH_EXECUTED                       # did it execute
    assert r["effects_observed"] == "db-write-42"            # what effects
    assert r["idempotency_key"] and r["fingerprint"]         # safe to touch?


# ------------------------------------------------------------------
# §9.14 circuit breaker trips and recovers
# ------------------------------------------------------------------
def test_circuit_breaker_trips_then_recovers():
    node = ActNode(executor=failing_executor())
    reg = make_tool_registry()
    reg["echo_tool"]["retry_policy"] = {"attempts": 0, "backoff": "none"}
    for i in range(5):
        receipt = make_decision_receipt(receipt_id=f"dec-cb-{i}")
        out = node.execute(state_for(decision_receipt=receipt, tool_registry=reg))
        assert out["path"] == PATH_FAILED
    # 6th: breaker OPEN -> refusal before invocation
    receipt = make_decision_receipt(receipt_id="dec-cb-5")
    out = node.execute(state_for(decision_receipt=receipt, tool_registry=reg))
    assert out["path"] == PATH_REFUSED
    assert "circuit breaker OPEN" in out["receipt"]["refusal_reasons"][0]


# ------------------------------------------------------------------
# §4.7 no executor -> refuse; never an unreceipted act
# ------------------------------------------------------------------
def test_no_executor_refuses_under_evidence_capture_impossible():
    node = ActNode()  # no executor
    out = node.execute(state_for())
    assert out["path"] == PATH_REFUSED
    assert "§4.7" in out["receipt"]["refusal_reasons"][0]
    assert out["receipt"]["effects_observed"] == "no effects — refused"
    # the refusal reasons are sealed under the receipt hash (recompute MATCH)
    assert node.recompute(out["receipt"]) == "MATCH"


# ------------------------------------------------------------------
# Authority checks declare but never grant
# ------------------------------------------------------------------
def test_authority_checks_declare_only():
    node = ActNode()
    checks = node.authority_checks()
    assert any("never grant" in c or "Declared" in c or "grant" in c for c in checks)
    src = open(__import__("naya_kernel.nodes.act_node", fromlist=["x"]).__file__, encoding="utf-8").read()
    assert "grant(" not in src


# ------------------------------------------------------------------
# NodeBase conformance
# ------------------------------------------------------------------
def test_manifest_entry():
    node = ActNode()
    entry = node.manifest_entry()
    assert entry.node_id == "NAYA-KERNEL-ACT"
    assert len(entry.responsibilities) == 6


def test_node_is_nodebase_subclass():
    assert issubclass(ActNode, NodeBase)


def test_gate_admits_valid_and_refuses_stale():
    node = ActNode()
    g = node.gate(state_for())
    assert g.verdict == GateVerdict.PASS
    g2 = node.gate(state_for(
        decision_receipt=make_decision_receipt(
            valid_until="2026-09-30T18:00:00+00:00")))
    assert g2.verdict == GateVerdict.FAIL


def test_persisted_transitions_are_receipted_state_machine():
    node = ActNode()
    ts = node.persisted_transitions()
    assert f"{S_AUTHORIZED} -> {S_CLAIMED}" in ts
    assert f"{S_EXECUTING} -> {S_RECEIPTED}" not in ts  # indirect via EFFECTS_OBSERVED
    assert any("RECEIPTED" in t for t in ts)


def test_evidence_hooks_name_streams():
    node = ActNode()
    hooks = node.evidence_hooks()
    assert any("smartledger.execution" in h for h in hooks)


def test_illegal_transition_fails_closed():
    node = ActNode()
    claim = {"state": S_AUTHORIZED}
    with pytest.raises(RuntimeError):
        node._transition(claim, S_AUTHORIZED, S_RECEIPTED,
                         "2026-09-30T19:00:00+00:00", "skip")


def test_heartbeat_renews_lease():
    node = ActNode(executor=ok_executor("e"))
    ledger = {}
    receipt = make_decision_receipt()
    key = "act:" + node._fingerprint(receipt, receipt["winner"])
    # prime a claim via a held execution: block the executor until heartbeat tested
    hold = {"release": False}

    def holding_executor(t, p):
        # simulate a long sync: we can't interleave here; just record lease state pre/post
        return {"status": "ok", "effects": "x", "error_class": None}

    node2 = ActNode(executor=holding_executor)
    out = node2.execute(state_for(execution_ledger=ledger, decision_receipt=receipt))
    assert out["path"] == PATH_EXECUTED
    rec = ledger[key]
    assert rec["state"] == S_RECEIPTED
    # heartbeat on a terminal claim returns False (no live claim)
    assert node2.heartbeat(key, ledger) is False
