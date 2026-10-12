"""Red-green tests for the push_branch_api.py >1MiB refuse-with-redirect guard.

The guard (INFRA, 2026-10-12): before any gh-api call, measure the exact argv
payload of the tree POST; if it exceeds 1 MiB, refuse with a stderr message
naming the exact push_branch_preserve.py redirect invocation. This closes the
failure that killed a live brain-index regen push ("Arg List Too Long" on a
~6MB blob via the gh-api argv).

Red: these tests FAIL against the unguarded script (no guard entry point,
no refusal). Green: they PASS on the guarded script.
"""
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "tools" / "push_branch_api.py"


def load_module(path):
    spec = importlib.util.spec_from_file_location("push_branch_api_under_test", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


mod = load_module(SCRIPT)

ROOT = "/home/hatch/workspace/nayapower-work"
BRANCH = "naya5/push-api-size-guard"
BASE = "501bf82a3c00000000000000000000000000000000"


def make_entries(total_bytes, n_files=4):
    """Synthetic tree entries whose JSON content sums to ~total_bytes."""
    per = max(1, total_bytes // n_files)
    return [
        {"path": f"synthetic-{i}.bin", "mode": "100644", "type": "blob",
         "content": "x" * per}
        for i in range(n_files)
    ]


def test_guard_refuses_over_1mb_with_redirect_message():
    """The red-green core: a >1MiB payload is REFUSED with the redirect."""
    entries = make_entries(mod.ARGV_PAYLOAD_LIMIT_BYTES + 65_536)
    body = {"base_tree": "0" * 40, "tree": entries}
    try:
        mod.guard_argv_payload(body, ROOT, BRANCH, BASE)
    except mod.PayloadTooLargeError as e:
        msg = str(e)
        assert "REFUSED" in msg
        assert "push_branch_preserve.py" in msg
        # The exact equivalent invocation, copy-pasteable:
        assert f"python3 {mod.PRESERVE_SCRIPT} {ROOT} {BRANCH} {BASE}" in msg
        # Names the measured size so the operator can see the scale:
        assert "MiB" in msg
        return
    raise AssertionError("guard did NOT refuse a >1MiB payload")


def test_guard_boundary_just_over_limit_refuses():
    """One byte over the limit still refuses (no off-by-one)."""
    entries = make_entries(1)
    body = {"base_tree": "0" * 40, "tree": entries}
    # Grow content until the measured payload is exactly limit+1
    size = mod.measure_argv_payload(body)
    deficit = (mod.ARGV_PAYLOAD_LIMIT_BYTES + 1) - size
    entries[0]["content"] += "y" * deficit
    try:
        mod.guard_argv_payload(body, ROOT, BRANCH, BASE)
    except mod.PayloadTooLargeError:
        return
    raise AssertionError("guard did NOT refuse at limit+1 bytes")


def test_guard_allows_under_1mb_normal_path():
    """The control: a <1MiB payload passes the guard — normal path proceeds."""
    entries = make_entries(mod.ARGV_PAYLOAD_LIMIT_BYTES - 65_536)
    body = {"base_tree": "0" * 40, "tree": entries}
    size = mod.guard_argv_payload(body, ROOT, BRANCH, BASE)
    assert size == len(json.dumps(body).encode("utf-8"))
    assert size < mod.ARGV_PAYLOAD_LIMIT_BYTES


def test_measure_argv_payload_matches_exact_argv_string():
    """The measurement is the true argv cost: the exact JSON gh() appends."""
    entries = make_entries(10_000)
    body = {"base_tree": "abc", "tree": entries}
    assert mod.measure_argv_payload(body) == len(json.dumps(body).encode("utf-8"))


def test_refuse_message_names_no_remote_change():
    """The message states nothing was pushed (safe to retry via redirect)."""
    entries = make_entries(mod.ARGV_PAYLOAD_LIMIT_BYTES + 1)
    body = {"base_tree": "0" * 40, "tree": entries}
    try:
        mod.guard_argv_payload(body, ROOT, BRANCH, BASE)
    except mod.PayloadTooLargeError as e:
        assert "Nothing was pushed" in str(e)
        return
    raise AssertionError("expected refusal")


def test_main_refuses_multimb_repo_end_to_end(tmp_path):
    """main() on a real git repo with a >1MiB file: exits 3, prints redirect.

    The guard fires BEFORE any gh-api call, so this needs no network and
    changes no remote state. Skipped where git is unavailable.
    """
    git = shutil.which("git")
    if git is None:
        import pytest
        pytest.skip("git not available")
    repo = tmp_path / "repo"
    repo.mkdir()
    def g(*args):
        subprocess.run([git, *args], cwd=repo, check=True,
                       capture_output=True, text=True)
    g("init", "-q", "-b", "main")
    g("config", "user.email", "t@t")
    g("config", "user.name", "t")
    (repo / "f.txt").write_text("base")
    g("add", ".")
    g("commit", "-qm", "base")
    base = subprocess.run([git, "rev-parse", "HEAD"], cwd=repo,
                          capture_output=True, text=True,
                          check=True).stdout.strip()
    (repo / "big.bin").write_text("z" * (mod.ARGV_PAYLOAD_LIMIT_BYTES + 1024))
    g("add", "big.bin")
    g("commit", "-qm", "big")
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), str(repo), "main", base],
        capture_output=True, text=True)
    assert proc.returncode == 3, proc.stdout + proc.stderr
    assert "REFUSED" in proc.stderr
    assert "push_branch_preserve.py" in proc.stderr
    assert f"python3 {mod.PRESERVE_SCRIPT} {repo} main {base}" in proc.stderr
    assert "gh-api" not in proc.stdout  # no API call was attempted


def test_guard_refuses_oversize_commit_body_too():
    """The commit POST also travels via argv: a huge message refuses."""
    body = {"message": "m" * (mod.ARGV_PAYLOAD_LIMIT_BYTES + 1),
            "tree": "0" * 40, "parents": ["0" * 40]}
    try:
        mod.guard_argv_payload(body, ROOT, BRANCH, BASE, what="commit")
    except mod.PayloadTooLargeError as e:
        assert "commit" in str(e)
        assert "push_branch_preserve.py" in str(e)
        return
    raise AssertionError("guard did NOT refuse an oversize commit body")


if __name__ == "__main__":
    sys.exit(0)
