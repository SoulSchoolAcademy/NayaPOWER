#!/usr/bin/env python3
"""
Tests for tools/chunk2_adapter.py — the UDM evidence_scorer -> engine
value-calculus seam (Naya Eta, DECISION).

Provenance: adapted from the w211 builder-task e2e runner
(run_e2e.py, PASS exit 0 at tip ba6263870425, zero network) and the
w203 chunk-2 mapping properties (PASS against live code at tip
ba6263870425). This file is self-contained: a cold successor checking
out main gets all five properties with no workspace paths.

Properties:
  P1 weight-sign preservation (UDM side: mapping never inverts risk/cost)
  P2 UNKNOWN propagation (anti-fabrication: UNKNOWN -> None, never 0.0)
  P3 risk monotonicity end-to-end (real adapter: monotone gates,
      risk=1.0 -> PROHIBITED via the ratified tail threshold severity 9.0,
      ordering preserved vs UDM combine())
  P4 dimension independence end-to-end (real adapter: each mapped
      primitive depends ONLY on its own dimension; pv.B byte-identical
      across a cost sweep; UNKNOWN option -> NEEDS_EVIDENCE ADAPTER_UNKNOWN_*)
  P5 byte-shape contract (UDM dimension names stable — the mapping keys
      off them)

P-011 honesty line (read before citing): P3(b) uses the RATIFIED engine
default RiskPolicy (severity_threshold=9.0) — risk>=0.9 trips the tail
gate, risk=1.0 -> PROHIBITED is the engine's decision, not the adapter's.
The adapter's CHOSEN constants (SCALE9, stake thresholds, evidence
floors, urgency cutpoints) are v1 guesses documented unratified in the
module docstring; calibrating them against the 54+30 UDM tests is a
separate area-list item (calibrate-adapter-constants).
"""

from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "kernel"))

import evidence_scorer as es  # noqa: E402
from value_calculus import (  # noqa: E402
    ADMISSIBLE,
    NEEDS_AUTHORITY,
    NEEDS_EVIDENCE,
    PROHIBITED,
    QualityProfile,
    RiskPolicy,
    evaluate_candidates,
)
from chunk2_adapter import (  # noqa: E402
    adapt_option,
    adapter_gate,
    map_mission_value,
    map_risk,
    map_urgency,
)

PROFILE = QualityProfile(profile_id="chunk2", version="1", objective="chunk2")
POLICY = RiskPolicy()  # engine defaults: severity 9.0, prob 0.01, PROHIBITED

GATE_STRENGTH = {
    ADMISSIBLE: 0,
    NEEDS_EVIDENCE: 1,
    NEEDS_AUTHORITY: 2,
    PROHIBITED: 3,
}


def dims(mv=0.8, ev=0.8, risk=0.2, cost=0.2, urg=0.5, conf=0.9):
    def d(v):
        return {"value": v, "evidence": ["t"], "confidence": conf}

    return {
        "mission_value": d(mv),
        "evidence": d(ev),
        "risk": d(risk),
        "cost": d(cost),
        "urgency": d(urg),
    }


# ---------------------------------------------------------------------------
# P1: Weight-sign preservation (UDM side of the seam)
# ---------------------------------------------------------------------------

def test_p1_weight_signs_preserved():
    """UDM weight signs must match the mapping's direction claims.

    mission_value (+0.35), evidence (+0.25), urgency (+0.10) are
    'higher is better'; risk (-0.20), cost (-0.10) are 'higher is worse'.
    If a weight flips sign, the mapping would invert preferences silently.
    """
    better = ["mission_value", "evidence", "urgency"]
    worse = ["risk", "cost"]
    for dim in better:
        assert es.WEIGHTS[dim] > 0, (
            f"P1 VIOLATION: {dim} must be 'higher is better' "
            f"(weight > 0), got {es.WEIGHTS[dim]}"
        )
    for dim in worse:
        assert es.WEIGHTS[dim] < 0, (
            f"P1 VIOLATION: {dim} must be 'higher is worse' "
            f"(weight < 0), got {es.WEIGHTS[dim]}"
        )


# ---------------------------------------------------------------------------
# P2: UNKNOWN propagation (anti-fabrication, UDM side)
# ---------------------------------------------------------------------------

def test_p2_unknown_not_zero():
    """UNKNOWN dimensions must be excluded, never zeroed.

    combine() with all UNKNOWN must return (None, 0.0) — an honest
    'cannot score' — and a single known dimension must renormalize to
    its own value (UNKNOWN dims must not dilute the total toward zero).
    """
    dims_all_unknown = {
        k: {"value": None, "confidence": 0.0}
        for k in ("mission_value", "evidence", "risk", "cost", "urgency")
    }
    total, conf = es.combine(dims_all_unknown)
    assert total is None, (
        f"P2 VIOLATION: all-UNKNOWN must yield total=None, got {total}"
    )

    dims_one_known = {
        "mission_value": {"value": 0.8, "confidence": 0.9},
        "evidence": {"value": None, "confidence": 0.0},
        "risk": {"value": None, "confidence": 0.0},
        "cost": {"value": None, "confidence": 0.0},
        "urgency": {"value": None, "confidence": 0.0},
    }
    total, conf = es.combine(dims_one_known)
    # mission_value weight 0.35, value 0.8 -> 0.35*0.8/0.35 = 0.8
    # (renormalized over known weights only)
    assert total is not None and abs(total - 0.8) < 0.001, (
        f"P2 VIOLATION: single-known dimension must renormalize to 0.8, "
        f"got {total}"
    )


# ---------------------------------------------------------------------------
# P3 (REAL): risk monotonicity end-to-end through the adapter
# ---------------------------------------------------------------------------

def test_p3_risk_monotone_e2e():
    """Risk 0.0 -> 1.0 with everything else fixed:
    (a) gate strength monotone non-decreasing in risk;
    (b) risk=1.0 -> PROHIBITED (ratified tail threshold severity 9.0);
    (c) TailRisk severity monotone in risk;
    (d) engine v_safe ordering matches UDM combine() ordering.
    """
    risks = [0.0, 0.25, 0.5, 0.75, 0.9, 1.0]
    cands, gates, sevs = [], [], []
    for r in risks:
        c, m = adapt_option(f"opt-risk-{r}", dims(risk=r), wall_passed=True)
        gate, reasons, _ = adapter_gate(c, m, PROFILE, POLICY)
        cands.append(c)
        gates.append(gate)
        sevs.append(c.tails[0].severity if c.tails else 0.0)

    strengths = [GATE_STRENGTH[g] for g in gates]
    assert strengths == sorted(strengths), (
        f"P3 VIOLATION (a): gate strength not monotone in risk: "
        f"{list(zip(risks, gates))}"
    )
    assert gates[-1] == PROHIBITED, (
        f"P3 VIOLATION (b): risk=1.0 must gate PROHIBITED, got {gates[-1]} "
        f"(reasons: {reasons})"
    )
    assert sevs == sorted(sevs), (
        f"P3 VIOLATION (c): TailRisk severity not monotone: {sevs}"
    )

    base, _ = adapt_option(
        "baseline", dims(mv=0.1, risk=0.1), wall_passed=True, baseline=True
    )
    lo, _ = adapt_option("lo", dims(mv=0.4, risk=0.6), wall_passed=True)
    hi, _ = adapt_option("hi", dims(mv=0.9, risk=0.1), wall_passed=True)
    ev = evaluate_candidates([base, lo, hi], "baseline", PROFILE, POLICY)
    by_id = {r["candidate_id"]: r for r in ev["rows"]}
    udm_lo, _ = es.combine(dims(mv=0.4, risk=0.6))
    udm_hi, _ = es.combine(dims(mv=0.9, risk=0.1))
    engine_order = by_id["hi"]["v_safe"] > by_id["lo"]["v_safe"]
    udm_order = udm_hi > udm_lo
    assert engine_order == udm_order, (
        f"P3 VIOLATION (d): ordering not preserved — UDM hi>lo: {udm_order}, "
        f"engine v_safe hi>lo: {engine_order}"
    )


# ---------------------------------------------------------------------------
# P4 (REAL): dimension independence end-to-end through the adapter
# ---------------------------------------------------------------------------

def test_p4_dimension_independence_e2e():
    """Each mapped primitive depends ONLY on its own dimension:
    pv.B byte-identical across a cost sweep; TailRisk stable when only
    urgency moves; horizon stable when only evidence moves; all-UNKNOWN
    option -> NEEDS_EVIDENCE with ADAPTER_UNKNOWN_* reasons (P-003).
    """
    fixed_mv = dims(mv=0.8)
    b0 = map_mission_value(fixed_mv["mission_value"])
    adapted = []
    for cost in (0.0, 0.5, 1.0):
        dd = dims(mv=0.8, cost=cost)
        b = map_mission_value(dd["mission_value"])
        assert b == b0, (
            f"P4 VIOLATION: map_mission_value moved ({b0} -> {b}) when only "
            f"cost changed: dimensions entangled"
        )
        c, m = adapt_option(f"opt-cost-{cost}", dd, wall_passed=True)
        adapted.append(c)
    bs = [c.pv.B for c in adapted]
    assert all(b == bs[0] for b in bs), (
        f"P4 VIOLATION: Candidate.pv.B not byte-identical across cost sweep: "
        f"{bs}"
    )

    t0 = map_risk(dims(risk=0.6, urg=0.1)["risk"])
    t1 = map_risk(dims(risk=0.6, urg=0.9)["risk"])
    assert (t0.severity, t0.probability) == (t1.severity, t1.probability), (
        "P4 VIOLATION: TailRisk moved when only urgency changed"
    )

    h0 = map_urgency(dims(urg=0.8)["urgency"])
    h1 = map_urgency(dims(urg=0.8, ev=0.2)["urgency"])
    assert h0 == h1 == "immediate", (
        f"P4 VIOLATION: horizon moved with evidence: {h0} -> {h1}"
    )

    unk = {
        k: {"value": None, "evidence": [], "confidence": 0.0}
        for k in ("mission_value", "evidence", "risk", "cost", "urgency")
    }
    c, m = adapt_option("opt-unknown", unk, wall_passed=True)
    gate, reasons, _ = adapter_gate(c, m, PROFILE, POLICY)
    assert gate == NEEDS_EVIDENCE and all(
        r.startswith("ADAPTER_UNKNOWN_") for r in reasons
    ), (
        f"P4 VIOLATION: UNKNOWN option gated {gate} {reasons} — "
        f"fabrication risk: ignorance scored as a number"
    )


# ---------------------------------------------------------------------------
# P5: Byte-shape contract (the mapping keys off UDM dimension names)
# ---------------------------------------------------------------------------

def test_p5_byte_shape_contract():
    """UDM dimension names are the adapter's mapping keys — they must be
    stable. If they change, the mapping breaks silently."""
    expected_dims = {"mission_value", "evidence", "risk", "cost", "urgency"}
    actual_dims = set(es.WEIGHTS.keys())
    assert actual_dims == expected_dims, (
        f"P5 VIOLATION: UDM dimensions changed. "
        f"Expected {expected_dims}, got {actual_dims}"
    )
