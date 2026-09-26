"""Stream B canonical intelligence_commit bridge contract.

The database remains the persistence seam; cryptographic portable authorization
is intentionally verified by the trusted Edge Function before the service-role
RPC is reached. These tests lock the fail-closed boundaries in source.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
M = ROOT / "supabase" / "migrations" / "20260924130000_canonical_intelligence_commit_bridge_v1.sql"


def _sql() -> str:
    return M.read_text(encoding="utf-8")


def test_canonical_seam_is_service_role_only():
    sql = _sql()
    assert "nayanet_canonical_intelligence_commit" in sql
    assert "request.jwt.claim.role" in sql
    assert "CANONICAL_INTELLIGENCE_COMMIT_SERVICE_ROLE_REQUIRED" in sql
    assert "grant execute on function public.nayanet_canonical_intelligence_commit" in sql
    assert "to service_role" in sql


def test_legacy_six_arg_intelligence_capture_cannot_bypass():
    sql = _sql()
    assert sql.count("INTELLIGENCE_CAPTURE_REQUIRES_CANONICAL_VERIFIER") >= 2
    assert "p_event->'metadata'->>'authority_grant_id'" in sql


def test_canonical_seam_requires_portable_artifact_shape():
    sql = _sql()
    assert "naya/portable_authorization/v1" in sql
    assert "PORTABLE_AUTHORIZATION_REQUIRED" in sql
    assert "PORTABLE_ACTION_TYPE_MISMATCH" in sql
    assert "PORTABLE_PERMISSION_MISMATCH" in sql
    assert "PORTABLE_TARGET_MISMATCH" in sql


def test_canonical_seam_rechecks_live_grant_after_portable_verification():
    sql = _sql()
    for marker in (
        "PRODUCTION_AUTHORITY_GRANT_NOT_ACTIVE",
        "PRODUCTION_AUTHORITY_GRANT_EXPIRED",
        "PRODUCTION_AUTHORITY_ACTION_NOT_GRANTED",
        "PRODUCTION_AUTHORITY_TARGET_OUT_OF_SCOPE",
        "EVENT_AUTHORITY_GRANT_MISMATCH",
        "PORTABLE_ACTOR_GRANT_MISMATCH",
        "PORTABLE_GRANT_ID_MISMATCH",
    ):
        assert marker in sql


def test_receipt_records_same_authority_lineage_and_verification_boundary():
    sql = _sql()
    assert "'verification_boundary','nayanet-compound-intelligence:portable-ed25519-v1'" in sql
    assert "v_grant.grant_id" in sql
    assert "v_grant.issuer_id" in sql
    assert "v_grant.source_event_id" in sql


def test_persistence_happens_only_inside_canonical_seam():
    sql = _sql()
    seam_start = sql.index("create or replace function public.nayanet_canonical_intelligence_commit")
    seam_end = sql.index("$function$;", seam_start)
    seam = sql[seam_start:seam_end]
    assert "insert into public.nayanet_cognition_events" in seam
    assert "insert into public.nayanet_execution_receipts" in seam
    assert "return jsonb_build_object" in seam
