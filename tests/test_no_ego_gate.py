"""Tests for SN-NO-EGO's mechanical gate (tools/protocol/checks/no_ego.py).

The gate enforces the ego half of decision governance: the decider's want
is not a basis. Red -> green: each ego failure mode is planted and must
FAIL naming the reason; honest records must PASS.
"""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CHECK = ROOT / "tools" / "protocol" / "checks" / "no_ego.py"
MANIFEST = ROOT / "kernel" / "protocol" / "protocol_manifest.json"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _load_check():
    spec = importlib.util.spec_from_file_location("no_ego", str(CHECK))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


no_ego = _load_check()


def _record(**over):
    rec = {
        "decision": "which cache backend to use",
        "decider": "naya5-lane-beta",
        "rationale": "Option B scored 8.1 vs 7.4 on the 7-dimension scorecard; "
                     "the evidence favors B on effect_size.",
        "math_winner": "opt-b",
        "chosen": "opt-b",
    }
    rec.update(over)
    return rec


# ---- happy paths ----

def test_pass_when_math_is_followed():
    res = no_ego.check(_record())
    assert res["pass"] is True, res["reasons"]
    assert res["details"]["law"] == "SN-NO-EGO"


def test_pass_override_with_evidence():
    res = no_ego.check(_record(
        chosen="opt-a",
        override_evidence="New load test (evidence/2026-10-11-load.json) shows "
                          "opt-b degrades past 10k rps; opt-a holds.",
    ))
    assert res["pass"] is True, res["reasons"]


def test_pass_no_math_with_honest_reason():
    rec = _record(math_winner=None, chosen="opt-a",
                  no_math_reason="Trivial, fully reversible config default; "
                                 "scoring would cost more than the decision.")
    res = no_ego.check(rec)
    assert res["pass"] is True, res["reasons"]


# ---- ego failure modes ----

def test_fail_ego_marker_in_rationale():
    res = no_ego.check(_record(
        rationale="I prefer option B, it's my call — trust me on this one."))
    assert res["pass"] is False
    text = " ".join(res["reasons"])
    assert "i prefer" in text and "trust me" in text, text


def test_fail_override_without_evidence_names_ego_override():
    res = no_ego.check(_record(chosen="opt-a"))
    assert res["pass"] is False
    assert "ego override" in " ".join(res["reasons"])


def test_fail_override_evidence_with_ego_markers():
    res = no_ego.check(_record(
        chosen="opt-a",
        override_evidence="I just feel like opt-a is right, my gut says so."))
    assert res["pass"] is False
    assert "my gut" in " ".join(res["reasons"])


def test_fail_no_math_and_no_reason():
    rec = _record(math_winner=None, chosen="opt-a")
    res = no_ego.check(rec)
    assert res["pass"] is False
    assert "vibes" in " ".join(res["reasons"])


def test_fail_anonymous_decider():
    rec = _record()
    rec["decider"] = "  "
    res = no_ego.check(rec)
    assert res["pass"] is False
    assert "anonymous decisions are void" in " ".join(res["reasons"])


def test_fail_malformed_record_names_reason():
    res = no_ego.check({"decision": "x"})
    assert res["pass"] is False
    assert res["reasons"], "fail-closed must name a reason"


# ---- ego-marker unit behavior ----

def test_find_ego_markers_word_boundaries():
    # "trust measurement" must not trip on "trust me"; honest hedging passes.
    assert no_ego.find_ego_markers("we ran the trust measurement twice") == []
    assert no_ego.find_ego_markers("in my opinion the data is thin") == []
    assert "trust me" in no_ego.find_ego_markers("Trust me, ship it")


# ---- manifest binding ----

def test_manifest_registers_no_ego_with_real_check():
    manifest = json.loads(MANIFEST.read_text())
    law = next(l for l in manifest["laws"] if l["id"] == "SN-NO-EGO")
    assert law["check"] == "tools/protocol/checks/no_ego.py"
    assert (ROOT / law["check"]).is_file()
    # The old misbinding (SN-0523's scorecard module) must be gone.
    assert law.get("machine_check") != "kernel/protocol/checks/scorecard.py"


# ---- CLI: fail-closed probe + fixtures ----

def test_cli_garbage_record_exits_nonzero():
    proc = subprocess.run(
        [sys.executable, str(CHECK), "--record", "###not-json###"],
        capture_output=True, text=True, timeout=60)
    assert proc.returncode != 0, "gate must be fail-closed"


def test_cli_pass_fixture_exits_zero():
    proc = subprocess.run(
        [sys.executable, str(CHECK), "--record", f"@{FIXTURES/'no_ego_pass.json'}",
         "--json"],
        capture_output=True, text=True, timeout=60)
    assert proc.returncode == 0, proc.stderr
    assert json.loads(proc.stdout)["pass"] is True


def test_cli_fail_fixture_exits_nonzero():
    proc = subprocess.run(
        [sys.executable, str(CHECK), "--record", f"@{FIXTURES/'no_ego_fail.json'}",
         "--json"],
        capture_output=True, text=True, timeout=60)
    assert proc.returncode != 0, "the gate must bite on an ego override"
    assert json.loads(proc.stdout)["pass"] is False
