#!/usr/bin/env python3
"""Fix-5 checker driver 2 — F9 regression + A-E re-measure at 390, my own probes.
FIX = fix-5 bytes on :18096. Writes checker-log2.json."""
import json
from playwright.sync_api import sync_playwright

CK = "/home/hatch/workspace/team-nitro/walkthrough-agreement-distill-fix5-20261119/checker"
FIX = "http://127.0.0.1:18096"
LOG = CK + "/checker-log2.json"

def counter(page):
    return page.evaluate("() => { const m = document.body.innerText.match(/(\\d+)\\s*\\/\\s*37/); return m ? m[0] : null; }")

def click_next_or_end(page):
    txt = page.evaluate("() => { const b=document.querySelector('#fpNextBtn'); return b ? b.innerText.trim() : ''; }")
    is_end = any(k in txt for k in ("Enter NayaNET", "I agree", "Read the Collective"))
    hold_cleared = None
    if is_end:
        hold_cleared = False
        for _ in range(30):
            hold = page.evaluate("() => { const h=document.querySelector('#fpNHold'); return h ? (!h.hidden && h.offsetParent!==null) : false; }")
            if not hold:
                hold_cleared = True
                break
            page.wait_for_timeout(500)
    page.locator("#fpNextBtn").click(timeout=6000)
    return {"btnText": txt, "holdCleared": hold_cleared}

def stage_walk(page, label):
    seen = []
    for i in range(42):
        c = counter(page)
        if c: seen.append(c)
        vis = page.evaluate("() => !!document.querySelector('#fpNextBtn') && document.querySelector('#fpNextBtn').offsetParent!==null")
        if not vis: break
        txt = page.evaluate("() => document.querySelector('#fpNextBtn').innerText.trim()")
        if any(k in txt for k in ("Enter NayaNET", "I agree", "Read the Collective")): break
        page.locator("#fpNextBtn").click(timeout=6000)
        page.wait_for_timeout(450)
    return {"label": label, "first": seen[:3], "last": seen[-3:], "count": len(seen),
            "sequential": seen == [f"{i} / 37" for i in range(1, len(seen)+1)],
            "nextBtnAtEnd": page.evaluate("() => { const b=document.querySelector('#fpNextBtn'); return b ? b.innerText.trim() : null; }")}

LINE_RECTS = r"""(sel) => {
  const el = document.querySelector(sel);
  if (!el) return null;
  const range = document.createRange();
  const lines = [];
  const walk = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
  let node;
  while ((node = walk.nextNode())) {
    const text = node.textContent;
    for (let i = 0; i < text.length; i++) {
      range.setStart(node, i); range.setEnd(node, i + 1);
      const r = range.getBoundingClientRect();
      if (r.width > 0 && r.height > 0) lines.push([Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]);
    }
  }
  // merge char rects into line rects by top
  const byTop = {};
  for (const [l, t, r, b] of lines) { byTop[t] = byTop[t] || [l, t, r, b]; byTop[t][0] = Math.min(byTop[t][0], l); byTop[t][2] = Math.max(byTop[t][2], r); }
  return Object.values(byTop);
}"""

RECT = r"""(sel) => { const el = document.querySelector(sel); if (!el) return null;
  const r = el.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; }"""

def ov(a, b):
    ox = max(0, min(a[2], b[2]) - max(a[0], b[0])); oy = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    return round(ox * oy)

out = {"label": "FIX5-CHECKER-DRIVE2-F9-AE", "legs": []}
def leg(name, fn):
    try:
        out["legs"].append({"leg": name, **fn()})
    except Exception as e:
        out["legs"].append({"leg": name, "ERROR": str(e)[:600]})
        print("LEG FAIL", name, str(e)[:300], flush=True)

with sync_playwright() as pw:
    b = pw.firefox.launch(headless=True)
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, ignore_https_errors=True)
    page = ctx.new_page()
    errs = []
    page.on("pageerror", lambda e: errs.append(str(e)[:200]))
    page.on("console", lambda m: errs.append(m.type + ": " + m.text[:200]) if m.type == "error" else None)

    # ---- A: identity paired / name-only / plain + overlap ----
    def leg_ident_paired():
        page.goto(FIX + "/identity.html?name=Shawn&alias=Shawn", timeout=60000); page.wait_for_timeout(2500)
        return page.evaluate(r"""() => {
          const inp = document.querySelector('input');
          const hero = document.querySelector('#displayName');
          const title = document.querySelector('.cert-title');
          const R = el => { const r = el.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; };
          return {input: inp ? inp.value : null, hero: hero ? hero.textContent.trim() : null,
            heroVisible: hero ? hero.offsetParent !== null : null,
            heroFont: hero ? getComputedStyle(hero).fontSize : null,
            heroRect: hero ? R(hero) : null, titleRect: title ? R(title) : null,
            dataText: hero ? hero.getAttribute('data-text') : null};
        }""")
    leg("A-identity-paired", leg_ident_paired)
    def leg_a_overlap():
        return page.evaluate(r"""() => {
          const R = el => { const r = el.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; };
          const ov = (a,b) => { const ox = Math.max(0, Math.min(a[2],b[2]) - Math.max(a[0],b[0])); const oy = Math.max(0, Math.min(a[3],b[3]) - Math.max(a[1],b[1])); return Math.round(ox*oy); };
          const hero = document.querySelector('#displayName'), title = document.querySelector('.cert-title');
          const cert = document.querySelector('.cert-certifies');
          return {heroTitleOverlap: ov(R(hero), R(title)),
            gap: R(hero)[1] - R(title)[3],
            certifiesDisplay: cert ? getComputedStyle(cert).display : null};
        }""")
    leg("A-overlap", leg_a_overlap)
    def leg_ident_nameonly():
        page.goto(FIX + "/identity.html?name=Shawn", timeout=60000); page.wait_for_timeout(2500)
        return page.evaluate("() => { const inp = document.querySelector('input'); const hero = document.querySelector('#displayName'); return {input: inp ? inp.value : null, hero: hero ? hero.textContent.trim() : null, heroVisible: hero ? hero.offsetParent !== null : null}; }")
    leg("identity-name-only", leg_ident_nameonly)
    def leg_ident_plain():
        page.goto(FIX + "/identity.html", timeout=60000); page.wait_for_timeout(2500)
        return page.evaluate("() => { const hero = document.querySelector('#displayName'); const cert = document.querySelector('.cert-certifies'); return {heroVisible: hero ? hero.offsetParent !== null : null, certifiesDisplay: cert ? getComputedStyle(cert).display : null, certifiesRect: cert ? (() => { const r = cert.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; })() : null}; }")
    leg("identity-plain", leg_ident_plain)
    def leg_c_banner():
        page.goto(FIX + "/identity.html?name=Shawn&alias=Shawn", timeout=60000); page.wait_for_timeout(2500)
        page.evaluate("() => { const n = document.querySelector('.hub-note.taken-note'); if (n) n.scrollIntoView({block:'center'}); }")
        page.wait_for_timeout(800)
        return page.evaluate(r"""() => {
          const R = el => { const r = el.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; };
          const ov = (a,b) => { const ox = Math.max(0, Math.min(a[2],b[2]) - Math.max(a[0],b[0])); const oy = Math.max(0, Math.min(a[3],b[3]) - Math.max(a[1],b[1])); return Math.round(ox*oy); };
          const note = document.querySelector('.hub-note.taken-note');
          const stone = document.querySelector('.cert-plaque.taken .frame-stone');
          const crests = [...document.querySelectorAll('.p3-crest-tl, .p3-crest-tr, .cert-crest, [class*=crest]')].filter(e => e.offsetParent !== null).map(R);
          // line rects of the banner text via range walk
          const range = document.createRange(); const byTop = {};
          const walk = document.createTreeWalker(note, NodeFilter.SHOW_TEXT); let node;
          while ((node = walk.nextNode())) {
            for (let i = 0; i < node.textContent.length; i++) {
              range.setStart(node, i); range.setEnd(node, i + 1);
              const r = range.getBoundingClientRect();
              if (r.width > 0 && r.height > 0) { const t = Math.round(r.top); byTop[t] = byTop[t] || [Math.round(r.left), t, Math.round(r.right), Math.round(r.bottom)]; byTop[t][0] = Math.min(byTop[t][0], Math.round(r.left)); byTop[t][2] = Math.max(byTop[t][2], Math.round(r.right)); }
            }
          }
          const lines = Object.values(byTop);
          return {noteText: note ? note.textContent.replace(/\s+/g,' ').trim().slice(0,140) : null,
            noteRect: note ? R(note) : null, lines,
            crestOverlaps: lines.map(ln => Math.max(0, ...crests.map(c => ov(ln, c)))),
            stoneDisplay: stone ? getComputedStyle(stone).display : 'absent',
            stoneOverlap: stone ? Math.max(0, ...lines.map(ln => ov(ln, R(stone)))) : null};
        }""")
    leg("C-banner", leg_c_banner)

    # ---- B + door hold + continue ----
    def leg_door():
        page.goto(FIX + "/welcome?name=Fix5%20Walk&alias=fix5walktest1", timeout=60000); page.wait_for_timeout(2000)
        steps0 = page.evaluate("() => [...document.querySelectorAll('[id^=step-]')].filter(e=>e.offsetParent!==null).map(e=>e.id)")
        page.wait_for_timeout(10000)
        steps10 = page.evaluate("() => [...document.querySelectorAll('[id^=step-]')].filter(e=>e.offsetParent!==null).map(e=>e.id)")
        bmeas = page.evaluate(r"""() => {
          const R = el => { const r = el.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; };
          const ov = (a,b) => { const ox = Math.max(0, Math.min(a[2],b[2]) - Math.max(a[0],b[0])); const oy = Math.max(0, Math.min(a[3],b[3]) - Math.max(a[1],b[1])); return Math.round(ox*oy); };
          const h = document.querySelector('#step-door .p3-question');
          const tl = document.querySelector('.p3-crest-tl'), tr = document.querySelector('.p3-crest-tr');
          const range = document.createRange(); const byTop = {};
          const walk = document.createTreeWalker(h, NodeFilter.SHOW_TEXT); let node;
          while ((node = walk.nextNode())) {
            for (let i = 0; i < node.textContent.length; i++) {
              range.setStart(node, i); range.setEnd(node, i + 1);
              const r = range.getBoundingClientRect();
              if (r.width > 0 && r.height > 0) { const t = Math.round(r.top); byTop[t] = byTop[t] || [Math.round(r.left), t, Math.round(r.right), Math.round(r.bottom)]; byTop[t][0] = Math.min(byTop[t][0], Math.round(r.left)); byTop[t][2] = Math.max(byTop[t][2], Math.round(r.right)); }
            }
          }
          const lines = Object.values(byTop);
          return {heading: h ? h.textContent.replace(/\s+/g,' ').trim() : null,
            padding: h ? [getComputedStyle(h).paddingLeft, getComputedStyle(h).paddingRight] : null,
            lines, crestOverlap: lines.map(ln => Math.max(ov(ln, R(tl)), ov(ln, R(tr))))};
        }""")
        page.screenshot(path=CK + "/ck5-fix-B-door.png")
        return {"at0": steps0, "at10s": steps10, "held": steps0 == steps10, "B": bmeas}
    leg("B-door-10s-hold", leg_door)
    def leg_continue():
        page.locator("#doorContinue").click(timeout=6000)
        page.wait_for_timeout(1500)
        return {"visibleSteps": page.evaluate("() => [...document.querySelectorAll('[id^=step-]')].filter(e=>e.offsetParent!==null).map(e=>e.id)")}
    leg("door-continue-step1", leg_continue)

    # ---- unfold 1->37 + D unfold ----
    def leg_unfold():
        page.goto(FIX + "/agreement", timeout=60000); page.wait_for_timeout(2000)
        seen = []
        for i in range(40):
            c = counter(page)
            if c: seen.append(c)
            if page.evaluate("() => [...document.querySelectorAll('button')].some(x=>x.offsetParent!==null && /I agree/i.test(x.innerText))"): break
            page.locator("button", has_text="Next").locator("visible=true").first.click(timeout=5000)
            page.wait_for_timeout(350)
        return {"first": seen[:3], "last": seen[-3:], "count": len(seen),
                "sequential": seen == [f"{i} / 37" for i in range(1, len(seen)+1)]}
    leg("unfold-1-37", leg_unfold)
    def leg_d_unfold():
        d = page.evaluate(r"""() => {
          const R = el => { const r = el.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; };
          const titles = [...document.querySelectorAll('.frame-title, .ib-title')].filter(e => e.offsetParent !== null && /Congratulations/.test(e.textContent));
          const orb = document.querySelector('.frame-icon');
          const out = titles.map(t => {
            const range = document.createRange(); const byTop = {};
            const walk = document.createTreeWalker(t, NodeFilter.SHOW_TEXT); let node;
            while ((node = walk.nextNode())) {
              for (let i = 0; i < node.textContent.length; i++) {
                range.setStart(node, i); range.setEnd(node, i + 1);
                const r = range.getBoundingClientRect();
                if (r.width > 0 && r.height > 0) { const tt = Math.round(r.top); byTop[tt] = byTop[tt] || [Math.round(r.left), tt, Math.round(r.right), Math.round(r.bottom)]; byTop[tt][0] = Math.min(byTop[tt][0], Math.round(r.left)); byTop[tt][2] = Math.max(byTop[tt][2], Math.round(r.right)); }
              }
            }
            return {cls: t.className, font: getComputedStyle(t).fontSize, rect: R(t), lines: Object.values(byTop)};
          });
          return {titles: out, orbRect: orb ? R(orb) : null};
        }""")
        page.screenshot(path=CK + "/ck5-fix-D-unfold37.png")
        return d
    leg("D-unfold37", leg_d_unfold)
    def leg_agree_bridge():
        page.locator("button", has_text="I agree").locator("visible=true").first.click(timeout=5000)
        page.wait_for_timeout(2500)
        return {"pair": page.evaluate("() => [...document.querySelectorAll('button')].filter(x=>x.offsetParent!==null).map(x=>x.innerText.trim()).filter(t=>/Begin the visual story|Read the agreement/.test(t))"),
                "url": page.url}
    leg("agree-to-bridge-pair", leg_agree_bridge)
    def leg_begin_deck():
        page.locator("button", has_text="Begin the visual story").locator("visible=true").first.click(timeout=5000)
        page.wait_for_timeout(2500)
        return {"counter": counter(page), "url": page.url}
    leg("pair-begin-deck", leg_begin_deck)
    def leg_deck():
        r = stage_walk(page, "deck")
        page.screenshot(path=CK + "/ck5-fix-E-deck37.png")
        return r
    leg("deck-1-37", leg_deck)
    def leg_deck_meas():
        return page.evaluate(r"""() => {
          const R = el => { const r = el.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; };
          const ov = (a,b) => { const ox = Math.max(0, Math.min(a[2],b[2]) - Math.max(a[0],b[0])); const oy = Math.max(0, Math.min(a[3],b[3]) - Math.max(a[1],b[1])); return Math.round(ox*oy); };
          const nuts = [...document.querySelectorAll('.ib-nutshell')].filter(e => e.offsetParent !== null).map(R);
          const photos = [...document.querySelectorAll('.deal-sign-photo')].filter(e => e.offsetParent !== null).map(R);
          const titles = [...document.querySelectorAll('.frame-title, .ib-title')].filter(e => e.offsetParent !== null && /Congratulations/.test(e.textContent));
          const t = titles[0];
          const range = document.createRange(); const byTop = {};
          if (t) { const walk = document.createTreeWalker(t, NodeFilter.SHOW_TEXT); let node;
            while ((node = walk.nextNode())) { for (let i = 0; i < node.textContent.length; i++) {
              range.setStart(node, i); range.setEnd(node, i + 1); const r = range.getBoundingClientRect();
              if (r.width > 0 && r.height > 0) { const tt = Math.round(r.top); byTop[tt] = byTop[tt] || [Math.round(r.left), tt, Math.round(r.right), Math.round(r.bottom)]; byTop[tt][0] = Math.min(byTop[tt][0], Math.round(r.left)); byTop[tt][2] = Math.max(byTop[tt][2], Math.round(r.right)); } } } }
          const face = document.querySelector('.deal-beat-photo.fp-speak-face');
          return {nutshell: nuts, photos, nutshellPhotoOverlap: (nuts.length && photos.length) ? ov(nuts[0], photos[0]) : null,
            titleFont: t ? getComputedStyle(t).fontSize : null, titleLines: Object.values(byTop),
            faceRect: face ? R(face) : null};
        }""")
    leg("D-E-deck37", leg_deck_meas)
    def leg_deck_end():
        r = click_next_or_end(page)
        page.wait_for_timeout(3000)
        return {"endClick": r, "url": page.url,
                "pair": page.evaluate("() => [...document.querySelectorAll('button')].filter(x=>x.offsetParent!==null).map(x=>x.innerText.trim()).filter(t=>/Begin the visual story|Read the agreement/.test(t))")}
    leg("deck-enter-bridge", leg_deck_end)
    def leg_read_agree():
        page.locator("button", has_text="Read the agreement").locator("visible=true").first.click(timeout=5000)
        page.wait_for_timeout(2500)
        return {"counter": counter(page), "url": page.url}
    leg("pair-read-agreement", leg_read_agree)
    def leg_letter():
        page.goto(FIX + "/?stage=letter", timeout=60000); page.wait_for_timeout(2500)
        r = stage_walk(page, "letter")
        page.screenshot(path=CK + "/ck5-fix-letter37.png")
        return r
    leg("letter-1-37", leg_letter)
    def leg_letter_meas():
        return page.evaluate(r"""() => {
          const R = el => { const r = el.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; };
          const ov = (a,b) => { const ox = Math.max(0, Math.min(a[2],b[2]) - Math.max(a[0],b[0])); const oy = Math.max(0, Math.min(a[3],b[3]) - Math.max(a[1],b[1])); return Math.round(ox*oy); };
          const titles = [...document.querySelectorAll('.frame-title, .ib-title')].filter(e => e.offsetParent !== null && /Congratulations/.test(e.textContent));
          const nuts = [...document.querySelectorAll('.ib-nutshell')].filter(e => e.offsetParent !== null).map(R);
          const photos = [...document.querySelectorAll('.deal-sign-photo')].filter(e => e.offsetParent !== null).map(R);
          const face = document.querySelector('.deal-beat-photo.fp-speak-face');
          const t = titles[0];
          const range = document.createRange(); const byTop = {};
          if (t) { const walk = document.createTreeWalker(t, NodeFilter.SHOW_TEXT); let node;
            while ((node = walk.nextNode())) { for (let i = 0; i < node.textContent.length; i++) {
              range.setStart(node, i); range.setEnd(node, i + 1); const r = range.getBoundingClientRect();
              if (r.width > 0 && r.height > 0) { const tt = Math.round(r.top); byTop[tt] = byTop[tt] || [Math.round(r.left), tt, Math.round(r.right), Math.round(r.bottom)]; byTop[tt][0] = Math.min(byTop[tt][0], Math.round(r.left)); byTop[tt][2] = Math.max(byTop[tt][2], Math.round(r.right)); } } } }
          return {visibleTitles: titles.map(x => ({cls: x.className, font: getComputedStyle(x).fontSize, rect: R(x)})),
            titleLines: Object.values(byTop), faceRect: face ? R(face) : null,
            nutshell: nuts, photos, nutshellPhotoOverlap: (nuts.length && photos.length) ? ov(nuts[0], photos[0]) : null};
        }""")
    leg("D-E-letter37", leg_letter_meas)
    def leg_letter_end():
        r = click_next_or_end(page)
        page.wait_for_timeout(3000)
        return {"endClick": r, "url": page.url,
                "agreedMarker": page.evaluate("() => /AGREED/.test(document.body.innerText)")}
    leg("letter-agree-bridge", leg_letter_end)
    out["legs"].append({"leg": "390-console-errors", "errors": errs})
    b.close()

with open(LOG, "w") as f:
    json.dump(out, f, indent=1)
for l in out["legs"]:
    print(json.dumps(l)[:1200], flush=True)
print("WROTE", LOG)
