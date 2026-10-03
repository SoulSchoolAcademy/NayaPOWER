#!/usr/bin/env node
/* SPACES SMOKE — stub-DOM suite for the Smart Spaces room.
 * No dependency: a minimal DOM/localStorage stub exercises the room's
 * real behaviors (parseSpaces -> smartSpaces -> grid/detail/post/persist)
 * plus the drilled CSS markers in spaces.css.
 *
 *   node HUB/app/preview/tests/spaces-smoke.js   # from the repo root
 */
'use strict';

const fs = require('fs');
const path = require('path');
const REPO = path.resolve(__dirname, '../../../..');

/* ---------------- minimal DOM stub ---------------- */
class StubEl {
  constructor(tag) {
    this.tagName = String(tag).toUpperCase();
    this.children = [];
    this.parentNode = null;
    this.className = '';
    this.textContent = '';
    this.value = '';
    this.disabled = false;
    this.rows = 0;
    this.placeholder = '';
    this.title = '';
    this.type = '';
    this.attrs = {};
    this._props = {};
    this.listeners = {};
    this.style = {
      setProperty: (k, v) => { this._props[k] = String(v); },
      getPropertyValue: (k) => this._props[k] || ''
    };
  }
  setAttribute(k, v) { this.attrs[k] = String(v); }
  getAttribute(k) { return this.attrs[k]; }
  appendChild(c) { c.parentNode = this; this.children.push(c); return c; }
  remove() { if (this.parentNode) this.parentNode.children = this.parentNode.children.filter(x => x !== this); }
  addEventListener(t, fn) { (this.listeners[t] = this.listeners[t] || []).push(fn); }
  dispatch(t, ev) { (this.listeners[t] || []).forEach(fn => fn(Object.assign({ target: this, key: '', preventDefault() {} }, ev || {}))); }
  set innerHTML(v) { if (v === '') this.children = []; else throw new Error('innerHTML set only supports ""'); }
  get innerHTML() { return ''; }
  _clsList() { return this.className.split(/\s+/).filter(Boolean); }
  _matches(sel) {
    if (sel[0] === '.') {
      const need = sel.slice(1).split('.').filter(Boolean);
      const have = this._clsList();
      return need.every(c => have.includes(c));
    }
    return false;
  }
  querySelector(sel) {
    for (const c of this.children) { if (c._matches(sel)) return c; const d = c.querySelector(sel); if (d) return d; }
    return null;
  }
  querySelectorAll(sel, acc) {
    acc = acc || [];
    for (const c of this.children) { if (c._matches(sel)) acc.push(c); c.querySelectorAll(sel, acc); }
    return acc;
  }
}

const store = {};
const localStorageStub = {
  getItem: k => (k in store ? store[k] : null),
  setItem: (k, v) => { store[k] = String(v); },
  removeItem: k => { delete store[k]; }
};

function makeEnv() {
  for (const k of Object.keys(store)) delete store[k];
  const body = new StubEl('body');
  const document = {
    createElement: t => new StubEl(t),
    body
  };
  const window = {};
  const g = { document, window, localStorage: localStorageStub };
  g.el = function (tag, cls, text) {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text !== undefined && text !== null) e.textContent = text;
    return e;
  };
  return g;
}

function loadScripts(env) {
  for (const f of ['HUB/app/js/rooms/spaces-adapter.js', 'HUB/app/js/rooms/spaces.js']) {
    const src = fs.readFileSync(path.join(REPO, f), 'utf8');
    const a = src.indexOf('(function(){');
    const b = src.lastIndexOf('})();');
    if (a === -1 || b === -1) throw new Error('IIFE wrapper missing in ' + f);
    const fn = new Function('window', 'document', 'localStorage', 'el',
      src.slice(a + '(function(){'.length, b));
    fn(env.window, env.document, env.localStorage, env.el);
  }
  return env;
}

/* ---------------- fixtures ---------------- */
const CONTACTS = [
  { id: 'shawn', name: 'Shawn Vibert', role: 'Human Director', color: '#facc15' },
  { id: 'naya1', name: 'Naya 1', role: 'Senior seat', color: '#a855f7' },
  { id: 'naya2', name: 'Naya 2', role: 'Review lane', color: '#38bdf8' }
];
const RAW = [
  { id: 'team-naya', name: 'Team Naya', color: '#a855f7', desc: 'd1',
    members: ['shawn', 'naya1', 'ghost'], demo: true,
    activity: [
      { ts: '2026-10-02T02:00:00Z', text: 'older', demo: true },
      { ts: '2026-10-02T10:00:00Z', text: 'newer', demo: true }
    ] },
  { id: 'solo', name: 'Solo', desc: 'd2', members: [], demo: false, activity: [] },
  null,
  { id: 'broken' }
];

/* ---------------- assertions ---------------- */
let pass = 0, fail = 0;
const failures = [];
function t(name, fn) {
  try { fn(); pass++; }
  catch (e) { fail++; failures.push(name + ' :: ' + e.message); }
}
function eq(a, b, msg) { if (a !== b) throw new Error((msg || 'mismatch') + ': ' + JSON.stringify(a) + ' !== ' + JSON.stringify(b)); }
function ok(v, msg) { if (!v) throw new Error(msg || 'expected truthy'); }

/* ---------------- adapter ---------------- */
t('adapter: resolves member ids to contacts', () => {
  const env = loadScripts(makeEnv());
  const s = env.window.SpacesAdapter.parseSpaces(RAW, CONTACTS);
  const m = s[0].members[0];
  eq(m.name, 'Shawn Vibert'); eq(m.role, 'Human Director'); eq(m.color, '#facc15');
});
t('adapter: unresolvable member kept, never dropped', () => {
  const env = loadScripts(makeEnv());
  const s = env.window.SpacesAdapter.parseSpaces(RAW, CONTACTS);
  const g = s[0].members.find(m => m.id === 'ghost');
  ok(g, 'ghost kept'); eq(g.name, 'ghost'); eq(g.color, '#888888');
});
t('adapter: skips unparseable records', () => {
  const env = loadScripts(makeEnv());
  const s = env.window.SpacesAdapter.parseSpaces(RAW, CONTACTS);
  eq(s.length, 2);
});
t('adapter: activity sorted newest-first', () => {
  const env = loadScripts(makeEnv());
  const s = env.window.SpacesAdapter.parseSpaces(RAW, CONTACTS);
  eq(s[0].activity[0].text, 'newer');
});
t('adapter: color falls back to violet chrome', () => {
  const env = loadScripts(makeEnv());
  const s = env.window.SpacesAdapter.parseSpaces(RAW, CONTACTS);
  eq(s[1].color, '#8b5cf6');
});

/* ---------------- room: grid ---------------- */
function mountSpaces(spaces, ctxExtra) {
  const env = loadScripts(makeEnv());
  const stage = env.window.NayaRooms.smartSpaces(env.el, Object.assign({ spaces }, ctxExtra));
  env.document.body.appendChild(stage);
  return { env, stage };
}
t('grid: renders one card per space', () => {
  const env = loadScripts(makeEnv());
  const spaces = env.window.SpacesAdapter.parseSpaces(RAW, CONTACTS);
  const { stage } = mountSpaces(spaces);
  eq(stage.querySelectorAll('.sp-card').length, 2);
});
t('grid: each card carries its OWN identity color in --sc', () => {
  const env = loadScripts(makeEnv());
  const spaces = env.window.SpacesAdapter.parseSpaces(RAW, CONTACTS);
  const { stage } = mountSpaces(spaces);
  const cards = stage.querySelectorAll('.sp-card');
  eq(cards[0].style.getPropertyValue('--sc'), '#a855f7');
  eq(cards[1].style.getPropertyValue('--sc'), '#8b5cf6'); // fallback, not list position
});
t('grid: cards are keyboard-operable with aria labels', () => {
  const env = loadScripts(makeEnv());
  const spaces = env.window.SpacesAdapter.parseSpaces(RAW, CONTACTS);
  const { stage } = mountSpaces(spaces);
  const card = stage.querySelectorAll('.sp-card')[0];
  eq(card.getAttribute('role'), 'button');
  eq(card.getAttribute('tabindex'), '0');
  ok(card.getAttribute('aria-label').includes('Team Naya'));
});
t('grid: DEMO chip on demo spaces only', () => {
  const env = loadScripts(makeEnv());
  const spaces = env.window.SpacesAdapter.parseSpaces(RAW, CONTACTS);
  const { stage } = mountSpaces(spaces);
  const cards = stage.querySelectorAll('.sp-card');
  ok(cards[0].querySelector('.sp-demo-chip'), 'demo chip on demo card');
  ok(!cards[1].querySelector('.sp-demo-chip'), 'no chip on non-demo card');
});
t('grid: member dots set --mc ball color (not flat inline bg)', () => {
  const env = loadScripts(makeEnv());
  const spaces = env.window.SpacesAdapter.parseSpaces(RAW, CONTACTS);
  const { stage } = mountSpaces(spaces);
  const dot = stage.querySelector('.sp-mdot');
  eq(dot.style.getPropertyValue('--mc'), '#facc15');
});
t('grid: empty spaces -> honest empty state', () => {
  const { stage } = mountSpaces([]);
  const empty = stage.querySelector('.sp-empty');
  ok(empty && empty.textContent.includes('No spaces yet'));
});

/* ---------------- room: detail + post ---------------- */
function openFirst(spaces, ctxExtra) {
  const { env, stage } = mountSpaces(spaces, ctxExtra);
  stage.querySelectorAll('.sp-card')[0].dispatch('click');
  return { env, stage };
}
t('detail: click opens hero with space name + member count', () => {
  const env = loadScripts(makeEnv());
  const spaces = env.window.SpacesAdapter.parseSpaces(RAW, CONTACTS);
  const { stage } = openFirst(spaces);
  const d = stage.querySelector('.sp-detail');
  ok(d, 'detail rendered');
  eq(d.style.getPropertyValue('--sc'), '#a855f7');
  ok(stage.querySelector('.sp-dname').textContent === 'Team Naya');
  ok(stage.querySelector('.sp-sec').textContent.includes('3'));
  eq(stage.querySelectorAll('.sp-avatar').length, 3);
});
t('detail: avatars set --av for the ball gradient', () => {
  const env = loadScripts(makeEnv());
  const spaces = env.window.SpacesAdapter.parseSpaces(RAW, CONTACTS);
  const { stage } = openFirst(spaces);
  const av = stage.querySelectorAll('.sp-avatar')[0];
  eq(av.style.getPropertyValue('--av'), '#facc15');
  eq(av.textContent, 'SV');
});
t('detail: Enter opens card, Escape returns to grid', () => {
  const env = loadScripts(makeEnv());
  const spaces = env.window.SpacesAdapter.parseSpaces(RAW, CONTACTS);
  const { stage } = mountSpaces(spaces);
  const card = stage.querySelectorAll('.sp-card')[0];
  card.dispatch('keydown', { key: 'Enter' });
  ok(stage.querySelector('.sp-detail'), 'detail after Enter');
  stage.dispatch('keydown', { key: 'Escape' });
  ok(stage.querySelector('.sp-grid'), 'grid after Escape');
  ok(!stage.querySelector('.sp-detail'), 'detail gone after Escape');
});
t('detail: back button returns to grid', () => {
  const env = loadScripts(makeEnv());
  const spaces = env.window.SpacesAdapter.parseSpaces(RAW, CONTACTS);
  const { stage } = openFirst(spaces);
  stage.querySelector('.sp-back').dispatch('click');
  ok(stage.querySelector('.sp-grid'), 'grid after back');
});
t('compose: send disabled until text is typed', () => {
  const env = loadScripts(makeEnv());
  const spaces = env.window.SpacesAdapter.parseSpaces(RAW, CONTACTS);
  const { stage } = openFirst(spaces);
  const ta = stage.querySelector('.sp-ta');
  const send = stage.querySelector('.sp-send');
  ok(send.disabled, 'disabled when empty');
  ta.value = 'hello space';
  ta.dispatch('input');
  ok(!send.disabled, 'enabled after input');
  ta.value = '   ';
  ta.dispatch('input');
  ok(send.disabled, 'disabled again on whitespace');
});
t('compose: send posts to feed, persists, dedupes SENT note', () => {
  const env = loadScripts(makeEnv());
  const spaces = env.window.SpacesAdapter.parseSpaces(RAW, CONTACTS);
  const { stage } = openFirst(spaces);
  const ta = stage.querySelector('.sp-ta');
  const send = stage.querySelector('.sp-send');
  ta.value = 'ship it'; ta.dispatch('input'); send.dispatch('click');
  const mine = stage.querySelector('.sp-arow.mine');
  ok(mine, 'mine row painted');
  ok(mine.querySelector('.sp-atext').textContent === 'ship it');
  ok(mine.querySelector('.sp-atime').textContent.includes('You'), 'author labeled You');
  const raw = JSON.parse(localStorageStub.getItem('naya.smartspaces.posts'));
  ok(raw['team-naya'] && raw['team-naya'].length === 1, 'persisted to localStorage');
  ta.value = 'again'; ta.dispatch('input'); send.dispatch('click');
  eq(stage.querySelectorAll('.sp-sent').length, 1, 'single SENT note after double send');
});
t('compose: posts survive a remount (cold retrieve)', () => {
  const env = loadScripts(makeEnv());
  const spaces = env.window.SpacesAdapter.parseSpaces(RAW, CONTACTS);
  const { stage } = openFirst(spaces);
  stage.querySelector('.sp-ta').value = 'persist me';
  stage.querySelector('.sp-ta').dispatch('input');
  stage.querySelector('.sp-send').dispatch('click');
  /* remount in the SAME browser store (localStorage is not wiped on re-render) */
  const stage2 = env.window.NayaRooms.smartSpaces(env.el, { spaces });
  stage2.querySelectorAll('.sp-card')[0].dispatch('click');
  const mine = stage2.querySelector('.sp-arow.mine');
  ok(mine && mine.querySelector('.sp-atext').textContent === 'persist me', 'post reloaded from store');
});
t('compose: onMail hook fires with (space, text)', () => {
  let got = null;
  const env = loadScripts(makeEnv());
  const spaces = env.window.SpacesAdapter.parseSpaces(RAW, CONTACTS);
  const { stage } = openFirst(spaces, { onMail: (s, text) => { got = [s.id, text]; } });
  const ta = stage.querySelector('.sp-ta');
  ta.value = 'via hook'; ta.dispatch('input');
  stage.querySelector('.sp-send').dispatch('click');
  eq(got[0], 'team-naya'); eq(got[1], 'via hook');
});
t('detail: empty activity -> honest empty state', () => {
  const env = loadScripts(makeEnv());
  const spaces = env.window.SpacesAdapter.parseSpaces(RAW, CONTACTS);
  const { stage } = mountSpaces(spaces);
  stage.querySelectorAll('.sp-card')[1].dispatch('click');
  const empty = stage.querySelector('.sp-feed').querySelector('.sp-empty');
  ok(empty && empty.textContent.includes('Nothing here yet'));
});

/* ---------------- drilled CSS markers ---------------- */
const css = fs.readFileSync(path.join(REPO, 'HUB/app/css/spaces.css'), 'utf8');
t('css: obsidian button law on .sp-back/.sp-send', () => {
  ok(css.includes('linear-gradient(180deg,#1b1b21,#0b0b0e)'), 'obsidian gradient present');
  ok(css.includes('inset 0 1px 0 rgba(255,255,255,.16)'), 'top-light inset present');
});
t('css: avatar balls — radial-gradient on .sp-avatar and .sp-mdot', () => {
  ok(/\.sp-avatar\{[\s\S]*?radial-gradient\(circle at 32% 28%/.test(css), 'avatar ball');
  ok(/\.sp-mdot\{[\s\S]*?radial-gradient\(circle at 32% 28%/.test(css), 'dot ball');
});
t('css: reduced-motion kill switch', () => {
  ok(css.includes('prefers-reduced-motion'), 'media query present');
  ok(css.includes('.sp-stage *{ animation:none !important; transition:none !important; }'), 'kill switch exact');
});
t('css: type floor 16px body text', () => {
  const bodySel = ['.sp-card-desc', '.sp-ddesc', '.sp-atext', '.sp-empty', '.sp-ta', '.sp-member-n'];
  for (const sel of bodySel) {
    const m = css.match(new RegExp(sel.replace(/\./g, '\\.') + '\\{[^}]*?font-size:(\\d+(?:\\.\\d+)?)px'));
    ok(m, sel + ' has font-size');
    if (parseFloat(m[1]) < 16) throw new Error(sel + ' is ' + m[1] + 'px, below 16px floor');
  }
});
t('css: violet #8b5cf6 is room chrome (--sp-violet)', () => {
  ok(css.includes('--sp-violet:#8b5cf6'), 'violet chrome token');
});
t('css: hover ignites identity color on cards', () => {
  ok(/\.sp-card:hover[\s\S]*?border-color:var\(--sc\)/.test(css), 'card hover ignites --sc');
});

/* ---------------- report ---------------- */
console.log('SPACES SMOKE: %d pass, %d fail', pass, fail);
for (const f of failures) console.log('FAIL ' + f);
process.exit(fail ? 1 : 0);
