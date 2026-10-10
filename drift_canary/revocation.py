"""Partial compromise and selective revocation (spec).

Governing rule: "Revoke the compromised evidence's right to certify a result
— not every result associated with the same benchmark."

One-sentence architecture: "Evidence immutable, independence revocable,
qualifications continuously recomputable from remaining valid evidence."

Four distinct units — compromise can hit one without the others:
  case         — a single canary fixture
  family       — a source family of cases
  receipt      — an evaluation receipt (a run's evidence)
  claim        — a qualification claim resting on the evidence

Critical: valid evidence ≠ sufficient evidence. If a benchmark needed 100
cases for its error bound and 20 are compromised, the remaining 80 may be
trustworthy observations but INSUFFICIENT for the original claim.
Statistical trap: if the compromised family was HARDER, deleting it inflates
apparent accuracy — must narrow the claim, replace the family, or account for
the changed population.
"""
from __future__ import annotations

from dataclasses import dataclass, field

COMPROMISE_UNITS = ("case", "family", "receipt", "claim")

# Scope status of a partial compromise record (append-only event).
# UNKNOWN: do NOT declare apparently-unaffected cases independent without
# verification.
SCOPE_STATUS = ("CONFIRMED_BOUNDED", "POTENTIALLY_BROADER", "UNKNOWN")

# Six verdicts — distinct from lesson truth states. A qualification's verdict
# describes the standing of its EVIDENCE, not the truth of any lesson.
VERDICTS = (
    "UNAFFECTED",        # no compromised evidence in the closure
    "REQUALIFIED",       # recomputed on remaining evidence; still meets bar
    "DOWNGRADED",        # meets a narrower claim only
    "INSUFFICIENT_DATA", # remaining evidence valid but too little
    "SUSPENDED",         # pending investigation / replacement
    "REVOKED",           # certified conclusion no longer supportable
)

# Two revocation forms. Evidence-contribution revocation does NOT always
# require qualification revocation — recompute first, then judge.
REVOCATION_FORMS = (
    "evidence_contribution",  # case no longer counts toward independence
    "qualification",          # certified conclusion no longer supportable
)


@dataclass(frozen=True)
class PartialCompromiseRecord:
    """Append-only event. Scope is stated explicitly; UNKNOWN scope forbids
    assuming the rest is clean."""
    record_id: str
    unit: str                    # one of COMPROMISE_UNITS
    unit_id: str
    mechanism: str               # one of the four compromise mechanisms
    scope_status: str            # CONFIRMED_BOUNDED | POTENTIALLY_BROADER | UNKNOWN
    tainted_ids: tuple = ()      # exactly the proven-tainted units
    note: str = ""

    def __post_init__(self):
        assert self.unit in COMPROMISE_UNITS
        assert self.scope_status in SCOPE_STATUS

    def may_assume_rest_clean(self) -> bool:
        """Only CONFIRMED_BOUNDED lets the rest stand without re-verification."""
        return self.scope_status == "CONFIRMED_BOUNDED"


# Six-step recomputation. Old receipt preserved; new verdict issued.
RECOMPUTATION_STEPS = (
    "1. verify_incident: confirm the compromise event and mechanism",
    "2. compute_affected_closure: all cases/families/receipts/claims downstream "
    "of the tainted units",
    "3. subtract_compromised_contributions: eligibility revoked, observations "
    "preserved (evidence immutable)",
    "4. recompute_metric_and_uncertainty: metric + confidence on remaining "
    "evidence only; account for population change if tainted family differed "
    "in difficulty",
    "5. check_acceptance: family coverage, sample size, independence, strength "
    "against the ORIGINAL bar",
    "6. issue_verdict: one of the six verdicts; old receipt preserved, new "
    "receipt linked",
)


@dataclass
class Recomputation:
    """State of one recomputation pass over remaining valid evidence."""
    incident_id: str
    remaining_cases: int
    original_cases: int
    remaining_families: tuple
    # difficulty accounting: was the tainted family harder/easier/same?
    tainted_family_difficulty: str = "unknown"  # harder | easier | same | unknown

    def sufficiency_note(self) -> str:
        if self.remaining_cases < self.original_cases:
            return (
                f"{self.remaining_cases}/{self.original_cases} cases remain: "
                f"observations may be valid but the original error bound "
                f"is no longer established"
            )
        return "case count intact"

    def difficulty_warning(self) -> str:
        if self.tainted_family_difficulty == "harder":
            return (
                "WARNING: tainted family was harder — naive deletion inflates "
                "apparent accuracy. Narrow the claim, replace the family, or "
                "reweight for the changed population."
            )
        if self.tainted_family_difficulty == "unknown":
            return (
                "difficulty unknown — treat recomputed metric as provisional "
                "pending difficulty analysis"
            )
        return "difficulty accounted"


# Ten rules (machine-enforceable where marked *).
PARTIAL_COMPROMISE_RULES = (
    "* versioned_eligibility: ACT and successors check certificate version; "
    "stale certificates never authorize",
    "* no_paraphrase_holdouts: replacements must come from disjoint source "
    "families, never paraphrases of tainted cases",
    "* cold_successor_reverify: successors re-derive usability from current "
    "certificates, never inherit stale verdicts",
    "scope_explicit: every compromise record states CONFIRMED_BOUNDED, "
    "POTENTIALLY_BROADER, or UNKNOWN",
    "unknown_means_verify: UNKNOWN scope forbids assuming the rest is clean",
    "observations_preserved: revocation removes certification rights, never "
    "deletes evidence",
    "narrow_before_revoke: prefer DOWNGRADED (narrower claim) over REVOKED "
    "when remaining evidence supports it",
    "old_receipts_kept: every recomputation links the invalidated receipt; "
    "history is append-only",
    "difficulty_accounted: recomputation must address population change",
    "independence_reproven: B-E families usable only if independence established",
)
