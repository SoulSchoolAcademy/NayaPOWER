#!/usr/bin/env python3
"""D22 liveness-claims gate — wire the canonical liveness seam onto the
governance path.

The D22 mechanism is the canonical seam `drift_canary/liveness.py` on main
(SPEC + deterministic machinery: assess_liveness, detect_deadlock,
detect_livelock, detect_starvation, is_genuine_progress, LivenessObligation,
LivenessReceipt, and the hard rules — liveness never creates permission,
WAITING_AUTHORITY only leaves via real authorization, no invented progress,
refusal/escalation are not completion). It is CODE-ONLY: zero workflows
reference it. This gate puts it on a live operating path: every liveness
claim registered in `tools/d22_liveness_claims_manifest.json` is judged by
the REAL mechanism, on the claim's declared evidence. A claim whose declared
verdict disagrees with the prover is BLOCKED.

Boundary (from the mechanism's own docstring): this wires D22 onto the CI
governance path only. Wiring liveness into kernel/, KNOW, LAW, ACT, or any
runtime path still needs Shawn's word. The gate enforces the subordination —
it judges claims, it authorizes nothing, and liveness can never create
permission through it.

Exit contract (the whole point of the gate):
  0  PASS     — every registered claim certified honest by the prover.
  0  DORMANT  — manifest registers zero claims. Explicit, never a false
                green: the gate says "nothing to judge".
  1  VIOLATION— a claim misstates a liveness verdict (QUALIFIED asserted on
                deadlocked / livelocked / starved / witness-bare evidence;
                honest NOT_QUALIFIED misreported as QUALIFIED, etc.).
  2  BROKEN   — fail-closed: manifest corrupt, claim fields unparseable or
                outside the mechanism's vocabulary, or claims exist but the
                mechanism is absent/neutered (the gate refuses to certify on
                defaults — it never invents the prover).

The gate never invents fields: unknown liveness types, states, fairness
assumptions, or claim verdicts are BROKEN, not defaulted. wait_for values
must be lists (a bare string would iterate as characters — fail-closed).

Directive: D22 (Multi-Node Liveness & Guaranteed Progress), owner naya2.
Wired by the night-shift WIRE lane. No merge — Shawn pulls triggers.
"""

from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOLS_DIR.parent
DEFAULT_MANIFEST = TOOLS_DIR / "d22_liveness_claims_manifest.json"

EXIT_PASS = 0
EXIT_VIOLATION = 1
EXIT_BROKEN = 2

CLAIMED_OVERALL_VALUES = ("QUALIFIED", "NOT_QUALIFIED")
TYPE_VERDICT_KEYS = ("DISPOSITION", "WORKFLOW_PROGRESS", "TASK_COMPLETION")
TYPE_VERDICT_VALUES = ("HOLDS", "VIOLATED", "INCOMPLETE")

REQUIRED_OBLIGATION_KEYS = frozenset({
    "obligation_id", "revision", "liveness_type", "participants",
    "trigger", "progress_target",
})
REQUIRED_EVIDENCE_KEYS = frozenset({
    "states", "wait_for", "escape_paths", "histories", "progress_seqs",
    "eligible_since", "opportunities", "scheduled_others",
    "fairness_holds", "witnesses",
})
REQUIRED_CLAIM_KEYS = frozenset({"id", "obligation", "evidence", "claimed_overall"})


class GateBroken(Exception):
    """Fail-closed: the gate cannot trust its inputs. Exit 2."""


class MechanismMissing(Exception):
    """The D22 mechanism is absent or neutered. Exit 2 when claims exist."""


def _load_mechanism():
    """Import the REAL D22 mechanism from this repo tree.

    Never synthesized, never defaulted. Verifies the module came from the
    checked-out tree (live bytes) and exposes the required API surface, so
    a neutered module cannot silently pass as the mechanism.
    """
    pkg_dir = REPO_ROOT / "drift_canary"
    mech_file = pkg_dir / "liveness.py"
    if not mech_file.is_file():
        raise MechanismMissing(f"mechanism not present: {mech_file}")
    sys.path.insert(0, str(REPO_ROOT))
    try:
        mod = importlib.import_module("drift_canary.liveness")
    except Exception as exc:
        raise MechanismMissing(f"mechanism failed to import: {exc}")
    finally:
        try:
            sys.path.remove(str(REPO_ROOT))
        except ValueError:
            pass
    loaded = Path(getattr(mod, "__file__", "") or "").resolve()
    if pkg_dir.resolve() not in loaded.parents:
        raise MechanismMissing(
            f"mechanism loaded from outside the tree: {loaded}")
    for attr in ("assess_liveness", "LivenessObligation", "WorkflowState",
                 "ProgressWitness", "LIVENESS_TYPES", "WORKFLOW_STATES",
                 "FAIRNESS_ASSUMPTIONS", "NON_PROGRESS_EVENTS"):
        if not hasattr(mod, attr):
            raise MechanismMissing(
                f"mechanism missing required API: {attr}")
    return mod


def _load_manifest(path):
    """Load the claims manifest. Returns None when the file is absent."""
    p = Path(path)
    if not p.is_file():
        return None
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        raise GateBroken(f"manifest is not valid JSON: {exc}")
    if not isinstance(data, dict) or not isinstance(data.get("claims"), list):
        raise GateBroken("manifest must be an object with a 'claims' list")
    if not isinstance(data.get("version"), int):
        raise GateBroken("manifest must carry an integer 'version'")
    seen = set()
    for entry in data["claims"]:
        if not isinstance(entry, dict):
            raise GateBroken("every claim must be an object")
        missing = REQUIRED_CLAIM_KEYS - set(entry.keys())
        if missing:
            raise GateBroken(f"claim missing required keys: {sorted(missing)}")
        cid = entry["id"]
        if not isinstance(cid, str) or not cid:
            raise GateBroken("claim id must be a non-empty string")
        if cid in seen:
            raise GateBroken(f"duplicate claim id: {cid!r}")
        seen.add(cid)
    return data


def _as_str_list(value, what):
    if not isinstance(value, list) or not all(
            isinstance(v, str) for v in value):
        raise GateBroken(f"{what} must be a list of strings")
    return tuple(value)


def _as_int(value, what, minimum=None):
    if isinstance(value, bool) or not isinstance(value, int):
        raise GateBroken(f"{what} must be an integer, got {value!r}")
    if minimum is not None and value < minimum:
        raise GateBroken(f"{what} must be >= {minimum}, got {value!r}")
    return value


def _build_obligation(raw, mech):
    if not isinstance(raw, dict):
        raise GateBroken("claim obligation must be an object")
    missing = REQUIRED_OBLIGATION_KEYS - set(raw.keys())
    if missing:
        raise GateBroken(
            f"obligation missing required keys: {sorted(missing)}")
    liveness_type = raw["liveness_type"]
    if liveness_type not in mech.LIVENESS_TYPES:
        raise GateBroken(
            f"unknown liveness_type {liveness_type!r}; vocabulary is "
            f"{list(mech.LIVENESS_TYPES)} (never defaulted)")
    assumptions = _as_str_list(
        raw.get("fairness_assumptions", []), "fairness_assumptions")
    for a in assumptions:
        if a not in mech.FAIRNESS_ASSUMPTIONS:
            raise GateBroken(
                f"unknown fairness_assumption {a!r}; vocabulary is "
                f"{list(mech.FAIRNESS_ASSUMPTIONS)} (never defaulted)")
    participants = _as_str_list(raw["participants"], "participants")
    if not participants:
        raise GateBroken("a liveness obligation needs participants")
    for key in ("obligation_id", "revision", "trigger", "progress_target"):
        if not isinstance(raw[key], str) or not raw[key]:
            raise GateBroken(f"obligation.{key} must be a non-empty string")
    dep_graph = raw.get("dependency_graph", [])
    if not isinstance(dep_graph, list) or not all(
            isinstance(p, list) and len(p) == 2
            and all(isinstance(x, str) for x in p) for p in dep_graph):
        raise GateBroken("dependency_graph must be a list of [a, b] pairs")
    deadline_policy = raw.get("deadline_policy", [])
    if not isinstance(deadline_policy, list):
        raise GateBroken("deadline_policy must be a list (never defaulted)")
    witnesses_req = _as_str_list(
        raw.get("progress_witnesses", []), "progress_witnesses")
    try:
        return mech.LivenessObligation(
            obligation_id=raw["obligation_id"],
            revision=raw["revision"],
            liveness_type=liveness_type,
            participants=participants,
            trigger=raw["trigger"],
            progress_target=raw["progress_target"],
            dependency_graph=tuple(tuple(p) for p in dep_graph),
            enabled_conditions=_as_str_list(
                raw.get("enabled_conditions", []), "enabled_conditions"),
            fairness_assumptions=assumptions,
            progress_witnesses=witnesses_req,
            deadline_policy=tuple(deadline_policy),
            recovery_policy=_as_str_list(
                raw.get("recovery_policy", []), "recovery_policy"),
            external_blockers=_as_str_list(
                raw.get("external_blockers", []), "external_blockers"),
            supersedes=raw.get("supersedes", ""),
        )
    except AssertionError as exc:
        raise GateBroken(f"obligation rejected by the mechanism: {exc}")


def _build_evidence(raw, mech):
    if not isinstance(raw, dict):
        raise GateBroken("claim evidence must be an object")
    missing = REQUIRED_EVIDENCE_KEYS - set(raw.keys())
    if missing:
        raise GateBroken(f"evidence missing required keys: {sorted(missing)}")

    states_raw = raw["states"]
    if not isinstance(states_raw, dict) or not states_raw:
        raise GateBroken("evidence.states must be a non-empty object")
    states = {}
    for wf, s in states_raw.items():
        if not isinstance(s, dict):
            raise GateBroken(f"states[{wf!r}] must be an object")
        state_name = s.get("state")
        if state_name not in mech.WORKFLOW_STATES:
            raise GateBroken(
                f"states[{wf!r}].state {state_name!r} unknown; vocabulary is "
                f"{list(mech.WORKFLOW_STATES)} (never defaulted)")
        note = s.get("note", "")
        if not isinstance(note, str):
            raise GateBroken(f"states[{wf!r}].note must be a string")
        try:
            states[wf] = mech.WorkflowState(
                workflow_id=wf, state=state_name,
                since_seq=_as_int(s.get("since_seq", 0),
                                  f"states[{wf!r}].since_seq", minimum=0),
                note=note,
            )
        except AssertionError as exc:
            raise GateBroken(f"states[{wf!r}] rejected: {exc}")

    def _wf_map(key, value_kind):
        m = raw[key]
        if not isinstance(m, dict):
            raise GateBroken(f"evidence.{key} must be an object")
        for wf in m:
            if wf not in states:
                raise GateBroken(
                    f"evidence.{key} references unknown workflow {wf!r}; "
                    f"every workflow needs a states entry (never invented)")
        return m

    wait_for = _wf_map("wait_for", "targets")
    for wf, targets in wait_for.items():
        if not isinstance(targets, list) or not all(
                isinstance(t, str) for t in targets):
            raise GateBroken(
                f"evidence.wait_for[{wf!r}] must be a list of workflow ids "
                f"(a bare string would iterate as characters — fail-closed)")
        for t in targets:
            if t not in states:
                raise GateBroken(
                    f"evidence.wait_for[{wf!r}] targets unknown workflow "
                    f"{t!r} (never invented)")

    escape_paths = _wf_map("escape_paths", "escapes")
    for wf, escapes in escape_paths.items():
        _as_str_list(escapes, f"evidence.escape_paths[{wf!r}]")

    histories = _wf_map("histories", "history")
    parsed_histories = {}
    for wf, hist in histories.items():
        if not isinstance(hist, list):
            raise GateBroken(f"evidence.histories[{wf!r}] must be a list")
        pairs = []
        for entry in hist:
            if not isinstance(entry, list) or len(entry) != 2:
                raise GateBroken(
                    f"evidence.histories[{wf!r}] entries must be [seq, state]")
            seq = _as_int(entry[0], f"evidence.histories[{wf!r}] seq",
                          minimum=0)
            if entry[1] not in mech.WORKFLOW_STATES:
                raise GateBroken(
                    f"evidence.histories[{wf!r}] unknown state {entry[1]!r}")
            pairs.append((seq, entry[1]))
        parsed_histories[wf] = tuple(pairs)

    def _int_map(key, minimum):
        m = _wf_map(key, "counts")
        out = {}
        for wf, v in m.items():
            out[wf] = _as_int(v, f"evidence.{key}[{wf!r}]", minimum=minimum)
        return out

    progress_seqs = _wf_map("progress_seqs", "seqs")
    parsed_progress = {}
    for wf, seqs in progress_seqs.items():
        if not isinstance(seqs, list):
            raise GateBroken(f"evidence.progress_seqs[{wf!r}] must be a list")
        parsed_progress[wf] = tuple(
            _as_int(s, f"evidence.progress_seqs[{wf!r}]", minimum=0)
            for s in seqs)

    eligible_since = _int_map("eligible_since", 0)
    opportunities = _int_map("opportunities", 0)
    scheduled_others = _int_map("scheduled_others", 0)

    fairness_holds = raw["fairness_holds"]
    if not isinstance(fairness_holds, bool):
        raise GateBroken("evidence.fairness_holds must be true/false "
                         "(never defaulted)")

    witnesses_raw = raw["witnesses"]
    if not isinstance(witnesses_raw, list):
        raise GateBroken("evidence.witnesses must be a list")
    witnesses = []
    for i, w in enumerate(witnesses_raw):
        if not isinstance(w, dict):
            raise GateBroken(f"evidence.witnesses[{i}] must be an object")
        for key in ("workflow_id", "node", "milestone", "evidence_ref"):
            if not isinstance(w.get(key), str) or not w.get(key):
                raise GateBroken(
                    f"evidence.witnesses[{i}].{key} must be a non-empty string")
        if w["workflow_id"] not in states:
            raise GateBroken(
                f"evidence.witnesses[{i}] references unknown workflow "
                f"{w['workflow_id']!r} (never invented)")
        delta = w.get("obligation_delta", "")
        if not isinstance(delta, str):
            raise GateBroken(
                f"evidence.witnesses[{i}].obligation_delta must be a string")
        try:
            witnesses.append(mech.ProgressWitness(
                workflow_id=w["workflow_id"], node=w["node"],
                milestone=w["milestone"], evidence_ref=w["evidence_ref"],
                seq=_as_int(w.get("seq", 0),
                            f"evidence.witnesses[{i}].seq", minimum=0),
                obligation_delta=delta,
            ))
        except AssertionError as exc:
            raise GateBroken(f"evidence.witnesses[{i}] rejected: {exc}")

    return {
        "states": states,
        "wait_for": {w: list(v) for w, v in wait_for.items()},
        "escape_paths": {w: list(v) for w, v in escape_paths.items()},
        "histories": parsed_histories,
        "progress_seqs": parsed_progress,
        "eligible_since": eligible_since,
        "opportunities": opportunities,
        "scheduled_others": scheduled_others,
        "fairness_holds": fairness_holds,
        "witnesses": tuple(witnesses),
    }


def _judge_claim(claim, mech):
    """Judge one claim against the real mechanism.

    Returns (verdict, detail) with verdict in PASS/VIOLATION.
    Raises GateBroken on untrustworthy inputs (caller maps to exit 2).
    """
    cid = claim["id"]
    claimed = claim["claimed_overall"]
    if claimed not in CLAIMED_OVERALL_VALUES:
        raise GateBroken(
            f"claim {cid!r}: claimed_overall {claimed!r} unknown; vocabulary "
            f"is {list(CLAIMED_OVERALL_VALUES)} (never defaulted)")
    obligation = _build_obligation(claim["obligation"], mech)
    ev = _build_evidence(claim["evidence"], mech)
    result = mech.assess_liveness(
        obligation, ev["states"], ev["wait_for"], ev["escape_paths"],
        ev["histories"], ev["progress_seqs"], ev["eligible_since"],
        ev["opportunities"], ev["scheduled_others"], ev["fairness_holds"],
        ev["witnesses"])
    actual = result["overall"]
    problems = []
    if claimed != actual:
        problems.append(
            f"claimed_overall={claimed} but the prover says {actual}")
    claimed_types = claim.get("claimed_type_verdicts")
    if claimed_types is not None:
        if not isinstance(claimed_types, dict):
            raise GateBroken(
                f"claim {cid!r}: claimed_type_verdicts must be an object")
        for key, value in claimed_types.items():
            if key not in TYPE_VERDICT_KEYS:
                raise GateBroken(
                    f"claim {cid!r}: unknown type-verdict key {key!r}")
            if value not in TYPE_VERDICT_VALUES:
                raise GateBroken(
                    f"claim {cid!r}: unknown type-verdict value {value!r}")
            actual_v = result["type_verdicts"][key]
            if value != actual_v:
                problems.append(
                    f"claimed_type_verdicts[{key}]={value} but the prover "
                    f"says {actual_v}")
    if problems:
        detail = "; ".join(problems)
        detail += (f" | prover overall={actual}, "
                   f"type_verdicts={result['type_verdicts']}, "
                   f"failures={result['failures']}, "
                   f"deadlock={result['deadlock'][0]}, "
                   f"livelock={result['livelock'][0]}, "
                   f"starvation={result['starvation'][0]}")
        return "VIOLATION", detail
    return "PASS", (f"prover overall={actual}, "
                    f"type_verdicts={result['type_verdicts']}")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="D22 liveness-claims gate: judge registered claims "
                    "against the real drift_canary.liveness mechanism.")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST),
                        help="path to the claims manifest JSON")
    args = parser.parse_args(argv)

    try:
        manifest = _load_manifest(args.manifest)
    except GateBroken as exc:
        print(f"D22-GATE BROKEN: {exc}")
        return EXIT_BROKEN

    if manifest is None:
        print("D22-GATE DORMANT: no manifest present; nothing to judge "
              "(not a green — a stated absence of coverage)")
        return EXIT_PASS

    claims = manifest["claims"]
    if not claims:
        print("D22-GATE DORMANT: manifest registers zero claims; nothing "
              "to judge (not a green — a stated absence of coverage)")
        return EXIT_PASS

    try:
        mech = _load_mechanism()
    except MechanismMissing as exc:
        print(f"D22-GATE BROKEN: {exc} (fail-closed: claims exist but the "
              f"mechanism cannot be proven present)")
        return EXIT_BROKEN

    violations = []
    broken = []
    passed = 0
    for claim in claims:
        cid = claim["id"]
        try:
            verdict, detail = _judge_claim(claim, mech)
        except GateBroken as exc:
            broken.append((cid, str(exc)))
            continue
        if verdict == "VIOLATION":
            violations.append((cid, detail))
        else:
            passed += 1
            print(f"D22-GATE PASS: claim {cid!r} honest — {detail}")

    if broken:
        for cid, detail in broken:
            print(f"D22-GATE BROKEN: claim {cid!r}: {detail}")
        print(f"D22-GATE BROKEN: {len(broken)} claim(s) unjudgeable; "
              f"{passed} passed, {len(violations)} violation(s). "
              f"Fail-closed: fix the manifest, do not ship the claims.")
        return EXIT_BROKEN

    if violations:
        for cid, detail in violations:
            print(f"D22-GATE VIOLATION: claim {cid!r}: {detail}")
        print(f"D22-GATE VIOLATION: {len(violations)} dishonest claim(s) "
              f"BLOCKED; {passed} passed. The prover disagrees — the claim "
              f"must be corrected or its evidence repaired.")
        return EXIT_VIOLATION

    print(f"D22-GATE PASS: {passed}/{len(claims)} registered claim(s) "
          f"certified honest by drift_canary.liveness")
    return EXIT_PASS


if __name__ == "__main__":
    sys.exit(main())