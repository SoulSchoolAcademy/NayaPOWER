#!/usr/bin/env python3
"""Fail-closed repository-native Naya execution claiming.

This is the first enforcement layer for Naya-to-Naya mechanism #21.
It prevents the canonical claim registry from representing overlapping active
execution scopes or multiple active owners for the same block.

It is intentionally NOT presented as a distributed real-time lock service.
The registry is a durable coordination contract consumed by repository and
future runtime/orchestrator layers.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / ".naya" / "control-plane" / "CLAIMS.json"
CLAIM_STATUSES = {"ACTIVE", "RELEASED"}
REQUIRED = {
    "claim_id", "block_id", "owner", "scope", "start_head", "status",
    "started_at", "last_update", "expires_at",
}


def fail(message: str) -> None:
    raise AssertionError(message)


def load() -> dict:
    if not REGISTRY.is_file():
        fail(f"missing canonical claim registry: {REGISTRY.relative_to(ROOT)}")
    try:
        return json.loads(REGISTRY.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid claim registry JSON: {exc}")


def parse_time(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        fail("claim timestamps must include timezone")
    return dt.astimezone(timezone.utc)


def now() -> datetime:
    return datetime.now(timezone.utc)


def git_head() -> str:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True,
            capture_output=True, check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        fail(f"cannot resolve live Git HEAD: {exc}")


def normalize_scope(value: str) -> str:
    value = value.strip().replace("\\", "/")
    while "//" in value:
        value = value.replace("//", "/")
    value = value.strip("/")
    if not value:
        fail("scope cannot be empty")
    return value


def scopes_overlap(a: str, b: str) -> bool:
    a = normalize_scope(a)
    b = normalize_scope(b)
    return a == b or a.startswith(b + "/") or b.startswith(a + "/")


def validate(registry: dict, expected_head: str | None = None,
             current_time: datetime | None = None) -> dict:
    if registry.get("$schema") != "naya/control-plane/claims/v1":
        fail("claim registry schema is not canonical")
    if registry.get("status") != "CANONICAL":
        fail("claim registry is not CANONICAL")
    policy = registry.get("policy") or {}
    for key in (
        "active_claims_must_have_owner", "active_claims_must_have_scope",
        "active_claims_must_have_start_head", "overlapping_active_scopes_are_forbidden",
        "one_active_claim_per_block", "expired_claims_are_not_valid", "release_is_explicit",
    ):
        if policy.get(key) is not True:
            fail(f"claim policy missing enforced rule: {key}")

    claims = registry.get("claims")
    if not isinstance(claims, list):
        fail("claims must be a list")

    current_time = current_time or now()
    active: list[dict] = []
    seen_ids: set[str] = set()

    for claim in claims:
        if not isinstance(claim, dict):
            fail("every claim must be an object")
        missing = REQUIRED - set(claim)
        if missing:
            fail(f"claim missing required fields: {sorted(missing)}")
        cid = str(claim["claim_id"]).strip()
        if not cid or cid in seen_ids:
            fail(f"duplicate/empty claim_id: {cid!r}")
        seen_ids.add(cid)
        status = str(claim["status"]).upper()
        if status not in CLAIM_STATUSES:
            fail(f"claim {cid}: invalid status {status}")
        scopes = claim["scope"]
        if not isinstance(scopes, list) or not scopes:
            fail(f"claim {cid}: scope must be a non-empty list")
        normalized = [normalize_scope(str(x)) for x in scopes]
        if len(normalized) != len(set(normalized)):
            fail(f"claim {cid}: duplicate scope entries")
        for timestamp in ("started_at", "last_update", "expires_at"):
            parse_time(str(claim[timestamp]))
        if status == "ACTIVE":
            if not str(claim["owner"]).strip():
                fail(f"claim {cid}: active claim requires owner")
            if not str(claim["block_id"]).strip():
                fail(f"claim {cid}: active claim requires block_id")
            if not str(claim["start_head"]).strip():
                fail(f"claim {cid}: active claim requires start_head")
            expiry = parse_time(str(claim["expires_at"]))
            if policy.get("expired_claims_are_not_valid") and expiry <= current_time:
                fail(f"claim {cid}: active claim is expired")
            if expected_head and claim["start_head"] != expected_head:
                fail(
                    f"claim {cid}: start_head {claim['start_head']} does not match expected head {expected_head}"
                )
            active.append({**claim, "scope": normalized})

    if policy.get("one_active_claim_per_block"):
        by_block: dict[str, list[str]] = {}
        for claim in active:
            by_block.setdefault(str(claim["block_id"]), []).append(str(claim["claim_id"]))
        conflicts = {b: ids for b, ids in by_block.items() if len(ids) > 1}
        if conflicts:
            fail(f"multiple active owners for block(s): {conflicts}")

    if policy.get("overlapping_active_scopes_are_forbidden"):
        for i, left in enumerate(active):
            for right in active[i + 1:]:
                for lscope in left["scope"]:
                    for rscope in right["scope"]:
                        if scopes_overlap(lscope, rscope):
                            fail(
                                "overlapping active execution scopes: "
                                f"{left['claim_id']}={lscope} vs {right['claim_id']}={rscope}"
                            )

    return {
        "status": "GREEN",
        "registry": str(REGISTRY.relative_to(ROOT)),
        "active_claim_count": len(active),
        "active_claims": [c["claim_id"] for c in active],
        "expected_head_checked": expected_head,
        "coordination_rule": "ONE ACTIVE OWNER PER BLOCK + NO OVERLAPPING ACTIVE SCOPES",
    }


def write(registry: dict) -> None:
    REGISTRY.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def claim(args: argparse.Namespace) -> int:
    registry = load()
    validate(registry)
    active = [c for c in registry["claims"] if str(c.get("status")).upper() == "ACTIVE"]
    if any(str(c.get("block_id")) == args.block for c in active):
        fail(f"block already actively claimed: {args.block}")
    new_scopes = [normalize_scope(x) for x in args.scope]
    for existing in active:
        for left in new_scopes:
            for right in existing.get("scope", []):
                if scopes_overlap(left, right):
                    fail(f"scope already claimed: {left} overlaps {right} ({existing['claim_id']})")
    current = now()
    registry["claims"].append({
        "claim_id": args.claim_id,
        "block_id": args.block,
        "owner": args.owner,
        "scope": new_scopes,
        "start_head": git_head(),
        "status": "ACTIVE",
        "started_at": current.isoformat(),
        "last_update": current.isoformat(),
        "expires_at": (current + timedelta(minutes=args.minutes)).isoformat(),
    })
    validate(registry, current_time=current)
    write(registry)
    print(json.dumps(registry["claims"][-1], indent=2))
    return 0


def release(args: argparse.Namespace) -> int:
    registry = load()
    found = False
    for item in registry["claims"]:
        if item.get("claim_id") == args.claim_id:
            if item.get("status") != "ACTIVE":
                fail(f"claim is not ACTIVE: {args.claim_id}")
            item["status"] = "RELEASED"
            item["last_update"] = now().isoformat()
            found = True
            break
    if not found:
        fail(f"claim not found: {args.claim_id}")
    validate(registry)
    write(registry)
    print(f"RELEASED={args.claim_id}")
    return 0


def self_test() -> int:
    registry = load()
    validate(registry)
    head = "self-test-head"
    fixture = json.loads(json.dumps(registry))
    t = now()
    expires = (t + timedelta(minutes=30)).isoformat()
    fixture["claims"] = [
        {
            "claim_id": "CL-TEST-A", "block_id": "B-TEST-A", "owner": "Naya-A",
            "scope": ["src/MAXIS"], "start_head": head, "status": "ACTIVE",
            "started_at": t.isoformat(), "last_update": t.isoformat(), "expires_at": expires,
        },
        {
            "claim_id": "CL-TEST-B", "block_id": "B-TEST-B", "owner": "Naya-B",
            "scope": ["src/MAXIS/results"], "start_head": head, "status": "ACTIVE",
            "started_at": t.isoformat(), "last_update": t.isoformat(), "expires_at": expires,
        },
    ]
    try:
        validate(fixture, expected_head=head, current_time=t)
    except AssertionError as exc:
        if "overlapping active execution scopes" not in str(exc):
            print(f"FAIL — wrong overlap failure: {exc}")
            return 1
    else:
        print("FAIL — overlapping active scopes were accepted")
        return 1
    fixture["claims"][1]["scope"] = ["docs/Naya"]
    result = validate(fixture, expected_head=head, current_time=t)
    print(json.dumps({"status": "GREEN", "self_test": "PASS", "positive": result}, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    v = sub.add_parser("validate")
    v.add_argument("--head", default=None)
    sub.add_parser("self-test")
    c = sub.add_parser("claim")
    c.add_argument("claim_id")
    c.add_argument("block")
    c.add_argument("owner")
    c.add_argument("scope", nargs="+")
    c.add_argument("--minutes", type=int, default=60)
    r = sub.add_parser("release")
    r.add_argument("claim_id")
    args = parser.parse_args()
    try:
        if args.command == "validate":
            head = args.head
            print(json.dumps(validate(load(), expected_head=head), indent=2))
            return 0
        if args.command == "self-test":
            return self_test()
        if args.command == "claim":
            return claim(args)
        return release(args)
    except AssertionError as exc:
        print(f"CLAIMING=RED\nFIRST_DIVERGENCE={exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
