"""Kernel VERIFY seam: consume ActionReceipts and close them with verdicts.

Closes the ACT -> VERIFY loop left open by kernel/act_pipeline.py, where
EXECUTION_COMPLETED receipts sit at truth_state UNKNOWN until an
independent verifier closes them via apply_verify_verdict.

This module is the consumer-side machinery. It does NOT judge outcomes
itself — the injected verifier does that (VERIFY node contract: never
collapse verification into execution). The seam enforces the contract's
invariants as fail-closed machinery:

- Only EXECUTION_COMPLETED receipts are eligible. Anything else is
  skipped and named, never silently dropped.
- Expected outcome undefined -> NOT_PROVEN (verifier not consulted).
- Observed outcome missing -> NOT_PROVEN (verifier not consulted —
  there is nothing to judge against).
- A verdict with no evidence is refused: no acceptance without evidence.
- Verdict pairs must be coherent: (True, ACCEPTED), (False, REJECTED),
  (False, PENDING). Incoherence is refused, not coerced.
- PENDING (inconclusive) never closes a receipt: inconclusive is neither
  success nor failure. The gap is recorded; the receipt stays UNKNOWN
  so a later verdict can still close it.
- Every verdict is bound to a verifier identity. Structural machine
  closures are bound to the seam itself — no anonymous verdicts.
- Close is idempotent-guarded: a receipt closes once. A second verdict
  on the same receipt_id fails loudly (ReceiptAlreadyClosed).

apply_verify_verdict remains the single writer of outcome_verified=True.
"""
from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable

from kernel import act_pipeline as ap

# Acceptance decisions (VERIFY node contract V1).
ACCEPTED = "ACCEPTED"
REJECTED = "REJECTED"
PENDING = "PENDING"

# Machine failure codes for structural closures.
EXPECTED_OUTCOME_UNDEFINED = "EXPECTED_OUTCOME_UNDEFINED"
OBSERVATION_MISSING = "OBSERVATION_MISSING"

# Skip / refusal reasons.
NOT_ELIGIBLE = "NOT_ELIGIBLE"
ALREADY_CLOSED = "ALREADY_CLOSED"

_SEAM_VERIFIER_ID = "verify-seam"


class VerdictRefused(Exception):
    """The seam refused to apply a verdict — fail closed, receipt untouched."""


class ReceiptAlreadyClosed(Exception):
    """A verdict was attempted on an already-closed receipt_id."""


class LogFull(Exception):
    """VerdictLog reached its bound — fail loud, never silently drop."""


@dataclass(frozen=True)
class Verdict:
    """A verifier's judgment on one receipt. Produced by the injected
    verifier, never by the seam itself."""
    verified: bool
    acceptance: str  # ACCEPTED | REJECTED | PENDING
    evidence: str


@dataclass(frozen=True)
class VerdictRecord:
    receipt_id: str
    plan_id: str
    verifier_id: str
    verified: bool
    acceptance: str
    evidence: str
    verdict_at: float
    codes: tuple = ()


@dataclass(frozen=True)
class CloseResult:
    closed: tuple      # ActionReceipt — verdict applied, truth_state settled
    records: tuple     # VerdictRecord — one per judgment, including PENDING gaps
    skipped: tuple     # (receipt_id, reason) — named, never silent


class VerdictLog:
    """Append-only, bounded consumer-side record of verdicts."""

    def __init__(self, max_entries: int = 10_000):
        if max_entries < 1:
            raise ValueError("max_entries must be >= 1")
        self._max = max_entries
        self._records: list[VerdictRecord] = []

    def append(self, record: VerdictRecord) -> None:
        if len(self._records) >= self._max:
            raise LogFull(f"verdict log bound reached ({self._max}); refusing silent drop")
        self._records.append(record)

    def records(self) -> tuple:
        return tuple(self._records)

    def closed_receipt_ids(self) -> frozenset:
        return frozenset(r.receipt_id for r in self._records
                         if r.acceptance in (ACCEPTED, REJECTED))


def _coherent(verdict: Verdict) -> bool:
    return ((verdict.verified and verdict.acceptance == ACCEPTED)
            or (not verdict.verified and verdict.acceptance in (REJECTED, PENDING)))


def close_receipts(receipts,
                   *,
                   verifier_id: str,
                   verdict_fn: Callable[[ap.ActionReceipt], Verdict],
                   now: float | None = None,
                   log: VerdictLog | None = None) -> CloseResult:
    """Close eligible receipts with independent verdicts.

    receipts: ActionReceipts to consider (e.g. a ReceiptLedger's entries).
    verifier_id: named identity bound to every judgment — required.
    verdict_fn: the independent verifier; receives a receipt, returns a
        Verdict. The seam never calls it when structural checks already
        decide the outcome.
    now: epoch seconds for verdict timestamps (defaults to time.time()).
    log: optional VerdictLog; records are still returned in the result.

    Raises VerdictRefused on missing identity, empty evidence, or
    incoherent verdict pairs. Raises ReceiptAlreadyClosed on a second
    verdict for the same receipt_id within this call or the given log.
    """
    if not verifier_id or not verifier_id.strip():
        raise VerdictRefused("verifier identity is required; anonymous verdicts refused")
    stamp = time.time() if now is None else now

    closed: list[ap.ActionReceipt] = []
    records: list[VerdictRecord] = []
    skipped: list[tuple] = []
    seen_this_call: set[str] = set()

    def record(rec: VerdictRecord) -> None:
        if log is not None:
            log.append(rec)
        records.append(rec)

    def structural_close(receipt: ap.ActionReceipt, code: str, note: str) -> None:
        """Machine closure: no verifier judgment involved."""
        closed_receipt = ap.apply_verify_verdict(
            receipt, verified=False,
            evidence=f"verify-seam structural closure [{code}]: {note}")
        # ap.apply_verify_verdict yields truth_state BLOCKED for verified=False;
        # the code is carried on the verdict record so NOT_PROVEN stays
        # distinguishable from REJECTED.
        record(VerdictRecord(
            receipt_id=receipt.receipt_id, plan_id=receipt.plan_id,
            verifier_id=_SEAM_VERIFIER_ID, verified=False,
            acceptance=REJECTED, evidence=note, verdict_at=stamp,
            codes=(code,)))
        closed.append(ap.ActionReceipt(
            receipt_id=closed_receipt.receipt_id, plan_id=closed_receipt.plan_id,
            phase=closed_receipt.phase, executed=closed_receipt.executed,
            outcome_verified=closed_receipt.outcome_verified,
            truth_state=closed_receipt.truth_state,
            evidence=closed_receipt.evidence,
            codes=closed_receipt.codes + (code,),
            observed_outcome=closed_receipt.observed_outcome,
            expected_outcome=closed_receipt.expected_outcome))

    for receipt in receipts:
        if receipt.phase != "EXECUTION_COMPLETED" or receipt.truth_state != "UNKNOWN":
            skipped.append((receipt.receipt_id,
                            f"{NOT_ELIGIBLE}: phase={receipt.phase} "
                            f"truth_state={receipt.truth_state}"))
            continue
        if receipt.receipt_id in seen_this_call or (
                log is not None and receipt.receipt_id in log.closed_receipt_ids()):
            raise ReceiptAlreadyClosed(
                f"receipt {receipt.receipt_id} already closed; second verdict refused")
        seen_this_call.add(receipt.receipt_id)

        if not receipt.expected_outcome:
            structural_close(receipt, EXPECTED_OUTCOME_UNDEFINED,
                             "expected outcome undefined; request definition (NOT_PROVEN)")
            continue
        if receipt.observed_outcome is None:
            structural_close(receipt, OBSERVATION_MISSING,
                             "observation data missing; request data (NOT_PROVEN)")
            continue

        verdict = verdict_fn(receipt)
        if not verdict.evidence or not verdict.evidence.strip():
            raise VerdictRefused(
                f"receipt {receipt.receipt_id}: verdict carries no evidence; "
                "no acceptance without evidence")
        if not _coherent(verdict):
            raise VerdictRefused(
                f"receipt {receipt.receipt_id}: incoherent verdict "
                f"(verified={verdict.verified}, acceptance={verdict.acceptance})")

        if verdict.acceptance == PENDING:
            # Inconclusive: record the gap, leave the receipt UNKNOWN.
            record(VerdictRecord(
                receipt_id=receipt.receipt_id, plan_id=receipt.plan_id,
                verifier_id=verifier_id, verified=False,
                acceptance=PENDING, evidence=verdict.evidence,
                verdict_at=stamp, codes=()))
            continue

        closed_receipt = ap.apply_verify_verdict(
            receipt, verified=verdict.verified, evidence=verdict.evidence)
        record(VerdictRecord(
            receipt_id=receipt.receipt_id, plan_id=receipt.plan_id,
            verifier_id=verifier_id, verified=verdict.verified,
            acceptance=verdict.acceptance, evidence=verdict.evidence,
            verdict_at=stamp, codes=()))
        closed.append(closed_receipt)

    return CloseResult(closed=tuple(closed), records=tuple(records),
                       skipped=tuple(skipped))


def reconcile_ledger(ledger: ap.ReceiptLedger,
                     *,
                     verifier_id: str,
                     verdict_fn: Callable[[ap.ActionReceipt], Verdict],
                     now: float | None = None,
                     log: VerdictLog | None = None) -> CloseResult:
    """Runtime entry point: feed the producer's receipt record through the
    VERIFY seam. A 24/7 worker calls this once per reconciliation cycle,
    after the independent verifier's judgments are available; the seam
    decides eligibility per receipt. No caller walks the ledger itself —
    one seam, no forks, no duplicate stores.

    A missing ledger is refused loudly: reconciliation of nothing is a
    defect, never a no-op success.
    """
    if ledger is None:
        raise VerdictRefused("receipt ledger is required; nothing to reconcile")
    return close_receipts(ledger.entries(), verifier_id=verifier_id,
                          verdict_fn=verdict_fn, now=now, log=log)
