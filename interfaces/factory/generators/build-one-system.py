#!/usr/bin/env python3
"""ONE-SYSTEM CURE — transform the flagship templates from two stacked
systems (fm-* layer over the legacy page) into ONE app: the page's own
cover + identity head lead, named blocks (data-block) shown one at a time
behind the page's own navigation, twin-plus as the only plus system,
install + profile picture inside the Settings block only.

Sources (single source of truth, also copied to factory-models/src/):
  cure/os-head.html    install-prompt capture (renamed, UI-free)
  cure/os-style.html   block + twin-plus CSS (geometry harvested from fm)
  cure/os-chrome.html  rooms-plus / eco-plus / drawer / eco-menu (Hub verbatim)
  cure/os-blocks.html  named blocks in ph-* grammar
  cure/os-script.html  the flagship engine, logic verbatim, os-* names

Every step asserts; a failed assert aborts before any file is written.
"""
import hashlib
import json
import os
import re
import subprocess
import sys

HERE = "/home/hatch/workspace/factory-models"
CURE = os.path.join(HERE, "cure")
PIPE = "/home/hatch/workspace/factory-pipeline"
TPL = os.path.join(PIPE, "templates")
BACKUP = os.path.join(HERE, "backup")

MODEL_LINE = {
    "personal": "Smart Personal flagship &mdash; one app, named blocks, one navigation.",
    "business": "Smart Business flagship &mdash; one app, named blocks, one navigation.",
    "community": "Smart Space flagship &mdash; one app, named blocks, one navigation.",
}
NAV_TABS = """<button class="ph-navtab on" style="--tc:#a06bff;" data-view="home" type="button"><span class="os-jewel os-jewel-sm" style="--jc:#a06bff">🏠</span> Home</button>
  <button class="ph-navtab" style="--tc:#3fb8ff;" data-view="dashboard" type="button"><span class="os-jewel os-jewel-sm" style="--jc:#3fb8ff">🌐</span> Dashboard</button>
  <button class="ph-navtab" style="--tc:#2fe89e;" data-view="about" type="button"><span class="os-jewel os-jewel-sm" style="--jc:#2fe89e">👋</span> About</button>
  <button class="ph-navtab" style="--tc:#ffbf3d;" data-view="today" type="button"><span class="os-jewel os-jewel-sm" style="--jc:#ffbf3d">☀️</span> Today</button>
  <button class="ph-navtab" style="--tc:#ff9a5a;" data-view="notes" type="button"><span class="os-jewel os-jewel-sm" style="--jc:#ff9a5a">📡</span> Smart Notes</button>
  <button class="ph-navtab" style="--tc:#ff5e6c;" data-view="people" type="button"><span class="os-jewel os-jewel-sm" style="--jc:#ff5e6c">👥</span> Connections</button>
  <button class="ph-navtab" style="--tc:#e84fff;" data-view="message" type="button"><span class="os-jewel os-jewel-sm" style="--jc:#e84fff">✉️</span> Message</button>
  <button class="ph-navtab" style="--tc:#a06bff;" data-view="inbox" type="button"><span class="os-jewel os-jewel-sm" style="--jc:#a06bff">📥</span> Inbox</button>
  <button class="ph-navtab" style="--tc:#3fb8ff;" data-view="growth" type="button"><span class="os-jewel os-jewel-sm" style="--jc:#3fb8ff">🌱</span> Growth</button>
  <button class="ph-navtab" style="--tc:#2fe89e;" data-view="lists" type="button"><span class="os-jewel os-jewel-sm" style="--jc:#2fe89e">📋</span> Lists</button>
  <button class="ph-navtab" style="--tc:#ff9a5a;" data-view="reports" type="button"><span class="os-jewel os-jewel-sm" style="--jc:#ff9a5a">📊</span> Reports</button>
  <button class="ph-navtab" style="--tc:#ff5e6c;" data-view="settings" type="button"><span class="os-jewel os-jewel-sm" style="--jc:#ff5e6c">⚙️</span> Settings</button>
"""


def load(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def block(name):
    src = load(os.path.join(CURE, "os-blocks.html"))
    m = re.search(r"<!--BLOCK:%s-->\n(.*?)\n<!--/BLOCK-->" % re.escape(name), src, re.S)
    assert m, f"block {name} not found"
    return m.group(1)


SRCDIR = os.path.join(HERE, "src")


def dashblock(name):
    """The Dashboard door layer's blocks live in src/dash-blocks.html
    (the door layer is kept apart from the os-* body sources)."""
    src = load(os.path.join(SRCDIR, "dash-blocks.html"))
    m = re.search(r"<!--BLOCK:%s-->\n(.*?)\n<!--/BLOCK-->" % re.escape(name), src, re.S)
    assert m, f"dash block {name} not found"
    return m.group(1)


def rep(html, old, new, n=1, what=""):
    c = html.count(old)
    assert c == n, f"{what}: expected {n} occurrence(s), found {c}: {old[:80]!r}"
    return html.replace(old, new)


def js_check(html, label):
    """Syntax-check every inline script block with node."""
    blocks = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", html, re.S)
    for i, b in enumerate(blocks):
        if not b.strip():
            continue
        p = f"/tmp/oscheck-{label}-{i}.js"
        with open(p, "w", encoding="utf-8") as f:
            f.write(b)
        r = subprocess.run(["node", "--check", p], capture_output=True, text=True)
        assert r.returncode == 0, f"{label} script {i} syntax: {r.stderr[:400]}"
    return len(blocks)


def css_check(html, label):
    sys.path.insert(0, PIPE)
    import importlib
    import deploy as deploy_mod
    importlib.reload(deploy_mod)
    assert deploy_mod.css_brace_check(html, label), f"{label}: CSS brace gate failed"


def cure_personal(html):
    # ── 1. head: swap the fm install-capture for the renamed os capture ──
    i0 = html.find('<link rel="manifest" href="/manifest.json">')
    assert i0 > 0
    i1 = html.find("</script>", i0) + len("</script>")
    html = html[:i0] + load(os.path.join(CURE, "os-head.html")).rstrip("\n") + html[i1:]

    # ── 2. remove the whole fm span (style + root + script) ──
    s0 = html.find('<style id="fm-style">')
    s1 = html.find('<script id="fm-script">')
    s2 = html.find("</script>", s1) + len("</script>")
    assert 0 < s0 < s1 < s2
    span = html[s0:s2]
    for probe in ('id="fm-root"', 'id="fm-view-home"', 'fmAnnounce'):
        assert probe in span, probe
    html = html[:s0] + html[s2:]

    # ── 3. os style + chrome go where the fm layer sat: first in body ──
    # (the Dashboard door layer's style rides with the body style — every
    #  flagship carries its dashboard behind the Home button)
    html = (html[:s0] + load(os.path.join(CURE, "os-style.html")).rstrip("\n")
            + "\n" + load(os.path.join(SRCDIR, "dash-style.html")).rstrip("\n")
            + "\n" + load(os.path.join(CURE, "os-chrome.html")).rstrip("\n")
            + html[s0:])

    # ── 4. remove the legacy single-plus (twin-plus is the one plus system) ──
    p0 = html.find('<button class="ph-plus" id="plusbtn"')
    p1 = html.find('<div class="ph-head">')
    assert 0 < p0 < p1 and 'id="plusmenu"' in html[p0:p1]
    html = html[:p0] + html[p1:]

    # ── 5. hero: cover + identity head become the Home block's head ──
    html = rep(html, '<div class="ph-cover" id="cvr">',
               '<div class="os-view on" data-os-view="home" data-block="cover">\n'
               '<div class="ph-cover" id="cvr">', 1, "cover wrap open")
    # EYE ROUND 2 (2026-10-22): the hero action row is RETIRED — it
    # duplicated the Smart Tabs below it (one home per action). The
    # cover view now closes directly onto the navwrap, so the tabs sit
    # level with the cover's bottom edge. Invite a friend, the row's
    # one tab-less action, lives in NAV_TABS now.
    html = rep(html, '<div class="ph-navwrap">',
               "</div>\n<div class=\"ph-navwrap\">",
               1, "cover view close (action row retired, EYE ROUND 2)")

    # ── 6. msgbtn becomes a door to the Message block ──
    html = rep(html, '<button class="ph-msg" id="msgbtn" type="button" style="display:none;">',
               '<button class="ph-msg" id="msgbtn" type="button" style="display:none;" data-os-go="message">',
               1, "msgbtn door")

    # ── 7. navtabs: the page's own nav becomes the block router ──
    n0 = html.find('<div class="ph-navtabs" id="navtabs">')
    assert n0 > 0
    n1 = html.find("</div>", n0)
    html = html[:n0] + '<div class="ph-navtabs" id="navtabs">\n  ' + NAV_TABS.rstrip("\n") + "\n" + html[n1:]

    # ── 7b. EYE ROUND 3 STEER (2026-10-22 21:19Z, Shawn's word): the
    #        header order is ONE ROW, then the cover flush under it.
    #        The single tab row leads the page; the cover view follows
    #        with nothing between them — no black gap, nothing
    #        floating. (The row is sticky, so at rest it sits at the
    #        very top with the cover directly beneath it.)
    _nv0 = html.find('<div class="ph-navwrap">')
    _nv1 = html.find('<div class="ph-main">')
    assert 0 < _nv0 < _nv1, "navwrap span not found"
    _navblock = html[_nv0:_nv1]
    html = html[:_nv0] + html[_nv1:]
    _cv0 = html.find('<div class="os-view on" data-os-view="home" data-block="cover">')
    assert _cv0 > 0, "cover view open not found"
    html = html[:_cv0] + _navblock + html[_cv0:]

    # ── 7c. EYE ROUND 3 STEER: "Change picture" as words is dead — a
    #        small camera button rides the avatar's own corner. The
    #        wrap keeps it OUTSIDE the avatar's overflow:hidden, so a
    #        photo change (which rewrites the avatar's innerHTML) can
    #        never wipe it. Its wiring is by id (#avedit → the file
    #        input) and survives the swap; tapping the picture itself
    #        still opens the editor too (Settings law).
    html = rep(html, '<div><span class="ph-edit" id="avedit">Change picture</span></div>\n',
               '', 1, "change-picture words retired (round 3 steer)")
    html = rep(html,
               '<div class="ph-av" id="avv">✦<input type="file" id="avin" accept="image/*" style="display:none;"></div>',
               '<div class="ph-avwrap"><div class="ph-av" id="avv">✦<input type="file" id="avin" accept="image/*" style="display:none;"></div><button class="ph-av-edit" id="avedit" type="button" aria-label="Change picture" title="Edit photo">📷</button></div>',
               1, "avatar corner camera button (round 3 steer)")

    # ── 8. .ph-main section surgery, chunk-wise on ph-sec boundaries ──
    m0 = html.find('<div class="ph-main">')
    assert m0 > 0
    mend = html.find('\n<div class="ph-bottom">', m0)
    assert mend > 0
    inner = html[m0 + len('<div class="ph-main">'):mend]
    assert inner.rstrip().endswith("</div>"), "main inner tail"
    inner = inner.rstrip()
    inner = inner[: -len("</div>")]  # .ph-main's own close
    parts = re.split(r'(?=<div class="ph-sec")', inner)
    head_ws, chunks = parts[0], {}
    for ch in parts[1:]:
        m = re.search(r'id="(\w+)"', ch)
        assert m, ch[:80]
        chunks[m.group(1)] = ch
    assert set(chunks) == {"about", "today", "feed", "people", "lists", "mail", "settings"}, set(chunks)

    def tag(chunk, view, blk):
        return chunk.replace('<div class="ph-sec"',
                             f'<div class="ph-sec os-view" data-os-view="{view}" data-block="{blk}"', 1)

    # INTERROGATION CURE (2026-10-22): the legacy about/feed/people/lists/
    # settings chunks were fixtures and theater (baked notes, ghost people,
    # dead lists, text-pill toggles). They are replaced wholesale by the
    # cured os blocks; the mail chunk was already dropped in batch 1.
    new_inner = (head_ws + block("wall") + "\n\n" + dashblock("dashboard-view") + "\n\n"
                 + block("about") + block("today") + "\n\n"
                 + block("notes") + block("connections") + block("lists") + "\n\n"
                 + block("message") + "\n\n" + block("inbox")
                 + "\n\n" + block("growth") + "\n\n" + block("reports") + "\n\n"
                 + block("settings").replace("__MODEL_LINE__", MODEL_LINE["personal"]))
    html = html[: m0 + len('<div class="ph-main">')] + new_inner + "</div>" + html[mend:]

    # ── 9. legacy behavior script: two surgical guards ──
    html = rep(html,
               "pb.addEventListener('click',function(e){e.stopPropagation();pm.classList.toggle('open');});",
               "if(pb&&pm){pb.addEventListener('click',function(e){e.stopPropagation();pm.classList.toggle('open');});}",
               1, "plus guard")
    html = rep(html,
               "document.addEventListener('click',function(){pm.classList.remove('open');});",
               "document.addEventListener('click',function(){if(pm)pm.classList.remove('open');});",
               1, "plus doc guard")
    html = rep(html,
               "onNavigate:function(u){var t=document.querySelector(u);if(t)t.scrollIntoView({behavior:'smooth'});}",
               "onNavigate:function(u){var map={'#today':'today','#feed':'notes','#people':'people','#lists':'lists','#library':'about','#mail':'inbox','#connections':'people','#reports':'reports','#settings':'settings','#about':'about','#growth':'growth','#message':'message','#dashboard':'dashboard','#home':'home'};if(window.osShowView&&map[u]){window.osShowView(map[u]);return;}var ext={'#ledger':'https://nayanet.live/#/hub/ledger','#spaces':'https://nayanet.live/#/hub/spaces','#connect':'https://nayanet.live/#/hub/connect'};if(ext[u]){window.open(ext[u],'_blank');return;}var t=document.querySelector(u);if(t)t.scrollIntoView({behavior:'smooth'});}",
               1, "smarttabs route via the one navigation")
    # Smart Tabs seed labels speak the one vocabulary (#25): Smart Notes,
    # Connections — and no phantom "Feed"/"People" view names.
    html = rep(html,
               "tabs:[{id:'t1',label:'Today',url:'#today'},{id:'t2',label:'Feed',url:'#feed'},{id:'t3',label:'People',url:'#people'},{id:'t4',label:'Lists',url:'#lists'}]",
               "tabs:[{id:'t1',label:'Today',url:'#today'},{id:'t2',label:'Smart Notes',url:'#feed'},{id:'t3',label:'Connections',url:'#people'},{id:'t4',label:'Lists',url:'#lists'}]",
               1, "smarttabs seed vocabulary")
    # #16: the unexplained "0 pts" pill leaves the cover — nothing on this
    # page awards points, so nothing may claim them.
    html = rep(html,
               """      <div class="ph-points" id="pointsdisplay" title="Your Naya points">
        <span class="ph-points-star">✦</span>
        <span id="pointscount">0</span>
        <span class="ph-points-label">pts</span>
      </div>
""",
               "",
               1, "points pill removed")
    # #31: Connect writes a REAL connection — a connect row on the page's
    # own store, through the engine — and only then claims "Connected".
    html = rep(html,
               """  var cb=document.getElementById('connectbtn');
  cb.addEventListener('click',function(){
    var c=cb.classList.toggle('connected');cb.textContent=c?'✓ Connected':'Connect';
    document.getElementById('msgbtn').style.display=c?'':'none';});""",
               """  var cb=document.getElementById('connectbtn');
  cb.addEventListener('click',function(){
    if(cb.dataset.osConnected){document.getElementById('msgbtn').style.display='';return;}
    cb.textContent='Connecting…';
    document.dispatchEvent(new CustomEvent('os-connect-request'));
  });
  document.addEventListener('os-connect-done',function(){
    cb.dataset.osConnected='1';cb.classList.add('connected');cb.textContent='✓ Connected';
    document.getElementById('msgbtn').style.display='';
  });
  document.addEventListener('os-connect-failed',function(){ if(!cb.dataset.osConnected) cb.textContent='Connect'; });
  try{ if(localStorage.getItem('os.connected')==='1'){ cb.dataset.osConnected='1'; cb.classList.add('connected'); cb.textContent='✓ Connected'; document.getElementById('msgbtn').style.display=''; } }catch(e){}""",
               1, "connect writes a real connection")
    # The legacy settings-toggle script claims every '#settings .ph-msg' as a
    # labeled toggle row; the Settings block now also carries action buttons
    # (photo / page doors) whose rows have no <span> label — guard it so it
    # only wires the toggle rows it was written for.
    html = rep(html,
               "var label = btn.parentElement.querySelector('span').textContent;",
               "var sp = btn.parentElement.querySelector('span'); if(!sp) return; var label = sp.textContent;",
               1, "settings toggle guard")

    # ── 10. the engine, last in body (app engine + the dashboard door
    #        layer's engine, one alias, one data path) ──
    engine = (load(os.path.join(CURE, "os-script.html")).replace("__ALIAS__", "flagship-personal")
              + "\n" + load(os.path.join(SRCDIR, "dash-script.html")).replace("__ALIAS__", "flagship-personal"))
    assert html.rstrip().endswith("</html>")
    b = html.rfind("</body>")
    html = html[:b] + engine.rstrip("\n") + "\n" + html[b:]
    # ── 12. Account card copy (EYE ROUND 2d ruling, 2026-10-22): the
    # "unlock" sentence becomes Shawn's plain framing. The base auth
    # script's mechanics (Supabase, prompts, signed-in state) stay
    # byte-identical — this is copy only. The card's ⓘ explainer is an
    # os-layer pattern (os-info-btn/os-info-panel), injected by os-script
    # when the auth script creates the card.
    html = rep(html, "Sign in to unlock intelligence features.",
               "Sign in so NayaNET knows it\u2019s you \u2014 your apps, your mail and your data, synced on every device.",
               1, "account card copy (round 2d)")
    # ── 13. EYE ROUND 3 (2026-10-22): the theme row is "Deep black",
    # never "Dark mode" (Shawn's word). The label lives in os-blocks
    # (renamed at the source); the legacy settings script finds its
    # row by matching that label text, so the matcher follows. The
    # stored preference KEY ('🌙 Dark mode' in os-script) is device
    # data, not copy — it stays, or existing devices lose the pref.
    html = rep(html, "label.includes('Dark mode')", "label.includes('Deep black')",
               1, "deep black label match (round 3)")

    # ── 14. ELEVATION (2026-10-23): Quick Capture files under THIS
    #        page's own alias — the one the Settings label carries —
    #        never a hardcoded person's name. Rows already filed under
    #        the old name stay where they are; the fix is forward-only.
    # ── WAVE 1 (2026-10-23, full sweep): the legacy Quick Capture IIFE
    #        itself is DELETED from the base — its DOM hooks
    #        (#captureinput/#capturebtn) never existed in the one-system
    #        shell, so it early-returned on every load (dead code,
    #        −4.6 KB ×4 pages). The live capture path is the Notes
    #        view's Quick Capture card (#os-note-capture). The
    #        elevation alias cure above is retired with the code it
    #        cured; this step now guards the deletion.
    assert 'captureinput' not in html and 'capturebtn' not in html, \
        "wave 1: legacy Quick Capture IIFE must stay deleted"

    return html


def verify(html, label, alias, other_idents):
    errs = []
    def chk(cond, msg):
        if not cond:
            errs.append(msg)
    for bad in ("fm-root", "fm-topbar", "fm-hero", "fm-view-", "fm-tabbar",
                "fm-drawer", "fm-script", "fm-style", "fmShowView", "fmAnnounce",
                "__fmInstallPrompt", 'id="plusbtn"', 'id="plusmenu"',
                "hub_smart_notes",
                # FRONT CURE (2026-10-22): the retired banners never return
                'id="os-dash-hero"', 'id="os-dash-gauge"', 'id="os-dash-orb"',
                'id="os-dash-world"', 'id="os-dash-health-note"',
                'id="os-dash-spotlight"', 'id="os-dash-life"',
                "healthScore", "renderGauge", "renderSpotlight", "renderLife",
                # INTERROGATION CURE (2026-10-22): the fixtures and theater never return
                "Your Circle", "pointsdisplay", 'id="feedgrid"', 'id="peoplegrid"',
                'id="capturebtn"', "Naya writes it", "stage('Opened'",
                "Opened and Joined honestly read 0",
                # EYE-PASS CURE (2026-10-22): the retired cover band, the
                # Today pill and the facts shortcut row never return
                "Dashboard &middot; Your World, Live", "ALSO ON YOUR DASHBOARD",
                "Meet them", "See the people",
                "Sign in to unlock intelligence features"):
        chk(bad not in html, f"{label}: forbidden string present: {bad}")

    # EYE-PASS CURE scope note: #40d3bb / #6675ff may survive ONLY inside
    # the base template's verbatim Law-9 token contexts — the PALETTE
    # array + tabColor() (the Hub ribbon's per-room identity tokens,
    # identical on the Hub itself), the unused --sapphire token
    # definition, and the never-rendered .spectrum-bar fossil CSS.
    # Everywhere else — every flagship surface — they are retired.
    for hexv in ("#40d3bb", "#6675ff"):
        for ln in html.split("\n"):
            if hexv in ln:
                chk("PALETTE" in ln or "tabColor" in ln or "--sapphire" in ln or ".spectrum-bar" in ln,
                    f"{label}: off-walk hex {hexv} outside base token contexts: {ln[:80]}")
    fm_hits = [m.start() for m in re.finditer(r"fm-", html)]
    allowed = html.count("[[fm-auto]]")
    chk(len(fm_hits) == allowed, f"{label}: fm- hits {len(fm_hits)} != allowed stored-data tokens {allowed}")
    chk(html.count("fm.photo") == 1, f"{label}: fm.photo legacy-read fallback must appear exactly once")
    chk(html.count('data-block="cover"') == 1, f"{label}: cover block count")
    chk(html.find('data-block="cover"') < html.find('id="os-wall"'), f"{label}: cover must lead")
    chk(html.find('<div class="ph-cover"') < html.find('<div class="ph-main">'), f"{label}: cover before main")
    chk(html.count('os-view on') == 2,
        f"{label}: exactly hero+wall start open, got {html.count('os-view on')}")
    # install UI only inside the Settings block
    s0 = html.find('data-block="settings"')
    for probe in ('id="os-install-btn"', 'id="os-install-state"', "Install as app"):
        chk(html.find(probe) > s0, f"{label}: {probe} not inside Settings block")
    chk(html.count("rooms-plus") >= 3 and html.count('id="os-rooms-plus"') == 1, f"{label}: rooms-plus system")
    chk(html.count('id="os-eco-plus"') == 1 and html.count('id="os-eco-menu"') == 1, f"{label}: eco-plus system")
    chk("width:48px;height:48px" in html, f"{label}: 48px plus rule")
    for probe in ("smart_mail_threads", "smart_mail_messages", "invitee_email_hash",
                  "crypto.subtle", "beforeinstallprompt", PAGE := alias):
        chk(probe in html, f"{label}: missing {probe}")
    # EYE-PASS CURE (2026-10-22): the new laws ride in the artifact
    for probe in ("osOrbFlow", "osNavDrift", "osIgnite", "--igc",
                  'id="os-sec-about-text"', 'id="os-sec-goals-text"',
                  'id="os-sec-motto-text"', "data-os-sec-save",
                  "k:'aboutsec'"):
        chk(probe in html, f"{label}: missing eye-pass piece {probe}")
    # EYE ROUND 2 (2026-10-22): no duplicated navigation — the hero
    # action row never returns; Invite a friend rides the tab bar; the
    # cover displays whole with the identity overlaid at its bottom;
    # the Message fields carry dictation and the box auto-grows.
    chk("os-dash-btn" not in html, f"{label}: retired action-row button class present")
    chk('<div class="ph-actions" style="padding:0 24px;margin-top:18px;">' not in html,
        f"{label}: retired hero action row present")
    _n0 = html.find('<div class="ph-navtabs" id="navtabs">')
    _n1 = html.find("</div>", _n0)
    _nav = html[_n0:_n1] if _n0 > 0 else ""
    _tcs = re.findall(r'--tc:(#[0-9a-f]{6})', _nav)
    _walk = ["#a06bff", "#3fb8ff", "#2fe89e", "#ffbf3d",
             "#ff9a5a", "#ff5e6c", "#e84fff"]
    chk(len(_tcs) == 13 and all(c == _walk[i % 7] for i, c in enumerate(_tcs)),
        f"{label}: navtab walk by position broken ({len(_tcs)} tabs: {_tcs})")
    chk('data-view="growth"' in _nav and "Invite a friend" not in _nav,
        f"{label}: duplicate Invite door back in the tab bar (Growth keeps the only one)")
    chk("Invite a friend" in html,
        f"{label}: Growth lost its Invite a friend card")
    for probe in ("os-fieldwrap", "data-os-mic", "SpeechRecognition",
                  "osAutoGrow", "osDictate", "osMicPulse",
                  ".ph-cover:has(>img)", '[data-block=cover] .ph-head'):
        chk(probe in html, f"{label}: missing round-2 piece {probe}")
    chk(html.count('data-os-mic="') == 13, f"{label}: exactly thirteen dictation buttons (3 message + 8 about + 0 smart link + 2 naya notes — the claim card is typed, per the claim-copy cure)")
    for probe in ("Sign in so NayaNET knows it", "os-info-btn", "os-info-panel",
                  "Your email is your key."):
        chk(probe in html, f"{label}: missing round-2d account piece {probe}")
    # EYE ROUND 3 (2026-10-22): the settings block once lost its
    # <!--/BLOCK--> terminator, so block("settings") swallowed the
    # notes block whole — every flagship shipped the Smart Notes view
    # TWICE (duplicate ids throughout) and the Data & privacy card
    # lost its opening lines. These guards make that class of loss a
    # build failure, forever:
    chk(html.count('id="feed"') == 1, f"{label}: notes view duplicated (settings terminator?)")
    chk(html.count('data-block="smart-notes"') == 1, f"{label}: smart-notes block duplicated")
    chk("<!--BLOCK" not in html and "<!--/BLOCK-->" not in html,
        f"{label}: block delimiter leaked into the artifact")
    _ids3 = re.findall(r'id="([\w-]+)"', html)
    _dupes3 = sorted({i for i in _ids3 if _ids3.count(i) > 1})
    chk(not _dupes3, f"{label}: duplicate ids {_dupes3}")
    chk('<span class="os-jewel os-jewel-h" style="--jc:#2fe89e">🔒</span> Data &amp; privacy' in html,
        f"{label}: Data & privacy card opening lost")
    # ELEVATION (2026-10-23): the duplicate Invite tab is retired —
    # Growth's card is the one Invite door; the theme row speaks
    # Shawn's words — Deep black.
    chk(len(re.findall(r'data-os-invite="1"', _nav)) == 0,
        f"{label}: Invite a friend action tab returned to the tab bar")
    chk("<b>Deep black</b>" in html and "<b>Dark mode</b>" not in html,
        f"{label}: Deep black rename missing")
    chk("label.includes('Deep black')" in html and "label.includes('Dark mode')" not in html,
        f"{label}: legacy deep-black label match missing")
    chk("setStatus('Deep black is '" in html, f"{label}: deep-black status copy missing")
    # EYE ROUND 3 STEER (21:19Z): one row leads, the cover sits flush
    # under it; the picture's editor is a camera button on its corner.
    chk(html.find('<div class="ph-navwrap">') < html.find('data-block="cover"'),
        f"{label}: the one tab row must lead the header (round-3 steer)")
    chk('class="ph-av-edit"' in html and '>Change picture</span>' not in html,
        f"{label}: avatar corner camera button missing / words survived")
    # EYE ROUND 3 STEER 2 (Phi's round-2 scorecard, 8.5/10): cover
    # geometry named in the bytes, auto-grow on every composer,
    # inherited "this page" copy cured to app language.
    chk("aspect-ratio:16/9" in html,
        f"{label}: cover geometry — the 16:9 (1.7778) proportion rule missing")
    chk("['os-post-body', 'os-lib-na']" in html,
        f"{label}: auto-grow — wall composer + Library answer box not wired")
    for bad in ("this page is live", "in this page’s library", "On this page since",
                "connected to this page", "on this page, with the time",
                "kept on this device, on this page", "txt:'Around this page'",
                "in this page’s Smart Mail inbox"):
        chk(bad not in html, f"{label}: app-language copy — {bad!r} survived")
    # Steer 3+4 (21:51Z / 21:53Z): the band is capped, the focal point
    # drags and persists, and dictation errors speak.
    chk("aspect-ratio:16/9;max-height:360px" in html,
        f"{label}: cover band — 16:9 with the 360px cap missing")
    chk("fm.coverPos" in html and "os-dragging" in html,
        f"{label}: cover focal drag / persistence missing")
    chk("Dictation needs microphone access" in html and "os-mic-note" in html
        and "Listening… speak now" in html,
        f"{label}: dictation must speak — guidance or Listening note missing")
    # EYE ROUND 2c/2d: About order + pronoun grammar ride in the artifact;
    # the Settings picture card never returns; install speaks smart-app.
    for gone in ('id="os-photo-btn"', 'id="os-photo-img"', 'id="os-photo-input"',
                 '> Profile picture</h3>', "Install this page", "Message this page",
                 "Page behaviour", 'data-room-install'):
        chk(gone not in html, f"{label}: retired round-2 string present: {gone}")
    for probe in ("Install this app", "Put this app on your home screen",
                  "App behaviour", "Message this app"):
        chk(probe in html, f"{label}: missing round-2 piece {probe}")
    def _tpos(*forms):
        ps = [html.find(f) for f in forms]
        ps = [p for p in ps if p >= 0]
        return min(ps) if ps else -1
    _ord2 = [_tpos("</span> My motto</h3>", "</span> Our motto</h3>"),
             _tpos("</span> My story</h3>", "</span> Our story</h3>"),
             _tpos("</span> My goals</h3>", "</span> Our goals</h3>"),
             _tpos("</span> My mission</h3>", "</span> Our mission</h3>"),
             _tpos("</span> My vision</h3>", "</span> Our vision</h3>"),
             _tpos("</span> My facts</h3>", "</span> Our facts</h3>")]
    chk(all(v > 0 for v in _ord2) and _ord2 == sorted(_ord2),
        f"{label}: About order broken (motto, story, goals, mission, vision, facts-last): {_ord2}")
    for probe in ('id="os-msg-btn"', 'id="os-inbox-list"', 'id="os-inv-btn"',
                  'id="os-rep-posts"', 'id="os-post-btn"',
                  'id="os-wall-list"', 'id="os-today-list"'):
        chk(probe in html, f"{label}: missing block piece {probe}")
    # ten-star pass: the living Reports dashboard + provably-moving tabs
    for probe in ('id="os-rep-donut"', 'id="os-rep-total"', 'id="os-rep-week"',
                  'id="os-rep-week-counts"', 'id="os-rep-week-days"',
                  'id="os-rep-week-note"', 'id="os-rep-posts-note"',
                  'id="os-rep-leg-posts"', 'id="os-rep-leg-people"',
                  'id="os-rep-people"', 'id="os-rep-today"', 'class="os-rcirc"',
                  'class="donut" id="os-rep-donut"',
                  "osTabsDrift", "data-os-clone", "renderWeek", "countUp"):
        chk(probe in html, f"{label}: missing ten-star piece {probe}")
    chk("countEq" not in html, f"{label}: retired naked-count loader still present")
    # living graphics pass (2026-10-22): lit data objects + v3 harvest
    for probe in ('os-well', 'os-skel', 'os-bar-pill', 'os-av-arc', 'os-donut-sheen',
                  'os-insight-gem', 'data-period', 'os-farrow', 'os-fbar-n',
                  'renderSpark',
                  'bucketize', 'renderBars', 'donutSegs', 'flashChange', 'os-changed',
                  'id="os-dash-fb-btn"', 'id="os-dash-fb-body"',
                  # FRONT CURE: icon jewels everywhere + the pick as move #1
                  'os-jewel', 'os-jewel-lg', 'pickMove', 'os-src-num',
                  'os-src-nums', 'osAmbient',
                  'os-xchip', 'sparkfill', 'os-litobj', 'Your next best moves'):
        chk(probe in html, f"{label}: missing living-graphics piece {probe}")
    # batch 2 (ten-star items 3-10): no naked numbers, Today pulse, inhabited
    # wall, invite journey funnel, faces board, conversation inbox, real
    # settings, and the life pass over every block
    for probe in ('id="os-wall-meta"', 'id="os-today-pulse"', 'id="os-inbox-meta"',
                  'id="os-funnel"', 'id="os-faces"', 'id="os-set-status"',
                  'id="os-set-drift"', 'id="os-set-motion"', 'id="os-set-refresh"',
                  'id="os-set-dark"', 'id="publictoggle"', 'class="os-switch',
                  "renderFunnel", "loadFaces", "loadToday", "applyPrivacy",
                  "refreshInboxBadge", "os-calm", "setEnabled", "colorFor",
                  "avatarHTML", "os-fbar", "os-face", "os-thread-new",
                  "PRIVATE_NOTE", "INBOX_SEEN_KEY"):
        chk(probe in html, f"{label}: missing batch-2 piece {probe}")
    for ident in other_idents:
        chk(ident not in html, f"{label}: LEAKAGE of {ident}")
    chk(html.count("--soul:#a06bff") == 1 and html.count("--tone:#a06bff") == 2,
        f"{label}: soul knobs moved")
    chk('<div class="ph-av" id="avv">' in html, f"{label}: #avv slot lost")
    chk(html.count("Alex Morgan") >= 2, f"{label}: base name spots lost")
    chk(".os-input,.os-textarea{" in html, f"{label}: block form grammar lost")
    chk('data-view="settings"' in html and 'data-view="home"' in html, f"{label}: doors missing")
    views = sorted(set(re.findall(r'data-os-view="(\w+)"', html)))
    chk(views == sorted(["home", "dashboard", "about", "today", "notes", "people", "message",
                         "inbox", "growth", "lists", "reports", "settings"]),
        f"{label}: view set {views}")
    # the Dashboard view (steer 2026-10-22 ~03:20Z): a named block of the
    # universal body, summoned by the prominent button on Home, fed by the
    # page's own tables — present in EVERY flagship
    blocks_seen = sorted(set(re.findall(r'data-block="([\w-]+)"', html)))
    chk(blocks_seen == sorted(["cover", "wall", "dashboard", "about", "today", "smart-notes",
                               "connections", "lists", "message", "inbox",
                               "growth", "reports", "settings"]),
        f"{label}: block set {blocks_seen}")
    for probe in ('id="os-dash"', 'id="os-dash-pulse"', 'id="os-dash-week"',
                  'id="os-dash-funnel"', 'id="os-dash-donut"', 'id="os-dash-faces"',
                  'id="os-dash-insights"', 'id="os-dash-convos"', 'id="os-dash-plugins"',
                  'id="os-dash-src-n-people"',
                  "loadDashboard", "buildInsights", "pickMove", "osLoadDashboard",
                  "BORN CONNECTED", 'data-view="dashboard"'):
        chk(probe in html, f"{label}: missing dashboard piece {probe}")
    chk(html.count("NOT CONNECTED") == 4, f"{label}: four honest invitation sources (website, social, AIs, booking)")
    # INTERROGATION CURE (2026-10-22): the cured blocks' working pieces
    for probe in ('id="os-note-capture-btn"', 'id="os-note-list"', 'id="os-note-saved"',
                  'id="os-list-add"', 'id="os-list-rows"', 'id="os-lib-list"',
                  'id="os-inv-share"', 'id="os-inbox-pulse"', 'id="os-today-faces"',
                  'id="os-born"', 'id="os-set-data"', 'id="os-about-facts"',
                  "loadLibrary", "saveQuestion", "loadLists", "loadNotes", "loadAbout",
                  "serviceWorker.register(", "os-dayorbs", "faceTileHTML", "presenceOf",
                  "renderInboxPulse", "os-connect-request", "bindSwitch"):
        chk(probe in html, f"{label}: missing interrogation-cure piece {probe}")
    # FRONT CURE: the front opens with the pulse — stats first, in order
    _ord = [html.find('id="os-dash-pulse"'), html.find('id="os-dash-week"'),
            html.find('id="os-dash-faces"'), html.find('id="os-dash-insights"'),
            html.find('id="os-dash-convos"'), html.find('id="os-dash-plugins"')]
    chk(all(v > 0 for v in _ord) and _ord == sorted(_ord),
        f"{label}: dashboard front order broken {_ord}")
    chk(html.count(alias) == 3, f"{label}: alias x3 (os engine + settings label + dash engine), got {html.count(alias)}")
    chk("OWNER_ALIAS = 'shawn'" not in html and "TODO: make dynamic per user" not in html,
        f"{label}: Quick Capture still files under a hardcoded name")
    nb = js_check(html, label)
    css_check(html, label)
    if errs:
        raise SystemExit("VERIFY FAIL\n" + "\n".join(errs))
    print(f"{label}: verify OK ({nb} script blocks syntax-clean, CSS gate OK, "
          f"{len(html.encode())} bytes)")
    return len(html.encode())


PLURAL_TITLES = [
    ("</span> My motto</h3>", "</span> Our motto</h3>"),
    ("</span> My story</h3>", "</span> Our story</h3>"),
    ("</span> My goals</h3>", "</span> Our goals</h3>"),
    ("</span> My mission</h3>", "</span> Our mission</h3>"),
    ("</span> My vision</h3>", "</span> Our vision</h3>"),
    ("</span> What I love</h3>", "</span> What we love</h3>"),
    ("</span> What I don&rsquo;t</h3>", "</span> What we don&rsquo;t</h3>"),
    ("</span> My facts</h3>", "</span> Our facts</h3>"),
    ("</span> About Me</div>", "</span> About Us</div>"),
]


def derive(cured, model, alias):
    assert cured.count("flagship-personal") == 3, cured.count("flagship-personal")
    out = cured.replace("flagship-personal", alias)
    out = rep(out, MODEL_LINE["personal"], MODEL_LINE[model], 1, "model line")
    if model in ("business", "community"):
        # Shawn's pronoun grammar (round 2c): plural bodies speak "our".
        for mine, ours in PLURAL_TITLES:
            out = rep(out, mine, ours, 1, f"plural title {mine[:40]}")
    return out


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "personal"
    if which == "personal":
        # Input is the pre-cure original (kept in backup/) so the transform
        # stays re-runnable after the cured file has been written.
        orig = os.path.join(BACKUP, "personal.html.pre-onesystem")
        src = load(orig if os.path.exists(orig) else os.path.join(TPL, "personal.html"))
        cured = cure_personal(src)
        n = verify(cured, "personal", "flagship-personal",
                   ["flagship-business", "flagship-community", "Acme Corp", "Our Community"])
        bak = os.path.join(BACKUP, "personal.html.pre-onesystem")
        if not os.path.exists(bak):
            with open(bak, "w", encoding="utf-8") as f:
                f.write(src)
        with open(os.path.join(TPL, "personal.html"), "w", encoding="utf-8") as f:
            f.write(cured)
        with open("/home/hatch/workspace/personal-app/personal-v5.html", "w", encoding="utf-8") as f:
            f.write(cured)
        print(f"personal: wrote templates/personal.html + personal-v5.html ({n} bytes, md5 {hashlib.md5(cured.encode()).hexdigest()})")
    else:
        model = which
        alias = {"business": "flagship-business", "community": "flagship-community"}[model]
        others = {"business": ["flagship-personal", "flagship-community", "Nova Reyes", "Our Community"],
                  "community": ["flagship-personal", "flagship-business", "Nova Reyes", "Acme Corp"]}[model]
        cured = load(os.path.join(TPL, "personal.html"))
        out = derive(cured, model, alias)
        # derived templates bake the base identity (Alex Morgan) like before;
        # the pipeline applies the model identity from the contract.
        n = verify(out, model, alias, others)
        bak = os.path.join(BACKUP, f"{model}.html.pre-onesystem")
        cur = load(os.path.join(TPL, f"{model}.html"))
        if not os.path.exists(bak):
            with open(bak, "w", encoding="utf-8") as f:
                f.write(cur)
        with open(os.path.join(TPL, f"{model}.html"), "w", encoding="utf-8") as f:
            f.write(out)
        print(f"{model}: wrote templates/{model}.html ({n} bytes, md5 {hashlib.md5(out.encode()).hexdigest()})")


if __name__ == "__main__":
    main()
