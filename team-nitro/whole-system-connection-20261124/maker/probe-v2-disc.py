import asyncio
from playwright.async_api import async_playwright

LOCAL = "http://127.0.0.1:8898/"

async def main():
    async with async_playwright() as p:
        b = await p.firefox.launch(headless=True)
        ctx = await b.new_context(viewport={'width':1280,'height':900})
        pg = await ctx.new_page()
        await pg.goto(LOCAL + "agreement.html", wait_until='load', timeout=90000)
        await pg.wait_for_timeout(2500)
        print(await pg.evaluate("""() => {
          const d = document.querySelector('#fpChoicePlay .pm-play-disc');
          const r = d.getBoundingClientRect();
          const cx = r.x + r.width/2, cy = r.y + r.height/2;
          const stack = document.elementsFromPoint(cx, cy).map(e => (e.id||e.tagName) + '.' + (e.className||'').toString().slice(0,40)).join(' | ');
          const btn = document.querySelector('#fpChoicePlay');
          return JSON.stringify({discRect: [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)],
            stack, btnPe: getComputedStyle(btn).pointerEvents, discPe: getComputedStyle(d).pointerEvents});
        }"""))
        box = await pg.evaluate("() => { const r = document.querySelector('#fpChoicePlay .pm-play-disc').getBoundingClientRect(); return {x: r.x+r.width/2, y: r.y+r.height/2}; }")
        await pg.mouse.move(box['x'], box['y'])
        await pg.mouse.down()
        await pg.wait_for_timeout(500)
        print("while held:", await pg.evaluate("""() => {
          const btn = document.querySelector('#fpChoicePlay');
          const d = btn.querySelector('.pm-play-disc');
          const cs = getComputedStyle(d);
          return JSON.stringify({btnActive: btn.matches(':active'), discActive: d.matches(':active'),
            transform: cs.transform, filter: cs.filter});
        }"""))
        await pg.mouse.up()
        await pg.wait_for_timeout(300)
        print("after release, screen:", await pg.evaluate("document.querySelector('.screen.active') && document.querySelector('.screen.active').id"))
        await b.close()

asyncio.run(main())
