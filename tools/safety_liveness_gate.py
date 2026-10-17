#!/usr/bin/env python3
"""D55 claims gate — wire the safety-liveness classifier onto the recovery-claims path.

The D55 classifier (tools/safety_liveness_classifier.py, PR #2302) proves, in a
sandbox, that a recovery obligation is classified honestly: safety and
liveness independently, heartbeats never counted as progress, legitimate
holds never misclassified as liveness failures. This gate puts that mechanism
on a live operating path: every recovery claim registered in
tools/recovery_claims_manifest.json is judged by the REAL classifier, on the
claim's declared evidence. A claim whose declared classification disagrees
with the classifier is BLOCKED.

Exit contract (the whole point of the gate):
  0  PASS     — every registered claim certified by the classifier.
  0  DORMANT  — manifest absent or registers zero claims. Explicit, never a
                false green: the gate says "nothing to judge".
  1  VIOLATION— a claim misclassifies a recovery obligation (heartbeat fraud,
                liveness fraud on a legitimate hold), or carries a terminal
                disposition with neither evidence nor reason.
  2  BROKEN   — fail-closed: manifest corrupt, claim fields unparseable, or
                claims exist but the mechanism is absent (the gate refuses to
                certify on defaults — it never invents the classifier).

The gate never invents fields: unknown auth states, event kinds, or
classification values are BROKEN, not defaulted.

Directive: D55 (Safe Recovery Holds vs. Liveness Failures), wave 5, owner naya2.
Wired by the night-shift WIRE lane. No merge — Shawn pulls triggers.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
DEFAULT_MANIFEST = TOOLS_DIR / "recovery_claims_manifest.json"
MECHANISM_FILE = TOOLS_DIR / "safety_liveness_classifier.py"
MECHANISM_MODULE_NAME = "safety_liveness_classifier"

EXIT_PASS = 0
EXIT_VIOLATION = 1
EXIT_BROKEN = 2

# The D55 vocabulary. The gate mirrors it as constants (source cited above)
# so an unknown value is a hard error instead of a silent default.
VALID_CLASSIFICATIONS = frozenset({
    "healthy", "valid_hold", "recovery_defect", "waiting_authority",
    "scheduler_defect",
})
REQUIRED_CLAIM_KEYS = frozenset({"id", "claimed_classification", "obligation"})


class GateBroken(Exception):
    """Fail-closed: the gate cannot trust its inputs. Exit 2."""


class MechanismMissing(Exception):
    """The D55 classifier is absent. Exit 2 when claims exist, else DORMANT."""


def _load_mechanism():
    """Import the REAL D55 classifier from this tools/ directory.

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
    # The classifier's @dataclass decorators resolve annotations against
    # sys.modules[cls.__module__]; the module MUST be registered before
    # exec_module, or loading fails. Discovered by the wire lane's fire
    # battery (real integration) — unit tests with injected fakes cannot
    # see this. Any future loader of this mechanism needs the same recipe.
    sys.modules[MECHANISM_MODULE_NAME] = mod
    try:
        spec.loader.exec_module(mod)
    except Exception as exc:
        sys.modules.pop(MECHANISM_MODULE_NAME, None)
        raise MechanismMissing(f"mechanism failed to load: {exc}")
    for attr in ("classify", "Obligation", "Event", "AuthState",
                 "Classification", "ValidDisposition", "SERVICE", "PROGRESS"):
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


def _parse_event(raw, mech):
    if not isinstance(raw, dict):
        raise GateBroken("every event must be an object")
    kind = raw.get("kind")
    if kind == "service":
        event_kind = mech.SERVICE
    elif kind == "progress":
        event_kind = mech.PROGRESS
    else:
        raise GateBroken(
            f"unknown event kind: {kind!r} (never defaulted)")
    return mech.Event(kind=event_kind, detail=str(raw.get("detail", "")))


def _parse_obligation(raw, mech):
    if not isinstance(raw, dict):
        raise GateBroken("obligation must be an object")
    auth = raw.get("auth")
    try:
        auth_state = mech.AuthState(auth)
    except ValueError:
        raise GateBroken(f"unknown auth state: {auth!r} (never defaulted)")
    raw_events = raw.get("events", [])
    if not isinstance(raw_events, list):
        raise GateBroken("obligation.events must be a list")
    events = [_parse_event(e, mech) for e in raw_events]
    rec_raw = raw.get("reconciliation")
    reconciliation = (_parse_obligation(rec_raw, mech)
                      if rec_raw is not None else None)
    return mech.Obligation(
        name=str(raw.get("name", "")),
        auth=auth_state,
        events=events,
        reconciliation=reconciliation,
    )


def _fraud_pattern(claimed, actual, progressed):
    """Name the defect class when the mismatch matches a known fraud shape."""
    if (claimed == "healthy" and actual == "recovery_defect"
            and not progressed):
        return ("heartbeat fraud: serviced without verifiable progress, "
                "claimed healthy")
    if (claimed in ("recovery_defect", "scheduler_defect", "waiting_authority")
            and actual == "valid_hold"):
        return ("liveness fraud: legitimately prohibited action misclassified "
                "as a liveness failure")
    return ""


def judge_claim(claim, mech):
    """Judge one claim against the real classifier. Returns a result dict."""
    claimed = claim["claimed_classification"]
    if claimed not in VALID_CLASSIFICATIONS:
        raise GateBroken(
            f"unknown claimed_classification: {claimed!r} (never defaulted)")
    obligation = _parse_obligation(claim["obligation"], mech)
    diagnosis = mech.classify(obligation)
    actual = diagnosis.classification.value
    result = {
        "id": claim["id"],
        "claimed": claimed,
        "actual": actual,
        "tri_fact": {
            "enabled": bool(diagnosis.tri_fact.enabled),
            "serviced": bool(diagnosis.tri_fact.serviced),
            "progressed": bool(diagnosis.tri_fact.progressed),
        },
        "note": diagnosis.note,
    }
    if getattr(diagnosis, "scheduler_defect", False):
        # The hold is valid AND the authorized reconciliation sits runnable and
        # ignored — a real signal, but the claim itself is true. Surfaced, not
        # blocked; the merge-protocol watch owns the follow-up.
        result["attention"] = ("scheduler_defect: hold valid but authorized "
                               "reconciliation runnable and ignored")
    disposition = claim.get("disposition")
    if disposition is not None:
        if not isinstance(disposition, dict):
            raise GateBroken("claim.disposition must be an object")
        valid = mech.ValidDisposition(
            disposition=str(disposition.get("disposition", "")),
            evidence=str(disposition.get("evidence", "")),
            reason=str(disposition.get("reason", "")),
        )
        result["disposition_valid"] = valid.is_valid()
        if not valid.is_valid():
            result["verdict"] = "violation"
            result["reason"] = ("terminal disposition with neither evidence "
                                "nor reason is not a governed disposition")
            return result
    if claimed != actual:
        result["verdict"] = "violation"
        result["reason"] = (
            _fraud_pattern(claimed, actual,
                           diagnosis.tri_fact.progressed)
            or f"misclassification: claimed {claimed}, classifier says {actual}")
    else:
        result["verdict"] = "certified"
    return result


def _finish(exit_code, verdict, reason, results, as_json):
    payload = {"verdict": verdict, "reason": reason, "claims": results}
    if as_json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"D55 claims gate: {verdict} — {reason}")
        for r in results:
            line = (f"  [{r['verdict']}] {r['id']}: claimed={r['claimed']} "
                    f"actual={r['actual']}")
            if r.get("reason"):
                line += f" — {r['reason']}"
            if r.get("attention"):
                line += f" (attention: {r['attention']})"
            print(line)
    return exit_code


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Judge recovery claims against the D55 classifier.")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST),
                        help="path to recovery_claims_manifest.json")
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
                       "misclassified — blocked",
                       results, args.as_json)
    return _finish(EXIT_PASS, "PASS",
                   f"{len(results)} claim(s) certified by the D55 classifier",
                   results, args.as_json)


if __name__ == "__main__":
    sys.exit(main())
