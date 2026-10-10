"""Uncertain compromise scope (spec). Extends drift_canary.revocation.

Principle: "Unknown independence is not proven independence. But unknown
contamination is not proven contamination either."

Unknown evidence remains preserved. Uncertain independence remains explicitly
uncertain. Only independently supported qualification claims remain eligible
to certify new learning.

Composes with revocation.py:
  - revocation's PARTIAL compromise = known-tainted closure (six verdicts).
  - this module adds the POSSIBLE exposure boundary: confirmed vs possibly
    compromised vs independently cleared vs unassessed, with three-valued
    propagation along typed exposure paths.
  - verdict_for_qualification() maps the four assessment states + the
    acceptance check onto revocation's six verdicts, so every incident gets
    exactly one uncertainty-aware verdict.
"""
from __future__ import annotations

from dataclasses import dataclass, field

# Four assessment states per evidence family. The possible boundary is the
# smallest defensible exposure closure — never the whole corpus by default.
FAMILY_ASSESSMENTS = (
    "confirmed_compromised",   # disqualify independent-proof contribution
    "possibly_compromised",    # suspend independent certification pending review
    "independently_cleared",   # positive evidence of separation — preserve
    "unassessed",              # never silently cleared
)

# Three-valued evidence assessments. Boolean logic is inadequate: missing
# proof of a leak is not proof of independence.
TRIVALUE = ("CONFIRMED", "EXCLUDED", "UNDETERMINED")

# Exposure semantics per edge type. A CITES edge, a DERIVED_FROM edge and an
# ANSWER_EXPOSED_TO edge do NOT imply the same thing. Possible dependency
# edges are kept separate from confirmed dependency edges.
EDGE_EXPOSURE_SEMANTICS = {
    "ANSWER_EXPOSED_TO": "propagates_confirmed_compromise",
    "SHARED_EVALUATOR": "creates_possible_exposure",
    "SHARED_SOURCE": "creates_possible_exposure",
    "DERIVED_FROM": "creates_possible_exposure",
    "CITES": "no_propagation",
    "HISTORICAL_ASSOCIATION": "no_propagation",
}

# Qualification policy per assessment. Uncertain independence can certify
# nothing; it also destroys nothing.
QUALIFICATION_POLICY = {
    "confirmed_compromised": "DISQUALIFY_CONTRIBUTION",
    "possibly_compromised": "HOLD_INDEPENDENT_CERTIFICATION",
    "independently_cleared": "PRESERVE_ELIGIBILITY",
    "unassessed": "REVIEW_REQUIRED",
}

# Four responses by intended use. An uncertain evaluation certificate is not
# proof the underlying software or lesson is false — the stricter requirement
# applies to the independence claim, not to existence of the evidence.
USE_RESPONSES = {
    "historical_research": "permit_reading_with_uncertainty_labels",
    "debugging": "permit_diagnostic_reuse_without_blindness_claim",
    "independent_qualification": "uncertain_contributions_do_not_count",
    "consequential_act": "hold_dependent_action_if_no_independently_sufficient_qualification",
}

# Governance: a review deadline is never an expiration date for safety
# restrictions. A reviewer may close as unresolvable while the qualification
# stays unavailable.
ESCALATION_RULES = (
    "bounded_uncertain_exposure: quarantine affected independent-proof contributions",
    "full_set_uncertain: suspend affected set-wide certification",
    "shared_evaluator_across_sets: review evaluator-level exposure across sets",
    "known_unaffected_certificate: preserve its eligibility",
    "irrecoverable_audit_history: retire disputed blind use, replace evidence",
    "dependent_high_risk_act_pending: apply LAW hard gates and escalate",
    "deadline_passed_without_proof: preserve unresolved status; replace evidence "
    "or escalate; NEVER auto-clear",
)

# The two measurements that prove uncertain scope is governed correctly.
# A system that revokes everything is safer against false certification but
# fails the mission of keeping verified intelligence useful.
GOVERNANCE_METRICS = (
    "unsafe_certification_rate",   # uncertain evidence treated as independent
    "unnecessary_qualification_loss",  # provably unaffected evidence discarded
)


@dataclass(frozen=True)
class ExposureEdge:
    """One typed dependency edge between evidence families. Status is
    POSSIBLE (pathway exists, extent unresolved) or CONFIRMED (evidence
    proves the pathway carried answer-bearing material)."""
    from_family: str
    to_family: str
    mechanism: str  # key of EDGE_EXPOSURE_SEMANTICS
    status: str     # POSSIBLE | CONFIRMED
    evidence_ref: str = ""

    def __post_init__(self):
        assert self.mechanism in EDGE_EXPOSURE_SEMANTICS, self.mechanism
        assert self.status in ("POSSIBLE", "CONFIRMED"), self.status

    def exposure_semantics(self) -> str:
        return EDGE_EXPOSURE_SEMANTICS[self.mechanism]


@dataclass
class UncertainCompromiseIncident:
    """Append-only record. Keeps possible edges separate from confirmed edges
    and binds corpus hash, code/model/policy versions, access-log coverage,
    time interval, authority receipt, and every reassessment event."""
    incident_id: str
    scope_state: str = "PARTIALLY_BOUNDED"  # PARTIALLY_BOUNDED | UNBOUNDED
    confirmed_affected: tuple = ()
    possibly_affected: tuple = ()
    independently_cleared: tuple = ()
    unassessed: tuple = ()
    exposure_edges: tuple = ()
    corpus_hash: str = ""
    code_version: str = ""
    model_version: str = ""
    policy_version: str = ""
    access_log_coverage: str = ""  # COMPLETE | PARTIAL | MISSING
    review_owner: str = "INDEPENDENT_VERIFY"
    review_deadline: str = ""  # explicit timestamp
    historical_receipts: str = "PRESERVE"
    reassessment_events: tuple = field(default_factory=tuple)

    def __post_init__(self):
        # A family must live in exactly one assessment bucket.
        all_families = (
            list(self.confirmed_affected) + list(self.possibly_affected)
            + list(self.independently_cleared) + list(self.unassessed)
        )
        assert len(set(all_families)) == len(all_families), "family in two buckets"

    def assessment_of(self, family: str) -> str:
        for bucket, state in (
            (self.confirmed_affected, "confirmed_compromised"),
            (self.possibly_affected, "possibly_compromised"),
            (self.independently_cleared, "independently_cleared"),
            (self.unassessed, "unassessed"),
        ):
            if family in bucket:
                return state
        raise KeyError(f"family {family!r} not classified in {self.incident_id}")

    def policy_for(self, family: str) -> str:
        return QUALIFICATION_POLICY[self.assessment_of(family)]

    def confirmed_closure(self) -> set:
        """Families with CONFIRMED compromised exposure: the incident's
        confirmed_affected plus families reached via CONFIRMED
        answer-bearing paths."""
        closure = set(self.confirmed_affected)
        changed = True
        while changed:
            changed = False
            for e in self.exposure_edges:
                if (e.status == "CONFIRMED"
                        and e.exposure_semantics() == "propagates_confirmed_compromise"
                        and e.from_family in closure and e.to_family not in closure):
                    closure.add(e.to_family)
                    changed = True
        return closure

    def possible_closure(self) -> set:
        """Families with POSSIBLE exposure: possibly_affected plus families
        reachable via POSSIBLE exposure-capable paths. This is the smallest
        defensible exposure closure, not the whole corpus."""
        closure = set(self.possibly_affected) | set(self.confirmed_affected)
        changed = True
        while changed:
            changed = False
            for e in self.exposure_edges:
                if (e.status == "POSSIBLE"
                        and e.exposure_semantics() in (
                            "creates_possible_exposure",
                            "propagates_confirmed_compromise")
                        and e.from_family in closure and e.to_family not in closure):
                    closure.add(e.to_family)
                    changed = True
        return closure

    def trivalue_of(self, family: str) -> str:
        """Three-valued independence assessment for one family."""
        if family in self.confirmed_closure():
            return "CONFIRMED"
        if family in self.possible_closure() or family in self.unassessed:
            return "UNDETERMINED"
        if family in self.independently_cleared:
            return "EXCLUDED"
        raise KeyError(f"family {family!r} not classified in {self.incident_id}")


@dataclass
class ClearancePacket:
    """Positive-evidence packet required to clear a family. Absence of a
    detected leak is NOT sufficient. If audit history is irrecoverable, the
    answer is retire-and-replace, not investigate forever."""
    family: str
    provenance_verified: bool = False            # creation history of the family
    access_exposure_evidence: bool = False        # exposure for the time period
    no_disqualifying_dependency: bool = False    # within the assessed boundary
    independent_reviewer: str = ""               # reviewer identity, qualified
    recomputed_stats: bool = False               # acceptance stats, if aggregate
    recorded_verdict: str = ""                   # independently reviewable verdict
    audit_history_irrecoverable: bool = False

    def is_complete(self) -> bool:
        return all([
            self.provenance_verified,
            self.access_exposure_evidence,
            self.no_disqualifying_dependency,
            bool(self.independent_reviewer),
            self.recomputed_stats,
            bool(self.recorded_verdict),
        ])

    def decision(self) -> str:
        """CLEARED | INCOMPLETE | RETIRE_AND_REPLACE. Missing history is a
        terminal condition for blind use, not a queue item."""
        if self.audit_history_irrecoverable:
            return "RETIRE_AND_REPLACE"
        return "CLEARED" if self.is_complete() else "INCOMPLETE"


@dataclass
class UncertainRecomputation:
    """Recompute under uncertainty: conservative qualification on cleared
    evidence only, plus sensitivity analysis over plausible uncertain
    outcomes. The 40-cleared example: their success rate may be biased toward
    easier tasks — it cannot generalize to the 100-case population without
    accounting."""
    qualification_id: str
    cleared_cases: int
    possible_cases: int
    unassessed_cases: int
    confirmed_cases: int
    original_cases: int
    cleared_family_difficulty: str = "unknown"  # easier | same | harder | unknown

    @property
    def total_cases(self) -> int:
        return (self.cleared_cases + self.possible_cases
                + self.unassessed_cases + self.confirmed_cases)

    def conservative_count(self) -> int:
        """Only cleared evidence counts toward independent qualification."""
        return self.cleared_cases

    def sensitivity_flip(self, cleared_rate: float, uncertain_rates: tuple) -> dict:
        """Could plausible outcomes for the uncertain families change the
        final verdict? Never treat optimistic assumptions as proof."""
        results = {}
        for rate in uncertain_rates:
            overall = (cleared_rate * self.cleared_cases
                       + rate * (self.possible_cases + self.unassessed_cases)
                       ) / max(self.total_cases - self.confirmed_cases, 1)
            results[rate] = overall
        return results

    def generalization_warning(self) -> str:
        if self.cleared_family_difficulty == "easier":
            return (
                "WARNING: cleared cases skew easier — their success rate does "
                "not generalize to the original population. Narrow the claim "
                "or reweight for the changed target population."
            )
        if self.cleared_family_difficulty == "unknown":
            return "difficulty bias unknown — conservative verdict must hold"
        return "difficulty accounted"

    def acceptance_hold(self, min_cases: int, min_families: int,
                        cleared_families: int) -> bool:
        """Conservative acceptance: cleared evidence only, against the
        ORIGINAL bar."""
        return self.cleared_cases >= min_cases and cleared_families >= min_families


def verdict_for_qualification(incident: UncertainCompromiseIncident,
                             families_in_claim: tuple,
                             acceptance_met_on_cleared: bool) -> str:
    """Map four assessment states + the acceptance check onto revocation's
    six verdicts. Returns exactly one verdict per qualification.

      REVOKED          — confirmed compromise of the claim's required
                         independence condition (or acceptance failed on
                         cleared with no narrower defensible claim)
      SUSPENDED        — possibly-compromised or unassessed families remain
                         in the claim's closure; pending review/replacement
      DOWNGRADED       — narrower claim supportable on cleared evidence
      INSUFFICIENT_DATA— cleared evidence valid but below the original bar
      REQUALIFIED      — recomputed on cleared evidence; original bar met
      UNAFFECTED       — no compromised evidence in the claim's closure
    """
    states = {incident.assessment_of(f) for f in families_in_claim}
    if "confirmed_compromised" in states:
        # Claim required independence from a family now confirmed tainted.
        return "REVOKED"
    if "possibly_compromised" in states or "unassessed" in states:
        # Independence cannot currently be established — hold, do not certify.
        return "SUSPENDED"
    # All families independently cleared: evidence tier supports recompute.
    if acceptance_met_on_cleared:
        return "REQUALIFIED"
    return "INSUFFICIENT_DATA"
