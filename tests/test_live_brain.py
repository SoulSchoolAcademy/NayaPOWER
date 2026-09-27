from pathlib import Path

import pytest

from kernel.value_calculus import ResourceCost, ValueProfile, calculate_value

from kernel.live_brain import (
    CausalVerification,
    FileBrainStore,
    GovernedBrain,
    MemoryRecord,
)


def test_registry_is_executable_and_exposes_exactly_nine_nodes():
    brain = GovernedBrain.from_repository(Path(__file__).resolve().parents[1])

    assert brain.node_names == (
        "SELF", "LAW", "ACT", "KNOW", "PROVE",
        "CONNECT", "VERIFY", "LEARN", "EVOLVE",
    )
    assert brain.registry["node_ids"] == [
        "NAYA-KERNEL-SELF", "NAYA-KERNEL-LAW", "NAYA-KERNEL-ACT",
        "NAYA-KERNEL-KNOW", "NAYA-KERNEL-PROVE", "NAYA-KERNEL-CONNECT",
        "NAYA-KERNEL-VERIFY", "NAYA-KERNEL-LEARN", "NAYA-KERNEL-EVOLVE",
    ]


def test_authority_is_independent_from_retrieval():
    brain = GovernedBrain.from_repository(Path(__file__).resolve().parents[1])

    brain.persist(MemoryRecord(
        object_id="LESSON-001",
        owner_id="owner-1",
        content="Use the retained checklist before acting.",
        provenance="test-source",
        epistemic_state="VERIFIED",
    ))

    assert brain.retrieve("checklist", owner_id="owner-1")[0].object_id == "LESSON-001"

    with pytest.raises(PermissionError):
        brain.authorize(
            action_id="ACTION-001",
            owner_id="owner-1",
            capability="send",
            authority=None,
        )


def test_persistence_survives_cold_store_reconstruction_and_retrieval():
    store_path = Path("/tmp/nayapower-live-brain-test.sqlite3")
    if store_path.exists():
        store_path.unlink()

    first = FileBrainStore(store_path)
    first.persist(MemoryRecord(
        object_id="MEM-001",
        owner_id="owner-1",
        content="The receiver must preserve provenance.",
        provenance="concept-13",
        epistemic_state="VERIFIED",
    ))
    first.close()

    cold = GovernedBrain.from_repository(
        Path(__file__).resolve().parents[1],
        store=FileBrainStore(store_path),
    )
    found = cold.retrieve("preserve provenance", owner_id="owner-1")

    assert [item.object_id for item in found] == ["MEM-001"]


def test_cvo_does_not_promote_execution_success_to_causality():
    cvo = CausalVerification(
        claim_id="CLAIM-001",
        input_fingerprint="input-a",
        intelligence_ids=("MEM-001",),
        decision_fingerprint="decision-a",
        action_id="ACTION-001",
        observation="action returned success",
        outcome="target behavior improved",
        evidence_ids=("EVIDENCE-001",),
        control_outcome="0.50",
        treatment_outcome="0.50",
    )

    assert cvo.verdict() == "NOT_PROVEN"


def test_learning_requires_later_behavioral_improvement():
    brain = GovernedBrain.from_repository(Path(__file__).resolve().parents[1])

    candidate = brain.record_learning(
        lesson_id="LESSON-002",
        source_event_id="EVENT-001",
        claimed_effect="avoid known failure",
        prior_outcome=0.40,
    )
    assert candidate["state"] == "CANDIDATE"

    assert brain.verify_learning(
        "LESSON-002",
        later_outcome=0.40,
        behavioral_change=False,
    )["state"] == "REJECTED"

    brain.record_learning(
        lesson_id="LESSON-003",
        source_event_id="EVENT-002",
        claimed_effect="use retained intelligence",
        prior_outcome=0.40,
    )
    verified = brain.verify_learning(
        "LESSON-003",
        later_outcome=0.80,
        behavioral_change=True,
    )

    assert verified["state"] == "VERIFIED"
    assert verified["improvement"] == pytest.approx(0.40)


def test_value_calculus_is_bound_to_event_outcome_and_receipt():
    brain = GovernedBrain.from_repository(Path(__file__).resolve().parents[1])

    receipt = brain.record_value(
        event_id="EVENT-VALUE-001",
        outcome_id="OUTCOME-VALUE-001",
        item_id="ACTION-001",
        dimensions={"U": 0.9, "R": 0.9, "A": 0.8, "E": 0.9, "C": 0.8, "Re": 0.7, "L": 0.6, "K": 0.5, "T": 0.8},
        profile=ValueProfile(
            profile_id="proof-profile",
            version="1",
            objective="prove retained intelligence creates value",
            priorities={"U": 1, "R": 1, "E": 1, "C": 1},
        ),
        verified_value=0.82,
        resources=ResourceCost(attention=1, time=2, compute=1),
        verification_state="VERIFIED",
    )

    assert receipt["event_id"] == "EVENT-VALUE-001"
    assert receipt["outcome_id"] == "OUTCOME-VALUE-001"
    assert receipt["verification_state"] == "VERIFIED"
    assert receipt["mvpa"] is not None


def test_graph_relationships_are_persisted_and_retrievable():
    brain = GovernedBrain.from_repository(Path(__file__).resolve().parents[1])

    relationships = brain.related("NAYA-KERNEL-LAW")

    assert relationships
    assert all(row["provenance"] for row in relationships)
    assert any(row["relationship_type"] == "GOVERNS" for row in relationships)


def test_successor_context_does_not_inherit_authority():
    brain = GovernedBrain.from_repository(Path(__file__).resolve().parents[1])
    successor = brain.create_successor("NAYA-NODE-0001", mission="continue proof")

    assert successor["identity"] != "NAYA-NODE-0001"
    assert successor["authority_inherited"] is False
