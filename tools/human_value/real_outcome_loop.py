"""Real-outcome loop — the bridge between measured human outcomes and the
Decision Value Calculus.

The calculus predicts value (delta_v_predicted) at decision time. The Human
Value instrument observes what actually happened (delta_v_actual) on events
linked by decision_id. This module joins the two and feeds the kernel's own
`calibration_summary` / `build_recalibration_receipt` — it never invents its
own scoring math (one decision engine, per the boot contract).

Loop: PREDICT (calculus) -> ACT -> OBSERVE (human-value event) ->
       CALIBRATE (this module) -> RECALIBRATE-CANDIDATE (kernel receipt).

Recalibration candidates are LEARN_CANDIDATE receipts: they propose, never
promote. Promotion stays a human/authority decision.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from kernel.value_calculus import (  # noqa: E402
    QualityProfile,
    build_recalibration_receipt,
    calibration_summary,
)


def join_prediction_to_outcome(
    receipts: Sequence[Mapping],
    events: Sequence[Mapping],
) -> list[dict]:
    """Join calculus predictions to observed human outcomes by decision_id.

    A join row exists only when BOTH sides are present: a receipt with a
    finite delta_v_predicted and an event with a finite delta_v_actual.
    Partial rows are dropped, never imputed — missing observation is not
    evidence of zero effect.
    """
    predicted: dict[str, float] = {}
    for r in receipts:
        did = r.get("decision_id")
        pred = r.get("delta_v_predicted")
        if isinstance(did, str) and did and isinstance(pred, (int, float)):
            predicted[did] = float(pred)
    rows = []
    for e in events:
        did = e.get("decision_id")
        actual = e.get("delta_v_actual")
        if (
            isinstance(did, str)
            and did in predicted
            and isinstance(actual, (int, float))
        ):
            rows.append({
                "decision_id": did,
                "delta_v_predicted": predicted[did],
                "delta_v_actual": float(actual),
            })
    return rows


def calibrate(receipts: Sequence[Mapping], events: Sequence[Mapping]) -> dict:
    """Kernel calibration summary over joined prediction/outcome rows."""
    rows = join_prediction_to_outcome(receipts, events)
    summary = calibration_summary(rows)
    summary["records"] = rows
    return summary


def recalibration_candidate(
    profile: QualityProfile,
    proposed_version: str,
    receipts: Sequence[Mapping],
    events: Sequence[Mapping],
    evidence_refs: Sequence[str] = (),
) -> dict:
    """Build a LEARN_CANDIDATE recalibration receipt from observed outcomes.

    Raises ValueError when the join is too thin to learn from (n < 3) —
    the kernel needs at least three observations before overprediction can
    be declared. Never promotes; the returned receipt's state is
    LEARN_CANDIDATE and automatic_promotion is False.
    """
    rows = join_prediction_to_outcome(receipts, events)
    if len(rows) < 3:
        raise ValueError(
            f"recalibration needs >= 3 joined observations, got {len(rows)} "
            f"(thin evidence does not move the profile)")
    return build_recalibration_receipt(
        current_profile=profile,
        proposed_version=proposed_version,
        records=rows,
        evidence_refs=list(evidence_refs),
    )
