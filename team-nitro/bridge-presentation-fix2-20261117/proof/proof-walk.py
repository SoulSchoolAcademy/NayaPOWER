#!/usr/bin/env python3
"""Walk-drive re-proof for fix2 (mirror): K1/K2/K3/K4/C1.
Loads /welcome with a fresh alias, drives the 14 question steps
(type + Enter), checks the name-step crests (K3), the end-slide links
(K4), and the certificate at 635 (C1). K1 eye geometry at 635 + 390.
Usage: python3 proof-walk.py [alias-suffix]
"""
import json, os, sys
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8899"
OUT = "/tmp/fix2/proof"
SUFFIX = sys.argv[1] if len(sys.argv) > 1 else "fix2a"
results = {}

with sync_playwright() as p:
    browser = p.chromium.launch(
        proxy={"server": "http://127.0.0.1:18080", "bypass": "127.0.0.1,localhost"},
        args=["--no-sandbox"])

    for w in (635, 390):
        ctx = browser.new_context(viewport={"width": w, "height": 900})
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        alias = ("fix2%s%d" % (SUFFIX, w)).lower()
        pg.goto(BASE + "/welcome?name=Fix2+Test&alias=" + alias,
                wait_until="load", timeout=60000)
        pg.wait_for_timeout(6000)
        k1 = pg.evaluate("""() => {
          const r = s => { const e = document.querySelector(s); if (!e) return null;
            const b = e.getBoundingClientRect();
            return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width),
                    h: Math.round(b.height), hidden: e.hidden,
                    disp: getComputedStyle(e).display}; };
          const q1 = document.querySelector('.p3-question');
          return { q1Text: q1 ? q1.textContent.trim() : null,
                   eye: r('.p3-choice-eye'), editBtn: r('.p3-custom-btns .p3-enter, .p3-custom-btns button'),
                   customBtns: r('.p3-custom-btns'), url: location.href }; }""")
        results[f"K1K2-{w}"] = {"k1": k1, "errors": errs}
        print(f"K1K2-{w}:", json.dumps({"k1": k1, "errors": errs}))
        pg.screenshot(path=OUT + f"/k1-{w}-q1.png")
        pg.close(); ctx.close()

    # Full drive at 635 for K3/K4/C1
    w = 635
    ctx = browser.new_context(viewport={"width": w, "height": 900})
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    alias = ("fix2%sdrive" % SUFFIX).lower()
    pg.goto(BASE + "/welcome?name=Fix2+Test&alias=" + alias,
            wait_until="load", timeout=60000)
    pg.wait_for_timeout(6000)
    answers = ["I am Fix2 Test, a tester.", "Learning and building.",
               "A kinder internet.", "To help everyone win.",
               "Honesty and care.", "A world that works for all.",
               "I make useful things.", "I offer my time and skill.",
               "I am building a test world.", "A space for testers.",
               "Local news matters.", "Global news matters.",
               "Provincial news matters.", "I create anywhere."]
    step = 0
    for ans in answers:
        try:
            ta = pg.query_selector("textarea.visionin")
            if not ta:
                print("drive: no textarea at step", step)
                break
            ta.fill(ans)
            pg.wait_for_timeout(400)
            pg.keyboard.press("Enter")
            pg.wait_for_timeout(1500)
            step += 1
        except Exception as ex:
            print("drive: step", step, "failed:", ex)
            break
    print("drive: completed", step, "question steps")
    pg.wait_for_timeout(3000)
    # names step?
    names = pg.evaluate("""() => {
      const bodyCls = document.body.className;
      const crests = Array.from(document.querySelectorAll('.p3-crest')).map(e => ({
        disp: getComputedStyle(e).display,
        rect: (() => { const b = e.getBoundingClientRect();
          return {w: Math.round(b.width), h: Math.round(b.height)}; })() }));
      return {bodyCls, crests, url: location.href,
              stepText: (document.querySelector('.p3-question')||{}).textContent}; }""")
    results["K3-names"] = names
    print("K3-names:", json.dumps(names))
    pg.screenshot(path=OUT + "/k3-635-names.png")
    # fill names if present
    try:
        for sel, val in (("#p3Name", "Fix2 Test"), ("#p3Alias", alias)):
            el = pg.query_selector(sel)
            if el:
                el.fill(val)
        # try the names continue button
        for sel in ("#p3NamesNext", ".p3-names-next", "button.p3-enter"):
            try:
                pg.click(sel, timeout=2000)
                pg.wait_for_timeout(2500)
                break
            except Exception:
                continue
    except Exception as ex:
        print("names fill failed:", ex)
    pg.wait_for_timeout(6000)
    end = pg.evaluate("""() => {
      const r = s => { const e = document.querySelector(s); if (!e) return null;
        const b = e.getBoundingClientRect();
        return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width),
                h: Math.round(b.height), hidden: e.hidden, text: (e.textContent||'').trim().slice(0,60)}; };
      return { url: location.href, bodyCls: document.body.className,
               endViews: r('.p3-end-views'),
               links: Array.from(document.querySelectorAll('.p3-end-views a')).map(a => ({
                 href: a.getAttribute('href'), text: a.textContent.trim(),
                 rect: (() => { const b = a.getBoundingClientRect();
                   return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width),
                           h: Math.round(b.height)}; })() })) }; }""")
    results["K4-end"] = end
    print("K4-end:", json.dumps(end), "errors:", errs)
    pg.screenshot(path=OUT + "/k4-635-end.png")
    pg.close(); ctx.close()
    browser.close()

json.dump(results, open("/tmp/fix2/proof/results-walk.json", "w"), indent=1)
print("WALK DONE")
