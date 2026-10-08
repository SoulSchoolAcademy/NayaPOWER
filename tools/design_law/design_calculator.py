#!/usr/bin/env python3
"""
design_calculator.py — The Naya Design Calculator.

Scores any HTML output 0-100 against the Naya design standard.
"The taste becomes computable."

This is the diploma: when a Naya's output scores elite on the calculator
without anyone looking, she's graduated.

Layers:
  1. Mechanical: reuses tools/design_law/check_design.py (the executable checker).
  2. Judgment: Shawn-directive overrides the raw checker gets wrong —
     richened token variants are sanctioned, white buttons at rest are law,
     gold/yellow tokens are not "amber violations", CSS variables resolve.
  3. Rubric: seven categories scored against the 100-point Elite Interface
     Playbook as interpreted through Shawn's standing brief (dark system).

Usage:
    python3 design_calculator.py <file.html> [--room mail] [--json] [--gate [N]]

Exit: 0 normally; with --gate, 1 when score < threshold (default 90).
Stdlib only.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_design as CD  # noqa: E402  (the mechanical checker)

# --------------------------------------------------------------------------
# Shawn's sanctioned extensions to the token set.
# His 2026-10-08 directives: "make them richer" (richened spectrum) and
# "buttons should be white" (white pearl at rest). The raw checker flags
# these; the calculator sanctions them because Shawn spoke them.
# --------------------------------------------------------------------------
RICHENED_TOKENS = {
    "#e84fff",  # magenta, richened per Shawn
    "#a06bff",  # purple, richened
    "#3fb8ff",  # blue, richened
    "#2fe89e",  # green, richened
    "#ffbf3d",  # gold, richened
    # v1.5 exemplar near-token variants (Naya 4's shipped ground truth)
    "#ed42c4",  # magenta variant
    "#35e39b",  # emerald variant
    "#e8c766",  # gold variant
    "#ffd45a",  # yellow variant
}
CALC_TOKENS = set(CD.TOKEN_HEXES) | RICHENED_TOKENS

# Spectrum flow anchors for order analysis (Shawn's law:
# magenta -> purple -> blue -> green -> gold, cycling to magenta).
FLOW_ANCHORS = [
    ("magenta", "#d86cff"),
    ("purple", "#9d75ff"),
    ("blue", "#55b9ee"),
    ("green", "#55e39a"),
    ("gold", "#e8b64c"),
]
ANCHOR_HUES = [(name, CD.rgb_to_hsl(CD.hex_to_rgb(h))[0]) for name, h in FLOW_ANCHORS]

# Brand voice phrases (contract language_law). Presence = the page speaks Naya.
BRAND_PHRASES = [
    "black ground", "white light", "purple soul",
    "proof, not promises", "a claim without verification",
    "your intelligence", "in a nutshell",
    "quiet at rest", "flat is dead",
    "jewels, not dots", "the details are the design",
    "private by default", "shared by choice", "collective by consent",
    "one intelligence", "many views", "one identity",
    "black hearts", "white voices", "visible skin",
]
NAV_MARKERS = ["rooms", "smart feed", "smart mail", "intelligent library"]

# Words that are technical machinery, never human prose (Shawn: human-child-first).
JARGON = [
    "idempotency", "idempotent", "subagent", "harness", "worktree",
    "pre-ship", "preship", "surrogate", "instantiation", "nonce",
    "middleware", "deserialize", "recursion",
]
# Button selector pattern: broader than the checker's — catches .cx-btn,
# .living-btn, .sp-cta and friends, not just bare .btn.
BTN_SEL_RE = re.compile(
    r"(^|[\s>+~,])(button|\.?[\w-]*btn\b|\.?[\w-]*cta\b|\.primary\b|a\.btn|input\[type=['\"]?(submit|button)['\"]?\])"
    r"|\[role=['\"]?button['\"]?\]", re.I)
# Selectors demonstrating drift (what-NOT-to-do specimens) are exempt from
# color checks — flagging the lesson as a violation is wrong.
DRIFT_RE = re.compile(r"drift|dread|\bbad\b|dont|anti|wrong|before|specimen-bad", re.I)
# SCREAMING_CASE terms Shawn himself sanctioned (navigation/motto language).
SANCTIONED_SCREAMING = {
    "ROOMS", "PRIVATE", "BY", "DEFAULT", "SHARED", "CHOICE",
    "COLLECTIVE", "CONSENT", "IN", "A", "NUTSHELL", "ONE",
    "INTELLIGENCE", "MANY", "VIEWS", "IDENTITY",
}

CATEGORIES = [
    ("spectrum_law", "Spectrum Law", 20),
    ("color_identity", "Color Identity", 15),
    ("buttons_dimensional", "Buttons / Dimensional", 20),
    ("typography", "Typography", 10),
    ("truth_language", "Truth Language", 15),
    ("details", "Details", 10),
    ("voice", "Voice", 10),
]
CAT_MAX = dict((c[0], c[2]) for c in CATEGORIES)


# ---------------------------------------------------------------- helpers --
def hue_of(h):
    return CD.rgb_to_hsl(CD.hex_to_rgb(h))[0]


def sat_of(h):
    return CD.rgb_to_hsl(CD.hex_to_rgb(h))[1]


def flow_position(h):
    """Map a chromatic hex to its spectrum-flow position 0-4 (nearest anchor)."""
    hue = hue_of(h)
    best, bestd = 0, 1e9
    for i, (_name, ah) in enumerate(ANCHOR_HUES):
        d = abs(hue - ah)
        d = min(d, 360 - d)
        if d < bestd:
            best, bestd = i, d
    return best


def token_family(h):
    """True if the color reads as a sanctioned token (exact, richened,
    near-token, or same hue family as a token)."""
    h = CD.norm_hex(h)
    if h in CALC_TOKENS:
        return True
    if CD.near_token(h, tol=30):
        return True
    if CD.is_gray(h):
        return False
    hue = hue_of(h)
    for _name, ah in ANCHOR_HUES:
        d = abs(hue - ah)
        d = min(d, 360 - d)
        if d <= 22 and sat_of(h) > 0.35:
            return True
    return False


def in_amber_rose_band(h):
    hue, s, li = CD.rgb_to_hsl(CD.hex_to_rgb(h))
    return ((30 <= hue <= 52) or hue >= 330 or hue <= 12) and s > 0.45 and li > 0.45


def resolve_vars(value, props):
    """Resolve var(--x) references against :root props (one level + fallback)."""
    def rep(m):
        name = "--" + m.group(1)
        fallback = m.group(2)
        if name in props:
            return props[name].split("!")[0].strip()
        return fallback.strip() if fallback else m.group(0)
    prev = None
    out = value
    for _ in range(3):
        prev = out
        out = re.sub(r"var\(\s*--([\w-]+)\s*(?:,\s*([^)]*))?\)", rep, out)
        if out == prev:
            break
    return out


def visible_text(html):
    t = re.sub(r"<script.*?</script>", " ", html, flags=re.S | re.I)
    t = re.sub(r"<style.*?</style>", " ", t, flags=re.S | re.I)
    t = re.sub(r"<!--.*?-->", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"\s+", " ", t)
    return t.strip()


# --------------------------------------------------------------------------
class Finding:
    def __init__(self, category, check, points, message):
        self.category = category      # category key
        self.check = check            # check id (e.g. SPECTRUM, BTN, TRUTH-PR)
        self.points = points          # points DEDUCTED (positive number)
        self.message = message        # specific, named failure

    def as_dict(self):
        return {"category": self.category, "check": self.check,
                "deducted": self.points, "message": self.message}


class DesignCalculator:
    def __init__(self, html_text, room=None):
        self.html = html_text
        self.room = room
        self.findings = []
        css, self.viewport, raw = CD.extract_css_and_meta(html_text)
        self.css = css
        self.raw = raw
        self.rules = CD.parse_css(css)
        self.props = CD.custom_props(self.rules)
        self.text = visible_text(html_text)
        # Mechanical layer: run the executable checker, then apply judgment.
        self.mechanical = CD.check(html_text, room=room)

    # -- finding helpers ------------------------------------------------
    def deduct(self, category, check, points, message):
        self.findings.append(Finding(category, check, points, message))

    def mech(self, cid):
        return [m for m in self.mechanical if m["id"] == cid and m["severity"] == "FAIL"]

    # ==================================================================
    # CATEGORY 1 — SPECTRUM LAW (20)
    # The spectrum is a law, not a palette. Magenta -> purple -> blue ->
    # green -> gold. No adjacent dupes. Token-family colors only.
    # ==================================================================
    def _drift_hexes(self):
        """Hexes appearing in drift-demonstration CSS rules (what-NOT-to-do)."""
        if not hasattr(self, "_drift_hex_cache"):
            hexes = set()
            for sel, decls, _media in self.rules:
                if sel.startswith("@"):
                    continue
                if DRIFT_RE.search(sel):
                    for val in decls.values():
                        hexes.update(CD.colors_in(val))
            self._drift_hex_cache = {CD.norm_hex(h) for h in hexes}
        return self._drift_hex_cache

    def _interactive_classes(self):
        """Classes belonging to interactive elements: <button>, <a>,
        [role=button], onclick handlers, or cursor:pointer + :hover."""
        if not hasattr(self, "_interactive_cache"):
            classes = set()
            for m in re.finditer(r"<(button|a)\b[^>]*class=\"([^\"]*)\"", self.html, re.I):
                classes.update(m.group(2).split())
            for m in re.finditer(
                    r"<\w+\b[^>]*\b(?:onclick|role=[\"']button[\"'])[^>]*class=\"([^\"]*)\"",
                    self.html, re.I):
                classes.update(m.group(1).split())
            hover_sels = set()
            for s, _d, _m in self.rules:
                if ":hover" in s:
                    hover_sels.add(s)
            for s, d, _m in self.rules:
                if s.startswith("@"):
                    continue
                if d.get("cursor", "").strip() == "pointer":
                    for c in re.findall(r"\.([\w-]+)", s):
                        if any(c in hs for hs in hover_sels):
                            classes.add(c)
            self._interactive_cache = classes
        return self._interactive_cache

    def _inline_classes_for(self, hex_color):
        """All classes of elements whose inline style contains hex_color."""
        h = CD.norm_hex(hex_color).lstrip("#")
        out = set()
        for pat in (r"<\w+[^>]*class=\"([^\"]*)\"[^>]*style=\"[^\"]*" + re.escape(h),
                    r"<\w+[^>]*style=\"[^\"]*" + re.escape(h) + r"[^>]*class=\"([^\"]*)\""):
            for m in re.finditer(pat, self.html, re.I):
                out.update(m.group(1).split())
        return out

    def _is_neutral(self, h):
        """A color too desaturated or too light to claim a color identity.
        Shawn's spectrum law governs IDENTITY colors; pearl tints, shadows,
        and code-comment grays are neutrals, not violations."""
        if CD.is_gray(h):
            return True
        hue, s, li = CD.rgb_to_hsl(CD.hex_to_rgb(h))
        if s < 0.30:
            return True
        if CD.rel_luminance(CD.hex_to_rgb(h)) > 0.60:
            return True
        return False

    def score_spectrum(self):
        drift_hexes = self._drift_hexes()
        seen_colors = {}  # hex -> first message (dedup: one decision, one deduction)
        for m in self.mech("SPECTRUM") + self.mech("AMBERROSE"):
            cm = re.search(r"#(?:[0-9a-f]{6}|[0-9a-f]{3})\b", m["message"], re.I)
            if not cm:
                continue
            h = CD.norm_hex(cm.group(0))
            if h in seen_colors:
                continue
            if h in drift_hexes:
                continue  # drift-demonstration specimen, not a violation
            if self._is_neutral(h):
                continue  # pearl tints, shadows, desaturated grays aren't identity colors
            if token_family(h):
                # Judgment: sanctioned family — the raw checker was wrong.
                continue
            if in_amber_rose_band(h):
                seen_colors[h] = m["message"]
                self.deduct("spectrum_law", "AMBERROSE", 3,
                            "amber/rose outside token family: %s — %s" % (h, m["message"][:80]))
            else:
                seen_colors[h] = m["message"]
                self.deduct("spectrum_law", "SPECTRUM", 3,
                            "non-token chromatic color %s — %s" % (h, m["message"][:80]))
        for m in self.mech("PURPLEFILL"):
            if "::selection" in m["message"]:
                continue  # text-selection highlight is sanctioned
            # PURPLEFILL is by definition #9d75ff (see checker regex).
            h = "#9d75ff"
            if h in drift_hexes:
                continue
            if "[inline]" in m["message"]:
                iclasses = self._inline_classes_for(h)
                if any("swatch" in c.lower() for c in iclasses):
                    continue  # token swatch demonstrating purple, not a fill
            self.deduct("spectrum_law", "PURPLEFILL", 2,
                        "solid purple fill — purple is glow, not paint: %s" % m["message"][:90])
        self._spectrum_sequences()

    def _spectrum_sequences(self):
        # Identity elements in document order: jewels, gems, dots, pills, tabs.
        # A stack-walking parse resolves each element's color with CORRECT
        # variable scoping: own inline style -> ancestor inline custom props
        # -> CSS class rules. (A naive regex pass misattributes parent-scoped
        # --nc/--sc variables and invents false adjacent-dupe findings.)
        from html.parser import HTMLParser

        class Scan(HTMLParser):
            def __init__(self, outer):
                super().__init__(convert_charrefs=True)
                self.outer = outer
                self.stack = []
                self.seq = []

            def handle_starttag(self, tag, attrs):
                d = dict(attrs)
                self.stack.append((tag, d))
                cls = d.get("class", "")
                if re.search(r"jewel|gem|dot|pill|tab", cls, re.I):
                    color = self._resolve(d)
                    if color:
                        self.seq.append((cls, color))

            def handle_endtag(self, tag):
                for i in range(len(self.stack) - 1, -1, -1):
                    if self.stack[i][0] == tag:
                        del self.stack[i:]
                        break

            def _resolve(self, attrs):
                # 1. own inline style
                for c in CD.colors_in(attrs.get("style", "")):
                    if not CD.is_gray(c):
                        return c
                # 2. ancestor inline custom properties (innermost first)
                for _tag, d in reversed(self.stack[:-1]):
                    for c in CD.colors_in(d.get("style", "")):
                        if not CD.is_gray(c):
                            return c
                # 3. CSS class rules
                classes = attrs.get("class", "").split()
                for sel, decls, _media in self.outer.rules:
                    if sel.startswith("@"):
                        continue
                    if any(re.search(r"\." + re.escape(c) + r"\b", sel) for c in classes):
                        for prop in ("background", "background-color", "color"):
                            cols = [c for c in CD.colors_in(
                                resolve_vars(decls.get(prop, ""), self.outer.props))
                                if not CD.is_gray(c)]
                            if cols:
                                return cols[0]
                return None

        scan = Scan(self)
        try:
            scan.feed(self.html)
        except Exception:  # noqa: BLE001 — broken pages still get scored
            pass
        seq = [(cls, c) for cls, c in scan.seq if token_family(c)]
        # Only judge runs of 3+ resolvable identity elements.
        if len(seq) < 3:
            return
        positions = [flow_position(c) for _cls, c in seq]
        dupes = sum(1 for i in range(1, len(positions))
                    if (positions[i] - positions[i - 1]) % 5 == 0)
        scrambles = sum(1 for i in range(1, len(positions))
                        if (positions[i] - positions[i - 1]) % 5 >= 3)
        if dupes:
            self.deduct("spectrum_law", "ADJ-DUPE", min(6, 2 * dupes),
                        "%d adjacent duplicate hue(s) in identity sequence "
                        "(%s) — adjacent things never share a hue"
                        % (dupes, ", ".join(c for _cls, c in seq[:6])))
        if scrambles:
            self.deduct("spectrum_law", "FLOW-ORDER", min(4, 2 * scrambles),
                        "%d scramble(s) in spectrum flow — law is magenta->purple->blue->green->gold"
                        % scrambles)

    # ==================================================================
    # CATEGORY 2 — COLOR IDENTITY (15)
    # Black ground, white light, purple soul. One color job per thing.
    # ==================================================================
    def score_color_identity(self):
        drift_hexes = self._drift_hexes()
        interactive = self._interactive_classes()
        for m in self.mech("LIGHTBG"):
            sel_m = re.search(r"on '([^']+)'", m["message"])
            sel = sel_m.group(1) if sel_m else ""
            cm = re.search(r"#(?:[0-9a-f]{6}|[0-9a-f]{3})\b", m["message"], re.I)
            h = CD.norm_hex(cm.group(0)) if cm else ""
            if h in drift_hexes:
                continue
            sel_classes = set(re.findall(r"\.([\w-]+)", sel))
            if "[inline]" in m["message"]:
                iclasses = self._inline_classes_for(h)
                if any("swatch" in c.lower() for c in iclasses) and h in CALC_TOKENS:
                    continue  # token swatch demonstrating a sanctioned color
                sel_classes |= iclasses
            # White/light on interactive elements = Shawn's white-at-rest law.
            if sel_classes & interactive:
                continue
            if re.search(r"btn|button", sel, re.I):
                continue
            if "swatch" in sel.lower():
                continue  # color swatches demonstrate tokens; not page backgrounds
            if DRIFT_RE.search(m["message"]):
                continue
            # Translucent white washes (glass, alpha < 0.35) are not light-mode.
            rule_text = ""
            for s, d, _md in self.rules:
                if s.startswith("@"):
                    continue
                if sel and sel.split("[")[0].lower() in s.lower():
                    rule_text = " ".join(d.values())
                    break
            alpha = None
            tw = re.search(r"rgba?\(\s*255\s*,\s*255\s*,\s*255\s*,\s*([0-9.]+)", rule_text, re.I)
            if tw:
                try:
                    alpha = float(tw.group(1))
                except ValueError:
                    alpha = None
            if alpha is not None and alpha < 0.35:
                continue
            self.deduct("color_identity", "LIGHTBG", 3,
                        "light background breaks black ground: %s" % m["message"][:90])
        for m in self.mech("BODYCOLOR"):
            self.deduct("color_identity", "BODYCOLOR", 5,
                        "body text is not white: %s" % m["message"][:90])
        # Gray body copy anywhere (SYN-R-2): scan text-element rules.
        gray_hits = set()
        for sel, decls, _media in self.rules:
            if sel.startswith("@"):
                continue
            if not re.search(r"p\b|body|li\b|span|\.text|label|h[1-6]", sel, re.I):
                continue
            col = resolve_vars(decls.get("color", ""), self.props).strip().lower()
            for c in CD.colors_in(col):
                if CD.is_gray(c):
                    lum = CD.rel_luminance(CD.hex_to_rgb(c))
                    if 0.15 < lum < 0.55:  # mid gray — neither field nor light
                        gray_hits.add(c)
        for c in sorted(gray_hits)[:4]:
            self.deduct("color_identity", "GRAY-COPY", 2,
                        "gray copy text %s — body text is white, always" % c)
        # Black ground: page root background should be dark.
        root_bg = None
        for sel, decls, _media in self.rules:
            if sel.strip().lower() in ("body", "html", ":root"):
                bg = resolve_vars(decls.get("background",
                                           decls.get("background-color", "")), self.props)
                cols = CD.colors_in(bg)
                if cols:
                    root_bg = cols[0]
        if root_bg and CD.rel_luminance(CD.hex_to_rgb(root_bg)) >= 0.25:
            self.deduct("color_identity", "NO-BLACK-GROUND", 6,
                        "page root %s is not black ground — the page is light mode, brand inverted" % root_bg)
        # Body text resolving dark through variables (the mechanical check
        # only warns on var(); resolve it and judge).
        body_col = None
        for _s, decls, _m in CD.rules_for(self.rules, "body"):
            if "color" in decls:
                body_col = resolve_vars(decls["color"], self.props).strip().lower()
        if body_col:
            cols = CD.colors_in(body_col)
            if cols and CD.rel_luminance(CD.hex_to_rgb(cols[0])) < 0.30:
                self.deduct("color_identity", "DARK-TEXT", 5,
                            "body text resolves dark (%s) — white text 99%%, always" % cols[0])

    # ==================================================================
    # CATEGORY 3 — BUTTONS / DIMENSIONAL (20)
    # White at rest, ignites in its own color on touch. Bevel, elevation,
    # glow. Three states. 44px floor. Flat is dead.
    # ==================================================================
    def _btn_rules(self):
        return [(s, d) for s, d, _m in self.rules
                if not s.startswith("@") and BTN_SEL_RE.search(s)]

    def _btn_static_rules(self):
        return [(s, d) for s, d in self._btn_rules()
                if ":hover" not in s and ":active" not in s and ":focus" not in s]

    def _button_height_px(self, decls):
        """Estimate button height: explicit height, else padding + font-size."""
        for prop in ("min-height", "height"):
            v = resolve_vars(decls.get(prop, ""), self.props)
            m = re.match(r"\s*([0-9.]+)px", v)
            if m:
                return float(m.group(1))
        # estimate from vertical padding + font-size
        pad_v = 0
        fs = 16
        m = re.match(r"\s*([0-9.]+)px", resolve_vars(decls.get("font-size", ""), self.props))
        if m:
            fs = float(m.group(1))
        pad = decls.get("padding", "")
        parts = re.findall(r"([0-9.]+)px", resolve_vars(pad, self.props))
        if parts:
            vals = [float(x) for x in parts]
            pad_v = vals[0] * 2 if len(vals) in (1, 2) else vals[0] + vals[2]
        if pad_v:
            return fs * 1.25 + pad_v
        return 0

    def score_buttons(self):
        btn_rules = self._btn_static_rules()
        if not btn_rules:
            self.deduct("buttons_dimensional", "NO-BUTTONS", 6,
                        "no button rules found — nothing to touch, nothing alive")
            return
        # Mechanical button-law violations (deduped).
        seen_btn = set()
        for m in self.mech("BTN"):
            key = m["message"][:60]
            if key in seen_btn:
                continue
            seen_btn.add(key)
            self.deduct("buttons_dimensional", "BTN", 3,
                        "button law: %s" % m["message"][:90])
        # Depth: buttons must carry box-shadow (elevation/glow). Flat is dead.
        with_shadow = [s for s, d in btn_rules if d.get("box-shadow", "").strip() not in ("", "none")]
        if not with_shadow:
            self.deduct("buttons_dimensional", "FLAT", 4,
                        "buttons have no box-shadow — flat is dead (bevel, elevation, glow required)")
        elif len(with_shadow) < len(btn_rules) / 2:
            self.deduct("buttons_dimensional", "FLAT-SOME", 1,
                        "%d of %d button rules lack box-shadow at rest" % (
                            len(btn_rules) - len(with_shadow), len(btn_rules)))
        # Pill radius.
        if not any("999px" in d.get("border-radius", "") for _s, d in btn_rules):
            self.deduct("buttons_dimensional", "NO-PILL", 1,
                        "no 999px pill radius on buttons (NC-5.2)")
        # Hover ignition: buttons must have :hover rules.
        hover_rules = [s for s, _d in self._btn_rules() if ":hover" in s]
        if not hover_rules:
            self.deduct("buttons_dimensional", "NO-HOVER", 3,
                        "buttons have no :hover state — quiet at rest means ignites on touch")
        # Focus: three observable states (R-button-three-states).
        if not any(":focus" in s for s, _d in self._btn_rules()):
            self.deduct("buttons_dimensional", "NO-FOCUS", 2,
                        "buttons have no :focus state — IDLE/HOVER/FOCUS required")
        # 44px touch floor (explicit or estimated from padding).
        if not any(self._button_height_px(d) >= 44 for _s, d in btn_rules):
            self.deduct("buttons_dimensional", "TOUCH-FLOOR", 2,
                        "no button reaches the 44px touch floor")
        # White at rest (Shawn 2026-10-08) — or a strong white edge light
        # with hover ignition (the v1.5 cx-btn pattern he loved).
        white_rest = False
        for _s, d in btn_rules:
            bg = resolve_vars(d.get("background", d.get("background-color", "")), self.props)
            cols = CD.colors_in(bg)
            if cols and all(CD.rel_luminance(CD.hex_to_rgb(c)) >= 0.55 for c in cols):
                white_rest = True
            border = d.get("border", "")
            if re.search(r"1\.5px|2px", border) and "255" in border and hover_rules:
                white_rest = True
        if not white_rest:
            self.deduct("buttons_dimensional", "NOT-WHITE-REST", 2,
                        "buttons are not white at rest and lack strong white edge light")
        # Reduced motion (animations without handling).
        for m in self.mech("RM"):
            self.deduct("buttons_dimensional", "RM", 2,
                        "motion without prefers-reduced-motion: %s" % m["message"][:80])

    # ==================================================================
    # CATEGORY 4 — TYPOGRAPHY (10). 24 headlines / 18 body / 14 small.
    # ==================================================================
    def score_typography(self):
        # Resolve body font-size through variables (the raw checker can't).
        body_fs = None
        for _s, decls, _m in CD.rules_for(self.rules, "body"):
            if "font-size" in decls:
                body_fs = resolve_vars(decls["font-size"], self.props)
        if body_fs is None and "var(--fs-body)" not in self.css:
            if self.props.get("--fs-body"):
                body_fs = resolve_vars(self.props["--fs-body"], self.props)
        is_presentation = (
            self.props.get("--fs-headline", "").strip() == "24px"
            and self.props.get("--fs-sub", "").strip() == "18px"
            and self.props.get("--fs-body", "").strip() == "14px"
        )
        if not is_presentation:
            if body_fs is None:
                self.deduct("typography", "D9", 4, "no explicit body font-size — law: 18px, always")
            else:
                m = re.match(r"\s*([0-9.]+)px", body_fs)
                if m:
                    px = float(m.group(1))
                    if px < 18:
                        self.deduct("typography", "D9", 4,
                                    "body %s < 18px — Shawn's spec: 24/18/14" % body_fs.strip())
                elif "18px" not in body_fs:
                    self.deduct("typography", "D9", 4,
                                "body font-size '%s' is not 18px" % body_fs.strip()[:30])
        # h1 24px.
        for _s, decls, _m in CD.rules_for(self.rules, "h1"):
            if "font-size" not in decls:
                continue
            fs = resolve_vars(decls["font-size"], self.props)
            m = re.match(r"\s*([0-9.]+)px", fs)
            if m and float(m.group(1)) != 24:
                self.deduct("typography", "SYN-H24", 2,
                            "h1 %s != 24px — headlines are 24" % fs.strip())
        # System font stack (resolve CSS variables first).
        families = " ".join(
            resolve_vars(d.get("font-family", ""), self.props)
            for _s, d, _m in self.rules).lower()
        if families and not re.search(r"inter|system|-apple-system|segoe|roboto|sf pro", families):
            self.deduct("typography", "FONT", 1,
                        "no Inter/system font stack declared")
        # Readability: no tiny body copy.
        tiny = 0
        for sel, decls, _media in self.rules:
            if sel.startswith("@") or not re.search(r"\bp\b|body|\.body", sel, re.I):
                continue
            fs = resolve_vars(decls.get("font-size", ""), self.props)
            m = re.match(r"\s*([0-9.]+)px", fs)
            if m and float(m.group(1)) < 14:
                tiny += 1
        if tiny:
            self.deduct("typography", "TINY", 2,
                        "%d text rule(s) under 14px — unreadable" % tiny)

    # ==================================================================
    # CATEGORY 5 — TRUTH LANGUAGE (15)
    # What is verified glows green; what is merely claimed stays quiet.
    # Human-child-first. Technicals ride as evidence links, never prose.
    # ==================================================================
    def score_truth(self):
        # PR / issue numbers in visible UI text.
        prs = set(re.findall(r"(?:PR\s*)?#(\d{3,5})\b", self.text))
        prs = {p for p in prs if not (len(p) == 6)}  # (hex colors can't appear here; visible text only)
        for p in sorted(prs)[:3]:
            self.deduct("truth_language", "TRUTH-PR", 3,
                        "PR/issue number #%s in visible UI text — technicals ride as links, never prose" % p)
        # UUIDs in visible text.
        uuids = set(re.findall(
            r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
            self.text, re.I))
        for u in sorted(uuids)[:2]:
            self.deduct("truth_language", "TRUTH-UUID", 3,
                        "UUID %s… in visible UI text" % u[:8])
        # Commit SHAs standing alone in prose.
        shas = set(re.findall(r"(?<![0-9a-f])[0-9a-f]{7,40}(?![0-9a-f])", self.text.lower()))
        shas = {s for s in shas if not re.match(r"^[0-9]+$", s)}
        for s in sorted(shas)[:2]:
            self.deduct("truth_language", "TRUTH-SHA", 2,
                        "commit hash '%s' in visible UI text — evidence link, not prose" % s)
        # SCREAMING_CASE in prose: true UPPER_SNAKE machine tokens.
        # (Plain uppercase words like BLACK/CLAIM are headers, not violations.)
        screaming = set(re.findall(r"\b[A-Z][A-Z0-9]*_[A-Z0-9_]+\b", self.text))
        screaming = {w for w in screaming if w not in SANCTIONED_SCREAMING}
        for w in sorted(screaming)[:3]:
            self.deduct("truth_language", "TRUTH-SCREAM", 1,
                        "SCREAMING_CASE '%s' in UI text" % w)
        # Jargon in prose.
        low = self.text.lower()
        for j in JARGON:
            if re.search(r"\b" + re.escape(j) + r"\b", low):
                self.deduct("truth_language", "TRUTH-JARGON", 1,
                            "machine jargon '%s' in human-facing text" % j)
                if sum(1 for f in self.findings if f.check == "TRUTH-JARGON") >= 4:
                    break
        # Claim-pill walls: many prominent CLAIM/PENDING pills.
        pills = re.findall(
            r"<[^>]*class=\"[^\"]*(?:pill|badge|status)[^\"]*\"[^>]*>([^<]{1,60})</",
            self.html, re.I)
        claim_pills = [p for p in pills if re.search(r"claim|pending|unverified|draft", p, re.I)]
        if len(claim_pills) > 5:
            self.deduct("truth_language", "PILL-WALL", 4,
                        "%d claim pills — a wall of CLAIM; what is merely claimed stays quiet" % len(claim_pills))
        # Verified claims should glow green (v1.5 §06).
        verified_mentions = len(re.findall(r"verif", low))
        green_present = bool(re.search(r"#55e39a|#2fe89e|#35e39b", self.html, re.I))
        if verified_mentions >= 3 and not green_present:
            self.deduct("truth_language", "NO-GREEN", 2,
                        "%d 'verif*' mentions but no green glow — what is verified glows green" % verified_mentions)

    # ==================================================================
    # CATEGORY 6 — DETAILS (10). The details ARE the design.
    # ==================================================================
    def score_details(self):
        for m in self.mech("D1"):
            self.deduct("details", "D1", 3, "pinch zoom blocked: %s" % m["message"][:70])
        for m in self.mech("DIVBTN"):
            self.deduct("details", "DIVBTN", 2, "clickable div — use a real <button>")
        for m in self.mech("MAXW"):
            self.deduct("details", "MAXW", 2, "max-width cap: %s" % m["message"][:70])
        for m in self.mech("MAXIS"):
            self.deduct("details", "MAXIS", 2, "link to the old app URL")
        # HTML validity: mismatched tags.
        from html.parser import HTMLParser
        void = {"br", "hr", "img", "input", "meta", "link", "source", "wbr",
                "circle", "rect", "path", "polygon", "ellipse", "line", "use",
                "area", "base", "col", "embed", "track", "param"}
        errors = []

        class P(HTMLParser):
            def __init__(self):
                super().__init__(convert_charrefs=True)
                self.stack = []
            def handle_starttag(self, tag, attrs):
                if tag not in void:
                    self.stack.append((tag, self.getpos()))
            def handle_startendtag(self, tag, attrs):
                pass
            def handle_endtag(self, tag):
                if tag in void:
                    return
                if self.stack and self.stack[-1][0] == tag:
                    self.stack.pop()
                elif tag in [t for t, _p in self.stack]:
                    while self.stack and self.stack[-1][0] != tag:
                        bad, pos = self.stack.pop()
                        errors.append("<%s> opened line %d never closed before </%s>" % (bad, pos[0], tag))
                    self.stack.pop()
                else:
                    errors.append("stray </%s> at line %d" % (tag, self.getpos()[0]))
        try:
            P().feed(self.html)
        except Exception as e:  # noqa: BLE001 — a broken page still gets scored
            errors.append("parse error: %s" % e)
        for e in errors[:3]:
            self.deduct("details", "HTML", 1, e[:100])
        # Duplicate IDs.
        ids = re.findall(r'id="([^"]+)"', self.html)
        dupes = sorted({i for i in ids if ids.count(i) > 1})
        for d in dupes[:2]:
            self.deduct("details", "DUP-ID", 1, "duplicate id=\"%s\"" % d)
        # Stranded boxes: bordered elements with no content.
        stranded = re.findall(
            r"<div[^>]*class=\"[^\"]*box[^\"]*\"[^>]*>\s*</div>", self.html, re.I)
        if stranded:
            self.deduct("details", "STRANDED", 2,
                        "%d empty/stranded box element(s)" % len(stranded))

    # ==================================================================
    # CATEGORY 7 — VOICE (10). Additive: the page earns voice points.
    # ==================================================================
    def score_voice(self):
        low = self.text.lower()
        hits = [p for p in BRAND_PHRASES if p in low]
        nav = any(n in low for n in NAV_MARKERS)
        score = 5 + min(4, len(set(hits))) + (1 if nav else 0)
        self.voice_earned = min(10, score)
        self.voice_notes = hits[:6]

    # ==================================================================
    def run(self):
        self.score_spectrum()
        self.score_color_identity()
        self.score_buttons()
        self.score_typography()
        self.score_truth()
        self.score_details()
        self.score_voice()
        cats = {}
        for key, label, mx in CATEGORIES:
            if key == "voice":
                cats[key] = {"label": label, "max": mx, "score": self.voice_earned,
                             "findings": [{"check": "VOICE", "message":
                                            "brand voice: %s" % (
                                                ", ".join("'%s'" % h for h in self.voice_notes)
                                                or "no brand phrases found")}], }
                continue
            deducted = sum(f.points for f in self.findings if f.category == key)
            cats[key] = {"label": label, "max": mx, "score": max(0, mx - deducted),
                         "findings": [f.as_dict() for f in self.findings if f.category == key]}
        total = sum(c["score"] for c in cats.values())
        return {"total": total, "max": 100, "categories": cats,
                "room": self.room,
                "verdict": ("ELITE — ships" if total >= 90 else
                            "STRONG — polish to ship" if total >= 80 else
                            "DEVELOPING — real work left" if total >= 60 else
                            "NOT THERE YET")}


# ---------------------------------------------------------------- CLI ------
def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(
        description="Naya Design Calculator — scores HTML 0-100 against the design standard.")
    ap.add_argument("source", help="HTML file path")
    ap.add_argument("--room", default=None, help="room name (for accent checks)")
    ap.add_argument("--json", action="store_true", help="JSON output")
    ap.add_argument("--gate", nargs="?", const=90, default=None, type=int,
                    help="exit 1 when score < N (default 90; the nine-floor doctrine)")
    args = ap.parse_args(argv)

    if not os.path.exists(args.source):
        ap.error("file not found: %s" % args.source)
    with open(args.source, "r", encoding="utf-8", errors="replace") as f:
        html = f.read()

    calc = DesignCalculator(html, room=args.room)
    result = calc.run()

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("=" * 64)
        print("NAYA DESIGN CALCULATOR — %s" % os.path.basename(args.source))
        print("=" * 64)
        for key, _label, _mx in CATEGORIES:
            c = result["categories"][key]
            bar = "#" * (c["score"] * 20 // c["max"]) if c["max"] else ""
            print("\n[%s] %d/%d  %s" % (c["label"].upper(), c["score"], c["max"], bar))
            for f in c["findings"]:
                if f.get("deducted"):
                    print("   -%d  [%s] %s" % (f["deducted"], f["check"], f["message"]))
                elif f.get("message"):
                    print("   %s" % f["message"])
        print("\n" + "=" * 64)
        print("TOTAL: %d/100 — %s" % (result["total"], result["verdict"]))
        print("=" * 64)

    if args.gate is not None:
        if result["total"] < args.gate:
            if not args.json:
                print("GATE FAILED: %d < %d" % (result["total"], args.gate))
            return 1
        if not args.json:
            print("GATE PASSED: %d >= %d" % (result["total"], args.gate))
    return 0


if __name__ == "__main__":
    sys.exit(main())
