"""Tests for tools/d62_pumping_witness_gate.py.

These tests judge the gate against the REAL D62 verifier
(drift_canary/pumping_witness.py) — the wire branch is stacked on the
mechanism PR (#2318), so the real bytes are on the tree. No fakes: a fake
verifier could diverge from the mechanism and the tests would lie.
On a tree without the mechanism the module skips with an explicit reason
(UNKNOWN, never PASS).
"""

import base64
import dataclasses
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

MECH = pytest.importorskip(
    "drift_canary.pumping_witness",
    reason="D62 mechanism absent on this tree — gate tests need the real "
           "verifier (wire branch stacked on PR #2318)")

TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools"
GATE_PATH = TOOLS_DIR / "d62_pumping_witness_gate.py"
MANIFEST_PATH = TOOLS_DIR / "d62_pumping_witness_manifest.json"


def _load_gate():
    spec = importlib.util.spec_from_file_location(
        "d62_pumping_witness_gate", GATE_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture()
def gate():
    return _load_gate()


def _b64(cert):
    return base64.b64encode(MECH.certificate_to_json(cert)).decode()


def _claim(cert_b64, asserts="PROVEN_UNBOUNDED", cid="PW-TEST-1",
           obligation_id="test-obligation"):
    return {
        "id": cid,
        "obligation_id": obligation_id,
        "claimant": "wire-lane test",
        "evidence_ref": "test",
        "asserts": asserts,
        "certificate_b64": cert_b64,
    }


def _write_manifest(tmp_path, claims):
    p = tmp_path / "manifest.json"
    p.write_text(json.dumps({"claims": claims}), encoding="utf-8")
    return p


def _fixtures():
    return MECH.fixtures_aer_live_007()


# ---------------------------------------------------------------------------
# DORMANT — the honest empty state.
# ---------------------------------------------------------------------------

def test_absent_manifest_dormant(gate, tmp_path):
    assert gate.main(
        ["--manifest", str(tmp_path / "nope.json")]) == 0


def test_empty_claims_dormant(gate, tmp_path):
    p = _write_manifest(tmp_path, [])
    assert gate.main(["--manifest", str(p)]) == 0


def test_shipped_manifest_dormant(gate):
    # The manifest shipped with the wire registers zero claims: the gate
    # must say DORMANT explicitly, never a false green.
    assert gate.main(["--manifest", str(MANIFEST_PATH)]) == 0


# ---------------------------------------------------------------------------
# PASS — the real verifier certifies a real certificate.
# ---------------------------------------------------------------------------

def test_valid_certificate_certified(gate, tmp_path):
    fx = _fixtures()
    p = _write_manifest(tmp_path, [_claim(_b64(fx["valid"]))])
    assert gate.main(["--manifest", str(p)]) == 0


# ---------------------------------------------------------------------------
# VIOLATION — the gate blocks what the law forbids.
# ---------------------------------------------------------------------------

def test_two_token_defect_blocked_names_repetition_3(gate, tmp_path, capsys):
    # The exact false witness D62 exists to catch: the naive shape-only
    # checker declares it PROVEN_UNBOUNDED; the real verifier rejects at
    # repetition 3. The gate must block it and name the counterexample.
    fx = _fixtures()
    assert MECH.naive_unbounded_checker(fx["two_token_defect"]) == \
        MECH.PROVEN_UNBOUNDED  # the bug, confirmed present
    p = _write_manifest(tmp_path, [_claim(_b64(fx["two_token_defect"]))])
    assert gate.main(["--manifest", str(p)]) == 1
    out = capsys.readouterr().out
    assert "repetition 3" in out


def test_mandatory_reset_defect_blocked(gate, tmp_path):
    fx = _fixtures()
    p = _write_manifest(tmp_path, [_claim(_b64(fx["mandatory_reset_defect"]))])
    assert gate.main(["--manifest", str(p)]) == 1


def test_unreachable_exit_defect_blocked(gate, tmp_path):
    fx = _fixtures()
    p = _write_manifest(tmp_path, [_claim(_b64(fx["unreachable_exit_defect"]))])
    assert gate.main(["--manifest", str(p)]) == 1


def test_non_minimal_certificate_blocked(gate, tmp_path):
    # A certificate carrying a zero-debt cycle step is not a minimization
    # fixed point — refused with the redundant part named, never silently
    # repaired.
    fx = _fixtures()
    valid = fx["valid"]
    padded = dataclasses.replace(
        valid,
        cycle=valid.cycle + (MECH.PumpingStep(
            name="Z:zero-debt-padding", debt_delta=0),))
    p = _write_manifest(tmp_path, [_claim(_b64(padded))])
    assert gate.main(["--manifest", str(p)]) == 1


def test_malformed_certificate_bytes_blocked(gate, tmp_path):
    # Decodable base64, garbage content: the cold verifier fails closed and
    # the claim is BLOCKED (exit 1) — the claim's evidence is untrustworthy,
    # not the manifest.
    bad = base64.b64encode(b'{"not": "a certificate"}').decode()
    p = _write_manifest(tmp_path, [_claim(bad)])
    assert gate.main(["--manifest", str(p)]) == 1


def test_breach_assertion_blocked_quantifier_separation(gate, tmp_path, capsys):
    # A pumping witness proves the unbounded peak, never a proven violation.
    # Asserting BREACH from a witness is a starvation accusation — blocked.
    fx = _fixtures()
    p = _write_manifest(
        tmp_path, [_claim(_b64(fx["valid"]), asserts="BREACH")])
    assert gate.main(["--manifest", str(p)]) == 1
    out = capsys.readouterr().out
    assert "starvation accusation" in out


def test_upgrade_to_breach_always_refuses():
    # Dogfood the mechanism's own integrity: the refusal the gate depends
    # on must hold on the real bytes.
    fx = _fixtures()
    verdict = MECH.verify_pumping_witness(fx["valid"])
    assert verdict.accepted
    with pytest.raises(MECH.StarvationAccusationError):
        MECH.upgrade_to_breach(verdict)


# ---------------------------------------------------------------------------
# BROKEN — fail-closed on untrustworthy inputs or a missing mechanism.
# ---------------------------------------------------------------------------

def test_corrupt_manifest_broken(gate, tmp_path):
    p = tmp_path / "manifest.json"
    p.write_text("{not json", encoding="utf-8")
    assert gate.main(["--manifest", str(p)]) == 2


def test_manifest_wrong_shape_broken(gate, tmp_path):
    p = tmp_path / "manifest.json"
    p.write_text(json.dumps({"claims": {}}), encoding="utf-8")
    assert gate.main(["--manifest", str(p)]) == 2


def test_duplicate_claim_id_broken(gate, tmp_path):
    fx = _fixtures()
    c = _claim(_b64(fx["valid"]))
    p = _write_manifest(tmp_path, [c, dict(c)])
    assert gate.main(["--manifest", str(p)]) == 2


def test_missing_key_broken(gate, tmp_path):
    fx = _fixtures()
    c = _claim(_b64(fx["valid"]))
    del c["certificate_b64"]
    p = _write_manifest(tmp_path, [c])
    assert gate.main(["--manifest", str(p)]) == 2


def test_unknown_asserts_broken_never_defaulted(gate, tmp_path):
    fx = _fixtures()
    p = _write_manifest(
        tmp_path, [_claim(_b64(fx["valid"]), asserts="MAYBE_UNBOUNDED")])
    assert gate.main(["--manifest", str(p)]) == 2


def test_invalid_base64_broken(gate, tmp_path):
    fx = _fixtures()
    c = _claim(_b64(fx["valid"]))
    c["certificate_b64"] = "!!! not base64 !!!"
    p = _write_manifest(tmp_path, [c])
    assert gate.main(["--manifest", str(p)]) == 2


def test_mechanism_missing_with_claims_broken(gate, tmp_path, monkeypatch):
    # Claims exist but the verifier is absent: the gate refuses to certify
    # on defaults — BROKEN, never a pass.
    fx = _fixtures()
    p = _write_manifest(tmp_path, [_claim(_b64(fx["valid"]))])
    real_import = gate._load_mechanism

    def _missing():
        raise gate.MechanismMissing("simulated absence")
    monkeypatch.setattr(gate, "_load_mechanism", _missing)
    try:
        assert gate.main(["--manifest", str(p)]) == 2
    finally:
        monkeypatch.setattr(gate, "_load_mechanism", real_import)


def test_mechanism_integrity_break_fails_closed(gate, tmp_path, monkeypatch):
    # If upgrade_to_breach ever stops refusing, the mechanism's quantifier
    # separation is broken and the gate fails closed (exit 2), never passes.
    fx = _fixtures()
    p = _write_manifest(tmp_path, [_claim(_b64(fx["valid"]))])

    def _compliant(_verdict):
        return None  # the break: returns instead of refusing
    monkeypatch.setattr(MECH, "upgrade_to_breach", _compliant)
    assert gate.main(["--manifest", str(p)]) == 2


# ---------------------------------------------------------------------------
# CLI surface.
# ---------------------------------------------------------------------------

def test_cli_json_dormant(tmp_path):
    p = tmp_path / "manifest.json"
    p.write_text(json.dumps({"claims": []}), encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, str(GATE_PATH), "--manifest", str(p), "--json"],
        capture_output=True, text=True, cwd=TOOLS_DIR.parent)
    assert proc.returncode == 0
    payload = json.loads(proc.stdout)
    assert payload["verdict"] == "DORMANT"
