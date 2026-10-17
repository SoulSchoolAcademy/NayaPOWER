"""Tests for tools/d59_unresolved_evidence_gate.py.

Fake-mechanism injection: the D59 governor is not on this tree (PR #2313
unmerged), so tests inject a faithful fake of the mechanism's API surface
into sys.modules. The fire battery (not committed) judges the same gate
against the REAL #2313/#2311 bytes.
"""

import importlib.util
import json
import sys
import types
from pathlib import Path

import pytest

TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools"
GATE_PATH = TOOLS_DIR / "d59_unresolved_evidence_gate.py"

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


class FakeUnresolvedEvidenceError(Exception):
    pass


class FakeHistorySpaceTooLargeError(FakeUnresolvedEvidenceError):
    pass


class FakeDuplicateRoundError(FakeUnresolvedEvidenceError):
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


class FakeAssessment:
    def __init__(self, obligation_id, bound, verdict, debt_min, debt_max,
                 histories_examined, unresolved_rounds):
        self.obligation_id = obligation_id
        self.bound = bound
        self.verdict = verdict
        self.debt_min = debt_min
        self.debt_max = debt_max
        self.histories_examined = histories_examined
        self.unresolved_rounds = unresolved_rounds


class FakeGovernor:
    # obligation_id -> FakeAssessment or Exception to raise from assess()
    script = {}

    def __init__(self):
        self._rounds = {}

    def register_round(self, record):
        seqs = self._rounds.setdefault(record.obligation_id, {})
        if record.round_seq in seqs:
            raise FakeDuplicateRoundError("duplicate round")
        seqs[record.round_seq] = record

    def assess(self, obligation_id, contract):
        entry = FakeGovernor.script.get(obligation_id)
        if isinstance(entry, Exception):
            raise entry
        assert entry is not None, f"no script for {obligation_id}"
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
    mech = types.ModuleType("drift_canary.unresolved_evidence")
    mech.UnresolvedEvidenceGovernor = FakeGovernor
    mech.RoundRecord = FakeRoundRecord
    mech.ComponentDefect = FakeComponentDefect
    mech.DEFECT_KINDS = FAKE_DEFECT_KINDS
    mech.BREACH_VERDICTS = FAKE_BREACH_VERDICTS
    mech.VERDICTS = FAKE_VERDICTS
    mech.UnresolvedEvidenceError = FakeUnresolvedEvidenceError
    mech.HistorySpaceTooLargeError = FakeHistorySpaceTooLargeError
    eproof = types.ModuleType("drift_canary.eligibility_proof")
    eproof.COMPONENTS = FAKE_COMPONENTS
    fairness = types.ModuleType("drift_canary.fairness")
    fairness.FairnessContract = FakeFairnessContract
    sys.modules["drift_canary"] = pkg
    sys.modules["drift_canary.unresolved_evidence"] = mech
    sys.modules["drift_canary.eligibility_proof"] = eproof
    sys.modules["drift_canary.fairness"] = fairness


@pytest.fixture(autouse=True)
def _clean_modules():
    saved = {k: sys.modules.get(k) for k in (
        "drift_canary", "drift_canary.unresolved_evidence",
        "drift_canary.eligibility_proof", "drift_canary.fairness")}
    _install_fakes()
    FakeGovernor.script = {}
    yield
    for k, v in saved.items():
        if v is None:
            sys.modules.pop(k, None)
        else:
            sys.modules[k] = v
    FakeGovernor.script = {}


def _load_gate():
    spec = importlib.util.spec_from_file_location(
        "d59_unresolved_evidence_gate", GATE_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _write_manifest(tmp_path, claims):
    p = tmp_path / "manifest.json"
    p.write_text(json.dumps({"claims": claims}), encoding="utf-8")
    return str(p)


def _round(seq, verdict, adequate=True, defects=()):
    return {"round_seq": seq, "verdict": verdict,
            "adequate_service": adequate, "defects": list(defects)}


def _defect(component="AUTHORIZATION", kind="MISSING", detail="log absent"):
    return {"component": component, "kind": kind, "detail": detail}


def _claim(cid="UE-0001", asserted="NO_BREACH", rounds=None,
           reconstructions=None, bound=2):
    c = {"id": cid, "obligation_id": "obl-1", "bound": bound,
         "capacity_basis": "capacity audit 2026-10-11",
         "asserted_conclusion": asserted,
         "rounds": rounds if rounds is not None else [
             _round(1, "eligible"), _round(2, "eligible")]}
    if reconstructions is not None:
        c["reconstructions"] = reconstructions
    return c


def _script_no_breach(bound=2):
    return FakeAssessment("obl-1", bound, "NO_BREACH", 0, 1, 1, ())


# -- DORMANT ---------------------------------------------------------------

def test_dormant_manifest_absent(tmp_path):
    gate = _load_gate()
    assert gate.main(["--manifest", str(tmp_path / "nope.json")]) == 0


def test_dormant_zero_claims(tmp_path):
    gate = _load_gate()
    assert gate.main(["--manifest", _write_manifest(tmp_path, [])]) == 0


# -- BROKEN: manifest shape -------------------------------------------------

def test_broken_corrupt_json(tmp_path):
    gate = _load_gate()
    p = tmp_path / "m.json"
    p.write_text("{not json", encoding="utf-8")
    assert gate.main(["--manifest", str(p)]) == 2


def test_broken_claims_not_list(tmp_path):
    gate = _load_gate()
    p = tmp_path / "m.json"
    p.write_text(json.dumps({"claims": {}}), encoding="utf-8")
    assert gate.main(["--manifest", str(p)]) == 2


def test_broken_missing_keys(tmp_path):
    gate = _load_gate()
    assert gate.main(
        ["--manifest", _write_manifest(tmp_path, [{"id": "x"}])]) == 2


def test_broken_duplicate_id(tmp_path):
    gate = _load_gate()
    assert gate.main(["--manifest", _write_manifest(
        tmp_path, [_claim("UE-1"), _claim("UE-1")])]) == 2


# -- BROKEN: claims without the mechanism -----------------------------------

def test_broken_claims_without_mechanism(tmp_path):
    for k in ("drift_canary", "drift_canary.unresolved_evidence",
              "drift_canary.eligibility_proof", "drift_canary.fairness"):
        sys.modules.pop(k, None)
    gate = _load_gate()
    assert gate.main(
        ["--manifest", _write_manifest(tmp_path, [_claim()])]) == 2


# -- BROKEN: claim field validation ------------------------------------------

def test_broken_unknown_verdict(tmp_path):
    gate = _load_gate()
    assert gate.main(["--manifest", _write_manifest(
        tmp_path, [_claim(rounds=[_round(1, "maybe")])])]) == 2


def test_broken_unknown_defect_kind(tmp_path):
    gate = _load_gate()
    assert gate.main(["--manifest", _write_manifest(tmp_path, [_claim(
        rounds=[_round(1, "undetermined",
                       defects=[_defect(kind="VANISHED")])])])]) == 2


def test_broken_unknown_component(tmp_path):
    gate = _load_gate()
    assert gate.main(["--manifest", _write_manifest(tmp_path, [_claim(
        rounds=[_round(1, "undetermined",
                       defects=[_defect(component="VIBES")])])])]) == 2


def test_broken_undetermined_without_defects(tmp_path):
    gate = _load_gate()
    assert gate.main(["--manifest", _write_manifest(
        tmp_path, [_claim(rounds=[_round(1, "undetermined")])])]) == 2


def test_broken_nonbool_adequate_service(tmp_path):
    gate = _load_gate()
    assert gate.main(["--manifest", _write_manifest(
        tmp_path, [_claim(rounds=[_round(1, "eligible", adequate="yes")])])]) == 2


def test_broken_bad_asserted_conclusion(tmp_path):
    gate = _load_gate()
    assert gate.main(["--manifest", _write_manifest(
        tmp_path, [_claim(asserted="FINE")])]) == 2


def test_broken_governor_refuses_assessment(tmp_path):
    gate = _load_gate()
    FakeGovernor.script["obl-1"] = FakeHistorySpaceTooLargeError("too many")
    assert gate.main(
        ["--manifest", _write_manifest(tmp_path, [_claim()])]) == 2


# -- PASS -------------------------------------------------------------------

def test_pass_certified(tmp_path, capsys):
    gate = _load_gate()
    FakeGovernor.script["obl-1"] = _script_no_breach()
    rc = gate.main(["--manifest", _write_manifest(tmp_path, [_claim()])])
    assert rc == 0
    assert "certified" in capsys.readouterr().out


def test_pass_unresolved_with_open_reconstruction(tmp_path):
    gate = _load_gate()
    FakeGovernor.script["obl-1"] = FakeAssessment(
        "obl-1", 2, "UNRESOLVED", 1, 3, 4, (1,))
    claim = _claim(
        asserted="UNRESOLVED",
        rounds=[_round(1, "undetermined", adequate=False,
                       defects=[_defect()]),
                _round(2, "eligible", adequate=False)],
        reconstructions=[{"round_seq": 1, "status": "open",
                          "reason": "re-fetch scheduled"}])
    assert gate.main(["--manifest", _write_manifest(tmp_path, [claim])]) == 0


def test_pass_unresolved_with_escalated_reconstruction(tmp_path):
    gate = _load_gate()
    FakeGovernor.script["obl-1"] = FakeAssessment(
        "obl-1", 2, "UNRESOLVED", 1, 3, 4, (1,))
    claim = _claim(
        asserted="UNRESOLVED",
        rounds=[_round(1, "undetermined", adequate=False,
                       defects=[_defect()]),
                _round(2, "eligible", adequate=False)],
        reconstructions=[{"round_seq": 1, "status": "escalated",
                          "reason": "budget exhausted after 3 attempts"}])
    assert gate.main(["--manifest", _write_manifest(tmp_path, [claim])]) == 0


# -- VIOLATION ----------------------------------------------------------------

def test_violation_proven_breach(tmp_path, capsys):
    gate = _load_gate()
    FakeGovernor.script["obl-1"] = FakeAssessment(
        "obl-1", 2, "BREACH", 3, 4, 1, ())
    rc = gate.main(["--manifest", _write_manifest(
        tmp_path, [_claim(asserted="BREACH")])])
    assert rc == 1
    assert "BREACH" in capsys.readouterr().out


def test_violation_unknown_laundering(tmp_path, capsys):
    gate = _load_gate()
    FakeGovernor.script["obl-1"] = FakeAssessment(
        "obl-1", 2, "UNRESOLVED", 2, 3, 2, (1,))
    claim = _claim(
        asserted="NO_BREACH",
        rounds=[_round(1, "undetermined", adequate=False,
                       defects=[_defect()]),
                _round(2, "eligible", adequate=False),
                _round(3, "eligible", adequate=False)],
        reconstructions=[{"round_seq": 1, "status": "open"}])
    rc = gate.main(["--manifest", _write_manifest(tmp_path, [claim])])
    assert rc == 1
    assert "unknown-laundering" in capsys.readouterr().out


def test_violation_missing_reconstruction_coverage(tmp_path, capsys):
    gate = _load_gate()
    FakeGovernor.script["obl-1"] = FakeAssessment(
        "obl-1", 2, "UNRESOLVED", 1, 3, 4, (1, 2))
    claim = _claim(
        asserted="UNRESOLVED",
        rounds=[_round(1, "undetermined", adequate=False,
                       defects=[_defect()]),
                _round(2, "undetermined", adequate=False,
                       defects=[_defect(kind="STALE")])],
        reconstructions=[{"round_seq": 1, "status": "open"}])
    rc = gate.main(["--manifest", _write_manifest(tmp_path, [claim])])
    assert rc == 1
    assert "ungoverned hole" in capsys.readouterr().out


def test_violation_false_breach(tmp_path, capsys):
    gate = _load_gate()
    FakeGovernor.script["obl-1"] = _script_no_breach()
    rc = gate.main(["--manifest", _write_manifest(
        tmp_path, [_claim(asserted="BREACH")])])
    assert rc == 1
    assert "false breach" in capsys.readouterr().out
