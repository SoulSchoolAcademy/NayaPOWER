#!/usr/bin/env python3
"""File the Hub bar-overflow fix to branch hub/bar-overflow-fix-20261114 as
ONE commit via the GitHub Git Data API (blobs -> tree -> commit -> ref),
using gh-direct.py (in-memory app token, never the cache file).
Bodies are piped via @/dev/stdin (no multi-MB body staged to disk — the
EPERM flake rule). Head-guard: the tree's base_tree is the main head
verified first-hand in this round (3d3ef4e66); the branch is created from
it. Never main, never a PR, never a merge. One file: HUB/app/index.html —
the fixed shell, byte-identical to the bake template. After the ref is
created, the file is read back via raw and compared byte-for-byte.
"""
import base64
import hashlib
import json
import subprocess
import sys

GH = "/home/hatch/workspace/team-nitro/gh-direct.py"
REPO = "SoulSchoolAcademy/NayaPOWER"
BRANCH = "hub/bar-overflow-fix-20261114"
MAIN_HEAD = "3d3ef4e668804a5d9b775b65994a62f9f4eac938"
WD = "/home/hatch/workspace/team-nitro/hub-bar-overflow-fix-20261114/work"

MESSAGE = (
    "Hub: 9-circle bar overflow fix — scroll affordance (staged, NOT live)\n\n"
    "At 390/360 the bar's 9 pills need 578px of row (370/340 available):\n"
    "CONNECTIONS cut at the edge, SMART LISTS / REPORTS / 10 APPS\n"
    "off-viewport. The row already scrolls (overflow-x:auto, snap-to-whole\n"
    "pills) but nothing says there is more — scrollbar hidden, no fade, no\n"
    "control. Fix, bar-only: edge fades + edge chevron buttons driven by\n"
    "data-obb-more on the bar (the row's own scroll state); a chevron tap\n"
    "scrolls the first not-fully-visible pill into view (scrollIntoView,\n"
    "snap-aware — plain scrollBy stops at the first snap point under\n"
    "scroll-snap-stop:always). At 1440 the row never overflows, so nothing\n"
    "shows and nothing changes. Same bytes as the bake template\n"
    "(~/workspace/user/files/index-2.html), so the next SN sync cannot\n"
    "revert it. Staged proof only; live is Shawn's tap."
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


data = open(WD + "/index-fixed.html", "rb").read()
print(f"fixed shell: {len(data)} B sha {hashlib.sha256(data).hexdigest()}")
assert hashlib.sha256(data).hexdigest() == "7d25f59105996fa0c40bde4d3b17a8c5e727e95861fc442b344c9f5ed840797d"
tpl = open("/home/hatch/workspace/user/files/index-2.html", "rb").read()
assert tpl == data, "template != fixed shell - STOP"
print("template byte-identical to fixed shell")

# 1. Head-guard.
first, resp, _ = gh("GET", f"/git/commits/{MAIN_HEAD}")
assert first.strip() == "HTTP 200", f"main head read failed: {first} {resp}"
base_tree = resp["tree"]["sha"]
print(f"main head {MAIN_HEAD} tree {base_tree}")

# 2. Blob.
first, resp, _ = gh("POST", "/git/blobs",
                    {"content": base64.b64encode(data).decode(), "encoding": "base64"})
assert first.strip() == "HTTP 201", f"blob failed: {first} {resp}"
blob_sha = resp["sha"]
print(f"blob HUB/app/index.html: {len(data)} B sha={blob_sha}")

# 3. Tree on the verified base.
first, resp, _ = gh("POST", "/git/trees",
                    {"base_tree": base_tree,
                     "tree": [{"path": "HUB/app/index.html", "mode": "100644",
                               "type": "blob", "sha": blob_sha}]})
assert first.strip() == "HTTP 201", f"tree failed: {first} {resp}"
tree_sha = resp["sha"]
print(f"tree {tree_sha}")

# 4. One commit.
first, resp, _ = gh("POST", "/git/commits",
                    {"message": MESSAGE, "tree": tree_sha, "parents": [MAIN_HEAD]})
assert first.strip() == "HTTP 201", f"commit failed: {first} {resp}"
commit_sha = resp["sha"]
print(f"commit {commit_sha}")

# 5. The branch ref.
first, resp, _ = gh("POST", "/git/refs",
                    {"ref": f"refs/heads/{BRANCH}", "sha": commit_sha})
assert first.strip() == "HTTP 201", f"ref failed: {first} {resp}"
print(f"branch {BRANCH} -> {commit_sha}")

# 6. Read-back via raw, byte-exact.
import urllib.request
url = (f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/HUB/app/index.html")
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
back = urllib.request.urlopen(req, timeout=120).read()
print(f"read-back raw: {len(back)} B sha {hashlib.sha256(back).hexdigest()}")
assert back == data, "read-back mismatch - STOP"
print(f"ALL VERIFIED: BRANCH {BRANCH} COMMIT {commit_sha} BLOB {blob_sha}")
print(f"PROOF LINK https://naya-proof-host.nayapower.workers.dev/?file=HUB/app/index.html&ref={BRANCH}&cb={blob_sha}")
