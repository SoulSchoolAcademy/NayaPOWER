#!/usr/bin/env python3
"""End-to-end proof for one governed Smart Note transaction."""
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
    tx = load(ROOT / ".naya/runtime/smart_note_transaction.py", "smart_note_transaction")
    builder = load(ROOT / "scripts/build-smart-feed-projection.py", "pis_builder")

    with tempfile.TemporaryDirectory(prefix="naya-smart-note-e2e-") as raw:
        temp = Path(raw)
        tx.ROOT = temp
        tx.SMART_NOTES_ROOT = temp / "SUPERBRAIN/SMART-NOTES"
        tx.CIS_ROOT = temp / ".naya/memory/intelligence"
        tx.CIS_PATH = tx.CIS_ROOT / "CIS.json"
        tx.RECEIPTS_ROOT = tx.CIS_ROOT / "transactions"
        tx.PIS_PATH = temp / "NAYANET/HUB/public/intelligence/pis-feed.json"
        tx.build_pis_projection = lambda note: builder.build_projection(source_root=temp, output=tx.PIS_PATH)

        note = {
            "topic": "Smart Note Transaction Proof",
            "in_a_nutshell": "A Smart Note becomes durable intelligence only when its learning is incorporated and projected.",
            "child": "Future Naya can use the resulting intelligence without reconstructing the originating conversation.",
            "grammar": "Make a Smart Note means create, learn, project, and prove the transaction.",
            "human": "The learning should survive the conversation and be visible as usable system intelligence.",
            "naya": "Naya must execute the canonical transaction rather than merely writing a Markdown file.",
            "machine": "Persist the note, retain the governed learning in CIS, rebuild PIS, and leave a receipt.",
            "learning": "Learning is governed improvement, not blind copying of statements.",
            "why_it_matters": "Without the learning and projection boundaries, storage can be mistaken for learning.",
            "how_to_use": "Use the transaction whenever a meaningful verified Smart Note is created.",
            "value": "Human, Naya, and the system retain one reusable intelligence unit with proof.",
            "evidence": ["E2E_TEST:canonical-smart-note-transaction", "PIS-3.0 builder output"],
            "current_state": "The transaction path is exercised in an isolated repository-shaped fixture.",
            "next_action": "Use the canonical transaction for the next real governed Smart Note.",
        }

        result = tx.execute(note)
        assert result["status"] in {"VERIFIED_TRANSACTION", "REPLAY_TRANSACTION"}
        assert result["smart_note"].exists()
        assert result["receipt"].exists()

        receipt = json.loads(result["receipt"].read_text(encoding="utf-8"))
        assert receipt["status"].endswith("TRANSACTION")
        assert receipt["cis"]["status"] in {"CREATED", "REPLAY"}
        smart_note_id = receipt["smart_note_id"]

        cis = json.loads(tx.CIS_PATH.read_text(encoding="utf-8"))
        assert any(row["smart_note_id"] == smart_note_id for row in cis["learning"])

        pis = json.loads(tx.PIS_PATH.read_text(encoding="utf-8"))
        event = next(row for row in pis["events"] if row["event_id"] == smart_note_id)
        assert event["source"]["type"] == "smart_note"
        assert event["lesson"]["retained"] is True
        assert event["action"]["text"] == note["next_action"]

        # Cold-Naya proof: read only the durable PIS projection and recover the
        # newly learned lesson + action without the originating note or chat.
        cold_view = {
            "event_id": event["event_id"],
            "lesson": event["lesson"]["text"],
            "next_action": event["action"]["text"],
            "source": event["context"]["canonical_path"],
        }
        assert cold_view["lesson"] == note["learning"]
        assert cold_view["next_action"] == note["next_action"]

        print("SMART_NOTE_E2E=PASS")
        print(f"SMART_NOTE_ID={smart_note_id}")
        print("CIS_LEARNING=PASS")
        print("PIS_PROJECTION=PASS")
        print(f"HUB_SOURCE={tx.PIS_PATH}")
        print("COLD_NAYA_RECOVERY=PASS")


if __name__ == "__main__":
    main()
