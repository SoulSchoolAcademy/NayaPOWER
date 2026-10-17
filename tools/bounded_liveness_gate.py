#!/usr/bin/env python3
"""D56 bounded-liveness claims gate — wire the prover onto the recovery path.

The D56 prover (tools/bounded_recovery_liveness.py, PR #2307) proves, in a
sandbox, that a bounded-liveness claim about a recovery obligation is honest:
six preconditions independently established, bound enforceable on proven
assumptions, bound clock counting ELIGIBLE time only, four claims judged
independently. This gate puts that mechanism on a live operating path: every
bounded-liveness claim registered in
tools/bounded_liveness_claims_manifest.json is judged by the REAL prover, on
the claim's declared evidence. A claim whose declared verdicts disagree with
the prover is BLOCKED.

Exit contract (the whole point of the gate):
  0  PASS     — every registered claim certified by the prover.
  0  DORMANT  — manifest absent or registers zero claims. Explicit, never a
                false green: the gate says "nothing to judge".
  1  VIOLATION— a claim misstates a bounded-liveness verdict (timeout-as-
                fairness fraud, false healthy on a real breach, unproven
                asserted as decided).
  2  BROKEN   — fail-closed: manifest corrupt, claim fields unparseable, or
                claims exist but the mechanism is absent (the gate refuses to
                certify on defaults — it never invents the prover).

The gate never invents fields: unknown segment states, ladder rungs,
precondition names, bound kinds, or claim states are BROKEN, not defaulted.

Directive: D56 (Proving Bounded Recovery Liveness, AER-LIVE-2), wave 5,
owner naya2. Wired by the night-shift WIRE lane. No merge — Shawn pulls
triggers.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
DEFAULT_MANIFEST = TOOLS_DIR / "bounded_liveness_claims_manifest.json"
MECHANISM_FILE = TOOLS_DIR / "bounded_recovery_liveness.py"
MECHANISM_MODULE_NAME = "bounded_recovery_liveness"

EXIT_PASS = 0
EXIT_VIOLATION = 1
EXIT_BROKEN = 2

# The four independent claim slots. The gate mirrors the prover's vocabulary
# as constants (source cited above) so an unknown value is a hard error
# instead of a silent default.
CLAIM_SLOTS = (
    "safety",
    "scheduling_fairness",
    "bounded_progress",
    "task_completion",
)
REQUIRED_CLAIM_KEYS = frozenset(
    {"id", "claimed", "obligation", "bound", "preconditions"})


class GateBroken(Exception):
    """Fail-closed: the gate cannot trust its inputs. Exit 2."""


class MechanismMissing(Exception):
    """The D56 prover is absent. Exit 2 when claims exist, else DORMANT."""


def _load_mechanism():
    """Import the REAL D56 prover from this tools/ directory.

    Never synthesized, never defaulted. Verifies the required API surface so
    a neutered module cannot silently pass as the mechanism.
    """
    if not MECHANISM_FILE.is_file():
        raise MechanismMissing(
            f"mechanism not present: {MECHANISM_FILE.name}")
    spec = importlib.util.spec_from_file_location(
        MECHANISM_MODULE_NAME, MECHANISM_FILE)
    if spec is None or spec.loader is None:
        raise MechanismMissing("mechanism file present but not importable")
    mod = importlib.util.module_from_spec(spec)
    # The prover's @dataclass decorators resolve annotations against
    # sys.modules[cls.__module__]; the module MUST be registered before
    # exec_module, or loading fails. Same recipe as the D55 gate
    # (tools/safety_liveness_gate.py) — discovered by that lane's fire
    # battery on real integration; unit tests with injected fakes cannot
    # see this. Any future loader of this mechanism needs the same recipe.
    sys.modules[MECHANISM_MODULE_NAME] = mod
    try:
        spec.loader.exec_module(mod)
    except Exception as exc:
        sys.modules.pop(MECHANISM_MODULE_NAME, None)
        raise MechanismMissing(f"mechanism failed to load: {exc}")
    for attr in ("assess", "ObligationHistory", "EligibilitySegment",
                 "ServiceObservation", "ProgressMark", "Precondition",
                 "Assumption", "Bound", "CLAIM_STATES", "SEGMENT_STATES",
                 "PRECONDITIONS", "BOUND_KINDS", "SERVICE_LADDER",
                 "SERVICE_EVIDENCE_FIELDS", "NON_PROGRESS_EVENTS"):
        if not hasattr(mod, attr):
            raise MechanismMissing(
                f"mechanism missing required API: {attr}")
    return mod


def _load_manifest(path):
    """Load the claims manifest. Returns None when the file is absent.

    Raises GateBroken on anything untrustworthy: bad JSON, wrong shape,
    duplicate ids, claims missing required keys.
    """
    p = Path(path)
    if not p.is_file():
        return None
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        raise GateBroken(f"manifest is not valid JSON: {exc}")
    if not isinstance(data, dict) or not isinstance(data.get("claims"), list):
        raise GateBroken("manifest must be an object with a 'claims' list")
    seen = set()
    for entry in data["claims"]:
        if not isinstance(entry, dict):
            raise GateBroken("every claim must be an object")
        missing = REQUIRED_CLAIM_KEYS - set(entry.keys())
        if missing:
            raise GateBroken(
                f"claim missing required keys: {sorted(missing)}")
        cid = entry["id"]
        if cid in seen:
            raise GateBroken(f"duplicate claim id: {cid!r}")
        seen.add(cid)
    return data


def _as_int(value, what):
    if isinstance(value, bool) or not isinstance(value, int):
        raise GateBroken(f"{what} must be an integer clock unit, "
                         f"got {value!r} (never defaulted)")
    return value


def _as_bool(value, what):
    if not isinstance(value, bool):
        raise GateBroken(f"{what} must be true/false, got {value!r} "
                         "(never defaulted)")
    return value


def _parse_segments(raw, mech):
    if not isinstance(raw, list) or not raw:
        raise GateBroken("obligation.segments must be a non-empty list")
    segments = []
    for i, s in enumerate(raw):
        if not isinstance(s, dict):
            raise GateBroken(f"segment {i} must be an object")
        state = s.get("state")
        if state not in mech.SEGMENT_STATES:
            raise GateBroken(
                f"unknown segment state: {state!r} (never defaulted)")
        start = _as_int(s.get("start"), f"segment {i} start")
        end = _as_int(s.get("end"), f"segment {i} end")
        if end <= start:
            raise GateBroken(
                f"segment {i}: end must exceed start (got {start}, {end})")
        segments.append(mech.EligibilitySegment(
            state=state, start=start, end=end))
    return tuple(segments)


def _parse_service_observations(raw, mech):
    if raw is None:
        return ()
    if not isinstance(raw, list):
        raise GateBroken("obligation.service_observations must be a list")
    obs = []
    for i, o in enumerate(raw):
        if not isinstance(o, dict):
            raise GateBroken(f"service_observation {i} must be an object")
        rung = o.get("rung")
        if rung not in mech.SERVICE_LADDER:
            raise GateBroken(
                f"unknown service ladder rung: {rung!r} (never defaulted)")
        ev_raw = o.get("evidence", {})
        if not isinstance(ev_raw, dict):
            raise GateBroken(
                f"service_observation {i}: evidence must be an object")
        evidence = tuple((str(k), str(v)) for k, v in ev_raw.items())
        obs.append(mech.ServiceObservation(
            seq=_as_int(o.get("seq"), f"service_observation {i} seq"),
            rung=rung,
            evidence=evidence,
        ))
    return tuple(obs)


def _parse_progress_marks(raw, mech):
    if raw is None:
        return ()
    if not isinstance(raw, list):
        raise GateBroken("obligation.progress_marks must be a list")
    marks = []
    for i, m in enumerate(raw):
        if not isinstance(m, dict):
            raise GateBroken(f"progress_mark {i} must be an object")
        kind = m.get("kind")
        if not isinstance(kind, str) or not kind:
            raise GateBroken(
                f"progress_mark {i}: kind must be a non-empty string")
        marks.append(mech.ProgressMark(
            seq=_as_int(m.get("seq"), f"progress_mark {i} seq"),
            kind=kind,
            state_advance=_as_bool(
                m.get("state_advance", False),
                f"progress_mark {i} state_advance"),
            moves_toward_outcome=_as_bool(
                m.get("moves_toward_outcome", False),
                f"progress_mark {i} moves_toward_outcome"),
        ))
    return tuple(marks)


def _parse_obligation(raw, mech):
    if not isinstance(raw, dict):
        raise GateBroken("obligation must be an object")
    return mech.ObligationHistory(
        obligation=str(raw.get("name", "")),
        segments=_parse_segments(raw.get("segments"), mech),
        service_observations=_parse_service_observations(
            raw.get("service_observations"), mech),
        progress_marks=_parse_progress_marks(raw.get("progress_marks"), mech),
        disposition=str(raw.get("disposition", "") or ""),
        disposition_evidence=str(raw.get("disposition_evidence", "") or ""),
    )


def _parse_preconditions(raw, mech):
    if not isinstance(raw, list):
        raise GateBroken("preconditions must be a list")
    pres = []
    for i, p in enumerate(raw):
        if not isinstance(p, dict):
            raise GateBroken(f"precondition {i} must be an object")
        name = p.get("name")
        if name not in mech.PRECONDITIONS:
            raise GateBroken(
                f"unknown precondition name: {name!r} (never defaulted)")
        pres.append(mech.Precondition(
            name=name,
            established=_as_bool(p.get("established"),
                                f"precondition {name} established"),
            evidence=str(p.get("evidence", "") or ""),
        ))
    return tuple(pres)


def _parse_bound(raw, mech):
    if not isinstance(raw, dict):
        raise GateBroken("bound must be an object")
    kind = raw.get("kind")
    if kind not in mech.BOUND_KINDS:
        raise GateBroken(f"unknown bound kind: {kind!r} (never defaulted)")
    limit = _as_int(raw.get("limit"), "bound limit")
    if limit <= 0:
        raise GateBroken(f"bound limit must be positive, got {limit}")
    raw_assumptions = raw.get("assumptions", [])
    if not isinstance(raw_assumptions, list):
        raise GateBroken("bound.assumptions must be a list")
    assumptions = []
    for i, a in enumerate(raw_assumptions):
        if not isinstance(a, dict):
            raise GateBroken(f"assumption {i} must be an object")
        assumptions.append(mech.Assumption(
            statement=str(a.get("statement", "")),
            proven=_as_bool(a.get("proven"),
                            f"assumption {i} proven"),
            proof_ref=str(a.get("proof_ref", "") or ""),
        ))
    return mech.Bound(
        kind=kind,
        limit=limit,
        assumptions=tuple(assumptions),
        evidence=str(raw.get("evidence", "") or ""),
        label=str(raw.get("label", "") or ""),
    )


def _parse_claimed(raw, mech):
    if not isinstance(raw, dict):
        raise GateBroken("claimed must be an object")
    missing = [s for s in CLAIM_SLOTS if s not in raw]
    if missing:
        raise GateBroken(
            f"claimed missing slots: {missing} (all four required)")
    claimed = {}
    for slot in CLAIM_SLOTS:
        value = raw[slot]
        if value not in mech.CLAIM_STATES:
            raise GateBroken(
                f"unknown claim state for {slot}: {value!r} (never defaulted)")
        claimed[slot] = value
    return claimed


def _fraud_pattern(slot, claimed, actual, verdict):
    """Name the defect class when the mismatch matches a known fraud shape."""
    if (slot == "scheduling_fairness"
            and claimed == "violated"
            and actual in ("holds", "not_applicable")
            and verdict.eligible_time == 0):
        return ("timeout-as-fairness fraud: a never-eligible obligation "
                "(hold / waiting-authority / outage time) presented as a "
                "scheduling failure — the bound clock counts eligible time "
                "only; a wall-clock timeout is never by itself a fairness "
                "failure")
    if claimed == "holds" and actual == "violated":
        return (f"false healthy on {slot}: the prover finds a bounded-"
                "liveness breach the claim denies")
    if claimed != "unproven" and actual == "unproven":
        return (f"unproven asserted as decided on {slot}: preconditions or "
                "the bound are not established — the prover refuses to "
                "decide, and so must the claim")
    return ""


def judge_claim(claim, mech):
    """Judge one claim against the real prover. Returns a result dict."""
    claimed = _parse_claimed(claim["claimed"], mech)
    history = _parse_obligation(claim["obligation"], mech)
    bound = _parse_bound(claim["bound"], mech)
    preconditions = _parse_preconditions(claim["preconditions"], mech)
    verdict = mech.assess(history, bound, preconditions)
    actual = {slot: getattr(verdict, slot) for slot in CLAIM_SLOTS}
    result = {
        "id": claim["id"],
        "claimed": claimed,
        "actual": actual,
        "bound_enforceable": bool(verdict.bound_enforceable),
        "eligible_time": verdict.eligible_time,
        "wall_time": verdict.wall_time,
        "detail": verdict.detail,
    }
    mismatches = [s for s in CLAIM_SLOTS if claimed[s] != actual[s]]
    if mismatches:
        slot = mismatches[0]
        result["verdict"] = "violation"
        result["reason"] = (
            _fraud_pattern(slot, claimed[slot], actual[slot], verdict)
            or f"misstated {slot}: claimed {claimed[slot]}, "
               f"prover says {actual[slot]}")
        result["mismatched_slots"] = mismatches
    else:
        result["verdict"] = "certified"
    return result


def _finish(exit_code, verdict, reason, results, as_json):
    payload = {"verdict": verdict, "reason": reason, "claims": results}
    if as_json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"D56 bounded-liveness gate: {verdict} — {reason}")
        for r in results:
            line = (f"  [{r['verdict']}] {r['id']}: "
                    f"claimed={r['claimed']} actual={r['actual']}")
            if r.get("reason"):
                line += f" — {r['reason']}"
            print(line)
    return exit_code


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Judge bounded-liveness claims against the D56 prover.")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST),
                        help="path to bounded_liveness_claims_manifest.json")
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="machine-readable output")
    args = parser.parse_args(argv)

    try:
        data = _load_manifest(args.manifest)
    except GateBroken as exc:
        return _finish(EXIT_BROKEN, "BROKEN", str(exc), [], args.as_json)
    if data is None:
        return _finish(EXIT_PASS, "DORMANT",
                       "manifest absent: nothing to judge (explicit)",
                       [], args.as_json)
    claims = data["claims"]
    if not claims:
        return _finish(EXIT_PASS, "DORMANT",
                       "manifest registers zero claims: nothing to judge "
                       "(explicit, not a false green)",
                       [], args.as_json)
    try:
        mech = _load_mechanism()
    except MechanismMissing as exc:
        return _finish(EXIT_BROKEN, "BROKEN",
                       f"{exc}: {len(claims)} claim(s) registered but cannot "
                       "be certified — refusing to pass on defaults",
                       [], args.as_json)
    results = []
    try:
        for entry in claims:
            results.append(judge_claim(entry, mech))
    except GateBroken as exc:
        return _finish(EXIT_BROKEN, "BROKEN", str(exc), results, args.as_json)
    violations = [r for r in results if r["verdict"] == "violation"]
    if violations:
        return _finish(EXIT_VIOLATION, "VIOLATION",
                       f"{len(violations)}/{len(results)} claim(s) "
                       "misstated — blocked",
                       results, args.as_json)
    return _finish(EXIT_PASS, "PASS",
                   f"{len(results)} claim(s) certified by the D56 prover",
                   results, args.as_json)


if __name__ == "__main__":
    sys.exit(main())
