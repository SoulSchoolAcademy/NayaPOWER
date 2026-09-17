#!/usr/bin/env python3
"""Canonical Activity Feed event record for Universal Team-Naya Activity Reporting (P0-01).

A governed execution is completely recorded only through one canonical Activity
event: persisted here through the canonical event store, verified by the
execution controller at VERIFIED, and re-verified by the controller's validate()
so a later suppression or tamper is an integrity failure.
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parents[2]
EVENTS_ROOT = ROOT / ".naya" / "memory" / "events"
INDEX_PATH = EVENTS_ROOT / "INDEX.json"

EVENT_TYPE = "activity"


def _stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_activity_event(
    *,
    event_id: str,
    claim_id: str,
    action_id: str,
    decision_id: str,
    authority_id: str,
    actor_id: str,
    subject: str,
    summary: str,
    receipt_id: str,
    next_action: str,
    successor: str,
    evidence: list[str],
    verification_method: str = "human-naya-verification",
    verification_schema: str = "naya-power-evidence/v1",
    run_id: Optional[str] = None,
    session_id: Optional[str] = None,
    effective_at: Optional[str] = None,
) -> dict[str, Any]:
    stamp = _stamp()
    effective = effective_at or stamp
    execution: dict[str, Any] = {
        "event_id": event_id,
        "claim_id": claim_id,
        "action_id": action_id,
        "decision_id": decision_id,
        "authority_id": authority_id,
        "actor_id": actor_id,
        "run_id": run_id,
    }
    if session_id:
        execution["session_id"] = session_id
    return {
        "event_id": event_id,
        "created_at": stamp,
        "effective_at": effective,
        "event_type": EVENT_TYPE,
        "status": "VERIFIED_REPOSITORY_RECORD",
        "subject": subject,
        "title": subject,
        "tags": [EVENT_TYPE],
        "source": {
            "kind": "execution",
            "event_id": f"EXECUTION-{claim_id}",
            "generator": "activity_event.build_activity_event",
        },
        "execution": execution,
        "receipt": {
            "receipt_id": receipt_id,
            "schema": verification_schema,
            "status": "MATCHED",
            "event_id": event_id,
        },
        "continuity": {
            "execution_state": "COMPLETED",
            "handoff": {
                "next_action": next_action,
                "successor": successor,
            },
            "learning_status": "RECORDED",
        },
        "activity_feed_projection": {
            "feed": "NAYA-ACTIVITY",
            "event_id": event_id,
            "title": subject,
            "summary": summary,
        },
        "verification": {
            "status": "VERIFIED",
            "method": verification_method,
            "schema": verification_schema,
            "evidence": evidence,
        },
        "evidence_ids": evidence,
    }


def persist_activity_event(
    event: dict[str, Any],
    *,
    events_root: Optional[Path] = None,
    index_path: Optional[Path] = None,
) -> dict[str, Any]:
    from canonical_event_store import create_or_replay

    return create_or_replay(
        event,
        Path(events_root) if events_root else EVENTS_ROOT,
        Path(index_path) if index_path else INDEX_PATH,
    )


def find_event(
    event_id: str,
    *,
    events_root: Optional[Path] = None,
    index_path: Optional[Path] = None,
) -> Optional[dict[str, Any]]:
    root = Path(events_root) if events_root else EVENTS_ROOT
    index = Path(index_path) if index_path else INDEX_PATH
    if index.exists():
        rows: list[dict[str, Any]] = []
        try:
            rows = json.loads(index.read_text(encoding="utf-8")).get("events", [])
        except Exception:
            rows = []
        for row in rows:
            if row.get("event_id") == event_id:
                candidate = root / str(row.get("path", ""))
                if candidate.exists():
                    try:
                        return json.loads(candidate.read_text(encoding="utf-8"))
                    except Exception:
                        return None
    for candidate in root.rglob(f"{event_id}.json"):
        try:
            return json.loads(candidate.read_text(encoding="utf-8"))
        except Exception:
            continue
    return None


def _binds_execution(body: dict[str, Any], *, claim_id: str, action_id: str, run_id: Optional[str]) -> bool:
    execution = body.get("execution")
    if not isinstance(execution, dict):
        return False
    if execution.get("claim_id") != claim_id:
        return False
    if execution.get("action_id") != action_id:
        return False
    if run_id and execution.get("run_id") != run_id:
        return False
    return True


def find_activity_event_by_execution(
    *,
    claim_id: str,
    action_id: str,
    run_id: Optional[str] = None,
    events_root: Optional[Path] = None,
    index_path: Optional[Path] = None,
) -> Optional[dict[str, Any]]:
    """Return the canonical Activity event durably bound to this execution, if any.

    Binding is by claim/action/run so a NEW run of the same claim can never be
    silently attached to an old completion record (no stale reuse), while a
    retry/resume of the SAME run finds and reuses its event (no duplicate).
    """
    root = Path(events_root) if events_root else EVENTS_ROOT
    index = Path(index_path) if index_path else INDEX_PATH
    if index.exists():
        rows: list[dict[str, Any]] = []
        try:
            rows = json.loads(index.read_text(encoding="utf-8")).get("events", [])
        except Exception:
            rows = []
        for row in rows:
            if str(row.get("type", "")).lower() != EVENT_TYPE:
                continue
            candidate = root / str(row.get("path", ""))
            if not candidate.exists():
                continue
            try:
                body = json.loads(candidate.read_text(encoding="utf-8"))
            except Exception:
                continue
            if _binds_execution(body, claim_id=claim_id, action_id=action_id, run_id=run_id):
                return body
    for candidate in root.rglob("SE-*.json"):
        try:
            body = json.loads(candidate.read_text(encoding="utf-8"))
        except Exception:
            continue
        if str(body.get("event_type", "")).lower() != EVENT_TYPE:
            continue
        if _binds_execution(body, claim_id=claim_id, action_id=action_id, run_id=run_id):
            return body
    return None


def _event_id_for(claim_id: str, action_id: str, run_id: Optional[str]) -> str:
    token = re.sub(r"[^a-z0-9]+", "-", f"{claim_id}-{action_id}".lower()).strip("-")
    digest = hashlib.sha1(f"{claim_id}|{action_id}|{run_id}".encode("utf-8")).hexdigest()[:6]
    stamp = datetime.now(timezone.utc)
    return f"SE-{stamp:%Y%m%d-%H%M%S}-activity-{token[:40] if token else 'execution'}-{digest}"


def ensure_activity_event(
    *,
    claim_id: str,
    action_id: str,
    decision_id: Optional[str],
    authority_id: Optional[str],
    actor_id: Optional[str],
    subject: str,
    summary: str,
    receipt_id: str,
    next_action: str,
    successor: str,
    evidence: list[str],
    run_id: Optional[str] = None,
    session_id: Optional[str] = None,
    effective_at: Optional[str] = None,
    events_root: Optional[Path] = None,
    index_path: Optional[Path] = None,
) -> dict[str, Any]:
    """Emit exactly one canonical Activity event for this execution, idempotently.

    Reuses the existing run-bound event when one is already durable (REPLAY_EVENT),
    otherwise builds and persists a new one through the canonical event store
    (create_or_replay) so the canonical index remains the single authority.
    """
    root = Path(events_root) if events_root else EVENTS_ROOT
    index = Path(index_path) if index_path else INDEX_PATH
    existing = find_activity_event_by_execution(
        claim_id=claim_id, action_id=action_id, run_id=run_id, events_root=root, index_path=index
    )
    if existing is not None:
        return {"status": "REPLAY_EVENT", "event_id": existing.get("event_id"), "event": existing, "persist": None}
    event_id = _event_id_for(claim_id, action_id, run_id)
    event = build_activity_event(
        event_id=event_id,
        claim_id=claim_id,
        action_id=action_id,
        decision_id=decision_id,
        authority_id=authority_id,
        actor_id=actor_id,
        subject=subject,
        summary=summary,
        receipt_id=receipt_id,
        next_action=next_action,
        successor=successor,
        evidence=evidence,
        run_id=run_id,
        session_id=session_id,
        effective_at=effective_at,
    )
    persisted = persist_activity_event(event, events_root=root, index_path=index)
    if persisted.get("status") == "CONFLICT":
        raise ValueError(f"conflicting existing canonical Activity event: {event_id}")
    if persisted.get("status") not in {"CREATED", "REPLAY"}:
        raise ValueError(f"failed to persist canonical Activity event: {event_id}")
    return {"status": persisted.get("status"), "event_id": event_id, "event": event, "persist": persisted}


__all__ = [
    "build_activity_event",
    "persist_activity_event",
    "find_event",
    "find_activity_event_by_execution",
    "ensure_activity_event",
    "EVENT_TYPE",
    "EVENTS_ROOT",
    "INDEX_PATH",
]