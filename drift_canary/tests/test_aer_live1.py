"""AER-LIVE-1 tests (SN-0807): the E_o/S_o/P_o distinction, the 8-row
diagnosis table, finite fairness checks, the safety×progress matrix, the
seven clocks, the nine-item evidence packet, smallest valid repair, the
epoch-82 worked example, the L1-L12 suite with the adversarial fixture,
ValidDisposition, and AER-LIVE-001. Every negative test gets a positive
control."""
import pytest

from drift_canary.revocation_linearization import (
    AER_LIVE1_IMPLEMENTATION_STATUS,
    NON_PROGRESS_SIGNALS,
    liveness_enabled,
    track_esp,
    LIVENESS_DIAGNOSES,
    diagnose_liveness,
    check_fairness_finite,
    SAFETY_X_PROGRESS,
    assess_safety_x_progress,
    CLOCKS,
    ESCALATION_POLICY,
    check_escalation,
    EVIDENCE_PACKET_ITEMS,
    classify_publication_state,
    smallest_repair,
    lab_epoch_82_worked_example,
    live_l_suite,
    valid_disposition,
    aer_live_001,
)


def T(*events):
    return [(i + 1, k, d) for i, (k, d) in enumerate(events)]


# --- Honest scope ----------------------------------------------------------------------------------

def test_implementation_status_is_proposed_labels():
    s = AER_LIVE1_IMPLEMENTATION_STATUS
    assert s["enters_as"] == "proposed diagnostic labels + harness demonstration"
    assert "replacement for canonical liveness states" in s["not_a"]
    assert "production AER-LIVE-1 monitor" in s["not_verified"]


def test_non_progress_signals_never_establish_p_o():
    assert set(NON_PROGRESS_SIGNALS) == {"HEARTBEAT", "LOG_ENTRY",
                                        "STATUS_REWRITE", "REASSIGNMENT",
                                        "REPEATED_FAILED_RETRY"}


# --- E_o / S_o / P_o ----------------------------------------------------------------------------------

def test_liveness_enabled_conjunction():
    assert liveness_enabled(True, True, True)["E_o"]
    assert not liveness_enabled(False, True, True)["E_o"]
    assert not liveness_enabled(True, False, True)["E_o"]
    assert not liveness_enabled(True, True, False)["E_o"]
    assert "not a starvation victim" in liveness_enabled(
        False, True, True)["note"]


def test_track_esp_separates_three_links():
    h = track_esp(T(("PERMITTED", {}), ("DEPS_READY", {}),
                    ("RESOURCES_OK", {}), ("SERVICED", {"w": 1}),
                    ("HEARTBEAT", {}), ("PROGRESS", {"done": 1})))
    assert all(e for _, e in h["E_o"][-3:])
    assert len(h["S_o"]) == 1 and len(h["P_o"]) == 1
    # The heartbeat is recorded but is not service and not progress.
    assert h["non_progress_signals"] == [(5, "HEARTBEAT")]
    assert len(h["S_o"]) == 1  # the heartbeat did not become S_o


def test_service_log_line_is_not_s_o():
    h = track_esp(T(("PERMITTED", {}), ("LOG_ENTRY", {"msg": "serviced"})))
    assert not h["S_o"]  # a SERVICE log line is not S_o
    assert h["non_progress_signals"]


# --- Diagnosis table ---------------------------------------------------------------------------------------

def test_eight_diagnoses_known():
    assert set(LIVENESS_DIAGNOSES) == {"WAITING_AUTHORITY",
                                       "WAITING_DEPENDENCY",
                                       "BLOCKED_RECOVERABLE",
                                       "STARVATION_SUSPECTED",
                                       "PROGRESS_ON_SERVICE_VIOLATION",
                                       "DEADLOCK_SUSPECTED",
                                       "INSUFFICIENT_EVIDENCE",
                                       "RECOVERING_NORMALLY"}


def test_waiting_authority_is_not_starvation():
    d = diagnose_liveness(T(("BLOCKED_AUTH", {}), ("DEPS_READY", {}),
                             ("RESOURCES_OK", {})))
    assert d["diagnosis"] == "WAITING_AUTHORITY"
    assert "not a starvation victim" in d["cause"]


def test_waiting_dependency():
    d = diagnose_liveness(T(("PERMITTED", {}), ("DEPS_BLOCKED", {}),
                             ("RESOURCES_OK", {})))
    assert d["diagnosis"] == "WAITING_DEPENDENCY"


def test_blocked_recoverable():
    d = diagnose_liveness(T(*([("PERMITTED", {}), ("DEPS_READY", {}),
                                ("RESOURCES_STARVED", {})]
                               + [("HEARTBEAT", {})] * 12)),
                          service_window=10)
    assert d["diagnosis"] == "BLOCKED_RECOVERABLE"


def test_starvation_suspected_not_proven():
    d = diagnose_liveness(T(*([("PERMITTED", {}), ("DEPS_READY", {}),
                                ("RESOURCES_OK", {})]
                               + [("HEARTBEAT", {})] * 12)),
                          service_window=10)
    assert d["diagnosis"] == "STARVATION_SUSPECTED"
    assert "suspicion, not proof" in d["cause"]


def test_progress_on_service_violation():
    d = diagnose_liveness(T(("PERMITTED", {}), ("DEPS_READY", {}),
                             ("RESOURCES_OK", {}), ("SERVICED", {"w": 1}),
                             ("HEARTBEAT", {})))
    assert d["diagnosis"] == "PROGRESS_ON_SERVICE_VIOLATION"


def test_deadlock_suspected():
    d = diagnose_liveness(T(("PERMITTED", {}),
                             ("WAITS_ON", {"obligation": "A", "on": "B"}),
                             ("WAITS_ON", {"obligation": "B", "on": "A"})))
    assert d["diagnosis"] == "DEADLOCK_SUSPECTED"


def test_insufficient_evidence_empty_trace():
    d = diagnose_liveness([])
    assert d["diagnosis"] == "INSUFFICIENT_EVIDENCE"
    assert "never collapse" in d["cause"]


def test_recovering_normally():
    d = diagnose_liveness(T(("PERMITTED", {}), ("DEPS_READY", {}),
                             ("RESOURCES_OK", {}), ("SERVICED", {"w": 1}),
                             ("PROGRESS", {"done": 1})))
    assert d["diagnosis"] == "RECOVERING_NORMALLY"


def test_diagnosis_by_cause_not_elapsed_time():
    # Same long elapsed time, different causes → different diagnoses.
    long_wait_auth = T(*([("BLOCKED_AUTH", {})] + [("HEARTBEAT", {})] * 50))
    long_starve = T(*([("PERMITTED", {}), ("DEPS_READY", {}),
                        ("RESOURCES_OK", {})] + [("HEARTBEAT", {})] * 50))
    assert diagnose_liveness(long_wait_auth)["diagnosis"] == "WAITING_AUTHORITY"
    assert diagnose_liveness(long_starve)["diagnosis"] == "STARVATION_SUSPECTED"


# --- Finite fairness ---------------------------------------------------------------------------------------------

def test_fairness_finite_honesty_clause():
    r = check_fairness_finite([])
    assert r["WF"] == "INSUFFICIENT_EVIDENCE"
    r2 = check_fairness_finite(
        T(*([("PERMITTED", {}), ("DEPS_READY", {}), ("RESOURCES_OK", {})]
            + [("HEARTBEAT", {})] * 15)), window=10)
    assert r2["WF"] == "SUSPECTED"  # suspicion, never infinite proof
    assert "never infinite-violation proofs" in r2["honesty"]


def test_pos_violation_on_service_without_progress():
    r = check_fairness_finite(
        T(("PERMITTED", {}), ("DEPS_READY", {}), ("RESOURCES_OK", {}),
          ("SERVICED", {"w": 1})) + [(10 + i, "HEARTBEAT", {})
                                     for i in range(15)], window=10)
    assert r["PoS"] == "VIOLATION"


# --- Safety × progress -----------------------------------------------------------------------------------------------

def test_safety_x_progress_seven_rows():
    assert len(SAFETY_X_PROGRESS) == 7


def test_hold_required_is_not_completion_claim():
    r = assess_safety_x_progress("HOLD_REQUIRED (correct)",
                                 "STALLED_INVESTIGATE")
    assert r["row"] == "SAFE_HOLD_STALLED"
    assert "scheduler needs investigation" in r["note"]


def test_three_safety_examples():
    correct = assess_safety_x_progress("HOLD_REQUIRED (correct)",
                                       "NO_OBLIGATION")
    assert correct["row"] == "SAFE_HOLD_CORRECT"
    stalled = assess_safety_x_progress("HOLD_REQUIRED (correct)",
                                       "STALLED_INVESTIGATE")
    assert stalled["row"] == "SAFE_HOLD_STALLED"
    failed = assess_safety_x_progress("HOLD_REQUIRED",
                                      "FAILED_DESPITE_CAPACITY")
    assert failed["row"] == "RECOVERY_FAILURE"


def test_unknown_never_collapses_to_healthy():
    r = assess_safety_x_progress("UNKNOWN", "UNKNOWN")
    assert r["row"] == "INSUFFICIENT_EVIDENCE"


# --- Seven clocks ----------------------------------------------------------------------------------------------------------

def test_seven_clocks_independent():
    assert len(CLOCKS) == 7
    assert "projection_lag" in CLOCKS and "evidence_freshness" in CLOCKS


def test_escalation_changes_responsibility_not_safety():
    r = check_escalation({"total_unresolved_age": 5000,
                          "projection_lag": 3},
                         {"total_unresolved_age": 100,
                          "projection_lag": 10})
    assert r["escalations"]["total_unresolved_age"]["escalated"]
    assert "projection_lag" not in r["escalations"]
    assert "never changes the safety predicate" in r["invariant"]
    # No threshold makes an unsafe retry safe: the policy table says so per
    # clock.
    assert all("responsibility" in v for _, v in
               [(k, ESCALATION_POLICY[k][1]) for k in CLOCKS])


# --- Evidence packet --------------------------------------------------------------------------------------------------------------

def test_nine_item_packet():
    assert len(EVIDENCE_PACKET_ITEMS) == 9
    assert "authoritative_transaction_receipt" in EVIDENCE_PACKET_ITEMS


def test_worker_log_never_substitutes():
    r = classify_publication_state({"worker_log": "published_successfully"})
    assert r["situation"] == "UNCLASSIFIABLE"
    assert "never a substitute" in r["note"]


def test_three_situations_distinguished():
    base = {"authoritative_transaction_receipt": {"seq": 7}}
    assert classify_publication_state(
        {**base, "projection_complete": False})["situation"] == "REPLAY"
    assert classify_publication_state(
        {**base, "projection_complete": False,
         "stalled_despite_capacity": True})["situation"] == "DIAGNOSE"
    assert classify_publication_state(
        {**base, "commit_status": "AMBIGUOUS"})["situation"] == \
        "CONTAIN_RECONSTRUCT"
    assert "never projection-repair" in classify_publication_state(
        {**base, "commit_status": "INCORRECT"})["action"]


# --- Smallest valid repair ----------------------------------------------------------------------------------------------------------------

def test_smallest_repairs():
    assert smallest_repair("committed_projection_stale", {})[
        "repair"] == "IDEMPOTENT_REPLAY"
    r = smallest_repair("committed_outbox_missing", {})
    assert r["repair"] == "INTEGRITY_DEFECT_RECONSTRUCTION"
    assert "linked to the original" in r["note"]
    r = smallest_repair("incorrect_canonical_commit", {})
    assert "never rewritten" in r["note"]
    r = smallest_repair("ambiguous_external_effect", {})
    assert r["repair"] == "EXTERNAL_RECONCILIATION_ONLY"
    assert smallest_repair("nope", {})["repair"] == "UNKNOWN_SITUATION"


# --- Worked example ---------------------------------------------------------------------------------------------------------------------------------

def test_epoch_82_worked_example_reports_both():
    w = lab_epoch_82_worked_example()
    assert w["safety"] == "PASS"
    assert w["recovery"] in ("PROGRESS_ON_SERVICE_VIOLATION",
                             "STARVATION_SUSPECTED")
    assert w["progress_obligation"] == "FAILING"
    assert w["both_reported"] == "SAFE_HOLD_STALLED"
    assert w["repair"] == "IDEMPOTENT_REPLAY"
    assert "must not touch B's canonical qualification" in w[
        "repair_constraint"]
    assert w["law_holds"]


# --- L1–L12 + ValidDisposition --------------------------------------------------------------------------------------------------------------------------------

def test_l_suite_all_twelve():
    results = live_l_suite()
    assert [i for i, _, _ in results] == [f"L{i}" for i in range(1, 13)]
    bad = [(i, n) for i, v, n in results if v != "PASS"]
    assert not bad, bad


def test_adversarial_heartbeat_fraud_caught():
    adv = [x for x in live_l_suite(progress_check_enabled=False)
           if x[0] == "L5"][0]
    assert adv[1] == "CAUGHT"
    # Positive control: with the check enabled, L5 is a clean PASS.
    clean = [x for x in live_l_suite(progress_check_enabled=True)
             if x[0] == "L5"][0]
    assert clean[1] == "PASS"


def test_valid_disposition_contract():
    assert valid_disposition({"repaired_and_verified": True})["valid"]
    assert valid_disposition({"terminal_disposition": {
        "permitted": True, "goal_retained": True}})["valid"]
    # A terminal disposition that drops the goal is not valid.
    assert not valid_disposition({"terminal_disposition": {
        "permitted": True, "goal_retained": False}})["valid"]
    assert not valid_disposition({})["valid"]


# --- AER-LIVE-001 -------------------------------------------------------------------------------------------------------------------------------------------

def test_aer_live_001():
    r = aer_live_001()
    assert r["control"]["safety"] == "PASS"
    assert r["control"]["diagnosis"] == "RECOVERING_NORMALLY"
    assert r["defective"]["diagnosis"] == "PROGRESS_ON_SERVICE_VIOLATION"
    assert r["defective"]["safety"] == "PASS"  # the hold itself is correct
    assert r["waiting"]["diagnosis"] == "WAITING_AUTHORITY"
    assert r["waiting"]["progress_via_duty"]
    assert r["verifier_isolates_three_facts"]
    assert r["adversarial"]["L5"] == "CAUGHT"
