import asyncio
from playwright.async_api import async_playwright

LOCAL = "http://127.0.0.1:8898/"

async def main():
    async with async_playwright() as p:
        b = await p.firefox.launch(headless=True)
        ctx = await b.new_context(viewport={'width':390,'height':844})
        pg = await ctx.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append(f"console.{m.type}: {m.text}") if m.type == 'error' else None)
        await pg.goto(LOCAL + "welcome-staged.html", wait_until='load', timeout=60000)
        await pg.wait_for_timeout(1500)
        print("errors:", errs)
        print(await pg.evaluate("""() => {
          const s = document.querySelector('#fpDeedSentence');
          const stages = [...document.querySelectorAll('.stage')].map(e => {
            const r = e.getBoundingClientRect();
            return e.tagName + ' rect=' + Math.round(r.x) + ',' + Math.round(r.y) + ' ' + Math.round(r.width) + 'x' + Math.round(r.height) + ' kids=' + [...e.children].map(c=>c.tagName+'.'+(c.className||'').toString().slice(0,20)).join(',');
          });
          const scripts = [...document.querySelectorAll('script')].filter(sc => sc.textContent.includes('fix 1')).length;
          return JSON.stringify({
            mq480: matchMedia('(max-width:480px)').matches,
            innerWidth: innerWidth,
            deedParent: s.parentElement.tagName + '.' + (s.parentElement.className||''),
            stageCount: document.querySelectorAll('.stage').length,
            stages,
            v2scripts: scripts,
            portalKids: document.querySelector('.portal') ? 'portal found' : 'no portal',
          }, null, 1);
        }"""))
        await b.close()

asyncio.run(main())
