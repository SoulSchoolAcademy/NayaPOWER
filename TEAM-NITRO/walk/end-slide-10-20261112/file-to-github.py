#!/usr/bin/env python3
"""File the Walk END SLIDE 10/10 round to branch walk/end-slide-10-20261112
(repo SoulSchoolAcademy/NayaPOWER), from S2 tip dbc2f7be.

Git-data flow, all in memory (no multi-MB staging to disk): create the branch
ref, POST one blob per file, one tree on the S2 base tree, one commit, update
the ref, then verify every blob by read-back (decoded sha256 == local file).

Usage:
  python3 file-to-github.py            # commit 1: work + probes + screenshots
  python3 file-to-github.py record     # commit 2: RECORD + SCORECARD only
"""
import base64
import hashlib
import json
import sys
import urllib.request
import urllib.error

sys.path.insert(0, "/home/hatch/workspace/team-nitro")
import importlib.util
spec = importlib.util.spec_from_file_location(
    "ghd", "/home/hatch/workspace/team-nitro/gh-direct.py")
ghd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ghd)

REPO = "SoulSchoolAcademy/NayaPOWER"
BASE = "https://api.github.com"
S2_TIP = "dbc2f7bea435cdffc3a4c052b70df02c79375f42"
S2_TREE = "5ed4985fb71158f8f2910be408f96c5268241ffd"
BRANCH = "walk/end-slide-10-20261112"
S2DIR = "/home/hatch/workspace/team-nitro/walk-s2-box-pages-20261112"
ROUND = "/home/hatch/workspace/team-nitro/walk/end-slide-10-20261112"
PREFIX_S2 = "TEAM-NITRO/walk-s2-box-pages-20261112/"
PREFIX_ROUND = "TEAM-NITRO/walk/end-slide-10-20261112/"

COMMIT1 = [
    # (local path, repo path)
    (f"{S2DIR}/walk-beginning-fixed.html", PREFIX_S2 + "walk-beginning-fixed.html"),
    (f"{S2DIR}/identity-fixed.html", PREFIX_S2 + "identity-fixed.html"),
    (f"{S2DIR}/welcome-staged.html", PREFIX_S2 + "welcome-staged.html"),
    (f"{S2DIR}/build-beginning-staging-worker.py", PREFIX_S2 + "build-beginning-staging-worker.py"),
    (f"{S2DIR}/walk-beginning-staging-worker.js", PREFIX_S2 + "walk-beginning-staging-worker.js"),
    (f"{ROUND}/bug-verify-v3.py", PREFIX_ROUND + "bug-verify-v3.py"),
    (f"{ROUND}/bug-verify-v4.py", PREFIX_ROUND + "bug-verify-v4.py"),
    (f"{ROUND}/bug-verify-results.json", PREFIX_ROUND + "bug-verify-results.json"),
    (f"{ROUND}/bug-verify-results-v4.json", PREFIX_ROUND + "bug-verify-results-v4.json"),
    (f"{ROUND}/end-probe-v2.py", PREFIX_ROUND + "end-probe-v2.py"),
    (f"{ROUND}/end-results-v2.json", PREFIX_ROUND + "end-results-v2.json"),
    (f"{ROUND}/bug-repro.py", PREFIX_ROUND + "bug-repro.py"),
    (f"{ROUND}/bug-repro-results.json", PREFIX_ROUND + "bug-repro-results.json"),
    (f"{ROUND}/transform-probes-v2v3.py", PREFIX_ROUND + "transform-probes-v2v3.py"),
    (f"{ROUND}/transform-v3v4.py", PREFIX_ROUND + "transform-v3v4.py"),
    (f"{ROUND}/worker-meta.json", PREFIX_ROUND + "worker-meta.json"),
]
SHOTS = ["bug-verify-v4-healed.png", "bug-verify-v4-cert-mike.png",
         "bug-verify-v4-mike-end.png", "bug-verify-v4-others.png",
         "bug-verify-v4-fresh-end.png",
         "end-slide-1440.png", "end-slide-390.png", "end-slide-360.png",
         "end-cards-1440.png", "end-cards-390.png", "end-cards-360.png",
         "end-deal-1440.png", "end-deal-390.png", "end-deal-360.png",
         "end-names-1440.png", "end-names-390.png"]
for s in SHOTS:
    COMMIT1.append((f"{ROUND}/{s}", PREFIX_ROUND + s))

COMMIT2 = [
    (f"{ROUND}/END-SLIDE-RECORD-20261112.md", PREFIX_ROUND + "END-SLIDE-RECORD-20261112.md"),
    (f"{ROUND}/END-SLIDE-SCORECARD-20261112.md", PREFIX_ROUND + "END-SLIDE-SCORECARD-20261112.md"),
    (f"{ROUND}/file-to-github.py", PREFIX_ROUND + "file-to-github.py"),
]

TOKEN = ghd.get_token()


def call(method, path, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        BASE + path, data=data, method=method,
        headers={"Accept": "application/vnd.github+json",
                 "X-GitHub-Api-Version": "2022-11-28",
                 "Authorization": f"Bearer {TOKEN}",
                 "Content-Type": "application/json",
                 "User-Agent": "muse-github-skill/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return resp.status, json.load(resp)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        print(f"HTTP {e.code} {method} {path}\n{body[:800]}")
        raise SystemExit(1)


def branch_head():
    st, b = call("GET", f"/repos/{REPO}/branches/{BRANCH}")
    return b["commit"]["sha"], b["commit"]["commit"]["tree"]["sha"]


def file_commit(files, message):
    head_sha, head_tree = branch_head()
    blobs = []
    for local, repo_path in files:
        raw = open(local, "rb").read()
        sha_local = hashlib.sha256(raw).hexdigest()
        st, b = call("POST", f"/repos/{REPO}/git/blobs",
                     {"content": base64.b64encode(raw).decode(), "encoding": "base64"})
        blob_sha = b["sha"]
        # verify by read-back
        st, rb = call("GET", f"/repos/{REPO}/git/blobs/{blob_sha}")
        back = base64.b64decode(rb["content"])
        ok = hashlib.sha256(back).hexdigest() == sha_local
        print(f"blob {repo_path} {len(raw)} B local {sha_local[:12]} blob {blob_sha[:12]} "
              f"read-back {'OK' if ok else 'MISMATCH'}")
        assert ok, f"read-back mismatch for {repo_path}"
        blobs.append((repo_path, blob_sha))
    tree_entries = [{"path": p, "mode": "100644", "type": "blob", "sha": s}
                    for p, s in blobs]
    st, t = call("POST", f"/repos/{REPO}/git/trees",
                 {"base_tree": head_tree, "tree": tree_entries})
    print(f"tree {t['sha']}")
    st, c = call("POST", f"/repos/{REPO}/git/commits",
                 {"message": message, "tree": t["sha"], "parents": [head_sha]})
    print(f"commit {c['sha']}")
    st, r = call("PATCH", f"/repos/{REPO}/git/refs/heads/{BRANCH}",
                 {"sha": c["sha"]})
    print(f"branch now at {c['sha'][:12]}")
    return c["sha"], blobs


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "work"
    if mode == "record":
        sha, blobs = file_commit(
            COMMIT2, "End slide 10/10: RECORD + SCORECARD (maker self-check x3, 9/10)")
    else:
        # create the branch first (from the S2 tip) if it does not exist
        try:
            call("GET", f"/repos/{REPO}/branches/{BRANCH}")
            print("branch already exists")
        except SystemExit:
            st, b = call("POST", f"/repos/{REPO}/git/refs",
                         {"ref": f"refs/heads/{BRANCH}", "sha": S2_TIP})
            print(f"branch created at {S2_TIP[:12]}")
        sha, blobs = file_commit(
            COMMIT1, "End slide 10/10 + new-account fix (identity v3 heal gate): "
                     "world cards, deal board, Naya speaks, quote-glow; "
                     "bug-verify-v4 67/0, end-probe-v2 200/0")
    print("COMMIT:", sha)
    for p, s in blobs:
        print(f"  {s}  {p}")
