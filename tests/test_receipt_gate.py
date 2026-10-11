"""Receipt gate: SHA evidence handles must resolve in the gate's own checkout.

THE DEFECT THIS GUARDS (2026-10-11, PR #2340, build-lane sign-out 6109237606)
---------------------------------------------------------------------------
tools/check_pr_receipt.py treats a 40-hex SHA as a live evidence handle and
resolves it with `git cat-file -e` inside the gate's checkout. The receipt
job ran `actions/checkout@v4` with the DEFAULT fetch-depth (1). For a
pull_request event the checkout is the PR merge commit, so the PR head and
base SHAs -- the merge commit's parents, and the most natural evidence a
receipt can cite -- are absent locally. The gate false-redded on a valid
handle: "1 dead artifact handle(s): sha:93eb473d" for #2340's own head SHA,
while the run URL in the same Evidence section verified fine.

THE FIX: the receipt job checks out with fetch-depth: 0 (full history), the
same as the two sibling jobs in the same workflow file. Every SHA in the
PR's history then resolves, matching the script's documented contract
("40-char git SHA -> must exist in this repo").

Tests below are stdlib-only (no yaml import -- see
tests/test_ci_declares_test_dependencies.py for why that matters) and
hermetic: they build tiny throwaway git repos instead of depending on the
ambient checkout.
"""

import os
import re
import subprocess
import tempfile
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
WORKFLOW = REPO / ".github" / "workflows" / "worker-protocol-gates.yml"
SCRIPT = REPO / "tools" / "check_pr_receipt.py"

GIT_ENV = {
    "GIT_AUTHOR_NAME": "receipt-gate-test",
    "GIT_AUTHOR_EMAIL": "test@example.invalid",
    "GIT_COMMITTER_NAME": "receipt-gate-test",
    "GIT_COMMITTER_EMAIL": "test@example.invalid",
}


def git(*args, cwd, env_extra=None):
    env = dict(os.environ, **GIT_ENV)
    if env_extra:
        env.update(env_extra)
    r = subprocess.run(["git", *args], cwd=cwd, env=env,
                       capture_output=True, text=True)
    assert r.returncode == 0, f"git {' '.join(args)} failed: {r.stderr}"
    return r.stdout.strip()


@pytest.fixture()
def two_commit_repo(tmp_path):
    """A repo with commits A <- B; returns (path, sha_a, sha_b)."""
    repo = tmp_path / "repo"
    repo.mkdir()
    git("init", "-q", cwd=repo)
    (repo / "note.md").write_text("first\n")
    git("add", "note.md", cwd=repo)
    git("commit", "-qm", "A", cwd=repo)
    sha_a = git("rev-parse", "HEAD", cwd=repo)
    (repo / "note.md").write_text("second\n")
    git("commit", "-qam", "B", cwd=repo)
    sha_b = git("rev-parse", "HEAD", cwd=repo)
    return repo, sha_a, sha_b


def run_gate(body, cwd):
    env = dict(os.environ, PR_BODY=body)
    r = subprocess.run(["python3", str(SCRIPT)], cwd=cwd, env=env,
                       capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def evidence(*lines):
    return "## Evidence\n\n" + "\n".join(lines) + "\n"


# --- Script contract: SHA handles -------------------------------------------

def test_sha_handle_resolves_in_full_history(two_commit_repo):
    repo, sha_a, _sha_b = two_commit_repo
    body = evidence(f"`{sha_a}`",
                    "The base commit the tests ran against.")
    rc, out = run_gate(body, repo)
    assert rc == 0, out
    assert "Receipt OK" in out


def test_sha_handle_dead_in_shallow_checkout(two_commit_repo, tmp_path):
    """Faithful sim of the pre-fix wiring: depth-1 checkout, parent SHA.

    This is the exact false-red class from PR #2340. It must FAIL here --
    the test documents why fetch-depth: 0 is load-bearing, not cosmetic.
    """
    repo, sha_a, _sha_b = two_commit_repo
    shallow = tmp_path / "shallow"
    git("clone", "-q", "--depth", "1", "--no-checkout",
        f"file://{repo}", str(shallow), cwd=tmp_path)
    # Sanity: the sim really is shallow -- the parent object is absent.
    r = subprocess.run(["git", "cat-file", "-e", sha_a], cwd=shallow,
                       capture_output=True)
    assert r.returncode != 0, "sim is not shallow; parent SHA unexpectedly present"
    body = evidence(f"`{sha_a}`",
                    "The base commit the tests ran against.")
    rc, out = run_gate(body, shallow)
    assert rc == 1, out
    assert "dead artifact handle" in out


def test_fabricated_sha_rejected(two_commit_repo):
    """Negative control: a 40-hex SHA that exists nowhere must still fail."""
    repo, _sha_a, _sha_b = two_commit_repo
    fake = "d" * 40
    body = evidence(f"`{fake}`", "A handle pointing at nothing.")
    rc, out = run_gate(body, repo)
    assert rc == 1, out
    assert "dead artifact handle" in out


def test_missing_evidence_section_rejected(two_commit_repo):
    repo, sha_a, _sha_b = two_commit_repo
    rc, out = run_gate(f"No evidence here, just `{sha_a}`.\n", repo)
    assert rc == 1, out
    assert "no `## Evidence` section" in out


def test_existing_path_accepted(two_commit_repo):
    repo, _sha_a, _sha_b = two_commit_repo
    body = evidence("`note.md`", "The file under test, at HEAD.")
    rc, out = run_gate(body, repo)
    assert rc == 0, out


def test_dead_path_rejected(two_commit_repo):
    repo, _sha_a, _sha_b = two_commit_repo
    body = evidence("`nope/missing.md`", "A path that is not in the repo.")
    rc, out = run_gate(body, repo)
    assert rc == 1, out


# --- Wire pin: the checkout the gate runs in --------------------------------

def receipt_job_checkout_segment():
    """Text of the receipt job's checkout step, up to the next step."""
    text = WORKFLOW.read_text()
    m = re.search(r"^  receipt:\n(.*?)(?=^  \S)", text,
                  re.MULTILINE | re.DOTALL)
    assert m, "receipt job not found in worker-protocol-gates.yml"
    job = m.group(1)
    i = job.find("uses: actions/checkout@v4")
    assert i != -1, "receipt job has no actions/checkout step"
    tail = job[i:]
    nxt = re.search(r"\n      - ", tail)
    return tail[:nxt.start()] if nxt else tail


def test_receipt_job_checkout_uses_full_history():
    """The defect's fix, pinned: depth-1 made valid SHA handles unresolvable.

    Sibling jobs (no-silent-deletion, overlap) already use fetch-depth: 0;
    the receipt job must match, or PR #2340's false-red class returns.
    """
    segment = receipt_job_checkout_segment()
    assert "fetch-depth: 0" in segment, (
        "receipt job checkout lost fetch-depth: 0 -- SHA evidence handles "
        "will false-red in the depth-1 merge checkout again.\n"
        f"Checkout step as found:\n{segment}"
    )
