"""Evidence-bound gate for capture lifecycle promotion.

This gate is distinct from learning-experiment admission. It allows a CANDIDATE
capture's lifecycle_state to become ACTIVE only after the exact capture is bound
to independently verified persisted-lineage evidence. It does not raise the
epistemic ceiling: automatic_truth_ceiling and persisted understanding_state
must remain CANDIDATE.
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class GateResult:
    admitted: bool
    reason: str


def _is_object(value: Any) -> bool:
    return isinstance(value, dict)


def verify_capture_admission(capture: Any, expected: Any, lineage: Any, proof: Any, *, capture_path: str) -> GateResult:
    """Return a fail-closed verdict; no missing field receives a permissive default."""
    if not all(_is_object(v) for v in (capture, expected, lineage, proof)):
        return GateResult(False, "ALL_EVIDENCE_INPUTS_MUST_BE_OBJECTS")

    lifecycle = capture.get("lifecycle_state")
    if not isinstance(lifecycle, str) or not lifecycle.strip():
        return GateResult(False, "LIFECYCLE_STATE_REQUIRED")
    if lifecycle.strip().upper() != "CANDIDATE":
        return GateResult(False, "LIFECYCLE_STATE_NOT_CANDIDATE")

    capture_id = capture.get("capture_id")
    if not isinstance(capture_id, str) or not capture_id.strip():
        return GateResult(False, "CAPTURE_ID_REQUIRED")
    if expected.get("capture_id") != capture_id:
        return GateResult(False, "CAPTURE_ID_MISMATCH")
    expected_path = expected.get("capture_path")
    if not isinstance(expected_path, str) or Path(expected_path).as_posix() != Path(capture_path).as_posix():
        return GateResult(False, "CAPTURE_PATH_MISMATCH")

    expected_hash = expected.get("content_hash")
    if not isinstance(expected_hash, str) or re.fullmatch(r"[0-9a-f]{64}", expected_hash) is None:
        return GateResult(False, "EXPECTED_CONTENT_HASH_INVALID")
    if not isinstance(expected.get("expected_content"), str) or not expected["expected_content"].strip():
        return GateResult(False, "EXPECTED_CONTENT_REQUIRED")

    ib_id = lineage.get("intelligent_block_id")
    if not isinstance(ib_id, str) or not ib_id.strip():
        return GateResult(False, "INTELLIGENT_BLOCK_ID_REQUIRED")
    if proof.get("schema") != "NAYA_SMART_NOTE_CAPTURE_PROOF_V2":
        return GateResult(False, "PROOF_SCHEMA_MISMATCH")
    if proof.get("intelligent_block_id") != ib_id:
        return GateResult(False, "INTELLIGENT_BLOCK_MISMATCH")
    for key in ("event_id", "receipt_id", "lineage_id", "relationship_id", "index_id", "checkpoint_id"):
        expected_value = lineage.get(key)
        if not isinstance(expected_value, str) or not expected_value.strip():
            return GateResult(False, f"LINEAGE_{key.upper()}_REQUIRED")
        if proof.get(key) != expected_value:
            return GateResult(False, f"LINEAGE_{key.upper()}_MISMATCH")
    if proof.get("content_hash") != expected_hash:
        return GateResult(False, "CONTENT_HASH_MISMATCH")
    if proof.get("independent_lineage_verification") is not True:
        return GateResult(False, "INDEPENDENT_LINEAGE_VERIFICATION_REQUIRED")
    if proof.get("exact_distilled_payload_match") is not True:
        return GateResult(False, "EXACT_DISTILLED_PAYLOAD_MATCH_REQUIRED")
    if proof.get("understanding_state") != "CANDIDATE":
        return GateResult(False, "PERSISTED_UNDERSTANDING_STATE_MUST_REMAIN_CANDIDATE")

    intelligence = capture.get("intelligence")
    machine_view = intelligence.get("machine_view") if _is_object(intelligence) else None
    if not _is_object(machine_view):
        return GateResult(False, "MACHINE_VIEW_REQUIRED")
    if machine_view.get("automatic_truth_ceiling") != "CANDIDATE":
        return GateResult(False, "AUTOMATIC_TRUTH_CEILING_MUST_REMAIN_CANDIDATE")

    return GateResult(True, "ADMIT")


def _load(path: str) -> Any:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--capture", required=True)
    parser.add_argument("--expected", required=True)
    parser.add_argument("--lineage", required=True)
    parser.add_argument("--proof", required=True)
    args = parser.parse_args()
    try:
        result = verify_capture_admission(_load(args.capture), _load(args.expected), _load(args.lineage), _load(args.proof), capture_path=args.capture)
    except (OSError, ValueError, TypeError) as exc:
        print(f"REJECT:EVIDENCE_READ_FAILED:{type(exc).__name__}")
        return 1
    print(result.reason)
    return 0 if result.admitted else 1


if __name__ == "__main__":
    raise SystemExit(main())
