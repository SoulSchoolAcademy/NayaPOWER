#!/usr/bin/env python3
"""IH-03 — prove one canonical intelligence identity end-to-end.

Proof chain:
canonical Smart Note event → PIS projection → verified Intelligent Block → feed projection.

The test uses the existing canonical Smart Note transaction and CCT boundary.
It creates no second authority and no alternate feed.
"""
from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    tx = load(ROOT / ".naya/runtime/smart_note_transaction.py", "ih03_tx")
    builder = load(ROOT / "scripts/build-smart-feed-projection.py", "ih03_pis_builder")

    with tempfile.TemporaryDirectory(prefix="naya-ih03-") as raw:
        temp = Path(raw)
        tx.ROOT = temp
        tx.SMART_NOTES_ROOT = temp / "SUPERBRAIN/SMART-NOTES"
        tx.CIS_ROOT = temp / ".naya/memory/intelligence"
        tx.CIS_PATH = tx.CIS_ROOT / "CIS.json"
        tx.RECEIPTS_ROOT = tx.CIS_ROOT / "transactions"
        tx.PIS_PATH = temp / "NAYANET/HUB/public/intelligence/pis-feed.json"
        tx.build_pis_projection = lambda note: builder.build_projection(source_root=temp, output=tx.PIS_PATH)

        timestamp = "2026-09-17T20:00:00+00:00"
        note = {
            "timestamp": timestamp,
            "topic": "IH-03 Canonical Intelligence Identity",
            "in_a_nutshell": "One intelligence object must remain one identity across every projection.",
            "child": "One thing, one ID, everywhere.",
            "grammar": "Identity is preserved through projection rather than recreated at each surface.",
            "human": "The canonical intelligence event must arrive in the feed without losing who and when it came from.",
            "naya": "Preserve identity, provenance, privacy, and verification state across the complete projection chain.",
            "machine": "Persist the canonical event, project it into PIS, bind one Intelligent Block to that event, and expose that same block to the feed.",
            "learning": "Projection must preserve lineage rather than manufacture a new intelligence identity.",
            "why_it_matters": "Without stable lineage, the Hub can display copies that cannot be trusted as the same intelligence.",
            "how_to_use": "Use the canonical event ID as the immutable identity across PIS, Intelligent Block, and feed.",
            "value": "A human can follow one intelligence object from source to visible feed and trust its lineage.",
            "evidence": ["IH-03 automated end-to-end proof"],
            "current_state": "Canonical source-to-feed identity proof is being exercised in an isolated repository-shaped transaction.",
            "next_action": "Preserve this identity contract in all future Hub projections.",
        }

        result = tx.execute(note)
        receipt = json.loads(result["receipt"].read_text(encoding="utf-8"))
        pis = json.loads(tx.PIS_PATH.read_text(encoding="utf-8"))
        event = next(e for e in pis["events"] if e["event_id"] == receipt["smart_note_id"])
        block = event.get("intelligent_block")
        assert block is not None, "PIS event has no Intelligent Block"
        assert block["block_id"] == f"IB-{event['event_id']}"
        assert block["content"]["event_id"] == event["event_id"]
        assert block["provenance"]["parent"] == event["event_id"]
        assert block["provenance"]["derivation"] == "pis-to-personal-feed"
        assert block["permissions"] == {"consumers": ["nayanet-hub.personal-feed"], "purposes": ["consume"]}
        assert block["verification"] == "SUPPORTED"
        assert block["lifecycle"] == "ACTIVE"
        assert block["integrity"]["algorithm"] == "sha256"

        # Identity and timestamp are invariant from canonical persistence → PIS → block.
        assert receipt["smart_note_id"] == event["event_id"]
        assert receipt["pis"]["event_id"] == event["event_id"]
        assert event["created_at"] == timestamp
        assert event["updated_at"] == timestamp
        assert event["human_input"]["captured_at"] == timestamp

        # Provenance and privacy are invariant at the event boundary.
        assert event["source"]["id"] == event["event_id"]
        assert event["context"]["canonical_path"] == receipt["smart_note_path"]
        assert event["privacy"] == {"visibility": "private", "consent_state": "not_granted"}

        # Feed projection consumes the same event object identity; it does not invent another ID.
        feed_events = pis["events"]
        feed_matches = [e for e in feed_events if e["event_id"] == event["event_id"]]
        assert len(feed_matches) == 1
        assert feed_matches[0]["intelligent_block"]["block_id"] == block["block_id"]

        # Re-project the same canonical source and prove identity/timestamp remain stable.
        replay = tx.execute(note)
        replay_receipt = json.loads(replay["receipt"].read_text(encoding="utf-8"))
        replay_pis = json.loads(tx.PIS_PATH.read_text(encoding="utf-8"))
        replay_event = next(e for e in replay_pis["events"] if e["event_id"] == event["event_id"])
        assert replay_receipt["smart_note_id"] == event["event_id"]
        assert replay_event["event_id"] == event["event_id"]
        assert replay_event["created_at"] == event["created_at"] == timestamp
        assert replay_event["updated_at"] == event["updated_at"] == timestamp
        assert replay_event["context"]["canonical_path"] == event["context"]["canonical_path"]
        assert replay_event["privacy"] == event["privacy"]
        assert replay_event["intelligent_block"]["block_id"] == block["block_id"]

        print("IH03_CANONICAL_EVENT=PASS")
        print("IH03_PIS_IDENTITY=PASS")
        print("IH03_INTELLIGENT_EVENT_ID=PASS")
        print("IH03_INTELLIGENT_BLOCK=PASS")
        print("IH03_FEED_PROJECTION=PASS")
        print("IH03_TIMESTAMP_INVARIANT=PASS")
        print("IH03_PROVENANCE_INVARIANT=PASS")
        print("IH03_PRIVACY_INVARIANT=PASS")
        print("IH03_VERIFICATION_STATE=PASS")
        print("IH03_REPLAY_IDENTITY_STABLE=PASS")
        print(f"IH03_EVENT_ID={event['event_id']}")
        print(f"IH03_BLOCK_ID={block['block_id']}")
        print("IH03=PASS")


if __name__ == "__main__":
    main()
