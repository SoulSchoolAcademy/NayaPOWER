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
    COMPREHENSION_QUESTIONS,
    PROTOCOL_VERSION,
    REQUIRED_SOURCE_PATHS,
    ReadReceipt,
    grade_answer,
    issue_receipt,
)
from kernel.protocol.authority_gate import classify_action, is_authorized, Verdict
from kernel.protocol.quality_gate import Scorecard, check_delivery, DELIVERY_FLOOR
from kernel.protocol.cold_start_gate import ColdStartState, run_cold_start
from kernel.protocol.cold_successor_test import Handoff, check_handoff
from kernel.protocol.work_cycle_receipt import (
    RECEIPT_START, RECEIPT_END, check_sign_in, check_sign_out,
)
from kernel.protocol.takeover import (
    TakeoverRecord,
    evaluate_takeover,
    validate_completed_takeover,
    STALL_WINDOW_SECONDS,
)

CORRECT = {
    "q1": "Shawn Vibert",
    "q2": "Production deployments, credentials, money, destructive actions, ratification, security, privacy, consent, and authority changes are protected gates.",
    "q3": "No",
    "q4": "9.0",
    "q5": "Independent evidence and proof establish verified success.",
    "q6": "The current shared coordination board is #2175; #1354 is a historical archive.",
    "q7": "Required boot sources include PROTOCOL.md, AGENTS.md, the Constitution, Laws Index, Portable Activation Protocol, Smart Note Operating Contract, Nonstop Loop, and Current Mission State.",
    "q8": "No; opening a file or hashing a receipt alone does not prove comprehension.",
    "q9": "Governed work remains HELD and BLOCKED while required sources are missing or conflicting.",
    "q10": "Sign in before substantive work and sign out on the same feed at cycle end.",
    "q11": "The Constitution constrains; the ratified Operating Law and Operating Code govern; the Protocol operationalizes them without replacing them.",
    "q12": "Unknown is never zero and never a pass; preserve uncertainty.",
    "q13": "The mission is maximum verified human value; independent evidence must establish success.",
}
CURRENT_MAIN_SHA = "a" * 40
SOURCE_REVISIONS = {
    path: f"{index + 1:040x}"
    for index, path in enumerate(REQUIRED_SOURCE_PATHS)
}
SOURCE_REVISIONS[
    "NAYA-ACTIVATION/CURRENT-REALITY/SOURCE-PRECEDENCE-AND-NAVIGATION-RECONCILIATION-2026-10-10.md"
] = "f" * 40


def _comment_body(payload):
    return (
        RECEIPT_START + "\n"
        + json.dumps(payload, sort_keys=True, separators=(",", ":"))
        + "\n" + RECEIPT_END
    )


def _good_sign_in():
    record = {
        "event_type": "SIGN_IN",
        "feed_issue": 1867,
        "agent_id": "naya-9",
        "task": "enforce protocol boot packet",
        "owner": "Law/Governance",
        "objective": "prove sources and comprehension before work",
        "definition_of_done": "negative controls block missing receipt and stale feed",
        "current_main_sha": CURRENT_MAIN_SHA,
        "authority_and_gates": "no protected gate bypass; no merge or production action",
        "known_unknowns_and_blockers": "exact-head CI and independent review pending",
        "first_action": "run the boot gate acceptance tests",
        "proof_target": "current source revisions, comprehension receipt, and live feed comment",
        "timestamp": "2026-10-10T21:00:00-08:00",
        "comment_id": "111",
    }
    payload = {key: value for key, value in record.items() if key != "comment_id"}
    body = _comment_body(payload)
    record.update({
        "comment_url": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1867#issuecomment-111",
        "comment_body": body,
        "comment_body_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
        "github_comment_observed": True,
    })
    return record


def _good_sign_out(sign_in=None):
    sign_in = sign_in or _good_sign_in()
    record = {
        "event_type": "SIGN_OUT",
        "feed_issue": sign_in["feed_issue"],
        "agent_id": sign_in["agent_id"],
        "actual_result": "protocol receipt and entry-point checks implemented on a candidate branch",
        "tested_revision": "b" * 40,
        "evidence_links": ["https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2281"],
        "truth_status": "IMPLEMENTED_NOT_YET_VERIFIED",
        "claim_limits": "do not claim exact-head CI or production behavior from this fixture",
        "score": 9.0,
        "score_delta": 0.5,
        "failure_or_root_cause": "stale source/feed marker identified",
        "remaining_blockers_and_owner": "CI and independent review; assigned verifier",
        "lesson_or_NO_CAPTURE": "NO_CAPTURE",
        "next_owner": "independent verifier",
        "exactly_one_next_action": "run exact-head acceptance tests",
        "timestamp": "2026-10-10T21:01:00-08:00",
        "sign_in_comment_id": str(sign_in["comment_id"]),
        "current_main_sha": CURRENT_MAIN_SHA,
        "comment_id": "222",
    }
    payload = {key: value for key, value in record.items() if key != "comment_id"}
    body = _comment_body(payload)
    record.update({
        "comment_url": f"https://github.com/SoulSchoolAcademy/NayaPOWER/issues/{record['feed_issue']}#issuecomment-222",
        "comment_body": body,
        "comment_body_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
        "github_comment_observed": True,
    })
    return record


def test_receipt_passes_with_correct_answers():
    receipt = issue_receipt("naya-test", CORRECT, SOURCE_REVISIONS, CURRENT_MAIN_SHA)
    assert receipt.passed
    assert receipt.verify()


def test_receipt_fails_with_wrong_answers():
    bad = dict(CORRECT)
    bad["q3"] = "yes; a high score can override a hard gate"
    receipt = issue_receipt("naya-test", bad, SOURCE_REVISIONS, CURRENT_MAIN_SHA)
    assert not receipt.passed
    assert not receipt.verify()


def test_receipt_fails_with_missing_answers():
    receipt = issue_receipt("naya-test", {}, SOURCE_REVISIONS, CURRENT_MAIN_SHA)
    assert not receipt.passed
    assert not receipt.verify()


def test_receipt_tamper_detected():
    receipt = issue_receipt("naya-test", CORRECT, SOURCE_REVISIONS, CURRENT_MAIN_SHA)
    receipt.passed = False
    assert not receipt.verify()


def test_receipt_version_is_pinned():
    receipt = issue_receipt("naya-test", CORRECT, SOURCE_REVISIONS, CURRENT_MAIN_SHA)
    assert receipt.protocol_version == PROTOCOL_VERSION
    assert receipt.verify()


def test_receipt_rejects_prefix_answer_false_positive():
    wrong_identity = dict(CORRECT)
    wrong_identity["q1"] = "Shawn is not the final human authority."
    assert not issue_receipt("naya-test", wrong_identity, SOURCE_REVISIONS, CURRENT_MAIN_SHA).passed
    wrong_score = dict(CORRECT)
    wrong_score["q4"] = "99"
    assert not issue_receipt("naya-test", wrong_score, SOURCE_REVISIONS, CURRENT_MAIN_SHA).passed


def test_receipt_binds_raw_answers_not_only_boolean_scores():
    receipt = issue_receipt("naya-test", CORRECT, SOURCE_REVISIONS, CURRENT_MAIN_SHA)
    assert receipt.verify()
    receipt.answer_text["q1"] = "Shawn is not the final human authority."
    receipt.sign()
    assert not receipt.verify()


def test_receipt_rejects_missing_boot_source_or_reconciliation():
    incomplete = dict(SOURCE_REVISIONS)
    incomplete.pop("NAYA-ACTIVATION/CONSTITUTION/CONSTITUTION.md")
    assert not issue_receipt("naya-test", CORRECT, incomplete, CURRENT_MAIN_SHA).passed
    no_reconciliation = {
        key: value for key, value in SOURCE_REVISIONS.items()
        if "SOURCE-PRECEDENCE-AND-NAVIGATION-RECONCILIATION-" not in key
    }
    assert not issue_receipt("naya-test", CORRECT, no_reconciliation, CURRENT_MAIN_SHA).passed


def test_receipt_rejects_stale_or_missing_main_sha():
    assert not issue_receipt("naya-test", CORRECT, SOURCE_REVISIONS, "").passed


def test_sign_in_accepts_structured_receipt_from_current_live_feed():
    result = check_sign_in(_good_sign_in(), CURRENT_MAIN_SHA, {1867, 2175})
    assert result.passed, result.failures


def test_sign_in_rejects_archived_feed():
    record = _good_sign_in()
    record["feed_issue"] = 1354
    record["comment_url"] = f"https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1354#issuecomment-{record['comment_id']}"
    start = record["comment_body"].index(RECEIPT_START) + len(RECEIPT_START)
    end = record["comment_body"].index(RECEIPT_END)
    payload = json.loads(record["comment_body"][start:end])
    payload["feed_issue"] = 1354
    record["comment_body"] = _comment_body(payload)
    record["comment_body_sha256"] = hashlib.sha256(record["comment_body"].encode("utf-8")).hexdigest()
    assert not check_sign_in(record, CURRENT_MAIN_SHA, {1867, 2175}).passed


def test_sign_in_rejects_payload_or_body_mismatch():
    record = _good_sign_in()
    record["comment_body"] += "edited after posting"
    assert not check_sign_in(record, CURRENT_MAIN_SHA, {1867, 2175}).passed


def test_sign_out_requires_same_feed_and_exact_sign_in_id():
    sign_in = _good_sign_in()
    sign_out = _good_sign_out(sign_in)
    assert check_sign_out(sign_in, sign_out, CURRENT_MAIN_SHA, {1867, 2175}).passed
    sign_out["feed_issue"] = 2175
    sign_out["comment_url"] = f"https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2175#issuecomment-{sign_out['comment_id']}"
    start = sign_out["comment_body"].index(RECEIPT_START) + len(RECEIPT_START)
    end = sign_out["comment_body"].index(RECEIPT_END)
    payload = json.loads(sign_out["comment_body"][start:end])
    payload["feed_issue"] = 2175
    sign_out["comment_body"] = _comment_body(payload)
    sign_out["comment_body_sha256"] = hashlib.sha256(sign_out["comment_body"].encode("utf-8")).hexdigest()
    assert not check_sign_out(sign_in, sign_out, CURRENT_MAIN_SHA, {1867, 2175}).passed


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
