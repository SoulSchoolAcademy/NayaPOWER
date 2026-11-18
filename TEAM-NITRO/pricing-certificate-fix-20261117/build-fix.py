#!/usr/bin/env python3
"""Pricing Certificate Fix round (2026-11-17) — Shawn's scorecard on the
staged /free certificate (eye 768bd8dd + his 19:37Z words).

BASE (reproduced in memory first, fail-stop if moved): the
certificate-current tip — entry 332,182 B sha 1e1bb489... (branch
pricing/certificate-current-20261117, tip d60151b2, PR #3419 open).
SOURCE OF THE BEAUTIFUL ONE (found, diff-proven, §1): Certificate Round 2
v2.13, identity-fixed-v213-staged.html, 326,013 B, sha
171eb90ccf486d7d079f0ff1b313d585a7b0f18ff6aa7080ee4b6484f011d2a8 — the
Micheal Nº 000204 treatment (Round 2, 2026-11-15), filed on GitHub as blob
bfe6461b808fdc0e9b3100e97b48fc096315af29 (branch
identity/certificate-round2-20261115) and byte-identical on disk. Its
certificate head IS the image's concept: the amethyst-crystal N seal in
its ring, five stones under the seal, the engraved title, "This certifies
that", the name. Its NAME construction (carved depth layers on the same
data-text mechanism: ::before extrusion below, ::after top-edge light)
is harvested into this fix, repainted per Shawn's new word — it is NOT
swapped in whole as the base: swapping the whole v2.13 file would delete
Rounds 3-5 and the current round's proven harvest (obsidian panels with
typed values, the 9-paragraph reader, TAKEN state, restore, Marcellus,
the exact official sentence), which §3.7 orders kept. The base stays the
certificate-current tip; v2.13's head and name-depth construction ride
on it. The fixpass fa3b2197 (326,004 B) is the same v2.13 with the
certified-name offset + indents corrected; its alignment corrections are
already carried in the current base.

THE FIX (each edit asserted, never retyped where harvest applies):
  F1 TITLE — "Certificate of Smart Identity" -> "Certificate of the
     Collective Agreement" (the one HTML title element).
  F2 CERTIFIES — "This certifies that" -> "This certificate of the
     Collective Agreement certifies that" (the one HTML line; the other
     7 occurrences are historical comments, untouched).
  F3 NAME SOLID WHITE — the Round 4 trophy's obsidian-gradient body
     (transparent color, background-clip) is retired: color #ffffff
     (solid fill, thick inside), the 1px chrome stroke stays as the
     THIN border, the purple clone behind stays as the light behind
     the object (the NayaNET wordmark glow, refined into a real
     object), plus a carved depth text-shadow and a ::after top-edge
     light harvested in construction from v2.13 (repainted white).
     The certified + taken text-shadow:none resets are removed — with
     a solid fill there is nothing to bleed through.
  F4 AGREEMENT STAYS — the certified hide rule for .cert-agree is
     replaced by a compact visible rule: the agreement-signing wording
     is the certificate's substance on the certified face too. The
     welcome-back status stays as the secondary line. Benefit +
     privacy are already hidden on certified, so the foot barely grows.
  F5 635 WRAP — the composing face gets the short-viewport treatment
     the certified/taken faces already have (overflow-y:auto +
     static flex face at max-height:700px; seal 72px), because the
     pre-claim agreement line was clipped by the card's
     overflow:hidden with nowhere to scroll at 635x349; plus an
     explicit wrap guard on .cert-agree.
  F6 CLAIM PATH — the Enter KEY claims. There was NO keydown on the
     alias field at all (no form element, no Enter handler): the button
     was the only claim path and the eye's Enter did nothing but let
     the debounced check show "Available". Now Enter with an Available
     alias calls activateAndRedirect (the button's own claim); Enter
     otherwise runs the availability check at once; Taken stays put.
     THE CLAIM PATH IS THE ENTER KEY (when Available) AND THE ENTER
     BUTTON (always) — both call activateAndRedirect().

Builds entirely in memory and stages to naya-pricing-free-staging ONLY.
Pricing v78 untouched. Nothing live, no merge, no voice.
"""
import difflib
import gzip
import hashlib
import importlib.util
import os
import re
import sys

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
sys.path.insert(0, os.path.expanduser("~/workspace/ninaya/integration"))

CURDIR = os.path.expanduser("~/workspace/team-nitro/pricing-certificate-current-20261117")
HERE = os.path.expanduser("~/workspace/team-nitro/pricing-certificate-fix-20261117")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_cur = load("certcurrent", os.path.join(CURDIR, "build-certificate.py"))
_bt = _cur._bt
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
BASE_ENTRY_SHA = "1e1bb4894b3e4bffed026781ac08976e8353b0e2bb020652357f567a711b16a3"
BASE_WORKER_SHA = "f4cc645f218b8b2a81f4daff7fcbb0ef604d8ac82bd867c38875dab0e6f44e73"
# PREV_ENTRY_SHA / PREV_WORKER_SHA: the first staging of THIS round
# (2026-11-17 19:50Z, entry 335,913 B, sha 6ef38123...) — superseded by
# the re-run below (a comment-only wording change). The fix re-run
# re-derives from the filed chain, never from live, but the live guards
# must accept these bytes as the expected live state.
PREV_ENTRY_SHA = "6ef38123b3a1b9bb813388e42f3c457c3018c99f6b650c9a60f59ed931619e07"
PREV_WORKER_SHA = "10e7acfa3c2f17938b3466027a9882495147b70e3fe9967db0486d0012455309"
IDENTITY_SHA = "8c641f96d31818b610d1a243d945dfb5c68e6016e036b7afb11b72445330013d"
PRICING_V78_SHA = "ca2eafeb896c763ae2459b4a10b8715e726765ced607c0aab3640d27e6c39ae2"
SW_SHA = "abac2ab507fc162788d9bdcd60f895049222e125d1445a4870be71342625d6a3"
MANI_SHA = "b4abd81c41e85f4149be355f740dd8ff9b136f6ea85e8b5874073a0686c67e81"
# Round 2 v2.13, the earlier beautiful certificate (Micheal Nº 000204).
V213_SHA = "171eb90ccf486d7d079f0ff1b313d585a7b0f18ff6aa7080ee4b6484f011d2a8"
V213_PATH = os.path.expanduser(
    "~/workspace/team-nitro/walk-v23-assembly-20261114/identity-fixed-v213-staged.html")


def sha(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode()).hexdigest()


# ------------------------------------------------------------------- fix
AFTER_RULE = (
    "    .cert-name::after { content: attr(data-text); position: absolute; inset: 0;\n"
    "      font: inherit; letter-spacing: inherit; line-height: inherit; text-align: center;\n"
    "      overflow-wrap: anywhere; pointer-events: none; z-index: 1;\n"
    "      transform: translateY(-1px); opacity: 0.5; color: #ffffff;\n"
    "      /* CERTIFICATE FIX: the top-edge light — the construction is harvested from Round 2 v2.13's ::after (light-gold top edge, same data-text mechanism) and repainted white, so the white object catches the light on its top edge. */ }"
)

ENTER_KEY_JS = (
    "\n    /* CERTIFICATE FIX (2026-11-17): the Enter KEY claims. The eye found the key did nothing — there was no keydown on the alias field at all (no form element, no Enter handler): the button was the only claim path. Now: Enter with an Available alias claims it (activateAndRedirect, the button's own claim); Enter otherwise runs the availability check at once, so a first Enter checks and a second claims. Taken stays put. THE CLAIM PATH IS THE ENTER KEY (when Available) AND THE ENTER BUTTON (always). */\n"
    "    (function(){\n"
    "      var inp = document.getElementById('aliasInput');\n"
    "      if (!inp) return;\n"
    "      inp.addEventListener('keydown', function(e){\n"
    "        if (e.key !== 'Enter') return;\n"
    "        e.preventDefault();\n"
    "        var st = document.getElementById('aliasStatus');\n"
    "        var state = st ? st.getAttribute('data-state') : '';\n"
    "        if (state === 'available') { window.activateAndRedirect(); return; }\n"
    "        if (state === 'taken') return;\n"
    "        var a = (inp.value || '').toLowerCase().replace(/[^a-z0-9]/g, '');\n"
    "        if (a) checkAliasAvailability(a, true);\n"
    "      });\n"
    "    })();\n"
)

COMPOSING_SCROLL = (
    "    /* CERTIFICATE FIX (2026-11-17): the COMPOSING face gets the same short-viewport treatment the certified/taken faces already have. At 635x349 the pre-claim agreement line was clipped by the card's overflow:hidden with nowhere to scroll — the card is one element (.identity-pro-card.cert-plaque), so overflow-y:auto on the plaque opens the scroll path and the static flex face lets the foot flow. Seal steps down to 72px to free room, as on certified. */\n"
    "    @media (max-height:700px){\n"
    "      .cert-plaque:not(.is-certified){overflow-y:auto}\n"
    "      .cert-plaque:not(.is-certified) .identity-face{position:static;display:flex;flex-direction:column;justify-content:center;min-height:100%;box-sizing:border-box}\n"
    "      .cert-plaque:not(.is-certified) .face-head,.cert-plaque:not(.is-certified) .face-foot{align-self:auto}\n"
    "      .cert-plaque:not(.is-certified) .face-foot{margin-top:16px}\n"
    "      .cert-plaque:not(.is-certified) .cert-seal{width:72px;height:72px}\n"
    "      .cert-plaque:not(.is-certified) .cert-jewels{margin-top:6px}\n"
    "    }\n"
)


def apply_fix(d, h):
    """Apply F1-F6 to the reproduced certificate-current tip."""
    assert "CERTIFICATE FIX (2026-11-17" not in d, "fix already present"
    new = d

    # --- F1 title (the one HTML title element).
    assert new.count("Certificate of Smart Identity") == 1, "title moved"
    new = replace_once(new, "Certificate of Smart Identity",
                       "Certificate of the Collective Agreement", "F1 title")

    # --- F2 certifies (the one HTML line; 7 comment mentions untouched).
    assert new.count('<p class="cert-certifies">This certifies that</p>') == 1
    new = replace_once(
        new, '<p class="cert-certifies">This certifies that</p>',
        '<p class="cert-certifies">This certificate of the Collective Agreement certifies that</p>',
        "F2 certifies")

    # --- F3 name solid white: retire the obsidian-gradient body.
    paint_block = (
        "      color: transparent;\n"
        "      background-image: linear-gradient(180deg, #34343e 0%, #131318 34%, #050505 62%, #0a0a0e 100%);\n"
        "      -webkit-background-clip: text; background-clip: text;\n")
    assert new.count(paint_block) == 1, "name paint block moved"
    new = replace_once(
        new, paint_block,
        "      color: #ffffff; /* CERTIFICATE FIX (2026-11-17): SOLID WHITE — thick inside, thin border. The fill is white now; the 1px chrome stroke below stays as the thin border; the purple clone behind stays as the light behind the object (the NayaNET wordmark glow, refined into a real object); the top-edge light (::after) and the carved depth shadow below make it a real object — more real, more profound. The obsidian-gradient body of Round 4 H1 is retired: Shawn — \"too much border, not enough inside\". */\n",
        "F3 solid fill")
    # Carved depth: a body edge below the white letter.
    new = replace_once(
        new, "      -webkit-text-stroke: 1px rgba(255,255,255,0.92);",
        "      -webkit-text-stroke: 1px rgba(255,255,255,0.92);\n"
        "      text-shadow: 0 2px 0 rgba(20,8,40,0.55), 0 4px 18px rgba(0,0,0,0.55); /* CERTIFICATE FIX: carved depth — the white letter sits IN the black with a body edge below it. */",
        "F3 depth shadow")
    # Certified + taken text-shadow:none resets: nothing to bleed through now.
    new = replace_once(
        new,
        "text-shadow: none; /* v2.12: the gold gradient carries its own drop-shadow; a text-shadow would bleed through the transparent glyphs. */",
        "/* CERTIFICATE FIX: no text-shadow reset — the fill is solid white now, so the carved depth shadow reads instead of bleeding through. */",
        "F3 certified shadow reset out")
    new = replace_once(
        new,
        "text-shadow:none; /* CERTIFICATE CURRENT: the clone carries the glow now. */",
        "/* CERTIFICATE FIX: the solid white fill keeps its carved depth shadow here too. */",
        "F3 taken shadow reset out")
    # ::after top-edge light, right after the clone paint rule.
    new = replace_once(new, h["clone_b"], h["clone_b"] + "\n" + AFTER_RULE,
                       "F3 top-edge light")

    # --- F4 agreement stays on the certified certificate.
    assert new.count("    .cert-plaque.is-certified .cert-agree { display: none; }") == 1
    new = replace_once(
        new, "    .cert-plaque.is-certified .cert-agree { display: none; }",
        "    .cert-plaque.is-certified .cert-agree { display: block; font-size: 0.78rem; line-height: 1.35; margin-top: 8px; } /* CERTIFICATE FIX (2026-11-17): the agreement-signing wording STAYS on the certified certificate — it is the certificate's substance, not a composing-only line. The welcome-back status stays as the secondary line. Compact type so the certified foot barely grows: benefit + privacy are already hidden on certified. */",
        "F4 agree stays on certified")

    # --- F5 635 wrap: explicit wrap guard + composing short-viewport scroll.
    new = replace_once(
        new, "max-width: 740px; padding: 0 6px;",
        "max-width: 740px; padding: 0 6px; overflow-wrap: anywhere; white-space: normal; /* CERTIFICATE FIX: the sentence always wraps — never one overflowing line. */",
        "F5 wrap guard")
    certified_scroll = (
        "    @media (max-height:700px){\n"
        "      .cert-plaque.is-certified{overflow-y:auto}\n"
        "      .cert-plaque.is-certified .identity-face{position:static;display:flex;flex-direction:column;justify-content:center;min-height:100%;box-sizing:border-box}\n"
        "      .cert-plaque.is-certified .face-head,.cert-plaque.is-certified .face-foot{align-self:auto}\n"
        "      .cert-plaque.is-certified .face-foot{margin-top:16px}\n"
        "      .cert-plaque.is-certified .cert-seal{width:72px;height:72px}\n"
        "      .cert-plaque.is-certified .cert-jewels{margin-top:6px}\n"
        "    }\n")
    assert new.count(certified_scroll) == 1, "certified scroll block moved"
    new = replace_once(new, certified_scroll,
                       certified_scroll + COMPOSING_SCROLL,
                       "F5 composing scroll")

    # --- F6 Enter key claims.
    anchor = "    if (savedAlias) checkAliasAvailability(savedAlias, true);"
    assert new.count(anchor) == 1, "restore anchor moved"
    new = replace_once(new, anchor, anchor + ENTER_KEY_JS, "F6 Enter key claims")
    return new


def check_invariants(old, new):
    """Everything the fix must hold, and everything it must not move."""
    # F1/F2
    assert new.count("Certificate of Smart Identity") == 0, "old title survives"
    assert new.count('<div class="cert-title">Certificate of the Collective Agreement</div>') == 1
    assert new.count('<p class="cert-certifies">This certificate of the Collective Agreement certifies that</p>') == 1
    assert new.count('<p class="cert-certifies">This certifies that</p>') == 0
    # The all-caps old title survives ONLY in one historical v2.x comment.
    assert new.count("CERTIFICATE OF SMART IDENTITY") == 1, "old-title comment count moved"
    # F3
    assert "background-image: linear-gradient(180deg, #34343e 0%, #131318 34%, #050505 62%, #0a0a0e 100%)" not in new
    assert new.count("color: transparent") == 1, "transparent color must survive only in the clone"
    assert ".cert-name::after" in new and "CERTIFICATE FIX: the top-edge light" in new
    assert "text-shadow: 0 2px 0 rgba(20,8,40,0.55)" in new
    # F4
    assert "    .cert-plaque.is-certified .cert-agree { display: none; }" not in new
    assert ".cert-plaque.is-certified .cert-agree { display: block;" in new
    assert '.face-foot:has(.alias-status[data-state="taken"]) .cert-agree { display: none; }' in new
    assert new.count("This Smart Name is yours") == 1, "welcome-back line moved"
    # F5
    assert ".cert-plaque:not(.is-certified){overflow-y:auto}" in new
    assert "overflow-wrap: anywhere; white-space: normal;" in new
    # F6
    assert "the Enter KEY claims" in new
    assert "window.activateAndRedirect(); return; }" in new
    # Kept
    assert new.count("By entering your name, you make it official") == 1, "official sentence moved"
    assert new.count('class="cert-info-para"') == 9
    assert new.count("paintHeroName(") >= 4 and new.count("paintValues(") >= 4
    assert new.count("})();") >= 2, "an IIFE closer is missing — STOP"
    assert "Marcellus" in new and new.count("Newsreader") == 0
    assert "cert-seal" in new and "cert-jewels" in new and "five stones" in new
    assert ".cert-name { font-size: clamp(2.4rem, 6.4vw, 4.1rem); }" in new
    assert ".cert-name { font-size: clamp(2.55rem, 13.5vw, 3.4rem); }" in new
    assert ".cert-name{font-size:clamp(1.65rem,6.2vw,2.5rem);}" in new
    assert ".cert-name[hidden] { display: none; }" in new
    assert "text-shadow:none; /* CERTIFICATE CURRENT: the clone carries the glow now. */" not in new
    print("invariants: PASS (F1-F6 present, kept pieces byte-identical)")


def main():
    # 0. The earlier beautiful certificate: found on disk, hash-verified.
    raw213 = open(V213_PATH, "rb").read()
    assert len(raw213) == 326013 and sha(raw213) == V213_SHA, \
        f"v2.13 moved: {len(raw213)} B sha={sha(raw213)}"
    print(f"v2.13 FOUND on disk: 326,013 B sha={V213_SHA[:8]}... (Micheal Nº 000204, Round 2)")

    # 0a. Reproduce the certificate-current tip in memory.
    walk_pf, entry_pf = _cur.regen_pricing_fix_tip()
    h = _cur.harvest_identity()
    base_entry = _cur.apply_certificate(entry_pf, h)
    assert sha(base_entry) == BASE_ENTRY_SHA, \
        f"tip NOT reproduced: {sha(base_entry)} — STOP"
    print(f"base reproduced: entry {len(base_entry.encode())} B sha={sha(base_entry)[:8]}... MATCH")

    # 0b. Live staged guards: /free + /free/walk + identity must serve the tip
    # (or this round's first staging on a fix re-run — the fix re-derives
    # from the filed chain, never from live).
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

    # 0c. Harvest live PWA assets verbatim.
    st, _, sw = _sim.http_get(LIVE + "/sw.js")
    assert st == 200, f"live sw.js: {st}"
    sw = sw.decode("utf-8")
    assert sha(sw) == SW_SHA, f"sw.js moved: {sha(sw)}"
    st, _, mani = _sim.http_get(LIVE + "/manifest.webmanifest")
    assert st == 200, f"live manifest: {st}"
    mani = mani.decode("utf-8")
    assert sha(mani) == MANI_SHA, f"manifest moved: {sha(mani)}"
    print(f"harvested live PWA assets: sw.js {len(sw.encode())} B, manifest {len(mani.encode())} B")

    # 0d. Reproduce the CURRENT staged worker byte-exact before changing anything.
    st, raw = _sim.api("GET", "/naya-pricing-free-staging")
    assert st == 200, f"worker GET failed: {st}"
    _, wb, _ = _sim.split_multipart(raw)
    assert sha(wb) in (BASE_WORKER_SHA, PREV_WORKER_SHA), \
        f"live staged worker moved: {sha(wb)[:8]}... — STOP"
    free_index = _bf.FREE_INDEX.replace(
        "__PRICING_STAGED__", "https://naya-pricing-f4-staging.nayapower.workers.dev/")
    worker_cur = _cur.build_worker_for(walk_pf, base_entry, sw, mani)
    assert sha(worker_cur) == BASE_WORKER_SHA, \
        f"current worker NOT reproduced: {sha(worker_cur)} — STOP"
    print(f"current worker reproduced: {len(worker_cur.encode())} B sha={sha(worker_cur)[:8]}... MATCH")

    # 1. Apply the fix.
    new_entry = apply_fix(base_entry, h)
    check_invariants(base_entry, new_entry)
    diff = list(difflib.unified_diff(base_entry.splitlines(), new_entry.splitlines(), lineterm="", n=0))
    removed = [ln for ln in diff if ln.startswith("-") and not ln.startswith("---")]
    added = [ln for ln in diff if ln.startswith("+") and not ln.startswith("+++")]
    print(f"entry diff: +{len(added)} lines, -{len(removed)} lines")
    for ln in removed:
        print("   -", ln[:220])
    for ln in added:
        print("   +", ln[:220])
    print(f"new entry: {len(new_entry.encode())} B sha256={sha(new_entry)}")
    _cur.js_syntax_check(new_entry)

    # 2. Worker rebuild with the new entry (walk unchanged) + node driver.
    new_worker = _cur.build_worker_for(walk_pf, new_entry, sw, mani)
    print(f"new worker: {len(new_worker.encode())} B sha256={sha(new_worker)}")
    gz = gzip.compress(new_worker.encode("utf-8"))
    print(f"worker gzip: {len(gz)} B (limit 10,485,760)")
    assert len(gz) < 10485760

    _sim.node_check(new_worker, FREE_HOST + "/free", sha(new_entry),
                    ["CERTIFICATE FIX (2026-11-17",
                     "Certificate of the Collective Agreement",
                     "This certificate of the Collective Agreement certifies that",
                     "color: #ffffff; /* CERTIFICATE FIX",
                     "cert-name::after", "the Enter KEY claims",
                     ".cert-plaque.is-certified .cert-agree { display: block;",
                     ".cert-plaque:not(.is-certified){overflow-y:auto}",
                     "By entering your name, you make it official",
                     'id="certInfoReader"', 'id="certInfoBtn"',
                     "paintHeroName", "paintValues", "settleHeroName",
                     "background: linear-gradient(180deg, #101013 0%, #050505 46%, #070708 100%)",
                     "--silver: #ffffff;", "--muted: #ffffff;",
                     "name-settle", "cert-info-para",
                     "TAKEN STATE (2026-11-17", "function fitTakenName()",
                     "PRICING FIX (2026-11-17", "Use a different alias",
                     "Enter free &mdash; no payment, no card.",
                     "--serif: Marcellus, Georgia, serif;",
                     'id="startOverBtn"', "WALKTHROUGH_URL = '/free/walk'"],
                    ['<div class="cert-title">Certificate of Smart Identity</div>',
                     '<p class="cert-certifies">This certifies that</p>',
                     ".cert-plaque.is-certified .cert-agree { display: none; }",
                     "background-image: linear-gradient(180deg, #34343e 0%, #131318 34%, #050505 62%, #0a0a0e 100%)",
                     "Newsreader", "#f2f2f6", "#a8dcff", "#ffd97a",
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
    # NOTE: do NOT open-then-write here — the EPERM flake truncates on
    # open() and leaves a 0-byte file (build-fix.py itself was destroyed
    # exactly this way on 2026-11-17 and had to be rewritten from the
    # filed copy). The bytes live in memory + on the staged worker; the
    # filing script re-derives them in memory, never from disk.
    print("SKIP disk save (EPERM flake: truncate-first writes destroy files; "
          "bytes reproducible in memory from this build script + staged worker)")
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
