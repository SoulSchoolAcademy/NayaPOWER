"""D35 tests — Preventing Stale Qualifications From Being Republished.

Every test asserts against the core rule:
  StaleWriter -> RejectPublication
  RevokedEvidence -> NoStaleCertification
  IndependentValidSupport -> PreserveSupportedClaim

And the invariant: PublishedCurrent(P) ⇒ ValidDependencies(P, now).
"""
import pytest

from drift_canary import d35_publication as d35
from drift_canary.d35_publication import (
    PublicationAuthority, STALE_DEPENDENCY, WRITE_CONFLICT, PUBLISHED,
    TOKEN_REJECTED, SCOPE_VIOLATION, DUPLICATE_EVENT, CURRENT, INVALID,
    FencingToken, RevisionTriple,
)


def make_authority():
    """Standard world: E1, E2 evidence; claim C on E1; claim D on E2."""
    a = PublicationAuthority()
    a.register_evidence("E1")
    a.register_evidence("E2")
    a.qualify("C", "REQUALIFIED", ("E1",), scope=frozenset({"staging"}))
    a.qualify("D", "REQUALIFIED", ("E2",), scope=frozenset({"staging"}))
    return a


# ----------------------------------------------------------------------
# Sharpest case (register version): paused writer vs revocation vs VERIFY
# ----------------------------------------------------------------------
def test_sharpest_case_paused_writer_rejected():
    a = make_authority()
    # Writer reads Claim C (REQUALIFIED), then gets paused.
    manifest_w, token_w = a.read_for_write("C", "writer-W")
    # E1 revoked.
    a.revoke_evidence("E1")
    # VERIFY publishes the new truth: C is SUSPENDED.
    a.qualify("C", "SUSPENDED", (), scope=frozenset())
    # Writer resumes and tries to publish the OLD REQUALIFIED summary.
    out = a.publish_summary(manifest_w, "C is REQUALIFIED (stale)",
                            frozenset({"staging"}))
    assert not out.ok
    assert out.reason == STALE_DEPENDENCY
    a.assert_invariant()


def test_sharpest_case_fencing_token_does_not_save_stale_writer():
    a = make_authority()
    # W reads at R5-equivalent: REQUALIFIED on E1, holding a VALID token.
    manifest_w, token_w = a.read_for_write("C", "W")
    assert a._token_valid(token_w)  # the token itself is legitimate
    # E1 revoked (evidence stream moves); VERIFY republishes SUSPENDED.
    a.revoke_evidence("E1")
    a.qualify("C", "SUSPENDED", (), scope=frozenset())
    # W attempts publication at R8 with its valid R5 token.
    out = a.publish_summary(manifest_w, "stale summary", frozenset({"staging"}))
    assert not out.ok and out.reason == STALE_DEPENDENCY
    # The token was valid; the EVIDENCE VERSION check is what rejected it.
    a.assert_invariant()


def test_rebased_writer_converges():
    a = make_authority()
    manifest_w, _ = a.read_for_write("C", "W")
    a.revoke_evidence("E1")
    a.qualify("C", "SUSPENDED", (), scope=frozenset())
    out = a.publish_summary(manifest_w, "stale", frozenset({"staging"}))
    assert out.reason == STALE_DEPENDENCY
    # W rebases: fresh read, recompute against current state, republish only
    # what current evidence supports (SUSPENDED, empty scope here).
    manifest2, _ = a.read_for_write("C", "W")
    out2 = a.publish_summary(manifest2, "C is SUSPENDED", frozenset())
    assert out2.ok and out2.reason == PUBLISHED
    a.assert_invariant()


def test_concurrent_fresh_writer_publishes_legitimately():
    a = make_authority()
    manifest_w, _ = a.read_for_write("C", "W")   # W reads, pauses
    a.revoke_evidence("E1")
    a.qualify("C", "SUSPENDED", (), scope=frozenset())
    # A concurrent writer with a FRESH read publishes legitimately.
    manifest_f, _ = a.read_for_write("C", "fresh")
    out = a.publish_summary(manifest_f, "C is SUSPENDED (fresh)",
                            frozenset())
    assert out.ok and out.reason == PUBLISHED
    # The stale writer is still rejected — freshness is per-writer. The head
    # moved under it (WRITE_CONFLICT) and its dependencies are stale
    # (STALE_DEPENDENCY): either way the stale write never becomes authority.
    out_w = a.publish_summary(manifest_w, "stale", frozenset({"staging"}))
    assert not out_w.ok and out_w.reason in (STALE_DEPENDENCY, WRITE_CONFLICT)
    a.assert_invariant()


def test_successor_sealed_before_revocation_fails_reconciliation():
    a = make_authority()
    package = a.seal_successor_package("C")   # sealed while REQUALIFIED on E1
    a.revoke_evidence("E1")
    a.qualify("C", "SUSPENDED", (), scope=frozenset())
    out = a.reconcile_package(package)
    assert not out.ok and out.reason == STALE_DEPENDENCY
    # History remains readable — only CURRENT certification is withheld.
    assert package["verdict_at_seal"] == "REQUALIFIED"
    a.assert_invariant()


def test_successor_sealed_after_revocation_reconciles():
    a = make_authority()
    a.revoke_evidence("E1")
    a.qualify("C", "SUSPENDED", (), scope=frozenset())
    package = a.seal_successor_package("C")
    out = a.reconcile_package(package)
    assert out.ok
    a.assert_invariant()


# ----------------------------------------------------------------------
# Selectivity: unaffected claims survive without rebuild
# ----------------------------------------------------------------------
def test_unaffected_claim_preserved_without_rebuild():
    a = make_authority()
    manifest_d, _ = a.read_for_write("D", "writer-D")
    out = a.publish_summary(manifest_d, "D is REQUALIFIED", frozenset({"staging"}))
    assert out.ok
    frag_id = out.fragment_id
    # E1 revoked — D depends only on E2.
    a.revoke_evidence("E1")
    a.qualify("C", "SUSPENDED", (), scope=frozenset())
    # D's fragment is still CURRENT: no rebuild was needed, none happened.
    assert a.read_current(frag_id) == CURRENT
    a.assert_invariant()


def test_per_fragment_manifests_no_global_rebuild():
    a = make_authority()
    m_c, _ = a.read_for_write("C", "w")
    m_d, _ = a.read_for_write("D", "w")
    oc = a.publish_summary(m_c, "C summary", frozenset({"staging"}))
    assert oc.ok
    # The head moved under D's writer; the protocol says rebase, not retry.
    od_rebased, _ = a.read_for_write("D", "w")
    od = a.publish_summary(od_rebased, "D summary", frozenset({"staging"}))
    assert od.ok
    a.revoke_evidence("E1")
    # C's fragment synchronously INVALID; D's untouched.
    assert a.fragments[oc.fragment_id].status == INVALID
    assert a.fragments[od.fragment_id].status == CURRENT
    a.assert_invariant()


# ----------------------------------------------------------------------
# Revocation effective BEFORE refresh: synchronous invalidation
# ----------------------------------------------------------------------
def test_revocation_invalidates_synchronously_before_refresh():
    a = make_authority()
    m, _ = a.read_for_write("C", "w")
    out = a.publish_summary(m, "C summary", frozenset({"staging"}))
    assert out.ok
    # No refresh has run. Revocation alone must invalidate.
    a.revoke_evidence("E1")
    assert a.fragments[out.fragment_id].status == INVALID
    assert a.read_current(out.fragment_id) == INVALID
    a.assert_invariant()


def test_read_time_verification_catches_stale_without_notification():
    """Even if the synchronous invalidation were missed (notification loss),
    the read-time check catches the stale fragment. Notification loss may
    delay refresh — it must never restore eligibility."""
    a = make_authority()
    m, _ = a.read_for_write("C", "w")
    out = a.publish_summary(m, "C summary", frozenset({"staging"}))
    assert out.ok
    # Simulate a missed invalidation: force the fragment back to CURRENT.
    a.fragments[out.fragment_id].status = CURRENT
    a.revoke_evidence("E1")
    a.fragments[out.fragment_id].status = CURRENT  # notification lost
    assert a.read_current(out.fragment_id) == INVALID
    a.assert_invariant()


# ----------------------------------------------------------------------
# Adversarial interleaving: delayed writer vs revocation vs fresh writer
# ----------------------------------------------------------------------
def test_adversarial_interleaving_invariant_holds_every_step():
    a = make_authority()
    log = []

    def step(name, fn):
        r = fn()
        a.assert_invariant()  # invariant after EVERY step
        log.append(name)
        return r

    m_w, _ = step("W reads C", lambda: a.read_for_write("C", "W"))
    step("publish W's fresh summary", lambda: a.publish_summary(
        m_w, "C ok", frozenset({"staging"})))
    step("E1 revoked", lambda: a.revoke_evidence("E1"))
    step("VERIFY qualifies C SUSPENDED", lambda: a.qualify(
        "C", "SUSPENDED", (), scope=frozenset()))
    m_f, _ = step("fresh writer reads", lambda: a.read_for_write("C", "F"))
    out_f = step("fresh writer publishes", lambda: a.publish_summary(
        m_f, "C suspended", frozenset()))
    assert out_f.ok
    # Delayed W tries its ORIGINAL manifest again (never rebased).
    out_w = step("stale W retries", lambda: a.publish_summary(
        m_w, "C ok (stale)", frozenset({"staging"})))
    assert not out_w.ok
    assert out_w.reason in (STALE_DEPENDENCY, WRITE_CONFLICT)
    # Async repair runs for the invalidated fragment.
    step("repair runs", lambda: a.repair_fragment(out_f.fragment_id, "repair"))
    # No CURRENT fragment anywhere has invalid dependencies.
    for fid, frag in a.fragments.items():
        if frag.status == CURRENT:
            assert a._dependencies_valid(frag.manifest), fid
    assert log  # the interleaving actually ran


def test_blind_retry_without_rebase_rejected_again():
    a = make_authority()
    m, _ = a.read_for_write("C", "W")
    a.revoke_evidence("E1")
    a.qualify("C", "SUSPENDED", (), scope=frozenset())
    out1 = a.publish_summary(m, "stale", frozenset({"staging"}))
    assert out1.reason == STALE_DEPENDENCY
    # Blind retry with the same stale manifest: rejected again, never applied.
    out2 = a.publish_summary(m, "stale", frozenset({"staging"}))
    assert not out2.ok and out2.reason == STALE_DEPENDENCY
    a.assert_invariant()


# ----------------------------------------------------------------------
# Negative controls
# ----------------------------------------------------------------------
def test_forged_token_rejected():
    a = make_authority()
    m, _ = a.read_for_write("C", "W")
    forged = FencingToken(token_id="tok-evil", worker_id="evil",
                          issued_at=RevisionTriple(0, 0, 0),
                          authority_id=999999)
    bad_manifest = d35.FragmentManifest(
        fragment_id=m.fragment_id, claim_id=m.claim_id,
        qualification_rev_at_read=m.qualification_rev_at_read,
        evidence_deps_at_read=dict(m.evidence_deps_at_read),
        projection_head_at_read=m.projection_head_at_read,
        scope_at_read=m.scope_at_read,
        token=forged)
    out = a.publish_summary(bad_manifest, "evil", frozenset({"staging"}))
    assert not out.ok and out.reason == TOKEN_REJECTED
    a.assert_invariant()


def test_scope_widening_rejected():
    a = make_authority()
    m, _ = a.read_for_write("C", "W")  # C qualified for staging only
    out = a.publish_summary(m, "C holds in production",
                            frozenset({"staging", "production"}))
    assert not out.ok and out.reason == SCOPE_VIOLATION
    a.assert_invariant()


def test_write_conflict_on_moved_head():
    a = make_authority()
    m, _ = a.read_for_write("C", "W")
    # Someone else publishes first: the head moves under W.
    m2, _ = a.read_for_write("D", "other")
    assert a.publish_summary(m2, "D summary", frozenset({"staging"})).ok
    out = a.publish_summary(m, "C summary", frozenset({"staging"}))
    assert not out.ok and out.reason == WRITE_CONFLICT
    a.assert_invariant()


def test_smart_note_event_id_idempotent():
    a = make_authority()
    out1 = a.append_smart_note("evt-1", "C", "note body")
    assert out1.ok
    out2 = a.append_smart_note("evt-1", "C", "note body")
    assert not out2.ok and out2.reason == DUPLICATE_EVENT
    # Exactly one head bump for the logical event.
    assert a.projection_head == out1.projection_rev
    a.assert_invariant()


def test_index_pointer_cas():
    a = make_authority()
    out1 = a.replace_index_pointer("ptr-v2", None)
    assert out1.ok
    # Stale expected-old: rejected, pointer unchanged.
    out2 = a.replace_index_pointer("ptr-v3", None)
    assert not out2.ok and out2.reason == WRITE_CONFLICT
    assert a.index_pointer == "ptr-v2"
    out3 = a.replace_index_pointer("ptr-v3", "ptr-v2")
    assert out3.ok and a.index_pointer == "ptr-v3"
    a.assert_invariant()


def test_crash_recovery_exactly_once():
    a = make_authority()
    a.record_intent("evt-9", "append_smart_note",
                    {"claim_id": "C", "content": "crash note"})
    # Crash before application. Recovery replays exactly once...
    replayed = a.recover()
    assert replayed == ["evt-9"]
    # ...and a second recovery is a no-op (idempotent).
    assert a.recover() == []
    assert len(a.seen_event_ids) == 1
    a.assert_invariant()


# ----------------------------------------------------------------------
# Positive controls
# ----------------------------------------------------------------------
def test_suspended_to_requalified_gets_new_revision_and_evidence():
    a = make_authority()
    q1 = a.qualifications["C"]
    a.revoke_evidence("E1")
    qs = a.qualify("C", "SUSPENDED", (), scope=frozenset())
    assert qs.qualification_rev > q1.qualification_rev
    # New evidence arrives; requalification is allowed with a NEWER revision.
    a.register_evidence("E3")
    qr = a.qualify("C", "REQUALIFIED", ("E3",), scope=frozenset({"staging"}))
    assert qr.qualification_rev > qs.qualification_rev
    assert qr.evidence_deps != q1.evidence_deps  # new evidence, not resurrected
    # The new qualification publishes cleanly.
    m, _ = a.read_for_write("C", "W")
    out = a.publish_summary(m, "C requalified on E3", frozenset({"staging"}))
    assert out.ok
    a.assert_invariant()


def test_three_revision_streams_are_independent():
    a = make_authority()
    t0 = a.revisions.current()
    a.revoke_evidence("E1")                       # evidence stream only
    t1 = a.revisions.current()
    assert t1.evidence_rev > t0.evidence_rev
    assert t1.qualification_rev == t0.qualification_rev
    assert t1.projection_rev == t0.projection_rev
    a.qualify("C", "SUSPENDED", (), scope=frozenset())  # qualification only
    t2 = a.revisions.current()
    assert t2.qualification_rev > t1.qualification_rev
    assert t2.evidence_rev == t1.evidence_rev
    a.append_smart_note("evt-x", "D", "x")        # projection only
    t3 = a.revisions.current()
    assert t3.projection_rev > t2.projection_rev
    assert t3.evidence_rev == t2.evidence_rev
    assert t3.qualification_rev == t2.qualification_rev


def test_fencing_tokens_are_monotonic_per_authority():
    a = make_authority()
    _, t1 = a.read_for_write("C", "W")
    _, t2 = a.read_for_write("C", "W")
    assert t1.token_id != t2.token_id
    a.assert_invariant()


def test_offline_successor_reads_history_withholds_certification():
    a = make_authority()
    package = a.seal_successor_package("C")
    a.revoke_evidence("E1")
    # The successor can still READ the sealed history...
    assert package["verdict_at_seal"] == "REQUALIFIED"
    assert "E1" in package["evidence_pins"]
    # ...but cannot treat the former PASS as current certification.
    out = a.reconcile_package(package)
    assert not out.ok and out.reason == STALE_DEPENDENCY
    a.assert_invariant()


def test_repair_never_resurrects_stale_manifest():
    a = make_authority()
    m, _ = a.read_for_write("C", "W")
    out = a.publish_summary(m, "C summary", frozenset({"staging"}))
    assert out.ok
    old_manifest = a.fragments[out.fragment_id].manifest
    a.revoke_evidence("E1")
    a.qualify("C", "SUSPENDED", (), scope=frozenset())
    # Repair recomputes against CURRENT state; the stale manifest is gone.
    rout = a.repair_fragment(out.fragment_id, "repair")
    assert rout.ok
    new_manifest = a.fragments[out.fragment_id].manifest
    assert new_manifest.qualification_rev_at_read != \
        old_manifest.qualification_rev_at_read
    a.assert_invariant()
