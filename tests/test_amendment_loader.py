"""Amendment-loader conformance suite (Workstream 3, Operating Code V2 Amendment Path).

The loader (tools/amendment_loader.py) validates amendment records against V2's
Amendment Path: required fields, structural validity, and Shawn's authorization
marker. It is a validator only - it never amends anything and never flips
ratification status.

Conventions: the loader is loaded standalone via importlib (no repo imports),
tests run against plain dicts. Every refusal reason in the loader has at
least one negative control here. All CLI checks run in-process through
loader.main() except the malformed-JSON case, which also exercises the real
CLI path via subprocess to prove no raw traceback escapes.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools" / "amendment_loader.py"

spec = importlib.util.spec_from_file_location("amendment_loader", TOOLS)
loader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(loader)


def make_record(**overrides):
    record = {
        "what_changed": "Restore the loader enforcement sentence in V2's Amendment Path",
        "provision": "0008-OPERATING-CODE-V2.ai.md - AMENDMENT PATH",
        "proposed_text": "The loader refuses invalid amendment records.",
        "score": 9.5,
        "scorecard_receipt_ref": "#1354 comment 6098808557",
        "proposer": "Naya 4 lane worker",
        "authorization": {
            "authority": "Shawn",
            "authorization_ref": "Shawn's directive: Operation Flow Like Water, NayaPOWER #1354 comment 6098784368",
        },
    }
    record.update(overrides)
    return record


# --- acceptance ---

def test_valid_record_accepted():
    verdict = loader.validate(make_record())
    assert verdict.accepted is True
    assert verdict.reason is None


def test_score_boundaries_accepted():
    assert loader.validate(make_record(score=0)).accepted is True
    assert loader.validate(make_record(score=10)).accepted is True
    assert loader.validate(make_record(score=10.0)).accepted is True


def test_extra_fields_allowed_and_ignored():
    verdict = loader.validate(make_record(schema_version="1.0", notes="future field"))
    assert verdict.accepted is True


def test_authorization_with_optional_date_still_accepted():
    auth = dict(make_record()["authorization"], authorization_date="2026-10-10")
    assert loader.validate(make_record(authorization=auth)).accepted is True


# --- missing fields ---

@pytest.mark.parametrize(
    "field",
    ["what_changed", "provision", "proposed_text", "score",
     "scorecard_receipt_ref", "proposer"],
)
def test_missing_field_refused(field):
    record = make_record()
    del record[field]
    verdict = loader.validate(record)
    assert verdict.accepted is False
    assert verdict.reason == f"MISSING_FIELD:{field}"


def test_missing_authorization_refused():
    record = make_record()
    del record["authorization"]
    verdict = loader.validate(record)
    assert verdict.accepted is False
    assert verdict.reason == "MISSING_AUTHORIZATION"


# --- structure ---

@pytest.mark.parametrize("bad", [[], "a string", 42, None, True])
def test_top_level_not_object_refused(bad):
    verdict = loader.validate(bad)
    assert verdict.accepted is False
    assert verdict.reason == "NOT_AN_OBJECT"


@pytest.mark.parametrize("field", ["what_changed", "provision", "proposed_text",
                                   "scorecard_receipt_ref", "proposer"])
def test_bad_type_refused(field):
    verdict = loader.validate(make_record(**{field: 123}))
    assert verdict.accepted is False
    assert verdict.reason == f"BAD_TYPE:{field}"


def test_score_bool_is_not_a_number():
    # bool subclasses int in Python; True/False are not scores.
    for bad in (True, False, "9.5", None, [9]):
        verdict = loader.validate(make_record(score=bad))
        assert verdict.accepted is False
        assert verdict.reason == "BAD_TYPE:score"


@pytest.mark.parametrize("field", ["what_changed", "provision", "proposed_text",
                                   "scorecard_receipt_ref", "proposer"])
def test_empty_field_refused(field):
    for blank in ("", "   ", "\t\n"):
        verdict = loader.validate(make_record(**{field: blank}))
        assert verdict.accepted is False
        assert verdict.reason == f"EMPTY_FIELD:{field}"


def test_score_out_of_range_refused():
    for bad in (-0.5, -10, 10.0001, 11, 100):
        verdict = loader.validate(make_record(score=bad))
        assert verdict.accepted is False
        assert verdict.reason == "SCORE_OUT_OF_RANGE"


# --- authorization ---

def test_authorization_not_object_refused():
    verdict = loader.validate(make_record(authorization="Shawn said yes"))
    assert verdict.accepted is False
    assert verdict.reason == "BAD_TYPE:authorization"


@pytest.mark.parametrize("bad_authority", ["Naya 4", "the team", "", "   ", None, 42])
def test_wrong_authority_refused(bad_authority):
    auth = {"authority": bad_authority, "authorization_ref": "some comment"}
    verdict = loader.validate(make_record(authorization=auth))
    assert verdict.accepted is False
    assert verdict.reason == "BAD_AUTHORITY"


def test_authorization_without_receipt_refused():
    auth = {"authority": "Shawn"}
    verdict = loader.validate(make_record(authorization=auth))
    assert verdict.accepted is False
    assert verdict.reason == "BAD_AUTHORIZATION_REF"


@pytest.mark.parametrize("bad_ref", ["", "   ", None, 123])
def test_authorization_with_empty_receipt_refused(bad_ref):
    auth = {"authority": "Shawn", "authorization_ref": bad_ref}
    verdict = loader.validate(make_record(authorization=auth))
    assert verdict.accepted is False
    assert verdict.reason == "BAD_AUTHORIZATION_REF"


# --- CLI surface ---

def test_cli_accept_exit_0(tmp_path):
    path = tmp_path / "good.json"
    path.write_text(json.dumps(make_record()), encoding="utf-8")
    assert loader.main([str(path)]) == 0


def test_cli_refuse_exit_1(tmp_path, capsys):
    path = tmp_path / "bad.json"
    bad = make_record()
    del bad["authorization"]
    path.write_text(json.dumps(bad), encoding="utf-8")
    assert loader.main([str(path)]) == 1
    out = capsys.readouterr().out
    assert "REFUSE [MISSING_AUTHORIZATION]" in out


def test_cli_malformed_json_exit_2(tmp_path, capsys):
    path = tmp_path / "broken.json"
    path.write_text('{"what_changed": oops', encoding="utf-8")
    assert loader.main([str(path)]) == 2
    out = capsys.readouterr().out
    assert "REFUSE [MALFORMED_JSON]" in out


def test_cli_json_flag_emits_machine_verdict(tmp_path, capsys):
    path = tmp_path / "good.json"
    path.write_text(json.dumps(make_record()), encoding="utf-8")
    assert loader.main(["--json", str(path)]) == 0
    verdict = json.loads(capsys.readouterr().out)
    assert verdict["accepted"] is True


def test_malformed_json_via_real_subprocess_no_traceback(tmp_path):
    """The worst input through the real CLI path must never dump a traceback."""
    path = tmp_path / "broken.json"
    path.write_text("not json at all {{{", encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, str(TOOLS), str(path)],
        capture_output=True, text=True, check=False,
    )
    assert proc.returncode == 2
    assert "Traceback" not in proc.stderr
    assert "MALFORMED_JSON" in proc.stdout


def test_never_raises_on_any_content():
    """validate() is total: garbage in yields a verdict, never an exception."""
    garbage = [{}, {"authorization": None}, [], "x", 0, 1.5, True, None,
               {"score": float("nan")}]
    for g in garbage:
        verdict = loader.validate(g)
        assert verdict.accepted is False
        assert isinstance(verdict.reason, str) and verdict.reason
