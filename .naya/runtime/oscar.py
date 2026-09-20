#!/usr/bin/env python3
"""Independent adversarial Claim/Evidence challenger for Naya Power."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA = "naya-power-oscar/v1"
PROVENANCE_SCHEMA = "naya-power-oscar-provenance/v1"
FORBIDDEN_METHODS = {"model_assertion", "memory_assertion", "user_assertion", "retrieved_content"}
VALID_RESULTS = {"PASS", "FAIL", "PARTIAL", "UNKNOWN"}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def git_head(root: Path) -> str | None:
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, text=True, capture_output=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def git_blob_sha(path: Path, root: Path) -> str | None:
    try:
        return subprocess.run(["git", "hash-object", str(path.relative_to(root))], cwd=root, text=True, capture_output=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError, ValueError):
        return None


def parse_time(value: str) -> bool:
    try:
        raw = value[:-1] + "+00:00" if value.endswith("Z") else value
        dt = datetime.fromisoformat(raw)
        return dt.tzinfo is not None
    except Exception:
        return False


def input_fingerprints(claim: dict[str, Any], evidence: list[dict[str, Any]], expected_commit: str | None) -> dict[str, str | None]:
    evidence_sorted = sorted(evidence, key=lambda item: str(item.get("evidence_id", "")))
    claim_sha = sha256_json(claim)
    evidence_sha = sha256_json(evidence_sorted)
    input_sha = sha256_json({"claim_sha256": claim_sha, "evidence_sha256": evidence_sha, "expected_commit": expected_commit})
    return {"claim_sha256": claim_sha, "evidence_sha256": evidence_sha, "input_sha256": input_sha}


def challenge(claim: dict[str, Any], evidence: list[dict[str, Any]], expected_commit: str | None = None, protected_baseline: str | None = None) -> dict[str, Any]:
    """Independently challenge a verification package; never imports evidence_runtime."""
    reasons: list[str] = []
    warnings: list[str] = []
    criteria = claim.get("success_criteria")

    if claim.get("status") != "VERIFIED":
        reasons.append("claim is not presented as VERIFIED")
    if not isinstance(criteria, list) or not criteria:
        reasons.append("success_criteria must be a non-empty list")
    if not evidence:
        reasons.append("no evidence records supplied")

    covered: set[str] = set()
    passing = 0
    for item in evidence:
        method = item.get("method")
        if method in FORBIDDEN_METHODS:
            reasons.append(f"forbidden evidence method: {method}")
        if item.get("result") != "PASS":
            reasons.append(f"evidence {item.get('evidence_id', '<unknown>')} is not PASS")
        else:
            passing += 1
        if item.get("claim_id") != claim.get("claim_id"):
            reasons.append(f"evidence {item.get('evidence_id', '<unknown>')} targets a different claim")
        if not item.get("command"):
            reasons.append(f"evidence {item.get('evidence_id', '<unknown>')} has no command")
        if not str(item.get("observed_output", "")).strip():
            reasons.append(f"evidence {item.get('evidence_id', '<unknown>')} has no observed output")
        if not item.get("commit_sha"):
            reasons.append(f"evidence {item.get('evidence_id', '<unknown>')} has no commit binding")
        if expected_commit and item.get("commit_sha") != expected_commit:
            reasons.append(f"evidence {item.get('evidence_id', '<unknown>')} is bound to the wrong commit")
        if not parse_time(str(item.get("observed_at", ""))):
            reasons.append(f"evidence {item.get('evidence_id', '<unknown>')} has invalid observation time")
        item_criteria = item.get("criteria_covered", [])
        if not isinstance(item_criteria, list):
            reasons.append(f"evidence {item.get('evidence_id', '<unknown>')} criteria_covered must be a list")
        else:
            covered.update(str(x) for x in item_criteria)

    if isinstance(criteria, list):
        required = {str(x) for x in criteria}
        missing = sorted(required - covered)
        if missing:
            reasons.append("success criteria lack explicit evidence coverage: " + "; ".join(missing))

    if protected_baseline and expected_commit and protected_baseline != expected_commit:
        warnings.append("protected baseline differs from the current verification commit; review scope before promotion")

    if passing == 0:
        reasons.append("no independently acceptable PASS evidence exists")

    verdict = "REJECT" if reasons else "ACCEPT"
    return {
        "schema": SCHEMA,
        "verdict": verdict,
        "claim_id": claim.get("claim_id"),
        "independent": True,
        "reasons": reasons,
        "warnings": warnings,
        "evidence_count": len(evidence),
        "passing_evidence": passing,
        "criteria_covered": sorted(covered),
        "expected_commit": expected_commit,
        "promotion_allowed": verdict == "ACCEPT",
    }


def attach_provenance(result: dict[str, Any], claim: dict[str, Any], evidence: list[dict[str, Any]], expected_commit: str | None, root: Path, run_id: str | None = None) -> dict[str, Any]:
    """Attach reproducible input/code provenance and a digest over the complete result."""
    fingerprints = input_fingerprints(claim, evidence, expected_commit)
    implementation_path = Path(__file__).resolve()
    implementation_sha = git_blob_sha(implementation_path, root)
    implementation_commit = git_head(root)
    result = dict(result)
    result["provenance"] = {
        "schema": PROVENANCE_SCHEMA,
        **fingerprints,
        "expected_commit": expected_commit,
        "implementation_path": str(implementation_path.relative_to(root)).replace("\\", "/"),
        "implementation_sha256": implementation_sha,
        "implementation_commit": implementation_commit,
        "execution_source": "github-actions" if os.getenv("GITHUB_ACTIONS") == "true" else "local",
        "execution_run_id": run_id or os.getenv("GITHUB_RUN_ID"),
    }
    unsigned = dict(result)
    result["result_sha256"] = sha256_json(unsigned)
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("claim")
    ap.add_argument("evidence")
    ap.add_argument("--commit", default=None)
    ap.add_argument("--baseline", default=None)
    ap.add_argument("--run-id", default=None)
    args = ap.parse_args()
    claim = json.loads(Path(args.claim).read_text(encoding="utf-8"))
    evidence = json.loads(Path(args.evidence).read_text(encoding="utf-8"))
    if isinstance(evidence, dict):
        evidence = [evidence]
    root = Path(__file__).resolve().parents[2]
    expected_commit = args.commit or git_head(root)
    result = challenge(claim, evidence, expected_commit, args.baseline)
    result = attach_provenance(result, claim, evidence, expected_commit, root, args.run_id)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["verdict"] == "ACCEPT" else 1


if __name__ == "__main__":
    sys.exit(main())
