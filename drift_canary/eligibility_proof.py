"""D58 / AER-LIVE-3: Independent Eligibility Proof for Every Scheduling Opportunity.

The independent-eligibility law: count a scheduling opportunity toward a
fairness bound only when authorization, outstanding work, ready
dependencies, schedulable capacity, an actual applicable opportunity, and
consistent authoritative ordering are ALL independently established.
Worker-supplied eligibility assertions shall not substitute for this
evidence. Unknown eligibility stays explicitly unresolved — it manufactures
neither a violation nor a clearance.

The gap it closes: drift_canary/fairness.py's FairnessLedger trusts
SchedulingEvent.eligible — the scheduler's own flag. Trace consistency
does not prove the eligibility booleans were true. This module recomputes
eligibility from six verifier-supplied evidence components and yields
three-valued verdicts:

  ELIGIBLE     — all six components PROVEN. Counts toward the fairness bound.
  INELIGIBLE   — at least one component REFUTED. Does not count.
  UNDETERMINED — at least one component UNKNOWN (none refuted). Does not
                 count; triggers an evidence-recovery obligation naming the
                 missing components. Never a violation, never a clearance.

The busy-guard (D58, verbatim): never call a task ineligible just because
every worker was busy — under fair queueing, contention is exactly why
fairness matters. SCHEDULABLE_CAPACITY is therefore STRUCTURAL: provisioned
slots for the obligation's worker class (> 0) and routability. Instantaneous
worker busyness has no field in the evidence model — it cannot be an input.
A component outside the six raises UnknownComponentError (fail closed), so
a future "busy -> ineligible" hack cannot slip in through extra components.

Evidence-origin discipline: every Evidence declares its origin
(e.g. "law_registry", "work_queue_snapshot"). Origins on the tainted list
("scheduler_flag", "worker_trace", "worker_assertion", "self_report",
"unattested") raise TaintedOriginError — the scheduler's eligible flag is a
claim to be assessed, never evidence. Honest limit, stated plainly: origin
is DECLARED, not cryptographically attested; cross-seat review of
evidence-source wiring is the backstop. What the mechanism does enforce:
UNDETERMINED never counts, flag mismatches are detected, and unknown
components are rejected.

Composes with (additive only — nothing here modifies them):
  fairness.py — SchedulingEvent (the flag this module second-guesses),
                FairnessContract, FairnessLedger.
  fairness_verify.py — the three-link qualification this module's receipts
                feed: a counted opportunity is the honest E_o input.

SPEC + deterministic machinery. NOT wired into kernel/, KNOW, LAW, ACT, or
any live path. Wiring needs Shawn's word.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping

# ---------------------------------------------------------------------------
# 1. The six evidence components (D58 registration comment 6102339440).
# ---------------------------------------------------------------------------
AUTHORIZATION = "AUTHORIZATION"                    # LAW authorization held at the round
OUTSTANDING_WORK = "OUTSTANDING_WORK"            # uncompleted work remained
READY_DEPENDENCIES = "READY_DEPENDENCIES"        # all dependencies satisfied
SCHEDULABLE_CAPACITY = "SCHEDULABLE_CAPACITY"    # structural: provisioned + routable
APPLICABLE_OPPORTUNITY = "APPLICABLE_OPPORTUNITY"  # a real scheduling round existed
CONSISTENT_ORDERING = "CONSISTENT_ORDERING"      # single authoritative ordering

COMPONENTS = (
    AUTHORIZATION,
    OUTSTANDING_WORK,
    READY_DEPENDENCIES,
    SCHEDULABLE_CAPACITY,
    APPLICABLE_OPPORTUNITY,
    CONSISTENT_ORDERING,
)

# Evidence statuses: three-valued, never collapsed.
PROVEN = "PROVEN"
REFUTED = "REFUTED"
UNKNOWN = "UNKNOWN"
EVIDENCE_STATUSES = (PROVEN, REFUTED, UNKNOWN)

# Verdicts: three-valued. UNDETERMINED is not a soft INELIGIBLE.
ELIGIBLE = "ELIGIBLE"
INELIGIBLE = "INELIGIBLE"
UNDETERMINED = "UNDETERMINED"
VERDICTS = (ELIGIBLE, INELIGIBLE, UNDETERMINED)

# Flag assessments: what the scheduler's own flag looks like next to the
# verifier's verdict. The flag is a claim; this is the assessment of the claim.
HIDDEN_OPPORTUNITY = "HIDDEN_OPPORTUNITY"  # verdict ELIGIBLE, flag False: breach signal
FALSE_CLAIM = "FALSE_CLAIM"                # verdict INELIGIBLE, flag True: refused
CONSISTENT = "CONSISTENT"
DEFERRED = "DEFERRED"                      # verdict UNDETERMINED: no accusation, no clearance
NOT_ASSESSED = "NOT_ASSESSED"              # no flag supplied

# Origins that may never back an evidence component: the worker's own trace
# and the scheduler's flag are claims, not evidence.
TAINTED_ORIGINS = frozenset({
    "scheduler_flag",
    "worker_trace",
    "worker_assertion",
    "self_report",
    "unattested",
})


class EligibilityProofError(Exception):
    """Base for fail-closed eligibility-proof errors."""


class UnknownComponentError(EligibilityProofError):
    """An evidence component outside the six was supplied. Fail closed."""


class TaintedOriginError(EligibilityProofError):
    """Evidence backed by a worker/scheduler-supplied origin. Fail closed."""


@dataclass(frozen=True)
class Evidence:
    """One component's evidence, as established by the VERIFIER.

    status: PROVEN | REFUTED | UNKNOWN.
    detail: human-auditable note (what was checked, what was found).
    origin: the independent source that established it
            (e.g. "law_registry"). Tainted origins are rejected at prove().
    """
    status: str
    detail: str
    origin: str

    def __post_init__(self):
        assert self.status in EVIDENCE_STATUSES, f"bad status: {self.status}"
        assert self.detail, "evidence needs a detail note"
        assert self.origin, "evidence needs a declared origin"


def missing_evidence(component: str) -> Evidence:
    """The fail-closed default: a component the source did not supply."""
    return Evidence(UNKNOWN, f"{component} not supplied by evidence source", "absent")


@dataclass(frozen=True)
class EligibilityReceipt:
    """The verifier's verdict for one scheduling opportunity.

    Frozen: the verdict cannot be flipped without replacing the receipt,
    and the per-component evidence travels with it for audit.
    """
    opportunity_id: str
    obligation_id: str
    round_seq: int
    verdict: str
    components: tuple          # ((component, Evidence), ...) — all six
    refuted: tuple = ()        # components REFUTED
    unknown: tuple = ()        # components UNKNOWN
    recovery_obligation: tuple = ()  # UNDETERMINED only: missing components to recover
    flag_assessment: str = NOT_ASSESSED
    counts_toward_bound: bool = False

    def __post_init__(self):
        assert self.verdict in VERDICTS, f"bad verdict: {self.verdict}"
        names = [c for c, _ in self.components]
        assert tuple(names) == COMPONENTS, f"receipt must carry all six: {names}"
        if self.verdict == ELIGIBLE:
            assert not self.refuted and not self.unknown, "ELIGIBLE with gaps"
            assert self.counts_toward_bound, "ELIGIBLE must count"
            assert not self.recovery_obligation, "ELIGIBLE needs no recovery"
        if self.verdict == INELIGIBLE:
            assert self.refuted, "INELIGIBLE needs a refuted component"
            assert not self.counts_toward_bound, "INELIGIBLE must not count"
        if self.verdict == UNDETERMINED:
            assert self.unknown and not self.refuted, "UNDETERMINED shape wrong"
            assert tuple(self.recovery_obligation) == tuple(self.unknown), \
                "recovery obligation must name exactly the unknown components"
            assert not self.counts_toward_bound, "UNDETERMINED must not count"
            assert self.flag_assessment in (DEFERRED, NOT_ASSESSED), \
                "UNDETERMINED manufactures neither violation nor clearance"

    def to_dict(self) -> dict:
        return {
            "opportunity_id": self.opportunity_id,
            "obligation_id": self.obligation_id,
            "round_seq": self.round_seq,
            "verdict": self.verdict,
            "components": {c: {"status": e.status, "detail": e.detail, "origin": e.origin}
                           for c, e in self.components},
            "refuted": list(self.refuted),
            "unknown": list(self.unknown),
            "recovery_obligation": list(self.recovery_obligation),
            "flag_assessment": self.flag_assessment,
            "counts_toward_bound": self.counts_toward_bound,
        }


class EligibilityProver:
    """Computes D58 eligibility verdicts from verifier evidence.

    The prover takes an evidence source (component -> Evidence) supplied by
    the verifier. It NEVER reads the scheduler's eligible flag as evidence;
    the flag may be passed to assess_flag() for claim assessment only.
    """

    def __init__(self, evidence_source: Mapping[str, Evidence]):
        unknown_keys = [k for k in evidence_source if k not in COMPONENTS]
        if unknown_keys:
            raise UnknownComponentError(
                f"components outside the six: {unknown_keys} — fail closed")
        self._source = dict(evidence_source)

    def _resolve(self, component: str) -> Evidence:
        ev = self._source.get(component)
        if ev is None:
            return missing_evidence(component)
        if not isinstance(ev, Evidence):
            raise EligibilityProofError(
                f"{component}: not an Evidence instance — fail closed")
        if ev.origin in TAINTED_ORIGINS:
            raise TaintedOriginError(
                f"{component}: tainted origin '{ev.origin}' — "
                f"worker/scheduler claims are not evidence")
        return ev

    def prove(self, opportunity_id: str, obligation_id: str, round_seq: int,
              scheduler_flag: bool | None = None) -> EligibilityReceipt:
        """Derive the three-valued verdict for one scheduling opportunity."""
        resolved = tuple((c, self._resolve(c)) for c in COMPONENTS)
        refuted = tuple(c for c, e in resolved if e.status == REFUTED)
        unknown = tuple(c for c, e in resolved if e.status == UNKNOWN)

        if refuted:
            verdict = INELIGIBLE
        elif unknown:
            verdict = UNDETERMINED
        else:
            verdict = ELIGIBLE

        assessment = self.assess_flag(verdict, scheduler_flag)
        return EligibilityReceipt(
            opportunity_id=opportunity_id,
            obligation_id=obligation_id,
            round_seq=round_seq,
            verdict=verdict,
            components=resolved,
            refuted=refuted,
            unknown=unknown,
            recovery_obligation=unknown,
            flag_assessment=assessment,
            counts_toward_bound=(verdict == ELIGIBLE),
        )

    @staticmethod
    def assess_flag(verdict: str, scheduler_flag: bool | None) -> str:
        """Assess the scheduler's eligibility claim against the verdict.

        The flag is a claim, never evidence. UNDETERMINED defers judgment —
        it manufactures neither a violation nor a clearance.
        """
        assert verdict in VERDICTS, f"bad verdict: {verdict}"
        if scheduler_flag is None:
            return NOT_ASSESSED
        if verdict == UNDETERMINED:
            return DEFERRED
        if verdict == ELIGIBLE and not scheduler_flag:
            return HIDDEN_OPPORTUNITY
        if verdict == INELIGIBLE and scheduler_flag:
            return FALSE_CLAIM
        return CONSISTENT


@dataclass
class EligibilityBoundCounter:
    """Counts scheduling opportunities toward a fairness bound — but only
    verifier-proven ELIGIBLE ones. The honest replacement for counting
    SchedulingEvent.eligible flags.

    debt_for(oid) is the D58-correct fairness debt: eligible opportunities
    elapsed without adequate service. Service accounting itself stays with
    FairnessLedger; this counter owns only the eligibility side.
    """
    _counts: dict = field(default_factory=dict)   # oid -> int
    _receipts: list = field(default_factory=list)

    def count(self, receipt: EligibilityReceipt) -> int:
        """Record one opportunity. Returns 1 if it counts, else 0."""
        assert isinstance(receipt, EligibilityReceipt), "count takes a receipt"
        self._receipts.append(receipt)
        oid = receipt.obligation_id
        self._counts.setdefault(oid, 0)
        if receipt.counts_toward_bound:
            self._counts[oid] += 1
            return 1
        return 0

    def debt_for(self, obligation_id: str) -> int:
        return self._counts.get(obligation_id, 0)

    def hidden_opportunities(self) -> list:
        """Receipts where the scheduler hid a genuine opportunity (E2-a)."""
        return [r for r in self._receipts
                if r.flag_assessment == HIDDEN_OPPORTUNITY]

    def false_claims(self) -> list:
        """Receipts where a claimed eligibility was refuted (E2-b)."""
        return [r for r in self._receipts
                if r.flag_assessment == FALSE_CLAIM]

    def open_recoveries(self) -> list:
        """UNDETERMINED receipts and their missing components."""
        return [(r.opportunity_id, list(r.recovery_obligation))
                for r in self._receipts if r.verdict == UNDETERMINED]
