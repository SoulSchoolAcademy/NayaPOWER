"""D32 tests: the evidence-addition path.

Positive controls: valid additions strengthen/resolve exactly the
affected claims; independent alternatives survive; mentioners are
untouched; the cascade detects promotion at every stage.

Negative controls: repetition changes nothing; promotion is rejected;
derived claims cannot exceed their premises; mention edges transmit
nothing; an unresolved hypothesis never becomes a fact by projection.
"""

from drift_canary.d32_evidence_addition import (
    NewEvidence, ClaimNode,
    ANCHORING, CORROBORATING, REPEATING, PROMOTING, INADMISSIBLE,
    KIND_OBSERVATION, KIND_SUMMARY, KIND_COPY,
    VERDICT_RANK,
    classify_addition, detect_promotion,
    material_downstream_closure, recompute_on_addition,
    build_d32_addition_fixture, run_d32_decisive_addition,
    run_false_certainty_cascade,
)
from drift_canary.uncertainty_propagation import (
    MOD_POSSIBLE, MOD_OBSERVED, MOD_VERIFIED,
)


def _hints(*ids_origins):
    return {eid: (origin, "none") for eid, origin in ids_origins}


# ---------------------------------------------------------------------------
# Addition classification
# ---------------------------------------------------------------------------

def test_fresh_independent_observation_is_anchoring():
    new = NewEvidence("E9", "telemetry_B", KIND_OBSERVATION, "p_new",
                      frozenset({"r1"}), MOD_OBSERVED, (), True, "",
                      "SUPPORTED")
    cls, _ = classify_addition(new, (), _hints())
    assert cls == ANCHORING


def test_independent_second_source_same_proposition_is_corroborating():
    old = NewEvidence("E1", "sensor_A", KIND_OBSERVATION, "p",
                      frozenset({"r1"}), MOD_OBSERVED, (), True, "",
                      "SUPPORTED")
    new = NewEvidence("E2", "sensor_B", KIND_OBSERVATION, "p",
                      frozenset({"r1"}), MOD_OBSERVED, (), True, "",
                      "SUPPORTED")
    cls, _ = classify_addition(new, (old,),
                               _hints(("E1", "sensor_A"), ("E2", "sensor_B")))
    assert cls == CORROBORATING


def test_summary_of_existing_evidence_is_repeating():
    old = NewEvidence("E1", "sensor_A", KIND_OBSERVATION, "p",
                      frozenset({"r1"}), MOD_OBSERVED, (), True, "",
                      "SUPPORTED")
    new = NewEvidence("E1s", "analyst", KIND_SUMMARY, "p",
                      frozenset({"r1"}), MOD_OBSERVED, ("E1",), True, "",
                      "SUPPORTED")
    cls, reasons = classify_addition(
        new, (old,),
        _hints(("E1", "sensor_A"), ("E1s", "analyst")))
    assert cls == REPEATING, reasons


def test_same_origin_rewitnessed_nothing_is_repeating():
    old = NewEvidence("E1", "sensor_A", KIND_OBSERVATION, "p",
                      frozenset({"r1"}), MOD_OBSERVED, (), True, "",
                      "SUPPORTED")
    new = NewEvidence("E1b", "sensor_A", KIND_COPY, "p",
                      frozenset({"r1"}), MOD_OBSERVED, (), True, "",
                      "SUPPORTED")
    cls, _ = classify_addition(new, (old,),
                               _hints(("E1", "sensor_A"), ("E1b", "sensor_A")))
    assert cls == REPEATING


def test_summary_claiming_verified_is_promoting():
    old = NewEvidence("E1", "sensor_A", KIND_OBSERVATION, "p",
                      frozenset({"r1"}), MOD_OBSERVED, (), True, "",
                      "SUPPORTED")
    new = NewEvidence("E1v", "analyst", KIND_SUMMARY, "p",
                      frozenset({"r1"}), MOD_OBSERVED, ("E1",), True, "",
                      "SUPPORTED", MOD_VERIFIED)
    cls, reasons = classify_addition(
        new, (old,),
        _hints(("E1", "sensor_A"), ("E1v", "analyst")))
    assert cls == PROMOTING, reasons
    assert any("modality_promotion" in r for r in reasons)


def test_widened_summary_is_promoting_not_strengthening():
    old = NewEvidence("E1", "sensor_A", KIND_OBSERVATION, "p",
                      frozenset({"r1"}), MOD_OBSERVED, (), True, "",
                      "SUPPORTED")
    wide = NewEvidence("E1w", "analyst", KIND_SUMMARY, "p",
                       frozenset({"r1", "r2", "r3"}), MOD_OBSERVED,
                       ("E1",), True, "", "SUPPORTED")
    cls, reasons = classify_addition(
        wide, (old,),
        _hints(("E1", "sensor_A"), ("E1w", "analyst")))
    # Broader than its ancestors witnessed: promotion, and therefore
    # never admitted as strengthening evidence.
    assert cls == PROMOTING, reasons
    assert any("scope_promotion" in r for r in reasons)


def test_inadmissible_evidence_rejected_first():
    new = NewEvidence("Ex", "unknown", KIND_OBSERVATION, "p",
                      frozenset({"r1"}), MOD_OBSERVED, (), False,
                      "no_provenance")
    cls, reasons = classify_addition(new, (), _hints())
    assert cls == INADMISSIBLE
    assert any("no_provenance" in r for r in reasons)


# ---------------------------------------------------------------------------
# Promotion detection
# ---------------------------------------------------------------------------

def test_verdict_promotion_detected():
    detected, reasons = detect_promotion(
        "SUPPORTED", MOD_POSSIBLE, frozenset({"r1"}),
        "UNDETERMINED", MOD_POSSIBLE, frozenset({"r1"}),
        "stage")
    assert detected
    assert any("verdict_promotion" in r for r in reasons)


def test_modality_promotion_detected():
    detected, reasons = detect_promotion(
        "UNDETERMINED", MOD_VERIFIED, frozenset({"r1"}),
        "UNDETERMINED", MOD_POSSIBLE, frozenset({"r1"}),
        "stage")
    assert detected
    assert any("modality_promotion" in r for r in reasons)


def test_scope_promotion_detected():
    detected, reasons = detect_promotion(
        "UNDETERMINED", MOD_POSSIBLE, frozenset({"all"}),
        "UNDETERMINED", MOD_POSSIBLE, frozenset({"r1"}),
        "stage")
    assert detected
    assert any("scope_promotion" in r for r in reasons)


def test_faithful_projection_not_flagged():
    detected, _ = detect_promotion(
        "UNDETERMINED", MOD_POSSIBLE, frozenset({"r1"}),
        "UNDETERMINED", MOD_POSSIBLE, frozenset({"r1"}),
        "stage")
    assert not detected


def test_narrowing_is_not_promotion():
    detected, _ = detect_promotion(
        "SUPPORTED", MOD_OBSERVED, frozenset({"r1"}),
        "SUPPORTED", MOD_OBSERVED, frozenset({"r1", "r2"}),
        "stage")
    assert not detected


# ---------------------------------------------------------------------------
# Closure and recomputation
# ---------------------------------------------------------------------------

def _mini_graph():
    # c1 requires E1 (material); c2 mentions E1; c3 derives from c1.
    graph = {
        "c1": (("E1", "REQUIRES_SUPPORT_FROM"),),
        "c2": (("E1", "MENTIONS"),),
        "c3": (("c1", "DERIVED_FROM"),),
    }
    claims = {
        "c1": ClaimNode("c1", (("E1", "REQUIRES_SUPPORT_FROM"),),
                        "AND", "UNDETERMINED"),
        "c2": ClaimNode("c2", (("E1", "MENTIONS"),),
                        "AND", "SUPPORTED"),
        "c3": ClaimNode("c3", (("c1", "DERIVED_FROM"),),
                        "AND", "UNDETERMINED"),
    }
    return graph, claims


def _ev(eid, origin="sensor_A"):
    return NewEvidence(eid, origin, KIND_OBSERVATION, "p1",
                       frozenset({"r1"}), MOD_OBSERVED, (), True, "",
                       "SUPPORTED")


def test_closure_excludes_mentions():
    graph, _ = _mini_graph()
    closure = material_downstream_closure(("E1",), graph)
    assert "c1" in closure
    assert "c3" in closure          # transitive through material edges
    assert "c2" not in closure      # MENTIONS is citation, not dependence


def test_recompute_only_affected_claims():
    graph, claims = _mini_graph()
    out = recompute_on_addition(
        graph, claims, {}, {"E1": "SUPPORTED"}, ((_ev("E1"), ANCHORING),))
    assert out["c2"][0] == "UNAFFECTED"
    assert out["c1"][0] in ("STRENGTHENED", "RESOLVED")
    assert out["c3"][0] != "UNAFFECTED"  # downstream of c1 recomputes


def test_repeating_addition_changes_nothing():
    graph, claims = _mini_graph()
    rep = NewEvidence("E1r", "analyst", KIND_SUMMARY, "p1",
                      frozenset({"r1"}), MOD_OBSERVED, ("E1",), True, "",
                      "SUPPORTED")
    out = recompute_on_addition(
        graph, claims, {"E1": "SUPPORTED"}, {"E1": "SUPPORTED"},
        ((rep, REPEATING),))
    assert all(action == "UNAFFECTED" for action, _ in out.values())


def test_promoting_addition_rejected_not_applied():
    graph = {"c": (("Ep", "DERIVED_FROM"),)}
    claims = {"c": ClaimNode("c", graph["c"], "AND", "UNDETERMINED")}
    prom = NewEvidence("Ep", "analyst", KIND_SUMMARY, "p",
                       frozenset({"r"}), MOD_OBSERVED, (), True, "",
                       "SUPPORTED", MOD_VERIFIED)
    out = recompute_on_addition(
        graph, claims, {}, {"Ep": "SUPPORTED"}, ((prom, PROMOTING),))
    assert out["c"][0] == "PROMOTION_REJECTED"


def test_and_bounded_by_weakest_premise():
    graph = {"c": (("E1", "REQUIRES_SUPPORT_FROM"),
                   ("E2", "REQUIRES_SUPPORT_FROM"))}
    claims = {"c": ClaimNode("c", graph["c"], "AND", "UNDETERMINED")}
    out = recompute_on_addition(
        graph, claims, {"E2": "UNDETERMINED"},
        {"E1": "SUPPORTED", "E2": "UNDETERMINED"},
        ((_ev("E1"), ANCHORING),))
    # E2 still UNDETERMINED: the conjunction cannot qualify.
    assert out["c"][0] == "RECOMPUTED_UNCHANGED"
    assert "UNDETERMINED" in out["c"][1]


def test_or_qualifies_through_one_sufficient_path():
    graph = {"c": (("E1", "INDEPENDENTLY_CORROBORATED_BY"),
                   ("E2", "INDEPENDENTLY_CORROBORATED_BY"))}
    claims = {"c": ClaimNode("c", graph["c"], "OR", "UNDETERMINED")}
    out = recompute_on_addition(
        graph, claims, {"E1": "UNDETERMINED"},
        {"E1": "UNDETERMINED", "E2": "SUPPORTED"},
        ((_ev("E2", "sB"), ANCHORING),))
    assert out["c"][0] in ("STRENGTHENED", "RESOLVED")


def test_derived_claim_capped_without_new_support():
    # E1's verdict does not change (still UNDETERMINED): the derived
    # claim cannot rise on a no-op.
    graph = {"c": (("E1", "DERIVED_FROM"),)}
    claims = {"c": ClaimNode("c", graph["c"], "AND", "UNDETERMINED")}
    out = recompute_on_addition(
        graph, claims, {"E1": "UNDETERMINED"}, {"E1": "UNDETERMINED"},
        ((_ev("E1"), ANCHORING),))
    assert out["c"][0] == "RECOMPUTED_UNCHANGED"


# ---------------------------------------------------------------------------
# The decisive addition demonstration
# ---------------------------------------------------------------------------

def test_decisive_addition_classified_anchoring():
    res = run_d32_decisive_addition()
    cls, _ = res["addition_classification"]
    assert cls == ANCHORING


def test_decisive_addition_recomputes_exactly_affected():
    res = run_d32_decisive_addition()
    actions = res["claim_actions"]
    assert actions["H1"][0] == "RESOLVED", actions["H1"]
    assert actions["H2"][0] == "RESOLVED", actions["H2"]
    assert actions["note_causal"][0] == "RECOMPUTED_AMENDMENT_REQUIRED", \
        actions["note_causal"]
    assert actions["outcome"][0] == "UNAFFECTED", actions["outcome"]
    assert actions["mentioner"][0] == "UNAFFECTED", actions["mentioner"]


def test_outcome_verdict_never_rises_on_causal_evidence():
    res = run_d32_decisive_addition()
    # The outcome was already SUPPORTED via its independent source; the
    # causal evidence must not "strengthen" it further.
    assert res["claim_actions"]["outcome"][0] == "UNAFFECTED"


def test_repetition_changes_nothing_end_to_end():
    res = run_d32_decisive_addition()
    cls, _ = res["repetition_classification"]
    assert cls == REPEATING
    assert res["repetition_changes_nothing"] is True


def test_promotion_rejected_end_to_end():
    res = run_d32_decisive_addition()
    cls, reasons = res["promotion_classification"]
    assert cls == PROMOTING, reasons


def test_fixture_graph_shape():
    fx = build_d32_addition_fixture()
    assert set(fx["claims"]) == {"outcome", "H1", "H2", "note_causal",
                                "mentioner"}
    assert "stage4_smart_note" in fx["base"]
    # The causal trace is not a premise of the outcome claim.
    assert all(dep != "E_trace_complete"
               for dep, _ in fx["claims"]["outcome"].premises)


# ---------------------------------------------------------------------------
# The false-certainty cascade
# ---------------------------------------------------------------------------

def test_cascade_detects_promotion_at_every_stage():
    res = run_false_certainty_cascade()
    assert res["all_promotions_detected"] is True
    for stage in ("causal_report", "smart_note", "brain_index",
                  "successor_package"):
        detected, reasons = res["stages"][stage]
        assert detected, (stage, reasons)


def test_cascade_outcome_stays_usable():
    res = run_false_certainty_cascade()
    assert res["outcome_usable_throughout"] is True
    for stage, verdict, modality, usable in res["outcome_trace"]:
        assert verdict == "SUPPORTED"
        assert usable == "usable"


def test_cascade_successor_denies_certification_use():
    res = run_false_certainty_cascade()
    detected, reasons = res["stages"]["successor_package"]
    assert detected
    assert any("certification_use_denied" in r for r in reasons)
