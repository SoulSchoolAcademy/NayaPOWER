"""Human Value instrument v1 — deterministic recomputation of measured human value.

Reads a validated event ledger (JSONL, one event per line), fails closed on any
schema violation, and emits a deterministic report: HV/day per value type,
DAI (demand-attention index), ledger hash for cold-successor verification, and
— when decision receipts are supplied — the Value Calculus real-outcome loop:
observed delta_v_actual joined to predicted delta_v, feeding
kernel/value_calculus.py `calibration_summary`.

Deterministic by construction:
  - `as_of` defaults to the latest event date in the ledger (never wall-clock).
  - events are processed sorted by (recorded_at, event_id).
  - the ledger sha256 pins the exact bytes a successor must reproduce.

Exit codes: 0 = valid ledger, report written. 2 = schema/validation failure
(fail closed; no number is emitted on invalid input).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import date, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from kernel.value_calculus import calibration_summary  # noqa: E402
from tools.human_value.schema import SCHEMA_VERSION, VALUE_TYPES, validate_ledger, SchemaError  # noqa: E402

INSTRUMENT = "human-value-instrument-v1"


def ledger_sha256(lines: list[str]) -> str:
    """Hash the exact ledger bytes (normalized line endings), in order."""
    h = hashlib.sha256()
    for line in lines:
        h.update(line.rstrip("\r\n").encode("utf-8"))
        h.update(b"\n")
    return "sha256:" + h.hexdigest()


def load_ledger(path: Path) -> tuple[list[str], list[dict]]:
    raw_lines = [ln for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    raw_events = []
    for i, ln in enumerate(raw_lines):
        try:
            raw_events.append(json.loads(ln))
        except json.JSONDecodeError as e:
            raise SchemaError(f"ledger line {i + 1}: invalid JSON: {e}")
    events = validate_ledger(raw_events)
    events.sort(key=lambda e: (e["recorded_at"], e["event_id"]))
    return raw_lines, events


def compute(events: list[dict], window_days: int, as_of: date) -> dict:
    if window_days < 1:
        raise ValueError("window_days must be >= 1")
    start = as_of - timedelta(days=window_days - 1)
    in_window = [e for e in events if start.isoformat() <= e["recorded_at"] <= as_of.isoformat()]

    hv_per_day = {vt: 0.0 for vt in VALUE_TYPES}
    for e in in_window:
        hv_per_day[e["value_type"]] += e["value_units"]
    hv_per_day = {vt: round(total / window_days, 4) for vt, total in hv_per_day.items()}
    total = round(sum(hv_per_day.values()), 4)

    # DAI: demand-attention index. Units are attention events; trend target DOWN.
    dai = hv_per_day.get("attention_demanded", 0.0)

    return {
        "instrument": INSTRUMENT,
        "schema_version": SCHEMA_VERSION,
        "as_of": as_of.isoformat(),
        "window_days": window_days,
        "window_start": start.isoformat(),
        "events_validated": len(events),
        "events_in_window": len(in_window),
        "hv_per_day_by_type": hv_per_day,
        "hv_per_day_total": total,
        "dai_per_day": dai,
    }


def load_receipts(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise SchemaError("receipts file must be a JSON list of decision receipts")
    return data


def calibrate(receipts: list[dict], events: list[dict]) -> dict:
    """Real-outcome loop: join observed delta_v_actual to predicted delta_v.

    A receipt supplies delta_v_predicted for a decision_id; a human-value event
    supplies the observed delta_v_actual. calibration_summary is the kernel's
    own math — this module only builds the join, never its own scorecard.
    """
    predicted_by_id: dict[str, float] = {}
    for r in receipts:
        did = r.get("decision_id")
        pred = r.get("delta_v_predicted")
        if did and isinstance(pred, (int, float)):
            predicted_by_id[did] = float(pred)
    records = []
    for e in events:
        did = e.get("decision_id")
        actual = e.get("delta_v_actual")
        if did and actual is not None and did in predicted_by_id:
            records.append({
                "decision_id": did,
                "delta_v_predicted": predicted_by_id[did],
                "delta_v_actual": actual,
            })
    summary = calibration_summary(records)
    summary["records"] = records
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Human Value instrument v1")
    parser.add_argument("--ledger", required=True, type=Path,
                        help="JSONL event ledger path")
    parser.add_argument("--window-days", type=int, default=7)
    parser.add_argument("--as-of", type=str, default=None,
                        help="YYYY-MM-DD; defaults to latest event date (deterministic)")
    parser.add_argument("--receipts", type=Path, default=None,
                        help="JSON list of value-calculus decision receipts for calibration")
    parser.add_argument("--expect-ledger-sha256", type=str, default=None,
                        help="fail closed if ledger bytes differ from this pin")
    args = parser.parse_args(argv)

    try:
        raw_lines, events = load_ledger(args.ledger)
        digest = ledger_sha256(raw_lines)
        if args.expect_ledger_sha256 and digest != args.expect_ledger_sha256:
            raise SchemaError(
                f"ledger hash mismatch: got {digest}, expected {args.expect_ledger_sha256} "
                f"(bytes changed since the pinned measurement)")
        if args.as_of:
            as_of = date.fromisoformat(args.as_of)
        elif events:
            as_of = date.fromisoformat(max(e["recorded_at"] for e in events))
        else:
            raise SchemaError("empty ledger: nothing to measure (no as-of date derivable)")
        report = compute(events, args.window_days, as_of)
        report["ledger_sha256"] = digest
        report["ledger_path"] = str(args.ledger)
        if args.receipts:
            report["calibration"] = calibrate(load_receipts(args.receipts), events)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    except SchemaError as e:
        print(f"SCHEMA_ERROR: {e}", file=sys.stderr)
        return 2
    except (ValueError, OSError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
