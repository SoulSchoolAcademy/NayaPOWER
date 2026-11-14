#!/usr/bin/env python3
"""Grounding experiment 2 (maker seat, Step 1): the live-feed race.
Delays /feed-live.json by N seconds via Playwright routing and records
what the app shows: does the feed stay on the 381-note bake? Does a
direct note load spin, resolve, or give up? Also measures the R6 gap
properly (in-flow elements only; fixed bars excluded).
Writes probe-grounding2-results.json to phase2-shots-rendered/.
"""
import json, os, time
from playwright.sync_api import sync_playwright

STG = "https://naya-public-blog-staging.nayapower.workers.dev"
BUA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
OUT = "/home/hatch/workspace/team-nitro/seo-ai-backend-20261113/phase2-shots-rendered"

SNAP = """() => {
  const fi = window.NayaFeedIntelligence || {};
  return { url: location.href, feedRef: fi.ref || null, feedCount: (fi.notes || []).length,
    firstNote: (fi.notes || []).length ? ((fi.notes[0].title || fi.notes[0].id)) : null,
    bodyElements: document.body ? document.body.querySelectorAll('*').length : 0,
    loading: !!document.querySelector('.note-loading'),
    notFound: document.body ? document.body.innerText.includes('That note isn') : false,
    h1: (document.querySelector('h1') || {}).innerText || null };
}"""

GAP = """() => {
  const se = document.scrollingElement || document.documentElement;
  // in-flow elements only: exclude fixed/sticky (the bottom bar) so the
  // void below the article footer is measured, not the chrome.
  const els = Array.from(document.querySelectorAll('body *')).filter(e => {
    const cs = getComputedStyle(e);
    if (cs.position === 'fixed' || cs.position === 'sticky') return false;
    const r = e.getBoundingClientRect();
    return r.height > 0 && r.width > 0;
  });
  let bottom = 0, what = null;
  for (const e of els) {
    const b = e.getBoundingClientRect().bottom + window.scrollY;
    if (b > bottom) { bottom = b; what = e.tagName + '.' + String(e.className && e.className.baseVal === undefined ? e.className : '').split(' ')[0]; }
  }
  const nv = document.querySelector('.note-view');
  const nvr = nv ? nv.getBoundingClientRect() : null;
  const main = document.querySelector('.main');
  const app = document.getElementById('app');
  return { scrollH: se.scrollHeight, lastInFlowBottom: Math.round(bottom), lowestEl: what,
    gapPx: Math.round(se.scrollHeight - bottom),
    noteViewBottom: nvr ? Math.round(nvr.bottom + window.scrollY) : null,
    noteViewH: nvr ? Math.round(nvr.height) : null,
    mainMinH: main ? getComputedStyle(main).minHeight : null,
    mainPadBottom: main ? getComputedStyle(main).paddingBottom : null,
    appH: app ? Math.round(app.getBoundingClientRect().height) : null,
    bodyH: Math.round(document.body.getBoundingClientRect().height) };
}"""

results = {}
with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)

    # --- A. feed-live.json delayed 3s: home + direct note ---
    for delay, tag in ((3, "delay3"), (20, "delay20")):
        ctx = browser.new_context(viewport={"width": 390, "height": 844}, user_agent=BUA)
        page = ctx.new_page()
        def slow(route, request=None, delay=delay):
            time.sleep(delay)
            route.continue_()
        page.route("**/feed-live.json", slow)
        page.goto(STG + "/", wait_until="domcontentloaded", timeout=90000)
        samples = []
        for t in (2, 6, 12, 20, 40, 70):
            prev = samples[-1][0] if samples else 0
            page.wait_for_timeout((t - prev) * 1000)
            s = page.evaluate(SNAP)
            samples.append((t, s))
            print(f"[{tag} home t={t}s] ref={s['feedRef']} n={s['feedCount']} first={str(s['firstNote'])[:40]!r}", flush=True)
            if s['feedCount'] == 1058:
                break
        results[f"home_{tag}"] = [{"t": t, **s} for t, s in samples]
        ctx.close()

        # direct note under the same delay
        ctx = browser.new_context(viewport={"width": 390, "height": 844}, user_agent=BUA)
        page = ctx.new_page()
        page.route("**/feed-live.json", slow)
        page.goto(STG + "/s/sn2766", wait_until="domcontentloaded", timeout=90000)
        samples = []
        for t in (2, 6, 12, 20, 40, 70):
            prev = samples[-1][0] if samples else 0
            page.wait_for_timeout((t - prev) * 1000)
            s = page.evaluate(SNAP)
            samples.append((t, s))
            print(f"[{tag} sn2766 t={t}s] loading={s['loading']} notFound={s['notFound']} ref={s['feedRef']} n={s['feedCount']}", flush=True)
            if s['notFound']:
                break
        results[f"sn2766_{tag}"] = [{"t": t, **s} for t, s in samples]
        ctx.close()

    # --- B. R6 gap measurement on sn2696, scrolled to bottom ---
    ctx = browser.new_context(viewport={"width": 390, "height": 844}, user_agent=BUA)
    page = ctx.new_page()
    page.goto(STG + "/s/sn2696", wait_until="domcontentloaded", timeout=90000)
    page.wait_for_timeout(8000)
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(800)
    gap = page.evaluate(GAP)
    print("[R6 gap]", json.dumps(gap), flush=True)
    page.screenshot(path=f"{OUT}/note-sn2696-390-scrolled-bottom.png")
    # which element owns the bottom of the page? list the 5 lowest in-flow boxes
    lowest = page.evaluate("""() => {
      const els = Array.from(document.querySelectorAll('body *')).filter(e => {
        const cs = getComputedStyle(e);
        if (cs.position === 'fixed' || cs.position === 'sticky') return false;
        const r = e.getBoundingClientRect(); return r.height > 0 && r.width > 0;
      });
      return els.map(e => ({ tag: e.tagName, cls: String(e.className && e.className.baseVal === undefined ? e.className : '').split(' ')[0],
        bottom: Math.round(e.getBoundingClientRect().bottom + window.scrollY),
        h: Math.round(e.getBoundingClientRect().height) }))
        .sort((a, b) => b.bottom - a.bottom).slice(0, 8);
    }""")
    print("[R6 lowest in-flow]", json.dumps(lowest), flush=True)
    results["R6_gap"] = {"gap": gap, "lowest": lowest}
    ctx.close()
    browser.close()

json.dump(results, open(f"{OUT}/probe-grounding2-results.json", "w"), indent=1)
print("RESULTS:", OUT + "/probe-grounding2-results.json")
