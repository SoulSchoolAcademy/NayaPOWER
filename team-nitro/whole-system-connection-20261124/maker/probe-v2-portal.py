import asyncio
from playwright.async_api import async_playwright

LOCAL = "http://127.0.0.1:8898/"

async def geom(pg, sel):
    return await pg.evaluate("""(sel) => {
      const e = document.querySelector(sel);
      if (!e) return sel + ' MISSING';
      const r = e.getBoundingClientRect();
      const cs = getComputedStyle(e);
      const cx = Math.min(innerWidth-1, Math.max(0, r.x + r.width/2));
      const cy = Math.min(innerHeight-1, Math.max(0, r.y + r.height/2));
      const el = document.elementFromPoint(cx, cy);
      return sel + ' rect x=' + Math.round(r.x) + ' y=' + Math.round(r.y) + ' w=' + Math.round(r.width) + ' h=' + Math.round(r.height) +
        ' hit=' + (el === e ? 'SELF' : (el ? (el.id||el.tagName)+'.'+(el.className||'').toString().slice(0,30) : 'none')) +
        ' inView=' + (r.top>=0 && r.bottom<=innerHeight) +
        ' scrollH=' + e.scrollHeight + ' clientH=' + e.clientHeight;
    }""", sel)

async def main():
    async with async_playwright() as p:
        b = await p.firefox.launch(headless=True)
        # ---------- PHONE portal ----------
        ctx = await b.new_context(viewport={'width':390,'height':844}, device_scale_factor=2)
        pg = await ctx.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(LOCAL + "welcome-staged.html", wait_until='load', timeout=60000)
        await pg.wait_for_timeout(2000)
        print("PHONE errors:", errs)
        for sel in ['#userName', '#presence', '#fpDeedSentence', '#fpDeedInfo', 'button.enter', '#fpEnterDeal']:
            print(await geom(pg, sel))
        print("presence text:", await pg.evaluate("document.querySelector('#presence').innerText"),
              "| single line (h<=24):", await pg.evaluate("() => { const e=document.querySelector('#presence'); const r=e.getBoundingClientRect(); return Math.round(r.height) + ' scrollW=' + e.scrollWidth + ' clientW=' + e.clientWidth; }"))
        deed_txt = await pg.evaluate("document.querySelector('#fpDeedSentence').innerText")
        print("deed text starts:", deed_txt[:80])
        print("deed whole (bottom<=844, no internal scroll):", await pg.evaluate("() => { const e=document.querySelector('#fpDeedSentence'); const r=e.getBoundingClientRect(); return r.bottom<=844 && e.scrollHeight<=e.clientHeight+2; }"))
        print("deed parent:", await pg.evaluate("document.querySelector('#fpDeedSentence').parentElement.className + '.' + document.querySelector('#fpDeedSentence').parentElement.tagName"))
        print("portal size:", await pg.evaluate("() => { const r=document.querySelector('.portal').getBoundingClientRect(); return Math.round(r.width)+'x'+Math.round(r.height); }"))
        print("footer label:", await pg.evaluate("document.querySelector('#fpEnterDeal').innerText"))
        # click into the name box for real, type
        await pg.mouse.click(195, 330)
        await pg.wait_for_timeout(600)
        print("activeElement after mouse click near input:", await pg.evaluate("document.activeElement && (document.activeElement.id||document.activeElement.tagName)"))
        box = await pg.evaluate("() => { const r = document.querySelector('#userName').getBoundingClientRect(); return {x: r.x+r.width/2, y: r.y+r.height/2}; }")
        await pg.mouse.click(box['x'], box['y'])
        await pg.wait_for_timeout(500)
        print("activeElement after click at input centre:", await pg.evaluate("document.activeElement && document.activeElement.id"))
        await pg.keyboard.type('Shawn', delay=60)
        await pg.wait_for_timeout(1200)
        print("typed value:", await pg.evaluate("document.querySelector('#userName').value"))
        # deed reader via the i button
        ib = await pg.evaluate("() => { const r = document.querySelector('#fpDeedInfo').getBoundingClientRect(); return {x: r.x+r.width/2, y: r.y+r.height/2}; }")
        await pg.mouse.click(ib['x'], ib['y'])
        await pg.wait_for_timeout(800)
        print("reader open:", await pg.evaluate("!document.querySelector('#fpDeedReader').hidden"),
              "| count:", await pg.evaluate("document.querySelector('#fpDeedCount').innerText"),
              "| reader rect:", await pg.evaluate("() => { const r=document.querySelector('#fpDeedReader').getBoundingClientRect(); return Math.round(r.top)+'-'+Math.round(r.bottom)+' vh='+innerHeight; }"))
        await pg.screenshot(path="/tmp/wsc-v2/phone-portal-v2.png")
        await pg.screenshot(path="/tmp/wsc-v2/phone-portal-reader-v2.png")
        await ctx.close()
        # ---------- DESKTOP portal ----------
        ctx = await b.new_context(viewport={'width':1280,'height':900})
        pg = await ctx.new_page()
        await pg.goto(LOCAL + "welcome-staged.html", wait_until='load', timeout=60000)
        await pg.wait_for_timeout(2000)
        for sel in ['#userName', '#presence', '#fpDeedSentence', '#fpDeedInfo', '#fpEnterDeal']:
            print(await geom(pg, sel))
        print("DESK deed inside core:", await pg.evaluate("() => { const d=document.querySelector('#fpDeedSentence').getBoundingClientRect(); const c=document.querySelector('.core').getBoundingClientRect(); return 'deed '+Math.round(d.top)+'-'+Math.round(d.bottom)+' core '+Math.round(c.top)+'-'+Math.round(c.bottom); }"))
        print("DESK deed parent:", await pg.evaluate("document.querySelector('#fpDeedSentence').parentElement.className"))
        await pg.screenshot(path="/tmp/wsc-v2/desk-portal-v2.png")
        # returning state on desktop
        await pg.evaluate("() => { localStorage.setItem('nayanet_smart_alias','shawn'); localStorage.setItem('nayanet_smart_name','Shawn'); }")
        await pg.goto(LOCAL + "welcome-staged.html", wait_until='load', timeout=60000)
        await pg.wait_for_timeout(2000)
        print("RETURNING desk: deed hidden:", await pg.evaluate("document.querySelector('#fpDeedSentence').hidden"),
              "| greeting:", await pg.evaluate("document.querySelector('#returningGreet').innerText"))
        print("RETURNING newAccountLine:", await geom(pg, '#newAccountLine'))
        print("RETURNING newAccount inside core:", await pg.evaluate("() => { const d=document.querySelector('#newAccountLine').getBoundingClientRect(); const c=document.querySelector('.core').getBoundingClientRect(); return 'line '+Math.round(d.top)+'-'+Math.round(d.bottom)+' core '+Math.round(c.top)+'-'+Math.round(c.bottom); }"))
        await pg.screenshot(path="/tmp/wsc-v2/desk-portal-returning-v2.png")
        await ctx.close()
        # ---------- WALK desktop + phone ----------
        for w, h, tag in [(1280,900,'DESK'), (390,844,'PHONE')]:
            ctx = await b.new_context(viewport={'width':w,'height':h})
            pg = await ctx.new_page()
            await pg.goto(LOCAL + "welcome-staged.html?walk=1&name=Shawn&alias=shawn", wait_until='load', timeout=60000)
            await pg.wait_for_timeout(2500)
            print(tag, "walk load:", await pg.evaluate("() => { const q=document.querySelector('#fpWalkQ'); const r=q.getBoundingClientRect(); const w=document.querySelector('#fpWalk').getBoundingClientRect(); return JSON.stringify({scrollY:Math.round(scrollY), loginHidden: document.querySelector('.fp-login').hidden, loginDisplay: getComputedStyle(document.querySelector('.fp-login')).display, q1:[Math.round(r.top),Math.round(r.bottom)], walkTop:Math.round(w.top), vh:innerHeight}); }"))
            for n in range(15):
                btn = await pg.query_selector('#fpWalkEnter')
                if not btn: break
                await btn.click()
                await pg.wait_for_timeout(700)
            await pg.wait_for_timeout(1500)
            print(tag, "end slide:", await pg.evaluate("() => { const t=document.body.innerText; const m=t.match(/Welcome home\\./g); return JSON.stringify({welcomeHomeCount: m?m.length:0, world: (document.querySelector('#fpWalkWorld')||{getBoundingClientRect:()=>({top:-1,bottom:-1})}).getBoundingClientRect().top, pricing: (document.querySelector('#fpWalkPricing')||{getBoundingClientRect:()=>({top:-1,bottom:-1})}).getBoundingClientRect().bottom, vh: innerHeight}); }"))
            for sel in ['#fpWalkWorld', '#fpWalkPricing']:
                print(tag, await geom(pg, sel))
            await pg.screenshot(path=f"/tmp/wsc-v2/walk-end-{tag.lower()}-v2.png")
            await ctx.close()
        await b.close()

asyncio.run(main())
