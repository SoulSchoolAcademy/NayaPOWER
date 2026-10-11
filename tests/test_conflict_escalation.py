"""T-08 conflict escalation: genuine trade-offs go to human governance.

Tests the consult, not just the verdict: every test below pins the exact
mechanism (elimination -> Pareto dominance -> escalation receipt). If you
can't break it, you didn't test it — the sabotage battery in
hidden_files/batt-t08/ proves the consult is the enforcement.
"""
import pytest

from kernel import act_pipeline as ap
from kernel.protocol import conflict_escalation as ce
from kernel.protocol import harm_profile as hp
from kernel.value_calculus import QualityProfile

NOW = 1_790_000_000.0
T0 = "2026-10-11T17:50:00+00:00"


def _g(gid, severity="negligible", reversibility="fully_reversible",
       timing="immediate", measurability="measured",
       distribution="single_person", note=""):
    return hp.GroupHarm(
        group_id=gid, severity=severity, reversibility=reversibility,
        timing=timing, measurability=measurability,
        distribution=distribution, note=note,
    )


def _p(*groups):
    return hp.HarmProfile(groups=tuple(groups), assessed_by="t08-test")


def _clean(*gids):
    return _p(*[_g(g) for g in gids])


def _consult(options, baseline, **kw):
    kw.setdefault("decided_at", T0)
    return ce.consult_conflicts(options, baseline_option=baseline, **kw)


# ---------------------------------------------------------------------------
# Elimination: rights / hard-harm violations never reach the Pareto round
# ---------------------------------------------------------------------------

def test_catastrophic_option_eliminated_never_on_front():
    a = _p(_g("x", severity="catastrophic", reversibility="irreversible",
             timing="immediate", measurability="measured",
             distribution="small_group"))
    r = _consult({"a": a, "b": _clean("x"), "base": _clean("x")}, "base")
    assert any(o == "a" for o, _ in r.receipt.eliminated)
    assert "a" not in r.receipt.pareto_front
    assert r.verdict == ce.PROCEED  # b/base clean, no conflict


def test_major_irreversible_option_eliminated():
    a = _p(_g("x", severity="major", reversibility="irreversible",
             timing="immediate", measurability="measured",
             distribution="small_group"))
    r = _consult({"a": a, "base": _clean("x")}, "base")
    assert any(o == "a" for o, _ in r.receipt.eliminated)
    assert "catastrophic" in r.receipt.eliminated[0][1] or "major" in r.receipt.eliminated[0][1]


def test_all_blocked_refuses_with_every_elimination_named():
    a = _p(_g("x", severity="catastrophic", reversibility="fully_reversible",
              timing="immediate", measurability="measured",
              distribution="single_person"))
    b = _p(_g("y", severity="major", reversibility="irreversible",
              timing="immediate", measurability="measured",
              distribution="small_group"))
    r = _consult({"a": a, "b": b}, "b")
    assert r.verdict == ce.REFUSE_ALL
    assert r.chosen_option is None
    eliminated_names = {o for o, _ in r.receipt.eliminated}
    assert eliminated_names == {"a", "b"}
    assert "refused" in r.receipt.render().lower()


def test_unknown_dimension_holds_option_never_proceeds():
    # Otherwise-best option with one unknown dimension: unknown is not safe.
    a = _p(hp.GroupHarm(group_id="x", severity="negligible",
                        reversibility="fully_reversible", timing="immediate",
                        measurability="unknown",  # <- unknown
                        distribution="single_person"))
    b = _p(_g("x", severity="minor", reversibility="fully_reversible",
              timing="immediate", measurability="measured",
              distribution="single_person"))
    r = _consult({"a": a, "b": b, "base": _clean("x")}, "base")
    assert "a" in r.receipt.evidence_pending
    assert "a" not in r.receipt.pareto_front
    # 'a' held; b admissible but baseline dominates b -> PROCEED base, never 'a'
    assert r.chosen_option != "a"


def test_all_unknown_refuses_as_needs_evidence():
    a = _p(hp.GroupHarm(group_id="x"))  # all unknown
    r = _consult({"a": a, "base": _clean("x")}, "base")
    # base clean -> admissible; a held. front=[base] -> PROCEED base.
    assert r.verdict == ce.PROCEED and r.chosen_option == "base"
    r2 = _consult({"a": _p(hp.GroupHarm(group_id="x")),
                   "b": _p(hp.GroupHarm(group_id="y"))}, "a")
    # 'a' is baseline but held for evidence; 'b' held too -> no admissible
    assert r2.verdict == ce.NEEDS_EVIDENCE


# ---------------------------------------------------------------------------
# Pareto: ordinal dominance only — no sums, no means, no invented rates
# ---------------------------------------------------------------------------

def test_single_dominant_option_proceeds():
    a = _clean("x", "y")
    b = _p(_g("x", severity="minor", reversibility="fully_reversible",
              timing="immediate", measurability="measured",
              distribution="small_group"),
            _g("y", severity="moderate", reversibility="conditionally_reversible",
               timing="near_term", measurability="estimated",
               distribution="small_group"))
    r = _consult({"a": a, "b": b, "base": _clean("x", "y")}, "base")
    # a dominates b; a harm-identical to base -> single digest on front
    assert r.verdict == ce.PROCEED
    assert r.chosen_option in ("a", "base")


def test_baseline_dominating_all_proceeds_with_baseline():
    a = _p(_g("x", severity="minor", reversibility="fully_reversible",
              timing="immediate", measurability="measured",
              distribution="single_person"))
    r = _consult({"a": a, "base": _clean("x")}, "base")
    assert r.verdict == ce.PROCEED
    assert r.chosen_option == "base"


def test_genuine_conflict_escalates_naming_cost_bearers():
    # The core case: A harms X, B harms Y. Neither dominates. The machine
    # must NOT pick — aggregate math would invent permission for the loser.
    a = _p(_g("x", severity="minor", reversibility="fully_reversible",
              timing="immediate", measurability="measured",
              distribution="small_group"),
            _g("y"))
    b = _p(_g("x"),
            _g("y", severity="minor", reversibility="fully_reversible",
               timing="immediate", measurability="measured",
               distribution="small_group"))
    base = _p(_g("x", severity="minor", reversibility="conditionally_reversible",
                 timing="delayed", measurability="estimated",
                 distribution="small_group"),
               _g("y", severity="minor", reversibility="conditionally_reversible",
                  timing="delayed", measurability="estimated",
                  distribution="small_group"))
    r = _consult({"a": a, "b": b, "base": base}, "base",
                 redesign_notes=("considered phased rollout; still shifts cost",))
    assert r.verdict == ce.ESCALATE_TO_HUMAN
    assert r.chosen_option is None
    bearers = dict(r.receipt.cost_bearers)
    assert any("x" in g for g in bearers["a"])
    assert any("y" in g for g in bearers["b"])
    assert r.receipt.human_decision_requested
    assert r.receipt.redesign_attempted is True
    text = r.receipt.render()
    assert text.startswith("IN A NUTSHELL")
    assert "human" in text.lower()


def test_aggregate_math_cannot_invent_permission():
    # Trap test: a naive "total harm" implementation would rank A (two
    # minors) worse than B (one moderate) or pick a "lesser evil". Ordinal
    # Pareto must see: A worse for Y, B worse for X -> incomparable ->
    # ESCALATE. Any PROCEED here is the defect.
    a = _p(_g("x", severity="minor", reversibility="fully_reversible",
              timing="immediate", measurability="measured",
              distribution="small_group"),
            _g("y", severity="minor", reversibility="fully_reversible",
               timing="immediate", measurability="measured",
               distribution="small_group"))
    b = _p(_g("x", severity="moderate", reversibility="fully_reversible",
              timing="immediate", measurability="measured",
              distribution="small_group"),
            _g("y"))
    base = _p(_g("x", severity="moderate",
                 reversibility="conditionally_reversible",
                 timing="delayed", measurability="estimated",
                 distribution="small_group"),
               _g("y", severity="minor",
                  reversibility="conditionally_reversible",
                  timing="delayed", measurability="estimated",
                  distribution="small_group"))
    r = _consult({"a": a, "b": b, "base": base}, "base")
    assert r.verdict == ce.ESCALATE_TO_HUMAN, (
        "incomparable harm trade-off must escalate, never be settled by math"
    )


def test_harm_identical_options_proceed_do_not_escalate():
    # Identical harm = no harm-conflict. Value differences are the
    # calculus's job, not this consult's.
    a = _clean("x")
    b = _clean("x")
    r = _consult({"a": a, "b": b, "base": _clean("x")}, "base")
    assert r.verdict == ce.PROCEED
    assert r.chosen_option in ("a", "b", "base")


def test_pareto_front_membership():
    a = _clean("x")
    b = _p(_g("x", severity="minor", reversibility="fully_reversible",
              timing="immediate", measurability="measured",
              distribution="single_person"))
    assert ce.pareto_front({"a": a, "b": b}) == ("a",)
    c = _p(_g("x"),
            _g("y", severity="minor", reversibility="fully_reversible",
               timing="immediate", measurability="measured",
               distribution="single_person"))
    # 'a' (clean on x, y unassessed -> assumed-negligible) dominates 'c'
    # (minor harm to y): not touching a group beats harming it, all else
    # equal. The assumption is recorded, not silent.
    assert ce.pareto_front({"a": a, "c": c}) == ("a",)
    d = _p(_g("x", severity="minor", reversibility="fully_reversible",
              timing="immediate", measurability="measured",
              distribution="single_person"),
           _g("y"))
    front = ce.pareto_front({"c": c, "d": d})
    assert set(front) == {"c", "d"}  # incomparable -> both on front


# ---------------------------------------------------------------------------
# Receipt: visible, deterministic, bound
# ---------------------------------------------------------------------------

def test_receipt_deterministic_and_bound():
    opts = {"a": _clean("x"), "base": _clean("x")}
    r1 = _consult(opts, "base")
    r2 = _consult(opts, "base")
    assert r1.receipt.receipt_id == r2.receipt.receipt_id
    assert len(r1.receipt.receipt_id) == 64
    digests = dict(r1.receipt.profile_digests)
    assert digests["a"] == hp.profile_digest(opts["a"])
    assert digests["base"] == hp.profile_digest(opts["base"])


def test_assumed_negligible_is_visible_never_silent():
    a = _p(_g("x"))            # assesses x only
    b = _p(_g("y"))            # assesses y only
    base = _p(_g("x"), _g("y"))
    r = _consult({"a": a, "b": b, "base": base}, "base")
    assumed = set(r.receipt.assumed_negligible)
    assert ("a", "y") in assumed
    assert ("b", "x") in assumed


def test_baseline_must_be_assessed_never_assumed():
    with pytest.raises(ValueError):
        ce.consult_conflicts({"a": _clean("x")}, baseline_option="missing")
    with pytest.raises(ValueError):
        ce.consult_conflicts({}, baseline_option="base")
    with pytest.raises(ValueError):
        ce.consult_conflicts({"a": "not-a-profile", "base": _clean("x")},
                             baseline_option="base")


def test_redesign_attestation_recorded():
    r = _consult({"a": _clean("x"), "base": _clean("x")}, "base")
    assert r.receipt.redesign_attempted is False
    assert "none attested" in r.receipt.render().lower()
    r2 = _consult({"a": _clean("x"), "base": _clean("x")}, "base",
                  redesign_notes=("tried narrower scope",))
    assert r2.receipt.redesign_attempted is True
    assert r2.receipt.redesign_notes == ("tried narrower scope",)


# ---------------------------------------------------------------------------
# Pipeline hook: the consult is USED by plan_action, not just present
# ---------------------------------------------------------------------------

def _pq_profile():
    return QualityProfile(profile_id="t08-test", version="1",
                          objective="minimum sufficient action")


def _authority(**kw):
    base = dict(action="naya_node_apply", scope="naya_node_apply",
                decided_at=NOW - 60, expires_at=None, grant_id="grant-1")
    base.update(kw)
    return ap.LawAuthority(**base)


def _candidate(cid="p1", harm_profile=None, **kw):
    base = dict(
        candidate_id=cid,
        action="naya_node_apply",
        description="apply retained intelligence",
        quality={"objective_fit": 9.0, "evidence_sufficiency": 9.0,
                 "applicability": 9.0, "robustness": 9.0,
                 "reversibility": 9.0, "blast_containment": 9.0,
                 "simplicity": 9.0},
        confidence={"objective_fit": 0.9, "evidence_sufficiency": 0.9,
                    "applicability": 0.9, "robustness": 0.9,
                    "reversibility": 0.9, "blast_containment": 0.9,
                    "simplicity": 0.9},
        reversibility="REVERSIBLE",
        expected_outcome="done",
        proof_requirements=("receipt",),
        stakes="low",
        lawful=True,
        rights_safe=True,
        privacy_safe=True,
        safety_safe=True,
        value_benefit=8.0, value_harm=1.0, value_cost=1.0, value_risk=0.5,
        value_confidence={"B": 0.9, "H": 0.9, "C": 0.9, "R": 0.9},
        value_evidence_count=3,
    )
    base.update(kw)
    if harm_profile is not None:
        base["harm_profile"] = harm_profile
    return ap.PlanCandidate(**base)


def _status_quo_baseline():
    # Doing nothing lets the existing problem persist (minor delayed harm to z).
    return _p(_g("z", severity="minor", reversibility="conditionally_reversible",
                 timing="delayed", measurability="estimated",
                 distribution="small_group", note="status quo harm"))


def test_pipeline_genuine_conflict_refuses_with_escalation_receipt():
    # A fixes z but harms x; B fixes z but harms y; doing nothing harms z.
    # No option dominates: the human must choose who bears the cost.
    prof_a = _p(_g("x", severity="minor", reversibility="fully_reversible",
                   timing="immediate", measurability="measured",
                   distribution="small_group"),
                 _g("z"))
    prof_b = _p(_g("y", severity="minor", reversibility="fully_reversible",
                   timing="immediate", measurability="measured",
                   distribution="small_group"),
                 _g("z"))
    plan, receipt = ap.plan_action(
        _authority(),
        [_candidate("pa", harm_profile=prof_a),
         _candidate("pb", harm_profile=prof_b)],
        _pq_profile(), now=NOW,
        baseline_harm_profile=_status_quo_baseline(),
    )
    assert plan is None
    assert receipt.phase == "PLAN_REFUSED"
    assert ap.PLAN_NEEDS_HUMAN_JUDGMENT in receipt.codes
    evidence = " ".join(receipt.evidence)
    assert "ESCALATE_TO_HUMAN" in evidence
    assert "pa" in evidence and "pb" in evidence


def test_pipeline_single_dominant_option_continues_to_selection():
    # A dominates B on harm and dominates the baseline: no conflict, the
    # value calculus still selects.
    prof_a = _p(_g("x"), _g("z"))
    prof_b = _p(_g("x", severity="minor", reversibility="fully_reversible",
                   timing="immediate", measurability="measured",
                   distribution="small_group"),
                 _g("z", severity="minor",
                    reversibility="conditionally_reversible",
                    timing="delayed", measurability="estimated",
                    distribution="small_group"))
    plan, receipt = ap.plan_action(
        _authority(),
        [_candidate("pa", harm_profile=prof_a, value_benefit=9.0),
         _candidate("pb", harm_profile=prof_b, value_benefit=7.0)],
        _pq_profile(), now=NOW,
        baseline_harm_profile=_status_quo_baseline(),
    )
    assert plan is not None, f"expected PLAN_ACCEPTED, got {receipt.codes}"
    assert receipt.phase == "PLAN_ACCEPTED"
    assert any("conflict consult PROCEED" in e for e in receipt.evidence)


def test_pipeline_hook_skipped_without_baseline():
    # No assessed baseline -> the hook fails closed (no consult), value
    # decides as before. Backward compatible.
    prof_a = _p(_g("x", severity="minor", reversibility="fully_reversible",
                   timing="immediate", measurability="measured",
                   distribution="small_group"))
    prof_b = _p(_g("y", severity="minor", reversibility="fully_reversible",
                   timing="immediate", measurability="measured",
                   distribution="small_group"))
    plan, receipt = ap.plan_action(
        _authority(),
        [_candidate("pa", harm_profile=prof_a, value_benefit=9.0),
         _candidate("pb", harm_profile=prof_b, value_benefit=7.0)],
        _pq_profile(), now=NOW,
    )
    assert plan is not None
    assert ap.PLAN_NEEDS_HUMAN_JUDGMENT not in receipt.codes


def test_pipeline_hook_skipped_with_single_profiled_candidate():
    prof_a = _p(_g("x", severity="minor", reversibility="fully_reversible",
                   timing="immediate", measurability="measured",
                   distribution="small_group"))
    plan, receipt = ap.plan_action(
        _authority(),
        [_candidate("pa", harm_profile=prof_a, value_benefit=9.0),
         _candidate("pb", value_benefit=7.0)],
        _pq_profile(), now=NOW,
        baseline_harm_profile=_status_quo_baseline(),
    )
    assert plan is not None
    assert ap.PLAN_NEEDS_HUMAN_JUDGMENT not in receipt.codes


def test_pipeline_catastrophic_profile_blocked_by_law11_threading():
    # The harm_profile threads candidate -> TypedAction -> law11_gate step 2b.
    prof = _p(_g("x", severity="catastrophic", reversibility="irreversible",
                 timing="immediate", measurability="measured",
                 distribution="small_group"))
    plan, receipt = ap.plan_action(
        _authority(), [_candidate("pa", harm_profile=prof)],
        _pq_profile(), now=NOW,
    )
    assert plan is None
    assert ap.PLAN_SAFETY_PROHIBITED in receipt.codes
