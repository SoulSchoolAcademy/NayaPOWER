#!/usr/bin/env python3
"""Independent runner for a governed Cloudflare portable authorization.

This process is intentionally independent of the issuer's in-process UEG
memory. It verifies the signed portable artifact against the current authority
registry, checks the exact source checkout, enforces single-use replay
protection when a lock file is supplied, and only then invokes the concrete
Cloudflare production adapter.

Exit codes:
  0 = external action executed and a verified machine receipt was written
  3 = governed refusal (bad/revoked/replayed authorization)
  4 = execution failure
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


ROOT = Path(__file__).resolve().parents[1]
PORTA = load("naya_portable_authorization_runner", ROOT / ".naya/runtime/portable_authorization.py")
ADAPTER = load("naya_cloudflare_production_adapter_runner", ROOT / ".naya/runtime/cloudflare_production_adapter.py")

SCHEMA = PORTA.SCHEMA


def canonical_hash(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def current_commit(source_dir: Path) -> str:
    proc = subprocess.run(
        ["git", "-C", str(source_dir), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    )
    return proc.stdout.strip()


def write_receipt(path: Path, receipt: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--artifact", required=True)
    ap.add_argument("--public-key", required=True)
    ap.add_argument("--registry", required=True)
    ap.add_argument("--source-dir", required=True)
    ap.add_argument("--receipt", required=True)
    ap.add_argument("--replay-lock", default=None)
    args = ap.parse_args()

    now = datetime.now(timezone.utc).isoformat()
    artifact_path = Path(args.artifact).resolve()
    source_dir = Path(args.source_dir).resolve()
    receipt_path = Path(args.receipt).resolve()
    lock_path = Path(args.replay_lock).resolve() if args.replay_lock else None

    artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
    public_key = Path(args.public_key).read_text(encoding="utf-8").strip()
    registry = PORTA._LOAD_REGISTRY(Path(args.registry))

    authorization = artifact.get("authorization") if isinstance(artifact, dict) else None
    action_id = str((authorization or {}).get("action_id") or "")
    artifact_hash = canonical_hash(artifact)
    receipt_base = {
        "schema": "naya/cloudflare/portable-execution-receipt/v1",
        "status": "REFUSED",
        "artifact_schema": artifact.get("schema") if isinstance(artifact, dict) else None,
        "artifact_sha256": artifact_hash,
        "runner": "independent-process",
        "verified_at": now,
        "action_id": action_id,
    }

    if not isinstance(artifact, dict) or artifact.get("schema") != SCHEMA:
        receipt_base["reason"] = "unsupported portable authorization schema"
        write_receipt(receipt_path, receipt_base)
        print("PORTABLE_AUTH=REFUSED")
        print("EXTERNAL_ADAPTER_INVOKED=FALSE")
        return 3

    try:
        boundary = PORTA.portable_boundary_release(
            artifact=artifact,
            public_key_hex=public_key,
            registry=registry,
            commit_sha=str(authorization.get("commit_sha") or ""),
            target_environment=str(authorization.get("environment") or ""),
            deployment_surface="cloudflare",
            repository=ADAPTER.REPOSITORY,
            worker_name=str(authorization.get("worker_name") or ADAPTER.WORKER),
            now=now,
        )
    except Exception as exc:
        receipt_base["reason"] = f"portable boundary error: {exc}"
        write_receipt(receipt_path, receipt_base)
        print("PORTABLE_AUTH=REFUSED")
        print("EXTERNAL_ADAPTER_INVOKED=FALSE")
        return 3

    if not boundary.allowed:
        receipt_base["reason"] = boundary.reason
        write_receipt(receipt_path, receipt_base)
        print("PORTABLE_AUTH=REFUSED")
        print(f"REFUSAL_REASON={boundary.reason}")
        print("EXTERNAL_ADAPTER_INVOKED=FALSE")
        return 3

    identity = {
        "identity_id": str(authorization.get("identity_id") or ""),
        "identity_fingerprint": str(authorization.get("identity_fingerprint") or ""),
        "identity_binding_hash": str(authorization.get("identity_binding_hash") or ""),
    }
    if not identity["identity_id"] or not identity["identity_fingerprint"] or not identity["identity_binding_hash"]:
        receipt_base["reason"] = "portable authorization lacks the governed identity continuity fields"
        write_receipt(receipt_path, receipt_base)
        print("PORTABLE_AUTH=REFUSED")
        print("REFUSAL_REASON=IDENTITY_CONTINUITY_FIELDS_MISSING")
        print("EXTERNAL_ADAPTER_INVOKED=FALSE")
        return 3

    actual_commit = current_commit(source_dir)
    if actual_commit != str(authorization.get("commit_sha") or ""):
        receipt_base["reason"] = f"source checkout {actual_commit} does not match authorization commit {authorization.get('commit_sha')}"
        write_receipt(receipt_path, receipt_base)
        print("PORTABLE_AUTH=REFUSED")
        print("REFUSAL_REASON=SOURCE_COMMIT_MISMATCH")
        print("EXTERNAL_ADAPTER_INVOKED=FALSE")
        return 3

    if lock_path and lock_path.exists():
        prior = lock_path.read_text(encoding="utf-8").strip()
        receipt = {
            **receipt_base,
            "reason": "portable authorization already consumed at this execution boundary",
            "replay_key": prior,
            "identity": identity,
            "adapter_invoked": False,
        }
        write_receipt(receipt_path, receipt)
        print("PORTABLE_AUTH=REFUSED")
        print("REPLAY=REFUSED")
        print("EXTERNAL_ADAPTER_INVOKED=FALSE")
        return 3

    action = dict(authorization)
    action.update({
        "action_id": action_id,
        "action_type": str(authorization.get("action_type") or "deploy_public_runtime"),
        "target": str(authorization.get("target") or ""),
        "environment": str(authorization.get("environment") or ""),
        "worker_name": str(authorization.get("worker_name") or ADAPTER.WORKER),
        "repository": str(authorization.get("repository") or ADAPTER.REPOSITORY),
        "commit_sha": str(authorization.get("commit_sha") or ""),
        "protected_baseline": str(authorization.get("commit_sha") or ""),
    })

    try:
        result = ADAPTER.CloudflareWorkerProductionAdapter(source_dir=source_dir).execute(action)
    except Exception as exc:
        receipt = {
            **receipt_base,
            "status": "FAILED",
            "reason": str(exc),
            "identity": identity,
            "adapter_invoked": True,
        }
        write_receipt(receipt_path, receipt)
        print("PORTABLE_AUTH=PASS")
        print("EXTERNAL_ADAPTER_INVOKED=TRUE")
        print("EXTERNAL_ACTION=FAILED")
        return 4

    if lock_path:
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        lock_path.write_text(
            f"{action_id}\n{artifact_hash}\n{result.get('external_version_id','')}",
            encoding="utf-8",
        )

    receipt = {
        **receipt_base,
        "status": "VERIFIED_EXTERNAL_ACTION",
        "identity": identity,
        "authorization": {
            "authority_id": authorization.get("authority_id"),
            "decision_id": authorization.get("decision_id"),
            "action_id": authorization.get("action_id"),
            "action_type": authorization.get("action_type"),
            "target": authorization.get("target"),
            "permission": authorization.get("permission"),
            "binding_hash": authorization.get("binding_hash"),
            "environment": authorization.get("environment"),
            "worker_name": authorization.get("worker_name"),
            "repository": authorization.get("repository"),
            "commit_sha": authorization.get("commit_sha"),
        },
        "registry_revision_at_use": PORTA.registry_revision(registry),
        "source_checkout": actual_commit,
        "external_execution": result,
        "adapter_invoked": True,
        "provenance": {
            "source": "github-actions-independent-runner",
            "portable_authorization_schema": SCHEMA,
            "artifact_sha256": artifact_hash,
            "verified_before_adapter": True,
        },
        "continuation": {
            "next_action": "consume portable receipt into canonical Activity/PIS projection and verify fresh-context retrieval",
            "successor": "NayaNET governed cognition continuity",
        },
    }
    write_receipt(receipt_path, receipt)
    print("PORTABLE_AUTH=PASS")
    print("EXTERNAL_ACTION=PASS")
    print("EXTERNAL_ADAPTER_INVOKED=TRUE")
    print("PORTABLE_RECEIPT_WRITTEN=" + str(receipt_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
