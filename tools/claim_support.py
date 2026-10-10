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


def add_obligation_evidence(claim_id, obligation_id, evidence_id, scope, independence="UNDETERMINED", provenance=""):
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


# Migration mapping determinations
MIGRATION_RELATIONS = {
    "ENTAILS": "Old evidence fully establishes the new obligation (independently justified)",
    "PARTIALLY_SUPPORTS": "Old evidence supports part of the new obligation",
    "DOES_NOT_SUPPORT": "Old evidence does not establish the new obligation",
    "UNDETERMINED": "Cannot determine from available evidence",
}

# Migration verdicts (obligation-specific, never just PASS/FAIL)
MIGRATION_VERDICTS = {
    "CARRIED_FORWARD": "Earlier evidence fully qualifies new obligation in verified scope",
    "PARTIALLY_MIGRATED": "Some requirements established; others need proof",
    "BRIDGE_REQUIRED": "Evidence valid but compatibility/integration unproven",
    "REQUALIFIED": "Additional independent evidence now establishes obligation",
    "INSUFFICIENT_EVIDENCE": "Qualification cannot currently be established",
    "INCOMPATIBLE": "Material requirement conflicts with old evidence",
}


def migrate_split(source_obligation_id, source_revision, children):
    """
    Split migration: one obligation → several children.
    children: list of {"id": ..., "text": ..., "relation": ENTAILS|PARTIALLY_SUPPORTS|...,
                        "evidence_refs": [...], "scope": ...}
    
    Each child assessed individually. Old PASS ≠ N new PASSes.
    """
    reg = load_registry()
    source = reg.get("obligations", {}).get(source_obligation_id)
    if not source or source_revision not in source["revisions"]:
        print(f"Source {source_obligation_id}@{source_revision} not found.")
        sys.exit(1)

    migration_id = f"MIG-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
    results = []

    for child in children:
        relation = child.get("relation", "UNDETERMINED")
        if relation not in MIGRATION_RELATIONS:
            print(f"ERROR: Unknown relation '{relation}'")
            sys.exit(1)

        # Determine verdict from relation
        if relation == "ENTAILS":
            verdict = "CARRIED_FORWARD"
        elif relation == "PARTIALLY_SUPPORTS":
            verdict = "PARTIALLY_MIGRATED"
        elif relation == "DOES_NOT_SUPPORT":
            verdict = "INSUFFICIENT_EVIDENCE"
        else:
            verdict = "INSUFFICIENT_EVIDENCE"

        # Register the child as a new obligation if it doesn't exist
        child_id = child["id"]
        if child_id not in reg.get("obligations", {}):
            register_obligation(
                child_id,
                child.get("text", f"Split from {source_obligation_id}"),
                scope=child.get("scope", ""),
            )
            # Reload after registration
            reg = load_registry()

        result = {
            "child_id": child_id,
            "relation": relation,
            "relation_meaning": MIGRATION_RELATIONS[relation],
            "evidence_refs": child.get("evidence_refs", []),
            "verdict": verdict,
            "shared_lineage": f"Derived from {source_obligation_id}@{source_revision}",
        }
        results.append(result)
        print(f"  {child_id}: {relation} → {verdict}")

    certificate = {
        "event_type": "COMPOSITE_PROOF_MIGRATION",
        "migration_id": migration_id,
        "operation": "SPLIT",
        "source_obligation": f"{source_obligation_id}@{source_revision}",
        "children": results,
        "historical_receipts": "PRESERVED",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    if "migrations" not in reg:
        reg["migrations"] = {}
    reg["migrations"][migration_id] = certificate
    save_registry(reg)
    log_event(certificate)

    print(f"\nSplit migration {migration_id}: {source_obligation_id}@{source_revision} → {len(children)} children")
    print(f"  Historical source qualification: PRESERVED")
    print(f"  Old PASS was NOT automatically converted to {len(children)} new PASSes")
    return certificate


def migrate_merge(target_id, target_text, mappings, new_interactions=None):
    """
    Merge migration: several obligations → one.
    mappings: list of {"source": "OBL@rev", "target_part": ..., "relation": ...}
    new_interactions: list of new interaction requirements introduced by the merge
    
    Three green components ≠ proven integration. New interactions need their own proof.
    """
    reg = load_registry()
    migration_id = f"MIG-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"

    # Validate all sources exist
    for m in mappings:
        src = m["source"]
        if "@" in src:
            oid, rev = src.split("@")
        else:
            oid, rev = src, None
        ob = reg.get("obligations", {}).get(oid)
        if not ob:
            print(f"ERROR: Source obligation {oid} not found.")
            sys.exit(1)
        if rev and rev not in ob["revisions"]:
            print(f"ERROR: Revision {rev} not found for {oid}.")
            sys.exit(1)

    # Check mapping relations
    print(f"\nMerge mappings:")
    all_entailed = True
    for m in mappings:
        relation = m.get("relation", "UNDETERMINED")
        print(f"  {m['source']} → {m.get('target_part', '?')}: {relation}")
        if relation != "ENTAILS":
            all_entailed = False

    # New interactions introduced by merge need their own proof
    unproved = []
    if new_interactions:
        print(f"\nNew interaction requirements (need independent proof):")
        for ni in new_interactions:
            print(f"  ⚠ {ni} — NOT established by component evidence alone")
            unproved.append(ni)

    # Determine target verdict
    if all_entailed and not unproved:
        verdict = "CARRIED_FORWARD"
    elif unproved:
        verdict = "BRIDGE_REQUIRED"
    else:
        verdict = "PARTIALLY_MIGRATED"

    # Register target obligation
    if target_id not in reg.get("obligations", {}):
        register_obligation(target_id, target_text, scope="merged composite")
        reg = load_registry()

    certificate = {
        "event_type": "COMPOSITE_PROOF_MIGRATION",
        "migration_id": migration_id,
        "operation": "MERGE",
        "source_obligations": [m["source"] for m in mappings],
        "target_obligation": target_id,
        "mappings": mappings,
        "unproved_obligations": unproved,
        "target_qualification": verdict,
        "historical_receipts": "PRESERVED",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    if "migrations" not in reg:
        reg["migrations"] = {}
    reg["migrations"][migration_id] = certificate
    save_registry(reg)
    log_event(certificate)

    print(f"\nMerge migration {migration_id} → {target_id}: {verdict}")
    print(f"  {MIGRATION_VERDICTS[verdict]}")
    if unproved:
        print(f"  Component PASSes do NOT prove the merged claim until interactions are verified.")
    return certificate


# Six interaction classes for systematic discovery
INTERACTION_CLASSES = {
    "DATA_CONTRACTS": "Does one obligation supply exactly what another needs?",
    "ORDERING_TIMING": "Must operations occur in a particular order?",
    "SHARED_STATE": "Do components rely on consistent identity, versions, resources?",
    "AUTHORITY_PRIVACY": "Could combination exceed either component's permission?",
    "FAILURE_COUPLING": "Can one's retry/timeout/failure corrupt another?",
    "EMERGENT_BEHAVIOR": "Does composite assert result absent from component contracts?",
}

# Interaction proof ladder (5 levels)
PROOF_LADDER = {
    1: "Contract proof — producer guarantees meet consumer assumptions",
    2: "Pairwise integration proof — actual interface with valid/malformed/delayed/revoked inputs",
    3: "Multi-party composition proof — shared resources, ordering, cycles, concurrency",
    4: "Environment bridge proof — result applies under target config/runtime",
    5: "Independent end-to-end proof — exact broader claim with fresh admissible evidence",
}

# Merge types
MERGE_TYPES = {
    "ADMINISTRATIVE": "Unchanged requirements grouped for convenience — no new behavioral claim",
    "SEMANTIC": "New claim about cooperation, sequencing, shared state, end-to-end result",
}


def discover_interactions(claim_id, component_obligations, composite_description):
    """
    Systematic interaction discovery: five checks before generating proof obligations.
    
    1. Semantic comparison: new words (together, before, after, across, improves) signal new claims
    2. Contract comparison: producer guarantees vs consumer assumptions
    3. Dependency tracing: real handoffs, shared state, event sequences
    4. Failure analysis: what goes wrong when components are individually correct?
    5. Environment comparison: staging vs production assumptions
    """
    reg = load_registry()
    if claim_id not in reg["claims"]:
        print(f"Claim {claim_id} not found.")
        sys.exit(1)

    claim = reg["claims"][claim_id]

    # Semantic comparison: detect interaction-signaling words
    interaction_words = ["together", "before", "after", "always", "across",
                         "independently", "in production", "improves", "uses",
                         "influence", "sequence", "end-to-end", "integrated"]
    found_words = [w for w in interaction_words if w in composite_description.lower()]

    discovery = {
        "claim_id": claim_id,
        "components": component_obligations,
        "composite_description": composite_description[:200],
        "semantic_signals": found_words,
        "discovered_interactions": [],
        "assessed_at": datetime.now(timezone.utc).isoformat(),
    }

    # For each pair of components, check each interaction class
    print(f"\nInteraction discovery for {claim_id}:")
    print(f"  Components: {', '.join(component_obligations)}")
    if found_words:
        print(f"  Semantic signals: {', '.join(found_words)} → likely SEMANTIC merge")

    # Generate candidate interactions for each class
    for i, comp_a in enumerate(component_obligations):
        for comp_b in component_obligations[i+1:]:
            for class_id, question in INTERACTION_CLASSES.items():
                candidate = {
                    "participants": [comp_a, comp_b],
                    "class": class_id,
                    "discovery_question": question,
                    "status": "CANDIDATE",
                }
                discovery["discovered_interactions"].append(candidate)

    print(f"  Candidate interactions: {len(discovery['discovered_interactions'])} "
          f"({len(component_obligations)} components × {len(INTERACTION_CLASSES)} classes)")

    if "interaction_discovery" not in claim:
        claim["interaction_discovery"] = []
    claim["interaction_discovery"].append(discovery)
    save_registry(reg)

    log_event({
        "event_type": "INTERACTION_DISCOVERY",
        "claim_id": claim_id,
        "discovery": discovery,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
    return discovery


def prove_interaction(claim_id, handoff_id, proof_level, positive_test="", negative_test="",
                      invariant="", participants=None):
    """
    Issue an interaction-specific proof receipt.
    Proof level 1-5 on the ladder. Requires both positive AND negative tests.
    """
    if proof_level not in PROOF_LADDER:
        print(f"ERROR: proof_level must be 1-5")
        sys.exit(1)

    reg = load_registry()
    claim = reg["claims"].get(claim_id)
    if not claim:
        print(f"Claim {claim_id} not found.")
        sys.exit(1)

    if "interaction_proofs" not in claim:
        claim["interaction_proofs"] = {}

    # A graph edge is not proof. Both witnesses required.
    if not positive_test or not negative_test:
        print(f"WARNING: interaction proof requires BOTH positive and negative test witnesses.")
        print(f"  A system that refuses all execution does not demonstrate correct integration.")

    receipt = {
        "interaction_id": handoff_id,
        "composite_claim_id": claim_id,
        "participants": participants or [],
        "invariant": invariant[:200],
        "proof_level": proof_level,
        "proof_description": PROOF_LADDER[proof_level],
        "positive_test": positive_test[:100],
        "negative_test": negative_test[:100],
        "independent_verification": "PENDING",
        "qualification": "NOT_YET_ESTABLISHED",
        "issued_at": datetime.now(timezone.utc).isoformat(),
    }
    claim["interaction_proofs"][handoff_id] = receipt
    save_registry(reg)

    log_event({
        "event_type": "INTERACTION_PROOF_ISSUED",
        "claim_id": claim_id,
        "receipt": receipt,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })

    print(f"\nInteraction proof {handoff_id} (level {proof_level}):")
    print(f"  {PROOF_LADDER[proof_level]}")
    print(f"  Invariant: {invariant[:80]}...")
    print(f"  Positive: {positive_test[:60]}...")
    print(f"  Negative: {negative_test[:60]}...")
    print(f"  Status: NOT_YET_ESTABLISHED (pending independent verification)")
    return receipt


def verify_interaction_proof(claim_id, handoff_id, verifier="independent", result="QUALIFIED"):
    """Independent verifier qualifies or rejects an interaction proof."""
    if result not in ("QUALIFIED", "REJECTED"):
        print(f"ERROR: result must be QUALIFIED or REJECTED")
        sys.exit(1)

    reg = load_registry()
    claim = reg["claims"].get(claim_id)
    if not claim or handoff_id not in claim.get("interaction_proofs", {}):
        print(f"Interaction proof {handoff_id} not found.")
        sys.exit(1)

    proof = claim["interaction_proofs"][handoff_id]
    proof["independent_verification"] = result
    proof["verifier"] = verifier
    proof["verified_at"] = datetime.now(timezone.utc).isoformat()
    proof["qualification"] = "ESTABLISHED" if result == "QUALIFIED" else "FAILED"
    save_registry(reg)

    log_event({
        "event_type": "INTERACTION_PROOF_VERIFIED",
        "claim_id": claim_id,
        "interaction_id": handoff_id,
        "result": result,
        "verifier": verifier,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })

    print(f"{handoff_id}: independently {result} by {verifier}")
    return proof


# Six multi-party invariant categories
INVARIANT_CATEGORIES = {
    "JOINT_IDENTITY": "All participants operate for same authorized principal/target",
    "TEMPORAL_ORDERING": "Required happens-before relationships hold",
    "SHARED_CONSISTENCY": "Compatible policy, resource, evidence versions across participants",
    "AUTHORITY_NON_ESCALATION": "Combined participants cannot exceed individual authority",
    "END_TO_END_INTEGRITY": "All participants agree on actual operation and outcome",
    "FAILURE_CONTAINMENT": "One participant's failure cannot cause unauthorized side effects",
}

# Invariant kinds
INVARIANT_KINDS = ["SAFETY", "LIVENESS", "TEMPORAL"]


def register_multi_party_interaction(interaction_id, participant_obligations, join_keys,
                                      invariants, scope="", environment=""):
    """
    Register a multi-party interaction obligation (3+ participants).
    
    The key insight: pairwise PASS ≠ joint PASS. All participants must agree on
    the same execution context (decision, identity, target, action).
    
    join_keys: fields that must match across all participants
               (e.g., decision_id, principal_id, action_digest, target_id)
    invariants: list of {"id": ..., "kind": SAFETY|LIVENESS|TEMPORAL,
                          "category": ..., "predicate": ...}
    """
    reg = load_registry()

    if len(participant_obligations) < 3:
        print(f"WARNING: multi-party interaction expects 3+ participants, got {len(participant_obligations)}")

    for inv in invariants:
        if inv.get("kind") not in INVARIANT_KINDS:
            print(f"ERROR: Unknown invariant kind '{inv.get('kind')}'")
            sys.exit(1)
        if inv.get("category") not in INVARIANT_CATEGORIES:
            print(f"ERROR: Unknown category '{inv.get('category')}'")
            sys.exit(1)

    interaction = {
        "interaction_id": interaction_id,
        "revision": "v1",
        "type": "MULTI_PARTY_INTERACTION",
        "participant_obligations": participant_obligations,
        "join_keys": join_keys,
        "scope": scope[:200],
        "environment": environment,
        "invariants": [
            {
                "id": inv["id"],
                "kind": inv["kind"],
                "category": inv["category"],
                "category_question": INVARIANT_CATEGORIES[inv["category"]],
                "predicate": inv.get("predicate", "")[:200],
                "status": "UNRESOLVED",
                "positive_witness": "",
                "counterexample": "",
            }
            for inv in invariants
        ],
        "qualification": "INSUFFICIENT_EVIDENCE",
        "registered_at": datetime.now(timezone.utc).isoformat(),
    }

    if "multi_party_interactions" not in reg:
        reg["multi_party_interactions"] = {}
    reg["multi_party_interactions"][interaction_id] = interaction
    save_registry(reg)

    log_event({
        "event_type": "MULTI_PARTY_INTERACTION_REGISTERED",
        "interaction_id": interaction_id,
        "participants": participant_obligations,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })

    print(f"\nRegistered multi-party interaction {interaction_id}:")
    print(f"  Participants: {', '.join(participant_obligations)}")
    print(f"  Join keys: {', '.join(join_keys)}")
    print(f"  Invariants: {len(invariants)}")
    for inv in interaction["invariants"]:
        print(f"    [{inv['kind']}] {inv['id']}: {inv['category']}")
    print(f"  Rule: pairwise PASS does not establish joint PASS")
    return interaction


def assess_invariant(interaction_id, invariant_id, status, positive_witness="", counterexample=""):
    """
    Assess a multi-party invariant with both positive witness and counterexample.
    status: QUALIFIED, FAILED, UNRESOLVED
    """
    if status not in ("QUALIFIED", "FAILED", "UNRESOLVED"):
        print(f"ERROR: status must be QUALIFIED, FAILED, or UNRESOLVED")
        sys.exit(1)

    reg = load_registry()
    interaction = reg.get("multi_party_interactions", {}).get(interaction_id)
    if not interaction:
        print(f"Interaction {interaction_id} not found.")
        sys.exit(1)

    inv = next((i for i in interaction["invariants"] if i["id"] == invariant_id), None)
    if not inv:
        print(f"Invariant {invariant_id} not found in {interaction_id}.")
        sys.exit(1)

    inv["status"] = status
    inv["positive_witness"] = positive_witness[:200]
    inv["counterexample"] = counterexample[:200]
    inv["assessed_at"] = datetime.now(timezone.utc).isoformat()

    # Recompute overall qualification
    statuses = [i["status"] for i in interaction["invariants"]]
    if all(s == "QUALIFIED" for s in statuses):
        interaction["qualification"] = "ESTABLISHED"
    elif any(s == "FAILED" for s in statuses):
        interaction["qualification"] = "FAILED"
    elif any(s == "QUALIFIED" for s in statuses):
        interaction["qualification"] = "PARTIALLY_ESTABLISHED"
    else:
        interaction["qualification"] = "INSUFFICIENT_EVIDENCE"

    save_registry(reg)
    log_event({
        "event_type": "INVARIANT_ASSESSED",
        "interaction_id": interaction_id,
        "invariant_id": invariant_id,
        "status": status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })

    print(f"{interaction_id}/{invariant_id}: → {status}")
    if status == "QUALIFIED" and not positive_witness:
        print(f"  WARNING: qualified without positive witness")
    if status == "QUALIFIED" and not counterexample:
        print(f"  WARNING: qualified without adversarial counterexample")
    print(f"  Overall: {interaction['qualification']}")
    return inv


def check_joint_context(interaction_id, participant_contexts):
    """
    Verify that all participants agree on the same execution context.
    
    participant_contexts: {"KNOW": {"decision_id": "D-101", ...}, "LAW": {...}, "ACT": {...}}
    
    This catches the D-101/D-102 mismatch: each pair passes locally but the
    joint execution is invalid because contexts don't agree.
    """
    reg = load_registry()
    interaction = reg.get("multi_party_interactions", {}).get(interaction_id)
    if not interaction:
        print(f"Interaction {interaction_id} not found.")
        sys.exit(1)

    join_keys = interaction["join_keys"]
    mismatches = []

    # Check each join key across all participants
    for key in join_keys:
        values = {}
        for participant, ctx in participant_contexts.items():
            values[participant] = ctx.get(key, "MISSING")
        unique_values = set(values.values())
        if len(unique_values) > 1:
            mismatches.append({
                "join_key": key,
                "values": values,
            })

    if mismatches:
        print(f"\n⚠ JOINT CONTEXT MISMATCH in {interaction_id}:")
        for m in mismatches:
            print(f"  {m['join_key']}:")
            for p, v in m["values"].items():
                print(f"    {p}: {v}")
        print(f"  Pairwise receipts may be green. Joint execution is INVALID.")
        print(f"  The operation must refuse or safely requalify.")
        return False, mismatches
    else:
        print(f"\n✓ Joint context consistent in {interaction_id}:")
        print(f"  All participants agree on: {', '.join(join_keys)}")
        return True, []


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
    oe.add_argument("--independence", default="UNDETERMINED",
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

    ms = sub.add_parser("migrate-split", help="Split one obligation into children")
    ms.add_argument("--source", required=True, help="OBLIGATION_ID@revision")
    ms.add_argument("--children", required=True, help="JSON list of child specs")

    mm = sub.add_parser("migrate-merge", help="Merge obligations into one")
    mm.add_argument("--sources", required=True, help="JSON list of mappings")
    mm.add_argument("--target", required=True)
    mm.add_argument("--target-text", required=True)
    mm.add_argument("--new-interactions", default="[]", help="JSON list of new interaction requirements")

    di = sub.add_parser("discover-interactions", help="Systematic interaction discovery")
    di.add_argument("--claim", required=True)
    di.add_argument("--components", required=True, help="Comma-separated obligation IDs")
    di.add_argument("--description", required=True, help="Composite claim description")

    pi = sub.add_parser("prove-interaction", help="Issue interaction proof receipt")
    pi.add_argument("--claim", required=True)
    pi.add_argument("--handoff", required=True)
    pi.add_argument("--level", type=int, required=True, choices=[1, 2, 3, 4, 5])
    pi.add_argument("--invariant", required=True)
    pi.add_argument("--participants", default="", help="Comma-separated")
    pi.add_argument("--positive-test", default="")
    pi.add_argument("--negative-test", default="")

    vi = sub.add_parser("verify-interaction", help="Independent verification of interaction")
    vi.add_argument("--claim", required=True)
    vi.add_argument("--handoff", required=True)
    vi.add_argument("--verifier", default="independent")
    vi.add_argument("--result", required=True, choices=["QUALIFIED", "REJECTED"])

    mpi = sub.add_parser("register-multi-party", help="Register multi-party interaction")
    mpi.add_argument("--id", required=True)
    mpi.add_argument("--participants", required=True, help="Comma-separated obligation IDs")
    mpi.add_argument("--join-keys", required=True, help="Comma-separated context keys")
    mpi.add_argument("--invariants", required=True, help="JSON list of {id,kind,category,predicate}")
    mpi.add_argument("--scope", default="")
    mpi.add_argument("--environment", default="")

    ai2 = sub.add_parser("assess-invariant", help="Assess multi-party invariant")
    ai2.add_argument("--interaction", required=True)
    ai2.add_argument("--invariant", required=True)
    ai2.add_argument("--status", required=True, choices=["QUALIFIED", "FAILED", "UNRESOLVED"])
    ai2.add_argument("--positive-witness", default="")
    ai2.add_argument("--counterexample", default="")

    cjc = sub.add_parser("check-joint-context", help="Verify shared execution context")
    cjc.add_argument("--interaction", required=True)
    cjc.add_argument("--contexts", required=True, help="JSON dict of participant->context")

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
    elif args.cmd == "migrate-split":
        if "@" in args.source:
            oid, rev = args.source.split("@")
        else:
            oid, rev = args.source, "v1"
        children = json.loads(args.children)
        migrate_split(oid, rev, children)
    elif args.cmd == "migrate-merge":
        mappings = json.loads(args.sources)
        new_interactions = json.loads(args.new_interactions)
        migrate_merge(args.target, args.target_text, mappings, new_interactions)
    elif args.cmd == "discover-interactions":
        components = [c.strip() for c in args.components.split(",")]
        discover_interactions(args.claim, components, args.description)
    elif args.cmd == "prove-interaction":
        participants = [p.strip() for p in args.participants.split(",")] if args.participants else []
        prove_interaction(args.claim, args.handoff, args.level, args.positive_test,
                          args.negative_test, args.invariant, participants)
    elif args.cmd == "verify-interaction":
        verify_interaction_proof(args.claim, args.handoff, args.verifier, args.result)
    elif args.cmd == "register-multi-party":
        participants = [p.strip() for p in args.participants.split(",")]
        join_keys = [k.strip() for k in args.join_keys.split(",")]
        invariants = json.loads(args.invariants)
        register_multi_party_interaction(args.id, participants, join_keys, invariants,
                                          args.scope, args.environment)
    elif args.cmd == "assess-invariant":
        assess_invariant(args.interaction, args.invariant, args.status,
                         args.positive_witness, args.counterexample)
    elif args.cmd == "check-joint-context":
        contexts = json.loads(args.contexts)
        check_joint_context(args.interaction, contexts)


if __name__ == "__main__":
    main()
