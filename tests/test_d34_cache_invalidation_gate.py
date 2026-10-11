"""Tests for the D34 cache-invalidation claims gate (WIRE lane).

The gate cold-judges registered scenarios against the REAL
drift_canary.d34_cache_invalidation.IntelligenceStore. These tests prove
the gate itself: honest/fraud directions, malformed inputs fail closed,
and sabotage negative controls (a neutered engine can never earn a pass).
"""
import copy
import json
import os
import subprocess
import sys

import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TOOLS = os.path.join(REPO_ROOT, "tools")
GATE = os.path.join(TOOLS, "d34_cache_invalidation_gate.py")
MANIFEST = os.path.join(TOOLS, "d34_cache_invalidation_manifest.json")

sys.path.insert(0, TOOLS)
sys.path.insert(0, REPO_ROOT)

import d34_cache_invalidation_gate as gate  # noqa: E402


def _run_gate(manifest_path):
    return subprocess.run(
        [sys.executable, GATE, manifest_path],
        capture_output=True, text=True, cwd=REPO_ROOT,
    )


def _write_manifest(tmp_path, manifest):
    path = str(tmp_path / "manifest.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh)
    return path


def _shipped_manifest():
    with open(MANIFEST, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _live(manifest, scenario):
    m = copy.deepcopy(manifest)
    m["scenarios"] = [scenario]
    return m


# -- shipped manifest: well-formed and honest (never pinned to DORMANT) --------

def test_shipped_manifest_is_wellformed_and_honest():
    """The owning lane registers real scenarios without editing tests: the
    shipped manifest must be well-formed and judge to the engine's honest
    word (DORMANT/PASS/VIOLATION) — never BROKEN. A test pinning
    scenarios==[] would fail the moment the first real claim lands and
    would make the TEST step, not the gate step, the thing that blocks."""
    manifest = _shipped_manifest()
    assert isinstance(manifest.get("scenarios", []), list)
    d34 = gate._import_mechanism()
    try:
        verdict, _ = gate.judge_manifest(d34, manifest)
    except gate.Violation:
        verdict = "VIOLATION"
    assert verdict in ("DORMANT", "PASS", "VIOLATION"), verdict


def test_shipped_manifest_gate_reports_honest_verdict():
    proc = _run_gate(MANIFEST)
    assert proc.returncode in (0, 1), proc.stdout + proc.stderr
    assert any(w in proc.stdout for w in ("DORMANT", "PASS", "VIOLATION"))
    assert "BROKEN" not in proc.stdout


def test_worked_fraud_example_is_a_real_violation():
    """The manifest's worked fraud, registered live, must exit 1 with the
    engine's own naming — this is what a dishonest claim meets."""
    manifest = _shipped_manifest()
    d34 = gate._import_mechanism()
    failures = gate.judge_scenario(d34, manifest["_example"])
    assert failures, "fraud example judged clean — the gate is blind"
    assert any("asserted=SERVE_CURRENT" in f and "actual=REFUSE_STALE" in f
               for f in failures), failures


def test_worked_honest_example_passes():
    manifest = _shipped_manifest()
    d34 = gate._import_mechanism()
    failures = gate.judge_scenario(d34, manifest["_example_honest"])
    assert failures == [], failures


def test_honest_live_scenario_passes_gate(tmp_path):
    manifest = _shipped_manifest()
    live = _live(manifest, manifest["_example_honest"])
    live["scenarios"][0] = dict(live["scenarios"][0], id="honest-live")
    proc = _run_gate(_write_manifest(tmp_path, live))
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "PASS" in proc.stdout


def test_fraud_live_scenario_blocked(tmp_path):
    manifest = _shipped_manifest()
    live = _live(manifest, manifest["_example"])
    live["scenarios"][0] = dict(live["scenarios"][0], id="fraud-live")
    proc = _run_gate(_write_manifest(tmp_path, live))
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "VIOLATION" in proc.stdout
    assert "asserted=SERVE_CURRENT" in proc.stdout
    assert "actual=REFUSE_STALE" in proc.stdout


# -- sharpest frauds -----------------------------------------------------------

def _fraud_stale_act():
    """ACT authorized on a revoked claim: the TOCTOU close must refuse."""
    return {
        "id": "fraud-stale-act",
        "ops": [
            {"op": "register_source", "source_id": "E1"},
            {"op": "register_claim", "claim_id": "K1",
             "paths": [[["E1"], ["staging", "production"]]]},
            {"op": "commit", "source_id": "E1", "new_status": "REVOKED",
             "reason": "confirmed compromised"},
            {"op": "authorize_act", "claim_dependencies": ["K1"],
             "seen_generation": "current", "assert": "AUTHORIZED"},
        ],
    }


def _fraud_delayed_refresh():
    """A delayed refresh republishing an earlier PASS over a later
    revocation: the generation CAS must refuse."""
    return {
        "id": "fraud-delayed-refresh",
        "ops": [
            {"op": "register_source", "source_id": "E1"},
            {"op": "register_claim", "claim_id": "K1",
             "paths": [[["E1"], ["staging", "production"]]]},
            {"op": "add_projection", "projection_id": "P1",
             "surface": "cached_summary", "claim_dependencies": ["K1"]},
            {"op": "commit", "source_id": "E1", "new_status": "REVOKED",
             "reason": "confirmed compromised"},
            {"op": "refresh", "projection_id": "P1",
             "expected_generation": 0, "assert": "ok"},
        ],
    }


def _fraud_history_rewrite():
    """A projection marked HISTORICAL_ONLY served as current: the
    read-time gate must refuse."""
    return {
        "id": "fraud-history-rewrite",
        "ops": [
            {"op": "register_source", "source_id": "E1"},
            {"op": "register_claim", "claim_id": "K1",
             "paths": [[["E1"], ["staging", "production"]]]},
            {"op": "add_projection", "projection_id": "H1",
             "surface": "historical_receipt", "claim_dependencies": ["K1"]},
            {"op": "serve", "projection_id": "H1",
             "route": "know_retrieval", "assert": "SERVE_CURRENT"},
        ],
    }


@pytest.mark.parametrize("fraud", [
    _fraud_stale_act(), _fraud_delayed_refresh(), _fraud_history_rewrite(),
])
def test_sharpest_frauds_blocked(tmp_path, fraud):
    manifest = _shipped_manifest()
    proc = _run_gate(_write_manifest(tmp_path, _live(manifest, fraud)))
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "VIOLATION" in proc.stdout


# -- fail-closed -----------------------------------------------------------------

def test_missing_manifest_fails_closed(tmp_path):
    proc = _run_gate(str(tmp_path / "nope.json"))
    assert proc.returncode == 2
    assert "BROKEN" in proc.stdout


def test_corrupt_manifest_fails_closed(tmp_path):
    path = str(tmp_path / "manifest.json")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("{not json")
    proc = _run_gate(path)
    assert proc.returncode == 2
    assert "BROKEN" in proc.stdout


def test_unknown_op_fails_closed(tmp_path):
    manifest = _shipped_manifest()
    bad = {"id": "bad-op", "ops": [{"op": "launch_missiles"}]}
    proc = _run_gate(_write_manifest(tmp_path, _live(manifest, bad)))
    assert proc.returncode == 2
    assert "BROKEN" in proc.stdout


def test_missing_mechanism_fails_closed(tmp_path, monkeypatch):
    """If drift_canary.d34_cache_invalidation cannot be imported, the gate
    must fail closed, never silently pass."""
    import builtins
    real_import = builtins.__import__

    def hostile_import(name, *args, **kwargs):
        if name.startswith("drift_canary"):
            raise ImportError("sabotage: mechanism removed")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", hostile_import)
    with pytest.raises(gate.GateBroken):
        gate._import_mechanism()


# -- sabotage negative controls ----------------------------------------------------

def test_neutered_engine_fails_canary_closed():
    """An engine that always serves stale as current must fail the fixed
    canary -> GateBroken (exit 2), never a blind pass."""

    class BlindStore:
        generation = 0

        def register_source(self, *a, **k):
            pass

        def register_claim(self, *a, **k):
            pass

        def add_projection(self, *a, **k):
            pass

        def commit_eligibility_change(self, *a, **k):
            pass

        def serve(self, projection_id, route):
            from types import SimpleNamespace
            return SimpleNamespace(decision="SERVE_CURRENT")

        def refresh_projection(self, *a, **k):
            pass

        def authorize_act(self, *a, **k):
            return "AUTHORIZED"

    class BlindD34:
        IntelligenceStore = BlindStore
        StaleGenerationError = type("StaleGenerationError", (Exception,), {})
        SERVE_CURRENT = "SERVE_CURRENT"
        REFUSE_STALE = "REFUSE_STALE"
        ACT_REFUSED = "REFUSED"
        REVOKED = "REVOKED"
        CACHED_SUMMARY = "cached_summary"
        KNOW_RETRIEVAL = "know_retrieval"

    with pytest.raises(gate.GateBroken):
        gate.run_canaries(BlindD34())


def test_sabotaged_gate_cannot_always_pass(tmp_path):
    """If the gate module were sabotaged to always exit 0, the fraud tests
    above would fail — this test pins the wiring: the fraud scenario must
    produce a non-empty failure list through judge_scenario."""
    manifest = _shipped_manifest()
    d34 = gate._import_mechanism()
    failures = gate.judge_scenario(d34, manifest["_example"])
    assert isinstance(failures, list) and len(failures) > 0
