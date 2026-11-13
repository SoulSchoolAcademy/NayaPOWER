#!/usr/bin/env python3
"""NAMES PAGE 10/10 rendered probe — presentation measurements, by doing.
Loads the EDITED walk file from a local static server (the staged deploy is
STOPPED by the deploy-order warning: the Q10 probe has not run, so no PUT),
jumps to #step-names via the DOM (showStep lives inside the walk IIFE;
wireNames already ran at boot), and measures RENDERED values at 1440/390/360:
column, gaps, padding, font sizes, getComputedStyle color/opacity on EVERY
visible text node, rest-vs-hover light per card, eye modals, card-click
focus, live slug typing, hero-button advance, overflow + console/page errors.
Usage: python3 names-probe.py   (prints PASS/FAIL lines; writes names-results.json)
"""
import http.server
import functools
import json
import os
import re
import socketserver
import threading

from playwright.sync_api import sync_playwright

D = "/home/hatch/workspace/team-nitro/walk-questions-10-20261112"
OUT = "/home/hatch/workspace/team-nitro/walk-names-page-10-20261112"
SHOTS = os.path.join(OUT, "names-probe-shots")
os.makedirs(SHOTS, exist_ok=True)

BOARD = {"personal": "rgb(160, 107, 255)", "business": "rgb(47, 232, 158)",
         "space": "rgb(255, 191, 61)"}
WHITE = "rgb(255, 255, 255)"

results = {"checks": [], "fails": []}


def check(name, ok, detail=""):
    results["checks"].append({"name": name, "pass": bool(ok), "detail": str(detail)})
    print(("PASS " if ok else "FAIL ") + name + ((" — " + str(detail)) if detail else ""))
    if not ok:
        results["fails"].append(name)


def start_server():
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=D)
    srv = socketserver.TCPServer(("127.0.0.1", 0), h)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, srv.server_address[1]


JS_SHOW_NAMES = """() => {
  document.querySelectorAll('.p3-step').forEach(s => s.hidden = true);
  const n = document.getElementById('step-names');
  n.hidden = false;
  window.scrollTo(0, 0);
  return {visible: !n.hidden, cards: document.querySelectorAll('.p3-namecard').length};
}"""

JS_MEASURE = """(w) => {
  const out = {};
  const sec = document.getElementById('step-names');
  const main = sec.querySelector('.p3-main');
  out.colW = main.getBoundingClientRect().width;
  const cards = [...sec.querySelectorAll('.p3-namecard')];
  out.gap = getComputedStyle(sec.querySelector('.p3-namecards')).rowGap;
  out.gapPx = cards.length > 1 ? Math.round(cards[1].getBoundingClientRect().top - cards[0].getBoundingClientRect().bottom) : null;
  out.pad = cards.map(c => getComputedStyle(c).paddingTop);
  out.nameFs = cards.map(c => getComputedStyle(c.querySelector('.p3-nc-input')).fontSize);
  out.urlFs = cards.map(c => getComputedStyle(c.querySelector('.p3-nc-urlinput')).fontSize);
  out.prefixFs = [...sec.querySelectorAll('.p3-nc-prefix')].map(e => getComputedStyle(e).fontSize);
  out.nutFs = cards.map(c => { const cs = getComputedStyle(c.querySelector('.p3-nc-nutshell')); return cs.fontSize + '/' + cs.opacity; });
  out.subFs = getComputedStyle(sec.querySelector('.p3-names-sub')).fontSize;
  out.labelFs = cards.map(c => getComputedStyle(c.querySelector('.p3-nc-label')).fontSize);
  out.progFs = getComputedStyle(sec.querySelector('.p3-progress')).fontSize;
  out.h1Fs = getComputedStyle(sec.querySelector('.p3-question')).fontSize;
  out.heroLabel = sec.querySelector('#enterBtn-11').textContent;
  out.heroFs = getComputedStyle(sec.querySelector('#enterBtn-11')).fontSize;
  out.noteCount = sec.querySelectorAll('.p3-nc-note').length;
  out.smartCount = sec.querySelectorAll('.p3-names-smart').length;
  out.enterCount = sec.querySelectorAll('.p3-enter').length;
  // every visible text node: computed color + size + opacity of its element
  const bad = [];
  const walker = document.createTreeWalker(sec, NodeFilter.SHOW_TEXT);
  let node;
  const allowed = ['rgb(255, 255, 255)', 'rgb(160, 107, 255)', 'rgb(47, 232, 158)', 'rgb(255, 191, 61)'];
  while ((node = walker.nextNode())) {
    const t = node.textContent.trim();
    if (!t) continue;
    const el = node.parentElement;
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) continue; // hidden (play-tip at rest, enterNote)
    const cs = getComputedStyle(el);
    const size = parseFloat(cs.fontSize);
    const entry = {text: t.slice(0, 40), color: cs.color, size: cs.fontSize, opacity: cs.opacity};
    if (!allowed.includes(cs.color)) { entry.why = 'color not white/board'; bad.push(entry); }
    else if (size < 16) { entry.why = 'under 16px'; bad.push(entry); }
    else if (parseFloat(cs.opacity) < 1) { entry.why = 'opacity < 1'; bad.push(entry); }
  }
  out.textNodesBad = bad;
  // placeholders: white at opacity 1
  out.placeholders = cards.map(c => {
    const inp = c.querySelector('.p3-nc-input');
    const cs = getComputedStyle(inp, '::placeholder');
    return cs.color + '/' + cs.opacity + '/' + cs.fontSize;
  });
  out.overflow = document.documentElement.scrollWidth - window.innerWidth;
  return out;
}"""

JS_HOVER = """(kind) => {
  const card = [...document.querySelectorAll('.p3-namecard')].find(c => c.querySelector('.p3-nc-eye').dataset.board === kind);
  const cs = getComputedStyle(card);
  const r = card.getBoundingClientRect();
  return {shadow: cs.boxShadow, border: cs.borderColor, top: r.top, transform: cs.transform, hover: card.matches(':hover')};
}"""

JS_EYE = """(kind) => {
  document.querySelector('.p3-nc-eye[data-board="' + kind + '"]').click();
  const m = document.getElementById('boardModal');
  const t = document.getElementById('boardTitle').textContent;
  const lines = [...document.getElementById('boardBody').querySelectorAll('p')].map(p => p.textContent);
  const open = !m.hidden;
  document.getElementById('boardClose').click();
  return {open, title: t, lines};
}"""

JS_CARDCLICK = """(kind) => {
  const card = [...document.querySelectorAll('.p3-namecard')].find(c => c.querySelector('.p3-nc-eye').dataset.board === kind);
  card.scrollIntoView({block: 'center'});
  const r = card.getBoundingClientRect();
  const x = r.left + 12, y = r.bottom - 12; // bottom padding strip: card, not input/eye
  const el = document.elementFromPoint(x, y);
  if (!el) return {clickedTag: null, active: document.activeElement.id, why: 'elementFromPoint null'};
  el.dispatchEvent(new MouseEvent('click', {bubbles: true, clientX: x, clientY: y}));
  return {clickedTag: el.tagName + '.' + (typeof el.className === 'string' ? el.className : 'svg'), active: document.activeElement.id};
}"""

JS_TYPE = """() => {
  const out = {};
  const bIn = document.getElementById('name-business');
  const uB = document.getElementById('url-business');
  bIn.value = 'Green Box Farm';
  bIn.dispatchEvent(new Event('input', {bubbles: true}));
  out.slugFollowsName = uB.value;
  out.stateSlug = window.__walkState.pageNames.business.slug;
  uB.value = 'my-biz';
  uB.dispatchEvent(new Event('input', {bubbles: true}));
  out.customSlug = window.__walkState.pageNames.business.slug;
  bIn.value = 'Green Box Farm Two';
  bIn.dispatchEvent(new Event('input', {bubbles: true}));
  out.customSticks = window.__walkState.pageNames.business.slug;
  const uP = document.getElementById('url-personal');
  uP.value = 'mike8';
  uP.dispatchEvent(new Event('input', {bubbles: true}));
  out.personalCustom = window.__walkState.pageNames.personal.slug;
  return out;
}"""


def run_width(pw, port, width, height, tag):
    print(f"\n===== {tag} {width}x{height} =====")
    browser = pw.firefox.launch(headless=True)
    ctx = browser.new_context(viewport={"width": width, "height": height})
    page = ctx.new_page()
    console = []
    pageerrors = []
    failed_req = []
    page.on("console", lambda m: console.append(m.type + ": " + m.text) if m.type in ("error", "warning") else None)
    page.on("pageerror", lambda e: pageerrors.append(str(e)))
    page.on("requestfailed", lambda r: failed_req.append(r.url + " :: " + str(r.failure)))
    page.goto(f"http://127.0.0.1:{port}/walk-beginning-fixed.html", wait_until="load", timeout=30000)
    page.wait_for_timeout(800)
    shown = page.evaluate(JS_SHOW_NAMES)
    check(f"{tag} names step shown, 3 cards", shown["visible"] and shown["cards"] == 3, shown)
    page.wait_for_timeout(400)
    m = page.evaluate(JS_MEASURE, width)
    results[f"measure-{tag}"] = m
    print(json.dumps(m, indent=1)[:3000])
    exp_col = 1100 if width == 1440 else width - 32
    check(f"{tag} column >= {exp_col}px", m["colW"] >= exp_col, f"colW={m['colW']:.1f}")
    exp_gap = 28 if width == 1440 else 20
    check(f"{tag} card gap >= {exp_gap}px", m["gapPx"] is not None and m["gapPx"] >= exp_gap,
          f"rowGap={m['gap']} boxGap={m['gapPx']}")
    check(f"{tag} card padding >= {exp_gap}px", all(float(p.replace("px", "")) >= exp_gap for p in m["pad"]), m["pad"])
    exp_name = 18 if width == 1440 else 17
    check(f"{tag} name inputs >= {exp_name}px", all(float(x.replace("px", "")) >= exp_name for x in m["nameFs"]), m["nameFs"])
    check(f"{tag} address inputs >= 16px", all(float(x.replace("px", "")) >= 16 for x in m["urlFs"]), m["urlFs"])
    check(f"{tag} address prefix >= 16px", all(float(x.replace("px", "")) >= 16 for x in m["prefixFs"]), m["prefixFs"])
    check(f"{tag} nutshells 16px opacity 1", all(x == "16px/1" for x in m["nutFs"]), m["nutFs"])
    check(f"{tag} subtitle 18px", float(m["subFs"].replace("px", "")) >= 18, m["subFs"])
    check(f"{tag} labels >= 16px", all(float(x.replace("px", "")) >= 16 for x in m["labelFs"]), m["labelFs"])
    check(f"{tag} progress 16px", float(m["progFs"].replace("px", "")) >= 16, m["progFs"])
    check(f"{tag} hero label is 'Build my pages'", m["heroLabel"] == "Build my pages", m["heroLabel"])
    check(f"{tag} hero font >= 18px", float(m["heroFs"].replace("px", "")) >= 18, m["heroFs"])
    check(f"{tag} .p3-nc-note gone (0)", m["noteCount"] == 0, m["noteCount"])
    check(f"{tag} .p3-names-smart gone (0)", m["smartCount"] == 0, m["smartCount"])
    check(f"{tag} one .p3-enter on the step", m["enterCount"] == 1, m["enterCount"])
    check(f"{tag} every visible text node white/board + >=16px + opacity 1",
          m["textNodesBad"] == [], json.dumps(m["textNodesBad"])[:600])
    check(f"{tag} placeholders white opacity 1",
          all(p.startswith("rgb(255, 255, 255)/1") for p in m["placeholders"]), m["placeholders"])
    check(f"{tag} zero horizontal overflow at scroll 0", m["overflow"] <= 0, f"overflow={m['overflow']}")
    # scrolled overflow
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(300)
    ov2 = page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
    check(f"{tag} zero horizontal overflow scrolled", ov2 <= 0, f"overflow={ov2}")
    page.evaluate("window.scrollTo(0,0)")
    page.screenshot(path=os.path.join(SHOTS, f"names-{tag}-rest.png"))
    # hover per card: rest vs lit — scroll the card to the center first
    # (the space card sits below the fold at 1440x900), hover its center,
    # settle 700ms (transition is .25s; headless compositor timing is loose)
    for kind in ("personal", "business", "space"):
        before = page.evaluate(JS_HOVER, kind)
        rect = page.evaluate("""(kind) => {
          const card = [...document.querySelectorAll('.p3-namecard')].find(c => c.querySelector('.p3-nc-eye').dataset.board === kind);
          card.scrollIntoView({block: 'center'});
          const r = card.getBoundingClientRect();
          return {x: r.left + r.width / 2, y: r.top + r.height / 2, top: r.top};
        }""", kind)
        page.wait_for_timeout(250)
        page.mouse.move(rect["x"], rect["y"])
        # settle 1200ms: the .25s hover transition starts late in headless
        # Firefox (proven by re-check: business sat at ty=-0.2 at 700ms and
        # fully settled ty=-4 + 44px own-color glow at 1200ms) — a 700ms read
        # measures the transition, not the state.
        page.wait_for_timeout(1200)
        after = page.evaluate(JS_HOVER, kind)
        ty = 0
        mm = re.search(r"matrix\([^,]+,[^,]+,[^,]+,[^,]+,[^,]+,\s*(-?[\d.]+)\)", after["transform"] or "")
        if mm:
            ty = float(mm.group(1))
        lit = after["hover"] and BOARD[kind] in after["shadow"] and "44px" in after["shadow"]
        lifted = ty <= -3.5
        check(f"{tag} {kind} card lights up on hover in its own color",
              lit and lifted, f"hover={after['hover']} ty={ty} shadow-has-44px={('44px' in after['shadow'])} color-in-shadow={BOARD[kind] in after['shadow']}")
        page.screenshot(path=os.path.join(SHOTS, f"names-{tag}-hover-{kind}.png"))
        page.mouse.move(5, 5)
        page.wait_for_timeout(300)
    # eyes
    for kind in ("personal", "business", "space"):
        r = page.evaluate(JS_EYE, kind)
        check(f"{tag} {kind} eye opens modal with 3 lines",
              r["open"] and len(r["lines"]) == 3 and kind.capitalize() in r["title"] or kind == "space" and "Space" in r["title"],
              json.dumps(r)[:300])
    # card-click focus
    for kind in ("personal", "business", "space"):
        r = page.evaluate(JS_CARDCLICK, kind)
        check(f"{tag} {kind} card click focuses its name input",
              r["active"] == f"name-{kind}", json.dumps(r))
    # typing / live slug (1440 leg only — behavior identical at all widths)
    if tag == "1440":
        t = page.evaluate(JS_TYPE)
        results["typing-1440"] = t
        check("1440 slug follows typed business name", t["slugFollowsName"] == "green-box-farm" and t["stateSlug"] == "green-box-farm", json.dumps(t))
        check("1440 custom address becomes the URL and sticks", t["customSlug"] == "my-biz" and t["customSticks"] == "my-biz", json.dumps(t))
        check("1440 custom personal address becomes the URL", t["personalCustom"] == "mike8", json.dumps(t))
    # hero button advances to building
    page.locator("#enterBtn-11").click()
    page.wait_for_timeout(900)
    adv = page.evaluate("() => ({namesHidden: document.getElementById('step-names').hidden, buildingShown: !document.getElementById('step-building').hidden})")
    check(f"{tag} hero button advances to the building page", adv["namesHidden"] and adv["buildingShown"], json.dumps(adv))
    page.screenshot(path=os.path.join(SHOTS, f"names-{tag}-building.png"))
    # console / page errors (adjudicated: local-server 404s for worker-only routes are expected, not product errors)
    results[f"errors-{tag}"] = {"console": console, "pageerrors": pageerrors, "failed_req": failed_req}
    check(f"{tag} zero page errors (JS exceptions)", pageerrors == [], json.dumps(pageerrors)[:400])
    real_console = [c for c in console if "404" not in c and "Failed to load resource" not in c]
    check(f"{tag} zero console errors (excluding local 404s for worker routes)", real_console == [], json.dumps(console)[:500])
    print(f"{tag} failed requests (local-server artifacts, adjudicated): {json.dumps(failed_req)[:400]}")
    ctx.close()
    browser.close()


def main():
    srv, port = start_server()
    print(f"local server on 127.0.0.1:{port} serving {D}")
    try:
        with sync_playwright() as pw:
            run_width(pw, port, 1440, 900, "1440")
            run_width(pw, port, 390, 844, "390")
            run_width(pw, port, 360, 800, "360")
    finally:
        srv.shutdown()
    n = len(results["checks"])
    f = len(results["fails"])
    print(f"\n===== TOTAL {n - f}/{n} PASS, {f} FAIL =====")
    if results["fails"]:
        print("FAILS:", json.dumps(results["fails"]))
    with open(os.path.join(OUT, "names-results.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1)
    print("results:", os.path.join(OUT, "names-results.json"))


if __name__ == "__main__":
    main()
