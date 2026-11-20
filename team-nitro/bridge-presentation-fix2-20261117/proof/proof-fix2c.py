#!/usr/bin/env python3
"""Follow-up probe C: deck drive to beat 9, §8 READ, W5 hover in bridge view.
Per-section try/except + incremental flush so one failure loses nothing."""
import json, sys
sys.path.insert(0, "/tmp/fix2")
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8899"
OUT = "/tmp/fix2/proof"
res = {}
try:
    res = json.load(open(OUT + "/results2.json"))
except Exception:
    pass

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

    # ---------- (1) deck drive ----------
    try:
        ctx = br.new_context(viewport={"width": 1920, "height": 900})
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(BASE + "/?stage=deck", wait_until="load")
        pg.wait_for_timeout(5000)
        struct = pg.evaluate("""() => {
          const arts = [...document.querySelectorAll('#deckBody article[data-beat]')].map(a => {
            const b = a.getBoundingClientRect();
            const cs = getComputedStyle(a);
            return {beat: a.getAttribute('data-beat'), vis: b.height > 0 && cs.display !== 'none',
                    y: Math.round(b.y), h: Math.round(b.height)};
          });
          const nexts = [...document.querySelectorAll('#deckBody .deck-next, #fpDeckNext, #deckBody [class*="next"]')].map(e => {
            const b = e.getBoundingClientRect();
            return {sel: e.id ? '#'+e.id : e.className, text: (e.textContent||'').trim().slice(0,40),
                    vis: b.height > 0, y: Math.round(b.y)};
          });
          const state = window.__fpStage ? window.__fpStage.state : null;
          return {arts, nexts, state};
        }""")
        res["deckStruct"] = struct
        # try advancing: click the visible article's next control, then #fpNextBtn, then figure
        steps = []
        for attempt, sel in (("deck-next", "#deckBody .deck-next"),
                             ("fpDeckNext", "#fpDeckNext"),
                             ("fpNextBtn", "#fpNextBtn")):
            try:
                pg.click(sel, timeout=2500)
                pg.wait_for_timeout(900)
            except Exception as ex:
                steps.append({attempt: "click failed: " + str(ex)[:100]})
                continue
            st = pg.evaluate("() => window.__fpStage ? window.__fpStage.state.deck : null")
            steps.append({attempt: "deck=" + str(st)})
            if st and st >= 8:
                break
        res["deckAdvanceSteps"] = steps
        cur = pg.evaluate("""() => {
          const vis = [...document.querySelectorAll('#deckBody article[data-beat]')].filter(a => a.getBoundingClientRect().height > 0).map(a => a.getAttribute('data-beat'));
          const img9 = document.querySelector('#deckBody article[data-beat="9"] figure.lb-showcase img');
          return {visibleBeats: vis, deck: window.__fpStage ? window.__fpStage.state.deck : null,
                  img9src: img9 ? img9.getAttribute('src').slice(0, 80) : null};
        }""")
        res["deckAfterAdvance"] = cur
        res["deckErrors"] = errs
        pg.screenshot(path=OUT + "/w4-1920-deck9b.png")
        # deckBack at the reached beat
        back = pg.locator("#fpDeckBack")
        res["deckBackFinal"] = {"hidden": back.is_hidden(), "rect": r(back),
                                "deckBefore": pg.evaluate("() => window.__fpStage ? window.__fpStage.state.deck : null")}
        back.click(timeout=5000)
        pg.wait_for_timeout(1500)
        res["deckBackFinal_after"] = pg.evaluate("() => document.body.className")
        pg.screenshot(path=OUT + "/deckback-1920-bridge2.png")
        ctx.close()
    except Exception as ex:
        res["deckDriveError"] = str(ex)[:500]
    flush()

    # ---------- (2) §8 READ ----------
    try:
        ctx = br.new_context(viewport={"width": 1920, "height": 900})
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(BASE + "/?stage=bridge", wait_until="load")
        pg.wait_for_timeout(5000)
        for btn in ("#fpBridgeMore1", "#fpBridgeMore2", "#fpBridgeMore3", "#fpBridgeMore4"):
            try:
                pg.click(btn, timeout=3000)
                pg.wait_for_timeout(1000)
            except Exception as ex:
                res.setdefault("s8_read_clicks", []).append(f"{btn} FAILED: {ex}"[:200])
        pg.evaluate("document.querySelector('#fpBridge').scrollTop = 999999")
        pg.wait_for_timeout(800)
        pg.click("#fpBridgeLetter", timeout=5000)
        url = None
        for _ in range(30):
            pg.wait_for_timeout(500)
            url = pg.url
            if "/agreement" in url:
                break
        pg.wait_for_timeout(1500)
        res["s8_read"] = {"url": url, "errors": errs,
                          "title": pg.evaluate("() => document.title"),
                          "h1": pg.evaluate("() => { const h = document.querySelector('h1'); return h ? h.textContent.slice(0, 80) : null; }"),
                          "bodyLen": pg.evaluate("() => document.body.innerText.length"),
                          "beats": pg.evaluate("() => document.querySelectorAll('[data-beat], article').length")}
        pg.screenshot(path=OUT + "/s8-1920-agreement.png")
        ctx.close()
    except Exception as ex:
        res["s8_read_error"] = str(ex)[:500]
    flush()

    # ---------- (3) W5 hover in bridge view ----------
    for w in (390, 635):
        try:
            ctx = br.new_context(viewport={"width": w, "height": 900})
            pg = ctx.new_page()
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto(BASE + "/?stage=bridge", wait_until="load")
            pg.wait_for_timeout(5000)
            btn = pg.locator("#fpIntroPlay")
            d = {"btnVisible": btn.is_visible(), "btnRect": r(btn)}
            btn.hover(timeout=5000)
            pg.wait_for_timeout(1200)
            d["tip"] = pg.evaluate("""() => {
              const els = [...document.querySelectorAll('[class*="tip"], [id*="tip"], .fp-play-tip, [role="tooltip"]')];
              const vis = els.filter(e => { const b = e.getBoundingClientRect(); const cs = getComputedStyle(e);
                return b.height > 0 && cs.visibility !== 'hidden' && cs.opacity !== '0'; });
              return vis.map(e => ({cls: String(e.className).slice(0,60), text: (e.textContent||'').trim().slice(0,140),
                rect: (() => { const b = e.getBoundingClientRect(); return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height), bottom: Math.round(b.bottom)}; })()}));
            }""")
            d["sub"] = pg.evaluate("""() => { const s = document.querySelector('#fpIntroSub, .fp-intro-sub, [class*="intro-sub"]');
              if (!s) return null; const b = s.getBoundingClientRect();
              return {text: s.textContent.trim().slice(0,140), y: Math.round(b.y), h: Math.round(b.height)}; }""")
            d["errors"] = errs
            res[f"w5_{w}"] = d
            pg.screenshot(path=OUT + f"/w5-{w}-hover.png")
            ctx.close()
        except Exception as ex:
            res[f"w5_{w}_error"] = str(ex)[:500]
        flush()
    br.close()

print(json.dumps({k: res[k] for k in res if k in ("deckStruct", "deckAdvanceSteps", "deckAfterAdvance", "deckBackFinal", "deckBackFinal_after", "s8_read", "w5_390", "w5_635") or "Error" in k or "error" in k}, indent=1)[:9000])
print("FLUSHED results2.json")
