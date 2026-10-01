"""Source contract for the owner-scoped GitHub projection target resolver.

This is intentionally a source-level gate. Runtime/database proof remains a
separate acceptance rung and must not be inferred from this test.
"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MIGRATION = ROOT / "supabase" / "migrations" / "20261001204000_owner_scoped_github_projection_target_v1.sql"


def source() -> str:
    return MIGRATION.read_text(encoding="utf-8")


def test_projection_target_resolver_uses_authenticated_owner_and_existing_binding_registry():
    sql = source()
    assert "auth.uid()" in sql
    assert "nayanet_smart_connect_participation" in sql
    assert "sp.member_id = v_actor" in sql
    assert "sp.door = 'github_app'" in sql
    assert "sp.status = 'active'" in sql
    assert "lower(b->>'repository') = v_repository" in sql


def test_projection_target_resolver_fails_closed_for_missing_or_ambiguous_binding():
    sql = source()
    assert "GITHUB_PROJECTION_TARGET_NOT_BOUND" in sql
    assert "GITHUB_PROJECTION_TARGET_AMBIGUOUS" in sql
    assert "if v_count = 0" in sql
    assert "if v_count > 1" in sql


def test_projection_target_resolver_does_not_grant_service_role_or_anon_access():
    sql = source()
    assert "from public, anon, service_role" in sql
    assert "to authenticated" in sql
