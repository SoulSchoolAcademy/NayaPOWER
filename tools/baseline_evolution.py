"""UD-15: NORMAL MAY EVOLVE, BUT NEVER LEARN FAILURE AS NORMAL.

Baselines and "normal" may evolve — but only on evidence, never by drift.
Every baseline change is recorded with what changed, why, and the evidence.
Silent drift is the enemy.

Three references are maintained, never one self-changing baseline:
  FROZEN_REFERENCE        — immutable, independently qualified picture of normal.
  ADAPTIVE_CANDIDATE      — learns in shadow; explains patterns, never replaces the contract.
  PROMOTED_OPERATIONAL    — the current operational baseline; changes only via the
                            governed promotion gate.

Promotion gate (hard obligations, conjunctive — never an aggregate score):
  CANDIDATE -> SHADOW -> INDEPENDENTLY_QUALIFIED -> PROMOTED

Training data is classified; unresolved incidents are barred from defining normality.
Scope isolation: four permanent scope IDs per observation; a sparse scope under a
healthy parent stays unqualified; aggregate improvement never overrides a local
regression; pooling may share estimates but never transfers certification.

The baseline ledger is append-only: old baselines are superseded, never
overwritten. Decisions computed on a baseline that is not the ledger's current
version are refused with STALE_BASELINE.

Absorbs D49, D50, D52. Stdlib only.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Training-data classification (D50)
# ---------------------------------------------------------------------------

class TrainingClass(str, Enum):
    VERIFIED_HEALTHY = "VERIFIED_HEALTHY"
    VERIFIED_WORKLOAD_SHIFT = "VERIFIED_WORKLOAD_SHIFT"
    DECLARED_MAINTENANCE = "DECLARED_MAINTENANCE"
    UNRESOLVED_ANOMALY = "UNRESOLVED_ANOMALY"
    CONFIRMED_REGRESSION = "CONFIRMED_REGRESSION"
    INSUFFICIENT_OBSERVABILITY = "INSUFFICIENT_OBSERVABILITY"
    INDEPENDENTLY_CLEARED = "INDEPENDENTLY_CLEARED"


# Classes that may define normality. Everything else is barred.
NORMALITY_DEFINING = frozenset({
    TrainingClass.VERIFIED_HEALTHY,
    TrainingClass.VERIFIED_WORKLOAD_SHIFT,
    TrainingClass.DECLARED_MAINTENANCE,
    TrainingClass.INDEPENDENTLY_CLEARED,
})

# Unresolved incidents must never define normality.
BARRED_FROM_NORMALITY = frozenset({
    TrainingClass.UNRESOLVED_ANOMALY,
    TrainingClass.CONFIRMED_REGRESSION,
    TrainingClass.INSUFFICIENT_OBSERVABILITY,
})


# ---------------------------------------------------------------------------
# Scopes: four permanent IDs per observation (D52)
# ---------------------------------------------------------------------------

ScopeId = Tuple[str, str, str, str]  # (service, region, endpoint, tenant)


@dataclass(frozen=True)
class Observation:
    scope: ScopeId
    metric: str
    value: float
    training_class: TrainingClass
    evidence_refs: Tuple[str, ...]


# ---------------------------------------------------------------------------
# Stages and the promotion gate
# ---------------------------------------------------------------------------

class Stage(str, Enum):
    FROZEN_REFERENCE = "FROZEN_REFERENCE"
    CANDIDATE = "CANDIDATE"
    SHADOW = "SHADOW"
    INDEPENDENTLY_QUALIFIED = "INDEPENDENTLY_QUALIFIED"
    PROMOTED = "PROMOTED"


_ALLOWED_TRANSITIONS = {
    Stage.CANDIDATE: {Stage.SHADOW},
    Stage.SHADOW: {Stage.INDEPENDENTLY_QUALIFIED},
    # NOTE: INDEPENDENTLY_QUALIFIED -> PROMOTED is deliberately absent.
    # PROMOTED is reachable only via promote(), which runs the full gate.
}


@dataclass(frozen=True)
class BaselineRecord:
    """One immutable entry in the append-only baseline ledger."""
    record_id: str
    scope: ScopeId
    metric: str
    value: float
    stage: Stage
    set_by: str
    set_at: str  # ISO-8601
    evidence_refs: Tuple[str, ...]
    supersedes: Optional[str]      # previous record_id for this scope+metric
    comparison: Tuple[Tuple[str, str], ...]  # ((field, old->new), ...)
    reason: str
    verifier: Optional[str]        # independent qualifier; None until qualified
    certified: bool = False        # certification transferred only per-scope


class BaselineLedger:
    """Append-only. Old baselines are superseded, never overwritten."""

    def __init__(self) -> None:
        self._records: List[BaselineRecord] = []
        self._by_id: Dict[str, BaselineRecord] = {}

    def append(self, record: BaselineRecord) -> BaselineRecord:
        if record.record_id in self._by_id:
            raise ValueError(f"DUPLICATE_RECORD {record.record_id}")
        if record.supersedes is not None and record.supersedes not in self._by_id:
            raise ValueError(f"UNKNOWN_SUPERSEDED {record.supersedes}")
        self._records.append(record)
        self._by_id[record.record_id] = record
        return record

    def current(self, scope: ScopeId, metric: str) -> Optional[BaselineRecord]:
        for r in reversed(self._records):
            if r.scope == scope and r.metric == metric and r.stage == Stage.PROMOTED:
                return r
        return None

    def history(self, scope: ScopeId, metric: str) -> List[BaselineRecord]:
        return [r for r in self._records if r.scope == scope and r.metric == metric]

    def frozen_reference(self, scope: ScopeId, metric: str) -> Optional[BaselineRecord]:
        for r in self._records:
            if r.scope == scope and r.metric == metric and r.stage == Stage.FROZEN_REFERENCE:
                return r
        return None

    def verify_append_only(self) -> Tuple[bool, str]:
        """No record may be mutated or removed: every earlier record must still
        be present and identical. Returns (ok, detail)."""
        seen = set()
        for r in self._records:
            if r.record_id in seen:
                return False, f"DUPLICATE {r.record_id}"
            seen.add(r.record_id)
        return True, f"{len(self._records)} records, append-only intact"


# ---------------------------------------------------------------------------
# Promotion gate: conjunctive hard obligations (D49)
# ---------------------------------------------------------------------------

@dataclass
class PromotionRequest:
    scope: ScopeId
    metric: str
    candidate_value: float
    proposed_by: str
    proposed_at: str
    training_window: Tuple[Observation, ...]
    evidence_refs: Tuple[str, ...]
    comparison: Tuple[Tuple[str, str], ...]
    reason: str
    higher_is_better: bool = True  # metric direction for regression checks


@dataclass
class GateVerdict:
    passed: bool
    code: str
    detail: str
    failed_obligations: Tuple[str, ...] = ()


def _obligation_training_clean(req: PromotionRequest) -> Optional[str]:
    barred = [o for o in req.training_window if o.training_class in BARRED_FROM_NORMALITY]
    if barred:
        return (f"TRAINING_BARRED: {len(barred)} observation(s) classified "
                f"{sorted({o.training_class.value for o in barred})} may not define normality")
    if not req.training_window:
        return "TRAINING_EMPTY: no training window"
    if any(o.scope != req.scope or o.metric != req.metric for o in req.training_window):
        return "TRAINING_SCOPE_MISMATCH: training window must match the promoted scope+metric"
    return None


def _obligation_evidence_present(req: PromotionRequest) -> Optional[str]:
    if not req.evidence_refs:
        return "EVIDENCE_MISSING: promotion requires cited evidence refs"
    if not req.reason.strip():
        return "REASON_MISSING: promotion requires a stated reason"
    if not req.comparison:
        return "COMPARISON_MISSING: promotion requires recorded old-vs-new comparison"
    return None


def _obligation_independent_qualification(req: PromotionRequest, verifier: Optional[str]) -> Optional[str]:
    if verifier is None:
        return "QUALIFIER_MISSING: independent qualification required"
    if verifier == req.proposed_by:
        return "SELF_QUALIFICATION: verifier must differ from proposer"
    return None


def _obligation_no_local_regression(
    req: PromotionRequest,
    frozen: Optional[BaselineRecord],
    regression_tolerance: float,
) -> Optional[str]:
    """Aggregate improvement never overrides a local regression (D52).
    Regression direction follows the metric: for higher-is-better metrics a
    drop beyond tolerance is a regression; for lower-is-better (e.g.
    error_rate) a rise beyond tolerance is."""
    if frozen is None:
        return None
    if req.higher_is_better:
        regressed = req.candidate_value < frozen.value - regression_tolerance
    else:
        regressed = req.candidate_value > frozen.value + regression_tolerance
    if regressed:
        return (f"LOCAL_REGRESSION: candidate {req.candidate_value} regresses frozen "
                f"reference {frozen.value} beyond tolerance {regression_tolerance}")
    return None


def promotion_gate(
    req: PromotionRequest,
    ledger: BaselineLedger,
    verifier: Optional[str],
    regression_tolerance: float = 0.0,
) -> GateVerdict:
    """Conjunction of hard obligations. Any failure refuses promotion."""
    failures = []
    for check in (
        lambda: _obligation_training_clean(req),
        lambda: _obligation_evidence_present(req),
        lambda: _obligation_independent_qualification(req, verifier),
        lambda: _obligation_no_local_regression(
            req, ledger.frozen_reference(req.scope, req.metric), regression_tolerance),
    ):
        f = check()
        if f:
            failures.append(f)
    if failures:
        return GateVerdict(False, "PROMOTION_REFUSED", "; ".join(failures), tuple(failures))
    return GateVerdict(True, "PROMOTION_GRANTED", "all hard obligations satisfied")


def advance_stage(
    ledger: BaselineLedger,
    record: BaselineRecord,
    to_stage: Stage,
    *,
    verifier: Optional[str] = None,
    at: str = "",
) -> BaselineRecord:
    """Move a baseline through CANDIDATE -> SHADOW -> INDEPENDENTLY_QUALIFIED.
    PROMOTED is only reached via promote(), which runs the full gate."""
    if to_stage not in _ALLOWED_TRANSITIONS.get(record.stage, set()):
        raise ValueError(f"ILLEGAL_TRANSITION {record.stage.value} -> {to_stage.value}")
    if to_stage == Stage.INDEPENDENTLY_QUALIFIED:
        if verifier is None or verifier == record.set_by:
            raise ValueError("SELF_QUALIFICATION: independent verifier required")
    new = BaselineRecord(
        record_id=record.record_id + f"@{to_stage.value}",
        scope=record.scope, metric=record.metric, value=record.value,
        stage=to_stage, set_by=record.set_by, set_at=at or record.set_at,
        evidence_refs=record.evidence_refs, supersedes=record.record_id,
        comparison=record.comparison, reason=record.reason, verifier=verifier,
    )
    return ledger.append(new)


def promote(
    ledger: BaselineLedger,
    req: PromotionRequest,
    verifier: str,
    record_id: str,
    regression_tolerance: float = 0.0,
) -> Tuple[GateVerdict, Optional[BaselineRecord]]:
    """Run the gate; on PASS, append a PROMOTED record superseding the current.
    Old baselines are never overwritten — only superseded."""
    verdict = promotion_gate(req, ledger, verifier, regression_tolerance)
    if not verdict.passed:
        return verdict, None
    prev = ledger.current(req.scope, req.metric)
    rec = BaselineRecord(
        record_id=record_id, scope=req.scope, metric=req.metric,
        value=req.candidate_value, stage=Stage.PROMOTED,
        set_by=req.proposed_by, set_at=req.proposed_at,
        evidence_refs=req.evidence_refs,
        supersedes=prev.record_id if prev else None,
        comparison=req.comparison, reason=req.reason,
        verifier=verifier, certified=True,
    )
    return verdict, ledger.append(rec)


# ---------------------------------------------------------------------------
# Dual-reference comparison: adaptive vs frozen (D49)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class DualReferenceVerdict:
    divergent: bool
    code: str
    detail: str


def dual_reference_check(
    ledger: BaselineLedger,
    scope: ScopeId,
    metric: str,
    adaptive_value: float,
    tolerance: float,
) -> DualReferenceVerdict:
    """Compare the adaptive candidate against the frozen reference. The frozen
    reference is immutable, so if both 'drift together' the divergence is still
    detected — the adaptive model can never move the reference with it."""
    frozen = ledger.frozen_reference(scope, metric)
    if frozen is None:
        return DualReferenceVerdict(True, "NO_FROZEN_REFERENCE",
                                    "cannot compare: no frozen reference")
    if abs(adaptive_value - frozen.value) > tolerance:
        return DualReferenceVerdict(
            True, "ADAPTIVE_DIVERGED",
            f"adaptive {adaptive_value} diverged from frozen {frozen.value} "
            f"beyond tolerance {tolerance}")
    return DualReferenceVerdict(False, "CONSISTENT",
                                "adaptive model consistent with frozen reference")


# ---------------------------------------------------------------------------
# Statistical pooling: share estimates, never transfer certification (D52)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class PooledEstimate:
    scopes: Tuple[ScopeId, ...]
    metric: str
    pooled_value: float
    per_scope_qualified: Tuple[Tuple[ScopeId, bool], ...]


def pooled_estimate(
    ledger: BaselineLedger,
    scopes: Tuple[ScopeId, ...],
    metric: str,
    observations: Tuple[Observation, ...],
) -> PooledEstimate:
    """Pool estimates across comparable scopes. Qualification stays per-scope:
    a sparse scope under a healthy parent remains unqualified."""
    qualified = []
    for s in scopes:
        obs = [o for o in observations if o.scope == s and o.metric == metric]
        dense = len(obs) >= 3 and all(
            o.training_class in NORMALITY_DEFINING for o in obs)
        qualified.append((s, dense))
    vals = [o.value for o in observations
            if o.metric == metric and o.training_class in NORMALITY_DEFINING]
    pooled = sum(vals) / len(vals) if vals else float("nan")
    return PooledEstimate(scopes, metric, pooled, tuple(qualified))


# ---------------------------------------------------------------------------
# Drift detection: decisions on stale baselines are refused (task spec)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class DecisionCheck:
    allowed: bool
    code: str
    detail: str


def check_decision_baseline(
    ledger: BaselineLedger,
    scope: ScopeId,
    metric: str,
    baseline_record_id: str,
) -> DecisionCheck:
    """A decision computed on a baseline that is not the ledger's current
    PROMOTED version for that scope+metric is refused."""
    cur = ledger.current(scope, metric)
    if cur is None:
        return DecisionCheck(False, "NO_BASELINE",
                             "no promoted baseline for scope+metric")
    if cur.record_id != baseline_record_id:
        return DecisionCheck(
            False, "STALE_BASELINE",
            f"decision used {baseline_record_id}; current is {cur.record_id} "
            f"(value {cur.value}, set by {cur.set_by} at {cur.set_at})")
    return DecisionCheck(True, "BASELINE_CURRENT", "baseline matches ledger head")


# ---------------------------------------------------------------------------
# Cold reconstruction: every promotion must be rebuildable from its record
# ---------------------------------------------------------------------------

def reconstruct_promotion(record: BaselineRecord) -> Dict[str, object]:
    """Rebuild the full promotion decision from the record alone."""
    if record.stage != Stage.PROMOTED:
        raise ValueError("RECONSTRUCT_ONLY_PROMOTED")
    return {
        "scope": record.scope,
        "metric": record.metric,
        "new_value": record.value,
        "set_by": record.set_by,
        "set_at": record.set_at,
        "evidence_refs": list(record.evidence_refs),
        "supersedes": record.supersedes,
        "comparison": [f"{f}: {c}" for f, c in record.comparison],
        "reason": record.reason,
        "verifier": record.verifier,
        "certified": record.certified,
    }


# ---------------------------------------------------------------------------
# Audit: detect silent drift — PROMOTED records that bypassed the gate
# ---------------------------------------------------------------------------

def audit_promotions(ledger: BaselineLedger) -> Tuple[bool, Tuple[str, ...]]:
    """Every PROMOTED record must carry the gate's fingerprints: an independent
    verifier, evidence refs, a recorded comparison, a reason, and an intact
    supersede chain. A record smuggled in via direct append (silent drift) is
    flagged here."""
    problems: List[str] = []
    for r in ledger._records:
        if r.stage != Stage.PROMOTED:
            continue
        if not r.verifier:
            problems.append(f"SILENT_DRIFT {r.record_id}: no independent verifier")
        elif r.verifier == r.set_by:
            problems.append(f"SILENT_DRIFT {r.record_id}: self-qualified")
        if not r.evidence_refs:
            problems.append(f"SILENT_DRIFT {r.record_id}: no evidence refs")
        if not r.comparison:
            problems.append(f"SILENT_DRIFT {r.record_id}: no old-vs-new comparison")
        if not r.reason.strip():
            problems.append(f"SILENT_DRIFT {r.record_id}: no reason")
        if r.supersedes is not None and r.supersedes not in ledger._by_id:
            problems.append(f"BROKEN_CHAIN {r.record_id}: supersedes unknown record")
    # chain order: for each scope+metric, supersedes must link consecutive PROMOTEDs
    chains: Dict[Tuple[ScopeId, str], List[BaselineRecord]] = {}
    for r in ledger._records:
        if r.stage == Stage.PROMOTED:
            chains.setdefault((r.scope, r.metric), []).append(r)
    for (scope, metric), recs in chains.items():
        ids = {r.record_id for r in recs}
        for r in recs[1:]:
            if r.supersedes not in ids:
                problems.append(
                    f"BROKEN_CHAIN {r.record_id}: supersedes {r.supersedes} "
                    f"outside this scope+metric chain")
    return (len(problems) == 0, tuple(problems))


# ---------------------------------------------------------------------------
# does-not-claim boundary
# ---------------------------------------------------------------------------

DOES_NOT_CLAIM = (
    "This module governs baseline evolution records; it does not measure the "
    "outside world itself. A PROMOTED baseline is only as good as the evidence "
    "refs it cites and the independence of its verifier. Statistical checks "
    "here are structural guards, not a substitute for domain measurement."
)
