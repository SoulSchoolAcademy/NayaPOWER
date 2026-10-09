#!/usr/bin/env python3
"""Fail-closed verifier for activation receipt provenance in protected CI.

The receipt's own fields are claims, not trust. This verifier independently
loads the referenced GitHub Actions run, checks repository/workflow/branch/SHA
and successful completion, downloads that run's named artifact, and requires
the exact artifact bytes to equal the cited receipt bytes. Requires gh CLI
authenticated with read access to Actions and repository metadata.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ARTIFACT_NAME = "naya-activation-receipt"


def gh_json(args: list[str]) -> dict:
    proc = subprocess.run(["gh", "api", *args], capture_output=True, text=True, check=False)
    if proc.returncode:
        raise RuntimeError(f"gh api failed ({proc.returncode}): {proc.stderr.strip()}")
    value = json.loads(proc.stdout)
    if not isinstance(value, dict):
        raise RuntimeError("GitHub API response is not an object")
    return value


def verify(receipt_path: Path, expected_repo: str, expected_repo_id: str,
           expected_main_sha: str) -> list[str]:
    failures: list[str] = []
    try:
        raw = receipt_path.read_bytes()
        receipt = json.loads(raw)
    except (OSError, ValueError) as exc:
        return [f"receipt unreadable: {exc}"]
    if not isinstance(receipt, dict):
        return ["receipt must be a JSON object"]

    run_id = str(receipt.get("activation_run_id", ""))
    attempt = str(receipt.get("activation_run_attempt", ""))
    workflow = str(receipt.get("activation_workflow", ""))
    if not run_id.isdigit() or not attempt.isdigit() or not workflow:
        return ["receipt lacks numeric activation run ID/attempt or workflow path"]

    try:
        run = gh_json([f"repos/{expected_repo}/actions/runs/{run_id}"])
    except Exception as exc:
        return [f"activation run could not be independently resolved: {exc}"]

    if str(run.get("id", "")) != run_id:
        failures.append("run ID does not match the receipt")
    if str(run.get("run_attempt", "")) != attempt:
        failures.append("run attempt does not match the receipt")
    repository = run.get("repository") or {}
    if str(repository.get("id", "")) != str(expected_repo_id):
        failures.append("activation run belongs to a different repository ID")
    if str(run.get("head_repository", {}).get("full_name", "")).lower() != expected_repo.lower():
        failures.append("activation run head repository does not match trusted repository")
    if run.get("head_branch") != "main":
        failures.append("activation run was not executed from protected main")
    if str(run.get("head_sha", "")).lower() != expected_main_sha.lower():
        failures.append("activation run head SHA is not the trusted live main tip")
    if str(receipt.get("main_sha", "")).lower() != expected_main_sha.lower():
        failures.append("receipt main SHA is not the trusted live main tip")
    if run.get("path") != workflow:
        failures.append("receipt workflow path does not match the actual run workflow")
    if run.get("status") != "completed" or run.get("conclusion") != "success":
        failures.append("activation workflow run is not completed successfully")

    # The run's own artifact is the source of truth. A self-consistent JSON file
    # with a matching marker is not enough; exact bytes must come from that run.
    try:
        with tempfile.TemporaryDirectory(prefix="naya-activation-") as td:
            proc = subprocess.run(
                ["gh", "run", "download", run_id, "--repo", expected_repo,
                 "--name", ARTIFACT_NAME, "--dir", td],
                capture_output=True, text=True, check=False,
            )
            if proc.returncode:
                failures.append("trusted activation artifact download failed: " +
                                proc.stderr.strip())
            else:
                matches = list(Path(td).rglob("receipt.json"))
                if len(matches) != 1:
                    failures.append("trusted activation run must contain exactly one receipt.json artifact")
                elif matches[0].read_bytes() != raw:
                    failures.append("receipt bytes differ from the artifact emitted by the trusted run")
    except OSError as exc:
        failures.append(f"cannot inspect trusted activation artifact: {exc}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", required=True, type=Path)
    parser.add_argument("--expected-repo", required=True)
    parser.add_argument("--expected-repo-id", required=True)
    parser.add_argument("--expected-main-sha", required=True)
    args = parser.parse_args()
    failures = verify(args.receipt, args.expected_repo, args.expected_repo_id,
                      args.expected_main_sha)
    if failures:
        print("ACTIVATION PROVENANCE: FAIL")
        for failure in failures:
            print(" -", failure)
        return 1
    print("ACTIVATION PROVENANCE: PASS — trusted successful run + exact artifact bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
