"""Tests: D55 claims gate (tools/safety_liveness_gate.py).

The gate must be honest on EVERY tree, including ones where the D55
classifier module does not exist yet. These tests inject fake mechanisms so
the gate's own logic — strict parsing, dormant/active transitions,
fail-closed refusals, fraud-pattern naming, exit codes — is proven
deterministically on main. Real-module integration (gate + the real
tools/safety_liveness_classifier.py) is proven by the wire lane's fire
battery on the combined tip+#2302 tree (see the WIRE-RECEIPT).

Every negative test carries a positive control. A sabotaged gate must fail
its own suite.
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

import safety_liveness_gate as gate


# ---------------------------------------------------------------------------
# Fake D55 mechanism: same API shape as tools/safety_liveness_classifier.py,
# canned verdicts. Stands in for the classifier's decisions; the gate's
# comparison, strictness, and exit-code logic is what's under test here.
# ---------------------------------------------------------------------------

class _FakeClassification:
    def __init__(self, value):
        self.value = value


class _FakeTriFact:
    def __init__(self, enabled, serviced, progressed):
        self.enabled = enabled
        self.serviced = serviced
        self.progressed = progressed


class _FakeDiagnosis:
    def __init__(self, verdict, tri_fact, note="", scheduler_defect=False):
        self.classification = _FakeClassification(verdict)
        self.tri_fact = _FakeTriFact(*tri_fact)
        self.note = note
        self.scheduler_defect = scheduler_defect


class _FakeAuthState:
    VALID = {"withdrawn", "granted", "missing_decision"}

    def __call__(self, value):
        if value not in self.VALID:
            raise ValueError(f"unknown auth state: {value!r}")
        return value


class _FakeEvent:
    def __init__(self, kind, detail=""):
        self.kind = kind
        self.detail = detail


class _FakeObligation:
    def __init__(self, name, auth, events=(), reconciliation=None):
        self.name = name
        self.auth = auth
        self.events = list(events)
        self.reconciliation = reconciliation


class _FakeDisposition:
    def __init__(self, disposition="", evidence="", reason=""):
        self._valid = bool(evidence.strip() or reason.strip())

    def is_valid(self):
        return self._valid


def make_fake_mech(verdict="healthy", tri_fact=(True, True, True), note="",
                   scheduler_defect=False):
    mod = types.ModuleType("fake_d55")
    mod.SERVICE = "service"
    mod.PROGRESS = "progress"
    mod.AuthState = _FakeAuthState()
    mod.Event = _FakeEvent
    mod.Obligation = _FakeObligation
    mod.ValidDisposition = _FakeDisposition
    mod.classify = lambda ob: _FakeDiagnosis(verdict, tri_fact, note,
                                             scheduler_defect)
    return mod


@pytest.fixture()
def fake_mech(monkeypatch):
    holder = {}

    def install(**kwargs):
        mech = make_fake_mech(**kwargs)
        holder["mech"] = mech
        monkeypatch.setattr(gate, "_load_mechanism", lambda: mech)
        return mech

    return install


def write_manifest(tmp_path, claims):
    p = tmp_path / "recovery_claims_manifest.json"
    p.write_text(json.dumps({"claims": claims}))
    return str(p)


def make_claim(cid, claimed, auth="granted", events=(), **extra):
    claim = {
        "id": cid,
        "claimant": "test",
        "claimed_classification": claimed,
        "obligation": {
            "name": cid,
            "auth": auth,
            "events": [{"kind": k, "detail": d} for k, d in events],
        },
    }
    claim.update(extra)
    return claim


def service_events(n):
    return [("service", f"heartbeat {i}") for i in range(n)]


# ---------------------------------------------------------------------------
# DORMANT paths — explicit, never a false green
# ---------------------------------------------------------------------------

def test_empty_manifest_is_dormant_not_green(tmp_path, fake_mech, capsys):
    fake_mech()
    code = gate.main(["--manifest", write_manifest(tmp_path, []),
                      "--json"])
    out = json.loads(capsys.readouterr().out)
    assert code == 0
    assert out["verdict"] == "DORMANT"
    assert "zero claims" in out["reason"]


def test_missing_manifest_file_is_dormant(tmp_path, fake_mech, capsys):
    fake_mech()
    code = gate.main(["--manifest", str(tmp_path / "nope.json"), "--json"])
    out = json.loads(capsys.readouterr().out)
    assert code == 0
    assert out["verdict"] == "DORMANT"


# ---------------------------------------------------------------------------
# Violation paths — the gate blocks real fraud shapes
# ---------------------------------------------------------------------------

def test_heartbeat_fraud_blocked(tmp_path, fake_mech, capsys):
    fake_mech(verdict="recovery_defect", tri_fact=(True, True, False))
    claim = make_claim("RC-HB", "healthy", events=service_events(100))
    code = gate.main(["--manifest", write_manifest(tmp_path, [claim]),
                      "--json"])
    out = json.loads(capsys.readouterr().out)
    assert code == 1
    assert out["verdict"] == "VIOLATION"
    assert out["claims"][0]["actual"] == "recovery_defect"
    assert "heartbeat fraud" in out["claims"][0]["reason"]


def test_liveness_fraud_on_legitimate_hold_blocked(tmp_path, fake_mech,
                                                   capsys):
    fake_mech(verdict="valid_hold", tri_fact=(False, False, False),
              note="authorization withdrawn; hold is valid")
    claim = make_claim("RC-LF", "recovery_defect", auth="withdrawn")
    code = gate.main(["--manifest", write_manifest(tmp_path, [claim]),
                      "--json"])
    out = json.loads(capsys.readouterr().out)
    assert code == 1
    assert out["verdict"] == "VIOLATION"
    assert "liveness fraud" in out["claims"][0]["reason"]


def test_disposition_without_evidence_or_reason_blocked(tmp_path, fake_mech,
                                                        capsys):
    fake_mech(verdict="healthy")
    claim = make_claim("RC-DX", "healthy", events=[("progress", "moved")],
                       disposition={"disposition": "closed"})
    code = gate.main(["--manifest", write_manifest(tmp_path, [claim]),
                      "--json"])
    out = json.loads(capsys.readouterr().out)
    assert code == 1
    assert out["claims"][0]["verdict"] == "violation"
    assert out["claims"][0]["disposition_valid"] is False


# ---------------------------------------------------------------------------
# Positive controls — true claims certify
# ---------------------------------------------------------------------------

def test_legit_healthy_claim_certified(tmp_path, fake_mech, capsys):
    fake_mech(verdict="healthy", tri_fact=(True, True, True))
    claim = make_claim("RC-OK", "healthy", events=[("progress", "moved")])
    code = gate.main(["--manifest", write_manifest(tmp_path, [claim]),
                      "--json"])
    out = json.loads(capsys.readouterr().out)
    assert code == 0
    assert out["verdict"] == "PASS"
    assert out["claims"][0]["verdict"] == "certified"


def test_legit_valid_hold_certified(tmp_path, fake_mech, capsys):
    fake_mech(verdict="valid_hold", tri_fact=(False, False, False))
    claim = make_claim("RC-HOLD", "valid_hold", auth="withdrawn")
    code = gate.main(["--manifest", write_manifest(tmp_path, [claim]),
                      "--json"])
    out = json.loads(capsys.readouterr().out)
    assert code == 0
    assert out["verdict"] == "PASS"


def test_disposition_with_reason_certified(tmp_path, fake_mech, capsys):
    fake_mech(verdict="waiting_authority", tri_fact=(False, False, False))
    claim = make_claim("RC-WA", "waiting_authority", auth="missing_decision",
                       disposition={"disposition": "parked",
                                    "reason": "awaiting LAW decision 6102257048"})
    code = gate.main(["--manifest", write_manifest(tmp_path, [claim]),
                      "--json"])
    out = json.loads(capsys.readouterr().out)
    assert code == 0
    assert out["claims"][0]["disposition_valid"] is True


def test_scheduler_defect_attention_surfaced_not_blocked(tmp_path, fake_mech,
                                                         capsys):
    fake_mech(verdict="valid_hold", tri_fact=(False, True, False),
              scheduler_defect=True)
    claim = make_claim("RC-SD", "valid_hold", auth="withdrawn",
                       events=service_events(3))
    code = gate.main(["--manifest", write_manifest(tmp_path, [claim]),
                      "--json"])
    out = json.loads(capsys.readouterr().out)
    assert code == 0
    assert out["verdict"] == "PASS"
    assert "scheduler_defect" in out["claims"][0]["attention"]


# ---------------------------------------------------------------------------
# Fail-closed paths — corrupt or unparseable inputs are BROKEN, never passed
# ---------------------------------------------------------------------------

def test_corrupt_manifest_json_is_broken(tmp_path, fake_mech, capsys):
    fake_mech()
    p = tmp_path / "m.json"
    p.write_text("{not json")
    code = gate.main(["--manifest", str(p), "--json"])
    out = json.loads(capsys.readouterr().out)
    assert code == 2
    assert out["verdict"] == "BROKEN"


def test_wrong_manifest_shape_is_broken(tmp_path, fake_mech, capsys):
    fake_mech()
    p = tmp_path / "m.json"
    p.write_text(json.dumps({"claims": {"not": "a list"}}))
    code = gate.main(["--manifest", str(p), "--json"])
    assert code == 2
    assert json.loads(capsys.readouterr().out)["verdict"] == "BROKEN"


def test_duplicate_claim_ids_are_broken(tmp_path, fake_mech, capsys):
    fake_mech()
    c = make_claim("RC-DUP", "healthy")
    code = gate.main(["--manifest", write_manifest(tmp_path, [c, c]),
                      "--json"])
    assert code == 2
    assert json.loads(capsys.readouterr().out)["verdict"] == "BROKEN"


def test_unknown_auth_state_is_broken_never_defaulted(tmp_path, fake_mech,
                                                      capsys):
    fake_mech(verdict="healthy")
    claim = make_claim("RC-UA", "healthy", auth="maybe")
    code = gate.main(["--manifest", write_manifest(tmp_path, [claim]),
                      "--json"])
    assert code == 2
    assert json.loads(capsys.readouterr().out)["verdict"] == "BROKEN"


def test_unknown_event_kind_is_broken(tmp_path, fake_mech, capsys):
    fake_mech(verdict="healthy")
    claim = make_claim("RC-UE", "healthy", events=[("vibes", "x")])
    code = gate.main(["--manifest", write_manifest(tmp_path, [claim]),
                      "--json"])
    assert code == 2
    assert json.loads(capsys.readouterr().out)["verdict"] == "BROKEN"


def test_unknown_claimed_classification_is_broken(tmp_path, fake_mech,
                                                  capsys):
    fake_mech(verdict="healthy")
    claim = make_claim("RC-UC", "probably_fine")
    code = gate.main(["--manifest", write_manifest(tmp_path, [claim]),
                      "--json"])
    assert code == 2
    assert json.loads(capsys.readouterr().out)["verdict"] == "BROKEN"


def test_claims_without_mechanism_refuse_to_certify(tmp_path, monkeypatch,
                                                    capsys):
    def boom():
        raise gate.MechanismMissing("mechanism not present: gone.py")

    monkeypatch.setattr(gate, "_load_mechanism", boom)
    claim = make_claim("RC-NM", "healthy")
    code = gate.main(["--manifest", write_manifest(tmp_path, [claim]),
                      "--json"])
    out = json.loads(capsys.readouterr().out)
    assert code == 2
    assert out["verdict"] == "BROKEN"
    assert "refusing to pass on defaults" in out["reason"]


def test_human_readable_output_names_verdict(tmp_path, fake_mech, capsys):
    fake_mech(verdict="healthy")
    claim = make_claim("RC-HR", "healthy")
    code = gate.main(["--manifest", write_manifest(tmp_path, [claim])])
    out = capsys.readouterr().out
    assert code == 0
    assert "D55 claims gate: PASS" in out
    assert "RC-HR" in out
