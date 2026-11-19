#!/usr/bin/env python3
"""Icon Library DATA build — orb renderer (2026-11-19).
Renders A-Z x 7 gematria colours at 512 and 192 from the harvested .cx-ava
recipe. Font fetched in-memory (never written to disk). Writes with retry +
size verification after every file (EPERM flake).
"""
import io, json, hashlib, math, os, sys, time, shutil
import urllib.request
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

LIB = "/home/hatch/workspace/icon-library"
GEM_NUM = {'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7,'H':6,'I':5,'J':4,'K':3,'L':2,
           'M':1,'N':1,'O':2,'P':3,'Q':4,'R':5,'S':6,'T':7,'U':6,'V':5,'W':4,'X':3,'Y':2,'Z':1}
GEM_COL = {1:'#c62828',2:'#c2410c',3:'#d4a017',4:'#07925f',5:'#0f52ba',6:'#3f51b5',7:'#8e24aa'}
NAMES = {1:'red',2:'orange',3:'gold',4:'emerald',5:'sapphire',6:'indigo',7:'royal-purple'}
DARK = np.array([16.0, 16.0, 20.0])  # #101014

def hx(h):
    return np.array([int(h[i:i+2], 16) for i in (1, 3, 5)], dtype=float)

def fetch_font_bytes():
    url = "https://raw.githubusercontent.com/google/fonts/main/ofl/inter/Inter%5Bopsz%2Cwght%5D.ttf"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"})
    data = urllib.request.urlopen(req, timeout=60).read()
    assert len(data) > 500000, f"font too small: {len(data)}"
    return data

def load_font(font_bytes, size):
    f = ImageFont.truetype(io.BytesIO(font_bytes), size)
    try:
        f.set_variation_by_axes([900])
        return f, "Inter variable wght 900"
    except Exception as e:
        print(f"  WARN set_variation_by_axes failed ({e}); trying static weight", flush=True)
        raise

def build_base(colour_hex, S):
    """Full disc+rim+glow+shadow for one colour/size, no letter. Returns PIL RGBA."""
    C = hx(colour_hex)
    cx = cy = S / 2.0
    D = 0.88 * S
    R = D / 2.0
    u = D / 58.0
    margin = (S - D) / 2.0
    yy, xx = np.mgrid[0:S, 0:S].astype(float)
    dx, dy = xx - cx, yy - cy
    r_px = np.sqrt(dx * dx + dy * dy)
    r = r_px / R

    # --- body radial gradient: mix55 at 0%, mix28 at 78%, hold after ---
    t = np.clip(r, 0.0, 1.0)
    p = np.where(t <= 0.78, 55.0 - 27.0 * (t / 0.78), 28.0) / 100.0
    body = C[None, None, :] * p[:, :, None] + DARK[None, None, :] * (1.0 - p[:, :, None])

    # --- highlight: radial at 32%/28%, white .35 -> 0 at 42% of farthest-corner radius ---
    hl_cx, hl_cy = cx - 0.18 * D, cy - 0.22 * D
    R_far = D * math.hypot(0.68, 0.72)
    d_hl = np.sqrt((xx - hl_cx) ** 2 + (yy - hl_cy) ** 2)
    hl_a = 0.35 * np.clip(1.0 - d_hl / (0.42 * R_far), 0.0, 1.0)
    rgb = body * (1.0 - hl_a[:, :, None]) + 255.0 * hl_a[:, :, None]

    # --- inset top light: inset 0 2px 3px rgba(255,255,255,.25) ---
    d_top = yy - (cy - R)
    top_a = 0.25 * np.exp(-((d_top - 2 * u) / (3 * u)) ** 2)
    top_a = np.where(d_top >= 0, top_a, 0.0)
    rgb = rgb * (1.0 - top_a[:, :, None]) + 255.0 * top_a[:, :, None]

    # --- inset bottom shade: inset 0 -6px 12px rgba(0,0,0,.45) ---
    d_bot = (cy + R) - yy
    bot_a = 0.45 * np.exp(-((d_bot - 6 * u) / (12 * u)) ** 2)
    bot_a = np.where(d_bot >= 0, bot_a, 0.0)
    rgb = rgb * (1.0 - bot_a[:, :, None])

    # --- rim: 2px solid mix(COLOUR 80%, white) ---
    rim_rgb = 0.8 * C + 0.2 * 255.0
    bw = 2 * u
    rim_band = (r_px >= R - bw) & (r_px <= R)
    rgb = np.where(rim_band[:, :, None], rim_rgb[None, None, :], rgb)

    # --- disc alpha with 1.5px antialiased edge ---
    edge = np.clip((R - r_px) / 1.5 + 0.5, 0.0, 1.0)

    # --- outer glow: 0 0 24px -4px COLOUR, contained to margin (blur ~ margin*0.6) ---
    glow_a = 0.55 * np.exp(-((r_px - R) / (margin * 0.6)) ** 2)
    glow_a = np.where(r_px > R, glow_a, 0.0)

    # --- drop shadow: 0 8px 20px rgba(0,0,0,.55), offset ~ margin*0.35, blur ~ margin*0.5 ---
    off = margin * 0.35
    d_sh = np.sqrt(dx ** 2 + (dy - off) ** 2)
    sh_a = 0.55 * np.where(d_sh <= R, 1.0, np.exp(-((d_sh - R) / (margin * 0.5)) ** 2))

    # --- composite bottom->top: shadow, glow, disc ---
    out_rgb = np.zeros((S, S, 3), dtype=float)
    out_a = np.zeros((S, S), dtype=float)
    def comp(src_rgb, src_a):
        nonlocal out_rgb, out_a
        sa = src_a[:, :, None]
        out_rgb = src_rgb * sa + out_rgb * (1.0 - sa)
        out_a = sa[:, :, 0] + out_a * (1.0 - sa[:, :, 0])
    comp(np.zeros((S, S, 3)), sh_a)                       # black shadow
    comp(np.tile(C, (S, S, 1)), glow_a)                    # coloured glow
    comp(rgb, edge)                                        # disc
    img = np.dstack([np.clip(out_rgb, 0, 255), np.clip(out_a, 0, 1) * 255.0])
    return Image.fromarray(img.astype(np.uint8), "RGBA")

def render_letter_layer(letter, S, font_bytes, font_source):
    D = 0.88 * S
    u = D / 58.0
    cx = cy = S / 2.0
    fsize = int(round(22.0 / 58.0 * D))
    try:
        font, _ = load_font(font_bytes, fsize)
        src = font_source
    except Exception:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", fsize)
        src = "FALLBACK DejaVu Sans Bold"
    layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    # shadow: black .6, offset 1u down, blur 3u
    sh = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(sh)
    d.text((cx, cy + 1 * u), letter, font=font, fill=(0, 0, 0, 153), anchor="mm")
    sh = sh.filter(ImageFilter.GaussianBlur(max(1.0, 3 * u)))
    layer.alpha_composite(sh)
    d = ImageDraw.Draw(layer)
    d.text((cx, cy), letter, font=font, fill=(255, 255, 255, 255), anchor="mm")
    return layer, src

def shell_write_bytes(data, path, tries=40):
    """Write bytes, rotating methods: the EPERM flake flips per-path per-moment
    and blocks python writes, shell writes, or both in a given window.
    Rotate (a) python open/write, (b) cat via child shell, (c) stage in /tmp
    via cat then cp. Verify size after every attempt."""
    import subprocess
    for i in range(tries):
        try:
            m = i % 3
            if m == 0:
                with open(path, "wb") as f:
                    f.write(data)
            elif m == 1:
                p = subprocess.run(["sh", "-c", 'cat > "$1"', "sh", path],
                                   input=data, timeout=30)
                if p.returncode != 0:
                    raise IOError(f"cat exit {p.returncode}")
            else:
                stage = "/tmp/orb-stage-%d.bin" % os.getpid()
                p = subprocess.run(["sh", "-c", 'cat > "$1"', "sh", stage],
                                   input=data, timeout=30)
                if p.returncode != 0:
                    raise IOError(f"stage cat exit {p.returncode}")
                p = subprocess.run(["cp", stage, path], timeout=30)
                if p.returncode != 0:
                    raise IOError(f"cp exit {p.returncode}")
            if os.path.getsize(path) == len(data) and len(data) > 0:
                return len(data)
        except Exception:
            pass
        time.sleep(2)
    raise IOError(f"could not write {path} after {tries} tries")

def save_verified(img, path, tries=40):
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    data = buf.getvalue()
    shell_write_bytes(data, path, tries=tries)
    with Image.open(path) as im:
        im.load()
    return len(data)

def existing_ok(path, S):
    try:
        if os.path.getsize(path) == 0:
            return False
        with Image.open(path) as im:
            im.load()
            return im.size == (S, S) and im.mode == "RGBA"
    except Exception:
        return False

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    print("fetching Inter variable font ...", flush=True)
    font_bytes = fetch_font_bytes()
    print(f"font OK: {len(font_bytes)} bytes", flush=True)
    font_source = "Inter variable (google/fonts Inter[opsz,wght].ttf), weight 900 via set_variation_by_axes"
    # probe variation support once
    try:
        ImageFont.truetype(io.BytesIO(font_bytes), 100).set_variation_by_axes([900])
    except Exception as e:
        print(f"VARIATION PROBE FAILED: {e} — will fall back per-letter", flush=True)
        font_source = "FALLBACK DejaVu Sans Bold (Inter variation failed: %s)" % e

    letters = [chr(c) for c in range(ord('A'), ord('Z') + 1)]
    recs = {}  # (letter, num) -> {bytes512, sha512, bytes192, sha192}
    used_source = font_source
    for S in (512, 192):
        for num in range(1, 8):
            col = GEM_COL[num]
            base = build_base(col, S)
            for letter in letters:
                name = f"{letter}-{num}-{NAMES[num]}.png"
                path = os.path.join(LIB, "orbs", str(S), name)
                if existing_ok(path, S):
                    rec = recs.setdefault((letter, num), {})
                    rec[f"bytes{S}"] = os.path.getsize(path)
                    rec[f"sha{S}"] = sha256_file(path)
                    continue
                lyr, src = render_letter_layer(letter, S, font_bytes, font_source)
                if "FALLBACK" in src:
                    used_source = src
                img = base.copy()
                img.alpha_composite(lyr)
                sz = save_verified(img, path)
                rec = recs.setdefault((letter, num), {})
                rec[f"bytes{S}"] = sz
                rec[f"sha{S}"] = sha256_file(path)
            print(f"  size {S} colour {num} {NAMES[num]} done", flush=True)
    print(f"orbs rendered: {len(recs)} x 2 sizes", flush=True)
    print("FONT SOURCE USED:", used_source, flush=True)
    shell_write_bytes((used_source + "\n").encode(), os.path.join(LIB, ".font_source.txt"))

    # --- logos: byte-identical copies (via cp: python writes EPERM in flake) ---
    import subprocess
    logos = []
    for fname, size_px in [("naya-icon-512.png", 512), ("naya-icon-192.png", 192), ("apple-touch-icon.png", 180)]:
        src = os.path.join("/home/hatch/workspace/user/files/icons", fname)
        dst = os.path.join(LIB, "logo", fname)
        ok = False
        for attempt in range(12):
            p = subprocess.run(["cp", src, dst])
            if p.returncode == 0 and os.path.getsize(dst) == os.path.getsize(src) and sha256_file(dst) == sha256_file(src):
                ok = True
                break
            time.sleep(1.5)
        assert ok, f"logo copy failed {fname}"
        logos.append({"file": fname, "size_px": size_px, "bytes": os.path.getsize(dst),
                      "sha256": sha256_file(dst), "source": src})
        print(f"logo copied: {fname} {os.path.getsize(dst)} B sha256 ok", flush=True)

    # --- icons.json ---
    orbs = []
    for letter in letters:
        for num in range(1, 8):
            e = recs[(letter, num)]
            orbs.append({
                "id": f"orb-{letter}-{num}",
                "initial": letter,
                "gematria_number": num,
                "colour_name": NAMES[num],
                "colour_hex": GEM_COL[num],
                "canonical": GEM_NUM[letter] == num,
                "file_512": f"orbs/512/{letter}-{num}-{NAMES[num]}.png",
                "file_192": f"orbs/192/{letter}-{num}-{NAMES[num]}.png",
                "bytes_512": e["bytes512"], "sha256_512": e["sha512"],
                "bytes_192": e["bytes192"], "sha256_192": e["sha192"],
            })
    doc = {
        "library": "Naya Icon Library",
        "version": "1.0.0",
        "date": "2026-11-19",
        "gematria_number": GEM_NUM,
        "gematria_colour": GEM_COL,
        "colour_names": NAMES,
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
            "Font: " + used_source,
            "Canonical orb for an initial is the one whose colour number equals GEM_NUM[initial]."
        ],
        "orbs": orbs,
        "logos": logos,
    }
    idx_path = os.path.join(LIB, "icons.json")
    idx_bytes = json.dumps(doc, indent=2).encode()
    shell_write_bytes(idx_bytes, idx_path)
    print(f"icons.json written: {os.path.getsize(idx_path)} B, {len(orbs)} orbs, {len(logos)} logos", flush=True)

if __name__ == "__main__":
    main()
