#!/usr/bin/env python3
"""Narrow boundary from human intent to a successor-consumable mission.

This module qualifies mission context only. It does not store mission state,
select priority, execute work, verify outcomes, or persist learning.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


class MissionError(ValueError):
    """Raised when a human mission cannot be safely qualified."""


MISSION_TYPES = {"LEARNING", "CREATION"}
LEARNING_STEPS = ("DIAGNOSE", "TEACH", "TEST", "ADAPT", "APPLY")
CREATION_STEPS = ("QUALIFY", "ANALYZE", "RECOMMEND", "PLAN", "EXECUTE", "VERIFY")


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise MissionError(f"{field} is required")
    return value.strip()


def _list(value: Any, field: str) -> list[str]:
    if value is None:
        raise MissionError(f"{field} must be explicit; do not invent constraints")
    if not isinstance(value, list) or any(not isinstance(x, str) or not x.strip() for x in value):
        raise MissionError(f"{field} must be a list of non-empty strings")
    return [x.strip() for x in value]


@dataclass(frozen=True)
class HumanMission:
    mission_id: str
    mission_type: str
    human_goal: str
    desired_outcome: str
    current_state: str
    constraints: tuple[str, ...]
    urgency: str
    current_capability: str
    success_criteria: tuple[str, ...]
    immediate_prompt: str
    path: tuple[str, ...]

    def for_priority(self) -> str:
        """Provide mission truth to the existing Priority authority."""
        return (
            f"Human goal: {self.human_goal}; desired outcome: {self.desired_outcome}; "
            f"current state: {self.current_state}; constraints: {', '.join(self.constraints)}; "
            f"urgency: {self.urgency}; current capability: {self.current_capability}; "
            f"success: {'; '.join(self.success_criteria)}"
        )

    def to_successor(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["constraints"] = list(self.constraints)
        payload["success_criteria"] = list(self.success_criteria)
        payload["path"] = list(self.path)
        payload["schema"] = "naya-power-human-mission/v1"
        payload["authority"] = "human-stated mission; Priority remains canonical selector"
        payload["priority_input"] = self.for_priority()
        return payload


def qualify_mission(raw: dict[str, Any]) -> HumanMission:
    if not isinstance(raw, dict):
        raise MissionError("mission input must be an object")
    mission_id = _text(raw.get("mission_id"), "mission_id")
    mission_type = _text(raw.get("mission_type"), "mission_type").upper()
    if mission_type not in MISSION_TYPES:
        raise MissionError("mission_type must be LEARNING or CREATION")

    human_goal = _text(raw.get("human_goal"), "human_goal")
    desired_outcome = _text(raw.get("desired_outcome"), "desired_outcome")
    current_state = _text(raw.get("current_state"), "current_state")
    urgency = _text(raw.get("urgency"), "urgency")
    current_capability = _text(raw.get("current_capability"), "current_capability")
    immediate_prompt = _text(raw.get("immediate_prompt"), "immediate_prompt")
    constraints = _list(raw.get("constraints"), "constraints")
    success = _list(raw.get("success_criteria"), "success_criteria")
    if not success:
        raise MissionError("success_criteria must contain at least one criterion")

    # Explicitly represent absence instead of guessing a constraint.
    if not constraints:
        constraints = ["NONE_STATED_BY_HUMAN"]

    path = LEARNING_STEPS if mission_type == "LEARNING" else CREATION_STEPS
    return HumanMission(
        mission_id=mission_id,
        mission_type=mission_type,
        human_goal=human_goal,
        desired_outcome=desired_outcome,
        current_state=current_state,
        constraints=tuple(constraints),
        urgency=urgency,
        current_capability=current_capability,
        success_criteria=tuple(success),
        immediate_prompt=immediate_prompt,
        path=tuple(path),
    )
