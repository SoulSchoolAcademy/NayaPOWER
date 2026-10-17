"""The ten trigger registry.

Each trigger names the event that should reopen a resolution, the evidence
shape it REQUIRES, and the response it mandates. A challenge that names a
trigger but carries none of its required evidence is INSUFFICIENT — a
different opinion is not a trigger.

Trigger -> (required evidence keys, mandated response)
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TriggerSpec:
    trigger_type: str
    description: str
    required_evidence: tuple[str, ...]   # keys the challenge must carry
    mandates: str                        # REASSESS | INSPECT | RECONSTRUCT ...


NEW_DIRECT_EVIDENCE = "NEW_DIRECT_EVIDENCE"
CONTRADICTORY_EVIDENCE = "CONTRADICTORY_EVIDENCE"
POLICY_CHANGE = "POLICY_CHANGE"
SOURCE_CORRECTION = "SOURCE_CORRECTION"
PROVENANCE_FAILURE = "PROVENANCE_FAILURE"
EXTRACTION_DEFECT = "EXTRACTION_DEFECT"
SUCCESSOR_CHALLENGE = "SUCCESSOR_CHALLENGE"
CONTEXT_CHANGE = "CONTEXT_CHANGE"
FAILED_PREDICTION = "FAILED_PREDICTION"
DEPENDENCY_INVALIDATION = "DEPENDENCY_INVALIDATION"


REGISTRY: dict[str, TriggerSpec] = {
    NEW_DIRECT_EVIDENCE: TriggerSpec(
        NEW_DIRECT_EVIDENCE,
        "Original recording or attributable record clarifies intended meaning.",
        ("clarifying_record_ref", "attribution"),
        "REASSESS",
    ),
    CONTRADICTORY_EVIDENCE: TriggerSpec(
        CONTRADICTORY_EVIDENCE,
        "Independent result challenges a resolved claim.",
        ("contradicting_evidence_ref", "independence_attestation"),
        "INSPECT",
    ),
    POLICY_CHANGE: TriggerSpec(
        POLICY_CHANGE,
        "The governing definition changed (P1 -> P2).",
        ("old_policy_version", "new_policy_version", "policy_diff_ref"),
        "REASSESS_APPLICABILITY",
    ),
    SOURCE_CORRECTION: TriggerSpec(
        SOURCE_CORRECTION,
        "Author explicitly clarifies an earlier statement.",
        ("correction_record_ref", "author_attribution"),
        "REASSESS",
    ),
    PROVENANCE_FAILURE: TriggerSpec(
        PROVENANCE_FAILURE,
        "A supporting receipt fails integrity validation.",
        ("failed_receipt_id", "integrity_report_ref"),
        "SUSPEND_DEPENDENT",
    ),
    EXTRACTION_DEFECT: TriggerSpec(
        EXTRACTION_DEFECT,
        "A negation, condition, or scope was omitted in extraction.",
        ("original_span_ref", "defect_description"),
        "RECONSTRUCT",
    ),
    SUCCESSOR_CHALLENGE: TriggerSpec(
        SUCCESSOR_CHALLENGE,
        "A cold successor identifies a missed plausible meaning.",
        ("missed_interpretation", "reproducible_reasoning"),
        "REASSESS",
    ),
    CONTEXT_CHANGE: TriggerSpec(
        CONTEXT_CHANGE,
        "A prior instruction applied to a different environment/scope.",
        ("original_scope", "current_scope"),
        "LIMIT_SCOPE",
    ),
    FAILED_PREDICTION: TriggerSpec(
        FAILED_PREDICTION,
        "An observed outcome contradicts an assumption behind the resolution.",
        ("prediction_ref", "observed_outcome_ref"),
        "CHALLENGE_ASSUMPTION",
    ),
    DEPENDENCY_INVALIDATION: TriggerSpec(
        DEPENDENCY_INVALIDATION,
        "A parent claim the resolution depended on is refuted or superseded.",
        ("parent_claim_ref", "invalidation_receipt_ref"),
        "REASSESS_DEPENDENTS",
    ),
}


def validate_trigger_evidence(trigger_type: str,
                              provided: dict[str, str]) -> tuple[bool, tuple[str, ...]]:
    """Check a challenge carries its trigger's required evidence shape.
    Returns (ok, missing_keys). Unknown trigger -> (False, ('unknown',))."""
    spec = REGISTRY.get(trigger_type)
    if spec is None:
        return False, ("unknown_trigger_type",)
    missing = tuple(k for k in spec.required_evidence if not provided.get(k))
    return (len(missing) == 0), missing
