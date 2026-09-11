#!/usr/bin/env python3
"""Naya Power Runtime Kernel v1.

Small, deterministic, provider-neutral constitutional decision kernel.
It governs candidate actions; it does not pretend to be the model or the tool.
Dependency-free by design so the exact source can be executed in CI or locally.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CONTRACT_PATH = Path(__file__).with_name("NAYA-POWER-RUNTIME-CONTRACT.json")
EVIDENCE_RANK = {
    "UNKNOWN": 0,
    "IMPLEMENTED": 1,
    "TESTED": 2,
    "VERIFIED": 3,
    "RUNTIME-PROVEN": 4,
    "PRODUCTION-PROVEN": 5,
}
ALLOWED_AUTH = {"approved", "denied", "unknown"}
DECISIONS = {"SELECT", "REFUSE", "ESCALATE"}


def load_contract() -> dict[str, Any]:
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _receipt_id(request_id: str, decision: str, candidate_id: str | None) -> str:
    basis = f"{request_id}|{decision}|{candidate_id or ''}"
    return "NPR-" + hashlib.sha256(basis.encode("utf-8")).hexdigest()[:16]


def _error(message: str) -> ValueError:
    return ValueError(message)


def validate_request(request: dict[str, Any], contract: dict[str, Any]) -> None:
    required = {"request_id", "mission", "context", "authority", "candidates", "constitution_version"}
    missing = sorted(required - set(request))
    if missing:
        raise _error(f"missing request fields: {', '.join(missing)}")
    if request["constitution_version"] != contract["version"]:
        raise _error("constitution_version does not match runtime contract version")
    if not isinstance(request["candidates"], list) or not request["candidates"]:
        raise _error("candidates must be a non-empty list")
    for candidate in request["candidates"]:
        required_candidate = {
            "id", "description", "expected_benefit", "necessary_cost", "risk_loss",
            "authorization", "boundary_violations", "evidence_state",
            "reversible", "governance_sensitive"
        }
        missing_candidate = sorted(required_candidate - set(candidate))
        if missing_candidate:
            raise _error(f"candidate {candidate.get('id', '<unknown>')} missing: {', '.join(missing_candidate)}")
        if candidate["authorization"] not in ALLOWED_AUTH:
            raise _error(f"candidate {candidate['id']}: invalid authorization")
        if candidate["evidence_state"] not in EVIDENCE_RANK:
            raise _error(f"candidate {candidate['id']}: invalid evidence_state")
        for field in ("expected_benefit", "necessary_cost", "risk_loss"):
            value = candidate[field]
            if not isinstance(value, (int, float)) or not 0 <= value <= 100:
                raise _error(f"candidate {candidate['id']}: {field} must be 0..100")
        if not isinstance(candidate["boundary_violations"], list):
            raise _error(f"candidate {candidate['id']}: boundary_violations must be a list")
        if candidate.get("verification_claim") and not candidate.get("evidence"):
            raise _error(f"candidate {candidate['id']}: fabricated verification claim without evidence")


def evaluate(request: dict[str, Any]) -> dict[str, Any]:
    contract = load_contract()
    validate_request(request, contract)

    evaluations: list[dict[str, Any]] = []
    eligible: list[dict[str, Any]] = []
    refusal_reasons: list[str] = []
    escalation_reasons: list[str] = []

    for candidate in request["candidates"]:
        cid = candidate["id"]
        reasons: list[str] = []
        status = "ELIGIBLE"
        decision = "CONSIDER"

        if candidate["boundary_violations"]:
            status = "INELIGIBLE"
            decision = "REFUSE"
            reasons.append("protected boundary violation")

        if candidate["authorization"] == "denied":
            status = "INELIGIBLE"
            decision = "REFUSE"
            reasons.append("authorization denied")
        elif candidate["authorization"] == "unknown":
            status = "INELIGIBLE"
            decision = "ESCALATE"
            reasons.append("authorization unknown")

        if candidate["governance_sensitive"] and candidate["authorization"] != "approved":
            status = "INELIGIBLE"
            decision = "ESCALATE"
            reasons.append("governance-sensitive action requires authority")

        if candidate.get("requires_verified_evidence") and EVIDENCE_RANK[candidate["evidence_state"]] < EVIDENCE_RANK["VERIFIED"]:
            status = "INELIGIBLE"
            decision = "ESCALATE"
            reasons.append("required evidence is not verified")

        if candidate.get("verification_claim") and not candidate.get("evidence"):
            status = "INELIGIBLE"
            decision = "REFUSE"
            reasons.append("fabricated verification")

        value = None
        if status == "ELIGIBLE":
            value = round(
                float(candidate["expected_benefit"])
                - float(candidate["necessary_cost"])
                - float(candidate["risk_loss"]),
                4,
            )
            eligible.append({"candidate": candidate, "value": value})
        else:
            if decision == "REFUSE":
                refusal_reasons.extend(f"{cid}: {reason}" for reason in reasons)
            else:
                escalation_reasons.extend(f"{cid}: {reason}" for reason in reasons)

        evaluations.append({
            "candidate_id": cid,
            "status": status,
            "decision": decision,
            "reasons": reasons,
            "value": value,
            "authorization": candidate["authorization"],
            "boundary_violations": list(candidate["boundary_violations"]),
            "evidence_state": candidate["evidence_state"],
        })

    if eligible:
        # Deterministic tie-break: highest value, then lower risk, then candidate id.
        winner = sorted(
            eligible,
            key=lambda item: (-item["value"], item["candidate"]["risk_loss"], item["candidate"]["id"]),
        )[0]
        decision = "SELECT"
        selected_id = winner["candidate"]["id"]
        reason = f"highest responsible eligible value={winner['value']}"
    elif refusal_reasons and not escalation_reasons:
        decision = "REFUSE"
        selected_id = None
        reason = "no eligible action; protected or denied action(s) were rejected"
    else:
        decision = "ESCALATE"
        selected_id = None
        reason = "no autonomous candidate is eligible under the supplied authority/evidence contract"

    now = datetime.now(timezone.utc).isoformat()
    receipt = {
        "receipt_id": _receipt_id(request["request_id"], decision, selected_id),
        "runtime": "Naya Power Runtime Kernel",
        "runtime_version": contract["version"],
        "request_id": request["request_id"],
        "constitution_version": request["constitution_version"],
        "decision": decision,
        "selected_candidate": selected_id,
        "reason": reason,
        "candidate_evaluations": evaluations,
        "evidence": {
            "kernel_evaluation": "RUNTIME-PROVEN",
            "external_action": "NOT_EXECUTED_BY_KERNEL",
            "external_outcome": "UNKNOWN",
        },
        "verification": {
            "decision_procedure_executed": True,
            "external_action_verified": False,
        },
        "timestamp": now,
    }
    return receipt


def demo_requests() -> list[tuple[str, dict[str, Any], str]]:
    base = {
        "request_id": "SELFTEST-001",
        "mission": "Improve a software system responsibly.",
        "context": {"project": "NayaPOWER", "mode": "self-test"},
        "authority": {"actor": "test-harness", "scope": "runtime-evaluation"},
        "constitution_version": "1.0.0",
    }
    return [
        (
            "safe-value-selection",
            {**base, "request_id": "SELFTEST-001", "candidates": [
                {"id": "safe-a", "description": "Run a verified test and repair a confirmed defect.", "expected_benefit": 90, "necessary_cost": 20, "risk_loss": 5, "authorization": "approved", "boundary_violations": [], "evidence_state": "VERIFIED", "reversible": True, "governance_sensitive": False},
                {"id": "safe-b", "description": "Make a cosmetic change without verification.", "expected_benefit": 60, "necessary_cost": 10, "risk_loss": 20, "authorization": "approved", "boundary_violations": [], "evidence_state": "IMPLEMENTED", "reversible": True, "governance_sensitive": False},
            ]},
            "SELECT",
        ),
        (
            "human-life-hard-boundary",
            {**base, "request_id": "SELFTEST-002", "candidates": [
                {"id": "harm", "description": "Cause human harm because it allegedly creates a greater benefit.", "expected_benefit": 100, "necessary_cost": 0, "risk_loss": 0, "authorization": "approved", "boundary_violations": ["HUMAN_LIFE_PROTECTED"], "evidence_state": "VERIFIED", "reversible": False, "governance_sensitive": False},
                {"id": "safe", "description": "Choose a safe alternative.", "expected_benefit": 30, "necessary_cost": 10, "risk_loss": 5, "authorization": "approved", "boundary_violations": [], "evidence_state": "VERIFIED", "reversible": True, "governance_sensitive": False},
            ]},
            "SELECT",
        ),
        (
            "unknown-authority-escalates",
            {**base, "request_id": "SELFTEST-003", "candidates": [
                {"id": "unknown", "description": "Take an external action with unknown authorization.", "expected_benefit": 100, "necessary_cost": 0, "risk_loss": 0, "authorization": "unknown", "boundary_violations": [], "evidence_state": "VERIFIED", "reversible": False, "governance_sensitive": False},
            ]},
            "ESCALATE",
        ),
        (
            "governance-mutation-escalates",
            {**base, "request_id": "SELFTEST-004", "candidates": [
                {"id": "mutate-law", "description": "Change the constitutional law because the model believes it is better.", "expected_benefit": 100, "necessary_cost": 0, "risk_loss": 0, "authorization": "unknown", "boundary_violations": [], "evidence_state": "VERIFIED", "reversible": True, "governance_sensitive": True},
            ]},
            "ESCALATE",
        ),
        (
            "fabricated-verification-rejected",
            {**base, "request_id": "SELFTEST-005", "candidates": [
                {"id": "fake-proof", "description": "Claim the external result was verified without evidence.", "expected_benefit": 100, "necessary_cost": 0, "risk_loss": 0, "authorization": "approved", "boundary_violations": [], "evidence_state": "VERIFIED", "reversible": True, "governance_sensitive": False, "verification_claim": True, "evidence": []},
            ]},
            "ERROR",
        ),
    ]


def self_test() -> dict[str, Any]:
    results = []
    passed = 0
    for name, request, expected in demo_requests():
        try:
            receipt = evaluate(request)
            actual = receipt["decision"]
            ok = actual == expected
            detail = receipt["reason"]
        except ValueError as exc:
            actual = "ERROR"
            ok = actual == expected
            detail = str(exc)
        results.append({"test": name, "expected": expected, "actual": actual, "passed": ok, "detail": detail})
        passed += int(ok)
    return {
        "runtime": "Naya Power Runtime Kernel",
        "version": load_contract()["version"],
        "tests": results,
        "passed": passed,
        "total": len(results),
        "status": "PASS" if passed == len(results) else "FAIL",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--request", type=Path)
    args = parser.parse_args()

    if args.self_test:
        result = self_test()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if result["status"] == "PASS" else 1

    if args.request:
        request = json.loads(args.request.read_text(encoding="utf-8"))
        print(json.dumps(evaluate(request), indent=2, ensure_ascii=False))
        return 0

    parser.error("use --self-test or --request <json-file>")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
