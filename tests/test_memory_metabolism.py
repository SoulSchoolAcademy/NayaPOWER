from kernel.memory_metabolism import (
    ACTIVE,
    ARCHIVED,
    DECAYED,
    QUARANTINED,
    SUPERSEDED,
    MemoryMetabolismError,
    archive,
    compress,
    create_record,
    decay,
    integrity_ok,
    metabolize,
    quarantine,
    reconcile,
    record_integrity,
    retrieve,
    strengthen,
    supersede,
)

NOW = "2026-10-08T09:45:00+00:00"
FRESH = "2026-10-01T09:45:00+00:00"
STALE = "2026-01-01T09:45:00+00:00"


def _rec(**over):
    kw = dict(content="Retention beats reconstruction", epistemic_state="LEARNING", now=FRESH)
    kw.update(over)
    return create_record(**kw)


def test_create_record_establishes_verifiable_integrity():
    record = _rec()
    assert record.memory_state == ACTIVE
    assert record.verification_weight == 0.0
    assert integrity_ok(record)
    assert record.integrity.startswith("MMI-")


def test_create_record_refuses_empty_content_and_unknown_epistemic():
    for kwargs in ({"content": ""}, {"epistemic_state": "VIBES"}):
        try:
            _rec(**kwargs)
        except MemoryMetabolismError as exc:
            assert str(exc) in ("content_missing", "epistemic_state_unknown")
        else:
            raise AssertionError(f"expected refusal for {kwargs}")


def test_integrity_excludes_id_from_own_preimage_like_checkpoint_id():
    record = _rec()
    first = record_integrity(record)
    record.verification_weight = 999.0  # mutate without recompute
    assert record_integrity(record) != first  # hash sees the mutation
    assert not integrity_ok(record)  # stored id no longer matches -> fail closed


def test_strengthen_bumps_weight_with_evidence_and_refreshes_verified_at():
    record = _rec()
    receipt = strengthen(record, "reused-in-trial-4", now=NOW)
    assert record.verification_weight == 1.0
    assert record.evidence == ["reused-in-trial-4"]
    assert record.last_verified_at == NOW
    assert integrity_ok(record)
    assert receipt["transition"] == "strengthen"
    assert receipt["receipt_id"].startswith("MMR-")


def test_strengthen_refuses_dead_records_and_missing_evidence():
    record = _rec()
    supersede(record, _rec(content="newer", now=FRESH), now=NOW)
    for fn, args in (
        (strengthen, (record, "evidence",)),
        (strengthen, (_rec(), "",)),
    ):
        try:
            fn(*args, **({} if len(args) == 2 else {"now": NOW}))
        except MemoryMetabolismError as exc:
            assert str(exc) in ("strengthen_refused_not_active", "strengthen_evidence_missing")
        else:
            raise AssertionError("expected strengthen refusal")


def test_supersede_retires_old_and_binds_lineage():
    old = _rec(content="old rule")
    new = _rec(content="new rule")
    receipt = supersede(old, new, now=NOW)
    assert old.memory_state == SUPERSEDED
    assert old.superseded_by == new.record_id
    assert old.superseded_at == NOW
    assert old.record_id in new.lineage
    assert integrity_ok(old) and integrity_ok(new)
    assert receipt["detail"] == f"superseded_by={new.record_id}"
    # stale record stays auditable but never surfaces by default
    result = retrieve([old, new])
    assert [r.record_id for r, _ in result.items] == [new.record_id]


def test_supersede_refuses_self_and_non_active_pair():
    record = _rec()
    try:
        supersede(record, record)
    except MemoryMetabolismError as exc:
        assert str(exc) == "supersede_self_refused"
    else:
        raise AssertionError("expected self-supersede refusal")
    other = _rec(content="other")
    archive(other, now=NOW)
    try:
        supersede(record, other)
    except MemoryMetabolismError as exc:
        assert str(exc) == "supersede_requires_active_pair"
    else:
        raise AssertionError("expected non-active-pair refusal")


def test_reconcile_winner_loser_with_mandatory_rationale():
    a = _rec(content="claim A")
    b = _rec(content="claim B")
    receipt = reconcile(a, b, "a_wins", rationale="Trial-4 falsified B", now=NOW)
    assert b.memory_state == SUPERSEDED and b.superseded_by == a.record_id
    assert a.memory_state == ACTIVE
    assert receipt["rationale"] == "Trial-4 falsified B"
    assert "winner=" in receipt["detail"]
    # audit retrieval surfaces the loser, explicitly labeled
    result = retrieve([a, b], include_audit_states=(SUPERSEDED,))
    labels = {r.record_id: label for r, label in result.items}
    assert labels[b.record_id] == "AUDIT:SUPERSEDED"
    assert labels[a.record_id] == ACTIVE


def test_reconcile_merged_and_refusals():
    a = _rec(content="claim A")
    b = _rec(content="claim B")
    merged = _rec(content="synthesis")
    receipt = reconcile(a, b, "merged", rationale="Both partial; synthesis verified", merged=merged, now=NOW)
    assert a.memory_state == SUPERSEDED and b.memory_state == SUPERSEDED
    assert set(merged.lineage) == {a.record_id, b.record_id}
    assert receipt["detail"].startswith("resolution=merged")
    for bad_call in (
        lambda: reconcile(_rec(), _rec(), "a_wins", rationale=""),
        lambda: reconcile(_rec(), _rec(), "sideways", rationale="x"),
        lambda: reconcile(_rec(), _rec(), "merged", rationale="x"),
    ):
        try:
            bad_call()
        except MemoryMetabolismError as exc:
            assert str(exc) in (
                "reconcile_rationale_missing",
                "reconcile_resolution_unknown",
                "reconcile_merged_record_missing",
            )
        else:
            raise AssertionError("expected reconcile refusal")


def test_decay_demotes_stale_and_noops_on_fresh():
    stale = _rec(now=STALE)
    fresh = _rec(now=FRESH)
    r1 = decay(stale, now=NOW, stale_after_days=90)
    assert stale.memory_state == DECAYED
    assert r1["to_state"] == DECAYED
    r2 = decay(fresh, now=NOW, stale_after_days=90)
    assert fresh.memory_state == ACTIVE and r2["to_state"] == ACTIVE
    # decayed never surfaces by default; decay refuses a bad policy
    assert retrieve([stale, fresh]).items[0][0].record_id == fresh.record_id
    try:
        decay(fresh, now=NOW, stale_after_days=0)
    except MemoryMetabolismError as exc:
        assert str(exc) == "decay_policy_invalid"
    else:
        raise AssertionError("expected decay policy refusal")


def test_compress_preserves_provenance_and_original_hash():
    record = _rec()
    receipt = compress(record, "Summary: retention wins", now=NOW)
    assert record.compressed is True
    assert record.content == "Summary: retention wins"
    assert record.original_content_hash.startswith("MOC-")
    assert record.memory_state == ACTIVE  # compression does not demote
    assert integrity_ok(record)
    assert "original_hash=" in receipt["detail"]
    archived = _rec()
    archive(archived, now=NOW)
    try:
        compress(archived, "x")
    except MemoryMetabolismError as exc:
        assert str(exc) == "compress_refused_immutable_history"
    else:
        raise AssertionError("expected compress refusal on archived history")
    try:
        compress(record, "again")
    except MemoryMetabolismError as exc:
        assert str(exc) == "compress_already_compressed"
    else:
        raise AssertionError("expected double-compress refusal")


def test_archive_moves_to_audit_only_and_refuses_dead():
    record = _rec()
    receipt = archive(record, now=NOW)
    assert record.memory_state == ARCHIVED and integrity_ok(record)
    assert receipt["to_state"] == ARCHIVED
    assert retrieve([record]).items == []
    quarantined = _rec()
    quarantine(quarantined, "hash mismatch", now=NOW)
    try:
        archive(quarantined, now=NOW)
    except MemoryMetabolismError as exc:
        # quarantine keeps the broken hash as evidence, so the integrity
        # gate fires first: fail closed, doubly refused.
        assert str(exc) == "memory_integrity_failed"
    else:
        raise AssertionError("expected archive refusal on quarantined")
    retired = _rec()
    supersede(retired, _rec(content="newer", now=FRESH), now=NOW)
    try:
        archive(retired, now=NOW)
    except MemoryMetabolismError as exc:
        assert str(exc) == "archive_requires_live_record"
    else:
        raise AssertionError("expected archive refusal on superseded")


def test_quarantine_isolates_and_is_never_served():
    record = _rec()
    receipt = quarantine(record, "tamper evidence", now=NOW)
    assert record.memory_state == QUARANTINED
    assert receipt["detail"] == "tamper evidence"
    result = retrieve([record])
    assert result.items == []
    try:
        retrieve([record], include_audit_states=(QUARANTINED,))
    except MemoryMetabolismError as exc:
        assert str(exc) == "quarantine_never_served"
    else:
        raise AssertionError("expected quarantine-never-served refusal")
    # corruption at read is dropped, not served
    corrupted = _rec()
    corrupted.content = "tampered"
    result = retrieve([corrupted])
    assert result.items == [] and result.dropped_integrity_failed == [corrupted.record_id]


def test_transitions_fail_closed_on_tampering():
    record = _rec()
    record.content = "tampered"
    for fn in (
        lambda: strengthen(record, "e"),
        lambda: supersede(record, _rec()),
        lambda: decay(record, now=NOW, stale_after_days=90),
        lambda: compress(record, "s"),
        lambda: archive(record),
    ):
        try:
            fn()
        except MemoryMetabolismError as exc:
            assert str(exc) == "memory_integrity_failed"
        else:
            raise AssertionError("expected fail-closed integrity refusal")


def test_retrieve_tracks_retrieval_and_honors_predicate():
    a = _rec(content="alpha")
    b = _rec(content="beta")
    result = retrieve([a, b], predicate=lambda r: "alpha" in r.content)
    assert [r.record_id for r, _ in result.items] == [a.record_id]
    assert a.retrieval_count == 1 and b.retrieval_count == 0
    assert integrity_ok(a)  # retrieval bookkeeping keeps integrity consistent


def test_metabolize_is_deterministic_and_refuses_corruption():
    stale = _rec(content="old", now=STALE)
    fresh = _rec(content="new", now=FRESH)
    _, receipts1 = metabolize([stale, fresh], now=NOW, stale_after_days=90)
    stale2 = _rec(content="old", now=STALE)
    fresh2 = _rec(content="new", now=FRESH)
    _, receipts2 = metabolize([stale2, fresh2], now=NOW, stale_after_days=90)
    assert [r["receipt_id"] for r in receipts1] == [r["receipt_id"] for r in receipts2]
    assert [r["to_state"] for r in receipts1] == [DECAYED, ACTIVE]
    corrupted = _rec()
    corrupted.content = "tampered"
    try:
        metabolize([corrupted], now=NOW)
    except MemoryMetabolismError as exc:
        assert str(exc) == "memory_integrity_failed"
    else:
        raise AssertionError("expected metabolize to refuse corruption")


def test_full_lifecycle_paths_without_stale_winning():
    # Path A: replacement — strengthen keeps it alive, supersede retires it.
    record = _rec(content="hypothesis H", epistemic_state="HYPOTHESIS", now=STALE)
    strengthen(record, "trial-4-positive", now=NOW)
    assert record.memory_state == ACTIVE  # fresh verification keeps it alive
    successor = _rec(content="verified fact F", epistemic_state="VERIFIED_FACT", now=NOW)
    supersede(record, successor, now=NOW)
    result = retrieve([record, successor])
    assert [r.record_id for r, _ in result.items] == [successor.record_id]
    # Path B: demotion — decay -> compress -> archive; never resurfaces.
    aging = _rec(content="old assumption", epistemic_state="OPERATING_ASSUMPTION", now=STALE)
    _, receipts = metabolize([aging], now=NOW, stale_after_days=90)
    assert receipts[0]["to_state"] == DECAYED
    compress(aging, "Summary: assumption superseded by trial evidence", now=NOW)
    archive(aging, now=NOW)
    assert aging.memory_state == ARCHIVED
    assert retrieve([aging]).items == []
    # epistemic type survived the lifecycle untouched on every record
    assert record.epistemic_state == "HYPOTHESIS"
    assert successor.epistemic_state == "VERIFIED_FACT"
    assert aging.epistemic_state == "OPERATING_ASSUMPTION"


def test_metabolize_skips_quarantined_placeholders_without_refusing():
    """Quarantine is a settled decision: housekeep must not die on its evidence.

    Regression guard for the cold-boot drill finding (2026-10-08): a store
    that quarantined corrupt lines could never run housekeep again, because
    the placeholder's deliberate non-verifying integrity marker tripped the
    strict pre-check. Resolved corruption is skipped with a noop receipt;
    live corruption is still refused.
    """
    from kernel.memory_metabolism import quarantine

    # NOTE: distinct record_ids — _rec() derives the id from (content, now),
    # so two default _rec()s collide and a receipt dict keyed by record_id
    # would silently drop one.
    settled = _rec(record_id="QR-SETTLED")
    quarantine(settled, "corrupt_line=5 reason=json_decode_failed", now=NOW)
    settled.integrity = "QUARANTINED-NO-HASH"  # as the store's placeholder does
    live = _rec(record_id="QR-LIVE", now=FRESH)

    records, receipts = metabolize([settled, live], now=NOW, stale_after_days=90)

    by_id = {r["record_id"]: r for r in receipts}
    assert by_id[settled.record_id]["detail"] == "quarantined_noop"
    assert by_id[settled.record_id]["to_state"] == QUARANTINED
    assert settled.memory_state == QUARANTINED  # untouched, still unservable
    assert retrieve([settled]).items == []


def test_metabolize_still_refuses_live_corruption():
    """The quarantine exemption never extends to servable records."""
    corrupted = _rec()
    corrupted.content = "tampered"
    try:
        metabolize([corrupted], now=NOW)
    except MemoryMetabolismError as exc:
        assert str(exc) == "memory_integrity_failed"
    else:
        raise AssertionError("expected metabolize to refuse corruption")
