#!/usr/bin/env python3
"""Brain-index auto-stamp orchestrator.

Heals brain-index drift at the source: runs the OFFICIAL generator
(tools/regenerate_brain_index.py -- never hand-edits, never reimplements it)
and commits the resulting receipt files so that whatever merges or lands is
always stamped.

Why this exists (diagnosed 2026-10-11 from PR #2230): the drift DETECTOR works
-- kernel-tests runs `regenerate_brain_index.py --check` and it correctly
failed on #2230's head. The PR merged anyway via owner self-merge override
(four red checks: test, receipt gate, team review, delivery-gate). More red
checks cannot close that bypass -- the owner can always run the light. So the
enforcement moves from "red light" to "repaved road": the machine commits the
stamp onto the PR head (pull_request trigger) or onto main itself (push
trigger for direct pushes), so no unstamped BRAIN/ change can land regardless
of who clicks merge. This script is the enforcement; the workflow file
`.github/workflows/brain-index-auto-stamp.yml` is the trigger.

Exit codes: 0 = ok (NO-STAMP or stamp committed [+ pushed]);
           2 = fail-closed (dirty worktree, generator failure, unexpected
               files touched, bad repo root) -- nothing committed, nothing pushed;
           3 = committed but the push failed (retry once after rebase).

Loop safety: pushes made with GitHub's GITHUB_TOKEN do not trigger new
workflow runs, so the stamp commit cannot re-trigger this workflow.
"""

from __future__ import annotations

import argparse
import importlib.util
import subprocess
import sys
from pathlib import Path

# The receipt files the official generator owns. Any regen output OUTSIDE
# this set is treated as a fail-closed abort. Coupled to the generator's own
# RECEIPT_PATHS by test_brain_index_auto_stamp.py::test_receipt_set_matches_generator.
RECEIPT_PATHS = frozenset({
    "BRAIN/REAL-TREE.json",
    "BRAIN/REAL-TREE.md",
    "BRAIN/NAYAPOWER-BRAIN-INDEX.json",
})

STAMP_COMMIT_MESSAGE = (
    "chore(brain-index): auto-stamp after BRAIN/ change [auto-stamp]\n"
    "\n"
    "Machine-committed by the brain-index auto-stamp: the official generator\n"
    "(tools/regenerate_brain_index.py) re-ran and produced receipt changes.\n"
    "Human content untouched -- receipt files only."
)


def run(cmd: list[str], cwd: Path, check: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)


def looks_like_repo(root: Path) -> bool:
    return (root / "BRAIN").is_dir() and (root / ".git").exists()


def worktree_is_clean(root: Path) -> bool:
    return run(["git", "status", "--porcelain"], root).stdout.strip() == ""


def changed_paths(root: Path) -> list[str]:
    out = run(["git", "status", "--porcelain"], root).stdout
    paths: list[str] = []
    for line in out.splitlines():
        # porcelain v1: XY <path> (or "XY orig -> new" for renames)
        rest = line[3:]
        if " -> " in rest:
            rest = rest.split(" -> ", 1)[1]
        paths.append(rest.strip().strip('"'))
    return paths


def run_generator(root: Path, generator: Path) -> int:
    """Run the official generator. Returns its exit code. Never writes by hand."""
    gen = generator if generator.is_absolute() else root / generator
    proc = run([sys.executable, str(gen), "--root", str(root)], root)
    sys.stdout.write(proc.stdout)
    sys.stderr.write(proc.stderr)
    return proc.returncode


def stamp(root: Path, generator: Path, dry_run: bool = False) -> tuple[int, str]:
    """Regenerate and (unless dry_run) commit the receipt files.

    Returns (exit_code, machine token): NO-STAMP | STAMP-NEEDED |
    STAMP-COMMITTED | ABORT-<reason>.
    """
    if not looks_like_repo(root):
        return 2, f"ABORT-NOT-A-REPO: {root}"
    if not worktree_is_clean(root):
        # SN-0327: a regen on a dirty worktree enumerates the committed past
        # and certifies it with a vacuous green. Refuse.
        return 2, "ABORT-DIRTY-WORKTREE"
    if not generator.is_absolute():
        generator = root / generator
    if not generator.is_file():
        return 2, f"ABORT-NO-GENERATOR: {generator}"

    gen_rc = run_generator(root, generator)
    if gen_rc != 0:
        # Fail closed: never commit a partial/failed regen.
        return 2, f"ABORT-GENERATOR-FAILED rc={gen_rc}"

    changed = changed_paths(root)
    unexpected = [p for p in changed if p not in RECEIPT_PATHS]
    if unexpected:
        return 2, f"ABORT-UNEXPECTED-FILES: {unexpected}"
    if not changed:
        return 0, "NO-STAMP"
    if dry_run:
        # Leave no trace: the worktree was verified clean on entry, so every
        # change present was made by the generator during this run. Restore
        # tracked files, remove untracked ones.
        for p in changed:
            target = root / p
            if run(["git", "ls-files", "--error-unmatch", p], root).returncode == 0:
                run(["git", "checkout", "--", p], root)
            else:
                target.unlink(missing_ok=True)
        return 0, f"STAMP-NEEDED: {sorted(changed)}"

    stage = run(["git", "add", "--"] + sorted(changed), root)
    if stage.returncode != 0:
        return 2, f"ABORT-STAGE-FAILED: {stage.stderr.strip()}"
    # Re-verify the stage set: only receipts may be committed.
    staged = run(["git", "diff", "--cached", "--name-only"], root).stdout.split()
    if sorted(staged) != sorted(changed):
        run(["git", "reset", "-q"], root)
        return 2, "ABORT-STAGE-MISMATCH"
    commit = run(["git", "commit", "-q", "-m", STAMP_COMMIT_MESSAGE], root)
    if commit.returncode != 0:
        run(["git", "reset", "-q"], root)
        return 2, f"ABORT-COMMIT-FAILED: {commit.stderr.strip()}"
    committed_files = run(
        ["git", "show", "--name-only", "--pretty=format:", "HEAD"], root
    ).stdout.split()
    if {p for p in committed_files if p} != set(changed):
        return 2, "ABORT-COMMIT-CONTENT-MISMATCH"
    return 0, f"STAMP-COMMITTED: {sorted(changed)}"


def push_head(root: Path, ref: str, remote: str = "origin") -> int:
    """Push local HEAD to <remote>/<ref>. Retry once after rebase. 0 ok, 3 failed."""
    first = run(["git", "push", remote, f"HEAD:{ref}"], root)
    if first.returncode == 0:
        return 0
    sys.stderr.write(f"auto-stamp: first push failed, rebasing once:\n{first.stderr}\n")
    rb = run(["git", "pull", "--rebase", remote, ref], root)
    if rb.returncode != 0:
        run(["git", "rebase", "--abort"], root)
        return 3
    second = run(["git", "push", remote, f"HEAD:{ref}"], root)
    return 0 if second.returncode == 0 else 3


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".", help="repo root (default: cwd)")
    ap.add_argument(
        "--generator",
        default="tools/regenerate_brain_index.py",
        help="generator script (default: the official one, relative to --root)",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="detect only: print STAMP-NEEDED/NO-STAMP, commit nothing",
    )
    ap.add_argument(
        "--push-to",
        default=None,
        metavar="REF",
        help="after committing, push HEAD to origin/<REF> (retry once after rebase)",
    )
    ap.add_argument(
        "--remote", default="origin", help="git remote for --push-to (default: origin)"
    )
    args = ap.parse_args(argv)

    root = Path(args.root).resolve()
    rc, token = stamp(root, Path(args.generator), dry_run=args.dry_run)
    print(token)
    if rc != 0 or args.push_to is None or args.dry_run:
        return rc
    prc = push_head(root, args.push_to, remote=args.remote)
    if prc != 0:
        print("ABORT-PUSH-FAILED (commit is local only)", file=sys.stderr)
        return 3
    print(f"PUSHED: HEAD -> {args.remote}/{args.push_to}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
