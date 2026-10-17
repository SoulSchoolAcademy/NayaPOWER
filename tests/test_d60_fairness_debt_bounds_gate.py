"""Tests for tools/d60_fairness_debt_bounds_gate.py.

Fake-mechanism injection: the D60 engine is not on this tree (PR #2315
unmerged), so tests inject a faithful fake of the mechanism's API surface
into sys.modules. The fire battery (not committed) judges the same gate
against the REAL #2315/#2313/#2311 bytes.
"""

import importlib.util
import json
import sys
import types
from pathlib import Path

import pytest

TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools"
GATE_PATH = TOOLS_DIR / "d60_fairness_debt_bounds_gate.py"

FAKE_COMPONENTS = (
    "AUTHORIZATION",
    "OUTSTANDING_WORK",
    "READY_DEPENDENCIES",
    "SCHEDULABLE_CAPACITY",
    "APPLICABLE_OPPORTUNITY",
    "CONSISTENT_ORDERING",
)
FAKE_VERDICTS = ("ELIGIBLE", "INELIGIBLE", "UNDETERMINED")
FAKE_DEFECT_KINDS = ("MISSING", "CONTRADICTORY", "STALE", "UNVERIFIABLE")
FAKE_BREACH_VERDICTS = ("BREACH", "NO_BREACH", "UNRESOLVED")


class FakeDebtBoundError(Exception):
    pass


class FakeMissingIntervalTooLongError(FakeDebtBoundError):
    pass


class FakeComponentDefect:
    def __init__(self, component, kind, detail):
        assert component in FAKE_COMPONENTS, component
        assert kind in FAKE_DEFECT_KINDS, kind
        assert detail, "detail required"
        self.component = component
        self.kind = kind
        self.detail = detail


class FakeRoundRecord:
    def __init__(self, round_seq, obligation_id, verdict,
                 adequate_service, defects=(), receipt=None):
        assert verdict in FAKE_VERDICTS, verdict
        assert isinstance(adequate_service, bool), adequate_service
        assert obligation_id, "obligation id required"
        if verdict == "UNDETERMINED":
            assert defects, "UNDETERMINED needs defects"
        else:
            assert not defects, "settled verdicts carry no defects"
        self.round_seq = round_seq
        self.obligation_id = obligation_id
        self.verdict = verdict
        self.adequate_service = adequate_service
        self.defects = defects


class FakeReceipt:
    def __init__(self, obligation_id, bound, verdict, debt_min, debt_max,
                 histories_admitted, unresolved_rounds,
                 missing_intervals=()):
        self.obligation_id = obligation_id
        self.bound = bound
        self.verdict = verdict
        self.debt_min = debt_min
        self.debt_max = debt_max
        self.histories_admitted = histories_admitted
        self.unresolved_rounds = unresolved_rounds
        self.missing_intervals = missing_intervals


class FakeEngine:
    # obligation_id -> FakeReceipt or Exception to raise from compute()
    script = {}

    @staticmethod
    def compute(rounds, contract):
        oid = rounds[0].obligation_id if rounds else None
        entry = FakeEngine.script.get(oid)
        if isinstance(entry, Exception):
            raise entry
        assert entry is not None, f"no script for {oid}"
        return entry


class FakeFairnessContract:
    def __init__(self, obligation_id, revision, standard,
                 eligibility_predicate, service_predicate,
                 service_bound_rounds=0, capacity_basis="",
                 wait_accounting="ELIGIBLE_SCHEDULER_ROUNDS",
                 preserve_across_reassignment=True):
        assert standard == "BOUNDED", standard
        assert obligation_id
        assert service_bound_rounds > 0
        assert capacity_basis, "BOUNDED needs a capacity basis"
        self.service_bound_rounds = service_bound_rounds


def _install_fakes():
    pkg = types.ModuleType("drift_canary")
    pkg.__path__ = []
    d60 = types.ModuleType("drift_canary.fairness_debt_bounds")
    d60.DebtBoundEngine = FakeEngine
    d60.DebtBoundError = FakeDebtBoundError
    d60.MissingIntervalTooLongError = FakeMissingIntervalTooLongError
    d60.MAX_MISSING_INTERVAL_ROUNDS = 64
    ue = types.ModuleType("drift_canary.unresolved_evidence")
    ue.RoundRecord = FakeRoundRecord
    ue.ComponentDefect = FakeComponentDefect
    ue.DEFECT_KINDS = FAKE_DEFECT_KINDS
    ue.BREACH_VERDICTS = FAKE_BREACH_VERDICTS
    ue.VERDICTS = FAKE_VERDICTS
    eproof = types.ModuleType("drift_canary.eligibility_proof")
    eproof.COMPONENTS = FAKE_COMPONENTS
    fairness = types.ModuleType("drift_canary.fairness")
    fairness.FairnessContract = FakeFairnessContract
    sys.modules["drift_canary"] = pkg
    sys.modules["drift_canary.fairness_debt_bounds"] = d60
    sys.modules["drift_canary.unresolved_evidence"] = ue
    sys.modules["drift_canary.eligibility_proof"] = eproof
    sys.modules["drift_canary.fairness"] = fairness


def _remove_fakes():
    for name in ("drift_canary", "drift_canary.fairness_debt_bounds",
                 "drift_canary.unresolved_evidence",
                 "drift_canary.eligibility_proof", "drift_canary.fairness"):
        sys.modules.pop(name, None)


def _load_gate():
    spec = importlib.util.spec_from_file_location(
        "d60_fairness_debt_bounds_gate", GATE_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture()
def gate():
    _install_fakes()
    try:
        yield _load_gate()
    finally:
        _remove_fakes()
        FakeEngine.script = {}


def _write_manifest(tmp_path, claims):
    p = tmp_path / "manifest.json"
    p.write_text(json.dumps({"claims": claims}), encoding="utf-8")
    return str(p)


def _claim(cid="DB-0001", obligation_id="ob", bound=3,
           asserted="NO_BREACH", rounds=None):
    if rounds is None:
        rounds = [
            {"round_seq": 1, "verdict": "eligible",
             "adequate_service": False, "defects": []},
        ]
    return {
        "id": cid,
        "obligation_id": obligation_id,
        "bound": bound,
        "capacity_basis": "scheduler capacity audit",
        "asserted_conclusion": asserted,
        "rounds": rounds,
    }


def _ok_receipt(obligation_id="ob", bound=3, verdict="NO_BREACH",
                debt_min=0, debt_max=2):
    return FakeReceipt(obligation_id, bound, verdict, debt_min, debt_max,
                       histories_admitted=4, unresolved_rounds=(4, 5))


# --- DORMANT ---------------------------------------------------------------

def test_dormant_manifest_absent(gate, tmp_path):
    assert gate.main(["--manifest", str(tmp_path / "nope.json")]) == 0


def test_dormant_zero_claims(gate, tmp_path):
    assert gate.main(["--manifest", _write_manifest(tmp_path, [])]) == 0


# --- BROKEN ----------------------------------------------------------------

def test_broken_corrupt_json(gate, tmp_path):
    p = tmp_path / "m.json"
    p.write_text("{not json", encoding="utf-8")
    assert gate.main(["--manifest", str(p)]) == 2


def test_broken_claims_not_list(gate, tmp_path):
    p = tmp_path / "m.json"
    p.write_text(json.dumps({"claims": {}}), encoding="utf-8")
    assert gate.main(["--manifest", str(p)]) == 2


def test_broken_missing_keys(gate, tmp_path):
    c = _claim()
    del c["bound"]
    assert gate.main(["--manifest", _write_manifest(tmp_path, [c])]) == 2


def test_broken_duplicate_id(gate, tmp_path):
    c1, c2 = _claim(cid="X"), _claim(cid="X")
    assert gate.main(["--manifest",
                      _write_manifest(tmp_path, [c1, c2])]) == 2


def test_broken_claims_without_mechanism(tmp_path):
    # No fakes installed: the real tree has no drift_canary/ yet.
    _remove_fakes()
    mod = _load_gate()
    p = tmp_path / "m.json"
    p.write_text(json.dumps({"claims": [_claim()]}), encoding="utf-8")
    assert mod.main(["--manifest", str(p)]) == 2


def test_broken_unknown_verdict(gate, tmp_path):
    c = _claim(rounds=[{"round_seq": 1, "verdict": "maybe",
                        "adequate_service": True, "defects": []}])
    assert gate.main(["--manifest", _write_manifest(tmp_path, [c])]) == 2


def test_broken_unknown_defect_kind(gate, tmp_path):
    c = _claim(rounds=[{
        "round_seq": 1, "verdict": "undetermined",
        "adequate_service": False,
        "defects": [{"component": "APPLICABLE_OPPORTUNITY",
                     "kind": "VANISHED", "detail": "x"}]}])
    assert gate.main(["--manifest", _write_manifest(tmp_path, [c])]) == 2


def test_broken_unknown_component(gate, tmp_path):
    c = _claim(rounds=[{
        "round_seq": 1, "verdict": "undetermined",
        "adequate_service": False,
        "defects": [{"component": "NO_SUCH_PART",
                     "kind": "MISSING", "detail": "x"}]}])
    assert gate.main(["--manifest", _write_manifest(tmp_path, [c])]) == 2


def test_broken_undetermined_without_defects(gate, tmp_path):
    c = _claim(rounds=[{"round_seq": 1, "verdict": "undetermined",
                        "adequate_service": False, "defects": []}])
    assert gate.main(["--manifest", _write_manifest(tmp_path, [c])]) == 2


def test_broken_nonbool_adequate_service(gate, tmp_path):
    c = _claim(rounds=[{"round_seq": 1, "verdict": "eligible",
                        "adequate_service": "yes", "defects": []}])
    assert gate.main(["--manifest", _write_manifest(tmp_path, [c])]) == 2


def test_broken_bad_asserted_conclusion(gate, tmp_path):
    c = _claim(asserted="FINE")
    assert gate.main(["--manifest", _write_manifest(tmp_path, [c])]) == 2


def test_broken_engine_refuses(gate, tmp_path):
    # A missing interval past the finite cap is D61 territory: the engine
    # refuses, the gate fails closed (BROKEN), never passes, never
    # invents bounds.
    FakeEngine.script["ob"] = FakeMissingIntervalTooLongError("too long")
    c = _claim()
    assert gate.main(["--manifest", _write_manifest(tmp_path, [c])]) == 2


# --- PASS ------------------------------------------------------------------

def test_pass_certified(gate, tmp_path, capsys):
    FakeEngine.script["ob"] = _ok_receipt()
    c = _claim(asserted="NO_BREACH")
    assert gate.main(["--manifest", _write_manifest(tmp_path, [c])]) == 0
    out = capsys.readouterr().out
    assert "certified" in out


def test_pass_unresolved_certified(gate, tmp_path):
    FakeEngine.script["ob"] = _ok_receipt(verdict="UNRESOLVED",
                                          debt_min=1, debt_max=4)
    c = _claim(asserted="UNRESOLVED", bound=3)
    assert gate.main(["--manifest", _write_manifest(tmp_path, [c])]) == 0


# --- VIOLATION ---------------------------------------------------------------

def test_violation_proven_breach(gate, tmp_path, capsys):
    FakeEngine.script["ob"] = _ok_receipt(verdict="BREACH",
                                          debt_min=4, debt_max=5, bound=2)
    c = _claim(asserted="BREACH", bound=2)
    assert gate.main(["--manifest", _write_manifest(tmp_path, [c])]) == 1
    assert "proven BREACH" in capsys.readouterr().out


def test_violation_breach_laundering(gate, tmp_path, capsys):
    # Asserting NO_BREACH where the engine proves BREACH: blocked as a
    # proven breach (the BREACH check fires before the mismatch check).
    FakeEngine.script["ob"] = _ok_receipt(verdict="BREACH",
                                          debt_min=4, debt_max=5, bound=2)
    c = _claim(asserted="NO_BREACH", bound=2)
    assert gate.main(["--manifest", _write_manifest(tmp_path, [c])]) == 1
    assert "proven BREACH" in capsys.readouterr().out


def test_violation_unknown_laundering(gate, tmp_path, capsys):
    FakeEngine.script["ob"] = _ok_receipt(verdict="UNRESOLVED",
                                          debt_min=1, debt_max=4)
    c = _claim(asserted="NO_BREACH", bound=3)
    assert gate.main(["--manifest", _write_manifest(tmp_path, [c])]) == 1
    assert "unknown-laundering" in capsys.readouterr().out


def test_violation_false_breach(gate, tmp_path, capsys):
    FakeEngine.script["ob"] = _ok_receipt()
    c = _claim(asserted="BREACH")
    assert gate.main(["--manifest", _write_manifest(tmp_path, [c])]) == 1
    assert "false breach" in capsys.readouterr().out


def test_violation_manufactured_doubt(gate, tmp_path):
    FakeEngine.script["ob"] = _ok_receipt()
    c = _claim(asserted="UNRESOLVED")
    assert gate.main(["--manifest", _write_manifest(tmp_path, [c])]) == 1
