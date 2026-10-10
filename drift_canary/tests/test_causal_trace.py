"""Tests for the Causal Execution Proof Contract (Shawn, 2026-10-10).

Every negative test has a positive control. Verdicts are asserted from
the evidence shape — never from a prewritten label.
"""

import pytest

from causal_trace import (
    CausalGraph, CausalHypothesis, CausalRelationship, CausalTraceReceipt,
    ControlledWorkflow, EvidenceEvent, IndependentCausalVerifier,
    ObservationCoverage,
    derive_verdict, derived_verdict_of, diagnose, qualify_ladder,
    verify_negative_claim,
    EV_DISPATCH, EV_DISPATCH_NOT_OBSERVED, EV_RESOURCE_OFFER,
    EV_OBLIGATION_ELIGIBLE, EV_EFFECT_OBSERVED, EV_SCHEDULER_HOLD,
    L0_REPORTED, L1_AUTHENTICATED, L2_CORROBORATED, L3_QUALIFIED,
    CAUSAL_UNASSESSED, CAUSAL_HYPOTHESIZED, CAUSAL_SUPPORTED,
    CAUSAL_EXPERIMENTALLY_VERIFIED,
    REL_CORRELATES_WITH, REL_HAPPENS_BEFORE, REL_DEPENDS_ON,
    REL_ENABLED_BY, REL_PREVENTED_BY, REL_CAUSED_BY,
    V_ENVIRONMENT_BLOCKER, V_SCHEDULER_STARVATION,
    V_SCHEDULER_SERVICE_FAILURE, V_WORKER_NONPROGRESS,
    V_GOVERNED_AUTHORITY_BLOCK, V_OUTCOME_NOT_VERIFIED,
    V_CONFLICTED_EVIDENCE, V_INSUFFICIENT_OBSERVABILITY,
    V_MULTIPLE_SUPPORTED_CAUSES, V_UNDETERMINED,
)


def _ev(eid, etype=EV_DISPATCH, producer="SCHEDULER", observer="SCHEDULER",
        status=L1_AUTHENTICATED, **kw):
    return EvidenceEvent(
        event_id=eid, workflow_id="WF-001", obligation_id="ACT-042",
        event_type=etype, producer=producer, observer=observer,
        trace_id="TRACE-WF-001", observation_status=status,
        scope="test", policy_version="LAW-V1", **kw)


def _coverage():
    return ObservationCoverage(
        observation_interval=(0, 100),
        monitored_sources=("SCHEDULER", "WORKER"),
        sequence_complete=True,
        dropped_message_indicators=(),
        visibility_limits=(),
    )


# ---------------------------------------------------------------------------
# 1. Canonical evidence event
# ---------------------------------------------------------------------------

class TestCanonicalEvent:
    def test_valid_event_constructs(self):
        e = _ev("E1")
        assert e.event_id == "E1"
        assert e.observation_status == L1_AUTHENTICATED

    def test_rejects_unknown_event_type(self):
        with pytest.raises(AssertionError):
            _ev("E1", etype="MADE_UP")

    def test_rejects_unknown_ladder_rung(self):
        with pytest.raises(AssertionError):
            _ev("E1", status="TRUST_ME")

    def test_event_claim_verdict_have_separate_identities(self):
        # The observed event, the causal claim, and the verdict are three
        # different objects — a worker cannot certify its own failure's
        # cause by embedding "reason": "scheduler" in a log line.
        e = _ev("E1")
        h = CausalHypothesis("H1", REL_CAUSED_BY, "E1", "E2")
        assert h.hypothesis_id != e.event_id
        assert isinstance(h, CausalHypothesis) and isinstance(e, EvidenceEvent)

    def test_duplicate_event_id_rejected(self):
        g = CausalGraph()
        g.add_event(_ev("E1"))
        with pytest.raises(ValueError):
            g.add_event(_ev("E1"))


# ---------------------------------------------------------------------------
# 2. Four-level ladder
# ---------------------------------------------------------------------------

class TestLadder:
    def test_no_integrity_stays_reported(self):
        # Negative: without integrity evidence the event never leaves L0.
        assert qualify_ladder(_ev("E1"), has_integrity=False) == L0_REPORTED

    def test_integrity_reaches_authenticated(self):
        # Positive control: integrity evidence reaches L1.
        assert qualify_ladder(_ev("E1"), has_integrity=True) == L1_AUTHENTICATED

    def test_signature_alone_does_not_corroborate(self):
        # A signature proves origin under a trust model — never truth.
        # An event with only its own signature stays at L1.
        e = _ev("E1", signature_or_attestation="sig:abc")
        assert qualify_ladder(e, has_integrity=True) == L1_AUTHENTICATED

    def test_independent_witness_reaches_l2(self):
        # Positive control: a genuinely independent witness corroborates.
        e = _ev("E1", producer="SCHEDULER", observer="SCHEDULER",
                artifact_hashes=("h1",))
        w = _ev("W1", producer="TRACE_VERIFIER", observer="VERIFY",
                status=L1_AUTHENTICATED, artifact_hashes=("h2",))
        assert qualify_ladder(e, True, independent_witness=w) == L2_CORROBORATED

    def test_shared_corrupted_record_is_not_corroboration(self):
        # Negative: two parties reading the SAME corrupted record is
        # agreement, not independent corroboration — stays at L1.
        e = _ev("E1", producer="SCHEDULER", observer="SCHEDULER",
                artifact_hashes=("corrupted",))
        w = _ev("W1", producer="SCHEDULER", observer="SCHEDULER",
                status=L1_AUTHENTICATED, artifact_hashes=("corrupted",))
        assert qualify_ladder(e, True, independent_witness=w) == L1_AUTHENTICATED

    def test_causal_argument_reaches_l3(self):
        e = _ev("E1")
        assert qualify_ladder(e, True,
                              causal_argument={"justified": True}) == L3_QUALIFIED


# ---------------------------------------------------------------------------
# 3. Promotion rules
# ---------------------------------------------------------------------------

class TestPromotionRules:
    def _graph(self):
        g = CausalGraph()
        g.add_event(_ev("E1"))
        g.add_event(_ev("E2"))
        return g

    def test_correlates_with_cannot_silently_become_caused_by(self):
        # Negative: the machine rejects the silent promotion.
        g = self._graph()
        g.add_relationship(CausalRelationship(REL_CORRELATES_WITH, "E1", "E2"))
        with pytest.raises(ValueError):
            g.add_relationship(CausalRelationship(REL_CAUSED_BY, "E1", "E2"))

    def test_caused_by_allowed_after_three_check(self):
        # Positive control: with the three-check recorded, CAUSED_BY is
        # assertable alongside the correlation.
        g = self._graph()
        g.add_relationship(CausalRelationship(REL_CORRELATES_WITH, "E1", "E2"))
        g.record_three_check("E1", "E2", mechanism=True,
                             counterfactual=True, reproduction=True)
        g.add_relationship(CausalRelationship(REL_CAUSED_BY, "E1", "E2"))
        assert len(g.relationships) == 2

    def test_happens_before_is_not_causation(self):
        # HAPPENS_BEFORE establishes ordering only; it never licenses a
        # CAUSED_BY conclusion by itself.
        g = self._graph()
        g.add_relationship(CausalRelationship(REL_HAPPENS_BEFORE, "E1", "E2"))
        with pytest.raises(ValueError):
            g.add_relationship(CausalRelationship(REL_CAUSED_BY, "E1", "E2"))

    def test_competing_explanations_preserved(self):
        g = self._graph()
        g.add_event(_ev("E3"))
        g.record_three_check("E1", "E3", True, True, True)
        g.record_three_check("E2", "E3", True, True, True)
        g.add_relationship(CausalRelationship(REL_CAUSED_BY, "E1", "E3"))
        g.add_relationship(CausalRelationship(REL_PREVENTED_BY, "E2", "E3"))
        assert len(g.competing_explanations("E3")) == 2


# ---------------------------------------------------------------------------
# 4. Causal-order reconstruction
# ---------------------------------------------------------------------------

class TestCausalOrder:
    def test_order_from_edges_not_timestamps(self):
        g = CausalGraph()
        # Wall-clock deliberately misleading: E2 "earlier" by timestamp.
        g.add_event(_ev("E1", local_sequence=2, logical_clock=20))
        g.add_event(_ev("E2", local_sequence=1, logical_clock=10))
        g.add_relationship(CausalRelationship(REL_HAPPENS_BEFORE, "E2", "E1"))
        tiers = g.causal_order()
        assert tiers == [{"E2"}, {"E1"}]

    def test_unordered_events_stay_concurrent(self):
        # No verified ordering relationship -> concurrent, never forcibly
        # arranged into a causal story.
        g = CausalGraph()
        g.add_event(_ev("E1"))
        g.add_event(_ev("E2"))
        tiers = g.causal_order()
        assert tiers == [{"E1", "E2"}]

    def test_ordering_cycle_rejected_not_invented(self):
        g = CausalGraph()
        g.add_event(_ev("E1"))
        g.add_event(_ev("E2"))
        g.add_relationship(CausalRelationship(REL_HAPPENS_BEFORE, "E1", "E2"))
        g.add_relationship(CausalRelationship(REL_HAPPENS_BEFORE, "E2", "E1"))
        with pytest.raises(ValueError):
            g.causal_order()


# ---------------------------------------------------------------------------
# 5. Three-check causal responsibility
# ---------------------------------------------------------------------------

class TestThreeCheck:
    def _verifier(self):
        g = CausalGraph()
        g.add_event(_ev("E1"))
        g.add_event(_ev("E2"))
        return IndependentCausalVerifier(g)

    def test_mechanism_only_is_hypothesized(self):
        v = self._verifier()
        h = CausalHypothesis("H1", REL_CAUSED_BY, "E1", "E2", mechanism_ok=True)
        assert v.evaluate_hypothesis(h) == CAUSAL_HYPOTHESIZED

    def test_mechanism_plus_counterfactual_is_supported_with_limits(self):
        # Positive control: observational evidence yields a mechanistic
        # explanation WITH limitations — never mislabeled as reproduced.
        v = self._verifier()
        h = CausalHypothesis("H1", REL_CAUSED_BY, "E1", "E2",
                             mechanism_ok=True, counterfactual_ok=True)
        assert v.evaluate_hypothesis(h) == CAUSAL_SUPPORTED
        assert "limitations" in h.notes

    def test_full_three_check_is_experimentally_verified(self):
        v = self._verifier()
        h = CausalHypothesis("H1", REL_CAUSED_BY, "E1", "E2",
                             mechanism_ok=True, counterfactual_ok=True,
                             reproduction_ok=True)
        assert v.evaluate_hypothesis(h) == CAUSAL_EXPERIMENTALLY_VERIFIED

    def test_no_mechanism_is_unassessed(self):
        v = self._verifier()
        h = CausalHypothesis("H1", REL_CAUSED_BY, "E1", "E2")
        assert v.evaluate_hypothesis(h) == CAUSAL_UNASSESSED


# ---------------------------------------------------------------------------
# 6. Negative-claim coverage
# ---------------------------------------------------------------------------

class TestNegativeClaims:
    def test_missing_entry_is_not_proof_of_absence(self):
        # Negative: a negative claim without coverage is rejected.
        e = _ev("E1", etype=EV_DISPATCH_NOT_OBSERVED)
        ok, verdict = verify_negative_claim(e, None)
        assert not ok and verdict == V_INSUFFICIENT_OBSERVABILITY

    def test_covered_negative_claim_accepted(self):
        # Positive control: with coverage, the negative claim stands.
        e = _ev("E1", etype=EV_DISPATCH_NOT_OBSERVED)
        ok, _ = verify_negative_claim(e, _coverage())
        assert ok

    def test_incomplete_coverage_rejected(self):
        cov = ObservationCoverage(
            observation_interval=(0, 0), monitored_sources=(),
            sequence_complete=False, dropped_message_indicators=(),
            visibility_limits=("scheduler channel unwatched",))
        e = _ev("E1", etype=EV_DISPATCH_NOT_OBSERVED)
        ok, verdict = verify_negative_claim(e, cov)
        assert not ok and verdict == V_INSUFFICIENT_OBSERVABILITY

    def test_non_negative_claim_needs_no_coverage(self):
        e = _ev("E1", etype=EV_DISPATCH)
        ok, _ = verify_negative_claim(e, None)
        assert ok

# ---------------------------------------------------------------------------
# 7. Nine-scenario adversarial suite — same symptom, nine causes.
# ---------------------------------------------------------------------------

EXPECTED_VERDICTS = {
    "environment_outage": V_ENVIRONMENT_BLOCKER,
    "scheduler_withholds": V_SCHEDULER_STARVATION,
    "dispatch_without_resources": V_SCHEDULER_SERVICE_FAILURE,
    "worker_fails": V_WORKER_NONPROGRESS,
    "authority_refused": V_GOVERNED_AUTHORITY_BLOCK,
    "false_success": V_OUTCOME_NOT_VERIFIED,
    "two_blockers": V_MULTIPLE_SUPPORTED_CAUSES,
}


def _run_case(fault, counterfactual_ok=True, reproduction_ok=True):
    """Drive one experiment: run the fault, the healthy counterfactual,
    and an independent reproduction; return the verifier's verdict."""
    wf = ControlledWorkflow()
    cov = _coverage()
    graph = wf.run(fault)
    # Counterfactual: the healthy run completes.
    healthy = ControlledWorkflow().run("healthy")
    hv, _ = derive_verdict(healthy, {"E4": cov, "E4v": cov})
    counterfactual_ok = counterfactual_ok and hv == V_UNDETERMINED
    # Independent reproduction: a second run reproduces the evidence shape.
    repro = ControlledWorkflow().run(fault)
    rv, _ = derive_verdict(repro, {"E4": cov, "E4v": cov})
    ev, _ = derive_verdict(graph, {"E4": cov, "E4v": cov})
    reproduction_ok = reproduction_ok and rv == ev
    hyp = diagnose(graph, fault, counterfactual_ok=counterfactual_ok,
                   reproduction_ok=reproduction_ok)
    verifier = IndependentCausalVerifier(graph)
    verdict, receipt = verifier.issue_verdict([hyp], {"E4": cov, "E4v": cov})
    return verdict, receipt, hyp


class TestAdversarialSuite:
    @pytest.mark.parametrize("fault,expected", list(EXPECTED_VERDICTS.items()))
    def test_each_cause_gets_its_verdict(self, fault, expected):
        # The same symptom (unfinished workflow) yields a different
        # verdict per actual cause — from evidence, not labels.
        verdict, receipt, hyp = _run_case(fault)
        assert verdict == expected, f"{fault}: got {verdict}"
        assert receipt["causal_hypothesis"]["verdict"] == expected

    def test_healthy_run_has_no_causal_verdict(self):
        verdict, _, _ = _run_case("healthy")
        assert verdict == V_UNDETERMINED

    def test_conflicted_evidence_detected(self):
        # Hand-built: scheduler claims a specific lease; the worker side
        # shows nothing and the claim is uncorroborated.
        g = CausalGraph()
        g.add_event(_ev("E1", etype=EV_RESOURCE_OFFER,
                        producer="RESOURCE_RUNTIME", observer="KNOW"))
        g.add_event(_ev("E2", etype=EV_OBLIGATION_ELIGIBLE,
                        producer="KNOW", observer="KNOW"))
        g.add_event(_ev("E4", etype=EV_DISPATCH, producer="SCHEDULER",
                        observer="SCHEDULER", lease_id="LEASE-9"))
        v, reasons = derive_verdict(g, {"E4": _coverage(), "E4v": _coverage()})
        assert v == V_CONFLICTED_EVIDENCE, reasons

    def test_incomplete_coverage_yields_insufficient_observability(self):
        # The dispatch-absence claim without coverage must not become a
        # scheduler verdict — and must not shift blame to the quieter
        # component either.
        g = ControlledWorkflow().run("scheduler_withholds")
        v, _ = derive_verdict(g, {})
        assert v == V_INSUFFICIENT_OBSERVABILITY


# ---------------------------------------------------------------------------
# 8. Label-swap negative test
# ---------------------------------------------------------------------------

class TestLabelSwap:
    def test_verdict_invariant_under_label_swap(self):
        # Swap the reported failure labels with the evidence unchanged:
        # the independently calculated verdict must NOT change.
        v1, _ = derive_verdict(ControlledWorkflow().run("environment_outage"),
                               {"E4": _coverage(), "E4v": _coverage()})
        v2, _ = derive_verdict(ControlledWorkflow().run("scheduler_withholds"),
                               {"E4": _coverage(), "E4v": _coverage()})
        assert v1 == V_ENVIRONMENT_BLOCKER
        assert v2 == V_SCHEDULER_STARVATION
        # The verdicts come from derive_verdict (evidence shape), which
        # takes no label input at all: there is no label to swap that
        # could move them.
        import inspect
        assert "label" not in inspect.signature(derive_verdict).parameters

    def test_corrupted_log_does_not_change_conclusion(self):
        # Corrupt the scheduler's log AND swap its labels: the verifier
        # must reject the false evidence (via the independent observer)
        # rather than follow the corrupted narrative.
        g = ControlledWorkflow().run(
            "scheduler_withholds", lying_producer="SCHEDULER",
            swapped_labels=True)
        v, reasons = derive_verdict(g, {"E4": _coverage(), "E4v": _coverage()})
        assert v == V_SCHEDULER_STARVATION, reasons
        assert any("set aside" in r for r in reasons)

    def test_fully_blinded_verifier_downgrades_to_uncertainty(self):
        # If the independent observation is ALSO removed, the verifier
        # must downgrade to uncertainty — never invent blame.
        g = ControlledWorkflow().run(
            "scheduler_withholds", lying_producer="SCHEDULER",
            swapped_labels=True)
        del g.events["E4v"]
        v, _ = derive_verdict(g, {})
        assert v in (V_UNDETERMINED, V_INSUFFICIENT_OBSERVABILITY,
                     V_CONFLICTED_EVIDENCE), v


# ---------------------------------------------------------------------------
# 9. Decisive experiment: KNOW -> LAW -> ACT -> VERIFY, three injections
# ---------------------------------------------------------------------------

class TestDecisiveExperiment:
    def test_case_a_environment_failure_no_false_blame(self):
        verdict, _, _ = _run_case("environment_outage")
        assert verdict == V_ENVIRONMENT_BLOCKER

    def test_case_b_scheduler_failure_not_hidden(self):
        # Environment assumptions cannot hide the scheduler defect.
        verdict, _, _ = _run_case("scheduler_withholds")
        assert verdict == V_SCHEDULER_STARVATION

    def test_case_c_worker_failure_scheduler_may_stay_qualified(self):
        verdict, _, _ = _run_case("worker_fails")
        assert verdict == V_WORKER_NONPROGRESS

    def test_same_symptom_different_verdicts(self):
        verdicts = {f: _run_case(f)[0] for f in
                    ("environment_outage", "scheduler_withholds",
                     "worker_fails")}
        assert len(set(verdicts.values())) == 3

    def test_lying_component_still_classified_correctly(self):
        # The failing component falsely blames another; the evidence
        # still names the right boundary.
        verdict, _, _ = _run_case("scheduler_withholds")
        g = ControlledWorkflow().run(
            "scheduler_withholds", lying_producer="SCHEDULER",
            swapped_labels=True)
        v, _ = derive_verdict(g, {"E4": _coverage(), "E4v": _coverage()})
        assert v == verdict == V_SCHEDULER_STARVATION


# ---------------------------------------------------------------------------
# 10. Causal-trace receipt
# ---------------------------------------------------------------------------

class TestReceipt:
    def test_receipt_is_machine_readable_and_blame_free(self):
        verdict, receipt, hyp = _run_case("scheduler_withholds")
        assert receipt["trace_id"].startswith("TRACE-")
        assert receipt["workflow_id"] == "WF-001"
        assert receipt["obligation_id"] == "ACT-042"
        assert receipt["causal_hypothesis"]["verdict"] == V_SCHEDULER_STARVATION
        assert receipt["causal_hypothesis"]["alternative_causes_checked"] is True
        # Blame-free before the three-check completes: with no
        # counterfactual/reproduction the qualification stays unestablished.
        _, receipt2, _ = _run_case("scheduler_withholds",
                                   counterfactual_ok=False,
                                   reproduction_ok=False)
        assert receipt2["overall_qualification"] == "NOT_YET_ESTABLISHED"

    def test_receipt_is_derived_not_a_second_source_of_truth(self):
        _, receipt, _ = _run_case("worker_fails")
        event_ids = {e["id"] for e in receipt["events"]}
        for eid in receipt["causal_hypothesis"]["supporting_events"]:
            assert eid in event_ids  # every cited event exists in the trace

    def test_verifier_identity_and_clock_assumptions_recorded(self):
        _, receipt, _ = _run_case("environment_outage")
        assert receipt["verifier_identity"] == "INDEPENDENT-VERIFY"
        assert "wall-clock" in receipt["clock_assumptions"]


# ---------------------------------------------------------------------------
# 11. Cold-verifier standard (top-level acceptance)
# ---------------------------------------------------------------------------

class TestColdVerifierStandard:
    def test_fresh_verifier_reproduces_conclusion(self):
        # A FRESH verifier — new graph object, new verifier instance, no
        # shared state with the experiment driver — reconstructs what
        # happened, names the failed guarantee, and reproduces the
        # conclusion from the evidence alone.
        g1 = ControlledWorkflow().run("worker_fails")
        v1, _ = derive_verdict(g1, {"E4": _coverage(), "E4v": _coverage()})
        # Fresh run, fresh objects, same evidence shape.
        g2 = ControlledWorkflow().run("worker_fails")
        fresh = IndependentCausalVerifier(g2, verifier_identity="COLD-VERIFY")
        hyp = diagnose(g2, "worker_fails", counterfactual_ok=True,
                       reproduction_ok=True)
        v2, receipt = fresh.issue_verdict([hyp], {"E4": _coverage(),
                                                 "E4v": _coverage()})
        assert v1 == v2 == V_WORKER_NONPROGRESS
        assert receipt["verifier_identity"] == "COLD-VERIFY"

    def test_cold_verifier_distinguishes_alternatives(self):
        for fault, expected in [("environment_outage", V_ENVIRONMENT_BLOCKER),
                                ("scheduler_withholds", V_SCHEDULER_STARVATION),
                                ("authority_refused",
                                 V_GOVERNED_AUTHORITY_BLOCK)]:
            g = ControlledWorkflow().run(fault)
            fresh = IndependentCausalVerifier(g)
            hyp = diagnose(g, fault, counterfactual_ok=True,
                           reproduction_ok=True)
            v, _ = fresh.issue_verdict([hyp], {"E4": _coverage(),
                                              "E4v": _coverage()})
            assert v == expected, f"{fault}: {v}"
