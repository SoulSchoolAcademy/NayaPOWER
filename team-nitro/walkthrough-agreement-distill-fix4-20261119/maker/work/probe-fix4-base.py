#!/usr/bin/env python3
"""Fix-4 maker — BASE reproduction (staging serves fix-3 bytes).
Measures defects A-F at 390x844 with rects + screenshots.
Writes proof-base/fix4-base.json + fix4-base-*.png under maker/work/.
"""
import json, os
from playwright.sync_api import sync_playwright

BASE = "https://naya-walk-beginning-staging.nayapower.workers.dev"
OUT = os.path.expanduser("~/workspace/team-nitro/walkthrough-agreement-distill-fix4-20261119/maker/work/proof-base")
os.makedirs(OUT, exist_ok=True)
LOG = {"steps": [], "errors": []}
ERRORS = []

def note(step, **kw):
    rec = {"step": step, **kw}
    LOG["steps"].append(rec)
    print(json.dumps(rec)[:900], flush=True)
    return rec

def shot(page, name):
    page.screenshot(path=os.path.join(OUT, name))
    return name

def rects(page, js):
    return page.evaluate(js)

GEOM = """() => {
  const R = el => { if (!el) return null; const r = el.getBoundingClientRect();
    return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; };
  const vis = el => el && el.offsetParent !== null;
  const ov = (a, b) => { if (!a || !b) return 0;
    const x = Math.max(0, Math.min(a[2], b[2]) - Math.max(a[0], b[0]));
    const y = Math.max(0, Math.min(a[3], b[3]) - Math.max(a[1], b[1]));
    return Math.round(x * y); };
  return { R, vis, ov };
}"""

def page_errors(page):
    page.on("pageerror", lambda e: ERRORS.append("pageerror: " + str(e)))
    page.on("console", lambda m: ERRORS.append("console." + m.type + ": " + m.text) if m.type == "error" else None)

with sync_playwright() as pw:
    browser = pw.firefox.launch(headless=True)
    # ---------- A + C: identity paired ----------
    ctx = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    page = ctx.new_page(); page_errors(page)
    page.goto(BASE + "/identity.html?name=Shawn&alias=Shawn", timeout=60000)
    page.wait_for_timeout(4000)
    m = page.evaluate("""() => {
      const R = el => { if (!el) return null; const r = el.getBoundingClientRect();
        return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; };
      const name = document.getElementById('displayName');
      const title = document.querySelector('.cert-title');
      const note = document.getElementById('hubNote');
      const crests = [...document.querySelectorAll('.corner-crest')].map(R);
      const input = document.getElementById('aliasInput');
      const nr = R(name), tr = R(title), nn = R(note);
      const ovY = (nr && tr) ? Math.max(0, Math.min(nr[3], tr[3]) - Math.max(nr[1], tr[1])) : 0;
      const ovX = (nr && tr) ? Math.max(0, Math.min(nr[2], tr[2]) - Math.max(nr[0], tr[0])) : 0;
      return {input: input ? input.value : null,
        hero: name ? name.textContent : null, heroHidden: name ? name.hidden : null,
        dataText: name ? name.getAttribute('data-text') : null,
        nameRect: nr, titleRect: tr, titleText: title ? title.textContent.trim() : null,
        overlapYpx: ovY, overlapXpx: ovX,
        noteRect: nn, noteHidden: note ? note.hidden : null,
        noteText: note ? (note.textContent||'').slice(0,80) : null,
        noteClass: note ? note.className : null,
        crestRects: crests,
        innerWidth: window.innerWidth, scrollW: document.documentElement.scrollWidth};
    }""")
    note("A-C-identity-paired", **m)
    shot(page, "fix4-base-A-identity.png")
    page.evaluate("() => { const n = document.getElementById('hubNote'); if (n) n.scrollIntoView({block:'center'}); }")
    page.wait_for_timeout(600)
    shot(page, "fix4-base-C-banner.png")
    ctx.close()

    # ---------- B: door ----------
    ctx = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    page = ctx.new_page(); page_errors(page)
    page.goto(BASE + "/welcome?name=FixFour&alias=fix4door7x", timeout=60000)
    page.wait_for_timeout(4000)
    m = page.evaluate("""() => {
      const R = el => { if (!el) return null; const r = el.getBoundingClientRect();
        return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; };
      const door = document.getElementById('step-door');
      const h1 = door ? door.querySelector('.p3-question') : null;
      const crests = [...document.querySelectorAll('.p3-crest')].map(R);
      const hr = R(h1);
      const ov = crests.map(c => { if (!c || !hr) return 0;
        const x = Math.max(0, Math.min(hr[2], c[2]) - Math.max(hr[0], c[0]));
        const y = Math.max(0, Math.min(hr[3], c[3]) - Math.max(hr[1], c[1]));
        return Math.round(x*y); });
      return {doorHidden: door ? door.hidden : null, doorVisible: door ? !door.hidden : null,
        h1Rect: hr, h1Text: h1 ? h1.textContent : null, crestRects: crests, crestOverlaps: ov,
        continueVisible: !!document.getElementById('doorContinue') && !document.getElementById('doorContinue').hidden};
    }""")
    note("B-door-h1", **m)
    shot(page, "fix4-base-B-door.png")
    # F9 door hold: still door after 10 s untouched, then Continue -> step-1
    page.wait_for_timeout(10000)
    m2 = page.evaluate("""() => {
      const vis = [...document.querySelectorAll('.p3-step')].filter(s => !s.hidden).map(s => s.id);
      return {visibleSteps: vis}; }""")
    note("B-door-10s-hold", **m2)
    page.locator("#doorContinue").click(timeout=6000)
    page.wait_for_timeout(1200)
    m3 = page.evaluate("""() => ({visibleSteps: [...document.querySelectorAll('.p3-step')].filter(s => !s.hidden).map(s => s.id)})""")
    note("B-door-continue", **m3)
    shot(page, "fix4-base-B-after-continue.png")
    ctx.close()

    # ---------- D unfold: /agreement 1->37 ----------
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
      const boards = [...document.querySelectorAll('.intel-board, .letter-beat, article')].filter(b => !b.hidden && b.offsetParent !== null);
      const b37 = boards[boards.length - 1];
      const title = b37 ? b37.querySelector('h2') : null;
      const orb = b37 ? b37.querySelector('.ib-orb') : null;
      const face = b37 ? (b37.querySelector('.deal-beat-photo') || document.querySelector('.fp-speak-face')) : null;
      const tr = R(title), or_ = R(orb), fr = R(face);
      const ov = (a,b) => { if (!a||!b) return 0; const x=Math.max(0,Math.min(a[2],b[2])-Math.max(a[0],b[0])); const y=Math.max(0,Math.min(a[3],b[3])-Math.max(a[1],b[1])); return Math.round(x*y); };
      return {titleRect: tr, titleText: title ? title.textContent.trim().slice(0,60) : null,
        orbRect: or_, faceRect: fr, titleOrbOverlap: ov(tr, or_), titleFaceOverlap: ov(tr, fr),
        boardClass: b37 ? b37.className.slice(0,80) : null};
    }""")
    note("D-unfold-board37", **m)
    shot(page, "fix4-base-D-unfold37.png")
    ctx.close()

    # ---------- D+E deck: /?stage=deck ----------
    ctx = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    page = ctx.new_page(); page_errors(page)
    page.goto(BASE + "/?stage=deck", timeout=60000)
    page.wait_for_timeout(2500)
    counters = []
    for i in range(42):
        c = page.evaluate("() => { const m = document.body.innerText.match(/(\\d+)\\s*\\/\\s*37/); return m ? m[0] : null; }")
        counters.append(c)
        btns = page.evaluate("() => [...document.querySelectorAll('#fpNextBtn')].filter(b=>b.offsetParent!==null).map(b=>b.innerText.trim().slice(0,30))")
        if not btns:
            break
        try:
            page.locator("#fpNextBtn").click(timeout=6000)
        except Exception as e:
            note("DE-deck-next-fail", counter=c, error=str(e)[:200]); break
        page.wait_for_timeout(550)
    note("DE-deck-walk", counters=[c for c in counters if c])
    m = page.evaluate("""() => {
      const R = el => { if (!el) return null; const r = el.getBoundingClientRect();
        return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; };
      const boards = [...document.querySelectorAll('.intel-board, .letter-beat, article')].filter(b => !b.hidden && b.offsetParent !== null);
      const b37 = boards[boards.length - 1];
      const title = b37 ? b37.querySelector('h2') : null;
      const orb = b37 ? b37.querySelector('.ib-orb') : null;
      const nutshell = b37 ? b37.querySelector('.ib-nutshell') : null;
      const tr = R(title), or_ = R(orb), nr = R(nutshell);
      const ov = (a,b) => { if (!a||!b) return 0; const x=Math.max(0,Math.min(a[2],b[2])-Math.max(a[0],b[0])); const y=Math.max(0,Math.min(a[3],b[3])-Math.max(a[1],b[1])); return Math.round(x*y); };
      // every visible element overlapping the nutshell box, big ones first
      const over = [...document.querySelectorAll('body *')].filter(e => e.offsetParent !== null).map(e => {
        const r = R(e); const a = ov(r, nr);
        return {tag: e.tagName, cls: (typeof e.className === 'string' ? e.className : '').slice(0,60), rect: r, overlap: a};
      }).filter(x => x.overlap > 2000).sort((a,b) => b.overlap - a.overlap).slice(0,8);
      const faces = [...document.querySelectorAll('.deal-beat-photo.fp-speak-face')].filter(e => e.offsetParent !== null).map(R);
      return {titleRect: tr, titleText: title ? title.textContent.trim().slice(0,60) : null,
        orbRect: or_, nutshellRect: nr, titleOrbOverlap: ov(tr, or_),
        speakFaces: faces, nutshellOverlaps: over};
    }""")
    note("DE-deck-board37", **m)
    shot(page, "fix4-base-E-deck37.png")
    # deck end -> bridge, then F footer
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
    shot(page, "fix4-base-F-bridge.png")
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
      return {found: true, navRect: R(nav), scrollWidth: nav.scrollWidth, clientWidth: nav.clientWidth,
        scrollable: nav.scrollWidth > nav.clientWidth + 1, flexWrap: cs.flexWrap, overflowX: cs.overflowX,
        scrollTest: {before, setTo: 60, after}, links,
        innerWidth: window.innerWidth};
    }""")
    note("F-footer-links", **fm)
    ctx.close()
    browser.close()

LOG["errors"] = ERRORS
with open(os.path.join(OUT, "fix4-base.json"), "w") as f:
    json.dump(LOG, f, indent=2)
print("BASE PROBE DONE, console errors:", len(ERRORS))
for e in ERRORS[:10]:
    print("ERR:", e[:200])
