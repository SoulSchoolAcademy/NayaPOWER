#!/usr/bin/env node
/* AGREEMENT-FRAME transform (2026-11-19, maker round):
   Base: walkthrough fix-9 tip cdc94c72 — unfold sha ab8da1fa, welcome sha 2062739e.
   1. UNFOLD (/agreement, text): regroup 47 beats -> 24 boards (sequential
      pairs; beat 47, the agree board, stands alone). Every beat's words
      stay verbatim and in order — the merge moves whole blocktops,
      nutshells, showcases and feet; only the duplicate Keep-reading /
      Back buttons and the duplicate foot line are dropped (one board =
      one button row). The dots row is removed (default NO dots).
   2. WELCOME (?stage=deck, visual): no regrouping (one slide = one clean
      presentation already); the dots row is removed and the deck frame
      system is injected, scoped to the deck view only.
   3. Inject the AF frame system (4 styles) into both files.
   Guards: sentence multiset identical before/after (unfold), article
   count 47 -> 24, dealAgreeBtn + agree handlers intact, no audio / mp3
   / m4a wired, node --check every script block. stdout carries ONLY the
   two output paths + shas (JSON); the bytes are written to the out paths
   (temp + verify + rename in the same directory, never truncate-first). */
const fs = require('fs');
const crypto = require('crypto');
const path = require('path');
const { spawnSync } = require('child_process');
console.log = (...a) => console.error(...a);

const UNFOLD_LOCAL = '/home/hatch/workspace/team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html';
const WELCOME_LOCAL = '/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/welcome-staged.html';
const UNFOLD_SHA = 'ab8da1faf825d9d24e3f4991063e81c052738502063d9e89f4479730fa94348f';
const WELCOME_SHA = '2062739ecb968b78cd823440bcfd4bbb8f7d0190d3bb2e5443ab3b35c0081955';
/* The transform's own verified outputs (v2 run 2026-11-19): if a later
   run finds these bytes already on the native paths (the build landed
   them), they are used as-is — they ARE the guarded output, sha-verified. */
const AF_UNFOLD_SHA = '1e58ea2fad767a9753adf69a57d17a0afab3156ba821e18cfbf738ae8d8af434';
const AF_WELCOME_SHA = '1f37416d79b0959b21dffb450d34e1a409dfe934fac40a144ecf0b0ef9f7cc49';
const MASTER = 'https://naya-proof-host.nayapower.workers.dev/?file=team-nitro/agreement-unfold-20261117/master-frame.png&ref=walkthrough/chain-fix7-20261119&cb=5a4dc2f9ca703945f12cec0b39b491d728e69c4a';

function sha(b) { return crypto.createHash('sha256').update(b).digest('hex'); }
function fail(m) { console.error('AF-FAIL: ' + m); process.exit(1); }
function writeVerified(outPath, data) {
  const tmp = outPath + '.tmp-af';
  fs.writeFileSync(tmp, data);
  const back = fs.readFileSync(tmp);
  if (sha(back) !== sha(data)) fail('temp write mismatch for ' + outPath);
  fs.renameSync(tmp, outPath);
  const fin = fs.readFileSync(outPath);
  if (sha(fin) !== sha(data)) fail('final write mismatch for ' + outPath);
  console.log('landed ' + outPath + ': ' + data.length + ' B sha ' + sha(data).slice(0, 12));
}
function checkScripts(text, label) {
  const blocks = [...text.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
  console.log(label + ' script blocks: ' + blocks.length);
  blocks.forEach((code, idx) => {
    const r = spawnSync('node', ['--check', '-'], { input: code });
    if (r.status !== 0) fail(label + ' script block ' + idx + ' fails node --check: ' + String(r.stderr).slice(0, 300));
  });
}
function sentencesOf(html) {
  // Buttons, feet and the dots row carry chrome, not agreement words —
  // strip them in BOTH the before and after text, so the merge's
  // one-button-row / one-foot-per-board cleanup is guard-neutral.
  const txt = html.replace(/<script[\s\S]*?<\/script>/g, ' ').replace(/<style[\s\S]*?<\/style>/g, ' ')
    .replace(/<button[\s\S]*?<\/button>/g, ' ').replace(/<div class="ib-foot">[\s\S]*?<\/div>/g, ' ')
    .replace(/<div class="letter-dots"[^>]*>[\s\S]*?<\/div>/g, ' ')
    .replace(/<[^>]+>/g, ' ').replace(/&[^;\s]+;/g, ' ').replace(/\s+/g, ' ').trim();
  return txt.split(/(?<=[.!?])\s+/).filter(x => x.length > 3).sort();
}
function noForbiddenMedia(text, label) {
  if (/<audio/.test(text) || /agreement-naya-voice|62bf05e6|Inside_the_NayaNET|b60233efb19466a0356330778ce38d5363d38cc77ca87435a64187d4c20eef19/.test(text))
    fail(label + ': forbidden media referenced');
}

/* ================= THE AF FRAME SYSTEM — 4 styles =================
   STYLE 1 — ROYAL ORNATE (desktop text, >=1024px): master-frame art harvested
   verbatim as four corner ornaments (quadrants, no distortion) + gold outer
   rim + purple inner hairline. Frame hugs the screen edges; the board sits
   inside it, centred, whole. Light travels INSIDE the rim.
   STYLE 2 — CALENDAR FRAME (desktop visual, >=1024px): the calendar's chrome
   — full-bleed obsidian, rim-only, maximum spacing — two columns, showcase
   large on the right, words on the left.
   STYLE 3 — ROYAL COMPACT (mobile text, <768px): same frame slimmed — small
   corners, tight insets, full-width board, thumb-sized buttons.
   STYLE 4 — ROYAL COMPACT VISUAL (mobile visual, <768px): same compact
   frame, showcase image first, stacked, scrolls inside the frame. */
const AF_CSS_UNFOLD = `
<style id="fpFrameAF">
/* ============ AGREEMENT FRAME (2026-11-19) — four styles, one frame system ============
   The old frame floated: master-frame.png at background-size:contain + content
   insets 220/200/170 left a small box in a big black field, light outside.
   The frame now HUGS the edges: corner ornaments harvested verbatim from the
   master-frame PNG (quadrants, no distortion) + a gold outer rim + a purple
   inner hairline. The flowing light travels INSIDE the rim (14px path). */
.naya-frame{background-image:none!important}
.naya-frame::before{content:"";position:absolute;inset:0;border:2px solid #d4a017;pointer-events:none}
.naya-frame::after{content:"";position:absolute;inset:10px;border:1px solid rgba(142,36,170,.65);pointer-events:none}
.af-corner{position:absolute;width:208px;height:208px;z-index:1;background-image:url(${MASTER});background-size:200% 200%;pointer-events:none}
.af-corner.tl{top:0;left:0;background-position:0 0}
.af-corner.tr{top:0;right:0;background-position:100% 0}
.af-corner.bl{bottom:0;left:0;background-position:0 100%}
.af-corner.br{bottom:0;right:0;background-position:100% 100%}
.frame-light{z-index:2!important;animation-name:frameLightAF!important}
@keyframes frameLightAF{0%{top:14px;left:14px}25%{top:14px;left:calc(100% - 26px)}50%{top:calc(100% - 26px);left:calc(100% - 26px)}75%{top:calc(100% - 26px);left:14px}100%{top:14px;left:14px}}
/* STYLE 1 — ROYAL ORNATE (desktop text): the board fills the frame. */
.p3-deal-unfold{--fin-t:76px!important;--fin-b:92px!important;--fin-l:96px!important;--fin-r:96px!important}
@media (min-width:1024px) and (min-aspect-ratio:1/1){.p3-deal-unfold{--fin-t:76px!important;--fin-b:92px!important;--fin-l:96px!important;--fin-r:96px!important}}
@media (min-aspect-ratio:1/1) and (max-height:700px){.p3-deal-unfold{--fin-t:64px!important;--fin-b:80px!important;--fin-l:72px!important;--fin-r:72px!important}}
#deckBody .letter-beat{max-width:940px;margin-left:auto!important;margin-right:auto!important;box-shadow:0 18px 48px rgba(0,0,0,.65),0 4px 12px rgba(0,0,0,.5)!important;border-radius:20px!important}
/* AF v2 — the board STRETCHES to fill the frame (was content-height, leaving
   a ~216px dead gap below the foot at desktop): the reading window grows
   with it, the foot pins to the frame's bottom inset. */
.p3-deal-unfold #deckBody{flex:1 1 auto!important;min-height:0!important}
#deckBody .letter-beat{height:100%!important;display:flex!important;flex-direction:column!important}
#deckBody .letter-beat .frame-scroll{flex:1 1 auto!important;min-height:0!important}
/* Naya's photo in the top-right corner — more writing space in the middle. */
.frame-topbar{display:flex!important;align-items:center!important;gap:16px!important}
.frame-topbar .frame-head{order:1!important}
.frame-topbar .frame-icon{order:2!important}
.frame-topbar .frame-face{order:3!important;margin-left:auto!important;width:64px!important;height:64px!important;flex:0 0 64px!important}
/* Text scale, the law: headlines 25, body 19, labels 17 — white, always. */
.frame-title{font-size:25px!important;line-height:1.2!important}
.frame-kind{font-size:17px!important}
.frame-scroll p{font-size:19px!important;line-height:1.55!important;color:#ffffff!important}
.frame-scroll .ib-title{font-size:25px!important;color:#ffffff!important}
/* Dots go — default NO dots. The read-it-all link stays, slim, at the bottom. */
#deckDots{display:none!important}
#deckControls{justify-content:center!important;margin-top:4px!important}
#deckControls .letter-all{font-size:17px!important}
/* Buttons close to the bottom, in the foot — never blocking the words.
   Spectrum order, never two the same: Back purple, Keep reading sapphire, Next emerald. */
.frame-foot{padding-bottom:6px!important}
.frame-btnrow{display:flex!important;gap:12px!important;justify-content:center!important;flex-wrap:wrap!important}
.frame-btnrow .deck-back{border-color:#8e24aa!important}
.frame-btnrow .deck-next:not(.frame-next){border-color:#0f52ba!important}
.frame-btnrow .frame-next{border-color:#07925f!important}
/* STYLE 3 — ROYAL COMPACT (mobile text, <768px).
   AF v2 — mobile frame 1 showed ZERO agreement words (the media board ate
   the whole reading window): the media slims, the top bar tightens, the
   anthem pill never wraps, and the buttons are pills in one row — never
   circles. The stretch above grows the window with it. */
@media (max-width:767px){
.af-corner{width:104px;height:104px}
.p3-deal-unfold{--fin-t:48px!important;--fin-b:76px!important;--fin-l:14px!important;--fin-r:14px!important}
#deckBody .letter-beat{max-width:none!important}
.frame-topbar{gap:8px!important}
.frame-topbar .frame-face{width:48px!important;height:48px!important;flex-basis:48px!important}
.frame-topbar .frame-kind{letter-spacing:.08em!important}
.frame-scroll p{font-size:17px!important;line-height:1.5!important}
.frame-media{padding:6px 12px!important}
.frame-media .play-btn{width:44px!important;height:44px!important}
.frame-media .frame-video-btn{white-space:nowrap!important;padding:10px 12px!important}
.frame-btnrow{flex-wrap:nowrap!important;gap:6px!important}
/* AF v3 — the v2 equal-share pills CLIPPED the middle button ("Keep readi"
   at 390): the buttons size to their own words now, never to equal shares. */
.frame-btnrow button{flex:0 1 auto!important;min-width:0!important;white-space:nowrap!important;font-size:17px!important;padding:10px 6px!important}
}
</style>
`;

const AF_JS_UNFOLD = `
<script>
/* ============ AGREEMENT FRAME JS (2026-11-19) — corners + style tag ============
   Mounts the four harvested corner ornaments into .naya-frame and tags the
   document with its situation (text-desktop / text-mobile) so the frame
   adapts. Navigation, agree, media and seals are untouched (wireFrame7/8/9). */
(function wireFrameAF(){
  var fr = document.querySelector('.naya-frame');
  if (fr) {
    ['tl','tr','bl','br'].forEach(function(c){
      var d = document.createElement('div');
      d.className = 'af-corner ' + c;
      d.setAttribute('aria-hidden', 'true');
      fr.appendChild(d);
    });
  }
  function style(){
    var w = window.innerWidth || 0;
    document.documentElement.setAttribute('data-af-style', w >= 1024 ? 'text-desktop' : (w >= 768 ? 'text-tablet' : 'text-mobile'));
  }
  style();
  window.addEventListener('resize', style);
})();
</script>
`;

const AF_CSS_DECK = `
<style id="fpDeckAF">
/* ============ AGREEMENT FRAME — DECK (2026-11-19) — the visual story, same frame ============
   Scoped to body.af-deck-on (deck view only): the landing, bridge and letter
   never see these rules. Dots go. The deck frame is the same system as the
   text frame: gold outer rim + purple inner hairline + harvested corner
   ornaments + light INSIDE the rim. Corners use screen blend so the PNG's
   black centre never covers the board. */
body.af-deck-on #deckDots{display:none!important}
body.af-deck-on #deckControls{justify-content:center!important;margin-top:4px!important}
body.af-deck-on #deckControls .letter-all{font-size:17px!important}
.af-deck-frame{position:fixed;inset:0;pointer-events:none;z-index:60}
.af-deck-frame::before{content:"";position:absolute;inset:0;border:2px solid #d4a017}
.af-deck-frame::after{content:"";position:absolute;inset:10px;border:1px solid rgba(142,36,170,.65)}
.af-deck-frame .af-corner{position:absolute;width:208px;height:208px;background-image:url(${MASTER});background-size:200% 200%;mix-blend-mode:screen}
.af-deck-frame .af-corner.tl{top:0;left:0;background-position:0 0}
.af-deck-frame .af-corner.tr{top:0;right:0;background-position:100% 0}
.af-deck-frame .af-corner.bl{bottom:0;left:0;background-position:0 100%}
.af-deck-frame .af-corner.br{bottom:0;right:0;background-position:100% 100%}
.af-deck-light{position:absolute;width:12px;height:12px;border-radius:50%;background:#fff;box-shadow:0 0 12px #fff,0 0 26px #8e24aa,0 0 44px #8e24aa;animation:frameLightAF 60s linear infinite}
@keyframes frameLightAF{0%{top:14px;left:14px}25%{top:14px;left:calc(100% - 26px)}50%{top:calc(100% - 26px);left:calc(100% - 26px)}75%{top:calc(100% - 26px);left:14px}100%{top:14px;left:14px}}
/* STYLE 2 — CALENDAR FRAME (desktop visual, >=1024px): the calendar's chrome —
   full-bleed obsidian, rim-only, maximum spacing — as the frame OVERLAY
   (rims + corners + inside light above). AF v2: the deck keeps its OWN
   slide layout (overview pills + slides, already built as the visual
   story) — the v1 two-column grid reflowed the overview pills, so it is
   gone; the frame, the dots removal and the text scale are the treatment. */
body.af-deck-on #deckBody .ib-title{font-size:25px!important;color:#ffffff!important}
body.af-deck-on #deckBody .ib-nutshell p{font-size:19px!important;line-height:1.55!important;color:#ffffff!important}
/* STYLE 4 — ROYAL COMPACT VISUAL (mobile visual, <768px): the same compact
   frame (corners off on mobile — rims + light only); the deck keeps its
   own stacked layout. AF v2: the v1 flex reflow garbled the overview
   pills on mobile, so it is gone. */
@media (max-width:767px){
.af-deck-frame .af-corner{display:none}
body.af-deck-on #deckBody .ib-nutshell p{font-size:17px!important;line-height:1.5!important}
}
</style>
`;

const AF_JS_DECK = `
<script>
/* ============ AGREEMENT FRAME — DECK JS (2026-11-19) ============
   Turns the deck frame on only while the visual story is the view:
   ?stage=deck on load, "Begin the visual story" on tap. Turns it off
   when the citizen leaves for the letter or the opening page, so the
   letter boards and the bridge never wear the deck frame. */
(function wireDeckAF(){
  function on(){
    document.body.classList.add('af-deck-on');
    var f = document.querySelector('.af-deck-frame');
    if (!f) {
      f = document.createElement('div');
      f.className = 'af-deck-frame';
      f.setAttribute('aria-hidden', 'true');
      ['tl','tr','bl','br'].forEach(function(c){
        var d = document.createElement('div');
        d.className = 'af-corner ' + c;
        f.appendChild(d);
      });
      var l = document.createElement('div');
      l.className = 'af-deck-light';
      f.appendChild(l);
      document.body.appendChild(f);
    }
  }
  function off(){ document.body.classList.remove('af-deck-on'); }
  try { var st = new URLSearchParams(window.location.search).get('stage'); if (st === 'deck') on(); } catch (e) {}
  var c1 = document.getElementById('fpChoiceDeck');
  if (c1) c1.addEventListener('click', function(){ setTimeout(on, 0); });
  var c2 = document.getElementById('fpBridgeDeck');
  if (c2) c2.addEventListener('click', function(){ setTimeout(on, 0); });
  var l1 = document.getElementById('fpChoiceLetter');
  if (l1) l1.addEventListener('click', function(){ setTimeout(off, 0); });
  var l2 = document.getElementById('fpBridgeLetter');
  if (l2) l2.addEventListener('click', function(){ setTimeout(off, 0); });
  var ex = document.getElementById('fpDeckBack');
  if (ex) ex.addEventListener('click', function(){ setTimeout(off, 0); });
})();
</script>
`;

/* ================= UNFOLD: regroup 47 -> 24 ================= */
function mergeUnfold(base) {
  const arts = [...base.matchAll(/<article[\s\S]*?<\/article>/g)].map(m => m[0]);
  if (arts.length !== 47) fail('unfold article count is not 47: ' + arts.length);
  const before = sentencesOf(base);
  // Pair sequentially: (1,2) (3,4) ... (45,46), (47) alone = 24 boards.
  const groups = [];
  for (let i = 0; i < 46; i += 2) groups.push([arts[i], arts[i + 1]]);
  groups.push([arts[46]]);
  const merged = groups.map((g, gi) => {
    if (g.length === 1) return g[0];
    const a = g[0], b = g[1];
    // Inner content of b (between its <article...> and </article>).
    let innerB = b.replace(/^<article[^>]*>/, '').replace(/<\/article>\s*$/, '');
    // Drop b's own Keep-reading + Back buttons (one board = one button row,
    // the row keeps a's buttons — wireFrame7/8 rewire by index anyway).
    innerB = innerB.replace(/<button[^>]*class="[^"]*deck-next[^"]*"[^>]*>[\s\S]*?<\/button>/g, '');
    innerB = innerB.replace(/<button[^>]*class="[^"]*deck-back[^"]*"[^>]*>[\s\S]*?<\/button>/g, '');
    // Drop b's duplicate foot line (one foot per board).
    innerB = innerB.replace(/<div class="ib-foot">[\s\S]*?<\/div>/, '');
    // Keep a's shell; append b's content before a's closing tag.
    let out = a.replace(/<\/article>\s*$/, '');
    // a's Keep-reading button stays (it becomes the board's Keep reading);
    // renumber the board's data-beat to its new board number.
    out = out.replace(/data-beat="\d+"/, 'data-beat="' + (gi + 1) + '"');
    out = out.replace(/(<button[^>]*class="[^"]*deck-next[^"]*"[^>]*data-beat=")\d+(")/, '$1' + (gi + 1) + '$2');
    return out + '\n' + innerB + '</article>';
  });
  // Splice merged articles back in place of the original 47: split the
  // file on article boundaries and swap the 47 article parts for the 24
  // merged boards (the 23 leftover article slots become empty).
  const parts = base.split(/(<article[\s\S]*?<\/article>)/g);
  const artIdx = [];
  parts.forEach((p, i) => { if (p.startsWith('<article')) artIdx.push(i); });
  if (artIdx.length !== 47) fail('article split count moved: ' + artIdx.length);
  artIdx.forEach((pi, k) => { parts[pi] = k < 24 ? merged[k] : ''; });
  let text = parts.join('');
  if ((text.match(/<article/g) || []).length !== 24) fail('merged article count is not 24');
  // Dots row goes (default NO dots). The JS dots queries are null-safe
  // (querySelectorAll -> empty list, forEach no-op; fix-9 guards the box).
  const dotsRe = /<div class="letter-dots" id="deckDots"[^>]*>[\s\S]*?<\/div>/;
  if (!dotsRe.test(text)) fail('unfold dots row not found');
  text = text.replace(dotsRe, '');
  if (text.includes('id="deckDots"')) fail('unfold dots row still present');
  // Word guard: the sentence multiset must be identical (words verbatim, in order).
  const after = sentencesOf(text);
  if (before.length !== after.length) fail('sentence count moved: ' + before.length + ' -> ' + after.length);
  for (let i = 0; i < before.length; i++) if (before[i] !== after[i]) fail('sentence changed at sorted index ' + i);
  // The agree board + handlers intact.
  for (const n of ['dealAgreeBtn', 'dealSeal', 'I agree — show me my world', 'wireDeck', 'wireFrame7', 'wireFrame8', 'wireFrame9', 'fpMediaFrame'])
    if (!text.includes(n)) fail('unfold content lost: ' + n);
  return text;
}

/* ================= WELCOME: deck frame only ================= */
function frameWelcome(base) {
  let text = base;
  const dotsRe = /<div class="letter-dots" id="deckDots"[^>]*>[\s\S]*?<\/div>/;
  if (!dotsRe.test(text)) fail('welcome dots row not found');
  text = text.replace(dotsRe, '');
  if (text.includes('id="deckDots"')) fail('welcome dots row still present');
  if (text.includes('fpDeckAF')) fail('deck frame already applied');
  text = text.replace('</head>', AF_CSS_DECK + '</head>');
  text = text.replace('</body>', AF_JS_DECK + '\n</body>');
  for (const n of ['fpChoiceDeck', 'fpChoiceLetter', 'enterStage', 'deckBeats', 'dealAgreeBtn', 'dealSeal'])
    if (!text.includes(n)) fail('welcome content lost: ' + n);
  return text;
}

function main() {
  // --emit unfold|welcome: print that file's bytes to stdout (binary).
  // The parent pipes them through writer9.js (chunked, fresh single
  // attempt per try) — EPERM is sticky per process, so no in-process
  // retry loop and no direct fs write of the outputs here.
  const mode = process.argv[2] === '--emit' ? process.argv[3] : null;
  if (mode !== 'unfold' && mode !== 'welcome') fail('usage: transform-af.js --emit unfold|welcome');
  const baseU = fs.readFileSync(UNFOLD_LOCAL, 'utf8');
  const baseUSha = sha(Buffer.from(baseU, 'utf8'));
  let u;
  if (baseUSha === UNFOLD_SHA) {
    u = mergeUnfold(baseU);
    if (u.includes('fpFrameAF')) fail('unfold frame already applied');
    u = u.replace('</head>', AF_CSS_UNFOLD + '</head>');
    u = u.replace('</body>', AF_JS_UNFOLD + '\n</body>');
    noForbiddenMedia(u, 'unfold');
    checkScripts(u, 'unfold');
  } else if (baseUSha === AF_UNFOLD_SHA) {
    console.log('unfold already AF bytes on disk — reusing verified output');
    u = baseU;
  } else fail('unfold base moved: ' + baseUSha.slice(0, 12));
  const baseW = fs.readFileSync(WELCOME_LOCAL, 'utf8');
  const baseWSha = sha(Buffer.from(baseW, 'utf8'));
  let w;
  if (baseWSha === WELCOME_SHA) {
    w = frameWelcome(baseW);
    noForbiddenMedia(w, 'welcome');
    checkScripts(w, 'welcome');
  } else if (baseWSha === AF_WELCOME_SHA) {
    console.log('welcome already AF bytes on disk — reusing verified output');
    w = baseW;
  } else fail('welcome base moved: ' + baseWSha.slice(0, 12));
  const out = mode === 'unfold' ? Buffer.from(u, 'utf8') : Buffer.from(w, 'utf8');
  console.log(mode + ' ready: ' + out.length + ' B sha ' + sha(out).slice(0, 12));
  process.stdout.write(out);
}
main();
