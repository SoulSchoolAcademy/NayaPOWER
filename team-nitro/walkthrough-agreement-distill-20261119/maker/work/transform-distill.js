#!/usr/bin/env node
/* DISTILL transform (2026-11-19, visual-led — Shawn 19:54 MST, supersedes the 10-board count):
   Base: v5 AF bytes (unfold sha 4a2e84b0, welcome sha 1f37416d) — NOT fix-9.
   37 boards (27 image + 10 text) on ALL THREE presentations:
   1. UNFOLD (/agreement): 24 articles -> 37 (image boards keep .lb-showcase,
      text boards have none — wireDeck's visual step lingers on pictures only).
   2. WELCOME deck (?stage=deck): 9 slides -> 37, same boards, deck shell.
   3. WELCOME letter (?stage=letter): 34 data-distilled beats -> 37, letter shell.
   Long text goes: #deckAll (unfold), #letterAll + #fpLinkLetterAll (welcome),
   the #dealPlain dialog (its opener is gone; its JS refs are all null-guarded
   already — openPlainLetter returns early, listeners are `if (x)`-guarded).
   The frame is harvested verbatim (AF CSS/JS untouched) except two additions:
   headFor no longer hardcodes board 0 (board 1 is now a picture board), and a
   small progress pill (.af-prog: jewel + "N / 37" + bar) is added to the unfold
   frame — the stage's own jewel/number/bar is kept untouched in the welcome.
   Pictures are harvested at runtime from the base bytes (never typed by hand):
   deck slides/faces, unfold showcases/faces, letter b-photos, deck logo.
   Guards: article counts, per-board sentence counts (img 1-2, txt 3-5),
   no "read the whole" anywhere, no dealPlain dialog, agree + seal + frame
   wiring intact, no audio/mp3, node --check every script block.
   stdout carries ONLY the two output paths + shas (JSON); bytes are written
   to the out paths (temp + verify + rename, never truncate-first). */
const fs = require('fs');
const crypto = require('crypto');
const { spawnSync } = require('child_process');
const BOARDS = require('./boards-distill.js');
console.log = (...a) => console.error(...a);

const UNFOLD_LOCAL = '/home/hatch/workspace/team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html';
const WELCOME_LOCAL = '/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/welcome-staged.html';
const UNFOLD_AF_SHA = '4a2e84b0104bf404b3e576ea91725cf0cd931688ff84837cc8ae177e2d952fb9';
const WELCOME_AF_SHA = '1f37416d79b0959b21dffb450d34e1a409dfe934fac40a144ecf0b0ef9f7cc49';
const TONES = ['#8e24aa', '#0f52ba', '#07925f', '#d4a017', '#c2410c', '#c62828', '#a21caf', '#3f51b5', '#0e7490', '#6d28d9'];
const TONE_CLASS = ['tone-purple', 'tone-sapphire', 'tone-emerald'];

function sha(b) { return crypto.createHash('sha256').update(b).digest('hex'); }
function fail(m) { console.error('DISTILL-FAIL: ' + m); process.exit(1); }
function esc(s) { return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
function sentCount(lines) {
  let n = 0;
  for (const l of lines) n += l.split(/(?<=[.!?])\s+/).filter(x => x.length > 0).length;
  return n;
}
function checkScripts(text, label) {
  const blocks = [...text.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
  console.log(label + ' script blocks: ' + blocks.length);
  blocks.forEach((code, idx) => {
    const r = spawnSync('node', ['--check', '-'], { input: code });
    if (r.status !== 0) fail(label + ' script block ' + idx + ' fails node --check: ' + String(r.stderr).slice(0, 300));
  });
}
function noForbiddenMedia(text, label) {
  if (/<audio/.test(text) || /agreement-naya-voice|62bf05e6|Inside_the_NayaNET|b60233efb19466a0356330778ce38d5363d38cc77ca87435a64187d4c20eef19/.test(text))
    fail(label + ': forbidden media referenced');
}
function noLongText(text, label) {
  // Visible text only (scripts/styles hold history comments, incl. the
  // wireLetter OVERHAUL note); the legal ToS "read the whole page" is a
  // different document and stays — the agreement's "read the whole letter /
  // agreement" must be gone.
  const vis = text.replace(/<script[\s\S]*?<\/script>/g, ' ').replace(/<style[\s\S]*?<\/style>/g, ' ');
  if (/read the whole (letter|agreement)/i.test(vis)) fail(label + ': "read the whole letter/agreement" still present');
  if (/id="dealPlain"/.test(text)) fail(label + ': dealPlain dialog still present');
  if (/Download the letter/.test(text)) fail(label + ': plain-letter download still present');
}

/* ---- harvest pictures from the base bytes (never typed by hand) ---- */
function harvest(baseU, baseW) {
  const H = {};
  // Deck slides 1-9: showcase src+alt, face src (from the 9 deck articles).
  const di = baseW.indexOf('id="deckBody"');
  const deckArts = [...baseW.slice(di).matchAll(/<article[\s\S]*?<\/article>/g)].map(m => m[0]).slice(0, 9);
  if (deckArts.length !== 9) fail('deck article harvest count is not 9: ' + deckArts.length);
  H.slides = deckArts.map((a, i) => {
    const s = a.match(/lb-showcase"><img src="([^"]+)" alt="([^"]*)"/);
    const f = a.match(/deal-beat-photo" src="([^"]+)"/);
    if (!s || !f) fail('deck slide ' + (i + 1) + ' missing showcase or face');
    return { src: s[1], alt: s[2], face: f[1] };
  });
  const dl = deckArts[0].match(/ib-foot-logo" src="([^"]+)"/);
  if (!dl) fail('deck logo not found');
  H.deckLogo = dl[1];
  // Unfold showcases keyed by welcome-N, unfold faces in order, unfold logo.
  H.wel = {};
  for (const m of baseU.matchAll(/lb-showcase"><img src="([^"]+)" alt="([^"]*)"/g)) {
    const k = (m[1].match(/welcome-(\d+)\.jpg/) || [])[1];
    if (k) H.wel[k] = { src: m[1], alt: m[2] };
  }
  H.ufaces = [...new Set([...baseU.matchAll(/deal-beat-photo" src="([^"]+)"/g)].map(m => m[1]))];
  const ul = baseU.match(/ib-foot-logo" src="([^"]+)"/);
  if (!ul) fail('unfold logo not found');
  H.unfoldLogo = ul[1];
  if (Object.keys(H.wel).length < 8) fail('unfold showcase harvest < 8: ' + Object.keys(H.wel).length);
  if (H.ufaces.length < 7) fail('unfold face harvest < 7: ' + H.ufaces.length);
  // Letter b-photos in order (distinct), agmt-unfold-20 alt.
  const li = baseW.indexOf('id="letterBody"');
  const lbSeg = baseW.slice(li, li + 400000);
  H.bphotos = [...new Set([...lbSeg.matchAll(/deal-beat-photo" src="([^"]+)"/g)].map(m => m[1]))];
  if (H.bphotos.length < 13) fail('letter b-photo harvest < 13: ' + H.bphotos.length);
  const a20 = lbSeg.match(/agmt-unfold-20\.jpg" alt="([^"]*)"/);
  H.agmt20alt = a20 ? a20[1] : 'Not just an app';
  // v5 unfold final article inner content (sign frame + ambChoice + ambNote), verbatim.
  const lastArt = [...baseU.matchAll(/<article[\s\S]*?<\/article>/g)].map(m => m[0]).pop();
  if (!/dealAgreeBtn/.test(lastArt)) fail('v5 final article has no agree button');
  H.signInner = lastArt.replace(/^<article[^>]*>/, '').replace(/<\/article>\s*$/, '');
  return H;
}
function picFor(H, key) {
  if (key.startsWith('slide-')) {
    const n = parseInt(key.slice(6), 10);
    return { src: H.slides[n - 1].src, alt: H.slides[n - 1].alt };
  }
  if (key.startsWith('wel-')) {
    const w = H.wel[key.slice(4)];
    if (!w) fail('no harvested welcome picture for ' + key);
    return w;
  }
  if (key.startsWith('face-')) {
    const n = parseInt(key.slice(5), 10);
    return { src: H.slides[n - 1].face, alt: 'Naya speaking' };
  }
  if (key === 'agmt20') return { src: '/agmt-unfold-20.jpg', alt: H.agmt20alt };
  fail('unknown pic key ' + key);
}

/* ---- article builders (one board shape per route) ---- */
function nutshellHTML(b) { return '<div class="ib-nutshell">' + b.lines.map(l => '<p>' + esc(l) + '</p>').join('') + '</div>'; }
function unfoldArticle(H, b, i) {
  const n = i + 1;
  const tone = TONES[i % TONES.length];
  const hidden = i === 0 ? '' : ' hidden';
  const face = H.ufaces[i % H.ufaces.length];
  let out = '<article class="intel-board letter-beat" data-beat="' + n + '" style="--tone:' + tone + '"' + hidden + '>'
    + '<div class="ib-blocktop"><img class="deal-beat-photo" src="' + face + '" alt="Naya speaking">'
    + '<div class="ib-identity"><span class="ib-jewel" aria-hidden="true">&#9670;</span><div>'
    + '<span class="ib-kind">' + esc(b.kind) + '</span><h2 class="ib-title">' + esc(b.title) + '</h2>'
    + '</div></div></div>' + nutshellHTML(b);
  if (b.type === 'img') {
    const p = picFor(H, b.pic);
    out += '<figure class="lb-showcase"><img src="' + p.src + '" alt="' + esc(p.alt) + '"></figure>';
  }
  if (i === BOARDS.length - 1) {
    out += H.signInner;
  } else {
    out += '<div class="ib-foot"><img class="ib-foot-logo" src="' + H.unfoldLogo + '" alt="NayaNET"> &middot; NayaNET &middot; The Collective Agreement</div>'
      + '<button class="p3-enter letter-next deck-next" type="button" data-beat="' + n + '">Keep reading &#9670;</button>';
  }
  return out + '</article>';
}
function deckArticle(H, b, i) {
  const n = i + 1;
  const tone = TONES[i % TONES.length];
  const hidden = i === 0 ? '' : ' hidden';
  const fr = (i % 2 === 1) ? ' face-right' : '';
  const face = H.slides[i % H.slides.length].face;
  let out = '<article class="intel-board letter-beat' + fr + '" data-beat="' + n + '" style="--tone:' + tone + '"' + hidden + '>'
    + '<div class="ib-blocktop"><img class="deal-beat-photo" src="' + face + '" alt="Naya speaking">'
    + '<div class="ib-identity"><span class="ib-jewel" aria-hidden="true">&#9670;</span><div>'
    + '<span class="ib-kind">' + esc(b.kind) + '</span><h2 class="ib-title">' + esc(b.title) + '</h2>'
    + '<p class="ib-subtitle">&ldquo;' + esc(b.sub) + '&rdquo;</p>'
    + '</div></div></div>' + nutshellHTML(b);
  if (b.type === 'img') {
    const p = picFor(H, b.pic);
    out += '<figure class="lb-showcase"><img src="' + p.src + '" alt="' + esc(p.alt) + '"></figure>';
  }
  out += '<div class="ib-foot"><img class="ib-foot-logo" src="' + H.deckLogo + '" alt="NayaNET"> &middot; NayaNET &middot; The Deck</div>'
    + '<button class="p3-enter letter-next deck-next" type="button" data-beat="' + n + '">Keep reading &#9670;</button>';
  return out + '</article>';
}
function letterArticle(H, b, i) {
  const n = i;
  const tc = TONE_CLASS[i % TONE_CLASS.length];
  const hidden = i === 0 ? '' : ' hidden';
  const lead = i === 0 ? ' lead' : '';
  const photo = H.bphotos[i % H.bphotos.length];
  let out = '<article class="intel-board ' + tc + ' letter-beat' + lead + '" data-beat="' + n + '" data-distilled' + hidden + '>'
    + '<div class="ib-blocktop"><img class="deal-beat-photo" src="' + photo + '" alt="Naya speaking">'
    + '<div class="ib-identity"><span class="ib-jewel" aria-hidden="true">&#9670;</span><div>'
    + '<span class="ib-kind">' + esc(b.kind) + '</span><h2 class="ib-title">' + esc(b.title) + '</h2>'
    + '</div></div></div>' + nutshellHTML(b);
  if (b.type === 'img') {
    const p = picFor(H, b.pic);
    out += '<figure class="lb-showcase"><img src="' + p.src + '" alt="' + esc(p.alt) + '"></figure>';
  }
  out += '<div class="ib-orb"><span class="ib-jewel" aria-hidden="true">&#9670;</span></div>'
    + '<div class="ib-foot"><img class="ib-foot-logo" src="/agmt-logo.jpg" alt="NayaNET"> &middot; The Collective Agreement</div>'
    + '<button class="p3-enter letter-next deck-next" type="button" data-beat="' + n + '">Keep reading &#9670;</button>';
  return out + '</article>';
}

/* ---- progress pill (unfold frame only) — the stage's jewel/number/bar, harvested in spirit ---- */
const PROG_CSS = `
/* DISTILL progress pill (2026-11-19) — the measuring thing, kept: a jewel set
   into the top of the frame, "N / 37" + bar, driven by .frame-now. Same
   language as the stage's fpStageJewel (jewel + number + bar). */
.af-prog{position:absolute;top:12px;left:50%;transform:translateX(-50%);z-index:3;display:flex;align-items:center;gap:8px;background:#050607;border:1.5px solid #d4a017;border-radius:999px;padding:6px 14px;pointer-events:none;box-shadow:0 4px 14px rgba(0,0,0,.6)}
.af-prog-jewel{color:#d4a017;font-size:17px}
.af-prog-num{color:#ffffff;font-size:17px;font-weight:700;white-space:nowrap}
.af-prog-bar{width:72px;height:6px;border-radius:999px;background:rgba(255,255,255,.18);overflow:hidden}
.af-prog-bar i{display:block;height:100%;background:#d4a017;width:3%;transition:width .3s ease}
@media (max-width:767px){.af-prog{top:8px;padding:4px 10px;gap:6px}.af-prog-bar{width:48px}}
`;
const PROG_JS = `
  /* DISTILL progress (2026-11-19) — the measuring thing, kept on the unfold:
     the pill reads .frame-now off #deckBody, so it follows every path
     (Keep reading, Next, Back, dots) without touching their handlers. */
  (function wireProgDistill(){
    var fr = document.querySelector('.naya-frame');
    var body = document.getElementById('deckBody');
    if (!fr || !body) return;
    var prog = document.createElement('div');
    prog.className = 'af-prog';
    prog.innerHTML = '<span class="af-prog-jewel" aria-hidden="true">&#9670;</span><span class="af-prog-num">1 / ' + document.querySelectorAll('#deckBody .letter-beat').length + '</span><span class="af-prog-bar"><i></i></span>';
    fr.appendChild(prog);
    function upd(){
      var beats = document.querySelectorAll('#deckBody .letter-beat');
      var cur = 0;
      for (var j = 0; j < beats.length; j++) if (beats[j].classList.contains('frame-now')) cur = j;
      var num = prog.querySelector('.af-prog-num');
      var bar = prog.querySelector('.af-prog-bar i');
      if (num) num.textContent = (cur + 1) + ' / ' + beats.length;
      if (bar) bar.style.width = Math.round(((cur + 1) / beats.length) * 100) + '%';
    }
    if (window.MutationObserver) new MutationObserver(upd).observe(body, { subtree: true, attributes: true, attributeFilter: ['class'] });
    upd();
  })();
`;

/* ---- unfold ---- */
function main() {
  const mode = process.argv[2] === '--emit' ? process.argv[3] : null;
  if (mode !== 'unfold' && mode !== 'welcome') fail('usage: transform-distill.js --emit unfold|welcome');
  // Sentence-count guard on the boards data itself (img 1-2, txt 3-5).
  let imgs = 0, txts = 0;
  BOARDS.forEach((b, i) => {
    const n = sentCount(b.lines);
    if (b.type === 'img') { imgs++; if (n < 1 || n > 2) fail('image board ' + (i + 1) + ' has ' + n + ' sentences'); }
    else { txts++; if (n < 3 || n > 5) fail('text board ' + (i + 1) + ' has ' + n + ' sentences'); }
    if (!b.kind || !b.title || !b.lines.length) fail('board ' + (i + 1) + ' missing kind/title/lines');
  });
  if (BOARDS.length !== 37 || imgs !== 27 || txts !== 10) fail('board split moved: ' + BOARDS.length + ' boards, ' + imgs + ' img, ' + txts + ' txt');
  const baseU = fs.readFileSync(UNFOLD_LOCAL, 'utf8');
  if (sha(Buffer.from(baseU, 'utf8')) !== UNFOLD_AF_SHA) fail('unfold base moved: ' + sha(Buffer.from(baseU, 'utf8')).slice(0, 12));
  const baseW = fs.readFileSync(WELCOME_LOCAL, 'utf8');
  if (sha(Buffer.from(baseW, 'utf8')) !== WELCOME_AF_SHA) fail('welcome base moved: ' + sha(Buffer.from(baseW, 'utf8')).slice(0, 12));
  const H = harvest(baseU, baseW);
  let out, label;
  if (mode === 'unfold') { out = buildUnfold(baseU, H); label = 'unfold'; }
  else { out = buildWelcome(baseW, H); label = 'welcome'; }
  noForbiddenMedia(out, label);
  noLongText(out, label);
  checkScripts(out, label);
  const buf = Buffer.from(out, 'utf8');
  console.log(label + ' ready: ' + buf.length + ' B sha ' + sha(buf).slice(0, 12));
  process.stdout.write(buf);
}

function buildUnfold(base, H) {
  // 24 articles -> 37 (whole article span swapped).
  const arts = [...base.matchAll(/<article[\s\S]*?<\/article>/g)].map(m => m[0]);
  if (arts.length !== 24) fail('unfold article count is not 24: ' + arts.length);
  const start = base.indexOf('<article');
  const end = base.lastIndexOf('</article>') + '</article>'.length;
  let text = base.slice(0, start) + BOARDS.map((b, i) => unfoldArticle(H, b, i)).join('\n') + base.slice(end);
  if ((text.match(/<article/g) || []).length !== 37) fail('unfold article count after is not 37');
  // deckAll goes (no "read the whole agreement" link).
  const dAll = /<button class="letter-all" id="deckAll"[^>]*>[\s\S]*?<\/button>/;
  if (!dAll.test(text)) fail('unfold deckAll button not found');
  text = text.replace(dAll, '');
  if (text.includes('id="deckAll"')) fail('unfold deckAll still present');
  // wireDeck guards: finish() + the read-it-all listener (all is now null).
  const finOld = "  function finish(){\n    all.hidden = true;\n  }";
  if (!text.includes(finOld)) fail('unfold wireDeck finish() not found');
  text = text.replace(finOld, "  function finish(){\n    if (all) all.hidden = true;\n  }");
  const allClicks = (text.match(/  all\.addEventListener\('click', function\(\)\{/g) || []).length;
  if (allClicks !== 1) fail('unfold bare all.addEventListener count is not 1: ' + allClicks);
  text = text.replace("  all.addEventListener('click', function(){", "  if (all) all.addEventListener('click', function(){");
  // headFor: board 1 is now a picture board — no more hardcoded board-0 title.
  const headOld = "  function headFor(b, i){\n    if (i === 0) return { kind: 'Naya \\u00b7 The Collective Agreement', title: 'Hi, I\\u2019m Naya' };";
  if (!text.includes(headOld)) fail('unfold headFor special-case not found');
  text = text.replace(headOld, "  function headFor(b, i){");
  // deck-sub: five questions -> pictures and words, a little at a time.
  const subOld = "Five questions. That&rsquo;s all this is. Naya talks you through it, one board at a time.";
  if (!text.includes(subOld)) fail('unfold deck-sub not found');
  text = text.replace(subOld, "Pictures and words, a little at a time &mdash; read them, or just tap through to agree.");
  // Progress pill: CSS into the fpFrameAF block, JS into the wireFrameAF IIFE.
  const cssAt = text.indexOf('id="fpFrameAF"');
  const cssEnd = text.indexOf('</style>', cssAt);
  if (cssAt < 0 || cssEnd < 0) fail('unfold fpFrameAF style block not found');
  text = text.slice(0, cssEnd) + PROG_CSS + text.slice(cssEnd);
  const jsOld = "  style();\n  window.addEventListener('resize', style);\n})();";
  if (!text.includes(jsOld)) fail('unfold wireFrameAF tail not found');
  text = text.replace(jsOld, "  style();\n  window.addEventListener('resize', style);\n" + PROG_JS + "})();");
  // Content guards.
  for (const n of ['dealAgreeBtn', 'dealSeal', 'I agree — show me my world', 'wireDeck', 'wireFrame7', 'wireFrame8', 'wireFrame9', 'fpMediaFrame', 'af-prog', 'wireProgDistill'])
    if (!text.includes(n)) fail('unfold content lost: ' + n);
  // BUTTON DESTINATIONS (Shawn 20:14 MST, standing order): every button
  // lands on the right page. Boards 1-36 carry Keep reading; board 37
  // carries I-agree -> bridge. A lost destination fails the build.
  const krCount = (text.match(/class="p3-enter letter-next deck-next"[^>]*data-beat="[0-9]+"/g) || []).length;
  if (krCount !== 36) fail('unfold Keep-reading count is not 36: ' + krCount);
  for (const n of ['/?stage=bridge', 'fpAudioState', 'fpAnthemVideoBtn', 'fpAudioNote', 'fpAnthemNote'])
    if (!text.includes(n)) fail('unfold destination lost: ' + n);
  if (text.includes('Read the full agreement')) fail('unfold full-agreement label present');
  return text;
}

function buildWelcome(base, H) {
  let text = base;
  // Deck: the 9 consecutive articles after #deckBody -> 37.
  const di = text.indexOf('id="deckBody"');
  if (di < 0) fail('welcome deckBody not found');
  const deckMs = [...text.slice(di).matchAll(/<article[\s\S]*?<\/article>/g)].slice(0, 9);
  if (deckMs.length !== 9) fail('welcome deck article count is not 9');
  const dStart = di + deckMs[0].index;
  const dEnd = di + deckMs[8].index + deckMs[8][0].length;
  const gap = text.slice(dStart, dEnd);
  if ((gap.match(/<article/g) || []).length !== 9) fail('welcome deck span miscount');
  text = text.slice(0, dStart) + BOARDS.map((b, i) => deckArticle(H, b, i)).join('') + text.slice(dEnd);
  // Letter: all 34 data-distilled articles -> 37 (extra boards appended after the last slot).
  const parts = text.split(/(<article[^>]*data-distilled[^>]*>[\s\S]*?<\/article>)/g);
  const idxs = [];
  parts.forEach((p, i) => { if (p.startsWith('<article') && p.includes('data-distilled')) idxs.push(i); });
  if (idxs.length !== 34) fail('welcome distilled count is not 34: ' + idxs.length);
  const newL = BOARDS.map((b, i) => letterArticle(H, b, i));
  idxs.forEach((pi, k) => { parts[pi] = k < 37 ? newL[k] : ''; });
  if (newL.length > idxs.length) parts[idxs[idxs.length - 1]] += newL.slice(idxs.length).join('');
  text = parts.join('');
  if ((text.match(/<article[^>]*data-distilled[^>]*>/g) || []).length !== 37) fail('welcome distilled count after is not 37');
  if ((text.match(/<article/g) || []).length < 37) fail('welcome article count moved');
  // letterAll + fpLinkLetterAll go (no "read the whole letter" link).
  const lAll = /<button class="letter-all" id="letterAll"[^>]*>[\s\S]*?<\/button>/;
  if (!lAll.test(text)) fail('welcome letterAll button not found');
  text = text.replace(lAll, '');
  const fLink = /<button[^>]*id="fpLinkLetterAll"[^>]*>[\s\S]*?<\/button>/;
  if (!fLink.test(text)) fail('welcome fpLinkLetterAll button not found');
  text = text.replace(fLink, '');
  if (text.includes('id="letterAll"') || text.includes('id="fpLinkLetterAll"')) fail('welcome read-it-all buttons still present');
  // dealEyeMain is the other plain-letter opener (eye button, aria-label
  // "Read the whole letter at once") — it goes with the dialog.
  const eyeRe = /<button[^>]*id="dealEyeMain"[^>]*>[\s\S]*?<\/button>/;
  if (!eyeRe.test(text)) fail('welcome dealEyeMain button not found');
  text = text.replace(eyeRe, '');
  const eyeJs = /document\.getElementById\('dealEyeMain'\)\.addEventListener\('click', function\(\)\{\s*openPlainLetter\(\);\s*\}\);/;
  if (!eyeJs.test(text)) fail('welcome dealEyeMain listener not found');
  text = text.replace(eyeJs, "var _dealEye = document.getElementById('dealEyeMain'); if (_dealEye) _dealEye.addEventListener('click', function(){ openPlainLetter(); });");
  if (text.includes('id="dealEyeMain"')) fail('welcome dealEyeMain still present');
  // Guide prose: "you read the whole letter" -> the boards, not the letter.
  // (It lives inside a distilled article's eye note, so the article swap
  // usually removes it already; replace it if it survives anywhere else.)
  text = text.replace('you read the whole letter, then you tap', 'you tap through the boards, then you tap');
  // wireLetter guard: the read-it-all listener (all is now null).
  const wAll = "  all.addEventListener('click', function(){ openPlainLetter(); });";
  if (!text.includes(wAll)) fail('welcome wireLetter all-listener not found');
  text = text.replace(wAll, "  if (all) all.addEventListener('click', function(){ openPlainLetter(); });");
  // dealPlain dialog goes (div-depth counted removal; its JS refs are all null-guarded).
  const dpStart = text.indexOf('<div class="deal-plain" id="dealPlain"');
  if (dpStart < 0) fail('welcome dealPlain dialog not found');
  let depth = 0, pos = dpStart, dpEnd = -1;
  const tagRe = /<\/?div\b[^>]*>/g;
  tagRe.lastIndex = dpStart;
  let m;
  while ((m = tagRe.exec(text)) !== null) {
    if (m[0].startsWith('</')) { depth--; if (depth === 0) { dpEnd = m.index + m[0].length; break; } }
    else depth++;
    if (m.index > dpStart + 20000) fail('welcome dealPlain removal ran away');
  }
  if (dpEnd < 0) fail('welcome dealPlain close not found');
  text = text.slice(0, dpStart) + text.slice(dpEnd);
  if (text.includes('id="dealPlain"')) fail('welcome dealPlain still present');
  // DECK PROGRESS (distill fix, 2026-11-19): the 9-dot strip saturates at
  // board 9 of 37, so the deck shows the count-agnostic jewel (N / 37 +
  // bar), same as the letter — one measuring thing per view, never two.
  const deckProgOld = "      dotsEl.classList.add('fp-on');\n      qa('.fp-dot',dotsEl).forEach(function(d,i){d.classList.toggle('on',i<=S.deck);});";
  if (!text.includes(deckProgOld)) fail('welcome deck dots block not found');
  text = text.replace(deckProgOld, "      jewelEl.classList.add('fp-on');\n      jewelNum.textContent=(S.deck+1)+' / '+deckBeats.length;\n      jewelBar.style.width=Math.round(((S.deck+1)/deckBeats.length)*100)+'%';\n      jewelEl.style.setProperty('--tone',tone);");
  if (text.includes(deckProgOld)) fail('welcome deck dots block still present');
  if (!text.includes("jewelNum.textContent=(S.deck+1)+' / '+deckBeats.length")) fail('welcome deck jewel not wired');
  // Deck-end button says "Read the full agreement" — the one "full/whole"
  // label left, and it goes to the same distilled unfold as the intro
  // button. Same destination, same words.
  const fullOld = "nextBtn2.textContent='Read the full agreement \\u25C6';";
  if (!text.includes(fullOld)) fail('welcome deck-end full-agreement label not found');
  text = text.replace(fullOld, "nextBtn2.textContent='Read the Collective Agreement \\u25C6';");
  // Stale hardcoded jewel text (86 was the old letter count).
  const jewelOld = 'id="fpStageJewelNum">1 / 86</span>';
  if (!text.includes(jewelOld)) fail('welcome stale jewel count not found');
  text = text.replace(jewelOld, 'id="fpStageJewelNum">1 / 37</span>');
  // Content guards.
  for (const n of ['fpChoiceDeck', 'fpChoiceLetter', 'enterStage', 'deckBeats', 'dealAgreeBtn', 'dealSeal', 'fpStageJewelNum'])
    if (!text.includes(n)) fail('welcome content lost: ' + n);
  // BUTTON DESTINATIONS (Shawn 20:14 MST, standing order): every button
  // lands on the right page. The three "read" buttons go to /agreement;
  // the stage's agree path is agreeFromLetterPage -> agree view -> the
  // real agree button; exits land on the login; Back lands on the bridge.
  for (const n of ["window.location.href='/agreement'", 'goBridgeAfterAgree', 'agreeFromLetterPage', 'exitStage', 'goResume', 'goBridgeToName', 'enterLetterPage'])
    if (!text.includes(n)) fail('welcome destination lost: ' + n);
  if ((text.match(/window\.location\.href='\/agreement'/g) || []).length < 3) fail('welcome /agreement destinations are not 3 (nextBtn2, choice, bridge)');
  if (text.includes('Read the full agreement')) fail('welcome full-agreement label present');
  return text;
}

main();
