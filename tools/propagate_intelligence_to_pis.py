#!/usr/bin/env python3
"""Propagate canonical Intelligence Events into the NayaPOWER PIS.

PIS authority is the Smart Notes runtime consumed by .naya/runtime/restore_context.py.
This is deliberately a separate transition from event creation/promotion: writing a
note is not itself proof that propagation occurred. The operation is deterministic,
idempotent, and refuses to overwrite a conflicting canonical note.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVENT_DIR = ROOT / "MASTER-NOTES" / "INTELLIGENCE-EVENTS"
PIS_DIR = ROOT / ".naya" / "memory" / "notes"
INDEX_PATH = ROOT / ".naya" / "memory" / "INDEX.json"

EVENT_ID_RE = re.compile(r"^SE-([0-9]{8})-([0-9]{6})-(.+)$")


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def note_id(event: dict) -> str:
    event_id = str(event["event_id"])
    match = EVENT_ID_RE.match(event_id)
    if match:
        return f"SN-{match.group(1)}-{match.group(2)}-{match.group(3)}"
    stamp = datetime.fromisoformat(str(event["timestamp"]).replace("Z", "+00:00")).astimezone(timezone.utc)
    slug = re.sub(r"[^a-z0-9-]+", "-", event_id.lower()).strip("-")[:48]
    return f"SN-{stamp:%Y%m%d}-{stamp:%H%M%S}-{slug or 'intelligence-event'}"


def build_note(event: dict, event_path: Path) -> dict:
    nid = note_id(event)
    timestamp = datetime.fromisoformat(str(event["timestamp"]).replace("Z", "+00:00")).isoformat()
    naya_path = f"MASTER-NOTES/NAYA-NOTES/{event['event_id']}.md"
    feed_path = f"MASTER-NOTES/INTELLIGENCE-FEED/{event['event_id']}.md"
    return {
        "id": nid,
        "event_id": event["event_id"],
        "representation": "NAYA",
        "type": "lesson",
        "title": event.get("title") or f"Naya intelligence: {event['project']}",
        "status": "ACTIVE",
        "created_at": timestamp,
        "effective_at": timestamp,
        "superseded_at": None,
        "source": {
            "kind": "canonical-intelligence-event",
            "path": display_path(event_path),
            "commit": None,
            "conversation_ref": None,
        },
        "summary": str(event["lesson"]),
        "what_happened": str(event.get("what_happened", "")),
        "what_we_learned": [str(event["lesson"])],
        "why_it_matters": str(event.get("value", "")),
        "what_changed": [str(event.get("actual_outcome", ""))],
        "next_best_action": str(event.get("next_action", "")),
        "content": (
            f"NAYA NOTE\n\n{event.get('lesson','')}\n\n"
            f"Naya representation: `{naya_path}`\n"
            f"Running Feed representation: `{feed_path}`\n"
        ),
        "tags": ["pis", "intelligence-event", str(event["project"]).lower().replace(" ", "-")],
        "aliases": [str(event.get("title", ""))] if event.get("title") else [],
        "relationships": {
            "related": [],
            "depends_on": [],
            "same_event": event["event_id"],
            "source_events": [event["event_id"]],
        },
        "verification": {
            "status": "PENDING",
            "verified_at": None,
            "evidence": ["PIS propagation artifact written by propagate_intelligence_to_pis.py"],
            "canonical_url": None,
            "receipt_url": None,
            "feed_posted": (ROOT / feed_path).exists(),
        },
        "confidence": "HIGH" if event.get("evidence_state") in {"VERIFIED", "RUNTIME-PROVEN", "PRODUCTION-PROVEN"} else "MEDIUM",
        "evidence": list(event.get("evidence", [])),
    }


def update_index(note_ids: list[str], event_map: dict[str, str]) -> None:
    index = load(INDEX_PATH)
    notes = list(index.get("notes", []))
    for nid in note_ids:
        if nid not in notes:
            notes.append(nid)
    index["notes"] = notes
    event_index = dict(index.get("event_index", {}))
    event_index.update(event_map)
    index["event_index"] = event_index
    index["generated_at"] = datetime.now(timezone.utc).isoformat()
    INDEX_PATH.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    if not EVENT_DIR.exists():
        print("PIS propagation: no Intelligence Event directory")
        return 0
    PIS_DIR.mkdir(parents=True, exist_ok=True)
    created = 0
    existing = 0
    note_ids: list[str] = []
    event_map: dict[str, str] = {}

    for event_path in sorted(EVENT_DIR.glob("*.json")):
        event = load(event_path)
        if not event.get("event_id") or not event.get("lesson"):
            continue
        nid = note_id(event)
        target = PIS_DIR / f"{nid}.json"
        note = build_note(event, event_path)
        if target.exists():
            current = load(target)
            if current != note:
                raise SystemExit(f"PIS CONFLICT: {display_path(target)} already exists with different content")
            existing += 1
        else:
            target.write_text(json.dumps(note, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            created += 1
        note_ids.append(nid)
        event_map[event["event_id"]] = nid

    if note_ids:
        update_index(note_ids, event_map)
    print(f"PIS propagation: created={created} existing={existing} total={len(note_ids)}")
    print("PIS_PROPAGATION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
