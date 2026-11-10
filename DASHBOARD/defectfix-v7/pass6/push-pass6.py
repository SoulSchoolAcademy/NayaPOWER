#!/usr/bin/env python3
"""Push pass-6 files to GitHub via the git-data API, all in memory.

Usage:
  push-pass6.py <base-ref> <message> <localpath:repopath> [<localpath:repopath> ...]
  base-ref: e.g. heads/main (commit 1) or heads/dashboard/pass6-orb-numbers-20261110 (commit 2)
Creates blobs -> tree (on the base commit's tree) -> commit -> creates or
fast-forwards branch dashboard/pass6-orb-numbers-20261110. Prints the commit
SHA and verifies the branch head. Never stages payloads to disk; never touches
the token cache (reuses gh-direct.py's in-memory mint).
"""
import base64, importlib.util, json, sys, urllib.request, urllib.error

SPEC = importlib.util.spec_from_file_location("ghd", "/home/hatch/workspace/team-nitro/gh-direct.py")
GHD = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(GHD)
REPO = "SoulSchoolAcademy/NayaPOWER"
BRANCH = "dashboard/pass6-orb-numbers-20261110"
TOKEN = GHD.get_token()

def call(method, path, body=None):
    req = urllib.request.Request(
        GHD.BASE + path, data=json.dumps(body).encode() if body is not None else None,
        method=method, headers={"Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28", "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json", "User-Agent": "muse-github-skill/1.0"})
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode("utf-8", "replace"))

def main():
    base_ref, message, specs = sys.argv[1], sys.argv[2], sys.argv[3:]
    st, ref = call("GET", f"/repos/{REPO}/git/ref/{base_ref}")
    assert st == 200, f"base ref {base_ref}: {st} {ref}"
    base_sha = ref["object"]["sha"]
    st, commit = call("GET", f"/repos/{REPO}/git/commits/{base_sha}")
    assert st == 200, f"base commit: {st} {commit}"
    base_tree = commit["tree"]["sha"]
    print(f"base {base_ref} = {base_sha} tree {base_tree}")
    entries = []
    for spec in specs:
        local, repo = spec.split(":", 1)
        raw = open(local, "rb").read()
        st, blob = call("POST", f"/repos/{REPO}/git/blobs",
                        {"content": base64.b64encode(raw).decode(), "encoding": "base64"})
        assert st == 201, f"blob {local}: {st} {blob}"
        print(f"blob {repo}: {blob['sha']} ({len(raw)} B)")
        entries.append({"path": repo, "mode": "100644", "type": "blob", "sha": blob["sha"]})
    st, tree = call("POST", f"/repos/{REPO}/git/trees", {"base_tree": base_tree, "tree": entries})
    assert st == 201, f"tree: {st} {tree}"
    st, new_commit = call("POST", f"/repos/{REPO}/git/commits",
                          {"message": message, "tree": tree["sha"], "parents": [base_sha]})
    assert st == 201, f"commit: {st} {new_commit}"
    print(f"commit: {new_commit['sha']}")
    st, existing = call("GET", f"/repos/{REPO}/git/ref/heads/{BRANCH}")
    if st == 200:
        st, upd = call("PATCH", f"/repos/{REPO}/git/refs/heads/{BRANCH}", {"sha": new_commit["sha"]})
        assert st == 200, f"ref update: {st} {upd}"
        print(f"branch {BRANCH} fast-forwarded to {new_commit['sha']}")
    elif st == 404:
        st, created = call("POST", f"/repos/{REPO}/git/refs",
                           {"ref": f"refs/heads/{BRANCH}", "sha": new_commit["sha"]})
        assert st == 201, f"ref create: {st} {created}"
        print(f"branch {BRANCH} created at {new_commit['sha']}")
    else:
        raise SystemExit(f"ref check: {st} {existing}")
    st, head = call("GET", f"/repos/{REPO}/git/ref/heads/{BRANCH}")
    assert st == 200 and head["object"]["sha"] == new_commit["sha"], f"head verify: {st} {head}"
    print(f"VERIFIED head {BRANCH} = {new_commit['sha']}")

main()
