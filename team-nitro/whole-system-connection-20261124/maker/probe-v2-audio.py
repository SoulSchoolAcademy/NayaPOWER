import asyncio
from playwright.async_api import async_playwright

LOCAL = "http://127.0.0.1:8898/"

async def main():
    async with async_playwright() as p:
        b = await p.firefox.launch(headless=True)
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
        print("cover active:", await pg.evaluate("document.querySelector('#screen-cover').classList.contains('active')"))
        info = await pg.evaluate("""() => {
          const a = document.querySelector('#welcomeAudio');
          const r = a.getBoundingClientRect();
          const pts = [[r.x+15, r.y+r.height/2], [r.x+22, r.y+r.height/2], [r.x+30, r.y+r.height/2], [r.x+r.width/2, r.y+r.height/2]];
          return JSON.stringify({rect: [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)],
            readyState: a.readyState, paused: a.paused, muted: a.muted, volume: a.volume,
            ctxState: (window.__fpCtx ? window.__fpCtx.state : 'no ctx ref'),
            hits: pts.map(([x,y]) => { const el = document.elementFromPoint(x,y); return Math.round(x)+','+Math.round(y)+'='+(el ? (el.id||el.tagName+'.'+(el.className||'').toString().slice(0,20)) : 'none'); })});
        }""")
        print(info)
        # try the real mouse click on the play button, several x offsets
        for dx in (12, 20, 28):
            box = await pg.evaluate("() => { const r=document.querySelector('#welcomeAudio').getBoundingClientRect(); return {x:r.x, y:r.y, h:r.height}; }")
            await pg.mouse.click(box['x'] + dx, box['y'] + box['h']/2)
            await pg.wait_for_timeout(1200)
            st = await pg.evaluate("() => { const a=document.querySelector('#welcomeAudio'); return JSON.stringify({dx: 'n/a', paused: a.paused, time: a.currentTime.toFixed(2), playing: window.audioPlaying}); }")
            print(f"click dx={dx}:", st)
            if 'false' in st and '"paused":false' in st:
                break
            await pg.evaluate("() => { const a=document.querySelector('#welcomeAudio'); if(!a.paused) a.pause(); }")
            await pg.wait_for_timeout(300)
        # direct play() call: does the element allow playback at all?
        print("direct play():", await pg.evaluate("""async () => {
          const a = document.querySelector('#welcomeAudio');
          try {
            await a.play();
            await new Promise(r => setTimeout(r, 1500));
            return JSON.stringify({ok: true, paused: a.paused, time: a.currentTime.toFixed(2), audioPlaying: window.audioPlaying,
              analyser: !!window.analyser});
          } catch (e) { return JSON.stringify({ok: false, err: e.name + ': ' + e.message}); }
        }"""))
        await pg.wait_for_timeout(1500)
        print("analyser after direct play:", await pg.evaluate("""() => {
          if (!window.analyser || !window.freqData) return 'no analyser';
          window.analyser.getByteFrequencyData(window.freqData);
          let sum = 0; for (let i=0;i<48;i++) sum += window.freqData[i];
          return JSON.stringify({audioPlaying: window.audioPlaying, freqSum48: sum, paused: document.querySelector('#welcomeAudio').paused, time: document.querySelector('#welcomeAudio').currentTime.toFixed(2)});
        }"""))
        print("errors:", errs)
        await b.close()

asyncio.run(main())
