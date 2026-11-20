#!/usr/bin/env python3
"""Fix-4 maker — VERIFICATION on staged fix-4 bytes.
Proves each fix at 390x844 (rects + screenshots) + F9 regression at 390 and 1920.
Writes proof-fix4/fix4-verify.json + fix4-verify-*.png under maker/work/.
"""
import json, os
from playwright.sync_api import sync_playwright

BASE = "https://naya-walk-beginning-staging.nayapower.workers.dev"
OUT = os.path.expanduser("~/workspace/team-nitro/walkthrough-agreement-distill-fix4-20261119/maker/work/proof-fix4")
os.makedirs(OUT, exist_ok=True)
LOG = {"steps": [], "errors": []}
ERRORS = []

def note(step, **kw):
    rec = {"step": step, **kw}
    LOG["steps"].append(rec)
    print(json.dumps(rec)[:1100], flush=True)
    return rec

def shot(page, name):
    page.screenshot(path=os.path.join(OUT, name))
    return name

def page_errors(page):
    page.on("pageerror", lambda e: ERRORS.append("pageerror: " + str(e)))
    page.on("console", lambda m: ERRORS.append("console." + m.type + ": " + m.text) if m.type == "error" else None)

RJS = """() => {
  const R = el => { if (!el) return null; const r = el.getBoundingClientRect();
    return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; };
  const ov = (a,b) => { if (!a||!b) return 0; const x=Math.max(0,Math.min(a[2],b[2])-Math.max(a[0],b[0])); const y=Math.max(0,Math.min(a[3],b[3])-Math.max(a[1],b[1])); return Math.round(x*y); };
  window.__R = R; window.__ov = ov; return true; }"""

def walk_to_37(page, next_selector="#fpNextBtn", max_steps=45):
    counters = []
    for i in range(max_steps):
        c = page.evaluate("() => { const m = document.body.innerText.match(/(\\d+)\\s*\\/\\s*37/); return m ? m[0] : null; }")
        counters.append(c)
        if c and c.startswith("37"):
            break
        try:
            page.locator(next_selector).click(timeout=6000)
        except Exception as e:
            note("walk-next-fail", counter=c, error=str(e)[:200]); break
        page.wait_for_timeout(500)
    return [c for c in counters if c]

with sync_playwright() as pw:
    browser = pw.firefox.launch(headless=True)

    # ---------- A + C: identity paired, 390 ----------
    ctx = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    page = ctx.new_page(); page_errors(page)
    page.goto(BASE + "/identity.html?name=Shawn&alias=Shawn", timeout=60000)
    page.wait_for_timeout(4000)
    m = page.evaluate("""() => {
      const R = el => { if (!el) return null; const r = el.getBoundingClientRect();
        return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; };
      const ov = (a,b) => { if (!a||!b) return 0; const x=Math.max(0,Math.min(a[2],b[2])-Math.max(a[0],b[0])); const y=Math.max(0,Math.min(a[3],b[3])-Math.max(a[1],b[1])); return Math.round(x*y); };
      const name = document.getElementById('displayName');
      const title = document.querySelector('.cert-title');
      const wrap = document.querySelector('.face-center');
      const status = document.querySelector('.alias-status');
      const input = document.getElementById('aliasInput');
      const plaque = document.querySelector('.cert-plaque');
      const nr = R(name), tr = R(title), wr = R(wrap), sr = R(status);
      const cs = name ? getComputedStyle(name) : null;
      return {input: input ? input.value : null, hero: name ? name.textContent : null,
        heroHidden: name ? name.hidden : null, dataText: name ? name.getAttribute('data-text') : null,
        nameFontPx: cs ? parseFloat(cs.fontSize) : null,
        nameRect: nr, titleRect: tr, wrapRect: wr, statusRect: sr,
        titleText: title ? title.textContent.trim() : null,
        nameTitleOverlap: ov(nr, tr), nameWrapOverlap: ov(nr, wr),
        plaqueClass: plaque ? plaque.className : null,
        innerWidth: window.innerWidth, scrollW: document.documentElement.scrollWidth};
    }""")
    note("A-identity-paired", **m)
    shot(page, "fix4-verify-A-identity.png")
    # C: note line rects vs every visible element (no offsetParent filter)
    page.evaluate("() => { const n = document.getElementById('hubNote'); if (n) n.scrollIntoView({block:'center'}); }")
    page.wait_for_timeout(600)
    cm = page.evaluate("""() => {
      const R = el => { if (!el) return null; const r = el.getBoundingClientRect();
        return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; };
      const ov = (a,b) => { if (!a||!b) return 0; const x=Math.max(0,Math.min(a[2],b[2])-Math.max(a[0],b[0])); const y=Math.max(0,Math.min(a[3],b[3])-Math.max(a[1],b[1])); return Math.round(x*y); };
      const note = document.getElementById('hubNote');
      const stone = document.querySelector('.cert-plaque .frame-stone');
      const nr = R(note);
      // first-line text rects via Range over the note's text
      const rng = document.createRange(); rng.selectNodeContents(note);
      const lineRects = [...rng.getClientRects()].map(r => [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]);
      const crests = [...document.querySelectorAll('.corner-crest')].map(R);
      const lineCrestOverlap = lineRects.reduce((t, lr) => t + crests.reduce((s, c) => s + ov(lr, c), 0), 0);
      // every element overlapping the note box (excluding ancestors of the note)
      const over = [...document.querySelectorAll('body *')].filter(e => e !== note && !note.contains(e) && !e.contains(note)).map(e => {
        const r = R(e); const a = ov(r, nr);
        return {tag: e.tagName, cls: (typeof e.className === 'string' ? e.className : '').slice(0,70), rect: r, overlap: a};
      }).filter(x => x.overlap > 0).sort((a,b) => b.overlap - a.overlap).slice(0,10);
      return {noteRect: nr, noteScrollW: note.scrollWidth, noteClientW: note.clientWidth,
        noteTextClipped: note.scrollWidth > note.clientWidth + 1,
        lineRects, lineCrestOverlap, stoneDisplay: stone ? getComputedStyle(stone).display : 'absent',
        stoneRect: R(stone), noteOverlaps: over,
        noteClass: note.className};
    }""")
    note("C-banner", **cm)
    shot(page, "fix4-verify-C-banner.png")
    ctx.close()

    # ---------- F9: name-only + plain identity, 390 ----------
    for label, q in [("name-only", "?name=Shawn"), ("plain", "")]:
        ctx = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        page = ctx.new_page(); page_errors(page)
        page.goto(BASE + "/identity.html" + q, timeout=60000)
        page.wait_for_timeout(3500)
        m = page.evaluate("""() => {
          const name = document.getElementById('displayName');
          const input = document.getElementById('aliasInput');
          return {input: input ? input.value : null, hero: name ? name.textContent : null,
            heroHidden: name ? name.hidden : null, dataText: name ? name.getAttribute('data-text') : null}; }""")
        note("F9-identity-" + label, **m)
        ctx.close()

    # ---------- B: door, 390 (hold + continue) ----------
    ctx = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    page = ctx.new_page(); page_errors(page)
    page.goto(BASE + "/welcome?name=FixFour&alias=fix4door7x", timeout=60000)
    page.wait_for_timeout(4000)
    m = page.evaluate("""() => {
      const R = el => { if (!el) return null; const r = el.getBoundingClientRect();
        return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; };
      const ov = (a,b) => { if (!a||!b) return 0; const x=Math.max(0,Math.min(a[2],b[2])-Math.max(a[0],b[0])); const y=Math.max(0,Math.min(a[3],b[3])-Math.max(a[1],b[1])); return Math.round(x*y); };
      const door = document.getElementById('step-door');
      const h1 = door ? door.querySelector('.p3-question') : null;
      const crests = [...document.querySelectorAll('.p3-crest')].map(R);
      const hr = R(h1);
      return {doorVisible: door ? !door.hidden : null, h1Rect: hr,
        h1Text: h1 ? h1.textContent : null, crestRects: crests,
        crestOverlaps: crests.map(c => ov(hr, c)),
        continueVisible: !!document.getElementById('doorContinue') && !document.getElementById('doorContinue').hidden};
    }""")
    note("B-door-h1", **m)
    shot(page, "fix4-verify-B-door.png")
    page.wait_for_timeout(10000)
    note("B-door-10s-hold", visibleSteps=page.evaluate("() => [...document.querySelectorAll('.p3-step')].filter(s => !s.hidden).map(s => s.id)"))
    page.locator("#doorContinue").click(timeout=6000)
    page.wait_for_timeout(1200)
    note("B-door-continue", visibleSteps=page.evaluate("() => [...document.querySelectorAll('.p3-step')].filter(s => !s.hidden).map(s => s.id)"))
    shot(page, "fix4-verify-B-after-continue.png")
    ctx.close()

    # ---------- B: door hold at 1920 ----------
    ctx = browser.new_context(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
    page = ctx.new_page(); page_errors(page)
    page.goto(BASE + "/welcome?name=FixFour&alias=fix4door7x", timeout=60000)
    page.wait_for_timeout(4000)
    page.wait_for_timeout(10000)
    note("F9-door-10s-hold-1920", visibleSteps=page.evaluate("() => [...document.querySelectorAll('.p3-step')].filter(s => !s.hidden).map(s => s.id)"))
    page.locator("#doorContinue").click(timeout=6000)
    page.wait_for_timeout(1200)
    note("F9-door-continue-1920", visibleSteps=page.evaluate("() => [...document.querySelectorAll('.p3-step')].filter(s => !s.hidden).map(s => s.id)"))
    ctx.close()

    # ---------- D unfold: /agreement 1->37, 390 ----------
    ctx = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    page = ctx.new_page(); page_errors(page)
    page.goto(BASE + "/agreement", timeout=60000)
    page.wait_for_timeout(2500)
    counters = []
    for i in range(45):
        c = page.evaluate("() => { const m = document.body.innerText.match(/(\\d+)\\s*\\/\\s*37/); return m ? m[0] : null; }")
        counters.append(c)
        if c and c.startswith("37"):
            break
        try:
            loc = page.locator("button", has_text="Keep reading").locator("visible=true").first
            if loc.count() == 0:
                loc = page.locator("button", has_text="Next").locator("visible=true").first
            loc.click(timeout=5000)
        except Exception as e:
            note("D-unfold-next-fail", counter=c, error=str(e)[:200]); break
        page.wait_for_timeout(500)
    note("D-unfold-walk", counters=[c for c in counters if c])
    m = page.evaluate("""() => {
      const R = el => { if (!el) return null; const r = el.getBoundingClientRect();
        return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; };
      const ov = (a,b) => { if (!a||!b) return 0; const x=Math.max(0,Math.min(a[2],b[2])-Math.max(a[0],b[0])); const y=Math.max(0,Math.min(a[3],b[3])-Math.max(a[1],b[1])); return Math.round(x*y); };
      const arts = [...document.querySelectorAll('article')].filter(a => !a.hidden && a.offsetParent !== null);
      const vis = arts.filter(a => { const r = a.getBoundingClientRect(); return r.width > 0 && r.height > 0 && r.top >= -20 && r.top < 700; });
      const b37 = vis[vis.length - 1] || arts[arts.length - 1];
      const title = b37 ? b37.querySelector('h2') : null;
      const tr = R(title);
      const face = document.querySelector('.deal-beat-photo.fp-speak-face');
      const orb = document.querySelector('.ib-orb');
      const cs = title ? getComputedStyle(title) : null;
      return {titleRect: tr, titleText: title ? title.textContent.trim().slice(0,60) : null,
        titleFontPx: cs ? parseFloat(cs.fontSize) : null,
        faceRect: R(face), orbRect: R(orb),
        titleFaceOverlap: ov(tr, R(face)), titleOrbOverlap: ov(tr, R(orb)),
        boardClass: b37 ? b37.className.slice(0,80) : null};
    }""")
    note("D-unfold-board37", **m)
    shot(page, "fix4-verify-D-unfold37.png")
    ctx.close()

    # ---------- D+E deck: /?stage=deck 1->37 -> bridge, 390 ----------
    ctx = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    page = ctx.new_page(); page_errors(page)
    page.goto(BASE + "/?stage=deck", timeout=60000)
    page.wait_for_timeout(2500)
    counters = walk_to_37(page)
    note("DE-deck-walk", counters=counters)
    m = page.evaluate("""() => {
      const R = el => { if (!el) return null; const r = el.getBoundingClientRect();
        return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; };
      const ov = (a,b) => { if (!a||!b) return 0; const x=Math.max(0,Math.min(a[2],b[2])-Math.max(a[0],b[0])); const y=Math.max(0,Math.min(a[3],b[3])-Math.max(a[1],b[1])); return Math.round(x*y); };
      const board = document.querySelector('#fpAgreement.fp-now') || document.querySelector('.fp-now');
      const title = board ? board.querySelector('.ib-title') : null;
      const nutshell = board ? board.querySelector('.ib-nutshell') : null;
      const signFrame = board ? board.querySelector('.deal-sign-frame') : null;
      const signPhoto = board ? board.querySelector('.deal-sign-photo') : null;
      const face = board ? board.querySelector('.deal-beat-photo.fp-speak-face') : null;
      const tr = R(title), nr = R(nutshell), sfr = R(signFrame), spr = R(signPhoto), fr = R(face);
      const cs = title ? getComputedStyle(title) : null;
      // what sits at the sign photo's centre? (identifies the photo element)
      let atCenter = null;
      if (spr) { const el = document.elementFromPoint(Math.round((spr[0]+spr[2])/2), Math.round((spr[1]+spr[3])/2));
        atCenter = el ? (el.tagName + '.' + (typeof el.className === 'string' ? el.className : '').slice(0,60)) : null; }
      return {titleRect: tr, titleText: title ? title.textContent.trim().slice(0,60) : null,
        titleFontPx: cs ? parseFloat(cs.fontSize) : null,
        nutshellRect: nr, signFrameRect: sfr, signPhotoRect: spr, speakFaceRect: fr,
        titleFaceOverlap: ov(tr, fr), nutshellSignOverlap: ov(nr, spr), nutshellFrameOverlap: ov(nr, sfr),
        atSignPhotoCenter: atCenter,
        boardClass: board ? board.className.slice(0,100) : null};
    }""")
    note("DE-deck-board37", **m)
    shot(page, "fix4-verify-E-deck37.png")
    # deck end -> bridge
    btns = page.evaluate("() => [...document.querySelectorAll('#fpStageBarB button, #fpStageBarT button')].filter(b=>b.offsetParent!==null).map(b=>({id:b.id, t:(b.innerText||'').trim().slice(0,40)}))")
    note("DE-deck-end-buttons", buttons=btns)
    for b in btns:
        if b["id"] not in ("fpDeckBack", "fpStageExit"):
            try:
                page.locator("#" + b["id"]).click(timeout=6000)
                page.wait_for_timeout(3000)
                break
            except Exception as e:
                note("DE-deck-end-error", button=b, error=str(e)[:150])
    note("DE-after-deck-enter", url=page.url,
         bodyStart=page.evaluate("() => document.body.innerText.replace(/\\s+/g,' ').trim().slice(0,200)"))
    shot(page, "fix4-verify-F-bridge.png")
    # F: footer links scroll + drag
    fm = page.evaluate("""() => {
      const R = el => { if (!el) return null; const r = el.getBoundingClientRect();
        return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; };
      const nav = document.querySelector('#fpLegal .fp-legal-links');
      if (!nav) return {found: false};
      const links = [...nav.querySelectorAll('.fp-legal-link')].map(e => ({t: e.textContent.trim(), rect: R(e)}));
      const cs = getComputedStyle(nav);
      const before = nav.scrollLeft;
      nav.scrollLeft = 60;
      const after = nav.scrollLeft;
      nav.scrollLeft = 0;
      return {found: true, navRect: R(nav), scrollWidth: nav.scrollWidth, clientWidth: nav.clientWidth,
        scrollable: nav.scrollWidth > nav.clientWidth + 1, flexWrap: cs.flexWrap, overflowX: cs.overflowX,
        scrollTest: {before, setTo: 60, after}, links, innerWidth: window.innerWidth};
    }""")
    note("F-footer-links", **fm)
    # drag/swipe test on the strip
    dm = page.evaluate("""() => {
      const nav = document.querySelector('#fpLegal .fp-legal-links');
      if (!nav) return {found: false};
      nav.scrollLeft = 0; return {start: nav.scrollLeft}; }""")
    try:
        nav = page.locator("#fpLegal .fp-legal-links")
        box = nav.bounding_box()
        if box:
            page.mouse.move(box["x"] + box["width"] - 40, box["y"] + box["height"] / 2)
            page.mouse.down()
            page.mouse.move(box["x"] + 60, box["y"] + box["height"] / 2, steps=12)
            page.mouse.up()
            page.wait_for_timeout(400)
            dm["afterDrag"] = page.evaluate("() => document.querySelector('#fpLegal .fp-legal-links').scrollLeft")
            dm["dragged"] = dm["afterDrag"] != dm["start"]
    except Exception as e:
        dm["dragError"] = str(e)[:200]
    note("F-footer-drag", **dm)
    # bridge pair
    pair = page.evaluate("""() => [...document.querySelectorAll('button')].filter(b=>b.offsetParent!==null).map(b=>({id:b.id, t:(b.innerText||'').trim().slice(0,50)}))""")
    note("F9-bridge-buttons", buttons=[b for b in pair if 'visual story' in b['t'] or 'agreement' in b['t'] or 'Continue' in b['t']])
    for target in ["Begin the visual story", "Read the agreement"]:
        try:
            loc = page.locator("button", has_text=target).locator("visible=true").first
            if loc.count() == 0:
                note("F9-bridge-pair-missing", target=target); continue
            loc.click(timeout=6000)
            page.wait_for_timeout(2500)
            note("F9-bridge-pair-click", target=target, url=page.url,
                 bodyStart=page.evaluate("() => document.body.innerText.replace(/\\s+/g,' ').trim().slice(0,150)"))
            page.go_back()
            page.wait_for_timeout(2000)
        except Exception as e:
            note("F9-bridge-pair-error", target=target, error=str(e)[:200])
    ctx.close()

    # ---------- letter: /?stage=letter 1->37 -> bridge, 390 ----------
    ctx = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    page = ctx.new_page(); page_errors(page)
    page.goto(BASE + "/?stage=letter", timeout=60000)
    page.wait_for_timeout(2500)
    counters = walk_to_37(page)
    note("F9-letter-walk", counters=counters)
    m = page.evaluate("""() => {
      const R = el => { if (!el) return null; const r = el.getBoundingClientRect();
        return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; };
      const ov = (a,b) => { if (!a||!b) return 0; const x=Math.max(0,Math.min(a[2],b[2])-Math.max(a[0],b[0])); const y=Math.max(0,Math.min(a[3],b[3])-Math.max(a[1],b[1])); return Math.round(x*y); };
      const board = document.querySelector('#fpAgreement.fp-now') || document.querySelector('.fp-now');
      const title = board ? board.querySelector('.ib-title') : null;
      const nutshell = board ? board.querySelector('.ib-nutshell') : null;
      const signPhoto = board ? board.querySelector('.deal-sign-photo') : null;
      const face = board ? board.querySelector('.deal-beat-photo.fp-speak-face') : null;
      const tr = R(title), nr = R(nutshell), spr = R(signPhoto), fr = R(face);
      return {titleRect: tr, titleText: title ? title.textContent.trim().slice(0,60) : null,
        nutshellRect: nr, signPhotoRect: spr, speakFaceRect: fr,
        titleFaceOverlap: ov(tr, fr), nutshellSignOverlap: ov(nr, spr)};
    }""")
    note("F9-letter-board37", **m)
    shot(page, "fix4-verify-letter37.png")
    ctx.close()
    browser.close()

LOG["errors"] = ERRORS
with open(os.path.join(OUT, "fix4-verify.json"), "w") as f:
    json.dump(LOG, f, indent=2)
print("VERIFY PROBE DONE, console errors:", len(ERRORS))
for e in ERRORS[:10]:
    print("ERR:", e[:200])
