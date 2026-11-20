#!/usr/bin/env node
// control-fix2.js — NON-VACUITY CONTROL for the fix-3 harness.
// Runs the F9 scenarios against the FIX-2 bytes (before the fix-3 transforms)
// and expects the three checker fails to REPRODUCE. If the control does not
// reproduce them, the fix-3 harness cannot detect the bugs and its passes are
// vacuous. Exit 0 iff all three bugs reproduce; exit 1 otherwise.
// No file writes. Deterministic.
const runFix2 = require('./run-fix2-export.js');
const H1 = require('./dom-harness3-dom.js');
const makeEnv = H1.makeEnv, q = H1.q, qa = H1.qa, sleep = H1.sleep;

function identityParts(doc) {
  var inputs = qa(doc, 'input');
  var input = null;
  for (var ii = 0; ii < inputs.length; ii++) {
    var ph = inputs[ii].getAttribute('placeholder') || '';
    if (ph.indexOf('lias') !== -1) { input = inputs[ii]; break; }
  }
  if (!input && inputs.length) input = inputs[0];
  var nameEl = doc.querySelector('[data-cert-name]') || doc.querySelector('.cert-name');
  return { input: input, nameEl: nameEl };
}

(async () => {
  const R = await runFix2();
  let reproduced = 0;
  console.log('\n== CONTROL: F9 scenarios on FIX-2 bytes (bugs must reproduce) ==');

  // C1 — F9(a) input, the checker's literal scenario: ?name= ONLY on fix-2
  // bytes. Expect value "" (fix-2's pre-fill is wiped by the FIX3 clear and
  // FIX6 paints nothing without an alias). NOTE: on fix-3 bytes the same ""
  // is CORRECT by the captain's reconciliation (never pre-paint unpaired —
  // main harness S6b); the operative paired case is covered by C2 + S6a.
  const e1 = makeEnv(R.I, '?name=Distill%20Eye%20Walk');
  await sleep(50);
  const p1 = identityParts(e1.document);
  const v1 = p1.input ? p1.input.value : null;
  console.log('C1 identity ?name=-only input value on fix-2 bytes: ' + JSON.stringify(v1) + ' (expect "")');
  if (v1 === '') { reproduced++; console.log('C1 REPRODUCED — F9(a) input fail present on fix-2 bytes'); }
  else console.log('C1 NOT REPRODUCED — harness cannot see fail 1');

  // C2 — F9(a) echo: PAIRED identity on fix-2 bytes. Expect hero blank +
  // hidden + no data-text (fix-2 sets textContent only, before the load-time
  // paint, and never sets data-text).
  const e2 = makeEnv(R.I, '?name=Distill%20Eye%20Walk&alias=Distill');
  await sleep(50);
  const p2 = identityParts(e2.document);
  const n1 = p2.nameEl;
  const t1 = n1 ? n1.textContent : null, h1 = n1 ? n1.hidden : null, d1 = n1 ? n1.getAttribute('data-text') : 'no-el';
  console.log('C2 identity-paired hero on fix-2 bytes: text=' + JSON.stringify(t1) + ' hidden=' + h1 + ' data-text=' + JSON.stringify(d1) + ' (expect ""/true/null)');
  if (t1 === '' && h1 === true && d1 === null) { reproduced++; console.log('C2 REPRODUCED — F9(a) echo fail present on fix-2 bytes'); }
  else console.log('C2 NOT REPRODUCED — harness cannot see fail 2');

  // C3 — F9(b) door: aliased walk, fix-2 bytes. Expect step-1 visible after ~1s (fetch verdict advances it).
  const e3 = makeEnv(R.WK, '?name=Distill%20Eye%20Walk&alias=Distill');
  const doc3 = e3.document;
  function vis() { return qa(doc3, '[id^="step-"]').filter(function (el) { return !el.hidden; }).map(function (el) { return el.id; }); }
  const before = vis();
  await sleep(1500);
  const after = vis();
  console.log('C3 walk door on fix-2 bytes: before=' + JSON.stringify(before) + ' after 1.5s=' + JSON.stringify(after) + ' (expect ["step-door"] -> ["step-1"])');
  if (JSON.stringify(before) === '["step-door"]' && after.indexOf('step-1') !== -1 && after.indexOf('step-door') === -1) {
    reproduced++; console.log('C3 REPRODUCED — F9(b) door-guard fail present on fix-2 bytes');
  } else console.log('C3 NOT REPRODUCED — harness cannot see fail 3');

  console.log('\nCONTROL: ' + reproduced + '/3 checker fails reproduced on fix-2 bytes');
  process.exit(reproduced === 3 ? 0 : 1);
})().catch((e) => { console.error('FATAL', e); process.exit(1); });
