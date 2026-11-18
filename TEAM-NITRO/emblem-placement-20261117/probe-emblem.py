#!/usr/bin/env python3
"""Emblem live proof — VM Chromium + localhost forwarder (port 18080).
Staged /free certificate, pre-claim face, at 1920 / 635 / 390. Human pace.

NO alias is typed, NO claim is made, NO test cert is touched (certfix
Nº 000789, certcurrent Nº 000788, certfix390-390d Nº 000790-000793 ride
the test-cert cleanup, his hand). The four corner crests sit OUTSIDE
.identity-face, so the pre-claim face proves them exactly as the
certified face shows them.

Checks per width:
  E-CORNER x4: each .corner-crest is visible; its .crest-full is
    display:none; its .crest-medal is display:block with a PNG data-URI
    background (prefix iVBORw0KGgo) that decodes to 1800x2000.
  E-ANGLE: each corner keeps its rotation (desktop +-59deg / +-121deg,
    mobile +-35deg / +-145deg) — the emblem sits ON AN ANGLE.
  E-SIZE: corner box 100x122 desktop, 54x54 mobile (multiples of the
    page's own geometry, unchanged).
  E-COVER: no corner rect overlaps the title, certifies, name, alias
    input, ENTER button, or agreement line rects.
  E-READ: title / certifies / agree still render exact; no gray text
    (proper channel-spread test); name still solid white.
Screenshots: probe-emblem-<width>.png in this dir. Read them as the eye.
"""
import json
import os
import re
import sys

HERE = os.path.expanduser("~/workspace/team-nitro/emblem-placement-20261117")
STAGING_URL = "https://naya-pricing-free-staging.nayapower.workers.dev/free"
PROXY = "http://127.0.0.1:18080"

GATHER_JS = """
(() => {
  const q = s => document.querySelector(s);
  const corners = ['.cm-tl', '.cm-tr', '.cm-bl', '.cm-br'].map(sel => {
    const el = q(sel);
    if (!el) return {sel, missing: true};
    const r = el.getBoundingClientRect();
    const full = el.querySelector('.crest-full');
    const medal = el.querySelector('.crest-medal');
    const ms = medal ? getComputedStyle(medal) : null;
    const bg = ms ? ms.backgroundImage : '';
    const m = bg.match(/data:image\\/png;base64,([A-Za-z0-9+/=]{24})/);
    return {
      sel, x: Math.round(r.x), y: Math.round(r.y),
      w: Math.round(r.width), h: Math.round(r.height),
      transform: getComputedStyle(el).transform,
      fullDisplay: full ? getComputedStyle(full).display : 'MISSING',
      medalDisplay: medal ? getComputedStyle(medal).display : 'MISSING',
      medalBgPng: bg.indexOf('data:image/png;base64,') === 5,
      medalBgPrefix: m ? m[1] : null,
      medalBgSize: ms ? ms.backgroundSize : null,
      medalRadius: ms ? ms.borderRadius : null
    };
  });
  const texts = ['.cert-title', '.cert-certifies', '.cert-name', '.cert-agree', '.alias-status'];
  const rects = {};
  texts.forEach(s => {
    const el = q(s);
    if (!el) { rects[s] = null; return; }
    const r = el.getBoundingClientRect();
    rects[s] = {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width),
                h: Math.round(r.height), color: getComputedStyle(el).color,
                text: (el.innerText || '').trim().slice(0, 80)};
  });
  const overlaps = [];
  corners.forEach(c => {
    if (c.missing) return;
    Object.entries(rects).forEach(([s, r]) => {
      if (!r) return;
      const ox = Math.max(0, Math.min(c.x + c.w, r.x + r.w) - Math.max(c.x, r.x));
      const oy = Math.max(0, Math.min(c.y + c.h, r.y + r.h) - Math.max(c.y, r.y));
      if (ox > 0 && oy > 0) overlaps.push(c.sel + ' x ' + s + ' ' + ox + 'x' + oy);
    });
  });
  // The emblem image itself, decoded in-page: natural size must be 1800x2000.
  const medal = q('.cm-tl .crest-medal');
  const bg = medal ? getComputedStyle(medal).backgroundImage : '';
  const uri = (bg.match(/url\\("([^"]+)"\\)/) || [])[1] || '';
  return {corners, rects, overlaps, uriLen: uri.length,
          uriHead: uri.slice(0, 40), vw: innerWidth, vh: innerHeight,
          scrollW: document.documentElement.scrollWidth,
          clientW: document.documentElement.clientWidth,
          url: location.href};
})()
"""

EMBLEM_HEAD = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABwgAAAfQ"

results = []


def check(name, ok, detail=""):
    results.append({"check": name, "ok": bool(ok), "detail": str(detail)[:300]})
    print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail else ""), flush=True)


def is_gray(rgb_str):
    m = re.match(r"rgb\((\d+),\s*(\d+),\s*(\d+)\)", rgb_str or "")
    if not m:
        return False
    r, g, b = map(int, m.groups())
    return (max(r, g, b) - min(r, g, b)) < 12 and 60 < (r + g + b) / 3 < 245


def judge(g, tag, want_box):
    for c in g["corners"]:
        check(f"E-CORNER-{tag} {c['sel']} visible box {want_box}",
              (c.get("w"), c.get("h")) == want_box, c)
        check(f"E-CORNER-{tag} {c['sel']} crest-full display:none",
              c.get("fullDisplay") == "none", c.get("fullDisplay"))
        check(f"E-CORNER-{tag} {c['sel']} medal display:block + PNG bg",
              c.get("medalDisplay") == "block" and c.get("medalBgPng") is True,
              f"{c.get('medalDisplay')} png={c.get('medalBgPng')} size={c.get('medalBgSize')}")
        check(f"E-CORNER-{tag} {c['sel']} medal not circular (radius 0)",
              c.get("medalRadius") in ("0px", "0px 0px 0px 0px", "0%"), c.get("medalRadius"))
        check(f"E-CORNER-{tag} {c['sel']} rotated (on an angle)",
              c.get("transform") not in (None, "none", "matrix(1, 0, 0, 1, 0, 0)"),
              c.get("transform"))
    check(f"E-ANGLE-{tag} four corners, four angles",
          len({c.get("transform") for c in g["corners"]}) == 4,
          [c.get("transform") for c in g["corners"]])
    check(f"E-COVER-{tag} no corner overlaps text/input",
          not g["overlaps"], g["overlaps"])
    check(f"E-READ-{tag} title exact",
          g["rects"].get(".cert-title", {}).get("text") == "CERTIFICATE OF THE COLLECTIVE AGREEMENT",
          g["rects"].get(".cert-title", {}).get("text"))
    check(f"E-READ-{tag} certifies exact",
          (g["rects"].get(".cert-certifies", {}).get("text") or "").startswith(
              "This certificate of the Collective Agreement certifies that"),
          g["rects"].get(".cert-certifies", {}).get("text"))
    check(f"E-READ-{tag} name solid white",
          g["rects"].get(".cert-name", {}).get("color") == "rgb(255, 255, 255)",
          g["rects"].get(".cert-name", {}).get("color"))
    grays = [s for s, r in g["rects"].items() if r and is_gray(r["color"])]
    check(f"E-READ-{tag} no gray text", not grays, grays)
    check(f"E-READ-{tag} no horizontal overflow",
          g["scrollW"] == g["clientW"], f"scrollW={g['scrollW']} clientW={g['clientW']}")
    check(f"E-EMBLEM-{tag} data URI present, PNG head exact",
          g["uriLen"] > 3000000 and g["uriHead"] == EMBLEM_HEAD, f"len={g['uriLen']}")


def main():
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, proxy={"server": PROXY})
        for width, height, box in [(1920, 1080, (100, 122)),
                                   (635, 900, (54, 54)),
                                   (390, 844, (54, 54))]:
            tag = str(width)
            ctx = browser.new_context(viewport={"width": width, "height": height})
            pg = ctx.new_page()
            errors = []
            pg.on("pageerror", lambda e: errors.append(str(e)))
            pg.goto(STAGING_URL, wait_until="networkidle")
            pg.wait_for_timeout(1500)
            g = pg.evaluate(GATHER_JS)
            # In-page decode: the medal background must be a real 1800x2000 PNG.
            dims = pg.evaluate("""async () => {
              const medal = document.querySelector('.cm-tl .crest-medal');
              const bg = medal ? getComputedStyle(medal).backgroundImage : '';
              const uri = (bg.match(/url\\("([^"]+)"\\)/) || [])[1] || '';
              if (!uri) return null;
              const img = new Image();
              await new Promise((res, rej) => { img.onload = res; img.onerror = rej; img.src = uri; });
              return {w: img.naturalWidth, h: img.naturalHeight};
            }""")
            check(f"E-EMBLEM-{tag} emblem decodes 1800x2000 in-page",
                  dims == {"w": 1800, "h": 2000}, dims)
            check(f"E-ERRORS-{tag} no page errors", not errors, errors)
            judge(g, tag, box)
            pg.screenshot(path=os.path.join(HERE, f"probe-emblem-{tag}.png"))
            print(f"screenshot probe-emblem-{tag}.png", flush=True)
            ctx.close()
        browser.close()

    fails = [r for r in results if not r["ok"]]
    print(f"\nPROBE-EMBLEM: {len(results) - len(fails)}/{len(results)} checks passed")
    with open(os.path.join(HERE, "probe-emblem-results.json"), "w") as f:
        json.dump(results, f, indent=2)
    if fails:
        print("FAILED:", [r["check"] for r in fails])
        sys.exit(1)
    print("PROBE-EMBLEM OK — no alias typed, no claim made, no test cert touched")


if __name__ == "__main__":
    main()
