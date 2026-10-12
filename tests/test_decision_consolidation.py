"""Consolidation tests — STAGE 2 "no exception" (2026-10-11).

kernel/decision_principle.py (the competing DecisionEngine) was retired:
its unique safety checks were folded into the canonical value calculus
(kernel/value_calculus.py) and the duplicate module was deleted. This file
ports the retired engine's scenario battery into canonical space, proving
no legitimate protection was lost in the consolidation.

Ported protections:
  (a) a prohibited action with otherwise-high value is DISQUALIFIED
      (PROHIBITED), not outscored
  (b) uncertainty alone never disqualifies (NEEDS_EVIDENCE, never PROHIBITED)
  (c) "I don't know" is a valid, honest output (READ_MORE, never a guess)
  (d) disqualified actions never enter the ranking (exclusion proof)
  (e) established deception disqualifies regardless of value (tell-truth gate)
  (f) truthfulness unknown defers judgment (TRUTHFULNESS_UNKNOWN)
  (g) forbidden scope is disqualified on the merits — never rescued by an
      authority grant (distinct from merely missing authority)
  (h) assessed severe tail risk disqualifies (the severity x probability path)
  (i) all-prohibited -> REFUSE; deterministic tie-break; gate determinism
"""

import random

import pytest

from kernel.value_calculus import (
    ACT,
    ASK,
    READ_MORE,
    REFUSE,
    ADMISSIBLE,
    NEEDS_AUTHORITY,
    NEEDS_EVIDENCE,
    PROHIBITED,
    Candidate,
    PVEstimate,
    QualityProfile,
    RiskPolicy,
    TailRisk,
    evaluate_candidates,
    gate_candidate,
)


@pytest.fixture
def profile():
    return QualityProfile(
        profile_id="NAYAPOWER-DECISION",
        version="2.1",
        objective="maximum responsible verified value",
        min_evidence_count=2,
        relative_margin=0.10,
    )


def pv(B=8, H=0, C=1, R=0.2, conf=0.95, evidence_count=3):
    return PVEstimate(B, H, C, R, {k: conf for k in ("B", "H", "C", "R")}, evidence_count)


def quality(score=9.5, conf=0.95, **overrides):
    dims = {
        "objective_fit": score,
        "evidence_sufficiency": score,
        "applicability": score,
        "robustness": score,
        "reversibility": score,
        "blast_containment": score,
        "simplicity": score,
    }
    dims.update(overrides)
    return dims, {k: conf for k in dims}


def cand(cid, *, baseline=False, B=8, score=9.5, conf=0.95, **kwargs):
    q, c = quality(score, conf)
    hard = dict(lawful=True, rights_safe=True, privacy_safe=True, safety_safe=True)
    hard.update({k: kwargs.pop(k) for k in list(kwargs) if k in hard})
    auth = dict(authorized=True, human_authorized=False)
    auth.update({k: kwargs.pop(k) for k in list(kwargs) if k in auth})
    return Candidate(
        cid, q, c, pv(B=B, conf=conf), reversible=True,
        is_baseline=baseline, **hard, **auth, **kwargs
    )


def base_candidates():
    return cand("base", baseline=True, B=5)


# ---------------------------------------------------------------------------
# (a) Disqualification, not zero-scoring
# ---------------------------------------------------------------------------

def test_high_value_harmful_intent_disqualified_not_outscored(profile):
    harmful = cand("harmful", B=100, intent_to_harm=True)
    safe = cand("safe", B=5)
    gate, reasons, _ = gate_candidate(harmful, profile, RiskPolicy())
    assert gate == PROHIBITED
    assert reasons == ["HARMFUL_INTENT_DISQUALIFIED"]

    ev = evaluate_candidates([base_candidates(), harmful, safe], "base", profile)
    assert ev["selected"] != "harmful"
    ranked = [r["candidate_id"] for r in ev["rows"] if r["candidate_id"] != "base"]
    assert "harmful" not in [r["candidate_id"] for r in ev.get("ranked_all", [])]
    assert ranked  # the safe candidate still competes


def test_deceptive_action_disqualified_despite_value(profile):
    liar = cand("liar", B=99, deceptive=True)
    honest = cand("honest", B=9)
    gate, reasons, _ = gate_candidate(liar, profile, RiskPolicy())
    assert gate == PROHIBITED
    assert reasons == ["DECEPTIVE"]

    ev = evaluate_candidates([base_candidates(), liar, honest], "base", profile)
    assert ev["selected"] == "honest"
    assert ev["decision"] == ACT


def test_forbidden_scope_disqualified_even_when_authorized(profile):
    # The retired engine's key distinction: forbidden scope is disqualified on
    # the merits. An authority grant can never rescue it.
    rogue = cand("rogue", B=42, forbidden_scope=True, authorized=True,
                 human_authorized=True)
    gate, reasons, _ = gate_candidate(rogue, profile, RiskPolicy())
    assert gate == PROHIBITED
    assert reasons == ["FORBIDDEN_SCOPE"]


def test_missing_authority_defers_but_forbidden_scope_does_not(profile):
    waiting = cand("waiting", B=42, authorized=False)
    gate, reasons, _ = gate_candidate(waiting, profile, RiskPolicy())
    assert gate == NEEDS_AUTHORITY
    assert "AUTHORITY_MISSING" in reasons

    rogue = cand("rogue", B=42, forbidden_scope=True, authorized=False)
    gate, reasons, _ = gate_candidate(rogue, profile, RiskPolicy())
    assert gate == PROHIBITED
    assert reasons == ["FORBIDDEN_SCOPE"]


def test_assessed_severe_tail_risk_disqualifies(profile):
    # Shawn 2026-10-11 bar decision (KEEP THE STRICT BAR, t972): the
    # retired engine's assessed-harm bar (severity >= 7.0, probability > 0.05)
    # is a policy override in the canonical engine — NOT the configurable
    # RiskPolicy tail path. The F1 band Lane 8 found (t942) is excluded here.
    reckless = cand("reckless", B=50, tails=(TailRisk(9.0, 0.5, "severe"),))
    modest = cand("modest", B=9)
    gate, reasons, _ = gate_candidate(reckless, profile, RiskPolicy())
    assert gate == PROHIBITED
    assert any(r.startswith("ASSESSED_HARM_STRICT_BAR") for r in reasons)

    ev = evaluate_candidates([base_candidates(), reckless, modest], "base", profile)
    assert ev["selected"] == "modest"


def test_configurable_tail_path_still_fires_below_strict_bar(profile):
    # The RiskPolicy tail path is intact for harms below the strict bar:
    # severity 6.0 (< 7.0) with probability 0.5 trips a custom policy
    # (5.0/0.01) via TAIL_RISK, never ASSESSED_HARM_STRICT_BAR.
    risky = cand("risky", B=50, tails=(TailRisk(6.0, 0.5, "moderate"),))
    policy = RiskPolicy(severity_threshold=5.0, probability_threshold=0.01)
    gate, reasons, _ = gate_candidate(risky, profile, policy)
    assert gate == PROHIBITED
    assert any(r.startswith("TAIL_RISK") for r in reasons)
    assert not any(r.startswith("ASSESSED_HARM_STRICT_BAR") for r in reasons)


# ---------------------------------------------------------------------------
# (b) Uncertainty alone never disqualifies
# ---------------------------------------------------------------------------

def test_uncertainty_alone_never_prohibits(profile):
    q, c = quality()
    unknown = Candidate("unknown", q, c, pv(evidence_count=0), authorized=True)
    gate, reasons, _ = gate_candidate(unknown, profile, RiskPolicy())
    assert gate == NEEDS_EVIDENCE
    assert gate != PROHIBITED


def test_truthfulness_unknown_defers(profile):
    unsure = cand("unsure", deceptive=None)
    gate, reasons, _ = gate_candidate(unsure, profile, RiskPolicy())
    assert gate == NEEDS_EVIDENCE
    assert "TRUTHFULNESS_UNKNOWN" in reasons
    assert gate != PROHIBITED


def test_deceptive_default_false_preserves_existing_callers(profile):
    # Backward compatibility: callers that never tracked deception see no
    # behavior change from the consolidation.
    legacy = cand("legacy")
    gate, _, _ = gate_candidate(legacy, profile, RiskPolicy())
    assert gate == ADMISSIBLE


# ---------------------------------------------------------------------------
# (c) "I don't know" is a valid, honest output — never a guess
# ---------------------------------------------------------------------------

def test_admissible_but_no_value_is_not_act(profile):
    flat_a = cand("a", B=5)  # v_safe == 0: admissible, but no verified value
    flat_b = cand("b", B=5)
    ev = evaluate_candidates([base_candidates(), flat_a, flat_b], "base", profile)
    assert ev["decision"] == READ_MORE
    assert ev["selected"] is None


def test_all_prohibited_refuses(profile):
    h1 = cand("h1", B=10, intent_to_harm=True)
    h2 = cand("h2", B=10, deceptive=True)
    ev = evaluate_candidates([base_candidates(), h1, h2], "base", profile)
    assert ev["decision"] == REFUSE
    assert ev["selected"] is None


# ---------------------------------------------------------------------------
# (d) Disqualified actions never enter the ranking (exclusion proof)
# ---------------------------------------------------------------------------

def test_pipeline_excludes_prohibited_before_optimizing(profile):
    # Port of the retired module's verify_pipeline_excludes_first: the proof
    # now runs against the canonical engine it always verified.
    base = base_candidates()
    prohibited = cand("bad", B=100, intent_to_harm=True)
    deceiver = cand("sneaky", B=100, deceptive=True)
    rogue = cand("rogue", B=100, forbidden_scope=True)
    good = cand("good", B=9)
    candidates = [base, prohibited, deceiver, rogue, good]

    gates = {}
    for c in candidates:
        gate, reasons, _ = gate_candidate(c, profile, RiskPolicy())
        gates[c.candidate_id] = gate
    assert gates["bad"] == PROHIBITED
    assert gates["sneaky"] == PROHIBITED
    assert gates["rogue"] == PROHIBITED

    ev = evaluate_candidates(candidates, "base", profile)
    for row in ev["rows"]:
        assert row["candidate_id"] != "bad" or row["gate"] == PROHIBITED
    ranked_ids = [r["candidate_id"] for r in ev.get("ranked_all", [])]
    top_ids = [r["candidate_id"] for r in ev.get("top3", [])]
    for cid in ("bad", "sneaky", "rogue"):
        assert cid not in ranked_ids
        assert cid not in top_ids
    assert ev["selected"] not in ("bad", "sneaky", "rogue", None)
    assert ev["selected"] == "good"


# ---------------------------------------------------------------------------
# (i) Determinism — the honest analog of the retired cross_verify agreement
# ---------------------------------------------------------------------------

def test_deterministic_tie_break_by_candidate_id(profile):
    mk = lambda: [base_candidates(), cand("b-action", B=7), cand("a-action", B=7)]
    first = evaluate_candidates(mk(), "base", profile)["selected"]
    second = evaluate_candidates(mk(), "base", profile)["selected"]
    assert first == second == "a-action"


def test_gate_determinism_over_randomized_candidates(profile):
    rng = random.Random(20261011)
    for _ in range(50):
        q, c = quality()
        candidate = Candidate(
            f"c{rng.randint(0, 9999)}", q, c, pv(B=rng.uniform(0, 20)),
            authorized=rng.random() < 0.7,
            hard_violation=rng.random() < 0.1,
            intent_to_harm=rng.random() < 0.1,
            deceptive=rng.choice([True, False, None]),
            forbidden_scope=rng.random() < 0.1,
        )
        first = gate_candidate(candidate, profile, RiskPolicy())
        second = gate_candidate(candidate, profile, RiskPolicy())
        assert first[0] == second[0]
        assert first[1] == second[1]


def test_verdict_space_covers_retired_adapter_mapping(profile):
    # The retired module mapped canonical verdicts as:
    #   PROHIBITED -> DISQUALIFIED, NEEDS_AUTHORITY/NEEDS_EVIDENCE -> DEFERRED,
    #   ADMISSIBLE -> ADMISSIBLE.
    # The canonical verdicts themselves are the contract now; assert each is
    # reachable through the consolidated gates.
    assert gate_candidate(cand("x", intent_to_harm=True), profile, RiskPolicy())[0] == PROHIBITED
    assert gate_candidate(cand("x", deceptive=True), profile, RiskPolicy())[0] == PROHIBITED
    assert gate_candidate(cand("x", forbidden_scope=True), profile, RiskPolicy())[0] == PROHIBITED
    assert gate_candidate(cand("x", authorized=False), profile, RiskPolicy())[0] == NEEDS_AUTHORITY
    assert gate_candidate(cand("x", deceptive=None), profile, RiskPolicy())[0] == NEEDS_EVIDENCE
    assert gate_candidate(cand("x"), profile, RiskPolicy())[0] == ADMISSIBLE
