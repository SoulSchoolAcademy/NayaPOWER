"""Tests for tools/d64_dependency_order_gate.py.

These tests judge the gate against the REAL D64 engine
(drift_canary/dependency_ordered_verification.py) — the wire branch is
stacked on the mechanism PR (#2323), so the real bytes are on the tree.
No fakes: a fake engine could diverge from the mechanism and the tests
would lie. On a tree without the mechanism the module skips with an
explicit reason (UNKNOWN, never PASS).
"""

import dataclasses
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

MECH = pytest.importorskip(
    "drift_canary.dependency_ordered_verification",
    reason="D64 mechanism absent on this tree — gate tests need the real "
           "engine (wire branch stacked on PR #2323)")

TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools"
GATE_PATH = TOOLS_DIR / "d64_dependency_order_gate.py"
MANIFEST_PATH = TOOLS_DIR / "d64_dependency_order_manifest.json"


def _load_gate():
    spec = importlib.util.spec_from_file_location(
        "d64_dependency_order_gate", GATE_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture()
def gate():
    return _load_gate()


def _cert_dict(cert):
    return json.loads(MECH.serialize_certificate(cert).decode("utf-8"))


def _engine_summary(cert):
    v = MECH.independent_verify(MECH.serialize_certificate(cert))
    return {
        "primary_failures": list(v.primary_failures),
        "dependent_failures": list(v.dependent_failures),
        "invariant_verdicts": {iv.name: iv.verdict
                               for iv in v.invariant_verdicts},
    }


def _claim(asserts, cert_dict, cid="DO-TEST-1",
           obligation_id="AER-LIVE-009-F1", verdict=None):
    entry = {
        "id": cid,
        "obligation_id": obligation_id,
        "claimant": "wire-lane test",
        "evidence_ref": "test",
        "asserts": asserts,
        "certificate": cert_dict,
    }
    if verdict is not None:
        entry["verdict"] = verdict
    return entry


def _write_manifest(tmp_path, claims):
    p = tmp_path / "manifest.json"
    p.write_text(json.dumps({"claims": claims}), encoding="utf-8")
    return p


# ---------------------------------------------------------------------------
# DORMANT — the honest empty state.
# ---------------------------------------------------------------------------

def test_absent_manifest_dormant(gate, tmp_path):
    assert gate.main(["--manifest", str(tmp_path / "nope.json")]) == 0


def test_empty_claims_dormant(gate, tmp_path):
    assert gate.main(["--manifest",
                      str(_write_manifest(tmp_path, []))]) == 0


def test_shipped_manifest_dormant(gate):
    # The shipped manifest registers zero claims: explicit DORMANT, and
    # the AE-EXAMPLE stays documented-not-registered. When the first real
    # claim lands, this test must be updated — that is the activation
    # tripwire, not a failure.
    assert MANIFEST_PATH.exists()
    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    assert data["claims"] == []
    assert gate.main([]) == 0


# ---------------------------------------------------------------------------
# Honest claims — certified.
# ---------------------------------------------------------------------------

def test_honest_verified_claim_certified(gate, tmp_path):
    # F1: the claimant's summary is exactly what the cold engine judges.
    cert = _cert_dict(MECH.aer_live9_certificate_f1())
    p = _write_manifest(tmp_path, [_claim(
        "VERIFIED", cert, verdict=_engine_summary(
            MECH.aer_live9_certificate_f1()))])
    assert gate.main(["--manifest", str(p)]) == 0


def test_honest_rejected_claim_certified(gate, tmp_path):
    # The cyclic certificate with no joint: the law rejects it, the
    # claimant records REJECTED — an honest rejection record passes.
    cert = _cert_dict(MECH.aer_live9_certificate_cyclic())
    p = _write_manifest(tmp_path, [_claim(
        "REJECTED", cert, obligation_id="AER-LIVE-009-CYCLE",
        cid="DO-TEST-REJ")])
    assert gate.main(["--manifest", str(p)]) == 0


def test_honest_joint_claim_certified(gate, tmp_path):
    # Joint-covered cycle: accepted with DEFERRED members — honest
    # unknowns, not defects.
    joint = MECH.aer_live9_certificate_joint()
    cert = _cert_dict(joint)
    p = _write_manifest(tmp_path, [_claim(
        "VERIFIED", cert, obligation_id="AER-LIVE-009-JOINT",
        cid="DO-TEST-JOINT",
        verdict=_engine_summary(joint))])
    assert gate.main(["--manifest", str(p)]) == 0


# ---------------------------------------------------------------------------
# Fraudulent claims — blocked.
# ---------------------------------------------------------------------------

def test_collapsed_f6_asserting_verified_blocked(gate, tmp_path, capsys):
    # THE fraud D64 exists to prevent: F6's UNDETERMINED collapsed to
    # PROVEN_FALSE by the naive checker, asserted as VERIFIED. The gate
    # must block it and name the divergence.
    f6 = MECH.aer_live9_certificate_f6()
    naive = MECH.naive_dependency_checker(f6)
    verdict = {
        "primary_failures": [naive["primary_failure"]],
        "dependent_failures": [
            n for n in naive["verification_order"]
            if naive["verdicts"][n] == "PROVEN_FALSE"
            and n != naive["primary_failure"]],
        "invariant_verdicts": naive["verdicts"],
    }
    p = _write_manifest(tmp_path, [_claim(
        "VERIFIED", _cert_dict(f6), obligation_id="AER-LIVE-009-F6",
        cid="DO-TEST-COLLAPSE", verdict=verdict)])
    assert gate.main(["--manifest", str(p)]) == 1
    out = capsys.readouterr().out
    assert "UNDETERMINED never collapses" in out
    assert "timing" in out


def test_wrong_primary_failure_blocked(gate, tmp_path):
    # F1 judged right, but the claimant names the primary in the wrong
    # order — causal diagnosis runs in execution order, never any other.
    f1 = MECH.aer_live9_certificate_f1()
    summary = _engine_summary(f1)
    summary["primary_failures"] = list(reversed(
        summary["primary_failures"]))
    p = _write_manifest(tmp_path, [_claim(
        "VERIFIED", _cert_dict(f1), verdict=summary,
        cid="DO-TEST-PRIMARY")])
    assert gate.main(["--manifest", str(p)]) == 1


def test_invented_true_blocked(gate, tmp_path):
    # preservation is UNDETERMINED on F1 (evidence missing); asserting
    # PROVEN_TRUE invents a verdict.
    f1 = MECH.aer_live9_certificate_f1()
    summary = _engine_summary(f1)
    summary["invariant_verdicts"]["preservation"] = "PROVEN_TRUE"
    p = _write_manifest(tmp_path, [_claim(
        "VERIFIED", _cert_dict(f1), verdict=summary,
        cid="DO-TEST-TRUE")])
    assert gate.main(["--manifest", str(p)]) == 1


def test_rejected_certificate_asserting_verified_blocked(gate, tmp_path,
                                                         capsys):
    # Uncovered cycle asserted as VERIFIED — the law rejects it.
    cert = _cert_dict(MECH.aer_live9_certificate_cyclic())
    p = _write_manifest(tmp_path, [_claim(
        "VERIFIED", cert, obligation_id="AER-LIVE-009-CYCLE",
        cid="DO-TEST-CYC", verdict={
            "primary_failures": [], "dependent_failures": [],
            "invariant_verdicts": {"cycle_a": "UNDETERMINED",
                                   "cycle_b": "UNDETERMINED"}})])
    assert gate.main(["--manifest", str(p)]) == 1
    assert "circular dependency" in capsys.readouterr().out


def test_invented_refusal_blocked(gate, tmp_path):
    # The law accepts F1; recording REJECTED is an invented refusal.
    cert = _cert_dict(MECH.aer_live9_certificate_f1())
    p = _write_manifest(tmp_path, [_claim(
        "REJECTED", cert, cid="DO-TEST-INVREF")])
    assert gate.main(["--manifest", str(p)]) == 1


def test_failed_witness_claim_blocked(gate, tmp_path, capsys):
    # A witness whose steps do not replay under the original model: the
    # law kills the certificate (failed witness demotes to UNDETERMINED).
    # Asserting the certificate's own PROVEN_FALSE as VERIFIED must block.
    f1 = MECH.aer_live9_certificate_f1()
    cert = _cert_dict(f1)
    for w in cert["witnesses"]:
        if w["invariant"] == "temporal":
            w["steps"] = ["corrupt_evidence"]  # wrong model step: breaks
            # authority, not temporal — replay fails
    p = _write_manifest(tmp_path, [_claim(
        "VERIFIED", cert, verdict=_engine_summary(f1),
        cid="DO-TEST-WIT")])
    assert gate.main(["--manifest", str(p)]) == 1
    assert "witness" in capsys.readouterr().out.lower()


def test_malformed_certificate_blocked(gate, tmp_path, capsys):
    # Claim content the law cannot even parse: VIOLATION, never silent.
    p = _write_manifest(tmp_path, [_claim(
        "VERIFIED", {"not": "a certificate"},
        verdict={"primary_failures": [], "dependent_failures": [],
                 "invariant_verdicts": {"x": "PROVEN_TRUE"}},
        cid="DO-TEST-MAL")])
    assert gate.main(["--manifest", str(p)]) == 1
    assert "refuses this certificate" in capsys.readouterr().out


def test_cross_obligation_certificate_blocked(gate, tmp_path, capsys):
    # The certificate binds F1's obligation; the claim binds another.
    cert = _cert_dict(MECH.aer_live9_certificate_f1())
    p = _write_manifest(tmp_path, [_claim(
        "VERIFIED", cert, obligation_id="AER-LIVE-009-OTHER",
        verdict=_engine_summary(MECH.aer_live9_certificate_f1()),
        cid="DO-TEST-XOB")])
    assert gate.main(["--manifest", str(p)]) == 1
    assert "cross-obligation" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# Fail-closed — the gate refuses before it invents.
# ---------------------------------------------------------------------------

def test_corrupt_manifest_broken(gate, tmp_path):
    p = tmp_path / "manifest.json"
    p.write_text("{not json", encoding="utf-8")
    assert gate.main(["--manifest", str(p)]) == 2


def test_manifest_wrong_shape_broken(gate, tmp_path):
    p = tmp_path / "manifest.json"
    p.write_text(json.dumps({"claims": "nope"}), encoding="utf-8")
    assert gate.main(["--manifest", str(p)]) == 2


def test_duplicate_claim_id_broken(gate, tmp_path):
    cert = _cert_dict(MECH.aer_live9_certificate_f1())
    p = _write_manifest(tmp_path, [
        _claim("REJECTED", cert, cid="DO-DUP"),
        _claim("REJECTED", cert, cid="DO-DUP")])
    assert gate.main(["--manifest", str(p)]) == 2


def test_missing_key_broken(gate, tmp_path):
    entry = _claim("REJECTED",
                   _cert_dict(MECH.aer_live9_certificate_f1()))
    del entry["obligation_id"]
    p = _write_manifest(tmp_path, [entry])
    assert gate.main(["--manifest", str(p)]) == 2


def test_unknown_asserts_broken_never_defaulted(gate, tmp_path):
    entry = _claim("REPEATABLE",
                   _cert_dict(MECH.aer_live9_certificate_f1()))
    p = _write_manifest(tmp_path, [entry])
    assert gate.main(["--manifest", str(p)]) == 2


def test_certificate_not_a_dict_broken(gate, tmp_path):
    entry = _claim("REJECTED", "not-a-dict")
    p = _write_manifest(tmp_path, [entry])
    assert gate.main(["--manifest", str(p)]) == 2


def test_verified_without_verdict_summary_broken(gate, tmp_path):
    # VERIFIED with no asserted summary: the gate cannot compare —
    # fail closed, never assume.
    p = _write_manifest(tmp_path, [_claim(
        "VERIFIED", _cert_dict(MECH.aer_live9_certificate_f1()))])
    assert gate.main(["--manifest", str(p)]) == 2


def test_mechanism_missing_with_claims_broken(gate, tmp_path, monkeypatch):
    # Claims exist but the engine is absent: the gate refuses to certify
    # on defaults — BROKEN, never a pass.
    cert = _cert_dict(MECH.aer_live9_certificate_f1())
    p = _write_manifest(tmp_path, [_claim("REJECTED", cert)])

    def _missing():
        raise gate.MechanismMissing("simulated absence")
    monkeypatch.setattr(gate, "_load_mechanism", _missing)
    assert gate.main(["--manifest", str(p)]) == 2


def test_verdict_coherence_break_fails_closed(gate, tmp_path, monkeypatch):
    # If the engine ever returns a verdict whose verification order is
    # NOT a valid topological order over the certificate's own
    # prerequisite graph (an invented ordering smuggled through the
    # engine), the gate's own Kahn pass must catch it — fail closed.
    f1 = MECH.aer_live9_certificate_f1()
    real = MECH.independent_verify(MECH.serialize_certificate(f1))
    order = list(real.verification_order)
    # Move a dependent before its prerequisite: invented ordering.
    order.remove("authority")
    order.insert(order.index("temporal"), "authority")
    forged = dataclasses.replace(real, verification_order=tuple(order))

    def _forged(_payload):
        return forged
    monkeypatch.setattr(MECH, "independent_verify", _forged)
    try:
        cert = _cert_dict(f1)
        p = _write_manifest(tmp_path, [_claim(
            "VERIFIED", cert, verdict={
                "primary_failures": list(forged.primary_failures),
                "dependent_failures": list(forged.dependent_failures),
                "invariant_verdicts": {
                    iv.name: iv.verdict
                    for iv in forged.invariant_verdicts}})])
        assert gate.main(["--manifest", str(p)]) == 2
    finally:
        monkeypatch.undo()


# ---------------------------------------------------------------------------
# CLI surface.
# ---------------------------------------------------------------------------

def test_cli_json_dormant(tmp_path):
    p = _write_manifest(tmp_path, [])
    out = subprocess.run(
        [sys.executable, str(GATE_PATH), "--manifest", str(p), "--json"],
        capture_output=True, text=True, cwd=TOOLS_DIR.parent)
    assert out.returncode == 0
    assert json.loads(out.stdout)["verdict"] == "DORMANT"
