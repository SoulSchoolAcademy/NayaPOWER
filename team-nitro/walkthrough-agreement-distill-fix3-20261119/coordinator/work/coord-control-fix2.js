// COORDINATOR control, part 2 — the input leg against FIX-2 bytes (not base).
// The fix-2 checker proved: on fix-2 bytes, the paired input reads "" after
// boot (FIX3's clear wipes FIX2's pre-fill). Base bytes have no FIX2 pre-fill,
// and FIX6's own load check fills the field — so base is the wrong control
// for the input leg. This script reproduces the fix-2 bytes and checks the
// input leg there, plus confirms fix-3 fixes it on the same harness.
// Usage: node coord-control-fix2.js (exit 0 = control reproduced + fix confirmed)
var fs = require('fs');
var path = require('path');
var H = require('/home/hatch/workspace/team-nitro/walkthrough-agreement-distill-fix3-20261119/maker/work/dom-harness3-dom.js');
var makeEnv = H.makeEnv, q = H.q, sleep = H.sleep;
var runFix2 = require('./run-fix2-localbase.js');

var pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('  PASS ' + name); }
  else { fail++; console.log('  FAIL ' + name + (detail ? ' — ' + detail : '')); }
}

(async function () {
  var R = await runFix2();
  console.log('fix-2 reproduced: identity ' + Buffer.byteLength(R.I) + 'B, walk ' + Buffer.byteLength(R.WK) + 'B');
  var crypto = require('crypto');
  var sha = function (s) { return crypto.createHash('sha256').update(s, 'utf8').digest('hex'); };
  console.log('fix-2 identity sha: ' + sha(R.I).slice(0, 16) + ' (expect d0f26529)');
  console.log('fix-2 walk sha: ' + sha(R.WK).slice(0, 16) + ' (expect 854a8f60)');

  // Control: fix-2 paired identity — input must read "" (checker's Fail 1).
  var e = makeEnv(R.I, '?name=Distill%20Eye%20Walk&alias=Distill');
  await sleep(50);
  var input = q(e.document, '#aliasInput');
  check('CONTROL fix-2 paired input is EMPTY after boot (the bug)', !!input && input.value === '', 'value=' + JSON.stringify(input && input.value));
  var hero = q(e.document, '#displayName');
  check('CONTROL fix-2 hero blank+hidden (the bug)', !!hero && hero.textContent === '' && hero.hidden === true, 'text=' + JSON.stringify(hero && hero.textContent));

  // Fix-3 on the same harness, same URL — input + hero must be painted.
  var DIR = '/home/hatch/workspace/team-nitro';
  var fixedI = fs.readFileSync(path.join(DIR, 'walk-v23-assembly-20261114/identity-fixed.html'), 'utf8');
  var e2 = makeEnv(fixedI, '?name=Distill%20Eye%20Walk&alias=Distill');
  await sleep(50);
  var input2 = q(e2.document, '#aliasInput');
  check('FIX-3 paired input holds the alias', !!input2 && input2.value === 'distill', 'value=' + JSON.stringify(input2 && input2.value));
  var hero2 = q(e2.document, '#displayName');
  check('FIX-3 hero paints the passed name', !!hero2 && hero2.textContent === 'Distill Eye Walk' && hero2.hidden === false, 'text=' + JSON.stringify(hero2 && hero2.textContent));

  console.log('\nCOORDINATOR-CONTROL-FIX2: ' + pass + ' pass / ' + fail + ' fail');
  process.exit(fail ? 1 : 0);
})().catch(function (err) { console.error('FATAL', err); process.exit(2); });
