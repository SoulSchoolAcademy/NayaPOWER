"""Explicit Naya identity, owner, and runtime-session binding semantics.

The canonical Naya identity is durable application identity. A Supabase Auth
session is an ephemeral authorization mechanism and MUST NOT redefine it.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BindingContext:
    naya_id: str
    owner_id: str
    runtime_subject_id: str
    session_id: str


@dataclass(frozen=True)
class RuntimeAuthorization:
    authorized: bool
    reason: str


def canonical_identity_is_stable_across_session_rotation(
    before: BindingContext,
    after: BindingContext,
) -> bool:
    """Return true only when durable identity/owner remain unchanged.

    Session IDs may rotate. Runtime subject may also change when an explicit
    delegation mechanism exists. Neither event is allowed to mutate naya_id.
    """
    return (
        before.naya_id == after.naya_id
        and before.owner_id == after.owner_id
    )


def resolve_runtime_authorization(
    *,
    naya_id: str,
    owner_id: str,
    runtime_subject_id: str,
    binding_owner_id: str | None,
    session_id: str,
) -> RuntimeAuthorization:
    """Resolve authorization without conflating session identity and Naya identity."""
    if not naya_id or not owner_id or not runtime_subject_id or not session_id:
        return RuntimeAuthorization(False, "IDENTITY_CONTEXT_INCOMPLETE")

    if binding_owner_id is None:
        if runtime_subject_id == owner_id:
            return RuntimeAuthorization(True, "DIRECT_OWNER_SESSION")
        return RuntimeAuthorization(False, "OWNER_BINDING_REQUIRED")

    if binding_owner_id != owner_id:
        return RuntimeAuthorization(False, "OWNER_BINDING_MISMATCH")

    return RuntimeAuthorization(True, "EXPLICIT_OWNER_BINDING")
