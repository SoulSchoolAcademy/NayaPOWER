#!/usr/bin/env python3
"""F4 maker probe v2 — rendered week-bars note in es/fr/de, both paths, both branches.
Run: python3 f4-probe.py <url> <width> <lang> <data|empty>
- Intercepts Supabase rest/v1: data mode seeds wall/note/message/invite rows
  (Busiest branch); empty mode returns [] everywhere (quiet branch).
- Fresh-load preset via ctx.add_init_script with JSON.stringify(lang) (the
  checker's working method — the page stores the lang JSON-encoded).
- Switch path via the Settings select; osRerenderDashboard re-renders.
- Reads #os-dash-week-note per kind (all/posts/notes/messages/invites).
- Clean overflow on a fresh context (no Settings opened)."""
import sys, json
from datetime import datetime, timedelta, timezone
from playwright.sync_api import sync_playwright

URL = sys.argv[1]
WIDTH = int(sys.argv[2])
LANG = sys.argv[3] if len(sys.argv) > 3 else 'es'
MODE = sys.argv[4] if len(sys.argv) > 4 else 'data'

EN_WORDS = ['The next post', 'lights the first bar', 'Posts, notes', 'Feed posts only',
            'Smart Notes only', 'Messages received only', 'Invites recorded only',
            'The next feed post', 'The first Smart Note', 'The next message',
            'The next invite', 'Busiest', 'A quiet stretch']

now = datetime.now(timezone.utc)
iso1 = (now - timedelta(days=1)).isoformat().replace('+00:00', 'Z')
iso2 = (now - timedelta(days=2)).isoformat().replace('+00:00', 'Z')

DATA = {
    'smart_notes': [
        {'id': 'synth-wall-1', 'content': json.dumps({'k': 'wall', 'a': 'Shawn', 'b': 'Test post one'}), 'created_at': iso1},
        {'id': 'synth-wall-2', 'content': json.dumps({'k': 'wall', 'a': 'Shawn', 'b': 'Test post two'}), 'created_at': iso2},
        {'id': 'synth-wall-3', 'content': json.dumps({'k': 'wall', 'a': 'Shawn', 'b': 'Test post three'}), 'created_at': iso1},
        {'id': 'synth-note-1', 'content': json.dumps({'k': 'note', 't': 'Test note', 'b': 'A test note'}), 'created_at': iso1},
    ],
    'smart_mail_threads': [
        {'id': 't1', 'subject': 'Hello', 'from_alias': 'sophia', 'preview': 'hi',
         'created_at': iso1, 'to_alias': 'flagship-personal'},
    ],
    'smart_mail_messages': [
        {'thread_id': 't1', 'from_alias': 'sophia', 'body': 'Hello there', 'created_at': iso1},
    ],
    'invites': [
        {'invitee_name': 'Test Friend', 'status': 'pending', 'dry_run': False, 'created_at': iso1},
        {'invitee_name': 'Test Two', 'status': 'pending', 'dry_run': False, 'created_at': iso2},
    ],
    'smart_links': [],
    'smart_link_daily_stats': [],
    'smart_link_dimension_stats': [],
}

def section(t):
    print("\n===== %s =====" % t, flush=True)

def has_en(text):
    return [w for w in EN_WORDS if w in (text or '')]

def click_visible(pg, sel):
    pg.evaluate("""(s) => { const els=[...document.querySelectorAll(s)];
      const vis=els.find(e=>e.offsetParent!==null); (vis||els[0]).click(); }""", sel)

def read_note(pg):
    return pg.evaluate("() => { const el=document.querySelector('#os-dash-week-note'); return el ? el.textContent.trim() : null; }")

def wait_note(pg, timeout_ms=20000):
    try:
        pg.wait_for_function("() => { const el=document.querySelector('#os-dash-week-note'); return el && el.textContent.trim().length > 0; }", timeout=timeout_ms)
    except Exception as e:
        print("note wait timeout:", str(e)[:150], flush=True)

with sync_playwright() as p:
    b = p.firefox.launch(headless=True, firefox_user_prefs={'security.enterprise_roots.enabled': True})

    def intercept(route):
        req = route.request
        if req.method == 'OPTIONS':
            route.fulfill(status=200, headers={'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*'})
            return
        table = req.url.split('/rest/v1/')[-1].split('?')[0].split('/')[0]
        rows = DATA.get(table, []) if MODE == 'data' else []
        route.fulfill(status=200, content_type='application/json',
                      headers={'Access-Control-Allow-Origin': '*'},
                      body=json.dumps(rows))

    # ---- main context: fresh load, lang preset ----
    ctx = b.new_context(viewport={'width': WIDTH, 'height': 844})
    ctx.add_init_script("try{ localStorage.setItem('mw.set.lang', JSON.stringify('%s')); }catch(e){}" % LANG)
    pg = ctx.new_page()
    pg.route('**/rest/v1/**', intercept)
    errs, perrs = [], []
    pg.on('console', lambda m: errs.append(m.type + ': ' + m.text[:200]) if m.type == 'error' else None)
    pg.on('pageerror', lambda e: perrs.append(str(e)[:200]))

    section("PATH A fresh load lang=%s width=%d mode=%s" % (LANG, WIDTH, MODE))
    pg.goto(URL, wait_until='commit', timeout=90000)
    pg.wait_for_timeout(9000)
    print("lang select value:", pg.evaluate("() => (document.querySelector('#mw-set-lang')||{}).value"), flush=True)
    click_visible(pg, '[data-os-go="dashboard"]')
    wait_note(pg)
    pg.wait_for_timeout(4000)
    note_a = read_note(pg)
    print("A note (kind all):", json.dumps(note_a, ensure_ascii=False), "| EN left:", has_en(note_a), flush=True)
    for kind in ['posts', 'notes', 'messages', 'invites']:
        click_visible(pg, '[data-kind-for="dash"] button[data-kind="%s"]' % kind)
        pg.wait_for_timeout(1500)
        n = read_note(pg)
        print("A note (kind %s):" % kind, json.dumps(n, ensure_ascii=False), "| EN left:", has_en(n), flush=True)
    click_visible(pg, '[data-kind-for="dash"] button[data-kind="all"]')
    pg.wait_for_timeout(1200)

    # ---- Path B: switch-after-load, from a CLEAN context (true EN start) ----
    section("PATH B switch-after-load lang=%s (clean context)" % LANG)
    pg.close(); ctx.close()
    ctx = b.new_context(viewport={'width': WIDTH, 'height': 844})
    pg = ctx.new_page()
    pg.route('**/rest/v1/**', intercept)
    pg.on('console', lambda m: errs.append(m.type + ': ' + m.text[:200]) if m.type == 'error' else None)
    pg.on('pageerror', lambda e: perrs.append(str(e)[:200]))
    pg.goto(URL, wait_until='commit', timeout=90000)
    pg.wait_for_timeout(9000)
    print("B start lang select value:", pg.evaluate("() => (document.querySelector('#mw-set-lang')||{}).value"), flush=True)
    click_visible(pg, '[data-os-go="dashboard"]')
    wait_note(pg)
    pg.wait_for_timeout(3000)
    print("B EN baseline note:", json.dumps(read_note(pg), ensure_ascii=False), flush=True)
    try:
        click_visible(pg, '#settingsbtn')
        pg.wait_for_timeout(1800)
        pg.select_option('#mw-set-lang', LANG)
        pg.wait_for_timeout(2500)
        print("switched, select value now:", pg.evaluate("() => (document.querySelector('#mw-set-lang')||{}).value"), flush=True)
    except Exception as e:
        print("settings switch FAILED:", str(e)[:300], flush=True)
    click_visible(pg, '[data-os-go="dashboard"]')
    pg.wait_for_timeout(3000)
    note_b = read_note(pg)
    print("B note after switch (kind all):", json.dumps(note_b, ensure_ascii=False), "| EN left:", has_en(note_b), flush=True)
    for kind in ['posts', 'notes', 'messages', 'invites']:
        click_visible(pg, '[data-kind-for="dash"] button[data-kind="%s"]' % kind)
        pg.wait_for_timeout(1500)
        n = read_note(pg)
        print("B note (kind %s):" % kind, json.dumps(n, ensure_ascii=False), "| EN left:", has_en(n), flush=True)
    pg.close(); ctx.close()

    # ---- console classification ----
    supa = [e for e in errs if 'supabase' in e.lower() or 'Cross-Origin' in e]
    other = [e for e in errs if e not in supa]
    print("console errors total:", len(errs), "supabase/cors:", len(supa), "OTHER:", len(other), "pageerrors:", len(perrs), flush=True)
    for e in other[:5]:
        print("  OTHER ERR:", e[:200], flush=True)
    for e in perrs[:5]:
        print("  PAGEERR:", e[:200], flush=True)
    pg.close(); ctx.close()

    # ---- clean overflow, fresh context, no settings ----
    section("CLEAN OVERFLOW width=%d" % WIDTH)
    ctx2 = b.new_context(viewport={'width': WIDTH, 'height': 844})
    pg2 = ctx2.new_page()
    pg2.route('**/rest/v1/**', intercept)
    pg2.goto(URL, wait_until='commit', timeout=90000)
    pg2.wait_for_timeout(9000)
    print("scroll0:", pg2.evaluate("() => ({iw: innerWidth, sw: document.documentElement.scrollWidth})"), flush=True)
    pg2.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    pg2.wait_for_timeout(1500)
    print("scrolled:", pg2.evaluate("() => ({iw: innerWidth, sw: document.documentElement.scrollWidth})"), flush=True)
    pg2.close(); ctx2.close()
    b.close()
print("F4 PROBE V2 DONE", flush=True)
