"""Tests for tools/d33_revocation_gate.py — the D33 wire gate.

The gate cold-judges registered revocation scenarios against the REAL
D33 RevocationEngine. These tests prove the gate itself: DORMANT when
there is nothing to judge, PASS on the honest case, VIOLATION (fraud
named) on the masquerade, and fail-closed BROKEN on sabotage —
including a neutered engine that cannot tell the masquerade from
independence.
"""
import json
import subprocess
import sys
import types
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS = REPO_ROOT / "tools"
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(TOOLS))

import d33_revocation_gate as gate
from drift_canary import d33_revocation as d33

SHIPPED_MANIFEST = TOOLS / "d33_revocation_manifest.json"


def _load_shipped():
    with open(SHIPPED_MANIFEST) as fh:
        return json.load(fh)


def _write_manifest(tmp_path, scenarios):
    p = tmp_path / "manifest.json"
    p.write_text(json.dumps({"scenarios": scenarios}))
    return str(p)


def _live_examples():
    shipped = _load_shipped()
    return {k: v for k, v in shipped["scenarios"].items()
            if not k.startswith("_")}, shipped["scenarios"]


# ---------------------------------------------------------------------------
# Contract directions
# ---------------------------------------------------------------------------

def test_dormant_on_empty_manifest(tmp_path):
    code, report = gate.judge_manifest(
        _write_manifest(tmp_path, {}))
    assert code == 0
    assert report["status"] == "DORMANT"


def test_dormant_on_examples_only__shipped_manifest_is_dormant():
    code, report = gate.judge_manifest(str(SHIPPED_MANIFEST))
    assert code == 0
    assert report["status"] == "DORMANT"


def test_dormant_on_absent_manifest(tmp_path):
    code, report = gate.judge_manifest(
        str(tmp_path / "does-not-exist.json"))
    assert code == 0
    assert report["status"] == "DORMANT"


def test_pass_on_honest_example(tmp_path):
    shipped = _load_shipped()
    honest = shipped["scenarios"]["_example_honest"]
    code, report = gate.judge_manifest(
        _write_manifest(tmp_path, {"honest-claim": honest}))
    assert code == 0, report
    assert report["status"] == "PASS"


def test_violation_on_masquerade_fraud__fraud_named(tmp_path):
    shipped = _load_shipped()
    fraud = shipped["scenarios"]["_example"]
    code, report = gate.judge_manifest(
        _write_manifest(tmp_path, {"fraud-claim": fraud}))
    assert code == 1, report
    assert report["status"] == "VIOLATION"
    # The fraud is named in the mechanism's own words.
    assert "asserted=REQUALIFIED" in report["reason"]
    assert "actual=DOWNGRADED" in report["reason"]


def test_violation_names_covered_scope_divergence(tmp_path):
    shipped = _load_shipped()
    fraud = json.loads(json.dumps(shipped["scenarios"]["_example_honest"]))
    # Honest engine verdict is REQUALIFIED over the full scope; assert a
    # narrowed scope and the gate must still block — scope is part of
    # the verdict.
    fraud["asserted"]["C"]["covered_scope"] = ["staging"]
    code, report = gate.judge_manifest(
        _write_manifest(tmp_path, {"scope-fraud": fraud}))
    assert code == 1, report
    assert report["status"] == "VIOLATION"


# ---------------------------------------------------------------------------
# Fail-closed: malformed manifests never get a default
# ---------------------------------------------------------------------------

def test_broken_on_unknown_verdict(tmp_path):
    shipped = _load_shipped()
    bad = json.loads(json.dumps(shipped["scenarios"]["_example_honest"]))
    bad["asserted"]["C"]["verdict"] = "MOSTLY_FINE"
    code, report = gate.judge_manifest(
        _write_manifest(tmp_path, {"bad": bad}))
    assert code == 2, report
    assert report["status"] == "BROKEN"


def test_broken_on_unknown_assessment(tmp_path):
    shipped = _load_shipped()
    bad = json.loads(json.dumps(shipped["scenarios"]["_example_honest"]))
    bad["revocation"]["assessment"] = "unassessed"
    code, report = gate.judge_manifest(
        _write_manifest(tmp_path, {"bad": bad}))
    assert code == 2, report
    assert report["status"] == "BROKEN"


def test_broken_on_unregistered_claim_reference(tmp_path):
    shipped = _load_shipped()
    bad = json.loads(json.dumps(shipped["scenarios"]["_example_honest"]))
    bad["asserted"]["GHOST"] = {"verdict": "REVOKED",
                                "covered_scope": ["staging"]}
    code, report = gate.judge_manifest(
        _write_manifest(tmp_path, {"bad": bad}))
    assert code == 2, report
    assert report["status"] == "BROKEN"


def test_broken_on_corrupt_manifest(tmp_path):
    p = tmp_path / "manifest.json"
    p.write_text("{not json")
    code, report = gate.judge_manifest(str(p))
    assert code == 2
    assert report["status"] == "BROKEN"


# ---------------------------------------------------------------------------
# Sabotage negative controls: the gate must not certify through a
# blind or missing engine.
# ---------------------------------------------------------------------------

class _FakeRecord:
    def __init__(self, verdict, scope):
        self.verdict = verdict
        self.covered_scope = frozenset(scope)
        self.reason = "fake: everything is fine"


class _BlindEngine:
    """Sabotage: an engine that cannot distinguish the masquerade —
    it certifies everything REQUALIFIED no matter what."""

    def __init__(self):
        self._claims = {}

    def register_source(self, source):
        pass

    def add_derivation(self, derived_id, origin_id):
        pass

    def register_claim(self, claim):
        self._claims[claim.claim_id] = claim

    def revoke(self, source_id, reason, assessment=None):
        pass

    def qualification(self, claim_id):
        return _FakeRecord("REQUALIFIED", {"staging", "production"})


def _install_fake_module(monkeypatch):
    fake = types.ModuleType("drift_canary.d33_revocation")
    fake.STAGING = "staging"
    fake.PRODUCTION = "production"
    fake.CONFIRMED_COMPROMISED = "confirmed_compromised"
    fake.POSSIBLY_COMPROMISED = "possibly_compromised"
    fake.DOWNGRADED = "DOWNGRADED"
    fake.UNAFFECTED = "UNAFFECTED"
    fake.REQUALIFIED = "REQUALIFIED"
    fake.EvidenceSource = lambda **kw: types.SimpleNamespace(**kw)
    fake.SupportPath = lambda **kw: types.SimpleNamespace(**kw)
    fake.Claim = lambda **kw: types.SimpleNamespace(**kw)
    fake.RevocationEngine = _BlindEngine
    monkeypatch.setitem(sys.modules, gate.MECHANISM_MODULE, fake)


def test_sabotage_blind_engine_fails_canary__exit_2(tmp_path, monkeypatch):
    _install_fake_module(monkeypatch)
    shipped = _load_shipped()
    honest = shipped["scenarios"]["_example_honest"]
    code, report = gate.judge_manifest(
        _write_manifest(tmp_path, {"honest-claim": honest}))
    assert code == 2, report
    assert report["status"] == "BROKEN"
    assert "canary" in report["reason"]


def test_sabotage_missing_mechanism__exit_2(tmp_path, monkeypatch):
    # A None entry in sys.modules makes importlib.import_module raise
    # ImportError("import of ... halted; None in sys.modules").
    monkeypatch.setitem(sys.modules, gate.MECHANISM_MODULE, None)
    shipped = _load_shipped()
    honest = shipped["scenarios"]["_example_honest"]
    code, report = gate.judge_manifest(
        _write_manifest(tmp_path, {"honest-claim": honest}))
    assert code == 2, report
    assert report["status"] == "BROKEN"


# ---------------------------------------------------------------------------
# CLI contract
# ---------------------------------------------------------------------------

def test_cli_json_exits_0_dormant_on_shipped_manifest():
    proc = subprocess.run(
        [sys.executable, str(TOOLS / "d33_revocation_gate.py"),
         "--manifest", str(SHIPPED_MANIFEST), "--json"],
        capture_output=True, text=True, cwd=str(REPO_ROOT))
    assert proc.returncode == 0, proc.stderr
    report = json.loads(proc.stdout)
    assert report["status"] == "DORMANT"


def test_cli_violation_exit_1_on_fraud(tmp_path):
    shipped = _load_shipped()
    fraud = shipped["scenarios"]["_example"]
    manifest = _write_manifest(tmp_path, {"fraud-claim": fraud})
    proc = subprocess.run(
        [sys.executable, str(TOOLS / "d33_revocation_gate.py"),
         "--manifest", manifest],
        capture_output=True, text=True, cwd=str(REPO_ROOT))
    assert proc.returncode == 1, proc.stderr + proc.stdout
    assert "D33-GATE VIOLATION" in proc.stdout
