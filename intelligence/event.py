"""Canonical event-native intelligence primitives.

An IntelligentEvent is the durable unit of meaningful experience/change. It is
indexed by multiple dimensions without encoding those dimensions into folders.
The event carries its own provenance, epistemic state, relationships, and
semantic links to the nine-node kernel.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Mapping


class EventState(str, Enum):
    UNKNOWN = "UNKNOWN"
    CANDIDATE = "CANDIDATE"
    DOCUMENTED = "DOCUMENTED"
    VERIFIED = "VERIFIED"
    SUPERSEDED = "SUPERSEDED"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class IntelligenceEvent:
    event_id: str
    occurred_at: datetime
    event_type: str
    topic: str
    category: str
    subject: str
    intelligence: Mapping[str, Any]
    nodes: tuple[str, ...] = ()
    source: str = "unknown"
    evidence: tuple[Mapping[str, Any], ...] = ()
    relationships: Mapping[str, tuple[str, ...]] = field(default_factory=dict)
    state: EventState = EventState.UNKNOWN

    def __post_init__(self) -> None:
        if not self.event_id.strip():
            raise ValueError("event_id is required")
        if self.occurred_at.tzinfo is None:
            raise ValueError("occurred_at must be timezone-aware")
        if not self.topic.strip() or not self.category.strip():
            raise ValueError("topic and category are required")
        object.__setattr__(self, "occurred_at", self.occurred_at.astimezone(timezone.utc))
        object.__setattr__(self, "nodes", tuple(dict.fromkeys(self.nodes)))
        object.__setattr__(
            self,
            "relationships",
            {k: tuple(dict.fromkeys(v)) for k, v in self.relationships.items()},
        )
        object.__setattr__(self, "evidence", tuple(self.evidence))

    @property
    def year(self) -> int:
        return self.occurred_at.year

    @property
    def month(self) -> int:
        return self.occurred_at.month

    @property
    def day(self) -> int:
        return self.occurred_at.day


class EventStore:
    """Small canonical in-memory projection for deterministic kernel tests.

    Production persistence belongs to the canonical Receiver. This store exists
    as the reference behavior for multidimensional retrieval and must not become
    a competing source of truth.
    """

    def __init__(self) -> None:
        self._events: dict[str, IntelligenceEvent] = {}

    def append(self, event: IntelligenceEvent) -> None:
        if event.event_id in self._events:
            raise ValueError(f"duplicate canonical event id: {event.event_id}")
        self._events[event.event_id] = event

    def search(
        self,
        *,
        year: int | None = None,
        month: int | None = None,
        day: int | None = None,
        topic: str | None = None,
        category: str | None = None,
        node: str | None = None,
        event_type: str | None = None,
        state: EventState | None = None,
    ) -> list[IntelligenceEvent]:
        def matches(e: IntelligenceEvent) -> bool:
            return all(
                (
                    year is None or e.year == year,
                    month is None or e.month == month,
                    day is None or e.day == day,
                    topic is None or e.topic.casefold() == topic.casefold(),
                    category is None or e.category.casefold() == category.casefold(),
                    node is None or node in e.nodes,
                    event_type is None or e.event_type.casefold() == event_type.casefold(),
                    state is None or e.state is state,
                )
            )

        return sorted(
            (e for e in self._events.values() if matches(e)),
            key=lambda e: (e.occurred_at, e.event_id),
        )

    def __len__(self) -> int:
        return len(self._events)
