import asyncio
from playwright.async_api import async_playwright

LOCAL = "http://127.0.0.1:8898/"

async def main():
    async with async_playwright() as p:
        b = await p.firefox.launch(headless=True)
        ctx = await b.new_context(viewport={'width':1280,'height':900})
        pg = await ctx.new_page()
        await pg.goto(LOCAL + "agreement.html", wait_until='domcontentloaded', timeout=90000)
        await pg.wait_for_timeout(2500)
        await pg.click('#fpChoiceDeck')
        await pg.wait_for_timeout(1000)
        await pg.click('#btnBack')
        await pg.wait_for_timeout(8000)
        print(await pg.evaluate("""() => {
          const q = s => { const e = document.querySelector(s); if (!e) return s + ' MISSING';
            const r = e.getBoundingClientRect(); const cs = getComputedStyle(e);
            return s + ' ' + Math.round(r.width) + 'x' + Math.round(r.height) + ' @' + Math.round(r.x) + ',' + Math.round(r.y) +
              ' op=' + cs.opacity + ' vis=' + cs.visibility + ' disp=' + cs.display; };
          const fac = document.querySelector('#videoFacade');
          const img = fac ? fac.querySelector('img') : null;
          const shell = document.querySelector('#videoShell');
          return JSON.stringify({
            art: q('.pm-art'), side: q('.pm-side'), facade: q('#videoFacade'),
            facadeImg: img ? (img.id + ' srcLen=' + (img.src||'').length + ' ' + Math.round(img.getBoundingClientRect().width) + 'x' + Math.round(img.getBoundingClientRect().height)) : 'none',
            shell: q('#videoShell'), iframe: shell ? !!shell.querySelector('iframe') : false,
            audio: q('#welcomeAudio'), orb: q('#voice'),
            screenOp: getComputedStyle(document.querySelector('#screen-cover')).opacity
          }, null, 1);
        }"""))
        await pg.screenshot(path="/tmp/wsc-v2/agree-cover-desk-2.png")
        await b.close()

asyncio.run(main())
