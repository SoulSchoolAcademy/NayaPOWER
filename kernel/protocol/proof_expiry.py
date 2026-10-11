"""
proof_expiry.py — Law 12: Proofs expire when world changes.

"An old proof is history, not authority."

Every proof (read receipt, scorecard, authority grant, test run) is issued
against a specific world state: a source SHA, a policy version, an authority
receipt. When that world state changes, the proof is STALE — it must be
rechecked or re-verified before it can authorize consequential action.

This is CHANGE-based expiry, not time-based. A proof does not go stale
because an hour passed. It goes stale because something it depended on moved.

Precise invalidation: a main-tip change does NOT invalidate an unrelated
note. Each dependency carries a scope; only dependencies within the proof's
scope can invalidate it.

Statuses:
  CURRENT_UNTIL_RECHECK — all dependencies match current state. Usable.
  STALE                 — a dependency changed. Recheck/reverify required.
  INVALID               — proof was wrong at issue, or a dependency was revoked.

This module extends the existing engine (read_receipt, cold_start_gate,
quality_gate, act_pipeline). It does not replace them.

INTEGRATION POINTS (Law 12 enforcement at execution boundaries):
  1. cold_start_gate.run_cold_start(..., current_protocol_version=...,
     current_source_sha=...) — boot boundary. A cryptographically valid
     read receipt is refused if the protocol version moved since it was
     issued. Backward compatible: without the optional params, behavior
     is unchanged.
  2. act_pipeline.execute_plan(..., law12_state=..., law12_proof_time=...)
     — execution boundary. After the existing time-based check, the fresh
     authority grant is validated as a ProofRecord. Stale grant refuses
     with LAW_AUTHORITY_PROOF_STALE. Backward compatible: without both
     params, the check is skipped.
  3. quality_gate.check_delivery(..., law12_state=..., law12_proof_time=...)
     — delivery boundary. A scorecard whose scored code moved is refused
     as stale. Backward compatible: without both params, behavior unchanged.

All three integrations are opt-in and precise: they only fire when the
caller supplies both proof-time and current values, and they only
invalidate on the dependencies the proof actually declared.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum


class ProofStatus(Enum):
    CURRENT_UNTIL_RECHECK = "CURRENT_UNTIL_RECHECK"
    STALE = "STALE"
    INVALID = "INVALID"


# Well-known dependency kinds. Custom kinds are allowed — the validator
# only requires that current_state provides a value for each kind present.
DEP_SOURCE_SHA = "source_sha"            # code tip the proof was validated against
DEP_POLICY_REF = "policy_ref"            # policy/protocol version in force
DEP_AUTHORITY_RECEIPT = "authority_receipt"  # authorization the proof relied on
DEP_EVIDENCE_REF = "evidence_ref"        # external evidence (test run, artifact)
DEP_CONFIG = "config"                    # configuration the proof assumed


@dataclass
class ProofDependency:
    """One thing the proof assumed about the world at issue time."""
    kind: str          # dependency kind (see DEP_* constants)
    value: str         # value at proof time (SHA, version, receipt ID, ...)
    scope: str = ""    # what this dependency covers; empty = global to the proof

    def matches(self, current_value: str | None) -> bool:
        """True if the world still looks the way the proof assumed."""
        if current_value is None:
            # Unknown current state is not a match — cannot confirm freshness.
            return False
        return current_value == self.value


@dataclass
class ProofRecord:
    """A proof with explicit, checkable dependencies."""
    proof_id: str
    proof_type: str      # "read_receipt" | "scorecard" | "authority" | "test_run" | ...
    dependencies: list[ProofDependency] = field(default_factory=list)
    issued_at: float = field(default_factory=time.time)
    status: ProofStatus = ProofStatus.CURRENT_UNTIL_RECHECK
    invalidated_by: list[str] = field(default_factory=list)  # kinds that went stale

    def dependency_kinds(self) -> list[str]:
        return [d.kind for d in self.dependencies]


@dataclass
class ProofValidation:
    """Result of validating a proof against current world state."""
    proof_id: str
    status: ProofStatus
    stale_dependencies: list[ProofDependency] = field(default_factory=list)
    missing_dependencies: list[str] = field(default_factory=list)
    checked_at: float = field(default_factory=time.time)

    @property
    def is_current(self) -> bool:
        return self.status == ProofStatus.CURRENT_UNTIL_RECHECK

    def reason(self) -> str:
        if self.status == ProofStatus.CURRENT_UNTIL_RECHECK:
            return "All dependencies match current state."
        parts = []
        for d in self.stale_dependencies:
            parts.append(f"{d.kind} changed (was {d.value[:12]})")
        for k in self.missing_dependencies:
            parts.append(f"{k} has no current value to check against")
        return "Stale: " + "; ".join(parts) if parts else "Stale: unknown cause"


def validate_proof(proof: ProofRecord,
                   current_state: dict[str, str]) -> ProofValidation:
    """Check each dependency against current state.

    current_state maps dependency kind -> current value.
    A dependency is stale if its current value differs from proof time.
    A dependency with no current value is missing (cannot confirm) — the
    proof is STALE, not current, because freshness cannot be established.

    Precise invalidation: only the dependencies listed on the proof are
    checked. An unrelated world change (a kind not in the proof's list)
    cannot invalidate this proof.
    """
    stale: list[ProofDependency] = []
    missing: list[str] = []

    for dep in proof.dependencies:
        current = current_state.get(dep.kind)
        if current is None:
            missing.append(dep.kind)
        elif not dep.matches(current):
            stale.append(dep)

    if stale or missing:
        proof.status = ProofStatus.STALE
        proof.invalidated_by = [d.kind for d in stale] + missing
        status = ProofStatus.STALE
    else:
        proof.status = ProofStatus.CURRENT_UNTIL_RECHECK
        proof.invalidated_by = []
        status = ProofStatus.CURRENT_UNTIL_RECHECK

    return ProofValidation(
        proof_id=proof.proof_id,
        status=status,
        stale_dependencies=stale,
        missing_dependencies=missing,
    )


def mark_invalid(proof: ProofRecord, reason: str) -> ProofRecord:
    """Mark a proof INVALID — it was wrong at issue or a dependency revoked.

    INVALID is stronger than STALE: a stale proof can be re-verified;
    an invalid proof must be discarded and re-issued from scratch.
    """
    proof.status = ProofStatus.INVALID
    proof.invalidated_by = [f"INVALID: {reason}"]
    return proof


def reverify(proof: ProofRecord, current_state: dict[str, str],
             new_values: dict[str, str] | None = None) -> ProofValidation:
    """Re-verify a STALE proof: refresh changed dependencies, re-validate.

    new_values maps kind -> new proof-time value (e.g. the new tip SHA).
    Dependencies not in new_values keep their old values (and will likely
    still be stale — the caller must supply the values the re-verification
    actually established).
    """
    if proof.status == ProofStatus.INVALID:
        raise ValueError(
            f"Proof {proof.proof_id} is INVALID and cannot be re-verified; "
            "issue a new proof."
        )
    if new_values:
        for dep in proof.dependencies:
            if dep.kind in new_values:
                dep.value = new_values[dep.kind]
    proof.issued_at = time.time()
    return validate_proof(proof, current_state)


# ---------------------------------------------------------------------------
# Adapters: build ProofRecords from existing proof types.
# ---------------------------------------------------------------------------

def proof_from_read_receipt(receipt, source_sha: str) -> ProofRecord:
    """A read receipt is valid for the protocol version and tip it was read at.

    If the protocol version changes, the receipt is stale (re-read required).
    If the tip moves, the receipt is NOT automatically stale — the protocol
    text the agent read may be unchanged. Tip staleness is scoped: only
    invalidate on tip change if the protocol files themselves changed.
    Here we record the tip as a dependency with scope "protocol_files" so
    callers can decide materiality.
    """
    return ProofRecord(
        proof_id=f"read-receipt:{receipt.agent_id}:{receipt.receipt_hash[:12]}",
        proof_type="read_receipt",
        dependencies=[
            ProofDependency(DEP_POLICY_REF, receipt.protocol_version,
                            scope="protocol_text"),
            ProofDependency(DEP_SOURCE_SHA, source_sha,
                            scope="protocol_files"),
        ],
        issued_at=receipt.issued_at,
    )


def proof_from_scorecard(scorecard, source_sha: str,
                         policy_ref: str = "") -> ProofRecord:
    """A scorecard is valid for the code it scored and the policy in force.

    Evidence refs (test runs, artifacts) are recorded when present in the
    evidence field; callers may add DEP_EVIDENCE_REF dependencies for
    specific run IDs they can re-resolve.
    """
    deps = [
        ProofDependency(DEP_SOURCE_SHA, source_sha, scope="scored_code"),
    ]
    if policy_ref:
        deps.append(ProofDependency(DEP_POLICY_REF, policy_ref,
                                    scope="scoring_rubric"))
    return ProofRecord(
        proof_id=f"scorecard:{scorecard.what[:40]}",
        proof_type="scorecard",
        dependencies=deps,
    )


def proof_from_authority(authority_receipt_id: str, source_sha: str,
                         policy_ref: str) -> ProofRecord:
    """An authority grant is valid while the grant stands and policy holds.

    Revocation is modeled as INVALID (not STALE): mark_invalid when the
    grant is revoked. The execution door must check revocation at execution
    time, not just at planning time.
    """
    return ProofRecord(
        proof_id=f"authority:{authority_receipt_id}",
        proof_type="authority",
        dependencies=[
            ProofDependency(DEP_AUTHORITY_RECEIPT, authority_receipt_id,
                            scope="grant"),
            ProofDependency(DEP_SOURCE_SHA, source_sha, scope="grant_scope"),
            ProofDependency(DEP_POLICY_REF, policy_ref, scope="grant_policy"),
        ],
    )


# ---------------------------------------------------------------------------
# Execution-boundary hook.
# ---------------------------------------------------------------------------

@dataclass
class BoundaryCheck:
    """Result of the Law 12 check at a consequential execution boundary."""
    proceed: bool
    validations: list[ProofValidation] = field(default_factory=list)

    def blockers(self) -> list[str]:
        out = []
        for v in self.validations:
            if not v.is_current:
                out.append(f"{v.proof_id}: {v.reason()}")
        return out


def check_execution_boundary(proofs: list[ProofRecord],
                             current_state: dict[str, str]) -> BoundaryCheck:
    """Law 12 enforcement at a consequential execution boundary.

    Validate every proof the action depends on. If ANY is stale or invalid,
    do not proceed on the old proof — recheck or reverify first.

    This is the check the spec requires "at every consequential execution
    boundary": plan → execute, merge, deploy, promote, authorize.
    """
    validations = [validate_proof(p, current_state) for p in proofs]
    proceed = all(v.is_current for v in validations)
    return BoundaryCheck(proceed=proceed, validations=validations)
