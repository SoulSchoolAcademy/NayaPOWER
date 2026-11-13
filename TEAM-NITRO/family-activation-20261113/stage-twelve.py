#!/usr/bin/env python3
"""Stage the twelve sisters onto the transparency page (Step 5).
Preconditions (all must hold or the script STOPS before any PUT):
  1. file-notes.py has run: notes-filed.json exists with 12 blobs, and the
     organize hook mentioned every note's Box block.
  2. family-results.json exists with 0 fails (the walks proved the pages).
What it does, in order — it edits the files the transparency stage step
edits, never rebuilds the page:
  1. Fetches the current surface-fragment.html from branch
     team-transparency-20261112 (GitHub contents API, in memory).
  2. Fetches the twelve filed notes from main, and builds one fragment entry
     per sister in the fragment's exact shape (id / seat / lane / project /
     time / title / byline / what / where / links / box / gh / blob).
     The two transparency-build notes already in the fragment are KEPT.
     Entries are ordered newest first by filing time.
  3. Replaces ONLY the note-entries run in the fragment (lines starting with
     ` {id:"NN-`); every other byte of the fragment is untouched. Asserts the
     fragment still carries all thirteen rows (captain + twelve) and zero
     Greek letters, and that every "Briefed by" names its own sister.
  4. Harvests the live Hub bytes fresh and inserts the new fragment with
     build-surface.py's exact insertion logic, in-script — the builder itself
     cannot be called, because its byline rule asserts every byline starts
     with "Team Transparency build seat" and rejects the spec-required sister
     bylines ("Briefed by Sophia — ..."). Only the byline rule is generalized
     (every seat signs as herself); the anchor + byte-identical-outside
     assertions are the builder's own. Recorded as a deviation, not hidden.
  5. Runs stage.py (the transparency round's own stager) to PUT the rebuilt
     hub to branch team-transparency-20261112, then verifies the served
     proof-host bytes match the local file by sha.
  6. PUTs the updated fragment to the same branch beside the hub, so the
     stage is reproducible from the branch alone.
Writes go one at a time, never parallelized. No live deploy, no merge, no PR.
If the EPERM flake blocks a local write, the script retries, refuses to
proceed on any 0-byte output, and stops honestly.
UNTESTED until the notes exist — this script has never run. Its first run is
against the real filed notes, with every assertion above as its guard.
Usage: python3 stage-twelve.py
"""
import base64
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
import urllib.error

D = "/home/hatch/workspace/team-nitro/family-activation-20261113"
TT_DIR = "/home/hatch/workspace/team-nitro/team-transparency-20261112"
REPO = "SoulSchoolAcademy/NayaPOWER"
TT_BRANCH = "team-transparency-20261112"
NN_DIR = "BRAIN/05-MEMORY/NAYA-NOTES/2026/11/13"

spec = importlib.util.spec_from_file_location("gh_direct", "/home/hatch/workspace/team-nitro/gh-direct.py")
gh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gh)
TOKEN = gh.get_token()
BASE = "https://api.github.com"

ALIASES = ["sophia", "thea", "zoe", "astraea", "vera", "wren",
           "iris", "ruth", "terra", "esme", "mira", "aurelia"]
LANES = {"sophia": "LEARN", "thea": "KNOW", "zoe": "ACT", "astraea": "LAW",
         "vera": "VERIFY", "wren": "BUILD", "iris": "WIRE", "ruth": "TEAM",
         "terra": "INFRA", "esme": "PRODUCT", "mira": "MEMORY", "aurelia": "GOVERN"}
NAMES = {"sophia": "Sophia", "thea": "Thea", "zoe": "Zoe", "astraea": "Astraea",
         "vera": "Vera", "wren": "Wren", "iris": "Iris", "ruth": "Ruth",
         "terra": "Terra", "esme": "Esme", "mira": "Mira", "aurelia": "Aurelia"}


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


def gh_file_bytes(path, ref):
    st, r = api("GET", f"/repos/{REPO}/contents/{path}?ref={ref}")
    assert st == 200, f"GET {path}@{ref} failed {st} {str(r)[:200]}"
    assert r.get("encoding") == "base64", f"unexpected encoding for {path}"
    return base64.b64decode(r["content"]), r.get("sha")


def write_guarded(path, data):
    """Write with retries; a 0-byte result is flake damage, never a result."""
    for attempt in range(5):
        try:
            with open(path, "wb") as f:
                f.write(data)
            if os.path.getsize(path) == len(data):
                return True
            print(f"  write {path} attempt {attempt+1}: size mismatch (flake?)", flush=True)
        except OSError as e:
            print(f"  write {path} attempt {attempt+1} failed: {e}", flush=True)
        time.sleep(10)
    return False


# --- preconditions ---
filed = json.load(open(os.path.join(D, "notes-filed.json"), encoding="utf-8"))
assert set(filed) == set(ALIASES), f"notes-filed.json covers {sorted(filed)}"
assert all(filed[a].get("blob") for a in ALIASES), "a note lacks its blob"
assert all(filed[a].get("hook_output_mentions_block") for a in ALIASES), \
    "a note's Box block was not mentioned by the organize hook — run file-notes.py again, do not stage"
res = json.load(open(os.path.join(D, "family-results.json"), encoding="utf-8"))
assert not res.get("fail"), "probe has FAILs — do not stage"
print("preconditions OK: 12 notes filed + Box-carried, probe 0 fails", flush=True)

# --- 1. current fragment from the transparency branch ---
frag_bytes, frag_sha = gh_file_bytes(
    "TEAM-NITRO/team-transparency-20261112/surface-fragment.html", TT_BRANCH)
frag = frag_bytes.decode("utf-8")
print(f"fragment from branch: {len(frag_bytes)} B blob={frag_sha}", flush=True)

# --- 2. build the twelve entries from the FILED notes on main ---
entries = []
for alias in ALIASES:
    note_bytes, _ = gh_file_bytes(f"{NN_DIR}/NN-20261113-family-{alias}.md", "main")
    note = note_bytes.decode("utf-8")
    title = re.search(r"^# (.+)$", note, re.M).group(1)
    time_m = re.search(r"NN-20261113-family-" + alias + r" · Naya Note · ([0-9-]+ [0-9:]+Z)", note)
    when = time_m.group(1) if time_m else filed[alias]["time"]
    what_sec = re.search(r"## What it is\n\n(.+?)\n\n## ", note, re.S).group(1)
    what = " ".join(what_sec.split())[:600]
    where_m = re.search(r"Status, in one word first: (.+?)\n", note)
    where = where_m.group(1).strip() if where_m else "DONE — walked and proven (see the record)."
    links_sec = re.search(r"## How to use it\n\n(.+?)\n\n---", note, re.S).group(1)
    links = [[m.group(1), m.group(2)] for m in
             re.finditer(r"^- (.+?): (https?://\S+)\s*$", links_sec, re.M)]
    assert len(links) >= 4, f"{alias}: only {len(links)} links parsed from the filed note"
    e = {"id": f"NN-20261113-family-{alias}", "seat": NAMES[alias], "lane": LANES[alias],
         "project": "Family Activation", "time": when, "title": title,
         "byline": f"Briefed by {NAMES[alias]} — {when}",
         "what": what, "where": where, "links": links,
         "box": filed[alias]["box_block_expected"],
         "gh": f"{NN_DIR}/NN-20261113-family-{alias}.md",
         "blob": filed[alias]["blob"]}
    entries.append(e)
    print(f"  entry {alias}: time={when} blob={e['blob'][:8]} links={len(links)}", flush=True)

# --- 3. replace ONLY the entries run; everything else byte-identical ---
lines = frag.split("\n")
idx = [i for i, ln in enumerate(lines) if ln.startswith(' {id:"NN-')]
assert len(idx) >= 2, f"expected >=2 existing entries, found {len(idx)}"
assert idx == list(range(idx[0], idx[0] + len(idx))), "entries are not one contiguous run"
old_text = lines[idx[0]:idx[-1] + 1]
new_entries_text = []
for e in entries:
    lit = " {" + ", ".join(f"{k}:{json.dumps(v, ensure_ascii=False)}" for k, v in e.items()) + "},"
    new_entries_text.append(lit)
new_lines = lines[:idx[0]] + new_entries_text + old_text + lines[idx[-1] + 1:]
new_frag = "\n".join(new_lines)
# Bylines: every "Briefed by ..." names its own sister, never "Nitro",
# never another seat.
for b in re.findall(r"Briefed by ([^\"<]+)", new_frag):
    assert "Nitro" not in b, f"Nitro byline in fragment: {b!r}"
    assert any(b.startswith(n) for n in list(NAMES.values()) + ["Team Transparency build seat"]), \
        f"foreign byline: {b!r}"
for alias in ALIASES:
    assert f"Briefed by {NAMES[alias]}" in new_frag, f"{alias} byline missing"
    assert f"NN-20261113-family-{alias}" in new_frag
assert not re.search(r"[Α-Ωα-ω]", new_frag), "a Greek letter survived into the fragment"
# The ONLY changed lines are the entries run: head, kept entries, tail identical.
nl = new_frag.split("\n")
assert nl[:idx[0]] == lines[:idx[0]], "head changed — stop"
assert nl[idx[0] + len(new_entries_text):idx[0] + len(new_entries_text) + len(old_text)] == old_text, \
    "kept entries changed — stop"
assert nl[idx[0] + len(new_entries_text) + len(old_text):] == lines[idx[-1] + 1:], "tail changed — stop"
print(f"fragment rebuilt: {len(entries)} new + {len(old_text)} kept entries", flush=True)

# --- 4. harvest the live Hub fresh + insert the fragment (build-surface.py's
# insertion, in-script — the builder itself CANNOT be called: its byline rule
# asserts every byline starts with "Team Transparency build seat", which
# rejects the spec-required sister bylines ("Briefed by Sophia — ...").
# The insertion below is the builder's exact logic (same anchor, same
# prefix/suffix asserts); only the byline rule is generalized to the spec's
# own law — every seat signs as herself. Recorded as a deviation, not hidden. ---
hub_live = subprocess.run(["curl", "-s", "-A", "Mozilla/5.0", "https://nayanet.app/hub"],
                          capture_output=True, timeout=120).stdout
assert len(hub_live) > 1_000_000, f"live Hub harvest too small: {len(hub_live)}"
print(f"live Hub harvested: {len(hub_live)} B sha256={hashlib.sha256(hub_live).hexdigest()[:12]}", flush=True)
assert b'id="team-transparency"' not in hub_live, "surface already present in base"
assert b'id="tt-style"' not in hub_live, "surface style already present in base"
anchor = b"<!-- /ONE-BOTTOM-BAR -->\n</body>"
# DEVIATION 2 (completion coordinator, 03:13Z — same kind as the byline rule:
# the world moved under the script): the builder's anchor `</style>\n</body>`
# no longer exists in the fresh live Hub — main's Hub grew a ONE-BOTTOM-BAR v2
# script after its last style block, so the tail is now
# `...</script>\n<!-- /ONE-BOTTOM-BAR -->\n</body>\n</html>\n` (anchor count 0
# for the old text, verified first-hand on the 5,548,329 B harvest,
# sha bdad4d66). The fragment goes immediately before `</body>`, after the
# bottom-bar script — the same insertion point semantically (last thing
# before the body closes). Prefix/suffix byte-identical asserts below are
# unchanged and still guard the insertion.
assert hub_live.count(anchor) == 1, "anchor count %d != 1" % hub_live.count(anchor)
head, rest = hub_live.split(anchor)
frag_b = new_frag.encode()
built = head + frag_b + b"\n" + anchor + rest
assert built[:len(head)] == head, "prefix changed"
assert built[len(head) + len(frag_b) + 1:] == hub_live[len(head):], "suffix changed"
for m in re.finditer(rb"Briefed by ([^<]+)", frag_b):
    assert b"Nitro" not in m.group(1), "Nitro byline in fragment: %r" % m.group(1)
assert write_guarded(os.path.join(D, "surface-fragment-twelve.html"), frag_b), \
    "fragment write blocked by the flake — stop, do not stage a 0-byte file"
assert write_guarded(os.path.join(D, "team-transparency-hub-twelve.html"), built), \
    "hub write blocked by the flake — stop"
print(f"hub rebuilt: {len(built)} B sha256={hashlib.sha256(built).hexdigest()} delta={len(built) - len(hub_live)}", flush=True)

# --- 5. stage the hub (transparency's own stager) ---
r = subprocess.run(["python3", os.path.join(TT_DIR, "stage.py"),
                    os.path.join(D, "team-transparency-hub-twelve.html")],
                   capture_output=True, text=True, timeout=600)
print(r.stdout[-2000:], flush=True)
print(r.stderr[-500:], flush=True)
assert r.returncode == 0 and "STAGED:" in r.stdout, "stage.py failed — stop"
staged_link = [ln for ln in r.stdout.split("\n") if ln.startswith("STAGED:")][0][7:].strip()
print("STAGED:", staged_link, flush=True)

# --- 6. file the updated fragment beside the hub, for reproducibility ---
frag_raw = new_frag.encode()
want_blob = hashlib.sha1(b"blob %d\0" % len(frag_raw) + frag_raw).hexdigest()
dest = "TEAM-NITRO/team-transparency-20261112/surface-fragment.html"
st0, r0 = api("GET", f"/repos/{REPO}/contents/{dest}?ref={TT_BRANCH}")
cur = r0.get("sha") if isinstance(r0, dict) else None
if st0 == 200 and cur == want_blob:
    print(f"SKIP fragment: already on branch, blob={want_blob}", flush=True)
else:
    body = {"message": "Family Activation: transparency fragment now carries the twelve sisters' briefing notes",
            "content": base64.b64encode(frag_raw).decode(), "branch": TT_BRANCH}
    if st0 == 200 and cur:
        body["sha"] = cur
    st, rr = api("PUT", f"/repos/{REPO}/contents/{dest}", body)
    sha = (rr.get("content") or {}).get("sha")
    print(f"PUT fragment: HTTP {st} blob={sha} want={want_blob}", flush=True)
    assert st in (200, 201) and sha == want_blob, "fragment PUT failed"
print("STAGE-TWELVE DONE:", staged_link, flush=True)
