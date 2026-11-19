#!/usr/bin/env python3
"""FIX3 live verification — walks the FIX3 staged bytes in Playwright Firefox.
Writes JSON + screenshots to evidence/. Registry: one fresh claim alias
(fix3livecheck) is created on purpose; do NOT delete rows (cleanup owed).
"""
import json, os, traceback
from playwright.sync_api import sync_playwright

HOME = os.path.expanduser("~")
EV = os.path.join(HOME, "workspace/team-nitro/walkthrough-chain-fix3-20261119/evidence")
STAGING = "https://naya-walk-beginning-staging.nayapower.workers.dev"
PROOF = "https://naya-proof-host.nayapower.workers.dev"
IDENT = (PROOF + "/?file=team-nitro/walk-v23-assembly-20261114/identity-fixed.html"
         "&ref=walkthrough/chain-fix3-20261119&cb=63217489bd0e31662f1a516177da4f52ac2dd6c4&t=1795054391")
OUT = {}

JS_BRIDGE = """() => {
  const q = s => document.querySelector(s);
  const vis = el => !!el && !el.hidden && el.getBoundingClientRect().height > 0 &&
    getComputedStyle(el).display !== 'none';
  const st = window.__fpStage ? window.__fpStage.state : null;
  const kids = [...document.querySelectorAll('#fpLegal .fp-legal-link')].map(el => {
    const r = el.getBoundingClientRect();
    return {t: el.textContent.trim(), w: Math.round(r.width*10)/10, h: Math.round(r.height*10)/10};
  });
  return { url: location.href, view: st ? st.view : null,
    bridgeVisible: vis(q('#fpBridge')),
    groups: Object.fromEntries(['#fpBridgeG1','#fpBridgeG2','#fpBridgeG3','#fpBridgeG4','#fpBridgeFinal'].map(s => [s, vis(q(s))])),
    more: Object.fromEntries(['#fpBridgeMore1','#fpBridgeMore2','#fpBridgeMore3','#fpBridgeMore4'].map(s => [s, vis(q(s))])),
    agreedVisible: vis(q('#fpBridgeAgreed')), onwardVisible: vis(q('#fpBridgeToName')),
    onwardText: q('#fpBridgeToName') ? q('#fpBridgeToName').textContent.trim() : null,
    lsStage: (() => { try { return localStorage.getItem('nayanet_fp_stage'); } catch(e){ return 'ERR'; } })(),
    lsAgreed: (() => { try { return localStorage.getItem('nayanet_fp_agreed'); } catch(e){ return 'ERR'; } })(),
    legalH: q('#fpLegal') ? Math.round(q('#fpLegal').getBoundingClientRect().height) : null,
    linkKids: kids,
    voices: (() => { try { return (window.speechSynthesis ? window.speechSynthesis.getVoices().length : -1); } catch(e){ return -2; } })(),
  };
}"""
JS_ENTRANCE = """() => {
  const q = s => document.querySelector(s);
  const vis = el => !!el && !el.hidden && el.getBoundingClientRect().height > 0 &&
    getComputedStyle(el).display !== 'none';
  const name = q('#userName');
  const jump = q('#jumpBackIn');
  const jr = jump ? jump.getBoundingClientRect() : null;
  const heading = [...document.querySelectorAll('h1,h2')].map(h => {
    const r = h.getBoundingClientRect();
    return {t: (h.textContent||'').trim().slice(0,50), x: Math.round(r.x), y: Math.round(r.y),
            w: Math.round(r.width), h: Math.round(r.height)}; });
  const portal = q('.portal') ? q('.portal').getBoundingClientRect().toJSON() : null;
  return { url: location.href, stageOn: document.body.classList.contains('fp-stage-on'),
    userNameVisible: vis(name), userNameFocused: document.activeElement === name,
    entryFormHidden: q('#entryForm') ? q('#entryForm').hidden : null,
    returningHidden: q('#returningView') ? q('#returningView').hidden : null,
    jump: jump ? {t: jump.textContent.trim(), vis: vis(jump),
      scrollW: jump.scrollWidth, clientW: jump.clientWidth,
      truncated: jump.scrollWidth > jump.clientWidth + 1} : null,
    jumpRect: jr ? {x: Math.round(jr.x), y: Math.round(jr.y), w: Math.round(jr.width), h: Math.round(jr.height)} : null,
    headings: heading, portal: portal,
    others: [...document.querySelectorAll('.returning-other')].map(b => ({
      t: b.textContent.trim(), scrollW: b.scrollWidth, clientW: b.clientWidth,
      truncated: b.scrollWidth > b.clientWidth + 1})),
  };
}"""
JS_ID = """() => {
  const q = s => document.querySelector(s);
  const vis = el => !!el && !el.hidden && el.getBoundingClientRect().height > 0 &&
    getComputedStyle(el).display !== 'none';
  const alias = q('#aliasInput');
  const st = q('#aliasStatus');
  const hero = q('#displayName');
  const crests = [...document.querySelectorAll('.corner-crest')].map(el => {
    const r = el.getBoundingClientRect();
    return {cls: el.className, x: Math.round(r.x), y: Math.round(r.y),
            w: Math.round(r.width), h: Math.round(r.height),
            clipped: r.left < 0 || r.top < 0 || r.right > innerWidth || r.bottom > innerHeight};
  });
  return { url: location.href, vw: innerWidth, vh: innerHeight,
    aliasValue: alias ? alias.value : null,
    statusText: st ? st.textContent.trim() : null, statusState: st ? st.dataset.state : null,
    noteHidden: q('#hubNote') ? q('#hubNote').hidden : null,
    noteText: q('#hubNote') ? q('#hubNote').textContent.trim().slice(0,160) : null,
    keyPanelHidden: q('#keyPanel') ? q('#keyPanel').hidden : null,
    keyPanelVisible: vis(q('#keyPanel')),
    enterBtn: (() => { const b=[...document.querySelectorAll('button')].find(x=>/ENTER/i.test(x.textContent||'')); return b ? {t:b.textContent.trim(), cls:b.className, vis:vis(b)} : null; })(),
    heroText: hero ? hero.textContent : null, heroHidden: hero ? hero.hidden : null,
    certNo: (() => { const el=q('#certNo')||q('.cert-no'); return el ? el.textContent.trim() : null; })(),
    keyValueText: q('#keyValue') ? q('#keyValue').textContent : null,
    keyValueVisible: vis(q('#keyValue')),
    keyCopyText: q('#keyCopyBtn') ? q('#keyCopyBtn').textContent.trim() : null,
    keyCopyVisible: vis(q('#keyCopyBtn')),
    certKeyHidden: q('#certKey') ? q('#certKey').hidden : null,
    crests: crests,
    lsName: (() => { try { return localStorage.getItem('nayanet_smart_name'); } catch(e){ return 'ERR'; } })(),
    lsAlias: (() => { try { return localStorage.getItem('nayanet_smart_alias'); } catch(e){ return 'ERR'; } })(),
  };
}"""

def main():
    with sync_playwright() as pw:
        b = pw.firefox.launch(headless=True)
        try:
            # --- A. /agreement agree -> bridge, 534 ---
            ctx = b.new_context(viewport={"width": 534, "height": 900})
            p = ctx.new_page()
            p.goto(STAGING + "/agreement", wait_until="load", timeout=60000)
            p.wait_for_timeout(1500)
            for _ in range(30):
                vis = p.evaluate("() => { const el=document.querySelector('#dealAgreeBtn'); if(!el) return false; const r=el.getBoundingClientRect(); return !el.hidden && r.height>0 && r.top < innerHeight && r.bottom > 0; }")
                if vis:
                    break
                keep = p.query_selector("text=Keep reading")
                if keep:
                    try: keep.click(timeout=5000)
                    except Exception: p.evaluate("() => window.scrollBy(0, 800)")
                else:
                    p.evaluate("() => window.scrollBy(0, 800)")
                p.wait_for_timeout(600)
            p.evaluate("() => { const el=document.querySelector('#dealAgreeBtn'); if(el) el.click(); }")
            p.wait_for_timeout(3000)
            OUT["A_after_agree_534"] = p.evaluate(JS_BRIDGE)
            p.screenshot(path=os.path.join(EV, "fix3-live-A-after-agree-534.png"))
            p.reload(wait_until="load"); p.wait_for_timeout(1500)
            OUT["A_reload_534"] = p.evaluate(JS_BRIDGE)
            p.screenshot(path=os.path.join(EV, "fix3-live-A-reload-534.png"))
            # gold onward pill -> name entry, no extra click
            onward = p.evaluate("() => { const el=document.querySelector('#fpBridgeToName'); if(!el) return null; const r=el.getBoundingClientRect(); return !el.hidden && r.height>0; }")
            OUT["A_onward_visible"] = onward
            if onward:
                p.evaluate("() => document.querySelector('#fpBridgeToName').click()")
                p.wait_for_timeout(1500)
                OUT["A_after_onward"] = p.evaluate(JS_ENTRANCE)
                p.screenshot(path=os.path.join(EV, "fix3-live-A-after-onward-534.png"))
            ctx.close()

            # --- B. ?stage=deck with agreed key set must stay deck ---
            ctx = b.new_context(viewport={"width": 1920, "height": 999})
            ctx.add_init_script("() => { try { localStorage.setItem('nayanet_fp_agreed','1'); localStorage.setItem('nayanet_fp_stage','bridge-agreed'); } catch(e){} }")
            p = ctx.new_page()
            p.goto(STAGING + "/?stage=deck", wait_until="load", timeout=60000)
            p.wait_for_timeout(1500)
            OUT["B_deck_with_agreed_key"] = p.evaluate(JS_BRIDGE)
            p.screenshot(path=os.path.join(EV, "fix3-live-B-deck-1920.png"))
            # direct ?stage=bridge with agreed key -> post-agree bridge on arrival
            p.goto(STAGING + "/?stage=bridge", wait_until="load", timeout=60000)
            p.wait_for_timeout(1500)
            OUT["B_bridge_with_agreed_key"] = p.evaluate(JS_BRIDGE)
            p.screenshot(path=os.path.join(EV, "fix3-live-B-bridge-1920.png"))
            ctx.close()

            # --- C. footer bridge 390 + entrance 390 ---
            for w, h in ((390, 844), (534, 900)):
                ctx = b.new_context(viewport={"width": w, "height": h})
                p = ctx.new_page()
                p.goto(STAGING + "/?stage=bridge", wait_until="load", timeout=60000)
                p.wait_for_timeout(1500)
                OUT[f"C_bridge_footer_{w}"] = p.evaluate(JS_BRIDGE)
                p.screenshot(path=os.path.join(EV, f"fix3-live-C-bridge-{w}.png"))
                ctx.close()

            # --- D. returning view: Jump back in truncation + heading/portal, 534 ---
            ctx = b.new_context(viewport={"width": 534, "height": 900})
            ctx.add_init_script("() => { try { localStorage.setItem('nayanet_smart_alias','jordantest'); localStorage.setItem('nayanet_smart_name','Jordan Test'); } catch(e){} }")
            p = ctx.new_page()
            p.goto(STAGING + "/", wait_until="load", timeout=60000)
            p.wait_for_timeout(1500)
            OUT["D_login_returning_534"] = p.evaluate(JS_ENTRANCE)
            p.screenshot(path=os.path.join(EV, "fix3-live-D-login-534.png"))
            # audio: voices + Play click state
            p.evaluate("() => { const b=document.querySelector('#fpIntroPlay'); if(b) b.click(); }")
            p.wait_for_timeout(2000)
            OUT["D_audio"] = p.evaluate("""() => ({
              voices: (() => { try { return window.speechSynthesis ? window.speechSynthesis.getVoices().length : -1; } catch(e){ return -2; } })(),
              speaking: (() => { try { return window.speechSynthesis ? window.speechSynthesis.speaking : null; } catch(e){ return null; } })(),
              pending: (() => { try { return window.speechSynthesis ? window.speechSynthesis.pending : null; } catch(e){ return null; } })(),
            })""")
            ctx.close()

            # --- E. identity: taken alias, hero echo, claim name, copy, crests, 534 cert ---
            ctx = b.new_context(viewport={"width": 1920, "height": 999})
            p = ctx.new_page()
            p.route("**/welcome*", lambda route: route.abort())
            p.goto(IDENT, wait_until="load", timeout=60000)
            p.wait_for_timeout(2000)
            p.fill("#aliasInput", "jordantest")
            p.wait_for_timeout(1800)
            OUT["E_taken_jordantest"] = p.evaluate(JS_ID)
            p.screenshot(path=os.path.join(EV, "fix3-live-E-taken-1920.png"))
            p.fill("#aliasInput", "nova eye test")
            p.wait_for_timeout(1200)
            OUT["E_hero_echo_nova"] = p.evaluate(JS_ID)
            # fresh claim with a stale ?name= paired to another alias
            p3ctx = b.new_context(viewport={"width": 1920, "height": 999})
            p3 = p3ctx.new_page()
            p3.route("**/welcome*", lambda route: route.abort())
            p3.goto(IDENT + "&name=Jordan%20Test", wait_until="load", timeout=60000)
            p3.wait_for_timeout(2000)
            p3.fill("#aliasInput", "fix3livecheck")
            p3.wait_for_timeout(1800)
            OUT["E_available_fix3livecheck"] = p3.evaluate(JS_ID)
            ent = p3.query_selector("button:has-text('ENTER')")
            if ent: ent.click()
            p3.wait_for_timeout(4000)
            OUT["E_after_claim"] = p3.evaluate(JS_ID)
            p3.screenshot(path=os.path.join(EV, "fix3-live-E-claim-1920.png"))
            kv = p3.query_selector("#keyValue")
            OUT["E_copy_pill_found"] = bool(kv)
            if kv:
                kv.click()
                p3.wait_for_timeout(1200)
                OUT["E_copy_after_pill_tap"] = p3.evaluate(JS_ID)
                OUT["E_copy_clipboard"] = p3.evaluate("() => navigator.clipboard.readText().catch(e => 'READ-ERR:' + e.name)")
                p3.screenshot(path=os.path.join(EV, "fix3-live-E-copy-1920.png"))
            # certified at 534: overlap check via element rects
            p4ctx = b.new_context(viewport={"width": 534, "height": 900})
            p4 = p4ctx.new_page()
            p4.route("**/welcome*", lambda route: route.abort())
            p4.goto(IDENT, wait_until="load", timeout=60000)
            p4.wait_for_timeout(2000)
            OUT["E_cert_534_arrival"] = p4.evaluate(JS_ID)
            p4.screenshot(path=os.path.join(EV, "fix3-live-E-cert-534.png"))
            p3ctx.close(); p4ctx.close(); ctx.close()
        finally:
            b.close()
        with open(os.path.join(EV, "fix3-live.json"), "w") as f:
            json.dump(OUT, f, indent=1)
        print("WROTE fix3-live.json")

try:
    main()
except Exception:
    traceback.print_exc()
    with open(os.path.join(EV, "fix3-live.json"), "w") as f:
        json.dump(OUT, f, indent=1)
    print("WROTE PARTIAL fix3-live.json")
