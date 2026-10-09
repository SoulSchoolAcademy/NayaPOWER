"""Tests for the ACT -> KNOW ExecutionHandoff arc (Phase 3, GAP 4).

Covers: handoff construction/validation (kernel/handoffs.py), KNOW-side
ingest as a knowledge edge (tools/know_ingest.py), and the wiring that emits
a handoff when execute_plan() completes.
"""
import json

import pytest

from kernel.handoffs import ExecutionHandoff, emit_execution_handoff
from tools.know_ingest import ingest_execution


def _handoff_dict(**kw):
    base = dict(execution_id="exec-1", action_taken="naya_node_apply")
    base.update(kw)
    return emit_execution_handoff(**base).to_dict()


# ---------------- handoff construction ----------------

def test_handoff_fields_and_schema():
    h = emit_execution_handoff(
        execution_id="exec-abc",
        action_taken="naya_node_apply",
        decision_ref="grant-1",
        outcome_observed="node state updated",
        predicted_outcome="node state updated, previous state restorable",
        provenance={"law_receipt_id": "grant-1", "act_receipt_id": "exec-abc"},
    )
    d = h.to_dict()
    assert d["schema"] == "naya.execution-handoff.v1"
    assert d["execution_id"] == "exec-abc"
    assert d["decision_ref"] == "grant-1"
    assert d["action_taken"] == "naya_node_apply"
    assert d["outcome_observed"] == "node state updated"
    assert d["predicted_outcome"] == "node state updated, previous state restorable"
    assert d["truth_state"] == "CANDIDATE"
    assert d["timestamp"]  # UTC stamp filled by the constructor helper
    assert d["provenance"]["law_receipt_id"] == "grant-1"
    assert d["provenance"]["act_receipt_id"] == "exec-abc"


def test_handoff_roundtrip_and_unknown_keys_ignored():
    h = emit_execution_handoff(execution_id="exec-1", action_taken="act")
    d = h.to_dict()
    assert ExecutionHandoff.from_dict(d) == h
    # forward-compatible: unknown keys are dropped, never crash
    assert ExecutionHandoff.from_dict({**d, "future_field": "x"}) == h


def test_handoff_truth_state_never_above_candidate():
    with pytest.raises(ValueError):
        emit_execution_handoff(execution_id="e", action_taken="a",
                               truth_state="ACTIVE")
    with pytest.raises(ValueError):
        emit_execution_handoff(execution_id="e", action_taken="a",
                               truth_state="LEARNED")


@pytest.mark.parametrize("kwargs", [
    {"execution_id": "", "action_taken": "a"},
    {"execution_id": "   ", "action_taken": "a"},
    {"execution_id": "e", "action_taken": ""},
    {"execution_id": None, "action_taken": "a"},
])
def test_emit_validates_required_fields(kwargs):
    with pytest.raises(ValueError):
        emit_execution_handoff(**kwargs)


# ---------------- KNOW-side ingest ----------------

def test_ingest_records_edge_with_lineage(tmp_path):
    edges = tmp_path / "execution-edges.jsonl"
    handoff = _handoff_dict(
        decision_ref="grant-1",
        outcome_observed="node state updated",
        predicted_outcome="node state updated, previous state restorable",
        provenance={"law_receipt_id": "grant-1", "act_receipt_id": "r-9"},
    )
    res = ingest_execution(handoff, registry_path=edges)
    assert res["status"] == "RECORDED"
    assert res["edge_id"]

    lines = edges.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    edge = json.loads(lines[0])
    assert edge["edge_id"] == res["edge_id"]
    assert edge["type"] == "EXECUTION"
    assert edge["ingested_at"]
    h = edge["handoff"]
    assert h["execution_id"] == "exec-1"
    assert h["action_taken"] == "naya_node_apply"
    assert h["truth_state"] == "CANDIDATE"
    # lineage: LAW decision link + provenance carried through
    assert h["decision_ref"] == "grant-1"
    assert h["provenance"]["law_receipt_id"] == "grant-1"
    assert h["provenance"]["act_receipt_id"] == "r-9"


def test_ingest_appends_without_clobbering(tmp_path):
    edges = tmp_path / "execution-edges.jsonl"
    r1 = ingest_execution(_handoff_dict(execution_id="e-1"), registry_path=edges)
    r2 = ingest_execution(_handoff_dict(execution_id="e-2"), registry_path=edges)
    assert r1["status"] == r2["status"] == "RECORDED"
    assert r1["edge_id"] != r2["edge_id"]
    lines = edges.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    assert json.loads(lines[0])["handoff"]["execution_id"] == "e-1"
    assert json.loads(lines[1])["handoff"]["execution_id"] == "e-2"


@pytest.mark.parametrize("handoff", [
    {},
    {"action_taken": "a"},                        # missing execution_id
    {"execution_id": "e", "action_taken": ""},     # missing action_taken
    {"execution_id": "", "action_taken": "a"},
    {"execution_id": "   ", "action_taken": "a"},
    "not-a-dict",
    None,
])
def test_ingest_refuses_fail_closed(tmp_path, handoff):
    edges = tmp_path / "execution-edges.jsonl"
    res = ingest_execution(handoff, registry_path=edges)
    assert res["status"] == "REFUSED"
    assert res["reason"]
    assert not edges.exists()  # nothing recorded on refusal


# ---------------- pipeline wiring ----------------

def _plan_and_execute(monkeypatch, tmp_path):
    from kernel import act_pipeline as ap
    from kernel.value_calculus import QualityProfile
    monkeypatch.setenv("NAYA_EXECUTION_EDGES",
                       str(tmp_path / "execution-edges.jsonl"))
    profile = QualityProfile(profile_id="p3-test", version="1",
                             objective="minimum sufficient action")
    now = 1_790_000_000.0
    authority = ap.LawAuthority(
        action="naya_node_apply", scope="naya_node_apply",
        decided_at=now - 60, expires_at=None, grant_id="grant-1")
    candidate = ap.PlanCandidate(
        candidate_id="p1", action="naya_node_apply", description="apply",
        quality={"objective_fit": 8.0, "evidence_sufficiency": 7.0,
                 "applicability": 8.0, "robustness": 7.0},
        confidence={"objective_fit": 0.9, "evidence_sufficiency": 0.8,
                    "applicability": 0.9, "robustness": 0.8},
        reversibility="REVERSIBLE",
        expected_outcome="node state updated",
        proof_requirements=("execution_receipt",), stakes="low",
    )
    plan, plan_receipt = ap.plan_action(authority, [candidate], profile, now=now)
    assert plan is not None and plan_receipt.phase == "PLAN_ACCEPTED"
    receipt = ap.execute_plan(
        plan, executor=lambda p: "node state updated",
        re_resolve=lambda: authority, now=now, profile=profile)
    return receipt


def test_pipeline_emits_handoff_on_completion(tmp_path, monkeypatch):
    receipt = _plan_and_execute(monkeypatch, tmp_path)
    assert receipt.phase == "EXECUTION_COMPLETED"
    lines = (tmp_path / "execution-edges.jsonl").read_text(
        encoding="utf-8").splitlines()
    assert len(lines) == 1
    edge = json.loads(lines[0])
    h = edge["handoff"]
    assert h["execution_id"] == receipt.receipt_id
    assert h["action_taken"] == "naya_node_apply"
    assert h["decision_ref"] == "grant-1"          # LAW grant linkage
    assert h["outcome_observed"] == "node state updated"
    assert h["predicted_outcome"] == "node state updated"
    assert h["truth_state"] == "CANDIDATE"
    assert h["provenance"]["act_receipt_id"] == receipt.receipt_id
    assert h["provenance"]["law_receipt_id"] == "grant-1"


def test_pipeline_survives_ingest_failure(tmp_path, monkeypatch, capsys):
    """KNOW ingest failure must never fail the execution itself."""
    import tools.know_ingest as ki

    def boom(handoff, registry_path=None):
        raise RuntimeError("KNOW down")

    monkeypatch.setattr(ki, "ingest_execution", boom)
    receipt = _plan_and_execute(monkeypatch, tmp_path)
    assert receipt.phase == "EXECUTION_COMPLETED"
    captured = capsys.readouterr()
    assert "KNOW ingest failed" in captured.err
