#!/usr/bin/env python3
"""FIX4 live verification — certified certificate overlap walk at 1920 + 534
on the FIX4 identity (the stale status must be hidden at BOTH widths, zero
overlaps), plus the follow-on #1 re-probe: deck/letter arrival with keys set
fresh in the same context (the checker's probe-B, built for exactly this).
Writes evidence/fix4-live.json + screenshots. Two fresh claim aliases
(fix4cert, fix4cert534) are created on purpose; do NOT delete rows
(registry cleanup owed separately).
"""
import json, os, traceback
from playwright.sync_api import sync_playwright

HOME = os.path.expanduser("~")
EV = os.path.join(HOME, "workspace/team-nitro/walkthrough-chain-fix4-20261119/evidence")
STAGING = "https://naya-walk-beginning-staging.nayapower.workers.dev"
PROOF = "https://naya-proof-host.nayapower.workers.dev"
IDENT_C = (PROOF + "/?file=team-nitro/walk-v23-assembly-20261114/identity-fixed.html"
           "&ref=walkthrough/chain-fix4-20261119&cb=PLACEHOLDER&t=1795070000")
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
  const st = q('#aliasStatus');
  const str = st ? st.getBoundingClientRect() : null;
  return { vw: innerWidth, vh: innerHeight,
    certNo: q('#certNoValue') ? q('#certNoValue').textContent.trim() : null,
    heroText: q('#displayName') ? q('#displayName').textContent : null,
    statusVisible: vis(st),
    statusText: st ? st.textContent.trim() : null,
    statusRect: str ? {x: Math.round(str.x), y: Math.round(str.y), w: Math.round(str.width), h: Math.round(str.height)} : null,
    statusComputedDisplay: st ? getComputedStyle(st).display : null,
    plaqueCertified: plaque.classList.contains('is-certified'),
    keyValueVisible: vis(q('#keyValue')),
    lsName: (() => { try { return localStorage.getItem('nayanet_smart_name'); } catch(e){ return 'ERR'; } })(),
    plaque: {y: Math.round(pr.y), bottom: Math.round(pr.bottom), h: Math.round(pr.height)},
    switchRect: swr ? {y: Math.round(swr.y), bottom: Math.round(swr.bottom),
      insidePlaque: swr.bottom <= pr.bottom + 1} : null,
    leaves: leaves, overlaps: overlaps };
}"""

JS_BRIDGE = """() => {
  const q = s => document.querySelector(s);
  const vis = el => !!el && !el.hidden && el.getBoundingClientRect().height > 0 &&
    getComputedStyle(el).display !== 'none';
  return { url: location.href,
    bridgeVisible: vis(q('#fpBridge')),
    groups: Object.fromEntries(['#fpBridgeG1','#fpBridgeG2','#fpBridgeG3','#fpBridgeG4','#fpBridgeFinal'].map(s => [s, vis(q(s))])),
    agreedVisible: vis(q('#fpBridgeAgreed')), onwardVisible: vis(q('#fpBridgeToName')),
    lsStage: (() => { try { return localStorage.getItem('nayanet_fp_stage'); } catch(e){ return 'ERR'; } })(),
    lsAgreed: (() => { try { return localStorage.getItem('nayanet_fp_agreed'); } catch(e){ return 'ERR'; } })(),
  };
}"""

KEYS_SET = """() => { localStorage.setItem('nayanet_fp_stage','bridge-agreed');
  localStorage.setItem('nayanet_fp_agreed','1');
  return {stage: localStorage.getItem('nayanet_fp_stage'),
          agreed: localStorage.getItem('nayanet_fp_agreed')}; }"""

READ_KEYS = """() => ({stage: localStorage.getItem('nayanet_fp_stage'),
  agreed: localStorage.getItem('nayanet_fp_agreed')})"""


def claim(p, alias, ident_url):
    p.goto(ident_url, wait_until="load", timeout=60000)
    p.wait_for_timeout(2000)
    p.fill("#aliasInput", alias)
    p.wait_for_timeout(2500)
    ent = p.query_selector("button:has-text('ENTER')")
    assert ent, "ENTER missing"
    ent.click()
    p.wait_for_timeout(5000)
    return p.evaluate(JS_CERT)


def main():
    import sys
    ident_cb = sys.argv[1] if len(sys.argv) > 1 else "PLACEHOLDER"
    ident_url = IDENT_C.replace("PLACEHOLDER", ident_cb)
    with sync_playwright() as pw:
        b = pw.firefox.launch(headless=True)
        try:
            # --- A. certified 1920 (the goes-back width) ---
            ctx = b.new_context(viewport={"width": 1920, "height": 999})
            ctx.grant_permissions(["clipboard-read", "clipboard-write"])
            p = ctx.new_page()
            p.route("**/welcome*", lambda route: route.abort())
            OUT["A_certified_1920"] = claim(p, "fix4cert", ident_url)
            p.screenshot(path=os.path.join(EV, "fix4-live-A-cert-1920.png"))
            ctx.close()

            # --- B. certified 534 (the fix3c width must stay clean) ---
            ctx = b.new_context(viewport={"width": 534, "height": 900})
            ctx.grant_permissions(["clipboard-read", "clipboard-write"])
            p = ctx.new_page()
            p.route("**/welcome*", lambda route: route.abort())
            OUT["B_certified_534"] = claim(p, "fix4cert534", ident_url)
            p.screenshot(path=os.path.join(EV, "fix4-live-B-cert-534.png"))
            ctx.close()

            # --- C. follow-on #1 re-probe: deck/letter arrival, keys set fresh
            # in the SAME context (checker's probe-B). Control first: keys set
            # on plain /, read back without navigating away. ---
            ctx = b.new_context(viewport={"width": 1920, "height": 999})
            p = ctx.new_page()
            p.goto(STAGING + "/", wait_until="load", timeout=60000)
            p.wait_for_timeout(1500)
            OUT["C_control_set"] = p.evaluate(KEYS_SET)
            p.wait_for_timeout(500)
            OUT["C_control_read"] = p.evaluate(READ_KEYS)
            # deck arrival with keys fresh
            p.evaluate(KEYS_SET)
            p.goto(STAGING + "/?stage=deck", wait_until="load", timeout=60000)
            p.wait_for_timeout(1500)
            OUT["C_deck_arrival"] = p.evaluate(JS_BRIDGE)
            p.screenshot(path=os.path.join(EV, "fix4-live-C-deck-1920.png"))
            # letter arrival with keys fresh again
            p.goto(STAGING + "/", wait_until="load", timeout=60000)
            p.wait_for_timeout(1000)
            p.evaluate(KEYS_SET)
            p.goto(STAGING + "/?stage=letter", wait_until="load", timeout=60000)
            p.wait_for_timeout(1500)
            OUT["C_letter_arrival"] = p.evaluate(JS_BRIDGE)
            p.screenshot(path=os.path.join(EV, "fix4-live-C-letter-1920.png"))
            # plain reload with keys fresh: the agreed state must survive
            p.goto(STAGING + "/", wait_until="load", timeout=60000)
            p.wait_for_timeout(1000)
            p.evaluate(KEYS_SET)
            p.reload(wait_until="load", timeout=60000)
            p.wait_for_timeout(1500)
            OUT["C_plain_reload"] = p.evaluate(JS_BRIDGE)
            ctx.close()
        finally:
            b.close()
        with open(os.path.join(EV, "fix4-live.json"), "w") as f:
            json.dump(OUT, f, indent=1)
        print("WROTE fix4-live.json")


try:
    main()
except Exception:
    traceback.print_exc()
    with open(os.path.join(EV, "fix4-live.json"), "w") as f:
        json.dump(OUT, f, indent=1)
    print("WROTE PARTIAL fix4-live.json")
