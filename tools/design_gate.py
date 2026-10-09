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


def _luminance_of(color: str) -> float | None:
    """Relative luminance 0..1, or None if the color cannot be parsed."""
    c = color.strip().lower()
    if c in _NAMED_COLORS:
        r, g, b = _NAMED_COLORS[c]
        return (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255
    m = re.match(r"#([0-9a-f]{3,8})", c)
    if m:
        h = m.group(1)
        if len(h) == 3:
            h = "".join(ch * 2 for ch in h)
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255
    m = re.match(
        r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)", c
    )
    if m:
        r, g, b = map(int, m.groups())
        return (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255
    m = re.match(
        r"hsla?\(\s*([\d.]+)\s*,\s*([\d.]+)%\s*,\s*([\d.]+)%", c
    )
    if m:
        h, s, l = float(m.group(1)) / 360.0, float(m.group(2)) / 100.0, float(m.group(3)) / 100.0
        if s == 0:
            return l
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
        r, g, b = hue2rgb(p, q, h + 1 / 3), hue2rgb(p, q, h), hue2rgb(p, q, h - 1 / 3)
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    return None


def _is_dark(color: str, vars: dict[str, str] | None = None) -> bool:
    color = _resolve_vars(color, vars or {})
    c = color.strip().lower()
    if c in ("transparent", "none", "initial", "inherit"):
        return True  # not a light surface
    if "gradient" in c:
        # gradients: judge by the first color stop (craft highlights allowed)
        first = c.split(",", 1)[1] if "," in c else c
        lum = _luminance_of(first.strip())
        if lum is None:
            return True  # unparseable stop: not provably a light surface
        return lum < 0.35
    lum = _luminance_of(c)
    if lum is None:
        # Unparseable opaque color: cannot verify it is dark -> fail closed.
        return False
    return lum < 0.35


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
            # Light surfaces are surfaces: any opaque background with high
            # luminance fails, however it is spelled (hex, name, hsl).
            # Gradient craft: judge by the first color stop only.
            probe = val
            if "gradient" in val.lower():
                parts = val.split(",", 1)
                probe = parts[1] if len(parts) > 1 else val
            lum = _luminance_of(_resolve_vars(probe, _root_vars(css)))
            if lum is not None and lum >= 0.6:
                v.append(f"NO LIGHT SURFACES: `{selector}` has light "
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
    violations += check_light_text(css)
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
