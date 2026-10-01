import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "supabase" / "PRODUCTION-MIGRATION-LEDGER-V1.json"
CAPABILITY = "20260930235959"
SUPERSESSION = "20261001000100"

def test_ai1_pending_migrations_apply_in_declared_dependency_order():
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    pending = {row["name"]: row for row in ledger.get("pending", [])}
    cap = pending["ai1_capability_carry_v1"]
    sup = pending["ai1_supersede_capability_integrity_v1"]
    assert cap["version"] == CAPABILITY
    assert sup["version"] == SUPERSESSION
    assert int(cap["version"]) < int(sup["version"])
    assert Path(cap["path"]).exists()
    assert Path(sup["path"]).exists()
    source = Path(sup["path"]).read_text(encoding="utf-8")
    assert "Depends on:" in source
    assert "20260930235959_ai1_capability_carry_v1.sql" in source

def test_ai1_pending_ledger_is_sorted_by_migration_version():
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    versions = [str(row["version"]) for row in ledger.get("pending", [])]
    assert versions == sorted(versions)
