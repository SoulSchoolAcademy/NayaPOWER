# FIX1 probe — D1-D5 + keeper re-probe. Real taps, Chromium via forwarder.
import json, time
from playwright.sync_api import sync_playwright
BASE = "https://official-walkthrough-staging.nayapower.workers.dev"
OUT = "/home/hatch/workspace/team-nitro/walkthrough-official-20261127/fix1/maker/evidence/"
fails = []
def check(name, ok, extra=""):
    print(("PASS " if ok else "FAIL ") + name + (" | " + str(extra)[:220] if extra != "" else ""), flush=True)
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
    # ---------- 390: certificate ----------
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
    pg.wait_for_timeout(10000)  # D1: veil used to pop at ~5s
    v = pg.evaluate("() => { const e = document.getElementById('installVeil'); return {hidden: e.hidden, disp: getComputedStyle(e).display}; }")
    check("D1: veil stays hidden after 10s+ on cert", v["hidden"] or v["disp"] == "none", v)
    ent = pg.evaluate("() => { const b = document.getElementById('enterBtn'); if (!b) return null; const r = b.getBoundingClientRect(); const el = document.elementFromPoint(r.x + r.width/2, r.y + r.height/2); return {vis: b.offsetParent !== null, disabled: b.disabled, hit: el ? (el.id || el.className || el.tagName) : null}; }")
    hit_ok = pg.evaluate("() => { const b = document.getElementById('enterBtn'); const r = b.getBoundingClientRect(); const el = document.elementFromPoint(r.x + r.width/2, r.y + r.height/2); return el ? !!el.closest('#enterBtn') : false; }")
    check("D1: ENTER tappable (top element is ENTER, not veil)", ent and ent["vis"] and not ent["disabled"] and hit_ok, (ent, hit_ok))
    # type alias + ENTER -> taken state
    alias_in = pg.locator("#aliasInput")
    alias_in.fill("shawn")
    pg.wait_for_timeout(1200)
    pg.locator("#enterBtn").click()
    for _ in range(10):
        pg.wait_for_timeout(2000)
        _st = pg.evaluate("() => { const s=document.getElementById('aliasStatus'); return s ? s.textContent : ''; }")
        if "already claimed" in _st: break
    dt = pg.evaluate("""() => { const el = document.getElementById('certDatetime'); if (!el) return null;
      const wd = el.querySelector('.cert-dt-word');
      return {hidden: el.hidden, text: el.textContent, wdColor: wd ? getComputedStyle(wd).color : null}; }""")
    print("certDatetime:", json.dumps(dt), flush=True)
    check("D3: digit tiles VISIBLE in already-claimed state", dt and not dt["hidden"] and len(dt["text"]) > 8, dt)
    check("D3: weekday word shown in its §3.3 colour (certified Tue 20 Oct 2026 = gold)", dt and "TUESDAY" in dt["text"] and dt["wdColor"] == "rgb(212, 160, 23)", dt)
    t1 = pg.evaluate("() => document.getElementById('certDatetime').textContent")
    pg.wait_for_timeout(2200)
    t2 = pg.evaluate("() => document.getElementById('certDatetime').textContent")
    check("D3: tiles tick (time changes in ~2s)", t1 != t2, (t1, t2))
    note = pg.evaluate("""() => { const n = document.getElementById('hubNote'); if (!n || n.hidden) return null;
      const r = n.getBoundingClientRect(); const p = n.parentElement.getBoundingClientRect();
      return {leftGap: Math.round(r.left - p.left), rightGap: Math.round(p.right - r.right), text: n.textContent.slice(0,60)}; }""")
    print("hubNote:", json.dumps(note), flush=True)
    check("D4: already-claimed note has margins clear of frame (>=16px each side)", note and note["leftGap"] >= 16 and note["rightGap"] >= 16, note)
    pg.screenshot(path=OUT + "fix1-390-cert.png")
    # silent restore on reload (savedAlias in localStorage now)
    pg.goto(BASE + "/identity.html?name=Shawn", wait_until="domcontentloaded", timeout=120000)
    pg.wait_for_timeout(4000)
    dt2 = pg.evaluate("() => { const el = document.getElementById('certDatetime'); return el ? {hidden: el.hidden, text: el.textContent} : null; }")
    check("D3: tiles visible on silent restore reload (no new claim)", dt2 and not dt2["hidden"] and "TUESDAY" in dt2["text"], dt2)
    # This is me -> walk
    alias_in = pg.locator("#aliasInput")
    try:
        alias_in.fill("shawn")
    except Exception: pass
    pg.wait_for_timeout(800)
    pg.locator("#enterBtn").click()
    pg.wait_for_timeout(3500)
    tim = pg.locator("#fpThisIsMe")
    check("D3: 'This is me' offered on taken state", tim.count() == 1)
    tim.click()
    pg.wait_for_selector("#bdTrio .bd-phone", timeout=60000)
    pg.wait_for_timeout(1200)
    check("walk loads after This-is-me", pg.url.startswith(BASE + "/?walk=1"), pg.url)
    # ---------- 390 walk: headers + clips group by group ----------
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
        if g == 2:  # vision reveal keeper
            vph = pg.locator('#bdTrio .bd-phone[data-key="vision"]')
            if vph.count():
                vph.locator(".bd-ball").click(); pg.wait_for_timeout(600)
                check("keeper: vision picture reveals on ball tap (390)", vph.locator(".bd-bgpic").evaluate("el => getComputedStyle(el).opacity") == "1")
                vph.locator(".bd-ball").click(); pg.wait_for_timeout(400)
        if g == 1:  # video keeper
            vph = pg.locator('#bdTrio .bd-phone[data-key="video"]')
            if vph.count():
                vph.locator(".bd-ball").click(); pg.wait_for_timeout(1500)
                st = pg.evaluate("() => { const v = document.querySelector('#bdTrio .bd-phone[data-key=\"video\"] video'); return v ? {paused: v.paused, t: v.currentTime} : null; }")
                check("keeper: video ball plays (390)", st and not st["paused"], st)
                vph.locator(".bd-ball").click(); pg.wait_for_timeout(400)
                st2 = pg.evaluate("() => { const v = document.querySelector('#bdTrio .bd-phone[data-key=\"video\"] video'); return v ? v.paused : null; }")
                check("keeper: video ball pauses (390)", st2 == True)
        clip = pg.evaluate(CLIP_JS)
        check("group %d of 8: no clipping at 390" % (g+1), clip == [], clip)
        hdr = pg.evaluate(HEADER_JS)
        ok_h = all(len(h["imgs"]) == 2 and all(i["nw"] > 0 and i["vis"] for i in h["imgs"]) for h in hdr)
        check("D5: header (emblem + Naya) on every phone, group %d (390)" % (g+1), ok_h, hdr)
        if g == 0: pg.screenshot(path=OUT + "fix1-390-g1.png")
        if g < 7:
            pg.locator("#fpWalkNext").click(); pg.wait_for_timeout(800)
    # end screen
    pg.locator("#fpWalkNext").click()
    pg.wait_for_selector("#fpWalkEnd:not([hidden])", timeout=30000)
    pg.wait_for_timeout(1500)
    end = pg.evaluate("""() => { const e = document.getElementById('fpWalkEnd'); const s = document.querySelector('#bdEndPhone .bd-screen');
      const er = e.getBoundingClientRect(), sr = s.getBoundingClientRect();
      return {whole: er.top >= sr.top - 1 && er.bottom <= sr.bottom + 1, top: Math.round(er.top), bottom: Math.round(er.bottom), sTop: Math.round(sr.top), sBottom: Math.round(sr.bottom), world: document.getElementById('fpWalkLink').textContent}; }""")
    check("keeper: end screen whole at 390", end["whole"], end)
    hdr_end = pg.evaluate("""() => { const p = document.querySelector('#bdEndPhone .bd-phone'); if (!p) return [];
      return [...p.querySelectorAll('.bd-walkhead img')].map(im => ({src: (im.getAttribute('src')||'').split('/').pop(), nw: im.naturalWidth, vis: im.offsetParent !== null})); }""")
    check("D5: header on end phone too (390)", len(hdr_end) == 2 and all(i["nw"] > 0 and i["vis"] for i in hdr_end), hdr_end)
    ls = pg.evaluate("() => { const S = JSON.parse(localStorage.getItem('naya_welcome_right_v1') || 'null'); return S ? Object.keys(S.answers).length : 0; }")
    check("keeper: answers saved (30+ keys)", ls >= 30, ls)
    pg.screenshot(path=OUT + "fix1-390-end.png")
    print("390 pageerrors:", perrs, "console errors:", cerrs, "failed:", failed[:6], flush=True)
    unexplained = [c for c in cerrs if "503" not in c and "409" not in c]
    check("0 UNEXPLAINED errors at 390 (503-agmt retried 200 + honest 409 only)", len(perrs) == 0 and len(unexplained) == 0, (perrs, unexplained))
    pg.close()
    # ---------- 1440 ----------
    ctx1440 = b.new_context(viewport={"width": 1440, "height": 900}, ignore_https_errors=True)
    p2 = ctx1440.new_page()
    p2.on("pageerror", lambda e: perrs.append("1440:" + str(e)))
    p2.goto(BASE + "/?walk=1&name=Shawn&alias=shawn", wait_until="domcontentloaded", timeout=120000)
    p2.wait_for_selector("#bdTrio .bd-phone", timeout=60000)
    p2.wait_for_timeout(1200)
    m = p2.evaluate("""() => { const ps=[...document.querySelectorAll('#bdTrio .bd-phone')].map(p=>Math.round(p.getBoundingClientRect().width));
      const tw=document.querySelector('#fpWalk').getBoundingClientRect();
      return {phones: ps, fpWalkW: Math.round(tw.width), fpWalkX: Math.round(tw.x)}; }""")
    print("1440 widths:", json.dumps(m), flush=True)
    check("D2: trio phones widened (~360, not 211)", m["phones"] and min(m["phones"]) >= 330, m)
    clip = p2.evaluate(CLIP_JS)
    check("D2: no clipping at 1440 group 1 (header, question, chin)", clip == [], clip)
    hdr = p2.evaluate(HEADER_JS)
    ok_h = all(len(h["imgs"]) == 2 and all(i["nw"] > 0 and i["vis"] for i in h["imgs"]) for h in hdr)
    check("D5: header on every phone at 1440", ok_h, hdr)
    p2.screenshot(path=OUT + "fix1-1440-g1.png")
    # walk 1440 to end (reuse fills minimal: just advance; answers optional)
    for g in range(7):
        p2.locator("#fpWalkNext").click(); p2.wait_for_timeout(700)
        clip = p2.evaluate(CLIP_JS)
        check("D2: no clipping at 1440 group %d" % (g+2), clip == [], clip)
    p2.locator("#fpWalkNext").click()
    p2.wait_for_selector("#fpWalkEnd:not([hidden])", timeout=30000)
    p2.wait_for_timeout(1200)
    end2 = p2.evaluate("""() => { const e = document.getElementById('fpWalkEnd'); const s = document.querySelector('#bdEndPhone .bd-screen');
      const er = e.getBoundingClientRect(), sr = s.getBoundingClientRect();
      return {whole: er.top >= sr.top - 1 && er.bottom <= sr.bottom + 1, video: !!document.querySelector('#bdEndPhone video')}; }""")
    check("keeper: end screen whole at 1440, no video at end", end2["whole"] and not end2["video"], end2)
    p2.screenshot(path=OUT + "fix1-1440-end.png")
    print("1440 pageerrors:", [e for e in perrs if e.startswith('1440')], flush=True)
    p2.close()
    b.close()
print("FAILS:", fails if fails else "NONE")
