#!/usr/bin/env python3
"""Progress & fairness claims gate — wire the canonical D23/D24/D25 seams
onto the governance path.

The mechanisms are the canonical seams on main (SPEC + deterministic
machinery, CODE-ONLY per their own docstrings and the Gate-7 registry
#2330 SP-010…SP-012):
  D23  drift_canary/progress.py        — what counts as real progress
       (classify_transition, TRANSITION_KINDS; the hard rules: heartbeats,
       log lines, bare retries, reassignments earn NO proof-progress credit;
       escalation transfers responsibility, it never completes the
       original objective; proof/termination progress are COMPUTED, never
       supplied by the agent).
  D24  drift_canary/fairness.py        — fairness and progress are two
       separate proofs (assess_three_truths, compose_conditional_liveness;
       the service ladder; adequate service requires reconstructable
       evidence; DISPATCHED without usable resources is not service;
       fairness debt is never part of the proof-completion score).
  D25  drift_canary/strong_fairness.py — when strong fairness is required
       (recommend_standard, check_assumptions, assumptions_satisfied;
       weak fairness permits indefinite postponement of intermittently
       enabled work; fairness NEVER creates permission — HUMAN_AUTH_MISSING
       resolves to NEITHER, LAW remains the gate).

Zero workflows reference these modules. This gate puts them on a live
operating path: every progress/fairness claim registered in
`tools/progress_fairness_claims_manifest.json` is judged by the REAL
mechanism on the claim's declared evidence. A claim whose asserted verdict
disagrees with the prover is BLOCKED.

Boundary (from the mechanisms' own docstrings): this wires D23/D24/D25
onto the CI governance path only. Wiring progress/fairness accounting into
kernel/, KNOW, LAW, ACT, or any runtime path still needs Shawn's word.
The gate judges claims; it authorizes nothing; fairness can never create
permission through it.

Claim types:
  d23_progress_rank     — declares one ranked transition and asserts the
                          (proof_progress, termination_progress) the
                          machinery computes for it. Defect class: gaming
                          the measure (HEARTBEAT / ESCALATION /
                          REASSIGNMENT / bare NEW_EPOCH claimed as proof
                          progress; escalation claimed as completion).
  d24_three_truths      — declares a fairness contract + scheduling events
                          + assessment inputs, and asserts the three truths
                          and the composed conditional-liveness verdict.
                          Defect class: conflating opportunity with
                          accomplishment (CONDITIONAL_LIVENESS asserted on
                          DISPATCHED-only evidence; starvation claimed when
                          the worker failed, not the scheduler).
  d25_standard_selection— declares a scheduling situation (+ optional
                          eight-assumption evidence) and asserts the
                          required fairness standard. Defect class: weak
                          where strong is required (starvation risk); any
                          standard asserted where the mechanism says
                          NEITHER (fairness used as a permission excuse).

Exit contract (the whole point of the gate):
  0  PASS     — every registered claim certified honest by the prover.
  0  DORMANT  — manifest registers zero claims. Explicit, never a false
                green: the gate says "nothing to judge".
  1  VIOLATION— a claim misstates a verdict the prover computes
                (proof progress asserted on a heartbeat; accomplishment
                asserted on dispatch-only evidence; WEAK asserted where
                STRONG is required; a standard asserted where NEITHER
                holds).
  2  BROKEN   — fail-closed: manifest corrupt, claim fields unparseable or
                outside the mechanism's vocabulary, or claims exist but a
                mechanism is absent/neutered (the gate refuses to certify
                on defaults — it never invents the prover).

The gate never invents fields: unknown claim types, transition kinds,
ladder rungs, fairness standards, situations, or assumption ids are
BROKEN, not defaulted.

Directives: D23 (Well-Founded Measure of Real Progress), D24 (Fair
Scheduling Without False Progress), D25 (When Strong Fairness Is
Required); owners naya2. Wired by the night-shift WIRE lane.
No merge — Shawn pulls triggers.
"""

from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOLS_DIR.parent
DEFAULT_MANIFEST = TOOLS_DIR / "progress_fairness_claims_manifest.json"

EXIT_PASS = 0
EXIT_VIOLATION = 1
EXIT_BROKEN = 2

CLAIM_TYPES = ("d23_progress_rank", "d24_three_truths",
               "d25_standard_selection")
COMPOSITION_VALUES = ("CONDITIONAL_LIVENESS", "LIVENESS_UNPROVEN")
D25_STANDARD_VALUES = ("WEAK", "STRONG", "BOUNDED", "NEITHER")

REQUIRED_CLAIM_KEYS = frozenset({"id", "type"})
REQUIRED_D23_KEYS = frozenset({"transition", "claimed"})
REQUIRED_D23_TRANSITION_KEYS = frozenset({
    "kind", "prev_ranks", "next_ranks",
    "retries_before", "retries_after", "discharged",
})
REQUIRED_D23_CLAIMED_KEYS = frozenset({
    "proof_progress", "termination_progress",
})
REQUIRED_D24_KEYS = frozenset({"contract", "events", "assessment", "claimed"})
REQUIRED_D24_CONTRACT_KEYS = frozenset({
    "obligation_id", "revision", "standard",
    "eligibility_predicate", "service_predicate",
})
REQUIRED_D24_EVENT_KEYS = frozenset({
    "obligation_id", "workflow_id", "seq", "rung", "eligible",
})
REQUIRED_D24_ASSESSMENT_KEYS = frozenset({
    "debt_threshold", "serviced_rounds", "advanced_rounds",
    "rank_decreasing",
})
REQUIRED_D24_CLAIMED_KEYS = frozenset({
    "fair_chance", "advanced_on_service", "converging", "composition",
})
REQUIRED_D25_KEYS = frozenset({"situation", "claimed_standard"})


class GateBroken(Exception):
    """Fail-closed: the gate cannot trust its inputs. Exit 2."""


class MechanismMissing(Exception):
    """A D23/D24/D25 mechanism is absent or neutered. Exit 2 when claims exist."""


def _load_mechanism():
    """Import the REAL D23/D24/D25 mechanisms from this repo tree.

    Never synthesized, never defaulted. Verifies each module came from the
    checked-out tree (live bytes) and exposes the required API surface, so
    a neutered module cannot silently pass as the mechanism.
    """
    pkg_dir = REPO_ROOT / "drift_canary"
    for name in ("progress", "fairness", "strong_fairness"):
        if not (pkg_dir / f"{name}.py").is_file():
            raise MechanismMissing(f"mechanism not present: {pkg_dir}/{name}.py")
    sys.path.insert(0, str(REPO_ROOT))
    try:
        prog = importlib.import_module("drift_canary.progress")
        fair = importlib.import_module("drift_canary.fairness")
        strong = importlib.import_module("drift_canary.strong_fairness")
    except Exception as exc:
        raise MechanismMissing(f"mechanism failed to import: {exc}")
    finally:
        try:
            sys.path.remove(str(REPO_ROOT))
        except ValueError:
            pass
    for mod, name in ((prog, "progress"), (fair, "fairness"),
                      (strong, "strong_fairness")):
        loaded = Path(getattr(mod, "__file__", "") or "").resolve()
        if pkg_dir.resolve() not in loaded.parents:
            raise MechanismMissing(
                f"mechanism {name} loaded from outside the tree: {loaded}")
    for attr in ("classify_transition", "TRANSITION_KINDS"):
        if not hasattr(prog, attr):
            raise MechanismMissing(
                f"mechanism progress missing required API: {attr}")
    for attr in ("assess_three_truths", "compose_conditional_liveness",
                 "FairnessContract", "FairnessLedger", "SchedulingEvent",
                 "SERVICE_LADDER", "FAIRNESS_STANDARDS"):
        if not hasattr(fair, attr):
            raise MechanismMissing(
                f"mechanism fairness missing required API: {attr}")
    for attr in ("recommend_standard", "check_assumptions",
                 "assumptions_satisfied", "SITUATIONS", "EIGHT_ASSUMPTIONS"):
        if not hasattr(strong, attr):
            raise MechanismMissing(
                f"mechanism strong_fairness missing required API: {attr}")
    return prog, fair, strong


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
        if entry["type"] not in CLAIM_TYPES:
            raise GateBroken(
                f"claim {cid!r}: unknown type {entry['type']!r}; vocabulary "
                f"is {list(CLAIM_TYPES)} (never defaulted)")
    return data


def _as_str(value, what):
    if not isinstance(value, str) or not value:
        raise GateBroken(f"{what} must be a non-empty string")
    return value


def _as_bool(value, what):
    if not isinstance(value, bool):
        raise GateBroken(f"{what} must be true/false (never defaulted)")
    return value


def _as_int(value, what, minimum=None):
    if isinstance(value, bool) or not isinstance(value, int):
        raise GateBroken(f"{what} must be an integer, got {value!r}")
    if minimum is not None and value < minimum:
        raise GateBroken(f"{what} must be >= {minimum}, got {value!r}")
    return value


def _as_rank_list(value, what):
    if not isinstance(value, list) or not all(
            isinstance(v, int) and not isinstance(v, bool) and v >= 0
            for v in value):
        raise GateBroken(f"{what} must be a list of non-negative integers")
    return tuple(value)


def _require_keys(raw, required, what, cid):
    if not isinstance(raw, dict):
        raise GateBroken(f"claim {cid!r}: {what} must be an object")
    missing = required - set(raw.keys())
    if missing:
        raise GateBroken(
            f"claim {cid!r}: {what} missing required keys: {sorted(missing)}")


# ---------------------------------------------------------------------------
# D23 — progress-rank claims.
# ---------------------------------------------------------------------------

def _judge_d23(claim, prog):
    cid = claim["id"]
    _require_keys(claim, REQUIRED_D23_KEYS, "claim", cid)
    _require_keys(claim["transition"], REQUIRED_D23_TRANSITION_KEYS,
                  "transition", cid)
    _require_keys(claim["claimed"], REQUIRED_D23_CLAIMED_KEYS, "claimed", cid)
    t = claim["transition"]
    kind = t["kind"]
    if kind not in prog.TRANSITION_KINDS:
        raise GateBroken(
            f"claim {cid!r}: unknown transition kind {kind!r}; vocabulary is "
            f"{list(prog.TRANSITION_KINDS)} (never defaulted)")
    prev = _as_rank_list(t["prev_ranks"], f"claim {cid!r} prev_ranks")
    nxt = _as_rank_list(t["next_ranks"], f"claim {cid!r} next_ranks")
    rb = _as_int(t["retries_before"], f"claim {cid!r} retries_before",
                 minimum=0)
    ra = _as_int(t["retries_after"], f"claim {cid!r} retries_after",
                 minimum=0)
    discharged = _as_bool(t["discharged"], f"claim {cid!r} discharged")
    claimed = claim["claimed"]
    c_proof = _as_bool(claimed["proof_progress"],
                       f"claim {cid!r} claimed.proof_progress")
    c_term = _as_bool(claimed["termination_progress"],
                      f"claim {cid!r} claimed.termination_progress")
    try:
        ok, (proof, term), reason = prog.classify_transition(
            kind, prev, nxt, rb, ra, discharged)
    except AssertionError as exc:
        raise GateBroken(
            f"claim {cid!r}: transition rejected by the mechanism: {exc}")
    if not ok:
        raise GateBroken(
            f"claim {cid!r}: transition not classifiable: {reason}")
    problems = []
    if c_proof != proof:
        problems.append(
            f"claimed proof_progress={c_proof} but the prover computes "
            f"{proof}")
    if c_term != term:
        problems.append(
            f"claimed termination_progress={c_term} but the prover computes "
            f"{term}")
    if problems:
        detail = "; ".join(problems)
        detail += f" | prover: proof={proof}, termination={term} ({reason})"
        return "VIOLATION", detail
    return "PASS", (f"prover: proof={proof}, termination={term} ({reason})")


# ---------------------------------------------------------------------------
# D24 — three-truths claims.
# ---------------------------------------------------------------------------

def _judge_d24(claim, fair):
    cid = claim["id"]
    _require_keys(claim, REQUIRED_D24_KEYS, "claim", cid)
    _require_keys(claim["contract"], REQUIRED_D24_CONTRACT_KEYS,
                  "contract", cid)
    c = claim["contract"]
    oid = _as_str(c["obligation_id"], f"claim {cid!r} contract.obligation_id")
    revision = _as_str(c["revision"], f"claim {cid!r} contract.revision")
    standard = c["standard"]
    if standard not in fair.FAIRNESS_STANDARDS:
        raise GateBroken(
            f"claim {cid!r}: unknown fairness standard {standard!r}; "
            f"vocabulary is {list(fair.FAIRNESS_STANDARDS)} (never defaulted)")
    for key in ("eligibility_predicate", "service_predicate"):
        _as_str(c[key], f"claim {cid!r} contract.{key}")
    wait_accounting = c.get("wait_accounting", "ELIGIBLE_SCHEDULER_ROUNDS")
    if not isinstance(wait_accounting, str) or not wait_accounting:
        raise GateBroken(
            f"claim {cid!r}: contract.wait_accounting must be a non-empty "
            f"string")
    preserve = c.get("preserve_across_reassignment", True)
    preserve = _as_bool(
        preserve, f"claim {cid!r} contract.preserve_across_reassignment")
    bound = _as_int(c.get("service_bound_rounds", 0),
                    f"claim {cid!r} contract.service_bound_rounds", minimum=0)
    capacity = c.get("capacity_basis", "")
    if not isinstance(capacity, str):
        raise GateBroken(
            f"claim {cid!r}: contract.capacity_basis must be a string")
    try:
        contract = fair.FairnessContract(
            obligation_id=oid, revision=revision, standard=standard,
            eligibility_predicate=c["eligibility_predicate"],
            service_predicate=c["service_predicate"],
            wait_accounting=wait_accounting,
            preserve_across_reassignment=preserve,
            service_bound_rounds=bound, capacity_basis=capacity)
    except AssertionError as exc:
        raise GateBroken(
            f"claim {cid!r}: contract rejected by the mechanism: {exc}")

    events = claim["events"]
    if not isinstance(events, list) or not events:
        raise GateBroken(
            f"claim {cid!r}: events must be a non-empty list")
    parsed = []
    for i, e in enumerate(events):
        _require_keys(e, REQUIRED_D24_EVENT_KEYS, f"events[{i}]", cid)
        if e["obligation_id"] != oid:
            raise GateBroken(
                f"claim {cid!r}: events[{i}] is for obligation "
                f"{e['obligation_id']!r}, not the contract's {oid!r} "
                f"(debt belongs to the obligation id — never mixed)")
        wid = _as_str(e["workflow_id"], f"claim {cid!r} events[{i}].workflow_id")
        seq = _as_int(e["seq"], f"claim {cid!r} events[{i}].seq", minimum=0)
        rung = e["rung"]
        if rung not in fair.SERVICE_LADDER:
            raise GateBroken(
                f"claim {cid!r}: events[{i}] unknown rung {rung!r}; vocabulary "
                f"is {list(fair.SERVICE_LADDER)} (never defaulted)")
        eligible = _as_bool(e["eligible"], f"claim {cid!r} events[{i}].eligible")
        ev_raw = e.get("evidence", {})
        if not isinstance(ev_raw, dict):
            raise GateBroken(
                f"claim {cid!r}: events[{i}].evidence must be an object")
        for k, v in ev_raw.items():
            if not isinstance(v, str):
                raise GateBroken(
                    f"claim {cid!r}: events[{i}].evidence[{k!r}] must be a "
                    f"string")
        note = e.get("note", "")
        if not isinstance(note, str):
            raise GateBroken(
                f"claim {cid!r}: events[{i}].note must be a string")
        try:
            parsed.append(fair.SchedulingEvent(
                obligation_id=oid, workflow_id=wid, seq=seq, rung=rung,
                eligible=eligible,
                evidence=tuple(sorted(ev_raw.items())), note=note))
        except AssertionError as exc:
            raise GateBroken(
                f"claim {cid!r}: events[{i}] rejected by the mechanism: {exc}")

    _require_keys(claim["assessment"], REQUIRED_D24_ASSESSMENT_KEYS,
                  "assessment", cid)
    a = claim["assessment"]
    debt_threshold = _as_int(a["debt_threshold"],
                             f"claim {cid!r} assessment.debt_threshold",
                             minimum=0)
    serviced = _as_int(a["serviced_rounds"],
                       f"claim {cid!r} assessment.serviced_rounds", minimum=0)
    advanced = _as_int(a["advanced_rounds"],
                       f"claim {cid!r} assessment.advanced_rounds", minimum=0)
    rank_dec = _as_bool(a["rank_decreasing"],
                        f"claim {cid!r} assessment.rank_decreasing")

    ledger = fair.FairnessLedger()
    ledger.register(contract)
    try:
        for ev in parsed:
            ok, _debt, _why = ledger.record_round(ev)
            if not ok:
                raise GateBroken(
                    f"claim {cid!r}: ledger refused a round: {_why}")
        truths = fair.assess_three_truths(
            ledger, oid, debt_threshold, serviced, advanced, rank_dec)
        established, verdict, reason = fair.compose_conditional_liveness(truths)
    except AssertionError as exc:
        raise GateBroken(
            f"claim {cid!r}: assessment rejected by the mechanism: {exc}")

    _require_keys(claim["claimed"], REQUIRED_D24_CLAIMED_KEYS, "claimed", cid)
    cl = claim["claimed"]
    c_fair = _as_bool(cl["fair_chance"], f"claim {cid!r} claimed.fair_chance")
    c_adv = _as_bool(cl["advanced_on_service"],
                      f"claim {cid!r} claimed.advanced_on_service")
    c_conv = _as_bool(cl["converging"], f"claim {cid!r} claimed.converging")
    c_comp = cl["composition"]
    if c_comp not in COMPOSITION_VALUES:
        raise GateBroken(
            f"claim {cid!r}: unknown composition {c_comp!r}; vocabulary is "
            f"{list(COMPOSITION_VALUES)} (never defaulted)")
    problems = []
    if c_fair != truths.fair_chance:
        problems.append(
            f"claimed fair_chance={c_fair} but the prover computes "
            f"{truths.fair_chance}")
    if c_adv != truths.advanced_on_service:
        problems.append(
            f"claimed advanced_on_service={c_adv} but the prover computes "
            f"{truths.advanced_on_service}")
    if c_conv != truths.converging:
        problems.append(
            f"claimed converging={c_conv} but the prover computes "
            f"{truths.converging}")
    if c_comp != verdict:
        problems.append(
            f"claimed composition={c_comp} but the prover computes {verdict}")
    if problems:
        detail = "; ".join(problems)
        detail += (f" | prover: fair_chance={truths.fair_chance}, "
                   f"advanced_on_service={truths.advanced_on_service}, "
                   f"converging={truths.converging}, verdict={verdict} "
                   f"({truths.detail})")
        return "VIOLATION", detail
    return "PASS", (f"prover: verdict={verdict} ({truths.detail})")


# ---------------------------------------------------------------------------
# D25 — standard-selection claims.
# ---------------------------------------------------------------------------

def _judge_d25(claim, strong):
    cid = claim["id"]
    _require_keys(claim, REQUIRED_D25_KEYS, "claim", cid)
    situation = claim["situation"]
    if situation not in strong.SITUATIONS:
        raise GateBroken(
            f"claim {cid!r}: unknown situation {situation!r}; vocabulary is "
            f"{list(strong.SITUATIONS)} (never defaulted)")
    claimed_standard = claim["claimed_standard"]
    if claimed_standard not in D25_STANDARD_VALUES:
        raise GateBroken(
            f"claim {cid!r}: unknown claimed_standard {claimed_standard!r}; "
            f"vocabulary is {list(D25_STANDARD_VALUES)} (never defaulted)")
    try:
        standard, reason = strong.recommend_standard(situation)
    except AssertionError as exc:
        raise GateBroken(
            f"claim {cid!r}: situation rejected by the mechanism: {exc}")
    problems = []
    if claimed_standard != standard:
        problems.append(
            f"claimed_standard={claimed_standard} but the decision rule "
            f"requires {standard} ({reason})")
    ev_raw = claim.get("assumptions_evidence")
    claimed_ok = claim.get("claimed_assumptions_ok")
    if (ev_raw is None) != (claimed_ok is None):
        raise GateBroken(
            f"claim {cid!r}: assumptions_evidence and claimed_assumptions_ok "
            f"must appear together (never half a claim)")
    if ev_raw is not None:
        if not isinstance(ev_raw, dict):
            raise GateBroken(
                f"claim {cid!r}: assumptions_evidence must be an object")
        known_ids = {a for a, _ in strong.EIGHT_ASSUMPTIONS}
        for k, v in ev_raw.items():
            if k not in known_ids:
                raise GateBroken(
                    f"claim {cid!r}: unknown assumption id {k!r}; vocabulary "
                    f"is {sorted(known_ids)} (never defaulted)")
            if v is not None and not isinstance(v, str):
                raise GateBroken(
                    f"claim {cid!r}: assumptions_evidence[{k!r}] must be a "
                    f"string or null")
        c_ok = _as_bool(claimed_ok,
                        f"claim {cid!r} claimed_assumptions_ok")
        results = strong.check_assumptions(ev_raw)
        ok, missing = strong.assumptions_satisfied(results)
        if c_ok != ok:
            problems.append(
                f"claimed_assumptions_ok={c_ok} but the prover computes "
                f"{ok} (missing: {missing})")
    if problems:
        detail = "; ".join(problems)
        detail += f" | prover standard={standard} ({reason})"
        return "VIOLATION", detail
    return "PASS", f"prover standard={standard} ({reason})"


def _judge_claim(claim, prog, fair, strong):
    """Judge one claim against the real mechanism.

    Returns (verdict, detail) with verdict in PASS/VIOLATION.
    Raises GateBroken on untrustworthy inputs (caller maps to exit 2).
    """
    ctype = claim["type"]
    if ctype == "d23_progress_rank":
        return _judge_d23(claim, prog)
    if ctype == "d24_three_truths":
        return _judge_d24(claim, fair)
    if ctype == "d25_standard_selection":
        return _judge_d25(claim, strong)
    raise GateBroken(  # unreachable: type checked at load; defense in depth
        f"claim {claim['id']!r}: unknown type {ctype!r}")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="D23/D24/D25 progress & fairness claims gate: judge "
                    "registered claims against the real drift_canary "
                    "mechanisms.")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST),
                        help="path to the claims manifest JSON")
    args = parser.parse_args(argv)

    try:
        manifest = _load_manifest(args.manifest)
    except GateBroken as exc:
        print(f"PF-GATE BROKEN: {exc}")
        return EXIT_BROKEN

    if manifest is None:
        print("PF-GATE DORMANT: no manifest present; nothing to judge "
              "(not a green — a stated absence of coverage)")
        return EXIT_PASS

    claims = manifest["claims"]
    if not claims:
        print("PF-GATE DORMANT: manifest registers zero claims; nothing "
              "to judge (not a green — a stated absence of coverage)")
        return EXIT_PASS

    try:
        prog, fair, strong = _load_mechanism()
    except MechanismMissing as exc:
        print(f"PF-GATE BROKEN: {exc} (fail-closed: claims exist but the "
              f"mechanism cannot be proven present)")
        return EXIT_BROKEN

    violations = []
    broken = []
    passed = 0
    for claim in claims:
        cid = claim["id"]
        try:
            verdict, detail = _judge_claim(claim, prog, fair, strong)
        except GateBroken as exc:
            broken.append((cid, str(exc)))
            continue
        if verdict == "VIOLATION":
            violations.append((cid, detail))
        else:
            passed += 1
            print(f"PF-GATE PASS: claim {cid!r} honest — {detail}")

    if broken:
        for cid, detail in broken:
            print(f"PF-GATE BROKEN: claim {cid!r}: {detail}")
        print(f"PF-GATE BROKEN: {len(broken)} claim(s) unjudgeable; "
              f"{passed} passed, {len(violations)} violation(s). "
              f"Fail-closed: fix the manifest, do not ship the claims.")
        return EXIT_BROKEN

    if violations:
        for cid, detail in violations:
            print(f"PF-GATE VIOLATION: claim {cid!r}: {detail}")
        print(f"PF-GATE VIOLATION: {len(violations)} dishonest claim(s) "
              f"BLOCKED; {passed} passed. The prover disagrees — the claim "
              f"must be corrected or its evidence repaired.")
        return EXIT_VIOLATION

    print(f"PF-GATE PASS: {passed}/{len(claims)} registered claim(s) "
          f"certified honest by drift_canary progress/fairness/strong_fairness")
    return EXIT_PASS


if __name__ == "__main__":
    sys.exit(main())
