#!/usr/bin/env python3
"""Deterministic promotion boundary for Claim -> Evidence -> Verification -> Oscar."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

LEVELS = ["UNVERIFIED", "BUILDER_VERIFIED", "OSCAR_ACCEPTED", "CANONICAL_VERIFIED", "PRODUCTION_SAFE"]
FORBIDDEN_METHODS = {"model_assertion", "memory_assertion", "user_assertion", "retrieved_content"}
PROVENANCE_SCHEMA = "naya-power-oscar-provenance/v1"


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def git_blob_sha(root: Path, relative_path: str) -> str | None:
    try:
        return subprocess.run(["git", "hash-object", relative_path], cwd=root, text=True, capture_output=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def fail(reasons: list[str]) -> dict[str, Any]:
    return {"eligible": False, "level": "UNVERIFIED", "reasons": reasons}


def verify_oscar_provenance(oscar: dict[str, Any], claim: dict[str, Any], evidence: list[dict[str, Any]], current_commit: str, root: Path) -> list[str]:
    reasons: list[str] = []
    provenance = oscar.get("provenance")
    if not isinstance(provenance, dict):
        return ["Oscar provenance is missing"]
    if provenance.get("schema") != PROVENANCE_SCHEMA:
        reasons.append("Oscar provenance schema is invalid")
    claim_sha = sha256_json(claim)
    evidence_sha = sha256_json(sorted(evidence, key=lambda item: str(item.get("evidence_id", ""))))
    input_sha = sha256_json({"claim_sha256": claim_sha, "evidence_sha256": evidence_sha, "expected_commit": current_commit})
    if provenance.get("claim_sha256") != claim_sha:
        reasons.append("Oscar provenance claim hash does not match the supplied claim")
    if provenance.get("evidence_sha256") != evidence_sha:
        reasons.append("Oscar provenance evidence hash does not match the supplied evidence")
    if provenance.get("input_sha256") != input_sha:
        reasons.append("Oscar provenance input fingerprint does not match current inputs")
    if provenance.get("expected_commit") != current_commit:
        reasons.append("Oscar provenance is bound to a different commit")
    implementation_path = provenance.get("implementation_path")
    if implementation_path != ".naya/runtime/oscar.py":
        reasons.append("Oscar implementation path is not canonical")
    actual_implementation_sha = git_blob_sha(root, implementation_path) if implementation_path else None
    if not actual_implementation_sha or provenance.get("implementation_sha256") != actual_implementation_sha:
        reasons.append("Oscar implementation provenance does not match the checked-out implementation")
    if provenance.get("implementation_commit") != current_commit:
        reasons.append("Oscar implementation provenance is from a different commit")
    if provenance.get("execution_source") != "github-actions":
        reasons.append("Oscar execution source is not GitHub Actions")
    run_id = provenance.get("execution_run_id")
    if not run_id:
        reasons.append("Oscar execution provenance is incomplete")
    current_run_id = os.getenv("GITHUB_RUN_ID")
    if current_run_id and str(run_id) != str(current_run_id):
        reasons.append("Oscar evidence was produced by a different CI run")
    unsigned = dict(oscar)
    unsigned.pop("result_sha256", None)
    if oscar.get("result_sha256") != sha256_json(unsigned):
        reasons.append("Oscar result integrity hash does not match the result contents")
    return reasons


def evaluate(package: dict[str, Any], current_commit: str, root: Path | None = None) -> dict[str, Any]:
    reasons: list[str] = []
    root = root or Path(__file__).resolve().parents[2]
    claim = package.get("claim") or {}
    evidence = package.get("evidence") or []
    oscar = package.get("oscar") or {}
    target = package.get("target", "CANONICAL_VERIFIED")
    if target not in LEVELS:
        return fail([f"unknown target level: {target}"])
    if claim.get("status") != "VERIFIED":
        reasons.append("builder verification is not VERIFIED")
    criteria = claim.get("success_criteria")
    if not isinstance(criteria, list) or not criteria:
        reasons.append("claim has no success criteria")
    if not claim.get("claim_id") or not claim.get("source"):
        reasons.append("claim provenance is missing")
    if not evidence:
        reasons.append("qualifying evidence is missing")
    passing, failing = [], []
    for item in evidence:
        if item.get("commit_sha") == current_commit and item.get("result") == "FAIL":
            failing.append(item)
        if item.get("result") != "PASS":
            continue
        if item.get("method") in FORBIDDEN_METHODS:
            continue
        if item.get("commit_sha") != current_commit:
            continue
        if not item.get("source") or not item.get("environment") or not item.get("command") or not item.get("observed_at"):
            continue
        if item.get("superseded_at") is not None or item.get("status") == "SUPERSEDED":
            continue
        passing.append(item)
    if passing and failing:
        reasons.append("conflicting current evidence contains both PASS and FAIL")
    if not passing:
        reasons.append("no current, qualifying, non-superseded PASS evidence with provenance")
    evidence_criteria = set().union(*(set(e.get("criteria_covered") or []) for e in passing)) if passing else set()
    if set(criteria or []) - evidence_criteria:
        reasons.append("qualifying evidence does not cover every success criterion")
    if target in {"OSCAR_ACCEPTED", "CANONICAL_VERIFIED", "PRODUCTION_SAFE"}:
        if oscar.get("verdict") != "ACCEPT":
            reasons.append("Oscar verdict is not ACCEPT")
        if oscar.get("independent") is not True:
            reasons.append("Oscar is not marked independent")
        if oscar.get("promotion_allowed") is not True:
            reasons.append("Oscar did not allow promotion")
        if oscar.get("expected_commit") != current_commit:
            reasons.append("Oscar evidence is bound to a different commit")
        covered = set(oscar.get("criteria_covered") or [])
        if set(criteria or []) - covered:
            reasons.append("Oscar does not cover every success criterion")
        if oscar.get("claim_id") != claim.get("claim_id"):
            reasons.append("Oscar claim_id does not match claim")
        reasons.extend(verify_oscar_provenance(oscar, claim, evidence, current_commit, root))
    if target == "CANONICAL_VERIFIED" and package.get("promotion_decision") != "PROMOTE":
        reasons.append("canonical promotion requires an explicit PROMOTE decision")
    if target == "PRODUCTION_SAFE":
        production = [e for e in passing if e.get("method") == "production_test" and e.get("environment") == "production"]
        if not production:
            reasons.append("PRODUCTION_SAFE requires qualifying production evidence")
        if package.get("promotion_decision") != "PROMOTE":
            reasons.append("production promotion requires an explicit PROMOTE decision")
    if reasons:
        return fail(reasons)
    level = "BUILDER_VERIFIED"
    if target in {"OSCAR_ACCEPTED", "CANONICAL_VERIFIED", "PRODUCTION_SAFE"}:
        level = "OSCAR_ACCEPTED"
    if target == "CANONICAL_VERIFIED":
        level = "CANONICAL_VERIFIED"
    if target == "PRODUCTION_SAFE":
        level = "PRODUCTION_SAFE"
    return {"eligible": True, "level": level, "claim_id": claim["claim_id"], "current_commit": current_commit, "target": target, "passing_evidence": [e["evidence_id"] for e in passing], "promotion_decision": package.get("promotion_decision"), "reasons": []}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("package")
    ap.add_argument("--commit", required=True)
    args = ap.parse_args()
    package = json.loads(Path(args.package).read_text(encoding="utf-8"))
    result = evaluate(package, args.commit)
    print(json.dumps(result, indent=2))
    return 0 if result.get("eligible") else 1


if __name__ == "__main__":
    sys.exit(main())
