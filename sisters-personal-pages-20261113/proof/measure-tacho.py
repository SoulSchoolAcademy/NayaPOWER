import json, hashlib
from playwright.sync_api import sync_playwright
JS = """() => {
  const m = document.querySelector('#tn-tacho-mount');
  const teethMount = m ? m.querySelectorAll('.tn-gear-tooth').length : -1;
  const teethDoc = document.querySelectorAll('.tn-gear-tooth').length;
  const needle = document.querySelector('.tn-tacho-needle');
  const t1 = needle ? getComputedStyle(needle).transform : 'none';
  return new Promise(res => {
    requestAnimationFrame(() => requestAnimationFrame(() => {
      const t2 = needle ? getComputedStyle(needle).transform : 'none';
      res({teeth_in_mount: teethMount, teeth_in_doc: teethDoc,
           needle_in_dom: !!needle,
           needle_transition: needle ? getComputedStyle(needle).transition : 'none',
           needle_moved: t1 !== t2, mount_html_len: m ? m.innerHTML.length : 0});
    }));
  });
}"""
out = {}
with sync_playwright() as pw:
    br = pw.firefox.launch()
    for label, url, f in [("live", "https://nayanet.app/personal", "/home/hatch/workspace/team-nitro/sisters-personal-pages-20261113/proof/personal-live.html"),
                          ("staged", "http://127.0.0.1:8901/pages/sophia/sophia", "/home/hatch/workspace/team-nitro/sisters-personal-pages-20261113/proof/p-sophia.html")]:
        ctx = br.new_context(viewport={"width": 1440, "height": 900})
        pg = ctx.new_page()
        pg.goto(url, wait_until="domcontentloaded")
        pg.wait_for_selector("#pname", timeout=20000)
        pg.wait_for_timeout(6000)
        m = pg.evaluate(JS)
        sha = hashlib.sha256(open(f, "rb").read()).hexdigest()
        ev = {"page": label, "page_sha256": sha, **m}
        out[label] = ev
        print(label, ev)
        ctx.close()
    br.close()
json.dump(out["live"], open("/home/hatch/workspace/team-nitro/sisters-personal-pages-20261113/proof/live-evidence-live.json", "w"), indent=2)
json.dump(out["staged"], open("/home/hatch/workspace/team-nitro/sisters-personal-pages-20261113/proof/live-evidence-staged.json", "w"), indent=2)
print("EVIDENCE WRITTEN")
