#!/usr/bin/env python3
"""Coarse composition map of a deck slide image, from stdin bytes.

Downscales to a 48x27 grid; each cell is classified by brightness/hue:
  ' ' dark/black   '.' dim gray   'W' bright white   'G' green
  'B' blue         'P' purple/magenta   'Y' gold/yellow   'o' other color
The three orbs (PERSONAL green / BUSINESS blue / SPACE purple, glossy
bright circles on black) show as three round G/B/P clusters, usually
in the lower half. Control: slides 1 and 9 (known orb slides) should
show the three clusters; slides 2/3/7 (known non-orb) should not.
Usage: curl ... | python3 slide-map.py <label>
"""
import sys
from PIL import Image
import io

data = sys.stdin.buffer.read()
im = Image.open(io.BytesIO(data)).convert("RGB")
W, H = im.size
small = im.resize((48, 27))
print(f"{sys.argv[1]}: {W}x{H} {len(data)} B")
for y in range(27):
    row = ""
    for x in range(48):
        r, g, b = small.getpixel((x, y))
        mx, mn = max(r, g, b), min(r, g, b)
        if mx < 40:
            row += " "
        elif mx < 110 and mx - mn < 30:
            row += "."
        elif mx > 200 and mx - mn < 40:
            row += "W"
        elif g > r + 25 and g > b + 15:
            row += "G"
        elif b > r + 25 and b > g + 15:
            row += "B"
        elif r > 110 and b > 110 and g < r - 20:
            row += "P"
        elif r > 150 and g > 110 and b < 90:
            row += "Y"
        else:
            row += "o"
    print(row)
