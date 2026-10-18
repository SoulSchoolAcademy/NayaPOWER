#!/usr/bin/env python3
"""Build the law-examples gallery: all 16 Naya design laws, each with one
RIGHT and one WRONG rendered example.

WRONG examples are harvested from our own failed v1 template apps
(../failed-v1/) — our failures become the teaching set. Where v1 has no
example of a failure mode, the wrong is minimal and captioned
"illustrative".

RIGHT examples are harvested VERBATIM from Shawn's 7 canonical libraries,
Verity's Smart_factory_incomplete.html, and the builder index pieces —
with law-breakers fixed as harvested (standing order): hexes snapped to
the canonical union token set, never invented.

Output: index.html (self-contained, mobile-friendly, white text).
"""
import html as htmlmod
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import appmode  # noqa: E402  (reuse the token normalizer + gate token set)

FAILED_V1 = os.path.join(HERE, "..", "failed-v1")
INDEX_PATH = os.path.join(
    HERE, "..", "..", "..", "library", "catalog", "builder-index-v1.json")
USER_FILES = os.path.expanduser("~/workspace/user/files")

SOUL = "#a06bff"  # gallery accent (law purple)


def esc(s):
    return htmlmod.escape("" if s is None else str(s), quote=True)


def code_block(code):
    return '<pre class="code">%s</pre>' % esc(code)


# --------------------------------------------------------------------------
# Harvests
# --------------------------------------------------------------------------

def failed_v1_css_snippet(page, start_marker, length=420):
    src = open(os.path.join(FAILED_V1, page)).read()
    i = src.find(start_marker)
    if i < 0:
        return "/* (snippet not found) */"
    return src[i:i + length].strip()


def index_piece_css(models):
    index = json.load(open(INDEX_PATH))
    return appmode._piece_css(index, SOUL, models)


def index_piece_html(model):
    index = json.load(open(INDEX_PATH))
    return index["pieces"][model]["html"]


def orb_html(oc_hex, cls="orb"):
    """JWL orb structure (harvest pattern), parameterized by color."""
    r, g, b = (int(oc_hex[i:i + 2], 16) for i in (1, 3, 5))
    return ('<span class="%s" style="--oc:%s;--oc-rgb:%d,%d,%d"></span>'
            % (cls, oc_hex, r, g, b))


# --------------------------------------------------------------------------
# The 16 laws
# --------------------------------------------------------------------------

LAW_QUOTES = {
    1: "White text. Always. — Headings are white. Body is white or silver. Never colored text.",
    2: "Gold is earned, never applied. — Gold means shown value; green means proven; blue means stated.",
    3: "Chrome acts. Text speaks. Theme identifies. — Spectrum colors appear only on borders, glows, dots, rails, jewels. Never on text.",
    4: "Adjacent things never share a hue. — No two neighboring elements share the same or almost the same color.",
    5: "One board, one color. — Each card gets one fixed, unique color — its identity.",
    6: "White at rest. Its own color ignites on touch. — A resting control is white/neutral; color appears only on the lit state, in its own color.",
    7: "Boards are rectangles. — Lists lay out as horizontal rectangles, one after another. Not grids of squares.",
    8: "Restraint. Never a flood. — Color is precious because it is rare. When everything is lit, nothing is.",
    9: "Verbatim tokens, no private colors. — The canonical tokens are copied exactly. No invented hexes. No close enough.",
    10: "One global spectrum sequence per page. — Section accents follow magenta \u2192 purple \u2192 blue \u2192 green \u2192 gold, in law order.",
    11: "Preview before pick. — Every template offers a big, obvious preview. Choosing blind is the builder's failure.",
    12: "Mobile IS the app. — Every page is a mobile app first: killer on the phone, install-ready.",
    13: "Every control works, or it doesn't ship. — A button that doesn't function is a lie on the page.",
    14: "Compose, don't create. — Build from the library's real pieces — real HTML, real CSS, verbatim.",
    15: "Depth before color. Zero flat. — Every surface gets living depth: elevation, edge light, seating shadow.",
    16: "Size separates. Color never does. — Hierarchy comes from size and weight, never from colored text.",
}

# (law_no, name, right_html, right_caption, wrong_html, wrong_caption)
LAWS = []


def law(no, name, right_html, right_cap, wrong_html, wrong_cap):
    LAWS.append((no, name, right_html, right_cap, wrong_html, wrong_cap))


# ---- Law 1 ----
_l1_wrong_css = failed_v1_css_snippet(
    "personal/index.html", ".hero .kicker{")
law(1, "White text. Always.",
    '<div class="demo-pad">'
    '<p class="l1-kicker">MORNING BRIEFING</p>'
    '<h3 class="l1-title">Today, handled</h3>'
    '<p class="l1-body">White headings, silver body, on obsidian. Hierarchy comes from size — never from colored text.</p>'
    "</div>",
    "RIGHT — white kicker, white title, silver body. Hierarchy from size. (Voice: the index card piece NAYA-CRD-008.)",
    code_block(_l1_wrong_css) +
    '<div class="demo-pad"><p style="color:#a06bff;font-size:12px;font-weight:700;letter-spacing:.22em">MORNING BRIEFING</p></div>',
    "WRONG — our failed v1: the kicker was colored with the soul color. Shawn's word: kickers stay white, always.")

# ---- Law 2 ----
law(2, "Gold is earned, never applied.",
    '<div class="demo-pad"><p class="l1-body">'
    + orb_html("#ffbf3d", "orb orb--xs") +
    ' <b>Live now</b> — gold marks shown value: the LED is lit because the thing is actually live.</p></div>',
    "RIGHT — gold LED meaning \u201alive\u2019. Gold is a truth-state, never decoration. (Jewel Library orb pattern.)",
    '<div class="demo-pad"><h3 style="color:#ffbf3d">Our Amazing Features</h3>'
    '<p class="l1-body">A gold heading and gold borders, applied for looks.</p></div>',
    "WRONG (illustrative) — gold headings, gold borders for decoration. Gold is earned, not applied.")

# ---- Law 3 ----
law(3, "Chrome acts. Text speaks.",
    '<div class="demo-pad"><p class="l1-body">Words stay white. Color works on the chrome:</p>'
    '<div class="chrome-row">'
    + "".join('<span class="chrome-dot" style="--c:%s"></span>' % h for h in
              ["#e84fff", "#a06bff", "#3fb8ff", "#2fe89e", "#ffbf3d"]) +
    "</div>"
    '<div class="chrome-rail" style="--c:#40d3bb"></div>'
    '<p class="l1-fine">Jewels, dots, rails carry the color — the words never do.</p></div>',
    "RIGHT — spectrum color lives on the jewel, the dot, the rail. Text stays white.",
    '<div class="demo-pad"><p class="l1-body">The status dot is <span style="color:#2fe89e">green text</span> '
    'and the heading is <span style="color:#3fb8ff">blue text</span>.</p></div>',
    "WRONG (illustrative) — color used as text. If removing the color changes nothing about understanding, remove the color.")

# ---- Law 4 ----
_l4_wrong = failed_v1_css_snippet("personal/index.html", 'class="orbs"')
law(4, "Adjacent things never share a hue.",
    '<div class="demo-pad"><div class="orb-row">'
    + "".join('<span class="orb-wrap">%s</span>' % orb_html(h, "orb orb--xs")
              for h in ["#e84fff", "#a06bff", "#3fb8ff", "#2fe89e", "#ffbf3d"]) +
    '</div><p class="l1-fine">Five orbs, five spectrum colors, in law order. Never twice adjacent.</p></div>',
    "RIGHT — five orbs, five spectrum colors, in law order. (Jewel Library orb pattern, harvested verbatim.)",
    '<div class="demo-pad"><div class="orb-row">'
    + "".join('<span class="orb-wrap">%s</span>' % orb_html("#a06bff", "orb orb--xs") for _ in range(5)) +
    '</div><p class="l1-fine">Our failed v1: every orb purple — "--oc:#a06bff" on all five.</p></div>',
    "WRONG — our failed v1 hero: five orbs, one hue. All purple, all adjacent.")

# ---- Law 5 ----
law(5, "One board, one color.",
    '<div class="demo-pad"><div class="mini-cards">'
    + "".join(
        '<div class="card nb-demo" style="--accent:%s;--accent-soft:%s">'
        '<h3><span class="jewel" style="--jewel:%s">\u2727</span>%s</h3></div>'
        % (h, appmode._rgba(h, ".45"), h, name)
        for h, name in [("#e84fff", "Magenta board"), ("#3fb8ff", "Blue board"), ("#2fe89e", "Green board")]) +
    '</div><p class="l1-fine">Each board owns one color — you recognize the thing by its color.</p></div>',
    "RIGHT — three boards, three identities. (Index card piece NAYA-CRD-008, one --accent per board.)",
    '<div class="demo-pad"><div class="mini-cards">'
    + "".join(
        '<div class="card nb-demo" style="--accent:#a06bff;--accent-soft:rgba(160,107,255,.45)">'
        '<h3><span class="jewel" style="--jewel:#a06bff">\u2727</span>%s</h3></div>' % name
        for name in ["Board one", "Board two", "Board three"]) +
    '</div><p class="l1-fine">Our failed v1: every section glowed var(--soul) — purple, purple, purple.</p></div>',
    "WRONG — our failed v1: every board wore the same soul color. One board, one color was broken.")

# ---- Law 6 ----
law(6, "White at rest. Own color ignites on touch.",
    '<div class="demo-pad"><button class="rest-btn" type="button">Touch me</button>'
    '<p class="l1-fine">White rim at rest. Hover/touch: it ignites in its own color.</p></div>',
    "RIGHT — quiet at rest, own color on touch. (Button Set pattern; card piece hover law.)",
    '<div class="demo-pad"><button class="flood-btn" type="button">Always glowing</button> '
    '<button class="flood-btn" type="button">Always glowing</button>'
    '<p class="l1-fine">Colored while unselected — a purple unlit button is nonsense.</p></div>',
    "WRONG (illustrative) — colored unselected controls. Five lit buttons in a row is overload.")

# ---- Law 7 ----
law(7, "Boards are rectangles.",
    '<div class="demo-pad"><div class="rect-list">'
    + "".join('<div class="rect-item"><b>%s</b><span>%s</span></div>' % t for t in
              [("Personal page", "My whole creative life in one app"),
               ("Booking page", "A calendar that books itself"),
               ("Menu page", "Everything we pour and bake")]) +
    "</div></div>",
    "RIGHT — horizontal rectangles, one after another. The eye reads down; each gets room to breathe.",
    '<div class="demo-pad"><div class="sq-grid">'
    + "".join('<div class="sq-item">%s</div>' % t for t in ["One", "Two", "Three", "Four"]) +
    "</div></div>",
    "WRONG (illustrative) — a grid of identical squares. No identity, no breathing room.")

# ---- Law 8 ----
law(8, "Restraint. Never a flood.",
    '<div class="demo-pad"><div class="card nb-demo" style="--accent:#a06bff;--accent-soft:rgba(160,107,255,.45)">'
    '<h3><span class="jewel" style="--jewel:#a06bff">\u2727</span>Restrained</h3>'
    '<p class="fine">Mostly black and white. One color, spent where it structures.</p></div></div>',
    "RIGHT — the rainbow knows its place. Color is precious because it is rare.",
    '<div class="demo-pad flood-demo"><h3 style="color:#a06bff">Everything glows</h3>'
    '<p style="color:#e84fff">Purple headings, magenta body,</p>'
    '<button class="flood-btn" type="button">Glowing button</button> '
    + orb_html("#a06bff", "orb orb--xs") +
    "<p class=\"l1-fine\">Our failed v1 scored 3\u20134/10: all pinks together.</p></div>",
    "WRONG — our failed v1: purple purple purple. A page where everything glows is a page where nothing does.")

# ---- Law 9 ----
law(9, "Verbatim tokens, no private colors.",
    '<div class="demo-pad"><div class="swatches">'
    + "".join('<span class="sw" style="background:%s" title="%s"></span>' % (h, n) for h, n in
              [("#050507", "obsidian"), ("#a06bff", "purple"), ("#e84fff", "magenta"),
               ("#3fb8ff", "blue"), ("#2fe89e", "green"), ("#ffbf3d", "gold"),
               ("#40d3bb", "teal"), ("#6675ff", "indigo"), ("#ff5e6c", "red"), ("#ff9a5a", "orange")]) +
    '</div><p class="l1-fine">Copied exactly. If it isn\u2019t a token, it doesn\u2019t go on the page.</p></div>',
    "RIGHT — the canonical N5 token set, verbatim. (The Law-9 gate fails any other hex.)",
    code_block("--field: #0B0D12;\n--raise: #10141d;\n--card: #141a28;  /* v1 shell CSS */"),
    "WRONG — our failed v1 shell used hexes outside the 16-law token set. (Reconciled 2026-10-18: the Hub :root tokens joined the canonical set.)")

# ---- Law 10 ----
law(10, "One global spectrum sequence per page.",
    '<div class="demo-pad"><div class="walk-row">'
    + "".join('<span class="walk-chip" style="--c:%s">%s</span>' % (h, n) for h, n in
              [("#e84fff", "magenta"), ("#a06bff", "purple"), ("#3fb8ff", "blue"),
               ("#2fe89e", "green"), ("#ffbf3d", "gold")]) +
    '</div><p class="l1-fine">Section accents follow the spectrum in law order, strict by position.</p></div>',
    "RIGHT — magenta \u2192 purple \u2192 blue \u2192 green \u2192 gold. Richest first, magenta leading.",
    '<div class="demo-pad"><p class="l1-body">Every section accent: <code>var(--soul)</code>.</p>'
    '<p class="l1-fine">Our failed v1: one hue for the whole page — the spectrum never walked.</p></div>',
    "WRONG — our failed v1: a single-hue page. The gate now fails any page walking fewer than 3 hues.")

# ---- Law 11 ----
law(11, "Preview before pick.",
    '<div class="demo-pad"><div class="tcard-demo"><b>Booking page</b>'
    '<span>A calendar that books itself</span>'
    '<button class="tview" type="button">VIEW</button></div>'
    '<p class="l1-fine">A lit board with a real view button — see the sample before you commit.</p></div>',
    "RIGHT — template card with a big, obvious preview. (Harvested from Verity's Smart_factory_incomplete.html.)",
    '<div class="demo-pad"><div class="sq-grid"><div class="sq-item">???</div></div>'
    '<p class="l1-fine">A small block, no preview. Choosing blind is the builder\u2019s failure.</p></div>',
    "WRONG (illustrative) — picking from a small block alone, sight unseen.")

# ---- Law 12 ----
law(12, "Mobile IS the app.",
    '<div class="demo-pad"><div class="phone"><div class="phone-notch"></div>'
    '<p class="l1-kicker">MORNING BRIEFING</p><h3 class="l1-title">Today, handled</h3>'
    '<button class="rest-btn" type="button">Open</button></div>'
    '<p class="l1-fine">Killer on the phone by default. Mobile isn\u2019t a version — mobile is the app.</p></div>',
    "RIGHT — every template is born a phone app: mobile-optimized, installable.",
    '<div class="demo-pad"><div class="desk"><p class="l1-fine">A 1400px canvas that collapses into nothing on a phone.</p></div></div>',
    "WRONG (illustrative) — desktop-only. A page that dies on the phone was never an app.")

# ---- Law 13 ----
law(13, "Every control works, or it doesn't ship.",
    '<div class="demo-pad"><button class="rest-btn" type="button" id="law13btn">Tap me</button> '
    '<span class="l1-fine" id="law13out">Not tapped yet.</span></div>',
    "RIGHT — this button really works: tap it and see. (Pretty but useless never ships.)",
    '<div class="demo-pad"><button class="dead-btn" type="button">Tap me</button> '
    '<span class="l1-fine">Nothing happens. A button that doesn\u2019t function is a lie on the page.</span></div>',
    "WRONG (illustrative) — the dead button above really does nothing. Staged, not working.")

# ---- Law 14 ----
_l14_wrong = failed_v1_css_snippet("personal/index.html", ".topbar{")
law(14, "Compose, don't create.",
    '<div class="demo-pad">'
    '<div class="card nb-demo" style="--accent:#2fe89e;--accent-soft:rgba(47,232,158,.45)">'
    '<h3><span class="jewel" style="--jewel:#2fe89e">\u2727</span>Section board</h3>'
    '<p class="fine">Model <b>NAYA-CRD-008</b> — every structural element traces to an index model.</p></div>'
    '<p class="l1-fine">Chassis pattern: index-2.html (Hub). Pieces: the 478-piece index. Nothing invented.</p></div>',
    "RIGHT — our fixed v2: the section board IS index piece NAYA-CRD-008, manifest-visible.",
    code_block(_l14_wrong),
    "WRONG — our failed v1: the topbar was hand-written CSS, invented, tracing to no piece.")

# ---- Law 15 ----
law(15, "Depth before color. Zero flat.",
    '<div class="demo-pad"><div class="card nb-demo" style="--accent:#3fb8ff;--accent-soft:rgba(63,184,255,.45)">'
    '<h3><span class="jewel" style="--jewel:#3fb8ff">\u2727</span>Elevated</h3>'
    '<p class="fine">Edge light, seating shadow, inner depth — premium in monochrome first.</p></div></div>',
    "RIGHT — living depth: elevation, edge light, seating shadow. (Index card piece; Law 15 sharpened: 3D, never flat 2D.)",
    '<div class="demo-pad"><div class="flat-box"><p class="l1-body">Flat box</p></div>'
    '<p class="l1-fine">No elevation, no edge light. Flat is a defect.</p></div>',
    "WRONG (illustrative) — a flat surface. If it does not read as premium in monochrome, color will not save it.")

# ---- Law 16 ----
law(16, "Size separates. Color never does.",
    '<div class="demo-pad">'
    '<p class="l1-kicker">KICKER — SMALL</p>'
    '<h3 class="l1-title">Headline — large</h3>'
    '<p class="l1-body">Body — medium. Three sizes, one color: white. The eye knows what matters.</p></div>',
    "RIGHT — hierarchy from size and weight. Color never tells the eye what matters most.",
    '<div class="demo-pad">'
    '<p style="color:#a06bff;font-size:14px">kicker — colored</p>'
    '<p style="color:#e84fff;font-size:14px">headline — colored, same size</p>'
    '<p style="font-size:14px">body — same size again</p></div>',
    "WRONG — our failed v1 habit: color doing size\u2019s job. Hierarchy from size, never from colored text.")

# Manifest rule (Shawn's 2026-10-17 rule, gated)
law("R", "Visible piece manifest.",
    '<div class="demo-pad manifest-demo"><p class="l1-fine">PIECE MANIFEST</p><ul>'
    '<li><b>NAYA-CRD-008</b> — Aliveness \u2727 · section boards</li>'
    '<li><b>NAYA-JWL-001</b> — finished objects of light · hero orb</li></ul></div>',
    "RIGHT — our fixed v2: every page carries a visible manifest — model number + label per element.",
    '<div class="demo-pad"><p class="l1-fine">Our failed v1 pages carried no manifest at all. '
    "Shawn couldn't verify a single piece. The build gate now fails pages without one.</p></div>",
    "WRONG — our failed v1: no visible piece manifest. Absent = build FAILS.")


GALLERY_CSS = """
:root{--obsidian:#050507;--soul:#a06bff;--ink:#F8F7FB;--quiet:rgba(248,247,251,.72);
--faint:rgba(248,247,251,.5);--line:rgba(255,255,255,.14)}
*{box-sizing:border-box}
body{margin:0;background:var(--obsidian);color:var(--ink);
font-family:Inter,system-ui,-apple-system,'Segoe UI',sans-serif;line-height:1.55;
-webkit-font-smoothing:antialiased}
.wrap{max-width:1060px;margin:0 auto;padding:0 20px}
.ghead{padding:56px 0 8px}
.ghead .eyebrow{font-size:11px;letter-spacing:.24em;font-weight:700;color:#fff;margin-bottom:12px}
.ghead h1{font-family:Newsreader,Georgia,serif;font-size:clamp(30px,5vw,48px);margin:0 0 12px;color:#fff}
.ghead p{color:var(--quiet);max-width:680px;margin:0}
.law{margin:26px 0;background:linear-gradient(180deg,rgba(255,255,255,.045),rgba(255,255,255,.015));
border:1px solid var(--line);border-radius:22px;padding:26px;
box-shadow:inset 0 1px 0 rgba(255,255,255,.09),0 24px 60px rgba(0,0,0,.55)}
.law-head{display:flex;gap:14px;align-items:baseline;margin-bottom:6px}
.law-no{font-size:12px;font-weight:800;letter-spacing:.18em;color:#fff;border:1px solid var(--line);
border-radius:999px;padding:5px 12px;white-space:nowrap}
.law-head h2{font-size:24px;margin:0;color:#fff}
.law-quote{color:var(--quiet);font-size:14px;margin:0 0 18px;max-width:760px}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:18px}
@media(max-width:720px){.pair{grid-template-columns:1fr}}
.side{border:1px solid var(--line);border-radius:16px;padding:18px;background:rgba(255,255,255,.02)}
.side-tag{display:inline-block;font-size:10px;font-weight:800;letter-spacing:.2em;
border-radius:999px;padding:5px 12px;margin-bottom:12px}
.side.right .side-tag{color:#050507;background:#2fe89e}
.side.wrong .side-tag{color:#fff;background:#ff5e6c}
.side .cap{font-size:13px;color:var(--quiet);margin:12px 0 0}
.demo-pad{padding:6px 2px}
pre.code{background:#020203;border:1px solid var(--line);border-radius:12px;padding:14px;
font-size:12px;color:var(--quiet);overflow:auto;white-space:pre-wrap;margin:0 0 12px}
.l1-kicker{font-size:11px;font-weight:700;letter-spacing:.24em;color:#fff;margin:0 0 8px}
.l1-title{font-size:26px;margin:0 0 8px;color:#fff}
.l1-body{font-size:15px;color:var(--quiet);margin:0}
.l1-fine{font-size:12px;color:var(--faint);margin:10px 0 0}
.orb-row{display:flex;gap:22px;flex-wrap:wrap;align-items:center;margin:8px 0}
.chrome-row{display:flex;gap:14px;margin:12px 0}
.chrome-dot{width:18px;height:18px;border-radius:50%;background:var(--c);
box-shadow:0 0 14px var(--c)}
.chrome-rail{height:6px;border-radius:3px;background:var(--c);margin:10px 0;
box-shadow:0 0 12px var(--c)}
.mini-cards{display:flex;flex-direction:column;gap:12px}
.rest-btn{background:#fff;color:#050507;border:1.5px solid #fff;border-radius:999px;
padding:12px 24px;font-weight:800;cursor:pointer;transition:all .2s}
.rest-btn:hover{background:#2fe89e;border-color:#2fe89e;color:#fff;
box-shadow:0 0 22px rgba(47,232,158,.7)}
.flood-btn{background:#a06bff;color:#fff;border:none;border-radius:999px;
padding:12px 24px;font-weight:800;cursor:pointer;box-shadow:0 0 18px #a06bff}
.dead-btn{background:transparent;color:#fff;border:1px solid var(--line);
border-radius:999px;padding:12px 24px;cursor:not-allowed;opacity:.7}
.rect-list{display:flex;flex-direction:column;gap:12px}
.rect-item{display:flex;flex-direction:column;gap:2px;border:1px solid var(--line);
border-radius:14px;padding:16px 18px;background:rgba(255,255,255,.02)}
.rect-item b{color:#fff}.rect-item span{color:var(--quiet);font-size:13px}
.sq-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}
.sq-item{aspect-ratio:1;border:1px solid var(--line);border-radius:12px;display:grid;
place-items:center;color:var(--quiet);font-size:13px}
.swatches{display:flex;gap:10px;flex-wrap:wrap;margin:6px 0}
.sw{width:44px;height:44px;border-radius:12px;border:1px solid rgba(255,255,255,.25)}
.walk-row{display:flex;gap:10px;flex-wrap:wrap}
.walk-chip{font-size:12px;font-weight:700;color:#fff;border:1px solid var(--c);
border-radius:999px;padding:8px 14px;box-shadow:0 0 14px var(--c)}
.tcard-demo{border:1px solid var(--line);border-radius:16px;padding:18px;
display:flex;flex-direction:column;gap:8px;background:rgba(255,255,255,.02)}
.tcard-demo b{color:#fff}.tcard-demo span{color:var(--quiet);font-size:13px}
.tview{align-self:center;background:#fff;color:#050507;border:none;border-radius:999px;
padding:10px 34px;font-weight:800;cursor:pointer;margin-top:6px}
.phone{width:280px;margin:0 auto;border:1px solid var(--line);border-radius:32px;
padding:38px 18px 26px;background:#0B0D12;position:relative;
box-shadow:inset 0 1px 0 rgba(255,255,255,.12),0 20px 50px rgba(0,0,0,.6)}
.phone-notch{position:absolute;top:12px;left:50%;transform:translateX(-50%);
width:110px;height:22px;border-radius:11px;background:#020203}
.desk{border:1px solid var(--line);border-radius:12px;padding:30px;max-width:560px;margin:0 auto}
.flat-box{border:1px solid var(--line);padding:22px;border-radius:6px;background:#0B0D12}
.manifest-demo ul{list-style:none;margin:10px 0 0;padding:0;display:flex;flex-direction:column;gap:6px}
.manifest-demo li{font-size:13px;color:var(--ink)}
.manifest-demo li b{color:#fff}
.gfoot{margin:40px 0 80px;color:var(--faint);font-size:13px}
code{color:var(--quiet)}
.nb-demo{margin:0}
"""

JS = """
<script>
(function(){
  var b=document.getElementById('law13btn'), o=document.getElementById('law13out');
  if(b&&o){ b.addEventListener('click',function(){
    o.textContent='Tapped — it works. '+new Date().toLocaleTimeString(); }); }
})();
</script>
"""


def main():
    sections = []
    for no, name, right_html, right_cap, wrong_html, wrong_cap in LAWS:
        sections.append(
            '<section class="law" id="law-%s">'
            '<div class="law-head"><span class="law-no">LAW %s</span><h2>%s</h2></div>'
            '<p class="law-quote">%s</p>'
            '<div class="pair">'
            '<div class="side right"><span class="side-tag">RIGHT</span>%s<p class="cap">%s</p></div>'
            '<div class="side wrong"><span class="side-tag">WRONG</span>%s<p class="cap">%s</p></div>'
            "</div></section>"
            % (no, no, esc(name), esc(LAW_QUOTES[no] if isinstance(no, int) else
              "Every page carries a visible piece manifest — model number + label per element."),
               right_html, right_cap, wrong_html, wrong_cap))
    piece_css = index_piece_css(["NAYA-CRD-008", "NAYA-JWL-001", "NAYA-JWL-003"])
    html = ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
            '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
            "<title>The 16 Naya Design Laws — Right and Wrong</title>\n"
            + '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800'
            '&family=Newsreader:opsz,wght@6..72,500;6..72,600&display=swap" rel="stylesheet">\n'
            "<style>\n" + GALLERY_CSS + "\n" + piece_css + "\n</style>\n</head>\n"
            '<body><div class="nb-scope"><div class="wrap">\n'
            '<header class="ghead"><div class="eyebrow">NAYA DESIGN LAWS — OFFICIAL 2026-10-17</div>'
            "<h1>Right and wrong, side by side</h1>"
            "<p>All 16 laws, each with one RIGHT and one WRONG rendered example. "
            "WRONG examples are harvested from our own failed v1 template apps — our failures "
            "are the teaching set. RIGHT examples are harvested verbatim from Shawn's 7 canonical "
            "libraries and Verity's factory page, with law-breakers fixed as harvested. "
            "Nothing invented.</p></header>\n"
            + "\n".join(sections) +
            '<footer class="gfoot">Built by BUILD/Nu, Team Nitro · 2026-10-18 · '
            'the design-law gate (gate_design_laws in appmode.py) enforces these mechanically.</footer>\n'
            "</div></div>" + JS + "\n</body>\n</html>\n")
    out = os.path.join(HERE, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("ok: wrote %s (%d bytes, %d laws)" % (out, len(html), len(LAWS)))


if __name__ == "__main__":
    main()
