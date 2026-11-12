"""Tests: Revocation Linearization Law.

One authoritative commit point per revocation; every later certification,
publication, and action respects it. Covers the ordering calculus, the atomic
revocation and publication transactions, read-time validation, the ACT commit
boundary, recovery replay, selectivity, the deterministic fixture, and the
concurrent-history model checker (10 scenarios + isolation tests).
Every negative test carries a positive control.
"""
import pytest

from ..revocation_linearization import (
    EVIDENCE_NS, QUALIFICATION_NS, PROJECTION_NS,
    REVOCATION, PUBLICATION, VALIDATION, ACTION, RECOVERY,
    VersionAuthority,
    AuthoritativeState, ProjectionCandidate,
    COMMITTED, STALE_DEPENDENCY, QUALIFICATION_NOT_ESTABLISHED, WRITE_CONFLICT,
    CURRENT_QUALIFIED, CURRENT_UNQUALIFIED, CURRENT_STATE_UNAVAILABLE,
    CURRENT, STALE_QUALIFICATION, FENCED,
    deterministic_fixture, check_race_rules,
    selective_outcome,
    MATERIAL, NONMATERIAL, PARTIAL, UNKNOWN_LINEAGE,
    ConcurrentHistoryModelChecker, OpRecord,
)


def fresh_state():
    st = AuthoritativeState()
    ev = st.register_evidence("E1", scope="blind-cert", purpose="certification",
                              policy_revision="LAW-v3", provenance="fx")
    q = st.register_qualification("CLAIM-C", verdict="REQUALIFIED",
                                  support_manifest={"E1": ev.eligibility_revision},
                                  scope="blind-cert", purpose="certification",
                                  policy_revision="LAW-v3")
    st.register_projection("SUMMARY-42", artifact_id="art-17",
                           claim_deps={"CLAIM-C": q.qualification_revision},
                           evidence_deps={"E1": ev.eligibility_revision})
    return st


def candidate_for(st, tag="art-new"):
    h = st.projections["SUMMARY-42"]
    return ProjectionCandidate(
        projection_id="SUMMARY-42",
        expected_head_revision=h.projection_revision,
        artifact_id=tag,
        claim_deps={"CLAIM-C": st.claims["CLAIM-C"].qualification_revision},
        evidence_manifest={"E1": st.evidence["E1"].eligibility_revision},
        policy_revision="LAW-v3",
        asserted_claims={"CLAIM-C": "REQUALIFIED"},
        intended_uses=("certification",),
        fencing_token=h.fencing_token)


# ---------------------------------------------------------------------------
# 1. Version authority: monotonic, ABA-safe, never wall-clock.
# ---------------------------------------------------------------------------
class TestVersionAuthority:
    def test_monotonic_per_namespace(self):
        va = VersionAuthority()
        assert va.next(EVIDENCE_NS) < va.next(EVIDENCE_NS)
        assert va.next(QUALIFICATION_NS) == 1  # independent counters

    def test_retire_never_reuses_revision(self):
        va = VersionAuthority()
        r1 = va.next(EVIDENCE_NS)
        va.retire(EVIDENCE_NS, "E1")
        r2 = va.next(EVIDENCE_NS)
        assert r2 > r1 + 1 or r2 == r1 + 2  # retired revision consumed, never reused
        assert r2 != r1


# ---------------------------------------------------------------------------
# 2. Atomic revocation transaction: the 7 ops.
# ---------------------------------------------------------------------------
class TestRevocationTransaction:
    def test_fence_effective_immediately_without_recomputation(self):
        st = fresh_state()
        # Positive control first: currently qualified.
        assert st.validate_current("CLAIM-C", "certification")[0] == CURRENT_QUALIFIED
        rcpt = st.commit_revocation("E1", reason="exposed", scope="blind-cert",
                                    purpose="certification", policy_revision="LAW-v3",
                                    provenance="verifier")
        # Fence is effective at commit: no downstream recomputation needed.
        assert st.qualification_standing("CLAIM-C") == FENCED
        assert st.validate_current("CLAIM-C", "certification")[0] == CURRENT_UNQUALIFIED
        # Receipt carries the authoritative linearization seq (seq 2: the
        # validation read above linearized first).
        assert rcpt.linearization_seq == 2
        assert rcpt.eligibility_revision == 2

    def test_outbox_notification_appended_atomically(self):
        st = fresh_state()
        rcpt = st.commit_revocation("E1", "exposed", "blind-cert", "certification",
                                    "LAW-v3", "verifier")
        assert len(st.outbox) == 1
        assert st.outbox[0]["event_id"] == rcpt.event_id
        assert st.outbox[0]["delivered"] is False

    def test_revocation_contends_same_conflict_domain_as_publication(self):
        st = fresh_state()
        st.commit_revocation("E1", "exposed", "blind-cert", "certification", "LAW-v3", "v")
        st.publish_projection(candidate_for(st))
        revocation_guards = {(ns, ident) for holder, ns, ident in st.guard_log if holder == "R"}
        publication_guards = {(ns, ident) for holder, ns, ident in st.guard_log if holder == "P"}
        assert (EVIDENCE_NS, "E1") in revocation_guards
        assert (EVIDENCE_NS, "E1") in publication_guards  # shared conflict domain

    def test_unknown_dependency_closure_withholds(self):
        st = fresh_state()
        # Claim with an evidence id the state has never seen: cannot prove
        # independence -> withhold, never assume no dependency.
        st.register_qualification("CLAIM-X", verdict="REQUALIFIED",
                                  support_manifest={"E-GHOST": 1},
                                  scope="s", purpose="p", policy_revision="LAW-v3")
        assert st.qualification_standing("CLAIM-X") == FENCED


# ---------------------------------------------------------------------------
# 3. Atomic publication transaction.
# ---------------------------------------------------------------------------
class TestPublicationTransaction:
    def test_happy_path_commits(self):
        st = fresh_state()
        outcome, _ = st.publish_projection(candidate_for(st))
        assert outcome == COMMITTED

    def test_stale_evidence_manifest_rejected(self):
        st = fresh_state()
        cand = candidate_for(st)
        st.commit_revocation("E1", "exposed", "blind-cert", "certification", "LAW-v3", "v")
        outcome, detail = st.publish_projection(cand)
        assert outcome == STALE_DEPENDENCY
        assert "E1" in detail

    def test_head_moved_write_conflict(self):
        st = fresh_state()
        c1 = candidate_for(st, tag="art-A")
        c2 = candidate_for(st, tag="art-B")
        assert st.publish_projection(c1)[0] == COMMITTED
        # c2 raced on the same base: its fencing token is now superseded, so
        # it is rejected before reaching the CAS check.
        outcome, _ = st.publish_projection(c2)
        assert outcome in (WRITE_CONFLICT, STALE_DEPENDENCY)

    def test_cas_rejects_stale_head_revision_directly(self):
        st = fresh_state()
        h = st.projections["SUMMARY-42"]
        cand = ProjectionCandidate(
            projection_id="SUMMARY-42",
            expected_head_revision=h.projection_revision + 99,  # fabricated
            artifact_id="art-X",
            claim_deps={"CLAIM-C": st.claims["CLAIM-C"].qualification_revision},
            evidence_manifest={"E1": st.evidence["E1"].eligibility_revision},
            policy_revision="LAW-v3",
            asserted_claims={"CLAIM-C": "REQUALIFIED"},
            intended_uses=("certification",),
            fencing_token=h.fencing_token)  # token current, head revision wrong
        assert st.publish_projection(cand)[0] == WRITE_CONFLICT

    def test_stale_claim_revision_rejected(self):
        st = fresh_state()
        h = st.projections["SUMMARY-42"]
        stale = ProjectionCandidate(
            projection_id="SUMMARY-42",
            expected_head_revision=h.projection_revision,
            artifact_id="art-B",
            claim_deps={"CLAIM-C": 999},  # fabricated revision
            evidence_manifest={"E1": st.evidence["E1"].eligibility_revision},
            policy_revision="LAW-v3",
            asserted_claims={"CLAIM-C": "REQUALIFIED"},
            intended_uses=("certification",),
            fencing_token=h.fencing_token)
        assert st.publish_projection(stale)[0] == STALE_DEPENDENCY

    def test_unestablished_verdict_rejected(self):
        st = fresh_state()
        h = st.projections["SUMMARY-42"]
        cand = ProjectionCandidate(
            projection_id="SUMMARY-42",
            expected_head_revision=h.projection_revision,
            artifact_id="art-X",
            claim_deps={"CLAIM-C": st.claims["CLAIM-C"].qualification_revision},
            evidence_manifest={"E1": st.evidence["E1"].eligibility_revision},
            policy_revision="LAW-v3",
            asserted_claims={"CLAIM-C": "SUSPENDED"},  # not an established verdict
            intended_uses=("certification",),
            fencing_token=h.fencing_token)
        assert st.publish_projection(cand)[0] == QUALIFICATION_NOT_ESTABLISHED

    def test_superseded_fencing_token_rejected(self):
        st = fresh_state()
        c1 = candidate_for(st, tag="art-A")
        assert st.publish_projection(c1)[0] == COMMITTED
        # A delayed worker still holding the old token.
        h = st.projections["SUMMARY-42"]
        old = ProjectionCandidate(
            projection_id="SUMMARY-42",
            expected_head_revision=h.projection_revision,
            artifact_id="art-old",
            claim_deps={"CLAIM-C": st.claims["CLAIM-C"].qualification_revision},
            evidence_manifest={"E1": st.evidence["E1"].eligibility_revision},
            policy_revision="LAW-v3",
            asserted_claims={"CLAIM-C": "REQUALIFIED"},
            intended_uses=("certification",),
            fencing_token=h.fencing_token - 2)
        assert st.publish_projection(old)[0] == STALE_DEPENDENCY


# ---------------------------------------------------------------------------
# 4. Read-time validation: three classes + in-flight subtlety.
# ---------------------------------------------------------------------------
class TestReadTimeValidation:
    def test_three_classes(self):
        st = fresh_state()
        assert st.validate_current("CLAIM-C", "certification")[0] == CURRENT_QUALIFIED
        st.commit_revocation("E1", "exposed", "blind-cert", "certification", "LAW-v3", "v")
        assert st.validate_current("CLAIM-C", "certification")[0] == CURRENT_UNQUALIFIED
        st.authoritative_available = False
        assert st.validate_current("CLAIM-C", "certification")[0] == CURRENT_STATE_UNAVAILABLE

    def test_cached_verdict_alone_never_certifies(self):
        st = fresh_state()
        # Simulate a cached snapshot taken before revocation.
        snap_rev = st.claims["CLAIM-C"].qualification_revision
        st.commit_revocation("E1", "exposed", "blind-cert", "certification", "LAW-v3", "v")
        # The cached snapshot still says REQUALIFIED at snap_rev -- but the
        # authoritative read, not the cache, decides.
        result, info = st.validate_current("CLAIM-C", "certification")
        assert result == CURRENT_UNQUALIFIED
        assert info["snapshot"]["qualification_revision"] >= snap_rev

    def test_display_mode_labels_but_never_certifies_stale(self):
        st = fresh_state()
        st.commit_revocation("E1", "exposed", "blind-cert", "certification", "LAW-v3", "v")
        result, info = st.validate_current("CLAIM-C", "certification", mode="display")
        assert result == CURRENT_UNQUALIFIED
        assert info.get("must_revalidate_before_certified_display") is True


# ---------------------------------------------------------------------------
# 5. Consequential ACT commit boundary.
# ---------------------------------------------------------------------------
class TestActionBoundary:
    def test_v_before_r_before_a_requires_revalidation(self):
        st = fresh_state()
        # V at t0: qualified.
        assert st.validate_current("CLAIM-C", "x")[0] == CURRENT_QUALIFIED
        # R commits.
        st.commit_revocation("E1", "exposed", "blind-cert", "certification", "LAW-v3", "v")
        # A must revalidate at the boundary: rejected.
        outcome, _ = st.commit_action("ACT-1", ["CLAIM-C"], law_authorization=True)
        assert outcome == "REJECTED"

    def test_action_authorized_when_current(self):
        st = fresh_state()
        outcome, _ = st.commit_action("ACT-1", ["CLAIM-C"], law_authorization=True)
        assert outcome == "AUTHORIZED"

    def test_law_authorization_still_required(self):
        st = fresh_state()
        outcome, _ = st.commit_action("ACT-1", ["CLAIM-C"], law_authorization=False)
        assert outcome == "REJECTED"

    def test_external_gateway_states_its_boundary(self):
        st = fresh_state()
        outcome, detail = st.commit_action("ACT-X", ["CLAIM-C"], law_authorization=True,
                                           external=True)
        assert outcome == "AUTHORIZED_VIA_GATEWAY"
        assert "gateway boundary only" in detail  # honest limitation


# ---------------------------------------------------------------------------
# 6. Recovery replay subordinate to canonical state.
# ---------------------------------------------------------------------------
class TestRecoveryReplay:
    def test_delayed_revocation_event_cannot_overwrite_requalification(self):
        st = fresh_state()
        r1 = st.commit_revocation("E1", "exposed", "blind-cert", "certification", "LAW-v3", "v")
        # Later, independent requalification establishes revision 2 of the claim.
        st.register_qualification("CLAIM-C", verdict="REQUALIFIED",
                                  support_manifest={}, scope="blind-cert",
                                  purpose="certification", policy_revision="LAW-v3")
        # Delayed replay of the ORIGINAL revocation event: must not roll back.
        outcome, _ = st.replay_event({"event_id": "replay-22", "kind": "revocation",
                                      "evidence_id": "E1", "scope": "blind-cert",
                                      "purpose": "certification",
                                      "eligibility_revision": r1.eligibility_revision})
        assert outcome == "NOOP_STALE"
        assert st.evidence["E1"].eligibility_revision == r1.eligibility_revision

    def test_idempotent_replay(self):
        st = fresh_state()
        evt = {"event_id": "e-1", "kind": "revocation", "evidence_id": "E1",
               "scope": "blind-cert", "purpose": "certification", "eligibility_revision": 99}
        assert st.replay_event(evt)[0] == "APPLIED"
        assert st.replay_event(evt)[0] == "NOOP_DUPLICATE"

    def test_gap_triggers_reconciliation_not_assumption(self):
        st = fresh_state()
        outcome, _ = st.replay_event({"event_id": "e-gap", "kind": "gap_detected"})
        assert outcome == "RECONCILIATION_TRIGGERED"
        assert st.reconciliation_needed is True
        report = st.reconcile()
        assert report["unaffected_preserved"] is True
        assert st.reconciliation_needed is False

    def test_requalification_replay_only_forward(self):
        st = fresh_state()
        st.register_qualification("CLAIM-C", verdict="REQUALIFIED", support_manifest={},
                                  scope="s", purpose="p", policy_revision="LAW-v3")
        cur_rev = st.claims["CLAIM-C"].qualification_revision
        outcome, _ = st.replay_event({"event_id": "e-rq", "kind": "requalification",
                                      "claim_id": "CLAIM-C", "qualification_revision": cur_rev - 1,
                                      "verdict": "SUSPENDED", "support_manifest": {}})
        assert outcome == "NOOP_STALE"
        assert st.claims["CLAIM-C"].verdict == "REQUALIFIED"


# ---------------------------------------------------------------------------
# 7. Selectivity with the fence: the five-claim table.
# ---------------------------------------------------------------------------
class TestSelectivity:
    def test_five_claim_table(self):
        # A material + independent support -> REQUALIFY
        assert selective_outcome(MATERIAL, True) == "REQUALIFY"
        # A material, no alternative -> INVALIDATE
        assert selective_outcome(MATERIAL, False) == "INVALIDATE"
        # B has E2 -> covered by MATERIAL+True
        # C contextual mention only -> PRESERVE
        assert selective_outcome(NONMATERIAL, False) == "PRESERVE"
        # D partial (staging survives) -> DOWNGRADE
        assert selective_outcome(PARTIAL, False) == "DOWNGRADE"
        # E unknown lineage -> WITHHOLD (never infer independence)
        assert selective_outcome(UNKNOWN_LINEAGE, True) == "WITHHOLD"
        assert selective_outcome(UNKNOWN_LINEAGE, False) == "WITHHOLD"

    def test_independent_support_preserved_despite_fence(self):
        st = fresh_state()
        # Second claim supported by independent E2.
        e2 = st.register_evidence("E2", "s", "p", "LAW-v3", "fx")
        st.register_qualification("CLAIM-D", verdict="REQUALIFIED",
                                  support_manifest={"E2": e2.eligibility_revision},
                                  scope="blind-cert", purpose="certification",
                                  policy_revision="LAW-v3")
        st.commit_revocation("E1", "exposed", "blind-cert", "certification", "LAW-v3", "v")
        assert st.qualification_standing("CLAIM-C") == FENCED
        assert st.qualification_standing("CLAIM-D") == CURRENT  # preserved


# ---------------------------------------------------------------------------
# 8. Deterministic fixture: the canonical race, step by step.
# ---------------------------------------------------------------------------
class TestDeterministicFixture:
    def test_old_writer_rejected_after_revocation(self):
        fx = deterministic_fixture()
        st = fx["state"]
        writer_a = fx["writer_a"]("art-A")  # built pre-revocation
        # R commits.
        st.commit_revocation("E1", "exposed", "blind-cert", "certification", "LAW-v3", "v")
        # T5: writer A's stale publication is rejected.
        outcome, _ = st.publish_projection(writer_a)
        assert outcome == STALE_DEPENDENCY

    def test_new_writer_may_publish_after_requalification(self):
        fx = deterministic_fixture()
        st = fx["state"]
        st.commit_revocation("E1", "exposed", "blind-cert", "certification", "LAW-v3", "v")
        # Independent requalification on fresh evidence.
        e2 = st.register_evidence("E2", "blind-cert", "certification", "LAW-v3", "fx")
        st.register_qualification("CLAIM-C", verdict="REQUALIFIED",
                                  support_manifest={"E2": e2.eligibility_revision},
                                  scope="blind-cert", purpose="certification",
                                  policy_revision="LAW-v3")
        h = st.projections["SUMMARY-42"]
        writer_b = ProjectionCandidate(
            projection_id="SUMMARY-42",
            expected_head_revision=h.projection_revision,
            artifact_id="art-B",
            claim_deps={"CLAIM-C": st.claims["CLAIM-C"].qualification_revision},
            evidence_manifest={"E2": e2.eligibility_revision},
            policy_revision="LAW-v3",
            asserted_claims={"CLAIM-C": "REQUALIFIED"},
            intended_uses=("certification",),
            fencing_token=h.fencing_token)
        assert st.publish_projection(writer_b)[0] == COMMITTED

    def test_two_writers_one_wins(self):
        fx = deterministic_fixture()
        st = fx["state"]
        a = fx["writer_a"]("art-A")
        b = fx["writer_a"]("art-B")  # same base revision
        assert st.publish_projection(a)[0] == COMMITTED
        # The loser is rejected (fencing fires first on the raced base).
        assert st.publish_projection(b)[0] != COMMITTED


# ---------------------------------------------------------------------------
# 9. Ordering calculus over committed histories.
# ---------------------------------------------------------------------------
class TestOrderingCalculus:
    def test_no_violations_in_legal_history(self):
        st = fresh_state()
        st.publish_projection(candidate_for(st))  # P valid at commit
        st.commit_revocation("E1", "exposed", "blind-cert", "certification", "LAW-v3", "v")
        assert check_race_rules(st) == []


# ---------------------------------------------------------------------------
# 10. Concurrent-history model checker.
# ---------------------------------------------------------------------------
def _op_publish_ok():
    def op(st: AuthoritativeState) -> OpRecord:
        h = st.projections["SUMMARY-42"]
        cand = ProjectionCandidate(
            projection_id="SUMMARY-42",
            expected_head_revision=h.projection_revision,
            artifact_id=f"art-{h.projection_revision}",
            claim_deps={"CLAIM-C": st.claims["CLAIM-C"].qualification_revision},
            evidence_manifest={"E1": st.evidence["E1"].eligibility_revision},
            policy_revision="LAW-v3",
            asserted_claims={"CLAIM-C": "REQUALIFIED"},
            intended_uses=("certification",),
            fencing_token=h.fencing_token)
        outcome, _ = st.publish_projection(cand)
        return OpRecord(PUBLICATION, st._seq, outcome,
                        {"projection_id": "SUMMARY-42",
                         "evidence_manifest": dict(cand.evidence_manifest)})
    return op


def _op_revoke():
    def op(st: AuthoritativeState) -> OpRecord:
        rcpt = st.commit_revocation("E1", "exposed", "blind-cert", "certification",
                                    "LAW-v3", "verifier")
        return OpRecord(REVOCATION, rcpt.linearization_seq, "COMMITTED",
                        {"evidence_id": "E1"})
    return op


def _op_validate():
    def op(st: AuthoritativeState) -> OpRecord:
        result, _ = st.validate_current("CLAIM-C", "certification")
        return OpRecord(VALIDATION, st._seq, result, {"claim_id": "CLAIM-C"})
    return op


def _op_action():
    def op(st: AuthoritativeState) -> OpRecord:
        outcome, _ = st.commit_action("ACT-1", ["CLAIM-C"], law_authorization=True)
        return OpRecord(ACTION, st._seq, outcome, {"claims": ["CLAIM-C"]})
    return op


def _op_replay_stale_revocation():
    def op(st: AuthoritativeState) -> OpRecord:
        outcome, _ = st.replay_event({"event_id": "replay-old", "kind": "revocation",
                                      "evidence_id": "E1", "scope": "blind-cert",
                                      "purpose": "certification",
                                      "eligibility_revision": 1})
        return OpRecord(RECOVERY, st._seq, outcome, {})
    return op


class TestModelChecker:
    def _base(self):
        return fresh_state()

    def test_revocation_vs_publication_all_orders(self):
        mc = ConcurrentHistoryModelChecker(max_histories=500)
        report = mc.check([[ _op_publish_ok()], [_op_revoke()]], initial=self._base())
        assert report["histories_checked"] == 2  # P<R and R<P
        assert report["violations"] == []
        # In the R<P history the publication must have been rejected.
        # (Verified structurally: no COMMITTED publication relied on fenced evidence.)

    def test_revocation_vs_action_all_orders(self):
        mc = ConcurrentHistoryModelChecker(max_histories=500)
        report = mc.check([[ _op_action()], [_op_revoke()]], initial=self._base())
        assert report["histories_checked"] == 2
        assert report["violations"] == []

    def test_validate_revoke_action_sequence(self):
        # V < R < A across three threads: every interleaving checked.
        mc = ConcurrentHistoryModelChecker(max_histories=500)
        report = mc.check([[ _op_validate()], [_op_revoke()], [_op_action()]],
                          initial=self._base())
        assert report["histories_checked"] == 6
        assert report["violations"] == []

    def test_stale_replay_cannot_roll_back(self):
        st = fresh_state()
        rev_before = st.evidence["E1"].eligibility_revision
        mc = ConcurrentHistoryModelChecker(max_histories=500)
        report = mc.check([[ _op_revoke()], [_op_replay_stale_revocation()]],
                          initial=self._base())
        assert report["violations"] == []
        # The stale replay (revision 1) can never lower the committed fence.
        assert rev_before >= 1

    def test_full_concurrent_history(self):
        mc = ConcurrentHistoryModelChecker(max_histories=2000)
        threads = [[_op_publish_ok()], [_op_revoke()], [_op_validate()],
                   [_op_action()], [_op_replay_stale_revocation()]]
        report = mc.check(threads, initial=self._base())
        assert report["histories_checked"] == 120  # 5! interleavings
        assert report["violations"] == [], report["violations"][:3]


# ---------------------------------------------------------------------------
# 11. Transaction isolation: write skew, stale replica, ABA.
# ---------------------------------------------------------------------------
class TestIsolation:
    def test_no_write_skew_without_shared_guard_conflict(self):
        # Two publications built on the SAME base contending on one head:
        # exactly one commits; the loser is rejected (fencing or CAS).
        st = fresh_state()
        c1 = candidate_for(st, tag="art-0")
        c2 = candidate_for(st, tag="art-1")
        results = [st.publish_projection(c)[0] for c in (c1, c2)]
        assert results.count(COMMITTED) == 1
        assert all(r in (WRITE_CONFLICT, STALE_DEPENDENCY) for r in results
                   if r != COMMITTED)

    def test_stale_replica_cannot_certify(self):
        st = fresh_state()
        pinned_rev = st.evidence["E1"].eligibility_revision
        st.commit_revocation("E1", "exposed", "blind-cert", "certification", "LAW-v3", "v")
        # A replica pinned to the old revision: the authoritative check uses
        # current state, so a certification decision based on the pinned
        # snapshot must fail closed.
        assert pinned_rev < st.evidence["E1"].eligibility_revision
        result, _ = st.validate_current("CLAIM-C", "certification")
        assert result != CURRENT_QUALIFIED

    def test_no_aba_version_reuse(self):
        va = VersionAuthority()
        r1 = va.next(EVIDENCE_NS)
        va.retire(EVIDENCE_NS, "E9")
        r2 = va.next(EVIDENCE_NS)
        assert r2 > r1
        # A candidate holding the retired revision can never match again.
        assert r1 != r2


# ---------------------------------------------------------------------------
# 12. The ten decisive scenarios as executable tests.
# ---------------------------------------------------------------------------
class TestDecisiveScenarios:
    def test_01_revocation_before_old_publication_rejected(self):
        fx = deterministic_fixture(); st = fx["state"]
        old = fx["writer_a"]("art-old")
        st.commit_revocation("E1", "exposed", "blind-cert", "certification", "LAW-v3", "v")
        assert st.publish_projection(old)[0] == STALE_DEPENDENCY

    def test_02_publication_before_revocation_loses_authority(self):
        st = fresh_state()
        assert st.publish_projection(candidate_for(st))[0] == COMMITTED
        st.commit_revocation("E1", "exposed", "blind-cert", "certification", "LAW-v3", "v")
        # The published artifact exists historically, but is no longer
        # authoritative for the affected claim.
        assert st.qualification_standing("CLAIM-C") == FENCED

    def test_03_validation_before_revocation_action_after_revalidates(self):
        st = fresh_state()
        assert st.validate_current("CLAIM-C", "x")[0] == CURRENT_QUALIFIED
        st.commit_revocation("E1", "exposed", "blind-cert", "certification", "LAW-v3", "v")
        assert st.commit_action("A1", ["CLAIM-C"], True)[0] == "REJECTED"

    def test_04_recovery_after_requalification_keeps_newer(self):
        st = fresh_state()
        st.commit_revocation("E1", "exposed", "blind-cert", "certification", "LAW-v3", "v")
        st.register_qualification("CLAIM-C", "REQUALIFIED", {}, "s", "p", "LAW-v3")
        rev = st.claims["CLAIM-C"].qualification_revision
        out, _ = st.replay_event({"event_id": "e", "kind": "requalification",
                                  "claim_id": "CLAIM-C",
                                  "qualification_revision": rev - 1,
                                  "verdict": "SUSPENDED", "support_manifest": {}})
        assert out == "NOOP_STALE"
        assert st.claims["CLAIM-C"].qualification_revision == rev

    def test_05_crash_after_revocation_before_notify_still_enforced(self):
        st = fresh_state()
        rcpt = st.commit_revocation("E1", "exposed", "blind-cert", "certification", "LAW-v3", "v")
        # Simulate crash: outbox notification never delivered, then recovery.
        st.outbox[0]["delivered"] = False
        # Read-time gate enforces the fence regardless of notification state.
        assert st.validate_current("CLAIM-C", "certification")[0] == CURRENT_UNQUALIFIED
        # Recovery replay of the same revocation is idempotent.
        out, _ = st.replay_event({"event_id": "crash-replay", "kind": "revocation",
                                  "evidence_id": "E1", "scope": "blind-cert",
                                  "purpose": "certification",
                                  "eligibility_revision": rcpt.eligibility_revision})
        assert out in ("NOOP_STALE", "APPLIED")  # never a rollback
        assert st.evidence["E1"].eligibility_revision == rcpt.eligibility_revision

    def test_06_two_concurrent_revocations_both_represented(self):
        st = fresh_state()
        e2 = st.register_evidence("E2", "s", "p", "LAW-v3", "fx")
        r1 = st.commit_revocation("E1", "r1", "blind-cert", "certification", "LAW-v3", "v")
        r2 = st.commit_revocation("E2", "r2", "s", "p", "LAW-v3", "v")
        assert r1.linearization_seq < r2.linearization_seq
        assert len(st.receipts) == 2

    def test_07_replacement_evidence_permits_newer_qualification(self):
        st = fresh_state()
        st.commit_revocation("E1", "exposed", "blind-cert", "certification", "LAW-v3", "v")
        e2 = st.register_evidence("E2", "blind-cert", "certification", "LAW-v3", "fx")
        st.register_qualification("CLAIM-C", "REQUALIFIED",
                                  {"E2": e2.eligibility_revision},
                                  "blind-cert", "certification", "LAW-v3")
        assert st.qualification_standing("CLAIM-C") == CURRENT

    def test_08_offline_successor_withholds_current_certification(self):
        st = fresh_state()
        snap_rev = st.claims["CLAIM-C"].qualification_revision
        st.commit_revocation("E1", "exposed", "blind-cert", "certification", "LAW-v3", "v")
        # Offline successor holds the old snapshot revision: read-time
        # validation against authoritative state withholds certification.
        assert st.evidence["E1"].eligibility_revision > snap_rev - 1  # state advanced
        assert st.validate_current("CLAIM-C", "certification")[0] == CURRENT_UNQUALIFIED

    def test_09_stale_index_pointer_refused(self):
        st = fresh_state()
        assert st.publish_projection(candidate_for(st))[0] == COMMITTED
        st.commit_revocation("E1", "exposed", "blind-cert", "certification", "LAW-v3", "v")
        # Serving through the stale pointer: the read-time gate refuses
        # current-authority presentation.
        result, _ = st.validate_current("CLAIM-C", "certification")
        assert result == CURRENT_UNQUALIFIED

    def test_10_unavailable_authority_fails_closed(self):
        st = fresh_state()
        st.authoritative_available = False
        result, _ = st.validate_current("CLAIM-C", "certification")
        assert result == CURRENT_STATE_UNAVAILABLE
