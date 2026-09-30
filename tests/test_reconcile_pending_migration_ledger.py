from pathlib import Path
import importlib.util, json

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("reconcile_pending", ROOT / "tools" / "reconcile_pending_migration_ledger.py")
mod = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(mod)

def test_metadata_matches_real_bytes_and_parser(tmp_path):
    p = tmp_path / "x.sql"; p.write_text("select 1;\nselect 2;\n", encoding="utf-8")
    m = mod.metadata(p)
    assert m["bytes"] == len(p.read_bytes())
    assert m["statement_count"] == 2
    assert len(m["sha256"]) == 64

def test_default_mode_is_read_only(monkeypatch, tmp_path):
    migration = tmp_path / "m.sql"; migration.write_text("select 1;\n", encoding="utf-8")
    ledger = tmp_path / "ledger.json"
    ledger.write_text(json.dumps({"pending":[{"version":"1","path":"m.sql","sha256":"bad","bytes":0,"statement_count":0}]}), encoding="utf-8")
    monkeypatch.setattr(mod, "ROOT", tmp_path); monkeypatch.setattr(mod, "LEDGER", ledger)
    before = ledger.read_bytes()
    assert mod.reconcile(False) == 1
    assert ledger.read_bytes() == before

def test_write_changes_metadata_not_status(monkeypatch, tmp_path):
    migration = tmp_path / "m.sql"; migration.write_text("select 1;\n", encoding="utf-8")
    ledger = tmp_path / "ledger.json"
    ledger.write_text(json.dumps({"pending":[{"version":"1","path":"m.sql","sha256":"bad","bytes":0,"statement_count":0,"status":"PENDING_REVIEW_NOT_PRODUCTION_APPLIED"}]}), encoding="utf-8")
    monkeypatch.setattr(mod, "ROOT", tmp_path); monkeypatch.setattr(mod, "LEDGER", ledger)
    assert mod.reconcile(True) == 0
    out=json.loads(ledger.read_text())
    assert out["pending"][0]["status"] == "PENDING_REVIEW_NOT_PRODUCTION_APPLIED"
    assert out["pending"][0]["statement_count"] == 1

def test_missing_file_never_rewritten(monkeypatch, tmp_path):
    ledger=tmp_path/"ledger.json"
    ledger.write_text(json.dumps({"pending":[{"version":"1","path":"missing.sql","sha256":"x","bytes":1,"statement_count":1}]}), encoding="utf-8")
    monkeypatch.setattr(mod,"ROOT",tmp_path); monkeypatch.setattr(mod,"LEDGER",ledger)
    before=ledger.read_bytes()
    assert mod.reconcile(True) == 2
    assert ledger.read_bytes() == before
