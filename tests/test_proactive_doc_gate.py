"""Tests for SN-PROACTIVE-DOC's mechanical gate
(tools/protocol/checks/proactive_doc.py).

The gate is the executable check the law was missing: a real CLI enforcing
capture-or-honest-excuse (kernel core), proactive timing, and a named
destination. Red -> green: each capture failure mode is planted and must
FAIL naming the reason; honest cycles must PASS.
"""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CHECK = ROOT / "tools" / "protocol" / "checks" / "proactive_doc.py"
MANIFEST = ROOT / "kernel" / "protocol" / "protocol_manifest.json"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _load_check():
    spec = importlib.util.spec_from_file_location("proactive_doc", str(CHECK))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


proactive_doc = _load_check()


def _record(**over):
    rec = {
        "work_description": "built the SN-NO-EGO gate module",
        "lesson": "Ego markers are checkable: first-person preference phrasing "
                  "in a rationale is a mechanical signal, not a vibe.",
        "provenance": "tests/test_no_ego_gate.py: 4 planted ego phrases all "
                      "tripped the marker scan, 0 false positives on evidence prose",
        "captured_at": "2026-10-11T22:30:00Z",
        "work_completed_at": "2026-10-11T21:30:00Z",
        "destination": "memory/2026-10-11.md",
    }
    rec.update(over)
    return rec


# ---- happy paths ----

def test_pass_full_cycle():
    res = proactive_doc.check(_record())
    assert res["pass"] is True, res["reasons"]
    assert res["details"]["law"] == "SN-PROACTIVE-DOC"
    assert res["details"]["lag_hours"] == 1.0


def test_pass_honest_no_lesson():
    rec = _record(lesson="", no_lesson_reason="pure mechanical regen; no new insight")
    res = proactive_doc.check(rec)
    assert res["pass"] is True, res["reasons"]


def test_pass_late_capture_with_reason():
    rec = _record(captured_at="2026-10-20T21:30:00Z",
                  late_reason="on-call incident; captured at first write window")
    res = proactive_doc.check(rec)
    assert res["pass"] is True, res["reasons"]
    assert res["details"]["lag_hours"] == 216.0


def test_kernel_core_is_delegated():
    res = proactive_doc.check(_record())
    assert res["details"]["kernel_delegated"] is True


# ---- capture failure modes ----

def test_fail_silence_is_not_documentation():
    rec = _record(lesson="", no_lesson_reason="")
    res = proactive_doc.check(rec)
    assert res["pass"] is False
    assert res["reasons"]


def test_fail_lesson_without_provenance():
    rec = _record(provenance="   ")
    res = proactive_doc.check(rec)
    assert res["pass"] is False
    text = " ".join(res["reasons"])
    assert "provenance" in text.lower()


def test_fail_late_capture_without_reason():
    rec = _record(captured_at="2026-10-20T21:30:00Z")
    res = proactive_doc.check(rec)
    assert res["pass"] is False
    assert "not proactive" in " ".join(res["reasons"])


def test_fail_missing_destination():
    rec = _record(destination=" ")
    res = proactive_doc.check(rec)
    assert res["pass"] is False
    assert "destination" in " ".join(res["reasons"]).lower()


def test_fail_unparseable_timestamp():
    rec = _record(captured_at="yesterday afternoon")
    res = proactive_doc.check(rec)
    assert res["pass"] is False
    assert "ISO-8601" in " ".join(res["reasons"])


def test_fail_captured_before_work():
    rec = _record(captured_at="2026-10-11T20:30:00Z")
    res = proactive_doc.check(rec)
    assert res["pass"] is False
    assert "predates" in " ".join(res["reasons"])


def test_fail_undescribed_work():
    rec = _record(work_description="  ")
    res = proactive_doc.check(rec)
    assert res["pass"] is False


def test_fail_nonpositive_lag_budget():
    rec = _record(max_lag_hours=0)
    res = proactive_doc.check(rec)
    assert res["pass"] is False


# ---- manifest binding ----

def test_manifest_registers_proactive_doc_with_real_check():
    manifest = json.loads(MANIFEST.read_text())
    law = next(l for l in manifest["laws"] if l["id"] == "SN-PROACTIVE-DOC")
    assert law["check"] == "tools/protocol/checks/proactive_doc.py"
    assert (ROOT / law["check"]).is_file()


# ---- CLI: fail-closed probe + fixtures ----

def test_cli_garbage_record_exits_nonzero():
    proc = subprocess.run(
        [sys.executable, str(CHECK), "--record", "###not-json###"],
        capture_output=True, text=True, timeout=60)
    assert proc.returncode != 0, "gate must be fail-closed"


def test_cli_pass_fixture_exits_zero():
    proc = subprocess.run(
        [sys.executable, str(CHECK), "--record",
         f"@{FIXTURES/'proactive_doc_pass.json'}", "--json"],
        capture_output=True, text=True, timeout=60)
    assert proc.returncode == 0, proc.stderr
    assert json.loads(proc.stdout)["pass"] is True


def test_cli_fail_fixture_exits_nonzero():
    proc = subprocess.run(
        [sys.executable, str(CHECK), "--record",
         f"@{FIXTURES/'proactive_doc_fail.json'}", "--json"],
        capture_output=True, text=True, timeout=60)
    assert proc.returncode != 0, "the gate must bite on an undocumented lesson"
    assert json.loads(proc.stdout)["pass"] is False
