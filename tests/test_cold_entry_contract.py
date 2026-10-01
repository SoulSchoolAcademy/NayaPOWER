"""Adversarial tests for the cold Naya intelligent-graph entry contract.

Why this exists: PR #870 established a cold-entry contract on a stale branch
(709 commits behind, unmergeable, self-declaring CANONICAL status no other
BRAIN file uses). This battery pins the refreshed contract's guarantees:

- the ten traversal gates are exactly the governed set, in deterministic order,
  with no duplicates (fail-closed: an unknown gate name is a defect, not a pass)
- the proof law never claims runtime/behavioral/causal/production proof
- failure behavior is fail-closed (UNKNOWN stays UNKNOWN; failed authority blocks)
- the contract is registered in the machine-verified index layer with a
  matching blob SHA (self-consistency between contract and index)
- the contract's status uses the established vocabulary (PROPOSED_CANONICAL,
  not a self-declared CANONICAL)
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]

CONTRACT_REL = "BRAIN/04-INTELLIGENCE/GRAPH/0006-COLD-NAYA-GRAPH-ENTRY-CONTRACT-V1.json"

# The ten traversal gates from the build-list evidence (issue #870).
REQUIRED_GATES = [
    "IDENTITY",
    "OWNER_SCOPE",
    "AUTHORITY",
    "PRIVACY_CONSENT",
    "PROVENANCE",
    "EPISTEMIC_STATE",
    "TEMPORAL_VALIDITY",
    "SUPERSESSION_CONFLICT",
    "APPLICABILITY",
    "CONTEXT_BUDGET",
]

REQUIRED_SUCCESS_CHAIN = [
    "DISCOVER",
    "RESTORE",
    "RETRIEVE",
    "UNDERSTAND",
    "AUTHORIZE",
    "APPLY",
    "ACT",
    "OBSERVE",
    "VERIFY",
    "LEARN",
    "HANDOFF",
    "CONTINUE",
]

# Phrases the contract must never present as accomplished fact.
FORBIDDEN_CLAIMS = [
    "production-proven",
    "production proof achieved",
    "causally proven",
    "live behavioral proof",
    "behavioral proof achieved",
]


def _contract() -> dict:
    path = REPO / CONTRACT_REL
    assert path.is_file(), f"missing cold-entry contract: {CONTRACT_REL}"
    return json.loads(path.read_text(encoding="utf-8"))


def test_contract_parses_and_declares_schema():
    doc = _contract()
    assert doc["schema"] == "naya.cold-graph-entry-contract.v1"
    assert doc["purpose"], "contract must state its purpose"


def test_ten_gates_exactly_once_in_deterministic_order():
    gates = _contract()["graph_entry_gates"]
    assert gates == REQUIRED_GATES, (
        "gate list drifted from the governed ten-gate set/order; "
        f"got {gates}"
    )
    assert len(set(gates)) == len(gates), "duplicate gate names break determinism"


def test_success_chain_is_complete_and_ordered():
    chain = _contract()["cold_naya_success"]
    assert chain == REQUIRED_SUCCESS_CHAIN
    assert chain[0] == "DISCOVER" and chain[-1] == "CONTINUE"


def test_proof_law_withholds_all_four_proof_claims():
    law = _contract()["proof_law"]
    assert law["architecture_contract"] == "does not equal runtime proof"
    assert law["graph_retrieval"] == "does not equal behavioral influence"
    assert law["behavioral_influence"] == "does not equal causal proof"
    assert law["verification"] == "does not equal production proof"


def test_contract_never_claims_unproven_proof():
    text = (REPO / CONTRACT_REL).read_text(encoding="utf-8").lower()
    hits = [p for p in FORBIDDEN_CLAIMS if p in text]
    assert not hits, f"contract claims unproven proof: {hits}"


def test_failure_behavior_is_fail_closed():
    fb = _contract()["failure_behavior"]
    assert fb["unknown"] == "remain UNKNOWN", "UNKNOWN must never promote to PASS"
    assert fb["missing_provenance"] == "exclude_or_block"
    assert fb["failed_scope"] == "exclude_or_block"
    assert fb["failed_authority"] == "block", "failed authority must block, not degrade"
    assert fb["budget_exceeded"] == "stop_expansion_and_record_exclusion"


def test_status_uses_established_vocabulary():
    # No BRAIN file on main self-declares CANONICAL; brain-level status is
    # PROPOSED pending Human-Director ratification (master-map reconciliation
    # note 2026-09-30). A novel CANONICAL_* status would bypass that gate.
    status = _contract()["status"]
    assert status == "PROPOSED_CANONICAL", f"unexpected status: {status}"


def test_cold_entry_order_has_no_duplicates_and_starts_with_constitution():
    order = _contract()["cold_entry_order"]
    assert len(set(order)) == len(order), "entry order must be deterministic (no dupes)"
    assert order[0] == "CONSTITUTION", "entry must start at the constitution"


def test_edge_requirements_cover_provenance_and_epistemic_state():
    reqs = _contract()["edge_requirements"]
    for field in ("relationship_id", "relationship_type", "source_id",
                  "target_id", "status", "epistemic_state", "provenance"):
        assert field in reqs, f"edge requirement missing: {field}"


def test_retrieval_results_must_carry_why_selected_and_provenance():
    reqs = _contract()["retrieval_result_requirements"]
    for field in ("object_id", "why_selected", "relationship_path", "provenance",
                  "epistemic_state", "applicability", "freshness",
                  "conflicts_or_exclusions"):
        assert field in reqs, f"retrieval requirement missing: {field}"


def test_acceptance_does_not_promise_runtime_proof():
    acceptance = _contract()["acceptance"]
    assert acceptance, "contract must declare its acceptance"
    assert "separate live evidence" in acceptance


def test_contract_registered_in_master_map():
    master_map = (REPO / "BRAIN/MASTER-MAP.md").read_text(encoding="utf-8")
    assert "0006-COLD-NAYA-GRAPH-ENTRY-CONTRACT-V1.json" in master_map


def test_contract_in_real_tree_with_matching_blob_sha():
    import hashlib
    raw = (REPO / CONTRACT_REL).read_bytes()
    blob_sha = hashlib.sha1(b"blob %d\0" % len(raw) + raw).hexdigest()
    tree = json.loads((REPO / "BRAIN/REAL-TREE.json").read_text(encoding="utf-8"))
    entries = [e for e in tree["files"] if e["path"] == CONTRACT_REL]
    assert len(entries) == 1, "contract must appear exactly once in REAL-TREE.json"
    assert entries[0]["blob_sha"] == blob_sha, "index blob SHA must match contract bytes"


def test_index_domain_count_includes_new_contract():
    tree = json.loads((REPO / "BRAIN/REAL-TREE.json").read_text(encoding="utf-8"))
    assert tree["domain_counts"]["04-INTELLIGENCE"] == 25
