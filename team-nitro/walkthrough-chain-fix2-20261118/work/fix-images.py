#!/usr/bin/env python3
"""FIX2 item 5 — attach the orphan image blobs at the paths the pages
reference, on the branches the proof-host URLs name.

Diagnosis: welcome's deck slides + the unfold's faces reference
proof-host URLs with ref=deck/royal-unfolding-20261115 and
ref=agreement/unfold-20261117. BOTH branches do not exist in the repo,
and the files exist nowhere in any tree — only the blobs exist (the
cb= values in the URLs ARE the blob shas). Proof-host resolves
path+ref+cb against the branch tree, so every image 404s.

Fix: verify every cb blob exists, then create each branch as a root
commit whose tree holds exactly those files at those paths. No page
bytes change; the existing srcs start serving. No PR, no merge, no
main change.
"""
import base64, json, os, subprocess, sys, time

HOME = os.path.expanduser("~")
GH = os.path.join(HOME, "workspace/team-nitro/gh-direct.py")
REPO = "SoulSchoolAcademy/NayaPOWER"

import re

def collect(path):
    t = open(path, encoding="utf-8").read().replace("&amp;", "&")
    urls = re.findall(
        r"https://naya-proof-host\.nayapower\.workers\.dev/\?file=([^&\"<> ]+)&ref=([^&\"<> ]+)&cb=([0-9a-f]+)",
        t)
    seen = {}
    for f, ref, cb in urls:
        seen[(f, ref)] = cb
    return seen

def gh(method, path, body=None):
    args = [sys.executable, GH, method, path]
    inp = None
    if body is not None:
        args.append("@/dev/stdin")
        inp = json.dumps(body).encode()
    p = subprocess.run(args, input=inp, capture_output=True)
    out = p.stdout.decode("utf-8", "replace")
    lines = out.split("\n", 1)
    status = int(lines[0].split()[1]) if lines and lines[0].startswith("HTTP") else -1
    payload = lines[1] if len(lines) > 1 else ""
    if status >= 400 or p.returncode != 0:
        print("FAIL %s %s: HTTP %s %s" % (method, path, status, payload[:400]), file=sys.stderr)
        sys.exit(1)
    try:
        return json.loads(payload) if payload.strip() else {}
    except json.JSONDecodeError:
        return {"_raw": payload[:300]}

WELCOME = os.path.join(HOME, "workspace/team-nitro/walk-v23-assembly-20261114/welcome-staged.html")
UNFOLD = os.path.join(HOME, "workspace/team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html")
imgs = {}
imgs.update(collect(WELCOME))
imgs.update(collect(UNFOLD))
print("total distinct image refs: %d" % len(imgs), flush=True)

# group by branch ref
by_ref = {}
for (f, ref), cb in sorted(imgs.items()):
    by_ref.setdefault(ref, []).append((f, cb))

# verify every blob exists
for ref, items in sorted(by_ref.items()):
    for f, cb in items:
        d = gh("GET", "/repos/%s/git/blobs/%s" % (REPO, cb))
        assert d.get("sha") == cb, "blob mismatch %s" % cb
        print("blob ok %s %d B %s" % (f, d.get("size", -1), cb[:12]), flush=True)

# create each branch
for ref, items in sorted(by_ref.items()):
    tree_entries = [{"path": f, "mode": "100644", "type": "blob", "sha": cb}
                    for f, cb in items]
    t = gh("POST", "/repos/%s/git/trees" % REPO, {"tree": tree_entries})
    tree_sha = t["sha"]
    print("tree %s: %s (%d files)" % (ref, tree_sha[:12], len(items)), flush=True)
    c = gh("POST", "/repos/%s/git/commits" % REPO,
           {"message": "FIX2 (2026-11-18): attach deck/unfold images at their referenced paths (orphan blobs, no page change)",
            "tree": tree_sha, "parents": []})
    commit_sha = c["sha"]
    print("commit %s: %s" % (ref, commit_sha[:12]), flush=True)
    r = gh("POST", "/repos/%s/git/refs" % REPO,
           {"ref": "refs/heads/%s" % ref, "sha": commit_sha})
    print("branch created: %s -> %s" % (ref, r.get("object", {}).get("sha", "")[:12]), flush=True)

print("IMAGE BRANCHES DONE", flush=True)
