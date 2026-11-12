#!/usr/bin/env python3
"""
check-gate.py — THE DESIGN-CONTRACT GATE AS A MACHINE CHECK
Concept 2 of Shawn's LOCK-IN-10 order (2026-11-08 16:37Z), plus the ADDENDUM
(Shawn's eye, 2026-11-08 16:41Z: look-alike parts, not harvested parts).

Usage:  python3 check-gate.py <page.html> [more pages...]
Exit 0 only when every gate item PASSES on every page given; non-zero on any FAIL.
Python stdlib only. STATIC source-level checker (HTML + CSS parsing).

STATIC-ONLY CONSTRAINT — Playwright is DEAD in this VM since 16:18Z 2026-11-08
(Firefox SIGSEGV / Chromium SIGTRAP on launch). This checker therefore measures
the SOURCE, never the render. It cannot see what Shawn's eye sees: whether a
gold glow reads as a yellow button, whether a gauge's needle actually moves,
whether a board sits in the right place. LIVE-RENDER UPGRADE PATH (when
Playwright recovers): run the SAME five checks plus (f) against a rendered
page — (a) computed background-color of every painted surface via
getComputedStyle, (b) computed box-shadow on every visible button/board,
(c) needle transform sampled over time (rAF must move it; no CSS transition),
(d) OCR / pixel-diff on <img> regions to catch text-in-image, (e) the same
containment walk on the live DOM, (f) computed styles of buttons/gauges/
numbers compared against the harvested reference rules. Until then, a PASS
here means "the source carries the harvested parts and no measured violation"
— never "Shawn has seen it". His eye is the final gate, always.

THE GATE ITEMS (a)–(i) + HUMAN CHECKS (H1–H5) (from THE-INVENTORY.md Part 1
+ the 2026-11-08 lesson: the contract was NAMED in every brief and CHECKED
in none; plus TONIGHT'S LAWS, 2026-11-09 — the laws live in the brief
template §2A and are checked here where the machine can check them):
  (a) ZERO white/light backgrounds anywhere on the page.
  (b) Every element raised/elevated (real depth, real lift, real light).
  (c) Gauges present and alive (the speedometer language on the numbers).
      Two kinds, two standards (2026-11-09 gate fix): a mount inside
      calculator context (any ancestor naming the calculator — id
      "calculator", class calc-gauge / calc-body / calc-...) is the
      CALCULATOR gauge — the pricing speedometer — measured against its
      own standard: number on top, gauge underneath, needle/dial alive
      (JS wiring moves it with the numbers), gold rim intact. A mount
      anywhere else is the Dashboard NEEDLE-LAW gauge: #tn-tacho-mount
      in the DOM, .tn-tacho-needle in the DOM, the winning needle rule
      carries NO real CSS transition (rAF owns the motion), gear teeth
      present (>= 2). Measuring the calculator gauge against the needle
      law is a category error — fixed 2026-11-09.
  (d) NO text-in-image, NO pasted document. A data:image/ payload is
      opaque binary — base64 noise contains random "doc"/"list"
      substrings — so the payload bytes are NEVER scanned for text
      signals (2026-11-09 gate fix: the 8 Naya faces + orbs were 23
      false positives). The alt text of a data-URI image IS still
      scanned, and file/URL images are scanned on src + alt as before:
      a real pasted document (screenshot file, document-signalling
      filename or alt) still FAILS.
  (e) NO bare text blocks — every word lives in a board, pill, jewel, or orb.
  (f) NO LOOK-ALIKE buttons/gauges/numbers (addendum 16:41Z) — a part that is
      not the harvested part FAILS. Any button, gauge, or number element whose
      classes are NOT on the allowlist below (and not a named harvest source
      with file + line) is flagged LOOK-ALIKE and fails.

THRESHOLDS (chosen by the gate seat, calibrated against the two known files —
see TEST-REPORT.md; change a constant here and the report must say so):
  (a) Light = HSL lightness >= 0.80 (a near-white / pale colour). Luminance
      was REJECTED as the test: it fires on saturated brand accents
      (emerald #2fe89e lum 0.61, gold #ffd45a lum 0.69) that are objects, not
      light backgrounds. Gold #d9a521 (lightness 0.50) and #ffbf3d (0.62)
      pass; #fff, #f8f7fb, #d9d9de, #e8e8ec pass as light. rgba() colours
      are blended over the obsidian base #050607 first, so a white tint at
      low alpha (rgba(255,255,255,.06)) stays dark.
      A1 base canvas: a body/html rule MUST set a dark background
      (luminance <= 0.30, var() resolved through :root). No dark canvas =
      the browser's default white canvas shows through — exactly the
      fix-12 defect (chart cells on white). A2 solid light surfaces: any
      solid background/background-color that is light, EXCEPT pseudo-elements
      (::before/::after — specular highlights), elements whose own rule
      declares width AND height both <= 32px (dots, jewels, toggle knobs),
      background-clip:text rules (text gradients, not surfaces), the NUMBER
      LANGUAGE (digit reels/tiles/caps — the number objects, judged by
      (c)/(f) instead of (a)), and ACTIVE-STATE INVERSIONS (a selected
      control inverting to light, e.g. .os-viewtoggle button.on — the lit
      state, white pill with dark text by design). A3 light gradients: a
      gradient background whose light stops cover >= 50% of its span (a
      segment counts light only when BOTH end stops are light, so a #fff 0%
      specular point does not condemn an orb), with the same exemptions.
      One hit in A1/A2/A3 fails (a). A naive "#fff anywhere" rule was
      REJECTED: the known-good Dashboard uses #fff legitimately as 0%
      specular highlights in radial gradients, 8px glow dots, and text
      gradients — counting those would fail the good file and teach
      builders to strip the light out of the real-object law.
  (b) Depth = a box-shadow declaration (other than none) on a rule that
      applies to the element (matched by class, id, attribute, or tag token).
      A border alone is NOT depth — a flat bordered box is not a raised
      object. In scope: every <button>, every <a> carrying a button-like
      class, every board/pill/jewel/orb/card/panel element. PASS when
      >= 90% of in-scope elements carry depth (the 10% slack is for text
      links and glyph-only closes that are flat by design).
  (c) PASS when the real needle-law gauge is present: #tn-tacho-mount in the
      DOM, .tn-tacho-needle in the DOM, the winning needle rule carries NO
      real CSS transition (`transition:none` IS the law — rAF owns the
      motion; the last .tn-tacho-needle rule in source order decides), and
      gear teeth are present (>= 2 occurrences of tn-gear-tooth). Pages with
      no gauge PASS on the fallback only when live numbers are present
      (tiled digits / svgnum / orbiting orbs with numerals); a page with
      neither a gauge nor live numbers FAILS (c). A page whose numbers are
      plain text FAILS the fallback.
  (d) FAIL on any <img> whose src or alt signals text content (keywords:
      top-ten/top10, chart, document, doc, screenshot, slide, reason, items,
      list, .pdf, docs.google), any <figure> whose caption says screenshot,
      any <iframe>/<embed>/<object> pointing at a document or PDF.
  (e) A substantial text block (>= 20 chars of direct text in p/h1-h6/li/td/
      div/span, outside button/a/nav/script/style/head) must live inside a
      board/pill/jewel/orb container — self or any ancestor carrying a
      container class (card, board, pill, jewel, orb, panel, strip, badge,
      tab, tile, note, item, cell, pop, modal, detail, or the os-/ph-/tn-/
      pj-/ib-/nsb- families). PASS when >= 80% of substantial blocks are
      contained. Page chrome (hero headlines, section kickers) counts as
      bare and is reported — the 20% slack is for it, and the report names it.
  (f) F1 pedigree: every <button> and every button-like <a> (class contains
      btn/primo/pill/tab/cta/toggle/switch) must carry an allowlisted class
      or a family-prefix class (os-, ph-, tn-, pj-, ib-, nsb-). An id or
      data-* address excuses a button ONLY when it carries no meaningful
      class at all (the Dashboard's 82 classless tab/back buttons live this
      way — counted, not failed). A button WITH a custom class outside the
      allowlist is LOOK-ALIKE even if it also has a data-* hook — the hook
      is wiring, not pedigree. Pure state classes (on/is-on/active/selected/
      open) are ignored when judging pedigree. Any other custom button class
      is LOOK-ALIKE. F2 gold-theme CTA: any button/CTA carrying theme-gold or
      theme-yellow, or an inline yellow/gold solid background, is LOOK-ALIKE
      (the condemned yellow "try her nine free" button wore exactly
      `primo theme-gold`). F3 needle law: when a gauge is present, its
      winning needle rule must have no real `transition` (`transition:none`
      is the law), and gear teeth must be present (>= 2 occurrences). F4 numbers are evidence only: tiled digits /
      svgnum / orb numerals counted and reported; a static check cannot
      prove the digits render as the harvested tiles — that is his eye's
      call, and the report says so. (f) FAILS on any F1, F2, or F3 hit.
  (g) NOTE FORMAT (2026-11-09, SN-2444) — a smart-note file (.md) must give
      the feed parser ## sections to find (Hook / Nutshell / Human / Child /
      Grandma / Naya). FAILS when the note carries NO ## sections at all, or
      when its sections are defined by bold-inline labels (**Hook:**,
      **Nutshell:**, ...) with zero ## headings — that is the defect that
      kept five notes out of the feed in one night. Bold-inline labels
      QUOTED as examples alongside real ## sections are reported, not
      failed: the note parses, and the note that documents the fix (SN-2444)
      quotes the bad format itself. Run as: check-gate.py <note.md> —
      .md files get (g) only.
  (h) NO DICTATION-BLUNT PHRASES (2026-11-09, SN-2442) — page copy must not
      carry blunt dictation lines Shawn himself flagged ("never cash back" —
      his private words posted in public, not professional copy). The banned
      list holds ONLY phrases Shawn flagged; extend it only with his flag.
  (i) TITLE + SUBTITLE + NUTSHELL + FACES ALTERNATE (2026-11-09, SN-2448 /
      SN-2431) — every story board (.calc-story-card) carries a non-empty
      .board-title, .board-sub and .board-nut; consecutive boards alternate
      face-left / face-right; every face image is a different source. A
      board missing any part, two boards on the same side in a row, or a
      repeated face FAILS. The Ten is the same family in a different
      shape (2026-11-09 gate fix): a board carrying .ult-card / .ult-part
      is a TEN board — title (.board-title) + three parts (.ult-part-why,
      .ult-part-sol, .ult-part-nut, each with at least one real bullet)
      + who line (.ult-who). A Ten missing its nutshell (.ult-part-nut)
      FAILS (i) exactly as a hired board missing .board-nut does. Pages
      with no story boards pass (i) as not applicable.
  HUMAN CHECKS (H1–H5) — what the machine cannot check, a NAMED HUMAN CHECK
  the seat must run and report in the handoff. A gate that isn't run is not
  a pass. Printed after the machine checks on every run; attested with
  --human-checks FILE (lines "H1: PASS — <evidence>"). Without the flag the
  verdict reads PASS — MACHINE ONLY, HUMAN CHECKS PENDING.
    H1 STRANGER TEST (SN-2442) — read every beat/board as a stranger who
       knows nothing: does she get it, believe it, trust us enough to come
       in? Every beat must answer the question it raises with a mechanism,
       a picture, or a number she can check.
    H2 PERFECT-WORDS LAW (daily log 2026-11-09 02:56Z) — public copy is
       professional and explains itself; no verbatim dictation, no process
       talk, no stage directions; Naya speaks in the first person.
    H3 FACE QUALITY (SN-2431) — every face beside the words looks real and
       high quality at render size: no pixelation, no blur. (The machine
       checks alternation + distinctness; the eye checks quality. Board 7's
       pixelated face on v63 is exactly what this check exists to catch.)
    H4 THE TEST IN HIS HEAD (SN-2443) — is this 10-star service? Would a
       stranger see the value and trust it? If they experienced it, would
       they get it? Is it obvious? Useful? Helpful? So clear it's evident
       what it does and what it is — and it does awesome?
    H5 THE ONE ULTIMATE TEN (daily log 2026-11-09 03:21Z + 03:28Z) — one
       set, not two: each item is pain + solution + what's in it for them
       (+ who it's for). The features are valuable BECAUSE they solve the
       pains.

HARVEST ALLOWLIST — harvested classes from THE-INVENTORY.md Parts 2/2b/2c
(~/workspace/team-nitro/THE-INVENTORY.md). A class is on the list only if the
inventory names it with a source file + line (or, for the family prefixes,
the inventory names the family as the shared language across pages).
  Buttons: .primo, .primo-btn, .powercast-topbtn, .nav-btn, .up-act,
    .tn-li-btn, .btn (PI face), .rooms-plus, .eco-plus, .nsb-btn.
  Boards: .ph-card, .ph-nutshell, .intel-item, .os-id-row, .strip,
    .pagecard, .inforow, .score, .panel, .todoitem, .board, .lib-card,
    .lib-cover, .handle-board, .pcard, .real-note.
  Jewels / orbs: .os-jewel, .os-jewel-h, .pj-jewel, .pj-jewel-lg,
    .ib-card-orb, .orb--hero, .intel-avatar, .chart-orb.
  Gauge / numbers: .tn-tacho-needle, .tn-gear-tooth, .tn-tacho (mount is
    the id #tn-tacho-mount), .svgnum, .progbar, .progfill, .pct-pop.
  Pills / tabs / badges: .smart-tabs, .smart-tab, .tabrow, .tab, .badge,
    .szpill.
  Families (prefixes — the shared language, inventory Part 2c cross-checks):
    os-, ph-, tn-, pj-, ib-, nsb-.
  NOT on the list (named gaps in the inventory — a builder citing one must
  name its harvest source with file + line, or the gate flags it):
    .note-card (Hub JS line 8225, no CSS rule found), .os-savebtn (cited
    in a mail.html comment, rule not located), the 7 canonical libraries
    (TO-LOCATE), .tier-head-btn, .calc-plan, .calc-unit-btn, .calc-ex,
    .detail-close, .detail-compact-toggle, .steppill (fix-12's own
    inventions — the chart's header pills have no harvested pedigree).
"""
import hashlib
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

# ---------------------------------------------------------------- thresholds
LIGHTNESS = 0.80        # HSL lightness at/above this is a light background
DARK_CANVAS_LUM = 0.30   # the base canvas must be at most this dark
TINY_PX = 32             # width AND height <= this: a dot/knob, not a surface
GRADIENT_LIGHT_COVERAGE = 0.50
DEPTH_PASS_RATIO = 0.90
CONTAINED_PASS_RATIO = 0.80
TEXT_MIN_LEN = 20
NUMBER_LANGUAGE_WORDS = ("reel", "tile", "digit", "svgnum", "cap", "numeral")
ACTIVE_STATE_WORDS = (".on", ".active", ".is-on", ".selected", "[aria-pressed=true]",
                      ":checked")

NOTE_SECTION_LABELS = ("hook", "nutshell", "human", "child", "grandma", "naya")
# Banned blunt phrases: ONLY phrases Shawn himself flagged as dictation made
# public. Extend ONLY with his flag — never by a seat's taste.
BANNED_BLUNT_PHRASES = (
    ("never cash back",
     "Shawn 2026-11-09 02:54Z — 'reads like my dictation posted in public'"),
)

HUMAN_CHECKS = (
    ("H1", "STRANGER TEST",
     "Read every beat/board as a stranger who knows nothing: does she get it, "
     "believe it, trust us enough to come in? Every beat must answer the "
     "question it raises with a mechanism, a picture, or a number she can check."),
    ("H2", "PERFECT-WORDS LAW",
     "Public copy is professional and explains itself; no verbatim dictation, "
     "no process talk, no stage directions; Naya speaks in the first person."),
    ("H3", "FACE QUALITY",
     "Every face beside the words looks real and high quality at render size: "
     "no pixelation, no blur. (The machine checks alternation + distinctness; "
     "the eye checks quality.)"),
    ("H4", "THE TEST IN HIS HEAD",
     "Is this 10-star service? Would a stranger see the value and trust it? "
     "If they experienced it, would they get it? Is it obvious? Useful? "
     "Helpful? So clear it's evident what it does and what it is — and it "
     "does awesome?"),
    ("H5", "THE ONE ULTIMATE TEN",
     "One set, not two: each item is pain + solution + what's in it for them "
     "(+ who it's for). The features are valuable BECAUSE they solve the pains."),
)

NAMED_COLORS = {
    "white": "#ffffff", "snow": "#fffafa", "ghostwhite": "#f8f8ff",
    "ivory": "#fffff0", "whitesmoke": "#f5f5f5", "seashell": "#fff5ee",
    "floralwhite": "#fffaf0", "aliceblue": "#f0f8ff", "azure": "#f0ffff",
    "honeydew": "#f0fff0", "mintcream": "#f5fffa", "lightgrey": "#d3d3d3",
    "lightgray": "#d3d3d3", "silver": "#c0c0c0", "gainsboro": "#dcdcdc",
    "beige": "#f5f5dc", "linen": "#faf0e6", "oldlace": "#fdf5e6",
    "lavender": "#e6e6fa", "mistyrose": "#ffe4e1", "lightyellow": "#ffffe0",
    "lightgoldenrodyellow": "#fafad2", "yellow": "#ffff00", "gold": "#ffd700",
    "khaki": "#f0e68c", "palegoldenrod": "#eee8aa",
}
BASE_RGB = (5, 6, 7)  # obsidian base #050607 — translucent whites blend over it


def lum_hex(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) not in (6, 8):
        return None
    try:
        r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    except ValueError:
        return None
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = f(r), f(g), f(b)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def parse_color(tok):
    """Return (r, g, b, alpha) or None for a CSS colour token."""
    tok = tok.strip().lower()
    if tok in NAMED_COLORS:
        tok = NAMED_COLORS[tok]
    m = re.match(r"#([0-9a-f]{3}|[0-9a-f]{6}|[0-9a-f]{8})$", tok)
    if m:
        h = m.group(1)
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 1.0)
    m = re.match(r"rgba?\(\s*([0-9.]+)[,\s]+([0-9.]+)[,\s]+([0-9.]+)(?:[,\s/]+([0-9.]+))?\s*\)$", tok)
    if m:
        a = float(m.group(4)) if m.group(4) is not None else 1.0
        return (float(m.group(1)), float(m.group(2)), float(m.group(3)), a)
    return None


def effective_lum(tok):
    """Relative luminance of a colour as painted over the obsidian base."""
    c = parse_color(tok)
    if c is None:
        return None
    r, g, b, a = c
    r = a * r + (1 - a) * BASE_RGB[0]
    g = a * g + (1 - a) * BASE_RGB[1]
    b = a * b + (1 - a) * BASE_RGB[2]
    return lum_hex("#%02x%02x%02x" % (round(r), round(g), round(b)))


def effective_lightness(tok):
    """HSL lightness (0..1) of a colour as painted over the obsidian base."""
    c = parse_color(tok)
    if c is None:
        return None
    r, g, b, a = c
    r = a * r + (1 - a) * BASE_RGB[0]
    g = a * g + (1 - a) * BASE_RGB[1]
    b = a * b + (1 - a) * BASE_RGB[2]
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    return (max(r, g, b) + min(r, g, b)) / 2.0


# ------------------------------------------------------------ harvest list
ALLOWLIST = {
    # buttons
    "primo", "primo-btn", "powercast-topbtn", "nav-btn", "up-act",
    "tn-li-btn", "btn", "rooms-plus", "eco-plus", "nsb-btn",
    # boards
    "ph-card", "ph-nutshell", "intel-item", "os-id-row", "strip",
    "pagecard", "inforow", "score", "panel", "todoitem", "board",
    "lib-card", "lib-cover", "handle-board", "pcard", "real-note",
    # jewels / orbs
    "os-jewel", "os-jewel-h", "pj-jewel", "pj-jewel-lg", "ib-card-orb",
    "orb--hero", "intel-avatar", "chart-orb",
    # gauge / numbers
    "tn-tacho-needle", "tn-gear-tooth", "tn-tacho", "svgnum",
    "progbar", "progfill", "pct-pop",
    # pills / tabs / badges
    "smart-tabs", "smart-tab", "tabrow", "tab", "badge", "szpill",
}
FAMILY_PREFIXES = ("os-", "ph-", "tn-", "pj-", "ib-", "nsb-")
STATE_CLASSES = {"on", "is-on", "active", "selected", "open"}
CONTAINER_WORDS = (
    "card", "board", "pill", "jewel", "orb", "panel", "strip", "badge",
    "tab", "tile", "note", "item", "cell", "pop", "modal", "detail",
)
BUTTON_LIKE_WORDS = ("btn", "primo", "pill", "tab", "cta", "toggle", "switch")
TEXT_IMG_WORDS = (
    "top-ten", "top10", "top_10", "chart", "document", "doc", "screenshot",
    "slide", "reason", "items", "list", ".pdf", "docs.google",
)
YELLOW_TOKENS = ("theme-gold", "theme-yellow")


def is_harvested(cls):
    return cls in ALLOWLIST or cls.startswith(FAMILY_PREFIXES)


def is_container_class(cls):
    low = cls.lower()
    return is_harvested(cls) or any(w in low for w in CONTAINER_WORDS)


# ------------------------------------------------------------- CSS handling
class CssRule:
    def __init__(self, selector, decl, line, source):
        self.selector = selector.strip()
        self.decl = decl
        self.line = line
        self.source = source

    def loc(self):
        return "%s:%d" % (self.source, self.line)


def strip_css_comments(text):
    # Remove comments but keep their newlines, so rule line numbers stay true.
    def _blank(m):
        return "".join("\n" if ch == "\n" else " " for ch in m.group(0))
    return re.sub(r"/\*.*?\*/", _blank, text, flags=re.S)


def parse_css_rules(css, base_line, source):
    """Yield CssRule objects; recurses into @media blocks."""
    css = strip_css_comments(css)
    rules = []
    i, n = 0, len(css)
    while i < n:
        j = css.find("{", i)
        if j == -1:
            break
        selector = css[i:j].strip()
        depth = 1
        k = j + 1
        while k < n and depth:
            if css[k] == "{":
                depth += 1
            elif css[k] == "}":
                depth -= 1
            k += 1
        decl = css[j + 1:k - 1]
        line = base_line + css[:i].count("\n")
        if selector.startswith("@"):
            rules.extend(parse_css_rules(decl, line, source + " " + selector.split("{")[0].strip()))
        elif selector:
            rules.append(CssRule(selector, decl, line, source))
        i = k
    return rules


def gradient_light_coverage(decl_value):
    """Fraction of a gradient's span covered by light segments.

    A segment between two adjacent stops counts light only when BOTH end
    stops are light colours. Stops without a position are spaced evenly.
    Returns None when the value has no gradient with >= 2 colour stops.
    """
    m = re.search(r"(?:linear|radial|conic)-gradient\((.*)\)", decl_value, re.S)
    if not m:
        return None
    inner = m.group(1)
    stops = []
    for cm in re.finditer(r"(#[0-9a-fA-F]{3,8}|rgba?\([^)]*\)|[a-z]+)"
                          r"(?:\s+([0-9.]+)\s*%)?", inner):
        tok = cm.group(1)
        if tok.lower() in ("circle", "ellipse", "at", "to", "deg") or tok.endswith("deg"):
            continue
        lum = effective_lightness(tok)
        if lum is None:
            continue
        pos = float(cm.group(2)) if cm.group(2) is not None else None
        stops.append((pos, lum))
    if len(stops) < 2:
        return None
    # fill missing positions evenly across 0..100
    known = [i for i, (p, _) in enumerate(stops) if p is not None]
    if not known:
        for i in range(len(stops)):
            stops[i] = (100.0 * i / (len(stops) - 1), stops[i][1])
    else:
        if stops[0][0] is None:
            stops[0] = (0.0, stops[0][1])
        if stops[-1][0] is None:
            stops[-1] = (100.0, stops[-1][1])
        prev = None
        for i, (p, lum) in enumerate(stops):
            if p is None:
                nxt = next((j for j in range(i + 1, len(stops)) if stops[j][0] is not None), None)
                p = stops[prev][0] + (stops[nxt][0] - stops[prev][0]) * (i - prev) / (nxt - prev) if nxt else 100.0
                stops[i] = (p, lum)
            else:
                prev = i
    covered = 0.0
    for (p0, l0), (p1, l1) in zip(stops, stops[1:]):
        if l0 >= LIGHTNESS and l1 >= LIGHTNESS:
            covered += max(0.0, p1 - p0)
    span = stops[-1][0] - stops[0][0]
    return (covered / span) if span > 0 else 0.0


def rule_is_pseudo(rule):
    return "::before" in rule.selector or "::after" in rule.selector


def rule_is_tiny(rule, size_map=None):
    w = re.search(r"(?<![a-z-])width\s*:\s*([0-9.]+)px", rule.decl)
    h = re.search(r"(?<![a-z-])height\s*:\s*([0-9.]+)px", rule.decl)
    if w and h and float(w.group(1)) <= TINY_PX and float(h.group(1)) <= TINY_PX:
        return True
    if size_map:
        # Size may be declared on a sibling rule for the same element
        # (e.g. `.calc-plan .sdot` sets 8x8 while
        # `.calc-plan[data-plan="Power"] .sdot` only recolours it).
        last = rule.selector.split()[-1] if rule.selector.split() else ""
        classes = re.findall(r"\.([a-zA-Z0-9_-]+)", last)
        if classes and all(size_map.get(c, (999, 999))[0] <= TINY_PX
                           and size_map.get(c, (999, 999))[1] <= TINY_PX
                           for c in classes):
            return True
    return False


def build_size_map(rules):
    """class -> (width, height) from rules that declare both on that class."""
    size_map = {}
    for r in rules:
        w = re.search(r"(?<![a-z-])width\s*:\s*([0-9.]+)px", r.decl)
        h = re.search(r"(?<![a-z-])height\s*:\s*([0-9.]+)px", r.decl)
        if not (w and h):
            continue
        last = r.selector.split()[-1] if r.selector.split() else ""
        for c in re.findall(r"\.([a-zA-Z0-9_-]+)", last):
            size_map.setdefault(c, (float(w.group(1)), float(h.group(1))))
    return size_map


def rule_is_clip_text(rule):
    return "background-clip:text" in rule.decl.replace(" ", "")


# ------------------------------------------------------------ HTML handling
class Element:
    def __init__(self, tag, attrs, line, parent):
        self.tag = tag
        self.attrs = dict(attrs)
        self.line = line
        self.parent = parent
        self.children = []
        self.text = ""  # direct text

    def classes(self):
        return self.attrs.get("class", "").split()

    def ancestors(self):
        node, out = self.parent, []
        while node is not None:
            out.append(node)
            node = node.parent
        return out


class PageParser(HTMLParser):
    VOID = {"img", "br", "hr", "meta", "link", "input", "source"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Element("root", [], 0, None)
        self.stack = [self.root]
        self.elements = []
        self.style_blocks = []  # (text, start_line)
        self._in_style = None
        self._style_start = 0

    def handle_starttag(self, tag, attrs):
        line = self.getpos()[0]
        if tag == "style":
            self._in_style = []
            self._style_start = line
            return
        el = Element(tag, attrs, line, self.stack[-1])
        self.stack[-1].children.append(el)
        self.elements.append(el)
        if tag not in self.VOID:
            self.stack.append(el)

    def handle_endtag(self, tag):
        if tag == "style" and self._in_style is not None:
            self.style_blocks.append(("".join(self._in_style), self._style_start))
            self._in_style = None
            return
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        if self._in_style is not None:
            self._in_style.append(data)
            return
        if self.stack:
            self.stack[-1].text += data


def needle_has_real_transition(rules):
    """True when the WINNING .tn-tacho-needle rule (last in source order,
    the cascade winner at equal specificity) sets a real CSS transition.
    `transition:none` is the needle law itself — it does NOT count."""
    needle_rules = [r for r in rules if ".tn-tacho-needle" in r.selector]
    if not needle_rules:
        return False, None
    winner = needle_rules[-1]
    m = re.search(r"transition\s*:\s*([^;]+)", winner.decl)
    if m and m.group(1).strip().lower() not in ("none", "0", "0s"):
        return True, winner
    return False, winner


# ------------------------------------------------- calculator-gauge helpers
# (2026-11-09 gate fix — bug 3.) The pricing calculator's speedometer is
# a DIFFERENT component from the Dashboard needle-law gauge. A mount is a
# calculator gauge when any ancestor names the calculator (id="calculator",
# class calc-gauge / calc-body / calc-...). The Dashboard gauge has no
# calc ancestor, so the needle law still applies to it unchanged.
CALC_GOLD_HEXES = ("#ffbf3d", "#e8b64c", "#ffd45a", "#f5d76e", "#d9a521",
                    "#ffcf5c")


def gauge_is_calculator(mount_el):
    for a in mount_el.ancestors():
        hay = ((a.attrs.get("class") or "") + " " + (a.attrs.get("id") or "")).lower()
        if "calc" in hay:
            return True
    return False


def _element_full_text(el):
    """Direct text + all descendant text, whitespace-collapsed."""
    txt = " ".join(el.text.split())
    for d in _descendants(el):
        txt += " " + " ".join(d.text.split())
    return txt.strip()


def _part_bullet_text(board_el, part_cls):
    """Text of the bullets in a Ten part block, or None when the part
    block itself is absent. Empty string when the block exists but
    carries no bullets — a label alone is not a nutshell."""
    for d in [board_el] + _descendants(board_el):
        if part_cls in d.classes():
            bullets = []
            for x in _descendants(d):
                if x.tag == "li":
                    t = _element_full_text(x)
                    if t:
                        bullets.append(t)
            return " ".join(bullets)
    return None


def calc_gauge_subchecks(mount_el, elements, rules, text, custom_props):
    """The calculator gauge's own standard. Returns (failures, notes,
    counts): failures is a list of FAIL strings (empty = the gauge passes
    its standard). The four sub-checks:
      1. NUMBER ON TOP — a numeric amount element exists and is paired
         with the gauge: amount and mount share a gauge-block ancestor
         (class containing "gauge"). Visual above/below is the live
         verifier's job (screenshots); the static check is the pairing —
         DOM order alone would misfire here (the mount precedes the
         amount in source while the number renders above the dial).
      2. NEEDLE/DIAL ALIVE — the needle is built by script (some script
         mentions tn-tacho-needle) AND the calculator drives the mount
         when the amount changes (some script mentions both the mount id
         and calc-amount). A gauge with no JS wiring is dead, not alive.
      3. GOLD RIM INTACT — the calculator's gold token (--gold, a gold
         hex) is defined and is used by a calculator/tacho-scope rule
         (the gauge's number/readout wears it).
    """
    failures, notes, counts = [], [], {}
    # 1. number paired with the gauge
    amount_el = None
    for el in elements:
        if el.attrs.get("id") == "calc-amount" or "calc-amount" in el.classes():
            amount_el = el
            break
    if amount_el is None:
        for el in elements:
            if "calc-readout" in el.classes() and re.search(r"\d", _element_full_text(el)):
                amount_el = el
                break
    paired = False
    if amount_el is not None and re.search(r"\d", _element_full_text(amount_el)):
        mount_gauge_blocks = {id(a) for a in mount_el.ancestors()
                              if "gauge" in (a.attrs.get("class") or "").lower()}
        amount_gauge_blocks = {id(a) for a in amount_el.ancestors()
                               if "gauge" in (a.attrs.get("class") or "").lower()}
        paired = bool(mount_gauge_blocks & amount_gauge_blocks)
    counts["calc_number_paired"] = int(paired)
    if amount_el is None:
        failures.append("C-CALC NO NUMBER: no calc-amount / calc-readout element "
                        "with a digit — the gauge has no number on top")
    elif not paired:
        failures.append("C-CALC NUMBER NOT PAIRED: the amount element does not share "
                        "a gauge-block ancestor with the mount — number and gauge "
                        "are not one component")
    else:
        notes.append("C-CALC number on top: amount \"%s\" shares a gauge block with "
                     "the mount" % _element_full_text(amount_el)[:40])
    # 2. needle/dial alive — JS wiring
    scripts = re.findall(r"<script[^>]*>(.*?)</script>", text, re.S | re.I)
    needle_built = any("tn-tacho-needle" in s for s in scripts)
    driven = any("tn-tacho-mount" in s and "calc-amount" in s for s in scripts)
    counts["calc_needle_built_by_js"] = int(needle_built)
    counts["calc_driven_by_amount"] = int(driven)
    if not needle_built:
        failures.append("C-CALC DEAD NEEDLE: no script builds tn-tacho-needle — "
                        "the dial has no needle to move")
    if not driven:
        failures.append("C-CALC NOT DRIVEN: no script mentions both the mount id and "
                        "calc-amount — nothing moves the needle with the numbers")
    if needle_built and driven:
        notes.append("C-CALC needle/dial alive: needle built by script, calculator "
                     "drives the mount when the amount changes")
    # 3. gold rim intact
    gold = (custom_props.get("--gold") or "")
    gold_defined = any(h in gold.lower() for h in CALC_GOLD_HEXES)
    gold_used = False
    for r in rules:
        sel = r.selector.lower()
        if "calc" in sel or "tacho" in sel:
            if "var(--gold)" in r.decl or any(h in r.decl.lower() for h in CALC_GOLD_HEXES):
                gold_used = True
                break
    counts["calc_gold_defined"] = int(gold_defined)
    counts["calc_gold_used"] = int(gold_used)
    if not gold_defined:
        failures.append("C-CALC GOLD RIM MISSING: --gold is not defined as a gold "
                        "colour in the calculator scope")
    elif not gold_used:
        failures.append("C-CALC GOLD RIM MISSING: --gold is defined but no "
                        "calculator/tacho rule uses it — the gold is gone from "
                        "the gauge")
    else:
        notes.append("C-CALC gold rim intact: --gold=%s, used by the gauge's "
                     "number/readout" % gold.strip())
    return failures, notes, counts


# ------------------------------------------------------------------ checks
class GateResult:
    def __init__(self, letter, name):
        self.letter = letter
        self.name = name
        self.passed = True
        self.evidence = []  # strings
        self.counts = {}

    def fail(self, msg):
        self.passed = False
        self.evidence.append(msg)

    def note(self, msg):
        self.evidence.append(msg)


def rule_is_number_language(rule):
    sel = rule.selector.lower()
    return any(w in sel for w in NUMBER_LANGUAGE_WORDS)


def rule_is_active_state(rule):
    sel = rule.selector.lower()
    return any(w in sel for w in ACTIVE_STATE_WORDS)


def check_a(rules, custom_props):
    """(a) zero white/light backgrounds."""
    res = GateResult("a", "zero white/light backgrounds")
    base_lum = None
    for r in rules:
        for sel in [s.strip() for s in r.selector.split(",")]:
            # only the canvas itself: `body` / `html`, optionally with classes —
            # never a descendant (body.foo #bar is a board, not the canvas)
            if not re.match(r"^(body|html)([.#:\[][^\s]*)?$", sel):
                continue
            for prop in ("background-color", "background"):
                m = re.search(r"%s\s*:\s*([^;]+)" % prop, r.decl)
                if m:
                    val = m.group(1).strip()
                    lum = resolve_bg_lum(val, custom_props)
                    if lum is not None:
                        base_lum = lum
                        res.note("base canvas %s = %s (luminance %.2f) at %s"
                                 % (sel, val.split()[0], lum, r.loc()))
    if base_lum is None:
        res.fail("A1 NO DARK BASE CANVAS: no body/html rule sets a dark background — "
                 "the browser default white canvas shows through (the fix-12 defect: "
                 "chart cells sit on white)")
    elif base_lum > DARK_CANVAS_LUM:
        res.fail("A1 LIGHT BASE CANVAS: body/html background luminance %.2f > %.2f"
                 % (base_lum, DARK_CANVAS_LUM))
    else:
        res.counts["base_canvas_lum"] = round(base_lum, 3)

    solid_hits, grad_hits = [], []
    size_map = build_size_map(rules)
    for r in rules:
        if (rule_is_pseudo(r) or rule_is_clip_text(r) or rule_is_tiny(r, size_map)
                or rule_is_number_language(r) or rule_is_active_state(r)):
            continue
        for prop in ("background-color", "background"):
            for m in re.finditer(r"%s\s*:\s*([^;}{]+)" % prop, r.decl):
                val = m.group(1).strip()
                if "gradient(" in val:
                    cov = gradient_light_coverage(val)
                    if cov is not None and cov >= GRADIENT_LIGHT_COVERAGE:
                        grad_hits.append("%s — light gradient covers %.0f%% of span "
                                         "at %s" % (r.selector, cov * 100, r.loc()))
                    continue
                light = effective_lightness_from_value(val, custom_props)
                if light is not None and light >= LIGHTNESS:
                    solid_hits.append("%s — %s (lightness %.2f) at %s"
                                      % (r.selector, val.split()[0], light, r.loc()))
    # inline style attributes are checked by the caller via extra rules
    for h in solid_hits[:10]:
        res.fail("A2 SOLID LIGHT SURFACE: " + h)
    for h in grad_hits[:10]:
        res.fail("A3 LIGHT GRADIENT SURFACE: " + h)
    res.counts["solid_light_surfaces"] = len(solid_hits)
    res.counts["light_gradient_surfaces"] = len(grad_hits)
    if not solid_hits and not grad_hits:
        res.note("no solid light surfaces and no light-gradient surfaces "
                 "(exempted by threshold: pseudo-element highlights, <= %dpx "
                 "dots/knobs, background-clip:text, number language, active-state "
                 "inversions)" % TINY_PX)
    return res


def _first_color_token(value):
    """First real colour in a background value: a hex/rgba token first
    (a gradient's first stop); a named colour only if no hex/rgba exists.
    Bare words like 'linear'/'radial'/'gradient' are function names, not
    colours, and must never be read as one."""
    m = re.search(r"(#[0-9a-fA-F]{3,8}|rgba?\([^)]*\))", value)
    if m:
        return m.group(1)
    m = re.search(r"\b([a-z]+)\b", value)
    return m.group(1) if m else None


def resolve_bg_lum(value, custom_props):
    """Luminance of a background shorthand's first colour, or None."""
    value = value.strip()
    if value.startswith("var("):
        m = re.match(r"var\(\s*(--[a-zA-Z0-9_-]+)", value)
        if m and m.group(1) in custom_props:
            return resolve_bg_lum(custom_props[m.group(1)], custom_props)
        return None
    tok = _first_color_token(value)
    if not tok:
        return None
    return effective_lum(tok)


def effective_lightness_from_value(value, custom_props):
    """HSL lightness of a background shorthand's first colour, or None."""
    value = value.strip()
    if value.startswith("var("):
        m = re.match(r"var\(\s*(--[a-zA-Z0-9_-]+)", value)
        if m and m.group(1) in custom_props:
            return effective_lightness_from_value(custom_props[m.group(1)], custom_props)
        return None
    tok = _first_color_token(value)
    if not tok:
        return None
    return effective_lightness(tok)


def check_b(elements, rules):
    """(b) every element raised/elevated."""
    res = GateResult("b", "every element raised/elevated")
    depth_rules = [r for r in rules
                   if re.search(r"box-shadow\s*:\s*(?!none\b)([^;]+)", r.decl)]

    def has_depth(el):
        toks = set()
        for c in el.classes():
            toks.add("." + c)
        if el.attrs.get("id"):
            toks.add("#" + el.attrs["id"])
        for k in el.attrs:
            if k.startswith("data-"):
                toks.add("[" + k)
        toks.add(el.tag)
        for r in depth_rules:
            sel = r.selector.lower()
            if any(t.lower() in sel for t in toks):
                return True
        return False

    scope = []
    for el in elements:
        if el.tag == "button":
            scope.append(el)
        elif el.tag == "a" and any(any(w in c.lower() for w in BUTTON_LIKE_WORDS)
                                   for c in el.classes()):
            scope.append(el)
        elif any(any(w in c.lower() for w in
                     ("card", "board", "pill", "jewel", "orb", "panel", "strip",
                      "badge", "tab", "tile", "note", "item", "cell", "pop",
                      "modal", "detail"))
                 for c in el.classes()):
            scope.append(el)
    missing = [el for el in scope if not has_depth(el)]
    res.counts["elements_in_scope"] = len(scope)
    res.counts["elements_with_depth"] = len(scope) - len(missing)
    res.counts["elements_missing_depth"] = len(missing)
    if scope:
        ratio = (len(scope) - len(missing)) / len(scope)
        res.counts["depth_ratio"] = round(ratio, 3)
        if ratio < DEPTH_PASS_RATIO:
            res.fail("only %.0f%% of %d in-scope elements carry a box-shadow "
                     "(need >= %.0f%%)" % (ratio * 100, len(scope), DEPTH_PASS_RATIO * 100))
    for el in missing[:15]:
        msg = ("NO DEPTH: <%s class=\"%s\"> line %d"
               % (el.tag, " ".join(el.classes())[:60], el.line))
        if res.passed:
            res.note(msg)
        else:
            res.fail(msg)
    if not missing:
        res.note("all %d in-scope elements carry a box-shadow" % len(scope))
    return res


def check_c(text, elements, rules, custom_props=None):
    """(c) gauges present and alive. Two kinds, two standards (2026-11-09
    gate fix): a mount inside calculator context is the calculator gauge
    (its own standard — number, pairing, aliveness, gold rim); a mount
    anywhere else is the Dashboard needle-law gauge (mount + needle in
    DOM, no CSS transition on the winning needle rule, >= 2 gear teeth).
    Every mount must pass its own standard. Pages with no gauge pass on
    the fallback only when live numbers are present."""
    res = GateResult("c", "gauges present and alive")
    mounts = [el for el in elements if el.attrs.get("id") == "tn-tacho-mount"]
    needle_dom = any("tn-tacho-needle" in el.classes() for el in elements)
    needle_css = any("tn-tacho-needle" in r.selector for r in rules)
    teeth = text.count("tn-gear-tooth")
    needle_transition, needle_rule = needle_has_real_transition(rules)
    tiled = len(re.findall(r"svgnum|tiled-digit|digit-tile|ct-reel|num-tile", text, re.I))
    orb_nums = sum(1 for el in elements
                   if any("orb" in c.lower() for c in el.classes())
                   and re.search(r"\d", el.text))
    res.counts.update({
        "tn_tacho_mount_in_dom": len(mounts),
        "tn_tacho_needle_in_dom": int(needle_dom),
        "tn_tacho_needle_in_css": int(needle_css),
        "tn_gear_tooth_occurrences": teeth,
        "needle_css_has_transition": int(needle_transition),
        "tiled_digit_occurrences": tiled,
        "orb_numerals": orb_nums,
    })
    if mounts:
        calc_mounts = [m for m in mounts if gauge_is_calculator(m)]
        needle_mounts = [m for m in mounts if not gauge_is_calculator(m)]
        res.counts["calc_gauges"] = len(calc_mounts)
        res.counts["needle_law_gauges"] = len(needle_mounts)
        if needle_mounts:
            # Needle-law path: unchanged semantics — evaluated only when a
            # needle exists (DOM or CSS); a needle-less mount falls back
            # to live numbers, exactly as before.
            if needle_dom or needle_css:
                res.note("needle-law gauge present: #tn-tacho-mount in DOM, needle %s, "
                         "%d gear-tooth occurrence(s)"
                         % ("in DOM" if needle_dom else "in CSS only", teeth))
                if needle_transition:
                    res.fail("C NEEDLE LAW BROKEN: .tn-tacho-needle carries a CSS transition "
                             "(%s) — rAF must own the motion, no CSS transition" % needle_rule.loc())
                if teeth < 2:
                    res.fail("C GEAR TEETH MISSING: only %d tn-gear-tooth occurrence(s) — "
                             "the harvested gauge has 246 teeth; this gauge is not the "
                             "harvested one" % teeth)
            elif tiled > 0 or orb_nums > 0:
                res.note("needle-law mount with no needle; live numbers present "
                         "instead: %d tiled-digit occurrence(s), %d orb numeral(s)"
                         % (tiled, orb_nums))
            else:
                res.fail("C NO GAUGE, NO LIVE NUMBERS: #tn-tacho-mount with no needle "
                         "and no tiled digits / orb numerals — the numbers are plain text")
        for m in calc_mounts:
            res.note("calculator gauge present: #tn-tacho-mount inside calculator "
                     "context (line %d) — measured against the calculator standard, "
                     "not the needle law" % m.line)
            failures, notes, cc = calc_gauge_subchecks(
                m, elements, rules, text, custom_props or {})
            res.counts.update(cc)
            for n in notes:
                res.note(n)
            for f in failures:
                res.fail(f)
    elif tiled > 0 or orb_nums > 0:
        res.note("no needle-law gauge; live numbers present instead: %d tiled-digit "
                 "occurrence(s), %d orb numeral(s)" % (tiled, orb_nums))
    else:
        res.fail("C NO GAUGE, NO LIVE NUMBERS: no #tn-tacho-mount / .tn-tacho-needle "
                 "and no tiled digits / orb numerals — the numbers are plain text")
    return res


def check_d(elements, text):
    """(d) no text-in-image, no pasted document. A data:image/ payload is
    opaque binary — base64 noise contains random "doc"/"list" substrings
    (2026-11-09 gate fix: the 8 Naya faces + orbs were 23 false
    positives) — so the payload bytes are never scanned for text
    signals. The alt text of a data-URI image IS still scanned, and
    file/URL images are scanned on src + alt as before."""
    res = GateResult("d", "no text-in-image, no pasted document")
    hits = 0
    data_uri_excluded = 0
    for el in elements:
        if el.tag == "img":
            src = el.attrs.get("src", "")
            alt = el.attrs.get("alt", "")
            if src.lower().startswith("data:image/"):
                # Opaque binary payload — the base64 itself signals
                # nothing. Only the human-written alt text can signal
                # text content (e.g. alt="Top 10 chart screenshot").
                data_uri_excluded += 1
                hay = alt.lower()
            else:
                hay = (src + " " + alt).lower()
            words = [w for w in TEXT_IMG_WORDS if w in hay]
            if words:
                hits += 1
                res.fail("TEXT-IN-IMAGE: <img src=\"%s\" alt=\"%s\"> line %d "
                         "(signals: %s)" % (src[:80],
                                            alt[:80], el.line,
                                            ", ".join(words)))
        elif el.tag in ("iframe", "embed", "object"):
            src = el.attrs.get("src", el.attrs.get("data", "")).lower()
            if any(w in src for w in ("docs.google", "drive.google", ".pdf", "document")):
                hits += 1
                res.fail("PASTED DOCUMENT: <%s src=\"%s\"> line %d"
                         % (el.tag, src[:100], el.line))
        elif el.tag == "figure":
            cap = " ".join(c.text for c in el.children if c.tag == "figcaption").lower()
            if "screenshot" in cap:
                hits += 1
                res.fail("SCREENSHOT FIGURE: <figure> line %d (caption: %s)"
                         % (el.line, cap[:100]))
    res.counts["text_in_image_hits"] = hits
    res.counts["img_count"] = sum(1 for el in elements if el.tag == "img")
    res.counts["data_uri_images_excluded"] = data_uri_excluded
    if data_uri_excluded:
        res.note("%d data-URI image payload(s) excluded from the src scan "
                 "(opaque binary — no text signal); alt text still scanned"
                 % data_uri_excluded)
    if not hits:
        res.note("%d <img> element(s), none signalling text content; no document embeds"
                 % res.counts["img_count"])
    return res


def check_e(elements):
    """(e) no bare text blocks."""
    res = GateResult("e", "no bare text blocks")
    skip_tags = {"button", "a", "nav", "script", "style", "head", "template",
                 "title", "option", "noscript"}
    blocks, bare = [], []
    for el in elements:
        if el.tag not in ("p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "td", "div", "span"):
            continue
        txt = " ".join(el.text.split())
        if len(txt) < TEXT_MIN_LEN:
            continue
        chain = [el] + el.ancestors()
        if any(a.tag in skip_tags for a in chain[1:]):
            continue
        blocks.append((el, txt))
        contained = any(any(is_container_class(c) for c in a.classes())
                        for a in chain)
        if not contained:
            bare.append((el, txt))
    res.counts["substantial_text_blocks"] = len(blocks)
    res.counts["bare_text_blocks"] = len(bare)
    if blocks:
        ratio = (len(blocks) - len(bare)) / len(blocks)
        res.counts["contained_ratio"] = round(ratio, 3)
        if ratio < CONTAINED_PASS_RATIO:
            res.fail("only %.0f%% of %d substantial text blocks live in a board/pill/"
                     "jewel/orb container (need >= %.0f%%)"
                     % (ratio * 100, len(blocks), CONTAINED_PASS_RATIO * 100))
    for el, txt in bare[:15]:
        msg = ("BARE TEXT: <%s> line %d — \"%s…\""
               % (el.tag, el.line, txt[:70]))
        if res.passed:
            res.note(msg)
        else:
            res.fail(msg)
    if not bare:
        res.note("all %d substantial text blocks live in a container" % len(blocks))
    return res


def check_f(elements, rules, text):
    """(f) no look-alike buttons/gauges/numbers (addendum 16:41Z)."""
    res = GateResult("f", "no look-alike buttons/gauges/numbers")
    lookalikes, gold_ctas, attr_addressed = [], [], 0

    def pedigree(el):
        """Return 'harvested', 'attribute', or the offending class list.

        An id/data-* address excuses a button ONLY when it carries no
        meaningful class at all (the Dashboard's classless tab/back buttons).
        A button WITH a custom non-allowlisted class is a look-alike even
        when it also has a data-* hook — the hook is wiring, not pedigree.
        """
        meaningful = [c for c in el.classes() if c not in STATE_CLASSES]
        if any(is_harvested(c) for c in meaningful):
            return "harvested"
        if meaningful:
            return meaningful
        if el.attrs.get("id") or any(k.startswith("data-") for k in el.attrs):
            return "attribute"
        return "bare"

    for el in elements:
        is_button = el.tag == "button"
        is_cta_link = (el.tag == "a" and any(any(w in c.lower() for w in BUTTON_LIKE_WORDS)
                                              for c in el.classes()))
        if not (is_button or is_cta_link):
            continue
        p = pedigree(el)
        if p == "attribute":
            attr_addressed += 1
        elif p == "bare":
            lookalikes.append("<%s> line %d — no class, no id, no data-* (unaddressed)"
                              % (el.tag, el.line))
        elif p != "harvested":
            lookalikes.append("<%s class=\"%s\"> line %d — class(es) %s not on the "
                              "harvest allowlist and no named harvest source"
                              % (el.tag, " ".join(el.classes())[:50], el.line, p))
        if any(t in el.classes() for t in YELLOW_TOKENS):
            gold_ctas.append("<%s class=\"%s\"> line %d — gold-theme CTA "
                             "(the condemned yellow button wore `primo theme-gold`)"
                             % (el.tag, " ".join(el.classes())[:50], el.line))
        style = el.attrs.get("style", "")
        if re.search(r"background\s*:\s*#[fF][fF][dD]|background\s*:\s*#ffbf3d|"
                     r"background\s*:\s*#f5d76e", style):
            gold_ctas.append("<%s> line %d — inline yellow/gold background"
                             % (el.tag, el.line))
    res.counts["lookalike_buttons"] = len(lookalikes)
    res.counts["gold_theme_ctas"] = len(gold_ctas)
    res.counts["attribute_addressed_controls"] = attr_addressed
    for h in lookalikes[:15]:
        res.fail("F1 LOOK-ALIKE BUTTON: " + h)
    for h in gold_ctas[:15]:
        res.fail("F2 GOLD-THEME CTA: " + h)
    if not lookalikes and not gold_ctas:
        res.note("every button/CTA traces to a harvested class, a harvested "
                 "family prefix, or an id/data-* address (%d attribute-addressed)"
                 % attr_addressed)
    # F3 needle law (gauge must be the harvested gauge, not a look-alike).
    # Calculator gauges are exempt (2026-11-09 gate fix): a mount inside
    # calculator context is the pricing speedometer, not the Dashboard
    # needle-law gauge — its aliveness is measured by (c)'s calculator
    # standard, and a dead calculator gauge still FAILs (c).
    mount = any(el.attrs.get("id") == "tn-tacho-mount" for el in elements)
    if mount:
        mounts = [el for el in elements if el.attrs.get("id") == "tn-tacho-mount"]
        if mounts and all(gauge_is_calculator(m) for m in mounts):
            res.note("F3 needle law skipped: every gauge mount is a calculator "
                     "gauge — aliveness is measured by (c)'s calculator standard")
        else:
            has_trans, needle_rule = needle_has_real_transition(rules)
            if has_trans:
                res.fail("F3 FAKE GAUGE: .tn-tacho-needle carries a CSS transition (%s) — "
                         "the harvested needle has NO transition; rAF owns the motion"
                         % needle_rule.loc())
            if text.count("tn-gear-tooth") < 2:
                res.fail("F3 FAKE GAUGE: only %d tn-gear-tooth occurrence(s) — the "
                         "harvested gauge has 246 teeth" % text.count("tn-gear-tooth"))
    # F4 numbers — evidence only (static source cannot prove the digits render
    # as the harvested tiles; that is his eye's call)
    tiled = len(re.findall(r"svgnum|tiled-digit|digit-tile|ct-reel|num-tile", text, re.I))
    res.counts["tiled_digit_occurrences"] = tiled
    res.note("F4 numbers (evidence only): %d tiled-digit/svgnum occurrence(s); "
             "whether they render as the harvested tiles is a live-eye check, "
             "not a static one" % tiled)
    return res


def _descendants(el):
    out = []
    for c in el.children:
        out.append(c)
        out.extend(_descendants(c))
    return out


def _class_text(el, cls):
    """Text of the first element (self or descendant) carrying class cls,
    else None. Empty string when the element exists but holds no text."""
    for d in [el] + _descendants(el):
        if cls in d.classes():
            txt = " ".join(d.text.split())
            for x in _descendants(d):
                txt += " " + " ".join(x.text.split())
            return txt.strip()
    return None


def check_g_note(text):
    """(g) note format — the note must give the feed parser ## sections to find.

    FAILS when the note carries NO ## sections at all, or when its sections
    are defined by bold-inline labels (**Hook:** ...) with zero ## headings
    (the defect that kept five notes out of the feed in one night).
    Bold-inline labels QUOTED as examples alongside real ## sections are
    reported, not failed — the note parses, and SN-2444 itself quotes the
    bad format while carrying 9 ## headings."""
    res = GateResult("g", "note format — ## sections, never bold-inline labels")
    labels = "|".join(NOTE_SECTION_LABELS)
    pat = re.compile(r"\*\*\s*(%s)\s*:\s*\*\*|\*\*\s*(%s)\s*\*\*\s*:"
                     % (labels, labels), re.I)
    hits = 0
    hit_lines = []
    headings = 0
    for ln, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("## "):
            headings += 1
        m = pat.search(line)
        if m:
            hits += 1
            hit_lines.append(ln)
    res.counts["bold_inline_labels"] = hits
    res.counts["hash_hash_headings"] = headings
    if headings == 0:
        res.fail("NO ## SECTIONS: the note carries zero ## headings — the feed "
                 "parser finds no sections, so this note never lands "
                 "(bold-inline labels found: %d)" % hits)
    elif hits:
        res.note("%d bold-inline label(s) quoted alongside %d ## headings "
                 "(lines %s) — verify they are examples, not section "
                 "definitions; the note parses"
                 % (hits, headings, ", ".join(str(x) for x in hit_lines[:10])))
    if not res.evidence:
        res.note("%d ## heading(s), zero bold-inline section labels — the note parses"
                 % headings)
    return res


def check_h(text):
    """(h) no dictation-blunt phrases in page copy."""
    res = GateResult("h", "no dictation-blunt phrases in page copy")
    hits = 0
    for phrase, why in BANNED_BLUNT_PHRASES:
        for ln, line in enumerate(text.splitlines(), 1):
            if phrase in line.lower():
                hits += 1
                if hits <= 10:
                    res.fail("BLUNT DICTATION PHRASE: line %d — \"%s\" (%s)"
                             % (ln, phrase, why))
    res.counts["banned_blunt_phrases"] = hits
    if not hits:
        res.note("none of the banned blunt phrases (%s) appear in the page"
                 % ", ".join(p for p, _ in BANNED_BLUNT_PHRASES))
    return res


def check_i(elements):
    """(i) title + subtitle + nutshell + faces alternate."""
    res = GateResult("i", "title + subtitle + nutshell + faces alternate")
    boards = [el for el in elements if "calc-story-card" in el.classes()]
    res.counts["story_boards"] = len(boards)
    if not boards:
        res.note("no story boards (.calc-story-card) on this page — (i) not applicable")
        return res
    missing = 0
    ten_count = 0
    for idx, b in enumerate(boards, 1):
        # The Ten is the same family in a different shape (2026-11-09 gate
        # fix): a board carrying .ult-card / .ult-part is a TEN board —
        # title + three parts (why / solution / nutshell, each with at
        # least one real bullet) + who line — NOT title + subtitle +
        # nutshell. A Ten missing its nutshell FAILS (i) exactly as a
        # hired board missing .board-nut does. Side alternation and face
        # distinctness below still apply to Ten boards unchanged.
        is_ten = "ult-card" in b.classes() or any(
            "ult-part" in d.classes() for d in _descendants(b))
        if is_ten:
            ten_count += 1
            title = _class_text(b, "board-title")
            if title is None:
                missing += 1
                res.fail("TEN BOARD %d MISSING .board-title — line %d" % (idx, b.line))
            elif not title:
                missing += 1
                res.fail("TEN BOARD %d EMPTY .board-title — line %d" % (idx, b.line))
            for part_cls, part_name in (("ult-part-why", "why"),
                                        ("ult-part-sol", "solution"),
                                        ("ult-part-nut", "nutshell")):
                part_txt = _part_bullet_text(b, part_cls)
                if part_txt is None:
                    missing += 1
                    res.fail("TEN BOARD %d MISSING .%s (%s) — line %d"
                             % (idx, part_cls, part_name, b.line))
                elif not part_txt:
                    missing += 1
                    res.fail("TEN BOARD %d EMPTY .%s (%s) — line %d"
                             % (idx, part_cls, part_name, b.line))
            who = _class_text(b, "ult-who")
            if who is None:
                missing += 1
                res.fail("TEN BOARD %d MISSING .ult-who (who line) — line %d"
                         % (idx, b.line))
            elif not who:
                missing += 1
                res.fail("TEN BOARD %d EMPTY .ult-who (who line) — line %d"
                         % (idx, b.line))
        else:
            for cls in ("board-title", "board-sub", "board-nut"):
                txt = _class_text(b, cls)
                if txt is None:
                    missing += 1
                    res.fail("BOARD %d MISSING .%s — line %d" % (idx, cls, b.line))
                elif not txt:
                    missing += 1
                    res.fail("BOARD %d EMPTY .%s — line %d" % (idx, cls, b.line))
    res.counts["ten_boards"] = ten_count
    if ten_count:
        res.note("%d Ten board(s) detected (.ult-card / .ult-part shape: title + "
                 "why / solution / nutshell + who line)"
                 % ten_count)
    res.counts["boards_missing_a_part"] = missing
    sides, face_hashes = [], []
    for b in boards:
        cls = b.classes()
        sides.append("left" if "face-left" in cls
                     else ("right" if "face-right" in cls else "?"))
        src = None
        for d in _descendants(b):
            if "board-face" in d.classes():
                for x in _descendants(d):
                    if x.tag == "img" and x.attrs.get("src"):
                        src = x.attrs["src"]
                        break
                if src:
                    break
        face_hashes.append(hashlib.sha256(src.encode("utf-8", "ignore")).hexdigest()[:12]
                           if src else None)
    res.counts["board_sides_dom_order"] = ",".join(sides)
    res.counts["boards_with_a_face"] = sum(1 for h in face_hashes if h)
    res.counts["distinct_faces"] = len({h for h in face_hashes if h})
    for i in range(1, len(sides)):
        if sides[i] == sides[i - 1] and sides[i] != "?":
            res.fail("FACE SIDES NOT ALTERNATING: board %d and board %d are both %s — "
                     "the switch resets attention; same side twice in a row breaks it"
                     % (i, i + 1, sides[i]))
    seen = [h for h in face_hashes if h]
    if len(set(seen)) < len(seen):
        res.fail("REPEATED FACE: two boards carry the same face image — "
                 "every board gets a different face")
    for j, h in enumerate(face_hashes, 1):
        if h is None:
            res.fail("BOARD %d HAS NO FACE IMAGE — Naya speaks the boards; every "
                     "board carries her face" % j)
    if res.passed:
        res.note("%d story boards (%d Ten-shaped, %d hired-shaped), each with its "
                 "required parts; sides %s; %d distinct faces"
                 % (len(boards), ten_count, len(boards) - ten_count,
                    "".join(s[0].upper() for s in sides),
                    len({h for h in face_hashes if h})))
    return res


def image_provenance(elements):
    """INFO only — not a gate item. Lists every image so provenance can be judged."""
    out = []
    for el in elements:
        if el.tag == "img":
            out.append("line %d: src=\"%s\" alt=\"%s\""
                       % (el.line, el.attrs.get("src", "")[:110],
                          el.attrs.get("alt", "")[:80]))
    return out


# --------------------------------------------------------------------- main
def check_file(path):
    path = Path(path)
    text = path.read_text(encoding="utf-8", errors="ignore")
    parser = PageParser()
    parser.feed(text)
    elements = parser.elements

    rules = []
    custom_props = {}
    for css, start_line in parser.style_blocks:
        rules.extend(parse_css_rules(css, start_line, "inline <style>"))
    for el in elements:
        if el.attrs.get("style"):
            fake = ".inline-style{%s}" % el.attrs["style"]
            rules.extend(parse_css_rules(fake, el.line, "style attribute line %d" % el.line))
    for el in elements:
        if el.tag == "link" and el.attrs.get("rel") == "stylesheet":
            href = el.attrs.get("href", "")
            if href and not href.startswith(("http://", "https://", "//", "data:")):
                css_path = (path.parent / href).resolve()
                if css_path.is_file():
                    css = css_path.read_text(encoding="utf-8", errors="ignore")
                    rules.extend(parse_css_rules(css, 1, str(css_path)))
    for r in rules:
        for m in re.finditer(r"(--[a-zA-Z0-9_-]+)\s*:\s*([^;]+);", r.decl):
            custom_props.setdefault(m.group(1), m.group(2).strip())

    results = [
        check_a(rules, custom_props),
        check_b(elements, rules),
        check_c(text, elements, rules, custom_props),
        check_d(elements, text),
        check_e(elements),
        check_f(elements, rules, text),
        check_h(text),
        check_i(elements),
    ]
    return results, image_provenance(elements)


def read_human_attestations(path):
    """Parse --human-checks FILE: lines 'H1: PASS — <evidence>' / 'H1: FAIL — <reason>'.
    Returns dict id -> (verdict, evidence)."""
    out = {}
    for line in Path(path).read_text(encoding="utf-8", errors="ignore").splitlines():
        m = re.match(r"\s*(H[1-5])\s*:\s*(PASS|FAIL)\b\s*[—\-]?\s*(.*)$", line, re.I)
        if m:
            out[m.group(1).upper()] = (m.group(2).upper(), m.group(3).strip())
    return out


def print_human_checks(attestations):
    """Print the H1–H5 block. Returns True only when every check is attested PASS.

    attestations None = no --human-checks file: every check prints PENDING.
    A gate that isn't run is not a pass — the verdict line says so."""
    print("\nHUMAN CHECKS (H1–H5) — what the machine cannot check; the seat runs")
    print("these and reports them in the handoff. A gate that isn't run is not a pass.")
    all_pass = True
    for hid, name, instruction in HUMAN_CHECKS:
        if attestations is None:
            print("      %s %s — PENDING: %s" % (hid, name, instruction))
            all_pass = False
        elif hid not in attestations:
            print("      %s %s — NOT ATTESTED (no %s line in the --human-checks file)"
                  % (hid, name, hid))
            all_pass = False
        else:
            verdict, ev = attestations[hid]
            print("      %s %s — %s%s" % (hid, name, verdict,
                                           (" — " + ev) if ev else ""))
            if verdict != "PASS":
                all_pass = False
    return all_pass


def main(argv):
    args = list(argv[1:])
    attestations = None
    if "--human-checks" in args:
        i = args.index("--human-checks")
        if i + 1 >= len(args):
            print("usage: check-gate.py [--human-checks FILE] <page.html|note.md> [more...]")
            return 2
        try:
            attestations = read_human_attestations(args[i + 1])
        except FileNotFoundError:
            print("ERROR: --human-checks file not found: %s" % args[i + 1])
            return 2
        del args[i:i + 2]
    if not args:
        print("usage: check-gate.py [--human-checks FILE] <page.html|note.md> [more...]")
        return 2
    overall_fail = False
    for fname in args:
        print("=" * 72)
        print("GATE: %s" % fname)
        print("=" * 72)
        if fname.lower().endswith(".md"):
            try:
                text = Path(fname).read_text(encoding="utf-8", errors="ignore")
            except FileNotFoundError:
                print("ERROR: file not found: %s" % fname)
                overall_fail = True
                continue
            results = [check_g_note(text)]
            for r in results:
                verdict = "PASS" if r.passed else "FAIL"
                print("\n(%s) %s — %s" % (r.letter, r.name, verdict))
                if r.counts:
                    print("      counts: " + ", ".join("%s=%s" % kv for kv in r.counts.items()))
                for ev in r.evidence:
                    print("      - " + ev)
                if not r.passed:
                    overall_fail = True
            print("\nHUMAN CHECKS: not applicable to note files — H1–H5 are page-copy")
            print("checks, run per build and reported in the handoff.")
            verdict = "FAIL" if any(not r.passed for r in results) else "PASS"
            print("\nOVERALL: %s — %s" % (verdict, fname))
            continue
        try:
            results, images = check_file(fname)
        except FileNotFoundError:
            print("ERROR: file not found: %s" % fname)
            overall_fail = True
            continue
        for r in results:
            verdict = "PASS" if r.passed else "FAIL"
            print("\n(%s) %s — %s" % (r.letter, r.name, verdict))
            if r.counts:
                print("      counts: " + ", ".join("%s=%s" % kv for kv in r.counts.items()))
            for ev in r.evidence:
                print("      - " + ev)
            if not r.passed:
                overall_fail = True
        print("\nINFO — image provenance (Law 14 matter, NOT a gate item):")
        if images:
            for img in images:
                print("      - " + img)
        else:
            print("      - no <img> elements")
        machine_ok = all(r.passed for r in results)
        human_ok = print_human_checks(attestations)
        if not machine_ok:
            verdict = "FAIL"
        elif attestations is None:
            verdict = "PASS — MACHINE ONLY, HUMAN CHECKS PENDING"
        elif human_ok:
            verdict = "PASS"
        else:
            verdict = "FAIL — HUMAN CHECKS NOT ALL PASS"
            overall_fail = True
        print("\nOVERALL: %s — %s" % (verdict, fname))
    return 1 if overall_fail else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
