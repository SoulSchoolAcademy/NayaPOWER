#!/usr/bin/env python3
"""Validate BRAIN/07-LEARNING/0002-LEARNING-RECORD-LIFECYCLE-V1.json.

Fail-closed rules (UNKNOWN != PASS):
  - stage claims are only honored when the evidence the stage's gate requires
    is present; missing evidence -> the stage claim is rejected.
  - stage_history must equal stages[0..index(stage)] exactly: forward-only,
    one stage at a time, no skips, no backward moves.
  - no fractional/manufactured stages: stage must be exactly one of the
    seven pipeline stages from the contract V1 pipeline.
  - CONTRADICTED records must name contradicted_by and be preserved=true
    (contradiction is a verdict, never an erasure).
  - REJECTED records must name a rejection_reason.
  - COMPOUND requires measured behavioral effect; CANDIDATE requires
    explicit applicability conditions.
  - authority_check.changes_authority must be false at ADOPT and beyond:
    learning never changes authority; authority claims are rejected.
  - status must remain PROPOSED_CANONICAL until human-director ratification;
    CANONICAL is rejected here.
Usage: python3 tools/validate_learning_record_lifecycle.py
Exit 0 when the lifecycle file is internally consistent and evidence-bound.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "BRAIN/07-LEARNING/0002-LEARNING-RECORD-LIFECYCLE-V1.json"

SCHEMA = "naya.learning-record-lifecycle.v1"
ALLOWED_STATUSES = {"PROPOSED_CANONICAL"}
STAGES = ["OBSERVE", "RECONCILE", "CANDIDATE", "VERIFY", "ADOPT", "MEASURE", "COMPOUND"]
OUTCOMES = {"ACTIVE", "CONTRADICTED", "REJECTED"}
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def _nonempty_str(value):
    return isinstance(value, str) and bool(value.strip())


def _nonempty_str_list(value):
    return (
        isinstance(value, list)
        and bool(value)
        and all(_nonempty_str(v) for v in value)
    )


def _record_failures(rid, record):
    out = []
    stage = record.get("stage")
    if stage not in STAGES:
        out.append(f"{rid}: STAGE_INVALID: {stage!r} not in pipeline stages")
        return out
    outcome = record.get("outcome", "ACTIVE")
    if outcome not in OUTCOMES:
        out.append(f"{rid}: OUTCOME_INVALID: {outcome!r}")
    idx = STAGES.index(stage)
    expected_history = STAGES[: idx + 1]
    if record.get("stage_history") != expected_history:
        out.append(
            f"{rid}: STAGE_HISTORY_INVALID: {record.get('stage_history')!r} "
            f"!= {expected_history!r} (forward-only, no skips, no backward)"
        )
    gates = STAGES[: idx + 1]
    if "OBSERVE" in gates and not _nonempty_str(record.get("observation_ref")):
        out.append(f"{rid}: OBSERVE_EVIDENCE_MISSING: observation_ref required")
    if "RECONCILE" in gates and not _nonempty_str(record.get("reconciliation_note")):
        out.append(f"{rid}: RECONCILE_EVIDENCE_MISSING: reconciliation_note required")
    if "CANDIDATE" in gates and not _nonempty_str_list(record.get("applicability_conditions")):
        out.append(
            f"{rid}: CANDIDATE_EVIDENCE_MISSING: applicability_conditions "
            "must be a non-empty list of non-empty strings"
        )
    if "VERIFY" in gates and not _nonempty_str_list(record.get("verification_evidence")):
        out.append(
            f"{rid}: VERIFY_EVIDENCE_MISSING: verification_evidence "
            "must be a non-empty list of non-empty strings"
        )
    if "ADOPT" in gates:
        if not _nonempty_str(record.get("adoption_record")):
            out.append(f"{rid}: ADOPT_EVIDENCE_MISSING: adoption_record required")
        authority = record.get("authority_check")
        if not isinstance(authority, dict) or authority.get("changes_authority") is not False:
            out.append(
                f"{rid}: AUTHORITY_CLAIM_REJECTED: authority_check.changes_authority "
                "must be false — learning never changes authority"
            )
    if "MEASURE" in gates:
        effect = record.get("behavioral_effect")
        if (
            not isinstance(effect, dict)
            or effect.get("measured") is not True
            or not _nonempty_str(effect.get("before"))
            or not _nonempty_str(effect.get("after"))
        ):
            out.append(
                f"{rid}: MEASURE_EVIDENCE_MISSING: behavioral_effect must have "
                "measured == true and non-empty before/after"
            )
    if "COMPOUND" in gates and not _nonempty_str(record.get("compounding_record")):
        out.append(f"{rid}: COMPOUND_EVIDENCE_MISSING: compounding_record required")
    if outcome == "CONTRADICTED":
        if not _nonempty_str(record.get("contradicted_by")):
            out.append(f"{rid}: CONTRADICTION_NOT_PRESERVED: contradicted_by required")
        if record.get("preserved") is not True:
            out.append(
                f"{rid}: CONTRADICTION_NOT_PRESERVED: contradicted records must "
                "be preserved (preserved == true), never deleted"
            )
    if outcome == "REJECTED" and not _nonempty_str(record.get("rejection_reason")):
        out.append(f"{rid}: REJECTION_REASON_MISSING: rejection_reason required")
    return out


def failures(data):
    out = []
    if data.get("schema") != SCHEMA:
        out.append(f"SCHEMA_MISMATCH: {data.get('schema')!r} != {SCHEMA!r}")
    if data.get("status") not in ALLOWED_STATUSES:
        out.append(
            f"STATUS_NOT_PROPOSED_CANONICAL: {data.get('status')!r} "
            "(CANONICAL requires human-director ratification)"
        )
    if data.get("stages") != STAGES:
        out.append(
            f"STAGE_ORDER_MISMATCH: {data.get('stages')!r} != {STAGES!r} "
            "(pipeline is fixed by the contract V1)"
        )
    if not SHA_RE.match(str(data.get("as_of") or "")):
        out.append(f"AS_OF_NOT_PINNED_SHA: {data.get('as_of')!r}")
    records = data.get("records")
    if not isinstance(records, list):
        out.append("RECORDS_NOT_A_LIST")
        return out
    seen = set()
    for i, record in enumerate(records):
        if not isinstance(record, dict):
            out.append(f"RECORD_{i}_NOT_AN_OBJECT")
            continue
        rid = record.get("record_id")
        if not _nonempty_str(rid):
            out.append(f"RECORD_{i}: RECORD_ID_MISSING")
            rid = f"RECORD_{i}"
        if rid in seen:
            out.append(f"{rid}: RECORD_ID_DUPLICATE")
        seen.add(rid)
        out.extend(_record_failures(rid, record))
    return out


def main() -> int:
    try:
        data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    except Exception as exc:  # fail closed on unreadable fixture
        print(json.dumps({"schema": "naya.learning-record-lifecycle.validation-report",
                          "failures": [f"FIXTURE_UNREADABLE: {exc}"],
                          "passed": False}, indent=2))
        return 1
    fails = failures(data)
    print(json.dumps({"schema": "naya.learning-record-lifecycle.validation-report",
                      "as_of": data.get("as_of"), "failures": fails,
                      "passed": not fails}, indent=2))
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
