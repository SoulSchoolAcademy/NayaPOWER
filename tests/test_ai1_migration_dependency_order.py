import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "supabase" / "PRODUCTION-MIGRATION-LEDGER-V1.json"
CAPABILITY = "20260930235959"
SUPERSESSION = "20261001000100"

def _ledger():
    return json.loads(LEDGER.read_text(encoding="utf-8"))

def test_ai1_migrations_recorded_in_declared_dependency_order():
    # Reconciled 2026-10-05 (bf4c8e9b): both AI1 migrations were moved from
    # `pending` to `production_applied` with verified notes ("Applied 2026-10-05
    # via Management API (Naya 2, authorized by Shawn); verified in
    # schema_migrations."). The dependency-order invariant is now checked
    # against the canonical applied records, not the pending list.
    ledger = _ledger()
    applied = {row["name"]: row for row in ledger.get("production_applied", [])}
    cap = applied["ai1_capability_carry_v1"]
    sup = applied["ai1_supersede_capability_integrity_v1"]
    assert cap["version"] == CAPABILITY
    assert sup["version"] == SUPERSESSION
    assert cap["status"] == "PRODUCTION_APPLIED"
    assert sup["status"] == "PRODUCTION_APPLIED"
    assert int(cap["version"]) < int(sup["version"])
    assert (ROOT / cap["path"]).exists()
    assert (ROOT / sup["path"]).exists()
    source = (ROOT / sup["path"]).read_text(encoding="utf-8")
    assert "Depends on:" in source
    assert "20260930235959_ai1_capability_carry_v1.sql" in source
    # Fail-closed: these must not simultaneously sit in `pending`. If they ever
    # return to pending, the ordering guard must be reinstated against it.
    pending_names = {row["name"] for row in ledger.get("pending", [])}
    assert "ai1_capability_carry_v1" not in pending_names
    assert "ai1_supersede_capability_integrity_v1" not in pending_names

def test_ai1_pending_ledger_is_sorted_by_migration_version():
    ledger = _ledger()
    versions = [str(row["version"]) for row in ledger.get("pending", [])]
    assert versions == sorted(versions)
