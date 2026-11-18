#!/usr/bin/env node
/* EPIC DISTILL HARNESS — runs the Epic engine's OWN code, in Node, at
   Factory build time. The engine file is read verbatim (never edited, never
   re-implemented): the canonical + epic <script> blocks are extracted from
   the stored engine file and evaluated in a minimal DOM stub, with ONE
   in-memory export line appended INSIDE the epic IIFE (before its closing
   `})();`) so the closure's functions are callable by the harness. The filed
   engine bytes are untouched by this — the export exists only in the
   evaluated copy, in memory, for this run.
   Usage: node epic-distill-harness.js <engine-path> < job.json
   Job JSON: {groups:[{key,kind,text,tones:[hex,...]}], pastes:{text,note}}
   (pastes default to the engine's own SAMPLES; image uses the engine's own
   DEMO_IMG). Output JSON on stdout:
   {groups:{key:{title,total,sentences,beats:[{tone,html}]}},
    pastes:{text:{...},note:{...},image:{boardHtml}},
    tiles:{money,clicks,points}} — html is the engine's own boardHTML /
   epicImageBoard output. Exits non-zero on any failure. */
'use strict';
const fs = require('fs');
const vm = require('vm');

function fail(msg) { console.error('HARNESS FAIL: ' + msg); process.exit(1); }

const enginePath = process.argv[2];
if (!enginePath) fail('no engine path');
const engine = fs.readFileSync(enginePath, 'utf8');

/* Extract the two <script> blocks by their markers. The canonical block is
   the first <script> in the file; the epic block is the one that opens with
   `(function epic(){`. */
const firstScript = engine.indexOf('<script>');
if (firstScript < 0) fail('no <script> in engine');
const firstEnd = engine.indexOf('</script>', firstScript);
if (firstEnd < 0) fail('canonical script has no close');
const canonical = engine.slice(firstScript + '<script>'.length, firstEnd);

const epicOpen = engine.indexOf('(function epic(){');
if (epicOpen < 0) fail('epic IIFE not found');
const epicClose = engine.indexOf('})();', epicOpen);
if (epicClose < 0) fail('epic IIFE has no close');
const epicSrc = engine.slice(epicOpen, epicClose + '})();'.length);

/* Append the export INSIDE the IIFE, in memory only. */
const EXPORT = '\n;window.__epic={distill:distill,boardHTML:boardHTML,cleanPaste:cleanPaste,epicImageBoard:epicImageBoard,miniTileHTML:miniTileHTML,titleFrom:titleFrom,SAMPLES:SAMPLES,DEMO_IMG:DEMO_IMG,SETS:SETS};\n';
const epicEval = epicSrc.slice(0, epicSrc.lastIndexOf('})();')) + EXPORT + '})();';

/* --- Minimal DOM stub: only what the two scripts touch at top level. --- */
function makeEl(id) {
  return {
    id: id || '', innerHTML: '', textContent: '', value: '', hidden: false,
    files: null, style: { setProperty: function () {} },
    classList: { add: function () {}, remove: function () {}, toggle: function () {}, contains: function () { return false; } },
    addEventListener: function () {}, removeEventListener: function () {},
    setAttribute: function () {}, getAttribute: function () { return null; },
    querySelectorAll: function () { return []; },
    querySelector: function () { return null; },
    closest: function () { return null; },
    scrollIntoView: function () {},
    appendChild: function () {},
    getBoundingClientRect: function () { return { top: 0, bottom: 0 }; },
  };
}
const els = {};
function getEl(id) { if (!els[id]) els[id] = makeEl(id); return els[id]; }
class ImageStub { constructor() { this._src = ''; } set src(v) { this._src = v; } get src() { return this._src; } }
const documentStub = {
  getElementById: function (id) { return getEl(id); },
  querySelectorAll: function () { return []; },
  querySelector: function () { return null; },
  createElement: function () { return makeEl(''); },
  body: { style: { setProperty: function () {} } },
};
const windowStub = {
  location: { search: '' },
  matchMedia: function () { return { matches: false }; },
  addEventListener: function () {},
  console: console,
};
windowStub.document = documentStub;
const sandbox = {
  window: windowStub, document: documentStub, console: console,
  setTimeout: setTimeout, clearTimeout: clearTimeout,
  Image: ImageStub,
  FileReader: function () {},
};
sandbox.window.window = sandbox.window;
vm.createContext(sandbox);
try {
  vm.runInContext(canonical, sandbox, { filename: 'epic-canonical.js' });
  vm.runInContext(epicEval, sandbox, { filename: 'epic-engine.js' });
} catch (e) {
  fail('engine eval failed: ' + (e && e.stack || e));
}
const E = sandbox.window.__epic;
if (!E || typeof E.distill !== 'function') fail('export missing after eval');

/* --- Job in on stdin. --- */
let jobRaw = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', function (c) { jobRaw += c; });
process.stdin.on('end', function () {
  let job;
  try { job = JSON.parse(jobRaw || '{}'); } catch (e) { fail('job JSON parse: ' + e.message); }
  const out = { groups: {}, pastes: {}, tiles: {} };
  const DEEP = ['#8e24aa', '#0f52ba', '#07925f', '#d4a017', '#c2410c', '#c62828', '#a21caf', '#3f51b5'];

  function distillGroup(key, kind, text, tones) {
    const d = E.distill(text);
    if (!d) fail('distill returned null for group ' + key);
    const beats = d.beats.map(function (sentences, i) {
      const tone = (tones && tones[i]) || DEEP[i % DEEP.length];
      const title = i === 0 ? d.title : E.titleFrom(sentences[0]);
      return { tone: tone, html: E.boardHTML(kind, title, 'One idea per board.', sentences, tone, i, d.beats.length) };
    });
    return { title: d.title, total: d.total, sentences: d.beats.reduce(function (n, b) { return n + b.length; }, 0), beats: beats };
  }

  (job.groups || []).forEach(function (g) {
    out.groups[g.key] = distillGroup(g.key, g.kind, g.text, g.tones);
  });

  const textPaste = (job.pastes && job.pastes.text) || E.SAMPLES.text;
  const notePaste = (job.pastes && job.pastes.note) || E.SAMPLES.note;
  out.pastes.text = distillGroup('paste-text', 'PLAIN TEXT, DISTILLED', textPaste, DEEP);
  out.pastes.note = distillGroup('paste-note', 'A SMART NOTE, DISTILLED', notePaste, DEEP);
  /* Seams must never show: assert here, in the engine's own terms. */
  const cleaned = E.cleanPaste(notePaste);
  if (cleaned.indexOf('SN-') !== -1) fail('seam strip failed: SN- id survived cleanPaste');
  if (cleaned.indexOf('Nutshell:') !== -1) fail('seam strip failed: Nutshell: label survived cleanPaste');
  out.pastes.note.seamsStripped = true;
  out.pastes.text.seamsStripped = E.cleanPaste(textPaste).indexOf('SN-') === -1;

  /* Image: the engine's own DEMO_IMG becomes the board. Capture the HTML
     the engine hands to showResults (the stub body's innerHTML). */
  getEl('epicResultsBody').innerHTML = '';
  E.epicImageBoard(E.DEMO_IMG, 'A world, in deep color.', 'The demo image — gold sun, emerald mountain, sapphire mountain. The image is the board.');
  const imgHtml = getEl('epicResultsBody').innerHTML;
  if (!imgHtml || imgHtml.indexOf('epic-img-board') === -1) fail('image board not produced');
  if (imgHtml.indexOf('background-image:url(') === -1) fail('image board has no background image');
  out.pastes.image = { boardHtml: imgHtml, demoImage: true };

  /* Tiles: the Dashboard's own renderer, alive in the engine. */
  const s0 = E.SETS[0];
  /* _osMiniNumHTML lives on window, not in __epic — read it off the stub. */
  const tilesFn = sandbox.window._osMiniNumHTML;
  if (typeof tilesFn !== 'function') fail('_osMiniNumHTML not exposed by engine');
  function countTiles(html) { return (html.match(/os-mini-tile/g) || []).length; }
  out.tiles = {
    sets0: s0,
    moneyHtml: tilesFn(s0.money, 'med'),
    clicksHtml: tilesFn(s0.clicks, 'med'),
    pointsHtml: tilesFn(s0.points, 'med'),
  };
  out.tiles.counts = { money: countTiles(out.tiles.moneyHtml), clicks: countTiles(out.tiles.clicksHtml), points: countTiles(out.tiles.pointsHtml) };
  if (out.tiles.counts.money !== 5 || out.tiles.counts.clicks !== 4 || out.tiles.counts.points !== 3) {
    fail('hero tile counts wrong: ' + JSON.stringify(out.tiles.counts) + ' (want 5/4/3)');
  }

  process.stdout.write(JSON.stringify(out));
});
