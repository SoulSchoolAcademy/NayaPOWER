#!/usr/bin/env node
/* LEDGER SMOKE — stub-DOM suite for the Smart Ledger room (Room Four).
 *
 * Pure Node, no jsdom: a minimal DOM stub drives the real room JS and the
 * real adapter JS. Covers the room's real behaviors, with ledger-honesty
 * assertions as hard gates: demo content is never labeled live, no entries
 * are ever invented, proof states never inflate, and every button has a
 * real consequence.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const REPO_DIR = '/home/hatch/workspace/nayapower-room02';

/* ---------- minimal DOM stub (extended for ledger: SVG, classList, innerHTML) ---------- */
function StubEl(tag) {
  this.tagName = String(tag).toUpperCase();
  this.children = [];
  this._className = '';
  this.textContent = '';
  this.type = '';
  this.title = '';
  this.parent = null;
  this._attrs = {};
  this._listeners = {};
  this._innerHTML = '';
  const self = this;
  this.classList = {
    add: function (c) { const p = self._className.split(/\s+/).filter(Boolean); if (p.indexOf(c) === -1) p.push(c); self._className = p.join(' '); },
    remove: function (c) { self._className = self._className.split(/\s+/).filter(Boolean).filter(x => x !== c).join(' '); },
    contains: function (c) { return self._className.split(/\s+/).indexOf(c) !== -1; }
  };
  this.style = { _props: {}, setProperty: function (k, v) { this._props[k] = v; }, getProperty: function (k) { return this._props[k]; } };
}
Object.defineProperty(StubEl.prototype, 'className', {
  get: function () { return this._className; },
  set: function (v) { this._className = v || ''; }
});
Object.defineProperty(StubEl.prototype, 'innerHTML', {
  get: function () { return this._innerHTML; },
  set: function (v) { this._innerHTML = String(v); if (v === '') this.children = []; }
});
StubEl.prototype.appendChild = function (c) { c.parent = this; this.children.push(c); return c; };
StubEl.prototype.setAttribute = function (k, v) { this._attrs[k] = v; if (k === 'class') this.className = v; };
StubEl.prototype.getAttribute = function (k) { return this._attrs[k]; };
StubEl.prototype.addEventListener = function (t, fn) { (this._listeners[t] = this._listeners[t] || []).push(fn); };
StubEl.prototype.click = function (ev) { (this._listeners.click || []).forEach(f => f.call(this, ev || { type: 'click', target: this })); };
StubEl.prototype.remove = function () { if (this.parent) { this.parent.children = this.parent.children.filter(c => c !== this); this.parent = null; } };
StubEl.prototype.focus = function () { documentStub.activeElement = this; };
StubEl.prototype._match = function (sel) {
  if (sel[0] !== '.') return false;
  return this.className.split(/\s+/).indexOf(sel.slice(1)) !== -1;
};
StubEl.prototype.querySelector = function (sel) { return this.querySelectorAll(sel)[0] || null; };
StubEl.prototype.querySelectorAll = function (sel) {
  const out = [];
  const stack = this.children.slice();
  while (stack.length) {
    const n = stack.shift();
    if (n._match(sel)) out.push(n);
    stack.push.apply(stack, n.children || []);
  }
  return out;
};
Object.defineProperty(StubEl.prototype, 'lastChild', { get: function () { return this.children[this.children.length - 1] || null; } });

function byClass(root, cls, out) {
  out = out || [];
  (root.children || []).forEach(function (n) {
    if (n.className.split(/\s+/).indexOf(cls) !== -1) out.push(n);
    byClass(n, cls, out);
  });
  return out;
}
function allButtons(root) {
  const out = [];
  (function walk(n) {
    if (n.tagName === 'BUTTON') out.push(n);
    (n.children || []).forEach(walk);
  })(root);
  return out;
}
function subText(n) {
  let t = n.textContent || '';
  (n.children || []).forEach(c => { t += ' ' + subText(c); });
  return t.replace(/\s+/g, ' ').trim();
}

const documentStub = {
  activeElement: null,
  _listeners: {},
  createElement: function (tag) { return new StubEl(tag); },
  createElementNS: function (ns, tag) { return new StubEl(tag); },
  addEventListener: function (t, fn) { (this._listeners[t] = this._listeners[t] || []).push(fn); }
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
const adSrc = fs.readFileSync(path.join(REPO_DIR, 'HUB/app/js/rooms/ledger-adapter.js'), 'utf8');
const roomSrc = fs.readFileSync(path.join(REPO_DIR, 'HUB/app/js/rooms/ledger.js'), 'utf8');
const css = fs.readFileSync(path.join(REPO_DIR, 'HUB/app/css/ledger.css'), 'utf8');

const windowStub = {};
const sandbox = { window: windowStub, document: documentStub, el: el, console: console,
  setTimeout: function () { return 0; }, clearTimeout: function () {} };
vm.createContext(sandbox);
vm.runInContext(inner(adSrc), sandbox);
vm.runInContext(inner(roomSrc), sandbox);
const LedgerAdapter = windowStub.LedgerAdapter;
const ledger = windowStub.NayaRooms.ledger;

/* ---------- tiny runner ---------- */
let pass = 0, fail = 0;
const failures = [];
function check(name, cond, detail) {
  if (cond) { pass++; }
  else { fail++; failures.push(name + (detail ? ' — ' + detail : '')); }
}

/* ---------- adapter: honest parsing, never invents ---------- */
check('adapter: parseMany([]) -> []', LedgerAdapter.parseMany([]).length === 0);
check('adapter: unparseable input yields [] (never invented)', (function () {
  const out = LedgerAdapter.parseMany([null, 42, 'x', {}, { receipt_id: null }]);
  return out.length === 0;
})());
check('adapter: decision receipt parses (never invents entries)', (function () {
  const dr = { decision_receipt: { decision_id: 'D-9', verdict: 'ACT', issued_at: '2026-10-02T12:00:00Z', candidate_banner: 'NOT RATIFIED', evaluation_order: ['SELF', 'LAW'], gates: [{ node: 'SELF', evaluated: true }], edge_trace: [], receipt_hash: 'ab'.repeat(32), inputs_hash: 'cd'.repeat(32) } };
  const e = LedgerAdapter.parseOne(dr);
  return e && e.kind === 'decision' && e.id === 'D-9' && e.outcome === 'ACT' && e.proofState === 'CANDIDATE' && e.nodes.length === 2;
})());
check('adapter: execution receipt parses with authority basis', (function () {
  const raw = { receipt_id: 'X-1', decision_ref: 'D-9', issued_at: '2026-10-02T12:05:00Z', effects_observed: 'done', authority_basis: { kind: 'director_order', ref: 'o-1' } };
  const e = LedgerAdapter.parseOne(raw);
  return e && e.kind === 'execution' && /director_order/.test(e.authorityBasis) && e.effectsObserved === 'done';
})());
check('adapter: smartNameFor is deterministic', (function () {
  const h = 'a'.repeat(64);
  return LedgerAdapter.smartNameFor(h) === LedgerAdapter.smartNameFor(h) && LedgerAdapter.smartNameFor(h).split(' ').length === 2;
})());
check('adapter: demoStream is deterministic (seeded)', (function () {
  const a = LedgerAdapter.demoStream(), b = LedgerAdapter.demoStream();
  return a.length === 28 && b.length === 28 &&
    a.every((e, i) => e.smartName === b[i].smartName && e.hash === b[i].hash);
})());
check('adapter: demo entries are ALL labeled demo:true', (function () {
  return LedgerAdapter.demoStream().every(e => e.demo === true);
})());
check('adapter: entries sorted newest first', (function () {
  const s = LedgerAdapter.demoStream();
  return s.every((e, i) => i === 0 || String(s[i - 1].issuedAt) >= String(e.issuedAt));
})());

/* ---------- room render ---------- */
const entries = LedgerAdapter.demoStream();
const copied = [];
const stage = ledger(el, { entries: entries, demo: true, onCopy: function (t) { copied.push(t); } });

check('room: stage has ledger-stage class', stage.className === 'ledger-stage');
check('room: header kicker reads SMART LEDGER', (function () {
  const k = byClass(stage, 'lg-kicker')[0];
  return k && k.textContent === 'SMART LEDGER';
})());
check('room: demo banner present in demo mode', byClass(stage, 'lg-demo').length === 1);
check('room: demo banner absent when demo:false', (function () {
  const s2 = ledger(el, { entries: entries, demo: false, onCopy: function () {} });
  return byClass(s2, 'lg-demo').length === 0;
})());

check('room: 4 counters with honest counts', (function () {
  const nums = byClass(stage, 'lg-counter-n').map(n => n.textContent);
  const inn = entries.filter(e => e.kind !== 'execution').length;
  const out = entries.filter(e => e.kind === 'execution').length;
  const ver = entries.filter(e => e.proofState === 'VERIFIED' || e.proofState === 'PRODUCTION-PROVEN').length;
  const ref = entries.filter(e => e.outcome === 'REFUSE').length;
  return nums.join('|') === [inn, out, ver, ref].join('|');
})(), byClass(stage, 'lg-counter-n').map(n => n.textContent).join('|'));
check('room: ACTIONS IN has the pulsing live dot', byClass(stage, 'lg-live-dot').length >= 1);

check('room: 5 tabs with stable identity colors', (function () {
  const tabs = byClass(stage, 'lg-tab');
  const colors = tabs.map(t => t.style.getProperty('--tab-c'));
  return tabs.length === 5 && colors.every(c => !!c) && new Set(colors).size === 5;
})());
check('room: HEARTBEAT tab is active first', (function () {
  const on = byClass(stage, 'lg-tab').filter(t => t.getAttribute('aria-selected') === 'true');
  return on.length === 1 && /HEARTBEAT/.test(on[0].textContent);
})());
check('room: tab colors keyed by view, not position', (function () {
  // stable: heartbeat is always #ef4444 even after re-render
  const s2 = ledger(el, { entries: entries, demo: true, onCopy: function () {} });
  const hb1 = byClass(stage, 'lg-tab')[0].style.getProperty('--tab-c');
  const hb2 = byClass(s2, 'lg-tab')[0].style.getProperty('--tab-c');
  return hb1 === '#ef4444' && hb2 === '#ef4444';
})());

check('room: clicking VALUE tab swaps the view', (function () {
  const tabs = byClass(stage, 'lg-tab');
  tabs[1].click();
  const sel = tabs.filter(t => t.getAttribute('aria-selected') === 'true');
  return sel.length === 1 && /VALUE/.test(sel[0].textContent) && byClass(stage, 'lg-engine').length === 1;
})());
check('room: arrow keys move tab focus (ArrowRight)', (function () {
  const tabsEl = byClass(stage, 'lg-tabs')[0];
  const handler = (tabsEl._listeners.keydown || [])[0];
  const tabs = byClass(stage, 'lg-tab');
  tabs[0].focus();
  handler({ key: 'ArrowRight', preventDefault: function () {} });
  return documentStub.activeElement === tabs[1];
})());

check('room: heartbeat pulse has one beat per entry', (function () {
  // back to heartbeat first
  byClass(stage, 'lg-tab')[0].click();
  return byClass(stage, 'lg-beat').length === entries.length;
})());
check('room: ticker has one row per entry', byClass(stage, 'lg-trow').length === entries.length);
check('room: DEMO label never claims LIVE', (function () {
  const labels = byClass(stage, 'lg-pulse-label').map(n => subText(n));
  return labels.length > 0 && labels.some(t => /DEMO STREAM/.test(t)) &&
    !labels.some(t => /(^|\s)LIVE(\s|·)/.test(t.replace('DEMO STREAM', '')));
})(), byClass(stage, 'lg-pulse-label').map(n => subText(n)).join(' // '));

/* nodes view + drill-down drawer */
check('room: nodes view renders 9 node cards', (function () {
  byClass(stage, 'lg-tab')[2].click();
  return byClass(stage, 'lg-node-card').length === 9;
})());
check('room: node card click opens the evaluation drawer', (function () {
  const self = byClass(stage, 'lg-node-card').filter(c => c.getAttribute('aria-label').indexOf('SELF:') === 0)[0];
  self.click();
  const drawer = byClass(stage, 'lg-node-drawer')[0];
  return drawer.style.display === 'block' && self.getAttribute('aria-expanded') === 'true' &&
    byClass(drawer, 'lg-node-drawer-h').length === 1;
})());
check('room: drawer rows carry real per-entry statuses', (function () {
  const drawer = byClass(stage, 'lg-node-drawer')[0];
  const statuses = byClass(drawer, 'lg-node-status').map(s => s.textContent);
  return statuses.length > 0 && statuses.every(s => /PASS|NON-PASS|EVALUATED|NOT RUN|REFUSED|READ_MORE|ASK/.test(s));
})());
check('room: clicking the card again closes the drawer (no dead buttons)', (function () {
  const self = byClass(stage, 'lg-node-card').filter(c => c.getAttribute('aria-label').indexOf('SELF:') === 0)[0];
  self.click(); // was open -> now closed
  const drawer = byClass(stage, 'lg-node-drawer')[0];
  return drawer.style.display === 'none' && self.getAttribute('aria-expanded') === 'false';
})());

/* proof + receipts views */
check('room: proof view renders 4 ladder columns', (function () {
  byClass(stage, 'lg-tab')[3].click();
  return byClass(stage, 'lg-proof-col').length === 4;
})());
check('room: proof ladder states the law (UNKNOWN != VERIFIED)', (function () {
  return /UNKNOWN/.test(byClass(stage, 'lg-foot')[0].textContent) && /PRODUCTION-PROVEN/.test(byClass(stage, 'lg-foot')[0].textContent);
})());
check('room: receipts view renders one board per entry', (function () {
  byClass(stage, 'lg-tab')[4].click();
  return byClass(stage, 'lg-entry').length === entries.length;
})());
check('room: value view renders the engine strip + charts', (function () {
  byClass(stage, 'lg-tab')[1].click();
  return byClass(stage, 'lg-engine').length === 1 && byClass(stage, 'lg-stage').length === 4 &&
    byClass(stage, 'lg-chart').length >= 2;
})());
check('room: proof view shows calibration (predicted vs observed)', (function () {
  byClass(stage, 'lg-tab')[3].click();
  return byClass(stage, 'lg-sec').some(h => /Calibration/.test(h.textContent));
})());

/* modal behaviors */
check('behavior: chip opens the smart-id modal with the FULL hash', (function () {
  byClass(stage, 'lg-tab')[0].click(); // heartbeat
  const chip = byClass(stage, 'lg-chip')[0];
  chip.focus(); chip.click();
  const overlay = byClass(stage, 'lg-overlay')[0];
  const hashEl = byClass(stage, 'lg-modal-hash')[0];
  return overlay.style.display === 'flex' && hashEl && hashEl.textContent.length === 64;
})());
check('behavior: COPY HASH calls onCopy with the full hash + says COPIED', (function () {
  const cp = byClass(stage, 'lg-copy').filter(b => b.textContent === 'COPY HASH')[0];
  cp.click();
  return copied.length === 1 && copied[0].length === 64 && cp.textContent === 'COPIED';
})());
check('behavior: VIEW RAW toggles the raw JSON', (function () {
  const raw = byClass(stage, 'lg-copy').filter(b => /VIEW RAW|HIDE RAW/.test(b.textContent))[0];
  raw.click();
  const pre = byClass(stage, 'lg-modal-raw')[0];
  const shown = !!pre && pre.textContent.indexOf('demo') !== -1 && raw.textContent === 'HIDE RAW';
  raw.click();
  return shown && byClass(stage, 'lg-modal-raw').length === 0 && raw.textContent === 'VIEW RAW';
})());
check('behavior: Escape closes the modal and returns focus to the chip', (function () {
  const overlay = byClass(stage, 'lg-overlay')[0];
  const opener = documentStub._listeners; // keydown lives on documentStub
  const keyH = documentStub._listeners.keydown.filter(f => String(f).indexOf('Escape') !== -1);
  const chip = byClass(stage, 'lg-chip')[0];
  chip.focus(); chip.click(); // reopen
  const before = documentStub.activeElement; // copy button (focus moved into modal)
  keyH.forEach(f => f({ key: 'Escape' }));
  void opener;
  return overlay.style.display === 'none' && documentStub.activeElement === chip && before !== chip;
})());
check('behavior: INSPECT on a receipt board opens the modal', (function () {
  byClass(stage, 'lg-tab')[4].click();
  const insp = byClass(stage, 'lg-copy').filter(b => b.textContent === 'INSPECT')[0];
  insp.click();
  return byClass(stage, 'lg-overlay')[0].style.display === 'flex';
})());

/* empty states — honest when there is nothing */
check('empty: zero entries -> counters read 0, honest empty messages', (function () {
  const s0 = ledger(el, { entries: [], demo: true, onCopy: function () {} });
  const nums = byClass(s0, 'lg-counter-n').map(n => n.textContent);
  return nums.join('|') === '0|0|0|0' &&
    byClass(s0, 'lg-empty-t').some(t => /No actions recorded yet/.test(t.textContent));
})());
check('empty: receipts view honest with zero entries', (function () {
  const s0 = ledger(el, { entries: [], demo: true, onCopy: function () {} });
  byClass(s0, 'lg-tab')[4].click();
  return byClass(s0, 'lg-empty-t').some(t => /No receipts recorded yet/.test(t.textContent));
})());
check('empty: value view honest when no scored decisions', (function () {
  const sig = LedgerAdapter.demoStream().filter(e => e.kind === 'signal');
  const s1 = ledger(el, { entries: sig, demo: true, onCopy: function () {} });
  byClass(s1, 'lg-tab')[1].click();
  return byClass(s1, 'lg-empty-t').some(t => /No scored decisions yet/.test(t.textContent));
})());
check('empty: node drawer honest for a node with no evaluations', (function () {
  const s1 = ledger(el, { entries: [], demo: true, onCopy: function () {} });
  byClass(s1, 'lg-tab')[2].click();
  byClass(s1, 'lg-node-card')[0].click();
  return byClass(s1, 'lg-empty-t').some(t => /No recorded evaluations/.test(t.textContent));
})());

/* button law: every button does something real */
check('button law: every <button> in the room has a click handler (after modal open)', (function () {
  const btns = allButtons(stage);
  return btns.length > 0 && btns.every(b => (b._listeners.click || []).length > 0);
})(), 'buttons: ' + allButtons(stage).length);

/* ---------- CSS markers (drilled law) ---------- */
check('css: obsidian button gradient present', css.indexOf('linear-gradient(180deg,#1b1b21,#0b0b0e)') !== -1);
check('css: inset top-light on buttons', css.indexOf('inset 0 1px 0 rgba(255,255,255,.16)') !== -1);
check('css: reduced-motion guard scoped to .ledger-stage', (function () {
  return /@media\s*\(\s*prefers-reduced-motion:\s*reduce\s*\)\s*\{\s*\.ledger-stage\s*\*\s*\{\s*animation:\s*none\s*!important;\s*transition:\s*none\s*!important;/.test(css);
})());
check('css: type floor holds (no font-size below 11px)', (function () {
  const ms = css.match(/font-size:\s*([\d.]+)px/g) || [];
  return ms.every(m => parseFloat(m.match(/([\d.]+)/)[1]) >= 11);
})());
check('css: node drawer styles present', css.indexOf('.ledger-stage .lg-node-drawer') !== -1);
check('css: brace balance', (function () {
  const o = (css.match(/\{/g) || []).length, c = (css.match(/\}/g) || []).length;
  return o === c && o > 0;
})());

console.log('\nLEDGER SMOKE: ' + pass + ' passed, ' + fail + ' failed');
if (failures.length) { failures.forEach(f => console.log('  FAIL: ' + f)); process.exit(1); }
console.log('ALL GREEN');
