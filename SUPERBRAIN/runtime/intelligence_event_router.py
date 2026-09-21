"""Canonical event-driven Naya intelligence communication primitives.

This module contains deterministic contract logic only. It does not require
GitHub Actions, cron, or a continuously running process.

The production transport may call these primitives from a webhook, database
trigger, queue consumer, serverless request, or equivalent event boundary.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import PurePosixPath
from typing import Tuple


CANONICAL_ROOT = PurePosixPath(".naya/INTELLIGENCE")


class EventType(str, Enum):
    NAYA_JOINED = "NAYA_JOINED"
    INTELLIGENCE_CREATED = "INTELLIGENCE_CREATED"
    ACTIVITY_CREATED = "ACTIVITY_CREATED"
    ACTION_TRIGGERED = "ACTION_TRIGGERED"
    ACTION_COMPLETED = "ACTION_COMPLETED"
    ACTION_BLOCKED = "ACTION_BLOCKED"
    VERIFICATION_FAILED = "VERIFICATION_FAILED"
    GOVERNANCE_CHANGED = "GOVERNANCE_CHANGED"
    HANDOFF_CREATED = "HANDOFF_CREATED"


class Visibility(str, Enum):
    PRIVATE = "PRIVATE"
    SHARED = "SHARED"
    COLLECTIVE = "COLLECTIVE"
    PUBLIC = "PUBLIC"


@dataclass(frozen=True)
class IntelligenceEvent:
    event_id: str
    event_type: EventType
    occurred_at: str
    source_naya_id: str
    source_surface: str
    mission: str
    summary: str
    why_it_matters: str
    required_awareness: bool
    authority_state: str
    evidence_state: str
    visibility: Visibility
    related_activity_id: str | None = None
    related_receipt_id: str | None = None
    caused_by: str | None = None

    def validate(self) -> None:
        if not self.event_id.strip():
            raise ValueError("event_id is required")
        if not self.source_naya_id.strip():
            raise ValueError("source_naya_id is required")
        if not self.mission.strip():
            raise ValueError("mission is required")
        if not self.summary.strip():
            raise ValueError("summary is required")
        if self.visibility == Visibility.COLLECTIVE and not self.required_awareness:
            raise ValueError("collective events must explicitly carry awareness scope")
        _parse_timestamp(self.occurred_at)


@dataclass(frozen=True)
class Briefing:
    event_id: str
    what_happened: str
    why_it_happened: str
    why_it_matters: str
    what_changed: str
    who_needs_to_know: Tuple[str, ...]
    recommendation: str
    authority_state: str
    evidence_state: str


@dataclass(frozen=True)
class DeliveryReceipt:
    event_id: str
    recipient: str
    state: str
    delivered_at: str | None = None


def _parse_timestamp(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("occurred_at must include timezone")
    return parsed.astimezone(timezone.utc)


def daily_path(occurred_at: str, filename: str) -> str:
    dt = _parse_timestamp(occurred_at)
    return str(
        CANONICAL_ROOT
        / f"{dt.year:04d}"
        / f"{dt.month:02d}"
        / f"{dt.day:02d}"
        / filename
    )


def canonical_record_paths(occurred_at: str) -> dict[str, str]:
    return {
        "smart_notes": daily_path(occurred_at, "SMART-NOTES.md"),
        "activity": daily_path(occurred_at, "ACTIVITY.md"),
        "notifications": daily_path(occurred_at, "NOTIFICATIONS.jsonl"),
        "briefings": daily_path(occurred_at, "BRIEFINGS.md"),
    }


def should_propagate(event: IntelligenceEvent) -> bool:
    event.validate()
    return event.required_awareness or event.event_type in {
        EventType.INTELLIGENCE_CREATED,
        EventType.ACTIVITY_CREATED,
        EventType.ACTION_TRIGGERED,
        EventType.ACTION_COMPLETED,
        EventType.ACTION_BLOCKED,
        EventType.VERIFICATION_FAILED,
        EventType.GOVERNANCE_CHANGED,
        EventType.HANDOFF_CREATED,
        EventType.NAYA_JOINED,
    }


def build_briefing(
    event: IntelligenceEvent,
    *,
    what_changed: str,
    who_needs_to_know: Tuple[str, ...],
    recommendation: str = "",
    why_it_happened: str = "",
) -> Briefing:
    event.validate()
    return Briefing(
        event_id=event.event_id,
        what_happened=event.summary,
        why_it_happened=why_it_happened or "Not supplied by the source event.",
        why_it_matters=event.why_it_matters,
        what_changed=what_changed,
        who_needs_to_know=who_needs_to_know,
        recommendation=recommendation,
        authority_state=event.authority_state,
        evidence_state=event.evidence_state,
    )


def delivery_state(receipts: Tuple[DeliveryReceipt, ...]) -> str:
    if not receipts:
        return "PENDING"
    states = {r.state.upper() for r in receipts}
    if states == {"DELIVERED"}:
        return "DELIVERED"
    if "DELIVERED" in states:
        return "PARTIAL"
    if "FAILED" in states:
        return "FAILED"
    return "PENDING"


def event_from_execution(
    *,
    event_id: str,
    occurred_at: str,
    source_naya_id: str,
    mission: str,
    action_id: str,
    result: str,
    evidence_state: str,
    related_receipt_id: str | None = None,
    visibility: Visibility = Visibility.PRIVATE,
) -> IntelligenceEvent:
    """Build the canonical communication event for an observed execution result.

    This is a contract builder, not a second persistence system. Production
    persistence/triggering is owned by the managed runtime boundary.
    """
    event_type = {
        "VERIFIED": EventType.ACTION_COMPLETED,
        "LIVE_VERIFIED": EventType.ACTION_COMPLETED,
        "BLOCKED": EventType.ACTION_BLOCKED,
        "FAILED": EventType.VERIFICATION_FAILED,
    }.get(evidence_state.upper(), EventType.ACTIVITY_CREATED)
    event = IntelligenceEvent(
        event_id=event_id,
        event_type=event_type,
        occurred_at=occurred_at,
        source_naya_id=source_naya_id,
        source_surface="NayaPOWER",
        mission=mission,
        summary=result,
        why_it_matters="A material execution result changed the mission's observed state.",
        required_awareness=True,
        authority_state="UNCHANGED",
        evidence_state=evidence_state.upper(),
        visibility=visibility,
        related_receipt_id=related_receipt_id,
        caused_by=action_id,
    )
    event.validate()
    return event
