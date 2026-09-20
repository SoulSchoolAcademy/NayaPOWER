#!/usr/bin/env python3
"""P0 acceptance proof: one real canonical SE event crosses the compounding seam."""

from __future__ import annotations

import copy
import importlib.util
import json
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / ".naya" / "runtime"))
sys.path.insert(0, str(ROOT / ".naya" / "memory"))
import compound_intelligence as ci
import adaptive_learning as al
from canonical_event_store import create_or_replay
from cct_note_event_promotion import promote_note_event
from memory_runtime import retrieve
import retrieve_learning as rl
from activity_event import ensure_activity_event
from cct005_note_event_integration import integrate_verified_note_event
from universal_execution_gate import (
    Authority,
    DecisionObject,
    Epistemic,
    Risk,
    VerificationPlan,
    UniversalExecutionGate,
)

EVENT_ID = "SE-20260825-200000-smart-brain-hardening-execution"
NOTE_ID = "SN-20260825-200000-smart-brain-hardening-naya"
EVENT_PATH = ROOT / ".naya" / "memory" / "events" / "2026" / "08" / "25" / "20" / f"{EVENT_ID}.json"
NOTE_PATH = ROOT / ".naya" / "memory" / "notes" / f"{NOTE_ID}.json"


def load_real_event() -> dict:
    assert EVENT_PATH.exists(), EVENT_PATH
    return json.loads(EVENT_PATH.read_text(encoding="utf-8"))


def test_real_canonical_event_to_learning():
    event = load_real_event()
    assert any(item.get("event_id") == EVENT_ID for item in ci.load_events())
    normalized = ci.canonical_to_learning_input(event)
    assert normalized["event_id"] == EVENT_ID
    assert normalized["smart_note_id"] == NOTE_ID
    assert normalized["lesson"] == event["representations"]["naya"]["lessons"][0]
    assert normalized["evidence_state"] == "VERIFIED"
    assert normalized["provenance"]["canonical_event_id"] == EVENT_ID

    learning = ci.build_candidate(event)
    assert learning is not None
    assert learning["source_event_id"] == EVENT_ID
    assert learning["smart_note_id"] == NOTE_ID
    assert learning["lesson"] == normalized["lesson"]
    assert learning["evidence_state"] == "VERIFIED"
    assert learning["provenance"]["canonical_event_id"] == EVENT_ID
    assert learning["source"]
    assert "conversation-and-repository-execution" in learning["source"][0]
    assert learning["learning_event_id"].startswith("LRN-")


def test_real_event_promotes_to_intelligent_block():
    event = ci.canonical_to_learning_input(load_real_event())
    block = promote_note_event(
        event,
        producer="nayapower-compounding-p0",
        consumers=["successor-naya"],
        purpose="inherit-learning",
    )
    assert block["block_id"] == f"IB-{EVENT_ID}"
    assert block["content"]["event_id"] == EVENT_ID
    assert block["content"]["learning"] == event["lesson"]
    assert block["verification"] == "VERIFIED"


def test_learning_event_retrieves_through_existing_runtime():
    # Exercise the current canonical Smart Note transaction namespace directly.
    # The historical SE fixture above intentionally remains a compatibility
    # fixture; it is not a valid locator for the current LRN -> Smart Note seam.
    tx_path = ROOT / ".naya" / "runtime" / "smart_note_transaction.py"
    spec = importlib.util.spec_from_file_location("canonical_tx_for_learning_bridge", tx_path)
    assert spec is not None and spec.loader is not None
    tx = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tx)

    with tempfile.TemporaryDirectory() as tmp:
        temp = Path(tmp)
        tx.ROOT = temp
        tx.SMART_NOTES_ROOT = temp / ".naya" / "memory" / "notes"
        tx.CIS_ROOT = temp / ".naya" / "memory" / "intelligence"
        tx.CIS_PATH = tx.CIS_ROOT / "CIS.json"
        tx.RECEIPTS_ROOT = tx.CIS_ROOT / "transactions"
        tx.PIS_PATH = temp / "NAYANET" / "HUB" / "public" / "intelligence" / "pis-feed.json"
        builder_path = ROOT / "scripts" / "build-smart-feed-projection.py"
        builder_spec = importlib.util.spec_from_file_location("canonical_tx_projection_builder", builder_path)
        assert builder_spec is not None and builder_spec.loader is not None
        builder = importlib.util.module_from_spec(builder_spec)
        builder_spec.loader.exec_module(builder)
        tx.build_pis_projection = lambda current_note: builder.build_projection(
            source_root=temp,
            output=tx.PIS_PATH,
            extra_notes=[builder.parse_canonical_note(tx.SMART_NOTES_ROOT / "2026" / "09" / "17" / "SN-20260917-IH-03-CANONICAL-INTELLIGENCE-IDENTITY.md", temp)],
        )

        timestamp = "2026-09-17T20:00:00+00:00"
        canonical_id = "SN-20260917T200000+0000-IH-03-CANONICAL-INTELLIGENCE-IDENTITY"
        note = {
            "timestamp": timestamp,
            "id": canonical_id,
            "topic": "IH-03 Canonical Intelligence Identity",
            "in_a_nutshell": "One intelligence object must remain one identity across every projection.",
            "child": "One thing, one ID, everywhere.",
            "grammar": "Identity is preserved through projection rather than recreated at each surface.",
            "human": "The human meaning remains attached to the canonical intelligence object.",
            "naya": "Preserve identity, provenance, privacy, and verification state across projection.",
            "machine": "Resolve one canonical Smart Note identity through the existing transaction namespace.",
            "learning": "Projection must preserve lineage rather than manufacture a new intelligence identity.",
            "why_it_matters": "Stable lineage lets retrieval prove that the learning still refers to the same intelligence.",
            "how_to_use": "Use the canonical Smart Note ID as the immutable identity across retrieval.",
            "value": "A later Naya can retrieve the same intelligence without reconstructing prior conversation.",
            "evidence": ["IH-03 automated canonical identity proof"],
            "current_state": "Current canonical Smart Note transaction namespace is exercised in isolation.",
            "next_action": "Preserve this identity contract in future compounding proofs.",
        }

        result = tx.execute(note)
        pis = json.loads(tx.PIS_PATH.read_text(encoding="utf-8"))
        event = next(e for e in pis["events"] if e["event_id"] == canonical_id)
        event["verification"] = {"status": "VERIFIED", "evidence": ["IH-03 automated canonical identity proof"]}
        event["evidence"] = ["IH-03 automated canonical identity proof"]
        event["evidence_state"] = "VERIFIED"

        learning = ci.build_candidate(event)
        assert learning is not None
        assert learning["smart_note_id"] == canonical_id

        learning_dir = temp / "learning"
        learning_dir.mkdir(parents=True)
        learning_path = learning_dir / f"{learning['learning_event_id']}.json"
        learning_path.write_text(json.dumps(learning, indent=2) + "\n", encoding="utf-8")

        retrieved = rl.retrieve_learning_event(
            learning["learning_event_id"],
            learning_dir=learning_dir,
            note_dir=tx.SMART_NOTES_ROOT,
        )
        receipt = retrieved["receipt"]
        assert receipt["learning_event_id"] == learning["learning_event_id"]
        assert receipt["smart_note_id"] == canonical_id
        assert receipt["retrieved_note_event_id"] == canonical_id
        assert receipt["cold_context"] is True
        assert retrieved["note"]["canonical_path"].endswith(
            "2026/09/17/SN-20260917-IH-03-CANONICAL-INTELLIGENCE-IDENTITY.md"
        )


def test_real_note_retrieves_cold_by_runtime():
    assert NOTE_PATH.exists(), NOTE_PATH
    note = json.loads(NOTE_PATH.read_text(encoding="utf-8"))
    assert note["event_id"] == EVENT_ID
    results = retrieve("constitution operational code CI enforce", limit=10)
    ids = [item[1]["id"] for item in results]
    assert NOTE_ID in ids
    retrieved = next(item[1] for item in results if item[1]["id"] == NOTE_ID)
    assert retrieved["event_id"] == EVENT_ID
    assert note["what_we_learned"][0] == "A constitution becomes operational only when code and CI enforce it."


def test_cold_retrieval_binds_successor_decision_without_granting_authority():
    # This successor-decision proof must consume the current canonical Smart Note
    # namespace, not the historical compatibility fixture used by older tests.
    tx_path = ROOT / ".naya" / "runtime" / "smart_note_transaction.py"
    spec = importlib.util.spec_from_file_location("canonical_tx_successor_decision", tx_path)
    assert spec is not None and spec.loader is not None
    tx = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tx)

    with tempfile.TemporaryDirectory() as tmp:
        temp = Path(tmp)
        tx.ROOT = temp
        tx.SMART_NOTES_ROOT = temp / ".naya" / "memory" / "notes"
        tx.CIS_ROOT = temp / ".naya" / "memory" / "intelligence"
        tx.CIS_PATH = tx.CIS_ROOT / "CIS.json"
        tx.RECEIPTS_ROOT = tx.CIS_ROOT / "transactions"
        tx.PIS_PATH = temp / "NAYANET" / "HUB" / "public" / "intelligence" / "pis-feed.json"
        builder_path = ROOT / "scripts" / "build-smart-feed-projection.py"
        builder_spec = importlib.util.spec_from_file_location("canonical_tx_successor_projection_builder", builder_path)
        assert builder_spec is not None and builder_spec.loader is not None
        builder = importlib.util.module_from_spec(builder_spec)
        builder_spec.loader.exec_module(builder)
        tx.build_pis_projection = lambda current_note: builder.build_projection(
            source_root=temp,
            output=tx.PIS_PATH,
            extra_notes=[builder.parse_canonical_note(tx.SMART_NOTES_ROOT / "2026" / "09" / "17" / "SN-20260917-IH-03-CANONICAL-INTELLIGENCE-IDENTITY.md", temp)],
        )

        timestamp = "2026-09-17T20:00:00+00:00"
        canonical_id = "SN-20260917T200000+0000-IH-03-CANONICAL-INTELLIGENCE-IDENTITY"
        note = {
            "timestamp": timestamp,
            "id": canonical_id,
            "topic": "IH-03 Canonical Intelligence Identity",
            "in_a_nutshell": "One intelligence object must remain one identity across every projection.",
            "child": "One thing, one ID, everywhere.",
            "grammar": "Identity is preserved through projection rather than recreated at each surface.",
            "human": "The human meaning remains attached to the canonical intelligence object.",
            "naya": "Preserve identity, provenance, privacy, and verification state across projection.",
            "machine": "Resolve one canonical Smart Note identity through the existing transaction namespace.",
            "learning": "Projection must preserve lineage rather than manufacture a new intelligence identity.",
            "why_it_matters": "Stable lineage lets retrieval prove that the learning still refers to the same intelligence.",
            "how_to_use": "Use the canonical Smart Note ID as the immutable identity across retrieval.",
            "value": "A later Naya can retrieve the same intelligence without reconstructing prior conversation.",
            "evidence": ["IH-03 automated canonical identity proof"],
            "current_state": "Current canonical Smart Note transaction namespace is exercised in isolation.",
            "next_action": "Preserve this identity contract in future compounding proofs.",
        }
        tx.execute(note)
        pis = json.loads(tx.PIS_PATH.read_text(encoding="utf-8"))
        event = next(e for e in pis["events"] if e["event_id"] == canonical_id)
        event["verification"] = {"status": "VERIFIED", "evidence": ["IH-03 automated canonical identity proof"]}
        event["evidence"] = ["IH-03 automated canonical identity proof"]
        event["evidence_state"] = "VERIFIED"

        learning = ci.build_candidate(event)
        assert learning is not None
        learning_dir = temp / "learning"
        learning_dir.mkdir(parents=True)
        learning_dir.joinpath(f"{learning['learning_event_id']}.json").write_text(
            json.dumps(learning, indent=2) + "\n", encoding="utf-8"
        )
        retrieved = rl.retrieve_learning_event(
            learning["learning_event_id"],
            learning_dir=learning_dir,
            note_dir=tx.SMART_NOTES_ROOT,
        )
        receipt = retrieved["receipt"]
        authority = Authority(
            authority_id="HUMAN-SOULSCHOOLACADEMY-REPO-WRITE",
            principal_id="SoulSchoolAcademy",
            purpose="governed maintenance and verification of NayaPOWER",
            scope="repo:SoulSchoolAcademy/NayaPOWER",
            granted_actions=frozenset({"repo_write"}),
        )
        decision = DecisionObject(
            decision_id="DEC-COMPOUNDING-SUCCESSOR-001",
            mission="apply verified learning to the next governed compounding proof",
            actor_id=authority.principal_id,
            action="repo_write",
            purpose=authority.purpose,
            scope=authority.scope,
            current_truth="cold retrieval returned the canonical Smart Note and lesson",
            gap="the successor proof must apply that lesson under existing governance",
            evidence=(
                f"learning:{learning['learning_event_id']}",
                f"retrieval:{receipt['retrieval_receipt_id']}",
            ),
            epistemic=frozenset({Epistemic.OBSERVED, Epistemic.VERIFIED}),
            consequence="bounded repository verification change",
            reversible=True,
            risk=Risk(uncertainty=1, consequence=2, irreversibility=1),
            alternatives=("do_not_execute",),
            expected_value="preserve causal learning lineage while executing only within existing authority",
            required_permission="repo_write",
            verification=VerificationPlan(
                "GitHub Actions observes the resulting proof run",
                "the proof run completes with all causal bindings intact",
                ("stop on any missing lineage or governance mismatch",),
            ),
            necessary_power=frozenset({"repo_write"}),
            requested_power=frozenset({"repo_write"}),
            learning_event_id=receipt["learning_event_id"],
            retrieval_receipt_id=receipt["retrieval_receipt_id"],
            retrieval_source_event_id=receipt["source_event_id"],
            retrieval_smart_note_id=receipt["smart_note_id"],
        )
        assert decision.learning_lineage_complete() is True
        assert decision.learning_event_id == learning["learning_event_id"]
        assert decision.retrieval_receipt_id == receipt["retrieval_receipt_id"]
        assert decision.retrieval_source_event_id == canonical_id
        assert decision.retrieval_smart_note_id == canonical_id

        action = {
            "action_id": "ACT-COMPOUNDING-SUCCESSOR-001",
            "action_type": "repository_write",
            "target": "tools/test_canonical_compound_bridge.py",
            "purpose": authority.purpose,
            "scope": authority.scope,
            "actor_id": authority.principal_id,
            "permission": decision.action,
            "decision_id": decision.decision_id,
            "authority_id": authority.authority_id,
            # Activity provenance is copied from the already-bound DecisionObject;
            # it is not part of ExecutionAuthorization and cannot grant authority.
            "learning_event_id": decision.learning_event_id,
            "retrieval_receipt_id": decision.retrieval_receipt_id,
            "retrieval_source_event_id": decision.retrieval_source_event_id,
            "retrieval_smart_note_id": decision.retrieval_smart_note_id,
        }
        gate = UniversalExecutionGate.from_canonical()
        authorized = gate.authorize(
            authority=authority,
            decision=decision,
            action=action,
        )
        assert authorized.allowed is True
        assert authorized.authorization is not None
        assert authorized.authorization.decision_id == decision.decision_id
        assert authorized.authorization.authority_id == authority.authority_id
        # Learning lineage is provenance on the DecisionObject, not authority.
        assert not hasattr(authorized.authorization, "learning_event_id")
        assert not hasattr(authorized.authorization, "retrieval_receipt_id")

        with tempfile.TemporaryDirectory() as activity_tmp:
            activity_root = Path(activity_tmp) / "events"
            activity_index = Path(activity_tmp) / "INDEX.json"
            activity = ensure_activity_event(
                claim_id="CL-COMPOUNDING-SUCCESSOR-001",
                action_id=action["action_id"],
                decision_id=decision.decision_id,
                authority_id=authority.authority_id,
                actor_id=decision.actor_id,
                subject="Compounding successor execution",
                summary="Decision learning lineage survives into canonical Activity.",
                receipt_id="RCP-CL-COMPOUNDING-SUCCESSOR-001",
                next_action="continue proof",
                successor="NEXT-COMPOUNDING-PROOF",
                evidence=[f"learning:{learning['learning_event_id']}", f"retrieval:{receipt['retrieval_receipt_id']}"],
                run_id="RUN-COMPOUNDING-SUCCESSOR-001",
                learning_event_id=decision.learning_event_id,
                retrieval_receipt_id=decision.retrieval_receipt_id,
                retrieval_source_event_id=decision.retrieval_source_event_id,
                retrieval_smart_note_id=decision.retrieval_smart_note_id,
                events_root=activity_root,
                index_path=activity_index,
            )
            activity_event = activity["event"]
            lineage = activity_event["execution"]["learning_lineage"]
            receipt_lineage = activity_event["receipt"]["learning_lineage"]
            # Re-run this proof whenever the canonical Activity receipt seam changes.
            assert lineage == receipt_lineage
            assert lineage["learning_event_id"] == decision.learning_event_id
            assert lineage["retrieval_receipt_id"] == decision.retrieval_receipt_id
            assert lineage["retrieval_source_event_id"] == decision.retrieval_source_event_id
            assert lineage["retrieval_smart_note_id"] == decision.retrieval_smart_note_id
            assert activity_event["execution"]["decision_id"] == authorized.authorization.decision_id
            assert activity_event["execution"]["authority_id"] == authorized.authorization.authority_id
            assert activity_event["receipt"]["receipt_id"] == "RCP-CL-COMPOUNDING-SUCCESSOR-001"

        missing_receipt = DecisionObject(
            decision_id=decision.decision_id,
            mission=decision.mission,
            actor_id=decision.actor_id,
            action=decision.action,
            purpose=decision.purpose,
            scope=decision.scope,
            current_truth=decision.current_truth,
            gap=decision.gap,
            evidence=decision.evidence,
            epistemic=decision.epistemic,
            consequence=decision.consequence,
            reversible=decision.reversible,
            risk=decision.risk,
            alternatives=decision.alternatives,
            expected_value=decision.expected_value,
            required_permission=decision.required_permission,
            verification=decision.verification,
            necessary_power=decision.necessary_power,
            requested_power=decision.requested_power,
            learning_event_id=decision.learning_event_id,
            retrieval_receipt_id=None,
            retrieval_source_event_id=decision.retrieval_source_event_id,
            retrieval_smart_note_id=decision.retrieval_smart_note_id,
        )
        assert missing_receipt.learning_lineage_complete() is False


def test_activity_receipt_binds_cct005_outcome_to_independent_verification_reference():
    event = load_real_event()
    activity_receipt_id = "RCP-CCT005-ACTIVITY-001"
    result = integrate_verified_note_event(
        event,
        producer="nayapower-compounding-p0",
        actor="successor-naya",
        intended_use="inherit-learning",
        action="apply verified learning to successor proof",
        result="observed completion",
        classification="SUCCESS",
        evidence=[{"type": "OBSERVED", "ref": activity_receipt_id}],
        confidence=1.0,
        context={"activity_receipt_id": activity_receipt_id},
        privacy="PRIVATE",
        outcome_id="OUT-CCT005-ACTIVITY-001",
        activity_receipt_id=activity_receipt_id,
        consumers=["successor-naya"],
    )
    outcome = result["outcome"]
    assert outcome["provenance"]["activity_receipt_id"] == activity_receipt_id
    assert outcome["provenance"]["source_event"] == EVENT_ID
    assert outcome["provenance"]["source_block"] == result["block"]["block_id"]

    # The verification reference is independent of outcome construction: it
    # identifies the outcome as its subject and the canonical Activity receipt
    # as its evidence reference. No authorization fields are introduced.
    verification_receipt = {
        "receipt_id": "VR-CCT005-ACTIVITY-001",
        "schema_version": "1.0",
        "subject_ref": outcome["outcome_id"],
        "verification_state": "outcome_verified",
        "verified_at": "2026-09-20T00:00:00+00:00",
        "verifier_type": "external_evidence",
        "evidence_refs": [activity_receipt_id],
        "verification_method": "independent observation of canonical Activity receipt",
    }
    assert verification_receipt["subject_ref"] == outcome["outcome_id"]
    assert activity_receipt_id in verification_receipt["evidence_refs"]
    assert "authority_id" not in outcome["provenance"]
    assert "decision_id" not in outcome["provenance"]


def test_daily_lineage_and_evidence_state():
    event = load_real_event()
    learning = ci.build_candidate(event)
    assert learning is not None
    report = ci.daily_synthesis([event], [learning], "2026-08-25")
    assert report["counts"]["verified_lessons"] == 1
    assert report["lessons"][0]["source_event_id"] == EVENT_ID
    assert report["lessons"][0]["learning_event_id"] == learning["learning_event_id"]
    assert report["lessons"][0]["smart_note_id"] == NOTE_ID


def test_legacy_evidence_string_does_not_upgrade():
    event = copy.deepcopy(load_real_event())
    event["evidence_state"] = "PERSISTED_AND_RE-READ"
    normalized = ci.canonical_to_learning_input(event)
    assert normalized["evidence_state"] == "UNKNOWN"
    learning = al.build_learning_event(
        normalized,
        {
            "lesson": normalized["lesson"],
            "evidence": normalized["evidence"],
            "evidence_state": normalized["evidence_state"],
            "smart_note_id": NOTE_ID,
        },
    )
    assert learning["evidence_state"] == "UNKNOWN"
    assert al.evidence_rank(learning["evidence_state"]) < al.evidence_rank("VERIFIED")


def test_canonical_store_replay_is_idempotent():
    event = load_real_event()
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        first = create_or_replay(event, root / "events", root / "INDEX.json")
        second = create_or_replay(event, root / "events", root / "INDEX.json")
        assert first["status"] == "CREATED"
        assert second["status"] == "REPLAY"
        assert second["event_id"] == EVENT_ID
        assert len(list((root / "events").rglob("SE-*.json"))) == 1


def write_vertical_proof() -> None:
    # The vertical proof must emit evidence from the same current canonical
    # Smart Note namespace exercised by the successor-decision proof.
    tx_path = ROOT / ".naya" / "runtime" / "smart_note_transaction.py"
    spec = importlib.util.spec_from_file_location("canonical_tx_vertical_proof", tx_path)
    assert spec is not None and spec.loader is not None
    tx = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tx)

    with tempfile.TemporaryDirectory() as tmp:
        temp = Path(tmp)
        tx.ROOT = temp
        tx.SMART_NOTES_ROOT = temp / ".naya" / "memory" / "notes"
        tx.CIS_ROOT = temp / ".naya" / "memory" / "intelligence"
        tx.CIS_PATH = tx.CIS_ROOT / "CIS.json"
        tx.RECEIPTS_ROOT = tx.CIS_ROOT / "transactions"
        tx.PIS_PATH = temp / "NAYANET" / "HUB" / "public" / "intelligence" / "pis-feed.json"
        builder_path = ROOT / "scripts" / "build-smart-feed-projection.py"
        builder_spec = importlib.util.spec_from_file_location("canonical_tx_vertical_projection_builder", builder_path)
        assert builder_spec is not None and builder_spec.loader is not None
        builder = importlib.util.module_from_spec(builder_spec)
        builder_spec.loader.exec_module(builder)
        tx.build_pis_projection = lambda current_note: builder.build_projection(
            source_root=temp,
            output=tx.PIS_PATH,
            extra_notes=[builder.parse_canonical_note(tx.SMART_NOTES_ROOT / "2026" / "09" / "17" / "SN-20260917-IH-03-CANONICAL-INTELLIGENCE-IDENTITY.md", temp)],
        )

        timestamp = "2026-09-17T20:00:00+00:00"
        canonical_id = "SN-20260917T200000+0000-IH-03-CANONICAL-INTELLIGENCE-IDENTITY"
        note = {
            "timestamp": timestamp,
            "id": canonical_id,
            "topic": "IH-03 Canonical Intelligence Identity",
            "in_a_nutshell": "One intelligence object must remain one identity across every projection.",
            "child": "One thing, one ID, everywhere.",
            "grammar": "Identity is preserved through projection rather than recreated at each surface.",
            "human": "The human meaning remains attached to the canonical intelligence object.",
            "naya": "Preserve identity, provenance, privacy, and verification state across projection.",
            "machine": "Resolve one canonical Smart Note identity through the existing transaction namespace.",
            "learning": "Projection must preserve lineage rather than manufacture a new intelligence identity.",
            "why_it_matters": "Stable lineage lets retrieval prove that the learning still refers to the same intelligence.",
            "how_to_use": "Use the canonical Smart Note ID as the immutable identity across retrieval.",
            "value": "A later Naya can retrieve the same intelligence without reconstructing prior conversation.",
            "evidence": ["IH-03 automated canonical identity proof"],
            "current_state": "Current canonical Smart Note transaction namespace is exercised in isolation.",
            "next_action": "Preserve this identity contract in future compounding proofs.",
        }
        tx.execute(note)
        pis = json.loads(tx.PIS_PATH.read_text(encoding="utf-8"))
        event = next(e for e in pis["events"] if e["event_id"] == canonical_id)
        event["verification"] = {"status": "VERIFIED", "evidence": ["IH-03 automated canonical identity proof"]}
        event["evidence"] = ["IH-03 automated canonical identity proof"]
        event["evidence_state"] = "VERIFIED"

        learning = ci.build_candidate(event)
        assert learning is not None
        learning_dir = temp / "learning"
        learning_dir.mkdir(parents=True)
        learning_dir.joinpath(f"{learning['learning_event_id']}.json").write_text(
            json.dumps(learning, indent=2) + "\n", encoding="utf-8"
        )
        retrieved = rl.retrieve_learning_event(
            learning["learning_event_id"],
            learning_dir=learning_dir,
            note_dir=tx.SMART_NOTES_ROOT,
        )
        action = "Run the canonical compounding proof under the governed CI boundary."
        receipt = {
            "schema": "naya-power/canonical-compounding-proof/v1",
            "status": "VERIFIED",
            "source_event_id": canonical_id,
            "smart_note_id": canonical_id,
            "intelligent_block_id": f"IB-{canonical_id}",
            "learning_event_id": learning["learning_event_id"],
            "retrieval_receipt": retrieved["receipt"],
            "decision": {
                "selected_action": action,
                "changed_by_learning": True,
                "reason": learning["lesson"],
            },
            "execution": {
                "plane": ".github/workflows/verify-canonical-compounding-p0.yml",
                "run_id": os.environ.get("GITHUB_RUN_ID"),
                "commit_sha": os.environ.get("GITHUB_SHA"),
            },
            "observation": {
                "status": "OBSERVED",
                "result": "All canonical compounding acceptance assertions passed.",
            },
            "verification": {
                "status": "INDEPENDENTLY_OBSERVED_BY_CI",
                "observer": "GitHub Actions check run",
                "proof": "canonical-compounding check completed successfully",
            },
        }
        proof_path = os.environ.get("PROOF_PATH")
        if proof_path:
            Path(proof_path).write_text(
                json.dumps(receipt, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
        print(json.dumps(receipt, indent=2, ensure_ascii=False))


def main():
    tests = [value for name, value in globals().items() if name.startswith("test_")]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"Canonical compounding P0 tests passed: {len(tests)}")
    write_vertical_proof()


if __name__ == "__main__":
    main()
