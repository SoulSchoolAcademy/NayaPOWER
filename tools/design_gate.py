#!/usr/bin/env python3
"""NayaNET design gate — code is law, machine-forced.

Usage:
    python3 tools/design_gate.py <page.html> [--manifest smart-blocks/manifest.json] [--hub]
    python3 tools/design_gate.py <page.html> --require-activation --receipt=<receipt.json>

Hub pages are auto-detected (filename, /HUB/ path, or hub markers);
--hub forces the Hub OUTPUT-law scan on any page.

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
  8. COLOR STANDARD — no amber or rose pink anywhere; no pale pink or
     light-purple text as a primary reading treatment. Yellow/gold hues
     (the semantic-accent band) are exempt: VISUAL-LANGUAGE.md permits
     them when they carry semantic theme/state. Canonical:
     NAYA-ACTIVATION/DESIGN/VISUAL-LANGUAGE.md + standing color standard
     (black, white, purple, blues, green, gold; no amber, no rose pink).
  9. TYPOGRAPHY — body 18px, headline 18px, sub-headline 14px,
     big headline 24px (Shawn's 2026-10-08 typography ruling). Selectors
     naming a headline role are bound to their canonical size; body must
     declare its font-size. Non-machine-verifiable sizes fail closed.
 10. HUB OUTPUT LAW — on Hub pages only: no capture/command surfaces in
     Hub chrome — capture buttons, command inputs, agent-invocation
     surfaces, and generate/post/create action buttons. Capture is input;
     the Hub is output (HUB/PROJECT-INTELLIGENCE.md §6 Law 1; PR #1290).
     Applies when the page is Hub-marked (filename/path/marker) or
     --hub is passed. "Ask Naya" retrieval inputs are NOT command inputs;
     growth-loop "create space/door/invite" actions are NOT violations.
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


def read_page(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def inline_css(html: str) -> str:
    """All <style> block contents concatenated."""
    return "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", html, re.S | re.I))


def check_self_contained(html: str) -> list[str]:
    v = []
    for m in re.finditer(
        r'<link[^>]+rel=["\']stylesheet["\'][^>]*>', html, re.I
    ):
        tag = m.group(0)
        href = re.search(r'href=["\']([^"\']+)', tag, re.I)
        ref = href.group(1) if href else tag
        if not ref.startswith("data:"):
            v.append(f"SELF-CONTAINED: external stylesheet reference: {ref}")
    for m in re.finditer(r'<script[^>]+src=["\']([^"\']+)["\']', html, re.I):
        src = m.group(1)
        if not src.startswith("data:"):
            v.append(f"SELF-CONTAINED: external script reference: {src}")
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


def _is_dark(color: str, vars: dict[str, str] | None = None) -> bool:
    color = _resolve_vars(color, vars or {})
    c = color.strip().lower()
    if c in ("transparent", "none", "initial", "inherit"):
        return True  # not a light surface
    # hex
    m = re.match(r"#([0-9a-f]{3,8})", c)
    if m:
        h = m.group(1)
        if len(h) == 3:
            h = "".join(ch * 2 for ch in h)
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        lum = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255
        return lum < 0.35
    if "gradient" in c:
        # gradients: fail only if they START with a light stop
        first = c.split(",", 1)[1] if "," in c else c
        mm = re.search(r"#([0-9a-f]{3,8})", first)
        if mm:
            return _is_dark("#" + mm.group(1))
        if re.search(r"\bwhite\b", first):
            return False
        return True
    if re.search(r"\bwhite\b", c):
        return False
    rgba = re.match(
        r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)", c
    )
    if rgba:
        r, g, b = map(int, rgba.groups())
        lum = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255
        return lum < 0.35
    return True


def check_black_root(html: str, css: str) -> list[str]:
    v = []
    vars = _root_vars(css)
    for sel in ("html", "body"):
        bg = _bg_of_rule(css, sel)
        # also accept body class selectors like body.naya-page
        if bg is None and sel == "body":
            m = re.search(
                r"body\.[a-zA-Z0-9_-]+\s*\{([^}]*)\}", css, re.I
            )
            if m:
                b2 = re.search(
                    r"background(?:-color)?\s*:\s*([^;}]+);?", m.group(1), re.I
                )
                bg = b2.group(1).strip() if b2 else None
        if bg is None:
            v.append(f"BLACK ROOT: no background declared for `{sel}` "
                     f"(browser default white leaks through)")
        elif not _is_dark(bg, vars):
            v.append(f"BLACK ROOT: `{sel}` background is not deep black: {bg}")
    return v


def check_no_light_surfaces(css: str) -> list[str]:
    v = []
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
            r"background(?:-color)?\s*:\s*([^;}]+);?", body, re.I
        ):
            val = bm.group(1).strip()
            # exact white / light page surfaces only — gradient highlights
            # and tiny jewel facets are craft, not surfaces
            if re.match(
                r"^(white|#fff|#ffffff|#fafafa|#f5f5f5|#eee|#eeeeee)$",
                val.lower(),
            ):
                v.append(f"NO LIGHT SURFACES: `{selector}` has white "
                         f"background: {val}")
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


def check_light_text(css: str) -> list[str]:
    v = []
    # body rule or body.<class> rules (page root carries the text color)
    bodies = re.findall(
        r"body(?:\.[a-zA-Z0-9_-]+)?\s*\{([^}]*)\}", css, re.I
    )
    if not bodies:
        return ["LIGHT TEXT: no body rule found"]
    col = None
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


# ---------------------------------------------------------------------------
# 8. COLOR STANDARD — NAYA-ACTIVATION/DESIGN/VISUAL-LANGUAGE.md + standing
#    color standard. Machine rule: every color token in the page's CSS is
#    classified by hue. Amber and rose-pink are banned outright; pale
#    pink/light-purple are banned as TEXT treatment (the "primary reading"
#    proxy is any `color:` declaration — a machine cannot judge primacy,
#    so the gate is explicit and fail-closed). Yellow/gold (hue 46-65°)
#    are exempt: the law permits them when they carry semantic theme/state,
#    and semantics are Shawn's eye, not the gate's.
# ---------------------------------------------------------------------------

# pink/purple keyword colors (mapped to hex for hue classification)
_COLOR_KEYWORDS = {
    "pink": "#ffc0cb", "hotpink": "#ff69b4", "deeppink": "#ff1493",
    "lightpink": "#ffb6c1", "palevioletred": "#db7093", "violet": "#ee82ee",
    "fuchsia": "#ff00ff", "magenta": "#ff00ff", "plum": "#dda0dd",
    "orchid": "#da70d6", "mediumorchid": "#ba55d3", "lavender": "#e6e6fa",
    "thistle": "#d8bfd8", "mistyrose": "#ffe4e1",
    "lavenderblush": "#fff0f5", "lightcoral": "#f08080",
}

_COLOR_TOKEN_RE = re.compile(
    r"#([0-9a-fA-F]{3,8})\b"
    r"|rgba?\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}[^)]*\)"
    r"|\b(" + "|".join(sorted(_COLOR_KEYWORDS)) + r")\b"
)

# props whose value IS a reading treatment (machine proxy for "primary
# reading treatment" — fail-closed: any color: declaration is judged)
_TEXT_PROPS = {"color", "caret-color"}


def _parse_rgb(value: str, vars: dict[str, str]) -> tuple[int, int, int] | None:
    v = _resolve_vars(value.strip(), vars).strip().lower()
    if v in _COLOR_KEYWORDS:
        v = _COLOR_KEYWORDS[v]
    m = re.match(r"#([0-9a-f]{3,8})$", v)
    if m:
        h = m.group(1)
        if len(h) in (3, 4):
            h = "".join(ch * 2 for ch in h[:3])
        if len(h) >= 6:
            return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return None
    m = re.match(r"rgba?\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})", v)
    if m:
        return tuple(min(255, int(x)) for x in m.groups())  # type: ignore[return-value]
    return None


def _to_hsl(r: int, g: int, b: int) -> tuple[float, float, float]:
    rr, gg, bb = r / 255, g / 255, b / 255
    mx, mn = max(rr, gg, bb), min(rr, gg, bb)
    light = (mx + mn) / 2 * 100
    d = mx - mn
    if d == 0:
        return 0.0, 0.0, light
    sat = d / (1 - abs(mx + mn - 1)) * 100
    if mx == rr:
        hue = ((gg - bb) / d) % 6
    elif mx == gg:
        hue = (bb - rr) / d + 2
    else:
        hue = (rr - gg) / d + 4
    return hue * 60, sat, light


def _banned_class(h: float, s: float, l: float) -> str | None:
    """Classify a color against the palette law. None = allowed."""
    if s < 15 or l < 8 or l >= 93:
        return None  # near-neutral, near-black, near-white: not palette claims
    # amber band; the 44-46.5° sliver is the gold/amber boundary — only
    # high-saturation reads as amber there (metallic golds like #D4AF37
    # are desaturated; #FFC107/#FFBF00 amber stay flagged). Gold/yellow
    # (46.5-65°) are exempt: the law permits them when semantic.
    if (25 <= h < 44 and s > 45) or (44 <= h < 46.5 and s > 85):
        return "amber"
    if 285 <= h <= 350 and s > 30:
        return "rose-pink"
    if 260 <= h < 285 and s > 40 and l > 40:
        return "light-purple"
    return None


def _iter_css_colors(html: str, css: str):
    """Yield (selector, prop, raw_value) for every declaration in the CSS."""
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", css):
        selector, body = m.group(1).strip(), m.group(2)
        if selector.startswith("@"):
            continue
        for dm in re.finditer(r"([a-zA-Z-]+)\s*:\s*([^;}]+);?", body):
            yield selector, dm.group(1).strip().lower(), dm.group(2).strip()
    # inline style="" attributes carry CSS too
    for m in re.finditer(r'style=["\']([^"\']*)["\']', html, re.I):
        for dm in re.finditer(r"([a-zA-Z-]+)\s*:\s*([^;}]+);?", m.group(1)):
            yield "(inline style)", dm.group(1).strip().lower(), dm.group(2).strip()


def check_color_standard(html: str, css: str) -> list[str]:
    v = []
    vars = _root_vars(css)
    seen: set[str] = set()
    for selector, prop, raw in _iter_css_colors(html, css):
        for tm in _COLOR_TOKEN_RE.finditer(raw):
            rgb = _parse_rgb(tm.group(0), vars)
            if not rgb:
                continue
            h, s, l = _to_hsl(*rgb)
            cls = _banned_class(h, s, l)
            if cls == "amber":
                key = ("amber", selector, prop)
                if key not in seen:
                    seen.add(key)
                    v.append(f"COLOR STANDARD: amber is not in the palette "
                             f"(black/white/purple/blues/green/gold) — "
                             f"`{selector}` {prop}: {tm.group(0)}")
            elif cls == "rose-pink":
                key = ("rose-pink", selector, prop)
                if key not in seen:
                    seen.add(key)
                    v.append(f"COLOR STANDARD: rose pink is not in the palette — "
                             f"`{selector}` {prop}: {tm.group(0)}")
            elif cls == "light-purple" and prop in _TEXT_PROPS:
                key = ("light-purple", selector, prop)
                if key not in seen:
                    seen.add(key)
                    v.append(f"COLOR STANDARD: light-purple text is not a "
                             f"primary reading treatment — `{selector}` "
                             f"{prop}: {tm.group(0)} (text stays "
                             f"white/off-white; purple is accent/glow only)")
    return v


# ---------------------------------------------------------------------------
# 9. TYPOGRAPHY — Shawn's 2026-10-08 ruling: body 18px / headline 18px /
#    sub-headline 14px / big headline 24px. Any rule whose selector names
#    one of these roles is bound to the canonical size; the body rule must
#    declare its font-size at all (browser default 16px is a deviation).
# ---------------------------------------------------------------------------

_TYPE_CANON = {
    "headline": 18.0,
    "sub-headline": 14.0,
    "big-headline": 24.0,
}
_TYPE_ROLE_RE = [
    ("big-headline", re.compile(r"big[-_\s]?head(?:line)?|\bhero\b|\bmasthead\b|\bdisplay\b", re.I)),
    ("sub-headline", re.compile(r"sub[-_\s]?head(?:line)?", re.I)),
    ("headline", re.compile(r"headline", re.I)),
    ("headline", re.compile(r"(?<![\w-])h1(?![\w-])", re.I)),
    ("sub-headline", re.compile(r"(?<![\w-])h2(?![\w-])", re.I)),
]
_BODY_RE = re.compile(r"^body(\.|$|\s|:|\[)", re.I)


def _type_role(selector: str) -> str | None:
    for role, rx in _TYPE_ROLE_RE:
        if rx.search(selector):
            return role
    return None


def _font_px(value: str, vars: dict[str, str]) -> float | None:
    v = _resolve_vars(value.strip(), vars).strip().lower()
    m = re.match(r"^([0-9]*\.?[0-9]+)\s*(px|em|rem|%|pt)$", v)
    if not m:
        return None
    n, u = float(m.group(1)), m.group(2)
    return {"px": n, "em": n * 16, "rem": n * 16,
            "%": n * 16 / 100, "pt": n * 4 / 3}[u]


def _fmt_px(px: float) -> str:
    return f"{px:g}"


def check_typography(css: str) -> list[str]:
    v = []
    vars = _root_vars(css)
    found_body = False
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", css):
        selector, body = m.group(1).strip(), m.group(2)
        if selector.startswith("@"):
            continue
        fm = re.search(r"font-size\s*:\s*([^;}]+);?", body, re.I)
        if not fm:
            # font shorthand: font: <size>/<lh> <family>
            sh = re.search(r"(?<![a-z-])font\s*:\s*([^;}]+);?", body, re.I)
            if sh:
                sm = re.search(r"([0-9]*\.?[0-9]+\s*(?:px|em|rem|%|pt))",
                              sh.group(1), re.I)
                fm_val = sm.group(1) if sm else None
            else:
                fm_val = None
        else:
            fm_val = fm.group(1).strip()
        if fm_val is None:
            continue
        px = _font_px(fm_val, vars)
        if _BODY_RE.match(selector):
            found_body = True
            if px is None:
                v.append(f"TYPOGRAPHY: body font-size `{fm_val}` is not "
                         f"machine-verifiable as 18px (canonical)")
            elif abs(px - 18.0) > 0.01:
                v.append(f"TYPOGRAPHY: body font-size is {_fmt_px(px)}px — "
                         f"canonical is 18px")
            continue
        role = _type_role(selector)
        if role:
            expected = _TYPE_CANON[role]
            if px is None:
                v.append(f"TYPOGRAPHY: `{selector}` font-size `{fm_val}` is "
                         f"not machine-verifiable as {_fmt_px(expected)}px "
                         f"({role})")
            elif abs(px - expected) > 0.01:
                v.append(f"TYPOGRAPHY: `{selector}` font-size is "
                         f"{_fmt_px(px)}px — canonical {role} is "
                         f"{_fmt_px(expected)}px")
    if not found_body:
        v.append("TYPOGRAPHY: no font-size declared on body "
                 "(canonical 18px; browser default 16px is a deviation)")
    return v


# ---------------------------------------------------------------------------
# 10. HUB OUTPUT LAW — HUB/PROJECT-INTELLIGENCE.md §6 Law 1: "no capture
#     surface in Hub chrome. Capture is input; the Hub is output." PR #1290
#     removed capture/generate/post actions from Feed/Today/Reports/Mail.
#     Scanned on Hub pages only (auto-detected, or --hub). "Ask Naya"
#     retrieval inputs are NOT command inputs; growth-loop "create
#     space/door/invite" actions are NOT violations.
# ---------------------------------------------------------------------------

_HUB_MARKERS = re.compile(
    r"hub-chrome|data-hub|naya-hub|hub-app|hub-shell|id=[\"']hub[\"']", re.I)

_CAPTURE_RES = [
    re.compile(r"\bcapture\b", re.I),
    re.compile(r"save[-_\s]?to[-_\s]?brain", re.I),
    re.compile(r"capture[-_\s]?to", re.I),
    re.compile(r"record[-_\s]?to[-_\s]?brain", re.I),
]
_COMMAND_INPUT_RE = re.compile(r"\bcommand\b|run[-_\s]?command|cmd[-_\s]?prompt", re.I)
_RETRIEVAL_RE = re.compile(r"ask[-_\s]?naya|search", re.I)
_AGENT_RES = [
    re.compile(r"\binvoke\b", re.I),
    re.compile(r"(deploy|spawn|launch|run|summon)[-_\s]?agent", re.I),
    re.compile(r"(invoke|deploy|spawn)[A-Za-z]*[Aa]gent", re.I),  # onclick handlers
]
_ACTION_WORD_RES = [
    ("generate", re.compile(r"^\s*generate\b", re.I)),
    ("post", re.compile(r"^\s*post\b", re.I)),
    ("create", re.compile(r"^\s*create\b", re.I)),
]
_GROWTH_NOUN_RE = re.compile(r"\b(space|door|invite|member|connect)\b", re.I)


def _is_hub_page(html: str, page: Path) -> bool:
    if "hub" in page.name.lower():
        return True
    if "/hub/" in str(page).lower().replace("\\", "/"):
        return True
    return bool(_HUB_MARKERS.search(html))


def _button_blobs(html: str):
    """Yield (kind, label_text, full_tag) for button-like surfaces."""
    for m in re.finditer(r"<button[^>]*>(.*?)</button>", html, re.S | re.I):
        tag = m.group(0)
        label = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        yield "button", label, tag
    for m in re.finditer(r'<a[^>]*role=["\']button["\'][^>]*>(.*?)</a>',
                         html, re.S | re.I):
        tag = m.group(0)
        label = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        yield "anchor-button", label, tag
    for m in re.finditer(r'<input[^>]*type=["\'](?:submit|button)["\'][^>]*>',
                         html, re.I):
        tag = m.group(0)
        vm = re.search(r'value=["\']([^"\']*)', tag, re.I)
        yield "input-button", (vm.group(1).strip() if vm else ""), tag


def _attr_blob(tag: str) -> str:
    parts = []
    for attr in ("aria-label", "title", "id", "name", "data-action"):
        m = re.search(attr + r'=["\']([^"\']*)', tag, re.I)
        if m:
            parts.append(m.group(1))
    return " ".join(parts)


def check_hub_output_law(html: str) -> list[str]:
    v = []
    for kind, label, tag in _button_blobs(html):
        blob = f"{label} {_attr_blob(tag)}"
        for rx in _CAPTURE_RES:
            if rx.search(blob):
                v.append(f"HUB OUTPUT LAW: capture surface in Hub chrome — "
                         f"<{kind}> {label!r} (capture is input; Hub is output)")
                break
        else:
            for rx in _AGENT_RES:
                if rx.search(blob):
                    v.append(f"HUB OUTPUT LAW: agent-invocation surface in Hub "
                             f"chrome — <{kind}> {label!r}")
                    break
            else:
                for word, rx in _ACTION_WORD_RES:
                    if rx.search(label):
                        if word == "create" and _GROWTH_NOUN_RE.search(label):
                            continue  # growth loop: create space/door/invite
                        v.append(f"HUB OUTPUT LAW: `{word}` action button in "
                                 f"Hub chrome — <{kind}> {label!r} "
                                 f"(retrieval-only; see PR #1290)")
                        break
    for m in re.finditer(r"<input(?![^>]*type=[\"'](?:submit|button|hidden|checkbox|radio)[\"'])[^>]*>",
                         html, re.I):
        tag = m.group(0)
        blob = _attr_blob(tag)
        ph = re.search(r'placeholder=["\']([^"\']*)', tag, re.I)
        if ph:
            blob += " " + ph.group(1)
        if _COMMAND_INPUT_RE.search(blob) and not _RETRIEVAL_RE.search(blob):
            v.append(f"HUB OUTPUT LAW: command input in Hub chrome — "
                     f"{tag[:80]}… (no command surfaces; Ask Naya is retrieval)")
    return v


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
             expected_repo: str | None = None,
             hub: bool | None = None) -> list[str]:
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
    violations += check_light_text(css)
    violations += check_color_standard(html, css)
    violations += check_typography(css)
    is_hub = hub if hub is not None else _is_hub_page(html, page)
    if is_hub:
        violations += check_hub_output_law(html)
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
<style>html{background:#050507}body{background:#050507;color:#f8f7fb;font-size:18px}
.naya-btn{color:#fff}.headline{font-size:18px}.sub-headline{font-size:14px}.big-headline{font-size:24px}</style></head>
<body><h1 class="headline">T</h1><p class="sub-headline">S</p><p class="big-headline">B</p><button class="naya-btn">Go</button></body></html>"""
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
        # --- new-check adversarial battery (Gate 4: design automation) ---
        cases: list[tuple[str, str, str, bool, str | None]] = []
        # (name, page_html, filename, expect_fail, expected_prefix)
        cases.append(("pink text (rose-pink)",
                      good.replace("#f8f7fb", "#FFC0CB"), "pink.html",
                      True, "COLOR STANDARD"))
        cases.append(("pink keyword text",
                      good.replace("#f8f7fb", "pink"), "pinkkw.html",
                      True, "COLOR STANDARD"))
        cases.append(("amber background",
                      good.replace(".naya-btn{color:#fff}",
                                   ".naya-btn{color:#fff;background:#FFBF00}"),
                      "amber.html", True, "COLOR STANDARD"))
        cases.append(("gold text (semantic band, allowed)",
                      good.replace("#f8f7fb", "#FFD700"), "gold.html",
                      False, None))
        cases.append(("metallic gold background (boundary sliver, allowed)",
                      good.replace(".naya-btn{color:#fff}",
                                   ".naya-btn{color:#fff;background:#D4AF37}"),
                      "metalgold.html", False, None))
        cases.append(("12px body text",
                      good.replace("font-size:18px", "font-size:12px", 1),
                      "typo12.html", True, "TYPOGRAPHY"))
        cases.append(("headline at 22px (canonical 18px)",
                      good.replace(".headline{font-size:18px}",
                                   ".headline{font-size:22px}"),
                      "headline.html", True, "TYPOGRAPHY"))
        cases.append(("sub-headline at 14px (lawful)", good, "sub.html",
                      False, None))
        cases.append(("unverifiable body font-size",
                      good.replace("font-size:18px", "font-size:clamp(16px,2vw,20px)", 1),
                      "clamp.html", True, "TYPOGRAPHY"))
        hub_head = ("<!DOCTYPE html><html data-hub='true'><head>"
                      '<meta name="viewport" content="width=device-width, initial-scale=1">'
                      '<meta name="color-scheme" content="dark">'
                      "<style>html{background:#050507}body{background:#050507;"
                      "color:#f8f7fb;font-size:18px}.naya-btn{color:#fff}</style>"
                      "</head><body>")
        hub_tail = "</body></html>"
        cases.append(("hub page with Capture button",
                      hub_head + '<button class="naya-btn">Capture</button>' + hub_tail,
                      "hub-capture.html", True, "HUB OUTPUT LAW"))
        cases.append(("hub page with command input",
                      hub_head + '<input type="text" placeholder="Type a command…">' + hub_tail,
                      "hub-cmd.html", True, "HUB OUTPUT LAW"))
        cases.append(("hub page with Generate button",
                      hub_head + '<button class="naya-btn">Generate report</button>' + hub_tail,
                      "hub-gen.html", True, "HUB OUTPUT LAW"))
        cases.append(("hub page with Invoke-agent button",
                      hub_head + '<button class="naya-btn">Invoke agent</button>' + hub_tail,
                      "hub-invoke.html", True, "HUB OUTPUT LAW"))
        cases.append(("hub page, Ask Naya input (retrieval, allowed)",
                      hub_head + '<input type="text" placeholder="Ask Naya anything…">' + hub_tail,
                      "hub-ask.html", False, None))
        cases.append(("hub page, Create space (growth loop, allowed)",
                      hub_head + '<button class="naya-btn">Create space</button>' + hub_tail,
                      "hub-space.html", False, None))
        cases.append(("non-hub page with Capture button (output law not applied)",
                      good.replace("</body>", '<button class="naya-btn">Capture</button></body>'),
                      "plain.html", False, None))
        for name, page_html, fname, want_fail, prefix in cases:
            p = Path(d) / fname
            p.write_text(page_html)
            vv = run_gate(p, mf)
            got = [x for x in vv if prefix is None or x.startswith(prefix)]
            failed = bool(got) if prefix else bool(vv)
            if want_fail and not failed:
                print(f"SELF-TEST FAIL: '{name}' did not fail "
                      f"(violations: {vv})")
                ok = False
            elif not want_fail and failed:
                print(f"SELF-TEST FAIL: '{name}' wrongly failed: {got or vv}")
                ok = False
            else:
                print(f"SELF-TEST: '{name}' "
                      f"{'failed as required' if want_fail else 'passed'} (good)")
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
    hub = True if "--hub" in flags else None
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
                          expected_repo=expected_repo,
                          hub=hub)
    if violations:
        print(f"DESIGN GATE: FAIL — {len(violations)} violation(s) in {page}:")
        for viol in violations:
            print(f"  ✕ {viol}")
        return 1
    print(f"DESIGN GATE: PASS — {page}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
