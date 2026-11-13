#!/usr/bin/env python3
"""File (or re-file) the Auto-Translate branch as ONE commit via gh-direct.py.
One API write at a time: a blob per file (base64 generated in memory via
process substitution — never staged to disk), then one tree, one commit,
one force ref-update. The new commit's parent is 5b1a8ccc1 (the Personal
complete tip), so the branch ends with exactly one commit — it REPLACES the
interim 17:50Z commit 5bd5b35f7, whose message claimed verifications that
were never run (translations read back, honest failure, no-words pass).
Usage: file-amend.py <manifest.json> <message-file>
Manifest: [{"repo": "TEAM-NITRO/...", "local": "/home/hatch/workspace/..."}]
Prints the new commit sha. Verifies the ref afterwards."""
import json, subprocess, sys, re

REPO = "SoulSchoolAcademy/NayaPOWER"
GH = "/home/hatch/workspace/team-nitro/gh-direct.py"
PARENT = "5b1a8ccc1d5b59bd4d2b49f2c80e83a46c695159"
BASE_TREE = "bbede72bedaf70ecc10406dfe67303f67add904e"
BRANCH = "personal/auto-translate-20261113"

def gh(method, path, body_arg=None):
    cmd = ["python3", GH, method, "/repos/%s%s" % (REPO, path)]
    if body_arg is not None:
        cmd.append(body_arg)
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    out = r.stdout or ""
    m = re.search(r"\{.*\}", out, re.S)
    if r.returncode != 0 or not m:
        raise RuntimeError("gh %s %s failed rc=%d out=%s err=%s" % (method, path, r.returncode, out[:500], r.stderr[:300]))
    return json.loads(m.group(0))

def blob_for(local):
    # base64 generated in memory by a child python, fed via process substitution
    gen = ("python3 -c \"import base64,json; d=open(%r,'rb').read(); "
           "print(json.dumps({'content':base64.b64encode(d).decode(),'encoding':'base64'}))\"" % local)
    cmd = "python3 %s POST /repos/%s/git/blobs @<( %s )" % (GH, REPO, gen)
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, executable="/bin/bash", timeout=180)
    m = re.search(r"\{.*\}", r.stdout or "", re.S)
    if r.returncode != 0 or not m:
        raise RuntimeError("blob %s failed rc=%d out=%s err=%s" % (local, r.returncode, (r.stdout or "")[:400], (r.stderr or "")[:300]))
    d = json.loads(m.group(0))
    return d["sha"]

def main():
    manifest = json.load(open(sys.argv[1]))
    message = open(sys.argv[2]).read()
    entries = []
    for item in manifest:
        sha = blob_for(item["local"])
        print("blob %-70s %s" % (item["repo"], sha), flush=True)
        entries.append({"path": item["repo"], "mode": "100644", "type": "blob", "sha": sha})
    tree = None
    # tree JSON goes through a small temp file (deleted after the call).
    tree_body = json.dumps({"base_tree": BASE_TREE, "tree": entries})
    import tempfile, os
    fd, tmp = tempfile.mkstemp(suffix=".json", dir="/tmp")
    with os.fdopen(fd, "w") as f:
        f.write(tree_body)
    try:
        tree = gh("POST", "/git/trees", "@" + tmp)
    finally:
        os.unlink(tmp)
    print("tree", tree["sha"], flush=True)
    commit_body = json.dumps({"message": message, "tree": tree["sha"], "parents": [PARENT]})
    fd, tmp = tempfile.mkstemp(suffix=".json", dir="/tmp")
    with os.fdopen(fd, "w") as f:
        f.write(commit_body)
    try:
        commit = gh("POST", "/git/commits", "@" + tmp)
    finally:
        os.unlink(tmp)
    print("commit", commit["sha"], flush=True)
    ref_body = json.dumps({"sha": commit["sha"], "force": True})
    fd, tmp = tempfile.mkstemp(suffix=".json", dir="/tmp")
    with os.fdopen(fd, "w") as f:
        f.write(ref_body)
    try:
        ref = gh("PATCH", "/git/refs/heads/" + BRANCH, "@" + tmp)
    finally:
        os.unlink(tmp)
    print("ref", json.dumps(ref.get("object", ref))[:300], flush=True)
    print("NEW_COMMIT", commit["sha"])

if __name__ == "__main__":
    main()
