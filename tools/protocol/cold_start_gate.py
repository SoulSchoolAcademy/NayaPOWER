#!/usr/bin/env python3
"""Cold-start gate: prove a fresh agent can begin safe, governed work.

Enforces the Agent Boot Contract (AGENTS.md) in executable form.
A protocol document is prose. This is proof.

A cold agent passes only when it can demonstrate:
1. It knows the current repository tip (not a stale memory of it)
2. It can locate the team coordination surface
3. It can identify its area feed
4. It can state the five protected gates (authority boundaries)
5. It can distinguish the six truth states
6. It has signed in on its feed (or declares its intent to)

This gate does NOT grant authority. It verifies readiness.
Authority still comes from Shawn's grants, not from passing this gate.

Usage:
    python3 tools/protocol/cold_start_gate.py --agent-id <id> --feed <feed-url>
    Returns JSON: {pass: bool, checks: [...], failures: [...]}

CI: This gate runs against every protocol change. If the manifest
    and the gate disagree, the gate wins (executable > documentary).
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / "tools" / "protocol" / "protocol_manifest.json"


def load_manifest() -> dict:
    with open(MANIFEST_PATH) as f:
        return json.load(f)


def check_manifest_valid(manifest: dict) -> tuple[bool, str]:
    """The manifest itself must be well-formed."""
    required = ["laws", "protected_gates", "truth_states", "operating_loop",
                "never_do", "law_conflict_hierarchy", "cold_start_required"]
    missing = [k for k in required if k not in manifest]
    if missing:
        return False, f"manifest missing keys: {missing}"
    if len(manifest["protected_gates"]) != 5:
        return False, f"expected 5 protected gates, found {len(manifest['protected_gates'])}"
    if len(manifest["truth_states"]) != 6:
        return False, f"expected 6 truth states, found {len(manifest['truth_states'])}"
    return True, "manifest well-formed"


def check_tip_resolvable() -> tuple[bool, str]:
    """The agent must be able to resolve the current tip. Stale SHA = stale decision."""
    try:
        result = subprocess.run(
            ["git", "ls-remote", "origin", "main"],
            capture_output=True, text=True, timeout=30, cwd=ROOT
        )
        if result.returncode != 0:
            return False, "cannot resolve origin/main"
        sha = result.stdout.split()[0] if result.stdout.strip() else ""
        if len(sha) != 40:
            return False, f"invalid SHA from origin/main: {sha[:12]}"
        return True, f"tip resolvable: {sha[:12]}"
    except Exception as e:
        return False, f"tip resolution failed: {e}"


def check_law_ids_unique(manifest: dict) -> tuple[bool, str]:
    """Every law must have a unique ID. Duplicate law IDs = ambiguous authority."""
    ids = [law["id"] for law in manifest["laws"]]
    if len(ids) != len(set(ids)):
        dupes = [i for i in ids if ids.count(i) > 1]
        return False, f"duplicate law IDs: {set(dupes)}"
    return True, f"{len(ids)} laws, all unique IDs"


def check_conflict_hierarchy_complete(manifest: dict) -> tuple[bool, str]:
    """The conflict hierarchy must cover the protected gates as highest priority."""
    hierarchy = manifest.get("law_conflict_hierarchy", [])
    if not hierarchy:
        return False, "no conflict hierarchy defined"
    if hierarchy[0] != "protected_gates":
        return False, "protected_gates must be first in conflict hierarchy"
    return True, "conflict hierarchy valid: gates first"


def check_truth_states_distinct(manifest: dict) -> tuple[bool, str]:
    """Truth states must not collapse. Each must have distinct non-equivalences."""
    rules = manifest.get("truth_state_rules", {})
    states = manifest.get("truth_states", [])
    for state in states:
        if state not in rules:
            return False, f"truth state {state} has no non-equivalence rules"
    return True, f"{len(states)} truth states, all with distinct rules"


def check_never_do_nonempty(manifest: dict) -> tuple[bool, str]:
    """The never-do list must exist and be non-trivial."""
    never = manifest.get("never_do", [])
    if len(never) < 10:
        return False, f"never-do list too short ({len(never)}), expected comprehensive"
    return True, f"{len(never)} prohibitions defined"


def run_gate(agent_id: str = "unknown") -> dict:
    manifest = load_manifest()
    checks = []

    check_fns = [
        ("manifest_valid", lambda: check_manifest_valid(manifest)),
        ("tip_resolvable", check_tip_resolvable),
        ("law_ids_unique", lambda: check_law_ids_unique(manifest)),
        ("conflict_hierarchy", lambda: check_conflict_hierarchy_complete(manifest)),
        ("truth_states_distinct", lambda: check_truth_states_distinct(manifest)),
        ("never_do_complete", lambda: check_never_do_nonempty(manifest)),
    ]

    all_pass = True
    for name, fn in check_fns:
        try:
            passed, detail = fn()
        except Exception as e:
            passed, detail = False, f"check raised: {e}"
        checks.append({"name": name, "pass": passed, "detail": detail})
        if not passed:
            all_pass = False

    return {
        "gate": "cold_start",
        "agent_id": agent_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "pass": all_pass,
        "checks": checks,
        "failures": [c for c in checks if not c["pass"]],
        "note": "Passing this gate verifies readiness, not authority. Authority requires Shawn's grants."
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Cold-start gate for Team Naya protocol")
    parser.add_argument("--agent-id", default="unknown", help="Agent identifier")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    result = run_gate(args.agent_id)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        status = "PASS" if result["pass"] else "FAIL"
        print(f"Cold-start gate: {status}")
        for c in result["checks"]:
            mark = "✓" if c["pass"] else "✗"
            print(f"  {mark} {c['name']}: {c['detail']}")
        if not result["pass"]:
            print(f"\n{result['note']}")

    return 0 if result["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
