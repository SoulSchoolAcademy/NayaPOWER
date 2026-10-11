#!/usr/bin/env python3
"""UD-06 — CLAIM ONLY WHAT THE EVIDENCE COVERS (absorbs D15, D16).

Every claim a Naya makes must carry exactly the evidence that covers it —
no more, no less. Unknowns are labeled unknown, never converted into passes
or failures. Summaries carry what they do NOT claim.

Core rules (from D15/D16):
- Evidence supports a claim only within its demonstrated scope. Scope
  dimensions: environment, time, population, runtime, policy, provenance.
  "40 staging tests passed" does not prove production is safe.
- The quantifier is part of the claim: 8/9 verified nodes is SUPPORTED for
  those eight, not PROVEN for nine.
- A verified counterexample cannot be outvoted by positive examples.
- QUALIFIED = Coverage AND Admissibility AND Compatibility AND
  Composition-validity. Overlapping sources are never double-counted
  (deduplicated by content hash).
- Only verification-kind artifacts (test_run, measurement, inspection,
  external_record) can carry a claim to PROVEN. Reviews and bare assertions
  cap at SUPPORTED.
- Unknown is labeled unknown. Asserting above the evidence raises
  ClaimRejected.

Grades: UNKNOWN < SUPPORTED < PROVEN. CONTESTED/REFUTED sit off the scale:
asserting SUPPORTED or PROVEN over them is inflation and is refused.
Underclaiming (asserting below the computed grade) is always allowed.

Stdlib only.
"""
import json

SCOPE_DIMS = ("environment", "time", "population", "runtime", "policy",
              "provenance")

# Artifact kinds strong enough to carry an obligation to PROVEN.
VERIFICATION_KINDS = {"test_run", "measurement", "inspection",
                      "external_record"}
# Weaker kinds: admissible as support, but cap the claim at SUPPORTED.
NON_VERIFICATION_KINDS = {"review", "assertion"}

GRADE_RANK = {"UNKNOWN": 0, "SUPPORTED": 1, "PROVEN": 2}

NONCLAIM_MARKERS = ("does not claim", "not established", "unknown",
                    "not proven", "unverified", "no admissible")


class ClaimRejected(Exception):
    """Raised when an asserted grade exceeds what the evidence covers."""

    def __init__(self, claim_id, asserted, computed, reasons):
        self.claim_id = claim_id
        self.asserted = asserted
        self.computed = computed
        self.reasons = reasons
        super().__init__(
            "ClaimRejected: claim '%s' asserted %s but evidence covers %s. %s"
            % (claim_id, asserted, computed, "; ".join(reasons)))


def dedupe_evidence(evidence):
    """Drop overlapping sources by content hash. Returns (kept, dropped_ids)."""
    seen = {}
    dropped = []
    for ev in evidence:
        h = ev.get("content_hash") or json.dumps(ev.get("scope", {}),
                                                 sort_keys=True)
        if h in seen:
            dropped.append(ev.get("id"))
        else:
            seen[h] = ev
    return list(seen.values()), dropped


def covers(ev, obligation):
    """True iff this evidence admissibly covers this obligation's scope."""
    if not ev.get("admissible", True):
        return False
    if ev.get("predicate") != obligation.get("predicate"):
        return False
    required = obligation.get("required_scope", {})
    scope = ev.get("scope", {})
    for dim, value in required.items():
        if scope.get(dim) != value:
            return False
    return True


def grade_obligation(obligation, evidence):
    """Verdict for one proof obligation: SUPPORTED / REFUTED / CONFLICTED /
    UNDETERMINED, with the exact coverage that was demonstrated."""
    covering = [e for e in evidence if covers(e, obligation)]
    supporting = [e["id"] for e in covering if e.get("supports", True)]
    refuting = [e["id"] for e in covering if not e.get("supports", True)]
    if supporting and refuting:
        verdict = "CONFLICTED"
    elif refuting:
        verdict = "REFUTED"
    elif supporting:
        verdict = "SUPPORTED"
    else:
        verdict = "UNDETERMINED"
    demonstrated = {}
    for e in covering:
        for dim in SCOPE_DIMS:
            if dim in e.get("scope", {}):
                demonstrated.setdefault(dim, set()).add(e["scope"][dim])
    return {
        "obligation_id": obligation["id"],
        "description": obligation.get("description", ""),
        "verdict": verdict,
        "supporting": supporting,
        "refuting": refuting,
        "demonstrated_scope": {k: sorted(v) for k, v in demonstrated.items()},
    }


def compatibility_gate(obligation_verdicts, evidence_by_id):
    """Cross-part composition check: all supporting evidence must agree on
    every scope dimension it demonstrates. Returns (ok, problems)."""
    problems = []
    supporting = []
    for v in obligation_verdicts:
        if v["verdict"] == "SUPPORTED":
            supporting.extend(v["supporting"])
    for dim in SCOPE_DIMS:
        values = {evidence_by_id[eid].get("scope", {}).get(dim)
                  for eid in supporting}
        values.discard(None)
        if len(values) > 1:
            problems.append(
                "incompatible %s across parts: %s (cannot compose into one "
                "conclusion)" % (dim, sorted(values)))
    return (not problems), problems


def _has_verification_kind(v, evidence_by_id):
    return any(evidence_by_id[eid].get("kind") in VERIFICATION_KINDS
               for eid in v["supporting"])


def grade_claim(claim):
    """Grade the whole claim. Returns a verdict dict carrying its non-claims."""
    obligations = claim.get("obligations", [])
    evidence, dropped = dedupe_evidence(claim.get("evidence", []))
    evidence_by_id = {e["id"]: e for e in evidence}

    verdicts = [grade_obligation(o, evidence) for o in obligations]
    by_verdict = {}
    for v in verdicts:
        by_verdict.setdefault(v["verdict"], []).append(v)

    non_claims = []
    for v in by_verdict.get("UNDETERMINED", []):
        non_claims.append(
            "not established: %s — no admissible covering evidence"
            % v["description"])
    for v in by_verdict.get("REFUTED", []):
        non_claims.append(
            "not established as claimed: %s — refuted by %s"
            % (v["description"], ", ".join(v["refuting"])))
    for v in by_verdict.get("CONFLICTED", []):
        non_claims.append(
            "contested: %s — supporting %s vs refuting %s; a verified "
            "counterexample cannot be outvoted"
            % (v["description"], ", ".join(v["supporting"]),
               ", ".join(v["refuting"])))
    if dropped:
        non_claims.append(
            "overlapping sources counted once, not twice: %s"
            % ", ".join(dropped))

    if not obligations:
        grade = "UNKNOWN"
        non_claims.append("no proof obligations defined — nothing to cover")
    elif by_verdict.get("REFUTED") or by_verdict.get("CONFLICTED"):
        grade = "CONTESTED"
    elif by_verdict.get("SUPPORTED"):
        grade = "SUPPORTED"
        if by_verdict.get("UNDETERMINED"):
            non_claims.append(
                "partial coverage only: %d of %d obligations supported"
                % (len(by_verdict["SUPPORTED"]), len(obligations)))
        else:
            ok, problems = compatibility_gate(verdicts, evidence_by_id)
            if not ok:
                non_claims.extend("composition not validated: " + p
                                  for p in problems)
            elif not all(_has_verification_kind(v, evidence_by_id)
                         for v in verdicts):
                non_claims.append(
                    "capped at SUPPORTED: at least one obligation rests on "
                    "review/assertion only — no verification-kind artifact")
            else:
                grade = "PROVEN"
    else:
        grade = "UNKNOWN"

    # Scope dims never demonstrated anywhere stay explicitly unknown.
    demonstrated_dims = set()
    for v in verdicts:
        demonstrated_dims.update(v["demonstrated_scope"].keys())
    for dim in SCOPE_DIMS:
        if dim not in demonstrated_dims and obligations:
            non_claims.append("scope dimension '%s' never demonstrated" % dim)

    return {
        "claim_id": claim.get("id"),
        "claim_text": claim.get("text", ""),
        "grade": grade,
        "obligation_verdicts": verdicts,
        "dropped_duplicates": dropped,
        "non_claims": non_claims,
    }


def strongest_defensible(claim):
    """Recompute the claim narrowed to exactly what the evidence covers."""
    verdict = grade_claim(claim)
    supported = [v for v in verdict["obligation_verdicts"]
                 if v["verdict"] == "SUPPORTED"]
    return {
        "grade": verdict["grade"],
        "holds_for": [v["description"] for v in supported],
        "does_not_claim": verdict["non_claims"],
    }


def assert_claim(claim, asserted_grade):
    """Accept the asserted grade only if the evidence covers it.
    Raises ClaimRejected on any inflation."""
    asserted = asserted_grade.strip().upper()
    if asserted not in GRADE_RANK:
        raise ValueError("unknown asserted grade: %r" % asserted_grade)
    verdict = grade_claim(claim)
    computed = verdict["grade"]
    if computed in GRADE_RANK:
        ok = GRADE_RANK[asserted] <= GRADE_RANK[computed]
    else:
        # CONTESTED / REFUTED: nothing above UNKNOWN may be asserted.
        ok = asserted == "UNKNOWN"
    if not ok:
        reasons = list(verdict["non_claims"])
        if computed in ("CONTESTED", "REFUTED"):
            reasons.insert(
                0, "claim is %s — a counterexample cannot be outvoted"
                % computed)
        raise ClaimRejected(claim.get("id"), asserted, computed, reasons)
    return verdict


def stamp(verdict):
    """Render a verdict with its non-claim boundary stamped on it."""
    lines = ["CLAIM %s: %s" % (verdict["claim_id"], verdict["grade"])]
    if verdict.get("claim_text"):
        lines.append("  %s" % verdict["claim_text"])
    lines.append("ESTABLISHED:")
    established = [v for v in verdict["obligation_verdicts"]
                   if v["verdict"] == "SUPPORTED"]
    if established:
        for v in established:
            lines.append("  - %s — scope %s — evidence [%s]"
                         % (v["description"],
                            json.dumps(v["demonstrated_scope"], sort_keys=True),
                            ", ".join(v["supporting"])))
    else:
        lines.append("  - (nothing)")
    lines.append("DOES NOT CLAIM:")
    if verdict["non_claims"]:
        for nc in verdict["non_claims"]:
            lines.append("  - %s" % nc)
    else:
        lines.append("  - (full coverage; no residual unknowns)")
    return "\n".join(lines)


def require_nonclaims(text):
    """Lightweight guard: a summary must state its non-claims explicitly.
    Raises ValueError if no non-claim marker is present. Keyword-based by
    design — it catches missing boundaries, not subtle ones."""
    lowered = text.lower()
    if not any(m in lowered for m in NONCLAIM_MARKERS):
        raise ValueError(
            "summary rejected: states claims without stating what is NOT "
            "claimed (no non-claim marker found)")
    return True
