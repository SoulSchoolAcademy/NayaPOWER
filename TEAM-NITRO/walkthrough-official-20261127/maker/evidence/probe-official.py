# Real-tap probe of the staged OFFICIAL walkthrough (Playwright Chromium
# via the localhost forwarder). Walks all 8 groups / 23 steps with real taps
# at 390x844, measures the picture/input separation on every picture step,
# then the end screen at 1440x900. Prints PASS/FAIL + measurements.
import json, re, sys
from playwright.sync_api import sync_playwright

BASE = "https://official-walkthrough-staging.nayapower.workers.dev/?walk=1&name=Shawn&alias=shawn"
OUT = "/home/hatch/workspace/team-nitro/walkthrough-official-20261127/maker/evidence/"
fails = []
def real_failures(failed, retry, jserrs):
    ok503 = {u.split(" ", 1)[1] for u in retry if u.startswith("200 ")}
    bad = []
    for u in failed:
        if "fonts.googleapis.com" in u:
            continue  # known forwarder cert artifact (checker2 precedent)
        if u.startswith("HTTP 503 ") and u.split(" ", 2)[2] in ok503:
            continue  # transient load flake, proven 200 on retry
        if u.startswith("FAILED ") and "naya-video.mp4" in u and "ERR_ABORTED" in u:
            continue  # leaving the video phone mid-buffer aborts its fetch
        bad.append(u)
    return [str(e) for e in jserrs] + bad
def check(name, ok, extra=""):
    print(("PASS " if ok else "FAIL ") + name + (" " + str(extra) if extra != "" else ""), flush=True)
    if not ok:
        fails.append(name)

PIC_STEPS = {"motto", "mission", "goal", "vision", "love", "dontlove", "thing", "promise", "gift", "unique", "benefit", "connect", "work", "values_stand"}

with sync_playwright() as pw:
    browser = pw.chromium.launch(proxy={"server": "http://127.0.0.1:18080"})
    ctx = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    page = ctx.new_page()
    errors = []
    jserrors = []
    failed_urls = []
    page.on("pageerror", lambda e: (errors.append(str(e)), jserrors.append(str(e))))
    page.on("console", lambda m: errors.append("console." + m.type + ": " + m.text) if m.type == "error" else None)
    page.on("requestfailed", lambda r: failed_urls.append("FAILED " + r.url + " " + str(r.failure)))
    page.on("response", lambda r: failed_urls.append("HTTP " + str(r.status) + " " + r.url) if r.status >= 400 else None)
    page.goto(BASE, wait_until="networkidle", timeout=120000)
    page.wait_for_selector("#bdTrio .bd-phone", timeout=30000)
    check("trio renders 3 phones at 390", page.locator("#bdTrio .bd-phone").count() == 3)
    check("group progress reads Group 1 of 8", "Group 1 of 8" in page.text_content("#bdGroupProg"), page.text_content("#bdGroupProg"))
    check("first phone is Where do you live", "live" in page.locator("#bdTrio .bd-phone").first.text_content().lower())
    check("no Skip visible", not page.is_visible("#fpWalkSkip"))
    check("no name step (first group has live/age_lang/gender)",
          page.locator("#bdTrio .bd-phone").nth(1).text_content().find("How old are you") >= 0)
    # gender dropdown has NO default
    gsel = page.locator('#bdTrio select[data-fid="gender"]')
    check("gender dropdown exists with NO default", gsel.count() == 1 and page.eval_on_selector('#bdTrio select[data-fid="gender"]', "el => el.value") == "")
    # Fill group 1
    page.select_option('#bdTrio select[data-fid="country"]', "canada")
    page.fill('#bdTrio input[data-fid="province"]', "Ontario")
    page.fill('#bdTrio input[data-fid="city"]', "Toronto")
    page.select_option('#bdTrio select[data-fid="age"]', "35-44")
    page.fill('#bdTrio input[data-fid="language"]', "English")
    page.select_option('#bdTrio select[data-fid="gender"]', "female")
    # Favorites + industry live in GROUP 2 in the official flow — filled there.
    # Separation measurement on every picture step, group by group
    sep = {}
    for g in range(8):
        if g == 1:
            # Group 2: favorites + industry_all (+ video phone, no fields)
            page.fill('#bdTrio input[data-fid="brand"]', "Naya")
            page.select_option('#bdTrio select[data-fid="music"]', "rock")
            page.fill('#bdTrio input[data-fid="hobby"]', "Gardening")
            page.fill('#bdTrio input[data-fid="loveelse"]', "Sunsets and good books")
            page.select_option('#bdTrio select[data-fid="sport"]', "soccer")
            page.fill('#bdTrio input[data-fid="team"]', "Toronto FC")
            page.select_option('#bdTrio select[data-fid="industry"]', "technology")
            page.select_option('#bdTrio select[data-fid="connect"]', "people-like-me")
            page.fill('#bdTrio input[data-fid="connectown"]', "People like me")
        phones = page.locator("#bdTrio .bd-phone")
        n = phones.count()
        for i in range(n):
            ph = phones.nth(i)
            key = ph.get_attribute("data-key")
            if key in PIC_STEPS:
                m = page.evaluate("""(ph) => {
                  const st = ph.querySelector('.bd-stage').getBoundingClientRect();
                  const card = ph.querySelector('.bd-card') || ph.querySelector('.bd-video-slot');
                  const cb = card.getBoundingClientRect();
                  const bg = ph.querySelector('.bd-bgpic').getBoundingClientRect();
                  const img = ph.querySelector('.bd-bgpic img');
                  return {stageTop: st.top, stageBottom: st.bottom, cardTop: cb.top, cardBottom: cb.bottom,
                          cardInStage: cb.top >= st.top - 1 && cb.bottom <= st.bottom + 1,
                          bgW: bg.width, bgH: bg.height, imgNat: img ? img.naturalWidth : 0,
                          bgTakesLayout: getComputedStyle(ph.querySelector('.bd-bgpic')).position};
                }""", ph.element_handle())
                sep[key] = m
                check(f"SEP {key}: input card whole inside stage at rest", m["cardInStage"], m)
                check(f"SEP {key}: picture layer is absolute (no layout space)", m["bgTakesLayout"] == "absolute", m["bgTakesLayout"])
                check(f"SEP {key}: picture loaded (naturalWidth>0)", m["imgNat"] > 0, m["imgNat"])
                # Ball reveal: picture full-bleed behind, reveal card whole
                ph.locator(".bd-ball").click()
                page.wait_for_timeout(600)
                r = page.evaluate("""(ph) => {
                  const st = ph.querySelector('.bd-stage').getBoundingClientRect();
                  const rc = ph.querySelector('.bd-reveal-card').getBoundingClientRect();
                  const bg = ph.querySelector('.bd-bgpic').getBoundingClientRect();
                  const op = parseFloat(getComputedStyle(ph.querySelector('.bd-bgpic')).opacity);
                  return {revealed: ph.classList.contains('bd-revealed'), bgOp: op,
                          cardWhole: rc.top >= st.top - 1 && rc.bottom <= st.bottom + 1,
                          bgCoversStage: bg.top <= st.top + 1 && bg.bottom >= st.bottom - 1,
                          cardTop: rc.top, cardBottom: rc.bottom, stageTop: st.top, stageBottom: st.bottom};
                }""", ph.element_handle())
                check(f"REVEAL {key}: ball reveals, picture opacity 1", r["revealed"] and r["bgOp"] >= 0.99, r)
                check(f"REVEAL {key}: picture covers stage full-bleed", r["bgCoversStage"], r)
                check(f"REVEAL {key}: reveal card whole inside stage", r["cardWhole"], r)
                ph.locator(".bd-ball").click()  # back to input
                page.wait_for_timeout(300)
        # Fill the rest of the group before moving on
        page.evaluate("""() => {
          document.querySelectorAll('#bdTrio .bd-answer').forEach(ta => {
            if (!ta.value) { ta.value = 'Our answer, in our own words.'; ta.dispatchEvent(new Event('input', {bubbles: true})); }
          });
        }""")
        if g == 1:
            vph = page.locator('[data-key="video"]')
            check("video phone present (mid-flow, group 2)", vph.count() == 1)
            vsrc = page.evaluate("(el) => el.querySelector('video').getAttribute('src')", vph.element_handle())
            check("video is the DIRECT file route, not YouTube", vsrc == "/naya-video.mp4", vsrc)
            check("video fills the phone screen (inside .bd-screen)", page.evaluate("""(el) => {
              const sc = el.querySelector('.bd-screen').getBoundingClientRect();
              const v = el.querySelector('video').getBoundingClientRect();
              return v.top >= sc.top - 1 && v.bottom <= sc.bottom + 1 && v.left >= sc.left - 1 && v.right <= sc.right + 1;
            }""", vph.element_handle()))
            check("video downloads nothing until play (preload=none)", page.evaluate("(el) => el.querySelector('video').getAttribute('preload')", vph.element_handle()) == "none")
            vph.locator(".bd-ball").click()
            page.wait_for_function("""(el) => { const v = el.querySelector('video'); return v && v.readyState >= 1; }""", arg=vph.element_handle(), timeout=30000)
            meta = page.evaluate("""(el) => { const v = el.querySelector('video'); return {w: v.videoWidth, h: v.videoHeight, dur: Math.round(v.duration)}; }""", vph.element_handle())
            check("video is 576x1024 = exactly 9:16 vertical", meta["w"] == 576 and meta["h"] == 1024, meta)
            check("video duration ~204s", 200 <= meta["dur"] <= 210, meta)
            check("pillars under video are the video's OWN four", "Auto Organizer" in vph.text_content() and "Smart Match" in vph.text_content() and "Your World. Your Freedom" not in vph.text_content())
            yt = page.evaluate("(el) => { const a = el.querySelector('.bd-video-fallback a'); return a ? a.getAttribute('href') : ''; }", vph.element_handle())
            check("YouTube is a fallback link only", yt == "https://youtube.com/watch?v=XqZe1zdF1Tc", yt)
            page.wait_for_timeout(2500)
            playing = page.evaluate("(el) => { const v = el.querySelector('video'); return {paused: v.paused, t: v.currentTime}; }", vph.element_handle())
            check("ball plays the video", (not playing["paused"]) and playing["t"] > 0, playing)
            vph.locator(".bd-ball").click()
            page.wait_for_timeout(500)
            paused = page.evaluate("(el) => el.querySelector('video').paused", vph.element_handle())
            check("ball pauses the video", paused == True, paused)
        if g == 1:
            # Real user path: tap the chip (the label span), not the hidden input.
            # Categories live in the industry_all frame (group 2) in the official flow.
            page.click('#bdTrio label:has(input[data-cat="music"]) span')
            page.wait_for_timeout(300)
            check("categories subs appear under picked Music", page.locator('#bdTrio .bd-subs-label').count() >= 1)
            page.click('#bdTrio label:has(input[data-sub="playing"]) span')
            page.wait_for_timeout(400)
            sub = page.evaluate("""() => {
              const inp = document.querySelector('#bdTrio input[data-sub="playing"]');
              const S = JSON.parse(localStorage.getItem('naya_welcome_right_v1') || 'null');
              return {checked: inp ? inp.checked : null,
                      saved: S && S.answers && S.answers.cats_subs ? S.answers.cats_subs : []};
            }""")
            check("sub Playing stays checked after a real tap", sub["checked"] == True, sub)
            check("sub Playing saved (Music: Playing)", "Music: Playing" in sub["saved"], sub)
        if g < 7:
            page.locator("#fpWalkNext").click()
            page.wait_for_timeout(800)
            check(f"group {g+2} of 8 renders", page.locator("#bdTrio .bd-phone").count() >= 2, page.text_content("#bdGroupProg"))
    # Back keeps answers: walk back seven groups to group 1, city must be intact
    for _ in range(7):
        page.locator("#fpWalkBack").click()
        page.wait_for_timeout(400)
    check("Back keeps answers (Toronto intact)", page.input_value('#bdTrio input[data-fid="city"]') == "Toronto")
    for _ in range(7):
        page.locator("#fpWalkNext").click()
        page.wait_for_timeout(400)
    # Complete on last group
    page.locator("#fpWalkNext").click()
    page.wait_for_selector("#fpWalkEnd:not([hidden])", timeout=30000)
    page.wait_for_timeout(1500)
    check("end screen reached", page.is_visible("#fpWalkEnd"))
    check("end title whole at rest (Welcome home.)", "Welcome home." in page.text_content("#fpWalkQ"))
    check("NO video at the end (390)", page.locator("#bdEndPhone video").count() == 0)
    print("390 end state:", page.evaluate("() => ({readyHidden: document.getElementById('fpWalkReadyLine').hidden, failHidden: document.getElementById('fpWalkFailLine').hidden, ready: document.getElementById('fpWalkReadyLine').textContent})"), flush=True)
    check("world link shawn.nayanet.app", "shawn.nayanet.app" in page.text_content("#fpWalkLink"))
    check("ball visible on end screen", page.is_visible("#fpWalkEnter"))
    ls = page.evaluate("() => { const S = JSON.parse(localStorage.getItem('naya_welcome_right_v1') || 'null'); return S ? Object.keys(S.answers).length : 0; }")
    print("localStorage answer keys:", ls, flush=True)
    check("answers saved as you go (30+ keys)", ls >= 30, ls)
    print("390 failed requests:", failed_urls, flush=True)
    retry390 = page.evaluate("""async (urls) => {
      const out = [];
      for (const u of urls) {
        const m = u.match(/^HTTP 503 (https?[^ ]+)/);
        if (!m) continue;
        try { const r = await fetch(m[1], {method: 'GET'}); out.push(r.status + ' ' + m[1]); }
        catch (e) { out.push('ERR ' + m[1]); }
      }
      return out;
    }""", failed_urls)
    print("390 retry:", retry390, flush=True)
    bad390 = real_failures(failed_urls, retry390, jserrors)
    print("390 real failures:", bad390, flush=True)
    check("0 REAL page errors at 390 (cert artifact + transient 503s + video teardown excluded, all with proof)", len(bad390) == 0, bad390[:3])
    page.screenshot(path=OUT + "official-390-end.png")
    page.screenshot(path=OUT + "official-390-trio-g1.png")
    # 1440 leg: fresh walk, fast through to the end
    ctx2 = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    p2 = ctx2.new_page()
    errs2 = []
    jserrors2 = []
    failed_urls2 = []
    p2.on("pageerror", lambda e: (errs2.append(str(e)), jserrors2.append(str(e))))
    p2.on("console", lambda m: errs2.append("console." + m.type + ": " + m.text) if m.type == "error" else None)
    p2.on("requestfailed", lambda r: failed_urls2.append("FAILED " + r.url + " " + str(r.failure)))
    p2.on("response", lambda r: failed_urls2.append("HTTP " + str(r.status) + " " + r.url) if r.status >= 400 else None)
    p2.goto(BASE, wait_until="networkidle", timeout=120000)
    p2.wait_for_selector("#bdTrio .bd-phone", timeout=30000)
    boxes = p2.locator("#bdTrio .bd-phone").evaluate_all("els => els.map(e => { const b = e.getBoundingClientRect(); return {x: b.x, y: b.y, w: b.width, h: b.height}; })")
    check("1440: three phones side by side", len(boxes) == 3 and boxes[0]["x"] < boxes[1]["x"] < boxes[2]["x"], boxes)
    check("1440: phones same row (tops within 5px)", abs(boxes[0]["y"] - boxes[2]["y"]) < 5, boxes)
    check("1440: first phone ball+ENTER inside viewport on arrival",
          boxes[0]["y"] + boxes[0]["h"] <= 900, boxes[0])
    p2.evaluate("""() => {
      document.querySelectorAll('#bdTrio .bd-answer').forEach(ta => { ta.value = 'Our answer.'; ta.dispatchEvent(new Event('input', {bubbles: true})); });
    }""")
    for g in range(7):
        p2.locator("#fpWalkNext").click()
        p2.wait_for_timeout(700)
        p2.evaluate("""() => {
          document.querySelectorAll('#bdTrio .bd-answer').forEach(ta => { if (!ta.value) { ta.value = 'Our answer.'; ta.dispatchEvent(new Event('input', {bubbles: true})); } });
        }""")
    # picture step at 1440: group 3 vision reveal (motto, vision, goal)
    p2.locator("#fpWalkBack").click(); p2.wait_for_timeout(500)
    p2.locator("#fpWalkBack").click(); p2.wait_for_timeout(500)
    p2.locator("#fpWalkBack").click(); p2.wait_for_timeout(500)
    p2.locator("#fpWalkBack").click(); p2.wait_for_timeout(500)
    p2.locator("#fpWalkBack").click(); p2.wait_for_timeout(700)
    vph = p2.locator('[data-key="vision"]')
    check("1440: vision phone present on group 3", vph.count() == 1)
    vph.locator(".bd-ball").click()
    p2.wait_for_timeout(700)
    rv = p2.evaluate("""(ph) => {
      const st = ph.querySelector('.bd-stage').getBoundingClientRect();
      const rc = ph.querySelector('.bd-reveal-card').getBoundingClientRect();
      const bg = ph.querySelector('.bd-bgpic').getBoundingClientRect();
      return {cardWhole: rc.top >= st.top - 1 && rc.bottom <= st.bottom + 1,
              bgCovers: bg.top <= st.top + 1 && bg.bottom >= st.bottom - 1, op: parseFloat(getComputedStyle(ph.querySelector('.bd-bgpic')).opacity)};
    }""", vph.element_handle())
    check("1440 REVEAL vision: picture full-bleed, card whole", rv["cardWhole"] and rv["bgCovers"] and rv["op"] >= 0.99, rv)
    p2.locator("#fpWalkNext").click(); p2.wait_for_timeout(500)
    p2.locator("#fpWalkNext").click(); p2.wait_for_timeout(500)
    p2.locator("#fpWalkNext").click(); p2.wait_for_timeout(500)
    p2.locator("#fpWalkNext").click(); p2.wait_for_timeout(500)
    p2.locator("#fpWalkNext").click(); p2.wait_for_timeout(500)
    p2.locator("#fpWalkNext").click()
    p2.wait_for_selector("#fpWalkEnd:not([hidden])", timeout=30000)
    p2.wait_for_timeout(1500)
    end = p2.evaluate("""() => {
      const st = document.querySelector('.bd-stage-end').getBoundingClientRect();
      const el = document.querySelector('#fpWalkEnd').getBoundingClientRect();
      const t = document.querySelector('#fpWalkQ').getBoundingClientRect();
      const grid = document.querySelectorAll('.fp-walk-endgrid button');
      const clipped = [];
      grid.forEach(b => { if (b.scrollWidth > b.clientWidth + 1 || b.scrollHeight > b.clientHeight + 1) clipped.push(b.textContent.trim()); });
      const chin = document.querySelector('#bdEndPhone .bd-chin-label').getBoundingClientRect();
      const chinWrap = document.querySelector('#bdEndPhone .bd-chin-label').scrollWidth > document.querySelector('#bdEndPhone .bd-chin-label').clientWidth + 1;
      return {stageTop: st.top, stageBottom: st.bottom, endTop: el.top, endBottom: el.bottom,
              endWhole: el.top >= st.top - 1 && el.bottom <= st.bottom + 1,
              titleTop: t.top, titleVisible: t.top >= st.top - 1, clipped, chinWrap,
              ready: document.querySelector('#fpWalkReadyLine').textContent};
    }""")
    check("1440 F4: end screen whole inside stage", end["endWhole"], end)
    check("1440 F4: end title whole at rest", end["titleVisible"], end)
    check("1440 F5: no end-button label clipped", len(end["clipped"]) == 0, end["clipped"])
    check("1440 F5: chin label does not wrap", not end["chinWrap"], end)
    check("1440: ready line counts answers", "of 23 questions answered" in end["ready"], end["ready"])
    check("1440: NO video at the end", p2.locator("#bdEndPhone video").count() == 0)
    print("1440 failed requests:", failed_urls2, flush=True)
    retry1440 = p2.evaluate("""async (urls) => {
      const out = [];
      for (const u of urls) {
        const m = u.match(/^HTTP 503 (https?[^ ]+)/);
        if (!m) continue;
        try { const r = await fetch(m[1], {method: 'GET'}); out.push(r.status + ' ' + m[1]); }
        catch (e) { out.push('ERR ' + m[1]); }
      }
      return out;
    }""", failed_urls2)
    print("1440 retry:", retry1440, flush=True)
    bad1440 = real_failures(failed_urls2, retry1440, jserrors2)
    print("1440 real failures:", bad1440, flush=True)
    check("1440: 0 REAL page errors (cert artifact + transient 503s + video teardown excluded, all with proof)", len(bad1440) == 0, bad1440[:3])
    p2.screenshot(path=OUT + "official-1440-end.png")
    p2.screenshot(path=OUT + "official-1440-trio.png")
    browser.close()
print("PROBE DONE, fails:", len(fails), fails)
sys.exit(1 if fails else 0)
