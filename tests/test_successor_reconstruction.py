#!/usr/bin/env python3
"""Self-tests for tools/successor_reconstruction.py.

Tests the actual seam: can the auditor distinguish a fully reconstructable
checkpoint from the thin live state, and does the handoff validator fail
closed on malformed or authority-inheriting payloads?
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from successor_reconstruction import (
    ELEMENTS,
    HANDOFF_SCHEMA_VERSION,
    audit,
    reconstruct,
    validate_handoff,
)

REPO = Path(__file__).resolve().parent.parent
TOOL = REPO / "tools" / "successor_reconstruction.py"


def thin_live_state():
    """Mirror of the actual live nayanet_project_cognition_state row
    observed 2026-10-07 (revision 1669): link IDs + event pointers,
    successor null, no why/proven/unknown/authority/learning/next."""
    return {
        "id": "00000000-0000-0000-0000-000000000001",
        "user_id": "11111111-1111-1111-1111-111111111111",
        "project_id": "NayaNET",
        "revision": 1669,
        "status": "READY",
        "state": {
            "checkpoint_type": "intelligence",
            "index_id": "idx-1",
            "intelligent_block_id": "IB-1",
            "last_event_at": "2026-10-07T20:00:00Z",
            "last_event_id": "evt-1",
            "latest_event_id": "evt-1",
            "latest_event_key": "k1",
            "lineage_id": "lin-1",
            "provenance_preserved": True,
            "receipt_id": "rcpt-1",
            "relationship_id": "rel-1",
            "status": "CANDIDATE",
            "successor": None,
            "target_id": "NAYA-NODE-0001",
        },
    }


def thin_receipt():
    return {
        "checkpoint_id": "cp-1",
        "user_id": "11111111-1111-1111-1111-111111111111",
        "project_id": "NayaNET",
        "revision": 1669,
        "checkpoint_type": "intelligence",
        "status": "READY",
        "state": {"last_event_id": "evt-1"},
        "source_receipt_id": "rcpt-0",
        "learning_id": "learn-1",
        "event_id": "evt-1",
        "intelligent_block_id": "IB-1",
        "lineage_id": "lin-1",
        "relationship_id": "rel-1",
        "index_id": "idx-1",
        "content_hash": "abc123",
        "recorded_at": "2026-10-07T20:00:00Z",
    }


def thin_event():
    """Checkpoint event WITHOUT the rich metadata (pre-contract shape)."""
    return {
        "event_id": "evt-1",
        "type": "intelligence_checkpoint",
        "classification": "cognitive_checkpoint",
        "title": "checkpoint",
        "content": "...",
        "source": "v7-smart-note-canonical",
        "status": "active",
        "actor": "naya",
        "metadata": {},
    }


def rich_structures():
    """All three structures populated per the V1 contract."""
    state = thin_live_state()
    state["state"]["successor"] = {
        "schema_version": HANDOFF_SCHEMA_VERSION,
        "handoff_id": "ho-1",
        "director": {"name": "Shawn", "role": "Human Director"},
        "predecessor": {"seat": "Naya 5", "session": "s-1"},
        "what": "Engine surge shift",
        "why": "Successor lane at 3.5/10 is not acceptable",
        "success_criteria": ["cold trial delta measured", "replayable archive"],
        "current_truth": {"revision": 1669, "summary": "main at 5e629d3"},
        "proven": ["PR #1665 merged"],
        "unknown": ["deploy pipeline failure root cause"],
        "authority": {"scope": "SUCCESSOR lane", "inherits_authority": False},
        "history": {"checkpoint_id": "cp-1", "parent_refs": ["evt-0"]},
        "learning": ["thin state fails reconstruction"],
        "next_actions": ["run cold trial T1"],
        "proof": {"receipt_ids": ["rcpt-1"]},
        "record": {"handoff_id": "ho-1", "created_at": "2026-10-07T21:00:00Z"},
        "continuation": "Resume at next_actions[0]; do not re-audit.",
    }
    event = thin_event()
    event["metadata"] = {
        "checkpoint_id": "cp-1",
        "source_event_ids": ["evt-0"],
        "what_changed": "handoff written",
        "learned": "thin state is not reconstructable",
        "evidence_refs": [{"kind": "receipt", "receipt_id": "rcpt-1"}],
        "authority_scope": "SUCCESSOR lane",
        "unknown": ["deploy root cause"],
        "applicable_scope": None,
        "next_use": "cold trial",
        "successor_relevance": "restore, assess, apply, verify",
        "source_head": "5e629d3",
        "checkpointed_at": "2026-10-07T21:00:00Z",
    }
    return {
        "cognition_state": state,
        "checkpoint_receipt": thin_receipt(),
        "checkpoint_event": event,
    }


# --- audit: the thin live state must FAIL ---------------------------------


def test_thin_live_state_is_not_reconstructable():
    structures = {
        "cognition_state": thin_live_state(),
        "checkpoint_receipt": thin_receipt(),
        "checkpoint_event": thin_event(),
    }
    result = reconstruct(structures)
    assert result["reconstructable"] is False
    # Four elements no structure carries at all.
    for el in ("why", "unknown", "authority", "next"):
        assert result["elements"][el]["status"] == "MISSING", el
    # Three more have only weak signals (status strings, hash, bare ID
    # pointers) — a cold successor cannot reconstruct from these alone.
    for el in ("success", "proven", "learning"):
        assert result["elements"][el]["status"] == "PARTIAL", el


def test_thin_state_gap_matrix_shape():
    matrix = audit(
        {
            "cognition_state": thin_live_state(),
            "checkpoint_receipt": thin_receipt(),
            "checkpoint_event": thin_event(),
        }
    )
    assert set(matrix.keys()) == set(ELEMENTS)
    for el in ELEMENTS:
        assert matrix[el]["status"] in ("PRESENT", "PARTIAL", "MISSING")
        assert isinstance(matrix[el]["sources"], list)


def test_rich_structures_reconstructable():
    result = reconstruct(rich_structures())
    assert result["reconstructable"] is True, result["missing"]
    assert result["score"]["MISSING"] == 0


def test_cli_audit_fails_closed_on_thin_state(tmp_path):
    p = tmp_path / "thin.json"
    p.write_text(
        json.dumps(
            {
                "cognition_state": thin_live_state(),
                "checkpoint_receipt": thin_receipt(),
                "checkpoint_event": thin_event(),
            }
        )
    )
    r = subprocess.run(
        [sys.executable, "-m", "tools.successor_reconstruction", "--audit", str(p)],
        cwd=str(REPO),
        capture_output=True,
        text=True,
    )
    assert r.returncode == 1
    assert "FAIL CLOSED" in r.stderr
    body = json.loads(r.stdout)
    assert body["reconstructable"] is False


def test_cli_audit_passes_on_rich_state(tmp_path):
    p = tmp_path / "rich.json"
    p.write_text(json.dumps(rich_structures()))
    r = subprocess.run(
        [sys.executable, "-m", "tools.successor_reconstruction", "--audit", str(p)],
        cwd=str(REPO),
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr
    body = json.loads(r.stdout)
    assert body["reconstructable"] is True


# --- handoff validator ------------------------------------------------------


def valid_handoff():
    return rich_structures()["cognition_state"]["state"]["successor"]


def test_valid_handoff_passes():
    result = validate_handoff(valid_handoff())
    assert result["valid"] is True, result["errors"]
    assert all(
        v == "PRESENT" for v in result["element_coverage"].values()
    ), result["element_coverage"]


def test_handoff_missing_field_fails():
    h = valid_handoff()
    del h["why"]
    result = validate_handoff(h)
    assert result["valid"] is False
    assert any("why" in e for e in result["errors"])


def test_handoff_wrong_schema_version_fails():
    h = valid_handoff()
    h["schema_version"] = "SOMETHING_ELSE_V9"
    result = validate_handoff(h)
    assert result["valid"] is False


def test_handoff_authority_inheritance_is_hard_fail():
    h = valid_handoff()
    h["authority"]["inherits_authority"] = True
    result = validate_handoff(h)
    assert result["valid"] is False
    assert any("inherits_authority" in e for e in result["errors"])


def test_handoff_non_object_fails():
    result = validate_handoff(["not", "a", "dict"])
    assert result["valid"] is False


def test_handoff_empty_unknown_warns_not_fails():
    h = valid_handoff()
    h["unknown"] = []
    result = validate_handoff(h)
    assert result["valid"] is True
    assert any("unknown" in w for w in result["warnings"])


def test_cli_validate_handoff(tmp_path):
    p = tmp_path / "handoff.json"
    p.write_text(json.dumps(valid_handoff()))
    r = subprocess.run(
        [
            sys.executable,
            "-m",
            "tools.successor_reconstruction",
            "--validate-handoff",
            str(p),
        ],
        cwd=str(REPO),
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr
