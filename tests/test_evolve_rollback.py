"""Tests for tools/evolve_rollback.py — EVOLVE rollback machinery.

Hermetic: every test builds its own tmp workdir + scratch dir; the repo
itself is never mutated. The tool is exercised through its real CLI so exit
codes (0=ADOPTED, 1=ROLLED_BACK, 2=FAIL-CLOSED) are part of the contract.
"""
import base64
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "evolve_rollback.py"


def run_tool(*argv):
    return subprocess.run(
        [sys.executable, str(TOOL), *argv],
        capture_output=True, text=True, timeout=120,
    )


def write_file(workdir: Path, rel: str, content: str) -> Path:
    p = workdir / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return p


def tree_hashes(workdir: Path) -> dict:
    out = {}
    for p in sorted(workdir.rglob("*")):
        if p.is_file():
            out[p.relative_to(workdir).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def make_proposal(path: Path, changes: dict, verify_cmd, proposal_id="EVOLVE-TEST-001",
                   base_commit="UNGOVERNED", blast_radius="COMPONENT"):
    proposal = {
        "proposal_id": proposal_id,
        "base_commit": base_commit,
        "blast_radius": blast_radius,
        "rationale": "test evolution",
        "changes": [
            {"path": rel, "content_b64": base64.b64encode(content.encode()).decode()}
            for rel, content in changes.items()
        ],
        "verify": {"cmd": verify_cmd, "timeout_s": 60},
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(proposal), encoding="utf-8")
    return path


@pytest.fixture
def env(tmp_path):
    workdir = tmp_path / "work"
    scratch = tmp_path / "scratch"
    workdir.mkdir()
    write_file(workdir, "a.txt", "original-a\n")
    write_file(workdir, "sub/b.txt", "original-b\n")
    return workdir, scratch


def test_adopt_on_verify_pass(env):
    workdir, scratch = env
    before = tree_hashes(workdir)
    prop = make_proposal(scratch / "p.json", {"a.txt": "evolved-a\n"},
                         [sys.executable, "-c", "import sys; sys.exit(0)"])
    # also create a brand-new file through the evolution
    prop_data = json.loads((scratch / "p.json").read_text())
    prop_data["changes"].append({
        "path": "new.txt",
        "content_b64": base64.b64encode(b"brand new\n").decode(),
    })
    (scratch / "p.json").write_text(json.dumps(prop_data))

    r = run_tool("execute", "--proposal", str(scratch / "p.json"),
                 "--workdir", str(workdir), "--scratch", str(scratch))
    assert r.returncode == 0, r.stderr
    assert (workdir / "a.txt").read_text() == "evolved-a\n"
    assert (workdir / "new.txt").read_text() == "brand new\n"
    assert (workdir / "sub/b.txt").read_text() == "original-b\n"
    receipts = list((scratch / "receipts").glob("*-ADOPTED-*.json"))
    assert len(receipts) == 1
    receipt = json.loads(receipts[0].read_text())
    assert receipt["schema"] == "NAYANET_EVOLVE_ROLLBACK_RECEIPT_V1"
    assert receipt["verdict"] == "ADOPTED"
    assert receipt["proposal_id"] == "EVOLVE-TEST-001"
    # untouched files are byte-identical
    assert tree_hashes(workdir)["sub/b.txt"] == before["sub/b.txt"]


def test_rollback_on_verify_fail(env):
    workdir, scratch = env
    before = tree_hashes(workdir)
    prop = make_proposal(scratch / "p.json", {"a.txt": "broken-a\n", "sub/b.txt": "broken-b\n"},
                         [sys.executable, "-c", "import sys; sys.exit(3)"])

    r = run_tool("execute", "--proposal", str(prop),
                 "--workdir", str(workdir), "--scratch", str(scratch))
    assert r.returncode == 1, r.stderr  # ROLLED_BACK, not an error
    # tree is byte-identical to the pre-arm state
    assert tree_hashes(workdir) == before
    receipts = list((scratch / "receipts").glob("*-ROLLED_BACK-*.json"))
    assert len(receipts) == 1
    receipt = json.loads(receipts[0].read_text())
    assert receipt["verdict"] == "ROLLED_BACK"
    assert "VERIFY_FAILED" in receipt["reason"]
    assert receipt["tree_match"] is True
    assert receipt["verify"]["exit_code"] == 3


def test_silent_drop_detected_even_when_verify_passes(env):
    """The 2026-10-07 head-tree incident: a change that silently drops a file
    the proposal never declared must trigger rollback even if verify passes."""
    workdir, scratch = env
    before = tree_hashes(workdir)
    prop = make_proposal(scratch / "p.json", {"a.txt": "evolved-a\n"},
                         [sys.executable, "-c", "import sys; sys.exit(0)"])

    r = run_tool("arm", "--proposal", str(prop),
                 "--workdir", str(workdir), "--scratch", str(scratch))
    assert "ARMED" in r.stderr, r.stderr
    # an outside actor silently deletes a file the proposal never declared
    (workdir / "sub" / "b.txt").unlink()
    r = run_tool("apply", "--proposal", str(prop),
                 "--workdir", str(workdir), "--scratch", str(scratch))
    assert r.returncode == 1, r.stderr
    assert tree_hashes(workdir) == before  # rolled back, byte-identical
    receipts = list((scratch / "receipts").glob("*-ROLLED_BACK-*.json"))
    assert len(receipts) == 1
    receipt = json.loads(receipts[0].read_text())
    assert "SILENT_CHANGE_DETECTED" in receipt["reason"]
    assert "sub/b.txt" in receipt["reason"]


def test_tampered_snapshot_fail_closed(env):
    workdir, scratch = env
    prop = make_proposal(scratch / "p.json", {"a.txt": "broken-a\n"},
                         [sys.executable, "-c", "import sys; sys.exit(1)"])

    r = run_tool("arm", "--proposal", str(prop),
                 "--workdir", str(workdir), "--scratch", str(scratch))
    assert "ARMED" in r.stderr, r.stderr
    r = run_tool("apply", "--proposal", str(prop),
                 "--workdir", str(workdir), "--scratch", str(scratch))
    assert "APPLIED" in r.stderr, r.stderr
    # tamper with the snapshot bytes before the rollback decision
    snap_file = scratch / "snapshot" / "a.txt"
    assert snap_file.is_file()
    snap_file.write_text("TAMPERED\n", encoding="utf-8")

    r = run_tool("decide", "--proposal", str(prop),
                 "--workdir", str(workdir), "--scratch", str(scratch))
    assert r.returncode == 2, r.stderr  # fail-closed, not a silent bad restore
    receipts = list((scratch / "receipts").glob("*-ROLLBACK_INCOMPLETE-*.json"))
    assert len(receipts) == 1
    receipt = json.loads(receipts[0].read_text())
    assert "SNAPSHOT_TAMPERED" in receipt["reason"]
    # workdir left untouched in the applied (broken) state — loudly, not hidden
    assert (workdir / "a.txt").read_text() == "broken-a\n"


def test_stale_proposal_refused(tmp_path):
    workdir = tmp_path / "work"
    scratch = tmp_path / "scratch"
    workdir.mkdir()
    write_file(workdir, "a.txt", "v1\n")
    subprocess.run(["git", "init", "-q", str(workdir)], check=True, timeout=30)
    subprocess.run(["git", "-C", str(workdir), "add", "."], check=True, timeout=30)
    subprocess.run(["git", "-C", str(workdir), "-c", "user.email=t@t", "-c", "user.name=t",
                    "commit", "-qm", "v1"], check=True, timeout=30)
    head = subprocess.run(["git", "-C", str(workdir), "rev-parse", "HEAD"],
                          capture_output=True, text=True, check=True, timeout=30).stdout.strip()

    prop = make_proposal(scratch / "p.json", {"a.txt": "v2\n"},
                         [sys.executable, "-c", "pass"],
                         base_commit="0" * 40)  # stale base
    r = run_tool("execute", "--proposal", str(prop),
                 "--workdir", str(workdir), "--scratch", str(scratch))
    assert r.returncode == 2, r.stderr
    assert "STALE_PROPOSAL" in r.stderr
    assert (workdir / "a.txt").read_text() == "v1\n"  # untouched
    assert subprocess.run(["git", "-C", str(workdir), "rev-parse", "HEAD"],
                          capture_output=True, text=True, timeout=30).stdout.strip() == head
    # a proposal pinned at the real HEAD arms fine (then verify passes -> adopted)
    prop2 = make_proposal(scratch / "p2.json", {"a.txt": "v2\n"},
                          [sys.executable, "-c", "pass"], proposal_id="EVOLVE-TEST-002",
                          base_commit=head)
    r = run_tool("execute", "--proposal", str(prop2),
                 "--workdir", str(workdir), "--scratch", str(scratch))
    assert r.returncode == 0, r.stderr
    assert (workdir / "a.txt").read_text() == "v2\n"


def test_empty_changeset_and_forbidden_radius_refused(env):
    workdir, scratch = env
    before = tree_hashes(workdir)

    prop = make_proposal(scratch / "p.json", {}, [sys.executable, "-c", "pass"])
    r = run_tool("execute", "--proposal", str(prop),
                 "--workdir", str(workdir), "--scratch", str(scratch))
    assert r.returncode == 2
    assert "non-empty" in r.stderr

    prop2 = make_proposal(scratch / "p2.json", {"a.txt": "x\n"},
                          [sys.executable, "-c", "pass"],
                          proposal_id="EVOLVE-TEST-003", blast_radius="PRODUCTION")
    r = run_tool("execute", "--proposal", str(prop2),
                 "--workdir", str(workdir), "--scratch", str(scratch))
    assert r.returncode == 2
    assert "PRODUCTION" in r.stderr
    assert tree_hashes(workdir) == before  # nothing touched in either case
