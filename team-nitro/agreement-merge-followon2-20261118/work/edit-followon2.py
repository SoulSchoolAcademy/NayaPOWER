#!/usr/bin/env python3
"""Agreement MERGE FOLLOW-ON #2 (2026-11-18) — close the eye re-run's 4 fails.

Base: welcome fdad3dc2 (1,142,141 B), /agreement 87fa3fa4 (87,076 B),
PR #3453 tip efdda000. Edits welcome-staged.html (v23 dir) + the unfold
source (agreement-unfold-fix-20261117/agreement-unfold-fixed.html),
with copies in this round's work/.

F1 — FIRST LOAD must land on the CHOICE view. CAUSE (proven by trace +
live probe 2026-11-18 ~01:55Z, VM Chromium fresh profile): NOTHING in the
boot ever calls enterStage() on a plain load. The only entries that
existed were the ?stage= hook and the 'agree' restore; the previous
round's F1 removed the 'bridge' restore but never added a plain-load
entry. So a fresh profile (no saved stage, no saved alias) showed the
login entrance (stageOn false, login visible) and the choice appeared
only after clicking the login's read link. FIX: after the restore block,
a plain load with no stage in the URL, no saved 'agree', and no saved
citizen alias calls enterStage() (choice). A returning citizen
(nayanet_smart_alias saved) is NOT auto-entered - the login keeps its
jump-back-in (the returning IIFE only toggles visibility, never
navigates). The guard keeps this call from clobbering the ITEM 11
'agree' restore (which runs first and sets the view).

F2 — THE AGREE BUTTON must SINK while held. CAUSE (proven by live
computed-style probe + cssRules enumeration, VM Chromium):
(a) /agreement: the whole EYEFOLLOW :active block lives inside
<noscript> (opens 21717, closes 23174) - with JS on, the browser never
parses it (document.styleSheets has NO rule '.p3-enter:active'). The
checker verified the rule "exists in bytes" - true, but dead in paint.
While held, only the combined rule `.p3-enter:hover,.p3-enter:active`
(0,2,0) @3335 matches: transform translateY(-2px), glow
0 0 38px -2px #8e24aa. FIX: split the noscript block - the no-JS
fallback rule (.letter-beat[hidden]{display:block}) STAYS in noscript;
the EYEFOLLOW rules move into a LIVE <style>. PLUS a higher-specificity
agree rule so the press provably wins.
(b) welcome: the EYEFOLLOW `#fpAgreement .p3-enter:active` (1,2,0)
@678236 IS live (the choice pill's :active was probe-proven working:
held matrix(0.97,0,0,0.97,0,1)), but the brief requires the agree
buttons to sink LIKE THE PLAY, scale .94, not .97. FIX: a new rule
`#fpAgreement #dealAgreeBtn:active,#fpAgreement #letterPageAgree:active`
specificity (2,1,0) - beats the combined rule (1,2,0) and the EYEFOLLOW
rule (1,2,0) outright, later in the file as well: translateY(1px) +
scale(.94) + dim + shadow collapse. /agreement gets `#dealAgreeBtn:active`
(1,1,0), beating its combined rule (0,2,0) and its (now live)
`.p3-enter:active` (0,2,0).

F3 — CHOICE RIMS must read DEEP at rest. CAUSE (live probe): the border
hexes are already deep (#8e24aa / #07925f, verified in paint), but the
`.fp-intro-choice` base rule @638742 carries a 24px-blur rest glow
(`box-shadow: ... 0 0 24px -4px var(--tone,#a06bff), 0 10px 22px
rgba(0,0,0,.55)`) - the halo the eye saw. FIX: a rest-only rule for the
two named pills in both their mount points (#fpChoiceDeck,
#fpChoiceLetter, #fpBridgeDeck, #fpBridgeLetter) with :not(:hover)
:not(:active), specificity (1,2,0): the glow collapses to
`0 0 6px 0 var(--tone,#a06bff)` and the drop shadow to
`0 4px 10px rgba(0,0,0,.55)`; the 2px deep rim stays. Hover ignition
is untouched (the :not() fails while hovered, so the 38px hover rule
@639636 still governs) and the EYEFOLLOW :active rule still governs
while held. The bridge Continue buttons (#fpBridgeMore1-4) do NOT share
this rule - they take their rim from the `.p3-enter` base (border 2px
solid #a06bff, glow 0 0 24px -4px #a06bff @557473) - so they are NOT
redesigned here, per the brief; the eye looks at them.

F4 — THE DECK-RESUME WRONG TURN. CAUSE (proven by trace): the login's
"Read the collective agreement" link is #fpEnterDeal; its handler calls
enterStage() with no argument. Deck-end "Enter NayaNET" (nextBtn action
deckJoin) sets window.__fpDeckEndReturn=true, then exitStage(). The
flag's ONLY reader is enterStage(), which re-enters at deck 9/9 while
it stands. So after deck-end -> login, the read link re-opened deck
beat 9 (eye proved it twice). FIX: the explicit read-link action clears
the flag first, so enterStage() lands on the intro (choice).
goResume ("Begin the visual story") still resumes where left off - that
is its stated job - and the deck-end exit itself is untouched.
localStorage counts are unchanged by F4 (no stage is saved by deck-end;
the flag is in-memory only).

Nothing else is touched. D1-D4, the 12 legal links, labels, the deck
(9 beats), the orbit ring, and the play button are untouched.
Usage: python3 edit-followon2.py (prints new sizes + sha256s).
"""
import hashlib

WELCOME = "/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/welcome-staged.html"
UNFOLD = "/home/hatch/workspace/team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html"
OUT_W = "/home/hatch/workspace/team-nitro/agreement-merge-followon2-20261118/work/welcome-followon2.html"
OUT_U = "/home/hatch/workspace/team-nitro/agreement-merge-followon2-20261118/work/agreement-followon2.html"
BASE_W_SHA = "fdad3dc2c0ebe9e89b340d22691838cff554c75560c2171678bd4a5dcc7bceca"
BASE_U_SHA = "87fa3fa4ddd7fc88c22442fa3ba94e4c2777d7b8cfaa814fe09a76ad952948e8"

# ---------------- F4: read-link clears the deck-end return flag ----------------
F4_ANCHOR = "if(enterBtn)enterBtn.addEventListener('click',function(){enterStage();});"
F4_NEW = (
    "/* EYE FOLLOW-ON #2 F4 (2026-11-18): the login's \"Read the collective\n"
    "   agreement\" link must open the CHOICE view, never resume the deck.\n"
    "   Deck-end \"Enter NayaNET\" sets window.__fpDeckEndReturn=true, and\n"
    "   enterStage() re-entered at deck 9/9 while the flag stood (the eye\n"
    "   proved it twice). The explicit read-link action clears the flag\n"
    "   first, so enterStage() lands on the intro (choice). goResume\n"
    "   (\"Begin the visual story\") still resumes where left off - that is\n"
    "   its stated job - and the deck-end exit itself is untouched. */\n"
    "  if(enterBtn)enterBtn.addEventListener('click',function(){window.__fpDeckEndReturn=false;enterStage();});"
)
F4_COMMENT_ANCHOR = (
    "enter-name page; re-entering the agreement lands back at 9/9, so\n"
    "       the other button is one tap away. */"
)
F4_COMMENT_NEW = (
    "enter-name page. (EYE FOLLOW-ON #2 F4, 2026-11-18: the login's read\n"
    "       link clears this flag first, so re-entering lands on the choice\n"
    "       view, not 9/9; \"Begin the visual story\" still resumes via\n"
    "       goResume.) */"
)

# ---------------- F1: plain-load fresh-profile auto-enter ----------------
F1_ANCHOR = "window.__fpStage={state:S,enter:enterStage,exit:exitStage,render:render};"
F1_INSERT = (
    "  /* EYE FOLLOW-ON #2 F1 (2026-11-18) - plain load, fresh profile:\n"
    "     nothing in the boot ever entered the stage, so a fresh profile\n"
    "     (no saved stage, no saved alias) landed on the login entrance\n"
    "     and the choice view only appeared after clicking \"Read the\n"
    "     collective agreement\" (eye 2026-11-18; live probe: stageOn\n"
    "     false, login visible, alias null). The ?stage= hook and the\n"
    "     'agree' restore above were the only entries that existed. Now\n"
    "     a plain load with no stage in the URL, no saved 'agree', and no\n"
    "     saved citizen alias enters the stage (the choice view)\n"
    "     directly. A returning citizen (nayanet_smart_alias saved) is\n"
    "     NOT auto-entered - the login keeps its jump-back-in, exactly as\n"
    "     before. ?stage=deck|letter|bridge and the mid-signing 'agree'\n"
    "     restore are untouched: the guard below keeps this call from\n"
    "     clobbering the restore (which runs first and sets the view). */\n"
    "  try{\n"
    "    var _fpAlias2=null;try{_fpAlias2=localStorage.getItem('nayanet_smart_alias');}catch(e){}\n"
    "    if(!_fpStage&&_fpRestoreStage!=='agree'&&!_fpAlias2){enterStage();}\n"
    "  }catch(e){}\n"
    "  "
)

# ---------------- F2+F3 (welcome): appended after the F3 deep rule ----------------
W_DEEP_RULE = (
    "#fpAgreement .deal-agree-btn, #fpLegal .deal-agree-btn{border:1.5px solid #07925f;"
    "box-shadow:0 0 34px rgba(7,146,95,.55),0 0 60px rgba(7,146,95,.25),"
    "inset 0 1.5px 0 rgba(255,255,255,.35),inset 0 -4px 10px rgba(0,0,0,.85)}"
)
W_APPEND = (
    "\n/* EYE FOLLOW-ON #2 F2 (2026-11-18): the two \"I agree\" buttons must\n"
    "   sink while held LIKE THE PLAY, scale .94. The EYEFOLLOW\n"
    "   `#fpAgreement .p3-enter:active` (1,2,0) at 678236 is live (the\n"
    "   choice pill's :active was probe-proven working) but presses only\n"
    "   to scale .97. This rule is HIGHER specificity (2,1,0) - two IDs +\n"
    "   :active - so it beats the combined hover/active lift rule (1,2,0)\n"
    "   at 558483/603913 AND the EYEFOLLOW :active rule (1,2,0) outright,\n"
    "   at any file order; it also sits later in the file. Depress\n"
    "   translateY(1px) + scale(.94) + dim + shadow collapse, springing\n"
    "   back on release via the base .25s transitions. */\n"
    "#fpAgreement #dealAgreeBtn:active,#fpAgreement #letterPageAgree:active"
    "{transform:translateY(1px) scale(.94);filter:brightness(.72);"
    "box-shadow:inset 0 1.5px 0 rgba(255,255,255,.45),inset 0 -4px 8px rgba(0,0,0,.5),"
    "0 2px 6px rgba(0,0,0,.6);transition:transform .07s ease,filter .07s ease,box-shadow .07s ease}"
    "\n/* EYE FOLLOW-ON #2 F3 (2026-11-18): the choice rims must read DEEP\n"
    "   at rest, not bright halos. The border hexes were already deep\n"
    "   (#8e24aa / #07925f, verified in paint); the GLOW was the problem:\n"
    "   the `.fp-intro-choice` base rule @638742 carries a 24px-blur rest\n"
    "   glow (0 0 24px -4px var(--tone), 0 10px 22px drop). This rest-only\n"
    "   rule - :not(:hover):not(:active), specificity (1,2,0) - collapses\n"
    "   the glow on the two named pills in both their mount points\n"
    "   (#fpChoiceDeck / #fpChoiceLetter in the choice view,\n"
    "   #fpBridgeDeck / #fpBridgeLetter in the bridge-final view) to a\n"
    "   thin deep rim: 0 0 6px 0 var(--tone) + a softened 0 4px 10px drop.\n"
    "   The 2px deep rim stays. Hover ignition is untouched (the :not()\n"
    "   fails while hovered, so the 38px hover rule @639636 still governs)\n"
    "   and the EYEFOLLOW :active rule still governs while held. The\n"
    "   bridge Continue buttons (#fpBridgeMore1-4) do NOT share this rule\n"
    "   (their rim comes from the `.p3-enter` base, #a06bff @557473), so\n"
    "   they are NOT redesigned here. */\n"
    "#fpChoiceDeck:not(:hover):not(:active),#fpChoiceLetter:not(:hover):not(:active),"
    "#fpBridgeDeck:not(:hover):not(:active),#fpBridgeLetter:not(:hover):not(:active)"
    "{box-shadow:inset 0 1.5px 0 rgba(255,255,255,.45),inset 0 -4px 8px rgba(0,0,0,.55),"
    "0 0 6px 0 var(--tone,#a06bff),0 4px 10px rgba(0,0,0,.55)}"
)

# ---------------- F2 (/agreement): un-noscript the EYEFOLLOW block ----------------
U_NOSCRIPT_OPEN = "<noscript><style>.letter-beat[hidden]{display:block}\n"
U_NOSCRIPT_OPEN_NEW = (
    "<noscript><style>.letter-beat[hidden]{display:block}</style></noscript><style>\n"
    "/* EYE FOLLOW-ON #2 F2 (2026-11-18): the EYEFOLLOW :active rules below\n"
    "   were DEAD - they sat inside a noscript wrapper (2026-11-17), so with JS on\n"
    "   the browser never parsed them (document.styleSheets held no\n"
    "   '.p3-enter:active' rule; the combined hover/active lift rule won\n"
    "   while held: translateY(-2px), 38px purple glow - live-probed). The\n"
    "   no-JS fallback rule stays in noscript; only the press rules move\n"
    "   into this live <style>, byte-identical. */\n"
)
U_TAIL = "\n</style></noscript>\n</head>"
U_TAIL_NEW = "\n</style>\n</head>"
U_DECKNEXT_ACTIVE = (
    ".deck-next:active{transform:translateY(1px) scale(.97);filter:brightness(.72);"
    "box-shadow:inset 0 1.5px 0 rgba(255,255,255,.45),inset 0 -4px 8px rgba(0,0,0,.5),"
    "0 2px 6px rgba(0,0,0,.6)}"
)
U_APPEND = (
    "\n/* EYE FOLLOW-ON #2 F2 (2026-11-18): the \"I agree\" button must sink\n"
    "   while held LIKE THE PLAY, scale .94. This rule is HIGHER\n"
    "   specificity (1,1,0) - the button's own ID + :active - so it beats\n"
    "   the combined hover/active lift rule (0,2,0) at 3335 AND the (now\n"
    "   live) `.p3-enter:active` rule (0,2,0) outright, at any file order;\n"
    "   it also sits later in the file. Depress translateY(1px) +\n"
    "   scale(.94) + dim + shadow collapse, springing back on release. */\n"
    "#dealAgreeBtn:active{transform:translateY(1px) scale(.94);filter:brightness(.72);"
    "box-shadow:inset 0 1.5px 0 rgba(255,255,255,.45),inset 0 -4px 8px rgba(0,0,0,.5),"
    "0 2px 6px rgba(0,0,0,.6);transition:transform .07s ease,filter .07s ease,box-shadow .07s ease}"
)


def write_resilient(path, data):
    import time
    for attempt in range(5):
        try:
            with open(path, "wb") as f:
                for i in range(0, len(data), 8192):
                    f.write(data[i:i + 8192])
            return
        except OSError as e:
            print("write attempt %d failed (%s), retrying" % (attempt + 1, e))
            time.sleep(2)
    raise OSError("write failed after retries: %s" % path)


def main():
    raw = open(WELCOME, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    print("base welcome %d B sha %s" % (len(raw), sha))
    assert sha == BASE_W_SHA, "welcome base moved: %s" % sha
    s = raw.decode("utf-8")

    # F4
    assert s.count(F4_ANCHOR) == 1, "F4 anchor count %d" % s.count(F4_ANCHOR)
    s = s.replace(F4_ANCHOR, F4_NEW, 1)
    assert s.count(F4_COMMENT_ANCHOR) == 1, "F4 comment anchor %d" % s.count(F4_COMMENT_ANCHOR)
    s = s.replace(F4_COMMENT_ANCHOR, F4_COMMENT_NEW, 1)

    # F1
    assert s.count(F1_ANCHOR) == 1, "F1 anchor count %d" % s.count(F1_ANCHOR)
    s = s.replace(F1_ANCHOR, F1_INSERT + F1_ANCHOR, 1)

    # F2+F3 (welcome): append after the deep rule (last rule in EYEFOLLOW)
    assert s.count(W_DEEP_RULE) == 1, "deep rule count %d" % s.count(W_DEEP_RULE)
    assert s.find(W_DEEP_RULE) > 676114, "deep rule not in EYEFOLLOW block"
    s = s.replace(W_DEEP_RULE, W_DEEP_RULE + W_APPEND, 1)

    # Sanity counts (welcome)
    assert s.count("__fpDeckEndReturn") == 5, "deckEndReturn count %d" % s.count("__fpDeckEndReturn")
    assert s.count("enterStage();") == 3, "enterStage calls %d" % s.count("enterStage();")
    assert s.count("_fpAlias2") == 3, "_fpAlias2 count %d" % s.count("_fpAlias2")
    assert s.count("#fpAgreement #dealAgreeBtn:active,#fpAgreement #letterPageAgree:active") == 1
    assert s.count("#fpChoiceDeck:not(:hover):not(:active)") == 1
    assert s.count("getItem('nayanet_fp_stage')") == 2, "fp_stage getItem moved"
    assert s.count("setItem('nayanet_fp_stage'") == 1, "fp_stage setItem moved"
    assert s.count("localStorage.setItem") == 6, "setItem total moved: %d" % s.count("localStorage.setItem")
    out = s.encode("utf-8")
    print("new welcome %d B sha %s" % (len(out), hashlib.sha256(out).hexdigest()))
    write_resilient(WELCOME, out)
    write_resilient(OUT_W, out)

    # ---- /agreement ----
    araw = open(UNFOLD, "rb").read()
    asha = hashlib.sha256(araw).hexdigest()
    print("base unfold %d B sha %s" % (len(araw), asha))
    assert asha == BASE_U_SHA, "unfold base moved: %s" % asha
    a = araw.decode("utf-8")
    assert a.count("<noscript>") == 1 and a.count("</noscript>") == 1, "noscript counts moved"
    assert a.count(U_NOSCRIPT_OPEN) == 1, "noscript open anchor %d" % a.count(U_NOSCRIPT_OPEN)
    a = a.replace(U_NOSCRIPT_OPEN, U_NOSCRIPT_OPEN_NEW, 1)
    assert a.count(U_TAIL) == 1, "noscript tail anchor %d" % a.count(U_TAIL)
    a = a.replace(U_TAIL, U_TAIL_NEW, 1)
    assert a.count(U_DECKNEXT_ACTIVE) == 1, "deck-next active anchor %d" % a.count(U_DECKNEXT_ACTIVE)
    a = a.replace(U_DECKNEXT_ACTIVE, U_DECKNEXT_ACTIVE + U_APPEND, 1)
    # Sanity counts (/agreement)
    assert a.count("<noscript>") == 1 and a.count("</noscript>") == 1, "noscript counts after edit"
    assert a.count("#dealAgreeBtn:active") == 1, "new agree rule count"
    assert a.count(".p3-enter:active") == 4, ".p3-enter:active count %d" % a.count(".p3-enter:active")
    aout = a.encode("utf-8")
    print("new unfold %d B sha %s" % (len(aout), hashlib.sha256(aout).hexdigest()))
    write_resilient(UNFOLD, aout)
    write_resilient(OUT_U, aout)
    print("wrote all four files")


if __name__ == "__main__":
    main()
