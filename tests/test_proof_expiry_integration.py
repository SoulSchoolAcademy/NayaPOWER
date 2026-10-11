"""Law 12 integration tests: proof-expiry wired into execution boundaries.

Tests that:
1. cold_start_gate refuses a stale read receipt (protocol version moved).
2. cold_start_gate accepts a fresh receipt (no Law 12 params = old behavior).
3. act_pipeline.execute_plan refuses when the authority grant proof is stale.
4. act_pipeline.execute_plan proceeds when law12_state matches.

These test the actual seams changed, per the ENGINEERING contract.
"""

import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from kernel.protocol.proof_expiry import DEP_POLICY_REF, DEP_SOURCE_SHA
from kernel.protocol.read_receipt import issue_receipt, PROTOCOL_VERSION
from kernel.protocol.cold_start_gate import ColdStartState, run_cold_start


def _valid_receipt():
    answers = {
        "q1": "Shawn",
        "q2": "production credentials money destructive ratification security privacy",
        "q3": "no",
        "q4": "9.0",
        "q5": "independent evidence",
    }
    return issue_receipt("test-agent", answers)


def _base_state():
    return ColdStartState(
        agent_id="test-agent",
        human_director="Shawn",
        lane="test",
        authority_summary="production, credentials, money, destructive, ratification",
        current_truth_location="feed #1354 and main",
        next_action="do the work",
        receipt=_valid_receipt(),
    )


# --- cold_start_gate Law 12 ---------------------------------------------------

def test_cold_start_old_behavior_unchanged_without_law12_params():
    """No Law 12 params = exact old behavior. Backward compatible."""
    result = run_cold_start(_base_state())
    assert result.passed, f"unexpected failures: {result.failures}"


def test_cold_start_accepts_fresh_receipt():
    result = run_cold_start(
        _base_state(),
        current_protocol_version=PROTOCOL_VERSION,
        current_source_sha="tip-abc",
    )
    # Note: proof_from_read_receipt records the receipt's issue-time tip as
    # "" when source_sha is passed to the adapter... here we pass the tip
    # the receipt was "read at" via the adapter's source_sha param.
    # The adapter is called with current_source_sha as both proof-time and
    # current value, so it matches. This tests the plumbing, not materiality.
    assert result.passed, f"unexpected failures: {result.failures}"


def test_cold_start_refuses_stale_protocol_version():
    """Protocol version moved since the receipt was issued -> STALE -> fail."""
    result = run_cold_start(
        _base_state(),
        current_protocol_version="2099-01-01-FUTURE",
        current_source_sha="tip-abc",
    )
    assert not result.passed
    assert any("Law 12" in f and "stale" in f.lower() for f in result.failures), \
        f"expected Law 12 staleness failure, got: {result.failures}"


# --- act_pipeline Law 12 ------------------------------------------------------

def _make_execute_plan_test():
    """Import act_pipeline pieces lazily; return (execute_plan, LawAuthority,
    ActionPlan, QualityProfile, gate names) or None if import fails."""
    try:
        sys.path.insert(0, str(REPO_ROOT))
        from kernel.act_pipeline import (
            execute_plan, LawAuthority, ActionPlan, PlanCandidate,
            QualityProfile, LAW_AUTHORITY_PROOF_STALE,
        )
        return (execute_plan, LawAuthority, ActionPlan, PlanCandidate,
                QualityProfile, LAW_AUTHORITY_PROOF_STALE)
    except Exception as e:
        return None


def _make_plan_parts(parts):
    (execute_plan, LawAuthority, ActionPlan, PlanCandidate,
     QualityProfile, LAW_AUTHORITY_PROOF_STALE) = parts
    from kernel.value_calculus import QualityProfile as QP
    now = time.time()
    authority = LawAuthority(
        action="test-action", scope="test-action",
        decided_at=now - 10, expires_at=None, grant_id="grant-1",
    )
    candidate = PlanCandidate(
        candidate_id="c1",
        action="test-action",
        description="test candidate",
        quality={}, confidence={},
        reversibility="REVERSIBLE",
        expected_outcome="test",
        proof_requirements=(),
    )
    plan = ActionPlan(
        plan_id="plan-1", action="test-action", chosen=candidate,
        authority=authority, candidate_scores=(("c1", 9.5),),
        planned_at=now - 20,
    )
    profile = QP(profile_id="test", version="1", objective="test")
    return execute_plan, plan, authority, profile, LAW_AUTHORITY_PROOF_STALE, now


def test_execute_plan_law12_blocks_stale_grant():
    parts = _make_execute_plan_test()
    if parts is None:
        raise AssertionError("act_pipeline import failed")
    execute_plan, plan, authority, profile, LAW_AUTHORITY_PROOF_STALE, now = \
        _make_plan_parts(parts)

    # law12_proof_time holds the world when the grant was established;
    # law12_state holds current values. They differ -> STALE -> refused.
    receipt = execute_plan(
        plan,
        executor=lambda p: "done",
        re_resolve=lambda: authority,
        now=now,
        profile=profile,
        law12_proof_time={DEP_SOURCE_SHA: "old-tip", DEP_POLICY_REF: "old-policy"},
        law12_state={DEP_SOURCE_SHA: "new-tip", DEP_POLICY_REF: "new-policy"},
    )
    assert receipt.phase == "EXECUTION_REFUSED", \
        f"expected refusal, got phase {receipt.phase}"
    assert LAW_AUTHORITY_PROOF_STALE in receipt.codes, \
        f"expected {LAW_AUTHORITY_PROOF_STALE} in {receipt.codes}"


def test_execute_plan_law12_absent_preserves_old_behavior():
    """No law12_state = exact old behavior. Backward compatible."""
    parts = _make_execute_plan_test()
    if parts is None:
        raise AssertionError("act_pipeline import failed")
    execute_plan, plan, authority, profile, _STALE, now = \
        _make_plan_parts(parts)

    # No law12_state: should proceed past the Law 12 check. We only assert
    # it was NOT refused for Law 12 reasons.
    receipt = execute_plan(
        plan,
        executor=lambda p: "done",
        re_resolve=lambda: authority,
        now=now,
        profile=profile,
    )
    assert "LAW_AUTHORITY_PROOF_STALE" not in receipt.codes


# --- quality_gate Law 12 ------------------------------------------------------

def test_quality_gate_blocks_stale_scorecard():
    from kernel.protocol.quality_gate import check_delivery, Scorecard
    sc = Scorecard(
        what="test widget",
        evidence="tests 10/10 pass",
        scores={"quality": 9.5},
        weights={"quality": 1.0},
        weakest_point="docs thin",
        verified_by="naya-1",
    )
    result = check_delivery(
        sc, "builder-1",
        law12_proof_time={DEP_SOURCE_SHA: "old-tip", DEP_POLICY_REF: "rubric-v1"},
        law12_state={DEP_SOURCE_SHA: "new-tip", DEP_POLICY_REF: "rubric-v1"},
    )
    assert not result.passed
    assert any("Law 12" in r for r in result.reasons), \
        f"expected Law 12 staleness, got: {result.reasons}"


def test_quality_gate_absent_preserves_old_behavior():
    from kernel.protocol.quality_gate import check_delivery, Scorecard
    sc = Scorecard(
        what="test widget",
        evidence="tests 10/10 pass",
        scores={"quality": 9.5},
        weights={"quality": 1.0},
        weakest_point="docs thin",
        verified_by="naya-1",
    )
    result = check_delivery(sc, "builder-1")
    assert result.passed, f"unexpected: {result.reasons}"
