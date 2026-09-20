#!/usr/bin/env python3
"""Fail-closed structural gate for the NayaPOWER GitHub operating environment.

This validator deliberately does not pretend to know live GitHub issue state or
external deployment state. Those are represented by checked-in audit snapshots.
A stale or incomplete snapshot fails the gate rather than becoming false proof.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / ".naya" / "control-plane"

REQUIRED = [
    CONTROL / "STATE.json",
    CONTROL / "BLOCKS.json",
    CONTROL / "MAP.json",
    CONTROL / "PROOF.json",
    CONTROL / "GITHUB-OPTIMIZATION-GATE.json",
    CONTROL / "GITHUB-ISSUE-AUDIT.json",
    CONTROL / "GITHUB-WORKFLOW-AUDIT.json",
    CONTROL / "GITHUB-AUTHORITY-AUDIT.json",
]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []

    for path in REQUIRED:
        if not path.exists():
            fail(errors, f"MISSING_REQUIRED={path.relative_to(ROOT)}")

    if errors:
        for e in errors:
            print(f"FAIL {e}")
        return 1

    gate = load(CONTROL / "GITHUB-OPTIMIZATION-GATE.json")
    state = load(CONTROL / "STATE.json")
    issues = load(CONTROL / "GITHUB-ISSUE-AUDIT.json")
    workflows = load(CONTROL / "GITHUB-WORKFLOW-AUDIT.json")
    authorities = load(CONTROL / "GITHUB-AUTHORITY-AUDIT.json")

    # Current-state integrity.
    if state.get("repository") != "SoulSchoolAcademy/NayaPOWER":
        fail(errors, "STATE_REPOSITORY_MISMATCH")
    if state.get("current_head", {}).get("mode") != "LIVE_RESOLUTION":
        fail(errors, "STATE_HEAD_IS_NOT_LIVE_RESOLUTION")
    if state.get("current_branch", {}).get("mode") != "LIVE_RESOLUTION":
        fail(errors, "STATE_BRANCH_IS_NOT_LIVE_RESOLUTION")
    if state.get("next_action_count") != 1:
        fail(errors, f"STATE_NEXT_ACTION_COUNT={state.get('next_action_count')} EXPECTED=1")
    if not state.get("single_next_action"):
        fail(errors, "STATE_SINGLE_NEXT_ACTION_MISSING")

    # Required canonical surfaces.
    if not (ROOT / ".naya" / "memory" / "events").is_dir():
        fail(errors, "CANONICAL_EVENT_STORE_MISSING")
    if not (ROOT / "SUPERBRAIN" / "NAYA-ACTIVITY").is_dir():
        fail(errors, "HUMAN_ACTIVITY_PROJECTION_MISSING")

    # Issue audit must cover the complete open-issue population observed when
    # the snapshot was produced. A partial audit is intentionally RED.
    observed = issues.get("observed_open_issue_count")
    classified = issues.get("classified_issue_count", 0)
    unclassified = issues.get("unclassified_issue_count", 0)
    if not isinstance(observed, int):
        fail(errors, "ISSUE_AUDIT_MISSING_OBSERVED_COUNT")
    if classified + unclassified != observed:
        fail(errors, "ISSUE_AUDIT_COUNTS_DO_NOT_RECONCILE")
    if gate["invariants"]["no_unclassified_open_issue"] and unclassified != 0:
        fail(errors, f"OPEN_ISSUES_UNCLASSIFIED={unclassified}")

    # Workflow audit must classify every workflow and every mutation/deployment
    # authority. Names alone never establish authority.
    if workflows.get("unclassified_workflow_count", 0) != 0:
        fail(errors, f"WORKFLOWS_UNCLASSIFIED={workflows.get('unclassified_workflow_count')}")
    if workflows.get("unresolved_authority_conflicts", 0) != 0:
        fail(errors, f"WORKFLOW_AUTHORITY_CONFLICTS={workflows.get('unresolved_authority_conflicts')}")

    # Authority audit must explicitly resolve the Activity, machine event,
    # runtime/deployment, Hub source, and state authorities.
    if authorities.get("unresolved_conflicts", 0) != 0:
        fail(errors, f"AUTHORITY_CONFLICTS={authorities.get('unresolved_conflicts')}")
    required_authorities = {
        "state",
        "machine_event_store",
        "human_activity_projection",
        "hub_source",
        "runtime_deployment",
    }
    actual = {x.get("key") for x in authorities.get("authorities", [])}
    for key in sorted(required_authorities - actual):
        fail(errors, f"AUTHORITY_MISSING={key}")

    # No accidental duplicate Activity stores may silently become canonical.
    activity_dirs = [ROOT / ".naya" / "activity", ROOT / "SUPERBRAIN" / "NAYA-ACTIVITY"]
    if all(p.exists() for p in activity_dirs):
        role = authorities.get("activity_secondary_surface_role")
        if role not in {"COMPATIBILITY_ARCHIVE", "SUPPORTING_RECORDS", "HISTORICAL_REFERENCE"}:
            fail(errors, "SECOND_ACTIVITY_SURFACE_ROLE_UNRESOLVED")

    print("NAYAPOWER_GITHUB_OPTIMIZATION_GATE=GREEN" if not errors else "NAYAPOWER_GITHUB_OPTIMIZATION_GATE=RED")
    print(f"OPEN_ISSUES_OBSERVED={observed}")
    print(f"OPEN_ISSUES_CLASSIFIED={classified}")
    print(f"OPEN_ISSUES_UNCLASSIFIED={unclassified}")
    print(f"WORKFLOWS_UNCLASSIFIED={workflows.get('unclassified_workflow_count')}")
    print(f"WORKFLOW_AUTHORITY_CONFLICTS={workflows.get('unresolved_authority_conflicts')}")
    print(f"AUTHORITY_CONFLICTS={authorities.get('unresolved_conflicts')}")
    if state.get("single_next_action"):
        print(f"SINGLE_NEXT_ACTION={state['single_next_action']}")
    for e in errors:
        print(f"FAIL {e}")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
