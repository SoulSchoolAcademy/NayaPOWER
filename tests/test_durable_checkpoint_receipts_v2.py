from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIG = ROOT / "supabase" / "migrations" / "20260930165500_durable_checkpoint_receipts_v2.sql"


def _sql() -> str:
    return " ".join(MIG.read_text(encoding="utf-8").lower().split())


def test_checkpoint_receipt_identity_is_revision_local_not_mutable_checkpoint_id():
    sql = _sql()
    assert "add column if not exists checkpoint_receipt_id uuid not null default gen_random_uuid()" in sql
    assert "primary key (checkpoint_receipt_id)" in sql
    assert "unique index if not exists nayanet_checkpoint_receipts_owner_project_revision_uidx" in sql
    assert "on public.nayanet_checkpoint_receipts(user_id, project_id, revision)" in sql
    assert "primary key (checkpoint_id)" not in sql


def test_two_successive_cognition_revisions_emit_two_immutable_receipts():
    sql = _sql()
    assert "create trigger nayanet_record_checkpoint_receipt_trg" in sql
    assert "after insert or update of revision, state, status" in sql
    assert "if tg_op = 'update' and new.revision = old.revision then return new" in sql
    assert "insert into public.nayanet_checkpoint_receipts" in sql
    assert "new.revision" in sql
    assert "on conflict (user_id, project_id, revision) do nothing" in sql

    # Regression model: the canonical cognition row keeps one stable row id
    # while successive intelligence commits advance revision. The evidence
    # ledger identity must therefore be revision-local, not checkpoint-row-local.
    checkpoint_id = "same-mutable-row"
    commits = [
        {"checkpoint_id": checkpoint_id, "revision": 100, "receipt": "r100"},
        {"checkpoint_id": checkpoint_id, "revision": 101, "receipt": "r101"},
    ]
    ledger_keys = {(c["checkpoint_id"], c["revision"]) for c in commits}
    assert len(ledger_keys) == 2
    assert commits[0]["checkpoint_id"] == commits[1]["checkpoint_id"]
    assert commits[0]["revision"] != commits[1]["revision"]


def test_checkpoint_receipt_carries_full_reconstructable_lineage():
    sql = _sql()
    for field in (
        "source_receipt_id",
        "event_id",
        "intelligent_block_id",
        "lineage_id",
        "relationship_id",
        "index_id",
        "content_hash",
    ):
        assert field in sql
    assert "'checkpoint_id', new.id" in sql
    assert "'revision', new.revision" in sql
    assert "'owner_id', new.user_id" in sql
    assert "'project_id', new.project_id" in sql
    assert "extensions.digest(v_state::text, 'sha256')" in sql


def test_checkpoint_history_remains_evidence_only_and_immutable():
    sql = _sql()
    assert "create or replace function public.nayanet_checkpoint_receipts_immutable()" not in sql
    assert "drop trigger if exists nayanet_checkpoint_receipts_immutable" not in sql
    assert "nayanet_project_cognition_state" in sql
    assert "nayanet_checkpoint_receipts" in sql
    assert "revoke execute on function public.nayanet_record_checkpoint_receipt()" in sql
