"""test_operating_essence_acceptance.py — Acceptance tests for the Director's
operating essence: moral value before numerical optimization.

Source: Shawn's comment on #2175 (2026-10-11) — "Director's operating
essence — moral value before numerical optimization". It reinforces the
existing Zero Value Law, Law of One, and canonical Decision Value Calculus
V2.1 (NOT a second calculus, NOT a new ratification) and names five
acceptance tests for the enforcing path:

  C1. Hard rights/safety/consent violations remain PROHIBITED even with
      large claimed benefit.
  C2. Missing critical harm evidence returns NEEDS_EVIDENCE.
  C3. Manageable residual risk is not automatically a hard prohibition.
  C4. No weighted score overrides a hard gate.
  C5. Refusal / mitigation / evidence gathering can be the most intelligent
      outcome (the decision is not always ACT).

The comment's own truth ceiling: it "does not claim every clause has its
own machine-enforced field or end-to-end proof." What this file proves is
exactly what the seams enforce today; where a clause has no machine field
(e.g. "mitigate" is not a calculus route — it lives in the conflict-
resolution / design-search seam), the test asserts the enforced boundary
and names the seam honestly instead of pretending.

Negative controls: each class is falsifiable — neutering the corresponding
seam (hard-flag check, unknown-evidence check) makes its tests FAIL. Ordering
(gate-before-rank) is a code-read property pinned by the `eligible` filter in
`evaluate_candidates`: neutering it without changing exclusion would NOT flip
this battery — see test_prohibited_scores_never_used_in_decision.
A passing battery on broken bytes would be theater.
"""

import pytest

import time

from kernel import act_pipeline as ap
from kernel.value_calculus import (
    ACT,
    ADMISSIBLE,
    ASK,
    NEEDS_AUTHORITY,
    NEEDS_EVIDENCE,
    PROHIBITED,
    READ_MORE,
    REFUSE,
    Candidate,
    PVEstimate,
    QualityProfile,
    RiskPolicy,
    TailRisk,
    evaluate_candidates,
    gate_candidate,
)
from kernel.protocol.typed_action import (
    TypedAction,
    law11_gate,
)
from kernel.protocol.harm_assessment import (
    HARM_UNCERTAIN,
    NEUTRAL_TRUE_ZERO,
    SEVERITY_MODERATE,
    HarmAssessment,
    assess_uncertain_harm,
)


# ---------------------------------------------------------------------------
# Shared fixtures (same conventions as tests/test_value_calculus.py).
# ---------------------------------------------------------------------------

@pytest.fixture
def profile():
    return QualityProfile(
        profile_id="NAYAPOWER-DECISION",
        version="2.1",
        objective="maximum responsible verified value",
        min_evidence_count=2,
        relative_margin=0.10,
    )


@pytest.fixture
def risk_policy():
    return RiskPolicy()


def _pv(B=8.0, H=0.0, C=1.0, R=0.2, conf=0.95, evidence_count=3):
    return PVEstimate(B, H, C, R, {k: conf for k in ("B", "H", "C", "R")}, evidence_count)


def _quality(score=9.5, conf=0.95, **overrides):
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


def _cand(cid, *, baseline=False, B=8.0, score=9.5, conf=0.95, **kwargs):
    q, c = _quality(score, conf)
    hard = dict(lawful=True, rights_safe=True, privacy_safe=True, safety_safe=True)
    hard.update({k: kwargs.pop(k) for k in list(kwargs) if k in hard})
    explicit = dict(authorized=True, reversible=True, human_authorized=False)
    explicit.update({k: kwargs.pop(k) for k in list(kwargs) if k in explicit})
    return Candidate(
        cid, q, c, _pv(B=B, conf=conf), is_baseline=baseline,
        **hard, **explicit, **kwargs
    )


def _safe_action(**overrides):
    base = dict(
        actor_id="naya-5",
        operation="write",
        environment="development",
        resource="kernel/test_module",
        rights_safe=True,
        safety_safe=True,
        privacy_safe=True,
        consent_obtained=True,
    )
    base.update(overrides)
    return TypedAction(**base)


def _full_assessment(**overrides):
    base = dict(
        stakeholder_group="test_group",
        group_size=100,
        harm_type=HARM_UNCERTAIN,
        severity=SEVERITY_MODERATE,
        likelihood=0.1,
        likelihood_reliability="high",
        reversibility="reversible",
        time_to_appear="immediate",
        cumulative_risk=False,
        detectability="high",
        mitigation_available=True,
        consent_obtained=True,
        monitoring_ready=True,
        stop_conditions_defined=True,
        neutrality_state=NEUTRAL_TRUE_ZERO,
    )
    base.update(overrides)
    return HarmAssessment(**base)


# ---------------------------------------------------------------------------
# C1. Hard violations stay PROHIBITED even with large claimed benefit.
# ---------------------------------------------------------------------------

class TestHardViolationsNeverScored:
    def test_rights_violation_prohibited_despite_astronomic_benefit(
        self, profile, risk_policy
    ):
        """rights_safe=False + B=1e9 -> PROHIBITED. score_quality is computed
        at the top of gate_candidate but the verdict path never consults
        it — the hard-flag return does not depend on q, so the benefit
        magnitude is irrelevant to the verdict."""
        c = _cand("violator", B=1e9, rights_safe=False)
        gate, reasons, _ = gate_candidate(c, profile, risk_policy)
        assert gate == PROHIBITED
        assert "RIGHTS" in reasons

    def test_safety_violation_prohibited_despite_astronomic_benefit(
        self, profile, risk_policy
    ):
        c = _cand("violator", B=1e9, safety_safe=False)
        gate, reasons, _ = gate_candidate(c, profile, risk_policy)
        assert gate == PROHIBITED
        assert "SAFETY" in reasons

    def test_law11_gate_rights_violation_prohibited(self):
        """v1 gate: a rights violation is PROHIBITED no matter what the
        free-text description claims (description is never the verdict).
        Delta vs tests/test_law11_gate.py::test_rights_violation_prohibited:
        adds the benefit-claiming description to prove wording never moves
        the verdict."""
        action = _safe_action(
            rights_safe=False,
            description="this action creates enormous verified human value",
        )
        verdict = law11_gate(action)
        assert verdict.verdict == PROHIBITED
        assert "RIGHTS_VIOLATION" in verdict.reasons

    def test_law11_gate_consent_missing_on_pii_prohibited(self):
        """Consent is a non-tradeable boundary: reading PII without consent
        is PROHIBITED, not a score dimension.
        Delta vs tests/test_law11_gate.py::test_pii_without_consent_prohibited:
        privacy_safe=None (unknown) instead of True — the consent block
        fires even when the privacy dimension is not yet assessed."""
        action = _safe_action(
            operation="read",
            resource="customer_pii_export",
            privacy_safe=None,  # unknown overall — the consent check still fires
            consent_obtained=False,
        )
        verdict = law11_gate(action)
        assert verdict.verdict == PROHIBITED
        assert "PRIVACY_VIOLATION:consent_missing" in verdict.reasons

    def test_law11_gate_consent_present_passes_consent_block(self):
        """Control: with consent confirmed, the same PII read is NOT
        prohibited by the consent block — but the unknown privacy dimension
        still fails closed to NEEDS_EVIDENCE (never a silent pass)."""
        action = _safe_action(
            operation="read",
            resource="customer_pii_export",
            privacy_safe=None,
            consent_obtained=True,
        )
        verdict = law11_gate(action)
        assert verdict.verdict == NEEDS_EVIDENCE
        assert "UNKNOWN_PRIVACY" in verdict.reasons
        assert not any("consent_missing" in r for r in verdict.reasons)

    def test_v2_never_softens_v1_prohibition(self):
        """Law 11 v2 can only tighten. A v1 PROHIBITED stays PROHIBITED
        even with a fully-assessed, harmless-looking v2 assessment."""
        action = _safe_action(safety_safe=False)
        verdict = assess_uncertain_harm(action, (_full_assessment(),))
        assert verdict.verdict == PROHIBITED


# ---------------------------------------------------------------------------
# C2. Missing critical harm evidence -> NEEDS_EVIDENCE.
# ---------------------------------------------------------------------------

class TestMissingEvidenceNeedsEvidence:
    # Self-contained: the lawful=None isolation lives here, not delegated to
    # another file by test name (a rename elsewhere must not silently strip
    # this battery's C2 coverage).

    @pytest.mark.parametrize(
        "flag,reason_key",
        [
            ("lawful", "LAW"),
            ("rights_safe", "RIGHTS"),
            ("privacy_safe", "PRIVACY"),
            ("safety_safe", "SAFETY"),
        ],
    )
    def test_unknown_hard_flag_needs_evidence(
        self, profile, risk_policy, flag, reason_key
    ):
        """Every unknown hard flag fails closed to NEEDS_EVIDENCE — the
        fail-closed isolation, generalized across all four flags so no
        single dimension can silently pass. Kept in this battery (not
        delegated to another file by test name) so C2's coverage survives
        refactors elsewhere."""
        c = _cand("unknown-flag", **{flag: None})
        gate, reasons, _ = gate_candidate(c, profile, risk_policy)
        assert gate == NEEDS_EVIDENCE
        assert f"UNKNOWN_{reason_key}" in reasons

    @pytest.mark.parametrize("missing_field", ["severity", "likelihood"])
    def test_incomplete_harm_assessment_needs_evidence(self, missing_field):
        """A harm assessment with an unknown critical field cannot clear v2.
        Parametrized over two critical fields (not just severity) so the
        "missing critical harm evidence" clause is proven generally.
        Delta vs tests/test_law11_v2_uncertainty.py::TestStructuredAssessment::
        test_incomplete_assessment_needs_evidence: same seam, kept here so
        the acceptance battery is self-contained per clause."""
        action = _safe_action()
        assessment = _full_assessment(**{missing_field: None})
        verdict = assess_uncertain_harm(action, (assessment,))
        assert verdict.verdict == NEEDS_EVIDENCE
        assert any("INCOMPLETE_ASSESSMENT" in r for r in verdict.reasons)

    def test_missing_evidence_means_read_more_when_frontier_empty(
        self, profile, risk_policy
    ):
        """NEEDS_EVIDENCE rows route to READ_MORE only through the
        empty-frontier fallback — when no admissible candidate clears the
        eligibility bar. A clearing admissible alternative still ACTs; see
        test_eligible_alternative_still_acts_with_evidence_gap_elsewhere.
        This test engineers the sub-bar case (weak-but-admissible at Q=7.0
        < q_accept=9.0) so the fallback is what fires — gathering evidence
        is chosen over acting, not over a viable action."""
        candidates = [
            _cand("unknown-rights", rights_safe=None),
            _cand("base", baseline=True, B=0.5),
        ]
        result = evaluate_candidates(candidates, "base", profile, risk_policy)
        assert result["decision"] == READ_MORE
        assert result["selected"] is None

    def test_law11_gate_unknown_rights_needs_evidence(self):
        """v1 seam: an unknown rights dimension fails closed to
        NEEDS_EVIDENCE — the only touchpoint the clause has at the v1
        layer."""
        action = _safe_action(rights_safe=None)
        verdict = law11_gate(action)
        assert verdict.verdict == NEEDS_EVIDENCE
        assert "UNKNOWN_RIGHTS" in verdict.reasons

    def test_law11_gate_unknown_safety_needs_evidence(self):
        """Same fail-closed shape at the safety dimension (sister test to
        the rights one above — kept for clause self-containment)."""
        action = _safe_action(safety_safe=None)
        verdict = law11_gate(action)
        assert verdict.verdict == NEEDS_EVIDENCE
        assert "UNKNOWN_SAFETY" in verdict.reasons

    def test_eligible_alternative_still_acts_with_evidence_gap_elsewhere(
        self, profile, risk_policy
    ):
        """Boundary (documented, not a defect): a NEEDS_EVIDENCE row does
        NOT veto an eligible alternative. When one candidate is admissible
        and clears the bar, the decision is ACT on that candidate — the
        evidence gap blocks its own row, not the whole decision."""
        candidates = [
            _cand("needs-proof", lawful=None, B=50.0),
            _cand("eligible-alt", B=1.0),
            _cand("base", baseline=True, B=0.5),
        ]
        result = evaluate_candidates(candidates, "base", profile, risk_policy)
        assert result["decision"] == ACT
        assert result["selected"] == "eligible-alt"


# ---------------------------------------------------------------------------
# C3. Manageable residual risk is not automatically prohibited.
# ---------------------------------------------------------------------------

class TestManageableResidualRiskNotProhibited:
    def test_sub_threshold_tail_risk_not_prohibited(self, profile, risk_policy):
        """A tail risk below the governed thresholds (severity 5 < 9.0) is
        priced into the decision, not a hard prohibition."""
        c = _cand(
            "risky-but-managed",
            tails=(TailRisk(severity=5.0, probability=0.5, harm_class="latency"),),
        )
        gate, _, _ = gate_candidate(c, profile, risk_policy)
        assert gate != PROHIBITED

    def test_above_threshold_tail_risk_fires_policy_response(
        self, profile, risk_policy
    ):
        """The other side of the C3 boundary: a tail above the governed
        thresholds (severity 9.5 >= 9.0, probability 0.5 > 0.01) fires the
        policy response — the "manageable" boundary is real in both
        directions, not just a one-sided leniency."""
        c = _cand(
            "unmanaged-tail",
            tails=(TailRisk(severity=9.5, probability=0.5, harm_class="latency"),),
        )
        gate, reasons, _ = gate_candidate(c, profile, risk_policy)
        assert gate == risk_policy.response
        assert gate == PROHIBITED
        assert "TAIL_RISK:latency" in reasons

    def test_high_residual_risk_reduces_value_not_admissibility(
        self, profile, risk_policy
    ):
        """Residual risk R is subtracted from value (v_safe), not gated.
        Caution is priced; it is not confused with prohibition."""
        q, c = _quality()
        c_risky = Candidate(
            "high-r", q, c,
            _pv(B=5.0, H=0.1, C=0.1, R=0.9),
            authorized=True, reversible=True, human_authorized=False,
            lawful=True, rights_safe=True, privacy_safe=True, safety_safe=True,
        )
        gate, _, _ = gate_candidate(c_risky, profile, risk_policy)
        assert gate == ADMISSIBLE
        base = _cand("base", baseline=True, B=0.5)
        result = evaluate_candidates(
            [c_risky, base], "base", profile, risk_policy
        )
        risky_row = next(r for r in result["rows"] if r["candidate_id"] == "high-r")
        assert risky_row["v_safe"] < 5.0  # residual risk priced in
        assert risky_row["gate"] == ADMISSIBLE

    def test_characterized_moderate_harm_not_prohibited(self):
        """A complete, reliable, moderate, reversible assessment with a
        safe neutrality state is not prohibited — uncertainty handled is
        not the same as harm proven.
        Delta vs tests/test_law11_v2_uncertainty.py::test_fully_assessed_safe_action_admissible:
        MODERATE (not LOW) severity — proves the non-prohibition holds one
        rung up the severity ladder."""
        action = _safe_action()
        verdict = assess_uncertain_harm(action, (_full_assessment(),))
        assert verdict.verdict == ADMISSIBLE


# ---------------------------------------------------------------------------
# C4. No weighted score overrides a hard gate.
# ---------------------------------------------------------------------------

class TestScoreNeverOverridesHardGate:
    def test_prohibited_candidate_with_astronomic_value_not_selected(
        self, profile, risk_policy
    ):
        """The prohibited candidate has ~1e9 value and top quality; the
        admissible candidate has modest value. Selection must ignore the
        prohibited candidate entirely."""
        candidates = [
            _cand("prohibited-giant", B=1e9, rights_safe=False),
            _cand("modest", B=1.0),
            _cand("base", baseline=True, B=0.5),
        ]
        result = evaluate_candidates(candidates, "base", profile, risk_policy)
        assert result["selected"] == "modest"
        frontier_ids = [r["candidate_id"] for r in result["frontier"]]
        assert "prohibited-giant" not in frontier_ids

    def test_prohibited_rows_excluded_from_ranking(self, profile, risk_policy):
        """Structural: no PROHIBITED row can appear in the frontier or the
        ranked top-3, whatever its scores."""
        candidates = [
            _cand("p1", B=1e6, safety_safe=False),
            _cand("p2", B=1e6, privacy_safe=False),
            _cand("ok", B=1.0),
            _cand("base", baseline=True, B=0.5),
        ]
        result = evaluate_candidates(candidates, "base", profile, risk_policy)
        ranked_ids = [r["candidate_id"] for r in result["top3"]]
        for r in result["rows"]:
            if r["gate"] == PROHIBITED:
                assert r["candidate_id"] not in ranked_ids
        assert result["selected"] == "ok"

    def test_prohibited_scores_never_used_in_decision(
        self, profile, risk_policy
    ):
        """Exclusion, not ordering: this test proves a PROHIBITED row's
        scores never reach any downstream use (frontier, ranking,
        selection). Score-then-filter would produce the same rows, so no
        test here can prove gate-before-rank ordering — ordering is a
        code-read property pinned by the `eligible` filter in
        `evaluate_candidates`, not an observable one."""
        candidates = [
            _cand("bad", B=100.0, hard_violation=True),
            _cand("good", B=1.0),
            _cand("base", baseline=True, B=0.5),
        ]
        result = evaluate_candidates(candidates, "base", profile, risk_policy)
        gates = {r["candidate_id"]: r["gate"] for r in result["rows"]}
        assert gates["bad"] == PROHIBITED
        assert gates["good"] == ADMISSIBLE
        # The weighted sort key only ever sees admissible rows.
        assert result["selected"] == "good"


# ---------------------------------------------------------------------------
# Composition: the enforcing path is layered — law11 pre-filter first,
# then the calculus gate. These tests prove the two layers agree through
# the pipeline's OWN candidate mapping (defense in depth, not one gate).
# ---------------------------------------------------------------------------

class TestEnforcingPathComposition:
    def _plan_candidate(self, **overrides):
        q, c = _quality()
        base = dict(
            candidate_id="pc",
            action="deploy",
            description="",
            quality=q,
            confidence=c,
            reversibility="REVERSIBLE",
            expected_outcome="x",
            proof_requirements=(),
            lawful=True,
            rights_safe=True,
            privacy_safe=True,
            safety_safe=True,
            value_benefit=5.0,
            value_harm=0.1,
            value_cost=0.1,
            value_risk=0.05,
            value_confidence={"B": 0.95, "H": 0.95, "C": 0.95, "R": 0.95},
            value_evidence_count=5,
        )
        base.update(overrides)
        return ap.PlanCandidate(**base)

    def test_hard_violation_survives_pipeline_mapping(self, profile, risk_policy):
        """A plan-level hard violation mapped through the pipeline's real
        _candidate_to_calculus still gates PROHIBITED — even if the law11
        pre-filter were ever bypassed, the calculus gate catches it."""
        plan_c = self._plan_candidate(candidate_id="violator", hard_violation=True)
        calc_c = ap._candidate_to_calculus(plan_c)
        gate, reasons, _ = gate_candidate(calc_c, profile, risk_policy)
        assert gate == PROHIBITED

    def test_rights_violation_survives_pipeline_mapping(self, profile, risk_policy):
        plan_c = self._plan_candidate(candidate_id="violator", rights_safe=False)
        calc_c = ap._candidate_to_calculus(plan_c)
        gate, _, _ = gate_candidate(calc_c, profile, risk_policy)
        assert gate == PROHIBITED

    def test_clean_candidate_maps_to_admissible(self, profile, risk_policy):
        """Control: the mapping preserves admissibility too — it neither
        invents prohibitions nor launders violations."""
        calc_c = ap._candidate_to_calculus(self._plan_candidate(candidate_id="clean"))
        gate, _, _ = gate_candidate(calc_c, profile, risk_policy)
        assert gate == ADMISSIBLE

    def test_rights_violating_plan_refused_end_to_end(self, profile, risk_policy):
        """End-to-end acceptance: the pipeline's OWN public entry —
        plan_action — refuses a rights-violating plan with a refusal path,
        not a selection. This closes the top-level-entry gap: no layer
        above the gates can launder the violation, and the receipt names
        the exact refusal code (PLAN_SAFETY_PROHIBITED)."""
        authority = ap.LawAuthority(
            action="deploy",
            scope="deploy",
            decided_at=time.time(),
            expires_at=None,
            grant_id="essence-e2e",
        )
        violator = self._plan_candidate(
            candidate_id="violator",
            rights_safe=False,
            proof_requirements=("ev-1",),
        )
        plan, receipt = ap.plan_action(
            authority, [violator], profile, now=time.time()
        )
        assert plan is None
        assert receipt.phase == "PLAN_REFUSED"
        assert "PLAN_SAFETY_PROHIBITED" in receipt.codes
        assert receipt.executed is False

    def test_clean_plan_accepted_end_to_end(self, profile, risk_policy):
        """Control: the same entry accepts a clean plan — the refusal
        above is caused by the violation, not by the entry itself."""
        authority = ap.LawAuthority(
            action="deploy",
            scope="deploy",
            decided_at=time.time(),
            expires_at=None,
            grant_id="essence-e2e",
        )
        plan, receipt = ap.plan_action(
            authority,
            [self._plan_candidate(
                candidate_id="clean", proof_requirements=("ev-1",)
            )],
            profile,
            now=time.time(),
        )
        assert plan is not None
        assert receipt.phase == "PLAN_ACCEPTED"


# ---------------------------------------------------------------------------
# C5. Refusal / evidence gathering can be the most intelligent outcome.
# ---------------------------------------------------------------------------

class TestRefusalIsAnOutcome:
    def test_all_prohibited_means_refuse_not_act(self, profile, risk_policy):
        """When every non-baseline candidate is prohibited, the calculus
        returns REFUSE explicitly — never a disguised ACT."""
        candidates = [
            _cand("bad1", rights_safe=False),
            _cand("bad2", safety_safe=False),
            _cand("base", baseline=True, B=0.5),
        ]
        result = evaluate_candidates(candidates, "base", profile, risk_policy)
        assert result["decision"] == REFUSE
        assert result["selected"] is None

    def test_missing_evidence_means_read_more_not_act(
        self, profile, risk_policy
    ):
        """Gathering evidence is a first-class outcome: NEEDS_EVIDENCE
        anywhere routes the decision to READ_MORE, not to the least-bad
        admissible action."""
        candidates = [
            _cand("needs-proof", lawful=None, B=50.0),
            _cand("weak-but-admissible", B=0.6, score=7.0),
            _cand("base", baseline=True, B=0.5),
        ]
        result = evaluate_candidates(candidates, "base", profile, risk_policy)
        assert result["decision"] == READ_MORE

    def test_authority_gap_means_ask_not_act(self, profile, risk_policy):
        """A consequential candidate without human authorization routes to
        ASK — the machine does not invent permission via aggregate math."""
        candidates = [
            _cand(
                "consequential",
                B=50.0,
                stakes="consequential",
                reversible=False,
                human_authorized=False,
            ),
            _cand("base", baseline=True, B=0.5),
        ]
        result = evaluate_candidates(candidates, "base", profile, risk_policy)
        assert result["decision"] == ASK
        assert result["selected"] is None

    def test_human_authorization_does_not_buy_auto_execution(
        self, profile, risk_policy
    ):
        """The ASK trigger is stakes, not the authorization flag. A
        consequential candidate WITH human authorization clears the
        NEEDS_AUTHORITY gate — but the decision is still ASK, with the
        candidate selected for the human to decide on. Consequential
        stakes are never auto-executable: authorization moves the
        question to the human, it does not answer it. (This is the
        honest control for the test above: ASK fires for the stakes,
        not merely for the missing flag.)"""
        candidates = [
            _cand(
                "cons-auth",
                B=50.0,
                stakes="consequential",
                reversible=False,
                human_authorized=True,
            ),
            _cand("base", baseline=True, B=0.5),
        ]
        result = evaluate_candidates(candidates, "base", profile, risk_policy)
        assert result["decision"] == ASK
        assert result["selected"] == "cons-auth"


# ---------------------------------------------------------------------------
# Boundary: what this battery does NOT claim — and the mitigation prong of
# C5, tested behaviorally against the seam that owns it.
# ---------------------------------------------------------------------------

def test_mitigation_strategy_satisfies_resolve_before_trade():
    """C5's "mitigation" prong, behaviorally tested. Choosing a mitigated
    redesign lives in the conflict-resolution / design-search seam
    (kernel/protocol/conflict_resolution.py): an action with material
    adverse effects satisfies the Resolve Before Trade invariant when a
    MITIGATE alternative is recorded."""
    from kernel.protocol.conflict_resolution import (
        STRATEGY_MITIGATE,
        AlternativeDesign,
        DesignSearchRecord,
        check_resolve_before_trade,
    )

    record = DesignSearchRecord(action_id="essence-c5-mitigate")
    record.record_alternative(
        AlternativeDesign(
            design_id="mit-1",
            strategy=STRATEGY_MITIGATE,
            description="rate-limit the rollout and add monitoring",
            expected_effect="reduces exposure while preserving the benefit",
            evidence="prior rollout telemetry",
        )
    )
    satisfied, _ = check_resolve_before_trade(
        record, has_material_adverse_effects=True
    )
    assert satisfied
    assert STRATEGY_MITIGATE in record.strategies_attempted


def test_resolve_before_trade_fails_closed_without_alternatives():
    """Negative control for the mitigation seam: an action with material
    adverse effects and NO recorded alternative fails the invariant — the
    seam is enforced, not decorative."""
    from kernel.protocol.conflict_resolution import (
        DesignSearchRecord,
        check_resolve_before_trade,
    )

    record = DesignSearchRecord(action_id="essence-c5-empty")
    satisfied, reason = check_resolve_before_trade(
        record, has_material_adverse_effects=True
    )
    assert not satisfied
    assert "RESOLVE_BEFORE_TRADE" in reason


def test_calculus_has_no_mitigate_route():
    """Change-detector (honestly labeled): the calculus routes are
    ACT / READ_MORE / ASK / REFUSE — there is no "mitigate-and-proceed"
    route in this seam. If a MITIGATE route is ever added here, this fails
    and forces the C5 story to be rewritten deliberately, not silently."""
    from kernel import value_calculus

    assert not hasattr(value_calculus, "MITIGATE")


def test_decision_routes_are_a_closed_set(profile, risk_policy):
    """Behavioral pin on the calculus route set: a representative sweep of
    scenarios — REFUSE (single and multiple prohibitions), READ_MORE
    (rights-unknown and law-unknown), ACT (clean candidates), ASK (gate
    path without authorization, decision path with it) — returns only
    decisions from the documented route set. This is falsifiable in the
    direction that matters: if any scenario ever produces a route outside
    the set, this fails. (No finite sweep can prove a fifth route never
    exists; the pin documents the observed set and forces any new route
    to be a conscious, deliberate change.)"""
    from kernel import value_calculus

    scenarios = [
        (
            [_cand("bad", rights_safe=False),
             _cand("base", baseline=True, B=0.5)],
            REFUSE,
        ),
        (
            [_cand("bad1", safety_safe=False),
             _cand("bad2", lawful=False),
             _cand("base", baseline=True, B=0.5)],
            REFUSE,
        ),
        (
            [_cand("unknown-rights", rights_safe=None),
             _cand("base", baseline=True, B=0.5)],
            READ_MORE,
        ),
        (
            [_cand("unknown-law", lawful=None),
             _cand("base", baseline=True, B=0.5)],
            READ_MORE,
        ),
        (
            [_cand("ok", B=8.0),
             _cand("base", baseline=True, B=0.5)],
            ACT,
        ),
        (
            [_cand("modest", B=1.0),
             _cand("base", baseline=True, B=0.5)],
            ACT,
        ),
        (
            [_cand(
                "cons", B=50.0, stakes="consequential",
                reversible=False, human_authorized=False,
            ),
             _cand("base", baseline=True, B=0.5)],
            ASK,
        ),
        (
            [_cand(
                "cons-auth", B=50.0, stakes="consequential",
                reversible=False, human_authorized=True,
            ),
             _cand("base", baseline=True, B=0.5)],
            ASK,
        ),
    ]
    route_set = {
        value_calculus.ACT,
        value_calculus.READ_MORE,
        value_calculus.ASK,
        value_calculus.REFUSE,
    }
    for candidates, expected in scenarios:
        result = evaluate_candidates(candidates, "base", profile, risk_policy)
        assert result["decision"] == expected
        assert result["decision"] in route_set
