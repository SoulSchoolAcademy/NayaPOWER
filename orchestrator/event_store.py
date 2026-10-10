"""Durable processing obligation: a committed capture creates exactly one event.

Idempotency: the event ID is derived deterministically from the canonical
lesson identity — committing the same capture twice yields the same event ID,
so duplicates are impossible and retries are safe.

Storage: append-only JSONL. Each line is one event record. Readers scan the
file; the file is the log. No database required for the obligation itself —
the obligation must survive even when downstream stores are unavailable.
"""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def derive_event_id(lesson_id: str, capture_fingerprint: str) -> str:
    """Deterministic event ID: same capture → same event, always."""
    digest = hashlib.sha256(f"{lesson_id}\n{capture_fingerprint}".encode("utf-8")).hexdigest()
    return f"evt_{digest[:32]}"


def derive_correlation_id() -> str:
    """Fresh correlation ID per event: chains every stage record of one run."""
    return f"corr_{uuid.uuid4().hex}"


@dataclass
class ProcessingEvent:
    event_id: str
    lesson_id: str
    correlation_id: str
    capture_fingerprint: str
    status: str = "OBLIGATED"  # OBLIGATED | RUNNING | INCOMPLETE | FAILED | BLOCKED | REJECTED | SUCCESS
    created_at: str = field(default_factory=_utcnow)
    updated_at: str = field(default_factory=_utcnow)
    note: str = ""


class EventStore:
    """Append-only JSONL event log. The log is the obligation."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _read_all(self) -> dict[str, ProcessingEvent]:
        events: dict[str, ProcessingEvent] = {}
        if not self.path.exists():
            return events
        with self.path.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                record = json.loads(line)
                events[record["event_id"]] = ProcessingEvent(**record)
        return events

    def _append(self, event: ProcessingEvent) -> None:
        # Append-only: open in append mode, single line, fsync for durability.
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(event), sort_keys=True) + "\n")
            f.flush()
            os.fsync(f.fileno())

    def commit(self, lesson_id: str, capture_fingerprint: str, note: str = "") -> ProcessingEvent:
        """Commit a capture. Idempotent: same capture → same event, returned as-is."""
        event_id = derive_event_id(lesson_id, capture_fingerprint)
        existing = self._read_all().get(event_id)
        if existing is not None:
            return existing  # Already obligated. No duplicate. No-op.
        event = ProcessingEvent(
            event_id=event_id,
            lesson_id=lesson_id,
            correlation_id=derive_correlation_id(),
            capture_fingerprint=capture_fingerprint,
            note=note,
        )
        self._append(event)
        return event

    def get(self, event_id: str) -> ProcessingEvent | None:
        return self._read_all().get(event_id)

    def set_status(self, event_id: str, status: str, note: str = "") -> ProcessingEvent:
        """Status transitions are recorded as new log lines (history preserved)."""
        current = self._read_all().get(event_id)
        if current is None:
            raise KeyError(f"unknown event: {event_id}")
        updated = ProcessingEvent(
            event_id=current.event_id,
            lesson_id=current.lesson_id,
            correlation_id=current.correlation_id,
            capture_fingerprint=current.capture_fingerprint,
            status=status,
            created_at=current.created_at,
            updated_at=_utcnow(),
            note=note or current.note,
        )
        self._append(updated)
        return updated

    def list_by_status(self, status: str) -> list[ProcessingEvent]:
        # Latest record per event wins.
        return [e for e in self._read_all().values() if e.status == status]


def commit_event(
    lesson_id: str,
    capture_fingerprint: str,
    store_path: str | Path = ".naya/orchestrator/events.jsonl",
    note: str = "",
) -> ProcessingEvent:
    """Convenience: commit against the default store location."""
    return EventStore(store_path).commit(lesson_id, capture_fingerprint, note=note)
