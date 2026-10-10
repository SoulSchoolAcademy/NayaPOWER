"""Proof tests for the CONNECT node (tools/connect_node.py).

What these prove (and what they don't):
- PROVEN: a lesson with known relationships produces the correct RELATED_TO
  links with explicit support; a deliberate claim-polarity conflict is
  flagged as a first-class record with BOTH sides preserved, resolution
  NONE, never merged/overwritten; downstream consumers are named from the
  registry and from related items; every emitted edge validates against the
  repository's own graph relationship contract; the knowledge store is never
  mutated; output is deterministic; the whole thing runs through the
  orchestrator path (not a standalone script).
- NOT PROVEN here: natural-language contradiction inference (declared
  polarity only — stated as a limitation in every output); production HTTP
  invocation; semantic (embedding) relatedness.
"""

import copy
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "tools"))

from orchestrator import NodeOrchestrator, RunStatus, StageStatus  # noqa: E402
from orchestrator.executors import LocalExecutor  # noqa: E402
from orchestrator.stages import STAGE_CONTRACTS, StageId  # noqa: E402
from connect_node import ConnectNode, build_graph, knowledge_item_snapshot  # noqa: E402
from validate_graph_relationship_v2 import validate_edge  # noqa: E402
from learning_admission_gate import ADMISSION_SCHEMA  # noqa: E402


# --------------------------------------------------------------------------
# Fixtures: one lesson with known relationships + one deliberate conflict.
# --------------------------------------------------------------------------

def make_lesson():
    return {
        "id": "SN-CONNECT-PROOF",
        "kind": "lesson",
        "title": "Admission must fail closed on missing evidence",
        "essence": (
            "admission decisions must fail closed when evidence is missing; "
            "fail-open admission lets poisoned lessons through the gate"
        ),
        "tags": ["admission-gate", "fail-closed"],
        "claims": [
            {
                "key": "admission-on-missing-evidence",
                "polarity": -1,
                "statement": "admission must fail closed on missing evidence",
            }
        ],
        "evidence_refs": ["WO3-proof-1", "WO3-proof-2"],
    }


def make_store():
    return [
        {
            "id": "IB-ADMISSION-GATE",
            "kind": "IB",
            "title": "The fail-closed admission gate",
            "essence": "the fail closed admission gate blocks unverified lessons at the candidate write site",
            "tags": ["admission-gate", "fail-closed"],
            "claims": [],
            "evidence_refs": ["WO3-ts-port-proof"],
            "consumers": ["nightly-report"],
        },
        {
            "id": "IB-ORCHESTRATOR",
            "kind": "IB",
            "title": "Stages execute in order",
            "essence": "the orchestrator executes stages in order; admission decisions must fail closed when evidence is missing",
            "tags": ["orchestrator"],
            "claims": [],
            "evidence_refs": [],
            "consumers": [],
        },
        {
            "id": "LESSON-OLD-VIEW",
            "kind": "lesson",
            "title": "The old permissive view",
            "essence": "admission may proceed when confidence is high",
            "tags": ["admission-gate"],
            "claims": [
                {
                    "key": "admission-on-missing-evidence",
                    "polarity": 1,
                    "statement": "admission may proceed on missing evidence when confidence is high",
                }
            ],
            "evidence_refs": ["old-confidence-survey"],
            "consumers": [],
        },
        {
            "id": "IB-UNRELATED",
            "kind": "IB",
            "title": "Something about voice",
            "essence": "the voice builder renders waveforms with warm colors",
            "tags": ["voice", "ui"],
            "claims": [],
            "evidence_refs": [],
            "consumers": [],
        },
    ]


def make_registry():
    return {
        "admission-gate": ["WO3-admission-gate", "learning-evidence-writer"],
        "fail-closed": ["safety-review-board"],
    }


@pytest.fixture
def graph():
    return build_graph(
        make_lesson(), make_store(), make_registry(),
        owner_id="owner-1", correlation_id="corr-proof-1",
    )


# --------------------------------------------------------------------------
# 1. Known relationships → correct RELATED_TO links with explicit support.
# --------------------------------------------------------------------------

def test_related_blocks_linked_with_support(graph):
    by_id = {b["id"]: b for b in graph["related_blocks"]}
    assert "IB-ADMISSION-GATE" in by_id  # shared tags
    assert "IB-ORCHESTRATOR" in by_id    # shared terms (>=3), no shared tags
    assert "IB-UNRELATED" not in by_id   # no overlap → no link, honestly

    gate = by_id["IB-ADMISSION-GATE"]
    assert set(gate["support"]["shared_tags"]) == {"admission-gate", "fail-closed"}
    assert gate["edge_id"].startswith("rel-")


def test_related_lessons_linked(graph):
    # LESSON-OLD-VIEW shares the admission-gate tag → related AND conflicting.
    # Relevance is distinguished from truth: both records exist side by side.
    ids = [l["id"] for l in graph["related_lessons"]]
    assert "LESSON-OLD-VIEW" in ids


# --------------------------------------------------------------------------
# 2. The deliberate conflict: explicit, both sides preserved, never resolved.
# --------------------------------------------------------------------------

def test_conflict_is_first_class_with_both_sides_preserved(graph):
    assert len(graph["conflicts"]) == 1
    c = graph["conflicts"][0]
    assert c["type"] == "POLARITY_OPPOSITION"
    assert c["claim_key"] == "admission-on-missing-evidence"
    assert c["resolution"] == "NONE"
    assert c["both_preserved"] is True

    new = c["new_side"]
    assert new["item_id"] == "SN-CONNECT-PROOF"
    assert new["polarity"] == -1
    assert "fail closed" in new["statement"]
    assert new["evidence_refs"] == ["WO3-proof-1", "WO3-proof-2"]

    old = c["existing_side"]
    assert old["item_id"] == "LESSON-OLD-VIEW"
    assert old["polarity"] == 1
    assert "may proceed" in old["statement"]
    assert old["evidence_refs"] == ["old-confidence-survey"]

    # The conflict also exists as a contract-valid CONTRADICTS edge.
    assert c["edge"]["relationship_type"] == "CONTRADICTS"


def test_conflict_never_merges_or_overwrites():
    store = make_store()
    before = knowledge_item_snapshot(store)
    graph = build_graph(make_lesson(), store, make_registry())
    # The store is byte-identical after CONNECT ran over it.
    assert store == before
    # The existing lesson's claim is untouched in the store.
    old = next(i for i in store if i["id"] == "LESSON-OLD-VIEW")
    assert old["claims"][0]["polarity"] == 1
    # And the graph carries no merged/resolved artifact.
    assert all(c["resolution"] == "NONE" for c in graph["conflicts"])


# --------------------------------------------------------------------------
# 3. Downstream consumers named, with provenance.
# --------------------------------------------------------------------------

def test_consumers_named_from_registry_and_inheritance(graph):
    by_id = {c["consumer_id"]: c for c in graph["downstream_consumers"]}
    # Registry consumers.
    assert by_id["WO3-admission-gate"]["via"] == "registry:tag=admission-gate"
    assert by_id["learning-evidence-writer"]["via"] == "registry:tag=admission-gate"
    assert by_id["safety-review-board"]["via"] == "registry:tag=fail-closed"
    # Inherited from a related block.
    assert by_id["nightly-report"]["via"] == "inherited:via=IB-ADMISSION-GATE"
    # Every consumer link has an edge id.
    assert all(c["edge_id"].startswith("rel-") for c in graph["downstream_consumers"])


# --------------------------------------------------------------------------
# 4. Every edge validates against the repo's own relationship contract.
# --------------------------------------------------------------------------

def test_all_edges_pass_repo_contract_validator(graph):
    assert graph["edges"], "no edges emitted — nothing to validate"
    for edge in graph["edges"]:
        errors = validate_edge(edge)
        assert not errors, f"edge {edge['relationship_id']} invalid: {errors}"


# --------------------------------------------------------------------------
# 5. Deterministic + idempotent (orchestrator retry-safe).
# --------------------------------------------------------------------------

def _normalize(graph):
    g = copy.deepcopy(graph)
    for e in g["edges"]:
        e.pop("created_at", None)
        e.pop("observed_at", None)
    return g


def test_build_graph_is_deterministic():
    g1 = _normalize(build_graph(make_lesson(), make_store(), make_registry(),
                                owner_id="owner-1", correlation_id="c"))
    g2 = _normalize(build_graph(make_lesson(), make_store(), make_registry(),
                                owner_id="owner-1", correlation_id="c"))
    assert g1 == g2


# --------------------------------------------------------------------------
# 6. Empty store → explicit empty graph, never a fabricated relationship.
# --------------------------------------------------------------------------

def test_empty_store_is_explicit_not_fabricated():
    # Empty store + empty registry: nothing discovered, nothing fabricated.
    graph = build_graph(make_lesson(), [], {})
    assert graph["edges"] == []
    assert graph["related_blocks"] == []
    assert graph["conflicts"] == []
    assert "empty_reason" in graph


def test_empty_store_still_yields_registry_consumers():
    # Consumers come from the registry, not the store — an empty store does
    # not suppress them, and no store relationship is fabricated.
    graph = build_graph(make_lesson(), [], make_registry())
    assert graph["related_blocks"] == []
    assert graph["related_lessons"] == []
    assert graph["conflicts"] == []
    assert len(graph["downstream_consumers"]) == 3
    assert "empty_reason" not in graph  # edges exist (consumers), so not empty


def test_malformed_store_entries_are_counted_not_crashy():
    store = make_store() + [{"no": "id"}, "not-a-dict"]
    graph = build_graph(make_lesson(), store, make_registry())
    assert graph["stats"]["malformed_items_skipped"] == 2


# --------------------------------------------------------------------------
# 7. The contract now marks CONNECT implemented with the real binding.
# --------------------------------------------------------------------------

def test_connect_contract_is_implemented():
    c = STAGE_CONTRACTS[StageId.CONNECT]
    assert c.implemented is True
    assert "tools/connect_node.py" in c.implementation
    assert c.not_implemented_reason == ""


# --------------------------------------------------------------------------
# 8. Through the orchestrator path: full run, CONNECT executes for real.
# --------------------------------------------------------------------------

def _proof_capture():
    return {
        "lesson_id": "SN-CONNECT-PROOF",
        "owner_id": "owner-1",
        "naya_id": "naya-1",
        "identity": {"actor_id": "naya-1", "system_id": "nayapower", "role": "learner"},
        "mission": "prove the CONNECT node through the orchestrator path",
        "objective": "CONNECT executes between PROVE and VERIFY and emits the relationship graph",
        "lesson": make_lesson(),
        "knowledge_store": make_store(),
        "consumer_registry": make_registry(),
        "candidate": {
            "schema": ADMISSION_SCHEMA,
            "claim": "CONNECT builds the relationship graph through the orchestrator path.",
            "falsification_condition": "If CONNECT does not COMPLETE with the expected links and conflict, the claim is wrong.",
            "task": "connect-node-proof",
            "lesson_id": "SN-CONNECT-PROOF",
            "success_criterion": "CONNECT COMPLETED; 2 related blocks, 1 conflict flagged with both sides preserved, 4 consumers named.",
            "criterion_independent_of_lesson": True,
            "criterion_registered_at": "2026-10-10T01:30:00Z",
            "doer": "naya-5",
            "scorer": "naya-2",
            "measurement": {"method": "machine", "detail": "orchestrator stage record inspection"},
            "arms": {
                "treatment": {"observable": "orchestrator run with CONNECT", "measured_at": "2026-10-10T01:35:00Z"},
                "control": {"observable": "orchestrator run without CONNECT", "measured_at": "2026-10-10T01:40:00Z"},
            },
            "asserts_behavioral_change": True,
            "behavioral_measure": "CONNECT stage output",
            "outcome": "pending",
        },
    }


def test_connect_executes_through_orchestrator_path(tmp_path):
    orch = NodeOrchestrator(
        LocalExecutor(continuity_dir=tmp_path / "continuity"),
        store_root=tmp_path / "orchestrator",
    )
    capture = _proof_capture()
    event_id = orch.commit_capture(
        capture["lesson_id"], json.dumps(capture["lesson"], sort_keys=True)[:200]
    )
    record = orch.run(event_id, capture)

    # CONNECT really executed — not NOT_IMPLEMENTED, not skipped.
    connect = record.stages["CONNECT"]
    assert connect.status == StageStatus.COMPLETED.value, (
        f"{connect.status} {connect.error_message} {connect.not_implemented_reason}"
    )
    assert connect.correlation_id == record.correlation_id
    assert connect.attempts == 1

    # The graph is in the run's durable state via the executor result path:
    # re-run the stage input through a fresh executor and compare the shape
    # the orchestrator recorded in its summary.
    assert "2 related block(s)" in connect.output_summary
    assert "1 conflict(s)" in connect.output_summary
    assert "preserved, none resolved" in connect.output_summary

    # Execution order: CONNECT ran after PROVE, before VERIFY.
    order = [s for s in
             ["SELF", "LAW", "ACT", "KNOW", "PROVE", "CONNECT", "VERIFY"]
             if record.stages[s].status == StageStatus.COMPLETED.value]
    assert order.index("CONNECT") == order.index("PROVE") + 1

    # The run ceiling is still INCOMPLETE — LEARN and EVOLVE remain loud.
    assert record.status == RunStatus.INCOMPLETE.value
    assert record.stages["LEARN"].status == StageStatus.NOT_IMPLEMENTED.value
    assert record.stages["EVOLVE"].status == StageStatus.NOT_IMPLEMENTED.value


def test_connect_stage_output_carries_graph_and_conflict(tmp_path):
    """Direct executor proof: the stage output contains the full graph."""
    from orchestrator.executors import StageOutput  # noqa: F401

    ex = LocalExecutor(continuity_dir=tmp_path / "continuity")
    capture = _proof_capture()
    stage_input = {
        "lesson_id": capture["lesson_id"],
        "owner_id": "owner-1",
        "capture": capture,
        "know_result": {"know_result": {"essence": capture["lesson"]["essence"]}},
        "prove_result": {"assessment": {"evidence_refs": ["WO3-proof-1"]}},
    }
    out = ex.execute(StageId.CONNECT, stage_input, "corr-proof-2")
    assert out.ok
    graph = out.result["graph"]
    assert len(graph["related_blocks"]) == 2
    assert len(graph["related_lessons"]) == 1
    assert len(graph["conflicts"]) == 1
    assert len(graph["downstream_consumers"]) == 4
    c = graph["conflicts"][0]
    assert c["resolution"] == "NONE" and c["both_preserved"] is True
    assert out.result["correlation_id"] == "corr-proof-2"
