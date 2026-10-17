"""Hierarchical risk model — conceptual spec, not fitted to fake data.

When confirmed high-risk failures are rare, a separate probability estimate
per narrow case category produces wildly overconfident rates. Partial
pooling shares information across related categories while allowing
genuinely different risk levels.

This module specifies the model STRUCTURE and its validation requirements.
It fits NOTHING: there is no historical dataset here, and inventing one
would be fabrication. Actual fitting happens only in the offline study
(calibration/study.py) against independently adjudicated cases.

Risk categories (the pooling groups):
"""

from __future__ import annotations

from dataclasses import dataclass, field


CATEGORIES = (
    "missing_independent_verification",
    "invalid_or_stale_provenance",
    "contradictory_source_evidence",
    "policy_version_mismatch",
    "ambiguous_human_authorization",
    "incorrect_claim_extraction",
    "cold_successor_interpretation_error",
)


@dataclass(frozen=True)
class PriorSpec:
    """One candidate prior over category base rates. Sensitivity analysis
    REQUIRES publishing results under >= 3 alternative priors — a single
    posterior is never treated as objective truth."""
    name: str
    description: str
    # (alpha, beta) pseudo-counts per category, or "empirical" / "skeptical"
    shape: str


SKEPTICAL_PRIOR = PriorSpec(
    "skeptical",
    "Assumes categories are no safer than the pooled mean until the "
    "category's own data says otherwise. Guards against 'zero failures "
    "in 12 trials therefore safe'.",
    shape="skeptical",
)

EMPIRICAL_PRIOR = PriorSpec(
    "empirical",
    "Centers each category on the pooled observed rate with modest "
    "regularization.",
    shape="empirical",
)

PESSIMISTIC_PRIOR = PriorSpec(
    "pessimistic",
    "Deliberately overstates rare-category risk to test whether decisions "
    "remain defensible under adverse assumptions.",
    shape="pessimistic",
)

REQUIRED_PRIORS = (SKEPTICAL_PRIOR, EMPIRICAL_PRIOR, PESSIMISTIC_PRIOR)


@dataclass
class CategoryEvidence:
    """Observed adjudicated outcomes for one category. Populated ONLY by
    the offline study from independently labeled cases — never synthesized."""
    category: str
    n_trials: int = 0
    n_confirmed_errors: int = 0
    n_censored: int = 0          # prevented outcomes: NOT zero-error evidence
    source: str = ""             # which adjudicated dataset

    def __post_init__(self):
        if self.category not in CATEGORIES:
            raise ValueError(f"unknown category {self.category!r}")
        if self.n_confirmed_errors > self.n_trials:
            raise ValueError("errors cannot exceed trials")


@dataclass(frozen=True)
class SensitivityReport:
    """The required output of any fitted model: the decision-relevant
    quantity under EACH prior, so reviewers see how much the conclusion
    depends on assumptions."""
    quantity: str
    by_prior: dict               # prior name -> (low, high) interval
    decision_stable: bool         # same recommended action under all priors?
    note: str = ""


def pooling_rationale() -> str:
    return (
        "Partial pooling: each category's estimated rate is a weighted blend "
        "of its own adjudicated outcomes and the pooled rate across "
        "categories. Categories with few observations shrink toward the "
        "pooled mean (no overconfident 'safe' verdicts from n=2); categories "
        "with abundant data dominate their own estimate. Priors matter most "
        "exactly where data is scarcest — hence mandatory sensitivity "
        "reporting under skeptical, empirical, and pessimistic priors."
    )


def zero_failure_warning(n: int) -> str:
    """What zero observed failures actually licenses (rule of three)."""
    bound = 3.0 / n if n > 0 else 1.0
    return (
        f"Zero failures in {n} trials licenses a 95% upper bound of ~{bound:.2%} "
        f"on the failure rate (binomial, representative trials assumed) — "
        f"NOT a claim that the failure probability is zero."
    )
