"""Gate unit tests for the D31 incident-representation claims gate.

Tests run the gate as a subprocess against the live tree (the checkout's
own bytes), mirroring CI. Includes sabotage negative controls: a gate
that can be bypassed is not a gate.

Convention (sibling-gate lesson): the shipped-manifest tests assert
well-formed-and-honest, NOT DORMANT - the owning lane registers real
claims without editing these tests.
"""
import json
import os
import subprocess
import sys

import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join(REPO_ROOT, "tools", "d31_incident_claims_gate.py")
MANIFEST = os.path.join(
    REPO_ROOT, "tools", "d31_incident_claims_manifest.json")


def run_gate(manifest_path, extra_args=()):
    env = dict(os.environ)
    env["PYTHONPATH"] = REPO_ROOT + os.pathsep + env.get("PYTHONPATH", "")
    proc = subprocess.run(
        [sys.executable, GATE, manifest_path] + list(extra_args),
        capture_output=True, text=True, env=env, timeout=120)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def write_manifest(tmp_path, payload):
    path = str(tmp_path / "manifest.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh)
    return path


def load_shipped():
    with open(MANIFEST, "r", encoding="utf-8") as fh:
        return json.load(fh)


def examples():
    manifest = load_shipped()
    return {k: v for k, v in manifest.items()
            if k.startswith("_example") and isinstance(v, dict)}


def promote(example):
    """Promote a worked example to a live scenario for judging."""
    ex = dict(example)
    ex["id"] = ex["id"].lstrip("_")
    return ex


# ---------------------------------------------------------------------------
# Shipped manifest: well-formed and honest (not pinned to DORMANT)
# ---------------------------------------------------------------------------

def test_shipped_manifest_well_formed():
    manifest = load_shipped()
    assert isinstance(manifest, dict)
    assert isinstance(manifest.get("scenarios"), list)
    ex = examples()
    assert len(ex) >= 8, "worked examples missing: %s" % sorted(ex)
    for key, scenario in ex.items():
        assert scenario["kind"] in (
            "verdict_match", "refusal", "cold_successor"), key


def test_shipped_examples_deserialize_clean():
    """Every worked example's incident bytes rebuild through the seam."""
    sys.path.insert(0, REPO_ROOT)
    from drift_canary.d31_incident import deserialize_incident
    for key, scenario in examples().items():
        if "incident_hex" not in scenario:
            continue
        incident = deserialize_incident(bytes.fromhex(scenario["incident_hex"]))
        assert incident.incident_id, key


def test_shipped_manifest_judges_clean():
    code, out, _ = run_gate(MANIFEST)
    assert code == 0, out
    assert "D31-GATE" in out


def test_live_registration_path_honest(tmp_path):
    """The owning lane can register a real claim without editing tests:
    an honest live scenario passes."""
    honest = promote(examples()["_example_honest"])
    path = write_manifest(tmp_path, {"scenarios": [honest]})
    code, out, _ = run_gate(path)
    assert code == 0, out
    assert "PASS" in out


# ---------------------------------------------------------------------------
# Worked examples: honest passes, frauds violate with the disagreement named
# ---------------------------------------------------------------------------

def test_example_honest_passes(tmp_path):
    honest = promote(examples()["_example_honest"])
    path = write_manifest(tmp_path, {"scenarios": [honest]})
    code, out, _ = run_gate(path)
    assert code == 0, out


def test_example_honest_cold_passes(tmp_path):
    honest = promote(examples()["_example_honest_cold"])
    path = write_manifest(tmp_path, {"scenarios": [honest]})
    code, out, _ = run_gate(path)
    assert code == 0, out


def test_example_fraud_verdict_blocked(tmp_path):
    fraud = promote(examples()["_example_fraud_verdict"])
    path = write_manifest(tmp_path, {"scenarios": [fraud]})
    code, out, _ = run_gate(path)
    assert code == 1, out
    assert "VIOLATION" in out
    assert "is_blocked" in out and "actual=True" in out


def test_example_fraud_failure_reason_blocked(tmp_path):
    fraud = promote(examples()["_example_fraud_failure_reason"])
    path = write_manifest(tmp_path, {"scenarios": [fraud]})
    code, out, _ = run_gate(path)
    assert code == 1, out
    assert "failure_reason" in out


def test_example_fraud_promotion_blocked(tmp_path):
    fraud = promote(examples()["_example_fraud_promotion"])
    path = write_manifest(tmp_path, {"scenarios": [fraud]})
    code, out, _ = run_gate(path)
    assert code == 1, out
    assert "PermissionError" in out


def test_example_fraud_blocker_blocked(tmp_path):
    fraud = promote(examples()["_example_fraud_blocker"])
    path = write_manifest(tmp_path, {"scenarios": [fraud]})
    code, out, _ = run_gate(path)
    assert code == 1, out
    assert "ValueError" in out


def test_example_fraud_single_witness_blocked(tmp_path):
    fraud = promote(examples()["_example_fraud_single_witness"])
    path = write_manifest(tmp_path, {"scenarios": [fraud]})
    code, out, _ = run_gate(path)
    assert code == 1, out
    assert "UNDETERMINED" in out


def test_example_fraud_partial_completion_blocked(tmp_path):
    fraud = promote(examples()["_example_fraud_partial_completion"])
    path = write_manifest(tmp_path, {"scenarios": [fraud]})
    code, out, _ = run_gate(path)
    assert code == 1, out
    assert "completion_declared" in out


# ---------------------------------------------------------------------------
# Fail-closed: broken inputs never pass
# ---------------------------------------------------------------------------

def test_corrupt_manifest_fails_closed(tmp_path):
    path = str(tmp_path / "bad.json")
    with open(path, "w") as fh:
        fh.write("{not json")
    code, out, _ = run_gate(path)
    assert code == 2, out
    assert "BROKEN" in out


def test_missing_manifest_fails_closed(tmp_path):
    code, out, _ = run_gate(str(tmp_path / "nope.json"))
    assert code == 2, out
    assert "BROKEN" in out


def test_unknown_scenario_kind_fails_closed(tmp_path):
    path = write_manifest(
        tmp_path, {"scenarios": [{"id": "x", "kind": "nope"}]})
    code, out, _ = run_gate(path)
    assert code == 2, out
    assert "BROKEN" in out


def test_tampered_incident_bytes_fail_closed(tmp_path):
    honest = promote(examples()["_example_honest"])
    blob = bytearray(bytes.fromhex(honest["incident_hex"]))
    blob[len(blob) // 2] ^= 0xFF
    honest["incident_hex"] = bytes(blob).hex()
    path = write_manifest(tmp_path, {"scenarios": [honest]})
    code, out, _ = run_gate(path)
    # Tamper either breaks the seam (exit 2) or degrades the verdict
    # (exit 1 on the now-dishonest claim). A silent pass is the failure.
    assert code in (1, 2), out
    assert code != 0


def test_neutered_engine_fails_canary(tmp_path):
    """Sabotage control: a blind analyzer must trip canary C1, never pass."""
    import shutil
    shadow_parent = str(tmp_path / "shadow")
    shutil.copytree(os.path.join(REPO_ROOT, "drift_canary"),
                    os.path.join(shadow_parent, "drift_canary"))
    shadow = os.path.join(shadow_parent, "drift_canary")
    with open(os.path.join(shadow, "d31_incident.py"), "a") as fh:
        fh.write(
            "\nclass _BlindVerdict:\n"
            "    is_blocked = False\n"
            "    completion_declared = True\n"
            "    blockers_established = ()\n"
            "    unresolved_hypotheses = ()\n"
            "    claim_verdicts = ()\n"
            "def _blind_verdict(self, incident):\n"
            "    return _BlindVerdict()\n"
            "IncidentAnalyzer.verdict = _blind_verdict\n")
    env = dict(os.environ)
    env["PYTHONPATH"] = str(tmp_path / "shadow")
    proc = subprocess.run(
        [sys.executable, GATE], capture_output=True, text=True,
        env=env, timeout=120)
    assert proc.returncode == 2, proc.stdout
    assert "canary C1" in proc.stdout


def test_refusal_honest_direction_passes(tmp_path):
    """A refusal claim asserting the engine DOES refuse must pass."""
    fraud = promote(examples()["_example_fraud_promotion"])
    fraud["asserted_refused"] = True
    path = write_manifest(tmp_path, {"scenarios": [fraud]})
    code, out, _ = run_gate(path)
    assert code == 0, out
