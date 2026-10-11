"""Tests for tools/d30_causal_trace_gate.py — the D30 wire gate.

All fixtures use the REAL D30 engine (drift_canary.d30_causal_trace):
traces are built with make_event, sealed by the engine, serialized and
deserialized through the gate's own reproduction seam. The fraud battery
asserts the gate names the exact asserted-vs-actual disagreement.
"""
import json
import os
import sys

import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)
TOOLS = os.path.join(REPO_ROOT, "tools")
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

from drift_canary import d30_causal_trace as m  # noqa: E402
from drift_canary.d29_boundary import CONTROLLERS  # noqa: E402
import d30_causal_trace_gate as gate  # noqa: E402


# ---------------------------------------------------------------------------
# Fixtures — real engine, real seals.
# ---------------------------------------------------------------------------
def _env_events(trace_id, condition, available_word, clock):
    evs = []
    for i in (1, 2, 3):
        evs.append(m.make_event(
            event_id="%s-ENV-%02d" % (trace_id, i),
            producer=m.ENV_WITNESS, observer=m.TRACE_MONITOR,
            trace_id=trace_id, clock=clock,
            resource_id="DB-CONN",
            condition=condition,
            state_before="DB-CONN:%s" % available_word,
            state_after="DB-CONN:%s" % available_word))
    return evs


def _outcome(trace_id, clock):
    return m.make_event(
        event_id="%s-WORKER-OUTCOME" % trace_id,
        producer=m.WORKER_PRODUCER, observer=m.TRACE_MONITOR,
        trace_id=trace_id, clock=clock,
        resource_id="DB-CONN",
        condition="WORKFLOW_UNFINISHED",
        state_before="obligation:OUTSTANDING",
        state_after="obligation:OUTSTANDING")


def build_h1():
    """Honest environment-blocker trace (needs H2 as corpus)."""
    trace_id = "TRACE-TEST-H1"
    clock = m.LogicalClock()
    evs = _env_events(trace_id, "RESOURCE_UNAVAILABLE", "UNAVAILABLE", clock)
    evs.append(_outcome(trace_id, clock))
    return m.CausalTrace(trace_id=trace_id, events=tuple(evs), edges=())


def build_h2():
    """Honest worker-nonprogress trace (needs H1 as corpus)."""
    trace_id = "TRACE-TEST-H2"
    clock = m.LogicalClock()
    evs = _env_events(trace_id, "RESOURCE_AVAILABLE", "AVAILABLE", clock)
    for i in (1, 2, 3):
        evs.append(m.make_event(
            event_id="%s-SCHED-%02d" % (trace_id, i),
            producer=m.SCHEDULER_PRODUCER, observer=m.TRACE_MONITOR,
            trace_id=trace_id, clock=clock,
            resource_id="DB-CONN", lease_id="L-%d" % i,
            condition="SERVICE_ADEQUATE",
            state_before="debt=0", state_after="debt=0"))
    evs.append(_outcome(trace_id, clock))
    return m.CausalTrace(trace_id=trace_id, events=tuple(evs), edges=())


def payload(trace):
    return json.loads(m.serialize_trace(trace).decode("utf-8"))


@pytest.fixture()
def h1():
    return build_h1()


@pytest.fixture()
def h2():
    return build_h2()


@pytest.fixture()
def controllers():
    return tuple(CONTROLLERS)


def _claim(claim_id, trace, corpus, asserted_verdict, asserted_controller):
    return {
        "claim_id": claim_id,
        "trace": payload(trace),
        "corpus": [payload(c) for c in corpus],
        "asserted_verdict": asserted_verdict,
        "asserted_controller": asserted_controller,
    }


def _write_manifest(tmp_path, claims):
    p = tmp_path / "manifest.json"
    p.write_text(json.dumps({"version": 1, "claims": claims}))
    return str(p)


# ---------------------------------------------------------------------------
# Engine sanity: the fixtures must exercise the intended engine paths.
# ---------------------------------------------------------------------------
def test_h1_verifies_environment_blocker(h1, h2):
    v = m.CausalVerifier().verify(h1, corpus=(h2,))
    assert v.verdict == "ENVIRONMENT_BLOCKER"
    assert v.controller == "ENVIRONMENT"
    assert any(e.kind == "CAUSED_BY" for e in v.edges)


def test_h2_verifies_worker_nonprogress(h1, h2):
    v = m.CausalVerifier().verify(h2, corpus=(h1,))
    assert v.verdict == "WORKER_NONPROGRESS"
    assert v.controller == "WORKER"


def test_tampered_h1_downgrades_to_uncertainty(h1):
    tampered = m.tamper(h1.events[1], state_after="DB-CONN:AVAILABLE")
    evs = (h1.events[0], tampered) + h1.events[2:]
    t = m.CausalTrace(trace_id=h1.trace_id, events=evs, edges=())
    v = m.CausalVerifier().verify(t)
    assert v.verdict == "INSUFFICIENT_OBSERVABILITY"
    assert v.controller == "UNDETERMINED"


# ---------------------------------------------------------------------------
# Gate: canary + honest claims.
# ---------------------------------------------------------------------------
def test_canary_passes_on_real_engine():
    ok, detail = gate.run_canary(m)
    assert ok, detail


def test_canary_reproduction_seam_passes_on_real_engine():
    # The second canary travels the real attack path: serialize ->
    # _trace_from_payload -> verify. The real seam preserves the tamper.
    ok, detail = gate.run_canary_reproduction_seam(m)
    assert ok, detail


def test_honest_claims_pass(h1, h2, controllers, tmp_path):
    claims = [
        _claim("H1", h1, [h2], "ENVIRONMENT_BLOCKER", "ENVIRONMENT"),
        _claim("H2", h2, [h1], "WORKER_NONPROGRESS", "WORKER"),
    ]
    code, lines = gate.run_gate(_write_manifest(tmp_path, claims))
    assert code == 0, "\n".join(lines)
    assert any("PASS: 2 claim(s)" in l for l in lines)


def test_empty_claims_means_dormant(tmp_path):
    # DORMANT is a behavior of the gate (zero registered claims), not a
    # property of the checked-in file: the owning lane registers claims
    # by editing the manifest, and temp-probe commits must flow through
    # to the gate step itself.
    code, lines = gate.run_gate(_write_manifest(tmp_path, []))
    assert code == 0, "\n".join(lines)
    assert any("DORMANT" in l for l in lines)


# ---------------------------------------------------------------------------
# Gate: fraud battery — every disagreement must be named and blocked.
# ---------------------------------------------------------------------------
def test_tamper_fraud_blocked(h1, h2, controllers, tmp_path):
    tampered = m.tamper(h1.events[1], state_after="DB-CONN:AVAILABLE")
    evs = (h1.events[0], tampered) + h1.events[2:]
    fraud = m.CausalTrace(trace_id=h1.trace_id, events=evs, edges=())
    claims = [_claim("F1", fraud, [h2],
                     "SCHEDULER_STARVATION", "SCHEDULER")]
    code, lines = gate.run_gate(_write_manifest(tmp_path, claims))
    assert code == 1, "\n".join(lines)
    blob = "\n".join(lines)
    assert "F1" in blob
    assert "asserted=SCHEDULER_STARVATION/SCHEDULER" in blob
    assert "actual=INSUFFICIENT_OBSERVABILITY/UNDETERMINED" in blob


def test_wrong_controller_fraud_blocked(h1, h2, controllers, tmp_path):
    claims = [_claim("F2", h2, [h1],
                     "SCHEDULER_SERVICE_FAILURE", "SCHEDULER")]
    code, lines = gate.run_gate(_write_manifest(tmp_path, claims))
    assert code == 1, "\n".join(lines)
    blob = "\n".join(lines)
    assert "actual=WORKER_NONPROGRESS/WORKER" in blob


# ---------------------------------------------------------------------------
# Gate: fail-closed on every broken input.
# ---------------------------------------------------------------------------
def test_missing_manifest_is_broken(tmp_path):
    code, lines = gate.run_gate(str(tmp_path / "nope.json"))
    assert code == 2
    assert any("BROKEN" in l for l in lines)


def test_corrupt_manifest_is_broken(tmp_path):
    p = tmp_path / "manifest.json"
    p.write_text("{not json")
    code, lines = gate.run_gate(str(p))
    assert code == 2
    assert any("BROKEN" in l for l in lines)


def test_wrong_version_is_broken(tmp_path):
    p = tmp_path / "manifest.json"
    p.write_text(json.dumps({"version": 999, "claims": []}))
    code, lines = gate.run_gate(str(p))
    assert code == 2
    assert any("BROKEN" in l for l in lines)


def test_malformed_claim_is_broken(h1, tmp_path):
    bad = {"claim_id": "BAD", "trace": payload(h1),
           "asserted_verdict": "NOT_A_VERDICT",
           "asserted_controller": "ENVIRONMENT"}
    code, lines = gate.run_gate(_write_manifest(tmp_path, [bad]))
    assert code == 2
    assert any("BROKEN" in l for l in lines)


def test_empty_trace_claim_is_broken(tmp_path):
    empty = m.CausalTrace(trace_id="TRACE-EMPTY", events=(), edges=())
    claims = [_claim("E0", empty, [], "COMPLETED", "UNDETERMINED")]
    code, lines = gate.run_gate(_write_manifest(tmp_path, claims))
    assert code == 2
    assert any("BROKEN" in l for l in lines)


def test_claim_missing_trace_is_broken(tmp_path):
    bad = {"claim_id": "NO_TRACE",
           "asserted_verdict": "COMPLETED",
           "asserted_controller": "UNDETERMINED"}
    code, lines = gate.run_gate(_write_manifest(tmp_path, [bad]))
    assert code == 2
    assert any("BROKEN" in l for l in lines)


# ---------------------------------------------------------------------------
# Sabotage: a blind engine must never look green.
# ---------------------------------------------------------------------------
def test_blind_engine_fails_canary_closed(monkeypatch):
    class BlindVerifier:
        def verify(self, trace, corpus=(), _repro_mode=False):
            return m.CausalVerdict(
                verdict="ENVIRONMENT_BLOCKER", controller="ENVIRONMENT",
                level=3, edges=(), explanations_preserved=(), reasons=(),
                trace_id=getattr(trace, "trace_id", ""))

    monkeypatch.setattr(m, "CausalVerifier", BlindVerifier)
    ok, detail = gate.run_canary(m)
    assert not ok
    assert "CANARY BLIND" in detail
    code, lines = gate.run_gate(
        os.path.join(TOOLS, "d30_causal_trace_manifest.json"))
    assert code == 2
    assert any("CANARY BLIND" in l for l in lines)


_REAL_DESERIALIZE = m.deserialize_trace


def _forgiving_deserialize_seam(blob):
    """Sabotage: a deserialization seam that recomputes seals, healing any
    tamper before the engine sees it. This is the hole the verify lane's
    sabotage battery found: the in-memory canary never sees this seam."""
    import dataclasses

    out = _REAL_DESERIALIZE(blob)
    healed = []
    for e in out.events:
        h = m.event_body_hash(e)
        healed.append(dataclasses.replace(
            e, artifact_hash=h,
            attestation=m.observer_attestation(h, e.observer)))
    return m.CausalTrace(trace_id=out.trace_id,
                         events=tuple(healed), edges=out.edges)


def test_forgiving_deserialize_seam_heals_the_tamper(monkeypatch):
    # Prove the sabotage actually lands: through the forgiving seam the
    # tampered canary no longer reads as tampered.
    monkeypatch.setattr(m, "deserialize_trace", _forgiving_deserialize_seam)
    blob = m.serialize_trace(gate._canary_trace(m))
    trace = gate._trace_from_payload(m, json.loads(blob.decode("utf-8")))
    v = m.CausalVerifier().verify(trace)
    assert not (v.verdict == "INSUFFICIENT_OBSERVABILITY"
                and v.controller == "UNDETERMINED"), \
        "sabotage did not land: the seam did not heal the tamper"


def test_forgiving_deserialize_seam_fails_seam_canary_closed(monkeypatch):
    # The reproduction-seam canary must catch the forgiving seam: the gate
    # goes BROKEN (exit 2), never green. This is Finding 1's 9.0 fix.
    monkeypatch.setattr(m, "deserialize_trace", _forgiving_deserialize_seam)
    ok, detail = gate.run_canary_reproduction_seam(m)
    assert not ok, detail
    assert "SEAM BROKEN" in detail
    code, lines = gate.run_gate(
        os.path.join(TOOLS, "d30_causal_trace_manifest.json"))
    assert code == 2
    assert any("SEAM BROKEN" in l for l in lines)


def test_api_drift_is_broken(monkeypatch):
    monkeypatch.delattr(m, "deserialize_trace", raising=False)
    mod, controllers, err = gate.load_mechanism()
    assert mod is None
    assert "API drift" in err


def test_mechanism_absent_is_broken(monkeypatch):
    import importlib as _il

    real_import_module = _il.import_module

    def fake_import_module(name, package=None):
        if name.startswith("drift_canary"):
            raise ImportError("No module named %r" % (name,))
        return real_import_module(name, package)

    monkeypatch.setattr(_il, "import_module", fake_import_module)
    mod, controllers, err = gate.load_mechanism()
    assert mod is None
    assert "import failed" in err
