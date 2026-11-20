#!/usr/bin/env python3
"""Fix-4b maker — FINAL verification on staged fix-4b bytes.
Proves the corrected fixes at 390x844 (rects + screenshots) + F9 spot
regression. Writes proof-fix4/fix4-verify2.json + fix4b-*.png.
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
    print(json.dumps(rec)[:1200], flush=True)
    return rec

def shot(page, name):
    page.screenshot(path=os.path.join(OUT, name))
    return name

def page_errors(page):
    page.on("pageerror", lambda e: ERRORS.append("pageerror: " + str(e)))
    page.on("console", lambda m: ERRORS.append("console." + m.type + ": " + m.text) if m.type == "error" else None)

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

TITLE_OVERLAPPERS = """() => {
  const R = el => { if (!el) return null; const r = el.getBoundingClientRect();
    return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; };
  const ov = (a,b) => { if (!a||!b) return 0; const x=Math.max(0,Math.min(a[2],b[2])-Math.max(a[0],b[0])); const y=Math.max(0,Math.min(a[3],b[3])-Math.max(a[1],b[1])); return Math.round(x*y); };
  const t = [...document.querySelectorAll('h2')].find(h => (h.textContent||'').includes('Congratulations'));
  if (!t) return {found: false};
  const tr = R(t);
  const over = [...document.querySelectorAll('body *')].filter(e => e !== t && !t.contains(e) && !e.contains(t)).map(e => {
    const r = R(e); const a = ov(r, tr);
    return {tag: e.tagName, cls: (typeof e.className === 'string' ? e.className : '').slice(0,70), rect: r, overlap: a};
  }).filter(x => x.overlap > 0).sort((a,b) => b.overlap - a.overlap).slice(0,8);
  return {found: true, titleClass: t.className, titleFontPx: parseFloat(getComputedStyle(t).fontSize),
    titleRect: tr, titleText: t.textContent.trim().slice(0,50), titleOverlaps: over};
}"""

with sync_playwright() as pw:
    browser = pw.firefox.launch(headless=True)

    # ---------- A taken-state (wait for .taken) + plain state ----------
    ctx = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    page = ctx.new_page(); page_errors(page)
    page.goto(BASE + "/identity.html?name=Shawn&alias=Shawn", timeout=60000)
    page.wait_for_timeout(6000)
    m = page.evaluate("""() => {
      const R = el => { if (!el) return null; const r = el.getBoundingClientRect();
        return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; };
      const ov = (a,b) => { if (!a||!b) return 0; const x=Math.max(0,Math.min(a[2],b[2])-Math.max(a[0],b[0])); const y=Math.max(0,Math.min(a[3],b[3])-Math.max(a[1],b[1])); return Math.round(x*y); };
      const name = document.getElementById('displayName');
      const title = document.querySelector('.cert-title');
      const line = document.querySelector('.cert-certifies');
      const wrap = document.querySelector('.face-center');
      const status = document.querySelector('.alias-status');
      const input = document.getElementById('aliasInput');
      return {plaqueClass: (document.querySelector('.cert-plaque')||{}).className,
        input: input ? input.value : null, hero: name ? name.textContent : null,
        heroHidden: name ? name.hidden : null, dataText: name ? name.getAttribute('data-text') : null,
        nameFontPx: name ? parseFloat(getComputedStyle(name).fontSize) : null,
        nameRect: R(name), titleRect: R(title), lineRect: R(line),
        lineDisplay: line ? getComputedStyle(line).display : null,
        wrapRect: R(wrap), statusRect: R(status),
        nameTitleOv: ov(R(name), R(title)), nameLineOv: ov(R(name), R(line)),
        nameWrapOv: ov(R(name), R(wrap)), wrapStatusOv: ov(R(wrap), R(status)),
        innerWidth: window.innerWidth, scrollW: document.documentElement.scrollWidth};
    }""")
    note("A-taken-final", **m)
    shot(page, "fix4b-A-identity.png")
    ctx.close()

    ctx = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    page = ctx.new_page(); page_errors(page)
    page.goto(BASE + "/identity.html", timeout=60000)
    page.wait_for_timeout(4000)
    m = page.evaluate("""() => {
      const line = document.querySelector('.cert-certifies');
      const name = document.getElementById('displayName');
      const R = el => { if (!el) return null; const r = el.getBoundingClientRect();
        return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; };
      return {plaqueClass: (document.querySelector('.cert-plaque')||{}).className,
        lineDisplay: line ? getComputedStyle(line).display : null, lineRect: R(line),
        lineText: line ? line.textContent.trim() : null,
        hero: name ? name.textContent : null, heroHidden: name ? name.hidden : null}; }""")
    note("A-plain-line-visible", **m)
    shot(page, "fix4b-A-plain.png")
    ctx.close()

    # ---------- C banner (identity file changed) ----------
    ctx = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    page = ctx.new_page(); page_errors(page)
    page.goto(BASE + "/identity.html?name=Shawn&alias=Shawn", timeout=60000)
    page.wait_for_timeout(6000)
    page.evaluate("() => { const n = document.getElementById('hubNote'); if (n) n.scrollIntoView({block:'center'}); }")
    page.wait_for_timeout(600)
    cm = page.evaluate("""() => {
      const R = el => { if (!el) return null; const r = el.getBoundingClientRect();
        return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; };
      const ov = (a,b) => { if (!a||!b) return 0; const x=Math.max(0,Math.min(a[2],b[2])-Math.max(a[0],b[0])); const y=Math.max(0,Math.min(a[3],b[3])-Math.max(a[1],b[1])); return Math.round(x*y); };
      const note = document.getElementById('hubNote');
      const stone = document.querySelector('.cert-plaque .frame-stone');
      const nr = R(note);
      const rng = document.createRange(); rng.selectNodeContents(note);
      const lineRects = [...rng.getClientRects()].map(r => [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]);
      const crests = [...document.querySelectorAll('.corner-crest')].map(R);
      return {noteRect: nr, noteTextClipped: note.scrollWidth > note.clientWidth + 1,
        lineRects, lineCrestOverlap: lineRects.reduce((t, lr) => t + crests.reduce((s, c) => s + ov(lr, c), 0), 0),
        stoneDisplay: stone ? getComputedStyle(stone).display : 'absent',
        noteText: (note.textContent||'').replace(/\\s+/g,' ').trim().slice(0,120)}; }""")
    note("C-banner-final", **cm)
    shot(page, "fix4b-C-banner.png")
    ctx.close()

    # ---------- B door text lines (walk file unchanged, quick re-prove) ----------
    ctx = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    page = ctx.new_page(); page_errors(page)
    page.goto(BASE + "/welcome?name=FixFour&alias=fix4door7x", timeout=60000)
    page.wait_for_timeout(4000)
    m = page.evaluate("""() => {
      const R = el => { if (!el) return null; const r = el.getBoundingClientRect();
        return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; };
      const ov = (a,b) => { if (!a||!b) return 0; const x=Math.max(0,Math.min(a[2],b[2])-Math.max(a[0],b[0])); const y=Math.max(0,Math.min(a[3],b[3])-Math.max(a[1],b[1])); return Math.round(x*y); };
      const h1 = document.querySelector('#step-door .p3-question');
      const rng = document.createRange(); rng.selectNodeContents(h1);
      const lines = [...rng.getClientRects()].map(r => [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]);
      const crests = [...document.querySelectorAll('.p3-crest')].map(R);
      return {h1Padding: getComputedStyle(h1).paddingLeft + ' / ' + getComputedStyle(h1).paddingRight,
        lineRects: lines, lineCrestOverlap: lines.reduce((t, lr) => t + crests.reduce((s, c) => s + ov(lr, c), 0), 0)};
    }""")
    note("B-door-final", **m)
    shot(page, "fix4b-B-door.png")
    page.wait_for_timeout(10000)
    note("B-door-10s-hold-final", visibleSteps=page.evaluate("() => [...document.querySelectorAll('.p3-step')].filter(s => !s.hidden).map(s => s.id)"))
    page.locator("#doorContinue").click(timeout=6000)
    page.wait_for_timeout(1200)
    note("B-door-continue-final", visibleSteps=page.evaluate("() => [...document.querySelectorAll('.p3-step')].filter(s => !s.hidden).map(s => s.id)"))
    ctx.close()

    # ---------- D unfold /agreement 1->37 ----------
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
    note("D-unfold-walk-final", counters=[c for c in counters if c])
    note("D-unfold-board37-final", **page.evaluate(TITLE_OVERLAPPERS))
    shot(page, "fix4b-D-unfold37.png")
    ctx.close()

    # ---------- D+E deck 1->37 -> bridge -> pair (letter first, then story) ----------
    ctx = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    page = ctx.new_page(); page_errors(page)
    page.goto(BASE + "/?stage=deck", timeout=60000)
    page.wait_for_timeout(2500)
    counters = walk_to_37(page)
    note("DE-deck-walk-final", counters=counters)
    note("DE-deck-board37-final", **page.evaluate(TITLE_OVERLAPPERS))
    m = page.evaluate("""() => {
      const R = el => { if (!el) return null; const r = el.getBoundingClientRect();
        return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; };
      const ov = (a,b) => { if (!a||!b) return 0; const x=Math.max(0,Math.min(a[2],b[2])-Math.max(a[0],b[0])); const y=Math.max(0,Math.min(a[3],b[3])-Math.max(a[1],b[1])); return Math.round(x*y); };
      const board = document.querySelector('#fpAgreement.fp-now') || document.querySelector('.fp-now');
      const nutshell = board ? board.querySelector('.ib-nutshell') : null;
      const signPhoto = board ? board.querySelector('.deal-sign-photo') : null;
      return {nutshellRect: R(nutshell), signPhotoRect: R(signPhoto),
        nutshellSignOverlap: ov(R(nutshell), R(signPhoto))};
    }""")
    note("E-deck-final", **m)
    shot(page, "fix4b-E-deck37.png")
    btns = page.evaluate("() => [...document.querySelectorAll('#fpStageBarB button, #fpStageBarT button')].filter(b=>b.offsetParent!==null).map(b=>({id:b.id, t:(b.innerText||'').trim().slice(0,40)}))")
    for b in btns:
        if b["id"] not in ("fpDeckBack", "fpStageExit"):
            page.locator("#" + b["id"]).click(timeout=6000)
            page.wait_for_timeout(3000)
            break
    note("DE-after-deck-enter-final", url=page.url,
         bodyStart=page.evaluate("() => document.body.innerText.replace(/\\s+/g,' ').trim().slice(0,150)"))
    # F footer
    fm = page.evaluate("""() => {
      const nav = document.querySelector('#fpLegal .fp-legal-links');
      if (!nav) return {found: false};
      const before = nav.scrollLeft; nav.scrollLeft = 60; const after = nav.scrollLeft; nav.scrollLeft = 0;
      return {found: true, scrollWidth: nav.scrollWidth, clientWidth: nav.clientWidth,
        scrollable: nav.scrollWidth > nav.clientWidth + 1, scrollTest: {before, after}}; }""")
    note("F-footer-final", **fm)
    shot(page, "fix4b-F-bridge.png")
    # bridge pair: letter FIRST
    pair = page.evaluate("() => [...document.querySelectorAll('button')].filter(b=>b.offsetParent!==null).map(b=>({id:b.id, t:(b.innerText||'').trim().slice(0,50)}))")
    note("F9-bridge-buttons-final", buttons=[b for b in pair if 'visual story' in b['t'] or 'agreement' in b['t'] or 'Continue' in b['t']])
    try:
        page.locator("#fpBridgeLetter").click(timeout=6000)
        page.wait_for_timeout(2500)
        note("F9-pair-letter-click", url=page.url,
             counter=page.evaluate("() => { const m = document.body.innerText.match(/(\\d+)\\s*\\/\\s*37/); return m ? m[0] : null; }"),
             bodyStart=page.evaluate("() => document.body.innerText.replace(/\\s+/g,' ').trim().slice(0,150)"))
    except Exception as e:
        note("F9-pair-letter-error", error=str(e)[:200])
    # reload the bridge in the same context (agree state persists in localStorage) and click story
    page.goto(BASE + "/?stage=bridge", timeout=60000)
    page.wait_for_timeout(3000)
    pair2 = page.evaluate("() => [...document.querySelectorAll('button')].filter(b=>b.offsetParent!==null).map(b=>({id:b.id, t:(b.innerText||'').trim().slice(0,50)}))")
    note("F9-bridge-buttons-reload", buttons=[b for b in pair2 if 'visual story' in b['t'] or 'agreement' in b['t'] or 'Continue' in b['t']])
    try:
        page.locator("#fpBridgeDeck").click(timeout=6000)
        page.wait_for_timeout(2500)
        note("F9-pair-story-click", url=page.url,
             counter=page.evaluate("() => { const m = document.body.innerText.match(/(\\d+)\\s*\\/\\s*37/); return m ? m[0] : null; }"),
             bodyStart=page.evaluate("() => document.body.innerText.replace(/\\s+/g,' ').trim().slice(0,150)"))
    except Exception as e:
        note("F9-pair-story-error", error=str(e)[:200])
    ctx.close()

    # ---------- letter 1->37 ----------
    ctx = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    page = ctx.new_page(); page_errors(page)
    page.goto(BASE + "/?stage=letter", timeout=60000)
    page.wait_for_timeout(2500)
    counters = walk_to_37(page)
    note("F9-letter-walk-final", counters=counters)
    note("F9-letter-board37-final", **page.evaluate(TITLE_OVERLAPPERS))
    m = page.evaluate("""() => {
      const R = el => { if (!el) return null; const r = el.getBoundingClientRect();
        return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; };
      const ov = (a,b) => { if (!a||!b) return 0; const x=Math.max(0,Math.min(a[2],b[2])-Math.max(a[0],b[0])); const y=Math.max(0,Math.min(a[3],b[3])-Math.max(a[1],b[1])); return Math.round(x*y); };
      const board = document.querySelector('#fpAgreement.fp-now') || document.querySelector('.fp-now');
      const nutshell = board ? board.querySelector('.ib-nutshell') : null;
      const signPhoto = board ? board.querySelector('.deal-sign-photo') : null;
      return {nutshellRect: R(nutshell), signPhotoRect: R(signPhoto),
        nutshellSignOverlap: ov(R(nutshell), R(signPhoto))};
    }""")
    note("F9-letter-E-final", **m)
    shot(page, "fix4b-letter37.png")
    ctx.close()
    browser.close()

LOG["errors"] = ERRORS
with open(os.path.join(OUT, "fix4-verify2.json"), "w") as f:
    json.dump(LOG, f, indent=2)
print("VERIFY2 PROBE DONE, console errors:", len(ERRORS))
for e in ERRORS[:10]:
    print("ERR:", e[:200])
