"""Durable executable Torch boundary for NayaPOWER.

This boundary converts an already-selected PriorityDecision into a
self-contained successor instruction. It does not choose priority, grant
authorization, execute work, verify results, or persist learning; those remain
with their existing authorities.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from priority_decision import PriorityDecision


class TorchError(ValueError):
    """Raised when a successor Torch is incomplete or unsafe."""


@dataclass(frozen=True)
class ExecutableTorch:
    torch_id: str
    mission: str
    priority: int
    work_id: str
    why: str
    next_action: str
    expected_value: float
    acceptance_criteria: str
    required_evidence: str
    constraints: str
    successor_instruction: str

    def validate(self) -> None:
        fields = (
            "torch_id", "mission", "why", "next_action", "acceptance_criteria",
            "required_evidence", "constraints", "successor_instruction",
        )
        for field in fields:
            if not getattr(self, field).strip():
                raise TorchError(f"{field} is required")
        if not self.work_id.strip():
            raise TorchError("work_id is required")
        if self.priority < 1:
            raise TorchError("priority must be positive")
        if self.expected_value < 0:
            raise TorchError("expected_value cannot be negative")


def create_torch(
    *,
    torch_id: str,
    mission: str,
    decision: PriorityDecision,
    required_evidence: str,
    constraints: str,
    successor_instruction: Optional[str] = None,
) -> ExecutableTorch:
    """Create a self-contained successor Torch from an existing decision."""
    if not mission.strip():
        raise TorchError("mission is required")
    if not required_evidence.strip():
        raise TorchError("required_evidence is required")
    if not constraints.strip():
        raise TorchError("constraints are required")

    instruction = successor_instruction or (
        f"Execute {decision.next_action}; verify against: "
        f"{decision.acceptance_criteria}; record exact evidence; then determine "
        "and issue the next highest-value continuation Torch."
    )

    torch = ExecutableTorch(
        torch_id=torch_id,
        mission=mission.strip(),
        priority=decision.priority,
        work_id=decision.work_id,
        why=decision.why,
        next_action=decision.next_action,
        expected_value=decision.expected_value,
        acceptance_criteria=decision.acceptance_criteria,
        required_evidence=required_evidence.strip(),
        constraints=constraints.strip(),
        successor_instruction=instruction.strip(),
    )
    torch.validate()
    return torch
