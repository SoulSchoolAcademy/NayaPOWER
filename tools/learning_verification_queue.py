"""Learning verification queue — the queue is WORKED, not watched.

Admitted candidates enter here. Each carries an SLA: verified within 48 hours
of admission (Shawn's rule, 2026-10-09) or retired. The queue sweeps itself:
overdue entries are retired with the reason recorded, never left to rot.

Claim rule: the verifier must differ from BOTH the doer and the scorer.
doer != scorer != verifier, always.

This is operational working state (who is verifying what, by when). It is not
a competing source of truth: the canonical learning store remains the
Receiver/Supabase. Queue state lives at
BRAIN/07-LEARNING/VERIFICATION-QUEUE/queue.json and is an internal projection.

Pure logic takes an explicit clock so tests are deterministic.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable

SLA_HOURS = 48

STATUS_QUEUED = "QUEUED"
STATUS_CLAIMED = "CLAIMED"
STATUS_VERIFIED = "VERIFIED"
STATUS_NOT_VERIFIED = "NOT_VERIFIED"
STATUS_RETIRED = "RETIRED"

VERDICTS = frozenset({STATUS_VERIFIED, STATUS_NOT_VERIFIED})


@dataclass
class QueueEntry:
    entry_id: str
    candidate_id: str
    claim: str
    task: str
    doer: str
    scorer: str
    admitted_at: str  # ISO-8601 UTC
    verify_by: str    # ISO-8601 UTC = admitted_at + 48h
    status: str = STATUS_QUEUED
    verifier: str = ""
    claimed_at: str = ""
    verdict: str = ""
    verdict_reason: str = ""
    decided_at: str = ""


def _now_iso(clock: Callable[[], datetime]) -> str:
    return clock().astimezone(timezone.utc).isoformat()


def enqueue(candidate: dict[str, Any], candidate_id: str,
            clock: Callable[[], datetime] = lambda: datetime.now(timezone.utc)) -> QueueEntry:
    """Admit a gate-passed candidate into the verification queue."""
    now = _now_iso(clock)
    verify_by = (clock().astimezone(timezone.utc) + timedelta(hours=SLA_HOURS)).isoformat()
    return QueueEntry(
        entry_id=f"VQ-{candidate_id[:8]}",
        candidate_id=candidate_id,
        claim=str(candidate.get("claim", "")),
        task=str(candidate.get("task", "")),
        doer=str(candidate.get("doer", "")),
        scorer=str(candidate.get("scorer", "")),
        admitted_at=now,
        verify_by=verify_by,
    )


def claim(entry: QueueEntry, verifier: str,
          clock: Callable[[], datetime] = lambda: datetime.now(timezone.utc)) -> QueueEntry:
    """A seat claims the verification job. Verifier must differ from doer and scorer."""
    if entry.status != STATUS_QUEUED:
        raise ValueError(f"cannot claim entry in status {entry.status}")
    v = verifier.strip()
    if not v:
        raise ValueError("verifier required")
    if v == entry.doer or v == entry.scorer:
        raise ValueError("verifier must differ from both doer and scorer")
    return QueueEntry(**{**asdict(entry), "status": STATUS_CLAIMED,
                         "verifier": v, "claimed_at": _now_iso(clock)})


def record_verdict(entry: QueueEntry, verdict: str, reason: str,
                   clock: Callable[[], datetime] = lambda: datetime.now(timezone.utc)) -> QueueEntry:
    """Record the independent verdict. Only a claimed entry can be decided."""
    if entry.status != STATUS_CLAIMED:
        raise ValueError(f"cannot decide entry in status {entry.status}")
    if verdict not in VERDICTS:
        raise ValueError(f"verdict must be one of {sorted(VERDICTS)}")
    if not reason.strip():
        raise ValueError("verdict reason required")
    return QueueEntry(**{**asdict(entry), "status": verdict,
                         "verdict": verdict, "verdict_reason": reason.strip(),
                         "decided_at": _now_iso(clock)})


def sweep_overdue(entries: list[QueueEntry],
                  clock: Callable[[], datetime] = lambda: datetime.now(timezone.utc)
                  ) -> tuple[list[QueueEntry], list[QueueEntry]]:
    """Retire every QUEUED/CLAIMED entry past its verify_by. Returns (kept, retired)."""
    now = clock().astimezone(timezone.utc)
    kept: list[QueueEntry] = []
    retired: list[QueueEntry] = []
    for e in entries:
        if e.status in (STATUS_QUEUED, STATUS_CLAIMED) and datetime.fromisoformat(e.verify_by) < now:
            retired.append(QueueEntry(**{**asdict(e), "status": STATUS_RETIRED,
                                         "verdict": STATUS_RETIRED,
                                         "verdict_reason": "SLA_EXPIRED: no verdict within 48h of admission",
                                         "decided_at": now.isoformat()}))
        else:
            kept.append(e)
    return kept, retired


def save_queue(entries: list[QueueEntry], path: str | Path) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps([asdict(e) for e in entries], indent=2), encoding="utf-8")


def load_queue(path: str | Path) -> list[QueueEntry]:
    p = Path(path)
    if not p.exists():
        return []
    return [QueueEntry(**d) for d in json.loads(p.read_text(encoding="utf-8"))]
