#!/usr/bin/env node
/* CONNECT SMOKE — stub-DOM suite for the Smart Connect room (Smart Doors).
 *
 * Pure Node, no jsdom: a minimal DOM stub drives the real room JS and the
 * real adapter JS. Covers the room's real behaviors, with door-honesty
 * assertions as hard gates: only genuinely live statuses may render LIVE,
 * every button has a real consequence, and statuses the adapter cannot
 * verify must fail CLOSED (design/unknown) — never a faked green light.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const REPO_DIR = '/home/hatch/workspace/nayapower-room02';

/* ---------- minimal DOM stub ---------- */
function StubEl(tag) {
  this.tagName = String(tag).toUpperCase();
  this.children = [];
  this.className = '';
  this.textContent = '';
  this.type = '';
  this.parent = null;
  this._attrs = {};
  this._listeners = {};
  this.style = { _props: {}, setProperty: function (k, v) { this._props[k] = v; }, getProperty: function (k) { return this._props[k]; } };
}
StubEl.prototype.appendChild = function (c) { c.parent = this; this.children.push(c); return c; };
StubEl.prototype.setAttribute = function (k, v) { this._attrs[k] = v; };
StubEl.prototype.getAttribute = function (k) { return this._attrs[k]; };
StubEl.prototype.addEventListener = function (t, fn) { (this._listeners[t] = this._listeners[t] || []).push(fn); };
StubEl.prototype.click = function () { (this._listeners.click || []).forEach(function (f) { f.call(this); }, this); };
StubEl.prototype.remove = function () { if (this.parent) { this.parent.children = this.parent.children.filter(c => c !== this); this.parent = null; } };
StubEl.prototype.focus = function () { documentStub.activeElement = this; };
StubEl.prototype.querySelector = function (sel) {
  if (sel[0] !== '.') return null;
  const cls = sel.slice(1);
  const stack = this.children.slice();
  while (stack.length) {
    const n = stack.shift();
    if ((n.className || '').split(/\s+/).indexOf(cls) !== -1) return n;
    stack.push.apply(stack, n.children);
  }
  return null;
};
Object.defineProperty(StubEl.prototype, 'lastChild', { get: function () { return this.children[this.children.length - 1] || null; } });

function byClass(root, cls, out) {
  out = out || [];
  (root.children || []).forEach(function (n) {
    if ((n.className || '').split(/\s+/).indexOf(cls) !== -1) out.push(n);
    byClass(n, cls, out);
  });
  return out;
}

const documentStub = {
  activeElement: null,
  createElement: function (tag) { return new StubEl(tag); }
};
function el(tag, cls, text) {
  const e = documentStub.createElement(tag);
  if (cls) e.className = cls;
  if (text !== undefined && text !== null) e.textContent = text;
  return e;
}

/* ---------- load the REAL adapter + room ---------- */
function inner(src) {
  const a = src.indexOf('(function(){');
  const b = src.lastIndexOf('})();');
  if (a === -1 || b === -1) throw new Error('IIFE wrapper missing');
  return src.slice(a + '(function(){'.length, b);
}
const adSrc = fs.readFileSync(path.join(REPO_DIR, 'HUB/app/js/rooms/connect-adapter.js'), 'utf8');
const roomSrc = fs.readFileSync(path.join(REPO_DIR, 'HUB/app/js/rooms/connect.js'), 'utf8');
const css = fs.readFileSync(path.join(REPO_DIR, 'HUB/app/css/connect.css'), 'utf8');
const registry = JSON.parse(fs.readFileSync(path.join(REPO_DIR, 'BRAIN/10-INTERFACES/0002-SMART-DOOR-REGISTRY-V1.json'), 'utf8'));

const windowStub = {};
const sandbox = { window: windowStub, document: documentStub, el: el, console: console };
vm.createContext(sandbox);
vm.runInContext(inner(adSrc), sandbox);
vm.runInContext(inner(roomSrc), sandbox);
const ConnectAdapter = windowStub.ConnectAdapter;
const connect = windowStub.NayaRooms.connect;

/* ---------- tiny runner ---------- */
let pass = 0, fail = 0;
const failures = [];
function check(name, cond, detail) {
  if (cond) { pass++; }
  else { fail++; failures.push(name + (detail ? ' — ' + detail : '')); }
}

function regDoor(door_id, status, caps) {
  return { door_id: door_id, name: door_id + ' name', provider: 'p', capabilities: caps || ['read'], operations: [], consequence_class: 'c', required_authority: 'a', identity_method: 'i', data_classes: [], health: 'h', status: status, audit: '' };
}
function p(list) { return ConnectAdapter.parse({ doors: list }); }

/* ---------- adapter: door honesty (hard gates) ---------- */
check('adapter: LIVE_BOUNDED parses as live/LIVE', (function () {
  const d = p([regDoor('D1', 'LIVE_BOUNDED')])[0];
  return d.statusKind === 'live' && d.statusLabel === 'LIVE';
})());
check('adapter: LIVE_BOUNDED_EXISTING_CAPABILITY parses as live/LIVE', (function () {
  const d = p([regDoor('D1', 'LIVE_BOUNDED_EXISTING_CAPABILITY')])[0];
  return d.statusKind === 'live' && d.statusLabel === 'LIVE';
})());
check('adapter: REGISTERED_CONTRACT_ONLY is design/IN DESIGN, never LIVE', (function () {
  const d = p([regDoor('D1', 'REGISTERED_CONTRACT_ONLY')])[0];
  return d.statusKind === 'design' && d.statusLabel === 'IN DESIGN';
})());
check('adapter: UNKNOWN status fails CLOSED (design), never faked LIVE', (function () {
  const d = p([regDoor('D1', 'LIVE_SOMETHING_NEW')])[0];
  return d.statusKind === 'design' && d.statusLabel !== 'LIVE';
})());
check('adapter: missing status fails CLOSED (design)', (function () {
  const raw = regDoor('D1', undefined); delete raw.status;
  const d = p([raw])[0];
  return d.statusKind === 'design';
})());
check('adapter: accepts a JSON string input', (function () {
  return ConnectAdapter.parse(JSON.stringify({ doors: [regDoor('D1', 'LIVE_BOUNDED')] }))[0].statusKind === 'live';
})());
check('adapter: preserves registry order (no re-sorting)', (function () {
  const ds = p([regDoor('Z', 'LIVE_BOUNDED'), regDoor('A', 'REGISTERED_CONTRACT_ONLY')]);
  return ds[0].id === 'Z' && ds[1].id === 'A';
})());

/* ---------- canonical registry grounding ---------- */
const doors = ConnectAdapter.parse(registry);
check('canonical: 9 doors parsed', doors.length === 9, 'got ' + doors.length);
const liveDoors = doors.filter(d => d.statusKind === 'live');
check('canonical: exactly 2 live doors', liveDoors.length === 2, 'got ' + liveDoors.length);
check('canonical: live ids are DOOR-AI + DOOR-DATA', (function () {
  const ids = liveDoors.map(d => d.id).sort().join(',');
  return ids === 'DOOR-AI,DOOR-DATA';
})());
check('canonical: no door invents a status label (only LIVE / IN DESIGN)', doors.every(d => d.statusLabel === 'LIVE' || d.statusLabel === 'IN DESIGN'));

/* ---------- room render ---------- */
const stage = connect(el, { doors: doors });
check('room: stage has connect-stage class', stage.className === 'connect-stage');
const boards = byClass(stage, 'cn-door');
check('room: 9 door boards rendered', boards.length === 9, 'got ' + boards.length);
check('room: boards follow registry order (display names match adapter order)', (function () {
  const names = byClass(stage, 'cn-name').map(n => n.textContent);
  const expected = doors.map(d => d.id === 'DOOR-AI' ? 'A2A Connect' : d.name);
  return JSON.stringify(names) === JSON.stringify(expected);
})());
check('room: header kicker reads SMART CONNECT', (function () {
  const k = byClass(stage, 'cn-kicker')[0];
  return k && k.textContent === 'SMART CONNECT';
})());
check('room: strip shows 2 LIVE + 7 IN DESIGN', (function () {
  const counts = byClass(stage, 'cn-count').map(c => c.textContent);
  return counts.join('|') === '2 LIVE|7 IN DESIGN';
})(), byClass(stage, 'cn-count').map(c => c.textContent).join('|'));
check('room: strip carries the no-fake-buttons note', (function () {
  const n = byClass(stage, 'cn-strip-note')[0];
  return n && /no fake buttons/i.test(n.textContent);
})());
check('room: live boards get .live, design boards .design', (function () {
  const liveBoards = boards.filter(b => b.className.split(/\s+/).indexOf('live') !== -1);
  const designBoards = boards.filter(b => b.className.split(/\s+/).indexOf('design') !== -1);
  return liveBoards.length === 2 && designBoards.length === 7;
})());
check('room: pill labels match honesty (2 LIVE / 7 IN DESIGN)', (function () {
  const pills = byClass(stage, 'cn-pill').map(p => p.textContent);
  return pills.filter(t => t === 'LIVE').length === 2 && pills.filter(t => t === 'IN DESIGN').length === 7;
})());
check('room: live button says MANAGE CONNECTION', (function () {
  const btns = byClass(stage, 'cn-connect');
  const liveBtns = btns.filter(b => b.className.split(/\s+/).indexOf('live') !== -1);
  return liveBtns.length === 2 && liveBtns.every(b => b.textContent === 'MANAGE CONNECTION');
})());
check('room: design buttons say CONNECT', (function () {
  const btns = byClass(stage, 'cn-connect');
  const designBtns = btns.filter(b => b.className.split(/\s+/).indexOf('live') === -1);
  return designBtns.length === 7 && designBtns.every(b => b.textContent === 'CONNECT');
})());
check('room: every button is type=button with an aria-label naming the door', (function () {
  const btns = byClass(stage, 'cn-connect');
  return btns.length === 9 && btns.every(b => b.type === 'button' && /connect/i.test(b.getAttribute('aria-label') || ''));
})());
check('room: A2A presentation name applied (DOOR-AI presents as A2A Connect)', (function () {
  const names = byClass(stage, 'cn-name').map(n => n.textContent);
  return names.indexOf('A2A Connect') !== -1 && names.indexOf('AI Connect') === -1;
})());
check('room: each board has a jewel glyph', (function () {
  return boards.length === 9 && boards.every(b => byClass(b, 'cn-gem-glyph').length === 1);
})());
check('room: footer states the connection≠authority law', (function () {
  const f = byClass(stage, 'cn-foot')[0];
  return f && /does not create authority/i.test(f.textContent);
})());
check('room: door color is stable identity (keyed by id, not list position)', (function () {
  // render reversed: colors must follow the door id, not the index
  const rev = doors.slice().reverse();
  const s2 = connect(el, { doors: rev });
  const b2 = byClass(s2, 'cn-door');
  const colorOf = b => b.style._props['--door'];
  // GitHub door is purple; find it in both renders
  const firstGithub = boards.filter(b => colorOf(b) === '#a371f7').length;
  const revGithub = b2.filter(b => colorOf(b) === '#a371f7').length;
  return firstGithub === 1 && revGithub === 1 && b2[0] !== boards[0] && colorOf(b2[b2.length - 1]) === '#a371f7';
})());
check('room: design boards whisper at rest (no forced glow)', (function () {
  return css.indexOf('.connect-stage .cn-door.design::before{ box-shadow:none; }') !== -1;
})());

/* ---------- button consequences ---------- */
check('behavior: onConnect handler called with the door id, no notice', (function () {
  const captured = {};
  const s = connect(el, { doors: doors, onConnect: function (id) { captured.id = id; } });
  const btn = byClass(s, 'cn-connect')[0];
  btn.click();
  return captured.id === doors[0].id && byClass(s, 'cn-notice').length === 0;
})());
check('behavior: design CONNECT without handler shows honest notice, not a connection', (function () {
  const s = connect(el, { doors: doors });
  const designBtn = byClass(s, 'cn-connect').filter(b => b.className.split(/\s+/).indexOf('live') === -1)[0];
  designBtn.click();
  const n = byClass(s, 'cn-notice');
  const t = byClass(s, 'cn-notice-text')[0];
  return n.length === 1 && t && /not yet wired|still being built/i.test(t.textContent) && /nothing was changed/i.test(t.textContent);
})());
check('behavior: notice has role=status + aria-live=polite', (function () {
  const s = connect(el, { doors: doors });
  const designBtn = byClass(s, 'cn-connect').filter(b => b.className.split(/\s+/).indexOf('live') === -1)[0];
  designBtn.click();
  const n = byClass(s, 'cn-notice')[0];
  return n.getAttribute('role') === 'status' && n.getAttribute('aria-live') === 'polite';
})());
check('behavior: live MANAGE without handler shows Connection manager notice', (function () {
  const s = connect(el, { doors: doors });
  const liveBtn = byClass(s, 'cn-connect').filter(b => b.className.split(/\s+/).indexOf('live') !== -1)[0];
  liveBtn.click();
  const title = byClass(s, 'cn-notice-title')[0];
  const text = byClass(s, 'cn-notice-text')[0];
  return title && title.textContent === 'Connection manager' && text && /nothing was changed/.test(text.textContent);
})());
check('behavior: GOT IT dismisses the notice and returns focus to the button', (function () {
  const s = connect(el, { doors: doors });
  const designBtn = byClass(s, 'cn-connect').filter(b => b.className.split(/\s+/).indexOf('live') === -1)[0];
  designBtn.click();
  const close = byClass(s, 'cn-notice-close')[0];
  close.click();
  return byClass(s, 'cn-notice').length === 0 && documentStub.activeElement === designBtn;
})());
check('behavior: clicking twice replaces the notice (no stacking)', (function () {
  const s = connect(el, { doors: doors });
  const designBtn = byClass(s, 'cn-connect').filter(b => b.className.split(/\s+/).indexOf('live') === -1)[0];
  designBtn.click(); designBtn.click();
  return byClass(s, 'cn-notice').length === 1;
})());

/* ---------- CSS markers (drilled law) ---------- */
check('css: obsidian button gradient present', css.indexOf('linear-gradient(180deg,#1b1b21,#0b0b0e)') !== -1);
check('css: inset top-light on buttons', css.indexOf('inset 0 1px 0 rgba(255,255,255,.16)') !== -1);
check('css: reduced-motion guard scoped to .connect-stage', (function () {
  return /@media\s*\(\s*prefers-reduced-motion:\s*reduce\s*\)\s*\{\s*\.connect-stage\s*\*\s*\{\s*animation:\s*none\s*!important;\s*transition:\s*none\s*!important;/.test(css);
})());
check('css: pill labels at 11px floor', (function () {
  const m = css.match(/\.connect-stage \.cn-pill\{[^}]*font-size:(\d+)px/);
  return m && parseInt(m[1], 10) >= 11;
})());
check('css: body text (cn-plain) at 16px floor', (function () {
  const m = css.match(/\.connect-stage \.cn-plain\{[^}]*font-size:([\d.]+)px/);
  return m && parseFloat(m[1]) >= 16;
})());
check('css: brace balance', (function () {
  const o = (css.match(/\{/g) || []).length, c = (css.match(/\}/g) || []).length;
  return o === c && o > 0;
})());

console.log('\nCONNECT SMOKE: ' + pass + ' passed, ' + fail + ' failed');
if (failures.length) { failures.forEach(f => console.log('  FAIL: ' + f)); process.exit(1); }
console.log('ALL GREEN');
