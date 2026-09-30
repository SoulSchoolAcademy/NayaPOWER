from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIG = ROOT / "supabase" / "migrations" / "20260929044000_checkpoint_receipts_rls_v1.sql"


def _sql():
    return MIG.read_text(encoding="utf-8").lower()


def test_checkpoint_receipts_rls_is_enabled_and_anon_is_revoked():
    sql = _sql()
    assert "alter table public.nayanet_checkpoint_receipts enable row level security" in sql
    assert "revoke all privileges on table public.nayanet_checkpoint_receipts from anon" in sql


def test_authenticated_access_is_owner_read_only():
    sql = _sql()
    assert "revoke all privileges on table public.nayanet_checkpoint_receipts from authenticated" in sql
    assert "grant select on table public.nayanet_checkpoint_receipts to authenticated" in sql
    assert "for select" in sql
    assert "to authenticated" in sql
    assert "using (user_id = auth.uid())" in sql
    assert "grant insert" not in sql
    assert "grant update" not in sql
    assert "grant delete" not in sql
    assert "grant truncate" not in sql
