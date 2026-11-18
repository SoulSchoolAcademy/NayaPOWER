#!/usr/bin/env python3
"""Metrics-only re-derivation for the Marcellus swap (no staging).
Regenerates the follow-on base in memory, applies the swap, fetches the
served latin woff2 files, measures sample-name widths with fontTools,
and prints the layout budgets. Used to capture the numbers for the
maker report after the build run's stdout was tail-truncated."""
import hashlib
import importlib.util
import io
import math
import os
import re
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

NEW_FONT_URL = ("https://fonts.googleapis.com/css2?family=Marcellus"
                "&family=Outfit:wght@300;400;600;700;800;900&display=swap")
OLD_FONT_URL = ("https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght"
                "@0,6..72,400..700;1,6..72,400..700&display=swap")


def sha(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode()).hexdigest()


def parse_css2(cssb):
    out = []
    for m in re.finditer(
            rb"/\* ([\w-]+) \*/\s*@font-face \{[^}]*?font-family: '([^']+)';"
            rb"[^}]*?font-style: (\w+);[^}]*?src: url\((https://[^)]+)\)",
            cssb, re.S):
        out.append((m.group(1).decode(), m.group(2).decode(),
                    m.group(3).decode(), m.group(4).decode()))
    return out


def fetch_latin_woff2(css_url, family):
    st, _, cssb = _sim.http_get(css_url)
    assert st == 200, f"css2 for {family}: {st}"
    faces = parse_css2(cssb)
    pick = [f for f in faces if f[0] == "latin" and f[1] == family
            and f[2] == "normal"]
    assert pick, f"no latin normal woff2 for {family}"
    st2, _, woff = _sim.http_get(pick[0][3])
    assert st2 == 200 and woff[:4] == b"wOF2"
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


walk_f4 = _fix.apply_walk_fixes(_bf.build_walk_free())
entry_f4 = _bf.build_free_entry()
walk = _fo.apply_item1_walk(walk_f4)
entry = _fo.apply_entry_followon(entry_f4)
assert sha(entry) == "e9462d8ee6fe3e45b4235bd7eb367dca658febcda42a0638eaad249dad86b814"
from fontTools.ttLib import TTFont
marc = TTFont(io.BytesIO(fetch_latin_woff2(NEW_FONT_URL, "Marcellus")))
news = TTFont(io.BytesIO(fetch_latin_woff2(OLD_FONT_URL, "Newsreader")))
print(f"Marcellus upm={marc['head'].unitsPerEm} glyphs={len(marc.getBestCmap())}")
print(f"Newsreader upm={news['head'].unitsPerEm} glyphs={len(news.getBestCmap())}")
samples = ["Shawn Vibert", "F4 Followon Test", "Alex Morgan",
           "Alexander Christopher Bennett"]
cases = [("desktop 1919w", 78.4, 920), ("635w", 54.4, 599), ("390w", 52.65, 354)]
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
name_line_635 = round(54.4 * 0.98)
name_line_390 = round(52.65 * 0.98)
content_635 = 72 + 15 + 30 + 20 + worst["635w"] * name_line_635 + 20 + 124 + 40 + 58 + 40 + 50
content_390 = 94 + 15 + 30 + 20 + worst["390w"] * name_line_390 + 20 + 130 + 40 + 58 + 40 + 50
print(f"budget 635x349: face 213px vs content ~{content_635}px "
      f"(worst {worst['635w']} name line(s)) -> scroll, ENTER in flow")
print(f"budget 390x844: face 708px vs content ~{content_390}px "
      f"(worst {worst['390w']} name line(s)) -> fits={content_390 < 708}")
# The italic serif line: 'This certifies that' at 1.22rem italic.
for txt in ["This certifies that"]:
    print(f"  certifies line {txt!r}: Marcellus {width_px(marc, txt, 19.52):.0f}px "
          f"vs Newsreader {width_px(news, txt, 19.52):.0f}px at 19.52px")
