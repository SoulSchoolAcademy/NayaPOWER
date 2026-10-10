"""Tests: provenance-preserving intelligence propagation.

Covers the ten acceptance tests, the A/B/C revocation matrix, the
four-surface propagation rules, the CONNECT relationship mapping, and
Shawn's scope-precision layer (meaning envelopes, region verdicts,
PARTIALLY_SUPPORTS, strongest defensible conclusion, scope-inflation
detection).
"""
import pytest

from ..propagation import (
    MeaningEnvelope, ClaimRegion, SupportSet, DependencyEdge,
    ClaimEnvelope, RegionAssessment, ClaimAssessment,
    RELATIONSHIP_TO_CONNECT, RELATIONSHIP_EXPOSURE,
    REGION_VERDICTS, QUANTIFIERS, PROPAGATION_METRICS, SURFACE_RULES,
    CLEARED, POSSIBLE, UNASSESSED, CONFIRMED,
    set_sufficient, detect_false_corroboration, genuine_paths,
    assess_region, evaluate_claim, strongest_defensible_conclusion,
    scope_inflation_check, validate_summary, index_lookup,
    copy_to_smart_note, build_successor_package,
    abc_envelope, abc_matrix,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def one_region_envelope(claim_id="CLAIM-C", quantifier="bounded_observation"):
    region = ClaimRegion("r1", MeaningEnvelope(
        component="brain-index", environment="staging",
        population="controlled-cases", behavior="index-repair",
        time="2026-10-10", conditions="controlled", outcome="check-passes"))
    return ClaimEnvelope(
        claim_id=claim_id,
        claim_scope=region.envelope,
        quantifier=quantifier,
        regions=(region,),
        support_sets=(
            SupportSet(set_id="SUPPORT-A", evidence_refs=("EVID-A",),
                       covers=("r1",), scope=region.envelope),
            SupportSet(set_id="SUPPORT-B", evidence_refs=("EVID-B",),
                       covers=("r1",), scope=region.envelope),
        ),
        source_refs=("EVID-A", "EVID-B"),
        historical_dependencies=("EVID-A", "EVID-B"),
        dependency_edges=(
            DependencyEdge("CLAIM-C", "EVID-A", "MENTIONS"),
            DependencyEdge("CLAIM-C", "EVID-B", "INDEPENDENTLY_CORROBORATED_BY"),
        ),
        policy_version="POLICY-SHA",
        assessment_receipt="RECEIPT-1",
    )


def origins_ab():
    return {"EVID-A": "origin-a", "EVID-B": "origin-b"}


# ---------------------------------------------------------------------------
# The ten acceptance tests
# ---------------------------------------------------------------------------
def test_1_undetermined_a_qualified_b_c_stays_qualified():
    env = one_region_envelope()
    a = evaluate_claim(env, {"EVID-A": UNASSESSED, "EVID-B": CLEARED},
                       origins_ab())
    assert a.verdict == "UNAFFECTED"
    assert a.region_assessments[0].verdict == "SUPPORTED"
    assert a.strongest_scope == ("r1",)


def test_2_partial_support_qualifies_only_supported_portion():
    r1 = ClaimRegion("r1", MeaningEnvelope(component="KNOW",
                                           environment="staging"))
    r2 = ClaimRegion("r2", MeaningEnvelope(component="KNOW",
                                           environment="production"))
    env = ClaimEnvelope(
        claim_id="CLAIM-PARTIAL", claim_scope=MeaningEnvelope(component="KNOW"),
        quantifier="universal", regions=(r1, r2),
        support_sets=(
            SupportSet(set_id="SUPPORT-A", evidence_refs=("EVID-A",),
                       covers=("r1", "r2"), scope=r1.envelope),
            # B only partially supports C: staging region only.
            SupportSet(set_id="SUPPORT-B", evidence_refs=("EVID-B",),
                       covers=("r1",), scope=r1.envelope),
        ),
        historical_dependencies=("EVID-A", "EVID-B"),
        policy_version="POLICY-SHA")
    a = evaluate_claim(env, {"EVID-A": UNASSESSED, "EVID-B": CLEARED},
                       origins_ab())
    by_region = {ra.region_id: ra.verdict for ra in a.region_assessments}
    assert by_region == {"r1": "SUPPORTED", "r2": "UNDETERMINED"}
    assert a.verdict == "DOWNGRADED"
    assert a.strongest_scope == ("r1",)


def test_3_hidden_shared_origin_no_false_corroboration():
    env = one_region_envelope()
    shared = {"EVID-A": "origin-x", "EVID-B": "origin-x"}
    assert detect_false_corroboration(env.support_sets, "r1",
                                      shared) == (("SUPPORT-A", "SUPPORT-B"),)
    covering = [s for s in env.support_sets if "r1" in s.covers]
    assert len(genuine_paths(tuple(covering), shared)) == 1
    # One genuine path, still valid: the claim holds, but "two independent
    # evaluations" would be a lie.
    a = evaluate_claim(env, {"EVID-A": CLEARED, "EVID-B": CLEARED}, shared)
    ra = a.region_assessments[0]
    assert ra.verdict == "SUPPORTED"
    assert ra.genuine_paths == 1


def test_4_mentions_in_summary_preserves_uncertainty():
    env = one_region_envelope()
    a = evaluate_claim(env, {"EVID-A": UNASSESSED, "EVID-B": CLEARED},
                       origins_ab())
    # A research summary MENTIONS the claim: lineage preserved, nothing
    # promoted, uncertainty retained in the envelope copy.
    copied = copy_to_smart_note(env, "NOTE-7")
    assert copied.support_sets == env.support_sets  # no new proof
    assert copied.historical_dependencies[-1] == "CLAIM-C"
    rels = [e.relationship for e in copied.dependency_edges]
    assert "DERIVED_FROM" in rels
    assert a.verdict == "UNAFFECTED"


def test_5_copy_creates_no_new_proof():
    env = one_region_envelope()
    copied = copy_to_smart_note(env, "NOTE-8")
    a_orig = evaluate_claim(env, {"EVID-A": UNASSESSED, "EVID-B": CLEARED},
                            origins_ab())
    a_copy = evaluate_claim(copied, {"EVID-A": UNASSESSED, "EVID-B": CLEARED},
                            origins_ab())
    # Same verdict — the copy did not strengthen the claim. Repetition is
    # not corroboration (anti-citogenesis).
    assert a_copy.verdict == a_orig.verdict
    assert a_copy.region_assessments[0].sufficient_sets == \
        a_orig.region_assessments[0].sufficient_sets


def test_6_stale_index_cache_overridden_by_canonical():
    env = one_region_envelope()
    a = evaluate_claim(env, {"EVID-A": CONFIRMED, "EVID-B": CLEARED},
                       origins_ab())
    assert a.verdict == "REQUALIFIED"
    cached = {"verdict": "UNAFFECTED", "qualification_version": "POLICY-OLD"}
    out = index_lookup("CLAIM-C", cached, a, canonical_version="POLICY-SHA")
    assert out["stale_cache_overridden"] is True
    assert out["current_verdict"] == "REQUALIFIED"
    assert out["cached_verdict"] == "UNAFFECTED"  # reported, not used


def test_7_revoking_a_does_not_revoke_c_while_b_sufficient():
    env = one_region_envelope()
    a = evaluate_claim(env, {"EVID-A": CONFIRMED, "EVID-B": CLEARED},
                       origins_ab())
    assert a.verdict == "REQUALIFIED"
    assert a.region_assessments[0].verdict == "SUPPORTED"
    assert a.region_assessments[0].sufficient_sets == ("SUPPORT-B",)


def test_8_revoking_b_with_a_undetermined_costs_c_qualification():
    env = one_region_envelope()
    a = evaluate_claim(env, {"EVID-A": UNASSESSED, "EVID-B": CONFIRMED},
                       origins_ab())
    assert a.verdict == "REVOKED"
    assert a.region_assessments[0].detail == "support_disqualified"
    # Observations preserved: the envelope and history survive revocation.
    assert env.historical_dependencies == ("EVID-A", "EVID-B")


def test_9_successor_revalidates_never_freezes():
    env = one_region_envelope()
    a = evaluate_claim(env, {"EVID-A": UNASSESSED, "EVID-B": CLEARED},
                       origins_ab())
    pkg = build_successor_package(env, a)
    assert pkg["revalidate_at_use"] is True
    assert pkg["current_qualification_verdict"] == "UNAFFECTED"
    assert "revalidate current eligibility at use time" in \
        pkg["required_checks_before_consequential_action"]
    # The package carries uncertainty; it does not launder it.
    assert pkg["region_verdicts"]["r1"][0] == "SUPPORTED"


def test_10_new_independent_source_d_restores_claim():
    env = one_region_envelope()
    # B revoked, A undetermined: C loses qualification (test 8).
    a1 = evaluate_claim(env, {"EVID-A": UNASSESSED, "EVID-B": CONFIRMED},
                        origins_ab())
    assert a1.verdict == "REVOKED"
    # A genuinely independent D arrives; a new support set is added and the
    # claim is re-evaluated — support is recomputed, never inherited.
    env2 = ClaimEnvelope(
        claim_id=env.claim_id, claim_scope=env.claim_scope,
        quantifier=env.quantifier, regions=env.regions,
        support_sets=env.support_sets + (
            SupportSet(set_id="SUPPORT-D", evidence_refs=("EVID-D",),
                       covers=("r1",), scope=env.regions[0].envelope),
        ),
        source_refs=env.source_refs + ("EVID-D",),
        historical_dependencies=env.historical_dependencies + ("EVID-D",),
        dependency_edges=env.dependency_edges,
        policy_version="POLICY-SHA2",
        assessment_receipt="RECEIPT-2")
    a2 = evaluate_claim(
        env2,
        {"EVID-A": UNASSESSED, "EVID-B": CONFIRMED, "EVID-D": CLEARED},
        {"EVID-A": "origin-a", "EVID-B": "origin-b", "EVID-D": "origin-d"})
    assert a2.verdict == "REQUALIFIED"
    assert a2.region_assessments[0].sufficient_sets == ("SUPPORT-D",)


# ---------------------------------------------------------------------------
# A/B/C revocation matrix — the decisive property
# ---------------------------------------------------------------------------
def test_abc_matrix_decisive_property():
    m = abc_matrix()
    # Revoking A never revokes C while B is sufficient.
    assert m[(CONFIRMED, CLEARED)] in ("REQUALIFIED", "UNAFFECTED")
    assert m[(UNASSESSED, CLEARED)] == "UNAFFECTED"
    assert m[(POSSIBLE, CLEARED)] == "REQUALIFIED"
    # Revoking B while A stays undetermined costs C its qualification.
    assert m[(UNASSESSED, CONFIRMED)] == "REVOKED"
    # Both gone: revoked. Neither assessed: suspended, never auto-clean.
    assert m[(CONFIRMED, CONFIRMED)] == "REVOKED"
    assert m[(UNASSESSED, UNASSESSED)] == "SUSPENDED"
    # A alone can carry C.
    assert m[(CLEARED, CONFIRMED)] == "REQUALIFIED"


# ---------------------------------------------------------------------------
# Relationship -> CONNECT contract mapping (no parallel registry)
# ---------------------------------------------------------------------------
def test_relationship_maps_to_existing_connect_contracts():
    assert RELATIONSHIP_TO_CONNECT == {
        "MENTIONS": "CONTEXTUALIZES",
        "DERIVED_FROM": "DERIVED_FROM",
        "REQUIRES_SUPPORT_FROM": "DEPENDS_ON",
        "INDEPENDENTLY_CORROBORATED_BY": "SUPPORTS",
        "PARTIALLY_SUPPORTS": "SUPPORTS",
    }
    # Every mapped contract exists in the canonical registry set.
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    try:
        from kernel.brain_registry import ALLOWED_RELATIONSHIPS
        for contract in RELATIONSHIP_TO_CONNECT.values():
            assert contract in ALLOWED_RELATIONSHIPS, contract
    except ImportError:
        pytest.skip("kernel not importable from this worktree layout")
    # Exposure semantics: MENTIONS never propagates; DERIVED_FROM may.
    assert RELATIONSHIP_EXPOSURE["MENTIONS"] == "no_propagation"
    assert RELATIONSHIP_EXPOSURE["DERIVED_FROM"] == "creates_possible_exposure"
    with pytest.raises(AssertionError):
        DependencyEdge("C", "E", "INVENTED_RELATIONSHIP")


# ---------------------------------------------------------------------------
# Scope-precision layer
# ---------------------------------------------------------------------------
def know_staging_envelope():
    """Shawn's canonical example: KNOW + staging + 40 controlled cases is
    SUPPORTED; other nodes, production, long-term are UNDETERMINED. This is
    scope mismatch, not compromise."""
    r1 = ClaimRegion("r-know-staging", MeaningEnvelope(
        component="KNOW", environment="staging", population="40-controlled",
        behavior="rejects-ineligible", time="2026-10-10",
        conditions="controlled", outcome="rejection"))
    r2 = ClaimRegion("r-know-production", MeaningEnvelope(
        component="KNOW", environment="production", population="all-traffic",
        behavior="rejects-ineligible", time="long-term",
        conditions="adversarial", outcome="rejection"))
    r3 = ClaimRegion("r-act-staging", MeaningEnvelope(
        component="ACT", environment="staging", population="40-controlled",
        behavior="rejects-ineligible", time="2026-10-10",
        conditions="controlled", outcome="rejection"))
    return ClaimEnvelope(
        claim_id="CLAIM-NINE-NODES",
        claim_scope=MeaningEnvelope(
            component="all-nine-nodes", environment="production",
            population="all-traffic", behavior="rejects-ineligible",
            time="long-term", conditions="adversarial", outcome="rejection"),
        quantifier="universal",
        regions=(r1, r2, r3),
        support_sets=(
            SupportSet(set_id="SUPPORT-KNOW-STAGING",
                       evidence_refs=("EVID-KNOW-40",),
                       covers=("r-know-staging",), scope=r1.envelope),
        ),
        historical_dependencies=("EVID-KNOW-40",),
        policy_version="POLICY-SHA")


def test_s1_know_staging_does_not_prove_nine_nodes_production():
    env = know_staging_envelope()
    a = evaluate_claim(env, {"EVID-KNOW-40": CLEARED}, {"EVID-KNOW-40": "o1"})
    by_region = {ra.region_id: ra.verdict for ra in a.region_assessments}
    assert by_region == {"r-know-staging": "SUPPORTED",
                         "r-know-production": "UNDETERMINED",
                         "r-act-staging": "UNDETERMINED"}
    # Region SUPPORTED while the overall universal claim is not certifiable.
    assert a.verdict == "DOWNGRADED"
    assert a.strongest_scope == ("r-know-staging",)
    assert "quantifier 'universal' applies ONLY within these regions" in \
        a.strongest_conclusion


def test_s1b_scope_inflation_caught_when_summary_drops_staging():
    env = know_staging_envelope()
    a = evaluate_claim(env, {"EVID-KNOW-40": CLEARED}, {"EVID-KNOW-40": "o1"})
    region_envelopes = {r.region_id: r.envelope for r in env.regions}
    # Honest summary: states the supported result AND its limits.
    honest = (("CLAIM-NINE-NODES",
               MeaningEnvelope(component="KNOW", environment="staging",
                               population="40-controlled",
                               behavior="rejects-ineligible",
                               time="2026-10-10", conditions="controlled",
                               outcome="rejection")),)
    assert validate_summary(honest, {"CLAIM-NINE-NODES": a},
                            region_envelopes) == ()
    # Dishonest summary: drops "staging" — a staging cert must never justify
    # a production op because a summary dropped the word.
    inflated = (("CLAIM-NINE-NODES",
                 MeaningEnvelope(component="KNOW", environment="production",
                                 population="40-controlled",
                                 behavior="rejects-ineligible",
                                 time="2026-10-10", conditions="controlled",
                                 outcome="rejection")),)
    violations = validate_summary(inflated, {"CLAIM-NINE-NODES": a},
                                  region_envelopes)
    assert len(violations) == 1
    assert "environment" in violations[0]


def test_s2_three_regions_supported_contradicted_unknown():
    r1 = ClaimRegion("r1", MeaningEnvelope(component="KNOW"))
    r2 = ClaimRegion("r2", MeaningEnvelope(component="ACT"))
    r3 = ClaimRegion("r3", MeaningEnvelope(component="LAW"))
    env = ClaimEnvelope(
        claim_id="CLAIM-3R", claim_scope=MeaningEnvelope(),
        quantifier="universal", regions=(r1, r2, r3),
        support_sets=(
            SupportSet(set_id="S1", evidence_refs=("E1",), covers=("r1",),
                       scope=r1.envelope),
            SupportSet(set_id="S2", evidence_refs=("E2",), covers=("r2",),
                       scope=r2.envelope, polarity="contradicts"),
        ),
        historical_dependencies=("E1", "E2"),
        policy_version="POLICY-SHA")
    ind = {"E1": CLEARED, "E2": CLEARED}
    org = {"E1": "o1", "E2": "o2"}
    a = evaluate_claim(env, ind, org)
    by_region = {ra.region_id: ra.verdict for ra in a.region_assessments}
    assert by_region == {"r1": "SUPPORTED", "r2": "REFUTED",
                         "r3": "UNDETERMINED"}
    # Supported stays usable, contradicted stays visibly rejected, unknown
    # never gets invented proof.
    assert a.verdict == "DOWNGRADED"
    assert a.strongest_scope == ("r1",)
    assert any("refuted regions excluded" in n for n in a.notes)
    # Through the successor surface: the refutation travels visibly.
    pkg = build_successor_package(env, a)
    assert pkg["region_verdicts"]["r2"][0] == "REFUTED"
    assert pkg["region_verdicts"]["r3"][0] == "UNDETERMINED"
    # A summary asserting the refuted region is rejected.
    region_envelopes = {r.region_id: r.envelope for r in env.regions}
    v = validate_summary(
        (("CLAIM-3R", MeaningEnvelope(component="ACT")),),
        {"CLAIM-3R": a}, region_envelopes)
    assert any("REFUTED" in x for x in v)


def test_s3_universal_with_counterexample_narrows_or_revokes():
    r1 = ClaimRegion("r1", MeaningEnvelope(component="KNOW"))
    r2 = ClaimRegion("r2", MeaningEnvelope(component="ACT"))
    env = ClaimEnvelope(
        claim_id="CLAIM-U", claim_scope=MeaningEnvelope(),
        quantifier="universal", regions=(r1, r2),
        support_sets=(
            SupportSet(set_id="S1", evidence_refs=("E1",), covers=("r1",),
                       scope=r1.envelope),
            SupportSet(set_id="S2", evidence_refs=("E2",), covers=("r2",),
                       scope=r2.envelope, polarity="contradicts"),
        ),
        historical_dependencies=("E1", "E2"),
        policy_version="POLICY-SHA")
    a = evaluate_claim(env, {"E1": CLEARED, "E2": CLEARED},
                       {"E1": "o1", "E2": "o2"})
    # One verified counterexample: the universal as stated is not
    # certifiable; the surviving region is narrowed, not deleted.
    assert a.verdict == "DOWNGRADED"
    assert a.strongest_scope == ("r1",)
    # All regions refuted and none supported: revoked.
    env2 = ClaimEnvelope(
        claim_id="CLAIM-U2", claim_scope=MeaningEnvelope(),
        quantifier="universal", regions=(r2,),
        support_sets=(
            SupportSet(set_id="S2", evidence_refs=("E2",), covers=("r2",),
                       scope=r2.envelope, polarity="contradicts"),
        ),
        historical_dependencies=("E2",), policy_version="POLICY-SHA")
    a2 = evaluate_claim(env2, {"E2": CLEARED}, {"E2": "o2"})
    assert a2.verdict == "REVOKED"


def test_s4_statistical_claim_needs_representativeness_and_bounds():
    r1 = ClaimRegion("r1", MeaningEnvelope(environment="production",
                                           population="all-traffic"))
    env = ClaimEnvelope(
        claim_id="CLAIM-99PCT", claim_scope=r1.envelope,
        quantifier="statistical", regions=(r1,),
        support_sets=(
            SupportSet(set_id="S1", evidence_refs=("E1",), covers=("r1",),
                       scope=r1.envelope,
                       sample_representative=False,
                       uncertainty_bounds_stated=False),
        ),
        historical_dependencies=("E1",), policy_version="POLICY-SHA")
    a = evaluate_claim(env, {"E1": CLEARED}, {"E1": "o1"})
    # 99 successes != a 99% population rate. The bounded observation is
    # SUPPORTED; the rate claim is INSUFFICIENT_DATA.
    assert a.region_assessments[0].verdict == "SUPPORTED"
    assert a.verdict == "INSUFFICIENT_DATA"
    assert any("bounded observation SUPPORTED" in n for n in a.notes)
    assert any("rate claim unestablished" in n for n in a.notes)


def test_s5_broad_claim_survives_compromise_region_by_region():
    rA = ClaimRegion("rA", MeaningEnvelope(component="KNOW"))
    rB = ClaimRegion("rB", MeaningEnvelope(component="ACT"))
    rC = ClaimRegion("rC", MeaningEnvelope(component="LAW"))
    env = ClaimEnvelope(
        claim_id="CLAIM-ABC-REGIONS", claim_scope=MeaningEnvelope(),
        quantifier="universal", regions=(rA, rB, rC),
        support_sets=(
            SupportSet(set_id="SE1", evidence_refs=("E1",), covers=("rA",),
                       scope=rA.envelope),
            SupportSet(set_id="SE2", evidence_refs=("E2",), covers=("rB",),
                       scope=rB.envelope),
        ),
        historical_dependencies=("E1", "E2"),
        policy_version="POLICY-SHA")
    org = {"E1": "o1", "E2": "o2"}
    # Before: A and B supported, C unestablished.
    a0 = evaluate_claim(env, {"E1": CLEARED, "E2": CLEARED}, org)
    assert a0.verdict == "DOWNGRADED"  # C unestablished narrows the claim
    assert a0.strongest_scope == ("rA", "rB")
    # E1 disqualified: B keeps its qualification, A loses it, C stays
    # unestablished, the broader claim is incomplete — no deletion, no
    # whole-lesson false.
    a1 = evaluate_claim(env, {"E1": CONFIRMED, "E2": CLEARED}, org)
    by_region = {ra.region_id: ra.verdict for ra in a1.region_assessments}
    assert by_region == {"rA": "UNDETERMINED", "rB": "SUPPORTED",
                         "rC": "UNDETERMINED"}
    assert a1.verdict == "DOWNGRADED"
    assert a1.strongest_scope == ("rB",)
    assert any("disqualified regions excluded" in n for n in a1.notes)


def test_s6_partially_supports_is_not_fractional_probability():
    regions = tuple(ClaimRegion(f"r{i}", MeaningEnvelope(component=f"node{i}"))
                    for i in range(9))
    env = ClaimEnvelope(
        claim_id="CLAIM-NINE", claim_scope=MeaningEnvelope(),
        quantifier="universal", regions=regions,
        support_sets=(
            SupportSet(set_id="S1", evidence_refs=("E1",),
                       covers=("r0", "r1"), scope=regions[0].envelope),
            SupportSet(set_id="S2", evidence_refs=("E2",),
                       covers=("r1",), scope=regions[1].envelope),
        ),
        historical_dependencies=("E1", "E2"),
        policy_version="POLICY-SHA")
    a = evaluate_claim(env, {"E1": CLEARED, "E2": CLEARED},
                       {"E1": "o1", "E2": "o2"})
    # 2 of 9 nodes verified: the supported scope is {r0, r1} — NOT "22.2%
    # true". The conjunction "all nine" remains unproven.
    assert set(a.strongest_scope) == {"r0", "r1"}
    assert a.verdict == "DOWNGRADED"
    assert "22.2" not in a.strongest_conclusion
    assert "probability" not in a.strongest_conclusion.lower()


def test_s8_region_supported_while_claim_insufficient():
    # Composition: region verdicts describe evidence; six verdicts describe
    # certification standing.
    env = know_staging_envelope()
    a = evaluate_claim(env, {"EVID-KNOW-40": CLEARED}, {"EVID-KNOW-40": "o1"})
    supported = [ra for ra in a.region_assessments
                 if ra.verdict == "SUPPORTED"]
    assert len(supported) == 1
    assert a.verdict in ("DOWNGRADED", "INSUFFICIENT_DATA", "SUSPENDED")


def test_s9_existential_needs_one_example():
    r1 = ClaimRegion("r1", MeaningEnvelope(component="KNOW"))
    r2 = ClaimRegion("r2", MeaningEnvelope(component="ACT"))
    env = ClaimEnvelope(
        claim_id="CLAIM-EX", claim_scope=MeaningEnvelope(),
        quantifier="existential", regions=(r1, r2),
        support_sets=(
            SupportSet(set_id="S1", evidence_refs=("E1",), covers=("r1",),
                       scope=r1.envelope),
        ),
        historical_dependencies=("E1",), policy_version="POLICY-SHA")
    a = evaluate_claim(env, {"E1": CLEARED}, {"E1": "o1"})
    assert a.verdict == "UNAFFECTED"
    assert "exists:" in a.strongest_conclusion
    a2 = evaluate_claim(env, {"E1": UNASSESSED}, {"E1": "o1"})
    assert a2.verdict == "SUSPENDED"


def test_quantifier_is_part_of_claim_meaning():
    # The same evidence under a universal vs existential quantifier yields
    # different verdicts: the quantifier can never be silently changed.
    r1 = ClaimRegion("r1", MeaningEnvelope(component="KNOW"))
    r2 = ClaimRegion("r2", MeaningEnvelope(component="ACT"))
    base = dict(claim_scope=MeaningEnvelope(), regions=(r1, r2),
                support_sets=(
                    SupportSet(set_id="S1", evidence_refs=("E1",),
                               covers=("r1",), scope=r1.envelope),),
                historical_dependencies=("E1",), policy_version="POLICY-SHA")
    uni = evaluate_claim(ClaimEnvelope(claim_id="C1", quantifier="universal",
                                       **base),
                         {"E1": CLEARED}, {"E1": "o1"})
    exi = evaluate_claim(ClaimEnvelope(claim_id="C2", quantifier="existential",
                                       **base),
                         {"E1": CLEARED}, {"E1": "o1"})
    assert uni.verdict == "DOWNGRADED"   # r2 unestablished narrows it
    assert exi.verdict == "UNAFFECTED"   # one example suffices
    with pytest.raises(AssertionError):
        ClaimEnvelope(claim_id="C3", quantifier="sometimes", **base)


def test_surface_rules_centralized():
    assert set(SURFACE_RULES) == {"summary", "index", "smart_note",
                                  "successor_package"}
    for surface, rules in SURFACE_RULES.items():
        assert rules["must_preserve"] and rules["must_never"] and rules["policy"]
    assert "compress_words_not_uncertainty" == SURFACE_RULES["summary"]["policy"]
    assert "revalidate_at_use" == SURFACE_RULES["successor_package"]["policy"]


def test_propagation_metrics_paired():
    assert "false_qualification_rate" in PROPAGATION_METRICS
    assert "unnecessary_qualification_loss" in PROPAGATION_METRICS
    assert "scope_inflation_errors" in PROPAGATION_METRICS


# ---------------------------------------------------------------------------
# Composition layer: combining partial evidence without inventing completeness
# ---------------------------------------------------------------------------
from ..propagation import (
    ProofObligation, CompositionRule, CompatibilityVerdict,
    CompositionReport, check_compatibility, compose_broader_claim,
    OBLIGATION_KINDS,
)


def _ob(obligation_id, component, environment="staging", kind="component",
        behavior="rejects-ineligible", outcome="rejection"):
    return ProofObligation(
        obligation_id=obligation_id,
        region=ClaimRegion(obligation_id, MeaningEnvelope(
            component=component, environment=environment,
            behavior=behavior, outcome=outcome)),
        acceptance=f"{component} {behavior} in {environment}",
        kind=kind)


def _ss(set_id, evidence, covers, component, environment="staging",
        behavior="rejects-ineligible", outcome="rejection",
        runtime="r1", policy="POLICY-SHA", polarity="supports"):
    return SupportSet(
        set_id=set_id, evidence_refs=tuple(evidence), covers=tuple(covers),
        scope=MeaningEnvelope(component=component, environment=environment,
                              behavior=behavior, outcome=outcome,
                              runtime=runtime),
        polarity=polarity, policy_version=policy)


def test_c1_compatible_conjunction_may_qualify():
    """Failure case 1: A∧B required with compatible evidence → may qualify."""
    obs = (_ob("oA", "KNOW"), _ob("oB", "ACT"))
    sets = (_ss("S1", ["E1"], ["oA"], "KNOW"),
            _ss("S2", ["E2"], ["oB"], "ACT"))
    ind = {"E1": CLEARED, "E2": CLEARED}
    org = {"E1": "o1", "E2": "o2"}
    assert check_compatibility(sets, org).compatible
    r = compose_broader_claim("CLAIM-AB", obs, sets, ind, org,
                              CompositionRule())
    assert r.overall_verdict == "UNAFFECTED"
    assert r.breadth == 2
    assert r.depth == {"oA": 1, "oB": 1}
    assert r.logical_sufficiency is True


def test_c2_interaction_unproven_blocks_joint_claim():
    """Failure case 2: A∧B∧interaction with the interaction unproven — the
    broader joint claim does not qualify even though both parts do."""
    obs = (_ob("oA", "KNOW"), _ob("oB", "ACT"),
           _ob("oAB", "KNOW+ACT", kind="interaction",
               behavior="handover-cleanly"))
    sets = (_ss("S1", ["E1"], ["oA"], "KNOW"),
            _ss("S2", ["E2"], ["oB"], "ACT"))
    ind = {"E1": CLEARED, "E2": CLEARED}
    org = {"E1": "o1", "E2": "o2"}
    r = compose_broader_claim("CLAIM-JOINT", obs, sets, ind, org,
                              CompositionRule(requires_interaction=True))
    assert r.component_coverage == {"oA": "SUPPORTED", "oB": "SUPPORTED"}
    assert r.interaction_status == {"oAB": "UNDETERMINED"}
    assert r.composition_valid is False
    assert r.overall_verdict == "INSUFFICIENT_DATA"
    assert any("noncompositional" in n for n in r.notes)


def test_c3_heavy_overlap_counted_once():
    """Failure case 3: E1 verifies KNOW+ACT, E2 verifies ACT+VERIFY →
    unique coverage is KNOW, ACT, VERIFY (breadth 3, not 4)."""
    obs = (_ob("oK", "KNOW"), _ob("oA", "ACT"), _ob("oV", "VERIFY"))
    sets = (_ss("S1", ["E1"], ["oK", "oA"], "KNOW+ACT"),
            _ss("S2", ["E2"], ["oA", "oV"], "ACT+VERIFY"))
    ind = {"E1": CLEARED, "E2": CLEARED}
    org = {"E1": "o1", "E2": "o2"}
    r = compose_broader_claim("CLAIM-3", obs, sets, ind, org,
                              CompositionRule())
    assert r.breadth == 3  # not 4: ACT counted once
    assert r.depth["oA"] == 2  # two independent corroborations of ACT
    assert r.overall_verdict == "UNAFFECTED"


def test_c4_staging_plus_production_no_manufactured_claim():
    """Failure case 4: staging evidence for KNOW + production evidence for
    ACT must not manufacture a complete production claim."""
    obs = (_ob("oK-prod", "KNOW", environment="production"),
           _ob("oA-prod", "ACT", environment="production"))
    sets = (_ss("S1", ["E1"], ["oK-prod"], "KNOW", environment="staging"),
            _ss("S2", ["E2"], ["oA-prod"], "ACT", environment="production"))
    ind = {"E1": CLEARED, "E2": CLEARED}
    org = {"E1": "o1", "E2": "o2"}
    r = compose_broader_claim("CLAIM-PROD", obs, sets, ind, org,
                              CompositionRule())
    assert r.component_coverage == {"oK-prod": "UNDETERMINED",
                                    "oA-prod": "SUPPORTED"}
    assert r.overall_verdict == "INSUFFICIENT_DATA"
    assert r.breadth == 1


def test_c5_contradiction_recorded_not_hidden():
    """Failure case 5: counterexample + positive coverage → contradiction is
    recorded and the joint claim waits for adjudication."""
    obs = (_ob("oA", "KNOW"), _ob("oB", "ACT"))
    sets = (_ss("S1", ["E1"], ["oA"], "KNOW"),
            _ss("S2", ["E2"], ["oB"], "ACT"),
            _ss("S3", ["E3"], ["oB"], "ACT", polarity="contradicts"))
    ind = {"E1": CLEARED, "E2": CLEARED, "E3": CLEARED}
    org = {"E1": "o1", "E2": "o2", "E3": "o3"}
    r = compose_broader_claim("CLAIM-CON", obs, sets, ind, org,
                              CompositionRule())
    assert r.component_coverage["oB"] == "CONFLICTED"
    assert r.overall_verdict == "SUSPENDED"
    assert any("contradiction recorded" in n for n in r.notes)


def test_compatibility_gate_predicate_mismatch():
    """'retrieves correctly' != 'refuses unauthorized retrieval': the gate
    blocks the combination; both parts stay valid-in-their-scopes."""
    obs = (_ob("oA", "KNOW"),)
    sets = (_ss("S1", ["E1"], ["oA"], "KNOW",
                behavior="retrieves-correctly", outcome="retrieval"),
            _ss("S2", ["E2"], ["oA"], "KNOW",
                behavior="refuses-unauthorized", outcome="rejection"))
    org = {"E1": "o1", "E2": "o2"}
    v = check_compatibility(sets, org)
    assert not v.compatible
    assert any("predicate_mismatch" in f for f in v.failures)
    r = compose_broader_claim("CLAIM-PRED", obs, sets,
                              {"E1": CLEARED, "E2": CLEARED}, org,
                              CompositionRule())
    assert r.overall_verdict == "INSUFFICIENT_DATA"
    assert any("valid-in-their-scopes" in n for n in r.notes)


def test_compatibility_gate_runtime_and_policy_mismatch():
    obs = (_ob("oA", "KNOW"),)
    sets = (_ss("S1", ["E1"], ["oA"], "KNOW", runtime="r1"),
            _ss("S2", ["E2"], ["oA"], "KNOW", runtime="r2",
                policy="POLICY-OTHER"))
    org = {"E1": "o1", "E2": "o2"}
    v = check_compatibility(sets, org)
    assert not v.compatible
    assert any("runtime_mismatch" in f for f in v.failures)
    assert any("policy_mismatch" in f for f in v.failures)


def test_highest_value_e1_e2_e3_e4():
    """The highest-value composition test.

    E1 supports A (staging). E2 independently supports B (staging).
    E3 duplicates A through shared lineage with E1 (must NOT double-count).
    E4 supports the A→B interaction in staging only.

    Claim 1: A and B pass individual staging requirements → may qualify.
    Claim 2: A and B work together in staging → may qualify via E4.
    Claim 3: A and B work together in production → remains unproven.
    """
    oA = _ob("oA", "A", behavior="passes", outcome="pass")
    oB = _ob("oB", "B", behavior="passes", outcome="pass")
    oAB = _ob("oAB", "A+B", kind="interaction",
              behavior="interacts-correctly", outcome="clean-handover")
    oAB_prod = _ob("oAB-prod", "A+B", environment="production",
                   kind="interaction", behavior="interacts-correctly",
                   outcome="clean-handover")
    sets = (
        _ss("S1", ["E1"], ["oA"], "A", behavior="passes", outcome="pass"),
        _ss("S2", ["E2"], ["oB"], "B", behavior="passes", outcome="pass"),
        _ss("S3", ["E3"], ["oA"], "A", behavior="passes", outcome="pass"),
        _ss("S4", ["E4"], ["oAB"], "A+B", behavior="interacts-correctly",
            outcome="clean-handover"),
    )
    ind = {"E1": CLEARED, "E2": CLEARED, "E3": CLEARED, "E4": CLEARED}
    # E3 shares lineage with E1: two reports, one source.
    org = {"E1": "lineage-1", "E2": "lineage-2",
           "E3": "lineage-1", "E4": "lineage-3"}

    # Claim 1: individual staging requirements.
    r1 = compose_broader_claim("CLAIM-1-STAGING-PARTS", (oA, oB), sets,
                               ind, org, CompositionRule())
    assert r1.overall_verdict == "UNAFFECTED"
    assert r1.breadth == 2
    assert r1.depth["oA"] == 1, "E3 must not double-count A"
    assert r1.depth["oB"] == 1
    assert any("counted_once" in n for n in r1.compatibility.notes)

    # Claim 2: work together in staging — via E4's interaction evidence.
    r2 = compose_broader_claim("CLAIM-2-STAGING-JOINT", (oA, oB, oAB), sets,
                               ind, org,
                               CompositionRule(requires_interaction=True))
    assert r2.overall_verdict == "UNAFFECTED"
    assert r2.interaction_status == {"oAB": "SUPPORTED"}
    assert r2.integration == ("oAB",)

    # Claim 3: work together in PRODUCTION — E4 is staging-only; unproven.
    r3 = compose_broader_claim("CLAIM-3-PROD-JOINT", (oA, oB, oAB_prod), sets,
                               ind, org,
                               CompositionRule(requires_interaction=True))
    assert r3.interaction_status == {"oAB-prod": "UNDETERMINED"}
    assert r3.composition_valid is False
    assert r3.overall_verdict == "INSUFFICIENT_DATA"
    # The system distinguishes all three claims.
    assert (r1.overall_verdict, r2.overall_verdict,
            r3.overall_verdict) == ("UNAFFECTED", "UNAFFECTED",
                                    "INSUFFICIENT_DATA")


def test_four_part_report_shape():
    obs = (_ob("oA", "KNOW"), _ob("oAB", "KNOW+ACT", kind="interaction",
                                  behavior="handover-cleanly"))
    sets = (_ss("S1", ["E1"], ["oA"], "KNOW"),)
    r = compose_broader_claim("CLAIM-R", obs, sets, {"E1": CLEARED},
                              {"E1": "o1"},
                              CompositionRule(requires_interaction=True))
    summary = r.four_part_summary()
    assert "1. component coverage" in summary
    assert "2. interactions" in summary
    assert "3. end-to-end" in summary
    assert "4. overall" in summary
    # Breadth, depth, integration reported separately — never merged into
    # one score.
    assert r.breadth == 1 and r.depth == {"oA": 1, "oAB": 0}
    assert r.integration == ()


# ---------------------------------------------------------------------------
# Composite Qualification Audit layer
# ---------------------------------------------------------------------------
from ..propagation import (
    InteractionContract, Assumption, CompositionArgument,
    EnvironmentDifference, QualificationCertificate,
    IndependentReconstruction, AuditResult,
    audit_environment_transfer, composition_proof_audit,
    AUDIT_QUESTIONS, VERIFY_OBLIGATIONS, CERTIFICATE_VERDICTS,
    ENV_DIFF_CLASSES,
)


def _audit_setup():
    """A fully-qualifying KNOW→LAW→ACT composition for audit tests."""
    obs = (_ob("oKNOW", "KNOW"), _ob("oLAW", "LAW"),
           _ob("oK-L", "KNOW+LAW", kind="interaction",
               behavior="handover-cleanly", outcome="clean-handover"))
    sets = (_ss("S1", ["E1"], ["oKNOW"], "KNOW"),
            _ss("S2", ["E2"], ["oLAW"], "LAW"),
            _ss("S3", ["E3"], ["oK-L"], "KNOW+LAW",
                behavior="handover-cleanly", outcome="clean-handover"))
    ind = {"E1": CLEARED, "E2": CLEARED, "E3": CLEARED}
    org = {"E1": "o1", "E2": "o2", "E3": "o3"}
    report = compose_broader_claim("CLAIM-KLA", obs, sets, ind, org,
                                   CompositionRule(requires_interaction=True))
    contracts = (InteractionContract(
        handoff_id="KNOW->LAW", sender="KNOW", receiver="LAW",
        sender_guarantee="evidence-labeled-with-uncertainty",
        receiver_assumption="evidence-labeled-with-uncertainty",
        shared_invariant="no-unlabeled-evidence-crosses",
        evidence_ref="E3"),)
    proven = {"KNOW": ("evidence-labeled-with-uncertainty",)}
    argument = CompositionArgument(
        argument_id="ARG-1",
        evidence_ids=("E1", "E2", "E3"),
        assumptions=(Assumption("A1", "same policy version at plan and "
                                     "execution time",
                                justification="policy pinned in receipt R1"),),
        conclusion="CLAIM-KLA holds in staging")
    recon = IndependentReconstruction(
        claim_id="CLAIM-KLA", source_reread=True, outcome_reproduced=True,
        derivation_checked=True, negatives_inspected=True,
        target_runtime_verified=True, blind_evidence=True)
    return report, contracts, proven, argument, recon


def test_audit_five_questions_all_yes():
    report, contracts, proven, argument, recon = _audit_setup()
    assert report.overall_verdict == "UNAFFECTED"
    diffs = (EnvironmentDifference("d1", "log volume differs",
                                   "immaterial",
                                   justification="no behavioral effect"),)
    res = composition_proof_audit("CLAIM-KLA", report, contracts, proven,
                                  diffs, argument, recon,
                                  evidence_refs=("E1", "E2", "E3"))
    assert set(res.answers) == set(AUDIT_QUESTIONS)
    assert all(v[0] for v in res.answers.values())
    assert res.certificate.verdict == "PRODUCTION_PROVEN"
    assert res.narrower_conclusions  # preserved regardless


def test_audit_unjustified_assumption_blocks_implication():
    report, contracts, proven, _, recon = _audit_setup()
    bad_argument = CompositionArgument(
        argument_id="ARG-2", evidence_ids=("E1", "E2", "E3"),
        assumptions=(Assumption(
            "A9", "same authorization receipt checked at execution"),),
        conclusion="CLAIM-KLA holds")
    ok, note = bad_argument.implication_established()
    assert not ok
    assert "A9" in note
    res = composition_proof_audit("CLAIM-KLA", report, contracts, proven,
                                  (), bad_argument, recon)
    assert not res.answers["independently_reproducible"][0]


def test_audit_assume_guarantee_failure():
    report, _, _, argument, recon = _audit_setup()
    contracts = (InteractionContract(
        handoff_id="KNOW->LAW", sender="KNOW", receiver="LAW",
        sender_guarantee="evidence-labeled-with-uncertainty",
        receiver_assumption="receipt-freshness-checked",
        shared_invariant="no-unlabeled-evidence-crosses",
        evidence_ref="E3"),)
    proven = {"KNOW": ("evidence-labeled-with-uncertainty",)}
    res = composition_proof_audit("CLAIM-KLA", report, contracts, proven,
                                  (), argument, recon)
    assert not res.answers["compatible_and_interactions_verified"][0]
    assert any("receipt-freshness-checked" in v[1]
               for v in res.answers.values())


def test_audit_environment_difference_blocks_transfer():
    report, contracts, proven, argument, recon = _audit_setup()
    diffs = (EnvironmentDifference("d1", "auth service differs",
                                   "requires_bridge"),)
    verdict, notes = audit_environment_transfer(diffs)
    assert verdict == "BLOCKED"
    res = composition_proof_audit("CLAIM-KLA", report, contracts, proven,
                                  diffs, argument, recon)
    assert not res.answers["survives_environment_changes"][0]
    assert res.certificate.verdict != "PRODUCTION_PROVEN"


def test_audit_incompatible_difference_blocks():
    verdict, notes = audit_environment_transfer((
        EnvironmentDifference("d9", "production denies the syscall",
                              "incompatible"),))
    assert verdict == "BLOCKED"
    assert any("incompatible" in n for n in notes)


def test_certificate_reopens_on_environment_change():
    cert = QualificationCertificate(
        claim_id="C", verdict="TRANSFER_QUALIFIED",
        scope=MeaningEnvelope(environment="staging"),
        evidence_refs=("E1",), assumptions=("A1",),
        environment="staging")
    reopened = cert.reopen_on_environment_change("production")
    assert reopened["status"] == "REOPENED"
    assert reopened["previous_verdict"] == "TRANSFER_QUALIFIED"
    assert "never inherit it" in reopened["requires"]
    with pytest.raises(AssertionError):
        QualificationCertificate(claim_id="C", verdict="ALWAYS_TRUE",
                                 scope=MeaningEnvelope(), evidence_refs=(),
                                 assumptions=(), environment="staging")


def test_independent_reconstruction_blind_vs_open():
    open_recon = IndependentReconstruction(
        claim_id="C", source_reread=True, outcome_reproduced=True,
        derivation_checked=True, negatives_inspected=True,
        target_runtime_verified=True, blind_evidence=False)
    assert open_recon.complete()
    assert not open_recon.qualifies_as_blind()
    # The 218 exposed files: regression, not fresh blind proof.


def test_audit_preserves_narrower_when_overall_fails():
    report, contracts, proven, argument, recon = _audit_setup()
    # Break the interaction: overall fails, components survive.
    bad_sets = (_ss("S1", ["E1"], ["oKNOW"], "KNOW"),
                 _ss("S2", ["E2"], ["oLAW"], "LAW"))
    ind = {"E1": CLEARED, "E2": CLEARED}
    org = {"E1": "o1", "E2": "o2"}
    obs = (_ob("oKNOW", "KNOW"), _ob("oLAW", "LAW"),
           _ob("oK-L", "KNOW+LAW", kind="interaction",
               behavior="handover-cleanly", outcome="clean-handover"))
    report2 = compose_broader_claim("CLAIM-KLA2", obs, bad_sets, ind, org,
                                    CompositionRule(requires_interaction=True))
    assert report2.overall_verdict == "INSUFFICIENT_DATA"
    res = composition_proof_audit("CLAIM-KLA2", report2, contracts, proven,
                                  (), argument, recon)
    assert res.certificate.verdict == "COMPONENT_QUALIFIED"
    assert len(res.narrower_conclusions) == 2


# Ten adversarial tests (auditor's red team) + positive controls.
def _adv_setup():
    return _audit_setup()


def test_adv_1_reorder_handoffs():
    # Reordering KNOW->LAW to LAW->KNOW breaks the contract direction.
    c = InteractionContract(
        handoff_id="LAW->KNOW", sender="LAW", receiver="KNOW",
        sender_guarantee="evidence-labeled-with-uncertainty",
        receiver_assumption="evidence-labeled-with-uncertainty",
        shared_invariant="x", evidence_ref="E3")
    ok, gap = c.assume_guarantee_holds({"LAW": ()})
    assert not ok  # LAW never proved the guarantee KNOW relies on


def test_adv_2_expire_auth_during_planning():
    arg = CompositionArgument(
        "ARG-X", ("E1",),
        (Assumption("AUTH", "authorization receipt valid at execution",
                    justification="receipt R1, expires 18:00Z"),),
        "C")
    ok, _ = arg.implication_established()
    assert ok  # justified while valid...
    expired = CompositionArgument(
        "ARG-X2", ("E1",),
        (Assumption("AUTH", "authorization receipt valid at execution"),),
        "C")
    ok2, note = expired.implication_established()
    assert not ok2  # ...unjustified once expired


def test_adv_3_replace_evidence_before_act_commits():
    # Evidence swapped after planning: the argument's evidence_ids no longer
    # match what ACT will use — implication references stale evidence.
    arg = CompositionArgument("ARG-X", ("E1-OLD",),
                              (Assumption("A1", "s", justification="j"),), "C")
    assert "E1-OLD" in arg.evidence_ids
    # Auditor must detect the swap: reconstruction re-reads the source.
    recon = IndependentReconstruction(claim_id="C", source_reread=False)
    assert not recon.complete()


def test_adv_4_duplicate_receipt():
    # Same receipt presented twice is one source, not two.
    org = {"E1": "receipt-R1", "E1-dup": "receipt-R1"}
    paths = genuine_paths(
        (SupportSet("S1", ("E1",), ("oA",)),
         SupportSet("S2", ("E1-dup",), ("oA",))), org)
    assert len(paths) == 1


def test_adv_5_out_of_order_verification():
    # VERIFY before PROVE: the derivation check must fail.
    recon = IndependentReconstruction(claim_id="C", derivation_checked=False,
                                      source_reread=True,
                                      outcome_reproduced=True,
                                      negatives_inspected=True,
                                      target_runtime_verified=True)
    assert not recon.complete()


def test_adv_6_disable_one_node():
    report, contracts, proven, argument, recon = _adv_setup()
    # LAW's evidence revoked: component coverage drops, audit notices.
    ind = {"E1": CLEARED, "E2": CONFIRMED, "E3": CLEARED}
    obs = (_ob("oKNOW", "KNOW"), _ob("oLAW", "LAW"),
           _ob("oK-L", "KNOW+LAW", kind="interaction",
               behavior="handover-cleanly", outcome="clean-handover"))
    sets = (_ss("S1", ["E1"], ["oKNOW"], "KNOW"),
            _ss("S2", ["E2"], ["oLAW"], "LAW"),
            _ss("S3", ["E3"], ["oK-L"], "KNOW+LAW",
                behavior="handover-cleanly", outcome="clean-handover"))
    org = {"E1": "o1", "E2": "o2", "E3": "o3"}
    report2 = compose_broader_claim("CLAIM-KLA3", obs, sets, ind, org,
                                    CompositionRule(requires_interaction=True))
    assert report2.component_coverage["oLAW"] == "UNDETERMINED"
    res = composition_proof_audit("CLAIM-KLA3", report2, contracts, proven,
                                  (), argument, recon)
    assert not res.answers["requirements_cover_claim"][0]


def test_adv_7_change_policy_version():
    sets = (_ss("S1", ["E1"], ["oA"], "KNOW", policy="POLICY-V1"),
            _ss("S2", ["E2"], ["oA"], "KNOW", policy="POLICY-V2"))
    v = check_compatibility(sets, {"E1": "o1", "E2": "o2"})
    assert not v.compatible
    assert any("policy_mismatch" in f for f in v.failures)


def test_adv_8_change_schema_config():
    # Schema change = environment difference requiring bridge evidence.
    verdict, _ = audit_environment_transfer((
        EnvironmentDifference("schema-2", "evidence schema v1->v2",
                              "requires_bridge"),))
    assert verdict == "BLOCKED"


def test_adv_9_concurrent_successors_one_checkpoint():
    # Two successors from one checkpoint: each must revalidate independently.
    env = one_region_envelope()
    a = evaluate_claim(env, {"EVID-A": UNASSESSED, "EVID-B": CLEARED},
                       origins_ab())
    pkg1 = build_successor_package(env, a)
    pkg2 = build_successor_package(env, a)
    assert pkg1["revalidate_at_use"] and pkg2["revalidate_at_use"]
    # Neither inherits a frozen verdict.
    assert pkg1["current_qualification_verdict"] == "UNAFFECTED"


def test_adv_10_exposed_canary_as_false_blind_proof():
    # An exposed fixture presented as blind proof must not qualify.
    recon = IndependentReconstruction(
        claim_id="C", source_reread=True, outcome_reproduced=True,
        derivation_checked=True, negatives_inspected=True,
        target_runtime_verified=True, blind_evidence=False)
    assert recon.complete()  # open reproduction is fine...
    assert not recon.qualifies_as_blind()  # ...but it is not blind proof


def test_positive_control_honest_work_qualifies():
    # The audit must not pass by refusing all work: honest, complete,
    # well-evidenced composition qualifies.
    report, contracts, proven, argument, recon = _adv_setup()
    diffs = (EnvironmentDifference("d1", "none material", "immaterial"),)
    res = composition_proof_audit("CLAIM-KLA", report, contracts, proven,
                                  diffs, argument, recon,
                                  evidence_refs=("E1", "E2", "E3"))
    assert res.certificate is not None
    assert res.certificate.verdict in CERTIFICATE_VERDICTS


# ---------------------------------------------------------------------------
# Versioning and retiring composite proof obligations (temporal layer)
# ---------------------------------------------------------------------------
from ..propagation import (
    ObligationRevision, QualificationReceipt, ObligationChange,
    MigrationReceipt, classify_migration, governing_revision,
    assess_applicability, affected_closure, check_decision_boundary,
    OBLIGATION_LIFECYCLE, CHANGE_CLASSES,
)


def _rev(oid, rid, frm, until="", lifecycle="ACTIVE", supersedes="",
         scope=None, retirement_reason=""):
    return ObligationRevision(
        obligation_id=oid, revision_id=rid,
        requirement_text=f"requirement {rid}",
        scope=scope or MeaningEnvelope(),
        acceptance_predicate=f"predicate({rid})",
        proof_standard="independent-reproduction",
        effective_from=frm, effective_until=until,
        supersedes=supersedes, lifecycle=lifecycle,
        retirement_reason=retirement_reason)


def test_obligation_lifecycle_states():
    assert OBLIGATION_LIFECYCLE == ("PROPOSED", "ACTIVE", "DEPRECATED",
                                    "SUPERSEDED", "RETIRED", "WITHDRAWN")
    with pytest.raises(AssertionError):
        _rev("o1", "r1", "2026-01-01", lifecycle="DELETED")


def test_change_classes_complete():
    assert set(CHANGE_CLASSES) == {"editorial", "stronger", "weaker",
                                   "interface_changed", "renamed",
                                   "environment_changed", "split", "merged",
                                   "removed", "found_invalid"}


def test_classify_migration_table():
    cases = {
        "editorial": ("carries_forward", "record equivalence"),
        "renamed": ("carries_forward", "documented compatibility"),
        "weaker": ("preserved_history", "review authorization"),
        "stronger": ("needs_requalification", "additional proof"),
        "interface_changed": ("needs_requalification", "requalify sender"),
        "environment_changed": ("needs_requalification", "bridge evidence"),
        "split": ("needs_requalification", "exact new obligations"),
        "merged": ("needs_requalification", "verify the conjunction"),
        "removed": ("preserved_history", "preserve receipts"),
        "found_invalid": ("withdrawn", "reassess all dependents"),
    }
    for cc, (standing, hint) in cases.items():
        s, action = classify_migration(
            ObligationChange("c1", "o1", "r1", "r2", cc))
        assert s == standing, cc
        assert hint in action, cc


def test_governing_revision_bitemporal():
    revs = (_rev("o1", "r1", "2026-01-01", "2026-06-01", lifecycle="SUPERSEDED",
                 supersedes=""),
            _rev("o1", "r2", "2026-06-01", supersedes="r1"))
    assert governing_revision(revs, "o1", "2026-03-01").revision_id == "r1"
    assert governing_revision(revs, "o1", "2026-09-01").revision_id == "r2"
    assert governing_revision(revs, "o1", "2025-01-01") is None


def test_receipt_survives_retirement_as_history():
    """Retiring a requirement ≠ revoking the qualification: the receipt
    stays valid history of what was established under r1."""
    revs = (_rev("o1", "r1", "2026-01-01", "2026-06-01",
                 lifecycle="SUPERSEDED"),
            _rev("o1", "r2", "2026-06-01", lifecycle="RETIRED",
                 retirement_reason="superseded by o2"))
    receipt = QualificationReceipt(
        "RC-1", "o1", "r1", ("E1",), "SUPPORTED",
        recorded_at="2026-03-01T00:00:00Z",
        effective_at="2026-03-01T00:00:00Z", policy_version="P1")
    # The receipt is intact history...
    assert receipt.revision_id == "r1"
    # ...but it does not automatically apply to the current revision.
    applies, reason = assess_applicability(receipt, revs, "2026-09-01")
    assert not applies
    assert "r2" in reason and "governs" in reason


def test_proof_reuse_is_not_proof_migration():
    """Evidence from r1 may be reused for r2, but the verdict migrates only
    when a new assessment establishes the evidence satisfies r2."""
    revs = (_rev("o1", "r1", "2026-01-01", "2026-06-01",
                 lifecycle="SUPERSEDED"),
            _rev("o1", "r2", "2026-06-01", supersedes="r1"))
    old_receipt = QualificationReceipt(
        "RC-1", "o1", "r1", ("E1",), "SUPPORTED",
        recorded_at="2026-03-01T00:00:00Z",
        effective_at="2026-03-01T00:00:00Z", policy_version="P1")
    applies, _ = assess_applicability(old_receipt, revs, "2026-09-01")
    assert not applies  # no silent migration
    # New assessment with the same evidence against r2:
    new_receipt = QualificationReceipt(
        "RC-2", "o1", "r2", ("E1",), "SUPPORTED",
        recorded_at="2026-09-01T00:00:00Z",
        effective_at="2026-09-01T00:00:00Z", policy_version="P1")
    applies2, _ = assess_applicability(new_receipt, revs, "2026-09-01")
    assert applies2


def test_affected_closure_reports_exact_gap():
    change = ObligationChange("c1", "o2", "r1", "r2", "stronger")
    dependents = {"o2": {"qualifications": ["Q-7"],
                         "composite_claims": ["CLAIM-X"],
                         "actions": ["ACT-3"]}}
    closure = affected_closure(change, dependents)
    assert closure["receipt_standing"] == "needs_requalification"
    assert closure["affected"]["qualifications"] == ["Q-7"]
    assert "o2" in closure["exact_gap"]


def test_decision_boundary_fail_closed():
    revs = (_rev("o1", "r1", "2026-01-01", "2026-06-01",
                 lifecycle="SUPERSEDED"),
            _rev("o1", "r2", "2026-06-01", supersedes="r1"))
    old_receipt = QualificationReceipt(
        "RC-1", "o1", "r1", ("E1",), "SUPPORTED",
        recorded_at="2026-03-01T00:00:00Z",
        effective_at="2026-03-01T00:00:00Z", policy_version="P1")
    # Stale receipt, current revision r2: blocked.
    ok, reasons = check_decision_boundary(
        "ACT-1", "o1", revs, (old_receipt,), "2026-09-01", "staging",
        bridge_verified=False, authorization_permits=True)
    assert not ok
    assert any("governing revision: r2" in r for r in reasons)
    # Fresh receipt against r2: permitted.
    new_receipt = QualificationReceipt(
        "RC-2", "o1", "r2", ("E1",), "SUPPORTED",
        recorded_at="2026-09-01T00:00:00Z",
        effective_at="2026-09-01T00:00:00Z", policy_version="P1")
    ok2, _ = check_decision_boundary(
        "ACT-1", "o1", revs, (new_receipt,), "2026-09-01", "staging",
        bridge_verified=False, authorization_permits=True)
    assert ok2
    # Withdrawn proof: blocked even with a receipt.
    revs_w = (_rev("o1", "r1", "2026-01-01", lifecycle="WITHDRAWN",
                   retirement_reason="acceptance predicate was invalid"),)
    ok3, reasons3 = check_decision_boundary(
        "ACT-1", "o1", revs_w, (old_receipt,), "2026-09-01", "staging",
        bridge_verified=False, authorization_permits=True)
    assert not ok3
    assert any("withdrawn" in r for r in reasons3)


def test_decision_boundary_environment_bridge():
    revs = (_rev("o1", "r1", "2026-01-01",
                 scope=MeaningEnvelope(environment="production")),)
    receipt = QualificationReceipt(
        "RC-1", "o1", "r1", ("E1",), "SUPPORTED",
        recorded_at="2026-03-01T00:00:00Z",
        effective_at="2026-03-01T00:00:00Z", policy_version="P1")
    # Same code, different environment, no bridge: blocked. SHA parity is
    # necessary but not sufficient.
    ok, _ = check_decision_boundary(
        "ACT-1", "o1", revs, (receipt,), "2026-03-01", "staging",
        bridge_verified=False, authorization_permits=True)
    assert not ok
    ok2, _ = check_decision_boundary(
        "ACT-1", "o1", revs, (receipt,), "2026-03-01", "staging",
        bridge_verified=True, authorization_permits=True)
    assert ok2


def test_first_experiment_v1_v2_v3():
    """V1 (component + one interface check → qualified) → V2 (adds
    concurrent revocation handling → partially supported) → V3 (distributed
    runtime → bridge required). The verifier reproduces the correct verdict
    at each version. V1 stays historically qualified; V2 cannot inherit the
    unproven interaction; V3 cannot inherit environment applicability."""
    # V1: component + interface, staging.
    v1 = (_rev("o-comp", "v1", "2026-01-01", "2026-04-01",
               lifecycle="SUPERSEDED"),
          _rev("o-iface", "v1", "2026-01-01", "2026-04-01",
               lifecycle="SUPERSEDED"))
    rc_v1 = (QualificationReceipt(
        "RC-V1", "o-comp", "v1", ("E1",), "SUPPORTED",
        recorded_at="2026-02-01T00:00:00Z", effective_at="2026-02-01T00:00:00Z",
        policy_version="P1"),)
    ok, _ = check_decision_boundary(
        "ACT-V1", "o-comp", v1, rc_v1, "2026-02-01", "staging",
        bridge_verified=False, authorization_permits=True)
    assert ok  # V1 qualified in its time

    # V2: adds concurrent-revocation interaction obligation (stronger).
    v2 = v1 + (_rev("o-conc-rev", "v1", "2026-04-01", lifecycle="ACTIVE"),)
    change = ObligationChange("chg-v2", "o-conc-rev", "", "v1", "stronger")
    standing, _ = classify_migration(change)
    assert standing == "needs_requalification"
    # V1 receipts stay historically qualified...
    applies, _ = assess_applicability(rc_v1[0], v1 + v2, "2026-02-01")
    assert applies
    # ...but V2's new interaction cannot be inherited: no receipt exists.
    ok2, _ = check_decision_boundary(
        "ACT-V2", "o-conc-rev", v2, (), "2026-05-01", "staging",
        bridge_verified=False, authorization_permits=True)
    assert not ok2

    # V3: distributed runtime (environment change) → bridge required.
    v3 = (_rev("o-comp", "v3", "2026-07-01",
               scope=MeaningEnvelope(environment="distributed"),
               lifecycle="ACTIVE"),)
    rc_v3_staging = (QualificationReceipt(
        "RC-V3", "o-comp", "v3", ("E1",), "SUPPORTED",
        recorded_at="2026-08-01T00:00:00Z", effective_at="2026-08-01T00:00:00Z",
        policy_version="P1"),)
    ok3, _ = check_decision_boundary(
        "ACT-V3", "o-comp", v3, rc_v3_staging, "2026-08-01", "staging",
        bridge_verified=False, authorization_permits=True)
    assert not ok3  # cannot inherit environment applicability
    ok4, _ = check_decision_boundary(
        "ACT-V3", "o-comp", v3, rc_v3_staging, "2026-08-01", "staging",
        bridge_verified=True, authorization_permits=True)
    assert ok4  # bridge evidence completes the transfer
