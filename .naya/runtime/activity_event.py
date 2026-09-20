#!/usr/bin/env python3
"""Canonical Activity Feed event record for Universal Team-Naya Activity Reporting (P0-01)."""
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


def build_activity_event(*, event_id: str, claim_id: str, action_id: str, decision_id: str, authority_id: str, actor_id: str, subject: str, summary: str, receipt_id: str, next_action: str, successor: str, evidence: list[str], verification_method: str = "human-naya-verification", verification_schema: str = "naya-power-evidence/v1", run_id: Optional[str] = None, session_id: Optional[str] = None, effective_at: Optional[str] = None, compounding_measurement: Optional[dict[str, Any]] = None, learning_event_id: Optional[str] = None, retrieval_receipt_id: Optional[str] = None, retrieval_source_event_id: Optional[str] = None, retrieval_smart_note_id: Optional[str] = None) -> dict[str, Any]:
    stamp = _stamp()
    effective = effective_at or stamp
    execution: dict[str, Any] = {"event_id": event_id, "claim_id": claim_id, "action_id": action_id, "decision_id": decision_id, "authority_id": authority_id, "actor_id": actor_id, "run_id": run_id}
    if session_id:
        execution["session_id"] = session_id
    learning_lineage = {
        "learning_event_id": learning_event_id,
        "retrieval_receipt_id": retrieval_receipt_id,
        "retrieval_source_event_id": retrieval_source_event_id,
        "retrieval_smart_note_id": retrieval_smart_note_id,
    }
    if any(value is not None for value in learning_lineage.values()):
        if not all(isinstance(value, str) and value.strip() for value in learning_lineage.values()):
            raise ValueError("incomplete learning/retrieval lineage for canonical Activity event")
        execution["learning_lineage"] = learning_lineage
    receipt = {"receipt_id": receipt_id, "schema": verification_schema, "status": "MATCHED", "event_id": event_id}
    if "learning_lineage" in execution:
        receipt["learning_lineage"] = dict(execution["learning_lineage"])
    return {"event_id": event_id, "created_at": stamp, "effective_at": effective, "event_type": EVENT_TYPE, "status": "VERIFIED_REPOSITORY_RECORD", "subject": subject, "title": subject, "tags": [EVENT_TYPE], "source": {"kind": "execution", "event_id": f"EXECUTION-{claim_id}", "generator": "activity_event.build_activity_event"}, "execution": execution, "receipt": receipt, "continuity": {"execution_state": "COMPLETED", "handoff": {"next_action": next_action, "successor": successor}, "learning_status": "RECORDED"}, "activity_feed_projection": {"feed": "NAYA-ACTIVITY", "event_id": event_id, "title": subject, "summary": summary}, "verification": {"status": "VERIFIED", "method": verification_method, "schema": verification_schema, "evidence": evidence}, "evidence_ids": evidence, **({"compounding_measurement": compounding_measurement} if compounding_measurement is not None else {})}


def _project_team_activity(event: dict[str, Any], events_root: Path, index_path: Path) -> None:
    """Bridge a completed governed execution into Team Naya communication."""
    from team_activity import emit_team_activity
    execution = event.get("execution") or {}
    continuity = event.get("continuity") or {}
    handoff = continuity.get("handoff") or {}
    verification = event.get("verification") or {}
    evidence = list(event.get("evidence_ids") or verification.get("evidence") or []) + [event["event_id"]]
    emit_team_activity(intent="NAYA_VERIFIED", actor_id=execution.get("actor_id") or "NAYA-EXECUTION-CONTROLLER", session_id=execution.get("session_id") or execution.get("run_id") or event["event_id"], mission=event.get("subject") or f"Governed execution {execution.get('claim_id')}", message=event.get("subject") or "Governed execution reached VERIFIED and was projected to Team Naya Activity.", next_action=handoff.get("next_action") or "Continue from the verified execution handoff.", successor=handoff.get("successor"), recipients=["TEAM-NAYA"], evidence=evidence, events_root=events_root, index_path=index_path, effective_at=event.get("effective_at"))


def persist_activity_event(event: dict[str, Any], *, events_root: Optional[Path] = None, index_path: Optional[Path] = None) -> dict[str, Any]:
    from canonical_event_store import create_or_replay
    effective_events_root = Path(events_root) if events_root else EVENTS_ROOT
    effective_index_path = Path(index_path) if index_path else INDEX_PATH
    result = create_or_replay(event, effective_events_root, effective_index_path)
    if result.get("status") in {"CREATED", "REPLAY"}:
        _project_team_activity(event, effective_events_root, effective_index_path)
        if effective_events_root.resolve() == EVENTS_ROOT.resolve():
            from calendar_projection import project_event
            project_event(event)
    return result


def find_event(event_id: str, *, events_root: Optional[Path] = None, index_path: Optional[Path] = None) -> Optional[dict[str, Any]]:
    root = Path(events_root) if events_root else EVENTS_ROOT
    index = Path(index_path) if index_path else INDEX_PATH
    if index.exists():
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
    return execution.get("claim_id") == claim_id and execution.get("action_id") == action_id and (not run_id or execution.get("run_id") == run_id)


def find_activity_event_by_execution(*, claim_id: str, action_id: str, run_id: Optional[str] = None, events_root: Optional[Path] = None, index_path: Optional[Path] = None) -> Optional[dict[str, Any]]:
    root = Path(events_root) if events_root else EVENTS_ROOT
    index = Path(index_path) if index_path else INDEX_PATH
    if index.exists():
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
        if str(body.get("event_type", "")).lower() == EVENT_TYPE and _binds_execution(body, claim_id=claim_id, action_id=action_id, run_id=run_id):
            return body
    return None


def _event_id_for(claim_id: str, action_id: str, run_id: Optional[str]) -> str:
    token = re.sub(r"[^a-z0-9]+", "-", f"{claim_id}-{action_id}".lower()).strip("-")
    digest = hashlib.sha1(f"{claim_id}|{action_id}|{run_id}".encode("utf-8")).hexdigest()[:6]
    stamp = datetime.now(timezone.utc)
    return f"SE-{stamp:%Y%m%d-%H%M%S}-activity-{token[:40] if token else 'execution'}-{digest}"


def ensure_activity_event(*, claim_id: str, action_id: str, decision_id: Optional[str], authority_id: Optional[str], actor_id: Optional[str], subject: str, summary: str, receipt_id: str, next_action: str, successor: str, evidence: list[str], run_id: Optional[str] = None, session_id: Optional[str] = None, effective_at: Optional[str] = None, events_root: Optional[Path] = None, index_path: Optional[Path] = None, measurement_context: Optional[dict[str, Any]] = None, learning_event_id: Optional[str] = None, retrieval_receipt_id: Optional[str] = None, retrieval_source_event_id: Optional[str] = None, retrieval_smart_note_id: Optional[str] = None) -> dict[str, Any]:
    root = Path(events_root) if events_root else EVENTS_ROOT
    index = Path(index_path) if index_path else INDEX_PATH
    existing = find_activity_event_by_execution(claim_id=claim_id, action_id=action_id, run_id=run_id, events_root=root, index_path=index)
    if existing is not None:
        return {"status": "REPLAY_EVENT", "event_id": existing.get("event_id"), "event": existing, "persist": None}
    event_id = _event_id_for(claim_id, action_id, run_id)
    event = build_activity_event(event_id=event_id, claim_id=claim_id, action_id=action_id, decision_id=decision_id, authority_id=authority_id, actor_id=actor_id, subject=subject, summary=summary, receipt_id=receipt_id, next_action=next_action, successor=successor, evidence=evidence, run_id=run_id, session_id=session_id, effective_at=effective_at, learning_event_id=learning_event_id, retrieval_receipt_id=retrieval_receipt_id, retrieval_source_event_id=retrieval_source_event_id, retrieval_smart_note_id=retrieval_smart_note_id)
    if measurement_context is not None:
        from compounding_measurement import build_compounding_measurement
        measurement_execution = {
            "claim_id": claim_id,
            "action_id": action_id,
            "run_id": run_id,
        }
        event["compounding_measurement"] = build_compounding_measurement(
            event=event,
            execution={**measurement_execution, **(measurement_context.get("execution") or {})},
            evidence=evidence,
            history=measurement_context.get("history") or [],
            resource_usage=measurement_context.get("resource_usage"),
            knowledge_reuse=measurement_context.get("knowledge_reuse"),
            new_learning=measurement_context.get("new_learning"),
        )
    persisted = persist_activity_event(event, events_root=root, index_path=index)
    if persisted.get("status") == "CONFLICT":
        raise ValueError(f"conflicting existing canonical Activity event: {event_id}")
    if persisted.get("status") not in {"CREATED", "REPLAY"}:
        raise ValueError(f"failed to persist canonical Activity event: {event_id}")
    return {"status": persisted.get("status"), "event_id": event_id, "event": event, "persist": persisted}


__all__ = ["build_activity_event", "persist_activity_event", "find_event", "find_activity_event_by_execution", "ensure_activity_event", "EVENT_TYPE", "EVENTS_ROOT", "INDEX_PATH"]
