"""Tests: D28 assumption-audit gate (tools/fairness_assumption_audit_gate.py).

The gate must be honest on EVERY tree, including ones where the D28 audit
module and the D27 registry do not exist yet. These tests inject fake
modules into sys.modules so the gate's own logic — dormant/active
transitions, fail-closed refusals, exit codes — is proven deterministically
on main. Real-module integration is proven by the wire lane's fire battery
on the combined #2306+#2295 tree (see the WIRE-RECEIPT).

Every negative test carries a positive control. No theater: a sabotaged
gate must fail its own suite.
"""
import io
import json
import os
import sys
import tempfile
import types
from contextlib import redirect_stdout

import pytest

GATE_PATH = os.path.join(os.path.dirname(__file__), "..", "tools",
                         "fairness_assumption_audit_gate.py")


def load_gate():
    import importlib.util
    spec = importlib.util.spec_from_file_location("audit_gate", GATE_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture()
def gate():
    return load_gate()


class FakeVerdict:
    def __init__(self, kind, failed_gate="", reason="", model_depth=12):
        self.kind = kind
        self.failed_gate = failed_gate
        self.reason = reason
        self.model_depth = model_depth


class FakeLedger:
    def __init__(self):
        self.names = set()

    def record(self, rec):
        if rec.name in self.names:
            raise ValueError(f"duplicate evidence record {rec.name}")
        self.names.add(rec.name)


class FakeEvidenceRecord:
    def __init__(self, name, produced_by, produced_at="", summary=""):
        self.name = name
        self.produced_by = produced_by


class FakeClaim:
    def __init__(self, **kw):
        self.__dict__.update(kw)


def make_fake_audit(verdicts=(), calls=None, bind_raises=False):
    """Build a fake drift_canary.fairness_audit module.

    verdicts: iterable of FakeVerdict, one per audit_assumption_set call.
    calls: list the fake appends ("audit",) to, proving the gate called it.
    bind_raises: from_d27 raises on every call (refusal contract).
    """
    mod = types.ModuleType("drift_canary.fairness_audit")
    mod.AUDIT_OWNERS = ("ENVIRONMENT", "WORKER", "HUMAN_AUTHORITY")
    mod._INPUT_OWNERS = mod.AUDIT_OWNERS + ("SCHEDULER",)

    class AuditInputError(Exception):
        pass

    mod.AuditInputError = AuditInputError
    mod.EvidenceLedger = FakeLedger
    mod.EvidenceRecord = FakeEvidenceRecord
    mod.QualificationClaim = FakeClaim

    def from_d27(assumption, *, owner, status, justification,
                 justification_evidence, model_constraint="NONE",
                 in_qualification_scope=True):
        if bind_raises:
            raise AuditInputError("refused")
        if not owner or not status or not justification or not justification_evidence:
            raise AuditInputError("refuses to invent justification fields")
        return (assumption.id, owner)

    mod.from_d27 = from_d27
    verdict_iter = iter(verdicts)

    def audit_assumption_set(bound, claim, ledger, model_depth=12):
        if calls is not None:
            calls.append("audit")
        return next(verdict_iter)

    mod.audit_assumption_set = audit_assumption_set
    return mod


class FakeAssumption:
    def __init__(self, aid, statement="stmt"):
        self.id = aid
        self.statement = statement


def install_fakes(monkeypatch, fake_audit, registry_ids=("FA-A1", "FA-A2")):
    pkg = types.ModuleType("drift_canary")
    pkg.fairness_audit = fake_audit
    monkeypatch.setitem(sys.modules, "drift_canary", pkg)
    monkeypatch.setitem(sys.modules, "drift_canary.fairness_audit", fake_audit)
    reg = types.ModuleType("fairness_assumptions")
    reg.ASSUMPTIONS = {i: FakeAssumption(i) for i in registry_ids}
    monkeypatch.setitem(sys.modules, "fairness_assumptions", reg)


def write_manifest(tmp_path, obj):
    p = tmp_path / "manifest.json"
    p.write_text(json.dumps(obj))
    return str(p)


def run(gate, path):
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = gate.run_gate(path)
    return code, buf.getvalue()


def full_entry(audit_id="A1", aids=("FA-A1",)):
    return {
        "audit_id": audit_id,
        "assumption_ids": list(aids),
        "owner": "ENVIRONMENT",
        "status": "JUSTIFIED",
        "justification": "ops runbook",
        "justification_evidence": [
            {"name": "runbook-7", "produced_by": "ops-team",
             "produced_at": "2026-10-01", "summary": "tasks stabilize"}
        ],
        "model_constraint": "NONE",
        "in_qualification_scope": False,
        "claim": {
            "claim_id": "Q-1",
            "property_claimed": "WEAK_FAIRNESS",
            "scheduler_id": "sched-main",
            "qualification_artifact": "receipt-xyz",
            "prover_policy": "WEAK",
            "excluded_behaviors": [],
        },
        "model_depth": 12,
    }


# ---------------------------------------------------------------------------
# Dormant states: exit 0, never claims "audited".
# ---------------------------------------------------------------------------

def test_dormant_no_manifest_file(gate, tmp_path):
    code, out = run(gate, str(tmp_path / "missing.json"))
    assert code == 0
    assert "DORMANT" in out and "no audit manifest" in out


def test_dormant_mechanism_absent(gate, tmp_path, monkeypatch):
    # Nothing injected: on main neither module exists.
    for m in ("drift_canary", "drift_canary.fairness_audit",
              "fairness_assumptions", "tools.fairness_assumptions"):
        monkeypatch.delitem(sys.modules, m, raising=False)
    p = write_manifest(tmp_path, {"audits": []})
    code, out = run(gate, p)
    assert code == 0
    assert "DORMANT" in out and "mechanism not present" in out


def test_dormant_empty_audits(gate, tmp_path, monkeypatch):
    install_fakes(monkeypatch, make_fake_audit())
    p = write_manifest(tmp_path, {"audits": [], "version": 1})
    code, out = run(gate, p)
    assert code == 0
    assert "DORMANT" in out and "0 audits registered" in out


# ---------------------------------------------------------------------------
# Active states.
# ---------------------------------------------------------------------------

def test_pass_when_audit_passes(gate, tmp_path, monkeypatch):
    calls = []
    install_fakes(monkeypatch,
                  make_fake_audit([FakeVerdict("AUDIT_PASSED")], calls=calls))
    p = write_manifest(tmp_path, {"audits": [full_entry()]})
    code, out = run(gate, p)
    assert code == 0
    assert calls == ["audit"], "the gate must actually call the audit"
    assert "PASS" in out and "A1" in out


def test_violation_rejected_blocks(gate, tmp_path, monkeypatch):
    install_fakes(monkeypatch, make_fake_audit(
        [FakeVerdict("REJECTED", failed_gate="G4_NON_CIRCULARITY",
                     reason="the test was rigged")]))
    p = write_manifest(tmp_path, {"audits": [full_entry()]})
    code, out = run(gate, p)
    assert code == 1
    assert "VIOLATION" in out and "G4_NON_CIRCULARITY" in out


def test_violation_redundant_blocks(gate, tmp_path, monkeypatch):
    install_fakes(monkeypatch, make_fake_audit(
        [FakeVerdict("REDUNDANT_ASSUMPTIONS", failed_gate="G3_MINIMAL_SUFFICIENCY",
                     reason="decorative")]))
    p = write_manifest(tmp_path, {"audits": [full_entry()]})
    code, out = run(gate, p)
    assert code == 1
    assert "VIOLATION" in out


def test_violation_missing_justification_refuses_to_invent(
        gate, tmp_path, monkeypatch):
    install_fakes(monkeypatch, make_fake_audit([FakeVerdict("AUDIT_PASSED")]))
    entry = full_entry()
    del entry["justification"]
    p = write_manifest(tmp_path, {"audits": [entry]})
    code, out = run(gate, p)
    assert code == 1
    assert "refuses to invent" in out


def test_violation_unknown_assumption_id(gate, tmp_path, monkeypatch):
    install_fakes(monkeypatch, make_fake_audit([FakeVerdict("AUDIT_PASSED")]))
    p = write_manifest(tmp_path, {"audits": [full_entry(aids=("FA-NOPE",))]})
    code, out = run(gate, p)
    assert code == 1
    assert "unknown to the D27 registry" in out


def test_violation_bind_refusal_blocks(gate, tmp_path, monkeypatch):
    install_fakes(monkeypatch, make_fake_audit(bind_raises=True))
    p = write_manifest(tmp_path, {"audits": [full_entry()]})
    code, out = run(gate, p)
    assert code == 1
    assert "binding refused" in out


def test_violation_duplicate_evidence_names(gate, tmp_path, monkeypatch):
    install_fakes(monkeypatch, make_fake_audit([FakeVerdict("AUDIT_PASSED")]))
    entry = full_entry()
    entry["justification_evidence"] = [
        {"name": "dup", "produced_by": "a"},
        {"name": "dup", "produced_by": "b"},
    ]
    p = write_manifest(tmp_path, {"audits": [entry]})
    code, out = run(gate, p)
    assert code == 1
    assert "ledger rejected evidence" in out


# ---------------------------------------------------------------------------
# Broken gate: fail-closed, never a silent pass.
# ---------------------------------------------------------------------------

def test_broken_corrupt_manifest_json(gate, tmp_path):
    p = tmp_path / "manifest.json"
    p.write_text("{not json")
    code, out = run(gate, str(p))
    assert code == 2
    assert "BROKEN" in out


def test_broken_manifest_wrong_shape(gate, tmp_path):
    p = write_manifest(tmp_path, {"audits": "not-a-list"})
    code, out = run(gate, p)
    assert code == 2
    assert "BROKEN" in out


# ---------------------------------------------------------------------------
# Negative control: a gate that blindly passes must fail this suite.
# (Modeled by asserting the spy: no audit call is observable here, so a
#  pass without a call is impossible by construction — test_pass asserts
#  calls == ["audit"].)
# ---------------------------------------------------------------------------

def test_second_audit_also_runs(gate, tmp_path, monkeypatch):
    calls = []
    install_fakes(monkeypatch, make_fake_audit(
        [FakeVerdict("AUDIT_PASSED"), FakeVerdict("AUDIT_PASSED")], calls=calls))
    p = write_manifest(tmp_path, {"audits": [full_entry("A1"), full_entry("A2")]})
    code, out = run(gate, p)
    assert code == 0
    assert calls == ["audit", "audit"]
    assert "all 2 registered audits passed" in out


def test_first_failure_stops_the_run(gate, tmp_path, monkeypatch):
    calls = []
    install_fakes(monkeypatch, make_fake_audit(
        [FakeVerdict("REJECTED", failed_gate="G1_INDEPENDENT_JUSTIFICATION",
                     reason="x"),
         FakeVerdict("AUDIT_PASSED")], calls=calls))
    p = write_manifest(tmp_path, {"audits": [full_entry("A1"), full_entry("A2")]})
    code, out = run(gate, p)
    assert code == 1
    assert calls == ["audit"], "fail-closed: first failure ends the run"
