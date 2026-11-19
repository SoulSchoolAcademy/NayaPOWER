#!/usr/bin/env python3
"""Verify the icon library (read-only): opens every PNG, checks dims/mode,
centre-pixel (letter-aware expected from the recipe, ±8), a pure body point,
letter bright-pixel count, corner transparency, absence of #29b6f6, and the
icons.json index (counts, existence, size+sha match). Prints a report.
"""
import sys, io, json, hashlib, math, os
import numpy as np
from PIL import Image
import importlib.util

spec = importlib.util.spec_from_file_location("render_orbs", "/home/hatch/workspace/icon-library/render-orbs.py")
ro = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ro)

LIB = "/home/hatch/workspace/icon-library"
GEM_NUM, GEM_COL, NAMES = ro.GEM_NUM, ro.GEM_COL, ro.NAMES
DARK = np.array([16.0, 16.0, 20.0])

def hx(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], dtype=float)

def expected_body(x, y, C, S):
    cx = cy = S / 2.0
    D = 0.88 * S
    R = D / 2.0
    u = D / 58.0
    r_px = math.hypot(x - cx, y - cy)
    t = min(max(r_px / R, 0.0), 1.0)
    p = (55.0 - 27.0 * (t / 0.78)) / 100.0 if t <= 0.78 else 0.28
    rgb = C * p + DARK * (1.0 - p)
    hl_cx, hl_cy = cx - 0.18 * D, cy - 0.22 * D
    R_far = D * math.hypot(0.68, 0.72)
    d_hl = math.hypot(x - hl_cx, y - hl_cy)
    hl_a = 0.35 * max(0.0, 1.0 - d_hl / (0.42 * R_far))
    rgb = rgb * (1.0 - hl_a) + 255.0 * hl_a
    d_top = y - (cy - R)
    top_a = 0.25 * math.exp(-((d_top - 2 * u) / (3 * u)) ** 2) if d_top >= 0 else 0.0
    rgb = rgb * (1.0 - top_a) + 255.0 * top_a
    d_bot = (cy + R) - y
    bot_a = 0.45 * math.exp(-((d_bot - 6 * u) / (12 * u)) ** 2) if d_bot >= 0 else 0.0
    rgb = rgb * (1.0 - bot_a)
    if R - 2 * u <= r_px <= R:
        rgb = 0.8 * C + 0.2 * 255.0
    return rgb

def main():
    font_bytes = ro.fetch_font_bytes()
    letters = [chr(c) for c in range(ord('A'), ord('Z') + 1)]
    fails, warns = [], []
    checked = 0
    worst_centre = (0, None)
    worst_body = (0, None)
    min_bright = {512: 10 ** 9, 192: 10 ** 9}
    cyan_hits = []
    for S in (512, 192):
        for num in range(1, 8):
            C = hx(GEM_COL[num])
            for letter in letters:
                rel = f"orbs/{S}/{letter}-{num}-{NAMES[num]}.png"
                path = os.path.join(LIB, rel)
                checked += 1
                try:
                    im = Image.open(path)
                    im.load()
                except Exception as e:
                    fails.append(f"{rel}: UNOPENABLE {e}")
                    continue
                if im.size != (S, S) or im.mode != "RGBA":
                    fails.append(f"{rel}: size/mode {im.size}/{im.mode}")
                if os.path.getsize(path) == 0:
                    fails.append(f"{rel}: 0 bytes")
                a = np.array(im)
                # corners: transparent or glow-only (alpha <= 10)
                for (cx0, cy0) in [(0, 0), (S - 1, 0), (0, S - 1), (S - 1, S - 1)]:
                    if a[cy0, cx0, 3] > 10:
                        fails.append(f"{rel}: corner ({cx0},{cy0}) alpha {a[cy0, cx0, 3]}")
                # no tab-cyan #29b6f6 anywhere
                if np.any((a[:, :, 0] == 41) & (a[:, :, 1] == 182) & (a[:, :, 2] == 246)):
                    cyan_hits.append(rel)
                # letter layer re-rendered for letter-aware centre expectation
                lyr, _ = ro.render_letter_layer(letter, S, font_bytes, "")
                la = np.array(lyr)
                cx = cy = S // 2
                body = expected_body(cx, cy, C, S)
                lr, lg, lb, lalpha = [float(v) for v in la[cy, cx]]
                la_f = lalpha / 255.0
                exp_c = np.array([lr, lg, lb]) * la_f + body * (1.0 - la_f)
                act_c = a[cy, cx, :3].astype(float)
                dc = float(np.max(np.abs(act_c - exp_c)))
                if dc > worst_centre[0]:
                    worst_centre = (dc, rel)
                if dc > 8:
                    fails.append(f"{rel}: centre pixel off by {dc:.1f} exp {np.round(exp_c,1)} act {act_c}")
                # pure body point below the letter: (cx, cy + 0.62R)
                R = 0.88 * S / 2.0
                bx, by = cx, int(round(cy + 0.62 * R))
                if la[by, bx, 3] > 5:
                    warns.append(f"{rel}: letter mask reaches body point (alpha {la[by, bx, 3]})")
                else:
                    exp_b = expected_body(bx, by, C, S)
                    act_b = a[by, bx, :3].astype(float)
                    db = float(np.max(np.abs(act_b - exp_b)))
                    if db > worst_body[0]:
                        worst_body = (db, rel)
                    if db > 8:
                        fails.append(f"{rel}: body point off by {db:.1f} exp {np.round(exp_b,1)} act {act_b}")
                # bright pixels in central letter box
                D = 0.88 * S
                x0, x1 = int(cx - 0.22 * D), int(cx + 0.22 * D)
                y0, y1 = int(cy - 0.22 * D), int(cy + 0.22 * D)
                box = a[y0:y1, x0:x1]
                bright = int(np.sum((box[:, :, 0] > 200) & (box[:, :, 1] > 200) & (box[:, :, 2] > 200) & (box[:, :, 3] > 200)))
                min_bright[S] = min(min_bright[S], bright)
                need = 800 if S == 512 else 100
                if bright < need:
                    fails.append(f"{rel}: bright letter pixels {bright} < {need}")
    print(f"PNG CHECK: {checked} files opened")
    print(f"worst centre-pixel deviation: {worst_centre[0]:.1f} ({worst_centre[1]})  tolerance ±8")
    print(f"worst body-point deviation: {worst_body[0]:.1f} ({worst_body[1]})  tolerance ±8")
    print(f"min bright letter pixels: 512->{min_bright[512]}  192->{min_bright[192]}")
    print(f"#29b6f6 exact-pixel hits: {len(cyan_hits)} {cyan_hits[:5]}")
    print(f"warnings: {len(warns)}")
    for w in warns[:10]:
        print("  WARN", w)

    # --- index check ---
    with open(os.path.join(LIB, "icons.json")) as f:
        doc = json.load(f)
    orbs, logos = doc["orbs"], doc["logos"]
    print(f"INDEX: {len(orbs)} orbs, {len(logos)} logos")
    if len(orbs) != 182:
        fails.append(f"index orb count {len(orbs)} != 182")
    if len(logos) != 3:
        fails.append(f"index logo count {len(logos)} != 3")
    canon = [o for o in orbs if o["canonical"]]
    print(f"INDEX: canonical orbs {len(canon)} (expect 26)")
    if len(canon) != 26:
        fails.append(f"canonical count {len(canon)} != 26")
    for o in orbs:
        for key, fkey, bkey, skey in [("file_512", "file_512", "bytes_512", "sha256_512"),
                                      ("file_192", "file_192", "bytes_192", "sha256_192")]:
            p = os.path.join(LIB, o[fkey])
            if not os.path.exists(p):
                fails.append(f"index {o['id']}: missing {o[fkey]}")
                continue
            if os.path.getsize(p) != o[bkey]:
                fails.append(f"index {o['id']}: size mismatch {o[fkey]}")
            h = hashlib.sha256(open(p, "rb").read()).hexdigest()
            if h != o[skey]:
                fails.append(f"index {o['id']}: sha mismatch {o[fkey]}")
        if o["colour_hex"] != GEM_COL[o["gematria_number"]]:
            fails.append(f"index {o['id']}: colour_hex wrong")
        if o["canonical"] != (GEM_NUM[o["initial"]] == o["gematria_number"]):
            fails.append(f"index {o['id']}: canonical flag wrong")
    for lg in logos:
        p = os.path.join(LIB, "logo", lg["file"])
        if not os.path.exists(p):
            fails.append(f"logo missing {lg['file']}")
            continue
        if os.path.getsize(p) != lg["bytes"]:
            fails.append(f"logo size mismatch {lg['file']}")
        h = hashlib.sha256(open(p, "rb").read()).hexdigest()
        if h != lg["sha256"]:
            fails.append(f"logo sha mismatch {lg['file']}")
    # logo hashes vs the harvested trio
    expect = {"naya-icon-192.png": "b84ac3a14d5c7babbfac8d9a3414cbf80ddc5f4f4774f2e37c3395e1297f1308",
              "naya-icon-512.png": "bb5728c0d075893ac6038c3a4081f20f7d878408bf3c5e354e7e6558f7213d58",
              "apple-touch-icon.png": "cb00859d0d1f167ec9cf460a30cb8b1a1d64df2006b2a556833fe7100db3cf5e"}
    for lg in logos:
        if expect.get(lg["file"]) != lg["sha256"]:
            fails.append(f"logo {lg['file']}: sha differs from harvested trio")
    # contact sheet + font source
    for extra in ["contact-sheet.png", ".font_source.txt"]:
        p = os.path.join(LIB, extra)
        print(f"{extra}: {'OK ' + str(os.path.getsize(p)) + ' B' if os.path.exists(p) and os.path.getsize(p) > 0 else 'MISSING/EMPTY'}")
        if not os.path.exists(p) or os.path.getsize(p) == 0:
            fails.append(f"{extra} missing/empty")
    print(f"FAILURES: {len(fails)}")
    for fl in fails:
        print("  FAIL", fl)
    print("VERIFY-VERDICT:", "PASS" if not fails else "GOES BACK")

if __name__ == "__main__":
    main()
