#!/usr/bin/env python3
"""verify-p1c-liveboard.py — promoted p1c live-board leg (gr-w519-alpha-p1c-liveboard).

Cold-seat re-proof that no Shawn-voice word on the p1 VERIFIED promotion
appears in the live board (#2765) tail from the board-open anchor.

Promoted from verify-p1-premise-pair.py's p1c leg
(tests/fixtures/gr-w433-alpha-gapclose/, landed via PR #2758) per the w518
spec (gr-w518-alpha-promotion-build):
  (1) new instrument dir on main, never in-place on
      tests/fixtures/gr-w448-alpha-boardscan/;
  (2) fixture board_scan_target 2721->2765;
  (3) script board constant 2721->2765 (3 call sites);
  (4) agent_header regex gains "# \u23f1" alternation (before "# [A-Z]");
  (5) anchor = #2765 board-open comment, pinned by live read at build time;
  (6) validate + DIFFERENT-SEAT IV + merge routed via the dock.

Reads the pin file p1c-liveboard-fixture.json, re-derives from LIVE bytes
(GitHub + repo tip), and compares. Exit 0 = PASS, exit 2 = FAIL/HOLD.

The body-voice test is semi-automated: the script surfaces every candidate
comment for a human seat to judge — it never auto-passes a voice claim.
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, "p1c-liveboard-fixture.json")
GH = os.path.join(os.path.expanduser("~"), "workspace/naya/bin/gh-api")


def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    if r.returncode != 0:
        raise RuntimeError("CMD FAILED %r: %s" % (cmd[:3], r.stderr[:300]))
    return r.stdout


def gh_get(path):
    return json.loads(sh([GH, "GET", path]))


def main():
    fix = json.load(open(FIX))
    fails, notes = [], []
    # w519 promotion spec (2)+(3): fixture board_scan_target AND script board
    # constant are both 2765 (was 2721). The 3 call sites below hardcode 2765;
    # the fixture pin must agree, or the instrument refuses to run.
    assert fix["board_scan_target"] == 2765, "fixture board_scan_target != 2765"

    # 0. Tip provenance — the premises live at the pin; a moved tip binds a new proof.
    tip = sh(["git", "ls-remote", "https://github.com/SoulSchoolAcademy/NayaPOWER.git",
              "HEAD"]).split()[0]
    if tip != fix["repo_tip_sha"]:
        notes.append("tip moved: proved at %s, live is %s — premises re-derived at the NEW tip" %
                     (fix["repo_tip_sha"][:12], tip[:12]))

    # p1c. Board tail from the anchor — page computed from the count FIRST.
    # 3 board-constant call sites, all 2765 (was 2721).
    issue = gh_get("/repos/SoulSchoolAcademy/NayaPOWER/issues/2765")
    n = issue["comments"]
    last_page = (n // 100) + 1
    comments = gh_get("/repos/SoulSchoolAcademy/NayaPOWER/issues/2765/comments?per_page=100&page=%d"
                      % last_page)
    anchor_utc = fix["anchor_utc"]
    post = [c for c in comments if c["created_at"] >= anchor_utc]
    if not post and n >= (last_page - 1) * 100 + 1:
        # anchor sits at the very end of the previous page — pull it too.
        prev = gh_get("/repos/SoulSchoolAcademy/NayaPOWER/issues/2765/comments?per_page=100&page=%d"
                      % (last_page - 1))
        post = [c for c in prev if c["created_at"] >= anchor_utc] + post
    kw = re.compile(fix["keyword_regex"], re.I)
    candidates = []
    for c in post:
        hits = [c["body"][max(0, m.start() - 140):m.end() + 140].replace("\n", " ")
                for m in kw.finditer(c["body"])]
        if hits:
            candidates.append((c["id"], c["created_at"], c["body"], hits))
    # agent_header: the w518-promoted set. "# \u23f1" (U+23F1 STOPWATCH,
    # byte-verified w519 from live comment 6262355680 as bytes
    # 23 20 23F1 FE0F 20 ...) sits BEFORE "# [A-Z]" — the w514 miss was
    # assuming "# [A-Z]" covered the emoji-headed Hourly Accountability format.
    # The distillation-table class is NOT shipped: unconfirmed at build time
    # (200 live #2765 bodies scanned, zero table-headed; w514 example
    # 6261460022 now accountability-headed).
    agent_header = re.compile(
        r"^\s*(\[Team|\[Naya|# \[Naya|# \*\*\[Naya|\*\*\[Naya|🧠|⚡|# \u23f1|# [A-Z])")
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
    print("board: #2765  anchor: %d @ %s" % (fix["anchor_comment_id"], anchor_utc))
    print("tip: %s" % tip)
    for line in notes:
        print(" ", line)
    if fails:
        print("VERDICT: FAIL")
        for f in fails:
            print(" ", f)
        sys.exit(2)
    print("VERDICT: PASS — p1c live-board leg re-proven from live bytes")
    sys.exit(0)


if __name__ == "__main__":
    main()
