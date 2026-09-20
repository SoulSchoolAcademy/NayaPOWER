#!/usr/bin/env python3
"""Thin CCT -> Superbrain coordination boundary.

Composes existing CCT block verification and Naya claim authorization. It does
not redefine either authority. A verified, authorized intelligence block may
inform a single executable next-action only when the active claim is current,
non-conflicting, and the action is explicitly bound to both artifacts.
"""
from __future__ import annotations

from typing import Any

from cct_intelligent_block import verify_block
from naya_claim import Claim, authorize_write


class CoordinationRejected(ValueError):
    """Raised when collective intelligence cannot safely become executable work."""


_REQUIRED_ACTION = {"action_id", "objective", "instruction", "acceptance", "claim_work_id", "block_id"}


def coordinate_next_action(
    block: dict[str, Any],
    *,
    consumer: str,
    claim: Claim,
    current_commit: str,
    existing_claims: list[Claim],
    next_action: dict[str, Any],
    now: str | None = None,
) -> dict[str, Any]:
    """Return a bound executable action or fail closed.

    CCT owns block trust/permission; Naya claims own write authorization. This
    function only composes those decisions and binds their identities into the
    resulting execution artifact.
    """
    decision = verify_block(block, consumer=consumer, purpose="execute")
    if not decision.allowed:
        raise CoordinationRejected("CCT block rejected: " + decision.reason)

    allowed, reason = authorize_write(
        claim, current_commit=current_commit, existing=existing_claims, now=now
    )
    if not allowed:
        raise CoordinationRejected("claim rejected: " + reason)

    if not isinstance(next_action, dict):
        raise CoordinationRejected("next_action must be an object")
    missing = sorted(_REQUIRED_ACTION - set(next_action))
    if missing:
        raise CoordinationRejected("next_action missing required fields: " + ", ".join(missing))
    if any(not isinstance(next_action[field], str) or not next_action[field].strip() for field in _REQUIRED_ACTION):
        raise CoordinationRejected("next_action fields must be non-empty strings")
    if next_action["claim_work_id"] != claim.work_id:
        raise CoordinationRejected("next_action is not bound to the active claim")
    if next_action["block_id"] != block["block_id"]:
        raise CoordinationRejected("next_action is not bound to the verified CCT block")

    return {
        "schema": "naya/cct/superbrain-coordination/v1",
        "action_id": next_action["action_id"],
        "objective": next_action["objective"],
        "instruction": next_action["instruction"],
        "acceptance": next_action["acceptance"],
        "claim_work_id": claim.work_id,
        "block_id": block["block_id"],
        "consumer": consumer,
        "base_commit": current_commit,
    }
