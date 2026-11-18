#!/usr/bin/env python3
"""Live verification — /free shows the CURRENT certificate (2026-11-17).

ONE fresh alias: `certcurrent` (hero "Certcurrent"). No other alias is
claimed in this round. Flow (one browser profile, viewports in order):
  390x844  type alias -> TYPED state (trophy name, panels, agree, reader)
  1920x1080 (same page) ENTER -> claim -> redirect to /free/walk ->
           back to /free -> CERTIFIED by own-restore
  390x844  reload -> CERTIFIED restore
  635x349  reload -> CERTIFIED restore + wheel ENTER reachability
Plus a second fresh profile (no new alias): type the same alias ->
TAKEN state (clone present, text-shadow none — no bleed-through).
The Install App veil is dismissed immediately before every measurement.
Chromium through the localhost forwarder (Firefox fires zero Supabase
reads in this VM). Screenshots go to shots/.
"""
import json
import os

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
SHOTDIR = os.path.join(HERE, "shots")
os.makedirs(SHOTDIR, exist_ok=True)

FREE = "https://naya-pricing-free-staging.nayapower.workers.dev/free"
WALK = "https://naya-pricing-free-staging.nayapower.workers.dev/free/walk"
ALIAS = "certcurrent"
NAME = "Certcurrent"
SENTENCE = ("By entering your name, you make it official \u2014 you are signing "
            "the Collective Agreement, and you get the deed to your own world: "
            "high-level digital real estate \u2014 your personal page, your "
            "business, your space \u2014 free forever.")

MEASURE_JS = """() => {
  const q = s => document.querySelector(s);
  const r = el => { if (!el) return null; const b = el.getBoundingClientRect();
    return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width),
            h: Math.round(b.height), top: Math.round(b.top), bottom: Math.round(b.bottom)}; };
  const cs = (el, pseudo) => { if (!el) return null; const c = getComputedStyle(el, pseudo || null);
    return {display: c.display, position: c.position, color: c.color,
            backgroundImage: c.backgroundImage, textShadow: c.textShadow,
            fontSize: c.fontSize, fontFamily: c.fontFamily,
            webkitTextStroke: c.webkitTextStroke || c.getPropertyValue('-webkit-text-stroke'),
            filter: c.filter, opacity: c.opacity, transform: c.transform}; };
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
        hub = q('#hubNote'), input = q('#aliasInput'),
        agree = q('.cert-agree'), reader = q('#certInfoReader'),
        link = q('#displayLink'), mail = q('#displayMail'),
        linkLine = q('.link-line'), mailLine = q('.mail-line'),
        linkLabel = linkLine ? linkLine.querySelector('.id-box-label') : null,
        mailLabel = mailLine ? mailLine.querySelector('.id-box-label') : null,
        regalia = q('#certRegalia'), certNo = q('#certNoValue'),
        infoBtn = q('#certInfoBtn'), prog = q('#certInfoProg');
  const nr = textRects(name), tr = textRects(title), cr = textRects(cert);
  const hit = (a, b) => a.some(x => b.some(y => x.x < y.x + y.w && x.x + x.w > y.x &&
    x.y < y.y + y.h && x.y + x.h > y.y));
  // computed-color audit: every visible text-bearing element in the plaque
  const colors = {};
  plaque.querySelectorAll('*').forEach(el => {
    if (!el.childNodes.length) return;
    let hasText = false;
    for (const n of el.childNodes) if (n.nodeType === 3 && n.textContent.trim()) { hasText = true; break; }
    if (!hasText) return;
    const c = getComputedStyle(el);
    if (c.display === 'none' || el.closest('[hidden]')) return;
    const b = el.getBoundingClientRect();
    if (b.width === 0 && b.height === 0) return;
    const key = c.color + ' @' + c.fontSize;
    colors[key] = (colors[key] || 0) + 1;
  });
  const pb = plaque ? plaque.getBoundingClientRect() : null;
  const foot = q('.face-foot');
  const priv = q('.cert-privacy');
  return {
    plaqueClass: plaque ? plaque.className : null,
    plaqueBox: pb ? r(plaque) : null,
    status: st ? {state: st.getAttribute('data-state'), text: st.textContent} : null,
    marcellusLoaded: document.fonts ? document.fonts.check('52px Marcellus') : null,
    name: {box: r(name), style: cs(name), before: cs(name, '::before'),
           text: name ? name.textContent : null, dataText: name ? name.getAttribute('data-text') : null,
           hidden: name ? name.hidden : null, textRects: nr,
           settle: name ? name.classList.contains('name-settle') : null},
    title: {box: r(title), textRects: tr},
    certifies: {box: r(cert), textRects: cr},
    nameGlyphOverlapsTitle: hit(nr, tr),
    nameGlyphOverlapsCertifies: hit(nr, cr),
    linkPanel: linkLine ? {bg: getComputedStyle(linkLine).backgroundImage,
              border: getComputedStyle(linkLine).borderColor,
              labelColor: linkLabel ? getComputedStyle(linkLabel).color : null,
              labelText: linkLabel ? linkLabel.textContent : null,
              value: link ? link.textContent : null,
              valueColor: link ? getComputedStyle(link).color : null,
              typing: link ? link.classList.contains('typing') : null} : null,
    mailPanel: mailLine ? {bg: getComputedStyle(mailLine).backgroundImage,
              border: getComputedStyle(mailLine).borderColor,
              labelColor: mailLabel ? getComputedStyle(mailLabel).color : null,
              labelText: mailLabel ? mailLabel.textContent : null,
              value: mail ? mail.textContent : null,
              valueColor: mail ? getComputedStyle(mail).color : null,
              typing: mail ? mail.classList.contains('typing') : null} : null,
    agree: agree ? {box: r(agree), display: getComputedStyle(agree).display,
              text: agree.textContent.slice(0, 220),
              exact: agree.textContent.replace(/\\s+/g, ' ').includes('By entering your name, you make it official')} : null,
    infoBtn: infoBtn ? {box: r(infoBtn), display: getComputedStyle(infoBtn).display} : null,
    reader: reader ? {hidden: reader.hidden, box: r(reader),
              prog: prog ? prog.textContent : null,
              paras: reader.querySelectorAll('.cert-info-para').length,
              visibleParas: [...reader.querySelectorAll('.cert-info-para')].filter(p => !p.hidden).length} : null,
    regalia: regalia ? {hidden: regalia.hidden, certNo: certNo ? certNo.textContent : null} : null,
    enter: {box: r(btn), inViewport: btn ? (btn.getBoundingClientRect().bottom <= window.innerHeight && btn.getBoundingClientRect().top >= 0) : null},
    startOver: {box: r(so), style: cs(so)},
    hubNote: hub ? {hidden: hub.hidden, text: hub.textContent.slice(0, 90)} : null,
    inputValue: input ? input.value : null,
    footBottom: foot ? Math.round(foot.getBoundingClientRect().bottom) : null,
    privacyBottom: priv ? Math.round(priv.getBoundingClientRect().bottom) : null,
    plaqueScroll: plaque ? {scrollH: plaque.scrollHeight, clientH: plaque.clientHeight,
      scrollTop: plaque.scrollTop, overflowY: getComputedStyle(plaque).overflowY,
      scrollable: plaque.scrollHeight > plaque.clientHeight + 1} : null,
    overflowX: document.documentElement.scrollWidth - window.innerWidth,
    innerH: window.innerHeight, innerW: window.innerWidth,
    textColors: colors,
  };
}"""


def new_browser(pw, width, height):
    browser = pw.chromium.launch(headless=True, proxy={"server": "http://127.0.0.1:18080"})
    ctx = browser.new_context(viewport={"width": width, "height": height},
                              device_scale_factor=1, is_mobile=(width <= 640),
                              ignore_https_errors=True)
    return browser, ctx


def collect(page):
    console, failed = [], []
    page.on("console", lambda m: console.append(f"{m.type}: {m.text}"))
    page.on("pageerror", lambda e: console.append(f"PAGEERROR: {e}"))
    page.on("requestfailed", lambda r: failed.append(f"{r.url} :: {r.failure}"))
    page.on("response", lambda r: failed.append(f"{r.url} :: HTTP {r.status}") if r.status >= 400 else None)
    return console, failed


def dismiss_veil(page):
    try:
        vis = page.evaluate("!document.getElementById('installVeil').hidden")
        if vis:
            page.click("#installLater", timeout=3000)
            page.wait_for_timeout(400)
            return True
    except Exception:
        pass
    return False


def shot(page, name):
    p = os.path.join(SHOTDIR, name)
    page.screenshot(path=p, full_page=False)
    return p


def main():
    results = {}
    with sync_playwright() as pw:
        # ---- Flow A: fresh claim, one profile, 390 -> 1920 -> 390 -> 635
        browser, ctx = new_browser(pw, 390, 844)
        page = ctx.new_page()
        console, failed = collect(page)
        page.goto(FREE, wait_until="load", timeout=60000)
        page.wait_for_timeout(1200)
        dismiss_veil(page)
        page.fill("#aliasInput", ALIAS)
        page.wait_for_function(
            "document.getElementById('aliasStatus').getAttribute('data-state') === 'available'",
            timeout=20000)
        page.wait_for_timeout(1200)
        dismiss_veil(page)
        m_typed390 = page.evaluate(MEASURE_JS)
        shot(page, "typed-390x844.png")
        # reader: open, next, close
        page.click("#certInfoBtn", timeout=5000)
        page.wait_for_timeout(500)
        m_reader_open = page.evaluate(MEASURE_JS)
        shot(page, "reader-open-390x844.png")
        page.click("#certInfoNext", timeout=5000)
        page.wait_for_timeout(300)
        m_reader_next = page.evaluate(MEASURE_JS)
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)
        m_reader_closed = page.evaluate(MEASURE_JS)
        print(f"TYPED 390: status={m_typed390['status']} name={m_typed390['name']['text']!r} "
              f"dataText={m_typed390['name']['dataText']!r} marcellus={m_typed390['marcellusLoaded']}")
        print(f"  name color={m_typed390['name']['style']['color']} bg={m_typed390['name']['style']['backgroundImage'][:80]}")
        print(f"  name stroke={m_typed390['name']['style']['webkitTextStroke']} filter={m_typed390['name']['style']['filter']}")
        print(f"  clone content={m_typed390['name']['before']['backgroundImage'][:80]} opacity={m_typed390['name']['before']['opacity']}")
        print(f"  overlap title={m_typed390['nameGlyphOverlapsTitle']} certifies={m_typed390['nameGlyphOverlapsCertifies']}")
        print(f"  link panel bg={m_typed390['linkPanel']['bg'][:90]}")
        print(f"  link label {m_typed390['linkPanel']['labelColor']} value={m_typed390['linkPanel']['value']!r} color={m_typed390['linkPanel']['valueColor']}")
        print(f"  mail label {m_typed390['mailPanel']['labelColor']} value={m_typed390['mailPanel']['value']!r} color={m_typed390['mailPanel']['valueColor']}")
        print(f"  agree display={m_typed390['agree']['display']} box={m_typed390['agree']['box']} exact={m_typed390['agree']['exact']}")
        print(f"  reader open: hidden={m_reader_open['reader']['hidden']} paras={m_reader_open['reader']['paras']} visible={m_reader_open['reader']['visibleParas']} prog={m_reader_open['reader']['prog']}")
        print(f"  reader next: prog={m_reader_next['reader']['prog']} visible={m_reader_next['reader']['visibleParas']}")
        print(f"  reader closed: hidden={m_reader_closed['reader']['hidden']}")
        print(f"  ENTER inViewport={m_typed390['enter']['inViewport']} box={m_typed390['enter']['box']} footBottom={m_typed390['footBottom']} plaqueBottom={m_typed390['plaqueBox']['bottom'] if m_typed390['plaqueBox'] else None} overflowX={m_typed390['overflowX']}")
        print(f"  textColors={m_typed390['textColors']}")
        results["typed390"] = m_typed390
        results["readerOpen"] = m_reader_open
        results["readerNext"] = m_reader_next
        results["readerClosed"] = m_reader_closed

        # 1920: claim
        page.set_viewport_size({"width": 1920, "height": 1080})
        page.wait_for_timeout(800)
        dismiss_veil(page)
        page.click("#enterBtn", timeout=5000)
        try:
            page.wait_for_url(WALK + "*", timeout=30000)
            print("  claim -> redirected to walk (stamp landed)")
        except Exception as e:
            print(f"  claim redirect NOT seen: {e}")
        page.goto(FREE, wait_until="load", timeout=60000)
        page.wait_for_timeout(1200)
        dismiss_veil(page)
        try:
            page.wait_for_function(
                "document.getElementById('certPlaque').classList.contains('is-certified')",
                timeout=20000)
        except Exception as e:
            print(f"  certified restore NOT seen at 1920: {e}")
        page.wait_for_timeout(2500)  # let the typed values finish
        dismiss_veil(page)
        m_cert1920 = page.evaluate(MEASURE_JS)
        shot(page, "certified-1920x1080.png")
        # hover the name
        nb = m_cert1920["name"]["box"]
        if nb:
            page.mouse.move(nb["x"] + nb["w"] // 2, nb["y"] + nb["h"] // 2)
            page.wait_for_timeout(600)
            m_hover = page.evaluate(MEASURE_JS)
            shot(page, "certified-1920x1080-hover.png")
        else:
            m_hover = None
        print(f"CERTIFIED 1920: plaqueClass={m_cert1920['plaqueClass']} status={m_cert1920['status']} certNo={m_cert1920['regalia']}")
        print(f"  name text={m_cert1920['name']['text']!r} dataText={m_cert1920['name']['dataText']!r} settle={m_cert1920['name']['settle']} box={m_cert1920['name']['box']}")
        print(f"  name shadow={m_cert1920['name']['style']['textShadow']!r} filter={m_cert1920['name']['style']['filter']}")
        print(f"  clone opacity={m_cert1920['name']['before']['opacity']} bg={m_cert1920['name']['before']['backgroundImage'][:80]}")
        if m_hover:
            print(f"  HOVER filter={m_hover['name']['style']['filter']} transform={m_hover['name']['style']['transform']} cloneOpacity={m_hover['name']['before']['opacity']}")
        print(f"  link value={m_cert1920['linkPanel']['value']!r} mail value={m_cert1920['mailPanel']['value']!r} typing link={m_cert1920['linkPanel']['typing']} mail={m_cert1920['mailPanel']['typing']}")
        print(f"  agree display={m_cert1920['agree']['display']} (must be none on certified)")
        print(f"  ENTER inViewport={m_cert1920['enter']['inViewport']} box={m_cert1920['enter']['box']} overflowX={m_cert1920['overflowX']}")
        print(f"  textColors={m_cert1920['textColors']}")
        results["cert1920"] = m_cert1920
        if m_hover:
            results["cert1920hover"] = m_hover

        # 390 certified restore
        page.set_viewport_size({"width": 390, "height": 844})
        page.reload(wait_until="load", timeout=60000)
        page.wait_for_timeout(1200)
        dismiss_veil(page)
        page.wait_for_function(
            "document.getElementById('certPlaque').classList.contains('is-certified')",
            timeout=20000)
        page.wait_for_timeout(2500)
        dismiss_veil(page)
        m_cert390 = page.evaluate(MEASURE_JS)
        shot(page, "certified-390x844.png")
        print(f"CERTIFIED 390: name box={m_cert390['name']['box']} text={m_cert390['name']['text']!r}")
        print(f"  overlap title={m_cert390['nameGlyphOverlapsTitle']} certifies={m_cert390['nameGlyphOverlapsCertifies']}")
        print(f"  ENTER inViewport={m_cert390['enter']['inViewport']} box={m_cert390['enter']['box']} overflowX={m_cert390['overflowX']}")
        print(f"  textColors={m_cert390['textColors']}")
        results["cert390"] = m_cert390

        # 635x349 certified restore + wheel ENTER reachability
        page.set_viewport_size({"width": 635, "height": 349})
        page.reload(wait_until="load", timeout=60000)
        page.wait_for_timeout(1200)
        dismiss_veil(page)
        page.wait_for_function(
            "document.getElementById('certPlaque').classList.contains('is-certified')",
            timeout=20000)
        page.wait_for_timeout(1500)
        dismiss_veil(page)
        m_cert635 = page.evaluate(MEASURE_JS)
        shot(page, "certified-635x349-load.png")
        before = m_cert635["plaqueScroll"]["scrollTop"]
        page.mouse.move(635 // 2, 349 // 2)
        for _ in range(3):
            page.mouse.wheel(0, 400)
            page.wait_for_timeout(250)
        dismiss_veil(page)
        m_cert635s = page.evaluate(MEASURE_JS)
        shot(page, "certified-635x349-scrolled.png")
        print(f"CERTIFIED 635: ENTER load inViewport={m_cert635['enter']['inViewport']} box={m_cert635['enter']['box']}")
        print(f"  wheel scrollTop {before} -> {m_cert635s['plaqueScroll']['scrollTop']}; ENTER after wheel inViewport={m_cert635s['enter']['inViewport']} box={m_cert635s['enter']['box']}")
        print(f"  overflowX={m_cert635['overflowX']} textColors={m_cert635['textColors']}")
        results["cert635"] = m_cert635
        results["cert635scrolled"] = m_cert635s
        print(f"FLOW A console ({len(console)}): {console[:20]}")
        print(f"FLOW A failed ({len(failed)}): {failed[:20]}")
        results["consoleA"] = console
        results["failedA"] = failed
        browser.close()

        # ---- Flow B: taken regression, fresh profile, same alias
        browser, ctx = new_browser(pw, 390, 844)
        page = ctx.new_page()
        console, failed = collect(page)
        page.goto(FREE, wait_until="load", timeout=60000)
        page.wait_for_timeout(1200)
        dismiss_veil(page)
        page.fill("#aliasInput", ALIAS)
        page.wait_for_function(
            "document.getElementById('aliasStatus').getAttribute('data-state') === 'taken'",
            timeout=20000)
        page.wait_for_timeout(1200)
        dismiss_veil(page)
        m_taken = page.evaluate(MEASURE_JS)
        shot(page, "taken-390x844.png")
        print(f"TAKEN 390: status={m_taken['status']} name={m_taken['name']['text']!r} dataText={m_taken['name']['dataText']!r}")
        print(f"  name textShadow={m_taken['name']['style']['textShadow']!r} (must be none — clone carries the glow)")
        print(f"  clone bg={m_taken['name']['before']['backgroundImage'][:80]} opacity={m_taken['name']['before']['opacity']}")
        print(f"  name box={m_taken['name']['box']} overlap title={m_taken['nameGlyphOverlapsTitle']} certifies={m_taken['nameGlyphOverlapsCertifies']}")
        print(f"  ENTER inViewport={m_taken['enter']['inViewport']} box={m_taken['enter']['box']} startOver={m_taken['startOver']['style']['display']}")
        print(f"FLOW B console ({len(console)}): {console[:10]}")
        print(f"FLOW B failed ({len(failed)}): {failed[:10]}")
        results["taken390"] = m_taken
        results["consoleB"] = console
        results["failedB"] = failed
        browser.close()

    with open(os.path.join(HERE, "probe-certificate.json"), "w") as f:
        json.dump(results, f, indent=1)
    print("PROBE DONE — results in probe-certificate.json, shots in shots/")


if __name__ == "__main__":
    main()
