"""Tests for tools/check_law_of_one.py — positive + negative controls."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from check_law_of_one import (  # noqa: E402
    EXIT_ERROR,
    EXIT_PASS,
    EXIT_UNOWNED,
    check,
)

RULES = [
    "collective_scoring",
    "best_effort_floor",
    "authenticity",
    "respect_triad",
    "intelligence_test",
]


def make_law(path, ratified=True, status="RATIFIED", rules=RULES):
    law = {
        "law_id": "LAW-OF-ONE-V1",
        "ratified": ratified,
        "status": status,
        "operational_rules": [{"rule": r, "description": f"{r} rule"} for r in rules],
    }
    path.write_text(json.dumps(law))
    return path


def make_registry(path, owners):
    reg = {
        "law": "BRAIN/01-GOVERNANCE/0007-law-of-one-v1.machine.json",
        "law_id": "LAW-OF-ONE-V1",
        "updated": "2026-10-10",
        "rules": {r: {"owner": owners.get(r), "note": "t"} for r in RULES},
    }
    path.write_text(json.dumps(reg))
    return path


def test_all_owned_pass(tmp_path):
    tool = tmp_path / "tools" / "t.py"
    tool.parent.mkdir()
    tool.write_text("# owner")
    law = make_law(tmp_path / "law.json")
    reg = make_registry(tmp_path / "reg.json", {r: "tools/t.py" for r in RULES})
    assert check(str(law), str(reg), tmp_path) == EXIT_PASS


def test_all_owned_dict_form_pass(tmp_path):
    tool = tmp_path / "w.yml"
    tool.write_text("# owner")
    law = make_law(tmp_path / "law.json")
    reg = make_registry(
        tmp_path / "reg.json",
        {r: {"path": "w.yml", "note": "t"} for r in RULES},
    )
    assert check(str(law), str(reg), tmp_path) == EXIT_PASS


def test_one_unowned_fails_naming_rule(tmp_path, capsys):
    law = make_law(tmp_path / "law.json")
    owners = {r: "x" for r in RULES}
    owners["authenticity"] = None
    reg = make_registry(tmp_path / "reg.json", owners)
    # 'x' does not exist -> stale too; make others exist to isolate
    for r in RULES:
        if r != "authenticity":
            (tmp_path / "x").write_text("x")
    assert check(str(law), str(reg), tmp_path) == EXIT_UNOWNED
    out = capsys.readouterr().out
    assert "RULE authenticity UNOWNED" in out


def test_stale_owner_path_fails(tmp_path, capsys):
    law = make_law(tmp_path / "law.json")
    reg = make_registry(tmp_path / "reg.json", {r: "tools/gone.py" for r in RULES})
    assert check(str(law), str(reg), tmp_path) == EXIT_UNOWNED
    assert "STALE" in capsys.readouterr().out


def test_missing_registry_is_error(tmp_path):
    law = make_law(tmp_path / "law.json")
    assert check(str(law), str(tmp_path / "nope.json"), tmp_path) == EXIT_ERROR


def test_unparseable_registry_is_error(tmp_path):
    law = make_law(tmp_path / "law.json")
    reg = tmp_path / "reg.json"
    reg.write_text("{not json")
    assert check(str(law), str(reg), tmp_path) == EXIT_ERROR


def test_missing_law_is_error(tmp_path):
    reg = make_registry(tmp_path / "reg.json", {})
    assert check(str(tmp_path / "nolaw.json"), str(reg), tmp_path) == EXIT_ERROR


def test_unratified_law_is_error(tmp_path):
    law = make_law(tmp_path / "law.json", ratified=False)
    reg = make_registry(tmp_path / "reg.json", {r: "x" for r in RULES})
    assert check(str(law), str(reg), tmp_path) == EXIT_ERROR


def test_law_without_rules_is_error(tmp_path):
    law = make_law(tmp_path / "law.json", rules=[])
    reg = make_registry(tmp_path / "reg.json", {})
    assert check(str(law), str(reg), tmp_path) == EXIT_ERROR


def test_registry_extra_rule_is_error(tmp_path):
    law = make_law(tmp_path / "law.json")
    reg = tmp_path / "reg.json"
    data = json.loads(make_registry(reg, {}).read_text())
    data["rules"]["invented_rule"] = {"owner": None, "note": "t"}
    reg.write_text(json.dumps(data))
    assert check(str(law), str(reg), tmp_path) == EXIT_ERROR


def test_registry_missing_rule_is_error(tmp_path):
    law = make_law(tmp_path / "law.json")
    reg = tmp_path / "reg.json"
    data = json.loads(make_registry(reg, {}).read_text())
    del data["rules"]["authenticity"]
    reg.write_text(json.dumps(data))
    assert check(str(law), str(reg), tmp_path) == EXIT_ERROR


def test_law_id_mismatch_is_error(tmp_path):
    law = make_law(tmp_path / "law.json")
    reg = tmp_path / "reg.json"
    data = json.loads(make_registry(reg, {}).read_text())
    data["law_id"] = "SOMETHING-ELSE"
    reg.write_text(json.dumps(data))
    assert check(str(law), str(reg), tmp_path) == EXIT_ERROR
