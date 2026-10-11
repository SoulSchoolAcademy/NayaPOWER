"""Tests for tools/d63_fullstate_repeatability_gate.py.

These tests judge the gate against the REAL D63 engine
(drift_canary/full_state_repeatability.py) — the wire branch is stacked on
the mechanism PR (#2320), so the real bytes are on the tree. No fakes: a
fake engine could diverge from the mechanism and the tests would lie.
On a tree without the mechanism the module skips with an explicit reason
(UNKNOWN, never PASS).
"""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

MECH = pytest.importorskip(
    "drift_canary.full_state_repeatability",
    reason="D63 mechanism absent on this tree — gate tests need the real "
           "engine (wire branch stacked on PR #2320)")

TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools"
GATE_PATH = TOOLS_DIR / "d63_fullstate_repeatability_gate.py"
MANIFEST_PATH = TOOLS_DIR / "d63_fullstate_repeatability_manifest.json"


def _load_gate():
    spec = importlib.util.spec_from_file_location(
        "d63_fullstate_repeatability_gate", GATE_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture()
def gate():
    return _load_gate()


@pytest.fixture()
def fixtures():
    return MECH.fixtures_aer_live_008()


def _cert_dict(cert):
    return json.loads(MECH.certificate_to_json(cert).decode("utf-8"))


def _claim(asserts, cert_dict, cid="FS-TEST-1",
           obligation_id="aer-live-008"):
    return {
        "id": cid,
        "obligation_id": obligation_id,
        "claimant": "wire-lane test",
        "evidence_ref": "test",
        "asserts": asserts,
        "certificate": cert_dict,
    }


def _write_manifest(tmp_path, claims):
    p = tmp_path / "manifest.json"
    p.write_text(json.dumps({"claims": claims}), encoding="utf-8")
    return p


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
# PASS — the real engine certifies real claims.
# ---------------------------------------------------------------------------

def test_honest_repeatable_claim_certified(gate, tmp_path, fixtures):
    # The AER-LIVE-008 valid certificate establishes arbitrary
    # repeatability across the full state — the claim asserts REPEATABLE
    # and the cold engine agrees.
    p = _write_manifest(tmp_path, [_claim(
        "REPEATABLE", _cert_dict(fixtures["valid"]))])
    assert gate.main(["--manifest", str(p)]) == 0


def test_honest_not_repeatable_claim_certified(gate, tmp_path, fixtures):
    # An honest negative claim is certifiable: the authority-expiry
    # certificate is NOT_REPEATABLE and the claim says so.
    p = _write_manifest(tmp_path, [_claim(
        "NOT_REPEATABLE",
        _cert_dict(fixtures["authority_expiry_defect"]))])
    assert gate.main(["--manifest", str(p)]) == 0


# ---------------------------------------------------------------------------
# VIOLATION — the gate blocks what the law refuses.
# ---------------------------------------------------------------------------

def test_authority_expiry_asserting_repeatable_blocked(
        gate, tmp_path, fixtures, capsys):
    # The flagship fraud D63 exists to prevent: debt-positive every
    # traversal, but the authority token expires after 50 traversals. The
    # naive debt-gain-only checker wrongly declares it repeatable — D63
    # rejects it at repetition 51 with the minimal counterexample named.
    p = _write_manifest(tmp_path, [_claim(
        "REPEATABLE",
        _cert_dict(fixtures["authority_expiry_defect"]))])
    assert gate.main(["--manifest", str(p)]) == 1
    out = capsys.readouterr().out
    assert "repetition 51" in out
    assert "authority_valid" in out


def test_budget_drain_asserting_repeatable_blocked(
        gate, tmp_path, fixtures, capsys):
    # Each traversal costs 5 budget from 100 — the invariant breaks at
    # repetition 20. A REPEATABLE claim over it is blocked.
    p = _write_manifest(tmp_path, [_claim(
        "REPEATABLE",
        _cert_dict(fixtures["budget_drain_defect"]))])
    assert gate.main(["--manifest", str(p)]) == 1
    out = capsys.readouterr().out
    assert "repetition 20" in out
    assert "budget_remaining" in out


def test_zero_gain_asserting_repeatable_blocked(
        gate, tmp_path, fixtures, capsys):
    # No positive debt gain — proof obligation 3 fails outright.
    # Repetition without debt gain proves nothing.
    p = _write_manifest(tmp_path, [_claim(
        "REPEATABLE",
        _cert_dict(fixtures["zero_gain_defect"]))])
    assert gate.main(["--manifest", str(p)]) == 1
    out = capsys.readouterr().out
    assert "proof obligation 3" in out


def test_finite_retries_control_asserting_repeatable_blocked(
        gate, tmp_path, fixtures, capsys):
    # CONTROL: 3 finite retries cannot support the arbitrary-repetition
    # claim — retries exhaust at repetition 4. Only eligible waiting
    # (retry_budget=None) leaves the retry constraint unbound.
    p = _write_manifest(tmp_path, [_claim(
        "REPEATABLE",
        _cert_dict(fixtures["finite_retries_defect"]))])
    assert gate.main(["--manifest", str(p)]) == 1
    out = capsys.readouterr().out
    assert "repetition 4" in out


def test_broken_entry_asserting_repeatable_blocked(
        gate, tmp_path, fixtures, capsys):
    # Entry violates the invariant at repetition 0 — proof obligation 1
    # fails before any repetition happens.
    p = _write_manifest(tmp_path, [_claim(
        "REPEATABLE",
        _cert_dict(fixtures["broken_entry_defect"]))])
    assert gate.main(["--manifest", str(p)]) == 1
    out = capsys.readouterr().out
    assert "repetition 0" in out


def test_unaffordable_exit_asserting_repeatable_blocked(
        gate, tmp_path, fixtures, capsys):
    # The invariant holds arbitrarily, but the exit itself is never
    # affordable — proof obligation 4 fails independently of preservation.
    p = _write_manifest(tmp_path, [_claim(
        "REPEATABLE",
        _cert_dict(fixtures["unaffordable_exit_defect"]))])
    assert gate.main(["--manifest", str(p)]) == 1
    out = capsys.readouterr().out
    assert "exit not available" in out


def test_malformed_certificate_bytes_blocked(gate, tmp_path, capsys):
    # Certificate bytes that fail the mechanism's own shape checks are the
    # claim's fault — the law refuses them (VIOLATION), not the manifest's
    # (BROKEN). Here: entry_state missing required components.
    bad = {"obligation_id": "aer-live-008", "entry_state": {"authority_valid": True}}
    p = _write_manifest(tmp_path, [_claim("REPEATABLE", bad)])
    assert gate.main(["--manifest", str(p)]) == 1
    out = capsys.readouterr().out
    assert "CertificateSerializationError" in out


def test_cross_obligation_certificate_blocked(gate, tmp_path, fixtures, capsys):
    # The certificate binds aer-live-008; the claim asserts a different
    # obligation. Cross-obligation judgment is refused by construction.
    p = _write_manifest(tmp_path, [_claim(
        "REPEATABLE", _cert_dict(fixtures["valid"]),
        obligation_id="some-other-obligation")])
    assert gate.main(["--manifest", str(p)]) == 1
    out = capsys.readouterr().out
    assert "cross-obligation" in out


def test_upgrade_to_authorization_refused(gate, fixtures):
    # The mechanical separation the gate dogfoods: a repeatability verdict
    # is never a production authorization — the mechanism always refuses.
    mech = gate._load_mechanism()
    verdict = mech.verify_full_state_repeatability(fixtures["valid"])
    assert verdict.authorization == mech.UNDETERMINED
    with pytest.raises(mech.ProductionAuthorizationError):
        mech.upgrade_to_authorization(verdict)


# ---------------------------------------------------------------------------
# BROKEN — fail closed on untrustworthy inputs.
# ---------------------------------------------------------------------------

def test_corrupt_manifest_broken(gate, tmp_path):
    p = tmp_path / "manifest.json"
    p.write_text("{not json", encoding="utf-8")
    assert gate.main(["--manifest", str(p)]) == 2


def test_manifest_wrong_shape_broken(gate, tmp_path):
    p = tmp_path / "manifest.json"
    p.write_text(json.dumps({"claims": {}}), encoding="utf-8")
    assert gate.main(["--manifest", str(p)]) == 2


def test_duplicate_claim_id_broken(gate, tmp_path, fixtures):
    cert = _cert_dict(fixtures["valid"])
    p = _write_manifest(tmp_path, [
        _claim("REPEATABLE", cert, cid="FS-DUP"),
        _claim("NOT_REPEATABLE", cert, cid="FS-DUP")])
    assert gate.main(["--manifest", str(p)]) == 2


def test_missing_key_broken(gate, tmp_path, fixtures):
    c = _claim("REPEATABLE", _cert_dict(fixtures["valid"]))
    del c["evidence_ref"]
    p = _write_manifest(tmp_path, [c])
    assert gate.main(["--manifest", str(p)]) == 2


def test_unknown_asserts_broken_never_defaulted(gate, tmp_path, fixtures):
    c = _claim("REPEATABLE", _cert_dict(fixtures["valid"]))
    c["asserts"] = "PROBABLY_REPEATABLE"
    p = _write_manifest(tmp_path, [c])
    assert gate.main(["--manifest", str(p)]) == 2


def test_certificate_not_a_dict_broken(gate, tmp_path):
    c = _claim("REPEATABLE", {"ok": True})
    c["certificate"] = "not-a-certificate"
    p = _write_manifest(tmp_path, [c])
    assert gate.main(["--manifest", str(p)]) == 2


def test_mechanism_missing_with_claims_broken(gate, tmp_path, fixtures,
                                              monkeypatch):
    # Claims exist but the engine is absent: the gate refuses to certify
    # on defaults — BROKEN, never a pass.
    p = _write_manifest(tmp_path, [_claim(
        "REPEATABLE", _cert_dict(fixtures["valid"]))])
    real_import = gate._load_mechanism

    def _missing():
        raise gate.MechanismMissing("simulated absence")
    monkeypatch.setattr(gate, "_load_mechanism", _missing)
    try:
        assert gate.main(["--manifest", str(p)]) == 2
    finally:
        monkeypatch.setattr(gate, "_load_mechanism", real_import)


def test_verdict_coherence_break_fails_closed(gate, tmp_path, fixtures,
                                              monkeypatch):
    # If the engine ever returns a verdict that violates its own
    # invariants (accepted REPEATABLE carrying a failure), the engine is
    # broken and the gate fails closed — never certifies.
    p = _write_manifest(tmp_path, [_claim(
        "REPEATABLE", _cert_dict(fixtures["valid"]))])
    mech = gate._load_mechanism()
    forged = object.__new__(mech.RepeatabilityVerdict)
    object.__setattr__(forged, "obligation_id", "aer-live-008")
    object.__setattr__(forged, "accepted", True)
    object.__setattr__(forged, "repeatability", mech.REPEATABLE)
    object.__setattr__(forged, "verified_up_to", None)
    object.__setattr__(forged, "authorization", mech.UNDETERMINED)
    object.__setattr__(forged, "demonstrated", ())
    object.__setattr__(forged, "failure", "forged failure on an accepted verdict")
    object.__setattr__(forged, "model_assumptions", ())
    object.__setattr__(forged, "certificate_fingerprint", "forged")

    def _forged(_payload):
        return forged
    monkeypatch.setattr(mech, "independent_verify", _forged)
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
