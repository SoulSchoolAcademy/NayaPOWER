#!/usr/bin/env python3
"""Advance an existing remote branch ref via the Git Data API (PAT).

Usage: push_ref.py <worktree> <branch> <expected-parent-H>
Steps: verify live head == H (SN-0493) -> POST novel blobs -> POST tree
(base_tree=H tree, verify == local tree) -> POST commit(parents=[H],
verify) -> PATCH ref -> verify live ref. Fails closed at every step.
"""
import base64, json, os, subprocess, sys, tempfile

# t0796 (lane 1, Verity) identity repair: seat-parameterized authorship,
# fail-closed when NAYA_SEAT_NAME/NAYA_SEAT_EMAIL are unset.
sys.path.insert(0, "/home/hatch/workspace/goals/bring-naya-to-life/hidden_files/bin")
from seat_identity import seat_identity

GH = os.path.expanduser("~/workspace/skills/github/bin/gh-api")
REPO = "SoulSchoolAcademy/NayaPOWER"


def git(wt, *args):
    p = subprocess.run(["git", "-C", wt, *args], capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {p.stderr.strip()[:300]}")
    return p.stdout


def api(method, path, body=None):
    if body is None:
        cmd = [GH, method, path]
    else:
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(body, f)
            tmp = f.name
        cmd = [GH, method, path, "@" + tmp]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if "tmp" in dir():
        os.unlink(tmp)
    if p.returncode != 0:
        raise RuntimeError(
            f"gh-api {method} {path} failed: {p.stderr.strip()[:500] or p.stdout.strip()[:500]}")
    return json.loads(p.stdout)


def main():
    wt, branch, H = sys.argv[1], sys.argv[2], sys.argv[3]
    refpath = f"/repos/{REPO}/git/ref/heads/{branch.replace('/', '%2F')}"
    live_H = api("GET", refpath)["object"]["sha"]
    if live_H != H:
        raise RuntimeError(
            f"BRANCH HEAD MOVED: expected {H[:8]}, live {live_H[:8]} — aborting")

    M = git(wt, "rev-parse", "HEAD").strip()
    TM = git(wt, "rev-parse", "HEAD^{tree}").strip()
    # NOTE: local HEAD need not be parented on H by SHA — API-created
    # commits diverge in SHA from local ones. The change set is computed
    # as diff(H, M) and the tree equality check (TP == TM) is the real
    # guarantee that nothing is dropped or added.
    msg = git(wt, "log", "-1", "--format=%B", M).strip()
    H_tree = git(wt, "rev-parse", f"{H}^{{tree}}").strip()

    out = git(wt, "diff-tree", "-r", "--no-commit-id", H, M)
    changes, new_blobs = [], {}
    for line in out.splitlines():
        if not line.startswith(":"):
            continue
        meta, path = line[1:].split("\t", 1)
        oldmode, newmode, oldsha, newsha, status = meta.split()
        if status == "D":
            changes.append({"path": path, "mode": "0", "type": "blob", "sha": None})
        else:
            changes.append({"path": path, "mode": newmode, "type": "blob", "sha": newsha})
            new_blobs[path] = newsha
    print(f"changes: {len(changes)} files; local tree {TM[:8]}")

    remote_blobs = set()
    for line in git(wt, "ls-tree", "-r", H).splitlines():
        parts = line.split()
        if len(parts) >= 3 and parts[1] == "blob":
            remote_blobs.add(parts[2])
    novel = {p: s for p, s in new_blobs.items() if s not in remote_blobs}
    print(f"novel blobs to POST: {len(novel)} of {len(new_blobs)}")

    for path, sha in novel.items():
        raw = subprocess.run(["git", "-C", wt, "cat-file", "blob", sha],
                             capture_output=True).stdout
        r = api("POST", f"/repos/{REPO}/git/blobs",
                {"content": base64.b64encode(raw).decode(), "encoding": "base64"})
        assert r["sha"] == sha, f"blob sha mismatch for {path}"
    print("blobs posted and SHA-verified")

    TP = api("POST", f"/repos/{REPO}/git/trees",
             {"base_tree": H_tree, "tree": changes})["sha"]
    if TP != TM:
        raise RuntimeError(f"TREE MISMATCH: proposed {TP[:8]} != local {TM[:8]} — REFUSING")
    print(f"tree verified: {TP[:8]} == local tree")

    ident = seat_identity()  # t0796: parameterized by executing seat
    c = api("POST", f"/repos/{REPO}/git/commits",
            {"message": msg, "tree": TP, "parents": [H],
             "author": ident, "committer": ident})
    C = c["sha"]
    assert c["tree"]["sha"] == TM, "commit tree drift"
    got_parents = [p["sha"] for p in c["parents"]]
    assert got_parents == [H], f"commit parents drift: {got_parents}"
    print(f"commit {C[:8]} created (tree+parents verified)")

    if api("GET", refpath)["object"]["sha"] != H:
        raise RuntimeError("head moved mid-push — aborting, nothing patched")
    # NOTE: single-ref GET is /git/ref/..., but update is /git/refs/...
    api("PATCH", refpath.replace("/git/ref/", "/git/refs/"), {"sha": C})
    assert api("GET", refpath)["object"]["sha"] == C, "ref patch not visible"
    print(f"OK: {branch} now at {C[:8]}")


main()
