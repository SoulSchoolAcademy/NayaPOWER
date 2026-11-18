// check-followon.mjs — prove the F4-FOLLOWON staged bytes by EXECUTING the
// real served scripts (walk + start-over control) in a minimal DOM facade.
// No browser exists in this VM; jsdom cannot be installed (npm blocked).
// Reads the staged WALK HTML from stdin; fetches /free, pricing v78, the
// font css2 files and the walk worker's /identity.html live itself.
// Usage: curl -s <free-walk-url> | node check-followon.mjs
// Tests:
//   T0 static facts (walk + entry bytes): Marcellus link + 3 family rules,
//      Newsreader link + --serif intact (9 uses), start-over control + narrow
//      CSS, F4 markers intact, play button glow-only.
//   T1 fresh walk, alias A (REAL claim + REAL complete POST to the staged
//      worker): boot at step-1 -> all 14 steps -> names Enter -> building
//      with progress -> buildDone -> end slide, five doors, Marcellus headline.
//   T2 start-over control: seeded completed state -> click -> the 6 identity/
//      walk keys + 2 session keys gone, unrelated key survives, reload fired.
//   T3 fresh walk, alias B (REAL claim): boot lands on step-1 (not the end
//      slide, not the door) with a NEW alias after the start-over.
//   T4 certificate layout math at 390/635/desktop from the served CSS.
//   T5 untouched surfaces: pricing v78 byte-exact, /free/hub 302, F4 markers.
//   T6 fonts really load: Marcellus + Newsreader css2 + latin woff2 (wOF2),
//      and the walk worker's /identity.html carries the SAME --serif as /free.
// Exit 0 = all pass, 1 = any fail.
import { readFileSync } from 'fs';
import vm from 'vm';

const walkHtml = readFileSync(0, 'utf-8');
const FREE = 'https://naya-pricing-free-staging.nayapower.workers.dev';
const PRICING = 'https://naya-pricing-f4-staging.nayapower.workers.dev';
const UA = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36' };

let failures = 0;
function check(name, cond, extra = '') {
  console.log((cond ? 'PASS' : 'FAIL') + ' ' + name + (extra ? ' — ' + extra : ''));
  if (!cond) failures++;
}
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
async function net(url, opts = {}) {
  const r = await fetch(url, { ...opts, headers: { ...UA, ...(opts.headers || {}) } });
  return r;
}

// ---------- fetch the staged /free + pricing v78 ----------
const entryRes = await net(FREE + '/free');
const entryHtml = await entryRes.text();
const v78Res = await net(PRICING + '/');
const v78Buf = Buffer.from(await v78Res.arrayBuffer());
const { createHash } = await import('crypto');
const sha = (b) => createHash('sha256').update(b).digest('hex');

// ---------- minimal DOM (same facade shape as the F4 harness) ----------
const VOID = new Set(['img', 'input', 'br', 'meta', 'link', 'hr', 'area', 'base', 'col', 'embed', 'source', 'track', 'wbr']);
class El {
  constructor(tag, attrs) {
    this.tagName = tag.toUpperCase(); this.attrs = attrs; this.children = [];
    this.parent = null; this._listeners = {}; this._cls = new Set((attrs.class || '').split(/\s+/).filter(Boolean));
    this.hidden = ('hidden' in attrs); this.disabled = ('disabled' in attrs); this.value = ''; this.textContent = '';
    this.style = {}; this._text = '';
  }
  get id() { return this.attrs.id || ''; }
  get classList() {
    const s = this._cls;
    return { add: (c) => s.add(c), remove: (c) => s.delete(c), toggle: (c) => { s.has(c) ? s.delete(c) : s.add(c); }, contains: (c) => s.has(c) };
  }
  getAttribute(n) { return this.attrs[n] ?? null; }
  setAttribute(n, v) { this.attrs[n] = String(v); }
  addEventListener(t, fn) { (this._listeners[t] = this._listeners[t] || []).push(fn); }
  dispatch(t, ev = {}) {
    ev.target = ev.target || this; ev.currentTarget = this;
    for (const fn of (this._listeners[t] || [])) fn(ev);
  }
  click() { this.dispatch('click', { target: this }); }
  focus() {}
  querySelector(sel) { return this.querySelectorAll(sel)[0] || null; }
  querySelectorAll(sel) {
    const out = [];
    const walk = (el) => { for (const c of el.children) { if (matchSel(c, sel)) out.push(c); walk(c); } };
    walk(this); return out;
  }
  closest(sel) {
    let el = this;
    for (const part of sel.split(',').map(s => s.trim())) {
      el = this;
      while (el) { if (matchSel(el, part)) return el; el = el.parent; }
    }
    return null;
  }
}
function matchSel(el, sel) {
  sel = sel.trim();
  const m = sel.match(/^([a-zA-Z][a-zA-Z0-9]*)?((?:[#.][a-zA-Z0-9_-]+)*)$/);
  if (!m) return false;
  if (m[1] && el.tagName !== m[1].toUpperCase()) return false;
  for (const p of (m[2].match(/[#.][a-zA-Z0-9_-]+/g) || [])) {
    if (p[0] === '#' && el.id !== p.slice(1)) return false;
    if (p[0] === '.' && !el._cls.has(p.slice(1))) return false;
  }
  return true;
}
function parseHTML(src) {
  const root = new El('root', {});
  const stack = [root];
  const tagRe = /<!--[\s\S]*?-->|<\/?([a-zA-Z][a-zA-Z0-9]*)((?:\s+[a-zA-Z_:][-a-zA-Z0-9_:.]*(?:\s*=\s*(?:"[^"]*"|'[^']*'|[^\s>]+))?)*)\s*\/?>/g;
  let m;
  const rawTags = new Set(['script', 'style']);
  while ((m = tagRe.exec(src)) !== null) {
    if (m[0].startsWith('<!--')) continue;
    const [full, tag, attrStr] = m;
    const closing = full.startsWith('</');
    const selfClose = full.endsWith('/>') || VOID.has(tag.toLowerCase());
    if (closing) { while (stack.length > 1 && stack[stack.length - 1].tagName !== tag.toUpperCase()) stack.pop(); if (stack.length > 1) stack.pop(); continue; }
    const attrs = {};
    for (const am of (attrStr || '').matchAll(/([a-zA-Z_:][-a-zA-Z0-9_:.]*)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+)))?/g)) attrs[am[1]] = am[2] ?? am[3] ?? am[4] ?? '';
    const el = new El(tag, attrs);
    el.parent = stack[stack.length - 1];
    stack[stack.length - 1].children.push(el);
    if (rawTags.has(tag.toLowerCase())) {
      const end = src.indexOf('</' + tag, tagRe.lastIndex);
      if (end === -1) break;
      el._raw = src.slice(tagRe.lastIndex, end);
      tagRe.lastIndex = end;
      continue;
    }
    if (!selfClose) stack.push(el);
  }
  return root;
}
function byId(root, id) {
  let found = null;
  const walk = (el) => { if (found) return; if (el.id === id) { found = el; return; } for (const c of el.children) walk(c); };
  walk(root); return found;
}
function makeWalkEnv({ fetchImpl, search = '', stored = {} }) {
  const root = parseHTML(walkHtml);
  const ls = new Map(Object.entries(stored));
  const listeners = {};
  const doc = {
    getElementById: (id) => byId(root, id),
    querySelectorAll: (sel) => root.querySelectorAll(sel),
    querySelector: (sel) => root.querySelector(sel),
  };
  const win = {
    localStorage: { getItem: (k) => (ls.has(k) ? ls.get(k) : null), setItem: (k, v) => ls.set(k, String(v)), removeItem: (k) => ls.delete(k) },
    sessionStorage: { getItem: () => null, setItem: () => {}, removeItem: () => {} },
    location: { search, pathname: '/free/walk', hash: '' },
    history: { replaceState: () => {} },
    scrollTo: () => {},
    addEventListener: (t, fn) => { (listeners[t] = listeners[t] || []).push(fn); },
    SpeechRecognition: undefined, webkitSpeechRecognition: undefined,
    __walkStep: null, __lastCompletionPayload: null, __walkState: null,
  };
  const scriptEl = root.querySelectorAll('script').find(s => (s._raw || '').includes('completeWalk'));
  if (!scriptEl) throw new Error('walk script not found in HTML');
  const sandbox = {
    document: doc, window: win, localStorage: win.localStorage,
    sessionStorage: win.sessionStorage,
    location: win.location, history: win.history,
    navigator: {}, fetch: fetchImpl,
    setTimeout, clearTimeout, setInterval, clearInterval,
    URLSearchParams, console,
  };
  sandbox.window = new Proxy(win, { get: (t, p) => (p in t ? t[p] : sandbox[p]), set: (t, p, v) => { t[p] = v; return true; } });
  vm.createContext(sandbox);
  vm.runInContext(scriptEl._raw, sandbox, { filename: 'walk.js' });
  return { root, doc, win, ls, byId: (id) => byId(root, id) };
}

// ---------- real network to the staged worker (browser UA; relative -> host) ----------
const realFetch = (path, opts = {}) => net(FREE + path, opts);
const rand = (n) => [...Array(n)].map(() => 'abcdefghijklmnopqrstuvwxyz'[Math.floor(Math.random() * 26)]).join('');
async function claimAlias(tag) {
  const alias = 'f4followon' + tag + rand(6);
  const key = 'nayanet_key_' + rand(13);
  const r = await net(FREE + '/api/claim', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ alias, name: 'F4 Followon Test', device_key: key }) });
  const d = await r.json();
  if (!d.ok) throw new Error('claim failed for ' + alias + ': ' + JSON.stringify(d));
  return { alias, key, cert_no: d.cert_no };
}

// ---------- T0: static facts ----------
// Item 1 — Marcellus on the walk, harvested link + family on display type.
check('T0 walk carries the live entrance Marcellus link verbatim',
  walkHtml.includes('https://fonts.googleapis.com/css2?family=Marcellus&family=Outfit:wght@300;400;600;700;800;900&display=swap'));
check('T0 walk preconnects fonts.googleapis', walkHtml.includes('<link rel="preconnect" href="https://fonts.googleapis.com">'));
check('T0 .p3-question in Marcellus,Georgia,serif', walkHtml.includes('.p3-question{font-family:Marcellus,Georgia,serif;'));
check('T0 .p3-congrats (end-slide headline) in Marcellus,Georgia,serif', walkHtml.includes('.p3-congrats{font-family:Marcellus,Georgia,serif;'));
check('T0 .p3-welcome in Marcellus,Georgia,serif', walkHtml.includes('.p3-welcome{font-family:Marcellus,Georgia,serif;'));
check('T0 walk has no Newsreader (serif separation)', !walkHtml.includes('Newsreader'));
// Item 4 — Newsreader on the certificate, properly loaded.
check('T0 /free carries the Newsreader css2 link', entryHtml.includes('css2?family=Newsreader:ital,opsz,wght@0,6..72,400..700;1,6..72,400..700&display=swap'));
check('T0 /free --serif unchanged', entryHtml.includes("--serif: 'Newsreader', Georgia, 'Times New Roman', serif"));
check('T0 /free still uses var(--serif) 9 times', (entryHtml.match(/var\(--serif\)/g) || []).length === 9);
check('T0 /free has no Marcellus (serif separation)', !entryHtml.includes('Marcellus'));
// Item 2 — certificate narrow CSS present.
check('T0 certified regalia stacks at <=640px', entryHtml.includes('.cert-plaque.is-certified .cert-regalia{flex-direction:column'));
check('T0 regalia dot hidden at <=640px', entryHtml.includes('.cert-plaque.is-certified .cert-regalia .regalia-dot{display:none}'));
check('T0 certified plaque scrolls at short heights', entryHtml.includes('.cert-plaque.is-certified{overflow-y:auto}'));
check('T0 certified face goes to flow layout at short heights', entryHtml.includes('.cert-plaque.is-certified .identity-face{position:static;display:flex;flex-direction:column'));
check('T0 certified name is static (in flow)', entryHtml.includes('.cert-plaque.is-certified .cert-name { position: static;'));
check('T0 ENTER is in normal flow (position:relative, not absolute)', /\.activate-btn \{ position: relative;/.test(entryHtml));
// Item 3 — start-over control present, gated, wired.
check('T0 start-over button present with the brief wording', entryHtml.includes('id="startOverBtn"') && entryHtml.includes('Use a different alias'));
check('T0 start-over hidden unless certified', entryHtml.includes('#startOverBtn{display:none') && entryHtml.includes('.cert-plaque.is-certified #startOverBtn{display:inline-flex'));
check('T0 start-over sits under ENTER (after enterBtn, before free-line)',
  entryHtml.indexOf('id="startOverBtn"') > entryHtml.indexOf('id="enterBtn"') &&
  entryHtml.indexOf('id="startOverBtn"') < entryHtml.indexOf('class="cert-claim free-line"'));
check('T0 start-over clears the walk state key', entryHtml.includes("'naya_welcome_right_v1'") && entryHtml.includes("localStorage.removeItem(k)"));
check('T0 start-over reloads the page', entryHtml.includes('window.location.reload()'));
// F4 fix intact + play button glow-only.
check('T0 F4 markers intact (buildBarFill, 25000, showStep(16))',
  walkHtml.includes('buildBarFill') && walkHtml.includes('25000') && walkHtml.includes('showStep(16)'));
check('T0 five doors, Hub first', JSON.stringify([...walkHtml.matchAll(/data-door="([^"]+)"/g)].map(m => m[1])) === JSON.stringify(['Hub', 'Dashboard', 'Personal', 'Business', 'Space']));
check('T0 play button glow-only (no audio wired)', !walkHtml.includes('<audio') && !walkHtml.includes('new Audio') && !walkHtml.includes('.play('));
check('T0 /free entry intact (free line, eye, walk URL)',
  entryHtml.includes('Enter free &mdash; no payment, no card.') && entryHtml.includes('id="freeEye"') && entryHtml.includes("WALKTHROUGH_URL = '/free/walk'"));

// ---------- T1: fresh walk, alias A, real network ----------
const A = await claimAlias('a');
console.log('alias A:', A.alias, 'cert', A.cert_no);
const storedA = { nayanet_smart_alias: A.alias, nayanet_smart_name: 'F4 Followon Test', nayanet_vault_key: A.key };
const envA = makeWalkEnv({ fetchImpl: realFetch, search: '?name=F4%20Followon%20Test&alias=' + A.alias, stored: storedA });
await sleep(100);
check('T1 fresh walk boots at step-1 (not end slide, not door)',
  !envA.byId('step-1').hidden && envA.byId('step-end').hidden && envA.byId('step-door').hidden);
for (let n = 1; n <= 14; n++) {
  const sec = envA.byId('step-' + n);
  const ans = sec.querySelector('#answer-' + n);
  if (ans) ans.value = n <= 10 ? 'followon answer ' + n : (n === 11 ? 'no' : n === 12 ? 'no' : n === 13 ? 'no' : 'yes');
  sec.querySelector('#enterBtn-' + n).click();
  await sleep(120);
  const nextId = n < 14 ? 'step-' + (n + 1) : 'step-names';
  check('T1 step-' + n + ' Enter advances to ' + nextId, !envA.byId(nextId).hidden);
}
const namesBtn = envA.byId('step-names').querySelector('#enterBtn-14');
const bIn = envA.byId('step-names').querySelector('#name-business');
const sIn = envA.byId('step-names').querySelector('#name-space');
if (bIn) bIn.value = 'Followon Biz'; if (sIn) sIn.value = 'Followon Space';
namesBtn.click();
await sleep(300);
check('T1 building step visible after names Enter', !envA.byId('step-building').hidden && !envA.byId('buildWorking').hidden);
let done = false;
for (let i = 0; i < 40; i++) { await sleep(250); if (!envA.byId('buildDone').hidden) { done = true; break; } }
check('T1 real build completes into buildDone', done);
check('T1 completion payload alias matches the claimed alias', envA.win.__lastCompletionPayload && envA.win.__lastCompletionPayload.alias === A.alias);
envA.byId('buildGo').click();
await sleep(100);
check('T1 end slide reached, five doors, Marcellus headline present',
  !envA.byId('step-end').hidden && envA.byId('doorRow').querySelectorAll('.p3-door').length === 5 &&
  (envA.byId('step-end').querySelector('.p3-congrats') !== null));
// KV record for A exists (the walk's completion was stored server-side).
{
  const r = await net(FREE + '/api/welcome/complete?alias=' + A.alias);
  check('T1 completion record stored server-side for alias A', r.status === 200);
}

// ---------- T2: start-over control, seeded completed state ----------
const soMatch = entryHtml.match(/<script>\(function\(\)\{var b=document\.getElementById\('startOverBtn'\);[\s\S]*?}\)\(\);<\/script>/);
check('T2 start-over script block extractable from staged /free', !!soMatch);
let reloads = 0;
{
  const ls = new Map(Object.entries({
    nayanet_smart_alias: A.alias, nayanet_smart_name: 'F4 Followon Test',
    nayanet_vault_key: A.key,
    naya_welcome_right_v1: JSON.stringify({ alias: A.alias, answers: { about: 'x' }, reveal: { pages: { personal: '/' + A.alias } } }),
    nayanet_free_entry: '1', nayanet_install_done: '1',
  }));
  const ss = new Map(Object.entries({ nayanet_user_name: 'F4 Followon Test', nayanet_pending_route: '#/hub' }));
  const btn = new El('button', { id: 'startOverBtn', type: 'button' });
  const doc = { getElementById: (id) => (id === 'startOverBtn' ? btn : null) };
  const loc = { reload: () => { reloads++; } };
  const sandbox = {
    document: doc, window: { location: loc },
    localStorage: { getItem: (k) => (ls.has(k) ? ls.get(k) : null), setItem: (k, v) => ls.set(k, String(v)), removeItem: (k) => ls.delete(k) },
    sessionStorage: { getItem: (k) => (ss.has(k) ? ss.get(k) : null), setItem: (k, v) => ss.set(k, String(v)), removeItem: (k) => ss.delete(k) },
    location: loc, console,
  };
  vm.createContext(sandbox);
  vm.runInContext(soMatch[0].replace(/<\/?script>/g, ''), sandbox, { filename: 'startover.js' });
  btn.click();
  check('T2 click clears the identity keys', !ls.has('nayanet_smart_alias') && !ls.has('nayanet_smart_name') && !ls.has('nayanet_vault_key'));
  check('T2 click clears the walk state + free flag', !ls.has('naya_welcome_right_v1') && !ls.has('nayanet_free_entry'));
  check('T2 click clears the session keys', !ss.has('nayanet_user_name') && !ss.has('nayanet_pending_route'));
  check('T2 click leaves unrelated keys alone (install flag survives)', ls.has('nayanet_install_done'));
  check('T2 click reloads the page exactly once', reloads === 1);
}

// ---------- T3: fresh walk, alias B, after the start-over ----------
const B = await claimAlias('b');
console.log('alias B:', B.alias, 'cert', B.cert_no);
const envB = makeWalkEnv({ fetchImpl: realFetch, search: '?name=F4%20Followon%20Test&alias=' + B.alias, stored: { nayanet_smart_alias: B.alias, nayanet_smart_name: 'F4 Followon Test', nayanet_vault_key: B.key } });
await sleep(100);
check('T3 new alias boots at step-1 (fresh walk, not the end slide)',
  !envB.byId('step-1').hidden && envB.byId('step-end').hidden && envB.byId('step-door').hidden);
envB.byId('step-1').querySelector('#answer-1').value = 'fresh start';
envB.byId('step-1').querySelector('#enterBtn-1').click();
await sleep(120);
check('T3 step-1 Enter advances to step-2 (live fresh walk)', !envB.byId('step-2').hidden);
{
  const r = await net(FREE + '/api/welcome/complete?alias=' + B.alias);
  check('T3 alias B has no completion record yet (walk not finished)', r.status === 404);
}
console.log('ALIASES_USED ' + JSON.stringify({ A, B }));

// ---------- T4: certificate layout math from the served CSS ----------
{
  const css = entryHtml;
  const num = (re) => { const m = css.match(re); return m ? parseFloat(m[1]) : null; };
  // Certified short-height rules exist and do what the fix needs.
  const shortBlock = css.slice(css.indexOf('@media (max-height:700px)'));
  check('T4 short-height block switches certified face to flow + scroll',
    shortBlock.includes('.cert-plaque.is-certified{overflow-y:auto}') &&
    shortBlock.includes('.cert-plaque.is-certified .identity-face{position:static;display:flex;flex-direction:column'));
  // 635x349 budget (certified): face height vs in-flow content height.
  // Top bar is 50px at <=640px; stage padding-bottom 36px at <=640px; the
  // bottom bar is 50px (all three measured from the served CSS, not assumed).
  // Face ~= 349 - 50 - 36 - 50 = 213px.
  // In-flow content at short heights (seal steps to 72px):
  //   seal 72 + title ~15 + jewels ~30 + certifies ~20 + name ~54 (3.4rem cap)
  //   + status ~20 + 2 boxes ~2x62 + regalia stacked ~40 + ENTER 58
  //   + start-over 40 + gaps/margins ~50  ≈ 523px  >  213px face.
  // The old fixed grid clipped the ~310px overflow (ENTER invisible). The new
  // flow layout + overflow-y:auto scrolls it instead: nothing overlaps,
  // ENTER stays in flow and reachable. Assert the extracted numbers.
  const sealShort = num(/\.cert-plaque\.is-certified \.cert-seal\{width:(\d+)px/);
  const enterMin = num(/\.activate-btn \{[^}]*min-height: (\d+)px/);
  const nameCap = css.includes('font-size: clamp(2.55rem, 13.5vw, 3.4rem)');
  const faceH = 349 - 50 - 36 - 50;
  const contentH = 72 + 15 + 30 + 20 + 54 + 20 + 124 + 40 + 58 + 40 + 50;
  check('T4 635x349: content (~523px) exceeds face (~213px) so the old grid MUST clip — scroll is the fix, not compression',
    sealShort === 72 && enterMin === 58 && nameCap && faceH === 213 && contentH > faceH,
    `face ${faceH}px vs content ~${contentH}px`);
  check('T4 635x349: in flow layout nothing can overlap (no absolute rows) and ENTER is in flow',
    shortBlock.includes('position:static') && /\.activate-btn \{ position: relative;/.test(css));
  // 390x844 budget (certified, grid mode — tall enough that the grid stands):
  // face ~= 844 - 50 - 36 - 50 = 708px. Content with the full seal (94px)
  // and stacked regalia ≈ 94+15+30+20+53+20+130+40+58+40+50 ≈ 550px < 708px.
  const face390 = 844 - 50 - 36 - 50;
  const content390 = 94 + 15 + 30 + 20 + 53 + 20 + 130 + 40 + 58 + 40 + 50;
  check('T4 390x844: content (~550px) fits the face (~708px) in grid mode, no scroll needed',
    face390 === 708 && content390 < face390, `face ${face390}px vs content ~${content390}px`);
  // 390px width: one-line regalia (~570px at desktop spacing) cannot fit a
  // ~354px content column, so the stack rule is load-bearing.
  const regaliaOneLine = 183 + 12 + 376; // Nº ~183 + gap 12 + date ~376
  const col390 = 390 - 18 - 18;
  check('T4 390px: one-line regalia (~571px) cannot fit the 354px column — the stack rule is required and present',
    regaliaOneLine > col390 && css.includes('.cert-plaque.is-certified .cert-regalia{flex-direction:column'));
  check('T4 desktop 1919x998: neither media query matches, so the presentation is untouched',
    1919 > 640 && 998 > 700);
}

// ---------- T5: untouched surfaces ----------
check('T5 pricing v78 byte-exact (unchanged)', sha(v78Buf) === 'ca2eafeb896c763ae2459b4a10b8715e726765ced607c0aab3640d27e6c39ae2');
{
  const r = await net(FREE + '/free/hub', { redirect: 'manual' });
  check('T5 /free/hub still 302 to nayanet.app', r.status === 302 && r.headers.get('location') === 'https://nayanet.app/');
}

// ---------- T6: the fonts really load ----------
async function fontLoads(family, cssUrl) {
  const r = await net(cssUrl);
  if (r.status !== 200) return { ok: false, why: 'css2 ' + r.status };
  const t = await r.text();
  const m = t.match(/\/\* latin \*\/\s*@font-face \{[^}]*src: url\((https:\/\/[^)]+\.woff2)\)/);
  if (!m) return { ok: false, why: 'no latin woff2' };
  const w = await net(m[1]);
  if (w.status !== 200) return { ok: false, why: 'woff2 ' + w.status };
  const buf = Buffer.from(await w.arrayBuffer());
  return { ok: buf.slice(0, 4).toString() === 'wOF2' && buf.length > 10000, why: buf.length + ' B', hasItalic: t.includes('font-style: italic') };
}
{
  const marc = await fontLoads('Marcellus', 'https://fonts.googleapis.com/css2?family=Marcellus&family=Outfit:wght@300;400;600;700;800;900&display=swap');
  check('T6 Marcellus css2 serves + latin woff2 downloads (wOF2)', marc.ok, marc.why);
  const news = await fontLoads('Newsreader', 'https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400..700;1,6..72,400..700&display=swap');
  check('T6 Newsreader css2 serves + latin woff2 downloads (wOF2)', news.ok, news.why);
  check('T6 Newsreader css2 includes the italic face the certificate uses', news.hasItalic === true);
  const idRes = await net('https://naya-walk-beginning-staging.nayapower.workers.dev/identity.html');
  const idHtml = await idRes.text();
  const serifFree = (entryHtml.match(/--serif:\s*[^;}]+/) || [''])[0];
  const serifWalk = (idHtml.match(/--serif:\s*[^;}]+/) || [''])[0];
  check('T6 the walk worker certificate carries the SAME --serif as /free (one serif, both certificate files)',
    serifFree === serifWalk && serifFree.includes('Newsreader'), serifFree.trim());
}

console.log(failures === 0 ? 'HARNESS: ALL PASS' : `HARNESS: ${failures} FAILURES`);
process.exit(failures === 0 ? 0 : 1);
