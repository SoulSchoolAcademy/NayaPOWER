#!/usr/bin/env python3
"""Narrow Activity Event -> Intelligence Event adapter.

This adapter performs no learning inference. A completed Activity Event is
eligible for semantic promotion only when an explicit non-empty lesson is
supplied by the caller. Existing Intelligence Event validation/promotion
machinery remains unchanged.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
INTELLIGENCE_DIR = ROOT / "MASTER-NOTES" / "INTELLIGENCE-EVENTS"


def _require_explicit_lesson(learning: Any) -> str:
    if not isinstance(learning, dict):
        raise ValueError("Activity -> Intelligence promotion refused: explicit learning payload is required")
    lesson = learning.get("lesson")
    if not isinstance(lesson, str) or not lesson.strip():
        raise ValueError("Activity -> Intelligence promotion refused: explicit non-empty lesson is required")
    return lesson.strip()


def build_intelligence_event(
    activity_event: dict[str, Any],
    learning: dict[str, Any],
) -> dict[str, Any]:
    """Build one existing-contract Intelligence Event from verified Activity.

    All provenance/evidence fields come from the canonical Activity Event.
    Learning semantics come only from the explicit learning payload.
    """
    lesson = _require_explicit_lesson(learning)

    event_id = activity_event.get("event_id")
    if not isinstance(event_id, str) or not event_id.strip():
        raise ValueError("Activity -> Intelligence promotion refused: Activity event_id is required")

    verification = activity_event.get("verification")
    if not isinstance(verification, dict) or verification.get("status") != "VERIFIED":
        raise ValueError("Activity -> Intelligence promotion refused: Activity verification is not VERIFIED")

    continuity = activity_event.get("continuity")
    if not isinstance(continuity, dict) or continuity.get("execution_state") != "COMPLETED":
        raise ValueError("Activity -> Intelligence promotion refused: Activity execution is not COMPLETED")

    evidence = activity_event.get("evidence_ids")
    if not isinstance(evidence, list) or not evidence:
        raise ValueError("Activity -> Intelligence promotion refused: Activity evidence_ids are required")

    timestamp = activity_event.get("effective_at") or activity_event.get("created_at")
    if not isinstance(timestamp, str) or not timestamp.strip():
        raise ValueError("Activity -> Intelligence promotion refused: Activity timestamp is required")

    source = [
        f"activity_event:{event_id}",
        f"execution:{(activity_event.get('execution') or {}).get('event_id', '')}",
    ]
    source = [item for item in source if item.rsplit(":", 1)[-1]]

    event: dict[str, Any] = {
        "event_id": f"INT-{event_id}",
        "timestamp": timestamp,
        "project": ROOT.name,
        "title": learning.get("title") or activity_event.get("subject") or event_id,
        "what_happened": activity_event.get("summary", ""),
        "lesson": lesson,
        "source": source,
        "evidence": list(evidence),
        "evidence_state": "VERIFIED",
        "promotion_status": "PROPOSED",
    }

    # These fields are semantic inputs only when explicitly supplied.
    for key in (
        "intended_outcome",
        "actual_outcome",
        "value",
        "recommendation",
        "root_cause",
        "successor_instruction",
    ):
        value = learning.get(key)
        if value not in (None, ""):
            event[key] = value

    next_action = learning.get("next_action")
    if next_action not in (None, ""):
        event["next_action"] = next_action
    else:
        handoff = continuity.get("handoff")
        if isinstance(handoff, dict) and handoff.get("next_action"):
            event["next_action"] = handoff["next_action"]

    return event


def persist_intelligence_event(event: dict[str, Any], intelligence_dir: Path | None = None) -> Path:
    """Persist only the canonical Intelligence Event; never overwrite conflicts."""
    target_dir = Path(intelligence_dir) if intelligence_dir else INTELLIGENCE_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    path = target_dir / f"{event['event_id']}.json"
    payload = json.dumps(event, indent=2, ensure_ascii=False) + "\n"

    if path.exists():
        existing = path.read_text(encoding="utf-8")
        if existing != payload:
            raise ValueError(
                f"Activity -> Intelligence promotion refused: existing Intelligence Event conflicts at {path}"
            )
        return path

    path.write_text(payload, encoding="utf-8")
    return path


def promote_activity_event(
    activity_event: dict[str, Any],
    learning: dict[str, Any] | None,
    intelligence_dir: Path | None = None,
) -> Path | None:
    """Convert a verified Activity Event only when explicit learning exists.

    Missing/invalid learning is a fail-closed no-promotion result for callers
    that treat learning as optional execution metadata.
    """
    if learning is None:
        return None
    event = build_intelligence_event(activity_event, learning)
    return persist_intelligence_event(event, intelligence_dir=intelligence_dir)
