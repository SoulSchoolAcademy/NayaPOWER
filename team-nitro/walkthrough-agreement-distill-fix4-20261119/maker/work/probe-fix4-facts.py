#!/usr/bin/env python3
"""Fix-4 maker — DOM facts for the D-title cascade (no walks).
For /agreement, /?stage=deck, /?stage=letter: find the 'Congratulations'
h2, report its class, its article's identifiers, ancestor chain, computed
font-size, and which candidate selectors match. Also: identity taken-state
timing (does .taken arrive?), door h1 text-line rects vs crests.
"""
import json, os
from playwright.sync_api import sync_playwright

BASE = "https://naya-walk-beginning-staging.nayapower.workers.dev"
OUT = os.path.expanduser("~/workspace/team-nitro/walkthrough-agreement-distill-fix4-20261119/maker/work/proof-fix4")
LOG = {"steps": [], "errors": []}
ERRORS = []

def note(step, **kw):
    rec = {"step": step, **kw}
    LOG["steps"].append(rec)
    print(json.dumps(rec)[:1400], flush=True)
    return rec

def page_errors(page):
    page.on("pageerror", lambda e: ERRORS.append("pageerror: " + str(e)))
    page.on("console", lambda m: ERRORS.append("console." + m.type + ": " + m.text) if m.type == "error" else None)

TITLE_JS = """() => {
  const hs = [...document.querySelectorAll('h2')].filter(h => (h.textContent||'').includes('Congratulations'));
  if (!hs.length) return {found: false, h2count: document.querySelectorAll('h2').length};
  const t = hs[0];
  const chain = [];
  let el = t;
  while (el && el !== document.body) {
    chain.push((el.tagName||'') + (el.id ? '#'+el.id : '') + (el.className && typeof el.className==='string' ? '.'+el.className.trim().split(/\\s+/).join('.') : '') + (el.getAttribute && el.getAttribute('data-beat') ? '[data-beat='+el.getAttribute('data-beat')+']' : ''));
    el = el.parentElement;
  }
  chain.push('BODY.' + document.body.className.trim().split(/\\s+/).join('.'));
  const cs = getComputedStyle(t);
  return {found: true, titleClass: t.className, titleFontPx: parseFloat(cs.fontSize),
    articleClass: t.closest('article') ? t.closest('article').className : null,
    articleId: t.closest('article') ? t.closest('article').id : null,
    articleBeat: t.closest('article') ? t.closest('article').getAttribute('data-beat') : null,
    chain: chain.slice(0, 10),
    matches: {
      'article[data-beat="37"] .ib-title': t.matches('article[data-beat="37"] .ib-title'),
      '.frame-scroll .ib-title': t.matches('.frame-scroll .ib-title'),
      'body.af-deck-on #deckBody .ib-title': t.matches('body.af-deck-on #deckBody .ib-title'),
      '#fpAgreement .ib-title': t.matches('#fpAgreement .ib-title')
    }};
}"""

with sync_playwright() as pw:
    browser = pw.firefox.launch(headless=True)
    for label, url in [("unfold", "/agreement"), ("deck", "/?stage=deck"), ("letter", "/?stage=letter")]:
        ctx = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        page = ctx.new_page(); page_errors(page)
        page.goto(BASE + url, timeout=60000)
        page.wait_for_timeout(3500)
        note("D-title-facts-" + label, **page.evaluate(TITLE_JS))
        ctx.close()

    # A taken-state timing: poll the plaque class for up to 20 s
    ctx = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    page = ctx.new_page(); page_errors(page)
    page.goto(BASE + "/identity.html?name=Shawn&alias=Shawn", timeout=60000)
    for wait in [4, 8, 12, 20]:
        page.wait_for_timeout(4000 if wait == 4 else 4000)
        m = page.evaluate("""() => {
          const R = el => { if (!el) return null; const r = el.getBoundingClientRect();
            return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; };
          const ov = (a,b) => { if (!a||!b) return 0; const x=Math.max(0,Math.min(a[2],b[2])-Math.max(a[0],b[0])); const y=Math.max(0,Math.min(a[3],b[3])-Math.max(a[1],b[1])); return Math.round(x*y); };
          const name = document.getElementById('displayName');
          const title = document.querySelector('.cert-title');
          const plaque = document.querySelector('.cert-plaque');
          const note = document.getElementById('hubNote');
          const cs = name ? getComputedStyle(name) : null;
          return {plaqueClass: plaque ? plaque.className : null,
            noteHidden: note ? note.hidden : null, noteClass: note ? note.className : null,
            nameFontPx: cs ? parseFloat(cs.fontSize) : null,
            nameRect: R(name), titleRect: R(title),
            nameTitleOverlap: ov(R(name), R(title))}; }""")
        note("A-taken-poll", waitedS=wait, **m)
        if m["plaqueClass"] and "taken" in m["plaqueClass"]:
            break
    page.screenshot(path=os.path.join(OUT, "fix4-verify-A-taken.png"))
    ctx.close()

    # B: h1 TEXT line rects vs crests
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
      const cs = getComputedStyle(h1);
      return {h1Rect: R(h1), h1Padding: cs.paddingLeft + ' / ' + cs.paddingRight,
        lineRects: lines, crestRects: crests,
        lineCrestOverlap: lines.reduce((t, lr) => t + crests.reduce((s, c) => s + ov(lr, c), 0), 0),
        h1Text: h1.textContent};
    }""")
    note("B-door-text-lines", **m)
    page.screenshot(path=os.path.join(OUT, "fix4-verify-B-door-text.png"))
    ctx.close()
    browser.close()

LOG["errors"] = ERRORS
with open(os.path.join(OUT, "fix4-facts.json"), "w") as f:
    json.dump(LOG, f, indent=2)
print("FACTS PROBE DONE, console errors:", len(ERRORS))
