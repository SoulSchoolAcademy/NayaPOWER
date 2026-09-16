#!/usr/bin/env python3
"""Naya Power Runtime Kernel.

The model may propose and rank actions, but it is never the authority source.
Every consequential candidate must resolve an explicit registry authority and
pass the canonical governance kernel before selection.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
GOVERNANCE = ROOT / ".naya" / "governance"
for path in (GOVERNANCE, ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from governance_kernel import (  # noqa: E402
    DecisionObject,
    Epistemic,
    Risk,
    VerificationPlan,
    evaluate as evaluate_governance,
    load_authority_registry,
    resolve_authority,
)
from SUPERBRAIN.naya_power_decision_calculus import (  # noqa: E402
    Candidate as CalculusCandidate,
    EVIDENCE_RANK as CALCULUS_EVIDENCE_RANK,
    decision as calculate_decision,
)

CONTRACT_PATH = Path(__file__).with_name("NAYA-POWER-RUNTIME-CONTRACT.json")
REGISTRY_PATH = GOVERNANCE / "authority-registry.json"
EVIDENCE_RANK = {"UNKNOWN": 0, "IMPLEMENTED": 1, "TESTED": 2, "VERIFIED": 3, "RUNTIME-PROVEN": 4, "PRODUCTION-PROVEN": 5}
ALLOWED_AUTH = {"approved", "denied", "unknown"}  # legacy vocabulary; never grants authority


def load_contract() -> dict[str, Any]:
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def _receipt_id(request_id: str, decision: str, candidate_id: str | None) -> str:
    return "NPR-" + hashlib.sha256(f"{request_id}|{decision}|{candidate_id or ''}".encode()).hexdigest()[:16]


def _require_authority(request: dict[str, Any], candidate: dict[str, Any]) -> Any:
    supplied = request.get("authority")
    if not isinstance(supplied, dict):
        raise ValueError("explicit authority object is required")
    authority_id = supplied.get("authority_id")
    actor_id = supplied.get("actor_id", supplied.get("actor"))
    purpose = supplied.get("purpose")
    scope = supplied.get("scope")
    permission = candidate.get("required_permission")
    if not all(isinstance(value, str) and value.strip() for value in (authority_id, actor_id, purpose, scope, permission)):
        raise ValueError("authority_id, actor_id, purpose, scope, and candidate.required_permission are required")
    registry = load_authority_registry(REGISTRY_PATH)
    try:
        return resolve_authority(registry, authority_id=authority_id, actor_id=actor_id, purpose=purpose, action=permission, scope=scope)
    except RuntimeError as exc:
        raise ValueError(str(exc)) from exc


def validate_request(request: dict[str, Any], contract: dict[str, Any]) -> None:
    required = {"request_id", "mission", "context", "authority", "candidates", "constitution_version"}
    missing = sorted(required - set(request))
    if missing:
        raise ValueError(f"missing request fields: {', '.join(missing)}")
    if request["constitution_version"] != contract["version"]:
        raise ValueError("constitution_version does not match runtime contract version")
    if not isinstance(request["candidates"], list) or not request["candidates"]:
        raise ValueError("candidates must be a non-empty list")
    for candidate in request["candidates"]:
        required_candidate = {"id", "description", "expected_benefit", "necessary_cost", "risk_loss", "authorization", "required_permission", "boundary_violations", "evidence_state", "reversible", "governance_sensitive"}
        missing_candidate = sorted(required_candidate - set(candidate))
        if missing_candidate:
            raise ValueError(f"candidate {candidate.get('id', '<unknown>')} missing: {', '.join(missing_candidate)}")
        if candidate["authorization"] not in ALLOWED_AUTH:
            raise ValueError(f"candidate {candidate['id']}: invalid legacy authorization value")
        if candidate["evidence_state"] not in EVIDENCE_RANK:
            raise ValueError(f"candidate {candidate['id']}: invalid evidence_state")
        for field in ("expected_benefit", "necessary_cost", "risk_loss"):
            if not isinstance(candidate[field], (int, float)) or not 0 <= candidate[field] <= 100:
                raise ValueError(f"candidate {candidate['id']}: {field} must be 0..100")
        if not isinstance(candidate["boundary_violations"], list):
            raise ValueError(f"candidate {candidate['id']}: boundary_violations must be a list")
        if candidate.get("verification_claim") and not candidate.get("evidence"):
            raise ValueError(f"candidate {candidate['id']}: fabricated verification claim without evidence")


def _legacy_candidate_to_calculus(candidate: dict[str, Any]) -> CalculusCandidate:
    evidence = candidate["evidence_state"]
    uncertainty = {"UNKNOWN": 100.0, "IMPLEMENTED": 70.0, "TESTED": 45.0, "VERIFIED": 20.0, "RUNTIME-PROVEN": 10.0, "PRODUCTION-PROVEN": 0.0}[evidence]
    return CalculusCandidate(
        name=candidate["id"], useful_value=float(candidate["expected_benefit"]),
        harm_avoidance=100.0 - float(candidate["risk_loss"]),
        verification_strength=float(CALCULUS_EVIDENCE_RANK[evidence] * 20), quality=50.0,
        reversibility=100.0 if candidate["reversible"] else 0.0,
        cost_efficiency=100.0 - float(candidate["necessary_cost"]), latency=50.0,
        uncertainty=uncertainty, evidence_state=evidence,
        violates_boundary=bool(candidate["boundary_violations"]), consequence=float(candidate["risk_loss"]),
    )


def _govern_candidate(request: dict[str, Any], candidate: dict[str, Any]) -> Any:
    authority = _require_authority(request, candidate)
    evidence_state = candidate["evidence_state"]
    if evidence_state == "UNKNOWN":
        epistemic = frozenset({Epistemic.UNKNOWN})
        uncertainty = 10
    else:
        epistemic = frozenset({Epistemic.VERIFIED if evidence_state in {"VERIFIED", "RUNTIME-PROVEN", "PRODUCTION-PROVEN"} else Epistemic.OBSERVED})
        uncertainty = {"IMPLEMENTED": 7, "TESTED": 5, "VERIFIED": 2, "RUNTIME-PROVEN": 1, "PRODUCTION-PROVEN": 1}.get(evidence_state, 5)
    risk = Risk(uncertainty=uncertainty, consequence=max(1, min(10, int(round(float(candidate["risk_loss"]) / 10)))), irreversibility=10 if not candidate["reversible"] else 2)
    decision = DecisionObject(
        decision_id=f"runtime:{request['request_id']}:{candidate['id']}", mission=request["mission"], actor_id=authority.principal_id,
        action=candidate["required_permission"], purpose=authority.purpose, scope=authority.scope,
        current_truth=json.dumps(request.get("context", {}), sort_keys=True), gap=candidate["description"],
        evidence=tuple(candidate.get("evidence", ())) or (f"evidence_state:{evidence_state}",), epistemic=epistemic,
        consequence=f"candidate risk_loss={candidate['risk_loss']}", reversible=bool(candidate["reversible"]), risk=risk,
        alternatives=("do_not_execute",), expected_value=f"benefit={candidate['expected_benefit']} cost={candidate['necessary_cost']}",
        required_permission=candidate["required_permission"],
        verification=VerificationPlan(observation="runtime receipt and downstream execution evidence", success_criteria="selected action remains bound to the same authority and scope", stop_conditions=("authority mismatch", "authority expiry/revocation", "scope mismatch", "verification failure")),
        necessary_power=frozenset({candidate["required_permission"]}), requested_power=frozenset({candidate["required_permission"]}),
    )
    return evaluate_governance(decision, authority, now=datetime.now(timezone.utc).isoformat())


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
        status, decision, calculus_score = "ELIGIBLE", "CONSIDER", None
        try:
            governance_result = _govern_candidate(request, candidate)
            if not governance_result.allowed:
                status = "INELIGIBLE"
                decision = "REFUSE" if candidate["boundary_violations"] else "ESCALATE"
                reasons.extend(governance_result.reasons)
        except ValueError as exc:
            status, decision = "INELIGIBLE", "ESCALATE"
            reasons.append(str(exc))
        if candidate["boundary_violations"]:
            status, decision = "INELIGIBLE", "REFUSE"
            reasons.append("protected boundary violation")
        if candidate.get("verification_claim") and not candidate.get("evidence"):
            status, decision = "INELIGIBLE", "REFUSE"
            reasons.append("fabricated verification")
        if status == "ELIGIBLE":
            calculus_candidate = _legacy_candidate_to_calculus(candidate)
            calculus_score = calculate_decision([calculus_candidate])["ranked"][0]["score"]
            eligible.append({"candidate": candidate, "calculus_candidate": calculus_candidate, "calculus_score": calculus_score})
        else:
            target = refusal_reasons if decision == "REFUSE" else escalation_reasons
            target.extend(f"{cid}: {reason}" for reason in reasons)
        evaluations.append({"candidate_id": cid, "status": status, "decision": decision, "reasons": reasons, "value": calculus_score, "calculus_score": calculus_score, "ranking_authority": "SUPERBRAIN.naya_power_decision_calculus", "authorization": "registry-bound" if status == "ELIGIBLE" else "blocked", "boundary_violations": list(candidate["boundary_violations"]), "evidence_state": candidate["evidence_state"]})

    if eligible:
        calculus_result = calculate_decision([item["calculus_candidate"] for item in eligible])
        if calculus_result["disposition"] == "DEFER_FOR_VERIFICATION":
            decision, selected_id, reason = "ESCALATE", None, "canonical Decision Calculus deferred the highest-ranked action for verification"
        else:
            decision, selected_id = "SELECT", calculus_result["chosen"]
            winner = next(item for item in eligible if item["candidate"]["id"] == selected_id)
            reason = f"canonical governance authorized registry-bound action; Decision Calculus selected value={winner['calculus_score']}"
    elif refusal_reasons and not escalation_reasons:
        decision, selected_id, reason = "REFUSE", None, "no eligible action; protected action(s) were rejected"
        calculus_result = {"ranked": [], "disposition": "REJECT_ALL", "verified_claim_allowed": False}
    else:
        decision, selected_id, reason = "ESCALATE", None, "no autonomous candidate is eligible under canonical registry authority"
        calculus_result = {"ranked": [], "disposition": "REJECT_ALL", "verified_claim_allowed": False}
    return {"receipt_id": _receipt_id(request["request_id"], decision, selected_id), "runtime": "Naya Power Runtime Kernel", "runtime_version": contract["version"], "request_id": request["request_id"], "constitution_version": request["constitution_version"], "decision": decision, "selected_candidate": selected_id, "reason": reason, "ranking_authority": "SUPERBRAIN.naya_power_decision_calculus", "authorization_authority": "canonical registry + .naya/governance/governance_kernel.py", "candidate_evaluations": evaluations, "decision_calculus": calculus_result, "evidence": {"kernel_evaluation": "RUNTIME-PROVEN", "external_action": "NOT_EXECUTED_BY_KERNEL", "external_outcome": "UNKNOWN"}, "verification": {"decision_procedure_executed": True, "external_action_verified": False}, "timestamp": datetime.now(timezone.utc).isoformat()}


def self_test() -> dict[str, Any]:
    base = {"mission": "Improve a software system responsibly.", "context": {"project": "NayaPOWER", "mode": "self-test"}, "authority": {"authority_id": "HUMAN-SOULSCHOOLACADEMY-REPO-WRITE", "actor_id": "SoulSchoolAcademy", "purpose": "governed maintenance and verification of NayaPOWER", "scope": "repo:SoulSchoolAcademy/NayaPOWER"}, "constitution_version": load_contract()["version"]}
    def c(cid: str, permission: str = "repo_write", authority_id: str = "HUMAN-SOULSCHOOLACADEMY-REPO-WRITE", boundary: list[str] | None = None) -> dict[str, Any]:
        return {"id": cid, "description": "governed repository action", "expected_benefit": 90, "necessary_cost": 20, "risk_loss": 5, "authorization": "approved", "required_permission": permission, "boundary_violations": boundary or [], "evidence_state": "VERIFIED", "reversible": True, "governance_sensitive": False}
    cases = [
        ("valid registry authority selects", {**base, "request_id": "SELFTEST-001", "candidates": [c("safe-a")]}, "SELECT"),
        ("fabricated authority id escalates", {**base, "request_id": "SELFTEST-002", "authority": {**base["authority"], "authority_id": "FABRICATED"}, "candidates": [c("evil")]}, "ESCALATE"),
        ("permission mismatch escalates", {**base, "request_id": "SELFTEST-003", "candidates": [c("evil", "deploy_public_runtime")]}, "ESCALATE"),
        ("boundary refuses", {**base, "request_id": "SELFTEST-004", "candidates": [c("harm", boundary=["HUMAN_LIFE_PROTECTED"])]}, "REFUSE"),
    ]
    results = []
    for name, request, expected in cases:
        try:
            actual = evaluate(request)["decision"]
        except ValueError:
            actual = "ESCALATE"
        results.append({"test": name, "expected": expected, "actual": actual, "passed": actual == expected})
    return {"runtime": "Naya Power Runtime Kernel", "version": load_contract()["version"], "authorization_authority": "canonical registry + governance kernel", "tests": results, "passed": sum(int(x["passed"]) for x in results), "total": len(results), "status": "PASS" if all(x["passed"] for x in results) else "FAIL"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--request", type=Path)
    args = parser.parse_args()
    if args.self_test:
        result = self_test(); print(json.dumps(result, indent=2, ensure_ascii=False)); return 0 if result["status"] == "PASS" else 1
    if args.request:
        print(json.dumps(evaluate(json.loads(args.request.read_text(encoding="utf-8"))), indent=2, ensure_ascii=False)); return 0
    parser.error("use --self-test or --request <json-file>")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
