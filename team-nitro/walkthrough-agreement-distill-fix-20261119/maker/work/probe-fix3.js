// probe-fix3.js — the unfold's real show/hide mechanism in the distill bytes.
var cp = require('child_process');
var path = require('path');
var t = path.join(__dirname, 'transform-distill.js');
function emit(mode) {
  var r = cp.spawnSync(process.execPath, [t, '--emit', mode], { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });
  if (r.status !== 0) { console.error('transform ' + mode + ' failed', r.status, r.stderr); process.exit(1); }
  return r.stdout;
}
var U = emit('unfold');
// 1. every rule mentioning frame-now or deckBody, with offset
var re = /[^{}]*frame-now[^{}]*\{[^}]*\}|[^{}]*#deckBody[^{}]*\{[^}]*\}/g, m;
console.log('=== UNFOLD frame-now / #deckBody rules ===');
while ((m = re.exec(U)) !== null) console.log('@' + m.index + ' ' + JSON.stringify(m[0].slice(0, 300)));
// 2. the [hidden] rules with offsets
re = /\.letter-beat\[hidden\]\{[^}]*\}/g;
console.log('=== UNFOLD .letter-beat[hidden] rules ===');
while ((m = re.exec(U)) !== null) console.log('@' + m.index + ' ' + JSON.stringify(m[0]));
// 3. showFrame / wireFrame7 / wireFrame8 in distill unfold
['function showFrame', 'wireFrame7', 'wireFrame8', 'frame-now', 'classList.add(\'frame-now\')', 'classList.remove(\'frame-now\')'].forEach(function (needle) {
  var i = U.indexOf(needle);
  console.log('--- ' + needle + ' first@' + i);
  if (i !== -1) console.log(JSON.stringify(U.slice(i, i + 700)));
});
// 4. how articles are hidden in markup: count hidden attributes on letter-beat
console.log('letter-beat hidden count: ' + (U.split('class="letter-beat').length - 1));
console.log('hidden> on beats: ' + (U.match(/class="letter-beat[^"]*"[^>]*hidden/g) || []).length);
console.log('frame-now class in markup: ' + (U.match(/frame-now/g) || []).length);
// 5. the af-prog pill + MutationObserver in unfold
var j = U.indexOf('af-prog');
console.log('af-prog first@' + j + ' ' + JSON.stringify(U.slice(j - 200, j + 500)));
