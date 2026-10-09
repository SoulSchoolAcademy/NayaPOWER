"""Tests for the REUSE (tools/reuse.py) and PROVE (tools/prove.py) steps."""
import json

import pytest

from kernel.handoffs import emit_execution_handoff
from tools.know_ingest import ingest_execution
from tools.prove import prove_execution
from tools.reuse import reuse_for_decision


class _Ctx:
    """Minimal decision context: object with .action and .scope."""
    def __init__(self, action, scope):
        self.action = action
        self.scope = scope


def _seed_registry(path):
    registry = {"entries": [
        {
            "intelligent_block_id": "IB-ACTIVE-1",
            "title": "Apply retained intelligence to naya node",
            "keywords": ["naya node", "apply", "retained intelligence"],
            "category": "EXECUTION", "topic": "NODE", "subtopic": "APPLY",
            "truth_state": "ACTIVE", "lifecycle_state": "ACTIVE",
            "captured_at": "2026-10-01",
            "provenance": {"receipt_id": "r-1"},
        },
        {
            "intelligent_block_id": "IB-CAND-1",
            "title": "Apply retained intelligence to naya node (candidate)",
            "keywords": ["naya node", "apply"],
            "category": "EXECUTION", "topic": "NODE", "subtopic": "APPLY",
            "truth_state": "CANDIDATE", "lifecycle_state": "ACTIVE",
            "captured_at": "2026-10-02",
        },
        {
            "intelligent_block_id": "IB-SUP-1",
            "title": "Apply retained intelligence to naya node (old)",
            "keywords": ["naya node", "apply"],
            "category": "EXECUTION", "topic": "NODE", "subtopic": "APPLY",
            "truth_state": "ACTIVE", "lifecycle_state": "SUPERSEDED",
            "captured_at": "2026-10-03",
        },
    ]}
    path.write_text(json.dumps(registry), encoding="utf-8")


# ---------------- REUSE ----------------

def test_reuse_attaches_active_learning(tmp_path, monkeypatch):
    reg = tmp_path / "index.json"
    _seed_registry(reg)
    monkeypatch.setenv("NAYA_SMART_NOTES_REGISTRY", str(reg))

    out = reuse_for_decision(_Ctx("naya_node_apply", "naya_node_apply"))

    assert out["attached_count"] == 1
    learning = out["learnings"][0]
    # the ACTIVE match attaches; CANDIDATE is below the ACTIVE floor and
    # SUPERSEDED is out of lifecycle — neither attaches
    assert learning["entry"]["id"] == "IB-ACTIVE-1"
    assert learning["truth_state"] == "ACTIVE"
    assert learning["provenance"]["entry_id"] == "IB-ACTIVE-1"
    assert learning["provenance"]["source"] == "smart-notes-registry"
    assert learning["provenance"]["captured_at"] == "2026-10-01"
    log = out["log_entry"]
    assert log["decision_action"] == "naya_node_apply"
    assert log["attached_learning_ids"] == ["IB-ACTIVE-1"]
    assert log["timestamp"]


def test_reuse_truth_floor_filters(tmp_path, monkeypatch):
    reg = tmp_path / "index.json"
    _seed_registry(reg)
    monkeypatch.setenv("NAYA_SMART_NOTES_REGISTRY", str(reg))

    out = reuse_for_decision(_Ctx("naya_node_apply", "naya_node_apply"),
                             truth_floor="LEARNED")
    assert out["attached_count"] == 0
    assert out["learnings"] == []
    assert out["log_entry"]["attached_learning_ids"] == []


def test_reuse_never_raises_on_empty(tmp_path, monkeypatch):
    # missing registry -> empty, not an exception
    monkeypatch.setenv("NAYA_SMART_NOTES_REGISTRY",
                       str(tmp_path / "missing.json"))
    out = reuse_for_decision(_Ctx("naya_node_apply", "naya_node_apply"))
    assert out["attached_count"] == 0
    assert out["learnings"] == []
    assert out["log_entry"]["decision_action"] == "naya_node_apply"
    # empty context -> empty, not an exception
    out2 = reuse_for_decision(_Ctx("", ""))
    assert out2["attached_count"] == 0


def test_reuse_no_match_attaches_nothing(tmp_path, monkeypatch):
    reg = tmp_path / "index.json"
    _seed_registry(reg)
    monkeypatch.setenv("NAYA_SMART_NOTES_REGISTRY", str(reg))

    out = reuse_for_decision(_Ctx("completely unrelated zebra xylophone", "qqq"))
    assert out["attached_count"] == 0
    assert out["learnings"] == []


def test_reuse_respects_max_results(tmp_path, monkeypatch):
    reg = tmp_path / "index.json"
    registry = {"entries": [
        {
            "intelligent_block_id": f"IB-ACTIVE-{i}",
            "title": "Apply retained intelligence to naya node",
            "keywords": ["naya node", "apply"],
            "category": "EXECUTION", "topic": "NODE", "subtopic": "APPLY",
            "truth_state": "ACTIVE", "captured_at": "2026-10-01",
        }
        for i in range(5)
    ]}
    reg.write_text(json.dumps(registry), encoding="utf-8")
    monkeypatch.setenv("NAYA_SMART_NOTES_REGISTRY", str(reg))

    out = reuse_for_decision(_Ctx("naya_node_apply", "naya_node_apply"),
                             max_results=2)
    assert out["attached_count"] == 2
    assert len(out["log_entry"]["attached_learning_ids"]) == 2


# ---------------- PROVE ----------------

def _seed_edge(edges_path, execution_id, predicted, observed):
    handoff = emit_execution_handoff(
        execution_id=execution_id, action_taken="naya_node_apply",
        outcome_observed=observed, predicted_outcome=predicted).to_dict()
    res = ingest_execution(handoff, registry_path=edges_path)
    assert res["status"] == "RECORDED"


def _proof_edge(edges_path):
    lines = edges_path.read_text(encoding="utf-8").splitlines()
    proof = json.loads(lines[-1])
    assert proof["type"] == "PROOF"
    return proof


def test_prove_match(tmp_path):
    edges = tmp_path / "edges.jsonl"
    _seed_edge(edges, "exec-match", "node state updated", "node state updated")

    out = prove_execution("exec-match", edges_path=edges)

    assert out["execution_id"] == "exec-match"
    assert out["verdict"] == "MATCH"
    assert out["predicted"] == "node state updated"
    assert out["observed"] == "node state updated"
    assert out["proven_at"]
    assert "flag" not in out
    assert out["proof_persisted"] is True
    proof = _proof_edge(edges)
    assert proof["execution_id"] == "exec-match"
    assert proof["verdict"] == "MATCH"
    assert proof["edge_id"] == out["proof_edge_id"]


def test_prove_mismatch_flags_deviation(tmp_path):
    edges = tmp_path / "edges.jsonl"
    _seed_edge(edges, "exec-mm", "node state updated", "node exploded")

    out = prove_execution("exec-mm", edges_path=edges)

    assert out["verdict"] == "MISMATCH"
    assert out["flag"] == "OUTCOME_DEVIATION"  # not silent
    proof = _proof_edge(edges)
    assert proof["verdict"] == "MISMATCH"
    assert proof["flag"] == "OUTCOME_DEVIATION"


def test_prove_insufficient_data_when_fields_missing(tmp_path):
    edges = tmp_path / "edges.jsonl"
    _seed_edge(edges, "exec-id", "", "")  # no prediction, no observation

    out = prove_execution("exec-id", edges_path=edges)

    assert out["verdict"] == "INSUFFICIENT_DATA"
    assert "flag" not in out
    proof = _proof_edge(edges)
    assert proof["verdict"] == "INSUFFICIENT_DATA"


def test_prove_insufficient_data_when_no_edge(tmp_path):
    edges = tmp_path / "edges.jsonl"
    out = prove_execution("exec-ghost", edges_path=edges)
    assert out["verdict"] == "INSUFFICIENT_DATA"
    assert "flag" not in out
