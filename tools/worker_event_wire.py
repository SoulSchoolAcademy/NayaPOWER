#!/usr/bin/env python3
"""Worker-lifecycle -> learning-event wire (issue #2244, implementation sequence D).

Wires the canonical learning-event envelope (tools/learning_event_envelope.py,
#2244 requirement 3) into the real worker activation/exit gates
(tools/worker_entry.py, tools/worker_exit.py):

  - worker_entry.py STAND_DOWN  -> DETECTED blocker event
  - worker_exit.py blocked claim -> DETECTED blocker event

Contract (the whole point of this module):
  - BEST-EFFORT, NEVER-RAISES. The wire must never change a gate verdict or
    exit code. Envelope missing, broken, or validation-rejected -> the gate
    proceeds exactly as it would have; the skip is returned to the caller.
  - NO NETWORK, NO API. Emission is a local ledger append under .naya/
    (brain-index-untracked) plus whatever the envelope itself does at
    DETECTED (the req3->req4 outbox handoff fires only on SHARED, so issuing
    DETECTED never touches the notification outbox).
  - IDEMPOTENT. Event IDs derive from the envelope's identity fields, so a
    repeated identical claim returns the existing event (duplicate: True).

Emission is DETECTED-only: deciding to SHARE an event with the team (the
specialty-feed post, the outbox publish) stays with the worker/lane, never
with this wire. Sharing is a judgment call; detecting is a fact.

Knobs (all env, all optional):
  NAYA_LIFECYCLE_EVENTS=0  kill switch (default: ON)
  NAYA_EVENT_OWNER         event owner (default "naya-2")
  NAYA_EVENT_TEAMS         comma-separated impacted teams (default "learn")
  NAYA_EVENT_LEDGER        ledger path override (tests; honored by envelope)
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

_SEAT_DEFAULT_OWNER = "naya-2"
_SEAT_DEFAULT_TEAMS = "learn"

_40HEX = re.compile(r"^[0-9a-f]{40}$")

# Fallback plan-tip location, used only when the caller cannot supply a SHA
# (worker_exit.py has no tip knowledge). Mirrors the entry gate's layout;
# the caller may pass goal_dir explicitly to avoid the hardcode.
_DEFAULT_GOAL_DIR = os.path.join(
    os.path.expanduser("~"),
    "workspace/goals/nayapower-10-10-completion-drive/hidden_files",
)
_LIVE_PLAN_NAME = "LIVE-PLAN.md"


def lifecycle_events_enabled() -> bool:
    """Kill switch. Default ON; any of 0/false/no/off disables."""
    return os.environ.get("NAYA_LIFECYCLE_EVENTS", "1").strip().lower() not in (
        "0",
        "false",
        "no",
        "off",
    )


def _event_owner() -> str:
    return os.environ.get("NAYA_EVENT_OWNER", _SEAT_DEFAULT_OWNER).strip() or _SEAT_DEFAULT_OWNER


def _event_teams() -> str:
    return os.environ.get("NAYA_EVENT_TEAMS", _SEAT_DEFAULT_TEAMS).strip() or _SEAT_DEFAULT_TEAMS


def plan_tip_40hex(goal_dir: str | None = None) -> str | None:
    """Local-only plan-tip read (no network, no API). 40-hex SHA or None."""
    try:
        plan = Path(goal_dir or os.environ.get("NAYA_GOAL_DIR", _DEFAULT_GOAL_DIR)) / _LIVE_PLAN_NAME
        content = plan.read_text(encoding="utf-8")
        sections = content.split("## TIP NOTE")
        if len(sections) < 2:
            return None
        section = sections[1].split("##")[0]
        match = re.search(r"\b([0-9a-f]{40})\b", section)
        return match.group(1) if match else None
    except Exception:
        return None


def _import_envelope():
    """Deferred import of the canonical envelope. Returns module or None.

    The envelope lives on the #2296 branch and is not merged to main yet;
    this wire must work with or without it (CODE-ONLY branch today,
    ENFORCED only after the envelope merges).
    """
    try:
        import learning_event_envelope  # noqa: F401

        return sys.modules["learning_event_envelope"]
    except Exception:
        return None


def emit_lifecycle_event(
    *,
    event_type: str,
    severity: str,
    title: str,
    expected: str,
    actual: str,
    next_action: str,
    source_artifact: str,
    source_sha: str | None = None,
    goal_dir: str | None = None,
) -> dict:
    """Issue a DETECTED learning event. Never raises.

    Returns a receipt dict: {"status": "emitted"|"duplicate"|"skipped",
    "event_id": ..., "reason": ...}. Callers print it; they never branch on it.
    """
    try:
        if not lifecycle_events_enabled():
            return {"status": "skipped", "reason": "kill_switch"}

        sha = source_sha or plan_tip_40hex(goal_dir)
        if not sha or not _40HEX.match(sha.lower()):
            return {"status": "skipped", "reason": "no_source_sha"}

        envelope = _import_envelope()
        if envelope is None:
            return {"status": "skipped", "reason": "envelope_unavailable"}

        owner = _event_owner()
        fields = {
            "event_type": event_type,
            "severity": severity,
            "title": title.strip()[:200],
            "source_artifact": source_artifact,
            "source_sha": sha.lower(),
            "expected": expected,
            "actual": actual,
            "owner": owner,
            "impacted_teams": _event_teams(),
            "next_action": next_action,
        }
        env, duplicate = envelope.issue_event(fields, issued_by=owner)
        return {
            "status": "duplicate" if duplicate else "emitted",
            "event_id": env["event_id"],
            "reason": "duplicate_idempotent" if duplicate else "ok",
        }
    except Exception as exc:  # never let the wire break the gate
        return {"status": "skipped", "reason": f"wire_error:{type(exc).__name__}"}


def emit_stand_down_event(reason: str, source_sha: str | None = None) -> dict:
    """Entry-gate helper: a STAND_DOWN verdict is a material blocker event."""
    return emit_lifecycle_event(
        event_type="blocker",
        severity="NOTICE",
        title="Worker stand-down: " + reason.strip()[:140],
        expected="worker shift proceeds",
        actual=reason,
        next_action="retry after the stand-down flag TTL expires; escalate if persistent",
        source_artifact="tools/worker_entry.py",
        source_sha=source_sha,
    )


def emit_blocked_event(blocker: str) -> dict:
    """Exit-gate helper: an accepted blocked claim is a material blocker event."""
    blocker = blocker.strip()
    return emit_lifecycle_event(
        event_type="blocker",
        severity="WARNING",
        title="Worker blocked: " + blocker[:140],
        expected="worker completes the shift",
        actual=blocker,
        next_action="owning lane or director resolves the blocker",
        source_artifact="tools/worker_exit.py",
    )


def main() -> None:
    """CLI smoke: python3 tools/worker_event_wire.py --probe."""
    if "--probe" in sys.argv:
        receipt = emit_stand_down_event("probe: lifecycle wire smoke test")
        print(json.dumps(receipt))
        sys.exit(0)
    print("worker_event_wire: library module; use --probe for a smoke emission")
    sys.exit(2)


if __name__ == "__main__":
    main()
