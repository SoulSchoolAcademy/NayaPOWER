#!/usr/bin/env python3
"""File the Hub live leg to branch hub/live-leg-20261113 as ONE commit via
the GitHub Git Data API (blobs -> tree -> commit -> ref), using gh-direct.py
(in-memory app token, never the cache file). Modeled on the bars round's
file-to-branch.py. Bodies piped via @/dev/stdin (no multi-MB body staged
to disk — the EPERM flake rule). Head-guard: the tree's base_tree is the
main head verified first-hand in this round (536d4cc2...); the branch is
created from it. This commit carries ONLY the three HUB live-leg files —
the record/scorecard/receipt land on the same branch in a second commit
after the live verification. The MERGE of this commit to main is the
deploy trigger (GitHub auto-deploy workflow); it happens only on the
separate merge step, after this filing is read back byte-exact.
"""
import base64
import json
import subprocess
import sys

GH = "/home/hatch/workspace/team-nitro/gh-direct.py"
REPO = "SoulSchoolAcademy/NayaPOWER"
BRANCH = "hub/live-leg-20261113"
WD = "/home/hatch/workspace/team-nitro/hub-live-leg-20261113/work"
MAIN_HEAD = "536d4cc255d9ed9373737e9dfa1e6bd481a60a0c"

# (repo path, local file)
FILES = [
    ("HUB/app/index.html", "index-intel-today-LIVE.html"),
    ("HUB/hub-worker.js", "hub-worker-phase1.js"),
    ("HUB/wrangler.toml", "wrangler.toml"),
]

MESSAGE = (
    "Hub live leg: restore the fixed shell + phase-1 worker + wrangler +4 (Shawn tap 16:24Z)\n\n"
    "HUB/app/index.html: the proven bars fixed shell (a687f16a, 5,559,180 B)\n"
    "re-baked with the current 200 live notes (SN-2766 in the set, SN-2696 in\n"
    "the set) + the /hub/feed absolute-src fix (src=\"/js/naya-search.js\").\n"
    "4,960,598 B, sha 64380ef3. Carries the slug fix (SLUG_MAP first in\n"
    "findNoteBySlug + install-modal suppression on note landings) and the\n"
    "bars fix (9 round black circles + 3 ultimate gems). Live was serving\n"
    "the 16:17Z SN-sync rebake (4,992,296 B, fa81a5f4) with zero note-route\n"
    "markers — this is a restoration, not a top-up.\n\n"
    "HUB/hub-worker.js: the UNCHANGED phase-1 worker (49,174 B, 8ee4f859)\n"
    "so Googlebot gets the note page in initial HTML instead of a 302.\n\n"
    "HUB/wrangler.toml: run_worker_first base 8 + /robots.txt, /sitemap.xml,\n"
    "/images, /images/* (no phase-2 patterns).\n\n"
    "SN-2696 publication approved by Shawn 16:28Z (\"Yes, publish SN-2696 as\n"
    "the first public note\") and rides this leg: /s/sn2696 renders live.\n"
    "The SN-sync bake template (~/workspace/user/files/index-2.html) was\n"
    "fixed to these same bytes BEFORE this filing, so the next sync rebake\n"
    "preserves the route (proven with the sync's own inject function).\n"
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


# 1. Head-guard.
first, resp, _ = gh("GET", f"/git/commits/{MAIN_HEAD}")
assert first.strip() == "HTTP 200", f"main head read failed: {first} {resp}"
base_tree = resp["tree"]["sha"]
print(f"main head {MAIN_HEAD} tree {base_tree}")

# 2. Blobs.
entries = []
local = {}
for repo_path, fname in FILES:
    data = open(f"{WD}/{fname}", "rb").read()
    local[repo_path] = data
    sha = make_blob(data)
    print(f"blob {repo_path}: {len(data)} B sha={sha}")
    entries.append({"path": repo_path, "mode": "100644",
                    "type": "blob", "sha": sha})

# 3. Tree on the verified base.
first, resp, _ = gh("POST", "/git/trees",
                    {"base_tree": base_tree, "tree": entries})
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

# 6. Read-back: every file via the contents API, byte-exact.
fails = []
for repo_path, _ in FILES:
    first, resp, _ = gh("GET", f"/contents/{repo_path}?ref={BRANCH}")
    assert first.strip() == "HTTP 200", f"read-back {repo_path} failed: {first}"
    back = base64.b64decode(resp.get("content", ""))
    ok = back == local[repo_path]
    print(f"read-back {repo_path}: {len(back)} B match={ok} sha={resp.get('sha','')}")
    if not ok:
        fails.append(repo_path)
if fails:
    print("READ-BACK FAILURES:", fails)
    sys.exit(1)
print(f"ALL {len(FILES)} FILES FILED IN ONE COMMIT {commit_sha} + READ-BACK VERIFIED")
print(f"BRANCH {BRANCH} BASE {MAIN_HEAD}")
