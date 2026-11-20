// probe-fix.js — gather exact anchors + counts from the distill outputs (in-memory).
// Run: node probe-fix.js  (in maker/work/)
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
function count(s, needle) { return s.split(needle).length - 1; }
function show(label, s, needle, ctx) {
  var n = count(s, needle);
  console.log(label + ' :: ' + JSON.stringify(needle) + ' => ' + n);
  if (ctx && n > 0) {
    var i = s.indexOf(needle);
    console.log('   first ctx: ' + JSON.stringify(s.slice(Math.max(0, i - 120), i + 220)));
  }
}
console.log('unfold bytes=' + Buffer.byteLength(U) + ' welcome bytes=' + Buffer.byteLength(W));
show('U', U, 'hired', true);
show('W', W, 'hired', true);
show('U', U, '99 out of 100', true);
show('W', W, '99 out of 100', true);
show('U', U, 'supercomputer', true);
show('W', W, 'supercomputer', true);
show('U', U, 'superhighway', false);
show('W', W, 'superhighway', false);
show('W', W, 'Nine pictures', true);
show('U', U, 'Nine pictures', false);
show('W', W, 'ib-subtitle', false);
show('U', U, 'ib-subtitle', false);
show('U', U, 'Waiting on the captioned video', true);
show('W', W, 'fpEnterDeal', true);
show('U', U, '#deckBody .letter-beat:not(.frame-now)', false);
show('U', U, '#deckBody.letter-beat{height:100%', false);
// welcome anchors for one-phase fix
show('W', W, "if (b.querySelector('.lb-showcase') && !b.classList.contains('fp-smart-visual'))", false);
show('W', W, "b.classList.toggle('fp-smart-visual',sd&&S.phase==='visual')", false);
show('W', W, "S.phase=(db&&db.classList.contains('fp-smart-visual'))?'visual':'talk'", false);
show('W', W, "function deckEnd(){return S.deck>=deckBeats.length-1&&(!hasShowcase(deckBeats[S.deck])||S.phase==='visual');}", false);
show('W', W, "function letterEnd(){return S.letter>=letterBeats.length-1&&(!hasShowcase(letterBeats[S.letter])||S.phase==='visual');}", false);
show('W', W, "if(S.view==='deck'&&S.phase!=='visual'){", false);
show('W', W, "enterBtn.addEventListener('click',function(){window.__fpDeckEndReturn=false;enterStage();});", false);
show('W', W, "window.location.href='/identity.html'+(v?'?name='+encodeURIComponent(v):'')", false);
show('W', W, "if (st === 'deck') on();", false);
show('W', W, "body.fp-stage-on #fpAgreement .fp-now.fp-smart-talk .lb-showcase{display:none}", false);
show('W', W, "S.phase='talk';", false);
// board 15/34/37 text in boards data
var B = require('./boards-distill.js');
[15, 34, 37].forEach(function (i) {
  var x = B[i - 1];
  console.log('BOARD ' + i + ' kind=' + x.kind + ' title=' + JSON.stringify(x.title) + ' sub=' + JSON.stringify(x.sub));
  (x.lines || []).forEach(function (l) { console.log('  L: ' + l); });
});
console.log('boards total=' + B.length);
