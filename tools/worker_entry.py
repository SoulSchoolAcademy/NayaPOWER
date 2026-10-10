#!/usr/bin/env python3
"""
worker_entry.py — Machine-enforced entry gate for every worker shift.

Every worker MUST run this first. It decides: WORK, NO_WORK, or STAND_DOWN.
The worker obeys the verdict. No exceptions.

Usage:
    python3 tools/worker_entry.py [--json]

Exit codes:
    0 = NO_WORK (nothing changed, exit cleanly)
    10 = WORK_AVAILABLE (proceed with the shift)
    20 = STAND_DOWN (rate limit active, exit immediately, zero API calls)

This is THE PROTOCOL, step 1 (WAKE), enforced in code — not prose.
"""

import json
import os
import subprocess
import sys
import time

# Paths
HOME = os.path.expanduser("~")
GOAL_DIR = os.path.join(HOME, "workspace/goals/nayapower-10-10-completion-drive/hidden_files")
LIVE_PLAN = os.path.join(GOAL_DIR, "LIVE-PLAN.md")
STAND_DOWN_FLAG = os.path.join(GOAL_DIR, "api-stand-down.flag")
BUILD_LIST = os.path.join(GOAL_DIR, "brain-build-list.json")
REPO_URL = "https://github.com/SoulSchoolAcademy/NayaPOWER.git"

STAND_DOWN_TTL = 3600  # 1 hour


def read_tip_from_plan():
    """Extract last-verified tip from LIVE-PLAN.md TIP NOTE section."""
    try:
        with open(LIVE_PLAN) as f:
            content = f.read()
        # Look for tip SHA in TIP NOTE section (40-char hex)
        import re
        # Find the TIP NOTE section, then the first 40-hex SHA after "tip:"
        tip_section = content.split("## TIP NOTE")
        if len(tip_section) < 2:
            return None
        section = tip_section[1].split("##")[0]  # until next section
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


def main():
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
        # Can't check = be conservative, allow work but flag it
        result = {"verdict": "WORK_AVAILABLE", "reason": "could not verify tip, proceeding with caution", "caution": True}
        if as_json:
            print(json.dumps(result))
        else:
            print("WORK_AVAILABLE (caution): could not verify live tip.")
        sys.exit(10)

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
