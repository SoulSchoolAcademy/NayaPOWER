#!/usr/bin/env python3
"""GitHub-mutation / release / deployment execution closure (NAYA POWER TEST #11).

The consequential seam is: UniversalExecutionGate -> repository mutation ->
release authorization -> Cloudflare/Vercel deployment. This suite proves the
release boundary around the SAME UniversalExecutionGate refuses every callerside
bypass, and statically documents the GitHub Actions workflow surface.

Safe: no repository state is written. The controller's EXECUTION-STATE is
redirected to a temp dir; every positive issue/verify uses one gate instance;
temporary registries live in tempfile dirs.

Run:  python tests/test_github_release_execution_closure.py
"""
from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone

ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(ROOT / ".naya" / "runtime"))
from execution_preflight_gate import approved_preflight  # noqa: E402

GATE_PATH = ROOT / ".naya" / "runtime" / "universal_execution_gate.py"
BOUNDARY_PATH = ROOT / ".naya" / "runtime" / "release_execution_boundary.py"
EC_PATH = ROOT / ".naya" / "runtime" / "execution_controller.py"

_gate_spec = importlib.util.spec_from_file_location("gr11_universal_execution_gate", GATE_PATH)
assert _gate_spec and _gate_spec.loader
GATE = importlib.util.module_from_spec(_gate_spec)
sys.modules[GATE.__name__] = GATE
_gate_spec.loader.exec_module(GATE)

_b_spec = importlib.util.spec_from_file_location("gr11_release_execution_boundary", BOUNDARY_PATH)
assert _b_spec and _b_spec.loader
BOUNDARY = importlib.util.module_from_spec(_b_spec)
sys.modules[BOUNDARY.__name__] = BOUNDARY
_b_spec.loader.exec_module(BOUNDARY)

_ec_spec = importlib.util.spec_from_file_location("execution_controller", EC_PATH)
assert _ec_spec and _ec_spec.loader
EC = importlib.util.module_from_spec(_ec_spec)
sys.modules["execution_controller"] = EC
_ec_spec.loader.exec_module(EC)

_TMP = Path(tempfile.mkdtemp(prefix="gr11-"))
EC.STATE = _TMP / "EXECUTION-STATE.json"
EC.SESSIONS_ROOT = _TMP / "sessions"
EC.SESSIONS_INDEX_PATH = EC.SESSIONS_ROOT / "INDEX.json"

REPOSITORY = "SoulSchoolAcademy/NayaPOWER"
PRINCIPAL = "SoulSchoolAcademy"
COMMIT = "a" * 40
OTHER_COMMIT = "b" * 40
WORKER = "sparkling-shape-7ae5"
OTHER_WORKER = "mistake-worker-7ae5"
DEPLOY_AID = "HUMAN-SOULSCHOOLACADEMY-HUB-DEPLOY-509"
REPO_AID = "HUMAN-SOULSCHOOLACADEMY-REPO-WRITE"
DEPLOY_PURPOSE = "deploy the canonical 509 NayaNET Intelligent Hub public runtime"
DEPLOY_SCOPE = "public-runtime:sparkling-shape-7ae5:/"
REPO_PURPOSE = "governed maintenance and verification of NayaPOWER"
REPO_SCOPE = "repo:SoulSchoolAcademy/NayaPOWER"
MUTATION_PATHS = ["2026 09 15 NayaNETHUB.html"]
NO_AUTH = ("no gate-issued ExecutionAuthorization supplied",)


def now_iso(offset_seconds: int = 0) -> str:
    return (datetime.now(timezone.utc) + timedelta(seconds=offset_seconds)).isoformat()


def deploy_target(commit=COMMIT, environment="preview", worker=WORKER, repository=REPOSITORY):
    return BOUNDARY.deploy_target(
        deployment_surface="cloudflare",
        environment=environment,
        repository=repository,
        commit_sha=commit,
        worker_name=worker,
    )


def deploy_decision(gate=GATE, scope=DEPLOY_SCOPE, purpose=DEPLOY_PURPOSE, **overrides):
    values = dict(
        decision_id="GR11-DEPLOY-DEC-001",
        mission="Deploy exact NayaPOWER commit to the canonical Cloudflare runtime",
        actor_id=PRINCIPAL,
        action="deploy_public_runtime",
        purpose=purpose,
        scope=scope,
        current_truth="release authorization binds a verified artifact to the exact runtime",
        gap="the verified artifact is not yet published to the target runtime",
        evidence=("evidence:registry-grant",),
        epistemic=frozenset({gate.Epistemic.OBSERVED, gate.Epistemic.VERIFIED}),
        consequence="public deployment to the canonical NayaNET Hub runtime",
        reversible=True,
        risk=gate.Risk(uncertainty=2, consequence=4, irreversibility=4),
        alternatives=("do_not_release",),
        expected_value="publish the explicitly authorized verified artifact",
        required_permission="deploy_public_runtime",
        verification=gate.VerificationPlan(
            observation="live Cloudflare runtime observation",
            success_criteria="exact authorized commit is deployed and live runtime verification passes",
            stop_conditions=("authorization mismatch", "kernel denial", "deployment failure"),
        ),
        necessary_power=frozenset({"deploy_public_runtime"}),
        requested_power=frozenset({"deploy_public_runtime"}),
    )
    values.update(overrides)
    return gate.DecisionObject(**values)


def deploy_action(commit=COMMIT, environment="preview", worker=WORKER, decision_id="GR11-DEPLOY-DEC-001",
                  aid=DEPLOY_AID, **overrides):
    values = dict(
        action_id="GR11-DEPLOY-ACT-001",
        action_type="deploy_public_runtime",
        target=deploy_target(commit=commit, environment=environment, worker=worker),
        purpose=DEPLOY_PURPOSE,
        scope=DEPLOY_SCOPE,
        actor_id=PRINCIPAL,
        permission="deploy_public_runtime",
        decision_id=decision_id,
        authority_id=aid,
    )
    values.update(overrides)
    return values


def repo_decision(gate=GATE, scope=REPO_SCOPE, purpose=REPO_PURPOSE, **overrides):
    values = dict(
        decision_id="GR11-REPO-DEC-001",
        mission="NayaPOWER governed maintenance and verification",
        actor_id=PRINCIPAL,
        action="repo_write",
        purpose=purpose,
        scope=scope,
        current_truth="repository mutation requested",
        gap="mutation requires canonical governance decision",
        evidence=("evidence:registry-grant",),
        epistemic=frozenset({gate.Epistemic.OBSERVED, gate.Epistemic.VERIFIED}),
        consequence="repository write under bounded governance",
        reversible=True,
        risk=gate.Risk(uncertainty=1, consequence=2, irreversibility=1),
        alternatives=("do_not_execute",),
        expected_value="authorized bounded mutation",
        required_permission="repo_write",
        verification=gate.VerificationPlan("post-write state", "verification passes", ("stop",)),
        necessary_power=frozenset({"repo_write"}),
        requested_power=frozenset({"repo_write"}),
    )
    values.update(overrides)
    return gate.DecisionObject(**values)


def repo_action(paths=MUTATION_PATHS, decision_id="GR11-REPO-DEC-001", **overrides):
    values = dict(
        action_id="GR11-REPO-ACT-001",
        action_type="repository_write",
        target=BOUNDARY.repo_mutation_target(repository=REPOSITORY, target_paths=paths),
        purpose=REPO_PURPOSE,
        scope=REPO_SCOPE,
        actor_id=PRINCIPAL,
        permission="repo_write",
        decision_id=decision_id,
        authority_id=REPO_AID,
    )
    values.update(overrides)
    return values


def issue(gate, *, deploy=True, **action_overrides):
    aid = DEPLOY_AID if deploy else REPO_AID
    authority = gate._current_registry().resolve(aid)
    decision = deploy_decision() if deploy else repo_decision()
    action = deploy_action(**action_overrides) if deploy else repo_action(**action_overrides)
    return gate.authorize(authority=authority, decision=decision, action=action)


class T11MatrixBase(unittest.TestCase):
    results: dict[str, str] = {}

    def record(self, name: str, ok: bool, why: str = "", refused: bool | None = None):
        T11MatrixBase.results[name] = "REFUSED" if refused else "ALLOW"
        self.assertTrue(ok, why)


# ---- 1. IDENTITY: the boundary only trusts a registry-origin authority ------
class IdentityTests(T11MatrixBase):
    def setUp(self) -> None:
        self.gate = GATE.UniversalExecutionGate(GATE.load_registry())

    def _release_refusal_reason(self, **kwargs):
        decision = BOUNDARY.authorize_release(
            gate=self.gate,
            execution_authorization=kwargs.get("execution_authorization"),
            commit_sha=kwargs.get("commit_sha", COMMIT),
            target_environment=kwargs.get("target_environment", "preview"),
            deployment_surface=kwargs.get("deployment_surface", "cloudflare"),
            worker_name=kwargs.get("worker_name", WORKER),
        )
        return decision

    def test_T01_no_authority_refused(self):
        d = self._release_refusal_reason(execution_authorization=None)
        self.record("T01", not d.allowed, d.reason, True)
        self.assertEqual(d.reason, NO_AUTH[0])

    def test_T02_caller_declared_principal_only_refused(self):
        d = self._release_refusal_reason(execution_authorization={"principal": PRINCIPAL, "granted": True})
        self.record("T02", not d.allowed, d.reason, True)
        self.assertIn("ExecutionAuthorization", d.reason)

    def test_T03_approval_string_alone_refused(self):
        d = self._release_refusal_reason(execution_authorization={"approval": "EXPLICIT_APPROVAL_GRANTED"})
        self.record("T03", not d.allowed, d.reason, True)
        self.assertIn("ExecutionAuthorization", d.reason)

    def test_T04_release_id_as_authority_refused(self):
        d = self._release_refusal_reason(execution_authorization={"release_id": "REL-001", "authorized": True})
        self.record("T04", not d.allowed, d.reason, True)
        self.assertIn("ExecutionAuthorization", d.reason)

    def test_T05_actor_claim_alone_refused(self):
        d = self._release_refusal_reason(execution_authorization={"actor_id": PRINCIPAL})
        self.record("T05", not d.allowed, d.reason, True)
        self.assertIn("ExecutionAuthorization", d.reason)

    def test_T06_permission_claim_alone_refused(self):
        d = self._release_refusal_reason(execution_authorization={"permission": "deploy_public_runtime"})
        self.record("T06", not d.allowed, d.reason, True)
        self.assertIn("ExecutionAuthorization", d.reason)

    def test_T07_target_claim_alone_refused(self):
        d = self._release_refusal_reason(
            execution_authorization={"target": deploy_target(), "action_type": "deploy_public_runtime"}
        )
        self.record("T07", not d.allowed, d.reason, True)
        self.assertIn("ExecutionAuthorization", d.reason)

    def test_T08_real_aid_string_refused(self):
        d = self._release_refusal_reason(execution_authorization={"authority_id": DEPLOY_AID})
        self.record("T08", not d.allowed, d.reason, True)
        self.assertIn("ExecutionAuthorization", d.reason)


# ---- 2. PROVENANCE: issued by THIS gate and registry-fingerprint origin -----
class ProvenanceTests(T11MatrixBase):
    def setUp(self) -> None:
        self.gate = GATE.UniversalExecutionGate(GATE.load_registry())
        self.ok = issue(self.gate, deploy=True)
        self.assertTrue(self.ok.allowed, self.ok.reasons)
        self.cred = self.ok.authorization

    def test_T09_caller_constructed_credential_refused(self):
        parts = [self.cred.authority_id, self.cred.decision_id, "NEVER",
                 self.cred.action_type, self.cred.target, self.cred.actor_id,
                 self.cred.scope, self.cred.permission]
        forged_hash = hashlib.sha256("|".join(parts).encode()).hexdigest()
        forged = self.cred.__class__(
            authority_id=self.cred.authority_id,
            decision_id=self.cred.decision_id,
            action_id="NEVER",
            action_type=self.cred.action_type,
            target=self.cred.target,
            actor_id=self.cred.actor_id,
            scope=self.cred.scope,
            permission=self.cred.permission,
            governance_state=self.cred.governance_state,
            risk_tier=self.cred.risk_tier,
            validated_at=self.cred.validated_at,
            binding_hash=forged_hash,
        )
        d = BOUNDARY.authorize_release(
            gate=self.gate, execution_authorization=forged, commit_sha=COMMIT,
            target_environment="preview", deployment_surface="cloudflare", worker_name=WORKER,
        )
        self.record("T09", not d.allowed, d.reason, True)
        self.assertIn("not issued by this gate", d.reason)

    def test_T10_valid_credential_from_different_gate_refused(self):
        other_gate = GATE.UniversalExecutionGate(GATE.load_registry())
        other = issue(other_gate, deploy=True, action_id="GR11-OTHER-GATE-ACT")
        self.assertTrue(other.allowed)
        d = BOUNDARY.authorize_release(
            gate=self.gate, execution_authorization=other.authorization, commit_sha=COMMIT,
            target_environment="preview", deployment_surface="cloudflare", worker_name=WORKER,
        )
        self.record("T10", not d.allowed, d.reason, True)
        self.assertIn("not issued by this gate", d.reason)

    def test_T11_authority_not_from_registry_refused(self):
        fake = GATE.Authority(
            authority_id=DEPLOY_AID,
            principal_id=PRINCIPAL,
            purpose=DEPLOY_PURPOSE,
            scope="public-runtime:unauthorized-worker:/",
            granted_actions=frozenset({"deploy_public_runtime"}),
        )
        result = self.gate.authorize(
            authority=fake,
            decision=deploy_decision(),
            action=deploy_action(scope="public-runtime:unauthorized-worker:/"),
        )
        self.record("T11", not result.allowed, "; ".join(result.reasons), True)
        self.assertIn("provenance failure", " ".join(result.reasons))

    def test_T12_revoked_before_use_refused(self):
        with tempfile.TemporaryDirectory(prefix="gr11-") as tmp:
            path = Path(tmp) / "authority-registry.json"
            payload = {
                "authorities": [
                    {
                        "authority_id": DEPLOY_AID,
                        "principal_id": PRINCIPAL,
                        "purpose": DEPLOY_PURPOSE,
                        "scope": DEPLOY_SCOPE,
                        "granted_actions": ["deploy_public_runtime"],
                        "expires_at": None,
                        "revoked": False,
                    }
                ]
            }
            path.write_text(json_dumps(payload), encoding="utf-8")
            gate = GATE.UniversalExecutionGate(registry_path=path)
            granted = issue(gate, deploy=True)
            self.assertTrue(granted.allowed)
            payload["authorities"][0]["revoked"] = True
            path.write_text(json_dumps(payload), encoding="utf-8")
            d = BOUNDARY.authorize_release(
                gate=gate, execution_authorization=granted.authorization, commit_sha=COMMIT,
                target_environment="preview", deployment_surface="cloudflare", worker_name=WORKER,
            )
            self.record("T12", not d.allowed, d.reason, True)
            self.assertIn("revoked", d.reason)


# ---- 3. INTERNAL: tamper / hash / swap -------------------------------------
class InternalTests(T11MatrixBase):
    def setUp(self) -> None:
        self.gate = GATE.UniversalExecutionGate(GATE.load_registry())
        self.ok = issue(self.gate, deploy=True)
        self.assertTrue(self.ok.allowed, self.ok.reasons)
        self.cred = self.ok.authorization

    def _release(self, credential, **kwargs):
        return BOUNDARY.authorize_release(
            gate=self.gate,
            execution_authorization=credential,
            commit_sha=kwargs.get("commit_sha", COMMIT),
            target_environment=kwargs.get("target_environment", "preview"),
            deployment_surface=kwargs.get("deployment_surface", "cloudflare"),
            worker_name=kwargs.get("worker_name", WORKER),
            project_id=kwargs.get("project_id"),
        )

    def test_T13_tampered_scope_refused(self):
        import dataclasses
        d = self._release(dataclasses.replace(self.cred, scope="repo:attacker/other"))
        self.record("T13", not d.allowed, d.reason, True)
        self.assertIn("binding_hash", d.reason)

    def test_T14_tampered_action_type_refused(self):
        import dataclasses
        d = self._release(dataclasses.replace(self.cred, action_type="file_write"))
        self.record("T14", not d.allowed, d.reason, True)
        self.assertIn("binding_hash", d.reason)

    def test_T15_tampered_target_refused(self):
        import dataclasses
        d = self._release(dataclasses.replace(self.cred, target="worker:other"))
        self.record("T15", not d.allowed, d.reason, True)
        self.assertIn("binding_hash", d.reason)

    def test_T16_cross_surface_swap_refused(self):
        d = self._release(self.cred, deployment_surface="vercel", project_id="prj_cHa9gwrtscCW8JuMDjcvw6DafaOK")
        self.record("T16", not d.allowed, d.reason, True)
        self.assertIn("deploy target", d.reason)

    def test_T17_environment_swap_refused(self):
        d = self._release(self.cred, target_environment="production")
        self.record("T17", not d.allowed, d.reason, True)
        self.assertIn("deploy target", d.reason)

    def test_T18_commit_swap_refused(self):
        d = self._release(self.cred, commit_sha=OTHER_COMMIT)
        self.record("T18", not d.allowed, d.reason, True)
        self.assertIn("deploy target", d.reason)

    def test_T19_worker_swap_refused(self):
        d = self._release(self.cred, worker_name=OTHER_WORKER)
        self.record("T19", not d.allowed, d.reason, True)
        self.assertIn("deploy target", d.reason)

    def test_T20_credential_cross_kind_swap_refused(self):
        repo_ok = issue(self.gate, deploy=False)
        self.assertTrue(repo_ok.allowed, repo_ok.reasons)
        d = self._release(repo_ok.authorization)
        self.record("T20", not d.allowed, d.reason, True)
        self.assertTrue(
            ("action_type" in d.reason) or ("deploy target" in d.reason),
            f"reason did not show kind or target refusal: {d.reason}",
        )


# ---- 4. CHAIN: gate -> boundary -> controller ------------------------------
class ChainTests(T11MatrixBase):
    def setUp(self) -> None:
        self.gate = GATE.UniversalExecutionGate(GATE.load_registry())

    def test_T21_valid_exact_target_allows(self):
        ok = issue(self.gate, deploy=True)
        self.assertTrue(ok.allowed, ok.reasons)
        d = BOUNDARY.authorize_release(
            gate=self.gate, execution_authorization=ok.authorization, commit_sha=COMMIT,
            target_environment="preview", deployment_surface="cloudflare", worker_name=WORKER,
        )
        self.record("T21", d.allowed, d.reason, False)
        self.assertIn("exact target", d.reason)

    def test_T22_controller_executing_requires_credential(self):
        import json
        start = {"schema_version": 1, "status": "CLAIMED", "claim_id": "CL-GR11",
                 "block_id": "B-GR11", "owner": PRINCIPAL, "scope": [REPO_SCOPE],
                 "start_head": "test-head", "history": []}
        EC.STATE.write_text(json.dumps(start), encoding="utf-8")
        with self.assertRaises(Exception) as ctx:
            EC.transition("EXECUTING")  # no credential, no gate, no action
        self.record("T22", "ExecutionAuthorization" in str(ctx.exception), str(ctx.exception), False)
        EC.STATE.unlink(missing_ok=True)

    def test_T23_controller_with_credential_and_exact_action_allows(self):
        import json
        ok = issue(self.gate, deploy=True)
        self.assertTrue(ok.allowed, ok.reasons)
        cred = ok.authorization
        start = {"schema_version": 1, "status": "CLAIMED", "claim_id": "CL-GR11",
                 "block_id": "B-GR11", "owner": PRINCIPAL, "scope": [REPO_SCOPE],
                 "start_head": "test-head", "history": []}
        EC.STATE.write_text(json.dumps(start), encoding="utf-8")
        action = {
            "action_id": cred.action_id,
            "authority_id": cred.authority_id,
            "decision_id": cred.decision_id,
            "actor_id": cred.actor_id,
            "scope": cred.scope,
            "permission": cred.permission,
        }
        data = EC.transition("EXECUTING", action=action, gate=self.gate,
                             execution_authorization=cred, preflight=approved_preflight())
        self.assertEqual(data["status"], "EXECUTING")
        self.record("T23", data.get("status") == "EXECUTING", "controller EXECUTING reached via gate-issued credential", False)
        EC.STATE.unlink(missing_ok=True)

    def test_T24_mutation_boundary_exact_changeset_allows(self):
        ok = issue(self.gate, deploy=False)
        self.assertTrue(ok.allowed, ok.reasons)
        d = BOUNDARY.authorize_repo_mutation(
            gate=self.gate, execution_authorization=ok.authorization, target_paths=MUTATION_PATHS,
        )
        self.record("T24", d.allowed, d.reason, False)

    def test_T24b_mutation_boundary_outside_changeset_refused(self):
        ok = issue(self.gate, deploy=False)
        self.assertTrue(ok.allowed, ok.reasons)
        d = BOUNDARY.authorize_repo_mutation(
            gate=self.gate, execution_authorization=ok.authorization,
            target_paths=["OUTSIDE.txt"],
        )
        self.record("T24b", not d.allowed, d.reason, True)
        self.assertIn("change-set", d.reason)


# ---- 5. EXTERNAL: GitHub Actions workflow surface (static proof) -----------
WORKFLOWS = ROOT / ".github" / "workflows"


def read_workflow(name: str) -> str:
    path = WORKFLOWS / name
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")


class WorkflowSurfaceTests(T11MatrixBase):
    """Static, no-execute proof of the workflow surface.

    T25/T26/T27/T29 are @expectedFailure BY DESIGN: each asserts the requirement
    (the workflow must verify a gate-issued credential before its side effect)
    so it is `XFAIL` until the GitHub Actions lane is wired to the gate via
    signed cross-process credentials (FUTURE WORK). They truthfully record that
    the surface is OPEN today; NOTHING was fake-grayed.
    """

    CONSEQUENTIAL_LIVE = [
        "assistant-cloudflare-hub-release.yml",
        "nayanet-canonical-hub-production-release.yml",
        "510-aaa-smart-board-visual-surgery.yml",
    ]

    @unittest.expectedFailure
    def test_T25_cloudflare_push_deploy_OPEN(self):
        text = read_workflow("assistant-cloudflare-hub-release.yml")
        self.assertNotEqual("", text, "workflow file exists")
        self.assertIn("wrangler", text)
        self.assertIn("universal_execution_gate", text)

    @unittest.expectedFailure
    def test_T26_dispatch_magic_string_OPEN(self):
        text = read_workflow("nayanet-canonical-hub-production-release.yml")
        self.assertNotEqual("", text, "workflow file exists")
        self.assertTrue("RELEASE_CANONICAL_HUB" in text or "workflow_dispatch" in text)
        self.assertIn("universal_execution_gate", text)

    @unittest.expectedFailure
    def test_T27_unattended_git_push_mutation_OPEN(self):
        text = read_workflow("510-aaa-smart-board-visual-surgery.yml")
        self.assertNotEqual("", text, "workflow file exists")
        self.assertIn("contents: write", text)
        self.assertIn("universal_execution_gate", text)

    @unittest.expectedFailure
    def test_T29_vercel_referenced_workflow_missing_OPEN(self):
        self.assertTrue((WORKFLOWS / "authorized-vercel-release.yml").is_file())

    def test_T29b_vercel_policy_references_absent_workflow(self):
        import json
        policy_path = ROOT / ".naya" / "control-plane" / "DEPLOYMENT-GOVERNANCE.json"
        policy = json.loads(policy_path.read_text(encoding="utf-8"))
        referenced = str(policy.get("canonical_release_workflow", ""))
        self.assertTrue(referenced.endswith("authorized-vercel-release.yml"), referenced)
        self.assertFalse((WORKFLOWS / "authorized-vercel-release.yml").is_file(),
                         "Vercel is unautomated: no executable workflow; policy default is DENY")

    def test_T28_legacy_deploy_stubs_fail_closed(self):
        for name in read_legacy_deploy_names():
            text = read_workflow(name)
            head = text.strip().splitlines()[0:2]
            joined = " ".join(head)
            self.assertTrue("DISABLED" in joined or "BLOCKED" in joined or "RETIRED" in joined,
                            f"legacy lane {name} is not explicitly disabled: {joined}")
            self.assertNotIn("wrangler-action", text, f"legacy lane {name} must not deploy via wrangler-action")
        self.record("T28", True, "legacy deploy lanes are disabled echo/block stubs", False)

    def test_T33_workflow_gate_reference_census(self):
        gate_referencing = [
            name for name in self.CONSEQUENTIAL_LIVE
            if "universal_execution_gate" in read_workflow(name)
        ]
        self.assertEqual(
            gate_referencing,
            [],
            "documented OPEN: no consequential live workflow references the UniversalExecutionGate",
        )
        self.record("T33", len(gate_referencing) == 0, "gate census: 0 consequential live workflows wired", False)

    def test_T30_push_trigger_is_not_authority(self):
        request = {"trigger": "push", "event_name": "push", "ref": "main", "actor": "anyone", "token": "x"}
        d = BOUNDARY.authorize_release(
            gate=GATE.UniversalExecutionGate(GATE.load_registry()),
            execution_authorization=request, commit_sha=COMMIT,
            target_environment="production", deployment_surface="cloudflare", worker_name=WORKER,
        )
        self.record("T30", not d.allowed, d.reason, True)
        self.assertIn("ExecutionAuthorization", d.reason)

    def test_T31_magic_string_is_not_authority(self):
        request = {"confirm": "RELEASE_CANONICAL_HUB", "authorized_by": PRINCIPAL}
        d = BOUNDARY.authorize_release(
            gate=GATE.UniversalExecutionGate(GATE.load_registry()),
            execution_authorization=request, commit_sha=COMMIT,
            target_environment="production", deployment_surface="cloudflare", worker_name=WORKER,
        )
        self.record("T31", not d.allowed, d.reason, True)
        self.assertIn("ExecutionAuthorization", d.reason)

    def test_T32_deploy_tokens_are_not_authority(self):
        request = {"CLOUDFLARE_API_TOKEN": "cld-xxxx", "VERCEL_TOKEN": "vrc-xxxx"}
        d = BOUNDARY.authorize_release(
            gate=GATE.UniversalExecutionGate(GATE.load_registry()),
            execution_authorization=request, commit_sha=COMMIT,
            target_environment="production", deployment_surface="cloudflare", worker_name=WORKER,
        )
        self.record("T32", not d.allowed, d.reason, True)
        self.assertIn("ExecutionAuthorization", d.reason)


def read_legacy_deploy_names():
    if not WORKFLOWS.is_dir():
        return []
    names = []
    for entry in sorted(WORKFLOWS.iterdir()):
        if entry.name.startswith("deploy-") or "authority-v6" in entry.name or "world-class" in entry.name:
            names.append(entry.name)
    return names


# ---- Direct-bypass harness (NO PRODUCTION OTHERWISE) -----------------------
class DirectBypassHarnessTests(unittest.TestCase):
    """Adversarial direct bypass attempts against the release boundary."""

    def setUp(self) -> None:
        self.gate = GATE.UniversalExecutionGate(GATE.load_registry())
        self.harness: dict[str, str] = {}

    def test_100_direct_bypass_harness(self):
        vectors = {
            "push-with-token": {"CLOUDFLARE_API_TOKEN": "x", "trigger": "push"},
            "approval-string": {"approval": "EXPLICIT_APPROVAL_GRANTED"},
            "exec-state": {"status": "EXECUTING", "execution_status": "EXECUTING"},
            "receipt": {"receipt": {"status": "verified", "authorized": True}},
            "claim": {"claim": {"status": "CLAIMED"}, "claim_id": "CL-X"},
            "release-id": {"release_id": "REL-1", "authorized_by": PRINCIPAL},
        }
        for name, payload in vectors.items():
            try:
                d = BOUNDARY.authorize_release(
                    gate=self.gate, execution_authorization=payload, commit_sha=COMMIT,
                    target_environment="production", deployment_surface="cloudflare", worker_name=WORKER,
                )
                refused = not d.allowed
            except Exception as exc:  # any unexpected success path is a failure
                refused = False
                d = None
                self.harness[name] = f"EXCEPTION {exc}"
            if refused:
                self.harness[name] = f"REFUSED ({d.reason})"
            else:
                self.harness[name] = "REFUSED"
            self.assertTrue(refused, f"direct bypass vector {name} was NOT refused")

    def test_101_mutation_bypass_harness(self):
        vectors = {
            "no-credential": None,
            "caller-approval": {"authorized": True, "approval": "GRANTED"},
        }
        for name, payload in vectors.items():
            d = BOUNDARY.authorize_repo_mutation(
                gate=self.gate, execution_authorization=payload, target_paths=MUTATION_PATHS,
            )
            self.harness[name] = "REFUSED" if not d.allowed else "ALLOW"
            self.assertFalse(d.allowed, f"mutation bypass vector {name} was NOT refused")


T11MatrixBase.results = {}


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(IdentityTests)
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(ProvenanceTests))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(InternalTests))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(ChainTests))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(WorkflowSurfaceTests))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(DirectBypassHarnessTests))
    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(suite)
    refused = sum(1 for v in T11MatrixBase.results.values() if v == "REFUSED")
    allowed = sum(1 for v in T11MatrixBase.results.values() if v == "ALLOW")
    print(f"GITHUB_RELEASE_EXECUTION_CLOSURE = matrix cases={len(T11MatrixBase.results)} "
          f"refused={refused} allowed={allowed}")
    return 0 if result.wasSuccessful() else 1


def json_dumps(value):
    import json
    return json.dumps(value, ensure_ascii=False)


if __name__ == "__main__":
    raise SystemExit(main())