#!/usr/bin/env python3
"""Third commit on hub/shell-bars-20261113: fix the §8 'one commit' line in the
record (it is now two commits) and file this script + file-correction.py, so
the correction mechanism is on the branch too. Nothing else changes.
Head-guard: parent is d3cc94fa804c53d8338b93c7a4d60b43af5c209c.
"""
import base64
import json
import subprocess
import sys

GH = "/home/hatch/workspace/team-nitro/gh-direct.py"
REPO = "SoulSchoolAcademy/NayaPOWER"
BRANCH = "hub/shell-bars-20261113"
PREFIX = "team-nitro/hub-shell-bars-20261113/"
WD = "/home/hatch/workspace/team-nitro/hub-shell-bars-20261113"
PARENT = "d3cc94fa804c53d8338b93c7a4d60b43af5c209c"

FILES = [
    "RECORD-HUB-SHELL-BARS-20261113.md",
    "file-correction.py",
    "file-record-fix.py",
]

MESSAGE = (
    "Hub shell bars: record says two commits; file the correction scripts\n\n"
    "The §8 DONE line said 'one commit' after the proof-link casing\n"
    "correction made it two. Fixed in the record. This commit also files\n"
    "file-correction.py (commit 2) and this script (commit 3), so the\n"
    "correction mechanism is on the branch too. Nothing else changes."
)


def gh(method, path, body=None):
    args = ["python3", GH, method, f"/repos/{REPO}{path}"]
    inp = None
    if body is not None:
        args.append("@/dev/stdin")
        inp = json.dumps(body)
    r = subprocess.run(args, input=inp, capture_output=True, text=True, timeout=180)
    first = r.stdout.splitlines()[0] if r.stdout.splitlines() else ""
    try:
        resp = json.loads("\n".join(r.stdout.splitlines()[1:]))
    except Exception:
        resp = {}
    return first, resp, r


def make_blob(data: bytes):
    first, resp, _ = gh("POST", "/git/blobs",
                        {"content": base64.b64encode(data).decode(), "encoding": "base64"})
    assert first.strip() == "HTTP 201", f"blob failed: {first} {resp}"
    return resp["sha"]


first, resp, _ = gh("GET", f"/git/commits/{PARENT}")
assert first.strip() == "HTTP 200", f"parent read failed: {first} {resp}"
base_tree = resp["tree"]["sha"]
print(f"parent {PARENT} tree {base_tree}")

entries = []
local = {}
for fname in FILES:
    data = open(f"{WD}/{fname}", "rb").read()
    local[fname] = data
    sha = make_blob(data)
    print(f"blob {fname}: {len(data)} B sha={sha}")
    entries.append({"path": PREFIX + fname, "mode": "100644",
                    "type": "blob", "sha": sha})

first, resp, _ = gh("POST", "/git/trees",
                    {"base_tree": base_tree, "tree": entries})
assert first.strip() == "HTTP 201", f"tree failed: {first} {resp}"
tree_sha = resp["sha"]
print(f"tree {tree_sha}")

first, resp, _ = gh("POST", "/git/commits",
                    {"message": MESSAGE, "tree": tree_sha, "parents": [PARENT]})
assert first.strip() == "HTTP 201", f"commit failed: {first} {resp}"
commit_sha = resp["sha"]
print(f"commit {commit_sha}")

first, resp, _ = gh("PATCH", f"/git/refs/heads/{BRANCH}", {"sha": commit_sha})
assert first.strip() == "HTTP 200", f"ref update failed: {first} {resp}"
print(f"branch {BRANCH} -> {commit_sha}")

fails = []
for fname in FILES:
    first, resp, _ = gh("GET", f"/contents/{PREFIX}{fname}?ref={BRANCH}")
    assert first.strip() == "HTTP 200", f"read-back {fname} failed: {first}"
    back = base64.b64decode(resp.get("content", ""))
    ok = back == local[fname]
    print(f"read-back {fname}: {len(back)} B match={ok} sha={resp.get('sha','')}")
    if not ok:
        fails.append(fname)
if fails:
    print("READ-BACK FAILURES:", fails)
    sys.exit(1)
print(f"RECORD-FIX COMMIT {commit_sha} FILED + READ-BACK VERIFIED")
print(f"BRANCH {BRANCH} NOW AT {commit_sha} (parent {PARENT})")
