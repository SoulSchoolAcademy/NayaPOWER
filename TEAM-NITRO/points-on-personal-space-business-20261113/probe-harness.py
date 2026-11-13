#!/usr/bin/env python3
"""Fixture harness for the points round (v2 — fresh page per fixture).
Live Supabase data cannot load in this VM (CORS blocks on direct Supabase
calls from file:// — the same limit the brief names), so the wiring is proven
with a fixture window._dashD of exactly the shape the live loader builds,
plus window._dashLinkT. A fresh page per fixture avoids the page's own
data path (which retries for ~15s and, when Supabase stays unreachable,
eventually re-renders with empty data) clobbering the fixture mid-read.
For each fixture:
  (1) pill text == the donut total computed by the page's own code path
      (recomputed independently here from the page's own exposed LD_NODES
      value table over the fixture counts);
  (2) the pill text CHANGES when the fixture changes (wired, not printed);
  (3) with the spine built (window.osBuildSpine, as the live data path does),
      the pill STILL equals the donut total while the big number
      (#os-se-val) sweeps toward the doubled spine score — the two numbers
      are named separately, never conflated.
Writes probe-harness.json into this dir.
"""
import json, os
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = {
    "personal": os.path.join(HERE, "personal-points.html"),
    "space": os.path.join(HERE, "space-points.html"),
    "business": os.path.join(HERE, "business-points.html"),
}

FIXTURES = {
    # A: 4 posts, 2 notes, 1 invite, 3 msgs, 5 saves, 1 link join.
    # donut total = 4*25 + 2*35 + 1*25 + 1*50 = 245 (the saves node has no
    # tkey/map in LD_NODES, so saves contribute 0 to the donut total).
    # spine score = 2*(100+70+25+25+50) = 540.
    "A": {"posts": 4, "notes": 2, "invs": 1, "msgs": 3, "saves": 5, "joins": 1,
          "donut": 245, "spine": 540},
    # B: 10 posts only -> donut total 250, spine 500 (pill must CHANGE A->B).
    "B": {"posts": 10, "notes": 0, "invs": 0, "msgs": 0, "saves": 0, "joins": 0,
          "donut": 250, "spine": 500},
    # C: genuinely new citizen, all zero -> donut total 0, pill "0", spine 0.
    "C": {"posts": 0, "notes": 0, "invs": 0, "msgs": 0, "saves": 0, "joins": 0,
          "donut": 0, "spine": 0},
}

SETUP_JS = """
(fx) => {
  const mk = (n) => { const out=[]; const now = Date.now();
    for (let i=0;i<n;i++) out.push(new Date(now - i*3600e3).toISOString());
    return out; };
  window._dashD = {
    postTimes: mk(fx.posts), noteTimes: mk(fx.notes), invTimes: mk(fx.invs),
    msgTimes: mk(fx.msgs), saveTimes: mk(fx.saves),
    peopleAround: [], peopleList: []
  };
  window._dashLinkT = {c: 0, j: fx.joins};
  window._dashClickDayMap = {};
  try { window.osLoadPointsBoard(); } catch(e) { return 'THREW: ' + e; }
  return 'called';
}
"""

READ_JS = """
() => ({
  pill: document.querySelector('#pointscount').textContent,
  pillCount: document.querySelectorAll('#pointsdisplay').length,
  dashD_posts: (window._dashD||{}).postTimes ? window._dashD.postTimes.length : 'NO_DASHD',
  bigNum: document.querySelector('#os-se-val').textContent,
  dashTotal: document.querySelector('#os-dash-total').textContent,
  donutWrapExists: !!document.getElementById('os-donut-wrap'),
  nodes: (window.LD_NODES || []).map(n => ({key: n.key, value: n.value, tkey: n.tkey || null, map: n.map || null}))
})
"""

SPINE_JS = """
() => {
  try {
    const s = window.osBuildSpine(window._dashD);
    window._osSpine = s;
    window.osLoadPointsBoard();
    return {spineScore: s.score, deltas: s.deltas || null};
  } catch(e) { return {error: String(e)}; }
}
"""

def expected_total(nodes, fx):
    counts = {"posts": fx["posts"], "notes": fx["notes"], "invs": fx["invs"],
              "saves": fx["saves"], "joins": fx["joins"]}
    total = 0
    for n in nodes:
        if n["tkey"]:
            key = {"postTimes": "posts", "noteTimes": "notes", "invTimes": "invs",
                   "saveTimes": "saves", "msgTimes": "msgs"}[n["tkey"]]
            c = counts.get(key, 0)
        elif n["map"] == "j":
            c = counts["joins"]
        elif n["map"] == "c":
            c = 0
        else:
            c = 0
        total += (n["value"] or 0) * c if n["value"] else c
    return total

def main():
    results = {"harness": "fixture window._dashD, fresh page per fixture (live Supabase blocked by CORS in this VM)",
               "pages": {}}
    with sync_playwright() as p:
        browser = p.firefox.launch()
        for page_name, path in FILES.items():
            results["pages"][page_name] = {}
            for fx_name, fx in FIXTURES.items():
                ctx = browser.new_context(viewport={"width": 1440, "height": 844})
                page = ctx.new_page()
                errs = []
                page.on("pageerror", lambda e: errs.append(str(e)))
                page.goto("file://" + path, wait_until="load", timeout=60000)
                page.wait_for_timeout(3000)
                called = page.evaluate(SETUP_JS, fx)
                r0 = page.evaluate(READ_JS)  # immediate read, fixture intact
                exp = expected_total(r0["nodes"], fx)
                page.wait_for_timeout(1000)
                r1 = page.evaluate(READ_JS)  # stability read 1s later
                spine = page.evaluate(SPINE_JS)  # simulate the live spine landing
                page.wait_for_timeout(500)
                r2 = page.evaluate(READ_JS)  # pill after spine lands
                rec = {
                    "fixture": {k: fx[k] for k in ("posts", "notes", "invs", "msgs", "saves", "joins")},
                    "setup": called,
                    "pill_t0": r0["pill"], "pill_t1s": r1["pill"],
                    "fixture_intact_at_read": r0["dashD_posts"] == fx["posts"],
                    "expected_donut_total": exp,
                    "expected_donut_total_fmt": f"{exp:,}",
                    "brief_expected_donut_total": fx["donut"],
                    "pill_equals_donut_total": r0["pill"] == f"{exp:,}",
                    "pill_stable_1s": r0["pill"] == r1["pill"],
                    "spine_simulation": spine,
                    "brief_expected_spine": fx["spine"],
                    "spine_matches_brief_expectation": spine.get("spineScore") == fx["spine"],
                    "pill_after_spine_lands": r2["pill"],
                    "pill_unchanged_by_spine": r2["pill"] == r0["pill"],
                    "big_number_mid_sweep": r2["bigNum"],
                    "dash_total_counts": r0["dashTotal"],
                    "donut_wrap_exists": r0["donutWrapExists"],
                    "pageerrors": errs[:5],
                }
                results["pages"][page_name][fx_name] = rec
                print(f"{page_name} {fx_name}: pill t0={r0['pill']!r} t1s={r1['pill']!r} "
                      f"expected={exp:,} match={rec['pill_equals_donut_total']} "
                      f"spine={spine} pill_after_spine={r2['pill']!r} "
                      f"bigNum(mid-sweep)={r2['bigNum']!r} dashTotal={r0['dashTotal']!r}")
                ctx.close()
        browser.close()
    out = os.path.join(HERE, "probe-harness.json")
    with open(out, "w") as f:
        json.dump(results, f, indent=1)
    print("wrote", out)

if __name__ == "__main__":
    main()
