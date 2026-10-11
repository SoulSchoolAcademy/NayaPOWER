"""Naya Code alias manifest conformance: positive and adversarial negative cases."""
import json
import shutil
from pathlib import Path

from tools.verify_naya_code_manifest import REL, validate

ROOT = Path(__file__).resolve().parent.parent


def fixture(tmp_path):
    data = json.loads((ROOT / REL).read_text(encoding="utf-8"))
    needed = [data["human_form"], data["ai_form"], *data["canonical_sources"].values()]
    for name in needed:
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
    dest = tmp_path / REL
    dest.parent.mkdir(parents=True, exist_ok=True)
    return data, dest


def test_real_repo_contract_references_resolve():
    assert validate(ROOT) == []


def test_missing_law_source_rejected(tmp_path):
    data, dest = fixture(tmp_path)
    dest.write_text(json.dumps(data), encoding="utf-8")
    (tmp_path / data["canonical_sources"]["law_of_one"]).unlink()
    assert "missing canonical source: law_of_one" in validate(tmp_path)


def test_false_production_claim_rejected(tmp_path):
    data, dest = fixture(tmp_path)
    data["status"] = "PRODUCTION_PROVEN"
    dest.write_text(json.dumps(data), encoding="utf-8")
    assert "unsupported enforcement claim" in validate(tmp_path)


def test_missing_critical_principle_rejected(tmp_path):
    data, dest = fixture(tmp_path)
    data["doctrine"] = data["doctrine"][:-1]
    dest.write_text(json.dumps(data), encoding="utf-8")
    assert "expected twelve distinct principles" in validate(tmp_path)


def test_stale_archived_board_rejected(tmp_path):
    data, dest = fixture(tmp_path)
    data["routing"]["current_board"] = data["routing"]["archive_only"]
    dest.write_text(json.dumps(data), encoding="utf-8")
    assert "stale coordination board" in validate(tmp_path)


def test_missing_ai_form_rejected(tmp_path):
    data, dest = fixture(tmp_path)
    dest.write_text(json.dumps(data), encoding="utf-8")
    (tmp_path / data["ai_form"]).unlink()
    assert "missing or incorrect ai_form" in validate(tmp_path)
