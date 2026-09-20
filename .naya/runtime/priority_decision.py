"""Deterministic Priority Decision boundary for NayaPOWER.

This module selects one next action from an explicit work queue. It does not
own governing law, authorization, claims, execution, or evidence. Those remain
with their canonical layers.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Tuple


class PriorityError(ValueError):
    """Raised when priority input is incomplete or unsafe to rank."""


@dataclass(frozen=True)
class WorkItem:
    work_id: str
    title: str
    next_action: str
    acceptance_criteria: str
    mission_alignment: float
    expected_value: float
    urgency: float
    dependency_impact: float
    reversibility: float
    risk: float
    executable: bool = True
    blocked: bool = False

    def validate(self) -> None:
        if not self.work_id or not self.title or not self.next_action:
            raise PriorityError("work_id, title, and next_action are required")
        if not self.acceptance_criteria:
            raise PriorityError("acceptance_criteria is required")
        for name in (
            "mission_alignment",
            "expected_value",
            "urgency",
            "dependency_impact",
            "reversibility",
            "risk",
        ):
            value = getattr(self, name)
            if not 0 <= value <= 1:
                raise PriorityError(f"{name} must be between 0 and 1")
        if self.blocked or not self.executable:
            return


@dataclass(frozen=True)
class PriorityDecision:
    priority: int
    work_id: str
    why: str
    next_action: str
    expected_value: float
    acceptance_criteria: str
    score: float


def _score(item: WorkItem) -> float:
    # Mission and useful outcome dominate. Urgency/dependency break ties in
    # favor of leverage; risk reduces score; reversibility is a safety tie-break.
    return (
        0.30 * item.mission_alignment
        + 0.25 * item.expected_value
        + 0.15 * item.urgency
        + 0.15 * item.dependency_impact
        + 0.05 * item.reversibility
        - 0.10 * item.risk
    )


def choose_priority(mission: str, items: Iterable[WorkItem]) -> PriorityDecision:
    if not mission or not mission.strip():
        raise PriorityError("mission is required")

    candidates = []
    for item in items:
        item.validate()
        if item.executable and not item.blocked:
            candidates.append((_score(item), item))

    if not candidates:
        raise PriorityError("no executable unblocked work is available")

    # Stable deterministic tie-break: score, dependency leverage, then work_id.
    candidates.sort(key=lambda pair: (pair[0], pair[1].dependency_impact, pair[1].work_id), reverse=True)
    score, winner = candidates[0]

    why = (
        f"Selected for mission alignment={winner.mission_alignment:.2f}, "
        f"expected value={winner.expected_value:.2f}, urgency={winner.urgency:.2f}, "
        f"dependency impact={winner.dependency_impact:.2f}, risk={winner.risk:.2f}."
    )

    return PriorityDecision(
        priority=1,
        work_id=winner.work_id,
        why=why,
        next_action=winner.next_action,
        expected_value=winner.expected_value,
        acceptance_criteria=winner.acceptance_criteria,
        score=score,
    )
