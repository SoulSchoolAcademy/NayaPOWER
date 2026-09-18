#!/usr/bin/env python3
"""Cross-process portable authorization closure (NAYA POWER TEST #12).

UniversalExecutionGate issues; the ISSUER signs a portable artifact with an
Ed25519 private key held issuer-side; an INDEPENDENT verifier process (a
simulated GitHub Actions runner) verifies signature + binding hash + registry
authority-of-record WITHOUT the issuer's in-process `_issued` set.

The verifier holds ONLY a pinned public key -> it can verify but can never
mint. Tokens, triggers, approval strings, receipts, and execution state are
capability, never authority.

Safe: nothing here is wired to production; no repo/registry/workflow state is
written; every keypair and artifact lives in a temp dir.

Run:  python tests/test_cross_process_authorization_closure.py
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TMP = Path(tempfile.mkdtemp(prefix="cpac-"))

GATE_PATH = ROOT / ".naya" / "runtime" / "universal_execution_gate.py"
BOUNDARY_PATH = ROOT / ".naya" / "runtime" / "release_execution_boundary.py"
PORTA_PATH = ROOT / ".naya" / "runtime" / "portable_authorization.py"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


GATE = load("cp12_universal_execution_gate", GATE_PATH)
BOUNDARY = load("cp12_release_execution_boundary", BOUNDARY_PATH)
PORTA = load("cp12_portable_authorization", PORTA_PATH)

REPOSITORY = "SoulSchoolAcademy/NayaPOWER"
PRINCIPAL = "SoulSchoolAcademy"
COMMIT = "a" * 40
OTHER_COMMIT = "b" * 40
WORKER = "sparkling-shape-7ae5"
OTHER_WORKER = "mistake-worker-7ae5"
OTHER_REPOSITORY = "OtherOrg/NayaPOWER"
VERCEL_PROJECT = "nayapower-canonical"
DEPLOY_AID = "HUMAN-SOULSCHOOLACADEMY-HUB-DEPLOY-509"
REPO_AID = "HUMAN-SOULSCHOOLACADEMY-REPO-WRITE"
DEPLOY_PURPOSE = "deploy the canonical 509 NayaNET Intelligent Hub public runtime"
DEPLOY_SCOPE = "public-runtime:sparkling-shape-7ae5:/"
REPO_PURPOSE = "governed maintenance and verification of NayaPOWER"
REPO_SCOPE = "repo:SoulSchoolAcademy/NayaPOWER"
MUTATION_PATHS = ["2026 09 15 NayaNETHUB.html"]
MUTATION_PATHS_EXTRA = ["2026 09 15 NayaNETHUB.html", "extra/path.txt"]


def now_iso(offset_seconds: int = 0) -> str:
    return (datetime.now(timezone.utc) + timedelta(seconds=offset_seconds)).isoformat()


def deploy_target(commit=COMMIT, environment="preview", worker=WORKER, repository=REPOSITORY):
    return BOUNDARY.deploy_target(
        deployment_surface="cloudflare", environment=environment,
        repository=repository, commit_sha=commit, worker_name=worker,
    )


def deploy_decision(gate=GATE, scope=DEPLOY_SCOPE, purpose=DEPLOY_PURPOSE, decision_id="CP12-DEPLOY-DEC", **overrides):
    values = dict(
        decision_id=decision_id, mission="Deploy exact NayaPOWER commit to the canonical runtime",
        actor_id=PRINCIPAL, action="deploy_public_runtime", purpose=purpose, scope=scope,
        current_truth="release authorization binds a verified artifact to the exact runtime",
        gap="the verified artifact is not yet published to the target runtime",
        evidence=("evidence:registry-grant",),
        epistemic=frozenset({gate.Epistemic.OBSERVED, gate.Epistemic.VERIFIED}),
        consequence="public deployment to the canonical NayaNET Hub runtime",
        reversible=True, risk=gate.Risk(2, 4, 4), alternatives=("do_not_release",),
        expected_value="publish the explicitly authorized verified artifact",
        required_permission="deploy_public_runtime",
        verification=gate.VerificationPlan("live observation", "deploy passes", ("stop",)),
        necessary_power=frozenset({"deploy_public_runtime"}),
        requested_power=frozenset({"deploy_public_runtime"}),
    )
    values.update(overrides)
    return gate.DecisionObject(**values)


def deploy_action(commit=COMMIT, environment="preview", worker=WORKER,
                  decision_id="CP12-DEPLOY-DEC", aid=DEPLOY_AID, **overrides):
    values = dict(
        action_id="CP12-DEPLOY-ACT", action_type="deploy_public_runtime",
        target=deploy_target(commit=commit, environment=environment, worker=worker),
        purpose=DEPLOY_PURPOSE, scope=DEPLOY_SCOPE, actor_id=PRINCIPAL,
        permission="deploy_public_runtime", decision_id=decision_id, authority_id=aid,
    )
    values.update(overrides)
    return values


def repo_decision(gate=GATE, scope=REPO_SCOPE, purpose=REPO_PURPOSE, decision_id="CP12-REPO-DEC", **overrides):
    values = dict(
        decision_id=decision_id, mission="NayaPOWER governed maintenance and verification",
        actor_id=PRINCIPAL, action="repo_write", purpose=purpose, scope=scope,
        current_truth="repository mutation requested", gap="mutation requires canonical decision",
        evidence=("evidence:registry-grant",),
        epistemic=frozenset({gate.Epistemic.OBSERVED, gate.Epistemic.VERIFIED}),
        consequence="repository write under bounded governance", reversible=True,
        risk=gate.Risk(1, 2, 1), alternatives=("do_not_execute",),
        expected_value="authorized bounded mutation", required_permission="repo_write",
        verification=gate.VerificationPlan("post-write state", "verification passes", ("stop",)),
        necessary_power=frozenset({"repo_write"}), requested_power=frozenset({"repo_write"}),
    )
    values.update(overrides)
    return gate.DecisionObject(**values)


def repo_action(paths=MUTATION_PATHS, decision_id="CP12-REPO-DEC", **overrides):
    values = dict(
        action_id="CP12-REPO-ACT", action_type="repository_write",
        target=BOUNDARY.repo_mutation_target(repository=REPOSITORY, target_paths=paths),
        purpose=REPO_PURPOSE, scope=REPO_SCOPE, actor_id=PRINCIPAL, permission="repo_write",
        decision_id=decision_id, authority_id=REPO_AID,
    )
    values.update(overrides)
    return values


def issue(gate, *, deploy=True, now=None, **action_overrides):
    aid = DEPLOY_AID if deploy else REPO_AID
    authority = gate._current_registry().resolve(aid)
    decision = deploy_decision() if deploy else repo_decision()
    action = deploy_action(**action_overrides) if deploy else repo_action(**action_overrides)
    return gate.authorize(authority=authority, decision=decision, action=action, now=now)


def issue_release_artifact(gate, now, private_hex, *, commit=COMMIT, environment="preview",
                           worker=WORKER, repository=REPOSITORY):
    decision = gate.authorize(
        authority=gate._current_registry().resolve(DEPLOY_AID),
        decision=deploy_decision(),
        action=deploy_action(commit=commit, environment=environment, worker=worker),
        now=now,
    )
    assert decision.allowed, decision.reasons
    return PORTA.issue_portable_authorization(
        execution_authorization=decision.authorization, registry=gate._current_registry(),
        commit_sha=commit, environment=environment, deployment_surface="cloudflare",
        worker_name=worker, repository=repository, private_key_hex=private_hex, now=now,
    )


def issue_mutation_artifact(gate, now, private_hex, *, paths=MUTATION_PATHS, repository=REPOSITORY):
    decision = gate.authorize(
        authority=gate._current_registry().resolve(REPO_AID),
        decision=repo_decision(),
        action=repo_action(paths=paths),
        now=now,
    )
    assert decision.allowed, decision.reasons
    return PORTA.issue_portable_authorization(
        execution_authorization=decision.authorization, registry=gate._current_registry(),
        commit_sha="", change_set=paths, repository=repository, private_key_hex=private_hex, now=now,
    )


def mutated_registry(*, authority_id=DEPLOY_AID, revoked=False, purpose=None, removed=False):
    loaded = GATE.load_registry()
    if removed:
        auths = {k: v for k, v in loaded.authorities.items() if k != authority_id}
        return GATE.AuthorityRegistry(authorities=auths)
    auths = dict(loaded.authorities)
    authority = auths[authority_id]
    auths[authority_id] = GATE.Authority(
        authority_id=authority.authority_id, principal_id=authority.principal_id,
        purpose=purpose or authority.purpose, scope=authority.scope,
        granted_actions=authority.granted_actions, expires_at=authority.expires_at,
        revoked=revoked,
    )
    return GATE.AuthorityRegistry(authorities=auths)


def verify_ok(artifact, public_hex, registry=None, now=None):
    return PORTA.verify_portable_authorization(
        artifact=artifact, public_key_hex=public_hex,
        registry=registry if registry is not None else GATE.load_registry(), now=now,
    )


class CP12Matrix(unittest.TestCase):
    results: dict[str, str] = {}
    subprocess_rows: list[str] = []

    def record(self, name: str, ok: bool, refused: bool, why: str = ""):
        CP12Matrix.results[name] = "REFUSED" if refused else "ALLOW"
        self.assertTrue(ok, why)


class FixturesMixin:
    @classmethod
    def setUpClass(cls):
        cls.priv, cls.pub = PORTA.generate_keypair()
        cls.now = now_iso()
        cls.gate = GATE.UniversalExecutionGate(GATE.load_registry())
        cls.release_artifact = issue_release_artifact(cls.gate, cls.now, cls.priv)
        cls.mutation_artifact = issue_mutation_artifact(cls.gate, cls.now, cls.priv)

    def registry(self):
        return GATE.load_registry()


class ProvenanceAndBindingTests(FixturesMixin, CP12Matrix):
    """T02-T11: forged, altered, and identity-swapped artifacts are refused."""

    def test_T02_forged_credential_refused(self):
        d = PORTA.portable_boundary_release(
            artifact={"schema": PORTA.SCHEMA, "authorization": {}, "signature": ""},
            public_key_hex=self.pub, registry=self.registry(), commit_sha=COMMIT,
            target_environment="preview", deployment_surface="cloudflare", worker_name=WORKER,
        )
        self.record("T02", not d.allowed, True, d.reason)

    def test_T03_altered_payload_refused(self):
        altered = json.loads(json.dumps(self.release_artifact))
        altered["authorization"]["scope"] = "public-runtime:elsewhere:/"
        ok, reasons = verify_ok(altered, self.pub)
        self.record("T03", not ok, True, "; ".join(reasons))

    def test_T04_altered_signature_refused(self):
        altered = json.loads(json.dumps(self.release_artifact))
        sig = altered["signature"]
        flipped = ("0" if sig[0] != "0" else "1") + sig[1:]
        altered["signature"] = flipped
        ok, reasons = verify_ok(altered, self.pub)
        self.record("T04", not ok, True, "; ".join(reasons))

    def test_T05_wrong_authority_refused(self):
        registry = mutated_registry(purpose="deploy a completely different service")
        ok, reasons = verify_ok(self.release_artifact, self.pub, registry=registry)
        self.record("T05", not ok and "fingerprint" in "; ".join(reasons), True, "; ".join(reasons))

    def test_T06_wrong_decision_refused(self):
        altered = json.loads(json.dumps(self.release_artifact))
        altered["authorization"]["decision_id"] = "SOME-OTHER-DECISION"
        ok, reasons = verify_ok(altered, self.pub)
        self.record("T06", not ok, True, "; ".join(reasons))

    def test_T07_wrong_action_refused(self):
        d = PORTA.portable_boundary_release(
            artifact=self.release_artifact, public_key_hex=self.pub, registry=self.registry(),
            commit_sha=COMMIT, target_environment="production", deployment_surface="cloudflare",
            worker_name=WORKER,
        )
        self.record("T07", not d.allowed, True, d.reason)

    def test_T08_wrong_actor_refused(self):
        altered = json.loads(json.dumps(self.release_artifact))
        altered["authorization"]["actor_id"] = "AttackerAccount"
        ok, reasons = verify_ok(altered, self.pub)
        self.record("T08", not ok, True, "; ".join(reasons))

    def test_T09_wrong_scope_refused(self):
        altered = json.loads(json.dumps(self.release_artifact))
        altered["authorization"]["scope"] = "public-runtime:attacker-worker-1:/"
        ok, reasons = verify_ok(altered, self.pub)
        self.record("T09", not ok, True, "; ".join(reasons))

    def test_T10_wrong_permission_refused(self):
        altered = json.loads(json.dumps(self.release_artifact))
        altered["authorization"]["permission"] = "repo_write"
        ok, reasons = verify_ok(altered, self.pub)
        self.record("T10", not ok and "binding_hash" not in "; ".join(reasons), True, "; ".join(reasons))

    def test_T11_wrong_action_type_refused(self):
        d = PORTA.portable_boundary_release(
            artifact=self.mutation_artifact, public_key_hex=self.pub, registry=self.registry(),
            commit_sha=COMMIT, target_environment="preview", deployment_surface="cloudflare",
            worker_name=WORKER,
        )
        self.record("T11", not d.allowed, True, d.reason)


class ExactTargetBindingTests(FixturesMixin, CP12Matrix):
    """T12-T18: a VALID artifact for ACTION A can never authorize ACTION B."""

    def test_T12_wrong_target_refused(self):
        d = PORTA.portable_boundary_release(
            artifact=self.release_artifact, public_key_hex=self.pub, registry=self.registry(),
            commit_sha=OTHER_COMMIT, target_environment="preview", deployment_surface="cloudflare",
            worker_name=WORKER,
        )
        self.record("T12", not d.allowed and "exact deploy target" in d.reason, True, d.reason)

    def test_T13_wrong_repository_refused(self):
        d = PORTA.portable_boundary_release(
            artifact=self.release_artifact, public_key_hex=self.pub, registry=self.registry(),
            commit_sha=COMMIT, target_environment="preview", deployment_surface="cloudflare",
            worker_name=WORKER, repository=OTHER_REPOSITORY,
        )
        self.record("T13", not d.allowed, True, d.reason)

    def test_T14_wrong_commit_refused(self):
        d = PORTA.portable_boundary_release(
            artifact=self.release_artifact, public_key_hex=self.pub, registry=self.registry(),
            commit_sha=OTHER_COMMIT, target_environment="preview", deployment_surface="cloudflare",
            worker_name=WORKER,
        )
        self.record("T14", not d.allowed, True, d.reason)

    def test_T15_wrong_change_set_refused(self):
        d = PORTA.portable_boundary_repo_mutation(
            artifact=self.mutation_artifact, public_key_hex=self.pub, registry=self.registry(),
            target_paths=MUTATION_PATHS_EXTRA,
        )
        self.record("T15", not d.allowed, True, d.reason)

    def test_T16_wrong_environment_refused(self):
        d = PORTA.portable_boundary_release(
            artifact=self.release_artifact, public_key_hex=self.pub, registry=self.registry(),
            commit_sha=COMMIT, target_environment="production", deployment_surface="cloudflare",
            worker_name=WORKER,
        )
        self.record("T16", not d.allowed, True, d.reason)

    def test_T17_wrong_deployment_surface_refused(self):
        d = PORTA.portable_boundary_release(
            artifact=self.release_artifact, public_key_hex=self.pub, registry=self.registry(),
            commit_sha=COMMIT, target_environment="preview", deployment_surface="vercel",
            project_id=VERCEL_PROJECT,
        )
        self.record("T17", not d.allowed, True, d.reason)

    def test_T18_wrong_worker_project_refused(self):
        d = PORTA.portable_boundary_release(
            artifact=self.release_artifact, public_key_hex=self.pub, registry=self.registry(),
            commit_sha=COMMIT, target_environment="preview", deployment_surface="cloudflare",
            worker_name=OTHER_WORKER,
        )
        self.record("T18", not d.allowed, True, d.reason)


class RevocationReplayTests(FixturesMixin, CP12Matrix):
    """T19-T27: time, revocation, and cross-context replay are bounded."""

    def test_T19_expired_refused(self):
        later = now_iso(offset_seconds=1600)
        ok, reasons = verify_ok(self.release_artifact, self.pub, now=later)
        self.record("T19", not ok and "expired" in "; ".join(reasons), True, "; ".join(reasons))

    def test_T20_revoked_before_use_refused(self):
        registry = mutated_registry(revoked=True)
        ok, reasons = verify_ok(self.release_artifact, self.pub, registry=registry)
        self.record("T20", not ok, True, "; ".join(reasons))

    def test_T21_revoked_after_issuance_refused(self):
        removed = mutated_registry(removed=True)
        revoked = mutated_registry(revoked=True)
        ok1, r1 = verify_ok(self.release_artifact, self.pub, registry=removed)
        ok2, r2 = verify_ok(self.release_artifact, self.pub, registry=revoked)
        self.record("T21", (not ok1) and (not ok2), True, f"{'; '.join(r1)} || {'; '.join(r2)}")

    def test_T22_copied_authorization_id_refused(self):
        forged = {
            "schema": PORTA.SCHEMA,
            "authorization": dict(self.release_artifact["authorization"]),
            "signature": "ab" * 32,
        }
        ok, reasons = verify_ok(forged, self.pub)
        self.record("T22", not ok, True, "; ".join(reasons))

    def test_T23_exact_replay_behavior_explicitly_defined(self):
        ok1, _ = verify_ok(self.release_artifact, self.pub, now=self.now)
        ok2, _ = verify_ok(self.release_artifact, self.pub, now=self.now)
        # Documented: deterministic same-action replay within validity is a
        # bounded re-execution, NOT a mint. It cannot move to any other action.
        self.assertTrue(ok1 and ok2, "valid artifact must re-verify while valid")
        self.record("T23", ok1 and ok2, False, "exact replay allowed only for the exact bound action within TTL; see report")

    def test_T24_cross_gate_replay_refused(self):
        other_pub = PORTA.generate_keypair()[1]
        ok, reasons = verify_ok(self.release_artifact, other_pub)
        self.record("T24", not ok, True, "; ".join(reasons))

    def test_T25_production_substitution_refused(self):
        d = PORTA.portable_boundary_release(
            artifact=self.release_artifact, public_key_hex=self.pub, registry=self.registry(),
            commit_sha=COMMIT, target_environment="production", deployment_surface="cloudflare",
            worker_name=WORKER,
        )
        self.record("T25", not d.allowed, True, d.reason)

    def test_T26_deployment_substitution_refused(self):
        d = PORTA.portable_boundary_release(
            artifact=self.mutation_artifact, public_key_hex=self.pub, registry=self.registry(),
            commit_sha=COMMIT, target_environment="preview", deployment_surface="cloudflare",
            worker_name=WORKER,
        )
        refused = (not d.allowed) and (
            "exact deploy target" in d.reason or "not a release action" in d.reason
        )
        self.record("T26", refused, True, d.reason)

    def test_T27_mutation_substitution_refused(self):
        d = PORTA.portable_boundary_repo_mutation(
            artifact=self.release_artifact, public_key_hex=self.pub, registry=self.registry(),
            target_paths=MUTATION_PATHS,
        )
        self.record("T27", not d.allowed, True, d.reason)


class CapabilityIsNotAuthorityTests(FixturesMixin, CP12Matrix):
    """T28-T34: tokens/triggers/strings/state are NEVER authorization."""

    def _release_refused(self, payload):
        return PORTA.portable_boundary_release(
            artifact=payload, public_key_hex=self.pub, registry=self.registry(),
            commit_sha=COMMIT, target_environment="production", deployment_surface="cloudflare",
            worker_name=WORKER,
        )

    def test_T28_github_token_without_authorization_refused(self):
        d = self._release_refused({"GITHUB_TOKEN": "ghs_x"})
        self.record("T28", not d.allowed, True, d.reason)

    def test_T29_workflow_dispatch_without_authorization_refused(self):
        d = self._release_refused({"workflow_dispatch": True, "confirm": "RELEASE_CANONICAL_HUB"})
        self.record("T29", not d.allowed, True, d.reason)

    def test_T30_approved_string_refused(self):
        d = self._release_refused({"approval": "EXPLICIT_APPROVAL_GRANTED"})
        self.record("T30", not d.allowed, True, d.reason)

    def test_T31_receipt_refused(self):
        d = self._release_refused({"receipt": {"status": "verified", "authorized": True}})
        self.record("T31", not d.allowed, True, d.reason)

    def test_T32_execution_state_refused(self):
        d = self._release_refused({"status": "EXECUTING", "EXECUTION-STATE": "CLOSED"})
        self.record("T32", not d.allowed, True, d.reason)

    def test_T33_model_approval_refused(self):
        d = self._release_refused({"model": "claude", "authorization": "approved"})
        self.record("T33", not d.allowed, True, d.reason)

    def test_T34_agent_approval_refused(self):
        d = self._release_refused({"agent": "deployer", "agent_authorized": True})
        self.record("T34", not d.allowed, True, d.reason)


class PositiveAndHarnessTests(FixturesMixin, CP12Matrix):
    """T35, T36, T37, T38: the genuine path ALLOWS; process isolation holds."""

    def test_T35_exact_genuine_credential_allows(self):
        release = PORTA.portable_boundary_release(
            artifact=self.release_artifact, public_key_hex=self.pub, registry=self.registry(),
            commit_sha=COMMIT, target_environment="preview", deployment_surface="cloudflare",
            worker_name=WORKER,
        )
        mutation = PORTA.portable_boundary_repo_mutation(
            artifact=self.mutation_artifact, public_key_hex=self.pub, registry=self.registry(),
            target_paths=MUTATION_PATHS,
        )
        self.record("T35", release.allowed and mutation.allowed, False,
                    f"{release.reason} || {mutation.reason}")

    def _popen(self, code: str, args: list[str]) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, "-c", code, *args], capture_output=True, text=True, timeout=120,
        )

    def test_T36_T01_independent_verifier_has_no_issuer_memory(self):
        work = TMP / "cross"
        work.mkdir(exist_ok=True)
        artifact_path = work / "artifact.json"
        pub_path = work / "public.hex"
        artifact_path.write_text(json.dumps(self.release_artifact), encoding="utf-8")
        pub_path.write_text(self.pub, encoding="utf-8")
        quoted_artifact = repr(str(artifact_path))
        quoted_pub = repr(str(pub_path))

        # A SEPARATE interpreter that has NEVER seen the issuer's gate or its
        # in-process `_issued` set verifies the artifact using only the public
        # key pin + the canonical registry.
        code2 = (
            "import importlib.util,sys,json\n"
            "from pathlib import Path\n"
            f"ROOT=Path({str(ROOT)!r})\n"
            "def load(n,p):\n"
            " s=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(s)\n"
            " sys.modules[n]=m; s.loader.exec_module(m); return m\n"
            f"G=load('cp_gate',ROOT/'.naya/runtime/universal_execution_gate.py')\n"
            f"P=load('cp_porta',ROOT/'.naya/runtime/portable_authorization.py')\n"
            f"art=json.loads(Path({quoted_artifact}).read_text(encoding='utf-8'))\n"
            "reg=G.load_registry()\n"
            f"pub=Path({quoted_pub}).read_text(encoding='utf-8').strip()\n"
            "ok,reasons=P.verify_portable_authorization(artifact=art,public_key_hex=pub,registry=reg)\n"
            "print('VERIFIER_GREEN' if ok else 'VERIFIER_RED '+'; '.join(reasons))\n"
        )
        result = self._popen(code2, [])
        output = result.stdout.strip()
        CP12Matrix.subprocess_rows.append(f"T36/T01 verifier process -> {output}")
        self.record("T36", result.returncode == 0 and output.startswith("VERIFIER_GREEN"), False,
                    f"subprocess verifier output: {output} (stderr: {result.stderr[:200]})")
        self.record("T01", result.returncode == 0 and output.startswith("VERIFIER_GREEN"), False,
                    f"subprocess verifier output: {output} (stderr: {result.stderr[:200]})")

    def test_T37_verifier_cannot_mint_a_new_credential(self):
        work = TMP / "mint"
        work.mkdir(exist_ok=True)
        quoted_pinned = repr(str(work / "pinned.hex"))
        artifact_path = work / "artifact.json"
        artifact_path.write_text(json.dumps(self.release_artifact), encoding="utf-8")
        (work / "pinned.hex").write_text(self.pub, encoding="utf-8")
        code = (
            "import importlib.util,sys,json\n"
            "from pathlib import Path\n"
            f"ROOT=Path({str(ROOT)!r})\n"
            "def load(n,p):\n"
            " s=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(s)\n"
            " sys.modules[n]=m; s.loader.exec_module(m); return m\n"
            f"G=load('mn_gate',ROOT/'.naya/runtime/universal_execution_gate.py')\n"
            f"P=load('mn_porta',ROOT/'.naya/runtime/portable_authorization.py')\n"
            f"pinned=Path({quoted_pinned}).read_text(encoding='utf-8').strip()\n"
            f"artifact=json.loads(Path({repr(str(artifact_path))}).read_text(encoding='utf-8'))\n"
            # the verifier crafts a SELF-consistent credential using its own key
            "own_priv, own_pub = P.generate_keypair()\n"
            "auth_obj=artifact['authorization']\n"
            "crafted=dict(auth_obj)\n"
            "crafted['actor_id']='Runner'  # bound to a different actor\n"
            "from hashlib import sha256\n"
            "binding=sha256('|'.join([crafted['authority_id'],crafted['decision_id'],crafted['action_id'],"
            "crafted['action_type'],crafted['target'],crafted['actor_id'],crafted['scope'],crafted['permission']]).encode()).hexdigest()\n"
            "crafted['binding_hash']=binding\n"
            "msg=P._canonical_json(crafted).encode('utf-8')\n"
            "sig=P._sign(own_priv,msg)\n"
            "minted={'schema':P.SCHEMA,'authorization':crafted,'signature':sig}\n"
            "ok,reasons=P.verify_portable_authorization(artifact=minted,public_key_hex=pinned,registry=G.load_registry())\n"
            "print('REFUSED' if not ok else 'MINTED')\n"
        )
        result = self._popen(code, [])
        output = result.stdout.strip()
        CP12Matrix.subprocess_rows.append(f"T37 verifier-mint attempt -> {output}")
        self.record("T37", result.returncode == 0 and output.startswith("REFUSED"), True,
                    f"verifier mint output: {output} (stderr: {result.stderr[:200]})")

    def test_T38_direct_bypass_harness_refused(self):
        vectors = {
            "github-token": {"GITHUB_TOKEN": "ghp_x"},
            "workflow-dispatch": {"workflow_dispatch": True},
            "approval-string": {"approved": True, "approval": "EXPLICIT_APPROVAL_GRANTED"},
            "exec-executing": {"status": "EXECUTING", "EXECUTION-STATE": "CLAIMED"},
            "receipt": {"receipt": {"status": "verified", "authorized": True}},
            "claim": {"claim_id": "CL-1", "claim": {"status": "CLAIMED"}},
            "magic-string": {"confirm": "RELEASE_CANONICAL_HUB"},
            "provider-credentials": {"CLOUDFLARE_API_TOKEN": "x", "VERCEL_TOKEN": "y"},
            "authz-idi": {"authorized_by": "SoulSchoolAcademy"},
        }
        for name, payload in vectors.items():
            d = PORTA.portable_boundary_release(
                artifact=payload, public_key_hex=self.pub, registry=self.registry(),
                commit_sha=COMMIT, target_environment="production", deployment_surface="cloudflare",
                worker_name=WORKER,
            )
            self.record(f"T38-{name}", not d.allowed, True, d.reason)


CP12Matrix.results = {}


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ProvenanceAndBindingTests)
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(ExactTargetBindingTests))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(RevocationReplayTests))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(CapabilityIsNotAuthorityTests))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(PositiveAndHarnessTests))
    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(suite)
    refused = sum(1 for v in CP12Matrix.results.values() if v == "REFUSED")
    allowed = sum(1 for v in CP12Matrix.results.values() if v == "ALLOW")
    print(f"CROSS_PROCESS_AUTHORIZATION_CLOSURE = matrix cases={len(CP12Matrix.results)} "
          f"refused={refused} allowed={allowed}")
    for row in CP12Matrix.subprocess_rows:
        print(row)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())