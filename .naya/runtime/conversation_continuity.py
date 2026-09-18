#!/usr/bin/env python3
"""One canonical conversation -> intelligence continuity adapter.

This is the missing thin vertical slice between a meaningful live conversation
and the existing NayaPOWER Note Event / Activity / Smart Note / restore
machinery. It does not create a second memory system.

Flow:
CONVERSATION
  -> canonical Note Event
  -> NAYAPOWER Activity projection
  -> Smart Note representations
  -> authorized retrieval
  -> independent successor continuation

The adapter is provider-neutral. A host may supply conversation text, a future
Hub UI may call it, and a test harness can call it without an LLM dependency.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
MEMORY = ROOT / ".naya" / "memory"
EVENTS = MEMORY / "events"
INDEX = EVENTS / "INDEX.json"
NEXT_EXECUTION = ".naya/handoffs/NEXT-EXECUTION-20260918-HUB-COMPOUNDING-INTELLIGENCE-VERTICAL-SLICE.md"

sys.path.insert(0, str(ROOT / ".naya" / "runtime"))
sys.path.insert(0, str(MEMORY))

from canonical_event_store import create_or_replay
from calendar_projection import project_event
from project_execution_contract import consume_next_execution
import smart_notes_v3 as brain


EVENT_RE = re.compile(r"^SE-[0-9]{8}-[0-9]{6}-[a-z0-9-]+$")


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", str(value).lower()).strip("-")[:60] or "conversation"


def _event_id(effective_at: str, title: str) -> str:
    dt = datetime.fromisoformat(effective_at.replace("Z", "+00:00"))
    return f"SE-{dt:%Y%m%d-%H%M%S}-smart-note-{_slug(title)}"


def _note_id(effective_at: str, title: str, lane: str) -> str:
    dt = datetime.fromisoformat(effective_at.replace("Z", "+00:00"))
    return f"SN-{dt:%Y%m%d-%H%M%S}-{_slug(title)}-{lane}"


def build_conversation_event(
    *,
    title: str,
    summary: str,
    what_happened: str,
    what_we_learned: list[str],
    what_changed: list[str],
    next_action: str,
    effective_at: str,
    source_event_id: str,
    project: dict[str, Any],
    actor_id: str = "NAYA-CONVERSATION-ADAPTER",
    scope: str = "NAYAPOWER",
    principal_id: str = "NAYA-FRESH-VERTICAL-TEST",
) -> dict[str, Any]:
    """Build the single authoritative Note Event for a durable conversation."""
    event_id = _event_id(effective_at, title)
    next_exec = consume_next_execution(NEXT_EXECUTION)
    next_exec_path = NEXT_EXECUTION

    representations = {
        "shawn": {
            "id": _note_id(effective_at, title, "shawn"),
            "canonical_event_id": event_id,
            "representation": "SHAWN",
            "summary": summary,
            "content": what_happened,
            "lessons": what_we_learned,
            "what_changed": what_changed,
            "next_best_actions": [next_action],
            "smart_link": f"repo://NayaPOWER/.naya/memory/events/{event_id}.json",
        },
        "naya": {
            "id": _note_id(effective_at, title, "naya"),
            "canonical_event_id": event_id,
            "representation": "NAYA",
            "summary": summary,
            "content": what_happened,
            "lessons": what_we_learned,
            "what_changed": what_changed,
            "next_best_actions": [next_action],
            "smart_link": f"repo://NayaPOWER/.naya/memory/events/{event_id}.json",
        },
        "machine": {
            "id": _note_id(effective_at, title, "machine"),
            "canonical_event_id": event_id,
            "representation": "MACHINE",
            "summary": summary,
            "content": json.dumps({
                "what_happened": what_happened,
                "what_we_learned": what_we_learned,
                "what_changed": what_changed,
                "next_action": next_action,
            }, ensure_ascii=False, sort_keys=True),
            "lessons": what_we_learned,
            "what_changed": what_changed,
            "next_best_actions": [next_action],
            "smart_link": f"repo://NayaPOWER/.naya/memory/events/{event_id}.json",
        },
    }

    return {
        "event_id": event_id,
        "idempotency_key": f"conversation:{source_event_id}",
        "created_at": effective_at,
        "effective_at": effective_at,
        "event_type": "smart-note",
        "type": "smart-note",
        "status": "CANONICAL",
        "project": project["project_name"],
        "project_context": {
            "project_id": project["project_id"],
            "current_daily_project": project["project_name"],
            "project_name": project["project_name"],
            "current_objective": project["current_objective"],
        },
        "title": title,
        "subject": title,
        "summary": summary,
        "tags": ["smart-note", "conversation", "CIS", "continuity", "hub"],
        "aliases": ["conversation intelligence", "compounding intelligence", "fresh naya continuation"],
        "concepts": ["conversation", "canonical event", "activity", "smart note", "retrieval", "continuation"],
        "source": {
            "kind": "live-conversation",
            "event_id": source_event_id,
            "generator": "conversation_continuity.build_conversation_event",
        },
        "representations": representations,
        "learning": {
            "status": "CAPTURED",
            "lessons": what_we_learned,
        },
        "relationships": {
            "source_events": [source_event_id],
            "related": [],
            "depends_on": [],
            "supersedes": None,
            "superseded_by": None,
        },
        "permissions": {
            "access": "PRIVATE",
            "scope": scope,
            "grants": [principal_id],
        },
        "continuity": {
            "execution_state": "CAPTURED",
            "learning_status": "CAPTURED",
            "handoff": {
                "next_action": next_action,
                "successor": "NEXT-NAYA",
            },
            "next_execution_path": next_exec_path,
        },
        "next_execution": {
            "path": next_exec_path,
            "next_action": next_exec["next_action"],
            "success_criteria": next_exec["success_criteria"],
            "verification_requirements": next_exec["verification_requirements"],
        },
        "verification": {
            "status": "PERSISTENCE_PENDING_RUNTIME_OBSERVATION",
            "method": "conversation-continuity-adapter",
            "evidence": ["Canonical event will be written through create_or_replay."],
        },
        "activity_feed_projection": {
            "feed": "NAYAPOWER-ACTIVITY",
            "title": title,
            "summary": summary,
        },
        "evidence_ids": [],
        "actor_id": actor_id,
    }


def capture_conversation(**kwargs: Any) -> dict[str, Any]:
    project_path = MEMORY / "projects" / "CURRENT-DAILY-PROJECT.json"
    project = json.loads(project_path.read_text(encoding="utf-8"))
    event = build_conversation_event(project=project, **kwargs)
    result = create_or_replay(event, EVENTS, INDEX)
    if result.get("status") not in {"CREATED", "REPLAY"}:
        raise RuntimeError(f"canonical conversation capture failed: {result}")
    projection = project_event(event)
    return {
        "status": result["status"],
        "event_id": event["event_id"],
        "canonical_event": result,
        "activity_projection": projection,
        "smart_note_ids": [rep["id"] for rep in event["representations"].values()],
        "next_execution": event["next_execution"],
    }


def fresh_naya_retrieve(
    query: str,
    *,
    principal_id: str = "NAYA-FRESH-VERTICAL-TEST",
    scope: str = "NAYAPOWER",
    project: str = "Naya Power Superbrain",
) -> dict[str, Any]:
    """Perform retrieval with a fresh principal and no originating conversation."""
    rows = brain.retrieve(
        query,
        limit=10,
        principal_id=principal_id,
        scope=scope,
        access_project=project,
        grants=(),
    )
    return {
        "query": query,
        "principal_id": principal_id,
        "result_count": len(rows),
        "results": [
            {
                "score": score,
                "event_id": event.get("event_id"),
                "title": event.get("title") or event.get("subject"),
                "next_action": (event.get("continuity") or {}).get("handoff", {}).get("next_action"),
            }
            for score, event in rows
        ],
    }


def verify_successor(event_id: str, query: str) -> dict[str, Any]:
    """Verify that a fresh retrieval can recover the exact successor action."""
    event_path = next(EVENTS.rglob(f"{event_id}.json"), None)
    if event_path is None:
        raise FileNotFoundError(f"canonical event not found: {event_id}")
    event = json.loads(event_path.read_text(encoding="utf-8"))
    retrieval = fresh_naya_retrieve(query)
    matched = next((row for row in retrieval["results"] if row["event_id"] == event_id), None)
    if matched is None:
        raise RuntimeError("fresh Naya retrieval did not recover the canonical event")
    expected = (event.get("continuity") or {}).get("handoff", {}).get("next_action")
    if matched.get("next_action") != expected:
        raise RuntimeError("fresh Naya recovered the event but not the exact successor action")
    return {
        "status": "VERIFIED",
        "event_id": event_id,
        "retrieval": retrieval,
        "continuation": {
            "next_action": expected,
            "successor": (event.get("continuity") or {}).get("handoff", {}).get("successor"),
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="command", required=True)
    c = sub.add_parser("capture")
    c.add_argument("--title", required=True)
    c.add_argument("--summary", required=True)
    c.add_argument("--what-happened", required=True)
    c.add_argument("--lesson", action="append", required=True)
    c.add_argument("--change", action="append", default=[])
    c.add_argument("--next-action", required=True)
    c.add_argument("--effective-at", required=True)
    c.add_argument("--source-event-id", required=True)
    v = sub.add_parser("verify")
    v.add_argument("--event-id", required=True)
    v.add_argument("--query", required=True)
    a = ap.parse_args()

    if a.command == "capture":
        print(json.dumps(capture_conversation(
            title=a.title,
            summary=a.summary,
            what_happened=a.what_happened,
            what_we_learned=a.lesson,
            what_changed=a.change,
            next_action=a.next_action,
            effective_at=a.effective_at,
            source_event_id=a.source_event_id,
        ), indent=2, ensure_ascii=False))
        return 0

    print(json.dumps(verify_successor(a.event_id, a.query), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
