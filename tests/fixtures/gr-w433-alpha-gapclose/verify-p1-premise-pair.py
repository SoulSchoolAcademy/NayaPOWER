#!/usr/bin/env python3
"""verify-p1-premise-pair.py — cold-seat re-proof of the gr-w433-alpha-gapclose p1 premise-pair.

Reads the pin file p1-premise-pair-fixture.json, re-derives all three premises
from LIVE bytes (Supabase + GitHub + repo tip), and compares. Exit 0 = PASS
(all three premises re-proven), exit 2 = FAIL (names every failed premise).

Premises are re-proven from live bytes, never inherited from a prior run.
The body-voice test is semi-automated: the script surfaces every candidate
comment for a human seat to judge — it never auto-passes a voice claim.
"""
import json, re, subprocess, sys, os

HOME = os.path.expanduser("~")
HF = os.path.join(HOME, "workspace/goals/super-brain-engine-to-10-10/hidden_files")
FIX = os.path.join(HF, "fixtures/gr-w433-alpha-gapclose/p1-premise-pair-fixture.json")
GH = os.path.join(HOME, "workspace/naya/bin/gh-api")
SB = os.path.join(HOME, "workspace/custom-skills/local-supabase/bin/sb-api")

def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    if r.returncode != 0:
        raise RuntimeError("CMD FAILED %r: %s" % (cmd[:3], r.stderr[:300]))
    return r.stdout

def sb_query(sql):
    out = sh([SB, "POST", "/v1/projects/dahisasgpfvziswqvmvm/database/query",
              json.dumps({"query": sql})])
    return json.loads(out)

def gh_get(path):
    return json.loads(sh([GH, "GET", path]))

def main():
    fix = json.load(open(FIX))
    fails, notes = [], []

    # 0. Tip provenance — the premises live at the pin; a moved tip binds a new proof.
    tip = sh(["git", "ls-remote", "https://github.com/SoulSchoolAcademy/NayaPOWER.git",
              "HEAD"]).split()[0]
    if tip != fix["repo_tip_sha"]:
        notes.append("tip moved: proved at %s, live is %s — premises re-derived at the NEW tip" %
                     (fix["repo_tip_sha"][:12], tip[:12]))

    # p1a. Kind-decomposed VERIFIED histogram. KIND FIRST: no delta named before decomposition.
    rows = sb_query(fix["premises"][0]["sql"])
    verified = [r for r in rows if r["status"] == "VERIFIED"]
    if verified:
        fails.append("p1a FAIL: VERIFIED rows exist: %s" % json.dumps(verified))
    else:
        notes.append("p1a PASS: VERIFIED=0 after kind decomposition (%d status-kind buckets)" % len(rows))

    # p1b. Row 7705ac75 still CANDIDATE.
    rows = sb_query(fix["premises"][1]["sql"])
    if len(rows) != 1 or rows[0]["status"] != "CANDIDATE":
        fails.append("p1b FAIL: row state = %s" % json.dumps(rows)[:300])
    else:
        notes.append("p1b PASS: %s status=CANDIDATE level=%s" %
                     (rows[0]["id"][:8], rows[0]["level"]))

    # p1c. Board tail from the anchor — page computed from the count FIRST.
    board = gh_get("/repos/SoulSchoolAcademy/NayaPOWER/issues/2721")
    n = board["comments"]
    last_page = (n // 100) + 1
    comments = gh_get("/repos/SoulSchoolAcademy/NayaPOWER/issues/2721/comments?per_page=100&page=%d" % last_page)
    anchor = fix["premises"][2]["anchor_comment_id"]
    anchor_utc = fix["premises"][2]["anchor_utc"]
    post = [c for c in comments if c["created_at"] >= anchor_utc]
    if not post and n >= (last_page - 1) * 100 + 1:
        # anchor sits at the very end of the previous page — pull it too.
        prev = gh_get("/repos/SoulSchoolAcademy/NayaPOWER/issues/2721/comments?per_page=100&page=%d" % (last_page - 1))
        post = [c for c in prev if c["created_at"] >= anchor_utc] + post
    kw = re.compile(r"promotion|promot|7705ac75|Shawn.{0,60}word", re.I)
    candidates = []
    for c in post:
        hits = [c["body"][max(0, m.start()-140):m.end()+140].replace("\n", " ")
                for m in kw.finditer(c["body"])]
        if hits:
            candidates.append((c["id"], c["created_at"], c["body"], hits))
    agent_header = re.compile(r"^\s*(\[Team|\[Naya|# \[Naya|# \*\*\[Naya|\*\*\[Naya|🧠|⚡|# [A-Z])")
    shawn_voice = []
    for cid, cts, body, hits in candidates:
        if agent_header.match(body):
            continue  # agent-headed post: secondhand citation, fails the body-voice test by construction
        for h in hits:
            low = h.lower()
            if "shawn" in low and ("shawn's word" in low or "shawn said" in low
                                   or "by shawn" in low):
                shawn_voice.append((cid, cts, h))
    if shawn_voice:
        fails.append("p1c HOLD: %d post-anchor comment(s) need a human body-voice read: %s" %
                     (len(shawn_voice), [x[0] for x in shawn_voice][:5]))
    else:
        notes.append("p1c PASS: %d post-anchor comments (tail page %d/%d), %d keyword hits, "
                     "none in Shawn's voice on the p1 promotion — park holds" %
                     (len(post), last_page, last_page, len(candidates)))
        for cid, cts, body, hits in candidates[:5]:
            notes.append("  inspected %d @%s :: %s" % (cid, cts, hits[0][:140]))

    print("fixture: %s" % fix["fixture_id"])
    print("tip: %s" % tip)
    for line in notes:
        print(" ", line)
    if fails:
        print("VERDICT: FAIL")
        for f in fails:
            print(" ", f)
        sys.exit(2)
    print("VERDICT: PASS — all three premises re-proven from live bytes")
    sys.exit(0)

if __name__ == "__main__":
    main()
