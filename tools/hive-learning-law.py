#!/usr/bin/env python3
"""Fail-closed machine contract for governed lesson promotion and adoption.

This module does not store lessons or calculate decision value. It validates
learning evidence and emits deterministic reports over supplied canonical
records. The existing Smart Note registry/receipt remains the source of truth.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

SCHEMA = "naya.hive-learning-law.v1"
SURPRISE_SCHEMA = "naya.surprise-signal.v1"
REQUIRED_LESSON_FIELDS = (
    "lesson_id", "source_ref", "essence", "why_it_matters",
    "applicability", "evidence_refs", "behavioral_probe",
)
HASH_LEN = 64

class LawViolation(ValueError):
    pass

def canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def verify_byte_integrity(law_path: str | Path, manifest_path: str | Path) -> dict:
    """Refuse to run when law bytes do not match the separately pinned digest."""
    law = Path(law_path)
    manifest = Path(manifest_path)
    if not law.is_file() or not manifest.is_file():
        raise LawViolation("LAW_INTEGRITY_INPUT_MISSING")
    expected = manifest.read_text(encoding="ascii").strip().split()[0].lower()
    if len(expected) != HASH_LEN or any(c not in "0123456789abcdef" for c in expected):
        raise LawViolation("LAW_INTEGRITY_MANIFEST_INVALID")
    actual = sha256_bytes(law.read_bytes())
    if actual != expected:
        raise LawViolation("LAW_BYTE_INTEGRITY_MISMATCH")
    return {"status": "PASS", "algorithm": "sha256", "expected": expected, "actual": actual}

def _nonempty(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return bool(value) and all(_nonempty(x) for x in value)
    if isinstance(value, dict):
        return bool(value)
    return value is not None

def validate_lesson(lesson: dict, existing_lessons: list[dict] | None = None) -> dict:
    """Validate seven required fields, specific falsifier, and duplicate identity/content."""
    if not isinstance(lesson, dict):
        raise LawViolation("LESSON_MUST_BE_OBJECT")
    missing = [key for key in REQUIRED_LESSON_FIELDS if not _nonempty(lesson.get(key))]
    if missing:
        raise LawViolation("LESSON_REQUIRED_FIELDS_MISSING:" + ",".join(missing))
    falsifier = lesson.get("falsifier")
    if not isinstance(falsifier, dict):
        raise LawViolation("LESSON_SPECIFIC_FALSIFIER_REQUIRED")
    if not _nonempty(falsifier.get("condition")) or not _nonempty(falsifier.get("observable_failure")):
        raise LawViolation("LESSON_SPECIFIC_FALSIFIER_INCOMPLETE")
    if not _nonempty(falsifier.get("measurement")):
        raise LawViolation("LESSON_FALSIFIER_MEASUREMENT_REQUIRED")
    lesson_id = str(lesson["lesson_id"]).strip().casefold()
    digest = sha256_bytes(canonical_json({k: v for k, v in lesson.items() if k not in {"created_at", "updated_at", "receipt", "lesson_id"}}))
    for old in existing_lessons or []:
        if not isinstance(old, dict):
            raise LawViolation("DUPLICATE_SCAN_CONTAINS_INVALID_RECORD")
        old_id = str(old.get("lesson_id") or "").strip().casefold()
        old_digest = sha256_bytes(canonical_json({k: v for k, v in old.items() if k not in {"created_at", "updated_at", "receipt", "lesson_id"}}))
        if old_id and old_id == lesson_id:
            raise LawViolation("DUPLICATE_LESSON_ID")
        if old_digest == digest:
            raise LawViolation("DUPLICATE_LESSON_CONTENT")
    return {"status": "PASS", "lesson_id": lesson["lesson_id"], "content_sha256": digest,
            "required_fields": list(REQUIRED_LESSON_FIELDS), "falsifier_verified": True,
            "duplicate_scan": "PASS"}

def validate_adoption(record: dict) -> dict:
    """Adoption counts only with canonical retrieval + independent behavior/outcome evidence."""
    required = ("lesson_id", "canonical_lesson_ref", "retrieval_receipt_id", "task_id",
                "control_behavior_hash", "treatment_behavior_hash", "outcome_evidence_ref",
                "independent_verifier", "verification_receipt_id", "cold_successor_ref")
    missing = [k for k in required if not _nonempty(record.get(k))]
    if missing:
        raise LawViolation("ADOPTION_EVIDENCE_MISSING:" + ",".join(missing))
    if record["control_behavior_hash"] == record["treatment_behavior_hash"]:
        raise LawViolation("ADOPTION_NO_BEHAVIOR_DELTA")
    if record.get("independent_verifier") == record.get("actor"):
        raise LawViolation("ADOPTION_SELF_VERIFICATION_FORBIDDEN")
    if record.get("cold_successor_verified") is not True:
        raise LawViolation("ADOPTION_COLD_SUCCESSOR_NOT_VERIFIED")
    if record.get("outcome_improved") is not True:
        raise LawViolation("ADOPTION_OUTCOME_NOT_IMPROVED")
    return {"status": "PASS", "lesson_id": record["lesson_id"], "adopted": True,
            "behavior_changed": True, "outcome_improved": True, "cold_successor_verified": True}

def velocity_report(events: list[dict], window_size: int = 20, minimum_rate: float = 0.5) -> dict:
    """Measure adoption among eligible verified lesson applications in a bounded event window."""
    if not isinstance(events, list) or window_size < 1 or not 0 <= minimum_rate <= 1:
        raise LawViolation("VELOCITY_INPUT_INVALID")
    window = events[-window_size:]
    eligible = [e for e in window if isinstance(e, dict) and e.get("eligible") is True]
    adopted = [e for e in eligible if e.get("adoption_verified") is True and e.get("outcome_improved") is True]
    rate = (len(adopted) / len(eligible)) if eligible else None
    status = "UNKNOWN" if rate is None else ("DEGRADED" if rate < minimum_rate else "HEALTHY")
    return {"schema": "naya.learning-velocity.v1", "status": status,
            "window_size": window_size, "observed_events": len(window),
            "eligible_applications": len(eligible), "verified_adoptions": len(adopted),
            "adoption_rate": rate, "minimum_rate": minimum_rate,
            "unknown_is_not_zero": True}

def validate_surprise_signal(signal: dict) -> dict:
    required = ("signal_id", "worker_id", "observed_at", "source_ref", "expected", "observed",
                "surprise_type", "impact", "evidence_refs", "proposed_lesson_id")
    if not isinstance(signal, dict):
        raise LawViolation("SURPRISE_SIGNAL_MUST_BE_OBJECT")
    missing = [k for k in required if not _nonempty(signal.get(k))]
    if missing:
        raise LawViolation("SURPRISE_SIGNAL_FIELDS_MISSING:" + ",".join(missing))
    if signal.get("schema") != SURPRISE_SCHEMA:
        raise LawViolation("SURPRISE_SIGNAL_SCHEMA_MISMATCH")
    if signal.get("authority_grant") or signal.get("promote_lesson"):
        raise LawViolation("SURPRISE_SIGNAL_CANNOT_GRANT_AUTHORITY_OR_PROMOTE")
    return {"status": "PASS", "schema": SURPRISE_SCHEMA, "signal_id": signal["signal_id"]}

def validate_learning_promotion(entry: dict, evidence_bundle: list[dict], existing_lessons: list[dict] | None = None) -> dict:
    """Adapter for Smart Note promotion: only learning/lesson entries get the extra law."""
    labels = " ".join(str(entry.get(k) or "") for k in ("category", "topic", "kind", "type", "title")).casefold()
    is_lesson = bool(entry.get("learning_law_required") is True or any(x in labels for x in ("lesson", "learning", "adoption")))
    if not is_lesson:
        return {"status": "NOT_APPLICABLE", "required": False}
    candidates = [e.get("lesson") for e in evidence_bundle if isinstance(e, dict) and isinstance(e.get("lesson"), dict)]
    if len(candidates) != 1:
        raise LawViolation("LEARNING_PROMOTION_REQUIRES_EXACTLY_ONE_LESSON_OBJECT")
    return validate_lesson(candidates[0], existing_lessons)

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="command", required=True)
    p = sub.add_parser("verify-integrity"); p.add_argument("--law", default=__file__); p.add_argument("--manifest", required=True)
    p = sub.add_parser("validate-lesson"); p.add_argument("--lesson", required=True); p.add_argument("--existing", help="JSON file containing an array of existing lesson objects")
    p = sub.add_parser("validate-adoption"); p.add_argument("--record", required=True)
    p = sub.add_parser("velocity"); p.add_argument("--events", required=True); p.add_argument("--window", type=int, default=20); p.add_argument("--minimum-rate", type=float, default=0.5)
    p = sub.add_parser("validate-surprise"); p.add_argument("--signal", required=True)
    args = ap.parse_args(argv)
    try:
        if args.command == "verify-integrity": result = verify_byte_integrity(args.law, args.manifest)
        elif args.command == "validate-lesson": result = validate_lesson(json.loads(Path(args.lesson).read_text(encoding="utf-8")), json.loads(Path(args.existing).read_text(encoding="utf-8")) if args.existing else [])
        elif args.command == "validate-adoption": result = validate_adoption(json.loads(Path(args.record).read_text(encoding="utf-8")))
        elif args.command == "velocity": result = velocity_report(json.loads(Path(args.events).read_text(encoding="utf-8")), args.window, args.minimum_rate)
        else: result = validate_surprise_signal(json.loads(Path(args.signal).read_text(encoding="utf-8")))
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError, LawViolation) as exc:
        print(json.dumps({"status": "BLOCKED", "reason": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result.get("status") in {"PASS", "HEALTHY", "DEGRADED", "UNKNOWN", "NOT_APPLICABLE"} else 2

if __name__ == "__main__":
    raise SystemExit(main())
