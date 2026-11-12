"""AER-CAL-5 tests (SN-0804): the three-operation separation, four permanent
scope IDs, the four scope decisions, comparability conditions + equivalence
discipline, split criteria, the provisional lifecycle, the no-qualification-
transfer invariant, versioned change records, the M1-M10 suite with the
guard-swap crown jewel, and AER-CAL-005. Every negative test gets a positive
control."""
import pytest

from drift_canary.revocation_linearization import (
    AER_CAL5_IMPLEMENTATION_STATUS,
    SCOPE_OPERATIONS,
    classify_scope_operation,
    pooling_never_certifies,
    ScopedObservation,
    endpoint_ab_example,
    SCOPE_DECISIONS,
    scope_decision,
    COMPARABILITY_CONDITIONS,
    check_comparability,
    equivalence_test,
    ten_k_vs_fifteen,
    SPLIT_TRIGGERS,
    evaluate_split_trigger,
    PROVISIONAL_STATES,
    ProvisionalScope,
    general_contract_may_cover,
    scope_semantically_within,
    use_guarantee,
    make_scope_change_record,
    HierarchicalScopeModel,
    cal5_m_suite,
    cal5_guard_swap_crown_jewel,
    aer_cal_005,
)


def _rev():
    return {"taxonomy": 7, "policy": 7, "incident": 7, "evidence": 7}


def _law():
    return {"receipt": "LAW-1", "valid": True}


def _guarantee_a():
    return {"guarantee_id": "idempotency:A", "kind": "idempotency",
            "verified": True, "qualified_scopes": ("qual:A",),
            "revision": 7, "current": True,
            "statistical_parent_id": "latency-parent-1"}


# --- Honest scope --------------------------------------------------------------------------------

def test_implementation_status_is_test_mechanism_not_production():
    s = AER_CAL5_IMPLEMENTATION_STATUS
    assert s["enters_as"] == "isolated test mechanism"
    assert s["not_a"] == "production authority change"
    assert "implemented merge/split engine" in s["not_verified"]
    assert "live provider baseline registry" in s["not_verified"]
    # Positive control: the aligned contracts are named, not over-claimed.
    assert "propagation.py" in s["contracts_align"]


# --- 1. Three-operation separation ----------------------------------------------------------------

def test_three_operations_have_distinct_requirements():
    kinds = set(SCOPE_OPERATIONS)
    assert kinds == {"STATISTICAL_POOLING", "OPERATIONAL_BASELINE_MERGE",
                     "QUALIFICATION_CONSOLIDATION"}
    reqs = [tuple(SCOPE_OPERATIONS[k]["requires"]) for k in kinds]
    assert len(set(reqs)) == 3  # never confused: distinct evidence gates


def test_unknown_operation_kind_rejected():
    r = classify_scope_operation({"kind": "MERGE_EVERYTHING", "scopes": []})
    assert not r["classified"]


def test_pooling_request_missing_evidence_not_authorized():
    r = classify_scope_operation({"kind": "STATISTICAL_POOLING",
                                  "scopes": ["a", "b"], "evidence": {}})
    assert r["classified"] and not r["authorized"]
    assert r["missing_evidence"]  # positive control below supplies it


def test_pooling_request_with_evidence_authorized():
    r = classify_scope_operation(
        {"kind": "STATISTICAL_POOLING", "scopes": ["a", "b"],
         "evidence": {"verified_comparability": True,
                      "calibrated_uncertainty": True,
                      "independence_assumptions_stated": True}})
    assert r["authorized"] and not r["missing_evidence"]


def test_consolidation_needs_union_evidence():
    bad = classify_scope_operation(
        {"kind": "QUALIFICATION_CONSOLIDATION", "scopes": ["a", "b"],
         "evidence": {"proof_guarantee_covers_every_member": True,
                      "relevant_cross_scope_interactions_tested": False}})
    assert not bad["authorized"]
    good = classify_scope_operation(
        {"kind": "QUALIFICATION_CONSOLIDATION", "scopes": ["a", "b"],
         "evidence": {"proof_guarantee_covers_every_member": True,
                      "relevant_cross_scope_interactions_tested": True}})
    assert good["authorized"]


def test_pooling_never_certifies_group():
    m = HierarchicalScopeModel(min_n_qualified=100)
    m.observe("s:A", 5000, 50)
    m.observe("s:B", 15, 0)
    r = pooling_never_certifies(["s:A", "s:B"], m)
    assert r["law_holds"]
    assert r["per_scope"]["s:B"]["qualification"] == "UNPROVEN_IN_SCOPE"
    assert r["per_scope"]["s:B"]["pooled_estimate"] > 0  # prediction kept


# --- 2. Four permanent scope IDs ------------------------------------------------------------------

def test_four_ids_survive_sharing():
    ex = endpoint_ab_example()
    assert ex["shared_statistical_parent"]
    assert ex["distinct_qualification_scopes"]
    assert ex["law_holds"]  # shared learning, no shared guarantee


def test_scoped_observation_keeps_original_taxonomy():
    o = ScopedObservation("p1", "q:A", "obs:A", "inter:A", 10, 1, "tax-v3")
    assert o.provenance()["taxonomy_version"] == "tax-v3"
    assert o.provenance()["observation_scope_id"] == "obs:A"


# --- 3. Four scope decisions ------------------------------------------------------------------------

def test_four_decisions_known():
    assert set(SCOPE_DECISIONS) == {"POOL_ESTIMATES", "MERGE_OPERATIONAL_MODEL",
                                   "SPLIT_MODEL", "CREATE_PROVISIONAL_SCOPE"}


def test_unknown_decision_rejected():
    assert not scope_decision("MERGE_QUALIFICATIONS", {})["taken"]


def test_pool_estimates_keeps_qualifications_separate():
    r = scope_decision("POOL_ESTIMATES",
                       {"comparable": True, "contamination": False})
    assert r["taken"] and r["effects"]["qualifications_stay_separate"]
    # Negative control: contamination blocks pooling.
    r2 = scope_decision("POOL_ESTIMATES",
                        {"comparable": True, "contamination": True})
    assert not r2["taken"]


def test_merge_operational_model_needs_heldout():
    r = scope_decision("MERGE_OPERATIONAL_MODEL",
                       {"held_out_preserves_detection_all_scopes": True})
    assert r["taken"] and r["effects"]["contract_gates_kept"]
    assert not scope_decision(
        "MERGE_OPERATIONAL_MODEL", {})["taken"]


def test_split_model_needs_established_difference():
    r = scope_decision("SPLIT_MODEL",
                       {"material_difference_established": True})
    assert r["taken"] and r["effects"]["dependent_claims_reassessed"]
    assert not scope_decision("SPLIT_MODEL", {})["taken"]


def test_provisional_scope_no_inherited_pass():
    r = scope_decision("CREATE_PROVISIONAL_SCOPE", {})
    assert r["taken"] and r["provisional"]
    assert not r["effects"]["inherited_pass"]
    assert r["effects"]["independent_qualification_required"]
    # Positive control: an explicitly valid contract can cover.
    r2 = scope_decision("CREATE_PROVISIONAL_SCOPE",
                        {"explicit_valid_contract_covers": True})
    assert not r2["provisional"] and r2["effects"]["inherited_pass"]


# --- 4. Comparability + equivalence -------------------------------------------------------------------

def test_four_comparability_conditions():
    assert set(COMPARABILITY_CONDITIONS) == {
        "semantic_compatibility", "statistical_compatibility",
        "risk_compatibility", "evidence_integrity"}


def test_comparability_requires_all_four():
    ev = {"semantic_compatible": True,
          "held_out_scope_specific_calibrated": True,
          "each_member_detection_preserved": True,
          "admissible_labeled": True,
          "unresolved_contamination": False}
    assert check_comparability({}, {}, ev)["comparable"]
    for drop in ("semantic_compatible", "held_out_scope_specific_calibrated",
                 "each_member_detection_preserved", "admissible_labeled"):
        ev2 = dict(ev)
        ev2[drop] = False
        assert not check_comparability({}, {}, ev2)["comparable"], drop
    ev3 = dict(ev)
    ev3["unresolved_contamination"] = True
    assert not check_comparability({}, {}, ev3)["comparable"]


def test_ten_k_vs_fifteen_is_not_equivalence():
    r = ten_k_vs_fifteen()
    assert r["result"]["verdict"] == "UNPROVEN"
    assert not r["pooling_permitted"]


def test_equivalence_positive_control():
    # 10k vs 10k at ~1%: the 95% difference interval fits a 1pp margin.
    r = equivalence_test(10000, 100, 10000, 105, margin=0.01)
    assert r["verdict"] == "EQUIVALENT"
    lo, hi = r["difference_interval"]
    assert lo >= -0.01 and hi <= 0.01


def test_equivalence_tight_margin_blocks():
    r = equivalence_test(10000, 100, 10000, 105, margin=0.001)
    assert r["verdict"] == "UNPROVEN"  # the margin is pre-specified, not tuned


# --- 5. Split criteria ----------------------------------------------------------------------------------

def test_split_trigger_table_shape():
    assert set(SPLIT_TRIGGERS) == {
        "idempotency_scope_change", "verified_duplicates", "regime_divergence",
        "repeated_calibration_failures", "isolated_sparse_residual",
        "shared_guarantee_differing_latency"}


def test_idempotency_change_separates_immediately():
    r = evaluate_split_trigger("idempotency_scope_change", {})
    assert r["split"] is True and r["action"] == "SEPARATE_IMMEDIATELY"


def test_verified_duplicates_contain_and_reassess():
    r = evaluate_split_trigger("verified_duplicates",
                               {"duplicates_verified": True})
    assert r["action"] == "CONTAIN_AND_REASSESS"
    assert not evaluate_split_trigger(
        "verified_duplicates", {})["split"]  # unverified claim: no split


def test_sparse_residual_never_auto_splits():
    r = evaluate_split_trigger("isolated_sparse_residual", {})
    assert r["split"] is False
    assert r["action"] == "INVESTIGATE_DO_NOT_AUTO_SPLIT"


def test_shared_guarantee_latency_splits_modeling_only():
    r = evaluate_split_trigger("shared_guarantee_differing_latency", {})
    assert r["split"] == "latency_modeling_only"
    # The valid guarantee is not fragmented.
    assert "never fragment" in r["note"]


def test_regime_divergence_needs_independent_evidence():
    assert evaluate_split_trigger(
        "regime_divergence",
        {"divergence_independently_established": True})["split"]
    assert not evaluate_split_trigger("regime_divergence", {})["split"]


def test_unknown_trigger():
    r = evaluate_split_trigger("nope", {})
    assert r["action"] == "UNKNOWN_TRIGGER" and not r["split"]


# --- 6. Provisional lifecycle ----------------------------------------------------------------------------

def test_provisional_states_known():
    assert PROVISIONAL_STATES == ("NEW_SCOPE", "PROVISIONAL_MODEL",
                                 "INDEPENDENT_QUALIFICATION",
                                 "QUALIFIED_IN_SCOPE")


def test_provisional_lifecycle_full_walk():
    c = ProvisionalScope("ep:C")
    assert c.state == "NEW_SCOPE"
    # Borrowed estimates require stated uncertainty.
    assert not c.to_provisional_model("p", uncertainty_noted=False)["advanced"]
    assert c.to_provisional_model("p", uncertainty_noted=True)["advanced"]
    # All four checks required.
    assert not c.to_independent_qualification(
        {"contract_applicability": True})["advanced"]
    assert c.to_independent_qualification(
        {"contract_applicability": True, "failure_cases": True,
         "interactions": True, "outcomes": True})["advanced"]
    # Wrong-order: cannot qualify straight from provisional model.
    c2 = ProvisionalScope("ep:D")
    c2.to_provisional_model("p", uncertainty_noted=True)
    assert not c2.to_qualified("x")["advanced"]
    assert c.to_qualified("verifier-7")["advanced"]
    assert c.state == "QUALIFIED_IN_SCOPE"
    assert [s for s, _ in c.history] == list(PROVISIONAL_STATES)


def test_general_contract_covers_when_all_verified():
    contract = {"covers": {
        "concurrency": {"verified": True, "scope": "low"},
        "key_identity": {"verified": True, "scope": "stable"},
        "region": {"verified": True, "scope": "r1"},
        "retention": {"verified": True, "scope": "30d"},
        "downstream_effects": {"verified": True, "scope": "ledger-only"}}}
    scope = {"concurrency": "low", "key_identity": "stable", "region": "r1",
             "retention": "30d", "downstream_effects": "ledger-only"}
    r = general_contract_may_cover(scope, contract)
    assert r["covered"] and not r["blocked_by"]


def test_general_contract_blocked_by_one_missing():
    contract = {"covers": {
        "concurrency": {"verified": True, "scope": "low"},
        "key_identity": {"verified": True, "scope": "stable"},
        "region": {"verified": True, "scope": "r1"},
        "retention": {"verified": False},
        "downstream_effects": {"verified": True, "scope": "ledger-only"}}}
    scope = {"concurrency": "low", "key_identity": "stable", "region": "r1",
             "retention": "30d", "downstream_effects": "ledger-only"}
    r = general_contract_may_cover(scope, contract)
    assert not r["covered"] and "retention" in r["blocked_by"]


def test_general_contract_blocked_by_scope_mismatch():
    contract = {"covers": {
        "concurrency": {"verified": True, "scope": "low"},
        "key_identity": {"verified": True, "scope": "stable"},
        "region": {"verified": True, "scope": "r2"},
        "retention": {"verified": True, "scope": "30d"},
        "downstream_effects": {"verified": True, "scope": "ledger-only"}}}
    scope = {"concurrency": "low", "key_identity": "stable", "region": "r1",
             "retention": "30d", "downstream_effects": "ledger-only"}
    r = general_contract_may_cover(scope, contract)
    assert not r["covered"] and any("region" in b for b in r["blocked_by"])


# --- 7. No-qualification-transfer invariant ------------------------------------------------------------------

def test_semantic_inclusion_not_label_hierarchy():
    assert scope_semantically_within("qual:A", "qual:A")
    assert not scope_semantically_within("qual:B", "qual:A")
    assert not scope_semantically_within("qual:A", "all-endpoints")


def test_use_guarantee_authorized_path():
    g = _guarantee_a()
    g["qualified_scopes"] = ("qual:B",)
    r = use_guarantee(g, "qual:B", _rev(), _law())
    assert r["authorized"] and not r["reasons"]


def test_use_guarantee_denied_outside_scope():
    r = use_guarantee(_guarantee_a(), "qual:B", _rev(), _law())
    assert not r["authorized"]
    assert any("qualified scope" in x for x in r["reasons"])


def test_use_guarantee_denied_unverified():
    g = _guarantee_a()
    g["verified"] = False
    assert not use_guarantee(g, "qual:A", _rev(), _law())["authorized"]


def test_use_guarantee_denied_stale_revision():
    g = _guarantee_a()
    rev = _rev()
    rev["policy"] = 8  # guarantee at revision 7, policy moved on
    r = use_guarantee(g, "qual:A", rev, _law())
    assert not r["authorized"] and any("current" in x for x in r["reasons"])


def test_use_guarantee_denied_no_law_receipt():
    r = use_guarantee(_guarantee_a(), "qual:A", _rev(), None)
    assert not r["authorized"] and any("LAW" in x for x in r["reasons"])


# --- 8. Change records --------------------------------------------------------------------------------------------

def _checks(**over):
    base = {"taxonomy": {"current": True}, "incident": {"current": True},
            "evidence": {"current": True}, "policy": {"current": True},
            "promotion_pending": False}
    base.update(over)
    return base


def test_change_record_split_needs_mapping():
    r = make_scope_change_record("SC-1", "SPLIT", "tax-v3", "tax-v4", {},
                                 [], [], _checks())
    assert not r["recorded"]


def test_change_record_split_ok():
    r = make_scope_change_record(
        "SC-1", "SPLIT", "tax-v3", "tax-v4",
        {"hist:A": ["child:A1", "child:A2"]},
        [{"record": "r-9", "auto_allocated": False}],
        ["idempotency:A"], _checks())
    assert r["recorded"] and r["schema"] == "SCOPE-CHANGE-014"
    assert r["past_observations_rewritten"] is False


def test_ambiguous_records_never_silently_allocated():
    r = make_scope_change_record(
        "SC-2", "SPLIT", "tax-v3", "tax-v4", {"hist:A": ["child:A1"]},
        [{"record": "r-9", "auto_allocated": True}], [], _checks())
    assert not r["recorded"] and "silently allocated" in r["reason"]


def test_change_record_races_withdrawal_blocked():
    r = make_scope_change_record(
        "SC-3", "MERGE", "tax-v3", "tax-v4", {}, [], [],
        _checks(incident={"current": True, "withdrawal_pending": True}))
    assert not r["recorded"] and "withdrawal" in r["reason"]


def test_change_record_races_promotion_blocked():
    r = make_scope_change_record(
        "SC-4", "MERGE", "tax-v3", "tax-v4", {}, [], [],
        _checks(promotion_pending=True))
    assert not r["recorded"] and "promotion" in r["reason"]


def test_change_record_stale_revision_blocked():
    r = make_scope_change_record(
        "SC-5", "MERGE", "tax-v3", "tax-v4", {}, [], [],
        _checks(evidence={"current": False}))
    assert not r["recorded"] and "evidence" in r["reason"]


# --- 9. M1–M10 + guard-swap crown jewel -------------------------------------------------------------------------------

def test_m_suite_guard_intact_all_hold():
    results = cal5_m_suite(guard_intact=True)
    assert [i for i, _, _ in results] == [f"M{i}" for i in range(1, 11)]
    bad = [(i, v, n) for i, v, n in results if v not in ("HOLD",)]
    assert not bad, bad


def test_m_suite_guard_swapped_yields_counterexample():
    results = cal5_m_suite(guard_intact=False)
    m10 = next((v, n) for i, v, n in results if i == "M10")
    assert m10[0] == "COUNTEREXAMPLE", m10
    # Only M10 flips: the theft is the single guard-controlled behavior.
    intact = dict((i, v) for i, v, _ in cal5_m_suite(guard_intact=True))
    swapped = dict((i, v) for i, v, _ in results)
    flipped = [i for i in intact if intact[i] != swapped[i]]
    assert flipped == ["M10"], flipped


def test_guard_swap_crown_jewel():
    j = cal5_guard_swap_crown_jewel()
    assert j["guard_intact_M10"] == "HOLD"
    assert j["guard_swapped_M10"] == "COUNTEREXAMPLE"
    assert "acquired A's guarantee" in j["minimal_counterexample"]
    assert "theft stays blocked" in j["restoration"]


# --- 10. AER-CAL-005 ----------------------------------------------------------------------------------------------------

def test_aer_cal_005():
    r = aer_cal_005()
    p = r["pooling"]
    assert p["comparable"] and p["pool_authorized"]
    assert p["b_qualification"] == "UNPROVEN_IN_SCOPE"
    assert not p["b_guarantee_authorized"]
    assert r["provisional_C"]["final"] == "QUALIFIED_IN_SCOPE"
    assert r["general_contract"]["all_verified_covers"]
    assert r["general_contract"]["one_missing_blocks"]
    reg = r["regression_in_B"]
    assert reg["detected_on_cell_evidence"]
    assert reg["a_cell_unaffected"]
    assert r["guard_removed"]["theft_authorized"]
    assert r["guard_restored"]["theft_blocked"]
    # Restoration keeps the legitimate learning: B's pooled prediction survives.
    assert r["guard_restored"]["b_pooled_estimate_kept"] > 0
