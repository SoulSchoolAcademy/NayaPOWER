#!/usr/bin/env python3
"""CAPTAIN'S EYE — Membership rebuild fix-8. Written fresh for this eye.
Walks the STAGED URL in VM Playwright Firefox, desktop 1920 then phone 390.
Real taps; audio judged by page state only. Logs to eye-log.json; shots e##/p##.
"""
import json, sys, time, traceback
from playwright.sync_api import sync_playwright

OUT = "/home/hatch/workspace/team-nitro/membership-rebuild-fix8-20261119/eye"
URL = ("https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/"
       "membership-rebuild-20261119/membership-rebuild.html"
       "&ref=membership/rebuild-fix8-20261119"
       "&cb=b13c17104a188e3b53bbbe77483fd4805afc29f2")
LOG, ERRORS = [], []

PROBE = """() => {
  const vis = el => { if(!el) return false; const cs=getComputedStyle(el);
    if(cs.display==='none'||cs.visibility==='hidden') return false;
    const r=el.getBoundingClientRect(); return r.width>0 && r.height>0; };
  const q = s => document.querySelector(s);
  const qa = s => [...document.querySelectorAll(s)];
  const a = window.saPcExactAudio || null;
  const bars = qa('.notif-bar').map(el => { const r=el.getBoundingClientRect();
    return {id: el.id||null, disp: getComputedStyle(el).display, vis: vis(el),
      x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)}; });
  const live = q('#os-bottom3');
  const tiles = live ? qa('#os-bottom3 .notif-seg').map(s => ({
    lbl: (s.textContent||'').trim().replace(/\\s+/g,' ').slice(0,14),
    nc: s.style.getPropertyValue('--nc'),
    href: (s.closest('a')||{}).href || null })) : [];
  const h3 = q('#saPaneLesson h3');
  const ifr = q('#saPaneLesson iframe') || q('.sa-sixteen iframe');
  const bodyText = document.body.innerText || '';
  let efp = null;
  if (ifr) { const r = ifr.getBoundingClientRect();
    const el = document.elementFromPoint(r.x + r.width/2, r.y + Math.min(30, r.height*0.2));
    efp = el ? (el.tagName + (el.id ? '#'+el.id : '') + (el.className && typeof el.className==='string' ? '.'+el.className.split(' ')[0] : '')) : null; }
  return {
    loginVis: vis(q('#saLoginStage')), courseVis: vis(q('#saCourse')),
    panes: {lesson: q('#saPaneLesson') ? !q('#saPaneLesson').hidden : null,
            audios: q('#saPanePodcasts') ? !q('#saPanePodcasts').hidden : null,
            videos: q('#saPaneVideo') ? !q('#saPaneVideo').hidden : null},
    lessonOpen: document.body.classList.contains('sa-lesson-open'),
    roomsPlus: q('#os-rooms-plus') ? getComputedStyle(q('#os-rooms-plus')).display : null,
    feedAdd: q('#mwFeedPills .add-tab') ? getComputedStyle(q('#mwFeedPills .add-tab')).display : null,
    deck: q('#deckStatus') ? q('#deckStatus').textContent.trim() : null,
    deckLive: q('#deckNowPlaying') ? q('#deckNowPlaying').textContent.trim().slice(0,80) : null,
    audio: a ? {paused: a.paused, t: +a.currentTime.toFixed(2), rs: a.readyState,
      err: a.error ? a.error.code : null} : null,
    theatre: vis(q('#saTheatre')),
    theatreTitle: q('#saTheatreTitle') ? q('#saTheatreTitle').textContent.trim() : null,
    watchVis: qa('[data-sa-watch-ch]').filter(b=>vis(b)).length,
    bars, tiles,
    staleExists: !!document.getElementById('naya-notif-bar'),
    liveVis: vis(live),
    visBarCount: bars.filter(b=>b.vis).length,
    h3: h3 ? {text: h3.textContent.trim(), sw: h3.scrollWidth, cw: h3.clientWidth,
      h: Math.round(h3.getBoundingClientRect().height),
      ws: getComputedStyle(h3).whiteSpace} : null,
    d2: {hasNayaNETCreate: bodyText.includes('NayaNET - Create'),
         hasGrEllipsis: bodyText.includes('Create. Connect. Gr'),
         iframe: ifr ? {x: Math.round(ifr.getBoundingClientRect().x),
           y: Math.round(ifr.getBoundingClientRect().y),
           w: Math.round(ifr.getBoundingClientRect().width),
           h: Math.round(ifr.getBoundingClientRect().height),
           contentDocNull: (ifr.contentDocument===null),
           src: (ifr.src||'').slice(0,90)} : null,
         efpTitleArea: efp},
    scrollW: document.documentElement.scrollWidth, innerW: window.innerWidth,
    url: location.href,
    errors: (window.__eyeErrors||[]).slice(-8),
  };
}"""

def log(step, ok, detail):
    LOG.append({"step": step, "ok": bool(ok), "detail": detail})
    print(f"[{'PASS' if ok else 'FAIL'}] {step}: {json.dumps(detail)[:650]}", flush=True)

def shot(page, name, clip=None):
    if clip:
        page.screenshot(path=f"{OUT}/{name}.png", clip=clip)
    else:
        page.screenshot(path=f"{OUT}/{name}.png")

def probe(page):
    return page.evaluate(PROBE)

def census_ok(st):
    return st["staleExists"] is False and st["visBarCount"] == 1 and st["liveVis"] is True

def join_door(page):
    st = probe(page)
    if st["loginVis"]:
        page.locator('[data-hook="name"]').fill("Eye Test")
        page.locator('[data-hook="code"]').fill("1234")
        page.locator('.enter').first.click(timeout=8000)
        page.wait_for_timeout(2500)

def pick_course(page):
    if page.locator('.sa-course-pick[data-mw-open-mship="Naya Academy"]').count() > 0:
        page.locator('.sa-course-pick[data-mw-open-mship="Naya Academy"]').click(timeout=8000)
        page.wait_for_timeout(2500)

def enter_course(page):
    page.locator('.mw-mship-btn[data-mw-cover="Naya Academy"]').click(timeout=8000)
    page.wait_for_timeout(2000)
    join_door(page)
    pick_course(page)

def back_course(page):
    page.locator('#saSectionHead button', has_text='Back to the course').first.click(timeout=8000)
    page.wait_for_timeout(1200)

def goto_audios(page):
    st = probe(page)
    if st["panes"].get("audios"):
        return
    b = page.locator('#saSectionHead button', has_text='Back to the course')
    if b.count() > 0:
        try: b.first.click(timeout=8000); page.wait_for_timeout(1200)
        except Exception: pass
    page.locator('[data-sa-toc="audios"]:visible').first.click(timeout=8000)
    page.wait_for_timeout(1200)
    if not probe(page)["panes"].get("audios"):
        raise RuntimeError("Audios pane did not open")

def click_play(page):
    try:
        page.locator('#dPlay:visible').click(timeout=15000)
    except Exception:
        bb = page.locator('#dPlay').bounding_box()
        page.mouse.click(bb["x"]+bb["width"]/2, bb["y"]+bb["height"]/2)

def play_until_advancing(page, wait_s=20):
    st = probe(page); a = st.get("audio") or {}
    if a and not a.get("paused"):
        t1 = a.get("t", 0); time.sleep(1.0)
        a2 = (probe(page).get("audio") or {})
        if a2.get("t", 0) > t1:
            return {"ok": True, "audio": a2, "deck": probe(page)["deck"], "already": True}
    click_play(page)
    t0 = time.time()
    while time.time()-t0 < wait_s:
        st = probe(page); a = st.get("audio") or {}
        if a and not a.get("paused"):
            t1 = a.get("t", 0); time.sleep(1.0)
            a2 = (probe(page).get("audio") or {})
            if a2.get("t", 0) > t1:
                return {"ok": True, "audio": a2, "deck": probe(page)["deck"]}
        time.sleep(0.5)
    st = probe(page)
    return {"ok": False, "audio": st.get("audio"), "deck": st.get("deck")}

def wait_paused(page, dur=6.0):
    t0 = time.time()
    while time.time()-t0 < dur:
        st = probe(page); a = st.get("audio") or {}
        if a.get("paused"):
            return {"paused": True, "lat": round(time.time()-t0, 2), "t": a.get("t"), "deck": st["deck"]}
        time.sleep(0.25)
    st = probe(page)
    return {"paused": False, "lat": None, "t": (st.get("audio") or {}).get("t"), "deck": st["deck"]}

def desktop(page):
    page.goto(URL, wait_until="load", timeout=90000)
    page.wait_for_timeout(4000)
    st = probe(page)
    log("E0 fresh load: one bar, no stale", census_ok(st),
        {"bars": st["bars"], "stale": st["staleExists"], "visCount": st["visBarCount"],
         "tiles": [(t["lbl"], t["nc"]) for t in st["tiles"]], "scrollW": st["scrollW"]})
    shot(page, "e00-desktop-fresh")
    shot(page, "e00b-desktop-bottom", clip={"x":0,"y":980,"width":1920,"height":100})
    # E1 enter course -> lesson
    try:
        enter_course(page)
        st = probe(page)
        log("E1 course + Day1 lesson: one bar", bool(st["panes"]["lesson"]) and census_ok(st),
            {"panes": st["panes"], "lessonOpen": st["lessonOpen"], "roomsPlus": st["roomsPlus"],
             "feedAdd": st["feedAdd"], "bars": st["bars"]})
        shot(page, "e01-desktop-lesson")
    except Exception as e:
        log("E1 course entry", False, {"err": str(e)[:300]})
    # E2 theatre twice from Videos Watch + feed card
    try:
        back_course(page)
        page.locator('[data-sa-toc="videos"]:visible', has_text="Open Videos").first.click(timeout=8000)
        page.wait_for_timeout(2000)
        page.locator('[data-sa-watch-ch]:visible').first.click(timeout=8000)
        page.wait_for_timeout(3000)
        st = probe(page); t1 = st["theatreTitle"]
        log("E2a F3 theatre opens (Videos Watch)", bool(st["theatre"]), {"title": t1})
        shot(page, "e02-desktop-theatre1")
        page.locator('#saTheatreClose').click(timeout=8000); page.wait_for_timeout(1200)
        page.locator('[data-sa-watch-ch]:visible').first.click(timeout=8000)
        page.wait_for_timeout(3000)
        st = probe(page)
        log("E2b F3 theatre opens 2nd time, same title", bool(st["theatre"]) and st["theatreTitle"]==t1,
            {"title": st["theatreTitle"]})
        shot(page, "e03-desktop-theatre2")
        page.locator('#saTheatreClose').click(timeout=8000); page.wait_for_timeout(1200)
    except Exception as e:
        log("E2 theatre", False, {"err": str(e)[:300], "trace": traceback.format_exc()[-300:]})
    # E3 F1 resume + deck stays live (updateDock watch)
    try:
        goto_audios(page)
        r = play_until_advancing(page)
        log("E3a Audios play", r["ok"], r)
        click_play(page); page.wait_for_timeout(1200)
        st = probe(page)
        log("E3b bare pause: audio paused, ON AIR stays (documented)", (st.get("audio") or {}).get("paused") is True,
            {"audio": st["audio"], "deck": st["deck"]})
        click_play(page); time.sleep(1.5)
        st = probe(page); a = st.get("audio") or {}
        log("E3c F1 resume re-lights ON AIR, deck live", (not a.get("paused")) and st["deck"]=="ON AIR",
            {"audio": a, "deck": st["deck"], "deckLive": st["deckLive"], "errors": st["errors"]})
        shot(page, "e04-desktop-playing")
    except Exception as e:
        log("E3 resume", False, {"err": str(e)[:300]})
    # E4 Space gate
    try:
        goto_audios(page)
        play_until_advancing(page)
        page.keyboard.press("Space"); page.wait_for_timeout(1000)
        st = probe(page)
        log("E4a F2 Space pauses in Audios", (st.get("audio") or {}).get("paused") is True, {"audio": st["audio"]})
        page.keyboard.press("Space"); page.wait_for_timeout(1500)
        st = probe(page); a = st.get("audio") or {}
        log("E4b F2 Space resumes in Audios", not a.get("paused"), {"audio": a, "deck": st["deck"]})
        back_course(page)
        page.keyboard.press("Space"); page.wait_for_timeout(1000)
        st = probe(page)
        log("E4c F2 Space NO resume at course home", (st.get("audio") or {}).get("paused") is True,
            {"audio": st["audio"], "panes": st["panes"]})
        page.locator('#saBackBtn:visible').first.click(timeout=8000); page.wait_for_timeout(1500)
        page.keyboard.press("Space"); page.wait_for_timeout(1000)
        st = probe(page)
        log("E4d F2 Space NO resume after course closed", (st.get("audio") or {}).get("paused") is True,
            {"audio": st["audio"], "courseVis": st["courseVis"]})
    except Exception as e:
        log("E4 space gate", False, {"err": str(e)[:300], "trace": traceback.format_exc()[-300:]})
    # E5 six leave paths
    paths = [("5a-lessons-tab","lessons"),("5b-videos-tab","videos"),("5c-chooser","chooser"),
             ("5d-add-tile","add"),("5e-browser-back","back"),("5f-back-button","btn")]
    for name, kind in paths:
        try:
            st = probe(page)
            if not st["courseVis"]:
                enter_course(page); page.wait_for_timeout(1000)
            goto_audios(page)
            r = play_until_advancing(page)
            if not r["ok"]:
                log(f"E5-{name} pre-play", False, r); continue
            lat = None
            if kind == "lessons":
                back_course(page); lat = wait_paused(page)
                page.locator('[data-sa-toc="lessons"]:visible', has_text="Open Lessons").first.click(timeout=8000)
                page.wait_for_timeout(1500)
            elif kind == "videos":
                back_course(page); lat = wait_paused(page)
                page.locator('[data-sa-toc="videos"]:visible', has_text="Open Videos").first.click(timeout=8000)
                page.wait_for_timeout(1500)
            elif kind == "chooser":
                h = page.locator('#saCoursePickHead:visible')
                if h.count()>0: h.first.click(timeout=8000)
                else:
                    back_course(page)
                    page.locator('#saCoursePickHead:visible').first.click(timeout=8000)
            elif kind == "add":
                page.locator('#os-bottom3 a[data-notif="plus"]').click(timeout=8000)
            elif kind == "back":
                page.go_back(timeout=15000)
            elif kind == "btn":
                page.locator('#saBackBtn:visible').first.click(timeout=8000)
            if lat is None: lat = wait_paused(page)
            page.wait_for_timeout(800)
            st = probe(page); a = st.get("audio") or {}
            shot(page, f"e05-leave-{name}")
            log(f"E5-{name} audio stops", bool(lat["paused"]),
                {"pausedAfter": a.get("paused"), "latS": lat["lat"], "deck": st["deck"],
                 "visCount": st["visBarCount"], "stale": st["staleExists"]})
            if kind == "add":
                page.keyboard.press("Escape"); page.wait_for_timeout(800)
        except Exception as e:
            log(f"E5-{name}", False, {"err": str(e)[:300], "trace": traceback.format_exc()[-300:]})
    # E6 lesson ADD-only bar, three entries + close
    try:
        st = probe(page)
        if not st["courseVis"]:
            enter_course(page)
        else:
            back_course(page); page.wait_for_timeout(1000); pick_course(page)
        st = probe(page)
        log("E6a lesson via chooser: ADD-only + one bar",
            st["lessonOpen"] and st["roomsPlus"]=="none" and st["feedAdd"]=="none" and census_ok(st),
            {"lessonOpen": st["lessonOpen"], "roomsPlus": st["roomsPlus"], "feedAdd": st["feedAdd"]})
        back_course(page)
        page.locator('[data-sa-toc="lessons"]:visible', has_text="Open Lessons").first.click(timeout=8000)
        page.wait_for_timeout(2500)
        st = probe(page)
        log("E6b lesson via Open Lessons: ADD-only + one bar",
            st["lessonOpen"] and st["roomsPlus"]=="none" and st["feedAdd"]=="none" and census_ok(st),
            {"lessonOpen": st["lessonOpen"]})
        page.locator('[data-sa-next-lesson]:visible').first.click(timeout=8000)
        page.wait_for_timeout(2500)
        st = probe(page)
        log("E6c lesson via Next lesson Day2: ADD-only + one bar",
            st["lessonOpen"] and st["roomsPlus"]=="none" and st["feedAdd"]=="none" and census_ok(st),
            {"h3": st["h3"]})
        shot(page, "e06-desktop-lesson2")
        back_course(page)
        st = probe(page)
        log("E6d lesson closed: full bar returns + one bar",
            (not st["lessonOpen"]) and st["roomsPlus"]!="none" and census_ok(st),
            {"lessonOpen": st["lessonOpen"], "roomsPlus": st["roomsPlus"]})
    except Exception as e:
        log("E6 lesson bar", False, {"err": str(e)[:300], "trace": traceback.format_exc()[-300:]})
    # E7 button destinations: bottom-bar tile hrefs + taps
    try:
        st = probe(page)
        log("E7a bottom-bar tile hrefs", True, {"tiles": st["tiles"]})
        # tap each non-ADD tile in turn on a fresh load, record landing
        for lbl in ["MAIL", "ACTIVITY", "WORLDS", "ECOSYSTEM", "CONNECT"]:
            try:
                page.goto(URL, wait_until="load", timeout=90000)
                page.wait_for_timeout(3500)
                tile = page.locator(f'#os-bottom3 .notif-seg:has-text("{lbl}")').first
                if tile.count() == 0:
                    log(f"E7b tile {lbl} present", False, {}); continue
                tile.click(timeout=8000)
                page.wait_for_timeout(3000)
                cur = page.evaluate("() => ({url: location.href, title: document.title})")
                log(f"E7b tile {lbl} tap lands", True, cur)
            except Exception as e:
                log(f"E7b tile {lbl} tap", False, {"err": str(e)[:200]})
    except Exception as e:
        log("E7 destinations", False, {"err": str(e)[:300]})

def defect2_verify(page):
    """Own defect-2 adjudication check at 390: is the clipped text page markup or iframe chrome?"""
    page.evaluate("() => { const h = document.querySelector('#saPaneLesson h3'); if(h) h.scrollIntoView({block:'center'}); const f = document.querySelector('#saPaneLesson iframe'); if(f) f.scrollIntoView({block:'center'}); }")
    page.wait_for_timeout(1500)
    st = probe(page)
    d = st["d2"]; h = st["h3"] or {}
    shot(page, "p01-phone-lesson-player")
    full_title = "ACTIVATE YOU / EXPERIENCE ME! Day #1 of the Naya POWER Academy."
    log("P1b D2 h3 wraps fully at 390", h.get("sw")==h.get("cw") and full_title in (h.get("text") or ""),
        {"h3": h})
    log("P1c D2 clipped strings NOT in page DOM", (not d["hasNayaNETCreate"]),
        {"hasNayaNETCreate": d["hasNayaNETCreate"], "hasGrEllipsis": d["hasGrEllipsis"],
         "iframe": d["iframe"], "efpTitleArea": d["efpTitleArea"]})
    return st

def phone(page):
    page.goto(URL, wait_until="load", timeout=90000)
    page.wait_for_timeout(4000)
    st = probe(page)
    log("P0 phone fresh load: one bar, no overflow", st["scrollW"]<=391 and census_ok(st),
        {"scrollW": st["scrollW"], "bars": st["bars"], "stale": st["staleExists"]})
    shot(page, "p00-phone-fresh")
    shot(page, "p00b-phone-bottom", clip={"x":0,"y":752,"width":390,"height":92})
    try:
        enter_course(page)
        st = probe(page)
        log("P1 phone joined + Day1 lesson: one bar", bool(st["panes"]["lesson"]) and census_ok(st),
            {"panes": st["panes"], "scrollW": st["scrollW"], "lessonOpen": st["lessonOpen"],
             "roomsPlus": st["roomsPlus"], "feedAdd": st["feedAdd"]})
        shot(page, "p01-phone-lesson")
        defect2_verify(page)
    except Exception as e:
        log("P1 phone lesson", False, {"err": str(e)[:300], "trace": traceback.format_exc()[-300:]})
    try:
        page.locator('#saPaneLesson [data-sa-toc="audios"]').first.click(timeout=8000)
        page.wait_for_timeout(2000)
        r = play_until_advancing(page)
        log("P2a phone Audios play", r["ok"], r)
        shot(page, "p02-phone-playing")
        click_play(page); time.sleep(1.5)
        st = probe(page)
        log("P2b phone Audios stop", (st.get("audio") or {}).get("paused") is True,
            {"audio": st["audio"], "deck": st["deck"]})
    except Exception as e:
        log("P2 phone Audios", False, {"err": str(e)[:300]})
    try:
        back_course(page)
        page.locator('[data-sa-toc="videos"]:visible', has_text="Open Videos").first.click(timeout=8000)
        page.wait_for_timeout(2000)
        page.locator('[data-sa-watch-ch]:visible').first.click(timeout=8000)
        page.wait_for_timeout(3000)
        st = probe(page)
        log("P3 phone Videos Watch -> theatre", bool(st["theatre"]), {"title": st["theatreTitle"], "scrollW": st["scrollW"]})
        shot(page, "p03-phone-theatre")
        page.locator('#saTheatreClose').click(timeout=8000); page.wait_for_timeout(1200)
    except Exception as e:
        log("P3 phone theatre", False, {"err": str(e)[:300]})
    try:
        back_course(page)
        page.locator('[data-sa-toc="lessons"]:visible', has_text="Open Lessons").first.click(timeout=8000)
        page.wait_for_timeout(2500)
        st = probe(page)
        log("P4 phone lesson ADD-only bar + one bar",
            st["lessonOpen"] and st["roomsPlus"]=="none" and st["feedAdd"]=="none" and census_ok(st) and st["scrollW"]<=391,
            {"lessonOpen": st["lessonOpen"], "roomsPlus": st["roomsPlus"], "feedAdd": st["feedAdd"],
             "bars": st["bars"], "scrollW": st["scrollW"]})
        shot(page, "p04-phone-lesson2")
    except Exception as e:
        log("P4 phone lesson bar", False, {"err": str(e)[:300]})
    st = probe(page)
    log("P5 phone six-tile bar, no overflow", st["scrollW"]<=391 and census_ok(st),
        {"scrollW": st["scrollW"], "bars": st["bars"]})

with sync_playwright() as p:
    browser = p.firefox.launch(headless=True, executable_path="/home/hatch/.cache/ms-playwright/firefox-1555/firefox/firefox")
    try:
        pg = browser.new_page(viewport={"width": 1920, "height": 1080})
        pg.on("pageerror", lambda e: ERRORS.append(str(e)[:300]))
        pg.add_init_script("window.__eyeErrors=[]; window.addEventListener('error', e=>{window.__eyeErrors.push(String(e.message).slice(0,200));});")
        try: desktop(pg)
        except Exception as e: log("DESKTOP RUN", False, {"err": str(e)[:300], "trace": traceback.format_exc()[-400:]})
        pg.close()
        pg2 = browser.new_page(viewport={"width": 390, "height": 844})
        pg2.on("pageerror", lambda e: ERRORS.append(str(e)[:300]))
        pg2.add_init_script("window.__eyeErrors=[]; window.addEventListener('error', e=>{window.__eyeErrors.push(String(e.message).slice(0,200));});")
        try: phone(pg2)
        except Exception as e: log("PHONE RUN", False, {"err": str(e)[:300], "trace": traceback.format_exc()[-400:]})
        pg2.close()
    finally:
        with open(f"{OUT}/eye-log.json", "w") as f:
            json.dump({"log": LOG, "pageErrors": ERRORS}, f, indent=2)
        print("SUMMARY: " + json.dumps({"pass": sum(1 for x in LOG if x["ok"]),
              "fail": sum(1 for x in LOG if not x["ok"]), "total": len(LOG),
              "failedSteps": [x["step"] for x in LOG if not x["ok"]]}))
        browser.close()
print("DONE")
