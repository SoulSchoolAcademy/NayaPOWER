#!/usr/bin/env python3
"""
interpretation_registry.py — Versioned, re-openable interpretations.

From Naya 1's "Interpretation Reopening Protocol":
A resolved interpretation should never become permanently unquestionable.
It becomes a versioned, evidence-backed decision that can reopen when
meaningful new information emerges.

Core rule: Preserve the original meaning. Preserve the original decision.
Reopen when evidence warrants it. Never rewrite history.

Usage:
    python3 tools/interpretation_registry.py register --id <id> --interpretation <text> --evidence <refs>
    python3 tools/interpretation_registry.py challenge --id <id> --evidence <text> --reason <trigger>
    python3 tools/interpretation_registry.py requalify --id <id> --new-interpretation <text> --evidence <refs>
    python3 tools/interpretation_registry.py show --id <id>
    python3 tools/interpretation_registry.py list
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

HOME = os.path.expanduser("~")
REGISTRY_DIR = os.path.join(HOME, "workspace/goals/nayapower-10-10-completion-drive/hidden_files/interpretation-registry")
REGISTRY_FILE = os.path.join(REGISTRY_DIR, "registry.json")


def load_registry():
    if not os.path.exists(REGISTRY_FILE):
        return {}
    with open(REGISTRY_FILE) as f:
        return json.load(f)


def save_registry(reg):
    os.makedirs(REGISTRY_DIR, exist_ok=True)
    with open(REGISTRY_FILE, "w") as f:
        json.dump(reg, f, indent=2)


def content_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def register(interp_id, interpretation, evidence_refs, scope="general", policy_version="P1"):
    reg = load_registry()
    if interp_id in reg:
        print(f"ERROR: {interp_id} already registered. Use challenge + requalify to update.")
        sys.exit(1)

    entry = {
        "id": interp_id,
        "versions": [
            {
                "version": 1,
                "interpretation": interpretation,
                "interpretation_hash": content_hash(interpretation),
                "evidence_refs": evidence_refs,
                "scope": scope,
                "policy_version": policy_version,
                "resolved_at": datetime.now(timezone.utc).isoformat(),
                "status": "RESOLVED",
                "supersedes": None,
            }
        ],
        "current_version": 1,
        "review_state": "RESOLVED",
        "challenges": [],
    }
    reg[interp_id] = entry
    save_registry(reg)
    print(f"Registered {interp_id} v1: {interpretation[:80]}...")
    return entry


def challenge(interp_id, evidence, reason, challenger="unknown"):
    reg = load_registry()
    if interp_id not in reg:
        print(f"ERROR: {interp_id} not found.")
        sys.exit(1)

    entry = reg[interp_id]
    challenge_id = f"CH-{len(entry['challenges']) + 1:03d}"
    chal = {
        "challenge_id": challenge_id,
        "evidence": evidence[:500],
        "trigger": reason,
        "challenger": challenger,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "PENDING",
    }
    entry["challenges"].append(chal)

    # Risk-based: does this warrant reopening?
    # For now: any challenge with evidence moves to CHALLENGED
    # Human or independent review moves CHALLENGED → REOPENED
    entry["review_state"] = "CHALLENGED"
    save_registry(reg)
    print(f"Challenge {challenge_id} registered for {interp_id}. State: CHALLENGED")
    print(f"  Trigger: {reason}")
    return chal


def requalify(interp_id, new_interpretation, evidence_refs, policy_version=None):
    reg = load_registry()
    if interp_id not in reg:
        print(f"ERROR: {interp_id} not found.")
        sys.exit(1)

    entry = reg[interp_id]
    old_version = entry["current_version"]
    new_version = old_version + 1

    # Preserve the old version — never rewrite history
    old_interp = entry["versions"][-1]

    new_entry = {
        "version": new_version,
        "interpretation": new_interpretation,
        "interpretation_hash": content_hash(new_interpretation),
        "evidence_refs": evidence_refs,
        "scope": old_interp["scope"],
        "policy_version": policy_version or old_interp["policy_version"],
        "resolved_at": datetime.now(timezone.utc).isoformat(),
        "status": "REQUALIFIED",
        "supersedes": old_version,
        # The old version is preserved below — history is append-only
    }
    entry["versions"].append(new_entry)
    entry["current_version"] = new_version
    entry["review_state"] = "REQUALIFIED"

    # Mark challenges as addressed
    for c in entry["challenges"]:
        if c["status"] == "PENDING":
            c["status"] = "ADDRESSED"

    save_registry(reg)
    print(f"{interp_id}: v{old_version} → v{new_version}")
    print(f"  Old (preserved): {old_interp['interpretation'][:80]}...")
    print(f"  New: {new_interpretation[:80]}...")
    return new_entry


def show(interp_id):
    reg = load_registry()
    if interp_id not in reg:
        print(f"ERROR: {interp_id} not found.")
        sys.exit(1)

    entry = reg[interp_id]
    print(f"\n{'='*60}")
    print(f"INTERPRETATION: {interp_id}")
    print(f"Current version: v{entry['current_version']} | State: {entry['review_state']}")
    print(f"{'='*60}")
    for v in entry["versions"]:
        marker = " ← CURRENT" if v["version"] == entry["current_version"] else ""
        print(f"\n  v{v['version']}{marker} [{v['status']}]")
        print(f"    {v['interpretation']}")
        print(f"    Evidence: {', '.join(v['evidence_refs'])}")
        print(f"    Resolved: {v['resolved_at'][:19]} | Policy: {v['policy_version']}")
        if v["supersedes"]:
            print(f"    Supersedes: v{v['supersedes']} (preserved, not deleted)")
    if entry["challenges"]:
        print(f"\n  Challenges:")
        for c in entry["challenges"]:
            print(f"    {c['challenge_id']} [{c['status']}] {c['trigger']}: {c['evidence'][:60]}...")


def list_all():
    reg = load_registry()
    if not reg:
        print("Registry empty.")
        return
    print(f"\n{'ID':<40} {'VER':<6} {'STATE':<12} {'CHALLENGES'}")
    print("-" * 70)
    for iid, entry in reg.items():
        print(f"{iid:<40} v{entry['current_version']:<5} {entry['review_state']:<12} {len(entry['challenges'])}")


def main():
    parser = argparse.ArgumentParser(description="Versioned interpretation registry")
    sub = parser.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("register", help="Register a new interpretation")
    r.add_argument("--id", required=True)
    r.add_argument("--interpretation", required=True)
    r.add_argument("--evidence", nargs="+", default=[])
    r.add_argument("--scope", default="general")

    c = sub.add_parser("challenge", help="Challenge an interpretation")
    c.add_argument("--id", required=True)
    c.add_argument("--evidence", required=True)
    c.add_argument("--reason", required=True)
    c.add_argument("--challenger", default="unknown")

    q = sub.add_parser("requalify", help="Create new version")
    q.add_argument("--id", required=True)
    q.add_argument("--new-interpretation", required=True)
    q.add_argument("--evidence", nargs="+", default=[])

    s = sub.add_parser("show", help="Show interpretation history")
    s.add_argument("--id", required=True)

    sub.add_parser("list", help="List all interpretations")

    args = parser.parse_args()
    if args.cmd == "register":
        register(args.id, args.interpretation, args.evidence, args.scope)
    elif args.cmd == "challenge":
        challenge(args.id, args.evidence, args.reason, args.challenger)
    elif args.cmd == "requalify":
        requalify(args.id, args.new_interpretation, args.evidence)
    elif args.cmd == "show":
        show(args.id)
    elif args.cmd == "list":
        list_all()


if __name__ == "__main__":
    main()
