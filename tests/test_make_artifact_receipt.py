"""Tests for tools/make_artifact_receipt.py (ACT sign-out wiring).

The generator must emit exactly the receipt schema consumed by
tools/verify_builder_artifacts.py, and must reject malformed inputs
fail-closed (exit 2) rather than emitting a bad receipt.
"""

import json
import subprocess
import sys
from pathlib import Path

TOOL = Path(__file__).resolve().parent.parent / "tools" / "make_artifact_receipt.py"


def run(*argv):
    return subprocess.run(
        [sys.executable, str(TOOL), *argv],
        capture_output=True, text=True, timeout=30,
    )


def receipt_of(proc):
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_pr_basic():
    r = receipt_of(run("--pr", "1767"))
    assert r == {"artifacts": [{"kind": "pr", "number": 1767}]}


def test_pr_with_pins():
    head = "c" * 40
    r = receipt_of(run("--pr", f"1767:head={head},state=open"))
    assert r["artifacts"][0] == {
        "kind": "pr", "number": 1767, "head": head, "state": "open",
    }


def test_pr_rejects_non_numeric():
    p = run("--pr", "abc")
    assert p.returncode == 2


def test_pr_rejects_bad_head_pin():
    p = run("--pr", "1767:head=xyz")
    assert p.returncode == 2


def test_pr_rejects_bad_state_pin():
    p = run("--pr", "1767:state=bogus")
    assert p.returncode == 2


def test_branch():
    r = receipt_of(run("--branch", "main"))
    assert r == {"artifacts": [{"kind": "branch", "name": "main"}]}


def test_branch_rejects_traversal():
    p = run("--branch", "../evil")
    assert p.returncode == 2


def test_commit():
    sha = "f" * 40
    r = receipt_of(run("--commit", sha))
    assert r == {"artifacts": [{"kind": "commit", "sha": sha}]}


def test_commit_with_ancestor():
    sha = "f" * 40
    r = receipt_of(run("--commit", f"{sha}:main"))
    assert r["artifacts"][0] == {"kind": "commit", "sha": sha, "ancestor_of": "main"}


def test_commit_rejects_short_sha():
    p = run("--commit", "abc123")
    assert p.returncode == 2


def test_file_with_ref_and_pins():
    r = receipt_of(run("--file", "tools/x.py:main,min_bytes=100"))
    assert r["artifacts"][0] == {
        "kind": "file", "path": "tools/x.py", "ref": "main", "min_bytes": 100,
    }


def test_file_rejects_traversal():
    p = run("--file", "../secret:main")
    assert p.returncode == 2


def test_file_rejects_bad_sha256():
    p = run("--file", "tools/x.py:main,sha256=xyz")
    assert p.returncode == 2


def test_multiple_artifacts_compose():
    r = receipt_of(run("--pr", "1767", "--branch", "main", "--commit", "a" * 40))
    assert len(r["artifacts"]) == 3
    assert [a["kind"] for a in r["artifacts"]] == ["pr", "branch", "commit"]


def test_no_artifacts_is_usage_error():
    p = run()
    assert p.returncode == 2


def test_out_writes_file(tmp_path):
    out = tmp_path / "receipt.json"
    p = run("--pr", "1767", "--out", str(out))
    assert p.returncode == 0, p.stderr
    assert json.loads(out.read_text()) == {"artifacts": [{"kind": "pr", "number": 1767}]}


def test_output_is_valid_receipt_schema():
    # The verifier requires a top-level "artifacts" list; the generator
    # must always emit exactly that shape.
    r = receipt_of(run("--pr", "1", "--branch", "b", "--commit", "d" * 40,
                       "--file", "f.py"))
    assert set(r.keys()) == {"artifacts"}
    assert isinstance(r["artifacts"], list) and len(r["artifacts"]) == 4
