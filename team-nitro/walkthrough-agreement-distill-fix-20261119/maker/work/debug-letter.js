// debug-letter.js — one mirror click in ?stage=letter: dump states.
var H = require('./dom-harness.js');
(async function () {
  var F = H.fixed();
  var e = H.makeEnv(F.welcome, '?stage=letter');
  var doc = e.document;
  console.log('errors:', e.errors.length);
  var lb = doc.querySelectorAll('#letterBody .letter-beat[data-distilled]');
  console.log('distilled:', lb.length, 'hidden 1-3:', lb.slice(0, 3).map(function (b) { return b.hidden; }).join(','));
  var d1 = doc.querySelector('#deckBody .letter-beat[data-beat="1"] .ib-nutshell');
  var l1 = doc.querySelector('#letterBody .letter-beat[data-distilled][data-beat="1"] .ib-nutshell');
  console.log('DECK B1:', JSON.stringify(d1 ? d1.textContent : '?'));
  console.log('LET  B1:', JSON.stringify(l1 ? l1.textContent : '?'));
  var nb = doc.querySelector('#fpNextBtn');
  nb.click();
  await H.sleep(50);
  console.log('after 1 click: jewel=', JSON.stringify(doc.querySelector('#fpStageJewelNum').textContent));
  console.log('hidden 1-3:', lb.slice(0, 3).map(function (b) { return b.hidden; }).join(','));
  console.log('fp-now 1-3:', lb.slice(0, 3).map(function (b) { return b.classList.contains('fp-now'); }).join(','));
  console.log('mirror text after:', JSON.stringify(nb.textContent));
  console.log('beat1 .deck-next exists:', !!lb[0].querySelector('.deck-next'));
  process.exit(0);
})();
