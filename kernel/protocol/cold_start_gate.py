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
machine-verified against canonical bytes.
Check 7 requires a fresh Step 0 declaration receipt bound to this agent
and the pinned current protocol. Missing, stale, mismatched, or
unverifiable declaration = boot refused. The receipt is an auditable
claim of declaration, not proof of speech, belief, or authorization.
Fail closed: missing tools or failed checks never authorize a boot.
"""
from __future__ import annotations

import importlib.util
from dataclasses import dataclass, field
from pathlib import Path

from .read_receipt import ReadReceipt

_REPO_ROOT = Path(__file__).resolve().parents[2]
_CHECKLIST_TOOL = _REPO_ROOT / "tools" / "activation_checklist.py"
_DECLARATION_TOOL = _REPO_ROOT / "tools" / "protocol_pin.py"
# Explicit admission freshness bound, not proof of one declaration per shift.
_DECLARATION_MAX_AGE_HOURS = 24


@dataclass
class ColdStartState:
    agent_id: str
    human_director: str
    lane: str
    authority_summary: str
    current_truth_location: str
    next_action: str
    receipt: ReadReceipt | None = None
    declaration_receipt: dict | None = None


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



def _check_step0_declaration(agent_id: str, receipt: dict | None) -> list[str]:
    """Admission check for the canonical Step 0 declaration, fail closed.

    Never issue a declaration inside the verifier: issuance must be an
    explicit preceding action, and self-issued receipts alone do not
    prove actual speech or confer authorization. A renewed shift must
    present a newly issued receipt; freshness alone is not a shift ID.
    """
    if receipt is None:
        return ["Step 0 declaration receipt MISSING - boot refused. "
                "Declare first and present a fresh receipt for this shift."]
    if not isinstance(receipt, dict):
        return ["Step 0 declaration receipt MALFORMED - boot refused."]
    if not isinstance(agent_id, str) or not agent_id.strip():
        return ["Step 0 declaration agent identity missing - boot refused."]
    if receipt.get("agent_id") != agent_id.strip():
        return ["Step 0 declaration AGENT_MISMATCH - receipt belongs to "
                "another agent. Boot refused."]

    try:
        spec = importlib.util.spec_from_file_location(
            "naya_protocol_declaration", str(_DECLARATION_TOOL))
        if spec is None or spec.loader is None:
            raise RuntimeError("canonical protocol declaration tool not loadable")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        pin_pass, detail = module.check_protocol_pin(str(_REPO_ROOT))
        if not pin_pass:
            return [f"Step 0 declaration protocol PIN_MISMATCH: "
                    f"{detail} - boot refused."]
        violations = module.check_declaration_receipt(
            str(_REPO_ROOT), receipt,
            max_age_hours=_DECLARATION_MAX_AGE_HOURS)
    except Exception as exc:
        return [f"Step 0 declaration verification UNAVAILABLE "
                f"({exc}) - boot refused."]
    return [f"Step 0 declaration REJECT: {v} - boot refused."
            for v in violations]


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

    # Step 0 is a non-optional admission precondition, not a CLI opt-in.
    # No automatic receipt issuance: the agent must declare first.
    failures.extend(_check_step0_declaration(
        state.agent_id, state.declaration_receipt))

    return ColdStartResult(passed=not failures, failures=failures)
