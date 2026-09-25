from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".naya" / "memory"))

import smart_notes_v3 as brain


def _objects():
    return [
        {
            "intelligent_block_id": "IB-000001",
            "canonical": True,
            "date": "2026-09-24",
            "status": "CANONICAL",
            "category": "system",
            "topic": "memory",
            "owner": "shawn",
            "scope": "personal",
            "project": "NayaPOWER",
            "permissions": {"access": "PRIVATE"},
            "content": "# SMART NOTE\nMemory retrieval and continuity.",
            "source": {
                "registry": ".naya/memory/smart-notes/REGISTRY.json",
                "intelligent_block_id": "IB-000001",
                "provenance": {"source_event_id": "SE-1"},
            },
        },
        {
            "intelligent_block_id": "IB-000002",
            "canonical": True,
            "date": "2026-09-20",
            "status": "SUPERSEDED",
            "category": "system",
            "topic": "old-memory",
            "owner": "shawn",
            "scope": "personal",
            "project": "NayaPOWER",
            "permissions": {"access": "PRIVATE"},
            "content": "# SMART NOTE\nOld memory.",
            "source": {
                "registry": ".naya/memory/smart-notes/REGISTRY.json",
                "intelligent_block_id": "IB-000002",
                "provenance": {"source_event_id": "SE-2"},
            },
        },
    ]


def test_canonical_retrieval_defaults_to_current_intelligence(monkeypatch):
    monkeypatch.setattr(brain, "load_canonical_ibs", lambda root=None: _objects())
    results = brain.retrieve_canonical_ibs(
        "memory continuity",
        limit=10,
        principal_id="shawn",
        scope="personal",
        project="NayaPOWER",
        principal_project="NayaPOWER",
    )
    assert [x["intelligent_block_id"] for x in results] == ["IB-000001"]


def test_canonical_retrieval_can_explicitly_include_history(monkeypatch):
    monkeypatch.setattr(brain, "load_canonical_ibs", lambda root=None: _objects())
    results = brain.retrieve_canonical_ibs(
        "old memory",
        limit=10,
        principal_id="shawn",
        scope="personal",
        project="NayaPOWER",
        principal_project="NayaPOWER",
        include_historical=True,
    )
    assert [x["intelligent_block_id"] for x in results] == ["IB-000002"]


def test_canonical_retrieval_respects_temporal_boundary(monkeypatch):
    monkeypatch.setattr(brain, "load_canonical_ibs", lambda root=None: _objects())
    results = brain.retrieve_canonical_ibs(
        "memory",
        limit=10,
        principal_id="shawn",
        scope="personal",
        project="NayaPOWER",
        principal_project="NayaPOWER",
        effective_on="2026-09-22",
    )
    assert [x["intelligent_block_id"] for x in results] == ["IB-000002"]


def test_canonical_retrieval_preserves_provenance_fields(monkeypatch):
    monkeypatch.setattr(brain, "load_canonical_ibs", lambda root=None: _objects())
    results = brain.retrieve_canonical_ibs(
        "memory continuity",
        limit=1,
        principal_id="shawn",
        scope="personal",
        project="NayaPOWER",
        principal_project="NayaPOWER",
    )
    assert results[0]["source"]["intelligent_block_id"] == "IB-000001"
    assert results[0]["source"]["provenance"]["source_event_id"] == "SE-1"
