#!/usr/bin/env python3
"""Agreement MERGE EYE FOLLOW-ON edits (2026-11-17,
BRIEF-AGREEMENT-MERGE-EYE-FOLLOWON-20261117.md).
Edits work/welcome-followon.html (root, base sha 8aad1e5c) and
work/agreement-followon.html (/agreement, base sha faea2190).
Every anchor is asserted unique before replacement; the script aborts
on any miss so no partial edit lands.

Fixes:
 F1 first load = State A (kill the localStorage 'bridge' hijack; ?stage=bridge
    and deck-end return and the 'agree' refresh-restore are untouched).
 F2 visible press-in on every button (separate :active rules, later in source
    so they beat the shared hover/active lift rules; Anatomy 1.2.8 physics:
    hover rises translateY(-2px), active presses IN translateY(1px) +
    scale(.97) + dim + shadow collapse).
 F3 deep purple/green rims on the choice pills, deck-end pills and
    Keep reading (button-scoped; boards keep their harvested tones).
 F4 legal links open from EVERY stage view (the intro-only gate + the stage
    CSS display:none left bridge-view clicks doing nothing visible);
    bridge openings return to the bridge on close.
 F5 title clear of the corner emblems in the bridge view (head padding).
 +  Alex Walker dup: collapse identities by NORMALIZED alias (spaces and
    punctuation stripped), so 'alexwalker' and 'Alex Walker' can no longer
    render as two rows.
Labels: UNCHANGED (named per arrival in the maker report; the variance is
 the action available in that view).
"""
import hashlib
import sys

WORK = "/home/hatch/workspace/team-nitro/agreement-merge-eye-followon-20261117/work/"
ROOT = WORK + "welcome-followon.html"
AGMT = WORK + "agreement-followon.html"

def rep(h, old, new, expect=1, label=""):
    n = h.count(old)
    assert n == expect, "%s: anchor count %d != %d :: %r" % (label, n, expect, old[:100])
    return h.replace(old, new)

def write_resilient(path, data, chunk=8192):
    """Write bytes in small chunks, retrying each chunk through EPERM flake windows."""
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

# ================= ROOT =================
h = open(ROOT, encoding="utf-8").read()
assert hashlib.sha256(h.encode()).hexdigest().startswith("8aad1e5c"), "root base moved"

# ---- F1a: render() must save ONLY the 'agree' end view. The old branch
# saved 'bridge' on every bridge/deck render, and the boot block below
# restored it on EVERY plain load - so a citizen who had ever visited the
# bridge (or started the deck) reloaded straight into State B and never
# saw the choice again. ----
old_save = ("if(S.view==='agree')localStorage.setItem('nayanet_fp_stage','agree');\n"
            "           else if(S.view==='bridge')localStorage.setItem('nayanet_fp_stage','bridge');\n"
            "           else if(S.view==='deck')localStorage.setItem('nayanet_fp_stage','bridge');\n"
            "          else localStorage.removeItem('nayanet_fp_stage');")
new_save = ("if(S.view==='agree')localStorage.setItem('nayanet_fp_stage','agree');\n"
            "           else localStorage.removeItem('nayanet_fp_stage');\n"
            "           /* EYE FOLLOW-ON F1 (2026-11-17) - the old branch saved\n"
            "              'bridge' on every bridge/deck render, and the boot block\n"
            "              restored it on every plain load, so a reload landed in\n"
            "              State B (the bridge) and the choice was never seen again.\n"
            "              Only the 'agree' end view is ever saved now (ITEM 11 -\n"
            "              a refresh mid-signing still restores the end view).\n"
            "              ?stage=bridge, the deck-end return and the enter-name\n"
            "              button all still land where they are designed to. */")
h = rep(h, old_save, new_save, 1, "F1a save branch")

# ---- F1b: boot block - drop the 'bridge' auto-restore. Keep 'agree'. ----
old_boot = ("if(localStorage.getItem('nayanet_fp_stage')==='agree'){enterStage();S.view='agree';S.all=null;render();}\n"
            "     else if(localStorage.getItem('nayanet_fp_stage')==='bridge'){enterStage('bridge');}")
new_boot = ("if(localStorage.getItem('nayanet_fp_stage')==='agree'){enterStage();S.view='agree';S.all=null;render();}\n"
            "     /* EYE FOLLOW-ON F1 (2026-11-17) - no 'bridge' auto-restore here:\n"
            "        a plain load must never auto-land on the bridge (State B).\n"
            "        The choice (State A) is what the citizen enters through the\n"
            "        login's 'Read the collective agreement' button, and\n"
            "        ?stage=bridge still opens the bridge by design. */")
h = rep(h, old_boot, new_boot, 1, "F1b boot restore")

# ---- F3a: choice pills + footer exit go deep (inline --tone). ----
h = rep(h, 'id="fpChoiceDeck" type="button" style="--tone:#a06bff"',
        'id="fpChoiceDeck" type="button" style="--tone:#8e24aa"', 1, "F3a choice deck")
h = rep(h, 'id="fpChoiceLetter" type="button" style="--tone:#2fe89e"',
        'id="fpChoiceLetter" type="button" style="--tone:#07925f"', 1, "F3a choice letter")
h = rep(h, 'id="fpLegalExit" type="button" style="--tone:#a06bff;margin:18px auto 0"',
        'id="fpLegalExit" type="button" style="--tone:#8e24aa;margin:18px auto 0"', 1, "F3a legal exit")

# ---- F3b: fixed-bar pill tones go deep. setNext is the choke point every
# fixed-bar pill tone passes through (including toneOf(beat) for Keep
# reading), so the map lives there; the nextBtn2 literals change too. ----
h = rep(h, "function setNext(label,tone,act){nextBtn.textContent=label;nextBtn.style.setProperty('--tone',tone);action=act;}",
        "/* EYE FOLLOW-ON F3 (2026-11-17) - the eye's verdict settles the\n"
        "   bright-vs-deep tension in favor of DEEP for the pills: bright\n"
        "   purple/green/teal rims map to their deep palette values here,\n"
        "   the one choke point every fixed-bar pill tone passes through\n"
        "   (choice pills, deck-end pills, Keep reading, I agree, legal).\n"
        "   Other hues pass through unchanged - the page-wide bright base\n"
        "   stays Shawn's ruling, as the merge round left it. */\n"
        "  function deepTone(t){var m={'#a06bff':'#8e24aa','#2fe89e':'#07925f','#40d3bb':'#0e7490'};var k=String(t||'').trim().toLowerCase();return m[k]||t;}\n"
        "  function setNext(label,tone,act){nextBtn.textContent=label;nextBtn.style.setProperty('--tone',deepTone(tone));action=act;}",
        1, "F3b deepTone+setNext")
h = rep(h, "','#a06bff','begin')", "','#8e24aa','begin')", 1, "F3b intro begin")
h = rep(h, "nextBtn2.style.setProperty('--tone','#2fe89e');",
        "nextBtn2.style.setProperty('--tone','#07925f');", 1, "F3b intro nextBtn2")
h = rep(h, "nextBtn2.style.setProperty('--tone','#a06bff');",
        "nextBtn2.style.setProperty('--tone','#8e24aa');", 1, "F3b deck-end nextBtn2")
# 'I agree' green (letter end, letterPage end, agree view) - 3 occurrences
h = rep(h, "'#2fe89e','letterPageAgree'", "'#07925f','letterPageAgree'", 2, "F3b I agree x2")
h = rep(h, "','#2fe89e','agree')", "','#07925f','agree')", 1, "F3b I agree agree-view")
# updateChrome defaults/fallbacks
h = rep(h, "function updateChrome(){\n    var tone='#a06bff';",
        "function updateChrome(){\n    var tone='#8e24aa';", 1, "F3b updateChrome default")
h = rep(h, "tone=p?toneOf(p):'#a06bff';",
        "tone=p?toneOf(p):'#8e24aa';", 1, "F3b legal fallback")

# ---- F4a: legal links open from EVERY stage view. The old gate returned
# early outside intro, so in the bridge view the click did nothing visible:
# wireLegal only flips panel.hidden, and the stage CSS keeps every
# .fp-legal-page display:none until render() sets fp-view-page + fp-now.
# Bridge openings remember to return to the bridge on close. ----
old_legal = ("  legalSec.addEventListener('click',function(e){\n"
             "    if(S.view!=='intro')return;\n"
             "    var b=(e.target&&e.target.closest)?e.target.closest('[data-legal-open]'):null;\n"
             "    if(b){var pid=b.getAttribute('data-legal-open');var lp=q('#legal-'+pid);var lbs=lp?legalBeatsOf(lp):[];var ll=lastShown(lbs);S.view='legal';S.legalId=pid;S.legal=ll>=0?ll:0;S.all=null;render();}\n"
             "  });")
new_legal = ("  legalSec.addEventListener('click',function(e){\n"
             "    var b=(e.target&&e.target.closest)?e.target.closest('[data-legal-open]'):null;\n"
             "    if(b){var pid=b.getAttribute('data-legal-open');var lp=q('#legal-'+pid);var lbs=lp?legalBeatsOf(lp):[];var ll=lastShown(lbs);/* EYE FOLLOW-ON F4 (2026-11-17) - the legal links open from EVERY stage view, not intro only. In the bridge view the old intro-only gate returned early, so the click did nothing visible: wireLegal only flips panel.hidden, and the stage CSS keeps every .fp-legal-page display:none until render() sets fp-view-page + fp-now. A bridge opening remembers to return to the bridge on close; every other view keeps the existing footer return. */window.__fpLegalReturn=(S.view==='bridge')?'bridge':null;S.view='legal';S.legalId=pid;S.legal=ll>=0?ll:0;S.all=null;render();}\n"
             "  });")
h = rep(h, old_legal, new_legal, 1, "F4a legal handler")

# ---- F4b: derive() legal branch - close returns to the remembered view. ----
h = rep(h, "if(!p){S.view='footer';S.all=null;}",
        "if(!p){S.view=(window.__fpLegalReturn||'footer');window.__fpLegalReturn=null;S.all=null;}",
        1, "F4b derive return")

# ---- F5: emblem glow goes deep (the rim-adjacent glow on the corners). ----
h = rep(h, "drop-shadow(0 0 18px rgba(160,107,255,.35))",
        "drop-shadow(0 0 18px rgba(142,36,170,.35))", 1, "F5 emblem glow")

# ---- Alex Walker dup: collapse by NORMALIZED alias (lowercase, spaces and
# punctuation stripped), so 'alexwalker' and 'Alex Walker' are one citizen.
# The old key ('Alex Walker' vs 'alexwalker') let the same name render twice.
# Two genuinely different aliases still stay separate people. ----
h = rep(h, "    var _seenAlias={};\n",
        "    var _normAlias=function(s){return String(s||'').toLowerCase().replace(/[^a-z0-9]/g,'');};\n"
        "    /* EYE FOLLOW-ON (2026-11-17) - the alias key is normalized (spaces\n"
        "       and punctuation stripped): 'alexwalker' and 'Alex Walker' are\n"
        "       the same citizen, not two rows. Two genuinely different\n"
        "       aliases still stay separate people. */\n"
        "    var _seenAlias={};\n", 1, "AW norm helper")
h = rep(h, "var k=String(it.alias).toLowerCase();",
        "var k=_normAlias(it.alias);", 1, "AW filter key")
h = rep(h, "String(it.name).toLowerCase()!==k&&(!_seenAlias[k].name||String(_seenAlias[k].name).toLowerCase()===k)",
        "_normAlias(it.name)!==k&&(!_seenAlias[k].name||_normAlias(_seenAlias[k].name)===k)", 1, "AW name heal")
h = rep(h, "String(it.alias).toLowerCase()===String(alias).toLowerCase()",
        "_normAlias(it.alias)===_normAlias(alias)", 1, "AW cur")
h = rep(h, "String(it.alias).toLowerCase()!==String(alias).toLowerCase()",
        "_normAlias(it.alias)!==_normAlias(alias)", 1, "AW others")
h = rep(h, "String(name).toLowerCase()!==String(alias).toLowerCase()&&(!_cur.name||String(_cur.name).toLowerCase()===String(alias).toLowerCase())",
        "_normAlias(name)!==_normAlias(alias)&&(!_cur.name||_normAlias(_cur.name)===_normAlias(alias))", 1, "AW cur heal")

# ---- EYEFOLLOW CSS block (root): F2 press-in, F3 Keep-reading deep rims,
# F5 head padding. Appended at the end of the LAST <style> so it wins over
# the shared hover/active lift rules at equal specificity. ----
css = """
/* ==== AGREEMENT EYE FOLLOW-ON (2026-11-17, BRIEF-AGREEMENT-MERGE-EYE-FOLLOWON-20261117.md) ====
   F2 PRESS (Laws SS1/SS4, Intelligent Block Rules L6, Anatomy 1.2.8: hover
   rises translateY(-2px), ACTIVE presses INTO the page translateY(1px)):
   the old bytes shared ONE hover/active rule, so a held button LIFTED
   instead of depressing - the eye correctly saw no press. These separate
   :active rules sit last, so they win at equal specificity: depress 1px +
   scale .97 + dim to ~72% + the outer glow and drop shadow collapse to a
   small contact shadow. Release springs back on the base transition.
   F3 DEEP (Laws SS3.1): the Keep-reading button's rim is its beat's tone,
   so the purple/green rims deepen ON THE BUTTON ONLY - the boards keep
   their harvested tones. Letter beats carry tone-purple / tone-emerald;
   deck beats 1 (purple) and 3 (green) are named by data-beat.
   F5 CLEAR (eye E5): in the bridge view the four 56px corner emblems sit
   at the head's edges, so the head's text column is padded 72px each side
   (56px emblem + 16px air) - the kicker and title can never reach an
   emblem. At <=480px the emblems are 40px, so the padding is 52px. The
   corners only ever display in the bridge view, so the padding is scoped
   there and the intro/deck/letter heads are untouched. */
.fp-intro-choice:active{transform:translateY(1px) scale(.97);filter:brightness(.72);box-shadow:inset 0 1.5px 0 rgba(255,255,255,.45),inset 0 -4px 8px rgba(0,0,0,.5),0 2px 6px rgba(0,0,0,.6);transition:transform .07s ease,filter .07s ease,box-shadow .07s ease}
.fp-next:active,#fpNextBtn:active,#fpNextBtn2:active{transform:translateY(1px) scale(.97);filter:brightness(.72);box-shadow:inset 0 1.5px 0 rgba(255,255,255,.45),inset 0 -4px 8px rgba(0,0,0,.5),0 2px 6px rgba(0,0,0,.6);transition:transform .07s ease,filter .07s ease,box-shadow .07s ease}
body.fp-stage-on.fp-dialed #fpNextBtn:active,body.fp-stage-on.fp-dialed #fpNextBtn2:active{animation:none;transform:translateY(1px) scale(.97);filter:brightness(.72);box-shadow:inset 0 1.5px 0 rgba(255,255,255,.45),inset 0 -4px 8px rgba(0,0,0,.5),0 2px 6px rgba(0,0,0,.6)}
#fpAgreement .p3-enter:active,#fpLegal .p3-enter:active{transform:translateY(1px) scale(.97);filter:brightness(.72);box-shadow:inset 0 1.5px 0 rgba(255,255,255,.45),inset 0 -4px 8px rgba(0,0,0,.5),0 2px 6px rgba(0,0,0,.6);transition:transform .07s ease,filter .07s ease,box-shadow .07s ease}
#fpAgreement .deck-next:active{transform:translateY(1px) scale(.97);filter:brightness(.72);box-shadow:inset 0 1.5px 0 rgba(255,255,255,.45),inset 0 -4px 8px rgba(0,0,0,.5),0 2px 6px rgba(0,0,0,.6)}
.p3-naya-play:active{transform:scale(.94);filter:brightness(.7);box-shadow:0 0 8px rgba(255,255,255,.25),0 4px 10px rgba(0,0,0,.6);transition:transform .07s ease,filter .07s ease,box-shadow .07s ease}
.p3-naya-play.pending-glow:active{transform:scale(.94);filter:brightness(.7);box-shadow:0 0 8px rgba(255,255,255,.25),0 4px 10px rgba(0,0,0,.6)}
.fp-legal-link:active{transform:scale(.97);filter:brightness(.7);transition:transform .07s ease,filter .07s ease}
.fp-stage-exit:active{transform:scale(.96);filter:brightness(.7);transition:transform .07s ease,filter .07s ease}
.fp-enter-deal:active{filter:brightness(.7)}
.new-account:active{filter:brightness(.75)}
#fpZoomClose:active{transform:scale(.94);filter:brightness(.75)}
.letter-beat.tone-purple .letter-next{--tone:#8e24aa}
.letter-beat.tone-emerald .letter-next{--tone:#07925f}
#deckBody article[data-beat="1"] .deck-next{--tone:#8e24aa}
#deckBody article[data-beat="3"] .deck-next{--tone:#07925f}
body.fp-stage-on #fpAgreement.fp-view-bridge .fp-agree-head{padding-left:72px;padding-right:72px}
@media(max-width:480px){body.fp-stage-on #fpAgreement.fp-view-bridge .fp-agree-head{padding-left:52px;padding-right:52px}}
"""
last_style = h.rfind("</style>")
assert last_style > 0, "F2 last style close missing"
h = h[:last_style] + css + h[last_style:]

write_resilient(ROOT, h.encode())
print("root written: %d B sha %s" % (len(h.encode()), hashlib.sha256(h.encode()).hexdigest()[:12]))

# ================= /agreement =================
a = open(AGMT, encoding="utf-8").read()
assert hashlib.sha256(a.encode()).hexdigest().startswith("faea2190"), "agreement base moved"

# F2 press-in only: this file's tones are already all deep (verified: its
# --tone counter shows only #8e24aa/#07925f/#3f51b5/#0e7490/#d4a017/#c2410c/
# #c62828/#a21caf), so no F3 change is needed here. Its .play-btn already
# carries a scale(.97) :active rule, but the shared hover/active rule keeps
# the glow bright and the lift, so the press does not read - the rules
# below replace the lift with a depress + dim + collapse, last in source.
css_a = """
/* ==== AGREEMENT EYE FOLLOW-ON (2026-11-17, BRIEF-AGREEMENT-MERGE-EYE-FOLLOWON-20261117.md) ====
   F2 PRESS (Laws SS1/SS4, Intelligent Block Rules L6, Anatomy 1.2.8):
   hover rises, ACTIVE presses INTO the page. The old bytes shared one
   hover/active lift rule (and a lone scale(.97) that kept the bright glow),
   so a held button did not read as pressed. These separate :active rules
   sit last and win at equal specificity: depress 1px + scale .97 (play
   .94, it is the bigger object) + dim to ~72% + glow and drop shadow
   collapse. No tone change in this file: its tones are already deep. */
.play-btn:active{transform:scale(.94);filter:brightness(.72);box-shadow:inset 0 1.5px 0 rgba(255,255,255,.45),inset 0 -4px 8px rgba(0,0,0,.5),0 0 12px -2px #8e24aa,0 4px 10px rgba(0,0,0,.6);transition:transform .07s ease,filter .07s ease,box-shadow .07s ease}
.p3-enter:active{transform:translateY(1px) scale(.97);filter:brightness(.72);box-shadow:inset 0 1.5px 0 rgba(255,255,255,.45),inset 0 -4px 8px rgba(0,0,0,.5),0 2px 6px rgba(0,0,0,.6);transition:transform .07s ease,filter .07s ease,box-shadow .07s ease}
.deck-next:active{transform:translateY(1px) scale(.97);filter:brightness(.72);box-shadow:inset 0 1.5px 0 rgba(255,255,255,.45),inset 0 -4px 8px rgba(0,0,0,.5),0 2px 6px rgba(0,0,0,.6)}
"""
last_style = a.rfind("</style>")
assert last_style > 0, "F2a last style close missing"
a = a[:last_style] + css_a + a[last_style:]

write_resilient(AGMT, a.encode())
print("agreement written: %d B sha %s" % (len(a.encode()), hashlib.sha256(a.encode()).hexdigest()[:12]))
print("ALL EDITS APPLIED")
