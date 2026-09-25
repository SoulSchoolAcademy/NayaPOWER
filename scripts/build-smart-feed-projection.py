#!/usr/bin/env python3
"""Build the Primary Intelligence System feed consumed by the Intelligent Hub.

Sources:
- legacy/canonical SMART FEED CONTENT
- canonical .naya/memory/notes Smart Note calendar
- optional in-transaction Smart Note objects

The output is a projection, not a competing source of truth.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
SMART_NOTES_ROOT = ROOT / ".naya" / "memory" / "smart-notes"
OUT = ROOT / "NAYANET" / "HUB" / "public" / "intelligence" / "pis-feed.json"

def clean(s: str) -> str:
    s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)
    s = re.sub(r"`([^`]+)`", r"\1", s)
    return re.sub(r"\n{3,}", "\n\n", s).strip()


def parse_canonical_note(path: Path, root: Path = ROOT) -> dict[str, Any] | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("# SMART NOTE"):
        return None
    headings = list(HEADING_RE.finditer(text))
    sec: dict[str, str] = {}
    for i, match in enumerate(headings):
        end = headings[i + 1].start() if i + 1 < len(headings) else len(text)
        sec[clean(match.group(1)).upper()] = clean(text[match.end():end])
    meta = {m.group(1).strip().lower(): clean(m.group(2)) for m in META_RE.finditer(text)}
    registry_path = root / ".naya" / "memory" / "smart-notes" / "REGISTRY.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    rel_from_root = str(path.relative_to(root)).replace("\\", "/")
    entry = next((e for e in registry.get("entries", []) if str(e.get("path", "")).lstrip("./") == rel_from_root.lstrip("./")), None)
    if not entry:
        return None
    eid = str(entry.get("source_event_id") or "").strip()
    ib_id = str(entry.get("intelligent_block_id") or "").strip()
    if not eid or not ib_id:
        return None
    eid_source = "registry.source_event_id"
    rel = str(path.relative_to(root)).replace("\\", "/")
    topic = text.splitlines()[0].replace("# SMART NOTE —", "").replace("# SMART NOTE -", "").strip()
    timestamp = meta.get("timestamp", when())
    evidence = [re.sub(r"^-\s*", "", x).strip() for x in sec.get("EVIDENCE / SMART LINKS", "").splitlines() if x.strip().startswith("-")]
    return {"event_id": eid, "user_id": "canonical", "created_at": timestamp, "updated_at": timestamp, "source": {"type": "smart_note", "id": eid, "label": topic}, "human_input": {"raw": sec.get("HUMAN NOTE", sec.get("IN A NUTSHELL", "")), "captured_at": timestamp}, "context": {"topic": topic, "tags": ["canonical", "smart-note", "naya-language"], "canonical_path": rel, "intelligent_block_id": ib_id}, "naya_interpretation": {"observation": sec.get("IN A NUTSHELL", ""), "interpretation": sec.get("NAYA NOTE", ""), "recommendation": sec.get("HOW TO USE IT", ""), "uncertainty": "Projection is derived from the canonical Smart Note; truth status remains governed by its evidence."}, "machine_evidence": {"items": evidence + [f"CANONICAL_SMART_NOTE:{rel}", f"EID_SOURCE:{eid_source}", f"INTELLIGENT_BLOCK_ID:{ib_id}"], "verification_state": "RECORDED"}, "weaver_synthesis": {"summary": sec.get("WHY IT MATTERS", topic), "relationships": []}, "lesson": {"text": sec.get("LEARNING LESSON / ADAPTIVE LEARNING", ""), "retained": True}, "meaning": {"text": sec.get("WHY IT MATTERS", ""), "significance": sec.get("WHY IT MATTERS", "")}, "action": {"text": sec.get("ONE NEXT ACTION", ""), "status": "canonical"}, "whats_in_it_for_you": sec.get("WHAT'S IN IT FOR ME / YOU / US", ""), "relationships": {"event_ids": [], "connection_ids": [], "space_ids": []}, "privacy": {"visibility": "private", "consent_state": "not_granted"}, "trust": {"level": "recorded", "evidence_ids": evidence}, "status": meta.get("status", "CANONICAL"), "perspectives": [{"label": "HUMAN", "body": sec.get("HUMAN NOTE", ""), "tone": "human"}, {"label": "CHILD", "body": sec.get("CHILD / DERIVED NOTE", ""), "tone": "child"}, {"label": "GRAMMAR", "body": sec.get("GRAMMAR NOTE", ""), "tone": "machine"}, {"label": "NAYA", "body": sec.get("NAYA NOTE", ""), "tone": "naya"}, {"label": "MACHINE", "body": sec.get("MACHINE NOTE", ""), "tone": "machine"}, {"label": "LEARNING", "body": sec.get("LEARNING LESSON / ADAPTIVE LEARNING", ""), "tone": "learning"}], "pis": {"source_ref": rel, "projection_version": "3.0", "timestamp_precision": "canonical-smart-note"}}


def canonical_note_events(root: Path = SMART_NOTES_ROOT, repository_root: Path = ROOT) -> list[dict[str, Any]]:
    if not root.exists():
        return []
    events = []
    for path in sorted(root.rglob("*.md")):
        event = parse_canonical_note(path, repository_root)
        if event:
            events.append(event)
    return events


def build_projection(*, extra_notes: Iterable[dict[str, Any]] | None = None, source_root: Path = ROOT, output: Path = OUT) -> dict[str, Any]:
    """Project only canonical Smart Note / IB projections into the Hub feed.

    This is a read-only projection. It does not create Smart Notes, allocate IBs,
    or consult legacy Smart Note namespaces.
    """
    source_root = Path(source_root)
    notes = canonical_note_events(source_root / ".naya" / "memory" / "smart-notes", source_root)
    merged: dict[str, dict[str, Any]] = {e["event_id"]: e for e in notes}
    for event in list(extra_notes or []):
        merged[event["event_id"]] = event
    events = sorted(merged.values(), key=lambda e: (e.get("created_at", ""), e["event_id"]), reverse=True)
    payload = {
        "schema_version": "PIS-3.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "github:canonical-smart-notes",
        "event_count": len(events),
        "events": events,
    }
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"status": "REBUILT", "event_count": len(events), "output": str(output), "events": events}


def main() -> None:
    result = build_projection()
    print(f"PIS_FEED_BUILT events={result['event_count']} source=canonical-smart-notes+smart-feed")


if __name__ == "__main__":
    main()
