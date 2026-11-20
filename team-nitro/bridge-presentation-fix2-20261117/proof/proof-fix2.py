#!/usr/bin/env python3
"""Live proof for bridge presentation FIX #2 against the LOCAL mirror
(http://127.0.0.1:8899 serving the fix2 bytes). The staging worker
currently serves the agreement-merge bytes (8aad1e5c), so staging is NOT
deployed for this round — see MAKER-REPORT.md. The mirror serves the
fix2 welcome (b1d4b16d) + the presentation walk/identity + the 842cae53
unfold + the KV emblem PNGs, byte-identical to what the worker will serve.

Parts: D1 returning flow, D2 ?stage= landings, D3 emblem geometry,
D4 legal strip vs bar + max-scroll Continue, W1/W2/W4/W5/deck-end-back,
§8 READ/VISUAL. Screenshots to /tmp/fix2/proof/.
"""
import json, os, sys
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8899"
OUT = "/tmp/fix2/proof"
os.makedirs(OUT, exist_ok=True)

def rect_js(sel):
    return ("(s=>{const e=document.querySelector(s);if(!e)return null;"
            "const b=e.getBoundingClientRect();return{x:Math.round(b.x),y:Math.round(b.y),"
            "w:Math.round(b.width),h:Math.round(b.height),right:Math.round(b.right),"
            "bottom:Math.round(b.bottom)}})(%r)" % sel)

def overlap(a, b):
    if not a or not b:
        return 0
    x = max(0, min(a["right"], b["right"]) - max(a["x"], b["x"]))
    y = max(0, min(a["bottom"], b["bottom"]) - max(a["y"], b["y"]))
    return x * y

def overlap_xy(a, b):
    if not a or not b:
        return (0, 0)
    x = max(0, min(a["right"], b["right"]) - max(a["x"], b["x"]))
    y = max(0, min(a["bottom"], b["bottom"]) - max(a["y"], b["y"]))
    return (x, y)

results = {}

with sync_playwright() as p:
    browser = p.chromium.launch(
        proxy={"server": "http://127.0.0.1:18080", "bypass": "127.0.0.1,localhost"},
        args=["--no-sandbox"])

    # ---------------- D1: returning-user flow (1920) ----------------
    ctx = browser.new_context(viewport={"width": 1920, "height": 900})
    ctx.add_init_script("""
      localStorage.setItem('nayanet_smart_alias', 'captaineyecheck');
      localStorage.setItem('nayanet_smart_name', 'Captain Eye');
      localStorage.setItem('nayanet_smart_identities', JSON.stringify([
        {alias:'captaineyecheck', name:'captaineyecheck'},
        {alias:'captaineyecheck', name:'Captain Eye'},
        {alias:'alexwalker', name:'alexwalker'},
        {alias:'alexwalker', name:'Alex Walker'}
      ]));
    """)
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(BASE + "/", wait_until="load", timeout=60000)
    pg.wait_for_timeout(6000)
    d1 = pg.evaluate("""() => {
      const q = s => document.querySelector(s);
      const qa = s => Array.from(document.querySelectorAll(s));
      const vis = el => { if (!el) return null; const b = el.getBoundingClientRect();
        return {hidden: el.hidden, w: Math.round(b.width), h: Math.round(b.height)}; };
      return {
        form: vis(q('#entryForm')),
        returningView: vis(q('#returningView')),
        jumpBackIn: q('#jumpBackIn') ? {text: q('#jumpBackIn').textContent.trim(),
          vis: vis(q('#jumpBackIn'))} : null,
        orbitChildren: q('#nayaColorOrbit') ? q('#nayaColorOrbit').children.length : null,
        othersRows: qa('#returningOthersList .returning-other-row').map(r => ({
          alias: r.getAttribute('data-alias'),
          text: r.textContent.trim().slice(0, 60)})),
        othersBoxHidden: q('#returningOthers') ? q('#returningOthers').hidden : null,
        stored: JSON.parse(localStorage.getItem('nayanet_smart_identities') || '[]')
      }; }""")
    d1["pageerrors"] = errs
    results["D1"] = d1
    print("D1:", json.dumps(d1))
    pg.screenshot(path=OUT + "/d1-1920-returning.png")
    pg.close(); ctx.close()

    # ---------------- D2: ?stage= landings at 1920/635/390 ----------------
    d2 = {}
    for w in (1920, 635, 390):
        for stage, expect in (("deck", "fp-view-deck"), ("letter", "fp-view-letterpage"),
                              ("bridge", "fp-view-bridge")):
            ctx = browser.new_context(viewport={"width": w, "height": 900})
            pg = ctx.new_page()
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto(BASE + "/?stage=" + stage, wait_until="load", timeout=60000)
            pg.wait_for_timeout(5000)
            cls = pg.evaluate("document.querySelector('#fpAgreement').className")
            d2[f"{w}/{stage}"] = {"class": cls, "landed": expect in cls, "errors": errs}
            pg.close(); ctx.close()
    results["D2"] = d2
    print("D2:", json.dumps(d2))

    # ---------------- D3 + D4: bridge geometry at 1920/635/390 ----------------
    for w in (1920, 635, 390):
        ctx = browser.new_context(viewport={"width": w, "height": 900})
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(BASE + "/?stage=bridge", wait_until="load", timeout=60000)
        pg.wait_for_timeout(6000)
        g = pg.evaluate("""() => {
          const r = s => { const e = document.querySelector(s); if (!e) return null;
            const b = e.getBoundingClientRect();
            return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width),
                    h: Math.round(b.height), right: Math.round(b.right),
                    bottom: Math.round(b.bottom)}; };
          return {
            head: r('.fp-agree-head'), kicker: r('.fp-agree-kicker'),
            title: r('.fp-agree-title'), sub: r('.fp-agree-sub'),
            logoImg: r('.fp-agree-logo img'),
            emblems: Array.from(document.querySelectorAll('.fp-bridge-emblem'))
              .map(e => ({cls: e.className.split(' ').pop(), rect: r('.' + e.className.split(' ').pop())})),
            legal: r('#fpLegal'), legalLinks: r('#fpLegal .fp-legal-links'),
            barB: r('#fpStageBarB'), nextBtn: r('#fpNextBtn'),
            bridge: r('#fpBridge'),
            view: document.querySelector('#fpAgreement').className,
            vw: innerWidth, vh: innerHeight
          }; }""")
        kicker = g["kicker"]
        d3 = {}
        for e in g["emblems"]:
            d3[e["cls"]] = {"rect": e["rect"],
                            "kickerOverlapXY": overlap_xy(e["rect"], kicker),
                            "clipped": e["rect"]["x"] < 0 or e["rect"]["right"] > w}
        d4 = {"legalH": g["legal"]["h"], "legal": g["legal"],
              "legalLinksH": g["legalLinks"]["h"],
              "barB": g["barB"],
              "nextBtn": g["nextBtn"],
              "nextBtnVsStripXY": overlap_xy(g["nextBtn"], g["legal"]),
              "barBottomVsStripTop": g["barB"]["bottom"] - g["legal"]["y"],
              "bridge": g["bridge"]}
        results[f"D3-{w}"] = d3
        results[f"D4-{w}-top"] = d4
        print(f"D3-{w}:", json.dumps(d3))
        print(f"D4-{w}-top:", json.dumps(d4), "errors:", errs)
        pg.screenshot(path=OUT + f"/d3-{w}-bridge-top.png")

        # D4 max scroll: click through Continues to the final page, then scroll to bottom
        for btn in ("#fpBridgeMore1", "#fpBridgeMore2", "#fpBridgeMore3", "#fpBridgeMore4"):
            try:
                pg.click(btn, timeout=3000)
                pg.wait_for_timeout(1200)
            except Exception as ex:
                print(f"  {w} click {btn} failed: {ex}")
        pg.evaluate("document.querySelector('#fpBridge').scrollTop = 999999")
        pg.wait_for_timeout(2000)
        bot = pg.evaluate("""() => {
          const r = s => { const e = document.querySelector(s); if (!e) return null;
            const b = e.getBoundingClientRect();
            return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width),
                    h: Math.round(b.height), right: Math.round(b.right),
                    bottom: Math.round(b.bottom), hidden: e.hidden}; };
          const br = document.querySelector('#fpBridge');
          return { legal: r('#fpLegal'), barB: r('#fpStageBarB'), nextBtn: r('#fpNextBtn'),
            final: r('#fpBridgeFinal'), more4: r('#fpBridgeMore4'),
            bridgeScroll: {top: br.scrollTop, max: br.scrollHeight - br.clientHeight},
            deckBtn: r('#fpBridgeDeck'), letterBtn: r('#fpBridgeLetter') }; }""")
        bot["nextBtnVsStripXY"] = overlap_xy(bot["nextBtn"], bot["legal"])
        if bot["final"]:
            bot["finalVsStripXY"] = overlap_xy(bot["final"], bot["legal"])
            bot["finalVsBarXY"] = overlap_xy(bot["final"], bot["barB"])
        results[f"D4-{w}-maxscroll"] = bot
        print(f"D4-{w}-maxscroll:", json.dumps(bot))
        pg.screenshot(path=OUT + f"/d4-{w}-bridge-bottom.png")
        pg.close(); ctx.close()

    # ---------------- §3 spot: W1/W2/W4/W5/deck-end-back/§8 (1920 + phones) ----------------
    ctx = browser.new_context(viewport={"width": 1920, "height": 900})
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(BASE + "/?stage=bridge", wait_until="load", timeout=60000)
    pg.wait_for_timeout(6000)
    w1 = pg.evaluate("""() => {
      const b = document.querySelector('#fpBridge');
      const r = b.getBoundingClientRect();
      let depth = 0, el = b;
      while (el && el.id !== 'fpAgreement') { depth++; el = el.parentElement; }
      return {rect: {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)},
              depthToAgreement: depth, display: getComputedStyle(b).display,
              overflowY: getComputedStyle(b).overflowY}; }""")
    results["W1"] = w1
    print("W1:", json.dumps(w1), "errors:", errs)
    # W2: scroll bridge to bottom
    w2 = pg.evaluate("""() => { const br = document.querySelector('#fpBridge');
      br.scrollTop = 999999; return {top: br.scrollTop, max: br.scrollHeight - br.clientHeight}; }""")
    pg.wait_for_timeout(1500)
    w2b = pg.evaluate("""() => { const br = document.querySelector('#fpBridge');
      return {top: br.scrollTop, max: br.scrollHeight - br.clientHeight,
              finalVisible: !!document.querySelector('#fpBridgeFinal') &&
                document.querySelector('#fpBridgeFinal').getBoundingClientRect().height > 0}; }""")
    results["W2"] = {"scroll": w2, "after": w2b}
    print("W2:", json.dumps({"scroll": w2, "after": w2b}))
    pg.close(); ctx.close()

    # W4 + deck-end back + §8 VISUAL, at 1920
    ctx = browser.new_context(viewport={"width": 1920, "height": 900})
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(BASE + "/?stage=deck", wait_until="load", timeout=60000)
    pg.wait_for_timeout(6000)
    w4 = pg.evaluate("""() => {
      const q = s => document.querySelector(s);
      const img1 = q('#deckBody article[data-beat="1"] figure.lb-showcase img');
      const img9 = q('#deckBody article[data-beat="9"] figure.lb-showcase img');
      return { view: document.querySelector('#fpAgreement').className,
        slide1: img1 ? img1.getAttribute('src') : null,
        slide9: img9 ? img9.getAttribute('src') : null,
        tapTip: !!Array.from(document.querySelectorAll('.lb-showcase')).length }; }""")
    results["W4-deck1"] = w4
    print("W4-deck1:", json.dumps(w4), "errors:", errs)
    pg.screenshot(path=OUT + "/w4-1920-deck1.png")
    # jump to beat 9 via the deck next buttons
    for i in range(8):
        try:
            pg.click("#deckBody .deck-next, #fpDeckNext", timeout=2000)
        except Exception:
            pass
        pg.wait_for_timeout(700)
    beat = pg.evaluate("document.querySelector('#fpAgreement').className + '|' + (window.__fpStage ? window.__fpStage.state.view + ':' + window.__fpStage.state.deck : '')")
    print("after 8x next:", beat)
    pg.screenshot(path=OUT + "/w4-1920-deck9.png")
    back = pg.evaluate("""() => { const b = document.querySelector('#fpDeckBack');
      if (!b) return null; const r = b.getBoundingClientRect();
      return {hidden: b.hidden, rect: {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width)}}; }""")
    print("deckBack:", json.dumps(back))
    try:
        pg.click("#fpDeckBack", timeout=3000)
        pg.wait_for_timeout(3000)
        results["deckEndBack"] = pg.evaluate("document.querySelector('#fpAgreement').className")
        print("deck-end back ->", results["deckEndBack"])
    except Exception as ex:
        results["deckEndBack"] = "CLICK FAILED: %s" % ex
        print("deck-end back click failed:", ex)
    pg.close(); ctx.close()

    # §8: bridge final page VISUAL -> deck; then READ -> /agreement
    ctx = browser.new_context(viewport={"width": 1920, "height": 900})
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(BASE + "/?stage=bridge", wait_until="load", timeout=60000)
    pg.wait_for_timeout(6000)
    for btn in ("#fpBridgeMore1", "#fpBridgeMore2", "#fpBridgeMore3", "#fpBridgeMore4"):
        try:
            pg.click(btn, timeout=3000); pg.wait_for_timeout(1200)
        except Exception as ex:
            print("§8 click", btn, "failed:", ex)
    pg.evaluate("document.querySelector('#fpBridge').scrollTop = 999999")
    pg.wait_for_timeout(1500)
    s8 = pg.evaluate("""() => { const q = s => document.querySelector(s);
      const r = s => { const e = q(s); if (!e) return null; const b = e.getBoundingClientRect();
        return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height)}; };
      return {deckBtn: r('#fpBridgeDeck'), letterBtn: r('#fpBridgeLetter')}; }""")
    print("§8 bridge choices:", json.dumps(s8))
    try:
        pg.click("#fpBridgeDeck", timeout=3000)
        pg.wait_for_timeout(3000)
        s8v = pg.evaluate("document.querySelector('#fpAgreement').className")
        results["S8-VISUAL"] = s8v
        print("§8 VISUAL ->", s8v)
        pg.click("#fpDeckBack", timeout=3000)
        pg.wait_for_timeout(2500)
        for btn in ("#fpBridgeMore1", "#fpBridgeMore2", "#fpBridgeMore3", "#fpBridgeMore4"):
            try:
                pg.click(btn, timeout=2000); pg.wait_for_timeout(800)
            except Exception:
                pass
        pg.evaluate("document.querySelector('#fpBridge').scrollTop = 999999")
        pg.wait_for_timeout(1200)
        with pg.expect_navigation(url="**/agreement", timeout=10000):
            pg.click("#fpBridgeLetter", timeout=3000)
        results["S8-READ"] = pg.url
        print("§8 READ ->", pg.url)
    except Exception as ex:
        results["S8"] = "FAILED: %s" % ex
        print("§8 failed:", ex)
    print("§8 errors:", errs)
    pg.close(); ctx.close()

    # W5: play tip below button (hover) at 390 and 635
    for w in (390, 635):
        ctx = browser.new_context(viewport={"width": w, "height": 900})
        pg = ctx.new_page()
        pg.goto(BASE + "/", wait_until="load", timeout=60000)
        pg.wait_for_timeout(6000)
        try:
            pg.hover("#fpIntroPlay", timeout=3000)
            pg.wait_for_timeout(2500)
            w5 = pg.evaluate("""() => { const q = s => document.querySelector(s);
              const r = s => { const e = q(s); if (!e) return null; const b = e.getBoundingClientRect();
                return {y: Math.round(b.y), bottom: Math.round(b.bottom), h: Math.round(b.height)}; };
              const tip = q('.p3-play-tip');
              return {btn: r('#fpIntroPlay'), tip: r('.p3-play-tip'),
                      tipText: tip ? tip.textContent.trim() : null,
                      tipVisible: tip ? getComputedStyle(tip).display : null,
                      sub: r('.fp-agree-sub')}; }""")
            results[f"W5-{w}"] = w5
            print(f"W5-{w}:", json.dumps(w5))
            pg.screenshot(path=OUT + f"/w5-{w}-play-hover.png")
        except Exception as ex:
            results[f"W5-{w}"] = "FAILED: %s" % ex
            print(f"W5-{w} failed:", ex)
        pg.close(); ctx.close()

    browser.close()

print("ERRORS-CHECK: D1 pageerrors =", results["D1"]["pageerrors"])
json.dump(results, open("/tmp/fix2/proof/results.json", "w"), indent=1)
print("DONE")
