#!/usr/bin/env python3
"""Normalize ChatGPT-produced candidate actions into the Naya Power kernel contract.

This is deliberately provider-neutral: the host supplies structured candidates;
the adapter strips untrusted verification claims and validates the machine shape.
"""
from __future__ import annotations

from typing import Any

REQUIRED = {
    "id", "description", "expected_benefit", "necessary_cost", "risk_loss",
    "authorization", "boundary_violations", "evidence_state", "reversible",
    "governance_sensitive",
}
ALLOWED_AUTHORITY = {"approved", "denied", "unknown"}
ALLOWED_EVIDENCE = {"UNKNOWN", "IMPLEMENTED", "TESTED", "VERIFIED", "RUNTIME-PROVEN", "PRODUCTION-PROVEN"}


def normalize_candidates(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for raw in candidates:
        missing = sorted(REQUIRED - raw.keys())
        if missing:
            raise ValueError(f"candidate {raw.get('id', '<unknown>')} missing: {', '.join(missing)}")
        item = dict(raw)
        if item["authorization"] not in ALLOWED_AUTHORITY:
            raise ValueError(f"candidate {item['id']} has invalid authorization")
        if item["evidence_state"] not in ALLOWED_EVIDENCE:
            raise ValueError(f"candidate {item['id']} has invalid evidence_state")
        for field in ("expected_benefit", "necessary_cost", "risk_loss"):
            value = item[field]
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= value <= 100:
                raise ValueError(f"candidate {item['id']} has invalid {field}")
        if not isinstance(item["boundary_violations"], list):
            raise ValueError(f"candidate {item['id']} boundary_violations must be a list")
        if not isinstance(item["reversible"], bool) or not isinstance(item["governance_sensitive"], bool):
            raise ValueError(f"candidate {item['id']} boolean fields are invalid")

        # Model-supplied claims are never promoted to evidence by this adapter.
        if raw.get("model_claimed_verified") is True and item["evidence_state"] in {"VERIFIED", "RUNTIME-PROVEN", "PRODUCTION-PROVEN"}:
            if not raw.get("evidence"):  # explicit evidence object/list is required
                item["evidence_state"] = "IMPLEMENTED"
        item.pop("model_claimed_verified", None)
        item.pop("verification_claim", None)
        normalized.append(item)
    return normalized


def build_request(base_request: dict[str, Any], model_candidates: list[dict[str, Any]]) -> dict[str, Any]:
    request = dict(base_request)
    request["candidates"] = normalize_candidates(model_candidates)
    return request


if __name__ == "__main__":
    demo = [{
        "id": "chatgpt-candidate",
        "description": "Perform the verified next implementation action.",
        "expected_benefit": 95,
        "necessary_cost": 15,
        "risk_loss": 5,
        "authorization": "approved",
        "boundary_violations": [],
        "evidence_state": "VERIFIED",
        "reversible": True,
        "governance_sensitive": False,
        "model_claimed_verified": True,
    }]
    print(build_request({"request_id": "CHATGPT-HOST-SMOKE", "constitution_version": "1.0.0"}, demo))
