from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIGRATION = ROOT / "supabase/migrations/20260930051000_harden_trigger_only_function_execution_v1.sql"


def sql() -> str:
    return " ".join(MIGRATION.read_text(encoding="utf-8").lower().split())


def test_checkpoint_trigger_function_has_safe_search_path_and_no_client_execute():
    body = sql()
    assert "alter function public.nayanet_checkpoint_receipts_immutable() set search_path = ''" in body
    assert "revoke execute on function public.nayanet_checkpoint_receipts_immutable() from public, anon, authenticated" in body


def test_consent_trigger_function_is_not_directly_client_executable():
    body = sql()
    assert "revoke execute on function public.nayanet_require_explicit_smart_connect_consent() from public, anon, authenticated" in body
