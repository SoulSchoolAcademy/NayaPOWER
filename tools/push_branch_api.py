#!/usr/bin/env python3
"""Push a local branch to origin via the GitHub Git Database API (quiet path).

Usage: push_branch_api.py <repo-root> <branch> <base-sha>
Creates/updates refs/heads/<branch> with a commit whose parent is <base-sha>
and whose tree = base tree + the local branch's file changes.

Only the surrogate credential from authdc leaves the machine (via gh-api),
same quiet path as the earlier ground-truth ref resolution. No raw tokens.

Exit codes: 0 = pushed; 1 = no changes; 2 = gh-api failure; 3 = REFUSED
(argv payload over the 1 MiB limit — nothing pushed, redirect printed).

ARGV PAYLOAD GUARD (added 2026-10-12, INFRA/Naya Lambda):
This script passes the tree-creation body through the gh-api argv. Multi-MB
payloads die there ("Arg List Too Long" / HTTP 500 — seen live when a 6MB
BRAIN/REAL-TREE.json blob killed a brain-index regen push). The guard below
measures the exact argv payload BEFORE any API call and REFUSES with the
exact redirect when it exceeds 1 MiB, so the failure is impossible instead
of merely documented.
"""
import json
import subprocess
import sys
from pathlib import Path

REPO = "SoulSchoolAcademy/NayaPOWER"
GH_API = str(Path.home() / "workspace" / "naya" / "bin" / "gh-api")

# Maximum bytes allowed to travel through the gh-api argv path. Payloads
# above this die with "Arg List Too Long" or an HTTP 500 from gh-api
# (proven live on a ~6MB blob, 2026-10-12). 1 MiB is the conservative
# ceiling: well under the OS ARG_MAX (~2MB) and the gh-api 500 threshold.
ARGV_PAYLOAD_LIMIT_BYTES = 1 * 1024 * 1024

# Where the operator's in-process fallback lives. The refuse message names
# this exact path so the operator can copy-paste the redirect.
PRESERVE_SCRIPT = str(Path.home() / "workspace" / "naya" / "bin" / "push_branch_preserve.py")


class PayloadTooLargeError(Exception):
    """Raised when the argv-bound payload exceeds ARGV_PAYLOAD_LIMIT_BYTES.

    Carries the exact redirect: the equivalent push_branch_preserve.py
    invocation with the operator's own arguments interpolated, ready to
    copy-paste. Nothing is pushed when this is raised.
    """

    def __init__(self, size_bytes, root, branch, base_sha, what="tree"):
        self.size_bytes = size_bytes
        self.root = str(root)
        self.branch = branch
        self.base_sha = base_sha
        mib = size_bytes / (1024 * 1024)
        limit_mib = ARGV_PAYLOAD_LIMIT_BYTES / (1024 * 1024)
        super().__init__(
            f"push_branch_api.py REFUSED: {what} argv payload is {mib:.2f} MiB, "
            f"over the {limit_mib:.2f} MiB limit.\n"
            f"The gh-api argv path cannot carry multi-MB payloads: it dies "
            f"with \"Arg List Too Long\" or an HTTP 500 "
            f"(seen live on a ~6MB blob, 2026-10-12).\n"
            f"Nothing was pushed. No remote state changed.\n"
            f"Push this branch with the in-process path instead "
            f"(takes the same three arguments):\n"
            f"  python3 {PRESERVE_SCRIPT} {self.root} {self.branch} {self.base_sha}"
        )


def measure_argv_payload(tree_body):
    """Bytes that would travel via the gh-api argv for the tree POST.

    This is the exact JSON string the gh() helper appends to the gh-api
    command line, so its length is the true argv cost.
    """
    return len(json.dumps(tree_body).encode("utf-8"))


def guard_argv_payload(body, root, branch, base_sha, what="tree"):
    """Refuse-with-redirect if an argv-bound POST body exceeds the limit.

    Returns the measured payload size in bytes when the payload fits
    (the normal path proceeds). Raises PayloadTooLargeError otherwise.
    Call this BEFORE every gh-api call whose body travels via argv.
    """
    size = measure_argv_payload(body)
    if size > ARGV_PAYLOAD_LIMIT_BYTES:
        raise PayloadTooLargeError(size, root, branch, base_sha, what=what)
    return size


def gh(method, path, body=None):
    cmd = [GH_API, method, f"/repos/{REPO}{path}"]
    if body is not None:
        cmd.append(json.dumps(body))
    out = subprocess.run(cmd, capture_output=True, text=True)
    if out.returncode != 0:
        print(f"gh-api {method} {path} FAILED:\n{out.stdout}\n{out.stderr}", file=sys.stderr)
        sys.exit(2)
    return json.loads(out.stdout)


def main():
    root = Path(sys.argv[1]).resolve()
    branch = sys.argv[2]
    base_sha = sys.argv[3]

    def git(*args):
        r = subprocess.run(["git", *args], capture_output=True, text=True, cwd=root)
        r.check_returncode()
        return r.stdout.strip()

    head_sha = git("rev-parse", branch)
    local_msg = git("log", "-1", "--format=%B", head_sha)
    author_name = git("log", "-1", "--format=%an", head_sha)
    author_email = git("log", "-1", "--format=%ae", head_sha)
    author_date = git("log", "-1", "--format=%aI", head_sha)
    committer_name = git("log", "-1", "--format=%cn", head_sha)
    committer_email = git("log", "-1", "--format=%ce", head_sha)
    base_tree = git("rev-parse", base_sha + "^{tree}")

    # Files changed between base and head
    changed = git("diff", "--name-only", "-z", base_sha, head_sha).split("\0")
    changed = [c for c in changed if c]
    if not changed:
        print("no changes to push", file=sys.stderr)
        sys.exit(1)

    entries = []
    for path in changed:
        mode = git("ls-tree", head_sha, path).split()[0]
        content = (root / path).read_text(encoding="utf-8")
        entries.append({"path": path, "mode": mode, "type": "blob", "content": content})

    tree_body = {"base_tree": base_tree, "tree": entries}

    # THE GUARD: measure the exact argv payload BEFORE any API call.
    # Refuse with the exact redirect instead of dying mid-push.
    try:
        payload_bytes = guard_argv_payload(tree_body, root, branch, base_sha)
    except PayloadTooLargeError as e:
        print(e, file=sys.stderr)
        sys.exit(3)
    print(f"argv payload: {payload_bytes} bytes (limit {ARGV_PAYLOAD_LIMIT_BYTES})")

    tree = gh("POST", "/git/trees", tree_body)
    print("tree:", tree["sha"])

    commit_body = {
        "message": local_msg,
        "tree": tree["sha"],
        "parents": [base_sha],
        "author": {"name": author_name, "email": author_email, "date": author_date},
        "committer": {"name": committer_name, "email": committer_email},
    }

    # The commit body also travels via argv: guard it too (a pathological
    # multi-MB commit message must refuse just like a multi-MB tree).
    try:
        guard_argv_payload(commit_body, root, branch, base_sha, what="commit")
    except PayloadTooLargeError as e:
        print(e, file=sys.stderr)
        sys.exit(3)

    commit = gh("POST", "/git/commits", commit_body)
    print("commit:", commit["sha"])

    # Create or update the ref. Try create first; if the branch already
    # exists on origin, update it instead.
    create = subprocess.run(
        [GH_API, "POST", f"/repos/{REPO}/git/refs",
         json.dumps({"ref": f"refs/heads/{branch}", "sha": commit["sha"]})],
        capture_output=True, text=True)
    if create.returncode == 0:
        print("ref created:", branch)
    else:
        upd = subprocess.run(
            [GH_API, "PATCH", f"/repos/{REPO}/git/refs/heads/{branch}",
             json.dumps({"sha": commit["sha"], "force": True})],
            capture_output=True, text=True)
        # force:true is used only here: this script pushes feature branches
        # that were rebased onto the current tip; it never touches main.
        if upd.returncode != 0:
            print(f"ref update FAILED:\n{create.stdout}\n{create.stderr}\n{upd.stdout}\n{upd.stderr}",
                  file=sys.stderr)
            sys.exit(2)
        print("ref updated:", branch)

    # Align local branch to the new remote commit
    git("update-ref", f"refs/heads/{branch}", commit["sha"])
    print("local branch aligned to", commit["sha"][:8])


if __name__ == "__main__":
    main()
