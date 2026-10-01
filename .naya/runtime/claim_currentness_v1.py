"""Claim Currentness V1 production contract resolver.

Pure, read-only resolution over canonical Intelligent Block rows.
No persistence, no event authority, and no recency tie-breaking.
"""
from __future__ import annotations
from datetime import datetime
from typing import Any, Iterable

CURRENT = "CURRENT"
NO_CURRENT = "NO_CURRENT_CLAIM"
AMBIGUOUS = "AMBIGUOUS"


def _eligible(block: dict[str, Any], now: datetime, requested_scope: str) -> tuple[bool, str]:
    content = block["content"]
    truth = content.get("truth") or {}
    context = content.get("context") or {}
    time = content.get("time") or {}
    evidence = content.get("evidence") or {}
    provenance = content.get("provenance") or {}

    if block.get("status") in {"SUPERSEDED", "REJECTED"}:
        return False, block["status"]
    if block.get("understanding_state") in {"CANDIDATE", "REJECTED", "SUPERSEDED"}:
        return False, "CANDIDATE_NOT_VERIFIED" if block["understanding_state"] == "CANDIDATE" else block["understanding_state"]
    if truth.get("state") != "VERIFIED":
        return False, "TRUTH_NOT_VERIFIED"
    if truth.get("conflicts"):
        return False, "CONFLICTED"
    if block.get("superseded_by_block_id"):
        return False, "SUPERSEDED"
    valid_from = time.get("valid_from")
    valid_until = time.get("valid_until")
    if valid_from and datetime.fromisoformat(str(valid_from).replace("Z", "+00:00")) > now:
        return False, "NOT_YET_VALID"
    if valid_until and datetime.fromisoformat(str(valid_until).replace("Z", "+00:00")) <= now:
        return False, "STALE_OR_EXPIRED"
    if context.get("scope") != requested_scope:
        return False, "SCOPE_MISMATCH"
    if not evidence.get("evidence_refs") or not provenance:
        return False, "MISSING_LINEAGE"
    return True, "ELIGIBLE"


def resolve_currentness(blocks: Iterable[dict[str, Any]], now: datetime, requested_scope: str = "PRIVATE") -> dict[str, Any]:
    candidates, excluded = [], {}
    for block in blocks:
        ok, reason = _eligible(block, now, requested_scope)
        if ok:
            candidates.append(block)
        else:
            excluded[block["block_id"]] = reason

    if not candidates:
        return {"resolution": NO_CURRENT, "selected_block_id": None, "candidate_ids": [], "excluded": excluded}

    signatures = {}
    for block in candidates:
        meaning = ((block.get("content") or {}).get("meaning") or {}).get("content")
        signatures.setdefault((block.get("subject_id"), meaning), []).append(block["block_id"])

    if len(signatures) > 1:
        return {"resolution": AMBIGUOUS, "selected_block_id": None, "candidate_ids": [block["block_id"] for block in candidates], "excluded": excluded}

    return {"resolution": CURRENT, "selected_block_id": candidates[0]["block_id"], "candidate_ids": [block["block_id"] for block in candidates], "excluded": excluded}
