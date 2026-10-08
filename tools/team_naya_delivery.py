"""Single governed writer for Team Naya delivery comments."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from tools.worker_handoff import TeamNayaHandoffExecution, execute_team_naya_handoff


@dataclass
class DeliveryResult:
    passed: bool
    decision: str
    execution: TeamNayaHandoffExecution
    posted: bool = False
    reasons: list[str] = field(default_factory=list)


def deliver_team_naya_comment(
    handoff_text: str,
    sign_out: dict,
    post: Callable[[str], object],
) -> DeliveryResult:
    """Validate the complete handoff/sign-out chain before allowing a post.

    The post callback is intentionally the only side-effect boundary. A hold
    or block returns before it is called, so a caller cannot accidentally make
    a failed delivery visible as a successful Team Naya completion.
    """
    execution = execute_team_naya_handoff(handoff_text, sign_out)
    if not execution.passed:
        reasons = list(getattr(execution.sign_out, "reasons", []))
        return DeliveryResult(False, execution.decision, execution, False, reasons)

    post(handoff_text)
    return DeliveryResult(True, "PASS", execution, True, [])
