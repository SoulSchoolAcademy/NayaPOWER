#!/usr/bin/env python3
"""Merge-queue fairness wiring — Naya 2 WIRE LANE, Group 5 (Fairness & Liveness), D58-D65.

D26's three-link standard wired to the team's REAL scheduling path: the merge
queue. The merge-consensus gate (tools/check_merge_consensus.py) answers
"may this PR merge NOW?" (safety). This module answers the question no
existing tool asks: "is eligible work being SERVED fairly over time — is
anything starving?" (liveness). No duplicate mechanism: consensus is per-PR
readiness; this is queue-wide fairness debt.

How it works
------------
Each queued PR becomes a fairness WorkItem. The five merge-readiness
requirements mirror the standing merge protocol (mission state #2154:
"scorecard >= 9.0 + independent validation + #2154 intent + no objection")
and reuse the evidence conventions of check_merge_consensus.py:

  1. scorecard_receipt_on_head -- a `## SCORECARD` comment naming the PR's
     exact head SHA, from a named seat other than the author.
  2. scorecard_meets_floor     -- that receipt's verdict >= 9.0
     (or merge: APPROVED with no numeric verdict).
  3. cross_seat_review         -- a `[NAYA M . REVIEW] ... APPROVED` comment
     naming the exact head, reviewer seat != author seat.
  4. checks_green_on_head      -- no failing completed check runs on the head
     SHA, except checks named in evidence['known_red_checks'] (each with a
     documented reason, e.g. the receipt-gate depth-1 bug #2188 fixes).
  5. merge_intent_recorded     -- the PR number appears in #2154's merge queue.

Every predicate reads ONLY the evidence bundle -- never the scheduler's claim
(labels, "ready" assertions). The EligibilityProver independently re-evaluates;
a contradiction between claim and evidence is named, never trusted.

Debt: for each complete 24h window since ready_since (the latest timestamp at
which all five requirements became simultaneously satisfied, each timestamp
from evidence), an eligible-but-unmerged PR accrues 1 debt. Debt > bound (3
windows = 72h) produces a falsifiable DebtWitness naming the PR, the windows,
the debt and the bound. Missing evidence widens the bound (documented rule)
instead of manufacturing a violation: unknown is unknown, not a PASS and not
a violation.

Legitimate non-service is not starvation:
  - blocked_by: PRs queued behind another queue item (e.g. #2201 behind #2188)
    accrue no debt; the deferral is named as an assumption.
  - parked: items awaiting Shawn's word (human gate) accrue no debt; named.
  - ineligible items (scorecard < 9.0, red checks, no intent) accrue no debt:
    correctly unserved is not starvation.

CLI:
    python3 tools/merge_queue_fairness.py --queue queue.json [--bound 3]
        [--window-hours 24] [--now ISO-8601] [--json]

Exit 0: no fairness violation. Exit 1: violation -- witnesses printed.
Exit 2: scanner error (fail closed -- never silent green).

Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from fairness_eligibility import (
    EligibilityProver,
    PredicateRegistry,
    WorkItem,
    VERDICT_LEVELS,
)
from fairness_debt import FairnessDebtLedger, DebtWitness

# The five merge-readiness requirements. ALL must hold for eligibility.
MERGE_QUEUE_REQUIREMENTS = (
    "scorecard_receipt_on_head",
    "scorecard_meets_floor",
    "cross_seat_review",
    "checks_green_on_head",
    "merge_intent_recorded",
)

SCORECARD_FLOOR = 9.0
BASE_BOUND_WINDOWS = 3
WINDOW_HOURS = 24

# Check-run conclusions that count as failing. 'skipped'/'neutral'/'success'
# are fine; anything still running means the evidence is incomplete.
FAILING_CONCLUSIONS = {"failure", "timed_out", "cancelled", "action_required", "stale"}


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _parse_iso(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


# ---------------------------------------------------------------------------
# Requirement predicates. Each: (evidence) -> (satisfied, detail).
# Predicates receive ONLY the evidence bundle -- never scheduler claims.
# ---------------------------------------------------------------------------

def _pred_scorecard_receipt_on_head(evidence: Dict[str, Any]) -> tuple:
    sc = evidence.get("scorecard") or {}
    head = evidence.get("head_sha", "")
    seat = sc.get("seat")
    author = evidence.get("author_seat")
    head_matches = bool(sc.get("head_matches"))
    seat_ok = bool(seat) and (author is None or seat != author)
    ok = head_matches and seat_ok
    return ok, (
        f"scorecard seat={seat!r} author={author!r} head_matches={head_matches} "
        f"head={head[:12]}"
    )


def _pred_scorecard_meets_floor(evidence: Dict[str, Any]) -> tuple:
    sc = evidence.get("scorecard") or {}
    verdict = sc.get("verdict")
    merge_approved = bool(sc.get("merge_approved"))
    if verdict is None:
        ok = merge_approved
        return ok, f"no numeric verdict; merge_approved={merge_approved}"
    try:
        score = float(verdict)
    except (TypeError, ValueError):
        return False, f"verdict {verdict!r} not numeric -- fail closed"
    ok = score >= SCORECARD_FLOOR
    return ok, f"verdict={score} floor={SCORECARD_FLOOR}"


def _pred_cross_seat_review(evidence: Dict[str, Any]) -> tuple:
    rv = evidence.get("review") or {}
    author = evidence.get("author_seat")
    seat = rv.get("seat")
    head_matches = bool(rv.get("head_matches"))
    seat_ok = bool(seat) and (author is None or seat != author)
    ok = head_matches and seat_ok
    return ok, (
        f"review seat={seat!r} author={author!r} head_matches={head_matches}"
    )


def _pred_checks_green_on_head(evidence: Dict[str, Any]) -> tuple:
    if not evidence.get("checks_evidence_present"):
        return False, "check-run evidence missing -- fail closed"
    runs = evidence.get("check_runs") or []
    known_red = evidence.get("known_red_checks") or {}
    if not runs:
        return False, "no check runs found for head -- fail closed"
    # GitHub semantics: the LATEST run per check name is the verdict.
    # A re-run that succeeds supersedes an earlier failure; stale runs
    # must not condemn the head. (Found live on #2188/#2201: old failing
    # runs alongside newer successful ones.)
    latest: Dict[str, Dict[str, Any]] = {}
    for r in runs:
        name = r.get("name") or "<unnamed>"
        prev = latest.get(name)
        key = r.get("completed_at") or r.get("started_at") or ""
        prev_key = (prev.get("completed_at") or prev.get("started_at") or "") if prev else ""
        if prev is None or key >= prev_key:
            latest[name] = r
    incomplete = [n for n, r in latest.items() if r.get("status") != "completed"]
    if incomplete:
        return False, f"checks still running: {incomplete[:5]} -- not ready"
    failing = [
        n for n, r in latest.items()
        if r.get("conclusion") in FAILING_CONCLUSIONS and n not in known_red
    ]
    if failing:
        return False, f"failing checks on head (latest runs): {failing[:8]}"
    excused = [n for n in known_red if n in latest]
    return True, (
        f"{len(latest)} checks (latest runs), 0 failing "
        f"({len(excused)} documented known-red excused)"
    )


def _pred_merge_intent_recorded(evidence: Dict[str, Any]) -> tuple:
    ok = bool(evidence.get("intent_recorded"))
    return ok, f"intent_recorded={ok} (mission state #2154 merge queue)"


def merge_queue_registry() -> PredicateRegistry:
    reg = PredicateRegistry()
    reg.register("scorecard_receipt_on_head", _pred_scorecard_receipt_on_head)
    reg.register("scorecard_meets_floor", _pred_scorecard_meets_floor)
    reg.register("cross_seat_review", _pred_cross_seat_review)
    reg.register("checks_green_on_head", _pred_checks_green_on_head)
    reg.register("merge_intent_recorded", _pred_merge_intent_recorded)
    return reg


# ---------------------------------------------------------------------------
# Queue item -> WorkItem + evidence bundle
# ---------------------------------------------------------------------------

@dataclass
class QueueVerdict:
    pr_number: int
    eligible: bool
    missing: List[str]
    claim_contradicted: bool
    ready_since: Optional[str]
    debt: int
    bound: int
    widenings: int
    violated: bool
    witness: Optional[DebtWitness]
    deferred_reason: Optional[str]  # blocked_by / parked -- legitimate non-service
    assumptions: List[str] = field(default_factory=list)
    verdict_level: str = "MODEL_CHECK_PASSED_IN_SCOPE"

    def __post_init__(self) -> None:
        if self.verdict_level not in VERDICT_LEVELS:
            raise ValueError(f"invalid verdict level: {self.verdict_level!r}")


def _ready_since(evidence: Dict[str, Any]) -> Optional[str]:
    """Latest timestamp at which all requirements became satisfied.

    Each timestamp comes from evidence (comment created_at, check completed_at).
    Intent is a standing record, not an event, so it does not move ready_since.
    Returns None when any required timestamp is unprovable -- the caller then
    treats the item as missing-evidence (bound widened, no debt accrued).
    """
    stamps: List[str] = []
    sc = evidence.get("scorecard") or {}
    rv = evidence.get("review") or {}
    if sc.get("at"):
        stamps.append(sc["at"])
    if rv.get("at"):
        stamps.append(rv["at"])
    runs = evidence.get("check_runs") or []
    completed = [r.get("completed_at") for r in runs if r.get("completed_at")]
    if completed:
        stamps.append(max(completed))
    if not stamps:
        return None
    # All three temporal evidences must exist for a provable ready_since.
    if not (sc.get("at") and rv.get("at") and completed):
        return None
    return max(stamps)


def _complete_windows_since(ready_since: str, now: datetime,
                            window_hours: int) -> int:
    """Number of COMPLETE windows elapsed since ready_since.

    The partial current window never accrues: a false starvation alarm is
    worse than a late one.
    """
    start = _parse_iso(ready_since)
    elapsed = (now - start).total_seconds() / 3600.0
    if elapsed < 0:
        return 0
    return int(elapsed // window_hours)


def scan_queue(queue: Dict[str, Any], bound: int = BASE_BOUND_WINDOWS,
               window_hours: int = WINDOW_HOURS,
               now: Optional[datetime] = None) -> List[QueueVerdict]:
    """Run the fairness gate over a merge-queue snapshot.

    Uses the REAL EligibilityProver and FairnessDebtLedger -- this is the
    wiring, not a reimplementation.
    """
    now = now or datetime.now(timezone.utc)
    registry = merge_queue_registry()
    prover = EligibilityProver(registry)
    verdicts: List[QueueVerdict] = []

    for item in queue.get("queue", []):
        pr = item["pr_number"]
        evidence = dict(item.get("evidence") or {})
        # The evidence bundle is primary; item-level fields are defaults.
        # (setdefault: never let a default stomp gathered evidence.)
        evidence.setdefault("pr_number", pr)
        evidence.setdefault("head_sha", item.get("head_sha", ""))
        evidence.setdefault("author_seat", item.get("author_seat"))
        evidence.setdefault("intent_recorded", item.get("intent_recorded", False))
        evidence.setdefault("blocked_by", item.get("blocked_by", []))
        evidence.setdefault("known_red_checks", item.get("known_red_checks", {}))

        work = WorkItem(
            item_id=f"PR-{pr}",
            requirements=list(MERGE_QUEUE_REQUIREMENTS),
            scheduler_claim=item.get("scheduler_claim"),  # untrusted, recorded only
            metadata={"pr_number": pr, "head_sha": evidence["head_sha"]},
        )
        assumptions: List[str] = list(item.get("assumptions", []))
        if evidence["author_seat"] is None:
            assumptions.append(
                "author seat not declared (no 'Seat: Naya N' in PR body and "
                "no nayaN/ branch prefix); cross-seat predicates accept any "
                "named reviewer seat"
            )

        window_id = f"scan-{now.strftime('%Y%m%dT%H%M%SZ')}"
        elig = prover.prove(work, evidence, window_id,
                            assumptions=assumptions or None)

        deferred: Optional[str] = None
        if item.get("blocked_by"):
            deferred = f"service deferred: blocked by {item['blocked_by']}"
            assumptions.append(deferred + " -- legitimate queue ordering, not starvation")
        parked = item.get("parked")
        if parked:
            reason = parked.get("reason") if isinstance(parked, dict) else str(parked)
            deferred = f"service deferred: parked -- {reason}"
            assumptions.append(deferred)

        ready = _ready_since(evidence) if elig.eligible else None
        ledger = FairnessDebtLedger(base_bound=bound)
        widened = False
        if elig.eligible and not deferred:
            if ready is None:
                # Missing evidence: widen the bound, accrue nothing.
                # Unknown is unknown -- not a violation.
                ledger.record_window(f"{window_id}-evidence-gap",
                                     eligible={work.item_id}, serviced=set(),
                                     evidence_present=False)
                widened = True
                assumptions.append(
                    "ready_since unprovable from evidence timestamps; "
                    "bound widened per missing-evidence rule, no debt accrued"
                )
            else:
                n_windows = _complete_windows_since(ready, now, window_hours)
                base = _parse_iso(ready)
                for w in range(n_windows):
                    ws = base + timedelta(hours=window_hours * w)
                    we = ws + timedelta(hours=window_hours)
                    ledger.record_window(
                        f"{ws.strftime('%Y%m%dT%H%MZ')}-{we.strftime('%Y%m%dT%H%MZ')}",
                        eligible={work.item_id}, serviced=set(),
                        evidence_present=True)

        status = ledger.check(work.item_id)
        level = elig.verdict_level
        if widened or status.widenings > 0:
            level = "FAIRNESS_QUALIFIED_WITH_ASSUMPTIONS"

        verdicts.append(QueueVerdict(
            pr_number=pr,
            eligible=elig.eligible,
            missing=list(elig.missing),
            claim_contradicted=elig.claim_contradicted,
            ready_since=ready,
            debt=status.debt,
            bound=status.bound,
            widenings=status.widenings,
            violated=status.violated,
            witness=status.witness,
            deferred_reason=deferred,
            assumptions=assumptions,
            verdict_level=level,
        ))
    return verdicts


def verdict_to_dict(v: QueueVerdict) -> Dict[str, Any]:
    d = {
        "pr_number": v.pr_number,
        "eligible": v.eligible,
        "missing_requirements": v.missing,
        "claim_contradicted": v.claim_contradicted,
        "ready_since": v.ready_since,
        "debt_windows": v.debt,
        "bound_windows": v.bound,
        "missing_evidence_widenings": v.widenings,
        "violated": v.violated,
        "deferred_reason": v.deferred_reason,
        "assumptions": v.assumptions,
        "verdict_level": v.verdict_level,
    }
    if v.witness:
        d["witness"] = {
            "item_id": v.witness.item_id,
            "window_start": v.witness.window_start,
            "window_end": v.witness.window_end,
            "debt": v.witness.debt,
            "bound": v.witness.bound,
            "widenings": v.witness.widenings,
            "description": v.witness.describe(),
        }
    return d


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description="Merge-queue fairness scan: D26 wired to the real merge queue.")
    ap.add_argument("--queue", required=True, help="queue snapshot JSON path")
    ap.add_argument("--bound", type=int, default=BASE_BOUND_WINDOWS,
                    help="base bound in windows (default 3)")
    ap.add_argument("--window-hours", type=int, default=WINDOW_HOURS,
                    help="window length in hours (default 24)")
    ap.add_argument("--now", default=None,
                    help="ISO-8601 now override (default: current UTC)")
    ap.add_argument("--json", action="store_true",
                    help="print machine-readable verdict JSON")
    args = ap.parse_args(argv)

    try:
        with open(args.queue) as f:
            queue = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"SCAN ERROR: cannot read queue snapshot: {e}", file=sys.stderr)
        return 2
    if args.bound < 1 or args.window_hours < 1:
        print("SCAN ERROR: --bound and --window-hours must be >= 1", file=sys.stderr)
        return 2
    try:
        now = _parse_iso(args.now) if args.now else datetime.now(timezone.utc)
    except ValueError as e:
        print(f"SCAN ERROR: bad --now: {e}", file=sys.stderr)
        return 2

    try:
        verdicts = scan_queue(queue, bound=args.bound,
                              window_hours=args.window_hours, now=now)
    except Exception as e:  # fail closed -- never silent green
        print(f"SCAN ERROR: {type(e).__name__}: {e}", file=sys.stderr)
        return 2

    out = {
        "scanned_at": _iso_now(),
        "queue_ref": queue.get("mission_state_ref"),
        "bound_windows": args.bound,
        "window_hours": args.window_hours,
        "verdicts": [verdict_to_dict(v) for v in verdicts],
    }
    violations = [v for v in verdicts if v.violated]

    if args.json:
        print(json.dumps(out, indent=2))
    else:
        print(f"Merge-queue fairness scan: {len(verdicts)} items, "
              f"{len(violations)} violations (bound={args.bound} windows "
              f"x {args.window_hours}h)")
        for v in verdicts:
            state = "VIOLATION" if v.violated else (
                "eligible" if v.eligible else "ineligible")
            extra = f" debt={v.debt}/{v.bound}"
            if v.deferred_reason:
                extra += f" [{v.deferred_reason}]"
            if v.missing:
                extra += f" missing={v.missing}"
            print(f"  PR-{v.pr_number}: {state}{extra} [{v.verdict_level}]")
            for a in v.assumptions:
                print(f"    assumption: {a}")
            if v.witness:
                print(f"    WITNESS: {v.witness.describe()}")

    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
