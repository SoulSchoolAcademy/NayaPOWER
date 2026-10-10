"""Registry writer must not erase machine-managed truth history.

Regression test for the re-ingestion hole: `_update_registry_locked` rebuilds
entries from the capture, and before the fix it silently dropped
`elevation_history` on re-registration. That erases the provenance the
write-time guard protects (apply_elevation rejects SUPERSESSION_ERASES_AUTHORITY)
and would regress the read-side CI audit (truth_state_guard --audit) to
flagging grandfathered ratifications after any re-ingest of the 8 backfilled
notes.

The writer module is loaded standalone via importlib so this pins the
preservation contract independently of the promotion machinery.
"""
import copy
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WRITER = ROOT / "tools" / "smart_note_v2.py"

spec = importlib.util.spec_from_file_location("smart_note_v2", WRITER)
w = importlib.util.module_from_spec(spec)
spec.loader.exec_module(w)

IB = "IB-TEST-HISTORY-001"
SN = "SN-0999"
HISTORY = [{
    "from": "CANDIDATE",
    "to": "RATIFIED",
    "authority": "Human Director",
    "authority_detail": "Shawn Vibert 2026-10-07: Make it so. Word. (test fixture)",
    "evidence_hashes": ["sha256:" + "ab" * 32],
    "evidence_types": ["ratification-record"],
    "at": "2026-10-07T00:00:00+00:00",
    "recorded_at": "2026-10-10T00:00:00Z",
    "kind": "backfill",
}]


def _registry_with_history():
    return {"entries": [{
        "smart_note_id": SN,
        "intelligent_block_id": IB,
        "truth_state": "RATIFIED",
        "title": "fixture note",
        "elevation_history": copy.deepcopy(HISTORY),
    }]}


def _capture():
    return {
        "title": "fixture note",
        "smart_note_id": SN,
        "source": {"captured_at": "2026-10-10T00:00:00Z"},
        "category": "SMART_NOTE",
        "topic": "",
        "subtopic": "",
        "lifecycle_state": "ACTIVE",
    }


def _verify():
    return {"persisted": {
        "block": {
            "intelligent_block_id": IB,
            "content": {"lesson": "the lesson text"},
            "understanding_state": "RATIFIED",
            "owner_scope": "PRIVATE",
        },
        "event": {"id": "e-fixture"},
        "lineage": {"id": "l-fixture"},
        "relationship": {"relationship_id": "r-fixture"},
        "index": {"id": "i-fixture"},
        "checkpoint": {"id": "c-fixture"},
        "receipt": {"id": "rc-fixture"},
    }}


def _projection():
    return w.ROOT / "BRAIN" / "05-MEMORY" / "fixture.md"


def test_reingestion_preserves_elevation_history():
    registry = _registry_with_history()
    entry = w._update_registry_locked(_capture(), _verify(), _projection(),
                                      registry, sn_id=SN)
    assert entry["elevation_history"] == HISTORY, \
        "re-ingestion dropped the note's elevation history"
    assert len(registry["entries"]) == 1, "re-ingestion must replace, not duplicate"


def test_fresh_entry_gets_no_fabricated_history():
    registry = {"entries": []}
    entry = w._update_registry_locked(_capture(), _verify(), _projection(),
                                      registry, sn_id=SN)
    assert "elevation_history" not in entry, \
        "the writer must never invent elevation history"


def test_history_survives_even_when_truth_state_changes():
    # Re-ingestion may legitimately update truth_state from the capture; the
    # machine history of HOW it got there must still be carried over.
    registry = _registry_with_history()
    verify = _verify()
    verify["persisted"]["block"]["understanding_state"] = "LEARNED"
    entry = w._update_registry_locked(_capture(), verify, _projection(),
                                      registry, sn_id=SN)
    assert entry["truth_state"] == "LEARNED"
    assert entry["elevation_history"] == HISTORY
