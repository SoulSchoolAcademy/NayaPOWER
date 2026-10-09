#!/usr/bin/env python3
"""NayaNET design gate — code is law, machine-forced.

Usage:
    python3 tools/design_gate.py <page.html> [--manifest smart-blocks/manifest.json]
    python3 tools/design_gate.py <page.html> --require-activation --receipt=<receipt.json>

Enforces the STRUCTURAL design laws from DESIGN-LAWS.md as a hard gate.
Exit 0 = pass. Exit 1 = fail, with each violation named specifically.
Eye-enforced laws (craft, copy, motion meaning) remain Shawn's verdict —
this gate catches what a machine can prove.

With --require-activation, the gate also rejects deliverables with no, stale,
or mismatched activation citation (Naya 3's Gap 2, PR #1974). The citation
marker <!-- NAYA-ACTIVATION-RECEIPT-SHA256:<64hex> --> must match the sha256
of the exact receipt bytes, and the receipt must be fresh (<4h). Deep
verification against live GitHub state is Naya 3's checker in CI.

Structural checks:
  1. SELF-CONTAINED — no external stylesheet/script references (all inlined).
  2. BLACK ROOT — html/body background is deep black.
  3. NO LIGHT SURFACES — no white/light background declarations.
  4. DARK COLOR-SCHEME — meta or CSS declares dark.
  5. NO FREESTYLE COMPONENTS — every Naya-prefixed class exists in the manifest.
  6. LIGHT TEXT — body text color is light.
  7. MOBILE VIEWPORT — the viewport meta declares width=device-width
     (mobile is the primary canvas).

Normalization architecture (durable law, validator 2026-10-09): every
parser is only as strong as the narrowest input channel it doesn't read.
So there is ONE scanned CSS stream — <style> blocks AND inline style
attributes concatenated — punctuation is stripped before every color
lookup, and cascade winners are judged (inline beats stylesheet,
!important beats normal, later beats earlier), never first declarations.

Encoding normalization (extended law, validator 2026-10-09 round 3):
every parser is only as strong as the narrowest ENCODING it doesn't
decode. Browsers decode HTML entities in style ATTRIBUTE values (but
never inside <style> blocks — raw text elements), strip CSS /* */
comments, and decode CSS \XX escapes before color lookup. The gate's
normalization layer does exactly the same, in the same order:
unescape (attributes only) -> strip comments -> decode escapes.
Fail direction is fail-closed: an encoding the layer cannot resolve
leaves the value unjudgeable, and unjudgeable is not-dark.

Fail direction: black-root judging is fail-CLOSED (an unjudgeable color
cannot be verified dark); light-surface judging is fail-OPEN on images
only (a url() cannot be judged without fetching — honest, not a hole).

Alpha judgment: alpha is composited over the black ground. A 5% white
sheen over black is visually black (passes); a 90% white overlay is
visually white (fails). The gate enforces the rendered result on Shawn's
black canvas, not raw channel values.
"""
from __future__ import annotations

import hashlib
import html as _ihtml
import json
import re
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def read_page(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


# --- encoding normalization (validator round 3, 2026-10-09) ---
# Browsers decode three encodings before a color is ever judged:
#   1. HTML entities in style ATTRIBUTE values (&#119; -> w). Never inside
#      <style> blocks — those are raw text elements, entities stay raw.
#   2. CSS /* */ comments (stripped). An unclosed comment swallows the rest
#      of the input per CSS Syntax — the gate drops it too (fail-closed).
#   3. CSS \XX escapes (\69<space> -> i, \<newline> -> line continuation).
# The gate normalizes in browser order: unescape (attributes only),
# then strip comments, then decode escapes.

_CSS_ESCAPE_RE = re.compile(
    r"\\([0-9a-fA-F]{1,6})[ \t\n\r\f]?|\\(\r\n|[\n\r\f])|\\(.)", re.S)


def _decode_css_escapes(text: str) -> str:
    """Decode CSS escape sequences the way a browser's CSS parser does.

    \\<1-6 hex digits> + one optional whitespace (consumed) -> the code
    point; \\<newline> -> line continuation (removed); \\<any other char>
    -> that char. Invalid code points become U+FFFD, never a crash."""
    def repl(m: re.Match) -> str:
        if m.group(1) is not None:
            code = int(m.group(1), 16)
            if code == 0 or code > 0x10FFFF or 0xD800 <= code <= 0xDFFF:
                return "\uFFFD"
            return chr(code)
        if m.group(2) is not None:
            return ""  # line continuation
        return m.group(3)
    return _CSS_ESCAPE_RE.sub(repl, text)


def _strip_css_comments(text: str) -> str:
    """Strip CSS /* */ comments from the scanned stream. An unclosed
    comment consumes the rest of the input (CSS Syntax) — the tail is
    dropped, the gate judges less, and _is_dark fails closed on whatever
    remains unjudgeable. CDO/CDC (<!-- -->) are not comments and are
    untouched."""
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    cut = text.find("/*")
    if cut != -1:
        text = text[:cut]
    return text


def _normalize_css_block(text: str) -> str:
    """Normalize a <style> block's content: NO html.unescape — browsers do
    not decode entities in raw text elements. Comments stripped, CSS
    escapes decoded."""
    return _decode_css_escapes(_strip_css_comments(text))


def _normalize_style_attr(text: str) -> str:
    """Normalize an extracted style="" attribute value: the HTML parser
    decodes entities in attribute values before CSS sees them, so
    html.unescape() runs first, then the CSS pipeline."""
    return _decode_css_escapes(_strip_css_comments(_ihtml.unescape(text)))


def inline_css(html: str) -> str:
    """The single scanned CSS stream: <style> blocks AND inline style
    attributes, concatenated.

    Durable law (validator, 2026-10-09): every parser is only as strong as
    the narrowest input channel it doesn't read. Inline styles were an
    unread channel — every color check missed them. Each inline style
    attribute is wrapped as a `*[inline]` rule so the rule-iterating checks
    judge it like any other rule.

    Encoding law (validator round 3): <style> blocks are normalized as
    raw text (no entity decoding); inline attribute values are
    entity-decoded first. Both then go through comment stripping and CSS
    escape decoding, in browser order.
    """
    parts = [_normalize_css_block(p)
             for p in re.findall(r"<style[^>]*>(.*?)</style>", html, re.S | re.I)]
    for m in re.finditer(
        r"""\bstyle\s*=\s*"([^"]*)"|\bstyle\s*=\s*'([^']*)'""", html, re.I
    ):
        decl = m.group(1) if m.group(1) is not None else m.group(2)
        decl = (decl or "").strip()
        if decl:
            parts.append(f"*[inline]{{{_normalize_style_attr(decl)}}}")
    return "\n".join(parts)


def _inline_style_of(html: str, tag: str) -> str | None:
    """The normalized style="" attribute of the first <tag>, for cascade
    judging (inline styles beat stylesheet rules). Normalized through the
    same encoding layer as inline_css so cascade winners are judged on
    what the browser actually sees."""
    m = re.search(
        r"<%s\b[^>]*?\bstyle\s*=\s*\"([^\"]*)\"" % tag, html, re.I
    )
    if not m:
        m = re.search(
            r"<%s\b[^>]*?\bstyle\s*=\s*'([^']*)'" % tag, html, re.I
        )
    if not m:
        return None
    decl = m.group(1).strip()
    return _normalize_style_attr(decl) if decl else None


def _split_top_level(value: str) -> list[str]:
    """Split on commas at paren depth 0 (layers, not gradient stops)."""
    parts, depth, cur = [], 0, []
    for ch in value:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        if ch == "," and depth == 0:
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    parts.append("".join(cur))
    return parts


def _strip_punct(s: str) -> str:
    """Strip trailing punctuation/whitespace before every color lookup.
    (Validator hole 2: "white)" never matched the named-color table.)"""
    return s.strip().strip(";,")


_GRADIENT_HINT_RE = re.compile(
    r"^(to\s+[a-z\s]+|\d+(\.\d+)?(deg|turn|rad|grad)|circle|ellipse"
    r"|closest-side|closest-corner|farthest-side|farthest-corner"
    r"|at\s+.+)$",
    re.I,
)


def _gradient_stops(value: str) -> list[str]:
    """Paren-aware color stops of a gradient(), direction/position hints
    removed, trailing punctuation stripped. Fail-closed callers treat an
    empty/unparseable result as not-dark."""
    m = re.search(r"[a-z-]*gradient\s*\(", value, re.I)
    if not m:
        return []
    depth, start, stops = 0, m.end(), []
    for j in range(m.end() - 1, len(value)):
        ch = value[j]
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                stops.append(value[start:j])
                break
        elif ch == "," and depth == 1:
            stops.append(value[start:j])
            start = j + 1
    cleaned = []
    for s in stops:
        t = _strip_punct(s)
        if _GRADIENT_HINT_RE.match(t):
            continue
        t = re.sub(r"(\s+\d+(\.\d+)?%)+$", "", t).strip()
        if t:
            cleaned.append(t)
    return cleaned


def _first_color_token(layer: str) -> str | None:
    """First color-parseable token of a background shorthand layer.
    Tries the whole value first (functional notations contain spaces:
    hsl(0, 0%, 100%) must not be split), then falls back to whitespace
    token scanning for multi-token shorthands (snow url(x.png)).
    url(...) is skipped (an image cannot be judged without fetching);
    a layer with no color token is unjudgeable, not light."""
    t = _strip_punct(layer)
    if _luminance_of(t) is not None:
        return t
    v = re.sub(r"url\(\s*[^)]*\s*\)", " ", layer, flags=re.I)
    v = re.sub(r"var\(\s*--[^)]*\)", " ", v)
    for tok in re.split(r"\s+", v):
        t = _strip_punct(tok)
        if not t or t.lower() in ("none", "transparent", "inherit",
                                  "initial"):
            continue
        if _luminance_of(t) is not None:
            return t
    return None


def check_self_contained(html: str) -> list[str]:
    v = []
    for m in re.finditer(
        r'<link[^>]+rel\s*=\s*["\']stylesheet["\'][^>]*>', html, re.I
    ):
        tag = m.group(0)
        href = re.search(r'href\s*=\s*["\']([^"\']+)', tag, re.I)
        ref = href.group(1) if href else tag
        if not ref.startswith("data:"):
            v.append(f"SELF-CONTAINED: external stylesheet reference: {ref}")
    for m in re.finditer(r'<script[^>]+src\s*=\s*["\']([^"\']+)["\']', html, re.I):
        src = m.group(1)
        if not src.startswith("data:"):
            v.append(f"SELF-CONTAINED: external script reference: {src}")
    return v


def _root_vars(css: str) -> dict[str, str]:
    """Parse :root { --name: value } custom properties."""
    vars: dict[str, str] = {}
    for m in re.finditer(r":root\s*\{([^}]*)\}", css, re.I):
        for vm in re.finditer(r"--([a-zA-Z0-9_-]+)\s*:\s*([^;}]+);?", m.group(1)):
            vars[vm.group(1)] = vm.group(2).strip()
    return vars


def _resolve_vars(color: str, vars: dict[str, str], depth: int = 0) -> str:
    if depth > 5:
        return color
    m = re.search(r"var\(\s*--([a-zA-Z0-9_-]+)", color)
    if m and m.group(1) in vars:
        return _resolve_vars(vars[m.group(1)], vars, depth + 1)
    return color


# CSS named colors -> (r, g, b). Full table so heuristic checks cannot be
# evaded by spelling a light surface as a name (e.g. "snow", "yellow").
_NAMED_COLORS = {
    "aliceblue": (240, 248, 255), "antiquewhite": (250, 235, 215), "aqua": (0, 255, 255),
    "aquamarine": (127, 255, 212), "azure": (240, 255, 255), "beige": (245, 245, 220),
    "bisque": (255, 228, 196), "black": (0, 0, 0), "blanchedalmond": (255, 235, 205),
    "blue": (0, 0, 255), "blueviolet": (138, 43, 226), "brown": (165, 42, 42),
    "burlywood": (222, 184, 135), "cadetblue": (95, 158, 160), "chartreuse": (127, 255, 0),
    "chocolate": (210, 105, 30), "coral": (255, 127, 80), "cornflowerblue": (100, 149, 237),
    "cornsilk": (255, 248, 220), "crimson": (220, 20, 60), "cyan": (0, 255, 255),
    "darkblue": (0, 0, 139), "darkcyan": (0, 139, 139), "darkgoldenrod": (184, 134, 11),
    "darkgray": (169, 169, 169), "darkgrey": (169, 169, 169), "darkgreen": (0, 100, 0),
    "darkkhaki": (189, 183, 107), "darkmagenta": (139, 0, 139), "darkolivegreen": (85, 107, 47),
    "darkorange": (255, 140, 0), "darkorchid": (153, 50, 204), "darkred": (139, 0, 0),
    "darksalmon": (233, 150, 122), "darkseagreen": (143, 188, 143), "darkslateblue": (72, 61, 139),
    "darkslategray": (47, 79, 79), "darkslategrey": (47, 79, 79), "darkturquoise": (0, 206, 209),
    "darkviolet": (148, 0, 211), "deeppink": (255, 20, 147), "deepskyblue": (0, 191, 255),
    "dimgray": (105, 105, 105), "dimgrey": (105, 105, 105), "dodgerblue": (30, 144, 255),
    "firebrick": (178, 34, 34), "floralwhite": (255, 250, 240), "forestgreen": (34, 139, 34),
    "fuchsia": (255, 0, 255), "gainsboro": (220, 220, 220), "ghostwhite": (248, 248, 255),
    "gold": (255, 215, 0), "goldenrod": (218, 165, 32), "gray": (128, 128, 128),
    "grey": (128, 128, 128), "green": (0, 128, 0), "greenyellow": (173, 255, 47),
    "honeydew": (240, 255, 240), "hotpink": (255, 105, 180), "indianred": (205, 92, 92),
    "indigo": (75, 0, 130), "ivory": (255, 255, 240), "khaki": (240, 230, 140),
    "lavender": (230, 230, 250), "lavenderblush": (255, 240, 245), "lawngreen": (124, 252, 0),
    "lemonchiffon": (255, 250, 205), "lightblue": (173, 216, 230), "lightcoral": (240, 128, 128),
    "lightcyan": (224, 255, 255), "lightgoldenrodyellow": (250, 250, 210), "lightgray": (211, 211, 211),
    "lightgrey": (211, 211, 211), "lightgreen": (144, 238, 144), "lightpink": (255, 182, 193),
    "lightsalmon": (255, 160, 122), "lightseagreen": (32, 178, 170), "lightskyblue": (135, 206, 250),
    "lightslategray": (119, 136, 153), "lightslategrey": (119, 136, 153), "lightsteelblue": (176, 196, 222),
    "lightyellow": (255, 255, 224), "lime": (0, 255, 0), "limegreen": (50, 205, 50),
    "linen": (250, 240, 230), "magenta": (255, 0, 255), "maroon": (128, 0, 0),
    "mediumaquamarine": (102, 205, 170), "mediumblue": (0, 0, 205), "mediumorchid": (186, 85, 211),
    "mediumpurple": (147, 112, 219), "mediumseagreen": (60, 179, 113), "mediumslateblue": (123, 104, 238),
    "mediumspringgreen": (0, 250, 154), "mediumturquoise": (72, 209, 204), "mediumvioletred": (199, 21, 133),
    "midnightblue": (25, 25, 112), "mintcream": (245, 255, 250), "mistyrose": (255, 228, 225),
    "moccasin": (255, 228, 181), "navajowhite": (255, 222, 173), "navy": (0, 0, 128),
    "oldlace": (253, 245, 230), "olive": (128, 128, 0), "olivedrab": (107, 142, 35),
    "orange": (255, 165, 0), "orangered": (255, 69, 0), "orchid": (218, 112, 214),
    "palegoldenrod": (238, 232, 170), "palegreen": (152, 251, 152), "paleturquoise": (175, 238, 238),
    "palevioletred": (219, 112, 147), "papayawhip": (255, 239, 213), "peachpuff": (255, 218, 185),
    "peru": (205, 133, 63), "pink": (255, 192, 203), "plum": (221, 160, 221),
    "powderblue": (176, 224, 230), "purple": (128, 0, 128), "rebeccapurple": (102, 51, 153),
    "red": (255, 0, 0), "rosybrown": (188, 143, 143), "royalblue": (65, 105, 225),
    "saddlebrown": (139, 69, 19), "salmon": (250, 128, 114), "sandybrown": (244, 164, 96),
    "seagreen": (46, 139, 87), "seashell": (255, 245, 238), "sienna": (160, 82, 45),
    "silver": (192, 192, 192), "skyblue": (135, 206, 235), "slateblue": (106, 90, 205),
    "slategray": (112, 128, 144), "slategrey": (112, 128, 144), "snow": (255, 250, 250),
    "springgreen": (0, 255, 127), "steelblue": (70, 130, 180), "tan": (210, 180, 140),
    "teal": (0, 128, 128), "thistle": (216, 191, 216), "tomato": (255, 99, 71),
    "turquoise": (64, 224, 208), "violet": (238, 130, 238), "wheat": (245, 222, 179),
    "white": (255, 255, 255), "whitesmoke": (245, 245, 245), "yellow": (255, 255, 0),
    "yellowgreen": (154, 205, 50),
}


def _rgba_of(color: str) -> tuple[float, float, float, float] | None:
    """Parse a CSS color to (r, g, b, a) in 0..1, or None if unparseable."""
    c = re.sub(r";+$", "", color.strip().lower())
    if c == "transparent":
        return (0.0, 0.0, 0.0, 0.0)
    if c in _NAMED_COLORS:
        r, g, b = _NAMED_COLORS[c]
        return (r / 255, g / 255, b / 255, 1.0)
    m = re.fullmatch(r"#([0-9a-f]{3,4}|[0-9a-f]{6}|[0-9a-f]{8})", c)
    if m:
        h = m.group(1)
        if len(h) in (3, 4):
            h = "".join(ch * 2 for ch in h)
        a = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
        return (int(h[0:2], 16) / 255, int(h[2:4], 16) / 255,
                int(h[4:6], 16) / 255, a)
    m = re.fullmatch(
        r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*"
        r"(?:,\s*([\d.]+))?\s*\)", c)
    if m:
        a = float(m.group(4)) if m.group(4) is not None else 1.0
        return (int(m.group(1)) / 255, int(m.group(2)) / 255,
                int(m.group(3)) / 255, max(0.0, min(1.0, a)))
    m = re.fullmatch(
        r"hsla?\(\s*([\d.]+)\s*,\s*([\d.]+)%\s*,\s*([\d.]+)%\s*"
        r"(?:,\s*([\d.]+))?\s*\)", c)
    if m:
        h, s, l = (float(m.group(1)) / 360.0, float(m.group(2)) / 100.0,
                   float(m.group(3)) / 100.0)
        if s == 0:
            r = g = b = l
        else:
            def hue2rgb(p: float, q: float, t: float) -> float:
                t %= 1.0
                if t < 1 / 6:
                    return p + (q - p) * 6 * t
                if t < 1 / 2:
                    return q
                if t < 2 / 3:
                    return p + (q - p) * (2 / 3 - t) * 6
                return p
            q = l * (1 + s) if l < 0.5 else l + s - l * s
            p = 2 * l - q
            r, g, b = (hue2rgb(p, q, h + 1 / 3), hue2rgb(p, q, h),
                       hue2rgb(p, q, h - 1 / 3))
        a = float(m.group(4)) if m.group(4) is not None else 1.0
        return (r, g, b, max(0.0, min(1.0, a)))
    return None


def _luminance_of(color: str) -> float | None:
    """Relative luminance 0..1 of the color as rendered on the gate's black
    ground (alpha composited over black), or None if unparseable.

    Design judgment (validator hole 6): the gate enforces the rendered
    result on Shawn's black canvas, not raw channel values. A 5% white
    sheen over black is visually black (passes); a 90% white overlay is
    visually white (fails)."""
    rgba = _rgba_of(color)
    if rgba is None:
        return None
    r, g, b, a = rgba
    r, g, b = r * a, g * a, b * a  # composite over black
    return (0.2126 * r + 0.7152 * g + 0.0722 * b) / 1.0


def _is_dark(color: str, vars: dict[str, str] | None = None) -> bool:
    """True only if the value is provably dark. Fail-closed everywhere:
    any light stop, any unparseable stop, any unjudgeable token -> False.

    Gradients are judged by ALL stops: a white-to-black gradient IS a light
    surface at its white end. (The old "first stop only" rule let
    linear-gradient(white, black) walk through.)"""
    color = _resolve_vars(color, vars or {})
    c = color.strip().lower()
    if c in ("transparent", "none", "initial", "inherit"):
        return True  # not a light surface
    if "gradient" in c:
        stops = _gradient_stops(c)
        if not stops:
            return False  # fail closed: no parseable stops
        for s in stops:
            lum = _luminance_of(_strip_punct(s))
            if lum is None:
                return False  # fail closed: unparseable stop
            if lum >= 0.35:
                return False  # any light stop -> not dark
        return True
    tok = _first_color_token(c)
    if tok is None:
        return False  # fail closed: cannot verify dark
    lum = _luminance_of(tok)
    if lum is None:
        return False
    return lum < 0.35


def _surface_is_light(value: str) -> bool:
    """True if any layer/stop/token of a background value is provably light.
    Unparseable layers (images) are unjudgeable, not light — fail-open here
    is honest: the gate cannot fetch images. (Black-root judging stays
    fail-closed via _is_dark.)"""
    c = value.strip()
    if not c:
        return False
    for layer in _split_top_level(c):
        layer = layer.strip()
        if not layer:
            continue
        if "gradient" in layer.lower():
            for s in _gradient_stops(layer):
                lum = _luminance_of(_strip_punct(s))
                if lum is not None and lum >= 0.6:
                    return True
        else:
            tok = _first_color_token(layer)
            if tok is None:
                continue
            lum = _luminance_of(tok)
            if lum is not None and lum >= 0.6:
                return True
    return False


_BG_PAT = re.compile(
    r"background(?:-color)?\s*:\s*([^;!{}]+)(\s*!important)?", re.I)
_COLOR_PAT = re.compile(
    r"(?<![a-z-])color\s*:\s*([^;!{}]+)(\s*!important)?", re.I)


def _selector_targets(selector: str, tag: str) -> bool:
    """Does a CSS selector target <tag> (bare, classed, or descendant)?"""
    for part in selector.split(","):
        p = part.strip().lower()
        if re.fullmatch(r"%s(\.[a-z0-9_-]+)*" % tag, p):
            return True
        if re.search(r"(^|[\s>+~])%s(\.[a-z0-9_-]+)?$" % tag, p):
            return True
    return False


def _prop_declarations(css: str, pat: re.Pattern, html: str,
                       tag: str) -> tuple[list[tuple[int, int, str]], bool]:
    """Collect (rank, order, value) for a property on <tag>.

    Cascade ranks: stylesheet normal 1, inline normal 2,
    stylesheet !important 3, inline !important 4. The winner is
    max(rank, order) — inline beats stylesheet, !important beats normal,
    later beats earlier. Durable law: judge the cascade winner, not the
    first declaration.
    Returns (declarations, any_rule_targeted_tag)."""
    decls: list[tuple[int, int, str]] = []
    order = 0
    any_rule = False
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", css):
        selector = m.group(1).strip()
        if selector.startswith("@"):
            continue
        if not _selector_targets(selector, tag):
            continue
        any_rule = True
        for pm in pat.finditer(m.group(2)):
            rank = 3 if pm.group(2) else 1
            decls.append((rank, order, pm.group(1).strip()))
            order += 1
    inl = _inline_style_of(html, tag)
    if inl:
        any_rule = True
        for pm in pat.finditer(inl):
            rank = 4 if pm.group(2) else 2
            decls.append((rank, order, pm.group(1).strip()))
            order += 1
    return decls, any_rule


def check_black_root(html: str, css: str) -> list[str]:
    v = []
    vars = _root_vars(css)
    for sel in ("html", "body"):
        decls, any_rule = _prop_declarations(css, _BG_PAT, html, sel)
        if not decls:
            v.append(f"BLACK ROOT: no background declared for `{sel}` "
                     f"(browser default white leaks through)")
        else:
            winner = max(decls, key=lambda d: (d[0], d[1]))[2]
            if not _is_dark(winner, vars):
                v.append(f"BLACK ROOT: `{sel}` background is not deep black: "
                         f"{winner}")
    return v


def check_no_light_surfaces(css: str) -> list[str]:
    v = []
    vars = _root_vars(css)
    for m in re.finditer(
        r"([^{}]+)\{([^{}]*)\}", css
    ):
        selector, body = m.group(1).strip(), m.group(2)
        if selector.startswith("@"):
            continue
        # pseudo-element detail craft (specular dots, facet highlights)
        # are not surfaces — skip them
        if ":before" in selector or ":after" in selector:
            continue
        for bm in re.finditer(
            r"background(?:-color)?\s*:\s*([^;{}]+);?", body, re.I
        ):
            val = _resolve_vars(bm.group(1).strip(), vars)
            # Light surfaces are surfaces: any opaque background with high
            # luminance fails, however it is spelled (hex, name, hsl).
            # Every layer of multi-backgrounds is judged; every stop of a
            # gradient is judged.
            if _surface_is_light(val):
                v.append(f"NO LIGHT SURFACES: `{selector}` has light "
                         f"background: {bm.group(1).strip()}")
    return v


def check_dark_scheme(html: str, css: str) -> list[str]:
    if re.search(
        r'<meta[^>]+name=["\']color-scheme["\'][^>]*content=["\']dark["\']',
        html, re.I,
    ):
        return []
    if re.search(r"color-scheme\s*:\s*dark", css, re.I):
        return []
    return ["DARK COLOR-SCHEME: no dark color-scheme declared "
            "(native controls/chrome render light)"]


def _manifest_classes(manifest_path: Path) -> set[str]:
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    known: set[str] = set()
    manifest_dir = manifest_path.parent
    # every class defined in the canonical CSS files is canonical
    css_files = list(manifest_dir.glob("*.css"))
    css_files += list(manifest_dir.glob("*/*.css"))
    for cssf in css_files:
        css = cssf.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r"\.([a-zA-Z0-9_-]+)", css):
            cls = m.group(1)
            if cls.startswith(_NAYA_PREFIXES):
                known.add(cls)
    for b in data.get("blocks", []):
        for c in b.get("css_classes", []):
            for part in re.split(r"[/,]", c):
                # all class names in the selector, not just the first
                # (handles `table.naya-table[x]` -> naya-table)
                known.update(re.findall(r"\.([a-zA-Z0-9_-]+)", part))
        # every class used inside the block's own snippet is canonical too
        html_file = b.get("html_file", "")
        if html_file:
            cat = b.get("category_id", "")
            snippet = manifest_dir / cat / Path(html_file).name
            if snippet.exists():
                shtml = snippet.read_text(encoding="utf-8", errors="replace")
                for m in re.finditer(r'class=["\']([^"\']+)["\']', shtml):
                    known.update(m.group(1).split())
    # structural page root — not a component
    known.add("naya-page")
    return known


_NAYA_PREFIXES = ("naya-", "board", "orb-", "lv-", "torb", "gem-")


def check_no_freestyle(html: str, known: set[str]) -> list[str]:
    v = []
    used: set[str] = set()
    for m in re.finditer(r'class=["\']([^"\']+)["\']', html):
        for cls in m.group(1).split():
            used.add(cls)
    for cls in sorted(used):
        if cls.startswith(_NAYA_PREFIXES) and cls not in known:
            # allow BEM/state suffixes of known bases
            base = re.match(r"([a-zA-Z0-9_-]+?)(--|__|-sm|-xs|-lg|$)", cls)
            base_name = cls.split("--")[0].split("__")[0]
            if base_name not in known and cls not in known:
                v.append(f"NO FREESTYLE: class `.{cls}` is not in the "
                         f"manifest — use a canonical block or file the gap")
    return v


def check_light_text(html: str, css: str) -> list[str]:
    """Body text must be light. Judges the cascade winner — the last
    declaration wins (inline styles beat stylesheet rules, !important beats
    normal) — not the first declaration. (Validator hole 5: a later dark
    override, including inside @media, used to walk through.)"""
    decls, any_rule = _prop_declarations(css, _COLOR_PAT, html, "body")
    if not any_rule:
        return ["LIGHT TEXT: no body rule found"]
    if not decls:
        return ["LIGHT TEXT: body has no text color declared"]
    col = max(decls, key=lambda d: (d[0], d[1]))[2]
    # light text = NOT dark
    if _is_dark(col, _root_vars(css)):
        return [f"LIGHT TEXT: body text color is dark: {col}"]
    return []


def check_viewport(html: str) -> list[str]:
    m = re.search(
        r'<meta[^>]+name=["\']viewport["\'][^>]*>', html, re.I
    )
    if not m:
        return ["MOBILE VIEWPORT: no viewport meta tag "
                "(mobile is the primary canvas)"]
    if "width=device-width" not in m.group(0).replace(" ", ""):
        return ["MOBILE VIEWPORT: viewport meta does not declare "
                "width=device-width"]
    return []


RECEIPT_MARKER_RE = re.compile(
    r"<!--\s*NAYA-ACTIVATION-RECEIPT-SHA256:([a-fA-F0-9]{64})\s*-->")
RECEIPT_TTL = timedelta(hours=4)


def _normalize_repo(ref: str) -> str:
    """Normalize a repository reference to owner/repo for comparison."""
    s = str(ref or "").strip().lower()
    s = re.sub(r"^(https?://github\.com/|git@github\.com:)", "", s)
    s = re.sub(r"\.git$", "", s).rstrip("/")
    return s


def _detect_repo() -> str:
    """Best-effort expected repository from git remote.origin.url."""
    try:
        out = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            capture_output=True, text=True, timeout=10,
            cwd=REPO_ROOT).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        out = ""
    return _normalize_repo(out)


def check_activation(html: str, receipt_path: Path | None,
                     expected_repo: str | None = None) -> list[str]:
    """Activation citation check (Naya 3's Gap 2 — PR #1974 integration).

    With --require-activation, a deliverable FAILS unless it carries a
    current activation citation. This is the gate layer: structural
    presence/format/freshness. Deep verification of the receipt against
    live GitHub state is Naya 3's checker (tools/qa/) running in CI —
    the gate cannot fetch live state, and must not trust builder-supplied
    state as live.
    """
    v = []
    m = RECEIPT_MARKER_RE.search(html)
    if not m:
        return ["ACTIVATION: no activation citation marker in deliverable "
                "(<!-- NAYA-ACTIVATION-RECEIPT-SHA256:<64hex> -->). "
                "Unactivated work doesn't ship."]
    marker_sha = m.group(1).lower()
    if receipt_path is None:
        return ["ACTIVATION: citation marker present but no --receipt given; "
                "cannot verify freshness or integrity."]
    try:
        raw = receipt_path.read_bytes()
        receipt = json.loads(raw)
    except (OSError, ValueError) as e:
        return [f"ACTIVATION: cannot read receipt {receipt_path}: {e}"]
    if receipt.get("schema") != "naya.activation.receipt.v2":
        v.append("ACTIVATION: receipt schema is not naya.activation.receipt.v2")
    if receipt.get("status") != "ACTIVATED":
        v.append("ACTIVATION: receipt status is not ACTIVATED")
    for field in ("session_id", "naya_identity", "human_authority",
                  "repository", "job", "proof_plan"):
        if not receipt.get(field):
            v.append(f"ACTIVATION: receipt missing {field}")
    if not receipt.get("gates"):
        v.append("ACTIVATION: receipt names no governing gates")
    main_sha = receipt.get("main_sha", "")
    if not re.fullmatch(r"[a-fA-F0-9]{40}", str(main_sha)):
        v.append("ACTIVATION: receipt main_sha is not a 40-hex SHA")
    # Repository binding: the receipt must name THIS repository. A receipt
    # minted for another repo is a wrong-repository activation - fail.
    want = _normalize_repo(expected_repo) if expected_repo else _detect_repo()
    got = _normalize_repo(receipt.get("repository", ""))
    if not want:
        v.append("ACTIVATION: cannot determine the gated repository "
                 "(no --expected-repo and no git remote) - refusing to bind")
    elif got != want:
        v.append(f"ACTIVATION: receipt is for repository '{got}', not the "
                 f"gated repository '{want}' (wrong-repository activation)")
    # Integrity: the marker must be the sha256 of the exact receipt bytes.
    digest = hashlib.sha256(raw).hexdigest()
    if digest != marker_sha:
        v.append("ACTIVATION: citation marker does not match receipt bytes "
                 "(stale or forged citation)")
    # Freshness: 4h TTL, no future activations.
    try:
        activated = datetime.fromisoformat(
            str(receipt.get("activated_at", "")).replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        if activated > now + timedelta(minutes=2):
            v.append("ACTIVATION: receipt activated_at is in the future")
        elif now - activated > RECEIPT_TTL:
            v.append("ACTIVATION: receipt expired (>4h old) — re-activate")
    except ValueError:
        v.append("ACTIVATION: receipt activated_at is not a valid timestamp")
    return v


def run_gate(page: Path, manifest: Path,
             require_activation: bool = False,
             receipt_path: Path | None = None,
             expected_repo: str | None = None) -> list[str]:
    html = read_page(page)
    css = inline_css(html)
    violations: list[str] = []
    violations += check_self_contained(html)
    violations += check_black_root(html, css)
    violations += check_no_light_surfaces(css)
    violations += check_dark_scheme(html, css)
    violations += check_viewport(html)
    if manifest.exists():
        violations += check_no_freestyle(html, _manifest_classes(manifest))
    else:
        violations.append(f"NO FREESTYLE: manifest not found at {manifest} "
                          f"— cannot verify components")
    violations += check_light_text(html, css)
    if require_activation:
        violations += check_activation(html, receipt_path, expected_repo)
    return violations


def self_test() -> int:
    """Red-green: a violating page must fail, a lawful page must pass."""
    bad = """<!DOCTYPE html><html><head><link rel="stylesheet" href="x.css">
<style>body{background:#fff;color:#111}</style></head>
<body><div class="naya-frobnicate">hi</div></body></html>"""
    good = """<!DOCTYPE html><html><head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark">
<style>html{background:#050507}body{background:#050507;color:#f8f7fb}
.naya-btn{color:#fff}</style></head>
<body><button class="naya-btn">Go</button></body></html>"""
    import tempfile
    mf = REPO_ROOT / "smart-blocks" / "manifest.json"
    with tempfile.TemporaryDirectory() as d:
        pb, pg = Path(d) / "bad.html", Path(d) / "good.html"
        pb.write_text(bad)
        pg.write_text(good)
        bad_v = run_gate(pb, mf)
        good_v = run_gate(pg, mf)
        # --- activation scenarios (Naya 3 Gap 2) ---
        now = datetime.now(timezone.utc)
        receipt = {
            "schema": "naya.activation.receipt.v2",
            "status": "ACTIVATED",
            "session_id": "selftest-1",
            "naya_identity": "Naya 5",
            "human_authority": "Shawn",
            "repository": "SoulSchoolAcademy/NayaPOWER",
            "job": "self-test",
            "gates": ["Usefulness Gate"],
            "proof_plan": "self-test",
            "main_sha": "a" * 40,
            "activated_at": now.isoformat(),
        }
        rp = Path(d) / "receipt.json"
        rp.write_bytes(json.dumps(receipt).encode())
        digest = hashlib.sha256(rp.read_bytes()).hexdigest()
        marked = good.replace("</body>",
                              f"<!-- NAYA-ACTIVATION-RECEIPT-SHA256:{digest} --></body>")
        pm = Path(d) / "marked.html"
        pm.write_text(marked)
        noact_v = run_gate(pg, mf, require_activation=True,
                           receipt_path=rp)          # no marker -> fail
        okact_v = run_gate(pm, mf, require_activation=True,
                           receipt_path=rp)          # valid -> pass
        forged = marked.replace(digest, "0" * 64)
        pf = Path(d) / "forged.html"
        pf.write_text(forged)
        forged_v = run_gate(pf, mf, require_activation=True,
                            receipt_path=rp)         # mismatch -> fail
        old = dict(receipt,
                   activated_at=(now - timedelta(hours=5)).isoformat())
        rp_old = Path(d) / "receipt_old.json"
        rp_old.write_bytes(json.dumps(old).encode())
        d_old = hashlib.sha256(rp_old.read_bytes()).hexdigest()
        pm_old = Path(d) / "marked_old.html"
        pm_old.write_text(good.replace(
            "</body>",
            f"<!-- NAYA-ACTIVATION-RECEIPT-SHA256:{d_old} --></body>"))
        expired_v = run_gate(pm_old, mf, require_activation=True,
                             receipt_path=rp_old)    # expired -> fail
        # wrong-repository receipt -> fail (Naya 1's adversarial case)
        wrong = dict(receipt, repository="SomeoneElse/OtherRepo")
        rp_wrong = Path(d) / "receipt_wrong.json"
        rp_wrong.write_bytes(json.dumps(wrong).encode())
        d_wrong = hashlib.sha256(rp_wrong.read_bytes()).hexdigest()
        pm_wrong = Path(d) / "marked_wrong.html"
        pm_wrong.write_text(good.replace(
            "</body>",
            f"<!-- NAYA-ACTIVATION-RECEIPT-SHA256:{d_wrong} --></body>"))
        wrongrepo_v = run_gate(
            pm_wrong, mf, require_activation=True, receipt_path=rp_wrong,
            expected_repo="SoulSchoolAcademy/NayaPOWER")  # wrong repo -> fail
    ok = True
    if not bad_v:
        print("SELF-TEST FAIL: violating page passed the gate")
        ok = False
    else:
        print(f"SELF-TEST: violating page failed with {len(bad_v)} violations (good)")
        for viol in bad_v:
            print("   -", viol)
    if good_v:
        print("SELF-TEST FAIL: lawful page failed the gate:")
        for viol in good_v:
            print("   -", viol)
        ok = False
    else:
        print("SELF-TEST: lawful page passed (good)")
    # --- parser blind-spot regressions (Pair D scorer, 2026-10-09) ---
    # Every heuristic parser had an evasion; each now has a pinned repro.
    blind_spots = [
        ("named light color", "body{background:yellow}", False),
        ("hsl white", "body{background:hsl(0,0%,100%)}", False),
        ("hsl black", "body{background:hsl(0,0%,0%)}", True),
        ("named snow surface", "div{background:snow}", "light"),
        ("script src whitespace", '<script src ="https://e/x.js"></script>', "ext"),
        ("link rel whitespace", '<link rel = "stylesheet" href="x.css">', "ext"),
    ]
    for name, frag, want in blind_spots:
        if want == "light":
            got = check_no_light_surfaces(frag)
            bad = not got
        elif want == "ext":
            got = check_self_contained(frag)
            bad = not got
        else:
            got = _is_dark(frag.split(":", 1)[1].rstrip("}"))
            bad = (got != want)
        if bad:
            print(f"SELF-TEST FAIL: blind-spot '{name}' regressed")
            ok = False
        else:
            print(f"SELF-TEST: blind-spot '{name}' held (good)")
    for name, vv, want_fail in [
            ("no-marker+required", noact_v, True),
            ("valid receipt", okact_v, False),
            ("forged marker", forged_v, True),
            ("expired receipt", expired_v, True),
            ("wrong-repository receipt", wrongrepo_v, True)]:
        has_act = any(x.startswith("ACTIVATION") for x in vv)
        if want_fail and not has_act:
            print(f"SELF-TEST FAIL: activation case '{name}' did not fail")
            ok = False
        elif not want_fail and vv:
            print(f"SELF-TEST FAIL: activation case '{name}' failed: {vv}")
            ok = False
        else:
            print(f"SELF-TEST: activation case '{name}' "
                  f"{'failed as required' if want_fail else 'passed'} (good)")
    # --- second-wave blind-spot regressions (validator, 2026-10-09) ---
    # The first red-team found holes INSIDE the parsers; these were at the
    # BOUNDARIES between parsers: stylesheet vs inline attribute, first stop
    # vs named stop, first layer vs second layer, first declaration vs
    # cascade winner. Durable law: one scanned stream, punctuation stripped
    # before every lookup, cascade winners judged.
    def _rule(decl: str) -> str:
        return "x{%s}" % decl

    wave2 = [
        # (name, fragment, check-kind, must_flag_violation)
        ("inline style light bg",
         '<div style="background:linen">x</div>', "surface_html", True),
        ("inline style light bg-color",
         '<div style="background-color: yellow">x</div>', "surface_html",
         True),
        ("inline style dark bg passes",
         '<div style="background:#0a0a0f">x</div>', "surface_html", False),
        ("inline body bg beats dark stylesheet",
         '<style>body{background:#050507}</style>'
         '<body style="background:#ffffff">x</body>', "rooth_html", True),
        ("inline body dark bg passes",
         '<html style="background:#000"></html>'
         '<body style="background:#050507">x</body>', "rooth_html", False),
        ("gradient named light stop",
         "linear-gradient(white, black)", "notdark", True),
        ("gradient all dark stops",
         "linear-gradient(#0a0a0f, #15151f)", "notdark", False),
        ("gradient uppercase fn",
         "LINEAR-GRADIENT(white, black)", "notdark", True),
        ("gradient rgba heavy stop",
         "linear-gradient(rgba(255,255,255,0.9), black)", "notdark", True),
        ("gradient transparent stop passes",
         "linear-gradient(rgba(0,0,0,0.9), transparent)", "notdark", False),
        ("background shorthand snow+url",
         _rule("background:snow url(x.png)"), "surface", True),
        ("background shorthand url+snow",
         _rule("background:url(x.png) snow"), "surface", True),
        ("background image only: unjudgeable",
         _rule("background:url(x.png)"), "surface", False),
        ("multi-layer second light",
         _rule("background:#050507,#ffffff"), "surface", True),
        ("multi-layer all dark",
         _rule("background:#050507,#0a0a0f"), "surface", False),
        ("text cascade: later dark wins",
         "body{color:#f8f7fb}body{color:#222}", "text", True),
        ("text cascade: later light wins",
         "body{color:#222}body{color:#f8f7fb}", "text", False),
        ("text inline beats stylesheet",
         '<style>body{color:#f8f7fb}</style>'
         '<body style="color:#111">x</body>', "texthtml", True),
        ("text important beats inline",
         '<style>body{color:#f8f7fb !important}</style>'
         '<body style="color:#111">x</body>', "texthtml", False),
        ("text dark inside media",
         "@media(max-width:1px){body{color:#333}}", "text", True),
        ("alpha hairline sheen passes",
         "rgba(255,255,255,0.05)", "notdark", False),
        ("alpha heavy overlay fails",
         _rule("background:rgba(255,255,255,0.9)"), "surface", True),
        ("hex8 translucent white passes",
         "#ffffff0d", "notdark", False),
    ]
    for name, frag, kind, must_flag in wave2:
        if kind == "surface":
            flagged = bool(check_no_light_surfaces(frag))
        elif kind == "surface_html":
            flagged = bool(check_no_light_surfaces(inline_css(frag)))
        elif kind == "notdark":
            # _is_dark True == dark == no violation
            flagged = not _is_dark(frag)
        elif kind == "rooth_html":
            flagged = bool(check_black_root(frag, inline_css(frag)))
        elif kind == "text":
            flagged = bool(check_light_text("", frag))
        elif kind == "texthtml":
            flagged = bool(check_light_text(frag, inline_css(frag)))
        if flagged != must_flag:
            print(f"SELF-TEST FAIL: wave-2 blind-spot '{name}' regressed "
                  f"(flagged={flagged}, want={must_flag})")
            ok = False
        else:
            print(f"SELF-TEST: wave-2 blind-spot '{name}' held (good)")
    # --- encoding bypass regressions (validator round 3, 2026-10-09) ---
    # Durable law: every parser is only as strong as the narrowest
    # ENCODING it doesn't decode. Browsers decode HTML entities in style
    # attribute values (but NOT inside <style> blocks), strip CSS /* */
    # comments, and decode CSS \XX escapes. Each has a pinned repro.
    enc = [
        # (name, fragment, check-kind, must_flag_violation)
        ("entity inline bg",
         '<div style="background:&#119;hite">x</div>', "surface_html", True),
        ("entity hex inline bg",
         '<div style="background:&#x77;hite">x</div>', "surface_html", True),
        ("entity inline bg-color",
         '<div style="background-color:&#121;ellow">x</div>',
         "surface_html", True),
        ("entity in property name",
         '<div style="&#98;ackground:white">x</div>', "surface_html", True),
        ("entity text color cascade",
         '<style>body{color:#f5f5f5}</style>'
         '<body style="color:&#35;111">x</body>', "texthtml", True),
        ("entity body bg cascade",
         '<style>body{background:#050507}</style>'
         '<body style="background:&#35;ffffff">x</body>', "rooth_html", True),
        ("entity double-encoded stays raw",
         '<div style="background:&amp;#119;hite">x</div>',
         "surface_html", False),
        ("entity in style block NOT decoded",
         "<style>div{background:&#119;hite}</style>",
         "surface_html", False),
        ("css escape inline bg",
         '<div style="background:wh\\69te">x</div>', "surface_html", True),
        ("css escape block bg",
         "<style>div{background:wh\\69te}</style>", "surface_html", True),
        ("css escape hex consumes space",
         "<style>div{background:wh\\49 te}</style>", "surface_html", True),
        ("css escape line continuation",
         "<style>div{background:bl\\\nack}</style>", "surface_html", False),
        ("css escape dark stays dark",
         "<style>div{background:bl\\61ck}</style>", "surface_html", False),
        ("css escape uppercase hex",
         "<style>div{background:WH\\49TE}</style>", "surface_html", True),
        ("css comment inline bg",
         '<div style="background:/*x*/white">x</div>', "surface_html", True),
        ("css comment block bg",
         "<style>div{background:/*x*/white}</style>", "surface_html", True),
        ("css comment splits property",
         "<style>div{back/*x*/ground:white}</style>", "surface_html", True),
        ("css comment in text color",
         "<style>body{color:/*x*/#111}</style>", "texthtml", True),
        ("css comment dark passes",
         "<style>div{background:/*ok*/#050507}</style>",
         "surface_html", False),
    ]
    for name, frag, kind, must_flag in enc:
        if kind == "surface_html":
            flagged = bool(check_no_light_surfaces(inline_css(frag)))
        elif kind == "rooth_html":
            flagged = bool(check_black_root(frag, inline_css(frag)))
        elif kind == "texthtml":
            flagged = bool(check_light_text(frag, inline_css(frag)))
        if flagged != must_flag:
            print(f"SELF-TEST FAIL: encoding blind-spot '{name}' regressed "
                  f"(flagged={flagged}, want={must_flag})")
            ok = False
        else:
            print(f"SELF-TEST: encoding blind-spot '{name}' held (good)")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return self_test()
    args = [a for a in argv if not a.startswith("--")]
    flags = {a for a in argv if a.startswith("--")}
    if not args:
        print(__doc__)
        return 2
    page = Path(args[0])
    manifest = Path(args[1]) if len(args) > 1 else (
        REPO_ROOT / "smart-blocks" / "manifest.json"
    )
    require_activation = "--require-activation" in flags
    receipt_path = None
    expected_repo = None
    for a in argv:
        if a.startswith("--receipt="):
            receipt_path = Path(a.split("=", 1)[1])
        elif a.startswith("--expected-repo="):
            expected_repo = a.split("=", 1)[1]
    if not page.exists():
        print(f"design_gate: no such file: {page}")
        return 2
    violations = run_gate(page, manifest,
                          require_activation=require_activation,
                          receipt_path=receipt_path,
                          expected_repo=expected_repo)
    if violations:
        print(f"DESIGN GATE: FAIL — {len(violations)} violation(s) in {page}:")
        for viol in violations:
            print(f"  ✕ {viol}")
        return 1
    print(f"DESIGN GATE: PASS — {page}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
