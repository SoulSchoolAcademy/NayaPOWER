#!/usr/bin/env python3
"""Walkthrough-frontend stage + file (2026-11-18) — identity Enter fix.

Files ONE commit on branch walkthrough-frontend-20261118 (from the
flow-end-fix1 tip 43c8ba1e, verified unchanged before branching):
  - team-nitro/walk-v23-assembly-20261114/identity-fixed.html (the fix)
  - team-nitro/walkthrough-frontend-20261118/work/stage-walkthrough.py (this script)
Deliberately NOT filed: welcome-staged.html, agreement-unfold-fixed.html,
walk-beginning-staging-worker.js, build-v23-staging-worker.py — the
agreement flow-end round owns those files mid-flight and this lane does
not touch them. No worker PUT: the staging worker still embeds the OLD
identity (a1550164) until the flow-end round lands and rebuilds it; this
round stages the fixed identity on the PROOF HOST instead and verifies
it serves the new bytes by sha256.
No PR, no merge, no message to Shawn. Report to the coordinator only.
"""
import base64, hashlib, json, subprocess, sys, time

HOME = "/home/hatch"
RECORDS = HOME + "/workspace/team-nitro/walkthrough-frontend-20261118"
WORK = RECORDS + "/work"
GH = HOME + "/workspace/team-nitro/gh-direct.py"
REPO = "SoulSchoolAcademy/NayaPOWER"
NEW_BRANCH = "walkthrough-frontend-20261118"
PARENT_BRANCH = "walk-end/agreement-flow-end-fix1-20261118"
PARENT_TIP = "43c8ba1e399bdc9a5a03c627865586559c83b995"
IDENT_PATH = "team-nitro/walk-v23-assembly-20261114/identity-fixed.html"
OLD_IDENT_SHA = "a1550164251ef804ff51b129c75c33571fedfdbb0554cd70f094dc5ec25c984e"

def sha(b): return hashlib.sha256(b).hexdigest()

def read_bytes(p):
    with open(p, "rb") as f: return f.read()

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
    try:
        data = json.loads(payload) if payload.strip() else {}
    except json.JSONDecodeError:
        data = {"_raw": payload[:500]}
    if status >= 400 or p.returncode != 0:
        print("FAIL %s %s: HTTP %s\n%s" % (method, path, status, payload[:800]), file=sys.stderr)
        sys.exit(1)
    return status, data

def main():
    new_ident = read_bytes(WORK + "/identity-fixed.html")
    ident_sha = sha(new_ident)
    print("input: identity %d B sha %s" % (len(new_ident), ident_sha))
    _, ref = gh("GET", "/repos/%s/git/refs/heads/%s" % (REPO, PARENT_BRANCH))
    print("base branch tip:", ref["object"]["sha"])
    assert ref["object"]["sha"] == PARENT_TIP, "base branch tip moved: %s" % ref["object"]["sha"]
    _, nb = gh("POST", "/repos/%s/git/refs" % REPO,
               {"ref": "refs/heads/%s" % NEW_BRANCH, "sha": PARENT_TIP})
    print("new branch created:", nb["ref"], nb["object"]["sha"])
    assert nb["object"]["sha"] == PARENT_TIP
    _, commit = gh("GET", "/repos/%s/git/commits/%s" % (REPO, PARENT_TIP))
    base_tree = commit["tree"]["sha"]
    print("base tree:", base_tree)
    stage_script = read_bytes(WORK + "/stage-walkthrough.py")
    files = [
        (IDENT_PATH, new_ident),
        ("team-nitro/walkthrough-frontend-20261118/work/stage-walkthrough.py", stage_script),
    ]
    blobs = {}
    for path, data in files:
        _, blob = gh("POST", "/repos/%s/git/blobs" % REPO,
                     {"content": base64.b64encode(data).decode("ascii"), "encoding": "base64"})
        blobs[path] = blob["sha"]
        print("blob %s: %s (%d B)" % (path.split("/")[-1], blob["sha"], len(data)))
    _, tree = gh("POST", "/repos/%s/git/trees" % REPO,
                 {"base_tree": base_tree,
                  "tree": [{"path": p, "mode": "100644", "type": "blob", "sha": s} for p, s in blobs.items()]})
    print("new tree:", tree["sha"])
    msg = ("walkthrough-frontend 2026-11-18: identity Enter works for the returning citizen\n\n"
           "Enter with ?name=Shawn and an empty alias no longer dies on 'Enter alias to\n"
           "continue.': the alias is taken from the arrived name and the claim runs.\n"
           "Enter on an 'already claimed' alias reads the registry row back: when the\n"
           "row's name matches the arrived name (Shawn's own cert No 1, shawn/Shawn,\n"
           "Oct 20), the certificate stamps from registry truth and Enter goes on to\n"
           "the walkthrough (/welcome). A non-matching name still stops, as before.\n"
           "No jump-back button: the staged identity already carries none (live still\n"
           "does - live deploy is Shawn's hand). Walk, welcome, unfold, worker,\n"
           "builder untouched - the flow-end round owns those mid-flight.\n\n"
           "identity %d B sha %s (was %s)\n" % (len(new_ident), ident_sha, OLD_IDENT_SHA[:8]))
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    _, cm = gh("POST", "/repos/%s/git/commits" % REPO,
               {"message": msg, "tree": tree["sha"], "parents": [PARENT_TIP],
                "author": {"name": "nayapower-lane-agent[bot]",
                           "email": "338161897+nayapower-lane-agent[bot]@users.noreply.github.com",
                           "date": now},
                "committer": {"name": "GitHub", "email": "noreply@github.com", "date": now}})
    commit_sha = cm["sha"]
    print("commit sha:", commit_sha)
    _, ref3 = gh("PATCH", "/repos/%s/git/refs/heads/%s" % (REPO, NEW_BRANCH),
                 {"sha": commit_sha, "force": False})
    print("branch now:", ref3["object"]["sha"])
    assert ref3["object"]["sha"] == commit_sha
    for path, data in files:
        _, rb = gh("GET", "/repos/%s/git/blobs/%s" % (REPO, blobs[path]))
        raw = base64.b64decode("".join(rb["content"].split()))
        assert len(raw) == len(data) and sha(raw) == sha(data), "blob read-back mismatch for %s" % path
        print("blob read-back OK:", path.split("/")[-1], len(raw), "bytes, sha match")
    print("IDENT_BLOB=%s" % blobs[IDENT_PATH])
    print("IDENT_SHA=%s" % ident_sha)
    print("COMMIT=%s" % commit_sha)

if __name__ == "__main__":
    main()
