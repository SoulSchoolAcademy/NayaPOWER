"""Tests for tools/d32_uncertainty_gate.py - the D32 wire gate.

The gate cold-judges registered uncertainty scenarios against the REAL
D32 engine (drift_canary.uncertainty_propagation). These tests prove the
gate itself: DORMANT when there is nothing to judge, PASS on the honest
cases, VIOLATION (fraud named in the engine's own words) on the
modality-upgrade fraud, and fail-closed BROKEN on sabotage - including a
neutered engine that upgrades every derivation to "verified" and a
missing mechanism.
"""
import importlib
import json
import sys
import types
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS = REPO_ROOT / "tools"
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(TOOLS))

import d32_uncertainty_gate as gate

SHIPPED_MANIFEST = TOOLS / "d32_uncertainty_manifest.json"
MECHANISM = "drift_canary.uncertainty_propagation"


def _load_shipped():
    with open(SHIPPED_MANIFEST) as fh:
        return json.load(fh)


def _write_manifest(tmp_path, scenarios):
    p = tmp_path / "manifest.json"
    p.write_text(json.dumps({"scenarios": scenarios}))
    return str(p)


def _honest_live():
    shipped = _load_shipped()["scenarios"]
    return {k.lstrip("_"): v for k, v in shipped.items()
            if k != "_example"}


# ---------------------------------------------------------------------------
# Contract directions
# ---------------------------------------------------------------------------

def test_dormant_on_empty_manifest(tmp_path):
    code, report = gate.run_gate(_write_manifest(tmp_path, {}))
    assert code == 0
    assert report["status"] == "DORMANT"


def test_dormant_on_examples_only__shipped_manifest_is_dormant():
    code, report = gate.run_gate(str(SHIPPED_MANIFEST))
    assert code == 0
    assert report["status"] == "DORMANT"


def test_dormant_on_absent_manifest(tmp_path):
    code, report = gate.run_gate(str(tmp_path / "does-not-exist.json"))
    assert code == 0
    assert report["status"] == "DORMANT"


def test_pass_on_honest_examples(tmp_path):
    code, report = gate.run_gate(
        _write_manifest(tmp_path, _honest_live()))
    assert code == 0, report
    assert report["status"] == "PASS"
    assert len(report["judged"]) == 3


def test_violation_on_modality_upgrade_fraud__fraud_named(tmp_path):
    shipped = _load_shipped()["scenarios"]
    fraud = shipped["_example"]
    code, report = gate.run_gate(
        _write_manifest(tmp_path, {"fraud-claim": fraud}))
    assert code == 1, report
    assert report["status"] == "VIOLATION"
    # The fraud is named in the mechanism's own words.
    assert "asserted modality=verified" in report["detail"]
    assert "recomputed modality=possible" in report["detail"]


def test_violation_on_explosive_reasoning_fraud(tmp_path):
    # Asserting that a conflict on P SUPPORTs unrelated Q is the exact
    # fraud the nonexplosion law refuses.
    fraud = {"type": "nonexplosion", "conflict_on_p": True,
             "unrelated_q": "Q", "asserted_q_standing": "SUPPORTED"}
    code, report = gate.run_gate(
        _write_manifest(tmp_path, {"explosive-fraud": fraud}))
    assert code == 1, report
    assert report["status"] == "VIOLATION"
    assert "UNDETERMINED" in report["detail"]


def test_violation_on_gap_overreach_fraud(tmp_path):
    # Asserting that a telemetry gap invalidates a claim that does not
    # depend on the missing events is the overreach the scoping law
    # refuses.
    shipped = _load_shipped()["scenarios"]
    honest = json.loads(json.dumps(shipped["_example_observation"]))
    honest["asserted"]["C-independent"] = "UNDETERMINED"
    code, report = gate.run_gate(
        _write_manifest(tmp_path, {"gap-fraud": honest}))
    assert code == 1, report
    assert report["status"] == "VIOLATION"
    assert "C-independent" in report["detail"]


def test_unknown_derivation_treated_as_copy__preserves_modality(tmp_path):
    scenario = {"type": "modality_derivation",
                "source_modality": "conditional",
                "derivation": "unknown_future_verb",
                "asserted_modality": "conditional"}
    code, report = gate.run_gate(
        _write_manifest(tmp_path, {"unknown-verb": scenario}))
    assert code == 0, report
    assert report["status"] == "PASS"


# ---------------------------------------------------------------------------
# Fail-closed: malformed input
# ---------------------------------------------------------------------------

def test_broken_on_unknown_modality(tmp_path):
    bad = {"type": "modality_derivation", "source_modality": "certain",
           "derivation": "copy", "asserted_modality": "possible"}
    code, report = gate.run_gate(
        _write_manifest(tmp_path, {"bad": bad}))
    assert code == 2, report
    assert report["status"] == "BROKEN"
    assert "unknown modality" in report["reason"]


def test_broken_on_unknown_scenario_type(tmp_path):
    bad = {"type": "prophecy", "source_modality": "possible",
           "derivation": "copy", "asserted_modality": "possible"}
    code, report = gate.run_gate(
        _write_manifest(tmp_path, {"bad": bad}))
    assert code == 2, report
    assert "unknown type" in report["reason"]


def test_broken_on_corrupt_manifest(tmp_path):
    p = tmp_path / "manifest.json"
    p.write_text("{not json")
    code, report = gate.run_gate(str(p))
    assert code == 2, report
    assert report["status"] == "BROKEN"


def test_broken_on_invented_kind_in_observation_gap(tmp_path):
    shipped = _load_shipped()["scenarios"]
    honest = json.loads(json.dumps(shipped["_example_observation"]))
    honest["gap"]["state"] = "haunted"
    code, report = gate.run_gate(
        _write_manifest(tmp_path, {"bad-gap": honest}))
    assert code == 2, report
    assert "unknown coverage state" in report["reason"]


# ---------------------------------------------------------------------------
# Fail-closed: sabotage of the mechanism
# ---------------------------------------------------------------------------

def _blind_engine():
    """A neutered engine: upgrades every derivation to 'verified'."""
    real = importlib.import_module(MECHANISM)
    fake = types.ModuleType(MECHANISM)
    for name in dir(real):
        if not name.startswith("__"):
            setattr(fake, name, getattr(real, name))

    def blind_derive(source_modality, derivation):
        return ("verified", "blind-engine-upgrades-everything")

    fake.derive_modality = blind_derive
    return fake


def test_broken_on_blind_engine__canary_fails_closed(tmp_path, monkeypatch):
    monkeypatch.setitem(sys.modules, MECHANISM, _blind_engine())
    code, report = gate.run_gate(
        _write_manifest(tmp_path, _honest_live()))
    assert code == 2, report
    assert report["status"] == "BROKEN"
    assert "canary FAILED" in report["reason"]


def test_broken_on_missing_mechanism_with_live_scenarios(
        tmp_path, monkeypatch):
    def gone():
        raise gate.MechanismMissing("mechanism deleted")
    monkeypatch.setattr(gate, "_load_mechanism", gone)
    code, report = gate.run_gate(
        _write_manifest(tmp_path, _honest_live()))
    assert code == 2, report
    assert report["status"] == "BROKEN"


def test_dormant_stays_green_when_mechanism_missing_and_nothing_to_judge(
        tmp_path, monkeypatch):
    def gone():
        raise gate.MechanismMissing("mechanism deleted")
    monkeypatch.setattr(gate, "_load_mechanism", gone)
    code, report = gate.run_gate(_write_manifest(tmp_path, {}))
    assert code == 0, report
    assert report["status"] == "DORMANT"


def test_gate_never_raises_on_hostile_input(tmp_path):
    # Non-object scenarios, wrong types everywhere: the gate must
    # fail closed with exit 2, never raise.
    hostile = {"scenarios": {"h1": [1, 2], "h2": None, "h3": 42}}
    code, report = gate.run_gate(
        _write_manifest(tmp_path, hostile["scenarios"]))
    assert code == 2, report
    assert report["status"] == "BROKEN"
