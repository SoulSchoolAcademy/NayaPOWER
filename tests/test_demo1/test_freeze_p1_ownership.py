"""P1 RED: freeze_evidence.py scratch-deletion ownership.

Shawn's directive: freeze_evidence.py deleted run_root after checking only
that it resolves beneath /tmp. That accepts /tmp itself and another
worker's scratch directory.

These tests verify REFUSAL for unsafe targets WITHOUT performing deletion.
The target directory must still exist after the refused run.
"""
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "demo1" / "freeze_evidence.py"


def _run_freeze(*args):
    """Run freeze_evidence.py; return (returncode, stdout+stderr)."""
    # Use the real HEAD so we pass the worktree check and reach
    # the run_root refusal logic.
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        capture_output=True, text=True, cwd=REPO_ROOT,
    ).stdout.strip()
    p = subprocess.run(
        [sys.executable, str(SCRIPT), "--code-head", head, *args],
        capture_output=True, text=True, cwd=REPO_ROOT,
    )
    return p.returncode, p.stdout + p.stderr


def test_p1_refuses_tmp_itself(tmp_path):
    """--run-root /tmp must be refused; /tmp must survive."""
    # Use a --out under evidence/ so we pass the out-containment check.
    # (The refusal must come from the run_root check, not out.)
    out = REPO_ROOT / "evidence" / "demo1" / "test-p1-tmp-itself"
    rc, output = _run_freeze(
        "--run-root", "/tmp",
        "--out", str(out),
    )
    assert rc != 0, "must refuse /tmp itself"
    assert "containment root" in output.lower(), f"wrong refusal: {output[:200]}"
    assert Path("/tmp").exists(), "/tmp must not be deleted"


def test_p1_refuses_unrelated_existing_dir(tmp_path):
    """An existing dir without our ownership marker must be refused."""
    victim = tmp_path / "other-worker-scratch"
    victim.mkdir()
    (victim / "important.txt").write_text("do not delete", encoding="utf-8")
    out = REPO_ROOT / "evidence" / "demo1" / "test-p1-unrelated"
    rc, output = _run_freeze(
        "--run-root", str(victim),
        "--out", str(out),
    )
    assert rc != 0, "must refuse unrelated existing directory"
    assert "ownership" in output.lower(), f"wrong refusal: {output[:200]}"
    assert victim.exists(), "victim directory must survive"
    assert (victim / "important.txt").exists(), "victim files must survive"


def test_p1_refuses_symlink(tmp_path):
    """A symlink --run-root must be refused."""
    real = tmp_path / "real-dir"
    real.mkdir()
    link = tmp_path / "link-dir"
    link.symlink_to(real, target_is_directory=True)
    out = REPO_ROOT / "evidence" / "demo1" / "test-p1-symlink"
    rc, output = _run_freeze(
        "--run-root", str(link),
        "--out", str(out),
    )
    assert rc != 0, "must refuse symlink"
    assert "symlink" in output.lower(), f"wrong refusal: {output[:200]}"
    assert real.exists(), "symlink target must survive"


def test_p1_refuses_escape_via_dotdot(tmp_path):
    """--run-root with .. escaping /tmp must be refused."""
    out = REPO_ROOT / "evidence" / "demo1" / "test-p1-escape"
    rc, output = _run_freeze(
        "--run-root", "/tmp/../etc",
        "--out", str(out),
    )
    assert rc != 0, "must refuse path escaping /tmp"
    assert "refused" in output.lower()
