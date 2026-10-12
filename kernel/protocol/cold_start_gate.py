"""
cold_start_gate.py — Machine law: mandatory boot sequence for fresh agents.

A fresh agent may not begin governed work until it can demonstrate:
1. Valid protocol read receipt (read_receipt.py)
2. Identity: who it is, who the human director is
3. Authority: what it may and may not do
4. Navigation: where current truth lives
5. Next action: exactly one executable next step
6. Activation checklist (Gate 1): all 14 thinking lessons + Operating Code
   V2 machine-verified from canonical bytes (tools/activation_checklist.py).
   The claim is UNTRUSTED — the gate recomputes the verdict. No checklist
   pass = no start (fail closed).

This is the machine twin of the ACTIVATION ACCEPTANCE contract.
"""
from __future__ import annotations

import os

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
    # Checkout whose canonical activation artifacts get verified.
    # Empty or nonexistent => the checklist cannot be verified => REJECT.
    repo_root: str = ""
    # The agent's activation checklist claim: {"lessons": [{"lesson_id",
    # "sha256"}], "v2": {rel_path: sha256}}. UNTRUSTED input — ids must be
    # canonical and hashes must equal recomputed canonical bytes. None =
    # self-audit of the canonical artifacts only (still machine-verified).
    checklist_claim: dict | None = None


@dataclass
class ColdStartResult:
    passed: bool
    failures: list = field(default_factory=list)


REQUIRED_TRUTH_MARKERS = ["#2154", "main"]


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

    # 6. Activation checklist (Gate 1, GRAND-TODO P0): all 14 thinking
    #    lessons + Operating Code V2 machine-verified from canonical
    #    bytes. The claim is UNTRUSTED — the gate recomputes the verdict,
    #    so a self-asserted "passed" buys nothing. No checklist pass =
    #    no start (fail closed).
    ok, checklist_msgs = _run_activation_checklist(
        state.repo_root, state.checklist_claim)
    if not ok:
        failures.extend(checklist_msgs)

    return ColdStartResult(passed=not failures, failures=failures)


def _load_checklist_tool(repo_root):
    """Import tools/activation_checklist.py by path (tools/ is not a
    package). Raises on failure — the caller fails closed."""
    import importlib.util
    tool_path = os.path.join(repo_root, "tools", "activation_checklist.py")
    spec = importlib.util.spec_from_file_location(
        "naya_activation_checklist", tool_path)
    if spec is None or spec.loader is None:
        raise ImportError(
            "cannot locate tools/activation_checklist.py under %r" % repo_root)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _run_activation_checklist(repo_root, claim):
    """Fold Gate 1 into the boot decision. Returns (ok, messages).

    Fail-closed on EVERY path: missing repo root, unimportable tool,
    unreadable canonical artifacts, tool errors, or a REJECT verdict all
    mean "not activated". There is no advisory mode and no way to assert
    a pass by supplying a claim — the predicate recomputes from the
    canonical bytes.
    """
    if not repo_root or not os.path.isdir(repo_root):
        return False, ["ACTIVATION_CHECKLIST_UNVERIFIED: no checkout root "
                       "supplied to verify the activation checklist against "
                       "— refusing to start (fail closed)"]
    try:
        ac = _load_checklist_tool(repo_root)
    except Exception as e:
        return False, ["ACTIVATION_CHECKLIST_UNAVAILABLE: gate-1 tool "
                       "unimportable (%s) — refusing to start "
                       "(fail closed)" % e]
    try:
        canonical, err = ac.load_canonical(repo_root, repo_root)
    except Exception as e:
        return False, ["ACTIVATION_CHECKLIST_TOOL_ERROR: load_canonical "
                       "raised (%s) — refusing to start (fail closed)" % e]
    if canonical is None:
        return False, ["ACTIVATION_CHECKLIST_TOOL_ERROR: %s — refusing to "
                       "start (fail closed)" % err]
    try:
        verdict, violations = ac.check_checklist(canonical, claim)
    except Exception as e:
        return False, ["ACTIVATION_CHECKLIST_TOOL_ERROR: check raised (%s) "
                       "— refusing to start (fail closed)" % e]
    if verdict != "CHECKLIST-VERIFIED":
        return False, ["ACTIVATION_CHECKLIST_REJECTED: "
                       + "; ".join(violations)]
    return True, []
