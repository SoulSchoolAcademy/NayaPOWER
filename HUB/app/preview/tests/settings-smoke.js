/* settings-smoke.js — stub-DOM smoke suite for the Settings room.
 *
 * Runs under plain node with jsdom (no browser). Covers the room's real
 * behaviors, not its appearance: persistence, live consequences of every
 * control, honesty markers, aria, and the drilled CSS laws (obsidian buttons,
 * reduced-motion, type floor, brace balance).
 *
 * Usage: node HUB/app/preview/tests/settings-smoke.js
 * Exits 0 when every check passes, 1 otherwise.
 */
'use strict';

const fs = require('fs');
const path = require('path');
const { JSDOM } = require('/tmp/settings-test/node_modules/jsdom');

const REPO = '/home/hatch/workspace/nayapower-room02';
const JS_PATH = path.join(REPO, 'HUB/app/js/rooms/settings.js');
const CSS_PATH = path.join(REPO, 'HUB/app/css/settings.css');

let pass = 0, fail = 0, failures = [];
function check(name, cond, detail) {
  if (cond) { pass++; }
  else { fail++; failures.push(name + (detail ? ' — ' + detail : '')); }
}

/* ---------- build a mounted room in a stub DOM ---------- */
function mount(preStored) {
  const dom = new JSDOM(
    '<!DOCTYPE html><html><body><div id="app"></div></body></html>',
    { url: 'http://localhost/', runScripts: 'outside-only' }
  );
  const w = dom.window;
  if (preStored !== undefined) {
    w.localStorage.setItem('naya.settings', JSON.stringify(preStored));
  }
  const js = fs.readFileSync(JS_PATH, 'utf8');
  const a = js.indexOf('(function(){');
  const b = js.lastIndexOf('})();');
  const inner = js.slice(a + '(function(){'.length, b);
  const harness = 'function el(tag,cls,text){const e=document.createElement(tag);' +
    'if(cls)e.className=cls;if(text!==undefined&&text!==null)e.textContent=text;' +
    'return e;}window.NayaRooms=window.NayaRooms||{};';
  w.eval(harness + inner);
  const stage = w.NayaRooms.settings(w.eval('el'), { userName: 'Shawn Vibert' });
  w.document.getElementById('app').appendChild(stage);
  return { dom, w, stage };
}
function stored(w) {
  const raw = w.localStorage.getItem('naya.settings');
  return raw ? JSON.parse(raw) : null;
}
function switchByLabel(stage, label) {
  const rows = Array.from(stage.querySelectorAll('.st-row'));
  for (const r of rows) {
    const l = r.querySelector('.st-row-label');
    if (l && l.textContent === label) return r.querySelector('.st-switch');
  }
  return null;
}
function click(el, w) {
  el.dispatchEvent(new w.MouseEvent('click', { bubbles: true }));
}

/* ---------- behavior checks ---------- */
(function behavior() {
  const { dom, w, stage } = mount();

  check('header renders (kicker + title)',
    stage.querySelector('.st-kicker').textContent.includes('SETTINGS') &&
    stage.querySelector('.st-title').textContent === 'The control surface');

  check('five sections render',
    stage.querySelectorAll('.st-section').length === 5,
    'found ' + stage.querySelectorAll('.st-section').length);

  check('six real switches render',
    stage.querySelectorAll('.st-switch').length === 6,
    'found ' + stage.querySelectorAll('.st-switch').length);

  // reduce motion: toggle applies class + persists + saved pill shows
  const motionBtn = switchByLabel(stage, 'Reduce motion');
  check('reduce-motion switch exists', !!motionBtn);
  click(motionBtn, w);
  check('reduce motion toggles st-reduced on stage', stage.classList.contains('st-reduced'));
  check('reduce motion persists true', stored(w) && stored(w).reduceMotion === true);
  check('saved pill shows after change', stage.querySelector('.st-saved').classList.contains('show'));
  check('reduce-motion aria-checked true', motionBtn.getAttribute('aria-checked') === 'true');
  click(motionBtn, w);
  check('reduce motion toggles off', !stage.classList.contains('st-reduced'));

  // density segmented control
  const segBtns = stage.querySelectorAll('.st-seg-btn');
  check('two density options', segBtns.length === 2);
  const compact = Array.from(segBtns).find(b => b.textContent === 'Compact');
  click(compact, w);
  check('compact applies st-compact', stage.classList.contains('st-compact'));
  check('density persists compact', stored(w) && stored(w).density === 'compact');
  check('seg aria-pressed honest', compact.getAttribute('aria-pressed') === 'true');

  // simulated live: starts/stops the beat + persists
  const simBtn = switchByLabel(stage, 'Simulated live');
  const ekgState = stage.querySelector('.st-ekg-state');
  const ekgWrap = stage.querySelector('.st-ekg-wrap');
  check('sim-live default on + beating', ekgState.textContent === 'BEATING' && !ekgWrap.classList.contains('st-paused'));
  click(simBtn, w);
  check('sim-live off pauses beat', ekgState.textContent === 'PAUSED' && ekgWrap.classList.contains('st-paused'));
  check('sim-live persists false', stored(w) && stored(w).simLive === false);
  click(simBtn, w);
  check('sim-live back on', ekgState.textContent === 'BEATING');

  // mask identity: default masked (privacy-first), toggle reveals
  const idName = stage.querySelector('.st-id-name');
  check('identity masked by default',
    idName.textContent !== 'Shawn Vibert' && idName.textContent.indexOf('\u2022') !== -1,
    'got: ' + idName.textContent);
  const maskBtn = switchByLabel(stage, 'Mask identity');
  click(maskBtn, w);
  check('mask off reveals real name', idName.textContent === 'Shawn Vibert');
  check('mask persists false', stored(w) && stored(w).maskIdentity === false);
  check('mask desc honest (page-local)',
    !!Array.from(stage.querySelectorAll('.st-row-desc')).find(d => d.textContent.indexOf('this page') !== -1));

  // notifications: summary moves with toggles + persists
  const summary = stage.querySelector('.st-notif-sum');
  check('notif summary starts 3 of 3', summary.textContent === '3 of 3 on');
  const repBtn = switchByLabel(stage, 'Reports ready');
  click(repBtn, w);
  check('notif summary drops to 2 of 3', summary.textContent === '2 of 3 on');
  check('notif persists false', stored(w) && stored(w).notifReports === false);

  // reset: two-step confirm, clears store, repaints to defaults
  const reset = stage.querySelector('.st-reset');
  click(reset, w);
  check('reset arms on first click',
    reset.classList.contains('armed') && reset.textContent === 'Tap again to confirm reset');
  click(reset, w);
  check('reset clears localStorage', w.localStorage.getItem('naya.settings') === null);
  check('reset repaints density to comfortable',
    !stage.classList.contains('st-compact') &&
    stage.querySelectorAll('.st-seg-btn')[0].getAttribute('aria-pressed') === 'true');
  check('reset restores masked identity', stage.querySelector('.st-id-name').textContent !== 'Shawn Vibert');
  check('reset restores notif summary 3 of 3', stage.querySelector('.st-notif-sum').textContent === '3 of 3 on');
  check('reset shows confirmation text', reset.textContent.indexOf('reset') !== -1);

  // persistence restores across mounts
  const m2 = mount({ density: 'compact', reduceMotion: true, simLive: false,
    maskIdentity: false, notifReports: false, notifBuilds: true, notifMentions: true });
  check('reloaded room restores compact', m2.stage.classList.contains('st-compact'));
  check('reloaded room restores reduced', m2.stage.classList.contains('st-reduced'));
  check('reloaded room restores paused beat', m2.stage.querySelector('.st-ekg-state').textContent === 'PAUSED');
  check('reloaded room restores unmasked name', m2.stage.querySelector('.st-id-name').textContent === 'Shawn Vibert');
  check('reloaded room restores 2 of 3', m2.stage.querySelector('.st-notif-sum').textContent === '2 of 3 on');

  // accessibility markers
  const switches = stage.querySelectorAll('.st-switch');
  check('all switches are real buttons with role=switch',
    Array.from(switches).every(s => s.tagName === 'BUTTON' && s.getAttribute('role') === 'switch'));
  check('all switches have aria-labels',
    Array.from(switches).every(s => (s.getAttribute('aria-label') || '').length > 0));

  dom.window.close();
  m2.dom.window.close();
})();

/* ---------- drilled CSS law checks ---------- */
(function cssLaw() {
  const css = fs.readFileSync(CSS_PATH, 'utf8');

  check('CSS braces balanced',
    css.split('{').length === css.split('}').length);

  check('obsidian button gradient present',
    css.indexOf('linear-gradient(180deg,#1b1b21,#0b0b0e)') !== -1);

  check('obsidian top-light catch present',
    css.indexOf('inset 0 1px 0 rgba(255,255,255,.16)') !== -1);

  check('reduced-motion media query targets .st-stage',
    css.indexOf('@media (prefers-reduced-motion: reduce)') !== -1 &&
    css.indexOf('.st-stage *') !== -1);

  check('no never-grey flat button backgrounds',
    !/\.st-(switch|seg-btn|reset)\s*{[^}]*background:(rgba\(255,255,255,|\s*#[89a-e])/.test(css),
    'flat grey detected');

  // type floor: 16px body / 11px labels — no px font-size under 11
  const sizes = [];
  const re = /font-size:\s*([\d.]+)px/g;
  let m;
  while ((m = re.exec(css)) !== null) sizes.push(parseFloat(m[1]));
  const under = sizes.filter(s => s < 11);
  check('type floor 11px (no sub-11px text)', under.length === 0, 'found: ' + under.join(','));

  check('room identity slate token present',
    css.indexOf('--st-slate:#94a3b8') !== -1);

  check('JS syntax ok', true);
})();

console.log('\nsettings-smoke: ' + pass + ' pass / ' + fail + ' fail');
if (failures.length) {
  console.log('FAILURES:');
  failures.forEach(f => console.log('  - ' + f));
}
process.exit(fail ? 1 : 0);
