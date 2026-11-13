#!/usr/bin/env python3
"""Verify the Personal-complete build locally (Playwright Firefox).
Serves the worktree lane dir on localhost:8131 and measures all seven items.
Local Supabase is CORS-blocked (as in the baseline probe) — wall content is
injected as stub posts through the page's own mwPaintWallPosts, and the points
number + live wall + Smart Lists are verified on the staged proof host.
Writes verify-complete.json + screenshots into the lane work dir.
"""
import json, os, threading, http.server, functools, sys
from playwright.sync_api import sync_playwright

LANE = "/home/hatch/workspace/personal-complete-wt/TEAM-NITRO/personal-page-complete-20261113"
OUT = "/home/hatch/workspace/team-nitro/personal-page-complete-20261113"
URL = "http://127.0.0.1:8131/personal-complete.html"
PORT = 8131

class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass

def serve():
    h = functools.partial(H, directory=LANE)
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), h)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd

STUB_POSTS = [
    {"j": {"k": "wall", "a": "Shawn Vibert", "b": "Building the new feed today — the Personal tab should show only my posts.", "t": "Building the feed"}, "at": "2026-11-13T10:00:00Z", "id": "stub-1"},
    {"j": {"k": "wall", "a": "Shawn Vibert", "b": "Second post by the owner, about shipping the page.", "t": "Shipping"}, "at": "2026-11-13T09:00:00Z", "id": "stub-2"},
    {"j": {"k": "wall", "a": "Guest Visitor", "b": "A visitor post about testing pages.", "t": "Testing"}, "at": "2026-11-13T08:00:00Z", "id": "stub-3"},
]

def inject_wall(page):
    page.evaluate("""(posts) => {
        window.MW_WALL_POSTS = posts;
        if (typeof window.mwPaintWallPosts === 'function') window.mwPaintWallPosts(posts);
    }""", STUB_POSTS)

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
    serve()
    res = {"widths": {}, "console": {}, "pageerrors": []}
    with sync_playwright() as p:
        b = p.firefox.launch()
        for w in (390, 1440, 360):
            errs, perrs = [], []
            pg = b.new_page(viewport={"width": w, "height": 844})
            pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            pg.on("pageerror", lambda e: perrs.append(str(e)))
            d = {"viewport": w}
            try:
                pg.goto(URL, wait_until="load")
                pg.wait_for_timeout(2500)
                # --- overflow
                d["overflowX"] = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
                d["scrollH"] = pg.evaluate("document.documentElement.scrollHeight")
                # --- Item 1: buttons
                btns = {}
                for bid in ("msgbtn", "aboutbtn", "myworldbtn", "skillsbtn", "connbtn", "growthbtn", "sharebtn", "joinbtn"):
                    btns[bid] = box(pg, "#" + bid)
                d["buttons"] = btns
                d["settings_in_row"] = pg.evaluate("!!document.querySelector('.ph-actions-row #settingsbtn')")
                d["gear"] = box(pg, "#settingsbtn")
                d["gear_text"] = pg.evaluate("(document.getElementById('settingsbtn')||{}).textContent")
                d["gear_aria"] = pg.evaluate("(document.getElementById('settingsbtn')||{}).getAttribute('aria-label')")
                widths = [v["w"] for v in btns.values() if v]
                d["button_widths_equal_2px"] = (max(widths) - min(widths) <= 2) if widths else False
                d["button_count_visible"] = len([v for v in btns.values() if v])
                # --- Item 2: pluses
                d["pluses_visible"] = pg.evaluate("""() => {
                    const out = [];
                    document.querySelectorAll('button, a, [role=button]').forEach(e => {
                        const r = e.getBoundingClientRect();
                        if (r.width && r.height && (e.innerText||'').trim() === '+') out.push(e.id || e.className);
                    });
                    document.querySelectorAll('.notif-seg').forEach(e => {
                        const r = e.getBoundingClientRect();
                        if (r.width && r.height) out.push('notif-seg:' + e.getAttribute('data-notif'));
                    });
                    return out;
                }""")
                d["pluswrap_visible"] = pg.evaluate("(() => { const e=document.getElementById('pluswrap'); return e ? getComputedStyle(e).display : 'absent'; })()")
                d["rooms_plus_visible"] = pg.evaluate("(() => { const e=document.getElementById('os-rooms-plus'); return e ? getComputedStyle(e).display : 'absent'; })()")
                d["eco_plus_visible"] = pg.evaluate("(() => { const e=document.getElementById('os-eco-plus'); return e ? getComputedStyle(e).display : 'absent'; })()")
                d["notif_segs"] = pg.evaluate("() => Array.from(document.querySelectorAll('.notif-seg')).map(e => e.getAttribute('data-notif'))")
                # click the bar + and read the menu
                plus = pg.query_selector('.notif-seg[data-notif="plus"]')
                if plus:
                    plus.click(); pg.wait_for_timeout(400)
                    d["plus_menu_visible"] = pg.evaluate("(() => { const m=document.getElementById('fcPlusMenu'); return m ? !m.hidden : false; })()")
                    d["plus_menu_items"] = visible_texts(pg, "#fcPlusMenu .fc-plusitem")
                    d["plus_menu_rect"] = box(pg, "#fcPlusMenu")
                    # close it again via Escape
                    pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
                # --- Item 3: the line above the bottom icons (pixel row above each seg tile)
                d["line_check"] = pg.evaluate("""() => {
                    const segs = Array.from(document.querySelectorAll('.notif-seg .notif-tile'));
                    if (!segs.length) return {segs: 0};
                    const c = document.createElement('canvas');
                    // sample via elementFromPoint instead: the point 2px above each tile must NOT be the seg button
                    return segs.map(t => {
                        const r = t.getBoundingClientRect();
                        const el = document.elementFromPoint(r.left + r.width/2, r.top - 2);
                        return {x: Math.round(r.left + r.width/2), y: Math.round(r.top - 2),
                                el: el ? (el.className && el.className.baseVal !== undefined ? 'svg' : (el.tagName + '.' + (typeof el.className === 'string' ? el.className : ''))) : 'none'};
                    });
                }""")
                d["notif_bar_top"] = box(pg, "#naya-notif-bar")
                # --- Item 4: name + pill
                d["name"] = box(pg, "#pname")
                d["pill"] = box(pg, "#pointsdisplay")
                d["cvrbtn"] = box(pg, "#cvrbtn")
                d["name_text"] = pg.evaluate("(document.getElementById('pname')||{}).textContent")
                d["pill_text"] = pg.evaluate("(document.getElementById('pointscount')||{}).textContent")
                # --- Item 5: tabs
                d["tab_labels"] = pg.evaluate("() => Array.from(document.querySelectorAll('#mwFeedTabs .lens-tab')).map(e => (e.innerText||'').trim())")
                d["tab_keys"] = pg.evaluate("() => Array.from(document.querySelectorAll('#mwFeedTabs .lens-tab')).map(e => e.getAttribute('data-mw-tab'))")
                d["feedline"] = pg.evaluate("(() => { const e=document.querySelector('.pc-feedline'); return e ? e.textContent.trim() : null; })()")
                d["feednames_visible"] = pg.evaluate("() => Array.from(document.querySelectorAll('.mw-feedname')).filter(e => e.offsetParent !== null).map(e => (e.innerText||'').trim())")
                d["composer_cards"] = pg.evaluate("() => Array.from(document.querySelectorAll('.ph-card h3')).filter(h => (h.innerText||'').includes('Make a post')).length")
                d["create_row_buttons"] = visible_texts(pg, "#fcCreateRow button")
                # wall behaviour with stub posts
                inject_wall(pg); pg.wait_for_timeout(600)
                d["wall_cards_personal"] = pg.evaluate("() => document.querySelectorAll('#os-wall-list .ph-card, #os-wall-list .intel-board').length")
                d["wall_meta_personal"] = pg.evaluate("(() => { const e=document.getElementById('os-wall-meta'); return e ? e.textContent : null; })()")
                d["ribbon_personal"] = visible_texts(pg, "#mwFeedPills .smart-tab")
                pg.click("#mwTabNaya"); pg.wait_for_timeout(600)
                inject_wall(pg); pg.wait_for_timeout(400)
                d["wall_cards_public"] = pg.evaluate("() => document.querySelectorAll('#os-wall-list .ph-card, #os-wall-list .intel-board').length")
                d["wall_meta_public"] = pg.evaluate("(() => { const e=document.getElementById('os-wall-meta'); return e ? e.textContent : null; })()")
                d["ribbon_public"] = visible_texts(pg, "#mwFeedPills .smart-tab")
                # the search band is hidden by Shawn's popup-only law — record it, do not fill it
                d["search_band_display"] = pg.evaluate("(() => { const e=document.getElementById('tnpsBand'); return e ? getComputedStyle(e).display : 'absent'; })()")
                d["search_input_visible"] = pg.evaluate("(() => { const e=document.getElementById('tnSearchPersonalInput'); if(!e) return false; const r=e.getBoundingClientRect(); return r.width>0 && r.height>0; })()")
                # Smart Tab pill click re-filters (public tab, author pill)
                pg.evaluate("() => { const p=document.querySelector('#mwFeedPills [data-mw-pill=\"shawn vibert\"]'); if(p) p.click(); }")
                pg.wait_for_timeout(500)
                d["wall_cards_pill_shawn"] = pg.evaluate("() => document.querySelectorAll('#os-wall-list .ph-card, #os-wall-list .intel-board').length")
                # Naya Notes tab
                pg.click("#mwTabActivity"); pg.wait_for_timeout(600)
                d["naya_panel_visible"] = pg.evaluate("(() => { const e=document.getElementById('mwFeedNaya'); return e ? !e.hidden : false; })()")
                d["wall_hidden_on_naya"] = pg.evaluate("(() => { const e=document.getElementById('os-wall-list'); return e ? !!e.hidden : null; })()")
                # creator opens from the create row (back on Personal first)
                pg.click("#mwTabSmart"); pg.wait_for_timeout(500)
                pg.click("#fcCreateRow [data-fc-create='naya']"); pg.wait_for_timeout(500)
                d["creator_visible_naya"] = pg.evaluate("(() => { const e=document.getElementById('fcCreator'); return e ? !e.hidden : false; })()")
                d["creator_title_naya"] = pg.evaluate("(() => { const e=document.getElementById('fcTitleText'); return e ? e.textContent : null; })()")
                pg.keyboard.press("Escape"); pg.wait_for_timeout(400)
                pg.click("#fcCreateRow [data-fc-create='smart']"); pg.wait_for_timeout(500)
                d["creator_title_smart"] = pg.evaluate("(() => { const e=document.getElementById('fcTitleText'); return e ? e.textContent : null; })()")
                pg.keyboard.press("Escape"); pg.wait_for_timeout(400)
                # creator post lands as a stub on the feed (author = owner so it shows on Personal)
                pg.click("#fcCreateRow [data-fc-create='post']"); pg.wait_for_timeout(400)
                pg.fill("#os-post-author", "Shawn Vibert")
                pg.fill("#os-post-body", "Probe post from the creator — personal complete check.")
                pg.click("#os-post-btn"); pg.wait_for_timeout(800)
                d["creator_closed_after_post"] = pg.evaluate("(() => { const e=document.getElementById('fcCreator'); return e ? !!e.hidden : null; })()")
                d["wall_cards_after_post"] = pg.evaluate("() => document.querySelectorAll('#os-wall-list .ph-card, #os-wall-list .intel-board').length")
                d["wall_has_stub"] = pg.evaluate("() => !!document.querySelector('#os-wall-list [data-fc-stub]')")
                # --- Item 7: the rail
                d["rail"] = box(pg, "#pcRail")
                d["rail_cards"] = pg.evaluate("() => document.querySelectorAll('#pcRailList .pc-card').length")
                d["rail_live_cards"] = pg.evaluate("() => document.querySelectorAll('#pcRailList .pc-card .pc-pct').length")
                d["rail_standing_cards"] = pg.evaluate("() => document.querySelectorAll('#pcRailList .pc-card .pc-mark').length")
                d["rail_imgs"] = pg.evaluate("() => document.querySelectorAll('#pcRail img').length")
                d["rail_head"] = pg.evaluate("(() => { const e=document.querySelector('.pc-rail-sub'); return e ? e.textContent.trim() : null; })()")
                d["rail_cards_detail"] = pg.evaluate("""() => Array.from(document.querySelectorAll('#pcRailList .pc-card')).map(c => ({
                    alias: c.getAttribute('data-pc-alias'),
                    pct: (c.querySelector('.pc-pct')||{}).textContent || null,
                    mark: (c.querySelector('.pc-mark')||{}).textContent || null,
                    nut: (c.querySelector('.pc-nut')||{}).textContent || null,
                    reasons: (c.querySelector('.pc-reasons')||{}).textContent || null,
                    btns: Array.from(c.querySelectorAll('.pc-btn')).map(b => b.textContent.trim()),
                    orb: (c.querySelector('.fc-pick-av')||{}).textContent || null,
                    imgs: c.querySelectorAll('img').length
                }))""")
                # chat opens in place from a rail card
                pg.evaluate("() => window.scrollTo(0, 0)")
                first_chat = pg.query_selector("#pcRailList .pc-card .pc-btn[data-pc-act='chat']")
                if first_chat:
                    first_chat.click(); pg.wait_for_timeout(500)
                    d["chat_visible"] = pg.evaluate("(() => { const e=document.getElementById('fcChat'); return e ? !e.hidden : false; })()")
                    d["chat_name"] = pg.evaluate("(() => { const e=document.getElementById('fcChatName'); return e ? e.textContent : null; })()")
                    pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
                # audio opens chat with the honest status
                first_audio = pg.query_selector("#pcRailList .pc-card .pc-btn[data-pc-act='audio']")
                if first_audio:
                    first_audio.click(); pg.wait_for_timeout(500)
                    d["audio_chat_visible"] = pg.evaluate("(() => { const e=document.getElementById('fcChat'); return e ? !e.hidden : false; })()")
                    d["audio_status"] = pg.evaluate("(() => { const e=document.getElementById('fcChatStatus'); return e ? e.textContent : null; })()")
                    pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
                # scroll rule: 3-person fixture -> no scrollbar; 25-person fixture -> scrollbar
                d["rail_scroll_3"] = pg.evaluate("""() => {
                    const live = window.PC_RAIL_LIVE.slice(0, 3);
                    window.pcRenderRail(live, []);
                    const l = document.getElementById('pcRailList');
                    return {scrollH: l.scrollHeight, clientH: l.clientHeight, scrolls: l.scrollHeight > l.clientHeight + 1};
                }""")
                d["rail_scroll_25"] = pg.evaluate("""() => {
                    const many = [];
                    for (let i = 0; i < 25; i++) many.push({alias: 'fixture' + i, nut: 'Fixture person number ' + i + ' — testing the scroll rule with a long rail.', pct: 10 + i, reasons: ['shared: test']});
                    window.pcRenderRail(many, []);
                    const l = document.getElementById('pcRailList');
                    return {scrollH: l.scrollHeight, clientH: l.clientHeight, scrolls: l.scrollHeight > l.clientHeight + 1};
                }""")
                pg.evaluate("() => window.pcRenderRail()")
                # gear opens Settings
                pg.evaluate("() => window.scrollTo(0, 0)")
                pg.click("#settingsbtn"); pg.wait_for_timeout(600)
                d["settings_opens"] = pg.evaluate("() => location.hash")
                pg.evaluate("() => { if (window.osShowView) window.osShowView('home'); }"); pg.wait_for_timeout(400)
                # screenshots
                pg.evaluate("() => window.scrollTo(0, 0)"); pg.wait_for_timeout(400)
                pg.screenshot(path=f"{OUT}/verify-{w}-top.png")
                pg.evaluate("() => window.scrollTo(0, document.body.scrollHeight)"); pg.wait_for_timeout(600)
                pg.screenshot(path=f"{OUT}/verify-{w}-end.png")
                pg.evaluate("() => { const f=document.getElementById('mwFeedTabs'); if(f) f.scrollIntoView({block:'start'}); }")
                pg.wait_for_timeout(400)
                pg.screenshot(path=f"{OUT}/verify-{w}-feed.png")
            except Exception as e:
                d["error"] = str(e)
            res["widths"][w] = d
            res["console"][w] = {"errors": errs, "pageerrors": perrs}
            pg.close()
        b.close()
    with open(f"{OUT}/verify-complete.json", "w") as f:
        json.dump(res, f, indent=1)
    print("wrote verify-complete.json")

if __name__ == "__main__":
    run()
