"""
cold_start_gate.py — Machine law: mandatory boot sequence for fresh agents.

A fresh agent may not begin governed work until it can demonstrate:
1. Valid protocol read receipt (read_receipt.py)
2. Identity: who it is, who the human director is
3. Authority: what it may and may not do
4. Navigation: where current truth lives
5. Next action: exactly one executable next step

This is the machine twin of the ACTIVATION ACCEPTANCE contract.

Check 6 folds in Gate 1 (tools/activation_checklist.py): activation is not
complete until the 14 thinking lessons + Operating Code V2 are
machine-verified against canonical bytes. Fail closed: if the checklist
tool is missing, unreadable, or any violation is found, boot is refused.
"""
from __future__ import annotations

import importlib.util
from dataclasses import dataclass, field
from pathlib import Path

from .read_receipt import ReadReceipt

_REPO_ROOT = Path(__file__).resolve().parents[2]
_CHECKLIST_TOOL = _REPO_ROOT / "tools" / "activation_checklist.py"


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


def _check_activation_checklist(checklist_claim=None) -> list[str]:
    """Gate 1 — activation checklist machine-verification, fail closed.

    Loads tools/activation_checklist.py from this repo's own bytes (never
    from an agent-supplied path), self-audits the canonical artifacts
    (14 lesson pins + V2 pins + twin consistency), and — when the caller
    supplies an agent's checklist claim — verifies the claim against the
    recomputed canonical bytes. Any error, any violation, any missing
    tool: boot refused. A claim is untrusted input; hashes are recomputed,
    never trusted.
    """
    failures: list[str] = []
    try:
        spec = importlib.util.spec_from_file_location(
            "naya_activation_checklist", str(_CHECKLIST_TOOL))
        if spec is None or spec.loader is None:
            raise RuntimeError("checklist tool not loadable")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception as e:
        return [f"Activation checklist tool unavailable ({e}) — "
                "cannot machine-verify activation. Boot refused (fail closed)."]
    canonical, err = module.load_canonical(str(_REPO_ROOT))
    if canonical is None:
        return [f"Activation checklist canonical artifacts unreadable: {err} "
                "— boot refused (fail closed)."]
    verdict, violations = module.check_checklist(canonical, checklist_claim)
    if verdict != "CHECKLIST-VERIFIED":
        failures.append(
            "Activation checklist NOT verified (Gate 1): "
            + "; ".join(violations[:6])
            + (f" (+{len(violations) - 6} more)" if len(violations) > 6 else "")
            + " — boot refused (fail closed).")
    return failures


def run_cold_start(state: ColdStartState,
                   current_protocol_version: str | None = None,
                   current_source_sha: str | None = None,
                   checklist_claim: dict | None = None) -> ColdStartResult:
    failures: list[str] = []

    # 1. Read receipt must exist and verify.
    if state.receipt is None:
        failures.append("No protocol read receipt. Read the protocol, answer the authority questions.")
    elif not state.receipt.verify():
        failures.append("Read receipt invalid or failed grading. Re-read the protocol.")
    else:
        # Law 12 (ACTIVE): an integrity-valid receipt is not enough —
        # it must be fresh. The seal proves the receipt was not altered; it
        # does not authenticate the issuer (see read_receipt.py trust
        # boundary, B-40). Current world state auto-resolves when the
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

    # 6. Gate 1 — activation checklist: the 14 thinking lessons and
    # Operating Code V2 must machine-verify against canonical bytes.
    # No checklist pass = no start. Fail closed.
    failures.extend(_check_activation_checklist(checklist_claim))

    return ColdStartResult(passed=not failures, failures=failures)
