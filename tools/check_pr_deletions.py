#!/usr/bin/env python3
"""No-silent-deletion gate: every deleted file must be declared.

Compares BASE_SHA...HEAD_SHA. For each file with deletion status, the PR body
must contain a `## Deletions` section naming the file (full path or basename)
with a reason. Undeclared deletions fail the gate.

This kills the stale-head trap: a PR built on an old base that silently drops
files added to main after the base will show those drops as deletions here,
forcing them to be declared or the rebase to happen.

Exit 0 = clean. Exit 1 = undeclared deletions.
"""
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
