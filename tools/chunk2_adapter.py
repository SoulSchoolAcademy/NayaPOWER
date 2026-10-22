#!/usr/bin/env python3
"""
Chunk-2 adapter: UDM evidence_scorer dimensions -> engine primitives
(Naya Eta, w211 builder task — DECISION.json chunk2-adapter-builder-task).

Asserted mapping (consolidation scope, w201 line 31):
  mission_value -> delta_value
  risk          -> gate_candidate + TailRisk
  cost          -> stakes
  evidence      -> freshness_confidence -> verification_state
  urgency       -> horizon on the receipt

RATIFIED vs CHOSEN (P-011 honesty line — read before citing):
  RATIFIED (from engine code at tip ba6263870425, not invented here):
    - TailRisk: severity 0-10, probability 0-1; RiskPolicy defaults
      severity_threshold=9.0, probability_threshold=0.01, response=PROHIBITED.
    - Candidate.stakes in {"low","high","consequential"} (STAKE_ORDER).
    - Quality dimensions 0-10 (score_quality _norm10).
    - verification_state() -> FAIL | PASS_PENDING_WINDOW | VERIFIED_PASS;
      build_decision_receipt verification also admits UNVERIFIED, ESCALATE.
    - d_verified clamp [-9,+9] (ZERO VALUE LAW, engine code).
    - Horizon vocabulary: "immediate","30d","6mo","cumulative"
      (kernel/protocol/conflict_resolution.py).
    - gate_candidate order: intent -> hard_violation -> hard flags ->
      tails -> stakeholder harms -> conflicts -> authority -> evidence floors.
  CHOSEN (adapter parameters v1 — calibration, NOT ratified):
    - SCALE9 = 9.0: UDM 0-1 magnitudes x9 into the -9/+9-compatible band.
    - stakes thresholds at 1/3 and 2/3 of UDM cost.
    - urgency->horizon cut points at 0.75 / 0.50 / 0.25.
    - evidence floors for PASS_PENDING_WINDOW: value>=0.75, conf>=0.75.
  A different seat re-calibrating these constants changes numbers, not the
  mechanism. Nothing here claims a ratified number that isn't.

ANTI-FABRICATION CORE (P-003): an UNKNOWN dimension (value=None) never
becomes a favorable number. Any UNKNOWN in {mission_value, risk, cost,
evidence} forces adapter_gate -> NEEDS_EVIDENCE with ADAPTER_UNKNOWN_<dim>
reasons. The option is excluded from evaluate_candidates' eligible set
(gate != ADMISSIBLE), so no ranking ever rests on a fabricated input.

SEAM CONTRACT: the UDM protected-gate wall (evidence_scorer PROTECTED_PATTERNS)
stays in tools/ and runs BEFORE the adapter. Options reaching the adapter
carry wall_passed=True; the adapter translates that explicit input into the
engine hard flags (lawful/rights_safe/privacy_safe/safety_safe=True) and
authorized/human_authorized=True. wall_passed=False (default) -> hard flags
stay None and engine gate returns NEEDS_EVIDENCE. The adapter never invents
clearance; it translates a named precondition and records it in meta.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Read-only import from the live tree (the adapter consumes the engine,
# it does not modify it). Repo-relative: tools/ and kernel/ are siblings
# at the repo root, so a cold successor importing from main gets the same
# engine the adapter was validated against.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "kernel"))

from value_calculus import (  # noqa: E402
    ADMISSIBLE,
    NEEDS_AUTHORITY,
    NEEDS_EVIDENCE,
    PROHIBITED,
    PVEstimate,
    QualityProfile,
    RiskPolicy,
    TailRisk,
    Candidate,
    gate_candidate,
    score_quality,
    verification_state,
)

ADAPTER_VERSION = "chunk2-adapter-v1"
ENGINE_PIN = "DECISION-VALUE-CALCULUS-V2.1"

# ---- Chosen constants (v1 calibration, NOT ratified) ----
SCALE9 = 9.0
STAKE_LOW_MAX = 1.0 / 3.0
STAKE_HIGH_MAX = 2.0 / 3.0
EVIDENCE_VALUE_FLOOR = 0.75
EVIDENCE_CONF_FLOOR = 0.75
# ---- Ratified horizon vocabulary (conflict_resolution.py) ----
HORIZONS = ("immediate", "30d", "6mo", "cumulative")

KNOWN_DIMS = ("mission_value", "evidence", "risk", "cost", "urgency")
# Dimensions whose UNKNOWN blocks admissibility.
BLOCKING_DIMS = ("mission_value", "risk", "cost", "evidence")


def _val(dim: dict):
    v = dim.get("value")
    return None if v is None else float(v)


# ---------------------------------------------------------------------------
# Per-dimension mapping functions (the P4 contract: each depends ONLY on its
# own dimension — verified byte-identically in run_e2e.py).
# ---------------------------------------------------------------------------

def map_mission_value(dim: dict):
    """mission_value (0-1) -> pv.B magnitude. None stays None (UNKNOWN)."""
    v = _val(dim)
    return None if v is None else SCALE9 * v


def map_risk(dim: dict) -> TailRisk | None:
    """risk (0-1) -> TailRisk. severity=10*risk, probability=risk.

    Ratified anchors: severity_threshold=9.0 (engine default) => risk>=0.9
    trips the tail gate; risk=1.0 => severity=10.0, prob=1.0 > 0.01 =>
    gate_candidate returns PROHIBITED (the w206 feasibility bound, now
    mechanical). UNKNOWN risk -> None (never a fabricated severity).
    """
    v = _val(dim)
    if v is None:
        return None
    return TailRisk(severity=10.0 * v, probability=v, harm_class="udm-risk")


def map_cost(dim: dict):
    """cost (0-1) -> (pv.C magnitude, stakes)."""
    v = _val(dim)
    if v is None:
        return None, None
    c = SCALE9 * v
    stakes = (
        "low" if v < STAKE_LOW_MAX
        else "high" if v < STAKE_HIGH_MAX
        else "consequential"
    )
    return c, stakes


def map_evidence(dim: dict):
    """evidence -> (freshness_confidence, receipt verification, evidence_sufficiency 0-10).

    freshness_confidence IS the UDM confidence (no invention). The receipt
    verification uses engine verification_state's vocabulary but never claims
    a post-observation state: FAIL and VERIFIED_PASS require an observed
    outcome, which scoring time does not have (P-011).
    """
    v = _val(dim)
    conf = float(dim.get("confidence", 0.0) or 0.0)
    if v is None:
        return conf, "UNVERIFIED", None
    verification = (
        "PASS_PENDING_WINDOW"
        if (v >= EVIDENCE_VALUE_FLOOR and conf >= EVIDENCE_CONF_FLOOR)
        else "UNVERIFIED"
    )
    # Sanity: the emitted string is inside the engine's admitted vocabulary.
    assert verification in ("UNVERIFIED", "PASS_PENDING_WINDOW", "VERIFIED_PASS", "FAIL", "ESCALATE")
    return conf, verification, 10.0 * v


def map_urgency(dim: dict) -> str:
    """urgency (0-1) -> receipt horizon. Receipt-scheduling hint only;
    never enters scoring. UNKNOWN -> least-committal 'cumulative'."""
    v = _val(dim)
    if v is None:
        return "cumulative"
    if v >= 0.75:
        return "immediate"
    if v >= 0.50:
        return "30d"
    if v >= 0.25:
        return "6mo"
    return "cumulative"


# ---------------------------------------------------------------------------
# Option assembly
# ---------------------------------------------------------------------------

def adapt_option(option_id: str, dims: dict, *, wall_passed: bool = False,
                 baseline: bool = False) -> tuple[Candidate, dict]:
    """Adapt one UDM-scored option into (engine Candidate, meta).

    dims: {mission_value, evidence, risk, cost, urgency} each
          {"value": 0-1|None, "evidence": [...], "confidence": 0-1}.
    """
    for d in KNOWN_DIMS:
        if d not in dims:
            raise ValueError(f"missing dimension: {d}")

    unknown = [d for d in BLOCKING_DIMS if _val(dims[d]) is None]

    b = map_mission_value(dims["mission_value"])
    tail = map_risk(dims["risk"])
    c, stakes = map_cost(dims["cost"])
    freshness_conf, verification, ev_suff = map_evidence(dims["evidence"])
    horizon = map_urgency(dims["urgency"])

    def conf_of(d):
        return float(dims[d].get("confidence", 0.0) or 0.0)

    pv = PVEstimate(
        B=0.0 if b is None else b,
        H=0.0,
        C=0.0 if c is None else c,
        R=0.0 if tail is None else SCALE9 * _val(dims["risk"]),
        confidence={
            "B": conf_of("mission_value"),
            "H": 0.0,
            "C": conf_of("cost"),
            "R": conf_of("risk"),
        },
        evidence_count=len(dims["evidence"].get("evidence") or []),
    )

    mv = _val(dims["mission_value"])
    quality = {
        "objective_fit": None if mv is None else 10.0 * mv,
        "evidence_sufficiency": ev_suff,
        "applicability": None,
        "robustness": None,
        "reversibility": None,
        "blast_containment": None,
        "simplicity": None,
    }
    qconf = {
        "objective_fit": conf_of("mission_value"),
        "evidence_sufficiency": conf_of("evidence"),
        "applicability": 0.0,
        "robustness": 0.0,
        "reversibility": 0.0,
        "blast_containment": 0.0,
        "simplicity": 0.0,
    }

    hard = True if wall_passed else None
    candidate = Candidate(
        candidate_id=option_id,
        quality=quality,
        confidence=qconf,
        pv=pv,
        tails=() if tail is None else (tail,),
        authorized=wall_passed,
        human_authorized=wall_passed,
        lawful=hard,
        rights_safe=hard,
        privacy_safe=hard,
        safety_safe=hard,
        stakes="consequential" if stakes is None else stakes,
        reversible=True,
        tail_penalty=0.0 if tail is None else SCALE9 * _val(dims["risk"]),
        # urgency maps to horizon ONLY (asserted mapping); it does not feed
        # dependency_unlock — that would be a second, unasserted use.
        dependency_unlock=0.0,
        is_baseline=baseline,
    )
    meta = {
        "adapter_version": ADAPTER_VERSION,
        "engine_pin": ENGINE_PIN,
        "unknown_dimensions": unknown,
        "freshness_confidence": freshness_conf,
        "horizon": horizon,
        "verification": verification,
        "wall_passed": wall_passed,
        "chosen_constants": {
            "SCALE9": SCALE9,
            "STAKE_LOW_MAX": STAKE_LOW_MAX,
            "STAKE_HIGH_MAX": STAKE_HIGH_MAX,
            "EVIDENCE_VALUE_FLOOR": EVIDENCE_VALUE_FLOOR,
            "EVIDENCE_CONF_FLOOR": EVIDENCE_CONF_FLOOR,
        },
    }
    return candidate, meta


def adapter_gate(candidate: Candidate, meta: dict, profile: QualityProfile,
                 risk_policy: RiskPolicy = RiskPolicy()) -> tuple[str, list[str], dict]:
    """Gate with the anti-fabrication wrapper: UNKNOWN -> NEEDS_EVIDENCE
    before the engine gate ever sees the candidate."""
    q = score_quality(candidate, profile)
    if meta["unknown_dimensions"]:
        reasons = ["ADAPTER_UNKNOWN_" + d.upper() for d in meta["unknown_dimensions"]]
        return NEEDS_EVIDENCE, reasons, q
    return gate_candidate(candidate, profile, risk_policy)
