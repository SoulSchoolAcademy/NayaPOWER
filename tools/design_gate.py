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
     Every vector, every quote form: <link>, <script src>, @import.
  2. BLACK ROOT — html/body background is deep black.
  3. NO LIGHT SURFACES — no white/light background declarations, in <style>
     blocks AND inline style= attributes alike.
  4. DARK COLOR-SCHEME — meta or CSS declares dark.
  5. NO FREESTYLE COMPONENTS — every Naya-prefixed class exists in the manifest.
  6. LIGHT TEXT — body text color is light.
  7. MOBILE VIEWPORT — the viewport meta declares width=device-width
     (mobile is the primary canvas).

Hardening doctrine (validator round 2): fix CLASSES, not instances.
  - One quote-tolerant attribute tokenizer for every tag scan.
  - One external-resource scan for every vector (<link>, <script>, @import).
  - One style-source collector (<style> + inline style=) feeding one law.
  - Fail CLOSED on unparseable color values; alpha-aware luminance
    composited over the black ground.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Luminance bands. Below _DARK_LUM a color is deep black / dark; at or above
# _LIGHT_LUM a background is a light surface. Between the two is "mid" —
# neither deep black nor a light surface (fails BLACK ROOT, passes
# NO LIGHT SURFACES — same semantics as the original gate).
_DARK_LUM = 0.35
_LIGHT_LUM = 0.6

# Values that are not surfaces at all.
_NON_SURFACE = ("transparent", "none", "initial", "inherit", "unset")


def read_page(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


# ---------------------------------------------------------------------------
# CLASS 1 — quote-tolerant attribute parsing.
# One tokenizer for every tag scan (src, href, rel, class, style, name,
# content). Handles double-quoted, single-quoted, and unquoted values per the
# HTML spec (an unquoted value ends at whitespace or `>`).
# ---------------------------------------------------------------------------
_ATTR_RE = re.compile(r"""
    (?P<name>[^\s"'`>/=]+)
    (?:\s*=\s*
        (?:"(?P<dq>[^"]*)"
         |'(?P<sq>[^']*)'
         |(?P<uq>[^\s"'`>]+))
    )?""", re.X)


def _parse_attrs(tag: str) -> dict[str, str | None]:
    """Parse a tag's attributes, tolerating every quote form."""
    attrs: dict[str, str | None] = {}
    inner = re.sub(r"^<\s*/?\s*[a-zA-Z][a-zA-Z0-9]*", "", tag)
    inner = inner.rsplit(">", 1)[0]
    for m in _ATTR_RE.finditer(inner):
        val = m.group("dq")
        if val is None:
            val = m.group("sq")
        if val is None:
            val = m.group("uq")
        attrs[m.group("name").lower()] = val
    return attrs


def _find_tags(html: str, name: str):
    return re.finditer(r"<%s\b[^>]*>" % re.escape(name), html, re.I)


def _all_tags(html: str):
    return re.finditer(r"<([a-zA-Z][a-zA-Z0-9]*)\b[^>]*>", html)


# ---------------------------------------------------------------------------
# CLASS 3 — every style source. <style> blocks AND inline style= attributes
# feed one rule list and one law. A background smuggled through style="" is
# the same violation as one in a <style> block.
# ---------------------------------------------------------------------------
def _style_block_css(html: str) -> str:
    """All <style> block contents concatenated."""
    return "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", html, re.S | re.I))


def _inline_styles(html: str) -> list[tuple[str, str]]:
    """(tag name, style body) for every element carrying style=, in order."""
    out = []
    for m in _all_tags(html):
        style = _parse_attrs(m.group(0)).get("style")
        if style:
            out.append((m.group(1).lower(), style))
    return out


def _css_rule_iter(html: str):
    """(selector, declarations) across EVERY style source."""
    css = _style_block_css(html)
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", css):
        yield m.group(1).strip(), m.group(2)
    for tag, body in _inline_styles(html):
        yield f"<{tag}> [style]", body


def _inline_decl(html: str, tagname: str, prop_re: str) -> str | None:
    """First matching declaration from an inline style= on <tagname>."""
    for m in _find_tags(html, tagname):
        style = _parse_attrs(m.group(0)).get("style")
        if style:
            bm = re.search(prop_re, style, re.I)
            if bm:
                return bm.group(1).strip()
    return None


# ---------------------------------------------------------------------------
# CLASS 2 — external resources. One scan for every vector:
# <link rel=stylesheet href>, <script src>, and @import in any CSS source,
# in every syntactic form. data: URLs are inline by definition.
# ---------------------------------------------------------------------------
# "@import" may be followed directly by a quoted string with no whitespace
# (@import"..." is valid CSS); anything else requires whitespace, so
# "@importfoo" (not a real at-rule) is not misread as an import.
_IMPORT_RE = re.compile(r"""@import(?:\s+|(?=["']))(?:
      url\(\s*"(?P<u1>[^"]+)"\s*\)
    | url\(\s*'(?P<u2>[^']+)'\s*\)
    | url\(\s*(?P<u3>[^"'\s)]+)\s*\)
    | "(?P<u4>[^"]+)"
    | '(?P<u5>[^']+)'
    | (?P<u6>[^"'\s;]+)
)""", re.I | re.X)


def check_self_contained(html: str) -> list[str]:
    v = []
    for m in _find_tags(html, "link"):
        attrs = _parse_attrs(m.group(0))
        rel = (attrs.get("rel") or "")
        href = attrs.get("href")
        if ("stylesheet" in rel.lower().split() and href
                and not href.lower().startswith("data:")):
            v.append(f"SELF-CONTAINED: external stylesheet reference: {href}")
    for m in _find_tags(html, "script"):
        src = _parse_attrs(m.group(0)).get("src")
        if src and not src.lower().startswith("data:"):
            v.append(f"SELF-CONTAINED: external script reference: {src}")
    css_sources = [_style_block_css(html)]
    css_sources += [body for _, body in _inline_styles(html)]
    for css in css_sources:
        for m in _IMPORT_RE.finditer(css):
            url = next(g for g in m.groups() if g)
            if not url.lower().startswith("data:"):
                v.append(
                    f"SELF-CONTAINED: external stylesheet via @import: {url}")
    return v


def _bg_of_rule(css: str, selector: str) -> str | None:
    for m in re.finditer(
        re.escape(selector) + r"\s*\{([^}]*)\}", css, re.I
    ):
        body = m.group(1)
        bg = re.search(r"background(?:-color)?\s*:\s*([^;}]+);?", body, re.I)
        if bg:
            return bg.group(1).strip()
    return None


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


# ---------------------------------------------------------------------------
# CLASS 6 — alpha-aware color model. Every color parses to
# (effective luminance over black, alpha): eff = alpha * lum, composited over
# the black ground the law requires. rgba(255,255,255,0.04) renders ~#0a0a0a
# on black — it is not a light surface, and the gate must not claim it is.
# ---------------------------------------------------------------------------
def _lum(r: float, g: float, b: float) -> float:
    return (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255


def _parse_alpha(s: str) -> float | None:
    s = s.strip()
    try:
        if s.endswith("%"):
            return float(s[:-1]) / 100
        return float(s)
    except ValueError:
        return None


def _chan(s: str) -> float:
    s = s.strip()
    if s.endswith("%"):
        return float(s[:-1]) * 255 / 100
    return float(s)


def _hue2rgb(p: float, q: float, t: float) -> float:
    t %= 1.0
    if t < 1 / 6:
        return p + (q - p) * 6 * t
    if t < 1 / 2:
        return q
    if t < 2 / 3:
        return p + (q - p) * (2 / 3 - t) * 6
    return p


def _parse_color(color: str, vars: dict[str, str]) -> tuple[float, float] | None:
    """Parse a CSS color -> (effective luminance over black, alpha).

    Supports named colors, #rgb/#rgba/#rrggbb/#rrggbbaa, rgb()/rgba() and
    hsl()/hsla() in comma or space form with optional `/ alpha`. Returns
    None when the color cannot be parsed.
    """
    c = _resolve_vars(color.strip(), vars).strip().lower()
    c = re.sub(r"\s*!important\s*$", "", c)
    if c == "transparent":
        return (0.0, 0.0)
    if c in _NAMED_COLORS:
        r, g, b = _NAMED_COLORS[c]
        return (_lum(r, g, b), 1.0)
    m = re.match(r"#([0-9a-f]+)$", c)
    if m:
        h = m.group(1)
        try:
            if len(h) == 3:
                r, g, b = (int(ch * 2, 16) for ch in h)
                return (_lum(r, g, b), 1.0)
            if len(h) == 4:
                r, g, b = (int(ch * 2, 16) for ch in h[:3])
                a = int(h[3] * 2, 16) / 255
                return (a * _lum(r, g, b), a)
            if len(h) == 6:
                r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
                return (_lum(r, g, b), 1.0)
            if len(h) == 8:
                r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
                a = int(h[6:8], 16) / 255
                return (a * _lum(r, g, b), a)
        except ValueError:
            return None
        return None
    m = re.match(r"rgba?\(\s*([^)]+)\)\s*$", c)
    if m:
        inner, alpha = m.group(1), 1.0
        if "/" in inner:
            inner, a_s = inner.split("/", 1)
            alpha = _parse_alpha(a_s)
            if alpha is None:
                return None
        else:
            comma = [p for p in inner.split(",") if p.strip()]
            if len(comma) == 4:
                alpha = _parse_alpha(comma[3])
                if alpha is None:
                    return None
                inner = ",".join(comma[:3])
        nums = [p for p in re.split(r"[,\s]+", inner.strip()) if p]
        if len(nums) != 3:
            return None
        try:
            r, g, b = (_chan(n) for n in nums)
        except ValueError:
            return None
        if any(not 0 <= x <= 255 for x in (r, g, b)) or not 0 <= alpha <= 1:
            return None
        return (alpha * _lum(r, g, b), alpha)
    m = re.match(r"hsla?\(\s*([^)]+)\)\s*$", c)
    if m:
        inner, alpha = m.group(1), 1.0
        if "/" in inner:
            inner, a_s = inner.split("/", 1)
            alpha = _parse_alpha(a_s)
            if alpha is None:
                return None
        else:
            comma = [p for p in inner.split(",") if p.strip()]
            if len(comma) == 4:
                alpha = _parse_alpha(comma[3])
                if alpha is None:
                    return None
                inner = ",".join(comma[:3])
        nums = [p for p in re.split(r"[,\s]+", inner.strip()) if p]
        if len(nums) != 3:
            return None
        try:
            h_s, s_s, l_s = (n.strip() for n in nums)
            h = float(h_s[:-3] if h_s.endswith("deg") else h_s) % 360 / 360.0
            if not s_s.endswith("%") or not l_s.endswith("%"):
                return None
            s, l = float(s_s[:-1]) / 100, float(l_s[:-1]) / 100
        except ValueError:
            return None
        if not 0 <= alpha <= 1 or not 0 <= s <= 1 or not 0 <= l <= 1:
            return None
        if s == 0:
            return (alpha * l, alpha)
        q = l * (1 + s) if l < 0.5 else l + s - l * s
        p = 2 * l - q
        r, g, b = (_hue2rgb(p, q, h + 1 / 3), _hue2rgb(p, q, h),
                   _hue2rgb(p, q, h - 1 / 3))
        return (alpha * (0.2126 * r + 0.7152 * g + 0.0722 * b), alpha)
    return None


# ---------------------------------------------------------------------------
# CLASS 4 — gradient stops done honestly. Background values are split into
# top-level comma layers FIRST (a light second layer must not hide behind a
# dark first one); each layer is judged alone; the worst verdict wins.
# Within a gradient, the argument list is split paren-aware, direction
# keywords / angles / shapes / positions are skipped, and the first stop
# that contributes a surface is judged. A stop the gate cannot parse is a
# verdict of "unknown" — fail CLOSED, never fail open.
# ---------------------------------------------------------------------------
_GRADIENT_CALL_RE = re.compile(
    r"(?:repeating-)?(?:linear|radial|conic)-gradient\s*\(", re.I)
_NON_COLOR_ARG_RE = re.compile(r"""^(
      to\s+[a-z][a-z\s]*
    | [+-]?[\d.]+(?:deg|grad|rad|turn)
    | from\s+[+-]?[\d.]+(?:deg|grad|rad|turn)
    | (?:circle|ellipse)(?:\s+at\s+.+)?
    | at\s+.+
    | closest-side|closest-corner|farthest-side|farthest-corner
)$""", re.I | re.X)


def _split_top_level(s: str) -> list[str]:
    parts, depth, cur = [], 0, []
    for ch in s:
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
    return [p.strip() for p in parts if p.strip()]


def _first_stop_eff(layer: str, vars: dict[str, str]) -> float | str:
    """Effective luminance of the first surface-contributing stop of ONE
    gradient layer.

    Returns "unknown" when no stop can be verified (fail closed), or
    "transparent" when every stop is fully transparent (renders nothing).
    """
    m = re.match(
        r"(?:repeating-)?(?:linear|radial|conic)-gradient\s*\((.*)\)\s*$",
        layer.strip(), re.I | re.S)
    if not m:
        return "unknown"
    for part in _split_top_level(m.group(1)):
        if _NON_COLOR_ARG_RE.match(part):
            continue
        # a stop may carry a position ("red 50%"): split it off, but not
        # inside parens ("rgba(0, 0, 0, .5) 20%")
        colorish = re.split(r"\s+(?![^(]*\))", part.strip(), maxsplit=1)[0]
        colorish = _resolve_vars(colorish, vars)
        parsed = _parse_color(colorish, vars)
        if parsed is None:
            return "unknown"  # unparseable stop: fail closed
        eff, alpha = parsed
        if alpha < 0.05:
            continue  # transparent stop contributes no surface
        return eff
    return "transparent"


_URL_RE = re.compile(r"url\(\s*[^)]*\)", re.I)


def _looks_like_color(c: str) -> bool:
    return bool(re.search(
        r"#|rgba?\(|hsla?\(|var\(|color-mix\(|color\(|lab\(|lch\(|"
        r"oklab\(|oklch\(|light-dark\(|hwb\(", c, re.I)
    ) or bool(re.fullmatch(r"[a-z]+", c or ""))


def _band(eff: float, dark_below: float) -> str:
    if eff >= _LIGHT_LUM:
        return "light"
    if eff < dark_below:
        return "dark"
    return "mid"


def _layer_verdict(layer: str, vars: dict[str, str],
                   dark_below: float) -> str:
    """Verdict for ONE background layer: light | mid | dark | unknown |
    not-a-color."""
    L = _resolve_vars(layer.strip(), vars).strip().lower()
    L = re.sub(r"\s*!important\s*$", "", L)
    if L in _NON_SURFACE:
        return "dark"  # not a surface at all
    if _GRADIENT_CALL_RE.match(L):
        r = _first_stop_eff(L, vars)
        if r == "unknown":
            return "unknown"
        if r == "transparent":
            return "dark"  # renders nothing
        return _band(r, dark_below)
    # strip image layers, judge any remaining color
    no_url = _URL_RE.sub(" ", L).strip(" ,")
    if no_url != L and not _looks_like_color(no_url):
        return "not-a-color"
    parsed = _parse_color(no_url or L, vars)
    if parsed is None:
        return "unknown" if _looks_like_color(no_url or L) else "not-a-color"
    return _band(parsed[0], dark_below)


def _surface_verdict(val: str, vars: dict[str, str],
                     dark_below: float = _DARK_LUM) -> str:
    """One verdict for any background value: light | mid | dark | unknown |
    not-a-color.

    Multi-layer backgrounds are split first and each layer is judged alone;
    the worst verdict wins, so a light second layer cannot hide behind a
    dark first one.

    - "unknown": looks like a color but cannot be parsed -> FAIL CLOSED.
    - "not-a-color": image backgrounds (url(...)) cannot be machine-verified;
      a documented boundary, not a silent pass.
    """
    c = _resolve_vars(val.strip(), vars).strip().lower()
    c = re.sub(r"\s*!important\s*$", "", c)
    if c in _NON_SURFACE:
        return "dark"  # not a surface at all
    verdicts = [_layer_verdict(L, vars, dark_below)
                for L in _split_top_level(c)]
    for v in ("light", "unknown", "mid", "dark"):
        if v in verdicts:
            return v
    return "not-a-color"  # every layer is an unverifiable image


def _is_dark(color: str, vars: dict[str, str] | None = None) -> bool:
    """True only when the color is verifiably deep black / dark, in EVERY
    layer. Fail CLOSED on unparseable opaque colors: a color the gate cannot
    prove dark is not dark."""
    vars = vars or {}
    c = _resolve_vars(color.strip(), vars).strip().lower()
    if c in _NON_SURFACE:
        return True
    return all(_layer_verdict(L, vars, _DARK_LUM) == "dark"
               for L in _split_top_level(c))


def check_black_root(html: str) -> list[str]:
    v = []
    css = _style_block_css(html)
    vars = _root_vars(css)
    for sel in ("html", "body"):
        # Inline style wins in the browser cascade — read it first, so a
        # style="" white root cannot hide behind a stylesheet black one.
        bg = _inline_decl(html, sel,
                          r"background(?:-color)?\s*:\s*([^;}]+)")
        if bg is None:
            bg = _bg_of_rule(css, sel)
            # also accept body class selectors like body.naya-page
            if bg is None and sel == "body":
                m = re.search(
                    r"body\.[a-zA-Z0-9_-]+\s*\{([^}]*)\}", css, re.I
                )
                if m:
                    b2 = re.search(
                        r"background(?:-color)?\s*:\s*([^;}]+);?",
                        m.group(1), re.I
                    )
                    bg = b2.group(1).strip() if b2 else None
        if bg is None:
            v.append(f"BLACK ROOT: no background declared for `{sel}` "
                     f"(browser default white leaks through)")
        elif not _is_dark(bg, vars):
            v.append(f"BLACK ROOT: `{sel}` background is not deep black: {bg}")
    return v


def check_no_light_surfaces(html: str) -> list[str]:
    """No light backgrounds — in <style> blocks AND inline style= attributes,
    one law for every style source."""
    v = []
    css = _style_block_css(html)
    vars = _root_vars(css)
    for selector, body in _css_rule_iter(html):
        if selector.startswith("@"):
            continue
        # pseudo-element detail craft (specular dots, facet highlights)
        # are not surfaces — skip them
        if ":before" in selector or ":after" in selector:
            continue
        for bm in re.finditer(
            r"background(?:-color)?\s*:\s*([^;}]+);?", body, re.I
        ):
            val = bm.group(1).strip()
            verdict = _surface_verdict(val, vars, dark_below=_DARK_LUM)
            if verdict == "light":
                v.append(f"NO LIGHT SURFACES: `{selector}` has light "
                         f"background: {val}")
            elif verdict == "unknown":
                # fail CLOSED: a background the gate cannot verify dark
                # does not pass (validator round 2: fail-open-on-unparseable)
                v.append(f"NO LIGHT SURFACES: `{selector}` background "
                         f"cannot be verified dark: {val}")
    return v


def check_dark_scheme(html: str) -> list[str]:
    for m in _find_tags(html, "meta"):
        attrs = _parse_attrs(m.group(0))
        if ((attrs.get("name") or "").lower() == "color-scheme"
                and (attrs.get("content") or "").lower() == "dark"):
            return []
    for _tag, body in _inline_styles(html):
        if re.search(r"color-scheme\s*:\s*dark", body, re.I):
            return []
    if re.search(r"color-scheme\s*:\s*dark", _style_block_css(html), re.I):
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
    for m in _all_tags(html):
        cls_attr = _parse_attrs(m.group(0)).get("class")
        if cls_attr:
            used.update(cls_attr.split())
    for cls in sorted(used):
        if cls.startswith(_NAYA_PREFIXES) and cls not in known:
            # allow BEM/state suffixes of known bases
            base = re.match(r"([a-zA-Z0-9_-]+?)(--|__|-sm|-xs|-lg|$)", cls)
            base_name = cls.split("--")[0].split("__")[0]
            if base_name not in known and cls not in known:
                v.append(f"NO FREESTYLE: class `.{cls}` is not in the "
                         f"manifest — use a canonical block or file the gap")
    return v


def check_light_text(html: str) -> list[str]:
    v = []
    css = _style_block_css(html)
    # inline style wins in the browser cascade — read it first
    col = _inline_decl(html, "body", r"(?<![a-z-])color\s*:\s*([^;}]+)")
    bodies: list[str] = []
    if col is None:
        # body rule or body.<class> rules (page root carries the text color)
        bodies = re.findall(
            r"body(?:\.[a-zA-Z0-9_-]+)?\s*\{([^}]*)\}", css, re.I
        )
    if col is None:
        if not bodies:
            return ["LIGHT TEXT: no body rule found"]
        for b in bodies:
            m = re.search(r"(?<![a-z-])color\s*:\s*([^;}]+);?", b, re.I)
            if m:
                col = m.group(1).strip()
                break
    if not col:
        return ["LIGHT TEXT: body has no text color declared"]
    # light text = NOT dark
    if _is_dark(col, _root_vars(css)):
        v.append(f"LIGHT TEXT: body text color is dark: {col}")
    return v


def check_viewport(html: str) -> list[str]:
    for m in _find_tags(html, "meta"):
        attrs = _parse_attrs(m.group(0))
        if (attrs.get("name") or "").lower() == "viewport":
            content = (attrs.get("content") or "").replace(" ", "")
            if "width=device-width" in content:
                return []
            return ["MOBILE VIEWPORT: viewport meta does not declare "
                    "width=device-width"]
    return ["MOBILE VIEWPORT: no viewport meta tag "
            "(mobile is the primary canvas)"]


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
    # CLASS FIX (validator round 2): a non-object receipt (array, string,
    # number, null) is a clean ACTIVATION violation — never an AttributeError.
    if not isinstance(receipt, dict):
        return [f"ACTIVATION: receipt is not a JSON object "
                f"(got {type(receipt).__name__}) — refusing to verify"]
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
    violations: list[str] = []
    violations += check_self_contained(html)
    violations += check_black_root(html)
    violations += check_no_light_surfaces(html)
    violations += check_dark_scheme(html)
    violations += check_viewport(html)
    if manifest.exists():
        violations += check_no_freestyle(html, _manifest_classes(manifest))
    else:
        violations.append(f"NO FREESTYLE: manifest not found at {manifest} "
                          f"— cannot verify components")
    violations += check_light_text(html)
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
        # non-object receipts -> clean ACTIVATION violation, never a crash
        # (validator round 2, issue 7)
        non_object_v: dict[str, list[str] | str] = {}
        for label, raw in [("array", b"[1,2,3]"), ("string", b'"nope"'),
                           ("number", b"42"), ("null", b"null")]:
            rp_x = Path(d) / f"receipt_{label}.json"
            rp_x.write_bytes(raw)
            d_x = hashlib.sha256(raw).hexdigest()
            html_x = f"<!-- NAYA-ACTIVATION-RECEIPT-SHA256:{d_x} -->"
            try:
                non_object_v[label] = check_activation(
                    html_x, rp_x,
                    expected_repo="SoulSchoolAcademy/NayaPOWER")
            except Exception as e:  # noqa: BLE001 — any crash here IS the bug
                non_object_v[label] = f"CRASH {type(e).__name__}: {e}"
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
            got = check_no_light_surfaces("<style>" + frag + "</style>")
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
    # --- validator round-2 regressions: 7 evasions, fixed at CLASS level ---
    # (name, html, probe, expect_violation)
    r2 = [
        # CLASS 1: quote-tolerant attribute parsing
        ("r2 unquoted script src",
         "<script src=https://e/x.js></script>", check_self_contained, True),
        ("r2 single-quoted script src",
         "<script src='https://e/x.js'></script>", check_self_contained, True),
        ("r2 unquoted link href",
         "<link rel=stylesheet href=x.css>", check_self_contained, True),
        ("r2 unquoted class",
         "<div class=naya-evil>x</div>",
         lambda h: check_no_freestyle(h, {"naya-btn"}), True),
        ("r2 unquoted viewport still passes",
         '<meta name=viewport content="width=device-width, initial-scale=1">',
         check_viewport, False),
        ("r2 unquoted color-scheme still passes",
         "<meta name=color-scheme content=dark>", check_dark_scheme, False),
        # CLASS 2: @import in every syntactic form
        ("r2 @import url dq",
         '<style>@import url("https://e/x.css");</style>',
         check_self_contained, True),
        ("r2 @import url sq",
         "<style>@import url('https://e/x.css');</style>",
         check_self_contained, True),
        ("r2 @import url unquoted",
         "<style>@import url(https://e/x.css);</style>",
         check_self_contained, True),
        ("r2 @import dq",
         '<style>@import "https://e/x.css";</style>',
         check_self_contained, True),
        ("r2 @import sq",
         "<style>@import 'https://e/x.css';</style>",
         check_self_contained, True),
        ("r2 @import bare",
         "<style>@import https://e/x.css;</style>",
         check_self_contained, True),
        ("r2 @import no space before string",
         '<style>@import"https://e/x.css";</style>',
         check_self_contained, True),
        ("r2 @import data: stays allowed",
         "<style>@import url(data:text/css,body{});</style>",
         check_self_contained, False),
        # CLASS 3: inline style= scanned exactly like <style> blocks
        ("r2 inline style white",
         '<div style="background:white">x</div>',
         check_no_light_surfaces, True),
        ("r2 inline style single-quoted",
         "<div style='background:#fff'>x</div>",
         check_no_light_surfaces, True),
        ("r2 inline style unquoted",
         "<div style=background:white>x</div>",
         check_no_light_surfaces, True),
        ("r2 inline style dark passes",
         '<div style="background:#050507">x</div>',
         check_no_light_surfaces, False),
        ("r2 inline style on body wins cascade",
         '<body style="background:white">x</body>',
         check_black_root, True),
        # CLASS 4: gradients — direction/angle skipped, fail closed
        ("r2 gradient direction + white",
         "<style>x{background:linear-gradient(to bottom, white, black)}</style>",
         check_no_light_surfaces, True),
        ("r2 gradient angle + white",
         "<style>x{background:linear-gradient(45deg, #fff, #000)}</style>",
         check_no_light_surfaces, True),
        ("r2 gradient turn + white",
         "<style>x{background:repeating-linear-gradient(.25turn, white, black)}</style>",
         check_no_light_surfaces, True),
        ("r2 gradient dark passes",
         "<style>x{background:linear-gradient(120deg,#050507,#0a0a0f)}</style>",
         check_no_light_surfaces, False),
        ("r2 gradient radial dark passes",
         "<style>x{background:radial-gradient(circle at center, #0a0a0f, #050507)}</style>",
         check_no_light_surfaces, False),
        ("r2 gradient unparseable stop fails closed",
         "<style>x{background:linear-gradient(to right, var(--nope), black)}</style>",
         check_no_light_surfaces, True),
        ("r2 gradient transparent first stop passes",
         "<style>x{background:linear-gradient(rgba(255,255,255,0.04), #050507)}</style>",
         check_no_light_surfaces, False),
        ("r2 multilayer light second layer fails",
         "<style>x{background:linear-gradient(#050507 0%,#050507 100%),"
         " linear-gradient(white, black)}</style>",
         check_no_light_surfaces, True),
        ("r2 multilayer dark layers pass",
         "<style>x{background:radial-gradient(circle, rgba(255,255,255,.12),"
         " transparent 48%),linear-gradient(180deg,#15151b,#020203)}</style>",
         check_no_light_surfaces, False),
        ("r2 multilayer image over dark fails black-root closed",
         "<style>html{background:#050507}"
         "body{background:url(x.png),#050507}</style>",
         check_black_root, True),
        # CLASS 6: alpha-aware luminance (composited over black)
        ("r2 rgba ghost-white passes",
         "<style>x{background:rgba(255,255,255,0.04)}</style>",
         check_no_light_surfaces, False),
        ("r2 rgba near-opaque white fails",
         "<style>x{background:rgba(255,255,255,0.9)}</style>",
         check_no_light_surfaces, True),
        ("r2 8-digit hex ghost passes",
         "<style>x{background:#ffffff0a}</style>",
         check_no_light_surfaces, False),
        ("r2 hsla ghost passes",
         "<style>x{background:hsla(0,0%,100%,0.04)}</style>",
         check_no_light_surfaces, False),
    ]
    for name, html, fn, want_viol in r2:
        got = fn(html)
        if bool(got) != want_viol:
            print(f"SELF-TEST FAIL: {name}: expected violation={want_viol}, "
                  f"got={got}")
            ok = False
        else:
            print(f"SELF-TEST: {name} held (good)")
    # CLASS 5: non-object receipts -> clean violation, never a crash
    for label, res in non_object_v.items():
        if isinstance(res, str) or not any(
                x.startswith("ACTIVATION: receipt is not a JSON object")
                for x in res):
            print(f"SELF-TEST FAIL: {label} receipt not cleanly rejected: "
                  f"{res}")
            ok = False
        else:
            print(f"SELF-TEST: {label} receipt cleanly rejected (good)")
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
