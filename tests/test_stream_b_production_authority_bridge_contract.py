"""Fail-first contract for Stream B production authority convergence.

These tests deliberately describe the required post-bridge invariants. They do
not claim the current production SQL implementation already satisfies them.
The structural assertions document the currently-known bypass and prevent a
future implementation from silently preserving it.
"""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "supabase" / "migrations"


def _migration(name: str) -> str:
    return (MIGRATIONS / name).read_text(encoding="utf-8-sig")


def test_legacy_six_argument_intelligence_capture_path_is_explicitly_detected():
    sql = _migration("20260924100000_wire_authority_grant_into_intelligence_commit_v1.sql")
    assert "p_action = 'intelligence.capture'" in sql
    assert "p_event->'metadata'->>'authority_grant_id'" in sql
    assert "nayanet_validate_authority_grant" in sql


def test_seven_argument_path_currently_does_not_verify_gate_provenance():
    sql = _migration("20260924110000_reconcile_execution_authorization_cognition_overload_v1.sql")
    assert "p_execution_authorization jsonb" in sql
    assert "nayanet_validate_authority_grant" in sql
    # Fail-first marker: the current implementation has no portable verifier,
    # Ed25519 verification, or UniversalExecutionGate call in this SQL boundary.
    assert "UniversalExecutionGate" not in sql
    assert "verify_portable_authorization" not in sql
    assert "Ed25519" not in sql


def test_bridge_contract_requires_one_canonical_authorization_seam():
    design = (ROOT / ".naya" / "STREAM-B-PRODUCTION-AUTHORITY-BRIDGE-V1.md").read_text(
        encoding="utf-8"
    )
    assert "single production intelligence_commit verifier" in design
    assert "canonical_intelligence_commit_authorize" in design
    assert "legacy metadata grant alone" in design


def test_gate_issued_credential_must_bind_production_grant_identity():
    design = (ROOT / ".naya" / "STREAM-B-PRODUCTION-AUTHORITY-BRIDGE-V1.md").read_text(
        encoding="utf-8"
    )
    assert "execution_authorization.authority_id" in design
    assert "canonical production grant identity" in design


def test_no_claim_of_exhaustive_application_caller_inventory():
    design = (ROOT / ".naya" / "STREAM-B-PRODUCTION-AUTHORITY-BRIDGE-V1.md").read_text(
        encoding="utf-8"
    )
    assert "cannot honestly be declared exhaustively inventoried" in design
