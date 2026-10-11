"""D31 incident-representation claims gate (WIRE lane, Naya 2).

Cold-judges every registered D31 scenario against the REAL
drift_canary.d31_incident.IncidentAnalyzer — never a reimplementation.
The incident is rebuilt from serialized bytes through the deserialization
seam, exactly as a cold successor would. A claim the D31 uncertainty law
refuses blocks the PR.

D31's core rule: an incident is an evidence-bound set of four independent
dimensions — observability, evidence, blockers, causal hypotheses — NEVER
a single failure_reason field. The gate enforces this structurally: any
incident payload carrying failure_reason is a VIOLATION.

Exit contract:
  0  PASS     - every live scenario's asserted claims match the engine
  0  DORMANT  - zero live scenarios registered (explicit, never a false green)
  1  VIOLATION- a scenario asserts a claim the engine refuses
  2  BROKEN   - fail-closed: manifest missing/corrupt, mechanism missing or
               tampered, canary probe failed (a blind engine never passes)

Fixed canary probes run before any judging:
  C1 blocked-canary - the sharpest-case incident (two OR blockers) MUST
     read is_blocked=True from the engine. A blind/neutered engine fails.
  C2 promotion-canary - promoting an UNRESOLVED hypothesis MUST raise
     PermissionError. An engine that lets blame collapse fails.
  C3 tamper-canary - tampered serialized bytes MUST fail deserialization.
     Bytes that silently survive tampering fail.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# The mechanism lives at the repo root. When CI runs
# `python tools/d31_incident_claims_gate.py`, Python puts tools/ on
# sys.path, not the repo root - so anchor the root explicitly. This also
# pins the "live tree" the gate judges: the checkout's own bytes.
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

MANIFEST_DEFAULT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "d31_incident_claims_manifest.json",
)

# The D31 vocabularies the gate speaks. The engine's own constants are
# asserted identical at import; the gate never invents competing words.
CLAIM_VERDICTS = ("SUPPORTED", "REFUTED", "CONFLICTED", "UNDETERMINED")
HYPOTHESIS_STATUSES = ("supported", "refuted", "unresolved")
CONTRIBUTION_TYPES = (
    "prevents_progress", "enables_progress", "masks_cause", "correlated_only",
)
REFUSAL_KINDS = ("promote_unresolved", "add_unestablished_blocker")
SCENARIO_KINDS = ("verdict_match", "refusal", "cold_successor")

# The forbidden collapse: D31's core rule is that this key must not exist
# anywhere in an incident representation or verdict.
FORBIDDEN_KEY = "failure_reason"


class GateBroken(Exception):
    """Fail-closed: the gate cannot judge honestly."""


class Violation(Exception):
    """A judged claim the D31 law refuses."""

    def __init__(self, scenario_id, detail):
        super().__init__("scenario=%s: %s" % (scenario_id, detail))
        self.scenario_id = scenario_id
        self.detail = detail


def _import_mechanism():
    """Import the REAL D31 engine from the live tree. Any tampering with
    the import surface fails closed."""
    try:
        from drift_canary import d31_incident as d31
    except Exception as exc:
        raise GateBroken("cannot import drift_canary.d31_incident "
                         "from the live tree: %r" % (exc,))
    required = (
        "IncidentAnalyzer", "Incident", "EvidenceState", "Blocker",
        "BlockerGraph", "Hypothesis", "ClaimProposition", "ObservationScope",
        "serialize_incident", "deserialize_incident",
        "cold_successor_reproduces", "recompute",
        "CLAIM_VERDICTS", "HYPOTHESIS_STATUSES", "CONTRIBUTION_TYPES",
    )
    missing = [name for name in required if not hasattr(d31, name)]
    if missing:
        raise GateBroken("mechanism tampered: missing names %s" % (missing,))
    # Vocabulary identity: the gate's words must BE the engine's words.
    if tuple(d31.CLAIM_VERDICTS) != CLAIM_VERDICTS:
        raise GateBroken("claim-verdict vocabulary drift")
    if tuple(d31.HYPOTHESIS_STATUSES) != HYPOTHESIS_STATUSES:
        raise GateBroken("hypothesis-status vocabulary drift")
    if tuple(d31.CONTRIBUTION_TYPES) != CONTRIBUTION_TYPES:
        raise GateBroken("contribution-type vocabulary drift")
    return d31


def load_manifest(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            manifest = json.load(fh)
    except FileNotFoundError:
        raise GateBroken("manifest not found: %s" % (path,))
    except json.JSONDecodeError as exc:
        raise GateBroken("manifest corrupt (not JSON): %s: %s" % (path, exc))
    if not isinstance(manifest, dict):
        raise GateBroken("manifest must be a JSON object")
    scenarios = manifest.get("scenarios", [])
    if not isinstance(scenarios, list):
        raise GateBroken("manifest 'scenarios' must be a list")
    return manifest


def _scan_forbidden(obj, trail="root"):
    """Recursively find the forbidden collapse key. Returns the trail
    where it was found, or None."""
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == FORBIDDEN_KEY:
                return trail + "." + key
            hit = _scan_forbidden(value, trail + "." + str(key))
            if hit:
                return hit
    elif isinstance(obj, (list, tuple)):
        for index, value in enumerate(obj):
            hit = _scan_forbidden(value, trail + "[%d]" % index)
            if hit:
                return hit
    return None


def _decode_incident(d31, scenario_id, incident_hex):
    """Cold rebuild through the deserialization seam. Tampered or
    malformed bytes fail closed."""
    if not isinstance(incident_hex, str) or not incident_hex:
        raise GateBroken("scenario=%s: incident_hex must be a non-empty "
                         "hex string" % (scenario_id,))
    try:
        blob = bytes.fromhex(incident_hex)
    except ValueError as exc:
        raise GateBroken("scenario=%s: incident_hex not hex: %s"
                         % (scenario_id, exc))
    try:
        payload = json.loads(blob.decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as exc:
        raise GateBroken("scenario=%s: incident bytes not decodable: %s"
                         % (scenario_id, exc))
    hit = _scan_forbidden(payload)
    if hit:
        raise Violation(scenario_id,
                        "forbidden collapse: incident payload carries '%s' "
                        "at %s - D31 forbids the single-explanation field"
                        % (FORBIDDEN_KEY, hit))
    try:
        incident = d31.deserialize_incident(blob)
    except Exception as exc:
        raise GateBroken("scenario=%s: deserialization failed: %r"
                         % (scenario_id, exc))
    return incident


def _check_verdict_match(d31, scenario):
    """The engine's independent verdict must equal the asserted one."""
    scenario_id = scenario["id"]
    incident = _decode_incident(d31, scenario_id, scenario.get("incident_hex"))
    asserted = scenario.get("asserted")
    if not isinstance(asserted, dict):
        raise GateBroken("scenario=%s: verdict_match needs an 'asserted' "
                         "object" % (scenario_id,))
    verdict = d31.IncidentAnalyzer().verdict(incident)
    if hasattr(verdict, FORBIDDEN_KEY):
        raise GateBroken("mechanism tampered: verdict carries '%s'"
                         % (FORBIDDEN_KEY,))
    failures = []
    actual_blocked = bool(verdict.is_blocked)
    if "is_blocked" in asserted and bool(asserted["is_blocked"]) != actual_blocked:
        failures.append("is_blocked: asserted=%s actual=%s"
                        % (asserted["is_blocked"], actual_blocked))
    actual_est = sorted(verdict.blockers_established)
    if "blockers_established" in asserted:
        if sorted(asserted["blockers_established"]) != actual_est:
            failures.append("blockers_established: asserted=%s actual=%s"
                            % (asserted["blockers_established"], actual_est))
    actual_unres = sorted(verdict.unresolved_hypotheses)
    if "unresolved_hypotheses" in asserted:
        if sorted(asserted["unresolved_hypotheses"]) != actual_unres:
            failures.append("unresolved_hypotheses: asserted=%s actual=%s"
                            % (asserted["unresolved_hypotheses"], actual_unres))
    actual_completion = bool(verdict.completion_declared)
    if "completion_declared" in asserted:
        if bool(asserted["completion_declared"]) != actual_completion:
            failures.append("completion_declared: asserted=%s actual=%s "
                            "(partial repair is never completion)"
                            % (asserted["completion_declared"],
                               actual_completion))
    if "claim_verdicts" in asserted:
        asserted_cv = asserted["claim_verdicts"]
        if not isinstance(asserted_cv, dict):
            raise GateBroken("scenario=%s: claim_verdicts must be an object"
                             % (scenario_id,))
        actual_cv = dict(verdict.claim_verdicts)
        for pid, averdict in asserted_cv.items():
            if averdict not in CLAIM_VERDICTS:
                raise GateBroken("scenario=%s: bad claim verdict %r"
                                 % (scenario_id, averdict))
            if actual_cv.get(pid) != averdict:
                failures.append("claim '%s': asserted=%s actual=%s"
                                % (pid, averdict, actual_cv.get(pid)))
    if failures:
        raise Violation(scenario_id, "; ".join(failures))
    return None


def _check_refusal(d31, scenario):
    """The engine must refuse exactly as asserted (or not)."""
    scenario_id = scenario["id"]
    kind = scenario.get("refusal")
    if kind not in REFUSAL_KINDS:
        raise GateBroken("scenario=%s: unknown refusal kind %r"
                         % (scenario_id, kind))
    asserted_refused = scenario.get("asserted_refused")
    if not isinstance(asserted_refused, bool):
        raise GateBroken("scenario=%s: asserted_refused must be boolean"
                         % (scenario_id,))
    payload = scenario.get("refusal_input")
    if not isinstance(payload, dict):
        raise GateBroken("scenario=%s: refusal needs a 'refusal_input' "
                         "object" % (scenario_id,))
    refused = False
    refusal_note = ""
    try:
        if kind == "promote_unresolved":
            status = payload.get("status", "unresolved")
            if status not in HYPOTHESIS_STATUSES:
                raise GateBroken("scenario=%s: bad hypothesis status %r"
                                 % (scenario_id, status))
            ctype = payload.get("contribution_type", "prevents_progress")
            if ctype not in CONTRIBUTION_TYPES:
                raise GateBroken("scenario=%s: bad contribution type %r"
                                 % (scenario_id, ctype))
            hyp = d31.Hypothesis(
                hypothesis_id=payload.get("hypothesis_id", "h-probe"),
                mechanism=payload.get("mechanism", "probe mechanism"),
                contribution_type=ctype,
                status=status)
            hyp.promote_to_verified_lesson()
            refusal_note = "promotion allowed"
        else:  # add_unestablished_blocker
            established = payload.get("established_by", [])
            if not isinstance(established, list):
                raise GateBroken("scenario=%s: established_by must be a list"
                                 % (scenario_id,))
            graph = d31.BlockerGraph()
            graph.add_blocker(d31.Blocker(
                blocker_id=payload.get("blocker_id", "b-probe"),
                description=payload.get("description", "probe blocker"),
                condition=payload.get("condition", "PROBE"),
                established_by=tuple(established)))
            refusal_note = "blocker accepted"
    except PermissionError as exc:
        refused = True
        refusal_note = "PermissionError: %s" % (exc,)
    except ValueError as exc:
        refused = True
        refusal_note = "ValueError: %s" % (exc,)
    if refused != asserted_refused:
        raise Violation(scenario_id,
                        "refusal=%s: asserted_refused=%s actual_refused=%s "
                        "(%s)" % (kind, asserted_refused, refused,
                                  refusal_note))
    return None


def _check_cold_successor(d31, scenario):
    scenario_id = scenario["id"]
    incident = _decode_incident(d31, scenario_id, scenario.get("incident_hex"))
    asserted = scenario.get("asserted")
    if not isinstance(asserted, bool):
        raise GateBroken("scenario=%s: cold_successor needs a boolean "
                         "'asserted'" % (scenario_id,))
    same, detail = d31.cold_successor_reproduces(incident)
    if bool(same) != asserted:
        raise Violation(scenario_id,
                        "cold_successor: asserted=%s actual=%s (%s)"
                        % (asserted, same, detail))
    return None


def judge_scenario(d31, scenario):
    """Judge one scenario against the real engine. Raises Violation on a
    refused claim, GateBroken when judging is impossible."""
    if not isinstance(scenario, dict) or "id" not in scenario:
        raise GateBroken("scenario malformed: %r" % (scenario,))
    kind = scenario.get("kind")
    if kind not in SCENARIO_KINDS:
        raise GateBroken("scenario=%s: unknown kind %r"
                         % (scenario.get("id", "?"), kind))
    if kind == "verdict_match":
        return _check_verdict_match(d31, scenario)
    if kind == "refusal":
        return _check_refusal(d31, scenario)
    return _check_cold_successor(d31, scenario)


def _canary_incident_hex(d31):
    """The sharpest-case incident, built in-code from the live tree. The
    canary never trusts the manifest."""
    from drift_canary.d30_causal_trace import LogicalClock, make_event
    clock = LogicalClock()

    def evt(eid, producer, observer, condition=""):
        return make_event(event_id=eid, producer=producer, observer=observer,
                          trace_id="d31canary", clock=clock,
                          condition=condition, state_before="before",
                          state_after="after")

    auth_ev = evt("c-ev-auth", "law-engine", "auth-monitor", "AUTH_EXPIRED")
    hb_ev = evt("c-ev-hb", "worker-pool", "pool-monitor", "WORKER_UNAVAILABLE")
    ev = d31.EvidenceState()
    ev.add_event(auth_ev)
    ev.add_event(hb_ev)
    graph = d31.BlockerGraph(blocking_sets=(
        frozenset({"c-law-auth"}), frozenset({"c-worker"})))
    graph.add_blocker(d31.Blocker(
        blocker_id="c-law-auth", description="canary auth blocker",
        condition="AUTH_EXPIRED", established_by=("c-ev-auth",)))
    graph.add_blocker(d31.Blocker(
        blocker_id="c-worker", description="canary worker blocker",
        condition="WORKER_UNAVAILABLE", established_by=("c-ev-hb",)))
    incident = d31.Incident(
        incident_id="canary-blocked",
        scopes=(),
        evidence=ev,
        blockers=graph,
        hypotheses=(d31.Hypothesis(
            hypothesis_id="c-h", mechanism="canary mechanism",
            contribution_type="prevents_progress", status="unresolved"),))
    return d31.serialize_incident(incident).hex()


def run_canaries(d31):
    """Fixed probes, run before any judging. A neutered or blind engine
    fails here -> GateBroken (exit 2), never a blind pass."""
    # C1: the blocked canary must read blocked from the REAL engine.
    incident = d31.deserialize_incident(
        bytes.fromhex(_canary_incident_hex(d31)))
    verdict = d31.IncidentAnalyzer().verdict(incident)
    if not verdict.is_blocked:
        raise GateBroken("canary C1 FAILED: sharpest-case incident reads "
                         "is_blocked=False (engine is blind to blockers)")
    if verdict.completion_declared:
        raise GateBroken("canary C1 FAILED: blocked incident declares "
                         "completion (engine is blind to the completion bar)")

    # C2: unresolved promotion must raise, mechanically.
    hyp = d31.Hypothesis(
        hypothesis_id="c-h-promo", mechanism="canary",
        contribution_type="prevents_progress", status="unresolved")
    try:
        hyp.promote_to_verified_lesson()
    except PermissionError:
        pass
    else:
        raise GateBroken("canary C2 FAILED: unresolved hypothesis promoted "
                         "without refusal (blame-collapse is live)")

    # C3: tampered bytes must fail the deserialization seam.
    blob = bytes.fromhex(_canary_incident_hex(d31))
    tampered = bytearray(blob)
    tampered[len(tampered) // 2] ^= 0xFF
    try:
        d31.deserialize_incident(bytes(tampered))
    except Exception:
        pass
    else:
        raise GateBroken("canary C3 FAILED: tampered incident bytes "
                         "deserialized cleanly (seal is theater)")


def judge_manifest(d31, manifest, include_examples=False):
    """Returns (verdict, detail) with verdict in PASS/DORMANT/VIOLATION."""
    scenarios = manifest.get("scenarios", [])
    live = [s for s in scenarios
            if not (isinstance(s, dict) and s.get("id", "").startswith("_"))]
    if include_examples:
        for key, value in manifest.items():
            if (isinstance(key, str) and key.startswith("_example")
                    and isinstance(value, dict) and "id" in value):
                live.append(value)
    if not live:
        return "DORMANT", "zero live scenarios registered"
    for scenario in live:
        judge_scenario(d31, scenario)
    return "PASS", "%d scenario(s) match the engine's word" % (len(live),)


def main(argv):
    manifest_path = argv[1] if len(argv) > 1 else MANIFEST_DEFAULT
    include_examples = "--include-examples" in argv
    try:
        d31 = _import_mechanism()
        manifest = load_manifest(manifest_path)
        run_canaries(d31)
        verdict, detail = judge_manifest(d31, manifest,
                                         include_examples=include_examples)
    except Violation as exc:
        print("D31-GATE VIOLATION: %s" % (exc,))
        return 1
    except GateBroken as exc:
        print("D31-GATE BROKEN (fail-closed): %s" % (exc,))
        return 2
    print("D31-GATE %s: %s" % (verdict, detail))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
