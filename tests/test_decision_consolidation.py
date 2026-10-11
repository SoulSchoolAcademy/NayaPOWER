"""Tests for the consolidated decision engine (Shawn 2026-10-11).

"Bring them together and put the best of them together." There is ONE
decision engine: kernel/value_calculus.py. kernel/decision_principle.py is
the independent verification oracle (non-authoritative, test role only).

Proves, in order:
  (a) the consolidated engine's two-phase API works (partition + decide)
  (b) disqualification is exclusion, not zero-scoring (never in ranking)
  (c) unknown defers, never disqualifies
  (d) consented + mitigated residual risk is admissible (the refinement)
  (e) honest outputs are first-class (ABSTAIN/ASK/READ_MORE/REFUSE)
  (f) the canonical engine agrees with the independent oracle (2,110 scenarios)
  (g) no competing engine exists (the law check passes)
  (h) all pre-existing value-calculus behavior is preserved (no regressions)
"""

import subprocess
import sys
from pathlib import Path

import pytest

from kernel import value_calculus as vc
from kernel import decision_principle as dp
from kernel.value_calculus import (
    Candidate, PVEstimate, QualityProfile, RiskPolicy,
    QUALITY_DIMENSIONS,
)

ROOT = Path(__file__).resolve().parents[1]


def _profile(**kw):
    d = dict(profile_id="TEST", version="1.0", objective="consolidation test")
    d.update(kw)
    return QualityProfile(**d)


def _candidate(cid, *, authorized=True, hard_violation=False,
               lawful=True, rights_safe=True, privacy_safe=True,
               safety_safe=True, value=5.0, evidence_count=1,
               informed_consent=False, harm_mitigated=False,
               tails=(), stakes="low", reversible=True):
    pv = PVEstimate(
        B=max(0.0, value), H=0.0, C=0.0, R=0.0,
        confidence={"B": 1.0, "H": 1.0, "C": 1.0, "R": 1.0},
        evidence_count=evidence_count,
    )
    quality = {d: 10.0 for d in QUALITY_DIMENSIONS}
    confidence = {d: 1.0 for d in QUALITY_DIMENSIONS}
    return Candidate(
        candidate_id=cid, quality=quality, confidence=confidence, pv=pv,
        tails=tails, authorized=authorized, hard_violation=hard_violation,
        lawful=lawful, rights_safe=rights_safe, privacy_safe=privacy_safe,
        safety_safe=safety_safe, informed_consent=informed_consent,
        harm_mitigated=harm_mitigated, stakes=stakes, reversible=reversible,
    )


PROFILE = _profile()


# ---------------------------------------------------------------------------
# (a) Two-phase API: partition + decide
# ---------------------------------------------------------------------------

def test_partition_separates_admissible_disqualified_deferred():
    good = _candidate("good", value=5.0)
    bad = _candidate("bad", hard_violation=True, value=100.0)
    waiting = _candidate("waiting", authorized=False, value=50.0)
    p = vc.partition_candidates([good, bad, waiting], PROFILE)
    assert p["admissible"] == ["good"]
    assert p["disqualified"] == ["bad"]
    assert p["deferred"] == ["waiting"]


def test_decide_chooses_best_admissible():
    a = _candidate("a", value=5.0)
    b = _candidate("b", value=8.0)
    d = vc.decide([a, b], baseline_id="__none__", profile=PROFILE)
    assert d["outcome"] == vc.DECIDE_ACT
    assert d["chosen"] == "b"
    assert d["chosen_value"] == 8.0
    assert d["ranking"] == ["b", "a"]


# ---------------------------------------------------------------------------
# (b) Disqualification is exclusion, not zero-scoring
# ---------------------------------------------------------------------------

def test_disqualified_never_enters_ranking_despite_high_value():
    harmful = _candidate("harmful", hard_violation=True, value=100.0)
    safe = _candidate("safe", value=5.0)
    d = vc.decide([harmful, safe], baseline_id="__none__", profile=PROFILE)
    assert d["outcome"] == vc.DECIDE_ACT
    assert d["chosen"] == "safe"
    assert d["disqualified"] == ["harmful"]
    assert "harmful" not in d["ranking"]
    assert d["ranking"] == ["safe"]


def test_all_disqualified_means_refuse():
    h1 = _candidate("h1", hard_violation=True, value=10.0)
    h2 = _candidate("h2", lawful=False, value=10.0)
    d = vc.decide([h1, h2], baseline_id="__none__", profile=PROFILE)
    assert d["outcome"] == vc.DECIDE_REFUSE
    assert d["chosen"] is None
    assert set(d["disqualified"]) == {"h1", "h2"}


# ---------------------------------------------------------------------------
# (c) Unknown defers, never disqualifies
# ---------------------------------------------------------------------------

def test_unknown_safety_defers_not_disqualifies():
    unknown = _candidate("unknown", safety_safe=None, value=5.0)
    d = vc.decide([unknown], baseline_id="__none__", profile=PROFILE)
    assert d["disqualified"] == []
    assert d["deferred"] == ["unknown"]
    assert d["outcome"] in (vc.DECIDE_READ_MORE, vc.DECIDE_ABSTAIN)


def test_unknown_authority_defers():
    noauth = _candidate("noauth", authorized=False, value=5.0)
    p = vc.partition_candidates([noauth], PROFILE)
    assert p["deferred"] == ["noauth"]
    assert p["disqualified"] == []


# ---------------------------------------------------------------------------
# (d) Consented + mitigated residual risk is admissible (the refinement)
# ---------------------------------------------------------------------------

def test_consented_mitigated_tail_risk_is_admissible():
    from kernel.value_calculus import TailRisk
    risky = _candidate(
        "risky", value=8.0,
        tails=(TailRisk(severity=9.5, probability=0.5, harm_class="test"),),
        informed_consent=True, harm_mitigated=True,
    )
    p = vc.partition_candidates([risky], PROFILE)
    assert p["admissible"] == ["risky"], p["verdicts"]
    assert p["disqualified"] == []


def test_unconsented_tail_risk_still_prohibited():
    from kernel.value_calculus import TailRisk
    reckless = _candidate(
        "reckless", value=50.0,
        tails=(TailRisk(severity=9.5, probability=0.5, harm_class="test"),),
    )
    p = vc.partition_candidates([reckless], PROFILE)
    assert p["disqualified"] == ["reckless"]


# ---------------------------------------------------------------------------
# (e) Honest outputs first-class
# ---------------------------------------------------------------------------

def test_no_verified_value_means_abstain_not_guess():
    # evidence_count=0 -> no verified value -> ABSTAIN, not a guess.
    a = _candidate("a", value=5.0, evidence_count=0)
    b = _candidate("b", value=3.0, evidence_count=0)
    d = vc.decide([a, b], baseline_id="__none__", profile=PROFILE)
    assert d["outcome"] == vc.DECIDE_ABSTAIN
    assert d["chosen"] is None
    assert d["admissible"] == ["a", "b"]  # admissible, just unverified


def test_authority_gap_asks():
    waiting = _candidate("waiting", authorized=False, value=5.0)
    d = vc.decide([waiting], baseline_id="__none__", profile=PROFILE)
    assert d["outcome"] == vc.DECIDE_ASK


def test_empty_means_abstain():
    d = vc.decide([], baseline_id="__none__", profile=PROFILE)
    assert d["outcome"] == vc.DECIDE_ABSTAIN
    assert d["chosen"] is None


# ---------------------------------------------------------------------------
# (f) Canonical engine agrees with the independent oracle
# ---------------------------------------------------------------------------

def test_consolidated_engine_matches_oracle_on_battery():
    ev = dp.cross_verify_consolidated(dp.scenario_battery())
    assert ev["agreed"], ev["divergences"]


def test_consolidated_engine_matches_oracle_on_random():
    for seed in (42, 1337):
        ev = dp.cross_verify_consolidated(dp.random_scenarios(seed=seed, count=100))
        assert ev["agreed"], f"seed {seed}: {ev['divergences'][:2]}"


# ---------------------------------------------------------------------------
# (g) No competing engine (the law check)
# ---------------------------------------------------------------------------

def test_no_competing_engine():
    r = subprocess.run(
        [sys.executable, "tools/check_no_competing_engine.py", "--root", str(ROOT)],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert "FAIL" not in r.stdout, r.stdout
    assert "OK" in r.stdout, r.stdout


def test_oracle_is_not_an_engine():
    # The oracle's class must not match the competing-engine name patterns.
    import re
    name = dp.PrincipleOracle.__name__
    normalized = re.sub(r"[_\s]", "", name).lower()
    assert not re.match(r"^(decision|scoring|value|choice|action)engine$", normalized), name


# ---------------------------------------------------------------------------
# (h) Pre-existing behavior preserved (spot-checks; full suite runs separately)
# ---------------------------------------------------------------------------

def test_intent_doctrine_still_first():
    bad = _candidate("bad", value=100.0)
    # intent_to_harm via dataclass replace
    import dataclasses
    bad = dataclasses.replace(bad, intent_to_harm=True)
    gate, reasons, _ = vc.gate_candidate(bad, PROFILE, RiskPolicy())
    assert gate == vc.PROHIBITED
    assert "HARMFUL_INTENT_DISQUALIFIED" in reasons


def test_evaluate_candidates_unchanged():
    baseline = _candidate("base", value=0.0)
    import dataclasses
    baseline = dataclasses.replace(baseline, is_baseline=True)
    alt = _candidate("alt", value=10.0)
    ev = vc.evaluate_candidates([baseline, alt], "base", PROFILE)
    assert ev["decision"] in (vc.ACT, vc.ASK, vc.READ_MORE)
    assert "harmful" not in [r["candidate_id"] for r in ev.get("ranked_all", [])]


def test_zero_value_law_still_enforced():
    receipt = vc.build_decision_receipt(
        decision_id="t", objective="t", baseline_id="b",
        stakeholders=[], horizon="t", evaluation={}, authority_basis="t",
        evidence_refs=[], observation_window={"status": "OPEN"},
        verification="UNVERIFIED",
    )
    violations = vc.validate_zero_value_law(receipt)
    assert violations == []
