#!/usr/bin/env python3
"""Stable Team Naya communication facade with retry-safe emission."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Optional

from team_activity_event import build_team_activity_event


def _identity_key(intent: str, actor_id: str, session_id: str, mission: str, message: str, next_action: str, successor: Optional[str], recipients: list[str], evidence: list[str]) -> str:
    payload = [intent, actor_id, session_id, mission, message, next_action, successor, recipients, evidence]
    return hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest()


def _find_existing(identity_key: str, events_root: Path, index_path: Path) -> Optional[dict[str, Any]]:
    if not index_path.exists():
        return None
    payload = json.loads(index_path.read_text(encoding="utf-8"))
    for row in payload.get("events", []):
        candidate = events_root / str(row.get("path", ""))
        if not candidate.exists():
            continue
        body = json.loads(candidate.read_text(encoding="utf-8"))
        if body.get("event_type") == "team-communication" and body.get("idempotency_key") == identity_key:
            return body
    return None


def emit_team_activity(*, intent: str, actor_id: str, session_id: str, mission: str, message: str, next_action: str, successor: Optional[str] = None, effective_at: Optional[str] = None, recipients: Optional[list[str]] = None, evidence: Optional[list[str]] = None, events_root: Optional[Path] = None, index_path: Optional[Path] = None) -> dict[str, Any]:
    from canonical_event_store import create_or_replay
    root = Path(events_root) if events_root else Path(__file__).resolve().parents[2] / ".naya" / "memory" / "events"
    index = Path(index_path) if index_path else root / "INDEX.json"
    recipient_list = recipients or ["TEAM-NAYA"]
    evidence_list = evidence or []
    identity_key = _identity_key(intent, actor_id, session_id, mission, message, next_action, successor, recipient_list, evidence_list)
    existing = _find_existing(identity_key, root, index)
    if existing:
        return {"status": "REPLAY", "event_id": existing["event_id"], "event": existing, "persist": None}
    event = build_team_activity_event(intent=intent, actor_id=actor_id, session_id=session_id, mission=mission, message=message, next_action=next_action, successor=successor, effective_at=effective_at, recipients=recipient_list, evidence=evidence_list)
    event["idempotency_key"] = identity_key
    result = create_or_replay(event, root, index)
    if result.get("status") not in {"CREATED", "REPLAY"}:
        raise ValueError(f"Team Naya communication event was not persisted: {result}")
    return {"status": result["status"], "event_id": event["event_id"], "event": event, "persist": result}
