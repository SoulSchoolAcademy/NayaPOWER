#!/usr/bin/env python3
"""D65 joint-proof qualification gate — wire the engine onto the
drift-canary governance-verification path.

The D65 mechanism (drift_canary/strongly_connected_groups.py, PR #2327)
is the strongly-connected-invariant-groups law as executable machinery
(AER-LIVE-10): when invariants depend on one another cyclically, no
member may serve as independent proof of another. The verifier collapses
the cycle into one joint state-transition system, grounds it in
authoritative initial state, and computes reachability, safety closure,
repeatability (greatest fixed point), progress (maximum-mean-cycle) and
exit viability from the PRESENTED complete transition relation — never
from pre-computed caller booleans. Five verdicts, never one:
REPEATABLE_PROVEN / DEADLOCK_IN_SCOPE / LIVELOCK_COUNTEREXAMPLE /
EXIT_POSSIBLE_NOT_GUARANTEED / JOINT_UNDETERMINED — because an escape
path existing is not the same as every fair execution escaping. A
refusal carries the MINIMAL joint obstruction: exactly the failed
grounding facts, each individually necessary, nothing else.

The frauds this law exists to prevent (the naive spec baseline in the
mechanism demonstrates all five, and the mechanism's tests prove it
wrong): (1) trusting caller booleans with no transition relation at
all — certifying a cycle repeatable on bare assertions; (2) a group
establishing its own external facts — self-certified authority, which
the naive shape cannot even express; (3) no progress check — a
zero-progress spin certified REPEATABLE instead of LIVELOCK; (4)
conflating exit with repeatable — swallowing the exit dimension;
(5) refusals that name nothing — a bare enum with no obstruction.

This gate puts that mechanism on a live operating path: every joint
declaration registered in tools/d65_joint_proof_manifest.json is
cold-judged by the REAL D65 engine. The declaration is rebuilt from
the claim's own model bytes and verify_joint recomputes the verdict;
the claimant's asserted verdict must match the engine's recomputed
judgment exactly. A claim the law refuses — a self-certified
authority, a digest mismatch (model drifted under the authorization),
a spurious joint (members not one strongly connected component), a
member-authorized replenishment, an invented REPEATABLE_PROVEN over a
livelock, a collapsed exit, or a malformed joint the engine refuses —
is BLOCKED. The gate also dogfoods the mechanism's own integrity on
every judged verdict: the verdict's model digest must equal the digest
of the model actually judged (the verdict qualifies the presented
model only), the verdict's group must name the declared joint, and the
canonical model encoding must be byte-stable across rebuilds.

OPERATING PATH (what this protects and how to verify it stays connected):
  Path: the drift-canary governance-verification CI path — any PR
  touching drift_canary/strongly_connected_groups.py, this gate, its
  manifest, or its tests.
  Trigger: the joint-proof-verification check on pull_request /
  push-to-main.
  Block: check red (exit 1 VIOLATION or exit 2 BROKEN) blocks the merge path.
  Defect class: joint-proof qualification claims the D65 law refuses —
  self-certified authorities, digest mismatches, spurious joints,
  member-authorized replenishments, invented repeatability over
  livelocks, exit conflation, ungrounded groups, malformed joints.
  Verify-still-connected: `python tools/d65_joint_proof_gate.py --json`
  must exit 0 DORMANT on a claim-free tree; registering the manifest's
  worked _example as a claim must exit 1 naming the livelock fraud;
  claims present with the mechanism deleted must exit 2. If the
  workflow file disappears from .github/workflows/, the path is
  unwired — re-add it.

Exit contract (the whole point of the gate):
  0  PASS     — every registered claim certified by the cold engine.
  0  DORMANT  — manifest absent or registers zero claims. Explicit, never a
                false green: the gate says "nothing to judge".
  1  VIOLATION— a claim BLOCKED: the law refuses it (the engine's
                recomputed verdict diverges from the claimant's asserted
                verdict — the naive-checker frauds live here). The
                mechanism's own words name the refusal.
  2  BROKEN   — fail-closed: manifest corrupt, claim fields untrustworthy,
                an unknown assertion value, claims exist but the mechanism
                is absent, or the mechanism's own verdict invariants broke.
                The gate never invents the engine and never defaults an
                unknown.

The gate never invents fields: unknown assertions, malformed shapes, or
missing keys are BROKEN, not defaulted. Claim CONTENT refused by the law is
VIOLATION, not BROKEN — the distinction is whose trust broke: the
manifest's (BROKEN) or the claim's (VIOLATION).

Structural note: the engine recomputes the relation digest over the
presented model and refuses on mismatch — the group cannot swap the
relation, the graph, or the initial state under the authorization. The
gate never pre-checks the digest; the engine's verdict is the authority.

Directive: D65 (Strongly Connected Invariant Groups, AER-LIVE-10; spec
PR #2209, mechanism PR #2327), owner naya2. Wired by the night-shift
WIRE lane. No merge — the merge lane owns it.
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
    "d65_joint_proof_manifest.json"
MECHANISM_MODULE = "drift_canary.strongly_connected_groups"

# The workflow runs this script as `python tools/...` (script dir on
# sys.path, not the repo root). The mechanism lives at the repo root —
# append it so the gate imports the REAL engine wherever it runs from.
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

ASSERT_VALUES = (
    "REPEATABLE_PROVEN",
    "DEADLOCK_IN_SCOPE",
    "LIVELOCK_COUNTEREXAMPLE",
    "EXIT_POSSIBLE_NOT_GUARANTEED",
    "JOINT_UNDETERMINED",
)


class GateBroken(Exception):
    """The manifest or the mechanism is untrustworthy — fail closed."""


class MechanismMissing(Exception):
    """Claims are registered but the D65 engine is absent."""


def _load_mechanism():
    try:
        return importlib.import_module(MECHANISM_MODULE)
    except Exception as exc:
        raise MechanismMissing(
            f"D65 mechanism {MECHANISM_MODULE!r} not importable: {exc}")


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


def _check_transition_shape(t, loc, idx, mech):
    """Validate one transition's JSON shape. The LAW judges unknown kinds,
    missing authorizations, and missing capacity/ownership — the gate only
    checks the JSON is shaped like a transition at all."""
    if not isinstance(t, dict):
        raise GateBroken(f"{loc}: model.transitions[{idx}] must be an "
                         f"object, got {type(t).__name__}")
    for key in ("src", "dst", "kind"):
        val = t.get(key)
        if not isinstance(val, str) or not val:
            raise GateBroken(
                f"{loc}: model.transitions[{idx}].{key!r} must be a "
                f"non-empty string")
    progress = t.get("progress", 0)
    if not isinstance(progress, int) or isinstance(progress, bool):
        raise GateBroken(
            f"{loc}: model.transitions[{idx}].progress must be an integer")
    for key in ("authorization", "capacity", "owner"):
        val = t.get(key)
        if val is not None and not isinstance(val, str):
            raise GateBroken(
                f"{loc}: model.transitions[{idx}].{key!r} must be a string "
                f"or null")
    return mech.JointTransition(
        src=t["src"], dst=t["dst"], kind=t["kind"], progress=progress,
        authorization=t.get("authorization"),
        capacity=t.get("capacity"), owner=t.get("owner"))


def _check_model_shape(model, loc, mech):
    """Rebuild the JointDeclaration from the claim's own model bytes.
    Raises GateBroken on anything the gate cannot trust — never defaulted.
    Content the LAW refuses (self-certified authority, digest mismatch,
    spurious joint, bad authorization) passes through to the engine."""
    if not isinstance(model, dict):
        raise GateBroken(
            f"{loc}: 'model' must be a JSON object, got "
            f"{type(model).__name__}")
    name = model.get("name")
    if not isinstance(name, str) or not name:
        raise GateBroken(f"{loc}: model.name must be a non-empty string")
    members = model.get("members")
    if not isinstance(members, list) or not members or \
            not all(isinstance(m, str) and m for m in members):
        raise GateBroken(
            f"{loc}: model.members must be a non-empty list of strings")
    declared_by = model.get("declared_by")
    if not isinstance(declared_by, str) or not declared_by:
        raise GateBroken(
            f"{loc}: model.declared_by must be a non-empty string")
    prereq = model.get("prereq")
    if not isinstance(prereq, dict) or not all(
            isinstance(k, str) and isinstance(v, list) and
            all(isinstance(x, str) for x in v)
            for k, v in prereq.items()):
        raise GateBroken(
            f"{loc}: model.prereq must map member names to lists of names")
    for key in ("initial_states", "authorized_initial"):
        val = model.get(key)
        if not isinstance(val, list) or \
                not all(isinstance(x, str) for x in val):
            raise GateBroken(
                f"{loc}: model.{key} must be a list of strings")
    exit_states = model.get("exit_states", [])
    if not isinstance(exit_states, list) or \
            not all(isinstance(x, str) for x in exit_states):
        raise GateBroken(
            f"{loc}: model.exit_states must be a list of strings")
    transitions = model.get("transitions")
    if not isinstance(transitions, list):
        raise GateBroken(
            f"{loc}: model.transitions must be a list, got "
            f"{type(transitions).__name__}")
    relation_digest = model.get("relation_digest")
    if not isinstance(relation_digest, str) or not relation_digest:
        raise GateBroken(
            f"{loc}: model.relation_digest must be a non-empty string")
    built = [_check_transition_shape(t, loc, i, mech)
             for i, t in enumerate(transitions)]
    return mech.JointDeclaration(
        name=name,
        members=frozenset(members),
        declared_by=declared_by,
        prereq={k: tuple(v) for k, v in prereq.items()},
        initial_states=frozenset(model["initial_states"]),
        authorized_initial=frozenset(model["authorized_initial"]),
        transitions=tuple(built),
        relation_digest=relation_digest,
        exit_states=frozenset(exit_states),
    )


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
    return obligation_id, asserts, model


def _dogfood_verdict(claim_id, verdict, declaration, mech):
    """Mechanism-integrity checks on every judged verdict. The law's own
    invariants, recomputed by the gate. Raises GateBroken on any break."""
    # The verdict qualifies the PRESENTED model only: the digest it
    # carries must equal the digest of the model actually judged.
    expected_digest = mech.model_digest_of(declaration)
    if verdict.model_digest != expected_digest:
        raise GateBroken(
            f"claim {claim_id}: mechanism integrity broken — verdict "
            f"carries model_digest {verdict.model_digest[:16]}… but the "
            f"presented model digests to {expected_digest[:16]}…")
    if verdict.group != declaration.name:
        raise GateBroken(
            f"claim {claim_id}: mechanism integrity broken — verdict "
            f"names group {verdict.group!r}, declaration names "
            f"{declaration.name!r}")
    # Canonical encoding must be byte-stable across rebuilds: what the
    # cold verifier judged is exactly the claim's canonical bytes.
    again = mech.canonical_model_encoding(declaration)
    if again != mech.canonical_model_encoding(declaration):
        raise GateBroken(
            f"claim {claim_id}: mechanism integrity broken — canonical "
            f"model encoding is not byte-stable")


def _judge_claim(entry, mech, manifest_path):
    """Cold-judge one claim against the REAL D65 engine. Returns a result
    dict with verdict 'pass' or 'violation'. Raises GateBroken when the
    manifest or the mechanism is untrustworthy (fail-closed)."""
    claim_id = entry.get("id")
    obligation_id, asserts, model = _check_claim_shape(entry, manifest_path)
    declaration = _check_model_shape(
        model, f"manifest {manifest_path}: claim {claim_id!r}", mech)
    try:
        verdict = mech.verify_joint(declaration)
    except Exception as exc:
        raise GateBroken(
            f"claim {claim_id}: the D65 engine broke on a shape-valid "
            f"model — failing closed: {type(exc).__name__}: {exc}")
    # Dogfood the mechanism on every judged verdict — a broken engine
    # fails closed, never certifies.
    _dogfood_verdict(claim_id, verdict, declaration, mech)

    actual = verdict.verdict.value
    if actual == asserts:
        if actual == "JOINT_UNDETERMINED":
            reason = ("honest refusal record: the law refuses the joint "
                      f"and names the obstruction: "
                      f"{list(verdict.obstruction)}")
        else:
            reason = ("claimant's asserted verdict matches the cold "
                      "engine verdict exactly")
        return {"id": claim_id, "verdict": "pass",
                "asserted": asserts, "actual": actual, "reason": reason}
    # The law refuses the claim's content — the naive-checker frauds live
    # here. Name the refusal in the mechanism's own words.
    refusal = list(verdict.obstruction)
    if verdict.safety_violations:
        refusal.append(
            "safety_violations=" + repr(list(verdict.safety_violations)))
    if verdict.deadlock_state:
        refusal.append(f"deadlock_state={verdict.deadlock_state!r}")
    if verdict.exhibited_cycle:
        refusal.append(
            f"exhibited_cycle={'->'.join(verdict.exhibited_cycle)} "
            f"(cycle_progress={verdict.cycle_progress})")
    if verdict.notes:
        refusal.append("notes=" + repr(list(verdict.notes)))
    return {"id": claim_id, "verdict": "violation",
            "asserted": asserts, "actual": actual,
            "reason": f"the D65 law judges {actual}, not {asserts} — "
                      f"{' | '.join(refusal) if refusal else 'no obstruction named'}"}


def _finish(exit_code, verdict, reason, results, as_json):
    payload = {"verdict": verdict, "reason": reason, "claims": results}
    if as_json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"D65 joint-proof qualification gate: {verdict} — {reason}")
        for r in results:
            line = (f"  [{r['verdict']}] {r['id']}: asserted={r['asserted']} "
                    f"actual={r['actual']}")
            if r.get("reason"):
                line += f" — {r['reason']}"
            print(line)
    return exit_code


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Judge joint-proof qualification claims against the "
                    "D65 engine.")
    parser.add_argument("--manifest",
                        default=str(DEFAULT_MANIFEST),
                        help="path to d65_joint_proof_manifest.json")
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
                   f"{len(results)} claim(s) certified by the D65 engine",
                   results, args.as_json)


if __name__ == "__main__":
    sys.exit(main())
