"""
cold_start_gate.py — fail-closed boot sequence for fresh agents.

Governed work requires a valid current-document read receipt, declared identity,
human authority, correct current navigation, and exactly one next action.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .read_receipt import ReadReceipt, REQUIRED_READING_PATHS


@dataclass
class ColdStartState:
    agent_id: str
    human_director: str
    lane: str
    authority_summary: str
    current_truth_location: str
    next_action: str
    receipt: ReadReceipt | None = None
    current_document_sha256: dict[str, str] = field(default_factory=dict)


@dataclass
class ColdStartResult:
    passed: bool
    failures: list = field(default_factory=list)


REQUIRED_TRUTH_MARKERS = ["#2175", "#2154", "#1599", "main"]


def run_cold_start(state: ColdStartState) -> ColdStartResult:
    failures: list[str] = []

    # 1. Receipt must bind every required reading to the bytes in current state.
    if state.receipt is None:
        failures.append("No protocol read receipt. Read the required sources and answer the comprehension questions.")
    elif set(state.current_document_sha256) != set(REQUIRED_READING_PATHS):
        failures.append("Current hashes for every mandatory reading were not supplied; activation fails closed.")
    elif not state.receipt.verify(expected_document_sha256=state.current_document_sha256):
        failures.append("Read receipt failed comprehension, completeness, integrity, or current-source binding.")

    # 2. Identity.
    if not state.agent_id.strip():
        failures.append("No agent identity declared.")
    if "shawn" not in state.human_director.lower():
        failures.append("Human director not identified as Shawn.")

    # 3. Authority summary must name at least one protected gate.
    auth = state.authority_summary.lower()
    if not any(k in auth for k in ["production", "credential", "money", "destructive", "ratif", "privacy", "security"]):
        failures.append("Authority summary does not name protected gates.")

    # 4. Current navigation: coordination, mission state, index, and current main.
    nav = state.current_truth_location.lower()
    if not all(marker in nav for marker in REQUIRED_TRUTH_MARKERS):
        failures.append(
            "Truth location must reference current coordination (#2175), mission state (#2154), "
            "the specialty-feed index (#1599), and current main."
        )

    # 5. Exactly one next action.
    if not state.next_action.strip():
        failures.append("No next executable action declared.")

    return ColdStartResult(passed=not failures, failures=failures)
