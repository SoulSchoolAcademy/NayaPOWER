#!/usr/bin/env python3
"""Live AFTER verification, round 2 — veil-aware (2026-11-17).

Round 1 proved the fix except for two probe artifacts:
  (a) the Install App veil auto-shows a few seconds after load on fresh
      profiles and eats wheel/click input + covers screenshots — dismiss
      it immediately before EVERY measurement, screenshot, and wheel test;
  (b) the Range line-box overlap test flags even the eye-passed fresh
      certificate, so it is reported but NOT the arbiter — the screenshot
      is (name glyphs clear of the title / "This certifies that").

This round: long alias (cert 753) + short alias (cert 755) taken states
at 390/635/1440, user wheel scroll at 635 (plaque + document), SW
registration + manifest fetch proof, clean screenshots.
"""
import json
import os

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
SHOTDIR = os.path.join(HERE, "shots-after2")
os.makedirs(SHOTDIR, exist_ok=True)

FREE = "https://naya-pricing-free-staging.nayapower.workers.dev/free"
LONG_ALIAS = "alexanderchristopherbennett"   # cert 753
SHORT_ALIAS = "takenfixshort"                # cert 755
NAME = "Alexander Christopher Bennett"
KEY = "nayanet_key_takenfix001"

MEASURE_JS = """() => {
  const q = s => document.querySelector(s);
  const r = el => { if (!el) return null; const b = el.getBoundingClientRect();
    return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width),
            h: Math.round(b.height), top: Math.round(b.top), bottom: Math.round(b.bottom)}; };
  const cs = el => { if (!el) return null; const c = getComputedStyle(el);
    return {display: c.display, position: c.position, textShadow: c.textShadow}; };
  const plaque = q('#certPlaque');
  const name = q('#displayName'), btn = q('#enterBtn'),
        so = q('#startOverBtn'), st = q('#aliasStatus'),
        veil = q('#installVeil');
  return {
    plaqueClass: plaque ? plaque.className : null,
    status: st ? {state: st.getAttribute('data-state'), text: st.textContent} : null,
    veilHidden: veil ? veil.hidden : null,
    name: {box: r(name), style: cs(name), text: name ? name.textContent : null},
    enter: {box: r(btn), inViewport: btn ? (btn.getBoundingClientRect().bottom <= window.innerHeight && btn.getBoundingClientRect().top >= 0) : null},
    startOver: {box: r(so), style: cs(so)},
    plaqueScroll: plaque ? {scrollH: plaque.scrollHeight, clientH: plaque.clientHeight,
      scrollTop: plaque.scrollTop, overflowY: getComputedStyle(plaque).overflowY} : null,
    winScrollY: window.scrollY, docScrollH: document.documentElement.scrollHeight,
    innerH: window.innerHeight,
  };
}"""


def settle(page):
    """Dismiss the Install App veil if it has shown; return True if it was up."""
    try:
        vis = page.evaluate("!document.getElementById('installVeil').hidden")
        if vis:
            page.click("#installLater", timeout=3000)
            page.wait_for_timeout(400)
            return True
    except Exception:
        pass
    return False


def probe_taken(pw, width, height, alias, label):
    browser = pw.chromium.launch(headless=True, proxy={"server": "http://127.0.0.1:18080"})
    ctx = browser.new_context(viewport={"width": width, "height": height},
                              device_scale_factor=1, is_mobile=(width <= 640),
                              ignore_https_errors=True)
    console, failed = [], []
    page = ctx.new_page()
    page.on("console", lambda m: console.append(f"{m.type}: {m.text}"))
    page.on("pageerror", lambda e: console.append(f"PAGEERROR: {e}"))
    page.on("response", lambda r: failed.append(f"{r.url} :: HTTP {r.status}") if r.status >= 400 else None)
    page.goto(FREE, wait_until="load", timeout=60000)
    page.wait_for_timeout(1500)
    settle(page)
    page.fill("#aliasInput", alias)
    page.wait_for_function(
        "document.getElementById('aliasStatus').getAttribute('data-state') === 'taken'",
        timeout=15000)
    page.wait_for_timeout(800)
    settle(page)
    m0 = page.evaluate(MEASURE_JS)
    shot0 = os.path.join(SHOTDIR, f"taken-{label}-{width}x{height}-load.png")
    page.screenshot(path=shot0, full_page=False)
    # USER wheel scroll over the plaque center (veil confirmed gone)
    veil_up = not page.evaluate("document.getElementById('installVeil').hidden")
    before_top, before_win = m0["plaqueScroll"]["scrollTop"], m0["winScrollY"]
    page.mouse.move(width // 2, height // 2)
    for _ in range(4):
        page.mouse.wheel(0, 400)
        page.wait_for_timeout(250)
    m1 = page.evaluate(MEASURE_JS)
    shot1 = os.path.join(SHOTDIR, f"taken-{label}-{width}x{height}-scrolled.png")
    page.screenshot(path=shot1, full_page=False)
    # SW registration + manifest fetch proof
    sw = page.evaluate(
        "navigator.serviceWorker.getRegistration().then(r => r ? r.scope : null)")
    res = page.evaluate(
        "performance.getEntriesByType('resource').map(e => e.name).filter(n => n.includes('sw.js') || n.includes('manifest'))")
    print(f"  TAKEN-{label} [{width}x{height}] status={m0['status']} veilUpAtWheel={veil_up} "
          f"nameBox={m0['name']['box']} pos={m0['name']['style']['position']} "
          f"shadow={'38px' in (m0['name']['style']['textShadow'] or '')}")
    print(f"    enter load inViewport={m0['enter']['inViewport']} box={m0['enter']['box']} "
          f"startOver={m0['startOver']['style']['display']} {m0['startOver']['box']}")
    print(f"    wheel: plaqueScrollTop {before_top}->{m1['plaqueScroll']['scrollTop']} "
          f"winScrollY {before_win}->{m1['winScrollY']} ENTER inViewport={m1['enter']['inViewport']} "
          f"box={m1['enter']['box']}")
    print(f"    swRegistration={sw} sw/manifestResources={res}")
    browser.close()
    return {"viewport": [width, height], "alias": alias, "takenAtLoad": m0,
            "takenAfterWheel": m1, "swRegistration": sw, "swResources": res,
            "console": console, "failed": failed}


def main():
    out = {}
    with sync_playwright() as pw:
        for w, h in [(390, 844), (635, 349), (1440, 900)]:
            print(f"TAKEN-long {w}x{h}:")
            out[f"taken-long-{w}x{h}"] = probe_taken(pw, w, h, LONG_ALIAS, "long")
        for w, h in [(390, 844), (1440, 900)]:
            print(f"TAKEN-short {w}x{h}:")
            out[f"taken-short-{w}x{h}"] = probe_taken(pw, w, h, SHORT_ALIAS, "short")
    with open(os.path.join(HERE, "probe-after2.json"), "w") as f:
        json.dump(out, f, indent=2)
    print("wrote probe-after2.json")
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


if __name__ == "__main__":
    main()
