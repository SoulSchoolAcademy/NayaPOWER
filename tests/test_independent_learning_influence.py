"""Verifier for the LIVE learning-influence receipt.

Same classification as tests/test_causal_learning_experiment_contract.py: the
prior FileNotFoundError was a PLACEMENT/ENVIRONMENT defect (a live-evidence
verifier collected on every offline run), not an implementation or contract
failure. The live jobs succeeded in run 36445685851.

Skipped explicitly when the receipt is absent; asserted in full when present.
The logic is extracted into `verify_learning_influence_receipt` so
tests/test_learning_receipt_verifier_bites.py can prove it still rejects a
degraded receipt.
"""

import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
RECEIPT = REPO / "learning-influence-receipt.json"


def verify_learning_influence_receipt(r: dict) -> None:
    """The learning-influence receipt contract. Every assertion is load-bearing."""
    assert r["schema"] == "NAYANET_LEARNING_INFLUENCE_RUNTIME_V1"
    assert r["status"] == "PASS"
    assert r["target_id"] == "NAYA-NODE-0001"
    assert r["learning_level"] == "E5_CAN_TEACH"
    assert r["source_event_id"] == "NAYA-NODE-0001-APPLY"
    # Stored information is not learned intelligence: a behavioural change must exist.
    assert r["behavioral_change"] is True
    # Treatment must outscore control. A stored string cannot satisfy this.
    assert r["control_verified_value"] < r["treatment_verified_value"]
    assert r["fresh_session_decision"] == "USE_VERIFIED_LEARNING_CONTEXT"
    assert r["influenced"] is True
    # Lineage: the decision must cite the same learning id that was retained.
    assert r["learning_id"] == r["evidence_id_from_decision"]


def test_independent_learning_influence_receipt():
    if not RECEIPT.exists():
        pytest.skip(
            "LIVE receipt 'learning-influence-receipt.json' is absent. This test verifies LIVE "
            "runtime evidence and executes inside .github/workflows/live-supabase-runtime-proof.yml "
            "once the runtime writes it. It is not satisfiable offline. SKIPPED, not passed."
        )
    verify_learning_influence_receipt(json.loads(RECEIPT.read_text(encoding="utf-8")))
