#!/usr/bin/env python3
"""Captain's eye fix-5 — drive 1b: unfold diagnosis + completion (phone 390, staged).
Fixes drive-1's selector miss on /agreement (no #fpNextBtn there), proves the bridge
strip through the real tap path, deck + letter D/E with visible-only faces,
anthem/Listen, and the intro strip in a FRESH browser (no agreed-state restore).
Writes eye-log1b.json."""
import json, time
from playwright.sync_api import sync_playwright

BASE = "https://naya-walk-beginning-staging.nayapower.workers.dev"
EYE = "/home/hatch/workspace/team-nitro/walkthrough-agreement-distill-fix5-20261119/eye"
LOGP = EYE + "/eye-log1b.json"

GEO_SWEEP = r"""() => {
  const nav = document.querySelector('#fpLegal .fp-legal-links');
  if (!nav) return {error: 'no nav'};
  const cs = getComputedStyle(nav);
  const nr = nav.getBoundingClientRect();
  const links = [...nav.querySelectorAll('a, button')].map(el => el.textContent.trim());
  const max = nav.scrollWidth - nav.clientWidth;
  const seenVP = links.map(() => null);
  const seenStrip = links.map(() => null);
  const positions = [0];
  for (let s = 50; s < max; s += 50) positions.push(s);
  if (max > 0) positions.push(max);
  for (const sl of positions) {
    nav.scrollLeft = sl;
    const actual = nav.scrollLeft;
    const rects = [...nav.querySelectorAll('a, button')].map(el => {
      const r = el.getBoundingClientRect();
      return {left: Math.round(r.left), right: Math.round(r.right)};
    });
    rects.forEach((rc, i) => {
      if (rc.left >= 0 && rc.right <= 390 && seenVP[i] === null) seenVP[i] = actual;
      if (rc.left >= Math.round(nr.left) && rc.right <= Math.round(nr.right) && seenStrip[i] === null) seenStrip[i] = actual;
    });
  }
  nav.scrollLeft = 0;
  const reachVP = seenVP.map((s, i) => ({link: links[i], reachable: s !== null, at: s}));
  const reachStrip = seenStrip.map((s, i) => ({link: links[i], reachable: s !== null, at: s}));
  return {navRect: [Math.round(nr.left), Math.round(nr.top), Math.round(nr.right), Math.round(nr.bottom)],
    scrollWidth: nav.scrollWidth, clientWidth: nav.clientWidth, maxScroll: max,
    justifyContent: cs.justifyContent, flexWrap: cs.flexWrap, overflowX: cs.overflowX,
    linkCount: links.length, links,
    reachableViewport: reachVP, unreachableViewport: reachVP.filter(r => !r.reachable).length,
    reachableStrip: reachStrip, unreachableStrip: reachStrip.filter(r => !r.reachable).length};
}"""

def counter(page):
    return page.evaluate("() => { const m = document.body.innerText.match(/(\\d+)\\s*\\/\\s*37/); return m ? m[0] : null; }")

def settle_counter(page, timeout=3000):
    end = time.time() + timeout / 1000
    last = None; stable = 0
    while time.time() < end:
        c = counter(page)
        if c is not None and c == last:
            stable += 1
            if stable >= 2: return c
        else:
            stable = 0
        last = c
        page.wait_for_timeout(120)
    return last

def walk_next_text(page, label, max_clicks=45):
    seen = []
    for i in range(max_clicks):
        c = settle_counter(page)
        if c and (not seen or seen[-1] != c): seen.append(c)
        if page.evaluate("() => [...document.querySelectorAll('button')].some(x=>x.offsetParent!==null && /I agree/i.test(x.innerText))"):
            return {"label": label, "seen": seen, "endBtn": "I agree",
                    "sequential": seen == [f"{n} / 37" for n in range(1, len(seen) + 1)]}
        page.locator("button", has_text="Next").locator("visible=true").first.click(timeout=5000)
        page.wait_for_timeout(350)
    return {"label": label, "seen": seen, "endBtn": None,
            "sequential": seen == [f"{n} / 37" for n in range(1, len(seen) + 1)]}

def walk_fpnext(page, label, max_clicks=45):
    seen = []
    for i in range(max_clicks):
        c = settle_counter(page)
        if c and (not seen or seen[-1] != c): seen.append(c)
        btn = page.evaluate("() => { const b = document.querySelector('#fpNextBtn'); return b && b.offsetParent !== null ? b.innerText.trim() : null; }")
        if btn is None: break
        if any(k in btn for k in ("Enter NayaNET", "I agree", "Read the Collective")):
            return {"label": label, "seen": seen, "endBtn": btn,
                    "sequential": seen == [f"{n} / 37" for n in range(1, len(seen) + 1)]}
        page.locator("#fpNextBtn").click(timeout=6000)
        page.wait_for_timeout(300)
    btn = page.evaluate("() => { const b = document.querySelector('#fpNextBtn'); return b ? b.innerText.trim() : null; }")
    return {"label": label, "seen": seen, "endBtn": btn,
            "sequential": seen == [f"{n} / 37" for n in range(1, len(seen) + 1)]}

TITLE_LINES_JS = r"""(t) => {
  const range = document.createRange(); const byTop = {};
  const walk = document.createTreeWalker(t, NodeFilter.SHOW_TEXT); let node;
  while ((node = walk.nextNode())) {
    for (let i = 0; i < node.textContent.length; i++) {
      range.setStart(node, i); range.setEnd(node, i + 1);
      const r = range.getBoundingClientRect();
      if (r.width > 0 && r.height > 0) { const tt = Math.round(r.top);
        byTop[tt] = byTop[tt] || [Math.round(r.left), tt, Math.round(r.right), Math.round(r.bottom)];
        byTop[tt][0] = Math.min(byTop[tt][0], Math.round(r.left)); byTop[tt][2] = Math.max(byTop[tt][2], Math.round(r.right)); }
    }
  }
  return Object.values(byTop);
}"""

def d_measure(page, which):
    return page.evaluate(r"""() => {
      const R = el => { if (!el) return null; const b = el.getBoundingClientRect();
        return [Math.round(b.left), Math.round(b.top), Math.round(b.right), Math.round(b.bottom)]; };
      const ov = (a,b) => { if (!a || !b) return null;
        return Math.round(Math.max(0, Math.min(a[2],b[2])-Math.max(a[0],b[0])) * Math.max(0, Math.min(a[3],b[3])-Math.max(a[1],b[1]))); };
      const vis = sel => [...document.querySelectorAll(sel)].filter(e => e.offsetParent !== null);
      const titles = vis('.frame-title, .ib-title').filter(e => /Congratulations/.test(e.textContent));
      const orb = vis('.frame-icon')[0] || null;
      const face = vis('.deal-beat-photo.fp-speak-face')[0] || null;
      const nuts = vis('.ib-nutshell').map(R);
      const photos = vis('.deal-sign-photo').map(R);
      const t = titles[0] || null;
      let lines = null;
      if (t) {
        const range = document.createRange(); const byTop = {};
        const walk = document.createTreeWalker(t, NodeFilter.SHOW_TEXT); let node;
        while ((node = walk.nextNode())) {
          for (let i = 0; i < node.textContent.length; i++) {
            range.setStart(node, i); range.setEnd(node, i + 1);
            const r = range.getBoundingClientRect();
            if (r.width > 0 && r.height > 0) { const tt = Math.round(r.top);
              byTop[tt] = byTop[tt] || [Math.round(r.left), tt, Math.round(r.right), Math.round(r.bottom)];
              byTop[tt][0] = Math.min(byTop[tt][0], Math.round(r.left)); byTop[tt][2] = Math.max(byTop[tt][2], Math.round(r.right)); }
          }
        }
        lines = Object.values(byTop);
      }
      return {titleFont: t ? getComputedStyle(t).fontSize : null, titleLines: lines,
        orbRect: R(orb), faceRect: R(face),
        titleOrbOverlap: (lines && lines.length && orb) ? Math.max(...lines.map(ln => ov(ln, R(orb)))) : null,
        titleFaceClear: (lines && lines.length && face) ? R(face)[0] - Math.max(...lines.map(ln => ln[2])) : null,
        nutshell: nuts, photos,
        nutshellPhotoOverlap: (nuts.length && photos.length) ? ov(nuts[0], photos[0]) : null};
    }""")

out = {"label": "EYE-FIX5-PHONE390-DRIVE1B", "legs": []}
def leg(name, fn):
    try:
        out["legs"].append({"leg": name, **fn()})
        print("LEG OK", name, flush=True)
    except Exception as e:
        out["legs"].append({"leg": name, "ERROR": str(e)[:600]})
        print("LEG FAIL", name, str(e)[:300], flush=True)

with sync_playwright() as pw:
    b = pw.firefox.launch(headless=True)
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, ignore_https_errors=True)
    page = ctx.new_page()
    errs = []
    page.on("pageerror", lambda e: errs.append("pageerror: " + str(e)[:200]))
    page.on("console", lambda m: errs.append("console." + m.type + ": " + m.text[:200]) if m.type == "error" else None)

    def leg_agree_dump():
        page.goto(BASE + "/agreement", timeout=60000); page.wait_for_timeout(2000)
        return page.evaluate("""() => ({
          fpNextBtnExists: !!document.querySelector('#fpNextBtn'),
          fpNextBtnVisible: (() => { const b = document.querySelector('#fpNextBtn'); return b ? b.offsetParent !== null : null; })(),
          counter: (document.body.innerText.match(/(\\d+)\\s*\\/\\s*37/) || [null])[0],
          visibleButtons: [...document.querySelectorAll('button')].filter(x=>x.offsetParent!==null).map(x=>({id: x.id || null, text: x.innerText.trim().slice(0,40), aria: x.getAttribute('aria-label') || null}))
        })""")
    leg("agree-controls-dump", leg_agree_dump)

    def leg_unfold():
        page.screenshot(path=EYE + "/eye-16-unfold-board1.png")
        r = walk_next_text(page, "unfold")
        page.screenshot(path=EYE + "/eye-17-unfold-board37.png")
        return {**r, "D-unfold": d_measure(page, "unfold")}
    leg("unfold-1-37-D", leg_unfold)

    def leg_agree_f():
        page.locator("button", has_text="I agree").locator("visible=true").first.click(timeout=5000)
        page.wait_for_timeout(2500)
        geo = page.evaluate(GEO_SWEEP)
        page.evaluate("() => { const n = document.querySelector('#fpLegal .fp-legal-links'); if (n) n.scrollLeft = 0; }")
        page.wait_for_timeout(400)
        page.screenshot(path=EYE + "/eye-18-bridge-s0.png")
        page.evaluate("() => { const n = document.querySelector('#fpLegal .fp-legal-links'); if (n) n.scrollLeft = n.scrollWidth; }")
        page.wait_for_timeout(400)
        page.screenshot(path=EYE + "/eye-19-bridge-smax.png")
        return {"url": page.url, "pair": page.evaluate("() => [...document.querySelectorAll('button')].filter(x=>x.offsetParent!==null).map(x=>x.innerText.trim()).filter(t=>/Begin the visual story|Read the agreement/.test(t))"),
                "F-bridge-real-tap": geo}
    leg("F-bridge-real-tap", leg_agree_f)

    def leg_deck():
        page.locator("button", has_text="Begin the visual story").locator("visible=true").first.click(timeout=5000)
        page.wait_for_timeout(2500)
        r = walk_fpnext(page, "deck")
        page.screenshot(path=EYE + "/eye-20-deck37.png")
        return {**r, "D-E-deck": d_measure(page, "deck")}
    leg("deck-1-37-D-E", leg_deck)

    def leg_deck_end():
        page.locator("#fpNextBtn").click(timeout=6000)
        page.wait_for_timeout(3000)
        return {"url": page.url, "pair": page.evaluate("() => [...document.querySelectorAll('button')].filter(x=>x.offsetParent!==null).map(x=>x.innerText.trim()).filter(t=>/Begin the visual story|Read the agreement/.test(t))")}
    leg("deck-enter-bridge", leg_deck_end)

    def leg_read_agree():
        page.locator("button", has_text="Read the agreement").locator("visible=true").first.click(timeout=5000)
        page.wait_for_timeout(2500)
        return {"counter": counter(page), "url": page.url}
    leg("pair-read-agreement", leg_read_agree)

    def leg_letter2():
        page.goto(BASE + "/?stage=letter", timeout=60000); page.wait_for_timeout(2500)
        r = walk_fpnext(page, "letter")
        page.screenshot(path=EYE + "/eye-21-letter37.png")
        return {**r, "D-E-letter": d_measure(page, "letter")}
    leg("letter-1-37-D-E-visible-face", leg_letter2)

    def leg_anthem():
        page.goto(BASE + "/agreement", timeout=60000); page.wait_for_timeout(2000)
        before = page.evaluate("() => [...document.querySelectorAll('button')].filter(x=>x.offsetParent!==null).map(x=>({id: x.id || null, text: x.innerText.trim().slice(0,44), aria: x.getAttribute('aria-label') || null}))")
        page.locator("button", has_text="Watch the anthem").locator("visible=true").first.click(timeout=5000)
        page.wait_for_timeout(1500)
        anthem = page.evaluate("() => ({anthemText: document.body.innerText.includes('How much of your digital life feels scattered'), iframes: document.querySelectorAll('iframe').length, videos: document.querySelectorAll('video').length})")
        page.screenshot(path=EYE + "/eye-22-after-anthem.png")
        after = page.evaluate("() => [...document.querySelectorAll('button')].filter(x=>x.offsetParent!==null).map(x=>({id: x.id || null, text: x.innerText.trim().slice(0,44), aria: x.getAttribute('aria-label') || null}))")
        listen = None
        try:
            page.get_by_role("button", name="Play — read the agreement with Naya").first.click(timeout=5000)
            page.wait_for_timeout(1500)
            listen = {"via": "aria-label", "ok": True}
        except Exception as e:
            listen = {"via": "aria-label", "ok": False, "error": str(e)[:200]}
            try:
                page.locator("button", has_text="Listen to the agreement").locator("visible=true").first.click(timeout=5000)
                page.wait_for_timeout(1500)
                listen = {"via": "text-fallback", "ok": True}
            except Exception as e2:
                listen = {"via": "text-fallback", "ok": False, "error": str(e2)[:200]}
        listen_state = page.evaluate("() => ({listenText: document.body.innerText.includes(\"Naya's reading arrives\"), audios: document.querySelectorAll('audio').length})")
        page.screenshot(path=EYE + "/eye-23-after-listen.png")
        return {"before": before, "anthem": anthem, "afterAnthemButtons": after, "listen": listen, "listenState": listen_state}
    leg("anthem-listen-diag", leg_anthem)
    b.close()

    # ---- intro strip in a FRESH browser (no agreed-state restore) ----
    b2 = pw.firefox.launch(headless=True)
    ctx2 = b2.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, ignore_https_errors=True)
    pg2 = ctx2.new_page()
    errs2 = []
    pg2.on("pageerror", lambda e: errs2.append("pageerror: " + str(e)[:200]))
    pg2.on("console", lambda m: errs2.append("console." + m.type + ": " + m.text[:200]) if m.type == "error" else None)
    def leg_intro_fresh():
        pg2.goto(BASE + "/", timeout=60000); pg2.wait_for_timeout(3000)
        cold = pg2.evaluate("() => { const f = document.querySelector('#fpLegal'); return {fpLegalDisplay: f ? getComputedStyle(f).display : 'MISSING'}; }")
        pg2.goto(BASE + "/?stage=intro", timeout=60000); pg2.wait_for_timeout(3000)
        param = pg2.evaluate("() => { const f = document.querySelector('#fpLegal'); return {fpLegalDisplay: f ? getComputedStyle(f).display : 'MISSING'}; }")
        pg2.goto(BASE + "/", timeout=60000); pg2.wait_for_timeout(3000)
        act = pg2.evaluate("() => { if (window.__fpStage && window.__fpStage.enter) { window.__fpStage.enter(); return {entered: true}; } return {entered: false}; }")
        pg2.wait_for_timeout(2500)
        state = pg2.evaluate("() => ({bodyClass: document.body.className, fpLegalDisplay: (() => { const f = document.querySelector('#fpLegal'); return f ? getComputedStyle(f).display : 'MISSING'; })(), choicePills: [...document.querySelectorAll('button')].filter(x=>x.offsetParent!==null).map(x=>x.innerText.trim()).filter(t=>/Begin the visual story|Read the agreement/.test(t))})")
        geo = pg2.evaluate(GEO_SWEEP)
        pg2.evaluate("() => { const n = document.querySelector('#fpLegal .fp-legal-links'); if (n) n.scrollLeft = 0; }")
        pg2.wait_for_timeout(400)
        pg2.screenshot(path=EYE + "/eye-24-intro-s0.png")
        pg2.evaluate("() => { const n = document.querySelector('#fpLegal .fp-legal-links'); if (n) n.scrollLeft = n.scrollWidth; }")
        pg2.wait_for_timeout(400)
        pg2.screenshot(path=EYE + "/eye-25-intro-smax.png")
        return {"coldFresh": cold, "param": param, "activation": act, "state": state, "F-intro-fresh": geo, "consoleErrors": errs2}
    leg("F-intro-fresh-browser", leg_intro_fresh)
    b2.close()

    out["legs"].append({"leg": "390-console-errors-drive1b", "errors": errs})
    with open(LOGP, "w") as f:
        json.dump(out, f, indent=1)
    print("WROTE", LOGP)
    for l in out["legs"]:
        print(json.dumps(l)[:900], flush=True)
