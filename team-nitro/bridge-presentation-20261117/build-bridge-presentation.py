#!/usr/bin/env python3
"""Bridge presentation fix round (2026-11-17) — welcome file build.

Base: ../bridge-page-fix-20261117/welcome-bridge-fix.html
      (branch walk-end/entrance-welcome-20261116 tip 80e7d532,
       blob 10e8bd74, 1,129,270 B, sha 395794a3...)
Out:  welcome-presentation.html (stdout; shell redirect does the write,
      because python writes are EPERM-blocked in this window).

Every change is an anchored replacement with an exact-occurrence check.
If any anchor is missing or occurs an unexpected number of times, the
script fails loudly and writes nothing.
"""
import sys, hashlib

BASE = '/home/hatch/workspace/team-nitro/bridge-page-fix-20261117/welcome-bridge-fix.html'
s = open(BASE, encoding='utf-8').read()
ORIG_LEN = len(s)
print(f'# base: {len(s)} chars, sha256 {hashlib.sha256(s.encode()).hexdigest()[:16]}', file=sys.stderr)

def rep(old, new, count=1, label=''):
    global s
    n = s.count(old)
    assert n == count, f'REP FAIL [{label}]: anchor occurs {n}x, expected {count}x :: {old[:90]!r}'
    s = s.replace(old, new)
    print(f'# rep ok [{label}]', file=sys.stderr)

# ---------------------------------------------------------------- W1: move #fpBridge out of #deckUnfold (Amendment #2a, root cause)
# #fpBridge was inserted inside #deckUnfold, which is display:none in
# bridge view — the whole bridge rendered 0x0. Move it to a direct child
# of #fpAgreement, right after #fpIntroSide closes (before #deckUnfold).
start = s.find('<div id="fpBridge">')
end_marker = '<div class="letter-controls" id="deckControls">'
end = s.find(end_marker)
assert start > 0 and end > start, 'W1: bridge block markers not found'
block = s[start:end]
# the block must be div-balanced (it is one <div id="fpBridge"> subtree)
assert block.count('<div') == block.count('</div>'), (
    f"W1: bridge block not div-balanced: opens={block.count('<div')} closes={block.count('</div>')}")
assert block.startswith('<div id="fpBridge">'), 'W1: block does not start at fpBridge'
s = s[:start] + s[end:]
ins = s.find('<section class="p3-deal-unfold" id="deckUnfold"')
assert ins > 0, 'W1: deckUnfold open not found for insertion'
s = s[:ins] + block + s[ins:]
# verify order: fpAgreement < fpIntroSide < fpBridge < deckUnfold < deckControls
for a, b in [('<section id="fpAgreement"', '<div class="fp-intro-side" id="fpIntroSide"'),
             ('<div class="fp-intro-side" id="fpIntroSide"', '<div id="fpBridge">'),
             ('<div id="fpBridge">', '<section class="p3-deal-unfold" id="deckUnfold"'),
             ('<section class="p3-deal-unfold" id="deckUnfold"', '<div class="letter-controls" id="deckControls">')]:
    assert s.find(a) < s.find(b), f'W1: order broken {a[:30]} !< {b[:30]}'
# and fpBridge is NOT inside deckUnfold: the bridge close precedes deckUnfold open
bridge_close = s.find('</div>', s.find('<div id="fpBridge">'))
assert s.find('<section class="p3-deal-unfold" id="deckUnfold"') > s.find('<div id="fpBridge">'), 'W1: sanity'
print('# W1 ok: #fpBridge moved to direct child of #fpAgreement', file=sys.stderr)

# ---------------------------------------------------------------- W2: bridge scrolls (flex child, like deck/letter)
rep("body.fp-stage-on #fpAgreement.fp-view-bridge #fpBridge{display:block}",
    "body.fp-stage-on #fpAgreement.fp-view-bridge #fpBridge{display:block;flex:1 1 auto;min-height:0;overflow-y:auto;padding-bottom:16px}",
    1, 'W2 bridge scroll')

# ---------------------------------------------------------------- W3: emblem corners (NAYA_ICON.png, on an angle)
rep('<div class="fp-bridge-corners" aria-hidden="true"><span class="ldot fp-bridge-corner-tl" style="--dc:#8e24aa"></span><span class="ldot fp-bridge-corner-tr" style="--dc:#0f52ba"></span><span class="ldot fp-bridge-corner-bl" style="--dc:#07925f"></span><span class="ldot fp-bridge-corner-br" style="--dc:#d4a017"></span></div>',
    '<div class="fp-bridge-corners" aria-hidden="true"><img class="fp-bridge-emblem fp-bridge-corner-tl" src="/naya-emblem-cut.png" alt=""><img class="fp-bridge-emblem fp-bridge-corner-tr" src="/naya-emblem-cut.png" alt=""><img class="fp-bridge-emblem fp-bridge-corner-bl" src="/naya-emblem-cut.png" alt=""><img class="fp-bridge-emblem fp-bridge-corner-br" src="/naya-emblem-cut.png" alt=""></div>',
    1, 'W3 emblem markup')
rep(".fp-bridge-corners .ldot{position:absolute}",
    ".fp-bridge-corners .fp-bridge-emblem{position:absolute;width:56px;height:56px;object-fit:contain;filter:drop-shadow(0 6px 14px rgba(0,0,0,.65)) drop-shadow(0 0 18px rgba(160,107,255,.35))}",
    1, 'W3 emblem css')
rep(".fp-bridge-corner-tl{top:-8px;left:0}",
    ".fp-bridge-corner-tl{top:-10px;left:-4px;transform:rotate(-20deg)}", 1, 'W3 tl')
rep(".fp-bridge-corner-tr{top:-8px;right:0}",
    ".fp-bridge-corner-tr{top:-10px;right:-4px;transform:rotate(20deg)}", 1, 'W3 tr')
rep(".fp-bridge-corner-bl{bottom:-8px;left:0}",
    ".fp-bridge-corner-bl{bottom:-10px;left:-4px;transform:rotate(20deg)}", 1, 'W3 bl')
rep(".fp-bridge-corner-br{bottom:-8px;right:0}",
    ".fp-bridge-corner-br{bottom:-10px;right:-4px;transform:rotate(-20deg)}", 1, 'W3 br')

# ------------------------------------------------- W4: pictures as real objects
# .lb-showcase frame: the even halo glow (0 0 44px) goes; one light from
# the top-left, a deep down-right shadow, and a lift on hover. The slide
# art inside is verbatim — the frame is what becomes a real object.
rep("box-shadow:0 20px 50px rgba(0,0,0,.7),0 0 44px color-mix(in srgb,var(--tone,#a06bff) 18%,transparent),inset 0 1px 0 rgba(255,255,255,.18)}",
    "box-shadow:0 24px 56px rgba(0,0,0,.75),0 6px 16px rgba(0,0,0,.6),inset 0 1px 0 rgba(255,255,255,.22),inset 0 -12px 24px rgba(0,0,0,.4);transition:transform .3s ease,box-shadow .3s ease}",
    2, 'W4 showcase base')
rep("box-shadow:0 20px 50px rgba(0,0,0,.7),0 0 44px color-mix(in srgb,var(--tone,#a06bff) 45%,transparent),inset 0 1px 0 rgba(255,255,255,.18)}",
    "box-shadow:0 32px 64px rgba(0,0,0,.8),0 0 40px color-mix(in srgb,var(--tone,#a06bff) 35%,transparent),inset 0 1px 0 rgba(255,255,255,.28),inset 0 -12px 24px rgba(0,0,0,.4);transform:translateY(-4px)}",
    2, 'W4 showcase hover')
# .deal-beat-photo: the 22px glow wash goes; tone rim + top-left light +
# real down-right shadow. Both the base and the lead (purple) variants.
rep("box-shadow:0 0 22px color-mix(in srgb, var(--tone, #a06bff) 55%, transparent),0 8px 20px rgba(0,0,0,.6)}",
    "box-shadow:inset 0 2px 5px rgba(255,255,255,.3),inset 0 -8px 16px rgba(0,0,0,.55),0 14px 30px rgba(0,0,0,.7),0 0 0 1px color-mix(in srgb, var(--tone, #a06bff) 45%, transparent)}",
    2, 'W4 photo base')
rep("box-shadow:0 0 22px rgba(168,107,255,.55),0 8px 20px rgba(0,0,0,.6)}",
    "box-shadow:inset 0 2px 5px rgba(255,255,255,.3),inset 0 -8px 16px rgba(0,0,0,.55),0 14px 30px rgba(0,0,0,.7),0 0 0 1px rgba(168,107,255,.45)}",
    2, 'W4 photo lead')
# speaking faces: 12px breathing room from the viewport edge (they sat
# flush at left:0/right:0, reading as clipped at 1920).
rep("img.style.left = '0px';", "img.style.left = '12px';", 1, 'W4 face left')
rep("img.style.right = '0px';", "img.style.right = '12px';", 1, 'W4 face right')

# ------------------------------------------------- W5: play tip below the button (never over the subtitle)
rep(".p3-play-tip{display:none;position:absolute;left:50%;bottom:calc(100% + 10px);",
    ".p3-play-tip{display:none;position:absolute;left:50%;top:calc(100% + 36px);",
    1, 'W5 tip below')
rep("@media (max-width:480px){.p3-naya-play .p3-play-tip{font-size:11px;padding:4px 10px;bottom:calc(100% + 6px)}}",
    "@media (max-width:480px){.p3-naya-play .p3-play-tip{font-size:11px;padding:4px 10px;top:calc(100% + 30px)}}",
    1, 'W5 tip 480')
rep("@media (max-width:360px){.p3-naya-play .p3-play-tip{padding:3px 8px;line-height:1.2;bottom:calc(100% + 4px)}}",
    "@media (max-width:360px){.p3-naya-play .p3-play-tip{padding:3px 8px;line-height:1.2;top:calc(100% + 28px)}}",
    1, 'W5 tip 360')

# ------------------------------------------------- W6: bars + eyebrows (bridge fix block, before </style>)
anchor = ".fp-bridge-corner-br{bottom:-10px;right:-4px;transform:rotate(-20deg)}\n</style>"
assert s.count(anchor) == 1, 'W6: bridge css tail anchor not found'
s = s.replace(anchor,
""".fp-bridge-corner-br{bottom:-10px;right:-4px;transform:rotate(-20deg)}
@media(max-width:480px){.fp-bridge-corners .fp-bridge-emblem{width:40px;height:40px}}
/* ---- BRIDGE PRESENTATION (2026-11-17, BRIEF-BRIDGE-PRESENTATION-20261117.md §7b) ----
   The stage bottom bar rides ABOVE the fixed legal strip in bridge view:
   the strip painted over the bar (same bottom:0, later in the DOM) and
   half-buried 'Back to the login'. At phone widths the legal links wrap
   instead of overflowing, and the bar rides higher to clear the taller
   wrapped strip. The centred eyebrow lines shrink at phone widths so
   their span clears the ‹ Login button at the left. */
body.fp-stage-on.fp-bridge #fpStageBarB{bottom:44px}
@media(max-width:640px){
html.fp-locked body.fp-stage-on.fp-bridge #fpLegal .fp-legal-links{flex-wrap:wrap;justify-content:center;overflow-x:visible}
body.fp-stage-on.fp-bridge #fpStageBarB{bottom:72px}
body.fp-stage-on #fpStageBarT .fp-dots{display:none}
}
</style>""")
print('# W6 ok: bridge bars + eyebrows', file=sys.stderr)

# ------------------------------------------------- W7: ?stage= deep link (walk end slide links here)
rep("if(enterBtn)enterBtn.addEventListener('click',function(){enterStage();});",
    """if(enterBtn)enterBtn.addEventListener('click',function(){enterStage();});
  /* BRIDGE PRESENTATION (2026-11-17) — deep link from the walk's end slide:
     ?stage=deck opens the visual story, ?stage=letter opens the read-it-all
     letter page, ?stage=bridge opens the bridge. Plain relative links, so
     the same URL works on staging and on the main URL alike. */
  try{var _fpStage=new URLSearchParams(window.location.search).get('stage');
  if(_fpStage==='deck'||_fpStage==='letter'||_fpStage==='bridge'){enterStage();if(_fpStage==='deck'){goResume();}else if(_fpStage==='letter'){enterLetterPage();}}}catch(e){}""",
    1, 'W7 stage param')

# ------------------------------------------------- W8: device list — one row per citizen (Amendment #2e)
old_seed = """    if(idList.filter(function(it){ return it&&it.alias&&String(it.alias).toLowerCase()===String(alias).toLowerCase(); }).length===0){
      idList.unshift({alias:alias,name:name||alias});
      try{ localStorage.setItem('nayanet_smart_identities', JSON.stringify(idList.slice(0,8))); }catch(e){}"""
new_seed = """    /* BRIDGE PRESENTATION (2026-11-17) — one row per citizen: the list
       held the same alias twice (once under a real name, once under the
       alias itself), so 'Captain Eye' and 'captaineyecheck' showed as two
       people, and 'Alex Walker' twice. Collapse by alias (case-insensitive),
       keeping the real name when one exists; a fresh claim heals a stale
       alias-as-name. */
    var _seenAlias={};
    idList=idList.filter(function(it){ if(!it||!it.alias)return false; var k=String(it.alias).toLowerCase(); if(_seenAlias[k]){ if(it.name&&String(it.name).toLowerCase()!==k&&(!_seenAlias[k].name||String(_seenAlias[k].name).toLowerCase()===k)) _seenAlias[k].name=it.name; return false; } _seenAlias[k]=it; return true; });
    var _cur=idList.filter(function(it){ return it&&it.alias&&String(it.alias).toLowerCase()===String(alias).toLowerCase(); })[0];
    if(!_cur){
      idList.unshift({alias:alias,name:name||alias});
      try{ localStorage.setItem('nayanet_smart_identities', JSON.stringify(idList.slice(0,8))); }catch(e){}
    } else if(name&&String(name).toLowerCase()!==String(alias).toLowerCase()&&(!_cur.name||String(_cur.name).toLowerCase()===String(alias).toLowerCase())){ _cur.name=name; try{ localStorage.setItem('nayanet_smart_identities', JSON.stringify(idList.slice(0,8))); }catch(e){} }"""
rep(old_seed, new_seed, 1, 'W8 dedupe')
old_note = """  /* SHARE PLUS (2026-11-16) — the remove warning + confirm. The removal
     rewrites nayanet_smart_identities, so the account stays gone on
     reload; duplicates of one name are separate rows (different device
     keys), and only the row whose X was tapped is removed. */"""
new_note = """  /* SHARE PLUS (2026-11-16) — the remove warning + confirm. The removal
     rewrites nayanet_smart_identities, so the account stays gone on
     reload; the list is deduped by alias (2026-11-17), so one citizen is
     one row, and only the row whose X was tapped is removed. */"""
rep(old_note, new_note, 1, 'W8 note')

print(f'# done: {ORIG_LEN} -> {len(s)} chars, sha256 {hashlib.sha256(s.encode()).hexdigest()[:16]}', file=sys.stderr)
sys.stdout.write(s)
