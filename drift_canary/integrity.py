"""Canary integrity lifecycle: DETECT → CONTAIN → TRACE → REPLACE → REQUALIFY.

Governing law: "Never erase compromised evidence. Never use it to certify
fresh learning. Preserve its diagnostic value, replace its independence, and
reassess only the qualifications that actually depended on it."

Key distinction: a compromised canary is an invalid source of INDEPENDENT
EVALUATION EVIDENCE, not necessarily an invalid test. A leaked test may still
catch regressions; a duplicated fixture may still reveal defects. But none can
prove generalization anymore.
"""
from __future__ import annotations

from dataclasses import dataclass, field

# Five integrity states — the EVALUATION EVIDENCE lifecycle, separate from
# truth states. A canary NEVER regains SEALED: exposure cannot be undone.
INTEGRITY_STATES = (
    "sealed",       # qualified holdout; independence established
    "suspect",      # credible concern raised; under investigation
    "compromised",  # independence disqualified; diagnostics only
    "retired",      # historical; preserved, never used for qualification
    "replaced",     # new independent set restored; linked to invalidated one
)

# Allowed transitions. Note: nothing transitions back to "sealed".
INTEGRITY_TRANSITIONS = {
    "sealed": ("suspect",),
    "suspect": ("sealed", "compromised"),  # cleared by investigation, or confirmed
    "compromised": ("retired", "replaced"),
    "retired": (),
    "replaced": ("suspect",),  # the replacement set is itself monitored
}

# Four compromise mechanisms. Suspicion triggers investigation; CONFIRMED
# compromised independence triggers disqualification.
COMPROMISE_MECHANISMS = (
    "answer_leakage",          # sealed answers reached the evaluated worker
    "duplicate_lineage",       # cases share source family, counted independent
    "evaluator_contamination", # reviewer exposed to builder conclusions/priors
    "repeated_exposure",       # feedback/adaptive rounds exceeded budget
)


@dataclass(frozen=True)
class IntegrityEvent:
    """One step in the DETECT → CONTAIN → TRACE → REPLACE → REQUALIFY chain."""
    event_id: str
    operation: str             # detect | contain | trace | replace | requalify
    canary_set_id: str
    mechanism: str = ""        # one of COMPROMISE_MECHANISMS (from detect on)
    prior_state: str = ""
    new_state: str = ""
    evidence_ref: str = ""
    actor: str = ""            # who performed the operation

    def __post_init__(self):
        assert self.operation in ("detect", "contain", "trace", "replace", "requalify")
        if self.mechanism:
            assert self.mechanism in COMPROMISE_MECHANISMS


def transition_allowed(prior: str, new: str) -> bool:
    return new in INTEGRITY_TRANSITIONS.get(prior, ())


# Seven-step replacement. Fresh qualification links to (never replaces) the
# invalidated certificate.
REPLACEMENT_STEPS = (
    "1. seal_incident: freeze the incident record; no further evaluation on the set",
    "2. freeze_affected_promotions: suspend qualifications whose certificates "
    "depend on the compromised cases",
    "3. partition_by_source_family: isolate exactly which cases are tainted; "
    "bound the leak before judging the rest",
    "4. generate_independent_replacements: NEW cases from disjoint source "
    "families — NOT paraphrases of the tainted ones",
    "5. blind_validation: independent reviewer validates replacements without "
    "seeing builder expectations",
    "6. reestablish_statistical_adequacy: replacement set meets the same "
    "denominators and coverage the original promised",
    "7. fresh_qualification: new certificate issued, linked to (not replacing) "
    "the invalidated one",
)


@dataclass(frozen=True)
class ReplacementPlan:
    incident_id: str
    compromised_set_id: str
    tainted_case_ids: tuple      # exactly the cases proven tainted
    unaffected_case_ids: tuple   # bounded as clean — still cannot certify alone
    replacement_source_families: tuple  # disjoint from tainted families
    steps: tuple = REPLACEMENT_STEPS
