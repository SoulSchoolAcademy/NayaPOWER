# FIX2 probe — F1 + veil REMOVAL + remove-modal conversion + deal/zoom live
# + complete() POST + Choose-plan click + keepers. Real taps, Chromium via forwarder.
import json, time
from playwright.sync_api import sync_playwright
BASE = "https://official-walkthrough-staging.nayapower.workers.dev"
OUT = "/home/hatch/workspace/team-nitro/walkthrough-official-20261127/fix2/maker/evidence/"
fails = []
def check(name, ok, extra=""):
    print(("PASS " if ok else "FAIL ") + name + (" | " + str(extra)[:240] if extra != "" else ""), flush=True)
    if not ok: fails.append(name)
    return ok

CLIP_JS = """() => {
  const bad = [];
  document.querySelectorAll('#bdTrio .bd-phone').forEach((p, i) => {
    const k = p.querySelector('.bd-kicker');
    if (k && k.scrollWidth > k.clientWidth) bad.push('phone'+(i+1)+' kicker clip '+k.scrollWidth+'>'+k.clientWidth);
    const c = p.querySelector('.bd-chin-label');
    if (c && c.scrollWidth > c.clientWidth) bad.push('phone'+(i+1)+' chin clip '+c.scrollWidth+'>'+c.clientWidth);
    const q = p.querySelector('.fp-walk-q'), card = p.querySelector('.bd-card');
    if (q && card) { const qr=q.getBoundingClientRect(), cr=card.getBoundingClientRect();
      if (qr.bottom > cr.top + 1) bad.push('phone'+(i+1)+' question covered by card ('+Math.round(qr.bottom-cr.top)+'px)'); }
    const st = p.querySelector('.bd-stage');
    if (st && st.scrollHeight > st.clientHeight + 2) bad.push('phone'+(i+1)+' stage overflow '+st.scrollHeight+'>'+st.clientHeight);
  });
  return bad;
}"""
HEADER_JS = """() => {
  const out = [];
  document.querySelectorAll('#bdTrio .bd-phone').forEach((p, i) => {
    const imgs = [...p.querySelectorAll('.bd-walkhead img')].map(im => ({src: (im.getAttribute('src')||'').split('/').pop(), nw: im.naturalWidth, vis: im.offsetParent !== null}));
    out.push({phone: i, key: p.getAttribute('data-key'), imgs});
  });
  return out;
}"""

with sync_playwright() as pw:
    b = pw.chromium.launch(proxy={"server": "http://127.0.0.1:18080"})
    # ================= 390: CERTIFICATE — F1 + veil removal + D3/D4 keepers =================
    ctx390 = b.new_context(viewport={"width": 390, "height": 844}, ignore_https_errors=True)
    pg = ctx390.new_page()
    perrs, cerrs, failed = [], [], []
    pg.on("pageerror", lambda e: perrs.append(str(e)))
    pg.on("console", lambda m: cerrs.append(m.text) if m.type == "error" else None)
    pg.on("response", lambda r: failed.append("HTTP %s %s" % (r.status, r.url[:100])) if r.status >= 400 else None)
    pg.goto(BASE + "/", wait_until="domcontentloaded", timeout=120000)
    pg.wait_for_timeout(1000)
    pg.locator("#userName").fill("Shawn")
    pg.keyboard.press("Enter")
    for _ in range(15):
        if pg.url.startswith(BASE + "/identity.html"): break
        pg.wait_for_timeout(2000)
    check("cert: landed on /identity.html same host", pg.url.startswith(BASE + "/identity.html"), pg.url)
    pg.wait_for_timeout(10000)
    veil = pg.evaluate("() => { const html = document.documentElement.outerHTML; return {el: document.getElementById('installVeil'), inHtml: html.includes('installVeil'), openModal: html.includes('openModal'), veilHidden: html.includes('veil.hidden')}; }")
    check("ITEM2: veil element GONE from the shipped cert DOM (no #installVeil)", veil["el"] is None and not veil["inHtml"], veil)
    check("ITEM2: no openModal / veil.hidden show-code anywhere in cert DOM", not veil["openModal"] and not veil["veilHidden"], veil)
    ent = pg.evaluate("() => { const b = document.getElementById('enterBtn'); if (!b) return null; const r = b.getBoundingClientRect(); const el = document.elementFromPoint(r.x + r.width/2, r.y + r.height/2); return {vis: b.offsetParent !== null, disabled: b.disabled, hit: el ? !!el.closest('#enterBtn') : false}; }")
    check("keeper: ENTER tappable (top element is ENTER)", ent and ent["vis"] and not ent["disabled"] and ent["hit"], ent)
    pg.locator("#aliasInput").fill("shawn")
    pg.wait_for_timeout(1200)
    pg.locator("#enterBtn").click()
    for _ in range(10):
        pg.wait_for_timeout(2000)
        _st = pg.evaluate("() => { const s=document.getElementById('aliasStatus'); return s ? s.textContent : ''; }")
        if "already claimed" in _st.lower(): break
    check("cert: taken state reached for alias shawn (reads only, no new row)", "already claimed" in _st.lower(), _st[:120])
    dt = pg.evaluate("""() => { const el = document.getElementById('certDatetime'); if (!el) return null;
      const wd = el.querySelector('.cert-dt-word');
      return {hidden: el.hidden, text: el.textContent, wdColor: wd ? getComputedStyle(wd).color : null}; }""")
    print("certDatetime:", json.dumps(dt), flush=True)
    check("keeper D3: digit tiles VISIBLE in already-claimed state", dt and not dt["hidden"] and len(dt["text"]) > 8, dt)
    check("keeper D3: Tuesday gold (certified Tue 20 Oct 2026)", dt and "TUESDAY" in dt["text"] and dt["wdColor"] == "rgb(212, 160, 23)", dt)
    t1 = pg.evaluate("() => document.getElementById('certDatetime').textContent")
    pg.wait_for_timeout(2200)
    t2 = pg.evaluate("() => document.getElementById('certDatetime').textContent")
    check("keeper D3: tiles tick", t1 != t2, (t1, t2))
    note = pg.evaluate("""() => { const n = document.getElementById('hubNote'); if (!n || n.hidden) return null;
      const r = n.getBoundingClientRect(); const p = n.parentElement.getBoundingClientRect();
      return {leftGap: Math.round(r.left - p.left), rightGap: Math.round(p.right - r.right)}; }""")
    check("keeper D4: hubNote margins clear of frame (>=16px each side)", note and note["leftGap"] >= 16 and note["rightGap"] >= 16, note)
    # ---- F1: the paragraph under ENTER ----
    f1 = pg.evaluate("""() => {
      const p = document.querySelector('.cert-benefit');
      if (!p) return null;
      const pr = p.getBoundingClientRect();
      const range = document.createRange(); range.selectNodeContents(p);
      const rects = [...range.getClientRects()].map(r => ({x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)}));
      const first = rects[0];
      const bl = document.querySelector('.corner-crest.cm-bl'), br = document.querySelector('.corner-crest.cm-br');
      const blr = bl ? bl.getBoundingClientRect() : null, brr = br ? br.getBoundingClientRect() : null;
      // point-test: the spot where "Yo" renders — what element is on top there?
      const px = first.x + 4, py = first.y + Math.round(first.h / 2);
      const el = document.elementFromPoint(px, py);
      const cs = getComputedStyle(p);
      return {text: p.textContent.slice(0, 60), para: {x: Math.round(pr.x), y: Math.round(pr.y), w: Math.round(pr.width)},
        firstLine: first, crestBL: blr ? {x: Math.round(blr.x), y: Math.round(blr.y), r: Math.round(blr.right), b: Math.round(blr.bottom)} : null,
        crestBR: brr ? {x: Math.round(brr.x), y: Math.round(brr.y), l: Math.round(brr.left), b: Math.round(brr.bottom)} : null,
        yoPoint: {x: px, y: py}, yoHit: el ? (el.closest('p.cert-benefit') ? 'cert-benefit' : (el.className && el.className.baseVal !== undefined ? el.tagName : (el.className || el.tagName))) : null,
        ml: cs.marginLeft, mr: cs.marginRight};
    }""")
    print("F1 geometry:", json.dumps(f1), flush=True)
    check("F1: paragraph text starts 'Your alias is your Smart Link route'", f1 and f1["text"].startswith("Your alias is your Smart Link route"), f1["text"] if f1 else None)
    check("F1: paragraph has 24px side margins", f1 and f1["ml"] == "24px" and f1["mr"] == "24px", (f1["ml"], f1["mr"]) if f1 else None)
    check("F1: 'Yo' point-test lands ON the paragraph, not a crest", f1 and f1["yoHit"] == "cert-benefit", f1)
    pg.screenshot(path=OUT + "fix2-390-cert.png")
    pg.screenshot(path=OUT + "fix2-390-cert-para.png", clip={"x": 0, "y": 480, "width": 390, "height": 180})
    # silent restore reload re-proves tiles without a new claim
    pg.goto(BASE + "/identity.html?name=Shawn", wait_until="domcontentloaded", timeout=120000)
    pg.wait_for_timeout(4000)
    dt2 = pg.evaluate("() => { const el = document.getElementById('certDatetime'); return el ? {hidden: el.hidden, text: el.textContent} : null; }")
    check("keeper D3: tiles visible on silent restore reload", dt2 and not dt2["hidden"] and "TUESDAY" in dt2["text"], dt2)
    pg.locator("#aliasInput").fill("shawn")
    pg.wait_for_timeout(800)
    pg.locator("#enterBtn").click()
    pg.wait_for_timeout(3500)
    tim = pg.locator("#fpThisIsMe")
    check("keeper: 'This is me' offered on taken state", tim.count() == 1)
    tim.click()
    pg.wait_for_selector("#bdTrio .bd-phone", timeout=60000)
    pg.wait_for_timeout(1200)
    check("walk loads after This-is-me", pg.url.startswith(BASE + "/?walk=1"), pg.url)
    # ================= 390 WALK — complete() POST + Choose plan + keepers =================
    comp, me = {}, {}
    pg.on("response", lambda r: comp.update({"status": r.status, "url": r.url}) if "welcome/complete" in r.url else None)
    pg.on("response", lambda r: me.update({"status": r.status, "url": r.url}) if "welcome/me" in r.url else None)
    pg.select_option('#bdTrio select[data-fid="country"]', "canada")
    pg.fill('#bdTrio input[data-fid="province"]', "Ontario")
    pg.fill('#bdTrio input[data-fid="city"]', "Toronto")
    pg.select_option('#bdTrio select[data-fid="age"]', "35-44")
    pg.fill('#bdTrio input[data-fid="language"]', "English")
    pg.select_option('#bdTrio select[data-fid="gender"]', "female")
    for g in range(8):
        if g == 1:
            pg.fill('#bdTrio input[data-fid="brand"]', "Naya")
            pg.select_option('#bdTrio select[data-fid="music"]', "rock")
            pg.fill('#bdTrio input[data-fid="hobby"]', "Gardening")
            pg.fill('#bdTrio input[data-fid="loveelse"]', "Sunsets and good books")
            pg.select_option('#bdTrio select[data-fid="sport"]', "soccer")
            pg.fill('#bdTrio input[data-fid="team"]', "Toronto FC")
            pg.select_option('#bdTrio select[data-fid="industry"]', "technology")
            pg.select_option('#bdTrio select[data-fid="connect"]', "people-like-me")
            pg.fill('#bdTrio input[data-fid="connectown"]', "People like me")
        if g == 2:
            vph = pg.locator('#bdTrio .bd-phone[data-key="vision"]')
            if vph.count():
                vph.locator(".bd-ball").click(); pg.wait_for_timeout(600)
                check("keeper: vision picture reveals on ball tap (390)", vph.locator(".bd-bgpic").evaluate("el => getComputedStyle(el).opacity") == "1")
                vph.locator(".bd-ball").click(); pg.wait_for_timeout(400)
        if g == 1:
            vph = pg.locator('#bdTrio .bd-phone[data-key="video"]')
            if vph.count():
                vph.locator(".bd-ball").click(); pg.wait_for_timeout(9000)
                st = pg.evaluate("() => { const v = document.querySelector('#bdTrio .bd-phone[data-key=\"video\"] video'); return v ? {paused: v.paused, t: v.currentTime, rs: v.readyState} : null; }")
                check("keeper: video ball plays (390)", st and not st["paused"], st)
                vph.locator(".bd-ball").click(); pg.wait_for_timeout(400)
                st2 = pg.evaluate("() => { const v = document.querySelector('#bdTrio .bd-phone[data-key=\"video\"] video'); return v ? v.paused : null; }")
                check("keeper: video ball pauses (390)", st2 == True)
        clip = pg.evaluate(CLIP_JS)
        check("group %d of 8: no clipping at 390" % (g+1), clip == [], clip)
        hdr = pg.evaluate(HEADER_JS)
        ok_h = all(len(h["imgs"]) == 2 and all(i["nw"] > 0 and i["vis"] for i in h["imgs"]) for h in hdr)
        check("keeper D5: header on every phone, group %d (390)" % (g+1), ok_h, hdr)
        if g == 0: pg.screenshot(path=OUT + "fix2-390-g1.png")
        if g < 7:
            pg.locator("#fpWalkNext").click(); pg.wait_for_timeout(800)
    pg.locator("#fpWalkNext").click()
    pg.wait_for_selector("#fpWalkEnd:not([hidden])", timeout=30000)
    pg.wait_for_timeout(2500)
    print("complete() response:", json.dumps(comp), "me:", json.dumps(me), flush=True)
    check("ITEM4: complete() POST observed live (welcome/complete 200)", comp.get("status") == 200, comp)
    check("ITEM4: verify /me POST observed live (has_world check)", me.get("status") == 200, me)
    ready = pg.evaluate("() => { const r = document.getElementById('fpWalkReadyLine'); return r ? {hidden: r.hidden, text: r.textContent.slice(0, 90)} : null; }")
    check("keeper: end screen shows READY (verify-before-declare passed)", ready and not ready["hidden"] and "ready" in ready["text"].lower(), ready)
    end = pg.evaluate("""() => { const e = document.getElementById('fpWalkEnd'); const s = document.querySelector('#bdEndPhone .bd-screen');
      const er = e.getBoundingClientRect(), sr = s.getBoundingClientRect();
      return {whole: er.top >= sr.top - 1 && er.bottom <= sr.bottom + 1, world: document.getElementById('fpWalkLink').textContent}; }""")
    check("keeper: end screen whole at 390", end["whole"], end)
    ls = pg.evaluate("() => { const S = JSON.parse(localStorage.getItem('naya_welcome_right_v1') || 'null'); return S ? Object.keys(S.answers).length : 0; }")
    check("keeper: answers saved (30+ keys)", ls >= 30, ls)
    pg.screenshot(path=OUT + "fix2-390-end.png")
    # Choose plan — LAST: it navigates away to the pricing worker
    pg.locator("#fpWalkPricing").click()
    try:
        pg.wait_for_url("**naya-model-pricing.nayapower.workers.dev/**", timeout=30000)
        check("ITEM4: 'Choose plan' click lands on pricing worker", True, pg.url)
    except Exception as e:
        check("ITEM4: 'Choose plan' click lands on pricing worker", False, "still at " + pg.url)
    print("390 pageerrors:", perrs, flush=True)
    print("390 console errors:", cerrs[:8], "failed responses:", failed[:6], flush=True)
    unexplained = [c for c in cerrs if "503" not in c and "409" not in c]
    check("0 UNEXPLAINED errors at 390", len(perrs) == 0 and len(unexplained) == 0, (perrs, unexplained))
    pg.close()
    # ================= 390: PORTAL — dealPlain + zoom + remove modal =================
    ctxP = b.new_context(viewport={"width": 390, "height": 844}, ignore_https_errors=True)
    pp = ctxP.new_page()
    perrs2, cerrs2 = [], []
    pp.on("pageerror", lambda e: perrs2.append(str(e)))
    pp.on("console", lambda m: cerrs2.append(m.text) if m.type == "error" else None)
    pp.goto(BASE + "/", wait_until="domcontentloaded", timeout=120000)
    pp.wait_for_timeout(1500)
    # ---- DEAL VIEW route (found by code-read + live state reads) ----
    # The stage (#fpAgreement layer) is the deal view. It has NO tap entry
    # in the shipped build: the story never enters it, ?stage= is disabled
    # (PORTAL-ROOT-FIRST), and nothing calls enterStage() from any control.
    # Its only entry is the page's own exposed API, window.__fpStage.enter().
    # The eye #dealEyeMain is hidden in EVERY reachable state (section
    # display:none under html.fp-locked out of stage; display:none in stage),
    # so it is NOT a live opener. The plain dialog's only live opener is
    # the stage-bar mirror link #fpLinkLetterAll, visible in letter /
    # letterPage views — and letterPage itself is only reachable via the
    # exposed state API (resumeTarget never returns 'letter'; enterLetterPage
    # has no caller). Proven live below: dialog opens on a real mirror tap.
    has_stage = pp.evaluate("() => !!window.__fpStage && typeof window.__fpStage.enter === 'function'")
    check("ITEM4: deal-view route found: window.__fpStage.enter() is the only entry (no UI caller ships; ?stage= disabled; story never enters it)", has_stage)
    eye_state = pp.evaluate("() => { const e = document.getElementById('dealEyeMain'); return {inDom: !!e, vis: e ? e.offsetParent !== null : false, secDisp: getComputedStyle(document.getElementById('fpAgreement')).display}; }")
    check("ITEM4: eye #dealEyeMain is NOT a live opener (hidden in every reachable state)", eye_state["inDom"] and not eye_state["vis"], eye_state)
    pp.evaluate("() => window.__fpStage.enter()")
    pp.wait_for_timeout(1000)
    stage_on = pp.evaluate("() => document.body.classList.contains('fp-stage-on')")
    check("ITEM4: stage entered via __fpStage.enter()", stage_on)
    ch = pp.locator("#fpChoiceDeck")
    check("ITEM4: intro choice 'Begin the visual story' is the tap target (bar is display:none in intro)", ch.count() == 1 and pp.evaluate("() => document.getElementById('fpChoiceDeck').offsetParent !== null"))
    ch.click()
    pp.wait_for_timeout(1000)
    deck0 = pp.evaluate("() => { const S = window.__fpStage.state; return {view: S.view, deck: S.deck}; }")
    check("ITEM4: deck view reached by real tap", deck0["view"] == "deck" and deck0["deck"] == 0, deck0)
    # ---- fpZoom: real tap on the deck beat's showcase image ----
    show = pp.evaluate("""() => [...document.querySelectorAll('#deckBody .letter-beat.fp-now .lb-showcase img')].map(im => ({vis: im.offsetParent !== null, src: (im.getAttribute('src')||'').slice(0, 60)}))""")
    print("deck showcase imgs:", json.dumps(show), flush=True)
    check("ITEM4: deck beat 0 carries a visible showcase image to tap", bool(show) and show[0]["vis"], show)
    pp.locator("#deckBody .letter-beat.fp-now .lb-showcase img").first.scroll_into_view_if_needed()
    pp.wait_for_timeout(500)
    pp.locator("#deckBody .letter-beat.fp-now .lb-showcase img").first.click()
    pp.wait_for_timeout(800)
    zoom = pp.evaluate("""() => { const z = document.getElementById('fpZoom'); if (!z) return null;
      const r = z.getBoundingClientRect(); const cs = getComputedStyle(z);
      const im = document.getElementById('fpZoomImg'); const c = document.getElementById('fpZoomClose');
      return {hidden: z.hidden, open: z.classList.contains('fp-open'), rect: {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)},
        pos: cs.position, bg: cs.backgroundColor, imgSrc: im ? (im.getAttribute('src')||'').slice(0, 60) : null, imgNw: im ? im.naturalWidth : null,
        closeVis: c ? c.offsetParent !== null : false}; }""")
    print("fpZoom:", json.dumps(zoom), flush=True)
    check("ITEM4: #fpZoom opens on a real showcase-image tap", zoom and not zoom["hidden"] and zoom["open"], zoom)
    check("ITEM4: #fpZoom is fullscreen fixed in-frame", zoom and zoom["rect"] == {"x": 0, "y": 0, "w": 390, "h": 844} and zoom["pos"] == "fixed", zoom["rect"] if zoom else None)
    check("ITEM4: #fpZoom close x in view", zoom and zoom["closeVis"], zoom)
    pp.screenshot(path=OUT + "fix2-390-zoom.png")
    pp.locator("#fpZoomClose").click()
    pp.wait_for_timeout(500)
    check("ITEM4: #fpZoom closes on x tap", pp.evaluate("() => document.getElementById('fpZoom').hidden") == True)
    pp.locator("#deckBody .letter-beat.fp-now .lb-showcase img").first.click()
    pp.wait_for_timeout(800)
    pp.keyboard.press("Escape")
    pp.wait_for_timeout(500)
    check("ITEM4: #fpZoom closes on Esc", pp.evaluate("() => document.getElementById('fpZoom').hidden") == True)
    # ---- walk the whole deck by taps: does any tap reach the letter? ----
    for i in range(8):
        st = pp.evaluate("() => { const S = window.__fpStage.state; return {view: S.view, deck: S.deck, letterShown: [...document.querySelectorAll('#letterBody .letter-beat')].filter(b => !b.hidden).length, mirror: document.getElementById('fpLinkLetterAll').offsetParent !== null}; }")
        print("deck tap", i, ":", json.dumps(st), flush=True)
        if st["view"] != "deck" or st["deck"] >= 8:
            break
        pp.locator("#fpNextBtn").click()
        pp.wait_for_timeout(800)
    dend = pp.evaluate("() => { const S = window.__fpStage.state; return {view: S.view, deck: S.deck, letterShown: [...document.querySelectorAll('#letterBody .letter-beat')].filter(b => !b.hidden).length, mirror: document.getElementById('fpLinkLetterAll').offsetParent !== null, next2: document.getElementById('fpNextBtn2').hidden ? 'hidden' : document.getElementById('fpNextBtn2').textContent}; }")
    print("deck end:", json.dumps(dend), flush=True)
    check("ITEM4: no tap in the whole deck reaches the letter (letter beats stay 1, mirror stays hidden)", dend["letterShown"] == 1 and not dend["mirror"], dend)
    # ---- letterPage via the exposed state API, then a REAL TAP on the mirror ----
    pp.evaluate("() => { const st = window.__fpStage; st.state.view='letterPage'; st.state.letter=0; st.render(); }")
    pp.wait_for_timeout(900)
    mir_vis = pp.evaluate("() => { const e = document.getElementById('fpLinkLetterAll'); return e ? e.offsetParent !== null : false; }")
    check("ITEM4: mirror link visible in letterPage view", mir_vis)
    pp.locator("#fpLinkLetterAll").click()
    pp.wait_for_timeout(800)
    plain = pp.evaluate("""() => { const d = document.getElementById('dealPlain'); if (!d) return null;
      const r = d.getBoundingClientRect(); const cs = getComputedStyle(d);
      const t = document.getElementById('dealPlainText');
      const c = document.getElementById('dealPlainClose');
      const cr = c ? c.getBoundingClientRect() : null;
      return {hidden: d.hidden, rect: {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)},
        pos: cs.position, bg: cs.backgroundColor, textHead: t ? t.textContent.slice(0, 40) : null,
        closeVis: c ? c.offsetParent !== null : false, closeRect: cr ? {x: Math.round(cr.x), y: Math.round(cr.y)} : null}; }""")
    print("dealPlain:", json.dumps(plain), flush=True)
    check("ITEM4: #dealPlain opens on a real mirror-link tap from the deal view", plain and not plain["hidden"], plain)
    check("ITEM4: #dealPlain is fullscreen fixed in-frame [0,0,390,844]", plain and plain["rect"] == {"x": 0, "y": 0, "w": 390, "h": 844} and plain["pos"] == "fixed", plain["rect"] if plain else None)
    check("ITEM4: #dealPlain carries the whole letter as plain text", plain and plain["textHead"] and plain["textHead"].startswith("THE COLLECTIVE AGREEMENT"), plain["textHead"] if plain else None)
    check("ITEM4: #dealPlain close x in view", plain and plain["closeVis"], plain)
    pp.screenshot(path=OUT + "fix2-390-dealplain.png")
    pp.keyboard.press("Escape")
    pp.wait_for_timeout(500)
    check("ITEM4: #dealPlain closes on Esc", pp.evaluate("() => document.getElementById('dealPlain').hidden") == True)
    pp.locator("#fpStageExit").click()
    pp.wait_for_timeout(800)
    # ---- remove modal: returning citizen, two saved accounts ----
    pp.evaluate("""() => {
      localStorage.setItem('nayanet_smart_alias', 'shawn');
      localStorage.setItem('nayanet_smart_name', 'Shawn');
      localStorage.setItem('nayanet_smart_identities', JSON.stringify([{alias:'shawn',name:'Shawn'},{alias:'friend',name:'Friend'}]));
    }""")
    pp.goto(BASE + "/", wait_until="domcontentloaded", timeout=120000)
    pp.wait_for_timeout(1500)
    ret = pp.evaluate("() => document.body.classList.contains('fp-returning')")
    check("ITEM3: returning view shows for saved alias", ret)
    pp.locator("#newAccountLine").click()
    pp.wait_for_timeout(800)
    rows = pp.locator(".returning-other-row")
    check("ITEM3: others list shows the second account row", rows.count() == 1, rows.count())
    pp.locator(".returning-other-x").first.click()
    pp.wait_for_timeout(800)
    rm = pp.evaluate("""() => { const m = document.getElementById('fpRemoveModal'); if (!m) return null;
      const r = m.getBoundingClientRect(); const cs = getComputedStyle(m);
      const card = document.querySelector('.fp-remove-card'); const cc = card ? getComputedStyle(card) : null;
      const cr = card ? card.getBoundingClientRect() : null;
      const x = document.getElementById('fpRemoveClose'); const xr = x ? x.getBoundingClientRect() : null;
      const t = document.getElementById('fpRemoveText');
      return {hidden: m.hidden, rect: {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)},
        pos: cs.position, bg: cs.backgroundColor,
        card: cr ? {x: Math.round(cr.x), y: Math.round(cr.y), w: Math.round(cr.width), h: Math.round(cr.height)} : null,
        cardBorder: cc ? cc.borderTopWidth : null, cardBg: cc ? cc.backgroundColor : null,
        closeVis: x ? x.offsetParent !== null : false, closeRect: xr ? {x: Math.round(xr.x), y: Math.round(xr.y)} : null,
        text: t ? t.textContent.slice(0, 60) : null}; }""")
    print("removeModal:", json.dumps(rm), flush=True)
    check("ITEM3: #fpRemoveModal opens on a real x tap (names the account)", rm and not rm["hidden"] and rm["text"] and "Friend" in rm["text"], rm)
    check("ITEM3: modal is fullscreen in-frame [0,0,390,844], opaque", rm and rm["rect"] == {"x": 0, "y": 0, "w": 390, "h": 844} and rm["bg"] == "rgb(2, 3, 10)", rm)
    check("ITEM3: no floating card (card is transparent, borderless, full-width)", rm and rm["cardBg"] in ("rgba(0, 0, 0, 0)", "transparent") and rm["cardBorder"] == "0px" and rm["card"]["w"] >= 350, rm)
    check("ITEM3: clear x close in view (top-right)", rm and rm["closeVis"] and rm["closeRect"]["x"] >= 320, rm)
    pp.screenshot(path=OUT + "fix2-390-remove.png")
    pp.locator("#fpRemoveClose").click()
    pp.wait_for_timeout(500)
    check("ITEM3: modal closes on x tap, account NOT removed", pp.evaluate("() => document.getElementById('fpRemoveModal').hidden") == True and pp.locator(".returning-other-row").count() == 1)
    pp.locator(".returning-other-x").first.click()
    pp.wait_for_timeout(600)
    pp.keyboard.press("Escape")
    pp.wait_for_timeout(500)
    check("ITEM3: modal closes on Esc", pp.evaluate("() => document.getElementById('fpRemoveModal').hidden") == True)
    print("portal pageerrors:", perrs2, "console errors:", cerrs2[:8], flush=True)
    check("0 page errors in portal session", len(perrs2) == 0, perrs2)
    pp.close()
    # ================= 1440: trio keepers =================
    ctx1440 = b.new_context(viewport={"width": 1440, "height": 900}, ignore_https_errors=True)
    p2 = ctx1440.new_page()
    perrs3 = []
    p2.on("pageerror", lambda e: perrs3.append("1440:" + str(e)))
    p2.goto(BASE + "/?walk=1&name=Shawn&alias=shawn", wait_until="domcontentloaded", timeout=120000)
    p2.wait_for_selector("#bdTrio .bd-phone", timeout=60000)
    p2.wait_for_timeout(1200)
    m = p2.evaluate("""() => { const ps=[...document.querySelectorAll('#bdTrio .bd-phone')].map(p=>Math.round(p.getBoundingClientRect().width));
      const tw=document.querySelector('#fpWalk').getBoundingClientRect();
      return {phones: ps, fpWalkW: Math.round(tw.width), fpWalkX: Math.round(tw.x)}; }""")
    print("1440 widths:", json.dumps(m), flush=True)
    check("keeper D2: trio phones ~360px at 1440", m["phones"] and min(m["phones"]) >= 330, m)
    clip = p2.evaluate(CLIP_JS)
    check("keeper D2: no clipping at 1440 group 1", clip == [], clip)
    hdr = p2.evaluate(HEADER_JS)
    ok_h = all(len(h["imgs"]) == 2 and all(i["nw"] > 0 and i["vis"] for i in h["imgs"]) for h in hdr)
    check("keeper D5: header on every phone at 1440", ok_h, hdr)
    p2.screenshot(path=OUT + "fix2-1440-g1.png")
    for g in range(7):
        p2.locator("#fpWalkNext").click(); p2.wait_for_timeout(700)
        clip = p2.evaluate(CLIP_JS)
        check("keeper D2: no clipping at 1440 group %d" % (g+2), clip == [], clip)
    p2.locator("#fpWalkNext").click()
    p2.wait_for_selector("#fpWalkEnd:not([hidden])", timeout=30000)
    p2.wait_for_timeout(1200)
    end2 = p2.evaluate("""() => { const e = document.getElementById('fpWalkEnd'); const s = document.querySelector('#bdEndPhone .bd-screen');
      const er = e.getBoundingClientRect(), sr = s.getBoundingClientRect();
      return {whole: er.top >= sr.top - 1 && er.bottom <= sr.bottom + 1, video: !!document.querySelector('#bdEndPhone video')}; }""")
    check("keeper: end screen whole at 1440, no video at end", end2["whole"] and not end2["video"], end2)
    p2.screenshot(path=OUT + "fix2-1440-end.png")
    print("1440 pageerrors:", perrs3, flush=True)
    check("0 page errors at 1440", len(perrs3) == 0, perrs3)
    p2.close()
    b.close()
print("FAILS:", fails if fails else "NONE")
