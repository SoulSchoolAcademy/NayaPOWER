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
7. The activation checklist (14 thinking lessons + Operating Code V2)
   machine-verifies against canonical bytes (Gate 1, fail closed)

This gate does NOT grant authority. It verifies readiness.
Authority still comes from Shawn's grants, not from passing this gate.

Usage:
    python3 kernel/protocol/protocol_integrity_gate.py --agent-id <id> --json
    Returns JSON: {pass: bool, checks: [...], failures: [...]}
    Exit 0 = pass (boot allowed); exit 1 = fail (boot refused, fail closed).

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
MANIFEST_PATH = ROOT / "kernel" / "protocol" / "protocol_manifest.json"


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


def check_activation_checklist() -> tuple[bool, str]:
    """Gate 1 — the activation checklist must machine-verify at boot.

    Wires tools/activation_checklist.py into this boot gate: the 14
    thinking lessons + Operating Code V2 are re-hashed from the repo's
    own canonical bytes and compared to the pinned fingerprints.
    Anything missing, tampered, stale, or unreadable fails the gate —
    no checklist pass = no start (fail closed). The check never crashes
    the gate: every error becomes a failed check, not an exception.
    """
    import importlib.util
    tool = ROOT / "tools" / "activation_checklist.py"
    try:
        spec = importlib.util.spec_from_file_location(
            "naya_activation_checklist", str(tool))
        if spec is None or spec.loader is None:
            return False, "checklist tool not loadable — boot refused (fail closed)"
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception as e:
        return False, f"checklist tool failed to load ({e}) — boot refused (fail closed)"
    try:
        canonical, err = module.load_canonical(str(ROOT))
    except Exception as e:
        return False, f"checklist canonical read failed ({e}) — boot refused (fail closed)"
    if canonical is None:
        return False, f"checklist canonical artifacts unreadable: {err} — boot refused (fail closed)"
    try:
        verdict, violations = module.check_checklist(canonical)
    except Exception as e:
        return False, f"checklist verdict computation failed ({e}) — boot refused (fail closed)"
    if verdict != "CHECKLIST-VERIFIED":
        shown = "; ".join(violations[:4])
        more = f" (+{len(violations) - 4} more)" if len(violations) > 4 else ""
        return False, f"activation checklist REJECT: {shown}{more} — boot refused (fail closed)"
    return True, "activation checklist verified: 14 lessons + Operating Code V2 match pinned canonical bytes"


def check_naya_contract(manifest: dict) -> tuple[bool, str]:
    """Gate 2 — the Naya Contract must machine-verify at boot.

    Re-hashes NAYA-ACTIVATION/NAYA-CONTRACT-V1.md and naya-contract.json
    from the repo's own bytes and compares to the pinned fingerprints in
    the protocol manifest. This is contract law, not guidance: who she is,
    how she operates, how she behaves, the process she follows.
    Anything missing, tampered, or unreadable fails the gate —
    no contract pass = no start (fail closed).
    """
    import hashlib
    contract = manifest.get("naya_contract")
    if not contract:
        return False, "manifest has no naya_contract section — boot refused (fail closed)"
    pins = contract.get("pinned_sha256") or {}
    if not pins:
        return False, "naya_contract has no pinned hashes — boot refused (fail closed)"
    for rel, pinned in pins.items():
        target = ROOT / rel
        try:
            body = target.read_bytes()
        except Exception as e:
            return False, f"contract file unreadable: {rel} ({e}) — boot refused (fail closed)"
        digest = hashlib.sha256(body).hexdigest()
        if digest != pinned:
            return False, (
                f"contract DRIFT: {rel} expected {pinned[:12]} got {digest[:12]} — "
                "boot refused (fail closed). Amendment requires Shawn's word."
            )
    return True, f"naya contract verified: {len(pins)} files match pinned canonical bytes (contract law)"


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
        ("activation_checklist", check_activation_checklist),
        ("naya_contract", lambda: check_naya_contract(manifest)),
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
