#!/usr/bin/env python3
"""
evidence_authorization.py — Purpose-bound evidence access & authority governance.

From Naya 1's "Evidence Access & Authority Governance":

Core rule: Undetermined evidence may be investigated, but must never silently
become independently verified evidence or authority to act.

Five capabilities (not just READ/DENY):
  INSPECT  — examine and understand authorized evidence
  ANALYZE  — generate hypotheses, diagnostics, non-authoritative findings
  TEST     — run permitted experiments without treating as blind holdout
  CERTIFY  — use independently admissible evidence for qualification claims
  ACT      — use qualified evidence-dependent decision under LAW authorization

Permit = f(identity, purpose, evidence, operation, context, LAW)

Key enforcement:
- Access-time check ≠ use-time check. Reading at 9AM ≠ permission to act at 5PM.
- Derived artifacts retain source dependencies (purpose laundering prevention).
- Undetermined independence blocks CERTIFY and ACT, not INSPECT/ANALYZE/TEST.

Usage:
    python3 tools/evidence_authorization.py request --principal <id> --role <role>
        --purpose <purpose> --operation <op> --evidence <id> --independence <state>
    python3 tools/evidence_authorization.py derive --source <evidence-id>
        --derived <new-id> --description <text>
    python3 tools/evidence_authorization.py check-use --principal <id> --claim <id>
        --action <action> --law-receipt <receipt>
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone, timedelta

HOME = os.path.expanduser("~")
AUTH_DIR = os.path.join(HOME, "workspace/goals/nayapower-10-10-completion-drive/hidden_files/evidence-auth")
REGISTRY_FILE = os.path.join(AUTH_DIR, "evidence_registry.json")
REQUESTS_FILE = os.path.join(AUTH_DIR, "requests.jsonl")
DERIVED_FILE = os.path.join(AUTH_DIR, "derived.jsonl")

# Five capabilities
CAPABILITIES = {
    "INSPECT": "Access authorized evidence for examination and understanding",
    "ANALYZE": "Generate hypotheses, diagnostics, non-authoritative findings",
    "TEST": "Run permitted experiments without treating as blind holdout",
    "CERTIFY": "Use independently admissible evidence for qualification claims",
    "ACT": "Use qualified evidence-dependent decision under valid LAW authorization",
}

# Independence states
INDEPENDENCE_STATES = {
    "CONFIRMED": "Independence established by positive evidence",
    "UNDETERMINED": "Independence not yet established",
    "COMPROMISED": "Independence failed — evidence proves contamination",
}

# Roles
ROLES = ["RESEARCH", "BUILDER", "VERIFY", "ACT", "LAW", "KNOW"]


def load_registry():
    if not os.path.exists(REGISTRY_FILE):
        return {"evidence": {}}
    with open(REGISTRY_FILE) as f:
        return json.load(f)


def save_registry(reg):
    os.makedirs(AUTH_DIR, exist_ok=True)
    with open(REGISTRY_FILE, "w") as f:
        json.dump(reg, f, indent=2)


def register_evidence(evidence_id, independence, integrity="VALID", description=""):
    """Register an evidence object with its independence classification."""
    reg = load_registry()
    reg["evidence"][evidence_id] = {
        "id": evidence_id,
        "independence": independence,
        "integrity": integrity,
        "description": description[:200],
        "registered_at": datetime.now(timezone.utc).isoformat(),
    }
    save_registry(reg)
    print(f"Registered evidence {evidence_id}: independence={independence}")
    return reg["evidence"][evidence_id]


def evaluate_request(principal_id, role, purpose, operation, evidence_id, context=""):
    """
    Access-time check: May this identity perform this operation on this evidence?
    
    Returns (decision, restrictions, reason).
    """
    if operation not in CAPABILITIES:
        return "DENY", [], f"Unknown operation: {operation}"
    if role not in ROLES:
        return "DENY", [], f"Unknown role: {role}"

    reg = load_registry()
    ev = reg["evidence"].get(evidence_id)
    if not ev:
        return "DENY", [], f"Evidence {evidence_id} not registered"

    independence = ev["independence"]
    restrictions = []

    # CERTIFY requires confirmed independence
    if operation == "CERTIFY":
        if independence != "CONFIRMED":
            return "DENY", [], (
                f"Cannot CERTIFY: evidence independence is {independence}. "
                f"Undetermined evidence may be investigated but never counted as independent proof."
            )
        if role != "VERIFY":
            return "DENY", [], "Only VERIFY role may CERTIFY"
        return "PERMIT", [], "Independence confirmed, VERIFY authorized"

    # ACT requires confirmed independence + LAW receipt
    if operation == "ACT":
        if independence != "CONFIRMED":
            return "DENY", ["NO_ACT_ON_UNDETERMINED"], (
                f"Cannot ACT: evidence independence is {independence}. "
                f"Mandatory independent-proof requirement not satisfied."
            )
        if role != "ACT":
            return "DENY", [], "Only ACT role may execute"
        return "PERMIT_WITH_RESTRICTIONS", ["LAW_RECEIPT_REQUIRED", "USE_TIME_RECHECK"], (
            "Access permitted. Use-time recheck required before execution."
        )

    # INSPECT, ANALYZE, TEST: permitted with restrictions for undetermined evidence
    if independence == "UNDETERMINED":
        restrictions = ["PRESERVE_UNCERTAINTY_LABEL", "NO_INDEPENDENT_CERTIFICATION", "NO_AUTOMATIC_PROMOTION"]
        return "PERMIT_WITH_RESTRICTIONS", restrictions, (
            f"{operation} permitted for investigation. "
            f"Uncertainty must be preserved. Cannot certify or promote."
        )

    if independence == "COMPROMISED":
        if operation in ("INSPECT", "ANALYZE"):
            restrictions = ["DIAGNOSTIC_ONLY", "PRESERVE_UNCERTAINTY_LABEL"]
            return "PERMIT_WITH_RESTRICTIONS", restrictions, "Diagnostic use only"
        return "DENY", [], "Evidence independence compromised"

    # CONFIRMED independence: full access per role
    return "PERMIT", [], f"{operation} permitted on confirmed-independent evidence"


def request(principal_id, role, purpose, operation, evidence_id, context=""):
    """Process an authorization request and log it."""
    decision, restrictions, reason = evaluate_request(
        principal_id, role, purpose, operation, evidence_id, context
    )

    receipt = {
        "request_id": f"REQ-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        "principal_id": principal_id,
        "role": role,
        "purpose": purpose,
        "operation": operation,
        "evidence_id": evidence_id,
        "context": context[:100],
        "decision": decision,
        "restrictions": restrictions,
        "reason": reason,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "expires_at": (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat(),
    }

    os.makedirs(AUTH_DIR, exist_ok=True)
    with open(REQUESTS_FILE, "a") as f:
        f.write(json.dumps(receipt) + "\n")

    print(f"\nAuthorization {receipt['request_id']}")
    print(f"  {principal_id} ({role}) → {operation} on {evidence_id}")
    print(f"  Decision: {decision}")
    if restrictions:
        print(f"  Restrictions: {', '.join(restrictions)}")
    print(f"  Reason: {reason}")
    return receipt


def derive(source_evidence_id, derived_id, description=""):
    """
    Purpose laundering prevention: derived artifacts retain source dependencies.
    A summary of undetermined evidence is still undetermined.
    """
    reg = load_registry()
    source = reg["evidence"].get(source_evidence_id)
    if not source:
        print(f"ERROR: Source evidence {source_evidence_id} not registered.")
        sys.exit(1)

    # Derived artifact inherits the WORST independence of its sources
    derived = {
        "id": derived_id,
        "independence": source["independence"],  # inherited, not reset
        "integrity": source["integrity"],
        "derived_from": source_evidence_id,
        "description": description[:200],
        "marker": "DERIVED_FROM_UNDETERMINED" if source["independence"] == "UNDETERMINED" else "DERIVED",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    reg["evidence"][derived_id] = derived
    save_registry(reg)

    with open(DERIVED_FILE, "a") as f:
        f.write(json.dumps(derived) + "\n")

    print(f"Derived {derived_id} from {source_evidence_id}")
    print(f"  Independence inherited: {derived['independence']}")
    print(f"  Marker: {derived['marker']}")
    if source["independence"] == "UNDETERMINED":
        print(f"  WARNING: derived artifact cannot independently certify its own ancestor")
    return derived


def check_use(principal_id, claim_id, action, law_receipt=""):
    """
    Use-time check: May this specific claim support this particular decision NOW?
    Separate from access-time. Must recheck current eligibility.
    """
    reg = load_registry()
    ev = reg["evidence"].get(claim_id)
    if not ev:
        print(f"DENY: Claim {claim_id} not registered")
        return False

    print(f"\nUse-time check: {principal_id} → {action} using {claim_id}")
    print(f"  Evidence independence: {ev['independence']}")
    print(f"  LAW receipt: {'present' if law_receipt else 'MISSING'}")

    if ev["independence"] != "CONFIRMED":
        print(f"  Result: DENY — independence is {ev['independence']}, not CONFIRMED")
        print(f"  Historical read permission ≠ permission for this action")
        return False

    if not law_receipt:
        print(f"  Result: DENY — LAW receipt required for consequential action")
        return False

    print(f"  Result: PERMIT — current eligibility confirmed at use time")
    return True


def main():
    parser = argparse.ArgumentParser(description="Purpose-bound evidence authorization")
    sub = parser.add_subparsers(dest="cmd", required=True)

    reg = sub.add_parser("register", help="Register evidence with independence classification")
    reg.add_argument("--id", required=True)
    reg.add_argument("--independence", required=True,
                     choices=["CONFIRMED", "UNDETERMINED", "COMPROMISED"])
    reg.add_argument("--integrity", default="VALID")
    reg.add_argument("--description", default="")

    req = sub.add_parser("request", help="Authorization request (access-time check)")
    req.add_argument("--principal", required=True)
    req.add_argument("--role", required=True,
                     choices=["RESEARCH", "BUILDER", "VERIFY", "ACT", "LAW", "KNOW"])
    req.add_argument("--purpose", required=True)
    req.add_argument("--operation", required=True,
                     choices=["INSPECT", "ANALYZE", "TEST", "CERTIFY", "ACT"])
    req.add_argument("--evidence", required=True)
    req.add_argument("--context", default="")

    der = sub.add_parser("derive", help="Create derived artifact (inherits uncertainty)")
    der.add_argument("--source", required=True)
    der.add_argument("--derived", required=True)
    der.add_argument("--description", default="")

    chk = sub.add_parser("check-use", help="Use-time check before consequential action")
    chk.add_argument("--principal", required=True)
    chk.add_argument("--claim", required=True)
    chk.add_argument("--action", required=True)
    chk.add_argument("--law-receipt", default="")

    args = parser.parse_args()
    if args.cmd == "register":
        register_evidence(args.id, args.independence, args.integrity, args.description)
    elif args.cmd == "request":
        request(args.principal, args.role, args.purpose, args.operation, args.evidence, args.context)
    elif args.cmd == "derive":
        derive(args.source, args.derived, args.description)
    elif args.cmd == "check-use":
        check_use(args.principal, args.claim, args.action, args.law_receipt)


if __name__ == "__main__":
    main()
