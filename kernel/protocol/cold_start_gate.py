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

from .read_receipt import PROTOCOL_VERSION, ReadReceipt
from .work_cycle_receipt import check_sign_in


@dataclass
class ColdStartState:
    agent_id: str
    human_director: str
    lane: str
    authority_summary: str
    current_truth_location: str
    next_action: str
    receipt: ReadReceipt | None = None
    current_main_sha: str = ""
    sign_in_record: dict | None = None
    live_feed_issues: list[int] | None = None


@dataclass
class ColdStartResult:
    passed: bool
    failures: list = field(default_factory=list)


REQUIRED_TRUTH_MARKERS = ["#2154", "#2175", "main"]


def run_cold_start(state: ColdStartState) -> ColdStartResult:
    failures: list[str] = []

    # 1. Read receipt must exist and verify.
    if state.receipt is None:
        failures.append("No protocol read receipt. Read the protocol, answer the authority questions.")
    elif not state.receipt.verify():
        failures.append("Read receipt invalid, stale, missing a required source, or failed comprehension. Re-read the current boot packet.")
    elif state.receipt.agent_id != state.agent_id:
        failures.append("Read receipt belongs to a different agent identity.")
    elif state.receipt.protocol_version != PROTOCOL_VERSION:
        failures.append("Read receipt is not bound to the current PROTOCOL.md candidate version.")
    elif not state.current_main_sha or state.receipt.current_main_sha != state.current_main_sha:
        failures.append("Read receipt does not match the current origin/main SHA.")

    # 2. Identity.
    if not state.agent_id.strip():
        failures.append("No agent identity declared.")
    if "shawn" not in state.human_director.lower():
        failures.append("Human director not identified as Shawn.")

    # 3. Authority summary must name at least one protected gate.
    auth = state.authority_summary.lower()
    if not any(k in auth for k in ["production", "credential", "money",
                                    "destructive", "ratif", "privacy", "security"]):
        failures.append("Authority summary does not name protected gates.")

    # 4. Navigation: must reference the coordination surface and current main.
    nav = state.current_truth_location.lower()
    if not all(m in nav for m in REQUIRED_TRUTH_MARKERS):
        failures.append(
            "Truth location must reference mission issue #2154, current coordination board #2175, and current main. #1354 is historical/read-only."
        )

    # 5. A real structured SIGN_IN must be observed before governed work.
    if state.sign_in_record is None:
        failures.append("No live-feed SIGN_IN receipt. Post and verify it before substantive work.")
    else:
        allowed = set(state.live_feed_issues) if state.live_feed_issues is not None else None
        result = check_sign_in(state.sign_in_record, state.current_main_sha, allowed)
        failures.extend(result.failures)

    # 6. Exactly one next action.
    if not state.next_action.strip():
        failures.append("No next executable action declared.")

    return ColdStartResult(passed=not failures, failures=failures)
