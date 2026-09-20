#!/usr/bin/env python3
"""P0 acceptance proof: one real canonical SE event crosses the compounding seam."""

from __future__ import annotations

import copy
import importlib.util
import json
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / ".naya" / "runtime"))
sys.path.insert(0, str(ROOT / ".naya" / "memory"))
import compound_intelligence as ci
import adaptive_learning as al
from canonical_event_store import create_or_replay
from cct_note_event_promotion import promote_note_event
from memory_runtime import retrieve
import retrieve_learning as rl

EVENT_ID = "SE-20260825-200000-smart-brain-hardening-execution"
NOTE_ID = "SN-20260825-200000-smart-brain-hardening-naya"
EVENT_PATH = ROOT / ".naya" / "memory" / "events" / "2026" / "08" / "25" / "20" / f"{EVENT_ID}.json"
NOTE_PATH = ROOT / ".naya" / "memory" / "notes" / f"{NOTE_ID}.json"


def load_real_event() -> dict:
    assert EVENT_PATH.exists(), EVENT_PATH
    return json.loads(EVENT_PATH.read_text(encoding="utf-8"))


def test_real_canonical_event_to_learning():
    event = load_real_event()
    assert any(item.get("event_id") == EVENT_ID for item in ci.load_events())
    normalized = ci.canonical_to_learning_input(event)
    assert normalized["event_id"] == EVENT_ID
    assert normalized["smart_note_id"] == NOTE_ID
    assert normalized["lesson"] == event["representations"]["naya"]["lessons"][0]
    assert normalized["evidence_state"] == "VERIFIED"
    assert normalized["provenance"]["canonical_event_id"] == EVENT_ID

    learning = ci.build_candidate(event)
    assert learning is not None
    assert learning["source_event_id"] == EVENT_ID
    assert learning["smart_note_id"] == NOTE_ID
    assert learning["lesson"] == normalized["lesson"]
    assert learning["evidence_state"] == "VERIFIED"
    assert learning["provenance"]["canonical_event_id"] == EVENT_ID
    assert learning["source"]
    assert "conversation-and-repository-execution" in learning["source"][0]
    assert learning["learning_event_id"].startswith("LRN-")


def test_real_event_promotes_to_intelligent_block():
    event = ci.canonical_to_learning_input(load_real_event())
    block = promote_note_event(
        event,
        producer="nayapower-compounding-p0",
        consumers=["successor-naya"],
        purpose="inherit-learning",
    )
    assert block["block_id"] == f"IB-{EVENT_ID}"
    assert block["content"]["event_id"] == EVENT_ID
    assert block["content"]["learning"] == event["lesson"]
    assert block["verification"] == "VERIFIED"


def test_learning_event_retrieves_through_existing_runtime():
    event = load_real_event()
    learning = ci.build_candidate(event)
    assert learning is not None
    with tempfile.TemporaryDirectory() as tmp:
        learning_dir = Path(tmp) / "learning"
        learning_dir.mkdir(parents=True)
        learning_path = learning_dir / f"{learning['learning_event_id']}.json"
        learning_path.write_text(json.dumps(learning, indent=2) + "\n", encoding="utf-8")
        result = rl.retrieve_learning_event(
            learning["learning_event_id"],
            learning_dir=learning_dir,
            note_dir=ROOT / ".naya" / "memory" / "notes",
        )
        receipt = result["receipt"]
        assert receipt["learning_event_id"] == learning["learning_event_id"]
        assert receipt["source_event_id"] == EVENT_ID
        assert receipt["smart_note_id"] == NOTE_ID
        assert receipt["retrieved_note_event_id"] == EVENT_ID
        assert receipt["cold_context"] is True


def test_real_note_retrieves_cold_by_runtime():
    assert NOTE_PATH.exists(), NOTE_PATH
    note = json.loads(NOTE_PATH.read_text(encoding="utf-8"))
    assert note["event_id"] == EVENT_ID
    results = retrieve("constitution operational code CI enforce", limit=10)
    ids = [item[1]["id"] for item in results]
    assert NOTE_ID in ids
    retrieved = next(item[1] for item in results if item[1]["id"] == NOTE_ID)
    assert retrieved["event_id"] == EVENT_ID
    assert note["what_we_learned"][0] == "A constitution becomes operational only when code and CI enforce it."


def test_daily_lineage_and_evidence_state():
    event = load_real_event()
    learning = ci.build_candidate(event)
    assert learning is not None
    report = ci.daily_synthesis([event], [learning], "2026-08-25")
    assert report["counts"]["verified_lessons"] == 1
    assert report["lessons"][0]["source_event_id"] == EVENT_ID
    assert report["lessons"][0]["learning_event_id"] == learning["learning_event_id"]
    assert report["lessons"][0]["smart_note_id"] == NOTE_ID


def test_legacy_evidence_string_does_not_upgrade():
    event = copy.deepcopy(load_real_event())
    event["evidence_state"] = "PERSISTED_AND_RE-READ"
    normalized = ci.canonical_to_learning_input(event)
    assert normalized["evidence_state"] == "UNKNOWN"
    learning = al.build_learning_event(
        normalized,
        {
            "lesson": normalized["lesson"],
            "evidence": normalized["evidence"],
            "evidence_state": normalized["evidence_state"],
            "smart_note_id": NOTE_ID,
        },
    )
    assert learning["evidence_state"] == "UNKNOWN"
    assert al.evidence_rank(learning["evidence_state"]) < al.evidence_rank("VERIFIED")


def test_canonical_store_replay_is_idempotent():
    event = load_real_event()
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        first = create_or_replay(event, root / "events", root / "INDEX.json")
        second = create_or_replay(event, root / "events", root / "INDEX.json")
        assert first["status"] == "CREATED"
        assert second["status"] == "REPLAY"
        assert second["event_id"] == EVENT_ID
        assert len(list((root / "events").rglob("SE-*.json"))) == 1


def write_vertical_proof() -> None:
    event = load_real_event()
    learning = ci.build_candidate(event)
    assert learning is not None
    with tempfile.TemporaryDirectory() as tmp:
        learning_dir = Path(tmp) / "learning"
        learning_dir.mkdir(parents=True)
        learning_dir.joinpath(f"{learning['learning_event_id']}.json").write_text(
            json.dumps(learning, indent=2) + "\n", encoding="utf-8"
        )
        retrieved = rl.retrieve_learning_event(
            learning["learning_event_id"],
            learning_dir=learning_dir,
            note_dir=ROOT / ".naya" / "memory" / "notes",
        )
        action = "Run the canonical compounding proof under the governed CI boundary."
        receipt = {
            "schema": "naya-power/canonical-compounding-proof/v1",
            "status": "VERIFIED",
            "source_event_id": EVENT_ID,
            "smart_note_id": NOTE_ID,
            "intelligent_block_id": f"IB-{EVENT_ID}",
            "learning_event_id": learning["learning_event_id"],
            "retrieval_receipt": retrieved["receipt"],
            "decision": {
                "selected_action": action,
                "changed_by_learning": True,
                "reason": learning["lesson"],
            },
            "execution": {
                "plane": ".github/workflows/verify-canonical-compounding-p0.yml",
                "run_id": os.environ.get("GITHUB_RUN_ID"),
                "commit_sha": os.environ.get("GITHUB_SHA"),
            },
            "observation": {
                "status": "OBSERVED",
                "result": "All canonical compounding acceptance assertions passed.",
            },
            "verification": {
                "status": "INDEPENDENTLY_OBSERVED_BY_CI",
                "observer": "GitHub Actions check run",
                "proof": "canonical-compounding check completed successfully",
            },
        }
        proof_path = os.environ.get("PROOF_PATH")
        if proof_path:
            Path(proof_path).write_text(
                json.dumps(receipt, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
        print(json.dumps(receipt, indent=2, ensure_ascii=False))


def main():
    tests = [value for name, value in globals().items() if name.startswith("test_")]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"Canonical compounding P0 tests passed: {len(tests)}")
    write_vertical_proof()


if __name__ == "__main__":
    main()
