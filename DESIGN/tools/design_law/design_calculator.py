#!/usr/bin/env python3
"""Naya design law calculator v1 — 0-100 page conformance scorer.

Scores a page's HTML+CSS against the machine-checkable predicates of
DESIGN/contract/naya-design-contract-v1.machine.json.

HONEST LIMITS (v1): this checks contract conformance, not beauty. It cannot
judge taste, hierarchy feel, or the rendered experience — Law "score the
experience, never the code" still requires a human/Naya eye. A 100 here means
"violates no machine law," not "triple-A."

Usage: python3 design_calculator.py <page.html> [--contract <machine.json>]
"""
import json
import re
import sys
from pathlib import Path

DEFAULT_CONTRACT = Path(__file__).resolve().parent.parent.parent / "contract" / "naya-design-contract-v1.machine.json"


def load_contract(path):
    with open(path) as f:
        return json.load(f)


def allowed_colors(contract):
    vals = set()
    for section in ("field", "light", "extended"):
        vals.update(str(v).lower() for v in contract.get(section, {}).values() if isinstance(v, str))
    vals.add(contract["soul"].lower())
    for s in contract["spectrum_law_order"]:
        vals.add(s["hex"].lower())
    for t in contract["truth"].values():
        vals.add(t.lower())
    vals.add(contract["room_accents"]["settings"].lower())
    # rgba() forms of the same palette
    vals.update({
        "rgba(248,247,251,.72)", "rgba(248,247,251,.55)",
        "rgba(255,255,255,.12)", "rgba(255,255,255,.20)",
        "rgba(255,255,255,.10)",
        "rgba(0,0,0,.55)", "rgba(0,0,0,.4)",
        "rgba(160,107,255,.35)", "rgba(28,18,38,.18)", "rgba(28,18,38,.11)",
    })
    return vals


def extract_colors(text):
    hexes = {m.lower() for m in re.findall(r"#[0-9a-fA-F]{3,8}\b", text)}
    rgbas = {re.sub(r"\s+", "", m).lower() for m in re.findall(r"rgba?\([^)]*\)", text)}
    return hexes | rgbas


def extract_font_sizes(text):
    return [float(m) for m in re.findall(r"font-size:\s*([0-9.]+)px", text)]


def check_no_private_colors(text, contract):
    colors = extract_colors(text)
    # var() references are always allowed; strip them from scrutiny
    allowed = allowed_colors(contract)
    bad = sorted(c for c in colors if c not in allowed)
    return bad


def check_type_floor(text, contract):
    floor = contract["predicates"]["detail_never_below_px"]
    # Law 52: 11px kickers (uppercase, tracked) are legal — exempt sizes tied
    # to kicker/eyebrow/tagline-classed elements, via stylesheet or inline style.
    kicker_sizes = []
    for style in re.findall(r"<style[^>]*>(.*?)</style>", text, re.I | re.S):
        for m in re.finditer(r"([^{}]+)\{([^}]*)\}", style):
            if re.search(r"kicker|eyebrow|tagline", m.group(1), re.I):
                kicker_sizes += [float(s) for s in re.findall(r"font-size:\s*([0-9.]+)px", m.group(2))]
    for m in re.finditer(r'<[^>]*class="[^"]*(?:kicker|eyebrow|tagline)[^"]*"[^>]*style="[^"]*font-size:\s*([0-9.]+)px', text, re.I):
        kicker_sizes.append(float(m.group(1)))
    small = []
    for s in extract_font_sizes(text):
        if s < floor:
            if s in kicker_sizes:
                kicker_sizes.remove(s)  # consume one exempt occurrence
            else:
                small.append(s)
    return sorted(small)


def check_kicker_words(text, contract):
    cap = contract["predicates"]["tagline_max_words"]
    # kicker-styled elements: class contains kicker/eyebrow/tagline
    hits = []
    for m in re.finditer(r'class="[^"]*(?:kicker|eyebrow|tagline)[^"]*"[^>]*>([^<]{1,120})<', text, re.I):
        words = len(m.group(1).split())
        if words > cap:
            hits.append((m.group(1).strip()[:60], words))
    return hits


def check_idle_rims(text, contract):
    minimum = contract["predicates"]["lighting.idle.border_min_px"]
    # interactive selectors should declare a border at rest
    thin = []
    for sel in re.finditer(r"(\.[a-z0-9_.-]*(?:btn|card|input|pill|tab)[a-z0-9_.-]*)\s*\{([^}]*)\}", text, re.I):
        body = sel.group(2)
        bm = re.search(r"border(?:-width)?\s*:\s*([0-9.]+)px", body)
        if bm and float(bm.group(1)) < minimum:
            thin.append((sel.group(1), bm.group(1)))
    return thin


def score_page(path, contract):
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    checks = []
    bad_colors = check_no_private_colors(text, contract)
    checks.append(("no_private_colors", 30, not bad_colors,
                   f"{len(bad_colors)} off-token colors" if bad_colors else "all colors from tokens"))
    small = check_type_floor(text, contract)
    checks.append(("type_floor_12px", 20, not small,
                   f"sizes below 12px: {small}" if small else "no text below 12px"))
    long_kickers = check_kicker_words(text, contract)
    checks.append(("kicker_word_cap", 15, not long_kickers,
                   f"{len(long_kickers)} over-long kickers" if long_kickers else "kickers within cap"))
    thin = check_idle_rims(text, contract)
    checks.append(("idle_rim_1.5px", 15, not thin,
                   f"{len(thin)} thin rims" if thin else "rims meet 1.5px"))
    has_tokens_link = "TOKENS.css" in text or ":root" in text
    checks.append(("tokens_present", 20, has_tokens_link,
                   "no TOKENS.css link or :root found" if not has_tokens_link else "token system referenced"))
    total = sum(w for _, w, ok, _ in checks if ok)
    return total, checks


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    page = sys.argv[1]
    contract_path = Path(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[2] == "--contract" else DEFAULT_CONTRACT
    contract = load_contract(contract_path)
    total, checks = score_page(page, contract)
    print(f"design score: {total}/100  ({page})")
    for name, weight, ok, detail in checks:
        mark = "PASS" if ok else "FAIL"
        print(f"  [{mark}] {name} ({weight}pts) — {detail}")
    print(f"ship threshold: {contract['predicates']['gates.ship_threshold'] * 10:.0f}/100 (machine laws only — human eye still required)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
