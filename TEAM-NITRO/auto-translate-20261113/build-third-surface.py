#!/usr/bin/env python3
"""Third-surface auto-translate fix — build the edited page IN MEMORY.

Reads the F1 base file, grows the dictionary in memory (same code as
apply-third-surface-dict.py), edits the language-block template, regenerates
the built file's language span from template + grown dict, then applies every
render-site edit with exact-count assertions. Prints the edited HTML to
STDOUT and a verification report to STDERR. Writes NO files (the EPERM
flake blocks exec writes; the caller pipes stdout to the filing path).

Usage: python3 build-third-surface.py <base.html> <mw-lang-block.js> <apply-dict.py>
"""
import sys, re, json, hashlib

BASE, TPL, DICTSCRIPT = sys.argv[1], sys.argv[2], sys.argv[3]
failures = []

def rep(html, old, new, expect=1, tag=""):
    global failures
    n = html.count(old)
    if n != expect:
        failures.append(f"REP {tag}: expected {expect}, found {n}: {old[:110]!r}")
        return html
    return html.replace(old, new)

def rep_re(html, pattern, repl, expect=1, tag=""):
    global failures
    n = len(re.findall(pattern, html))
    if n != expect:
        failures.append(f"REP_RE {tag}: expected {expect}, found {n}: {pattern[:110]!r}")
        return html
    return re.sub(pattern, repl, html)

# ---------- grown dictionary (in memory; same assertions as apply script) ----------
src = open(DICTSCRIPT, encoding="utf-8").read()
head = src.split("def main():")[0]
g = {}
exec(head, g)
NEW, FIXES, IDENTICAL_OK, DE_LEAK = g["NEW"], g["FIXES"], g["IDENTICAL_OK"], g["DE_LEAK"]
html0 = open(BASE, encoding="utf-8").read()
m0 = re.search(r"var MW_I18N\s*=\s*(\{.*?\});", html0, re.S)
assert m0, "MW_I18N not found in base"
d = json.loads(m0.group(1))
assert {k: len(v) for k, v in d.items()} == {"es": 266, "fr": 266, "de": 266}, "base dict not 266"
for k, es, fr, de in NEW:
    for lang in ("es", "fr", "de"):
        assert k not in d[lang], f"COLLISION {k!r} in {lang}"
    for lang, v in (("es", es), ("fr", fr), ("de", de)):
        assert isinstance(v, str) and v
        if lang in ("es", "fr"):
            assert not [c for c in v if c in DE_LEAK], f"DE-leak {k!r} {lang}"
        if "NayaNET" in k: assert "NayaNET" in v
        if "Naya" in k: assert "Naya" in v
        if v == k and (k, lang) not in IDENTICAL_OK:
            raise AssertionError(f"identical not allowlisted: {k!r} {lang}")
    d["es"][k] = es; d["fr"][k] = fr; d["de"][k] = de
for lang, k, old, new in FIXES:
    assert d[lang].get(k) == old, f"FIX precond {lang} {k!r}"
    d[lang][k] = new
assert {k: len(v) for k, v in d.items()} == {"es": 266 + len(NEW), "fr": 266 + len(NEW), "de": 266 + len(NEW)}
DICT_JSON = json.dumps(d, ensure_ascii=False, indent=1, sort_keys=True)
print(f"DICT grown: 266 -> {266 + len(NEW)} keys/language ({len(NEW)} new + 2 fixes)", file=sys.stderr)

# ---------- template edits (mw-lang-block.js) ----------
tpl = open(TPL, encoding="utf-8").read()
TPL_ORIG = tpl
# (T1) mwLocale helper, before the window exposure line.
tpl = rep(tpl,
  "window.mwTr=mwTr; window.mwLangCode=mwLangCode; window.mwBrowserLang=mwBrowserLang;",
  "function mwLocale(){\n  var c=mwLangCode();\n  return c==='es'?'es-ES':c==='fr'?'fr-FR':c==='de'?'de-DE':'en-US';\n}\nwindow.mwLocale=mwLocale;\nwindow.mwTr=mwTr; window.mwLangCode=mwLangCode; window.mwBrowserLang=mwBrowserLang;",
  tag="T1-mwLocale")
# (T2) [data-mw-title] pass, after the [data-mw-aria] pass.
tpl = rep(tpl,
  """  document.querySelectorAll('[data-mw-aria]').forEach(function(el){
    var en=el.getAttribute('data-mw-aria')||'';
    if(!en) return;
    el.setAttribute('aria-label',(code==='en')?en:(dict[en]||en));
  });""",
  """  document.querySelectorAll('[data-mw-aria]').forEach(function(el){
    var en=el.getAttribute('data-mw-aria')||'';
    if(!en) return;
    el.setAttribute('aria-label',(code==='en')?en:(dict[en]||en));
  });
  /* THIRD-SURFACE-FIX: title attributes ride the same shape as aria-labels —
     the English key rides in data-mw-title, re-synced in place on switch. */
  document.querySelectorAll('[data-mw-title]').forEach(function(el){
    var en=el.getAttribute('data-mw-title')||'';
    if(!en) return;
    el.setAttribute('title',(code==='en')?en:(dict[en]||en));
  });""",
  tag="T2-mw-title-pass")
# (T3) feedback Send button joins byId.
tpl = rep(tpl, "fcChatSend:'Send'};", "fcChatSend:'Send','os-dash-fb-btn':'Send'};", tag="T3-byId-fb")
# (T4) re-sync hooks before the Translate-taps dispatch.
tpl = rep(tpl,
  "  /* AUTO-TRANSLATE: the Translate taps re-label with the chrome. */",
  """  /* THIRD-SURFACE-FIX: re-sync every surface this round routed through mwTr
     that paints once and never re-renders — record/note/link buttons, the
     wall meta line, the dashboard (via its own re-renderer), My World rows,
     feed pills and the Notes filter. Each call is guarded: a surface that
     has not painted yet is simply skipped. */
  var T=function(en){ return (code==='en')?en:(dict[en]||en); };
  try{
    document.querySelectorAll('[data-mn-rec]').forEach(function(b){
      var k=b.getAttribute('data-mn-rec');
      b.textContent=(k==='video'?'\\uD83C\\uDFa5 ':'\\uD83C\\uDF99 ')+T(k==='video'?'Record video note':'Record voice note');
    });
  }catch(e){}
  try{
    document.querySelectorAll('[data-nn-copy]').forEach(function(b){ b.textContent=T('Copy'); });
    document.querySelectorAll('[data-nn-move]').forEach(function(b){ b.textContent=T('Move'); });
    document.querySelectorAll('[data-nn-list]').forEach(function(b){ b.textContent=T('List'); });
    document.querySelectorAll('[data-nn-unfile]').forEach(function(b){ b.textContent=T('Unfile'); });
    document.querySelectorAll('[data-mn-copylink]').forEach(function(b){ b.textContent=T('Copy link'); });
    document.querySelectorAll('[data-mn-play]').forEach(function(b){ b.setAttribute('aria-label',T('Play the voice note')); });
    document.querySelectorAll('[data-mn-vplay]').forEach(function(b){ b.setAttribute('aria-label',T('Play the video note')); });
    document.querySelectorAll('[data-nn-in]').forEach(function(el){
      el.textContent=T('In: ')+el.textContent.replace(/^(In: |En: |Dans : )/,'');
    });
    document.querySelectorAll('[data-sl-copy]').forEach(function(b){ b.textContent=T('Copy the link'); });
    document.querySelectorAll('[data-sl-open]').forEach(function(b){ b.textContent=T('Open it'); });
    document.querySelectorAll('[data-sl-dim]').forEach(function(b){ b.textContent=T('Breakdown'); });
    document.querySelectorAll('[data-dash-retry-links]').forEach(function(b){ b.textContent=T('Retry'); });
    document.querySelectorAll('.os-rel[data-at]').forEach(function(el){
      if(window.relLabel){ try{ el.textContent=window.relLabel(el.getAttribute('data-at')); }catch(e){} }
    });
    var af=document.querySelector('[data-nn-filter="All"]'); if(af) af.textContent=T('All');
  }catch(e){}
  if(window.mwSyncDashCtx){ try{ window.mwSyncDashCtx(); }catch(e){} }
  if(window.osRerenderDashboard){ try{ window.osRerenderDashboard(); }catch(e){} }
  if(window.mwRenderMyWorld){ try{ window.mwRenderMyWorld(); }catch(e){} }
  if(window.mwBuildFeedPills){ try{ window.mwBuildFeedPills(); }catch(e){} }
  if(window.mwSyncWallMeta){ try{ window.mwSyncWallMeta(); }catch(e){} }
  /* AUTO-TRANSLATE: the Translate taps re-label with the chrome. */""",
  tag="T4-hooks")

# ---------- span regeneration (boundary-asserted) ----------
SPAN_START = "/* ---------- language (fix 18, grown AUTO-TRANSLATE 2026-11-13) ---------- */"
SPAN_END = "/* ---------- settings binding ---------- */"
s0 = html0.index(SPAN_START)
s1 = html0.index(SPAN_END)
old_span = html0[s0:s1]
# identity check: old span with its JSON replaced by the placeholder == original template
old_span_code = re.sub(r"var MW_I18N=.*?;\n", "var MW_I18N=/*__MW_I18N_JSON__*/;\n", old_span, count=1, flags=re.S)
if old_span_code != TPL_ORIG:
    # report first diff to stderr for diagnosis
    import difflib
    for line in list(difflib.unified_diff(TPL_ORIG.splitlines(), old_span_code.splitlines(), lineterm=""))[:40]:
        print("SPAN-DIFF:", line, file=sys.stderr)
    failures.append("SPAN identity: built span code != mw-lang-block.js template")
new_span = tpl.replace("/*__MW_I18N_JSON__*/", DICT_JSON)
html = html0[:s0] + new_span + html0[s1:]
print(f"SPAN regenerated: old {len(old_span)} chars -> new {len(new_span)} chars", file=sys.stderr)

# ---------- S1: composer static (Notes view) ----------
html = rep(html, '<span class="ph-dot" style="background:#a06bff;color:#a06bff;"></span> Smart Notes</div>',
  '<span class="ph-dot" style="background:#a06bff;color:#a06bff;"></span> <span data-mw-tr="composer">Smart Notes</span></div>', tag="S1-smartnotes-title")
html = rep(html, '<a class="ph-connect" href="https://nayanet.app/rooms/library">Open the Library →</a>',
  '<a class="ph-connect" href="https://nayanet.app/rooms/library"><span data-mw-tr="composer">Open the Library →</span></a>', tag="S1-library")
html = rep(html, '<h3><span class="os-jewel os-jewel-h" style="--jc:#a06bff">✦</span> Quick Capture</h3>',
  '<h3><span class="os-jewel os-jewel-h" style="--jc:#a06bff">✦</span> <span data-mw-tr="composer">Quick Capture</span></h3>', tag="S1-quickcapture")
html = rep(html, '<p>Smart note this &mdash; capture a thought, and it lands here as a card in this app.</p>',
  '<p data-mw-tr="composer">Smart note this &mdash; capture a thought, and it lands here as a card in this app.</p>', tag="S1-smartnote-this")
html = rep(html, '<input class="os-input" id="os-note-capture" type="text" placeholder="What&rsquo;s on your mind?" style="flex:1;margin:0;">',
  '<input class="os-input" id="os-note-capture" type="text" placeholder="What&rsquo;s on your mind?" data-mw-ph="composer" style="flex:1;margin:0;">', tag="S1-capture-ph")
html = rep(html, '<button class="ph-connect" id="os-note-capture-btn" type="button" style="padding:12px 24px;">Note it</button>',
  '<button class="ph-connect" id="os-note-capture-btn" type="button" style="padding:12px 24px;"><span data-mw-tr="composer">Note it</span></button>', tag="S1-noteit")
html = rep(html, '<h3><span class="os-jewel os-jewel-h" style="--jc:#3fb8ff">📝</span> Naya Notes</h3>',
  '<h3><span class="os-jewel os-jewel-h" style="--jc:#3fb8ff">📝</span> <span data-mw-tr="composer">Naya Notes</span></h3>', tag="S1-nayanotes-h3")
html = rep(html, '<p>Your private notes to Naya — the same store your Hub home reads, here in this app. Not Smart Notes: these never enter any feed. Messages you save from the Inbox land here too.</p>',
  '<p data-mw-tr="composer">Your private notes to Naya — the same store your Hub home reads, here in this app. Not Smart Notes: these never enter any feed. Messages you save from the Inbox land here too.</p>', tag="S1-nn-para")
html = rep(html, '<input class="os-input" id="os-nn-title" type="text" placeholder="Title (optional)" autocomplete="off">',
  '<input class="os-input" id="os-nn-title" type="text" placeholder="Title (optional)" data-mw-ph="composer" autocomplete="off">', tag="S1-title-ph")
html = rep(html, 'data-os-mic="os-nn-title" aria-label="Dictate the title"',
  'data-os-mic="os-nn-title" data-mw-aria="Dictate the title" aria-label="Dictate the title"', tag="S1-dictate-title")
html = rep(html, '<textarea class="os-textarea" id="os-nn-body" rows="3" placeholder="Write a note to Naya&hellip;">',
  '<textarea class="os-textarea" id="os-nn-body" rows="3" placeholder="Write a note to Naya&hellip;" data-mw-ph="composer">', tag="S1-body-ph")
html = rep(html, 'data-os-mic="os-nn-body" aria-label="Dictate the note"',
  'data-os-mic="os-nn-body" data-mw-aria="Dictate the note" aria-label="Dictate the note"', tag="S1-dictate-note")
html = rep(html, '<input class="os-input" id="os-nn-newcat" type="text" placeholder="&hellip;or name a new category" autocomplete="off">',
  '<input class="os-input" id="os-nn-newcat" type="text" placeholder="&hellip;or name a new category" data-mw-ph="composer" autocomplete="off">', tag="S1-newcat-ph")
html = rep(html, '<button class="ph-connect" id="os-nn-save" type="button">Save note</button>',
  '<button class="ph-connect" id="os-nn-save" type="button"><span data-mw-tr="composer">Save note</span></button>', tag="S1-savenote")

# ---------- S2: feed chrome (aria-labels) ----------
html = rep(html, '<div class="fc-create-row" id="fcCreateRow" role="group" aria-label="Create on this feed">',
  '<div class="fc-create-row" id="fcCreateRow" role="group" aria-label="Create on this feed" data-mw-aria="Create on this feed">', tag="S2-create-row")
html = rep(html, '<div class="lens-tabs" id="mwFeedTabs" role="tablist" aria-label="Feed categories">',
  '<div class="lens-tabs" id="mwFeedTabs" role="tablist" aria-label="Feed categories" data-mw-aria="Feed categories">', tag="S2-feedcats")
html = rep(html, '<div class="pc-feedline" aria-label="How the feed works" data-mw-tr="feedline">',
  '<div class="pc-feedline" aria-label="How the feed works" data-mw-aria="How the feed works" data-mw-tr="feedline">', tag="S2-feedline")
html = rep(html, '<div class="smart-tabs" id="mwFeedPills" aria-label="Feed filters"></div>',
  '<div class="smart-tabs" id="mwFeedPills" aria-label="Feed filters" data-mw-aria="Feed filters"></div>', tag="S2-feedfilters")

# ---------- S3: My World checkboxes (Settings) ----------
for key in ("Personal", "Business", "Contacts", "About"):
    html = rep(html, f'<label for="mw-set-mw-{key.lower()}">{key}</label>',
      f'<label for="mw-set-mw-{key.lower()}"><span data-mw-tr="mwshow">{key}</span></label>', tag=f"S3-mw-{key.lower()}")

# ---------- S4: avatar tooltip ----------
html = rep(html, '<div class="ph-av" id="avv">',
  '<div class="ph-av" id="avv" data-mw-title="Tap to change your picture">', tag="S4-avv-title")
html = rep(html, "if (avvEl){ avvEl.style.cursor='pointer'; avvEl.title='Tap to change your picture'; }",
  "if (avvEl){ avvEl.style.cursor='pointer'; avvEl.title=(window.mwTr?window.mwTr('Tap to change your picture'):'Tap to change your picture'); }", tag="S4-avv-boot")

# ---------- S5: Dashboard view static ----------
html = rep(html, '<span class="ph-dot" style="background:#e84fff;color:#e84fff;"></span> Your World, Live &middot; Dashboard</div>',
  '<span class="ph-dot" style="background:#e84fff;color:#e84fff;"></span> <span data-mw-tr="dash">Your World, Live &middot; Dashboard</span></div>', tag="S5-dash-title")
html = rep(html, '<p class="tn-hero-voice" data-tn-voice="hero" aria-label="Naya reads your score"></p>',
  '<p class="tn-hero-voice" data-tn-voice="hero" aria-label="Naya reads your score" data-mw-aria="Naya reads your score"></p>', tag="S5-hero-voice")
html = rep(html, '<div class="os-ld-timepills" id="os-ld-timepills" role="tablist" aria-label="Time window">',
  '<div class="os-ld-timepills" id="os-ld-timepills" role="tablist" aria-label="Time window" data-mw-aria="Time window">', tag="S5-timewindow")
for _pill, _lab in (("daily", "Day"), ("weekly", "Week"), ("monthly", "Month"), ("all", "All")):
    html = rep(html, f'<button type="button" data-ldtw="{_pill}" role="tab">{_lab}</button>' if _pill != "all" else '<button type="button" data-ldtw="all" role="tab" class="on">All</button>',
      f'<button type="button" data-ldtw="{_pill}" role="tab"{"" if _pill != "all" else " class=\"on\""}><span data-mw-tr="dash">{_lab}</span></button>', tag=f"S5-pill-{_pill}")
html = rep(html, '<div class="os-se-label">SMART SCORE</div>',
  '<div class="os-se-label"><span data-mw-tr="dash">SMART SCORE</span></div>', tag="S5-smartscore")
html = rep(html, '<div class="os-ld-drawer" id="os-ld-drawer" role="dialog" aria-label="Source detail" aria-hidden="true">',
  '<div class="os-ld-drawer" id="os-ld-drawer" role="dialog" aria-label="Source detail" data-mw-aria="Source detail" aria-hidden="true">', tag="S5-drawer")
html = rep(html, '<button type="button" class="os-ld-drawer-x" id="os-ld-drawer-x" aria-label="Close detail">×</button>',
  '<button type="button" class="os-ld-drawer-x" id="os-ld-drawer-x" aria-label="Close detail" data-mw-aria="Close detail">×</button>', tag="S5-drawer-x")
html = rep(html, 'cursor:pointer;">× clear</button></div>',
  'cursor:pointer;"><span data-mw-tr="dash">× clear</span></button></div>', tag="S5-dashctx-x")
# pulse cards: title -> data-mw-title, label -> inner span
for _go, _title, _lab in (
  ("home", "Open the Live Feed — where these posts live", "FEED POSTS"),
  ("inbox", "Open the Smart Mail inbox — where these messages live", "MESSAGES RECEIVED"),
  ("growth", "Open Smart Growth — where these invites live", "INVITES RECORDED"),
  ("people", "Open Connections — where these people live", "PEOPLE AROUND YOU")):
    html = rep(html, f'data-os-go="{_go}" title="{_title}"',
      f'data-os-go="{_go}" title="{_title}" data-mw-title="{_title}"', tag=f"S5-pulse-title-{_go}")
    html = rep(html, f'</span> {_lab}</div>', f'</span> <span data-mw-tr="dash">{_lab}</span></div>', tag=f"S5-pulse-lab-{_go}")
# notif chips
for _kind, _lab in (("activity", "Activity"), ("mail", "Mail"), ("stats", "Stats")):
    html = rep(html, f'>{_lab} <span id="os-notif-n-{_kind}"></span></button>',
      f'><span data-mw-tr="dash">{_lab}</span> <span id="os-notif-n-{_kind}"></span></button>', tag=f"S5-chip-{_kind}")
html = rep(html, '<div class="os-mw-list" id="os-notif-list"><p class="os-note">Reading your notifications&hellip;</p></div>',
  '<div class="os-mw-list" id="os-notif-list"><p class="os-note" data-mw-tr="dash">Reading your notifications&hellip;</p></div>', tag="S5-notif-reading")
html = rep(html, '<button class="ph-msg" type="button" id="os-notif-showall" hidden>Show all</button>',
  '<button class="ph-msg" type="button" id="os-notif-showall" hidden><span data-mw-tr="dash">Show all</span></button>', tag="S5-showall")
html = rep(html, '<h3><span class="os-jewel os-jewel-h" style="--jc:#a06bff">🔔</span> Notifications</h3>',
  '<h3><span class="os-jewel os-jewel-h" style="--jc:#a06bff">🔔</span> <span data-mw-tr="dash">Notifications</span></h3>', tag="S5-notif-h3")
html = rep(html, '<h3><span class="os-jewel os-jewel-h" style="--jc:#ff9a5a">✦</span> Smart notes in this world</h3>',
  '<h3><span class="os-jewel os-jewel-h" style="--jc:#ff9a5a">✦</span> <span data-mw-tr="dash">Smart notes in this world</span></h3>', tag="S5-mwnotes-h3")
html = rep(html, '<div class="os-mw-list" id="os-myworld-notes-list"><p class="os-note">Reading your Smart Notes&hellip;</p></div>',
  '<div class="os-mw-list" id="os-myworld-notes-list"><p class="os-note" data-mw-tr="dash">Reading your Smart Notes&hellip;</p></div>', tag="S5-mwnotes-reading")
html = rep(html, '<h3><span class="os-jewel os-jewel-h" style="--jc:#2fe89e">🌍</span> Joined pages &amp; spaces</h3>',
  '<h3><span class="os-jewel os-jewel-h" style="--jc:#2fe89e">🌍</span> <span data-mw-tr="dash">Joined pages &amp; spaces</span></h3>', tag="S5-joined-h3")
html = rep(html, '<div class="os-mw-list" id="os-myworld-joined-list"><p class="os-note">Reading your pages &amp; spaces&hellip;</p></div>',
  '<div class="os-mw-list" id="os-myworld-joined-list"><p class="os-note" data-mw-tr="dash">Reading your pages &amp; spaces&hellip;</p></div>', tag="S5-joined-reading")
html = rep(html, '>🔗</span> Smart Links <span class="os-sl-live"><i></i>LIVE</span></h3>',
  '>🔗</span> <span data-mw-tr="dash">Smart Links</span> <span class="os-sl-live"><i></i><span data-mw-tr="dash">LIVE</span></span></h3>', tag="S5-sllinks-h3")
html = rep(html, '<p class="os-note" id="os-dash-links-head">Reading your links&hellip;</p>',
  '<p class="os-note" id="os-dash-links-head" data-mw-tr="dash">Reading your links&hellip;</p>', tag="S5-links-head")
html = rep(html, '<h3><span class="os-jewel os-jewel-h" style="--jc:#3fb8ff">📈</span> The trend</h3>',
  '<h3><span class="os-jewel os-jewel-h" style="--jc:#3fb8ff">📈</span> <span data-mw-tr="dash">The trend</span></h3>', tag="S5-trend-h3")
for _per, _lab in (("7", "7 days"), ("30", "30 days"), ("0", "All")):
    html = rep(html, f'data-period="{_per}" style="--pc:#3fb8ff;">{_lab}</button>',
      f'data-period="{_per}" style="--pc:#3fb8ff;"><span data-mw-tr="dash">{_lab}</span></button>', tag=f"S5-period-{_per}")
html = rep_re(html, r'(<button type="button"[^>]*data-kind="[a-z]+" style="--pc:#[0-9a-f]+;">)(All|Posts|Notes|Messages|Invites)(</button>)',
  r'\1<span data-mw-tr="dash">\2</span>\3', expect=5, tag="S5-kind-buttons")
html = rep(html, '<p class="os-note" id="os-dash-week-note">Reading this world&rsquo;s own activity&hellip;</p>',
  '<p class="os-note" id="os-dash-week-note" data-mw-tr="dash">Reading this world&rsquo;s own activity&hellip;</p>', tag="S5-week-note")
html = rep(html, '<h3><span class="os-jewel os-jewel-h" style="--jc:#ff5e6c">🧭</span> The invite journey</h3>',
  '<h3><span class="os-jewel os-jewel-h" style="--jc:#ff5e6c">🧭</span> <span data-mw-tr="dash">The invite journey</span></h3>', expect=2, tag="S5-funnel-h3")
html = rep(html, '<h3><span class="os-jewel os-jewel-h" style="--jc:#e84fff">📊</span> Activity mix</h3>',
  '<h3><span class="os-jewel os-jewel-h" style="--jc:#e84fff">📊</span> <span data-mw-tr="dash">Activity mix</span></h3>', tag="S5-donut-h3")
html = rep(html, '<span class="os-donut-cap">TOTAL</span>',
  '<span class="os-donut-cap"><span data-mw-tr="dash">TOTAL</span></span>', expect=2, tag="S5-donut-total")
for _lab, _id in (("Feed posts", "posts"), ("Messages received", "messages"), ("Invites recorded", "invites")):
    html = rep(html, f'</span>{_lab}<b id="os-dash-leg-{_id}">',
      f'</span><span data-mw-tr="dash">{_lab}</span><b id="os-dash-leg-{_id}">', tag=f"S5-legend-{_id}")
html = rep(html, '<h3><span class="os-jewel os-jewel-h" style="--jc:#2fe89e">👥</span> Faces in your world</h3>',
  '<h3><span class="os-jewel os-jewel-h" style="--jc:#2fe89e">👥</span> <span data-mw-tr="dash">Faces in your world</span></h3>', tag="S5-faces-h3")
html = rep(html, '<p class="os-note" id="os-dash-faces-head">Reading the faces&hellip;</p>',
  '<p class="os-note" id="os-dash-faces-head" data-mw-tr="dash">Reading the faces&hellip;</p>', tag="S5-faces-head")
html = rep(html, '<button class="ph-msg" type="button" data-os-go="people">See everyone</button>',
  '<button class="ph-msg" type="button" data-os-go="people"><span data-mw-tr="dash">See everyone</span></button>', expect=2, tag="S5-see-everyone")
html = rep(html, '<h3><span class="os-jewel os-jewel-h" style="--jc:#2fe89e">💡</span> Your next best moves</h3>',
  '<h3><span class="os-jewel os-jewel-h" style="--jc:#2fe89e">💡</span> <span data-mw-tr="dash">Your next best moves</span></h3>', tag="S5-moves-h3")
html = rep(html, '<h3><span class="os-jewel os-jewel-h" style="--jc:#ffbf3d">💬</span> Latest conversations</h3>',
  '<h3><span class="os-jewel os-jewel-h" style="--jc:#ffbf3d">💬</span> <span data-mw-tr="dash">Latest conversations</span></h3>', tag="S5-convos-h3")
html = rep(html, '<button class="ph-msg" type="button" data-os-go="inbox">Open the inbox</button>',
  '<button class="ph-msg" type="button" data-os-go="inbox"><span data-mw-tr="dash">Open the inbox</span></button>', tag="S5-open-inbox")
html = rep(html, '<h3><span class="os-jewel os-jewel-h" style="--jc:#ff5e6c">🔥</span> Heat &amp; streaks</h3>',
  '<h3><span class="os-jewel os-jewel-h" style="--jc:#ff5e6c">🔥</span> <span data-mw-tr="dash">Heat &amp; streaks</span></h3>', tag="S5-heat-h3")
html = rep(html, '<p class="os-note">The last fourteen days of this world &mdash; every post, note, message and invite, day by day.</p>',
  '<p class="os-note" data-mw-tr="dash">The last fourteen days of this world &mdash; every post, note, message and invite, day by day.</p>', tag="S5-heat-note")
html = rep(html, '<p class="os-note" id="os-dash-heat-note">Reading the days&hellip;</p>',
  '<p class="os-note" id="os-dash-heat-note" data-mw-tr="dash">Reading the days&hellip;</p>', tag="S5-heat-reading")
# plugin + room cards: names, chips, notes, feeds lines, doors, how paragraphs
html = rep_re(html, r'(<span class="os-src-name">)([^<]+)(</span>)',
  r'\1<span data-mw-tr="dash">\2</span>\3', expect=19, tag="S5-src-names")
html = rep_re(html, r'(<span class="os-src-chip live">)(LIVE)(</span>)',
  r'\1<span data-mw-tr="dash">\2</span>\3', expect=13, tag="S5-chip-live")
html = rep(html, '<span class="os-src-chip born">● BORN CONNECTED</span>',
  '<span class="os-src-chip born"><span data-mw-tr="dash">● BORN CONNECTED</span></span>', tag="S5-chip-born")
html = rep_re(html, r'(<span class="os-src-chip idle">)(○ NOT CONNECTED)(</span>)',
  r'\1<span data-mw-tr="dash">\2</span>\3', expect=5, tag="S5-chip-idle")
html = rep_re(html, r'(<p class="os-src-note"[^>]*)(>)',
  r'\1 data-mw-tr="dash"\2', expect=18, tag="S5-src-notes")
html = rep_re(html, r'(<p class="os-src-feeds">)([^<]+)(</p>)',
  r'\1<span data-mw-tr="dash">\2</span>\3', expect=19, tag="S5-src-feeds")
html = rep_re(html, r'(<p class="os-src-how"[^>]*)(>)',
  r'\1 data-mw-tr="dash"\2', expect=5, tag="S5-src-how")
html = rep_re(html, r'(<a class="ph-connect os-src-door"[^>]*>)([^<]+)(</a>)',
  r'\1<span data-mw-tr="dash">\2</span>\3', expect=15, tag="S5-src-doors-a")
html = rep(html, '<button class="ph-connect os-src-door" type="button" data-os-go="home">Open this app</button>',
  '<button class="ph-connect os-src-door" type="button" data-os-go="home"><span data-mw-tr="dash">Open this app</span></button>', tag="S5-door-thisapp")
html = rep(html, '<button class="ph-connect os-src-door" type="button" data-os-go="people">See your people</button>',
  '<button class="ph-connect os-src-door" type="button" data-os-go="people"><span data-mw-tr="dash">See your people</span></button>', tag="S5-door-people")
html = rep(html, '<button class="ph-connect os-src-door" type="button" data-dash-how="social">How connecting works</button>',
  '<button class="ph-connect os-src-door" type="button" data-dash-how="social"><span data-mw-tr="dash">How connecting works</span></button>', tag="S5-door-how-social")
html = rep(html, '<button class="ph-connect os-src-door" type="button" data-dash-how="ai">How connecting works</button>',
  '<button class="ph-connect os-src-door" type="button" data-dash-how="ai"><span data-mw-tr="dash">How connecting works</span></button>', tag="S5-door-how-ai")
html = rep(html, '<i>people around you</i>', '<i><span data-mw-tr="dash">people around you</span></i>', tag="S5-people-around")
html = rep(html, '<h3><span class="os-jewel os-jewel-h" style="--jc:#a06bff">🚪</span> The rooms this world opens</h3>',
  '<h3><span class="os-jewel os-jewel-h" style="--jc:#a06bff">🚪</span> <span data-mw-tr="dash">The rooms this world opens</span></h3>', tag="S5-rooms-h3")
html = rep(html, '<p class="os-note">Every room this world is plugged into — listed here, one tap away. Nobody hunts for anything. What you do here appears there; what happens there feeds this world.</p>',
  '<p class="os-note" data-mw-tr="dash">Every room this world is plugged into — listed here, one tap away. Nobody hunts for anything. What you do here appears there; what happens there feeds this world.</p>', tag="S5-rooms-intro")
html = rep(html, '<h3><span class="os-jewel os-jewel-h" style="--jc:#e84fff">✍️</span> Help shape this living app</h3>',
  '<h3><span class="os-jewel os-jewel-h" style="--jc:#e84fff">✍️</span> <span data-mw-tr="dash">Help shape this living app</span></h3>', tag="S5-feedback-h3")
html = rep(html, '<p class="os-note">One line &mdash; it lands in this app&rsquo;s Smart Mail inbox, where the person who runs this app reads it.</p>',
  '<p class="os-note" data-mw-tr="dash">One line &mdash; it lands in this app&rsquo;s Smart Mail inbox, where the person who runs this app reads it.</p>', tag="S5-feedback-note")
html = rep(html, '<input class="os-input" id="os-dash-fb-body" type="text" placeholder="What would make this front better?">',
  '<input class="os-input" id="os-dash-fb-body" type="text" placeholder="What would make this front better?" data-mw-ph="dash">', tag="S5-feedback-ph")

# ---------- JS helpers ----------
def tr(k):
    """mwTr guard for a JS string literal (keys never contain an ASCII quote)."""
    assert "'" not in k and "\\" not in k, f"key not safe for JS single quotes: {k!r}"
    return "(window.mwTr?window.mwTr('" + k + "'):'" + k + "')"
def trd(k):
    """mwTr guard for a double-quoted JS string literal."""
    assert '"' not in k and "\\" not in k, f"key not safe for JS double quotes: {k!r}"
    return '(window.mwTr?window.mwTr("' + k + '"):"' + k + '")'

# ---------- J1: composer JS (Notes view) ----------
# record row header + buttons (render) — the T4 hook re-syncs [data-mn-rec] on switch.
html = rep(html, """'<div class="mn-sec">OR SAY IT, OR SHOW IT — RECORD A NOTE INSTEAD OF TYPING</div>'""",
  "'<div class=\"mn-sec\">'+" + tr("OR SAY IT, OR SHOW IT — RECORD A NOTE INSTEAD OF TYPING") + "+'</div>'", tag="J1-rec-head")
html = rep(html, """data-mn-rec="voice" style="--ac:#a06bff">🎙 Record voice note</button>'""",
  "data-mn-rec=\"voice\" style=\"--ac:#a06bff\">🎙 '+" + tr("Record voice note") + "+'</button>'", tag="J1-rec-voice")
html = rep(html, """data-mn-rec="video" style="--ac:#3fb8ff">🎥 Record video note</button>'""",
  "data-mn-rec=\"video\" style=\"--ac:#3fb8ff\">🎥 '+" + tr("Record video note") + "+'</button>'", tag="J1-rec-video")
html = rep(html, """r.btn.textContent = r.kind === 'video' ? '🎥 Record video note' : '🎙 Record voice note';""",
  "r.btn.textContent = r.kind === 'video' ? '🎥 '+" + tr("Record video note") + " : '🎙 '+" + tr("Record voice note") + ";", tag="J1-rec-reset")
html = rep(html, """say(kind === 'video' ? 'Recording — your camera preview is below. Tap the button again to stop.' : 'Recording — speak now. Tap the button again to stop.');""",
  "say(kind === 'video' ? " + tr("Recording — your camera preview is below. Tap the button again to stop.") + " : " + tr("Recording — speak now. Tap the button again to stop.") + ");", tag="J1-rec-say")
html = rep(html, """btn.textContent = '⏹ ' + fmtDur(s) + ' — tap to stop';""",
  "btn.textContent = '⏹ ' + fmtDur(s) + " + tr(" — tap to stop") + ";", tag="J1-rec-timer")
html = rep(html, """say((kind === 'video' ? 'Camera/microphone' : 'Microphone') + ' permission was denied — the recording did not start. Allow it in your browser, then tap record again.');""",
  "say((kind === 'video' ? " + tr("Camera/microphone") + " : " + tr("Microphone") + ") + " + tr(" permission was denied — the recording did not start. Allow it in your browser, then tap record again.") + ");", tag="J1-rec-denied")
# player aria-labels (T4 hook re-syncs [data-mn-play]/[data-mn-vplay] on switch).
html = rep(html, """aria-label="Play the video note">▶</button></div>';""",
  "aria-label=\"'+" + tr("Play the video note") + "+'\">▶</button></div>';", tag="J1-play-video")
html = rep(html, """aria-label="Play the voice note">▶</button>'""",
  "aria-label=\"'+" + tr("Play the voice note") + "+'\">▶</button>'", tag="J1-play-voice")
# nnRenderFilter 'All' chip: visible text translates, the filter value stays 'All'.
html = rep(html, """return '<button class="os-like' + (nnFilter === c ? ' on' : '') + '" type="button" data-nn-filter="' + esc(c) + '" style="--ac:' + NN_WALK[ix % NN_WALK.length] + ';margin:0 6px 6px 0;">' + esc(c) + '</button>';""",
  """return '<button class="os-like' + (nnFilter === c ? ' on' : '') + '" type="button" data-nn-filter="' + esc(c) + '" style="--ac:' + NN_WALK[ix % NN_WALK.length] + ';margin:0 6px 6px 0;">' + esc(c==='All'?""" + tr("All") + """:c) + '</button>';""", tag="J1-filter-all")
# nnRenderList empties + filed line + buttons (T4 hook re-syncs the buttons on switch).
html = rep(html, """'Nothing under this category yet.'""", tr("Nothing under this category yet."), tag="J1-empty-cat")
html = rep(html, """'Nothing here yet — write the first note above. It is kept in your Naya Notes, on every surface that reads them.'""", tr("Nothing here yet — write the first note above. It is kept in your Naya Notes, on every surface that reads them."), tag="J1-empty-none")
html = rep(html, """'<div class="naya-note-time">Filed to: ' + esc(lk.b_label || 'a person') + '</div>'""",
  "'<div class=\"naya-note-time\">'+" + tr("Filed to: ") + "+esc(lk.b_label || " + tr("a person") + ")+'</div>'", expect=2, tag="J1-filed-to")
html = rep(html, """>Unfile</button>""", ">'+" + tr("Unfile") + "+'</button>", expect=2, tag="J1-unfile-btn")
html = rep(html, """data-nn-copy="' + esc(n.id) + '" style="--ac:#2fe89e">Copy</button>'""",
  "data-nn-copy=\"' + esc(n.id) + '\" style=\"--ac:#2fe89e\">'+" + tr("Copy") + "+'</button>'", tag="J1-nn-copy")
html = rep(html, """data-nn-move="' + esc(n.id) + '" style="--ac:#ffbf3d">Move</button>'""",
  "data-nn-move=\"' + esc(n.id) + '\" style=\"--ac:#ffbf3d\">'+" + tr("Move") + "+'</button>'", tag="J1-nn-move")
html = rep(html, """data-nn-list="' + esc(n.id) + '" style="--ac:#2fe89e">List</button>'""",
  "data-nn-list=\"' + esc(n.id) + '\" style=\"--ac:#2fe89e\">'+" + tr("List") + "+'</button>'", tag="J1-nn-list")
# save/status strings (nn + mn share the unfile pair — expect=2 where shared).
html = rep(html, """st.textContent = 'Write the note first — even one line is enough.';""",
  "st.textContent = " + tr("Write the note first — even one line is enough.") + ";", tag="J1-st-write")
html = rep(html, """st.textContent = 'Saving…';""", "st.textContent = " + tr("Saving…") + ";", tag="J1-st-saving")
html = rep(html, """st.textContent = 'Couldn’t save just now — the save service did not answer. Your words are still here; nothing was lost.';""",
  "st.textContent = " + tr("Couldn’t save just now — the save service did not answer. Your words are still here; nothing was lost.") + ";", expect=2, tag="J1-st-couldnt")
html = rep(html, """st.textContent = 'Saved — it is in your Naya Notes.';""",
  "st.textContent = " + tr("Saved — it is in your Naya Notes.") + ";", tag="J1-st-saved")
html = rep(html, """stEl.textContent = 'Copied — the note exactly as stored.';""",
  "stEl.textContent = " + tr("Copied — the note exactly as stored.") + ";", tag="J1-st-copied")
html = rep(html, """'Connection unavailable — the unfile did not happen.'""",
  tr("Connection unavailable — the unfile did not happen."), expect=2, tag="J1-st-unfile-conn")
html = rep(html, """'Unfile failed: '""", tr("Unfile failed: "), expect=2, tag="J1-st-unfile-fail")
html = rep(html, """host.innerHTML = '<p class="os-note">Connection unavailable — your Naya Notes could not be read.</p>';""",
  "host.innerHTML = '<p class=\"os-note\">'+" + tr("Connection unavailable — your Naya Notes could not be read.") + "+'</p>';", tag="J1-load-conn")
html = rep(html, """cardStatus(id, 'That recording is no longer there — it may have been removed.');""",
  "cardStatus(id, " + tr("That recording is no longer there — it may have been removed.") + ");", expect=4, tag="J1-card-gone")
html = rep(html, """cardStatus(id, 'Copied — the playable link, exactly as stored.');""",
  "cardStatus(id, " + tr("Copied — the playable link, exactly as stored.") + ");", tag="J1-card-copied")
html = rep(html, """st.textContent='Write the thought first — then Note it.';""",
  "st.textContent=" + tr("Write the thought first — then Note it.") + ";", tag="J1-cap-write")
html = rep(html, """st.textContent='The note could not be saved — try once more.';""",
  "st.textContent=" + tr("The note could not be saved — try once more.") + ";", expect=2, tag="J1-cap-fail")
html = rep(html, """st.textContent='Captured — it is a card below, in this app, with the time it landed.';""",
  "st.textContent=" + tr("Captured — it is a card below, in this app, with the time it landed.") + ";", tag="J1-cap-done")
# media-card transcript/summary + fallback titles + Copy link (T4 re-syncs [data-mn-copylink]).
html = rep(html, """<div class="mn-sec">TRANSCRIPT</div>""", "<div class=\"mn-sec\">'+" + tr("TRANSCRIPT") + "+'</div>", tag="J1-transcript-h")
html = rep(html, """<div class="mn-sec">SUMMARY</div>""", "<div class=\"mn-sec\">'+" + tr("SUMMARY") + "+'</div>", tag="J1-summary-h")
html = rep(html, """>The transcript did not go through — the recording itself is safe and playable above.</p>""", ">' + " + tr("The transcript did not go through — the recording itself is safe and playable above.") + " + '</p>", tag="J1-transcript-fail")
html = rep(html, """>Transcript on its way — Naya is writing down what was said.</p>""", ">' + " + tr("Transcript on its way — Naya is writing down what was said.") + " + '</p>", tag="J1-transcript-way")
html = rep(html, """esc(m.title || (m.kind === 'video' ? 'Video note' : 'Voice note'))""",
  "esc(m.title || (m.kind === 'video' ? " + tr("Video note") + " : " + tr("Voice note") + "))", tag="J1-media-title")
html = rep(html, """data-mn-copylink="' + esc(m.id) + '" style="--ac:#2fe89e">Copy link</button>'""",
  "data-mn-copylink=\"' + esc(m.id) + '\" style=\"--ac:#2fe89e\">'+" + tr("Copy link") + "+'</button>'", tag="J1-copylink")
# wall empty state (Notes view, line 10844).
html = rep(html, """✦</span> No notes yet</h3>""", "✦</span> '+" + tr("No notes yet") + "+'</h3>", tag="J1-wall-empty-h")
html = rep(html, """>Nothing captured in this app yet. The first note you capture above becomes the first real card here.</p>""", ">' + " + tr("Nothing captured in this app yet. The first note you capture above becomes the first real card here.") + " + '</p>", tag="J1-wall-empty-p")
# slInLine 'In: ' prefix (T4 hook rebuilds [data-nn-in] on switch; this covers first paint).
html = rep(html, """return names.length ? ('In: ' + names.join(', ')) : '';""",
  "return names.length ? (" + tr("In: ") + " + names.join(', ')) : '';", tag="J1-slinline")
# Smart Lists kind labels (the List picker opened from a Notes card).
html = rep(html, """var SL_KIND_LABEL = { smart_note: 'Smart Note', naya_note: 'Naya Note', person: 'Person', mail_thread: 'Mail', smart_link: 'Smart Link', text: 'Note to self' };""",
  "var SL_KIND_LABEL = { smart_note: " + tr("Smart Note") + ", naya_note: " + tr("Naya Note") + ", person: " + tr("Person") + ", mail_thread: " + tr("Mail") + ", smart_link: " + tr("Smart Link") + ", text: " + tr("Note to self") + " };", tag="J1-sl-kinds")

# ---------- J2: feed meta line (mwPaintWallPosts) ----------
# A shared composer + stored state: mwApplyLang re-syncs only the meta line
# (never the wall cards — repainting them would reset Translate-tap state).
html = rep(html, """  function mwPaintWallPosts(posts){""",
  """  function mwWallMetaText(shown, pill, kw){
    if(!shown.length) return '';
    var t;
    if(pill && pill!=='all'){
      var disp='Guest'; for(var i=0;i<MW_WALL_POSTS.length;i++){ if((MW_WALL_POSTS[i].j.a||'Guest').toLowerCase()===pill){ disp=MW_WALL_POSTS[i].j.a||'Guest'; break; } }
      t=shown.length+(shown.length===1?""" + tr(" post") + """:""" + tr(" posts") + """)+(window.mwTr?window.mwTr(' by '):' by ')+disp+(window.mwTr?window.mwTr(' on this feed.'):' on this feed.');
    } else {
      var voices={}; shown.forEach(function(p){ voices[(p.j.a||'Guest').toLowerCase()]=1; });
      var n=Object.keys(voices).length;
      t=shown.length+(shown.length===1?""" + tr(" post") + """:""" + tr(" posts") + """)+(window.mwTr?window.mwTr(' on this feed — the newest landed '):' on this feed — the newest landed ')+relLabel(shown[0].at)+(window.mwTr?window.mwTr(', across '):', across ')+n+(n===1?""" + tr(" voice") + """:""" + tr(" voices") + """)+ '.';
    }
    if(kw){ t=shown.length? (t+(window.mwTr?window.mwTr(' Matching \\u201c'):' Matching \\u201c')+window.MW_PUBLIC_KEYWORD+(window.mwTr?window.mwTr('\\u201d.'):'\\u201d.')) : ((window.mwTr?window.mwTr('No notes match \\u201c'):'No notes match \\u201c')+window.MW_PUBLIC_KEYWORD+(window.mwTr?window.mwTr('\\u201d — try another word.'):'\\u201d — try another word.')); }
    return t;
  }
  window.mwSyncWallMeta=function(){
    if(!window._mwWallMetaState) return;
    var s=window._mwWallMetaState, meta=$('os-wall-meta');
    if(meta) meta.textContent=mwWallMetaText(s.shown, s.pill, s.kw);
  };
  function mwPaintWallPosts(posts){""", tag="J2-meta-helper")
html = rep(html, """    var meta=$('os-wall-meta');
    if(meta){
      if(!shown.length){ meta.textContent=''; }
      else if(pill && pill!=='all'){
        var disp='Guest'; for(var i=0;i<MW_WALL_POSTS.length;i++){ if((MW_WALL_POSTS[i].j.a||'Guest').toLowerCase()===pill){ disp=MW_WALL_POSTS[i].j.a||'Guest'; break; } }
        meta.textContent=shown.length+(shown.length===1?' post':' posts')+' by '+disp+' on this feed.';
      }
      else{
        var voices={}; shown.forEach(function(p){ voices[(p.j.a||'Guest').toLowerCase()]=1; });
        var n=Object.keys(voices).length;
        meta.textContent=shown.length+(shown.length===1?' post':' posts')+' on this feed — the newest landed '+relLabel(shown[0].at)+', across '+n+(n===1?' voice':' voices')+'.';
      }
    }
    /* FOLLOW-UP: the meta line says what the feed is showing — including the keyword, when one is pulling it. textContent, never HTML, so a typed keyword can never inject markup. */
    if(meta && kw){ meta.textContent=shown.length? (meta.textContent+' Matching \\u201c'+window.MW_PUBLIC_KEYWORD+'\\u201d.') : ('No notes match \\u201c'+window.MW_PUBLIC_KEYWORD+'\\u201d — try another word.'); }""",
  """    var meta=$('os-wall-meta');
    if(meta){ meta.textContent=mwWallMetaText(shown, pill, kw); }
    window._mwWallMetaState={shown:shown, pill:pill, kw:kw};""", tag="J2-meta-call")

# ---------- J3: relative-time functions + date locales ----------
# relLabel x2 (identical one-liners, lines 8153 + 11748).
html = rep(html, """function relLabel(iso){ var ms=Date.now()-new Date(iso).getTime(); if(ms<60000) return 'just now'; var m=Math.floor(ms/60000); if(m<60) return m+'m ago'; var h=Math.floor(m/60); if(h<24) return h+'h ago'; var d=Math.floor(h/24); return d+'d ago'; }""",
  "function relLabel(iso){ var ms=Date.now()-new Date(iso).getTime(); if(ms<60000) return " + tr("just now") + "; var m=Math.floor(ms/60000); if(m<60) return " + tr("{n}m ago") + ".replace('{n}', m); var h=Math.floor(m/60); if(h<24) return " + tr("{n}h ago") + ".replace('{n}', h); var d=Math.floor(h/24); return " + tr("{n}d ago") + ".replace('{n}', d); }", expect=2, tag="J3-relLabel")
# stamp() date/time locale (wall-card dates).
html = rep(html, """var date=d.toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'}); var time=d.toLocaleTimeString('en-US',{hour:'numeric',minute:'2-digit'});""",
  "var date=d.toLocaleDateString((window.mwLocale?window.mwLocale():'en-US'),{month:'short',day:'numeric',year:'numeric'}); var time=d.toLocaleTimeString((window.mwLocale?window.mwLocale():'en-US'),{hour:'numeric',minute:'2-digit'});", tag="J3-stamp-locale")
# bucketize labels + locales.
html = rep(html, """b.label=last?'Today':(period===7?b.d.toLocaleDateString('en-US',{weekday:'short'}):(ix%5===0?String(b.d.getDate()):''));""",
  "b.label=last?" + tr("Today") + ":(period===7?b.d.toLocaleDateString((window.mwLocale?window.mwLocale():'en-US'),{weekday:'short'}):(ix%5===0?String(b.d.getDate()):''));", expect=2, tag="J3-bucket-today")
html = rep(html, """b.note=b.d.toLocaleDateString('en-US',{weekday:'long'})+': '+b.n+(b.n===1?' event':' events')+'.';""",
  "b.note=b.d.toLocaleDateString((window.mwLocale?window.mwLocale():'en-US'),{weekday:'long'})+': '+b.n+(b.n===1?" + tr(" event") + ":" + tr(" events") + ")+'.';", expect=2, tag="J3-bucket-note7")
html = rep(html, """b.label=last?'This week':b.d.toLocaleDateString('en-US',{month:'short', day:'numeric'});""",
  "b.label=last?" + tr("This week") + ":b.d.toLocaleDateString((window.mwLocale?window.mwLocale():'en-US'),{month:'short', day:'numeric'});", expect=2, tag="J3-bucket-week")
html = rep(html, """b.note='Week of '+b.d.toLocaleDateString('en-US',{month:'long', day:'numeric'})+': '+b.n+(b.n===1?' event':' events')+'.';""",
  "b.note=" + tr("Week of ") + "+b.d.toLocaleDateString((window.mwLocale?window.mwLocale():'en-US'),{month:'long', day:'numeric'})+': '+b.n+(b.n===1?" + tr(" event") + ":" + tr(" events") + ")+'.';", expect=2, tag="J3-bucket-noteW")
# ldRel (dash IIFE, 17839): 'just now' + m/h/d/mo templates.
html = rep(html, """  if (s < 60) return 'just now';
  var m = Math.floor(s/60); if (m < 60) return m+'m ago';
  var h = Math.floor(m/60); if (h < 24) return h+'h ago';
  var d = Math.floor(h/24); if (d < 30) return d+'d ago';
  return Math.floor(d/30)+'mo ago';""",
  "  if (s < 60) return " + tr("just now") + ";\n  var m = Math.floor(s/60); if (m < 60) return " + tr("{n}m ago") + ".replace('{n}', m);\n  var h = Math.floor(m/60); if (h < 24) return " + tr("{n}h ago") + ".replace('{n}', h);\n  var d = Math.floor(h/24); if (d < 30) return " + tr("{n}d ago") + ".replace('{n}', d);\n  return " + tr("{n}mo ago") + ".replace('{n}', Math.floor(d/30));", tag="J3-ldRel")
# ibRel (14537, dead path — routed per the card-labels precedent).
html = rep(html, """    if (s < 60) return 'just now';
    var m = Math.floor(s/60); if (m < 60) return m + 'm ago';
    var h = Math.floor(m/60); if (h < 24) return h + 'h ago';
    var dd = Math.floor(h/24); if (dd < 30) return dd + 'd ago';
    return new Date(iso).toLocaleDateString();""",
  "    if (s < 60) return " + tr("just now") + ";\n    var m = Math.floor(s/60); if (m < 60) return " + tr("{n}m ago") + ".replace('{n}', m);\n    var h = Math.floor(m/60); if (h < 24) return " + tr("{n}h ago") + ".replace('{n}', h);\n    var dd = Math.floor(h/24); if (dd < 30) return " + tr("{n}d ago") + ".replace('{n}', dd);\n    return new Date(iso).toLocaleDateString((window.mwLocale?window.mwLocale():'en-US'));", tag="J3-ibRel")
# relTime, live wall path (15733).
html = rep(html, """      if (m < 1) return 'just now';
      if (m < 60) return m + 'm ago';
      const h = Math.floor(m / 60);
      if (h < 24) return h + 'h ago';
      const d = Math.floor(h / 24);
      if (d < 7) return d + 'd ago';
      return new Date(iso).toLocaleDateString();""",
  "      if (m < 1) return " + tr("just now") + ";\n      if (m < 60) return " + tr("{n}m ago") + ".replace('{n}', m);\n      const h = Math.floor(m / 60);\n      if (h < 24) return " + tr("{n}h ago") + ".replace('{n}', h);\n      const d = Math.floor(h / 24);\n      if (d < 7) return " + tr("{n}d ago") + ".replace('{n}', d);\n      return new Date(iso).toLocaleDateString((window.mwLocale?window.mwLocale():'en-US'));", tag="J3-relTime15733")
# rel (16637, truth module, double-quoted) + relTime (17070).
html = rep(html, """function rel(ts){
  if(!ts) return "never";""",
  "function rel(ts){\n  if(!ts) return " + trd("never") + ";", tag="J3-rel-never")
html = rep(html, """  if(d < 45e3) return "just now";
  if(d < 3600e3){ var m=Math.floor(d/60e3); return m+(m===1?"m ago":"m ago"); }
  if(d < 86400e3){ var h=Math.floor(d/3600e3); return h+(h===1?" hr ago":" hrs ago"); }
  var dd=Math.floor(d/86400e3); return dd+(dd===1?" day ago":" days ago");""",
  "  if(d < 45e3) return " + trd("just now") + ";\n  if(d < 3600e3){ var m=Math.floor(d/60e3); return " + trd("{n}m ago") + ".replace('{n}', m); }\n  if(d < 86400e3){ var h=Math.floor(d/3600e3); return (h===1?" + trd("{n} hr ago") + ".replace('{n}', h):" + trd("{n} hrs ago") + ".replace('{n}', h)); }\n  var dd=Math.floor(d/86400e3); return (dd===1?" + trd("{n} day ago") + ".replace('{n}', dd):" + trd("{n} days ago") + ".replace('{n}', dd));", tag="J3-rel-body")
html = rep(html, """    if (!(d >= 0)) return 'just now';
    if (d < 60e3) return 'just now';
    if (d < 3600e3){ var m = Math.floor(d/60e3); return m + 'm ago'; }
    if (d < 86400e3){ var h = Math.floor(d/3600e3); return h + 'h ago'; }
    return Math.floor(d/86400e3) + 'd ago';""",
  "    if (!(d >= 0)) return " + tr("just now") + ";\n    if (d < 60e3) return " + tr("just now") + ";\n    if (d < 3600e3){ var m = Math.floor(d/60e3); return " + tr("{n}m ago") + ".replace('{n}', m); }\n    if (d < 86400e3){ var h = Math.floor(d/3600e3); return " + tr("{n}h ago") + ".replace('{n}', h); }\n    return " + tr("{n}d ago") + ".replace('{n}', Math.floor(d/86400e3));", tag="J3-relTime17070")

# ---------- J4: presence + face tiles ----------
html = rep(html, """    if (!iso) return {on:false, txt:'Around this app'};
    var mins=(Date.now()-new Date(iso).getTime())/60000;
    if (mins<60) return {on:true, txt:'Around now'};
    if (mins<1440) return {on:true, txt:'Active '+relLabel(iso)};
    return {on:false, txt:'Last active '+relLabel(iso)};""",
  "    if (!iso) return {on:false, txt:" + tr("Around this app") + "};\n    var mins=(Date.now()-new Date(iso).getTime())/60000;\n    if (mins<60) return {on:true, txt:" + tr("Around now") + "};\n    if (mins<1440) return {on:true, txt:" + tr("Active ") + "+relLabel(iso)};\n    return {on:false, txt:" + tr("Last active ") + "+relLabel(iso)};", expect=2, tag="J4-presence")

# ---------- J5: notifications + Smart Notes + Joined (My World) ----------
html = rep(html, """(d.posts||[]).forEach(function(p){ act.push({ic:'✦', ti:(p.j.b||'Feed post'), su:((p.j.a||'Guest')+' posted'), at:p.at, go:'home'}); });""",
  "(d.posts||[]).forEach(function(p){ act.push({ic:'✦', ti:(p.j.b||" + tr("Feed post") + "), su:((p.j.a||" + tr("Guest") + ")+" + tr(" posted") + "), at:p.at, go:'home'}); });", tag="J5-notif-post")
html = rep(html, """(d.noteRows||[]).forEach(function(r){ act.push({ic:'✦', ti:(r.j.t||'Untitled note'), su:'Smart Note', at:r.at, go:'notes'}); });""",
  "(d.noteRows||[]).forEach(function(r){ act.push({ic:'✦', ti:(r.j.t||" + tr("Untitled note") + "), su:" + tr("Smart Note") + ", at:r.at, go:'notes'}); });", tag="J5-notif-note")
html = rep(html, """(d.connectRows||[]).forEach(function(r){ act.push({ic:'🤝', ti:'Someone connected', su:((r.j.a||'A visitor')+' connected'), at:r.at, go:'people'}); });""",
  "(d.connectRows||[]).forEach(function(r){ act.push({ic:'🤝', ti:" + tr("Someone connected") + ", su:((r.j.a||" + tr("A visitor") + ")+" + tr(" connected") + "), at:r.at, go:'people'}); });", tag="J5-notif-connect")
html = rep(html, """(d.invRows||[]).forEach(function(v){ if (upIsProofName(v.invitee_name)) return; act.push({ic:'💌', ti:(v.invitee_name||'Someone'), su:'Invited'+(v.status?(' · '+v.status):''), at:v.created_at, go:'growth'}); });""",
  "(d.invRows||[]).forEach(function(v){ if (upIsProofName(v.invitee_name)) return; act.push({ic:'💌', ti:(v.invitee_name||" + tr("Someone") + "), su:" + tr("Invited") + "+(v.status?(' · '+v.status):''), at:v.created_at, go:'growth'}); });", tag="J5-notif-inv")
html = rep(html, """(d.threads||[]).forEach(function(t){ mail.push({ic:'✉️', ti:(t.subject||'(no subject)'), su:humanize(t.from_alias)+(t.preview?(' — '+t.preview):''), at:t.created_at, go:'inbox'}); });""",
  "(d.threads||[]).forEach(function(t){ mail.push({ic:'✉️', ti:(t.subject||" + tr("(no subject)") + "), su:humanize(t.from_alias)+(t.preview?(' — '+t.preview):''), at:t.created_at, go:'inbox'}); });", tag="J5-notif-mail")
html = rep(html, """(d.joinedRows||[]).forEach(function(v){ if (upIsProofName(v.invitee_name)) return; stats.push({ic:'✅', ti:(v.invitee_name||'Someone'), su:'Joined', at:v.created_at, go:'growth'}); });""",
  "(d.joinedRows||[]).forEach(function(v){ if (upIsProofName(v.invitee_name)) return; stats.push({ic:'✅', ti:(v.invitee_name||" + tr("Someone") + "), su:" + tr("Joined") + ", at:v.created_at, go:'growth'}); });", tag="J5-notif-joined")
html = rep(html, """      var empty = _mwNotifKind==='mail' ? 'No messages yet — the inbox is listening.'
        : _mwNotifKind==='stats' ? 'No joins yet — the first join starts the growth story.'
        : 'No activity yet — the first post starts the story.';""",
  "      var empty = _mwNotifKind==='mail' ? " + tr("No messages yet — the inbox is listening.") + "\n        : _mwNotifKind==='stats' ? " + tr("No joins yet — the first join starts the growth story.") + "\n        : " + tr("No activity yet — the first post starts the story.") + ";", tag="J5-notif-empty")
html = rep(html, """      html+='<p class="os-note">Totals — '+dd.postTimes.length+' posts · '+dd.msgTimes.length+' messages · '+dd.invTimes.length+' invites · '+dd.joined+' joins.</p>';""",
  "      html+='<p class=\"os-note\">'+" + tr("Totals — ") + "+dd.postTimes.length+" + tr(" posts · ") + "+dd.msgTimes.length+" + tr(" messages · ") + "+dd.invTimes.length+" + tr(" invites · ") + "+dd.joined+" + tr(" joins.") + "+'</p>';", tag="J5-notif-totals")
html = rep(html, """showAllBtn.textContent='Show all '+rows.length;""",
  "showAllBtn.textContent=" + tr("Show all ") + "+rows.length;", tag="J5-notif-showall")
html = rep(html, """    if(!rows.length){ list.innerHTML='<p class="os-note">No Smart Notes yet — the first one starts the intelligence.</p>'; return; }""",
  "    if(!rows.length){ list.innerHTML='<p class=\"os-note\">'+" + tr("No Smart Notes yet — the first one starts the intelligence.") + "+'</p>'; return; }", tag="J5-mwnotes-empty")
html = rep(html, """      return _mwRowHTML('✦', (r.j.t||'Untitled note'), 'Smart Note', relLabel(r.at), {go:'notes'}, null, 'Open in Notes');""",
  "      return _mwRowHTML('✦', (r.j.t||" + tr("Untitled note") + "), " + tr("Smart Note") + ", relLabel(r.at), {go:'notes'}, null, " + tr("Open in Notes") + ");", tag="J5-mwnotes-row")
# renderJoined: fallback rooms + world pages route through mwTr at render; the
# gateway live path reads translated button text, and mwTr passes it through.
html = rep(html, """      rooms=[{label:'Home',go:'home'},{label:'Dashboard',go:'dashboard'},{label:'About',go:'about'},{label:'Today',go:'today'},{label:'Notes',go:'notes'},{label:'Connections',go:'people'},{label:'Message',go:'message'},{label:'Inbox',go:'inbox'},{label:'Invite',go:'growth'},{label:'Lists',go:'lists'},{label:'Scheduler',go:'scheduler'},{label:'Reports',go:'reports'}];""",
  "      rooms=[{label:" + tr("Home") + ",go:'home'},{label:" + tr("Dashboard") + ",go:'dashboard'},{label:" + tr("About") + ",go:'about'},{label:" + tr("Today") + ",go:'today'},{label:" + tr("Notes") + ",go:'notes'},{label:" + tr("Connections") + ",go:'people'},{label:" + tr("Message") + ",go:'message'},{label:" + tr("Inbox") + ",go:'inbox'},{label:" + tr("Invite") + ",go:'growth'},{label:" + tr("Lists") + ",go:'lists'},{label:" + tr("Scheduler") + ",go:'scheduler'},{label:" + tr("Reports") + ",go:'reports'}];", tag="J5-joined-rooms")
html = rep(html, """      {label:'Dashboard', ic:'📊', dest:{go:'dashboard'}},
      {label:'Personal', ic:'🌍', dest:{href:'https://nayanet.app/personal'}},
      {label:'Business', ic:'💼', dest:worldByLabel('Business', {href:'https://nayanet.app/business'})},
      {label:'Space', ic:'🚀', dest:worldByLabel('Space', {href:'https://nayanet.app/space'})},
      {label:'Membership', ic:'🎫', dest:worldByLabel('Memberships', {go:'memberships'})}""",
  "      {label:" + tr("Dashboard") + ", ic:'📊', dest:{go:'dashboard'}},\n      {label:" + tr("Personal") + ", ic:'🌍', dest:{href:'https://nayanet.app/personal'}},\n      {label:" + tr("Business") + ", ic:'💼', dest:worldByLabel('Business', {href:'https://nayanet.app/business'})},\n      {label:" + tr("Space") + ", ic:'🚀', dest:worldByLabel('Space', {href:'https://nayanet.app/space'})},\n      {label:" + tr("Membership") + ", ic:'🎫', dest:worldByLabel('Memberships', {go:'memberships'})}", tag="J5-joined-pages")
html = rep(html, """      html+=_mwRowHTML(p.ic, p.label, 'Your world', '', p.dest, 'JOINED');""",
  "      html+=_mwRowHTML(p.ic, (window.mwTr?window.mwTr(p.label):p.label), " + tr("Your world") + ", '', p.dest, " + tr("JOINED") + ");", tag="J5-joined-worldrow")
html = rep(html, """      html+=_mwRowHTML('🚪', r.label, 'Room on this page', '', {go:r.go}, 'JOINED');""",
  "      html+=_mwRowHTML('🚪', (window.mwTr?window.mwTr(r.label):r.label), " + tr("Room on this page") + ", '', {go:r.go}, " + tr("JOINED") + ");", tag="J5-joined-roomrow")
html = rep(html, """    list.innerHTML=html||'<p class="os-note">No pages joined yet.</p>';""",
  "    list.innerHTML=html||'<p class=\"os-note\">'+" + tr("No pages joined yet.") + "+'</p>';", tag="J5-joined-empty")

# ---------- J6: trend kinds, funnel, faces, insights, convos, shortStat ----------
html = rep(html, """  var KIND_META={
    all:{subject:'Posts, notes, messages and invites together.', color:null, quiet:'The next post, note, message or invite lights the first bar.'},
    posts:{subject:'Feed posts only.', color:'#a06bff', quiet:'The next feed post lights the first bar.'},
    notes:{subject:'Smart Notes only.', color:'#ff9a5a', quiet:'The first Smart Note lights the first bar.'},
    messages:{subject:'Messages received only.', color:'#3fb8ff', quiet:'The next message lights the first bar.'},
    invites:{subject:'Invites recorded only.', color:'#2fe89e', quiet:'The next invite lights the first bar.'}
  };""",
  "  var KIND_META={\n    all:{subject:" + tr("Posts, notes, messages and invites together.") + ", color:null, quiet:" + tr("The next post, note, message or invite lights the first bar.") + "},\n    posts:{subject:" + tr("Feed posts only.") + ", color:'#a06bff', quiet:" + tr("The next feed post lights the first bar.") + "},\n    notes:{subject:" + tr("Smart Notes only.") + ", color:'#ff9a5a', quiet:" + tr("The first Smart Note lights the first bar.") + "},\n    messages:{subject:" + tr("Messages received only.") + ", color:'#3fb8ff', quiet:" + tr("The next message lights the first bar.") + "},\n    invites:{subject:" + tr("Invites recorded only.") + ", color:'#2fe89e', quiet:" + tr("The next invite lights the first bar.") + "}\n  };", tag="J6-kind-meta")
# shortStat: the noun/plural arrive in English from the callers — translate the word.
html = rep(html, """    var sp=weekSplit(times), word=total===1?noun:plural;
    var t=total+' '+word+' — '+sp.wk+' this week';""",
  "    var sp=weekSplit(times), word=(window.mwTr?window.mwTr(total===1?noun:plural):(total===1?noun:plural));\n    var t=total+' '+word+' — '+sp.wk+" + tr(" this week") + ";", tag="J6-shortstat-word")
html = rep(html, """    if (sp.pv>0) t+= sp.wk>sp.pv ? ', up from '+sp.pv+'.' : (sp.wk<sp.pv ? ', down from '+sp.pv+'.' : ', same pace as last.');""",
  "    if (sp.pv>0) t+= sp.wk>sp.pv ? " + tr(", up from ") + "+sp.pv+'.' : (sp.wk<sp.pv ? " + tr(", down from ") + "+sp.pv+'.' : " + tr(", same pace as last.") + ");", tag="J6-shortstat-trend")
html = rep(html, """    if (np) np.textContent=shortStat('post','posts',d.postTimes,'No posts yet — the feed speaks first.');""",
  "    if (np) np.textContent=shortStat('post','posts',d.postTimes," + tr("No posts yet — the feed speaks first.") + ");", tag="J6-pulse-posts")
html = rep(html, """    if (nm){ nm.textContent=shortStat('message','messages',d.msgTimes,'No messages yet — the inbox is listening.'); if (d.waitingCount) nm.textContent+=' '+d.waitingCount+(d.waitingCount===1?' conversation is':' conversations are')+' waiting for your reply.'""",
  "    if (nm){ nm.textContent=shortStat('message','messages',d.msgTimes," + tr("No messages yet — the inbox is listening.") + "); if (d.waitingCount) nm.textContent+=' '+d.waitingCount+(d.waitingCount===1?" + tr(" conversation is") + ":" + tr(" conversations are") + ")+" + tr(" waiting for your reply.") + "", tag="J6-pulse-msgs")
html = rep(html, """    if (ni) ni.textContent=shortStat('invite','invites',d.invTimes,'No invites yet — the first starts the growth story.');""",
  "    if (ni) ni.textContent=shortStat('invite','invites',d.invTimes," + tr("No invites yet — the first starts the growth story.") + ");", tag="J6-pulse-inv")
html = rep(html, """      if (!d.peopleList.length) nf.textContent='No faces yet — the first post, message or invite brings the first face.';""",
  "      if (!d.peopleList.length) nf.textContent=" + tr("No faces yet — the first post, message or invite brings the first face.") + ";", tag="J6-pulse-nofaces")
html = rep(html, """        nf.textContent=d.peopleAround.length+(d.peopleAround.length===1?' person has':' people have')+' posted, messaged or been invited here'+(hot?(' — '+hot+' in the last day.'):'');""",
  "        nf.textContent=d.peopleAround.length+(d.peopleAround.length===1?" + tr(" person has") + ":" + tr(" people have") + ")+" + tr(" posted, messaged or been invited here") + "+(hot?(' — '+hot+" + tr(" in the last day.") + "):'');", tag="J6-pulse-people")
# funnel truths + stages + conversions.
html = rep(html, """    if (!total && !clicks) truth='No invites yet — record the first one in Growth.';""",
  "    if (!total && !clicks) truth=" + tr("No invites yet — record the first one in Growth.") + ";", tag="J6-fun-truth0")
html = rep(html, """    else if (allDry && !joinedAll) truth='Record-only mode: saved, never sent — Joined honestly reads 0 until a friend connects.';""",
  "    else if (allDry && !joinedAll) truth=" + tr("Record-only mode: saved, never sent — Joined honestly reads 0 until a friend connects.") + ";", tag="J6-fun-truthdry")
html = rep(html, """    else if (!joinedAll) truth='Invites are recorded'+(clicks?' and your links are being clicked':'')+' — the first join is the milestone ahead.';""",
  "    else if (!joinedAll) truth=" + tr("Invites are recorded") + "+(clicks?" + tr(" and your links are being clicked") + ":'')+" + tr(" — the first join is the milestone ahead.") + ";", tag="J6-fun-truth1")
html = rep(html, """    else truth=joinedAll+(joinedAll===1?' person has':' people have')+' walked the whole journey.';""",
  "    else truth=joinedAll+(joinedAll===1?" + tr(" person has") + ":" + tr(" people have") + ")+" + tr(" walked the whole journey.") + ";", tag="J6-fun-truth2")
html = rep(html, """      mid='<div class="os-fconv"><span class="os-farrow" style="--fc:#2fe89e"></span><b>'+clicks+'</b> '+(clicks===1?'click':'clicks')+' counted on your Smart Links</div>'
        +stage('Clicked', clicks, '#2fe89e', 1)
        +conv(joinedAll, clicks, 'of clicks joined', '#3fb8ff')
        +stage('Joined', joinedAll, '#3fb8ff', 2);""",
  "      mid='<div class=\"os-fconv\"><span class=\"os-farrow\" style=\"--fc:#2fe89e\"></span><b>'+clicks+'</b> '+(clicks===1?" + tr("click") + ":" + tr("clicks") + ")+" + tr(" counted on your Smart Links") + "+'</div>'\n        +stage(" + tr("Clicked") + ", clicks, '#2fe89e', 1)\n        +conv(joinedAll, clicks, " + tr("of clicks joined") + ", '#3fb8ff')\n        +stage(" + tr("Joined") + ", joinedAll, '#3fb8ff', 2);", tag="J6-fun-mid")
html = rep(html, """      mid=conv(joined, total, 'of recorded invites joined', '#3fb8ff')
        +stage('Joined', joined, '#3fb8ff', 1);""",
  "      mid=conv(joined, total, " + tr("of recorded invites joined") + ", '#3fb8ff')\n        +stage(" + tr("Joined") + ", joined, '#3fb8ff', 1);", tag="J6-fun-mid2")
html = rep(html, """      +stage('Recorded', total, '#a06bff', 0)""",
  "      +stage(" + tr("Recorded") + ", total, '#a06bff', 0)", expect=2, tag="J6-fun-stage")
# faces front: head line + Hello subject prefix (app-composed, editable by the citizen).
html = rep(html, """    if (head) head.textContent = !d.peopleList.length ? 'No faces yet — the first post, message or invite brings one.'
      : d.peopleAround.length+(d.peopleAround.length===1?' person':' people')+' around this world.';""",
  "    if (head) head.textContent = !d.peopleList.length ? " + tr("No faces yet — the first post, message or invite brings one.") + "\n      : d.peopleAround.length+(d.peopleAround.length===1?" + tr(" person") + ":" + tr(" people") + ")+" + tr(" around this world.") + ";", tag="J6-faces-head")
html = rep(html, """        var s=$('os-msg-subject'); if (s) s.value='Hello '+b.getAttribute('data-dash-msg');""",
  "        var s=$('os-msg-subject'); if (s) s.value=" + tr("Hello ") + "+b.getAttribute('data-dash-msg');", tag="J6-faces-hello")
# insights (buildInsights).
html = rep(html, """      out.push({c:'#ffbf3d', t:d.waiting.length+' conversations are waiting for your reply — the oldest unanswered is '+ow.name+'’s, waiting since '+relLabel(ow.at)+'.', e:d.waiting.length+' waiting · oldest '+relLabel(ow.at), go:'inbox', label:'Answer in the inbox'});""",
  "      out.push({c:'#ffbf3d', t:d.waiting.length+" + tr(" conversations are waiting for your reply — the oldest unanswered is ") + "+ow.name+" + tr("’s, waiting since ") + "+relLabel(ow.at)+'.', e:d.waiting.length+" + tr(" waiting · oldest ") + "+relLabel(ow.at), go:'inbox', label:" + tr("Answer in the inbox") + "});", tag="J6-ins-waiting")
html = rep(html, """      out.push({c:'#2fe89e', t:d.joined+(d.joined===1?' person has':' people have')+' walked the whole invite journey in this world — recorded and joined. Growth here has already happened.', e:'From '+d.invRows.length+' recorded invites', go:'growth', label:'See the journey'});""",
  "      out.push({c:'#2fe89e', t:d.joined+(d.joined===1?" + tr(" person has") + ":" + tr(" people have") + ")+" + tr(" walked the whole invite journey in this world — recorded and joined. Growth here has already happened.") + ", e:" + tr("From ") + "+d.invRows.length+" + tr(" recorded invites") + ", go:'growth', label:" + tr("See the journey") + "});", tag="J6-ins-journey")
html = rep(html, """      out.push({c:'#ff5e6c', t:d.invRows.length+(d.invRows.length===1?' invite is':' invites are')+' recorded and waiting — record-only by design; nothing has gone out yet.', e:'Joined 0 — stated honestly', go:'growth', label:'Open Growth'});""",
  "      out.push({c:'#ff5e6c', t:d.invRows.length+(d.invRows.length===1?" + tr(" invite is") + ":" + tr(" invites are") + ")+" + tr(" recorded and waiting — record-only by design; nothing has gone out yet.") + ", e:" + tr("Joined 0 — stated honestly") + ", go:'growth', label:" + tr("Open Growth") + "});", tag="J6-ins-dry")
html = rep(html, """      out.push({c:'#ff9a5a', t:'Invites are recorded — the first join is the milestone ahead.', e:d.invRows.length+' recorded · 0 joined', go:'growth', label:'Open Growth'});""",
  "      out.push({c:'#ff9a5a', t:" + tr("Invites are recorded — the first join is the milestone ahead.") + ", e:d.invRows.length+" + tr(" recorded · 0 joined") + ", go:'growth', label:" + tr("Open Growth") + "});", tag="J6-ins-waiting2")
html = rep(html, """      if (ws.pv>0 && ws.wk>ws.pv) out.push({c:'#a06bff', t:'Your world is speeding up — '+ws.wk+' events this week against '+ws.pv+' the week before.', e:ws.wk+' this week · '+ws.pv+' last week', go:'reports', label:'See Reports'});""",
  "      if (ws.pv>0 && ws.wk>ws.pv) out.push({c:'#a06bff', t:" + tr("Your world is speeding up — ") + "+ws.wk+" + tr(" events this week against ") + "+ws.pv+" + tr(" the week before.") + ", e:ws.wk+" + tr(" this week · ") + "+ws.pv+" + tr(" last week") + ", go:'reports', label:" + tr("See Reports") + "});", tag="J6-ins-fast")
html = rep(html, """      else if (ws.pv>0 && ws.wk<ws.pv) out.push({c:'#a06bff', t:'A quieter week — '+ws.wk+' events against '+ws.pv+' the week before.', e:ws.wk+' this week · '+ws.pv+' last week', go:'reports', label:'See Reports'});""",
  "      else if (ws.pv>0 && ws.wk<ws.pv) out.push({c:'#a06bff', t:" + tr("A quieter week — ") + "+ws.wk+" + tr(" events against ") + "+ws.pv+" + tr(" the week before.") + ", e:ws.wk+" + tr(" this week · ") + "+ws.pv+" + tr(" last week") + ", go:'reports', label:" + tr("See Reports") + "});", tag="J6-ins-quiet")
html = rep(html, """      else if (ws.pv>0) out.push({c:'#a06bff', t:'Steady as she goes — '+ws.wk+' events this week, the same pace as last.', e:ws.wk+' this week · '+ws.pv+' last week', go:'reports', label:'See Reports'});""",
  "      else if (ws.pv>0) out.push({c:'#a06bff', t:" + tr("Steady as she goes — ") + "+ws.wk+" + tr(" events this week, the same pace as last.") + ", e:ws.wk+" + tr(" this week · ") + "+ws.pv+" + tr(" last week") + ", go:'reports', label:" + tr("See Reports") + "});", tag="J6-ins-steady")
html = rep(html, """      else out.push({c:'#a06bff', t:'Every event in this world landed in the last 7 days — '+ws.wk+' of them.', e:ws.wk+' events, all this week', go:'reports', label:'See Reports'});""",
  "      else out.push({c:'#a06bff', t:" + tr("Every event in this world landed in the last 7 days — ") + "+ws.wk+" + tr(" of them.") + ", e:ws.wk+" + tr(" events, all this week") + ", go:'reports', label:" + tr("See Reports") + "});", tag="J6-ins-allweek")
html = rep(html, """      if (Date.now()-new Date(d.postTimes[0]).getTime()>2*864e5) out.push({c:'#3fb8ff', t:'The feed has been quiet since '+relLabel(d.postTimes[0])+'.', e:'Latest post '+relLabel(d.postTimes[0]), go:'home', label:'Make a post on the feed'});""",
  "      if (Date.now()-new Date(d.postTimes[0]).getTime()>2*864e5) out.push({c:'#3fb8ff', t:" + tr("The feed has been quiet since ") + "+relLabel(d.postTimes[0])+ " + "'.'" + ", e:" + tr("Latest post ") + "+relLabel(d.postTimes[0]), go:'home', label:" + tr("Make a post on the feed") + "});", tag="J6-ins-feedquiet")
html = rep(html, """      out.push({c:'#3fb8ff', t:'The feed is empty — the first post is its first heartbeat.', e:'0 posts so far', go:'home', label:'Start with the feed'});""",
  "      out.push({c:'#3fb8ff', t:" + tr("The feed is empty — the first post is its first heartbeat.") + ", e:" + tr("0 posts so far") + ", go:'home', label:" + tr("Start with the feed") + "});", tag="J6-ins-feedempty")
html = rep(html, """    if (hot>0) out.push({c:'#ff9a5a', t:hot+(hot===1?' person has':' people have')+' been around your world in the last day — say hello while it is warm.', e:hot+' active in the last 24 hours', go:'people', label:'See the faces'});""",
  "    if (hot>0) out.push({c:'#ff9a5a', t:hot+(hot===1?" + tr(" person has been around") + ":" + tr(" people have been around") + ")+" + tr(" your world in the last day — say hello while it is warm.") + ", e:hot+" + tr(" active in the last 24 hours") + ", go:'people', label:" + tr("See the faces") + "});", tag="J6-ins-hot")
html = rep(html, """      out.push({c:'#ff9a5a', t:'Your most-saved note: \\u201C'+d.bestSave.title+'\\u201D — saved '+d.bestSave.n+(d.bestSave.n===1?' time':' times')+' in this app. What gets kept is what this world values.', e:'Counted from this app\\u2019s own save records', go:'notes', label:'See Smart Notes'});""",
  "      out.push({c:'#ff9a5a', t:" + tr("Your most-saved note: “") + "+d.bestSave.title+" + tr("” — saved ") + "+d.bestSave.n+(d.bestSave.n===1?" + tr(" time") + ":" + tr(" times") + ")+" + tr(" in this app. What gets kept is what this world values.") + ", e:" + tr("Counted from this app’s own save records") + ", go:'notes', label:" + tr("See Smart Notes") + "});", tag="J6-ins-best")
html = rep(html, """    if (!out.length) out.push({c:'#a06bff', t:'Your world is brand new. Make a post on the feed, send the first message, record the first invite — and this front starts telling your story in sentences like these.', e:'Nothing to read yet — honestly', go:'home', label:'Start with the feed'});""",
  "    if (!out.length) out.push({c:'#a06bff', t:" + tr("Your world is brand new. Make a post on the feed, send the first message, record the first invite — and this front starts telling your story in sentences like these.") + ", e:" + tr("Nothing to read yet — honestly") + ", go:'home', label:" + tr("Start with the feed") + "});", tag="J6-ins-new")
# pickMove: the drop strings are matched against translated insight text, so they
# translate too — their values are exact substrings of the insight fragments.
html = rep(html, """    if (d.waiting && d.waiting.length){ var w=d.waiting[d.waiting.length-1]; pick={c:'#ffbf3d', title:'A conversation is waiting', body:w.name+' wrote \\u201C'+(w.subject||'(no subject)')+'\\u201D '+relLabel(w.at)+' — it is waiting for your reply.', go:'inbox', label:'Open the inbox', drop:null}; }""",
  "    if (d.waiting && d.waiting.length){ var w=d.waiting[d.waiting.length-1]; pick={c:'#ffbf3d', title:" + tr("A conversation is waiting") + ", body:w.name+" + tr(" wrote “") + "+(w.subject||" + tr("(no subject)") + ")+'\\u201D '+relLabel(w.at)+" + tr(" — it is waiting for your reply.") + ", go:'inbox', label:" + tr("Open the inbox") + ", drop:null}; }", tag="J6-pick-waiting")
html = rep(html, """    else if (d.joined>0){ pick={c:'#2fe89e', title:'The journey completed', body:d.joined+(d.joined===1?' person has':' people have')+' walked the whole invite journey in this world.', go:'growth', label:'See the journey', drop:'walked the whole invite journey in this world'}; }""",
  "    else if (d.joined>0){ pick={c:'#2fe89e', title:" + tr("The journey completed") + ", body:d.joined+(d.joined===1?" + tr(" person has") + ":" + tr(" people have") + ")+" + tr(" walked the whole invite journey in this world.") + ", go:'growth', label:" + tr("See the journey") + ", drop:" + tr("walked the whole invite journey in this world") + "}; }", tag="J6-pick-journey")
html = rep(html, """    else if (d.invRows.length){ pick={c:'#ff5e6c', title:'Invites recorded and waiting', body:d.invRows.length+(d.invRows.length===1?' invite is':' invites are')+' recorded — the next milestone is a first open.', go:'growth', label:'Open Growth', drop:'recorded and waiting'}; }""",
  "    else if (d.invRows.length){ pick={c:'#ff5e6c', title:" + tr("Invites recorded and waiting") + ", body:d.invRows.length+(d.invRows.length===1?" + tr(" invite is") + ":" + tr(" invites are") + ")+" + tr(" recorded — the next milestone is a first open.") + ", go:'growth', label:" + tr("Open Growth") + ", drop:" + tr("recorded and waiting") + "}; }", tag="J6-pick-recorded")
html = rep(html, """    else if (d.posts.length){ var p0=d.posts[0]; pick={c:'#a06bff', title:'The newest voice on the feed', body:(p0.j.a||'Guest')+' posted '+relLabel(p0.at)+': \\u201C'+String(p0.j.b||'').slice(0, 90)+'\\u201D', go:'home', label:'See the feed', drop:null}; }""",
  "    else if (d.posts.length){ var p0=d.posts[0]; pick={c:'#a06bff', title:" + tr("The newest voice on the feed") + ", body:(p0.j.a||" + tr("Guest") + ")+" + tr(" posted ") + "+relLabel(p0.at)+" + tr(": “") + "+String(p0.j.b||'').slice(0, 90)+" + tr("”") + ", go:'home', label:" + tr("See the feed") + ", drop:null}; }", tag="J6-pick-voice")
html = rep(html, """    else { pick={c:'#a06bff', title:'A brand-new world', body:'The first post, message or invite becomes this world\\u2019s first move.', go:'home', label:'Start with the feed', drop:null}; }""",
  "    else { pick={c:'#a06bff', title:" + tr("A brand-new world") + ", body:" + tr("The first post, message or invite becomes this world’s first move.") + ", go:'home', label:" + tr("Start with the feed") + ", drop:null}; }", tag="J6-pick-new")
# renderConvos.
html = rep(html, """    if (!d.threads.length){ box.innerHTML='<div class="os-status">No conversations yet — the first message opens one here.</div>'; return; }""",
  "    if (!d.threads.length){ box.innerHTML='<div class=\"os-status\">'+" + tr("No conversations yet — the first message opens one here.") + "+'</div>'; return; }", tag="J6-convos-empty")
html = rep(html, """esc(t.subject||'(no subject)')""", "esc(t.subject||" + tr("(no subject)") + ")", tag="J6-convos-subj")

# ---------- J7: heat, dimensions, Smart Links board ----------
# dayCounts note locale + event/events.
html = rep(html, """      return {n:c, d:d, today:ix===n-1, note:d.toLocaleDateString('en-US',{weekday:'long', month:'long', day:'numeric'})+': '+c+(c===1?' event':' events')+'.'};""",
  "      return {n:c, d:d, today:ix===n-1, note:d.toLocaleDateString((window.mwLocale?window.mwLocale():'en-US'),{weekday:'long', month:'long', day:'numeric'})+': '+c+(c===1?" + tr(" event") + ":" + tr(" events") + ")+'.'};", tag="J7-daycounts")
html = rep(html, """    if (note) note.textContent=total?('Fourteen days, '+total+(total===1?' event':' events')+' — tap a day to read it.'):'A quiet fourteen days — the next post, note, message or invite lights the first cell.';""",
  "    if (note) note.textContent=total?(" + tr("Fourteen days, ") + "+total+(total===1?" + tr(" event") + ":" + tr(" events") + ")+" + tr(" — tap a day to read it.") + "):" + tr("A quiet fourteen days — the next post, note, message or invite lights the first cell.") + ";", tag="J7-heat-note")
html = rep(html, """    if (cur>0) lines.push('On a '+cur+'-day streak — something landed '+cur+(cur===1?' day':' days')+' running.');""",
  "    if (cur>0) lines.push(" + tr("On a ") + "+cur+" + tr("-day streak — something landed ") + "+cur+(cur===1?" + tr(" day") + ":" + tr(" days") + ")+" + tr(" running.") + ");", tag="J7-streak-cur")
html = rep(html, """    else lines.push('No streak running — the next event starts one.');""",
  "    else lines.push(" + tr("No streak running — the next event starts one.") + ");", tag="J7-streak-none")
html = rep(html, """    if (longest>cur) lines.push('Longest streak so far: '+longest+(longest===1?' day':' days')+'.');""",
  "    if (longest>cur) lines.push(" + tr("Longest streak so far: ") + "+longest+(longest===1?" + tr(" day") + ":" + tr(" days") + ")+'.');", tag="J7-streak-long")
html = rep(html, """    lines.push(active30+(active30===1?' active day':' active days')+' in the last thirty.');""",
  "    lines.push(active30+(active30===1?" + tr(" active day") + ":" + tr(" active days") + ")+" + tr(" in the last thirty.") + ");", tag="J7-streak-30")
# dimLabel: the class maps stay English keys; the returned label translates.
html = rep(html, """    if (v===null || v===undefined || v==='' || v==='unknown' || v==='null' || v==='undefined') return 'Not recorded';""",
  "    if (v===null || v===undefined || v==='' || v==='unknown' || v==='null' || v==='undefined') return " + tr("Not recorded") + ";", tag="J7-dim-none")
html = rep(html, """    return m[v]||(String(v).charAt(0).toUpperCase()+String(v).slice(1));""",
  "    var _lbl=m[v]||(String(v).charAt(0).toUpperCase()+String(v).slice(1)); return (window.mwTr?window.mwTr(_lbl):_lbl);", tag="J7-dim-label")
html = rep(html, """    var when=dim.first===dim.last?('on '+dim.first):('from '+dim.first+' to '+dim.last);""",
  "    var when=dim.first===dim.last?(" + tr("on ") + "+dim.first):(" + tr("from ") + "+dim.first+" + tr(" to ") + "+dim.last);", tag="J7-dim-when")
html = rep(html, """    return '<div class="os-link-dim" data-dim-for="'+esc(r.name)+'" hidden><p class="os-note">Every counted click on this link, '+when+' — where it came from, what it arrived on, and where in the world it was.</p>'+dimGroup('Came from', dim.from, 'referrer')+dimGroup('Arrived on', dim.on, 'device')+dimGroup('From', dim.country, 'country')+'</div>';""",
  "    return '<div class=\"os-link-dim\" data-dim-for=\"'+esc(r.name)+'\" hidden><p class=\"os-note\">'+" + tr("Every counted click on this link, ") + "+when+" + tr(" — where it came from, what it arrived on, and where in the world it was.") + "+'</p>'+dimGroup(" + tr("Came from") + ", dim.from, 'referrer')+dimGroup(" + tr("Arrived on") + ", dim.on, 'device')+dimGroup(" + tr("From") + ", dim.country, 'country')+'</div>';", tag="J7-dim-panel")
# slDayBuckets locales + click/join units.
html = rep(html, """        lab: d.toLocaleDateString('en-US', { weekday: 'short' }),
        note: d.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' }) });""",
  "        lab: d.toLocaleDateString((window.mwLocale?window.mwLocale():'en-US'), { weekday: 'short' }),\n        note: d.toLocaleDateString((window.mwLocale?window.mwLocale():'en-US'), { weekday: 'long', month: 'long', day: 'numeric' }) });", tag="J7-buckets-locale")
html = rep(html, """    out.forEach(function(b){ b.note += ': ' + b.n + (b.n === 1 ? ' click' : ' clicks') + (b.j ? ', ' + b.j + (b.j === 1 ? ' join' : ' joins') : '') + '.'; });""",
  "    out.forEach(function(b){ b.note += ': ' + b.n + (b.n === 1 ? " + tr(" click") + " : " + tr(" clicks") + ") + (b.j ? ', ' + b.j + (b.j === 1 ? " + tr(" join") + " : " + tr(" joins") + ") : '') + '.'; });", tag="J7-buckets-units")
html = rep(html, """    var note = total ? ('Busiest: ' + buckets[bi].note + ' Tap a bar to read its day.') : 'No clicks yet — this graph wakes with the first click.';""",
  "    var note = total ? (" + tr("Busiest: ") + " + buckets[bi].note + " + tr(" Tap a bar to read its day.") + ") : " + tr("No clicks yet — this graph wakes with the first click.") + ";", tag="J7-graph-note")
# renderLinks: head + row units/buttons + footer. (T4 hook re-syncs the row buttons.)
html = rep(html, """      if (head) head.textContent='Your links couldn’t be read — tap to retry.';""",
  "      if (head) head.textContent=" + tr("Your links couldn’t be read — tap to retry.") + ";", tag="J7-links-err")
html = rep(html, """    if (head) head.textContent=!rows.length?'No Smart Links yet — claim a name and every click through it starts counting here.'
      :(rows.length+(rows.length===1?' link':' links')+' out in the world — '+tc+(tc===1?' click':' clicks')+' counted, '+tj+(tj===1?' join':' joins')+' attributed.');""",
  "    if (head) head.textContent=!rows.length?" + tr("No Smart Links yet — claim a name and every click through it starts counting here.") + "\n      :(rows.length+(rows.length===1?" + tr(" link") + ":" + tr(" links") + ")+" + tr(" out in the world — ") + "+tc+(tc===1?" + tr(" click") + ":" + tr(" clicks") + ")+" + tr(" counted, ") + "+tj+(tj===1?" + tr(" join") + ":" + tr(" joins") + ")+" + tr(" attributed.") + ");", tag="J7-links-head")
html = rep(html, """<b data-sl-num="'+esc(r.name)+':clicks">0</b><i>clicks</i></span><span class="os-link-num"><b data-sl-num="'+esc(r.name)+':joins">0</b><i>joins</i></span>""",
  "<b data-sl-num=\"'+esc(r.name)+':clicks\">0</b><i>'+" + tr("clicks") + "+'</i></span><span class=\"os-link-num\"><b data-sl-num=\"'+esc(r.name)+':joins\">0</b><i>'+" + tr("joins") + "+'</i></span>", tag="J7-links-units")
html = rep(html, """data-sl-copy="'+esc(r.name)+'">Copy the link</button>""",
  "data-sl-copy=\"'+esc(r.name)+'\">'+" + tr("Copy the link") + "+'</button>", tag="J7-links-copy")
html = rep(html, """data-sl-open="'+esc(r.name)+'">Open it</button>'""",
  "data-sl-open=\"'+esc(r.name)+'\">'+" + tr("Open it") + "+'</button>'", tag="J7-links-open")
html = rep(html, """data-sl-dim="'+esc(r.name)+'">Breakdown</button>'""",
  "data-sl-dim=\"'+esc(r.name)+'\">'+" + tr("Breakdown") + "+'</button>'", tag="J7-links-dim")
html = rep(html, """    }).join('')+(tc>0?'<p class="os-note">Clicked &rarr; Joined: '+tc+(tc===1?' click':' clicks')+' became '+tj+(tj===1?' join':' joins')+(tj?(' — '+Math.round(tj/tc*100)+'% of clicks joined.'):' — the first join is the milestone ahead.')+'</p>':'<p class=""",
  "    }).join('')+(tc>0?'<p class=\"os-note\">'+" + tr("Clicked → Joined: ") + "+tc+(tc===1?" + tr(" click") + ":" + tr(" clicks") + ")+" + tr(" became ") + "+tj+(tj===1?" + tr(" join") + ":" + tr(" joins") + ")+(tj?(' — '+Math.round(tj/tc*100)+" + tr("% of clicks joined.") + "):" + tr(" — the first join is the milestone ahead.") + ")+'</p>':'<p class=\"", tag="J7-links-foot")
# loadDashboard stores the link args so osRerenderDashboard can re-run renderLinks.
html = rep(html, """        dashCache=d;""",
  "        dashCache=d; window._dashLinkArgs=[out[3], out[4], linkErr.v, out[5]];", tag="J7-linkargs")

# ---------- J8: booking + payments plug-ins, loadDashboard, feedback ----------
html = rep(html, """      return d.toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric' }) +
        ' \\u00b7 ' + d.toLocaleTimeString(undefined, { hour: 'numeric', minute: '2-digit' });""",
  "      return d.toLocaleDateString((window.mwLocale?window.mwLocale():undefined), { weekday: 'short', month: 'short', day: 'numeric' }) +\n        ' \\u00b7 ' + d.toLocaleTimeString((window.mwLocale?window.mwLocale():undefined), { hour: 'numeric', minute: '2-digit' });", tag="J8-plugwhen-locale")
html = rep(html, """    function unread(){ if (note) note.textContent = 'The booking state could not be read just now.'; }""",
  "    function unread(){ if (note) note.textContent = " + tr("The booking state could not be read just now.") + "; }", tag="J8-book-unread")
html = rep(html, """chip.textContent = '\\u25cf LIVE';""",
  "chip.textContent = '\\u25cf ' + " + tr("LIVE") + ";", expect=2, tag="J8-chip-live")
html = rep(html, """        var line = upcoming === 1 ? '1 appointment coming' : upcoming + ' appointments coming';""",
  "        var line = upcoming === 1 ? " + tr("1 appointment coming") + " : " + tr("{n} appointments coming") + ".replace('{n}', upcoming);", tag="J8-book-line")
html = rep(html, """        if (st.next_at) line += ' \\u00b7 next ' + plugWhenLabel(st.next_at) + (st.next_title ? ' \\u2014 ' + st.next_title : '');""",
  "        if (st.next_at) line += " + tr(" · next ") + " + plugWhenLabel(st.next_at) + (st.next_title ? ' \\u2014 ' + st.next_title : '');", tag="J8-book-next")
html = rep(html, """        if (note) note.textContent = (st.pages > 1 ? 'Your booking pages are live \\u2014 ' : 'Your booking page is live \\u2014 ') + line + '.';""",
  "        if (note) note.textContent = (st.pages > 1 ? " + tr("Your booking pages are live — ") + " : " + tr("Your booking page is live — ") + ") + line + '.';", tag="J8-book-live")
html = rep(html, """            ? 'Calendar sync is connected \\u2014 bookings also land on your calendar.'
            : 'Calendar sync: not connected yet \\u2014 bookings live in NayaNET only, and every one is filed on the person it belongs to.') + '</span></div>' +""",
  "            ? " + tr("Calendar sync is connected — bookings also land on your calendar.") + "\n            : " + tr("Calendar sync: not connected yet — bookings live in NayaNET only, and every one is filed on the person it belongs to.") + ") + '</span></div>' +", tag="J8-book-sync")
html = rep(html, """<span>Your booking door: <b>nayanet.app/book?book='""",
  "<span>'+" + tr("Your booking door: ") + "+'<b>nayanet.app/book?book='", tag="J8-book-door")
html = rep(html, """    if (!paid) return 'Payments are connected \\u2014 nothing has come in yet. The first payment lands here as a sentence, not a spreadsheet.';""",
  "    if (!paid) return " + tr("Payments are connected — nothing has come in yet. The first payment lands here as a sentence, not a spreadsheet.") + ";", tag="J8-pay-none")
html = rep(html, """    var s = 'You made ' + plugMoney(st.gross_cents) + ' from ' + paid + (paid === 1 ? ' payment' : ' payments');""",
  "    var s = " + tr("You made ") + " + plugMoney(st.gross_cents) + " + tr(" from ") + " + paid + (paid === 1 ? " + tr(" payment") + " : " + tr(" payments") + ");", tag="J8-pay-made")
html = rep(html, """    if (st.best_title && Number(st.best_cents || 0) > 0) s += ' \\u2014 best earner \\u201c' + st.best_title + '\\u201d (' + plugMoney(st.best_cents) + ')';""",
  "    if (st.best_title && Number(st.best_cents || 0) > 0) s += " + tr(" — best earner “") + " + st.best_title + " + tr("” (") + " + plugMoney(st.best_cents) + ')';", tag="J8-pay-best")
html = rep(html, """    function unread(){ if (note) note.textContent = 'The payments state could not be read just now.'; }""",
  "    function unread(){ if (note) note.textContent = " + tr("The payments state could not be read just now.") + "; }", tag="J8-pay-unread")
html = rep(html, """        if (repLine) repLine.textContent = live
          ? 'Money so far: ' + plugRevenue(st)
          : (st.links
            ? 'Money: your payment link is live, but payments are not connected yet \\u2014 there is no revenue to report until they are.'
            : 'Money: payments are not connected yet, so there is no revenue to report \\u2014 the sentence lands here the day they are.');""",
  "        if (repLine) repLine.textContent = live\n          ? " + tr("Money so far: ") + " + plugRevenue(st)\n          : (st.links\n            ? " + tr("Money: your payment link is live, but payments are not connected yet — there is no revenue to report until they are.") + "\n            : " + tr("Money: payments are not connected yet, so there is no revenue to report — the sentence lands here the day they are.") + ");", tag="J8-pay-repline")
html = rep(html, """          if (note) note.textContent = (state === 'test' ? 'Test mode. ' : '') + plugRevenue(st);""",
  "          if (note) note.textContent = (state === 'test' ? " + tr("Test mode. ") + " : '') + plugRevenue(st);", tag="J8-pay-test")
html = rep(html, """          note.textContent = (st.links > 1 ? 'Your payment links are live' : 'Your payment link is live') + ' \\u2014 the door shows the real price and says plainly that payments are not switched on. The money starts the day you connect Stripe.';""",
  "          note.textContent = (st.links > 1 ? " + tr("Your payment links are live") + " : " + tr("Your payment link is live") + ") + " + tr(" — the door shows the real price and says plainly that payments are not switched on. The money starts the day you connect Stripe.") + ";", tag="J8-pay-links")
html = rep(html, """          if (!live) rows += '<div class="os-feeds-row">\\ud83d\\udcb3 <span>Payments: not connected yet \\u2014 connecting Stripe is one sign-in, and it is yours to make.</span></div>';""",
  "          if (!live) rows += '<div class=\"os-feeds-row\">\\ud83d\\udcb3 <span>'+" + tr("Payments: not connected yet — connecting Stripe is one sign-in, and it is yours to make.") + "+'</span></div>';", tag="J8-pay-notconn")
html = rep(html, """          if (Number(st.failed_count || 0) > 0) rows += '<div class="os-feeds-row">\\u26a0\\ufe0f <span>' + st.failed_count + (st.failed_count === 1 ? ' payment didn\\u2019t go through' : ' payments didn\\u2019t go through') + ' \\u2014 a recovery draft is waiting in your Growth room.</span></div>';""",
  "          if (Number(st.failed_count || 0) > 0) rows += '<div class=\"os-feeds-row\">\\u26a0\\ufe0f <span>' + st.failed_count + (st.failed_count === 1 ? " + tr(" payment didn’t go through") + " : " + tr(" payments didn’t go through") + ") + " + tr(" — a recovery draft is waiting in your Growth room.") + "+'</span></div>';", tag="J8-pay-failed")
html = rep(html, """<span>Your payment door: <b>nayanet.app/pay?pay='""",
  "<span>'+" + tr("Your payment door: ") + "+'<b>nayanet.app/pay?pay='", tag="J8-pay-door")
# loadDashboard no-Supabase strings + faces facts.
html = rep(html, """      var n=$('os-dash-n-posts-note'); if (n) n.textContent='Connection unavailable — this front reads live data only, so it shows nothing rather than something invented.';""",
  "      var n=$('os-dash-n-posts-note'); if (n) n.textContent=" + tr("Connection unavailable — this front reads live data only, so it shows nothing rather than something invented.") + ";", tag="J8-load-conn1")
html = rep(html, """      var lh=$('os-dash-links-head'); if (lh) lh.textContent='Connection unavailable — Smart Links read live data only.';""",
  "      var lh=$('os-dash-links-head'); if (lh) lh.textContent=" + tr("Connection unavailable — Smart Links read live data only.") + ";", tag="J8-load-conn2")
html = rep(html, """        wallRows.forEach(function(p){ var a=p.j.a||'Guest'; var n=postCounts[a.toLowerCase()]; add(a, n+(n===1?' feed post':' feed posts'), p.at); });""",
  "        wallRows.forEach(function(p){ var a=p.j.a||" + tr("Guest") + "; var n=postCounts[a.toLowerCase()]; add(a, n+(n===1?" + tr(" feed post") + ":" + tr(" feed posts") + "), p.at); });", tag="J8-faces-posts")
html = rep(html, """        threads.forEach(function(t){ add(humanize(t.from_alias), 'Sent a message', t.created_at); });""",
  "        threads.forEach(function(t){ add(humanize(t.from_alias), " + tr("Sent a message") + ", t.created_at); });", tag="J8-faces-msg")
html = rep(html, """        invRows.forEach(function(v){ add(v.invitee_name, 'Invited', v.created_at); });""",
  "        invRows.forEach(function(v){ add(v.invitee_name, " + tr("Invited") + ", v.created_at); });", tag="J8-faces-inv")
# feedback card (Dashboard view): status strings + the app-composed subject.
html = rep(html, """    if (!body){ if (st) st.textContent='Write one line first.'; return; }""",
  "    if (!body){ if (st) st.textContent=" + tr("Write one line first.") + "; return; }", tag="J8-fb-write")
html = rep(html, """    if (!sb){ if (st) st.textContent='Connection unavailable — feedback not sent.'; return; }""",
  "    if (!sb){ if (st) st.textContent=" + tr("Connection unavailable — feedback not sent.") + "; return; }", tag="J8-fb-conn")
html = rep(html, """    if (st) st.textContent='Sending…';""",
  "    if (st) st.textContent=" + tr("Sending…") + ";", tag="J8-fb-sending")
html = rep(html, """'Send failed: '""", tr("Send failed: "), expect=5, tag="J8-fb-fail")
html = rep(html, """        inp.value=''; if (st) st.textContent='Sent — it is in this app’s Smart Mail inbox, for the person who runs this app. Thank you.';""",
  "        inp.value=''; if (st) st.textContent=" + tr("Sent — it is in this app’s Smart Mail inbox, for the person who runs this app. Thank you.") + ";", tag="J8-fb-sent")
html = rep(html, """    sb.from('smart_mail_threads').insert({subject:'Feedback — help shape this app', from_alias:'dashboard-feedback', to_alias:PAGE_ALIAS, preview:body.slice(0, 120)}).select().single().then(function(res){""",
  "    sb.from('smart_mail_threads').insert({subject:" + tr("Feedback — help shape this app") + ", from_alias:'dashboard-feedback', to_alias:PAGE_ALIAS, preview:body.slice(0, 120)}).select().single().then(function(res){", tag="J8-fb-subject")

# ---------- J9: dashboard IIFE — orb labels, aria, points board, series days ----------
for _lab in ("Sales", "Joins", "Smart notes", "Invites", "Creations", "Shares", "Comments", "Likes", "Saves"):
    html = rep(html, f"label:'{_lab}',", f"label:{tr(_lab)},", expect=(2 if _lab == 'Joins' else 1), tag=f"J9-node-{_lab.lower().replace(' ', '-')}")
html = rep(html, """      var al = _lbl+': '+pts.toLocaleString()+' points. Open detail.';""",
  "      var al = _lbl+': '+pts.toLocaleString()+" + tr(" points. Open detail.") + ";", tag="J9-orb-aria")
html = rep(html, """    else { var n=$('os-points-note'); if (n) n.textContent='Still reading — the connection is slow. Your actions count the moment it lands.';""",
  "    else { var n=$('os-points-note'); if (n) n.textContent=" + tr("Still reading — the connection is slow. Your actions count the moment it lands.") + ";", tag="J9-pointsboard")
html = rep(html, """    var DN=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];""",
  "    var DN=(function(){ try{ var loc=(window.mwLocale?window.mwLocale():'en-US'); var a=[]; for(var i=0;i<7;i++){ a.push(new Date(2026,0,4+i).toLocaleDateString(loc,{weekday:'short'})); } return a; }catch(e){ return ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']; } })();", tag="J9-dn-locale")

# ---------- J10: TnTacho captions, PERIODS, language invalidation ----------
html = rep(html, """    var PERIODS = { hour:'the last hour', day:'the last 24 hours',
                    week:'the last 7 days', month:'the last 30 days' };""",
  "    var PERIODS = { hour:" + tr("the last hour") + ", day:" + tr("the last 24 hours") + ",\n                    week:" + tr("the last 7 days") + ", month:" + tr("the last 30 days") + " };", tag="J10-periods")
html = rep(html, """    var displayed = 0;      /* the one value everything paints from */
    var lastNumTxt = '';""",
  "    var displayed = 0;      /* the one value everything paints from */\n    var lastNumTxt = '';\n    var _tnLastLang = null; /* THIRD-SURFACE-FIX: reset the cached label/caption on switch */", tag="J10-lastlang-var")
html = rep(html, """    function frame(){
      if (dead) return;
      var r = readSpine();""",
  "    function frame(){\n      if (dead) return;\n      var _lc=(window.mwLangCode?window.mwLangCode():'en'); if (_lc!==_tnLastLang){ _tnLastLang=_lc; if (label) label._t=null; cap._h=null; if (svgGain) svgGain._t=null; }\n      var r = readSpine();", tag="J10-frame-inval")
html = rep(html, """        if (label && label._t !== 'gained'){ label._t = 'gained'; label.textContent = 'GAINED'; }""",
  "        if (label && label._t !== 'gained'){ label._t = 'gained'; label.textContent = " + tr("GAINED") + "; }", tag="J10-label-gained")
html = rep(html, """        var _g = (_tot == null) ? 'GAINED' : 'GAINED \\u00B7 TOTAL ' + _tot;""",
  "        var _g = (_tot == null) ? " + tr("GAINED") + " : " + tr("GAINED · TOTAL ") + " + _tot;", tag="J10-svg-gain")
html = rep(html, """          setCap(_tot == null ? '+' + fmt(dm.target) + ' GAINED in ' + dm.period + '.' : '<b>+' + fmt(dm.target) + ' GAINED</b> in ' + dm.period + ' · Total <b>' + _tot + '</b>');""",
  "          setCap(_tot == null ? '+' + fmt(dm.target) + " + tr(" GAINED in ") + " + dm.period + '.' : '<b>+' + fmt(dm.target) + " + tr(" GAINED") + " + '</b>' + " + tr(" in ") + " + dm.period + " + tr(" · Total ") + " + '<b>' + _tot + '</b>');", tag="J10-cap-gained")
html = rep(html, """          setCap(_tot == null ? 'Nothing gained in ' + dm.period + ' — quiet is rest, not failure.' : 'Nothing gained in ' + dm.period + ' — quiet is rest, not failure. Total <b>' + _tot + '</b>');""",
  "          setCap(_tot == null ? " + tr("Nothing gained in ") + " + dm.period + " + tr(" — quiet is rest, not failure.") + " : " + tr("Nothing gained in ") + " + dm.period + " + tr(" — quiet is rest, not failure.") + " + " + tr(" Total ") + " + '<b>' + _tot + '</b>');", tag="J10-cap-nothing")
html = rep(html, """        root.setAttribute('aria-label', 'Score gauge — gained ' + fmt(dm.target) + ' in ' + dm.period);""",
  "        root.setAttribute('aria-label', " + tr("Score gauge — gained ") + " + fmt(dm.target) + " + tr(" in ") + " + dm.period);", tag="J10-aria-gained")
html = rep(html, """label.textContent = 'YOUR SMART SCORE'""",
  "label.textContent = " + tr("YOUR SMART SCORE"), expect=2, tag="J10-label-score")
html = rep(html, """        setCap('Period timing isn\\u2019t on the ledger yet \\u2014 this pill reads the total for now.');""",
  "        setCap(" + tr("Period timing isn’t on the ledger yet — this pill reads the total for now.") + ");", tag="J10-cap-period")
html = rep(html, """root.setAttribute('aria-label', 'Score gauge — your live score is ' + fmt(score));""",
  "root.setAttribute('aria-label', " + tr("Score gauge — your live score is ") + " + fmt(score));", expect=2, tag="J10-aria-live")
html = rep(html, """        root.setAttribute('aria-label', 'Score gauge — quiet, no score yet');""",
  "        root.setAttribute('aria-label', " + tr("Score gauge — quiet, no score yet") + ");", tag="J10-aria-quiet")
html = rep(html, """        root.setAttribute('aria-label', 'Score gauge — reading your actions');""",
  "        root.setAttribute('aria-label', " + tr("Score gauge — reading your actions") + ");", tag="J10-aria-reading")
html = rep(html, """<span class="tn-tacho-label">YOUR SMART SCORE</span>""",
  "<span class=\"tn-tacho-label\">'+" + tr("YOUR SMART SCORE") + "+'</span>", tag="J10-tacho-html")
html = rep(html, """aria-label="Smart Score gauge — tap for deeper stats">""",
  "aria-label=\"'+" + tr("Smart Score gauge — tap for deeper stats") + "+'\">", tag="J10-tacho-aria")
html = rep(html, """      if (lab) lab.textContent = gain ? 'GAINED' : 'SMART SCORE';""",
  "      if (lab) lab.textContent = gain ? " + tr("GAINED") + " : " + tr("SMART SCORE") + ";", tag="J10-featured-label")

# ---------- J11: drawer, osStatsView, link drawer ----------
html = rep(html, """>7-DAY TREND</div>""", ">'+" + tr("7-DAY TREND") + "+'</div>", expect=2, tag="J11-trend7")
html = rep(html, """>THIS WEEK</div>""", ">'+" + tr("THIS WEEK") + "+'</div>", tag="J11-thisweek-div")
html = rep(html, """_cc(week.toLocaleString(), 'THIS WEEK', '#fff')""",
  "_cc(week.toLocaleString(), " + tr("THIS WEEK") + ", '#fff')", tag="J11-thisweek-cc")
html = rep(html, """_cc(prior.toLocaleString(), 'PRIOR WEEK', '#fff')""",
  "_cc(prior.toLocaleString(), " + tr("PRIOR WEEK") + ", '#fff')", tag="J11-priorweek")
html = rep(html, """_cc(older.toLocaleString(), 'OLDER', '#fff')""",
  "_cc(older.toLocaleString(), " + tr("OLDER") + ", '#fff')", tag="J11-older")
html = rep(html, """    var WD = ['S','M','T','W','T','F','S'];""",
  "    var WD = (function(){ try{ var loc=(window.mwLocale?window.mwLocale():'en-US'); var a=[]; for(var i=0;i<7;i++){ a.push(new Date(2026,0,4+i).toLocaleDateString(loc,{weekday:'short'}).charAt(0).toUpperCase()); } return a; }catch(e){ return ['S','M','T','W','T','F','S']; } })();", tag="J11-wd-locale")
html = rep(html, """+last7[i].c+' clicks" """, "+last7[i].c+" + tr(" clicks") + "+'\" ", tag="J11-bar-title")
html = rep(html, """>CLICKS</div>""", ">'+" + tr("CLICKS") + "+'</div>", expect=2, tag="J11-clicks-label")
html = rep(html, """'<div class="os-detail-sub">nayanet.app/'+esc(link.name)+' · '+link.joins+' joins attributed</div>'""",
  "'<div class=\"os-detail-sub\">nayanet.app/'+esc(link.name)+' · '+link.joins+" + tr(" joins attributed") + "+'</div>'", tag="J11-link-sub")
html = rep(html, """    osStatsView(vals, '#a06bff', 'clicks')+""",
  "    osStatsView(vals, '#a06bff', " + tr("clicks") + ")+", tag="J11-stats-label")
html = rep(html, """<span class="os-dg-wk-l">this week</span>""",
  "<span class=\"os-dg-wk-l\">'+" + tr("this week") + "+'</span>", tag="J11-link-week")
html = rep(html, "title=\"'+v+' clicks\"", "title=\"'+v+" + tr(" clicks") + "+'\"", tag="J11-link-bartitle")
html = rep(html, """+Math.abs(delta)+'% vs last""", "+Math.abs(delta)+" + tr("% vs last") + "+'</span></div>", tag="J11-vs-last")
html = rep(html, """(bestK?'<div class="os-dg-streak" style="color:#a06bff">★ Best: '+best+' on '+bestK+'</div>':'')""",
  "(bestK?'<div class=\"os-dg-streak\" style=\"color:#a06bff\">'+" + tr("★ Best: ") + "+best+" + tr(" on ") + "+bestK+'</div>':'')", tag="J11-best")
# osStatsView chrome + locales.
html = rep(html, """    return d.toLocaleDateString('en-US',{month:'short',day:'numeric'});""",
  "    return d.toLocaleDateString((window.mwLocale?window.mwLocale():'en-US'),{month:'short',day:'numeric'});", tag="J11-daylabel")
html = rep(html, """  var barsView = '<div class="os-dg-headline">'+total.toLocaleString()+' '+label+' in 30 days · avg '+avg+'/day'+(peakV>0?' · peak '+peakV+' on '+dayLabel(peakIx):'')+'</div>'+""",
  "  var barsView = '<div class=\"os-dg-headline\">'+total.toLocaleString()+' '+label+" + tr(" in 30 days · avg ") + "+avg+" + tr("/day") + "+(peakV>0?" + tr(" · peak ") + "+peakV+" + tr(" on ") + "+dayLabel(peakIx):'')+'</div>'+", tag="J11-bars-head")
html = rep(html, """<div class="os-dg-label">each bar = one day · hover for exact date + count</div>""",
  "<div class=\"os-dg-label\">'+" + tr("each bar = one day · hover for exact date + count") + "+'</div>", tag="J11-bars-label")
html = rep(html, """  var flowHeadline = peakV>0 ?
    'Peak activity: '+peakV+' '+label+' on '+dayLabel(peakIx)+' — '+((function(){var daysAgo=29-peakIx; return daysAgo<=7?'this week':(daysAgo<=14?'last week':'earlier this month');})()) :
    'No '+label+' in the last 30 days';""",
  "  var flowHeadline = peakV>0 ?\n    " + tr("Peak activity: ") + "+peakV+' '+label+" + tr(" on ") + "+dayLabel(peakIx)+' — '+((function(){var daysAgo=29-peakIx; return daysAgo<=7?" + tr("this week") + ":(daysAgo<=14?" + tr("last week") + ":" + tr("earlier this month") + ");})()) :\n    " + tr("No ") + "+label+" + tr(" in the last 30 days") + ";", tag="J11-flow-head")
html = rep(html, """'</svg><div class="os-dg-label">the shape of your '+label+' — rises show when you are most active</div>';""",
  "'</svg><div class=\"os-dg-label\">'+" + tr("the shape of your ") + "+label+" + tr(" — rises show when you are most active") + "+'</div>';", tag="J11-flow-label")
html = rep(html, """    trendText='no '+label+' in the last 30 days';""",
  "    trendText=" + tr("no ") + "+label+" + tr(" in the last 30 days") + ";", tag="J11-trend-none")
html = rep(html, """    trendText='new activity — '+secondHalf+' '+label+' in the last 15 days';""",
  "    trendText=" + tr("new activity — ") + "+secondHalf+' '+label+" + tr(" in the last 15 days") + ";", tag="J11-trend-new")
html = rep(html, """    trendText = trendIcon+' '+Math.abs(trendPct)+'% '+trendDir+' — '+(trendDir==='rising'?'your '+label+' are accelerating':(trendDir==='falling'?'your '+label+' are slowing down':'your '+label+' are holding steady'));""",
  "    trendText = trendIcon+' '+Math.abs(trendPct)+'% '+trendDir+' — '+(trendDir==='rising'?" + tr("your ") + "+label+" + tr(" are accelerating") + ":(trendDir==='falling'?" + tr("your ") + "+label+" + tr(" are slowing down") + ":" + tr("your ") + "+label+" + tr(" are holding steady") + "));", tag="J11-trend-dir")
html = rep(html, """'</svg><div class="os-dg-label">comparing first 15 days vs last 15 days</div>';""",
  "'</svg><div class=\"os-dg-label\">'+" + tr("comparing first 15 days vs last 15 days") + "+'</div>';", tag="J11-trend-label")
html = rep(html, """    var wlabel = i===0?'This week':(i===1?'Last week':(i+1)+' weeks ago');""",
  "    var wlabel = i===0?" + tr("This week") + ":(i===1?" + tr("Last week") + ":" + tr("{n} weeks ago") + ".replace('{n}', i+1));", tag="J11-wlabel")
html = rep(html, """  var bdView = bdRows + '<div class="os-dg-label">weekly breakdown</div>';""",
  "  var bdView = bdRows + '<div class=\"os-dg-label\">'+" + tr("weekly breakdown") + "+'</div>';", tag="J11-bd-label")
html = rep(html, """data-view="bars">Bars</button>""", "data-view=\"bars\">'+" + tr("Bars") + "+'</button>", tag="J11-tab-bars")
html = rep(html, """data-view="flow">Flow</button>""", "data-view=\"flow\">'+" + tr("Flow") + "+'</button>", tag="J11-tab-flow")
html = rep(html, """data-view="trend">Trend</button>""", "data-view=\"trend\">'+" + tr("Trend") + "+'</button>", tag="J11-tab-trend")
html = rep(html, """data-view="breakdown">Breakdown</button>""", "data-view=\"breakdown\">'+" + tr("Breakdown") + "+'</button>", tag="J11-tab-breakdown")

# ---------- J12: My World rows, dashboard ctx, dashboard re-renderer ----------
html = rep(html, """<span>'+esc(p.label)+'</span></button>'""",
  "<span>'+esc((window.mwTr?window.mwTr(p.label):p.label))+'</span></button>'", tag="J12-myworld-label")
html = rep(html, """title="Open '+esc(p.label)+'&rsquo;s dashboard" aria-label="Open '+esc(p.label)+'&rsquo;s dashboard">📊</button></div>';""",
  "title=\"'+esc((window.mwTr?window.mwTr('Open {name}’s dashboard'):'Open {name}’s dashboard').split('{name}').join(p.label))+'\" aria-label=\"'+esc((window.mwTr?window.mwTr('Open {name}’s dashboard'):'Open {name}’s dashboard').split('{name}').join(p.label))+'\">📊</button></div>';", tag="J12-myworld-stat")
html = rep(html, """  if(note) note.textContent=shown<5?'Some pages are hidden — turn them back on in Settings, My World.':'';
}
function mwOpenPageDashboard(key){""",
  "  if(note) note.textContent=shown<5?" + tr("Some pages are hidden — turn them back on in Settings, My World.") + ":'';\n}\nwindow.mwRenderMyWorld=mwRenderMyWorld;\nfunction mwOpenPageDashboard(key){", tag="J12-myworld-note")
# mwOpenPageDashboard ctx: the template (curly ’) also fixes the pre-existing
# literal-&rsquo; display bug — textContent was rendering "&rsquo;" on screen.
html = rep(html, """  if(ctx){ ctx.style.display=''; ctx.querySelector('span').textContent='Dashboard for '+p.label+' — your world&rsquo;s numbers, with '+p.label+'&rsquo;s card lit.'; }""",
  "  if(ctx){ ctx.style.display=''; window._mwDashCtxKey=p; ctx.querySelector('span').textContent=(window.mwTr?window.mwTr('Dashboard for {name} — your world’s numbers, with {name}’s card lit.'):'Dashboard for {name} — your world’s numbers, with {name}’s card lit.').split('{name}').join(p.label); }\nwindow.mwSyncDashCtx=function(){ var p=window._mwDashCtxKey; if(!p) return; var ctx=$('mwDashCtx'); if(ctx && ctx.style.display!=='none'){ ctx.querySelector('span').textContent=(window.mwTr?window.mwTr('Dashboard for {name} — your world’s numbers, with {name}’s card lit.'):'Dashboard for {name} — your world’s numbers, with {name}’s card lit.').split('{name}').join(p.label); } };", tag="J12-dashctx")
# osRerenderDashboard: re-run the pure dashboard renderers from the cached
# load (no refetch); if nothing loaded yet, load once.
html = rep(html, """  window.osLoadDashboard = loadDashboard;""",
  """  window.osLoadDashboard = loadDashboard;
  window.osRerenderDashboard=function(){
    try{
      if(!dashCache){ if(typeof loadDashboard==='function') loadDashboard(); return; }
      var d=dashCache;
      renderPulse(d); renderMyWorld(d); renderHighlightBar(d, window._persLinkStats||[]);
      renderSparks(d); renderWeekFront(d); renderFunnelFront(d.invRows, window._persLinkStats||[]);
      renderDonutFront(d.postTimes.length, d.msgTimes.length, d.invTimes.length);
      renderFacesFront(d); renderInsights(d); renderConvos(d); renderHeat(d);
      if(window._dashLinkArgs) renderLinks(window._dashLinkArgs[0], window._dashLinkArgs[1], window._dashLinkArgs[2], window._dashLinkArgs[3]);
      renderPluginsNative(d);
      if(window.osLoadPointsBoard) window.osLoadPointsBoard();
    }catch(e){}
  };""", tag="J12-rerender")

# ---------- verification + output ----------
m1 = re.search(r"var MW_I18N\s*=\s*(\{.*?\});", html, re.S)
d1 = json.loads(m1.group(1))
assert d1 == d, "embedded MW_I18N != grown dict"
for _attr in ("data-mw-tr", "data-mw-ph", "data-mw-aria", "data-mw-title"):
    print(f"{_attr}: base {html0.count(_attr)} -> new {html.count(_attr)}", file=sys.stderr)
print(f"mwTr guard uses: base {html0.count('window.mwTr?')} -> new {html.count('window.mwTr?')}", file=sys.stderr)
print(f"mwLocale uses: new {html.count('window.mwLocale?')}", file=sys.stderr)
if failures:
    print(f"FAILURES ({len(failures)}):", file=sys.stderr)
    for _f in failures:
        print("  -", _f, file=sys.stderr)
    sys.exit(1)
print(f"OK sha256={hashlib.sha256(html.encode('utf-8')).hexdigest()} bytes={len(html.encode('utf-8'))} lines={html.count(chr(10))+1}", file=sys.stderr)
sys.stdout.write(html)






