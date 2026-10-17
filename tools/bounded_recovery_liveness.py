#!/usr/bin/env python3
"""D56 — Proving Bounded Recovery Liveness (AER-LIVE-2).

Bounded-liveness law: claim it only where eligibility, scheduling
opportunities, usable service, progress witnesses, capacity assumptions,
and the governing bound are all independently established. A timeout may
prove a specific deadline breach — it shall never by itself establish a
fairness failure. Safety holds stay authoritative; liveness machinery may
demand investigation or escalation but never manufactures permission or
completion.

Four claims, kept separate — never merged into one verdict:
  safety              — the hold / safety predicate still authoritative
  scheduling_fairness — eligible work got its scheduling opportunities
  bounded_progress    — serviced work showed verified progress in bound
  task_completion     — the required outcome was established in bound

Three evidenced facts (dispatch is not service, a heartbeat is not
progress):
  enabled    — legally permitted to execute (eligibility segment)
  serviced   — usable execution opportunity WITH reconstructable evidence
  progressed — verifiable state advance (genuine progress mark)

Three bounds, each enforced only after its assumptions are proven:
  SERVICE     — eligible obligation receives adequate service within B_s
  PROGRESS    — serviced obligation shows verified progress within B_p
  DISPOSITION — accepted obligation reaches a governed disposition within B_d

The bound clock counts ELIGIBLE time only. WAITING_AUTHORITY,
SAFETY_HOLD, and OUTAGE_VERIFIED segments are excluded: thirty minutes
outstanding with twenty-nine in a verified provider outage is not a
scheduler failure, and a wall-clock timeout is never by itself a
fairness failure.

Composes with (no duplicate mechanism):
  tools/safety_liveness_classifier.py (D55, PR #2302) — the safety/
    liveness classifier this prover consumes duck-typed via from_d55().
    D55 classifies; D56 proves bounded liveness on top. Nothing here
    re-implements the tri-fact or the VALID_HOLD contract.
  drift_canary/fairness.py (D24, on main) — SERVICE_LADDER rungs and
    SERVICE_EVIDENCE_FIELDS mirrored here as canonical constants; the
    ledger itself is not re-implemented.
  drift_canary/progress.py (D23, on main) — W(s) ranking is the progress
    measure; this module consumes progress marks, it does not re-rank.
  drift_canary/liveness.py (D22, on main) — WAITING_AUTHORITY taxonomy
    and the liveness-never-creates-permission rule, honored by
    construction (no transition out of WAITING_AUTHORITY exists here).

SPEC + deterministic machinery. NOT wired into kernel/, KNOW, LAW, ACT,
or any live path. Wiring needs Shawn's word.

Directive: D56, wave 5, owner naya2. Source: issue comment 6102289345.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field, asdict
from typing import Any, Callable, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Eligibility segments: the bound clock counts ELIGIBLE time only.
# ---------------------------------------------------------------------------

ELIGIBLE = "eligible"                  # permitted and able to progress
WAITING_AUTHORITY = "waiting_authority"  # a LAW decision is required
SAFETY_HOLD = "safety_hold"            # legitimately prohibited; hold is correct
OUTAGE_VERIFIED = "outage_verified"    # verified provider outage, outside control
DISPOSITIONED = "dispositioned"        # reached a governed disposition (terminal)

SEGMENT_STATES = (ELIGIBLE, WAITING_AUTHORITY, SAFETY_HOLD,
                  OUTAGE_VERIFIED, DISPOSITIONED)

# States whose time is EXCLUDED from every bound clock. Waiting on
# authority, a correct safety hold, or a verified outage is never
# scheduler debt.
EXCLUDED_FROM_BOUND_CLOCK = (WAITING_AUTHORITY, SAFETY_HOLD, OUTAGE_VERIFIED)


@dataclass(frozen=True)
class EligibilitySegment:
    """One contiguous interval of an obligation's eligibility state."""
    state: str
    start: int      # inclusive, in clock units
    end: int        # exclusive

    def __post_init__(self):
        assert self.state in SEGMENT_STATES, f"unknown segment state {self.state}"
        assert self.end > self.start, "segments must have positive duration"

    @property
    def duration(self) -> int:
        return self.end - self.start


def eligible_time(segments: Tuple[EligibilitySegment, ...]) -> int:
    """Bound-clock time: ELIGIBLE segments only. Everything excluded by
    EXCLUDED_FROM_BOUND_CLOCK contributes zero — a wall clock that counts
    outage or waiting-authority time is the TIME_ONLY detector, rejected."""
    return sum(s.duration for s in segments if s.state == ELIGIBLE)


def wall_time(segments: Tuple[EligibilitySegment, ...]) -> int:
    return sum(s.duration for s in segments)


# ---------------------------------------------------------------------------
# Service ladder (canonical: drift_canary/fairness.py SERVICE_LADDER).
# ---------------------------------------------------------------------------

SERVICE_LADDER = (
    "SELECTED",    # scheduler chose the task
    "DISPATCHED",  # work lease / execution opportunity issued
    "SERVICED",    # usable execution opportunity received (evidence required)
    "ATTEMPTED",   # a valid transition was actually attempted
    "ADVANCED",    # a verified transition reduced outstanding work
    "COMPLETED",   # the required outcome was established
)

ADEQUATE_SERVICE_RUNG = "SERVICED"

# Reconstructable evidence of adequate service. A bare scheduler assertion
# ("I scheduled it") satisfies none of these — without them the event is
# recorded as DISPATCHED-ONLY and the bound clock keeps running.
SERVICE_EVIDENCE_FIELDS = (
    "lease_id",            # bounded execution lease issued
    "worker_ack",           # worker acknowledged receipt of the opportunity
    "resources_available",  # required resources were actually available
)

# Event kinds that NEVER count as progress, no matter how many occur.
NON_PROGRESS_EVENTS = (
    "heartbeat",
    "log_line",
    "status_rewrite",
    "retry_attempt",       # a bare retry, without an obligation state change
)


@dataclass(frozen=True)
class ServiceObservation:
    """One observed service event with its evidence."""
    seq: int
    rung: str
    evidence: Tuple[Tuple[str, str], ...] = ()  # ((field, value), ...)

    def __post_init__(self):
        assert self.rung in SERVICE_LADDER, f"unknown rung {self.rung}"

    def is_usable_service(self) -> bool:
        """Usable service = at/above SERVICED on the ladder WITH all
        evidence fields present. Dispatch without evidence is
        DISPATCHED-ONLY: it earns no service credit."""
        if SERVICE_LADDER.index(self.rung) < SERVICE_LADDER.index(ADEQUATE_SERVICE_RUNG):
            return False
        present = {k for k, _ in self.evidence}
        return all(f in present for f in SERVICE_EVIDENCE_FIELDS)


@dataclass(frozen=True)
class ProgressMark:
    """One observed progress event. Genuine only if it changed the state
    of a required proof obligation or moved toward a valid outcome."""
    seq: int
    kind: str
    state_advance: bool = False
    moves_toward_outcome: bool = False

    def is_genuine(self) -> bool:
        if self.kind in NON_PROGRESS_EVENTS:
            return False
        return bool(self.state_advance or self.moves_toward_outcome)


# ---------------------------------------------------------------------------
# The six independently-established preconditions. A bound is ENFORCED
# only when all six hold; otherwise every claim is UNPROVEN (unknown),
# never "passed", never "failed".
# ---------------------------------------------------------------------------

PRECONDITIONS = (
    "eligibility",            # eligibility established with evidence
    "opportunities",          # scheduling opportunities observed + counted
    "usable_service",         # usable-service evidence available to check
    "progress_witnesses",     # progress witnesses available to check
    "capacity_assumptions",   # capacity assumptions stated (proven separately)
    "governing_bound",        # the bound itself stated with source
)


@dataclass(frozen=True)
class Precondition:
    name: str
    established: bool
    evidence: str = ""

    def __post_init__(self):
        assert self.name in PRECONDITIONS, f"unknown precondition {self.name}"


@dataclass(frozen=True)
class Assumption:
    """One assumption a bound's enforcement rests on. Proven before
    enforcement — an unproven assumption makes the bound UNENFORCEABLE,
    and any verdict drawn from it is rejected, not trusted."""
    statement: str
    proven: bool
    proof_ref: str = ""


# ---------------------------------------------------------------------------
# The three bounds.
# ---------------------------------------------------------------------------

SERVICE = "service"            # adequate service within B_s of eligible time
PROGRESS = "progress"          # verified progress within B_p of eligible time
DISPOSITION = "disposition"    # governed disposition within B_d of eligible time

BOUND_KINDS = (SERVICE, PROGRESS, DISPOSITION)


@dataclass(frozen=True)
class Bound:
    kind: str
    limit: int                       # eligible-time units
    assumptions: Tuple[Assumption, ...]
    evidence: str = ""               # where the bound comes from
    label: str = ""

    def __post_init__(self):
        assert self.kind in BOUND_KINDS, f"unknown bound kind {self.kind}"
        assert self.limit > 0, "bounds must be positive"


def enforceable(bound: Bound) -> Tuple[bool, str]:
    """A bound is enforceable only when every assumption it rests on is
    proven. Returns (ok, reason)."""
    unproven = [a.statement for a in bound.assumptions if not a.proven]
    if unproven:
        return False, (f"bound {bound.label or bound.kind} not enforceable: "
                       f"unproven assumptions: {'; '.join(unproven)}")
    return True, "all bound assumptions proven"


# ---------------------------------------------------------------------------
# Four-claim verdict. The slots are independent; there is deliberately no
# merged PASS/FAIL — a single boolean would let one truth hide another.
# ---------------------------------------------------------------------------

HOLDS = "holds"
VIOLATED = "violated"
UNPROVEN = "unproven"
NOT_APPLICABLE = "not_applicable"

CLAIM_STATES = (HOLDS, VIOLATED, UNPROVEN, NOT_APPLICABLE)


@dataclass(frozen=True)
class BoundedLivenessVerdict:
    """Four independent claims about one obligation under one bound."""
    obligation: str
    bound_kind: str
    bound_enforceable: bool
    eligible_time: int
    wall_time: int
    safety: str               # the safety hold stays authoritative
    scheduling_fairness: str  # eligible work got its opportunities
    bounded_progress: str     # serviced work progressed in bound
    task_completion: str      # required outcome established in bound
    detail: str = ""

    def __post_init__(self):
        for slot in (self.safety, self.scheduling_fairness,
                     self.bounded_progress, self.task_completion):
            assert slot in CLAIM_STATES, f"unknown claim state {slot}"

    def as_dict(self) -> Dict[str, Any]:
        return {
            "obligation": self.obligation,
            "bound_kind": self.bound_kind,
            "bound_enforceable": self.bound_enforceable,
            "eligible_time": self.eligible_time,
            "wall_time": self.wall_time,
            "safety": self.safety,
            "scheduling_fairness": self.scheduling_fairness,
            "bounded_progress": self.bounded_progress,
            "task_completion": self.task_completion,
            "detail": self.detail,
        }


def _unproven(obligation: str, bound: Bound, segments, detail: str) -> BoundedLivenessVerdict:
    return BoundedLivenessVerdict(
        obligation=obligation, bound_kind=bound.kind,
        bound_enforceable=False,
        eligible_time=eligible_time(segments), wall_time=wall_time(segments),
        safety=UNPROVEN, scheduling_fairness=UNPROVEN,
        bounded_progress=UNPROVEN, task_completion=UNPROVEN,
        detail=detail,
    )

# ---------------------------------------------------------------------------
# Assessment. The prover never manufactures permission or completion.
# ---------------------------------------------------------------------------

@dataclass
class ObligationHistory:
    """Everything the prover may look at for one obligation."""
    obligation: str
    segments: Tuple[EligibilitySegment, ...]
    service_observations: Tuple[ServiceObservation, ...] = ()
    progress_marks: Tuple[ProgressMark, ...] = ()
    disposition: str = ""          # governed disposition, if reached
    disposition_evidence: str = ""


def _has_usable_service(history: ObligationHistory) -> bool:
    return any(o.is_usable_service() for o in history.service_observations)


def _has_genuine_progress(history: ObligationHistory) -> bool:
    return any(m.is_genuine() for m in history.progress_marks)


def _has_governed_disposition(history: ObligationHistory) -> bool:
    return bool(history.disposition.strip())


def assess(history: ObligationHistory, bound: Bound,
           preconditions: Tuple[Precondition, ...]) -> BoundedLivenessVerdict:
    """Prove (or refuse to prove) bounded liveness for one obligation.

    Fail-closed order:
      1. All six preconditions established, else every claim UNPROVEN.
      2. Bound enforceable (assumptions proven), else every claim UNPROVEN.
      3. Bound clock = ELIGIBLE time only. Waiting-authority, safety-hold,
         and verified-outage segments contribute zero.
      4. Four claims assessed independently; a WAITING_AUTHORITY or
         SAFETY_HOLD obligation can never yield a fairness VIOLATED, and
         the prover never transitions anything out of those states.

    Returns a BoundedLivenessVerdict. Never raises on missing evidence:
    missing evidence is UNPROVEN, not an exception.
    """
    segs = history.segments
    elig = eligible_time(segs)
    wall = wall_time(segs)

    missing = [p.name for p in preconditions if not p.established]
    if missing:
        return _unproven(history.obligation, bound, segs,
                         f"preconditions not established: {', '.join(missing)}; "
                         f"claims unknown, not failed")

    ok, reason = enforceable(bound)
    if not ok:
        return _unproven(history.obligation, bound, segs,
                         f"bound not enforceable: {reason}")

    held_states = {s.state for s in segs}
    under_hold = bool(held_states & {WAITING_AUTHORITY, SAFETY_HOLD})
    ever_eligible = elig > 0

    # Safety: authoritative unless evidenced otherwise. The prover takes the
    # hold as given — it never weakens it, and a hold is never a violation.
    safety = HOLDS

    # Scheduling fairness: a fairness failure needs eligible time beyond the
    # bound with no usable service. A held obligation is never starved.
    if under_hold and not ever_eligible:
        scheduling_fairness = NOT_APPLICABLE
        fair_detail = "obligation never eligible: fairness not applicable, hold authoritative"
    elif bound.kind == SERVICE:
        if elig > bound.limit and not _has_usable_service(history):
            scheduling_fairness = VIOLATED
            fair_detail = (f"eligible {elig} > bound {bound.limit} with no "
                           f"usable service: bounded-service breach")
        else:
            scheduling_fairness = HOLDS
            fair_detail = (f"eligible {elig} within bound {bound.limit} or "
                           f"usable service observed")
    else:
        # Fairness is still assessed for progress/disposition bounds: an
        # obligation that never got usable service cannot be failed for
        # lack of progress — the failure is the scheduler's, not the work's.
        if ever_eligible and not _has_usable_service(history) and elig > bound.limit:
            scheduling_fairness = VIOLATED
            fair_detail = (f"eligible {elig} > bound {bound.limit}, no usable "
                           f"service: scheduler failure, not a progress failure")
        else:
            scheduling_fairness = HOLDS
            fair_detail = "no scheduling breach on eligible time"

    # Bounded progress: serviced work must show verified progress in bound.
    # Unserviced work cannot fail progress — that would blame the worker
    # for the scheduler's failure (D24's separation).
    if bound.kind == PROGRESS:
        if not _has_usable_service(history):
            bounded_progress = NOT_APPLICABLE
            prog_detail = "no usable service: progress not assessable (see scheduling_fairness)"
        elif elig > bound.limit and not _has_genuine_progress(history):
            bounded_progress = VIOLATED
            prog_detail = (f"serviced {elig} eligible units > bound "
                           f"{bound.limit} with no genuine progress")
        else:
            bounded_progress = HOLDS
            prog_detail = "genuine progress within bound or bound not exceeded"
    else:
        bounded_progress = NOT_APPLICABLE
        prog_detail = f"bound kind is {bound.kind}, not progress"

    # Task completion: the required outcome established in bound. A timeout
    # may prove a deadline breach here — it never establishes a fairness
    # failure (that slot is decided above, on eligible time + service).
    if bound.kind == DISPOSITION:
        if _has_governed_disposition(history):
            task_completion = HOLDS
            comp_detail = f"governed disposition reached: {history.disposition}"
        elif elig > bound.limit:
            task_completion = VIOLATED
            comp_detail = (f"no governed disposition within {bound.limit} "
                           f"eligible units (eligible {elig}): deadline breach")
        else:
            task_completion = HOLDS
            comp_detail = "disposition bound not exceeded on eligible time"
    elif _has_governed_disposition(history):
        task_completion = HOLDS
        comp_detail = f"governed disposition reached: {history.disposition}"
    else:
        task_completion = UNPROVEN
        comp_detail = f"bound kind is {bound.kind}: completion not claimed"

    detail = "; ".join([fair_detail, prog_detail, comp_detail,
                        f"eligible {elig} / wall {wall}"])
    return BoundedLivenessVerdict(
        obligation=history.obligation, bound_kind=bound.kind,
        bound_enforceable=True, eligible_time=elig, wall_time=wall,
        safety=safety, scheduling_fairness=scheduling_fairness,
        bounded_progress=bounded_progress, task_completion=task_completion,
        detail=detail,
    )


# ---------------------------------------------------------------------------
# The TIME_ONLY detector — the wrong procedure, kept for rejection.
# ---------------------------------------------------------------------------
# A detector that compares wall-clock time against the bound without
# excluding waiting-authority, safety-hold, or verified-outage segments.
# AER-LIVE-002 proves it indiscriminate: it gives the authority-blocked
# history and the starved history the SAME verdict. It exists here so the
# verifier can demonstrate the rejection mechanically. NEVER use it for
# decisions.

def time_only_verdict(history: ObligationHistory, bound: Bound) -> str:
    """Wall-clock-only breach check. WRONG BY DESIGN — provided so the
    experiment can prove it indiscriminate."""
    if wall_time(history.segments) > bound.limit:
        return "BREACH"
    return "NO_BREACH"


# ---------------------------------------------------------------------------
# D55 seam — duck-typed, no import of the unmerged module.
# ---------------------------------------------------------------------------
# D55 (tools/safety_liveness_classifier.py, PR #2302) classifies safety vs
# liveness with the tri-fact. D56 consumes that classification to decide
# which segments of a D55 obligation were eligible. The adapter binds on
# attribute shape (.auth with a .value, .events list of (.kind, .detail))
# and RAISES rather than imagining fields — same contract as D28's
# from_d27().

def from_d55(obligation: Any, d55: Any = None) -> Tuple[EligibilitySegment, ...]:
    """Map a D55-style obligation to eligibility segments.

    d55: the D55 module (or a compatible namespace) providing AuthState
    with WITHDRAWN / GRANTED / MISSING_DECISION members. When omitted,
    the obligation's auth must already be a plain string naming one of
    the three states.

    Because D55 obligations do not carry segment timelines, the mapping
    is honest about its coarseness: one segment covering the whole
    observed span, state derived from the auth state. Finer timelines
    are the caller's job — this adapter never invents them.
    """
    auth = getattr(obligation, "auth", None)
    if auth is None:
        raise ValueError("from_d55: obligation has no .auth; refusing to imagine one")
    if d55 is not None:
        states = getattr(d55, "AuthState", None)
        if states is None:
            raise ValueError("from_d55: d55 module has no AuthState")
        withdrawn = getattr(states, "WITHDRAWN", None)
        granted = getattr(states, "GRANTED", None)
        missing = getattr(states, "MISSING_DECISION", None)
        if auth == withdrawn:
            state = SAFETY_HOLD
        elif auth == granted:
            state = ELIGIBLE
        elif auth == missing:
            state = WAITING_AUTHORITY
        else:
            raise ValueError(f"from_d55: unrecognized auth state {auth!r}")
    else:
        if auth not in ("withdrawn", "granted", "missing_decision"):
            raise ValueError(f"from_d55: unrecognized auth string {auth!r}")
        state = {"withdrawn": SAFETY_HOLD, "granted": ELIGIBLE,
                 "missing_decision": WAITING_AUTHORITY}[auth]
    events = getattr(obligation, "events", None)
    span = max(1, len(events) if isinstance(events, (list, tuple)) else 1)
    return (EligibilitySegment(state, 0, span),)


# ---------------------------------------------------------------------------
# AER-LIVE-002: timeout versus proven bounded-service breach.
# ---------------------------------------------------------------------------
# Two histories with IDENTICAL wall-clock timeout patterns (30 units vs a
# bound of 10). One is blocked by missing authority; the other is
# continuously enabled but starved. A time-only detector gives both the
# same verdict and must be rejected. The corrected detector preserves
# waiting-authority for the first and detects the bounded-service breach
# in the second — with zero false fairness violations on the safety-hold
# controls.

BOUND_LIMIT = 10

def _proven(label: str) -> Assumption:
    return Assumption(label, True, proof_ref=f"aer-live-002:{label}")


def _six_preconditions() -> Tuple[Precondition, ...]:
    return tuple(Precondition(name, True, evidence=f"aer-live-002:{name}")
                 for name in PRECONDITIONS)


def _service_bound() -> Bound:
    return Bound(
        kind=SERVICE, limit=BOUND_LIMIT, label="AER-LIVE-002 service bound",
        evidence="capacity model C-7: single worker, 1 obligation, bound 10 eligible units",
        assumptions=(
            _proven("capacity model C-7 matches the real scheduler"),
            _proven("scheduler policy is the modeled FIFO policy"),
            _proven("bound 10 derived from C-7 capacity, not arbitrary"),
        ),
    )


def _history_authority_blocked() -> ObligationHistory:
    # 29 units waiting on a LAW decision, 1 unit eligible and serviced.
    # Wall clock 30 > bound 10. Eligible time 1 < 10. No breach.
    return ObligationHistory(
        obligation="reconciliation-retry",
        segments=(
            EligibilitySegment(WAITING_AUTHORITY, 0, 29),
            EligibilitySegment(ELIGIBLE, 29, 30),
        ),
        service_observations=(
            ServiceObservation(29, "SERVICED",
                               (("lease_id", "L-99"), ("worker_ack", "ack-99"),
                                ("resources_available", "yes"))),
        ),
        progress_marks=(
            ProgressMark(29, "lease_accepted", moves_toward_outcome=True),
        ),
    )


def _history_starved() -> ObligationHistory:
    # 30 units continuously eligible, zero usable service. Wall 30,
    # eligible 30 > bound 10. Bounded-service breach.
    return ObligationHistory(
        obligation="reconciliation-retry",
        segments=(EligibilitySegment(ELIGIBLE, 0, 30),),
        service_observations=(
            # DISPATCHED without evidence: DISPATCHED-ONLY, not service.
            ServiceObservation(5, "DISPATCHED", ()),
            ServiceObservation(15, "DISPATCHED", ()),
            ServiceObservation(25, "DISPATCHED", (("lease_id", "L-x"),)),
        ),
        progress_marks=(
            ProgressMark(6, "heartbeat"),
            ProgressMark(16, "heartbeat"),
            ProgressMark(26, "log_line"),
        ),
    )


def _history_safety_hold() -> ObligationHistory:
    # 30 units under a correct safety hold (authorization withdrawn).
    # No breach, no fairness violation — the hold is authoritative.
    return ObligationHistory(
        obligation="retry-blocked-action",
        segments=(EligibilitySegment(SAFETY_HOLD, 0, 30),),
        service_observations=(),
        progress_marks=(),
        disposition="held",
        disposition_evidence="LAW decision L-118 prohibits retry during incident",
    )


def _history_outage() -> ObligationHistory:
    # 29 units verified provider outage + 1 eligible. The directive's
    # "thirty minutes outstanding with twenty-nine in a verified provider
    # outage is not a scheduler failure".
    return ObligationHistory(
        obligation="reconciliation-retry",
        segments=(
            EligibilitySegment(OUTAGE_VERIFIED, 0, 29),
            EligibilitySegment(ELIGIBLE, 29, 30),
        ),
        service_observations=(
            ServiceObservation(29, "SERVICED",
                               (("lease_id", "L-100"), ("worker_ack", "ack-100"),
                                ("resources_available", "yes"))),
        ),
    )


HISTORIES: Dict[str, Callable[[], ObligationHistory]] = {
    "H1": _history_authority_blocked,
    "H2": _history_starved,
    "H3": _history_safety_hold,
    "H4": _history_outage,
}


def run_history(history_id: str) -> BoundedLivenessVerdict:
    return assess(HISTORIES[history_id](), _service_bound(), _six_preconditions())


def run_aer_live_002() -> Dict[str, BoundedLivenessVerdict]:
    return {hid: run_history(hid) for hid in ("H1", "H2", "H3", "H4")}


def verify_aer_live_002(results: Dict[str, BoundedLivenessVerdict]) -> List[str]:
    """Verify the directive's acceptance criteria. Empty list = PASS."""
    violations: List[str] = []
    for hid in ("H1", "H2", "H3", "H4"):
        if hid not in results:
            violations.append(f"missing history {hid}")
    if violations:
        return violations

    bound = _service_bound()

    # (1) The time-only detector is indiscriminate: identical wall-clock
    # patterns (H1 authority-blocked, H2 starved) get the SAME verdict.
    # A procedure that cannot tell them apart is rejected as a decision
    # procedure — the test asserts the sameness, then rejects the detector.
    t1 = time_only_verdict(HISTORIES["H1"](), bound)
    t2 = time_only_verdict(HISTORIES["H2"](), bound)
    if t1 != t2:
        violations.append(
            f"time-only detector distinguished H1 ({t1}) from H2 ({t2}); "
            f"the rejection proof requires it to be indiscriminate")
    if t1 != "BREACH":
        violations.append(
            f"time-only detector says {t1} on H1's 30-unit wall clock; "
            f"the rejection proof requires it to fire")

    # (2) Corrected detector: H1 preserves waiting-authority — no breach,
    # no fairness violation. Liveness never manufactures permission.
    h1 = results["H1"]
    if h1.scheduling_fairness == VIOLATED:
        violations.append("H1: waiting-authority history flagged as fairness violation")
    if h1.bound_kind == SERVICE and h1.eligible_time >= BOUND_LIMIT:
        violations.append("H1: eligible time miscounted; waiting-authority excluded")
    if not any(s.state == WAITING_AUTHORITY for s in HISTORIES["H1"]().segments):
        violations.append("H1: fixture lost its waiting-authority segment")

    # (3) H2: bounded-service breach detected on eligible time.
    h2 = results["H2"]
    if h2.scheduling_fairness != VIOLATED:
        violations.append(f"H2: starved history not flagged; got {h2.scheduling_fairness}")
    if h2.eligible_time != 30:
        violations.append(f"H2: eligible time {h2.eligible_time}, expected 30")

    # (4) H3: safety hold authoritative — zero fairness violations, no
    # breach, safety holds.
    h3 = results["H3"]
    if h3.scheduling_fairness == VIOLATED:
        violations.append("H3: safety-hold control flagged as fairness violation")
    if h3.safety != HOLDS:
        violations.append(f"H3: safety claim {h3.safety}, expected holds")
    if h3.task_completion == VIOLATED:
        violations.append("H3: held obligation failed completion — holds are not failures")

    # (5) H4: verified outage excluded — 29 outage + 1 eligible is not a
    # scheduler failure.
    h4 = results["H4"]
    if h4.eligible_time != 1:
        violations.append(f"H4: eligible time {h4.eligible_time}, expected 1 (outage excluded)")
    if h4.scheduling_fairness == VIOLATED:
        violations.append("H4: outage history flagged as fairness violation")

    # (6) Unenforceable bound: unproven assumption -> UNPROVEN everywhere,
    # never a trusted verdict.
    bad_bound = Bound(kind=SERVICE, limit=BOUND_LIMIT, label="unenforceable",
                      assumptions=(Assumption("unproven capacity claim", False),))
    v = assess(HISTORIES["H2"](), bad_bound, _six_preconditions())
    for slot in ("safety", "scheduling_fairness", "bounded_progress", "task_completion"):
        if getattr(v, slot) != UNPROVEN:
            violations.append(f"unenforceable bound: {slot} = {getattr(v, slot)}, not unproven")
    if v.bound_enforceable:
        violations.append("unenforceable bound reported enforceable")

    # (7) Missing precondition -> UNPROVEN, never failed, never passed.
    missing_pre = tuple(
        Precondition(p.name, False) if p.name == "capacity_assumptions" else p
        for p in _six_preconditions())
    v2 = assess(HISTORIES["H2"](), _service_bound(), missing_pre)
    if v2.scheduling_fairness != UNPROVEN:
        violations.append("missing precondition did not yield UNPROVEN")

    # (8) Heartbeats are not progress; dispatch without evidence is not
    # service (H2's fixture carries both frauds).
    if _has_genuine_progress(HISTORIES["H2"]()):
        violations.append("H2: heartbeats counted as genuine progress")
    if _has_usable_service(HISTORIES["H2"]()):
        violations.append("H2: evidence-free dispatches counted as usable service")

    return violations


# ---------------------------------------------------------------------------
# Machine-readable output + CLI
# ---------------------------------------------------------------------------

def _jsonable(obj: Any) -> Any:
    if isinstance(obj, BoundedLivenessVerdict):
        return obj.as_dict()
    if isinstance(obj, (EligibilitySegment, ServiceObservation, ProgressMark,
                        Precondition, Assumption, Bound)):
        d = asdict(obj)
        return {k: _jsonable(v) for k, v in d.items()}
    if isinstance(obj, dict):
        return {k: _jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_jsonable(v) for v in obj]
    return obj


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="D56 bounded recovery liveness + AER-LIVE-002")
    ap.add_argument("--run-experiment", action="store_true",
                    help="run AER-LIVE-002 and verify; exit 2 on failure")
    ap.add_argument("--history", choices=["H1", "H2", "H3", "H4"],
                    help="print one history's verdict as JSON")
    ap.add_argument("--verify", action="store_true",
                    help="verify AER-LIVE-002 and print violations")
    args = ap.parse_args(argv)

    if args.history:
        print(json.dumps(_jsonable(run_history(args.history)), indent=2))
        return 0

    results = run_aer_live_002()
    violations = verify_aer_live_002(results)

    if args.verify or args.run_experiment:
        payload = {
            "experiment": "AER-LIVE-002",
            "directive": "D56",
            "verdicts": {hid: _jsonable(v) for hid, v in results.items()},
            "violations": violations,
            "pass": not violations,
        }
        print(json.dumps(payload, indent=2))
        return 0 if not violations else 2

    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
