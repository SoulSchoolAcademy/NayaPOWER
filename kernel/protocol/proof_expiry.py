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
  NEEDS_EVIDENCE        — the proof declares no dependencies, so freshness
                          cannot be established. Fail closed: do not proceed.

This module extends the existing engine (read_receipt, cold_start_gate,
quality_gate, act_pipeline). It does not replace them.

INTEGRATION POINTS (Law 12 enforcement at execution boundaries):
  1. cold_start_gate.run_cold_start(...) — boot boundary. Current world
     state auto-resolves (resolve_current_state); explicit params override.
     A cryptographically valid read receipt is refused if the protocol
     version moved since it was issued. Fires on every boot.
  2. act_pipeline.execute_plan(..., law12_proof_time=...) — execution
     boundary. The PLAN's authority grant is validated as a ProofRecord
     against auto-resolved current state (plus the fresh re-resolution's
     grant standing). Stale grant refuses with LAW_AUTHORITY_PROOF_STALE.
     Without law12_proof_time the check is skipped (staleness cannot be
     established without proof-time values — precise, never speculative).
  3. quality_gate.check_delivery(..., law12_proof_time=...) — delivery
     boundary. A scorecard whose scored code moved is refused as stale.
     Current state auto-resolves; without law12_proof_time the check is
     skipped.

Scope-based precision: each dependency may carry a scope; validate_proof
accepts material_scopes to skip dependencies immaterial to a given
decision (e.g. a tip change is immaterial when the protocol text is
byte-identical). Dependencies with empty scope are always checked.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum


class ProofStatus(Enum):
    CURRENT_UNTIL_RECHECK = "CURRENT_UNTIL_RECHECK"
    STALE = "STALE"
    INVALID = "INVALID"
    NEEDS_EVIDENCE = "NEEDS_EVIDENCE"


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
        if self.status == ProofStatus.NEEDS_EVIDENCE:
            return ("NEEDS_EVIDENCE: proof declares no dependencies — "
                    "freshness cannot be established. Supply proof-time "
                    "dependencies or re-issue the proof.")
        parts = []
        for d in self.stale_dependencies:
            parts.append(f"{d.kind} changed (was {d.value[:12]})")
        for k in self.missing_dependencies:
            parts.append(f"{k} has no current value to check against")
        return "Stale: " + "; ".join(parts) if parts else "Stale: unknown cause"


def validate_proof(proof: ProofRecord,
                   current_state: dict[str, str],
                   material_scopes: set[str] | frozenset[str] | None = None
                   ) -> ProofValidation:
    """Check each dependency against current state.

    current_state maps dependency kind -> current value.
    A dependency is stale if its current value differs from proof time.
    A dependency with no current value is missing (cannot confirm) — the
    proof is STALE, not current, because freshness cannot be established.

    A proof with NO dependencies is NEEDS_EVIDENCE (fail closed): a
    dependency-free proof is a vacuous pass — freshness cannot be
    established from nothing, so the boundary must not proceed on it.

    Precise invalidation, two levels:
    1. Kind level: only the dependencies listed on the proof are checked.
       An unrelated world change (a kind not in the proof's list) cannot
       invalidate this proof.
    2. Scope level: when material_scopes is given, dependencies carrying a
       non-empty scope outside that set are skipped — the caller declares
       which scopes are material to THIS decision (e.g. a tip change is
       immaterial when the protocol text is byte-identical). Dependencies
       with empty scope are always checked (global to the proof).
       material_scopes=None (default) checks every dependency.
    """
    if proof.status == ProofStatus.INVALID:
        # INVALID is terminal: mark_invalid means the proof was wrong at
        # issue or a dependency was revoked. Re-validation must not
        # resurrect it — issue a new proof instead.
        return ProofValidation(
            proof_id=proof.proof_id,
            status=ProofStatus.INVALID,
        )

    if not proof.dependencies:
        proof.status = ProofStatus.NEEDS_EVIDENCE
        proof.invalidated_by = ["NEEDS_EVIDENCE: no dependencies declared"]
        return ProofValidation(
            proof_id=proof.proof_id,
            status=ProofStatus.NEEDS_EVIDENCE,
        )

    stale: list[ProofDependency] = []
    missing: list[str] = []
    skipped_scopes: list[str] = []

    for dep in proof.dependencies:
        if (material_scopes is not None and dep.scope
                and dep.scope not in material_scopes):
            skipped_scopes.append(f"{dep.kind}:{dep.scope}")
            continue
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

def proof_from_read_receipt(receipt, source_sha: str | None = None) -> ProofRecord:
    """A read receipt is valid for the protocol version and tip it was read at.

    If the protocol version changes, the receipt is stale (re-read required).
    If the tip moves, the receipt is NOT automatically stale — the protocol
    text the agent read may be unchanged. Tip staleness is scoped: only
    invalidate on tip change if the protocol files themselves changed.
    The tip dependency is recorded with scope "protocol_files" (so callers
    can declare it immaterial via material_scopes) and ONLY when the caller
    actually knows the read-time tip — a fabricated "" would make the check
    vacuous (self-referential match) or spuriously stale.
    """
    deps = [
        ProofDependency(DEP_POLICY_REF, receipt.protocol_version,
                        scope="protocol_text"),
    ]
    if source_sha:
        deps.append(ProofDependency(DEP_SOURCE_SHA, source_sha,
                                    scope="protocol_files"))
    return ProofRecord(
        proof_id=f"read-receipt:{receipt.agent_id}:{receipt.receipt_hash[:12]}",
        proof_type="read_receipt",
        dependencies=deps,
        issued_at=receipt.issued_at,
    )


def proof_from_scorecard(scorecard, source_sha: str = "",
                         policy_ref: str = "") -> ProofRecord:
    """A scorecard is valid for the code it scored and the policy in force.

    Empty values are skipped, not recorded: a dependency on "" can never
    honestly match. A proof left with no dependencies validates as
    NEEDS_EVIDENCE (fail closed).

    Evidence refs (test runs, artifacts) are recorded when present in the
    evidence field; callers may add DEP_EVIDENCE_REF dependencies for
    specific run IDs they can re-resolve.
    """
    deps = []
    if source_sha:
        deps.append(ProofDependency(DEP_SOURCE_SHA, source_sha,
                                    scope="scored_code"))
    if policy_ref:
        deps.append(ProofDependency(DEP_POLICY_REF, policy_ref,
                                    scope="scoring_rubric"))
    return ProofRecord(
        proof_id=f"scorecard:{scorecard.what[:40]}",
        proof_type="scorecard",
        dependencies=deps,
    )


def proof_from_authority(authority_receipt_id: str, source_sha: str = "",
                         policy_ref: str = "") -> ProofRecord:
    """An authority grant is valid while the grant stands and policy holds.

    Revocation is modeled as INVALID (not STALE): mark_invalid when the
    grant is revoked. The execution door must check revocation at execution
    time, not just at planning time.

    Empty source_sha/policy_ref are skipped (see proof_from_scorecard).
    """
    deps = [
        ProofDependency(DEP_AUTHORITY_RECEIPT, authority_receipt_id,
                        scope="grant"),
    ]
    if source_sha:
        deps.append(ProofDependency(DEP_SOURCE_SHA, source_sha,
                                    scope="grant_scope"))
    if policy_ref:
        deps.append(ProofDependency(DEP_POLICY_REF, policy_ref,
                                    scope="grant_policy"))
    return ProofRecord(
        proof_id=f"authority:{authority_receipt_id}",
        proof_type="authority",
        dependencies=deps,
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
                             current_state: dict[str, str],
                             material_scopes: set[str] | frozenset[str] | None = None
                             ) -> BoundaryCheck:
    """Law 12 enforcement at a consequential execution boundary.

    Validate every proof the action depends on. If ANY is stale, invalid,
    or needs evidence, do not proceed on the old proof — recheck or
    reverify first.

    This is the check the spec requires "at every consequential execution
    boundary": plan → execute, merge, deploy, promote, authorize.
    """
    validations = [validate_proof(p, current_state, material_scopes)
                   for p in proofs]
    proceed = all(v.is_current for v in validations)
    return BoundaryCheck(proceed=proceed, validations=validations)


def resolve_current_state(repo_root: str | None = None) -> dict[str, str]:
    """Best-effort resolution of the current world state for Law 12 checks.

    Returns {"source_sha": <git HEAD or "">, "policy_ref": <PROTOCOL_VERSION>}.
    The policy ref is a module constant and always resolves; the tip needs
    a git checkout and is best-effort. Never raises: on git failure the tip
    is "" (callers then treat source_sha deps as missing -> STALE, fail
    closed — honest, never a silent pass).
    """
    state: dict[str, str] = {}
    state["policy_ref"] = _current_protocol_version()
    tip = _git_head(repo_root)
    if tip:
        state["source_sha"] = tip
    return state


def _current_protocol_version() -> str:
    """Current PROTOCOL_VERSION, robust to however this module was imported.

    proof_expiry is imported both as kernel.protocol.proof_expiry and as a
    top-level module (tests insert kernel/protocol on sys.path), so the
    read_receipt module is located by relative import first, then by
    absolute module name. Returns "" only if every path fails.
    """
    import importlib
    for name in (
            __package__ + ".read_receipt" if __package__ else "",
            "read_receipt",
            "kernel.protocol.read_receipt",
    ):
        if not name:
            continue
        try:
            mod = importlib.import_module(name)
            v = getattr(mod, "PROTOCOL_VERSION", "")
            if isinstance(v, str) and v:
                return v
        except Exception:
            continue
    return ""


def _git_head(repo_root: str | None = None) -> str:
    """Best-effort `git rev-parse HEAD`. Returns "" on any failure."""
    import subprocess
    from pathlib import Path
    candidates: list[str] = []
    if repo_root:
        candidates.append(repo_root)
    # The repo containing this file: kernel/protocol/proof_expiry.py -> up 3.
    try:
        candidates.append(str(Path(__file__).resolve().parents[2]))
    except Exception:
        pass
    candidates.append(".")
    for cwd in candidates:
        try:
            r = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=cwd, capture_output=True, text=True, timeout=10,
            )
            head = (r.stdout or "").strip()
            if r.returncode == 0 and len(head) == 40 and all(
                    c in "0123456789abcdef" for c in head):
                return head
        except Exception:
            continue
    return ""
