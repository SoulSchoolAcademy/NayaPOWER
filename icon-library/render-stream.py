#!/usr/bin/env python3
"""Icon Library DATA build — streaming emitter (2026-11-19).
Renders all orbs in memory and streams them to stdout as:
  @@FILE <relpath> <nbytes> <sha256>
  <base64, single line>
The shell decode loop (not python) writes the files: python-process writes
EPERM / land 0 bytes in this VM's flake windows, while shell writes land.
Nothing in this script writes a file. icons.json sha256 values are computed
from the emitted bytes in memory.
"""
import sys, io, json, hashlib, base64, importlib.util
from PIL import Image, ImageDraw, ImageFont

spec = importlib.util.spec_from_file_location("render_orbs", "/home/hatch/workspace/icon-library/render-orbs.py")
ro = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ro)

LIB = "icon-library"  # relpaths emitted relative to ~/workspace/icon-library
OUT = sys.stdout

def emit(relpath, data: bytes):
    sha = hashlib.sha256(data).hexdigest()
    OUT.write(f"@@FILE {relpath} {len(data)} {sha}\n")
    OUT.write(base64.b64encode(data).decode() + "\n")
    OUT.flush()
    return sha

def png_bytes(img):
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def main():
    font_bytes = ro.fetch_font_bytes()
    print(f"@@NOTE font {len(font_bytes)} bytes", flush=True)
    try:
        ImageFont.truetype(io.BytesIO(font_bytes), 100).set_variation_by_axes([900])
        font_source = "Inter variable (google/fonts Inter[opsz,wght].ttf), weight 900 via set_variation_by_axes"
    except Exception as e:
        font_source = "FALLBACK DejaVu Sans Bold (Inter variation failed: %s)" % e
    letters = [chr(c) for c in range(ord('A'), ord('Z') + 1)]
    recs = {}
    keep512 = {}  # (letter,num) -> PIL image, for the contact sheet
    for S in (512, 192):
        for num in range(1, 8):
            base = ro.build_base(ro.GEM_COL[num], S)
            for letter in letters:
                lyr, src = ro.render_letter_layer(letter, S, font_bytes, font_source)
                if "FALLBACK" in src:
                    font_source = src
                img = base.copy()
                img.alpha_composite(lyr)
                data = png_bytes(img)
                rel = f"orbs/{S}/{letter}-{num}-{ro.NAMES[num]}.png"
                sha = emit(rel, data)
                rec = recs.setdefault((letter, num), {})
                rec[f"bytes{S}"] = len(data)
                rec[f"sha{S}"] = sha
                if S == 512 and ro.GEM_NUM[letter] == num:
                    keep512[(letter, num)] = img
                if S == 512 and (letter, num) in [('A', 2), ('M', 7), ('Z', 3), ('T', 1)]:
                    keep512[(letter, num)] = img
            print(f"@@NOTE size {S} colour {num} {ro.NAMES[num]} done", flush=True)

    emit(".font_source.txt", (font_source + "\n").encode())

    orbs = []
    for letter in letters:
        for num in range(1, 8):
            e = recs[(letter, num)]
            orbs.append({
                "id": f"orb-{letter}-{num}", "initial": letter,
                "gematria_number": num, "colour_name": ro.NAMES[num],
                "colour_hex": ro.GEM_COL[num],
                "canonical": ro.GEM_NUM[letter] == num,
                "file_512": f"orbs/512/{letter}-{num}-{ro.NAMES[num]}.png",
                "file_192": f"orbs/192/{letter}-{num}-{ro.NAMES[num]}.png",
                "bytes_512": e["bytes512"], "sha256_512": e["sha512"],
                "bytes_192": e["bytes192"], "sha256_192": e["sha192"],
            })
    logos = []
    for fname, size_px in [("naya-icon-512.png", 512), ("naya-icon-192.png", 192), ("apple-touch-icon.png", 180)]:
        with open(f"/home/hatch/workspace/user/files/icons/{fname}", "rb") as f:
            data = f.read()
        logos.append({"file": fname, "size_px": size_px, "bytes": len(data),
                      "sha256": hashlib.sha256(data).hexdigest(),
                      "source": f"~/workspace/user/files/icons/{fname}"})
    doc = {
        "library": "Naya Icon Library", "version": "1.0.0", "date": "2026-11-19",
        "gematria_number": ro.GEM_NUM, "gematria_colour": ro.GEM_COL,
        "colour_names": ro.NAMES,
        "orb_recipe": {
            "source": ".cx-ava from Personal mirror (branch personal/mirror-hub-20261119, blob 010dd56c) and Hub (blob 7a15413b), verbatim",
            "shape": "circle",
            "letter": {"colour": "#ffffff", "weight": 900, "size": "22px on a 58px orb (0.379 of diameter)",
                       "text_shadow": "0 1px 3px rgba(0,0,0,.6)",
                       "font": "inherited sans (Inter / system sans) — NOT Marcellus (no 900 weight; certificate script face)"},
            "body": "radial-gradient(circle at 32% 28%, rgba(255,255,255,.35) 0%, rgba(255,255,255,0) 42%) over radial-gradient(circle at 50% 50%, color-mix(in srgb, COLOUR 55%, #101014) 0%, color-mix(in srgb, COLOUR 28%, #060607) 78%)",
            "rim": "border 2px solid color-mix(in srgb, COLOUR 80%, white) (2px on 58px orb; scales with diameter)",
            "shadows": "box-shadow 0 0 24px -4px COLOUR, inset 0 2px 3px rgba(255,255,255,.25), inset 0 -6px 12px rgba(0,0,0,.45), 0 8px 20px rgba(0,0,0,.55); all lengths scale with orb diameter",
            "animation_note": "The live page has a spinning sheen ring (osOrbFlow, 7s). It is ANIMATION, not part of the static icon file, and is not drawn."
        },
        "notes": [
            "TAB vs ORB colour for 5: the Hub TAB-colour table uses bright cyan #29b6f6 for 5 (verified from the fix-9 digit-5 tile). That is the TAB colour, NOT the orb colour. Orbs use the deep table: 5 = #0f52ba sapphire. #29b6f6 appears in NO orb file.",
            "SQUARE-FILE ADAPTATION (coordinator's call): on the page the glow/drop-shadow extend ~0.4x the disc diameter beyond the disc. A square icon file cannot hold that proportionally, so disc diameter = 88% of canvas (450px in 512, 169px in 192), centred; border, highlight, body gradient, inset light/shade and letter at EXACT CSS proportions relative to the disc; outer glow and drop shadow scaled to fit the remaining margin (glow blur ~ margin x 0.6 fading to ~0 at canvas edge; drop-shadow offset ~ margin x 0.35, blur ~ margin x 0.5). Disc, rim, highlight, letter and colours are exact; only the atmospheric shadows are contained to the square. No sheen ring, no extra decoration.",
            "Font: " + font_source,
            "Canonical orb for an initial is the one whose colour number equals GEM_NUM[initial]."
        ],
        "orbs": orbs, "logos": logos,
    }
    emit("icons.json", json.dumps(doc, indent=2).encode())

    # --- contact sheet: 26 canonical (13x2) + 4 non-canonical samples (row 3) ---
    thumb, label_h, pad = 128, 26, 10
    cell = thumb + pad
    cols, rows = 13, 3
    W = cols * cell + pad
    H = rows * (thumb + label_h + pad) + pad
    sheet = Image.new("RGBA", (W, H), (10, 10, 15, 255))
    d = ImageDraw.Draw(sheet)
    try:
        lf = ImageFont.truetype(io.BytesIO(font_bytes), 20)
        lf.set_variation_by_axes([700])
    except Exception:
        lf = ImageFont.load_default()
    items = []
    for letter in letters:
        num = ro.GEM_NUM[letter]
        items.append((letter, num, True))
    for letter, num in [('A', 2), ('M', 7), ('Z', 3), ('T', 1)]:
        items.append((letter, num, False))
    for i, (letter, num, canon) in enumerate(items):
        r, c = divmod(i, cols)
        x = pad + c * cell
        y = pad + r * (thumb + label_h + pad)
        im = keep512[(letter, num)].resize((thumb, thumb), Image.LANCZOS)
        sheet.alpha_composite(im, (x, y))
        tag = f"{letter}-{num} {ro.NAMES[num]}" + (" ★" if canon else "")
        d.text((x + thumb / 2, y + thumb + 4), tag, font=lf, fill=(255, 255, 255, 255), anchor="ma")
    emit("contact-sheet.png", png_bytes(sheet))
    OUT.write("@@DONE\n")
    OUT.flush()
    print("@@NOTE all emitted", flush=True)

if __name__ == "__main__":
    main()
