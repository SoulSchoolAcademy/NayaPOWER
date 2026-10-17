#!/usr/bin/env python3
"""
worker_entry.py — Machine-enforced entry gate for every worker shift.

Every worker MUST run this first. It decides: WORK, NO_WORK, or STAND_DOWN.
The worker obeys the verdict. No exceptions.

Usage:
    python3 tools/worker_entry.py [--json]
    python3 tools/worker_entry.py --pre-action --expected-main <40-char-main-sha> --agent-id <seat> --json

Exit codes:
    0 = NO_WORK (nothing changed, exit cleanly)
    10 = WORK_AVAILABLE (proceed with the shift)
    20 = STAND_DOWN (rate limit, stale state, or failed proof: no governed action)

This is THE PROTOCOL, step 1 (WAKE), enforced in code — not prose.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

# Paths
HOME = os.path.expanduser("~")
GOAL_DIR = os.path.join(HOME, "workspace/goals/nayapower-10-10-completion-drive/hidden_files")
LIVE_PLAN = os.path.join(GOAL_DIR, "LIVE-PLAN.md")
STAND_DOWN_FLAG = os.path.join(GOAL_DIR, "api-stand-down.flag")
BUILD_LIST = os.path.join(GOAL_DIR, "brain-build-list.json")
REPO_URL = "https://github.com/SoulSchoolAcademy/NayaPOWER.git"
REPO_ROOT = Path(__file__).resolve().parents[1]

STAND_DOWN_TTL = 3600  # 1 hour


def read_tip_from_plan():
    """Extract last-verified tip from LIVE-PLAN.md TIP NOTE section."""
    try:
        with open(LIVE_PLAN) as f:
            content = f.read()
        # Look for tip SHA in TIP NOTE section (40-char hex)
        import re
        # Find the TIP NOTE section, then the first 40-hex SHA after "tip:"
        # The machine-contract occurrence is the authority. Pass-note prose may
        # quote the "## TIP NOTE" heading textually — a prose quote must never
        # be read as the contract (2026-10-16: a prose quote in the 19:03Z pass
        # note froze the gate tip at 9f80e8e while the contract carried
        # e19a75d6, misfiring WORK_AVAILABLE on every run). Prefer the section
        # carrying the "(machine contract)" marker; fall back to the last
        # occurrence (the contract is appended last; prose quotes come earlier).
        sections = content.split("## TIP NOTE")
        if len(sections) < 2:
            return None
        section = None
        for cand in sections[1:]:
            sec = cand.split("##")[0]  # until next section
            if "machine contract" in sec:
                section = sec
                break
        if section is None:
            section = sections[-1].split("##")[0]
        match = re.search(r'\b([0-9a-f]{40})\b', section)
        if match:
            return match.group(1)
        # Fallback: short SHA
        match = re.search(r'tip[:\s]+`?([0-9a-f]{7,40})`?', section, re.IGNORECASE)
        if match:
            return match.group(1)
        return None
    except Exception:
        return None


def get_live_tip():
    """One cheap git ls-remote. Zero API cost."""
    try:
        r = subprocess.run(
            ["git", "ls-remote", REPO_URL, "refs/heads/main"],
            capture_output=True, text=True, timeout=30
        )
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip().split()[0]
        return None
    except Exception:
        return None


def check_stand_down():
    """Check if stand-down flag is active."""
    try:
        if not os.path.exists(STAND_DOWN_FLAG):
            return False
        mtime = os.path.getmtime(STAND_DOWN_FLAG)
        age = time.time() - mtime
        return age < STAND_DOWN_TTL
    except Exception:
        return False


def has_pending_work():
    """Check build list for pending items (cheap local read)."""
    try:
        with open(BUILD_LIST) as f:
            data = json.load(f)
        items = data.get("items", [])
        for item in items:
            if item.get("status") == "pending" and not item.get("blocked_by"):
                return True
        return False
    except Exception:
        return False  # Can't determine = assume no pending (fail safe toward NO_WORK)



def pre_action_readiness(expected_main, agent_id):
    """Second source read before consequential action; NOT an authority verdict.

    This only proves the worker is using a current checked-out source and has
    passed the existing mandatory boot gate. Task ownership, consent, LAW and
    action permission still belong to their canonical gates.
    """
    def hold(reason):
        return {"verdict": "STAND_DOWN", "reason": reason, "phase": "pre_action"}

    if check_stand_down():
        return hold("active stand-down flag; no remote reads or governed actions")

    if not re.fullmatch(r"[0-9a-f]{40}", expected_main or ""):
        return hold("missing or malformed full expected main SHA")
    if not re.fullmatch(r"[a-zA-Z0-9_.:-]{3,80}", agent_id or ""):
        return hold("missing or malformed agent identity")

    live_tip = get_live_tip()
    if not live_tip or not re.fullmatch(r"[0-9a-f]{40}", live_tip):
        return hold("cannot independently resolve current main")
    if live_tip != expected_main:
        return hold("main moved since first read; re-orient and rescore")

    try:
        # A current main ancestor is needed even if this worker is on a PR.
        ancestry = subprocess.run(
            ["git", "merge-base", "--is-ancestor", expected_main, "HEAD"],
            cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=15
        )
        if ancestry.returncode != 0:
            return hold("checked-out task is not based on current main")
        gate = subprocess.run(
            [sys.executable,
             str(REPO_ROOT / "kernel/protocol/protocol_integrity_gate.py"),
             "--agent-id", agent_id, "--json"],
            cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=45
        )
        if gate.returncode != 0:
            return hold("mandatory boot gate refused or could not run")
        payload = json.loads(gate.stdout)
        checks = payload.get("checks")
        if (payload.get("pass") is not True
                or not isinstance(checks, list) or not checks
                or any(x.get("pass") is not True for x in checks)):
            return hold("boot receipt did not prove all required checks")
    except (OSError, subprocess.TimeoutExpired, ValueError, TypeError,
            AttributeError):
        return hold("could not independently prove checkout and boot readiness")

    # Second remote observation is required: main may move while boot runs.
    # A stale first read cannot authorize the next action.
    if check_stand_down():
        return hold("stand-down became active during pre-action verification")
    final_tip = get_live_tip()
    if final_tip != live_tip:
        return hold("main changed or became unreachable during pre-action verification")

    return {
        "verdict": "PRE_ACTION_READY_FOR_LAW",
        "phase": "pre_action",
        "agent_id": agent_id,
        "main_sha": live_tip,
        "authority": "NOT_GRANTED",
        "reason": "fresh source and existing boot proven; LAW, owner, consent and ACT still required",
    }


def main():
    if "--pre-action" in sys.argv:
        parser = argparse.ArgumentParser(description="Recheck source and boot before a governed action")
        parser.add_argument("--pre-action", action="store_true")
        parser.add_argument("--expected-main", required=True)
        parser.add_argument("--agent-id", required=True)
        parser.add_argument("--json", action="store_true")
        args = parser.parse_args()
        result = pre_action_readiness(args.expected_main, args.agent_id)
        if args.json:
            print(json.dumps(result))
        else:
            print(f"{result['verdict']}: {result['reason']}")
        sys.exit(10 if result["verdict"] == "PRE_ACTION_READY_FOR_LAW" else 20)

    as_json = "--json" in sys.argv

    # Gate 1: Stand-down flag
    if check_stand_down():
        result = {"verdict": "STAND_DOWN", "reason": "API rate limit active, zero API calls this shift"}
        if as_json:
            print(json.dumps(result))
        else:
            print("STAND_DOWN: API rate limit flag active. Exit immediately.")
        sys.exit(20)

    # Gate 2: Cheap tip check
    plan_tip = read_tip_from_plan()
    live_tip = get_live_tip()

    if live_tip is None:
        # Missing fresh source is not permission to start a consequential shift.
        result = {"verdict": "STAND_DOWN", "reason": "could not verify current main; read more before acting"}
        if as_json:
            print(json.dumps(result))
        else:
            print("STAND_DOWN: cannot verify current main.")
        sys.exit(20)

    tips_match = plan_tip and live_tip.startswith(plan_tip[:7]) if plan_tip else False
    pending = has_pending_work()

    if tips_match and not pending:
        result = {
            "verdict": "NO_WORK",
            "reason": "tip unchanged and no pending work",
            "tip": live_tip[:10],
        }
        if as_json:
            print(json.dumps(result))
        else:
            print(f"NO_WORK: tip {live_tip[:10]} unchanged, no pending work. Exit cleanly.")
        sys.exit(0)
    else:
        reasons = []
        if not tips_match:
            reasons.append(f"tip moved ({plan_tip[:7] if plan_tip else 'unknown'} → {live_tip[:7]})")
        if pending:
            reasons.append("pending work items exist")
        result = {
            "verdict": "WORK_AVAILABLE",
            "reason": "; ".join(reasons),
            "live_tip": live_tip,
            "plan_tip": plan_tip,
        }
        if as_json:
            print(json.dumps(result))
        else:
            print(f"WORK_AVAILABLE: {'; '.join(reasons)}")
        sys.exit(10)


if __name__ == "__main__":
    main()
