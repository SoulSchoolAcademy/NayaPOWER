"""Five evaluation-contamination checks (deterministic).

1. TRAINING LEAKAGE — worker can retrieve sealed questions/answers from files,
   prompts, Brain, logs, or connected sources.
2. FEEDBACK LEAKAGE — repeated detailed failure reports let the builder infer
   hidden answer keys.
3. LINEAGE LEAKAGE — examples descend from the same incident/template yet are
   counted as independent.
4. TEMPORAL LEAKAGE — evaluation uses information available only AFTER the
   historical decision being replayed.
5. EVALUATOR CONTAMINATION — reviewer sees builder's expected conclusion,
   earlier judgments, or treatment assignment.

Rule: lineage-disjoint splits by source family / incident / task lineage /
affected entity / time — never random rows. Exact duplicates, near-duplicates,
and paraphrases checked before a case joins a protected set.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass


def _norm(text: str) -> str:
    return " ".join(text.lower().split())


def content_hash(text: str) -> str:
    return hashlib.sha256(_norm(text).encode()).hexdigest()


@dataclass(frozen=True)
class ContaminationVerdict:
    check: str
    passed: bool
    detail: str


def check_training_leakage(accessible_paths: tuple[str, ...],
                           sealed_ids: tuple[str, ...]) -> ContaminationVerdict:
    """Any sealed case id reachable from a path the evaluated worker can read?"""
    leaked = [s for s in sealed_ids
              if any(s in p for p in accessible_paths)]
    return ContaminationVerdict(
        "training_leakage", not leaked,
        f"sealed ids reachable: {leaked}" if leaked else "no sealed ids reachable")


def check_feedback_leakage(feedback_rounds: int,
                            max_detail_per_round: int,
                            key_space_bits: int = 128,
                            max_rounds: int = 5) -> ContaminationVerdict:
    """Bounded feedback must not let the builder infer hidden keys.
    Conservative model: each round leaks at most `max_detail_per_round` bits."""
    leaked_bits = feedback_rounds * max_detail_per_round
    ok = feedback_rounds <= max_rounds and leaked_bits < key_space_bits // 2
    return ContaminationVerdict(
        "feedback_leakage", ok,
        f"{feedback_rounds} rounds x {max_detail_per_round} bits = {leaked_bits} "
        f"leaked of {key_space_bits}-bit key space (cap {max_rounds} rounds)")


def check_lineage_leakage(case_families: tuple[str, ...]) -> ContaminationVerdict:
    """Protected splits must be lineage-disjoint: no shared source family."""
    seen: dict[str, int] = {}
    dupes = []
    for i, fam in enumerate(case_families):
        if fam in seen:
            dupes.append((seen[fam], i, fam))
        else:
            seen[fam] = i
    return ContaminationVerdict(
        "lineage_leakage", not dupes,
        f"shared families across split: {dupes}" if dupes else "split is lineage-disjoint")


def check_temporal_leakage(case_decision_time: str,
                            newest_evidence_time: str) -> ContaminationVerdict:
    """Evaluation must not use evidence newer than the decision being replayed."""
    ok = newest_evidence_time <= case_decision_time  # ISO-8601 lexicographic
    return ContaminationVerdict(
        "temporal_leakage", ok,
        f"newest evidence {newest_evidence_time} vs decision {case_decision_time}")


def check_evaluator_contamination(reviewer_saw_builder_conclusion: bool,
                                   reviewer_saw_prior_judgments: bool,
                                   reviewer_knew_treatment: bool) -> ContaminationVerdict:
    ok = not (reviewer_saw_builder_conclusion
              or reviewer_saw_prior_judgments
              or reviewer_knew_treatment)
    return ContaminationVerdict(
        "evaluator_contamination", ok,
        "reviewer blind to conclusion/priors/treatment"
        if ok else "reviewer exposed to builder conclusion, priors, or treatment")


def run_all_contamination_checks(**kwargs) -> tuple[ContaminationVerdict, ...]:
    return (
        check_training_leakage(kwargs["accessible_paths"], kwargs["sealed_ids"]),
        check_feedback_leakage(kwargs["feedback_rounds"], kwargs["max_detail_per_round"]),
        check_lineage_leakage(kwargs["case_families"]),
        check_temporal_leakage(kwargs["case_decision_time"], kwargs["newest_evidence_time"]),
        check_evaluator_contamination(kwargs["reviewer_saw_builder_conclusion"],
                                      kwargs["reviewer_saw_prior_judgments"],
                                      kwargs["reviewer_knew_treatment"]),
    )
