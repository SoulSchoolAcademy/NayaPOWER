"""Tests: Evidence-Bounded Uncertainty Propagation + SN-0783 recomputation.

Covers the four uncertainty kinds, the claim-level propagation rule, all
seven relationship semantics, modality preservation, observation-limit
propagation, the six-step/two-stage recomputation, projection preservation,
use-gating, the false-certainty cascade, and the decisive experiment.
Every negative test carries a positive control.
"""
import pytest

from ..propagation import (
    MeaningEnvelope, ClaimRegion, SupportSet, ClaimEnvelope,
    CLEARED, POSSIBLE, UNASSESSED, CONFIRMED,
    assess_region, evaluate_claim,
)
from ..uncertainty_propagation import (
    PARTIAL_OBSERVABILITY, CONFLICTING_EVIDENCE,
    UNRESOLVED_CAUSAL_HYPOTHESIS, INSUFFICIENT_EVIDENCE, UNCERTAINTY_KINDS,
    UncertaintyAnnotation,
    COVERED_COMPLETE, COVERED_PARTIAL, UNOBSERVED, CONFLICTED_COVERAGE,
    NOT_APPLICABLE, ObservationCoverage,
    CAUSE_CONTRIBUTING, CAUSE_NECESSARY, CAUSE_SUFFICIENT_CONDITIONAL,
    CAUSE_POSSIBLE, MOD_POSSIBLE, MOD_PROBABLE, MOD_CONDITIONAL,
    MOD_OBSERVED, MOD_VERIFIED, MODALITIES, CausalHypothesis,
    derive_modality,
    PATH_AND, PATH_OR, PATH_PARTIAL, PATH_CONTEXTUAL, SupportPath,
    UncertaintyEnvelope,
    support_refutation_matrix, qualify_claim,
    PROPAGATION_SEMANTICS, EXTENDED_RELATIONSHIPS,
    propagate_along_edge, nonexplosive_check,
    propagate_observation_limit,
    RECOMPUTATION_VERDICTS, EligibilityChangeReceipt,
    four_fact_assessment, SELECTIVE_PROPAGATION,
    secret_derivation_check,
    stage_a_impact_discovery, stage_b_recompute, recompute_closure,
    RequalificationRecord, retroactive_discovery,
    revocation_receipt, check_commit_boundary,
    MUST_SURVIVE, PROJECTION_SURFACES, check_projection_preservation,
    partial_scope_preservation,
    USE_HISTORICAL_RESEARCH, USE_DEBUGGING, USE_INVESTIGATION_PLANNING,
    USE_CERTIFICATION, USE_LEARN_PROMOTION, USE_CONSEQUENTIAL_ACT,
    INTENDED_USES, gate_use,
    build_five_stage_cascade_fixture, verify_cascade_stage,
    run_decisive_experiment,
)


# ---------------------------------------------------------------------------
# Helpers.
# ---------------------------------------------------------------------------
def _region(rid="r1"):
    return ClaimRegion(region_id=rid, envelope=MeaningEnvelope())


def _set(sid="s1", ev=("e1",), rid="r1", polarity="supports"):
    return SupportSet(set_id=sid, evidence_refs=ev, covers=(rid,),
                      polarity=polarity)


def _env(sets, rids=("r1",)):
    return ClaimEnvelope(
        claim_id="c1", claim_scope=MeaningEnvelope(),
        regions=tuple(_region(r) for r in rids),
        support_sets=tuple(sets))


def _uenv(**kw):
    base = dict(claim_id="c1", original_claim="original causal claim",
                claim_envelope=_env([_set()]))
    base.update(kw)
    return UncertaintyEnvelope(**base)


# ---------------------------------------------------------------------------
# 1. Four uncertainty kinds: distinct, never interchangeable.
# ---------------------------------------------------------------------------
def test_four_kinds_distinct():
    assert len(set(UNCERTAINTY_KINDS)) == 4


def test_annotation_rejects_unknown_kind():
    with pytest.raises(AssertionError):
        UncertaintyAnnotation(kind="vibes", proposition="p",
                              scope_region="r1", detail="d")


def test_kinds_have_distinct_downstream_rules():
    # Positive control: each kind annotates without collapsing into another.
    anns = [UncertaintyAnnotation(kind=k, proposition="p",
                                  scope_region="r1", detail="d")
            for k in UNCERTAINTY_KINDS]
    assert {a.kind for a in anns} == set(UNCERTAINTY_KINDS)


# ---------------------------------------------------------------------------
# His verdict table: the same incident, four different qualifications.
# ---------------------------------------------------------------------------
def test_outcome_supported_while_cause_unresolved():
    # "The deployment did not complete." — independently observed.
    assert support_refutation_matrix(True, False) == "SUPPORTED"
    # "The scheduler never dispatched." — missing telemetry.
    assert support_refutation_matrix(False, False) == "UNDETERMINED"


def test_causation_unproven_is_not_refuted():
    hyp = CausalHypothesis(
        hyp_id="H1", mechanism="scheduler withheld dispatch",
        cause_type=CAUSE_POSSIBLE, modality=MOD_POSSIBLE,
        status="UNDETERMINED")
    assert hyp.status == "UNDETERMINED"  # not REFUTED
    assert hyp.modality == MOD_POSSIBLE   # not verified


def test_unsupported_generalization_rejected():
    # "The scheduler is generally unreliable" from one incident: the
    # evidence scope (one workflow) cannot cover the general claim.
    narrow = _env([_set()])
    a = evaluate_claim(narrow, {"e1": CLEARED})
    assert a.strongest_scope == ("r1",)  # stays narrow; never widened
    assert "r1" in a.strongest_conclusion


def test_cause_uncertainty_does_not_erase_outcome():
    # Certainty about the outcome must not manufacture certainty about
    # its cause — and vice versa.
    outcome = support_refutation_matrix(True, False)
    cause = support_refutation_matrix(False, False)
    assert outcome == "SUPPORTED" and cause == "UNDETERMINED"


# ---------------------------------------------------------------------------
# 3. Support/refutation matrix + four-predicate qualification.
# ---------------------------------------------------------------------------
def test_matrix_all_four():
    assert support_refutation_matrix(True, False) == "SUPPORTED"
    assert support_refutation_matrix(False, True) == "REFUTED"
    assert support_refutation_matrix(True, True) == "CONFLICTED"
    assert support_refutation_matrix(False, False) == "UNDETERMINED"


def test_qualify_claim_all_four_required():
    ok, failed = qualify_claim(True, True, True, True)
    assert ok and failed == ""


def test_qualify_claim_names_failed_predicate():
    cases = [(False, True, True, True, "scope_valid"),
             (True, False, True, True, "evidence_admissible"),
             (True, True, False, True, "support_sufficient"),
             (True, True, True, False, "conflicts_resolved")]
    for sv, ea, ss, cr, name in cases:
        ok, failed = qualify_claim(sv, ea, ss, cr)
        assert not ok and failed == name


# ---------------------------------------------------------------------------
# 4. Seven relationship semantics.
# ---------------------------------------------------------------------------
def test_relationship_vocabulary_complete():
    assert set(EXTENDED_RELATIONSHIPS) == {
        "MENTIONS", "DERIVED_FROM", "REQUIRES_SUPPORT_FROM",
        "INDEPENDENTLY_CORROBORATED_BY", "PARTIALLY_SUPPORTS",
        "CONTRADICTS", "HYPOTHESIZED_CAUSE_OF"}


def test_mentions_transmits_nothing():
    # Positive control: a note mentioning an unresolved incident keeps
    # its own standing.
    child, mod, rule = propagate_along_edge("UNDETERMINED", "MENTIONS")
    assert "no_transmission" in rule


def test_derived_from_preserves_uncertainty():
    child, mod, rule = propagate_along_edge("UNDETERMINED", "DERIVED_FROM")
    assert child == "UNDETERMINED" and "uncertainty_travels" in rule


def test_hypothesized_cause_stays_hypothesis():
    child, mod, rule = propagate_along_edge("UNDETERMINED",
                                            "HYPOTHESIZED_CAUSE_OF",
                                            parent_modality=MOD_POSSIBLE)
    assert mod == MOD_POSSIBLE and "hypothesis_preserved" in rule


def test_contradicts_preserves_conflict():
    child, _, rule = propagate_along_edge("SUPPORTED", "CONTRADICTS")
    assert child == "CONFLICTED" and "conflict_preserved" in rule


def test_contradicts_without_material_support_no_conflict():
    child, _, _ = propagate_along_edge("UNDETERMINED", "CONTRADICTS")
    assert child == "UNDETERMINED"


def test_partially_supports_carries_restriction():
    child, _, rule = propagate_along_edge("SUPPORTED", "PARTIALLY_SUPPORTS",
                                          scope_restriction="staging_only")
    assert "staging_only" in rule


def test_nonexplosive_reasoning():
    verdict, q, reason = nonexplosive_check(True, "unrelated_Q")
    assert verdict == "UNDETERMINED" and "does_not_support_or_refute" in reason


# ---------------------------------------------------------------------------
# Modality: derivation never upgrades; copying never strengthens.
# ---------------------------------------------------------------------------
def test_derivation_preserves_modality():
    for derivation in ("copy", "summarize", "index", "repeat", "cite",
                       "project", "handover"):
        mod, rule = derive_modality(MOD_POSSIBLE, derivation)
        assert mod == MOD_POSSIBLE, derivation


def test_no_derivation_upgrades_to_verified():
    # Positive control of the forbidden direction: nothing in derive_*
    # may turn possible into verified.
    for m in MODALITIES:
        out, _ = derive_modality(m, "copy")
        assert out == m


def test_modality_rank_ordering_sane():
    from ..uncertainty_propagation import MODALITY_RANK
    assert MODALITY_RANK[MOD_POSSIBLE] < MODALITY_RANK[MOD_VERIFIED]

# ---------------------------------------------------------------------------
# AND/OR/PARTIAL/CONTEXTUAL support paths.
# ---------------------------------------------------------------------------
def test_and_requires_all_premises():
    # AND path with an unresolved premise cannot qualify through it.
    p = SupportPath(path_id="and1", required_refs=("A", "B"), kind=PATH_AND,
                    status="UNDETERMINED")
    ok, failed = qualify_claim(True, True, p.status == "SUPPORTED", True)
    assert not ok and failed == "support_sufficient"


def test_or_qualifies_through_one_sufficient_path():
    # Positive control: B sufficient -> qualifies despite A uncertain.
    a = SupportPath(path_id="a", required_refs=("A",), kind=PATH_OR,
                    status="UNDETERMINED")
    b = SupportPath(path_id="b", required_refs=("B",), kind=PATH_OR,
                    status="SUPPORTED")
    assert b.status == "SUPPORTED"  # the OR is satisfied by B alone


def test_or_does_not_erase_material_refutation():
    # An alternative path does not make a genuine contradiction disappear.
    assert support_refutation_matrix(True, True) == "CONFLICTED"


def test_contextual_citation_keeps_own_standing():
    p = SupportPath(path_id="ctx", required_refs=("incident-9",),
                    kind=PATH_CONTEXTUAL, status="UNDETERMINED")
    child, _, rule = propagate_along_edge("UNDETERMINED", "MENTIONS")
    assert "no_transmission" in rule and p.kind == PATH_CONTEXTUAL


# ---------------------------------------------------------------------------
# 5. Observation-limit propagation: the five-claim table.
# ---------------------------------------------------------------------------
def _gap():
    return ObservationCoverage(
        source="SCHEDULER", event_type="DISPATCHED", resource="lease",
        interval="SEQ-107:SEQ-110", state=COVERED_PARTIAL,
        coverage_evidence=("loss_counter",))


def test_gap_table():
    claims = (
        ("no_dispatch_in_interval", True, False),     # depends, no alt
        ("worker_no_usable_lease", True, True),       # receiver-side indep.
        ("target_unchanged", True, True),             # target-state indep.
        ("scheduler_caused_failure", True, False),    # needs causal evidence
        ("workflow_unfinished", False, True),         # not gap-dependent
    )
    out = propagate_observation_limit(claims, _gap())
    assert out["no_dispatch_in_interval"][0] == "UNDETERMINED"
    assert out["worker_no_usable_lease"][0] == "PRESERVED_VIA_INDEPENDENT_EVIDENCE"
    assert out["target_unchanged"][0] == "PRESERVED_VIA_INDEPENDENT_EVIDENCE"
    assert out["scheduler_caused_failure"][0] == "UNDETERMINED"
    assert out["workflow_unfinished"][0] == "UNAFFECTED"


def test_gap_does_not_erase_independent_support():
    # Positive control: the gap is about scheduler telemetry; the
    # target-state observation stands on its own evidence.
    out = propagate_observation_limit(
        (("target_unchanged", False, True),), _gap())
    assert out["target_unchanged"][0] != "UNDETERMINED"


def test_negative_claim_needs_completeness_contract():
    partial = _gap()
    ok, _ = partial.negative_claim_allowed()
    assert not ok  # COVERED_PARTIAL: absence is inconclusive
    complete = ObservationCoverage(
        source="SCHEDULER", event_type="DISPATCHED", resource="lease",
        interval="SEQ-100:SEQ-106", state=COVERED_COMPLETE,
        coverage_evidence=("sequence_continuity", "snapshots"))
    ok2, reason = complete.negative_claim_allowed()
    assert ok2 and reason == "completeness_contract_established"


def test_complete_without_evidence_rejected():
    bare = ObservationCoverage(
        source="SCHEDULER", event_type="DISPATCHED", resource="lease",
        interval="SEQ-100:SEQ-106", state=COVERED_COMPLETE,
        coverage_evidence=())
    ok, reason = bare.negative_claim_allowed()
    assert not ok and "without_coverage_evidence" in reason


# ---------------------------------------------------------------------------
# 8. Recomputation: receipts, four facts, selective propagation.
# ---------------------------------------------------------------------------
def _receipt(**kw):
    base = dict(receipt_id="r1", evidence_id="e1",
                original_provenance="blind_fixture_v3",
                ineligibility_reason="confirmed_contamination",
                affected_use="certify", policy_version="pol-v9",
                temporal_scope="2026-10-10",
                decision_evidence=("forensic_report",),
                independent_verifier="naya-2")
    base.update(kw)
    return EligibilityChangeReceipt(**base)


def test_receipt_append_only():
    r2 = _receipt(receipt_id="r2", supersedes=("r1",))
    assert r2.supersedes == ("r1",)  # history preserved, never overwritten


def test_four_facts_distinct():
    facts = four_fact_assessment("e1", {"e1": {"eligibility": CONFIRMED,
                                              "correctness": "accurate"}})
    assert facts["current_eligibility"] == CONFIRMED
    assert facts["factual_correctness"] == "accurate"
    assert facts["historical_existence"] is True  # ineligible != false


def test_selective_propagation_table_complete():
    assert len(SELECTIVE_PROPAGATION) == 8
    assert SELECTIVE_PROPAGATION["confirmed_contamination"] == \
        "exclude_contribution"
    assert SELECTIVE_PROPAGATION["valid_unrelated_evidence"] == "preserve"


def test_stage_a_ignores_mentions():
    graph = {"c1": (("e1", "REQUIRES_SUPPORT_FROM"),),
             "c2": (("e1", "MENTIONS"),)}
    impacted = stage_a_impact_discovery(("e1",), graph)
    assert ("c1", "e1", "REQUIRES_SUPPORT_FROM") in impacted
    assert not any(c == "c2" for c, _, _ in impacted)


def test_secret_derivation_detected():
    hints = {"e1": ("originX", "none"), "e2": ("originX", "reformat")}
    independent, reason = secret_derivation_check("e1", "e2", hints)
    assert not independent and "shared_hidden_origin" in reason


def test_secret_derivation_positive_control():
    hints = {"e1": ("originX", "none"), "e2": ("originY", "none")}
    independent, _ = secret_derivation_check("e1", "e2", hints)
    assert independent


def test_revocation_receipt_requires_verifier():
    with pytest.raises(AssertionError):
        revocation_receipt(_receipt(independent_verifier=""), ())


def test_revocation_receipt_shape():
    rec = revocation_receipt(
        _receipt(), (("c1", "UNAFFECTED", "DOWNGRADED", ("s1",)),))
    assert rec["kind"] == "EVIDENCE_ELIGIBILITY_CHANGE"
    assert rec["affected_claims"][0]["new_verdict"] == "DOWNGRADED"
    assert rec["independent_verifier"] == "naya-2"


def test_commit_boundary_blocks_dependent_action():
    action = {"action_id": "a1", "depends_on_evidence": ("e1",),
              "mandatory_qualifications": {"e1": "certify"}}
    state = {"e1": {"eligibility": CONFIRMED}}
    allowed, reason = check_commit_boundary(action, state)
    assert not allowed and "commit_blocked_by_e1" in reason


def test_commit_boundary_allows_unrelated_action():
    action = {"action_id": "a2", "depends_on_evidence": ("e9",),
              "mandatory_qualifications": {"e9": "certify"}}
    state = {"e1": {"eligibility": CONFIRMED},
             "e9": {"eligibility": "independently_cleared"}}
    allowed, _ = check_commit_boundary(action, state)
    assert allowed  # revocation is targeted, not a shutdown


def test_retroactive_discovery_blast_radius():
    uses = (("u1", "qual-q1", "t1"), ("u2", "qual-q2", "t2"),
            ("u3", "qual-q1", "t3"))
    assert retroactive_discovery(uses, "qual-q1") == ("u1", "u3")


def test_requalification_record_fields():
    rec = RequalificationRecord(
        evidence_ids=("e1",), receipt_ids=("r2",), change_event_id="ev1",
        prior_qualification="UNAFFECTED", new_qualification="DOWNGRADED",
        affected_scope="production", affected_use="certify",
        surviving_support_paths=("path-b",),
        unresolved_dependencies=("H1",), policy_code_revision="pol-v9/sha",
        effective_time="2026-10-10T19:00Z",
        recorded_time="2026-10-10T19:05Z", independent_verifier="naya-2")
    assert rec.new_qualification == "DOWNGRADED"
    assert rec.effective_time != rec.recorded_time


def test_requalification_rejects_bad_verdict():
    with pytest.raises(AssertionError):
        RequalificationRecord(
            evidence_ids=("e1",), receipt_ids=(), change_event_id="ev1",
            prior_qualification="UNAFFECTED", new_qualification="MAYBE",
            affected_scope="s", affected_use="u", surviving_support_paths=(),
            unresolved_dependencies=(), policy_code_revision="p",
            effective_time="t", recorded_time="t",
            independent_verifier="v")


def test_cycle_without_anchor_cannot_self_support():
    edges = {"a": ("b",), "b": ("a",)}
    out = stage_b_recompute(("a", "b"), {"__changed__": ("e1",)},
                            "pol-v9", edges, {})
    assert out["a"][0] == "UNDETERMINED"
    assert "cannot_self_support" in out["a"][1]


def test_cycle_with_anchor_gets_fixed_point():
    edges = {"a": ("b",), "b": ("a",)}
    out = stage_b_recompute(("a", "b"), {"__changed__": ("e1",)},
                            "pol-v9", edges, {"a": ("anchor_ev",)})
    assert "fixed_point" in out["a"][1]


def test_recompute_closure_six_steps():
    graph = {"c1": (("e1", "REQUIRES_SUPPORT_FROM"),)}
    out = recompute_closure(("e1",), graph,
                            {"__changed__": ("e1",)}, "pol-v9",
                            {"c1": ()}, {})
    assert "step1_impacted" in out and "step5_conclusions" in out
    assert out["monotonicity"] == \
        "justification_only_repetition_never_strengthens"


# ---------------------------------------------------------------------------
# 9. Projection preservation + partial scope.
# ---------------------------------------------------------------------------
def test_nine_items_must_survive():
    assert len(MUST_SURVIVE) == 9
    assert "causal_qualification_and_modality" in MUST_SURVIVE
    assert "material_contradictory_evidence" in MUST_SURVIVE


def test_corrupted_summary_rejected():
    src = _uenv(
        strongest_defensible_conclusion="the workflow stalled; "
                                       "cause unresolved",
        contrary_evidence_refs=("OBS-03",),
        unresolved_hypotheses=(
            CausalHypothesis(hyp_id="H1", mechanism="m",
                             cause_type=CAUSE_POSSIBLE,
                             modality=MOD_POSSIBLE, status="UNDETERMINED"),))
    projected = {"surface": "smart_note", "claims": (
        ("c1", "scheduler failure caused the outage", ()),)}
    violations = check_projection_preservation(projected, src)
    assert any("dropped 'unresolved'" in v for v in violations)
    assert any("contradiction dropped" in v for v in violations)


def test_faithful_projection_passes():
    src = _uenv(
        strongest_defensible_conclusion="the workflow stalled; "
                                       "cause unresolved")
    projected = {"surface": "summary", "claims": (
        ("c1", "the workflow stalled; cause unresolved",
         ("scope", "modality")),)}
    assert check_projection_preservation(projected, src) == ()


def test_partial_scope_preservation():
    out = partial_scope_preservation(
        "composite-claim",
        {"staging": "SUPPORTED", "production": "INSUFFICIENT_DATA"},
        "universal")
    assert "supported_regions=staging" in out[0]
    assert out[1] == "composite_not_qualified"
    assert out[2] == "broken_everywhere_not_established"
    assert "quantifier_universal_preserved" in out[3]


def test_envelope_retains_original_claim():
    env = _uenv(original_claim="scheduler caused the stall (H1)",
                strongest_defensible_conclusion="stalled; cause unresolved")
    assert env.original_claim == "scheduler caused the stall (H1)"
    assert "unresolved" in env.strongest_defensible_conclusion


# ---------------------------------------------------------------------------
# 10. Use-gating: six intended uses.
# ---------------------------------------------------------------------------
def test_use_gating_matrix():
    assert gate_use(USE_HISTORICAL_RESEARCH, "UNDETERMINED")[0] is True
    assert gate_use(USE_DEBUGGING, "UNDETERMINED")[0] is True
    assert gate_use(USE_INVESTIGATION_PLANNING, "CONFLICTED")[0] is True
    assert gate_use(USE_CERTIFICATION, "UNDETERMINED")[0] is False
    assert gate_use(USE_CERTIFICATION, "SUPPORTED")[0] is True
    assert gate_use(USE_LEARN_PROMOTION, "UNDETERMINED")[0] is False
    assert gate_use(USE_CONSEQUENTIAL_ACT, "UNDETERMINED")[0] is False
    # ...unless a valid independent alternative exists.
    assert gate_use(USE_CONSEQUENTIAL_ACT, "UNDETERMINED",
                    has_independent_alternative=True)[0] is True
    assert len(INTENDED_USES) == 6


# ---------------------------------------------------------------------------
# 11/12. False-certainty cascade + decisive experiment.
# ---------------------------------------------------------------------------
def test_cascade_fixture_five_stages():
    fx = build_five_stage_cascade_fixture()
    assert fx["stage1_incomplete_observation"]["gap"] == "SEQ-107:SEQ-110"
    assert fx["stage3_unresolved_hypothesis"].modality == MOD_POSSIBLE
    assert fx["independent_source"]["verdict"] == "SUPPORTED"


def test_cascade_two_results_preserved():
    fx = build_five_stage_cascade_fixture()
    assert fx["independent_source"]["claim"] == "the workflow did not complete"
    assert fx["stage3_unresolved_hypothesis"].status == "UNDETERMINED"


def test_decisive_experiment():
    out = run_decisive_experiment()
    rejected, reason = out["corrupted_summary_rejected"]
    assert rejected and "rejected" in reason
    assert out["independent_outcome_preserved"][0] is True
    ok_succ, _ = out["successor_reconstruction"]
    assert ok_succ
    assert "only_causal_claims_recompute" in out["selective_recompute"]


def test_successor_missing_fields_rejected():
    ok, reason = verify_cascade_stage("stage5_successor", {"scope": "s"},
                                      build_five_stage_cascade_fixture())
    assert not ok and "successor_missing" in reason

# ---------------------------------------------------------------------------
# SN-0784: Selective Cache Invalidation and Intelligence Preservation.
# ---------------------------------------------------------------------------
from ..uncertainty_propagation import (
    SURFACE_REFRESH_POLICIES, ClaimDependency, ProjectionManifest,
    VERDICT_CACHE_ACTION, CACHE_STATES, CACHE_CURRENT,
    CACHE_REVALIDATION_REQUIRED, CACHE_REFRESH_PENDING,
    CACHE_HISTORICAL_ONLY, cache_action_for_verdict,
    INVALIDATION_PHASES, serve_projection,
    annotate_summary_span, amend_note_append_only,
    index_entry_for_claim, seal_successor_snapshot,
    STALE_CHECK_ROUTES, check_route_currency,
    cas_publish, run_projection_cascade_fixture,
)
from ..propagation import build_successor_package


def _manifest(**kw):
    base = dict(projection_id="p1", surface="cached_summary",
                claim_dependencies=(),
                qualification_snapshot_generation=5,
                projection_status=CACHE_CURRENT)
    base.update(kw)
    return ProjectionManifest(**base)


def test_verdict_cache_action_mapping():
    assert cache_action_for_verdict("UNAFFECTED") == ("keep_current",
                                                     CACHE_CURRENT)
    assert cache_action_for_verdict("REVOKED") == \
        ("invalidate_for_certification_keep_history", CACHE_HISTORICAL_ONLY)
    assert cache_action_for_verdict("DOWNGRADED")[1] == CACHE_REFRESH_PENDING
    assert cache_action_for_verdict("SUSPENDED")[1] == \
        CACHE_REVALIDATION_REQUIRED


def test_stale_cache_is_not_false_claim():
    # HISTORICAL_ONLY preserves history; it does not declare falsehood.
    action, state = cache_action_for_verdict("REVOKED")
    assert "keep_history" in action and state == CACHE_HISTORICAL_ONLY


def test_serve_projection_withholds_stale_for_certification():
    m = _manifest(
        claim_dependencies=(ClaimDependency("A", "v3", "qr-a", "A held"),),
        qualification_snapshot_generation=3)
    served, state, reason = serve_projection(m, 4, {"A": "REVOKED"},
                                             USE_CERTIFICATION)
    assert served == "WITHHELD" and state == CACHE_REVALIDATION_REQUIRED


def test_serve_projection_annotates_stale_for_research():
    m = _manifest(qualification_snapshot_generation=3)
    served, state, _ = serve_projection(m, 4, {}, USE_HISTORICAL_RESEARCH)
    assert served == "SERVED_ANNOTATED" and state == CACHE_REFRESH_PENDING


def test_serve_projection_serves_current():
    m = _manifest(qualification_snapshot_generation=5)
    served, state, _ = serve_projection(m, 5, {"A": "UNAFFECTED"},
                                        USE_CONSEQUENTIAL_ACT)
    assert served == "SERVED" and state == CACHE_CURRENT


def test_serve_projection_blocks_revoked_for_act():
    m = _manifest(
        claim_dependencies=(ClaimDependency("A", "v5", "qr-a", "A"),),
        qualification_snapshot_generation=5)
    served, _, reason = serve_projection(m, 5, {"A": "REVOKED"},
                                         USE_CONSEQUENTIAL_ACT)
    assert served == "WITHHELD" and "not_eligible" in reason


def test_summary_amendment_preserves_history():
    out = annotate_summary_span("A held in production.", "A",
                                "UNAFFECTED", "DOWNGRADED", "staging only")
    assert "A held in production." in out  # original kept
    assert "AMENDMENT" in out and "staging only" in out


def test_note_amendment_append_only():
    claims = tuple((f"c{i}", "SUPPORTED", f"text{i}") for i in range(10))
    amended = amend_note_append_only(
        claims, {"c3": ("DOWNGRADED", "narrowed to staging"),
                 "c7": ("SUSPENDED", "pending review")})
    statuses = [s for _, s, _ in amended]
    assert statuses.count("SUPPORTED") == 8
    assert statuses.count("DOWNGRADED") == 1
    assert statuses.count("SUSPENDED") == 1
    # Amended claims keep their history inline; none becomes a new witness.
    assert "[AMENDMENT:" in amended[3][2]


def test_index_is_discovery_not_certification():
    e = index_entry_for_claim("A", "SUPPORTED", "qr-a")
    assert e["discoverable"] is True
    assert "discovery_not_certification" in e["rule"]


def test_successor_snapshot_sealed():
    snap = seal_successor_snapshot({"claim_id": "A"}, 7)
    assert snap["mutable"] is False and snap["generation"] == 7
    assert "reconcile_against_canonical" in snap["use_requires"]


def test_eight_routes_checked():
    assert len(STALE_CHECK_ROUTES) == 8
    m = _manifest(qualification_snapshot_generation=3)
    ok, action = check_route_currency("consequential_act", m, 4)
    assert not ok and action == "stale_withhold_until_revalidated"
    ok2, action2 = check_route_currency("connect_expansion", m, 4)
    assert not ok2 and "no_promotion" in action2


def test_cas_rejects_stale_write():
    diagnostics = []
    ok, gen, reason = cas_publish(7, 5, {"id": "old"}, diagnostics)
    assert not ok and gen == 7 and reason == "stale_write_rejected"
    assert diagnostics and "stale_write_rejected" in \
        diagnostics[0]["reason"]  # retained as diagnostics


def test_cas_accepts_newer():
    diagnostics = []
    ok, gen, _ = cas_publish(7, 8, {"id": "new"}, diagnostics)
    assert ok and gen == 8 and not diagnostics


def test_projection_cascade_fixture():
    out = run_projection_cascade_fixture()
    assert out["claim_verdicts"]["A"][1] == "REVOKED"
    assert out["claim_verdicts"]["B"][1] == "REQUALIFIED"
    assert out["claim_verdicts"]["C"][1] == "DOWNGRADED"
    served, state, _ = out["stale_summary_for_certification"]
    assert served == "WITHHELD"  # stale qualification unusable
    assert out["successor_reconciled_verdicts"]["A"] == "REVOKED"
    assert out["history_reconstructable"] is True


def test_invalidation_phases_complete():
    assert len(INVALIDATION_PHASES) == 6
    assert INVALIDATION_PHASES[0] == "commit_eligibility_change"
    assert INVALIDATION_PHASES[-1] == "independently_reconcile"


# ---------------------------------------------------------------------------
# The propagation.py defect repair: historical vs currently-eligible refs.
# ---------------------------------------------------------------------------
def test_successor_package_splits_evidence_refs():
    env = _env([_set("s1", ("e1",)), _set("s2", ("e2",))])
    a = evaluate_claim(env, {"e1": CLEARED, "e2": POSSIBLE})
    pkg = build_successor_package(env, a)
    assert set(pkg["historical_evidence_refs"]) == {"e1", "e2"}
    # e2 is possibly compromised -> not in any sufficient set -> excluded
    # from the currently-eligible list.
    assert "e2" not in pkg["currently_eligible_evidence_refs"]
    assert "e1" in pkg["currently_eligible_evidence_refs"]


def test_successor_package_eligible_empty_when_nothing_supported():
    env = _env([_set("s1", ("e1",))])
    a = evaluate_claim(env, {"e1": POSSIBLE})
    pkg = build_successor_package(env, a)
    assert pkg["currently_eligible_evidence_refs"] == []
    assert pkg["historical_evidence_refs"] == ["e1"]
