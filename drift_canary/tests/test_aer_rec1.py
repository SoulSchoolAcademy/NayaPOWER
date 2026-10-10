"""AER-REC-1 tests (SN-0806 + Crash-Recovery Lab): crash classification, atomic
commit + transactional outbox, GOV-OP-904 identity, the recovery state
machine, reconcile-don't-rewrite, per-operation recovery, stale-projection
rejection, multi-store containment, the C1-C15 matrix, the four recovery
mutations, the R1-R4 invariants, the seven lab fixtures, and AER-REC-001.
Every negative test gets a positive control."""
import pytest

from drift_canary.revocation_linearization import (
    AER_REC1_IMPLEMENTATION_STATUS,
    CRASH_CLASSES,
    CANONICAL_COMMIT_CONTENTS,
    RecoverableGovernance,
    CrashSimulated,
    RECOVERY_STATES,
    recover_governance_operation,
    recover_per_operation,
    ProjectionConsumer,
    epoch_81_82_example,
    lab_projection_guard_mutation,
    contain_multi_store,
    acquire_recovery_fence,
    rec_crash_matrix,
    rec_mutation_suite,
    rec_r_invariants,
    lab_withdrawal_replay_81_82,
    lab_promotion_crash_five_outcomes,
    lab_multi_store_partial_commit,
    lab_law_authorized_act_unknown,
    lab_two_worker_recovery,
    lab_chaos_checklist,
    lab_verifier_proof_table,
    lab_first_fixture,
    aer_rec_001,
    authorize_tax_action,
)


def _law():
    return {"receipt": "LAW-1", "valid": True}


def _rg1():
    rg = RecoverableGovernance()
    rg.gov.scope_mapping["s:A"] = {"parent": None, "children": [],
                                   "taxonomy_version": 0}
    rg.gov.active_qualifications["s:A"] = {
        "guarantee": "g:A", "status": "QUALIFIED", "qualification_rev": 0,
        "taxonomy_version": 0}
    return rg


def _merge(op="op-1", h="h-1"):
    return {"change_id": op, "change_type": "TAXONOMY_MERGE",
            "scopes": ["s:A"], "evidence": {"merged_id": "s:AB"},
            "law_receipt": _law()}, op, h


# --- Honest scope ----------------------------------------------------------------------------------

def test_implementation_status_is_conceptual():
    s = AER_REC1_IMPLEMENTATION_STATUS
    assert s["enters_as"] == "conceptual protocol + crash harness demonstration"
    assert "deployed atomic governance-outbox protocol" in s["not_verified"]
    assert "PR #2185 in production" in s["not_verified"]


def test_crash_classes_cover_seven():
    assert set(CRASH_CLASSES) == {"BEFORE_COMMIT", "DURING_COMMIT",
                                  "AFTER_COMMIT_BEFORE_ACK",
                                  "AFTER_COMMIT_BEFORE_PROJECTION",
                                  "DURING_OUTBOX_DELIVERY",
                                  "ACROSS_MULTIPLE_STORES",
                                  "DURING_EXTERNAL_ACT"}


def test_canonical_commit_contents():
    assert set(CANONICAL_COMMIT_CONTENTS) == {
        "taxonomy_state", "scope_mappings", "incident_qualification_state",
        "commit_identity", "receipt", "durable_outbox_event"}


def test_recovery_states_known():
    assert set(RECOVERY_STATES) == {"PREPARED", "COMMIT_OUTCOME_UNKNOWN",
                                    "COMMITTED", "PROJECTION_PENDING",
                                    "INDEPENDENTLY_VERIFIED", "ABORTED"}


# --- Identity (GOV-OP-904) -----------------------------------------------------------------------------

def test_identity_mismatch_rejected():
    rg = _rg1()
    ch, op, h = _merge()
    assert rg.commit_with_crash(ch, op, h, _law())["committed"]
    r = rg.commit_with_crash(ch, op, "DIFFERENT", _law())
    assert r["status"] == "IDENTITY_MISMATCH"


def test_committed_retry_returns_original():
    rg = _rg1()
    ch, op, h = _merge()
    ack1 = rg.commit_with_crash(ch, op, h, _law())
    ack2 = rg.commit_with_crash(ch, op, h, _law())
    assert ack2["status"] == "RECOVERED_ORIGINAL_RESULT"
    assert ack2["receipt"]["seq"] == ack1["receipt"]["seq"]
    # No duplicate outbox event minted.
    assert len(rg.durable_log[op]["outbox_event_ids"]) == 1


# --- Crash matrix ------------------------------------------------------------------------------------------

def test_crash_matrix_all_fifteen_pass():
    results = rec_crash_matrix()
    ids = [i for i, _, _ in results]
    assert "C1" in ids and "C15" in ids and "C6b" in ids
    bad = [(i, n) for i, v, n in results if v != "PASS"]
    assert not bad, bad


def test_before_commit_discards_nothing_applied():
    rg = _rg1()
    rg.crash_at = {"BEFORE_COMMIT"}
    ch, op, h = _merge()
    with pytest.raises(CrashSimulated):
        rg.commit_with_crash(ch, op, h, _law())
    assert rg.gov.epoch == 0
    r = recover_governance_operation(rg, op, h)
    assert r["status"] == "PROVABLY_UNCOMMITTED"


def test_during_commit_completes_without_reapply():
    rg = _rg1()
    rg.crash_at = {"DURING_COMMIT"}
    ch, op, h = _merge()
    with pytest.raises(CrashSimulated):
        rg.commit_with_crash(ch, op, h, _law())
    assert rg.gov.epoch == 1  # state applied exactly once
    r = recover_governance_operation(rg, op, h)
    assert r["status"] == "COMMIT_COMPLETED_BY_RECOVERY"
    assert rg.gov.epoch == 1  # never reapplied
    # The canonical receipt was finalized, not duplicated.
    seqs = [x["seq"] for x in rg.gov.receipts]
    assert len(seqs) == len(set(seqs))


def test_stale_replica_never_proves_abort():
    rg = _rg1()
    ch, op, h = _merge()
    rg.commit_with_crash(ch, op, h, _law())
    r = recover_governance_operation(rg, op, h, read_authoritative=False)
    assert not r["recovered"] and "stale replica" in r["reason"]
    # Positive control: the authoritative read recovers.
    assert recover_governance_operation(rg, op, h)["recovered"]


def test_no_timeout_converts_ambiguous_to_aborted():
    rg = _rg1()
    r = recover_governance_operation(rg, "op-ghost", "h-g")
    assert r["status"] == "COMMIT_OUTCOME_UNKNOWN"
    assert "no timeout converts" in r["note"]


def test_verified_abort_is_terminal():
    rg = _rg1()
    rg.durable_log["op-x"] = {"operation_id": "op-x", "proposal_hash": "h",
                              "state": "ABORTED", "applied": False,
                              "receipt": None, "outbox_event_ids": []}
    r = recover_governance_operation(rg, "op-x", "h")
    assert r["status"] == "ABORTED_VERIFIED_TERMINAL"


# --- Outbox ---------------------------------------------------------------------------------------------

def test_outbox_redelivery_idempotent():
    rg = _rg1()
    ch, op, h = _merge()
    ack = rg.commit_with_crash(ch, op, h, _law())
    eid = ack["outbox_event_ids"][0]
    assert rg.deliver_outbox(eid)["status"] == "DELIVERED"
    d2 = rg.deliver_outbox(eid)
    assert d2["status"] == "ALREADY_DELIVERED"
    assert "no duplicate effect" in d2["note"]


# --- Projections -------------------------------------------------------------------------------------------

def test_projection_consumer_dedup_stale_gap():
    c = ProjectionConsumer("c1")
    assert c.apply({"event_id": "e1", "revision": 1})["status"] == "APPLIED"
    assert c.apply({"event_id": "e1", "revision": 1})["status"] == "DEDUPED"
    # Gap: revision 3 while at 1 → fetch canonical, never decide from cache.
    g = c.apply({"event_id": "e3", "revision": 3})
    assert g["status"] == "GAP_DETECTED" and "never decide" in g["note"]
    # Stale: revision 1 while at 2.
    c.apply({"event_id": "e2", "revision": 2})
    s = c.apply({"event_id": "e1b", "revision": 1})
    assert s["status"] == "STALE_REPLAY_REJECTED"


def test_epoch_81_82_example():
    r = epoch_81_82_example()
    assert r["law_holds"]
    assert r["stale_81"] == "STALE_REPLAY_REJECTED"
    assert r["applied_revision"] == 82


def test_projection_guard_mutation():
    j = lab_projection_guard_mutation()
    assert j["intact_rejects"] and j["mutant_counterexample"]
    assert "epoch-81" in j["minimal"]


# --- Multi-store + fencing ------------------------------------------------------------------------------------

def test_multi_store_containment_modes():
    rg = _rg1()
    assert contain_multi_store(rg, "o1",
                               "single-canonical-boundary")["mode"] == "CANONICAL"
    d = contain_multi_store(rg, "o2", "qualified-distributed")
    assert d["mode"] == "DISTRIBUTED_FENCED"
    f = contain_multi_store(rg, "o3", "none")
    assert f["mode"] == "FAIL_CLOSED" and f["integrity_incident"]


def test_two_workers_one_transition():
    r = lab_two_worker_recovery()
    assert r["law_holds"]
    assert r["worker_a_fence"] == "FENCE_ACQUIRED"
    assert r["worker_b_fence"] == "WAIT"
    assert r["one_authoritative_transition"]


def test_fence_holder_reacquire_ok():
    rg = _rg1()
    assert acquire_recovery_fence(rg, "op-1", "A")["acquired"]
    assert acquire_recovery_fence(rg, "op-1", "A")["acquired"]  # same holder
    assert not acquire_recovery_fence(rg, "op-1", "B")["acquired"]


# --- Mutations + invariants ---------------------------------------------------------------------------------------

def test_recovery_mutations_all_counterexample():
    results = rec_mutation_suite()
    assert [i for i, _, _ in results] == ["M-outbox", "M-id", "M-fence",
                                          "M-proj"]
    bad = [(i, n) for i, v, n in results if v != "COUNTEREXAMPLE"]
    assert not bad, bad


def test_recovery_r_invariants():
    r = rec_r_invariants()
    assert r["holds"], r["issues"]
    assert "CommitUnknown(o)" in r["formula"]
    assert "escalate" in r["liveness"]


# --- Crash-Recovery Lab fixtures ---------------------------------------------------------------------------------------

def test_lab_withdrawal_replay_81_82():
    r = lab_withdrawal_replay_81_82()
    assert r["law_holds"]
    assert r["stale_replay"] == "STALE_REPLAY_REJECTED"
    assert r["b_qualification"] == "WITHDRAWN"
    assert not r["b_act_authorized"] and r["a_still_qualified"]


def test_lab_promotion_crash_five_outcomes():
    rows = lab_promotion_crash_five_outcomes()
    assert [c for c, _, _ in rows] == ["durable-confirms", "reliably-aborted",
                                      "neither-establishable",
                                      "incident-advanced", "id-hash-mismatch"]
    bad = [(c, n) for c, v, n in rows if v != "PASS"]
    assert not bad, bad


def test_lab_multi_store_partial_commit():
    r = lab_multi_store_partial_commit()
    assert r["law_holds"]
    assert r["containment"] == "FAIL_CLOSED"
    assert r["integrity_incident"]
    assert not r["old_parent_act_permitted"]


def test_lab_law_authorized_act_unknown():
    r = lab_law_authorized_act_unknown()
    assert r["law_holds"]
    assert r["reconciliation"] == "AMBIGUOUS_EXTERNAL_EFFECT"
    assert not r["new_execution_permitted"]


def test_lab_chaos_checklist_shape():
    items = lab_chaos_checklist()
    assert len(items) == 8
    assert items[0][0] == "chaos-1" and items[7][0] == "chaos-8"


def test_lab_verifier_proof_table():
    rows = lab_verifier_proof_table()
    assert [i for i, _ in rows] == ["atomic-authoritative-publication",
                                    "replay-idempotency",
                                    "monotone-eligibility",
                                    "evidence-preserving-split",
                                    "ambiguous-outcome-integrity",
                                    "selective-recovery",
                                    "crash-reconstruction"]
    bad = [i for i, v in rows if v != "PASS"]
    assert not bad, bad


def test_lab_first_fixture():
    r = lab_first_fixture()
    after = r["crash_after_commit"]
    assert after["worker_a"] == "FENCE_ACQUIRED"
    assert after["worker_b"] == "WAIT"
    assert after["stale_merge_replay"] == "STALE_REPLAY_REJECTED"
    assert after["b_stays_unqualified"] and after["a_preserves_eligibility"]
    assert after["epoch_never_backward"]
    before = r["crash_before_commit"]
    # A DIFFERENT reconstructed outcome: the withdrawal never happened.
    assert before["different_outcome"] and before["b_act_authorized"]
    assert "cannot create new authority" in r["demonstrated"]


def test_aer_rec_001_acceptance():
    r = aer_rec_001()
    assert r["acceptance"], {
        "matrix": r["matrix_failures"],
        "mutations": r["mutation_failures"],
        "invariants": r["invariant_issues"],
        "lab": r["lab"],
    }
