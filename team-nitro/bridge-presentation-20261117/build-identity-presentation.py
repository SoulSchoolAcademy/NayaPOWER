#!/usr/bin/env python3
"""Bridge presentation fix round (2026-11-17) — identity file build.

Base: ../walk-v23-assembly-20261114/identity-fixed.html
Out:  identity-presentation.html (stdout; shell redirect does the write).
Anchored replacements with exact-occurrence checks; fails loudly.

(c) Certificate at 635px: the giant serif name overlaps the welcome-back
line, the membership sentence, the SMART LINK box and the SMART MAIL box.
The certified plaque is a grid whose head track is funded by a lean
ratio; desktop was fixed 0.78 -> 0.88 for exactly this overlap (ROUND 3c)
while "phone keeps the base 0.78 lean". At 635 the head content is
taller than at 390 (bigger name, wider lines), so the 0.74fr phone lean
starves the head track again. This round funds ONLY the 600-640 band
with the desktop lean — 390 keeps its proven 0.74fr untouched.

The crystal (logo-hero) and small N-mark (brand-mark) are embedded
data-URI JPEGs; both decode valid (512x512, sha f9c2290e). There is no
network image here to fail — no byte change for that half of (c); it is
a live-verification item (see MAKER-REPORT).
"""
import sys, hashlib

BASE = '/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/identity-fixed.html'
s = open(BASE, encoding='utf-8').read()
ORIG_LEN = len(s)
print(f'# base: {len(s)} chars, sha256 {hashlib.sha256(s.encode()).hexdigest()[:16]}', file=sys.stderr)

def rep(old, new, count=1, label=''):
    global s
    n = s.count(old)
    assert n == count, f'REP FAIL [{label}]: anchor occurs {n}x, expected {count}x :: {old[:90]!r}'
    s = s.replace(old, new)
    print(f'# rep ok [{label}]', file=sys.stderr)

# ------------------------------------------------- C1: fund the certified head at 600-640px
# The 640 block sets the phone lean; add a 600-640 override AFTER the
# short-height 640 blocks so it wins in that band at every height.
# confirm the phone lean anchor is present (it occurs twice: the 640
# block and a short-height 640 block share the rule).
assert s.count("      .cert-plaque.is-certified .identity-face { grid-template-rows: 0.74fr auto 1.26fr; }") == 2, 'C1: phone lean anchor missing'
print('# C1 phone lean present (2x)', file=sys.stderr)
# append the band override just before </style>, so it is the last word in
# the sheet and wins over every 640 block at every height in the band.
anchor = "  </style>"
assert s.count(anchor) == 1, 'C1: style-close anchor not found'
s = s.replace(anchor,
"""    /* BRIDGE PRESENTATION (2026-11-17, §7c) — at 600-640px the certified
       head content is taller than at 390 (bigger name, wider lines) and
       the 0.74fr phone lean starves the head track, so the in-flow name
       overlaps the welcome-back line, the membership sentence and the
       two boxes below it — the same overlap desktop fixed with lean
       0.88 (ROUND 3c). Fund this band with the desktop lean; 390 keeps
       its proven 0.74fr. */
    @media (min-width: 600px) and (max-width: 640px) {
      .cert-plaque.is-certified .identity-face { grid-template-rows: 0.88fr auto 1.12fr; }
    }
  </style>""")
print('# C1 ok: 600-640 certified lean 0.88fr', file=sys.stderr)

print(f'# done: {ORIG_LEN} -> {len(s)} chars, sha256 {hashlib.sha256(s.encode()).hexdigest()[:16]}', file=sys.stderr)
sys.stdout.write(s)
