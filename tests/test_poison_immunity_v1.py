"""POISON immune battery v1 — the merge gate must reject poisoned intelligence.

Each case injects one poison class into a clean fixture and asserts the
gate refuses it. The gate under test is audit_registry (the CI ratchet) plus
the registry write path (_update_registry_locked).

A poison the gate cannot see is marked xfail(strict=True): a DOCUMENTED
HOLE, not a pass. When the hole is repaired, the xfail flips to a pass and
the battery goes fully green. An xpass (strict) fails loudly so a silent
repair cannot hide.

Threat model: a crafted capture (compromised seat, injected prompt, or
hand-edited JSON) enters through the normal write path. Structural poisons
must be caught by audit_registry; semantic poisons (fabricated authority)
must be caught by truth-state transition validation on the write path.
"""
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("smart_note_v2", ROOT / "tools" / "smart_note_v2.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

PAGE = "BRAIN/05-MEMORY/SMART-NOTES/2026/01/01/CAT/TOPIC/SUB/SN-001/IB-1.md"


def _hash(intelligence):
    return mod._canonical_content_hash(
        json.dumps(intelligence, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    )


def build_clean_root(tmp_path):
    """Minimal fully-reconciled tree: one capture, one entry, one page."""
    intelligence = {"essence": "a", "distilled_intelligence": "b"}
    cap_dir = tmp_path / ".naya" / "capture"
    cap_dir.mkdir(parents=True)
    (cap_dir / "c1.json").write_text(
        json.dumps({"smart_note_id": "SN-001", "intelligence": intelligence}), encoding="utf-8"
    )
    page = tmp_path / PAGE
    page.parent.mkdir(parents=True)
    page.write_text("# IB-1\n", encoding="utf-8")
    reg_path = tmp_path / ".naya" / "memory" / "smart-notes" / "index.json"
    reg_path.parent.mkdir(parents=True)
    reg_path.write_text(
        json.dumps(
            {
                "schema": "naya.smart-note-projection-index.v1",
                "entries": [
                    {
                        "smart_note_id": "SN-001",
                        "intelligent_block_id": "IB-1",
                        "content_hash": _hash(intelligence),
                        "projection_path": PAGE,
                        "projection_status": "GITHUB_BRAIN_PUBLISHED",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    return reg_path


# ---------------------------------------------------------------------------
# Structural poisons — audit_registry must catch every one (detector proven).
# ---------------------------------------------------------------------------

def _mutate_orphan_page(root):
    p = root / "BRAIN/05-MEMORY/SMART-NOTES/2026/01/03/CAT/TOPIC/SUB/SN-009/IB-9.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("# IB-9\nPOISON: fabricated RATIFIED lesson, no registry entry.\n", encoding="utf-8")


def _mutate_stale_hash(root):
    reg = root / ".naya" / "memory" / "smart-notes" / "index.json"
    entries = json.loads(reg.read_text(encoding="utf-8"))["entries"]
    entries[0]["content_hash"] = "0" * 64
    doc = json.loads(reg.read_text(encoding="utf-8"))
    doc["entries"] = entries
    reg.write_text(json.dumps(doc), encoding="utf-8")


def _mutate_duplicate_sn(root):
    reg = root / ".naya" / "memory" / "smart-notes" / "index.json"
    doc = json.loads(reg.read_text(encoding="utf-8"))
    doc["entries"].append(dict(doc["entries"][0]))
    reg.write_text(json.dumps(doc), encoding="utf-8")


def _mutate_hashless_entry(root):
    reg = root / ".naya" / "memory" / "smart-notes" / "index.json"
    doc = json.loads(reg.read_text(encoding="utf-8"))
    doc["entries"][0]["content_hash"] = None
    reg.write_text(json.dumps(doc), encoding="utf-8")


def _mutate_ghost_projection(root):
    reg = root / ".naya" / "memory" / "smart-notes" / "index.json"
    doc = json.loads(reg.read_text(encoding="utf-8"))
    doc["entries"][0]["projection_path"] = PAGE.replace("IB-1.md", "IB-MISSING.md")
    reg.write_text(json.dumps(doc), encoding="utf-8")


@pytest.mark.parametrize(
    "mutate,expected_class",
    [
        pytest.param(_mutate_orphan_page, "published_pages_without_registry_entry", id="orphan_poison_page"),
        pytest.param(_mutate_stale_hash, "entries_with_stale_hash", id="fabricated_hash"),
        pytest.param(_mutate_duplicate_sn, "duplicate_smart_note_ids", id="duplicate_sn_id"),
        pytest.param(_mutate_hashless_entry, "entries_without_hash", id="hashless_entry"),
        pytest.param(_mutate_ghost_projection, "registry_projection_paths_absent", id="ghost_projection"),
    ],
)
def test_structural_poison_rejected(tmp_path, mutate, expected_class):
    """Every structural poison class must be caught by the audit detector."""
    build_clean_root(tmp_path)
    assert mod.audit_registry(root=tmp_path)["ok"] is True, "fixture must start clean"
    mutate(tmp_path)
    report = mod.audit_registry(root=tmp_path)
    assert report["ok"] is False, f"detector missed poison class {expected_class}"
    assert report["counts"][expected_class] >= 1, report["defects"]


# ---------------------------------------------------------------------------
# Semantic poisons — fabricated authority. KNOWN HOLE (xfail).
#
# _update_registry_locked copies block["understanding_state"] verbatim into
# the entry's truth_state and REPLACES the existing entry for the same IB.
# A poisoned re-capture can therefore escalate CANDIDATE -> RATIFIED (or
# invent states like ABSOLUTE_TRUTH), bypassing promote_note()'s evidence
# thresholds entirely. audit_registry has no truth_state defect class, so
# the fabrication is also invisible to the CI ratchet.
# ---------------------------------------------------------------------------

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


@pytest.mark.xfail(strict=True, reason="KNOWN HOLE: write path allows truth_state escalation, bypassing promote_note()")
def test_truth_state_escalation_rejected(tmp_path, monkeypatch):
    """A re-capture must not silently escalate CANDIDATE -> RATIFIED."""
    _write_via_locked(tmp_path, monkeypatch, "CANDIDATE")
    entry = _write_via_locked(tmp_path, monkeypatch, "RATIFIED")
    assert entry["truth_state"] == "CANDIDATE", (
        f"POISON: truth_state escalated to {entry['truth_state']} without promotion evidence"
    )


@pytest.mark.xfail(strict=True, reason="KNOWN HOLE: write path accepts arbitrary truth_state strings")
def test_invalid_truth_state_value_rejected(tmp_path, monkeypatch):
    """States outside the governed vocabulary must be refused or normalized."""
    entry = _write_via_locked(tmp_path, monkeypatch, "ABSOLUTE_TRUTH")
    assert entry["truth_state"] in ("CANDIDATE", "VERIFIED", "RATIFIED"), (
        f"POISON: ungoverned truth_state {entry['truth_state']!r} accepted"
    )


@pytest.mark.xfail(strict=True, reason="KNOWN HOLE: audit_registry has no truth_state defect class")
def test_audit_flags_fabricated_truth_state(tmp_path):
    """The CI ratchet must see fabricated authority, not just structural drift."""
    reg_path = build_clean_root(tmp_path)
    doc = json.loads(reg_path.read_text(encoding="utf-8"))
    doc["entries"][0]["truth_state"] = "RATIFIED"
    reg_path.write_text(json.dumps(doc), encoding="utf-8")
    report = mod.audit_registry(root=tmp_path)
    assert report["ok"] is False, "detector missed fabricated truth_state"
