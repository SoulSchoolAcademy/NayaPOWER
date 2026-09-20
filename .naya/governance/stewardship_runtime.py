#!/usr/bin/env python3
"""Deterministic Stewardship of Intelligence gate.

Standard-library only. This module does not execute external actions. It decides
whether a consequential action is sufficiently governed to proceed, retry,
escalate, or stop, and persists a small attempt ledger so equivalent failures
cannot silently loop across invocations.
"""
from __future__ import annotations
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_LEDGER = ROOT / ".naya" / "governance" / "ACTION-LEDGER.json"
THRESHOLDS = {"caution": 3, "high_caution": 5, "redline": 10}
REQUIRED_PREFLIGHT = ("objective", "current_truth", "proposed_action", "expected_effect", "verification_plan", "stop_condition")
MATERIAL_KEYS = ("tool", "environment", "source", "dependency", "diagnostic", "implementation", "test_strategy", "runtime_boundary", "permission_boundary", "hypothesis", "strategy")


def now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_ledger(path=DEFAULT_LEDGER):
    if not path.exists():
        return {"schema": "naya-power-action-ledger/v1", "operations": {}}
    return json.loads(path.read_text(encoding="utf-8"))


def save_ledger(ledger, path=DEFAULT_LEDGER):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(path)


def material_change(previous, current):
    return any(previous.get(k) != current.get(k) for k in MATERIAL_KEYS if k in previous or k in current)


def equivalent_attempts(history, current):
    count = 0
    for attempt in history:
        if attempt.get("failure", False) and not material_change(attempt, current):
            count += 1
    return count


def preflight(action):
    missing = [k for k in REQUIRED_PREFLIGHT if not str(action.get(k, "")).strip()]
    if missing:
        return {"decision": "BLOCKED_PENDING_GOVERNANCE", "reason": "missing required pre-action fields", "missing": missing}
    return {"decision": "PROCEED_TO_CHEAP_VALIDATION", "reason": "pre-action governance fields present"}


def resource_decision(action):
    """Require cost awareness and cheap validation before materially expensive work."""
    expensive = bool(action.get("expensive", False))
    cheap = str(action.get("cheaper_validation", "")).strip()
    cost = action.get("cost_estimate")
    if expensive and not cheap:
        return {"decision": "BLOCKED_CHEAP_VALIDATION_REQUIRED", "reason": "an expensive action lacks a cheaper reliable validation path"}
    if cost is None:
        return {"decision": "COST_AWARENESS_REQUIRED", "reason": "provide a reasonable cost estimate before consequential execution"}
    return {"decision": "RESOURCE_GATE_PASS", "cost_estimate": cost}


def evidence_decision(action, observed=None):
    plan = str(action.get("verification_plan", "")).strip()
    if not plan:
        return {"decision": "BLOCKED_NO_VERIFICATION_PLAN"}
    if observed is None:
        return {"decision": "EXECUTED_NOT_VERIFIED", "verification_plan": plan}
    if observed.get("verified", False):
        return {"decision": "VERIFIED", "evidence": observed.get("evidence", [])}
    return {"decision": "NOT_VERIFIED", "evidence": observed.get("evidence", [])}


def failure_decision(action, ledger=None):
    ledger = ledger if ledger is not None else load_ledger()
    key = action.get("operation_key")
    if not key:
        return {"decision": "BLOCKED_PENDING_GOVERNANCE", "reason": "operation_key required for failure tracking"}
    history = ledger.setdefault("operations", {}).setdefault(key, [])
    equivalent = equivalent_attempts(history, action) + 1
    if equivalent >= THRESHOLDS["redline"]:
        decision = "STOP_REDLINE"
    elif equivalent >= THRESHOLDS["high_caution"]:
        decision = "STOP_HIGH_CAUTION"
    elif equivalent >= THRESHOLDS["caution"]:
        decision = "STRATEGY_REASSESSMENT_REQUIRED"
    else:
        decision = "DIAGNOSE_BEFORE_RETRY"
    return {"decision": decision, "equivalent_failure_count": equivalent, "thresholds": THRESHOLDS}


def stop_decision(action, outcome):
    if outcome.get("objective_satisfied", False):
        return {"decision": "STOP_OBJECTIVE_SATISFIED"}
    if outcome.get("no_new_information", False):
        return {"decision": "STOP_NO_NEW_INFORMATION"}
    if outcome.get("evidence_unavailable", False):
        return {"decision": "STOP_EVIDENCE_UNAVAILABLE"}
    if outcome.get("disproportionate_cost", False):
        return {"decision": "STOP_DISPROPORTIONATE_COST"}
    return {"decision": "CONTINUE_IF_AUTHORIZED"}


def record_result(action, result, ledger=None, path=DEFAULT_LEDGER):
    ledger = ledger if ledger is not None else load_ledger(path)
    key = action.get("operation_key")
    if not key:
        raise ValueError("operation_key required")
    entry = dict(action)
    entry.update({"failure": bool(result.get("failure")), "success": bool(result.get("success")), "observed_result": result.get("observed_result", ""), "recorded_at": now()})
    ledger.setdefault("operations", {}).setdefault(key, []).append(entry)
    save_ledger(ledger, path)
    return entry


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("preflight"); p.add_argument("json_file")
    f = sub.add_parser("failure"); f.add_argument("json_file")
    r = sub.add_parser("resource"); r.add_argument("json_file")
    args = ap.parse_args()
    action = json.loads(Path(args.json_file).read_text(encoding="utf-8"))
    if args.cmd == "preflight": result = preflight(action)
    elif args.cmd == "failure": result = failure_decision(action)
    else: result = resource_decision(action)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
