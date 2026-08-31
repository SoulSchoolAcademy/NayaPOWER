#!/usr/bin/env python3
"""Adversarial tests for Naya-to-Naya execution claiming."""
from __future__ import annotations

import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".naya" / "control-plane"))
import claiming  # noqa: E402


def base_registry() -> dict:
    return json.loads((ROOT / ".naya" / "control-plane" / "CLAIMS.json").read_text(encoding="utf-8"))


def claim(cid: str, block: str, owner: str, scope: str, head: str, minutes: int = 30) -> dict:
    now = datetime.now(timezone.utc)
    return {
        "claim_id": cid,
        "block_id": block,
        "owner": owner,
        "scope": [scope],
        "start_head": head,
        "status": "ACTIVE",
        "started_at": now.isoformat(),
        "last_update": now.isoformat(),
        "expires_at": (now + timedelta(minutes=minutes)).isoformat(),
    }


def expect_red(registry: dict, fragment: str, **kwargs) -> None:
    try:
        claiming.validate(registry, **kwargs)
    except AssertionError as exc:
        if fragment not in str(exc):
            raise AssertionError(f"expected {fragment!r}, got {exc}")
        return
    raise AssertionError(f"expected RED containing {fragment!r}")


def main() -> int:
    registry = base_registry()
    head = "test-head"
    registry["claims"] = [claim("A", "B1", "Naya-A", "src/MAXIS", head)]
    claiming.validate(registry, expected_head=head)

    duplicate_block = json.loads(json.dumps(registry))
    duplicate_block["claims"].append(claim("B", "B1", "Naya-B", "docs/Naya", head))
    expect_red(duplicate_block, "multiple active owners")

    overlap = json.loads(json.dumps(registry))
    overlap["claims"].append(claim("B", "B2", "Naya-B", "src/MAXIS/results", head))
    expect_red(overlap, "overlapping active execution scopes")

    expired = json.loads(json.dumps(registry))
    expired["claims"][0]["expires_at"] = (datetime.now(timezone.utc) - timedelta(minutes=1)).isoformat()
    expect_red(expired, "active claim is expired")

    missing_owner = json.loads(json.dumps(registry))
    missing_owner["claims"][0]["owner"] = ""
    expect_red(missing_owner, "active claim requires owner")

    stale_head = json.loads(json.dumps(registry))
    expect_red(stale_head, "does not match expected head", expected_head="different-head")

    released = json.loads(json.dumps(registry))
    released["claims"][0]["status"] = "RELEASED"
    released["claims"].append(claim("B", "B1", "Naya-B", "src/MAXIS", head))
    claiming.validate(released, expected_head=head)

    print("PASS — Naya-to-Naya claiming positive and deliberate-failure tests GREEN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
