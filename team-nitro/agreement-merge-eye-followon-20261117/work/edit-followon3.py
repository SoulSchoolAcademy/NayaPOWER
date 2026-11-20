#!/usr/bin/env python3
"""Agreement MERGE EYE FOLLOW-ON edits, part 3 (2026-11-17) - carry bridge
presentation fix #2 (D1-D4) into the build, per the coordinator amendment.
Operates on the part-2 output (root sha 37cd0764). The /agreement file is
untouched by D1-D4 (fix2's diff touches only the welcome bytes).

Harvest method: the D3/D4/D2 replacement texts are EXTRACTED VERBATIM from
the fix2 welcome blob (branch walk-end/bridge-presentation-fix2-20261117,
tip 2169da0e, blob 36b0eaa6, 1,134,179 B, sha256 b1d4b16d...) at runtime -
nothing is retyped. The script asserts each old anchor is present exactly
once in my build before replacing it.

D1 stray `}`: ALREADY in my build via the merge round's R10 (same one-brace
   deletion at line 237; stray-brace anchor 0 in mine, 0 in fix2). Verified
   by region comparison, no change made.
D2 stage-restore guard: carried in MECHANISM (the _fpRestoreStage guard line
   verbatim) with ONE adaptation the amendment's own job requires: fix2's
   restore still reads 'bridge', but my F1 removed the 'bridge' save and the
   'bridge' restore (a plain load must never auto-land on the bridge). So
   the carried guard restores ONLY 'agree' (ITEM 11, mid-signing refresh),
   and the comment is adapted to say so. The guard's purpose is fully
   preserved: when the URL carried a stage the hook handled (?stage=deck /
   letter / bridge), the restore stands down instead of dragging the view
   back - which also fixes the ?stage=deck + saved-'agree' race in my build.
D3 corner emblems: carried VERBATIM (desktop top:-76px + comment; phone
   top:-56px + 8px inset). Measured by fix2: 12px/12px/10px clear at
   1920/635/390, 0 overlap, 0 clipping.
D4 legal-footer wrap: carried VERBATIM (stale comment replaced, wrap
   override line deleted). The 13px final-vs-bar overlap at 635/390 is
   PRE-EXISTING (fix2 checker: bar lifts, scroll padding and final layout
   byte-identical to base; bar hidden:true at max scroll) - not redesigned.
F5 NOTE: my part-1 F5 padding (72px / 52px on the bridge head) is REMOVED
   by this script. D3's own comment proves why: the head shrink-wraps to
   its widest child (the title, 482px), so padding would narrow the text
   column D3 was measured in and risks wrapping the title/kicker at 390.
   F5's requirement (title clear of the emblems in every state) is met by
   the harvested D3 itself, measured 10-12px clear with 0 overlap - the
   padding is redundant with D3 carried, not an additional fix.
"""
import hashlib

WORK = "/home/hatch/workspace/team-nitro/agreement-merge-eye-followon-20261117/work/"
ROOT = WORK + "welcome-followon.html"
FIX2 = WORK + "fix2-welcome.html"

def rep(h, old, new, expect=1, label=""):
    n = h.count(old)
    assert n == expect, "%s: anchor count %d != %d :: %r" % (label, n, expect, old[:100])
    return h.replace(old, new)

def write_resilient(path, data, chunk=8192):
    import os, time
    if os.path.exists(path):
        os.remove(path)
    with open(path, "wb") as g:
        off = 0
        while off < len(data):
            piece = data[off:off + chunk]
            done = False
            for attempt in range(40):
                try:
                    g.write(piece); g.flush(); done = True; break
                except PermissionError:
                    time.sleep(5)
            if not done:
                raise IOError("could not write chunk at offset %d after retries" % off)
            off += len(piece)
    print("wrote %s %d B" % (path, len(data)))

h = open(ROOT, encoding="utf-8").read()
assert hashlib.sha256(h.encode()).hexdigest().startswith("37cd0764"), "root part-2 output moved"
f = open(FIX2, encoding="utf-8").read()
assert hashlib.sha256(f.encode()).hexdigest().startswith("b1d4b16d"), "fix2 blob moved"
assert len(f.encode()) == 1134179, "fix2 blob size moved"

def fix2_span(start_anchor, end_anchor):
    i = f.find(start_anchor)
    assert i >= 0, "fix2 anchor missing: %r" % start_anchor[:60]
    j = f.find(end_anchor, i)
    assert j >= 0, "fix2 end anchor missing: %r" % end_anchor[:60]
    return f[i:j + len(end_anchor)]

# ---- D1: verify already present (same deletion as merge R10). ----
assert h.count("}catch(e){} }\n    }\n    var others=") == 0, "D1 stray anchor present in mine"
assert f.count("}catch(e){} }\n    }\n    var others=") == 0, "D1 stray anchor present in fix2"
_sig = "}catch(e){} }\n    var others="
assert h.count(_sig) == 1 and f.count(_sig) == 1, "D1 post-deletion signature not exactly once in both"
print("D1 verified already present (post-deletion signature once in mine and fix2)")

# ---- D3 desktop: old top:-10px pair -> fix2 comment + top:-76px pair. ----
d3_desktop_new = fix2_span(
    "/* ---- BRIDGE PRESENTATION FIX #2 (2026-11-17, D3) ----",
    ".fp-bridge-corner-tr{top:-76px;right:-4px;transform:rotate(20deg)}")
d3_desktop_old = (".fp-bridge-corner-tl{top:-10px;left:-4px;transform:rotate(-20deg)}\n"
                  ".fp-bridge-corner-tr{top:-10px;right:-4px;transform:rotate(20deg)}")
h = rep(h, d3_desktop_old, d3_desktop_new, 1, "D3 desktop")

# ---- D3 phone: old single media line -> fix2 phone block. ----
d3_phone_new = fix2_span(
    "@media(max-width:480px){.fp-bridge-corners .fp-bridge-emblem{width:40px;height:40px}",
    ".fp-bridge-corner-br{right:8px}}")
d3_phone_old = "@media(max-width:480px){.fp-bridge-corners .fp-bridge-emblem{width:40px;height:40px}}"
h = rep(h, d3_phone_old, d3_phone_new, 1, "D3 phone")

# ---- D4: stale §7b comment -> fix2 D4 comment (verbatim). ----
d4_comment_new = fix2_span(
    "/* ---- BRIDGE PRESENTATION FIX #2 (2026-11-17, D4) ----", "*/")
_i = h.find("/* ---- BRIDGE PRESENTATION (2026-11-17, BRIEF-BRIDGE-PRESENTATION-20261117.md")
_j = h.find("*/", _i)
assert _i >= 0 and _j > _i, "D4 old comment anchor missing"
d4_comment_old = h[_i:_j + 2]
assert h.count(d4_comment_old) == 1, "D4 old comment count != 1"
h = h.replace(d4_comment_old, d4_comment_new, 1)
print("D4 comment replaced verbatim")

# ---- D4: wrap override line deleted (verbatim deletion). ----
wrap_old = ("html.fp-locked body.fp-stage-on.fp-bridge #fpLegal .fp-legal-links"
            "{flex-wrap:wrap;justify-content:center;overflow-x:visible}\n")
h = rep(h, wrap_old, "", 1, "D4 wrap override deleted")

# ---- D2: guard carried verbatim; restore agree-only (F1 adaptation). ----
guard_line = fix2_span("var _fpRestoreStage=", ";")
assert guard_line.startswith("var _fpRestoreStage=("), guard_line[:80]
agree_line = fix2_span("if(_fpRestoreStage==='agree')", "render();}")
assert agree_line.startswith("if(_fpRestoreStage==='agree'){enterStage();S.view='agree';S.all=null;render();}"), agree_line[:80]
old_boot = ("  try{\n"
            "    if(localStorage.getItem('nayanet_fp_stage')==='agree'){enterStage();S.view='agree';S.all=null;render();}\n"
            "     /* EYE FOLLOW-ON F1 (2026-11-17) - no 'bridge' auto-restore here:\n"
            "        a plain load must never auto-land on the bridge (State B).\n"
            "        The choice (State A) is what the citizen enters through the\n"
            "        login's 'Read the collective agreement' button, and\n"
            "        ?stage=bridge still opens the bridge by design. */\n"
            "  }catch(e){}")
new_boot = ("  /* BRIDGE PRESENTATION FIX #2 (2026-11-17) — D2, carried with the\n"
            "     eye follow-on F1 adaptation: ?stage=deck never landed, because\n"
            "     this restore block runs after the hook in the same init and\n"
            "     dragged the view back. When the URL carried a stage the hook\n"
            "     handled, the restore stands down (the guard line below, carried\n"
            "     verbatim from fix2). F1's adaptation: only 'agree' is ever\n"
            "     saved or restored now — the 'bridge' save and the 'bridge'\n"
            "     restore are gone, so a plain load never auto-lands on the\n"
            "     bridge (State B); ?stage=bridge still opens it by design. */\n"
            "  try{\n"
            "    " + guard_line + "\n"
            "    " + agree_line + "\n"
            "     /* EYE FOLLOW-ON F1 (2026-11-17) - no 'bridge' auto-restore here:\n"
            "        a plain load must never auto-land on the bridge (State B).\n"
            "        The choice (State A) is what the citizen enters through the\n"
            "        login's 'Read the collective agreement' button, and\n"
            "        ?stage=bridge still opens the bridge by design. */\n"
            "  }catch(e){}")
h = rep(h, old_boot, new_boot, 1, "D2 guard + F1 boot")

# ---- F5: remove my part-1 head padding (D3 carries F5; see header note). ----
h = rep(h, "body.fp-stage-on #fpAgreement.fp-view-bridge .fp-agree-head{padding-left:72px;padding-right:72px}\n",
        "/* F5 (eye follow-on) is carried by the harvested D3 above, not by\n   head padding: the head shrink-wraps to the title (482px), so padding\n   would narrow the text column D3 was measured in and risks wrapping\n   the title/kicker at 390. D3 measures 10-12px clear, 0 overlap. */\n",
        1, "F5 padding removed (desktop)")
h = rep(h, "@media(max-width:480px){body.fp-stage-on #fpAgreement.fp-view-bridge .fp-agree-head{padding-left:52px;padding-right:52px}}\n",
        "", 1, "F5 padding removed (phone)")
# The EYEFOLLOW block comment still describes the padding - correct it.
old_f5_comment = ("   F5 CLEAR (eye E5): in the bridge view the four 56px corner emblems sit\n"
                  "   at the head's edges, so the head's text column is padded 72px each side\n"
                  "   (56px emblem + 16px air) - the kicker and title can never reach an\n"
                  "   emblem. At <=480px the emblems are 40px, so the padding is 52px. The\n"
                  "   corners only ever display in the bridge view, so the padding is scoped\n"
                  "   there and the intro/deck/letter heads are untouched. */")
new_f5_comment = ("   F5 CLEAR (eye E5): carried by the harvested bridge fix #2 D3, not by\n"
                  "   head padding (see the note where the padding rules were): D3 moves\n"
                  "   the top emblems up out of the head (top:-76px, -56px at <=480px)\n"
                  "   and measures 10-12px clear, 0 overlap, 0 clipping at 1920/635/390.\n"
                  "   The emblem glow below went deep with F3 (rgba(142,36,170,.35)). */")
h = rep(h, old_f5_comment, new_f5_comment, 1, "F5 block comment corrected")

write_resilient(ROOT, h.encode())
print("root written: %d B sha %s" % (len(h.encode()), hashlib.sha256(h.encode()).hexdigest()[:12]))
print("ALL PART-3 (D1-D4) EDITS APPLIED")
