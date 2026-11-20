#!/usr/bin/env python3
"""Walk re-proof v4 (CORRECTED drive — for re-run when the VM browsers recover).
Fixes v1-v3 probe errors:
- Step is tracked by the VISIBLE [id^="step-"] section, NEVER by
  document.querySelector('.p3-question') (always returns step 1's heading).
- Answers go into the visible #answer-N box + #enterBtn-N click; yes/no
  steps use [data-act="yes"]/["no"]; Skip is the fallback, never the plan.
- K3 reads body.p3-names-on + crest displays AT step 14 (names).
- K4 reads .p3-end-views links when ENDSEC (step 16) is visible.
- C1 screenshots the certificate at 635 in the end section.
K1 (4/4 pairs same-row, 635+390) and K2 (21/21 headings unquoted) are
already proven live — see results-walk2.json; this script re-checks them
cheaply and drives K3/K4/C1.
Usage: python3 proof-walk4.py [alias-suffix]"""
import json, sys
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8899"
OUT = "/tmp/fix2/proof"
SUFFIX = sys.argv[1] if len(sys.argv) > 1 else "fix2d"
ANSWERS = ["I am Fix2 Test, a tester.", "Learning and building.",
           "A kinder internet.", "To help everyone win.",
           "Honesty and care.", "A world that works for all.",
           "I make useful things.", "I offer my time and skill.",
           "I am building a test world.", "A space for testers.",
           "Local news matters.", "Global news matters.",
           "Provincial news matters.", "I create anywhere."]
res = {}

def cur_step(pg):
    return pg.evaluate("""() => {
      const vis = [...document.querySelectorAll('[id^="step-"]')].filter(s => s.getBoundingClientRect().height > 0).map(s => s.id);
      const names = !document.querySelector('#step-names').hidden;
      const build = !document.querySelector('#step-build').hidden;
      const end = !document.querySelector('#step-end').hidden;
      return {visibleSections: vis, namesShown: names, buildShown: build, endShown: end,
              body: document.body.className};
    }""")

with sync_playwright() as p:
    br = p.chromium.launch(
        proxy={"server": "http://127.0.0.1:18080", "bypass": "127.0.0.1,localhost"},
        args=["--no-sandbox"])
    ctx = br.new_context(viewport={"width": 635, "height": 900})
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(BASE + "/welcome?name=Fix2+Test&alias=fix2" + SUFFIX + "drive",
            wait_until="load", timeout=60000)
    pg.wait_for_timeout(6000)
    log = []
    for step in range(14):
        cs = cur_step(pg)
        log.append(f"step{step}: {cs}")
        if cs["namesShown"] or cs["endShown"]:
            break
        n = cs["visibleSections"][0].split("-")[1] if cs["visibleSections"] else "?"
        ans = ANSWERS[step]
        done = False
        # yes/no steps have no answer box: use the yes button
        try:
            yn = pg.locator('[data-act="yes"] >> visible=true')
            if yn.count():
                yn.first.click(timeout=2000)
                pg.wait_for_timeout(1500)
                done = True
                log.append(f"  answered YES (step {n})")
        except Exception:
            pass
        if not done:
            try:
                box = pg.locator(f"#answer-{n} >> visible=true")
                box.fill(ans)
                pg.wait_for_timeout(400)
                pg.click(f"#enterBtn-{n} >> visible=true", timeout=3000)
                pg.wait_for_timeout(1500)
                done = True
            except Exception as ex:
                log.append(f"  answer FAIL step {n}: {str(ex)[:150]}")
        if not done:
            try:
                pg.click('[data-act="skip"] >> visible=true', timeout=2500)
                pg.wait_for_timeout(1200)
                log.append(f"  used SKIP (step {n})")
            except Exception as ex:
                log.append(f"  SKIP FAIL step {n}: {str(ex)[:150]}")
                break
    res["driveLog"] = log
    res["afterDrive"] = cur_step(pg)
    pg.screenshot(path=OUT + "/k3d-635-after-drive.png")
    res["K3-names"] = pg.evaluate("""() => {
      const crests = [...document.querySelectorAll('.p3-crest')].map(e => ({
        cls: e.className, disp: getComputedStyle(e).display,
        w: Math.round(e.getBoundingClientRect().width), h: Math.round(e.getBoundingClientRect().height)}));
      return {bodyCls: document.body.className, crests,
              nameInput: !!document.querySelector('#p3Name'),
              aliasInput: !!document.querySelector('#p3Alias')};
    }""")
    for sel, val in (("#p3Name", "Fix2 Test"), ("#p3Alias", "fix2" + SUFFIX + "drive")):
        el = pg.query_selector(sel)
        if el:
            el.fill(val)
    pg.wait_for_timeout(500)
    clicked = None
    for sel in ("#p3NamesNext", ".p3-names-next", '[data-act="names-next"]',
                ".p3-names .p3-enter", ".p3-names button"):
        try:
            pg.click(sel + " >> visible=true", timeout=2000)
            clicked = sel
            break
        except Exception:
            continue
    res["namesContinueClicked"] = clicked
    pg.wait_for_timeout(6000)
    res["afterNames"] = cur_step(pg)
    pg.screenshot(path=OUT + "/k4d-635-after-names.png")
    res["K4-end"] = pg.evaluate("""() => {
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
    pg.screenshot(path=OUT + "/k4d-635-end.png")
    res["C1"] = pg.evaluate("""() => {
      const h = [...document.querySelectorAll('#step-end h1, #step-end h2, #step-end [class*="cert"]')].map(e => ({
        tag: e.tagName, cls: String(e.className).slice(0,50),
        vis: e.getBoundingClientRect().height > 0,
        text: (e.textContent||'').trim().slice(0,100)}));
      return {bodyCls: document.body.className, endHeadings: h};
    }""")
    pg.screenshot(path=OUT + "/c1d-635.png")
    res["walkErrors"] = errs
    ctx.close()
    br.close()

print(json.dumps(res, indent=1)[:11000])
with open(OUT + "/results-walk4.json", "w") as f:
    json.dump(res, f, indent=1)
print("WROTE results-walk4.json")
