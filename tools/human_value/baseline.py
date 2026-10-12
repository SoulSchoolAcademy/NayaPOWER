#!/usr/bin/env python3
"""baseline.py — pin the human-value baseline as a re-runnable, verifiable snapshot.

Reads the observed-experience ledgers (observed-events, pending-candidates,
observation-sweeps), folds them exactly the way `observe.py report` does, and
writes a pinned baseline JSON: the first honest numbers plus the questions the
numbers cannot answer.

The baseline is a snapshot, not a verdict. Every number traces to a ledger
record; every ledger record traces to evidence. Re-run weekly; the diff between
baselines is the trend.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.human_value.observe import (  # noqa: E402
    OBSERVED_EVENTS,
    OBSERVATION_SWEEPS,
    PENDING_CANDIDATES,
    read_jsonl,
)
from tools.human_value.observation_schema import (  # noqa: E402
    fold_candidates,
    validate_observation_ledger,
    validate_sweep,
)

INSTRUMENT = "observed-experience-instrument-v1"

OPEN_QUESTIONS = [
    {
        "id": "Q1",
        "question": "The 3 pending candidates were graded by naya-mu, the same seat that "
                    "collected this sweep. A different seat must run the next sweep's "
                    "promotion step for them (assessor != collector). Who takes it?",
        "owner": "human-value lead (next sweep)",
    },
    {
        "id": "Q2",
        "question": "The counterfactual value types (cognitive_load_reduced, rework_avoided, "
                    "error_prevented) are candidate-heavy by design — a prevented error is only "
                    "real if the human confirms it was real. What does 'better' look like for "
                    "these, in Shawn's judgment?",
        "owner": "Shawn (charter escalation: instrument designed first, input requested now)",
    },
    {
        "id": "Q3",
        "question": "All 6 observed events are C2 (durable chat log as recorded by the main "
                    "agent). API-grounded authorship (his own comment under his own account, or "
                    "an explicit relay protocol) would strengthen every future observation.",
        "owner": "Shawn / human-value lead",
    },
]

HONESTY_NOTES = [
    "All numbers are FORMATIVE until the instrument's §5 calibration completes "
    "(two_seat_agreement and Coda 1 adversarial review still pending).",
    "UNOBSERVED is not zero value — it is 'no human observation exists.'",
    "The 21-day candidate expiry clock started 2026-10-12 for the 3 pending candidates.",
    "useful_outcome units are counts of observed experiences/actions, never ratings.",
    "attention_demanded counts corrective interventions; its trend target is DOWN.",
]


def _instrument_head() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=REPO_ROOT, capture_output=True, text=True, check=True,
        )
        return out.stdout.strip()
    except Exception:
        return "unknown"


def _calibration_banner(status: dict) -> str:
    checks = ("known_answer", "two_seat_agreement", "adversarial_review")
    done = [k for k in checks if status.get(k) == "pass"]
    if len(done) == len(checks):
        return "CALIBRATED — all three §5 checks passed."
    pending = [k for k in checks if status.get(k) != "pass"]
    return ("FORMATIVE — calibration incomplete. Pending: " + ", ".join(pending) +
            ". Do not cite these numbers as established metrics.")


def build_baseline(ledgers: Path, as_of: str, calibration_status: dict | None) -> dict:
    events = validate_observation_ledger(read_jsonl(ledgers / OBSERVED_EVENTS))
    folded = fold_candidates(read_jsonl(ledgers / PENDING_CANDIDATES))
    sweeps = [validate_sweep(s) for s in read_jsonl(ledgers / OBSERVATION_SWEEPS)]

    by_type: dict[str, int] = {}
    observed_detail = []
    for e in events:
        by_type[e["value_type"]] = by_type.get(e["value_type"], 0) + e["value_units"]
        observed_detail.append({
            "event_id": e["event_id"],
            "observation_kind": e["observation_kind"],
            "value_type": e["value_type"],
            "value_units": e["value_units"],
            "verbatim_hash": e["verbatim_hash"],
            "observed_at": e["observed_at"],
            "authorship": e["authorship"],
        })

    pending = [c for c in folded.values() if c["status"] == "pending"]
    unobserved = [c for c in folded.values() if c["status"] == "unobserved"]

    window_start = min([s["watermark_start"] for s in sweeps], default=as_of)

    return {
        "baseline_id": "HV-BASELINE-" + as_of[:10].replace("-", ""),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "window": {"start": window_start, "end": as_of},
        "method": {
            "instrument": INSTRUMENT,
            "instrument_head": _instrument_head(),
            "calibration_banner": _calibration_banner(calibration_status or {}),
        },
        "observed": {
            "units_by_value_type": by_type,
            "event_count": len(events),
            "events": observed_detail,
        },
        "candidates": {
            "pending": len(pending),
            "unobserved": len(unobserved),
            "expiry_days": 21,
            "pending_ids": sorted(c["candidate_id"] for c in pending),
        },
        "sweeps": [
            {"sweep_id": s["sweep_id"], "watermark": [s["watermark_start"], s["watermark_end"]],
             "observations_found": s["observations_found"],
             "promotions_proposed": s["promotions_proposed"],
             "null_sweep": s["null_sweep"]}
            for s in sweeps
        ],
        "open_questions": OPEN_QUESTIONS,
        "honesty_notes": HONESTY_NOTES,
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Pin the human-value baseline snapshot.")
    p.add_argument("--ledgers", required=True)
    p.add_argument("--out", required=True, help="path for the baseline JSON")
    p.add_argument("--as-of", required=True, help="ISO-8601 snapshot time")
    p.add_argument("--calibration-status", default=None,
                   help="path to JSON with {known_answer,two_seat_agreement,adversarial_review}")
    args = p.parse_args(argv)

    status: dict = {}
    if args.calibration_status:
        doc = json.loads(Path(args.calibration_status).read_text())
        status = doc.get("calibration_status", doc)

    baseline = build_baseline(Path(args.ledgers), args.as_of, status)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(baseline, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8")
    print(json.dumps({
        "baseline": str(out),
        "baseline_id": baseline["baseline_id"],
        "observed_units": baseline["observed"]["units_by_value_type"],
        "candidates_pending": baseline["candidates"]["pending"],
        "banner": baseline["method"]["calibration_banner"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
