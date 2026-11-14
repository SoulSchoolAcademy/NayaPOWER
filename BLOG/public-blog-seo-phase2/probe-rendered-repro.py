#!/usr/bin/env python3
"""Rendered-layer repro probe (maker seat, Step 0) for the SEO/AI
rendered fix round. Fresh Firefox context per load, phone 390 FIRST.
Reproduces R1-R6 on the STAGED link as a browser sees it:
  R1 related cards on /s/sn2696 (browser UA -> 302 -> SPA note view)
  R2 sn2766 by feed click AND direct /s/sn2766
  R3 sn2695 by feed click AND direct /s/sn2695
  R4 feed snapshot across 3 consecutive fresh home loads
  R5 blank loads (0 elements) across the battery
  R6 black gap below the article footer on note pages
Also measures the BAKED snapshot (feed-live.json blocked) so the
stale-snapshot grounding is a number, not a guess.
Writes probe-rendered-repro-results.json + screenshots to phase2-shots-rendered/.
Usage: probe-rendered-repro.py
"""
import json, os, sys
from playwright.sync_api import sync_playwright

STG = "https://naya-public-blog-staging.nayapower.workers.dev"
BUA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
OUT = "/home/hatch/workspace/team-nitro/seo-ai-backend-20261113/phase2-shots-rendered"
os.makedirs(OUT, exist_ok=True)

SNAP = """() => {
  const fi = window.NayaFeedIntelligence || {};
  const notes = fi.notes || [];
  const cards = Array.from(document.querySelectorAll('a.ib-title-link'));
  const h1 = document.querySelector('h1');
  const bodyTxt = document.body ? document.body.innerText : '';
  return {
    url: location.href, hash: location.hash,
    title: document.title,
    bodyElements: document.body ? document.body.querySelectorAll('*').length : 0,
    feedRef: fi.ref || null, feedCount: notes.length,
    firstNote: notes.length ? (notes[0].title || notes[0].id) : null,
    cardLinks: cards.length,
    firstCard: cards.length ? (cards[0].innerText || '').trim().slice(0, 80) : null,
    hasSn2766Card: cards.some(a => (a.getAttribute('href') || '').includes('sn2766')),
    hasSn2695Card: cards.some(a => (a.getAttribute('href') || '').includes('sn2695')),
    h1: h1 ? h1.innerText : null,
    relCards: document.querySelectorAll('.rel-card').length,
    relatedText: bodyTxt.includes('Related in this cluster'),
    relatedWord: (bodyTxt.match(/RELATED/g) || []).length,
    sLinks: Array.from(document.querySelectorAll('a[href^="/s/"]')).map(a => a.getAttribute('href')),
    noteLoading: !!document.querySelector('.note-loading'),
    notFound: bodyTxt.includes('That note isn'),
    scrollH: (document.scrollingElement || document.documentElement).scrollHeight,
    innerH: window.innerHeight,
  };
}"""

GAP = """() => {
  const se = document.scrollingElement || document.documentElement;
  const els = Array.from(document.querySelectorAll('body *')).filter(e => {
    const r = e.getBoundingClientRect();
    return r.height > 0 && r.width > 0;
  });
  let bottom = 0, what = null;
  for (const e of els) {
    const b = e.getBoundingClientRect().bottom + window.scrollY;
    if (b > bottom) { bottom = b; what = e.tagName + '.' + (e.className && e.className.baseVal === undefined ? String(e.className).split(' ')[0] : ''); }
  }
  return { scrollH: se.scrollHeight, lastBottom: Math.round(bottom),
           gapPx: Math.round(se.scrollHeight - bottom), lowestEl: what };
}"""

results = {}
fails = []

def fresh(browser, w=390, h=844):
    ctx = browser.new_context(viewport={"width": w, "height": h}, user_agent=BUA)
    return ctx

with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)

    # --- R4: three consecutive fresh home loads, 390 ---
    snaps = []
    for i in range(3):
        ctx = fresh(browser)
        errors = []
        page = ctx.new_page()
        page.on("console", lambda m: errors.append(f"console.{m.type}: {m.text}") if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
        page.goto(STG + "/", wait_until="domcontentloaded", timeout=90000)
        page.wait_for_timeout(1000)
        early = page.evaluate(SNAP)
        page.wait_for_timeout(6000)
        late = page.evaluate(SNAP)
        snaps.append({"early": early, "late": late, "errors": errors})
        print(f"[R4 load {i+1}] early ref={early['feedRef']} n={early['feedCount']} first={str(early['firstNote'])[:50]!r} "
              f"-> late ref={late['feedRef']} n={late['feedCount']} first={str(late['firstNote'])[:50]!r} "
              f"cards={late['cardLinks']} blank={late['bodyElements']==0} err={len(errors)}", flush=True)
        if i == 0:
            page.screenshot(path=f"{OUT}/home-390.png")
        ctx.close()
    results["R4_fresh_loads"] = snaps

    # --- Baked snapshot: block /feed-live.json, read the bake ---
    ctx = fresh(browser)
    page = ctx.new_page()
    page.route("**/feed-live.json", lambda route: route.abort())
    page.goto(STG + "/", wait_until="domcontentloaded", timeout=90000)
    page.wait_for_timeout(4000)
    baked = page.evaluate(SNAP)
    print(f"[BAKED] ref={baked['feedRef']} n={baked['feedCount']} first={str(baked['firstNote'])[:60]!r} cards={baked['cardLinks']}", flush=True)
    results["baked_snapshot"] = baked
    ctx.close()

    # --- R1/R6: /s/sn2696 as a browser ---
    ctx = fresh(browser)
    errors = []
    page = ctx.new_page()
    page.on("console", lambda m: errors.append(f"console.{m.type}: {m.text}") if m.type == "error" else None)
    page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
    page.goto(STG + "/s/sn2696", wait_until="domcontentloaded", timeout=90000)
    page.wait_for_timeout(8000)
    m = page.evaluate(SNAP)
    gap = page.evaluate(GAP)
    page.screenshot(path=f"{OUT}/note-sn2696-390.png", full_page=True)
    print(f"[R1 sn2696] url={m['url']} h1={m['h1']!r} relCards={m['relCards']} relatedText={m['relatedText']} "
          f"sLinks={len(m['sLinks'])} feedRef={m['feedRef']} n={m['feedCount']} gap={gap['gapPx']}px lowest={gap['lowestEl']} err={len(errors)}", flush=True)
    for e in errors: print("  ERROR:", e[:200])
    results["R1_sn2696"] = {"snap": m, "gap": gap, "errors": errors}
    ctx.close()

    # --- R2: /s/sn2766 direct, sampled over time ---
    ctx = fresh(browser)
    errors = []
    page = ctx.new_page()
    page.on("console", lambda m: errors.append(f"console.{m.type}: {m.text}") if m.type == "error" else None)
    page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
    page.goto(STG + "/s/sn2766", wait_until="domcontentloaded", timeout=90000)
    samples = []
    for t in (2, 8, 15):
        page.wait_for_timeout((t - (samples[-1][0] if samples else 0)) * 1000 if samples else t * 1000)
        s = page.evaluate(SNAP)
        samples.append((t, s))
        print(f"[R2 sn2766 direct t={t}s] loading={s['noteLoading']} notFound={s['notFound']} h1={str(s['h1'])[:50]!r} "
              f"relCards={s['relCards']} feedRef={s['feedRef']} n={s['feedCount']}", flush=True)
    page.screenshot(path=f"{OUT}/note-sn2766-390.png", full_page=True)
    results["R2_sn2766_direct"] = {"samples": [{"t": t, **s} for t, s in samples], "errors": errors}
    ctx.close()

    # --- R3: /s/sn2695 direct, sampled over time ---
    ctx = fresh(browser)
    errors = []
    page = ctx.new_page()
    page.on("console", lambda m: errors.append(f"console.{m.type}: {m.text}") if m.type == "error" else None)
    page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
    page.goto(STG + "/s/sn2695", wait_until="domcontentloaded", timeout=90000)
    samples = []
    for t in (2, 8, 15):
        page.wait_for_timeout((t - (samples[-1][0] if samples else 0)) * 1000 if samples else t * 1000)
        s = page.evaluate(SNAP)
        samples.append((t, s))
        print(f"[R3 sn2695 direct t={t}s] loading={s['noteLoading']} notFound={s['notFound']} h1={str(s['h1'])[:50]!r} "
              f"relCards={s['relCards']} feedRef={s['feedRef']} n={s['feedCount']}", flush=True)
    page.screenshot(path=f"{OUT}/note-sn2695-390.png", full_page=True)
    results["R3_sn2695_direct"] = {"samples": [{"t": t, **s} for t, s in samples], "errors": errors}
    ctx.close()

    # --- R2/R3 feed click: home, find sn2766 + sn2695 cards, click each ---
    for slug in ("sn2766", "sn2695"):
        ctx = fresh(browser)
        errors = []
        page = ctx.new_page()
        page.on("console", lambda m: errors.append(f"console.{m.type}: {m.text}") if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
        page.goto(STG + "/", wait_until="domcontentloaded", timeout=90000)
        page.wait_for_timeout(7000)
        before = page.evaluate(SNAP)
        clicked = page.evaluate("""(slug) => {
          const a = Array.from(document.querySelectorAll('a.ib-title-link')).find(x => (x.getAttribute('href') || '').includes(slug));
          if (!a) return {found: false};
          a.click(); return {found: true, href: a.getAttribute('href')};
        }""", slug)
        page.wait_for_timeout(6000)
        after = page.evaluate(SNAP)
        print(f"[FEED-CLICK {slug}] feed n={before['feedCount']} first={str(before['firstNote'])[:40]!r} "
              f"clicked={clicked} -> loading={after['noteLoading']} notFound={after['notFound']} h1={str(after['h1'])[:50]!r} rel={after['relCards']}", flush=True)
        page.screenshot(path=f"{OUT}/feedclick-{slug}-390.png", full_page=True)
        results[f"feed_click_{slug}"] = {"before": before, "clicked": clicked, "after": after, "errors": errors}
        ctx.close()

    browser.close()

json.dump(results, open(f"{OUT}/probe-rendered-repro-results.json", "w"), indent=1)
print("RESULTS:", OUT + "/probe-rendered-repro-results.json")
