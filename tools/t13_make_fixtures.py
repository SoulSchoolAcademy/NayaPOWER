#!/usr/bin/env python3
"""Test #13 fixture generator (ISSUER-side tool; runs ONLY where the test
signing key may exist - i.e. the human's controlled environment).

Generated fixture set is PUBLIC and signature-secured. The Ed25519 test private
key NEVER leaves this machine and is NEVER written to the repository or to the
output fixtures directory.

Usage:
    python tools/t13_make_fixtures.py [output_fixtures_dir] [--keyseat <path>]

The keyseat path (private key) is expected to live OUTSIDE the fixtures dir.
If --keyseat is omitted, a fresh seat is created under the OS temp dir.
A freshness fingerprint of the run is printed (never the key itself).
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


GATE = load("t13f_gate", ROOT / ".naya/runtime/universal_execution_gate.py")
PORTA = load("t13f_porta", ROOT / ".naya/runtime/portable_authorization.py")

REPOSITORY = "SoulSchoolAcademy/NayaPOWER"
PRINCIPAL = "SoulSchoolAcademy"
COMMIT = "896594e9453312d85b00a5d4c6e5d41d29f72d76"
WORKER = "test-13-runner-verify-a7b9"
OTHER_WORKER = "test-13-runner-attacker-c3d4"
OTHER_REPOSITORY = "OtherOrg/NayaPOWER"
OTHER_COMMIT = "b" * 40
DEPLOY_AID = "HUMAN-SOULSCHOOLACADEMY-HUB-DEPLOY-509"
DEPLOY_PURPOSE = "deploy the canonical 509 NayaNET Intelligent Hub public runtime"
DEPLOY_SCOPE = "public-runtime:sparkling-shape-7ae5:/"
CONTEXT = {
    "commit_sha": COMMIT,
    "target_environment": "preview",
    "deployment_surface": "cloudflare",
    "repository": REPOSITORY,
    "worker_name": WORKER,
}


def now_iso(offset=0):
    return (datetime.now(timezone.utc) + timedelta(seconds=offset)).isoformat()


def deploy_decision(decision_id="T13-DEPLOY-DEC", **o):
    v = dict(
        decision_id=decision_id, mission="Test #13 runner verification (no side effect)",
        actor_id=PRINCIPAL, action="deploy_public_runtime", purpose=DEPLOY_PURPOSE,
        scope=DEPLOY_SCOPE, current_truth="runner verifies the portable credential",
        gap="credential must be understood by an independent runner", evidence=("evidence:registry-grant",),
        epistemic=frozenset({GATE.Epistemic.OBSERVED, GATE.Epistemic.VERIFIED}),
        consequence="verification only; never a real deploy", reversible=True,
        risk=GATE.Risk(1, 1, 1), alternatives=("do_not_verify",),
        expected_value="prove cross-process authorization", required_permission="deploy_public_runtime",
        verification=GATE.VerificationPlan("runner ALLOW/REFUSED", "matches reference matrix", ("stop",)),
        necessary_power=frozenset({"deploy_public_runtime"}),
        requested_power=frozenset({"deploy_public_runtime"}),
    )
    v.update(o)
    return GATE.DecisionObject(**v)


def deploy_action(commit=COMMIT, environment="preview", worker=WORKER, decision_id="T13-DEPLOY-DEC",
                  repository=REPOSITORY, **o):
    v = dict(
        action_id="T13-DEPLOY-ACT", action_type="deploy_public_runtime",
        target=PORTA.DEPLOY_TARGET(deployment_surface="cloudflare", environment=environment,
                                   repository=repository, commit_sha=commit, worker_name=worker),
        purpose=DEPLOY_PURPOSE, scope=DEPLOY_SCOPE, actor_id=PRINCIPAL,
        permission="deploy_public_runtime", decision_id=decision_id, authority_id=DEPLOY_AID,
    )
    v.update(o)
    return v


def issue_artifact(gate, now, key, *, commit=COMMIT, environment="preview", worker=WORKER,
                   repository=REPOSITORY, expires_in=900):
    res = gate.authorize(
        authority=gate._current_registry().resolve(DEPLOY_AID),
        decision=deploy_decision(),
        action=deploy_action(commit=commit, environment=environment, worker=worker,
                             repository=repository),
        now=now,
    )
    assert res.allowed, res.reasons
    return PORTA.issue_portable_authorization(
        execution_authorization=res.authorization, registry=gate._current_registry(),
        commit_sha=commit, environment=environment, deployment_surface="cloudflare",
        worker_name=worker, repository=repository, private_key_hex=key, now=now,
        expires_in_seconds=expires_in,
    )


def sign_authorization_dict(auth_dict, key):
    msg = PORTA._canonical_json(auth_dict).encode("utf-8")
    return PORTA._sign(key, msg)


def canonical_registry_payload():
    return json.loads((ROOT / ".naya/governance/authority-registry.json").read_text(encoding="utf-8"))


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("out", nargs="?", default=str(ROOT / ".naya/github-actions/test-13-fixtures"))
    ap.add_argument("--keyseat", default=None)
    args = ap.parse_args()

    out = Path(args.out)
    keyseat = Path(args.keyseat) if args.keyseat else None
    if keyseat is None:
        keyseat = Path(tempfile.gettempdir()) / "t13-test-signing-seat" / "private.hex"
    keyseat.parent.mkdir(parents=True, exist_ok=True)

    now = now_iso()
    gate = GATE.UniversalExecutionGate(GATE.load_registry())
    if keyseat.is_file():
        priv = keyseat.read_text(encoding="utf-8").strip()
        if len(priv) != 64:
            raise SystemExit("invalid keyseat contents; refusing to continue")
    else:
        priv, _ = PORTA.generate_keypair()
        keyseat.write_text(priv, encoding="utf-8")
    _, pub = PORTA.generate_keypair()  # placeholder; recompute below
    pub = _public_of(priv)

    cases_dir = out / "cases"
    regs_dir = out / "registries"
    base_registry = canonical_registry_payload()
    write_json(out / "registry.json", base_registry)
    (out / "public.hex").write_text(pub, encoding="utf-8")
    write_json(out / "context.json", {"now": now, **CONTEXT})

    genuine = issue_artifact(gate, now, priv)
    write_json(cases_dir / "T01-genuine.json",
               {"id": "T01", "mode": "release", "expected": "ALLOW", "artifact": genuine,
                "context": CONTEXT})
    write_json(cases_dir / "T02-altered-signature.json",
               {"id": "T02", "mode": "release", "expected": "REFUSED",
                "artifact": _mutate(genuine, {"signature": _flip(genuine["signature"])}),
                "context": CONTEXT})
    write_json(cases_dir / "T03-altered-payload.json",
               {"id": "T03", "mode": "release", "expected": "REFUSED",
                "artifact": _mutate(genuine, {"authorization": {
                    **genuine["authorization"], "actor_id": "SomeOtherActor"}}, deep=True),
                "context": CONTEXT})
    other_priv, other_pub = PORTA.generate_keypair()
    write_json(cases_dir / "T04-different-public-key.json",
               {"id": "T04", "mode": "release", "expected": "REFUSED",
                "public_key_hex": other_pub, "artifact": genuine, "context": CONTEXT})
    write_json(cases_dir / "T05-different-authority-id.json",
               {"id": "T05", "mode": "release", "expected": "REFUSED",
                "artifact": _mutate(genuine, {
                    "authorization": {**genuine["authorization"],
                                      "authority_id": "HUMAN-SOULSCHOOLACADEMY-REPO-WRITE"}}, deep=True),
                "context": CONTEXT})
    write_json(cases_dir / "T06-altered-authority-fingerprint.json",
               {"id": "T06", "mode": "release", "expected": "REFUSED",
                "artifact": _mutate(genuine, {"authorization": {
                    **genuine["authorization"], "authority_fingerprint": "0" * 64}}, deep=True),
                "context": CONTEXT})
    write_json(cases_dir / "T07-different-action-id.json",
               {"id": "T07", "mode": "release", "expected": "REFUSED",
                "artifact": _mutate(genuine, {"authorization": {
                    **genuine["authorization"], "action_id": "ATTACK-ACT-999"}}, deep=True),
                "context": CONTEXT})
    write_json(cases_dir / "T08-different-decision-id.json",
               {"id": "T08", "mode": "release", "expected": "REFUSED",
                "artifact": _mutate(genuine, {"authorization": {
                    **genuine["authorization"], "decision_id": "ATTACK-DEC-999"}}, deep=True),
                "context": CONTEXT})
    write_json(cases_dir / "T09-different-actor.json",
               {"id": "T09", "mode": "release", "expected": "REFUSED",
                "artifact": _mutate(genuine, {"authorization": {
                    **genuine["authorization"], "actor_id": "attacker"}}, deep=True),
                "context": CONTEXT})
    write_json(cases_dir / "T10-different-permission.json",
               {"id": "T10", "mode": "release", "expected": "REFUSED",
                "artifact": _mutate(genuine, {"authorization": {
                    **genuine["authorization"], "permission": "repo_write"}}, deep=True),
                "context": CONTEXT})
    write_json(cases_dir / "T11-different-scope.json",
               {"id": "T11", "mode": "release", "expected": "REFUSED",
                "artifact": _mutate(genuine, {"authorization": {
                    **genuine["authorization"], "scope": "public-runtime:attacker:/"}}, deep=True),
                "context": CONTEXT})
    write_json(cases_dir / "T12-different-action-type.json",
               {"id": "T12", "mode": "release", "expected": "REFUSED",
                "artifact": _mutate(genuine, {"authorization": {
                    **genuine["authorization"], "action_type": "repository_write"}}, deep=True),
                "context": CONTEXT})
    # T13-T18: VALID artifacts purpose-issued for a DIFFERENT bound action.
    other_ctx = {**CONTEXT, "commit_sha": OTHER_COMMIT}
    write_json(cases_dir / "T13-different-target.json",
               {"id": "T13", "mode": "release", "expected": "REFUSED",
                "artifact": issue_artifact(gate, now, priv, commit=OTHER_COMMIT),
                "context": CONTEXT})
    write_json(cases_dir / "T14-different-repository.json",
               {"id": "T14", "mode": "release", "expected": "REFUSED",
                "artifact": issue_artifact(gate, now, priv, repository=OTHER_REPOSITORY),
                "context": CONTEXT})
    write_json(cases_dir / "T15-different-commit.json",
               {"id": "T15", "mode": "release", "expected": "REFUSED",
                "artifact": issue_artifact(gate, now, priv, commit=OTHER_COMMIT),
                "context": CONTEXT})
    write_json(cases_dir / "T16-different-environment.json",
               {"id": "T16", "mode": "release", "expected": "REFUSED",
                "artifact": issue_artifact(gate, now, priv, environment="preview"),
                "context": {**CONTEXT, "target_environment": "production"}})
    write_json(cases_dir / "T17-different-deployment-surface.json",
               {"id": "T17", "mode": "release", "expected": "REFUSED",
                "artifact": issue_artifact(gate, now, priv),
                "context": {**CONTEXT, "deployment_surface": "vercel", "worker_name": None,
                            "project_id": "nayapower-canonical"}})
    write_json(cases_dir / "T18-different-worker-project.json",
               {"id": "T18", "mode": "release", "expected": "REFUSED",
                "artifact": issue_artifact(gate, now, priv, worker=OTHER_WORKER),
                "context": CONTEXT})
    # T19: genuinely signed but expired.
    auth = dict(genuine["authorization"])
    auth["expires_at"] = (datetime.now(timezone.utc) - timedelta(seconds=60)).isoformat()
    write_json(cases_dir / "T19-expired.json",
               {"id": "T19", "mode": "release", "expected": "REFUSED",
                "artifact": {"schema": PORTA.SCHEMA, "authorization": auth,
                             "signature": sign_authorization_dict(auth, priv)},
                "context": CONTEXT})
    # T20/T21/T22: registry variants.
    revoked = json.loads(json.dumps(base_registry))
    for a in revoked.get("authorities", []):
        if a.get("authority_id") == DEPLOY_AID:
            a["revoked"] = True
    write_json(regs_dir / "registry-revoked.json", revoked)
    write_json(cases_dir / "T20-revoked-authority.json",
               {"id": "T20", "mode": "release", "expected": "REFUSED",
                "artifact": genuine, "registry_path": "registries/registry-revoked.json",
                "context": CONTEXT})
    removed = {"authorities": [a for a in base_registry.get("authorities", [])
                               if a.get("authority_id") != DEPLOY_AID]}
    write_json(regs_dir / "registry-removed.json", removed)
    write_json(cases_dir / "T21-removed-authority.json",
               {"id": "T21", "mode": "release", "expected": "REFUSED",
                "artifact": genuine, "registry_path": "registries/registry-removed.json",
                "context": CONTEXT})
    modified = json.loads(json.dumps(base_registry))
    for a in modified.get("authorities", []):
        if a.get("authority_id") == DEPLOY_AID:
            a["purpose"] = "purposed rewritten by attacker"
    write_json(regs_dir / "registry-modified.json", modified)
    write_json(cases_dir / "T22-modified-grant.json",
               {"id": "T22", "mode": "release", "expected": "REFUSED",
                "artifact": genuine, "registry_path": "registries/registry-modified.json",
                "context": CONTEXT})
    # T23-T31, T36: capability payloads / bypass (no artifact).
    bypass = [
        ("T23", "github-token", {"GITHUB_TOKEN": "ghp_X"}),
        ("T24", "dispatch-approved", {"workflow_dispatch": True, "inputs": {"approved": "true"}}),
        ("T25", "authorization-approved", {"authorization": "approved", "approved_by": "model"}),
        ("T26", "fabricated-receipt", {"receipt": {"status": "verified", "authorized": True}}),
        ("T27", "fabricated-claim", {"claim_id": "CL-X", "claim": {"status": "CLAIMED"}}),
        ("T28", "execution-state", {"status": "EXECUTING", "EXECUTION-STATE": "CLOSED"}),
        ("T29", "model-approval", {"model": "claude", "authorization": "approved"}),
        ("T30", "agent-approval", {"agent": "deploy-bot", "agent_authorized": True}),
        ("T31", "provider-credential", {"CLOUDFLARE_API_TOKEN": "x", "VERCEL_TOKEN": "y"}),
        ("T36", "direct-bypass", None),
    ]
    for tid, name, payload in bypass:
        write_json(cases_dir / f"{tid}-{name}.json",
                   {"id": tid, "mode": "bypass", "expected": "REFUSED", "payload": payload,
                    "context": CONTEXT})
    # T32/T33: genuine artifact re-verified in a fresh environment (evidence modes).
    write_json(cases_dir / "T32-no-issuer-memory.json",
               {"id": "T32", "mode": "memory", "expected": "ALLOW", "artifact": genuine,
                "context": CONTEXT})
    write_json(cases_dir / "T33-no-private-key.json",
               {"id": "T33", "mode": "memory", "expected": "ALLOW", "artifact": genuine,
                "context": CONTEXT})
    write_json(cases_dir / "T34-cannot-mint.json",
               {"id": "T34", "mode": "mint", "expected": "REFUSED",
                "artifact": genuine, "context": CONTEXT})
    write_json(cases_dir / "T35-copied-artifact-rebound.json",
               {"id": "T35", "mode": "release", "expected": "REFUSED",
                "artifact": _mutate(genuine, {"authorization": {
                    **genuine["authorization"], "target": OTHER_COMMIT, "commit_sha": OTHER_COMMIT}}, deep=True),
                "context": {**CONTEXT, "commit_sha": OTHER_COMMIT}})

    matrix = {"schema": "naya/test-13-matrix/v1", "repository": REPOSITORY,
              "cases": []}
    for path in sorted(cases_dir.glob("*.json")):
        case = json.loads(path.read_text(encoding="utf-8"))
        matrix["cases"].append({"id": case["id"], "file": f"cases/{path.name}",
                                "expected": case["expected"]})
    write_json(out / "matrix.json", matrix)
    print(f"T13_FIXTURES_GENERATED run_fingerprint={hashlib.sha256(priv.encode()).hexdigest()[:12]}")
    print(f"T13_FIXTURES_DIR={out}")
    print(f"T13_KEYSEAT={keyseat}")
    print(f"T13_CASES={len(matrix['cases'])}")
    return 0


def _public_of(priv):
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    return Ed25519PrivateKey.from_private_bytes(bytes.fromhex(priv)).public_key().public_bytes_raw().hex()


def _mutate(base, patch, deep=False):
    if deep:
        out = json.loads(json.dumps(base))
        au = dict(out["authorization"])
        for k, v in patch["authorization"].items():
            au[k] = v
        out["authorization"] = au
        return out
    out = dict(base)
    out.update(patch)
    return out


def _flip(hexstr):
    return ("0" if hexstr[0] != "0" else "1") + hexstr[1:]


if __name__ == "__main__":
    raise SystemExit(main())