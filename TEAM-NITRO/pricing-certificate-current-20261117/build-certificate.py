#!/usr/bin/env python3
"""Pricing Certificate Current round (2026-11-17) — bring /free to the
CURRENT certificate (the identity treatment, staged 8c641f96).

BASE (regenerated first, fail-stop if moved): the pricing-fix tip —
  walk 3,293,555 B sha 46bc52e5... | entry 315,878 B sha 06b08242... |
  worker 3,630,970 B sha 59e65835... | live staged /free must still serve
  the tip entry before anything is staged.
SOURCE (the current treatment, harvested verbatim, never rebuilt):
  identity-fixed.html 376,814 B sha 8c641f96... (Round 4 H1 trophy name +
  Round 5 H3/H1/H2, staged on naya-walk-beginning-staging) — the Micheal
  certificate's treatment (Nº 000204, Round 2 2026-11-15 21:58Z), carried
  through Rounds 3-5. The walk's certificate file walk-beginning-fixed.html
  sha df17ac67... (Nov 14) is the walk bundle the /free/walk derives from;
  the certificate VIEW in the walk is /identity.html, so identity is the
  harvest source. SN-2922 is the bar: official, glowing, solid; mail ID
  first-class.

THE HARVEST (what /free gains, each piece extracted from the identity
bytes by anchor and asserted, never retyped):
  H1 NAME — the trophy: obsidian gradient body, chrome 1px stroke,
     purple clone behind (Round 4 clone trick, 01:52Z), hover pop
     (lift 2px + purple halo), name-settle arrival, certified in-flow
     with text-shadow none. Geometry (size/position) KEPT from /free —
     the paint is the harvest, not the size.
  H2 PANELS — obsidian fills (#101013->#050505->#070708) in place of the
     blue/brown fills; labels WHITE (the glow carries the color);
     values TYPE letter-by-letter with a caret in the panel's own
     color on restore + stamp (instant while composing).
  H3 TOKENS — the gray lift (Round 2 F4): --silver/--muted #f2f2f6 ->
     #ffffff, --faint -> white 0.88, --purple #a855f7 -> #a06bff (ONE
     purple), --hair cream -> white; every code #f2f2f6 text rule ->
     white; cream/silver-white rgba tints -> white at the same alpha.
     The dead harvested .enter rule (live entrance, verbatim) is left
     alone — its #302054 / rgba(168,85,247) are purple-family glow in
     a rule no element uses, not gray text.
  H4 AGREEMENT — the official sentence (typed face only, Round 5 H1)
     under ENTER + the clone-trick ⓘ + the one-paragraph-at-a-time
     reader (Round 5 H2), harvested whole: CSS + HTML + JS. Hidden in
     the certified and taken states (Round 5 H1 amended).
NOT harvested (named, not hidden): the membership sentence
  (.cert-member, Round 3 H1 — absent on /free; needs its own geometry
  funding on /free's certified face) and the H6 green taken message
  (.hub-note.taken-note — absent on /free). Both are outside the
  brief's five diff dimensions; follow-ons if the captain wants them.

Builds entirely in memory and stages to naya-pricing-free-staging ONLY.
Pricing v78 untouched. Nothing live, no merge.
"""
import difflib
import gzip
import hashlib
import importlib.util
import json
import os
import re
import sys

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
sys.path.insert(0, os.path.expanduser("~/workspace/ninaya/integration"))

FIXDIR = os.path.expanduser("~/workspace/team-nitro/pricing-fix-20261117")
F4 = os.path.expanduser("~/workspace/team-nitro/pricing-free-entry-20261116")
HERE = os.path.expanduser("~/workspace/team-nitro/pricing-certificate-current-20261117")
IDENTITY_PATH = os.path.expanduser(
    "~/workspace/team-nitro/walk-v23-assembly-20261114/identity-fixed.html")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_fixmod = load("pricingfix", os.path.join(FIXDIR, "build-fix.py"))
_bt = _fixmod._bt
_bf = _bt._bf
_fix = _bt._fix
_fo = _bt._fo
_marc = _bt._marc
_sim = _bt._sim
replace_once = _bf.replace_once

FREE_HOST = "https://naya-pricing-free-staging.nayapower.workers.dev"
PRICING_HOST = "https://naya-pricing-f4-staging.nayapower.workers.dev"
LIVE = "https://nayanet.app"
IDENTITY_HOST = "https://naya-walk-beginning-staging.nayapower.workers.dev"

BASE_WALK_SHA = "46bc52e54ac02e87cdad0ae2924ce35555671333ce3c7cd96676f17d86253fa1"
BASE_ENTRY_SHA = "06b08242c72e9d0b8f28037df3b93e74c5955e6702f358d0a07fff799edf58fd"
# PREV_ENTRY_SHA: the first staging of THIS round (2026-11-17 18:59Z) — it
# shipped the reader IIFE with its grouping paren dropped (}(); instead of
# })();), a JS syntax error that kills the whole inline block in a browser.
# The fix re-run re-derives from the filed chain, not from live, but the
# step-0b live guard must accept these bytes as the expected live state.
PREV_ENTRY_SHA = "72b18a32fd8d6bc0e876b1ae36a6f633fa32d453e224ff139b0a123c63797262"
BASE_WORKER_SHA = "59e658353c079ca4ce3f8c7f8d37341efdd9bec92770bee22c1c77e48761fb90"
IDENTITY_SHA = "8c641f96d31818b610d1a243d945dfb5c68e6016e036b7afb11b72445330013d"
PRICING_V78_SHA = "ca2eafeb896c763ae2459b4a10b8715e726765ced607c0aab3640d27e6c39ae2"
SW_SHA = "abac2ab507fc162788d9bdcd60f895049222e125d1445a4870be71342625d6a3"
MANI_SHA = "b4abd81c41e85f4149be355f740dd8ff9b136f6ea85e8b5874073a0686c67e81"


def sha(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode()).hexdigest()


def extract_rule(text, start_marker, what):
    """Extract one CSS/JS rule starting at start_marker, brace-counted
    (comments skipped), returned verbatim including its leading indent."""
    i = text.find(start_marker)
    assert i >= 0, f"harvest anchor missing: {what}"
    assert text.count(start_marker) == 1, f"harvest anchor not unique: {what}"
    j = text.find("{", i)
    assert j > i, f"no open brace: {what}"
    depth = 0
    k = j
    while k < len(text):
        if text.startswith("/*", k):
            e = text.find("*/", k + 2)
            assert e > 0, f"unterminated comment in {what}"
            k = e + 2
            continue
        c = text[k]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return text[i:k + 1]
        k += 1
    raise AssertionError(f"unbalanced braces: {what}")


def extract_lines(text, start_marker, end_marker, what):
    """Extract consecutive lines from the line containing start_marker
    through the line containing end_marker, verbatim."""
    lines = text.split("\n")
    si = next(i for i, ln in enumerate(lines) if start_marker in ln)
    ei = next(i for i, ln in enumerate(lines) if end_marker in ln and i >= si)
    assert sum(1 for ln in lines if start_marker in ln) == 1, f"not unique: {what}"
    return "\n".join(lines[si:ei + 1])


def swap_outside_comments(text, old, new, expect, what):
    """Replace old->new everywhere EXCEPT inside /* */ comments.
    Asserts the total replacement count == expect."""
    out = []
    n = 0
    i = 0
    while i < len(text):
        if text.startswith("/*", i):
            e = text.find("*/", i + 2)
            assert e > 0, f"unterminated comment while swapping {what}"
            out.append(text[i:e + 2])
            i = e + 2
            continue
        j = text.find(old, i)
        k = text.find("/*", i)
        if j < 0 or (0 <= k < j):
            out.append(text[i:(k if k >= 0 else len(text))])
            i = k if k >= 0 else len(text)
            continue
        out.append(text[i:j])
        out.append(new)
        n += 1
        i = j + len(old)
    assert n == expect, f"{what}: replaced {n}, expected {expect}"
    return "".join(out)


def harvest_identity():
    raw = open(IDENTITY_PATH, "rb").read()
    assert len(raw) > 0, "identity file empty — STOP (flake damage?)"
    assert sha(raw) == IDENTITY_SHA, f"identity source moved: {sha(raw)}"
    t = raw.decode("utf-8")
    h = {}
    # H1 — the name. Base rule (font-size line swapped for /free's own
    # geometry at apply time); clone x2; settle; certified; hover x4.
    h["name_base"] = extract_rule(
        t, "    .cert-name { position: absolute; left: 50%; transform: translateX(-50%);",
        "name base")
    h["clone_a"] = extract_rule(
        t, "    .cert-name::before { content: attr(data-text); position: absolute; inset: 0;",
        "clone ::before (body)")
    h["clone_b"] = extract_rule(
        t, "    .cert-name::before { z-index: -1; transform: translateY(4px) scale(1.02); opacity: 0.45;",
        "clone ::before (paint)")
    h["settle"] = extract_rule(
        t, "    .cert-name.name-settle { animation: name-settle .5s cubic-bezier(.16,.84,.22,1); }",
        "name-settle rule")
    h["settle_kf"] = extract_rule(
        t, "    @keyframes name-settle { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: translateY(0); } }",
        "name-settle keyframes")
    h["name_certified"] = extract_rule(
        t, "    .cert-plaque.is-certified .cert-name { position: relative; left: auto; bottom: auto; transform: none;",
        "certified name")
    h["hover"] = "\n".join([
        extract_rule(t, "    .cert-name:hover { filter: drop-shadow(0 12px 26px rgba(0,0,0,0.75)) drop-shadow(0 0 34px rgba(160,107,255,0.6)); }",
                     "hover base"),
        extract_rule(t, "    .cert-plaque:not(.is-certified) .cert-name:hover { transform: translateX(-50%) translateY(-2px); }",
                     "hover composing"),
        extract_rule(t, "    .cert-plaque.is-certified .cert-name:hover { transform: translateY(-2px); }",
                     "hover certified"),
        extract_rule(t, "    .cert-name:hover::before { opacity: 0.9; filter: blur(16px); }",
                     "hover clone"),
    ])
    # H2 — panels: label rule + typing caret block.
    h["label"] = extract_rule(
        t, "    .id-box-label { font-size: 0.66rem; font-weight: 700; letter-spacing: 0.36em;",
        "panel label")
    h["caret"] = extract_lines(
        t, "    .id-box-value.typing::after { content: \"\"; display: inline-block;",
        "    @keyframes caret-blink { 50% { opacity: 0; } }",
        "typing caret")
    # H4 — agreement: sentence rule, info button, reader.
    h["agree"] = extract_rule(
        t, "    .cert-agree { position: relative; margin-top: 10px; font-size: 0.82rem; font-weight: 600;",
        "agree line")
    h["info"] = extract_lines(
        t, "    .cert-info { position: relative; z-index: 0;",
        "    .cert-info:hover { border-color: var(--royal);",
        "info button")
    h["reader_css"] = extract_lines(
        t, "    .cert-info-reader:not([hidden]) { position: absolute;",
        "    .cert-info-reader .cert-info-x { position: absolute;",
        "reader css")
    h["agree_html"] = next(
        ln for ln in t.split("\n") if '<p class="cert-agree">' in ln)
    assert h["agree_html"].count("By entering your name, you make it official") == 1
    h["reader_html"] = extract_lines(
        t, '        <div class="cert-info-reader" id="certInfoReader"',
        '        <p class="hub-note" id="hubNote"',
        "reader html").rsplit("\n", 1)[0]
    assert h["reader_html"].count('class="cert-info-para"') == 9, \
        "reader must carry exactly 9 paragraphs"
    # JS — painters (with their Round 2 comments) + reader IIFE.
    h["painters"] = extract_lines(
        t, "    /* ROUND 2 F3: ONE hero painter",
        "    function paintValues(linkText, mailText, typed) {",
        "painters").rsplit("    function paintValues(linkText, mailText, typed) {", 1)[0] \
        + extract_rule(t, "    function paintValues(linkText, mailText, typed) {",
                       "paintValues")
    # extract_rule returns through the function's closing brace only —
    # the IIFE's grouping paren + call live AFTER it, so the append must
    # be ")();" (identity ends "})();"). The first staging appended
    # "();" — a missing ")" that broke the whole inline block in a
    # browser; the byte-identity assert below is the guard against a
    # repeat. The harvested IIFE must equal identity's own bytes.
    h["reader_js"] = extract_rule(
        t, "    (function(){\n      var reader = document.getElementById('certInfoReader');",
        "reader IIFE") + ")();"
    _ri = t.find("    (function(){\n      var reader = document.getElementById('certInfoReader');")
    _rj = t.find("})();", _ri)
    assert _ri >= 0 and _rj > _ri, "identity reader IIFE end not found"
    assert h["reader_js"] == t[_ri:_rj + len("})();")], \
        "reader IIFE differs from identity — STOP"
    assert h["reader_js"].endswith("})();"), "reader IIFE closer wrong"
    print("harvest extracted from identity 8c641f96 (all anchors unique):")
    for k, v in h.items():
        print(f"  {k}: {len(v.encode())} B")
    return h


# ------------------------------------------------------------------ harvest
def apply_certificate(d, h):
    """Harvest the identity treatment onto the /free entry. Every
    replacement is asserted (replace_once / exact counts)."""
    assert "CERTIFICATE CURRENT (2026-11-17" not in d, "harvest already present"
    assert d.count("Newsreader") == 0, "base must carry no Newsreader"
    assert "Marcellus" in d, "base must carry Marcellus"
    new = d

    # --- H3 tokens (:root, in place, verbatim identity values).
    new = replace_once(new, "      --silver: #f2f2f6;",
                       "      --silver: #ffffff;", "silver -> white")
    new = replace_once(new, "      --muted: #f2f2f6;",
                       "      --muted: #ffffff;", "muted -> white")
    new = replace_once(new, "      --faint: rgba(242, 242, 246, 0.88);",
                       "      --faint: rgba(255, 255, 255, 0.88);", "faint -> white")
    new = replace_once(new, "      --hair: rgba(245, 241, 232, 0.16);",
                       "      --hair: rgba(255, 255, 255, 0.16);", "hair -> white")
    new = replace_once(
        new,
        "      --purple: #a855f7; /* harvested with the entrance .enter button — its border color */",
        "      --purple: #a06bff; /* CERTIFICATE CURRENT: ONE purple — the second purple is cut (identity Round 2 F6); the entrance .enter button's border is royal now */",
        "one purple")
    # --- H3 gray lift, code only (comments keep their history).
    new = swap_outside_comments(new, "#f2f2f6", "#ffffff", 7, "gray #f2f2f6")
    new = swap_outside_comments(new, "rgba(245,241,232,", "rgba(255,255,255,", 12,
                                "cream rgba")
    new = swap_outside_comments(new, "rgba(232,232,236,", "rgba(255,255,255,", 4,
                                "silver-white rgba")
    new = swap_outside_comments(new, "rgba(248,247,251,0.30)", "rgba(255,255,255,0.30)", 1,
                                "warm-white rgba")
    new = swap_outside_comments(new, "rgba(220,228,255,0.14)", "rgba(255,255,255,0.14)", 1,
                                "pale-blue rgba")

    # --- H2 panels: obsidian fills in place of blue / brown-gold.
    new = replace_once(
        new,
        "      background: linear-gradient(180deg, #163a56 0%, #0a1c2e 46%, #030609 100%);",
        "      background: linear-gradient(180deg, #101013 0%, #050505 46%, #070708 100%);",
        "link panel obsidian")
    new = replace_once(
        new,
        "    .mail-line { background: linear-gradient(180deg, #3a2a09 0%, #1c1204 46%, #060402 100%);",
        "    .mail-line { background: linear-gradient(180deg, #101013 0%, #050505 46%, #070708 100%);",
        "mail panel obsidian")
    # --- H2 labels white (the glow carries the color now).
    old_label = ("    .id-box-label { font-size: 0.66rem; font-weight: 700; letter-spacing: 0.36em;\n"
                 "      text-transform: uppercase; color: var(--label); text-indent: 0.36em; }")
    new = replace_once(new, old_label, h["label"], "panel labels white")
    old_label_colors = ("    /* v2.7: each label carries its own box's family light — lightened\n"
                        "       shades of the assigned colors, readable on black. */\n"
                        "    .link-line .id-box-label { color: #a8dcff; }\n"
                        "    .mail-line .id-box-label { color: #ffd97a; }")
    new = replace_once(
        new, old_label_colors,
        "    /* CERTIFICATE CURRENT (Round 2 F4): the labels go WHITE — the panel's own glow carries the\n"
        "       color now, never the words. White text, always; color only as accent. */",
        "per-line label colors out")
    # --- H2 typing caret, after the value rule (identity order).
    value_rule = ("    .id-box-value { font-family: var(--serif); font-size: 1.24rem; font-weight: 560;\n"
                  "      color: var(--ink); letter-spacing: 0.015em; max-width: 100%;\n"
                  "      overflow-wrap: anywhere; word-break: break-all;\n"
                  "      text-shadow: 0 0 18px rgba(255,255,255,0.17); }")
    new = replace_once(new, value_rule, value_rule + "\n" + h["caret"],
                       "typing caret rules")

    # --- H1 name: base rule in place (identity paint, /free geometry).
    free_name = extract_rule(
        new, "    .cert-name { position: absolute; left: 50%; transform: translateX(-50%);",
        "free name base")
    id_name = h["name_base"]
    assert "font-size: clamp(2.4rem, min(7.4vw, 10vh), 5.4rem);" in id_name
    assert "font-size: clamp(2.9rem, 7.4vw, 4.9rem);" in free_name
    id_name = id_name.replace(
        "font-size: clamp(2.4rem, min(7.4vw, 10vh), 5.4rem);",
        "font-size: clamp(2.9rem, 7.4vw, 4.9rem); /* CERTIFICATE CURRENT: /free's own size kept — the paint is the harvest, not the size. */")
    new = replace_once(new, free_name, id_name, "name base -> trophy")
    # --- H1 certified name in place (relative so the clone anchors;
    # text-shadow none — the clone carries the glow).
    free_cert = extract_rule(
        new, "    .cert-plaque.is-certified .cert-name { position: static; transform: none;",
        "free certified name")
    new = replace_once(new, free_cert, h["name_certified"], "certified name -> trophy")
    # --- H1 taken name: the clone carries the glow now; a text-shadow
    # would bleed through the transparent glyphs (identity v2.12).
    new = replace_once(
        new,
        "text-shadow:0 0 38px rgba(160,107,255,0.16), 0 3px 30px rgba(0,0,0,0.55);",
        "text-shadow:none; /* CERTIFICATE CURRENT: the clone carries the glow now. */",
        "taken text-shadow out")

    # --- Appended block: clone, settle, hover, agreement + reader CSS.
    appended = (
        "\n    /* CERTIFICATE CURRENT (2026-11-17): harvested verbatim from the\n"
        "       identity treatment (identity-fixed.html sha 8c641f96 — Round 4 H1\n"
        "       trophy name + Round 5 H3/H1/H2). The name is a real object:\n"
        "       obsidian body, chrome edge, purple clone behind; the panels\n"
        "       are obsidian; the agreement sentence lives on the typed face. */\n"
        + h["clone_a"] + "\n" + h["clone_b"] + "\n"
        + h["settle"] + "\n" + h["settle_kf"] + "\n"
        + h["hover"] + "\n"
        + h["agree"] + "\n"
        + "    .cert-plaque.is-certified .cert-agree { display: none; }\n"
        + "    .face-foot:has(.alias-status[data-state=\"taken\"]) .cert-agree { display: none; }\n"
        + h["info"] + "\n" + h["reader_css"] + "\n"
        + "    /* Panels shown: the sentence funds its own room (identity Round 5). */\n"
        + "    .cert-plaque:not(.is-certified):has(.cert-lines:not([hidden])) .cert-agree { margin-top: 2px; }\n"
        + "    @media (max-width: 640px) {\n"
        + "      .cert-plaque:not(.is-certified):has(.cert-lines:not([hidden])) .cert-agree { font-size: 0.78rem; line-height: 1.35; }\n"
        + "    }\n"
    )
    assert new.count("</style>") == 1
    new = new.replace("</style>", appended + "    </style>", 1)

    # --- H4 HTML: the sentence + reader, directly under ENTER.
    enter_btn = (
        "        <button type=\"button\" class=\"activate-btn\" id=\"enterBtn\" onclick=\"activateAndRedirect()\">\n"
        "          <span class=\"ab-face\" aria-hidden=\"true\"></span>\n"
        "          <span class=\"ab-content\">\n"
        "            <span class=\"ab-title\">ENTER</span>\n"
        "          </span>\n"
        "        </button>")
    assert new.count(enter_btn) == 1, "enterBtn anchor moved"
    new = replace_once(
        new, enter_btn,
        enter_btn + "\n" + h["agree_html"] + "\n" + h["reader_html"],
        "agree + reader HTML")

    # --- JS painters (harvested) after prettyName; wire the paint sites.
    anchor = "const prettyName = s => s ? s.charAt(0).toUpperCase() + s.slice(1) : '';"
    assert new.count(anchor) == 1, "prettyName anchor moved"
    name_click = (
        "\n    /* CERTIFICATE CURRENT: the certified name is clickable to the\n"
        "       same place as USE A DIFFERENT ALIAS (identity Round 2 F8 —\n"
        "       the name is the deed; in composing it only hovers). */\n"
        "    (function(){\n"
        "      var heroEl = document.getElementById('displayName');\n"
        "      if (!heroEl) return;\n"
        "      heroEl.addEventListener('click', function(){\n"
        "        var pq = document.getElementById('certPlaque');\n"
        "        if (pq && pq.classList.contains('is-certified')) {\n"
        "          var so = document.getElementById('startOverBtn');\n"
        "          if (so) so.click();\n"
        "        }\n"
        "      });\n"
        "    })();\n")
    painters = ("\n" + h["painters"] + "\n" + h["reader_js"] + name_click)
    new = replace_once(new, anchor, anchor + painters, "painters + reader JS")

    # --- Paint site 1: typing (instant values, live hero echo).
    new = replace_once(
        new, "if (nameEl) { nameEl.textContent = ''; nameEl.hidden = true; }",
        "paintHeroName('');", "typing empty -> paintHeroName")
    new = replace_once(
        new, "if (nameEl) { nameEl.textContent = prettyName(currentAlias); nameEl.hidden = false; }",
        "paintHeroName(prettyName(currentAlias));", "typing hero -> paintHeroName")
    new = replace_once(
        new,
        "      const linkEl = document.getElementById('displayLink');\n"
        "      linkEl.textContent = currentAlias + '.nayanet.app';\n"
        "      linkEl.title = currentAlias + '.nayanet.app';\n"
        "      document.getElementById('displayMail').textContent = currentAlias;",
        "      paintValues(currentAlias + '.nayanet.app', currentAlias, false);",
        "typing values -> paintValues instant")
    # --- Paint site 2: own restore (typed values, settle once).
    new = replace_once(
        new, "if (nm) { nm.textContent = certName; nm.hidden = !certName; }",
        "paintHeroName(certName); settleHeroName();", "restore hero -> paintHeroName")
    new = replace_once(
        new,
        "        var lk = document.getElementById('displayLink');\n"
        "        if (lk) { lk.textContent = (certRegalia.alias || alias) + '.nayanet.app'; lk.title = lk.textContent; }\n"
        "        var ml = document.getElementById('displayMail'); if (ml) ml.textContent = certRegalia.alias || alias;",
        "        paintValues((certRegalia.alias || alias) + '.nayanet.app', certRegalia.alias || alias, true);",
        "restore values -> paintValues typed")
    # --- Paint site 3: claim stamp (typed values, settle once).
    new = replace_once(
        new,
        "        if (heroEl) { var heroName = ''; try { heroName = localStorage.getItem('nayanet_smart_name') || ''; } catch(e){} heroEl.textContent = heroName; heroEl.hidden = !heroName; }",
        "        var heroName = ''; try { heroName = localStorage.getItem('nayanet_smart_name') || ''; } catch(e){}\n"
        "        paintHeroName(heroName); settleHeroName();\n"
        "        var stampAlias = ''; try { stampAlias = localStorage.getItem('nayanet_smart_alias') || ''; } catch(e){}\n"
        "        if (stampAlias) paintValues(stampAlias + '.nayanet.app', stampAlias, true);",
        "stamp hero -> paintHeroName")
    return new


# ------------------------------------------------------------------- main
def regen_pricing_fix_tip():
    """Regenerate the pricing-fix tip (the base of this round) in memory
    through the filed build chain; fail-stop if any link moved."""
    walk_f4 = _fix.apply_walk_fixes(_bf.build_walk_free())
    entry_f4 = _bf.build_free_entry()
    walk_base = _fo.apply_item1_walk(walk_f4)
    entry_fo = _fo.apply_entry_followon(entry_f4)
    entry_marc = _marc.apply_marcellus_swap(entry_fo)
    entry_base = _bt.apply_taken_fix(entry_marc)
    assert sha(walk_base) == "2370eae2f9ae9e281d1c3f3b35d99f8699c7df6a2fe4f73328e2877c3b6453ea", \
        f"taken-fix walk moved: {sha(walk_base)}"
    assert sha(entry_base) == "3d5b913f117b90a1fdd3e72347f8458c4de4429972eb05a38c6fb118f7fbf285", \
        f"taken-fix entry moved: {sha(entry_base)}"
    entry_pf = _fixmod.apply_entry_fix(entry_base)
    walk_pf = _fixmod.apply_walk_fix(walk_base)
    assert sha(entry_pf) == BASE_ENTRY_SHA, f"pricing-fix entry moved: {sha(entry_pf)}"
    assert sha(walk_pf) == BASE_WALK_SHA, f"pricing-fix walk moved: {sha(walk_pf)}"
    print(f"base verified: walk {len(walk_pf.encode())} B sha={sha(walk_pf)[:8]}... "
          f"entry {len(entry_pf.encode())} B sha={sha(entry_pf)[:8]}...")
    return walk_pf, entry_pf


def build_worker_for(walk, entry, sw, mani):
    """The pricing-fix worker shape: build + PWA patch + asset consts/routes."""
    from importlib.util import spec_from_file_location as _sfl, module_from_spec as _mfs
    _dn_spec = _sfl("deploy_ninaya", os.path.expanduser(
        "~/workspace/ninaya/integration/deploy-ninaya.py"))
    _dn = _mfs(_dn_spec)
    _dn_spec.loader.exec_module(_dn)
    js_encode = _dn.js_encode
    worker = _fix.apply_worker_fix(_bf.build_worker(walk, entry))
    anchor_const = 'const SB_URL = "https://dahisasgpfvziswqvmvm.supabase.co/rest/v1/nayanet_identities";'
    consts = ('const TAKEN_SW = "' + js_encode(sw) + '";\n'
              'const TAKEN_MANIFEST = "' + js_encode(mani) + '";\n')
    worker = replace_once(worker, anchor_const, consts + anchor_const, "PWA asset consts")
    anchor_route = '    if (p === "/free/hub") {'
    routes = (
        '    if (p === "/sw.js") {\n'
        '      return new Response(TAKEN_SW, { headers: { "content-type": '
        '"application/javascript;charset=utf-8", "cache-control": "no-store" } });\n'
        '    }\n'
        '    if (p === "/manifest.webmanifest") {\n'
        '      return new Response(TAKEN_MANIFEST, { headers: { "content-type": '
        '"application/manifest+json;charset=utf-8", "cache-control": "no-store" } });\n'
        '    }\n')
    worker = replace_once(worker, anchor_route, routes + anchor_route, "PWA asset routes")
    return worker


def js_syntax_check(entry):
    """Compile every inline <script> block with node vm.Script, fed via
    stdin — NO disk writes (the EPERM flake blocks temp files) and NO
    skips. The first staging's temp-file check silently skipped every
    block when the flake blocked the writes, and the browser probe that
    was meant to be the fallback could not run (VM browsers dead) — so
    a one-character harvest error shipped live. A check that can skip is
    not a check: if this cannot run, the build FAILS."""
    import subprocess
    blocks = re.findall(r"<script>(.*?)</script>", entry, re.S)
    assert blocks, "no inline script blocks found"
    check = ("const vm=require('vm');let s='';process.stdin.on('data',d=>s+=d)"
             ".on('end',()=>{try{new vm.Script(s,{filename:'entry-script.js'});"
             "console.log('SYNTAX OK '+s.length);}catch(e){console.log('SYNTAX FAIL: '+e.message);process.exit(1);}});")
    checked = 0
    for i, js in enumerate(blocks):
        if not js.strip():
            continue
        p = subprocess.run(["node", "-e", check], input=js.encode(),
                           capture_output=True, timeout=120)
        assert p.returncode == 0, \
            f"script block {i} fails syntax check: {p.stdout.decode()[:400]}"
        checked += 1
    print(f"vm.Script syntax: {checked}/{len(blocks)} inline script blocks OK")


def main():
    walk_pf, entry_pf = regen_pricing_fix_tip()

    # 0b. Live staged /free + /free/walk must still serve the expected
    # bytes: the pricing-fix tip on a first run, or this round's first
    # (broken) staging on a fix re-run — the fix re-derives from the
    # filed chain, never from live, so either is the honest guard.
    st, _, live_entry = _sim.http_get(FREE_HOST + "/free")
    assert st == 200 and sha(live_entry) in (BASE_ENTRY_SHA, PREV_ENTRY_SHA), \
        f"live staged /free moved: {st} {sha(live_entry)[:8]}... — STOP"
    st, _, live_walk = _sim.http_get(FREE_HOST + "/free/walk")
    assert st == 200 and sha(live_walk) == BASE_WALK_SHA, \
        f"live staged /free/walk moved: {st} {sha(live_walk)[:8]}... — STOP"
    st, _, live_id = _sim.http_get(IDENTITY_HOST + "/identity.html")
    assert st == 200 and sha(live_id) == IDENTITY_SHA, \
        f"live staged identity moved: {st} {sha(live_id)[:8]}... — STOP"
    print("live staged /free + /free/walk + identity == tip MATCH")

    # 0c. Harvest the page's own PWA assets verbatim from the live site.
    st, _, sw = _sim.http_get(LIVE + "/sw.js")
    assert st == 200, f"live sw.js: {st}"
    sw = sw.decode("utf-8")
    assert sha(sw) == SW_SHA, f"sw.js moved: {sha(sw)}"
    st, _, mani = _sim.http_get(LIVE + "/manifest.webmanifest")
    assert st == 200, f"live manifest: {st}"
    mani = mani.decode("utf-8")
    assert sha(mani) == MANI_SHA, f"manifest moved: {sha(mani)}"
    print(f"harvested live PWA assets: sw.js {len(sw.encode())} B, "
          f"manifest {len(mani.encode())} B")

    # 0d. Reproduce the CURRENT staged worker byte-exact first: the chain
    # must reproduce the pricing-fix worker before I change anything.
    free_index = _bf.FREE_INDEX.replace(
        "__PRICING_STAGED__", "https://naya-pricing-f4-staging.nayapower.workers.dev/")
    worker_pf = build_worker_for(walk_pf, entry_pf, sw, mani)
    assert sha(worker_pf) == BASE_WORKER_SHA, \
        f"pricing-fix worker NOT reproduced: {sha(worker_pf)} — STOP"
    print(f"pricing-fix worker reproduced: {len(worker_pf.encode())} B "
          f"sha={sha(worker_pf)[:8]}... MATCH")

    # 1. Apply the harvest.
    h = harvest_identity()
    old_certified = re.findall(r'\.cert-plaque\.is-certified[^{]*\{[^}]*\}', entry_pf)
    old_certname = re.findall(r'\.cert-name[^{]*\{[^}]*\}', entry_pf)
    new_entry = apply_certificate(entry_pf, h)
    # Invariants: every old certified rule and every old .cert-name rule
    # still present byte-identical, except the two the harvest replaces.
    new_certified = re.findall(r'\.cert-plaque\.is-certified[^{]*\{[^}]*\}', new_entry)
    # Exactly two new certified rules are expected: the agree hide
    # (certified face carries no composing line) and the certified hover.
    assert len(new_certified) == len(old_certified) + 2, \
        f"certified rule count moved: {len(old_certified)} -> {len(new_certified)}"
    for r in old_certified:
        if ".cert-name" in r:
            continue
        assert r in new_entry, f"certified rule changed — STOP: {r[:120]}"
    # The regex captures every rule starting AT ".cert-name", so a loop
    # over them cannot tell replaced from untouched — assert the geometry
    # rules explicitly instead (the two the harvest replaces are the base
    # and certified rules; everything else must be byte-identical).
    for keep in [
        ".cert-name[hidden] { display: none; }",
        ".cert-name { font-size: clamp(2.4rem, 6.4vw, 4.1rem); }",
        ".cert-name { font-size: clamp(2.55rem, 13.5vw, 3.4rem); }",
        ".cert-name{white-space:nowrap;overflow:visible;line-height:1.14;"
        "padding-bottom:.14em;margin-bottom:10px;}",
        ".cert-name{font-size:clamp(1.65rem,6.2vw,2.5rem);}",
    ]:
        assert keep in new_entry, f"geometry rule lost — STOP: {keep[:80]}"
    assert 'text-shadow:none; /* CERTIFICATE CURRENT: the clone carries the glow now. */' in new_entry, \
        "taken text-shadow edit missing"
    assert "Marcellus" in new_entry and new_entry.count("Newsreader") == 0
    assert "By entering your name, you make it official" in new_entry
    assert new_entry.count('class="cert-info-para"') == 9
    assert new_entry.count("paintHeroName(") >= 4, "paint sites not wired"
    assert new_entry.count("paintValues(") >= 4, "value paint sites not wired"
    # Both harvested/written IIFEs must close with "})();" — the reader
    # shipped once as "}();" and killed the whole inline block.
    assert new_entry.count("})();") >= 2, "an IIFE closer is missing — STOP"
    for label, old, new in [("entry", entry_pf, new_entry)]:
        diff = list(difflib.unified_diff(old.splitlines(), new.splitlines(), lineterm="", n=0))
        removed = [ln for ln in diff if ln.startswith("-") and not ln.startswith("---")]
        added = [ln for ln in diff if ln.startswith("+") and not ln.startswith("+++")]
        print(f"{label} diff: +{len(added)} lines, -{len(removed)} lines")
        for ln in removed:
            print("   -", ln[:220])
        for ln in added:
            print("   +", ln[:220])
    print(f"new entry: {len(new_entry.encode())} B sha256={sha(new_entry)}")
    js_syntax_check(new_entry)

    # 2. Worker rebuild with the new entry (walk unchanged) + node driver.
    new_worker = build_worker_for(walk_pf, new_entry, sw, mani)
    print(f"new worker: {len(new_worker.encode())} B sha256={sha(new_worker)}")
    gz = gzip.compress(new_worker.encode("utf-8"))
    print(f"worker gzip: {len(gz)} B (limit 10,485,760)")
    assert len(gz) < 10485760

    _sim.node_check(new_worker, FREE_HOST + "/free", sha(new_entry),
                    ["CERTIFICATE CURRENT (2026-11-17",
                     "By entering your name, you make it official",
                     'id="certInfoReader"', 'id="certInfoBtn"',
                     "paintHeroName", "paintValues", "settleHeroName",
                     "background: linear-gradient(180deg, #101013 0%, #050505 46%, #070708 100%)",
                     "--silver: #ffffff;", "--muted: #ffffff;",
                     "text-shadow:none; /* CERTIFICATE CURRENT",
                     "name-settle", "cert-info-para",
                     "TAKEN STATE (2026-11-17", "function fitTakenName()",
                     "PRICING FIX (2026-11-17", "Use a different alias",
                     "Enter free &mdash; no payment, no card.",
                     "--serif: Marcellus, Georgia, serif;",
                     'id="startOverBtn"', "WALKTHROUGH_URL = '/free/walk'"],
                    ["Newsreader", "#f2f2f6", "#a8dcff", "#ffd97a",
                     "#163a56", "#0a1c2e", "#3a2a09", "#1c1204"])
    _sim.node_check(new_worker, FREE_HOST + "/free/walk", sha(walk_pf),
                    ["fonts.googleapis.com/css2?family=Marcellus",
                     "font-family:Marcellus,Georgia,serif",
                     ".p3-congrats{font-family:Marcellus",
                     "function adoptWalkName",
                     'id="enterBtn-names"',
                     "buildBarFill", "showStep(16)"],
                    ["Newsreader"])
    _sim.node_check(new_worker, FREE_HOST + "/", sha(free_index),
                    ["Enter free — the route, staged"], [])
    _sim.node_check(new_worker, FREE_HOST + "/sw.js", sha(sw),
                    ["self-retiring", "skipWaiting", "unregister"], [])
    _sim.node_check(new_worker, FREE_HOST + "/manifest.webmanifest", sha(mani),
                    ["NayaNET", "start_url"], [])
    _sim.node_redirect_check(new_worker, FREE_HOST + "/free/hub",
                             "https://nayanet.app/")
    print("node driver: PASS (new entry + walk + index + sw.js + manifest + hub)")

    # 3. Stage the new free worker (STAGING ONLY — pricing untouched).
    kv = [{"type": "kv_namespace", "name": "WELCOME_ASSETS",
           "namespace_id": "1cf80db6183245d19dd5296645a12bd0"}]
    _sim.put_worker("naya-pricing-free-staging", new_worker.encode(), kv)
    status, raw = _sim.api("GET", "/naya-pricing-free-staging")
    assert status == 200
    _, wb, _ = _sim.split_multipart(raw)
    assert wb == new_worker.encode(), "read-back differs from PUT — STOP"
    print(f"read-back sha256={sha(wb)} — MATCH")

    # 4. Live HTTP verification of the staged routes.
    for path, want in [("/", free_index), ("/free", new_entry),
                       ("/free/walk", walk_pf)]:
        st, _, got = _sim.http_get(FREE_HOST + path)
        assert st == 200, f"GET {path}: {st}"
        assert got.decode("utf-8") == want, f"GET {path}: bytes != source — STOP"
        print(f"GET {FREE_HOST}{path}: 200, {len(got)} B == source MATCH")
    for path, want_bytes, want_ct in [
            ("/sw.js", sw.encode(), "application/javascript"),
            ("/manifest.webmanifest", mani.encode(), "application/manifest+json")]:
        st, hdrs, got = _sim.http_get(FREE_HOST + path)
        assert st == 200, f"GET {path}: {st}"
        assert got == want_bytes, f"GET {path}: bytes != harvested — STOP"
        assert want_ct in hdrs.get("Content-Type", ""), \
            f"GET {path}: content-type {hdrs.get('Content-Type')} — STOP"
        print(f"GET {FREE_HOST}{path}: 200, {len(got)} B == harvested MATCH "
              f"({hdrs.get('Content-Type')})")
    st, hdrs, _ = _sim.http_get(FREE_HOST + "/free/hub")
    assert st in (301, 302) and hdrs.get("Location") == "https://nayanet.app/"
    print("GET /free/hub: 302 -> https://nayanet.app/ MATCH")

    # 5. Pricing v78 still byte-exact on its own staging worker (untouched).
    st, _, v78 = _sim.http_get(PRICING_HOST + "/")
    assert st == 200 and sha(v78) == PRICING_V78_SHA, "pricing v78 MOVED — STOP"
    print(f"pricing v78: {len(v78)} B sha={sha(v78)[:8]}... UNCHANGED")

    # 6. Save the fixed bytes locally (filing + checker source of truth).
    try:
        with open(os.path.join(HERE, "fixed-entry.html"), "w") as f:
            f.write(new_entry)
        print(f"saved {os.path.join(HERE, 'fixed-entry.html')}")
    except OSError as e:
        print(f"DISK WRITE FAILED (EPERM flake?): {e} — bytes remain "
              f"reproducible in memory from this build script + staged worker")
    print("BUILD+STAGE OK")
    print(f"  walk sha256={sha(walk_pf)} (UNCHANGED)")
    print(f"  entry sha256={sha(new_entry)}")
    print(f"  worker sha256={sha(new_worker)}")
    print(f"  sw.js sha256={sha(sw)} ({len(sw.encode())} B, live verbatim)")
    print(f"  manifest sha256={sha(mani)} ({len(mani.encode())} B, live verbatim)")
    return {"walk": walk_pf, "entry": new_entry, "free_index": free_index,
            "worker": new_worker, "sw": sw, "manifest": mani}


if __name__ == "__main__":
    main()
