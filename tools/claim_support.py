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


# Scope dimensions (Naya 1's scope-limited truth):
# Every claim and evidence contribution is assessed across these dimensions.
# A mismatch in any dimension = scope limitation, not necessarily evidence failure.
SCOPE_DIMENSIONS = [
    "component",    # which nodes/parts (e.g., KNOW vs ALL_NINE)
    "environment",  # staging vs production
    "population",   # which cases/executions
    "behavior",     # what behavior was tested
    "time",         # when / ongoing vs specific run
    "conditions",   # operating conditions
    "outcome",      # what outcome was established
]

# Region verdicts for each scoped region of a claim
REGION_VERDICTS = {
    "SUPPORTED": "Evidence meets required standard in this region",
    "REFUTED": "Valid evidence contradicts the claim in this region",
    "CONFLICTED": "Material evidence disagrees, cannot yet reconcile",
    "UNDETERMINED": "Evidence absent or insufficient",
    "NOT_APPLICABLE": "Outside the claim's actual domain",
}

# Support relationship types
SUPPORT_RELATIONSHIPS = {
    "FULLY_SUPPORTS": "Evidence establishes the claim within its stated scope",
    "PARTIALLY_SUPPORTS": "Evidence supports a narrower proposition, not the full claim",
    "CONTRADICTS": "Evidence refutes the claim in the tested region",
    "IRRELEVANT": "Evidence does not address the claim's scope",
}


def add_scope_region(claim_id, region_id, scope, verdict, evidence_id="", notes=""):
    """
    Add a scoped region assessment to a claim.
    Divides the claim's scope into independently assessed regions.
    """
    if verdict not in REGION_VERDICTS:
        print(f"ERROR: Unknown verdict '{verdict}'. Valid: {', '.join(REGION_VERDICTS.keys())}")
        sys.exit(1)

    reg = load_registry()
    if claim_id not in reg["claims"]:
        print(f"Claim {claim_id} not found.")
        sys.exit(1)

    claim = reg["claims"][claim_id]
    if "scope_regions" not in claim:
        claim["scope_regions"] = []

    # scope is a dict of dimension -> value
    region = {
        "region_id": region_id,
        "scope": scope,
        "verdict": verdict,
        "verdict_description": REGION_VERDICTS[verdict],
        "evidence_id": evidence_id,
        "notes": notes[:200],
        "assessed_at": datetime.now(timezone.utc).isoformat(),
    }
    claim["scope_regions"].append(region)
    save_registry(reg)

    log_event({
        "event_type": "SCOPE_REGION_ASSESSED",
        "claim_id": claim_id,
        "region_id": region_id,
        "verdict": verdict,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })

    print(f"{claim_id}/{region_id}: {verdict} — {REGION_VERDICTS[verdict]}")
    return region


def assess_scope_match(claim_id, evidence_id, claim_scope, evidence_scope):
    """
    Compute scope mismatch between what was claimed and what was tested.
    Returns the dimensions where evidence is narrower than the claim.
    """
    mismatches = []
    for dim in SCOPE_DIMENSIONS:
        claim_val = claim_scope.get(dim, "")
        ev_val = evidence_scope.get(dim, "")
        if claim_val and ev_val and claim_val != ev_val:
            # Evidence is narrower if it's a subset/specific instance
            mismatches.append({
                "dimension": dim,
                "claimed": claim_val,
                "evidence_covers": ev_val,
            })

    reg = load_registry()
    if claim_id in reg["claims"]:
        claim = reg["claims"][claim_id]
        if "scope_assessments" not in claim:
            claim["scope_assessments"] = []
        claim["scope_assessments"].append({
            "evidence_id": evidence_id,
            "mismatches": mismatches,
            "assessed_at": datetime.now(timezone.utc).isoformat(),
        })
        save_registry(reg)

    if mismatches:
        print(f"\nScope mismatch for {claim_id} (evidence {evidence_id}):")
        for m in mismatches:
            print(f"  {m['dimension']}: claimed '{m['claimed']}' but evidence covers '{m['evidence_covers']}'")
        print(f"  → PARTIALLY_SUPPORTS. Broader claim remains UNDETERMINED outside evidence scope.")
    else:
        print(f"\nNo scope mismatch: evidence covers the claimed scope.")
    return mismatches


def strongest_conclusion(claim_id):
    """
    Compute the strongest defensible conclusion from scoped regions.
    Never claims more than the evidence establishes.
    """
    reg = load_registry()
    if claim_id not in reg["claims"]:
        print(f"Claim {claim_id} not found.")
        sys.exit(1)

    claim = reg["claims"][claim_id]
    regions = claim.get("scope_regions", [])

    if not regions:
        print(f"{claim_id}: no scope regions assessed")
        return None

    supported = [r for r in regions if r["verdict"] == "SUPPORTED"]
    refuted = [r for r in regions if r["verdict"] == "REFUTED"]
    conflicted = [r for r in regions if r["verdict"] == "CONFLICTED"]
    undetermined = [r for r in regions if r["verdict"] == "UNDETERMINED"]

    conclusion = {
        "claim_id": claim_id,
        "supported_regions": [r["region_id"] for r in supported],
        "refuted_regions": [r["region_id"] for r in refuted],
        "conflicted_regions": [r["region_id"] for r in conflicted],
        "undetermined_regions": [r["region_id"] for r in undetermined],
        "computed_at": datetime.now(timezone.utc).isoformat(),
    }

    # The strongest defensible conclusion
    if refuted:
        conclusion["overall"] = "PARTIALLY_REFUTED"
        conclusion["statement"] = (
            f"Claim refuted in {len(refuted)} region(s). "
            f"Supported in {len(supported)} region(s). "
            f"Undetermined in {len(undetermined)} region(s)."
        )
    elif supported and not undetermined and not conflicted:
        conclusion["overall"] = "FULLY_SUPPORTED_IN_SCOPE"
        conclusion["statement"] = f"All {len(supported)} assessed regions supported."
    elif supported:
        conclusion["overall"] = "PARTIALLY_SUPPORTED"
        conclusion["statement"] = (
            f"Supported in {len(supported)} region(s): {', '.join(conclusion['supported_regions'])}. "
            f"Broader claim beyond these regions remains UNDETERMINED — not established."
        )
    else:
        conclusion["overall"] = "INSUFFICIENT_EVIDENCE"
        conclusion["statement"] = "No regions currently supported by evidence."

    print(f"\nStrongest defensible conclusion for {claim_id}:")
    print(f"  {conclusion['overall']}")
    print(f"  {conclusion['statement']}")
    print(f"  Rule: never claim more than evidence establishes.")

    log_event({
        "event_type": "STRONGEST_CONCLUSION_COMPUTED",
        "claim_id": claim_id,
        "conclusion": conclusion,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
    return conclusion


# Compatibility dimensions for combining evidence sources.
# Two sources can only be combined when ALL compatibility checks pass.
COMPATIBILITY_DIMENSIONS = [
    "predicate",      # same thing being tested?
    "policy",         # same policy version requirements?
    "runtime",        # compatible runtime versions?
    "environment",    # staging vs production — not interchangeable
    "time_period",    # compatible time periods?
    "population",     # compatible test populations?
    "provenance",     # independent where required?
]


def register_composite_claim(claim_id, description, obligations, composition_rule="ALL_REQUIRED"):
    """
    Register a composite claim decomposed into proof obligations.
    obligations: list of obligation IDs (e.g., nine node names)
    composition_rule: ALL_REQUIRED (conjunction) or ANY_SUFFICIENT (disjunction)
    """
    reg = load_registry()
    if claim_id in reg["claims"]:
        print(f"Claim {claim_id} already registered — use existing claim.")
        claim = reg["claims"][claim_id]
    else:
        claim = {
            "id": claim_id,
            "description": description[:300],
            "support_sets": [],
            "historical_dependencies": [],
            "qualification": {"status": "UNEVALUATED", "basis": None},
            "registered_at": datetime.now(timezone.utc).isoformat(),
        }
        reg["claims"][claim_id] = claim

    claim["composite"] = True
    claim["obligations"] = obligations
    claim["composition_rule"] = composition_rule
    claim["obligation_evidence"] = {}  # obligation_id -> list of evidence
    claim["cross_requirements"] = []   # e.g., handoffs, interactions
    save_registry(reg)
    print(f"Registered composite claim {claim_id}: {len(obligations)} obligations, rule={composition_rule}")
    return claim


def add_obligation_evidence(claim_id, obligation_id, evidence_id, scope, independence="CONFIRMED", provenance=""):
    """Record that evidence supports a specific obligation within a composite claim."""
    reg = load_registry()
    if claim_id not in reg["claims"]:
        print(f"Claim {claim_id} not found.")
        sys.exit(1)

    claim = reg["claims"][claim_id]
    if not claim.get("composite"):
        print(f"Claim {claim_id} is not composite. Use register_composite_claim first.")
        sys.exit(1)

    if obligation_id not in claim["obligations"]:
        print(f"WARNING: {obligation_id} not in declared obligations for {claim_id}")

    if "obligation_evidence" not in claim:
        claim["obligation_evidence"] = {}
    if obligation_id not in claim["obligation_evidence"]:
        claim["obligation_evidence"][obligation_id] = []

    claim["obligation_evidence"][obligation_id].append({
        "evidence_id": evidence_id,
        "scope": scope,
        "independence": independence,
        "provenance": provenance[:100],
        "added_at": datetime.now(timezone.utc).isoformat(),
    })
    save_registry(reg)
    print(f"  {obligation_id} ← {evidence_id} [{independence}, scope={scope}]")
    return True


def check_compatibility(evidence_list):
    """
    Check if evidence sources are compatible for combination.
    Returns (compatible, issues).
    """
    if len(evidence_list) < 2:
        return True, []

    issues = []
    # Check provenance independence: different evidence IDs sharing provenance = not independent
    # Same evidence covering multiple obligations is fine (not double-counted as separate sources)
    ev_by_provenance = {}
    for e in evidence_list:
        prov = e.get("provenance", "")
        eid = e.get("evidence_id", "")
        if prov:
            if prov not in ev_by_provenance:
                ev_by_provenance[prov] = set()
            ev_by_provenance[prov].add(eid)
    shared = {p: ids for p, ids in ev_by_provenance.items() if len(ids) > 1}
    if shared:
        issues.append(f"Shared provenance across different evidence: {shared} — not independently sourced")

    # Check scope compatibility
    scopes = [e.get("scope", "") for e in evidence_list]
    if len(set(scopes)) > 1:
        issues.append(f"Mixed scopes: {set(scopes)} — staging and production not interchangeable")

    # Check independence
    compromised = [e["evidence_id"] for e in evidence_list if e.get("independence") == "COMPROMISED"]
    if compromised:
        issues.append(f"Compromised evidence: {compromised}")

    return len(issues) == 0, issues


def evaluate_composite(claim_id):
    """
    Evaluate a composite claim: coverage ∧ admissibility ∧ compatibility ∧ composition.
    
    Coverage: does combined evidence cover all required obligations?
    Composition: does satisfying individual obligations entail the broader claim?
    """
    reg = load_registry()
    if claim_id not in reg["claims"]:
        print(f"Claim {claim_id} not found.")
        sys.exit(1)

    claim = reg["claims"][claim_id]
    if not claim.get("composite"):
        print(f"Claim {claim_id} is not composite.")
        sys.exit(1)

    obligations = claim["obligations"]
    ob_ev = claim.get("obligation_evidence", {})
    rule = claim.get("composition_rule", "ALL_REQUIRED")

    # Coverage: which obligations have confirmed-independent evidence?
    covered = []
    uncovered = []
    for ob in obligations:
        ev_list = ob_ev.get(ob, [])
        confirmed = [e for e in ev_list if e.get("independence") == "CONFIRMED"]
        if confirmed:
            covered.append(ob)
        else:
            uncovered.append(ob)

    # Compatibility: check all evidence together
    all_evidence = []
    for ev_list in ob_ev.values():
        all_evidence.extend(ev_list)
    compatible, compat_issues = check_compatibility(all_evidence)

    # Composition validity: cross-requirements (handoffs, interactions)
    cross_reqs = claim.get("cross_requirements", [])
    cross_met = len(cross_reqs) == 0  # simplified: no cross-reqs = vacuously met

    # Compute verdict
    coverage_complete = len(uncovered) == 0
    
    if rule == "ALL_REQUIRED":
        if coverage_complete and compatible and cross_met:
            status = "FULLY_QUALIFIED"
            statement = f"All {len(obligations)} obligations covered with compatible evidence."
        elif covered:
            status = "PARTIALLY_QUALIFIED"
            statement = (
                f"Covered {len(covered)}/{len(obligations)} obligations: {', '.join(covered)}. "
                f"Missing: {', '.join(uncovered) if uncovered else 'none'}. "
                f"Broader claim NOT established — coverage is necessary but not sufficient."
            )
        else:
            status = "INSUFFICIENT_EVIDENCE"
            statement = "No obligations currently covered."
    else:  # ANY_SUFFICIENT
        if covered:
            status = "QUALIFIED"
            statement = f"At least one obligation covered: {covered[0]}"
        else:
            status = "INSUFFICIENT_EVIDENCE"
            statement = "No obligations covered."

    # Breadth, depth, integration
    breadth = f"{len(covered)}/{len(obligations)} distinct obligations"
    depth = f"{len(all_evidence)} evidence contributions"
    integration = "ESTABLISHED" if cross_met else "NOT_ESTABLISHED"

    qualification = {
        "status": status,
        "covered_obligations": covered,
        "uncovered_obligations": uncovered,
        "compatibility": "COMPATIBLE" if compatible else "INCOMPATIBLE",
        "compatibility_issues": compat_issues,
        "composition_valid": cross_met,
        "breadth": breadth,
        "depth": depth,
        "integration": integration,
        "statement": statement,
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
    }
    claim["qualification"] = qualification
    save_registry(reg)

    log_event({
        "event_type": "COMPOSITE_EVALUATED",
        "claim_id": claim_id,
        "qualification": qualification,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })

    print(f"\nComposite evaluation for {claim_id}:")
    print(f"  Status: {status}")
    print(f"  Breadth: {breadth} | Depth: {depth} | Integration: {integration}")
    print(f"  Compatibility: {'✓' if compatible else '✗ ' + '; '.join(compat_issues)}")
    if uncovered:
        print(f"  Missing: {', '.join(uncovered)}")
    print(f"  {statement}")
    return qualification


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

    sr = sub.add_parser("add-region", help="Add scoped region assessment")
    sr.add_argument("--claim", required=True)
    sr.add_argument("--region", required=True)
    sr.add_argument("--scope", required=True, help="JSON dict of scope dimensions")
    sr.add_argument("--verdict", required=True,
                    choices=["SUPPORTED", "REFUTED", "CONFLICTED", "UNDETERMINED", "NOT_APPLICABLE"])
    sr.add_argument("--evidence", default="")
    sr.add_argument("--notes", default="")

    sm = sub.add_parser("scope-match", help="Compute scope mismatch")
    sm.add_argument("--claim", required=True)
    sm.add_argument("--evidence", required=True)
    sm.add_argument("--claim-scope", required=True, help="JSON dict")
    sm.add_argument("--evidence-scope", required=True, help="JSON dict")

    sc = sub.add_parser("strongest", help="Compute strongest defensible conclusion")
    sc.add_argument("--claim", required=True)

    cc = sub.add_parser("register-composite", help="Register composite claim with obligations")
    cc.add_argument("--id", required=True)
    cc.add_argument("--description", required=True)
    cc.add_argument("--obligations", required=True, help="Comma-separated obligation IDs")
    cc.add_argument("--rule", default="ALL_REQUIRED", choices=["ALL_REQUIRED", "ANY_SUFFICIENT"])

    oe = sub.add_parser("add-obligation-evidence", help="Record evidence for obligation")
    oe.add_argument("--claim", required=True)
    oe.add_argument("--obligation", required=True)
    oe.add_argument("--evidence", required=True)
    oe.add_argument("--scope", required=True)
    oe.add_argument("--independence", default="CONFIRMED",
                    choices=["CONFIRMED", "UNDETERMINED", "COMPROMISED"])
    oe.add_argument("--provenance", default="")

    ec = sub.add_parser("evaluate-composite", help="Evaluate composite claim")
    ec.add_argument("--claim", required=True)

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
    elif args.cmd == "add-region":
        scope = json.loads(args.scope)
        add_scope_region(args.claim, args.region, scope, args.verdict, args.evidence, args.notes)
    elif args.cmd == "scope-match":
        claim_scope = json.loads(args.claim_scope)
        evidence_scope = json.loads(args.evidence_scope)
        assess_scope_match(args.claim, args.evidence, claim_scope, evidence_scope)
    elif args.cmd == "strongest":
        strongest_conclusion(args.claim)
    elif args.cmd == "register-composite":
        obligations = [o.strip() for o in args.obligations.split(",")]
        register_composite_claim(args.id, args.description, obligations, args.rule)
    elif args.cmd == "add-obligation-evidence":
        add_obligation_evidence(args.claim, args.obligation, args.evidence,
                                args.scope, args.independence, args.provenance)
    elif args.cmd == "evaluate-composite":
        evaluate_composite(args.claim)


if __name__ == "__main__":
    main()
