#!/usr/bin/env python3
"""Fix-4 maker — detail geometry for A (wrapper top, center stone), D (unfold orb/avatar), E (deck .fp-now board 37)."""
import json, os
from playwright.sync_api import sync_playwright

BASE = "https://naya-walk-beginning-staging.nayapower.workers.dev"
OUT = os.path.expanduser("~/workspace/team-nitro/walkthrough-agreement-distill-fix4-20261119/maker/work/proof-base")
LOG = {"steps": [], "errors": []}
ERRORS = []

def note(step, **kw):
    rec = {"step": step, **kw}
    LOG["steps"].append(rec)
    print(json.dumps(rec)[:1200], flush=True)
    return rec

def shot(page, name):
    page.screenshot(path=os.path.join(OUT, name))

OVERLAP_JS = """(targetRect) => {
  const R = el => { const r = el.getBoundingClientRect();
    return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; };
  const ov = (a,b) => { const x=Math.max(0,Math.min(a[2],b[2])-Math.max(a[0],b[0]));
    const y=Math.max(0,Math.min(a[3],b[3])-Math.max(a[1],b[1])); return Math.round(x*y); };
  const out = [];
  document.querySelectorAll('body *').forEach(e => {
    if (e.offsetParent === null && e.tagName !== 'BODY') return;
    const r = R(e); const a = ov(r, targetRect);
    if (a > 100) out.push({tag: e.tagName, cls: (typeof e.className==='string'?e.className:'').slice(0,70),
      id: e.id || '', rect: r, overlap: a,
      text: (e.textContent||'').replace(/\\s+/g,' ').trim().slice(0,40)});
  });
  return out.sort((a,b)=>b.overlap-a.overlap).slice(0,10);
}"""

with sync_playwright() as pw:
    browser = pw.firefox.launch(headless=True)
    # ---------- A detail ----------
    ctx = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    page = ctx.new_page()
    page.on("pageerror", lambda e: ERRORS.append(str(e)))
    page.goto(BASE + "/identity.html?name=Shawn&alias=Shawn", timeout=60000)
    page.wait_for_timeout(4000)
    m = page.evaluate("""() => {
      const R = el => { if (!el) return null; const r = el.getBoundingClientRect();
        return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; };
      const name = document.getElementById('displayName');
      const wrap = document.querySelector('.alias-field-wrapper');
      const fc = document.querySelector('.face-center');
      const title = document.querySelector('.cert-title');
      const cs = getComputedStyle(name);
      return {nameRect: R(name), titleRect: R(title), wrapRect: R(wrap), faceCenterRect: R(fc),
        nameFont: cs.fontSize, nameBottom: cs.bottom, nameLineHeight: cs.lineHeight,
        titleBottom: R(title)[3]};
    }""")
    note("A-detail", **m)
    noteRect = page.evaluate("() => { const n = document.getElementById('hubNote'); const r = n.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; }")
    ov = page.evaluate(OVERLAP_JS, noteRect)
    note("C-note-overlaps", noteRect=noteRect, overlappers=ov)
    ctx.close()

    # ---------- D unfold detail ----------
    ctx = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    page = ctx.new_page()
    page.on("pageerror", lambda e: ERRORS.append(str(e)))
    page.goto(BASE + "/agreement", timeout=60000)
    page.wait_for_timeout(2500)
    for i in range(45):
        c = page.evaluate("() => { const m = document.body.innerText.match(/(\\d+)\\s*\\/\\s*37/); return m ? m[0] : null; }")
        if c and c.startswith("37"):
            break
        loc = page.locator("button", has_text="Keep reading").locator("visible=true").first
        if loc.count() == 0:
            loc = page.locator("button", has_text="Next").locator("visible=true").first
        loc.click(timeout=5000)
        page.wait_for_timeout(450)
    m = page.evaluate("""() => {
      const R = el => { if (!el) return null; const r = el.getBoundingClientRect();
        return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; };
      const b37 = document.querySelector('article[data-beat="37"]');
      const title = b37 ? b37.querySelector('h2.ib-title') : null;
      const tr = R(title);
      const photos = [...document.querySelectorAll('.deal-beat-photo')].filter(e => e.offsetParent !== null).map(e => ({cls: e.className, rect: R(e)}));
      const orbs = [...document.querySelectorAll('[class*="orb"]')].filter(e => e.offsetParent !== null).map(e => ({cls: (typeof e.className==='string'?e.className:''), rect: R(e)}));
      return {titleRect: tr, titleFont: title ? getComputedStyle(title).fontSize : null,
        blocktopRect: b37 ? R(b37.querySelector('.ib-blocktop')) : null,
        boardRect: b37 ? R(b37) : null, visiblePhotos: photos, visibleOrbs: orbs};
    }""")
    note("D-detail", **m)
    titleRect = m["titleRect"]
    ov = page.evaluate(OVERLAP_JS, titleRect)
    note("D-title-overlaps", titleRect=titleRect, overlappers=ov)
    ctx.close()

    # ---------- E deck detail ----------
    ctx = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    page = ctx.new_page()
    page.on("pageerror", lambda e: ERRORS.append(str(e)))
    page.goto(BASE + "/?stage=deck", timeout=60000)
    page.wait_for_timeout(2500)
    for i in range(40):
        c = page.evaluate("() => { const m = document.body.innerText.match(/(\\d+)\\s*\\/\\s*37/); return m ? m[0] : null; }")
        if c and c.startswith("37"):
            break
        page.locator("#fpNextBtn").click(timeout=6000)
        page.wait_for_timeout(500)
    note("E-deck-at-37", counter=c)
    m = page.evaluate("""() => {
      const R = el => { if (!el) return null; const r = el.getBoundingClientRect();
        return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; };
      const now = document.querySelector('.letter-beat.fp-now, article.fp-now');
      const title = now ? now.querySelector('h2') : document.querySelector('h2.ib-title');
      const tr = R(title);
      const nutshell = now ? now.querySelector('.ib-nutshell') : null;
      const photos = [...document.querySelectorAll('.deal-beat-photo')].filter(e => e.offsetParent !== null).map(e => ({cls: e.className, rect: R(e)}));
      const orbs = [...document.querySelectorAll('[class*="orb"]')].filter(e => e.offsetParent !== null).map(e => ({cls: (typeof e.className==='string'?e.className:''), rect: R(e)}));
      return {nowClass: now ? now.className.slice(0,100) : null, titleRect: tr,
        titleText: title ? title.textContent.trim().slice(0,50) : null,
        nutshellRect: R(nutshell), boardRect: now ? R(now) : null,
        visiblePhotos: photos, visibleOrbs: orbs,
        nextBtn: (() => { const b = document.getElementById('fpNextBtn'); return b ? b.innerText.trim() : null; })()};
    }""")
    note("E-detail", **m)
    if m["nutshellRect"]:
        ov = page.evaluate(OVERLAP_JS, m["nutshellRect"])
        note("E-nutshell-overlaps", nutshellRect=m["nutshellRect"], overlappers=ov)
    if m["titleRect"]:
        ov2 = page.evaluate(OVERLAP_JS, m["titleRect"])
        note("E-title-overlaps", titleRect=m["titleRect"], overlappers=ov2)
    shot(page, "fix4-base-E-deck37.png")
    ctx.close()
    browser.close()

LOG["errors"] = ERRORS
with open(os.path.join(OUT, "fix4-base-detail.json"), "w") as f:
    json.dump(LOG, f, indent=2)
print("DETAIL DONE, errors:", len(ERRORS))
