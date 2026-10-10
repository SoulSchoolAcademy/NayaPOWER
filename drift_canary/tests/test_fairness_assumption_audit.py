"""Tests for the Fairness Assumption Audit Protocol (FAAP) (spec).

Every negative test carries a positive control. UNKNOWN stays UNKNOWN.
"""
import json

import pytest

from drift_canary.fairness_assumption_audit import (
    TARGET_PROPERTY_ID,
    Assumption,
    AssumptionManifest,
    AuditReceipt,
    BoundaryViolation,
    CircularityFinding,
    ControlBoundary,
    IndependenceFinding,
    Justification,
    Qualification,
    SensitivityEntry,
    adversarial_substitution,
    admits_recurring_eligibility,
    audit_circularity,
    audit_independence,
    audit_satisfiability,
    check_consistency,
    decisive_experiment,
    detect_semantic_equivalence,
    find_audit_lassos,
    is_starvation_lasso,
    minimize_assumptions,
    run_full_audit,
    sensitivity_report,
    validate_receipt,
    decide_qualification,
    CIRCULAR,
    NOT_CIRCULAR,
    NO_MASKING,
    MASKING_RISK,
    MINIMALITY_UNKNOWN,
    NEC_NECESSARY,
    NEC_REDUNDANT,
    NEC_UNRESOLVED,
    NEC_DOMAIN_CONSTRAINT_MISSING,
    SAT_PASS,
    SAT_UNSATISFIABLE,
    SAT_VACUOUS,
)


def env_boundary(condition="RESOURCE_AVAILABILITY"):
    return ControlBoundary("ENVIRONMENT", condition)


def sched_boundary(condition="QUEUE_SELECTION"):
    return ControlBoundary("SCHEDULER", condition)


def make_assumption(aid="A_TEST", predicate="GF(eligible(o))",
                    boundary=None, just_refs=("J1",), excluded=()):
    return Assumption(
        assumption_id=aid, revision=1, predicate=predicate,
        scope="audit model", owner="ENVIRONMENT",
        control_boundary=boundary or env_boundary(),
        justification_refs=just_refs, dependency_refs=(),
        counterexamples_excluded=excluded,
    )


def proto_justification(jid="J1", origin="RESOURCE_PROTOCOL",
                        depends_on=(), test=None):
    return Justification(jid, "FORMAL_GUARANTEE", origin, "scope",
                         depends_on, test)


# ---------------------------------------------------------------------------
# Boundary enforcement (bricks): enforced at REGISTRATION, not audit time.
# ---------------------------------------------------------------------------
class TestBoundary:
    def test_scheduler_controlled_rejected(self):
        m = AssumptionManifest()
        with pytest.raises(BoundaryViolation):
            m.register(make_assumption(boundary=sched_boundary()))

    def test_scheduler_influenced_rejected(self):
        m = AssumptionManifest()
        b = ControlBoundary("ENVIRONMENT", "RESOURCE_AVAILABILITY",
                            scheduler_influenced=True)
        with pytest.raises(BoundaryViolation):
            m.register(make_assumption(boundary=b))

    def test_temporary_ineligibility_rejected(self):
        # The scheduler making an obligation temporarily ineligible must
        # remain visible as a scheduler decision.
        m = AssumptionManifest()
        b = ControlBoundary("ENVIRONMENT", "TEMPORARY_INELIGIBILITY")
        with pytest.raises(BoundaryViolation):
            m.register(make_assumption(boundary=b))

    def test_environmental_accepted_positive_control(self):
        m = AssumptionManifest()
        a = m.register(make_assumption())
        assert m.assumptions[a.identity()] is a

    def test_duplicate_registration_rejected(self):
        m = AssumptionManifest()
        m.register(make_assumption())
        with pytest.raises(BoundaryViolation):
            m.register(make_assumption())


# ---------------------------------------------------------------------------
# Versioning (compass): content hashes, append-only revisions.
# ---------------------------------------------------------------------------
class TestVersioning:
    def test_manifest_sha_stable(self):
        m1, m2 = AssumptionManifest(), AssumptionManifest()
        m1.register(make_assumption())
        m2.register(make_assumption())
        assert m1.manifest_sha == m2.manifest_sha

    def test_revise_appends_never_edits(self):
        m = AssumptionManifest()
        old = m.register(make_assumption())
        new = m.revise(old, predicate="GF(serviced(o))")
        assert new.revision == 2
        assert new.supersedes == ("A_TEST", 1)
        assert m.assumptions[old.identity()].predicate == "GF(eligible(o))"
        assert m.manifest_sha != AssumptionManifest().manifest_sha

    def test_old_receipt_references_old_sha(self):
        m = AssumptionManifest()
        m.register(make_assumption())
        sha_v1 = m.manifest_sha
        old = m.assumptions["A_TEST#r1"]
        m.revise(old, scope="wider scope")
        assert m.manifest_sha != sha_v1  # new revision, new hash


# ---------------------------------------------------------------------------
# Justification classes carry honest limits.
# ---------------------------------------------------------------------------
class TestJustifications:
    def test_empirical_does_not_prove_infinite(self):
        j = Justification("J", "EMPIRICAL_EVIDENCE", "MONITORING", "s")
        assert "100" in j.honest_limit() or "infinite" in j.honest_limit()

    def test_formal_guarantee_scoped(self):
        j = Justification("J", "FORMAL_GUARANTEE", "PROTOCOL", "s")
        assert "protocol" in j.honest_limit().lower()

    def test_contract_not_runtime_proof(self):
        j = Justification("J", "AUTHORITATIVE_CONTRACT", "VENDOR", "s")
        assert "runtime" in j.honest_limit().lower()


# ---------------------------------------------------------------------------
# Gate 1 — independent justification.
# ---------------------------------------------------------------------------
class TestIndependence:
    def test_scheduler_self_report_rejected(self):
        # Acceptance: scheduler self-report as its own justification.
        a = make_assumption(just_refs=("J_SELF",))
        js = {"J_SELF": proto_justification("J_SELF",
                                            origin="SCHEDULER_UNDER_TEST")}
        f = audit_independence(a, js)
        assert not f.passed
        assert "EVIDENCE_FROM_SCHEDULER_UNDER_TEST" in f.flags

    def test_independent_protocol_passes_positive_control(self):
        a = make_assumption(just_refs=("J_PROTO",))
        js = {"J_PROTO": proto_justification("J_PROTO")}
        f = audit_independence(a, js)
        assert f.passed and f.flags == ()

    def test_reviewer_copied_author_expectation_flagged(self):
        a = make_assumption(just_refs=("J_REV",))
        js = {"J_REV": proto_justification(
            "J_REV", origin="REVIEWER_COPY_OF_AUTHOR_EXPECTATION")}
        f = audit_independence(a, js)
        assert "REVIEWER_COPIED_AUTHOR_EXPECTATION" in f.flags

    def test_different_reviewer_not_enough_when_same_test(self):
        # Independence is NOT established by "a different agent reviewed it":
        # two justifications sharing one originating test are flagged even
        # with different reviewers.
        a = make_assumption(just_refs=("J_A", "J_B"))
        js = {
            "J_A": proto_justification("J_A", origin="REVIEWER_ONE",
                                       test="T_ORIGIN"),
            "J_B": proto_justification("J_B", origin="REVIEWER_TWO",
                                       test="T_ORIGIN"),
        }
        f = audit_independence(a, js)
        assert "SHARED_ORIGINATING_TEST" in f.flags

    def test_distinct_originating_tests_pass_positive_control(self):
        a = make_assumption(just_refs=("J_A", "J_B"))
        js = {
            "J_A": proto_justification("J_A", test="T_ONE"),
            "J_B": proto_justification("J_B", test="T_TWO"),
        }
        f = audit_independence(a, js)
        assert f.passed

    def test_cycle_through_derived_conclusion_flagged(self):
        a = make_assumption(aid="A_X", just_refs=("J_CYC",))
        js = {"J_CYC": proto_justification("J_CYC", depends_on=("A_X",))}
        f = audit_independence(a, js)
        assert "CYCLE_THROUGH_DERIVED_CONCLUSION" in f.flags

    def test_indirect_dependence_on_target_flagged(self):
        a = make_assumption(just_refs=("J_1",))
        js = {
            "J_1": proto_justification("J_1", depends_on=("J_2",)),
            "J_2": proto_justification("J_2",
                                       depends_on=(TARGET_PROPERTY_ID,)),
        }
        f = audit_independence(a, js)
        assert "ASSUMPTION_DEPENDS_ON_TARGET" in f.flags

    def test_no_justification_at_all_flagged(self):
        a = make_assumption(just_refs=())
        f = audit_independence(a, {})
        assert not f.passed


# ---------------------------------------------------------------------------
# Gate 2 — satisfiability: consistency AND relevant behavior.
# ---------------------------------------------------------------------------
class TestSatisfiability:
    def test_contradictory_assumptions_unsatisfiable(self):
        a1 = make_assumption("A_1", predicate="GF(eligible(o))")
        a2 = make_assumption("A_2", predicate="NOT(GF(eligible(o)))")
        verdict, artifact = audit_satisfiability([a1, a2])
        assert verdict == SAT_UNSATISFIABLE
        assert "contradictory" in artifact["reason"]

    def test_consistent_pair_passes_positive_control(self):
        a1 = make_assumption("A_1", predicate="GF(eligible(o))")
        a2 = make_assumption("A_2", predicate="lawful_authorization(o)")
        verdict, artifact = audit_satisfiability([a1, a2])
        assert verdict == SAT_PASS
        assert artifact["consistency_witness"]["cycle_len"] > 0

    def test_overconstrained_environment_vacuous(self):
        # Acceptance: assumptions admit no recurring eligibility.
        a = make_assumption("A_CONT",
                            predicate="GF(continuous_eligibility(o))")
        verdict, artifact = audit_satisfiability([a])
        assert verdict == SAT_VACUOUS
        assert "intermittent" in artifact["reason"]

    def test_honest_flicker_environment_passes_positive_control(self):
        a = make_assumption("A_RECURS", predicate="GF(eligible(o))")
        verdict, _ = audit_satisfiability([a])
        assert verdict == SAT_PASS

    def test_relevant_behavior_witness_has_both_phases(self):
        ok, wit = admits_recurring_eligibility(False)
        assert ok
        pat = [s.elig for s in wit.prefix + wit.cycle]
        assert True in pat and False in pat


# ---------------------------------------------------------------------------
# Gate 3 — minimal sufficiency.
# ---------------------------------------------------------------------------
class TestMinimization:
    def test_redundant_assumption_removed(self):
        # Acceptance: redundant assumption removed without losing proof.
        a_cont = make_assumption("A_CONT",
                                 predicate="GF(continuous_eligibility(o))")
        a_auth = make_assumption("A_AUTH",
                                 predicate="lawful_authorization(o)")
        r = minimize_assumptions([a_cont, a_auth], policy="FAIR")
        assert r["status"] == "COMPLETE"
        assert r["A_AUTH#r1"] == NEC_REDUNDANT

    def test_necessary_assumption_recorded(self):
        # Acceptance: removal exposes genuine starvation -> necessary
        # RELATIVE to the model (here: the unfair scheduler's "proof"
        # depends on the masking assumption — the diagnostic signal).
        a_cont = make_assumption("A_CONT",
                                 predicate="GF(continuous_eligibility(o))")
        r = minimize_assumptions([a_cont], policy="FLICKER_UNFAIR")
        assert r["A_CONT#r1"] == NEC_NECESSARY

    def test_timeout_is_unknown_not_pass(self):
        # Acceptance: checker times out during minimization.
        a = make_assumption()
        r = minimize_assumptions([a], step_budget=0)
        assert r["status"] == MINIMALITY_UNKNOWN
        assert r["status"] != "COMPLETE"

    def test_physically_impossible_counterexample_flagged(self):
        # The counterexample lives entirely outside the declared domain:
        # inspect the missing constraint, don't declare necessity.
        a_cont = make_assumption("A_CONT",
                                 predicate="GF(continuous_eligibility(o))")
        r = minimize_assumptions(
            [a_cont], policy="FLICKER_UNFAIR",
            domain_constraints=(lambda s: s.era == 1,))
        assert r["A_CONT#r1"] == NEC_DOMAIN_CONSTRAINT_MISSING

    def test_minimality_is_relative(self):
        a1 = make_assumption("A_1")
        a2 = make_assumption("A_2")
        r = minimize_assumptions([a1, a2], policy="FAIR")
        assert r["status"] == "COMPLETE"
        # The claim is inclusion-minimal relative to the declared model
        # and vocabulary — never "globally minimal".
        assert set(r["minimal_set"]) <= {"A_1#r1", "A_2#r1"}


# ---------------------------------------------------------------------------
# Gate 4a — non-circularity.
# ---------------------------------------------------------------------------
class TestCircularity:
    def test_hidden_semantic_dependency_circular(self):
        # "Every eligible queue entry is eventually removed" where
        # removal only follows service == the desired property renamed.
        a = make_assumption("A_RM", predicate="GF removed(o)")
        js = {"J1": proto_justification("J1")}
        f = audit_circularity(a, js,
                              domain_rules=("removed(o) -> serviced(o)",))
        assert f.verdict == CIRCULAR
        assert "different words" in f.detail

    def test_clean_assumption_not_circular_positive_control(self):
        a = make_assumption("A_RES", predicate="GF(resource_available(o))")
        js = {"J1": proto_justification("J1")}
        f = audit_circularity(a, js,
                              domain_rules=("removed(o) -> serviced(o)",))
        assert f.verdict == NOT_CIRCULAR

    def test_provenance_cycle_circular(self):
        a = make_assumption(aid="A_X", just_refs=("J_CYC",))
        js = {"J_CYC": proto_justification("J_CYC", depends_on=("A_X",))}
        f = audit_circularity(a, js)
        assert f.verdict == CIRCULAR

    def test_never_serviced_as_axiom_is_circular(self):
        # The checker must NEVER receive eventually_serviced(o) as an
        # environmental axiom: that is assuming the result.
        a = make_assumption("A_SVC", predicate="GF serviced(o)")
        js = {"J1": proto_justification("J1")}
        f = audit_circularity(a, js, target_consequent_atom="serviced(o)")
        assert f.verdict == CIRCULAR


# ---------------------------------------------------------------------------
# Gate 4b — adversarial scheduler substitution.
# ---------------------------------------------------------------------------
class TestAdversarial:
    def test_unfair_passes_due_to_assumptions_masking(self):
        # Acceptance: deliberately unfair scheduler passes because of the
        # assumptions -> flag masking risk, reject unqualified PASS.
        a_cont = make_assumption("A_CONT",
                                 predicate="GF(continuous_eligibility(o))")
        r = adversarial_substitution([a_cont])
        assert r["verdict"] == MASKING_RISK
        assert r["per_policy"]["FLICKER_UNFAIR"] == "STARVATION_IMPOSSIBLE"

    def test_honest_assumptions_no_masking_positive_control(self):
        a = make_assumption("A_RECURS", predicate="GF(eligible(o))")
        r = adversarial_substitution([a])
        assert r["verdict"] == NO_MASKING
        assert r["per_policy"]["FLICKER_UNFAIR"] == "STARVATION_POSSIBLE"

    def test_masking_is_specific_not_blanket(self):
        # A_CONT masks the flicker-unfair scheduler but cannot mask a
        # scheduler that never serves: masking analysis is specific.
        a_cont = make_assumption("A_CONT",
                                 predicate="GF(continuous_eligibility(o))")
        r = adversarial_substitution([a_cont],
                                     unfair_policies=("NEVER",))
        assert r["per_policy"]["NEVER"] == "STARVATION_POSSIBLE"


# ---------------------------------------------------------------------------
# Sensitivity report: disappearance is never proof of repair.
# ---------------------------------------------------------------------------
class TestSensitivity:
    def test_remove_reveals_counterexample(self):
        a_cont = make_assumption("A_CONT",
                                 predicate="GF(continuous_eligibility(o))")
        a_rec = make_assumption("A_RECURS", predicate="GF(eligible(o))")
        e = sensitivity_report([a_cont], [a_rec], "REMOVE", a_cont,
                               policy="FLICKER_UNFAIR")
        assert isinstance(e, SensitivityEntry)
        assert e.counterexamples_added > 0
        assert "exposed" in e.interpretation

    def test_add_conceals_counterexample_warns(self):
        a_cont = make_assumption("A_CONT",
                                 predicate="GF(continuous_eligibility(o))")
        a_rec = make_assumption("A_RECURS", predicate="GF(eligible(o))")
        e = sensitivity_report([a_rec], [a_cont], "ADD", a_cont,
                               policy="FLICKER_UNFAIR")
        assert e.counterexamples_removed > 0
        assert "NOT proof" in e.interpretation

    def test_no_change_no_drift(self):
        a_rec = make_assumption("A_RECURS", predicate="GF(eligible(o))")
        e = sensitivity_report([a_rec], [a_rec], "WEAKEN", a_rec,
                               policy="FAIR")
        assert e.counterexamples_removed == 0
        assert e.counterexamples_added == 0


# ---------------------------------------------------------------------------
# Receipt validation: every PASS names its artifact.
# ---------------------------------------------------------------------------
def example_receipt():
    return {
        "audit_id": "FAAP-001",
        "target_property": "STRONG_FAIRNESS",
        "scheduler_model_sha": "exact-model-sha",
        "assumption_manifest_sha": "exact-manifest-sha",
        "scheduler_version": "sched-v3",
        "obligation_class": "ACT",
        "environment": "audit-model",
        "model_abstraction": "explicit-state-v1",
        "assumptions": [
            {"id": "RESOURCE_RECURS#r1", "owner": "RESOURCE_RUNTIME",
             "classification": "ENVIRONMENT",
             "independent_justification": "PENDING",
             "satisfiable": True,
             "satisfiability_witness": {"prefix_len": 1, "cycle_len": 2},
             "necessity": "UNDETERMINED",
             "circularity": "NOT_YET_CHECKED"},
        ],
        "audit_gates": {
            "independence": "PENDING", "satisfiability": "PASS",
            "non_vacuity": "PENDING", "minimality": "PENDING",
            "non_circularity": "PENDING", "adversarial_scheduler": "PENDING",
        },
        "gate_artifacts": {
            "satisfiability": {"witness": "lasso-001",
                               "reproduce": "find_audit_lassos('NEVER', False)"},
        },
        "qualification": "UNPROVEN",
    }


class TestReceipt:
    def test_honest_receipt_validates(self):
        valid, problems = validate_receipt(example_receipt())
        assert valid, problems

    def test_bare_pass_without_artifact_rejected(self):
        r = example_receipt()
        r["audit_gates"]["independence"] = "PASS"  # no artifact attached
        valid, problems = validate_receipt(r)
        assert not valid
        assert any("independence" in p for p in problems)

    def test_bare_satisfiable_true_rejected(self):
        r = example_receipt()
        del r["assumptions"][0]["satisfiability_witness"]
        valid, problems = validate_receipt(r)
        assert not valid
        assert any("satisfiable" in p for p in problems)

    def test_bare_pass_qualification_rejected(self):
        r = example_receipt()
        r["qualification"] = "PASS"
        valid, problems = validate_receipt(r)
        assert not valid
        assert any("bare PASS" in p for p in problems)

    def test_receipt_round_trips_through_json(self):
        r = example_receipt()
        assert json.loads(json.dumps(r))["audit_id"] == "FAAP-001"


# ---------------------------------------------------------------------------
# Qualification: conditional, versioned, never bare.
# ---------------------------------------------------------------------------
class TestQualification:
    def test_render_names_everything(self):
        q = Qualification("QUALIFIED_IN_MODEL_SCOPE", "sched-v3", "ACT",
                          "prod-eu", "abc123", "explicit-state-v1",
                          ("FAAP-001",))
        text = q.render()
        for token in ("sched-v3", "ACT", "prod-eu", "abc123",
                      "explicit-state-v1", "FAAP-001"):
            assert token in text
        assert "requalify" in text  # environment change -> requalify

    def test_three_of_four_is_failure(self):
        gates = {"independence": False, "satisfiability": SAT_PASS,
                 "minimality": "COMPLETE", "non_circularity": NOT_CIRCULAR,
                 "adversarial": NO_MASKING}
        assert decide_qualification(gates) != "QUALIFIED_IN_MODEL_SCOPE"

    def test_unknown_stays_unknown(self):
        gates = {"independence": True, "satisfiability": SAT_PASS,
                 "minimality": MINIMALITY_UNKNOWN,
                 "non_circularity": NOT_CIRCULAR, "adversarial": NO_MASKING}
        assert decide_qualification(gates) == "UNPROVEN"

    def test_all_gates_qualifies_in_scope(self):
        gates = {"independence": True, "satisfiability": SAT_PASS,
                 "minimality": "COMPLETE", "non_circularity": NOT_CIRCULAR,
                 "adversarial": NO_MASKING}
        assert decide_qualification(gates) == "QUALIFIED_IN_MODEL_SCOPE"

    def test_masking_blocks_qualification(self):
        gates = {"independence": True, "satisfiability": SAT_PASS,
                 "minimality": "COMPLETE", "non_circularity": NOT_CIRCULAR,
                 "adversarial": MASKING_RISK}
        assert decide_qualification(gates) == "MASKING_RISK"


# ---------------------------------------------------------------------------
# The first decisive experiment.
# ---------------------------------------------------------------------------
class TestDecisiveExperiment:
    def test_conceal_reveal_repair(self):
        exp = decisive_experiment()
        assert exp["step1_concealed_under_A_CONT"] is True
        assert exp["step2_counterexample_reappears_without_A_CONT"] is True
        assert exp["step2_starvation_lassos"] >= 1
        assert exp["step2_witness"] is not None
        assert exp["step3_repaired_scheduler_no_starvation"] is True
        assert exp["step3_recurring_eligibility_served"] is True
        assert exp["progress_on_service_separate"] is True


# ---------------------------------------------------------------------------
# The full pipeline (magnifier): run_full_audit.
# ---------------------------------------------------------------------------
def honest_manifest():
    return [
        make_assumption("A_RECURS", predicate="GF(eligible(o))",
                        just_refs=("J_PROTO",)),
        make_assumption("A_AUTH", predicate="lawful_authorization(o)",
                        boundary=env_boundary("LAWFUL_AUTHORIZATION"),
                        just_refs=("J_CONTRACT",)),
    ]


def honest_justifications():
    return {
        "J_PROTO": proto_justification("J_PROTO"),
        "J_CONTRACT": Justification("J_CONTRACT", "AUTHORITATIVE_CONTRACT",
                                    "SERVICE_VENDOR", "bounded availability"),
    }


class TestFullAudit:
    def test_honest_set_qualifies_in_scope(self):
        receipt = run_full_audit(
            "FAAP-TEST-001", honest_manifest(), honest_justifications(),
            "sched-v3", "ACT", "audit-model", "explicit-state-v1")
        assert "QUALIFIED_IN_MODEL_SCOPE" in receipt.qualification
        valid, problems = validate_receipt(receipt.to_dict())
        assert valid, problems

    def test_masking_set_rejected(self):
        # A_RUNLEN ("eligible runs last >= 2 rounds") is satisfiable and
        # non-vacuous — yet it masks the flicker-unfair scheduler, which
        # serves 2-round runs but starves single-round windows.
        a_runlen = make_assumption(
            "A_RUNLEN", predicate="eligible_runs_last_2_rounds(o)",
            just_refs=("J_HIST",))
        js = {"J_HIST": Justification("J_HIST", "EMPIRICAL_EVIDENCE",
                                      "MONITORING", "observed run lengths")}
        receipt = run_full_audit(
            "FAAP-TEST-002", [a_runlen], js,
            "sched-v3", "ACT", "audit-model", "explicit-state-v1")
        assert "MASKING_RISK" in receipt.qualification
        assert receipt.audit_gates["adversarial_scheduler"] == "FAIL"

    def test_vacuous_set_rejected_before_adversarial(self):
        # A_CONT alone cannot represent recurring eligibility: Gate 2
        # rejects it as VACUOUS_FOR_TARGET before the adversarial gate.
        a_cont = make_assumption("A_CONT",
                                 predicate="GF(continuous_eligibility(o))",
                                 just_refs=("J_HIST",))
        js = {"J_HIST": Justification("J_HIST", "EMPIRICAL_EVIDENCE",
                                      "MONITORING", "100 uptimes")}
        receipt = run_full_audit(
            "FAAP-TEST-002b", [a_cont], js,
            "sched-v3", "ACT", "audit-model", "explicit-state-v1")
        assert "VACUOUS_FOR_TARGET" in receipt.qualification

    def test_pipeline_emits_all_eight_artifacts(self):
        receipt = run_full_audit(
            "FAAP-TEST-003", honest_manifest(), honest_justifications(),
            "sched-v3", "ACT", "audit-model", "explicit-state-v1")
        d = receipt.to_dict()
        for gate in ("independence", "satisfiability", "non_vacuity",
                     "minimality", "non_circularity",
                     "adversarial_scheduler"):
            assert gate in d["gate_artifacts"], gate

    def test_old_receipt_does_not_cover_new_scheduler(self):
        # (compass) qualification names the scheduler version AND the
        # model SHA: a new scheduler version needs a new receipt.
        r1 = run_full_audit("FAAP-V3", honest_manifest(),
                            honest_justifications(), "sched-v3", "ACT",
                            "audit-model", "explicit-state-v1")
        r2 = run_full_audit("FAAP-V4", honest_manifest(),
                            honest_justifications(), "sched-v4", "ACT",
                            "audit-model", "explicit-state-v1")
        assert "sched-v3" in r1.qualification
        assert "sched-v4" in r2.qualification
        assert "sched-v3" not in r2.qualification
