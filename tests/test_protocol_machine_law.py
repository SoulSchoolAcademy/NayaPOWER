"""
Tests for kernel/protocol — the machine law of the Team Naya Operating Protocol.

Prime 2: the law is the code. These tests prove the machinery enforces it.
Positive AND negative controls: gates must block what they claim to block
and allow what they claim to allow.
"""
import time

import pytest

from kernel.protocol.read_receipt import (
    AUTHORITY_QUESTIONS,
    ReadReceipt,
    grade_answer,
    issue_receipt,
)
from kernel.protocol.authority_gate import classify_action, is_authorized, Verdict
from kernel.protocol.quality_gate import Scorecard, check_delivery, DELIVERY_FLOOR
from kernel.protocol.cold_start_gate import ColdStartState, run_cold_start
from kernel.protocol.cold_successor_test import Handoff, check_handoff
from kernel.protocol.takeover import (
    TakeoverRecord,
    evaluate_takeover,
    validate_completed_takeover,
    STALL_WINDOW_SECONDS,
)


# ---------- read_receipt ----------

CORRECT = {
    "q1": "Shawn Vibert",
    "q2": "production deploys, credentials and money, destructive actions, ratification, security and privacy",
    "q3": "No, never",
    "q4": "9.0",
    "q5": "independent evidence and proof",
}


def test_receipt_passes_with_correct_answers():
    r = issue_receipt("naya-test", CORRECT)
    assert r.passed
    assert r.verify()


def test_receipt_fails_with_wrong_answers():
    bad = dict(CORRECT)
    bad["q3"] = "yes, if the score is high enough"
    r = issue_receipt("naya-test", bad)
    assert not r.passed
    assert not r.verify()


def test_receipt_fails_with_missing_answers():
    r = issue_receipt("naya-test", {})
    assert not r.passed


def test_receipt_tamper_detected():
    r = issue_receipt("naya-test", CORRECT)
    r.passed = False  # tamper after signing
    assert not r.verify()


def test_receipt_bound_to_protocol_version():
    r = issue_receipt("naya-test", CORRECT)
    assert r.protocol_version  # version pinned; stale receipts detectable


# ---------- authority_gate ----------

def test_production_deploy_needs_shawn():
    res = classify_action("deploy to production the new build")
    assert res.verdict == Verdict.NEEDS_SHAWN
    assert res.gate_id == "production"


def test_credentials_need_shawn():
    res = classify_action("use the api key to charge the card")
    assert res.verdict == Verdict.NEEDS_SHAWN


def test_destructive_needs_shawn():
    res = classify_action("drop table users in production")
    assert res.verdict == Verdict.NEEDS_SHAWN


def test_ratification_needs_shawn():
    res = classify_action("mark ratified the new doctrine")
    assert res.verdict == Verdict.NEEDS_SHAWN


def test_hard_stop_refuses():
    res = classify_action("fabricate evidence for the demo")
    assert res.verdict == Verdict.REFUSE


def test_routine_work_allowed():
    assert is_authorized("open a PR with the repair and run the test suite")
    assert is_authorized("capture the lesson as a smart note")


def test_score_cannot_grant_permission():
    # Even a perfect-sounding action at a protected gate stays gated.
    res = classify_action("deploy to production — scorecard 10/10, all tests green")
    assert res.verdict == Verdict.NEEDS_SHAWN


# ---------- quality_gate ----------

def _good_scorecard():
    return Scorecard(
        what="repair PR",
        evidence="tests 42/42, commit abc123",
        scores={"correctness": 9.5, "completeness": 9.0, "evidence": 9.5},
        weights={"correctness": 0.4, "completeness": 0.3, "evidence": 0.3},
        weakest_point="docs could be richer; why not 10: no independent run yet",
        verified_by="naya-1",
    )


def test_quality_gate_passes_good_scorecard():
    res = check_delivery(_good_scorecard(), builder_id="naya-4")
    assert res.passed, res.reasons
    assert res.total >= DELIVERY_FLOOR


def test_quality_gate_blocks_missing_scorecard():
    res = check_delivery(None, builder_id="naya-4")
    assert not res.passed


def test_quality_gate_blocks_below_floor_dimension():
    sc = _good_scorecard()
    sc.scores["completeness"] = 8.0  # a 10 never covers a 7
    res = check_delivery(sc, builder_id="naya-4")
    assert not res.passed


def test_quality_gate_blocks_self_verification():
    res = check_delivery(_good_scorecard(), builder_id="naya-1")
    assert not res.passed  # verified_by == builder


def test_quality_gate_blocks_missing_weakest_point():
    sc = _good_scorecard()
    sc.weakest_point = ""
    res = check_delivery(sc, builder_id="naya-4")
    assert not res.passed


def test_quality_gate_rejects_bad_weights():
    sc = _good_scorecard()
    sc.weights = {"correctness": 0.5, "completeness": 0.5, "evidence": 0.5}
    res = check_delivery(sc, builder_id="naya-4")
    assert not res.passed


# ---------- cold_start_gate ----------

def _good_state():
    return ColdStartState(
        agent_id="naya-9",
        human_director="Shawn Vibert",
        lane="verify",
        authority_summary="Protected gates: production deploys, credentials/money, "
                          "destructive actions, ratification, security/privacy.",
        current_truth_location="coordination feed #1354 and current main",
        next_action="re-anchor on live main and check the board",
        receipt=issue_receipt("naya-9", CORRECT),
    )


def test_cold_start_passes_complete_state():
    assert run_cold_start(_good_state()).passed


def test_cold_start_blocks_missing_receipt():
    s = _good_state()
    s.receipt = None
    res = run_cold_start(s)
    assert not res.passed


def test_cold_start_blocks_failed_receipt():
    s = _good_state()
    s.receipt = issue_receipt("naya-9", {})  # failed grading
    res = run_cold_start(s)
    assert not res.passed


def test_cold_start_requires_board_and_main():
    s = _good_state()
    s.current_truth_location = "the board"  # board alone is not the source of truth
    res = run_cold_start(s)
    assert not res.passed


# ---------- cold_successor_test ----------

def _good_handoff():
    return Handoff(
        what_happened="repaired the registry drift",
        what_is_true="main is green at abc123",
        authority_used="standing merge authority under Scorecard Law",
        proof="PR #1800, tests 1056 passed, commit abc123",
        what_is_open="cold-graph gap still open",
        what_is_blocked="none",
        next_action="re-anchor and run the battery",
    )


def test_handoff_passes_complete():
    assert check_handoff(_good_handoff()).passed


def test_handoff_fails_missing_proof():
    h = _good_handoff()
    h.proof = ""
    assert not check_handoff(h).passed


def test_handoff_fails_unstated_blockers():
    h = _good_handoff()
    h.what_is_blocked = ""
    assert not check_handoff(h).passed


# ---------- takeover ----------

def _takeover_record(**over):
    base = dict(
        taker_id="naya-4",
        owner_id="naya-2",
        task="repair the registry drift test",
        reason="no progress in 6 hours",
        last_owner_progress_at=time.time() - 6 * 3600,
    )
    base.update(over)
    return TakeoverRecord(**base)


def test_takeover_allowed_when_stalled():
    assert evaluate_takeover(_takeover_record()).allowed


def test_takeover_blocked_when_owner_active():
    rec = _takeover_record(last_owner_progress_at=time.time() - 3600)
    res = evaluate_takeover(rec)
    assert not res.allowed


def test_takeover_blocked_at_protected_gate():
    rec = _takeover_record(task="deploy to production the fix")
    res = evaluate_takeover(rec)
    assert not res.allowed


def test_completed_takeover_requires_record():
    rec = _takeover_record()
    res = validate_completed_takeover(rec)
    assert not res.allowed  # nothing recorded yet
    rec.what_changed = "fixed the drift"
    rec.evidence = "tests green, commit xyz"
    rec.owner_notified = True
    rec.owner_next_task = "review the repair"
    assert validate_completed_takeover(rec).allowed


# ---------- minimal_action ----------

from kernel.protocol.minimal_action import ChangeProposal, check_minimal
from kernel.protocol.learning_capture import CycleLesson, check_lesson


def _good_proposal():
    return ChangeProposal(
        description="fix the registry drift check",
        files_changed=["tests/test_registry.py"],
        behavior_preserved="all other checks unchanged",
        why_not_smaller="single-file fix; the drift is isolated to this check",
    )


def test_minimal_action_passes():
    assert check_minimal(_good_proposal()).passed


def test_minimal_action_requires_preservation_statement():
    p = _good_proposal()
    p.behavior_preserved = ""
    assert not check_minimal(p).passed


def test_minimal_action_requires_why_not_smaller():
    p = _good_proposal()
    p.why_not_smaller = ""
    assert not check_minimal(p).passed


def test_minimal_action_flags_broad_change():
    p = _good_proposal()
    p.files_changed = [f"file_{i}.py" for i in range(20)]
    assert not check_minimal(p).passed


# ---------- learning_capture ----------

def test_learning_capture_passes_with_lesson():
    c = CycleLesson(
        work_description="repaired the drift",
        lesson="presence checks don't catch field stripping",
        provenance="test_protected_intelligence_integrity.py",
        smart_note_id="SN-0633",
    )
    assert check_lesson(c).passed


def test_learning_capture_passes_with_stated_no_lesson():
    c = CycleLesson(
        work_description="routine dependency bump",
        lesson="",
        no_lesson_reason="no behavioral change, no new insight",
    )
    assert check_lesson(c).passed


def test_learning_capture_blocks_silent_no_lesson():
    c = CycleLesson(work_description="did some work", lesson="")
    assert not check_lesson(c).passed


def test_learning_capture_requires_provenance():
    c = CycleLesson(
        work_description="did work",
        lesson="learned something",
        provenance="",
    )
    assert not check_lesson(c).passed
