"""DRILL: full-system cold-boot reconstruction across a real process boundary.

Memory & Continuity acceptance drill. The falsifiable claim under test:

    A machine can crash the brain mid-life, corrupt the record log, tamper a
    record version, and cold-boot back to a provably correct serving state —
    with the receipt chain intact, the corruption quarantined (never served),
    the tampered version quarantined (last-good state preserved), and stale
    intelligence decayed under receipt.

Every "cold" phase below runs in a FRESH `python -m kernel.memory_store`
subprocess with zero shared in-memory state with the seeding process. That
subprocess boundary is the whole point: `MemoryStore.load()` must rebuild
everything from the JSONL logs alone.

Adversary coverage (4 corrupt lines, each a distinct failure class):
    L5  json_decode_failed   — truncated / garbage line
    L6  not_an_object        — valid JSON, wrong shape
    L7  schema_mismatch      — full record + an unknown field
    L8  integrity_failed     — R1's version with altered content, stale hash

Expected cold-boot outcome:
    - 8 records: 3 ACTIVE, 1 SUPERSEDED, 4 QUARANTINED
    - exactly 4 quarantine receipts (one per corrupt line; re-loads add none)
    - receipt hash chain verifies end-to-end
    - housekeep decays the stale ACTIVE record under receipt
    - serve returns ACTIVE only; audit states labeled AUDIT:<STATE>
    - QUARANTINED is never served, even when explicitly requested
    - R1 serves its ORIGINAL content — the tampered version did not win
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]

SEED_NOW = "2026-01-01T00:00:00+00:00"
FRESH_NOW = "2026-10-01T21:55:00+00:00"  # 7 days before DRILL_NOW: not stale
STALE_AT = "2025-01-01T00:00:00+00:00"
DRILL_NOW = "2026-10-08T21:55:00+00:00"

R1_ID = "MEM-DRILL-R1"
R1_CONTENT = "The Receiver is the single canonical capture path."
R2_ID = "MEM-DRILL-R2"
R2_CONTENT = "Engines before interfaces; proof before promotion."
R3_OLD_ID = "MEM-DRILL-R3-OLD"
R3_NEW_ID = "MEM-DRILL-R3-NEW"
TAMPERED_CONTENT = "TAMPERED: the Receiver is optional."


def _cli(store_dir: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "kernel.memory_store", "--store", str(store_dir),
         *args],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=120,
    )


@pytest.fixture()
def crashed_store(tmp_path):
    """Seed a store, then corrupt/tamper its record log like a real crash."""
    from kernel import memory_metabolism as mm
    from kernel.memory_store import MemoryStore, _canonical, _record_to_dict

    store_dir = tmp_path / "drill-store"
    store = MemoryStore(store_dir)

    # R1 and R3-new are FRESH (verified days before the drill's housekeep);
    # R2 is backdated so housekeep must decay it. Freshness is what the
    # not_stale_noop vs real-decay paths turn on.
    r1 = mm.create_record(R1_CONTENT, epistemic_state="VERIFIED_FACT",
                          record_id=R1_ID, now=FRESH_NOW)
    r2 = mm.create_record(R2_CONTENT, epistemic_state="VERIFIED_FACT",
                          record_id=R2_ID, now=SEED_NOW)
    # Backdate R2's verification clock so the drill's housekeep must decay it.
    r2.created_at = STALE_AT
    r2.last_verified_at = STALE_AT
    r2.integrity = mm.record_integrity(r2)
    r3_old = mm.create_record("Superseded claim.", epistemic_state="EXTERNAL_CLAIM",
                              record_id=R3_OLD_ID, now=SEED_NOW)
    r3_new = mm.create_record("Corrected claim.", epistemic_state="VERIFIED_FACT",
                              record_id=R3_NEW_ID, now=FRESH_NOW)
    mm.supersede(r3_old, r3_new, now=SEED_NOW)

    for record in (r1, r2, r3_old, r3_new):
        store.save(record)
    r1_line = _canonical(_record_to_dict(r1))

    # --- the adversary: raw appends to the record log, post-seed ---
    records_path = store_dir / "records.jsonl"
    with records_path.open("a", encoding="utf-8") as fh:
        fh.write("{not valid json\n")                                   # L5
        fh.write("[1, 2, 3]\n")                                          # L6
        full = _record_to_dict(r3_new)
        full["unknown_field_xyz"] = 1
        fh.write(_canonical(full) + "\n")                                # L7
        tampered = json.loads(r1_line)
        tampered["content"] = TAMPERED_CONTENT
        fh.write(json.dumps(tampered, sort_keys=True,
                            separators=(",", ":")) + "\n")                # L8

    # The seeding process "dies" here: everything below is a fresh process.
    return store_dir


def _verify(store_dir: Path) -> dict:
    proc = _cli(store_dir, "verify")
    assert proc.returncode == 0, f"verify failed:\n{proc.stderr}"
    return json.loads(proc.stdout)


def test_cold_boot_quarantines_corruption_and_chain_verifies(crashed_store):
    """Cold boot: 4 corrupt lines quarantined; receipt chain intact."""
    health = _verify(crashed_store)

    assert health["corrupt_lines"] == 4
    assert health["receipt_chain_broken"] == []
    assert health["records"] == 8
    assert health["by_state"] == {"ACTIVE": 3, "SUPERSEDED": 1, "QUARANTINED": 4}

    reasons = {c["reason"] for c in health["corruption"]}
    assert reasons == {"json_decode_failed", "not_an_object",
                       "schema_mismatch", "integrity_failed"}
    lines = {c["line"] for c in health["corruption"]}
    assert lines == {5, 6, 7, 8}

    # Exactly one quarantine receipt per corrupt line in the durable log.
    receipts = [json.loads(line) for line in
                (crashed_store / "receipts.jsonl").read_text(
                    encoding="utf-8").splitlines() if line.strip()]
    quarantines = [r for r in receipts if r.get("transition") == "quarantine"]
    assert len(quarantines) == 4
    assert len({r["raw_sha256"] for r in quarantines}) == 4


def test_quarantine_is_idempotent_across_reloads(crashed_store):
    """Re-loading the same corrupt log must not mint new quarantine receipts."""
    first = _verify(crashed_store)["receipts"]
    second = _verify(crashed_store)["receipts"]
    assert first == second == 4


def test_housekeep_decays_stale_under_receipt(crashed_store):
    """The stale ACTIVE record decays; history records are receipted as noops."""
    _verify(crashed_store)  # cold boot first, so quarantines exist
    proc = _cli(crashed_store, "housekeep", "--now", DRILL_NOW,
                "--stale-days", "90")
    assert proc.returncode == 0, f"housekeep failed:\n{proc.stderr}"
    out = json.loads(proc.stdout)

    assert out["receipts"] == 8          # one per record in the mixed store
    assert out["state_changes"] == 6     # R2 decay + 5 non-ACTIVE noop receipts
    assert out["health"]["by_state"]["DECAYED"] == 1

    # The decay receipt names the policy that fired.
    receipts = [json.loads(line) for line in
                (crashed_store / "receipts.jsonl").read_text(
                    encoding="utf-8").splitlines() if line.strip()]
    decays = [r for r in receipts if r.get("transition") == "decay"
              and r.get("record_id") == R2_ID]
    assert len(decays) == 1
    assert decays[0]["to_state"] == "DECAYED"
    assert "stale_beyond_90.0d" in decays[0]["detail"]


def test_serve_fail_closed_and_audit_labeled(crashed_store):
    """serve(): ACTIVE only; audit states labeled; tampered version never wins."""
    _cli(crashed_store, "housekeep", "--now", DRILL_NOW, "--stale-days", "90")

    proc = _cli(crashed_store, "serve")
    assert proc.returncode == 0, f"serve failed:\n{proc.stderr}"
    out = json.loads(proc.stdout)
    served = {item["record_id"]: item for item in out["served"]}
    assert out["dropped_integrity_failed"] == []

    # R1 + R3-new serve. R2 decayed out. R3-old is history. Quarantine absent.
    assert set(served) == {R1_ID, R3_NEW_ID}
    assert all(item["label"] == "ACTIVE" for item in served.values())
    assert not any(rid.startswith("CORRUPT-") for rid in served)

    # Last-good state survived the tampered version: original content served.
    assert served[R1_ID]["memory_state"] == "ACTIVE"
    # (content proven at the store level below)

    # Audit states are available but always labeled as history.
    proc = _cli(crashed_store, "serve", "--include-audit", "SUPERSEDED,DECAYED")
    assert proc.returncode == 0, f"audit serve failed:\n{proc.stderr}"
    audit = {item["record_id"]: item["label"]
             for item in json.loads(proc.stdout)["served"]}
    assert audit[R3_OLD_ID] == "AUDIT:SUPERSEDED"
    assert audit[R2_ID] == "AUDIT:DECAYED"

    # QUARANTINED is never served — requesting it is a hard refusal.
    proc = _cli(crashed_store, "serve", "--include-audit", "QUARANTINED")
    assert proc.returncode != 0
    assert "quarantine_never_served" in proc.stderr


def test_tampered_version_did_not_destroy_last_good(crashed_store):
    """The integrity-failed version of R1 is quarantined; R1 keeps its truth."""
    from kernel.memory_store import MemoryStore

    _verify(crashed_store)
    store = MemoryStore(crashed_store)
    store.load()

    r1 = store._records[R1_ID]
    assert r1.content == R1_CONTENT
    assert r1.memory_state == "ACTIVE"

    tampered = [rid for rid in store._records
                if rid.startswith("CORRUPT-L8-")]
    assert len(tampered) == 1
    assert store._records[tampered[0]].memory_state == "QUARANTINED"


def test_full_drill_chain_clean_after_everything(crashed_store):
    """After the whole drill, the receipt chain still verifies end-to-end."""
    _cli(crashed_store, "housekeep", "--now", DRILL_NOW, "--stale-days", "90")
    _cli(crashed_store, "serve")
    health = _verify(crashed_store)
    assert health["receipt_chain_broken"] == []
    # 4 quarantine + 8 housekeep receipts, all chained from MMC-GENESIS.
    assert health["receipts"] == 12
