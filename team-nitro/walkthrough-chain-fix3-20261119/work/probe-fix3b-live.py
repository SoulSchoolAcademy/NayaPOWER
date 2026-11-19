#!/usr/bin/env python3
"""FIX3b live verification — crests on the FIX3b identity, the returning-view
timing/truncation at 534, and the certified certificate at 534.
Writes evidence/fix3b-live.json + screenshots. One fresh claim alias
(fix3cert534) is created on purpose; do NOT delete rows (cleanup owed).
"""
import json, os, traceback
from playwright.sync_api import sync_playwright

HOME = os.path.expanduser("~")
EV = os.path.join(HOME, "workspace/team-nitro/walkthrough-chain-fix3-20261119/evidence")
STAGING = "https://naya-walk-beginning-staging.nayapower.workers.dev"
PROOF = "https://naya-proof-host.nayapower.workers.dev"
IDENT_B = (PROOF + "/?file=team-nitro/walk-v23-assembly-20261114/identity-fixed.html"
           "&ref=walkthrough/chain-fix3-20261119&cb=c6801542b8fb481b3754905fda8d4ac48d0d4c6e&t=1795055536")
OUT = {}

JS_CRESTS = """() => [...document.querySelectorAll('.corner-crest')].map(el => {
  const r = el.getBoundingClientRect();
  return {cls: el.className, x: Math.round(r.x), y: Math.round(r.y),
    w: Math.round(r.width), h: Math.round(r.height),
    right: Math.round(r.right), bottom: Math.round(r.bottom),
    clipped: r.left < 0 || r.top < 0 || r.right > innerWidth || r.bottom > innerHeight};
})"""

JS_RETURNING = """() => {
  const q = s => document.querySelector(s);
  const vis = el => !!el && !el.hidden && el.getBoundingClientRect().height > 0 &&
    getComputedStyle(el).display !== 'none';
  const btn = (el) => el ? {t: el.textContent.trim(), vis: vis(el),
    scrollW: el.scrollWidth, clientW: el.clientWidth,
    truncated: el.scrollWidth > el.clientWidth + 1,
    rect: (() => { const r = el.getBoundingClientRect();
      return {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)}; })()} : null;
  return { t: Date.now(),
    returningHidden: q('#returningView') ? q('#returningView').hidden : null,
    entryFormHidden: q('#entryForm') ? q('#entryForm').hidden : null,
    jump: btn(q('#jumpBackIn')),
    others: [...document.querySelectorAll('.returning-other')].map(btn),
    stageOn: document.body.classList.contains('fp-stage-on'),
  };
}"""

JS_CERT = """() => {
  const q = s => document.querySelector(s);
  const vis = el => !!el && !el.hidden && el.getBoundingClientRect().height > 0 &&
    getComputedStyle(el).display !== 'none';
  const plaque = q('.cert-plaque') || q('#certPlaque') || document.body;
  const leaves = [];
  plaque.querySelectorAll('*').forEach(el => {
    if (el.children.length) return;
    const t = (el.textContent || '').trim();
    if (!t) return;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) return;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return;
    leaves.push({t: t.slice(0, 60), cls: el.className && el.className.baseVal !== undefined ? '' : String(el.className).slice(0, 40),
      x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)});
  });
  const overlaps = [];
  for (let i = 0; i < leaves.length; i++) for (let j = i + 1; j < leaves.length; j++) {
    const a = leaves[i], b = leaves[j];
    const ox = Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x);
    const oy = Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y);
    if (ox > 2 && oy > 2) overlaps.push({a: a.t, b: b.t, ox: Math.round(ox), oy: Math.round(oy)});
  }
  return { vw: innerWidth, vh: innerHeight,
    certNo: q('#certNo') ? q('#certNo').textContent.trim() : null,
    heroText: q('#displayName') ? q('#displayName').textContent : null,
    keyValueText: q('#keyValue') ? q('#keyValue').textContent : null,
    keyValueVisible: vis(q('#keyValue')),
    lsName: (() => { try { return localStorage.getItem('nayanet_smart_name'); } catch(e){ return 'ERR'; } })(),
    leaves: leaves, overlaps: overlaps };
}"""

def main():
    with sync_playwright() as pw:
        b = pw.firefox.launch(headless=True)
        try:
            # --- A. crests, FIX3b identity, 1920 + 534 ---
            for w, h in ((1920, 999), (534, 900)):
                ctx = b.new_context(viewport={"width": w, "height": h})
                p = ctx.new_page()
                p.goto(IDENT_B, wait_until="load", timeout=60000)
                p.wait_for_timeout(1500)
                OUT[f"A_crests_{w}"] = p.evaluate(JS_CRESTS)
                p.screenshot(path=os.path.join(EV, f"fix3b-live-A-crests-{w}.png"))
                ctx.close()

            # --- B. returning view timing + truncation, 534 ---
            ctx = b.new_context(viewport={"width": 534, "height": 900})
            ctx.add_init_script("""() => { try {
              localStorage.setItem('nayanet_smart_alias','jordantest');
              localStorage.setItem('nayanet_smart_name','Jordan Test');
              localStorage.setItem('nayanet_smart_identities', JSON.stringify([
                {alias:'jordantest', name:'Jordan Test'},
                {alias:'walkertest', name:'Walker Test'}]));
            } catch(e){} }""")
            p = ctx.new_page()
            p.goto(STAGING + "/", wait_until="load", timeout=60000)
            p.wait_for_timeout(800)
            OUT["B_returning_800ms"] = p.evaluate(JS_RETURNING)
            p.screenshot(path=os.path.join(EV, "fix3b-live-B-returning-800ms.png"))
            p.wait_for_timeout(2500)
            OUT["B_returning_3300ms"] = p.evaluate(JS_RETURNING)
            p.screenshot(path=os.path.join(EV, "fix3b-live-B-returning-3300ms.png"))
            ctx.close()

            # --- C. certified certificate at 534 ---
            ctx = b.new_context(viewport={"width": 534, "height": 900})
            p = ctx.new_page()
            p.route("**/welcome*", lambda route: route.abort())
            p.goto(IDENT_B, wait_until="load", timeout=60000)
            p.wait_for_timeout(2000)
            p.fill("#aliasInput", "fix3cert534")
            p.wait_for_timeout(1800)
            OUT["C_available"] = p.evaluate(JS_CERT)
            ent = p.query_selector("button:has-text('ENTER')")
            if ent: ent.click()
            p.wait_for_timeout(4000)
            OUT["C_certified_534"] = p.evaluate(JS_CERT)
            p.screenshot(path=os.path.join(EV, "fix3b-live-C-cert-534.png"))
            ctx.close()
        finally:
            b.close()
        with open(os.path.join(EV, "fix3b-live.json"), "w") as f:
            json.dump(OUT, f, indent=1)
        print("WROTE fix3b-live.json")

try:
    main()
except Exception:
    traceback.print_exc()
    with open(os.path.join(EV, "fix3b-live.json"), "w") as f:
        json.dump(OUT, f, indent=1)
    print("WROTE PARTIAL fix3b-live.json")
