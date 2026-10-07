#!/usr/bin/env python3
"""Mechanical gate for git-data fallback merges (ACT node: no phantom work).

Background (2026-10-07): the GitHub pulls/merge endpoint 404'd, so three
merges (#1700/#1701/#1700->#1702) were rebuilt via the git-data API as
blobs -> tree -> commit -> PATCH ref. The trees were built as
`tree = head tree` while the PR heads predated earlier merges, silently
dropping 34 files from main (note_bridge.py, the compounding gate, BRAIN
index updates, tests). GitHub showed all three PRs as merged. The damage
was caught only by human inspection and repaired as 955b1996.

Law: never trust a git-data "merge" without diffing the result against a
REAL local merge. This tool is that diff, as machinery instead of memory.

Workflow (between commit creation and the ref PATCH):
    # 1. build the merge commit via the git-data API -> PROPOSED_COMMIT
    TREE=$(gh-api GET /repos/OWNER/REPO/git/commits/$PROPOSED_COMMIT | jq -r .tree.sha)
    # 2. verify BEFORE moving the ref:
    python3 tools/verify_gitdata_merge_tree.py <base_sha> <head_sha> $TREE
    #    exit 0 -> safe to PATCH the ref
    #    exit 1 -> MISMATCH: REFUSE to move the ref; the JSON names dropped/added files
    #    exit 2 -> INCONCLUSIVE or usage error: REFUSE (fail closed)

How it verifies: resolves the merge base, performs the merge for real in a
scratch worktree (`git merge --no-commit --no-ff` + `git write-tree`), and
compares the true tree SHA against the proposed tree SHA. A fast-forward
merge verifies naturally (true tree == head tree).

Stdlib only. Needs `git` on PATH and a repo containing the objects.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile

LAW_ID = "GITDATA-MERGE-TREE-VERIFY-V1"


def _git(repo, *args, check=True):
    proc = subprocess.run(
        ["git", "-C", repo, *args],
        capture_output=True, text=True, timeout=300,
    )
    if check and proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {proc.stderr.strip()[:400]}")
    return proc


def _obj_type(repo, sha):
    proc = _git(repo, "cat-file", "-t", sha, check=False)
    return proc.stdout.strip() if proc.returncode == 0 else None


def _tree_diff(repo, true_tree, proposed_tree):
    """Names of files present in the true merge tree but missing from the
    proposed tree (dropped), and vice versa (phantom-added)."""
    def names(a, b):
        proc = _git(repo, "diff-tree", "--no-commit-id", "--name-only", "-r", a, b)
        return sorted(n for n in proc.stdout.splitlines() if n)
    dropped = names(true_tree, proposed_tree)   # in true, not in proposed
    added = names(proposed_tree, true_tree)     # in proposed, not in true
    return dropped, added


def verify(base_sha, head_sha, proposed_tree_sha, repo):
    """Returns a verdict dict. Never raises on bad input: garbage fails
    closed as INCONCLUSIVE, never as MATCH."""
    for label, sha, want in (
        ("base_sha", base_sha, "commit"),
        ("head_sha", head_sha, "commit"),
        ("proposed_tree_sha", proposed_tree_sha, "tree"),
    ):
        got = _obj_type(repo, sha)
        if got != want:
            return {
                "law": LAW_ID,
                "verdict": "INCONCLUSIVE",
                "reason": f"{label} '{sha}' is {got or 'missing'}, expected {want} — refusing to bless",
            }

    merge_base = _git(repo, "merge-base", base_sha, head_sha).stdout.strip()

    scratch = tempfile.mkdtemp(prefix="gitdata-merge-verify-")
    try:
        _git(repo, "worktree", "add", "--detach", scratch, base_sha)
        # Explicit flags: no fast-forward games from repo config, no commit.
        merge = _git(
            scratch, "-c", "merge.ff=false", "merge",
            "--no-commit", "--no-ff", head_sha, check=False,
        )
        if merge.returncode != 0:
            return {
                "law": LAW_ID,
                "verdict": "INCONCLUSIVE",
                "reason": (
                    "the pair does not merge cleanly locally "
                    f"({merge.stderr.strip()[:200]}) — a git-data 'merge' of a "
                    "conflicted pair cannot be verified this way; refusing to bless"
                ),
            }
        true_tree = _git(scratch, "write-tree").stdout.strip()
    finally:
        _git(repo, "worktree", "remove", "--force", scratch, check=False)
        shutil.rmtree(scratch, ignore_errors=True)

    if true_tree == proposed_tree_sha:
        return {
            "law": LAW_ID,
            "verdict": "MATCH",
            "base_sha": base_sha,
            "head_sha": head_sha,
            "merge_base": merge_base,
            "true_tree": true_tree,
            "proposed_tree": proposed_tree_sha,
            "safe_to_move_ref": True,
        }

    dropped, added = _tree_diff(repo, true_tree, proposed_tree_sha)
    return {
        "law": LAW_ID,
        "verdict": "MISMATCH",
        "base_sha": base_sha,
        "head_sha": head_sha,
        "merge_base": merge_base,
        "true_tree": true_tree,
        "proposed_tree": proposed_tree_sha,
        "dropped_files": dropped,
        "phantom_files": added,
        "safe_to_move_ref": False,
        "reason": (
            f"proposed tree != true merge tree: "
            f"{len(dropped)} file(s) dropped, {len(added)} file(s) phantom-added. "
            "REFUSE to move the ref."
        ),
    }


def main(argv):
    if len(argv) not in (4, 6) or (len(argv) == 6 and argv[4] != "--repo"):
        print(
            "usage: python3 tools/verify_gitdata_merge_tree.py "
            "<base_sha> <head_sha> <proposed_tree_sha> [--repo PATH]",
            file=sys.stderr,
        )
        return 2
    base_sha, head_sha, proposed_tree_sha = argv[1], argv[2], argv[3]
    repo = argv[5] if len(argv) == 6 else os.getcwd()
    verdict = verify(base_sha, head_sha, proposed_tree_sha, repo)
    print(json.dumps(verdict, indent=2))
    return {"MATCH": 0, "MISMATCH": 1, "INCONCLUSIVE": 2}[verdict["verdict"]]


if __name__ == "__main__":
    sys.exit(main(sys.argv))
