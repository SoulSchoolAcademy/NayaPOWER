"""Tests for kernel/memory_store.py — the durable wiring of memory metabolism.

Covers: save/load round-trip, append-only latest-wins, corruption quarantine,
tamper isolation, receipt hash-chaining, fail-closed serve, deterministic
housekeep, cold-boot reconstruction from zero warm state, and the CLI.
"""

import hashlib
import json
from pathlib import Path

import pytest

from kernel import memory_metabolism as mm
from kernel.memory_store import (
    GENESIS_CHAIN,
    MemoryStore,
    MemoryStoreError,
    _chain_step,
    main,
    verify_receipt_chain,
)

NOW = "2026-10-08T15:45:00+00:00"
OLD = "2026-01-01T00:00:00+00:00"


def _rec(content="lesson one", epistemic="LEARNING", at=NOW):
    return mm.create_record(content, epistemic_state=epistemic,
                            provenance={"test": True}, now=at)


def _ev(eid, content, origin="trial-store", verifier="coda-1"):
    return mm.EvidenceDescriptor(
        evidence_id=eid,
        content=content,
        content_hash=hashlib.sha256(content.encode()).hexdigest(),
        origin=origin,
        verifier=verifier,
    )


def _store(tmp_path: Path) -> MemoryStore:
    return MemoryStore(tmp_path / "memstore")


# Save / load -------------------------------------------------------------------

def test_save_load_round_trip(tmp_path):
    store = _store(tmp_path)
    a, b = _rec("alpha"), _rec("beta", epistemic="VERIFIED_FACT")
    store.save(a)
    store.save(b)
    fresh = MemoryStore(store.directory)
    records = fresh.load(now=NOW)
    assert set(records) == {a.record_id, b.record_id}
    assert records[a.record_id].content == "alpha"
    assert all(mm.integrity_ok(r) for r in records.values())


def test_load_missing_directory_is_empty_boot(tmp_path):
    store = MemoryStore(tmp_path / "does-not-exist")
    assert store.load(now=NOW) == {}
    assert store.health()["records"] == 0


def test_latest_version_wins_append_only(tmp_path):
    store = _store(tmp_path)
    r = _rec()
    store.save(r)
    mm.strengthen(r, _ev("EV-1", "store evidence 1"), now=NOW)
    store.save(r)
    assert store.records_path.read_text().count("\n") == 2  # both versions kept
    fresh = MemoryStore(store.directory)
    loaded = fresh.load(now=NOW)
    assert loaded[r.record_id].verification_weight == 1.0
    entry = loaded[r.record_id].evidence[0]
    assert entry["evidence_id"] == "EV-1"
    assert entry["origin"] == "trial-store"
    assert entry["verifier"] == "coda-1"
    assert entry["content_hash"] == hashlib.sha256(
        "store evidence 1".encode()).hexdigest()


def test_save_refuses_broken_integrity(tmp_path):
    store = _store(tmp_path)
    r = _rec()
    r.content = "tampered before save"
    with pytest.raises(MemoryStoreError):
        store.save(r)


# Corruption quarantine -----------------------------------------------------------

def test_corrupt_line_quarantined_never_served(tmp_path):
    store = _store(tmp_path)
    good = _rec("good record")
    store.save(good)
    with store.records_path.open("a", encoding="utf-8") as fh:
        fh.write("{this is not json\n")
    fresh = MemoryStore(store.directory)
    records = fresh.load(now=NOW)
    assert good.record_id in records
    quarantined = [r for r in records.values()
                   if r.memory_state == mm.QUARANTINED]
    assert len(quarantined) == 1
    assert quarantined[0].record_id.startswith("CORRUPT-L2-")
    # Never served, even when audit states are requested
    result = fresh.serve(include_audit_states=(mm.SUPERSEDED, mm.DECAYED,
                                               mm.ARCHIVED))
    served_ids = [r.record_id for r, _ in result.items]
    assert quarantined[0].record_id not in served_ids
    assert good.record_id in served_ids
    assert fresh.health()["corrupt_lines"] == 1


def test_quarantine_receipt_idempotent_across_loads(tmp_path):
    store = _store(tmp_path)
    store.save(_rec("good"))
    with store.records_path.open("a", encoding="utf-8") as fh:
        fh.write("garbage\n")
    first = MemoryStore(store.directory)
    first.load(now=NOW)
    n_receipts = len(first._receipts)
    assert n_receipts == 2  # 1 save + 1 quarantine
    assert len([e for e in first._receipts
                if e["transition"] == "quarantine"]) == 1
    second = MemoryStore(store.directory)
    second.load(now=NOW)
    assert len(second._receipts) == n_receipts  # no duplicate quarantine receipt


def test_tampered_version_does_not_destroy_last_good(tmp_path):
    store = _store(tmp_path)
    r = _rec("original truth")
    store.save(r)
    mm.strengthen(r, _ev("EV-1", "store evidence 1"), now=NOW)
    store.save(r)
    # Tamper the *latest* version's line in the log (simulates disk tampering).
    lines = store.records_path.read_text(encoding="utf-8").splitlines()
    payload = json.loads(lines[-1])
    payload["content"] = "forged content"
    lines[-1] = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    store.records_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    fresh = MemoryStore(store.directory)
    records = fresh.load(now=NOW)
    # Last-good version survives; the forged version is quarantined. The
    # strengthened fields die with the tampered version — no field of a
    # tampered version is trusted, so the survivor is the last fully
    # verified version (weight 0.0), not the strengthened one (weight 1.0).
    assert records[r.record_id].content == "original truth"
    assert records[r.record_id].verification_weight == 0.0
    assert records[r.record_id].evidence == []
    assert any(v.memory_state == mm.QUARANTINED for v in records.values())
    result = fresh.serve()
    assert [rec.record_id for rec, _ in result.items] == [r.record_id]


def test_integrity_verified_at_read_not_just_load(tmp_path):
    store = _store(tmp_path)
    r = _rec("reads must verify")
    store.save(r)
    # Corrupt the in-memory record after a clean load (bypasses load checks).
    r.content = "mutated in memory"
    result = store.serve()
    assert result.items == []
    assert result.dropped_integrity_failed == [r.record_id]


# Serve discipline -----------------------------------------------------------------

def test_serve_active_only_by_default(tmp_path):
    store = _store(tmp_path)
    active = _rec("active")
    old = _rec("old", at=OLD)
    store.save(active)
    store.save(old)
    mm.supersede(old, active, now=NOW)
    store.save(old)
    store.save(active)
    result = store.serve(now=NOW)
    served = {r.record_id: label for r, label in result.items}
    assert served == {active.record_id: mm.ACTIVE}


def test_serve_audit_states_labeled(tmp_path):
    store = _store(tmp_path)
    a, b = _rec("a", at=OLD), _rec("b")
    store.save(a)
    store.save(b)
    mm.supersede(a, b, now=NOW)
    store.save(a)
    result = store.serve(include_audit_states=(mm.SUPERSEDED,), now=NOW)
    labels = {r.record_id: label for r, label in result.items}
    assert labels[a.record_id] == f"AUDIT:{mm.SUPERSEDED}"
    assert labels[b.record_id] == mm.ACTIVE


def test_quarantine_never_served_even_when_requested(tmp_path):
    store = _store(tmp_path)
    store.save(_rec("x"))
    with pytest.raises(MemoryStoreError):
        store.serve(include_audit_states=(mm.QUARANTINED,))


# Housekeep -------------------------------------------------------------------------

def test_housekeep_decays_stale_persists_and_receipts(tmp_path):
    store = _store(tmp_path)
    stale = _rec("stale", at=OLD)
    fresh = _rec("fresh")
    store.save(stale)
    store.save(fresh)
    receipts = store.housekeep(now=NOW, stale_after_days=90.0)
    assert len(receipts) == 2
    changed = [r for r in receipts if r["to_state"] == mm.DECAYED]
    assert len(changed) == 1 and changed[0]["record_id"] == stale.record_id
    # Change persisted: a fresh load sees the decayed state.
    reloaded = MemoryStore(store.directory).load(now=NOW)
    assert reloaded[stale.record_id].memory_state == mm.DECAYED
    assert reloaded[fresh.record_id].memory_state == mm.ACTIVE
    # Receipts are hash-chained and verifiable.
    assert verify_receipt_chain(store._receipts) == []


def test_housekeep_refuses_instant_decay_policy(tmp_path):
    store = _store(tmp_path)
    store.save(_rec("x"))
    # The refusal surfaces as the machinery's error: the store is thin wiring,
    # it does not translate the metabolism's own policy gate.
    with pytest.raises(mm.MemoryMetabolismError) as exc:
        store.housekeep(now=NOW, stale_after_days=0)
    assert str(exc.value) == "decay_policy_invalid"


def test_housekeep_deterministic(tmp_path):
    def run(directory):
        s = MemoryStore(directory)
        r = _rec("deterministic", at=OLD)
        s.save(r)
        receipts = s.housekeep(now=NOW, stale_after_days=30.0)
        return receipts[0]["receipt_id"], receipts[0]["chain"]
    a = run(tmp_path / "a")
    b = run(tmp_path / "b")
    assert a == b


# Receipt chain -----------------------------------------------------------------------

def test_receipt_chain_genesis_and_tamper_detection(tmp_path):
    store = _store(tmp_path)
    r = _rec("chain me", at=OLD)
    store.save(r)
    store.housekeep(now=NOW, stale_after_days=30.0)
    entries = store._receipts
    assert entries[0]["prev_chain"] == GENESIS_CHAIN
    assert verify_receipt_chain(entries) == []
    # Tamper with a logged receipt: chain breaks at that seq.
    tampered = [dict(e) for e in entries]
    tampered[0]["detail"] = "forged detail"
    assert verify_receipt_chain(tampered) == [tampered[0]["log_seq"]]


def test_chain_step_is_deterministic():
    receipt = {"a": 1}
    assert _chain_step("prev", receipt) == _chain_step("prev", receipt)
    assert _chain_step("prev", receipt) != _chain_step("other", receipt)


def test_save_is_receipted_chain_covers_record_history(tmp_path):
    # Hard law: all persisted mutations are receipted. save() must leave a
    # "save" receipt so the chain reconstructs the record's whole history.
    store = _store(tmp_path)
    r = _rec("receipted save", at=OLD)
    store.save(r, now=NOW)
    mm.strengthen(r, _ev("EV-1", "store evidence 1"), now=NOW)
    store.save(r, now=NOW)
    saves = [e for e in store._receipts if e["transition"] == "save"]
    assert len(saves) == 2
    assert all(e["record_id"] == r.record_id for e in saves)
    assert verify_receipt_chain(store._receipts) == []
    # Cold load: receipts survive the process boundary intact.
    rebuilt = MemoryStore(store.directory)
    rebuilt.load(now=NOW)
    assert len([e for e in rebuilt._receipts
                if e["transition"] == "save"]) == 2
    assert verify_receipt_chain(rebuilt._receipts) == []


def test_serve_touch_persist_is_receipted(tmp_path):
    store = _store(tmp_path)
    r = _rec("touched", at=OLD)
    store.save(r, now=NOW)
    before = len(store._receipts)
    result = store.serve(now=NOW)
    assert len(result.items) == 1
    saves = [e for e in store._receipts[before:]
             if e["transition"] == "save"]
    assert len(saves) == 1
    assert saves[0]["record_id"] == r.record_id
    assert verify_receipt_chain(store._receipts) == []


def test_corrupt_receipt_line_counted_chain_misses_it(tmp_path):
    # A garbage receipt line never participated in the hash chain, so every
    # prev_chain link still verifies. health() must still surface the damage.
    store = _store(tmp_path)
    r = _rec("receipt damage", at=OLD)
    store.save(r)
    store.housekeep(now=NOW, stale_after_days=30.0)
    assert len(store._receipts) >= 1
    lines = store.receipts_path.read_text(encoding="utf-8").splitlines()
    lines.insert(1, "{not valid json")
    store.receipts_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    rebuilt = MemoryStore(store.directory)
    rebuilt.load(now=NOW)
    health = rebuilt.health()
    assert health["corrupt_receipt_lines"] == 1
    assert health["receipt_chain_broken"] == []
    # Counter resets on every load: no double counting.
    rebuilt.load(now=NOW)
    assert rebuilt.health()["corrupt_receipt_lines"] == 1


# Cold-boot reconstruction ---------------------------------------------------------------

def test_full_lifecycle_cold_boot_reconstruction(tmp_path):
    store = _store(tmp_path)
    a = _rec("lesson v1", at=OLD)
    b = _rec("lesson v2")
    store.save(a)
    store.save(b)
    mm.strengthen(b, _ev("EV-1", "trial evidence"), now=NOW)
    store.save(b)
    mm.supersede(a, b, now=NOW)
    store.save(a)
    store.save(b)
    c = _rec("ancient note", at="2025-01-01T00:00:00+00:00")
    store.save(c)
    store.housekeep(now=NOW, stale_after_days=90.0)
    served_before = {r.record_id for r, _ in store.serve(now=NOW).items}
    # Drop ALL in-memory state: reconstruct from disk only.
    del store
    rebuilt = MemoryStore(tmp_path / "memstore")
    records = rebuilt.load(now=NOW)
    assert records[a.record_id].memory_state == mm.SUPERSEDED
    assert records[a.record_id].superseded_by == b.record_id
    assert records[b.record_id].memory_state == mm.ACTIVE
    assert records[b.record_id].verification_weight == 1.0
    assert records[c.record_id].memory_state == mm.DECAYED
    served_after = {r.record_id for r, _ in rebuilt.serve(now=NOW).items}
    assert served_after == served_before == {b.record_id}
    assert verify_receipt_chain(rebuilt._receipts) == []
    health = rebuilt.health()
    assert health["receipt_chain_broken"] == []
    assert health["corrupt_lines"] == 0
    assert health["by_state"][mm.ACTIVE] == 1


# CLI ---------------------------------------------------------------------------------------

def test_cli_housekeep_serve_verify(tmp_path, capsys):
    directory = tmp_path / "cli"
    r = _rec("cli record", at=OLD)
    s = MemoryStore(directory)
    s.save(r)
    assert main(["--store", str(directory), "housekeep",
                 "--now", NOW, "--stale-days", "30"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["state_changes"] == 1
    assert main(["--store", str(directory), "serve", "--now", NOW]) == 0
    served = json.loads(capsys.readouterr().out)
    assert served["served"] == []  # decayed out of the active set
    assert main(["--store", str(directory), "verify"]) == 0
    health = json.loads(capsys.readouterr().out)
    assert health["by_state"] == {mm.DECAYED: 1}


def test_cli_verify_returns_2_on_broken_chain(tmp_path, capsys):
    directory = tmp_path / "broken"
    s = MemoryStore(directory)
    r = _rec("x", at=OLD)
    s.save(r)
    s.housekeep(now=NOW, stale_after_days=30.0)
    lines = s.receipts_path.read_text(encoding="utf-8").splitlines()
    entry = json.loads(lines[0])
    entry["detail"] = "forged"
    lines[0] = json.dumps(entry, sort_keys=True, separators=(",", ":"))
    s.receipts_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    assert main(["--store", str(directory), "verify"]) == 2
