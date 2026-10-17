#!/usr/bin/env node
/* reports-smoke.js — stub-DOM suite for the Reports room (Room 02).
 *
 * Covers the room's real behaviors plus the CSS law markers:
 *   - week strip (7 tiles, rainbow-day accents, live/open/todo)
 *   - dynamic orient date (no hardcoded date)
 *   - archive cards newest-first, honest empty states (no invented reports)
 *   - full report board: sections, scorecard dials, chain strip, pull-quotes,
 *     prompt copy button
 *   - period tabs switch + aria; search filters; every button typed
 *   - adapter distillation (chain, scores, prompt) and loader dayPaths
 *   - CSS law markers: reduced-motion block, obsidian button gradient,
 *     11px+ label type floor
 *
 * Run: node HUB/app/preview/tests/reports-smoke.js   (repo root)
 */
'use strict';
const fs = require('fs');
const path = require('path');

const ROOM = path.join(__dirname, '../../js/rooms');
const CSS = fs.readFileSync(path.join(__dirname, '../../css/reports.css'), 'utf8');

/* ---------- minimal DOM stub ---------- */
class El {
  constructor(tag) {
    this.tagName = String(tag).toUpperCase();
    this.children = [];
    this._cls = '';
    this.textContent = '';
    this.attrs = {};
    this._listeners = {};
    this.style = { _p: {}, setProperty(k, v) { this._p[k] = v; } };
    this._innerHTML = '';
    this.disabled = false;
    this.type = undefined;
    this.value = '';
    this.placeholder = '';
  }
  set className(v) { this._cls = String(v); }
  get className() { return this._cls; }
  set innerHTML(v) { this._innerHTML = String(v); if (this._innerHTML === '') this.children = []; }
  get innerHTML() { return this._innerHTML; }
  appendChild(c) { this.children.push(c); return c; }
  addEventListener(t, f) { (this._listeners[t] = this._listeners[t] || []).push(f); }
  fire(t, ev) { (this._listeners[t] || []).forEach(f => f(ev || {})); }
  click() { this.fire('click'); }
  setAttribute(k, v) { this.attrs[k] = String(v); }
  getAttribute(k) { return this.attrs[k]; }
  querySelector(sel) { return findOne(this, sel.replace(/^\./, '')); }
  querySelectorAll(sel) { return findAll(this, sel.replace(/^\./, '')); }
}
function hasClass(e, cls) { return e instanceof El && e.className.split(/\s+/).includes(cls); }
function findAll(root, cls) {
  const out = [];
  const walk = e => { for (const c of e.children) { if (c instanceof El) { if (hasClass(c, cls)) out.push(c); walk(c); } } };
  walk(root); return out;
}
function findOne(root, cls) { return findAll(root, cls)[0] || null; }

const document = { createElement: tag => new El(tag) };
const window = { scrollTo: () => { window._scrolled = true; } };
const navigator = { clipboard: { writeText: async t => { navigator._copied = t; } } };

function el(tag, cls, text) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (text !== undefined && text !== null) e.textContent = text;
  return e;
}

function innerOf(file) {
  const s = fs.readFileSync(file, 'utf8');
  const a = s.indexOf('(function(){');
  const b = s.lastIndexOf('})();');
  if (a === -1 || b === -1) throw new Error('IIFE wrapper missing in ' + file);
  return s.slice(a + '(function(){'.length, b);
}
new Function('el', 'document', 'window', 'navigator', innerOf(path.join(ROOM, 'reports-adapter.js')))(el, document, window, navigator);
new Function('el', 'document', 'window', 'navigator', innerOf(path.join(ROOM, 'reports.js')))(el, document, window, navigator);
new Function('el', 'document', 'window', 'navigator', innerOf(path.join(ROOM, 'reports-loader.js')))(el, document, window, navigator);

const ReportsRoom = window.NayaRooms.reports;
const Adapter = window.ReportsAdapter;
const Loader = window.ReportsLoader;

/* ---------- fixtures (adapter-shaped, like the loader produces) ---------- */
const REPORTS = [
  { id: 'R-2026-10-02', ib: 'IB-20261002-001', period: 'daily', date: '2026-10-02',
    dateKey: '2026-10-02', dateLabel: 'October 2, 2026', scope: 'NayaPOWER / System Intelligence',
    status: 'CANONICAL', title: 'Daily Intelligence Briefing', subtitle: 'A concrete memory surface',
    bigPicture: 'The big shift: Daily Intelligence became a concrete Brain memory surface.',
    sections: [
      { label: 'WHAT CHANGED?', kind: 'standard',
        nutshell: 'In a nutshell: the canonical home was confirmed and history was filed.',
        points: ['The canonical Brain home for daily reports was confirmed and written down.',
                 'The existing October 1 report established the current canonical record shape.'] },
      { label: 'SCORECARD', kind: 'scorecard',
        nutshell: 'Strong on architecture, honest about composition.',
        scores: [{ label: 'Architecture', value: '8.5/10' }, { label: 'Trust boundaries', value: '9/10' }],
        chain: ['CREATE REPORT', 'VERIFY CANONICAL PATH', 'HUB PROJECTS EVENT'],
        points: ['Architecture: real code, genuinely running through the runtime today.'] },
      { label: 'EXACT READY-TO-USE PROMPT', kind: 'prompt',
        prompt: 'Take the LEARN intake repair and execute it through the default runtime.' },
      { label: 'A VOICE', kind: 'standard',
        points: [{ t: 'Do not rebuild what exists. Compose it, follow the receipts.', q: true }] },
    ] },
  { id: 'R-2026-10-01', ib: 'IB-20261001-001', period: 'daily', date: '2026-10-01',
    dateKey: '2026-10-01', dateLabel: 'October 1, 2026', scope: 'NayaPOWER / System Intelligence',
    status: 'CANONICAL', title: 'Daily Intelligence Briefing',
    bigPicture: 'Yesterday we moved from designing the brain into proving it.',
    sections: [] },
];

/* ---------- tiny runner ---------- */
let pass = 0, fail = 0;
const failures = [];
function t(name, fn) {
  try { fn(); pass++; }
  catch (e) { fail++; failures.push(name + ' — ' + e.message); }
}
function eq(a, b, msg) { if (a !== b) throw new Error((msg || 'eq') + ': got ' + JSON.stringify(a) + ', want ' + JSON.stringify(b)); }
function ok(v, msg) { if (!v) throw new Error(msg || 'expected truthy'); }

/* ---------- tests ---------- */
t('mount: stage renders with orient, tabs, search, list', () => {
  const s = ReportsRoom(el, { reports: REPORTS });
  ok(hasClass(s, 'reports-stage'), 'stage class');
  ok(findOne(s, 'orient'), 'orient');
  eq(findAll(s, 'report-tab').length, 4, 'four period tabs');
  ok(findOne(s, 'search-input'), 'search input');
  ok(findOne(s, 'reports-list'), 'list zone');
});

t('orient date is dynamic, not hardcoded', () => {
  const s = ReportsRoom(el, { reports: REPORTS });
  const now = new Date();
  const names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  const months = ['January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'];
  const want = names[now.getDay()] + ', ' + months[now.getMonth()] + ' ' + now.getDate() + ', ' + now.getFullYear();
  eq(findOne(s, 'orient-date').textContent, want, 'orient date');
});

t('week strip: 7 tiles, day tiles carry live reports', () => {
  const s = ReportsRoom(el, { reports: REPORTS });
  eq(findAll(s, 'day-tile').length, 7, 'seven day tiles');
  const tiles = findAll(s, 'day-tile');
  const liveTiles = tiles.filter(x => hasClass(x, 'live'));
  eq(liveTiles.length, 2, 'two live tiles (Oct 1 + Oct 2)');
  const live = liveTiles[0];
  ok(live.style._p['--day'], 'day accent color set');
});

t('archive cards newest-first', () => {
  const s = ReportsRoom(el, { reports: REPORTS });
  const cards = findAll(s, 'report-card');
  eq(cards.length, 2, 'two cards');
  ok(findOne(cards[0], 'card-kicker').textContent.includes('FRIDAY, OCTOBER 2, 2026'), 'newest first');
});

t('open report: full board with all section kinds', () => {
  const s = ReportsRoom(el, { reports: REPORTS });
  findAll(s, 'card-open')[0].click();
  ok(window._scrolled, 'scroll to top on open');
  const board = findOne(s, 'report-board');
  ok(board, 'board present');
  eq(findAll(board, 'rb-section').length, 4, 'four sections');
  eq(findAll(board, 'sc-dial').length, 2, 'two score dials');
  eq(findAll(board, 'sc-link').length, 3, 'three chain pills');
  ok(findOne(board, 'prompt-copy'), 'copy button');
  const quotes = findAll(board, 'rb-quote');
  eq(quotes.length, 1, 'quote renders as pull-quote, not bullet');
  ok(findOne(board, 'rb-prov'), 'provenance footer');
});

t('copy prompt uses clipboard and confirms', async () => {
  const s = ReportsRoom(el, { reports: REPORTS });
  findAll(s, 'card-open')[0].click();
  const copy = findOne(s, 'prompt-copy');
  copy.click();
  await new Promise(r => setTimeout(r, 20));
  eq(copy.textContent, 'COPIED \u2713', 'copy confirmation');
  ok((navigator._copied || '').includes('LEARN intake repair'), 'prompt text copied');
});

t('back button returns to list', () => {
  const s = ReportsRoom(el, { reports: REPORTS });
  findAll(s, 'card-open')[0].click();
  findOne(s, 'report-back').click();
  ok(findOne(s, 'reports-list'), 'list restored');
});

t('weekly tab: honest empty state, no invented report', () => {
  const s = ReportsRoom(el, { reports: REPORTS });
  findAll(s, 'report-tab')[1].click(); // WEEKLY
  const note = findOne(s, 'quiet-note');
  ok(note, 'quiet note present');
  ok(note.textContent.includes('No weekly reports yet'), 'honest empty');
  ok(note.textContent.includes('will not invent'), 'anti-invention line');
  eq(findAll(s, 'report-tab')[1].getAttribute('aria-selected'), 'true', 'aria-selected');
});

t('search filters archive and reports no-match honestly', () => {
  const s = ReportsRoom(el, { reports: REPORTS });
  const input = findOne(s, 'search-input');
  eq(input.getAttribute('aria-label'), 'Search reports', 'aria label');
  input.value = 'concrete brain memory';
  input.fire('input');
  eq(findAll(s, 'report-card').length, 1, 'one match');
  input.value = 'zzz-no-such-report';
  input.fire('input');
  eq(findAll(s, 'report-card').length, 0, 'zero cards');
  ok(findOne(s, 'quiet-note').textContent.includes('No reports match'), 'no-match note');
});

t('empty ctx.reports: honest empty, never invents', () => {
  const s = ReportsRoom(el, { reports: [] });
  const note = findOne(s, 'quiet-note');
  ok(note && note.textContent.includes('No daily reports yet'), 'honest empty daily');
});

t('day board: open day with no report stays honest', () => {
  const s = ReportsRoom(el, { reports: REPORTS });
  const openTiles = findAll(s, 'day-tile open');
  if (!openTiles.length) return; // depends on the day of week; live tiles suffice
  findOne(openTiles[0], 'tile-view').click();
  const board = findOne(s, 'report-board');
  ok(board, 'day board opens');
  ok(findOne(board, 'rb-nutshell').textContent.includes('no raw report'), 'honest nutshell');
});

t('keyboard/aria: all buttons typed, tabs carry role', () => {
  const s = ReportsRoom(el, { reports: REPORTS });
  const btns = [];
  const walk = e => { for (const c of e.children) { if (c instanceof El) { if (c.tagName === 'BUTTON') btns.push(c); walk(c); } } };
  walk(s);
  ok(btns.length > 5, 'several buttons');
  btns.forEach(b => eq(b.type, 'button', 'button type on ' + b.className));
  findAll(s, 'report-tab').forEach(tb => eq(tb.getAttribute('role'), 'tab', 'tab role'));
});

t('adapter: distills chain, scores, prompt from markdown', () => {
  const md = [
    '# Canonical Intelligence Report Record',
    '',
    'Object type: DAILY_INTELLIGENCE_REPORT',
    'Intelligent Block ID: IB-DIR-NAYAPOWER-20261002-001',
    'Report ID: DIR-NAYAPOWER-2026-10-02',
    'Period type: DAILY', 'Period date: 2026-10-02',
    'Scope: NayaPOWER / System Intelligence', 'Status: CANONICAL',
    '',
    '# Daily Intelligence Briefing — October 2, 2026',
    '',
    'The big picture: a concrete memory surface now exists.',
    '',
    '## WHAT CHANGED?',
    '',
    'A substantial paragraph about what changed in the system today, more than thirty chars.',
    '',
    '- First real bullet with enough text to survive the length floor.',
    '',
    '## SCORECARD',
    '',
    'Architecture is holding at 8.5/10 while trust boundaries sit closer to 9/10.',
    '',
    '## THE CHAIN',
    '',
    'CREATE REPORT \u2192 VERIFY CANONICAL PATH \u2192 HUB PROJECTS EVENT \u2192 HUMAN OPENS REPORT',
    '',
    '## EXACT READY-TO-USE PROMPT',
    '',
    '> Run the wiring proof through the default runtime and show receipts.',
  ].join('\n');
  const r = Adapter.parse(md);
  eq(r.id, 'DIR-NAYAPOWER-2026-10-02', 'report id');
  eq(r.dateKey, '2026-10-02', 'date key');
  eq(r.bigPicture, 'The big picture: a concrete memory surface now exists.', 'big picture');
  eq(r.sections.length, 4, 'four sections');
  const sc = r.sections.find(x => x.kind === 'scorecard');
  eq(sc.scores.length, 2, 'two score dials');
  ok(sc.scores[0].value === '8.5/10', 'first dial 8.5/10');
  const ch = r.sections.find(x => x.chain && x.chain.length);
  eq(ch.chain.length, 4, 'four chain pills');
  const pr = r.sections.find(x => x.kind === 'prompt');
  ok(pr.prompt.includes('wiring proof'), 'prompt distilled');
});

t('loader: dayPaths builds the canonical Brain path', () => {
  const p = Loader.dayPaths('2026-10-02');
  eq(p.file, 'BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/DAILY/2026/10/02/IB-DIR-NAYAPOWER-20261002-001.md', 'canonical path');
});

t('CSS: reduced-motion law block present', () => {
  ok(CSS.includes('@media (prefers-reduced-motion: reduce)'), 'media query');
  ok(CSS.includes('.reports-stage *{ animation:none !important; transition:none !important; }'), 'stage-wide still rule');
});

t('CSS: obsidian button gradient + top-light law', () => {
  ok(CSS.includes('linear-gradient(180deg,#1b1b21,#0b0b0e)'), 'obsidian gradient');
  ok(CSS.includes('inset 0 1px 0 rgba(255,255,255,.16)'), 'top-light catch');
});

t('CSS: 11px label type floor (no sub-11px font-size)', () => {
  const bad = CSS.match(/font-size:(8|9|10)px/g);
  eq(bad, null, 'no sub-11px sizes');
});

/* ---------- report ---------- */
(async () => {
  // wait for the async copy test
  await new Promise(r => setTimeout(r, 50));
  console.log('\nreports-smoke: ' + pass + ' passed, ' + fail + ' failed');
  failures.forEach(f => console.log('  FAIL ' + f));
  process.exit(fail ? 1 : 0);
})();
