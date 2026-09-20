#!/usr/bin/env python3
"""Small canonical bridge: Smart Note/Note Event -> CCT -> outcome/value.

This module composes existing authorities; it does not create a second memory
or event store. Canonical Note Events remain the source of truth, the existing
Note Event -> CCT promotion boundary remains the authorization boundary, and
CCT-005 remains the outcome/value primitive.
"""
from __future__ import annotations

from typing import Any

from cct_intelligent_block import verify_block
from cct005_value_feedback import make_outcome, value_signal, verify_outcome
from cct_note_event_promotion import PromotionRejected, promote_note_event


class IntegrationRejected(ValueError):
    """Raised when the canonical Smart Note/Event cannot enter the value loop."""


def _is_canonical_smart_note(event: dict[str, Any]) -> bool:
    event_id = event.get("event_id")
    if not isinstance(event_id, str) or not event_id.startswith("SE-"):
        return False
    representations = event.get("representations")
    if not isinstance(representations, dict):
        return False
    for representation in representations.values():
        if not isinstance(representation, dict):
            continue
        note_id = representation.get("id")
        if isinstance(note_id, str) and note_id.startswith("SN-") and representation.get("canonical_event_id") == event_id:
            return True
    return False


def integrate_verified_note_event(
    event: dict[str, Any],
    *,
    producer: str,
    actor: str,
    intended_use: str,
    action: str,
    result: str,
    classification: str,
    evidence: list[dict[str, Any]],
    confidence: float,
    context: dict[str, Any],
    privacy: str,
    outcome_id: str,
    consumers: list[str] | None = None,
) -> dict[str, Any]:
    """Execute the smallest complete Smart Note -> CCT-005 value loop."""
    if not isinstance(event, dict) or not _is_canonical_smart_note(event):
        raise IntegrationRejected("input must be a canonical Smart Note/Note Event with an SN representation")
    if not isinstance(outcome_id, str) or not outcome_id:
        raise IntegrationRejected("unique outcome_id is required")
    consumers = list(consumers or [actor])
    if actor not in consumers:
        raise IntegrationRejected("actor must be explicitly authorized as a CCT consumer")

    try:
        block = promote_note_event(
            event,
            producer=producer,
            consumers=consumers,
            purpose=intended_use,
        )
    except PromotionRejected as exc:
        raise IntegrationRejected(str(exc)) from exc

    decision = verify_block(block, consumer=actor, purpose=intended_use)
    if not decision.allowed:
        raise IntegrationRejected("promoted block rejected: " + decision.reason)

    outcome = make_outcome(
        outcome_id=outcome_id,
        block_id=block["block_id"],
        actor=actor,
        intended_use=intended_use,
        action=action,
        result=result,
        classification=classification,
        evidence=evidence,
        confidence=confidence,
        context=context,
        privacy=privacy,
        provenance={"source_block": block["block_id"], "source_event": event["event_id"]},
    )
    outcome_decision = verify_outcome(outcome, block_id=block["block_id"], authorized_actor=actor)
    if not outcome_decision.allowed:
        raise IntegrationRejected("outcome rejected: " + outcome_decision.reason)

    return {
        "event_id": event["event_id"],
        "block": block,
        "outcome": outcome,
        "value": value_signal([outcome]),
    }
