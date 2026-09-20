#!/usr/bin/env python3
"""Acceptance proof for NOTE EVENT → PIS → fresh-Naya retrieval."""
from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

engine = load_module(ROOT / "tools" / "promote_intelligence.py", "promotion_engine")
pis = load_module(ROOT / "tools" / "propagate_intelligence_to_pis.py", "pis_propagator")
memory = load_module(ROOT / ".naya" / "memory" / "memory_runtime.py", "memory_runtime")


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        events = root / "events"; receipts = root / "receipts"; naya = root / "naya"; shawn = root / "shawn"; feed = root / "feed"; hub = root / "hub.md"
        pis_dir = root / "pis"; index = root / "INDEX.json"
        for p in (events, receipts, naya, shawn, feed, pis_dir): p.mkdir(parents=True)
        hub.write_text("# Hub\n", encoding="utf-8")
        index.write_text(json.dumps({"schema":"naya-power-memory-index/v2","generated_at":"2026-09-11T00:00:00Z","authority":"fixture","notes":[],"categories":{},"aliases":{},"relationships":{},"temporal":{"active":[],"historical":[],"superseded":[]},"event_index":{}})+"\n", encoding="utf-8")

        engine.EVENT_DIR=events; engine.RECEIPT_DIR=receipts; engine.NAYA_DIR=naya; engine.SHAWN_DIR=shawn; engine.FEED_DIR=feed; engine.HUB_PATH=hub
        pis.EVENT_DIR=events; pis.PIS_DIR=pis_dir; pis.INDEX_PATH=index
        memory.NOTE_DIR=pis_dir; memory.INDEX=index

        event={
            "event_id":"SE-20260911-071500-pis-acceptance",
            "timestamp":"2026-09-11T07:15:00Z",
            "project":"PIS-ACCEPTANCE",
            "lesson":"A propagated intelligence event must be retrievable by a fresh Naya through the canonical Smart Notes runtime.",
            "source":["tools/test_superbrain_note_event_to_pis.py"],
            "evidence_state":"TESTED",
            "promotion_status":"PROPOSED",
            "candidate_homes":["NAYA_NOTE"],
            "what_happened":"The acceptance fixture created one canonical intelligence event.",
            "value":"A successor can retrieve the lesson without the source conversation.",
            "actual_outcome":"Promotion created the Naya representation and running-feed projection.",
            "evidence":["fixture"],
            "next_action":"Retrieve the lesson through memory_runtime from a fresh successor context.",
            "successor_instruction":"Read the propagated lesson before selecting the next action.",
            "title":"PIS acceptance propagation lesson"
        }
        event_path=events/(event["event_id"]+".json"); event_path.write_text(json.dumps(event,indent=2)+"\n",encoding="utf-8")

        assert engine.main()==0
        assert (naya/(event["event_id"]+".md")).exists()
        assert (feed/(event["event_id"]+".md")).exists()

        assert pis.main()==0
        nid=pis.note_id(event)
        canonical=pis_dir/(nid+".json")
        assert canonical.exists()
        note=json.loads(canonical.read_text(encoding="utf-8"))
        assert note["event_id"]==event["event_id"]
        assert note["relationships"]["same_event"]==event["event_id"]
        assert note["verification"]["status"]=="PENDING"

        retrieved=memory.retrieve("propagated intelligence event fresh Naya",10)
        assert retrieved, "fresh Smart Notes runtime could not retrieve propagated intelligence"
        assert retrieved[0][1]["id"]==nid

        restored=memory.restore("fresh Naya propagated intelligence")
        assert any(item["note"]["id"]==nid for item in restored["retrieved"])

        # Idempotency: a second propagation changes nothing and does not duplicate the note/index entry.
        assert pis.main()==0
        indexed=json.loads(index.read_text(encoding="utf-8"))["notes"]
        assert indexed.count(nid)==1

    print("PASS — NOTE EVENT → PIS → fresh-Naya retrieval → idempotent re-propagation")
    print("NOTE_EVENT_TO_PIS=PASS")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
