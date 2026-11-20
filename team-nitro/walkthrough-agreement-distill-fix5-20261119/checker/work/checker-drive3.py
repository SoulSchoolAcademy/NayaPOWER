#!/usr/bin/env python3
"""Fix-5 checker driver 3 — desktop 1920 regression + staged spot-check +
bounded full-walk intro attempt. Writes checker-log3.json."""
import json
from playwright.sync_api import sync_playwright

CK = "/home/hatch/workspace/team-nitro/walkthrough-agreement-distill-fix5-20261119/checker"
FIX = "http://127.0.0.1:18096"
STAGE = "https://naya-walk-beginning-staging.nayapower.workers.dev"
LOG = CK + "/checker-log3.json"

GEO_SWEEP = r"""() => {
  const nav = document.querySelector('#fpLegal .fp-legal-links');
  if (!nav) return {error: 'no nav'};
  const cs = getComputedStyle(nav);
  const links = [...nav.querySelectorAll('a, button')].map(el => el.textContent.trim());
  const max = nav.scrollWidth - nav.clientWidth;
  const seen = links.map(() => null);
  const positions = [0];
  for (let s = 100; s < max; s += 100) positions.push(s);
  if (max > 0) positions.push(max);
  for (const sl of positions) {
    nav.scrollLeft = sl;
    const actual = nav.scrollLeft;
    [...nav.querySelectorAll('a, button')].forEach((el, i) => {
      const r = el.getBoundingClientRect();
      if (r.left >= 0 && r.right <= 390 && seen[i] === null) seen[i] = actual;
    });
  }
  nav.scrollLeft = 0;
  const reach = seen.map((s, i) => ({link: links[i], reachable: s !== null, at: s}));
  return {scrollWidth: nav.scrollWidth, clientWidth: nav.clientWidth, maxScroll: max,
    justifyContent: cs.justifyContent, linkCount: links.length,
    unreachable: reach.filter(r => !r.reachable).length, reachable: reach};
}"""

def counter(page):
    return page.evaluate("() => { const m = document.body.innerText.match(/(\\d+)\\s*\\/\\s*37/); return m ? m[0] : null; }")

out = {"label": "FIX5-CHECKER-DRIVE3", "legs": []}
def leg(name, fn):
    try:
        out["legs"].append({"leg": name, **fn()})
    except Exception as e:
        out["legs"].append({"leg": name, "ERROR": str(e)[:600]})
        print("LEG FAIL", name, str(e)[:300], flush=True)

with sync_playwright() as pw:
    # ---- desktop 1920 on FIX5 ----
    b = pw.firefox.launch(headless=True)
    ctx = b.new_context(viewport={"width": 1920, "height": 1080}, device_scale_factor=1, ignore_https_errors=True)
    page = ctx.new_page()
    errs = []
    page.on("pageerror", lambda e: errs.append(str(e)[:200]))
    page.on("console", lambda m: errs.append(m.type + ": " + m.text[:200]) if m.type == "error" else None)
    def leg_desk_ident():
        page.goto(FIX + "/identity.html?name=Shawn&alias=Shawn", timeout=60000); page.wait_for_timeout(2500)
        return page.evaluate("() => { const inp = document.querySelector('input'); const hero = document.querySelector('#displayName'); const r = hero ? hero.getBoundingClientRect() : null; return {input: inp ? inp.value : null, hero: hero ? hero.textContent.trim() : null, heroRect: r ? [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)] : null, scrollW: document.documentElement.scrollWidth, innerW: window.innerWidth}; }")
    leg("1920-identity-paired", leg_desk_ident)
    def leg_desk_door():
        page.goto(FIX + "/welcome?name=Fix5%20Walk&alias=fix5walktest1", timeout=60000); page.wait_for_timeout(2000)
        steps0 = page.evaluate("() => [...document.querySelectorAll('[id^=step-]')].filter(e=>e.offsetParent!==null).map(e=>e.id)")
        page.wait_for_timeout(10000)
        steps10 = page.evaluate("() => [...document.querySelectorAll('[id^=step-]')].filter(e=>e.offsetParent!==null).map(e=>e.id)")
        page.locator("#doorContinue").click(timeout=6000); page.wait_for_timeout(1500)
        after = page.evaluate("() => [...document.querySelectorAll('[id^=step-]')].filter(e=>e.offsetParent!==null).map(e=>e.id)")
        return {"at0": steps0, "at10s": steps10, "held": steps0 == steps10, "afterContinue": after}
    leg("1920-door-10s-continue", leg_desk_door)
    def leg_desk_unfold():
        page.goto(FIX + "/agreement", timeout=60000); page.wait_for_timeout(2000)
        for i in range(40):
            if page.evaluate("() => [...document.querySelectorAll('button')].some(x=>x.offsetParent!==null && /I agree/i.test(x.innerText))"): break
            page.locator("button", has_text="Next").locator("visible=true").first.click(timeout=5000)
            page.wait_for_timeout(350)
        t = page.evaluate("() => { const el = [...document.querySelectorAll('.frame-title, .ib-title')].find(e=>e.offsetParent!==null && /Congratulations/.test(e.textContent)); if (!el) return null; const r = el.getBoundingClientRect(); return {font: getComputedStyle(el).fontSize, rect: [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]}; }")
        page.screenshot(path=CK + "/ck5-1920-unfold37.png")
        return {"title37": t, "counter": counter(page)}
    leg("1920-unfold-board37", leg_desk_unfold)
    out["legs"].append({"leg": "1920-console-errors", "errors": errs})
    b.close()

    # ---- staged spot-check: bridge sweep on the live staged host ----
    b = pw.firefox.launch(headless=True)
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, ignore_https_errors=True)
    page = ctx.new_page()
    errs2 = []
    page.on("pageerror", lambda e: errs2.append(str(e)[:200]))
    page.on("console", lambda m: errs2.append(m.type + ": " + m.text[:200]) if m.type == "error" else None)
    def leg_staged():
        page.goto(STAGE + "/agreement", timeout=60000); page.wait_for_timeout(2000)
        for i in range(40):
            if page.evaluate("() => [...document.querySelectorAll('button')].some(x=>x.offsetParent!==null && /I agree/i.test(x.innerText))"): break
            page.locator("button", has_text="Next").locator("visible=true").first.click(timeout=5000)
            page.wait_for_timeout(350)
        page.locator("button", has_text="I agree").locator("visible=true").first.click(timeout=5000)
        page.wait_for_timeout(2500)
        geo = page.evaluate(GEO_SWEEP)
        page.evaluate("() => { const n = document.querySelector('#fpLegal .fp-legal-links'); if (n) n.scrollLeft = 0; }")
        page.wait_for_timeout(400)
        page.screenshot(path=CK + "/ck5-staged-bridge-s0.png")
        geo["consoleErrors"] = errs2
        return geo
    leg("staged-bridge-footer-geo", leg_staged)
    b.close()

    # ---- bounded full-walk intro attempt: identity paired -> ENTER -> walk ----
    b = pw.firefox.launch(headless=True)
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, ignore_https_errors=True)
    page = ctx.new_page()
    errs3 = []
    page.on("pageerror", lambda e: errs3.append(str(e)[:200]))
    page.on("console", lambda m: errs3.append(m.type + ": " + m.text[:200]) if m.type == "error" else None)
    def leg_walk_intro():
        page.goto(FIX + "/identity.html?name=Checker%20Five&alias=checkerfive", timeout=60000); page.wait_for_timeout(2500)
        page.locator("#enterBtn").click(timeout=6000); page.wait_for_timeout(3000)
        trace = [{"url": page.url, "body": page.evaluate("() => document.body.className"),
                  "steps": page.evaluate("() => [...document.querySelectorAll('[id^=step-]')].filter(e=>e.offsetParent!==null).map(e=>e.id)")}]
        # walk the door + steps, clicking the visible continue/next control each time (cap 20)
        for i in range(20):
            state = page.evaluate("() => ({url: location.href, body: document.body.className, fpLegal: (() => { const f = document.querySelector('#fpLegal'); return f ? getComputedStyle(f).display : 'MISSING'; })(), steps: [...document.querySelectorAll('[id^=step-]')].filter(e=>e.offsetParent!==null).map(e=>e.id), btns: [...document.querySelectorAll('button')].filter(x=>x.offsetParent!==null).map(x=>(x.id?'#'+x.id+' ':'')+x.innerText.trim().slice(0,36))})")
            trace.append(state)
            if "fp-intro" in state["body"] and state["fpLegal"] == "block":
                break
            clicked = False
            for sel in ("#doorContinue", "#fpNextBtn"):
                try:
                    loc = page.locator(sel)
                    if loc.count() and page.evaluate("(s) => { const el=document.querySelector(s); return el && el.offsetParent!==null; }", sel):
                        loc.first.click(timeout=4000); page.wait_for_timeout(1200); clicked = True; break
                except Exception:
                    pass
            if not clicked:
                # fall back to any visible Continue/Next button
                try:
                    page.locator("button", has_text="Continue").locator("visible=true").first.click(timeout=4000)
                    page.wait_for_timeout(1200); clicked = True
                except Exception:
                    break
            if not clicked:
                break
        final = page.evaluate("() => ({url: location.href, body: document.body.className, fpLegal: (() => { const f = document.querySelector('#fpLegal'); return f ? getComputedStyle(f).display : 'MISSING'; })()})")
        geo = page.evaluate(GEO_SWEEP) if "fp-intro" in final["body"] else {"error": "intro stage not reached by the walk in 20 clicks"}
        return {"trace": trace, "final": final, "geo": geo, "consoleErrors": errs3}
    leg("intro-via-full-walk-bounded", leg_walk_intro)
    b.close()

with open(LOG, "w") as f:
    json.dump(out, f, indent=1)
for l in out["legs"]:
    print(json.dumps(l)[:1500], flush=True)
print("WROTE", LOG)
