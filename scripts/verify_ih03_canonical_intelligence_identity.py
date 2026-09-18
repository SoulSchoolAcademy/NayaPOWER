#!/usr/bin/env python3
"""IH-03 focused proof: canonical event identity survives the PIS projection boundary."""
from __future__ import annotations
import json
import tempfile
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_smart_feed_projection import build_projection

EVENT = ROOT / ".naya/memory/events/2026/09/17/03/SE-20260917-030839-p001a-auto-emission-verified.json"
EXPECTED = "SE-20260917-030839-p001a-auto-emission-verified"
BOARD = ROOT / "NAYANET/HUB/src/intelligence/SmartFeedBoard.tsx"

def main() -> int:
    raw = json.loads(EVENT.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "pis-feed.json"
        payload = build_projection(output=out)
    projected = next((e for e in payload["events"] if e.get("event_id") == EXPECTED), None)
    assert projected, "IH03_CANONICAL_EVENT_MISSING_FROM_PIS"
    assert projected["event_id"] == raw["event_id"], "IH03_EVENT_ID_CHANGED"
    assert projected["created_at"] == raw["created_at"], "IH03_CREATED_AT_CHANGED"
    assert projected["updated_at"] == raw.get("updated_at", raw["created_at"]), "IH03_UPDATED_AT_CHANGED"
    assert projected["source"]["id"] == raw["source"]["event_id"], "IH03_SOURCE_ID_CHANGED"
    assert f"EVIDENCE:{raw['evidence_ids'][0]}" in projected["machine_evidence"]["items"], "IH03_EVIDENCE_LOST"
    assert projected["machine_evidence"]["verification_state"] == raw["verification"]["status"], "IH03_VERIFICATION_LOST"
    assert projected["privacy"]["visibility"] == raw.get("privacy", {}).get("visibility", "PRIVATE BY DEFAULT"), "IH03_PRIVACY_CHANGED"
    board = BOARD.read_text(encoding="utf-8")
    assert 'data-event-id={event.event_id}' in board, "IH03_BOARD_ID_BINDING_MISSING"
    print("IH-03 CANONICAL EVENT → PIS → INTELLIGENT EVENT → INTELLIGENT BLOCK")
    print(f"event_id={projected['event_id']}")
    print(f"created_at={projected['created_at']}")
    print(f"source_id={projected['source']['id']}")
    print(f"verification={projected['machine_evidence']['verification_state']}")
    print(f"privacy={projected['privacy']['visibility']} / {projected['privacy']['consent_state']}")
    print("evidence=preserved")
    print("board_identity=data-event-id(event.event_id)")
    print("PASS — stable canonical identity and required truth fields preserved")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
