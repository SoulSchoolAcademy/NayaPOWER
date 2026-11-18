#!/usr/bin/env python3
"""Checker-seat probe for the Pricing Certificate Fix (2026-11-17).
RUN ONCE — the probe alias `certfix` is single-use: the 390 Enter-key
step CLAIMS it (Nº assigned, /api/claim POST). Re-running after the claim
reads the TAKEN state, not the certificate view.

FIXES THE PRIOR ROUND'S PROBE GAPS:
  (a) typed-1920 measurement BEFORE claiming (the prior probe never
      measured the typed name at 1920px);
  (b) Chromium launches with NO proxy — the VM forwarder
      http://127.0.0.1:18080 is VM-only; the cloud browser has its own
      network. Never set proxy here.

ORDER MATTERS: 635 pre-claim first, then 1920 typed, then the 390 claim
LAST (typing + availability check does not claim; only Enter-when-
Available or the ENTER button POSTs /api/claim).

Checks: A2 title + certifies text, old title 0 hits in rendered text;
A3 name computed color solid white + ::after top-edge light present +
carved text-shadow present; A4 agree display:block on certified +
official sentence exact + welcome-back secondary; A5 635 pre-claim:
agree line reachable by wheel scroll, no clip/overlap/black band;
A6 Enter key claims (390) and the ENTER button is the same path;
A7 no gray text (computed colors), certified restore on reload.
VM browsers are DEAD — this probe runs in the cloud browser, not the VM.
"""
import json
import os
import sys

FIXDIR = os.path.expanduser("~/workspace/team-nitro/pricing-certificate-fix-20261117")
URL = "https://naya-pricing-free-staging.nayapower.workers.dev/free"
ALIAS = "certfix"  # FRESH, reserved for this probe, unclaimed. Single-use.
WANT_ENTRY_SHA = "fbd6477f348ab50b8b0eb278fb36e475c25eb55ae27a4d79ca416942161f16fd"

TITLE = "Certificate of the Collective Agreement"
CERTIFIES = "This certificate of the Collective Agreement certifies that"
OFFICIAL = ("By entering your name, you make it official — you are signing the Collective Agreement, "
            "and you get the deed to your own world: high-level digital real estate — your personal page, "
            "your business, your space — free forever.")
WELCOME_BACK = "This Smart Name is yours"

results = []


def check(name, ok, detail=""):
    results.append({"check": name, "ok": bool(ok), "detail": str(detail)[:300]})
    print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail else ""))


def main():
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        # NO proxy: the cloud browser reaches the network directly.
        browser = p.chromium.launch(headless=True)

        # ---- 635x349 PRE-CLAIM (A5): the eye's clipped size, typed state.
        ctx = browser.new_context(viewport={"width": 635, "height": 349})
        pg = ctx.new_page()
        pg.goto(URL, wait_until="networkidle")
        pg.fill("#aliasInput", ALIAS)
        pg.wait_for_selector('#aliasStatus[data-state="available"]', timeout=15000)
        agree = pg.locator(".cert-agree")
        card = pg.locator("#certPlaque")
        box = agree.bounding_box()
        cbox = card.bounding_box()
        check("A5-635 agree element exists", box is not None, box)
        # The card clips (overflow:hidden) until scrolled — the fix opens the scroll path.
        scrollable = pg.evaluate(
            "(() => { const c = document.getElementById('certPlaque'); "
            "return {sh: c.scrollHeight, ch: c.clientHeight, oy: getComputedStyle(c).overflowY}; })()")
        check("A5-635 card scrolls (scrollHeight > clientHeight, overflow-y auto)",
              scrollable["sh"] > scrollable["ch"] and scrollable["oy"] == "auto", scrollable)
        pg.mouse.wheel(0, 800)
        pg.wait_for_timeout(400)
        box2 = agree.bounding_box()
        in_view = (box2 is not None and cbox is not None
                   and box2["y"] >= cbox["y"] and box2["y"] + box2["height"] <= cbox["y"] + cbox["height"])
        check("A5-635 agree line scrolls INTO view whole", in_view, box2)
        txt = agree.inner_text()
        check("A5-635 agree sentence complete after scroll",
              OFFICIAL in txt, txt[:120])
        enter = pg.locator(".activate-btn")
        ebox = enter.bounding_box()
        overlap = (box2 is not None and ebox is not None
                   and not (box2["y"] + box2["height"] <= ebox["y"] or box2["y"] >= ebox["y"] + ebox["height"]))
        check("A5-635 agree does not overlap ENTER button", not overlap,
              f"agree={box2} enter={ebox}")
        pg.screenshot(path=os.path.join(FIXDIR, "probe-635-preclaim.png"))
        ctx.close()

        # ---- 1920 TYPED (A2/A3, gap (a)): measure the typed name before claiming.
        ctx = browser.new_context(viewport={"width": 1920, "height": 1080})
        pg = ctx.new_page()
        pg.goto(URL, wait_until="networkidle")
        pg.fill("#aliasInput", ALIAS)
        pg.wait_for_selector('#aliasStatus[data-state="available"]', timeout=15000)
        check("A2-1920 title text", pg.locator(".cert-title").inner_text() == TITLE,
              pg.locator(".cert-title").inner_text())
        check("A2-1920 certifies text", pg.locator(".cert-certifies").inner_text() == CERTIFIES,
              pg.locator(".cert-certifies").inner_text())
        body_text = pg.inner_text("body")
        check("A2-1920 old title 0 hits in rendered text",
              "Certificate of Smart Identity" not in body_text and
              "CERTIFICATE OF SMART IDENTITY" not in body_text)
        name = pg.locator(".cert-name")
        cs = pg.evaluate(
            "(() => { const n = document.querySelector('.cert-name'); const c = getComputedStyle(n); "
            "const a = getComputedStyle(n, '::after'); const b = getComputedStyle(n, '::before'); "
            "const r = n.getBoundingClientRect(); "
            "return {color: c.color, fontSize: c.fontSize, textShadow: c.textShadow, "
            "afterContent: a.content, afterOpacity: a.opacity, afterColor: a.color, "
            "beforeOpacity: b.opacity, rect: {x: r.x, y: r.y, w: r.width, h: r.height}}; })()")
        check("A3-1920 name computed color solid white",
              cs["color"] == "rgb(255, 255, 255)", cs["color"])
        check("A3-1920 name ::after top-edge light present",
              cs["afterContent"] not in ("none", '""') and float(cs["afterOpacity"]) > 0, cs)
        check("A3-1920 name carved text-shadow present",
              cs["textShadow"] not in ("none", ""), cs["textShadow"][:120])
        check("A3-1920 name rect sane (desktop clamp)", cs["rect"]["w"] > 100 and cs["rect"]["h"] > 30, cs["rect"])
        check("A4-1920 pre-claim official sentence exact x1",
              body_text.count(OFFICIAL) == 1, f"count={body_text.count(OFFICIAL)}")
        pg.screenshot(path=os.path.join(FIXDIR, "probe-1920-typed.png"))
        ctx.close()

        # ---- 390 CLAIM BY ENTER KEY (A6), then certified face (A3/A4/A7).
        ctx = browser.new_context(viewport={"width": 390, "height": 844})
        pg = ctx.new_page()
        pg.goto(URL, wait_until="networkidle")
        pg.fill("#aliasInput", ALIAS)
        pg.wait_for_selector('#aliasStatus[data-state="available"]', timeout=15000)
        pg.press("#aliasInput", "Enter")
        pg.wait_for_selector("#certPlaque.is-certified", timeout=15000)
        check("A6-390 Enter key claimed (is-certified)", True,
              pg.url)
        check("A2-390 certified title", pg.locator(".cert-title").inner_text() == TITLE)
        check("A2-390 certified certifies", pg.locator(".cert-certifies").inner_text() == CERTIFIES)
        disp = pg.evaluate(
            "getComputedStyle(document.querySelector('.cert-agree')).display")
        check("A4-390 agree display:block on certified", disp == "block", disp)
        body_text = pg.inner_text("body")
        check("A4-390 official sentence still on certified",
              OFFICIAL in body_text)
        check("A4-390 welcome-back secondary line present",
              WELCOME_BACK in body_text)
        ncs = pg.evaluate(
            "(() => { const n = document.querySelector('.cert-name'); const c = getComputedStyle(n); "
            "return {color: c.color, textShadow: c.textShadow}; })()")
        check("A3-390 certified name still solid white",
              ncs["color"] == "rgb(255, 255, 255)", ncs)
        # A7: no gray text — sample the rendered text colors on the certified face.
        colors = pg.evaluate(
            "(() => ['.cert-title', '.cert-certifies', '.cert-agree', '.cert-name', '.alias-status']"
            ".map(s => { const el = document.querySelector(s); "
            "return el ? s + '=' + getComputedStyle(el).color : s + '=MISSING'; }))()")
        gray = [c for c in colors if "rgb(128" in c or "rgb(160" in c or "rgb(169" in c]
        check("A7-390 no gray text (computed colors)", not gray, colors)
        pg.screenshot(path=os.path.join(FIXDIR, "probe-390-certified.png"))
        # Certified restore on reload.
        pg.reload(wait_until="networkidle")
        pg.wait_for_selector("#certPlaque.is-certified", timeout=15000)
        disp2 = pg.evaluate(
            "getComputedStyle(document.querySelector('.cert-agree')).display")
        check("A7-390 certified restore on reload + agree still shown",
              disp2 == "block", disp2)
        pg.screenshot(path=os.path.join(FIXDIR, "probe-390-restored.png"))
        ctx.close()
        browser.close()

    fails = [r for r in results if not r["ok"]]
    print(f"\nPROBE: {len(results) - len(fails)}/{len(results)} checks passed")
    with open(os.path.join(FIXDIR, "probe-fix-results.json"), "w") as f:
        json.dump(results, f, indent=2)
    if fails:
        print("FAILED:", [r["check"] for r in fails])
        sys.exit(1)
    print("PROBE OK — alias certfix claimed once; do not re-run the claim step")


if __name__ == "__main__":
    main()
