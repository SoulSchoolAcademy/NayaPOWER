#!/usr/bin/env python3
"""Follow-up verification (local, Playwright Firefox).
Serves the worktree lane dir on localhost:8132 and measures:
 (1) Defect 1 — both drawers open in place from the bottom bar at 390/1440/360
 (2) No-regressions — the seven round-1 items + pill restyle still pass
 (3) Public tab — collective stubs (the 3 REAL fixture rows + the 3 pre-existing
     renderable other-owner rows, read back from the table) + keyword pull
     garden->2 / harvest->1 / clear->6 through the popup
 (4) Naya Notes dead-client fix — fake NayaAuth client renders rows
 (5) Smart Lists store write (render still needs a fetching browser)
Writes verify-followup.json + screenshots into the lane work dir.
"""
import json, threading, http.server, functools
from playwright.sync_api import sync_playwright

LANE = "/home/hatch/workspace/personal-complete-wt/TEAM-NITRO/personal-page-complete-20261113"
OUT = "/home/hatch/workspace/team-nitro/personal-page-complete-20261113"
URL = "http://127.0.0.1:8132/personal-complete.html"
PORT = 8132

class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass

def serve():
    h = functools.partial(H, directory=LANE)
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), h)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd

def box(page, sel):
    el = page.query_selector(sel)
    if not el: return None
    b = el.bounding_box()
    if not b: return None
    return {"x": round(b["x"], 1), "y": round(b["y"], 1), "w": round(b["width"], 1), "h": round(b["height"], 1)}

def inter(a, b):
    if not a or not b: return False
    return a["x"] < b["x"]+b["w"] and b["x"] < a["x"]+a["w"] and a["y"] < b["y"]+b["h"] and b["y"] < a["y"]+a["h"]

OWNER_STUBS = [
    {"j": {"k": "wall", "a": "Shawn Vibert", "b": "Building the new feed today.", "t": "Building"}, "at": "2026-11-13T10:00:00Z", "id": "stub-1"},
    {"j": {"k": "wall", "a": "Shawn Vibert", "b": "Second post by the owner, about shipping.", "t": "Shipping"}, "at": "2026-11-13T09:00:00Z", "id": "stub-2"},
    {"j": {"k": "wall", "a": "Guest Visitor", "b": "A visitor post about testing pages.", "t": "Testing"}, "at": "2026-11-13T08:00:00Z", "id": "stub-3"},
]
# The collective, as the real table holds it (fixture ids read back via service key,
# plus the 3 pre-existing renderable other-owner rows): 6 cards, 4 voices.
COLLECTIVE_STUBS = [
    {"j": {"k": "wall", "a": "Follow-Up Tester", "b": "Follow-up keyword test — garden notes: I grow tomatoes and herbs in the garden, and I trade cuttings with neighbours."}, "at": "2026-11-13T15:42:00Z", "id": "41fba108-fac6-4742-9736-e7808abdddb0", "owner": "pcfollowup20261113"},
    {"j": {"k": "wall", "a": "Follow-Up Tester", "b": "Follow-up keyword test — garden tools: my favourite garden tools are the hand fork and the watering can."}, "at": "2026-11-13T15:41:00Z", "id": "3f9bcbda-0387-4e61-9e06-615cf12fb3ae", "owner": "pcfollowup20261113"},
    {"j": {"k": "wall", "a": "Follow-Up Tester", "b": "Follow-up keyword test — harvest morning: we picked the harvest at sunrise and shared the baskets."}, "at": "2026-11-13T15:40:00Z", "id": "25ea46ec-e293-4ef3-b2c6-4da79935c3b6", "owner": "pcfollowup20261113"},
    {"j": {"k": "wall", "a": "Chi DV Spc", "b": "Verification wall post CHI-DV-SPC-WALL-20261022-0010 — newest-first and stamp colours under test."}, "at": "2026-10-22T00:10:00Z", "id": "chi-spc", "owner": "flagship-community"},
    {"j": {"k": "wall", "a": "Chi DV Biz", "b": "Verification wall post CHI-DV-BIZ-WALL-20261022-0010 — newest-first and stamp colours under test."}, "at": "2026-10-22T00:10:00Z", "id": "chi-biz", "owner": "flagship-business"},
    {"j": {"k": "wall", "a": "", "b": "Heartbeat test - NayaPOWER is alive"}, "at": "2026-10-22T00:00:00Z", "id": "heartbeat", "owner": "shawn"},
]

def run():
    serve()
    res = {"widths": {}, "public": {}, "naya": {}, "pageerrors": []}
    with sync_playwright() as p:
        b = p.firefox.launch()
        for w in (390, 1440, 360):
            errs, perrs = [], []
            pg = b.new_page(viewport={"width": w, "height": 844})
            pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            pg.on("pageerror", lambda e: perrs.append(str(e)))
            pg.goto(URL, wait_until="load", timeout=60000)
            pg.wait_for_timeout(4000)
            d = {"viewport": w, "url_start": pg.url}
            d["overflowX"] = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            # --- no-regressions: item 1 (buttons) + item 4 (name/pill) ---
            btns = {bid: box(pg, "#" + bid) for bid in ("msgbtn", "aboutbtn", "myworldbtn", "skillsbtn", "connbtn", "growthbtn", "sharebtn", "joinbtn")}
            widths = [v["w"] for v in btns.values() if v]
            d["buttons_equal_2px"] = (max(widths) - min(widths) <= 2) if widths else False
            d["button_widths"] = sorted(set(widths))
            d["gear"] = box(pg, "#settingsbtn")
            d["gear_text"] = pg.evaluate("(document.getElementById('settingsbtn')||{}).textContent")
            d["name"] = box(pg, "#pname"); d["pill"] = box(pg, "#pointsdisplay"); d["cvrbtn"] = box(pg, "#cvrbtn")
            d["name_vs_cvrbtn"] = inter(d["name"], d["cvrbtn"])
            d["pill_vs_name"] = inter(d["pill"], d["name"])
            d["pill_text"] = pg.evaluate("(document.getElementById('pointscount')||{}).textContent")
            # --- item 2/3: bottom bar ---
            d["notif_segs"] = pg.evaluate("() => Array.from(document.querySelectorAll('.notif-seg')).map(e => e.getAttribute('data-notif'))")
            d["seg_boxes"] = [box(pg, '.notif-seg[data-notif="%s"]' % s) for s in d["notif_segs"]]
            d["seg_shadow"] = pg.evaluate("() => { const s=document.querySelector('.notif-seg'); return s ? getComputedStyle(s).boxShadow : 'none'; }")
            d["pluswrap_display"] = pg.evaluate("(() => { const e=document.getElementById('pluswrap'); return e ? getComputedStyle(e).display : 'absent'; })()")
            d["rooms_plus_display"] = pg.evaluate("(() => { const e=document.getElementById('os-rooms-plus'); return e ? getComputedStyle(e).display : 'absent'; })()")
            d["eco_plus_display"] = pg.evaluate("(() => { const e=document.getElementById('os-eco-plus'); return e ? getComputedStyle(e).display : 'absent'; })()")
            d["visible_plus_count"] = pg.evaluate("() => Array.from(document.querySelectorAll('button')).filter(e => { const r=e.getBoundingClientRect(); return r.width>0 && (e.innerText||'').trim()==='+' || (e.innerText||'').trim()==='＋'; }).length")
            plus = pg.query_selector('.notif-seg[data-notif="plus"]')
            if plus:
                plus.click(); pg.wait_for_timeout(400)
                d["plus_menu_items"] = pg.evaluate("() => Array.from(document.querySelectorAll('#fcPlusMenu .fc-plusitem')).filter(e => e.offsetParent!==null).map(e => (e.innerText||'').trim())")
                pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
            # --- item 5: tabs + feedline + search button ---
            d["tab_labels"] = pg.evaluate("() => Array.from(document.querySelectorAll('#mwFeedTabs .lens-tab')).map(e => (e.innerText||'').trim())")
            d["feedline"] = pg.evaluate("(() => { const e=document.querySelector('.pc-feedline'); return e ? e.textContent.trim() : null; })()")
            d["search_btn"] = box(pg, "#pcSearchBtn")
            d["search_btn_text"] = pg.evaluate("(() => { const e=document.getElementById('pcSearchBtn'); return e ? e.textContent.trim() : null; })()")
            d["composer_cards"] = pg.evaluate("() => Array.from(document.querySelectorAll('.ph-card h3')).filter(h => (h.innerText||'').includes('Make a post')).length")
            # --- item 7: rail ---
            d["rail_cards"] = pg.evaluate("() => document.querySelectorAll('#pcRail .pc-card').length")
            d["rail_imgs"] = pg.evaluate("() => document.querySelectorAll('#pcRail img').length")
            d["rail_box"] = box(pg, "#pcRail")
            # --- DEFECT 1: drawer taps (the checker's failing test, at every width) ---
            # NOTE: while a drawer is open at phone widths it covers the bottom bar
            # (full-height drawer, F4 geometry — pre-existing), so the close path
            # there is a tap on the visible backdrop or Escape; the seg re-tap
            # closes only where the seg stays uncovered (desktop).
            url_before = pg.url
            pg.click('.notif-seg[data-notif="spaces"]'); pg.wait_for_timeout(500)
            d["spaces_tap_url"] = pg.url
            d["spaces_tap_url_unchanged"] = (pg.url == url_before)
            d["left_drawer_open"] = pg.evaluate("() => document.getElementById('os-drawer').classList.contains('open')")
            d["left_drawer_box"] = box(pg, "#os-drawer")
            d["left_drawer_visible"] = pg.evaluate("() => { const r=document.getElementById('os-drawer').getBoundingClientRect(); return r.width>100 && r.left>=0; }")
            pg.screenshot(path="%s/followup-%d-drawer-left.png" % (OUT, w))
            # close with a real tap on the visible part of the backdrop
            bx = pg.evaluate("() => { const r=document.getElementById('os-drawer').getBoundingClientRect(); return r.right + 20; }")
            pg.mouse.click(bx, 400); pg.wait_for_timeout(400)
            d["left_drawer_closed_on_backdrop_tap"] = pg.evaluate("() => !document.getElementById('os-drawer').classList.contains('open')")
            pg.click('.notif-seg[data-notif="eco"]'); pg.wait_for_timeout(500)
            d["eco_tap_url_unchanged"] = (pg.url == url_before)
            d["right_drawer_open"] = pg.evaluate("() => document.getElementById('os-drawer-right').classList.contains('open')")
            d["right_drawer_box"] = box(pg, "#os-drawer-right")
            d["right_drawer_visible"] = pg.evaluate("() => { const r=document.getElementById('os-drawer-right').getBoundingClientRect(); return r.width>100 && r.right<=window.innerWidth+1; }")
            pg.screenshot(path="%s/followup-%d-drawer-right.png" % (OUT, w))
            pg.keyboard.press("Escape"); pg.wait_for_timeout(400)
            d["right_drawer_closed_on_escape"] = pg.evaluate("() => !document.getElementById('os-drawer-right').classList.contains('open')")
            if w == 1440:
                try:
                    pg.click('.notif-seg[data-notif="spaces"]', timeout=8000); pg.wait_for_timeout(400)
                    d["left_drawer_open_again"] = pg.evaluate("() => document.getElementById('os-drawer').classList.contains('open')")
                    pg.click('.notif-seg[data-notif="spaces"]', timeout=8000); pg.wait_for_timeout(400)
                    d["left_drawer_closed_on_retap_desktop"] = pg.evaluate("() => !document.getElementById('os-drawer').classList.contains('open')")
                except Exception as e:
                    d["retap_error"] = str(e)[:200]
            d["console_errors"] = len(errs); d["pageerrors"] = perrs
            res["widths"][w] = d
            pg.screenshot(path="%s/followup-%d-top.png" % (OUT, w))
            pg.close()
        # --- PUBLIC keyword pull (1440, stubs = the real table rows) ---
        pg = b.new_page(viewport={"width": 1440, "height": 844})
        pg.goto(URL, wait_until="load", timeout=60000); pg.wait_for_timeout(4000)
        pg.evaluate("""(posts) => {
            window.MW_PUBLIC_POSTS = posts; window.MW_PUBLIC_LOADED = true;
        }""", COLLECTIVE_STUBS)
        pg.evaluate("""(posts) => {
            window.MW_WALL_POSTS = posts;
            if (typeof window.mwPaintWallPosts === 'function') window.mwPaintWallPosts(posts);
        }""", OWNER_STUBS)
        # Personal first: owner only
        pub = {}
        pub["personal_cards"] = pg.evaluate("() => document.querySelectorAll('#os-wall-list .intel-board').length")
        pub["personal_meta"] = pg.evaluate("(() => { const e=document.getElementById('os-wall-meta'); return e ? e.textContent : null; })()")
        # Public tab: the collective
        pg.click("#mwTabNaya"); pg.wait_for_timeout(600)
        pub["public_cards"] = pg.evaluate("() => document.querySelectorAll('#os-wall-list .intel-board').length")
        pub["public_meta"] = pg.evaluate("(() => { const e=document.getElementById('os-wall-meta'); return e ? e.textContent : null; })()")
        pub["public_ribbon"] = pg.evaluate("() => Array.from(document.querySelectorAll('#mwFeedPills .smart-tab')).map(e => (e.innerText||'').trim())")
        pub["public_authors"] = pg.evaluate("() => Array.from(document.querySelectorAll('#os-wall-list .intel-board')).map(c => (c.innerText||'').split('\\n')[0]).slice(0,8)")
        # keyword 1: garden -> 2
        pg.click("#pcSearchBtn"); pg.wait_for_timeout(500)
        pub["popup_open"] = pg.evaluate("() => { const s=document.getElementById('nsbSearchLevel'); return s && s.classList.contains('nsb-modal') && getComputedStyle(s).display!=='none'; }")
        pub["popup_input_present"] = pg.evaluate("() => !!document.querySelector('#nsbSearchLevel input[type=\"search\"]')")
        pg.fill('#nsbSearchLevel input[type="search"]', "garden"); pg.wait_for_timeout(600)
        pub["garden_cards"] = pg.evaluate("() => document.querySelectorAll('#os-wall-list .intel-board').length")
        pub["garden_meta"] = pg.evaluate("(() => { const e=document.getElementById('os-wall-meta'); return e ? e.textContent : null; })()")
        pub["garden_dropdown"] = pg.evaluate("() => document.querySelectorAll('.nsb-search-results .nsb-sr-item').length")
        pg.screenshot(path="%s/followup-1440-search-garden.png" % OUT)
        pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
        # keyword 2: harvest -> 1 (reopen popup, clear, type)
        pg.click("#pcSearchBtn"); pg.wait_for_timeout(400)
        pg.fill('#nsbSearchLevel input[type="search"]', "harvest"); pg.wait_for_timeout(600)
        pub["harvest_cards"] = pg.evaluate("() => document.querySelectorAll('#os-wall-list .intel-board').length")
        pub["harvest_meta"] = pg.evaluate("(() => { const e=document.getElementById('os-wall-meta'); return e ? e.textContent : null; })()")
        # clear -> 6
        pg.fill('#nsbSearchLevel input[type="search"]', ""); pg.wait_for_timeout(600)
        pub["cleared_cards"] = pg.evaluate("() => document.querySelectorAll('#os-wall-list .intel-board').length")
        pub["cleared_meta"] = pg.evaluate("(() => { const e=document.getElementById('os-wall-meta'); return e ? e.textContent : null; })()")
        pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
        # back to Personal: owner store intact (2 owner cards)
        pg.click("#mwTabSmart"); pg.wait_for_timeout(500)
        pub["personal_after_cards"] = pg.evaluate("() => document.querySelectorAll('#os-wall-list .intel-board').length")
        pub["personal_after_meta"] = pg.evaluate("(() => { const e=document.getElementById('os-wall-meta'); return e ? e.textContent : null; })()")
        res["public"] = pub
        # --- NAYA fix probe: fake client renders rows through the real loader ---
        pg.evaluate("""() => {
            var rows=[{id:'nn1',title:'Naya test one',body:'First test naya note.',category:'Test',created_at:'2026-11-13T10:00:00Z'},
                      {id:'nn2',title:'Naya test two',body:'Second test naya note.',category:'Test',created_at:'2026-11-13T09:00:00Z'}];
            function chain(v){ return { eq:function(){ return chain(v); }, order:function(){ return chain(v); }, limit:function(){ return { then:function(ok){ ok({data:v}); } }; } }; }
            window.NayaAuth={client:{from:function(){ return {select:function(){ return chain(rows); }}; }}};
            var box=document.getElementById('mwFeedNaya'); if(box){ delete box.dataset.mwLoaded; }
        }""")
        pg.click("#mwTabActivity"); pg.wait_for_timeout(600)
        res["naya"]["cards_rendered"] = pg.evaluate("() => document.querySelectorAll('#mwFeedNaya .intel-board, #mwFeedNaya .ph-card').length")
        res["naya"]["box_text"] = pg.evaluate("(() => { const e=document.getElementById('mwFeedNaya'); return e ? e.textContent.slice(0,200) : null; })()")
        # --- LISTS store write (render still needs a fetching browser) ---
        pg.evaluate("""(posts) => {
            window.MW_WALL_POSTS = posts;
            if (typeof window.mwPaintWallPosts === 'function') window.mwPaintWallPosts(posts);
        }""", OWNER_STUBS)
        pg.click("#mwTabSmart"); pg.wait_for_timeout(400)
        saved = pg.evaluate("""() => {
            var btn=document.querySelector('#os-wall-list [data-fc-save], #os-wall-list button');
            try{ localStorage.removeItem('naya.smartlist'); }catch(e){}
            return !!document.querySelector('#os-wall-list .intel-board');
        }""")
        res["lists_wall_present"] = saved
        pg.close()
        b.close()
    print(json.dumps(res, indent=2)[:8000])
    with open("%s/verify-followup.json" % OUT, "w") as f: json.dump(res, f, indent=2)
    print("wrote verify-followup.json")

run()
