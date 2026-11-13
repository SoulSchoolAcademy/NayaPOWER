"""Tests for tools/repair_smart_note_registry.py (drift cure, w3221/w3222).

The cure re-anchors stale/missing entry content_hashes to the current
capture for the same note (matched by NORMALIZED SN), and reports
everything it cannot repair deterministically instead of guessing.
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import smart_note_v2 as snv  # noqa: E402
import repair_smart_note_registry as rep  # noqa: E402

PAGE = "BRAIN/05-MEMORY/SMART-NOTES/2026/01/01/CAT/TOPIC/SUB/SN-001/IB-1.md"


def _hash(intelligence):
    return snv._canonical_content_hash(
        json.dumps(intelligence, sort_keys=True, separators=(",", ":"),
                   ensure_ascii=False)
    )


def build_root(tmp_path, sn="SN-001", intelligence=None, entry_hash="SET",
               capture_sn=None):
    """A minimal fully-reconciled tree, validator-passing (schema +
    page_hash + manifest), exactly like the drift test's clean fixture
    plus the B-51 fields the validator requires."""
    intelligence = intelligence if intelligence is not None else {"essence": "a", "distilled_intelligence": "b"}
    cap_dir = tmp_path / ".naya" / "capture"
    cap_dir.mkdir(parents=True)
    (cap_dir / "c1.json").write_text(
        json.dumps({"smart_note_id": capture_sn if capture_sn is not None else sn,
                    "intelligence": intelligence}), encoding="utf-8")
    page = tmp_path / PAGE
    page.parent.mkdir(parents=True)
    page.write_text("# IB-1\n", encoding="utf-8")
    entry = {
        "smart_note_id": sn,
        "intelligent_block_id": "IB-1",
        "content_hash": _hash(intelligence) if entry_hash == "SET" else entry_hash,
        "projection_path": PAGE,
        "projection_status": "GITHUB_BRAIN_PUBLISHED",
        "page_hash": snv._page_file_hash(page),
    }
    entries = [entry]
    reg_path = tmp_path / ".naya" / "memory" / "smart-notes" / "index.json"
    reg_path.parent.mkdir(parents=True)
    registry = {"schema": snv.INDEX_SCHEMA, "entries": entries}
    registry["corpus_manifest_hash"] = snv._corpus_manifest_hash(entries)
    reg_path.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    return reg_path


def read_entries(reg_path):
    return json.loads(reg_path.read_text(encoding="utf-8"))["entries"]


def _rewrite_capture(tmp_path, intelligence, filename="c1.json"):
    (tmp_path / ".naya" / "capture" / filename).write_text(
        json.dumps({"smart_note_id": "SN-001", "intelligence": intelligence}),
        encoding="utf-8")


def test_stale_entry_repaired_and_audit_clean(tmp_path):
    reg_path = build_root(tmp_path)
    assert snv.audit_registry(root=tmp_path)["ok"] is True
    _rewrite_capture(tmp_path, {"essence": "a2", "distilled_intelligence": "b2"})
    before = snv.audit_registry(root=tmp_path)
    assert before["counts"]["entries_with_stale_hash"] == 1
    assert before["counts"]["captures_unregistered_by_hash"] == 1

    plan = rep.plan_repair(tmp_path)
    assert len(plan["updates"]) == 1
    assert plan["updates"][0]["smart_note_id"] == "SN-001"
    receipt = rep.apply_repair(tmp_path, plan, write=True)
    assert receipt["validator"] == "PASS"
    assert receipt["after_defect_total"] == 0
    assert snv.audit_registry(root=tmp_path)["ok"] is True


def test_hashless_entry_filled(tmp_path):
    reg_path = build_root(tmp_path, entry_hash=None)
    plan = rep.plan_repair(tmp_path)
    assert len(plan["updates"]) == 1
    assert plan["updates"][0]["old_hash"] is None
    rep.apply_repair(tmp_path, plan, write=True)
    assert read_entries(reg_path)[0]["content_hash"] == _hash(
        {"essence": "a", "distilled_intelligence": "b"})


def test_unpadded_capture_sn_pairs_by_normalization(tmp_path):
    # Registry spells SN-0633; capture spells SN-633. Exact-SN pairing
    # misses; normalized pairing repairs. (Live-tip cause: 234/238.)
    reg_path = build_root(tmp_path, sn="SN-0633", capture_sn="SN-633",
                          entry_hash="0" * 64)
    plan = rep.plan_repair(tmp_path)
    assert len(plan["updates"]) == 1
    assert plan["updates"][0]["smart_note_id"] == "SN-0633"
    receipt = rep.apply_repair(tmp_path, plan, write=True)
    assert receipt["after_defect_total"] == 0


def test_dry_run_writes_nothing(tmp_path):
    reg_path = build_root(tmp_path, entry_hash="0" * 64)
    before_bytes = reg_path.read_bytes()
    plan = rep.plan_repair(tmp_path)
    receipt = rep.apply_repair(tmp_path, plan, write=False)
    assert receipt["written"] is False
    assert receipt["updates_planned"] == 1
    assert reg_path.read_bytes() == before_bytes


def test_latest_ib_date_wins_over_migration_stub(tmp_path):
    # Two IB captures, Oct-13 migration stub + Oct-19 real capture:
    # the latest embedded date is authoritative.
    reg_path = build_root(tmp_path, entry_hash="0" * 64)
    cap_dir = tmp_path / ".naya" / "capture"
    (cap_dir / "c1.json").unlink()
    old = {"essence": "old", "distilled_intelligence": "stub"}
    new = {"essence": "new", "distilled_intelligence": "real"}
    (cap_dir / "IB-SMART-NOTE-20261013-sn0001-migrated.json").write_text(
        json.dumps({"smart_note_id": "SN-001", "intelligence": old}))
    (cap_dir / "IB-SMART-NOTE-20261019-sn0001-how-to.json").write_text(
        json.dumps({"smart_note_id": "SN-001", "intelligence": new}))
    plan = rep.plan_repair(tmp_path)
    assert len(plan["updates"]) == 1
    assert plan["updates"][0]["capture"] == "IB-SMART-NOTE-20261019-sn0001-how-to.json"
    assert plan["updates"][0]["new_hash"] == _hash(new)


def test_same_date_tie_is_ambiguous_not_applied(tmp_path):
    reg_path = build_root(tmp_path, entry_hash="0" * 64)
    cap_dir = tmp_path / ".naya" / "capture"
    (cap_dir / "c1.json").unlink()
    for tag in ("aaa", "bbb"):
        (cap_dir / f"IB-SMART-NOTE-20261019-sn0001-{tag}.json").write_text(
            json.dumps({"smart_note_id": "SN-001",
                        "intelligence": {"essence": tag}}))
    plan = rep.plan_repair(tmp_path)
    assert plan["updates"] == []
    assert len(plan["ambiguous"]) == 1
    assert plan["ambiguous"][0]["reason"] == "ambiguous-capture"
    before_bytes = reg_path.read_bytes()
    rep.apply_repair(tmp_path, plan, write=True)
    assert reg_path.read_bytes() == before_bytes


def test_entry_without_capture_is_residual_not_deleted(tmp_path):
    reg_path = build_root(tmp_path, entry_hash="0" * 64)
    (tmp_path / ".naya" / "capture" / "c1.json").unlink()
    plan = rep.plan_repair(tmp_path)
    assert plan["updates"] == []
    assert plan["entries_without_capture"] == ["SN-001"]
    rep.apply_repair(tmp_path, plan, write=True)
    assert read_entries(reg_path)[0]["content_hash"] == "0" * 64


def test_manifest_reanchored_on_apply(tmp_path):
    reg_path = build_root(tmp_path, entry_hash="0" * 64)
    plan = rep.plan_repair(tmp_path)
    receipt = rep.apply_repair(tmp_path, plan, write=True)
    registry = json.loads(reg_path.read_text(encoding="utf-8"))
    assert registry["corpus_manifest_hash"] == snv._corpus_manifest_hash(
        registry["entries"])
    assert receipt["corpus_manifest_hash"] == registry["corpus_manifest_hash"]


def test_healthy_entry_never_touched(tmp_path):
    reg_path = build_root(tmp_path)
    before_bytes = reg_path.read_bytes()
    plan = rep.plan_repair(tmp_path)
    assert plan["updates"] == []
    rep.apply_repair(tmp_path, plan, write=True)
    assert reg_path.read_bytes() == before_bytes


def test_shared_capture_hash_is_ambiguous_not_applied(tmp_path):
    # REGRESSION (live tip 8e5baeff): 24 captures share one intelligence
    # hash. Copying that hash into 12 stale entries manufactured a
    # duplicate_smart_note_ids defect (a green class turned red). A hash
    # N captures share cannot identify a note — refuse all of them.
    reg_path = build_root(tmp_path, entry_hash="0" * 64)
    registry = json.loads(reg_path.read_text(encoding="utf-8"))
    page2 = tmp_path / PAGE.replace("SN-001", "SN-002").replace("IB-1.md", "IB-2.md")
    page2.parent.mkdir(parents=True)
    page2.write_text("# IB-2\n", encoding="utf-8")
    entry2 = {
        "smart_note_id": "SN-002",
        "intelligent_block_id": "IB-2",
        "content_hash": "1" * 64,
        "projection_path": str(page2.relative_to(tmp_path)).replace("\\", "/"),
        "projection_status": "GITHUB_BRAIN_PUBLISHED",
        "page_hash": snv._page_file_hash(page2),
    }
    registry["entries"].append(entry2)
    registry["corpus_manifest_hash"] = snv._corpus_manifest_hash(registry["entries"])
    reg_path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    cap_dir = tmp_path / ".naya" / "capture"
    # Second capture for SN-002 with intelligence IDENTICAL to SN-001's.
    (cap_dir / "c2.json").write_text(json.dumps({
        "smart_note_id": "SN-002",
        "intelligence": {"essence": "a", "distilled_intelligence": "b"}}))
    plan = rep.plan_repair(tmp_path)
    assert plan["updates"] == []
    assert {a["smart_note_id"] for a in plan["ambiguous"]} == {"SN-001", "SN-002"}
    assert all(a["reason"] == "shared-capture-hash" for a in plan["ambiguous"])
    before_bytes = reg_path.read_bytes()
    rep.apply_repair(tmp_path, plan, write=True)
    assert reg_path.read_bytes() == before_bytes


def test_preexisting_validator_failure_does_not_block(tmp_path):    # A pre-existing validator failure on an UNRELATED entry (ACTIVE
    # fixture with no projection_path) must not block the hash repair,
    # and must be reported honestly — not hidden behind a PASS.
    reg_path = build_root(tmp_path, entry_hash="0" * 64)
    registry = json.loads(reg_path.read_text(encoding="utf-8"))
    registry["entries"].append({
        "smart_note_id": "SN-9999",
        "intelligent_block_id": "IB-FIXTURE",
        "content_hash": "0" * 64,
        "projection_path": None,
        "projection_status": None,
        "page_hash": None,
        "lifecycle_state": "ACTIVE",
    })
    registry["corpus_manifest_hash"] = snv._corpus_manifest_hash(registry["entries"])
    reg_path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    with pytest.raises(SystemExit):
        snv._validate_index_against_corpus(registry, root=tmp_path)
    plan = rep.plan_repair(tmp_path)
    assert len(plan["updates"]) == 1
    receipt = rep.apply_repair(tmp_path, plan, write=True)
    assert receipt["updates_applied"] == 1
    assert receipt["preexisting_validator_failure"] is not None
    assert "ENTRY_MALFORMED" in receipt["preexisting_validator_failure"]
    assert receipt["validator"].startswith("PREEXISTING:")
    # The fixture entry itself stays stale (no capture exists for it) —
    # the repair fixed the one real stale entry and left the residual.
    assert receipt["after_defect_total"] == 1
