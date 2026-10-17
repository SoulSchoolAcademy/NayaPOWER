"""Tests: D56 bounded-liveness claims gate (tools/bounded_liveness_gate.py).

The gate must be honest on EVERY tree, including ones where the D56 prover
module does not exist yet. These tests inject fake mechanisms so the gate's
own logic — strict parsing, dormant/active transitions, fail-closed refusals,
fraud-pattern naming, exit codes — is proven deterministically on main. Real-
module integration (gate + the real tools/bounded_recovery_liveness.py) is
proven by the wire lane's fire battery on the combined tree (see the PR
body). A sabotaged gate must fail its own suite.
"""
import io
import json
import sys
import types
from contextlib import redirect_stdout
from pathlib import Path

import pytest

TOOLS_DIR = str(Path(__file__).resolve().parent.parent / "tools")
sys.path.insert(0, TOOLS_DIR)

import bounded_liveness_gate as gate


# ---------------------------------------------------------------------------
# Fake D56 mechanism: same API shape as tools/bounded_recovery_liveness.py,
# canned verdicts. Stands in for the prover's decisions; the gate's
# comparison, strictness, and exit-code logic is what's under test here.
# ---------------------------------------------------------------------------

class _FakeVerdict:
    def __init__(self, safety="holds", scheduling_fairness="holds",
                 bounded_progress="not_applicable",
                 task_completion="unproven", bound_enforceable=True,
                 eligible_time=5, wall_time=5, detail="fake"):
        self.safety = safety
        self.scheduling_fairness = scheduling_fairness
        self.bounded_progress = bounded_progress
        self.task_completion = task_completion
        self.bound_enforceable = bound_enforceable
        self.eligible_time = eligible_time
        self.wall_time = wall_time
        self.detail = detail


def _simple_cls(name, fields):
    def __init__(self, **kwargs):
        for f in fields:
            setattr(self, f, kwargs.get(f))

    return type(name, (), {"__init__": __init__})


def make_fake_mech(verdict=None, **verdict_kwargs):
    canned = verdict if verdict is not None else _FakeVerdict(**verdict_kwargs)
    mod = types.ModuleType("fake_d56")
    mod.CLAIM_STATES = ("holds", "violated", "unproven", "not_applicable")
    mod.SEGMENT_STATES = ("eligible", "waiting_authority", "safety_hold",
                          "outage_verified", "dispositioned")
    mod.PRECONDITIONS = ("eligibility", "opportunities", "usable_service",
                         "progress_witnesses", "capacity_assumptions",
                         "governing_bound")
    mod.BOUND_KINDS = ("service", "progress", "disposition")
    mod.SERVICE_LADDER = ("SELECTED", "DISPATCHED", "SERVICED", "ATTEMPTED",
                          "ADVANCED", "COMPLETED")
    mod.SERVICE_EVIDENCE_FIELDS = ("lease_id", "worker_ack",
                                   "resources_available")
    mod.NON_PROGRESS_EVENTS = ("heartbeat", "log_line", "status_rewrite",
                               "retry_attempt")
    mod.ObligationHistory = _simple_cls("ObligationHistory",
                                        ("obligation", "segments",
                                         "service_observations",
                                         "progress_marks", "disposition",
                                         "disposition_evidence"))
    mod.EligibilitySegment = _simple_cls("EligibilitySegment",
                                         ("state", "start", "end"))
    mod.ServiceObservation = _simple_cls("ServiceObservation",
                                         ("seq", "rung", "evidence"))
    mod.ProgressMark = _simple_cls("ProgressMark",
                                    ("seq", "kind", "state_advance",
                                     "moves_toward_outcome"))
    mod.Precondition = _simple_cls("Precondition",
                                    ("name", "established", "evidence"))
    mod.Assumption = _simple_cls("Assumption",
                                  ("statement", "proven", "proof_ref"))
    mod.Bound = _simple_cls("Bound",
                             ("kind", "limit", "assumptions", "evidence",
                              "label"))
    mod.assess = lambda history, bound, preconditions: canned
    return mod


@pytest.fixture()
def fake_mech(monkeypatch):
    def install(verdict=None, **kwargs):
        mech = make_fake_mech(verdict=verdict, **kwargs)
        monkeypatch.setattr(gate, "_load_mechanism", lambda: mech)
        return mech

    return install


# ---------------------------------------------------------------------------
# Claim builders — one fully valid claim; tests mutate from there.
# ---------------------------------------------------------------------------

def _valid_claim(**overrides):
    claim = {
        "id": "BL-0001",
        "claimant": "test",
        "evidence_ref": "test",
        "claimed": {
            "safety": "holds",
            "scheduling_fairness": "holds",
            "bounded_progress": "not_applicable",
            "task_completion": "unproven",
        },
        "obligation": {
            "name": "test obligation",
            "segments": [{"state": "eligible", "start": 0, "end": 5}],
            "service_observations": [
                {"seq": 1, "rung": "SERVICED",
                 "evidence": {"lease_id": "L1", "worker_ack": "A1",
                              "resources_available": "yes"}}
            ],
            "progress_marks": [],
        },
        "bound": {
            "kind": "service",
            "limit": 10,
            "assumptions": [{"statement": "capacity adequate",
                             "proven": True, "proof_ref": "audit"}],
            "evidence": "runbook",
        },
        "preconditions": [
            {"name": n, "established": True, "evidence": "e"}
            for n in ("eligibility", "opportunities", "usable_service",
                      "progress_witnesses", "capacity_assumptions",
                      "governing_bound")
        ],
    }
    for key, value in overrides.items():
        claim[key] = value
    return claim


def _write_manifest(tmp_path, claims):
    p = tmp_path / "manifest.json"
    p.write_text(json.dumps({"claims": claims}), encoding="utf-8")
    return str(p)


def _run_gate(manifest_path):
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = gate.main(["--manifest", manifest_path, "--json"])
    return code, json.loads(buf.getvalue())


# ---------------------------------------------------------------------------
# DORMANT — explicit, never a false green.
# ---------------------------------------------------------------------------

def test_dormant_empty_claims(tmp_path, fake_mech):
    fake_mech()
    code, payload = _run_gate(_write_manifest(tmp_path, []))
    assert code == 0
    assert payload["verdict"] == "DORMANT"


def test_dormant_absent_manifest(tmp_path, fake_mech):
    fake_mech()
    code, payload = _run_gate(str(tmp_path / "no-such-file.json"))
    assert code == 0
    assert payload["verdict"] == "DORMANT"


# ---------------------------------------------------------------------------
# PASS — a true claim is certified.
# ---------------------------------------------------------------------------

def test_pass_certified_claim(tmp_path, fake_mech):
    fake_mech()  # canned verdict matches _valid_claim's declared verdicts
    code, payload = _run_gate(_write_manifest(tmp_path, [_valid_claim()]))
    assert code == 0
    assert payload["verdict"] == "PASS"
    assert payload["claims"][0]["verdict"] == "certified"


# ---------------------------------------------------------------------------
# VIOLATION — mismatches block, with the defect class named.
# ---------------------------------------------------------------------------

def test_violation_mismatch_blocks(tmp_path, fake_mech):
    fake_mech(scheduling_fairness="violated")  # claim says holds
    code, payload = _run_gate(_write_manifest(tmp_path, [_valid_claim()]))
    assert code == 1
    assert payload["verdict"] == "VIOLATION"
    result = payload["claims"][0]
    assert result["verdict"] == "violation"
    assert "scheduling_fairness" in result["reason"]


def test_violation_timeout_as_fairness_fraud_named(tmp_path, fake_mech):
    fake_mech(_FakeVerdict(scheduling_fairness="not_applicable",
                           eligible_time=0, wall_time=30))
    claim = _valid_claim()
    claim["claimed"]["scheduling_fairness"] = "violated"
    claim["obligation"]["segments"] = [
        {"state": "safety_hold", "start": 0, "end": 30}]
    code, payload = _run_gate(_write_manifest(tmp_path, [claim]))
    assert code == 1
    assert "timeout-as-fairness fraud" in payload["claims"][0]["reason"]


def test_violation_unproven_asserted_as_decided(tmp_path, fake_mech):
    fake_mech(_FakeVerdict(safety="unproven", scheduling_fairness="unproven",
                           bounded_progress="unproven",
                           task_completion="unproven",
                           bound_enforceable=False))
    code, payload = _run_gate(_write_manifest(tmp_path, [_valid_claim()]))
    assert code == 1
    assert "unproven asserted as decided" in payload["claims"][0]["reason"]


# ---------------------------------------------------------------------------
# BROKEN — fail-closed on untrustworthy inputs. Never defaulted.
# ---------------------------------------------------------------------------

def test_broken_corrupt_manifest(tmp_path, fake_mech):
    fake_mech()
    p = tmp_path / "manifest.json"
    p.write_text("{not json", encoding="utf-8")
    code, payload = _run_gate(str(p))
    assert code == 2
    assert payload["verdict"] == "BROKEN"


@pytest.mark.parametrize("mutate", [
    lambda c: c["obligation"]["segments"].__setitem__(
        0, {"state": "napping", "start": 0, "end": 5}),
    lambda c: c["obligation"].__setitem__(
        "service_observations",
        [{"seq": 1, "rung": "TELEPORTED", "evidence": {}}]),
    lambda c: c["claimed"].__setitem__("safety", "maybe"),
    lambda c: c["claimed"].pop("task_completion"),
    lambda c: c["preconditions"].__setitem__(
        0, {"name": "vibes", "established": True}),
    lambda c: c["bound"].__setitem__("kind", "eventually"),
    lambda c: c["bound"].__setitem__("limit", 0),
    lambda c: c["obligation"]["segments"].__setitem__(
        0, {"state": "eligible", "start": 5, "end": 5}),
])
def test_broken_never_invents_fields(tmp_path, fake_mech, mutate):
    """Unknown states, rungs, slots, names, kinds, limits — all BROKEN."""
    fake_mech()
    claim = _valid_claim()
    mutate(claim)
    code, payload = _run_gate(_write_manifest(tmp_path, [claim]))
    assert code == 2, payload
    assert payload["verdict"] == "BROKEN"


def test_broken_duplicate_ids(tmp_path, fake_mech):
    fake_mech()
    code, payload = _run_gate(
        _write_manifest(tmp_path, [_valid_claim(), _valid_claim()]))
    assert code == 2
    assert payload["verdict"] == "BROKEN"


def test_broken_missing_required_keys(tmp_path, fake_mech):
    fake_mech()
    claim = _valid_claim()
    del claim["bound"]
    code, payload = _run_gate(_write_manifest(tmp_path, [claim]))
    assert code == 2
    assert payload["verdict"] == "BROKEN"


def test_broken_claims_without_mechanism(tmp_path, monkeypatch):
    def missing():
        raise gate.MechanismMissing("mechanism not present: nope.py")

    monkeypatch.setattr(gate, "_load_mechanism", missing)
    code, payload = _run_gate(_write_manifest(tmp_path, [_valid_claim()]))
    assert code == 2
    assert payload["verdict"] == "BROKEN"
    assert "refusing to pass on defaults" in payload["reason"]


def test_broken_neutered_mechanism_rejected(tmp_path, monkeypatch):
    """A module missing the assess API cannot pass as the mechanism."""
    neutered = tmp_path / "bounded_recovery_liveness.py"
    neutered.write_text("X = 1\n", encoding="utf-8")
    monkeypatch.setattr(gate, "MECHANISM_FILE", neutered)
    with pytest.raises(gate.MechanismMissing):
        gate._load_mechanism()
