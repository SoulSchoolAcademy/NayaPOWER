#!/usr/bin/env python3
"""Walk re-proof v2 for fix2 (mirror): K1/K2/K3/K4/C1 with the correct drive.
Drive = pick first visible choice row, then click visible [data-act=submit].
Per-step question text is logged to prove advancement."""
import json
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8899"
OUT = "/tmp/fix2/proof"
res = {}

def vis_rects(pg, sel):
    return pg.evaluate("""(sel) => {
      return [...document.querySelectorAll(sel)].map(e => {
        const b = e.getBoundingClientRect();
        const cs = getComputedStyle(e);
        return {vis: b.height > 0 && b.width > 0 && cs.display !== 'none',
                x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width),
                h: Math.round(b.height), text: (e.textContent||'').trim().slice(0,40)};
      });
    }""", sel)

with sync_playwright() as p:
    br = p.chromium.launch(
        proxy={"server": "http://127.0.0.1:18080", "bypass": "127.0.0.1,localhost"},
        args=["--no-sandbox"])

    # ---------- K1 + K2 at 635 and 390 ----------
    for w in (635, 390):
        ctx = br.new_context(viewport={"width": w, "height": 900})
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(BASE + "/welcome?name=Fix2+Test&alias=fix2k1%d" % w,
                wait_until="load", timeout=60000)
        pg.wait_for_timeout(6000)
        k1 = pg.evaluate("""() => {
          const rows = [];
          document.querySelectorAll('.p3-choice-eye').forEach(eye => {
            const eb = eye.getBoundingClientRect();
            if (eb.height === 0) return;
            // find the row container: nearest ancestor containing an EDIT button
            let row = eye.closest('[class*="choice-row"], [class*="p3-choice"], article, .p3-choices, div');
            let edit = null;
            let el = eye.parentElement;
            while (el && el !== document.body) {
              edit = [...el.querySelectorAll('button')].find(b => b.textContent.trim() === 'EDIT' && b.getBoundingClientRect().height > 0);
              if (edit) { row = el; break; }
              el = el.parentElement;
            }
            const bb = edit ? edit.getBoundingClientRect() : null;
            rows.push({eye: {x: Math.round(eb.x), y: Math.round(eb.y), w: Math.round(eb.width), h: Math.round(eb.height)},
                       edit: bb ? {x: Math.round(bb.x), y: Math.round(bb.y), w: Math.round(bb.width), h: Math.round(bb.height)} : null,
                       sameRow: bb ? !(bb.bottom < eb.top || eb.bottom < bb.top) : false,
                       eyeRightOfEdit: bb ? eb.x >= bb.right - 2 : false});
          });
          return rows;
        }""")
        heads = pg.evaluate("""() => {
          const ts = [];
          document.querySelectorAll('.p3-question, h1, h2').forEach(e => {
            const t = (e.textContent||'').trim();
            if (t) ts.push(t);
          });
          return ts;
        }""")
        quoted = [t for t in heads if t[:1] in ('"', '\u201c', '\u2018', "'") or t[-1:] in ('"', '\u201d', '\u2019', "'")]
        res[f"K1-{w}"] = {"pairs": k1, "errors": errs}
        res[f"K2-{w}-at-load"] = {"headings": heads, "quoted": quoted}
        pg.screenshot(path=OUT + f"/k1b-{w}-q1.png")
        ctx.close()

    # ---------- Drive at 635: K3/K4/C1 ----------
    ctx = br.new_context(viewport={"width": 635, "height": 900})
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(BASE + "/welcome?name=Fix2+Test&alias=fix2drive2",
            wait_until="load", timeout=60000)
    pg.wait_for_timeout(6000)
    qtexts = []
    for step in range(16):
        q = pg.evaluate("() => { const e = document.querySelector('.p3-question'); return e ? e.textContent.trim() : document.body.className; }")
        qtexts.append(q)
        # pick first visible choice row
        try:
            pg.click(".p3-choice:not([hidden]) >> visible=true", timeout=2000)
            pg.wait_for_timeout(600)
        except Exception:
            pass
        # submit
        try:
            pg.click('[data-act="submit"] >> visible=true', timeout=2500)
        except Exception as ex:
            qtexts.append("SUBMIT-FAIL@" + str(step) + ": " + str(ex)[:120])
            break
        pg.wait_for_timeout(1800)
        # stop if we left the questions (names step / end)
        body = pg.evaluate("() => document.body.className")
        if "step-names" in body or "step-end" in body or "step-cert" in body:
            qtexts.append("BODY:" + body)
            break
    res["drive"] = {"questions": qtexts, "errors": errs,
                    "bodyAfter": pg.evaluate("() => document.body.className")}
    pg.screenshot(path=OUT + "/k3b-635-after-drive.png")
    # K3: names step crests
    k3 = pg.evaluate("""() => {
      const crests = [...document.querySelectorAll('.p3-crest')].map(e => ({
        cls: e.className, disp: getComputedStyle(e).display,
        w: Math.round(e.getBoundingClientRect().width), h: Math.round(e.getBoundingClientRect().height)}));
      return {bodyCls: document.body.className, crests,
              q: (document.querySelector('.p3-question')||{textContent:''}).textContent.trim(),
              nameInput: !!document.querySelector('#p3Name'),
              aliasInput: !!document.querySelector('#p3Alias')};
    }""")
    res["K3-names"] = k3
    # fill names + continue
    try:
        for sel, val in (("#p3Name", "Fix2 Test"), ("#p3Alias", "fix2drive2")):
            el = pg.query_selector(sel)
            if el:
                el.fill(val)
        pg.wait_for_timeout(500)
        # names continue: try likely buttons
        clicked = None
        for sel in ("#p3NamesNext", ".p3-names-next", '[data-act="names-next"]',
                    ".p3-names .p3-enter", ".p3-names button"):
            try:
                pg.click(sel + " >> visible=true", timeout=2000)
                clicked = sel
                break
            except Exception:
                continue
        res["namesContinueClicked"] = clicked
        pg.wait_for_timeout(4000)
    except Exception as ex:
        res["namesError"] = str(ex)[:300]
    res["afterNames"] = {"body": pg.evaluate("() => document.body.className"),
                         "q": pg.evaluate("() => (document.querySelector('.p3-question')||{textContent:''}).textContent.trim().slice(0,80)")}
    pg.screenshot(path=OUT + "/k4b-635-after-names.png")
    # K4: end views
    k4 = pg.evaluate("""() => {
      const r = s => { const e = document.querySelector(s); if (!e) return null;
        const b = e.getBoundingClientRect();
        return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width),
                h: Math.round(b.height), hidden: e.hidden, disp: getComputedStyle(e).display}; };
      const links = [...document.querySelectorAll('.p3-end-views a, .p3-end-view')].map(a => ({
        href: a.getAttribute('href'), text: (a.textContent||'').trim(),
        rect: (() => { const b = a.getBoundingClientRect();
          return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height)}; })(),
        disp: getComputedStyle(a).display }));
      return {bodyCls: document.body.className, endViews: r('.p3-end-views'), links};
    }""")
    res["K4-end"] = k4
    pg.screenshot(path=OUT + "/k4b-635-end.png")
    # C1: certificate — look for certificate elements now
    c1 = pg.evaluate("""() => {
      const els = [...document.querySelectorAll('[class*="cert"], [id*="cert"]')].map(e => ({
        cls: String(e.className).slice(0,50), id: e.id,
        vis: e.getBoundingClientRect().height > 0,
        text: (e.textContent||'').trim().slice(0,80)}));
      const h = [...document.querySelectorAll('h1,h2')].map(e => e.textContent.trim());
      return {bodyCls: document.body.className, certEls: els.slice(0, 12), headings: h};
    }""")
    res["C1"] = c1
    pg.screenshot(path=OUT + "/c1-635.png")
    res["walkErrors"] = errs
    ctx.close()
    br.close()

print(json.dumps(res, indent=1)[:10000])
with open(OUT + "/results-walk2.json", "w") as f:
    json.dump(res, f, indent=1)
print("WROTE results-walk2.json")
