#!/usr/bin/env python3
"""Follow-up probe: strip computed style, deck advance to beat 9,
§8 READ clean re-proof, W5 hover in bridge view."""
import json, sys, time
sys.path.insert(0, "/tmp/fix2")
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8899"
OUT = "/tmp/fix2/proof"
res = {}

def flush():
    with open(OUT + "/results2.json", "w") as f:
        json.dump(res, f, indent=1)

def r(el):
    if not el:
        return None
    b = el.bounding_box()
    if not b:
        return None
    return {"x": round(b["x"]), "y": round(b["y"]), "w": round(b["width"]),
            "h": round(b["height"]), "right": round(b["x"] + b["width"]),
            "bottom": round(b["y"] + b["height"])}

with sync_playwright() as p:
    br = p.chromium.launch(
        proxy={"server": "http://127.0.0.1:18080", "bypass": "127.0.0.1,localhost"},
        args=["--no-sandbox"])

    # (a) strip computed style at 635
    ctx = br.new_context(viewport={"width": 635, "height": 900})
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(BASE + "/?stage=bridge", wait_until="load")
    pg.wait_for_timeout(5000)
    st = pg.evaluate("""() => {
      const nav = document.querySelector('#fpLegal .fp-legal-links');
      const cs = getComputedStyle(nav);
      const links = [...document.querySelectorAll('#fpLegal .fp-legal-link')].map(a => {
        const b = a.getBoundingClientRect(); return {t: a.textContent.trim().slice(0,18), x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height)};
      });
      const ys = [...new Set(links.map(l => l.y))];
      return {flexWrap: cs.flexWrap, overflowX: cs.overflowX, justifyContent: cs.justifyContent,
              linkRows: ys, linkCount: links.length, links: links.slice(0, 6)};
    }""")
    res["strip635"] = st
    flush()
    res["strip635_errors"] = errs
    pg.screenshot(path=OUT + "/d4-635-bridge-bottom.png")
    ctx.close()

    # (b) deck advance to beat 9 via #fpNextBtn, screenshot, deckBack at beat 9
    ctx = br.new_context(viewport={"width": 1920, "height": 900})
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(BASE + "/?stage=deck", wait_until="load")
    pg.wait_for_timeout(5000)
    beats = []
    for i in range(9):
        stt = pg.evaluate("() => ({cls: document.body.className, deck: (window.__fpDeck||window.deck||null)})")
        # read the deck state from the DOM: which slide img is shown
        cur = pg.evaluate("""() => {
          const imgs = [...document.querySelectorAll('#fpDeckStage img, #fpDeck img')].map(i => i.getAttribute('src') || '');
          const vis = imgs.filter(s => s.includes('slide-'));
          const beat = document.querySelector('#fpDeckBeat, .deck-beat');
          return {vis, beatText: beat ? beat.textContent : null};
        }""")
        beats.append(cur)
        if i < 8:
            pg.click("#fpNextBtn")
            pg.wait_for_timeout(1200)
    pg.screenshot(path=OUT + "/w4-1920-deck9.png")
    last = pg.evaluate("""() => {
      const imgs = [...document.querySelectorAll('#fpDeckStage img, #fpDeck img')].map(i => i.getAttribute('src') || '');
      return imgs.filter(s => s.includes('slide-'));
    }""")
    res["deckAdvance"] = {"beatsSeen": beats, "finalImgs": last, "errors": errs}
    # deckBack at beat 9
    back = pg.locator("#fpDeckBack")
    res["deckBackAt9"] = {"hidden": back.is_hidden(), "rect": r(back)}
    back.click()
    pg.wait_for_timeout(1500)
    res["deckBackAt9_after"] = pg.evaluate("() => document.body.className")
    flush()
    pg.screenshot(path=OUT + "/deckback-1920-bridge.png")
    ctx.close()

    # (c) §8 READ clean: poll URL after clicking #fpBridgeLetter
    ctx = br.new_context(viewport={"width": 1920, "height": 900})
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(BASE + "/?stage=bridge", wait_until="load")
    pg.wait_for_timeout(5000)
    for i in range(1, 5):
        pg.click("#fpContinue" + str(i))
        pg.wait_for_timeout(900)
    pg.evaluate("() => { document.querySelector('#fpBridge').scrollTop = document.querySelector('#fpBridge').scrollHeight; }")
    pg.wait_for_timeout(800)
    pg.click("#fpBridgeLetter")
    url = None
    for _ in range(30):
        pg.wait_for_timeout(500)
        url = pg.url
        if "/agreement" in url:
            break
    res["s8_read"] = {"url": url, "errors": errs,
                      "title": pg.evaluate("() => document.title"),
                      "h1": pg.evaluate("() => { const h = document.querySelector('h1'); return h ? h.textContent.slice(0,80) : null; }"),
                      "bodyLen": pg.evaluate("() => document.body.innerText.length")}
    pg.screenshot(path=OUT + "/s8-1920-agreement.png")
    flush()
    ctx.close()

    # (d) W5 hover in bridge view at 390 and 635
    for w in (390, 635):
        ctx = br.new_context(viewport={"width": w, "height": 900})
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(BASE + "/?stage=bridge", wait_until="load")
        pg.wait_for_timeout(5000)
        btn = pg.locator("#fpIntroPlay")
        res[f"w5_{w}"] = {"btnVisible": btn.is_visible(), "btnRect": r(btn)}
        btn.hover(timeout=5000)
        pg.wait_for_timeout(1200)
        tip = pg.evaluate("""() => {
          const els = [...document.querySelectorAll('[class*="tip"], [id*="tip"], .fp-play-tip, [role="tooltip"]')];
          const vis = els.filter(e => { const b = e.getBoundingClientRect(); const cs = getComputedStyle(e); return b.height > 0 && cs.visibility !== 'hidden' && cs.opacity !== '0'; });
          return vis.map(e => ({cls: e.className, text: (e.textContent||'').trim().slice(0,120), rect: (() => { const b = e.getBoundingClientRect(); return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height), bottom: Math.round(b.bottom)}; })()}));
        }""")
        sub = pg.evaluate("""() => { const s = document.querySelector('#fpIntroSub, .fp-intro-sub, [class*="intro-sub"]'); if (!s) return null; const b = s.getBoundingClientRect(); return {text: s.textContent.trim().slice(0,120), y: Math.round(b.y), h: Math.round(b.height)}; }""")
        res[f"w5_{w}"]["tip"] = tip
        res[f"w5_{w}"]["sub"] = sub
        res[f"w5_{w}"]["errors"] = errs
        pg.screenshot(path=OUT + f"/w5-{w}-hover.png")
        ctx.close()
    br.close()

print(json.dumps(res, indent=1)[:12000])
with open(OUT + "/results2.json", "w") as f:
    json.dump(res, f, indent=1)
print("WROTE results2.json")
