#!/usr/bin/env python3
"""Emblem corners fix — live proof. VM Chromium + localhost forwarder (port 18080).
Staged /free certificate, pre-claim face, at 1920x999 / 635x390 / 390x844.
Human pace. Cloud-browser route if the VM browsers are still dead.

NO alias is typed, NO claim is made, NO test cert is touched (certfix
Nº 000789, certcurrent Nº 000788, certfix390-390d Nº 000790-000793 ride
the test-cert cleanup, his hand). The four corner crests sit OUTSIDE
.identity-face, so the pre-claim face proves them exactly as the
certified face shows them.

Checks per width (the eye's exact defects, one by one):
  C-WHOLE x4: each .corner-crest's rotated bounding rect is fully inside
    the viewport (x >= 0, y >= 0, right <= vw, bottom <= vh) — the
    clipping defect, fixed by the 112px / 56px centers.
  C-CUT: the #crestCut SVG filter defs exist (x1); each .crest-medal's
    computed filter contains url(#crestCut) — the die-cut, on both
    desktop and mobile rules. (Whether any square edge still READS is
    the eye's judgment from the screenshots, not a computed check.)
  C-SIZE: corner box 132x161 desktop, 64x64 mobile — the bigger emblem
    (the surround / teardrop legibility fix).
  C-ANGLE: each corner keeps its rotation (desktop +-59deg / +-121deg,
    mobile +-35deg / +-145deg) — the emblem sits ON AN ANGLE.
  C-COVER: no corner rect overlaps the title, certifies, name, alias
    input, ENTER button, or agreement line rects. (Box rects overstate
    the rotated emblem — a touch here is the eye's call, not a fail
    by itself; the die-cut leaves most of the box transparent.)
  C-READ: title / certifies / agree still render exact; no gray text
    (proper channel-spread test); name still solid white.
Screenshots: probe-corners-<width>.png in this dir. Read them as the eye:
the corners whole, no diamond edge, the surround readable, the center
seal untouched.
"""
import json
import os
import re
import sys

HERE = os.path.expanduser("~/workspace/team-nitro/emblem-corners-fix-20261117")
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
      ow: el.offsetWidth, oh: el.offsetHeight,
      right: Math.round(r.right), bottom: Math.round(r.bottom),
      transform: getComputedStyle(el).transform,
      fullDisplay: full ? getComputedStyle(full).display : 'MISSING',
      medalDisplay: medal ? getComputedStyle(medal).display : 'MISSING',
      medalFilter: ms ? ms.filter : null,
      medalBgPng: bg.indexOf('data:image/png;base64,') === 5,
      medalBgPrefix: m ? m[1] : null,
      medalBgSize: ms ? ms.backgroundSize : null,
      medalRadius: ms ? ms.borderRadius : null
    };
  });
  const texts = ['.cert-title', '.cert-certifies', '.cert-name', '.cert-agree', '.cert-benefit', '.cert-privacy', '.alias-status'];
  const rects = {};
  texts.forEach(s => {
    // Some selectors match a hidden copy first (zero rect) — take the
    // first with a real rect, falling back to the first match (the name
    // echo is empty pre-claim and has a zero-height rect).
    const cands = [...document.querySelectorAll(s)];
    const el = cands.find(e => e.getBoundingClientRect().height > 0) || cands[0];
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
  const medal = q('.cm-tl .crest-medal');
  const bg = medal ? getComputedStyle(medal).backgroundImage : '';
  const uri = (bg.match(/url\\("([^"]+)"\\)/) || [])[1] || '';
  const cut = document.querySelector('#crestCut');
  const seal = q('.cert-seal .logo-hero');
  return {corners, rects, overlaps, uriLen: uri.length,
          uriHead: uri.slice(0, 54), vw: innerWidth, vh: innerHeight,
          scrollW: document.documentElement.scrollWidth,
          clientW: document.documentElement.clientWidth,
          crestCutPresent: !!cut,
          sealPresent: !!seal,
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


def judge(g, g2, tag, want_box):
    # Top corners are judged at scroll 0 (g); bottom corners after the
    # plaque is scrolled to its bottom (g2) — at 635x390 the plaque
    # scrolls, so the bottom pair only enters the viewport down there.
    # At 1920 / 390 the plaque does not scroll and g2 == g.
    src = {}
    for c in g["corners"]:
        if c["sel"] in (".cm-tl", ".cm-tr"):
            src[c["sel"]] = (c, g)
    for c in g2["corners"]:
        if c["sel"] in (".cm-bl", ".cm-br"):
            src[c["sel"]] = (c, g2)
    for sel, (c, gg) in src.items():
        check(f"C-SIZE-{tag} {c['sel']} layout box {want_box} (offsetWidth/Height — the rect is the rotated bbox)",
              (c.get("ow"), c.get("oh")) == want_box, f"ow={c.get('ow')} oh={c.get('oh')} rect={c.get('w')}x{c.get('h')}")
        check(f"C-WHOLE-{tag} {c['sel']} fully inside viewport",
              c.get("x", -1) >= 0 and c.get("y", -1) >= 0
              and c.get("right", 9999) <= gg["vw"] and c.get("bottom", 9999) <= gg["vh"],
              f"x={c.get('x')} y={c.get('y')} right={c.get('right')} bottom={c.get('bottom')} vw={gg['vw']} vh={gg['vh']}")
        check(f"C-CUT-{tag} {c['sel']} medal filter carries url(#crestCut)",
              c.get("medalFilter") is not None and "url(#crestCut)" in c.get("medalFilter")
              or (c.get("medalFilter") or "").startswith("url(\"#crestCut\")"),
              c.get("medalFilter"))
        check(f"C-CORNER-{tag} {c['sel']} crest-full display:none",
              c.get("fullDisplay") == "none", c.get("fullDisplay"))
        check(f"C-CORNER-{tag} {c['sel']} medal display:block + PNG bg",
              c.get("medalDisplay") == "block" and c.get("medalBgPng") is True,
              f"{c.get('medalDisplay')} png={c.get('medalBgPng')} size={c.get('medalBgSize')}")
        check(f"C-CORNER-{tag} {c['sel']} medal not circular (radius 0)",
              c.get("medalRadius") in ("0px", "0px 0px 0px 0px", "0%"), c.get("medalRadius"))
        check(f"C-CORNER-{tag} {c['sel']} rotated (on an angle)",
              c.get("transform") not in (None, "none", "matrix(1, 0, 0, 1, 0, 0)"),
              c.get("transform"))
    check(f"C-ANGLE-{tag} four corners, four angles",
          len({c.get("transform") for c in g["corners"]}) == 4,
          [c.get("transform") for c in g["corners"]])
    check(f"C-CUT-{tag} #crestCut defs present in the document",
          g.get("crestCutPresent") is True, g.get("crestCutPresent"))
    check(f"C-SEAL-{tag} center crystal-N seal still present",
          g.get("sealPresent") is True, g.get("sealPresent"))
    both_overlaps = (g["overlaps"] or []) + (g2["overlaps"] or [])
    check(f"C-COVER-{tag} no corner overlaps text/input (scroll 0 + scrolled to bottom)",
          not both_overlaps, both_overlaps)
    check(f"C-READ-{tag} title exact",
          (g["rects"].get(".cert-title") or {}).get("text") == "CERTIFICATE OF THE COLLECTIVE AGREEMENT",
          (g["rects"].get(".cert-title") or {}).get("text"))
    check(f"C-READ-{tag} certifies exact",
          ((g["rects"].get(".cert-certifies") or {}).get("text") or "").startswith(
              "This certificate of the Collective Agreement certifies that"),
          (g["rects"].get(".cert-certifies") or {}).get("text"))
    check(f"C-READ-{tag} name solid white",
          (g["rects"].get(".cert-name") or {}).get("color") == "rgb(255, 255, 255)",
          (g["rects"].get(".cert-name") or {}).get("color"))
    grays = [s for s, r in g["rects"].items() if r and is_gray(r["color"])]
    check(f"C-READ-{tag} no gray text", not grays, grays)
    check(f"C-READ-{tag} no horizontal overflow",
          g["scrollW"] == g["clientW"], f"scrollW={g['scrollW']} clientW={g['clientW']}")
    check(f"C-EMBLEM-{tag} data URI present, PNG head exact",
          g["uriLen"] > 3000000 and g["uriHead"] == EMBLEM_HEAD, f"len={g['uriLen']}")


def main():
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, proxy={"server": PROXY})
        for width, height, box in [(1920, 999, (132, 161)),
                                   (635, 390, (64, 64)),
                                   (390, 844, (64, 64))]:
            tag = str(width)
            ctx = browser.new_context(viewport={"width": width, "height": height})
            pg = ctx.new_page()
            errors = []
            pg.on("pageerror", lambda e: errors.append(str(e)))
            pg.goto(STAGING_URL, wait_until="networkidle")
            pg.wait_for_timeout(1500)
            g = pg.evaluate(GATHER_JS)
            # Second gather with the page scrolled to its bottom, so the
            # bottom pair is judged where it actually sits when the page
            # scrolls (635x390 — the DOCUMENT scrolls there, not the
            # plaque: the plaque barely overflows, the body does);
            # at 1920 / 390 this is a no-op.
            pg.evaluate("""() => {
              window.scrollTo(0, document.documentElement.scrollHeight);
            }""")
            pg.wait_for_timeout(500)
            g2 = pg.evaluate(GATHER_JS)
            pg.screenshot(path=os.path.join(HERE, f"probe-corners-{tag}-bottom.png"))
            print(f"screenshot probe-corners-{tag}-bottom.png", flush=True)
            pg.evaluate("""() => {
              window.scrollTo(0, 0);
            }""")
            pg.wait_for_timeout(400)
            dims = pg.evaluate("""async () => {
              const medal = document.querySelector('.cm-tl .crest-medal');
              const bg = medal ? getComputedStyle(medal).backgroundImage : '';
              const uri = (bg.match(/url\\("([^"]+)"\\)/) || [])[1] || '';
              if (!uri) return null;
              const img = new Image();
              await new Promise((res, rej) => { img.onload = res; img.onerror = rej; img.src = uri; });
              return {w: img.naturalWidth, h: img.naturalHeight};
            }""")
            check(f"C-EMBLEM-{tag} emblem decodes 1800x2000 in-page",
                  dims == {"w": 1800, "h": 2000}, dims)
            check(f"C-ERRORS-{tag} no page errors", not errors, errors)
            judge(g, g2, tag, box)
            # The pre-existing install veil auto-shows 5s after load (up
            # to 3x per browser, never over a finished document) and
            # would cover the certificate in the screenshot. Dismiss it
            # the user's way (NOT NOW) so the evidence shows the page;
            # the veil is base behavior, not this round's, and dismissing
            # it touches no certificate state.
            try:
                pg.locator("#installLater").click(timeout=1200)
                print(f"veil dismissed at {tag} (pre-existing install prompt)", flush=True)
            except Exception:
                pass
            pg.screenshot(path=os.path.join(HERE, f"probe-corners-{tag}.png"))
            print(f"screenshot probe-corners-{tag}.png", flush=True)
            ctx.close()
        browser.close()

    fails = [r for r in results if not r["ok"]]
    print(f"\nPROBE-CORNERS: {len(results) - len(fails)}/{len(results)} checks passed")
    with open(os.path.join(HERE, "probe-corners-results.json"), "w") as f:
        json.dump(results, f, indent=2)
    if fails:
        print("FAILED:", [r["check"] for r in fails])
        sys.exit(1)
    print("PROBE-CORNERS OK — no alias typed, no claim made, no test cert touched")


if __name__ == "__main__":
    main()
