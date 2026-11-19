#!/usr/bin/env python3
"""Letter-mask exporter (read-only, no file writes): renders the 26 letter
layers (white glyph + blurred shadow, exact PIL/Inter code from render-orbs.py)
for 512 and 192, crops each to its non-transparent bbox, PNG-encodes the crop,
and prints ONE JSON object to stdout: {"512": {letter: {x,y,w,h,png_b64}}, ...}.
Node renders the orbs and composites these masks (Node can write files;
Python cannot in this VM)."""
import sys, io, json, base64, importlib.util
from PIL import Image
import numpy as np

spec = importlib.util.spec_from_file_location("render_orbs", "/home/hatch/workspace/icon-library/render-orbs.py")
ro = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ro)

def main():
    font_bytes = ro.fetch_font_bytes()
    try:
        from PIL import ImageFont
        ImageFont.truetype(io.BytesIO(font_bytes), 100).set_variation_by_axes([900])
        font_source = "Inter variable (google/fonts Inter[opsz,wght].ttf), weight 900 via set_variation_by_axes"
    except Exception as e:
        font_source = "FALLBACK DejaVu Sans Bold (Inter variation failed: %s)" % e
    out = {"font_source": font_source, "sizes": {}}
    letters = [chr(c) for c in range(ord('A'), ord('Z') + 1)]
    for S in (512, 192):
        d = {}
        for letter in letters:
            lyr, src = ro.render_letter_layer(letter, S, font_bytes, font_source)
            if "FALLBACK" in src:
                out["font_source"] = src
            a = np.array(lyr)
            ys, xs = np.where(a[:, :, 3] > 0)
            x0, x1 = int(xs.min()), int(xs.max())
            y0, y1 = int(ys.min()), int(ys.max())
            pad = 2
            x0 = max(0, x0 - pad); y0 = max(0, y0 - pad)
            x1 = min(S - 1, x1 + pad); y1 = min(S - 1, y1 + pad)
            crop = lyr.crop((x0, y0, x1 + 1, y1 + 1))
            buf = io.BytesIO()
            crop.save(buf, format="PNG")
            png = buf.getvalue()
            # alpha checksum for the Node decoder test
            asum = int(np.array(crop)[:, :, 3].astype(np.int64).sum())
            d[letter] = {"x": x0, "y": y0, "w": x1 + 1 - x0, "h": y1 + 1 - y0,
                         "png_b64": base64.b64encode(png).decode(),
                         "png_bytes": len(png), "alpha_sum": asum}
        out["sizes"][str(S)] = d
    sys.stdout.write(json.dumps(out))
    sys.stdout.flush()

if __name__ == "__main__":
    main()
