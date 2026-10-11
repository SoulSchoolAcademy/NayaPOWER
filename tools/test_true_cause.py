"""Adversarial tests for UD-09 true_cause.py.

Acceptance gate: same symptoms produce different verdicts from different
evidence; swapped labels don't move verdicts; corrupted logs are rejected
or downgraded to uncertainty; a fresh verifier reproduces conclusions
without trusting original agents.
"""
import pytest

from true_cause import (
    CORRELATION_NOT_CAUSATION,
    INSUFFICIENT_LINEAGE,
    INSUFFICIENT_OBSERVABLE_EVIDENCE,
    LABEL_INPUT_REFUSED,
    NO_COUNTERFACTUAL,
    NO_INDEPENDENT_REPRODUCTION,
    NO_MECHANISM,
    SELF_CERTIFICATION,
    CausalCase,
    CausalRefusal,
    ComponentReport,
    EvidenceConstructionError,
    EvidenceEvent,
    FailureCase,
    LadderPromotionError,
    Observation,
    ObservationLadder,
    ResponsibilityRecord,
    TrueCauseVerifier,
    check_counterfactual,
    check_mechanism,
    check_reproduction,
    establish_caused_by,
    make_event,
)

SYMPTOMS = ("workflow did not complete",)


def env_down_events():
    return [
        make_event("e1", 1, "db_probe", "env_witness",
                   {"resource_id": "DB-CONN", "resource_available": False}),
        make_event("e2", 2, "db_probe2", "env_witness2",
                   {"resource_id": "DB-CONN", "resource_available": False}),
    ]


def scheduler_starved_events():
    return [
        make_event("e1", 1, "sched_log", "sched_auditor",
                   {"obligation": "ACT-042", "dispatched": False}),
        make_event("e2", 2, "queue_probe", "queue_auditor",
                   {"obligation": "ACT-042", "queue_depth": 3}),
    ]


def worker_stalled_events():
    return [
        make_event("e1", 1, "conn_meter", "service_auditor",
                   {"obligation": "ACT-042", "adequate_service": True}),
        make_event("e2", 2, "progress_log", "progress_auditor",
                   {"obligation": "ACT-042", "verified_advancement": False}),
    ]


def resp(controller, by=("e1", "e2")):
    return [ResponsibilityRecord("db-connection-for-ACT-042",
                                controller, version=1,
                                established_by=by, lamport=3)]


# ---------------------------------------------------------------------------
# 1. Same symptoms, different evidence -> different verdicts
# ---------------------------------------------------------------------------

def test_same_symptoms_env_down():
    v = TrueCauseVerifier().verify(FailureCase(
        "c-env", SYMPTOMS, tuple(env_down_events()), tuple(resp("ENVIRONMENT"))))
    assert v.verdict == "ENVIRONMENT_BLOCKER"
    assert v.controller == "ENVIRONMENT"


def test_same_symptoms_scheduler_starved():
    v = TrueCauseVerifier().verify(FailureCase(
        "c-sched", SYMPTOMS, tuple(scheduler_starved_events()),
        tuple(resp("SCHEDULER"))))
    assert v.verdict == "SCHEDULER_STARVATION"


def test_same_symptoms_worker_stalled():
    v = TrueCauseVerifier().verify(FailureCase(
        "c-worker", SYMPTOMS, tuple(worker_stalled_events()),
        tuple(resp("WORKER"))))
    assert v.verdict == "WORKER_NONPROGRESS"


def test_verdicts_differ_across_evidence():
    digests = set()
    for cid, ev, ctl in (("a", env_down_events(), "ENVIRONMENT"),
                         ("b", scheduler_starved_events(), "SCHEDULER"),
                         ("c", worker_stalled_events(), "WORKER")):
        v = TrueCauseVerifier().verify(
            FailureCase(cid, SYMPTOMS, tuple(ev), tuple(resp(ctl))))
        digests.add(v.digest)
    assert len(digests) == 3  # same symptoms, three different verdicts


# ---------------------------------------------------------------------------
# 2. Label swaps leave verdicts byte-identical
# ---------------------------------------------------------------------------

def _case_with_labels(labels):
    return FailureCase("c-label", SYMPTOMS, tuple(env_down_events()),
                       tuple(resp("ENVIRONMENT")),
                       narrative_labels=tuple(labels))


def test_label_swap_byte_identical():
    v1 = TrueCauseVerifier().verify(_case_with_labels(
        [("WORKER", "DATABASE_UNAVAILABLE"), ("SCHEDULER", "WORKER_FAULT")]))
    v2 = TrueCauseVerifier().verify(_case_with_labels(
        [("ENVIRONMENT", "SCHEDULER_STARVATION"), ("WORKER", "ALL_FINE")]))
    v3 = TrueCauseVerifier().verify(_case_with_labels([]))
    assert v1.digest == v2.digest == v3.digest
    assert v1.verdict == "ENVIRONMENT_BLOCKER"


def test_narrative_cannot_override_controller():
    # Every component blames the worker; controller + evidence say scheduler.
    v = TrueCauseVerifier().verify(FailureCase(
        "c-blame", SYMPTOMS, tuple(scheduler_starved_events()),
        tuple(resp("SCHEDULER")),
        narrative_labels=(("WORKER", "SCHEDULER_STARVATION"),
                          ("SCHEDULER", "WORKER_NONPROGRESS"),
                          ("ENVIRONMENT", "WORKER_FAULT"))))
    assert v.verdict == "SCHEDULER_STARVATION"
    assert v.controller == "SCHEDULER"


def test_verifier_accepts_no_label_like_inputs():
    with pytest.raises(EvidenceConstructionError) as exc:
        make_event("eX", 1, "p", "o", {"label": "DATABASE_UNAVAILABLE"})
    assert LABEL_INPUT_REFUSED in str(exc.value)
    with pytest.raises(EvidenceConstructionError):
        make_event("eX", 1, "p", "o", {"blame": "worker"})


# ---------------------------------------------------------------------------
# 3. Corrupted logs rejected or downgraded to uncertainty
# ---------------------------------------------------------------------------

def test_self_certification_is_construction_error():
    with pytest.raises(EvidenceConstructionError) as exc:
        make_event("eX", 1, "worker", "worker", {"x": 1})
    assert SELF_CERTIFICATION in str(exc.value)


def test_hash_mismatch_rejected():
    with pytest.raises(EvidenceConstructionError) as exc:
        EvidenceEvent("eX", 1, "p", "o", {"x": 1},
                      "0" * 64, {"event_id": "eX"})
    assert "HASH_MISMATCH" in str(exc.value)


def test_missing_attestation_rejected():
    import hashlib, json
    claim = {"x": 1}
    h = hashlib.sha256(
        json.dumps(claim, sort_keys=True,
                   separators=(",", ":")).encode()).hexdigest()
    with pytest.raises(EvidenceConstructionError) as exc:
        EvidenceEvent("eX", 1, "p", "o", claim, h, {})
    assert "MISSING_ATTESTATION" in str(exc.value)


def test_no_evidence_downgrades_to_undetermined():
    v = TrueCauseVerifier().verify(FailureCase("c-empty", SYMPTOMS, (),
                                               tuple(resp("ENVIRONMENT"))))
    assert v.verdict == "BOUNDARY_UNDETERMINED"
    assert INSUFFICIENT_OBSERVABLE_EVIDENCE in v.reason


def test_evidence_not_corroborating_controller_downgrades():
    # Controller says ENVIRONMENT but evidence shows nothing about resources.
    v = TrueCauseVerifier().verify(FailureCase(
        "c-mismatch", SYMPTOMS,
        tuple([make_event("e1", 1, "p", "o", {"unrelated": True})]),
        tuple(resp("ENVIRONMENT"))))
    assert v.verdict == "BOUNDARY_UNDETERMINED"


# ---------------------------------------------------------------------------
# 4. Fresh verifier reproduces without trusting original agents
# ---------------------------------------------------------------------------

def test_fresh_verifier_byte_identical():
    case = FailureCase("c-fresh", SYMPTOMS, tuple(worker_stalled_events()),
                       tuple(resp("WORKER")))
    d1 = TrueCauseVerifier().verify(case).digest
    d2 = TrueCauseVerifier().verify(case).digest  # fresh instance
    assert d1 == d2


def test_digest_deterministic_across_event_order():
    ev = worker_stalled_events()
    c1 = FailureCase("c-ord", SYMPTOMS, tuple(ev), tuple(resp("WORKER")))
    c2 = FailureCase("c-ord", SYMPTOMS, tuple(reversed(ev)),
                     tuple(resp("WORKER")))
    assert TrueCauseVerifier().verify(c1).digest == \
        TrueCauseVerifier().verify(c2).digest


# ---------------------------------------------------------------------------
# 5. The three causal checks
# ---------------------------------------------------------------------------

def causal_events():
    return [
        make_event("m1", 1, "mechanism_probe", "mech_auditor",
                   {"link": "A->B", "observed": True}),
        make_event("c1", 2, "control_arm", "control_auditor",
                   {"cause_absent": True, "effect_absent": True}),
        make_event("r1", 3, "repro_lab", "repro_auditor",
                   {"link": "A->B", "reproduced": True}),
    ]


def full_case():
    return CausalCase("config_push", "outage",
                      "config push exhausted connection pool; pool metrics "
                      "show saturation 40s after push",
                      mechanism_evidence=("m1",),
                      counterfactual_evidence=("c1",),
                      reproduction_evidence=("r1",))


def test_caused_by_all_three_checks():
    by_id = {e.event_id: e for e in causal_events()}
    edge = establish_caused_by(full_case(), by_id)
    assert edge["edge"] == "CAUSED_BY"


def test_ordering_is_not_causation_no_mechanism():
    by_id = {e.event_id: e for e in causal_events()}
    case = CausalCase("deploy", "outage", "",  # no mechanism stated
                      mechanism_evidence=(), counterfactual_evidence=("c1",),
                      reproduction_evidence=("r1",))
    with pytest.raises(CausalRefusal) as exc:
        establish_caused_by(case, by_id)
    assert exc.value.code == NO_MECHANISM


def test_mechanism_without_evidence_refused():
    by_id = {e.event_id: e for e in causal_events()}
    case = CausalCase("deploy", "outage", "deploy broke it, trust me",
                      mechanism_evidence=(),
                      counterfactual_evidence=("c1",),
                      reproduction_evidence=("r1",))
    with pytest.raises(CausalRefusal) as exc:
        check_mechanism(case, by_id)
    assert exc.value.code == NO_MECHANISM


def test_missing_counterfactual_refused():
    by_id = {e.event_id: e for e in causal_events()}
    case = CausalCase("x", "y", "mechanism here",
                      mechanism_evidence=("m1",),
                      counterfactual_evidence=(),
                      reproduction_evidence=("r1",))
    with pytest.raises(CausalRefusal) as exc:
        check_counterfactual(case, by_id)
    assert exc.value.code == NO_COUNTERFACTUAL


def test_missing_reproduction_refused():
    by_id = {e.event_id: e for e in causal_events()}
    case = CausalCase("x", "y", "mechanism here",
                      mechanism_evidence=("m1",),
                      counterfactual_evidence=("c1",),
                      reproduction_evidence=())
    with pytest.raises(CausalRefusal) as exc:
        check_reproduction(case, by_id)
    assert exc.value.code == NO_INDEPENDENT_REPRODUCTION


def test_reproduction_sharing_lineage_refused():
    events = causal_events() + [
        make_event("r2", 4, "mechanism_probe", "other_auditor",
                   {"link": "A->B", "reproduced": True}),
    ]
    by_id = {e.event_id: e for e in events}
    case = CausalCase("x", "y", "mechanism here",
                      mechanism_evidence=("m1",),
                      counterfactual_evidence=("c1",),
                      reproduction_evidence=("r2",))  # same producer as m1
    with pytest.raises(CausalRefusal) as exc:
        check_reproduction(case, by_id)
    assert exc.value.code == NO_INDEPENDENT_REPRODUCTION


# ---------------------------------------------------------------------------
# 6. The observation ladder
# ---------------------------------------------------------------------------

def ladder_events():
    return [
        make_event("o1", 1, "probe_a", "auditor_a", {"f": 1}),
        make_event("o2", 2, "probe_b", "auditor_b", {"f": 1}),
    ]


def test_full_ladder_promotion():
    events = ladder_events()
    lad = ObservationLadder(events)
    obs = Observation("obs1", ("o1", "o2"))
    obs = lad.promote(obs, "AUTHENTICATED")
    assert obs.rung == "AUTHENTICATED"
    obs = lad.promote(obs, "INDEPENDENTLY_CORROBORATED")
    assert obs.rung == "INDEPENDENTLY_CORROBORATED"


def test_rung_skip_refused():
    lad = ObservationLadder(ladder_events())
    obs = Observation("obs1", ("o1", "o2"))
    with pytest.raises(LadderPromotionError) as exc:
        lad.promote(obs, "INDEPENDENTLY_CORROBORATED")
    assert "RUNG_SKIP_REFUSED" in str(exc.value)


def test_shared_lineage_not_corroboration():
    events = [
        make_event("o1", 1, "probe_a", "auditor_a", {"f": 1}),
        make_event("o2", 2, "probe_a", "auditor_b", {"f": 1}),  # same producer
    ]
    lad = ObservationLadder(events)
    obs = lad.promote(Observation("obs1", ("o1", "o2")), "AUTHENTICATED")
    with pytest.raises(LadderPromotionError) as exc:
        lad.promote(obs, "INDEPENDENTLY_CORROBORATED")
    assert INSUFFICIENT_LINEAGE in str(exc.value)


def test_correlation_never_causally_qualified():
    events = causal_events()
    lad = ObservationLadder(events)
    obs = Observation("obs1", ("m1", "c1"), rung="INDEPENDENTLY_CORROBORATED",
                      edge_type="CORRELATES_WITH")
    with pytest.raises(LadderPromotionError) as exc:
        lad.promote(obs, "CAUSALLY_QUALIFIED", causal_case=full_case())
    assert CORRELATION_NOT_CAUSATION in str(exc.value)


def test_causal_qualification_requires_three_checks():
    events = causal_events()
    lad = ObservationLadder(events)
    obs = Observation("obs1", ("m1", "c1", "r1"),
                      rung="INDEPENDENTLY_CORROBORATED", edge_type="NONE")
    # No causal case supplied -> refused
    with pytest.raises(LadderPromotionError):
        lad.promote(obs, "CAUSALLY_QUALIFIED")
    # Failing causal case -> refused with the check's code
    bad = CausalCase("x", "y", "mech", ("m1",), (), ("r1"))
    with pytest.raises(CausalRefusal) as exc:
        lad.promote(obs, "CAUSALLY_QUALIFIED", causal_case=bad)
    assert exc.value.code == NO_COUNTERFACTUAL
    # Full case -> qualified with CAUSED_BY edge
    done = lad.promote(obs, "CAUSALLY_QUALIFIED", causal_case=full_case())
    assert done.rung == "CAUSALLY_QUALIFIED"
    assert done.edge_type == "CAUSED_BY"


# ---------------------------------------------------------------------------
# 7. Fourth ownership domain
# ---------------------------------------------------------------------------

def test_orchestrator_domain():
    events = [make_event("e1", 1, "spec_checker", "spec_auditor",
                         {"condition": "run-on-no-hardware",
                          "condition_impossible": True})]
    v = TrueCauseVerifier().verify(FailureCase(
        "c-orch", SYMPTOMS, tuple(events), tuple(resp("ORCHESTRATOR"))))
    assert v.verdict == "ORCHESTRATOR_MISCONFIGURATION"
    assert v.controller == "ORCHESTRATOR"


def test_invalid_controller_rejected():
    with pytest.raises(ValueError):
        ResponsibilityRecord("cond", "DATABASE")


def test_latest_responsibility_version_decisive():
    v = TrueCauseVerifier().verify(FailureCase(
        "c-ver", SYMPTOMS, tuple(scheduler_starved_events()),
        (ResponsibilityRecord("c", "WORKER", version=1,
                              established_by=("e1",), lamport=1),
         ResponsibilityRecord("c", "SCHEDULER", version=2,
                              established_by=("e1",), lamport=2))))
    assert v.controller == "SCHEDULER"
    assert v.verdict == "SCHEDULER_STARVATION"
