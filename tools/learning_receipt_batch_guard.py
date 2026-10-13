"""Batch-generation guard for learning receipts (convergence item D hardening).

The #2524 defect (Epsilon's wave-78 provenance audit, 2026-10-13): 750 ledger
rows stamped VERIFIED, all emitted inside a 78-millisecond window, zero rows
pointing to an existing receipt file, agent names outside the named-seat
roster. The convergence-D validators (tools/learning_application_receipt.py)
PASS such receipts: they verify internal consistency (schema, id integrity,
link binding, verifier != applier) -- not external grounding. A batch
generator minting internally-consistent receipts is invisible to them.
Demonstrated 2026-10-13: 25/25 batch-pattern receipts valid, E2/E3 eligible,
B evidence-integrity ok.

This module is the distributional counterweight, pure by the same contract
(no DB, no network): given a set of receipt dicts, it measures the emission
distribution -- timestamp window, per-receipt pace, timestamp collisions --
and ANNOTATES batch-suspect sets. It never rejects: legitimate backfills
(e.g. the B-51 backfill) are also bulk-emitted, and legitimacy is a caller
judgment, not a distributional fact.

Signals:
  BATCH_WINDOW_NARROW   n >= min_batch and the whole set fits in a window
                        implying faster than one genuine receipt per second
                        (a human cannot emit real learning receipts faster)
  TIMESTAMP_COLLISIONS  distinct timestamps < half the set -- batch stampers
                        reuse the same ts across rows
  ROSTER_UNKNOWN_NAMES  (only with known_seats=) applier/verifier names
                        outside the supplied roster -- the #2524 invented-seat
                        pattern, checked against caller-supplied truth

What this does NOT claim (P-011):
  - Suspect != fabricated. A narrow window proves programmatic emission, not
    dishonesty. The B-51 backfill is the standing legitimate counterexample.
    The guard annotates; the caller judges.
  - Clean != provenanced. A human-paced set can still carry false claims;
    artifact existence and content truth need a runtime auditor with world
    access (Epsilon's census technique: every receipt path looked up in the
    tree).
  - Clustered batches inside a wide set are not detected: the window is
    measured over the whole set handed to the guard.
  - Name checks need the caller to supply known_seats; the guard carries no
    roster and no network. Without it, invented names are invisible.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

# A human cannot emit genuine learning receipts faster than this pace.
# The #2524 signal (750 rows / 78 ms ~= 0.1 ms per receipt) is ~10,000x
# below the floor; the floor is deliberately generous so only programmatic
# emission trips it.
DEFAULT_PACE_FLOOR_SECONDS = 1.0

# Below this many parseable receipts, no distribution exists to measure.
DEFAULT_MIN_BATCH = 5

_VERDICT_CLEAN = "CLEAN"
_VERDICT_SUSPECT = "BATCH_SUSPECT"
_VERDICT_INCONCLUSIVE = "INCONCLUSIVE"


def _parse_ts(value: Any) -> datetime | None:
    """Parse an ISO-8601 timestamp; None when unparseable. Never raises."""
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    try:
        # fromisoformat in 3.11+ handles 'Z'; normalize for older parsers.
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        parsed = datetime.fromisoformat(text)
    except (ValueError, OverflowError):
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def _resolve_path(mapping: dict[str, Any], path: str) -> Any:
    """Resolve a dotted path (e.g. 'independent_verification.verifier')."""
    current: Any = mapping
    for part in path.split("."):
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current


def assess_batch(
    receipts: list[dict[str, Any]] | tuple[dict[str, Any], ...],
    ts_field: str = "applied_at",
    min_batch: int = DEFAULT_MIN_BATCH,
    pace_floor_seconds: float = DEFAULT_PACE_FLOOR_SECONDS,
    known_seats: set[str] | frozenset[str] | list[str] | tuple[str, ...] | None = None,
    name_fields: tuple[str, ...] = ("applier",),
) -> dict[str, Any]:
    """Assess a receipt set for batch-generation signals. Pure: no I/O.

    receipts: the set to assess (one kind of receipt; ts_field names the
        timestamp on that kind, e.g. 'retrieved_at', 'applied_at',
        'observed_at').
    known_seats: optional caller-supplied roster; when given, names outside
        it are reported under ROSTER_UNKNOWN_NAMES. The guard carries no
        roster of its own.
    Returns a verdict dict; verdict is one of CLEAN / BATCH_SUSPECT /
    INCONCLUSIVE. BATCH_SUSPECT is an annotation for caller judgment --
    never a rejection (legitimate backfills trip the same signals).
    """
    receipts = list(receipts or [])
    stamps: list[datetime] = []
    unparseable = 0
    for receipt in receipts:
        if not isinstance(receipt, dict):
            unparseable += 1
            continue
        parsed = _parse_ts(receipt.get(ts_field))
        if parsed is None:
            unparseable += 1
        else:
            stamps.append(parsed)

    n = len(stamps)
    signals: list[str] = []

    if n < min_batch:
        return {
            "verdict": _VERDICT_INCONCLUSIVE,
            "signals": [
                "INSUFFICIENT_DATA: %d parseable timestamps, need >= %d to measure a distribution"
                % (n, min_batch)
            ],
            "assessed": len(receipts),
            "parseable": n,
            "unparseable": unparseable,
            "window_ms": None,
            "ms_per_receipt": None,
            "distinct_ts": len({s.isoformat() for s in stamps}),
            "roster_unknown": [],
        }

    window_ms = (max(stamps) - min(stamps)).total_seconds() * 1000.0
    ms_per_receipt = window_ms / n if n else 0.0
    distinct_ts = len({s.isoformat() for s in stamps})

    pace_floor_ms = pace_floor_seconds * 1000.0 * n
    if window_ms < pace_floor_ms:
        signals.append(
            "BATCH_WINDOW_NARROW: %d receipts in %.1f ms (%.2f ms/receipt) -- "
            "faster than one receipt per %.1fs; programmatic emission"
            % (n, window_ms, ms_per_receipt, pace_floor_seconds)
        )
    if distinct_ts < n / 2:
        signals.append(
            "TIMESTAMP_COLLISIONS: %d distinct timestamps across %d receipts -- "
            "batch stampers reuse the same ts" % (distinct_ts, n)
        )

    roster_unknown: list[str] = []
    if known_seats is not None:
        roster = {str(s) for s in known_seats}
        seen: set[str] = set()
        for receipt in receipts:
            if not isinstance(receipt, dict):
                continue
            for field in name_fields:
                name = _resolve_path(receipt, field)
                if isinstance(name, str) and name.strip() and name.strip() not in roster:
                    seen.add(name.strip())
        roster_unknown = sorted(seen)
        if roster_unknown:
            signals.append(
                "ROSTER_UNKNOWN_NAMES: %d name(s) outside the supplied roster: %s"
                % (len(roster_unknown), ", ".join(roster_unknown[:8]))
            )

    verdict = _VERDICT_SUSPECT if signals else _VERDICT_CLEAN
    return {
        "verdict": verdict,
        "signals": signals,
        "assessed": len(receipts),
        "parseable": n,
        "unparseable": unparseable,
        "window_ms": window_ms,
        "ms_per_receipt": ms_per_receipt,
        "distinct_ts": distinct_ts,
        "roster_unknown": roster_unknown,
    }


def summarize_assessment(assessment: dict[str, Any]) -> str:
    """One-line human summary of an assess_batch() verdict."""
    assessment = assessment if isinstance(assessment, dict) else {}
    return (
        "batch-guard %s | assessed=%s parseable=%s unparseable=%s | "
        "window_ms=%s ms_per_receipt=%s distinct_ts=%s | signals=%d"
        % (
            assessment.get("verdict"),
            assessment.get("assessed"),
            assessment.get("parseable"),
            assessment.get("unparseable"),
            assessment.get("window_ms"),
            assessment.get("ms_per_receipt"),
            assessment.get("distinct_ts"),
            len(assessment.get("signals") or []),
        )
    )
