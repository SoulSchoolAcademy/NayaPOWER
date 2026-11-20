#!/usr/bin/env python3
"""Captain's eye fix-5 — drive 2: desktop 1920x1080 regression, staged host.
Root, identity paired, door 10s hold + Continue, unfold 1-37 (text-Next),
board-37 title, bridge geo (no overflow, symmetric margins), F9 spot checks.
Writes eye-log2.json."""
import json, secrets, time
from playwright.sync_api import sync_playwright

BASE = "https://naya-walk-beginning-staging.nayapower.workers.dev"
EYE = "/home/hatch/workspace/team-nitro/walkthrough-agreement-distill-fix5-20261119/eye"
LOGP = EYE + "/eye-log2.json"
ALIAS = "eye5desk" + secrets.token_hex(3)

def counter(page):
    return page.evaluate("() => { const m = document.body.innerText.match(/(\\d+)\\s*\\/\\s*37/); return m ? m[0] : null; }")

def settle_counter(page, timeout=3000):
    end = time.time() + timeout / 1000
    last = None; stable = 0
    while time.time() < end:
        c = counter(page)
        if c is not None and c == last:
            stable += 1
            if stable >= 2: return c
        else:
            stable = 0
        last = c
        page.wait_for_timeout(120)
    return last

out = {"label": "EYE-FIX5-DESKTOP1920", "alias": ALIAS, "legs": []}
def leg(name, fn):
    try:
        out["legs"].append({"leg": name, **fn()})
        print("LEG OK", name, flush=True)
    except Exception as e:
        out["legs"].append({"leg": name, "ERROR": str(e)[:600]})
        print("LEG FAIL", name, str(e)[:300], flush=True)

with sync_playwright() as pw:
    b = pw.firefox.launch(headless=True)
    ctx = b.new_context(viewport={"width": 1920, "height": 1080}, device_scale_factor=1, ignore_https_errors=True)
    page = ctx.new_page()
    errs = []
    page.on("pageerror", lambda e: errs.append("pageerror: " + str(e)[:200]))
    page.on("console", lambda m: errs.append("console." + m.type + ": " + m.text[:200]) if m.type == "error" else None)

    def leg_root():
        page.goto(BASE + "/", timeout=60000); page.wait_for_timeout(2500)
        page.screenshot(path=EYE + "/eye-30-desk-root.png")
        return page.evaluate("() => ({scrollW: document.documentElement.scrollWidth, innerW: window.innerWidth, buttons: [...document.querySelectorAll('button')].filter(x=>x.offsetParent!==null).map(x=>x.innerText.trim()).slice(0,10)})")
    leg("1-root-1920", leg_root)

    def leg_ident():
        page.goto(BASE + "/identity.html?name=Shawn&alias=Shawn", timeout=60000); page.wait_for_timeout(2500)
        page.screenshot(path=EYE + "/eye-31-desk-identity.png")
        return page.evaluate(r"""() => {
          const R = el => { if (!el) return null; const b = el.getBoundingClientRect();
            return [Math.round(b.left), Math.round(b.top), Math.round(b.right), Math.round(b.bottom)]; };
          const ov = (a,b) => { if (!a || !b) return null;
            return Math.round(Math.max(0, Math.min(a[2],b[2])-Math.max(a[0],b[0])) * Math.max(0, Math.min(a[3],b[3])-Math.max(a[1],b[1]))); };
          const hero = document.querySelector('#displayName'), title = document.querySelector('.cert-title');
          return {hero: hero ? hero.textContent.trim() : null, heroVisible: hero ? hero.offsetParent !== null : null,
            heroTitleOverlap: ov(R(hero), R(title)), heroRect: R(hero), titleRect: R(title),
            scrollW: document.documentElement.scrollWidth, innerW: window.innerWidth};
        }""")
    leg("A-identity-1920", leg_ident)

    def leg_door():
        page.goto(BASE + f"/welcome?name=Eye%20Five&alias={ALIAS}", timeout=60000); page.wait_for_timeout(2000)
        steps0 = page.evaluate("() => [...document.querySelectorAll('[id^=step-]')].filter(e=>e.offsetParent!==null).map(e=>e.id)")
        page.wait_for_timeout(10000)
        steps10 = page.evaluate("() => [...document.querySelectorAll('[id^=step-]')].filter(e=>e.offsetParent!==null).map(e=>e.id)")
        page.screenshot(path=EYE + "/eye-32-desk-door.png")
        page.locator("#doorContinue").click(timeout=6000)
        page.wait_for_timeout(1500)
        steps_after = page.evaluate("() => [...document.querySelectorAll('[id^=step-]')].filter(e=>e.offsetParent!==null).map(e=>e.id)")
        return {"at0": steps0, "at10s": steps10, "held": steps0 == steps10, "afterContinue": steps_after}
    leg("door-10s-hold-1920", leg_door)

    def leg_unfold():
        page.goto(BASE + "/agreement", timeout=60000); page.wait_for_timeout(2000)
        page.screenshot(path=EYE + "/eye-33-desk-unfold1.png")
        seen = []
        for i in range(45):
            c = settle_counter(page)
            if c and (not seen or seen[-1] != c): seen.append(c)
            if page.evaluate("() => [...document.querySelectorAll('button')].some(x=>x.offsetParent!==null && /I agree/i.test(x.innerText))"): break
            page.locator("button", has_text="Next").locator("visible=true").first.click(timeout=5000)
            page.wait_for_timeout(350)
        page.screenshot(path=EYE + "/eye-34-desk-unfold37.png")
        d = page.evaluate(r"""() => {
          const R = el => { if (!el) return null; const b = el.getBoundingClientRect();
            return [Math.round(b.left), Math.round(b.top), Math.round(b.right), Math.round(b.bottom)]; };
          const titles = [...document.querySelectorAll('.frame-title, .ib-title')].filter(e => e.offsetParent !== null && /Congratulations/.test(e.textContent));
          const orb = [...document.querySelectorAll('.frame-icon')].filter(e => e.offsetParent !== null)[0] || null;
          return {titleFont: titles[0] ? getComputedStyle(titles[0]).fontSize : null,
            titleRect: titles[0] ? R(titles[0]) : null, orbRect: R(orb),
            titleText: titles[0] ? titles[0].textContent.replace(/\s+/g,' ').trim() : null};
        }""")
        return {"seenCount": len(seen), "first": seen[:2], "last": seen[-2:],
                "sequential": seen == [f"{n} / 37" for n in range(1, len(seen) + 1)], "D-desktop": d}
    leg("unfold-1-37-1920", leg_unfold)

    def leg_bridge_geo():
        page.locator("button", has_text="I agree").locator("visible=true").first.click(timeout=5000)
        t0 = time.time()
        page.wait_for_selector("#fpLegal .fp-legal-links", state="attached", timeout=15000)
        waited = round(time.time() - t0, 1)
        page.wait_for_timeout(800)
        geo = page.evaluate(r"""() => {
          const nav = document.querySelector('#fpLegal .fp-legal-links');
          if (!nav) return {error: 'no nav'};
          const cs = getComputedStyle(nav);
          const r = nav.getBoundingClientRect();
          const links = [...nav.querySelectorAll('a, button')].map(el => {
            const b = el.getBoundingClientRect();
            return {t: el.textContent.trim(), left: Math.round(b.left), right: Math.round(b.right)};
          });
          return {navRect: [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)],
            scrollWidth: nav.scrollWidth, clientWidth: nav.clientWidth,
            justifyContent: cs.justifyContent, flexWrap: cs.flexWrap, links,
            firstLeft: links[0] ? links[0].left : null, lastRight: links[links.length-1] ? links[links.length-1].right : null,
            scrollW: document.documentElement.scrollWidth, innerW: window.innerWidth};
        }""")
        page.screenshot(path=EYE + "/eye-35-desk-bridge.png")
        return {"url": page.url, "waitForNavSeconds": waited, "geo": geo}
    leg("bridge-geo-1920", leg_bridge_geo)

    def leg_pair():
        return {"pair": page.evaluate("() => [...document.querySelectorAll('button')].filter(x=>x.offsetParent!==null).map(x=>x.innerText.trim()).filter(t=>/Begin the visual story|Read the agreement/.test(t))")}
    leg("bridge-pair-1920", leg_pair)

    out["legs"].append({"leg": "1920-console-errors", "errors": errs})
    b.close()

with open(LOGP, "w") as f:
    json.dump(out, f, indent=1)
print("WROTE", LOGP)
for l in out["legs"]:
    print(json.dumps(l)[:1000], flush=True)
