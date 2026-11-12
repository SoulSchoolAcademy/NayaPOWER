#!/usr/bin/env python3
"""Migrate v1.0 seed blocks to the canonical v1.1 contract.

Reads each IB-NNNN.json, normalizes to v1.1, writes back in place.
Honest about what it cannot decide: owner_id is left EMPTY with an explicit
pending flag — validation fails loudly until a human assigns ownership.
Never invents an owner identity.

Usage: python3 migrate_v10_to_v11.py [--check] [--apply]
  --check: report what would change, don't write
  --apply: write migrated blocks
"""
import copy
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ib_reconcile import normalize_file_block, validate_v11

BLOCKS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "blocks")


def migrate_block(block):
    b = normalize_file_block(copy.deepcopy(block),
                             default_owner_id="",
                             default_owner_scope="TEAM")
    # Seed blocks are team standing laws from AGENTS.md -> TEAM scope.
    # Owner identity is a human decision; flag it loudly, don't invent it.
    b["owner_scope"] = "TEAM"
    prov = b.get("provenance") or {}
    prov["owner_assignment_pending"] = True
    prov["migration"] = "v1.0 -> v1.1 canonical contract (P0-A, 2026-10-11)"
    prov["aliases"] = [block.get("id")] if block.get("id") else []
    b["provenance"] = prov
    # purpose: derive from title when absent
    if not b.get("purpose"):
        b["purpose"] = f"Standing team law: {b.get('title', '')}"
    return b


def main():
    apply = "--apply" in sys.argv
    files = sorted(f for f in os.listdir(BLOCKS_DIR)
                   if f.startswith("IB-") and f.endswith(".json")
                   and f not in ("REGISTRY.json",))
    print(f"Found {len(files)} seed blocks")
    needs_owner = 0
    for fname in files:
        path = os.path.join(BLOCKS_DIR, fname)
        with open(path) as f:
            original = json.load(f)
        if original.get("schema_version") == "1.1":
            print(f"  {fname}: already v1.1, skipping")
            continue
        migrated = migrate_block(original)
        problems = validate_v11(migrated)
        owner_problems = [p for p in problems if "owner_id" in p]
        other_problems = [p for p in problems if "owner_id" not in p]
        needs_owner += 1 if owner_problems else 0
        status = "APPLY" if apply else "CHECK"
        print(f"  [{status}] {fname}: v1.0 -> v1.1 "
              f"(owner_pending={bool(owner_problems)}, other_problems={len(other_problems)})")
        for p in other_problems:
            print(f"      ! {p}")
        if apply:
            with open(path, "w") as f:
                json.dump(migrated, f, indent=2, ensure_ascii=False)
                f.write("\n")
    print()
    print(f"Blocks needing owner assignment: {needs_owner}/{len(files)}")
    print("Owner assignment is a human decision (Shawn). Run validation to see the list:")
    print("  python3 -c \"from ib_reconcile import validate_v11; ...\"")


if __name__ == "__main__":
    main()
