#!/usr/bin/env python3
"""Live AFTER verification — taken state fixed (2026-11-17).

Fresh Chromium profile (new device) -> /free -> type the already-claimed
alias -> measure the taken state at 390x844, 635x349, 1440x900.
Improvements over the before-probe:
  - ignore_https_errors=True so Marcellus loads through the forwarder
    (the before-probe's css2 CERT error was a probe artifact).
  - GLYPH-level overlap: Range rects of the name's first text line vs
    the title / "This certifies that" text (box overlap over-reports).
  - USER scroll: mouse.wheel over the plaque (programmatic scrollTop is
    not a user path — overflow:hidden accepts it).
  - Start-over click: clears the claim and returns to composing.
  - ENTER-on-taken path at 390 (hubNote + start-over from there).
  - At-load screenshot AND scrolled screenshot per viewport.
  - Font check + console-error check (item 5).

Usage: probe-after.py   (shots go to shots-after/)
"""
import json
import os

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
SHOTDIR = os.path.join(HERE, "shots-after")
os.makedirs(SHOTDIR, exist_ok=True)

FREE = "https://naya-pricing-free-staging.nayapower.workers.dev/free"
ALIAS = "alexanderchristopherbennett"   # cert 753, claimed 2026-11-17
NAME = "Alexander Christopher Bennett"  # 29 chars
KEY = "nayanet_key_takenfix001"

MEASURE_JS = """() => {
  const q = s => document.querySelector(s);
  const r = el => { if (!el) return null; const b = el.getBoundingClientRect();
    return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width),
            h: Math.round(b.height), top: Math.round(b.top), bottom: Math.round(b.bottom)}; };
  const cs = el => { if (!el) return null; const c = getComputedStyle(el);
    return {display: c.display, position: c.position, textShadow: c.textShadow,
            fontSize: c.fontSize, fontFamily: c.fontFamily}; };
  // glyph-level: first text-line rect of the name vs the title/certifies text
  function textRects(el) {
    if (!el) return [];
    const out = [];
    for (const node of el.childNodes) {
      if (node.nodeType !== 3 || !node.textContent.trim()) continue;
      const range = document.createRange();
      range.selectNodeContents(node);
      for (const b of range.getClientRects())
        out.push({x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width),
                  h: Math.round(b.height), top: Math.round(b.top), bottom: Math.round(b.bottom)});
      range.detach();
    }
    return out;
  }
  const plaque = q('#certPlaque');
  const name = q('#displayName'), title = q('.cert-title'),
        cert = q('.cert-certifies'), btn = q('#enterBtn'),
        so = q('#startOverBtn'), st = q('#aliasStatus'),
        hub = q('#hubNote'), input = q('#aliasInput');
  const nr = textRects(name), tr = textRects(title), cr = textRects(cert);
  const hit = (a, b) => a.some(x => b.some(y => x.x < y.x + y.w && x.x + x.w > y.x &&
    x.y < y.y + y.h && x.y + x.h > y.y));
  const firstName = nr.length ? nr[0] : null;
  return {
    plaqueClass: plaque ? plaque.className : null,
    status: st ? {state: st.getAttribute('data-state'), text: st.textContent} : null,
    marcellusLoaded: document.fonts ? document.fonts.check('52px Marcellus') : null,
    name: {box: r(name), style: cs(name), text: name ? name.textContent : null,
           hidden: name ? name.hidden : null, firstLineText: firstName,
           textRects: nr},
    title: {box: r(title), textRects: tr},
    certifies: {box: r(cert), textRects: cr},
    nameGlyphOverlapsTitle: hit(nr, tr),
    nameGlyphOverlapsCertifies: hit(nr, cr),
    enter: {box: r(btn), inViewport: btn ? (btn.getBoundingClientRect().bottom <= window.innerHeight && btn.getBoundingClientRect().top >= 0) : null},
    startOver: {box: r(so), style: cs(so)},
    hubNote: hub ? {hidden: hub.hidden, text: hub.textContent.slice(0, 90)} : null,
    inputValue: input ? input.value : null,
    plaqueScroll: plaque ? {scrollH: plaque.scrollHeight, clientH: plaque.clientHeight,
      scrollTop: plaque.scrollTop,
      overflowY: getComputedStyle(plaque).overflowY,
      scrollable: plaque.scrollHeight > plaque.clientHeight + 1} : null,
    innerH: window.innerHeight, innerW: window.innerWidth,
  };
}"""


def new_browser(pw, width, height, preset_own=False):
    browser = pw.chromium.launch(headless=True, proxy={"server": "http://127.0.0.1:18080"})
    ctx = browser.new_context(viewport={"width": width, "height": height},
                              device_scale_factor=1, is_mobile=(width <= 640),
                              ignore_https_errors=True)
    if preset_own:
        ctx.add_init_script(
            f"localStorage.setItem('nayanet_smart_alias', '{ALIAS}');"
            f"localStorage.setItem('nayanet_smart_name', '{NAME}');"
            f"localStorage.setItem('nayanet_vault_key', '{KEY}');")
    return browser, ctx


def collect(page):
    console, failed, allreq = [], [], []
    page.on("console", lambda m: console.append(f"{m.type}: {m.text}"))
    page.on("pageerror", lambda e: console.append(f"PAGEERROR: {e}"))
    page.on("requestfailed", lambda r: failed.append(f"{r.url} :: {r.failure}"))
    page.on("response", lambda r: failed.append(f"{r.url} :: HTTP {r.status}") if r.status >= 400 else None)
    page.on("request", lambda r: allreq.append(f"{r.method} {r.url}"))
    return console, failed, allreq



def dismiss_veil(page):
    """The Install App veil auto-shows on fresh profiles and intercepts
    pointer events; a user dismisses it. Dismiss if present so wheel /
    click tests measure the certificate, not the popup."""
    try:
        vis = page.evaluate("!document.getElementById('installVeil').hidden")
        if vis:
            page.click("#installLater", timeout=3000)
            page.wait_for_timeout(400)
            return True
    except Exception:
        pass
    return False

def reach_taken(page):
    page.goto(FREE, wait_until="load", timeout=60000)
    page.wait_for_timeout(1200)
    dismiss_veil(page)
    page.fill("#aliasInput", ALIAS)
    page.wait_for_function(
        "document.getElementById('aliasStatus').getAttribute('data-state') === 'taken'",
        timeout=15000)
    page.wait_for_timeout(800)


def probe_taken(pw, width, height, extra_enter=False):
    browser, ctx = new_browser(pw, width, height)
    page = ctx.new_page()
    console, failed, allreq = collect(page)
    reach_taken(page)
    m0 = page.evaluate(MEASURE_JS)
    shot0 = os.path.join(SHOTDIR, f"taken-{width}x{height}-load.png")
    page.screenshot(path=shot0, full_page=False)
    # USER scroll: wheel over the plaque center, three notches
    before = m0["plaqueScroll"]["scrollTop"]
    page.mouse.move(width // 2, height // 2)
    for _ in range(3):
        page.mouse.wheel(0, 400)
        page.wait_for_timeout(250)
    m1 = page.evaluate(MEASURE_JS)
    wheel_moved = m1["plaqueScroll"]["scrollTop"] != before
    shot1 = os.path.join(SHOTDIR, f"taken-{width}x{height}-scrolled.png")
    page.screenshot(path=shot1, full_page=False)
    result = {"viewport": [width, height], "takenAtLoad": m0,
              "takenAfterWheel": m1, "wheelMovedPlaque": wheel_moved,
              "console": console, "failed": failed, "allreq": allreq}
    print(f"  TAKEN [{width}x{height}] status={m0['status']} marcellus={m0['marcellusLoaded']}")
    print(f"    glyphOverlap title={m0['nameGlyphOverlapsTitle']} certifies={m0['nameGlyphOverlapsCertifies']} "
          f"nameFirstLine={m0['name']['firstLineText']} certifiesText={m0['certifies']['textRects']}")
    print(f"    name pos={m0['name']['style']['position']} shadow={m0['name']['style']['textShadow']!r}")
    print(f"    enter load inViewport={m0['enter']['inViewport']} box={m0['enter']['box']} "
          f"plaque overflowY={m0['plaqueScroll']['overflowY']} scrollable={m0['plaqueScroll']['scrollable']}")
    print(f"    wheel moved plaque scrollTop {before} -> {m1['plaqueScroll']['scrollTop']} (moved={wheel_moved}); "
          f"after wheel ENTER inViewport={m1['enter']['inViewport']} box={m1['enter']['box']}")
    print(f"    startOver display={m0['startOver']['style']['display']} box={m0['startOver']['box']}")
    if extra_enter:
        # ENTER on a taken alias -> hubNote; then start-over -> composing
        page.evaluate("document.getElementById('certPlaque').scrollTop = 0")
        page.click("#enterBtn")
        page.wait_for_timeout(1500)
        m2 = page.evaluate(MEASURE_JS)
        print(f"    after ENTER-on-taken: status={m2['status']} hubNote hidden={m2['hubNote']['hidden']} "
              f"text={m2['hubNote']['text']!r}")
        page.click("#startOverBtn")
        page.wait_for_timeout(1500)
        m3 = page.evaluate(MEASURE_JS)
        keys = page.evaluate("[localStorage.getItem('nayanet_smart_alias'), localStorage.getItem('nayanet_smart_name'), localStorage.getItem('nayanet_vault_key'), localStorage.getItem('naya_welcome_right_v1'), localStorage.getItem('nayanet_free_entry')]")
        print(f"    after START-OVER click: status={m3['status']} input={m3['inputValue']!r} "
              f"plaqueClass={m3['plaqueClass']} leftoverKeys={keys}")
        result["afterEnterOnTaken"] = m2
        result["afterStartOver"] = m3
        result["leftoverKeys"] = keys
        shot2 = os.path.join(SHOTDIR, f"taken-{width}x{height}-after-startover.png")
        page.screenshot(path=shot2, full_page=False)
    browser.close()
    return result


def probe_fresh(pw, width, height):
    browser, ctx = new_browser(pw, width, height, preset_own=True)
    page = ctx.new_page()
    console, failed, allreq = collect(page)
    page.goto(FREE, wait_until="load", timeout=60000)
    page.wait_for_timeout(1200)
    dismiss_veil(page)
    try:
        page.wait_for_function(
            "document.getElementById('certPlaque').classList.contains('is-certified')",
            timeout=15000)
    except Exception as e:
        print(f"  FRESH [{width}x{height}] never certified: {e}")
    page.wait_for_timeout(800)
    m0 = page.evaluate(MEASURE_JS)
    shot0 = os.path.join(SHOTDIR, f"fresh-{width}x{height}-load.png")
    page.screenshot(path=shot0, full_page=False)
    print(f"  FRESH [{width}x{height}] plaqueClass={m0['plaqueClass']} status={m0['status']} marcellus={m0['marcellusLoaded']}")
    print(f"    glyphOverlap title={m0['nameGlyphOverlapsTitle']} certifies={m0['nameGlyphOverlapsCertifies']} "
          f"nameFirstLine={m0['name']['firstLineText']}")
    print(f"    name shadow={m0['name']['style']['textShadow']!r}")
    print(f"    enter load inViewport={m0['enter']['inViewport']} box={m0['enter']['box']}")
    print(f"    startOver display={m0['startOver']['style']['display']} box={m0['startOver']['box']}")
    browser.close()
    return {"viewport": [width, height], "freshAtLoad": m0,
            "console": console, "failed": failed, "allreq": allreq}


def main():
    out = {}
    with sync_playwright() as pw:
        for w, h in [(390, 844), (635, 349), (1440, 900)]:
            print(f"TAKEN {w}x{h}:")
            out[f"taken-{w}x{h}"] = probe_taken(pw, w, h, extra_enter=(w == 390))
        for w, h in [(390, 844), (635, 349), (1440, 900)]:
            print(f"FRESH {w}x{h}:")
            out[f"fresh-{w}x{h}"] = probe_fresh(pw, w, h)
    with open(os.path.join(HERE, "probe-after.json"), "w") as f:
        json.dump(out, f, indent=2)
    print("wrote probe-after.json")
    print("---- console messages (all runs) ----")
    seen = set()
    for k, v in out.items():
        for c in v["console"]:
            if c not in seen:
                seen.add(c)
                print(f"  [{k}] {c}")
    print("---- failed requests / HTTP>=400 (all runs) ----")
    seen = set()
    for k, v in out.items():
        for c in v["failed"]:
            if c not in seen:
                seen.add(c)
                print(f"  [{k}] {c}")
    print("---- sw.js / manifest requests seen ----")
    seen = set()
    for k, v in out.items():
        for c in v.get("allreq", []):
            if ("sw.js" in c or "manifest" in c) and c not in seen:
                seen.add(c)
                print(f"  [{k}] {c}")


if __name__ == "__main__":
    main()
