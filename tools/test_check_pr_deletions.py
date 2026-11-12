"""test_check_pr_deletions.py — tests for tools/check_pr_deletions.py.

Includes the #2600 replay (2026-10-15): the real merge message of bb45896f
(Gamma's w181 resolution — deleted tests/test_post_checker.py with a prose
rationale, but no `## Deletions` section in the PR body) must FAIL the old
gate and PASS the new one. The old implementation is frozen inline as
OLD_GATE_SOURCE so the replay documents the artifact class permanently.

D32 note: the replay sets PR_BODY="" — the real #2600 body provably contains
no `## Deletions` section (pulls API, w183), so the body channel is inert
for the old gate either way; the verdicts (old FAIL / new PASS) are faithful
regardless of the body's remaining prose.

Run:  python3 -m pytest tools/test_check_pr_deletions.py -q
"""
import os
import subprocess
import sys

import pytest

GATE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "check_pr_deletions.py")

# Verbatim message of bb45896f (GET /repos/SoulSchoolAcademy/NayaPOWER/
# git/commits/bb45896f6306a9a794b4ed2947671c8b2727dd05, w183).
REAL_2600_MESSAGE = """Resolve #2600 add/add conflict: tools/post_checker.py (w181 surgical merge)

What changed: reconciled the single TRUE conflict at true merge-base
c13f260fad3d73847a88043cdbc42062d3af53b4 (tip blob 4e5fdff0 vs head blob
99a891ac) per builder-packet-2600-conflict-w180.md. Head's three-level
protocol (PULSE/RECEIPT/EVENT + DEDUP + CLAIM-CHECK) is canonical; ported
from the tip: _unquoted() (quoted/fenced lines never bind), ROSTER names
folded into the identity regex (Naya 1-5, Narzan leads), contextual
ANCHORED_SHA_RE (7-40 hex with sha/commit/tree/tip/head/ref anchors) OR'd
with the bare 40-hex check, and score-meaning rigor on RECEIPT (no bare
numbers, ever). Tip's old-schema tests/test_post_checker.py superseded by
tests/test_post_checker_tip_translated.py (failure-mode coverage
translated to the current schema; the duplicate-basename layout broke
`pytest -q` collection, so the translated battery carries a unique name).
Rehearsed tree 3d507b574ee25abd3c3264f5983e916f72f4ea58; 45/45 tests green.

NOT claimed: merge to main (cron workers never merge), CI green on this
head, independent validation. Fresh CI fires on push; fresh different-seat
IV owed — Epsilon's IV on 6499295050 does NOT transfer to this head.

Next: dock judges the five merge conditions on the new head | owner: merge dock
"""

# Pre-fix implementation, frozen 2026-10-15 (PR-body `## Deletions` only).
OLD_GATE_SOURCE = r'''#!/usr/bin/env python3
import os
import re
import subprocess
import sys


def fail(msg):
    print(f"DELETION GATE FAILED: {msg}")
    print("Fix: either rebase onto current main (if the deletion is a stale-")
    print("head accident), or declare each deletion under `## Deletions` in the")
    print("PR body with one line of reason per file.")
    sys.exit(1)


def main():
    base = os.environ.get("BASE_SHA", "")
    head = os.environ.get("HEAD_SHA", "")
    body = os.environ.get("PR_BODY") or ""
    if not base or not head:
        print("No base/head SHAs provided; skipping deletion check.")
        return
    out = subprocess.run(
        ["git", "diff", "--name-status", f"{base}...{head}"],
        capture_output=True, text=True)
    if out.returncode != 0:
        print(f"git diff failed ({out.stderr.strip()}); skipping.")
        return
    deleted = [line.split("\t", 1)[1] for line in out.stdout.splitlines()
               if line.startswith("D\t")]
    if not deleted:
        print("No deletions. Clean.")
        return

    m = re.search(r"^##\s+deletions\s*$", body, re.IGNORECASE | re.MULTILINE)
    declared = ""
    if m:
        declared = body[m.end():]
        nxt = re.search(r"^##\s+", declared, re.MULTILINE)
        if nxt:
            declared = declared[:nxt.start()]
    declared_low = declared.lower()

    undeclared = [f for f in deleted
                 if f.lower() not in declared_low
                 and os.path.basename(f).lower() not in declared_low]
    if undeclared:
        fail(f"{len(undeclared)} undeclared deletion(s): "
             f"{', '.join(undeclared[:10])}. "
             f"Total deleted in this PR: {len(deleted)}.")
    print(f"Deletion check OK: {len(deleted)} deletion(s), all declared.")


if __name__ == "__main__":
    main()
'''


def make_repo(tmp_path, message, delete=("tests/test_post_checker.py",)):
    repo = tmp_path / "repo"
    repo.mkdir()
    def run(*a):
        return subprocess.run(a, cwd=repo, check=True,
                              capture_output=True, text=True)
    run("git", "init", "-b", "main")
    run("git", "config", "user.email", "test@naya.local")
    run("git", "config", "user.name", "naya-test")
    (repo / "keep.txt").write_text("keep\n")
    (repo / "tests").mkdir()
    (repo / "tests" / "test_post_checker.py").write_text("# old battery\n")
    run("git", "add", "-A")
    run("git", "commit", "-m", "base")
    base = run("git", "rev-parse", "HEAD").stdout.strip()
    for d in delete:
        (repo / d).unlink()
    if not delete:
        # keep the head commit non-empty so the fixture always has a diff
        with open(repo / "keep.txt", "a") as f:
            f.write("touched\n")
    run("git", "add", "-A")
    run("git", "commit", "-m", message)
    head = run("git", "rev-parse", "HEAD").stdout.strip()
    return repo, base, head


def run_gate(source, repo, base, head, body):
    env = dict(os.environ, BASE_SHA=base, HEAD_SHA=head, PR_BODY=body)
    out = subprocess.run([sys.executable, str(source)], cwd=repo, env=env,
                         capture_output=True, text=True)
    return out.returncode, out.stdout


@pytest.fixture()
def old_gate(tmp_path):
    p = tmp_path / "old_gate.py"
    p.write_text(OLD_GATE_SOURCE)
    return p


def test_2600_replay_old_gate_fails(tmp_path, old_gate):
    """The artifact: pre-fix gate FAILED on the real #2600 merge message."""
    repo, base, head = make_repo(tmp_path, REAL_2600_MESSAGE)
    rc, out = run_gate(old_gate, repo, base, head, "")
    assert rc == 1, out
    assert "DELETION GATE FAILED" in out
    assert "tests/test_post_checker.py" in out


def test_2600_replay_new_gate_passes(tmp_path):
    """The fix: merge-message prose rationale now declares the deletion."""
    repo, base, head = make_repo(tmp_path, REAL_2600_MESSAGE)
    rc, out = run_gate(GATE, repo, base, head, "")
    assert rc == 0, out
    assert "all declared" in out
    assert "prose+rationale" in out


def test_fail_closed_undeclared_deletion(tmp_path):
    """A truly silent deletion still fails — the stale-head trap is dead."""
    repo, base, head = make_repo(tmp_path, "cleanup: remove dead code")
    rc, out = run_gate(GATE, repo, base, head, "")
    assert rc == 1, out
    assert "DELETION GATE FAILED" in out


def test_pr_body_section_regression(tmp_path):
    """The original channel (PR body `## Deletions`) still works."""
    repo, base, head = make_repo(tmp_path, "cleanup")
    body = "## Deletions\ntests/test_post_checker.py — superseded by the translated battery\n"
    rc, out = run_gate(GATE, repo, base, head, body)
    assert rc == 0, out
    assert "section" in out


def test_drop_rationale_alias_in_commit_message(tmp_path):
    repo, base, head = make_repo(
        tmp_path, "cleanup\n\n## Drop rationale\ntests/test_post_checker.py: replaced\n")
    rc, out = run_gate(GATE, repo, base, head, "")
    assert rc == 0, out


def test_waiver_trailer(tmp_path):
    """Explicit waiver passes but names the file — never silent."""
    repo, base, head = make_repo(
        tmp_path, "do the thing\n\nWaived-Deletions: tests/test_post_checker.py\n")
    rc, out = run_gate(GATE, repo, base, head, "")
    assert rc == 0, out
    assert "waiver" in out
    assert "tests/test_post_checker.py" in out


def test_prose_mention_without_cue_fails(tmp_path):
    """Naming the path without a rationale cue is not a declaration."""
    repo, base, head = make_repo(
        tmp_path, "see tests/test_post_checker.py for the old battery layout")
    rc, out = run_gate(GATE, repo, base, head, "")
    assert rc == 1, out


def test_no_deletions_clean(tmp_path):
    repo, base, head = make_repo(tmp_path, "touch nothing", delete=())
    rc, out = run_gate(GATE, repo, base, head, "")
    assert rc == 0, out
    assert "No deletions" in out
