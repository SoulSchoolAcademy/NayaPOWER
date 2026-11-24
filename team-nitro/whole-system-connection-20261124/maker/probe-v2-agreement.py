import asyncio, sys
from playwright.async_api import async_playwright

LOCAL = "http://127.0.0.1:8898/"
RUN = sys.argv[1] if len(sys.argv) > 1 else "ABCDEF"  # e.g. "ABC" or "DEF"

async def held_measure(pg, btn_sel, target_sel=None):
    box = await pg.evaluate("""(sel) => {
      const e = document.querySelector(sel);
      if (!e) return null;
      const r = e.getBoundingClientRect();
      return {x: r.x + r.width/2, y: r.y + r.height/2};
    }""", btn_sel)
    if not box:
        return btn_sel + " MISSING"
    await pg.mouse.move(box['x'], box['y'])
    await pg.mouse.down()
    await pg.wait_for_timeout(1200)
    res = await pg.evaluate("""([btn, tgt]) => {
      const b = document.querySelector(btn);
      const e = tgt ? document.querySelector(tgt) : b;
      const cs = getComputedStyle(e);
      return JSON.stringify({btnActive: b.matches(':active'), transform: cs.transform, filter: cs.filter});
    }""", [btn_sel, target_sel])
    await pg.mouse.up()
    await pg.wait_for_timeout(300)
    return btn_sel + " HELD: " + res

async def main():
    async with async_playwright() as p:
        b = await p.firefox.launch(headless=True)
        if 'A' in RUN:
            for url, tag in [(LOCAL + "agreement.html", "plain"),
                             (LOCAL + "agreement.html?view=deck", "deck"),
                             (LOCAL + "agreement.html?view=letter", "letter")]:
                ctx = await b.new_context(viewport={'width':1280,'height':900})
                pg = await ctx.new_page()
                errs = []
                pg.on('pageerror', lambda e: errs.append(str(e)))
                await pg.goto(url, wait_until='domcontentloaded', timeout=90000)
                await pg.wait_for_timeout(2500)
                print(tag, "load errors:", errs, flush=True)
                await ctx.close()
        if 'B' in RUN:
            ctx = await b.new_context(viewport={'width':1280,'height':900})
            pg = await ctx.new_page()
            await pg.goto(LOCAL + "agreement.html", wait_until='domcontentloaded', timeout=90000)
            await pg.wait_for_timeout(2500)
            print("pills:", await pg.evaluate("""() => ['#fpChoiceDeck','#fpChoiceLetter'].map(s => {
              const e = document.querySelector(s); const r = e.getBoundingClientRect();
              return s + ' ' + Math.round(r.width) + 'x' + Math.round(r.height);
            }).join(' | ')"""), flush=True)
            print("play disc:", await held_measure(pg, '#fpChoicePlay', '#fpChoicePlay .pm-play-disc'), flush=True)
            await ctx.close()
        if 'C' in RUN:
            ctx = await b.new_context(viewport={'width':1280,'height':900})
            pg = await ctx.new_page()
            errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            await pg.goto(LOCAL + "agreement.html", wait_until='domcontentloaded', timeout=90000)
            await pg.wait_for_timeout(2500)
            await pg.click('#fpChoiceDeck')
            await pg.wait_for_timeout(1200)
            st0 = await pg.evaluate("document.querySelector('#slideStation').innerText")
            await pg.click('#btnForward')
            await pg.wait_for_timeout(800)
            st1 = await pg.evaluate("document.querySelector('#slideStation').innerText")
            await pg.click('#btnForward')
            await pg.wait_for_timeout(800)
            st2 = await pg.evaluate("document.querySelector('#slideStation').innerText")
            print("forward nav by real clicks:", st0, "->", st1, "->", st2, flush=True)
            # jump to slide 27 in the probe (each slide change decodes a big
            # image; the checker already proved the 26-click walk in v1)
            await pg.evaluate("() => { current = 26; renderSlide(); }")
            await pg.wait_for_timeout(2000)
            print("slide 27 station:", await pg.evaluate("document.querySelector('#slideStation') && document.querySelector('#slideStation').innerText"), flush=True)
            print("final row:", await pg.evaluate("!!document.querySelector('#fpFinalRow')"),
                  "| deck agree:", await pg.evaluate("() => { const a=document.querySelector('[data-fp-agree]'); return a ? a.innerText : 'MISSING'; }"), flush=True)
            links = await pg.evaluate("() => [...document.querySelectorAll('[data-final]')].map(e => e.getAttribute('data-final'))")
            print("final links:", links, flush=True)
            ok = 0
            for key in links:
                await pg.evaluate("""(key) => {
                  [...document.querySelectorAll('[data-final]')].find(e => e.getAttribute('data-final') === key).click();
                }""", key)
                await pg.wait_for_timeout(500)
                st = await pg.evaluate("() => ({hidden: document.querySelector('#fpFinalReader').hidden, title: document.querySelector('#fpFinalTitle').innerText, len: document.querySelector('#fpFinalBody').innerText.length})")
                await pg.click('#fpFinalClose')
                await pg.wait_for_timeout(400)
                closed = await pg.evaluate("document.querySelector('#fpFinalReader').hidden")
                print(" ", key, "open:", st, "close->hidden:", closed, flush=True)
                if st['hidden'] is False and closed:
                    ok += 1
            print(f"FINAL READER: {ok}/8 open+close", flush=True)
            print("deck agree press:", await held_measure(pg, '[data-fp-agree]'), flush=True)
            await pg.wait_for_timeout(400)
            print("deck agree N hold (after press-click):", await pg.evaluate("!!document.querySelector('#fpNHold')"), flush=True)
            await pg.wait_for_timeout(2500)
            print("after deck agree, URL:", pg.url, flush=True)
            print("live portal userName focused:", await pg.evaluate("document.activeElement && document.activeElement.id"), flush=True)
            print("deck errors:", errs, flush=True)
            await ctx.close()

        if 'D' in RUN:
            ctx = await b.new_context(viewport={'width':1280,'height':900})
            pg = await ctx.new_page()
            errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            await pg.goto(LOCAL + "agreement.html?view=letter", wait_until='domcontentloaded', timeout=90000)
            await pg.wait_for_timeout(2500)
            for i in range(20):
                vis = await pg.evaluate("() => { const a = document.querySelector('[data-legal-agree]'); return a && !a.hidden; }")
                if vis:
                    break
                nxt = await pg.query_selector('[data-legal-next]:not([hidden])')
                if not nxt:
                    print("letter: no Next visible at beat", i, flush=True)
                    break
                await nxt.click()
                await pg.wait_for_timeout(400)
            print("letter agree visible:", await pg.evaluate("() => { const a = document.querySelector('[data-legal-agree]'); return a && !a.hidden && a.innerText; }"), flush=True)
            print("letter agree press:", await held_measure(pg, '[data-legal-agree]'), flush=True)
            # (the press measurement's mouse-up IS the click: goToPortal runs,
            # the N hold covers the screen, then it navigates in place)
            await pg.wait_for_timeout(800)
            print("letter agree N hold:", await pg.evaluate("!!document.querySelector('#fpNHold')"), flush=True)
            try:
                await pg.wait_for_url("**nayanet.app/**", timeout=30000)
            except Exception:
                print("letter nav wait timed out; URL now:", pg.url, flush=True)
            await pg.wait_for_timeout(3000)
            print("after letter agree, URL:", pg.url, flush=True)
            print("live portal userName focused:", await pg.evaluate("document.activeElement && document.activeElement.id"), flush=True)
            print("letter errors:", errs, flush=True)
            await ctx.close()
        if 'E' in RUN:
            ctx = await b.new_context(viewport={'width':390,'height':844})
            pg = await ctx.new_page()
            await pg.goto(LOCAL + "agreement.html", wait_until='domcontentloaded', timeout=90000)
            await pg.wait_for_timeout(2500)
            print("daybar title:", await pg.evaluate("""() => { const e=document.querySelector('#tbTitle'); const cs=getComputedStyle(e);
              return JSON.stringify({text: e.innerText, ws: cs.whiteSpace, scrollW: e.scrollWidth, clientW: e.clientWidth, h: Math.round(e.getBoundingClientRect().height)}); }"""), flush=True)
            await pg.screenshot(path="/tmp/wsc-v2/agree-phone-daybar.png")
            await ctx.close()
        if 'F' in RUN:
            ctx = await b.new_context(viewport={'width':1280,'height':900})
            pg = await ctx.new_page()
            errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            await pg.goto(LOCAL + "agreement.html", wait_until='domcontentloaded', timeout=90000)
            await pg.wait_for_timeout(2500)
            await pg.click('#fpChoiceDeck')
            await pg.wait_for_timeout(1000)
            await pg.click('#btnBack')
            await pg.wait_for_timeout(1200)
            print("cover active:", await pg.evaluate("document.querySelector('#screen-cover').classList.contains('active')"), flush=True)
            print("frame:", await pg.evaluate("""() => {
              const art = document.querySelector('.pm-art'); const side = document.querySelector('.pm-side');
              const a = art.getBoundingClientRect(), s = side.getBoundingClientRect();
              return JSON.stringify({videoLeft: Math.round(a.x), videoW: Math.round(a.width), audioLeft: Math.round(s.x), audioW: Math.round(s.width),
                videoFirst: a.x < s.x, facade: !!document.querySelector('#videoFacade'), audioEl: !!document.querySelector('#welcomeAudio'),
                ytLink: (document.querySelector('.pm-yt-link')||{}).href || null});
            }"""), flush=True)
            await pg.screenshot(path="/tmp/wsc-v2/agree-cover-desk.png")
            audio_box = await pg.evaluate("() => { const e=document.querySelector('#welcomeAudio'); const r=e.getBoundingClientRect(); return {x: r.x, y: r.y, w: r.width, h: r.height}; }")
            print("audio el:", audio_box, flush=True)
            await pg.mouse.click(audio_box['x'] + 22, audio_box['y'] + audio_box['h']/2)
            await pg.wait_for_timeout(1000)
            print("audio state after click:", await pg.evaluate("() => { const a=document.querySelector('#welcomeAudio'); return JSON.stringify({paused: a.paused, time: a.currentTime, dur: a.duration, srcSet: !!a.src}); }"), flush=True)
            await pg.wait_for_timeout(3000)
            print("analyser live:", await pg.evaluate("""() => {
              let s1 = null;
              if (window.analyser && window.freqData){
                window.analyser.getByteFrequencyData(window.freqData);
                s1 = 0; for (let i=0;i<48;i++) s1 += window.freqData[i];
              }
              return JSON.stringify({audioPlaying: window.audioPlaying, analyser: !!window.analyser, freqSum48: s1,
                paused: document.querySelector('#welcomeAudio').paused, time: document.querySelector('#welcomeAudio').currentTime});
            }"""), flush=True)
            await pg.wait_for_timeout(2000)
            print("analyser live (2nd sample):", await pg.evaluate("""() => {
              if (!window.analyser || !window.freqData) return 'no analyser';
              window.analyser.getByteFrequencyData(window.freqData);
              let sum = 0; for (let i=0;i<48;i++) sum += window.freqData[i];
              return JSON.stringify({audioPlaying: window.audioPlaying, freqSum48: sum, paused: document.querySelector('#welcomeAudio').paused});
            }"""), flush=True)
            print("cover errors:", errs, flush=True)
        await b.close()

asyncio.run(main())
