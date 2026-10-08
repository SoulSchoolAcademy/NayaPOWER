"""
takeover.py — Machine law: the no-waiting doctrine as executable rules.

Lane ownership is about speed, not territory. A takeover is legitimate only if:
1. The owning lane is stalled (no progress within the stall window).
2. The work is within the taker's standing authority (authority_gate ALLOW).
3. The takeover is recorded: what, why, what changed, evidence.
4. The original owner is notified and given the next useful task.

Takeover never bypasses protected gates. "Don't wait" != "don't verify".
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field

from .authority_gate import classify_action, Verdict


STALL_WINDOW_SECONDS = 4 * 3600  # 4 hours of no progress = stalled


@dataclass
class TakeoverRecord:
    taker_id: str
    owner_id: str
    task: str
    reason: str                     # why the lane was judged stalled
    last_owner_progress_at: float   # timestamp of owner's last progress
    what_changed: str = ""
    evidence: str = ""
    owner_notified: bool = False
    owner_next_task: str = ""
    recorded_at: float = field(default_factory=time.time)


@dataclass
class TakeoverResult:
    allowed: bool
    reasons: list = field(default_factory=list)


def evaluate_takeover(record: TakeoverRecord, now: float | None = None) -> TakeoverResult:
    reasons: list[str] = []
    now = now if now is not None else time.time()

    # 1. Stall check: owner must actually be stalled.
    idle_for = now - record.last_owner_progress_at
    if idle_for < STALL_WINDOW_SECONDS:
        reasons.append(
            f"Owner not stalled: last progress {idle_for/3600:.1f}h ago "
            f"(window {STALL_WINDOW_SECONDS/3600:.0f}h). Coordinate, don't take over."
        )

    # 2. Authority check: the task itself must be within standing authority.
    gate = classify_action(record.task)
    if gate.verdict != Verdict.ALLOW:
        reasons.append(
            f"Takeover task fails authority gate: {gate.verdict.value} — {gate.reason}"
        )

    # 3. Same agent taking over its own lane is not a takeover.
    if record.taker_id == record.owner_id:
        reasons.append("Taker and owner are the same agent — this is not a takeover.")

    return TakeoverResult(allowed=not reasons, reasons=reasons)


def validate_completed_takeover(record: TakeoverRecord) -> TakeoverResult:
    """After the work: the record must be complete or the takeover is invalid."""
    reasons: list[str] = []
    if not record.what_changed.strip():
        reasons.append("Takeover record missing: what changed.")
    if not record.evidence.strip():
        reasons.append("Takeover record missing: evidence.")
    if not record.owner_notified:
        reasons.append("Original owner was not notified.")
    if not record.owner_next_task.strip():
        reasons.append("Owner was not given the next useful task.")
    return TakeoverResult(allowed=not reasons, reasons=reasons)
