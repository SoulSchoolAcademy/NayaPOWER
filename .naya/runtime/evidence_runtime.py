#!/usr/bin/env python3
"""Deterministic Claim -> Evidence -> Verification runtime for Naya Power."""
from __future__ import annotations
import argparse, json, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = ROOT / ".naya" / "evidence"
CLAIMS_DIR = EVIDENCE_DIR / "claims"
EVIDENCE_STORE = EVIDENCE_DIR / "records"

CLAIM_SCHEMA = "naya-power-claim/v1"
EVIDENCE_SCHEMA = "naya-power-evidence/v1"
CLAIM_STATUSES = {"UNVERIFIED", "VERIFIED", "REJECTED", "SUPERSEDED", "PARTIAL", "BLOCKED"}
RESULTS = {"PASS", "FAIL", "PARTIAL", "UNKNOWN"}
FORBIDDEN_METHODS = {"model_assertion", "memory_assertion", "user_assertion", "retrieved_content"}
REQUIRED_CLAIM = {"schema", "claim_id", "statement", "success_criteria", "created_at", "status", "evidence_ids", "source"}
REQUIRED_EVIDENCE = {"schema", "evidence_id", "claim_id", "observed_at", "method", "command", "observed_output", "result", "commit_sha", "environment", "source"}


def parse_time(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        raise ValueError("timestamp must include timezone")
    return dt.astimezone(timezone.utc)


def git_head() -> str | None:
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def validate_claim(claim: dict[str, Any], evidence_by_id: dict[str, dict[str, Any]], expected_commit: str | None = None) -> list[str]:
    errors: list[str] = []
    missing = REQUIRED_CLAIM - set(claim)
    if missing:
        errors.append(f"claim {claim.get('claim_id', '<unknown>')}: missing {sorted(missing)}")
        return errors
    if claim.get("schema") != CLAIM_SCHEMA:
        errors.append(f"claim {claim['claim_id']}: invalid schema")
    if claim.get("status") not in CLAIM_STATUSES:
        errors.append(f"claim {claim['claim_id']}: invalid status")
    if not isinstance(claim.get("success_criteria"), list) or not claim["success_criteria"]:
        errors.append(f"claim {claim['claim_id']}: success_criteria must be non-empty list")
    if not isinstance(claim.get("evidence_ids"), list):
        errors.append(f"claim {claim['claim_id']}: evidence_ids must be a list")
    try:
        parse_time(claim["created_at"])
    except Exception as exc:
        errors.append(f"claim {claim['claim_id']}: invalid created_at: {exc}")

    evidence = []
    for eid in claim.get("evidence_ids", []):
        item = evidence_by_id.get(eid)
        if item is None:
            errors.append(f"claim {claim['claim_id']}: missing evidence {eid}")
        else:
            evidence.append(item)
            if item.get("claim_id") != claim["claim_id"]:
                errors.append(f"claim {claim['claim_id']}: evidence {eid} points to another claim")

    if claim.get("status") == "VERIFIED":
        if not evidence:
            errors.append(f"claim {claim['claim_id']}: VERIFIED requires evidence")
        for item in evidence:
            errors.extend(validate_evidence(item, expected_commit=expected_commit))
        passing = [e for e in evidence if e.get("result") == "PASS"]
        if not passing:
            errors.append(f"claim {claim['claim_id']}: VERIFIED requires at least one PASS evidence record")
    return errors


def validate_evidence(evidence: dict[str, Any], expected_commit: str | None = None) -> list[str]:
    errors: list[str] = []
    eid = evidence.get("evidence_id", "<unknown>")
    missing = REQUIRED_EVIDENCE - set(evidence)
    if missing:
        return [f"evidence {eid}: missing {sorted(missing)}"]
    if evidence.get("schema") != EVIDENCE_SCHEMA:
        errors.append(f"evidence {eid}: invalid schema")
    if evidence.get("result") not in RESULTS:
        errors.append(f"evidence {eid}: invalid result")
    if evidence.get("method") in FORBIDDEN_METHODS:
        errors.append(f"evidence {eid}: method {evidence['method']} cannot establish evidence")
    if not evidence.get("command"):
        errors.append(f"evidence {eid}: command is required")
    if not str(evidence.get("observed_output", "")).strip():
        errors.append(f"evidence {eid}: observed_output is required")
    if not str(evidence.get("commit_sha", "")).strip():
        errors.append(f"evidence {eid}: commit_sha is required")
    try:
        parse_time(evidence["observed_at"])
    except Exception as exc:
        errors.append(f"evidence {eid}: invalid observed_at: {exc}")
    if expected_commit and evidence.get("commit_sha") != expected_commit:
        errors.append(f"evidence {eid}: commit_sha {evidence.get('commit_sha')} does not match expected {expected_commit}")
    return errors


def verify_claim(claim: dict[str, Any], evidence_by_id: dict[str, dict[str, Any]], expected_commit: str | None = None) -> dict[str, Any]:
    errors = validate_claim(claim, evidence_by_id, expected_commit)
    evidence = [evidence_by_id[eid] for eid in claim.get("evidence_ids", []) if eid in evidence_by_id]
    passing = [e for e in evidence if e.get("result") == "PASS" and not validate_evidence(e, expected_commit)]
    status = "VERIFIED" if not errors and claim.get("status") == "VERIFIED" and passing else ("REJECTED" if errors else "UNVERIFIED")
    return {"claim_id": claim.get("claim_id"), "status": status, "errors": errors, "evidence_count": len(evidence), "passing_evidence": [e["evidence_id"] for e in passing]}


def load_store() -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]], list[str]]:
    claims: dict[str, dict[str, Any]] = {}
    evidence: dict[str, dict[str, Any]] = {}
    errors: list[str] = []
    for p in sorted(CLAIMS_DIR.glob("*.json")):
        try:
            item = json.loads(p.read_text(encoding="utf-8")); claims[item["claim_id"]] = item
        except Exception as exc: errors.append(f"{p}: {exc}")
    for p in sorted(EVIDENCE_STORE.glob("*.json")):
        try:
            item = json.loads(p.read_text(encoding="utf-8")); evidence[item["evidence_id"]] = item
        except Exception as exc: errors.append(f"{p}: {exc}")
    return claims, evidence, errors


def validate_store(expected_commit: str | None = None) -> list[str]:
    claims, evidence, errors = load_store()
    for item in evidence.values():
        errors.extend(validate_evidence(item, expected_commit=None))
    for item in claims.values():
        errors.extend(validate_claim(item, evidence, expected_commit=expected_commit))
    return errors


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("validate"); v.add_argument("--commit", default=None)
    r = sub.add_parser("verify"); r.add_argument("claim_id"); r.add_argument("--commit", default=None)
    args = ap.parse_args()
    if args.cmd == "validate":
        expected = args.commit or git_head()
        errors = validate_store(expected_commit=expected)
        if errors:
            print("FAIL"); print("\n".join(f"- {e}" for e in errors)); return 1
        print("PASS — Claim/Evidence store is structurally valid")
        return 0
    claims, evidence, errors = load_store()
    if errors or args.claim_id not in claims:
        print(json.dumps({"status":"REJECTED","errors":errors+[f"claim not found: {args.claim_id}"]}, indent=2)); return 1
    result = verify_claim(claims[args.claim_id], evidence, args.commit or git_head())
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "VERIFIED" else 1

if __name__ == "__main__": sys.exit(main())
