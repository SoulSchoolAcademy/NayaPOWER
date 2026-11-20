#!/usr/bin/env python3
"""Agreement MERGE edits (2026-11-17, BRIEF-AGREEMENT-UPDATE-20261117.md).
Edits work/welcome-merged.html (root, base sha 9eea1703) and
work/agreement-merged.html (/agreement, base sha 842cae53).
Every anchor is asserted unique before replacement; the script aborts
on any miss so no partial edit lands. Run: python3 edit-merge.py
"""
import hashlib
import sys

WORK = "/home/hatch/workspace/team-nitro/agreement-update-20261117/work/"
ROOT = WORK + "welcome-merged.html"
AGMT = WORK + "agreement-merged.html"

def rep(h, old, new, expect=1, label=""):
    n = h.count(old)
    assert n == expect, "%s: anchor count %d != %d :: %r" % (label, n, expect, old[:90])
    return h.replace(old, new)

h = open(ROOT, encoding="utf-8").read()
assert hashlib.sha256(h.encode()).hexdigest().startswith("9eea1703"), "root base moved"

# ---- E1: MERGE CSS block, appended at the end of the LAST <style> ----
# (two style blocks exist; the second holds the stage/fp-view rules and
# closes just before </head> - the MERGE block goes there so it wins.)
css = """
/* ==== AGREEMENT MERGE (2026-11-17, BRIEF-AGREEMENT-UPDATE-20261117.md, Shawn 22:19Z) ====
   One choice screen at the root: emblems + title + welcome + play + two
   buttons + legal footer, on one screen. The intro welcome boards are gone
   from the choice view (their byte-identical copy lives on in #fpBridge -
   the citizen reads them once, on the bridge, not twice). The portrait
   moved into the hero, so her face stays on the choice screen. The Royal
   Unfolding header/lines belong to the deck, behind the visual button -
   hidden here, shown in the deck view as before. New in-flow 'Back to the
   login' exits (bridge final + footer) replace the fixed-bar button, so it
   never covers the twelve legal links. Choice pills render at 17px even
   at phone widths (Design Laws 2.3). New buttons hover rim-only (lift +
   rim brighten, no whole-board wash - Shawn 22:28Z) and press in / come
   out (Shawn 22:39Z), as the harvested .fp-intro-choice already does. */
body.fp-stage-on #fpAgreement.fp-view-intro .fp-intro-side{display:block;max-width:860px;margin:0 auto 24px;padding:0 16px;box-sizing:border-box}
body.fp-stage-on #fpAgreement.fp-view-intro #deckUnfold>.letter-steplabel,
body.fp-stage-on #fpAgreement.fp-view-intro #deckUnfold>.deal-title,
body.fp-stage-on #fpAgreement.fp-view-intro #deckUnfold>.deck-sub,
body.fp-stage-on #fpAgreement.fp-view-intro .fp-royal-lines{display:none}
body.fp-stage-on #fpLegal #fpLegalExit{display:none}
body.fp-stage-on #fpLegal.fp-view-footer #fpLegalExit{display:flex}
@media(max-width:480px){.fp-intro-choice{font-size:17px}}
"""
last_style = h.rfind("</style>")
assert last_style > 0 and h[last_style:last_style + 30].startswith("</style>"), "E1 last style close missing"
assert h[last_style - 20:last_style].rstrip().endswith("}"), "E1 last style close not after a rule"
h = h[:last_style] + css + h[last_style:]

# ---- E2: portrait into the hero, above the play button ----
h = rep(h, '<button class="p3-naya-play" id="fpIntroPlay"',
        '<img class="fp-naya-portrait" src="/agmt-b06.png" alt="Naya"><button class="p3-naya-play" id="fpIntroPlay"',
        1, "E2 hero portrait")

# ---- E3: delete the #fpWelcome block (G1-G3 + Continue buttons) ----
s = h.find('<div class="fp-welcome" id="fpWelcome">')
assert s > 0, "E3 fpWelcome start missing"
b = h.find('<div id="fpBridge"', s)
assert b > s, "E3 fpBridge missing after fpWelcome"
# the text just before #fpBridge is: </div> (fpWelcome close) + </div> (fpIntroSide close)
tail = h[b - 80:b]
assert tail.rstrip().endswith("</div>"), "E3 unexpected tail before fpBridge: %r" % tail[-60:]
# fpWelcome close = the second-last </div> before fpBridge
i2 = h.rfind("</div>", 0, b)          # fpIntroSide close
i1 = h.rfind("</div>", 0, i2)          # fpWelcome close
end = i1 + len("</div>")
block = h[s:end]
assert 'id="fpWelcomeG1"' in block and 'id="fpWelcomeG3"' in block, "E3 block missing groups"
assert 'id="fpWelcomeMore1"' in block and 'id="fpWelcomeMore2"' in block, "E3 block missing mores"
assert 'fp-naya-portrait' in block, "E3 block missing portrait (moved to hero first)"
h = h[:s] + h[end:]
assert 'id="fpWelcome"' not in h, "E3 fpWelcome survived"
# (JS keeps null-guarded references to #fpWelcomeG1 / wMore1 / wMore2 -
# placeFaces + Continue wiring both check before use - so only the HTML
# ids must be gone, not the JS mentions.)
assert 'id="fpWelcomeG' not in h, "E3 welcome group ids survived"
assert 'id="fpWelcomeMore' not in h, "E3 welcome more ids survived"
assert 'id="fpBridgeG1"' in h, "E3 bridge groups damaged"
print("E3 deleted fpWelcome block: %d B" % len(block))

# ---- E4: in-flow exit button in the bridge final ----
h = rep(h, 'id="fpBridgeLetter" type="button" style="--tone:#07925f">Read the Collective Agreement &#9670;</button></div>',
        'id="fpBridgeLetter" type="button" style="--tone:#07925f">Read the Collective Agreement &#9670;</button></div><button class="fp-intro-choice fp-bridge-exit" id="fpBridgeExit" type="button" style="--tone:#8e24aa;margin-top:12px">Back to the login &#9670;</button>',
        1, "E4 bridge exit")

# ---- E5: in-flow exit button in the footer flow, after the legal note ----
h = rep(h, '<p class="fp-legal-note">These pages are part of the front page — not a separate site. The agreement above is the record: it stays right here, so you can read it again any time.</p>',
        '<p class="fp-legal-note">These pages are part of the front page — not a separate site. The agreement above is the record: it stays right here, so you can read it again any time.</p><button class="fp-intro-choice fp-legal-exit" id="fpLegalExit" type="button" style="--tone:#a06bff;margin:18px auto 0">Back to the login &#9670;</button>',
        1, "E5 footer exit")

# ---- E6: intro READ choice -> /agreement (one letter destination) ----
h = rep(h, "if(cLetter){cLetter.addEventListener('click',function(){if(S.view==='intro')enterLetterPage();});}",
        "if(cLetter){cLetter.addEventListener('click',function(){if(S.view==='intro')window.location.href='/agreement';});}",
        1, "E6 cLetter")

# ---- E7: intro next-button (nextBtn2) -> /agreement ----
h = rep(h, "if(nextBtn2)nextBtn2.addEventListener('click',function(){if(S.view==='intro'){enterLetterPage();}else if(S.view==='deck'&&S.deck===deckBeats.length-1){window.location.href='/agreement';}});",
        "if(nextBtn2)nextBtn2.addEventListener('click',function(){if(S.view==='intro'){window.location.href='/agreement';}else if(S.view==='deck'&&S.deck===deckBeats.length-1){window.location.href='/agreement';}});",
        1, "E7 nextBtn2")

# ---- E8: enterStage defaults to the INTRO (choice) view ----
h = rep(h, "function enterStage(){", "function enterStage(_t){", 1, "E8a signature")
h = rep(h, "else{S.view='bridge';", "else{S.view=(_t==='bridge')?'bridge':'intro';", 1, "E8b default view")
h = rep(h, "enterStage();if(_fpStage==='deck'){goResume();}else if(_fpStage==='letter'){enterLetterPage();}",
        "enterStage(_fpStage);if(_fpStage==='deck'){goResume();}else if(_fpStage==='letter'){enterLetterPage();}",
        1, "E8c ?stage=")
h = rep(h, "else if(localStorage.getItem('nayanet_fp_stage')==='bridge'){enterStage();}",
        "else if(localStorage.getItem('nayanet_fp_stage')==='bridge'){enterStage('bridge');}",
        1, "E8d resume bridge")

# ---- E9: 'Back to the login' out of the fixed bar ----
h = rep(h, "if(nextBtn2)nextBtn2.hidden=true;",
        "if(nextBtn2)nextBtn2.hidden=true;\n  if(nextBtn)nextBtn.hidden=false;",
        1, "E9a reset")
h = rep(h, "if(S.view==='bridge'){setNext('Back to the login \\u25C6','#a06bff','exit');}",
        "if(S.view==='bridge'){if(nextBtn)nextBtn.hidden=true;}",
        1, "E9b bridge branch")
h = rep(h, "else if(S.view==='footer'){\n      setNext('Back to the login \\u25C6','#a06bff','exit');\n      if(linkToAgree)linkToAgree.hidden=false;\n    }",
        "else if(S.view==='footer'){\n      if(nextBtn)nextBtn.hidden=true;\n      if(linkToAgree)linkToAgree.hidden=false;\n    }",
        1, "E9c footer branch")
assert "setNext('Back to the login" not in h, "E9 fixed-bar login survived"

# ---- E10: wire the two in-flow exit buttons ----
h = rep(h, "if(bLetter){bLetter.addEventListener('click',function(){if(S.view==='bridge')window.location.href='/agreement';});}",
        "if(bLetter){bLetter.addEventListener('click',function(){if(S.view==='bridge')window.location.href='/agreement';});}\n  /* AGREEMENT MERGE (2026-11-17) - 'Back to the login' lives in the flow\n     now (bridge final + footer), never in the fixed bar over the footer. */\n  var bExit=q('#fpBridgeExit'), fExit=q('#fpLegalExit');\n  if(bExit){bExit.addEventListener('click',function(){cancelAgreeExit();exitStage();});}\n  if(fExit){fExit.addEventListener('click',function(){cancelAgreeExit();exitStage();});}",
        1, "E10 exit wiring")

open(ROOT, "w", encoding="utf-8").write(h)
print("root written: %d B sha %s" % (len(h.encode()), hashlib.sha256(h.encode()).hexdigest()[:12]))

# ================= /agreement =================
a = open(AGMT, encoding="utf-8").read()
assert hashlib.sha256(a.encode()).hexdigest().startswith("842cae53"), "agreement base moved"
old_url = 'window.location.href = "https://naya-proof-host.nayapower.workers.dev/?file=team-nitro/walk-v23-assembly-20261114/welcome-staged.html&ref=front-page/visual-agreement-end-20261116#userName";'
assert a.count(old_url) == 1, "A1 proof-host destination count != 1"
a = a.replace(old_url,
    '// AGREEMENT MERGE (2026-11-17): the agree button returns to the bridge\n    // on this worker - the proof-host welcome-staged.html is never a\n    // destination (BRIEF-AGREEMENT-UPDATE-20261117.md).\n    window.location.href = "/?stage=bridge";')
assert "naya-proof-host.nayapower.workers.dev/?file=team-nitro/walk-v23-assembly-20261114/welcome-staged.html&ref=front-page" not in a, "A1 destination survived"
open(AGMT, "w", encoding="utf-8").write(a)
print("agreement written: %d B sha %s" % (len(a.encode()), hashlib.sha256(a.encode()).hexdigest()[:12]))
print("ALL EDITS APPLIED")
