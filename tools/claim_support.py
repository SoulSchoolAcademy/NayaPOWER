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


# Five proof obligations for composite qualification audit
AUDIT_OBLIGATIONS = {
    "COMPONENT_CORRECTNESS": "Each component satisfies its stated behavior in tested scope",
    "INTERFACE_COMPATIBILITY": "Outputs satisfy the next component's input contract",
    "INTERACTION_CORRECTNESS": "Ordering, shared state, concurrency preserve invariants",
    "ENVIRONMENT_APPLICABILITY": "Test evidence applies to target runtime",
    "COMPOSITE_SUFFICIENCY": "Verified obligations actually establish the broader claim",
}

# Four-tier qualification verdicts
QUALIFICATION_TIERS = {
    "COMPONENT_QUALIFIED": "Individual behaviors established",
    "INTEGRATION_QUALIFIED": "Composition established within defined environment",
    "TRANSFER_QUALIFIED": "Qualification justified for target environment via bridge evidence",
    "PRODUCTION_PROVEN": "Independently demonstrated in actual production",
}

# Environment difference classifications
ENV_DIFF_CLASSIFICATIONS = {
    "IMMATERIAL": "Demonstrably cannot affect the qualified property",
    "COVERED": "Independent evidence establishes property survives the difference",
    "REQUIRES_BRIDGE": "Additional testing or formal argument needed",
    "INCOMPATIBLE": "Original evidence does not qualify target environment",
}


def add_interaction(claim_id, handoff_id, sender, receiver, invariant, audit_test=""):
    """
    Record a required node-to-node interaction with its invariant.
    e.g., LAW → ACT: unexpired, applicable permission required
    """
    reg = load_registry()
    if claim_id not in reg["claims"]:
        print(f"Claim {claim_id} not found.")
        sys.exit(1)

    claim = reg["claims"][claim_id]
    if "interactions" not in claim:
        claim["interactions"] = {}

    claim["interactions"][handoff_id] = {
        "sender": sender,
        "receiver": receiver,
        "required_invariant": invariant[:200],
        "audit_test": audit_test[:200],
        "status": "UNRESOLVED",
        "assessed_at": None,
    }
    save_registry(reg)
    print(f"Added interaction {handoff_id}: {sender} → {receiver}")
    print(f"  Invariant: {invariant[:80]}...")
    return claim["interactions"][handoff_id]


def assess_interaction(claim_id, handoff_id, status, evidence=""):
    """Assess whether an interaction's invariant holds."""
    if status not in ("QUALIFIED", "UNRESOLVED", "FAILED"):
        print(f"ERROR: status must be QUALIFIED, UNRESOLVED, or FAILED")
        sys.exit(1)

    reg = load_registry()
    claim = reg["claims"].get(claim_id)
    if not claim or handoff_id not in claim.get("interactions", {}):
        print(f"Interaction {handoff_id} not found in {claim_id}.")
        sys.exit(1)

    claim["interactions"][handoff_id]["status"] = status
    claim["interactions"][handoff_id]["evidence"] = evidence[:200]
    claim["interactions"][handoff_id]["assessed_at"] = datetime.now(timezone.utc).isoformat()
    save_registry(reg)
    print(f"{handoff_id}: → {status}")
    return True


def assess_environment_bridge(claim_id, source_env, target_env, differences):
    """
    Assess staging → production (or any env → env) transfer.
    differences: list of {"dimension": ..., "source": ..., "target": ..., "classification": ...}
    """
    reg = load_registry()
    if claim_id not in reg["claims"]:
        print(f"Claim {claim_id} not found.")
        sys.exit(1)

    claim = reg["claims"][claim_id]
    for d in differences:
        if d.get("classification") not in ENV_DIFF_CLASSIFICATIONS:
            print(f"ERROR: Unknown classification '{d.get('classification')}'")
            sys.exit(1)

    unresolved = [d for d in differences if d["classification"] in ("REQUIRES_BRIDGE", "INCOMPATIBLE")]
    incompatible = [d for d in differences if d["classification"] == "INCOMPATIBLE"]

    if incompatible:
        bridge_status = "INCOMPATIBLE"
    elif unresolved:
        bridge_status = "INCOMPLETE"
    else:
        bridge_status = "COMPLETE"

    claim["environment_bridge"] = {
        "source": source_env,
        "target": target_env,
        "status": bridge_status,
        "differences": differences,
        "unresolved": [d["dimension"] for d in unresolved],
        "assessed_at": datetime.now(timezone.utc).isoformat(),
    }
    save_registry(reg)

    print(f"\nEnvironment bridge {source_env} → {target_env}: {bridge_status}")
    for d in differences:
        print(f"  {d['dimension']}: {d['classification']} — {ENV_DIFF_CLASSIFICATIONS[d['classification']][:50]}")
    return claim["environment_bridge"]


def audit_composite(claim_id):
    """
    Full composite qualification audit.
    Requires: component sufficiency + interaction sufficiency + environment applicability.
    Issues the highest justified tier, preserves narrower valid conclusions.
    """
    reg = load_registry()
    if claim_id not in reg["claims"]:
        print(f"Claim {claim_id} not found.")
        sys.exit(1)

    claim = reg["claims"][claim_id]
    if not claim.get("composite"):
        print(f"Claim {claim_id} is not composite.")
        sys.exit(1)

    # Recompute component coverage
    evaluate_composite(claim_id)
    claim = reg["claims"][claim_id]  # reload after recompute
    comp_qual = claim["qualification"]

    # Check interactions
    interactions = claim.get("interactions", {})
    int_qualified = all(i["status"] == "QUALIFIED" for i in interactions.values()) if interactions else True
    int_failed = any(i["status"] == "FAILED" for i in interactions.values())

    # Check environment bridge
    bridge = claim.get("environment_bridge", {})
    bridge_status = bridge.get("status", "NOT_ASSESSED")

    # Determine highest justified tier
    # Tier 1: components
    if comp_qual["status"] not in ("FULLY_QUALIFIED", "PARTIALLY_QUALIFIED", "QUALIFIED"):
        tier = None
        verdict = "INSUFFICIENT_EVIDENCE"
        statement = "Component obligations not met."
    elif int_failed:
        tier = "COMPONENT_QUALIFIED"
        verdict = "COMPONENT_QUALIFIED"
        statement = "Components qualified. Interaction FAILED — composition not established."
    elif not int_qualified:
        tier = "COMPONENT_QUALIFIED"
        verdict = "COMPONENT_QUALIFIED"
        statement = "Components qualified. Interactions unresolved — integration not proven."
    elif bridge_status == "INCOMPATIBLE":
        tier = "INTEGRATION_QUALIFIED"
        verdict = "INTEGRATION_QUALIFIED"
        statement = "Integration qualified in source env. Target env incompatible."
    elif bridge_status == "INCOMPLETE":
        tier = "INTEGRATION_QUALIFIED"
        verdict = "INTEGRATION_QUALIFIED"
        statement = "Integration qualified in source env. Environment transfer incomplete."
    elif bridge_status == "COMPLETE":
        tier = "TRANSFER_QUALIFIED"
        verdict = "TRANSFER_QUALIFIED"
        statement = "Qualification transferred to target env via bridge evidence."
    else:
        tier = "COMPONENT_QUALIFIED"
        verdict = "COMPONENT_QUALIFIED"
        statement = "Components qualified. Environment bridge not assessed."

    # Special: if all components + interactions + bridge complete in production → PRODUCTION_PROVEN
    if (comp_qual["status"] == "FULLY_QUALIFIED" and int_qualified and
        bridge.get("target") == "production" and bridge_status == "COMPLETE"):
        tier = "PRODUCTION_PROVEN"
        verdict = "PRODUCTION_PROVEN"
        statement = "Independently demonstrated in production."

    audit = {
        "claim_id": claim_id,
        "tier": tier,
        "verdict": verdict,
        "statement": statement,
        "component_status": comp_qual["status"],
        "interaction_status": "QUALIFIED" if int_qualified else ("FAILED" if int_failed else "UNRESOLVED"),
        "bridge_status": bridge_status,
        "narrower_conclusions_preserved": True,
        "audited_at": datetime.now(timezone.utc).isoformat(),
    }
    claim["composite_audit"] = audit
    save_registry(reg)

    log_event({
        "event_type": "COMPOSITE_AUDITED",
        "claim_id": claim_id,
        "audit": audit,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })

    print(f"\n{'='*60}")
    print(f"COMPOSITE AUDIT: {claim_id}")
    print(f"{'='*60}")
    print(f"  Verdict: {verdict}")
    print(f"  {QUALIFICATION_TIERS.get(tier, 'No tier achieved')}")
    print(f"  Components: {comp_qual['status']}")
    print(f"  Interactions: {audit['interaction_status']}")
    print(f"  Environment bridge: {bridge_status}")
    print(f"  {statement}")
    print(f"  Narrower valid conclusions: PRESERVED")
    return audit


# Obligation lifecycle states (append-only, never overwrite)
OBLIGATION_LIFECYCLE = {
    "PROPOSED": "New or revised requirement awaiting review",
    "ACTIVE": "Ratified and applicable within effective scope",
    "DEPRECATED": "Still applicable in legacy contexts, replacement scheduled",
    "SUPERSEDED": "Replaced by newer obligation for defined contexts",
    "RETIRED": "No longer governs new qualifications in retired scope",
    "WITHDRAWN": "Obligation found erroneous; authority withdrawn",
}

# Change classifications for migration
CHANGE_CLASSES = {
    "EDITORIAL": "No semantic change — retain qualifications",
    "STRENGTHENED": "Stronger criterion — require additional proof",
    "WEAKENED": "Weaker criterion — preserve history, review authorization",
    "INTERFACE_CHANGED": "Behavior changed — requalify affected obligations",
    "INTERFACE_RENAMED": "Semantics preserved — carry forward with compatibility doc",
    "ENV_CHANGED": "Environment assumptions changed — require bridge evidence",
    "SPLIT": "One obligation → several — map old proof to exact new obligations",
    "MERGED": "Several → one — verify conjunction establishes merged claim",
    "REMOVED": "Requirement removed — retire in scope, preserve receipts",
    "INVALID": "Prior obligation invalid — withdraw authority, reassess dependents",
}


def register_obligation(obligation_id, requirement_text, scope="", acceptance_predicate="",
                        proof_standard="", assumptions=""):
    """Register a new proof obligation at revision v1."""
    reg = load_registry()
    if "obligations" not in reg:
        reg["obligations"] = {}

    if obligation_id in reg["obligations"]:
        print(f"Obligation {obligation_id} exists. Use revise_obligation for new revision.")
        return

    reg["obligations"][obligation_id] = {
        "id": obligation_id,
        "revisions": {
            "v1": {
                "revision_id": "v1",
                "requirement_text": requirement_text[:500],
                "scope": scope[:200],
                "acceptance_predicate": acceptance_predicate[:200],
                "proof_standard": proof_standard[:200],
                "assumptions": assumptions[:200],
                "lifecycle": "PROPOSED",
                "effective_from": datetime.now(timezone.utc).isoformat(),
                "effective_until": None,
                "recorded_at": datetime.now(timezone.utc).isoformat(),
                "supersedes": None,
                "events": [],
            }
        },
        "current_revision": "v1",
    }
    save_registry(reg)
    print(f"Registered obligation {obligation_id} at v1 (PROPOSED)")
    return reg["obligations"][obligation_id]


def transition_obligation(obligation_id, revision, new_state, reason=""):
    """Move an obligation revision through its lifecycle (append-only events)."""
    if new_state not in OBLIGATION_LIFECYCLE:
        print(f"ERROR: Unknown state '{new_state}'")
        sys.exit(1)

    reg = load_registry()
    ob = reg["obligations"].get(obligation_id)
    if not ob or revision not in ob["revisions"]:
        print(f"Obligation {obligation_id} revision {revision} not found.")
        sys.exit(1)

    rev = ob["revisions"][revision]
    old_state = rev["lifecycle"]
    rev["lifecycle"] = new_state
    rev["events"].append({
        "from": old_state,
        "to": new_state,
        "reason": reason[:200],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
    if new_state in ("RETIRED", "WITHDRAWN", "SUPERSEDED"):
        rev["effective_until"] = datetime.now(timezone.utc).isoformat()

    save_registry(reg)
    log_event({
        "event_type": "OBLIGATION_TRANSITION",
        "obligation_id": obligation_id,
        "revision": revision,
        "from": old_state,
        "to": new_state,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
    print(f"{obligation_id} {revision}: {old_state} → {new_state}")
    print(f"  {OBLIGATION_LIFECYCLE[new_state]}")
    return rev


def revise_obligation(obligation_id, new_requirement_text, change_class, scope="",
                      acceptance_predicate="", proof_standard="", assumptions="",
                      effective_from=None):
    """
    Create a new immutable revision. Semantic change = new revision, never edit in place.
    Returns migration assessment: what proof carries forward, what's needed.
    """
    if change_class not in CHANGE_CLASSES:
        print(f"ERROR: Unknown change class '{change_class}'")
        sys.exit(1)

    reg = load_registry()
    ob = reg["obligations"].get(obligation_id)
    if not ob:
        print(f"Obligation {obligation_id} not found.")
        sys.exit(1)

    old_rev_id = ob["current_revision"]
    old_rev = ob["revisions"][old_rev_id]
    new_rev_num = len(ob["revisions"]) + 1
    new_rev_id = f"v{new_rev_num}"

    # Bitemporal: effective time vs recorded time
    recorded_at = datetime.now(timezone.utc).isoformat()

    new_rev = {
        "revision_id": new_rev_id,
        "requirement_text": new_requirement_text[:500],
        "scope": scope[:200] or old_rev["scope"],
        "acceptance_predicate": acceptance_predicate[:200] or old_rev["acceptance_predicate"],
        "proof_standard": proof_standard[:200] or old_rev["proof_standard"],
        "assumptions": assumptions[:200] or old_rev["assumptions"],
        "lifecycle": "PROPOSED",
        "effective_from": effective_from or recorded_at,
        "effective_until": None,
        "recorded_at": recorded_at,
        "supersedes": old_rev_id,
        "events": [],
    }
    ob["revisions"][new_rev_id] = new_rev
    ob["current_revision"] = new_rev_id

    # Migration assessment based on change class
    migration = {
        "change_class": change_class,
        "change_description": CHANGE_CLASSES[change_class],
        "reusable_evidence": [],
        "new_proof_required": [],
        "historical_qualification": "PRESERVED",
    }

    if change_class == "EDITORIAL":
        migration["reusable_evidence"] = ["ALL_PRIOR"]
        migration["new_proof_required"] = []
    elif change_class == "STRENGTHENED":
        migration["reusable_evidence"] = ["PARTIAL — prior proof covers original conditions"]
        migration["new_proof_required"] = ["ADDITIONAL — new strengthened conditions"]
    elif change_class == "INTERFACE_CHANGED":
        migration["reusable_evidence"] = ["UNCHANGED_PARTS — if semantically verified"]
        migration["new_proof_required"] = ["AFFECTED_SENDER_RECEIVER_INTERACTION"]
    elif change_class == "ENV_CHANGED":
        migration["reusable_evidence"] = ["SOURCE_ENV_RESULTS"]
        migration["new_proof_required"] = ["BRIDGE_EVIDENCE_FOR_MATERIAL_DIFFERENCES"]
    elif change_class in ("SPLIT", "MERGED"):
        migration["reusable_evidence"] = ["MAPPED — to exact new obligations"]
        migration["new_proof_required"] = ["COMPOSITION_VERIFICATION"]
    elif change_class == "INVALID":
        migration["reusable_evidence"] = []
        migration["new_proof_required"] = ["FULL_REASSESSMENT"]
        migration["historical_qualification"] = "AUTHORITY_WITHDRAWN"

    # Supersede the old revision
    old_rev["lifecycle"] = "SUPERSEDED"
    old_rev["effective_until"] = new_rev["effective_from"]
    old_rev["events"].append({
        "from": "ACTIVE",
        "to": "SUPERSEDED",
        "reason": f"Superseded by {new_rev_id} ({change_class})",
        "timestamp": recorded_at,
    })

    save_registry(reg)
    log_event({
        "event_type": "PROOF_OBLIGATION_SUPERSEDED",
        "obligation_id": obligation_id,
        "previous_revision": old_rev_id,
        "new_revision": new_rev_id,
        "change_class": change_class,
        "migration_assessment": migration,
        "timestamp": recorded_at,
    })

    print(f"\n{obligation_id}: {old_rev_id} → {new_rev_id} ({change_class})")
    print(f"  {CHANGE_CLASSES[change_class]}")
    print(f"  Historical {old_rev_id} qualification: {migration['historical_qualification']}")
    print(f"  Reusable: {migration['reusable_evidence']}")
    print(f"  New proof required: {migration['new_proof_required']}")
    return new_rev, migration


def obligation_status(obligation_id):
    """Show full revision history and current state."""
    reg = load_registry()
    ob = reg["obligations"].get(obligation_id)
    if not ob:
        print(f"Obligation {obligation_id} not found.")
        return
    print(f"\nObligation {obligation_id} (current: {ob['current_revision']})")
    for rev_id, rev in sorted(ob["revisions"].items()):
        print(f"  {rev_id}: {rev['lifecycle']}")
        print(f"    {rev['requirement_text'][:80]}...")
        print(f"    Effective: {rev['effective_from'][:10]} → {rev['effective_until'][:10] if rev['effective_until'] else 'present'}")
        print(f"    Recorded: {rev['recorded_at'][:19]}")
        if rev["supersedes"]:
            print(f"    Supersedes: {rev['supersedes']}")


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

    ai = sub.add_parser("add-interaction", help="Record required node handoff")
    ai.add_argument("--claim", required=True)
    ai.add_argument("--handoff", required=True)
    ai.add_argument("--sender", required=True)
    ai.add_argument("--receiver", required=True)
    ai.add_argument("--invariant", required=True)
    ai.add_argument("--audit-test", default="")

    si = sub.add_parser("assess-interaction", help="Assess interaction invariant")
    si.add_argument("--claim", required=True)
    si.add_argument("--handoff", required=True)
    si.add_argument("--status", required=True, choices=["QUALIFIED", "UNRESOLVED", "FAILED"])
    si.add_argument("--evidence", default="")

    eb = sub.add_parser("env-bridge", help="Assess environment transfer")
    eb.add_argument("--claim", required=True)
    eb.add_argument("--source", required=True)
    eb.add_argument("--target", required=True)
    eb.add_argument("--differences", required=True, help="JSON list of {dimension,source,target,classification}")

    au = sub.add_parser("audit", help="Full composite qualification audit")
    au.add_argument("--claim", required=True)

    ro = sub.add_parser("register-obligation", help="Register proof obligation")
    ro.add_argument("--id", required=True)
    ro.add_argument("--text", required=True)
    ro.add_argument("--scope", default="")
    ro.add_argument("--predicate", default="")
    ro.add_argument("--standard", default="")
    ro.add_argument("--assumptions", default="")

    to = sub.add_parser("transition-obligation", help="Lifecycle transition")
    to.add_argument("--id", required=True)
    to.add_argument("--revision", required=True)
    to.add_argument("--state", required=True,
                    choices=["PROPOSED", "ACTIVE", "DEPRECATED", "SUPERSEDED", "RETIRED", "WITHDRAWN"])
    to.add_argument("--reason", default="")

    vo = sub.add_parser("revise-obligation", help="Create new immutable revision")
    vo.add_argument("--id", required=True)
    vo.add_argument("--text", required=True)
    vo.add_argument("--change-class", required=True,
                    choices=["EDITORIAL", "STRENGTHENED", "WEAKENED", "INTERFACE_CHANGED",
                             "INTERFACE_RENAMED", "ENV_CHANGED", "SPLIT", "MERGED",
                             "REMOVED", "INVALID"])
    vo.add_argument("--scope", default="")
    vo.add_argument("--effective-from", default=None)

    so = sub.add_parser("obligation-status", help="Show obligation history")
    so.add_argument("--id", required=True)

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
    elif args.cmd == "add-interaction":
        add_interaction(args.claim, args.handoff, args.sender, args.receiver,
                        args.invariant, args.audit_test)
    elif args.cmd == "assess-interaction":
        assess_interaction(args.claim, args.handoff, args.status, args.evidence)
    elif args.cmd == "env-bridge":
        differences = json.loads(args.differences)
        assess_environment_bridge(args.claim, args.source, args.target, differences)
    elif args.cmd == "audit":
        audit_composite(args.claim)
    elif args.cmd == "register-obligation":
        register_obligation(args.id, args.text, args.scope, args.predicate,
                            args.standard, args.assumptions)
    elif args.cmd == "transition-obligation":
        transition_obligation(args.id, args.revision, args.state, args.reason)
    elif args.cmd == "revise-obligation":
        revise_obligation(args.id, args.text, args.change_class, args.scope,
                          effective_from=args.effective_from)
    elif args.cmd == "obligation-status":
        obligation_status(args.id)


if __name__ == "__main__":
    main()
