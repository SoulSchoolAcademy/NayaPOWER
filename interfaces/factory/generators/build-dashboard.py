#!/usr/bin/env python3
"""THE DASHBOARD DOOR (Mirror B5, 2026-10-22, Nu) — a door CONFIGURATION
of the one universal template.

Since the ~03:20Z steer (Shawn's dashboard-button doctrine), the
"Your World, Live" composition is a VIEW of the universal body
(data-block="dashboard", in every flagship, summoned by the Dashboard
button on Home). The Dashboard door is therefore not a different body:
templates/dashboard.html is the SAME generated body as Smart Personal
(same 13 named blocks, same engines, same alias flagship-personal — it
reads Nova Reyes' real tables) with the door configuration applied:
the Dashboard view opens first, Home waits one tap away, and the
Settings model line names the door.

Every step asserts; a failed assert aborts before any file is written.
Backup: backup/dashboard.html.pre-dashview (first-write only).
"""
import hashlib
import json
import os
import re
import subprocess
import sys

HERE = "/home/hatch/workspace/factory-models"
PIPE = "/home/hatch/workspace/factory-pipeline"
TPL = os.path.join(PIPE, "templates")
BACKUP = os.path.join(HERE, "backup")

PERSONAL_LINE = "Smart Personal flagship &mdash; one app, named blocks, one navigation."
DASH_LINE = "The Dashboard door of this app &mdash; one app, many doors. Your world, live."
ALIAS = "flagship-personal"

COVER_ON = '<div class="os-view on" data-os-view="home" data-block="cover">'
COVER_OFF = '<div class="os-view" data-os-view="home" data-block="cover">'
WALL_ON = '<div class="ph-sec os-view on" id="os-wall" data-os-view="home" data-block="wall">'
WALL_OFF = '<div class="ph-sec os-view" id="os-wall" data-os-view="home" data-block="wall">'
DASH_OFF = '<div class="ph-sec os-view" data-os-view="dashboard" data-block="dashboard">'
DASH_ON = '<div class="ph-sec os-view on" data-os-view="dashboard" data-block="dashboard">'
TAB_HOME_ON = '<button class="ph-navtab on" style="--tc:#a06bff;" data-view="home" type="button">'
TAB_HOME_OFF = '<button class="ph-navtab" style="--tc:#a06bff;" data-view="home" type="button">'
TAB_DASH_OFF = '<button class="ph-navtab" style="--tc:#3fb8ff;" data-view="dashboard" type="button">'
TAB_DASH_ON = '<button class="ph-navtab on" style="--tc:#3fb8ff;" data-view="dashboard" type="button">'


def load(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def rep(html, old, new, n=1, what=""):
    c = html.count(old)
    assert c == n, f"{what}: expected {n} occurrence(s), found {c}: {old[:80]!r}"
    return html.replace(old, new)


def js_check(html, label):
    blocks = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", html, re.S)
    for i, b in enumerate(blocks):
        if not b.strip():
            continue
        p = f"/tmp/dashcheck-{label}-{i}.js"
        with open(p, "w", encoding="utf-8") as f:
            f.write(b)
        r = subprocess.run(["node", "--check", p], capture_output=True, text=True)
        assert r.returncode == 0, f"{label} script {i} syntax: {r.stderr[:400]}"
    return len(blocks)


def css_check(html, label):
    sys.path.insert(0, PIPE)
    import deploy as deploy_mod
    assert deploy_mod.css_brace_check(html, label), f"{label}: CSS brace gate failed"


def build(personal_html):
    html = personal_html
    html = rep(html, PERSONAL_LINE, DASH_LINE, 1, "model line")
    # the door configuration: Dashboard opens first; Home one tap away
    html = rep(html, COVER_ON, COVER_OFF, 1, "cover closed at the door")
    html = rep(html, WALL_ON, WALL_OFF, 1, "wall closed at the door")
    html = rep(html, DASH_OFF, DASH_ON, 1, "dashboard open at the door")
    html = rep(html, TAB_HOME_ON, TAB_HOME_OFF, 1, "home tab rests")
    html = rep(html, TAB_DASH_OFF, TAB_DASH_ON, 1, "dashboard tab lit")
    return html


def verify(html, label):
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
                "Your Circle", "pointsdisplay", 'id="feedgrid"', 'id="peoplegrid"',
                "Naya writes it", "stage('Opened'",
                "YOUR WORLD, LIVE",
                # EYE-PASS CURE (2026-10-22): same retirements as the body
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
    chk(len([m for m in re.finditer(r"fm-", html)]) == html.count("[[fm-auto]]") == 3,
        f"{label}: fm- stored-data tokens")
    chk(html.count("fm.photo") == 1, f"{label}: fm.photo fallback exactly once")
    blocks = re.findall(r'data-block="([\w-]+)"', html)
    chk(sorted(set(blocks)) == sorted(["cover", "wall", "dashboard", "about", "today",
                                       "smart-notes", "connections", "lists", "message",
                                       "inbox", "growth", "reports", "settings"]),
        f"{label}: block set {sorted(set(blocks))}")
    chk(blocks[0] == "cover", f"{label}: cover still the first block in the body")
    # door state: exactly ONE view open at load — the dashboard
    chk(html.count('os-view on') == 1, f"{label}: exactly the dashboard view open, got {html.count('os-view on')}")
    chk(DASH_ON in html and COVER_OFF in html and WALL_OFF in html, f"{label}: door open/closed state")
    for probe in ("osOrbFlow", "osNavDrift", "osIgnite", "--igc",
                  'id="os-sec-about-text"', "data-os-sec-save", "k:'aboutsec'"):
        chk(probe in html, f"{label}: missing eye-pass piece {probe}")
    chk(TAB_DASH_ON in html and TAB_HOME_OFF in html, f"{label}: dashboard tab lit, home tab rests")
    w0, d0 = html.find('id="os-wall"'), html.find('id="os-dash"')
    chk(0 < w0 < d0, f"{label}: dashboard view sits after the wall in the one body")
    s0 = html.find('data-block="settings"')
    for probe in ('id="os-install-btn"', 'id="os-install-state"', "Install as app"):
        chk(html.find(probe) > s0, f"{label}: {probe} not inside Settings block")
    chk(html.count('id="os-rooms-plus"') == 1 and html.count('id="os-eco-plus"') == 1
        and html.count('id="os-eco-menu"') == 1, f"{label}: twin-plus system")
    chk("width:48px;height:48px" in html, f"{label}: 48px plus rule")
    for probe in ("smart_mail_threads", "smart_mail_messages", "invitee_email_hash",
                  "crypto.subtle", "beforeinstallprompt"):
        chk(probe in html, f"{label}: missing {probe}")
    chk(html.count(ALIAS) == 3, f"{label}: alias x3, got {html.count(ALIAS)}")
    for probe in ('id="os-msg-btn"', 'id="os-inbox-list"', 'id="os-inv-btn"',
                  'id="os-rep-posts"', 'id="os-post-btn"',
                  'id="os-wall-list"', 'id="os-today-list"',
                  'id="os-rep-donut"', 'id="os-rep-week"', "osTabsDrift", "data-os-clone",
                  "renderWeek", "countUp",
                  'id="os-wall-meta"', 'id="os-today-pulse"', 'id="os-inbox-meta"',
                  'id="os-funnel"', 'id="os-faces"', 'id="os-set-status"',
                  "renderFunnel", "loadFaces", "loadToday", "applyPrivacy",
                  "refreshInboxBadge", "avatarHTML", "PRIVATE_NOTE", "INBOX_SEEN_KEY"):
        chk(probe in html, f"{label}: missing body piece {probe}")
    chk("countEq" not in html, f"{label}: retired naked-count loader still present")
    # EYE ROUND 2: the hero action row + Settings picture card never return
    for gone in ('id="os-photo-btn"', 'id="os-photo-img"', 'data-os-go="dashboard"', "os-dash-btn"):
        chk(gone not in html, f"{label}: retired round-2 piece present: {gone}")
    # EYE ROUND 3: the duplication guards ride the door too (the
    # settings block's lost terminator once shipped the notes view
    # twice in every flagship — see build-one-system.py's note)
    chk(html.count('id="feed"') == 1 and html.count('data-block="smart-notes"') == 1,
        f"{label}: notes view duplicated (settings terminator?)")
    chk("<!--BLOCK" not in html and "<!--/BLOCK-->" not in html,
        f"{label}: block delimiter leaked into the artifact")
    _ids3 = re.findall(r'id="([\w-]+)"', html)
    _dupes3 = sorted({i for i in _ids3 if _ids3.count(i) > 1})
    chk(not _dupes3, f"{label}: duplicate ids {_dupes3}")
    chk("<b>Deep black</b>" in html and "<b>Dark mode</b>" not in html,
        f"{label}: Deep black rename missing")
    chk(html.find('<div class="ph-navwrap">') < html.find('data-block="cover"'),
        f"{label}: the one tab row must lead the header (round-3 steer)")
    chk('class="ph-av-edit"' in html and '>Change picture</span>' not in html,
        f"{label}: avatar corner camera button missing / words survived")
    chk("aspect-ratio:16/9" in html and "['os-post-body', 'os-lib-na']" in html,
        f"{label}: steer 2 — 16:9 cover rule / auto-grow coverage missing")
    for bad in ("this page is live", "in this page’s library", "On this page since",
                "connected to this page", "txt:'Around this page'",
                "in this page’s Smart Mail inbox"):
        chk(bad not in html, f"{label}: app-language copy — {bad!r} survived")
    chk("aspect-ratio:16/9;max-height:min(55vh,600px)" in html and "fm.coverPos" in html
        and "Dictation needs microphone access" in html,
        f"{label}: steer 3+4 — capped band / focal drag / speaking dictation missing")
    for probe in ('id="os-dash"', 'id="os-dash-pulse"', 'id="os-dash-n-posts"', 'id="os-dash-n-messages"',
                  'id="os-dash-n-invites"', 'id="os-dash-n-people"', 'id="os-dash-n-posts-note"',
                  'id="os-dash-n-people-note"', 'id="os-dash-spark-posts"', 'id="os-dash-spark-people"',
                  'id="os-dash-week"', 'id="os-dash-week-counts"', 'id="os-dash-week-days"',
                  'id="os-dash-week-note"', 'id="os-dash-funnel"', 'id="os-dash-donut"',
                  'id="os-dash-total"', 'id="os-dash-leg-posts"', 'id="os-dash-leg-messages"',
                  'id="os-dash-leg-invites"', 'id="os-dash-faces"', 'id="os-dash-faces-head"',
                  'id="os-dash-insights"', 'id="os-dash-convos"', 'id="os-dash-plugins"',
                  'id="os-dash-src-n-people"', 'id="os-dash-minifaces"',
                  'id="os-dash-how-web"', 'id="os-dash-how-social"', 'id="os-dash-how-ai"',
                  "loadDashboard", "buildInsights", "renderInsights", "renderSparks",
                  'id="os-dash-fb-btn"',
                  "bucketize", "donutSegs", "flashChange", "os-skel", "data-period",
                  "pickMove", "os-jewel", "os-jewel-lg", "os-src-num",
                  "osLoadDashboard", "BORN CONNECTED",
                  'data-view="dashboard"', "os-src-feeds"):
        chk(probe in html, f"{label}: missing dashboard piece {probe}")
    chk(html.count("NOT CONNECTED") == 4, f"{label}: four honest invitation sources, got {html.count('NOT CONNECTED')}")
    _ord = [html.find('id="os-dash-pulse"'), html.find('id="os-dash-week"'),
            html.find('id="os-dash-faces"'), html.find('id="os-dash-insights"'),
            html.find('id="os-dash-convos"'), html.find('id="os-dash-plugins"')]
    chk(all(v > 0 for v in _ord) and _ord == sorted(_ord),
        f"{label}: dashboard front order broken {_ord}")
    chk(html.count('data-dash-how=') == 4, f"{label}: four how-it-works toggles")
    chk(DASH_LINE in html and PERSONAL_LINE not in html, f"{label}: model line swap")
    for ident in ("flagship-business", "flagship-community", "Acme Corp", "Our Community", "Nova Reyes"):
        chk(ident not in html, f"{label}: base must not carry {ident} (contract applies identity)")
    chk(html.count("--soul:#a06bff") == 1 and html.count("--tone:#a06bff") == 2,
        f"{label}: soul knobs moved")
    chk('<div class="ph-av" id="avv">' in html, f"{label}: #avv slot lost")
    chk(html.count("Alex Morgan") >= 2, f"{label}: base name spots lost")
    chk(".os-input,.os-textarea{" in html, f"{label}: block form grammar lost")
    views = sorted(set(re.findall(r'data-os-view="(\w+)"', html)))
    chk(views == sorted(["home", "dashboard", "about", "today", "notes", "people", "message",
                         "inbox", "growth", "lists", "reports", "settings"]),
        f"{label}: view set {views}")
    nb = js_check(html, label)
    css_check(html, label)
    if errs:
        raise SystemExit("VERIFY FAIL\n" + "\n".join(errs))
    print(f"{label}: verify OK ({nb} script blocks syntax-clean, CSS gate OK, "
          f"{len(html.encode())} bytes)")
    return len(html.encode())


def main():
    src_path = os.path.join(TPL, "personal.html")
    personal = load(src_path)
    reg = json.load(open(os.path.join(PIPE, "templates-registry.json")))
    md5 = hashlib.md5(personal.encode()).hexdigest()
    assert md5 == reg["templates"]["personal"]["md5"], \
        f"personal base drift: file {md5} != registry {reg['templates']['personal']['md5']}"
    out = build(personal)
    n = verify(out, "dashboard")
    bak = os.path.join(BACKUP, "dashboard.html.pre-dashview")
    cur_path = os.path.join(TPL, "dashboard.html")
    if not os.path.exists(bak):
        with open(bak, "w", encoding="utf-8") as f:
            f.write(load(cur_path))
    with open(cur_path, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"dashboard: wrote templates/dashboard.html ({n} bytes, md5 {hashlib.md5(out.encode()).hexdigest()})")


if __name__ == "__main__":
    main()
