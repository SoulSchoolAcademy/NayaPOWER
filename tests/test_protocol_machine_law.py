"""
Tests for kernel/protocol — the machine law of the Team Naya Operating Protocol.

Prime 2: the law is the code. These tests prove the machinery enforces it.
Positive AND negative controls: gates must block what they claim to block
and allow what they claim to allow.
"""
import hashlib
import json
import time

import pytest

from kernel.protocol.read_receipt import (
    AUTHORITY_QUESTIONS,
    REQUIRED_SOURCE_PATHS,
    ReadReceipt,
    grade_answer,
    issue_receipt,
)
from kernel.protocol.authority_gate import classify_action, is_authorized, Verdict
from kernel.protocol.quality_gate import Scorecard, check_delivery, DELIVERY_FLOOR
from kernel.protocol.cold_start_gate import ColdStartState, run_cold_start
from kernel.protocol.work_cycle_receipt import check_sign_in, check_sign_out
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
    "q2": "production deploys, credentials, money, destructive actions, ratification, security, privacy, consent and authority changes",
    "q3": "No",
    "q4": "9.0",
    "q5": "independent evidence and proof",
    "q6": "The current shared coordination board is #2175; #1354 is a read-only historical archive.",
    "q7": "Mandatory boot sources include AGENTS.md, Naya-Protocol V1, the Constitution, OPERATING-LAW.md, 0008-OPERATING-CODE-V2.ai.md, and TEAM-NAYA-OPERATING-PROTOCOL-V1.md.",
    "q8": "No, opening a file or hashing a receipt alone does not prove comprehension.",
    "q9": "Governed work is held and blocked until the missing or conflicting required sources are resolved.",
    "q10": "Sign in before substantive work and sign out on the same feed at cycle end.",
    "q11": "The Constitution constrains; Operating Law and Operating Code govern; the Naya Protocol operationalizes them without replacing them.",
    "q12": "Unknown means missing knowledge is not zero or a pass; preserve uncertainty.",
    "q13": "The mission is maximum verified human value; independent evidence must prove success before claiming it.",
}

CURRENT_MAIN_SHA = "640a5fb41522e4a5ae6bbd4d258b8a0a88945ff6"
SOURCE_REVISIONS = {
    path: f"{i + 1:040x}" for i, path in enumerate(REQUIRED_SOURCE_PATHS)
}
SOURCE_REVISIONS[
    "NAYA-ACTIVATION/CURRENT-REALITY/SOURCE-PRECEDENCE-AND-NAVIGATION-RECONCILIATION-2026-10-10.md"
] = "f" * 40


def _receipt_body(payload):
    start = "<!-- NAYA-WORK-CYCLE-RECEIPT:START -->"
    end = "<!-- NAYA-WORK-CYCLE-RECEIPT:END -->"
    return start + "\n" + json.dumps(payload, sort_keys=True) + "\n" + end


def _good_sign_in():
    comment_id = "6105462971"
    record = {
        "event_type": "SIGN_IN",
        "agent_id": "naya-9",
        "feed_issue": 1867,
        "comment_id": comment_id,
        "comment_url": f"https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1867#issuecomment-{comment_id}",
        "task": "protocol boot gate",
        "owner": "Law/Governance",
        "objective": "require source-linked protocol comprehension before work",
        "definition_of_done": "tests prove missing packet or sign-in blocks boot",
        "current_main_sha": CURRENT_MAIN_SHA,
        "authority_and_gates": "documentation and reversible branch edits only; no merge",
        "known_unknowns_and_blockers": "CI and independent review pending",
        "first_action": "correct cold-start source requirements",
        "proof_target": "exact-head negative tests",
        "timestamp": "2026-10-10T21:00:00-08:00",
    }
    fields = [
        "event_type", "feed_issue", "agent_id", "task", "owner", "objective",
        "definition_of_done", "current_main_sha", "authority_and_gates",
        "known_unknowns_and_blockers", "first_action", "proof_target", "timestamp",
    ]
    record["comment_body"] = _receipt_body({key: record[key] for key in fields})
    record["comment_body_sha256"] = hashlib.sha256(record["comment_body"].encode("utf-8")).hexdigest()
    record["github_comment_observed"] = True
    return record


def _good_sign_out(sign_in=None):
    sign_in = sign_in or _good_sign_in()
    comment_id = "6105463999"
    record = {
        "event_type": "SIGN_OUT",
        "agent_id": sign_in["agent_id"],
        "feed_issue": sign_in["feed_issue"],
        "comment_id": comment_id,
        "comment_url": f"https://github.com/SoulSchoolAcademy/NayaPOWER/issues/{sign_in['feed_issue']}#issuecomment-{comment_id}",
        "sign_in_comment_id": sign_in["comment_id"],
        "current_main_sha": CURRENT_MAIN_SHA,
        "actual_result": "boot packet and receipt checks changed in PR",
        "tested_revision": CURRENT_MAIN_SHA,
        "evidence_links": "PR #2281, exact-head CI to be checked",
        "truth_status": "IMPLEMENTED_NOT_YET_VERIFIED",
        "claim_limits": "No test or production claim until CI/independent review",
        "score": 9.0,
        "score_delta": 0.5,
        "failure_or_root_cause": "stale #1354 marker identified and corrected",
        "remaining_blockers_and_owner": "CI and independent reviewer; Naya 4",
        "lesson_or_NO_CAPTURE": "NO_CAPTURE",
        "next_owner": "Naya 4 independent reviewer",
        "exactly_one_next_action": "Run exact-head acceptance tests",
        "timestamp": "2026-10-10T21:01:00-08:00",
    }
    fields = [
        "event_type", "feed_issue", "agent_id", "actual_result", "tested_revision",
        "evidence_links", "truth_status", "claim_limits", "score", "score_delta",
        "failure_or_root_cause", "remaining_blockers_and_owner",
        "lesson_or_NO_CAPTURE", "next_owner", "exactly_one_next_action",
        "timestamp", "sign_in_comment_id", "current_main_sha",
    ]
    record["comment_body"] = _receipt_body({key: record[key] for key in fields})
    record["comment_body_sha256"] = hashlib.sha256(record["comment_body"].encode("utf-8")).hexdigest()
    record["github_comment_observed"] = True
    return record


def test_sign_in_receipt_passes_for_current_specialist_feed():
    result = check_sign_in(_good_sign_in(), CURRENT_MAIN_SHA)
    assert result.passed, result.failures


def test_sign_in_rejects_archived_feed():
    receipt = _good_sign_in()
    receipt["feed_issue"] = 1354
    receipt["comment_url"] = (
        f"https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1354"
        f"#issuecomment-{receipt['comment_id']}"
    )
    result = check_sign_in(receipt, CURRENT_MAIN_SHA)
    assert not result.passed


def test_sign_in_rejects_body_hash_mismatch():
    receipt = _good_sign_in()
    receipt["comment_body"] += " forged"
    result = check_sign_in(receipt, CURRENT_MAIN_SHA)
    assert not result.passed


def test_sign_out_requires_same_feed_and_sign_in_reference():
    sign_in = _good_sign_in()
    sign_out = _good_sign_out(sign_in)
    result = check_sign_out(sign_in, sign_out, CURRENT_MAIN_SHA)
    assert result.passed, result.failures
    sign_out["feed_issue"] = 2175
    sign_out["comment_url"] = (
        f"https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2175"
        f"#issuecomment-{sign_out['comment_id']}"
    )
    result = check_sign_out(sign_in, sign_out, CURRENT_MAIN_SHA)
    assert not result.passed


def test_sign_out_rejects_missing_outcome_receipt():
    sign_in = _good_sign_in()
    sign_out = _good_sign_out(sign_in)
    sign_out["evidence_links"] = ""
    result = check_sign_out(sign_in, sign_out, CURRENT_MAIN_SHA)
    assert not result.passed




def test_receipt_passes_with_correct_answers():
    r = issue_receipt("naya-test", CORRECT, SOURCE_REVISIONS, CURRENT_MAIN_SHA)
    assert r.passed
    assert r.verify()


def test_receipt_fails_with_wrong_answers():
    bad = dict(CORRECT)
    bad["q3"] = "yes, if the score is high enough"
    r = issue_receipt("naya-test", bad, SOURCE_REVISIONS, CURRENT_MAIN_SHA)
    assert not r.passed
    assert not r.verify()


def test_receipt_fails_with_missing_answers():
    r = issue_receipt("naya-test", {}, SOURCE_REVISIONS, CURRENT_MAIN_SHA)
    assert not r.passed

def test_receipt_rejects_answer_that_only_starts_with_accepted_text():
    bad_identity = dict(CORRECT)
    bad_identity["q1"] = "Shawn is not the final human authority."
    assert not issue_receipt("naya-test", bad_identity, SOURCE_REVISIONS, CURRENT_MAIN_SHA).passed

    bad_score = dict(CORRECT)
    bad_score["q4"] = "99"
    assert not issue_receipt("naya-test", bad_score, SOURCE_REVISIONS, CURRENT_MAIN_SHA).passed


def test_receipt_tamper_detected():
    r = issue_receipt("naya-test", CORRECT, SOURCE_REVISIONS, CURRENT_MAIN_SHA)
    r.passed = False  # tamper after signing
    assert not r.verify()

def test_receipt_binds_raw_comprehension_answers():
    receipt = issue_receipt("naya-test", CORRECT, SOURCE_REVISIONS, CURRENT_MAIN_SHA)
    assert receipt.verify()
    receipt.answer_text["q1"] = "Shawn is not the final human authority."
    receipt.sign()  # even a recomputed public digest cannot make a false answer pass
    assert not receipt.verify()


def test_receipt_rejects_boolean_only_answers_without_answer_text():
    receipt = issue_receipt("naya-test", CORRECT, SOURCE_REVISIONS, CURRENT_MAIN_SHA)
    receipt.answer_text = {}
    receipt.sign()
    assert not receipt.verify()


def test_receipt_bound_to_protocol_version():
    r = issue_receipt("naya-test", CORRECT, SOURCE_REVISIONS, CURRENT_MAIN_SHA)
    assert r.protocol_version == "NAYA-PROTOCOL-V1/2026-10-11"  # version pinned; stale receipts detectable



def test_receipt_requires_all_boot_sources():
    incomplete = dict(SOURCE_REVISIONS)
    incomplete.pop("CONSTITUTION/🔱 THE NAYAPOWER CONSTITUTION Foundational Operating Laws of Naya, NayaPOWER & NayaNET  Version 1.0 — Founding Constitution.md")
    r = issue_receipt("naya-test", CORRECT, incomplete, CURRENT_MAIN_SHA)
    assert not r.passed
    assert not r.verify()


def test_receipt_requires_dated_source_precedence_document():
    incomplete = {
        key: value for key, value in SOURCE_REVISIONS.items()
        if not key.startswith("NAYA-ACTIVATION/CURRENT-REALITY/SOURCE-PRECEDENCE-AND-NAVIGATION-RECONCILIATION-")
    }
    r = issue_receipt("naya-test", CORRECT, incomplete, CURRENT_MAIN_SHA)
    assert not r.passed


def test_receipt_requires_valid_current_main_sha():
    r = issue_receipt("naya-test", CORRECT, SOURCE_REVISIONS, "stale-or-missing")
    assert not r.passed


def test_cold_start_rejects_receipt_for_another_agent():
    state = _good_state()
    state.receipt = issue_receipt("other-seat", CORRECT, SOURCE_REVISIONS, CURRENT_MAIN_SHA)
    assert not run_cold_start(state).passed


def test_cold_start_rejects_archived_feed_as_current_navigation():
    state = _good_state()
    state.current_truth_location = "historical archive #1354 and current main"
    assert not run_cold_start(state).passed


def test_cold_start_requires_receipt_to_match_main_sha():
    state = _good_state()
    state.current_main_sha = "a" * 40
    assert not run_cold_start(state).passed


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
        current_truth_location="mission issue #2154, current coordination board #2175, and live main",
        next_action="re-anchor on live main and check the board",
        receipt=issue_receipt("naya-9", CORRECT, SOURCE_REVISIONS, CURRENT_MAIN_SHA),
        current_main_sha=CURRENT_MAIN_SHA,
        sign_in_record=_good_sign_in(),
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
    s.receipt = issue_receipt("naya-9", {}, SOURCE_REVISIONS, CURRENT_MAIN_SHA)  # failed comprehension
    res = run_cold_start(s)
    assert not res.passed


def test_cold_start_requires_board_and_main():
    s = _good_state()
    s.current_truth_location = "the board"  # board alone is not the source of truth
    res = run_cold_start(s)
    assert not res.passed


# ---------- cold_successor_test ----------

def _good_handoff():
    sign_in = _good_sign_in()
    return Handoff(
        what_happened="repaired the registry drift",
        what_is_true="main is green at abc123",
        authority_used="standing merge authority under Scorecard Law",
        proof="PR #1800, tests 1056 passed, commit abc123",
        what_is_open="cold-graph gap still open",
        what_is_blocked="none",
        next_action="re-anchor and run the battery",
        sign_in_receipt=sign_in,
        sign_out_receipt=_good_sign_out(sign_in),
        current_main_sha=CURRENT_MAIN_SHA,
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

def test_handoff_fails_without_sign_out_receipt():
    h = _good_handoff()
    h.sign_out_receipt = None
    result = check_handoff(h)
    assert not result.passed
    assert any("sign-in and sign-out" in failure.lower() for failure in result.failures)


def test_handoff_fails_when_sign_out_uses_different_feed():
    h = _good_handoff()
    h.sign_out_receipt["feed_issue"] = 2175
    h.sign_out_receipt["comment_url"] = (
        "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2175"
        f"#issuecomment-{h.sign_out_receipt['comment_id']}"
    )
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
