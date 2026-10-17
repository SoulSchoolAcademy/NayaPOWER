#!/usr/bin/env python3
"""Protected-path push check: the human gate's tripwire on the direct-merge path.

Standing law (tools/auto_merge_gate.py, PROTECTED_PATH_PREFIXES): changes under
protected paths are NEVER merged without a proven supreme-law exception
(ratified_by == "Shawn Vibert" + ratification evidence comment id + scope).

The auto-merge gate only sees merges that go through it. A direct merge to main
(e.g. PR #2152, 2026-10-10: three .github/workflows/ files, no exception proof,
circular self-authored override) bypasses it entirely. This script closes that
hole: on every push to main it inspects the pushed commits, and any push that
touches a protected path WITHOUT the exception marker on any commit in the
pushed range is flagged to the LAW feed (#1718). The marker names its evidence
comment id, so a false claim of ratification is itself auditable.

Report-only by design: the push already landed, so a violation must NEVER fail
the check run -- a red check on main would freeze the merge queue per the
red-main discipline. Use --post in CI: violations go to the board, exit stays 0.
Without --post (tests, CLI): exit 1 on violation, 0 when clean, 2 on error.

The protected-path list is duplicated here deliberately; the sync is enforced
mechanically by tests/test_protected_path_push_check.py::test_prefixes_in_sync
(one source of truth would couple this tripwire's import to the gate module).

Stdlib only.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request

# Canonical source: tools/auto_merge_gate.py::PROTECTED_PATH_PREFIXES.
# Kept in sync by test_prefixes_in_sync_with_gate. Do not edit one without the other.
PROTECTED_PATH_PREFIXES = (
    ".github/workflows/",
    "CONSTITUTION/",
    "BRAIN/01-GOVERNANCE/",
    "GOVERNANCE/",
    "NAYA-ACTIVATION/",
)

# Exception marker: must appear in the merge/push commit message.
#   Supreme-law-exception: ratified_by=Shawn Vibert evidence=<comment_id> scope=<20+ chars>
EXCEPTION_RE = re.compile(
    r"Supreme-law-exception:.*ratified_by=Shawn Vibert.*evidence=(\d+).*scope=(.{20,})",
    re.DOTALL,
)

LAW_FEED_ISSUE = 1718
MARKER = "<!-- protected-path-watch -->"
API = "https://api.github.com"
ZERO_SHA = "0" * 40


def sh(args, cwd, check=True):
    p = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=60)
    if check and p.returncode != 0:
        raise RuntimeError(f"{' '.join(args)} failed: {p.stderr.strip()[:200]}")
    return p


def commit_shas(base, head, repo_dir):
    """Shas in (base, head], oldest first. Handles zero-sha base (new branch)."""
    if base == ZERO_SHA:
        base = sh(["git", "rev-list", "--max-parents=0", head], repo_dir).stdout.split()[0]
        rng = base + ".." + head
    else:
        rng = base + ".." + head
    out = sh(["git", "rev-list", "--reverse", rng], repo_dir).stdout.strip()
    return out.split() if out else []


def files_changed(sha, repo_dir):
    """Files the commit introduced to its first-parent line.

    For merges this is the diff vs the first parent (what the merge brought
    into main); the merge's own branch commits are walked separately in the
    pushed range, so nothing is missed and main-side drift is not misattributed.
    """
    parents = sh(["git", "rev-list", "--parents", "-n", "1", sha], repo_dir).stdout.split()[1:]
    if not parents:  # root commit: everything it adds
        out = sh(["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "--root", sha],
                 repo_dir).stdout
    else:
        out = sh(["git", "diff", "--name-only", parents[0], sha], repo_dir).stdout
    return sorted({l.strip() for l in out.splitlines() if l.strip()})


def commit_message(sha, repo_dir):
    return sh(["git", "log", "--format=%B", "-n", "1", sha], repo_dir).stdout


def protected_hits(files):
    return sorted({p for f in files for p in PROTECTED_PATH_PREFIXES if f.startswith(p)})


def check(base, head, repo_dir):
    """Return list of violations: commits touching protected paths w/o exception.

    Exception semantics are range-level: if ANY commit in the pushed range
    carries a valid supreme-law exception marker, the push is excepted (the
    marker names its evidence comment id, so the claim stays auditable).
    Otherwise every commit touching a protected path is a violation.
    """
    shas = commit_shas(base, head, repo_dir)
    excepted_by = None
    for sha in shas:
        if EXCEPTION_RE.search(commit_message(sha, repo_dir)):
            excepted_by = sha
            break
    violations = []
    if excepted_by:
        return violations, excepted_by
    for sha in shas:
        files = files_changed(sha, repo_dir)
        hits = protected_hits(files)
        if not hits:
            continue
        msg = commit_message(sha, repo_dir)
        touched = [f for f in files if any(f.startswith(p) for p in hits)]
        subject = msg.strip().splitlines()[0][:120] if msg.strip() else "(no message)"
        violations.append({"sha": sha, "subject": subject, "paths": hits, "files": touched})
    return violations, None


def rest(path, method="GET", data=None):
    token = os.environ.get("GH_TOKEN", "")
    if not token:
        raise RuntimeError("GH_TOKEN missing; cannot post flag")
    req = urllib.request.Request(
        API + path, method=method,
        data=json.dumps(data).encode() if data is not None else None,
        headers={"Authorization": f"Bearer {token}",
                 "Accept": "application/vnd.github+json",
                 "User-Agent": "naya-protected-path-watch/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def post_flag(violations, repo):
    owner, name = repo.split("/")
    lines = [MARKER, "## [PROTECTED-PATH-WATCH] Human-gate bypass detected on main",
             "",
             "The following pushed commit(s) touch protected paths",
             f"({', '.join(PROTECTED_PATH_PREFIXES)})",
             "without a `Supreme-law-exception` marker proving Shawn's ratification",
             "(see tools/auto_merge_gate.py: protected paths are never merged",
             "without ratified_by=Shawn Vibert + evidence comment id).",
             "This detector is report-only; the push already landed.", ""]
    for v in violations:
        lines.append(f"- `{v['sha'][:12]}` {v['subject']}")
        for f in v["files"][:10]:
            lines.append(f"  - `{f}`")
    lines += ["", "Owning lane: LAW driver. Expected: director ratify-or-restore decision."]
    body = "\n".join(lines)
    try:
        rest(f"/repos/{owner}/{name}/issues/{LAW_FEED_ISSUE}/comments",
             method="POST", data={"body": body})
        print(f"Flag posted to #{LAW_FEED_ISSUE}.")
    except Exception as e:
        print(f"Could not post flag ({e}).")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-ref", required=True)
    ap.add_argument("--head-ref", required=True)
    ap.add_argument("--post", action="store_true",
                    help="post violations to the LAW feed; always exit 0 (CI report-only)")
    ap.add_argument("--repo-dir", default=".")
    ap.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY", ""))
    args = ap.parse_args(argv)

    try:
        base = sh(["git", "rev-parse", args.base_ref], args.repo_dir).stdout.strip()
    except RuntimeError:
        base = ZERO_SHA  # unknown base (e.g. event.before on first push): check head only
    try:
        head = sh(["git", "rev-parse", args.head_ref], args.repo_dir).stdout.strip()
    except RuntimeError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    if base == head:
        print("clean: empty range")
        return 0

    try:
        violations, excepted_by = check(base, head, args.repo_dir)
    except RuntimeError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    if excepted_by:
        print(f"clean: excepted by {excepted_by[:12]} (supreme-law marker in range)")
        return 0
    if not violations:
        print("clean: no unexcepted protected-path changes")
        return 0
    for v in violations:
        print(f"VIOLATION {v['sha'][:12]} [{', '.join(v['paths'])}] {v['subject']}")
        for f in v["files"][:10]:
            print(f"    {f}")
    if args.post:
        if args.repo:
            post_flag(violations, args.repo)
        else:
            print("no --repo/GITHUB_REPOSITORY; skipping post")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
