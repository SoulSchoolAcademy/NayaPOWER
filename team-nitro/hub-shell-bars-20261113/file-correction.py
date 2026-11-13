#!/usr/bin/env python3
"""Follow-up commit on hub/shell-bars-20261113: correct the proof-host link
casing in the record + receipt (TEAM-NITRO/ -> team-nitro/).
Why: the first commit carried the link with an uppercase path, copied from
the bottom-icons pattern — but this round's files live under lowercase
team-nitro/ (the repo carries both casings), so the uppercase link 404d.
The corrected lowercase link is verified 200 + byte-identical before this
commit is made. Nothing else changes. Bodies piped via @/dev/stdin.
Head-guard: parent is the first commit b2bd78cd732041b262d69d077ebf9a9758a6af11.
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
PARENT = "b2bd78cd732041b262d69d077ebf9a9758a6af11"

FILES = [
    "RECORD-HUB-SHELL-BARS-20261113.md",
    "receipt-hub-shell-bars.json",
]

MESSAGE = (
    "Hub shell bars: correct the proof-host link casing (record + receipt)\n\n"
    "The first commit carried the proof-host link with an uppercase\n"
    "TEAM-NITRO/ path, copied from the bottom-icons pattern — but this\n"
    "round's files live under lowercase team-nitro/ (the repo carries both\n"
    "casings), so the uppercase link 404d. The corrected lowercase link is\n"
    "verified 200 + byte-identical to the fixed shell. Nothing else changes."
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


# Head-guard: parent must be the first commit; get its tree.
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
print(f"CORRECTION COMMIT {commit_sha} FILED + READ-BACK VERIFIED")
print(f"BRANCH {BRANCH} NOW AT {commit_sha} (parent {PARENT})")
