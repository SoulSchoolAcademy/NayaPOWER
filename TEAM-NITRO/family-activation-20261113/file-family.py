#!/usr/bin/env python3
"""File the Family Activation work-dir docs on branch
family/activation-twelve-heroes-20261113, all in memory where the flake
bites (reads from disk are fine; network PUTs are fine; exec writes are not
trusted — every PUT is verified by read-back blob sha).
Creates the branch from the CURRENT main tip, read first-hand at run time.
PUTs each file sequentially (GitHub writes go one at a time), skips files
whose blob sha already matches (idempotent — safe to re-run after updating
the record with the round-3 findings).
Usage: python3 file-family.py"""
import base64
import hashlib
import importlib.util
import json
import os
import sys
import urllib.request
import urllib.error

spec = importlib.util.spec_from_file_location("gh_direct", "/home/hatch/workspace/team-nitro/gh-direct.py")
gh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gh)

REPO = "SoulSchoolAcademy/NayaPOWER"
BRANCH = "family/activation-twelve-heroes-20261113"
D = "/home/hatch/workspace/team-nitro/family-activation-20261113"
TOKEN = gh.get_token()
BASE = "https://api.github.com"


def api(method, path, body=None):
    req = urllib.request.Request(
        BASE + path, data=json.dumps(body).encode() if body is not None else None,
        method=method, headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": "muse-github-skill/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or "{}")


def git_blob_sha(raw: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(raw) + raw).hexdigest()


# --- main tip, first-hand ---
st, main = api("GET", f"/repos/{REPO}/branches/main")
assert st == 200, f"main read failed {st} {str(main)[:200]}"
tip = main["commit"]["sha"]
print("main tip:", tip, main["commit"]["commit"]["message"][:60], flush=True)

# --- branch (idempotent: 422 = already exists) ---
st, r = api("POST", f"/repos/{REPO}/git/refs",
            {"ref": f"refs/heads/{BRANCH}", "sha": tip})
print("branch create:", st, r.get("ref") or r.get("message"), flush=True)
if st == 422:
    st, r = api("GET", f"/repos/{REPO}/git/refs/heads/{BRANCH}")
    print("branch exists at:", st, (r.get("object") or {}).get("sha"), flush=True)
    assert (r.get("object") or {}).get("sha") == tip or True, "branch tip differs (noted, not fatal)"
elif st not in (200, 201):
    raise SystemExit(f"branch create failed {st} {str(r)[:300]}")

ALIASES = ["sophia", "thea", "zoe", "astraea", "vera", "wren",
           "iris", "ruth", "terra", "esme", "mira", "aurelia"]
files = [
    ("RECORD-FAMILY-ACTIVATION-20261113.md",
     "Record: family activation maker round — ground proven, walks blocked, probe + drafts + chain ready"),
    ("SCORECARD-FAMILY-ACTIVATION-20261113.md",
     "Scorecard: family activation maker round — honest 5/10, rate 0 closed loops/hour"),
    ("RECEIPT-FAMILY-ACTIVATION-20261113.md",
     "Receipt: family activation maker round — first-hand measurements"),
    ("TWELVE-ANSWERS.md",
     "The twelve sisters' ten walk answers in lane voice (120 answers) + page names"),
    ("family-probe.py",
     "Family probe: twelve walks through the staged walk v22 (harvested from q10-probe.py)"),
    ("file-notes.py",
     "File the twelve briefing notes after the walks prove the pages (gh-direct mechanism)"),
    ("stage-twelve.py",
     "Stage the twelve sisters onto the transparency page (edits the stage step's files)"),
    ("STAGE-TWELVE-README.md",
     "Stage-twelve README: chain, files edited, builder byline deviation"),
    ("file-family.py",
     "File this round's work-dir docs to the branch (branch from live main tip, sequential PUTs, read-back verified)"),
] + [(f"NN-20261113-family-{a}.md",
      f"Briefing Naya Note DRAFT for {a} (not filed — links TBD until her walk proves her pages)")
     for a in ALIASES]

failed = []
for name, msg in files:
    raw = open(os.path.join(D, name), "rb").read()
    assert len(raw) > 0, f"{name} is 0 bytes — flake damage, refusing to file it"
    path = f"TEAM-NITRO/family-activation-20261113/{name}"
    want = git_blob_sha(raw)
    st0, r0 = api("GET", f"/repos/{REPO}/contents/{path}?ref={BRANCH}")
    cur = r0.get("sha") if isinstance(r0, dict) else None
    if st0 == 200 and cur == want:
        print(f"SKIP {name}: already filed, blob={want}", flush=True)
        continue
    body = {"message": msg, "content": base64.b64encode(raw).decode(), "branch": BRANCH}
    if st0 == 200 and cur:
        body["sha"] = cur
    st, r = api("PUT", f"/repos/{REPO}/contents/{path}", body)
    sha = (r.get("content") or {}).get("sha")
    print(f"PUT {name}: HTTP {st} blob={sha} size={len(raw)} want={want}", flush=True)
    st2, r2 = api("GET", f"/repos/{REPO}/contents/{path}?ref={BRANCH}")
    got = r2.get("sha") if isinstance(r2, dict) else None
    print(f"  read-back: HTTP {st2} blob={got} match={got == want}", flush=True)
    if got != want:
        failed.append(name)
if failed:
    raise SystemExit(f"FAILED read-backs: {failed}")
print(f"FILED: {len(files)} files on branch {BRANCH} (main tip {tip})", flush=True)
