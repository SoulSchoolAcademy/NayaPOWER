#!/usr/bin/env python3
"""FIX5 live verification — the taken-alias ENTER probe at 1920 on the FIX5
identity, plus an available-alias control and the follow-on #1 re-probe.

A. TAKEN, FAST ENTER (the captain's eye path): fresh context, type
jordantest, click ENTER immediately (no wait — the race the FIX5 gate
closes). Expect: NO navigation to /welcome, status "already claimed",
state taken, taken note visible, key panel visible, ENTER dim, and NO
localStorage alias/name written (the gate returns before any write).
B. TAKEN, SLOW ENTER (typing check resolves first): same expectations.
C. AVAILABLE control: fresh context, claim fix5avail — ENTER must stamp
a certificate and head to /welcome (route aborted; cert state recorded).
D. Follow-on #1 re-probe: deck/letter arrival with keys set fresh in
the same context (the checker's probe-B, still owed from fix4).
Writes evidence/fix5-live.json + screenshots. The taken probes create
NO registry rows (the gate returns before the claim POST). The control
claim creates ONE row (fix5avail) — do NOT delete rows (registry cleanup
owed separately).
"""
import json, os, sys, traceback
from playwright.sync_api import sync_playwright

HOME = os.path.expanduser("~")
EV = os.path.join(HOME, "workspace/team-nitro/walkthrough-chain-fix5-20261119/evidence")
STAGING = "https://naya-walk-beginning-staging.nayapower.workers.dev"
PROOF = "https://naya-proof-host.nayapower.workers.dev"
IDENT_C = (PROOF + "/?file=team-nitro/walk-v23-assembly-20261114/identity-fixed.html"
           "&ref=walkthrough/chain-fix5-20261119&cb=PLACEHOLDER&t=1795075000")
OUT = {}

JS_TAKEN = """() => {
  const q = s => document.querySelector(s);
  const vis = el => !!el && !el.hidden && el.getBoundingClientRect().height > 0 &&
    getComputedStyle(el).display !== 'none';
  const st = q('#aliasStatus');
  const ent = q('#enterBtn') || [...document.querySelectorAll('button')].find(b => (b.textContent || '').trim() === 'ENTER');
  return { url: location.href,
    aliasValue: q('#aliasInput') ? q('#aliasInput').value : null,
    statusText: st ? st.textContent.trim() : null,
    statusState: st ? st.getAttribute('data-state') : null,
    noteHidden: q('#hubNote') ? q('#hubNote').hidden : null,
    noteText: q('#hubNote') ? q('#hubNote').textContent.trim() : null,
    keyPanelHidden: q('#keyPanel') ? q('#keyPanel').hidden : null,
    keyPanelVisible: vis(q('#keyPanel')),
    enterDim: ent ? ent.classList.contains('dim') : null,
    enterArmed: ent ? ent.classList.contains('armed') : null,
    plaqueCertified: (q('.cert-plaque') || {classList:{contains:()=>false}}).classList.contains('is-certified'),
    lsAlias: (() => { try { return localStorage.getItem('nayanet_smart_alias'); } catch(e){ return 'ERR'; } })(),
    lsName: (() => { try { return localStorage.getItem('nayanet_smart_name'); } catch(e){ return 'ERR'; } })(),
    lsKey: (() => { try { return !!localStorage.getItem('nayanet_vault_key'); } catch(e){ return 'ERR'; } })(),
  };
}"""

JS_CERT = """() => {
  const q = s => document.querySelector(s);
  return { url: location.href,
    certNo: q('#certNoValue') ? q('#certNoValue').textContent.trim() : null,
    heroText: q('#displayName') ? q('#displayName').textContent : null,
    plaqueCertified: q('.cert-plaque') ? q('.cert-plaque').classList.contains('is-certified') : null,
    lsAlias: (() => { try { return localStorage.getItem('nayanet_smart_alias'); } catch(e){ return 'ERR'; } })(),
  };
}"""

JS_BRIDGE = """() => {
  const q = s => document.querySelector(s);
  const vis = el => !!el && !el.hidden && el.getBoundingClientRect().height > 0 &&
    getComputedStyle(el).display !== 'none';
  return { url: location.href,
    bridgeVisible: vis(q('#fpBridge')),
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


def taken_probe(p, ident_url, wait_ms, tag):
    p.goto(ident_url, wait_until="load", timeout=60000)
    p.wait_for_timeout(2000)
    p.fill("#aliasInput", "jordantest")
    if wait_ms:
        p.wait_for_timeout(wait_ms)
    ent = p.query_selector("button:has-text('ENTER')")
    assert ent, "ENTER missing"
    ent.click()
    p.wait_for_timeout(4000)
    OUT[tag] = p.evaluate(JS_TAKEN)
    p.screenshot(path=os.path.join(EV, "fix5-live-%s.png" % tag))


def main():
    ident_cb = sys.argv[1] if len(sys.argv) > 1 else "PLACEHOLDER"
    ident_url = IDENT_C.replace("PLACEHOLDER", ident_cb)
    with sync_playwright() as pw:
        b = pw.firefox.launch(headless=True)
        try:
            # --- A. taken, FAST ENTER (the race) ---
            ctx = b.new_context(viewport={"width": 1920, "height": 999})
            p = ctx.new_page()
            taken_probe(p, ident_url, 0, "A_taken_fast_enter")
            ctx.close()
            # --- B. taken, SLOW ENTER (check resolves first) ---
            ctx = b.new_context(viewport={"width": 1920, "height": 999})
            p = ctx.new_page()
            taken_probe(p, ident_url, 2500, "B_taken_slow_enter")
            ctx.close()
            # --- C. available control: claim fix5avail ---
            ctx = b.new_context(viewport={"width": 1920, "height": 999})
            p = ctx.new_page()
            p.route("**/welcome*", lambda route: route.abort())
            p.goto(ident_url, wait_until="load", timeout=60000)
            p.wait_for_timeout(2000)
            p.fill("#aliasInput", "fix5avail")
            p.wait_for_timeout(2500)
            ent = p.query_selector("button:has-text('ENTER')")
            assert ent, "ENTER missing"
            ent.click()
            p.wait_for_timeout(5000)
            OUT["C_available_claim"] = p.evaluate(JS_CERT)
            p.screenshot(path=os.path.join(EV, "fix5-live-C-available.png"))
            ctx.close()
            # --- D. follow-on #1 re-probe ---
            ctx = b.new_context(viewport={"width": 1920, "height": 999})
            p = ctx.new_page()
            p.goto(STAGING + "/", wait_until="load", timeout=60000)
            p.wait_for_timeout(1500)
            OUT["D_control_set"] = p.evaluate(KEYS_SET)
            p.wait_for_timeout(500)
            OUT["D_control_read"] = p.evaluate(READ_KEYS)
            p.evaluate(KEYS_SET)
            p.goto(STAGING + "/?stage=deck", wait_until="load", timeout=60000)
            p.wait_for_timeout(1500)
            OUT["D_deck_arrival"] = p.evaluate(JS_BRIDGE)
            p.screenshot(path=os.path.join(EV, "fix5-live-D-deck-1920.png"))
            p.goto(STAGING + "/", wait_until="load", timeout=60000)
            p.wait_for_timeout(1000)
            p.evaluate(KEYS_SET)
            p.goto(STAGING + "/?stage=letter", wait_until="load", timeout=60000)
            p.wait_for_timeout(1500)
            OUT["D_letter_arrival"] = p.evaluate(JS_BRIDGE)
            p.screenshot(path=os.path.join(EV, "fix5-live-D-letter-1920.png"))
            p.goto(STAGING + "/", wait_until="load", timeout=60000)
            p.wait_for_timeout(1000)
            p.evaluate(KEYS_SET)
            p.reload(wait_until="load", timeout=60000)
            p.wait_for_timeout(1500)
            OUT["D_plain_reload"] = p.evaluate(JS_BRIDGE)
            ctx.close()
        finally:
            b.close()
        with open(os.path.join(EV, "fix5-live.json"), "w") as f:
            json.dump(OUT, f, indent=1)
        print("WROTE fix5-live.json")


try:
    main()
except Exception:
    traceback.print_exc()
    try:
        with open(os.path.join(EV, "fix5-live.json"), "w") as f:
            json.dump(OUT, f, indent=1)
        print("WROTE PARTIAL fix5-live.json")
    except Exception:
        print("COULD NOT WRITE fix5-live.json (EPERM?)")
