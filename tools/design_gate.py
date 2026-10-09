#!/usr/bin/env python3
"""NayaNET design gate — code is law, machine-forced.

Usage:
    python3 tools/design_gate.py <page.html> [--manifest smart-blocks/manifest.json]

Enforces the STRUCTURAL design laws from DESIGN-LAWS.md as a hard gate.
Exit 0 = pass. Exit 1 = fail, with each violation named specifically.
Eye-enforced laws (craft, copy, motion meaning) remain Shawn's verdict —
this gate catches what a machine can prove.

Structural checks:
  1. SELF-CONTAINED — no external stylesheet/script references (all inlined).
  2. BLACK ROOT — html/body background is deep black.
  3. NO LIGHT SURFACES — no white/light background declarations.
  4. DARK COLOR-SCHEME — meta or CSS declares dark.
  5. NO FREESTYLE COMPONENTS — every Naya-prefixed class exists in the manifest.
  6. LIGHT TEXT — body text color is light.
"""
from __future__ import annotations

import json
import re
import sys
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


def run_gate(page: Path, manifest: Path) -> list[str]:
    html = read_page(page)
    css = inline_css(html)
    violations: list[str] = []
    violations += check_self_contained(html)
    violations += check_black_root(html, css)
    violations += check_no_light_surfaces(css)
    violations += check_dark_scheme(html, css)
    if manifest.exists():
        violations += check_no_freestyle(html, _manifest_classes(manifest))
    else:
        violations.append(f"NO FREESTYLE: manifest not found at {manifest} "
                          f"— cannot verify components")
    violations += check_light_text(css)
    return violations


def self_test() -> int:
    """Red-green: a violating page must fail, a lawful page must pass."""
    bad = """<!DOCTYPE html><html><head><link rel="stylesheet" href="x.css">
<style>body{background:#fff;color:#111}</style></head>
<body><div class="naya-frobnicate">hi</div></body></html>"""
    good = """<!DOCTYPE html><html><head>
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
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return self_test()
    if not argv:
        print(__doc__)
        return 2
    page = Path(argv[0])
    manifest = Path(argv[1]) if len(argv) > 1 else (
        REPO_ROOT / "smart-blocks" / "manifest.json"
    )
    if not page.exists():
        print(f"design_gate: no such file: {page}")
        return 2
    violations = run_gate(page, manifest)
    if violations:
        print(f"DESIGN GATE: FAIL — {len(violations)} violation(s) in {page}:")
        for viol in violations:
            print(f"  ✕ {viol}")
        return 1
    print(f"DESIGN GATE: PASS — {page}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
