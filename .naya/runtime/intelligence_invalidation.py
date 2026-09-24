from __future__ import annotations

import copy
import hashlib
import json
from typing import Any

PLAN_SCHEMA = "NAYAPOWER_DERIVED_INTELLIGENCE_REVALIDATION_PLAN_V1"
BATCH_SCHEMA = "NAYAPOWER_INTELLIGENCE_INVALIDATION_BATCH_V1"
RECEIPT_SCHEMA = "NAYAPOWER_INTELLIGENCE_INVALIDATION_RECEIPT_V1"
ACTIONS = ("INVALIDATE", "RECHECK", "RECALCULATE", "SUPERSEDE")
RECHECK_OUTCOMES = {"CONFIRMED", "NEEDS_RECALCULATION", "REJECTED", "BLOCKED"}
TERMINAL_RECHECK_OUTCOMES = {"CONFIRMED", "NEEDS_RECALCULATION", "REJECTED"}


class InvalidationError(ValueError):
    pass


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest_value(value: Any) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()


def require_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InvalidationError(f"{field} is required")
    return value.strip()


def require_digest(value: Any, field: str) -> str:
    text = require_text(value, field).lower()
    if len(text) != 64 or any(character not in "0123456789abcdef" for character in text):
        raise InvalidationError(f"{field} must be a SHA-256 hex digest")
    return text


def require_refs(values: Any, field: str) -> list[str]:
    if not isinstance(values, list) or not values:
        raise InvalidationError(f"{field} must contain at least one reference")
    refs = [require_text(value, field) for value in values]
    if len(refs) != len(set(refs)):
        raise InvalidationError(f"{field} must not contain duplicate references")
    return sorted(refs)


def record_status(record: dict[str, Any]) -> str:
    lifecycle = record.get("lifecycle") if isinstance(record.get("lifecycle"), dict) else {}
    truth = record.get("truth") if isinstance(record.get("truth"), dict) else {}
    verification = record.get("verification") if isinstance(record.get("verification"), dict) else {}
    return str(lifecycle.get("stage") or truth.get("state") or verification.get("status") or record.get("status") or "UNKNOWN")


class IntelligenceInvalidationRun:
    def __init__(
        self,
        plan: dict[str, Any],
        records: dict[str, dict[str, Any]],
        *,
        authority_ref: str,
        invalidator_id: str,
        reason: str,
        evidence_refs: list[str],
        idempotency_key: str,
    ) -> None:
        if plan.get("schema") != PLAN_SCHEMA or plan.get("mode") != "PLAN_ONLY":
            raise InvalidationError("System 45 PLAN_ONLY evidence is required")
        if plan.get("status") != "COMPLETE":
            raise InvalidationError("partial or empty revalidation plans cannot authorize invalidation")
        if plan.get("system46_actions_invoked") != []:
            raise InvalidationError("System 45 plan already contains System 46 actions")
        candidate_ids = plan.get("impacted_derived_intelligence_ids")
        if not isinstance(candidate_ids, list) or not candidate_ids:
            raise InvalidationError("revalidation plan contains no candidates")
        self.candidate_ids = sorted(require_text(value, "candidate id") for value in candidate_ids)
        if len(self.candidate_ids) != len(set(self.candidate_ids)):
            raise InvalidationError("revalidation plan contains duplicate candidates")
        missing = [candidate_id for candidate_id in self.candidate_ids if candidate_id not in records]
        if missing:
            raise InvalidationError("candidate records missing: " + ", ".join(missing))
        self.plan = copy.deepcopy(plan)
        self.plan_sha256 = digest_value(plan)
        self.records = {candidate_id: copy.deepcopy(records[candidate_id]) for candidate_id in self.candidate_ids}
        self.authority_ref = require_text(authority_ref, "authority_ref")
        self.invalidator_id = require_text(invalidator_id, "invalidator_id")
        self.reason = require_text(reason, "reason")
        self.evidence_refs = require_refs(evidence_refs, "evidence_refs")
        self.idempotency_key = require_text(idempotency_key, "idempotency_key")
        self.stage = "INVALIDATE"
        self.states = {
            candidate_id: {
                "id": candidate_id,
                "original_status": record_status(self.records[candidate_id]),
                "working_status": record_status(self.records[candidate_id]),
                "invalidation": None,
                "recheck": None,
                "recalculation": None,
                "supersession": None,
            }
            for candidate_id in self.candidate_ids
        }
        self.receipts: list[dict[str, Any]] = []

    def _append_receipt(self, action: str, candidate_ids: list[str], details: dict[str, Any]) -> dict[str, Any]:
        if action not in ACTIONS or self.stage != action:
            raise InvalidationError(f"invalid System 46 action order at {action}")
        previous = self.receipts[-1]["receipt_sha256"] if self.receipts else None
        receipt = {
            "schema": RECEIPT_SCHEMA,
            "sequence": len(self.receipts),
            "action": action,
            "plan_sha256": self.plan_sha256,
            "authority_ref": self.authority_ref,
            "idempotency_key": self.idempotency_key,
            "candidate_ids": sorted(candidate_ids),
            "previous_receipt_sha256": previous,
            "details": copy.deepcopy(details),
        }
        receipt["receipt_sha256"] = digest_value(receipt)
        self.receipts.append(receipt)
        return copy.deepcopy(receipt)

    def _require_stage(self, expected: str) -> None:
        if self.stage != expected:
            raise InvalidationError(f"System 46 requires {expected}; current stage is {self.stage}")

    def invalidate(self) -> dict[str, Any]:
        self._require_stage("INVALIDATE")
        for candidate_id in self.candidate_ids:
            state = self.states[candidate_id]
            state["working_status"] = "STALE"
            state["invalidation"] = {
                "state": "INVALIDATED",
                "reason": self.reason,
                "authority_ref": self.authority_ref,
                "invalidator_id": self.invalidator_id,
                "evidence_refs": list(self.evidence_refs),
                "plan_sha256": self.plan_sha256,
            }
        receipt = self._append_receipt(
            "INVALIDATE",
            self.candidate_ids,
            {
                "resulting_status": "STALE",
                "canonical_records_modified": False,
                "persistence_performed": False,
            },
        )
        self.stage = "RECHECK"
        return receipt

    def recheck(self, results: dict[str, dict[str, Any]]) -> dict[str, Any]:
        self._require_stage("RECHECK")
        if set(results) != set(self.candidate_ids):
            raise InvalidationError("recheck results must match candidate IDs exactly")
        for candidate_id in self.candidate_ids:
            result = results[candidate_id]
            if not isinstance(result, dict):
                raise InvalidationError(f"recheck result missing for {candidate_id}")
            outcome = str(result.get("outcome") or "")
            if outcome not in RECHECK_OUTCOMES:
                raise InvalidationError(f"invalid recheck outcome for {candidate_id}")
            verifier_id = require_text(result.get("verifier_id"), "verifier_id")
            if verifier_id == self.invalidator_id:
                raise InvalidationError("recheck verifier must differ from invalidator")
            state = self.states[candidate_id]
            state["recheck"] = {
                "outcome": outcome,
                "verifier_id": verifier_id,
                "evidence_refs": require_refs(result.get("evidence_refs"), "recheck evidence_refs"),
                "verification_record_ref": require_text(
                    result.get("verification_record_ref"),
                    "verification_record_ref",
                ),
            }
            if outcome == "CONFIRMED":
                state["working_status"] = state["original_status"]
            else:
                state["working_status"] = "STALE"
        receipt = self._append_receipt(
            "RECHECK",
            self.candidate_ids,
            {
                "outcomes": {candidate_id: self.states[candidate_id]["recheck"]["outcome"] for candidate_id in self.candidate_ids},
                "canonical_records_modified": False,
                "persistence_performed": False,
            },
        )
        self.stage = "RECALCULATE"
        return receipt

    def _recalculation_ids(self) -> list[str]:
        return [
            candidate_id
            for candidate_id in self.candidate_ids
            if self.states[candidate_id]["recheck"]["outcome"] in {"NEEDS_RECALCULATION", "REJECTED"}
        ]

    def recalculate(self, results: dict[str, dict[str, Any]]) -> dict[str, Any]:
        self._require_stage("RECALCULATE")
        required_ids = self._recalculation_ids()
        if set(results) != set(required_ids):
            raise InvalidationError("recalculation results must match candidates requiring recalculation")
        successors = set()
        for candidate_id in required_ids:
            result = results[candidate_id]
            if not isinstance(result, dict):
                raise InvalidationError(f"recalculation result missing for {candidate_id}")
            recalculator_id = require_text(result.get("recalculator_id"), "recalculator_id")
            if recalculator_id == self.invalidator_id:
                raise InvalidationError("recalculator must differ from invalidator")
            calculation_id = require_text(result.get("calculation_id"), "calculation_id")
            successor_id = f"{candidate_id}:recalculated:{calculation_id}"
            if successor_id in successors:
                raise InvalidationError("recalculation successor collision")
            successors.add(successor_id)
            self.states[candidate_id]["recalculation"] = {
                "state": "RECALCULATION_PROPOSED",
                "calculation_id": calculation_id,
                "successor_id": successor_id,
                "successor_content_sha256": require_digest(
                    result.get("successor_content_sha256"),
                    "successor_content_sha256",
                ),
                "derivation_receipt_ref": require_text(
                    result.get("derivation_receipt_ref"),
                    "derivation_receipt_ref",
                ),
                "recalculator_id": recalculator_id,
                "evidence_refs": require_refs(result.get("evidence_refs"), "recalculation evidence_refs"),
                "persistence_performed": False,
            }
        receipt = self._append_receipt(
            "RECALCULATE",
            required_ids,
            {
                "successor_ids": sorted(successors),
                "successor_state": "CANDIDATE",
                "canonical_records_modified": False,
                "persistence_performed": False,
            },
        )
        self.stage = "SUPERSEDE"
        return receipt

    def _supersession_ids(self) -> list[str]:
        return [candidate_id for candidate_id in self.candidate_ids if self.states[candidate_id]["recalculation"] is not None]

    def supersede(self, results: dict[str, dict[str, Any]]) -> dict[str, Any]:
        self._require_stage("SUPERSEDE")
        required_ids = self._supersession_ids()
        if set(results) != set(required_ids):
            raise InvalidationError("supersession results must match recalculated candidates")
        for candidate_id in required_ids:
            result = results[candidate_id]
            if not isinstance(result, dict):
                raise InvalidationError(f"supersession result missing for {candidate_id}")
            if require_text(result.get("authority_ref"), "authority_ref") != self.authority_ref:
                raise InvalidationError("supersession authority does not match invalidation authority")
            recalculation = self.states[candidate_id]["recalculation"]
            self.states[candidate_id]["supersession"] = {
                "state": "SUPERSESSION_PROPOSED",
                "predecessor_id": candidate_id,
                "successor_id": recalculation["successor_id"],
                "predecessor_proposed_status": "SUPERSEDED",
                "successor_proposed_status": "CANDIDATE",
                "history_preserved": True,
                "authority_ref": self.authority_ref,
                "evidence_refs": require_refs(result.get("evidence_refs"), "supersession evidence_refs"),
                "supersession_receipt_ref": require_text(
                    result.get("supersession_receipt_ref"),
                    "supersession_receipt_ref",
                ),
                "persistence_performed": False,
            }
        receipt = self._append_receipt(
            "SUPERSEDE",
            required_ids,
            {
                "proposals": [copy.deepcopy(self.states[candidate_id]["supersession"]) for candidate_id in required_ids],
                "history_preserved": True,
                "canonical_records_modified": False,
                "persistence_performed": False,
            },
        )
        self.stage = "COMPLETE"
        return receipt

    def export(self) -> dict[str, Any]:
        blocked = [
            candidate_id
            for candidate_id in self.candidate_ids
            if self.states[candidate_id]["recheck"] is not None
            and self.states[candidate_id]["recheck"]["outcome"] == "BLOCKED"
        ]
        return {
            "schema": BATCH_SCHEMA,
            "status": "BLOCKED" if blocked else "PROPOSALS_READY" if self.stage == "COMPLETE" else "IN_PROGRESS",
            "mode": "PROPOSAL_ONLY",
            "plan_sha256": self.plan_sha256,
            "authority_ref": self.authority_ref,
            "idempotency_key": self.idempotency_key,
            "candidate_ids": list(self.candidate_ids),
            "states": [copy.deepcopy(self.states[candidate_id]) for candidate_id in self.candidate_ids],
            "receipts": copy.deepcopy(self.receipts),
            "blocked_candidate_ids": blocked,
            "persistence_performed": False,
            "canonical_records_modified": False,
            "truth_boundary": "This batch proposes invalidation, recheck, recalculation, and supersession transitions only. It does not persist, invalidate, restore, recalculate, or supersede canonical intelligence.",
        }


def validate_batch(batch: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if batch.get("schema") != BATCH_SCHEMA or batch.get("mode") != "PROPOSAL_ONLY":
        return ["invalidation batch schema or mode"]
    if batch.get("persistence_performed") is not False or batch.get("canonical_records_modified") is not False:
        errors.append("proposal-only boundary is invalid")
    receipts = batch.get("receipts")
    if not isinstance(receipts, list) or not receipts:
        return errors + ["receipts are required"]
    previous = None
    last_action_index = -1
    for index, receipt in enumerate(receipts):
        if receipt.get("schema") != RECEIPT_SCHEMA or receipt.get("sequence") != index:
            errors.append(f"receipt {index} schema or sequence is invalid")
        action = receipt.get("action")
        if action not in ACTIONS:
            errors.append(f"receipt {index} action is invalid")
        else:
            action_index = ACTIONS.index(action)
            if action_index < last_action_index:
                errors.append(f"receipt {index} action order is invalid")
            last_action_index = action_index
        if receipt.get("previous_receipt_sha256") != previous:
            errors.append(f"receipt {index} previous digest is invalid")
        if receipt.get("plan_sha256") != batch.get("plan_sha256"):
            errors.append(f"receipt {index} plan digest is invalid")
        details = receipt.get("details")
        if not isinstance(details, dict) or details.get("persistence_performed") is not False or details.get("canonical_records_modified") is not False:
            errors.append(f"receipt {index} proposal-only detail is invalid")
        recorded = receipt.get("receipt_sha256")
        material = {key: value for key, value in receipt.items() if key != "receipt_sha256"}
        if recorded != digest_value(material):
            errors.append(f"receipt {index} digest is invalid")
        previous = recorded
    blocked = batch.get("blocked_candidate_ids")
    status = batch.get("status")
    if blocked and status != "BLOCKED":
        errors.append("blocked batch status is invalid")
    if not blocked and status not in {"IN_PROGRESS", "PROPOSALS_READY"}:
        errors.append("unblocked batch status is invalid")
    return errors
