// probe-fix4.js — dump the welcome regions the fix touches, to files for reading.
var cp = require('child_process');
var fs = require('fs');
var path = require('path');
var t = path.join(__dirname, 'transform-distill.js');
function emit(mode) {
  var r = cp.spawnSync(process.execPath, [t, '--emit', mode], { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });
  if (r.status !== 0) { console.error('transform ' + mode + ' failed', r.status, r.stderr); process.exit(1); }
  return r.stdout;
}
var W = emit('welcome');
var OUT = path.join(__dirname, 'welcome-regions');
try { fs.mkdirSync(OUT); } catch (e) {}
function dump(name, needle, before, after) {
  var i = W.indexOf(needle);
  if (i === -1) { console.log(name + ': NOT FOUND :: ' + needle.slice(0, 80)); return; }
  var s = W.slice(Math.max(0, i - before), i + after);
  fs.writeFileSync(path.join(OUT, name + '.txt'), 'needle@' + i + '\n' + s);
  console.log(name + ': @' + i + ' bytes=' + s.length);
}
dump('wireDeck', '(function wireDeck(){', 0, 4200);
dump('wireLetterUnfold', '(function wireLetterUnfold(){', 0, 4200);
dump('render', 'function render(){', 0, 5200);
dump('derive', 'function derive(){', 0, 2600);
dump('onStageClick', 'function onStageClick(e){', 0, 4200);
dump('updateChrome', 'function updateChrome(){', 0, 3600);
dump('goBridgeToName', 'function goBridgeToName(){', 0, 1600);
dump('submitHandler', "f.addEventListener('submit'", 600, 1400);
dump('bootRestore', '_fpRestoreStage', 400, 2600);
dump('wireDeckAF', 'function wireDeckAF(){', 0, 2600);
dump('enterBtn', "enterBtn.addEventListener('click'", 200, 400);
dump('bExit', "bExit.addEventListener('click'", 0, 900);
dump('fExit', "fExit.addEventListener('click'", 0, 900);
dump('agreeBtn', "agreeBtn.addEventListener('click'", 0, 2200);
dump('wireAgree', '(function wireAgree(){', 0, 2600);
dump('showNHold', 'function showNHold(', 0, 1200);
dump('deckEndAnchor', 'a.deck-next', 200, 1200);
