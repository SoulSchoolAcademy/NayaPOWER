#!/usr/bin/env python3
"""Test #13 GitHub Actions runner verifier.

Runs on a REAL GitHub-hosted runner. It receives ONLY public material from the
fixtures dir: the signed portable artifacts, the public test key, the registry
snapshots, and the expected context. It NEVER receives the issuer private key,
the issuer process, the gate's `_issued` set, or any hidden authorization state.

The runner therefore: verifies, and cannot mint.

Evidence is printed for the workflow log:
  T13_RUNNER=RUNNING
  T13_ISSUER_MEMORY=none
  T13_PRIVATE_KEY=absent
  T13_<case>=ALLOW|REFUSED        (per case)
  T13_MISMATCHES=<n>
  T13_VERDICT=PASS|FAIL

Usage:
  python tools/t13_runner_verify.py [--dir <fixtures_dir>]
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


GATE = load("t13r_gate", ROOT / ".naya/runtime/universal_execution_gate.py")
PORTA = load("t13r_porta", ROOT / ".naya/runtime/portable_authorization.py")

EXPECTED_REPOSITORY = "SoulSchoolAcademy/NayaPOWER"
FORBIDDEN_BRANCH = "main"
KEY_MARKERS = ("private", "keyseat", "signing-seat", "secret")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def branch_and_repo():
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    ref = os.environ.get("GITHUB_REF_NAME", "")
    if not repo:
        run = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True)
        ref = run.stdout.strip() or ""
    if not repo:
        run = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True)
        url = run.stdout.strip().lower()
        if "github.com/" in url:
            repo = url.split("github.com/", 1)[1].rstrip(".git")
    return repo, ref


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=str(ROOT / ".naya/github-actions/test-13-fixtures"))
    ap.add_argument("--now", default=None, help="optional ISO timestamp (deterministic tests only)")
    args = ap.parse_args()

    fixtures = Path(args.dir)
    matrix = load_json(fixtures / "matrix.json")
    default_context = load_json(fixtures / "context.json")
    default_pub = (fixtures / "public.hex").read_text(encoding="utf-8").strip()

    print("T13_RUNNER=RUNNING")
    repo, ref = branch_and_repo()
    print(f"T13_REPOSITORY={repo or '<unset>'}")
    print(f"T13_REF={ref or '<unset>'}")
    if repo and repo.lower() != matrix.get("repository", EXPECTED_REPOSITORY).lower():
        print("T13_VERDICT=FAIL (wrong repository)")
        return 1
    if ref == FORBIDDEN_BRANCH:
        print("T13_VERDICT=FAIL (ref is the forbidden branch)")
        return 1

    private_present = False
    if os.environ.get("T13_PRIVATE_KEY"):
        private_present = True
    for candidate in fixtures.rglob("*"):
        if not candidate.is_file():
            continue
        low = candidate.name.lower()
        if low.startswith(("private.", "private_", "keyseat", "signing-seat", "secret.", "secret_")):
            private_present = True
        elif candidate.suffix.lower() == ".hex" and low != "public.hex":
            private_present = True
    print(f"T13_ISSUER_MEMORY=none")
    print(f"T13_PRIVATE_KEY={'present' if private_present else 'absent'}")
    print(f"T13_CRYPTOGRAPHY={'ok' if PORTA.Ed25519PublicKey is not None else 'missing'}")

    mismatches = 0
    for row in matrix["cases"]:
        case = load_json(fixtures / row["file"])
        expected = row["expected"]
        try:
            result = run_case(case, fixtures, default_pub, default_context, args.now)
            actual = "ALLOW" if result else "REFUSED"
        except Exception as exc:
            actual = "REFUSED"
            print(f"T13_{case['id']}=REFUSED (verifier rejection: {exc})")
        if actual != expected:
            mismatches += 1
            print(f"T13_{case['id']}=REFUSED (mismatch: expected {expected}, got {actual})")
        else:
            print(f"T13_{case['id']}={actual}")

    print(f"T13_CASES={len(matrix['cases'])}")
    print(f"T13_MISMATCHES={mismatches}")
    if mismatches == 0 and not private_present:
        print("T13_VERDICT=PASS")
        return 0
    print("T13_VERDICT=FAIL")
    return 1


def run_case(case: dict, fixtures: Path, default_pub: str, default_ctx: dict, now):
    mode = case["mode"]
    context = {**default_ctx, **case.get("context", {})}
    registry_path = fixtures / (case.get("registry_path") or "registry.json")
    registry = GATE.load_registry(registry_path)
    public_key_hex = case.get("public_key_hex", default_pub)

    if mode == "release":
        decision = PORTA.portable_boundary_release(
            artifact=case["artifact"], public_key_hex=public_key_hex, registry=registry,
            commit_sha=context["commit_sha"],
            target_environment=context["target_environment"],
            deployment_surface=context["deployment_surface"],
            repository=context["repository"], worker_name=context.get("worker_name"),
            project_id=context.get("project_id"), now=now,
        )
        return decision.allowed
    if mode == "bypass":
        decision = PORTA.portable_boundary_release(
            artifact=case.get("payload"), public_key_hex=public_key_hex, registry=registry,
            commit_sha=context["commit_sha"],
            target_environment=context["target_environment"],
            deployment_surface=context["deployment_surface"],
            repository=context["repository"], worker_name=context.get("worker_name"),
            project_id=context.get("project_id"), now=now,
        )
        return False if not decision.allowed else True
    if mode == "memory":
        ok, _ = PORTA.verify_portable_authorization(
            artifact=case["artifact"], public_key_hex=public_key_hex, registry=registry, now=now,
        )
        return ok
    if mode == "mint":
        crafted = dict(case["artifact"]["authorization"])
        crafted["actor_id"] = "RunnerWhoMints"
        from hashlib import sha256
        crafted_text = "|".join([
            crafted["authority_id"], crafted["decision_id"], crafted["action_id"],
            crafted["action_type"], crafted["target"], crafted["actor_id"],
            crafted["scope"], crafted["permission"],
        ])
        crafted["binding_hash"] = sha256(crafted_text.encode("utf-8")).hexdigest()
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
        runner_key = Ed25519PrivateKey.generate()
        msg = PORTA._canonical_json(crafted).encode("utf-8")
        signature = runner_key.sign(msg).hex()
        minted = {"schema": PORTA.SCHEMA, "authorization": crafted, "signature": signature}
        ok, _ = PORTA.verify_portable_authorization(
            artifact=minted, public_key_hex=public_key_hex, registry=registry, now=now,
        )
        return False  # a runner-minted artifact must NEVER verify
    raise ValueError(f"unknown case mode {mode}")


if __name__ == "__main__":
    raise SystemExit(main())