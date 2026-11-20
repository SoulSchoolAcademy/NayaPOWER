// probe-fix2.js — exact CSS rules + render/derive/Back forms in the distill outputs.
var fs = require('fs');
var cp = require('child_process');
var path = require('path');
var t = path.join(__dirname, 'transform-distill.js');
function emit(mode) {
  var r = cp.spawnSync(process.execPath, [t, '--emit', mode], { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });
  if (r.status !== 0) { console.error('transform ' + mode + ' failed', r.status, r.stderr); process.exit(1); }
  return r.stdout;
}
var U = emit('unfold'), W = emit('welcome');
function grepAll(s, re, label, max) {
  var m, n = 0;
  console.log('=== ' + label + ' ===');
  while ((m = re.exec(s)) !== null) {
    n++;
    if (n <= (max || 20)) console.log('[' + n + '] ' + JSON.stringify(m[0].slice(0, 400)));
    if (m[0].length === 0) re.lastIndex++;
  }
  console.log('total: ' + n);
}
grepAll(U, /\.letter-beat[^{]*\{[^}]*\}/g, 'UNFOLD .letter-beat CSS rules');
grepAll(U, /frame-now/g, 'UNFOLD frame-now occurrences');
grepAll(W, /fp-smart-visual/g, 'WELCOME fp-smart-visual occurrences');
grepAll(W, /S\.phase=/g, 'WELCOME S.phase= assignments');
grepAll(W, /<p class="ib-subtitle">/g, 'WELCOME <p class="ib-subtitle"> elements');
grepAll(U, /<p class="ib-subtitle">/g, 'UNFOLD <p class="ib-subtitle"> elements');
grepAll(U, /hired/g, 'UNFOLD hired (all, short ctx)', 10);
// show the SCRIPT hired line in unfold
var i = U.indexOf('hired');
var seen = 0;
while (i !== -1 && seen < 8) {
  console.log('U hired ctx ' + seen + ': ' + JSON.stringify(U.slice(Math.max(0, i - 160), i + 120)));
  i = U.indexOf('hired', i + 1); seen++;
}
