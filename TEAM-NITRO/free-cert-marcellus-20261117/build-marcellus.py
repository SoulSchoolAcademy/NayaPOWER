#!/usr/bin/env python3
"""Free Certificate Marcellus Swap (2026-11-17).

BASE (verified first, fail-stop if moved): the F4-follow-on staged bytes —
  walk 3,292,257 B sha 2370eae2... | entry 310,241 B sha e9462d8e... |
  worker 3,622,237 B sha f571768c... (checker-verified).
Regenerates the follow-on base in memory (follow-on builder functions)
and asserts the base shas before patching anything.

ITEM 1 — /free CERTIFICATE --serif -> MARCELLUS (the walk's font).
Captain's call 02:28Z (Shawn's thumbs-up): ONE serif in both places, and
it is Marcellus. The walk's certificate/end-slide headline are Marcellus;
the /free certificate is Newsreader. Align /free to Marcellus.
  (a) font loading restored faithfully: the css2 link tag VERBATIM from
      the live walk entrance (https://naya-walk-beginning-staging.
      nayapower.workers.dev/ carries exactly:
      css2?family=Marcellus&family=Outfit:wght@300;400;600;700;800;900
      &display=swap — verified live in this run, and independently by the
      follow-on checker). The Newsreader css2 URL is replaced by that
      Marcellus URL inside the entry's existing <link> tag, so the
      resulting tag is byte-identical to the entrance's tag (same href,
      same rel); the preconnect line is identical in both and stays.
      Outfit rides along unused, as on the walk.
  (b) --serif: 'Newsreader', Georgia, 'Times New Roman', serif
      -> Marcellus, Georgia, serif — the walk's stack
      (Marcellus,Georgia,serif), spaced to match this file's style.
      All 9 var(--serif) uses unchanged.
  Nothing else moves: same copy, same boxes, same seal, same ENTER,
  same layered glow shadows (extracted before/after and asserted
  identical), same narrow CSS, same start-over control. The walk is
  untouched (byte-identical). No new colors.

ITEM 2 — THE NAME STILL MEETS THE SN-2922 BAR (official, glowing, solid).
The layered glow text-shadows on .cert-name are extracted from the old
and new entry and asserted byte-identical; the --serif change only swaps
which face renders inside them. Marcellus css2 + latin woff2 verified
live (expect 14,552 B, wOF2 magic — the checker's measured size).
NOTE (honest, for the eye): Marcellus ships ONE weight (400) and NO
italic face. The certificate asks weight 560 for the name and (see the
inspection printout) italic for some serif lines — with Marcellus those
render the 400 face / a synthesized oblique, exactly as the walk's
800-weight Marcellus headline already does. The brief orders Marcellus;
the eye judges the paint.

ITEM 3 — NARROW LAYOUT STILL HOLDS WITH MARCELLUS.
Layout math from the served CSS (checker's harness approach) + real
glyph metrics: the served latin woff2 files measured with fontTools
for sample names at the certificate's real sizes, lines-needed computed
at the real column widths. Heights are family-independent (line-height
in em); only the name's line count can move the budgets, and the
margins cover it (see the printout).

Builds entirely in memory (EPERM flake) and stages to
naya-pricing-free-staging ONLY. Pricing worker NOT touched.
"""
import difflib
import hashlib
import importlib.util
import io
import math
import os
import re
import subprocess
import sys

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
sys.path.insert(0, os.path.expanduser("~/workspace/ninaya/integration"))

F4 = os.path.expanduser("~/workspace/team-nitro/pricing-free-entry-20261116")
F4FIX = os.path.expanduser("~/workspace/team-nitro/pricing-f4-fix-20261117")
FO = os.path.expanduser("~/workspace/team-nitro/pricing-f4-followon-20261117")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_bf = load("bfree", os.path.join(F4, "build-free-staging-worker.py"))
_fix = load("ffix", os.path.join(F4FIX, "build-fix.py"))
_fo = load("fo", os.path.join(FO, "build-followon.py"))
_sim = load("sim", os.path.join(F4, "stage-in-memory.py"))
replace_once = _bf.replace_once

FREE_HOST = "https://naya-pricing-free-staging.nayapower.workers.dev"
PRICING_HOST = "https://naya-pricing-f4-staging.nayapower.workers.dev"
WALK_ENTRANCE = "https://naya-walk-beginning-staging.nayapower.workers.dev/"

BASE_WALK_SHA = "2370eae2f9ae9e281d1c3f3b35d99f8699c7df6a2fe4f73328e2877c3b6453ea"
BASE_ENTRY_SHA = "e9462d8ee6fe3e45b4235bd7eb367dca658febcda42a0638eaad249dad86b814"
BASE_WORKER_SHA = "f571768cd3866a809d8f413da3db1c5461090afc47be62a7f7893e4dfbb06a06"
PRICING_V78_SHA = "ca2eafeb896c763ae2459b4a10b8715e726765ced607c0aab3640d27e6c39ae2"

OLD_SERIF_DEF = "--serif: 'Newsreader', Georgia, 'Times New Roman', serif;"
NEW_SERIF_DEF = "--serif: Marcellus, Georgia, serif;"
OLD_FONT_URL = ("https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght"
                "@0,6..72,400..700;1,6..72,400..700&display=swap")
NEW_FONT_URL = ("https://fonts.googleapis.com/css2?family=Marcellus"
                "&family=Outfit:wght@300;400;600;700;800;900&display=swap")


def sha(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode()).hexdigest()


def apply_marcellus_swap(d):
    """The swap: exactly two substitutions, nothing else."""
    assert d.count(OLD_SERIF_DEF) == 1, "serif def not found exactly once"
    d = replace_once(d, OLD_SERIF_DEF, NEW_SERIF_DEF, "serif def")
    assert d.count(OLD_FONT_URL) == 1, "Newsreader css2 URL not found exactly once"
    d = replace_once(d, OLD_FONT_URL, NEW_FONT_URL, "font URL")
    return d


def main():
    # 0. Regenerate the F4-follow-on base in memory; fail-stop if moved.
    walk_f4 = _fix.apply_walk_fixes(_bf.build_walk_free())
    entry_f4 = _bf.build_free_entry()
    walk = _fo.apply_item1_walk(walk_f4)
    entry = _fo.apply_entry_followon(entry_f4)
    worker = _fix.apply_worker_fix(_bf.build_worker(walk, entry))
    assert sha(walk) == BASE_WALK_SHA, f"base walk moved: {sha(walk)}"
    assert sha(entry) == BASE_ENTRY_SHA, f"base entry moved: {sha(entry)}"
    assert sha(worker) == BASE_WORKER_SHA, f"base worker moved: {sha(worker)}"
    print(f"base verified: walk {len(walk.encode())} B sha={sha(walk)[:8]}... "
          f"entry {len(entry.encode())} B sha={sha(entry)[:8]}... "
          f"worker {len(worker.encode())} B sha={sha(worker)[:8]}...")

    # 0b. Inspect the old entry: serif uses, italic serif lines, glow.
    print("--- old entry inspection ---")
    print("Newsreader occurrences:", entry.count("Newsreader"))
    print("Marcellus occurrences:", entry.count("Marcellus"))
    print("var(--serif) uses:", entry.count("var(--serif)"))
    for m in re.finditer(r'var\(--serif\)', entry):
        a = entry.rfind('{', 0, m.start()); c = entry.find('}', m.start())
        print("  USE:", entry[a:c + 1].replace('\n', ' ')[:200])
    print("italic rules in entry:")
    for m in re.finditer(r'[^{}]*font-style:\s*italic[^{}]*', entry):
        print("  ITALIC:", m.group(0).replace('\n', ' ')[:200])
    old_shadows = re.findall(r'text-shadow:[^;]*;', entry)
    print(f"layered text-shadows ({len(old_shadows)}):")
    for s in old_shadows:
        print("  SHADOW:", s[:300])
    old_certname = re.findall(r'\.cert-name[^{]*\{[^}]*\}', entry)
    print(f".cert-name rules ({len(old_certname)}):")
    for r in old_certname:
        print("  CERTNAME:", r.replace('\n', ' ')[:400])

    # 0c. The live entrance carries the Marcellus link verbatim (re-verify).
    r = subprocess.run(["curl", "-s", "--max-time", "25", "-A", "Mozilla/5.0",
                        WALK_ENTRANCE], capture_output=True, timeout=60)
    assert r.returncode == 0, "curl to live walk entrance failed"
    entrance = r.stdout.decode("utf-8", "replace")
    assert NEW_FONT_URL in entrance, "live entrance does NOT carry the Marcellus URL — STOP"
    assert '<link rel="preconnect" href="https://fonts.googleapis.com">' in entrance
    print("live entrance verified: Marcellus css2 URL + preconnect present verbatim")

    # 1. Apply the swap.
    new_entry = apply_marcellus_swap(entry)
    assert "Newsreader" not in new_entry, "Newsreader leaked into the new entry"
    assert new_entry.count("Marcellus") == 2, "Marcellus count wrong (want URL + --serif)"
    assert new_entry.count("var(--serif)") == 9, "cert serif uses changed"
    assert new_entry.count(NEW_FONT_URL) == 1
    assert "--serif: Marcellus, Georgia, serif;" in new_entry
    new_shadows = re.findall(r'text-shadow:[^;]*;', new_entry)
    assert new_shadows == old_shadows, "layered glow shadows CHANGED — STOP"
    new_certname = re.findall(r'\.cert-name[^{]*\{[^}]*\}', new_entry)
    # .cert-name rules use var(--serif), not the literal stack, so they must
    # be byte-identical before/after the swap.
    assert new_certname == old_certname, ".cert-name rules changed — STOP"
    print("swap applied: --serif -> Marcellus, Georgia, serif; css2 URL -> Marcellus+Outfit")
    print(f"new entry: {len(new_entry.encode())} B sha256={sha(new_entry)}")

    # 1b. The diff must touch ONLY the two lines.
    diff = list(difflib.unified_diff(entry.splitlines(), new_entry.splitlines(),
                                     lineterm="", n=1))
    changed = [ln for ln in diff if ln.startswith(("+", "-")) and not ln.startswith(("+++", "---"))]
    print("diff changed lines:")
    for ln in changed:
        print("   ", ln[:220])
    assert len(changed) == 4, f"diff touches more than the 2 lines: {len(changed)}"
    assert all("Newsreader" in ln or "Marcellus" in ln for ln in changed), "diff touches a non-font line — STOP"
    print("diff check: ONLY the --serif line and the font-link line changed")

    # 2. Marcellus really loads: css2 + latin woff2, live, right now.
    def parse_css2(cssb):
        """css2 -> list of (subset, family, style, url) in file order."""
        out = []
        for m in re.finditer(
                rb"/\* ([\w-]+) \*/\s*@font-face \{[^}]*?font-family: '([^']+)';"
                rb"[^}]*?font-style: (\w+);[^}]*?src: url\((https://[^)]+)\)",
                cssb, re.S):
            out.append((m.group(1).decode(), m.group(2).decode(),
                        m.group(3).decode(), m.group(4).decode()))
        return out

    st, _, css = _sim.http_get(NEW_FONT_URL)
    assert st == 200 and b"font-family: 'Marcellus'" in css, f"Marcellus css2: {st}"
    faces = parse_css2(css)
    assert faces, "no @font-face blocks parsed from Marcellus css2"
    latin = [f for f in faces if f[0] == "latin" and f[1] == "Marcellus"
             and f[2] == "normal"]
    assert latin, f"no latin Marcellus normal face: {faces}"
    st2, _, woff = _sim.http_get(latin[0][3])
    assert st2 == 200 and woff[:4] == b"wOF2", f"Marcellus woff2 fetch: {st2}"
    print(f"Marcellus loads: css2 200 ({len(css)} B, {css.count(b'@font-face')} faces), "
          f"latin woff2 200 ({len(woff)} B, wOF2 magic)")
    assert len(woff) == 14552, f"latin Marcellus woff2 size moved: {len(woff)} (checker measured 14,552)"

    # 3. Layout math with Marcellus — real glyph metrics (fontTools on the
    # served latin woff2 files themselves; brotli is installed, so TTFont
    # reads woff2 directly). Newsreader normal-400 latin woff2 is the
    # comparison face (132,000 B per the follow-on checker).
    from fontTools.ttLib import TTFont

    def fetch_latin_woff2(css_url, family):
        st, _, cssb = _sim.http_get(css_url)
        assert st == 200, f"css2 for {family}: {st}"
        faces = parse_css2(cssb)
        pick = [f for f in faces if f[0] == "latin" and f[1] == family
                and f[2] == "normal"]
        assert pick, f"no latin normal woff2 for {family}: {faces}"
        st2, _, woff = _sim.http_get(pick[0][3])
        assert st2 == 200 and woff[:4] == b"wOF2", f"woff2 for {family}: {st2}"
        return woff

    def width_px(font, text, px):
        cmap = font.getBestCmap()
        hmtx = font["hmtx"]
        upm = font["head"].unitsPerEm
        total = 0
        for ch in text:
            g = cmap.get(ord(ch))
            total += hmtx[g][0] if g else 0
        return total / upm * px

    marc_woff = fetch_latin_woff2(NEW_FONT_URL, "Marcellus")
    news_woff = fetch_latin_woff2(OLD_FONT_URL, "Newsreader")
    marc = TTFont(io.BytesIO(marc_woff))
    news = TTFont(io.BytesIO(news_woff))
    print(f"metrics: Marcellus latin woff2 {len(marc_woff)} B, "
          f"Newsreader latin woff2 {len(news_woff)} B")
    samples = ["Shawn Vibert", "F4 Followon Test", "Alex Morgan",
               "Alexander Christopher Bennett"]
    # cert-name sizes: desktop clamp(2.9rem,7.4vw,4.9rem)->78.4px cap;
    # <=640px clamp(2.55rem,13.5vw,3.4rem): 635w -> 54.4px cap, 390w -> 52.65px.
    cases = [("desktop 1919w", 78.4, 920), ("635w", 54.4, 599), ("390w", 52.65, 354)]
    print("name width (px) Marcellus vs Newsreader-400 — lines at column width:")
    worst = {}
    for label, px, col in cases:
        for name in samples:
            wm = width_px(marc, name, px)
            wn = width_px(news, name, px)
            lm, ln = math.ceil(wm / col), math.ceil(wn / col)
            print(f"  {label} {name!r}: Marcellus {wm:.0f}px ({lm} line(s)) vs "
                  f"Newsreader {wn:.0f}px ({ln} line(s))")
            worst[label] = max(worst.get(label, 0), lm)
    print("worst Marcellus line counts:", worst)
    # Budgets (checker basis, face heights measured from served CSS):
    # 635x349 certified: face 213px; flow+scroll, content ~523px (1-line name)
    #   + ~53px per extra name line — scroll absorbs it, ENTER stays in flow.
    # 390x844 certified: face 708px; content ~550px (1-line) + ~52px/extra line.
    name_line_635 = round(54.4 * 0.98)
    name_line_390 = round(52.65 * 0.98)
    content_635 = 72 + 15 + 30 + 20 + worst["635w"] * name_line_635 + 20 + 124 + 40 + 58 + 40 + 50
    content_390 = 94 + 15 + 30 + 20 + worst["390w"] * name_line_390 + 20 + 130 + 40 + 58 + 40 + 50
    print(f"budget 635x349: face 213px vs content ~{content_635}px "
          f"(worst {worst['635w']} name line(s)) -> scroll, no overlap, ENTER in flow")
    print(f"budget 390x844: face 708px vs content ~{content_390}px "
          f"(worst {worst['390w']} name line(s)) -> "
          f"{'FITS in grid mode' if content_390 < 708 else 'OVERFLOW — STOP'}")
    assert content_390 < 708, "390px budget fails with Marcellus"
    assert new_entry.count("@media (max-width:640px)") >= 1
    assert ".cert-plaque.is-certified .cert-regalia{flex-direction:column" in new_entry
    assert ".cert-plaque.is-certified{overflow-y:auto}" in new_entry
    assert ".cert-plaque.is-certified .identity-face{position:static;display:flex;flex-direction:column" in new_entry
    assert re.search(r"\.activate-btn \{ position: relative;", new_entry)
    print("layout: narrow rules intact; 390 fits, 635 scrolls by design")

    # 4. Markers: new present, old-code intact where it must be.
    for good in [NEW_FONT_URL, "--serif: Marcellus, Georgia, serif;",
                 "id=\"startOverBtn\"", "Use a different alias",
                 ".cert-plaque.is-certified .cert-regalia{flex-direction:column",
                 ".cert-plaque.is-certified{overflow-y:auto}",
                 "Enter free &mdash; no payment, no card."]:
        assert good in new_entry, f"marker missing: {good}"
    for keep in ["buildBarFill", "25000", "showStep(16)",
                 "The build timed out after 25 seconds",
                 "WALKTHROUGH_URL = '/free/walk'"]:
        assert keep in (walk + new_entry), f"F4 marker lost: {keep}"
    assert "Newsreader" not in new_entry and "Newsreader" not in walk
    assert walk.count("Marcellus") == 4, "walk Marcellus count moved (walk must be untouched)"
    assert sha(walk) == BASE_WALK_SHA, "walk bytes moved — STOP"
    print("markers: HAVE all; walk byte-identical; serif separation holds "
          "(walk Marcellus, cert Marcellus, Newsreader nowhere)")

    # 5. Build the new worker, prove it serves the new entry via Node.
    free_index = _bf.FREE_INDEX.replace(
        "__PRICING_STAGED__", "https://naya-pricing-f4-staging.nayapower.workers.dev/")
    new_worker = _fix.apply_worker_fix(_bf.build_worker(walk, new_entry))
    print(f"new worker: {len(new_worker.encode())} B sha256={sha(new_worker)}")
    import gzip
    gz = gzip.compress(new_worker.encode("utf-8"))
    print(f"worker gzip: {len(gz)} B (limit 10,485,760)")
    assert len(gz) < 10485760
    _sim.node_check(new_worker, FREE_HOST + "/free", sha(new_entry),
                    [NEW_FONT_URL, "--serif: Marcellus, Georgia, serif;",
                     "id=\"startOverBtn\"", "Use a different alias",
                     ".cert-plaque.is-certified .cert-regalia{flex-direction:column",
                     ".cert-plaque.is-certified{overflow-y:auto}",
                     "Enter free &mdash; no payment, no card.",
                     'id="freeEye"', "WALKTHROUGH_URL = '/free/walk'"],
                    ["Newsreader"])
    _sim.node_check(new_worker, FREE_HOST + "/free/walk", sha(walk),
                    ["fonts.googleapis.com/css2?family=Marcellus",
                     "font-family:Marcellus,Georgia,serif",
                     ".p3-congrats{font-family:Marcellus",
                     "buildBarFill", "showStep(16)"],
                    ["Newsreader"])
    _sim.node_check(new_worker, FREE_HOST + "/", sha(free_index),
                    ["Enter free — the route, staged"], [])
    _sim.node_redirect_check(new_worker, FREE_HOST + "/free/hub",
                             "https://nayanet.app/")
    print("node driver: PASS (new entry + unchanged walk + index + hub)")

    # 6. Stage the new free worker (STAGING ONLY — pricing untouched).
    kv = [{"type": "kv_namespace", "name": "WELCOME_ASSETS",
           "namespace_id": "1cf80db6183245d19dd5296645a12bd0"}]
    _sim.put_worker("naya-pricing-free-staging", new_worker.encode(), kv)
    status, raw = _sim.api("GET", "/naya-pricing-free-staging")
    assert status == 200
    _, wb, _ = _sim.split_multipart(raw)
    assert wb == new_worker.encode(), "read-back differs from PUT — STOP"
    print(f"read-back sha256={sha(wb)} — MATCH")

    # 7. Live HTTP verification of the staged routes.
    for path, want in [("/", free_index), ("/free", new_entry),
                       ("/free/walk", walk)]:
        st, _, got = _sim.http_get(FREE_HOST + path)
        assert st == 200, f"GET {path}: {st}"
        assert got.decode("utf-8") == want, f"GET {path}: bytes != source — STOP"
        print(f"GET {FREE_HOST}{path}: 200, {len(got)} B == source MATCH")
    st, hdrs, _ = _sim.http_get(FREE_HOST + "/free/hub")
    assert st in (301, 302) and hdrs.get("Location") == "https://nayanet.app/"
    print("GET /free/hub: 302 -> https://nayanet.app/ MATCH")

    # 8. Pricing v78 still byte-exact on its own staging worker (untouched).
    st, _, v78 = _sim.http_get(PRICING_HOST + "/")
    assert st == 200 and sha(v78) == PRICING_V78_SHA, "pricing v78 MOVED — STOP"
    print(f"pricing v78: {len(v78)} B sha={sha(v78)[:8]}... UNCHANGED")

    print("BUILD+STAGE OK")
    print(f"  walk sha256={sha(walk)} (UNCHANGED)")
    print(f"  entry sha256={sha(new_entry)}")
    print(f"  worker sha256={sha(new_worker)}")
    return {"walk": walk, "entry": new_entry, "free_index": free_index,
            "worker": new_worker}


if __name__ == "__main__":
    main()
