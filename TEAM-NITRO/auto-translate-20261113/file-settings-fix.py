#!/usr/bin/env python3
"""File the Auto-Translate SETTINGS-FIX branch as ONE commit via gh-direct.py.
One API write at a time: a blob per file (base64 generated in memory via
process substitution — never staged to disk), then one tree, one commit,
one ref-create (POST — the branch is new; PATCH if it already exists).
The new commit's parent is f9242820 (the Auto-Translate tip), so the branch
ends with exactly one commit on top of the round.
Usage: file-settings-fix.py <manifest.json> <message-file>
Manifest: [{"repo": "TEAM-NITRO/...", "local": "/home/hatch/workspace/..."}]
Prints the new commit sha. Verifies the ref afterwards."""
import json, subprocess, sys, re

REPO = "SoulSchoolAcademy/NayaPOWER"
GH = "/home/hatch/workspace/team-nitro/gh-direct.py"
PARENT = "f9242820df009ce0270b2e4ad93cd5cbe98a170c"
BASE_TREE = "d4e98d3c51f3f1b05e6a946262f88ec949decc7d"
BRANCH = "personal/auto-translate-settings-fix-20261113"

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
    try:
        ref_body = json.dumps({"ref": "refs/heads/" + BRANCH, "sha": commit["sha"]})
        fd, tmp = tempfile.mkstemp(suffix=".json", dir="/tmp")
        with os.fdopen(fd, "w") as f:
            f.write(ref_body)
        try:
            ref = gh("POST", "/git/refs", "@" + tmp)
        finally:
            os.unlink(tmp)
    except RuntimeError:
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
