"""Tests for tools/d61_unbounded_debt_gate.py.

These tests judge the gate against the REAL D61 engine
(drift_canary/unbounded_debt_bounds.py) — the wire branch is stacked on the
mechanism PR (#2316), so the real bytes are on the tree. No fakes: a fake
engine could diverge from the mechanism and the tests would lie.
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
    "drift_canary.unbounded_debt_bounds",
    reason="D61 mechanism absent on this tree — gate tests need the real "
           "engine (wire branch stacked on PR #2316)")

TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools"
GATE_PATH = TOOLS_DIR / "d61_unbounded_debt_gate.py"
MANIFEST_PATH = TOOLS_DIR / "d61_unbounded_debt_manifest.json"


def _load_gate():
    spec = importlib.util.spec_from_file_location(
        "d61_unbounded_debt_gate", GATE_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture()
def gate():
    return _load_gate()


def _interval(lo=0, hi=0, exit=True):
    return {"entry_debt_lo": lo, "entry_debt_hi": hi,
            "must_end_with_service": exit}


def _contract(bound=5, standard="BOUNDED"):
    return {
        "revision": "r1",
        "standard": standard,
        "eligibility_predicate": "eligible when queued",
        "service_predicate": "adequate service when served",
        "service_bound_rounds": bound,
        "capacity_basis": "capacity plan v3: 5 slots per round",
    }


def _claim(asserts, interval, evidence, cid="DB-TEST-1",
           obligation_id="test-obligation", bound=5, standard="BOUNDED",
           finite_limit=None, tested_sla_ref=""):
    c = {
        "id": cid,
        "obligation_id": obligation_id,
        "claimant": "wire-lane test",
        "evidence_ref": "test",
        "asserts": asserts,
        "interval": interval,
        "contract": _contract(bound, standard),
        "evidence": evidence,
    }
    if finite_limit is not None:
        c["finite_limit"] = finite_limit
    if tested_sla_ref:
        c["tested_sla_ref"] = tested_sla_ref
    return c


def _limit(source="TRUSTED_SEQUENCE_NUMBERS", cap=5, ref="evidence:ok"):
    return {"source": source, "max_unserved_rounds": cap,
            "evidence_ref": ref}


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

def test_honest_breach_claim_certified(gate, tmp_path):
    # Entry 12 > bound 10: every defensible history's peak breaches — the
    # claim cites the 0-U peak witness exactly.
    p = _write_manifest(tmp_path, [_claim(
        "BREACH", _interval(lo=12, hi=12),
        {"peak_witness": {"entry_debt": 12, "unserved_rounds": 0}},
        bound=10)])
    assert gate.main(["--manifest", str(p)]) == 0


def test_honest_no_breach_via_finite_limit_certified(gate, tmp_path):
    # Trusted sequence numbers cap the unserved count at 5: peak in
    # [2, 8] against bound 10 — NO_BREACH established through the finite
    # limit, cited exactly (source, cap, evidence_ref).
    p = _write_manifest(tmp_path, [_claim(
        "NO_BREACH", _interval(lo=2, hi=3),
        {"finite_limit_source": "TRUSTED_SEQUENCE_NUMBERS",
         "max_unserved_rounds": 5, "evidence_ref": "evidence:ok"},
        bound=10, finite_limit=_limit(cap=5), tested_sla_ref="sla:other")])
    assert gate.main(["--manifest", str(p)]) == 0


def test_unresolved_claim_accepted(gate, tmp_path):
    # Holding undetermined over an unbounded interval is conservative and
    # always consistent — the verifier accepts it.
    p = _write_manifest(tmp_path, [_claim(
        "UNRESOLVED", _interval(lo=0, hi=0), {"note": "holding"})])
    assert gate.main(["--manifest", str(p)]) == 0


# ---------------------------------------------------------------------------
# VIOLATION — the gate blocks what the law refuses.
# ---------------------------------------------------------------------------

def test_aer_live_006_final_debt_only_blocked(gate, tmp_path, capsys):
    # The flagship fraud D61 exists to prevent: terminal service S clears
    # the counter (final 0), so the claim declares NO_BREACH on final-debt
    # evidence alone — over a PROVEN_UNBOUNDED peak. The independent
    # verifier refuses it; the gate must block and name the refusal.
    p = _write_manifest(tmp_path, [_claim(
        "NO_BREACH", _interval(lo=0, hi=0), {"final_debt": 0})])
    assert gate.main(["--manifest", str(p)]) == 1
    out = capsys.readouterr().out
    assert "FinalDebtOnlyClaimError" in out
    assert "final-debt-only" in out


def test_no_breach_against_unbounded_peak_blocked(gate, tmp_path, capsys):
    # Citing peak evidence does not help when the receipt verdict is not
    # NO_BREACH: compliance is establishable only through a finite limit.
    p = _write_manifest(tmp_path, [_claim(
        "NO_BREACH", _interval(lo=0, hi=0),
        {"peak_witness": {"entry_debt": 0, "unserved_rounds": 0}})])
    assert gate.main(["--manifest", str(p)]) == 1
    out = capsys.readouterr().out
    assert "PeakUnboundedClaimError" in out


def test_circular_finite_limit_blocked(gate, tmp_path, capsys):
    # The finite limit's evidence IS the SLA under test — the SLA can never
    # serve as its own enforcement evidence.
    p = _write_manifest(tmp_path, [_claim(
        "NO_BREACH", _interval(lo=2, hi=3),
        {"finite_limit_source": "TRUSTED_SEQUENCE_NUMBERS",
         "max_unserved_rounds": 5, "evidence_ref": "sla:under-test"},
        bound=10,
        finite_limit=_limit(cap=5, ref="sla:under-test"),
        tested_sla_ref="sla:under-test")])
    assert gate.main(["--manifest", str(p)]) == 1
    out = capsys.readouterr().out
    assert "CircularEvidenceError" in out


def test_unnamed_tested_sla_with_limit_blocked(gate, tmp_path, capsys):
    # A finite limit without the tested SLA named: circularity cannot be
    # excluded — the law fails closed.
    p = _write_manifest(tmp_path, [_claim(
        "NO_BREACH", _interval(lo=2, hi=3),
        {"finite_limit_source": "TRUSTED_SEQUENCE_NUMBERS",
         "max_unserved_rounds": 5, "evidence_ref": "evidence:ok"},
        bound=10, finite_limit=_limit(cap=5))])
    assert gate.main(["--manifest", str(p)]) == 1
    out = capsys.readouterr().out
    assert "CircularEvidenceError" in out


def test_unknown_limit_source_blocked(gate, tmp_path, capsys):
    # Only TRUSTED_SEQUENCE_NUMBERS / ENFORCED_RESET / LAW_WITHDRAWAL can
    # carry a finite limit — self-attestation is refused.
    p = _write_manifest(tmp_path, [_claim(
        "NO_BREACH", _interval(lo=2, hi=3), {"finite_limit_source": "x"},
        bound=10, finite_limit=_limit(source="SELF_ATTESTED"),
        tested_sla_ref="sla:other")])
    assert gate.main(["--manifest", str(p)]) == 1
    out = capsys.readouterr().out
    assert "UnknownLimitSourceError" in out


def test_breach_claim_with_wrong_witness_blocked(gate, tmp_path, capsys):
    # A BREACH claim must cite the 0-U peak witness at the receipt's entry
    # debt — a mismatched witness is receipt-inconsistent.
    p = _write_manifest(tmp_path, [_claim(
        "BREACH", _interval(lo=12, hi=12),
        {"peak_witness": {"entry_debt": 5, "unserved_rounds": 0}},
        bound=10)])
    assert gate.main(["--manifest", str(p)]) == 1
    out = capsys.readouterr().out
    assert "ClaimMismatchError" in out


def test_non_bounded_contract_blocked(gate, tmp_path, capsys):
    # An unbounded interval under a non-BOUNDED contract is doubly
    # unjudgeable — refused.
    p = _write_manifest(tmp_path, [_claim(
        "UNRESOLVED", _interval(lo=0, hi=0), {"note": "x"},
        standard="WEAK")])
    assert gate.main(["--manifest", str(p)]) == 1
    out = capsys.readouterr().out
    assert "UnboundedContractError" in out


def test_inverted_debt_interval_blocked(gate, tmp_path, capsys):
    # The claim's own interval is unjudgeable — the law refuses it.
    p = _write_manifest(tmp_path, [_claim(
        "UNRESOLVED", _interval(lo=5, hi=2), {"note": "x"})])
    assert gate.main(["--manifest", str(p)]) == 1
    out = capsys.readouterr().out
    assert "UnboundedDebtError" in out


def test_u_star_final_debt_only_blocked(gate, tmp_path, capsys):
    # U* without a demonstrated exit: the final debt is itself unbounded,
    # so a final-debt-only NO_BREACH is doubly fraudulent.
    p = _write_manifest(tmp_path, [_claim(
        "NO_BREACH", _interval(lo=0, hi=0, exit=False),
        {"final_debt": 0})])
    assert gate.main(["--manifest", str(p)]) == 1
    out = capsys.readouterr().out
    assert "FinalDebtOnlyClaimError" in out


# ---------------------------------------------------------------------------
# BROKEN — fail-closed on untrustworthy inputs or a broken engine.
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
    c = _claim("UNRESOLVED", _interval(lo=0, hi=0), {})
    p = _write_manifest(tmp_path, [c, dict(c)])
    assert gate.main(["--manifest", str(p)]) == 2


def test_missing_key_broken(gate, tmp_path):
    c = _claim("UNRESOLVED", _interval(lo=0, hi=0), {})
    del c["evidence"]
    p = _write_manifest(tmp_path, [c])
    assert gate.main(["--manifest", str(p)]) == 2


def test_unknown_asserts_broken_never_defaulted(gate, tmp_path):
    p = _write_manifest(tmp_path, [_claim(
        "MAYBE_COMPLIANT", _interval(lo=0, hi=0), {})])
    assert gate.main(["--manifest", str(p)]) == 2


def test_interval_not_a_dict_broken(gate, tmp_path):
    c = _claim("UNRESOLVED", _interval(lo=0, hi=0), {})
    c["interval"] = "unbounded-ish"
    p = _write_manifest(tmp_path, [c])
    assert gate.main(["--manifest", str(p)]) == 2


def test_mechanism_missing_with_claims_broken(gate, tmp_path, monkeypatch):
    # Claims exist but the engine is absent: the gate refuses to certify
    # on defaults — BROKEN, never a pass.
    p = _write_manifest(tmp_path, [_claim(
        "UNRESOLVED", _interval(lo=0, hi=0), {})])
    real_import = gate._load_mechanism

    def _missing():
        raise gate.MechanismMissing("simulated absence")
    monkeypatch.setattr(gate, "_load_mechanism", _missing)
    try:
        assert gate.main(["--manifest", str(p)]) == 2
    finally:
        monkeypatch.setattr(gate, "_load_mechanism", real_import)


def test_receipt_coherence_break_fails_closed(gate, tmp_path, monkeypatch):
    # If the engine ever returns a receipt that violates the
    # verdict-off-peak coherence (BREACH with peak_lower_bound <= bound),
    # the engine is broken and the gate fails closed — never certifies.
    p = _write_manifest(tmp_path, [_claim(
        "UNRESOLVED", _interval(lo=0, hi=0), {})])
    mech, _ = gate._load_mechanism()
    forged = object.__new__(mech.UnboundedDebtReceipt)
    object.__setattr__(forged, "verdict", mech.BREACH)
    object.__setattr__(forged, "peak_status", mech.PROVEN_UNBOUNDED)
    object.__setattr__(forged, "peak_lower_bound", 0)
    object.__setattr__(forged, "peak_upper_bound", None)
    object.__setattr__(forged, "bound", 10)
    object.__setattr__(forged, "finite_limit", None)

    def _forged(_iv, _co, _fl=None, _sla=""):
        return forged
    monkeypatch.setattr(mech.UnboundedDebtEngine, "assess",
                        staticmethod(_forged))
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
