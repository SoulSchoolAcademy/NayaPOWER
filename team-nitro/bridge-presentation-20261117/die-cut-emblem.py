#!/usr/bin/env python3
"""Die-cut the official emblem (NAYA_ICON.png) for the bridge corners.

PROBLEM (proven 2026-11-17 ~22:00Z): NAYA_ICON.png is RGBA but fully
opaque — its background is solid pure black (0,0,0,255) on every pixel
(alpha histogram: 0 transparent, 3,600,000 opaque). Rendered rotated
as a corner jewel, the black rectangle reads as a tilted black diamond
patch — "looks pasted, not die-cut". The 21:57Z emblem eye flagged
exactly this defect on the other round's corners.

FIX: flood-fill from the image borders through EXACTLY-black pixels
and make only those transparent. The artwork is untouched: its
506,445 enclosed pure-black pixels (dark interiors of the crown /
diamond / wings) and its near-black anti-aliased edges (RGB sums 1-5)
are preserved — a naive black-threshold would punch holes in them.
Measured: 2,712,718 exactly-black pixels (75.4%); 2,206,273
background-connected (61.3%) go transparent; 506,445 enclosed stay.

The artwork pixels are byte-identical to the source — this is a
die-cut (cutting the sticker from its sheet), not a redraw or
redesign. The verbatim original stays in KV as wbf-naya-emblem.png;
the die-cut goes to wbf-naya-emblem-cut.png.

Usage: python3 die-cut-emblem.py > /tmp/... (stdout = PNG bytes;
stats go to stderr). In this round it pipes straight into
kv-put-emblem-cut.py — no disk write anywhere (EPERM flake).
"""
import sys
from collections import deque
from PIL import Image

SRC = "/home/hatch/workspace/user/media_library/image/NAYA_ICON.png"

im = Image.open(SRC).convert("RGBA")
W, H = im.size
px = im.load()
seen = bytearray(W * H)
dq = deque()
for x in range(W):
    for y in (0, H - 1):
        if px[x, y][:3] == (0, 0, 0) and not seen[y * W + x]:
            seen[y * W + x] = 1
            dq.append((x, y))
for y in range(H):
    for x in (0, W - 1):
        if px[x, y][:3] == (0, 0, 0) and not seen[y * W + x]:
            seen[y * W + x] = 1
            dq.append((x, y))
while dq:
    x, y = dq.popleft()
    for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
        if 0 <= nx < W and 0 <= ny < H and not seen[ny * W + nx] and px[nx, ny][:3] == (0, 0, 0):
            seen[ny * W + nx] = 1
            dq.append((nx, ny))
nbg = sum(seen)
for i in range(W * H):
    if seen[i]:
        x, y = i % W, i // W
        r, g, b, _a = px[x, y]
        px[x, y] = (r, g, b, 0)
print(f"die-cut: {W}x{H} background-transparent={nbg} ({100*nbg/(W*H):.1f}%)", file=sys.stderr)
im.save(sys.stdout.buffer, format="PNG")
