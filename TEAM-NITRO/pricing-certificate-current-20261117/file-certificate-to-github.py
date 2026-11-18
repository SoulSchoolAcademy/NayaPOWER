#!/usr/bin/env python3
"""File the Pricing Certificate Current round to GitHub on a NEW branch.

Repo: SoulSchoolAcademy/NayaPOWER (TEAM-NITRO is a folder inside it).
Branch: pricing/certificate-current-20261117 (NEW, created from the
pricing-f4 tip e6bf9a87 — never from main, never merged).
Method: git data API via gh-direct.py (token minted in memory, never the
cache). Blobs -> tree (base = tip tree) -> commit -> CREATE ref -> PR
(base main, open, unmerged).
The FIXED ENTRY BYTES are filed too (332,182 B, sha 1e1bb489...) —
re-derived IN MEMORY by importing the build module (regen + harvest +
apply + syntax check) and asserted equal to the live staged bytes. They
are NEVER read from disk: the EPERM flake leaves fixed-entry.html as a
0-byte file on disk, and reading it would file damage.
Verifies: base ref == e6bf9a87; ref points at the new commit; every filed
blob read-back decodes to the local/in-memory bytes (sha256 match).
"""
import base64
import hashlib
import importlib.util
import json
import os
import sys
import urllib.error
import urllib.request

spec = importlib.util.spec_from_file_location(
    "gh_direct", "/home/hatch/workspace/team-nitro/gh-direct.py")
gh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gh)

REPO = "SoulSchoolAcademy/NayaPOWER"
BASE_BRANCH = "pricing-f4-free-entry-20261116"
# Current tip of the base branch, verified live 2026-11-17 19:2xZ:
# eafbac16 — "Pricing Fix round: maker report with the filed commit SHA
# recorded (e6bf9a87). No code change." — on top of the pricing-fix commit
# e6bf9a87. (An earlier note said the tip was e6bf9a87; that was stale —
# the tip moved one commit forward when the pricing-fix report was
# re-filed with its receipts.)
BASE_TIP = "eafbac16"
BRANCH = "pricing/certificate-current-20261117"
BASE = "https://api.github.com"
HOME = "/home/hatch/workspace/team-nitro/"
ROUND = "pricing-certificate-current-20261117/"
STAGED_ENTRY_SHA = "1e1bb4894b3e4bffed026781ac08976e8353b0e2bb020652357f567a711b16a3"

DISK_FILES = [
    "MAKER-REPORT.md",
    "build-certificate.py",
    "probe-certificate.py",
    "laws-check-new.py",
    "audit-static.py",
    "audit-static2.py",
    "fetch-new.py",
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


# --- 0. Verify the base branch tip, then re-derive the entry in memory.
st, ref = call("GET", f"/repos/{REPO}/git/ref/heads/{BASE_BRANCH}")
assert st == 200, f"base ref GET failed: {st} {ref}"
tip = ref["object"]["sha"]
assert tip.startswith(BASE_TIP), f"base tip moved: {tip} (want {BASE_TIP}...)"
print("base branch tip:", tip, flush=True)
st, tip_commit = call("GET", f"/repos/{REPO}/git/commits/{tip}")
assert st == 200, f"tip commit GET failed: {st} {tip_commit}"
base_tree = tip_commit["tree"]["sha"]
print("base tree:", base_tree, flush=True)

spec_b = importlib.util.spec_from_file_location(
    "bcert", HOME + ROUND + "build-certificate.py")
bc = importlib.util.module_from_spec(spec_b)
spec_b.loader.exec_module(bc)
walk_pf, entry_pf = bc.regen_pricing_fix_tip()
h = bc.harvest_identity()
new_entry = bc.apply_certificate(entry_pf, h)
bc.js_syntax_check(new_entry)
assert hashlib.sha256(new_entry.encode()).hexdigest() == STAGED_ENTRY_SHA, \
    f"re-derived entry != staged: {hashlib.sha256(new_entry.encode()).hexdigest()}"
print(f"entry re-derived in memory: {len(new_entry.encode())} B "
      f"sha={STAGED_ENTRY_SHA[:8]}... == staged MATCH", flush=True)

# --- 1. Blobs.
entries = []
local_by_path = {}
for name in DISK_FILES:
    local = HOME + ROUND + name
    raw = open(local, "rb").read()
    assert len(raw) > 0, f"{local} is 0 bytes — STOP (flake damage)"
    repo_path = ROUND + name
    st, blob = call("POST", f"/repos/{REPO}/git/blobs",
                    {"content": base64.b64encode(raw).decode("ascii"),
                     "encoding": "base64"})
    assert st == 201, f"blob POST failed for {repo_path}: {st} {blob}"
    print(f"blob {repo_path}: {blob['sha']} ({len(raw)} B, "
          f"sha256={hashlib.sha256(raw).hexdigest()[:8]}...)", flush=True)
    entries.append({"path": "TEAM-NITRO/" + repo_path, "mode": "100644",
                    "type": "blob", "sha": blob["sha"]})
    local_by_path[repo_path] = raw

raw = new_entry.encode()
repo_path = ROUND + "fixed-entry.html"
st, blob = call("POST", f"/repos/{REPO}/git/blobs",
                {"content": base64.b64encode(raw).decode("ascii"),
                 "encoding": "base64"})
assert st == 201, f"blob POST failed for {repo_path}: {st} {blob}"
print(f"blob {repo_path}: {blob['sha']} ({len(raw)} B, "
      f"sha256={hashlib.sha256(raw).hexdigest()}) [in-memory bytes]", flush=True)
entries.append({"path": "TEAM-NITRO/" + repo_path, "mode": "100644",
                "type": "blob", "sha": blob["sha"]})
local_by_path[repo_path] = raw

# --- 2. Tree + commit (parent = base tip).
st, tree = call("POST", f"/repos/{REPO}/git/trees",
                {"base_tree": base_tree, "tree": entries})
assert st == 201, f"tree POST failed: {st} {tree}"
print("tree:", tree["sha"], flush=True)

msg = ("Pricing Certificate Current round (2026-11-17): /free now shows "
       "the CURRENT certificate, harvested verbatim from the identity "
       "treatment (identity-fixed.html 8c641f96...): trophy name (obsidian "
       "gradient, chrome stroke, purple clone, hover lift, settle), "
       "obsidian Smart Link / Mail ID panels with typed values, white "
       "tokens (zero #f2f2f6 / #a8dcff / #ffd97a / #163a56 / #3a2a09), "
       "official agreement sentence + 9-paragraph reader (hidden on "
       "certified/taken), taken text-shadow none. Geometry kept. "
       "FIXED in this round: the first staging shipped the reader IIFE "
       "as }(); (missing paren) — a JS syntax error killing the whole "
       "inline block; the build now appends )(); with a byte-identity "
       "assert and a no-skip vm.Script syntax check. Entry 332,182 B, "
       "sha 1e1bb489... staged on naya-pricing-free-staging only; "
       "pricing v78 untouched; walk unchanged. Live browser probe OWED "
       "(VM browsers dead — Chromium SIGTRAP, Firefox SIGSEGV); probe "
       "script filed, alias certcurrent reserved, none claimed. Maker "
       "report + build/probe/audit scripts.")
st, commit = call("POST", f"/repos/{REPO}/git/commits",
                  {"message": msg, "tree": tree["sha"], "parents": [tip]})
assert st == 201, f"commit POST failed: {st} {commit}"
commit_sha = commit["sha"]
print("commit:", commit_sha, flush=True)

# --- 3. CREATE the new branch ref at the commit.
st, ref = call("POST", f"/repos/{REPO}/git/refs",
               {"ref": f"refs/heads/{BRANCH}", "sha": commit_sha})
assert st == 201, f"ref CREATE failed: {st} {ref}"
print("ref:", ref["ref"], "->", ref["object"]["sha"], flush=True)

st, ref2 = call("GET", f"/repos/{REPO}/git/ref/heads/{BRANCH}")
assert st == 200 and ref2["object"]["sha"] == commit_sha, "ref verify FAILED"
for repo_path in local_by_path:
    sha = [e["sha"] for e in entries
           if e["path"] == "TEAM-NITRO/" + repo_path][0]
    st, blob = call("GET", f"/repos/{REPO}/git/blobs/{sha}")
    assert st == 200, f"blob read-back failed for {repo_path}: {st}"
    decoded = base64.b64decode(blob["content"])
    want = local_by_path[repo_path]
    assert decoded == want, f"blob read-back MISMATCH for {repo_path} — STOP"
    print(f"blob read-back MATCH {repo_path} sha256="
          f"{hashlib.sha256(decoded).hexdigest()}", flush=True)
print(f"FILED: branch={BRANCH} commit={commit_sha} blobs={len(entries)}",
      flush=True)

# --- 4. Open the PR (base main, unmerged).
st, pr = call("POST", f"/repos/{REPO}/pulls",
              {"title": "Pricing Certificate Current — /free shows the current certificate (2026-11-17)",
               "head": BRANCH, "base": "main",
               "body": ("Brings the staging `/free` certificate to the CURRENT "
                        "treatment (identity 8c641f96...): trophy name, obsidian "
                        "panels, white tokens, agreement sentence + reader. "
                        "Includes the fix for a JS syntax error the first "
                        "staging shipped (reader IIFE `}();` → `})();`).\n\n"
                        "Staged on naya-pricing-free-staging only "
                        "(entry 332,182 B, sha 1e1bb489...); pricing v78 "
                        "untouched; walk unchanged.\n\n"
                        "NOT YET PROVEN: the live browser probe (1920 + 390, "
                        "fresh alias `certcurrent`) — VM browsers dead "
                        "(Chromium SIGTRAP, Firefox SIGSEGV). Probe script "
                        "filed in the round directory; checker to run via "
                        "the cloud browser route.\n\n"
                        "DO NOT MERGE — staging verification only.")})
assert st == 201, f"PR CREATE failed: {st} {pr}"
print(f"PR OPEN: #{pr['number']} {pr['html_url']} (unmerged)", flush=True)
print(f"PR: number={pr['number']} url={pr['html_url']} state={pr['state']}", flush=True)
