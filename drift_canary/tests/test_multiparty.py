"""Tests: multi-obligation interaction invariants (3+ parties).

The decisive experiment: pairwise passes -> triple mismatch ->
refuse-or-requalify -> restore + concurrency variant -> cold successor
reconstructs. Plus the temporal/concurrency machinery (T1-T4 race,
commit-boundary eligibility, TOCTOU).
"""
import pytest

from ..migration import (
    ExecutionContext, EventRecord, InvariantSpec, MultiPartyInteraction,
    MultiPartyReceipt,
    JOIN_KEYS, INVARIANT_CATEGORIES, INVARIANT_KINDS,
    VERIFICATION_TECHNIQUES,
    check_joint_consistency, check_temporal_order,
    check_commit_eligibility, assess_multi_party,
)


def ctx(decision="D-100", principal="P-1", digest="H-1", target="T-1"):
    return ExecutionContext(decision, principal, digest, target)


def std_invariants():
    return (
        InvariantSpec(
            invariant_id="INV-JOINT-CTX", category="joint_identity",
            kind="SAFETY", predicate="spec:join_keys_equal@v3",
            positive_witness="all three receipts bind D-100/P-1/H-1/T-1",
            counterexample="KNOW binds D-101 while LAW binds D-102"),
        InvariantSpec(
            invariant_id="INV-ORDER", category="temporal_ordering",
            kind="TEMPORAL", predicate="spec:kap_lt_pfp_lt_commit@v3",
            positive_witness="seq 3 < 7 < 11 for D-100",
            counterexample="knowledge_applied seq 12 after plan_finalized 7"),
        InvariantSpec(
            invariant_id="INV-NO-ESCALATION",
            category="authority_non_escalation", kind="SAFETY",
            predicate="spec:law_supremacy@v3",
            positive_witness="lesson marked advisory; LAW denial blocked ACT",
            counterexample="ACT executed a lesson-flagged prohibited action"),
    )


def std_interaction(decision="D-100"):
    return MultiPartyInteraction(
        interaction_id="INT-KNOW-LAW-ACT", revision="v1",
        participant_obligations=("KNOW-001@v1", "LAW-002@v1", "ACT-003@v1"),
        execution_context=ctx(decision),
        invariants=std_invariants(),
        ordering_constraints=(("knowledge_applied", "plan_finalized"),
                              ("plan_finalized", "commit")),
        proof_requirements=("fault_injection", "independent_end_to_end"))


# ---------------------------------------------------------------------------
# Decisive experiment.
# ---------------------------------------------------------------------------
def test_exp_phase1_pairwise_passes():
    """Pairwise joint consistency holds for each pair in isolation."""
    ok, mm = check_joint_consistency({
        "KNOW": ctx("D-100"), "LAW": ctx("D-100")})
    assert ok and mm == ()
    ok2, mm2 = check_joint_consistency({
        "LAW": ctx("D-100"), "ACT": ctx("D-100")})
    assert ok2 and mm2 == ()


def test_exp_phase2_triple_mismatch_pairwise_green_joint_invalid():
    """The D-101/D-102 case: KNOW applied the lesson to D-101, LAW
    authorized D-102, ACT executed with D-102's authorization. Every
    pairwise check passes; the joint execution has no coherent decision."""
    ok_pair, _ = check_joint_consistency({
        "KNOW": ctx("D-101"), "LAW": ctx("D-101")})
    assert ok_pair  # pairwise green (as observed locally)
    ok, mismatches = check_joint_consistency({
        "KNOW": ctx("D-101"), "LAW": ctx("D-102"), "ACT": ctx("D-102")})
    assert not ok
    assert ("LAW", ("decision_id",)) in mismatches
    assert ("ACT", ("decision_id",)) in mismatches


def test_exp_phase3_combined_operation_must_refuse():
    """With the mismatch present, the multi-party assessment cannot
    qualify — the combined operation must refuse (or safely requalify
    after rebinding to one decision)."""
    inter = std_interaction("D-100")
    result = assess_multi_party(
        inter,
        {"KNOW": ctx("D-101"), "LAW": ctx("D-102"), "ACT": ctx("D-102")},
        (EventRecord("knowledge_applied", "D-100", 3),
         EventRecord("plan_finalized", "D-100", 7),
         EventRecord("commit", "D-100", 11)),
        ())
    assert result["joint_consistency"] == "VIOLATED"
    assert result["overall"] == "NOT_QUALIFIED"
    # Rebinding all participants to ONE coherent decision requalifies the
    # consistency leg (invariants still need their own proof).
    result2 = assess_multi_party(
        inter,
        {"KNOW": ctx("D-100"), "LAW": ctx("D-100"), "ACT": ctx("D-100")},
        (EventRecord("knowledge_applied", "D-100", 3),
         EventRecord("plan_finalized", "D-100", 7),
         EventRecord("commit", "D-100", 11)),
        ())
    assert result2["joint_consistency"] == "HOLDS"
    assert result2["temporal_order"] == "HOLDS"


def test_exp_phase4_concurrency_variant_t1_t4_race():
    """T1: KNOW returns E1. T2: LAW approves. T3: E1 becomes ineligible.
    T4: ACT commits using E1. The commit must be blocked — eligibility is
    re-verified against the commit snapshot, and the revocation is
    ordered before the commit boundary."""
    commit = EventRecord("commit", "D-100", seq=40)
    ok, reasons = check_commit_eligibility(
        commit,
        {"E1": (True, 38)},          # snapshot says eligible...
        (("E1", 39),))              # ...but revoked at seq 39 < commit 40
    assert not ok
    assert any("revoked at seq 39 before commit seq 40" in r for r in reasons)


def test_exp_phase4_commit_allowed_when_no_revocation():
    commit = EventRecord("commit", "D-100", seq=40)
    ok, reasons = check_commit_eligibility(
        commit, {"E1": (True, 38), "E2": (True, 38)}, ())
    assert ok
    assert reasons[-1] == "commit boundary eligibility holds"


def test_exp_phase4_cold_successor_reconstructs():
    """A cold successor with only the interaction, contexts, events and
    receipts reproduces the assessment — deterministic, twice."""
    inter = std_interaction("D-100")
    contexts = {"KNOW": ctx("D-100"), "LAW": ctx("D-100"),
                "ACT": ctx("D-100")}
    events = (EventRecord("knowledge_applied", "D-100", 3),
              EventRecord("plan_finalized", "D-100", 7),
              EventRecord("commit", "D-100", 11))
    receipts = (MultiPartyReceipt(
        interaction_id="INT-KNOW-LAW-ACT", revision="v1",
        join_keys={"decision_id": "D-100"},
        techniques_applied=("fault_injection",),
        positive_receipts=("POS-JOINT-1",),
        independent_verification="verifier-M: replay matched",
        qualification="REQUALIFIED"),)
    r1 = assess_multi_party(inter, contexts, events, receipts)
    r2 = assess_multi_party(inter, contexts, events, receipts)
    assert r1 == r2
    assert r1["overall"] == "QUALIFIED"
    assert r1["categories"]["joint_identity"] == ["PROVED"]


def test_exp_narrower_results_preserved_when_joint_fails():
    """Receipt invalidation recalculates the joint assessment without
    revoking proven components: pairwise results are narrower conclusions
    that survive the joint failure."""
    inter = std_interaction("D-100")
    good = MultiPartyReceipt(
        interaction_id="INT-KNOW-LAW-ACT", revision="v1",
        join_keys={"decision_id": "D-100"},
        techniques_applied=("fault_injection",),
        positive_receipts=("POS-JOINT-1",),
        independent_verification="verifier-M",
        qualification="REQUALIFIED")
    bad = MultiPartyReceipt(
        interaction_id="INT-KNOW-LAW-ACT", revision="v1",
        join_keys={"decision_id": "D-100"},
        techniques_applied=("fault_injection",),
        negative_receipts=("NEG-RACE-1",),
        independent_verification="verifier-M: T1-T4 race reproduced",
        qualification="REVOKED")
    contexts = {"KNOW": ctx("D-100"), "LAW": ctx("D-100"),
                "ACT": ctx("D-100")}
    events = (EventRecord("knowledge_applied", "D-100", 3),
              EventRecord("plan_finalized", "D-100", 7),
              EventRecord("commit", "D-100", 11))
    before = assess_multi_party(inter, contexts, events, (good,))
    assert before["overall"] == "QUALIFIED"
    after = assess_multi_party(inter, contexts, events, (good, bad))
    assert after["overall"] == "NOT_QUALIFIED"
    assert "FAILED" in after["invariant_status"].values()
    # Pairwise joint consistency still holds — the failure is scoped to
    # the joint invariants, not the components.
    assert after["joint_consistency"] == "HOLDS"


# ---------------------------------------------------------------------------
# Temporal ordering.
# ---------------------------------------------------------------------------
def test_temporal_order_lesson_after_plan_fails():
    ok, violations = check_temporal_order(
        (EventRecord("knowledge_applied", "D-100", 12),
         EventRecord("plan_finalized", "D-100", 7),
         EventRecord("commit", "D-100", 15)), "D-100")
    assert not ok
    assert ("knowledge_applied", "plan_finalized") in violations


def test_temporal_order_uses_sequence_not_timestamps():
    # Same wall-clock timestamp, different source-bound seq: order is
    # decided by seq within the correlation scope.
    ok, _ = check_temporal_order(
        (EventRecord("knowledge_applied", "D-100", 3, at="10:00:00"),
         EventRecord("plan_finalized", "D-100", 7, at="10:00:00"),
         EventRecord("commit", "D-100", 11, at="10:00:00")), "D-100")
    assert ok


def test_temporal_order_other_decisions_ignored():
    ok, _ = check_temporal_order(
        (EventRecord("knowledge_applied", "D-100", 3),
         EventRecord("plan_finalized", "D-100", 7),
         EventRecord("commit", "D-100", 11),
         EventRecord("knowledge_applied", "D-999", 50)), "D-100")
    assert ok


# ---------------------------------------------------------------------------
# Invariant hygiene.
# ---------------------------------------------------------------------------
def test_invariant_requires_counterexample():
    with pytest.raises(AssertionError):
        InvariantSpec(invariant_id="INV-X", category="joint_identity",
                      kind="SAFETY", predicate="spec:x@v1",
                      positive_witness="w", counterexample="")


def test_invariant_categories_complete():
    assert set(INVARIANT_CATEGORIES) == {
        "joint_identity", "temporal_ordering", "shared_consistency",
        "authority_non_escalation", "end_to_end_integrity",
        "failure_containment"}
    assert set(INVARIANT_KINDS) == {"SAFETY", "TEMPORAL", "LIVENESS"}
    assert set(VERIFICATION_TECHNIQUES) == {
        "formal_model", "fault_injection", "independent_end_to_end"}


def test_join_keys_complete():
    assert set(JOIN_KEYS) == {"decision_id", "principal_id",
                              "action_digest", "target_id"}


def test_execution_context_mismatch_fields():
    a, b = ctx("D-100", target="T-1"), ctx("D-100", target="T-2")
    assert not a.matches(b)
    assert a.mismatch_fields(b) == ("target_id",)


def test_multi_party_receipt_techniques_validated():
    with pytest.raises(AssertionError):
        MultiPartyReceipt(interaction_id="I", revision="v1", join_keys={},
                          techniques_applied=("vibes",))
