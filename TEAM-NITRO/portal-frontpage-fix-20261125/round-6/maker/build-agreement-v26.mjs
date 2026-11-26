// build-agreement-v26.mjs — Portal round 6e: the live /agreement file
// (v25, 22,953,906 B, sha 2c88513f…) edited so the preview intro is GONE
// and the agreement opens on the welcome player, then LET'S GO starts
// slide 1 "The Old Way", all 27 slides in order, end slide = deed text +
// Agree at the very bottom (flashing) above the arrows, eight links on a
// bar BELOW the page. No text harvested, no slides reordered, no legal
// pages touched. Output: agreement-v25-fixed-r6.html in this lane — the
// captain's live step R2-PUTs it to key agreement-v25.html.
import fs from 'node:fs';
import crypto from 'node:crypto';
import vm from 'node:vm';

const SRC = '/home/hatch/workspace/team-nitro/dashboard/bullseye-20261124/agreement-v25.html';
const SRC_SHA = '2c88513f9011b176c0af910ec0d81e314578cfe904dd62ded9010a9a54052e11';
const OUT = new URL('./agreement-v25-fixed-r6.html', import.meta.url).pathname;

const DEED = 'By entering your name, you make it official — you are signing the Collective Agreement, and you get the deed to your own world: high-level digital real estate — your personal page, your business, your space — free forever.';

let html = fs.readFileSync(SRC, 'utf8');
const fails = [];
function assert(name, ok, extra = '') {
  console.log((ok ? 'PASS ' : 'FAIL ') + name + (extra ? ' — ' + extra : ''));
  if (!ok) fails.push(name);
}
function rep(oldS, newS, n, tag) {
  const parts = html.split(oldS);
  if (parts.length - 1 !== n) { console.log('FAIL rep ' + tag + ': expected ' + n + ' got ' + (parts.length - 1)); fails.push('rep ' + tag); return; }
  html = parts.join(newS);
  console.log('replaced ' + tag);
}
function count(re) { return (html.match(re) || []).length; }

assert('base sha verified', crypto.createHash('sha256').update(fs.readFileSync(SRC)).digest('hex') === SRC_SHA);

// ---- V1. Remove the whole preview intro (comment + section) ----
{
  const start = html.indexOf('<!-- ======= CHOICE');
  const end = html.indexOf('<section class="screen" id="screen-cover">');
  assert('V1: choice comment + section found', start > 0 && end > start, 'start=' + start + ' end=' + end);
  const span = html.slice(start, end);
  assert('V1: removed span is the intro (has Begin the visual story + screen-choice)', span.includes('Begin the visual story') && span.includes('screen-choice') && span.includes('Read the agreement'));
  html = html.slice(0, start) + html.slice(end);
}
rep('<section class="screen" id="screen-cover">', '<section class="screen active" id="screen-cover">', 1, 'V1 cover active');

// ---- V2. JS: screens object minus choice; show() minus choice ----
rep(", choice: document.getElementById('screen-choice')", '', 1, 'V2 screens object');
rep("if (name === 'cover' || name === 'choice') barForCover();", "if (name === 'cover') barForCover();", 1, 'V2 show()');

// ---- V2c. Remove the choice-wiring IIFE (script 2) — buttons gone, deep links gone ----
rep(`/* WHOLE-SYSTEM CONNECTION 2026-11-24 (items 10/53) — choice wiring + the
   final-board reader. Deep links: ?view=deck starts the visual story,
   ?view=letter opens the letter. Closing a legal page returns to the view
   it came from (lastScreen), so the choice is the bridge. */
(function(){
  function startDeck(){ current = 0; renderSlide(); show('slide'); }
  var deckBtn = document.getElementById('fpChoiceDeck');
  var letterBtn = document.getElementById('fpChoiceLetter');
  var playBtn = document.getElementById('fpChoicePlay');
  if (deckBtn) deckBtn.addEventListener('click', startDeck);
  if (playBtn) playBtn.addEventListener('click', startDeck);
  if (letterBtn) letterBtn.addEventListener('click', function(){ openLegal('terms'); });
  var q = new URLSearchParams(window.location.search);
  if (q.get('view') === 'deck'){ startDeck(); }
  else if (q.get('view') === 'letter'){ openLegal('terms'); }
})();`, '', 1, 'V2c choice wiring IIFE');

// ---- V3. Remove the choice CSS rules (raw rule parser, byte-preserving) ----
function stripComments(sel) { return sel.replace(/\/\*[\s\S]*?\*\//g, ''); }
function parseCssChunks(text) {
  const chunks = []; let i = 0; const n = text.length;
  while (i < n) {
    const prefixStart = i;
    while (i < n) {
      if (text.startsWith('/*', i)) { const e = text.indexOf('*/', i + 2); i = e < 0 ? n : e + 2; }
      else if (/\s/.test(text[i])) i++;
      else break;
    }
    if (i >= n) { chunks.push({ raw: text.slice(prefixStart), kind: 'tail' }); break; }
    const selStart = i; let j = i; let inStr = null; let opened = false;
    while (j < n) {
      const ch = text[j];
      if (inStr) { if (ch === '\\') j += 2; else { if (ch === inStr) inStr = null; j++; } continue; }
      if (ch === '"' || ch === "'") { inStr = ch; j++; continue; }
      if (ch === '{') { opened = true; j++; break; }
      if (ch === ';' || ch === '}') { j++; break; }
      j++;
    }
    if (!opened) { chunks.push({ raw: text.slice(prefixStart, j), kind: 'tail' }); i = j; continue; }
    let depth = 1; let k = j; inStr = null;
    while (k < n && depth > 0) {
      const ch = text[k];
      if (inStr) { if (ch === '\\') k += 2; else { if (ch === inStr) inStr = null; k++; } continue; }
      if (ch === '"' || ch === "'") { inStr = ch; k++; continue; }
      if (ch === '{') depth++;
      else if (ch === '}') { depth--; if (depth === 0) { k++; break; } }
      k++;
    }
    chunks.push({ raw: text.slice(prefixStart, k), sel: text.slice(selStart, j - 1), kind: 'rule' });
    i = k;
  }
  return chunks;
}
function isChoiceSelector(sel) {
  return /screen-choice|\.choice-|#fpChoice|choice-pill|choice-play/.test(stripComments(sel));
}
function filterCss(text) {
  let out = '', dropped = 0, kept = 0;
  for (const c of parseCssChunks(text)) {
    if (c.kind !== 'rule') { out += c.raw; continue; }
    const sel = c.sel.trim();
    if (sel.startsWith('@')) {
      const open = c.raw.indexOf('{');
      const inner = c.raw.slice(open + 1, c.raw.lastIndexOf('}'));
      const filtered = filterCss(inner);
      if (filtered.trim() === '') { dropped++; continue; }
      out += c.raw.slice(0, open + 1) + filtered + c.raw.slice(c.raw.lastIndexOf('}'));
      kept++;
    } else if (isChoiceSelector(sel)) { dropped++; }
    else { out += c.raw; kept++; }
  }
  filterCss.lastDropped = dropped; filterCss.lastKept = kept;
  return out;
}
{
  const styleOpen = html.indexOf('<style>');
  const styleClose = html.indexOf('</style>');
  assert('V3: style block found', styleOpen > 0 && styleClose > styleOpen);
  const before = html.slice(styleOpen, styleClose);
  const after = filterCss(before);
  console.log('V3: CSS rules dropped=' + filterCss.lastDropped + ' kept=' + filterCss.lastKept);
  assert('V3: choice CSS dropped, base rules kept', filterCss.lastDropped > 0 && filterCss.lastKept > 100);
  html = html.slice(0, styleOpen) + after + html.slice(styleClose);
}

// ---- V4. Audio bar goes (element stays, hidden, no controls) ----
rep('<audio class="real-audio" id="welcomeAudio" preload="auto" controls playsinline aria-label="Naya\'s Welcome — the actual recording"></audio>',
  '<audio class="real-audio" id="welcomeAudio" preload="auto" hidden playsinline aria-label="Naya\'s Welcome — the actual recording"></audio>', 1, 'V4 audio hidden');

// ---- V5. Facade moves out of the frame to below it (static row) ----
const FACADE = `                  <button class="pm-facade" id="videoFacade" type="button" aria-label="Play the welcome video — with sound">
                    <span class="pm-play-disc" aria-hidden="true">&#9654;</span>
                    <span class="pm-facade-label">Watch Naya&rsquo;s Welcome<small>Tap to play &mdash; with sound, and her voice on the deck</small></span>
                  </button>
`;
rep(FACADE, '', 1, 'V5 facade out of frame');
rep('                </div>\n                <p class="cover-saying">',
  '                </div>\n                <button class="pm-facade" id="videoFacade" type="button" aria-label="Play the welcome video — with sound">\n                  <span class="pm-play-disc" aria-hidden="true">&#9654;</span>\n                  <span class="pm-facade-label">Watch Naya&rsquo;s Welcome<small>Tap to play &mdash; with sound, and her voice on the deck</small></span>\n                </button>\n                <p class="cover-saying">', 1, 'V5 facade below frame');

// ---- V8a. renderSlide: remove the links bar too on non-last renders ----
rep(`var _oldRow = document.getElementById('fpFinalRow');
  if (_oldRow) _oldRow.remove();`,
  `var _oldRow = document.getElementById('fpFinalRow');
  if (_oldRow) _oldRow.remove();
  var _oldBar = document.getElementById('fpLinksBar');
  if (_oldBar) _oldBar.remove();`, 1, 'V8a oldBar removal');

// ---- V8b. End slide: deed text + Agree at the bottom; links on a bar below the page ----
const NEW_FINAL = `  if (current === TOTAL - 1){
    var _row = document.createElement('div');
    _row.id = 'fpFinalRow'; _row.className = 'fp-final-row';
    _row.innerHTML = '<p class="fp-final-deed">${DEED}</p>' +
      '<button class="fp-agree-btn" type="button" data-fp-agree>I agree &#9670;</button>';
    var _nav = document.querySelector('#screen-slide .floatnav');
    if (_nav && _nav.parentNode) _nav.parentNode.insertBefore(_row, _nav);
    else document.getElementById('slideBoards').appendChild(_row);
    _row.querySelectorAll('[data-fp-agree]').forEach(function(b){
      b.addEventListener('click', function(){ goToPortal(); });
    });
    var _bar = document.createElement('div');
    _bar.id = 'fpLinksBar'; _bar.className = 'fp-links-bar';
    _bar.innerHTML = '<p class="fp-links-label">The Invitation</p>' +
      '<nav class="fp-final-links">' +
      '<button class="fp-final-link" type="button" data-final="vow">Our Vow</button>' +
      '<button class="fp-final-link" type="button" data-final="deal">The Deal</button>' +
      '<button class="fp-final-link" type="button" data-final="promise">Our Promise</button>' +
      '<button class="fp-final-link" type="button" data-final="governance">The Governance</button>' +
      '<button class="fp-final-link" type="button" data-final="constitution">Our Constitution</button>' +
      '<button class="fp-final-link" type="button" data-final="laws">Our Laws</button>' +
      '<button class="fp-final-link" type="button" data-final="rules">Our Rules</button>' +
      '<button class="fp-final-link" type="button" data-final="oath">Our Oath</button></nav>';
    if (_nav && _nav.parentNode) _nav.parentNode.insertBefore(_bar, _nav.nextSibling);
    else document.getElementById('slideBoards').appendChild(_bar);
    _bar.querySelectorAll('[data-final]').forEach(function(b){
      b.addEventListener('click', function(){ openFinal(b.getAttribute('data-final')); });
    });
  }`;
{
  const anchor = '  var _oldBar = document.getElementById(\'fpLinksBar\');';
  const a = html.indexOf('  if (current === TOTAL - 1){', html.indexOf(anchor));
  const b = html.indexOf("  var dec = document.createElement('div'); dec.innerHTML = s.t;", a);
  assert('V8b: last-slide block found', a > 0 && b > a, 'a=' + a + ' b=' + b);
  const span = html.slice(a, b);
  assert('V8b: removed block is the old end slide (invite + 8 links + agree)', span.includes('fp-final-invite') && span.includes('data-final="vow"') && span.includes('data-fp-agree'));
  html = html.slice(0, a) + NEW_FINAL + '\n' + html.slice(b);
}

// ---- V9. Completion flag in goToPortal() ----
rep('function goToPortal(){\n', "function goToPortal(){\n  try{localStorage.setItem('nayanet_agreement_done', new Date().toISOString());}catch(e){}\n", 1, 'V9 completion flag');

// ---- V6/V7/V8c. Appended ROUND 6e CSS (facade row, poster contain, end slide, phone fit) ----
const R6E_CSS = `
/* ROUND 6e (2026-11-26) — the preview intro is gone; the agreement opens on
   the welcome player. (1) The main play button no longer covers the picture:
   it sits BELOW the visual, in the clear space, as one static row.
   (2) The poster shows WHOLE and centered (object-fit:contain).
   (3) End slide (slide 27): deed text + Agree at the very bottom above the
   arrows, flashing; the eight links sit on a bar BELOW the page.
   (4) Phone fit: the cover's caption strip and its (dead) arrows hide so the
   whole player frame fits the viewport. */
#screen-cover .pm-facade{position:static;width:100%;height:auto;display:flex;flex-direction:row;align-items:center;justify-content:center;gap:14px;padding:12px 16px 0;background:none;border-radius:0}
#screen-cover .pm-facade .pm-play-disc{flex:none}
#screen-cover .pm-facade-label{text-align:left}
#screen-cover .pm-art-frame.playing + .pm-facade{display:none !important}
#screen-cover .pm-poster{object-fit:contain;object-position:center center}
#screen-slide > .fp-final-row{margin:0 auto;text-align:center;max-width:860px;padding:12px 16px 6px}
#screen-slide > .fp-final-row .fp-final-deed{font-family:Marcellus,Georgia,serif;font-size:19px;line-height:1.6;color:#fff;margin:0 0 12px}
#screen-slide > .fp-final-row .fp-agree-btn{margin-top:0;animation:agreeFlash 2.4s ease-in-out infinite}
@keyframes agreeFlash{0%,100%{box-shadow:0 0 18px rgba(47,232,158,.22)}50%{box-shadow:0 0 42px rgba(47,232,158,.55)}}
#screen-slide > .fp-links-bar{flex:none;text-align:center;padding:10px 16px 14px;border-top:1px solid rgba(255,255,255,.18)}
#screen-slide > .fp-links-bar .fp-links-label{font-family:Marcellus,Georgia,serif;font-size:19px;color:#fff;margin:0 0 6px}
#screen-slide > .fp-links-bar .fp-final-links{display:flex;flex-wrap:wrap;justify-content:center;gap:8px 14px}
@media(max-width:640px){
#screen-cover .pm-cap{display:none}
#screen-cover .floatnav{display:none}
#screen-cover .pm-side .orb-wrap:not(.jewel){width:96px;height:96px}
#screen-cover .cover-n{width:48px;height:48px;margin-top:6px}
#screen-cover .pm-facade{padding-top:8px}
#screen-cover .pm-facade .pm-play-disc{width:56px;height:56px;font-size:20px}
}
`;
rep('</style>', R6E_CSS + '</style>', 1, 'V6/V7/V8c R6e CSS');

// ---- V assertions ----
assert('V: 0 "Begin the visual story"', count(/Begin the visual story/g) === 0, 'got ' + count(/Begin the visual story/g));
assert('V: 0 "Read the agreement"', count(/Read the agreement/g) === 0, 'got ' + count(/Read the agreement/g));
assert('V: 0 "Welcome. Let\'s begin with trust."', count(/Welcome\. Let.s begin with trust\./g) === 0, 'got ' + count(/Welcome\. Let.s begin with trust\./g));
assert('V: 0 screen-choice', count(/screen-choice/g) === 0, 'got ' + count(/screen-choice/g));
assert('V: 0 choice-pill / choice-play / fpChoice', count(/choice-pill|choice-play|fpChoice/g) === 0, 'got ' + count(/choice-pill|choice-play|fpChoice/g));
assert("V: 0 show('choice')", count(/show\('choice'\)/g) === 0);
assert('V: cover active in markup', count(/class="screen active" id="screen-cover"/g) === 1);
assert('V: audio hidden, no controls', html.includes('<audio class="real-audio" id="welcomeAudio" preload="auto" hidden playsinline'));
assert('V: facade no longer inside the frame', !html.includes('id="videoShell" hidden></div>\n                  <button class="pm-facade"'));
assert('V: facade directly after the frame close', html.includes('</div>\n                <button class="pm-facade"'));
assert('V: poster contain override present', html.includes('#screen-cover .pm-poster{object-fit:contain'));
assert('V: deed text verbatim in renderSlide', count(new RegExp(DEED.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g')) === 1);
assert('V: agree button + flash present', html.includes('data-fp-agree') && html.includes('@keyframes agreeFlash'));
assert('V: links bar present (fpLinksBar)', count(/fpLinksBar/g) === 2 && html.includes('#screen-slide > .fp-links-bar'));
assert('V: all eight links kept', ['vow','deal','promise','governance','constitution','laws','rules','oath'].every(k => html.includes('data-final="' + k + '"')));
assert('V: completion flag in goToPortal', count(/localStorage\.setItem\('nayanet_agreement_done'/g) === 1);
const TITLES = ['The Old Way','Welcome','The Collective Intelligence Network','Your Worlds','In a Nutshell','The System','How It Works','Your Day','Smart Calendar','The Simple Version','For AIs','Your AIs, Together','The Mother Brain','The Machine View','What It Means','Plug In','Why It Matters','The Naya Machine','Your Three Worlds','The Whole-System Unfolding','Done For You','The Platform','Your Own Worlds',"What's In It For You","You're Hired",'Your Franchise'];
assert('V: all 27 slide titles present', TITLES.every(t => html.includes(t)), 'missing: ' + TITLES.filter(t => !html.includes(t)).join(', '));
assert('V: v7 ending present', html.includes('Welcome home. Your world begins here'));
assert('V: legal pages intact (12)', count(/id="legal-/g) === 12 && html.includes('FP_FINAL') && html.includes('function openFinal'));
assert('V: base poster/frame rules intact', html.includes('.pm-poster{') && html.includes('.pm-art-frame{'));
// both inline scripts compile
{
  const scripts = [];
  let p = -1;
  while ((p = html.indexOf('<script>', p + 1)) >= 0) {
    const e = html.indexOf('</script>', p);
    scripts.push(html.slice(p + 8, e));
  }
  assert('V: two inline scripts found', scripts.length === 2, 'got ' + scripts.length);
  scripts.forEach((code, i) => {
    try { console.time('compile script ' + (i + 1)); new vm.Script(code, { filename: 'agreement-script-' + (i + 1) + '.js' }); console.timeEnd('compile script ' + (i + 1)); console.log('PASS V: script ' + (i + 1) + ' compiles (' + code.length + ' B)'); }
    catch (e) { console.log('FAIL V: script ' + (i + 1) + ' compile — ' + e.message); fails.push('script ' + (i + 1) + ' compile'); }
  });
}

if (fails.length) { console.log('FAILED: ' + fails.join(' | ')); process.exit(1); }
fs.writeFileSync(OUT, html, 'utf8');
const out = fs.readFileSync(OUT);
console.log('agreement-v25-fixed-r6.html ' + out.length + ' B sha256 ' + crypto.createHash('sha256').update(out).digest('hex'));
console.log('v25 was ' + fs.readFileSync(SRC).length + ' B; delta ' + (out.length - fs.readFileSync(SRC).length) + ' B');
