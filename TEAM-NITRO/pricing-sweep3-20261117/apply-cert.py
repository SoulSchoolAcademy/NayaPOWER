#!/usr/bin/env python3
"""Apply the CERTIFICATE CURRENT harvest onto the Sweep #3 fixed /free file.

SOURCE (verified in this round): the identity certificate treatment,
  ~/workspace/team-nitro/walk-v23-assembly-20261114/identity-fixed.html
  376,814 B, sha256 8c641f96d31818b610d1a243d945dfb5c68e6016e036b7afb11b72445330013d
  (Round 4 H1 trophy name + Round 5 H3/H1/H2; the Micheal certificate's
  treatment, Nº 000204, Round 2 2026-11-15 21:58Z, carried through Rounds 3-5).
  Harvest extraction is reused from the sibling seat's builder
  (~/workspace/team-nitro/pricing-certificate-current-20261117/build-certificate.py,
  harvest_identity() — all anchors unique); this script applies the same
  H1-H4 harvest onto the SWEEP #3 file (which already carries the 14 fixes),
  instead of the F4 base the sibling builds from.

WHAT LANDS (H1-H4), each piece extracted by anchor and asserted, never retyped:
  H1 NAME — the trophy: obsidian gradient body, chrome 1px stroke, purple
     clone behind (Round 4 clone trick), hover pop, name-settle arrival,
     certified in-flow. Geometry (size/position) KEPT from /free.
  H2 PANELS — obsidian fills; labels WHITE (the glow carries the color);
     values TYPE letter-by-letter with a caret in the panel's own color
     on restore + stamp (instant while composing).
  H3 TOKENS — the gray lift: --silver/--muted #f2f2f6 -> #ffffff,
     --faint -> white 0.88, --hair cream -> white; every #f2f2f6 text rule
     -> white.
  H4 AGREEMENT — the official sentence (typed face only) under ENTER +
     the clone-trick (i) + the one-paragraph-at-a-time reader, harvested
     whole. Hidden in the certified and taken states (Round 5 H1 amended).
NOT harvested (named, not hidden): the membership sentence (.cert-member)
  and the H6 green taken message — both absent on /free, outside the brief.

DOCUMENTED RE-VALUINGS (harvest the shape, re-value where a newer system
law governs — never silent, never by taste):
  R1 DEEP PALETTE (Fix 2, §3.1): the identity's bright purples are re-valued
     to the deep family — rgba(160,107,255,...) -> rgba(142,36,170,...);
     clone gradient #c9a5ff/#a06bff/#6d28d9 -> #e3c8f5/#8e24aa/#3d0a52
     (the clock jewel's own ramp); caret #3fb8ff -> #0f52ba, #ffbf3d -> #d4a017.
     H3's purple unification (#a855f7 -> #a06bff) does NOT apply: /free
     already unifies to ONE deep purple (#8e24aa) by Fix 2.
  R2 TYPE FLOOR (Fix 1, 25/19/17): the identity's small sizes are raised —
     agree 0.82rem, info 13px, reader title 1.05rem, para 0.92rem,
     prog/next 0.72rem, close 15px, label 0.66rem (not taken) — all to
     1.0625rem (17px). Geometry/size is /free's; the paint is the harvest.
  R3 LIGHT (Fix 10): the reader's 165deg panel gradient -> 135deg. The name
     body's and the clone's 180deg gradients are KEPT as the top-light
     exception Fix 10 allows (vertical gloss fall — the object's own top
     light, the same exception the inspector's Fix 10 names).
  R4 READER IIFE: the sibling's extractor drops the grouping paren
     (extract ends at the function's } and appends "();" — the identity
     source reads "})();"). This script repairs the ending and asserts
     balanced parens. The sibling's build carries the same latent bug.

SAFETY: builds entirely in memory; writes via temp file in the same
directory + os.replace (never truncate-first on the live file); the
pre-harvest bytes are backed up as fixed-entry.sweep3-14fixes.html.
"""
import hashlib
import importlib.util
import os
import re
import sys

HERE = os.path.expanduser("~/workspace/team-nitro/pricing-sweep3-20261117")
TARGET = os.path.join(HERE, "fixed-entry.html")
TMP = os.path.join(HERE, ".fixed-entry.cert-tmp")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def rep(t, old, new, count=1):
    n = t.count(old)
    assert n == count, f"REPLACE FAIL (want {count}, got {n}): {old[:110]!r}"
    return t.replace(old, new)


def sub(t, old, new, count, what):
    n = t.count(old)
    assert n == count, f"REVALUE FAIL {what} (want {count}, got {n}): {old[:80]!r}"
    return t.replace(old, new)


def main():
    cert = load("build_cert",
                "/home/hatch/workspace/team-nitro/pricing-certificate-current-20261117/build-certificate.py")
    h = cert.harvest_identity()

    # ---------- Re-valuings R1/R2/R3 on the harvested pieces ----------
    # H1 name body: bright rest-glow -> deep royal (R1).
    h["name_base"] = sub(h["name_base"], "rgba(160,107,255,0.18)",
                         "rgba(142,36,170,0.18)", 1, "name rest glow")
    # H1 name body: /free's geometry, not the identity's (R2/sibling note).
    h["name_base"] = sub(h["name_base"],
                         "font-size: clamp(2.4rem, min(7.4vw, 10vh), 5.4rem);",
                         "font-size: clamp(2.9rem, 7.4vw, 4.9rem);", 1, "name size")
    # H1 clone paint: bright purple ramp -> deep royal ramp (R1).
    h["clone_b"] = sub(h["clone_b"],
                       "linear-gradient(180deg, #c9a5ff 0%, #a06bff 55%, #6d28d9 100%)",
                       "linear-gradient(180deg, #e3c8f5 0%, #8e24aa 55%, #3d0a52 100%)",
                       1, "clone ramp")
    # H1 hover halo: bright -> deep (R1).
    h["hover"] = sub(h["hover"], "rgba(160,107,255,0.6)",
                     "rgba(142,36,170,0.6)", 1, "hover halo")
    # H2 caret: bright blue/gold -> deep sapphire/gold (R1).
    h["caret"] = sub(h["caret"], "#3fb8ff", "#0f52ba", 1, "caret link")
    h["caret"] = sub(h["caret"], "#ffbf3d", "#d4a017", 1, "caret mail")
    # H4 agree line: 0.82rem -> 17px (R2).
    h["agree"] = sub(h["agree"], "font-size: 0.82rem;", "font-size: 1.0625rem;", 1, "agree size")
    # H4 info button: clone ramp -> deep (R1); glyph 13px -> 17px (R2).
    h["info"] = sub(h["info"],
                    "linear-gradient(135deg, #c9a5ff 0%, #a06bff 55%, #6d28d9 100%)",
                    "linear-gradient(135deg, #e3c8f5 0%, #8e24aa 55%, #3d0a52 100%)",
                    1, "info clone ramp")
    h["info"] = sub(h["info"], "rgba(160,107,255,0.65)",
                    "rgba(142,36,170,0.65)", 1, "info hover halo")
    h["info"] = sub(h["info"], "font-size: 13px;", "font-size: 1.0625rem;", 1, "info glyph")
    # H4 reader: 165deg -> 135deg (R3); small sizes -> 17px (R2); glows -> deep (R1).
    h["reader_css"] = sub(h["reader_css"], "linear-gradient(165deg,",
                          "linear-gradient(135deg,", 1, "reader angle")
    h["reader_css"] = sub(h["reader_css"], "rgba(160,107,255,0.20)",
                          "rgba(142,36,170,0.20)", 1, "reader glow")
    h["reader_css"] = sub(h["reader_css"], "rgba(160,107,255,0.55)",
                          "rgba(142,36,170,0.55)", 1, "reader next halo")
    h["reader_css"] = sub(h["reader_css"], "font-size: 1.05rem;",
                          "font-size: 1.0625rem;", 1, "reader title")
    h["reader_css"] = sub(h["reader_css"], "font-size: 0.92rem;",
                          "font-size: 1.0625rem;", 1, "reader para")
    h["reader_css"] = sub(h["reader_css"], "font-size: 0.72rem;",
                          "font-size: 1.0625rem;", 2, "reader prog/next")
    h["reader_css"] = sub(h["reader_css"], "font-size: 15px;",
                          "font-size: 1.0625rem;", 1, "reader close")
    # R4: repair the reader IIFE ending (extractor drops the grouping paren).
    rjs = h["reader_js"].rstrip()
    assert rjs.endswith("}();"), f"reader IIFE ending moved: {rjs[-20:]!r}"
    rjs = rjs[:-4] + "})();"
    assert rjs.count("(") == rjs.count(")"), "reader IIFE parens unbalanced after repair"
    h["reader_js"] = rjs

    t = open(TARGET, encoding="utf-8").read()
    assert len(t) > 300000, "target looks truncated — STOP"
    base_sha = hashlib.sha256(t.encode()).hexdigest()
    print(f"base: {len(t.encode())} B sha {base_sha[:12]}...", flush=True)

    # ---------- H1: the trophy name ----------
    t = rep(t,
            "    .cert-name { position: absolute; left: 50%; transform: translateX(-50%);\n"
            "      bottom: calc(100% + clamp(8px, 1.2vh, 12px)); width: min(100%, 920px);\n"
            "      font-family: var(--serif); font-weight: 560;\n"
            "      font-size: clamp(2.9rem, 7.4vw, 4.9rem); line-height: 0.98;\n"
            "      letter-spacing: 0.008em; color: var(--ink); overflow-wrap: anywhere;\n"
            "      margin-top: 0; pointer-events: none; z-index: 2; }",
            h["name_base"].rstrip())
    # Clone + settle + hover + caret + agree + info + reader CSS, one block.
    harvest_css = (
        "\n    /* ============ SWEEP #3 CERTIFICATE CURRENT (2026-11-17) ============\n"
        "       Harvested from identity-fixed.html sha 8c641f96 (Round 4 H1 +\n"
        "       Round 5 H3/H1/H2) — the clone trick, the typing caret, the\n"
        "       official sentence + reader. Re-valued per R1/R2/R3 above;\n"
        "       the 180deg name/clone gradients are the Fix-10 top-light\n"
        "       exception (vertical gloss fall). */\n"
        + h["clone_a"] + "\n" + h["clone_b"] + "\n" + h["settle"] + "\n"
        + h["settle_kf"] + "\n" + h["hover"] + "\n" + h["caret"] + "\n"
        + h["agree"] + "\n" + h["info"] + "\n" + h["reader_css"] + "\n"
        "    /* CERTIFIED + TAKEN: the agreement line and its reader are\n"
        "       typed-face only (Round 5 H1 amended) — the certificate\n"
        "       statement already says the signing. */\n"
        "    .cert-plaque.is-certified .cert-agree, .cert-plaque.taken .cert-agree,\n"
        "    .cert-plaque.is-certified .cert-info-reader, .cert-plaque.taken .cert-info-reader { display: none; }")
    t = rep(t, "    .cert-name[hidden] { display: none; }",
            "    .cert-name[hidden] { display: none; }" + harvest_css)
    # Certified seat: relative (clone anchor) + no text-shadow bleed.
    t = rep(t,
            "    .cert-plaque.is-certified .cert-name { position: static; transform: none;\n"
            "      width: auto; pointer-events: auto;\n"
            "      text-shadow: 0 0 38px rgba(142,36,170,0.16), 0 3px 30px rgba(0,0,0,0.55); }",
            "    /* SWEEP #3 CERT: the trophy's certified seat, harvested — position:relative\n"
            "       (not static) so the ::before clone anchors to the name, and\n"
            "       text-shadow:none (a shadow would bleed through the transparent\n"
            "       glyphs; the base rule's drop-shadow filter carries the glow). */\n"
            "    .cert-plaque.is-certified .cert-name { position: relative; transform: none;\n"
            "      width: auto; pointer-events: auto; cursor: pointer;\n"
            "      text-shadow: none; }")
    # Taken seat: same clone-anchor + no-bleed rule.
    t = rep(t,
            '.cert-plaque:has(.alias-status[data-state="taken"]) .cert-name{position:static;transform:none;width:auto;pointer-events:auto;text-shadow:0 0 38px rgba(142,36,170,0.16), 0 3px 30px rgba(0,0,0,0.55);}',
            '.cert-plaque:has(.alias-status[data-state="taken"]) .cert-name{position:relative;transform:none;width:auto;pointer-events:auto;text-shadow:none; /* SWEEP #3 CERT: clone anchor + no bleed, as the certified seat. */}')

    # ---------- H2: obsidian panel fills + white labels ----------
    t = rep(t,
            "      background: linear-gradient(135deg, #0b3d2c 0%, #062015 46%, #030604 100%);",
            "      background: linear-gradient(135deg, #101013 0%, #050505 46%, #070708 100%); /* SWEEP #3 CERT H2: obsidian fill — the glow carries the color. */")
    t = rep(t,
            "    .mail-line { background: linear-gradient(135deg, #33260a 0%, #1a1305 46%, #060402 100%);",
            "    .mail-line { background: linear-gradient(135deg, #101013 0%, #050505 46%, #070708 100%); /* SWEEP #3 CERT H2: obsidian fill. */")
    t = rep(t,
            "      text-transform: uppercase; color: var(--label); text-indent: 0.36em; }",
            "      text-transform: uppercase; color: #ffffff; text-indent: 0.36em; }")
    t = rep(t,
            "    /* v2.7: each label carries its own box's family light — lightened\n"
            "       shades of the assigned colors, readable on black. */\n"
            "    .link-line .id-box-label { color: #a9e5cd; }\n"
            "    .mail-line .id-box-label { color: #ecd27e; }",
            "    /* SWEEP #3 CERT H2: labels WHITE, harvested — the glow carries the family\n"
            "       color; the v2.7 family-light labels are superseded. */")

    # ---------- H3: the gray lift ----------
    t = rep(t, "#f2f2f6", "#ffffff", count=9)
    t = rep(t, "rgba(242, 242, 246, 0.88)", "rgba(255, 255, 255, 0.88)")
    t = rep(t, "rgba(245, 241, 232, 0.16)", "rgba(255, 255, 255, 0.16)")

    # ---------- H4: agreement HTML (under ENTER) + reader HTML (before hubNote) ----------
    t = rep(t,
            "          <span class=\"ab-title\">ENTER</span>\n"
            "          </span>\n"
            "        </button>",
            "          <span class=\"ab-title\">ENTER</span>\n"
            "          </span>\n"
            "        </button>\n"
            + h["agree_html"])
    t = rep(t,
            "        <p class=\"hub-note\" id=\"hubNote\" hidden>",
            h["reader_html"] + "\n"
            "        <p class=\"hub-note\" id=\"hubNote\" hidden>")

    # ---------- H1/H2 JS: the one hero painter + the typing values + the reader ----------
    t = rep(t, "    function updateSmartCredentials() {",
            "    /* SWEEP #3 CERT (2026-11-17): the harvested painters + reader,\n"
            "       verbatim from identity 8c641f96 (ROUND 2 F3/F5 + Round 5 H2).\n"
            "       The reader IIFE's ending is repaired (R4) — see header. */\n"
            + h["painters"] + "\n" + h["reader_js"] + "\n\n"
            "    function updateSmartCredentials() {")
    # Echo: paint the hero through the one painter (data-text stays in sync).
    t = rep(t,
            "        if (nameEl) { nameEl.textContent = ''; nameEl.hidden = true; }",
            "        if (nameEl) paintHeroName('');")
    t = rep(t,
            "      if (nameEl) { nameEl.textContent = spacedName(currentAlias); nameEl.hidden = false; }",
            "      if (nameEl) paintHeroName(spacedName(currentAlias));")
    t = rep(t,
            "      const linkEl = document.getElementById('displayLink');\n"
            "      linkEl.textContent = currentAlias + '.nayanet.app';\n"
            "      linkEl.title = currentAlias + '.nayanet.app';\n"
            "      document.getElementById('displayMail').textContent = currentAlias;",
            "      paintValues(currentAlias + '.nayanet.app', currentAlias, false);")
    # Certified restore: hero + settle, values typed.
    t = rep(t,
            "        if (nm) { nm.textContent = certName; nm.hidden = !certName; }",
            "        if (nm) { paintHeroName(certName); settleHeroName(); }")
    t = rep(t,
            "        var lk = document.getElementById('displayLink');\n"
            "        if (lk) { lk.textContent = (certRegalia.alias || alias) + '.nayanet.app'; lk.title = lk.textContent; }\n"
            "        var ml = document.getElementById('displayMail'); if (ml) ml.textContent = certRegalia.alias || alias;",
            "        paintValues((certRegalia.alias || alias) + '.nayanet.app', certRegalia.alias || alias, true);")
    # Stamp: hero + settle.
    t = rep(t,
            "        if (heroEl) { var heroName = ''; try { heroName = localStorage.getItem('nayanet_smart_name') || ''; } catch(e){} heroEl.textContent = heroName; heroEl.hidden = !heroName; }",
            "        if (heroEl) { var heroName = ''; try { heroName = localStorage.getItem('nayanet_smart_name') || ''; } catch(e){} paintHeroName(heroName); settleHeroName(); }")

    # ---------- Final guards ----------
    bright = re.findall(r"#(2fe89e|ffbf3d|a06bff|a855f7|3fb8ff|a8dcff|ffd97a|c9a5ff)"
                        r"|rgba\((47,232,158|63,184,255|255,191,61|160,107,255|168,85,247)", t)
    assert not bright, f"bright tokens remain: {bright[:5]}"
    assert "#f2f2f6" not in t, "#f2f2f6 remains"
    assert "rgba(242, 242, 246" not in t and "rgba(242,242,246" not in t, "gray faint remains"
    sizes = re.findall(r"font-size:\s*([^;}\s]+)", t)

    def px(s):
        m = re.match(r"([\d.]+)rem", s)
        if m:
            return float(m.group(1)) * 16
        m = re.match(r"clamp\(([\d.]+)rem", s)
        if m:
            return float(m.group(1)) * 16
        m = re.match(r"([\d.]+)px", s)
        if m:
            return float(m.group(1))
        return None
    bad = [(s, px(s)) for s in set(sizes) if px(s) is not None and px(s) < 17]
    assert not bad, f"font-size below 17px: {bad}"
    angles = sorted(set(re.findall(r"linear-gradient\((\d+)deg", t)))
    assert set(angles) <= {"135", "180"}, f"unexpected gradient angles: {angles}"
    assert t.count("linear-gradient(180deg") == 2, \
        f"180deg gradients (want 2, name body + clone): {t.count('linear-gradient(180deg')}"
    ids = re.findall(r'id="([^"]+)"', t)
    assert len(ids) == 29 and len(set(ids)) == 29, \
        f"ids: {len(ids)} total, {len(set(ids))} unique"
    assert t.count('class="cert-info-para"') == 9, "reader must carry exactly 9 paragraphs"
    assert "By entering your name, you make it official" in t, "official sentence missing"
    for needle in ["paintHeroName", "settleHeroName", "name-settle", "data-text",
                   "cert-agree", "certInfoReader", "cert-info", "typing::after",
                   "cert-name::before"]:
        assert needle in t, f"missing: {needle}"

    raw = t.encode()
    with open(TMP, "wb") as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())
    got = open(TMP, "rb").read()
    assert got == raw, "temp write mismatch — STOP"
    os.replace(TMP, TARGET)
    print(f"APPLY-CERT DONE: {len(raw)} B sha256 "
          f"{hashlib.sha256(raw).hexdigest()}")
    return t


if __name__ == "__main__":
    main()
