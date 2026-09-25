from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIGRATION = ROOT / "supabase/migrations/20260925000000_require_human_authority_root.sql"

def test_authority_issuance_requires_root_or_active_parent():
    source = MIGRATION.read_text(encoding="utf-8")
    for marker in ("nayanet_authority_roots", "AUTHORITY_ROOT_OR_PARENT_REQUIRED", "AUTHORITY_PARENT_NOT_ACTIVE", "AUTHORITY_ROOT_ACTION_NOT_GRANTED", "v_parent.scope @> p_scope", "v_root.scope @> p_scope"):
        assert marker in source
    assert "p_parent_authority->>'grant_id'" in source
    assert "status = 'ACTIVE'" in source

def test_authority_root_has_no_authenticated_write_policy():
    source = MIGRATION.read_text(encoding="utf-8")
    assert "revoke all on table public.nayanet_authority_roots from anon, authenticated, public" in source
    assert "for insert" not in source
    assert "for update" not in source
    assert "for delete" not in source
