#!/usr/bin/env python3
"""Fairness eligibility prover — Group 5 (Fairness & Liveness), D58-D65.

D26 Link 1: OPPORTUNITY — "Was the chance actually provided?"
Before asking whether service was fair, prove the work item was actually
eligible. The prover INDEPENDENTLY re-evaluates every requirement predicate
against the evidence bundle. The scheduler's own eligibility claim is treated
as untrusted input: it is recorded, never trusted. If the evidence contradicts
the scheduler's claim, the evidence wins and the contradiction is named.

Every verdict carries one of D26's four explicit verdict levels (never a bare
PASS/FAIL):
  OBSERVED_NO_VIOLATION          — we checked and saw nothing wrong (weakest)
  MODEL_CHECK_PASSED_IN_SCOPE    — proven within the stated model scope
  FAIRNESS_QUALIFIED_WITH_ASSUMPTIONS — qualified, resting on named assumptions
  WORKFLOW_COMPLETED_IN_SCOPE    — the real work finished (strongest)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

# D27 assumption-guarantee boundary: every assumption a verdict rests on must
# resolve through the canonical registry. Unknown refs raise
# UnknownAssumptionError -- fail closed, never silently named.
from fairness_assumptions import resolve as _resolve_assumption

# D26's four verdict levels. Every verdict this module emits names one.
VERDICT_LEVELS = (
    "OBSERVED_NO_VIOLATION",
    "MODEL_CHECK_PASSED_IN_SCOPE",
    "FAIRNESS_QUALIFIED_WITH_ASSUMPTIONS",
    "WORKFLOW_COMPLETED_IN_SCOPE",
)

# A requirement predicate: (evidence_bundle) -> (satisfied: bool, detail: str).
# Predicates must be pure functions of the evidence. They must never consult
# the scheduler's claim; the prover enforces this by construction (predicates
# receive only the evidence bundle, never the item's claimed status).
Predicate = Callable[[Dict[str, Any]], tuple]


class PredicateRegistry:
    """Named requirement predicates, evaluated against evidence only."""

    def __init__(self) -> None:
        self._predicates: Dict[str, Predicate] = {}

    def register(self, name: str, predicate: Predicate) -> None:
        if not callable(predicate):
            raise TypeError(f"predicate {name!r} is not callable")
        self._predicates[name] = predicate

    def names(self) -> List[str]:
        return sorted(self._predicates)

    def evaluate(self, name: str, evidence: Dict[str, Any]) -> tuple:
        if name not in self._predicates:
            raise KeyError(f"unknown requirement predicate: {name!r}")
        satisfied, detail = self._predicates[name](evidence)
        return bool(satisfied), str(detail)


@dataclass
class WorkItem:
    """A unit of work with eligibility requirements."""
    item_id: str
    requirements: List[str]  # predicate names, ALL must hold for eligibility
    scheduler_claim: Optional[bool] = None  # untrusted; recorded, never trusted
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RequirementResult:
    name: str
    satisfied: bool
    detail: str


@dataclass
class EligibilityVerdict:
    item_id: str
    window_id: str
    eligible: bool
    requirements: List[RequirementResult]
    missing: List[str]  # requirement names not satisfied
    scheduler_claim: Optional[bool]
    claim_contradicted: bool  # True when evidence contradicts scheduler's claim
    verdict_level: str
    assumptions: List[str] = field(default_factory=list)  # resolved statements
    assumption_ids: List[str] = field(default_factory=list)  # canonical ids

    def __post_init__(self) -> None:
        if self.verdict_level not in VERDICT_LEVELS:
            raise ValueError(f"invalid verdict level: {self.verdict_level!r}")
        if len(self.assumptions) != len(self.assumption_ids):
            raise ValueError(
                "assumptions and assumption_ids out of sync: "
                f"{len(self.assumptions)} statements vs "
                f"{len(self.assumption_ids)} ids")


class EligibilityProver:
    """Independently proves eligibility from evidence. Never trusts the scheduler."""

    def __init__(self, registry: PredicateRegistry) -> None:
        self.registry = registry

    def prove(
        self,
        item: WorkItem,
        evidence: Dict[str, Any],
        window_id: str,
        assumptions: Optional[List[str]] = None,
    ) -> EligibilityVerdict:
        """Re-evaluate every requirement predicate against the evidence bundle.

        The scheduler's claim is compared afterwards purely as a diagnostic:
        if the independent evaluation disagrees with the claim, the verdict
        names the contradiction. The claim never influences the verdict.

        D27: every assumption is resolved through the canonical registry
        BEFORE any verdict is constructed. An unregistered (phantom)
        assumption raises UnknownAssumptionError -- no verdict is emitted.
        """
        # D27 choke point: resolve first, verdict second. A phantom ref here
        # raises before EligibilityVerdict is ever constructed.
        resolved_ids: List[str] = []
        resolved_statements: List[str] = []
        for ref in (assumptions or []):
            asm = _resolve_assumption(ref)
            resolved_ids.append(asm.id)
            resolved_statements.append(asm.statement)

        results: List[RequirementResult] = []
        missing: List[str] = []
        for req in item.requirements:
            satisfied, detail = self.registry.evaluate(req, evidence)
            results.append(RequirementResult(req, satisfied, detail))
            if not satisfied:
                missing.append(req)

        eligible = len(missing) == 0

        claim_contradicted = (
            item.scheduler_claim is not None and item.scheduler_claim != eligible
        )

        # Verdict level: independent re-evaluation from evidence is a model
        # check in the scope of the provided evidence. It becomes
        # FAIRNESS_QUALIFIED_WITH_ASSUMPTIONS when the caller names
        # assumptions the evidence does not cover; it is never stronger than
        # MODEL_CHECK_PASSED_IN_SCOPE because this module does not observe
        # the live system by itself (the harness in fairness_invariants.py
        # lifts it to WORKFLOW_COMPLETED_IN_SCOPE when wired to real traces).
        if resolved_ids:
            level = "FAIRNESS_QUALIFIED_WITH_ASSUMPTIONS"
        else:
            level = "MODEL_CHECK_PASSED_IN_SCOPE"

        return EligibilityVerdict(
            item_id=item.item_id,
            window_id=window_id,
            eligible=eligible,
            requirements=results,
            missing=missing,
            scheduler_claim=item.scheduler_claim,
            claim_contradicted=claim_contradicted,
            verdict_level=level,
            assumptions=resolved_statements,
            assumption_ids=resolved_ids,
        )


# ---------------------------------------------------------------------------
# Built-in predicates for the common requirement shapes.
# ---------------------------------------------------------------------------

def _pred_evidence_key_present(key: str) -> Predicate:
    def check(evidence: Dict[str, Any]) -> tuple:
        present = key in evidence and evidence[key] not in (None, "", [], {})
        return present, f"evidence key {key!r} {'present' if present else 'absent'}"
    check.__name__ = f"evidence_key_present[{key}]"
    return check


def _pred_evidence_key_equals(key: str, expected: Any) -> Predicate:
    def check(evidence: Dict[str, Any]) -> tuple:
        actual = evidence.get(key, "<absent>")
        ok = actual == expected
        return ok, f"evidence[{key!r}]={actual!r} expected {expected!r}"
    check.__name__ = f"evidence_key_equals[{key}=={expected!r}]"
    return check


def _pred_evidence_key_true(key: str) -> Predicate:
    def check(evidence: Dict[str, Any]) -> tuple:
        ok = bool(evidence.get(key))
        return ok, f"evidence[{key!r}] is {'truthy' if ok else 'falsy/absent'}"
    check.__name__ = f"evidence_key_true[{key}]"
    return check


def standard_registry() -> PredicateRegistry:
    """A registry with the common built-in predicate factories available."""
    return PredicateRegistry()
