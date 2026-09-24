#!/usr/bin/env python3
"""RED-FIRST cross-process adversarial suite for portable INTELLIGENCE_COMMIT authorization."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

RUNTIME = Path(__file__).resolve().parent
sys.path.insert(0, str(RUNTIME))
sys.path.insert(0, str(RUNTIME.parent / "governance"))

from governance_kernel import Authority, AuthorityRegistry, DecisionObject, Epistemic, Risk, VerificationPlan
from portable_authorization import (
    INTELLIGENCE_COMMIT_ACTION_TYPE,
    INTELLIGENCE_COMMIT_PERMISSION,
    INTELLIGENCE_COMMIT_TARGET,
    issue_portable_authorization,
    generate_keypair,
    verify_portable_authorization,
)
from universal_execution_gate import ExecutionAuthorization, UniversalExecutionGate


ISSUED_AT = "2026-01-01T00:00:00+00:00"
SOURCE_SHA = "d253610f8ff8f27a838294a04c8893bf71bf7d4e"


def build_gate():
    authority = Authority(
        authority_id="redfirst-authority",
        principal_id="redfirst-actor",
        purpose="RED-FIRST portable intelligence commit proof",
        scope="NayaNET",
        granted_actions=frozenset({INTELLIGENCE_COMMIT_PERMISSION}),
        expires_at="2030-01-01T00:00:00+00:00",
        revoked=False,
    )
    registry = AuthorityRegistry(authorities={authority.authority_id: authority})
    decision = DecisionObject(
        decision_id="redfirst-decision",
        mission="RED-FIRST portable intelligence commit proof",
        actor_id=authority.principal_id,
        action=INTELLIGENCE_COMMIT_PERMISSION,
        purpose=authority.purpose,
        scope=authority.scope,
        current_truth="A bounded intelligence commit is the verification target.",
        gap="The serialized authorization must prove gate issuance across a process boundary.",
        evidence=("RED-FIRST source/test evidence",),
        epistemic=frozenset({Epistemic.OBSERVED, Epistemic.VERIFIED}),
        consequence="persist one bounded intelligence record",
        reversible=True,
        risk=Risk(uncertainty=1, consequence=2, irreversibility=1),
        alternatives=("do_not_execute",),
        expected_value="reconstructable governed intelligence commit",
        required_permission=INTELLIGENCE_COMMIT_PERMISSION,
        verification=VerificationPlan(
            observation="portable authorization verification result",
            success_criteria="fresh process accepts only the genuine signed credential",
        ),
        necessary_power=frozenset({INTELLIGENCE_COMMIT_PERMISSION}),
        requested_power=frozenset({INTELLIGENCE_COMMIT_PERMISSION}),
    )
    action = {
        "action_id": "redfirst-action",
        "action_type": INTELLIGENCE_COMMIT_ACTION_TYPE,
        "target": INTELLIGENCE_COMMIT_TARGET,
        "purpose": authority.purpose,
        "scope": authority.scope,
        "actor_id": authority.principal_id,
        "permission": INTELLIGENCE_COMMIT_PERMISSION,
        "decision_id": decision.decision_id,
        "authority_id": authority.authority_id,
    }
    gate = UniversalExecutionGate(registry=registry)
    issued = gate.authorize(authority=authority, decision=decision, action=action, now=ISSUED_AT)
    assert issued.allowed and issued.authorization is not None, issued.reasons
    return gate, registry, authority, issued.authorization


def fresh_verify(artifact, registry_path, public_key, now):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump(artifact, f)
        artifact_path = f.name
    code = (
        "import json,sys;"
        "from pathlib import Path;"
        "sys.path.insert(0," + repr(str(RUNTIME)) + ");"
        "sys.path.insert(0," + repr(str(RUNTIME.parent / "governance")) + ");"
        "from universal_execution_gate import load_registry;"
        "from portable_authorization import verify_portable_authorization;"
        "artifact=json.load(open(sys.argv[1],encoding='utf-8'));"
        "registry=load_registry(sys.argv[2]);"
        "ok,reasons=verify_portable_authorization(artifact=artifact,public_key_hex=sys.argv[3],registry=registry,now=sys.argv[4]);"
        "print(json.dumps({'ok':ok,'reasons':reasons}));"
        "raise SystemExit(0 if ok else 1)"
    )
    proc = subprocess.run(
        [sys.executable, "-c", code, artifact_path, str(registry_path), public_key, now],
        cwd=RUNTIME.parents[2],
        text=True,
        capture_output=True,
    )
    Path(artifact_path).unlink(missing_ok=True)
    try:
        result = json.loads(proc.stdout.strip().splitlines()[-1])
    except Exception:
        result = {"ok": False, "reasons": ("child-process-output-invalid", proc.stdout, proc.stderr)}
    return proc.returncode == 0, tuple(result.get("reasons", ()))


def write_registry(registry, path):
    authorities = []
    for authority in registry.authorities.values():
        authorities.append({
            "authority_id": authority.authority_id,
            "principal_id": authority.principal_id,
            "purpose": authority.purpose,
            "scope": authority.scope,
            "granted_actions": sorted(authority.granted_actions),
            "expires_at": authority.expires_at,
            "revoked": bool(authority.revoked),
        })
    path.write_text(json.dumps({"authorities": authorities}, indent=2), encoding="utf-8")


def main():
    gate, registry, authority, execution_authorization = build_gate()
    private_key, public_key = generate_keypair()

    with tempfile.TemporaryDirectory() as td:
        registry_path = Path(td) / "registry.json"
        write_registry(registry, registry_path)

        artifact = issue_portable_authorization(
            execution_authorization=execution_authorization,
            registry=registry,
            gate=gate,
            commit_sha=SOURCE_SHA,
            private_key_hex=private_key,
            repository="SoulSchoolAcademy/NayaPOWER",
            now=ISSUED_AT,
            expires_in_seconds=60,
        )

        # 1-3 + 8: genuine gate issuance -> serialization -> fresh independent process -> PASS.
        ok, reasons = fresh_verify(artifact, registry_path, public_key, ISSUED_AT)
        assert ok, ("LEGITIMATE credential failed in fresh process", reasons)

        # 4: tamper one signed field -> FAIL.
        tampered = copy.deepcopy(artifact)
        tampered["authorization"]["target"] = "evil-target"
        ok, _ = fresh_verify(tampered, registry_path, public_key, ISSUED_AT)
        assert not ok, "tampered authorization unexpectedly verified"

        # 5: sign the same credential with a wrong key -> FAIL.
        wrong_private, _ = generate_keypair()
        wrong = copy.deepcopy(artifact)
        from portable_authorization import _canonical_json, _sign
        wrong["signature"] = _sign(wrong_private, _canonical_json(wrong["authorization"]).encode("utf-8"))
        ok, _ = fresh_verify(wrong, registry_path, public_key, ISSUED_AT)
        assert not ok, "wrong-key signature unexpectedly verified"

        # 6: identical unsigned credential -> FAIL.
        unsigned = copy.deepcopy(artifact)
        unsigned.pop("signature")
        ok, _ = fresh_verify(unsigned, registry_path, public_key, ISSUED_AT)
        assert not ok, "unsigned credential unexpectedly verified"

        # 7a: replay after expiry -> FAIL.
        ok, reasons = fresh_verify(artifact, registry_path, public_key, "2026-01-01T00:01:01+00:00")
        assert not ok and any("expired" in str(r) for r in reasons), reasons

        # 7b: replay after revocation -> FAIL.
        revoked_registry = AuthorityRegistry(authorities={
            authority.authority_id: Authority(
                authority_id=authority.authority_id,
                principal_id=authority.principal_id,
                purpose=authority.purpose,
                scope=authority.scope,
                granted_actions=authority.granted_actions,
                expires_at=authority.expires_at,
                revoked=True,
            )
        })
        revoked_path = Path(td) / "revoked-registry.json"
        write_registry(revoked_registry, revoked_path)
        ok, reasons = fresh_verify(artifact, revoked_path, public_key, "2026-01-01T00:00:30+00:00")
        assert not ok and any("fingerprint" in str(r) or "no longer permits" in str(r) for r in reasons), reasons

        # Additional provenance RED: identical dataclass not issued by the gate must not be signable.
        forged = ExecutionAuthorization(**execution_authorization.__dict__)
        foreign_gate = UniversalExecutionGate(registry=registry)
        try:
            issue_portable_authorization(
                execution_authorization=forged,
                registry=registry,
                gate=foreign_gate,
                commit_sha=SOURCE_SHA,
                private_key_hex=private_key,
                repository="SoulSchoolAcademy/NayaPOWER",
                now=ISSUED_AT,
                expires_in_seconds=60,
            )
        except ValueError:
            pass
        else:
            raise AssertionError("non-gate credential was accepted for signing")

    print("RED_FIRST_PORTABLE_INTELLIGENCE_COMMIT=PASS")
    print("1 gate issues: PASS")
    print("2 serialize: PASS")
    print("3 fresh independent process verifies: PASS")
    print("4 tamper one field: FAIL (rejected)")
    print("5 wrong signing key: FAIL (rejected)")
    print("6 identical unsigned credential: FAIL (rejected)")
    print("7 expiry/revocation replay: FAIL (rejected)")
    print("8 legitimate credential: PASS")
    print("9 live causal transaction: NOT RUN")
    print("10 storage/receipt/attestation reconstruction: NOT RUN")


if __name__ == "__main__":
    main()
