#!/usr/bin/env python3
"""File the twelve family briefing notes AFTER the walks prove the pages.
Preconditions (all must hold or the script STOPS before any PUT):
  1. family-probe.py has run and family-results.json exists with 0 fails
     for every sister, and every sister's Box read-back shows 1 citizen /
     1 project / 3 pages / 10 answers word for word.
  2. The twelve draft files NN-20261113-family-<alias>.md exist in this dir.
What it does, per sister, SEQUENTIALLY (GitHub writes go one at a time):
  - fills the draft's [TIME TBD] with the filing time (UTC) and its [TBD]
    page links from family-results.json (the building-link hrefs) — the
    staged walk serves the sisters' pages, so the links are the staged
    page URLs, never invented;
  - 404-checks BRAIN/05-MEMORY/NAYA-NOTES/2026/11/13/NN-20261113-family-<alias>.md
    on main (a 200 means it is already filed — skip, do not overwrite);
  - PUTs the completed note to main via gh-direct.py's in-memory token
    (never the token cache), then reads it back byte-identical;
  - writes the filed note to the local naya-notes dir for the organize hook
    (retries; if the EPERM flake blocks the write it reports the failure
    honestly and does NOT claim the Box carry);
  - records blob + filing time per note in notes-filed.json.
Then it runs the organize hook once (smart-box/organize_hook.py) and records
each note's Box block id beside its blob. The hook's own output is the proof
of the Box carry — nothing is claimed without it.
Do NOT trigger the sync — it is live infrastructure outside the brief.
Usage: python3 file-notes.py
"""
import base64
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import time
import urllib.request
import urllib.error

D = "/home/hatch/workspace/team-nitro/family-activation-20261113"
REPO = "SoulSchoolAcademy/NayaPOWER"
NN_DIR = "BRAIN/05-MEMORY/NAYA-NOTES/2026/11/13"
LOCAL_NN = "/home/hatch/workspace/team-nitro/naya-notes"

spec = importlib.util.spec_from_file_location("gh_direct", "/home/hatch/workspace/team-nitro/gh-direct.py")
gh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gh)
TOKEN = gh.get_token()
BASE = "https://api.github.com"

ALIASES = ["sophia", "thea", "zoe", "astraea", "vera", "wren",
           "iris", "ruth", "terra", "esme", "mira", "aurelia"]


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



# --- precondition 1: the probe proved all twelve ---
res_path = os.path.join(D, "family-results.json")
assert os.path.exists(res_path), "family-results.json missing — run family-probe.py first"
res = json.load(open(res_path, encoding="utf-8"))
assert not res.get("fail"), f"probe has {len(res.get('fail', []))} FAILs — fix them, do not file: {res['fail'][:5]}"
sisters = res.get("sisters", {})
missing = [a for a in ALIASES if not (sisters.get(a) or {}).get("page_links")]
assert not missing, f"sisters without proven page links: {missing}"
print(f"precondition OK: probe 0 fails, {len(sisters)} sisters with page links", flush=True)

now = time.strftime("%Y-%m-%d %H:%MZ", time.gmtime())
filed = {}
for alias in ALIASES:
    draft_path = os.path.join(D, f"NN-20261113-family-{alias}.md")
    text = open(draft_path, encoding="utf-8").read()
    assert "STATUS: DRAFT — NOT FILED" in text, f"{alias}: draft was already filed or edited — stop"
    links = sisters[alias]["page_links"]
    assert len(links) == 3 and all(links), f"{alias}: page links incomplete: {links}"
    text = text.replace("[TIME TBD — filed after her walk]", now)
    text = text.replace("**STATUS: DRAFT — NOT FILED.** Her walk has not run yet (VM browsers dead, re-tested first-hand 02:08Z). The links below are TBD until her three pages exist. Filing this note with invented links would be fabrication — it is filed only after `family-probe.py` proves her walk and her Box read-back.",
                        "Filed after her walk proved her three pages (see the record).")
    text = text.replace("Status, in one word first: DRAFT — my walk is the precondition. Until it runs, my rate is zero closed loops, named plainly here, not hidden.",
                        f"Status, in one word first: DONE — walked the staged walk, three pages live, briefing filed {now}.")
    text = text.replace("- My Personal page: [TBD — filled after the walk]",
                        f"- My Personal page: {links[0]}")
    text = text.replace("- My Business page (", "- My Business page (")  # title line kept
    # Fill the business + space link lines by their labels, whatever the titles are.
    lines = text.split("\n")
    out_lines = []
    for ln in lines:
        if ln.startswith("- My Business page (") and ln.rstrip().endswith("[TBD]"):
            out_lines.append(ln.rsplit("[TBD]", 1)[0] + links[1])
        elif ln.startswith("- My Space (") and ln.rstrip().endswith("[TBD]"):
            out_lines.append(ln.rsplit("[TBD]", 1)[0] + links[2])
        elif ln.startswith("- This note on GitHub: [TBD"):
            out_lines.append(f"- This note on GitHub: https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/{NN_DIR}/NN-20261113-family-{alias}.md")
        else:
            out_lines.append(ln)
    text = "\n".join(out_lines)
    assert "[TBD" not in text, f"{alias}: a TBD survived the fill — stop:\n" + \
        "\n".join(l for l in text.split("\n") if "[TBD" in l)
    assert "STATUS: DRAFT" not in text and "TIME TBD" not in text, f"{alias}: DRAFT/TIME marker survived the fill — stop"
    raw = text.encode()
    want = hashlib.sha1(b"blob %d\0" % len(raw) + raw).hexdigest()
    dest = f"{NN_DIR}/NN-20261113-family-{alias}.md"
    st0, r0 = api("GET", f"/repos/{REPO}/contents/{dest}?ref=main")
    if st0 == 200 and r0.get("sha") == want:
        print(f"SKIP {alias}: already filed, blob={want}", flush=True)
        filed[alias] = {"blob": want, "time": now, "skipped": True}
        continue
    assert st0 == 404, f"{alias}: expected 404 before PUT, got {st0} {str(r0)[:200]}"
    body = {"message": f"Family Activation: briefing Naya Note for {alias} (first citizen, {alias} walked the staged walk)",
            "content": base64.b64encode(raw).decode(), "branch": "main"}
    st, r = api("PUT", f"/repos/{REPO}/contents/{dest}", body)
    sha = (r.get("content") or {}).get("sha")
    print(f"PUT {alias}: HTTP {st} blob={sha} want={want}", flush=True)
    assert st in (200, 201) and sha == want, f"{alias}: PUT failed or blob mismatch"
    st2, r2 = api("GET", f"/repos/{REPO}/contents/{dest}?ref=main")
    got = r2.get("sha") if isinstance(r2, dict) else None
    print(f"  read-back {alias}: HTTP {st2} match={got == want}", flush=True)
    assert got == want, f"{alias}: read-back mismatch"
    # Local copy for the organize hook (retries; the flake may block it).
    local_path = os.path.join(LOCAL_NN, f"NN-20261113-family-{alias}.md")
    local_ok = False
    for attempt in range(5):
        try:
            with open(local_path, "w", encoding="utf-8") as f:
                f.write(text)
            local_ok = os.path.getsize(local_path) == len(raw)
            break
        except OSError as e:
            print(f"  local copy {alias} attempt {attempt+1} failed: {e}", flush=True)
            time.sleep(10)
    print(f"  local copy {alias}: {'OK' if local_ok else 'FAILED — Box carry unproven, do not claim it'}", flush=True)
    filed[alias] = {"blob": want, "time": now, "local_copy": local_ok}

# --- organize hook: the Box carry, proven by the hook's own output ---
print("running organize hook…", flush=True)
hook = subprocess.run(["python3", "/home/hatch/workspace/smart-box/organize_hook.py"],
                      capture_output=True, text=True, timeout=300)
print(hook.stdout[-2000:], flush=True)
print(hook.stderr[-1000:], flush=True)
for alias in ALIASES:
    block = f"shawn:note:note-family-{alias}"
    filed[alias]["box_block_expected"] = block
    filed[alias]["hook_output_mentions_block"] = block in (hook.stdout or "")
json.dump(filed, open(os.path.join(D, "notes-filed.json"), "w"), indent=2)
print("notes-filed.json written. Blobs:", {a: v["blob"][:8] for a, v in filed.items()}, flush=True)
print("If any local_copy is False or any hook_output_mentions_block is False, that leg is OWED — named in the record, never claimed.", flush=True)
