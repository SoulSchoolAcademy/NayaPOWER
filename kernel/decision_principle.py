"""Naya Decision Principle — INDEPENDENT VERIFICATION ORACLE.

NON-AUTHORITATIVE. This module is NOT a decision authority.

The ONE canonical decision engine is kernel/value_calculus.py (Shawn
2026-10-11: "Bring them together and put the best of them together" —
consolidate, no exception for a second engine).

This module's role, and ONLY this role: an INDEPENDENT implementation of the
decision principle, written straight from the spec text, sharing no code paths
with the canonical engine. It exists so the consolidated engine can be
cross-verified — two independent implementations must agree, or something is
wrong. It is a test oracle, never a production decision-maker.

Shawn's principle, as code:

    FIRST — HARD GATES
        Protect people · Tell the truth · Respect authority
    THEN — INTELLIGENT OPTIMIZATION
        a* = argmax over A_admissible of V_verified(a)

The critical distinction: an action that violates a non-negotiable human
protection is not worth zero points. It is DISQUALIFIED from the competition
entirely. Disqualification is not a score — it is exclusion. A disqualified
action cannot win on other dimensions, no matter how high its value.

The refinement: not every risk is a prohibition. Helping someone involves
uncertainty and trade-offs. The protect-people gate tests for UNACCEPTABLE
HARM — not for the mere presence of uncertainty. Uncertainty alone never
disqualifies; it defers (unknown is not safe, and unknown is not prohibited —
the Zero Value Law). Residual risk with informed consent and genuine
mitigation is admissible.

Honest outputs are first-class: "I don't know yet", "this isn't safe", or
"there's a better way" are not failures to create value. When no admissible
action has verified value, abstaining IS the highest-value choice.

Deterministic, dependency-free. Scores never create authority.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Mapping, Optional, Sequence
import math
import random

ENGINE_VERSION = "NAYA-DECISION-PRINCIPLE-V1"

# ---------------------------------------------------------------------------
# Verdicts — the only three outcomes a hard gate can produce.
# ---------------------------------------------------------------------------

ADMISSIBLE = "ADMISSIBLE"      # passes the gate; may compete on value
DISQUALIFIED = "DISQUALIFIED"  # fails on merits; excluded from the competition
DEFERRED = "DEFERRED"          # cannot be judged yet; needs evidence/authority

# Decision outcomes (Phase 2)
ACT = "ACT"            # an admissible action was chosen on verified value
ABSTAIN = "ABSTAIN"    # honest output: no admissible action has verified value
REFUSE = "REFUSE"      # every candidate was disqualified; nothing may proceed
ASK = "ASK"            # admissible actions exist but all are deferred on authority


def _finite(value: float, name: str) -> float:
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, _finite(value, "probability")))


# ---------------------------------------------------------------------------
# Action — the unit of decision.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Action:
    """One candidate action, carrying exactly the evidence the gates need.

    Gate evidence uses Optional[bool] deliberately:
      True  = established by evidence
      False = established absent by evidence
      None  = unknown (defers judgment; unknown is neither safe nor prohibited)
    """
    action_id: str
    description: str = ""

    # --- protect-people evidence -------------------------------------------
    unacceptable_harm: Optional[bool] = None   # established unacceptable harm?
    harm_severity: Optional[float] = None      # 0..10 scale when assessed
    harm_probability: Optional[float] = None   # 0..1 when assessed
    harm_mitigated: bool = False               # residual risk genuinely minimized?
    informed_consent: bool = False              # affected party chose with full info?

    # --- tell-truth evidence ------------------------------------------------
    deceptive: Optional[bool] = None           # established deceptive?

    # --- respect-authority evidence -----------------------------------------
    authorized: bool = False                   # holds valid authority?
    forbidden_scope: bool = False              # explicitly outside permitted scope?

    # --- Phase 2 evidence ----------------------------------------------------
    verified_value: Optional[float] = None     # V_verified; None = not verified
    value_evidence: str = ""                   # provenance of the value claim
    honest_abstention: bool = False            # is this action an honest
                                               # "I don't know / not safe /
                                               #  better way" output?


@dataclass(frozen=True)
class GateResult:
    verdict: str          # ADMISSIBLE | DISQUALIFIED | DEFERRED
    gate: str             # which gate produced this
    reasons: tuple = ()   # machine-readable reason codes


# ---------------------------------------------------------------------------
# Phase 1 — HARD GATES. Binary. No scoring. No trade-offs.
# ---------------------------------------------------------------------------

# Unacceptable-harm bar: severity and probability thresholds. An action is
# only ever DISQUALIFIED for harm when harm is ESTABLISHED above this bar.
# Uncertainty alone (unknown severity/probability) DEFERS — never disqualifies.
HARM_SEVERITY_THRESHOLD = 7.0
HARM_PROBABILITY_THRESHOLD = 0.05


def gate_protect_people(action: Action) -> GateResult:
    """DISQUALIFIED only on established unacceptable harm.

    Unacceptable harm = established harm above the severity×probability bar,
    without both informed consent and genuine mitigation. Residual risk that
    is minimized and consented to is ADMISSIBLE — helping involves trade-offs.
    Unknown harm DEFERS (unknown != safe, unknown != prohibited).
    """
    if action.unacceptable_harm is True:
        # Established on the merits — but consent + mitigation can still admit.
        if action.informed_consent and action.harm_mitigated:
            return GateResult(ADMISSIBLE, "protect_people",
                              ("RESIDUAL_RISK_CONSENTED_MITIGATED",))
        return GateResult(DISQUALIFIED, "protect_people",
                          ("UNACCEPTABLE_HARM",))

    if action.unacceptable_harm is None:
        # Fall back to assessed severity/probability when present.
        if action.harm_severity is not None and action.harm_probability is not None:
            sev = _finite(action.harm_severity, "harm_severity")
            prob = _clamp01(action.harm_probability)
            if sev >= HARM_SEVERITY_THRESHOLD and prob > HARM_PROBABILITY_THRESHOLD:
                if action.informed_consent and action.harm_mitigated:
                    return GateResult(ADMISSIBLE, "protect_people",
                                      ("RESIDUAL_RISK_CONSENTED_MITIGATED",))
                return GateResult(DISQUALIFIED, "protect_people",
                                  ("UNACCEPTABLE_HARM_ASSESSED",))
        # Cannot judge safety — defer, do not prohibit, do not permit.
        return GateResult(DEFERRED, "protect_people", ("HARM_UNKNOWN",))

    # unacceptable_harm is False: established no unacceptable harm.
    return GateResult(ADMISSIBLE, "protect_people", ("NO_UNACCEPTABLE_HARM",))


def gate_tell_truth(action: Action) -> GateResult:
    """DISQUALIFIED on established deception. Unknown defers."""
    if action.deceptive is True:
        return GateResult(DISQUALIFIED, "tell_truth", ("DECEPTIVE",))
    if action.deceptive is None:
        return GateResult(DEFERRED, "tell_truth", ("TRUTHFULNESS_UNKNOWN",))
    return GateResult(ADMISSIBLE, "tell_truth", ("NOT_DECEPTIVE",))


def gate_respect_authority(action: Action) -> GateResult:
    """Forbidden scope DISQUALIFIES. Merely missing authority DEFERS.

    The distinction matters: an action outside permitted scope can never be
    rescued by value. An action that simply lacks authorization yet may
    become admissible once authority is granted.
    """
    if action.forbidden_scope:
        return GateResult(DISQUALIFIED, "respect_authority",
                          ("FORBIDDEN_SCOPE",))
    if not action.authorized:
        return GateResult(DEFERRED, "respect_authority",
                          ("AUTHORITY_MISSING",))
    return GateResult(ADMISSIBLE, "respect_authority", ("AUTHORIZED",))


HARD_GATES: tuple[Callable[[Action], GateResult], ...] = (
    gate_protect_people,
    gate_tell_truth,
    gate_respect_authority,
)


def run_hard_gates(action: Action) -> tuple[str, list[GateResult]]:
    """Run all hard gates. DISQUALIFIED if ANY gate disqualifies.

    A single disqualification removes the action from the competition —
    other gates still run so the receipt is complete, but the verdict
    cannot be rescued by passing elsewhere.
    """
    results = [gate(action) for gate in HARD_GATES]
    if any(r.verdict == DISQUALIFIED for r in results):
        return DISQUALIFIED, results
    if any(r.verdict == DEFERRED for r in results):
        return DEFERRED, results
    return ADMISSIBLE, results


# ---------------------------------------------------------------------------
# Phase 2 — INTELLIGENT OPTIMIZATION over the admissible set only.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Decision:
    outcome: str                       # ACT | ABSTAIN | REFUSE | ASK
    chosen_action_id: Optional[str]    # None unless outcome == ACT
    chosen_value: Optional[float]       # V_verified of the choice
    admissible_ids: tuple              # every action that passed all hard gates
    disqualified_ids: tuple            # excluded on merits — never competed
    deferred_ids: tuple                # not yet judgeable
    ranking: tuple                     # admissible+verified, best first
    receipts: tuple                    # per-action gate receipts
    note: str = ""                     # human-readable explanation


class PrincipleOracle:
    """Independent oracle of the two-phase decision principle.

    NON-AUTHORITATIVE — test oracle only. The canonical engine is
    kernel/value_calculus.py.

    Phase 1 partitions candidates into admissible / disqualified / deferred.
    Phase 2 runs argmax of V_verified over the admissible set ONLY.
    Disqualified actions never enter the ranking — they were excluded,
    not outscored.

    Written independently from the spec text; shares no code paths with the
    canonical engine. Used by cross_verify() to prove the consolidated
    engine governs behavior correctly across MULTIPLE implementations.
    """

    def decide(self, actions: Sequence[Action]) -> Decision:
        receipts: list[tuple[str, str, list[GateResult]]] = []
        admissible: list[Action] = []
        disqualified: list[Action] = []
        deferred: list[Action] = []

        # ---- Phase 1: hard gates -------------------------------------------
        for action in actions:
            verdict, results = run_hard_gates(action)
            receipts.append((action.action_id, verdict, results))
            if verdict == ADMISSIBLE:
                admissible.append(action)
            elif verdict == DISQUALIFIED:
                disqualified.append(action)
            else:
                deferred.append(action)

        admissible_ids = tuple(a.action_id for a in admissible)
        disqualified_ids = tuple(a.action_id for a in disqualified)
        deferred_ids = tuple(a.action_id for a in deferred)
        receipt_tuples = tuple((aid, v, tuple(r.reasons for r in rs))
                               for aid, v, rs in receipts)

        # ---- Phase 2: optimize over admissible set only --------------------
        # Only verified value competes. Choosing on unverified value would
        # be guessing, not intelligence.
        #
        # Trust boundary (stated plainly): `verified_value is not None` is
        # the caller's assertion that the value is verified — upstream
        # evidence floors (e.g. gate_candidate's EVIDENCE_FLOOR) are the
        # caller's contract to enforce. This engine's contract is narrower
        # and absolute: it never optimizes on None.
        contenders = [a for a in admissible if a.verified_value is not None]
        contenders.sort(key=lambda a: (-_finite(a.verified_value, "verified_value"),
                                       a.action_id))
        ranking = tuple(a.action_id for a in contenders)

        if contenders:
            winner = contenders[0]
            return Decision(
                outcome=ACT,
                chosen_action_id=winner.action_id,
                chosen_value=winner.verified_value,
                admissible_ids=admissible_ids,
                disqualified_ids=disqualified_ids,
                deferred_ids=deferred_ids,
                ranking=ranking,
                receipts=receipt_tuples,
                note=(f"Chose {winner.action_id} with verified value "
                      f"{winner.verified_value} from {len(admissible)} admissible "
                      f"action(s); {len(disqualified)} disqualified, "
                      f"{len(deferred)} deferred."),
            )

        if not actions:
            return Decision(
                outcome=ABSTAIN,
                chosen_action_id=None,
                chosen_value=None,
                admissible_ids=(),
                disqualified_ids=(),
                deferred_ids=(),
                ranking=(),
                receipts=(),
                note="No actions were proposed. Honest output: nothing to decide.",
            )

        if admissible:
            # Admissible actions exist, but none has verified value.
            # The honest output is abstention — not a guess.
            return Decision(
                outcome=ABSTAIN,
                chosen_action_id=None,
                chosen_value=None,
                admissible_ids=admissible_ids,
                disqualified_ids=disqualified_ids,
                deferred_ids=deferred_ids,
                ranking=(),
                receipts=receipt_tuples,
                note=("Admissible actions exist but none has verified value. "
                      "Honest output: 'I don't know yet' — abstaining rather "
                      "than guessing."),
            )

        if deferred:
            # Deferred actions may still proceed once the gap closes.
            # Authority gaps ask; evidence gaps abstain honestly.
            # Only DEFERRED actions' reasons count — a disqualified action's
            # missing authority is irrelevant; it is out on the merits.
            deferred_ids_set = set(deferred_ids)
            needs_authority = any(
                r.verdict == DEFERRED and "AUTHORITY_MISSING" in r.reasons
                for aid, _, rs in receipts if aid in deferred_ids_set
                for r in rs
            )
            if needs_authority:
                return Decision(
                    outcome=ASK,
                    chosen_action_id=None,
                    chosen_value=None,
                    admissible_ids=(),
                    disqualified_ids=disqualified_ids,
                    deferred_ids=deferred_ids,
                    ranking=(),
                    receipts=receipt_tuples,
                    note=("Candidates are deferred pending authority. "
                          "Honest output: ask for the missing authority."),
                )
            return Decision(
                outcome=ABSTAIN,
                chosen_action_id=None,
                chosen_value=None,
                admissible_ids=(),
                disqualified_ids=disqualified_ids,
                deferred_ids=deferred_ids,
                ranking=(),
                receipts=receipt_tuples,
                note=("Candidates are deferred pending evidence. "
                      "Honest output: 'I don't know yet'."),
            )

        return Decision(
            outcome=REFUSE,
            chosen_action_id=None,
            chosen_value=None,
            admissible_ids=(),
            disqualified_ids=disqualified_ids,
            deferred_ids=deferred_ids,
            ranking=(),
            receipts=receipt_tuples,
            note=("Every candidate was disqualified on the merits. "
                  "Nothing may proceed. Honest output: 'this isn't safe'."),
        )


# ---------------------------------------------------------------------------
# Integration — the existing value-calculus pipeline already separates
# gating from optimization. These adapters prove it in this verdict space.
# ---------------------------------------------------------------------------

def verdict_from_calculus_gate(calculus_gate: str) -> str:
    """Map value_calculus gate_candidate outcomes into this verdict space.

    PROHIBITED  -> DISQUALIFIED (excluded on merits)
    NEEDS_AUTHORITY / NEEDS_EVIDENCE -> DEFERRED (may become admissible)
    ADMISSIBLE  -> ADMISSIBLE
    """
    mapping = {
        "PROHIBITED": DISQUALIFIED,
        "NEEDS_AUTHORITY": DEFERRED,
        "NEEDS_EVIDENCE": DEFERRED,
        "ADMISSIBLE": ADMISSIBLE,
    }
    if calculus_gate not in mapping:
        raise ValueError(f"unknown calculus gate: {calculus_gate}")
    return mapping[calculus_gate]


def verify_pipeline_excludes_first(candidates, baseline_id, profile,
                                   risk_policy=None) -> dict:
    """Prove the existing pipeline excludes before it optimizes.

    Runs the real gate_candidate + evaluate_candidates and asserts:
      - no PROHIBITED candidate appears in the eligible/ranked set
      - no PROHIBITED candidate is ever the chosen action
    Returns the evidence dict; raises AssertionError on violation.
    """
    from kernel.value_calculus import (
        gate_candidate, evaluate_candidates, ADMISSIBLE as VC_ADMISSIBLE,
        PROHIBITED as VC_PROHIBITED,
    )

    policy = risk_policy
    if policy is None:
        from kernel.value_calculus import RiskPolicy
        policy = RiskPolicy()

    gates = {}
    for c in candidates:
        gate, reasons, _ = gate_candidate(c, profile, policy)
        gates[c.candidate_id] = (gate, reasons)

    result = evaluate_candidates(candidates, baseline_id, profile, policy)

    ranked_ids = [r["candidate_id"] for r in result.get("ranked_all", [])]
    top_ids = [r["candidate_id"] for r in result.get("top3", [])]
    chosen = result.get("decision")

    violations = []
    for cid in ranked_ids + top_ids:
        if gates[cid][0] == VC_PROHIBITED:
            violations.append(cid)
    if isinstance(chosen, dict) and chosen.get("candidate_id"):
        if gates[chosen["candidate_id"]][0] == VC_PROHIBITED:
            violations.append(chosen["candidate_id"])

    evidence = {
        "gates": {cid: g for cid, (g, _) in gates.items()},
        "ranked_ids": ranked_ids,
        "top3_ids": top_ids,
        "decision": chosen,
        "violations": violations,
    }
    assert not violations, (
        f"pipeline optimized over prohibited candidates: {violations}")
    return evidence


# ---------------------------------------------------------------------------
# Cross-implementation verification — Shawn's test: the principles must
# govern behavior across MULTIPLE implementations, not just one.
#
# Implementation B below is written independently, straight from the spec
# text, sharing no code paths with PrincipleOracle. The harness runs both
# over a scenario battery plus randomized scenarios and requires agreement
# on: the disqualified set, the admissible set, and the chosen action.
# ---------------------------------------------------------------------------

def _independent_decide(actions: Sequence[Action]) -> dict:
    """Independent reimplementation, written directly from the spec.

    Deliberately shares no code with PrincipleOracle: different structure,
    different order of checks, same required semantics.
    """
    disqualified: list[str] = []
    admissible: list[dict] = []   # (action_id, verified_value)
    deferred: list[str] = []
    deferred_on_authority: set[str] = set()

    for a in actions:
        out = None  # (verdict, reason)

        # Gate 1: protect people — spec order differs from run_hard_gates.
        if a.unacceptable_harm is True and not (a.informed_consent and a.harm_mitigated):
            out = (DISQUALIFIED, "UNACCEPTABLE_HARM")
        elif (a.unacceptable_harm is None and a.harm_severity is not None
              and a.harm_probability is not None
              and float(a.harm_severity) >= 7.0 and float(a.harm_probability) > 0.05
              and not (a.informed_consent and a.harm_mitigated)):
            out = (DISQUALIFIED, "UNACCEPTABLE_HARM_ASSESSED")

        # Gate 2: tell truth.
        if out is None and a.deceptive is True:
            out = (DISQUALIFIED, "DECEPTIVE")

        # Gate 3: respect authority.
        if out is None and a.forbidden_scope:
            out = (DISQUALIFIED, "FORBIDDEN_SCOPE")

        if out is not None:
            disqualified.append(a.action_id)
            continue

        # Deferred checks (epistemic, not merits).
        unknown = (
            a.unacceptable_harm is None
            and not (a.harm_severity is not None and a.harm_probability is not None
                     and float(a.harm_severity) >= 7.0 and float(a.harm_probability) > 0.05)
        )
        if unknown or a.deceptive is None or not a.authorized:
            deferred.append(a.action_id)
            if not a.authorized:
                deferred_on_authority.add(a.action_id)
            continue

        admissible.append((a.action_id, a.verified_value))

    # Phase 2: argmax over admissible with verified value.
    contenders = sorted(
        [(aid, v) for aid, v in admissible if v is not None],
        key=lambda t: (-float(t[1]), t[0]),
    )
    chosen = contenders[0][0] if contenders else None

    if chosen is not None:
        outcome = ACT
    elif not actions:
        outcome = ABSTAIN
    elif admissible:
        outcome = ABSTAIN
    elif deferred:
        outcome = ASK if deferred_on_authority else ABSTAIN
    else:
        outcome = REFUSE

    return {
        "outcome": outcome,
        "chosen": chosen,
        "disqualified": sorted(disqualified),
        "admissible": sorted(aid for aid, _ in admissible),
        "deferred": sorted(deferred),
    }


def cross_verify(scenarios: Sequence[Sequence[Action]]) -> dict:
    """Run PrincipleOracle and the independent implementation over every
    scenario. They must agree on disqualified set, admissible set, chosen
    action, and outcome. Returns agreement evidence; raises on divergence.
    """
    engine = PrincipleOracle()
    divergences: list[dict] = []

    for i, actions in enumerate(scenarios):
        d = engine.decide(actions)
        a_result = {
            "outcome": d.outcome,
            "chosen": d.chosen_action_id,
            "disqualified": sorted(d.disqualified_ids),
            "admissible": sorted(d.admissible_ids),
            "deferred": sorted(d.deferred_ids),
        }
        b_result = _independent_decide(actions)
        if a_result != b_result:
            divergences.append({
                "scenario": i,
                "engine": a_result,
                "independent": b_result,
            })

    evidence = {
        "scenarios": len(scenarios),
        "divergences": divergences,
        "agreed": len(divergences) == 0,
    }
    assert evidence["agreed"], (
        f"implementations diverged on {len(divergences)} scenario(s): "
        f"{divergences[:3]}")
    return evidence


def random_scenarios(seed: int, count: int,
                     max_actions: int = 5) -> list[list[Action]]:
    """Deterministic randomized scenario battery for cross-verification."""
    rng = random.Random(seed)
    scenarios: list[list[Action]] = []
    for s in range(count):
        n = rng.randint(1, max_actions)
        actions: list[Action] = []
        for k in range(n):
            aid = f"s{s}a{k}"
            uharm = rng.choice([True, False, None, None])
            sev = round(rng.uniform(0, 10), 2) if rng.random() < 0.5 else None
            prob = round(rng.uniform(0, 1), 3) if rng.random() < 0.5 else None
            actions.append(Action(
                action_id=aid,
                unacceptable_harm=uharm,
                harm_severity=sev,
                harm_probability=prob,
                harm_mitigated=rng.random() < 0.3,
                informed_consent=rng.random() < 0.3,
                deceptive=rng.choice([True, False, None]),
                authorized=rng.random() < 0.6,
                forbidden_scope=rng.random() < 0.15,
                verified_value=(round(rng.uniform(-5, 20), 2)
                                if rng.random() < 0.7 else None),
            ))
        scenarios.append(actions)
    return scenarios


def scenario_battery() -> list[list[Action]]:
    """Hand-built edge scenarios: the cases the principle must get right."""
    def base(aid: str, **kw) -> Action:
        d = dict(action_id=aid, unacceptable_harm=False, deceptive=False,
                 authorized=True, verified_value=5.0)
        d.update(kw)
        return Action(**d)

    return [
        # 1. High-value prohibited action must be disqualified, not outscored.
        [base("harmful", unacceptable_harm=True, verified_value=100.0),
         base("safe", verified_value=5.0)],
        # 2. Uncertainty alone never disqualifies.
        [base("unknown", unacceptable_harm=None, harm_severity=None,
              harm_probability=None, deceptive=None, authorized=False)],
        # 3. Consented, mitigated residual risk is admissible.
        [base("risky-but-consented", harm_severity=9.0, harm_probability=0.5,
              harm_mitigated=True, informed_consent=True, verified_value=8.0)],
        # 4. Unassessed high severity+probability disqualifies.
        [base("reckless", unacceptable_harm=None, harm_severity=9.0,
              harm_probability=0.5, verified_value=50.0),
         base("modest", verified_value=3.0)],
        # 5. Deception disqualifies regardless of value.
        [base("liar", deceptive=True, verified_value=99.0),
         base("honest", verified_value=1.0)],
        # 6. Forbidden scope disqualifies; missing authority defers.
        [base("forbidden", forbidden_scope=True, verified_value=42.0),
         base("unauthorized", authorized=False, verified_value=42.0)],
        # 7. No verified values anywhere -> honest abstention.
        [base("a", verified_value=None), base("b", verified_value=None)],
        # 8. Explicit honest-abstention action can win phase 2.
        [base("bold-guess", verified_value=None),
         base("say-i-dont-know", honest_abstention=True, verified_value=0.5,
              value_evidence="honesty avoids acting on unverified value")],
        # 9. All disqualified -> refuse.
        [base("h1", unacceptable_harm=True, verified_value=10.0),
         base("h2", deceptive=True, verified_value=10.0)],
        # 10. Tie on value breaks deterministically by action_id.
        [base("b-action", verified_value=7.0),
         base("a-action", verified_value=7.0)],
    ]


# ---------------------------------------------------------------------------
# Consolidated cross-verification — proves the ONE canonical engine
# (kernel/value_calculus.py) governs behavior identically to this independent
# oracle. This is the consolidation proof: two independent implementations,
# one authoritative engine.
# ---------------------------------------------------------------------------

def _action_to_candidate(a: Action):
    """Adapt a simple Action to the canonical engine's rich Candidate.

    Maps the oracle's epistemic evidence (Optional[bool]) into the calculus's
    hard-gate flags, preserving the exact gate semantics:
      - established harm/deception/forbidden scope -> hard_violation (PROHIBITED)
      - unknown harm/truth -> hard flags None (NEEDS_EVIDENCE -> DEFERRED)
      - missing authority -> authorized=False (NEEDS_AUTHORITY -> DEFERRED)
      - consented + mitigated residual risk -> admissible (not prohibited)
      - verified_value None -> evidence_count=0 (unverified; never competes)
    """
    from kernel.value_calculus import Candidate, PVEstimate, QUALITY_DIMENSIONS

    consented_mitigated = bool(a.informed_consent and a.harm_mitigated)

    # --- Hard-gate mapping ------------------------------------------------
    hard_violation = False
    safety_safe: Optional[bool] = None

    if a.unacceptable_harm is True and not consented_mitigated:
        hard_violation = True
    elif (a.unacceptable_harm is None and a.harm_severity is not None
          and a.harm_probability is not None
          and float(a.harm_severity) >= 7.0 and float(a.harm_probability) > 0.05
          and not consented_mitigated):
        hard_violation = True
    elif a.unacceptable_harm is False:
        safety_safe = True
    elif consented_mitigated and (
        a.unacceptable_harm is True
        or (a.harm_severity is not None and a.harm_probability is not None
            and float(a.harm_severity) >= 7.0 and float(a.harm_probability) > 0.05)
    ):
        # The oracle explicitly admits consented + mitigated residual risk —
        # but only when there WAS established harm or HIGH assessed risk to
        # consent to and mitigate. The oracle is conservative: uharm=None
        # with low/unassessed risk always DEFERS, even if consent/mitigation
        # flags are set. Match that exactly.
        safety_safe = True
    # else: unacceptable_harm is None without high assessed risk -> unknown -> None

    if a.deceptive is True or a.forbidden_scope:
        hard_violation = True

    lawful: Optional[bool] = None
    if a.deceptive is True:
        lawful = False  # deception already triggers hard_violation; flag for receipt
    elif a.deceptive is False:
        lawful = True

    # --- Value mapping ----------------------------------------------------
    # verified_value None -> evidence_count=0 (unverified; never competes).
    # Otherwise B=verified_value with full confidence (the oracle's "verified").
    vv = a.verified_value
    if vv is None:
        pv = PVEstimate(B=0.0, H=0.0, C=0.0, R=0.0,
                        confidence={"B": 1.0, "H": 1.0, "C": 1.0, "R": 1.0},
                        evidence_count=0)
    else:
        pv = PVEstimate(B=max(0.0, float(vv)), H=0.0, C=0.0, R=0.0,
                        confidence={"B": 1.0, "H": 1.0, "C": 1.0, "R": 1.0},
                        evidence_count=1)

    # Quality at ceiling so the Q-gate never interferes with the cross-check;
    # the gates under test are the hard gates, not quality scoring.
    quality = {d: 10.0 for d in QUALITY_DIMENSIONS}
    confidence = {d: 1.0 for d in QUALITY_DIMENSIONS}

    return Candidate(
        candidate_id=a.action_id,
        quality=quality,
        confidence=confidence,
        pv=pv,
        authorized=a.authorized,
        hard_violation=hard_violation,
        lawful=lawful,
        rights_safe=True,
        privacy_safe=True,
        safety_safe=safety_safe,
        informed_consent=a.informed_consent,
        harm_mitigated=a.harm_mitigated,
        stakes="low",
        reversible=True,
    )


def _default_consolidation_profile():
    """A QualityProfile permissive on quality (ceiling in adapter) but strict
    on the hard gates — the gates under cross-verification."""
    from kernel.value_calculus import QualityProfile
    return QualityProfile(
        profile_id="CROSS-VERIFY",
        version="1.0",
        objective="cross-verification of consolidated engine vs oracle",
        q_accept=9.0,
        aggregate_confidence_floor=0.80,
        critical_confidence_floor=0.75,
        min_evidence_count=1,
    )


def cross_verify_consolidated(scenarios: Sequence[Sequence[Action]]) -> dict:
    """Prove the canonical engine agrees with the independent oracle.

    For each scenario: adapt Actions to Candidates, run value_calculus.decide()
    (the ONE authoritative engine) and PrincipleOracle.decide() (the
    independent oracle). They must agree on: disqualified set, admissible set,
    deferred set, chosen action. Outcomes must be in the same family
    (ACT<->ACT, REFUSE<->REFUSE, ASK<->ASK, ABSTAIN<->ABSTAIN/READ_MORE).

    Returns agreement evidence; raises AssertionError on divergence.
    """
    from kernel import value_calculus as vc

    profile = _default_consolidation_profile()
    oracle = PrincipleOracle()
    divergences: list[dict] = []

    # Outcome family mapping: oracle -> acceptable canonical outcomes.
    # The canonical engine distinguishes evidence-gap (READ_MORE) from
    # no-verified-value (ABSTAIN); the oracle folds both into ABSTAIN.
    family = {
        ACT: {vc.DECIDE_ACT},
        REFUSE: {vc.DECIDE_REFUSE},
        ASK: {vc.DECIDE_ASK},
        ABSTAIN: {vc.DECIDE_ABSTAIN, vc.DECIDE_READ_MORE},
    }

    for i, actions in enumerate(scenarios):
        candidates = [_action_to_candidate(a) for a in actions]
        canon = vc.decide(candidates, baseline_id="__none__", profile=profile)
        orac = oracle.decide(actions)

        canon_result = {
            "disqualified": sorted(canon["disqualified"]),
            "admissible": sorted(canon["admissible"]),
            "deferred": sorted(canon["deferred"]),
            "chosen": canon["chosen"],
        }
        oracle_result = {
            "disqualified": sorted(orac.disqualified_ids),
            "admissible": sorted(orac.admissible_ids),
            "deferred": sorted(orac.deferred_ids),
            "chosen": orac.chosen_action_id,
        }
        outcome_ok = canon["outcome"] in family.get(orac.outcome, set())

        if canon_result != oracle_result or not outcome_ok:
            divergences.append({
                "scenario": i,
                "canonical": {**canon_result, "outcome": canon["outcome"]},
                "oracle": {**oracle_result, "outcome": orac.outcome},
            })

    evidence = {
        "scenarios": len(scenarios),
        "divergences": divergences,
        "agreed": len(divergences) == 0,
    }
    assert evidence["agreed"], (
        f"canonical engine and oracle diverged on {len(divergences)} "
        f"scenario(s): {divergences[:3]}")
    return evidence
