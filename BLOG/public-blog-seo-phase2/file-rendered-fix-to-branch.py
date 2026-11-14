#!/usr/bin/env python3
"""File the RENDERED-FIX-round changed files to branch
public-blog/seo-ai-backend-rendered-fix-20261113 under
BLOG/public-blog-seo-phase2/, one contents-API PUT at a time,
verifying each with a read-back. Never main, never a PR, never a merge.
Bodies are piped via bash process substitution (never staged to disk):
the shell is 5.5 MB and the EPERM flake kills multi-MB disk writes.
Read-back: files <= 1 MB are byte-compared via the contents GET;
files > 1 MB are verified by git-blob-sha1 (`git hash-object` locally
vs the `sha` the contents GET returns), because the contents API
omits the `content` field above 1 MB.
Usage: file-rendered-fix-to-branch.py <group>   (group = build | record)
  build  — the edited shell, deploy script, probes, results, bars
           checker results, preserved other-lane bytes, eye-proof shots
  record — the record + scorecard (filed LAST, after the build tip is
           known, so the record's Filing section can state it)
"""
import base64
import json
import subprocess
import sys
import time

GH = "/home/hatch/workspace/team-nitro/gh-direct.py"
REPO = "SoulSchoolAcademy/NayaPOWER"
BRANCH = "public-blog/seo-ai-backend-rendered-fix-20261113"
PREFIX = "BLOG/public-blog-seo-phase2/"
WD = "/home/hatch/workspace/team-nitro/seo-ai-backend-20261113/"

GROUPS = {
    "build": [
        "index-intel-today-phase2.html",
        "deploy-rendered-fix-staging.py",
        "probe-rendered-repro.py",
        "probe-rendered-after.py",
        "probe-grounding2.py",
        "phase2-shots-rendered/probe-rendered-repro-results.json",
        "phase2-shots-rendered/probe-rendered-after-results.json",
        "phase2-shots-rendered/probe-grounding2-results.json",
        "probe-dedupe-results.json",
        "probe-phase2-results.json",
        "probe-phase2-failures.json",
        "phase2-shots-bars/checker-results.json",
        "staging-overwritten-by-other-lane-20261114.html",
        "staging-feed-overwritten-by-other-lane-20261114.json",
        "phase2-shots-rendered/after-note-sn2696-390-related.png",
        "phase2-shots-rendered/after-note-sn2696-1440-related.png",
        "phase2-shots-rendered/after-note-sn2696-360-related.png",
        "phase2-shots-rendered/after-note-sn2766-390-related.png",
        "phase2-shots-rendered/after-note-sn2695-390-related.png",
        "phase2-shots-rendered/after-feedclick-sn2766-390.png",
        "phase2-shots-rendered/after-feedclick-sn2695-390.png",
        "file-rendered-fix-to-branch.py",
    ],
    "record": [
        "RECORD-SEO-AI-BACKEND-RENDERED-FIX-20261113.md",
        "SCORECARD-SEO-AI-BACKEND-RENDERED-FIX-20261113.md",
    ],
}

def run(cmd):
    r = subprocess.run(cmd, shell=True, executable="/bin/bash",
                       capture_output=True, text=True, timeout=300)
    return r.stdout, r.stderr

def git_blob_sha1(path):
    out, _ = run(f"git hash-object '{path}'")
    return out.strip()

group = sys.argv[1]
FILES = GROUPS[group]
fails = []
for fname in FILES:
    local = WD + fname
    data = open(local, "rb").read()
    out0, _ = run(f"python3 {GH} GET /repos/{REPO}/contents/{PREFIX}{fname}?ref={BRANCH}")
    existing_sha = ""
    try:
        resp0 = json.loads("\n".join(out0.splitlines()[1:]))
        existing_sha = resp0.get("sha", "")
    except Exception:
        pass
    mkbody = ("python3 -c \"import json,base64,sys; "
              "d=open(sys.argv[1],'rb').read(); "
              "body={'message': sys.argv[2], 'content': base64.b64encode(d).decode(), 'branch': sys.argv[3]}; "
              f"body.update({{'sha': sys.argv[4]}}) if len(sys.argv) > 4 else None; "
              "print(json.dumps(body))\" "
              f"'{local}' 'Rendered fix Area #9 (R1-R6): {fname}' '{BRANCH}'"
              + (f" '{existing_sha}'" if existing_sha else ""))
    cmd = (f"python3 {GH} PUT /repos/{REPO}/contents/{PREFIX}{fname} "
           f"@<({mkbody})")
    out, err = run(cmd)
    first = out.splitlines()[0] if out.splitlines() else ""
    ok = first.strip() in ("HTTP 200", "HTTP 201")
    sha = ""
    try:
        resp = json.loads("\n".join(out.splitlines()[1:]))
        sha = resp.get("content", {}).get("sha", "")
    except Exception:
        pass
    print(f"PUT {fname}: {first} sha={sha[:12]} bytes={len(data)}", flush=True)
    if not ok or not sha:
        print("  RESPONSE:", out[:500], err[:300])
        fails.append(fname)
        continue
    time.sleep(2)
    out2, _ = run(f"python3 {GH} GET /repos/{REPO}/contents/{PREFIX}{fname}?ref={BRANCH}")
    try:
        resp2 = json.loads("\n".join(out2.splitlines()[1:]))
        if len(data) > 1_000_000:
            want = git_blob_sha1(local)
            got = resp2.get("sha", "")
            print(f"  read-back (blob sha): filed={got[:12]} local={want[:12]} match={got == want}", flush=True)
            if got != want:
                fails.append(fname + " (blob-sha mismatch)")
        else:
            back = base64.b64decode(resp2.get("content", ""))
            print(f"  read-back: {len(back)}B match={back == data} sha={resp2.get('sha','')[:12]}", flush=True)
            if back != data:
                fails.append(fname + " (read-back mismatch)")
    except Exception as e:
        print("  read-back FAILED:", str(e)[:200], out2[:300])
        fails.append(fname + " (read-back error)")

if fails:
    print("FAILED:", fails)
    sys.exit(1)
print(f"ALL {len(FILES)} FILES FILED + READ-BACK VERIFIED ({group})")
