#!/usr/bin/env python3
import copy
import os
import subprocess
import unittest
from pathlib import Path
from promotion_runtime import evaluate, sha256_json

COMMIT = "a" * 40
ROOT = Path(__file__).resolve().parents[2]
CLAIM = {
    "claim_id": "CL-1",
    "status": "VERIFIED",
    "source": "github-actions:1",
    "success_criteria": ["tests pass", "process exits successfully"],
}
EVIDENCE = {
    "evidence_id": "EV-1",
    "result": "PASS",
    "method": "ci_test",
    "commit_sha": COMMIT,
    "source": "workflow-run:1",
    "environment": "github-actions",
    "command": "python tests.py",
    "observed_at": "2026-08-24T02:00:00Z",
    "criteria_covered": ["tests pass", "process exits successfully"],
}


def implementation_sha():
    return subprocess.run(["git", "hash-object", ".naya/runtime/oscar.py"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip()


def valid_oscar(claim=CLAIM, evidence=None, commit=COMMIT, run_id=None):
    evidence = [copy.deepcopy(EVIDENCE)] if evidence is None else evidence
    run_id = str(run_id or os.getenv("GITHUB_RUN_ID") or "1")
    claim_sha = sha256_json(claim)
    evidence_sha = sha256_json(sorted(evidence, key=lambda item: str(item.get("evidence_id", ""))))
    input_sha = sha256_json({"claim_sha256": claim_sha, "evidence_sha256": evidence_sha, "expected_commit": commit})
    result = {
        "schema": "naya-power-oscar/v1",
        "verdict": "ACCEPT",
        "claim_id": claim["claim_id"],
        "independent": True,
        "reasons": [],
        "warnings": [],
        "evidence_count": len(evidence),
        "passing_evidence": len(evidence),
        "criteria_covered": list(claim["success_criteria"]),
        "expected_commit": commit,
        "promotion_allowed": True,
        "provenance": {
            "schema": "naya-power-oscar-provenance/v1",
            "claim_sha256": claim_sha,
            "evidence_sha256": evidence_sha,
            "input_sha256": input_sha,
            "expected_commit": commit,
            "implementation_path": ".naya/runtime/oscar.py",
            "implementation_sha256": implementation_sha(),
            "implementation_commit": commit,
            "execution_source": "github-actions",
            "execution_run_id": run_id,
        },
    }
    result["result_sha256"] = sha256_json(result)
    return result


def package(target="CANONICAL_VERIFIED", decision="PROMOTE", run_id=None):
    evidence = [copy.deepcopy(EVIDENCE)]
    return {"claim": copy.deepcopy(CLAIM), "evidence": evidence, "oscar": valid_oscar(CLAIM, evidence, run_id=run_id), "target": target, "promotion_decision": decision}


class PromotionTests(unittest.TestCase):
    def test_builder_verified_oscar_rejected(self):
        p = package("OSCAR_ACCEPTED"); p["oscar"]["verdict"] = "REJECT"
        self.assertFalse(evaluate(p, COMMIT)["eligible"])

    def test_builder_verified_stale_evidence(self):
        p = package("BUILDER_VERIFIED"); p["evidence"][0]["commit_sha"] = "b" * 40
        self.assertFalse(evaluate(p, COMMIT)["eligible"])

    def test_oscar_accepted_wrong_commit(self):
        p = package("OSCAR_ACCEPTED"); p["oscar"]["expected_commit"] = "b" * 40
        self.assertFalse(evaluate(p, COMMIT)["eligible"])

    def test_oscar_accepted_superseded_evidence(self):
        p = package("OSCAR_ACCEPTED"); p["evidence"][0]["superseded_at"] = "2026-08-24T03:00:00Z"
        self.assertFalse(evaluate(p, COMMIT)["eligible"])

    def test_oscar_accepted_missing_provenance(self):
        p = package("OSCAR_ACCEPTED"); del p["oscar"]["provenance"]
        self.assertFalse(evaluate(p, COMMIT)["eligible"])

    def test_conflicting_evidence(self):
        p = package("BUILDER_VERIFIED")
        conflict = copy.deepcopy(EVIDENCE); conflict["evidence_id"] = "EV-2"; conflict["result"] = "FAIL"
        p["evidence"].append(conflict)
        self.assertFalse(evaluate(p, COMMIT)["eligible"])

    def test_production_claim_without_production_evidence(self):
        self.assertFalse(evaluate(package("PRODUCTION_SAFE"), COMMIT)["eligible"])

    def test_historical_verification_is_not_current(self):
        p = package("OSCAR_ACCEPTED"); p["evidence"][0]["commit_sha"] = "c" * 40
        self.assertFalse(evaluate(p, COMMIT)["eligible"])

    def test_verified_state_followed_by_repository_change(self):
        self.assertFalse(evaluate(package("OSCAR_ACCEPTED"), "d" * 40)["eligible"])

    def test_retrieved_content_cannot_influence_promotion(self):
        p = package("BUILDER_VERIFIED"); p["evidence"][0]["method"] = "retrieved_content"
        self.assertFalse(evaluate(p, COMMIT)["eligible"])

    def test_eligible_is_not_automatically_canonical(self):
        self.assertFalse(evaluate(package("CANONICAL_VERIFIED", decision=None), COMMIT)["eligible"])

    def test_oscar_acceptance_can_reach_eligible(self):
        r = evaluate(package("OSCAR_ACCEPTED"), COMMIT)
        self.assertTrue(r["eligible"]); self.assertEqual(r["level"], "OSCAR_ACCEPTED")

    def test_canonical_requires_explicit_promotion(self):
        r = evaluate(package("CANONICAL_VERIFIED", decision="PROMOTE"), COMMIT)
        self.assertTrue(r["eligible"]); self.assertEqual(r["level"], "CANONICAL_VERIFIED")

    def test_tampered_result_digest_is_rejected(self):
        p = package("OSCAR_ACCEPTED")
        p["oscar"]["promotion_allowed"] = False
        self.assertFalse(evaluate(p, COMMIT)["eligible"])

    def test_tampered_claim_is_rejected_by_provenance(self):
        p = package("OSCAR_ACCEPTED")
        p["claim"]["source"] = "forged"
        self.assertFalse(evaluate(p, COMMIT)["eligible"])

    def test_tampered_evidence_is_rejected_by_provenance(self):
        p = package("OSCAR_ACCEPTED")
        p["evidence"][0]["observed_output"] = "forged"
        self.assertFalse(evaluate(p, COMMIT)["eligible"])

    def test_wrong_implementation_hash_is_rejected(self):
        p = package("OSCAR_ACCEPTED")
        p["oscar"]["provenance"]["implementation_sha256"] = "0" * 40
        self.assertFalse(evaluate(p, COMMIT)["eligible"])

    def test_wrong_implementation_commit_is_rejected(self):
        p = package("OSCAR_ACCEPTED")
        p["oscar"]["provenance"]["implementation_commit"] = "b" * 40
        self.assertFalse(evaluate(p, COMMIT)["eligible"])

    def test_missing_execution_provenance_is_rejected(self):
        p = package("OSCAR_ACCEPTED")
        del p["oscar"]["provenance"]["execution_run_id"]
        self.assertFalse(evaluate(p, COMMIT)["eligible"])

    def test_wrong_ci_run_is_rejected(self):
        p = package("OSCAR_ACCEPTED", run_id="old-run")
        old = os.environ.get("GITHUB_RUN_ID")
        os.environ["GITHUB_RUN_ID"] = "current-run"
        try:
            self.assertFalse(evaluate(p, COMMIT)["eligible"])
        finally:
            if old is None:
                os.environ.pop("GITHUB_RUN_ID", None)
            else:
                os.environ["GITHUB_RUN_ID"] = old

    def test_current_ci_run_is_accepted(self):
        p = package("OSCAR_ACCEPTED", run_id="current-run")
        old = os.environ.get("GITHUB_RUN_ID")
        os.environ["GITHUB_RUN_ID"] = "current-run"
        try:
            self.assertTrue(evaluate(p, COMMIT)["eligible"])
        finally:
            if old is None:
                os.environ.pop("GITHUB_RUN_ID", None)
            else:
                os.environ["GITHUB_RUN_ID"] = old


if __name__ == "__main__":
    unittest.main()
