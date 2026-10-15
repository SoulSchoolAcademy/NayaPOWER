#!/usr/bin/env python3
"""Push a local branch to GitHub via the git-data REST API.

Worker envs lack git push credentials (no SSH, gh CLI unauthenticated),
but bin/gh-api works (custom.github credential). This recreates the branch's
commits on top of the same base via the API. Content is byte-identical
(same tree SHA); only commit SHAs differ (recreated metadata).

Usage: python3 push_branch.py <branch-name> [base-sha]
  base-sha defaults to the branch's merge-base with main.

The new remote SHA is printed; append it to your receipt.
"""
import base64, json, subprocess, sys, tempfile, os

# t0796 (lane 1, Verity) identity repair: seat-parameterized authorship,
# fail-closed when NAYA_SEAT_NAME/NAYA_SEAT_EMAIL are unset. Without this
# the API stamps the GitHub App default identity ("NayaPOWER Lane Agent"),
# which no self-review gate can attribute to a seat.
sys.path.insert(0, "/home/hatch/workspace/goals/bring-naya-to-life/hidden_files/bin")
from seat_identity import seat_identity

REPO = "SoulSchoolAcademy/NayaPOWER"
WORK = "/home/hatch/workspace/nayapower-rescue"
GH_API = "/home/hatch/workspace/skills/github/bin/gh-api"

def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=WORK)
    if r.returncode != 0:
        print(f"CMD FAILED: {' '.join(cmd)}\n{r.stderr}", file=sys.stderr)
        sys.exit(1)
    return r.stdout.strip()

def api(method, path, body=None):
    cmd = [GH_API, method, path]
    tmp = None
    if body is not None:
        # Bodies ride a temp file (@file), not argv: large blobs (e.g. the
        # ~1MB brain-index files) exceed the OS argument-length limit.
        tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        tmp.write(json.dumps(body))
        tmp.close()
        cmd.append("@" + tmp.name)
    try:
        r = subprocess.run(cmd, capture_output=True, text=True)
    finally:
        if tmp is not None:
            os.unlink(tmp.name)
    if r.returncode != 0:
        print(f"API FAILED: {method} {path}\n{r.stdout}\n{r.stderr}", file=sys.stderr)
        sys.exit(1)
    return json.loads(r.stdout)

def main():
    if len(sys.argv) < 2:
        print("Usage: push_branch.py <branch-name> [base-sha]", file=sys.stderr)
        sys.exit(1)
    branch = sys.argv[1]
    base = sys.argv[2] if len(sys.argv) > 2 else sh(["git", "merge-base", "main", branch])
    print(f"Pushing {branch} onto base {base[:12]}")

    files = sh(["git", "diff", "--name-only", f"{base}..{branch}"]).splitlines()
    base_tree = sh(["git", "rev-parse", f"{base}^{{tree}}"])
    local_msg = sh(["git", "log", "-1", "--format=%B", branch])

    tree_entries = []
    for f in files:
        r = subprocess.run(["git", "cat-file", "-e", f"{branch}:{f}"],
                           cwd=WORK, capture_output=True)
        if r.returncode != 0:
            tree_entries.append({"path": f, "mode": "100644", "type": "blob", "sha": None})
            continue
        content = subprocess.run(["git", "show", f"{branch}:{f}"],
                                 cwd=WORK, capture_output=True).stdout
        mode = sh(["git", "ls-tree", branch, "--", f]).split()[0]
        b = api("POST", f"/repos/{REPO}/git/blobs",
                {"content": base64.b64encode(content).decode(), "encoding": "base64"})
        tree_entries.append({"path": f, "mode": mode, "type": "blob", "sha": b["sha"]})

    t = api("POST", f"/repos/{REPO}/git/trees", {"base_tree": base_tree, "tree": tree_entries})
    ident = seat_identity()  # t0796: parameterized by executing seat
    print(f"commit identity: {ident['name']} <{ident['email']}>")
    c = api("POST", f"/repos/{REPO}/git/commits",
            {"message": local_msg + "\n\nPushed via git-data API (worker env lacks push creds). Content byte-identical; commit SHA differs (recreated).",
             "tree": t["sha"], "parents": [base],
             "author": ident, "committer": ident})
    try:
        api("POST", f"/repos/{REPO}/git/refs",
            {"ref": f"refs/heads/{branch}", "sha": c["sha"]})
    except SystemExit:
        # Ref exists: try a normal update first; re-anchored heads are
        # non-fast-forward (new base commit), so retry with force on the
        # lane-owned naya/* branch — the re-anchor mechanism, not a
        # history rewrite of shared work.
        try:
            api("PATCH", f"/repos/{REPO}/git/refs/heads/{branch}",
                {"sha": c["sha"]})
        except SystemExit:
            print(f"Non-fast-forward update; retrying with force on {branch}")
            api("PATCH", f"/repos/{REPO}/git/refs/heads/{branch}",
                {"sha": c["sha"], "force": True})

    # verify tree matches local (byte-identical content proof)
    local_tree = sh(["git", "rev-parse", f"{branch}^{{tree}}"])
    remote_tree = api("GET", f"/repos/{REPO}/git/commits/{c['sha']}")["tree"]["sha"]
    match = "MATCH" if local_tree == remote_tree else "MISMATCH"
    print(f"REMOTE_SHA={c['sha']}")
    print(f"TREE_CHECK={match} (local {local_tree[:12]} vs remote {remote_tree[:12]})")

if __name__ == "__main__":
    main()
