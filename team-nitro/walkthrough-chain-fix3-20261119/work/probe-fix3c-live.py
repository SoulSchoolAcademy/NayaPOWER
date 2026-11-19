#!/usr/bin/env python3
"""FIX3c live verification — certified certificate at 534 on the FIX3c
identity (overlaps must be gone, switch pill inside the plaque), crests
at 1920, and the returning-view other-identity buttons at 534.
Writes evidence/fix3c-live.json + screenshots. One fresh claim alias
(fix3certc) is created on purpose; do NOT delete rows (cleanup owed).
"""
import json, os, traceback
from playwright.sync_api import sync_playwright

HOME = os.path.expanduser("~")
EV = os.path.join(HOME, "workspace/team-nitro/walkthrough-chain-fix3-20261119/evidence")
STAGING = "https://naya-walk-beginning-staging.nayapower.workers.dev"
PROOF = "https://naya-proof-host.nayapower.workers.dev"
IDENT_C = (PROOF + "/?file=team-nitro/walk-v23-assembly-20261114/identity-fixed.html"
           "&ref=walkthrough/chain-fix3-20261119&cb=ee6a99aeb4a56262f978ff7685b7b5d343a6fede&t=1795057362")
OUT = {}

JS_CERT = """() => {
  const q = s => document.querySelector(s);
  const vis = el => !!el && !el.hidden && el.getBoundingClientRect().height > 0 &&
    getComputedStyle(el).display !== 'none';
  const plaque = q('.cert-plaque') || document.body;
  const leaves = [];
  plaque.querySelectorAll('*').forEach(el => {
    if (el.children.length) return;
    const t = (el.textContent || '').trim();
    if (!t) return;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) return;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return;
    leaves.push({t: t.slice(0, 60), cls: String(el.className).slice(0, 40),
      x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)});
  });
  const overlaps = [];
  for (let i = 0; i < leaves.length; i++) for (let j = i + 1; j < leaves.length; j++) {
    const a = leaves[i], b = leaves[j];
    const ox = Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x);
    const oy = Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y);
    if (ox > 2 && oy > 2) overlaps.push({a: a.t, b: b.t, ox: Math.round(ox), oy: Math.round(oy)});
  }
  const sw = q('#certSwitch');
  const swr = sw ? sw.getBoundingClientRect() : null;
  const pr = plaque.getBoundingClientRect();
  const face = q('.identity-face');
  const fr = face ? face.getBoundingClientRect() : null;
  return { vw: innerWidth, vh: innerHeight,
    certNo: q('#certNoValue') ? q('#certNoValue').textContent.trim() : null,
    heroText: q('#displayName') ? q('#displayName').textContent : null,
    statusVisible: vis(q('#aliasStatus')),
    statusText: q('#aliasStatus') ? q('#aliasStatus').textContent.trim() : null,
    keyValueVisible: vis(q('#keyValue')),
    lsName: (() => { try { return localStorage.getItem('nayanet_smart_name'); } catch(e){ return 'ERR'; } })(),
    plaque: {y: Math.round(pr.y), bottom: Math.round(pr.bottom), h: Math.round(pr.height)},
    faceH: fr ? Math.round(fr.height) : null,
    switchRect: swr ? {y: Math.round(swr.y), bottom: Math.round(swr.bottom),
      insidePlaque: swr.bottom <= pr.bottom + 1} : null,
    leaves: leaves, overlaps: overlaps };
}"""

def main():
    with sync_playwright() as pw:
        b = pw.firefox.launch(headless=True)
        try:
            # --- A. certified 534 on FIX3c identity ---
            ctx = b.new_context(viewport={"width": 534, "height": 900})
            p = ctx.new_page()
            p.route("**/welcome*", lambda route: route.abort())
            p.goto(IDENT_C, wait_until="load", timeout=60000)
            p.wait_for_timeout(2000)
            p.fill("#aliasInput", "fix3certc")
            p.wait_for_timeout(1800)
            ent = p.query_selector("button:has-text('ENTER')")
            if ent: ent.click()
            p.wait_for_timeout(4000)
            OUT["A_certified_534"] = p.evaluate(JS_CERT)
            p.screenshot(path=os.path.join(EV, "fix3c-live-A-cert-534.png"))
            # crests 1920 on the same bytes
            ctx2 = b.new_context(viewport={"width": 1920, "height": 999})
            p2 = ctx2.new_page()
            p2.goto(IDENT_C, wait_until="load", timeout=60000)
            p2.wait_for_timeout(1500)
            OUT["A_crests_1920"] = p2.evaluate("""() => [...document.querySelectorAll('.corner-crest')].map(el => {
              const r = el.getBoundingClientRect();
              return {cls: el.className, x: Math.round(r.x), right: Math.round(r.right),
                clipped: r.left < 0 || r.top < 0 || r.right > innerWidth || r.bottom > innerHeight};
            })""")
            ctx2.close()
            ctx.close()

            # --- B. returning view with two identities, 534 (reliable path) ---
            ctx = b.new_context(viewport={"width": 534, "height": 900})
            p = ctx.new_page()
            p.goto(STAGING + "/", wait_until="load", timeout=60000)
            p.evaluate("""() => { localStorage.setItem('nayanet_smart_alias','jordantest');
              localStorage.setItem('nayanet_smart_name','Jordan Test');
              localStorage.setItem('nayanet_smart_identities', JSON.stringify([
                {alias:'jordantest', name:'Jordan Test'},
                {alias:'walkertest', name:'Walker Test'}])); }""")
            p.reload(wait_until="load")
            p.wait_for_timeout(800)
            OUT["B_returning_534"] = p.evaluate("""() => {
              const q = s => document.querySelector(s);
              const vis = el => !!el && !el.hidden && el.getBoundingClientRect().height > 0 &&
                getComputedStyle(el).display !== 'none';
              const btn = el => el ? {t: el.textContent.trim(), vis: vis(el),
                scrollW: el.scrollWidth, clientW: el.clientWidth,
                truncated: el.scrollWidth > el.clientWidth + 1,
                rect: (() => { const r = el.getBoundingClientRect();
                  return {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)}; })()} : null;
              return { returningHidden: q('#returningView') ? q('#returningView').hidden : null,
                entryFormHidden: q('#entryForm') ? q('#entryForm').hidden : null,
                stageOn: document.body.classList.contains('fp-stage-on'),
                jump: btn(q('#jumpBackIn')),
                others: [...document.querySelectorAll('.returning-other')].map(btn) };
            }""")
            p.screenshot(path=os.path.join(EV, "fix3c-live-B-returning-534.png"))
            ctx.close()
        finally:
            b.close()
        with open(os.path.join(EV, "fix3c-live.json"), "w") as f:
            json.dump(OUT, f, indent=1)
        print("WROTE fix3c-live.json")

try:
    main()
except Exception:
    traceback.print_exc()
    with open(os.path.join(EV, "fix3c-live.json"), "w") as f:
        json.dump(OUT, f, indent=1)
    print("WROTE PARTIAL fix3c-live.json")
