"""Receipt gate + checkout depth: the mechanism, proved.

`tools/check_pr_receipt.py::git_exists` validates every 40-char SHA in the PR
body's `## Evidence` section with `git cat-file -e` against the LOCAL object
store. CI checks out the PR merge ref; with a depth-1 checkout the merge commit
exists but the PR head commit (its second parent) is NOT in the store -- so a
CORRECT head SHA always failed the gate. The `receipt` job's checkout must
therefore fetch full history (`fetch-depth: 0`).

These tests prove that mechanism on a faithful miniature (a merge ref cloned
at depth 1 vs full), run the REAL gate script end to end in both clones, and
guard the workflow file against regression.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
GATE = REPO_ROOT / "tools" / "check_pr_receipt.py"
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "worker-protocol-gates.yml"

GIT_ENV = {
    "GIT_AUTHOR_NAME": "naya-test",
    "GIT_AUTHOR_EMAIL": "naya-test@example.invalid",
    "GIT_COMMITTER_NAME": "naya-test",
    "GIT_COMMITTER_EMAIL": "naya-test@example.invalid",
}


def _git(args, cwd, **kw):
    env = {**os.environ, **GIT_ENV}
    return subprocess.run(["git", *args], cwd=cwd, env=env,
                          capture_output=True, text=True, **kw)


def _build_pr_repo(root: Path):
    """A miniature PR: main @ A, PR branch adds B, merge ref M = merge(B)."""
    src = root / "src"
    src.mkdir()
    _git(["init", "-b", "main"], cwd=src, check=True)
    (src / "f.txt").write_text("base\n")
    _git(["add", "."], cwd=src, check=True)
    _git(["commit", "-m", "base"], cwd=src, check=True)
    _git(["checkout", "-b", "pr"], cwd=src, check=True)
    (src / "f.txt").write_text("base\npr-change\n")
    _git(["commit", "-am", "pr head"], cwd=src, check=True)
    head = _git(["rev-parse", "HEAD"], cwd=src, check=True).stdout.strip()
    _git(["checkout", "main"], cwd=src, check=True)
    _git(["merge", "--no-ff", "pr", "-m", "merge pr"], cwd=src, check=True)
    merge = _git(["rev-parse", "HEAD"], cwd=src, check=True).stdout.strip()
    assert re.fullmatch(r"[0-9a-f]{40}", head)
    assert re.fullmatch(r"[0-9a-f]{40}", merge)
    return src, head, merge


def _clone(src: Path, dst: Path, depth_args):
    # file:// forces the transport path so --depth is honored for local clones.
    _git(["clone", *depth_args, "--branch", "main",
          f"file://{src}", str(dst)], cwd=src.parent, check=True)


def _evidence_body(sha: str) -> str:
    return ("## Evidence\n"
            f"{sha}\n"
            "The PR head commit — proves the receipt names a real artifact.\n")


def _run_gate(clone_dir: Path, sha: str):
    env = {**os.environ, "PR_BODY": _evidence_body(sha)}
    return subprocess.run([sys.executable, str(GATE)], cwd=clone_dir, env=env,
                          capture_output=True, text=True, timeout=60)


# ---------------------------------------------------------------- mechanism
def test_pr_head_sha_missing_from_depth1_merge_checkout(tmp_path):
    """THE DEFECT: depth-1 checkout of the merge ref has the merge commit
    but NOT the PR head commit object."""
    src, head, merge = _build_pr_repo(tmp_path)
    shallow = tmp_path / "shallow"
    _clone(src, shallow, ["--depth", "1"])
    assert _git(["cat-file", "-e", merge], cwd=shallow).returncode == 0, \
        "merge commit itself must exist in a depth-1 checkout"
    assert _git(["cat-file", "-e", head], cwd=shallow).returncode != 0, \
        "PR head SHA must be MISSING from a depth-1 checkout (the defect)"


def test_pr_head_sha_present_with_full_history(tmp_path):
    """WHAT THE FIX BUYS: full history contains the head object."""
    src, head, merge = _build_pr_repo(tmp_path)
    full = tmp_path / "full"
    _clone(src, full, [])
    assert _git(["cat-file", "-e", merge], cwd=full).returncode == 0
    assert _git(["cat-file", "-e", head], cwd=full).returncode == 0, \
        "PR head SHA must exist once full history is fetched"


# ------------------------------------------------------- the real gate script
def test_receipt_gate_rejects_correct_head_sha_on_shallow_clone(tmp_path):
    """End to end: the real gate FAILS a correct head SHA on depth-1."""
    src, head, _ = _build_pr_repo(tmp_path)
    shallow = tmp_path / "shallow"
    _clone(src, shallow, ["--depth", "1"])
    r = _run_gate(shallow, head)
    assert r.returncode == 1, f"gate must fail on depth-1, got: {r.stdout}"
    assert "dead artifact handle" in r.stdout
    assert head[:8] in r.stdout


def test_receipt_gate_accepts_correct_head_sha_with_full_history(tmp_path):
    """End to end: the real gate PASSES the same SHA with full history."""
    src, head, _ = _build_pr_repo(tmp_path)
    full = tmp_path / "full"
    _clone(src, full, [])
    r = _run_gate(full, head)
    assert r.returncode == 0, f"gate must pass with full history: {r.stdout}"
    assert "Receipt OK" in r.stdout


# ------------------------------------------------------- regression guard
def test_receipt_job_checkout_fetches_full_history():
    """The `receipt` job's checkout must keep fetch-depth: 0.

    This is the mechanical guard for PR #2188's fix: removing it reintroduces
    the defect proved above, and this test fails first.
    """
    wf = yaml.safe_load(WORKFLOW.read_text())
    receipt = wf["jobs"]["receipt"]
    checkout = next(
        s for s in receipt["steps"]
        if str(s.get("uses", "")).startswith("actions/checkout@")
    )
    assert (checkout.get("with") or {}).get("fetch-depth") == 0, \
        "receipt job checkout must use fetch-depth: 0 (PR #2188)"
    assert any("check_pr_receipt.py" in str(s.get("run", ""))
               for s in receipt["steps"]), \
        "regression guard is targeting the wrong job: receipt step missing"
