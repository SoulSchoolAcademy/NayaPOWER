#!/usr/bin/env python3
"""Assemble the Official Welcome — LIVE walk (10 question slides + end slide v2).

Method (harvest, not reinvention):
- Steps: FINAL2 preview (slide 1) + slides 02-10 + end slide v2, each
  <main> block VERBATIM except element ids suffixed per step (so one page
  can hold all ten steps). Questions verified verbatim against the locked
  flow; progress cues N of 10; jewel labels/actions untouched.
- Stylesheet: middle.css = the end-slide stylesheet (verified: it contains
  the full question-slide stylesheet as a substring, plus door/linkchip
  classes). No preview comments ship: the head is written clean.
- Frame: the identity frame div ONCE (a page frame, not a step element).
- Photos: the 5 portrait data-URIs ONCE in a JS PHOTOS map, assigned to
  step images at boot — the live walk's own mechanism (the live walk
  embeds its images as data URIs; see walk.html's brand-mark/logo-hero).
  Cycle verified: slides 1-5 = photos 1-5, slides 6-10 repeat, end reuses
  photo 1. Byte-identical embeds, never re-encoded.
- Script: app.js, the generalized preview script with LIVE wiring only:
  complete() POSTs /api/welcome/complete; boot verifies /api/welcome/me
  and shows the certificate door unless verified; end doors navigate to
  real URLs; no preview-only markers, no faked audio (slots empty, glow
  only). Topics: [] — no picker (live-step decision; shape preserved).
- Server: UNCHANGED stage below (worker-pre-right.js -> server-stage1.js
  with the real-claim credential auth, apiComplete/apiSettings/apiMe/
  apiOwner/worldPage/router). transform2.py then applies THE JOINING +
  flagship render + walk embedding -> worker.js (candidate via WORKER_OUT).
Outputs: walk.html (inspection), server-stage1.js (transform2 input).
"""
import json, re, os

HERE = "/home/hatch/workspace/welcome-build"

def read(f):
    with open(os.path.join(HERE, f)) as fh:
        return fh.read()

def style_of(s):
    return s[s.find('<style>'):s.find('</style>') + len('</style>')]

def main_of(s):
    m = re.search(r'<main class="p3-main">.*?</main>', s, re.S)
    assert m, 'no main block'
    return m.group(0)

def frame_of(s):
    m = re.search(r'<div class="p3-frame".*?</div>', s, re.S)
    assert m, 'no frame'
    return m.group(0)

def uris_of(s):
    return re.findall(r'data:image/[^;]+;base64,[A-Za-z0-9+/=]+', s)

QUESTIONS = [
    ('about', 'Tell me who you are, in your own words'),
    ('into', 'What are you into, and why?'),
    ('vision', 'What is your vision?'),
    ('mission', 'What is your mission?'),
    ('motto', 'What is your motto?'),
    ('goal', 'Your goal — for your life'),
    ('biz_do', 'What do you do?'),
    ('biz_offer', 'What do you offer?'),
    ('biz_building', "What are you building, and what's the goal?"),
    ('space', 'What kind of space do you want around it, and who do you want to meet there?'),
]
SLIDE_FILES = ['walk-page3-v10-FINAL2.html'] + ['walk-slide-%02d.html' % i for i in range(2, 11)]

def main():
    slides = [read(f) for f in SLIDE_FILES]
    end = read('walk-slide-end-v2.html')

    # --- stylesheet checks (fail loudly) ---
    qstyle = style_of(slides[0])
    estyle = style_of(end)
    assert qstyle[:-len('</style>')] in estyle[:-len('</style>')], 'question CSS is not inside end CSS'
    for s in slides[1:]:
        assert style_of(s) == qstyle, 'question CSS differs across slides'
    middle_css = read('middle.css')
    assert middle_css == estyle, 'middle.css is not the end-slide stylesheet'

    # --- photos: 5 distinct portraits, cycle verified, byte-identical ---
    big = [uris_of(s)[1] for s in slides]
    assert len(set(big)) == 5, 'expected exactly 5 distinct portraits, got %d' % len(set(big))
    photos = big[:5]
    for i in range(10):
        assert big[i] == photos[i % 5], 'photo cycle broken at slide %d' % (i + 1)
    assert uris_of(end)[1] == photos[0], 'end slide photo is not photo 1'
    assert len(set(uris_of(s)[0] for s in slides + [end])) == 1, 'crest URI differs'

    # --- per-step mains, ids suffixed, questions verbatim ---
    step_mains = []
    for i, s in enumerate(slides):
        n = i + 1
        m = main_of(s)
        q = re.search(r'<h1 class="p3-question">(.*?)</h1>', m).group(1)
        assert q == '"%s"' % QUESTIONS[i][1], 'question mismatch step %d: %s' % (n, q)
        assert ('%d of 10' % n) in m, 'progress cue missing step %d' % n
        m = re.sub(r'id="([A-Za-z0-9_-]+)"', r'id="\1-%d"' % n, m)
        step_mains.append(m)

    end_main = main_of(end)
    assert 'Congratulations' in end_main and 'data-door="Dashboard"' in end_main

    # --- top-group template (from FINAL2), portrait src assigned by JS ---
    top_tpl = '''<div class="p3-naya p3-naya-flank" data-top="STEPN"><span class="p3-flank-side p3-flank-left">
<img class="p3-flank-photo" data-photo="PHOTON" src="" alt="Naya">
</span>
<button class="p3-naya-play" id="playBtn-STEPN" type="button" aria-label="PLAYLABEL"><svg viewBox="0 0 24 24" width="24" height="24" fill="#fff" aria-hidden="true"><path d="M7 4l13 8-13 8z"/></svg><span class="p3-play-tip">PLAYLABEL</span></button>
<span class="p3-flank-side p3-flank-right"><span class="p3-logo-top">NAYA</span></span></div>'''

    steps_html = []
    for i in range(10):
        n = i + 1
        top = top_tpl.replace('STEPN', str(n)).replace('PHOTON', str(i % 5)).replace(
            'PLAYLABEL', 'Naya will talk you through this page')
        steps_html.append('<section class="p3-step" id="step-%d" data-key="%s" hidden>\n%s\n%s\n</section>'
                          % (n, QUESTIONS[i][0], top, step_mains[i]))
    end_top = top_tpl.replace('STEPN', 'end').replace('PHOTON', '0').replace(
        'PLAYLABEL', 'Naya will welcome you here')
    steps_html.append('<section class="p3-step" id="step-end" data-key="end" hidden>\n%s\n%s\n</section>'
                      % (end_top, end_main))

    # --- door fallback (LIVE: real certificate link, not a staging note) ---
    door_html = '''<section class="p3-step" id="step-door" hidden>
<main class="p3-main">
<h1 class="p3-question">"Welcome starts with your certificate."</h1>
<p class="p3-note">This walk opens after your certificate. If this device does not know you yet, claim your Smart Identity first — thirty seconds, and this page will greet you by name.</p>
<div class="p3-doors"><a class="p3-door" href="https://nayanet.nayapower.workers.dev/identity.html" style="--dc:#a06bff">Get My Certificate</a></div>
<p class="p3-note">Already certified on this device? Open your Hub once — it sets this device's memory — then come back, and the walk will know you.</p>
</main>
</section>'''

    # --- script: app.js with PHOTOS + KEYS substituted ---
    app_js = read('app.js')
    photos_js = ',\n'.join(json.dumps(p) for p in photos)
    keys_js = ', '.join(json.dumps(k) for k, _ in QUESTIONS)
    assert '__PHOTOS__' in app_js and '__KEYS__' in app_js, 'app.js placeholders missing'
    app_js = app_js.replace('__PHOTOS__', photos_js).replace('__KEYS__', keys_js)

    head = ('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">\n'
            '<meta name="theme-color" content="#000000">\n'
            '<title>The Official Welcome | NayaNET</title>\n'
            '<!-- The Official Welcome — live walk. Built by assemble.py from FINAL2 + slides 02-10 + end slide v2 + live app.js. -->\n'
            + middle_css + '\n</head>\n')
    html = (head + '<body>\n' + frame_of(slides[0]) + '\n'
            + '\n'.join(steps_html) + '\n' + door_html + '\n'
            + '<script>\n' + app_js + '\n</script>\n</body>\n</html>\n')
    assert '__lastCompletionPayload' not in html, 'preview marker leaked into walk.html'
    assert 'Preview only' not in html and 'PREVIEW ONLY' not in html, 'preview text leaked into walk.html'
    assert '__PHOTOS__' not in html and '__KEYS__' not in html, 'unsubstituted placeholder in walk.html'
    open(os.path.join(HERE, 'walk.html'), 'w').write(html)
    print('walk.html bytes:', len(html.encode()))
    print('checks:',
          '| step sections:', html.count('class="p3-step"'),
          '| questions verbatim:', sum(1 for _, q in QUESTIONS if ('"%s"' % q) in html),
          '| door:', html.count('id="step-door"'),
          '| end:', html.count('id="step-end"'),
          '| photos embedded once:', len(photos),
          '| portrait bytes:', sum(len(p) for p in photos))

if __name__ == '__main__':
    main()
# ---------------------------------------------------------------- server
old = None
# NOTE: worker.js currently holds the OLD worker; the transform source is
# the same file — read it fully before overwriting.
old = open(HERE + "/backups/worker-pre-right.js").read()  # pristine pre-rebuild worker (harvest source)

def between(s, a, b):
    i = s.index(a); j = s.index(b, i)
    return i, j

def replace_between(s, a, b, new):
    i, j = between(s, a, b)
    return s[:i] + new + s[j:]

def delete_between(s, a, b):
    i, j = between(s, a, b)
    return s[:i] + s[j:]

HEADER = """// naya-welcome — THE OFFICIAL WELCOME, built right (2026-10-24).
// The page AFTER identity: nayanet.live/welcome · /api/welcome/* · /world/*.
// Identity is NOT built here — the Smart Identity Activation already
// certifies the citizen (nayanet_identities: alias · name · device_key ·
// cert_no) and hands them to nayanet.live, where the Hub greets them by
// the device-local identity store. This walk reads THAT store, verifies
// it with the registry, and asks only the ten questions that build the
// world. There is no begin endpoint and no claim form — never was again.
// Server core: the proven previous worker (matches v1 · jewel covers ·
// world pages with server-side privacy), re-authenticated on the real
// claim's credential. Privacy law: findable != visible — a private page
// serves the CONNECT LAYER ONLY to anyone but its owner.

"""
i = old.index('const SB_URL')
srv = HEADER + old[i:]

# WALK_HTML const after NAME_RE
anchor = "const NAME_RE = /^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$/;"
assert anchor in srv
srv = srv.replace(anchor, anchor + "\nconst WALK_HTML = /*__WALK_HTML__*/ '';", 1)

# delete HER VOICE block (CLIPS/NAYA_LINES live in the walk document now)
srv = delete_between(srv, '// ─── HER VOICE', 'const DEFAULT_SETTINGS')

# replace cookie/owner section with the real-claim credential auth
AUTH_BLOCK = """// ─── CITIZEN AUTH — the real claim's credential ─────────────────────────
// A completed claim leaves the device-local identity in localStorage on
// this origin — nayanet_smart_name / nayanet_smart_alias /
// nayanet_vault_key — the same store the Hub greets from. Clients present
// {alias, device_key, name} from that store. A presented vault key must
// match the registry row exactly. When this origin holds no key (the
// claim keeps its own copy on the identity origin), the device's stored
// name must match the certificate's name — the device-local trust the
// Hub itself runs on. Nothing new is minted here: no cookie, no token.
async function getIdentity(env, alias) {
  const r = await sb(env, 'GET', 'nayanet_identities?alias=eq.' + encodeURIComponent(alias) + '&select=alias,name,device_key,cert_no,created_at');
  return (r.ok && Array.isArray(r.data) && r.data.length) ? r.data[0] : null;
}
async function authCitizen(env, body) {
  const alias = typeof body.alias === 'string' ? body.alias.trim().toLowerCase() : '';
  if (!NAME_RE.test(alias)) return { error: err(400, 'That alias does not look right — come in through your Hub, where this device already knows you.') };
  const id = await getIdentity(env, alias);
  if (!id) return { error: err(404, 'That alias is not certified yet — your certificate comes first, then this walk knows your name.') };
  const key = typeof body.device_key === 'string' ? body.device_key : '';
  if (key) {
    if (key !== id.device_key) return { error: err(403, 'This device key does not match that certificate — open the Welcome on the device that claimed this alias.') };
  } else {
    const nm = typeof body.name === 'string' ? body.name.trim().toLowerCase() : '';
    if (!nm || nm !== String(id.name).trim().toLowerCase()) {
      return { error: err(403, 'We could not confirm this world is yours on this device — come in through your Hub, on the device that claimed this alias.') };
    }
  }
  return { id };
}
async function getWorld(env, alias) {
  const r = await sb(env, 'GET', 'citizen_worlds?alias=eq.' + encodeURIComponent(alias) + '&select=*');
  return (r.ok && Array.isArray(r.data) && r.data.length) ? r.data[0] : null;
}
"""
srv = replace_between(srv, '// ─── COOKIES / OWNER', 'const esc =', AUTH_BLOCK)

# delete the old ceremony client (the walk document carries its own)
srv = delete_between(srv, '// ─── CEREMONY CLIENT LOGIC', '// ─── API HANDLERS')

# delete apiBegin entirely — there is no claim here, ever again
srv = delete_between(srv, 'async function apiBegin', 'const ANSWER_KEYS')

API_COMPLETE = """async function apiComplete(request, env) {
  const body = await parseBody(request);
  if (!body) return err(400, 'We could not read your answers — they are still on your screen; try once more.');
  const auth = await authCitizen(env, body);
  if (auth.error) return auth.error;
  const id = auth.id;
  const alias = id.alias;
  const existing = await getWorld(env, alias);
  const settings = existing ? normSettings(existing) : JSON.parse(JSON.stringify(DEFAULT_SETTINGS));
  const world = {
    alias, name: id.name,
    answers: cleanAnswers(body.answers),
    topics: cleanTopics(body.topics),
    settings, updated_at: new Date().toISOString()
  };
  const up = await sb(env, 'POST', 'citizen_worlds', world, 'resolution=merge-duplicates,return=representation');
  if (!up.ok || !Array.isArray(up.data) || !up.data.length) {
    return err(500, 'Something went wrong on our side while building your world — your answers are still on your screen. Please try once more.');
  }
  const saved = up.data[0];
  saved.settings = normSettings(saved);
  const matches = await matchesFor(env, saved);
  return json(200, {
    pages: { personal: '/world/' + alias, business: '/world/' + alias + '/business', space: '/world/' + alias + '/space' },
    matches, settings: saved.settings
  });
}

"""
srv = replace_between(srv, 'async function apiComplete', 'async function apiSettings', API_COMPLETE)

API_SETTINGS_ME_OWNER = """async function apiSettings(request, env) {
  const body = await parseBody(request);
  if (!body) return err(400, 'We could not read that change — try again.');
  const auth = await authCitizen(env, body);
  if (auth.error) return auth.error;
  const id = auth.id;
  const page = body.page;
  if (!['personal', 'business', 'space'].includes(page)) return err(400, 'That page name is not one of yours.');
  const visibility = body.visibility === 'private' ? 'private' : 'public';
  const findable = body.findable === true;
  const world = await getWorld(env, id.alias);
  if (!world) return err(404, 'Your world has not been built yet — finish the welcome first.');
  const settings = normSettings(world);
  settings[page] = { visibility, findable };
  const up = await sb(env, 'PATCH', 'citizen_worlds?alias=eq.' + encodeURIComponent(id.alias), { settings, updated_at: new Date().toISOString() });
  if (!up.ok) return err(500, 'That did not save on our side — please try again in a moment.');
  return json(200, { ok: true, settings });
}

async function apiMe(request, env) {
  const body = await parseBody(request);
  if (!body) return err(400, 'We could not read that — reload the welcome and try again.');
  const alias = typeof body.alias === 'string' ? body.alias.trim().toLowerCase() : '';
  if (!NAME_RE.test(alias)) return err(400, 'That alias does not look right.');
  const id = await getIdentity(env, alias);
  if (!id) return err(404, 'That alias is not certified yet.');
  const world = await getWorld(env, alias);
  const key = typeof body.device_key === 'string' ? body.device_key : '';
  return json(200, {
    name: id.name, alias: id.alias, cert_no: id.cert_no, created_at: id.created_at,
    has_world: !!world, owner: !!key && key === id.device_key
  });
}

// The owner's own view of their world pages, delivered only to the
// device that holds the identity — private content never rides in the
// anonymous server render; it arrives here, after the credential check.
async function apiOwner(request, env) {
  const body = await parseBody(request);
  if (!body) return err(400, 'We could not read that — try again.');
  const auth = await authCitizen(env, body);
  if (auth.error) return auth.error;
  const page = ['personal', 'business', 'space'].includes(body.page) ? body.page : 'personal';
  const world = await getWorld(env, auth.id.alias);
  if (!world) return json(200, { html: '', settings: null });
  world.settings = normSettings(world);
  const settings = world.settings;
  let fragment;
  if (page === 'personal') {
    const matches = await matchesFor(env, world);
    fragment = personalBody(world, matches, settings, true);
  } else if (settings[page].visibility === 'private') {
    fragment = page === 'business' ? businessBody(world, settings, true) : spaceBody(world, settings, true);
  } else {
    fragment = ownerSettingsBar(world.alias, settings);
  }
  return json(200, { html: fragment, settings });
}

"""
srv = replace_between(srv, 'async function apiSettings', '// ─── WORLD ROUTES', API_SETTINGS_ME_OWNER)

WORLD_PAGE = """async function worldPage(request, env, alias, page) {
  const world = await getWorld(env, alias);
  if (!world) return html(404, renderNotFound(alias));
  world.settings = normSettings(world);
  const s = world.settings[page];
  if (s.visibility === 'private') {
    // Server-side privacy: anyone but the owner gets the connect layer
    // only. The owner upgrades in place via /api/welcome/owner, on the
    // real claim's credential — private answers never ship anonymously.
    return html(200, renderConnectLayer(world, null));
  }
  if (page === 'personal') {
    const matches = await matchesFor(env, world);
    return html(200, renderPersonal(world, matches, world.settings));
  }
  if (page === 'business') return html(200, renderBusiness(world, world.settings));
  return html(200, renderSpace(world, world.settings));
}

"""
srv = replace_between(srv, 'async function worldPage', '// ─── ROUTER', WORLD_PAGE)

ROUTER = """// ─── ROUTER ────────────────────────────────────────────────────────────────
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;
    if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: CORS });
    if (!env.SUPABASE_SERVICE_ROLE_KEY) {
      const msg = 'The welcome is not fully switched on yet — please try again later.';
      return path.startsWith('/api/') ? err(500, msg) : html(500, '<body style="background:#040405;color:#fff;font-family:Georgia,serif;padding:44px"><h1>' + msg + '</h1></body>');
    }
    if (path === '/welcome' && request.method === 'GET') return html(200, WALK_HTML);
    if (path === '/api/welcome/me' && request.method === 'POST') return apiMe(request, env);
    if (path === '/api/welcome/complete' && request.method === 'POST') return apiComplete(request, env);
    if (path === '/api/welcome/settings' && request.method === 'POST') return apiSettings(request, env);
    if (path === '/api/welcome/owner' && request.method === 'POST') return apiOwner(request, env);
    const m = path.match(/^\\/world\\/([a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)(?:\\/(business|space))?\\/?$/);
    if (m && request.method === 'GET') return worldPage(request, env, m[1], m[2] || 'personal');
    if (path.startsWith('/world/')) return html(404, renderNotFound(path.split('/')[2] || ''));
    return html(404, '<body style="background:#040405;color:#fff;font-family:Georgia,serif;padding:44px"><h1>Nothing lives at this address.</h1><p><a style="color:#a06bff" href="/welcome">The Official Welcome →</a></p></body>');
  }
};
"""
i = srv.index('// ─── ROUTER')
srv = srv[:i] + ROUTER

open(HERE + "/server-stage1.js", "w").write(srv)
print("server stage1 bytes:", len(srv.encode()))
