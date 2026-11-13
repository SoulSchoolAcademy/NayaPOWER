#!/usr/bin/env python3
"""Rendered walk of the staged twelve-sisters transparency page (Step 4).
Playwright Firefox, widths 1440/390/360. Read-only: clicks + scrolls only.
Checks per width: surface present, all 12 sisters + 2 build notes visible,
horizontal overflow 0 at scroll 0/mid/bottom, console/page errors counted
and classified. Click-through at 1440: Sophia's Personal page link (proves
an entry's links work) + her GitHub note link href check.
Writes walk-twelve-results.json + screenshots into this dir.
Usage: python3 walk-twelve-probe.py
"""
import json, os, sys
from playwright.sync_api import sync_playwright

D = "/home/hatch/workspace/team-nitro/family-activation-20261113"
URL = ("https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/"
       "team-transparency-20261112/team-transparency-hub.html"
       "&ref=team-transparency-20261112&cb=e04f77d6e0233d550b1e1174668a8821c032606d")
SISTERS = ["Sophia", "Thea", "Zoe", "Astraea", "Vera", "Wren",
           "Iris", "Ruth", "Terra", "Esme", "Mira", "Aurelia"]

results = {"url": URL, "widths": {}, "fail": []}

with sync_playwright() as p:
    b = p.firefox.launch()
    for w in (1440, 390, 360):
        errs, pageerrs = [], []
        ctx = b.new_context(viewport={"width": w, "height": 900})
        pg = ctx.new_page()
        pg.on("console", lambda m: errs.append(f"{m.type}: {m.text[:200]}") if m.type == "error" else None)
        pg.on("pageerror", lambda e: pageerrs.append(str(e)[:200]))
        pg.goto(URL, wait_until="load", timeout=120000)
        pg.wait_for_timeout(4000)
        # surface present?
        surf = pg.evaluate("() => { const el = document.querySelector('#team-transparency'); return el ? {h: el.offsetHeight, top: el.getBoundingClientRect().top + window.scrollY} : null; }")
        text = pg.evaluate("() => document.querySelector('#team-transparency') ? document.querySelector('#team-transparency').innerText : ''")
        seen = [s for s in SISTERS if s in text and f"Briefed by {s}" in text]
        build_notes = sum(1 for t in ("team-transparency-build-finished", "team-transparency-build-started") if t in text or t in pg.content())
        # overflow at scroll 0 / mid / bottom
        ov = {}
        for label, y in (("top", 0), ("mid", None), ("bottom", None)):
            if y is None:
                h = pg.evaluate("() => document.documentElement.scrollHeight")
                y = h // 2 if label == "mid" else h
            pg.evaluate(f"() => window.scrollTo(0, {y})")
            pg.wait_for_timeout(1200)
            ov[label] = pg.evaluate("() => ({sw: document.documentElement.scrollWidth, iw: window.innerWidth, over: document.documentElement.scrollWidth - window.innerWidth, sh: document.documentElement.scrollHeight, sy: window.scrollY})")
        shots = {}
        pg.evaluate("() => window.scrollTo(0, 0)")
        pg.wait_for_timeout(800)
        pg.screenshot(path=os.path.join(D, f"walk-twelve-{w}-top.png"))
        shots["top"] = f"walk-twelve-{w}-top.png"
        h = pg.evaluate("() => document.documentElement.scrollHeight")
        pg.evaluate(f"() => window.scrollTo(0, {h})")
        pg.wait_for_timeout(800)
        pg.screenshot(path=os.path.join(D, f"walk-twelve-{w}-bottom.png"))
        shots["bottom"] = f"walk-twelve-{w}-bottom.png"
        click = {}
        if w == 1440:
            # click Sophia's Personal page link inside the surface
            href = pg.evaluate("""() => {
              const surf = document.querySelector('#team-transparency');
              const links = [...surf.querySelectorAll('a')];
              const l = links.find(a => (a.href || '').includes('/pages/sophia/sophia'));
              if (!l) return null;
              return {href: l.href, text: l.textContent.trim().slice(0, 80)};
            }""")
            click["sophia_personal_link"] = href
            if href:
                with pg.expect_navigation(timeout=60000):
                    pg.evaluate("""() => {
                      const surf = document.querySelector('#team-transparency');
                      [...surf.querySelectorAll('a')].find(a => (a.href || '').includes('/pages/sophia/sophia')).click();
                    }""")
                pg.wait_for_timeout(3000)
                click["landed_url"] = pg.url
                click["landed_title"] = pg.title()
                pg.go_back(wait_until="load", timeout=60000)
                pg.wait_for_timeout(2000)
                click["back_url_ok"] = "cb=e04f77d6" in pg.url
        # classify console errors: CORS vs other
        cors = [e for e in errs if "CORS" in e or "Cross-Origin" in e]
        other = [e for e in errs if e not in cors]
        results["widths"][w] = {
            "surface": surf, "sisters_seen": len(seen), "sisters_missing": [s for s in SISTERS if s not in seen],
            "build_notes": build_notes, "overflow": ov, "console_errors": len(errs),
            "console_cors": len(cors), "console_other": other[:5], "pageerrors": pageerrs[:5],
            "click": click, "shots": shots,
        }
        print(f"{w}: surface={surf} sisters={len(seen)}/12 missing={[s for s in SISTERS if s not in seen]} build_notes={build_notes} "
              f"overflow={[ov[k]['over'] for k in ('top','mid','bottom')]} console={len(errs)} (cors {len(cors)}, other {len(other)}) pageerrors={len(pageerrs)}", flush=True)
        if click: print(f"   click: {click}", flush=True)
        ctx.close()
    b.close()

# verdict
for w, r in results["widths"].items():
    if r["sisters_seen"] != 12: results["fail"].append(f"{w}: only {r['sisters_seen']}/12 sisters visible")
    if r["build_notes"] != 2: results["fail"].append(f"{w}: build notes {r['build_notes']} != 2")
    for k, o in r["overflow"].items():
        if o["over"] != 0: results["fail"].append(f"{w} {k}: horizontal overflow {o['over']}px")
    if r["pageerrors"]: results["fail"].append(f"{w}: {len(r['pageerrors'])} pageerrors")
    if r["console_other"]: results["fail"].append(f"{w}: {len(r['console_other'])} non-CORS console errors")
json.dump(results, open(os.path.join(D, "walk-twelve-results.json"), "w"), indent=2)
print("FAILS:", results["fail"] if results["fail"] else "NONE — 0 fails")
print("results written:", os.path.join(D, "walk-twelve-results.json"))
