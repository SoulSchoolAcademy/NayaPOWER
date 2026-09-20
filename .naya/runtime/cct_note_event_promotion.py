#!/usr/bin/env python3
"""Canonical Note Event -> CCT Intelligent Block promotion boundary.

This adapter does not create a second memory system. It converts an already
canonical, verified Note Event into a portable CCT artifact only when the
source event carries sufficient evidence and an explicit network permission.
Fail closed is intentional: missing/weak verification or permission never
becomes a shareable block by inference.
"""
from __future__ import annotations

from typing import Any

from cct_intelligent_block import make_block


class PromotionRejected(ValueError):
    """Raised when a canonical event is not eligible for CCT promotion."""


def promote_note_event(event: dict[str, Any], *, producer: str, consumers: list[str], purpose: str = "consume") -> dict[str, Any]:
    if not isinstance(event, dict):
        raise PromotionRejected("canonical event must be an object")
    event_id = str(event.get("event_id", ""))
    if not event_id:
        raise PromotionRejected("canonical event_id is required")

    verification = event.get("verification") or {}
    status = str(verification.get("status", "")).upper() if isinstance(verification, dict) else ""
    if status != "VERIFIED":
        raise PromotionRejected("only VERIFIED canonical events may cross the CCT promotion boundary")

    evidence = event.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        raise PromotionRejected("verified CCT promotion requires evidence")

    provenance = event.get("provenance")
    if not isinstance(provenance, dict):
        raise PromotionRejected("canonical event provenance is required")

    if not consumers or any(not isinstance(item, str) or not item for item in consumers):
        raise PromotionRejected("explicit consumer authorization is required")

    permissions = {"consumers": list(consumers), "purposes": [purpose]}
    content = {
        "event_id": event_id,
        "type": event.get("type") or event.get("event_type"),
        "subject": event.get("subject"),
        "learning": event.get("learning"),
        "why_it_matters": event.get("why_it_matters"),
        "next_best_action": event.get("next_best_action"),
    }
    return make_block(
        block_id=f"IB-{event_id}",
        producer=producer,
        content=content,
        evidence=evidence,
        permissions=permissions,
        verification="VERIFIED",
    )
