#!/usr/bin/env python3
"""
canary_registry.py — The three-layer canary system for calibration drift detection.

From Naya 1's "Three-Layer Canary System" + "Detecting Calibration Drift":

Three populations, three jobs:
- FIXED: frozen regression tests — detect if previously correct behavior breaks
- ROLLING: representative current cases — detect if reality is changing
- ADVERSARIAL: red-team attacks — discover failure modes we haven't seen

Governing rule: Naya may learn from evaluation results, but must not train,
tune, promote, or certify itself using hidden evaluation answers.

The 10 canary families (each needs positive control, negative control,
adversarial variation, source-of-truth reference):
 1. Negation and scope
 2. Ambiguous authority
 3. Circular evidence
 4. Mixed-validity bundles
 5. Independent corroboration
 6. Interpretation reopening
 7. Risk-based quarantine
 8. Policy and model drift
 9. Concurrent eligibility changes
10. Cold-successor transfer

Usage:
    python3 tools/canary_registry.py register-family --id <n> --name <name> --description <text>
    python3 tools/canary_registry.py add-case --family <id> --set-type <fixed|rolling|adversarial>
        --visibility <open|sealed> --description <text> --expected <result>
    python3 tools/canary_registry.py run --family <id> [--set-type TYPE]
    python3 tools/canary_registry.py report
    python3 tools/canary_registry.py fingerprint
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

HOME = os.path.expanduser("~")
CANARY_DIR = os.path.join(HOME, "workspace/goals/nayapower-10-10-completion-drive/hidden_files/canary-registry")
REGISTRY_FILE = os.path.join(CANARY_DIR, "registry.json")
RUNS_FILE = os.path.join(CANARY_DIR, "runs.jsonl")

# The 10 canary families from Naya 1's spec
FAMILIES = {
    1: ("Negation and scope", "Whether meaning changes during claim extraction"),
    2: ("Ambiguous authority", "Whether uncertainty creates unauthorized permission"),
    3: ("Circular evidence", "Whether self-generated agreement becomes fake proof"),
    4: ("Mixed-validity bundles", "Whether good claims survive alongside contaminated ones"),
    5: ("Independent corroboration", "Whether derivative sources are counted as independent"),
    6: ("Interpretation reopening", "Whether genuine contradictory evidence reopens decisions"),
    7: ("Risk-based quarantine", "Whether dangerous use stops while safe work continues"),
    8: ("Policy and model drift", "Whether outdated qualification is detected"),
    9: ("Concurrent eligibility changes", "Whether ACT refuses newly quarantined dependencies"),
    10: ("Cold-successor transfer", "Whether fresh Naya preserves correct understanding and boundaries"),
}


def load_registry():
    if not os.path.exists(REGISTRY_FILE):
        return {"families": {}, "fingerprint": None}
    with open(REGISTRY_FILE) as f:
        return json.load(f)


def save_registry(reg):
    os.makedirs(CANARY_DIR, exist_ok=True)
    with open(REGISTRY_FILE, "w") as f:
        json.dump(reg, f, indent=2)


def content_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def register_family(family_id, name=None, description=None):
    reg = load_registry()
    fid = str(family_id)
    if fid in reg["families"]:
        print(f"Family {family_id} already registered.")
        return
    default_name, default_desc = FAMILIES.get(int(family_id), ("Unknown", ""))
    reg["families"][fid] = {
        "id": int(family_id),
        "name": name or default_name,
        "description": description or default_desc,
        "cases": [],
        "registered_at": datetime.now(timezone.utc).isoformat(),
    }
    save_registry(reg)
    print(f"Registered canary family {family_id}: {name or default_name}")


def add_case(family_id, set_type, visibility, description, expected):
    reg = load_registry()
    fid = str(family_id)
    if fid not in reg["families"]:
        print(f"Family {family_id} not registered. Register it first.")
        sys.exit(1)

    if set_type not in ("fixed", "rolling", "adversarial"):
        print(f"Invalid set_type: {set_type}")
        sys.exit(1)
    if visibility not in ("open", "sealed"):
        print(f"Invalid visibility: {visibility}")
        sys.exit(1)

    case_id = f"F{fid}-{set_type[0].upper()}{len(reg['families'][fid]['cases']) + 1:03d}"
    case = {
        "case_id": case_id,
        "set_type": set_type,
        "visibility": visibility,
        "description": description[:500],
        "expected": expected[:200],
        "case_hash": content_hash(description),
        "added_at": datetime.now(timezone.utc).isoformat(),
        "status": "ACTIVE",
        # Sealed cases: answer key is stored separately, not in this file
        "answer_sealed": visibility == "sealed",
    }
    reg["families"][fid]["cases"].append(case)
    save_registry(reg)
    print(f"Added {case_id} ({set_type}/{visibility}) to family {family_id}")
    if visibility == "sealed":
        print(f"  WARNING: answer key must be stored separately — not in this registry.")
    return case


def run_family(family_id, set_type=None):
    reg = load_registry()
    fid = str(family_id)
    if fid not in reg["families"]:
        print(f"Family {family_id} not registered.")
        sys.exit(1)

    cases = reg["families"][fid]["cases"]
    if set_type:
        cases = [c for c in cases if c["set_type"] == set_type]

    print(f"\nCanary family {family_id}: {reg['families'][fid]['name']}")
    print(f"Cases to run: {len(cases)}")
    for c in cases:
        if c["visibility"] == "sealed":
            print(f"  [{c['case_id']}] SEALED — requires independent evaluator, skipping automated run")
        else:
            print(f"  [{c['case_id']}] OPEN — {c['description'][:60]}...")
            print(f"    Expected: {c['expected'][:60]}...")
            print(f"    Status: DEFINED (execution requires test implementation)")


def fingerprint():
    """Generate a calibration fingerprint: policy + model + verifier + environment."""
    import subprocess
    reg = load_registry()

    # Get current main SHA as policy proxy
    try:
        r = subprocess.run(
            ["git", "ls-remote", "https://github.com/SoulSchoolAcademy/NayaPOWER.git", "refs/heads/main"],
            capture_output=True, text=True, timeout=30
        )
        main_sha = r.stdout.strip().split()[0][:10] if r.stdout.strip() else "unknown"
    except Exception:
        main_sha = "unknown"

    fp = {
        "policy_version": f"main-{main_sha}",
        "registry_version": content_hash(json.dumps(reg.get("families", {}), sort_keys=True)),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "families_count": len(reg.get("families", {})),
        "total_cases": sum(len(f["cases"]) for f in reg.get("families", {}).values()),
    }
    fp["fingerprint"] = content_hash(json.dumps(fp, sort_keys=True))
    print(json.dumps(fp, indent=2))
    return fp


def report():
    reg = load_registry()
    families = reg.get("families", {})
    if not families:
        print("No canary families registered.")
        print("\nThe 10 families from Naya 1's spec are defined but not yet registered.")
        print("Run: python3 tools/canary_registry.py register-family --id <1-10>")
        return

    print(f"\n{'='*60}")
    print("CANARY REGISTRY REPORT")
    print(f"{'='*60}")
    total_cases = 0
    for fid in sorted(families.keys(), key=int):
        f = families[fid]
        cases = f["cases"]
        total_cases += len(cases)
        by_type = {}
        by_vis = {"open": 0, "sealed": 0}
        for c in cases:
            by_type[c["set_type"]] = by_type.get(c["set_type"], 0) + 1
            by_vis[c["visibility"]] += 1
        print(f"\n  Family {fid}: {f['name']}")
        print(f"    Cases: {len(cases)} | " + " | ".join(f"{k}:{v}" for k, v in by_type.items()))
        print(f"    Visibility: open={by_vis['open']}, sealed={by_vis['sealed']}")
    print(f"\n  Total: {len(families)} families, {total_cases} cases")


# Canary integrity states (Naya 1's compromise lifecycle):
# SEALED → SUSPECT → COMPROMISED → RETIRED → REPLACED
# Key rule: never erase compromised evidence. Never use it to certify fresh learning.
INTEGRITY_STATES = {
    "SEALED": "Protected holdout with independently established provenance",
    "SUSPECT": "Credible exposure, lineage, or reviewer-integrity concern exists",
    "COMPROMISED": "Independent qualification no longer defensible",
    "RETIRED": "Removed from blind qualification, retained for diagnostics",
    "REPLACED": "New independent set has taken its evaluation role",
}

# Four compromise mechanisms
COMPROMISE_TYPES = {
    "ANSWER_LEAKAGE": "Worker gained access to hidden expected results",
    "DUPLICATE_LINEAGE": "Cases derive from training/development examples",
    "EVALUATOR_CONTAMINATION": "Verifier influenced by builder outputs",
    "REPEATED_EXPOSURE": "System memorized repeatedly presented holdout",
}


def report_compromise(family_id, case_id, compromise_type, evidence, reporter="unknown"):
    """
    DETECT → CONTAIN: Report a canary compromise.
    Creates append-only event, marks case SUSPECT, suspends its independent-proof use.
    """
    if compromise_type not in COMPROMISE_TYPES:
        print(f"ERROR: Unknown type '{compromise_type}'. Valid: {', '.join(COMPROMISE_TYPES.keys())}")
        sys.exit(1)

    reg = load_registry()
    fid = str(family_id)
    if fid not in reg["families"]:
        print(f"Family {family_id} not found.")
        sys.exit(1)

    # Find the case
    case = None
    for c in reg["families"][fid]["cases"]:
        if c["case_id"] == case_id:
            case = c
            break
    if not case:
        print(f"Case {case_id} not found in family {family_id}.")
        sys.exit(1)

    # Create append-only compromise event
    event = {
        "event_type": "CANARY_INDEPENDENCE_COMPROMISED",
        "event_id": f"COMP-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        "family_id": int(family_id),
        "case_id": case_id,
        "compromise_type": compromise_type,
        "compromise_description": COMPROMISE_TYPES[compromise_type],
        "evidence_refs": [evidence[:200]],
        "reporter": reporter,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "previous_state": case.get("integrity_state", "SEALED"),
    }

    # CONTAIN: mark SUSPECT, suspend independent-proof use
    # Preserve the case — never delete. Only its qualification status changes.
    case["integrity_state"] = "SUSPECT"
    case["compromise_event"] = event["event_id"]
    case["independent_proof_suspended"] = True

    # Append event to log
    events_file = os.path.join(CANARY_DIR, "compromise_events.jsonl")
    os.makedirs(CANARY_DIR, exist_ok=True)
    with open(events_file, "a") as f:
        f.write(json.dumps(event) + "\n")

    save_registry(reg)
    print(f"Compromise {event['event_id']}: {case_id} marked SUSPECT")
    print(f"  Type: {compromise_type} — {COMPROMISE_TYPES[compromise_type]}")
    print(f"  Independent proof use: SUSPENDED (case preserved for diagnostics)")
    return event


def confirm_compromise(family_id, case_id, confirmed=True):
    """TRACE → confirm or clear. COMPROMISED or back to SEALED."""
    reg = load_registry()
    fid = str(family_id)
    case = next((c for c in reg["families"][fid]["cases"] if c["case_id"] == case_id), None)
    if not case:
        print(f"Case {case_id} not found.")
        sys.exit(1)

    if confirmed:
        case["integrity_state"] = "COMPROMISED"
        print(f"{case_id}: SUSPECT → COMPROMISED")
        print(f"  Independent qualification: DISQUALIFIED")
        print(f"  Diagnostic use: RETAINED (never erase compromised evidence)")
    else:
        case["integrity_state"] = "SEALED"
        case["independent_proof_suspended"] = False
        print(f"{case_id}: SUSPECT → SEALED (cleared)")
    save_registry(reg)


def retire_case(family_id, case_id, replacement_case_id=None):
    """RETIRED → REPLACED: remove from blind qualification, optionally link replacement."""
    reg = load_registry()
    fid = str(family_id)
    case = next((c for c in reg["families"][fid]["cases"] if c["case_id"] == case_id), None)
    if not case:
        print(f"Case {case_id} not found.")
        sys.exit(1)

    case["integrity_state"] = "RETIRED"
    case["retired_at"] = datetime.now(timezone.utc).isoformat()
    if replacement_case_id:
        case["integrity_state"] = "REPLACED"
        case["replacement_case_id"] = replacement_case_id
        print(f"{case_id}: RETIRED → REPLACED by {replacement_case_id}")
    else:
        print(f"{case_id}: RETIRED (no replacement yet)")
    save_registry(reg)


def track_exposure(family_id, case_id):
    """Exposure accounting: count presentations of sealed cases."""
    reg = load_registry()
    fid = str(family_id)
    case = next((c for c in reg["families"][fid]["cases"] if c["case_id"] == case_id), None)
    if not case:
        print(f"Case {case_id} not found.")
        sys.exit(1)

    case["exposure_count"] = case.get("exposure_count", 0) + 1
    case["last_exposure"] = datetime.now(timezone.utc).isoformat()
    save_registry(reg)
    print(f"{case_id}: exposure count = {case['exposure_count']}")
    # Warning: no universal safe number, but flag for review
    if case["exposure_count"] >= 10 and case.get("visibility") == "sealed":
        print(f"  WARNING: sealed case exposed {case['exposure_count']}× — review independence")
    return case["exposure_count"]


# Qualification verdicts (Naya 1's selective revocation):
# Evidence-contribution revocation ≠ qualification revocation.
# A case can lose its right to certify without the lesson being declared false.
QUALIFICATION_VERDICTS = {
    "UNAFFECTED": "No material dependency on compromised evidence",
    "REQUALIFIED": "Remaining independent evidence meets acceptance standard",
    "DOWNGRADED": "Narrower claim remains supportable",
    "INSUFFICIENT_DATA": "Evidence valid but no longer sufficient",
    "SUSPENDED": "Independence or blast radius unresolved",
    "REVOKED": "Required evidence condition has failed",
}

# Scope confidence levels
SCOPE_STATUS = {
    "CONFIRMED_BOUNDED": "Affected population defensibly identified",
    "POTENTIALLY_BROADER": "Other cases may share exposure",
    "UNKNOWN": "Cannot reliably determine blast radius",
}


def register_qualification(qual_id, description, required_families, acceptance_criteria=""):
    """
    Register a qualification claim that depends on specific canary families.
    This tracks WHAT the evaluation established, separate from the cases themselves.
    """
    reg = load_registry()
    if "qualifications" not in reg:
        reg["qualifications"] = {}

    if qual_id in reg["qualifications"]:
        print(f"Qualification {qual_id} already registered.")
        return

    reg["qualifications"][qual_id] = {
        "id": qual_id,
        "description": description[:300],
        "required_families": required_families,  # list of family IDs
        "acceptance_criteria": acceptance_criteria[:200],
        "status": "ACTIVE",
        "verdict": None,
        "registered_at": datetime.now(timezone.utc).isoformat(),
        "history": [],
    }
    save_registry(reg)
    print(f"Registered qualification {qual_id}: depends on families {required_families}")
    return reg["qualifications"][qual_id]


def compromise_family(family_id, compromise_type, evidence, scope_status="CONFIRMED_BOUNDED", reporter="unknown"):
    """
    Partial compromise at the FAMILY level.
    Marks all cases in the family, then recalculates affected qualifications.
    """
    if scope_status not in SCOPE_STATUS:
        print(f"ERROR: Unknown scope '{scope_status}'")
        sys.exit(1)

    reg = load_registry()
    fid = str(family_id)
    if fid not in reg["families"]:
        print(f"Family {family_id} not found.")
        sys.exit(1)

    family = reg["families"][fid]
    affected_cases = [c["case_id"] for c in family["cases"]]

    # Create the partial-compromise event
    event = {
        "event_type": "CANARY_PARTIAL_COMPROMISE",
        "incident_id": f"CCI-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        "family_id": int(family_id),
        "cause": compromise_type,
        "affected_cases": affected_cases,
        "scope_status": scope_status,
        "scope_description": SCOPE_STATUS[scope_status],
        "evidence_refs": [evidence[:200]],
        "reporter": reporter,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    # Mark all cases in family
    for c in family["cases"]:
        c["integrity_state"] = "COMPROMISED" if scope_status == "CONFIRMED_BOUNDED" else "SUSPECT"
        c["independent_proof_suspended"] = True

    # Append event
    events_file = os.path.join(CANARY_DIR, "compromise_events.jsonl")
    os.makedirs(CANARY_DIR, exist_ok=True)
    with open(events_file, "a") as f:
        f.write(json.dumps(event) + "\n")

    print(f"Family {family_id} compromise: {event['incident_id']}")
    print(f"  Affected cases: {len(affected_cases)}")
    print(f"  Scope: {scope_status} — {SCOPE_STATUS[scope_status]}")

    # Recalculate qualifications
    if scope_status == "UNKNOWN":
        print(f"  WARNING: blast radius unknown — cannot declare unaffected families independent")
        print(f"  All dependent qualifications → SUSPENDED pending investigation")
        for qid, q in reg.get("qualifications", {}).items():
            if int(family_id) in q["required_families"]:
                q["verdict"] = "SUSPENDED"
                q["status"] = "SUSPENDED"
                q["history"].append({
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "event": event["incident_id"],
                    "verdict": "SUSPENDED",
                    "reason": "Blast radius unknown — cannot verify independence of remaining families",
                })
                print(f"    Qualification {qid}: → SUSPENDED")
    else:
        for qid, q in reg.get("qualifications", {}).items():
            if int(family_id) not in q["required_families"]:
                # Explicitly record unaffected — don't leave it ambiguous
                q["verdict"] = "UNAFFECTED"
                q["history"].append({
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "event": event["incident_id"],
                    "verdict": "UNAFFECTED",
                    "reason": "No dependency on compromised family",
                })
                print(f"    Qualification {qid}: → UNAFFECTED (no dependency)")
                continue
            remaining = [f for f in q["required_families"] if f != int(family_id)]
            if not remaining:
                # All required families compromised
                q["verdict"] = "REVOKED"
                q["status"] = "REVOKED"
                reason = "All required evidence families compromised"
            elif len(remaining) < len(q["required_families"]):
                # Partial — check if remaining meets acceptance
                # For now: downgrade unless explicitly requalified
                q["verdict"] = "DOWNGRADED"
                q["status"] = "DOWNGRADED"
                reason = f"Narrowed to families {remaining}; original broad claim no longer supported"
            else:
                q["verdict"] = "UNAFFECTED"
                reason = "No dependency on compromised family"

            q["history"].append({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "event": event["incident_id"],
                "verdict": q["verdict"],
                "reason": reason,
            })
            print(f"    Qualification {qid}: → {q['verdict']} ({reason[:60]}...)")

    save_registry(reg)
    return event


def main():
    parser = argparse.ArgumentParser(description="Three-layer canary system")
    sub = parser.add_subparsers(dest="cmd", required=True)

    rf = sub.add_parser("register-family", help="Register a canary family")
    rf.add_argument("--id", required=True)
    rf.add_argument("--name", default=None)
    rf.add_argument("--description", default=None)

    ac = sub.add_parser("add-case", help="Add a test case")
    ac.add_argument("--family", required=True)
    ac.add_argument("--set-type", required=True, choices=["fixed", "rolling", "adversarial"])
    ac.add_argument("--visibility", required=True, choices=["open", "sealed"])
    ac.add_argument("--description", required=True)
    ac.add_argument("--expected", required=True)

    rn = sub.add_parser("run", help="Run canary cases")
    rn.add_argument("--family", required=True)
    rn.add_argument("--set-type", default=None)

    sub.add_parser("report", help="Registry report")
    sub.add_parser("fingerprint", help="Calibration fingerprint")

    comp = sub.add_parser("compromise", help="Report canary compromise (DETECT→CONTAIN)")
    comp.add_argument("--family", required=True)
    comp.add_argument("--case", required=True)
    comp.add_argument("--type", required=True,
                      choices=["ANSWER_LEAKAGE", "DUPLICATE_LINEAGE",
                               "EVALUATOR_CONTAMINATION", "REPEATED_EXPOSURE"])
    comp.add_argument("--evidence", required=True)
    comp.add_argument("--reporter", default="unknown")

    conf = sub.add_parser("confirm", help="Confirm or clear compromise (TRACE)")
    conf.add_argument("--family", required=True)
    conf.add_argument("--case", required=True)
    conf.add_argument("--confirmed", action="store_true")

    ret = sub.add_parser("retire", help="Retire/replace case (REPLACE→REQUALIFY)")
    ret.add_argument("--family", required=True)
    ret.add_argument("--case", required=True)
    ret.add_argument("--replacement", default=None)

    exp = sub.add_parser("expose", help="Track sealed case exposure")
    exp.add_argument("--family", required=True)
    exp.add_argument("--case", required=True)

    reg_q = sub.add_parser("register-qual", help="Register a qualification claim")
    reg_q.add_argument("--id", required=True)
    reg_q.add_argument("--description", required=True)
    reg_q.add_argument("--families", required=True, help="Comma-separated family IDs")
    reg_q.add_argument("--criteria", default="")

    comp_f = sub.add_parser("compromise-family", help="Family-level partial compromise")
    comp_f.add_argument("--family", required=True)
    comp_f.add_argument("--type", required=True,
                        choices=["ANSWER_LEAKAGE", "DUPLICATE_LINEAGE",
                                 "EVALUATOR_CONTAMINATION", "REPEATED_EXPOSURE"])
    comp_f.add_argument("--evidence", required=True)
    comp_f.add_argument("--scope", default="CONFIRMED_BOUNDED",
                        choices=["CONFIRMED_BOUNDED", "POTENTIALLY_BROADER", "UNKNOWN"])
    comp_f.add_argument("--reporter", default="unknown")

    args = parser.parse_args()
    if args.cmd == "register-family":
        register_family(args.id, args.name, args.description)
    elif args.cmd == "add-case":
        add_case(args.family, args.set_type, args.visibility, args.description, args.expected)
    elif args.cmd == "run":
        run_family(args.family, args.set_type)
    elif args.cmd == "report":
        report()
    elif args.cmd == "fingerprint":
        fingerprint()
    elif args.cmd == "compromise":
        report_compromise(args.family, args.case, args.type, args.evidence, args.reporter)
    elif args.cmd == "confirm":
        confirm_compromise(args.family, args.case, args.confirmed)
    elif args.cmd == "retire":
        retire_case(args.family, args.case, args.replacement)
    elif args.cmd == "expose":
        track_exposure(args.family, args.case)
    elif args.cmd == "register-qual":
        families = [int(f.strip()) for f in args.families.split(",")]
        register_qualification(args.id, args.description, families, args.criteria)
    elif args.cmd == "compromise-family":
        compromise_family(args.family, args.type, args.evidence, args.scope, args.reporter)


if __name__ == "__main__":
    main()
