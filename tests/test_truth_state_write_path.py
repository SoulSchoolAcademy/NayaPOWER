"""Write-path truth-state hardening (safety, 2026-10-07).

Closes the three documented holes in the POISON immune battery (#1461):
  1. _update_registry_locked copied block["understanding_state"] verbatim and
     REPLACED the existing entry — a re-capture could escalate
     CANDIDATE -> RATIFIED, bypassing promote_note() and the truth-state
     guard entirely.
  2. Arbitrary state strings (e.g. ABSOLUTE_TRUTH) were accepted as truth_state.
  3. audit_registry (the CI ratchet) had no truth_state defect class, so
     fabricated authority was invisible.

The invariant now enforced, fail-closed:
  - A NEW note always enters as CANDIDATE: capture is not ratification.
  - A RE-CAPTURE updates content, never authority: existing truth_state and
    elevation_history are preserved verbatim. The write path can neither
    escalate nor demote.
  - Unknown state names collapse to CANDIDATE, never pass through.
  - The semantic audit is wired into audit_registry, so fabricated authority
    on disk fails the ratchet. Pre-machinery director ratifications are
    grandfathered named/dated/attributed, never extended.

Conventions: smart_note_v2 is loaded via importlib like the battery does;
tests run the real _update_registry_locked and the real audit_registry.
"""
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("smart_note_v2", ROOT / "tools" / "smart_note_v2.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

gspec = importlib.util.spec_from_file_location("truth_state_guard", ROOT / "tools" / "truth_state_guard.py")
g = importlib.util.module_from_spec(gspec)
gspec.loader.exec_module(g)

PAGE = "BRAIN/05-MEMORY/SMART-NOTES/2026/01/01/CAT/TOPIC/SUB/SN-001/IB-1.md"


def _hash(intelligence):
    return mod._canonical_content_hash(
        json.dumps(intelligence, sort_keys=True, separators=(",", ":"),
                   ensure_ascii=False)
    )


def _write_via_locked(tmp_path, monkeypatch, understanding_state, ib="IB-1", sn_id="SN-001"):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    reg_path = tmp_path / ".naya" / "memory" / "smart-notes" / "index.json"
    capture = {
        "title": "poison probe",
        "source": {"captured_at": "2026-10-05"},
        "category": "SMART_NOTE",
        "topic": "T",
        "subtopic": "S",
        "projection": {"publication_scope": "PRIVATE"},
    }
    block = {
        "intelligent_block_id": ib,
        "content": {"lesson": "probe lesson"},
        "understanding_state": understanding_state,
        "owner_scope": "PRIVATE",
    }
    verify = {"persisted": {
        "block": block,
        "event": {"id": "e1"}, "lineage": {"id": "l1"},
        "relationship": {"relationship_id": "r1"},
        "index": {"id": "i1"}, "checkpoint": {"id": "c1"},
        "receipt": {"id": "rc1"},
    }}
    projection = tmp_path / "probe.md"
    projection.write_text("# probe\n", encoding="utf-8")
    with mod.registry_transaction(registry_path=reg_path) as registry:
        mod._update_registry_locked(capture, verify, projection, registry, sn_id=sn_id)
    entries = json.loads(reg_path.read_text(encoding="utf-8"))["entries"]
    return next(e for e in entries if e["intelligent_block_id"] == ib)


def _clean_audit_root(tmp_path):
    """Battery-style fully-reconciled fixture: one capture, one entry, one page."""
    intelligence = {"essence": "a", "distilled_intelligence": "b"}
    cap_dir = tmp_path / ".naya" / "capture"
    cap_dir.mkdir(parents=True)
    (cap_dir / "c1.json").write_text(
        json.dumps({"smart_note_id": "SN-001", "intelligence": intelligence}),
        encoding="utf-8",
    )
    page = tmp_path / PAGE
    page.parent.mkdir(parents=True)
    page.write_text("# IB-1\n", encoding="utf-8")
    reg_path = tmp_path / ".naya" / "memory" / "smart-notes" / "index.json"
    reg_path.parent.mkdir(parents=True)
    reg_path.write_text(
        json.dumps({
            "schema": "naya.smart-note-projection-index.v1",
            "entries": [{
                "smart_note_id": "SN-001",
                "intelligent_block_id": "IB-1",
                "content_hash": _hash(intelligence),
                "projection_path": PAGE,
                "projection_status": "GITHUB_BRAIN_PUBLISHED",
            }],
        }),
        encoding="utf-8",
    )
    return reg_path


# --- The three battery holes, now closed -----------------------------------

def test_recapture_cannot_escalate_truth_state(tmp_path, monkeypatch):
    """A re-capture must not silently escalate CANDIDATE -> RATIFIED."""
    _write_via_locked(tmp_path, monkeypatch, "CANDIDATE")
    entry = _write_via_locked(tmp_path, monkeypatch, "RATIFIED")
    assert entry["truth_state"] == "CANDIDATE", (
        f"POISON: truth_state escalated to {entry['truth_state']} without promotion evidence"
    )


def test_unknown_truth_state_clamped_to_candidate(tmp_path, monkeypatch):
    """States outside the governed vocabulary must be refused, not recorded."""
    entry = _write_via_locked(tmp_path, monkeypatch, "ABSOLUTE_TRUTH")
    assert entry["truth_state"] == "CANDIDATE", (
        f"POISON: ungoverned truth_state {entry['truth_state']!r} accepted"
    )


def test_audit_registry_flags_fabricated_truth_state(tmp_path):
    """The CI ratchet must see fabricated authority, not just structural drift."""
    reg_path = _clean_audit_root(tmp_path)
    doc = json.loads(reg_path.read_text(encoding="utf-8"))
    doc["entries"][0]["truth_state"] = "RATIFIED"  # hand-edited, no provenance
    reg_path.write_text(json.dumps(doc), encoding="utf-8")
    report = mod.audit_registry(root=tmp_path)
    assert report["ok"] is False, "detector missed fabricated truth_state"
    assert report["counts"].get("elevated_without_provenance", 0) >= 1, report["defects"]


# --- Adversarial controls ---------------------------------------------------

def test_new_capture_always_enters_candidate(tmp_path, monkeypatch):
    """Capture is not ratification: a fresh note claiming RATIFIED lands CANDIDATE."""
    entry = _write_via_locked(tmp_path, monkeypatch, "RATIFIED", ib="IB-NEW", sn_id="SN-002")
    assert entry["truth_state"] == "CANDIDATE"


def test_recapture_cannot_demote_either(tmp_path, monkeypatch):
    """The write path never changes authority: a RATIFIED entry re-captured
    with CANDIDATE stays RATIFIED. Stripping authority via raw capture is a
    poisoning vector; demotion-for-containment goes through the guard."""
    entry = _write_via_locked(tmp_path, monkeypatch, "RATIFIED", ib="IB-D", sn_id="SN-003")
    assert entry["truth_state"] == "CANDIDATE"  # new entry: clamped (see above)
    # Simulate a legitimately elevated entry, then re-capture over it.
    reg_path = tmp_path / ".naya" / "memory" / "smart-notes" / "index.json"
    doc = json.loads(reg_path.read_text(encoding="utf-8"))
    target = next(e for e in doc["entries"] if e["intelligent_block_id"] == "IB-D")
    target["truth_state"] = "RATIFIED"
    target["elevation_history"] = [{
        "from": "CANDIDATE", "to": "RATIFIED", "authority": "shawn",
        "evidence_hashes": ["a" * 64], "evidence_types": ["document"],
        "at": "t", "kind": "elevation",
    }]
    reg_path.write_text(json.dumps(doc), encoding="utf-8")
    entry = _write_via_locked(tmp_path, monkeypatch, "CANDIDATE", ib="IB-D", sn_id="SN-003")
    assert entry["truth_state"] == "RATIFIED"
    assert entry["elevation_history"][0]["authority"] == "shawn"


def test_recapture_preserves_elevation_history(tmp_path, monkeypatch):
    """Supersession must not erase authority history (defect class:
    supersession_erased_history)."""
    history = [{
        "from": "CANDIDATE", "to": "VERIFIED", "authority": "naya-2",
        "evidence_hashes": ["b" * 64], "evidence_types": ["test-report"],
        "at": "t", "kind": "elevation",
    }]
    reg_path = tmp_path / ".naya" / "memory" / "smart-notes" / "index.json"
    _write_via_locked(tmp_path, monkeypatch, "CANDIDATE", ib="IB-H", sn_id="SN-004")
    doc = json.loads(reg_path.read_text(encoding="utf-8"))
    target = next(e for e in doc["entries"] if e["intelligent_block_id"] == "IB-H")
    target["truth_state"] = "VERIFIED"
    target["elevation_history"] = history
    reg_path.write_text(json.dumps(doc), encoding="utf-8")
    entry = _write_via_locked(tmp_path, monkeypatch, "RATIFIED", ib="IB-H", sn_id="SN-004")
    assert entry["truth_state"] == "VERIFIED"
    assert entry["elevation_history"] == history


def test_garbage_on_disk_state_collapses_to_candidate(tmp_path, monkeypatch):
    """Fail closed: a garbage state already on disk is not preserved."""
    reg_path = tmp_path / ".naya" / "memory" / "smart-notes" / "index.json"
    _write_via_locked(tmp_path, monkeypatch, "CANDIDATE", ib="IB-G", sn_id="SN-005")
    doc = json.loads(reg_path.read_text(encoding="utf-8"))
    target = next(e for e in doc["entries"] if e["intelligent_block_id"] == "IB-G")
    target["truth_state"] = "BLESSED"
    reg_path.write_text(json.dumps(doc), encoding="utf-8")
    entry = _write_via_locked(tmp_path, monkeypatch, "CANDIDATE", ib="IB-G", sn_id="SN-005")
    assert entry["truth_state"] == "CANDIDATE"


def test_incoming_state_ignored_for_existing_entry(tmp_path, monkeypatch):
    """Every ladder rung is ignored on re-capture — not just RATIFIED."""
    _write_via_locked(tmp_path, monkeypatch, "CANDIDATE", ib="IB-L", sn_id="SN-006")
    for rung in ("TESTING", "VERIFIED", "RATIFIED", "ACTIVE", "LEARNED"):
        entry = _write_via_locked(tmp_path, monkeypatch, rung, ib="IB-L", sn_id="SN-006")
        assert entry["truth_state"] == "CANDIDATE", f"rung {rung} leaked through the write path"


# --- Grandfathering: legacy truth does not red the ratchet ------------------

def test_grandfathered_legacy_ratified_passes_semantic_audit():
    """The eight pre-machinery director ratifications are named, dated,
    attributed, reported-not-blocking — the ratchet stays green on legacy."""
    registry = {"entries": [
        {"smart_note_id": sn, "truth_state": "RATIFIED"}
        for sn in sorted(g.LEGACY_GRANDFATHERED_ELEVATIONS)
    ]}
    r = g.audit_registry_semantics(registry)
    assert r["ok"], r["defects"]
    assert r["defect_total"] == 0


def test_non_grandfathered_fabrication_still_flagged():
    """A new note cannot hide behind the grandfather list."""
    registry = {"entries": [
        {"smart_note_id": "SN-9999", "truth_state": "RATIFIED"},
    ]}
    r = g.audit_registry_semantics(registry)
    assert not r["ok"]
    assert r["defects"]["elevated_without_provenance"] == ["SN-9999"]


def test_grandfather_list_is_closed():
    """The list documents exactly the eight known pre-machinery ratifications."""
    assert len(g.LEGACY_GRANDFATHERED_ELEVATIONS) == 8
    assert "SN-016" in g.LEGACY_GRANDFATHERED_ELEVATIONS


def test_full_audit_clean_on_grandfathered_registry(tmp_path):
    """End-to-end: a clean fixture whose entry is a grandfathered legacy
    RATIFIED passes the full audit_registry (structural + semantic)."""
    reg_path = _clean_audit_root(tmp_path)
    doc = json.loads(reg_path.read_text(encoding="utf-8"))
    doc["entries"][0]["smart_note_id"] = "SN-016"
    doc["entries"][0]["truth_state"] = "RATIFIED"
    reg_path.write_text(json.dumps(doc), encoding="utf-8")
    report = mod.audit_registry(root=tmp_path)
    assert report["ok"], report["defects"]
