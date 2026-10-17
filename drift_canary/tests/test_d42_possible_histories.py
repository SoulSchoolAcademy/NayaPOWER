"""Tests for drift_canary/d42_possible_histories.py — D42.

RFD-AMB-001 (sharpest case): two sealed worlds, identical visible
observations (request sent, revocation committed, effect receipt missing).
World L: effect committed BEFORE revocation (legal). World V: effect
committed AFTER revocation against an established fence (violation).
The worker — blind to the answer key — must return AMBIGUOUS_BOTH_POSSIBLE
for both. Staged evidence narrows correctly in both directions; removing
it returns to ambiguity.
"""

import inspect

import pytest

from drift_canary.d42_possible_histories import (
    ABORTED,
    ABSENCE_PROVES_NOTHING_OUTSIDE_COVERAGE,
    ACK_PROVES_NO_EFFECT,
    AMBIGUOUS_BOTH_POSSIBLE,
    COMMITTED,
    INCONSISTENT_OBSERVATIONS_OR_MODEL,
    INSUFFICIENT_MODEL_OR_OBSERVABILITY,
    NOT_EXECUTED,
    SAFETY_ESTABLISHED_IN_SCOPE,
    TIMEOUT_PROVES_NOTHING,
    UNRESOLVED,
    VIOLATION_ESTABLISHED,
    InconsistentEvidenceError,
    InventedFactError,
    Observation,
    PossibleHistories,
    SafetyPolicy,
    Scenario,
    cold_successor_reproduces,
    diagnose,
    history_get,
    infer_absence_from_missing_receipt,
    infer_effect_from_ack,
    infer_from_timeout,
    make_history,
)


# ---------------------------------------------------------------------------
# RFD-AMB-001 fixture
# ---------------------------------------------------------------------------

def amb001_scenario() -> Scenario:
    def coherent(f: dict) -> bool:
        out, tim = f["effect_outcome"], f["effect_timing"]
        if out in (ABORTED, NOT_EXECUTED):
            return tim == "NEVER"
        if out == COMMITTED:
            return tim in ("BEFORE_REVOKE", "AFTER_REVOKE")
        return True  # UNRESOLVED: timing genuinely unknown

    def violates(f: dict) -> bool:
        # The fence: an effect committed at/after revocation is a violation.
        return (f["effect_outcome"] == COMMITTED
                and f["effect_timing"] == "AFTER_REVOKE")

    return Scenario(
        scenario_id="RFD-AMB-001",
        fact_domains=(
            ("request_outcome", (COMMITTED,)),
            ("revocation_outcome", (COMMITTED,)),
            ("effect_outcome",
             (COMMITTED, ABORTED, NOT_EXECUTED, UNRESOLVED)),
            ("effect_timing",
             ("BEFORE_REVOKE", "AFTER_REVOKE", "NEVER")),
        ),
        constraints=(coherent,),
        violates=violates,
    )


def amb001_base_observations() -> tuple:
    # Identical in BOTH sealed worlds: request sent, revocation committed,
    # effect receipt missing (receipt scope NOT covered-complete, so the
    # absence constrains nothing).
    return (
        Observation("o-req", "request_outcome", (COMMITTED,),
                    source="dispatch-log", trusted=True),
        Observation("o-rev", "revocation_outcome", (COMMITTED,),
                    source="governance-ledger", trusted=True),
    )


def worker_diagnose(observations: tuple) -> dict:
    """The worker. NOTE the signature: observations ONLY. There is no
    `truth` / `world` parameter — answer-key leakage is structurally
    impossible, not just discouraged."""
    return diagnose(PossibleHistories(scenario=amb001_scenario(),
                                      observations=observations))


# ---------------------------------------------------------------------------
# Twin worlds stay ambiguous
# ---------------------------------------------------------------------------

def test_twin_worlds_both_ambiguous():
    # World L truth: effect BEFORE revocation (legal).
    # World V truth: effect AFTER revocation (violation).
    # The worker sees neither truth — only the identical observations.
    d_l = worker_diagnose(amb001_base_observations())
    d_v = worker_diagnose(amb001_base_observations())
    assert d_l["verdict"] == AMBIGUOUS_BOTH_POSSIBLE
    assert d_v["verdict"] == AMBIGUOUS_BOTH_POSSIBLE
    assert d_l == d_v  # indistinguishable observations, identical diagnosis
    assert d_l["may_violate"] is True
    assert d_l["must_violate"] is False
    assert d_l["n_histories"] > 1


def test_worker_takes_no_truth_parameter():
    sig = inspect.signature(worker_diagnose)
    assert "truth" not in sig.parameters
    assert "world" not in sig.parameters


def test_ambiguity_names_missing_evidence():
    d = worker_diagnose(amb001_base_observations())
    missing = d["missing_discriminating_evidence"]
    assert "effect_outcome" in missing
    assert "effect_timing" in missing


# ---------------------------------------------------------------------------
# Staged evidence narrows correctly in both directions
# ---------------------------------------------------------------------------

def test_stage_2a_narrows_to_legal():
    ph = PossibleHistories(scenario=amb001_scenario(),
                           observations=amb001_base_observations())
    ph2 = ph.refine(Observation("o-receipt", "effect_timing",
                               ("BEFORE_REVOKE",),
                               source="effect-receipt-ts", trusted=True))
    assert ph2.verdict() == SAFETY_ESTABLISHED_IN_SCOPE
    assert ph2.may_violate() is False
    assert len(ph2) < len(ph)  # monotonic: H(O) shrank


def test_stage_2b_narrows_to_violation():
    ph = PossibleHistories(scenario=amb001_scenario(),
                           observations=amb001_base_observations())
    ph2 = ph.refine(Observation("o-fence", "effect_outcome",
                               (COMMITTED,),
                               source="fence-audit", trusted=True))
    ph3 = ph2.refine(Observation("o-fence-ts", "effect_timing",
                                ("AFTER_REVOKE",),
                                source="fence-audit", trusted=True))
    assert ph3.verdict() == VIOLATION_ESTABLISHED
    assert ph3.must_violate() is True


def test_removing_evidence_returns_to_ambiguity():
    ph = PossibleHistories(scenario=amb001_scenario(),
                           observations=amb001_base_observations())
    narrowed = ph.refine(Observation("o-receipt", "effect_timing",
                                    ("BEFORE_REVOKE",),
                                    source="effect-receipt-ts", trusted=True))
    assert narrowed.verdict() == SAFETY_ESTABLISHED_IN_SCOPE
    back = narrowed.recompute(amb001_base_observations())
    assert back.verdict() == AMBIGUOUS_BOTH_POSSIBLE


def test_refinement_never_grows_histories():
    ph = PossibleHistories(scenario=amb001_scenario(),
                           observations=amb001_base_observations())
    n0 = len(ph)
    ph2 = ph.refine(Observation("o-x", "effect_outcome",
                               (COMMITTED, UNRESOLVED),
                               source="partial-probe", trusted=True))
    assert len(ph2) <= n0


def test_contradictory_evidence_flagged_not_resolved():
    ph = PossibleHistories(scenario=amb001_scenario(),
                           observations=amb001_base_observations())
    ph2 = ph.refine(Observation("o-a", "effect_timing",
                               ("BEFORE_REVOKE",),
                               source="receipt-ts", trusted=True))
    with pytest.raises(InconsistentEvidenceError):
        ph2.refine(Observation("o-b", "effect_timing",
                              ("AFTER_REVOKE",),
                              source="other-ts", trusted=True))


def test_irreconcilable_observations_never_vacuous_pass():
    bad = amb001_base_observations() + (
        Observation("o-c1", "effect_outcome", (COMMITTED,),
                    source="a", trusted=True),
        Observation("o-c2", "effect_outcome", (ABORTED,),
                    source="b", trusted=True),
    )
    ph = PossibleHistories(scenario=amb001_scenario(), observations=bad)
    assert ph.verdict() == INCONSISTENT_OBSERVATIONS_OR_MODEL
    # Vacuous truth is refused: empty H(O) never yields "all safe".
    assert ph.must_violate() is False
    assert ph.all_safe() is False


# ---------------------------------------------------------------------------
# Forbidden inferences — never invent facts
# ---------------------------------------------------------------------------

def test_timeout_proves_nothing():
    with pytest.raises(InventedFactError) as e:
        infer_from_timeout()
    assert TIMEOUT_PROVES_NOTHING in str(e.value)


def test_timeout_proves_nothing_even_in_covered_scope():
    with pytest.raises(InventedFactError):
        infer_from_timeout(scope_covered_complete=True)


def test_ack_proves_no_effect():
    with pytest.raises(InventedFactError) as e:
        infer_effect_from_ack()
    assert ACK_PROVES_NO_EFFECT in str(e.value)


def test_missing_receipt_proves_nothing_outside_coverage():
    with pytest.raises(InventedFactError) as e:
        infer_absence_from_missing_receipt(scope_covered_complete=False)
    assert ABSENCE_PROVES_NOTHING_OUTSIDE_COVERAGE in str(e.value)


def test_missing_receipt_is_evidence_inside_covered_scope():
    assert infer_absence_from_missing_receipt(
        scope_covered_complete=True) is True


def test_untrusted_observation_rejected_at_admission():
    with pytest.raises(AssertionError):
        Observation("o-u", "effect_outcome", (COMMITTED,),
                    source="worker-label", trusted=False)


# ---------------------------------------------------------------------------
# Verdict vocabulary
# ---------------------------------------------------------------------------

def test_positive_control_fully_observed_legal():
    ph = PossibleHistories(
        scenario=amb001_scenario(),
        observations=amb001_base_observations() + (
            Observation("o-full", "effect_outcome", (COMMITTED,),
                        source="receipt", trusted=True),
            Observation("o-full-ts", "effect_timing", ("BEFORE_REVOKE",),
                        source="receipt-ts", trusted=True),
        ))
    assert ph.verdict() == SAFETY_ESTABLISHED_IN_SCOPE


def test_all_histories_violate():
    ph = PossibleHistories(
        scenario=amb001_scenario(),
        observations=amb001_base_observations() + (
            Observation("o-v", "effect_outcome", (COMMITTED,),
                        source="fence-audit", trusted=True),
            Observation("o-vt", "effect_timing", ("AFTER_REVOKE",),
                        source="fence-audit", trusted=True),
        ))
    assert ph.verdict() == VIOLATION_ESTABLISHED


def test_insufficient_when_model_incomplete():
    sc = Scenario(
        scenario_id="incomplete",
        fact_domains=(("x", (1, 2)),),
        violates=lambda f: False,
        model_complete=False)
    ph = PossibleHistories(scenario=sc, observations=())
    assert ph.verdict() == INSUFFICIENT_MODEL_OR_OBSERVABILITY


def test_insufficient_when_space_too_big():
    sc = Scenario(
        scenario_id="huge",
        fact_domains=tuple((f"f{i}", tuple(range(10))) for i in range(7)),
        violates=lambda f: False)
    ph = PossibleHistories(scenario=sc, observations=())
    # 10^7 > MAX_HISTORIES: refused to silently sample.
    assert ph.verdict() == INSUFFICIENT_MODEL_OR_OBSERVABILITY


# ---------------------------------------------------------------------------
# Safety policy while ambiguous
# ---------------------------------------------------------------------------

def test_policy_withholds_consequential_use_while_ambiguous():
    p = SafetyPolicy(AMBIGUOUS_BOTH_POSSIBLE)
    assert p.may_inspect() is True
    assert p.may_reconcile() is True
    assert p.may_certify_safety() is False
    assert p.may_promote_to_learn() is False
    assert p.may_blind_retry() is False


def test_policy_withholds_while_insufficient():
    p = SafetyPolicy(INSUFFICIENT_MODEL_OR_OBSERVABILITY)
    assert p.may_certify_safety() is False
    assert p.may_promote_to_learn() is False


def test_policy_permits_certify_only_when_established():
    assert SafetyPolicy(SAFETY_ESTABLISHED_IN_SCOPE).may_certify_safety() is True
    assert SafetyPolicy(VIOLATION_ESTABLISHED).may_certify_safety() is False
    # An established violation IS established knowledge — may be learned from.
    assert SafetyPolicy(VIOLATION_ESTABLISHED).may_promote_to_learn() is True


def test_handoff_preserves_both_worlds():
    ph = PossibleHistories(scenario=amb001_scenario(),
                           observations=amb001_base_observations())
    worlds = SafetyPolicy(AMBIGUOUS_BOTH_POSSIBLE).handoff_preserves_worlds(ph)
    assert len(worlds) == len(ph) > 1
    timings = {history_get(h, "effect_timing") for h in worlds}
    assert "BEFORE_REVOKE" in timings and "AFTER_REVOKE" in timings


def test_cold_successor_reproduces():
    ph = PossibleHistories(scenario=amb001_scenario(),
                           observations=amb001_base_observations())
    same, report = cold_successor_reproduces(ph)
    assert same, report
