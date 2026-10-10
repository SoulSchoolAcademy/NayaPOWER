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


if __name__ == "__main__":
    main()
