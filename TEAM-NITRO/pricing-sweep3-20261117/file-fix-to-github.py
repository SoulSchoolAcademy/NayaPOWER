#!/usr/bin/env python3
"""File the Sweep #3 fix round (14 fixes + certificate harvest) to GitHub.

Repo: SoulSchoolAcademy/NayaPOWER (TEAM-NITRO is a folder inside it).
Base: pricing-f4-free-entry-20261116, head eafbac16.
New branch: pricing/sweep3-20261117 (created from eafbac16 here).
PR: opened UNMERGED against pricing-f4-free-entry-20261116 (the branch's
parent — the diff is exactly this round's files). No merge, no deploy.
Method: git data API via gh-direct.py (token minted in memory, never the
cache). Create ref -> blobs -> tree (base = eafbac16's tree) -> commit ->
ref PATCH -> verify (ref + every blob read-back decodes to the local bytes,
sha256 match) -> open PR.
"""
import base64
import hashlib
import importlib.util
import json
import os
import urllib.error
import urllib.request

spec = importlib.util.spec_from_file_location(
    "gh_direct", "/home/hatch/workspace/team-nitro/gh-direct.py")
gh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gh)

REPO = "SoulSchoolAcademy/NayaPOWER"
BASE_BRANCH = "pricing-f4-free-entry-20261116"
BASE_SHA = "eafbac1616966bd6b1d0151a916140722c7699ba"
BRANCH = "pricing/sweep3-20261117"
BASE = "https://api.github.com"
HOME = "/home/hatch/workspace/team-nitro/"

FILES = [
    "fixed-entry.html",
    "manifest.webmanifest",
    "icons/icon-512.png",
    "icons/icon-192.png",
    "icons/apple-touch-icon.png",
    "apply-fix.py",
    "apply-cert.py",
    "MAKER-REPORT.md",
    "CHECKER-VERDICT.md",
    "RECORD-CORRECTIONS.md",
    "DEPLOY-NOTE.md",
    "file-fix-to-github.py",
]

token = gh.get_token()


def call(method, path, body=None):
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(body).encode() if body is not None else None,
        method=method,
        headers={"Accept": "application/vnd.github+json",
                 "X-GitHub-Api-Version": "2022-11-28",
                 "Authorization": f"Bearer {token}",
                 "Content-Type": "application/json",
                 "User-Agent": "muse-github-skill/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        try:
            return e.code, json.loads(raw)
        except json.JSONDecodeError:
            return e.code, {"raw": raw[:300]}


# 1. Create the branch from eafbac16 (fail-stop if it already exists —
#    a second run must not silently file onto a moved branch).
st, ref = call("GET", f"/repos/{REPO}/git/ref/heads/{BRANCH}")
assert st == 404, f"branch {BRANCH} already exists ({st}) — STOP, do not re-file blind"
st, ref = call("POST", f"/repos/{REPO}/git/refs",
               {"ref": f"refs/heads/{BRANCH}", "sha": BASE_SHA})
assert st == 201, f"branch create failed: {st} {ref}"
print(f"branch {BRANCH} created at {ref['object']['sha']}", flush=True)

st, base_commit = call("GET", f"/repos/{REPO}/git/commits/{BASE_SHA}")
assert st == 200, f"base commit GET failed: {st} {base_commit}"
base_tree = base_commit["tree"]["sha"]
print("base tree:", base_tree, flush=True)

# 2. Blobs.
entries = []
local_by_path = {}
for name in FILES:
    local = os.path.join(HOME, "pricing-sweep3-20261117", name)
    raw = open(local, "rb").read()
    assert len(raw) > 0, f"{local} is 0 bytes — STOP (flake damage)"
    st, blob = call("POST", f"/repos/{REPO}/git/blobs",
                    {"content": base64.b64encode(raw).decode("ascii"),
                     "encoding": "base64"})
    assert st == 201, f"blob POST failed for {name}: {st} {blob}"
    print(f"blob {name}: {blob['sha']} ({len(raw)} B, "
          f"sha256={hashlib.sha256(raw).hexdigest()[:8]}...)", flush=True)
    entries.append({"path": "TEAM-NITRO/pricing-sweep3-20261117/" + name,
                    "mode": "100644", "type": "blob", "sha": blob["sha"]})
    local_by_path[name] = raw

# 3. Tree -> commit -> ref.
st, tree = call("POST", f"/repos/{REPO}/git/trees",
                {"base_tree": base_tree, "tree": entries})
assert st == 201, f"tree POST failed: {st} {tree}"
print("tree:", tree["sha"], flush=True)

msg = ("Inspector Sweep #3 fix round — Free Entry (/free), link #13 (score 7/10) "
       "+ certificate-current harvest (Shawn 18:44Z). 14 fixes: type scale "
       "25/19/17 (31 rules); deep palette (bright grep to zero); keyboard Enter "
       "submits (veil-up dismisses, never submits); install icons + manifest "
       "(theme #8e24aa); veil intercepts (first click dismisses only); taken "
       "name spaced; h1 + zoom unlocked; Spectrum Flow re-flow (blue->green->"
       "gold); gradients 135 deg; clock jewel; empty clock span; hub-note in "
       "plain words; F4 record corrections. Certificate harvest from identity "
       "8c641f96 (Micheal N.000204 treatment): trophy name (obsidian body, "
       "chrome stroke, purple clone), obsidian panels, white labels, typing "
       "values, white lift, official sentence + (i) reader. Fix 7 (alias "
       "reservation) is Shawn's decision, recorded only. Checker verdict is a "
       "self-check (same seat) — an independent checker is owed. PR open "
       "UNMERGED; no merge, no deploy, no live touch.")
st, commit = call("POST", f"/repos/{REPO}/git/commits",
                  {"message": msg, "tree": tree["sha"], "parents": [BASE_SHA]})
assert st == 201, f"commit POST failed: {st} {commit}"
commit_sha = commit["sha"]
print("commit:", commit_sha, flush=True)

st, ref = call("PATCH", f"/repos/{REPO}/git/refs/heads/{BRANCH}",
               {"sha": commit_sha, "force": False})
assert st == 200, f"ref PATCH failed: {st} {ref}"
print("ref:", ref["ref"], "->", ref["object"]["sha"], flush=True)

# 4. Verify: ref + every blob read-back.
st, ref2 = call("GET", f"/repos/{REPO}/git/ref/heads/{BRANCH}")
assert st == 200 and ref2["object"]["sha"] == commit_sha, "ref verify FAILED"
for name in FILES:
    sha = [e["sha"] for e in entries
           if e["path"] == "TEAM-NITRO/pricing-sweep3-20261117/" + name][0]
    st, blob = call("GET", f"/repos/{REPO}/git/blobs/{sha}")
    assert st == 200, f"blob read-back failed for {name}: {st}"
    decoded = base64.b64decode(blob["content"])
    want = local_by_path[name]
    assert decoded == want, f"blob read-back MISMATCH for {name} — STOP"
    print(f"blob read-back MATCH {name} sha256="
          f"{hashlib.sha256(decoded).hexdigest()}", flush=True)

# 5. Open the PR, UNMERGED, against the F4 branch.
st, pr = call("POST", f"/repos/{REPO}/pulls",
              {"title": "Sweep #3: /free — 14 inspector fixes + certificate-current harvest",
               "head": BRANCH, "base": BASE_BRANCH,
               "body": ("Inspector Sweep #3, link #13 (Free Entry, score 7/10): all 14 "
                        "fixes in §6 of REPORT-13-free-entry.md, plus the "
                        "certificate-current harvest (Shawn 18:44Z — the Micheal "
                        "Nº 000204 treatment, harvested from identity 8c641f96). "
                        "Fixed entry 337,770 B sha256 "
                        "9ac3b4f5f8189bf353af34f186ea9d14133e4024e1312be879a09a87d5f01ad3; "
                        "manifest + 3 icons filed. Fix 7 (alias reservation) is "
                        "Shawn's decision, recorded only. Checker verdict is a "
                        "self-check (same seat, spawn blocked) — an independent "
                        "checker is owed before the captain's eye. DO NOT MERGE. "
                        "No deploy, no live touch; the live step is Shawn's hand.")})
assert st == 201, f"PR create failed: {st} {pr}"
print(f"PR OPEN: {pr['html_url']} (#{pr['number']}) state={pr['state']}", flush=True)
print(f"FILED: branch={BRANCH} commit={commit_sha} blobs={len(entries)} "
      f"pr={pr['html_url']}", flush=True)
