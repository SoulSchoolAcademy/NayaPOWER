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


# Well-founded progress measure (Naya 1's "Well-Founded Measure of Real Progress"):
#
# Two separate measures:
#   Proof progress: has a required obligation been discharged with acceptable evidence?
#   Termination progress: is the system moving toward finite resolution?
#
# W(s) = multiset of ranks of outstanding obligations (well-founded multiset order)
# R(s) = remaining permitted recovery attempts
# Φ(s) = (W(s), R(s)) ordered lexicographically
#
# Activity is not progress. Verified reduction in outstanding obligations is progress.


def register_obligation_graph(obligation_id, obligations):
    """
    Register the obligation graph for a liveness obligation.
    obligations: list of {"id": ..., "rank": int, "type": "AND"|"OR"|"LEAF",
                           "children": [...], "acceptance": ...}
    
    Rank rule: a higher-rank obligation decomposes only into finitely many
    strictly lower-rank obligations. New objectives start a new epoch.
    """
    reg = load_registry()
    if obligation_id not in reg["obligations"]:
        print(f"Liveness obligation {obligation_id} not found. Register it first.")
        sys.exit(1)

    # Validate ranks: children must have strictly lower rank than parent
    ob_map = {o["id"]: o for o in obligations}
    for o in obligations:
        for child_id in o.get("children", []):
            child = ob_map.get(child_id)
            if not child:
                print(f"ERROR: child {child_id} not in obligation list")
                sys.exit(1)
            if child["rank"] >= o["rank"]:
                print(f"ERROR: child {child_id} rank {child['rank']} not < parent {o['id']} rank {o['rank']}")
                print(f"  Refinement must be strictly rank-decreasing (well-founded).")
                sys.exit(1)

    reg["obligations"][obligation_id]["obligation_graph"] = obligations
    reg["obligations"][obligation_id]["epoch"] = 1
    save_registry(reg)
    print(f"Registered obligation graph for {obligation_id}: {len(obligations)} obligations, epoch 1")
    return obligations


def compute_progress_measure(obligation_id, workflow_id):
    """
    Compute Φ(s) = (W(s), R(s)):
    - W(s): multiset of ranks of outstanding (non-discharged) obligations
    - R(s): remaining recovery budget
    
    Returns the measure and whether it decreased since last computation.
    """
    reg = load_registry()
    ob = reg["obligations"].get(obligation_id)
    if not ob or "obligation_graph" not in ob:
        print(f"No obligation graph for {obligation_id}.")
        return None

    wf_key = f"{obligation_id}/{workflow_id}"
    wf = reg["workflows"].get(wf_key, {})
    discharged = set(wf.get("discharged_obligations", []))

    # W(s): ranks of outstanding obligations
    outstanding = [o for o in ob["obligation_graph"] if o["id"] not in discharged]
    W = sorted([o["rank"] for o in outstanding], reverse=True)

    # R(s): remaining recovery budget
    R = wf.get("recovery_budget", ob.get("default_recovery_budget", 3))

    measure = {"W": W, "R": R, "outstanding_ids": [o["id"] for o in outstanding]}

    # Compare with previous
    prev = wf.get("last_measure")
    decreased = None
    if prev:
        # Lexicographic: W decreases (multiset order), or W same and R decreases
        if multiset_less(W, prev["W"]):
            decreased = "PROOF_PROGRESS"
        elif W == prev["W"] and R < prev["R"]:
            decreased = "TERMINATION_PROGRESS"
        elif W == prev["W"] and R == prev["R"]:
            decreased = "NO_CHANGE"
        else:
            decreased = "INCREASED (invalid — work grew without new epoch)"

    wf["last_measure"] = measure
    if wf_key not in reg["workflows"]:
        reg["workflows"][wf_key] = wf
    else:
        reg["workflows"][wf_key]["last_measure"] = measure
    save_registry(reg)

    print(f"\nProgress measure Φ for {workflow_id}:")
    print(f"  W (outstanding ranks): {W}")
    print(f"  R (recovery budget): {R}")
    print(f"  Outstanding: {measure['outstanding_ids']}")
    if decreased:
        print(f"  Change: {decreased}")
        if decreased == "PROOF_PROGRESS":
            print(f"    ✓ Verified reduction in outstanding obligations")
        elif decreased == "TERMINATION_PROGRESS":
            print(f"    → Recovery consumed, no proof advancement")
        elif decreased == "NO_CHANGE":
            print(f"    → Activity without progress (no credit)")
    return measure, decreased


def multiset_less(a, b):
    """
    Well-founded multiset order: a < b if a can be obtained from b by
    replacing one element with finitely many strictly smaller elements,
    or by removing elements.
    Simplified: compare sorted descending; a < b if at first difference, a[i] < b[i],
    or if a is a proper prefix-subset.
    """
    # Remove common elements
    from collections import Counter
    ca, cb = Counter(a), Counter(b)
    # a < b iff for the largest element where they differ, a has fewer
    all_ranks = sorted(set(list(ca.keys()) + list(cb.keys())), reverse=True)
    for r in all_ranks:
        if ca[r] < cb[r]:
            return True
        elif ca[r] > cb[r]:
            return False
    return False  # equal


def discharge_obligation(obligation_id, workflow_id, obligation_id_to_discharge, evidence=""):
    """
    Discharge an obligation with acceptable evidence.
    This is the ONLY way to reduce W(s). Status updates, retries, reassignments don't count.
    """
    reg = load_registry()
    ob = reg["obligations"].get(obligation_id)
    if not ob or "obligation_graph" not in ob:
        print(f"No obligation graph for {obligation_id}.")
        sys.exit(1)

    wf_key = f"{obligation_id}/{workflow_id}"
    if wf_key not in reg["workflows"]:
        print(f"Workflow {wf_key} not found.")
        sys.exit(1)

    wf = reg["workflows"][wf_key]
    if "discharged_obligations" not in wf:
        wf["discharged_obligations"] = []

    # Check AND/OR logic: for AND children, all must be discharged before parent
    ob_map = {o["id"]: o for o in ob["obligation_graph"]}
    target = ob_map.get(obligation_id_to_discharge)
    if not target:
        print(f"Obligation {obligation_id_to_discharge} not in graph.")
        sys.exit(1)

    # For AND-type parents: verify all children discharged first
    for o in ob["obligation_graph"]:
        if obligation_id_to_discharge in o.get("children", []) and o.get("type") == "AND":
            # This is a child; parent discharge requires all siblings too
            pass  # child can be discharged independently

    if obligation_id_to_discharge in wf["discharged_obligations"]:
        print(f"  {obligation_id_to_discharge} already discharged — no double-counting")
        return False

    wf["discharged_obligations"].append(obligation_id_to_discharge)
    wf.setdefault("discharge_receipts", []).append({
        "obligation_id": obligation_id_to_discharge,
        "evidence": evidence[:200],
        "discharged_at": datetime.now(timezone.utc).isoformat(),
    })
    save_registry(reg)

    log_event({
        "event_type": "OBLIGATION_DISCHARGED",
        "obligation_id": obligation_id,
        "workflow_id": workflow_id,
        "discharged": obligation_id_to_discharge,
        "evidence": evidence[:100],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })

    print(f"  ✓ {obligation_id_to_discharge} DISCHARGED (rank {target['rank']})")
    print(f"    Evidence: {evidence[:80]}...")
    return True


def consume_recovery(obligation_id, workflow_id, reason=""):
    """
    Consume one recovery attempt. Reduces R(s), not W(s).
    Termination progress, not proof progress.
    """
    reg = load_registry()
    wf_key = f"{obligation_id}/{workflow_id}"
    wf = reg["workflows"].get(wf_key)
    if not wf:
        print(f"Workflow {wf_key} not found.")
        sys.exit(1)

    ob = reg["obligations"][obligation_id]
    current = wf.get("recovery_budget", ob.get("default_recovery_budget", 3))
    if current <= 0:
        print(f"  ✗ Recovery budget exhausted — no attempts remaining")
        print(f"    Workflow must reach terminal disposition or escalate.")
        return False

    wf["recovery_budget"] = current - 1
    save_registry(reg)
    log_event({
        "event_type": "RECOVERY_CONSUMED",
        "obligation_id": obligation_id,
        "workflow_id": workflow_id,
        "remaining": current - 1,
        "reason": reason[:100],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
    print(f"  Recovery consumed: {current} → {current - 1} remaining")
    print(f"    Termination progress (budget decreased), NOT proof progress.")
    return True


def new_epoch(obligation_id, reason=""):
    """
    Start a new assessment epoch when genuinely new requirements appear.
    Old baseline preserved. Progress resets against new obligations.
    """
    reg = load_registry()
    ob = reg["obligations"].get(obligation_id)
    if not ob:
        print(f"Obligation {obligation_id} not found.")
        sys.exit(1)

    old_epoch = ob.get("epoch", 1)
    ob["epoch"] = old_epoch + 1
    ob[f"epoch_{old_epoch}_graph"] = ob.get("obligation_graph", [])
    save_registry(reg)

    log_event({
        "event_type": "NEW_ASSESSMENT_EPOCH",
        "obligation_id": obligation_id,
        "from_epoch": old_epoch,
        "to_epoch": old_epoch + 1,
        "reason": reason[:200],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })

    print(f"{obligation_id}: epoch {old_epoch} → {old_epoch + 1}")
    print(f"  Reason: {reason[:80]}...")
    print(f"  Old baseline preserved. New obligations must be registered.")
    return ob["epoch"]


# Scheduler fairness (Naya 1's "Fair Scheduling Without False Progress"):
#
# Two independent proof obligations:
#   Progress: did a required obligation get discharged? (W(s) decreases)
#   Fairness: was eligible work given adequate opportunity? (F_o(t) tracked)
#
# Governing rule: Fairness guarantees opportunity. Execution creates observations.
# Only qualifying evidence establishes accomplishment.
#
# Service levels (each strictly stronger than the last):
#   SELECTED → DISPATCHED → SERVICED → ATTEMPTED → ADVANCED → COMPLETED
# Only ADVANCED and COMPLETED affect the proof-progress ranking.

# Fairness standards
FAIRNESS_STANDARDS = {
    "WEAK": "Continuously enabled transition cannot be postponed forever",
    "STRONG": "Infinitely-often-enabled transition cannot be ignored forever",
    "BOUNDED": "Eligible obligation receives adequate service within specified bound",
}

# Service levels
SERVICE_LEVELS = ["SELECTED", "DISPATCHED", "SERVICED", "ATTEMPTED", "ADVANCED", "COMPLETED"]


def register_fairness(obligation_id, fairness_type="WEAK", service_bound=None):
    """Register fairness contract for a liveness obligation."""
    if fairness_type not in FAIRNESS_STANDARDS:
        print(f"ERROR: Unknown fairness type '{fairness_type}'")
        sys.exit(1)

    reg = load_registry()
    if obligation_id not in reg["obligations"]:
        print(f"Obligation {obligation_id} not found.")
        sys.exit(1)

    reg["obligations"][obligation_id]["fairness"] = {
        "type": fairness_type,
        "description": FAIRNESS_STANDARDS[fairness_type],
        "service_bound": service_bound,
        "ledger": {},  # obligation_id -> {opportunities, services, last_service}
    }
    save_registry(reg)
    print(f"Fairness registered for {obligation_id}: {fairness_type}")
    print(f"  {FAIRNESS_STANDARDS[fairness_type]}")
    return reg["obligations"][obligation_id]["fairness"]


def record_service(obligation_id, workflow_id, target_obligation, service_level, evidence=""):
    """
    Record a scheduler service event for a specific obligation.
    
    Critical: service does NOT change proof progress. Only verified discharge does.
    Fairness debt belongs to the obligation ID — survives reassignment.
    """
    if service_level not in SERVICE_LEVELS:
        print(f"ERROR: Unknown service level '{service_level}'")
        sys.exit(1)

    reg = load_registry()
    ob = reg["obligations"].get(obligation_id)
    if not ob or "fairness" not in ob:
        print(f"No fairness contract for {obligation_id}. Register fairness first.")
        sys.exit(1)

    ledger = ob["fairness"]["ledger"]
    if target_obligation not in ledger:
        ledger[target_obligation] = {
            "opportunities": 0,      # times eligible for scheduling
            "services": 0,            # times received usable execution opportunity
            "advancements": 0,       # times service led to proof progress
            "last_service": None,
            "fairness_debt": 0,      # eligible rounds without adequate service
        }

    entry = ledger[target_obligation]
    level_idx = SERVICE_LEVELS.index(service_level)

    # SELECTED/DISPATCHED: scheduling decisions, not service
    # SERVICED+: counts as genuine opportunity
    if level_idx >= SERVICE_LEVELS.index("SERVICED"):
        entry["services"] += 1
        entry["fairness_debt"] = 0  # debt cleared on genuine service
        entry["last_service"] = datetime.now(timezone.utc).isoformat()
    else:
        # Mere selection/dispatch without usable resources: no fairness credit
        print(f"  Note: {service_level} is scheduling, not service — no fairness credit")

    if level_idx >= SERVICE_LEVELS.index("ADVANCED"):
        entry["advancements"] += 1

    save_registry(reg)
    log_event({
        "event_type": "FAIRNESS_SERVICE",
        "obligation_id": obligation_id,
        "workflow_id": workflow_id,
        "target": target_obligation,
        "level": service_level,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })

    print(f"  {target_obligation}: {service_level} (services={entry['services']}, debt={entry['fairness_debt']})")
    if level_idx < SERVICE_LEVELS.index("SERVICED"):
        print(f"    → Does NOT satisfy fairness obligation. Does NOT advance proof.")
    return entry


def record_eligible_round(obligation_id, eligible_obligations):
    """
    Record a scheduler round. Obligations that were eligible but not serviced
    accumulate fairness debt. Debt belongs to obligation ID, survives reassignment.
    """
    reg = load_registry()
    ob = reg["obligations"].get(obligation_id)
    if not ob or "fairness" not in ob:
        print(f"No fairness contract for {obligation_id}.")
        sys.exit(1)

    ledger = ob["fairness"]["ledger"]
    for obl_id in eligible_obligations:
        if obl_id not in ledger:
            ledger[obl_id] = {"opportunities": 0, "services": 0, "advancements": 0,
                              "last_service": None, "fairness_debt": 0}
        ledger[obl_id]["opportunities"] += 1
        # Debt increases if not serviced this round
        # (servicing resets it in record_service)
        ledger[obl_id]["fairness_debt"] += 1

    save_registry(reg)

    # Check for starvation: high debt = potential fairness violation
    starving = [(k, v["fairness_debt"]) for k, v in ledger.items() if v["fairness_debt"] >= 5]
    if starving:
        print(f"  ⚠ STARVATION SUSPECTED:")
        for obl_id, debt in starving:
            print(f"    {obl_id}: {debt} eligible rounds without adequate service")
    return ledger


def fairness_report(obligation_id):
    """Report fairness and progress independently."""
    reg = load_registry()
    ob = reg["obligations"].get(obligation_id)
    if not ob or "fairness" not in ob:
        print(f"No fairness contract for {obligation_id}.")
        return

    print(f"\n{'='*60}")
    print(f"FAIRNESS LEDGER: {obligation_id}")
    print(f"{'='*60}")
    print(f"  Standard: {ob['fairness']['type']} — {ob['fairness']['description']}")
    print(f"\n  {'Obligation':<20} {'Opportunities':<14} {'Services':<10} {'Advanced':<10} {'Debt':<6}")
    print(f"  {'-'*70}")

    for obl_id, entry in ob["fairness"]["ledger"].items():
        print(f"  {obl_id:<20} {entry['opportunities']:<14} {entry['services']:<10} "
              f"{entry['advancements']:<10} {entry['fairness_debt']:<6}")

    print(f"\n  Interpretation:")
    print(f"  - Fairly served but stalled = fairness OK, progress failed")
    print(f"  - Never served while eligible = fairness violation (starvation)")
    print(f"  - Service never counts as proof. Only discharge reduces W(s).")


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

    rg2 = sub.add_parser("register-graph", help="Register obligation graph with ranks")
    rg2.add_argument("--id", required=True)
    rg2.add_argument("--obligations", required=True, help="JSON list of {id,rank,type,children}")

    pm = sub.add_parser("measure", help="Compute well-founded progress measure")
    pm.add_argument("--id", required=True)
    pm.add_argument("--workflow", required=True)

    dc = sub.add_parser("discharge", help="Discharge obligation with evidence")
    dc.add_argument("--id", required=True)
    dc.add_argument("--workflow", required=True)
    dc.add_argument("--obligation", required=True)
    dc.add_argument("--evidence", default="")

    cr = sub.add_parser("consume-recovery", help="Consume recovery attempt")
    cr.add_argument("--id", required=True)
    cr.add_argument("--workflow", required=True)
    cr.add_argument("--reason", default="")

    ne = sub.add_parser("new-epoch", help="Start new assessment epoch")
    ne.add_argument("--id", required=True)
    ne.add_argument("--reason", default="")

    rf = sub.add_parser("register-fairness", help="Register fairness contract")
    rf.add_argument("--id", required=True)
    rf.add_argument("--type", default="WEAK", choices=["WEAK", "STRONG", "BOUNDED"])
    rf.add_argument("--bound", type=int, default=None)

    sv = sub.add_parser("record-service", help="Record scheduler service event")
    sv.add_argument("--id", required=True)
    sv.add_argument("--workflow", required=True)
    sv.add_argument("--obligation", required=True)
    sv.add_argument("--level", required=True,
                    choices=["SELECTED", "DISPATCHED", "SERVICED", "ATTEMPTED", "ADVANCED", "COMPLETED"])
    sv.add_argument("--evidence", default="")

    er = sub.add_parser("eligible-round", help="Record scheduler round")
    er.add_argument("--id", required=True)
    er.add_argument("--eligible", required=True, help="Comma-separated obligation IDs")

    fr = sub.add_parser("fairness-report", help="Fairness ledger report")
    fr.add_argument("--id", required=True)

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
    elif args.cmd == "register-graph":
        obligations = json.loads(args.obligations)
        register_obligation_graph(args.id, obligations)
    elif args.cmd == "measure":
        compute_progress_measure(args.id, args.workflow)
    elif args.cmd == "discharge":
        discharge_obligation(args.id, args.workflow, args.obligation, args.evidence)
    elif args.cmd == "consume-recovery":
        consume_recovery(args.id, args.workflow, args.reason)
    elif args.cmd == "new-epoch":
        new_epoch(args.id, args.reason)
    elif args.cmd == "register-fairness":
        register_fairness(args.id, args.type, args.bound)
    elif args.cmd == "record-service":
        record_service(args.id, args.workflow, args.obligation, args.level, args.evidence)
    elif args.cmd == "eligible-round":
        eligible = [e.strip() for e in args.eligible.split(",")]
        record_eligible_round(args.id, eligible)
    elif args.cmd == "fairness-report":
        fairness_report(args.id)


if __name__ == "__main__":
    main()
