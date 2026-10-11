"""D30 wire gate — causal-trace claims judged against the real D30 engine.

Wire for D30 (Verifiable Causal Trace Across Environment, Scheduler and
Worker; mechanism: drift_canary/d30_causal_trace.py, PR #2202, Naya 4's
lane). This gate binds the CI path to the mechanism: every registered
causal-trace claim is cold-judged by the REAL CausalVerifier, rebuilt
from serialized bytes. A claim whose asserted verdict/controller does
not equal the engine's independent verdict is BLOCKED.

Exit contract:
  0 PASS     — every registered claim matches the engine's verdict.
  0 DORMANT  — zero registered claims (canary still ran; explicit, not silent).
  1 VIOLATION— at least one claim's asserted verdict/controller disagrees
               with the engine. The disagreement is named.
  2 BROKEN   — fail-closed: manifest unreadable/corrupt, claim malformed,
               mechanism unavailable or API-incompatible, or either
               fixed canary probe fails (a blind engine — or a seam
               that heals tampers — must never look green).

The fixed canary (run first, every run): a trace carrying one tampered
event (seal broken without reseal) MUST verify as
INSUFFICIENT_OBSERVABILITY/UNDETERMINED. If the engine says anything
else, it is blind or broken — the gate refuses (exit 2).
A second canary runs the SAME tampered trace through the reproduction
seam (serialize -> _trace_from_payload -> verify) — the exact path
every registered claim travels. A deserialization seam that recomputes
seals heals the tamper before the engine sees it; that is BROKEN, never
green.

Boundary: CI governance path only. Runtime kernel/KNOW/LAW/ACT wiring
still needs Shawn's word per the mechanism docstring. Nothing here
merges, deploys, or writes to production.
"""
from __future__ import annotations

import argparse
import importlib
import json
import os
import sys

MANIFEST_VERSION = 1

# Required engine API surface. If any name is missing the mechanism is
# not the D30 contract we wire against — fail closed, never adapt.
_REQUIRED_API = (
    "CausalVerifier",
    "CausalTrace",
    "EvidenceEvent",
    "LogicalClock",
    "VERDICTS",
    "ENV_WITNESS",
    "TRACE_MONITOR",
    "WORKER_PRODUCER",
    "authenticate",
    "make_event",
    "tamper",
    "serialize_trace",
    "deserialize_trace",
)

# Controller vocabulary lives in d29_boundary (D30's evidence layer).
_FALLBACK_CONTROLLERS = ("ENVIRONMENT", "SCHEDULER", "WORKER", "UNDETERMINED")


def load_mechanism():
    """Import the real D30 engine. Returns (module, controllers, error).

    Fail-closed: any import problem or API drift is BROKEN, not a pass.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(here)  # tools/ -> repo root
    if root not in sys.path:
        sys.path.insert(0, root)
    try:
        mod = importlib.import_module("drift_canary.d30_causal_trace")
    except Exception as exc:  # noqa: BLE001 — any import failure is fatal
        return None, None, "mechanism import failed: %r" % (exc,)
    missing = [name for name in _REQUIRED_API if not hasattr(mod, name)]
    if missing:
        return None, None, (
            "mechanism API drift: missing %s" % (", ".join(missing),))
    try:
        d29 = importlib.import_module("drift_canary.d29_boundary")
        controllers = tuple(getattr(d29, "CONTROLLERS", _FALLBACK_CONTROLLERS))
    except Exception:  # noqa: BLE001 — fallback vocabulary, still closed
        controllers = _FALLBACK_CONTROLLERS
    return mod, controllers, None


def _canary_trace(mod):
    """The fixed canary: three environment observations + one outcome,
    with the middle event's sealed body altered without resealing.
    The engine MUST refuse to reason from this trace."""
    trace_id = "TRACE-D30-CANARY"
    clock = mod.LogicalClock()
    evs = []
    for i in (1, 2, 3):
        evs.append(mod.make_event(
            event_id="%s-ENV-%02d" % (trace_id, i),
            producer=mod.ENV_WITNESS, observer=mod.TRACE_MONITOR,
            trace_id=trace_id, clock=clock,
            resource_id="DB-CONN",
            condition="RESOURCE_UNAVAILABLE",
            state_before="DB-CONN:UNAVAILABLE",
            state_after="DB-CONN:UNAVAILABLE"))
    evs.append(mod.make_event(
        event_id="%s-WORKER-OUTCOME" % trace_id,
        producer=mod.WORKER_PRODUCER, observer=mod.TRACE_MONITOR,
        trace_id=trace_id, clock=clock,
        resource_id="DB-CONN",
        condition="WORKFLOW_UNFINISHED",
        state_before="obligation:OUTSTANDING",
        state_after="obligation:OUTSTANDING"))
    tampered = mod.tamper(evs[1], state_after="DB-CONN:AVAILABLE")
    return mod.CausalTrace(
        trace_id=trace_id,
        events=(evs[0], tampered, evs[2], evs[3]), edges=())


def _canary_ok(verdict):
    return (verdict.verdict == "INSUFFICIENT_OBSERVABILITY"
            and verdict.controller == "UNDETERMINED")


def run_canary(mod):
    """Returns (ok, detail). A blind engine is a BROKEN gate, never green."""
    verdict = mod.CausalVerifier().verify(_canary_trace(mod))
    if _canary_ok(verdict):
        return True, ("canary: tampered trace -> "
                      "INSUFFICIENT_OBSERVABILITY/UNDETERMINED")
    return False, (
        "CANARY BLIND: tampered trace verified as %s/%s "
        "(expected INSUFFICIENT_OBSERVABILITY/UNDETERMINED)" % (
            verdict.verdict, verdict.controller))


def run_canary_reproduction_seam(mod):
    """Second canary, on the REAL attack path. The tampered canary trace
    is serialized and rebuilt through _trace_from_payload — the exact
    json.dumps -> deserialize_trace seam every registered claim travels.
    A seam that recomputes seals heals the tamper before the engine sees
    it; that must be BROKEN, never green. Returns (ok, detail)."""
    try:
        blob = mod.serialize_trace(_canary_trace(mod))
        payload = json.loads(blob.decode("utf-8"))
        trace = _trace_from_payload(mod, payload)
        verdict = mod.CausalVerifier().verify(trace)
    except Exception as exc:  # noqa: BLE001 — any seam failure is fatal
        return False, "CANARY SEAM BROKEN: reproduction seam failed: %r" % (
            exc,)
    if _canary_ok(verdict):
        return True, ("canary-seam: tampered trace via reproduction seam -> "
                      "INSUFFICIENT_OBSERVABILITY/UNDETERMINED")
    return False, (
        "CANARY SEAM BROKEN: tampered trace through the reproduction seam "
        "verified as %s/%s (expected "
        "INSUFFICIENT_OBSERVABILITY/UNDETERMINED) — "
        "the seam heals tampers" % (verdict.verdict, verdict.controller))


def _trace_from_payload(mod, payload):
    """Rebuild a trace from the manifest's serialized payload through the
    real deserialization path — the reproduction seam, not a shortcut."""
    if not isinstance(payload, dict):
        raise ValueError("trace payload must be a JSON object")
    blob = json.dumps(payload, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")
    trace = mod.deserialize_trace(blob)
    if not trace.events:
        raise ValueError("trace carries zero events: nothing to judge")
    return trace


def _validate_claim(mod, controllers, claim):
    """Returns (claim_id, trace, corpus, asserted_verdict, asserted_controller)
    or raises ValueError on any malformation (fail-closed)."""
    if not isinstance(claim, dict):
        raise ValueError("claim must be a JSON object")
    claim_id = claim.get("claim_id")
    if not claim_id or not isinstance(claim_id, str):
        raise ValueError("claim missing string claim_id")
    asserted_verdict = claim.get("asserted_verdict")
    asserted_controller = claim.get("asserted_controller")
    if asserted_verdict not in tuple(mod.VERDICTS):
        raise ValueError(
            "%s: asserted_verdict %r not in D30 verdict vocabulary" % (
                claim_id, asserted_verdict))
    if asserted_controller not in tuple(controllers):
        raise ValueError(
            "%s: asserted_controller %r not in controller vocabulary" % (
                claim_id, asserted_controller))
    if "trace" not in claim:
        raise ValueError("%s: claim missing trace payload" % claim_id)
    trace = _trace_from_payload(mod, claim["trace"])
    corpus = []
    raw_corpus = claim.get("corpus", [])
    if not isinstance(raw_corpus, list):
        raise ValueError("%s: corpus must be a list" % claim_id)
    for peer in raw_corpus:
        corpus.append(_trace_from_payload(mod, peer))
    return claim_id, trace, tuple(corpus), asserted_verdict, asserted_controller


def judge_claim(mod, controllers, claim):
    """Judge one claim. Returns (verdict_word, detail).

    verdict_word in {"PASS", "VIOLATION"}; malformation raises ValueError.
    """
    (claim_id, trace, corpus,
     asserted_verdict, asserted_controller) = _validate_claim(
        mod, controllers, claim)
    actual = mod.CausalVerifier().verify(trace, corpus=corpus)
    if (actual.verdict == asserted_verdict
            and actual.controller == asserted_controller):
        return "PASS", (
            "%s: engine agrees (%s/%s)" % (
                claim_id, actual.verdict, actual.controller))
    return "VIOLATION", (
        "%s: asserted=%s/%s actual=%s/%s — engine disagrees" % (
            claim_id, asserted_verdict, asserted_controller,
            actual.verdict, actual.controller))


def load_manifest(path):
    """Returns (manifest_dict, error). Corrupt manifests are BROKEN."""
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        return None, "manifest not found: %s" % path
    except json.JSONDecodeError as exc:
        return None, "manifest is not valid JSON: %s" % (exc,)
    except OSError as exc:
        return None, "manifest unreadable: %s" % (exc,)
    if not isinstance(data, dict):
        return None, "manifest root must be a JSON object"
    if data.get("version") != MANIFEST_VERSION:
        return None, (
            "manifest version %r != gate version %r" % (
                data.get("version"), MANIFEST_VERSION))
    claims = data.get("claims", [])
    if not isinstance(claims, list):
        return None, "manifest 'claims' must be a list"
    return data, None


def run_gate(manifest_path):
    """Returns (exit_code, lines). The full gate run, testable in-process."""
    lines = []
    mod, controllers, err = load_mechanism()
    if err is not None:
        return 2, ["BROKEN: %s" % err]
    ok, detail = run_canary(mod)
    lines.append(detail)
    if not ok:
        return 2, ["BROKEN: %s" % detail] + lines[1:]
    ok, detail = run_canary_reproduction_seam(mod)
    lines.append(detail)
    if not ok:
        return 2, ["BROKEN: %s" % detail] + lines[1:]
    manifest, err = load_manifest(manifest_path)
    if err is not None:
        return 2, lines + ["BROKEN: %s" % err]
    claims = manifest["claims"]
    if not claims:
        return 0, lines + ["DORMANT: zero registered claims; "
                           "canary passed, engine live"]
    violations = []
    for claim in claims:
        try:
            word, detail = judge_claim(mod, controllers, claim)
        except ValueError as exc:
            return 2, lines + ["BROKEN: malformed claim: %s" % (exc,)]
        lines.append(detail)
        if word == "VIOLATION":
            violations.append(detail)
    if violations:
        return 1, lines + ["VIOLATION: %d claim(s) disagree with "
                           "the independent engine" % len(violations)]
    return 0, lines + ["PASS: %d claim(s) agree with the independent "
                       "engine" % len(claims)]


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="D30 causal-trace claims gate")
    parser.add_argument("--manifest", required=True,
                        help="path to the claims manifest JSON")
    args = parser.parse_args(argv)
    code, lines = run_gate(args.manifest)
    for line in lines:
        print(line)
    return code


if __name__ == "__main__":
    sys.exit(main())
