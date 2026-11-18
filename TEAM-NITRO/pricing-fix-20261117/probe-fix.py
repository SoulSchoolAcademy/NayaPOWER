#!/usr/bin/env python3
"""Live maker verification for the Pricing Fix round (2026-11-17).
Chromium via the localhost forwarder (127.0.0.1:18080).
Items: 1 long taken name one line at 635+desktop; 2 descender clearance
at both widths (glyph Range rects vs alias-box top); 3 fresh claim with
walk-typed name "Poppy Green" -> reload cert shows it at 635 AND desktop;
4 veil never blocks ENTER/start-over and never covers a result document;
5 no duplicate ids in the walk; scroll/ENTER at 635.
"""
import json
import os

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
SHOTDIR = os.path.join(HERE, "shots-fix")
os.makedirs(SHOTDIR, exist_ok=True)

FREE = "https://naya-pricing-free-staging.nayapower.workers.dev/free"
WALK = "https://naya-pricing-free-staging.nayapower.workers.dev/free/walk"
LONG_ALIAS = "alexanderchristopherbennett"   # cert 753
SHORT_ALIAS = "takenfixshort"                # cert 755
FRESH_ALIAS = "fixfresh17c"                  # new test alias for this round
# NOTE: fixfresh17a was claimed + walked in a probe run that died before
# the reload check; its device key died with that closed context, so the
# reload proof uses fixfresh17b. Both rows await Shawn's-hand cleanup.
FRESH_NAME = "Poppy Green"

NAME_JS = """() => {
  const name = document.getElementById('displayName');
  const wrap = document.querySelector('.alias-field-wrapper');
  const wb = wrap ? wrap.getBoundingClientRect() : null;
  let rects = [];
  try {
    const range = document.createRange();
    range.selectNodeContents(name);
    rects = [...range.getClientRects()].map(r => ({x: Math.round(r.x), y: Math.round(r.y),
      w: Math.round(r.width), h: Math.round(r.height), bottom: Math.round(r.bottom)}));
  } catch(e) {}
  const nb = name.getBoundingClientRect();
  const cs = getComputedStyle(name);
  return {
    text: name.textContent,
    lines: rects.length, rects,
    glyphBottom: rects.length ? Math.max(...rects.map(r => r.bottom)) : null,
    wrapTop: wb ? Math.round(wb.top) : null,
    clearance: (wb && rects.length) ? Math.round(wb.top) - Math.max(...rects.map(r => r.bottom)) : null,
    nameBox: {x: Math.round(nb.x), y: Math.round(nb.y), w: Math.round(nb.width), h: Math.round(nb.height), bottom: Math.round(nb.bottom)},
    fontSize: cs.fontSize, whiteSpace: cs.whiteSpace, lineHeight: cs.lineHeight,
    scrollW: name.scrollWidth, clientW: name.clientWidth,
    fitsOneLine: name.scrollWidth <= name.clientWidth + 1,
    textShadow: cs.textShadow,
  };
}"""

MEASURE_JS = """() => {
  const q = s => document.querySelector(s);
  const r = el => { if (!el) return null; const b = el.getBoundingClientRect();
    return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width),
            h: Math.round(b.height), top: Math.round(b.top), bottom: Math.round(b.bottom)}; };
  const plaque = q('#certPlaque'), st = q('#aliasStatus'), veil = q('#installVeil');
  return {
    plaqueClass: plaque ? plaque.className : null,
    status: st ? {state: st.getAttribute('data-state'), text: st.textContent} : null,
    veilHidden: veil ? veil.hidden : null,
    veilPointerEvents: veil ? getComputedStyle(veil).pointerEvents : null,
    regalia: q('#certRegalia') ? {hidden: q('#certRegalia').hidden,
      no: q('#certNoValue') ? q('#certNoValue').textContent : null,
      date: q('#certDate') ? q('#certDate').textContent : null} : null,
    enter: {box: r(q('#enterBtn')), inViewport: q('#enterBtn') ? (q('#enterBtn').getBoundingClientRect().bottom <= window.innerHeight && q('#enterBtn').getBoundingClientRect().top >= 0) : null},
    startOver: {box: r(q('#startOverBtn')), display: q('#startOverBtn') ? getComputedStyle(q('#startOverBtn')).display : null},
    ls: {smart_name: localStorage.getItem('nayanet_smart_name'),
         smart_alias: localStorage.getItem('nayanet_smart_alias'),
         install_dismissed: localStorage.getItem('nayanet_install_dismissed'),
         install_shows: localStorage.getItem('nayanet.install.shows')},
  };
}"""


def new_page(pw, width, height):
    browser = pw.chromium.launch(headless=True, proxy={"server": "http://127.0.0.1:18080"})
    ctx = browser.new_context(viewport={"width": width, "height": height},
                              device_scale_factor=1, is_mobile=(width <= 640),
                              ignore_https_errors=True)
    page = ctx.new_page()
    console = []
    page.on("console", lambda m: console.append(f"{m.type}: {m.text}"))
    page.on("pageerror", lambda e: console.append(f"PAGEERROR: {e}"))
    return browser, ctx, page, console


def veil_state(page):
    return page.evaluate("() => { const v = document.getElementById('installVeil'); return {hidden: v.hidden, shows: localStorage.getItem('nayanet.install.shows'), dismissed: localStorage.getItem('nayanet_install_dismissed')}; }")


def probe_taken(pw, width, height, alias, label):
    browser, ctx, page, console = new_page(pw, width, height)
    page.goto(FREE, wait_until="load", timeout=60000)
    page.wait_for_timeout(1200)
    # Type fast, before the 5s veil timer fires: the veil must NEVER show
    # over a taken document (auto-show gate).
    page.fill("#aliasInput", alias)
    page.wait_for_function(
        "document.getElementById('aliasStatus').getAttribute('data-state') === 'taken'",
        timeout=15000)
    page.wait_for_timeout(600)
    m = page.evaluate(MEASURE_JS)
    n = page.evaluate(NAME_JS)
    page.wait_for_timeout(6000)  # past the 5s auto-show point
    v_after = veil_state(page)
    shot = os.path.join(SHOTDIR, f"taken-{label}-{width}x{height}.png")
    page.screenshot(path=shot)
    print(f"  TAKEN-{label} [{width}x{height}] state={m['status']} lines={n['lines']} "
          f"font={n['fontSize']} fits={n['fitsOneLine']} clearance={n['clearance']}px "
          f"veilHiddenAtLoad={m['veilHidden']} veilAfter7s={v_after} glow={'38px' in (n['textShadow'] or '')}")
    print(f"    nameBox={n['nameBox']} wrapTop={n['wrapTop']} glyphBottom={n['glyphBottom']} "
          f"startOver={m['startOver']['display']} enterInViewport={m['enter']['inViewport']}")
    browser.close()
    return {"taken": m, "name": n, "veilAfter7s": v_after, "console": console}


def probe_veil_blocks_enter(pw):
    """Fresh profile, composing state: veil auto-shows at 5s. The brief's
    shape is 'dismiss on first interaction': a real mouse click on ENTER
    while the veil is up must dismiss the veil (the dismissing click does
    not also fire ENTER — the click target was the card); the NEXT click
    must activate ENTER. Locator clicks are NOT used here: Playwright's
    actionability check refuses a covered element, which is stricter
    than a human mouse."""
    browser, ctx, page, console = new_page(pw, 635, 900)
    page.goto(FREE, wait_until="load", timeout=60000)
    page.wait_for_function("!document.getElementById('installVeil').hidden", timeout=12000)
    box = page.evaluate("""() => { const b = document.getElementById('enterBtn').getBoundingClientRect();
      return {x: b.x + b.width/2, y: b.y + b.height/2}; }""")
    print(f"  VEIL up in composing state — real mouse click on ENTER at {box}")
    page.mouse.click(box["x"], box["y"])
    page.wait_for_timeout(600)
    v = veil_state(page)
    print(f"  VEIL after 1st click: veilHidden={v['hidden']} dismissed={v['dismissed']} (expect hidden/1)")
    assert v["hidden"] is True, "veil still up after first click on ENTER — BLOCKED"
    page.mouse.click(box["x"], box["y"])
    page.wait_for_timeout(600)
    m = page.evaluate(MEASURE_JS)
    print(f"  VEIL after 2nd click: status={m['status']} (expect 'Enter alias to continue.')")
    assert m["status"]["text"] == "Enter alias to continue.", "ENTER did not act on 2nd click"
    # start-over works from the taken state (veil never shows there).
    page.fill("#aliasInput", LONG_ALIAS)
    page.wait_for_function(
        "document.getElementById('aliasStatus').getAttribute('data-state') === 'taken'",
        timeout=15000)
    page.wait_for_timeout(400)
    page.click("#startOverBtn", timeout=5000)
    page.wait_for_timeout(800)
    m2 = page.evaluate(MEASURE_JS)
    print(f"  VEIL start-over: state={m2['status']} lsAlias={m2['ls']['smart_alias']} (expect neutral/null)")
    assert m2["status"]["state"] == "neutral" and m2["ls"]["smart_alias"] is None
    browser.close()
    return {"console": console}


def probe_walk_dup_ids(pw):
    browser, ctx, page, console = new_page(pw, 1440, 900)
    page.goto(WALK, wait_until="load", timeout=60000)
    page.wait_for_timeout(1000)
    dupes = page.evaluate("""() => {
      const ids = [...document.querySelectorAll('[id]')].map(e => e.id);
      const seen = {}, d = [];
      ids.forEach(i => { seen[i] = (seen[i] || 0) + 1; });
      Object.keys(seen).forEach(k => { if (seen[k] > 1) d.push(k + ' x' + seen[k]); });
      return {total: ids.length, dupes: d,
        enter14: document.querySelectorAll('#enterBtn-14').length,
        enterNames: document.querySelectorAll('#enterBtn-names').length};
    }""")
    print(f"  WALK ids: total={dupes['total']} dupes={dupes['dupes']} "
          f"enterBtn-14={dupes['enter14']} enterBtn-names={dupes['enterNames']}")
    assert dupes["dupes"] == [] and dupes["enter14"] == 1 and dupes["enterNames"] == 1
    browser.close()
    return {"dupes": dupes, "console": console}


def probe_fresh_claim(pw):
    """Fresh claim at 635 with the veil UP: ENTER through the veil, walk
    with typed name 'Poppy Green' at step 1 + names page, end slide,
    reload -> cert must show 'Poppy Green' (not the alias echo)."""
    browser, ctx, page, console = new_page(pw, 635, 900)
    page.goto(FREE, wait_until="load", timeout=60000)
    # fresh alias must not exist yet
    st = page.evaluate(f"fetch('/api/claim?alias={FRESH_ALIAS}').then(r => r.json()).then(d => d.exists)")
    assert st is False, f"fresh alias {FRESH_ALIAS} already exists — pick another"
    page.wait_for_function("!document.getElementById('installVeil').hidden", timeout=12000)
    print("  FRESH veil up before claim — claiming while it is up, so the")
    print("  stamp must close it (click-through-ENTER is proven separately).")
    # Fill + claim via JS: locator fill/click refuse a covered element,
    # and the human click path is proven in probe_veil_blocks_enter.
    page.evaluate(f"""() => {{ const i = document.getElementById('aliasInput');
      i.value = '{FRESH_ALIAS}'; i.dispatchEvent(new Event('input', {{bubbles: true}})); }}""")
    page.wait_for_function(
        "document.getElementById('aliasStatus').getAttribute('data-state') === 'available'",
        timeout=15000)
    page.evaluate("activateAndRedirect()")
    # stamp must close the veil; redirect to walk follows ~800ms later
    page.wait_for_function(
        "document.getElementById('certPlaque').classList.contains('is-certified')",
        timeout=15000)
    v = veil_state(page)
    print(f"  FRESH stamped: veilHiddenAtStamp={v['hidden']} (expect True — stamp closes veil)")
    assert v["hidden"] is True, "veil still up after stamp — fresh cert sits behind it"
    page.wait_for_url("**/free/walk**", timeout=30000)
    page.wait_for_timeout(1200)
    print(f"  FRESH on walk: {page.url[:80]}")
    # Step 1: type the name
    page.fill("#answer-1", FRESH_NAME)
    page.click("#enterBtn-1", timeout=5000)
    page.wait_for_timeout(600)
    ls1 = page.evaluate("localStorage.getItem('nayanet_smart_name')")
    print(f"  FRESH after step 1: localStorage smart_name={ls1!r} (expect 'Poppy Green')")
    assert ls1 == FRESH_NAME, "step-1 name was NOT adopted"
    # Steps 2-13: short answers
    for n in range(2, 14):
        page.fill(f"#answer-{n}", "test answer")
        page.click(f"#enterBtn-{n}", timeout=5000)
        page.wait_for_timeout(250)
    # Step 14: choose No
    page.click("#hintRow-14 button[data-act='no']", timeout=5000)
    page.wait_for_timeout(800)
    # Names page: type the name as the personal title
    page.fill("#name-personal", FRESH_NAME)
    page.fill("#name-business", "Poppy Business")
    page.fill("#name-space", "Poppy Space")
    page.click("#enterBtn-names", timeout=5000)
    page.wait_for_timeout(1000)
    ls2 = page.evaluate("localStorage.getItem('nayanet_smart_name')")
    payload = page.evaluate("window.__lastCompletionPayload ? window.__lastCompletionPayload.name : null")
    print(f"  FRESH after names page: smart_name={ls2!r} completionPayloadName={payload!r}")
    # Building -> build done ("See your pages") -> end slide
    try:
        page.wait_for_selector("#buildDone:not([hidden])", timeout=30000)
        page.click("#buildGo", timeout=5000)
        page.wait_for_selector("#step-end:not([hidden])", timeout=15000)
    except Exception:
        page.screenshot(path=os.path.join(SHOTDIR, "fresh-635-end-wait-failed.png"))
        raise
    page.wait_for_timeout(800)
    page.screenshot(path=os.path.join(SHOTDIR, "fresh-635-end-slide.png"))
    print("  FRESH end slide reached")
    # Reload the entry at 635: cert must show the walk's typed name
    page.goto(FREE, wait_until="load", timeout=60000)
    page.wait_for_function(
        "document.getElementById('aliasStatus').getAttribute('data-state') === 'own'",
        timeout=15000)
    page.wait_for_timeout(800)
    m = page.evaluate(MEASURE_JS)
    n = page.evaluate(NAME_JS)
    page.screenshot(path=os.path.join(SHOTDIR, "fresh-635-cert.png"))
    print(f"  FRESH cert 635: name={n['text']!r} lines={n['lines']} regalia={m['regalia']} "
          f"veilHidden={m['veilHidden']} (expect 'Poppy Green', veil hidden)")
    assert n["text"] == FRESH_NAME, f"cert shows {n['text']!r}, not the walk name"
    # Wait past the 5s auto-show: veil must NOT appear over the certificate
    page.wait_for_timeout(6000)
    v = veil_state(page)
    print(f"  FRESH cert 635 after 7s: veilHidden={v['hidden']} shows={v['shows']} (expect hidden, no auto-show)")
    assert v["hidden"] is True
    # Same identity at desktop width (own-device restore): name must agree
    ls = page.evaluate("""() => { const o = {}; for (let i = 0; i < localStorage.length; i++) { const k = localStorage.key(i); o[k] = localStorage.getItem(k); } return o; }""")
    ss = page.evaluate("""() => { const o = {}; for (let i = 0; i < sessionStorage.length; i++) { const k = sessionStorage.key(i); o[k] = sessionStorage.getItem(k); } return o; }""")
    browser.close()
    browser2, ctx2, page2, console2 = new_page(pw, 1440, 900)
    page2.goto(FREE, wait_until="load", timeout=60000)
    page2.evaluate("(ls) => { Object.keys(ls).forEach(k => localStorage.setItem(k, ls[k])); }", ls)
    page2.evaluate("(ss) => { Object.keys(ss).forEach(k => sessionStorage.setItem(k, ss[k])); }", ss)
    page2.reload(wait_until="load", timeout=60000)
    page2.wait_for_function(
        "document.getElementById('aliasStatus').getAttribute('data-state') === 'own'",
        timeout=15000)
    page2.wait_for_timeout(800)
    m2 = page2.evaluate(MEASURE_JS)
    n2 = page2.evaluate(NAME_JS)
    page2.screenshot(path=os.path.join(SHOTDIR, "fresh-1440-cert.png"))
    print(f"  FRESH cert 1440: name={n2['text']!r} lines={n2['lines']} regalia={m2['regalia']} veilHidden={m2['veilHidden']}")
    assert n2["text"] == FRESH_NAME, f"desktop cert shows {n2['text']!r}"
    page2.wait_for_timeout(6000)
    v2 = veil_state(page2)
    print(f"  FRESH cert 1440 after 7s: veilHidden={v2['hidden']} (expect hidden)")
    assert v2["hidden"] is True
    browser2.close()
    return {"cert635": {"measure": m, "name": n}, "cert1440": {"measure": m2, "name": n2},
            "console": console + console2}


def main():
    out = {}
    with sync_playwright() as pw:
        print("TAKEN long (29 chars):")
        out["taken-long-635x900"] = probe_taken(pw, 635, 900, LONG_ALIAS, "long")
        out["taken-long-1440x900"] = probe_taken(pw, 1440, 900, LONG_ALIAS, "long")
        print("TAKEN short:")
        out["taken-short-635x900"] = probe_taken(pw, 635, 900, SHORT_ALIAS, "short")
        out["taken-short-1440x900"] = probe_taken(pw, 1440, 900, SHORT_ALIAS, "short")
        print("VEIL blocks ENTER:")
        out["veil-enter"] = probe_veil_blocks_enter(pw)
        print("WALK duplicate ids:")
        out["walk-dup-ids"] = probe_walk_dup_ids(pw)
        print("FRESH claim:")
        out["fresh"] = probe_fresh_claim(pw)
    with open(os.path.join(HERE, "probe-fix.json"), "w") as f:
        json.dump(out, f, indent=2)
    print("wrote probe-fix.json")
    seen = set()
    print("---- console (all runs) ----")
    for k, v in out.items():
        for c in v.get("console", []):
            if c not in seen:
                seen.add(c)
                print(f"  [{k}] {c}")


if __name__ == "__main__":
    main()
