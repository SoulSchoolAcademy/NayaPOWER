#!/usr/bin/env python3
"""
check_design.py — Naya Design Law executable checker.

Enforces THE NAYA DESIGN CONTRACT V1 (CANDIDATE) against an HTML file or CSS text.
FAILS (exit 1) on any FAIL-severity violation; warnings do not fail.

Usage:
    python3 check_design.py <file.html|file.css> [--room mail] [--json]
    python3 check_design.py "<style>...</style>"   # raw CSS/HTML text
    python3 check_design.py --stdin [--room mail]

Checks: D1 (zoom), D2-D4 (room accents), D9 (18px body), SPECTRUM (non-token
chromatic colors), LIGHTBG, BTN (button law), DIVBTN, MAXW, MAXIS, AMBERROSE,
BODYCOLOR, PURPLEFILL, RM (reduced motion). Warnings: jewel clip-path drift,
missing eco-bottombar, thin token system.
"""
import json
import os
import re
import sys

# ---------------------------------------------------------------- tokens ---
FIELD_HEXES = {
    "#0b0d12", "#010103", "#12151d", "#171b25", "#252b39",
    "#050505", "#000000", "#ffffff", "#f5f7fb", "#aab2bf",
}
SPECTRUM_HEXES = {
    "#9d75ff", "#6675ff", "#55b9ee", "#40d3bb", "#55e39a", "#b8ee57",
    "#e8b64c", "#f1d75a", "#ff9a5a", "#ff7a3d", "#ff5a6e", "#d86cff",
}
TOKEN_HEXES = FIELD_HEXES | SPECTRUM_HEXES

ROOM_HEX = {
    "today": "#d86cff", "reports": "#6675ff", "library": "#55b9ee",
    "smart-doors": "#40d3bb", "ledger": "#e8b64c", "connections": "#ff9a5a",
    "lists": "#9d75ff", "mail": "#ff7a3d", "spaces": "#b8ee57",
    "smart-grow": "#55e39a",
}
ROOM_TOKEN = {
    "today": "magenta", "reports": "indigo", "library": "blue",
    "smart-doors": "teal", "ledger": "gold", "connections": "orange",
    "lists": "purple", "mail": "rich-orange", "spaces": "lime",
    "smart-grow": "emerald",
}
# Known wrong accents recorded in the drift register (D2-D4 = HARD)
ROOM_WRONG = {
    "mail": ({"#3ca8ff"}, "D2"),
    "spaces": ({"#7c3aed"}, "D3"),
    "connections": ({"#9d75ff"}, "D4"),
}
JEWEL_CLIP_EXACT = "polygon(50% 0%, 86% 28%, 74% 82%, 50% 100%, 26% 82%, 14% 28%)"

ACCENT_VAR_RE = re.compile(
    r"accent|room|^--(ml|sc|cx|cn|rs|li)\b|--day\b|--door\b|--gem\b|--glow\b", re.I
)
BTN_SEL_RE = re.compile(
    r"(^|[\s>+~,])(button|\.btn\b|\.primary\b|a\.btn|input\[type=['\"]?(submit|button)['\"]?\])"
    r"|\[role=['\"]?button['\"]?\]"
)
ROOT_SEL_RE = re.compile(r"^(body|html)$|\.app$|#app$|^main$|chassis|room", re.I)

# ---------------------------------------------------------------- helpers --
def norm_hex(h):
    h = h.lower()
    if len(h) == 4:  # #rgb
        return "#" + h[1] * 2 + h[2] * 2 + h[3] * 2
    if len(h) == 5:  # #rgba -> drop alpha
        return "#" + h[1] * 2 + h[2] * 2 + h[3] * 2
    if len(h) == 9:  # #rrggbbaa -> drop alpha
        return h[:7]
    return h


def hex_to_rgb(h):
    h = norm_hex(h).lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rel_luminance(rgb):
    def ch(c):
        c /= 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def rgb_to_hsl(rgb):
    r, g, b = (c / 255.0 for c in rgb)
    mx, mn = max(r, g, b), min(r, g, b)
    l = (mx + mn) / 2.0
    if mx == mn:
        return 0.0, 0.0, l
    d = mx - mn
    s = d / (2.0 - mx - mn) if l > 0.5 else d / (mx + mn)
    if mx == r:
        h = (g - b) / d + (6 if g < b else 0)
    elif mx == g:
        h = (b - r) / d + 2
    else:
        h = (r - g) / d + 4
    return h * 60.0, s, l


def is_gray(h):
    r, g, b = hex_to_rgb(h)
    return r == g == b


def near_token(c, tol=25):
    """Same-family tolerance: within `tol` RGB Euclidean distance of a token."""
    r, g, b = hex_to_rgb(c)
    for t in TOKEN_HEXES:
        tr, tg, tb = hex_to_rgb(t)
        if (r - tr) ** 2 + (g - tg) ** 2 + (b - tb) ** 2 <= tol * tol:
            return True
    return False


HEX_RE = re.compile(r"#([0-9a-fA-F]{3,8})\b")
RGB_RE = re.compile(r"rgba?\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})")


def colors_in(value):
    """Yield normalized hex colors found in a CSS value (hex + rgb())."""
    out = []
    for m in HEX_RE.finditer(value):
        out.append(norm_hex("#" + m.group(1)))
    for m in RGB_RE.finditer(value):
        r, g, b = (max(0, min(255, int(x))) for x in m.groups())
        out.append("#%02x%02x%02x" % (r, g, b))
    return out


# ---------------------------------------------------------------- parsing --
def split_top_blocks(css):
    blocks = []
    i, n = 0, len(css)
    while i < n:
        j = css.find("{", i)
        if j == -1:
            break
        prelude = css[i:j].strip()
        depth, k = 1, j + 1
        while k < n and depth:
            if css[k] == "{":
                depth += 1
            elif css[k] == "}":
                depth -= 1
            k += 1
        blocks.append((prelude, css[j + 1:k - 1]))
        i = k
    return blocks


def parse_decls(body):
    decls = {}
    for part in body.split(";"):
        if ":" in part:
            prop, _, val = part.partition(":")
            prop, val = prop.strip().lower(), val.strip()
            if prop:
                decls[prop] = val
    return decls


def parse_css(css, media=None, rules=None):
    if rules is None:
        rules = []
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    for prelude, body in split_top_blocks(css):
        pl = prelude.strip()
        if pl.lower().startswith("@media"):
            parse_css(body, media=pl, rules=rules)
        elif pl.startswith("@"):
            rules.append((pl, {}, media))  # at-rule marker (e.g. keyframes)
        else:
            for sel in pl.split(","):
                sel = sel.strip()
                if sel:
                    rules.append((sel, parse_decls(body), media))
    return rules


def extract_css_and_meta(text):
    """Return (css_text, viewport_content_or_None, raw_text)."""
    styles = re.findall(r"<style[^>]*>(.*?)</style>", text, re.S | re.I)
    css = "\n".join(styles)
    # inline styles -> pseudo rules tagged with their element
    for tag, style in re.findall(r"<(\w+)[^>]*?\sstyle=\"([^\"]*)\"", text, re.I):
        css += "\n%s[inline]{%s}" % (tag.lower(), style)
    viewport = None
    m = re.search(r"<meta[^>]*name=[\"']viewport[\"'][^>]*>", text, re.I)
    if m:
        c = re.search(r"content=[\"']([^\"']*)[\"']", m.group(0), re.I)
        if c:
            viewport = c.group(1)
    is_html = bool(re.search(r"<html|<!doctype|<style|<body", text, re.I))
    if not is_html:
        css = text  # raw CSS text input
    return css, viewport, text


def custom_props(rules):
    props = {}
    for _sel, decls, _media in rules:
        for p, v in decls.items():
            if p.startswith("--"):
                props[p] = v
    return props


def rules_for(rules, selector):
    return [(s, d, m) for s, d, m in rules if s.strip().lower() == selector]


# ---------------------------------------------------------------- checks ---
def check(source_text, room=None):
    """Run all checks. Returns list of violation dicts."""
    v = []
    css, viewport, raw = extract_css_and_meta(source_text)
    rules = parse_css(css)
    props = custom_props(rules)

    def add(cid, severity, message):
        v.append({"id": cid, "severity": severity, "message": message})

    # ---- D1: pinch zoom ------------------------------------------------
    if viewport is not None:
        low = viewport.lower().replace(" ", "")
        if "user-scalable=no" in low:
            add("D1", "FAIL", "viewport blocks pinch zoom: user-scalable=no (NC-12.4)")
        m = re.search(r"maximum-scale=([0-9.]+)", low)
        if m and float(m.group(1)) <= 1.0:
            add("D1", "FAIL", "viewport blocks pinch zoom: maximum-scale=%s (NC-12.4)" % m.group(1))
    else:
        add("VIEWPORT", "WARN", "no viewport meta found")

    # ---- D2-D4 / room accents ------------------------------------------
    if room:
        room = room.lower().replace("_", "-")
        expected = ROOM_HEX.get(room)
        if expected:
            accent_vars = {k: val for k, val in props.items() if ACCENT_VAR_RE.search(k)}
            token_name = ROOM_TOKEN.get(room, "")
            found = any(
                expected in colors_in(val) or ("var(--%s" % token_name) in val.replace(" ", "")
                for val in accent_vars.values()
            ) or expected in [c for _s, d, _m in rules for val in d.values() for c in colors_in(val)]
            wrong, did = ROOM_WRONG.get(room, (set(), "ROOM"))
            for name, val in accent_vars.items():
                if set(colors_in(val)) & wrong:
                    add(did, "FAIL", "room '%s': wrong room accent in %s (drift %s); expected %s"
                        % (room, name, did, expected))
            if not found:
                add(did, "FAIL", "room '%s': expected accent %s not declared (NC-2.8)" % (room, expected))

    # ---- D9: body 18px ---------------------------------------------------
    is_presentation = (
        props.get("--fs-headline", "").strip() == "24px"
        and props.get("--fs-sub", "").strip() == "18px"
        and props.get("--fs-body", "").strip() == "14px"
    )
    if not is_presentation:
        body_fs = None
        for _s, decls, _m in rules_for(rules, "body"):
            if "font-size" in decls:
                body_fs = decls["font-size"]
        if body_fs is None and "var(--fs-body)" not in css:
            # also resolve via :root var
            if props.get("--fs-body"):
                body_fs = props["--fs-body"]
        if body_fs is None:
            add("D9", "FAIL", "no explicit body font-size declared; law requires 18px (NC-3.1)")
        else:
            m = re.match(r"\s*([0-9.]+)px", body_fs)
            if m:
                if float(m.group(1)) < 18:
                    add("D9", "FAIL", "body font-size %s < 18px (NC-3.1, NC-12.1)" % body_fs.strip())
            elif "18px" not in body_fs and "var(--fs-body)" not in body_fs:
                add("D9", "FAIL", "body font-size '%s' is not 18px (NC-3.1)" % body_fs.strip()[:40])

    # ---- BODYCOLOR: white body text --------------------------------------
    white_ok = {"#ffffff", "#f5f7fb", "#f4f6fb", "#f8f7fb", "white",
                "var(--ink)", "var(--white)"}
    for _s, decls, _m in rules_for(rules, "body"):
        col = decls.get("color", "").strip().lower()
        if col and not col.startswith("var(") and col not in white_ok:
            add("BODYCOLOR", "FAIL", "body text color '%s' is not white (A-LAW-07)" % col[:30])
        elif col.startswith("var(") and col not in white_ok:
            add("BODYCOLOR", "WARN", "body text color '%s' not resolvable to white" % col[:30])

    # ---- SPECTRUM + AMBERROSE + LIGHTBG + PURPLEFILL ----------------------
    for sel, decls, _media in rules:
        if sel.startswith("@"):
            continue
        for prop, val in decls.items():
            if prop in ("background", "background-color"):
                # solid purple fill (NC-12.2)
                if re.match(r"^\s*#9d75ff\s*$", val, re.I):
                    add("PURPLEFILL", "FAIL",
                        "solid purple fill on '%s' — purple is glow, not paint (NC-12.2)" % sel[:40])
                # light backgrounds (NC-1.3)
                if "gradient" not in val.lower():
                    for c in colors_in(val):
                        if rel_luminance(hex_to_rgb(c)) >= 0.55:
                            add("LIGHTBG", "FAIL",
                                "light background %s on '%s' (NC-1.3: no light mode)" % (c, sel[:40]))
                            break
                else:
                    # Gradients: only fail when EVERY stop is light (an all-light
                    # wash). Mixed stops are legitimate glows/sheens/jewel cores.
                    stops = colors_in(val)
                    if stops and all(rel_luminance(hex_to_rgb(c)) >= 0.55 for c in stops):
                        add("LIGHTBG", "FAIL",
                            "all-light gradient on '%s' (NC-1.3: no light mode)" % sel[:40])
            for c in colors_in(val):
                if is_gray(c):
                    continue  # grayscale (incl. white/black) is field/light, not spectrum
                if c in TOKEN_HEXES:
                    continue  # exact token
                h, s, li = rgb_to_hsl(hex_to_rgb(c))
                if ((30 <= h <= 52) or h >= 330 or h <= 12) and s > 0.45 and li > 0.45:
                    add("AMBERROSE", "FAIL",
                        "amber/rose-pink color %s forbidden (NC-12.3)" % c)
                    continue
                if near_token(c):
                    continue  # same-family approximation of a token
                lum = rel_luminance(hex_to_rgb(c))
                if lum < 0.025 or lum > 0.88:
                    continue  # near-black field variant / near-white light
                add("SPECTRUM", "FAIL",
                    "non-token chromatic color %s in '%s: %s' (DC-030)" % (c, sel[:40], prop))

    # ---- BTN: button law --------------------------------------------------
    for sel, decls, _media in rules:
        if sel.startswith("@") or not BTN_SEL_RE.search(sel):
            continue
        if ":hover" in sel or ":active" in sel or ":focus" in sel:
            continue  # themed/chrome ignition on hover is sanctioned
        col = decls.get("color", "").strip().lower()
        if col and col not in {"#ffffff", "#fff", "white", "#f5f7fb",
                               "var(--ink)", "var(--white)", "inherit"}:
            add("BTN", "FAIL", "colored text '%s' on button '%s' — never, ever (A-LAW-06)"
                % (col[:30], sel[:40]))
        bg = decls.get("background", decls.get("background-color", "")).strip().lower()
        if bg and "gradient" not in bg:
            for c in colors_in(bg):
                if is_gray(c) and rel_luminance(hex_to_rgb(c)) < 0.08:
                    continue  # black / near-black fill is the law
                add("BTN", "FAIL", "solid non-black fill %s on button '%s' (NC-5.1)"
                    % (c, sel[:40]))
                break

    # ---- DIVBTN / MAXIS / MAXW --------------------------------------------
    if re.search(r"<div[^>]*\bonclick", raw, re.I):
        add("DIVBTN", "FAIL", "clickable div found — use real <button> (NC-12.5)")
    if "app.nayanet.technology" in raw:
        add("MAXIS", "FAIL", "link to app.nayanet.technology (NC-12.7)")
    for sel, decls, _media in rules:
        if sel.startswith("@") or not ROOT_SEL_RE.search(sel):
            continue
        mw = decls.get("max-width", "")
        m = re.match(r"\s*([0-9.]+)px", mw)
        if m and float(m.group(1)) < 1400:
            add("MAXW", "FAIL", "max-width cap %s on '%s' (NC-6.14, NC-12.6)"
                % (mw.strip(), sel[:40]))

    # ---- RM: reduced motion ------------------------------------------------
    has_anim = any(
        not sel.startswith("@")
        and (decls.get("animation", "").strip() not in ("", "none")
             or decls.get("transition", "").strip() not in ("", "none"))
        for sel, decls, _media in rules
    )
    has_rm = any("prefers-reduced-motion" in (media or "") for _s, _d, media in rules)
    if has_anim and not has_rm:
        add("RM", "FAIL", "animations present without prefers-reduced-motion handling (NC-7.7)")

    # ---- warnings: jewel drift / bottombar / token thinness ----------------
    for sel, decls, _media in rules:
        if sel.startswith("@"):
            continue
        if "jewel" in sel and "clip-path" in decls:
            got = re.sub(r"\s+", " ", decls["clip-path"]).strip().lower()
            want = JEWEL_CLIP_EXACT.lower()
            got_n = re.sub(r"(\d)(%|,)", r"\1\2", got)
            if got.replace(" ", "") != want.replace(" ", ""):
                add("JEWEL", "WARN", "jewel clip-path drifts from Code-exact polygon (D8)")
                break
    if room and ".eco-bottombar" not in css:
        add("BOTTOMBAR", "WARN", "shared eco-bottombar not found on room '%s' (D10)" % room)
    root_vars = [p for s, d, _m in rules_for(rules, ":root") for p in d if p.startswith("--")]
    if root_vars and len(set(root_vars)) < 15:
        add("TOKENS", "WARN", "thin :root token system (%d vars) — adopt canonical map (D12)"
            % len(set(root_vars)))

    return v


# ---------------------------------------------------------------- CLI ------
def infer_room(path):
    stem = os.path.splitext(os.path.basename(path))[0].lower()
    stem = re.sub(r"[-_]?2$", "", stem)
    mapping = {"connect": "smart-doors", "index": None, "index-2": None, "start": None}
    return mapping.get(stem, stem if stem in ROOM_HEX else None)


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description="Naya Design Law checker (Contract V1, CANDIDATE)")
    ap.add_argument("source", nargs="?", help="HTML/CSS file path, raw CSS/HTML text, or '-'")
    ap.add_argument("--stdin", action="store_true", help="read source from stdin")
    ap.add_argument("--room", default=None, help="room name for accent checks (e.g. mail)")
    ap.add_argument("--json", action="store_true", help="JSON output")
    args = ap.parse_args(argv)

    if args.stdin or args.source == "-":
        text = sys.stdin.read()
        room = args.room
    elif args.source and os.path.exists(args.source):
        with open(args.source, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
        room = args.room or infer_room(args.source)
    elif args.source:
        text = args.source
        room = args.room
    else:
        ap.error("no source given")

    violations = check(text, room=room)
    fails = [x for x in violations if x["severity"] == "FAIL"]
    warns = [x for x in violations if x["severity"] == "WARN"]

    if args.json:
        print(json.dumps({"room": room, "fail": len(fails) > 0,
                          "violations": violations}, indent=2))
    else:
        for x in violations:
            print("[%s] %s: %s" % (x["severity"], x["id"], x["message"]))
        print("---")
        print("room=%s fail=%d warn=%d -> %s"
              % (room, len(fails), len(warns), "FAIL" if fails else "PASS"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
