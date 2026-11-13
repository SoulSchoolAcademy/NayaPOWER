#!/usr/bin/env python3
"""Playwright verification for the phase-1 staged note page.
Loads the staged note page as Googlebot (so the worker serves the
server-rendered page, not the Hub 302) at 1440 / 390 / 360 and asserts:
zero horizontal overflow, zero console errors, zero page errors, the
title/H1/hook present in the rendered DOM. Saves screenshots to
phase1-shots/ as the receipt.
Usage: probe-phase1-playwright.py [--proxy http://127.0.0.1:18080]
"""
import json
import os
import sys

from playwright.sync_api import sync_playwright

STG = "https://naya-public-blog-staging.nayapower.workers.dev/s/sn2696"
GUA = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
OUT = "/home/hatch/workspace/team-nitro/public-blog-seo-20261112/phase1-shots"
os.makedirs(OUT, exist_ok=True)

proxy = None
if "--proxy" in sys.argv:
    proxy = {"server": sys.argv[sys.argv.index("--proxy") + 1]}

fails = []
results = {}
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-gpu"])
    for name, w, h in [("1440", 1440, 900), ("390", 390, 844), ("360", 360, 800)]:
        ctx = browser.new_context(viewport={"width": w, "height": h},
                                  user_agent=GUA, proxy=proxy)
        errors = []
        page = ctx.new_page()
        page.on("console", lambda m: errors.append(f"console.{m.type}: {m.text}") if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
        resp = page.goto(STG, wait_until="networkidle", timeout=60000)
        m = page.evaluate("""() => {
          const de = document.documentElement;
          const se = document.scrollingElement || de;
          return {
            scrollW: se.scrollWidth, clientW: de.clientWidth, innerW: window.innerWidth,
            overflowX: se.scrollWidth - window.innerWidth,
            title: document.title,
            h1: (document.querySelector('h1') || {}).innerText || null,
            hook: (document.querySelector('.nutshell') || {}).innerText || null,
            boards: document.querySelectorAll('.board').length,
            scrollH: se.scrollHeight
          };
        }""")
        page.screenshot(path=f"{OUT}/note-{name}.png", full_page=True)
        # scrolled check too: scroll to bottom and re-measure
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(400)
        m2 = page.evaluate("() => ({overflowX: (document.scrollingElement||document.documentElement).scrollWidth - window.innerWidth})")
        ok_overflow = m["overflowX"] <= 0 and m2["overflowX"] <= 0
        ok_errors = len(errors) == 0
        ok_title = m["title"] == "The Infinite Smart Feeds — one feed per topic · NayaNET"
        ok_h1 = m["h1"] == "The Infinite Smart Feeds"
        ok_hook = m["hook"] and "Not one feed like Facebook" in m["hook"]
        ok_boards = m["boards"] == 7
        results[name] = {"status": resp.status, "metrics": m, "scrolled_overflowX": m2["overflowX"],
                         "errors": errors, "overflow_ok": ok_overflow, "errors_ok": ok_errors,
                         "title_ok": ok_title, "h1_ok": ok_h1, "hook_ok": ok_hook,
                         "boards_ok": ok_boards, "boards": m["boards"]}
        print(f"[{name}] HTTP {resp.status} overflowX={m['overflowX']}/{m2['overflowX']} "
              f"errors={len(errors)} boards={m['boards']} title_ok={ok_title} h1_ok={ok_h1} hook_ok={ok_hook}")
        if errors:
            for e in errors:
                print(f"  ERROR: {e[:200]}")
        if not (ok_overflow and ok_errors and ok_title and ok_h1 and ok_hook and ok_boards):
            fails.append(name)
        ctx.close()
    browser.close()

json.dump(results, open(f"{OUT}/results.json", "w"), indent=1)
print("SHOTS:", OUT)
if fails:
    print("FAILED viewports:", fails)
    sys.exit(1)
print("ALL PLAYWRIGHT VIEWPORTS PASS: zero overflow, zero console errors")
