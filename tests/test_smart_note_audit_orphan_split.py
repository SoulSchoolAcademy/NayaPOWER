"""Orphan decomposition in the registry audit (LEARN convergence item a).

The orphan count conflates two defects: pages never registered, and pages
filed under an SN id the registry already gave to an earlier page. A cure
that "registers the orphans" by id collides on the second class. These tests
pin the split on a synthetic tree: one collision, two truly-unregistered
(one by field id, one by folder id), one page with no id anywhere — plus
the guard that the decomposition adds no defects of its own.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.smart_note_v2 import audit_registry

BASE = "BRAIN/05-MEMORY/SMART-NOTES/2026/11/15/SYSTEM"


def _entry(sn, ib, rel):
    return {
        "intelligent_block_id": ib,
        "smart_note_id": sn,
        "projection_path": rel,
        "projection_status": "GITHUB_BRAIN_PUBLISHED",
        "content_hash": "deadbeef",
    }


def _fixture(tmp_path):
    (tmp_path / ".naya" / "memory" / "smart-notes").mkdir(parents=True)
    (tmp_path / ".naya" / "capture").mkdir(parents=True)
    entries = [
        _entry("SN-0001", "IB-000001", f"{BASE}/SN-0001/page-one.md"),
        _entry("SN-0002", "IB-000002", f"{BASE}/SN-0002/page-two.md"),
    ]
    (tmp_path / ".naya" / "memory" / "smart-notes" / "index.json").write_text(
        json.dumps({"entries": entries}), encoding="utf-8"
    )
    pages = {
        f"{BASE}/SN-0001/page-one.md": "# Page One\n\nRegistered by projection path.\n",
        f"{BASE}/SN-0002/page-two.md": "# Page Two\n\nRegistered by projection path.\n",
        # Same SN id as the SN-0001 entry, different path: id collision.
        f"{BASE}/SN-0001/page-one-again.md": "# Page One Again\n\nsmart_note_id: SN-0001\n",
        # Fresh id, carried in the field: truly unregistered.
        f"{BASE}/SN-0003/page-three.md": "# Page Three\n\nsmart_note_id: SN-0003\n",
        # Fresh id, carried only by the folder: truly unregistered.
        f"{BASE}/SN-0004/page-four.md": "# Page Four\n\nNo field; the folder is the id.\n",
        # No SN id in field, folder, or filename: unidentified.
        f"{BASE}/misc/random-note.md": "# Random Note\n\nNo identifier anywhere.\n",
    }
    for rel, text in pages.items():
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    return tmp_path


def test_orphan_decomposition_splits_the_three_classes(tmp_path):
    report = audit_registry(root=_fixture(tmp_path))
    assert report["orphan_decomposition_counts"] == {
        "id_collision": 1,
        "truly_unregistered": 2,
        "no_id": 1,
    }


def test_collision_names_the_claimed_id_and_path(tmp_path):
    report = audit_registry(root=_fixture(tmp_path))
    collisions = report["orphan_decomposition"]["id_collision"]
    assert len(collisions) == 1
    assert collisions[0]["smart_note_id"] == "SN-0001"
    assert collisions[0]["path"].endswith("SN-0001/page-one-again.md")


def test_truly_unregistered_covers_field_and_folder_ids(tmp_path):
    report = audit_registry(root=_fixture(tmp_path))
    ids = {item["smart_note_id"] for item in report["orphan_decomposition"]["truly_unregistered"]}
    assert ids == {"SN-0003", "SN-0004"}


def test_no_id_item_carries_no_id(tmp_path):
    report = audit_registry(root=_fixture(tmp_path))
    no_id = report["orphan_decomposition"]["no_id"]
    assert len(no_id) == 1
    assert no_id[0]["smart_note_id"] is None
    assert no_id[0]["path"].endswith("misc/random-note.md")


def test_decomposition_adds_no_defects_and_keeps_receipt_shape(tmp_path):
    report = audit_registry(root=_fixture(tmp_path))
    assert report["counts"]["published_pages_without_registry_entry"] == 4
    assert report["defect_total"] == sum(report["counts"].values())
    for key in ("ok", "counts", "defect_total", "defects", "surfaces"):
        assert key in report
    # The three classes account for every orphan path exactly once.
    total_paths = sum(
        len(group["paths"])
        for group in report["defects"]["published_pages_without_registry_entry"]
    )
    assert total_paths == sum(report["orphan_decomposition_counts"].values()) == 4
