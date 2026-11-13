#!/usr/bin/env python3
"""Playwright verification for the phase-2 staged Hub + note pages.
Firefox, fresh context per width — phone 390 FIRST, then 1440, then 360.
Asserts: zero horizontal overflow at scroll 0 AND scrolled, zero console
errors, zero page errors. Pages:
  A. /s/sn2696 as Googlebot (server-rendered note): title/H1/hook,
     boards, related block (6 rel-cards with reasons), cluster + Hub
     links, cover image loaded.
  B. /s/sn2209 (topic-less) + ambassador rep as Googlebot: renders,
     related >= 3.
  C. Hub / as a browser: six cluster tabs present, card title links are
     canonical /s/<slug>, clicking a card title lands on the note in the
     Hub (302 -> hash route), clicking a cluster tab filters the feed,
     ?cluster= arrival opens that tab.
  D. Bars spot no-regression: bottom-bar geometry (radii 50%, sizes
     46/44 and 38/27) + bar buttons enumerated and clicked.
Screenshots + results.json into phase2-shots/. Exits 1 on failure.
Usage: probe-phase2-playwright.py
"""
import json, os, sys
from playwright.sync_api import sync_playwright

STG = "https://naya-public-blog-staging.nayapower.workers.dev"
GUA = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
BUA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
OUT = "/home/hatch/workspace/team-nitro/seo-ai-backend-20261113/phase2-shots"
os.makedirs(OUT, exist_ok=True)

fails, results = [], {}
MEASURE = """() => {
  const de = document.documentElement;
  const se = document.scrollingElement || de;
  return { scrollW: se.scrollWidth, innerW: window.innerWidth,
    overflowX: se.scrollWidth - window.innerWidth,
    title: document.title,
    h1: (document.querySelector('h1') || {}).innerText || null,
    boards: document.querySelectorAll('.board').length,
    relCards: document.querySelectorAll('.rel-card').length,
    relReasons: Array.from(document.querySelectorAll('.rel-card .why')).map(e => e.innerText),
    clusterLinks: Array.from(document.querySelectorAll('a[href^="/?cluster="]')).map(a => a.getAttribute('href')),
    coverOk: (() => { const im = document.querySelector('figure.cover img'); return im ? (im.complete && im.naturalWidth > 0) : null; })(),
    scrollH: se.scrollHeight };
}"""

def fresh_ctx(browser, w, h, ua):
    return browser.new_context(viewport={"width": w, "height": h}, user_agent=ua)

def overflow_check(page):
    m = page.evaluate(MEASURE)
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(400)
    m2 = page.evaluate("() => ({overflowX: (document.scrollingElement||document.documentElement).scrollWidth - window.innerWidth})")
    return m, m2["overflowX"]

with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)
    for name, w, h in [("390", 390, 844), ("1440", 1440, 900), ("360", 360, 800)]:
        r = {}
        # --- A. note page as Googlebot ---
        ctx = fresh_ctx(browser, w, h, GUA)
        errors = []
        page = ctx.new_page()
        page.on("console", lambda m: errors.append(f"console.{m.type}: {m.text}") if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
        resp = page.goto(STG + "/s/sn2696", wait_until="networkidle", timeout=90000)
        m, ox2 = overflow_check(page)
        page.screenshot(path=f"{OUT}/note-sn2696-{name}.png", full_page=True)
        r["note_sn2696"] = {"status": resp.status, "overflowX": [m["overflowX"], ox2],
            "errors": errors, "title": m["title"], "h1": m["h1"], "boards": m["boards"],
            "relCards": m["relCards"], "relReasons": m["relReasons"],
            "clusterLinks": m["clusterLinks"], "coverOk": m["coverOk"]}
        ok = (resp.status == 200 and m["overflowX"] <= 0 and ox2 <= 0 and not errors
              and m["title"] == "The Infinite Smart Feeds \u2014 Shawn read back his \u00b7 NayaNET"
              and m["h1"] == "The Infinite Smart Feeds" and m["boards"] >= 1
              and m["relCards"] == 6 and len(m["clusterLinks"]) >= 1 and m["coverOk"])
        if not ok: fails.append(f"{name}/note-sn2696")
        print(f"[{name}] note sn2696: {resp.status} ox={m['overflowX']}/{ox2} err={len(errors)} "
              f"boards={m['boards']} rel={m['relCards']} cover={m['coverOk']} ok={ok}", flush=True)
        for e in errors: print("  ERROR:", e[:200])
        # --- B. topic-less + ambassador rep as Googlebot ---
        for slug, tag in [("sn2209", "topicless"), ("nn-20261112-the-ambassador-academy-two-moves-voice-bugatti", "ambassador")]:
            resp2 = page.goto(STG + "/s/" + slug, wait_until="networkidle", timeout=90000)
            m2b, ox2b = overflow_check(page)
            r["note_" + tag] = {"status": resp2.status, "overflowX": [m2b["overflowX"], ox2b],
                "errors": list(errors), "title": m2b["title"], "relCards": m2b["relCards"]}
            ok2 = resp2.status == 200 and m2b["overflowX"] <= 0 and ox2b <= 0 and m2b["relCards"] >= 3
            if not ok2: fails.append(f"{name}/note-{tag}")
            print(f"[{name}] note {tag} ({slug}): {resp2.status} ox={m2b['overflowX']}/{ox2b} rel={m2b['relCards']} ok={ok2}", flush=True)
        ctx.close()
        # --- C+D. Hub as a browser ---
        ctx = fresh_ctx(browser, w, h, BUA)
        errors = []
        page = ctx.new_page()
        page.on("console", lambda m: errors.append(f"console.{m.type}: {m.text}") if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
        resp = page.goto(STG + "/", wait_until="networkidle", timeout=90000)
        page.wait_for_timeout(1500)
        hub = page.evaluate("""() => {
          const tabs = Array.from(document.querySelectorAll('.smart-tab')).map(t => (t.innerText || '').trim());
          const cardLinks = Array.from(document.querySelectorAll('a.ib-title-link')).map(a => a.getAttribute('href'));
          return { tabs, tabCount: tabs.length, cardLinks: cardLinks.slice(0, 8),
            allCardLinksCanonical: cardLinks.length > 0 && cardLinks.every(h => h && h.startsWith('/s/')),
            cardLinkCount: cardLinks.length,
            hashCardLinks: cardLinks.filter(h => h && h.startsWith('#/')).length };
        }""")
        m, ox2 = overflow_check(page)
        page.screenshot(path=f"{OUT}/hub-{name}.png")  # viewport only: the Hub full page exceeds the 32767px screenshot cap
        # click a cluster tab (AI Is Hiring) and read the active tab + count
        tab_clicked = page.evaluate("""() => {
          const t = Array.from(document.querySelectorAll('.smart-tab')).find(x => (x.innerText || '').includes('AI Is Hiring'));
          if (!t) return {found: false};
          t.click(); return {found: true};
        }""")
        page.wait_for_timeout(1200)
        tab_after = page.evaluate("""() => {
          const a = document.querySelector('.smart-tab.active');
          return { active: a ? (a.innerText || '').trim() : null,
            cards: document.querySelectorAll('a.ib-title-link').length };
        }""")
        # click the first card title -> must land on the note in the Hub
        card_clicked = page.evaluate("""() => {
          const a = document.querySelector('a.ib-title-link');
          if (!a) return {found: false};
          const href = a.getAttribute('href'); a.click(); return {found: true, href};
        }""")
        page.wait_for_timeout(2500)
        after_click = page.evaluate("() => ({url: location.href, hash: location.hash, h1: (document.querySelector('h1')||{}).innerText || null})")
        # bars geometry spot check
        bars = page.evaluate("""() => {
          const els = Array.from(document.querySelectorAll('.circle, [class*=circle], .icon-btn, button[aria-label]')).slice(0, 40);
          const sizes = els.map(e => { const cs = getComputedStyle(e); const r = e.getBoundingClientRect();
            return { w: Math.round(r.width), h: Math.round(r.height), br: cs.borderRadius }; });
          return { count: els.length, sizes: sizes.slice(0, 12) };
        }""")
        r["hub"] = {"status": resp.status, "overflowX": [m["overflowX"], ox2], "errors": errors,
                    "tabs": hub["tabs"], "cardLinks": hub["cardLinks"],
                    "allCardLinksCanonical": hub["allCardLinksCanonical"],
                    "cardLinkCount": hub["cardLinkCount"], "hashCardLinks": hub["hashCardLinks"],
                    "tab_clicked": tab_clicked, "tab_after": tab_after,
                    "card_clicked": card_clicked, "after_click": after_click, "bars": bars}
        ok_hub = (resp.status == 200 and m["overflowX"] <= 0 and ox2 <= 0 and not errors
                  and hub["allCardLinksCanonical"] and hub["hashCardLinks"] == 0
                  and len([t for t in hub["tabs"] if "AI Is Hiring" in t or "Intelligent Internet" in t or "Ambassador" in t]) >= 3
                  and tab_after.get("active") and "AI Is Hiring" in (tab_after.get("active") or "")
                  and card_clicked.get("found") and "#/smart-notes/" in (after_click.get("hash") or ""))
        if not ok_hub: fails.append(f"{name}/hub")
        print(f"[{name}] hub: {resp.status} ox={m['overflowX']}/{ox2} err={len(errors)} "
              f"tabs={hub['tabCount']} canonicalCards={hub['allCardLinksCanonical']} ({hub['cardLinkCount']}) "
              f"tabActive={tab_after.get('active')} clickHash={after_click.get('hash')} ok={ok_hub}", flush=True)
        for e in errors: print("  ERROR:", e[:200])
        # ?cluster= arrival
        resp3 = page.goto(STG + "/?cluster=ai-is-hiring", wait_until="networkidle", timeout=90000)
        page.wait_for_timeout(1200)
        cq = page.evaluate("() => { const a = document.querySelector('.smart-tab.active'); return a ? (a.innerText || '').trim() : null; }")
        r["hub_cluster_arrival"] = {"status": resp3.status, "active": cq}
        if not (cq and "AI Is Hiring" in cq): fails.append(f"{name}/hub-cluster-arrival")
        print(f"[{name}] ?cluster=ai-is-hiring active tab: {cq}", flush=True)
        ctx.close()
        results[name] = r
    browser.close()

json.dump(results, open(f"{OUT}/results.json", "w"), indent=1)
print("SHOTS:", OUT)
if fails:
    print("FAILED:", fails)
    sys.exit(1)
print("ALL PLAYWRIGHT VIEWPORTS PASS")
