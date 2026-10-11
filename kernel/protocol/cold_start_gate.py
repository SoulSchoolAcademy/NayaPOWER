"""
cold_start_gate.py — Machine law: mandatory boot sequence for fresh agents.

A fresh agent may not begin governed work until it can demonstrate:
1. Valid protocol read receipt (read_receipt.py)
2. Identity: who it is, who the human director is
3. Authority: what it may and may not do
4. Navigation: where current truth lives
5. Next action: exactly one executable next step

This is the machine twin of the ACTIVATION ACCEPTANCE contract.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .read_receipt import ReadReceipt


@dataclass
class ColdStartState:
    agent_id: str
    human_director: str
    lane: str
    authority_summary: str
    current_truth_location: str
    next_action: str
    receipt: ReadReceipt | None = None


@dataclass
class ColdStartResult:
    passed: bool
    failures: list = field(default_factory=list)


REQUIRED_TRUTH_MARKERS = ["#2154", "main"]


def run_cold_start(state: ColdStartState) -> ColdStartResult:
    failures: list[str] = []

    # 1. Read receipt must exist and verify.
    if state.receipt is None:
        failures.append("No protocol read receipt. Read the protocol, answer the authority questions.")
    elif not state.receipt.verify():
        failures.append("Read receipt invalid or failed grading. Re-read the protocol.")

    # 2. Identity.
    if not state.agent_id.strip():
        failures.append("No agent identity declared.")
    if "shawn" not in state.human_director.lower():
        failures.append("Human director not identified as Shawn.")

    # 3. Authority summary must name at least one protected gate and
    # acknowledge Law 11 (do no harm) as the only hard law.
    auth = state.authority_summary.lower()
    if not any(k in auth for k in ["production", "credential", "money",
                                    "destructive", "ratif", "privacy", "security"]):
        failures.append("Authority summary does not name protected gates.")
    if "do no harm" not in auth and "law 11" not in auth:
        failures.append(
            "Authority summary does not acknowledge Law 11 (do no harm) "
            "as the only hard law."
        )

    # 4. Navigation: must reference the mission-state feed and current main.
    nav = state.current_truth_location.lower()
    if not all(m in nav for m in REQUIRED_TRUTH_MARKERS):
        failures.append(
            "Truth location must reference the mission-state feed (#2154) "
            "and current main — the board alone is not the entire source of truth. "
            "(#1354 is archived; sign in/out on #1713/#1714/#1715.)"
        )

    # 5. Exactly one next action.
    if not state.next_action.strip():
        failures.append("No next executable action declared.")

    return ColdStartResult(passed=not failures, failures=failures)
