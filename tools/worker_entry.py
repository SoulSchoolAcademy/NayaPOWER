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


def _surface_notifications():
    """Surface pending worker notifications (#2244 req 4). Informational only.

    Never changes the verdict, never raises. A broken outbox degrades to
    silence — activation must not depend on it.
    """
    try:
        here = os.path.dirname(os.path.abspath(__file__))
        if here not in sys.path:
            sys.path.insert(0, here)
        import notify_outbox
        audience = os.environ.get("NAYA_NOTIFY_AUDIENCE", "all")
        worker = os.environ.get("NAYA_WORKER_ID", "worker-entry")
        return notify_outbox.deliver_pending(audience, worker)
    except Exception:
        return ""


def main():
    as_json = "--json" in sys.argv

    # Notification outbox (#2244 req 4): surface pending awareness FIRST, so it
    # appears even on NO_WORK/STAND_DOWN runs. Local files only (zero API
    # calls) — safe under stand-down. Never alters the verdict below.
    notify_digest = _surface_notifications()

    def finish(result, text_line, exit_code):
        if as_json:
            if notify_digest:
                result["notifications"] = notify_digest
            print(json.dumps(result))
        else:
            if notify_digest:
                print(notify_digest)
            print(text_line)
        sys.exit(exit_code)

    # Gate 1: Stand-down flag
    if check_stand_down():
        finish({"verdict": "STAND_DOWN", "reason": "API rate limit active, zero API calls this shift"},
               "STAND_DOWN: API rate limit flag active. Exit immediately.", 20)

    # Gate 2: Cheap tip check
    plan_tip = read_tip_from_plan()
    live_tip = get_live_tip()

    if live_tip is None:
        # Can't check = be conservative, allow work but flag it
        finish({"verdict": "WORK_AVAILABLE", "reason": "could not verify tip, proceeding with caution", "caution": True},
               "WORK_AVAILABLE (caution): could not verify live tip.", 10)

    tips_match = plan_tip and live_tip.startswith(plan_tip[:7]) if plan_tip else False
    pending = has_pending_work()

    if tips_match and not pending:
        finish({"verdict": "NO_WORK", "reason": "tip unchanged and no pending work", "tip": live_tip[:10]},
               f"NO_WORK: tip {live_tip[:10]} unchanged, no pending work. Exit cleanly.", 0)
    else:
        reasons = []
        if not tips_match:
            reasons.append(f"tip moved ({plan_tip[:7] if plan_tip else 'unknown'} → {live_tip[:7]})")
        if pending:
            reasons.append("pending work items exist")
        finish({"verdict": "WORK_AVAILABLE", "reason": "; ".join(reasons), "live_tip": live_tip, "plan_tip": plan_tip},
               f"WORK_AVAILABLE: {'; '.join(reasons)}", 10)


if __name__ == "__main__":
    main()
