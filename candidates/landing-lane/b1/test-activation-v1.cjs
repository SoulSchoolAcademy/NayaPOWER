'use strict';
// test-activation-v1.cjs — Activation fix validation (TEAM BUILD, 2026-10-28).
// Usage: node test-activation-v1.cjs
// Proves: the exact query "how to do input a smart note" returns the
// SN-1880 block at #1 AND activation opens that block itself as a
// standalone view (no feed scroll, no feed navigation, no href to
// follow). Same for Q2 (SN-1887) and Q3 (SN-1886). Edge cases prove a
// blockless result is UNAVAILABLE, never a feed fallback.
// Exits 0 only if every check passes. Ranking is untouched by this
// file; the five open ranks remain owed (see report), not fixed here.
const fs = require('fs');
const path = require('path');
const HERE = __dirname;
const I = require('./integration-v3.js');
const A = require('./activation-v1.js');
const corpus = JSON.parse(fs.readFileSync(path.join(HERE, 'refreshed-notes.json'), 'utf8'))
  .concat(JSON.parse(fs.readFileSync(path.join(HERE, 'notes-base-official.json'), 'utf8')))
  .concat(JSON.parse(fs.readFileSync(path.join(HERE, 'notes-base-concat.json'), 'utf8')));
const FAILURES = [];
function check(name, cond, detail) {
  console.log((cond ? 'PASS' : 'FAIL') + ' ' + name + (detail ? ' ' + detail : ''));
  if (!cond) FAILURES.push(name);
}
function esc(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}
function checkActivation(label, query, expectedId, expectedTitle) {
  const res = I.integratedSearch(corpus, query);
  const top = res.data.items[0];
  check(label + '-top-is-expected', !!(top && top.id === expectedId),
    'top=' + (top ? top.id : 'none'));
  check(label + '-top-title', !!(top && top.title === expectedTitle),
    'title=' + (top ? top.title : 'none'));
  check(label + '-top-has-block', !!(top && top.block && top.block.title),
    'block=' + (top && top.block ? top.block.title : 'none'));
  const view = A.activateResult(top);
  check(label + '-action-standalone', view.action === 'open-block-standalone', 'action=' + view.action);
  check(label + '-noteId-matches', view.noteId === expectedId, 'noteId=' + view.noteId);
  check(label + '-block-is-matched-block', view.block === top.block, 'same-object=' + (view.block === top.block));
  check(label + '-title-matches', view.title === expectedTitle, 'title=' + view.title);
  check(label + '-no-feed-scroll', view.feedScroll === false, 'feedScroll=' + view.feedScroll);
  check(label + '-no-feed-navigation', view.feedNavigation === null, 'feedNavigation=' + view.feedNavigation);
  check(label + '-open-target-block-itself', view.openTarget === 'block-itself', 'openTarget=' + view.openTarget);
  check(label + '-standalone-has-title', view.standaloneHtml.indexOf(esc(expectedTitle)) !== -1, 'has-title');
  if (top.block.nutshell) {
    check(label + '-standalone-has-nutshell', view.standaloneHtml.indexOf(esc(String(top.block.nutshell).slice(0, 40))) !== -1, 'has-nutshell-snippet');
  }
  check(label + '-standalone-no-anchor', view.standaloneHtml.indexOf('<a ') === -1, 'no-<a>');
  check(label + '-standalone-no-href', view.standaloneHtml.indexOf('href=') === -1, 'no-href');
  check(label + '-standalone-no-feed-path', view.standaloneHtml.indexOf('/hub/feed') === -1, 'no-feed-path');
  check(label + '-standalone-is-card-minus-anchors', view.standaloneHtml === A.stripAnchors(view.panelCardHtml), 'card-minus-anchors');
  return view;
}
checkActivation('Q1', 'how to do input a smart note',
  'IB-SMART-NOTE-20261026-sn1880-how-to-input-a-smart-note',
  'How to Input a Smart Note, Successfully — So It Goes Live');
checkActivation('Q2', 'No Ego — Do What\'s Right, Not Just What\'s Said',
  'IB-SMART-NOTE-20261027-sn1887-no-ego-do-whats-right-not-just-whats-said',
  'No Ego — Do What\'s Right, Not Just What\'s Said');
checkActivation('Q3', 'The Inheritance — Intelligence That Outlives Its Founder',
  'IB-SMART-NOTE-20261027-sn1886-the-inheritance-intelligence-that-outlives-its-founder',
  'The Inheritance — Intelligence That Outlives Its Founder');
const vNull = A.activateResult(null);
check('EDGE-null-unavailable', vNull.action === 'unavailable', 'action=' + vNull.action);
check('EDGE-null-no-feed', vNull.feedScroll === false && vNull.feedNavigation === null, 'no-feed-fallback');
const vNoBlock = A.activateResult({ id: 'x', title: 'No block here' });
check('EDGE-noblock-unavailable', vNoBlock.action === 'unavailable', 'action=' + vNoBlock.action);
check('EDGE-noblock-no-feed', vNoBlock.feedScroll === false && vNoBlock.feedNavigation === null, 'no-feed-fallback');
console.log('FAILURES:', FAILURES.length ? FAILURES : 'none');
console.log('ALL_PASS:', FAILURES.length === 0);
process.exit(FAILURES.length ? 1 : 0);
