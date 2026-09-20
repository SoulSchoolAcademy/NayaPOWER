"""Thin adapter from a validated ExecutableTorch to canonical execution.

Priority selects. Torch packages. The existing project execution contract
remains authoritative for canonical NEXT-EXECUTION consumption. This module
only binds the two representations and refuses divergence.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from executable_torch import ExecutableTorch
from project_execution_contract import validate_next_execution


class TorchExecutionBindingError(ValueError):
    """Raised when a Torch cannot be safely bound to canonical execution."""


@dataclass(frozen=True)
class ExecutionBinding:
    torch_id: str
    work_id: str
    successor: Mapping[str, Any]


def bind_torch_to_canonical_execution(
    torch: ExecutableTorch, successor: Mapping[str, Any]
) -> ExecutionBinding:
    """Validate and bind a Torch to an already-canonical successor.

    This does not execute work and does not replace the project execution
    contract. The supplied successor is validated by that existing authority.
    """
    torch.validate()
    errors = validate_next_execution(dict(successor))
    if errors:
        raise TorchExecutionBindingError("; ".join(errors))

    checks = (
        ("next_action", torch.next_action, successor.get("next_action")),
        ("constraints", torch.constraints, successor.get("constraints")),
        ("acceptance_criteria", torch.acceptance_criteria, successor.get("success_criteria")),
        ("required_evidence", torch.required_evidence, successor.get("verification_requirements")),
    )
    for field, torch_value, canonical_value in checks:
        canonical_text = str(canonical_value or "")
        if torch_value not in canonical_text:
            raise TorchExecutionBindingError(
                f"Torch/canonical successor divergence: {field}"
            )

    return ExecutionBinding(
        torch_id=torch.torch_id,
        work_id=torch.work_id,
        successor=dict(successor),
    )
