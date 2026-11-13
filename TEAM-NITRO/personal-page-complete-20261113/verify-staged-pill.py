#!/usr/bin/env python3
"""Staged re-verification of the pill restyle on the proof host.
Fresh cb per width (commit sha + width nonce). Checks the pill (place, tiles,
gauge, no overlap/clipping) + regression spot-checks on the seven items.
Writes verify-staged-pill.json + screenshots staged-pill-{390,1440,360}.png.
"""
import json
from playwright.sync_api import sync_playwright

COMMIT = "1aa9275834f2333d92184643dd399f2f292404c7"
BASE = ("https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/"
        "personal-page-complete-20261113/personal-complete.html"
        "&ref=personal/personal-page-complete-20261113")
OUT = "/home/hatch/workspace/team-nitro/personal-page-complete-20261113"

def box(page, sel):
    el = page.query_selector(sel)
    if not el: return None
    b = el.bounding_box()
    if not b: return None
    return {"x": round(b["x"], 1), "y": round(b["y"], 1), "w": round(b["width"], 1), "h": round(b["height"], 1)}

def run():
    res = {"staged_sha": "ec5c4cce083708fa6ea301da45e8097e35174cdffc8216910c8953f70b4ba281",
           "commit": COMMIT, "widths": {}, "console": {}}
    with sync_playwright() as p:
        b = p.firefox.launch()
        for w in (390, 1440, 360):
            errs, perrs = [], []
            pg = b.new_page(viewport={"width": w, "height": 844})
            pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            pg.on("pageerror", lambda e: perrs.append(str(e)))
            d = {"viewport": w}
            try:
                pg.goto(BASE + "&cb=" + COMMIT + "-pill-w" + str(w), wait_until="load")
                pg.wait_for_timeout(4000)
                d["overflowX"] = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
                d["pill_loading"] = box(pg, "#pointsdisplay")
                d["pill_text_loading"] = pg.evaluate("(document.getElementById('pointscount')||{}).textContent")
                d["name"] = box(pg, "#pname")
                d["tagline"] = box(pg, "#ptag")
                # simulate the wiring write (same write the points wiring performs)
                pg.evaluate("() => { var pc = document.getElementById('pointscount'); pc.textContent = (1293).toLocaleString(); }")
                pg.wait_for_timeout(600)
                d["pill_1293"] = box(pg, "#pointsdisplay")
                d["tiles_1293"] = pg.evaluate("() => Array.from(document.querySelectorAll('#pointscount .os-mini-tile')).map(t => t.className)")
                d["gaps_1293"] = pg.evaluate("() => document.querySelectorAll('#pointscount .os-mini-gap').length")
                d["gauge_1293"] = pg.evaluate("() => { var f = document.getElementById('pcPillGaugeFill'); return f ? f.style.width : null; }")
                d["tile_border_d1"] = pg.evaluate("() => { var t = document.querySelector('#pointscount .os-mini-tile.d1'); return t ? getComputedStyle(t).borderColor : null; }")
                d["overlap"] = pg.evaluate("""() => {
                    function r(s){ var e=document.querySelector(s); if(!e) return null; var b=e.getBoundingClientRect(); return {x:b.x,y:b.y,w:b.width,h:b.height}; }
                    function ov(a,b){ return a && b && a.x < b.x+b.w && b.x < a.x+a.w && a.y < b.y+b.h && b.y < a.y+a.h; }
                    var pill=r('#pointsdisplay'), name=r('#pname'), tag=r('#ptag'), cvr=r('#cvrbtn'), gear=r('#settingsbtn');
                    return {pill_vs_name: ov(pill,name), pill_vs_tagline: ov(pill,tag), pill_vs_cvrbtn: ov(pill,cvr), pill_vs_gear: ov(pill,gear)};
                }""")
                # regression spot-checks
                btns = {}
                for bid in ("msgbtn", "aboutbtn", "myworldbtn", "skillsbtn", "connbtn", "growthbtn", "sharebtn", "joinbtn"):
                    btns[bid] = box(pg, "#" + bid)
                d["buttons_equal"] = (max(v["w"] for v in btns.values() if v) - min(v["w"] for v in btns.values() if v) <= 2)
                d["segs"] = pg.evaluate("() => Array.from(document.querySelectorAll('.notif-seg')).map(e => e.getAttribute('data-notif'))")
                d["seg_shadow"] = pg.evaluate("() => { const s=document.querySelector('.notif-seg'); return s ? getComputedStyle(s).boxShadow : 'none'; }")
                d["tabs"] = pg.evaluate("() => Array.from(document.querySelectorAll('#mwFeedTabs .lens-tab')).map(e => (e.innerText||'').trim())")
                d["feedline"] = pg.evaluate("(() => { const e=document.querySelector('.pc-feedline'); return e ? e.textContent.trim() : null; })()")
                d["rail_cards"] = pg.evaluate("() => document.querySelectorAll('#pcRailList .pc-card').length")
                d["rail_imgs"] = pg.evaluate("() => document.querySelectorAll('#pcRail img').length")
                pg.evaluate("() => window.scrollTo(0, 0)"); pg.wait_for_timeout(300)
                pg.screenshot(path=f"{OUT}/staged-pill-{w}.png")
            except Exception as e:
                d["error"] = str(e)
            res["widths"][w] = d
            res["console"][w] = {"errors": len(errs), "pageerrors": perrs}
            pg.close()
        b.close()
    with open(f"{OUT}/verify-staged-pill.json", "w") as f:
        json.dump(res, f, indent=1)
    print("wrote verify-staged-pill.json")

if __name__ == "__main__":
    run()
