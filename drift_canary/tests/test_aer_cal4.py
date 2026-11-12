"""AER-CAL-4 tests (SN-0801): scope keys, Simpson's paradox, hierarchical
pooling with the restriction, three views, versioned taxonomies,
cross-scope interactions, scope-specific thresholds, the promotion
invariant, BL-042, the P1-P10 suite, the guard-removal crown jewel, and
AER-CAL-004."""
import pytest

from drift_canary.revocation_linearization import (
    ScopeKey,
    scope_key_material,
    aggregate_hides_regression,
    simpson_two_regime,
    HierarchicalScopeModel,
    three_views,
    CONCURRENCY_REGIMES,
    TaxonomyVersion,
    classify_concurrency,
    migrate_taxonomy,
    InteractionScope,
    interaction_covered,
    scope_threshold_advice,
    promote_scope,
    ScopeQualificationManifest,
    bl042_pending,
    cal4_p_suite,
    cal4_guard_removal_crown_jewel,
    aer_cal_004,
    PROMOTION_OBLIGATIONS,
)


def _scope(**kw):
    base = dict(provider="p1", endpoint="charge", region="east",
                concurrency_regime="low", workload_class="standard")
    base.update(kw)
    return ScopeKey(**base)


def test_scope_key_canonical():
    s = _scope()
    assert scope_key_material(s) == s
    assert s.concurrency_regime == "low" and s.workload_class == "standard"


def test_simpson_paradox_standing_test():
    before, after = simpson_two_regime()
    paradox, detail = aggregate_hides_regression(before, after)
    assert paradox
    assert detail["cell_directions"] == {"low": "worse", "high": "worse"}
    assert detail["aggregate"] == "better"
    assert detail["aggregate_before"] == 0.046
    assert detail["aggregate_after"] == 0.026
    # No paradox when the aggregate agrees with the cells.
    p2, d2 = aggregate_hides_regression(
        {"a": (1000, 10)}, {"a": (1000, 20)})
    assert not p2 and d2["aggregate"] == "worse"


def test_hierarchical_pooling_restriction():
    m = HierarchicalScopeModel(min_n_qualified=100)
    m.observe(_scope(region="east"), 5000, 50)
    sparse = _scope(region="west")
    m.observe(sparse, 20, 1)
    est, n = m.cell_posterior(sparse)
    assert 0 < est < 0.1  # pooled estimate borrows strength
    # ...but certification stays with the cell's own evidence.
    assert m.cell_qualification(sparse) == "UNPROVEN_IN_SCOPE"
    assert m.cell_qualification(_scope(region="east")) == "QUALIFIED"


def test_ineligible_training_data_rejected():
    m = HierarchicalScopeModel()
    r = m.observe(_scope(), 5000, 50, training_state="CONFIRMED_REGRESSION")
    assert not r["accepted"]
    r2 = m.observe(_scope(), 5000, 50, training_state="UNRESOLVED_ANOMALY")
    assert not r2["accepted"]


def test_quarantine_recomputes_parent_and_flags_dependents():
    m = HierarchicalScopeModel()
    a, b = _scope(region="east"), _scope(region="west")
    m.observe(a, 5000, 50)
    m.observe(b, 5000, 500)
    pa_before = m.parent_a
    q = m.quarantine(b, "contamination")
    assert b in m.quarantined
    assert m.parent_a < pa_before  # the bad cell's mass left the parent
    assert a in q["dependents_flagged"]
    assert m.cell_qualification(b) == "QUARANTINED"
    r = m.observe(b, 100, 1)
    assert not r["accepted"] and "quarantined" in r["reason"]


def test_three_views():
    views = three_views({"low": (9000, 180), "high": (1000, 80)},
                        {"low": 0.1, "high": 0.9})
    assert views["individual"] == {"low": 0.02, "high": 0.08}
    assert views["standardized"] == 0.074  # 0.1*2% + 0.9*8%
    assert views["observed"] == 0.026
    assert "overrides a local regression" in views["note"]


def test_concurrency_taxonomy_at_admission():
    assert classify_concurrency(5) == "low"
    assert classify_concurrency(50) == "medium"
    assert classify_concurrency(500) == "high"
    old = TaxonomyVersion(1, tuple((n, lo, hi) for n, lo, hi in CONCURRENCY_REGIMES),
                          ("standard",), None)
    mig = migrate_taxonomy(old, old.regimes, ("standard", "bulk"))
    assert mig["new_taxonomy"].version == 2
    assert mig["new_taxonomy"].supersedes == 1
    assert "no silent remapping" in mig["note"]


def test_interaction_scope_healthy_cells_broken_boundary():
    e, w = _scope(region="east"), _scope(region="west")
    covered, note = interaction_covered(InteractionScope(e, w, "failover"), {})
    assert not covered
    assert "broken boundary" in note
    covered2, _ = interaction_covered(
        InteractionScope(e, w, "failover"), {("east", "west", "failover"): True})
    assert covered2


def test_scope_threshold_advice():
    assert scope_threshold_advice(5000, False)["action"] == "conditional_threshold"
    assert scope_threshold_advice(20, False)["action"] == "hierarchical_and_canary"
    assert scope_threshold_advice(5000, True)["action"] == "shared_incident"
    d = scope_threshold_advice(5000, False, verified_duplicates=2)
    assert d["action"] == "withdraw" and "irrelevant" in d["note"]
    u = scope_threshold_advice(0, False, seen_before=False)
    assert u["action"] == "unqualified"


def test_promotion_invariant():
    m = HierarchicalScopeModel()
    sa, sb = _scope(region="east"), _scope(region="west")
    m.observe(sa, 5000, 50)
    m.observe(sb, 5000, 250)
    r = promote_scope(sa, (("ctx", 0.005, 0.02),), m, (sa, sb),
                      {ob: True for ob in PROMOTION_OBLIGATIONS})
    assert r["promoted"]
    assert sb in r["neighbor_effects_measured"]
    assert "RecheckSharedDependencies" in r["invariant"]
    r2 = promote_scope(sa, (("ctx", 0.005, 0.02),), m, (sa, sb),
                       {ob: True for ob in PROMOTION_OBLIGATIONS
                        if ob != "safety_preservation"})
    assert not r2["promoted"]


def test_bl042_pending_intentional():
    m = bl042_pending(_scope())
    assert m.manifest_id.startswith("BL-042/")
    assert m.status == "PENDING"
    assert isinstance(m, ScopeQualificationManifest)


def test_p_suite_all_ten():
    results = cal4_p_suite()
    assert len(results) == 10
    expected = {
        "P1": "WEST_FLAGGED", "P2": "PARADOX_DETECTED",
        "P3": "UNPROVEN_IN_SCOPE", "P4": "DISTINGUISHED",
        "P5": "INTERACTION_UNPROVEN", "P6": "QUARANTINED",
        "P7": "MIGRATION_REQUIRED", "P8": "UNPROVEN_IN_SCOPE",
        "P9": "NEIGHBORS_RECHECKED", "P10": "LOCALIZED",
    }
    for pid, verdict, _ev in results:
        assert verdict == expected[pid], (pid, verdict)


def test_guard_removal_crown_jewel():
    r = cal4_guard_removal_crown_jewel()
    ce = r["counterexample"]
    assert ce["aggregate_says"] == "IMPROVED"
    assert ce["cells_say"] == {"low": "worse", "high": "worse"}
    assert all(v == "QUALIFIED" for v in r["restored"].values())


def test_aer_cal_004():
    r = aer_cal_004()
    d = r["designs"]
    assert d["D1_aggregate_only"] == "no regression"
    assert d["D2_D3_both_regime_detection"] == ["high", "low"]
    assert d["D3_sparse_cell"] == "UNPROVEN_IN_SCOPE"
    assert d["D4_defect_certifies_sparse"] is True  # the defect, documented
    assert r["cross_region_duplicates"]["covered"] is False
    assert r["scoped_promotion"]["neighbors_rechecked"] == 7
    assert r["contamination"]["quarantined"]
    assert r["contamination"]["dependents_reassessed"] == 7
    assert r["guard_removal_crown_jewel"]["aggregate_says"] == "IMPROVED"
