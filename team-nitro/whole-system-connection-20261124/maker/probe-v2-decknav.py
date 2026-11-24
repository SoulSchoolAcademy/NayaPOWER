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
        await pg.wait_for_timeout(1200)
        await pg.evaluate("() => { current = 26; renderSlide(); }")
        await pg.wait_for_timeout(2000)
        await pg.click('[data-fp-agree]')
        print("clicked agree; waiting for live navigation...", flush=True)
        try:
            await pg.wait_for_url("**nayanet.app/**", timeout=30000)
        except Exception as e:
            print("wait_for_url timed out; current URL:", pg.url, flush=True)
        await pg.wait_for_timeout(3000)
        print("final URL:", pg.url, flush=True)
        print("activeElement:", await pg.evaluate("document.activeElement && document.activeElement.id"), flush=True)
        print("userName visible:", await pg.evaluate("() => { const e=document.querySelector('#userName'); if(!e) return 'no input on this page'; const r=e.getBoundingClientRect(); return JSON.stringify({x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height),ph:e.placeholder}); }"), flush=True)
        print("errors:", errs, flush=True)
        await b.close()

asyncio.run(main())
