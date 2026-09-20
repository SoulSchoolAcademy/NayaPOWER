#!/usr/bin/env python3
"""Dependency-free regression tests for the release authorization gate.

Contract (Test #11): release authorization is unified with the ONE
UniversalExecutionGate. No caller-declared authorization dict may mint an
Authority, so every positive case drives a real gate-issued
ExecutionAuthorization bound to the exact deploy target.
"""
from __future__ import annotations

from dataclasses import dataclass
import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]

RA_PATH = ROOT / ".naya" / "runtime" / "release_authorization.py"
GATE_PATH = ROOT / ".naya" / "runtime" / "universal_execution_gate.py"
BOUNDARY_PATH = ROOT / ".naya" / "runtime" / "release_execution_boundary.py"

_ra_spec = importlib.util.spec_from_file_location("release_authorization_test_module", RA_PATH)
assert _ra_spec and _ra_spec.loader
module = importlib.util.module_from_spec(_ra_spec)
sys.modules[_ra_spec.name] = module
_ra_spec.loader.exec_module(module)

_gate_spec = importlib.util.spec_from_file_location("naya_ueg_release_authorization", GATE_PATH)
assert _gate_spec and _gate_spec.loader
GATE = importlib.util.module_from_spec(_gate_spec)
sys.modules[GATE.__name__] = GATE
_gate_spec.loader.exec_module(GATE)

_b_spec = importlib.util.spec_from_file_location("naya_release_bnd_test", BOUNDARY_PATH)
assert _b_spec and _b_spec.loader
BOUNDARY = importlib.util.module_from_spec(_b_spec)
sys.modules[BOUNDARY.__name__] = BOUNDARY
_b_spec.loader.exec_module(BOUNDARY)

COMMIT = "a" * 40
OTHER_COMMIT = "b" * 40
WORKER = "sparkling-shape-7ae5"
REPOSITORY = "SoulSchoolAcademy/NayaPOWER"
AUTHORITY_ID = "HUMAN-SOULSCHOOLACADEMY-HUB-DEPLOY-509"
PRINCIPAL = "SoulSchoolAcademy"
PURPOSE = "deploy the canonical 509 NayaNET Intelligent Hub public runtime"
SCOPE = "public-runtime:sparkling-shape-7ae5:/"
DECISION_ID = "RA-DEPLOY-DEC-001"
ACTION_ID = "RA-DEPLOY-ACT-001"


@dataclass(frozen=True)
class DeployCredential:
    authorization: object
    gate: object
    authority: object


def deploy_decision(**overrides):
    values = dict(
        decision_id=DECISION_ID,
        mission="Deploy exact NayaPOWER commit to the canonical Cloudflare runtime",
        actor_id=PRINCIPAL,
        action="deploy_public_runtime",
        purpose=PURPOSE,
        scope=SCOPE,
        current_truth="release authorization binds a verified artifact to the exact runtime",
        gap="the verified artifact is not yet published to the target runtime",
        evidence=("evidence:registry-grant",),
        epistemic=frozenset({GATE.Epistemic.OBSERVED, GATE.Epistemic.VERIFIED}),
        consequence="public deployment to the canonical NayaNET Hub runtime",
        reversible=True,
        risk=GATE.Risk(uncertainty=2, consequence=4, irreversibility=4),
        alternatives=("do_not_release",),
        expected_value="publish the explicitly authorized verified artifact",
        required_permission="deploy_public_runtime",
        verification=GATE.VerificationPlan(
            observation="live Cloudflare runtime observation",
            success_criteria="exact authorized commit is deployed and live runtime verification passes",
            stop_conditions=("authorization mismatch", "kernel denial", "deployment failure"),
        ),
        necessary_power=frozenset({"deploy_public_runtime"}),
        requested_power=frozenset({"deploy_public_runtime"}),
    )
    values.update(overrides)
    return GATE.DecisionObject(**values)


def deploy_action(commit_sha=COMMIT, environment="preview", worker=WORKER, **overrides):
    values = dict(
        action_id=ACTION_ID,
        action_type="deploy_public_runtime",
        target=BOUNDARY.deploy_target(
            deployment_surface="cloudflare",
            environment=environment,
            repository=REPOSITORY,
            commit_sha=commit_sha,
            worker_name=worker,
        ),
        purpose=PURPOSE,
        scope=SCOPE,
        actor_id=PRINCIPAL,
        permission="deploy_public_runtime",
        decision_id=DECISION_ID,
        authority_id=AUTHORITY_ID,
    )
    values.update(overrides)
    return values


def issue_credential(gate=None, **action_overrides):
    gate = gate or GATE.UniversalExecutionGate(GATE.load_registry())
    authority = gate._current_registry().resolve(AUTHORITY_ID)
    decision = deploy_decision()
    action = deploy_action(**action_overrides)
    result = gate.authorize(authority=authority, decision=decision, action=action)
    return result


class ReleaseAuthorizationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = GATE.load_registry()
        self.gate = GATE.UniversalExecutionGate(self.registry)

    def test_checked_in_template_fails_closed(self):
        for environment in ("preview", "production"):
            decision = module.current_template_decision(COMMIT, environment)
            self.assertFalse(decision.allowed, decision.reason)
            self.assertIn(
                "mismatch",
                decision.reason.lower(),
                f"template rejection reason did not mention a binding: {decision.reason}",
            )

    def test_valid_exact_cloudflare_target_allows(self):
        result = issue_credential(gate=self.gate)
        self.assertTrue(result.allowed, result.reasons)
        decision = module.authorize(
            execution_authorization=result.authorization,
            gate=self.gate,
            commit_sha=COMMIT,
            target_environment="preview",
            deployment_surface="cloudflare",
            worker_name=WORKER,
        )
        self.assertTrue(decision.allowed, decision.reason)
        self.assertIn("exact target", decision.reason)

    def test_wrong_commit_denied(self):
        result = issue_credential(gate=self.gate, commit_sha=COMMIT)
        self.assertTrue(result.allowed)
        decision = module.authorize(
            execution_authorization=result.authorization,
            gate=self.gate,
            commit_sha=OTHER_COMMIT,
            target_environment="preview",
            deployment_surface="cloudflare",
            worker_name=WORKER,
        )
        self.assertFalse(decision.allowed, decision.reason)
        self.assertIn("deploy target", decision.reason)

    def test_wrong_worker_denied(self):
        result = issue_credential(gate=self.gate, worker=WORKER)
        self.assertTrue(result.allowed)
        decision = module.authorize(
            execution_authorization=result.authorization,
            gate=self.gate,
            commit_sha=COMMIT,
            target_environment="preview",
            deployment_surface="cloudflare",
            worker_name="mistake-worker-7ae5",
        )
        self.assertFalse(decision.allowed, decision.reason)
        self.assertIn("deploy target", decision.reason)

    def test_caller_declared_approval_dict_is_not_authority(self):
        caller_authorization = {
            "status": "AUTHORIZED",
            "repository": "SoulSchoolAcademy/NayaPOWER",
            "commit_sha": COMMIT,
            "target_environment": "preview",
            "deployment_surface": "cloudflare",
            "approval": "EXPLICIT_APPROVAL_GRANTED",
            "verification": {"status": "PASS", "evidence": ["test"]},
            "release_id": "TEST-001",
            "authorized_by": "test",
            "authorized_at": "2026-08-29T00:00:00Z",
        }
        decision = module.authorize(
            execution_authorization=caller_authorization,
            gate=self.gate,
            commit_sha=COMMIT,
            target_environment="preview",
            deployment_surface="cloudflare",
            worker_name=WORKER,
        )
        self.assertFalse(decision.allowed, decision.reason)
        self.assertIn("gate", decision.reason.lower())
        self.assertIn("ExecutionAuthorization", decision.reason)

    def test_missing_gate_denied(self):
        result = issue_credential(gate=self.gate)
        self.assertTrue(result.allowed)
        decision = module.authorize(
            execution_authorization=result.authorization,
            gate=None,
            commit_sha=COMMIT,
            target_environment="preview",
            deployment_surface="cloudflare",
            worker_name=WORKER,
        )
        self.assertFalse(decision.allowed, decision.reason)


class ReleaseBoundaryTests(unittest.TestCase):
    """Direct boundary checks for the release/mutation adapters."""

    def setUp(self) -> None:
        self.registry = GATE.load_registry()
        self.gate = GATE.UniversalExecutionGate(self.registry)
        self.deploy = issue_credential(gate=self.gate)
        self.assertTrue(self.deploy.allowed)
        self.credential = self.deploy.authorization

    def test_mutation_target_is_valid(self):
        target = BOUNDARY.repo_mutation_target(
            repository="SoulSchoolAcademy/NayaPOWER",
            target_paths=["2026 09 15 NayaNETHUB.html"],
        )
        self.assertIn("2026 09 15 NayaNETHUB.html", target)
        self.assertIn("repo:SoulSchoolAcademy/NayaPOWER:paths:", target)

    def test_repo_mutation_missing_credential_refused(self):
        decision = BOUNDARY.authorize_repo_mutation(
            gate=self.gate,
            execution_authorization=None,
            target_paths=["2026 09 15 NayaNETHUB.html"],
        )
        self.assertFalse(decision.allowed)
        self.assertIn("ExecutionAuthorization", decision.reason)


if __name__ == "__main__":
    unittest.main(verbosity=2)