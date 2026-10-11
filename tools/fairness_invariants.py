#!/usr/bin/env python3
"""Fairness invariants + runtime harness — Group 5 (Fairness & Liveness), D58-D65.

This module is the successor to the branch-only fairness_verifier.py (PR #2161):
it keeps the three-property classifier design (WF / SF / progress-on-service)
and D26's four explicit verdict levels, but adds what the D26 audit found
missing:

  GAP-2 (no runtime harness): SchedulerHarness runs REAL scheduler
      implementations against workloads and emits event traces. The
      classifier consumes harness output, not hand-built fixtures.
  GAP-3 (traces, not schedulers): three intentionally BROKEN schedulers with
      injected faults. The acceptance test is: the harness runs each broken
      scheduler and the classifier names the fault correctly.
  GAP-4 (self-reported liveness): TickLedger records scheduler ticks
      independently of the scheduler's self-report; missed ticks are
      missing opportunity (Link 1), not worker failure.
  GAP-5 (collapsed verdicts): every verdict names one of the four levels.
  GAP-6 (merge safety without liveness): MergeLivenessTracker applies the
      three-link standard to PR review lifecycles.

Classifier design credit: Naya 1's verification design via the D26 audit.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

from fairness_eligibility import VERDICT_LEVELS
from fairness_debt import FairnessDebtLedger, DebtWitness

# ---------------------------------------------------------------------------
# Diagnostics and verdict levels (D26: never collapse into one green PASS)
# ---------------------------------------------------------------------------

DIAGNOSTICS = {
    "WF_VIOLATION": "Continuously enabled, never serviced (also violates SF)",
    "SF_ONLY_VIOLATION": "Intermittently enabled, never serviced (WF permits, SF forbids)",
    "PROGRESS_ON_SERVICE_VIOLATION": "Serviced repeatedly, no ranking decrease or terminal disposition",
    "OPPORTUNITY_ASSUMPTION_NOT_MET": "Eligibility never recurs — not a scheduler failure (Link 1 fails)",
    "CORRECT_PROGRESS": "Eligible -> serviced -> ranking decreased or terminal disposition",
    "INSUFFICIENT_DATA": "Not enough observations to classify",
}

# Maps each diagnostic to the D26 verdict level it earns. A classifier verdict
# over harness-generated traces is MODEL_CHECK_PASSED_IN_SCOPE; it becomes
# WORKFLOW_COMPLETED_IN_SCOPE only when the harness ran against the live
# system (harness.run(live=True)), and FAIRNESS_QUALIFIED_WITH_ASSUMPTIONS
# when the trace had missing-evidence windows.
DIAGNOSTIC_LEVELS = {
    "WF_VIOLATION": "MODEL_CHECK_PASSED_IN_SCOPE",
    "SF_ONLY_VIOLATION": "MODEL_CHECK_PASSED_IN_SCOPE",
    "PROGRESS_ON_SERVICE_VIOLATION": "MODEL_CHECK_PASSED_IN_SCOPE",
    "OPPORTUNITY_ASSUMPTION_NOT_MET": "OBSERVED_NO_VIOLATION",
    "CORRECT_PROGRESS": "MODEL_CHECK_PASSED_IN_SCOPE",
    "INSUFFICIENT_DATA": "OBSERVED_NO_VIOLATION",
}


def _multiset_less(after: List, before: List) -> bool:
    """True if `after` is strictly smaller than `before` as multisets.

    Ranking functions map states to multisets of naturals; a strict decrease
    proves progress. Implemented by sorted comparison.
    """
    if len(after) >= len(before):
        return False
    sa, sb = sorted(after), sorted(before)
    return all(a <= b for a, b in zip(sa, sb)) and sa != sb


@dataclass
class Classification:
    diagnostic: str
    explanation: str
    verdict_level: str
    live: bool = False  # True when the trace came from the live system

    def __post_init__(self) -> None:
        if self.diagnostic not in DIAGNOSTICS:
            raise ValueError(f"unknown diagnostic: {self.diagnostic!r}")
        if self.verdict_level not in VERDICT_LEVELS:
            raise ValueError(f"invalid verdict level: {self.verdict_level!r}")


def classify_cycle(cycle_states: List[Dict[str, Any]], live: bool = False) -> Classification:
    """Classify a repeating behavior cycle (lasso) from a scheduler trace.

    Each state: {"enabled": bool, "serviced": bool,
                 "rank_before": [...], "rank_after": [...], "terminal": bool}
    """
    if not cycle_states:
        return Classification("INSUFFICIENT_DATA", "Empty cycle",
                              DIAGNOSTIC_LEVELS["INSUFFICIENT_DATA"], live)
    n = len(cycle_states)
    enabled = sum(1 for s in cycle_states if s.get("enabled"))
    serviced = sum(1 for s in cycle_states if s.get("serviced"))

    progress = False
    for s in cycle_states:
        rb, ra = s.get("rank_before", []), s.get("rank_after", [])
        if ra != rb and _multiset_less(list(ra), list(rb)):
            progress = True
        if s.get("terminal"):
            progress = True

    def lvl(diag: str) -> str:
        base = DIAGNOSTIC_LEVELS[diag]
        # Live traces earn the strongest level for correct progress; violations
        # found live are still model-grade claims about the scheduler (they
        # prove the fault exists, not that every future run fails).
        if live and diag == "CORRECT_PROGRESS":
            return "WORKFLOW_COMPLETED_IN_SCOPE"
        return base

    if enabled == n and serviced == 0:
        d = "WF_VIOLATION"
        return Classification(d, f"Enabled in all {n} states, zero service. {DIAGNOSTICS[d]}", lvl(d), live)
    if 0 < enabled < n and serviced == 0:
        d = "SF_ONLY_VIOLATION"
        return Classification(d, f"Enabled in {enabled}/{n} states (intermittent), zero service. {DIAGNOSTICS[d]}", lvl(d), live)
    if serviced > 0 and not progress:
        d = "PROGRESS_ON_SERVICE_VIOLATION"
        return Classification(d, f"Serviced {serviced}/{n} states, no ranking decrease or terminal state. {DIAGNOSTICS[d]}", lvl(d), live)
    if enabled == 0:
        d = "OPPORTUNITY_ASSUMPTION_NOT_MET"
        return Classification(d, f"Never enabled in {n} states. {DIAGNOSTICS[d]}", lvl(d), live)
    d = "CORRECT_PROGRESS"
    return Classification(d, DIAGNOSTICS[d], lvl(d), live)


# ---------------------------------------------------------------------------
# Runtime harness: real (fault-injectable) schedulers, real traces (GAP-2/3)
# ---------------------------------------------------------------------------

@dataclass
class SchedulerEvent:
    tick: int
    item_id: str
    enabled: bool
    serviced: bool
    rank_before: List[int] = field(default_factory=list)
    rank_after: List[int] = field(default_factory=list)
    terminal: bool = False

    def to_state(self) -> Dict[str, Any]:
        return {"enabled": self.enabled, "serviced": self.serviced,
                "rank_before": self.rank_before, "rank_after": self.rank_after,
                "terminal": self.terminal}


class Scheduler:
    """Base scheduler: decides which enabled item to service each tick."""

    def __init__(self, name: str) -> None:
        self.name = name

    def select(self, tick: int, enabled_items: List[str]) -> Optional[str]:
        """Return the item id to service, or None."""
        raise NotImplementedError


class RoundRobinScheduler(Scheduler):
    """Correct baseline: fair round-robin over enabled items."""

    def __init__(self) -> None:
        super().__init__("round-robin")
        self._cursor = 0

    def select(self, tick: int, enabled_items: List[str]) -> Optional[str]:
        if not enabled_items:
            return None
        choice = enabled_items[self._cursor % len(enabled_items)]
        self._cursor += 1
        return choice


class WeakFairnessBreakingScheduler(Scheduler):
    """FAULT: starves one continuously-enabled item forever (breaks WF)."""

    def __init__(self, victim: str) -> None:
        super().__init__(f"wf-breaker(victim={victim})")
        self.victim = victim

    def select(self, tick: int, enabled_items: List[str]) -> Optional[str]:
        others = [i for i in enabled_items if i != self.victim]
        return others[0] if others else None


class StrongFairnessBreakingScheduler(Scheduler):
    """FAULT: serves continuously-enabled items but starves an
    intermittently-enabled one (breaks SF only; WF permits this)."""

    def __init__(self, victim: str) -> None:
        super().__init__(f"sf-breaker(victim={victim})")
        self.victim = victim

    def select(self, tick: int, enabled_items: List[str]) -> Optional[str]:
        others = [i for i in enabled_items if i != self.victim]
        return others[0] if others else None


class NoProgressScheduler(Scheduler):
    """FAULT: fair service, but the worker never decreases the ranking
    (breaks progress-on-service; scheduler fairness holds)."""

    def __init__(self) -> None:
        super().__init__("no-progress")
        self._cursor = 0

    def select(self, tick: int, enabled_items: List[str]) -> Optional[str]:
        if not enabled_items:
            return None
        choice = enabled_items[self._cursor % len(enabled_items)]
        self._cursor += 1
        return choice  # fair selection; the WORKER is broken, not the choice


@dataclass
class WorkloadItem:
    item_id: str
    # enabled_at(tick) -> bool. Intermittent items return True on some ticks.
    enabled_at: Any  # Callable[[int], bool]
    initial_rank: List[int] = field(default_factory=lambda: [3, 2, 1])
    makes_progress: bool = True  # False => worker never decreases rank


class SchedulerHarness:
    """Runs a REAL scheduler against a workload and emits the event trace.

    This is the runtime harness GAP-2 demanded: the classifier consumes
    harness output, not hand-built fixtures. A broken scheduler's BEHAVIOR
    is observed; nothing is pre-labeled.
    """

    def __init__(self, debt_base_bound: int = 3) -> None:
        self.debt_base_bound = debt_base_bound

    def run(
        self,
        scheduler: Scheduler,
        workload: List[WorkloadItem],
        ticks: int,
        live: bool = False,
    ) -> Dict[str, Any]:
        events: List[SchedulerEvent] = []
        ledger = FairnessDebtLedger(base_bound=self.debt_base_bound)
        ranks: Dict[str, List[int]] = {w.item_id: list(w.initial_rank) for w in workload}
        done: Set[str] = set()

        for tick in range(ticks):
            window_id = f"tick-{tick}"
            enabled = [w.item_id for w in workload
                       if w.item_id not in done and w.enabled_at(tick)]
            chosen = scheduler.select(tick, enabled)
            serviced = {chosen} if chosen else set()
            ledger.record_window(window_id, set(enabled), serviced,
                                 evidence_present=True)
            for w in workload:
                if w.item_id in done:
                    continue
                is_enabled = w.item_id in enabled
                is_serviced = w.item_id in serviced
                rb = list(ranks[w.item_id])
                ra = list(rb)
                terminal = False
                if is_serviced:
                    if w.makes_progress and len(ra) > 0:
                        ra = ra[1:]  # ranking strictly decreases
                    if len(ra) == 0:
                        terminal = True
                        done.add(w.item_id)
                    ranks[w.item_id] = ra
                events.append(SchedulerEvent(
                    tick=tick, item_id=w.item_id, enabled=is_enabled,
                    serviced=is_serviced, rank_before=rb, rank_after=ra,
                    terminal=terminal))

        return {
            "scheduler": scheduler.name,
            "ticks": ticks,
            "events": events,
            "ledger": ledger,
            "live": live,
        }

    def classify_item(self, result: Dict[str, Any], item_id: str) -> Classification:
        """Classify one item's behavior cycle from harness output."""
        states = [e.to_state() for e in result["events"] if e.item_id == item_id]
        return classify_cycle(states, live=result["live"])


# ---------------------------------------------------------------------------
# Full-state invariants
# ---------------------------------------------------------------------------

@dataclass
class InvariantViolation:
    kind: str  # STARVATION | DEPENDENCY_ORDER | DEADLOCK_CYCLE
    detail: str
    witness: Dict[str, Any]
    verdict_level: str = "MODEL_CHECK_PASSED_IN_SCOPE"

    def __post_init__(self) -> None:
        if self.verdict_level not in VERDICT_LEVELS:
            raise ValueError(f"invalid verdict level: {self.verdict_level!r}")


class InvariantChecker:
    """Full-state invariant verification over a system snapshot.

    Snapshot shape:
      {
        "debt_ledger": FairnessDebtLedger,
        "dependencies": {item_id: [dep ids that must resolve first]},
        "resolved": set(item ids with terminal disposition),
        "serviced_before_resolved": [(item, dep)]  # observed order violations
      }
    """

    def check(self, snapshot: Dict[str, Any]) -> List[InvariantViolation]:
        violations: List[InvariantViolation] = []
        violations.extend(self._check_starvation(snapshot))
        violations.extend(self._check_dependency_order(snapshot))
        violations.extend(self._check_deadlock_cycles(snapshot))
        return violations

    def _check_starvation(self, snapshot: Dict[str, Any]) -> List[InvariantViolation]:
        ledger: Optional[FairnessDebtLedger] = snapshot.get("debt_ledger")
        if ledger is None:
            return []
        out = []
        for witness in ledger.violations():
            out.append(InvariantViolation(
                kind="STARVATION",
                detail=witness.describe(),
                witness={"debt_witness": witness.__dict__},
            ))
        return out

    def _check_dependency_order(self, snapshot: Dict[str, Any]) -> List[InvariantViolation]:
        deps: Dict[str, List[str]] = snapshot.get("dependencies", {})
        resolved: Set[str] = set(snapshot.get("resolved", set()))
        serviced: Set[str] = set(snapshot.get("serviced", set()))
        out = []
        for item, dep_list in deps.items():
            if item in serviced:
                for dep in dep_list:
                    if dep not in resolved:
                        out.append(InvariantViolation(
                            kind="DEPENDENCY_ORDER",
                            detail=(f"Item {item!r} was serviced before dependency "
                                    f"{dep!r} reached terminal disposition."),
                            witness={"item": item, "unresolved_dep": dep},
                        ))
        return out

    def _check_deadlock_cycles(self, snapshot: Dict[str, Any]) -> List[InvariantViolation]:
        """Detect dependency cycles where every member waits on another member.

        A cycle is only a deadlock if no member can make progress: every
        member must be unserviced and unresolved. A cycle with an
        in-progress member is a warning-free ordering constraint.
        """
        deps: Dict[str, List[str]] = snapshot.get("dependencies", {})
        resolved: Set[str] = set(snapshot.get("resolved", set()))
        serviced: Set[str] = set(snapshot.get("serviced", set()))
        waiting: Set[str] = set(snapshot.get("waiting", set()))

        # Find cycles via DFS.
        cycles: List[List[str]] = []
        visited: Set[str] = set()
        stack: List[str] = []

        def dfs(node: str) -> None:
            if node in stack:
                cycles.append(stack[stack.index(node):] + [node])
                return
            if node in visited:
                return
            visited.add(node)
            stack.append(node)
            for dep in deps.get(node, []):
                dfs(dep)
            stack.pop()

        for node in deps:
            dfs(node)

        out = []
        for cycle in cycles:
            members = set(cycle)
            # Deadlock: every member waits, none serviced, none resolved.
            if (members <= waiting
                    and not (members & serviced)
                    and not (members & resolved)):
                out.append(InvariantViolation(
                    kind="DEADLOCK_CYCLE",
                    detail=(f"Deadlock cycle: {cycle}. Every member waits on "
                            f"another member; none serviced, none resolved."),
                    witness={"cycle": cycle},
                ))
        return out


# ---------------------------------------------------------------------------
# Tick ledger — independent liveness observation (GAP-4)
# ---------------------------------------------------------------------------

@dataclass
class TickRecord:
    tick_id: str
    scheduled_at: str  # ISO timestamp the tick was EXPECTED
    observed_at: Optional[str]  # ISO timestamp the tick was OBSERVED, None = missed
    worker_id: str


class TickLedger:
    """Independent record of scheduler ticks.

    The ledger is written by an OBSERVER, not by the worker itself. A tick
    the worker claims but the observer never saw is a missing opportunity
    (D26 Link 1 fails) — it is never counted as worker progress.
    """

    def __init__(self) -> None:
        self._records: List[TickRecord] = []

    def expect(self, tick_id: str, scheduled_at: str, worker_id: str) -> None:
        self._records.append(TickRecord(tick_id, scheduled_at, None, worker_id))

    def observe(self, tick_id: str, observed_at: str) -> bool:
        for r in self._records:
            if r.tick_id == tick_id and r.observed_at is None:
                r.observed_at = observed_at
                return True
        return False

    def missed_ticks(self) -> List[TickRecord]:
        return [r for r in self._records if r.observed_at is None]

    def observed_ticks(self) -> List[TickRecord]:
        return [r for r in self._records if r.observed_at is not None]

    def liveness_report(self) -> Dict[str, Any]:
        missed = self.missed_ticks()
        # A missed tick is Link-1 failure (no opportunity), NOT a worker fault.
        # Verdict level is OBSERVED_NO_VIOLATION when nothing missed (weakest
        # honest claim: we watched and saw the ticks happen).
        return {
            "total_expected": len(self._records),
            "observed": len(self._records) - len(missed),
            "missed": [{"tick_id": r.tick_id, "worker_id": r.worker_id,
                        "scheduled_at": r.scheduled_at} for r in missed],
            "all_ticks_observed": len(missed) == 0,
            "verdict_level": ("OBSERVED_NO_VIOLATION" if not missed
                              else "FAIRNESS_QUALIFIED_WITH_ASSUMPTIONS"),
            "note": ("Missed ticks are missing opportunity (Link 1), "
                     "never worker failure.") if missed else "",
        }


# ---------------------------------------------------------------------------
# Live trace reader — traces from the running system, not fixtures (GAP-2)
# ---------------------------------------------------------------------------

class LiveTraceReader:
    """Reads scheduler event traces from a JSONL log (the live system).

    Each line: {"tick": int, "item_id": str, "enabled": bool, "serviced": bool,
                "rank_before": [...], "rank_after": [...], "terminal": bool,
                "evidence_present": bool}
    Lines missing "evidence_present" are treated as evidence_present=True
    only when they carry all required fields; otherwise the window is
    flagged missing-evidence and the debt bound widens (never a silent PASS).
    """

    REQUIRED_FIELDS = ("tick", "item_id", "enabled", "serviced")

    def read(self, path: str) -> Dict[str, Any]:
        events: List[SchedulerEvent] = []
        missing_evidence_windows: Set[str] = set()
        with open(path, "r", encoding="utf-8") as f:
            for lineno, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError as e:
                    raise ValueError(f"{path}:{lineno}: invalid JSON: {e}")
                window_id = f"tick-{obj.get('tick', f'line-{lineno}')}"
                if not all(k in obj for k in self.REQUIRED_FIELDS):
                    missing_evidence_windows.add(window_id)
                    continue
                events.append(SchedulerEvent(
                    tick=int(obj["tick"]), item_id=str(obj["item_id"]),
                    enabled=bool(obj["enabled"]), serviced=bool(obj["serviced"]),
                    rank_before=list(obj.get("rank_before", [])),
                    rank_after=list(obj.get("rank_after", [])),
                    terminal=bool(obj.get("terminal", False))))
                if obj.get("evidence_present") is False:
                    missing_evidence_windows.add(window_id)
        return {"events": events,
                "missing_evidence_windows": sorted(missing_evidence_windows),
                "live": True}

    def to_cycle_states(self, trace: Dict[str, Any], item_id: str) -> List[Dict[str, Any]]:
        return [e.to_state() for e in trace["events"] if e.item_id == item_id]


# ---------------------------------------------------------------------------
# Merge liveness tracker — three links on the PR review pipeline (GAP-6)
# ---------------------------------------------------------------------------

@dataclass
class PRRecord:
    pr_number: int
    review_requested_at: Optional[str]  # Link 1: opportunity exists?
    first_review_at: Optional[str]      # Link 2: fair service?
    resolved_at: Optional[str]         # Link 3: merged or closed?
    resolution: Optional[str] = None   # "merged" | "closed" | None


@dataclass
class MergeLivenessVerdict:
    pr_number: int
    link1_opportunity: bool
    link2_fair_service: bool
    link3_progress: bool
    starved: bool
    starvation_witness: Optional[Dict[str, Any]]
    verdict_level: str

    def __post_init__(self) -> None:
        if self.verdict_level not in VERDICT_LEVELS:
            raise ValueError(f"invalid verdict level: {self.verdict_level!r}")


class MergeLivenessTracker:
    """Applies D26's three links to PR review lifecycles.

    The merge gate proves SAFETY (bad merges blocked). This tracker proves
    LIVENESS: reviews are requested (Link 1), no PR starves (Link 2), PRs
    reach resolution (Link 3). A PR can be protocol-compliant and stalled
    forever; this tracker names the stall.
    """

    def __init__(self, starvation_bound_hours: float = 72.0) -> None:
        self.starvation_bound_hours = starvation_bound_hours

    @staticmethod
    def _hours_between(start_iso: str, end_iso: str) -> float:
        from datetime import datetime
        a = datetime.fromisoformat(start_iso.replace("Z", "+00:00"))
        b = datetime.fromisoformat(end_iso.replace("Z", "+00:00"))
        return (b - a).total_seconds() / 3600.0

    def check(self, pr: PRRecord, now_iso: str) -> MergeLivenessVerdict:
        link1 = pr.review_requested_at is not None
        link2 = link1 and pr.first_review_at is not None
        link3 = pr.resolved_at is not None and pr.resolution in ("merged", "closed")

        starved = False
        witness = None
        if link1 and not link2:
            waited = self._hours_between(pr.review_requested_at, now_iso)
            if waited > self.starvation_bound_hours:
                starved = True
                witness = {"pr": pr.pr_number, "waited_hours": round(waited, 1),
                           "bound_hours": self.starvation_bound_hours,
                           "phase": "review-starved"}

        if not link1:
            level = "OBSERVED_NO_VIOLATION"  # nothing to check yet
        elif starved:
            level = "MODEL_CHECK_PASSED_IN_SCOPE"
        elif link3:
            level = "WORKFLOW_COMPLETED_IN_SCOPE"
        elif link2:
            level = "FAIRNESS_QUALIFIED_WITH_ASSUMPTIONS"
        else:
            level = "OBSERVED_NO_VIOLATION"

        return MergeLivenessVerdict(
            pr_number=pr.pr_number, link1_opportunity=link1,
            link2_fair_service=link2, link3_progress=link3,
            starved=starved, starvation_witness=witness, verdict_level=level)
