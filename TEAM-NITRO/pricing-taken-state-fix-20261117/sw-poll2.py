from playwright.sync_api import sync_playwright
FREE="https://naya-pricing-free-staging.nayapower.workers.dev/free"
with sync_playwright() as pw:
    b=pw.chromium.launch(headless=True, proxy={"server":"http://127.0.0.1:18080"})
    ctx=b.new_context(viewport={"width":390,"height":844}, ignore_https_errors=True)
    page=ctx.new_page()
    reqs=[]
    page.on("request", lambda r: reqs.append(r.url))
    page.on("response", lambda r: reqs.append(f"RESP {r.status} {r.url}"))
    page.goto(FREE, wait_until="commit", timeout=60000)
    hits=[]
    for i in range(60):
        page.wait_for_timeout(100)
        r=page.evaluate("navigator.serviceWorker.getRegistration().then(x=>x?x.scope:null)")
        sws=[w.url for w in ctx.service_workers]
        if r or sws:
            hits.append((i, r, sws))
    print("transient registration hits (100ms polls, 6s):", hits)
    print("sw.js in requests:", [u for u in reqs if 'sw.js' in u])
    print("n requests:", len(reqs))
    b.close()
