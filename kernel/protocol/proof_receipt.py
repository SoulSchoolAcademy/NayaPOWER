"""
proof_receipt.py — Law 12 enforcement: proofs expire on material change.

Per the Naya Code enforcement spec (Naya 1, 2026-10-11): "Receipts bind exact
SHA, law/profile version, resource state, scope, time/revocation; invalidate
on relevant change." And: "Proofs expire when the world changes. Not by time
— by change. Re-prove when things move."

A proof receipt is an immutable, integrity-bound record of a LAW verdict that
names the exact world it was proven against. check_proof_validity() is the
Law 12 runtime gate: it refuses to honor a receipt whose bound world has
moved in any MATERIAL way, and it does NOT invalidate on immaterial change
(description text, display names). Unknown never becomes valid: unbound
fields are recorded as UNBOUND in the receipt, never silently assumed.

Invalidation taxonomy (invalidation_event strings):
  SOURCE_SHA_MOVED        the exact source commit the proof bound has moved
  POLICY_VERSION_CHANGED  the governing law/policy version changed
  POLICY_HASH_CHANGED     the policy bytes changed under the same version
  RESOURCE_STATE_CHANGED  the target resource's state digest changed
  SCOPE_MISMATCH          the receipt's scope does not cover the current scope
  REVOKED                 the receipt's revocation reference was exercised
  EXPIRED                 now is past the receipt's validity window
  INTEGRITY_TAMPERED      the receipt bytes do not match their integrity digest

Tampering with the receipt is itself an invalidation, never a bypass.
"""
from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass, field


# Unbound sentinel: the field was not bound at issuance. Recorded openly;
# the validity check treats unbound fields as non-comparable, never as
# silently-valid.
UNBOUND = "UNBOUND"

# LAW_POLICY_VERSION — the canonical version of the governing law/policy
# bound into every Law 12 proof receipt. The machine twin of the Twelve
# Laws as pinned by the director (canonical: #2154 comment 6110527301,
# 2026-10-11). It is a version STRING, not "CURRENT": "CURRENT" can never
# change, so a proof bound to it could never expire on a law change.
# Bump this string whenever the governing law/policy text changes —
# outstanding proofs issued under the old version invalidate on
# revalidation (Law 12: proofs expire when the world changes, and the
# law is part of the world).
LAW_POLICY_VERSION = "2026-10-11-twelve-laws"

# Invalidation events.
SOURCE_SHA_MOVED = "SOURCE_SHA_MOVED"
POLICY_VERSION_CHANGED = "POLICY_VERSION_CHANGED"
POLICY_HASH_CHANGED = "POLICY_HASH_CHANGED"
RESOURCE_STATE_CHANGED = "RESOURCE_STATE_CHANGED"
SCOPE_MISMATCH = "SCOPE_MISMATCH"
REVOKED = "REVOKED"
EXPIRED = "EXPIRED"
INTEGRITY_TAMPERED = "INTEGRITY_TAMPERED"
# T-19 (Evidence Binding Law): a mandatory binding left UNBOUND, or a bound
# assumption set that changed since the proof was issued.
MISSING_BINDING = "MISSING_BINDING"
ASSUMPTION_CHANGED = "ASSUMPTION_CHANGED"

# REQUIRED_BINDINGS — which receipt fields are MANDATORY for each operation.
# A mandatory field left UNBOUND fails validation outright (MISSING_BINDING):
# an unbound mandatory field is not "unknown, therefore fine" — it is
# "unproven, therefore blocked." The machine rule: same claim, same
# authorized scope, same relevant target and conditions, valid supporting
# proof — otherwise recheck before acting.
#
# "*" is the default for any operation not named explicitly.
REQUIRED_BINDINGS = {
    # Identity fields are always mandatory: a proof must say who, what,
    # where, and on what.
    "*": ("actor_id", "operation", "environment", "resource"),
    # Deploying code: must pin the exact commit and the governing policy.
    "deploy": (
        "actor_id", "operation", "environment", "resource",
        "source_sha", "policy_version", "scope",
    ),
    # Protected writes: must pin exact source, live resource state, scope.
    "write": (
        "actor_id", "operation", "environment", "resource",
        "source_sha", "resource_state_digest", "scope",
    ),
    "delete": (
        "actor_id", "operation", "environment", "resource",
        "source_sha", "resource_state_digest", "scope",
    ),
    # Reads: identity only — the content proof carries the weight.
    "read": ("actor_id", "operation", "environment", "resource"),
}


def required_bindings_for(operation: str) -> tuple[str, ...]:
    """The mandatory binding fields for an operation. Unknown operations
    fall back to the "*" default — never to an empty set."""
    return REQUIRED_BINDINGS.get(operation, REQUIRED_BINDINGS["*"])

# Re-verification outcomes.
STILL_VALID = "STILL_VALID"
RECHECK = "RECHECK"      # dependencies changed: re-run the gate, do not trust
REVERIFY = "REVERIFY"    # material change: the proof must be re-earned


@dataclass(frozen=True)
class ProofReceipt:
    """Immutable proof receipt bound to the exact world it was proven against.

    Fields per the enforcement spec's audit receipt schema (core subset):
      receipt_id: immutable event ID (uuid4 hex).
      actor_id: who the verdict governed (credential reference, privacy-safe).
      operation / environment / resource: what was judged.
      law_verdict: ADMISSIBLE | NEEDS_AUTHORITY | NEEDS_EVIDENCE | PROHIBITED.
      reason_ids: the gate's reason codes.
      policy_version / policy_hash: which law/profile governed, byte-pinned.
      source_sha: exact source commit the proof was earned against (or UNBOUND).
      resource_state_digest: state of the target at proof time (or UNBOUND).
      scope: the authority scope covered.
      evidence_ids: input evidence receipt IDs the verdict rested on.
      issued_at / valid_until: epoch seconds; the proof's validity window.
      revocation_ref: reference that, when exercised, revokes the proof
        (or None).
      dependencies: tuple of (dep_kind, dep_id) the proof remains bound to.
      assumptions_digest: digest of the bound assumption set (data categories,
        consent requirements, retention limits, policy version — anything the
        proof's validity depends on). UNBOUND when the proof binds no
        assumptions; a changed digest invalidates (ASSUMPTION_CHANGED).
      superseded_by: receipt_id of the receipt that replaced this one, or None.
      integrity: sha256 over the canonical serialization of all fields above.
    """
    receipt_id: str
    actor_id: str
    operation: str
    environment: str
    resource: str
    law_verdict: str
    reason_ids: tuple[str, ...] = ()
    policy_version: str = UNBOUND
    policy_hash: str = UNBOUND
    source_sha: str = UNBOUND
    resource_state_digest: str = UNBOUND
    scope: str = UNBOUND
    evidence_ids: tuple[str, ...] = ()
    issued_at: float = 0.0
    valid_until: float | None = None
    revocation_ref: str | None = None
    dependencies: tuple[tuple[str, str], ...] = ()
    assumptions_digest: str = UNBOUND
    superseded_by: str | None = None
    integrity: str = ""

    def _canonical(self) -> str:
        payload = {
            "receipt_id": self.receipt_id,
            "actor_id": self.actor_id,
            "operation": self.operation,
            "environment": self.environment,
            "resource": self.resource,
            "law_verdict": self.law_verdict,
            "reason_ids": list(self.reason_ids),
            "policy_version": self.policy_version,
            "policy_hash": self.policy_hash,
            "source_sha": self.source_sha,
            "resource_state_digest": self.resource_state_digest,
            "scope": self.scope,
            "evidence_ids": list(self.evidence_ids),
            "issued_at": self.issued_at,
            "valid_until": self.valid_until,
            "revocation_ref": self.revocation_ref,
            "dependencies": [list(d) for d in self.dependencies],
            "assumptions_digest": self.assumptions_digest,
            "superseded_by": self.superseded_by,
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":"))

    def integrity_ok(self) -> bool:
        """The receipt bytes match their integrity digest. Tamper -> False."""
        if not self.integrity:
            return False
        return hashlib.sha256(self._canonical().encode()).hexdigest() == self.integrity


def issue_proof_receipt(
    *,
    actor_id: str,
    operation: str,
    environment: str,
    resource: str,
    law_verdict: str,
    reason_ids: tuple[str, ...] = (),
    policy_version: str = UNBOUND,
    policy_hash: str = UNBOUND,
    source_sha: str = UNBOUND,
    resource_state_digest: str = UNBOUND,
    scope: str = UNBOUND,
    evidence_ids: tuple[str, ...] = (),
    issued_at: float,
    valid_until: float | None = None,
    revocation_ref: str | None = None,
    dependencies: tuple[tuple[str, str], ...] = (),
    assumptions_digest: str = UNBOUND,
) -> ProofReceipt:
    """Issue a Law-12-bound proof receipt. The receipt is immutable once
    issued; its integrity digest is computed over the canonical serialization
    so any later mutation is detectable."""
    receipt = ProofReceipt(
        receipt_id=uuid.uuid4().hex,
        actor_id=actor_id,
        operation=operation,
        environment=environment,
        resource=resource,
        law_verdict=law_verdict,
        reason_ids=tuple(reason_ids),
        policy_version=policy_version,
        policy_hash=policy_hash,
        source_sha=source_sha,
        resource_state_digest=resource_state_digest,
        scope=scope,
        evidence_ids=tuple(evidence_ids),
        issued_at=issued_at,
        valid_until=valid_until,
        revocation_ref=revocation_ref,
        dependencies=tuple(dependencies),
        assumptions_digest=assumptions_digest,
    )
    digest = hashlib.sha256(receipt._canonical().encode()).hexdigest()
    return ProofReceipt(
        **{**receipt.__dict__, "integrity": digest},
    )


@dataclass(frozen=True)
class ProofContext:
    """The current world, against which a receipt's bound world is checked."""
    source_sha: str = UNBOUND
    policy_version: str = UNBOUND
    policy_hash: str = UNBOUND
    resource_state_digest: str = UNBOUND
    scope: str = UNBOUND
    assumptions_digest: str = UNBOUND
    now: float = 0.0
    revoked_refs: tuple[str, ...] = ()


def check_proof_validity(
    receipt: ProofReceipt,
    context: ProofContext,
    required_bindings: tuple[str, ...] | None = None,
) -> tuple[bool, str | None]:
    """Law 12 runtime gate. Returns (valid, invalidation_event).

    Fail-closed order, most severe first:
      0. MISSING_BINDING — a MANDATORY binding field was left UNBOUND.
         Unknown never becomes valid: if the proof does not pin what it
         must pin, it cannot be honored. (T-19 Evidence Binding Law.)
      1. INTEGRITY_TAMPERED — the receipt itself was altered. Never trusted.
      2. REVOKED — the bound revocation reference was exercised.
      3. EXPIRED — the validity window passed.
      4. SOURCE_SHA_MOVED — bound SHA differs from current SHA (both bound).
      5. POLICY_VERSION_CHANGED / POLICY_HASH_CHANGED — the governing law moved.
      6. RESOURCE_STATE_CHANGED — the target's state moved.
      7. ASSUMPTION_CHANGED — the bound assumption set changed.
      8. SCOPE_MISMATCH — the receipt's scope does not cover the current scope.

    required_bindings: the mandatory field names for this check. Defaults
    to required_bindings_for(receipt.operation). Pass an explicit tuple to
    override (e.g. a stricter profile for a consequential action).

    Non-mandatory UNBOUND fields remain non-comparable: they neither
    validate nor invalidate. Immaterial change (description text, display
    names) is not in the bound set and can never invalidate.
    """
    # 0. Mandatory bindings: UNBOUND on a required field is a hard fail.
    #    A proof that does not pin what it must pin proves nothing.
    required = (
        required_bindings
        if required_bindings is not None
        else required_bindings_for(receipt.operation)
    )
    for field_name in required:
        if getattr(receipt, field_name, UNBOUND) == UNBOUND:
            return False, MISSING_BINDING
    # 1. Tamper: a receipt that does not match its own digest is unusable.
    if not receipt.integrity_ok():
        return False, INTEGRITY_TAMPERED
    # 2. Revocation exercised.
    if receipt.revocation_ref is not None and receipt.revocation_ref in context.revoked_refs:
        return False, REVOKED
    # 3. Validity window passed.
    if receipt.valid_until is not None and context.now > receipt.valid_until:
        return False, EXPIRED
    # 4. Source SHA moved (only when both sides bound the SHA).
    if (
        receipt.source_sha != UNBOUND
        and context.source_sha != UNBOUND
        and receipt.source_sha != context.source_sha
    ):
        return False, SOURCE_SHA_MOVED
    # 5. Policy moved.
    if (
        receipt.policy_version != UNBOUND
        and context.policy_version != UNBOUND
        and receipt.policy_version != context.policy_version
    ):
        return False, POLICY_VERSION_CHANGED
    if (
        receipt.policy_hash != UNBOUND
        and context.policy_hash != UNBOUND
        and receipt.policy_hash != context.policy_hash
    ):
        return False, POLICY_HASH_CHANGED
    # 6. Resource state moved.
    if (
        receipt.resource_state_digest != UNBOUND
        and context.resource_state_digest != UNBOUND
        and receipt.resource_state_digest != context.resource_state_digest
    ):
        return False, RESOURCE_STATE_CHANGED
    # 7. Assumptions moved (T-19): the proof was earned under one set of
    #    assumptions (data categories, consent, retention, policy); the
    #    world now operates under another. The old proof cannot cover it.
    if (
        receipt.assumptions_digest != UNBOUND
        and context.assumptions_digest != UNBOUND
        and receipt.assumptions_digest != context.assumptions_digest
    ):
        return False, ASSUMPTION_CHANGED
    # 8. Scope mismatch: the receipt must cover the current scope.
    if (
        receipt.scope != UNBOUND
        and context.scope != UNBOUND
        and receipt.scope != context.scope
    ):
        return False, SCOPE_MISMATCH
    return True, None


def reverify(receipt: ProofReceipt, context: ProofContext) -> str:
    """Law 12 re-verification outcome: STILL_VALID, RECHECK, or REVERIFY.

    RECHECK: dependencies moved in a way that only requires re-running the
    gate against the same proof (e.g. policy hash drifted under same version).
    REVERIFY: the proof must be re-earned — expiry, revocation, tamper,
    or a material world move (SHA, version, resource state, scope).
    """
    valid, event = check_proof_validity(receipt, context)
    if valid:
        return STILL_VALID
    if event == POLICY_HASH_CHANGED:
        return RECHECK
    return REVERIFY


def digest_state(state: object) -> str:
    """Stable sha256 digest of a resource-state payload for binding."""
    canonical = json.dumps(state, sort_keys=True, separators=(",", ":"),
                           default=str)
    return hashlib.sha256(canonical.encode()).hexdigest()
