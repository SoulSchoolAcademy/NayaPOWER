"""SN-0808 AER-LIVE-2 — Bounded Recovery Liveness Law: the evidence ladder that
turns a timeout into a verdict. Every negative test gets a positive control.

HONEST SCOPE: contract extension + harness demonstration; no production
service bound validated; AER-LIVE-2 guarantees not production-proven.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from revocation_linearization import (
    LIVENESS_CLAIMS, SERVICE_EVIDENCE_KINDS, PROGRESS_EVIDENCE_KINDS,
    observable_links, track_fairness_debt, check_service_bound,
    check_progress_bound, check_disposition_bound, BOUND_ASSUMPTIONS,
    check_bound_assumptions, compose_bounds, BOUNDED_VERDICTS,
    ASSURANCE_LEVELS, bounded_verdict, BOUNDED_EVIDENCE_PACKET,
    verify_bounded_packet, lab_six_round_example, live_bl_suite, aer_live_002,
)

SVC = {"kind": "ACKNOWLEDGMENT", "evidence": "ack-1"}

# L2-01: four claims separated, each with its own proof burden. (+)
def test_l2_01_four_claims_separated():
    assert set(LIVENESS_CLAIMS) == {"safety", "scheduling_fairness",
                                    "bounded_progress", "task_completion"}
    for claim, burden in LIVENESS_CLAIMS.items():
        assert burden, claim

# L2-02: E_o precise — safety hold ⇒ not enabled ⇒ not starvation. (-)
def test_l2_02_safety_hold_is_not_starvation():
    l = observable_links({"law_permits": True, "dependencies_ready": True,
                          "resources_available": True, "safety_hold": True})
    assert not l["E_o"]
    l2 = observable_links({"law_permits": True, "dependencies_ready": True,
                           "resources_available": True, "safety_hold": False})
    assert l2["E_o"]  # (+) genuine enabling is detected

# L2-03: S_o precise — dispatch alone never counts. (-)
def test_l2_03_dispatch_alone_is_not_service():
    l = observable_links({"service_kind": "DISPATCHED",
                          "service_evidence": None})
    assert not l["S_o"]
    l2 = observable_links({"service_kind": "LEASE",
                           "service_evidence": "lease-1"})
    assert l2["S_o"]  # (+) leased service counts

# L2-04: P_o precise — heartbeats never count. (-)
def test_l2_04_heartbeats_never_progress():
    assert not observable_links({"progress_kind": "HEARTBEAT",
                                 "progress_evidence": "hb"})["P_o"]
    assert observable_links(
        {"progress_kind": "PUBLICATION_ADVANCED",
         "progress_evidence": "ev-82"})["P_o"]  # (+) real progress counts

# L2-05: the debt contract — accrue / leave / reset / never-reset. (+)
def test_l2_05_debt_contract():
    d = track_fairness_debt([
        {"eligible": True, "service": None},
        {"eligible": True, "service": None},
        {"eligible": False, "service": None},
        {"eligible": True, "service": SVC},
        {"eligible": True, "service": None, "reassigned": True}])
    assert [h["debt"] for h in d["debt_history"]] == [1, 2, 2, 0, 1]
    assert d["max_debt"] == 2

# L2-06: six-round base ⇒ service PASS, progress PASS, no fairness violation. (+)
def test_l2_06_six_round_base():
    b = lab_six_round_example("base")
    assert b["service"] == "SERVICE_WITHIN_BOUND"
    assert b["progress"] == "PROGRESS_WITHIN_BOUND"
    assert not b["fairness_violation"]
    assert b["debt_history"] == [0, 0, 1, 0, 1, 0]

# L2-07: one-fact variant ⇒ BOUNDED_SERVICE_VIOLATION, still not WF/SF. (-)
def test_l2_07_six_round_variant_breach():
    b = lab_six_round_example("variant")
    assert b["service"] == "BOUNDED_SERVICE_VIOLATION"
    assert not b["fairness_violation"]
    assert b["debt_history"] == [0, 0, 1, 2, 3, 0]

# L2-08: the outage warning — 29 ineligible minutes accrue nothing. (+)
def test_l2_08_outage_rounds_ineligible():
    d = track_fairness_debt([{"eligible": True, "service": SVC}] * 2
                            + [{"eligible": False, "service": None}] * 29
                            + [{"eligible": True, "service": SVC}])
    assert d["max_debt"] == 0
    assert check_service_bound(
        d["debt_history"], 3, True)["verdict"] == "SERVICE_WITHIN_BOUND"

# L2-09: paired CONTROL vs TREATMENT, identical timeouts. (-)
def test_l2_09_paired_experiment():
    dc = track_fairness_debt([{"eligible": False, "service": None}
                              for _ in range(6)])
    dt = track_fairness_debt([{"eligible": True, "service": None}
                              for _ in range(6)])
    vc = bounded_verdict({"timeout_observed": True, "cause_known": False,
                          "waiting_on_authority": True})
    vt = bounded_verdict({"timeout_observed": True, "cause_known": True,
                          "trace_complete_and_verified": True,
                          "debt_history": dt["debt_history"], "B_S": 3})
    assert dc["max_debt"] == 0
    assert vc["verdict"] == "WAITING_AUTHORITY"          # control preserved
    assert vt["verdict"] == "BOUNDED_SERVICE_VIOLATION"  # treatment caught

# L2-10: the mutation — evidence-free dispatch cannot hide a breach. (-)
def test_l2_10_dispatched_as_serviced_rejected():
    rounds = [{"eligible": True,
               "service": {"kind": "DISPATCHED", "evidence": None}}
              for _ in range(6)]
    honest = track_fairness_debt(rounds, count_dispatched_as_service=False)
    mutant = track_fairness_debt(rounds, count_dispatched_as_service=True)
    assert check_service_bound(
        honest["debt_history"], 3,
        True)["verdict"] == "BOUNDED_SERVICE_VIOLATION"
    assert mutant["max_debt"] == 0  # the mutant hides it; honest law catches it

# L2-11: bound composition. (+)
def test_l2_11_compose_bounds():
    c = compose_bounds(3, 4, 10, {"consistent_units": True,
                                  "per_stage_bounds_proven": True,
                                  "finite_attempts": True,
                                  "contention_accounted": True})
    assert c["composed"] and c["B_total"] == 17
    bad = compose_bounds(3, 4, 10, {"consistent_units": False,
                                    "per_stage_bounds_proven": True,
                                    "finite_attempts": True,
                                    "contention_accounted": True})
    assert not bad["composed"]

# L2-12: the ladder — a timeout alone never climbs. (+)
def test_l2_12_timeout_alone_never_fairness():
    v = bounded_verdict({"timeout_observed": True})
    assert v["verdict"] == "EXECUTION_TIMEOUT_OBSERVED"
    assert v["assurance"] == "RUNTIME_OBSERVATION"

# L2-13: the seven assumptions gate every bound claim. (+)
def test_l2_13_bound_assumptions_first():
    ok = check_bound_assumptions({a: True for a in BOUND_ASSUMPTIONS})
    assert ok["grounded"]
    missing = check_bound_assumptions({"finite_queue_capacity": True})
    assert not missing["grounded"] and missing["missing"]

# L2-14: ten-field packet; gaps never count as opportunities. (+)
def test_l2_14_evidence_packet():
    pkt = {"obligation_identity": "o", "bound_capacity_basis": "b",
           "canonical_state_revisions": {}, "eligibility_history": [],
           "scheduling_history": [], "usable_service": None,
           "progress": None, "recovery_budget": "ok",
           "deadline_witness": "w", "independent_verdict": "v",
           "trace_gaps": [2]}
    r = verify_bounded_packet(pkt)
    assert not r["packet_valid"]  # gaps flagged, never counted
    full = dict(pkt, trace_gaps=[])
    r2 = verify_bounded_packet(full)
    assert r2["packet_valid"]

# L2-15: AER-LIVE-002 acceptance. (+)
def test_l2_15_aer_live_002():
    r = aer_live_002()
    assert r["paired"]["control"] == "WAITING_AUTHORITY"
    assert r["paired"]["treatment"] == "BOUNDED_SERVICE_VIOLATION"
    assert r["restart_continuity"]["verdict"] == "BOUNDED_SERVICE_VIOLATION"
    assert r["restart_continuity"]["debt_survived"] == [1, 2, 3]
    assert r["intermittent_eligibility"]["debt"] == [1, 1, 2, 2, 3]
    assert not r["absent_receipts"]["packet_valid"]
    assert r["budget_exhaustion"]["verdict"] == "DISPOSITION_BOUND_BREACHED"
    assert r["incomplete_telemetry"]["max_debt"] == 2
    assert all(r["acceptance"].values())

# L2-16: the full BL1–BL12 suite green. (+)
def test_l2_16_bl_suite_green():
    results = live_bl_suite()
    assert len(results) == 12
    fails = [r for r in results if r[1] != "PASS"]
    assert not fails, fails
