import asyncio, json
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
        ' display=' + cs.display + ' vis=' + cs.visibility + ' op=' + cs.opacity +
        ' hit=' + (el === e ? 'SELF' : (el ? (el.id||el.tagName)+'.'+(el.className||'').toString().slice(0,30) : 'none')) +
        ' inView=' + (r.top>=0 && r.bottom<=innerHeight);
    }""", sel)

async def stack(pg, x, y):
    return await pg.evaluate("""([x,y]) => document.elementsFromPoint(x,y).map(e => {
      const r = e.getBoundingClientRect(); const cs = getComputedStyle(e);
      return (e.id||e.tagName) + '.' + (e.className||'').toString().slice(0,25) + ' pe=' + cs.pointerEvents + ' z=' + cs.zIndex + ' pos=' + cs.position + ' rect=' + Math.round(r.x) + ',' + Math.round(r.y) + ' ' + Math.round(r.width) + 'x' + Math.round(r.height);
    }).join(' | ')""", [x, y])

async def main():
    async with async_playwright() as p:
        b = await p.firefox.launch(headless=True)
        # PHONE portal fresh
        ctx = await b.new_context(viewport={'width':390,'height':844}, device_scale_factor=2)
        pg = await ctx.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(LOCAL + "welcome-staged.html", wait_until='load', timeout=60000)
        await pg.wait_for_timeout(2000)
        print("PHONE portal errors:", errs)
        print("scrollY:", await pg.evaluate("Math.round(scrollY)"), "docH:", await pg.evaluate("document.body.scrollHeight"))
        for sel in ['#userName', '#fpDeedSentence', '#fpDeedInfo', '#presence', '#fpEnterDeal', 'button.enter', '.portal', '.core', '.content', '#returningView', '#newAccountLine']:
            print(await geom(pg, sel))
        print("stack at input centre (195,263):", await stack(pg, 195, 263))
        box = await pg.evaluate("() => { const r = document.querySelector('#userName').getBoundingClientRect(); return {x: r.x+r.width/2, y: r.y+r.height/2}; }")
        print("input centre:", box)
        print("stack at input centre:", await stack(pg, int(box['x']), int(box['y'])))
        print("deed sentence rect/overflow:", await pg.evaluate("""() => { const e=document.querySelector('#fpDeedSentence'); const r=e.getBoundingClientRect(); const c=document.querySelector('.core').getBoundingClientRect(); return JSON.stringify({deed:[Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height)], core:[Math.round(c.x),Math.round(c.y),Math.round(c.width),Math.round(c.height)], scrollW:e.scrollWidth, clientW:e.clientWidth}); }"""))
        print("portal/core/content heights:", await pg.evaluate("""() => { const g=s=>{const e=document.querySelector(s); const r=e.getBoundingClientRect(); return s+' '+Math.round(r.width)+'x'+Math.round(r.height)+' y='+Math.round(r.y)+' scrollH='+e.scrollHeight+' clientH='+e.clientHeight;}; return [g('.portal'),g('.core'),g('.content'),g('#entryForm')].join(' | '); }"""))
        await pg.screenshot(path="/tmp/wsc-v2/phone-portal.png")
        await ctx.close()
        # DESKTOP portal fresh
        ctx = await b.new_context(viewport={'width':1280,'height':900})
        pg = await ctx.new_page()
        await pg.goto(LOCAL + "welcome-staged.html", wait_until='load', timeout=60000)
        await pg.wait_for_timeout(2000)
        for sel in ['#userName', '#fpDeedSentence', '#fpDeedInfo', '#fpEnterDeal', '#newAccountLine']:
            print(await geom(pg, sel))
        print("DESK deed vs core:", await pg.evaluate("""() => { const e=document.querySelector('#fpDeedSentence'); const r=e.getBoundingClientRect(); const c=document.querySelector('.core').getBoundingClientRect(); return JSON.stringify({deedTop:Math.round(r.top), deedBot:Math.round(r.bottom), coreTop:Math.round(c.top), coreBot:Math.round(c.bottom)}); }"""))
        await pg.screenshot(path="/tmp/wsc-v2/desk-portal.png")
        await ctx.close()
        # WALK load desktop + phone
        for w, h, tag in [(1280,900,'desk'), (390,844,'phone')]:
            ctx = await b.new_context(viewport={'width':w,'height':h})
            pg = await ctx.new_page()
            await pg.goto(LOCAL + "welcome-staged.html?walk=1&name=Shawn&alias=shawn", wait_until='load', timeout=60000)
            await pg.wait_for_timeout(2500)
            print(tag.upper(), "walk load:", await pg.evaluate("""() => { const q=document.querySelector('#fpWalkQ'); const r=q? q.getBoundingClientRect():null; const w=document.querySelector('#fpWalk'); const wr=w? w.getBoundingClientRect():null; return JSON.stringify({scrollY:Math.round(scrollY), docH:document.body.scrollHeight, q1:r?[Math.round(r.top),Math.round(r.bottom)]:null, walk:[Math.round(wr.top),Math.round(wr.bottom)], vh:innerHeight}); }"""))
            await ctx.close()
        await b.close()

asyncio.run(main())
