"""Receipt gate + backticked-branch-name trap: the mechanism, proved.

PR #2635 names the trap: a backticked BRANCH name (e.g. `naya5/foo`) in the
`## Evidence` section is parsed as a repo path, `git cat-file -e
HEAD:naya5/foo` fails, and the gate exits 1 — a branch name is not a path.
The exit-1 path must name the trap, and a parse-time pre-check must catch
branch-like handles before the verify/dead loop.

These tests run the REAL `tools/check_pr_receipt.py` end to end (subprocess,
PR_BODY env) in miniature git repos:
  T1  backticked branch name -> exit 1, trap hint named, path: classification
  T2  valid 40-char SHA      -> exit 0, Receipt OK, no TRAP (control)
  T3  dead non-branch path   -> exit 1, trap hint kept on the exit-1 path
  T4  branch-like backtick   -> exit 1, pre-check message (mechanism)
  T5  backticked real path   -> exit 0, pre-check does not fire (control)

Classification note (for the IV seat): a dead non-branch path like
`docs/deleted-page.md` is branch-shaped, so it fails at the pre-check rather
than the dead-handle branch — both messages name the trap, exit code is 1 in
both cases.

Red/green record (Naya Zeta, 2026-10-16): T1, T3, T4 FAIL against the
pre-#2635 script (no trap text anywhere); all five PASS on the #2635 head.
"""
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
GATE = REPO_ROOT / "tools" / "check_pr_receipt.py"

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


def _mini_repo(root: Path, files: dict) -> Path:
    """A one-commit git repo: HEAD exists, branch names never resolve."""
    d = root / "mini"
    d.mkdir()
    _git(["init", "-b", "main"], cwd=d, check=True)
    for rel, content in files.items():
        p = d / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
    _git(["add", "."], cwd=d, check=True)
    _git(["commit", "-m", "init"], cwd=d, check=True)
    return d


def _run_gate(cwd: Path, body: str):
    env = {**os.environ, "PR_BODY": body}
    return subprocess.run([sys.executable, str(GATE)], cwd=cwd, env=env,
                          capture_output=True, text=True, timeout=60)


def _head_sha(repo: Path) -> str:
    return _git(["rev-parse", "HEAD"], cwd=repo, check=True).stdout.strip()


def test_backticked_branch_name_fails_with_trap_hint(tmp_path):
    """T1: the trap — `naya5/trap-branch` is classified as a path and dies."""
    repo = _mini_repo(tmp_path, {"f.txt": "base\n"})
    body = ("## Evidence\n"
            "`naya5/trap-branch`\n"
            "The branch that carried the work.\n")
    r = _run_gate(repo, body)
    assert r.returncode == 1, f"gate must exit 1 on the trap, got: {r.stdout}"
    assert "RECEIPT GATE FAILED" in r.stdout
    assert "TRAP: a backticked branch name" in r.stdout
    assert "path:naya5/trap-branch" in r.stdout, \
        "the name must be proved classified as a path — the trap mechanism"


def test_valid_sha_evidence_passes_without_trap_hint(tmp_path):
    """T2 (control): a real 40-char SHA passes and names no trap."""
    repo = _mini_repo(tmp_path, {"f.txt": "base\n"})
    sha = _head_sha(repo)
    body = ("## Evidence\n"
            f"{sha}\n"
            "The repo's own head commit — "
            "proves the hint fires only on the trap path.\n")
    r = _run_gate(repo, body)
    assert r.returncode == 0, f"gate must pass on a real SHA: {r.stdout}"
    assert "Receipt OK" in r.stdout
    assert "TRAP" not in r.stdout


def test_dead_path_handle_still_carries_trap_hint(tmp_path):
    """T3: the exit-1 path keeps explaining the trap for dead handles."""
    repo = _mini_repo(tmp_path, {"f.txt": "base\n"})
    body = ("## Evidence\n"
            "`docs/deleted-page.md`\n"
            "A page that no longer exists.\n")
    r = _run_gate(repo, body)
    assert r.returncode == 1, f"gate must exit 1 on a dead handle: {r.stdout}"
    assert "TRAP: a backticked branch name" in r.stdout


def test_branch_like_backtick_fails_at_precheck(tmp_path):
    """T4: the mechanism — branch-like backticks fail at parse time."""
    repo = _mini_repo(tmp_path, {"f.txt": "base\n"})
    body = ("## Evidence\n"
            "`naya5/foo`\n"
            "A branch-like handle that is not a repo path.\n")
    r = _run_gate(repo, body)
    assert r.returncode == 1, f"pre-check must fail the handle: {r.stdout}"
    assert "TRAP: branch-like backticked handle(s)" in r.stdout


def test_backticked_real_path_passes_precheck(tmp_path):
    """T5 (control): a real backticked path never trips the pre-check."""
    repo = _mini_repo(tmp_path, {"f.txt": "base\n",
                                 "tools/check_pr_receipt.py": "# stub\n"})
    body = ("## Evidence\n"
            "`tools/check_pr_receipt.py`\n"
            "A path that exists — proves real paths skip the pre-check.\n")
    r = _run_gate(repo, body)
    assert r.returncode == 0, f"real paths must pass: {r.stdout}"
    assert "Receipt OK" in r.stdout
    assert "TRAP" not in r.stdout
