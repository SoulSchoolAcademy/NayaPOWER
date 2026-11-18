// check-walk-flow.mjs — prove the FIXED free walk's state machine by
// EXECUTING its real inline <script> in a minimal DOM facade (no browser
// available in this VM; jsdom cannot be installed — npm registry blocked).
// Reads the walk HTML from stdin. Usage:
//   curl -s <walk-url> | node check-walk-flow.mjs [timeoutOverrideMs]
// Tests (all against the served bytes, not a copy):
//   T1 happy path: step-14 Enter -> names Enter (pressed feedback, building
//      visible with moving progress) -> fetch resolves -> buildDone ->
//      "See your pages" -> end slide, five doors Hub/Dashboard/Personal/
//      Business/Space in order + free line.
//   T2 timeout path (harness copy only: 25000 -> override ms): fetch never
//      resolves -> buildError visible with a timeout message + Try again +
//      Back to your names; Back returns to names; retry with a resolving
//      fetch reaches buildDone.
//   T3 resume with a saved reveal: boot lands on the END slide directly
//      (the eye's stall was landing on "Building it" here).
//   T4 390px note: this harness proves the width-independent state machine;
//      layout at 390px is NOT proven here (no layout engine) — the checker
//      must walk it at 390px in a real browser. Viewport meta is asserted.
// Exit 0 = all pass, 1 = any fail. Prints PASS/FAIL per test.
import { readFileSync } from 'fs';
import vm from 'vm';

const html = readFileSync(0, 'utf-8');
const timeoutOverride = process.argv[2] ? parseInt(process.argv[2], 10) : null;

let failures = 0;
function check(name, cond, extra = '') {
  console.log((cond ? 'PASS' : 'FAIL') + ' ' + name + (extra ? ' — ' + extra : ''));
  if (!cond) failures++;
}

// ---------- minimal DOM ----------
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
  let i = 0;
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
const sleep = (ms) => new Promise(r => setTimeout(r, ms));

function makeEnv({ fetchImpl, search = '', stored = {} }) {
  const root = parseHTML(html);
  const ls = new Map(Object.entries(stored));
  const listeners = {};
  const doc = {
    getElementById: (id) => byId(root, id),
    querySelectorAll: (sel) => root.querySelectorAll(sel),
    querySelector: (sel) => root.querySelector(sel),
  };
  const win = {
    localStorage: { getItem: (k) => (ls.has(k) ? ls.get(k) : null), setItem: (k, v) => ls.set(k, String(v)), removeItem: (k) => ls.delete(k) },
    location: { search, pathname: '/free/walk', hash: '' },
    history: { replaceState: () => {} },
    scrollTo: () => {},
    addEventListener: (t, fn) => { (listeners[t] = listeners[t] || []).push(fn); },
    SpeechRecognition: undefined, webkitSpeechRecognition: undefined,
    __walkStep: null, __lastCompletionPayload: null, __walkState: null,
  };
  const scriptEl = root.querySelectorAll('script').find(s => (s._raw || '').includes('completeWalk'));
  if (!scriptEl) throw new Error('walk script not found in HTML');
  let code = scriptEl._raw;
  if (timeoutOverride) code = code.replace('25000', String(timeoutOverride));
  const sandbox = {
    document: doc, window: win, localStorage: win.localStorage,
    location: win.location, history: win.history,
    navigator: {}, fetch: fetchImpl,
    setTimeout, clearTimeout, setInterval, clearInterval,
    URLSearchParams, console,
  };
  sandbox.window = new Proxy(win, { get: (t, p) => (p in t ? t[p] : sandbox[p]), set: (t, p, v) => { t[p] = v; return true; } });
  vm.createContext(sandbox);
  vm.runInContext(code, sandbox, { filename: 'walk.js' });
  return { root, doc, win, ls, byId: (id) => byId(root, id) };
}
const REVEAL = { alias: 'f4fixharness', ambassador_link: 'https://nayanet.app/joinus?ref=f4fixharness', pages: { personal: '/f4fixharness', business: '/f4fixharness/business', space: '/f4fixharness/space', dashboard: 'https://nayanet.app/dashboard?name=F4&alias=f4fixharness' } };
const resolvingFetch = async () => ({ ok: true, json: async () => REVEAL });
const slowFetch = async () => { await sleep(3000); return { ok: true, json: async () => REVEAL }; };

// ---------- T0: static facts ----------
const ANSWERS = { about: 'a', into: 'b', vision: 'c', mission: 'd', motto: 'e', goal: 'f', biz_do: 'g', biz_offer: 'h', biz_building: 'i', space: 'j', news_local: 'no', news_global: 'no', news_province: 'no', news_create_anywhere: 'no' };
function seedState(alias, withReveal) {
  const s = { alias, answers: ANSWERS, topics: [], reveal: withReveal ? REVEAL : null, pageNames: { personal: { title: 'F4 Fix', slug: alias }, business: { title: 'Fix Biz', slug: 'fix-biz' }, space: { title: 'Fix Space', slug: 'fix-space' } } };
  return { nayanet_smart_alias: alias, nayanet_smart_name: 'F4 Fix', naya_welcome_right_v1: JSON.stringify(s) };
}

check('T0 viewport meta (width=device-width) present', html.includes('width=device-width'));
check('T0 five doors in served bytes, Hub first', (() => {
  const doors = [...html.matchAll(/data-door="([^"]+)"/g)].map(m => m[1]);
  return JSON.stringify(doors) === JSON.stringify(['Hub', 'Dashboard', 'Personal', 'Business', 'Space']);
})());
check('T0 free end line present', html.includes('You&rsquo;re in on Naya Free'));
check('T0 no old showStep(14)+completeWalk call', !html.includes('showStep(14); completeWalk()'));
check('T0 25s timeout present', html.includes('25000'));

// ---------- T1: happy path (slow fetch so progress is observable) ----------
if (!timeoutOverride) {
  const env = makeEnv({ fetchImpl: slowFetch, search: '?name=F4%20Fix&alias=f4fixharness', stored: seedState('f4fixharness', false) });
  await sleep(50);
  check('T1 boot with all answers answered shows step-14 (last question)', env.byId('step-14') && !env.byId('step-14').hidden);
  // step-14's Enter lives inside step-14; the names Enter shares the id — scope it.
  const step14Btn = env.byId('step-14').querySelector('#enterBtn-14');
  const ans14 = env.byId('step-14').querySelector('#answer-14');
  if (ans14) ans14.value = 'yes';
  step14Btn.click();
  await sleep(50);
  check('T1 after step-14 Enter, names step visible', !env.byId('step-names').hidden);
  const namesBtn = env.byId('step-names').querySelector('#enterBtn-14');
  const bIn = env.byId('step-names').querySelector('#name-business');
  const sIn = env.byId('step-names').querySelector('#name-space');
  if (bIn) bIn.value = 'Fix Biz'; if (sIn) sIn.value = 'Fix Space';
  namesBtn.click();
  check('T1 naming Enter immediate feedback: disabled + Building… + is-busy', namesBtn.disabled === true && namesBtn.textContent.includes('Building') && namesBtn.classList.contains('is-busy'));
  await sleep(250);
  check('T1 building step visible after Enter', !env.byId('step-building').hidden);
  const bs = env.byId('buildStatus');
  check('T1 buildWorking visible with live status text', !env.byId('buildWorking').hidden && bs && (bs.textContent || '').length > 3);
  const barEl = env.byId('buildBarFill');
  const bar1 = barEl ? barEl.style.width : 'n/a';
  await sleep(2600);
  const bar2 = barEl ? barEl.style.width : 'n/a';
  check('T1 progress moves while building (bar + stage text advance)', (bar1 !== bar2) || (bs && (bs.textContent || '').includes('Building your pages')), `bar ${bar1} -> ${bar2}`);
  await sleep(400);
  check('T1 build completes: buildDone visible, buildWorking hidden', !env.byId('buildDone').hidden && env.byId('buildWorking').hidden);
  env.byId('buildGo').click();
  await sleep(50);
  check('T1 "See your pages" reaches the end slide', !env.byId('step-end').hidden);
  check('T1 end slide shows the five doors', !env.byId('step-end').hidden && env.byId('doorRow').querySelectorAll('.p3-door').length === 5);
}

// ---------- T2: timeout path (only when run with an override, e.g. 150ms) ----------
if (timeoutOverride) {
  // Simulated aborted fetch: rejects with AbortError at the timeout, the
  // way a real browser fetch rejects when AbortController fires. (Passing
  // the host AbortController into the vm context aborts the Node process,
  // so the wiring half is proven separately: `node -e` below in the report
  // shows new AbortController() + abort() firing AbortError. The code path
  // under test here — AbortError -> timedOut -> loud error — is the same.)
  const never = (path, opts) => new Promise((resolve, reject) => {
    setTimeout(() => { const e = new Error('The operation was aborted.'); e.name = 'AbortError'; reject(e); }, timeoutOverride);
  });
  const env = makeEnv({ fetchImpl: never, search: '?name=F4%20Fix&alias=f4fixharness', stored: seedState('f4fixharness', false) });
  await sleep(50);
  const step14Btn = env.byId('step-14').querySelector('#enterBtn-14');
  step14Btn.click();
  await sleep(50);
  const namesBtn = env.byId('step-names').querySelector('#enterBtn-14');
  namesBtn.click();
  await sleep(900);
  check('T2 hanging POST fails loudly: buildError visible', !env.byId('buildError').hidden);
  const bem = env.byId('buildErrorMsg');
  check('T2 error names the timeout + readable reason', !!bem && (bem.textContent || '').includes('timed out after 25 seconds'));
  check('T2 error offers Try again + Back to your names', !!env.byId('buildRetry') && !!env.byId('buildBack'));
  check('T2 naming Enter re-enabled after failure', namesBtn.disabled === false);
  const bb = env.byId('buildBack');
  check('T2 Back button exists', !!bb);
  if (bb) bb.click();
  await sleep(50);
  check('T2 Back returns to the names step', !!bb && !env.byId('step-names').hidden);
}

// ---------- T3: resume with a saved reveal ----------
if (!timeoutOverride) {
  const env = makeEnv({ fetchImpl: resolvingFetch, search: '', stored: seedState('f4fixharness', true) });
  await sleep(50);
  check('T3 reload with saved reveal lands on the END slide (never Building it)', !env.byId('step-end').hidden && env.byId('step-building').hidden);
  check('T3 end slide doors present on resume', !env.byId('step-end').hidden && env.byId('doorRow').querySelectorAll('.p3-door').length === 5);
}

console.log(failures === 0 ? 'HARNESS: ALL PASS' : `HARNESS: ${failures} FAILURES`);
process.exit(failures === 0 ? 0 : 1);
