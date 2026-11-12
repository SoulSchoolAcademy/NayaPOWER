"""
minimal_action.py — Machine law: enforce the smallest effective change.

Point 5 of the Unified Operating Law: "Execute the smallest effective
authorized action, preserving correct existing behavior."

A proposed change must declare: what it changes, what it preserves,
and why nothing smaller would work. This is checked, not assumed.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ChangeProposal:
    description: str
    files_changed: list[str]
    behavior_preserved: str      # what existing behavior is kept intact
    why_not_smaller: str        # why this is the minimum


@dataclass
class MinimalActionResult:
    passed: bool
    reasons: list = field(default_factory=list)


# Hard ceiling: a "minimal" change touching more files than this is suspect.
FILE_COUNT_SOFT_CAP = 15


def check_minimal(proposal: ChangeProposal) -> MinimalActionResult:
    reasons: list[str] = []
    if not proposal.description.strip():
        reasons.append("No description of the change.")
    if not proposal.files_changed:
        reasons.append("No files listed as changed.")
    if not proposal.behavior_preserved.strip():
        reasons.append("Does not state what existing behavior is preserved.")
    if not proposal.why_not_smaller.strip():
        reasons.append("Does not justify why nothing smaller would work.")
    if len(proposal.files_changed) > FILE_COUNT_SOFT_CAP:
        reasons.append(
            f"Touches {len(proposal.files_changed)} files (soft cap {FILE_COUNT_SOFT_CAP}) — "
            "split into smaller changes or justify the breadth."
        )
    return MinimalActionResult(passed=not reasons, reasons=reasons)
