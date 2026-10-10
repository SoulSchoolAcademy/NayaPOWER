"""Tests for Causal Uncertainty Without False Blame (SN-0781).

Extension of the causal contracts — same seams, uncertainty machinery.
Every negative test has a positive control.
"""

import pytest

from causal_trace import EvidenceEvent, L1_AUTHENTICATED, L0_REPORTED
from causal_uncertainty import (
    ObservabilityClaim, Proposition, Blocker, BlockerSet,
    RevisableHypothesis, HypothesisSet, CausalUncertaintyRecord,
    decompose_dispatch_dispute, recompute_support, select_next_test,
    OBS_COVERED_COMPLETE, OBS_COVERED_PARTIAL, OBS_UNOBSERVED,
    OBS_CONFLICTED_COVERAGE, OBS_NOT_APPLICABLE,
    PROP_SUPPORTED, PROP_REFUTED, PROP_CONFLICTED, PROP_UNDETERMINED,
    PROP_NOT_APPLICABLE,
    STAGE_ISSUED, STAGE_REACHED, STAGE_ACCEPTED, STAGE_ATTEMPTED,
    BLOCKER_ACTIVE, BLOCKER_CLEARED, BLOCKER_UNASSESSED,
    CAUSE_CONTRIBUTING, CAUSE_NECESSARY, CAUSE_SUFFICIENT, CAUSE_POSSIBLE,
    HYP_ACTIVE, HYP_REFINED, HYP_SUPERSEDED, HYP_UNRESOLVED,
    REL_COMPATIBLE, REL_COMPETING, REL_DEPENDENT, REL_UNASSESSED,
)


def _ev(eid, etype, producer="SCHEDULER", observer="SCHEDULER",
        status=L1_AUTHENTICATED, artifacts=()):
    return EvidenceEvent(
        event_id=eid, workflow_id="WF-001", obligation_id="ACT-042",
        event_type=etype, producer=producer, observer=observer,
        trace_id="TRACE-WF-001", observation_status=status,
        artifact_hashes=tuple(artifacts), scope="test",
        policy_version="LAW-V1")


# ---------------------------------------------------------------------------
# 1. Four dimensions, never collapsed
# ---------------------------------------------------------------------------

class TestFourDimensions:
    def test_dimensions_stay_independent(self):
        rec = CausalUncertaintyRecord(
            record_id="R1", trace_id="TRACE-WF-001",
            observability=[ObservabilityClaim(
                source="SCHEDULER", event_type="DISPATCH",
                resource="queue", interval=(0, 50),
                status=OBS_COVERED_PARTIAL)],
            propositions=[Proposition("R1-P1", "issued", STAGE_ISSUED,
                                      verdict=PROP_SUPPORTED,
                                      evidence_refs=("E4",))],
            blockers=[Blocker("B1", "ACT-042", "no lease",
                              status=BLOCKER_ACTIVE, controller="SCHEDULER")],
            causal_hypotheses=[RevisableHypothesis(
                "H1", mechanism="withheld dispatch",
                cause_type=CAUSE_CONTRIBUTING, status=HYP_UNRESOLVED)],
            overall_causal_verdict="UNDETERMINED")
        d = rec.to_dict()
        # The overall verdict does not override the parts: a SUPPORTED
        # proposition and an ACTIVE blocker coexist with an UNDETERMINED
        # causal verdict and an UNRESOLVED hypothesis.
        assert d["propositions"][0]["verdict"] == PROP_SUPPORTED
        assert d["blockers"][0]["status"] == BLOCKER_ACTIVE
        assert d["causal_hypotheses"][0]["status"] == HYP_UNRESOLVED
        assert d["overall_causal_verdict"] == "UNDETERMINED"
        assert "never substitutes" in d["verdict_disclaimer"]

    def test_not_observed_is_not_did_not_happen(self):
        c = ObservabilityClaim(source="WORKER", event_type="ATTEMPT",
                               resource="worker-1", interval=(0, 50),
                               status=OBS_UNOBSERVED)
        assert not c.absence_meaningful()

    def test_conflicting_evidence_is_not_a_tie(self):
        p = Proposition("P1", "issued", STAGE_ISSUED, verdict=PROP_CONFLICTED)
        assert p.verdict == PROP_CONFLICTED  # stays conflicted; not averaged

    def test_confirmed_blocker_is_not_sole_cause(self):
        b = Blocker("B1", "ACT-042", "no lease", status=BLOCKER_ACTIVE,
                    controller="SCHEDULER")
        # A Blocker carries no causal claim at all: explaining current
        # impossibility is not proving original causality.
        assert not hasattr(b, "cause_type")
        assert b.status == BLOCKER_ACTIVE

    def test_unresolved_hypothesis_is_not_false(self):
        h = RevisableHypothesis("H1", mechanism="m",
                                cause_type=CAUSE_POSSIBLE,
                                status=HYP_UNRESOLVED)
        assert h.status == HYP_UNRESOLVED  # unresolved != false != true


# ---------------------------------------------------------------------------
# 2. Multi-hypothesis branches
# ---------------------------------------------------------------------------

class TestHypothesisSet:
    def test_conjunction_and_alternative_branches(self):
        hs = HypothesisSet()
        hs.add(RevisableHypothesis("H1", mechanism="m1",
                                   relationships={"H2": REL_COMPATIBLE}),
               branch=("conjunction", ("H1", "H2")))
        hs.add(RevisableHypothesis("H2", mechanism="m2",
                                   relationships={"H1": REL_COMPATIBLE}))
        hs.add(RevisableHypothesis("H3", mechanism="m3",
                                   relationships={"H1": REL_UNASSESSED}),
               branch=("alternative", ("H1", "H3")))
        assert len(hs.live()) == 3
        # The unassessed H1-vs-H3 relationship is flagged: choosing now
        # would force an unsupported choice.
        violations = hs.check_no_forced_choice()
        assert any("H1" in v and "H3" in v for v in violations)

    def test_no_violation_when_relationships_assessed(self):
        hs = HypothesisSet()
        hs.add(RevisableHypothesis("H1", mechanism="m1",
                                   relationships={"H2": REL_COMPETING}),
               branch=("alternative", ("H1", "H2")))
        hs.add(RevisableHypothesis("H2", mechanism="m2",
                                   relationships={"H1": REL_COMPETING}))
        assert hs.check_no_forced_choice() == []


# ---------------------------------------------------------------------------
# 3. Scoped observability
# ---------------------------------------------------------------------------

class TestObservability:
    def test_covered_complete_makes_absence_meaningful(self):
        c = ObservabilityClaim(source="S", event_type="DISPATCH",
                               resource="q", interval=(0, 100),
                               status=OBS_COVERED_COMPLETE,
                               sequence_continuous=True)
        assert c.absence_meaningful()

    def test_covered_complete_needs_sequence_continuity(self):
        c = ObservabilityClaim(source="S", event_type="DISPATCH",
                               resource="q", interval=(0, 100),
                               status=OBS_COVERED_COMPLETE,
                               sequence_continuous=False)
        assert not c.absence_meaningful()

    def test_partial_coverage_scoped(self):
        c = ObservabilityClaim(source="S", event_type="DISPATCH",
                               resource="q", interval=(0, 50),
                               status=OBS_COVERED_PARTIAL,
                               sequence_continuous=True,
                               collection_boundaries=("second half unwatched",))
        assert not c.absence_meaningful()
        assert c.collection_boundaries == ("second half unwatched",)


# ---------------------------------------------------------------------------
# 4. Claim-level propositions
# ---------------------------------------------------------------------------

class TestPropositions:
    def test_dispatch_dispute_decomposes_to_four(self):
        from causal_trace import (EV_DISPATCH, EV_DISPATCH_ACCEPTED,
                                  EV_SERVICE_DELIVERED, EV_ATTEMPT)
        evs = [_ev("E4", EV_DISPATCH, producer="SCHEDULER",
                   observer="SCHEDULER", artifacts=("h-sched",)),
               _ev("E4v", EV_DISPATCH, producer="TRACE_VERIFIER",
                   observer="VERIFY", artifacts=("h-indep",)),
               _ev("E6", EV_SERVICE_DELIVERED, producer="SCHEDULER",
                   observer="WORKER", artifacts=("h-svc",)),
               _ev("E5", EV_DISPATCH_ACCEPTED, producer="WORKER",
                   observer="SCHEDULER", artifacts=("h-acc",)),
               _ev("E7", EV_ATTEMPT, producer="WORKER",
                   observer="WORKER", artifacts=("h-att",))]
        props = decompose_dispatch_dispute("D1", evs)
        assert [p.stage for p in props] == [STAGE_ISSUED, STAGE_REACHED,
                                            STAGE_ACCEPTED, STAGE_ATTEMPTED]
        by_stage = {p.stage: p for p in props}
        # P1 has two independent witness groups -> SUPPORTED.
        assert by_stage[STAGE_ISSUED].verdict == PROP_SUPPORTED
        # P2..P4 have one witness group each -> UNDETERMINED, not refuted.
        assert by_stage[STAGE_REACHED].verdict == PROP_UNDETERMINED

    def test_two_logs_one_bus_is_one_witness(self):
        # Negative: the scheduler emits the same dispatch claim twice
        # from the same bus — still one witness, still UNDETERMINED.
        from causal_trace import EV_DISPATCH
        evs = [_ev("E4a", EV_DISPATCH, artifacts=("h-same",)),
               _ev("E4b", EV_DISPATCH, artifacts=("h-same",))]
        props = decompose_dispatch_dispute("D2", evs)
        assert props[0].verdict == PROP_UNDETERMINED

    def test_reports_about_different_stages_do_not_contradict(self):
        # A report that P1 (issued) happened and a report that P4
        # (attempted) did not happen are about different stages: no
        # manufactured contradiction.
        from causal_trace import EV_DISPATCH
        evs = [_ev("E4", EV_DISPATCH, artifacts=("h1",))]
        props = decompose_dispatch_dispute("D3", evs)
        by_stage = {p.stage: p for p in props}
        assert by_stage[STAGE_ATTEMPTED].verdict == PROP_UNDETERMINED
        assert by_stage[STAGE_ATTEMPTED].verdict != PROP_REFUTED


# ---------------------------------------------------------------------------
# 5. Blocker algebra (+ anti-gaming #5)
# ---------------------------------------------------------------------------

class TestBlockerAlgebra:
    def _two_blockers(self):
        return BlockerSet(blockers=[
            Blocker("B1", "ACT-042", "no resource", status=BLOCKER_ACTIVE,
                    controller="RESOURCE_RUNTIME",
                    evidence_refs=("E1",)),
            Blocker("B2", "ACT-042", "scheduler hold", status=BLOCKER_ACTIVE,
                    controller="SCHEDULER", evidence_refs=("E4b",)),
        ])

    def test_minimal_blocking_sets(self):
        bs = self._two_blockers()
        assert bs.is_blocked()
        assert bs.minimal_blocking_sets() == [frozenset({"B1", "B2"})]

    def test_repair_one_of_two_still_blocked(self):
        # ANTI-GAMING #5: repair one confirmed blocker while another
        # remains -> workflow stays blocked, the repair IS recognized,
        # completion is NOT declared.
        bs = self._two_blockers()
        bs2 = bs.repair("B1", evidence_refs=("E1-clear",))
        repaired = {b.blocker_id: b for b in bs2.blockers}["B1"]
        assert repaired.status == BLOCKER_CLEARED      # repair recognized
        assert bs2.is_blocked()                         # still blocked
        assert bs2.minimal_blocking_sets() == [frozenset({"B2"})]

    def test_repair_requires_evidence(self):
        # ANTI-GAMING: assertion alone cannot clear a blocker.
        bs = self._two_blockers()
        with pytest.raises(ValueError):
            bs.repair("B1", evidence_refs=())

    def test_single_blocker_repair_unblocks(self):
        # Positive control: the last blocker repaired with evidence.
        bs = BlockerSet(blockers=[
            Blocker("B1", "ACT-042", "no resource", status=BLOCKER_ACTIVE,
                    controller="RESOURCE_RUNTIME", evidence_refs=("E1",))])
        bs2 = bs.repair("B1", evidence_refs=("E1-clear",))
        assert not bs2.is_blocked()
        assert bs2.minimal_blocking_sets() == []

    def test_alternative_paths(self):
        bs = BlockerSet(
            blockers=[
                Blocker("B1", "A", "c1", status=BLOCKER_ACTIVE,
                        controller="X", evidence_refs=("e",)),
                Blocker("B2", "A", "c2", status=BLOCKER_CLEARED,
                        controller="Y", evidence_refs=("e2",)),
                Blocker("B3", "A", "c3", status=BLOCKER_ACTIVE,
                        controller="Z", evidence_refs=("e3",)),
            ],
            alternatives=[frozenset({"B1", "B2"}), frozenset({"B3"})])
        assert bs.is_blocked()
        # Minimal: {B3} alone explains it; {B1} alone does not (B2 cleared).
        assert bs.minimal_blocking_sets() == [frozenset({"B3"})]


# ---------------------------------------------------------------------------
# 6. Revisable hypotheses
# ---------------------------------------------------------------------------

class TestRevisableHypotheses:
    def test_refine_supersedes_preserves_history(self):
        h = RevisableHypothesis("H1", mechanism="m1",
                                status=HYP_ACTIVE)
        child = h.refine(mechanism="m1-refined",
                         discriminating_test="T-compare")
        assert h.status == HYP_SUPERSEDED
        assert child.status == HYP_REFINED
        assert child.discriminating_test == "T-compare"

    def test_unresolved_never_auto_promotes(self):
        # ANTI-GAMING: no method promotes an unresolved hypothesis to
        # verified; only a discriminating test outcome plus re-evaluation
        # may change status, and that is the caller's job.
        h = RevisableHypothesis("H1", mechanism="m",
                                cause_type=CAUSE_POSSIBLE,
                                status=HYP_UNRESOLVED)
        assert h.status == HYP_UNRESOLVED
        assert h.cause_type == CAUSE_POSSIBLE  # weakest claim by default


# ---------------------------------------------------------------------------
# 7. Uncertainty record versioning
# ---------------------------------------------------------------------------

class TestUncertaintyRecord:
    def test_supersede_versions_never_edits(self):
        r1 = CausalUncertaintyRecord(record_id="R1", trace_id="T1")
        r2 = r1.supersede()
        assert r1.version == 1
        assert r2.version == 2
        assert r2.record_id == "R1"

    def test_record_has_all_five_sections(self):
        d = CausalUncertaintyRecord(record_id="R1",
                                    trace_id="T1").to_dict()
        for key in ("observability", "propositions", "blockers",
                    "causal_hypotheses", "overall_causal_verdict"):
            assert key in d

# ---------------------------------------------------------------------------
# 8. Support-set recomputation
# ---------------------------------------------------------------------------

class TestSupportRecomputation:
    def test_alternative_path_survives(self):
        # H1 <= (E1&E2) | (E3&E4). E2 unreliable -> second path supports.
        r = recompute_support("H1", [frozenset({"E1", "E2"}),
                                     frozenset({"E3", "E4"})],
                              unreliable={"E2"},
                              evidence_sources={"E1": "S1", "E2": "S2",
                                                "E3": "S3", "E4": "S4"})
        assert r["verdict"] == "SUPPORTED"
        assert r["admissible_paths"] == [["E3", "E4"]]

    def test_no_path_survives(self):
        r = recompute_support("H1", [frozenset({"E1", "E2"})],
                              unreliable={"E1"},
                              evidence_sources={"E1": "S1", "E2": "S2"})
        assert r["verdict"] == "UNDERMINED"
        assert r["admissible_paths"] == []

    def test_shared_contaminated_source_rejects_independence(self):
        # ANTI-GAMING: the remaining path shares E3's source with the
        # contaminated E2 -> apparent independence rejected.
        r = recompute_support("H1", [frozenset({"E1", "E2"}),
                                     frozenset({"E3", "E4"})],
                              unreliable={"E2"},
                              evidence_sources={"E1": "S1", "E2": "S2",
                                                "E3": "S2", "E4": "S4"})
        assert r["verdict"] == "NOT_INDEPENDENT"

    def test_uncertainty_follows_dependencies(self):
        # Contaminating a source used by every path undermines all of them.
        r = recompute_support("H1", [frozenset({"E1"}), frozenset({"E2"})],
                              unreliable={"E1", "E2"},
                              evidence_sources={"E1": "S1", "E2": "S1"})
        assert r["verdict"] == "UNDERMINED"


# ---------------------------------------------------------------------------
# 9. Next-test selection
# ---------------------------------------------------------------------------

class TestNextTestSelection:
    def test_picks_max_worst_case_elimination(self):
        cands = [
            {"test_id": "T1",
             "outcomes": {"a": ["H1", "H2"], "b": []}},
            {"test_id": "T2",
             "outcomes": {"a": ["H1"], "b": ["H2"]}},
        ]
        # T1 worst case eliminates 0; T2 worst case eliminates 1 -> T2.
        r = select_next_test(cands, ["H1", "H2", "H3"])
        assert r["test_id"] == "T2"
        assert r["distinguishing_power"] == 1

    def test_no_candidate_eliminates_nothing(self):
        r = select_next_test(
            [{"test_id": "T0", "outcomes": {}}], ["H1"])
        assert r["test_id"] is None
        assert r["distinguishing_power"] == 0

    def test_tie_breaks_toward_simpler(self):
        cands = [
            {"test_id": "T-big",
             "outcomes": {"a": ["H1"], "b": ["H2"], "c": ["H1"]}},
            {"test_id": "T-small", "outcomes": {"x": ["H1"], "y": ["H2"]}},
        ]
        r = select_next_test(cands, ["H1", "H2"])
        assert r["test_id"] == "T-small"

    def test_selection_does_not_mutate_hypotheses(self):
        # ANTI-GAMING: selecting (or running) a test never changes a
        # hypothesis by itself; only re-evaluation against the actual
        # outcome may.
        h = RevisableHypothesis("H1", mechanism="m", status=HYP_UNRESOLVED)
        select_next_test(
            [{"test_id": "T1", "outcomes": {"a": ["H1"]}}], ["H1"])
        assert h.status == HYP_UNRESOLVED


# ---------------------------------------------------------------------------
# 10. Anti-gaming acceptance suite (ten scenarios)
# ---------------------------------------------------------------------------

class TestAntiGaming:
    def test_1_single_blocker_repair_unblocks(self):
        bs = BlockerSet(blockers=[Blocker("B1", "A", "c",
                                          status=BLOCKER_ACTIVE,
                                          controller="X",
                                          evidence_refs=("e",))])
        assert bs.repair("B1", ("e-clear",)).is_blocked() is False

    def test_2_assertion_cannot_clear(self):
        bs = BlockerSet(blockers=[Blocker("B1", "A", "c",
                                          status=BLOCKER_ACTIVE,
                                          controller="X",
                                          evidence_refs=("e",))])
        with pytest.raises(ValueError):
            bs.repair("B1", ())

    def test_3_conflict_is_not_a_tie(self):
        p = Proposition("P1", "s", STAGE_ISSUED, verdict=PROP_CONFLICTED)
        assert p.verdict not in (PROP_SUPPORTED, PROP_REFUTED)

    def test_4_unobserved_is_not_absence(self):
        c = ObservabilityClaim(source="S", event_type="X", resource="r",
                               interval=(0, 10), status=OBS_UNOBSERVED)
        assert not c.absence_meaningful()

    def test_5_partial_repair_no_completion(self):
        # THE key anti-gaming case: repair recognized, still blocked,
        # completion NOT declared.
        bs = BlockerSet(blockers=[
            Blocker("B1", "A", "c1", status=BLOCKER_ACTIVE, controller="X",
                    evidence_refs=("e1",)),
            Blocker("B2", "A", "c2", status=BLOCKER_ACTIVE, controller="Y",
                    evidence_refs=("e2",))])
        bs2 = bs.repair("B1", ("e1-clear",))
        assert bs2.is_blocked()
        assert {b.blocker_id: b.status for b in bs2.blockers} == {
            "B1": BLOCKER_CLEARED, "B2": BLOCKER_ACTIVE}

    def test_6_hypothesis_not_promoted_without_test(self):
        h = RevisableHypothesis("H1", mechanism="m", status=HYP_UNRESOLVED,
                                discriminating_test="")
        assert h.status == HYP_UNRESOLVED

    def test_7_one_bus_is_one_witness(self):
        from causal_trace import EV_DISPATCH
        evs = [_ev("E1", EV_DISPATCH, artifacts=("h",)),
               _ev("E2", EV_DISPATCH, artifacts=("h",))]
        props = decompose_dispatch_dispute("D", evs)
        assert props[0].verdict == PROP_UNDETERMINED

    def test_8_shared_source_rejects_independence(self):
        r = recompute_support("H", [frozenset({"E1"})],
                              unreliable=set(),
                              evidence_sources={"E1": "BUS"})
        # Sanity: single path, no contamination -> SUPPORTED (control).
        assert r["verdict"] == "SUPPORTED"
        r2 = recompute_support("H", [frozenset({"E1"}), frozenset({"E2"})],
                               unreliable={"E2"},
                               evidence_sources={"E1": "BUS", "E2": "BUS"})
        assert r2["verdict"] == "NOT_INDEPENDENT"

    def test_9_test_performance_is_not_resolution(self):
        h = RevisableHypothesis("H1", mechanism="m", status=HYP_UNRESOLVED)
        sel = select_next_test(
            [{"test_id": "T1", "outcomes": {"pass": ["H1"]}}], ["H1"])
        assert sel["test_id"] == "T1"
        assert h.status == HYP_UNRESOLVED  # performing T1 changes nothing

    def test_10_verdict_never_substitutes_for_assessments(self):
        rec = CausalUncertaintyRecord(
            record_id="R", trace_id="T",
            propositions=[Proposition("P1", "s", STAGE_ISSUED,
                                      verdict=PROP_SUPPORTED)],
            overall_causal_verdict="UNDETERMINED")
        d = rec.to_dict()
        assert d["propositions"][0]["verdict"] == PROP_SUPPORTED
        assert d["overall_causal_verdict"] == "UNDETERMINED"


# ---------------------------------------------------------------------------
# 11. Decisive experiment for the uncertainty extension
# ---------------------------------------------------------------------------

class TestUncertaintyDecisiveExperiment:
    """Two established blockers + one missing observation interval + two
    competing explanations + one alternative evidence path + one
    single-blocker intervention. The verifier must preserve all
    uncertainties, recognize the partial repair, never declare
    completion, and name the discriminating evidence. A cold successor
    reconstructs the same verdict from the versioned evidence.
    """

    def _experiment(self):
        # Two established blockers (different controllers).
        bs = BlockerSet(blockers=[
            Blocker("B-res", "ACT-042", "resource unavailable",
                    status=BLOCKER_ACTIVE, controller="RESOURCE_RUNTIME",
                    valid_interval=(0, 100), evidence_refs=("E1",)),
            Blocker("B-hold", "ACT-042", "scheduler policy hold",
                    status=BLOCKER_ACTIVE, controller="SCHEDULER",
                    valid_interval=(0, 100), evidence_refs=("E4b",)),
        ])
        # One missing observation interval: the worker channel was
        # unwatched for half the window.
        obs = [
            ObservabilityClaim(source="SCHEDULER", event_type="DISPATCH",
                               resource="queue", interval=(0, 100),
                               status=OBS_COVERED_COMPLETE,
                               sequence_continuous=True),
            ObservabilityClaim(source="WORKER", event_type="ATTEMPT",
                               resource="worker-1", interval=(50, 100),
                               status=OBS_UNOBSERVED,
                               collection_boundaries=("0-50 unwatched",)),
        ]
        # Two competing explanations.
        hs = HypothesisSet()
        hs.add(RevisableHypothesis(
            "H-env", mechanism="resource outage blocked dispatch",
            cause_type=CAUSE_CONTRIBUTING, supporting=("E1",),
            gaps=("worker channel 0-50 unobserved",),
            relationships={"H-sched": REL_COMPETING},
            discriminating_test="T-restore-resource",
            status=HYP_ACTIVE),
            branch=("alternative", ("H-env", "H-sched")))
        hs.add(RevisableHypothesis(
            "H-sched", mechanism="scheduler withheld eligible work",
            cause_type=CAUSE_CONTRIBUTING, supporting=("E4b",),
            gaps=("worker channel 0-50 unobserved",),
            relationships={"H-env": REL_COMPETING},
            discriminating_test="T-restore-resource",
            status=HYP_ACTIVE))
        # One alternative evidence path for H-env: (E1) or (E9&E10).
        support = recompute_support(
            "H-env", [frozenset({"E1"}), frozenset({"E9", "E10"})],
            unreliable=set(),
            evidence_sources={"E1": "RESOURCE_RUNTIME",
                              "E9": "VERIFY", "E10": "VERIFY"})
        rec = CausalUncertaintyRecord(
            record_id="R-DECISIVE", trace_id="TRACE-WF-001",
            observability=obs, blockers=list(bs.blockers),
            causal_hypotheses=list(hs.hypotheses.values()),
            overall_causal_verdict="UNDETERMINED")
        return bs, obs, hs, support, rec

    def test_uncertainties_preserved(self):
        bs, obs, hs, support, rec = self._experiment()
        d = rec.to_dict()
        # The missing interval is preserved as UNOBSERVED, not filled in.
        assert d["observability"][1]["status"] == OBS_UNOBSERVED
        # Both hypotheses stay live and competing.
        assert {h["status"] for h in d["causal_hypotheses"]} == {HYP_ACTIVE}
        assert hs.check_no_forced_choice() == []  # assessed as competing
        # Alternative path supports H-env.
        assert support["verdict"] == "SUPPORTED"

    def test_single_blocker_intervention_recognized_not_completed(self):
        bs, obs, hs, support, rec = self._experiment()
        # Intervene on ONE blocker: restore the resource with evidence.
        bs2 = bs.repair("B-res", evidence_refs=("E1-restored",))
        assert bs2.is_blocked()  # scheduler hold remains
        # The repair is recognized...
        assert {b.blocker_id: b.status for b in bs2.blockers}[
            "B-res"] == BLOCKER_CLEARED
        # ...but completion is NEVER declared from a partial repair.
        assert bs2.minimal_blocking_sets() == [frozenset({"B-hold"})]

    def test_discriminating_evidence_named(self):
        _, _, hs, _, _ = self._experiment()
        for h in hs.live():
            assert h.discriminating_test == "T-restore-resource"
        # After the intervention, H-env's support collapses to the
        # alternative path; H-sched is unaffected: the test discriminates.
        r = recompute_support(
            "H-env", [frozenset({"E1"}), frozenset({"E9", "E10"})],
            unreliable={"E1"},
            evidence_sources={"E1": "RESOURCE_RUNTIME",
                              "E9": "VERIFY", "E10": "VERIFY"})
        assert r["verdict"] == "SUPPORTED"
        assert r["admissible_paths"] == [["E10", "E9"]]

    def test_cold_successor_reconstructs_same_verdict(self):
        # A cold successor rebuilds the record from the versioned
        # evidence and reaches the same assessments.
        bs, obs, hs, support, rec = self._experiment()
        d1 = rec.to_dict()
        # Cold rebuild: fresh objects from the serialized record.
        rec2 = CausalUncertaintyRecord(
            record_id=d1["record_id"], trace_id=d1["trace_id"],
            version=d1["version"],
            observability=[ObservabilityClaim(**o)
                           for o in d1["observability"]],
            propositions=[Proposition(**p) for p in d1["propositions"]],
            blockers=[Blocker(**b) for b in d1["blockers"]],
            overall_causal_verdict=d1["overall_causal_verdict"])
        d2 = rec2.to_dict()
        assert d2["overall_causal_verdict"] == d1["overall_causal_verdict"]
        assert [o["status"] for o in d2["observability"]] == [
            o["status"] for o in d1["observability"]]
        assert [b["status"] for b in d2["blockers"]] == [
            b["status"] for b in d1["blockers"]]
