#!/usr/bin/env python3
"""FIX6 live verification — the fresh-device hole, probed on the FIX6
staging worker at 1920.

A. FRESH-DEVICE URL ARRIVAL (the checker-proven hole): fresh context,
open /welcome?name=Jordan%20Test&alias=jordantest directly. Expect: the
walk bounces to /identity.html?name=..&alias=jordantest BEFORE the
questionnaire renders, and identity shows status "already claimed",
state taken, taken note visible, key panel visible, input filled
jordantest — with NO localStorage alias/name written by the walk (the
bounce happens before any claim; the walk ingest wrote the pair, so
lsAlias/lsName are recorded, not asserted empty — see note in the
report).
B. IDENTITY URL ARRIVAL (the bounce target, direct): fresh context,
open the proof-host identity with ?name=Jordan%20Test&alias=jordantest.
Expect the same flag + key panel on LOAD, no typing, no ENTER.
C. SERVER REFUSAL (no browser needed): POST /api/welcome/complete as
jordantest with a fresh device key, and again with the key missing.
Expect 409 {"ok":false,"error":"taken"} both times, and the stored
completion record (GET before vs after) byte-identical — no writes.
Writes evidence/fix6-live.json + screenshots. The probes create NO
registry rows and NO completion records (both refusal paths return
before any write).
"""
import json, os, sys, traceback, urllib.request, urllib.error
from playwright.sync_api import sync_playwright

HOME = os.path.expanduser("~")
EV = os.path.join(HOME, "workspace/team-nitro/walkthrough-chain-fix6-20261119/evidence")
STAGING = "https://naya-walk-beginning-staging.nayapower.workers.dev"
PROOF = "https://naya-proof-host.nayapower.workers.dev"
IDENT_C = (PROOF + "/?file=team-nitro/walk-v23-assembly-20261114/identity-fixed.html"
           "&ref=walkthrough/chain-fix6-20261119&cb=PLACEHOLDER&t=1795076000")
WALK_URL = STAGING + "/welcome?name=Jordan%20Test&alias=jordantest"
OUT = {}

JS_IDENT = """() => {
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
    plaqueCertified: (q('.cert-plaque') || {classList:{contains:()=>false}}).classList.contains('is-certified'),
    lsAlias: (() => { try { return localStorage.getItem('nayanet_smart_alias'); } catch(e){ return 'ERR'; } })(),
    lsName: (() => { try { return localStorage.getItem('nayanet_smart_name'); } catch(e){ return 'ERR'; } })(),
    lsKey: (() => { try { return !!localStorage.getItem('nayanet_vault_key'); } catch(e){ return 'ERR'; } })(),
  };
}"""


def api(method, path, body=None):
    req = urllib.request.Request(STAGING + path,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Content-Type": "application/json"},
                                 method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def section_c():
    before_status, before = api("GET", "/api/welcome/complete?alias=jordantest")
    OUT["C_complete_before"] = {"status": before_status, "bytes": len(before),
                                "sha": __import__("hashlib").sha256(before).hexdigest()[:12]}
    for tag, key in (("C_complete_fresh_key", "nayanet_key_fix6probe_freshdevice"),
                     ("C_complete_missing_key", None)):
        body = {"alias": "jordantest", "name": "Jordan Test",
                "answers": {}, "topics": [], "pageNames": {}}
        if key is not None:
            body["device_key"] = key
        status, raw = api("POST", "/api/welcome/complete", body)
        OUT[tag] = {"status": status, "body": raw.decode("utf-8", "replace")[:200]}
    after_status, after = api("GET", "/api/welcome/complete?alias=jordantest")
    OUT["C_complete_after"] = {"status": after_status, "bytes": len(after),
                               "sha": __import__("hashlib").sha256(after).hexdigest()[:12]}
    OUT["C_no_write"] = (before_status == after_status and before == after)


def main():
    ident_cb = sys.argv[1] if len(sys.argv) > 1 else "PLACEHOLDER"
    walk_cb = sys.argv[2] if len(sys.argv) > 2 else "PLACEHOLDER"
    ident_url = IDENT_C.replace("PLACEHOLDER", ident_cb)
    with sync_playwright() as pw:
        b = pw.firefox.launch(headless=True)
        try:
            # --- A. fresh-device walk URL arrival -> bounce to identity ---
            ctx = b.new_context(viewport={"width": 1920, "height": 999})
            p = ctx.new_page()
            p.goto(WALK_URL, wait_until="load", timeout=60000)
            p.wait_for_timeout(6000)
            OUT["A_walk_url_arrival"] = p.evaluate(JS_IDENT)
            p.screenshot(path=os.path.join(EV, "fix6-live-A-bounce-1920.png"))
            ctx.close()
            # --- B. identity URL arrival, direct ---
            ctx = b.new_context(viewport={"width": 1920, "height": 999})
            p = ctx.new_page()
            p.goto(ident_url + "&name=Jordan%20Test&alias=jordantest",
                   wait_until="load", timeout=60000)
            p.wait_for_timeout(5000)
            OUT["B_identity_url_arrival"] = p.evaluate(JS_IDENT)
            p.screenshot(path=os.path.join(EV, "fix6-live-B-identity-1920.png"))
            ctx.close()
        finally:
            b.close()
        section_c()
        with open(os.path.join(EV, "fix6-live.json"), "w") as f:
            json.dump(OUT, f, indent=1)
        print("WROTE fix6-live.json")


try:
    main()
except Exception:
    traceback.print_exc()
    try:
        with open(os.path.join(EV, "fix6-live.json"), "w") as f:
            json.dump(OUT, f, indent=1)
        print("WROTE PARTIAL fix6-live.json")
    except Exception:
        print("COULD NOT WRITE fix6-live.json (EPERM?)")
