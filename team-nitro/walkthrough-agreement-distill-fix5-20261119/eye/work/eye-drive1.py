#!/usr/bin/env python3
"""Captain's eye — Agreement distill fix-5. Phone 390x844 FIRST, staged host.
My own driver, my own taps, my own rects and screenshots. Writes eye-log1.json."""
import json, re, secrets, time
from playwright.sync_api import sync_playwright

BASE = "https://naya-walk-beginning-staging.nayapower.workers.dev"
EYE = "/home/hatch/workspace/team-nitro/walkthrough-agreement-distill-fix5-20261119/eye"
LOGP = EYE + "/eye-log1.json"
ALIAS = "eye5walk" + secrets.token_hex(3)

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

LINE_RECTS = r"""(el) => {
  const range = document.createRange(); const byTop = {};
  const walk = document.createTreeWalker(el, NodeFilter.SHOW_TEXT); let node;
  while ((node = walk.nextNode())) {
    for (let i = 0; i < node.textContent.length; i++) {
      range.setStart(node, i); range.setEnd(node, i + 1);
      const r = range.getBoundingClientRect();
      if (r.width > 0 && r.height > 0) { const t = Math.round(r.top);
        byTop[t] = byTop[t] || [Math.round(r.left), t, Math.round(r.right), Math.round(r.bottom)];
        byTop[t][0] = Math.min(byTop[t][0], Math.round(r.left)); byTop[t][2] = Math.max(byTop[t][2], Math.round(r.right)); }
    }
  }
  return Object.values(byTop);
}"""

R = r"""(el) => { if (!el) return null; const b = el.getBoundingClientRect();
  return [Math.round(b.left), Math.round(b.top), Math.round(b.right), Math.round(b.bottom)]; }"""

def ov(a, b):
    if not a or not b: return None
    return round(max(0, min(a[2], b[2]) - max(a[0], b[0])) * max(0, min(a[3], b[3]) - max(a[1], b[1])))

def counter(page):
    m = page.evaluate("() => { const m = document.body.innerText.match(/(\\d+)\\s*\\/\\s*37/); return m ? m[0] : null; }")
    return m

def settle_counter(page, timeout=3000):
    """Wait until the counter text is present and stable across two polls."""
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

def walk_stage(page, label, max_clicks=45):
    """Real taps on #fpNextBtn until the end button appears. Returns seen counters + end text."""
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

out = {"label": "EYE-FIX5-PHONE390", "alias": ALIAS, "legs": []}
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

    def leg_root():
        page.goto(BASE + "/", timeout=60000); page.wait_for_timeout(2500)
        page.screenshot(path=EYE + "/eye-01-root-390.png")
        return page.evaluate("""() => ({title: document.title, scrollW: document.documentElement.scrollWidth,
          innerW: window.innerWidth, hasAgreement: document.body.innerText.includes('The Collective Agreement'),
          buttons: [...document.querySelectorAll('button')].filter(x=>x.offsetParent!==null).map(x=>x.innerText.trim()).slice(0,20)})""")
    leg("1-root", leg_root)

    def leg_ident_paired():
        page.goto(BASE + "/identity.html?name=Shawn&alias=Shawn", timeout=60000); page.wait_for_timeout(2500)
        page.screenshot(path=EYE + "/eye-02-identity-paired.png")
        return page.evaluate(r"""() => {
          const R = el => { if (!el) return null; const b = el.getBoundingClientRect();
            return [Math.round(b.left), Math.round(b.top), Math.round(b.right), Math.round(b.bottom)]; };
          const ov = (a,b) => { if (!a || !b) return null;
            return Math.round(Math.max(0, Math.min(a[2],b[2])-Math.max(a[0],b[0])) * Math.max(0, Math.min(a[3],b[3])-Math.max(a[1],b[1]))); };
          const inp = document.querySelector('input'), hero = document.querySelector('#displayName'),
                title = document.querySelector('.cert-title'), cert = document.querySelector('.cert-certifies');
          return {input: inp ? inp.value : null, hero: hero ? hero.textContent.trim() : null,
            heroVisible: hero ? hero.offsetParent !== null : null, dataText: hero ? hero.getAttribute('data-text') : null,
            heroRect: R(hero), titleRect: R(title), heroTitleOverlap: ov(R(hero), R(title)),
            gap: R(hero) && R(title) ? R(hero)[1] - R(title)[3] : null,
            certifiesDisplay: cert ? getComputedStyle(cert).display : null,
            scrollW: document.documentElement.scrollWidth, innerW: window.innerWidth};
        }""")
    leg("A-identity-paired", leg_ident_paired)

    def leg_ident_nameonly():
        page.goto(BASE + "/identity.html?name=Shawn", timeout=60000); page.wait_for_timeout(2500)
        return page.evaluate("() => { const inp = document.querySelector('input'); const hero = document.querySelector('#displayName'); return {input: inp ? inp.value : null, hero: hero ? hero.textContent.trim() : null, heroVisible: hero ? hero.offsetParent !== null : null}; }")
    leg("identity-name-only", leg_ident_nameonly)

    def leg_ident_plain():
        page.goto(BASE + "/identity.html", timeout=60000); page.wait_for_timeout(2500)
        return page.evaluate("() => { const hero = document.querySelector('#displayName'); return {heroVisible: hero ? hero.offsetParent !== null : null, showsCertifies: document.body.innerText.includes('This certifies that')}; }")
    leg("identity-plain", leg_ident_plain)

    def leg_c_banner():
        page.goto(BASE + "/identity.html?name=Shawn&alias=Shawn", timeout=60000); page.wait_for_timeout(2500)
        page.evaluate("() => { const n = document.querySelector('.hub-note.taken-note'); if (n) n.scrollIntoView({block:'center'}); }")
        page.wait_for_timeout(800)
        page.screenshot(path=EYE + "/eye-03-banner.png")
        return page.evaluate(r"""() => {
          const R = el => { if (!el) return null; const b = el.getBoundingClientRect();
            return [Math.round(b.left), Math.round(b.top), Math.round(b.right), Math.round(b.bottom)]; };
          const ov = (a,b) => { if (!a || !b) return null;
            return Math.round(Math.max(0, Math.min(a[2],b[2])-Math.max(a[0],b[0])) * Math.max(0, Math.min(a[3],b[3])-Math.max(a[1],b[1]))); };
          const note = document.querySelector('.hub-note.taken-note');
          const stone = document.querySelector('.cert-plaque.taken .frame-stone');
          const crests = [...document.querySelectorAll('.p3-crest-tl, .p3-crest-tr, .cert-crest, [class*=crest]')].filter(e => e.offsetParent !== null).map(R);
          const range = document.createRange(); const byTop = {};
          const walk = document.createTreeWalker(note, NodeFilter.SHOW_TEXT); let node;
          while ((node = walk.nextNode())) {
            for (let i = 0; i < node.textContent.length; i++) {
              range.setStart(node, i); range.setEnd(node, i + 1);
              const r = range.getBoundingClientRect();
              if (r.width > 0 && r.height > 0) { const t = Math.round(r.top);
                byTop[t] = byTop[t] || [Math.round(r.left), t, Math.round(r.right), Math.round(r.bottom)];
                byTop[t][0] = Math.min(byTop[t][0], Math.round(r.left)); byTop[t][2] = Math.max(byTop[t][2], Math.round(r.right)); }
            }
          }
          const lines = Object.values(byTop);
          return {noteText: note ? note.textContent.replace(/\s+/g,' ').trim().slice(0,140) : null,
            lines, crestOverlaps: lines.map(ln => Math.max(0, ...crests.map(c => ov(ln, c)))),
            stoneDisplay: stone ? getComputedStyle(stone).display : 'absent',
            stoneOverlap: stone ? Math.max(0, ...lines.map(ln => ov(ln, R(stone)))) : null};
        }""")
    leg("C-banner", leg_c_banner)

    def leg_door():
        page.goto(BASE + f"/welcome?name=Eye%20Five&alias={ALIAS}", timeout=60000); page.wait_for_timeout(2000)
        steps0 = page.evaluate("() => [...document.querySelectorAll('[id^=step-]')].filter(e=>e.offsetParent!==null).map(e=>e.id)")
        page.wait_for_timeout(10000)
        steps10 = page.evaluate("() => [...document.querySelectorAll('[id^=step-]')].filter(e=>e.offsetParent!==null).map(e=>e.id)")
        page.screenshot(path=EYE + "/eye-04-door.png")
        bmeas = page.evaluate(r"""() => {
          const R = el => { if (!el) return null; const b = el.getBoundingClientRect();
            return [Math.round(b.left), Math.round(b.top), Math.round(b.right), Math.round(b.bottom)]; };
          const ov = (a,b) => { if (!a || !b) return null;
            return Math.round(Math.max(0, Math.min(a[2],b[2])-Math.max(a[0],b[0])) * Math.max(0, Math.min(a[3],b[3])-Math.max(a[1],b[1]))); };
          const h = document.querySelector('#step-door .p3-question');
          const tl = document.querySelector('.p3-crest-tl'), tr = document.querySelector('.p3-crest-tr');
          const range = document.createRange(); const byTop = {};
          const walk = document.createTreeWalker(h, NodeFilter.SHOW_TEXT); let node;
          while ((node = walk.nextNode())) {
            for (let i = 0; i < node.textContent.length; i++) {
              range.setStart(node, i); range.setEnd(node, i + 1);
              const r = range.getBoundingClientRect();
              if (r.width > 0 && r.height > 0) { const t = Math.round(r.top);
                byTop[t] = byTop[t] || [Math.round(r.left), t, Math.round(r.right), Math.round(r.bottom)];
                byTop[t][0] = Math.min(byTop[t][0], Math.round(r.left)); byTop[t][2] = Math.max(byTop[t][2], Math.round(r.right)); }
            }
          }
          const lines = Object.values(byTop);
          return {heading: h ? h.textContent.replace(/\s+/g,' ').trim() : null,
            padding: h ? [getComputedStyle(h).paddingLeft, getComputedStyle(h).paddingRight] : null,
            lines, crestOverlap: lines.map(ln => Math.max(ov(ln, R(tl)), ov(ln, R(tr))))};
        }""")
        return {"at0": steps0, "at10s": steps10, "held": steps0 == steps10, "B": bmeas}
    leg("B-door-10s-hold", leg_door)

    def leg_continue():
        page.locator("#doorContinue").click(timeout=6000)
        page.wait_for_timeout(1500)
        page.screenshot(path=EYE + "/eye-05-after-continue.png")
        return {"visibleSteps": page.evaluate("() => [...document.querySelectorAll('[id^=step-]')].filter(e=>e.offsetParent!==null).map(e=>e.id)")}
    leg("door-continue-step1", leg_continue)

    def leg_unfold():
        page.goto(BASE + "/agreement", timeout=60000); page.wait_for_timeout(2000)
        page.screenshot(path=EYE + "/eye-06-unfold-board1.png")
        r = walk_stage(page, "unfold")
        page.screenshot(path=EYE + "/eye-07-unfold-board37.png")
        d = page.evaluate(r"""() => {
          const R = el => { if (!el) return null; const b = el.getBoundingClientRect();
            return [Math.round(b.left), Math.round(b.top), Math.round(b.right), Math.round(b.bottom)]; };
          const titles = [...document.querySelectorAll('.frame-title, .ib-title')].filter(e => e.offsetParent !== null && /Congratulations/.test(e.textContent));
          const orb = document.querySelector('.frame-icon');
          const out = titles.map(t => {
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
            return {font: getComputedStyle(t).fontSize, lines: Object.values(byTop)};
          });
          return {titles: out, orbRect: R(orb)};
        }""")
        return {**r, "D-unfold": d}
    leg("unfold-1-37-D", leg_unfold)

    def leg_agree_bridge_f():
        page.locator("button", has_text="I agree").locator("visible=true").first.click(timeout=5000)
        page.wait_for_timeout(2500)
        geo = page.evaluate(GEO_SWEEP)
        page.evaluate("() => { const n = document.querySelector('#fpLegal .fp-legal-links'); if (n) n.scrollLeft = 0; }")
        page.wait_for_timeout(400)
        page.screenshot(path=EYE + "/eye-08-bridge-s0.png")
        page.evaluate("() => { const n = document.querySelector('#fpLegal .fp-legal-links'); if (n) n.scrollLeft = n.scrollWidth; }")
        page.wait_for_timeout(400)
        page.screenshot(path=EYE + "/eye-09-bridge-smax.png")
        return {"url": page.url, "pair": page.evaluate("() => [...document.querySelectorAll('button')].filter(x=>x.offsetParent!==null).map(x=>x.innerText.trim()).filter(t=>/Begin the visual story|Read the agreement/.test(t))"),
                "F-bridge": geo, "scrollW": page.evaluate("() => document.documentElement.scrollWidth"), "innerW": page.evaluate("() => window.innerWidth")}
    leg("F-bridge-strip", leg_agree_bridge_f)

    def leg_deck():
        page.locator("button", has_text="Begin the visual story").locator("visible=true").first.click(timeout=5000)
        page.wait_for_timeout(2500)
        r = walk_stage(page, "deck")
        page.screenshot(path=EYE + "/eye-10-deck37.png")
        m = page.evaluate(r"""() => {
          const R = el => { if (!el) return null; const b = el.getBoundingClientRect();
            return [Math.round(b.left), Math.round(b.top), Math.round(b.right), Math.round(b.bottom)]; };
          const ov = (a,b) => { if (!a || !b) return null;
            return Math.round(Math.max(0, Math.min(a[2],b[2])-Math.max(a[0],b[0])) * Math.max(0, Math.min(a[3],b[3])-Math.max(a[1],b[1]))); };
          const nuts = [...document.querySelectorAll('.ib-nutshell')].filter(e => e.offsetParent !== null).map(R);
          const photos = [...document.querySelectorAll('.deal-sign-photo')].filter(e => e.offsetParent !== null).map(R);
          const titles = [...document.querySelectorAll('.frame-title, .ib-title')].filter(e => e.offsetParent !== null && /Congratulations/.test(e.textContent));
          const t = titles[0];
          const range = document.createRange(); const byTop = {};
          if (t) { const walk = document.createTreeWalker(t, NodeFilter.SHOW_TEXT); let node;
            while ((node = walk.nextNode())) { for (let i = 0; i < node.textContent.length; i++) {
              range.setStart(node, i); range.setEnd(node, i + 1); const r = range.getBoundingClientRect();
              if (r.width > 0 && r.height > 0) { const tt = Math.round(r.top);
                byTop[tt] = byTop[tt] || [Math.round(r.left), tt, Math.round(r.right), Math.round(r.bottom)];
                byTop[tt][0] = Math.min(byTop[tt][0], Math.round(r.left)); byTop[tt][2] = Math.max(byTop[tt][2], Math.round(r.right)); } } } }
          const face = document.querySelector('.deal-beat-photo.fp-speak-face');
          return {nutshell: nuts, photos, nutshellPhotoOverlap: (nuts.length && photos.length) ? ov(nuts[0], photos[0]) : null,
            titleFont: t ? getComputedStyle(t).fontSize : null, titleLines: Object.values(byTop), faceRect: R(face)};
        }""")
        return {**r, "D-E-deck": m}
    leg("deck-1-37-D-E", leg_deck)

    def leg_deck_end():
        page.locator("#fpNextBtn").click(timeout=6000)
        page.wait_for_timeout(3000)
        return {"url": page.url, "pair": page.evaluate("() => [...document.querySelectorAll('button')].filter(x=>x.offsetParent!==null).map(x=>x.innerText.trim()).filter(t=>/Begin the visual story|Read the agreement/.test(t))")}
    leg("deck-enter-bridge", leg_deck_end)

    def leg_letter():
        page.goto(BASE + "/?stage=letter", timeout=60000); page.wait_for_timeout(2500)
        r = walk_stage(page, "letter")
        page.screenshot(path=EYE + "/eye-11-letter37.png")
        m = page.evaluate(r"""() => {
          const R = el => { if (!el) return null; const b = el.getBoundingClientRect();
            return [Math.round(b.left), Math.round(b.top), Math.round(b.right), Math.round(b.bottom)]; };
          const ov = (a,b) => { if (!a || !b) return null;
            return Math.round(Math.max(0, Math.min(a[2],b[2])-Math.max(a[0],b[0])) * Math.max(0, Math.min(a[3],b[3])-Math.max(a[1],b[1]))); };
          const titles = [...document.querySelectorAll('.frame-title, .ib-title')].filter(e => e.offsetParent !== null && /Congratulations/.test(e.textContent));
          const nuts = [...document.querySelectorAll('.ib-nutshell')].filter(e => e.offsetParent !== null).map(R);
          const photos = [...document.querySelectorAll('.deal-sign-photo')].filter(e => e.offsetParent !== null).map(R);
          const face = document.querySelector('.deal-beat-photo.fp-speak-face');
          const t = titles[0];
          const range = document.createRange(); const byTop = {};
          if (t) { const walk = document.createTreeWalker(t, NodeFilter.SHOW_TEXT); let node;
            while ((node = walk.nextNode())) { for (let i = 0; i < node.textContent.length; i++) {
              range.setStart(node, i); range.setEnd(node, i + 1); const r = range.getBoundingClientRect();
              if (r.width > 0 && r.height > 0) { const tt = Math.round(r.top);
                byTop[tt] = byTop[tt] || [Math.round(r.left), tt, Math.round(r.right), Math.round(r.bottom)];
                byTop[tt][0] = Math.min(byTop[tt][0], Math.round(r.left)); byTop[tt][2] = Math.max(byTop[tt][2], Math.round(r.right)); } } } }
          return {visibleTitles: titles.map(x => ({font: getComputedStyle(x).fontSize, rect: R(x)})),
            titleLines: Object.values(byTop), faceRect: R(face),
            nutshell: nuts, photos, nutshellPhotoOverlap: (nuts.length && photos.length) ? ov(nuts[0], photos[0]) : null};
        }""")
        return {**r, "D-E-letter": m}
    leg("letter-1-37-D-E", leg_letter)

    def leg_letter_end():
        page.locator("#fpNextBtn").click(timeout=6000)
        page.wait_for_timeout(3000)
        return {"url": page.url, "agreedMarker": page.evaluate("() => /AGREED/.test(document.body.innerText)")}
    leg("letter-agree-bridge", leg_letter_end)

    def leg_anthem_listen():
        page.goto(BASE + "/agreement", timeout=60000); page.wait_for_timeout(2000)
        page.locator("button", has_text="Watch the anthem").locator("visible=true").first.click(timeout=5000)
        page.wait_for_timeout(1500)
        anthem = page.evaluate("() => ({anthemText: document.body.innerText.includes('How much of your digital life feels scattered'), iframes: document.querySelectorAll('iframe').length, videos: document.querySelectorAll('video').length})")
        page.screenshot(path=EYE + "/eye-12-after-anthem.png")
        page.locator("button", has_text="Listen to the agreement").locator("visible=true").first.click(timeout=5000)
        page.wait_for_timeout(1500)
        listen = page.evaluate("() => ({listenText: document.body.innerText.includes(\"Naya's reading arrives\"), audios: document.querySelectorAll('audio').length})")
        page.screenshot(path=EYE + "/eye-13-after-listen.png")
        return {"anthem": anthem, "listen": listen}
    leg("anthem-listen", leg_anthem_listen)

    def leg_intro():
        page.goto(BASE + "/", timeout=60000); page.wait_for_timeout(3000)
        cold = page.evaluate("() => { const f = document.querySelector('#fpLegal'); return {fpLegalDisplay: f ? getComputedStyle(f).display : 'MISSING'}; }")
        page.goto(BASE + "/?stage=intro", timeout=60000); page.wait_for_timeout(3000)
        param = page.evaluate("() => { const f = document.querySelector('#fpLegal'); return {fpLegalDisplay: f ? getComputedStyle(f).display : 'MISSING'}; }")
        page.goto(BASE + "/", timeout=60000); page.wait_for_timeout(3000)
        act = page.evaluate("() => { if (window.__fpStage && window.__fpStage.enter) { window.__fpStage.enter(); return {entered: true}; } return {entered: false}; }")
        page.wait_for_timeout(2500)
        state = page.evaluate("() => ({bodyClass: document.body.className, fpLegalDisplay: (() => { const f = document.querySelector('#fpLegal'); return f ? getComputedStyle(f).display : 'MISSING'; })(), choicePills: [...document.querySelectorAll('button')].filter(x=>x.offsetParent!==null).map(x=>x.innerText.trim()).filter(t=>/Begin the visual story|Read the agreement/.test(t))})")
        geo = page.evaluate(GEO_SWEEP)
        page.evaluate("() => { const n = document.querySelector('#fpLegal .fp-legal-links'); if (n) n.scrollLeft = 0; }")
        page.wait_for_timeout(400)
        page.screenshot(path=EYE + "/eye-14-intro-s0.png")
        page.evaluate("() => { const n = document.querySelector('#fpLegal .fp-legal-links'); if (n) n.scrollLeft = n.scrollWidth; }")
        page.wait_for_timeout(400)
        page.screenshot(path=EYE + "/eye-15-intro-smax.png")
        return {"cold": cold, "param": param, "activation": act, "state": state, "F-intro": geo}
    leg("F-intro-strip", leg_intro)

    out["legs"].append({"leg": "390-console-errors", "errors": errs})
    b.close()

with open(LOGP, "w") as f:
    json.dump(out, f, indent=1)
print("WROTE", LOGP)
for l in out["legs"]:
    print(json.dumps(l)[:900], flush=True)
