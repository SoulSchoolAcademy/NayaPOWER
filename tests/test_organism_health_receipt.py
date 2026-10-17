import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "organism_health_receipt", ROOT / "tools" / "organism_health_receipt.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def _tree(tmp_path, ledger, migrations):
    supa = tmp_path / "supabase"
    (supa / "migrations").mkdir(parents=True)
    for name in migrations:
        (supa / "migrations" / name).write_text("-- test\n")
    (supa / "PRODUCTION-MIGRATION-LEDGER-V1.json").write_text(
        json.dumps(ledger), encoding="utf-8")
    return tmp_path


def _ledger(applied, pending=(), claimed=None):
    return {
        "production_applied": [{"version": v} for v in applied],
        "production_applied_count": len(applied) if claimed is None else claimed,
        "pending": [{"version": v, "status": "PENDING_REVIEW_NOT_PRODUCTION_APPLIED"}
                    for v in pending],
        "captured_date": "2026-10-06",
    }


def test_applied_plus_recorded_pending_is_accounted_not_broken(tmp_path):
    tree = _tree(
        tmp_path,
        _ledger(["20260101000000"], pending=["20260102000000"]),
        ["20260101000000_a.sql", "20260102000000_b.sql"],
    )
    a = mod.measure_migrations(tree)
    assert a["status"] == "FLAG"
    assert "BROKEN" not in a["summary"]
    assert "EXACT" in a["summary"]
    ev = a["evidence"]
    assert ev["in_repo_not_in_ledger_at_all"] == []
    assert ev["in_ledger_applied_not_repo"] == []
    assert ev["recorded_pending_not_production_applied"] == ["20260102000000"]
    assert "PENDING_REVIEW_NOT_PRODUCTION_APPLIED" in a["summary"]


def test_unrecorded_repo_file_is_broken(tmp_path):
    tree = _tree(
        tmp_path,
        _ledger(["20260101000000"]),
        ["20260101000000_a.sql", "20260103000000_c.sql"],
    )
    a = mod.measure_migrations(tree)
    assert a["status"] == "FLAG"
    assert "BROKEN" in a["summary"]
    assert a["evidence"]["in_repo_not_in_ledger_at_all"] == ["20260103000000"]


def test_applied_ledger_version_missing_from_repo_is_broken(tmp_path):
    tree = _tree(
        tmp_path,
        _ledger(["20260101000000", "20260102000000"]),
        ["20260101000000_a.sql"],
    )
    a = mod.measure_migrations(tree)
    assert a["status"] == "FLAG"
    assert "BROKEN" in a["summary"]
    assert a["evidence"]["in_ledger_applied_not_repo"] == ["20260102000000"]


def test_recorded_pending_file_missing_from_repo_is_broken(tmp_path):
    tree = _tree(
        tmp_path,
        _ledger(["20260101000000"], pending=["20260102000000"]),
        ["20260101000000_a.sql"],
    )
    a = mod.measure_migrations(tree)
    assert a["status"] == "FLAG"
    assert "BROKEN" in a["summary"]
    assert a["evidence"]["recorded_pending_missing_from_repo"] == ["20260102000000"]


def test_claimed_applied_count_mismatch_is_broken(tmp_path):
    tree = _tree(
        tmp_path,
        _ledger(["20260101000000"], claimed=7),
        ["20260101000000_a.sql"],
    )
    a = mod.measure_migrations(tree)
    assert a["status"] == "FLAG"
    assert "BROKEN" in a["summary"]


def test_exact_parity_still_flags_production_db_unverified(tmp_path):
    tree = _tree(
        tmp_path,
        _ledger(["20260101000000"]),
        ["20260101000000_a.sql"],
    )
    a = mod.measure_migrations(tree)
    assert a["status"] == "FLAG"
    assert "EXACT" in a["summary"]
    assert "UNVERIFIED" in a["summary"]
    assert "BROKEN" not in a["summary"]


def test_real_ledger_at_repo_tip_is_not_reported_broken():
    a = mod.measure_migrations(ROOT)
    assert a["status"] == "FLAG"
    assert "BROKEN" not in a["summary"], a["summary"]
    ev = a["evidence"]
    assert ev["in_repo_not_in_ledger_at_all"] == []
    assert ev["in_ledger_applied_not_repo"] == []
    assert ev["recorded_pending_missing_from_repo"] == []
    assert ev["ledger_recorded_pending"] >= len(
        ev["recorded_pending_not_production_applied"])
    assert ev["repo_files"] == ev["ledger_versions"] + ev["ledger_recorded_pending"]


def test_tool_version_is_bumped_and_schema_stable():
    assert mod.TOOL_VERSION == "1.1.0"
    assert mod.SCHEMA == "naya.organism.health.receipt/v1"
