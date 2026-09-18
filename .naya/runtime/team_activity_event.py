#!/usr/bin/env python3
"""Canonical Team Naya communication events.

Execution receipts record completed governed work. This module records the
team's operational communication layer: sign-in, inspection, discovery,
decision, block/recovery, learning, handoff, and continuation. It uses the
same canonical event store as execution so communication is durable,
idempotent, indexed, and visible to the Activity projection pipeline.
"""
from __future__ import annotations

import hashlib
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parents[2]
EVENTS_ROOT = ROOT / ".naya" / "memory" / "events"
INDEX_PATH = EVENTS_ROOT / "INDEX.json"
EVENT_TYPE = "team-communication"
ALLOWED_INTENTS = {
    "NAYA_SIGNED_IN", "NAYA_INSPECTED", "NAYA_QUESTION", "NAYA_DISCOVERY",
    "NAYA_DECISION", "NAYA_CHANGED", "NAYA_TESTED", "NAYA_VERIFIED",
    "NAYA_BLOCKED", "NAYA_RECOVERED", "NAYA_LEARNED", "NAYA_HANDOFF",
    "NAYA_COMPLETED", "NAYA_CONTINUING",
}


def _stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def _event_id(intent: str, actor_id: str, session_id: str, effective_at: str) -> str:
    digest = hashlib.sha1(f"{intent}|{actor_id}|{session_id}|{effective_at}".encode("utf-8")).hexdigest()[:8]
    stamp = datetime.fromisoformat(effective_at.replace("Z", "+00:00"))
    token = re.sub(r"[^a-z0-9-]+", "-", intent.lower()).strip("-")
    return f"SE-{stamp:%Y%m%d-%H%M%S}-team-{token}-{digest}"


def build_team_activity_event(*, intent: str, actor_id: str, session_id: str, mission: str, message: str, next_action: str, successor: Optional[str] = None, effective_at: Optional[str] = None, recipients: Optional[list[str]] = None, evidence: Optional[list[str]] = None) -> dict[str, Any]:
    if intent not in ALLOWED_INTENTS:
        raise ValueError(f"unsupported Team Naya communication intent: {intent}")
    if not actor_id or not session_id or not mission or not message or not next_action:
        raise ValueError("actor_id, session_id, mission, message, and next_action are required")
    effective = effective_at or _stamp()
    event_id = _event_id(intent, actor_id, session_id, effective)
    continuity = {"next_action": next_action, "handoff_ready": intent in {"NAYA_HANDOFF", "NAYA_COMPLETED", "NAYA_CONTINUING"}}
    if successor:
        continuity["successor"] = successor
    return {
        "event_id": event_id,
        "created_at": _stamp(),
        "effective_at": effective,
        "event_type": EVENT_TYPE,
        "type": EVENT_TYPE,
        "status": "RECORDED",
        "subject": f"{intent}: {actor_id}",
        "title": f"{intent}: {actor_id}",
        "tags": ["team-communication", intent.lower()],
        "source": {"kind": "naya-session", "event_id": f"TEAM-{actor_id}-{session_id}-{intent}", "generator": "team_activity_event.build_team_activity_event"},
        "team": {"intent": intent, "actor_id": actor_id, "session_id": session_id, "recipients": recipients or ["TEAM-NAYA"], "mission": mission, "message": message},
        "continuity": continuity,
        "evidence_ids": evidence or [],
        "activity_feed_projection": {"feed": "NAYA-ACTIVITY", "event_id": event_id, "title": f"{intent}: {actor_id}", "summary": message},
    }


def emit_team_activity(*, intent: str, actor_id: str, session_id: str, mission: str, message: str, next_action: str, successor: Optional[str] = None, effective_at: Optional[str] = None, recipients: Optional[list[str]] = None, evidence: Optional[list[str]] = None, events_root: Optional[Path] = None, index_path: Optional[Path] = None) -> dict[str, Any]:
    from canonical_event_store import create_or_replay
    root = Path(events_root) if events_root else EVENTS_ROOT
    index = Path(index_path) if index_path else root / "INDEX.json"
    event = build_team_activity_event(intent=intent, actor_id=actor_id, session_id=session_id, mission=mission, message=message, next_action=next_action, successor=successor, effective_at=effective_at, recipients=recipients, evidence=evidence)
    result = create_or_replay(event, root, index)
    if result.get("status") not in {"CREATED", "REPLAY"}:
        raise ValueError(f"Team Naya communication event was not persisted: {result}")
    return {"status": result["status"], "event_id": event["event_id"], "event": event, "persist": result}


__all__ = ["ALLOWED_INTENTS", "EVENT_TYPE", "EVENTS_ROOT", "INDEX_PATH", "build_team_activity_event", "emit_team_activity"]
