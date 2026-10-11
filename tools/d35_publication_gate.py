#!/usr/bin/env python3
"""D35 publication-boundary gate — wire the engine onto the
drift-canary governance-verification path.

The D35 mechanism (drift_canary/d35_publication.py, PR #2215) is the
atomic publication boundary as executable machinery: no cached
artifact, background worker, concurrent writer, or successor may
publish or reuse a qualification unless its evidence dependencies are
valid at the moment of publication or consequential use. Every publish
is a compare-and-swap evaluated against ONE consistent snapshot:

    PublishAllowed = ProjectionHeadMatches
                   ∧ QualificationDependenciesCurrent
                   ∧ EvidenceDependenciesAdmissible

The fraud this law exists to prevent (the mechanism's sharpest case):
worker W reads claim C at R5 holding a VALID fencing token; E1 is
revoked; W attempts publication. The naive checker certifies the write
— the token is valid, after all. The real engine REJECTS it
STALE_DEPENDENCY: a fencing token proves WHEN a worker read; it never
replaces the evidence-version check. A stale write that became current
authority is a system failure, not a test failure.

This gate puts that mechanism on a live operating path: every
publication scenario registered in tools/d35_publication_manifest.json
is cold-executed against the REAL D35 engine
(drift_canary/d35_publication.PublicationAuthority). The scenario is
rebuilt from the claim's own model bytes — a setup script plus one
publication attempt — and the claimant's asserted outcome must match
the engine's recomputed outcome exactly. A scenario the law refuses —
a stale dependency under a valid token, a write conflict on a moved
head, a scope wider than the read-time pin, a forged token, a sealed
successor package that no longer reconciles, a replayed smart-note
event, an index pointer that moved — is BLOCKED. The gate also
dogfoods the mechanism's own invariant on every judged scenario:
PublishedCurrent(P) ⇒ ValidDependencies(P, now) must hold after the
attempt; if the engine's own law breaks, the gate fails closed.

OPERATING PATH (what this protects and how to verify it stays connected):
  Path: the drift-canary governance-verification CI path — any PR
  touching drift_canary/d35_publication.py, this gate, its manifest,
  or its tests.
  Trigger: the publication-boundary check on pull_request / push-to-main.
  Block: check red (exit 1 VIOLATION or exit 2 BROKEN) blocks the merge path.
  Defect class: stale qualifications republished as current authority —
  valid-token stale writes, head-moved blind writes, scope-widened
  publications, forged tokens, unreconciled successor packages, torn
  indexes, double-applied smart notes.
  Verify-still-connected: `python tools/d35_publication_gate.py --json`
  must exit 0 DORMANT on a claim-free tree; registering the manifest's
  worked _example as a claim must exit 1 naming STALE_DEPENDENCY; claims
  present with the mechanism deleted must exit 2. If the workflow file
  disappears from .github/workflows/, the path is unwired — re-add it.

Exit contract (the whole point of the gate):
  0  PASS     — every registered scenario's outcome certified by the
                cold engine.
  0  DORMANT  — manifest absent or registers zero scenarios. Explicit,
                never a false green: the gate says "nothing to judge".
  1  VIOLATION— a scenario BLOCKED: the law refuses the publication
                (the engine's recomputed outcome diverges from the
                claimant's asserted outcome — the naive-checker frauds
                live here). The mechanism's own words name the refusal.
  2  BROKEN   — fail-closed: manifest corrupt, claim fields
                untrustworthy, an unknown assertion value, scenarios
                exist but the mechanism is absent, a scenario the engine
                cannot even construct, or the mechanism's own invariant
                broke. The gate never invents the engine and never
                defaults an unknown.

The gate never invents fields: unknown assertions, unknown ops,
malformed shapes, or missing keys are BROKEN, not defaulted. Scenario
CONTENT refused by the law is VIOLATION, not BROKEN — the distinction
is whose trust broke: the manifest's (BROKEN) or the scenario's
(VIOLATION).

Structural note: the gate never pre-computes the outcome — the
engine's PublicationOutcome is the authority, exactly as a real
atomic boundary must be the authority over its own CAS predicate.

Directive: D35 (Preventing Stale Qualifications From Being Republished;
mechanism PR #2215), owner naya4. Wired by the Naya 2 night-shift WIRE
lane. No merge — the merge lane owns it.
"""

import argparse
import importlib
import json
import sys
from pathlib import Path

EXIT_PASS = 0
EXIT_VIOLATION = 1
EXIT_BROKEN = 2

DEFAULT_MANIFEST = Path(__file__).resolve().parent / \
    "d35_publication_manifest.json"
MECHANISM_MODULE = "drift_canary.d35_publication"

# The workflow runs this script as `python tools/...` (script dir on
# sys.path, not the repo root). The mechanism lives at the repo root —
# append it so the gate imports the REAL engine wherever it runs from.
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

ASSERT_VALUES = (
    "PUBLISHED",
    "STALE_DEPENDENCY",
    "WRITE_CONFLICT",
    "TOKEN_REJECTED",
    "SCOPE_VIOLATION",
    "DUPLICATE_EVENT",
)

SETUP_OPS = (
    "register_evidence",
    "qualify",
    "read",
    "read_foreign",
    "revoke_evidence",
    "seal_package",
    "append_smart_note",
    "replace_index_pointer",
)

ATTEMPT_OPS = (
    "publish_summary",
    "reconcile_package",
    "publish_smart_note",
    "replace_index_pointer",
)


class GateBroken(Exception):
    """The manifest or the mechanism is untrustworthy — fail closed."""


class MechanismMissing(Exception):
    """Scenarios are registered but the D35 engine is absent."""


def _load_mechanism():
    try:
        return importlib.import_module(MECHANISM_MODULE)
    except Exception as exc:
        raise MechanismMissing(
            f"D35 mechanism {MECHANISM_MODULE!r} not importable: {exc}")


def _load_manifest(path):
    """Fail-closed loader. Returns None when absent (DORMANT), the data
    when present, raises GateBroken on anything untrustworthy."""
    p = Path(path)
    if not p.exists():
        return None
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        raise GateBroken(f"manifest {p} is not valid JSON: {exc}")
    if not isinstance(data, dict):
        raise GateBroken(
            f"manifest {p} must be a JSON object, got "
            f"{type(data).__name__}")
    claims = data.get("claims", None)
    if not isinstance(claims, list):
        raise GateBroken(
            f"manifest {p}: 'claims' must be a list, got "
            f"{type(claims).__name__}")
    seen = set()
    for i, entry in enumerate(claims):
        if not isinstance(entry, dict):
            raise GateBroken(
                f"manifest {p}: claim[{i}] must be an object, got "
                f"{type(entry).__name__}")
        cid = entry.get("id")
        if not isinstance(cid, str) or not cid:
            raise GateBroken(
                f"manifest {p}: claim[{i}] has no usable 'id'")
        if cid in seen:
            raise GateBroken(
                f"manifest {p}: duplicate claim id {cid!r} — refusing "
                f"to judge an ambiguous register")
        seen.add(cid)
    return data


def _check_str(val, loc, what):
    if not isinstance(val, str) or not val:
        raise GateBroken(f"{loc}: {what} must be a non-empty string")
    return val


def _check_str_list(val, loc, what):
    if not isinstance(val, list) or not all(
            isinstance(x, str) and x for x in val):
        raise GateBroken(
            f"{loc}: {what} must be a list of non-empty strings")
    return val


def _check_claim_shape(entry, manifest_path):
    """Structural trust of the claim's fields. Raises GateBroken on
    anything the gate cannot trust — never defaulted."""
    cid = entry.get("id")
    loc = f"manifest {manifest_path}: claim {cid!r}"
    obligation_id = entry.get("obligation_id")
    if not isinstance(obligation_id, str) or not obligation_id:
        raise GateBroken(f"{loc}: 'obligation_id' must be a non-empty "
                         f"string")
    asserts = entry.get("asserts")
    if asserts not in ASSERT_VALUES:
        raise GateBroken(
            f"{loc}: 'asserts' must be one of {ASSERT_VALUES}, got "
            f"{asserts!r} — the gate never defaults an unknown assertion")
    model = entry.get("model")
    if not isinstance(model, dict):
        raise GateBroken(
            f"{loc}: 'model' must be a JSON object, got "
            f"{type(model).__name__}")
    steps = model.get("steps")
    if not isinstance(steps, list):
        raise GateBroken(
            f"{loc}: model.steps must be a list, got "
            f"{type(steps).__name__}")
    attempt = model.get("attempt")
    if not isinstance(attempt, dict):
        raise GateBroken(
            f"{loc}: model.attempt must be a JSON object, got "
            f"{type(attempt).__name__}")
    return obligation_id, asserts, steps, attempt


def _exec_setup_op(auth, op, loc, mech, store, foreign_auth):
    """Execute one setup op on the REAL PublicationAuthority. Stores named
    manifests/packages in `store`. Engine construction failures (e.g.
    qualifying on unknown evidence) are GateBroken: the manifest asked
    for something the law cannot even construct — the manifest is
    untrustworthy, not the scenario content."""
    if not isinstance(op, dict):
        raise GateBroken(f"{loc}: setup op must be an object, got "
                         f"{type(op).__name__}")
    kind = op.get("op")
    if kind not in SETUP_OPS:
        raise GateBroken(
            f"{loc}: unknown setup op {kind!r} — the gate never invents "
            f"operations")
    try:
        if kind == "register_evidence":
            auth.register_evidence(_check_str(op.get("ev_id"), loc, "ev_id"))
        elif kind == "qualify":
            auth.qualify(
                _check_str(op.get("claim_id"), loc, "claim_id"),
                _check_str(op.get("verdict"), loc, "verdict"),
                tuple(_check_str_list(op.get("evidence_ids"), loc,
                                      "evidence_ids")),
                frozenset(_check_str_list(op.get("scope", []), loc,
                                          "scope")))
        elif kind == "read":
            name = _check_str(op.get("as"), loc, "'as' (manifest name)")
            manifest, _token = auth.read_for_write(
                _check_str(op.get("claim_id"), loc, "claim_id"),
                _check_str(op.get("worker_id"), loc, "worker_id"))
            store[name] = manifest
        elif kind == "read_foreign":
            # A token issued by a DIFFERENT authority — the forged-token
            # fraud. The mechanism must reject it at the boundary.
            name = _check_str(op.get("as"), loc, "'as' (manifest name)")
            if foreign_auth is None:
                raise GateBroken(
                    f"{loc}: read_foreign needs a foreign authority")
            foreign = foreign_auth()
            claim_id = _check_str(op.get("claim_id"), loc, "claim_id")
            foreign.register_evidence("foreign-ev")
            foreign.qualify(claim_id, "REQUALIFIED", ("foreign-ev",),
                            frozenset({"s1"}))
            manifest, _token = foreign.read_for_write(
                claim_id, _check_str(op.get("worker_id"), loc, "worker_id"))
            store[name] = manifest
        elif kind == "revoke_evidence":
            auth.revoke_evidence(_check_str(op.get("ev_id"), loc, "ev_id"))
        elif kind == "seal_package":
            name = _check_str(op.get("as"), loc, "'as' (package name)")
            store[name] = auth.seal_successor_package(
                _check_str(op.get("claim_id"), loc, "claim_id"))
        elif kind == "append_smart_note":
            auth.append_smart_note(
                _check_str(op.get("event_id"), loc, "event_id"),
                _check_str(op.get("claim_id"), loc, "claim_id"),
                str(op.get("content", "")))
        elif kind == "replace_index_pointer":
            new_pointer = _check_str(op.get("new_pointer"), loc,
                                     "new_pointer")
            expected_old = op.get("expected_old", None)
            if expected_old is not None and not isinstance(expected_old,
                                                           str):
                raise GateBroken(f"{loc}: expected_old must be a string "
                                 f"or null")
            auth.replace_index_pointer(new_pointer, expected_old)
    except GateBroken:
        raise
    except Exception as exc:
        raise GateBroken(
            f"{loc}: the D35 engine refused to construct setup op "
            f"{kind!r} — {type(exc).__name__}: {exc}")


def _exec_attempt(auth, attempt, loc, store):
    """Execute the single publication attempt against the REAL engine.
    Returns the PublicationOutcome. Engine crashes are GateBroken —
    failing closed."""
    if not isinstance(attempt, dict):
        raise GateBroken(f"{loc}: attempt must be an object, got "
                         f"{type(attempt).__name__}")
    kind = attempt.get("op")
    if kind not in ATTEMPT_OPS:
        raise GateBroken(
            f"{loc}: unknown attempt op {kind!r} — the gate never invents "
            f"operations")
    try:
        if kind == "publish_summary":
            name = _check_str(attempt.get("use"), loc, "'use' (manifest)")
            manifest = store.get(name)
            if manifest is None:
                raise GateBroken(
                    f"{loc}: attempt references unknown manifest "
                    f"{name!r} — nothing to publish from")
            return auth.publish_summary(
                manifest,
                str(attempt.get("content", "")),
                frozenset(_check_str_list(attempt.get("scope", []), loc,
                                          "scope")))
        if kind == "reconcile_package":
            name = _check_str(attempt.get("use"), loc, "'use' (package)")
            package = store.get(name)
            if package is None:
                raise GateBroken(
                    f"{loc}: attempt references unknown package "
                    f"{name!r} — nothing to reconcile")
            return auth.reconcile_package(package)
        if kind == "publish_smart_note":
            return auth.append_smart_note(
                _check_str(attempt.get("event_id"), loc, "event_id"),
                _check_str(attempt.get("claim_id"), loc, "claim_id"),
                str(attempt.get("content", "")))
        if kind == "replace_index_pointer":
            new_pointer = _check_str(attempt.get("new_pointer"), loc,
                                     "new_pointer")
            expected_old = attempt.get("expected_old", None)
            if expected_old is not None and not isinstance(expected_old,
                                                           str):
                raise GateBroken(f"{loc}: expected_old must be a string "
                                 f"or null")
            return auth.replace_index_pointer(new_pointer, expected_old)
    except GateBroken:
        raise
    except Exception as exc:
        raise GateBroken(
            f"{loc}: the D35 engine broke on the attempt — failing "
            f"closed: {type(exc).__name__}: {exc}")
    raise GateBroken(f"{loc}: unreachable attempt path")


def _judge_claim(entry, mech, manifest_path):
    """Cold-judge one publication scenario against the REAL D35 engine.
    Returns a result dict with verdict 'pass' or 'violation'. Raises
    GateBroken when the manifest or the mechanism is untrustworthy
    (fail-closed)."""
    claim_id = entry.get("id")
    loc = f"manifest {manifest_path}: claim {claim_id!r}"
    _obligation_id, asserts, steps, attempt = _check_claim_shape(
        entry, manifest_path)

    auth = mech.PublicationAuthority()
    store = {}

    def _foreign():
        return mech.PublicationAuthority()

    for i, op in enumerate(steps):
        _exec_setup_op(auth, op, f"{loc}: steps[{i}]", mech, store,
                       _foreign)
    outcome = _exec_attempt(auth, attempt, f"{loc}: attempt", store)

    # Dogfood the mechanism on every judged scenario: the D35 invariant
    # (PublishedCurrent(P) ⇒ ValidDependencies(P, now)) must hold after
    # the attempt. A broken engine fails closed, never certifies.
    try:
        auth.assert_invariant()
    except AssertionError as exc:
        raise GateBroken(
            f"claim {claim_id}: mechanism integrity broken — the D35 "
            f"invariant failed after the attempt: {exc}")

    actual = outcome.reason
    if actual == asserts:
        if actual == "PUBLISHED":
            reason = ("claimant's asserted outcome matches the cold "
                      "engine outcome exactly — the boundary committed "
                      f"at projection_rev={outcome.projection_rev}")
        else:
            reason = ("claimant's asserted outcome matches the cold "
                      "engine outcome exactly — the boundary refused: "
                      f"{outcome.detail}")
        return {"id": claim_id, "verdict": "pass",
                "asserted": asserts, "actual": actual, "reason": reason}
    # The law refuses the scenario's content — the naive-checker frauds
    # live here. Name the refusal in the mechanism's own words.
    return {"id": claim_id, "verdict": "violation",
            "asserted": asserts, "actual": actual,
            "reason": f"the D35 law judges {actual}, not {asserts} — "
                      f"{outcome.detail}"}


def _finish(exit_code, verdict, reason, results, as_json):
    payload = {"verdict": verdict, "reason": reason, "claims": results}
    if as_json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"D35 publication-boundary gate: {verdict} — {reason}")
        for r in results:
            line = (f"  [{r['verdict']}] {r['id']}: asserted={r['asserted']} "
                    f"actual={r['actual']}")
            if r.get("reason"):
                line += f" — {r['reason']}"
            print(line)
    return exit_code


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Judge publication scenarios against the D35 engine.")
    parser.add_argument("--manifest",
                        default=str(DEFAULT_MANIFEST),
                        help="path to d35_publication_manifest.json")
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
            results.append(_judge_claim(entry, mech, args.manifest))
    except GateBroken as exc:
        return _finish(EXIT_BROKEN, "BROKEN", str(exc), results,
                       args.as_json)
    violations = [r for r in results if r["verdict"] == "violation"]
    if violations:
        return _finish(EXIT_VIOLATION, "VIOLATION",
                       f"{len(violations)}/{len(results)} claim(s) blocked",
                       results, args.as_json)
    return _finish(EXIT_PASS, "PASS",
                   f"{len(results)} claim(s) certified by the D35 engine",
                   results, args.as_json)


if __name__ == "__main__":
    sys.exit(main())
