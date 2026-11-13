#!/usr/bin/env python3
"""Staged verification of the Personal-complete build on the proof host.
Reads the file fresh (cb = commit sha + width nonce), measures all seven items
against the REAL wall / points / lists. Writes verify-staged.json + screenshots.
The creator post + lists save are tested with a clearly labeled probe note;
any live row they create is deleted afterwards by cleanup-staged.py.
"""
import json, sys
from playwright.sync_api import sync_playwright

COMMIT = "b0a792186992dc06ee1d1dffafce343041b1faab"
BASE = ("https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/"
        "personal-page-complete-20261113/personal-complete.html"
        "&ref=personal/personal-page-complete-20261113")
OUT = "/home/hatch/workspace/team-nitro/personal-page-complete-20261113"
PROBE_TEXT = "Probe — personal complete check (delete me)."

def box(page, sel):
    el = page.query_selector(sel)
    if not el: return None
    b = el.bounding_box()
    if not b: return None
    return {"x": round(b["x"], 1), "y": round(b["y"], 1), "w": round(b["width"], 1), "h": round(b["height"], 1)}

def visible_texts(page, sel):
    return page.evaluate("""(sel) => {
        return Array.from(document.querySelectorAll(sel))
            .filter(e => e.offsetParent !== null || e.getClientRects().length)
            .map(e => (e.innerText || '').trim());
    }""", sel)

def run():
    res = {"staged_sha": "87d038470fb65ccd90b4c4a25af4cf2abea20afe7045c5aff193ae3ee73fc04c",
           "commit": COMMIT, "widths": {}, "console": {}}
    with sync_playwright() as p:
        b = p.firefox.launch()
        for w in (390, 1440, 360):
            errs, perrs = [], []
            pg = b.new_page(viewport={"width": w, "height": 844})
            pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            pg.on("pageerror", lambda e: perrs.append(str(e)))
            url = BASE + "&cb=" + COMMIT + "-w" + str(w)
            d = {"viewport": w, "url": url}
            try:
                pg.goto(url, wait_until="load")
                pg.wait_for_timeout(4000)
                d["overflowX"] = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
                d["scrollH"] = pg.evaluate("document.documentElement.scrollHeight")
                # Item 1
                btns = {}
                for bid in ("msgbtn", "aboutbtn", "myworldbtn", "skillsbtn", "connbtn", "growthbtn", "sharebtn", "joinbtn"):
                    btns[bid] = box(pg, "#" + bid)
                d["buttons"] = btns
                widths = [v["w"] for v in btns.values() if v]
                d["button_widths_equal_2px"] = (max(widths) - min(widths) <= 2) if widths else False
                d["gear"] = box(pg, "#settingsbtn")
                d["gear_text"] = pg.evaluate("(document.getElementById('settingsbtn')||{}).textContent")
                # Item 2
                d["notif_segs"] = pg.evaluate("() => Array.from(document.querySelectorAll('.notif-seg')).map(e => e.getAttribute('data-notif'))")
                d["pluswrap_display"] = pg.evaluate("(() => { const e=document.getElementById('pluswrap'); return e ? getComputedStyle(e).display : 'absent'; })()")
                plus = pg.query_selector('.notif-seg[data-notif="plus"]')
                if plus:
                    plus.click(); pg.wait_for_timeout(400)
                    d["plus_menu_items"] = visible_texts(pg, "#fcPlusMenu .fc-plusitem")
                    pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
                # Item 3
                d["seg_shadow"] = pg.evaluate("() => { const s=document.querySelector('.notif-seg'); return s ? getComputedStyle(s).boxShadow : 'none'; }")
                # Item 4 — the points NUMBER, live
                d["name"] = box(pg, "#pname")
                d["pill"] = box(pg, "#pointsdisplay")
                d["cvrbtn"] = box(pg, "#cvrbtn")
                d["pill_text"] = pg.evaluate("(document.getElementById('pointscount')||{}).textContent")
                # Item 5 — the real wall
                d["tab_labels"] = pg.evaluate("() => Array.from(document.querySelectorAll('#mwFeedTabs .lens-tab')).map(e => (e.innerText||'').trim())")
                d["feedline"] = pg.evaluate("(() => { const e=document.querySelector('.pc-feedline'); return e ? e.textContent.trim() : null; })()")
                d["composer_cards"] = pg.evaluate("() => Array.from(document.querySelectorAll('.ph-card h3')).filter(h => (h.innerText||'').includes('Make a post')).length")
                d["wall_cards_personal"] = pg.evaluate("() => document.querySelectorAll('#os-wall-list .ph-card, #os-wall-list .intel-board').length")
                d["wall_authors_personal"] = pg.evaluate("() => Array.from(document.querySelectorAll('#os-wall-list .intel-board')).slice(0,8).map(c => (c.innerText||'').split('\\n')[0])")
                d["wall_meta_personal"] = pg.evaluate("(() => { const e=document.getElementById('os-wall-meta'); return e ? e.textContent : null; })()")
                d["ribbon_personal"] = visible_texts(pg, "#mwFeedPills .smart-tab")
                pg.click("#mwTabNaya"); pg.wait_for_timeout(800)
                d["wall_cards_public"] = pg.evaluate("() => document.querySelectorAll('#os-wall-list .ph-card, #os-wall-list .intel-board').length")
                d["wall_meta_public"] = pg.evaluate("(() => { const e=document.getElementById('os-wall-meta'); return e ? e.textContent : null; })()")
                d["ribbon_public"] = visible_texts(pg, "#mwFeedPills .smart-tab")
                pg.click("#mwTabActivity"); pg.wait_for_timeout(800)
                d["naya_panel_visible"] = pg.evaluate("(() => { const e=document.getElementById('mwFeedNaya'); return e ? !e.hidden : false; })()")
                d["naya_cards"] = pg.evaluate("() => document.querySelectorAll('#mwFeedNaya .ph-card, #mwFeedNaya .intel-board, #mwFeedNaya .os-note').length")
                # creator opens (no write)
                pg.click("#mwTabSmart"); pg.wait_for_timeout(600)
                pg.click("#fcCreateRow [data-fc-create='naya']"); pg.wait_for_timeout(500)
                d["creator_visible_naya"] = pg.evaluate("(() => { const e=document.getElementById('fcCreator'); return e ? !e.hidden : false; })()")
                d["creator_title_naya"] = pg.evaluate("(() => { const e=document.getElementById('fcTitleText'); return e ? e.textContent : null; })()")
                pg.keyboard.press("Escape"); pg.wait_for_timeout(400)
                # creator POST (only at 1440 — one probe note, cleaned up afterwards)
                if w == 1440:
                    pg.click("#fcCreateRow [data-fc-create='post']"); pg.wait_for_timeout(400)
                    pg.fill("#os-post-author", "Shawn Vibert")
                    pg.fill("#os-post-body", PROBE_TEXT)
                    pg.click("#os-post-btn"); pg.wait_for_timeout(1200)
                    d["creator_closed_after_post"] = pg.evaluate("(() => { const e=document.getElementById('fcCreator'); return e ? !!e.hidden : null; })()")
                    d["wall_has_probe_stub"] = pg.evaluate("() => Array.from(document.querySelectorAll('#os-wall-list [data-fc-stub]')).some(e => (e.innerText||'').includes('personal complete check'))")
                    d["wall_has_probe_text"] = pg.evaluate("() => document.querySelector('#os-wall-list') ? document.querySelector('#os-wall-list').innerText.includes('personal complete check') : false")
                    # Smart Lists: SAVE the probe card, then open Lists
                    pg.evaluate("""() => {
                        const cards = Array.from(document.querySelectorAll('#os-wall-list .ph-card, #os-wall-list .intel-board'));
                        const card = cards.find(c => (c.innerText||'').includes('personal complete check'));
                        if (!card) return;
                        const save = Array.from(card.querySelectorAll('button')).find(b => /SAVE/i.test(b.innerText||''));
                        if (save) save.click();
                    }""")
                    pg.wait_for_timeout(1000)
                    d["smartlist_store"] = pg.evaluate("() => { try { return localStorage.getItem('naya.smartlist'); } catch(e){ return 'ERR:'+e; } }")
                    pg.evaluate("() => { if (window.osShowView) window.osShowView('lists'); }")
                    pg.wait_for_timeout(2000)
                    d["lists_view_text"] = pg.evaluate("() => { const v=document.querySelector('[data-os-view=\"lists\"]'); return v ? (v.innerText||'').slice(0, 900) : 'no lists view'; }")
                    pg.evaluate("() => { if (window.osShowView) window.osShowView('home'); }")
                    pg.wait_for_timeout(800)
                # Item 7 — rail
                d["rail"] = box(pg, "#pcRail")
                d["rail_cards"] = pg.evaluate("() => document.querySelectorAll('#pcRailList .pc-card').length")
                d["rail_live_cards"] = pg.evaluate("() => document.querySelectorAll('#pcRailList .pc-card .pc-pct').length")
                d["rail_standing_cards"] = pg.evaluate("() => document.querySelectorAll('#pcRailList .pc-card .pc-mark').length")
                d["rail_imgs"] = pg.evaluate("() => document.querySelectorAll('#pcRail img').length")
                d["rail_head"] = pg.evaluate("(() => { const e=document.querySelector('.pc-rail-sub'); return e ? e.textContent.trim() : null; })()")
                # chat opens in place
                first_chat = pg.query_selector("#pcRailList .pc-card .pc-btn[data-pc-act='chat']")
                if first_chat:
                    first_chat.click(); pg.wait_for_timeout(500)
                    d["chat_visible"] = pg.evaluate("(() => { const e=document.getElementById('fcChat'); return e ? !e.hidden : false; })()")
                    d["chat_name"] = pg.evaluate("(() => { const e=document.getElementById('fcChatName'); return e ? e.textContent : null; })()")
                    pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
                # gear opens Settings
                pg.evaluate("() => window.scrollTo(0, 0)")
                pg.click("#settingsbtn"); pg.wait_for_timeout(600)
                d["settings_opens"] = pg.evaluate("() => location.hash")
                pg.evaluate("() => { if (window.osShowView) window.osShowView('home'); }"); pg.wait_for_timeout(400)
                # screenshots
                pg.evaluate("() => window.scrollTo(0, 0)"); pg.wait_for_timeout(400)
                pg.screenshot(path=f"{OUT}/staged-{w}-top.png")
                pg.evaluate("() => window.scrollTo(0, document.body.scrollHeight)"); pg.wait_for_timeout(600)
                pg.screenshot(path=f"{OUT}/staged-{w}-end.png")
                pg.evaluate("() => { const f=document.getElementById('mwFeedTabs'); if(f) f.scrollIntoView({block:'start'}); }")
                pg.wait_for_timeout(400)
                pg.screenshot(path=f"{OUT}/staged-{w}-feed.png")
            except Exception as e:
                d["error"] = str(e)
            res["widths"][w] = d
            res["console"][w] = {"errors": errs, "pageerrors": perrs}
            pg.close()
        b.close()
    with open(f"{OUT}/verify-staged.json", "w") as f:
        json.dump(res, f, indent=1)
    print("wrote verify-staged.json")

if __name__ == "__main__":
    run()
