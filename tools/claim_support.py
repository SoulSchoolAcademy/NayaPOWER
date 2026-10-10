#!/usr/bin/env python3
"""
claim_support.py — Provenance-preserving intelligence propagation.

From Naya 1's "Provenance-Preserving Intelligence Propagation":

Governing rule: Uncertainty follows evidence dependencies.
Eligibility follows sufficient independent support.
Authority remains with LAW.

Every claim carries an evidence-support envelope:
  - claim_id: stable identity
  - source_refs: original provenance
  - support_sets: alternative combinations of evidence sufficient for the claim
  - independence_state: per evidence contribution
  - qualification: current status, basis, scope

Support logic:
  C ⇐ A ∨ B  (OR): if B independently supports C, A's uncertainty doesn't disqualify C
  C ⇐ A ∧ B  (AND): if the contract requires both, A's uncertainty blocks full qualification

Usage:
    python3 tools/claim_support.py register-claim --id CLAIM-C --description <text>
    python3 tools/claim_support.py add-support --claim CLAIM-C --set-id SUPPORT-A
        --evidence EVID-A --independence UNDETERMINED --logic OR
    python3 tools/claim_support.py evaluate --claim CLAIM-C
    python3 tools/claim_support.py revoke-evidence --evidence EVID-A --reason <text>
    python3 tools/claim_support.py report
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

HOME = os.path.expanduser("~")
CLAIM_DIR = os.path.join(HOME, "workspace/goals/nayapower-10-10-completion-drive/hidden_files/claim-support")
REGISTRY_FILE = os.path.join(CLAIM_DIR, "claims.json")
EVENTS_FILE = os.path.join(CLAIM_DIR, "events.jsonl")


def load_registry():
    if not os.path.exists(REGISTRY_FILE):
        return {"claims": {}}
    with open(REGISTRY_FILE) as f:
        return json.load(f)


def save_registry(reg):
    os.makedirs(CLAIM_DIR, exist_ok=True)
    with open(REGISTRY_FILE, "w") as f:
        json.dump(reg, f, indent=2)


def log_event(event):
    os.makedirs(CLAIM_DIR, exist_ok=True)
    with open(EVENTS_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")


def register_claim(claim_id, description, scope=""):
    reg = load_registry()
    if claim_id in reg["claims"]:
        print(f"Claim {claim_id} already registered.")
        return
    reg["claims"][claim_id] = {
        "id": claim_id,
        "description": description[:300],
        "scope": scope[:200],
        "support_sets": [],
        "historical_dependencies": [],
        "qualification": {
            "status": "UNEVALUATED",
            "basis": None,
            "scope": scope,
        },
        "registered_at": datetime.now(timezone.utc).isoformat(),
    }
    save_registry(reg)
    print(f"Registered claim {claim_id}")
    return reg["claims"][claim_id]


def add_support(claim_id, set_id, evidence_refs, independence, logic="OR", scope=""):
    """
    Add a support set to a claim.
    logic=OR: this set alone is sufficient (C ⇐ A ∨ B)
    logic=AND: this set must combine with others (C ⇐ A ∧ B)
    """
    reg = load_registry()
    if claim_id not in reg["claims"]:
        print(f"Claim {claim_id} not found.")
        sys.exit(1)

    claim = reg["claims"][claim_id]
    ev_list = [e.strip() for e in evidence_refs.split(",")]

    support_set = {
        "set_id": set_id,
        "evidence_refs": ev_list,
        "independence": independence,
        "logic": logic,
        "scope": scope[:200],
        "added_at": datetime.now(timezone.utc).isoformat(),
    }
    claim["support_sets"].append(support_set)
    for e in ev_list:
        if e not in claim["historical_dependencies"]:
            claim["historical_dependencies"].append(e)

    save_registry(reg)
    print(f"Added {set_id} to {claim_id}: {logic}-support via {ev_list} [{independence}]")
    return support_set


def evaluate(claim_id):
    """
    Recompute claim qualification from current support sets.
    
    OR logic: claim qualifies if ANY support set has confirmed independence
    AND logic: claim qualifies only if ALL required sets have confirmed independence
    """
    reg = load_registry()
    if claim_id not in reg["claims"]:
        print(f"Claim {claim_id} not found.")
        sys.exit(1)

    claim = reg["claims"][claim_id]
    sets = claim["support_sets"]

    if not sets:
        claim["qualification"] = {"status": "INSUFFICIENT_DATA", "basis": None, "reason": "No support sets"}
        save_registry(reg)
        print(f"{claim_id}: INSUFFICIENT_DATA — no support sets")
        return claim["qualification"]

    # Separate OR and AND sets
    or_sets = [s for s in sets if s["logic"] == "OR"]
    and_sets = [s for s in sets if s["logic"] == "AND"]

    # OR: any confirmed-independent set suffices
    or_qualified = [s for s in or_sets if s["independence"] == "CONFIRMED"]
    # AND: all must be confirmed
    and_qualified = all(s["independence"] == "CONFIRMED" for s in and_sets) if and_sets else True

    if or_qualified and and_qualified:
        basis = or_qualified[0]["set_id"] if or_qualified else "AND-sets"
        # Scope: narrowest of the qualifying sets
        scopes = [s["scope"] for s in or_qualified if s["scope"]]
        scope = scopes[0] if scopes else claim["scope"]
        claim["qualification"] = {
            "status": "SUPPORTED_IN_SCOPE",
            "basis": basis,
            "scope": scope,
            "evaluated_at": datetime.now(timezone.utc).isoformat(),
        }
        reason = f"Qualified through {basis}"
    elif or_sets and not or_qualified:
        # Has OR sets but none confirmed — check if any undetermined
        undetermined = [s for s in or_sets if s["independence"] == "UNDETERMINED"]
        if undetermined:
            claim["qualification"] = {
                "status": "UNDETERMINED",
                "basis": None,
                "reason": f"No confirmed support; {[s['set_id'] for s in undetermined]} undetermined",
                "evaluated_at": datetime.now(timezone.utc).isoformat(),
            }
            reason = "No confirmed independent support"
        else:
            claim["qualification"] = {
                "status": "UNSUPPORTED",
                "basis": None,
                "reason": "All support sets compromised or revoked",
                "evaluated_at": datetime.now(timezone.utc).isoformat(),
            }
            reason = "All support compromised"
    elif and_sets and not and_qualified:
        failed = [s["set_id"] for s in and_sets if s["independence"] != "CONFIRMED"]
        claim["qualification"] = {
            "status": "BLOCKED",
            "basis": None,
            "reason": f"AND-requirement failed: {failed} not confirmed",
            "evaluated_at": datetime.now(timezone.utc).isoformat(),
        }
        reason = f"AND-blocked by {failed}"
    else:
        claim["qualification"] = {
            "status": "INSUFFICIENT_DATA",
            "basis": None,
            "reason": "Cannot determine from current support sets",
            "evaluated_at": datetime.now(timezone.utc).isoformat(),
        }
        reason = "Insufficient data"

    save_registry(reg)
    log_event({
        "event_type": "CLAIM_EVALUATED",
        "claim_id": claim_id,
        "qualification": claim["qualification"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
    print(f"{claim_id}: {claim['qualification']['status']} — {reason}")
    return claim["qualification"]


def revoke_evidence(evidence_id, reason=""):
    """
    Revoke an evidence source. Recompute all claims that depend on it.
    Uncertainty follows dependencies. Eligibility follows remaining support.
    """
    reg = load_registry()
    affected = []

    for claim_id, claim in reg["claims"].items():
        for s in claim["support_sets"]:
            if evidence_id in s["evidence_refs"]:
                s["independence"] = "COMPROMISED"
                s["revoked_at"] = datetime.now(timezone.utc).isoformat()
                s["revoke_reason"] = reason[:200]
                affected.append(claim_id)
                break

    log_event({
        "event_type": "EVIDENCE_REVOKED",
        "evidence_id": evidence_id,
        "reason": reason[:200],
        "affected_claims": affected,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })

    save_registry(reg)
    print(f"Evidence {evidence_id} revoked. Recomputing {len(affected)} affected claims...")
    for cid in affected:
        evaluate(cid)
    return affected


def report():
    reg = load_registry()
    claims = reg.get("claims", {})
    if not claims:
        print("No claims registered.")
        return
    print(f"\n{'='*60}")
    print("CLAIM SUPPORT REPORT")
    print(f"{'='*60}")
    for cid, c in claims.items():
        q = c["qualification"]
        print(f"\n  {cid}: {q['status']}")
        print(f"    {c['description'][:60]}...")
        for s in c["support_sets"]:
            print(f"    [{s['logic']}] {s['set_id']}: {s['evidence_refs']} → {s['independence']}")
        if q.get("basis"):
            print(f"    Qualified via: {q['basis']} (scope: {q.get('scope', 'unbounded')[:40]})")


def main():
    parser = argparse.ArgumentParser(description="Claim-level support-set evaluator")
    sub = parser.add_subparsers(dest="cmd", required=True)

    rc = sub.add_parser("register-claim", help="Register a claim")
    rc.add_argument("--id", required=True)
    rc.add_argument("--description", required=True)
    rc.add_argument("--scope", default="")

    asp = sub.add_parser("add-support", help="Add support set to claim")
    asp.add_argument("--claim", required=True)
    asp.add_argument("--set-id", required=True)
    asp.add_argument("--evidence", required=True, help="Comma-separated evidence IDs")
    asp.add_argument("--independence", required=True,
                     choices=["CONFIRMED", "UNDETERMINED", "COMPROMISED"])
    asp.add_argument("--logic", default="OR", choices=["OR", "AND"])
    asp.add_argument("--scope", default="")

    ev = sub.add_parser("evaluate", help="Recompute claim qualification")
    ev.add_argument("--claim", required=True)

    rev = sub.add_parser("revoke-evidence", help="Revoke evidence, recompute dependents")
    rev.add_argument("--evidence", required=True)
    rev.add_argument("--reason", default="")

    sub.add_parser("report", help="Claim support report")

    args = parser.parse_args()
    if args.cmd == "register-claim":
        register_claim(args.id, args.description, args.scope)
    elif args.cmd == "add-support":
        add_support(args.claim, args.set_id, args.evidence, args.independence, args.logic, args.scope)
    elif args.cmd == "evaluate":
        evaluate(args.claim)
    elif args.cmd == "revoke-evidence":
        revoke_evidence(args.evidence, args.reason)
    elif args.cmd == "report":
        report()


if __name__ == "__main__":
    main()
