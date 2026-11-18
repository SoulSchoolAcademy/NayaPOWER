#!/usr/bin/env python3
"""Bridge presentation fix round (2026-11-17) — walk file build.

Base: ../walk-v23-assembly-20261114/walk-beginning-fixed.html
Out:  walk-presentation.html (stdout; shell redirect does the write).
Anchored replacements with exact-occurrence checks; fails loudly.
"""
import sys, hashlib

BASE = '/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/walk-beginning-fixed.html'
s = open(BASE, encoding='utf-8').read()
ORIG_LEN = len(s)
print(f'# base: {len(s)} chars, sha256 {hashlib.sha256(s.encode()).hexdigest()[:16]}', file=sys.stderr)

def rep(old, new, count=1, label=''):
    global s
    n = s.count(old)
    assert n == count, f'REP FAIL [{label}]: anchor occurs {n}x, expected {count}x :: {old[:90]!r}'
    s = s.replace(old, new)
    print(f'# rep ok [{label}]', file=sys.stderr)

# ------------------------------------------------- K1: Full Custom eye stays beside EDIT (Amendment #2e)
# .p3-choice-eye is display:flex (block-level), so inside the inline
# .p3-custom-btns span it dropped to its own line, under EDIT.
rep(".p3-custom-q .p3-choice-eye{vertical-align:middle;margin-left:6px;border-color:#ffbf3d}",
    ".p3-custom-q .p3-choice-eye{display:inline-flex;vertical-align:middle;margin-left:6px;border-color:#ffbf3d}",
    1, 'K1 eye inline-flex')
# the row itself: text and buttons never split the buttons apart.
rep(".p3-custom-btns{white-space:nowrap}",
    ".p3-custom-btns{white-space:nowrap;display:inline-flex;align-items:center;gap:6px}",
    1, 'K1 btns flex')

# ------------------------------------------------- K2: doubled quotes off every heading (Amendment #2e)
# Every .p3-question heading wears one pair of straight quotes in the
# markup; the eye reads them as doubled on every heading. A heading
# should not wear quotes at all — strip the pair (punctuation only, no
# words change). 18 headings: 14 questions + names + building + error +
# certificate.
import re
heads = re.findall(r'<h1 class="p3-question">"([^<]*)"</h1>', s)
assert len(heads) == 18, f'K2: expected 18 quoted headings, found {len(heads)}'
s2 = re.sub(r'<h1 class="p3-question">"([^<]*)"</h1>', r'<h1 class="p3-question">\1</h1>', s)
assert s2.count('<h1 class="p3-question">"') == 0, 'K2: quotes remain'
assert s2.count('<h1 class="p3-question">') == 18, 'K2: heading count changed'
s = s2
print(f'# K2 ok: quotes stripped from 18 headings', file=sys.stderr)

# ------------------------------------------------- K3: name screen hides the corner crests (Amendment #2d)
# The viewport-fixed crest medals cover form text as the names form
# scrolls at 635px. Mirror the end slide's p3-end-on precedent: a body
# class while the names step (n=14) is showing, crests hidden under it.
rep("body.p3-end-on .p3-crest{display:none}",
    "body.p3-end-on .p3-crest{display:none}\nbody.p3-names-on .p3-crest{display:none}",
    1, 'K3 names css')
rep("  cur = n;\n  STEPS.forEach(function(s, i){ s.hidden = (i !== n); });",
    "  cur = n;\n  document.body.classList.toggle('p3-names-on', n === 14);\n  STEPS.forEach(function(s, i){ s.hidden = (i !== n); });",
    1, 'K3 names toggle')

# ------------------------------------------------- K4: the walk offers VISUAL and READ (Amendment #2a)
# The end slide (congratulations) never offered the bridge's two views.
# Two choices beside the Hub / package buttons, linking to the front
# door's stage with ?stage= (the welcome file honours it this round).
anchor = """<a class="p3-enter" id="hubBtn" href="https://nayanet.app/hub" style="text-decoration:none">Step into your Hub &#9670;</a>
<button class="p3-enter" id="pricingBtn" type="button">Choose your package</button>
<div class="p3-foot">"""
assert s.count(anchor) == 1, 'K4: end-slide buttons anchor not found'
s = s.replace(anchor,
"""<a class="p3-enter" id="hubBtn" href="https://nayanet.app/hub" style="text-decoration:none">Step into your Hub &#9670;</a>
<button class="p3-enter" id="pricingBtn" type="button">Choose your package</button>
<div class="p3-end-views"><a class="p3-enter p3-end-view" href="/?stage=deck">Begin the visual story &#9670;</a><a class="p3-enter p3-end-view" href="/?stage=letter">Read the Collective Agreement &#9670;</a></div>
<div class="p3-foot">""")
print('# K4 ok: end-slide VISUAL/READ choices', file=sys.stderr)
# their row: two buttons side by side, wrapping under each other at 635.
rep(".p3-note{font-size:16px;color:#fff;opacity:1}",
    ".p3-note{font-size:16px;color:#fff;opacity:1}\n.p3-end-views{display:flex;flex-wrap:wrap;gap:12px;justify-content:center;margin:16px auto 0;max-width:860px}\n.p3-end-views .p3-end-view{flex:1 1 280px;text-align:center;text-decoration:none}",
    1, 'K4 views css')

print(f'# done: {ORIG_LEN} -> {len(s)} chars, sha256 {hashlib.sha256(s.encode()).hexdigest()[:16]}', file=sys.stderr)
sys.stdout.write(s)
