#!/usr/bin/env python3
"""Staged probe for the points round: geometry + fixture harness on the
proof-host links (fresh cb = staged sha). Same measurements as probe-verify.py,
plus: first read whether live data populated on staged (_dashD defined?),
then fixture A/B per page (fresh page each) to prove the staged wiring.
Writes probe-staged-firefox.json + proof-staged-firefox-*.png into this dir.
"""
import json, os
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = ("https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/"
        "points-on-personal-space-business-20261113/%s-points.html"
        "&ref=points/personal-space-business-20261113&cb=%s")
URLS = {
    "personal": BASE % ("personal", "eb0173c99920d28f12e1ad2942b452fcfd170bcbfa920af141da6354db4c8b95"),
    "space": BASE % ("space", "f7eced7b39570f312c9c741805b2ce548d0e31f80ec54dcabcfbaef158aab613"),
    "business": BASE % ("business", "f8c769fb301c0dab6313c6126d07ba71a242df5b5de259c6caac096a6bcc2481"),
}
WIDTHS = [390, 1440, 360]
SELS = ["#pname", "#pointsdisplay", "#ptag", "#cvrbtn", ".ph-cover"]
JS = """
() => {
  const out = {};
  for (const s of %s) {
    const el = document.querySelector(s);
    if (!el) { out[s] = null; continue; }
    const r = el.getBoundingClientRect();
    out[s] = {x: +r.x.toFixed(1), y: +r.y.toFixed(1), w: +r.width.toFixed(1),
              h: +r.height.toFixed(1), top: +r.top.toFixed(1),
              bottom: +r.bottom.toFixed(1), left: +r.left.toFixed(1),
              right: +r.right.toFixed(1)};
  }
  out._doc = {scrollW: document.documentElement.scrollWidth,
              clientW: document.documentElement.clientWidth,
              innerW: window.innerWidth};
  out._pillText = (document.querySelector('#pointscount')||{}).textContent ?? null;
  out._pillCount = document.querySelectorAll('#pointsdisplay').length;
  out._dashD = typeof window._dashD;
  return out;
}
""" % json.dumps(SELS)

def overlap(a, b):
    if not a or not b: return None
    return not (a["right"] <= b["left"] or b["right"] <= a["left"]
                or a["bottom"] <= b["top"] or b["bottom"] <= a["top"])

SETUP_JS = """
(fx) => {
  const mk = (n) => { const out=[]; const now = Date.now();
    for (let i=0;i<n;i++) out.push(new Date(now - i*3600e3).toISOString());
    return out; };
  window._dashD = { postTimes: mk(fx.posts), noteTimes: mk(fx.notes), invTimes: mk(fx.invs),
    msgTimes: mk(fx.msgs), saveTimes: mk(fx.saves), peopleAround: [], peopleList: [] };
  window._dashLinkT = {c: 0, j: fx.joins};
  window._dashClickDayMap = {};
  try { window.osLoadPointsBoard(); } catch(e) { return 'THREW: ' + e; }
  return 'called';
}
"""
FIXTURES = {
    "A": ({"posts": 4, "notes": 2, "invs": 1, "msgs": 3, "saves": 5, "joins": 1}, 245),
    "B": ({"posts": 10, "notes": 0, "invs": 0, "msgs": 0, "saves": 0, "joins": 0}, 250),
}

def main():
    results = {"browser": "firefox", "staged": True, "pages": {}, "harness": {}}
    with sync_playwright() as p:
        browser = p.firefox.launch()
        for page_name, url in URLS.items():
            results["pages"][page_name] = {}
            for w in WIDTHS:
                ctx = browser.new_context(viewport={"width": w, "height": 844})
                page = ctx.new_page()
                errors = []
                page.on("console", lambda m: errors.append(f"{m.type}: {m.text}") if m.type == "error" else None)
                page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
                page.goto(url, wait_until="load", timeout=90000)
                page.wait_for_timeout(5000)
                top = page.evaluate(JS)
                live = page.evaluate("""() => ({
                  dashD: typeof window._dashD,
                  dashD_posts: (window._dashD||{}).postTimes ? window._dashD.postTimes.length : null,
                  pill: document.querySelector('#pointscount').textContent
                })""")
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(800)
                end = page.evaluate(JS)
                page.evaluate("window.scrollTo(0,0)")
                page.wait_for_timeout(300)
                page.screenshot(path=os.path.join(HERE, f"proof-staged-firefox-{page_name}-{w}-top.png"))
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(400)
                page.screenshot(path=os.path.join(HERE, f"proof-staged-firefox-{page_name}-{w}-end.png"))
                pname, pill = top.get("#pname"), top.get("#pointsdisplay")
                same_row = None; gap = None
                if pname and pill:
                    same_row = abs(pill["top"] - pname["top"]) < 8 or (pill["top"] >= pname["top"] and pill["bottom"] <= pname["bottom"] + 8)
                    gap = round(pill["left"] - pname["right"], 1)
                results["pages"][page_name][str(w)] = {
                    "top": top, "end": end, "live": live,
                    "pill_present": pill is not None,
                    "pill_same_row_as_name": same_row, "pill_gap_px": gap,
                    "overflow_px": max(0, top["_doc"]["scrollW"] - top["_doc"]["clientW"]),
                    "cvrbtn_intersects_pname": overlap(pname, top.get("#cvrbtn")),
                    "console_errors": errors[:20], "console_error_count": len(errors),
                }
                print(f"STAGED {page_name} {w}: pname_y={top['#pname']['top']} pill={pill} "
                      f"same_row={same_row} gap={gap} cvrXname={results['pages'][page_name][str(w)]['cvrbtn_intersects_pname']} "
                      f"overflow={results['pages'][page_name][str(w)]['overflow_px']} pillText={top['_pillText']!r} "
                      f"live_dashD={live['dashD']} live_pill={live['pill']!r} errs={len(errors)}")
                ctx.close()
        # staged fixture harness (fresh page per fixture)
        for page_name, url in URLS.items():
            results["harness"][page_name] = {}
            for fx_name, (fx, exp) in FIXTURES.items():
                ctx = browser.new_context(viewport={"width": 1440, "height": 844})
                page = ctx.new_page()
                page.goto(url, wait_until="load", timeout=90000)
                page.wait_for_timeout(4000)
                called = page.evaluate(SETUP_JS, fx)
                r = page.evaluate("""() => ({
                  pill: document.querySelector('#pointscount').textContent,
                  dashD_posts: (window._dashD||{}).postTimes ? window._dashD.postTimes.length : 'NO_DASHD'
                })""")
                results["harness"][page_name][fx_name] = {
                    "fixture": fx, "setup": called, "pill": r["pill"],
                    "expected": exp, "match": r["pill"] == f"{exp:,}",
                    "fixture_intact": r["dashD_posts"] == fx["posts"],
                }
                print(f"STAGED HARNESS {page_name} {fx_name}: pill={r['pill']!r} expected={exp:,} "
                      f"match={r['pill'] == f'{exp:,}'} intact={r['dashD_posts'] == fx['posts']}")
                ctx.close()
        browser.close()
    results["pname_top_spread"] = {}
    for w in WIDTHS:
        tops = {pn: results["pages"][pn][str(w)]["top"]["#pname"]["top"] for pn in URLS}
        results["pname_top_spread"][str(w)] = {"tops": tops,
            "spread_px": round(max(tops.values()) - min(tops.values()), 1)}
    print("pname top spread (staged):", json.dumps(results["pname_top_spread"]))
    out = os.path.join(HERE, "probe-staged-firefox.json")
    with open(out, "w") as f:
        json.dump(results, f, indent=1)
    print("wrote", out)

if __name__ == "__main__":
    main()
