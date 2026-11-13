#!/usr/bin/env python3
"""Re-verify the pill restyle locally (Playwright Firefox, localhost serve).
Checks: pill place (beside name / wraps below at phone), tiled digits when the
wiring value is simulated, gauge fill = dialPos(total)/500, no overlap or
clipping, and no regression on the seven items (spot-check). Writes
verify-pill.json + screenshots pill-{390,1440,360}-top.png.
The wiring write is simulated by setting #pointscount textContent — the same
write the points wiring performs — so the observer + tiler path is exercised.
"""
import json, threading, http.server, functools
from playwright.sync_api import sync_playwright

LANE = "/home/hatch/workspace/personal-complete-wt/TEAM-NITRO/personal-page-complete-20261113"
OUT = "/home/hatch/workspace/team-nitro/personal-page-complete-20261113"

def box(page, sel):
    el = page.query_selector(sel)
    if not el: return None
    b = el.bounding_box()
    if not b: return None
    return {"x": round(b["x"], 1), "y": round(b["y"], 1), "w": round(b["width"], 1), "h": round(b["height"], 1)}

def run():
    class H(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 8137), functools.partial(H, directory=LANE))
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    res = {"widths": {}}
    with sync_playwright() as p:
        b = p.firefox.launch()
        for w in (390, 1440, 360):
            pg = b.new_page(viewport={"width": w, "height": 844})
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            d = {"viewport": w}
            pg.goto("http://127.0.0.1:8137/personal-complete.html", wait_until="load")
            pg.wait_for_timeout(3500)
            d["overflowX"] = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            d["pageerrors"] = errs
            # pill place (before any simulation — the loading state)
            d["pill_loading"] = box(pg, "#pointsdisplay")
            d["pill_text_loading"] = pg.evaluate("(document.getElementById('pointscount')||{}).textContent")
            d["name"] = box(pg, "#pname")
            d["cvrbtn"] = box(pg, "#cvrbtn")
            d["tagline"] = box(pg, "#ptag")
            # simulate the wiring write: total 1293 (the Dashboard's live value)
            pg.evaluate("() => { var pc = document.getElementById('pointscount'); pc.textContent = (1293).toLocaleString(); }")
            pg.wait_for_timeout(600)
            d["pill_1293"] = box(pg, "#pointsdisplay")
            d["tiles_1293"] = pg.evaluate("() => Array.from(document.querySelectorAll('#pointscount .os-mini-tile')).map(t => ({cls: t.className, digit: (t.querySelector('.rd')||{}).textContent}))")
            d["gaps_1293"] = pg.evaluate("() => document.querySelectorAll('#pointscount .os-mini-gap').length")
            d["gauge_1293"] = pg.evaluate("() => { var f = document.getElementById('pcPillGaugeFill'); return f ? f.style.width : null; }")
            d["tile_border_d1"] = pg.evaluate("() => { var t = document.querySelector('#pointscount .os-mini-tile.d1'); return t ? getComputedStyle(t).borderColor : null; }")
            d["tile_border_d9"] = pg.evaluate("() => { var t = document.querySelector('#pointscount .os-mini-tile.d9'); return t ? getComputedStyle(t).borderColor : null; }")
            # overlap checks: pill vs name, pill vs tagline, pill vs cover btn
            d["overlap"] = pg.evaluate("""() => {
                function r(s){ var e=document.querySelector(s); if(!e) return null; var b=e.getBoundingClientRect(); return {x:b.x,y:b.y,w:b.width,h:b.height}; }
                function ov(a,b){ return a && b && a.x < b.x+b.w && b.x < a.x+a.w && a.y < b.y+b.h && b.y < a.y+a.h; }
                var pill=r('#pointsdisplay'), name=r('#pname'), tag=r('#ptag'), cvr=r('#cvrbtn'), gear=r('#settingsbtn');
                return {pill_vs_name: ov(pill,name), pill_vs_tagline: ov(pill,tag), pill_vs_cvrbtn: ov(pill,cvr), pill_vs_gear: ov(pill,gear)};
            }""")
            # fallback 0, then back to loading glyph
            pg.evaluate("() => { var pc = document.getElementById('pointscount'); pc._pcLastDigits = null; pc.textContent = '0'; }")
            pg.wait_for_timeout(400)
            d["tiles_0"] = pg.evaluate("() => Array.from(document.querySelectorAll('#pointscount .os-mini-tile')).map(t => t.className)")
            d["gauge_0"] = pg.evaluate("() => { var f = document.getElementById('pcPillGaugeFill'); return f ? f.style.width : null; }")
            # regression spot-checks
            btns = {}
            for bid in ("msgbtn", "aboutbtn", "myworldbtn", "skillsbtn", "connbtn", "growthbtn", "sharebtn", "joinbtn"):
                btns[bid] = box(pg, "#" + bid)
            d["buttons_equal"] = (max(v["w"] for v in btns.values() if v) - min(v["w"] for v in btns.values() if v) <= 2)
            d["segs"] = pg.evaluate("() => Array.from(document.querySelectorAll('.notif-seg')).map(e => e.getAttribute('data-notif'))")
            d["seg_shadow"] = pg.evaluate("() => { const s=document.querySelector('.notif-seg'); return s ? getComputedStyle(s).boxShadow : 'none'; }")
            d["tabs"] = pg.evaluate("() => Array.from(document.querySelectorAll('#mwFeedTabs .lens-tab')).map(e => (e.innerText||'').trim())")
            d["rail_cards"] = pg.evaluate("() => document.querySelectorAll('#pcRailList .pc-card').length")
            d["rail_imgs"] = pg.evaluate("() => document.querySelectorAll('#pcRail img').length")
            d["gear_text"] = pg.evaluate("(document.getElementById('settingsbtn')||{}).textContent")
            pg.evaluate("() => window.scrollTo(0, 0)"); pg.wait_for_timeout(300)
            pg.screenshot(path=f"{OUT}/pill-{w}-top.png")
            res["widths"][w] = d
            pg.close()
        b.close()
    with open(f"{OUT}/verify-pill.json", "w") as f:
        json.dump(res, f, indent=1)
    print("wrote verify-pill.json")

if __name__ == "__main__":
    run()
