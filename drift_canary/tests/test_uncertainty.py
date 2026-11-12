"""Tests: uncertain compromise scope — four-family fixture + ten framework tests."""
import pytest

from ..uncertainty import (
    UncertainCompromiseIncident, ExposureEdge, ClearancePacket,
    UncertainRecomputation, verdict_for_qualification,
    FAMILY_ASSESSMENTS, TRIVALUE, EDGE_EXPOSURE_SEMANTICS,
    QUALIFICATION_POLICY, USE_RESPONSES, ESCALATION_RULES,
)


def make_four_family_incident():
    """The fixture: one compromised, one possibly exposed, one independently
    cleared, one unassessed family."""
    return UncertainCompromiseIncident(
        incident_id="CCI-EXAMPLE-017",
        scope_state="PARTIALLY_BOUNDED",
        confirmed_affected=("FAMILY-A",),
        possibly_affected=("FAMILY-B",),
        independently_cleared=("FAMILY-C",),
        unassessed=("FAMILY-D",),
        exposure_edges=(
            ExposureEdge(from_family="FAMILY-A", to_family="FAMILY-B",
                         mechanism="SHARED_EVALUATOR", status="POSSIBLE",
                         evidence_ref="EXPOSURE-RECEIPT-001"),
            # A mere citation edge must NOT propagate compromise.
            ExposureEdge(from_family="FAMILY-A", to_family="FAMILY-C",
                         mechanism="CITES", status="POSSIBLE"),
        ),
        corpus_hash="sha256:abc",
        access_log_coverage="PARTIAL",
        review_deadline="2026-10-17T18:00:00Z",
    )


def test_fixture_four_different_outcomes():
    """Four families, four different outcomes — not one blanket quarantine."""
    inc = make_four_family_incident()
    assert inc.policy_for("FAMILY-A") == "DISQUALIFY_CONTRIBUTION"
    assert inc.policy_for("FAMILY-B") == "HOLD_INDEPENDENT_CERTIFICATION"
    assert inc.policy_for("FAMILY-C") == "PRESERVE_ELIGIBILITY"
    assert inc.policy_for("FAMILY-D") == "REVIEW_REQUIRED"
    assert inc.trivalue_of("FAMILY-A") == "CONFIRMED"
    assert inc.trivalue_of("FAMILY-B") == "UNDETERMINED"
    assert inc.trivalue_of("FAMILY-C") == "EXCLUDED"
    assert inc.trivalue_of("FAMILY-D") == "UNDETERMINED"


def test_1_confirmed_leakage_disqualifies_contribution():
    inc = make_four_family_incident()
    assert inc.assessment_of("FAMILY-A") == "confirmed_compromised"
    assert verdict_for_qualification(inc, ("FAMILY-A",), False) == "REVOKED"


def test_2_plausible_shared_exposure_is_undetermined():
    inc = make_four_family_incident()
    assert inc.assessment_of("FAMILY-B") == "possibly_compromised"
    assert verdict_for_qualification(inc, ("FAMILY-B",), True) == "SUSPENDED"


def test_3_verified_independent_provenance_preserved():
    inc = make_four_family_incident()
    assert inc.assessment_of("FAMILY-C") == "independently_cleared"
    assert verdict_for_qualification(inc, ("FAMILY-C",), True) == "REQUALIFIED"
    assert verdict_for_qualification(inc, ("FAMILY-C",), False) == "INSUFFICIENT_DATA"


def test_4_missing_audit_records_not_auto_cleared():
    inc = make_four_family_incident()
    assert inc.assessment_of("FAMILY-D") == "unassessed"
    assert verdict_for_qualification(inc, ("FAMILY-D",), True) == "SUSPENDED"
    # Cleared-only verdict cannot reach through an unassessed family.
    assert verdict_for_qualification(
        inc, ("FAMILY-C", "FAMILY-D"), True) == "SUSPENDED"


def test_5_possible_exposure_traced_across_evaluations():
    inc = UncertainCompromiseIncident(
        incident_id="CCI-018", confirmed_affected=("A",),
        possibly_affected=("B",), independently_cleared=(),
        unassessed=("D",),
        exposure_edges=(
            ExposureEdge("A", "B", "SHARED_EVALUATOR", "POSSIBLE"),
            ExposureEdge("B", "D", "SHARED_EVALUATOR", "POSSIBLE"),
        ))
    closure = inc.possible_closure()
    assert "B" in closure and "D" in closure
    assert "A" in inc.confirmed_closure()


def test_6_nonmaterial_citation_does_not_propagate():
    inc = make_four_family_incident()
    # CITES edge A→C: C stays EXCLUDED, never pulled into the possible closure.
    assert "FAMILY-C" not in inc.possible_closure()
    assert inc.trivalue_of("FAMILY-C") == "EXCLUDED"


def test_7_aggregate_losing_coverage_suspends_or_downgrades():
    inc = make_four_family_incident()
    # Aggregate over all four: confirmed + uncertain families present.
    verdict = verdict_for_qualification(
        inc, ("FAMILY-A", "FAMILY-B", "FAMILY-C", "FAMILY-D"), True)
    assert verdict == "REVOKED"  # confirmed A taints the aggregate claim
    # Narrow to cleared family only: claim narrows, not revoked.
    verdict = verdict_for_qualification(inc, ("FAMILY-C",), True)
    assert verdict == "REQUALIFIED"
    verdict = verdict_for_qualification(inc, ("FAMILY-C",), False)
    assert verdict == "INSUFFICIENT_DATA"


def test_8_new_evidence_narrows_boundary_recomputes():
    inc = make_four_family_incident()
    # B proves independent provenance → moves to cleared → recompute.
    narrowed = UncertainCompromiseIncident(
        incident_id="CCI-EXAMPLE-017", scope_state="PARTIALLY_BOUNDED",
        confirmed_affected=("FAMILY-A",),
        possibly_affected=(),
        independently_cleared=("FAMILY-B", "FAMILY-C"),
        unassessed=("FAMILY-D",),
        reassessment_events=("CLEARANCE-FAMILY-B-CLEARED",))
    assert verdict_for_qualification(
        narrowed, ("FAMILY-B", "FAMILY-C"), True) == "REQUALIFIED"
    assert narrowed.trivalue_of("FAMILY-B") == "EXCLUDED"


def test_9_irrecoverable_history_retires_blind_use():
    packet = ClearancePacket(
        family="FAMILY-D",
        audit_history_irrecoverable=True,
    )
    assert packet.decision() == "RETIRE_AND_REPLACE"
    assert not packet.is_complete()


def test_9b_clearance_requires_positive_evidence():
    packet = ClearancePacket(
        family="FAMILY-B",
        provenance_verified=True,
        access_exposure_evidence=True,
        no_disqualifying_dependency=True,
        independent_reviewer="coda-1",
        recomputed_stats=True,
        recorded_verdict="cleared-2026-10-10",
    )
    assert packet.is_complete()
    assert packet.decision() == "CLEARED"
    partial = ClearancePacket(family="FAMILY-B", provenance_verified=True)
    assert partial.decision() == "INCOMPLETE"
    # No auto-clear: nothing is cleared by default.
    assert ClearancePacket(family="FAMILY-X").decision() == "INCOMPLETE"


def test_10_cold_successor_honors_current_eligibility_preserves_history():
    inc = make_four_family_incident()
    # Successor re-derives from current certificates, never inherits verdicts.
    current = {f: inc.policy_for(f) for f in
               ("FAMILY-A", "FAMILY-B", "FAMILY-C", "FAMILY-D")}
    assert current == {
        "FAMILY-A": "DISQUALIFY_CONTRIBUTION",
        "FAMILY-B": "HOLD_INDEPENDENT_CERTIFICATION",
        "FAMILY-C": "PRESERVE_ELIGIBILITY",
        "FAMILY-D": "REVIEW_REQUIRED",
    }
    assert inc.historical_receipts == "PRESERVE"


def test_uncertain_recomputation_conservative_and_sensitivity():
    r = UncertainRecomputation(
        qualification_id="Q-AGG",
        cleared_cases=40, possible_cases=30, unassessed_cases=10,
        confirmed_cases=20, original_cases=100,
        cleared_family_difficulty="easier",
    )
    assert r.conservative_count() == 40
    assert not r.acceptance_hold(min_cases=80, min_families=4, cleared_families=2)
    sens = r.sensitivity_flip(cleared_rate=0.9, uncertain_rates=(0.9, 0.5, 0.1))
    # Optimistic assumption must never drive the verdict: even 0.9 uncertain
    # rate does not restore the original population claim.
    assert sens[0.1] < sens[0.9]
    assert "easier" in r.generalization_warning()


def test_deadline_passing_never_auto_clears():
    rules = "\n".join(ESCALATION_RULES)
    assert "NEVER auto-clear" in rules


def test_edge_semantics_typed():
    assert EDGE_EXPOSURE_SEMANTICS["ANSWER_EXPOSED_TO"] == "propagates_confirmed_compromise"
    assert EDGE_EXPOSURE_SEMANTICS["SHARED_EVALUATOR"] == "creates_possible_exposure"
    assert EDGE_EXPOSURE_SEMANTICS["CITES"] == "no_propagation"
    assert EDGE_EXPOSURE_SEMANTICS["HISTORICAL_ASSOCIATION"] == "no_propagation"
    assert set(FAMILY_ASSESSMENTS) == {
        "confirmed_compromised", "possibly_compromised",
        "independently_cleared", "unassessed"}
    assert set(TRIVALUE) == {"CONFIRMED", "EXCLUDED", "UNDETERMINED"}


def test_family_in_two_buckets_rejected():
    with pytest.raises(AssertionError):
        UncertainCompromiseIncident(
            incident_id="bad", confirmed_affected=("A",),
            possibly_affected=("A",))


def test_use_responses_four_by_use():
    assert USE_RESPONSES["independent_qualification"] == \
        "uncertain_contributions_do_not_count"
    assert USE_RESPONSES["consequential_act"].startswith("hold_dependent_action")
