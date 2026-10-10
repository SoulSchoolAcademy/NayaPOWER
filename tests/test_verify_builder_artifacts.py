"""Tests for tools/verify_builder_artifacts.py.

Positive controls prove the verifier ACCEPTS real artifacts; negative
controls prove it REJECTS phantoms (claimed-but-missing). The git tests run
against a local fixture repo (no network); the PR test stubs the gh-api call.
"""

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

TOOL = Path(__file__).resolve().parents[1] / "tools" / "verify_builder_artifacts.py"

sys.path.insert(0, str(TOOL.parent))
import verify_builder_artifacts as vba  # noqa: E402


@pytest.fixture()
def fixture_repo(tmp_path):
    """A tiny local git repo: main branch + feature branch + known file."""
    repo = tmp_path / "fixture.git"
    work = tmp_path / "work"
    subprocess.run(["git", "init", "-q", "-b", "main", str(work)], check=True)
    subprocess.run(
        ["git", "-C", str(work), "config", "user.email", "t@t"], check=True
    )
    subprocess.run(
        ["git", "-C", str(work), "config", "user.name", "t"], check=True
    )
    payload = b"builder artifact bytes\n"
    (work / "hello.txt").write_bytes(payload)
    subprocess.run(["git", "-C", str(work), "add", "."], check=True)
    subprocess.run(
        ["git", "-C", str(work), "commit", "-qm", "add hello"], check=True
    )
    main_sha = subprocess.run(
        ["git", "-C", str(work), "rev-parse", "HEAD"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    subprocess.run(
        ["git", "-C", str(work), "checkout", "-qb", "feature"], check=True
    )
    (work / "other.txt").write_text("x")
    subprocess.run(["git", "-C", str(work), "add", "."], check=True)
    subprocess.run(
        ["git", "-C", str(work), "commit", "-qm", "add other"], check=True
    )
    feature_sha = subprocess.run(
        ["git", "-C", str(work), "rev-parse", "HEAD"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    # Bare clone serves as the "remote".
    subprocess.run(
        ["git", "clone", "-q", "--bare", str(work), str(repo)], check=True
    )
    return {
        "remote": str(repo),
        "main_sha": main_sha,
        "feature_sha": feature_sha,
        "hello_sha256": hashlib.sha256(payload).hexdigest(),
        "hello_bytes": len(payload),
    }


def run_tool(receipt_path, repo, ref="main", fmt="json"):
    p = subprocess.run(
        [sys.executable, str(TOOL), "--repo", repo, "--ref", ref,
         "--format", fmt, str(receipt_path)],
        capture_output=True, text=True, timeout=180,
    )
    return p


def write_receipt(tmp_path, artifacts):
    rp = tmp_path / "receipt.json"
    rp.write_text(json.dumps({"artifacts": artifacts}))
    return rp


# ---- positive controls: real artifacts verify ----

def test_file_exists_positive(fixture_repo, tmp_path):
    f = fixture_repo
    rp = write_receipt(tmp_path, [{
        "kind": "file", "path": "hello.txt", "ref": "main",
        "sha256": f["hello_sha256"], "min_bytes": f["hello_bytes"],
    }])
    p = run_tool(rp, f["remote"])
    assert p.returncode == 0, p.stdout + p.stderr
    out = json.loads(p.stdout)
    assert out["ok"] and out["summary"] == {"pass": 1, "fail": 0}


def test_branch_and_commit_positive(fixture_repo, tmp_path):
    f = fixture_repo
    rp = write_receipt(tmp_path, [
        {"kind": "branch", "name": "feature"},
        {"kind": "commit", "sha": f["feature_sha"], "ancestor_of": "feature"},
        {"kind": "commit", "sha": f["main_sha"], "ref": f["main_sha"]},
    ])
    p = run_tool(rp, f["remote"])
    assert p.returncode == 0, p.stdout + p.stderr
    out = json.loads(p.stdout)
    assert out["ok"] and out["summary"]["pass"] == 3


def test_pr_positive_stubbed(tmp_path, monkeypatch):
    canned = {
        "number": 1759, "state": "closed", "merged_at": "2026-10-07T19:56:06Z",
        "head": {"sha": "8012bd26" + "0" * 32},
    }
    monkeypatch.setattr(
        vba, "gh_api_get", lambda gh, path: canned if "1759" in path else None
    )
    monkeypatch.setattr(vba, "find_gh_api", lambda: "/bin/true")
    git = vba.GitRemote.__new__(vba.GitRemote)  # unused for pr kind
    v = vba.verify_artifact(
        {"kind": "pr", "number": 1759,
         "head": "8012bd26" + "0" * 32, "state": "closed"},
        git, "/bin/true", "main",
    )
    assert v.ok, v.detail


# ---- negative controls: phantoms are rejected ----

def test_missing_file_is_phantom(fixture_repo, tmp_path):
    f = fixture_repo
    rp = write_receipt(tmp_path, [
        {"kind": "file", "path": "does-not-exist.txt", "ref": "main"},
    ])
    p = run_tool(rp, f["remote"])
    assert p.returncode == 1, p.stdout + p.stderr
    out = json.loads(p.stdout)
    assert not out["ok"] and out["summary"]["fail"] == 1
    assert "PHANTOM" in out["verdicts"][0]["detail"]


def test_missing_branch_is_phantom(fixture_repo, tmp_path):
    f = fixture_repo
    rp = write_receipt(tmp_path, [{"kind": "branch", "name": "no-such-branch"}])
    p = run_tool(rp, f["remote"])
    assert p.returncode == 1
    out = json.loads(p.stdout)
    assert not out["ok"] and "PHANTOM" in out["verdicts"][0]["detail"]


def test_bogus_commit_is_phantom(fixture_repo, tmp_path):
    f = fixture_repo
    rp = write_receipt(tmp_path, [
        {"kind": "commit", "sha": "d" * 40, "ref": "main"},
    ])
    p = run_tool(rp, f["remote"])
    assert p.returncode == 1
    assert not json.loads(p.stdout)["ok"]


def test_wrong_sha256_rejected(fixture_repo, tmp_path):
    f = fixture_repo
    rp = write_receipt(tmp_path, [{
        "kind": "file", "path": "hello.txt", "ref": "main",
        "sha256": "0" * 64,
    }])
    p = run_tool(rp, f["remote"])
    assert p.returncode == 1
    out = json.loads(p.stdout)
    assert "mismatch" in out["verdicts"][0]["detail"]


def test_min_bytes_violation_rejected(fixture_repo, tmp_path):
    f = fixture_repo
    rp = write_receipt(tmp_path, [{
        "kind": "file", "path": "hello.txt", "ref": "main",
        "min_bytes": f["hello_bytes"] + 1000,
    }])
    p = run_tool(rp, f["remote"])
    assert p.returncode == 1
    assert "too small" in json.loads(p.stdout)["verdicts"][0]["detail"]


def test_unresolvable_ref_rejected(fixture_repo, tmp_path):
    f = fixture_repo
    rp = write_receipt(tmp_path, [
        {"kind": "file", "path": "hello.txt", "ref": "no-such-ref"},
    ])
    p = run_tool(rp, f["remote"])
    assert p.returncode == 1
    assert not json.loads(p.stdout)["ok"]


def test_missing_pr_is_phantom_stubbed(monkeypatch):
    monkeypatch.setattr(vba, "gh_api_get", lambda gh, path: None)
    monkeypatch.setattr(vba, "find_gh_api", lambda: "/bin/true")
    git = vba.GitRemote.__new__(vba.GitRemote)
    v = vba.verify_artifact(
        {"kind": "pr", "number": 999999}, git, "/bin/true", "main"
    )
    assert not v.ok and "PHANTOM" in v.detail


def test_malformed_receipt_is_usage_error(tmp_path, fixture_repo):
    rp = tmp_path / "bad.json"
    rp.write_text('{"nope": true}')
    p = run_tool(rp, fixture_repo["remote"])
    assert p.returncode == 2


def test_unknown_kind_rejected(fixture_repo, tmp_path):
    f = fixture_repo
    rp = write_receipt(tmp_path, [{"kind": "teleport", "x": 1}])
    p = run_tool(rp, f["remote"])
    assert p.returncode == 1
    assert "unknown kind" in json.loads(p.stdout)["verdicts"][0]["detail"]


def test_path_traversal_rejected(fixture_repo, tmp_path):
    f = fixture_repo
    rp = write_receipt(tmp_path, [
        {"kind": "file", "path": "../escape.txt", "ref": "main"},
    ])
    p = run_tool(rp, f["remote"])
    assert p.returncode == 1
    assert "invalid path" in json.loads(p.stdout)["verdicts"][0]["detail"]
