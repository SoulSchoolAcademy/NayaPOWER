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


REQUIRED_TRUTH_MARKERS = ["#1354", "main"]


def run_cold_start(state: ColdStartState,
                   current_protocol_version: str | None = None,
                   current_source_sha: str | None = None) -> ColdStartResult:
    failures: list[str] = []

    # 1. Read receipt must exist and verify.
    if state.receipt is None:
        failures.append("No protocol read receipt. Read the protocol, answer the authority questions.")
    elif not state.receipt.verify():
        failures.append("Read receipt invalid or failed grading. Re-read the protocol.")
    else:
        # Law 12 (ACTIVE): a cryptographically valid receipt is not enough —
        # it must be fresh. Current world state auto-resolves when the
        # caller does not supply it, so this check fires on every boot, not
        # only for callers that opt in. If the protocol version moved since
        # the receipt was issued, the agent read a different protocol:
        # re-read required. (The receipt does not record the read-time tip,
        # so no tip dependency is fabricated — the version check is the
        # precise, honest signal.)
        from .proof_expiry import (
            proof_from_read_receipt, validate_proof, resolve_current_state,
        )
        current_state = resolve_current_state()
        if current_protocol_version is not None:
            current_state["policy_ref"] = current_protocol_version
        if current_source_sha is not None:
            current_state["source_sha"] = current_source_sha
        proof = proof_from_read_receipt(state.receipt)
        validation = validate_proof(proof, current_state)
        if not validation.is_current:
            failures.append(
                f"Read receipt stale (Law 12): {validation.reason()}. "
                "Re-read the current protocol.")

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
            "Truth location must reference the coordination feed (#1354) "
            "and current main — the board alone is not the entire source of truth."
        )

    # 5. Exactly one next action.
    if not state.next_action.strip():
        failures.append("No next executable action declared.")

    return ColdStartResult(passed=not failures, failures=failures)
