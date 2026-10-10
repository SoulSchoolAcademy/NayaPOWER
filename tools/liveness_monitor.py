#!/usr/bin/env python3
"""
liveness_monitor.py — Multi-node liveness and guaranteed progress.

From Naya 1's "Multi-Node Liveness & Guaranteed Progress":

Governing principle: Safety prevents wrong actions. Liveness ensures eligible
work makes progress. Neither may be sacrificed to satisfy the other.

Safety: □(Commit(d) → Authorized(d))           — never do wrong
Liveness: □(Eligible(d) ∧ Fair(d) → ◇Completed(d)) — eventually do right

Three liveness types:
  DISPOSITION: every accepted request gets outcome or governed waiting state
  WORKFLOW_PROGRESS: enabled eligible workflow advances without starvation
  TASK_COMPLETION: eligible work with available resources reaches outcome

Three failure modes:
  DEADLOCK: circular wait with no escape path
  LIVELOCK: processing without progress
  STARVATION: eligible task never scheduled

Usage:
    python3 tools/liveness_monitor.py register --id LIVE-001 --participants KNOW,LAW,ACT,VERIFY
        --trigger "AUTHORIZED_WORKFLOW_ACCEPTED" --target "VERIFIED_EXECUTION_OUTCOME"
    python3 tools/liveness_monitor.py update --id LIVE-001 --workflow WF-001
        --state WAITING_DEPENDENCY --node KNOW --details <text>
    python3 tools/liveness_monitor.py witness --id LIVE-001 --workflow WF-001
        --milestone KNOW_RECEIPT --evidence <receipt>
    python3 tools/liveness_monitor.py check --id LIVE-001 --workflow WF-001
    python3 tools/liveness_monitor.py report --id LIVE-001
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

HOME = os.path.expanduser("~")
LIVE_DIR = os.path.join(HOME, "workspace/goals/nayapower-10-10-completion-drive/hidden_files/liveness")
REGISTRY_FILE = os.path.join(LIVE_DIR, "liveness.json")
EVENTS_FILE = os.path.join(LIVE_DIR, "events.jsonl")

# Eight workflow states
WORKFLOW_STATES = {
    "RUNNABLE": "All prerequisites satisfied — must receive fair execution",
    "IN_PROGRESS": "Worker actively advancing — monitor milestones",
    "WAITING_DEPENDENCY": "Required dependency not responded — monitor/retry/recover",
    "WAITING_AUTHORITY": "Human decision required — preserve, don't bypass",
    "BLOCKED_RECOVERABLE": "Technical fault — bounded recovery",
    "DEADLOCK_SUSPECTED": "Apparent nonprogressing cycle — analyze escape paths",
    "STARVATION_SUSPECTED": "Eligible but never scheduled — investigate fairness",
    "COMPLETED": "Required work and proof satisfied — preserve receipt",
}

# Three liveness types
LIVENESS_TYPES = {
    "DISPOSITION": "Every accepted request gets outcome or governed waiting state",
    "WORKFLOW_PROGRESS": "Enabled eligible workflow advances without starvation",
    "TASK_COMPLETION": "Eligible work with resources reaches required outcome",
}

# Progress witnesses (meaningful milestones, not heartbeats)
WITNESS_TYPES = {
    "KNOW_RECEIPT": "Applicable evidence returned with provenance",
    "LAW_RECEIPT": "Valid decision receipt or explicit refusal",
    "ACT_EXECUTION_RECEIPT": "Execution attempt and effect with exact target",
    "VERIFY_RECEIPT": "Independently checked outcome",
    "LEARN_QUALIFICATION": "Eligible lesson assessed against proof criteria",
    "EVOLVE_HANDOFF": "Successor package persisted and validated",
}


def load_registry():
    if not os.path.exists(REGISTRY_FILE):
        return {"obligations": {}, "workflows": {}}
    with open(REGISTRY_FILE) as f:
        return json.load(f)


def save_registry(reg):
    os.makedirs(LIVE_DIR, exist_ok=True)
    with open(REGISTRY_FILE, "w") as f:
        json.dump(reg, f, indent=2)


def log_event(event):
    os.makedirs(LIVE_DIR, exist_ok=True)
    with open(EVENTS_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")


def register(obligation_id, participants, trigger, target, liveness_type="TASK_COMPLETION"):
    if liveness_type not in LIVENESS_TYPES:
        print(f"ERROR: Unknown type '{liveness_type}'")
        sys.exit(1)

    reg = load_registry()
    if obligation_id in reg["obligations"]:
        print(f"Obligation {obligation_id} already registered.")
        return

    reg["obligations"][obligation_id] = {
        "id": obligation_id,
        "type": "MULTI_PARTY_LIVENESS",
        "liveness_type": liveness_type,
        "participants": [p.strip() for p in participants.split(",")],
        "trigger": trigger,
        "progress_target": target,
        "fairness_assumptions": "WEAK_FAIRNESS: continuously enabled transitions eventually scheduled",
        "registered_at": datetime.now(timezone.utc).isoformat(),
    }
    save_registry(reg)
    print(f"Registered liveness obligation {obligation_id} ({liveness_type})")
    print(f"  Participants: {participants}")
    print(f"  Target: {target}")
    return reg["obligations"][obligation_id]


def update_workflow(obligation_id, workflow_id, state, node, details=""):
    """Update a workflow's state. Tracks transitions for livelock detection."""
    if state not in WORKFLOW_STATES:
        print(f"ERROR: Unknown state '{state}'. Valid: {', '.join(WORKFLOW_STATES.keys())}")
        sys.exit(1)

    reg = load_registry()
    if obligation_id not in reg["obligations"]:
        print(f"Obligation {obligation_id} not found.")
        sys.exit(1)

    wf_key = f"{obligation_id}/{workflow_id}"
    if wf_key not in reg["workflows"]:
        reg["workflows"][wf_key] = {
            "obligation_id": obligation_id,
            "workflow_id": workflow_id,
            "state_history": [],
            "witnesses": [],
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

    wf = reg["workflows"][wf_key]
    transition = {
        "from": wf["state_history"][-1]["to"] if wf["state_history"] else "NONE",
        "to": state,
        "node": node,
        "details": details[:200],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    wf["state_history"].append(transition)
    wf["current_state"] = state

    # Livelock detection: repeated cycling without new witnesses
    recent = [t["to"] for t in wf["state_history"][-6:]]
    if len(recent) >= 4 and len(set(recent)) <= 2 and state not in ("COMPLETED",):
        print(f"  ⚠ LIVELOCK SUSPECTED: cycling between {set(recent)} without progress")

    # Deadlock detection: all participants waiting on each other
    if state == "WAITING_DEPENDENCY":
        waiting_nodes = set()
        for t in reversed(wf["state_history"][-10:]):
            if t["to"] == "WAITING_DEPENDENCY":
                waiting_nodes.add(t["node"])
        participants = set(reg["obligations"][obligation_id]["participants"])
        if waiting_nodes >= participants and len(participants) >= 2:
            print(f"  ⚠ DEADLOCK SUSPECTED: all participants waiting — check escape paths")
            wf["current_state"] = "DEADLOCK_SUSPECTED"

    save_registry(reg)
    log_event({
        "event_type": "WORKFLOW_STATE_CHANGE",
        "obligation_id": obligation_id,
        "workflow_id": workflow_id,
        "transition": transition,
        "timestamp": transition["timestamp"],
    })

    print(f"{workflow_id}: → {state} ({node})")
    print(f"  {WORKFLOW_STATES[state]}")
    return wf


def record_witness(obligation_id, workflow_id, milestone, evidence=""):
    """Record a meaningful progress witness (not a heartbeat)."""
    if milestone not in WITNESS_TYPES:
        print(f"ERROR: Unknown milestone '{milestone}'")
        sys.exit(1)

    reg = load_registry()
    wf_key = f"{obligation_id}/{workflow_id}"
    if wf_key not in reg["workflows"]:
        print(f"Workflow {wf_key} not found.")
        sys.exit(1)

    wf = reg["workflows"][wf_key]
    witness = {
        "milestone": milestone,
        "meaning": WITNESS_TYPES[milestone],
        "evidence": evidence[:200],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    wf["witnesses"].append(witness)
    save_registry(reg)

    log_event({
        "event_type": "PROGRESS_WITNESS",
        "obligation_id": obligation_id,
        "workflow_id": workflow_id,
        "witness": witness,
        "timestamp": witness["timestamp"],
    })

    print(f"{workflow_id}: witness {milestone} recorded")
    print(f"  {WITNESS_TYPES[milestone]}")
    return witness


def check(obligation_id, workflow_id):
    """Check liveness: is this workflow progressing or stalled?"""
    reg = load_registry()
    wf_key = f"{obligation_id}/{workflow_id}"
    wf = reg["workflows"].get(wf_key)
    if not wf:
        print(f"Workflow {wf_key} not found.")
        sys.exit(1)

    ob = reg["obligations"][obligation_id]
    state = wf.get("current_state", "UNKNOWN")
    n_witnesses = len(wf["witnesses"])
    n_transitions = len(wf["state_history"])

    print(f"\nLiveness check for {workflow_id}:")
    print(f"  Current state: {state}")
    print(f"  Transitions: {n_transitions} | Progress witnesses: {n_witnesses}")
    print(f"  Liveness type: {ob['liveness_type']}")

    # A heartbeat is not proof of progress
    if n_transitions > 5 and n_witnesses == 0:
        print(f"  ⚠ ACTIVITY WITHOUT PROGRESS: {n_transitions} transitions, zero witnesses")
        print(f"    Log lines and retries are not evidence of advancement.")
        return "STALLED"

    if state == "COMPLETED":
        if n_witnesses > 0:
            print(f"  ✓ COMPLETED with {n_witnesses} verified witnesses")
            return "COMPLETED"
        else:
            print(f"  ⚠ Marked COMPLETED but no witnesses — verify actual completion")
            return "SUSPECT"

    if state == "WAITING_AUTHORITY":
        print(f"  → Legitimate wait. Liveness does not create permission.")
        print(f"    Do NOT reclassify as COMPLETED. Preserve ownership.")
        return "WAITING_LEGITIMATE"

    if state in ("DEADLOCK_SUSPECTED", "STARVATION_SUSPECTED"):
        print(f"  ⚠ {state}: independent analysis required")
        return "BLOCKED"

    if state in ("WAITING_DEPENDENCY", "BLOCKED_RECOVERABLE"):
        print(f"  → Monitor, retry within policy, or recover")
        return "RECOVERING"

    print(f"  → Progressing normally")
    return "PROGRESSING"


def report(obligation_id):
    reg = load_registry()
    ob = reg.get("obligations", {}).get(obligation_id)
    if not ob:
        print(f"Obligation {obligation_id} not found.")
        return

    print(f"\n{'='*60}")
    print(f"LIVENESS REPORT: {obligation_id}")
    print(f"{'='*60}")
    print(f"  Type: {ob['liveness_type']} — {LIVENESS_TYPES[ob['liveness_type']]}")
    print(f"  Participants: {', '.join(ob['participants'])}")
    print(f"  Target: {ob['progress_target']}")

    for wf_key, wf in reg["workflows"].items():
        if wf["obligation_id"] == obligation_id:
            print(f"\n  Workflow {wf['workflow_id']}: {wf.get('current_state', 'UNKNOWN')}")
            print(f"    Witnesses: {len(wf['witnesses'])} | Transitions: {len(wf['state_history'])}")


def main():
    parser = argparse.ArgumentParser(description="Multi-node liveness monitor")
    sub = parser.add_subparsers(dest="cmd", required=True)

    rg = sub.add_parser("register", help="Register liveness obligation")
    rg.add_argument("--id", required=True)
    rg.add_argument("--participants", required=True)
    rg.add_argument("--trigger", required=True)
    rg.add_argument("--target", required=True)
    rg.add_argument("--type", default="TASK_COMPLETION",
                    choices=["DISPOSITION", "WORKFLOW_PROGRESS", "TASK_COMPLETION"])

    up = sub.add_parser("update", help="Update workflow state")
    up.add_argument("--id", required=True)
    up.add_argument("--workflow", required=True)
    up.add_argument("--state", required=True, choices=list(WORKFLOW_STATES.keys()))
    up.add_argument("--node", required=True)
    up.add_argument("--details", default="")

    wt = sub.add_parser("witness", help="Record progress witness")
    wt.add_argument("--id", required=True)
    wt.add_argument("--workflow", required=True)
    wt.add_argument("--milestone", required=True, choices=list(WITNESS_TYPES.keys()))
    wt.add_argument("--evidence", default="")

    ck = sub.add_parser("check", help="Check liveness")
    ck.add_argument("--id", required=True)
    ck.add_argument("--workflow", required=True)

    rp = sub.add_parser("report", help="Liveness report")
    rp.add_argument("--id", required=True)

    args = parser.parse_args()
    if args.cmd == "register":
        register(args.id, args.participants, args.trigger, args.target, args.type)
    elif args.cmd == "update":
        update_workflow(args.id, args.workflow, args.state, args.node, args.details)
    elif args.cmd == "witness":
        record_witness(args.id, args.workflow, args.milestone, args.evidence)
    elif args.cmd == "check":
        check(args.id, args.workflow)
    elif args.cmd == "report":
        report(args.id)


if __name__ == "__main__":
    main()
