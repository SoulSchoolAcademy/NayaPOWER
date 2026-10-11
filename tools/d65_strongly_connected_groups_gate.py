#!/usr/bin/env python3
"""D65 strongly-connected invariant groups gate — wire the joint-proof verifier onto the CI path.

The D65 engine (drift_canary/strongly_connected_groups.py, PR #2327) verifies
a cyclically-dependent invariant group as ONE joint proof obligation: it
collapses the cycle into a single state-transition system, grounds it in
authoritative initial state, and COMPUTES reachability, safety closure,
repeatability (greatest fixed point), progress (maximum-mean-cycle) and exit
viability from the presented complete legal transition relation. It never
accepts pre-computed booleans — the spec's naive checker (PR #2209) is kept
in-module as the defective baseline and is never used.

This gate puts that mechanism on a live operating path: every joint-proof
claim registered in tools/d65_strongly_connected_groups_manifest.json is
judged by the REAL engine, rebuilt from the claim's declared evidence. A
claim that launders a joint proof — asserting REPEATABLE_PROVEN where the
engine exhibits a zero-progress cycle, swallowing the exit dimension the
engine keeps separate, or asserting grounded where the engine refuses
(authority is a member, digest mismatch, no authorized initial) — is BLOCKED.

Exit contract (the whole point of the gate):
  0  PASS     — every registered claim certified by the engine.
  0  DORMANT  — manifest absent or registers zero claims. Explicit, never a
                false green: the gate says "nothing to judge".
  1  VIOLATION— asserted verdict != engine verdict: joint-proof laundering.
                The engine's obstruction is named, never swallowed.
  2  BROKEN   — fail-closed: manifest corrupt, claim fields unparseable,
                unknown asserted verdict / transition kind (never defaulted),
                claims exist but the mechanism is absent (the gate refuses to
                certify on defaults — it never invents the engine), or the
                engine raised instead of judging.

The gate never invents fields: unknown verdicts, kinds, or member names are
BROKEN, not defaulted. A tampered model is judgeable: a claim may present a
`presented_digest`; the gate passes it through untouched, the engine refuses
on mismatch, and only an asserted JOINT_UNDETERMINED is certified for it.

Directive: D65 (Strongly Connected Invariant Groups and Joint Proof
Qualification, AER-LIVE-10), owner naya2 (build lane). Wired by the
night-shift WIRE lane. No merge — Shawn pulls triggers.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOLS_DIR.parent
DEFAULT_MANIFEST = TOOLS_DIR / "d65_strongly_connected_groups_manifest.json"

# The mechanism lives in the drift_canary package at the repo root. The
# workflow runs this script as `python tools/...` (script dir on sys.path,
# not the repo root), so the root is appended explicitly. Appended — not
# prepended — so a test/battery overlay earlier on sys.path (or PYTHONPATH)
# keeps winning; the repo root is the fallback, never an override.
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

EXIT_PASS = 0
EXIT_VIOLATION = 1
EXIT_BROKEN = 2

REQUIRED_CLAIM_KEYS = frozenset(
    {"id", "joint_name", "asserted_verdict", "declared_by", "members",
     "prereq", "initial_states", "authorized_initial", "transitions",
     "exit_states"})

EXPECTED_VERDICTS = frozenset(
    {"REPEATABLE_PROVEN", "DEADLOCK_IN_SCOPE", "LIVELOCK_COUNTEREXAMPLE",
     "EXIT_POSSIBLE_NOT_GUARANTEED", "JOINT_UNDETERMINED"})

_HEX64 = re.compile(r"^[0-9a-f]{64}$")


class GateBroken(Exception):
    """Fail-closed: the gate cannot trust its inputs. Exit 2."""


class MechanismMissing(Exception):
    """The D65 engine is absent. Exit 2 when claims exist, else DORMANT."""


def _load_mechanism():
    """Import the REAL D65 engine.

    Never synthesized, never defaulted. Verifies the required API surface
    so a neutered module cannot silently pass as the mechanism.
    """
    try:
        import drift_canary.strongly_connected_groups as d65
    except ImportError as exc:
        raise MechanismMissing(
            f"D65 mechanism not importable: {exc}")
    for attr in ("verify_joint", "make_declaration", "JointDeclaration",
                 "JointTransition", "Verdict", "KINDS"):
        if not hasattr(d65, attr):
            raise MechanismMissing(
                f"mechanism missing required API: {attr}")
    try:
        verdict_values = {m.value for m in d65.Verdict}
    except Exception as exc:
        raise MechanismMissing(f"mechanism Verdict not enumerable: {exc}")
    if verdict_values != EXPECTED_VERDICTS:
        raise MechanismMissing(
            f"mechanism Verdict surface wrong: {sorted(verdict_values)} "
            f"(expected {sorted(EXPECTED_VERDICTS)}) — a neutered engine "
            "cannot certify joint proofs")
    if not isinstance(d65.KINDS, (tuple, list)) or not d65.KINDS:
        raise MechanismMissing("mechanism KINDS missing or empty")
    return d65


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


def _as_nonempty_str(value, what):
    if not isinstance(value, str) or not value.strip():
        raise GateBroken(f"{what} must be a non-empty string, "
                         f"got {value!r} (never defaulted)")
    return value


def _as_int(value, what):
    if isinstance(value, bool) or not isinstance(value, int):
        raise GateBroken(f"{what} must be an integer, got {value!r} "
                         "(never defaulted)")
    return value


def _as_name_list(raw, what, claim_id, allow_empty=False):
    if not isinstance(raw, list) or (not raw and not allow_empty):
        raise GateBroken(
            f"claim {claim_id}: {what} must be a "
            f"{'possibly-empty' if allow_empty else 'non-empty'} list")
    names = []
    for i, n in enumerate(raw):
        _as_nonempty_str(n, f"claim {claim_id} {what}[{i}]")
        names.append(n)
    if len(set(names)) != len(names):
        raise GateBroken(f"claim {claim_id}: {what} has duplicate names")
    return names


def _parse_transitions(raw, d65, claim_id):
    if not isinstance(raw, list) or not raw:
        raise GateBroken(
            f"claim {claim_id}: transitions must be a non-empty list")
    kinds = set(d65.KINDS)
    out = []
    for i, t in enumerate(raw):
        if not isinstance(t, dict):
            raise GateBroken(f"claim {claim_id} transition {i}: must be an object")
        src = _as_nonempty_str(t.get("src"), f"claim {claim_id} transition {i} src")
        dst = _as_nonempty_str(t.get("dst"), f"claim {claim_id} transition {i} dst")
        kind = t.get("kind")
        if kind not in kinds:
            raise GateBroken(
                f"claim {claim_id} transition {i}: unknown kind {kind!r} "
                f"(expected one of {sorted(kinds)}; never defaulted)")
        progress = _as_int(t.get("progress"),
                           f"claim {claim_id} transition {i} progress")
        kw = {}
        for opt in ("authorization", "capacity", "owner"):
            v = t.get(opt)
            if v is not None:
                kw[opt] = _as_nonempty_str(
                    v, f"claim {claim_id} transition {i} {opt}")
        try:
            out.append(d65.JointTransition(src=src, dst=dst, kind=kind,
                                           progress=progress, **kw))
        except (TypeError, ValueError, AssertionError) as exc:
            raise GateBroken(
                f"claim {claim_id} transition {i}: rejected by the mechanism: {exc}")
    return tuple(out)


def _laundering_pattern(asserted, actual, obstruction):
    """Name the defect class when the mismatch matches a known shape."""
    obs = "; ".join(obstruction) if obstruction else "no obstruction named"
    if asserted == "REPEATABLE_PROVEN" and actual == "LIVELOCK_COUNTEREXAMPLE":
        return ("progress-laundering: the claim certifies a repeatable joint "
                "proof where the engine exhibits a zero-progress cycle — "
                "repeatability of motion is not repeatability of progress")
    if asserted == "REPEATABLE_PROVEN" and actual == "EXIT_POSSIBLE_NOT_GUARANTEED":
        return ("exit-swallowing: the claim collapses the exit dimension the "
                "engine keeps separate — an escape path existing is not the "
                "same as the joint cycle being closed")
    if asserted != "JOINT_UNDETERMINED" and actual == "JOINT_UNDETERMINED":
        return ("grounding-laundering: the engine refuses the joint proof "
                f"({obs}) — the claim asserts a verdict the presented model "
                "cannot ground")
    if asserted == "JOINT_UNDETERMINED" and actual != "JOINT_UNDETERMINED":
        return ("refusal-laundering: the engine certifies the joint proof "
                f"({actual}) — asserting refusal where the model grounds is "
                "manufactured doubt")
    return ""


def judge_claim(claim, d65):
    """Judge one claim against the real joint-proof verifier. Returns a result dict."""
    claim_id = claim["id"]
    joint_name = _as_nonempty_str(claim["joint_name"],
                                  f"claim {claim_id} joint_name")
    asserted = claim["asserted_verdict"]
    if asserted not in EXPECTED_VERDICTS:
        raise GateBroken(
            f"claim {claim_id}: unknown asserted_verdict {asserted!r} "
            f"(expected one of {sorted(EXPECTED_VERDICTS)}; never defaulted)")
    declared_by = _as_nonempty_str(claim["declared_by"],
                                   f"claim {claim_id} declared_by")
    members = _as_name_list(claim["members"], "members", claim_id)

    prereq_raw = claim["prereq"]
    if not isinstance(prereq_raw, dict):
        raise GateBroken(f"claim {claim_id}: prereq must be an object")
    member_set = set(members)
    prereq = {}
    for k, v in prereq_raw.items():
        _as_nonempty_str(k, f"claim {claim_id} prereq key")
        if k not in member_set:
            raise GateBroken(
                f"claim {claim_id}: prereq key {k!r} is not a member "
                "(the joint's internal topology only; never defaulted)")
        deps = _as_name_list(v, f"prereq[{k}]", claim_id, allow_empty=True)
        for d in deps:
            if d not in member_set:
                raise GateBroken(
                    f"claim {claim_id}: prereq[{k}] dependency {d!r} is not "
                    "a member (never defaulted)")
        prereq[k] = tuple(deps)

    initial_states = _as_name_list(claim["initial_states"], "initial_states",
                                   claim_id)
    authorized_initial = _as_name_list(claim["authorized_initial"],
                                       "authorized_initial", claim_id,
                                       allow_empty=True)
    exit_states = _as_name_list(claim["exit_states"], "exit_states",
                                claim_id, allow_empty=True)
    transitions = _parse_transitions(claim["transitions"], d65, claim_id)

    presented_digest = claim.get("presented_digest")
    if presented_digest is not None:
        if not isinstance(presented_digest, str) or not _HEX64.match(presented_digest):
            raise GateBroken(
                f"claim {claim_id}: presented_digest must be a 64-hex-char "
                f"sha256, got {presented_digest!r} (never defaulted)")

    try:
        decl = d65.make_declaration(
            name=joint_name,
            members=members,
            declared_by=declared_by,
            prereq=prereq,
            initial_states=initial_states,
            authorized_initial=authorized_initial,
            transitions=transitions,
            exit_states=exit_states,
        )
    except (TypeError, ValueError, AssertionError) as exc:
        raise GateBroken(
            f"claim {claim_id}: declaration rejected by the mechanism: {exc}")

    if presented_digest is not None:
        # Tamper path: the presented digest is passed through untouched.
        # The engine recomputes and refuses on mismatch; only an asserted
        # JOINT_UNDETERMINED can be certified for it.
        try:
            decl = d65.JointDeclaration(
                **{**decl.__dict__, "relation_digest": presented_digest})
        except (TypeError, ValueError) as exc:
            raise GateBroken(
                f"claim {claim_id}: digest override rejected: {exc}")

    try:
        result = d65.verify_joint(decl)
    except Exception as exc:
        # The engine judges; it does not raise. An exception is an
        # unjudgeable claim — fail closed, never passed.
        raise GateBroken(
            f"claim {claim_id}: engine raised instead of judging: "
            f"{type(exc).__name__}: {exc}")

    verdict = result.verdict
    actual = verdict.value if hasattr(verdict, "value") else str(verdict)
    obstruction = [str(o) for o in (result.obstruction or ())]
    model_digest = str(getattr(result, "model_digest", ""))

    out = {
        "id": claim_id,
        "joint_name": joint_name,
        "asserted": asserted,
        "actual": actual,
        "model_digest": model_digest,
        "obstruction": obstruction,
    }
    if actual != asserted:
        out["verdict"] = "violation"
        out["reason"] = (
            _laundering_pattern(asserted, actual, obstruction)
            or f"verdict mismatch: asserted {asserted}, engine finds "
               f"{actual} (obstruction: {obs if (obs := '; '.join(obstruction)) else 'none'})")
        return out
    out["verdict"] = "certified"
    return out


def _finish(exit_code, verdict, reason, results, as_json):
    payload = {"verdict": verdict, "reason": reason, "claims": results}
    if as_json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"D65 strongly-connected groups gate: {verdict} — {reason}")
        for r in results:
            line = (f"  [{r['verdict']}] {r['id']} ({r['joint_name']}): "
                    f"asserted={r['asserted']} actual={r['actual']}")
            if r.get("obstruction"):
                line += f" obstruction={r['obstruction']}"
            if r.get("reason"):
                line += f" — {r['reason']}"
            print(line)
    return exit_code


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Judge joint-proof claims against the D65 engine.")
    parser.add_argument("--manifest",
                        default=str(DEFAULT_MANIFEST),
                        help="path to d65_strongly_connected_groups_manifest.json")
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
        d65 = _load_mechanism()
    except MechanismMissing as exc:
        return _finish(EXIT_BROKEN, "BROKEN",
                       f"{exc}: {len(claims)} claim(s) registered but cannot "
                       "be certified — refusing to pass on defaults",
                       [], args.as_json)
    results = []
    try:
        for entry in claims:
            results.append(judge_claim(entry, d65))
    except GateBroken as exc:
        return _finish(EXIT_BROKEN, "BROKEN", str(exc), results, args.as_json)
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
