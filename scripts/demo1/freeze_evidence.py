#!/usr/bin/env python3
"""Freeze the Demo-1 evidence package: one run, captured whole, sealed.

Runs the real Demo-1 effect exactly once (act_run.py -> LAW gate ->
ACT executor -> artifact), captures the full receipt chain (LAW gate
receipt, decision receipt, execution receipt), the artifact, the grant,
the fresh-verify report, and the test evidence, then writes
MANIFEST.json + package_seal.json.

The package is self-contained: Naya 2 consumes these exact bytes for
the durable write -> kill/fresh -> read proof; Coda 2/3 verify the real
effect from them. The freeze identifier is the commit SHA that carries
the package; the manifest records the code head the run executed
against (they differ by exactly the package commit).

Usage:
    python3 scripts/demo1/freeze_evidence.py --code-head <sha>
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
RUN_ROOT = Path("/tmp/demo1-frozen-pkg")
PACKAGE_DIR = REPO_ROOT / "evidence" / "demo1" / "frozen-2026-10-01"
# Containment roots: --out must stay under EVIDENCE_ROOT; --run-root under /tmp.
EVIDENCE_ROOT = (REPO_ROOT / "evidence").resolve()
TMP_ROOT = Path("/tmp").resolve()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=REPO_ROOT, **kw)


def contained(path: Path, root: Path) -> bool:
    """True iff path resolves within root (no escape via .. or symlink)."""
    try:
        path.resolve().relative_to(root)
        return True
    except ValueError:
        return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--code-head", required=True,
                    help="published code head the run must execute against")
    ap.add_argument("--run-root", default=str(RUN_ROOT))
    ap.add_argument("--out", default=str(PACKAGE_DIR))
    args = ap.parse_args()

    # Guard: the working tree must be exactly the code head, clean.
    head = run(["git", "rev-parse", "HEAD"]).stdout.strip()
    dirty = run(["git", "status", "--porcelain"]).stdout.strip()
    if head != args.code_head:
        print(f"REFUSED: worktree HEAD {head} != code head {args.code_head}")
        return 1
    if dirty:
        print("REFUSED: worktree not clean:\n" + dirty)
        return 1
    print("worktree == code head", head, "(clean)")

    run_root = Path(args.run_root)
    if not contained(run_root, TMP_ROOT):
        print(f"REFUSED: --run-root {run_root} escapes {TMP_ROOT}")
        return 1
    out = Path(args.out)
    if not contained(out, EVIDENCE_ROOT):
        print(f"REFUSED: --out {out} escapes {EVIDENCE_ROOT}")
        return 1
    # Immutable replay protection: never overwrite a frozen package.
    if out.exists():
        print(f"REFUSED: package already exists at {out} — frozen evidence "
              f"is immutable; choose a new --out or remove it by hand with "
              f"an explicit, reviewed action.")
        return 1
    if run_root.exists():
        shutil.rmtree(run_root)

    # 1. The one real run.
    p = run([sys.executable, "scripts/demo1/act_run.py",
             "--root", str(run_root)])
    print(p.stdout)
    if p.returncode != 0:
        print("act_run.py FAILED:\n" + p.stderr)
        return 1
    lines = dict(l.split(": ", 1) for l in p.stdout.splitlines() if ": " in l)
    receipt_path = Path(lines["receipt"].strip())
    artifact_path = Path(lines["artifact"].strip())
    execution_id = lines["execution_id"].strip()
    artifact_sha = lines["artifact sha256"].strip()
    gate_id = lines["law gate receipt"].strip()
    decision_id = lines["decision receipt"].strip()
    receipts_dir = receipt_path.parent

    # 2. Fresh verify in a fresh process; capture the report.
    v = run([sys.executable, "scripts/demo1/fresh_verify.py",
             str(receipt_path)])
    print(v.stdout)
    if v.returncode != 0 or "FRESH VERIFY: PASS" not in v.stdout:
        print("fresh_verify FAILED:\n" + v.stderr)
        return 1

    # 3. Test evidence: LAW-auth boundary tests + full suite tail.
    t = run([sys.executable, "-m", "pytest",
             "tests/test_nodes/test_demo1_law_authorization.py", "-q"])
    if t.returncode != 0:
        print("law-auth tests FAILED:\n" + t.stdout[-2000:])
        return 1
    law_tests = t.stdout.strip().splitlines()[-1]
    s = run([sys.executable, "-m", "pytest", "tests/", "-q"])
    if s.returncode != 0:
        # Fail fast: a FAILED suite must never be recorded as evidence
        # while assembly continues.
        print("full suite FAILED — refusing to freeze:\n" + s.stdout[-2000:])
        return 1
    suite = s.stdout.strip().splitlines()[-1]
    print("law-auth:", law_tests, "| suite:", suite)

    # 4. Assemble the package.
    out.mkdir(parents=True)
    files = {}
    def add(name: str, src: Path, object_type: str):
        dst = out / name
        shutil.copy2(src, dst)
        files[name] = {"sha256": sha256_file(dst), "object_type": object_type}
    add("artifact.md", artifact_path, "demo_artifact")
    add("law_gate_receipt.json",
        receipts_dir / ("law-gate-" + gate_id + ".json"),
        "law_gate_receipt")
    add("decision_receipt.json",
        receipts_dir / ("decision-" + decision_id + ".json"),
        "decision_receipt")
    add("execution_receipt.json", receipt_path, "execution_receipt")
    add("demo_grant.json", REPO_ROOT / "scripts" / "demo1" / "demo_grant.json",
        "authority_grant")
    add("proposal.json", receipts_dir / "proposal.json", "law_proposal")
    add("input_state.json", receipts_dir / "input_state.json", "input_state")
    add("grant_provenance.json", receipts_dir / "grant_provenance.json",
        "grant_provenance")
    add("registry_ref.json", receipts_dir / "registry_ref.json",
        "registry_reference")
    (out / "fresh_verify_report.txt").write_text(v.stdout, encoding="utf-8")
    files["fresh_verify_report.txt"] = {
        "sha256": sha256_file(out / "fresh_verify_report.txt"),
        "object_type": "verification_report"}
    (out / "test_evidence.txt").write_text(
        f"law-auth boundary tests: {law_tests}\nfull suite: {suite}\n",
        encoding="utf-8")
    files["test_evidence.txt"] = {
        "sha256": sha256_file(out / "test_evidence.txt"),
        "object_type": "test_evidence"}

    # Relationship hashes: how the objects bind to each other.
    # A verifier recomputes these from the files; a mismatch means
    # the package was assembled from inconsistent parts.
    decision = json.loads((out / "decision_receipt.json").read_bytes())
    execution = json.loads((out / "execution_receipt.json").read_bytes())
    law_gate = json.loads((out / "law_gate_receipt.json").read_bytes())
    input_state = json.loads((out / "input_state.json").read_bytes())
    # The artifact SHA in the manifest must match the sealed file.
    assert files["artifact.md"]["sha256"] == artifact_sha
    # The decision receipt's inputs_hash must match the input state's.
    assert decision.get("inputs_hash") == input_state.get("inputs_hash")
    relationships = {
        "decision_receipt.authority_basis_ref":
            decision.get("authority_basis", {}).get("ref"),
        "decision_receipt.law_gate_receipt_id":
            law_gate.get("receipt_id"),
        "decision_receipt.inputs_hash":
            decision.get("inputs_hash"),
        "input_state.inputs_hash_matches_decision": True,
        "execution_receipt.decision_receipt_id":
            decision.get("receipt_id"),
        "execution_receipt.execution_id":
            execution.get("execution_id"),
        "artifact.sha256": files["artifact.md"]["sha256"],
        "proposal.proposal_id_binds_to_law_gate":
            law_gate.get("proposal_id"),
    }

    # Dual binding: the executing code (local tree) vs the published
    # commit. They must match; the package commit (carrying these files)
    # is a descendant, recorded by the committer, never by this script.
    code_tree = run(["git", "rev-parse", "HEAD^{tree}"]).stdout.strip()
    manifest = {
        "package_id": "demo1-frozen-2026-10-01",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "code_head": args.code_head,
        "code_tree": code_tree,
        "code_head_is_published": True,
        "branch": "naya4/nine-node-kernel-v1",
        "executing_code_sha": args.code_head,
        "package_commit_sha": None,
        "freeze_note": ("The freeze identifier is the commit SHA carrying "
                        "this package (parent == code_head). The executing "
                        "code SHA (above) and the package commit SHA (filled "
                        "by the committer) are distinct by construction."),
        "run": {
            "execution_id": execution_id,
            "law_gate_receipt_id": gate_id,
            "decision_receipt_id": decision_id,
            "artifact_sha256": artifact_sha,
            "fresh_verify": "PASS (V1/V2/V3)",
        },
        "grant_ref": "grant-demo1-director-20261001",
        "files": [{"path": n, **meta}
                  for n, meta in sorted(files.items())],
        "relationships": relationships,
    }
    manifest_bytes = json.dumps(manifest, indent=2, sort_keys=True).encode()
    (out / "MANIFEST.json").write_bytes(manifest_bytes)
    seal = hashlib.sha256(manifest_bytes).hexdigest()
    (out / "package_seal.json").write_text(
        json.dumps({"sha256": seal, "covers": "MANIFEST.json (binds all files)"},
                   indent=2) + "\n", encoding="utf-8")

    # 5. Verify the seal before declaring frozen.
    assert artifact_sha == files["artifact.md"]["sha256"] == sha256_file(artifact_path)
    assert hashlib.sha256((out / "MANIFEST.json").read_bytes()).hexdigest() == seal
    print("package:", out)
    print("seal:", seal)
    print("FROZEN —", len(files), "files sealed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
