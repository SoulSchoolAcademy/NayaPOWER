#!/usr/bin/env python3
"""Walk re-proof v3: correct drive — type into the VISIBLE answer box
(textarea.visionin) then Enter; fall back to Skip if a step stalls.
Then K3 (names-step crests), K4 (end links), C1 (certificate)."""
import json
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8899"
OUT = "/tmp/fix2/proof"
res = {}
ANSWERS = ["I am Fix2 Test, a tester.", "Learning and building.",
           "A kinder internet.", "To help everyone win.",
           "Honesty and care.", "A world that works for all.",
           "I make useful things.", "I offer my time and skill.",
           "I am building a test world.", "A space for testers.",
           "Local news matters.", "Global news matters.",
           "Provincial news matters.", "I create anywhere."]

with sync_playwright() as p:
    br = p.chromium.launch(
        proxy={"server": "http://127.0.0.1:18080", "bypass": "127.0.0.1,localhost"},
        args=["--no-sandbox"])
    ctx = br.new_context(viewport={"width": 635, "height": 900})
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(BASE + "/welcome?name=Fix2+Test&alias=fix2drive3",
            wait_until="load", timeout=60000)
    pg.wait_for_timeout(6000)
    log = []
    for step, ans in enumerate(ANSWERS):
        q = pg.evaluate("() => (document.querySelector('.p3-question')||{textContent:'?'}).textContent.trim()")
        # type into the visible answer box
        try:
            box = pg.locator("textarea.visionin >> visible=true").first
            box.fill(ans)
            pg.wait_for_timeout(400)
            box.press("Enter")
            pg.wait_for_timeout(1500)
        except Exception as ex:
            log.append(f"step{step} fill/enter FAIL: {str(ex)[:150]}")
            # fallback: Skip
            try:
                pg.click('[data-act="skip"] >> visible=true', timeout=2500)
                pg.wait_for_timeout(1200)
                log.append(f"step{step} used SKIP")
            except Exception as ex2:
                log.append(f"step{step} SKIP FAIL: {str(ex2)[:150]}")
                break
        q2 = pg.evaluate("() => (document.querySelector('.p3-question')||{textContent:'?'}).textContent.trim()")
        body = pg.evaluate("() => document.body.className")
        log.append(f"step{step}: {q[:38]} -> {q2[:38]} | body={body}")
        if "step-names" in body or "step-end" in body or "step-cert" in body:
            break
    res["driveLog"] = log
    res["bodyAfterDrive"] = pg.evaluate("() => document.body.className")
    pg.screenshot(path=OUT + "/k3c-635-after-drive.png")
    k3 = pg.evaluate("""() => {
      const crests = [...document.querySelectorAll('.p3-crest')].map(e => ({
        cls: e.className, disp: getComputedStyle(e).display,
        w: Math.round(e.getBoundingClientRect().width), h: Math.round(e.getBoundingClientRect().height)}));
      return {bodyCls: document.body.className, crests,
              q: (document.querySelector('.p3-question')||{textContent:''}).textContent.trim(),
              nameInput: !!document.querySelector('#p3Name'),
              aliasInput: !!document.querySelector('#p3Alias')};
    }""")
    res["K3-names"] = k3
    # fill names + continue
    try:
        for sel, val in (("#p3Name", "Fix2 Test"), ("#p3Alias", "fix2drive3")):
            el = pg.query_selector(sel)
            if el:
                el.fill(val)
        pg.wait_for_timeout(500)
        clicked = None
        for sel in ("#p3NamesNext", ".p3-names-next", '[data-act="names-next"]',
                    ".p3-names .p3-enter", ".p3-names button",
                    '[data-act="submit"] >> visible=true'):
            try:
                pg.click(sel, timeout=2000)
                clicked = sel
                break
            except Exception:
                continue
        res["namesContinueClicked"] = clicked
        pg.wait_for_timeout(5000)
    except Exception as ex:
        res["namesError"] = str(ex)[:300]
    res["afterNames"] = {"body": pg.evaluate("() => document.body.className"),
                         "q": pg.evaluate("() => (document.querySelector('.p3-question')||{textContent:''}).textContent.trim().slice(0,80)")}
    pg.screenshot(path=OUT + "/k4c-635-after-names.png")
    k4 = pg.evaluate("""() => {
      const r = s => { const e = document.querySelector(s); if (!e) return null;
        const b = e.getBoundingClientRect();
        return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width),
                h: Math.round(b.height), hidden: e.hidden, disp: getComputedStyle(e).display}; };
      const links = [...document.querySelectorAll('.p3-end-views a, .p3-end-view')].map(a => ({
        href: a.getAttribute('href'), text: (a.textContent||'').trim(),
        rect: (() => { const b = a.getBoundingClientRect();
          return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height)}; })(),
        disp: getComputedStyle(a).display }));
      return {bodyCls: document.body.className, endViews: r('.p3-end-views'), links};
    }""")
    res["K4-end"] = k4
    pg.screenshot(path=OUT + "/k4c-635-end.png")
    c1 = pg.evaluate("""() => {
      const els = [...document.querySelectorAll('[class*="cert"], [id*="cert"]')].map(e => ({
        cls: String(e.className).slice(0,60), id: e.id,
        vis: e.getBoundingClientRect().height > 0,
        rect: (() => { const b = e.getBoundingClientRect();
          return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height)}; })(),
        text: (e.textContent||'').trim().slice(0,100)}));
      const h = [...document.querySelectorAll('h1,h2')].map(e => e.textContent.trim());
      return {bodyCls: document.body.className, certEls: els.slice(0, 12), headings: h};
    }""")
    res["C1"] = c1
    pg.screenshot(path=OUT + "/c1c-635.png")
    res["walkErrors"] = errs
    ctx.close()
    br.close()

print(json.dumps(res, indent=1)[:11000])
with open(OUT + "/results-walk3.json", "w") as f:
    json.dump(res, f, indent=1)
print("WROTE results-walk3.json")
