import asyncio
from playwright.async_api import async_playwright

LOCAL = "http://127.0.0.1:8898/"
PROXY = 'http://127.0.0.1:18080'

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
        ' color=' + cs.color + ' fontSize=' + cs.fontSize + ' weight=' + cs.fontWeight +
        ' hit=' + (el === e ? 'SELF' : (el ? (el.id||el.tagName) : 'none')) +
        ' inView=' + (r.top>=0 && r.bottom<=innerHeight) + ' text=' + JSON.stringify((e.innerText||'').slice(0,60));
    }""", sel)

async def taken_run(pg, w, h, tag):
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    await pg.goto(LOCAL + "identity.html?name=Shawn", wait_until='load', timeout=60000)
    await pg.wait_for_timeout(2500)
    nn = await pg.query_selector("text=NOT NOW")
    if nn:
        await nn.click()
        print(tag, "dismissed install modal")
        await pg.wait_for_timeout(500)
    print(tag, "errors:", errs)
    await pg.click('#aliasInput')
    await pg.type('#aliasInput', 'shawn', delay=100)
    await pg.wait_for_timeout(3500)
    print(tag, "alias state after typing:", await pg.evaluate("document.querySelector('#aliasStatus').getAttribute('data-state')"))
    print(tag, await geom(pg, '#aliasStatus'))
    # the green note + This-is-me appear on the claim attempt (ENTER)
    await pg.click('#enterBtn')
    await pg.wait_for_timeout(4000)
    print(tag, await geom(pg, '#aliasStatus'))
    print(tag, await geom(pg, '#hubNote'))
    print(tag, await geom(pg, '#fpThisIsMe'))
    await pg.screenshot(path=f"/tmp/wsc-v2/identity-taken-{tag.lower()}.png")
    btn = await pg.query_selector('#fpThisIsMe')
    if btn:
        await btn.click()
        await pg.wait_for_timeout(2500)
        print(tag, "after This-is-me URL:", pg.url)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True, proxy={'server': PROXY, 'bypass': '127.0.0.1,localhost'})
        ctx = await b.new_context(viewport={'width':1280,'height':900}, ignore_https_errors=True)
        pg = await ctx.new_page()
        await taken_run(pg, 1280, 900, 'DESK')
        await ctx.close()
        ctx = await b.new_context(viewport={'width':390,'height':844}, ignore_https_errors=True)
        pg = await ctx.new_page()
        await taken_run(pg, 390, 844, 'PHONE')
        await ctx.close()
        await b.close()

asyncio.run(main())
