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


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=REPO_ROOT, **kw)


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
    suite = s.stdout.strip().splitlines()[-1] if s.returncode == 0 else "FAILED"
    print("law-auth:", law_tests, "| suite:", suite)

    # 4. Assemble the package.
    out = Path(args.out)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    files = {}
    def add(name: str, src: Path):
        dst = out / name
        shutil.copy2(src, dst)
        files[name] = sha256_file(dst)
    add("artifact.md", artifact_path)
    add("law_gate_receipt.json",
        receipts_dir / ("law-gate-" + gate_id + ".json"))
    add("decision_receipt.json",
        receipts_dir / ("decision-" + decision_id + ".json"))
    add("execution_receipt.json", receipt_path)
    add("demo_grant.json", REPO_ROOT / "scripts" / "demo1" / "demo_grant.json")
    (out / "fresh_verify_report.txt").write_text(v.stdout, encoding="utf-8")
    files["fresh_verify_report.txt"] = sha256_file(out / "fresh_verify_report.txt")
    (out / "test_evidence.txt").write_text(
        f"law-auth boundary tests: {law_tests}\nfull suite: {suite}\n",
        encoding="utf-8")
    files["test_evidence.txt"] = sha256_file(out / "test_evidence.txt")

    manifest = {
        "package_id": "demo1-frozen-2026-10-01",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "code_head": args.code_head,
        "branch": "naya4/nine-node-kernel-v1",
        "freeze_note": ("The freeze identifier is the commit SHA carrying "
                        "this package (parent == code_head)."),
        "run": {
            "execution_id": execution_id,
            "law_gate_receipt_id": gate_id,
            "decision_receipt_id": decision_id,
            "artifact_sha256": artifact_sha,
            "fresh_verify": "PASS (V1/V2/V3)",
        },
        "grant_ref": "grant-demo1-director-20261001",
        "files": [{"path": n, "sha256": h}
                  for n, h in sorted(files.items())],
    }
    manifest_bytes = json.dumps(manifest, indent=2, sort_keys=True).encode()
    (out / "MANIFEST.json").write_bytes(manifest_bytes)
    seal = hashlib.sha256(manifest_bytes).hexdigest()
    (out / "package_seal.json").write_text(
        json.dumps({"sha256": seal, "covers": "MANIFEST.json (binds all files)"},
                   indent=2) + "\n", encoding="utf-8")

    # 5. Verify the seal before declaring frozen.
    assert artifact_sha == files["artifact.md"] == sha256_file(artifact_path)
    assert hashlib.sha256((out / "MANIFEST.json").read_bytes()).hexdigest() == seal
    print("package:", out)
    print("seal:", seal)
    print("FROZEN —", len(files), "files sealed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
