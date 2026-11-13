#!/usr/bin/env python3
"""Hub Slug Resolution — Step 6 walked-entrance proof (Playwright Firefox).

Fresh browser profile per width (no dismissed-modal state, no stored login).
390px FIRST, then 1440, then 360.
Per width:
  1. Start at the LIVE login page https://nayanet.app/ (the entrance a fresh
     visitor meets; the staging worker carries no login page — it serves the
     Hub shell directly at /). Record the entrance, click "Enter NayaNET".
  2. From the entered page, follow the staged deep link with a REAL anchor
     click (an <a href=".../s/sn2696"> appended and clicked in-page — the
     same navigation a shared-link click performs), in the same fresh session.
     Never start the browser already sitting on the hash route.
  3. Measure: URL, title, "That note isn't here" absent, hook present,
     boards, install-overlay presence at first paint (~800 ms) and at +3s/+6s,
     console/page errors, horizontal overflow at scroll 0 and scrolled.
  4. Full-id control (#/smart-notes/IB-...) at 390, same session.
Screenshots -> this work dir.
"""
import json, sys
from playwright.sync_api import sync_playwright

WD = "/home/hatch/workspace/team-nitro/hub-slug-resolution-20261113"
STAGING = "https://naya-public-blog-staging.nayapower.workers.dev"
FULL_ID = "IB-SMART-NOTE-20261112-the-infinite-smart-feeds"
NOTE_TITLE = "SN-2696 \u00b7 SYSTEM / INTELLIGENCE / FEEDS"
HOOK = "Not one feed like Facebook"

results = {}

def measure_note(pg, label):
    pg.wait_for_timeout(3500)
    data = pg.evaluate("""() => {
      const txt = document.body.innerText || '';
      const ov = document.querySelector('.naya-install-overlay');
      return {
        url: location.href,
        title: document.title,
        notHere: txt.includes("That note isn't here") || txt.includes('Note not found'),
        hook: txt.includes("Not one feed like Facebook"),
        hubTitle: txt.includes("SN-2696"),
        boards: document.querySelectorAll('.intel-board, [class*=board]').length,
        overlayShown: !!(ov && ov.classList.contains('show')),
        overlayVisible: !!(ov && getComputedStyle(ov).display !== 'none' && ov.getBoundingClientRect().height > 50),
        scrollW: document.documentElement.scrollWidth,
        innerW: window.innerWidth,
        h2s: [...document.querySelectorAll('h2')].map(e => e.innerText.trim().slice(0, 40))
      };
    }""")
    # scrolled overflow
    pg.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    pg.wait_for_timeout(800)
    scrolled = pg.evaluate("({scrollW: document.documentElement.scrollWidth, innerW: window.innerWidth})")
    pg.evaluate("window.scrollTo(0, 0)")
    data["overflow_scroll0"] = data["scrollW"] - data["innerW"]
    data["overflow_scrolled"] = scrolled["scrollW"] - scrolled["innerW"]
    print(f"  [{label}] url={data['url']}")
    print(f"  [{label}] title={data['title']!r} notHere={data['notHere']} hook={data['hook']} hubTitle={data['hubTitle']} boards~{data['boards']} overlayShown={data['overlayShown']} overlayVisible={data['overlayVisible']} overflow0={data['overflow_scroll0']} overflowScrolled={data['overflow_scrolled']}")
    print(f"  [{label}] h2s={data['h2s']}")
    return data

def run_width(pw, width, height):
    print(f"== WIDTH {width} ==")
    browser = pw.firefox.launch(headless=True)
    ctx = browser.new_context(viewport={"width": width, "height": height})
    pg = ctx.new_page()
    console_errors, page_errors = [], []
    pg.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: page_errors.append(str(e)))
    r = {"width": width, "console_errors": console_errors, "page_errors": page_errors}
    # 1. entrance (live login page)
    pg.goto("https://nayanet.app/", timeout=60000)
    pg.wait_for_timeout(3000)
    r["entrance_url"] = pg.url
    r["entrance_title"] = pg.title()
    r["entrance_text"] = (pg.evaluate("document.body.innerText.slice(0,300)") or "").replace("\n", " | ")
    print(f"  entrance: {r['entrance_url']} title={r['entrance_title']!r} text={r['entrance_text']!r}")
    pg.screenshot(path=f"{WD}/proof-entrance-{width}.png")
    # walk in: the entrance is a name-only form (input #userName, required).
    # Fill a clearly-test name and submit, the way a fresh visitor would.
    # (Recorded first-hand: the served entrance form has NO action and NO
    # submit handler — submitting reloads the same entrance. That is a live
    # finding, named in the record, not worked around.)
    try:
        pg.fill("#userName", "Probe Visitor", timeout=8000)
        pg.click("text=Enter NayaNET", timeout=8000)
        print("  filled name + clicked Enter NayaNET")
    except Exception as e:
        print(f"  Enter walk FAILED: {e}")
        r["enter_click"] = "FAILED"
    pg.wait_for_timeout(3000)
    r["after_enter_url"] = pg.url
    r["after_enter_title"] = pg.title()
    r["after_enter_text"] = (pg.evaluate("document.body.innerText.slice(0,400)") or "").replace("\n", " | ")
    print(f"  after Enter: {r['after_enter_url']} title={r['after_enter_title']!r}")
    print(f"  after Enter text: {r['after_enter_text']!r}")
    pg.screenshot(path=f"{WD}/proof-after-enter-{width}.png")
    # 2. follow the staged deep link with a real anchor click
    pg.evaluate("""(href) => {
      const a = document.createElement('a');
      a.href = href; a.textContent = 'staged note link';
      document.body.appendChild(a); a.click();
    }""", STAGING + "/s/sn2696")
    try:
        pg.wait_for_url("**#/smart-notes/sn2696", timeout=30000)
    except Exception as e:
        print(f"  wait for hash FAILED: {e}; url now {pg.url}")
    pg.wait_for_timeout(800)
    # first-paint modal check (~800ms after DOMContentLoaded is past; check ASAP + at +3s)
    r["firstpaint_overlay"] = pg.evaluate("""() => {
      const ov = document.querySelector('.naya-install-overlay');
      return ov ? {shown: ov.classList.contains('show'), display: getComputedStyle(ov).display} : null;
    }""")
    print(f"  first-paint overlay: {r['firstpaint_overlay']}")
    pg.screenshot(path=f"{WD}/proof-note-firstpaint-{width}.png")
    r["note"] = measure_note(pg, f"deep link {width}")
    pg.screenshot(path=f"{WD}/proof-note-{width}.png")
    pg.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    pg.wait_for_timeout(600)
    pg.screenshot(path=f"{WD}/proof-note-scrolled-{width}.png")
    pg.evaluate("window.scrollTo(0, 0)")
    # 3. full-id control (390 only, same session)
    if width == 390:
        pg.goto(STAGING + "/#/smart-notes/" + FULL_ID, timeout=60000)
        r["control"] = measure_note(pg, "full-id control 390")
        pg.screenshot(path=f"{WD}/proof-note-fullid-390.png")
    r["console_errors"] = list(console_errors)
    r["page_errors"] = list(page_errors)
    print(f"  console errors: {len(console_errors)} page errors: {len(page_errors)}")
    browser.close()
    return r

with sync_playwright() as pw:
    for w, h in [(390, 844), (1440, 900), (360, 800)]:
        results[str(w)] = run_width(pw, w, h)

json.dump(results, open(WD + "/proof-results.json", "w"), indent=2, default=str)
print("PROOF DONE — results in proof-results.json")
