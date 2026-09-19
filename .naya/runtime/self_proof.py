#!/usr/bin/env python3
"""NayaNET Autonomous Self-Proof V1.
Evaluates evidence already produced by canonical system paths.
No second state, event, ledger, or authority system is introduced.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Mapping, Sequence

CONTRACT = "NAYANET_SELF_PROOF_V1"
PASS = "PASS"
FAIL = "FAIL"
NOT_VERIFIED = "NOT_VERIFIED"
OVERALL_SELF_VERIFIED = "SELF_VERIFIED"
OVERALL_LIMITED = "SELF_VERIFIED_WITH_LIMITATIONS"
OVERALL_NOT_VERIFIED = "NOT_VERIFIED"

REQUIRED_CHECKS = (
    "identity", "source", "build", "deployment", "runtime", "connectivity",
    "intelligence", "authority", "execution", "persistence", "lineage",
    "retrieval", "integrity",
)

@dataclass(frozen=True)
class ProofCheck:
    name: str
    status: str
    evidence: tuple[str, ...] = ()
    detail: str = ""
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

def _check(name: str, value: Any, *, evidence: Sequence[str] = (), detail: str = "") -> ProofCheck:
    if isinstance(value, bool):
        status = PASS if value else FAIL
    elif value in {PASS, FAIL, NOT_VERIFIED}:
        status = value
    else:
        status = NOT_VERIFIED
    return ProofCheck(name, status, tuple(str(x) for x in evidence), detail)

def evaluate_self_proof(evidence: Mapping[str, Any], *, observed_at: str | None = None) -> dict[str, Any]:
    checks = []
    for name in REQUIRED_CHECKS:
        item = evidence.get(name)
        if isinstance(item, Mapping):
            checks.append(_check(name, item.get("status"), evidence=item.get("evidence", ()), detail=str(item.get("detail", ""))))
        else:
            checks.append(_check(name, item))
    failed = [c.name for c in checks if c.status == FAIL]
    missing = [c.name for c in checks if c.status == NOT_VERIFIED]
    overall = OVERALL_NOT_VERIFIED if failed else OVERALL_LIMITED if missing else OVERALL_SELF_VERIFIED
    return {
        "contract": CONTRACT,
        "contract_version": "1.0.0",
        "observed_at": observed_at or datetime.now(timezone.utc).isoformat(),
        "overall": overall,
        "checks": [c.to_dict() for c in checks],
        "failed_checks": failed,
        "unverified_checks": missing,
        "truth_rule": "missing evidence never becomes PASS",
    }

def build_durable_self_proof_event(
    proof: Mapping[str, Any], *, event_id: str, claim_id: str, action_id: str,
    decision_id: str, authority_id: str, actor_id: str, receipt_id: str,
    next_action: str, successor: str,
) -> dict[str, Any]:
    checks = proof.get("checks") or []
    evidence = list(dict.fromkeys(str(e) for c in checks for e in (c.get("evidence") or [])))
    overall = proof.get("overall")
    return {
        "event_id": event_id,
        "created_at": str(proof.get("observed_at")),
        "effective_at": str(proof.get("observed_at")),
        "event_type": "activity",
        "status": "VERIFIED_REPOSITORY_RECORD" if overall == OVERALL_SELF_VERIFIED else "SELF_PROOF_RECORDED",
        "subject": f"{CONTRACT} · {overall}",
        "title": f"{CONTRACT} · {overall}",
        "tags": ["activity", "self-proof", "nayanet-self-proof-v1"],
        "execution": {
            "event_id": event_id, "claim_id": claim_id, "action_id": action_id,
            "decision_id": decision_id, "authority_id": authority_id, "actor_id": actor_id,
        },
        "receipt": {"receipt_id": receipt_id, "schema": CONTRACT, "status": "MATCHED", "event_id": event_id},
        "continuity": {
            "execution_state": "COMPLETED",
            "handoff": {"next_action": next_action, "successor": successor},
            "learning_status": "RECORDED",
        },
        "activity_feed_projection": {
            "feed": "NAYA-ACTIVITY", "event_id": event_id,
            "title": f"{CONTRACT} · {overall}",
            "summary": "Autonomous service proof evaluated existing canonical evidence; missing evidence remains explicitly unverified.",
        },
        "verification": {
            "status": "VERIFIED" if overall == OVERALL_SELF_VERIFIED else "LIMITED",
            "method": "nayanet-self-proof-v1", "schema": CONTRACT, "evidence": evidence,
        },
        "self_proof": dict(proof),
        "evidence_ids": evidence,
    }

__all__ = [
    "CONTRACT", "REQUIRED_CHECKS", "PASS", "FAIL", "NOT_VERIFIED",
    "OVERALL_SELF_VERIFIED", "OVERALL_LIMITED", "OVERALL_NOT_VERIFIED",
    "evaluate_self_proof", "build_durable_self_proof_event",
]
