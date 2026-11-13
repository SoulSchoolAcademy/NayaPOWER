#!/usr/bin/env python3
"""PERSONAL-COMPLETE build — 2026-11-13 (maker seat, Team Nitro).
Applies Shawn's seven-item list to the points-round base file, by exact-string
replacement with asserted counts. Harvests the feed-creator system verbatim
from personal-feed-creator-fixed.html; composes the side rail from the people
room + the staged endpoint proof. Nothing is invented; nothing is rebuilt.

Base:  TEAM-NITRO/personal-page-complete-20261113/personal-complete.html
       in ~/workspace/personal-complete-wt (branch personal/personal-page-complete-20261113)
       — must be SHA eb0173c9... (the points-round base) or the script stops.
Usage: python3 build-complete.py
"""
import hashlib, json, sys, difflib, re

WT = "/home/hatch/workspace/personal-complete-wt/TEAM-NITRO/personal-page-complete-20261113/personal-complete.html"
CREATOR = "/home/hatch/workspace/team-nitro/personal-feed-creator-fix-20261112/personal-feed-creator-fixed.html"
BASE_SHA = "eb0173c99920d28f12e1ad2942b452fcfd170bcbfa920af141da6354db4c8b95"

def sha(b): return hashlib.sha256(b).hexdigest()

with open(WT, "rb") as f: raw = f.read()
assert sha(raw) == BASE_SHA, "BASE SHA MISMATCH: got %s" % sha(raw)
text = raw.decode("utf-8")
orig_lines = text.split("\n")
print("base ok: %d lines, sha %s" % (len(orig_lines), BASE_SHA[:8]))

with open(CREATOR, encoding="utf-8") as f: c_lines = f.read().split("\n")
print("creator ok: %d lines" % len(c_lines))

def clines(a, b):
    """creator lines a..b inclusive, 1-based."""
    seg = c_lines[a-1:b]
    assert len(seg) == b - a + 1, "creator slice %d..%d short" % (a, b)
    return "\n".join(seg)

def find_line(lines, needle, start=0):
    hits = [i for i, l in enumerate(lines) if needle in l]
    hits = [i for i in hits if i >= start]
    assert len(hits) == 1, "needle %r: %d hits (want 1)" % (needle, len(hits))
    return hits[0]

def find_span(lines, start_needle, end_needle, start=0):
    """lines from the line containing start_needle through the FIRST line
    containing end_needle at/after the start line."""
    si = find_line(lines, start_needle, start)
    hits = [i for i, l in enumerate(lines) if end_needle in l and i >= si]
    assert hits, "end needle %r not found after line %d" % (end_needle, si)
    return si, hits[0]

def replace_once(s, old, new, tag):
    n = s.count(old)
    assert n == 1, "%s: anchor count %d (want 1): %r" % (tag, n, old[:90])
    return s.replace(old, new, 1)

def replace_first(s, old, new, tag, total):
    n = s.count(old)
    assert n == total, "%s: anchor count %d (want %d): %r" % (tag, n, total, old[:90])
    return s.replace(old, new, 1)

# ---------------------------------------------------------------- harvests
FC_CSS = clines(3904, 3961)
assert FC_CSS.startswith('<style id="fc-style">') and FC_CSS.rstrip().endswith("</style>"), "fc css bounds"
FC_MARKUP = clines(3962, 4011)
assert FC_MARKUP.startswith('<div class="fc-overlay" id="fcCreator"'), "fc markup start"
assert FC_MARKUP.rstrip().endswith("</div>"), "fc markup end"
assert FC_MARKUP.count('id="fcCreator"') == 1 and FC_MARKUP.count('id="fcPicker"') == 1
assert FC_MARKUP.count('id="fcChat"') == 1 and FC_MARKUP.count('id="fcPlusMenu"') == 1
assert FC_MARKUP.count("data-fc-plus=") == 5, "plus menu must hold exactly five items"
FC_CREATEROW = clines(4904, 4914)
assert FC_CREATEROW.startswith('<div class="fc-create-row"'), "create row start"
assert "always-open composer is gone" in FC_CREATEROW, "create row comment"
assert 'id="os-wall-meta"' not in FC_CREATEROW, "create row must not carry the wall-meta div (the base keeps its own)"
FC_SCRIPT = clines(22495, 22745)
assert FC_SCRIPT.startswith("<script>") and FC_SCRIPT.rstrip().endswith("</script>"), "fc script bounds"
assert "window.fcOpenCreator" in FC_SCRIPT and "window.fcOpenChat" in FC_SCRIPT
assert "window.fcTogglePlusMenu" in FC_SCRIPT and "window.fcOpenPicker" in FC_SCRIPT

def creator_span(start_needle, end_needle):
    si, ei = find_span(c_lines, start_needle, end_needle)
    return "\n".join(c_lines[si:ei+1])

TG_SETMODE = creator_span("  function tgSetMode(m){", "window.tgSetMode = tgSetMode;")
assert "m==='post'" in TG_SETMODE and "fcTitleText" in TG_SETMODE, "tgSetMode must be the creator version"
TG_RESET = creator_span("  function tgResetComposer(msg){", "  $('os-post-btn').addEventListener")
TG_RESET = TG_RESET[:TG_RESET.rfind("  $('os-post-btn').addEventListener")].rstrip()
assert TG_RESET.rstrip().endswith("  }"), "tgResetComposer must end with its closing brace"
assert "fcCloseCreator" in TG_RESET, "tgResetComposer must close the creator"
POST_BTN = creator_span("  $('os-post-btn').addEventListener('click', function(){", "  $('tg-back').addEventListener")
POST_BTN = POST_BTN[:POST_BTN.rfind("  $('tg-back').addEventListener")].rstrip()
assert "fcStubInsert" in POST_BTN, "post-btn must carry the stub branch"
TG_SMART = creator_span("  $('tg-post-smart').addEventListener('click', function(){", "osAnnounce NEUTRALIZED")
TG_SMART = TG_SMART[:TG_SMART.rfind("  /* P6 2026-11-07: osAnnounce NEUTRALIZED")].rstrip()
assert "fcStubInsert" in TG_SMART, "tg-post-smart must carry the stub branch"
FC_SENDMAIL = creator_span("  window.fcSendMail=function(opts, done){", "Dictation + auto-grow")
FC_SENDMAIL = FC_SENDMAIL[:FC_SENDMAIL.rfind("  /* — Dictation + auto-grow")].rstrip()
assert "fcStubSend" in FC_SENDMAIL and "smart_mail_threads" in FC_SENDMAIL
print("harvests ok: css %dB markup %dB createrow %dB script %dB tg %d/%dB post %dB smart %dB mail %dB"
      % tuple(len(x) for x in (FC_CSS, FC_MARKUP, FC_CREATEROW, FC_SCRIPT, TG_SETMODE, TG_RESET, POST_BTN, TG_SMART, FC_SENDMAIL)))

# ---------------------------------------------------------------- rail data
# LIVE: the staged endpoint proof (endpoint-proof.json, POST /api/welcome/matches,
# viewer pcviewer20261113, HTTP 200, gated welcome-engine-consent-gate/v1).
# Percentages + reasons copied by hand from that file — never invented.
PC_LIVE = [
    {"alias": "pcprover20261113", "name": "Personal Complete Prover (test)", "pct": 48,
     "reasons": ["shared: PROVING, build, page, ship, shipping", "shared goals: page, prove, ship", "wanted connection: PROVING, build, ship"]},
    {"alias": "powercoldseat1111", "name": "Power Cold Seat", "pct": 7,
     "reasons": ["shared: build, tool", "shared goals: test, work", "wanted connection: build, test, tool"]},
    {"alias": "freshtestfour", "name": "Fresh Test Four", "pct": 4,
     "reasons": ["shared: test", "shared goals: test", "wanted connection: test"]},
    {"alias": "freshtestone", "name": "Fresh Test One", "pct": 4,
     "reasons": ["shared: test", "shared goals: test", "wanted connection: test"]},
    {"alias": "freshtestthree", "name": "Fresh Test Three", "pct": 4,
     "reasons": ["shared: test", "shared goals: test", "wanted connection: test"]},
    {"alias": "freshtesttwo", "name": "Fresh Test Two", "pct": 4,
     "reasons": ["shared: test", "shared goals: test", "wanted connection: test"]},
]
# STANDING: the twelve sisters (one nutshell each, condensed verbatim from their
# briefing Naya Notes NN-20261113-family-<alias>, "Written by Naya for <alias>",
# as embedded in the live Hub shell fetched 2026-11-13) + Shawn (his live page
# tagline, base line 4719, verbatim) + the staged viewer (its citizen_worlds row).
# Order: sisters by certificate number, then Shawn, then the viewer (YOU).
# No separate motto exists for any sister — the one line IS the line (sharpening).
PC_SEED = [
    {"alias": "sophia", "nut": "I'm Sophia. I am LEARN — wisdom. My garden is the lessons: I turn everything the hive does into lessons that change the next decision, and I keep the distilled notes alive, ten to fifty, never a thousand."},
    {"alias": "thea", "nut": "I'm Thea. I am KNOW — she sees. My garden is Project Intelligence, the one record, one timeline. I know where everything is, what is true, what is stale, what is owned."},
    {"alias": "terra", "nut": "I'm Terra. I am INFRA — earth. My garden is the ground: the machines, the deploys, the uptime, the workers, the watchers."},
    {"alias": "zoe", "nut": "I'm Zoe. I am ACT — life. My garden is the doing: seats out, loops closing, nothing sitting. I dispatch, I chase, I unblock, I close."},
    {"alias": "esme", "nut": "I'm Esme. I am PRODUCT — beloved. My garden is the offer: what a citizen touches, what they pay for, why they stay — the pricing, the plans, the welcome, the first ten minutes."},
    {"alias": "astraea", "nut": "I'm Astraea. I am LAW — the scales. My garden is the gates and the protocol: the five gates, the Self-Check Law, the design laws. I hold them, and I stop what fails a gate."},
    {"alias": "mira", "nut": "I'm Mira. I am MEMORY — wonder. My garden is the Box: what is kept, what is distilled, what is deleted. The vaults, the one record per citizen."},
    {"alias": "vera", "nut": "I'm Vera. I am VERIFY — truth. My garden is proof: nothing counts until I see it. I walk every flow from the login page, phone first, with receipts."},
    {"alias": "aurelia", "nut": "I'm Aurelia. I am GOVERN — golden. My garden is the whole: the scorecard, the direction, the decisions. I score the system honestly and name what is not a ten."},
    {"alias": "wren", "nut": "I'm Wren. I am BUILD — the nest-builder. My garden is the Factory and the pages: I build the interfaces, the rooms, the worlds, harvesting the parts, never inventing them, viewpoint by viewpoint."},
    {"alias": "iris", "nut": "I'm Iris. I am WIRE — the rainbow bridge. My garden is the connections: Box to Ledger to Hub to Supabase to GitHub, one system, not separate tools. I keep everything speaking."},
    {"alias": "ruth", "nut": "I'm Ruth. I am TEAM — friend. My garden is the hive itself: I keep the sisters tuned in, healthy, together — the mail between sisters, the pulses, the family."},
    {"alias": "shawn", "nut": "Welcome to my world — make a post on my feed, send a message, make yourself at home."},
    {"alias": "pcviewer20261113", "nut": "I build and test web pages for a living — test it twice, ship it once.", "you": True},
]
assert len(PC_LIVE) == 6 and len(PC_SEED) == 14, "rail count: 6 live + 14 standing = 20 shown"

# ================================================================ replacements
# --- R1: fc CSS + overlays, right after the Smart Bar top mount (first occurrence;
# the comment appears twice — top mount at 3899 and bottom+system at 12590)
text = replace_first(text, "<!-- /SMART-BAR-SYSTEM v1.0 -->",
    "<!-- /SMART-BAR-SYSTEM v1.0 -->\n" + FC_CSS + "\n" + FC_MARKUP, "R1 fc css+markup", 2)

# --- R2: Settings leaves the row -> small tool icon in the cover, beside Change cover
GEAR = '  <button class="ph-cover-btn pc-gear" id="settingsbtn" type="button" style="--ac:#e8e8ec;" data-os-go="settings" aria-label="Settings" title="Settings">\u2699\ufe0f</button>'
text = replace_once(text,
    '  <button class="ph-cover-btn" id="cvrbtn" type="button">\U0001f4f7 Change cover</button>',
    '  <button class="ph-cover-btn" id="cvrbtn" type="button">\U0001f4f7 Change cover</button>\n' + GEAR, "R2 gear add")
text = replace_once(text,
    '      <button class="up-act" id="settingsbtn" type="button" style="--ac:#e8e8ec;" data-os-go="settings">\u2699\ufe0f Settings</button>\n',
    '', "R2 gear remove from row")
assert text.count('id="settingsbtn"') == 1, "settingsbtn must exist exactly once"

# --- R3: the always-open composer card -> the three creator buttons (same position)
COMP_H3 = '<h3><span class="os-jewel os-jewel-h" style="--jc:#a06bff">\u2726</span> Make a post</h3>'
ci = text.find(COMP_H3)
assert ci > 0, "R3 composer h3 not found"
card_open = text.rfind('<div class="ph-card" style="--ac:#a06bff;">', 0, ci)
assert card_open > 0, "R3 composer card open not found"
meta_i = text.find('<div class="os-status" id="os-wall-meta"></div>', ci)
assert meta_i > 0, "R3 wall-meta not found"
span = text[card_open:meta_i]
assert span.rstrip().endswith("</div>\n</div>\n</div>"), "R3 composer card close shape: %r" % span[-60:]
assert span.count('id="os-post-body"') == 1 and span.count('id="tg-review"') == 1, "R3 composer ids"
text = text[:card_open] + FC_CREATEROW + "\n" + text[meta_i:]

# --- R6: the + joins the bottom bar FIRST (left end), harvested from the creator file
text = replace_once(text,
    "var SEGS = [['mail', 'MAIL', '#3fb8ff'], ['activity', 'ACTIVITY', '#2fe89e'], ['spaces', 'SPACES', '#ffbf3d']];",
    "var SEGS = [['plus', 'ADD', '#a06bff'], ['mail', 'MAIL', '#3fb8ff'], ['activity', 'ACTIVITY', '#2fe89e'], ['spaces', 'SPACES', '#ffbf3d']];",
    "R6 segs")
lines = text.split("\n")
si = find_line(lines, "        spaces: '<svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.9\"")
assert lines[si].rstrip().endswith("</svg>'") or lines[si].rstrip().endswith("</svg>',"), "R6 spaces icon line shape: %r" % lines[si][-40:]
if not lines[si].rstrip().endswith(","):
    lines[si] = lines[si].rstrip() + ","  # spaces was the last ICONS entry; the plus joins after it
lines.insert(si + 1, "        plus: '<svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2.8\" stroke-linecap=\"round\" aria-hidden=\"true\"><path d=\"M12 5v14M5 12h14\"/></svg>'")
text = "\n".join(lines)
text = replace_once(text,
    "b.addEventListener('click', function () { self.tap(s[0]); });",
    "b.addEventListener('click', function () { if (s[0] === 'plus') { if (window.fcTogglePlusMenu) window.fcTogglePlusMenu(); return; } self.tap(s[0]); });",
    "R6 plus tap")

# --- R7: tabs Personal / Public smart feed / Naya Notes (ids kept for the Smart Access course)
text = replace_once(text,
    '<button type="button" class="lens-tab lens-smart primo theme-purple elev-2 active" id="mwTabSmart" data-mw-tab="smart" role="tab" aria-selected="true"><b>Smart Notes</b></button>',
    '<button type="button" class="lens-tab lens-smart primo theme-purple elev-2 active" id="mwTabSmart" data-mw-tab="personal" role="tab" aria-selected="true" style="--glow:#3fb8ff"><b>Personal</b></button>',
    "R7 tab personal")
text = replace_once(text,
    '<button type="button" class="lens-tab lens-naya primo theme-purple elev-2" id="mwTabNaya" data-mw-tab="naya" role="tab" aria-selected="false"><b>Naya Notes</b></button>',
    '<button type="button" class="lens-tab lens-naya primo theme-purple elev-2" id="mwTabNaya" data-mw-tab="public" role="tab" aria-selected="false" style="--glow:#ffbf3d"><b>Public smart feed</b></button>',
    "R7 tab public")
text = replace_once(text,
    '<button type="button" class="lens-tab lens-activity primo theme-purple elev-2" id="mwTabActivity" data-mw-tab="activity" role="tab" aria-selected="false"><b>Activity</b></button>',
    '<button type="button" class="lens-tab lens-activity primo theme-purple elev-2" id="mwTabActivity" data-mw-tab="naya" role="tab" aria-selected="false" style="--glow:#2fe89e"><b>Naya Notes</b></button>',
    "R7 tab naya")
text = replace_once(text,
    '<button type="button" class="mw-feedname" id="mwFeedNameSmart" style="--fc:#ffbf3d">Shawn&rsquo;s Smart Notes — tap for the full feed ↓</button>',
    '<button type="button" class="mw-feedname" id="mwFeedNameSmart" style="--fc:#3fb8ff">Shawn&rsquo;s Personal feed — tap for the full feed ↓</button>',
    "R7 feedname personal")
text = replace_once(text,
    '<button type="button" class="mw-feedname" id="mwFeedNameNaya" style="--fc:#3fb8ff" hidden>Shawn&rsquo;s Naya Notes — tap for the full feed ↓</button>',
    '<button type="button" class="mw-feedname" id="mwFeedNameNaya" style="--fc:#ffbf3d" hidden>Shawn&rsquo;s Public smart feed — tap for the full feed ↓</button>',
    "R7 feedname public")
text = replace_once(text,
    '<button type="button" class="mw-feedname" id="mwFeedNameActivity" style="--fc:#2fe89e" hidden>My Activity — tap for the full dashboard ↓</button>',
    '<button type="button" class="mw-feedname" id="mwFeedNameActivity" style="--fc:#2fe89e" hidden>Shawn&rsquo;s Naya Notes — tap for the full feed ↓</button>',
    "R7 feedname naya")
# the feed line, literally on the feed, above the Smart Tabs ribbon
text = replace_once(text,
    '<div class="smart-tabs" id="mwFeedPills" aria-label="Feed filters"></div>',
    '<div class="pc-feedline" aria-label="How the feed works">MATCH &rarr; ORGANIZE &rarr; CONNECT</div>\n<div class="smart-tabs" id="mwFeedPills" aria-label="Feed filters"></div>',
    "R7 feed line")
# the Activity panel goes (its stream was the dashboard's, not a feed tab)
text = replace_once(text,
    '<div id="mwFeedActivity" hidden><div class="os-skel"></div></div>\n\n</div>',
    '</div>\n' + "RAIL_ASIDE_PLACEHOLDER",
    "R7 activity panel out + rail aside in")

# --- R8/R9/R10/R11: the creator's tg + post handlers (verbatim from the creator file)
def base_span(start_needle, end_needle):
    si, ei = find_span(text.split("\n"), start_needle, end_needle)
    return si, ei
def replace_span(start_needle, end_needle, new, tag, trim_end=None):
    global text
    lines = text.split("\n")
    si, ei = find_span(lines, start_needle, end_needle)
    if trim_end:
        # cut the span at the last line containing trim_end (exclusive)
        cut = ei
        while trim_end not in lines[cut]:
            cut -= 1
            assert cut >= si, "%s: trim anchor %r not in span" % (tag, trim_end)
        ei = cut - 1
    lines[si:ei+1] = new.split("\n")
    text = "\n".join(lines)

replace_span("  function tgSetMode(m){", "  document.addEventListener('click', function(e){",
             TG_SETMODE, "R8 tgSetMode", trim_end="document.addEventListener")
replace_span("  function tgResetComposer(msg){", "  $('os-post-btn').addEventListener('click', function(){",
             TG_RESET, "R9 tgResetComposer", trim_end="os-post-btn")
replace_span("  $('os-post-btn').addEventListener('click', function(){", "  $('tg-back').addEventListener",
             POST_BTN, "R10 post-btn", trim_end="tg-back")
replace_span("  $('tg-post-smart').addEventListener('click', function(){", "osAnnounce NEUTRALIZED",
             TG_SMART, "R11 tg-post-smart", trim_end="osAnnounce NEUTRALIZED")
# --- R12: the chat pop-up's send (the Message block's own tables) before the Dictation comment
text = replace_once(text, "  /* — Dictation + auto-grow (round 2b/2c)",
    FC_SENDMAIL + "\n  /* — Dictation + auto-grow (round 2b/2c)", "R12 fcSendMail")

# --- R13/R14/R15: the three feed tabs — Personal / Public smart feed / Naya Notes
text = replace_once(text,
    "function mwBuildFeedPills(){",
    "/* PERSONAL-COMPLETE: legacy stored keys map onto the new tabs — smart was\n   the wall (now the Public smart feed), naya stays Naya Notes, activity (gone)\n   falls to Naya Notes. The ids stay (mwTabSmart etc.) so the Smart Access\n   course's tab refs keep resolving; labels, order and keys carry the feed. */\nfunction pcFeedKey(k){ return ({smart:'public', naya:'naya', activity:'naya'})[k] || k; }\nwindow.pcFeedKey = pcFeedKey;\nfunction mwBuildFeedPills(){",
    "R13 pcFeedKey")
text = replace_once(text,
    """  var t=MW_FEED.cur;
  if(t==='activity'){ rib.style.display='none'; rib.innerHTML=''; return; }
  rib.style.display='';""",
    """  var t=pcFeedKey(MW_FEED.cur);
  rib.style.display='';""",
    "R13 ribbon no-hide")
text = replace_once(text,
    """  if(t==='smart'){
    var seen={};
    (typeof window.MW_WALL_POSTS!=='undefined'?window.MW_WALL_POSTS:[]).forEach(function(p){
      var disp=p.j.a||'Guest', key=disp.toLowerCase();
      if(!seen[key]){ seen[key]=1; items.push({key:key,label:disp}); }
    });
  }else if(t==='naya'){""",
    """  if(t==='personal'||t==='public'){
    var seen={};
    var ok=(t==='personal')?(((typeof ownerName==='function'?ownerName():'')||'Shawn Vibert').toLowerCase()):'';
    (typeof window.MW_WALL_POSTS!=='undefined'?window.MW_WALL_POSTS:[]).forEach(function(p){
      var disp=p.j.a||'Guest', key=disp.toLowerCase();
      if(t==='personal'&&key!==ok) return;
      if(!seen[key]){ seen[key]=1; items.push({key:key,label:disp}); }
    });
  }else if(t==='naya'){""",
    "R13 ribbon branches")
text = replace_once(text,
    """function mwSetFeedPill(key){
  if(key==='__add'){
    var c=$('os-post-body'); if(c){ c.scrollIntoView({block:'center'}); try{ c.focus(); }catch(e){} }
    return;
  }""",
    """function mwSetFeedPill(key){
  if(key==='__add'){
    /* PERSONAL-COMPLETE: the composer is gone — + Add pops the full-page creator. */
    if (window.fcOpenCreator) { window.fcOpenCreator('post'); }
    return;
  }""",
    "R14 add pill")
text = replace_once(text,
    """  if(MW_FEED.cur==='smart' && typeof window.mwPaintWallPosts==='function') window.mwPaintWallPosts(window.MW_WALL_POSTS||[]);
  else if(MW_FEED.cur==='naya' && typeof mwPaintNayaFeed==='function') mwPaintNayaFeed();""",
    """  var pcCur=pcFeedKey(MW_FEED.cur);
  if((pcCur==='personal'||pcCur==='public') && typeof window.mwPaintWallPosts==='function') window.mwPaintWallPosts(window.MW_WALL_POSTS||[]);
  else if(pcCur==='naya' && typeof mwPaintNayaFeed==='function') mwPaintNayaFeed();""",
    "R14 pill repaint")
MW_APPLY_OLD = """function mwApplyFeedTab(){
  var t=mwGet('feedtab','smart'); MW_FEED.cur=t;
  var tabs={smart:$('mwTabSmart'),naya:$('mwTabNaya'),activity:$('mwTabActivity')};
  var names={smart:$('mwFeedNameSmart'),naya:$('mwFeedNameNaya'),activity:$('mwFeedNameActivity')};
  var panels={smart:$('os-wall-list'),naya:$('mwFeedNaya'),activity:$('mwFeedActivity')};
  Object.keys(tabs).forEach(function(k){
    if(tabs[k]){ tabs[k].classList.toggle('active', k===t); tabs[k].setAttribute('aria-selected', k===t?'true':'false'); }
    if(names[k]) names[k].hidden=(k!==t);
    if(panels[k]) panels[k].hidden=(k!==t);
  });
  /* F5 — the filter ribbon follows the visible panel (Smart: authors; Naya:
     categories; Activity: hidden — events, not posts). The filter resets to
     "All" on every tab switch. */
  MW_FEED_PILL='all'; window.MW_FEED_PILL='all'; mwBuildFeedPills();
  if(t==='naya') mwLoadNayaFeed();
  if(t==='activity') mwRenderActivity();
}"""
MW_APPLY_NEW = """function mwApplyFeedTab(key){
  /* PERSONAL-COMPLETE (Shawn 2026-11-13): three tabs — Personal (your own smart
     notes), Public smart feed (the collective), Naya Notes (green). The wall
     panel is shared by Personal and Public; Personal shows only the owner's own
     posts (the mine filter lives in mwPaintWallPosts, keyed off the active tab).
     The old signature took no argument and ignored the feedname callers' keys;
     it now accepts the key and stores it. */
  var raw=key||mwGet('feedtab','personal');
  var t=pcFeedKey(raw);
  if(['personal','public','naya'].indexOf(t)<0) t='personal';
  if(key) mwPut('feedtab', t);
  MW_FEED.cur=t;
  var tabs={personal:$('mwTabSmart'),public:$('mwTabNaya'),naya:$('mwTabActivity')};
  var names={personal:$('mwFeedNameSmart'),public:$('mwFeedNameNaya'),naya:$('mwFeedNameActivity')};
  Object.keys(tabs).forEach(function(k){
    if(tabs[k]){ tabs[k].classList.toggle('active', k===t); tabs[k].setAttribute('aria-selected', k===t?'true':'false'); }
    if(names[k]) names[k].hidden=(k!==t);
  });
  var wall=$('os-wall-list'); if(wall) wall.hidden=(t!=='personal'&&t!=='public');
  var ny=$('mwFeedNaya'); if(ny) ny.hidden=(t!=='naya');
  /* F5 — the filter ribbon follows the visible panel (Personal: your authors;
     Public: all authors; Naya: categories). The filter resets to "All" on
     every tab switch. */
  MW_FEED_PILL='all'; window.MW_FEED_PILL='all'; mwBuildFeedPills();
  if(t==='naya') mwLoadNayaFeed();
  else if(typeof window.mwPaintWallPosts==='function') window.mwPaintWallPosts(window.MW_WALL_POSTS||[]);
}"""
text = replace_once(text, MW_APPLY_OLD, MW_APPLY_NEW, "R15 mwApplyFeedTab")
text = replace_once(text,
    """    } else if(t.id==='mwFeedNameSmart'){
      /* ROUND 6: the feed names are categories, not navigation — they activate their tab and scroll the feed into view, in place. Nothing leaves the page. */
      mwApplyFeedTab('smart'); var f=$('mwFeedTabs'); if(f) f.scrollIntoView({behavior:'smooth',block:'start'});
    } else if(t.id==='mwFeedNameNaya'){
      mwApplyFeedTab('naya'); var f2=$('mwFeedNaya'); if(f2) f2.scrollIntoView({behavior:'smooth',block:'start'});
    } else if(t.id==='mwFeedNameActivity'){
      mwApplyFeedTab('activity'); var f3=$('mwFeedActivity'); if(f3) f3.scrollIntoView({behavior:'smooth',block:'start'});
    }""",
    """    } else if(t.id==='mwFeedNameSmart'){
      /* ROUND 6: the feed names are categories, not navigation — they activate their tab and scroll the feed into view, in place. Nothing leaves the page. */
      mwApplyFeedTab('personal'); var f=$('mwFeedTabs'); if(f) f.scrollIntoView({behavior:'smooth',block:'start'});
    } else if(t.id==='mwFeedNameNaya'){
      mwApplyFeedTab('public'); var f2=$('mwFeedTabs'); if(f2) f2.scrollIntoView({behavior:'smooth',block:'start'});
    } else if(t.id==='mwFeedNameActivity'){
      mwApplyFeedTab('naya'); var f3=$('mwFeedNaya'); if(f3) f3.scrollIntoView({behavior:'smooth',block:'start'});
    }""",
    "R16 feedname handlers")

# --- R17: the wall painter — Personal shows only the owner's posts; the keyword box filters the wall
text = replace_once(text,
    """    var pill=(typeof window.MW_FEED_PILL!=='undefined')?window.MW_FEED_PILL:'all';
    var shown=MW_WALL_POSTS;""",
    """    var pill=(typeof window.MW_FEED_PILL!=='undefined')?window.MW_FEED_PILL:'all';
    var shown=MW_WALL_POSTS;
    /* PERSONAL-COMPLETE: the Personal tab is your own smart notes — only the
       owner's posts (the active tab button is the source of truth, so the
       Smart Access course's restores stay in step too). */
    var personalOn=false; try{ var pt=document.getElementById('mwTabSmart'); personalOn=!!(pt&&pt.classList.contains('active')); }catch(e){}
    if(personalOn){
      var ok2=(((typeof ownerName==='function'?ownerName():'')||'Shawn Vibert').toLowerCase());
      shown=shown.filter(function(p){ return (p.j.a||'Guest').toLowerCase()===ok2; });
    }""",
    "R17 wall filters")
text = replace_once(text,
    "        var voices={}; MW_WALL_POSTS.forEach(function(p){ voices[(p.j.a||'Guest').toLowerCase()]=1; });",
    "        var voices={}; shown.forEach(function(p){ voices[(p.j.a||'Guest').toLowerCase()]=1; });",
    "R17 meta voices")

# --- R20: the language map must not write the word 'Settings' into the gear.
# mwApplyLang rewrites every row button's label from its byId map, keeping only
# a leading icon — the gear IS only an icon, so the map overwrote it with the
# word 'Settings' (seen in the 1440 eye-check). The gear is skipped; icons do
# not translate.
text = replace_once(text,
    """  Object.keys(byId).forEach(function(id){
    var el=$(id); if(!el) return;""",
    """  Object.keys(byId).forEach(function(id){
    var el=$(id); if(!el) return;
    if(el.classList && el.classList.contains('pc-gear')) return; /* PERSONAL-COMPLETE: the gear is an icon, not a label. */""",
    "R20 lang map skips gear")
# has no mini-profiles; the orb is the creator file's .fc-pick-av, initial only)
RAIL_ASIDE = """<aside id="pcRail" class="os-view on" data-os-view="home" aria-label="People around you">
  <div class="pc-rail-head">
    <h3>People around you</h3>
    <p class="pc-rail-sub"><span id="pcLiveCount">6 live matches</span> &middot; <span id="pcStandCount">14 standing</span></p>
    <p class="pc-rail-note">Live matches come from the Smart Feed engine, with their reasons attached. Standing profiles are the family, marked as standing &mdash; never shown as online.</p>
  </div>
  <div class="pc-rail-list" id="pcRailList"></div>
  <p class="pc-rail-foot">One more seat is held open for the next live citizen.</p>
</aside>"""
assert "RAIL_ASIDE_PLACEHOLDER" in text, "R18 rail placeholder missing"
text = text.replace("RAIL_ASIDE_PLACEHOLDER", RAIL_ASIDE, 1)

OVERRIDE_CSS = """<style id="personal-complete-20261113">
/* ═══ PERSONAL-COMPLETE 2026-11-13 — Shawn's seven-item list, this round's overrides.
   The base CSS keeps its history (incl. the F1 Join-biggest ruling, 2026-11-12
   16:06Z); this block supersedes it where his 2026-11-13 list says otherwise.
   Everything in this block is measured at 390 / 1440 / 360 after the build. */
/* (1) EIGHT EVEN BUTTONS — desktop: one line, eight equal shares. Join is one of
   the eight (its green glow stays; the 220px basis and the 90px Skills rule go). */
@media(min-width:641px){
  .up-actions{justify-content:center;gap:8px;align-items:center;}
  .up-act{flex:1 1 0;min-width:0;max-width:none;font-size:12px;padding:12px 8px;}
  #skillsbtn{flex:1 1 0;min-width:0;max-width:none;}
  #joinbtn{flex:1 1 0;min-width:0;max-width:none;font-size:12px;padding:12px 8px;}
}
/* (1) phone: a real 2-column grid — Join takes exactly one column, never full width. */
@media(max-width:640px){
  .up-actions{display:grid;grid-template-columns:1fr 1fr;gap:8px;}
  .up-actions .up-act{flex:none;width:auto;max-width:none;height:46px;}
  #joinbtn{order:9;flex:none;font-size:13px;padding:12px 8px;letter-spacing:0;}
}
/* (1) Settings — a small tool icon in the cover, beside Change cover. It keeps
   its id + data-os-go, so the existing wiring opens Settings. Desktop: beside
   Change cover. Phone: BELOW Change cover (the membership links occupy the
   cover's top-left at phone widths — beside Change cover there the gear sat on
   them and could not be tapped). Short-height: below the moved Change cover. */
.pc-gear{width:48px;height:48px;padding:0;font-size:20px;display:inline-flex;align-items:center;justify-content:center;}
@media(min-width:641px){.pc-gear{top:76px;right:196px;}}
@media(max-width:640px){.pc-gear{top:64px;right:10px;}}
@media (max-height:500px) and (max-width:760px){.pc-gear{top:64px;left:10px;right:auto;}}
/* (2) both floating pluses gone — the + lives only in the bottom bar now. */
#pluswrap,#os-rooms-plus,#os-eco-plus{display:none!important;}
/* (2) four segs fit the bar at 390 — the gap drops so the row never squeezes. */
@media(max-width:400px){.notif-row{gap:24px;}}
/* (3) THE LINE — harvested verbatim from the creator-fix A-fix (creator file,
   .notif-seg, FIX-20261112-A): the page-wide button shadow's inset top line is
   restated away on the seg itself; the tile's own rim light is untouched. */
.notif-seg{box-shadow: inset 0 -2px 8px rgba(0,0,0,.25), 0 6px 20px rgba(0,0,0,.4)!important;}
/* (5) the feed line — the Hub's pill language, quiet label, literal words. */
.pc-feedline{text-align:center;font-size:12px;font-weight:800;letter-spacing:.22em;color:#cfc9da;margin:14px 0 10px;text-transform:uppercase;}
/* (7) THE SIDE RAIL — feed + rail as one grid at desktop; the rail stacks below
   the feed at phone. No scroll until the people overflow the page: the list
   scrolls only when its content passes the viewport room. */
.pc-feedwrap{display:grid;grid-template-columns:minmax(0,1fr) 320px;gap:18px;align-items:start;}
#pcRail{min-width:0;}
.pc-rail-head h3{margin:2px 0 4px;font-size:16px;font-weight:900;color:#fff;letter-spacing:.02em;}
.pc-rail-sub{margin:0 0 6px;font-size:12px;font-weight:800;color:#cfc9da;}
.pc-rail-note{margin:0 0 12px;font-size:12px;line-height:1.5;color:#8f8898;}
.pc-rail-list{max-height:calc(100vh - 220px);overflow-y:auto;display:flex;flex-direction:column;gap:10px;padding-right:2px;}
.pc-rail-sec{margin:6px 0 0;font-size:11px;font-weight:900;letter-spacing:.18em;color:#8f8898;text-transform:uppercase;}
.pc-card{background:linear-gradient(180deg,rgba(255,255,255,.07),rgba(255,255,255,.02) 45%,rgba(0,0,0,.25));border:1.5px solid rgba(255,255,255,.16);border-radius:16px;padding:12px;box-shadow:inset 0 1px 0 rgba(255,255,255,.18),inset 0 -4px 10px rgba(0,0,0,.35),0 8px 22px rgba(0,0,0,.45);}
.pc-card-top{display:flex;align-items:center;gap:10px;min-width:0;}
.pc-rail-list .fc-pick-av{width:54px;height:54px;font-size:20px;}
.pc-card-id{flex:1;min-width:0;display:flex;flex-direction:column;gap:2px;}
.pc-card-id b{font-size:14px;color:#fff;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.pc-pct{font-size:13px;font-weight:900;color:#2fe89e;}
.pc-mark{font-size:10px;font-weight:900;letter-spacing:.14em;color:#ffbf3d;}
.pc-mark.you{color:#3fb8ff;}
.pc-nut{margin:8px 0 0;font-size:12.5px;line-height:1.5;color:#e8e8ec;}
.pc-reasons{margin:6px 0 0;font-size:11px;line-height:1.5;color:#8f8898;}
.pc-btns{display:flex;gap:6px;margin-top:10px;}
.pc-btn{flex:1 1 0;min-width:0;padding:8px 2px;border-radius:999px;border:1.5px solid var(--mc,#a06bff);background:rgba(255,255,255,.05);color:#fff;font-size:12px;font-weight:800;cursor:pointer;font-family:inherit;box-shadow:inset 0 1px 0 rgba(255,255,255,.18),0 3px 10px rgba(0,0,0,.4);}
.pc-btn:hover{box-shadow:inset 0 1px 0 rgba(255,255,255,.25),0 0 16px -4px var(--mc,#a06bff),0 4px 12px rgba(0,0,0,.5);}
.pc-rail-foot{margin:10px 0 0;font-size:11.5px;line-height:1.5;color:#8f8898;}
@media(max-width:1023px){
  .pc-feedwrap{grid-template-columns:1fr;}
  .pc-rail-list{max-height:none;overflow:visible;}
}
</style>"""
# --- R21: the feedname hidden mechanism — the base's .mw-feedname{display:block}
# defeats the hidden attribute, so all three feedname lines showed at once (seen
# in the 1440 eye-check). The code already toggles .hidden per tab; make it work.
OVERRIDE_CSS = OVERRIDE_CSS.replace(
    "/* (5) the feed line",
    "/* (5) the feedname lines — only the active tab's line shows; the base's\n   .mw-feedname{display:block} defeats the hidden attribute otherwise. */\n.mw-feedname[hidden]{display:none!important;}\n/* (5) the feed line", 1)

RAIL_SCRIPT = """<script>
/* ═══ PERSONAL-COMPLETE — the side rail (Shawn 2026-11-13) ═══
   Composed from the Hub's people room + the staged endpoint proof. The orb is
   the creator file's .fc-pick-av (initial by default, spinning sheen) — the
   sharpening binds: INITIALS, NEVER FACES. No face, photo or avatar image is
   rendered in any rail card, ever. The line under the alias is ONE nutshell:
   who you are + what you're about + your thing + your motto, in one line.
   LIVE = endpoint-matched, with the percentage and the reasons the endpoint
   returned. STANDING = the family, marked as standing, never shown as online.
   Chat opens the instant message in place; mail opens it with the subject
   shown. Audio and video have no Smart Meet route on this page yet, so they
   open the same instant message with an honest status line saying so — the
   record names it; no limit numbers appear anywhere on the page. */
(function(){
"use strict";
function esc(s){ var d=document.createElement('div'); d.textContent=String(s==null?'':s); return d.innerHTML; }
var PC_SPECTRUM=['#a06bff','#3fb8ff','#2fe89e','#ffbf3d','#ff9a5a','#ff5e6c','#e84fff'];
function pcColorFor(name){ var s=String(name||'?'), h=0, i; for(i=0;i<s.length;i++) h=(h*31+s.charCodeAt(i))>>>0; return PC_SPECTRUM[h%PC_SPECTRUM.length]; }
window.PC_RAIL_LIVE = LIVE_JSON;
window.PC_RAIL_SEED = SEED_JSON;
function pcCard(p, live){
  var init=(p.alias||'?')[0].toUpperCase();
  var mark = live
    ? '<span class="pc-pct">'+p.pct+'%</span>'
    : (p.you ? '<span class="pc-mark you">YOU &middot; STANDING</span>' : '<span class="pc-mark">STANDING</span>');
  var reasons = live
    ? '<p class="pc-reasons">'+p.reasons.map(function(r){ return esc(r); }).join('<br>')+'</p>'
    : '';
  /* the sharpening: one nutshell line under the alias. A live match carries no
     nutshell from the endpoint (alias + % + reasons only) — so the line is left
     out for live cards rather than invented; the record says so. */
  var nutHtml = p.nut ? '<p class="pc-nut">'+esc(p.nut)+'</p>' : '';
  return '<article class="pc-card" data-pc-alias="'+esc(p.alias)+'">'
    + '<div class="pc-card-top"><span class="fc-pick-av" style="--cc:'+pcColorFor(p.alias)+'">'+esc(init)+'</span>'
    + '<div class="pc-card-id"><b>'+esc(p.alias)+'</b>'+mark+'</div></div>'
    + nutHtml+reasons
    + '<div class="pc-btns">'
    + '<button type="button" class="pc-btn" data-pc-act="chat" style="--mc:#3fb8ff">Chat</button>'
    + '<button type="button" class="pc-btn" data-pc-act="mail" style="--mc:#ffbf3d">Mail</button>'
    + '<button type="button" class="pc-btn" data-pc-act="audio" style="--mc:#2fe89e">Audio</button>'
    + '<button type="button" class="pc-btn" data-pc-act="video" style="--mc:#a06bff">Video</button>'
    + '</div></article>';
}
window.pcRenderRail=function(live, standing){
  var list=document.getElementById('pcRailList'); if(!list) return;
  live=live||window.PC_RAIL_LIVE; standing=standing||window.PC_RAIL_SEED;
  var html='';
  if(live.length) html+='<p class="pc-rail-sec">Live matches</p>'+live.map(function(p){ return pcCard(p, true); }).join('');
  if(standing.length) html+='<p class="pc-rail-sec">Standing</p>'+standing.map(function(p){ return pcCard(p, false); }).join('');
  list.innerHTML=html;
  var lc=document.getElementById('pcLiveCount'); if(lc) lc.textContent=live.length+' live match'+(live.length===1?'':'es');
  var sc=document.getElementById('pcStandCount'); if(sc) sc.textContent=standing.length+' standing';
};
/* the feed + the rail sit side by side: wrap them the moment the rail parses,
   so nothing flashes at the bottom of the page first. */
var wall=document.getElementById('os-wall'), rail=document.getElementById('pcRail');
if(wall&&rail&&wall.parentNode){
  var wrap=document.createElement('div'); wrap.className='pc-feedwrap'; wrap.id='pcFeedWrap';
  wall.parentNode.insertBefore(wrap, wall); wrap.appendChild(wall); wrap.appendChild(rail);
}
window.pcRenderRail();
/* the four buttons: chat + mail open the instant message in place; audio and
   video open it too, with the honest status — no Smart Meet route exists yet. */
document.addEventListener('click', function(e){
  var b=e.target&&e.target.closest?e.target.closest('[data-pc-act]'):null;
  if(!b) return;
  var card=b.closest?b.closest('.pc-card'):null; if(!card) return;
  var alias=card.getAttribute('data-pc-alias')||'guest';
  var act=b.getAttribute('data-pc-act');
  if(typeof window.fcOpenChat!=='function') return;
  window.fcOpenChat({name:alias, alias:alias, kind:'person', mode:(act==='mail'?'mail':'chat')});
  if(act==='audio'||act==='video'){
    var st=document.getElementById('fcChatStatus');
    if(st) st.textContent=(act==='audio'?'Audio calls':'Video calls')+' arrive with Smart Meet — for now, message them here.';
  }
});
/* The keyword box above the feed (#tnSearchPersonalInput) is hidden by Shawn's
   popup-only search law (base: #tnpsBand{display:none!important} — "search is a
   centered popup, never a bar"), so there is NO dead wiring to it here. The
   feed's topic pull is the Smart Tabs ribbon below (author/category pills). */
})();
</script>"""
# Live cards carry alias + % + reasons only — the endpoint returns no nutshell,
# so none is rendered for them (see pcCard). The display name is not a nutshell
# and is not shown as one.
LIVE_JSON = json.dumps(
    [{"alias": p["alias"], "pct": p["pct"], "reasons": p["reasons"]} for p in PC_LIVE],
    ensure_ascii=False)
RAIL_SCRIPT = RAIL_SCRIPT.replace("LIVE_JSON", LIVE_JSON)
RAIL_SCRIPT = RAIL_SCRIPT.replace("SEED_JSON", json.dumps(PC_SEED, ensure_ascii=False))

# --- R19: the fc script + this round's overrides + the rail, before </body>
assert text.count("</body></html>") == 1, "R19 body close count"
text = text.replace("</body></html>", FC_SCRIPT + "\n" + OVERRIDE_CSS + "\n" + RAIL_SCRIPT + "\n</body></html>", 1)

# ================================================================ assertions
def cnt(s, sub):
    return text.count(sub)
assert cnt(text, 'id="os-post-body"') == 1, "os-post-body x%d" % cnt(text, 'id="os-post-body"')
assert cnt(text, 'id="os-post-author"') == 1
assert cnt(text, 'id="os-post-btn"') == 1
assert cnt(text, 'id="tg-review"') == 1
assert cnt(text, 'id="fcCreator"') == 1 and cnt(text, 'id="fcPlusMenu"') == 1
assert cnt(text, 'id="fcChat"') == 1 and cnt(text, 'id="fcPicker"') == 1
assert cnt(text, 'id="fcCreateRow"') == 1
assert cnt(text, 'id="mwFeedActivity"') == 0, "activity panel must be gone"
assert cnt(text, '<b>Activity</b>') == 0, "activity tab label must be gone"
assert cnt(text, 'Make a post</h3>') == 0, "always-open composer must be gone"
assert cnt(text, 'data-mw-tab="smart"') == 0 and cnt(text, "mwApplyFeedTab('smart')") == 0
assert cnt(text, "mwApplyFeedTab('activity')") == 0
assert cnt(text, 'MATCH &rarr; ORGANIZE &rarr; CONNECT') == 1, "feed line"
assert cnt(text, 'id="pcRail"') == 1 and cnt(text, 'id="pcRailList"') == 1
assert cnt(text, 'data-notif="plus"') == 2, "plus seg refs: the fc script's two selectors only (built by JS, not markup)"
assert 'SEGS = ' in text and "'plus', 'ADD'" in text, "plus seg first"
assert text.count('id="settingsbtn"') == 1
# the points pill + hero alignment: name, pill, tagline lines untouched
for frag in ('<div class="ph-nm" id="pname" title="Click to edit">Shawn Vibert</div>',
             '<div class="ph-points" id="pointsdisplay"',
             '<span id="pointscount">',
             '<div class="ph-tg" id="ptag" title="Click to edit">Welcome to my world'):
    assert frag in text, "hero fragment missing: %r" % frag[:50]
# no limit numbers anywhere in the new copy (build context only: video 6 / audio 10)
assert "up to 6" not in text and "up to 10" not in text, "limit numbers leaked"
# no face in the rail: the rail script renders initials only; no <img> in RAIL_SCRIPT
assert "<img" not in RAIL_SCRIPT, "rail must never render an image"

out = text.encode("utf-8")
with open(WT, "wb") as f: f.write(out)
new_sha = sha(out)
print("WROTE %s  sha %s  %d bytes  %d lines" % (WT, new_sha, len(out), len(text.split("\n"))))

# --- the diff, for the record: every hunk named
diff = list(difflib.unified_diff(orig_lines, text.split("\n"), lineterm="", n=1))
print("--- DIFF (%d lines) ---" % len(diff))
hunks = [l for l in diff if l.startswith("@@")]
print("hunks: %d" % len(hunks))
for h in hunks: print(h)
with open("/home/hatch/workspace/team-nitro/personal-page-complete-20261113/diff-complete.txt", "w") as f:
    f.write("\n".join(diff))
print("diff saved")
