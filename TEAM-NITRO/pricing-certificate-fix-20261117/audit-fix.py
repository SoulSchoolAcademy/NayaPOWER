#!/usr/bin/env python3
"""Pricing Certificate Fix — independent static audit of the STAGED bytes.
Re-derives the new entry in memory (never from disk — the EPERM flake
leaves fixed-entry.html unwritten), fetches live staged /free, asserts
sha equality, then counts every acceptance item + prints the base->new
diff. No staging, no filing, no browser.
"""
import difflib
import hashlib
import importlib.util
import os
import re
import sys

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
sys.path.insert(0, os.path.expanduser("~/workspace/ninaya/integration"))

CURDIR = os.path.expanduser("~/workspace/team-nitro/pricing-certificate-current-20261117")
FIXDIR = os.path.expanduser("~/workspace/team-nitro/pricing-certificate-fix-20261117")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode()).hexdigest()


bf = load("buildfix", os.path.join(FIXDIR, "build-fix.py"))
_cur = bf._cur
_sim = bf._sim

WANT = "fbd6477f348ab50b8b0eb278fb36e475c25eb55ae27a4d79ca416942161f16fd"
BASE_SHA = bf.BASE_ENTRY_SHA

walk_pf, entry_pf = _cur.regen_pricing_fix_tip()
h = _cur.harvest_identity()
base_entry = _cur.apply_certificate(entry_pf, h)
assert sha(base_entry) == BASE_SHA, "base tip NOT reproduced — STOP"
new_entry = bf.apply_fix(base_entry, h)
assert sha(new_entry) == WANT, f"re-derived new entry != staged: {sha(new_entry)}"
print(f"new entry re-derived in memory: {len(new_entry.encode())} B sha={WANT[:8]}...")

st, _, got = _sim.http_get(
    "https://naya-pricing-free-staging.nayapower.workers.dev/free")
assert st == 200
live = got.decode("utf-8")
assert sha(live) == WANT, "live staged /free moved — STOP"
assert live == new_entry, "live staged bytes != re-derived bytes — STOP"
print(f"live staged /free: {len(got)} B sha={WANT[:8]}... == re-derived MATCH")

_cur.js_syntax_check(live)
print("JS syntax: all inline script blocks compile (node vm.Script, stdin)")


def count(pat, text=None):
    return (text if text is not None else live).count(pat)


print("\n--- A1 earlier beautiful certificate ---")
print("  v2.13 on disk: 326,013 B sha 171eb90c... (asserted in build-fix.py step 0)")
print("  v2.13 GitHub blob bfe6461b...: 326,013 B, decoded sha256 171eb90c... (blob API)")
print("  v2.13 head present in new entry: seal", count("cert-seal"), "| stones",
      count("cert-jewels"), "| 'five stones'", count("five stones"))

print("\n--- A2 title ---")
print("  'Certificate of the Collective Agreement' (title div):",
      count('<div class="cert-title">Certificate of the Collective Agreement</div>'))
print("  'Certificate of Smart Identity' (anywhere):", count("Certificate of Smart Identity"))
print("  'CERTIFICATE OF SMART IDENTITY' (anywhere):", count("CERTIFICATE OF SMART IDENTITY"))
print("  'This certificate of the Collective Agreement certifies that':",
      count("This certificate of the Collective Agreement certifies that"))
print("  'This certifies that' (HTML line):",
      count('<p class="cert-certifies">This certifies that</p>'),
      "| total occurrences (comments):", count("This certifies that"))

print("\n--- A3 name solid white ---")
print("  'color: #ffffff; /* CERTIFICATE FIX' (solid fill):",
      count("color: #ffffff; /* CERTIFICATE FIX"))
print("  'color: transparent' (clone only):", count("color: transparent"))
print("  obsidian gradient body gone:", "linear-gradient(180deg, #34343e" not in live)
print("  chrome stroke kept (thin border):",
      count("-webkit-text-stroke: 1px rgba(255,255,255,0.92)"))
print("  carved depth text-shadow:", count("text-shadow: 0 2px 0 rgba(20,8,40,0.55)"))
print("  ::after top-edge light:", count(".cert-name::after"),
      "| clone ::before (halo):", count(".cert-name::before"))
print("  name-settle:", count("name-settle"), "| hover rules:", count(".cert-name:hover"))
print("  geometry kept: desktop clamp", count("clamp(2.4rem, 6.4vw, 4.1rem)"),
      "| phone clamp", count("clamp(2.55rem, 13.5vw, 3.4rem)"),
      "| taken clamp", count("clamp(1.65rem,6.2vw,2.5rem)"))

print("\n--- A4 agreement stays on certified ---")
print("  certified agree hide rule:", count(".cert-plaque.is-certified .cert-agree { display: none; }"))
print("  certified agree visible rule:", count(".cert-plaque.is-certified .cert-agree { display: block;"))
print("  taken agree hide rule (kept):",
      count('.face-foot:has(.alias-status[data-state="taken"]) .cert-agree { display: none; }'))
print("  official sentence exact x1:", count("By entering your name, you make it official"))
print("  welcome-back secondary line x1:", count("This Smart Name is yours"))
print("  reader paras:", count('class="cert-info-para"'), "| reader present:",
      count('id="certInfoReader"'))
print("  'Collective Agreement' total:", count("Collective Agreement"))

print("\n--- A5 635 wrap (structural) ---")
print("  composing scroll rule:", count(".cert-plaque:not(.is-certified){overflow-y:auto}"))
print("  certified scroll rule:", count(".cert-plaque.is-certified{overflow-y:auto}"))
print("  taken scroll rule:", count('.cert-plaque:has(.alias-status[data-state="taken"]){overflow-y:auto}'))
print("  agree wrap guard:", count("overflow-wrap: anywhere; white-space: normal;"))
print("  agree 640px compact rule:", count(".cert-plaque:not(.is-certified):has(.cert-lines:not([hidden])) .cert-agree { font-size: 0.78rem;"))
print("  card clip (the cause): '.identity-pro-card' overflow hidden:",
      count("overflow: hidden;") , "| plaque == card (one element):",
      count('<div class="identity-pro-card cert-plaque" id="certPlaque">'))
# DOM order: agree <p> sits inside .face-foot inside #certPlaque (the scroll container).
i_plaque = live.find('id="certPlaque"')
i_agree = live.find('<p class="cert-agree">')
i_foot = live.find('<div class="face-zone face-foot">')
print("  DOM order plaque < foot < agree:", i_plaque < i_foot < i_agree)

print("\n--- A6 claim path ---")
print("  Enter-key claim IIFE:", count("the Enter KEY claims"))
print("  keydown on #aliasInput:", count("getElementById('aliasInput')"))
print("  Enter->activateAndRedirect:", count("if (state === 'available') { window.activateAndRedirect(); return; }"))
print("  ENTER button onclick:", count('onclick="activateAndRedirect()"'))
print("  claim function:", count("window.activateAndRedirect = function()"))
print("  <form> tags (must be 0 — Enter has no form to submit):", count("<form"))

print("\n--- A7 kept / no gray ---")
for pat in ["#f2f2f6", "#a8dcff", "#ffd97a", "#163a56", "#0a1c2e", "#3a2a09",
            "#1c1204", "#060402", "#a855f7", "Newsreader", "rgba(242,242,246"]:
    print(f"  cut token {pat}: {count(pat)}")
print("  Marcellus present:", "Marcellus" in live)
print("  obsidian panels:", count("linear-gradient(180deg, #101013 0%, #050505 46%, #070708 100%)"))
print("  paintHeroName calls:", count("paintHeroName("), "| paintValues calls:", count("paintValues("))
print("  IIFE closers })();:", count("})();"), "| bare }(); (must be 0):", count("}();"))
print("  cert number + date slots:", count('id="certNoValue"'), count('id="certDate"'))
print("  restore hook (savedAlias lookup):", count("if (savedAlias) checkAliasAvailability(savedAlias, true);"))

print("\n--- diff base -> new ---")
diff = list(difflib.unified_diff(base_entry.splitlines(), new_entry.splitlines(), lineterm="", n=0))
removed = [ln for ln in diff if ln.startswith("-") and not ln.startswith("---")]
added = [ln for ln in diff if ln.startswith("+") and not ln.startswith("+++")]
print(f"+{len(added)} lines, -{len(removed)} lines")
for ln in removed:
    print("   -", ln[:220])
for ln in added:
    print("   +", ln[:220])
print("\nAUDIT DONE")
