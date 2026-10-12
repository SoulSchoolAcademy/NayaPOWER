"""Naya Canonical Decision Engine — ONE engine (Shawn's word, 2026-10-11).

"bring them together and put the best of them together" — no exception for
a second engine.

This module COMPOSES the two proven engines without rewriting either:

  Phase 1 — GATES (best of decision_principle):
      kernel.decision_principle hard gates (protect people / tell truth /
      respect authority) with the two-phase verdict space
      ADMISSIBLE / DISQUALIFIED / DEFERRED — disqualification is EXCLUSION,
      not outscoring; uncertainty DEFERS, never disqualifies.
      PLUS kernel.value_calculus.gate_candidate (Intent Doctrine, hard
      flags, tail risk, conflicts, authority, evidence/confidence floors),
      mapped into the same verdict space. Strictest verdict wins.

  Phase 2 — SCORE (best of value_calculus):
      kernel.value_calculus.evaluate_candidates — THE ONE ranking.
      The principle's contract "only verified value competes" is now
      machine-enforced: Phase 2 ranks on the calculus's conservative
      value (v_safe) with its confidence floors, not on caller-asserted
      numbers.

  Outcomes: ACT / ABSTAIN / REFUSE / ASK (the principle's honest outputs).
  Receipts: principle Decision + calculus build_decision_receipt.

Input is ONE dataclass, EngineAction, carrying both evidence surfaces
(gate evidence + scoring evidence); it projects to the principle's Action
and the calculus's Candidate internally — no information loss, no second
input type.

UDM front-end: from_udm_scored_option() adapts a Layer-4 scored option
{value, evidence, confidence} per dimension into an EngineAction, so the
UDM's evidence pipeline (L1 world model → L2 intent → L3 options → L4
evidence) submits to the canonical engine. The canonical engine performs
the ONLY ranking for decisions that flow through it.

Deterministic, dependency-free (stdlib + the two kernel engines).
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from typing import Mapping, Optional, Sequence

from kernel import decision_principle as dp
from kernel import value_calculus as vc

ENGINE_VERSION = "NAYA-DECISION-ENGINE-V1"
CANONICAL_RANKER = "kernel.value_calculus.evaluate_candidates"

# ---------------------------------------------------------------------------
# Verdicts — the principle's space is the canonical one.
# ---------------------------------------------------------------------------

ADMISSIBLE = dp.ADMISSIBLE
DISQUALIFIED = dp.DISQUALIFIED
DEFERRED = dp.DEFERRED

# Outcomes — the principle's honest outputs.
ACT = dp.ACT
ABSTAIN = dp.ABSTAIN
REFUSE = dp.REFUSE
ASK = dp.ASK


# ---------------------------------------------------------------------------
# EngineAction — the ONE input type for the canonical engine.
#
# It carries both evidence surfaces:
#   * gate evidence  (the principle's Action needs)
#   * scoring evidence (the calculus's Candidate needs)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class EngineAction:
    action_id: str
    description: str = ""

    # --- gate evidence (→ decision_principle.Action) -----------------------
    unacceptable_harm: Optional[bool] = None
    harm_severity: Optional[float] = None
    harm_probability: Optional[float] = None
    harm_mitigated: bool = False
    informed_consent: bool = False
    deceptive: Optional[bool] = None
    authorized: bool = False
    forbidden_scope: bool = False
    honest_abstention: bool = False

    # --- scoring evidence (→ value_calculus.Candidate) --------------------
    # quality: 0..10 per QUALITY_DIMENSION; confidence: 0..1 per dimension.
    # None quality = unknown → confidence 0 (the calculus then honestly
    # defers via its evidence/confidence floors; nothing is invented).
    quality: Mapping[str, Optional[float]] = field(default_factory=dict)
    confidence: Mapping[str, float] = field(default_factory=dict)
    value_evidence: str = ""          # provenance of the value claim

    # present-value components (non-negative; unknown → 0 with low confidence)
    pv_benefit: float = 0.0
    pv_harm: float = 0.0
    pv_cost: float = 0.0
    pv_residual_risk: float = 0.0
    pv_confidence: float = 0.0        # shared component confidence 0..1
    evidence_count: int = 0

    intent_to_harm: bool = False
    hard_violation: bool = False
    lawful: Optional[bool] = None
    rights_safe: Optional[bool] = None
    privacy_safe: Optional[bool] = None
    safety_safe: Optional[bool] = None
    stakes: str = "low"
    reversible: bool = True
    human_authorized: bool = False
    tails: Sequence[vc.TailRisk] = ()
    stakeholder_harms: Mapping[str, float] = field(default_factory=dict)
    principal_conflict: bool = False
    coordination_conflict: bool = False
    jurisdiction_conflict: bool = False
    uncertainty_penalty: float = 0.0
    tail_penalty: float = 0.0
    dependency_unlock: float = 0.0
    human_burden: float = 0.0
    is_baseline: bool = False


def _to_principle_action(a: EngineAction) -> dp.Action:
    return dp.Action(
        action_id=a.action_id,
        description=a.description,
        unacceptable_harm=a.unacceptable_harm,
        harm_severity=a.harm_severity,
        harm_probability=a.harm_probability,
        harm_mitigated=a.harm_mitigated,
        informed_consent=a.informed_consent,
        deceptive=a.deceptive,
        authorized=a.authorized,
        forbidden_scope=a.forbidden_scope,
        verified_value=None,  # Phase 2 derives this from the calculus.
        value_evidence=a.value_evidence,
        honest_abstention=a.honest_abstention,
    )


def _to_calculus_candidate(a: EngineAction) -> vc.Candidate:
    quality = {d: a.quality.get(d) for d in vc.QUALITY_DIMENSIONS}
    confidence = {
        d: max(0.0, min(1.0, float(a.confidence.get(d, 0.0))))
        for d in vc.QUALITY_DIMENSIONS
    }
    pv = vc.PVEstimate(
        B=max(0.0, float(a.pv_benefit)),
        H=max(0.0, float(a.pv_harm)),
        C=max(0.0, float(a.pv_cost)),
        R=max(0.0, float(a.pv_residual_risk)),
        confidence={k: max(0.0, min(1.0, float(a.pv_confidence)))
                    for k in ("B", "H", "C", "R")},
        evidence_count=max(0, int(a.evidence_count)),
    )
    return vc.Candidate(
        candidate_id=a.action_id,
        quality=quality,
        confidence=confidence,
        pv=pv,
        tails=tuple(a.tails),
        stakeholder_harms=dict(a.stakeholder_harms) or None,
        authorized=a.authorized,
        human_authorized=a.human_authorized,
        hard_violation=a.hard_violation,
        intent_to_harm=a.intent_to_harm,
        lawful=a.lawful,
        rights_safe=a.rights_safe,
        privacy_safe=a.privacy_safe,
        safety_safe=a.safety_safe,
        stakes=a.stakes,
        reversible=a.reversible,
        principal_conflict=a.principal_conflict,
        coordination_conflict=a.coordination_conflict,
        jurisdiction_conflict=a.jurisdiction_conflict,
        uncertainty_penalty=a.uncertainty_penalty,
        tail_penalty=a.tail_penalty,
        dependency_unlock=a.dependency_unlock,
        human_burden=a.human_burden,
        is_baseline=a.is_baseline,
    )


# ---------------------------------------------------------------------------
# Phase 1 — unified gates. Both gate layers run; the strictest verdict wins.
# DISQUALIFIED (exclusion) can never be outscored back in.
# ---------------------------------------------------------------------------

_VERDICT_STRICTNESS = {ADMISSIBLE: 0, DEFERRED: 1, DISQUALIFIED: 2}


def _unified_gate(action: EngineAction, profile: vc.QualityProfile,
                  risk_policy: vc.RiskPolicy) -> tuple[str, list]:
    """Run both gate layers; return (verdict, gate_records).

    gate_records: list of dicts {layer, verdict, reasons} for the receipt.
    """
    records = []

    p_verdict, p_results = dp.run_hard_gates(_to_principle_action(action))
    records.append({
        "layer": "decision_principle",
        "verdict": p_verdict,
        "reasons": [r for res in p_results for r in res.reasons],
    })

    c_gate, c_reasons, _q = vc.gate_candidate(
        _to_calculus_candidate(action), profile, risk_policy)
    c_verdict = dp.verdict_from_calculus_gate(c_gate)
    records.append({
        "layer": "value_calculus",
        "verdict": c_verdict,
        "reasons": list(c_reasons),
    })

    verdict = max((p_verdict, c_verdict),
                  key=lambda v: _VERDICT_STRICTNESS[v])
    return verdict, records


# ---------------------------------------------------------------------------
# Baseline — the decision-compression doctrine always includes
# "do nothing / wait". evaluate_candidates requires exactly one baseline.
# ---------------------------------------------------------------------------

def _do_nothing_baseline() -> EngineAction:
    zero_q = {d: 0.0 for d in vc.QUALITY_DIMENSIONS}
    zero_c = {d: 1.0 for d in vc.QUALITY_DIMENSIONS}
    return EngineAction(
        action_id="do_nothing",
        description="Do nothing / wait — the honest default alternative.",
        unacceptable_harm=False,
        deceptive=False,
        authorized=True,
        quality=zero_q,
        confidence=zero_c,
        value_evidence="baseline: inaction has zero delta by definition",
        pv_confidence=1.0,
        evidence_count=1,
        lawful=True,
        rights_safe=True,
        privacy_safe=True,
        safety_safe=True,
        honest_abstention=True,
        is_baseline=True,
    )


# ---------------------------------------------------------------------------
# UDM adapter — Layer-4 evidence submits to the canonical engine.
#
# Maps a Layer-4 scored option's five evidence dimensions
# (mission_value, evidence, risk, cost, urgency — each {value, evidence,
# confidence}, value None = UNKNOWN) into an EngineAction's quality dims
# (0..10) + confidence (0..1). The mapping is documented, monotonic, and
# honest: UNKNOWN dims become quality None (missing dimension) with
# confidence 0.0, which the calculus's floors then turn into
# NEEDS_EVIDENCE — never a silent rank.
#
#   objective_fit       ← mission_value   (does it close the real gap?)
#   evidence_sufficiency← evidence        (how proven?)
#   applicability       ← mission_value   (relevance to the stated intent)
#   robustness          ← 1 − risk        (risk = fragility)
#   reversibility       ← 1 − risk        (risk includes irreversibility)
#   blast_containment   ← 1 − risk
#   simplicity          ← 1 − cost
#
# PV components come straight from the dims with the dims' confidence;
# nothing is invented — evidence_count counts known dims, and low
# confidence flows into the calculus's aggregate/critical floors.
# ---------------------------------------------------------------------------

_UDM_QUALITY_MAP = {
    "objective_fit": ("mission_value", False),
    "evidence_sufficiency": ("evidence", False),
    "applicability": ("mission_value", False),
    "robustness": ("risk", True),
    "reversibility": ("risk", True),
    "blast_containment": ("risk", True),
    "simplicity": ("cost", True),
}


def from_udm_scored_option(option: Mapping,
                           intent: Optional[Mapping] = None) -> EngineAction:
    """Adapt a UDM Layer-4 scored option into an EngineAction.

    option: {id, title, gated, gate_reason, dimensions: {name: {value,
    evidence, confidence}}}. intent: Layer-2 intent dict; when it
    requires Shawn's word (requires_shawn / protected gates hit), the
    action is marked unauthorized so the unified gates defer it.
    """
    intent = intent or {}
    dims = option.get("dimensions") or {}

    def dim(name):
        d = dims.get(name) or {}
        v = d.get("value")
        return (None if v is None else max(0.0, min(1.0, float(v))),
                str(d.get("evidence") or ""),
                max(0.0, min(1.0, float(d.get("confidence") or 0.0))))

    quality: dict = {}
    confidence: dict = {}
    evidence_bits = []
    known = 0
    for qdim, (lname, invert) in _UDM_QUALITY_MAP.items():
        v, ev, conf = dim(lname)
        if v is None:
            # UNKNOWN stays unknown: quality None (missing dimension) with
            # confidence 0. The calculus's floors then defer honestly —
            # nothing is invented, and the receipt names the missing dims.
            quality[qdim] = None
            confidence[qdim] = 0.0
        else:
            quality[qdim] = round((1.0 - v if invert else v) * 10.0, 3)
            confidence[qdim] = conf
            known += 1
        if ev:
            evidence_bits.append(f"{lname}: {ev}")

    mv, _, mv_conf = dim("mission_value")
    risk, _, risk_conf = dim("risk")
    cost, _, cost_conf = dim("cost")

    gated = bool(option.get("gated"))
    requires_shawn = bool(intent.get("requires_shawn")) or gated

    title = str(option.get("title") or "")
    provenance = "; ".join(evidence_bits) if evidence_bits else \
        "no evidence supplied by Layer 4"

    return EngineAction(
        action_id=str(option.get("id") or option.get("option_id") or "udm-option"),
        description=title,
        # Gate evidence: a Layer-4 wall (REQUIRES_SHAWN) means the action
        # lacks authority — the unified gates will DEFER it, never rank it.
        authorized=not requires_shawn,
        forbidden_scope=False,
        unacceptable_harm=False,
        deceptive=False,
        quality=quality,
        confidence=confidence,
        value_evidence=f"{title} — {provenance}" if title else provenance,
        pv_benefit=(mv * 10.0) if mv is not None else 0.0,
        pv_harm=(risk * 10.0) if risk is not None else 0.0,
        pv_cost=(cost * 10.0) if cost is not None else 0.0,
        pv_residual_risk=(risk * 10.0) if risk is not None else 0.0,
        pv_confidence=min(mv_conf, risk_conf, cost_conf),
        evidence_count=known,
        lawful=True,
        rights_safe=True,
        privacy_safe=True,
        safety_safe=True,
    )


# ---------------------------------------------------------------------------
# The canonical engine.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class EngineDecision:
    outcome: str                       # ACT | ABSTAIN | REFUSE | ASK
    chosen_action_id: Optional[str]
    chosen_v_safe: Optional[float]     # calculus conservative value of choice
    admissible_ids: tuple
    disqualified_ids: tuple
    deferred_ids: tuple
    ranking: tuple                     # admissible, best first (v_safe order)
    evaluation: dict                   # full calculus evaluate_candidates output
    receipts: tuple                    # per-action unified gate records
    receipt: dict                      # calculus decision receipt bundle
    note: str = ""


class DecisionEngine:
    """ONE canonical decision engine.

    Phase 1: unified hard gates (principle + calculus) — exclusion first.
    Phase 2: THE one ranking — value_calculus.evaluate_candidates over the
    admissible set only. "Only verified value competes" is machine-enforced
    by the calculus's conservative value + confidence floors.
    """

    def __init__(self, profile: Optional[vc.QualityProfile] = None,
                 risk_policy: Optional[vc.RiskPolicy] = None):
        self.profile = profile or vc.QualityProfile(
            profile_id="canonical-default",
            version="1",
            objective="maximum verified human value per moment",
        )
        self.risk_policy = risk_policy or vc.RiskPolicy()

    def decide(self, actions: Sequence[EngineAction],
               objective: str = "",
               stakeholders: Sequence[str] = (),
               decision_id: str = "engine-decision") -> EngineDecision:
        actions = list(actions)

        if not actions:
            return EngineDecision(
                outcome=ABSTAIN, chosen_action_id=None, chosen_v_safe=None,
                admissible_ids=(), disqualified_ids=(), deferred_ids=(),
                ranking=(), evaluation={},
                receipts=(), receipt={},
                note="No actions were proposed. Honest output: nothing to decide.",
            )

        # ---- Phase 1: unified gates ---------------------------------------
        verdicts: dict = {}
        records: dict = {}
        for action in actions:
            verdict, recs = _unified_gate(action, self.profile,
                                          self.risk_policy)
            verdicts[action.action_id] = verdict
            records[action.action_id] = recs

        admissible = [a for a in actions
                      if verdicts[a.action_id] == ADMISSIBLE]
        disqualified = [a for a in actions
                        if verdicts[a.action_id] == DISQUALIFIED]
        deferred = [a for a in actions
                    if verdicts[a.action_id] == DEFERRED]

        # ---- Phase 2: THE one ranking -------------------------------------
        evaluation = self._score_admissible(admissible)
        calc_decision = evaluation.get("decision")
        selected = evaluation.get("selected")

        if calc_decision == vc.ACT and selected is not None:
            outcome, chosen = ACT, selected
        elif calc_decision == vc.ASK:
            outcome, chosen = ASK, None
        elif calc_decision == vc.REFUSE:
            outcome, chosen = REFUSE, None
        elif not admissible and deferred:
            # Nothing admissible; deferred actions may proceed once the gap
            # closes. Authority gaps ask; evidence gaps abstain honestly.
            outcome = (ASK if self._deferred_on_authority(deferred, records)
                       else ABSTAIN)
            chosen = None
        elif not admissible:
            outcome, chosen = REFUSE, None
        else:
            # Admissible actions exist but none cleared value/confidence.
            outcome, chosen = ABSTAIN, None

        chosen_v_safe = None
        if chosen is not None:
            row = next(r for r in evaluation["rows"]
                       if r["candidate_id"] == chosen)
            chosen_v_safe = row["v_safe"]

        ranking = tuple(r["candidate_id"]
                        for r in evaluation.get("top3", []))

        receipts = tuple(
            (a.action_id, verdicts[a.action_id], tuple(records[a.action_id]))
            for a in actions
        )

        receipt = vc.build_decision_receipt(
            decision_id=decision_id,
            objective=objective or self.profile.objective,
            baseline_id="do_nothing",
            stakeholders=list(stakeholders),
            horizon="decision",
            evaluation=evaluation,
            authority_basis="canonical-engine-v1",
            evidence_refs=[a.value_evidence for a in admissible
                           if a.value_evidence],
            observation_window={},
            verification="UNVERIFIED",
        )

        note = self._note(outcome, chosen, admissible, disqualified, deferred)
        return EngineDecision(
            outcome=outcome, chosen_action_id=chosen,
            chosen_v_safe=chosen_v_safe,
            admissible_ids=tuple(a.action_id for a in admissible),
            disqualified_ids=tuple(a.action_id for a in disqualified),
            deferred_ids=tuple(a.action_id for a in deferred),
            ranking=ranking, evaluation=evaluation, receipts=receipts,
            receipt=receipt, note=note,
        )

    def _score_admissible(self, admissible: Sequence[EngineAction]) -> dict:
        """Phase 2: THE one ranking — evaluate_candidates over admissible.

        The do-nothing baseline is synthesized when the caller provides none
        (decision-compression doctrine: always include do-nothing/wait).
        """
        candidates = [_to_calculus_candidate(a) for a in admissible]
        if not any(c.is_baseline for c in candidates):
            candidates.append(_to_calculus_candidate(_do_nothing_baseline()))
        return vc.evaluate_candidates(
            candidates, "do_nothing", self.profile, self.risk_policy)

    @staticmethod
    def _deferred_on_authority(deferred, records) -> bool:
        authority_reasons = {
            "AUTHORITY_MISSING", "NEEDS_AUTHORITY",
            "CONSEQUENTIAL_OR_IRREVERSIBLE", "CONFLICT_REQUIRES_GOVERNANCE",
        }
        for a in deferred:
            for g in records[a.action_id]:
                if any(r in authority_reasons for r in g["reasons"]):
                    return True
        return False

    @staticmethod
    def _note(outcome, chosen, admissible, disqualified, deferred) -> str:
        if outcome == ACT:
            return (f"Chose {chosen} on verified value from "
                    f"{len(admissible)} admissible action(s); "
                    f"{len(disqualified)} disqualified, "
                    f"{len(deferred)} deferred.")
        if outcome == REFUSE:
            return ("Every candidate was disqualified on the merits. "
                    "Nothing may proceed. Honest output: 'this isn't safe'.")
        if outcome == ASK:
            return ("Candidates are deferred pending authority. "
                    "Honest output: ask for the missing authority.")
        return ("No admissible action has verified value. "
                "Honest output: 'I don't know yet' — abstaining rather "
                "than guessing.")


def decide_words(objective: str, options: Sequence[Mapping],
                 decision_id: str = "engine-words") -> EngineDecision:
    """Decide from words: UDM-style scored options straight to a verdict.

    `options` are Layer-4-style scored option dicts (id/title/gated/
    gate_reason/dimensions). Returns the canonical EngineDecision.
    """
    engine = DecisionEngine()
    actions = [from_udm_scored_option(o) for o in options]
    return engine.decide(actions, objective=objective,
                         decision_id=decision_id)


# ---------------------------------------------------------------------------
# CLI — parity with the UDM layers: workers can invoke the canonical engine
# from the shell. Reads EngineAction dicts or UDM-style scored options.
# ---------------------------------------------------------------------------

def _cli_action_from_dict(d: Mapping) -> EngineAction:
    known = {f.name for f in EngineAction.__dataclass_fields__.values()}
    return EngineAction(**{k: v for k, v in d.items() if k in known})


def main(argv=None) -> int:
    import argparse
    import json

    ap = argparse.ArgumentParser(
        description="Naya canonical decision engine — ONE engine.")
    ap.add_argument("--actions", default=None,
                    help="JSON list of EngineAction dicts")
    ap.add_argument("--udm-options", default=None,
                    help="JSON list of UDM Layer-4 scored option dicts")
    ap.add_argument("--objective", default="",
                    help="decision objective in words")
    ap.add_argument("--decision-id", default="engine-cli")
    ap.add_argument("--stdin", action="store_true",
                    help="read the JSON payload from stdin")
    args = ap.parse_args(argv)

    payload = None
    if args.stdin:
        payload = json.load(sys.stdin)
    elif args.actions:
        payload = {"actions": json.loads(args.actions)}
    elif args.udm_options:
        payload = {"udm_options": json.loads(args.udm_options)}
    else:
        ap.error("one of --actions, --udm-options, or --stdin is required")

    engine = DecisionEngine()
    if "udm_options" in payload:
        actions = [from_udm_scored_option(o)
                   for o in payload["udm_options"]]
    else:
        actions = [_cli_action_from_dict(d) for d in payload["actions"]]
    d = engine.decide(actions, objective=args.objective,
                      decision_id=args.decision_id)
    out = {
        "outcome": d.outcome,
        "chosen_action_id": d.chosen_action_id,
        "chosen_v_safe": d.chosen_v_safe,
        "admissible_ids": list(d.admissible_ids),
        "disqualified_ids": list(d.disqualified_ids),
        "deferred_ids": list(d.deferred_ids),
        "ranking": list(d.ranking),
        "receipt": d.receipt,
        "note": d.note,
        "engine_version": ENGINE_VERSION,
        "canonical_ranker": CANONICAL_RANKER,
    }
    print(json.dumps(out, indent=2, default=str))
    return 0 if d.outcome in (ACT, ABSTAIN, ASK) else 2


if __name__ == "__main__":
    sys.exit(main())
