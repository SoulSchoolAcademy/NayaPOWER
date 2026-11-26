// Portal front-page fix ROUND 3 — the agreement-entry round (Shawn's rulings,
// voice calls 2026-11-25 ~17:32-17:39 MST). Base: the PROVEN round-2 staged
// portal (sha 66664c07...). Do not redo F1/F2.
//   1. The ⓘ in the front-page circle is REPLACED by a beautiful red ACTIVE N
//      (the harvested ball, same bytes as the corner; spins eco-spin 90s).
//   2. EVERY N (circle, black bottom-left, red bottom-right) + "Read the
//      agreement" open the REAL agreement — the visual story — IN PLACE,
//      directly at slide 1 ("The Old Way"). No landing, no Terms overlay,
//      no pop-up below. The old 13-paragraph pop-up reader GOES.
//   3. End slide ("Your Franchise") per his eye: no agree button mid-slide;
//      agree at the very bottom just above the < > arrows, flashing; the eight
//      links in a bar across the bottom; the franchise text box back on the
//      slide; agree returns to the name box. Official button wording
//      "I agree — show me my world ◆" (v7 words source) — FLAGGED: the live
//      end slide reads just "I agree ◆".
//   4. Pictures untouched (his update, he provides them).
// Harvest: SLIDES (27) + EMBED.slides (27 JPEGs) + FP_FINAL (8 answers) +
// PORTRAITS (16) extracted from the live agreement bytes below — never
// rewritten, never typed from memory. Node only (python writes EPERM).
import {readFileSync, writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const sha = b => createHash('sha256').update(b).digest('hex');
const LANE = new URL('./', import.meta.url).pathname;
const R2 = LANE + 'portal-r2.html';
const AGMT = LANE + 'evidence/agreement-live-r3.html';

// --- 0. Base identity: the R2 staged bytes exactly. ---
const base = readFileSync(R2);
const baseSha = sha(base);
if (baseSha !== '66664c07a1b4ae3b73f69af318a405a29d1848589d535424917f8229e0e49ead')
  throw new Error('R2 base sha mismatch: ' + baseSha);
const baseStr = base.toString('utf8');

// --- 0b. Live agreement identity + reconciliation. ---
// Brief's "fresh" figure (18,530,304 B, sha 6527cde7…) does NOT match this
// fetch: the live page returns 22,953,906 B, sha 2c88513f… — byte-identical
// to round 1 / round 2 v25. The 18.5 MB figure is unreconciled; harvest is
// from the bytes actually fetched here.
const agmt = readFileSync(AGMT);
const agmtSha = sha(agmt);
if (agmtSha !== '2c88513f9011b176c0af910ec0d81e314578cfe904dd62ded9010a9a54052e11')
  throw new Error('agreement-live sha mismatch: ' + agmtSha + ' bytes=' + agmt.length);
const agmtStr = agmt.toString('utf8');
if (agmt.length !== 22953906) throw new Error('agreement-live bytes mismatch: ' + agmt.length);

// --- 0c. Extract SLIDES (27), EMBED.slides (27), FP_FINAL (8), PORTRAITS. ---
function extractSlides(s) {
  const start = s.indexOf('var SLIDES = [');
  if (start === -1) throw new Error('SLIDES anchor not found');
  const end = s.indexOf('\n];', start);
  if (end === -1) throw new Error('SLIDES end not found');
  const arrText = s.slice(s.indexOf('[', start), end + 2); // include the closing ]
  // JS literal, not JSON (unquoted t/x/a keys) — evaluate the literal.
  return (new Function('return (' + arrText + ')'))();
}
function extractSlideImgs(s) {
  const start = s.indexOf('slides: ["data:image');
  if (start === -1) throw new Error('EMBED.slides anchor not found');
  const out = [];
  let pos = start;
  for (let i = 0; i < 27; i++) {
    const q = s.indexOf('"data:image', pos);
    if (q === -1) throw new Error('slide img ' + i + ' not found');
    const e = s.indexOf('"', q + 1);
    out.push(s.slice(q + 1, e));
    pos = e + 1;
  }
  return out;
}
function extractFinal(s) {
  const start = s.indexOf('FP_FINAL = {');
  if (start === -1) throw new Error('FP_FINAL anchor not found');
  let i = s.indexOf('{', start);
  let depth = 0, inStr = false, esc = false;
  for (; i < s.length; i++) {
    const ch = s[i];
    if (inStr) { if (esc) esc = false; else if (ch === '\\') esc = true; else if (ch === '"') inStr = false; }
    else if (ch === '"') inStr = true;
    else if (ch === '{') depth++;
    else if (ch === '}') { depth--; if (depth === 0) { i++; break; } }
  }
  return JSON.parse(s.slice(s.indexOf('{', start), i));
}
function extractPortraits(s) {
  const start = s.indexOf('var PORTRAITS = [');
  if (start === -1) throw new Error('PORTRAITS anchor not found');
  const end = s.indexOf('].map', start);
  const baseUrl = 'https://pub-ee146405c865419591fbf27a945ce6d4.r2.dev/portraits/';
  // JS literal (single quotes) — evaluate it.
  return ((new Function('return (' + s.slice(s.indexOf('[', start), end + 1) + ')'))()).map(n => baseUrl + n);
}
const SLIDES = extractSlides(agmtStr);
const SLIDE_IMGS = extractSlideImgs(agmtStr);
const FINAL = extractFinal(agmtStr);
const PORTRAITS = extractPortraits(agmtStr);
if (SLIDES.length !== 27) throw new Error('SLIDES count ' + SLIDES.length);
if (SLIDE_IMGS.length !== 27) throw new Error('slide imgs count ' + SLIDE_IMGS.length);
if (Object.keys(FINAL).length !== 8) throw new Error('FP_FINAL keys ' + Object.keys(FINAL).length);
if (SLIDES[0].t !== 'The Old Way') throw new Error('first slide is not The Old Way: ' + SLIDES[0].t);
if (SLIDES[26].t !== 'Your Franchise') throw new Error('last slide is not Your Franchise: ' + SLIDES[26].t);
if (!SLIDE_IMGS.every(u => /^data:image\/(jpeg|webp|png);base64,/.test(u))) throw new Error('a slide img is not an image data URI');
const slideTitles = SLIDES.map((s, i) => (i + 1) + '. ' + s.t);
writeFileSync(LANE + 'evidence/slides-r3.json', JSON.stringify({source: 'live nayanet.app/agreement v25, 22953906 B, sha 2c88513f…', count: SLIDES.length, titles: slideTitles, final_keys: Object.keys(FINAL), portraits: PORTRAITS}, null, 2) + '\n');
writeFileSync(LANE + 'evidence/slide-order-r3.md', '# Visual story slide order — harvested verbatim from live agreement v25\n\n' + slideTitles.map(t => '- ' + t).join('\n') + '\n\nEntry slide: 1. The Old Way (live station label "THE OLD WAY"). Last slide: 27. Your Franchise.\n\nSlide text (t/x/a) and pictures (EMBED.slides) are embedded verbatim in portal.html; the eight link answers (FP_FINAL) likewise. The official v7 words source (COLLECTIVE-AGREEMENT-OFFICIAL-20261115.md) governs the end-card wording: "I agree — show me my world ◆".\n');

let html = baseStr;
const evidence = {
  base: 'round-2 staged portal.html (portal-r2.html)',
  base_bytes: base.length, base_sha256: baseSha,
  agreement_live_bytes: agmt.length, agreement_live_sha256: agmtSha,
  agreement_reconciliation: 'brief cited a fresh fetch of 18,530,304 B sha 6527cde7…; this fetch returns 22,953,906 B sha 2c88513f…, byte-identical to round-1/round-2 v25. Harvest is from the bytes actually fetched here.',
  slides: SLIDES.length, slide_images: SLIDE_IMGS.length,
  slide_image_chars: SLIDE_IMGS.reduce((a, b) => a + b.length, 0),
  final_keys: Object.keys(FINAL),
  first_slide: SLIDES[0].t, last_slide: SLIDES[26].t,
};

// --- 1. The ⓘ in the circle becomes the red ACTIVE N. ---
const infoAnchor = '<button class="fp-deed-info" id="fpDeedInfo" type="button" aria-label="Read the full agreement">&#9432;</button>';
if (!html.includes(infoAnchor)) throw new Error('ⓘ button anchor not found');
html = html.replace(infoAnchor,
  '<button class="fp-deed-info fp-circle-n" id="fpCircleN" type="button" aria-label="The Collective Agreement — the red N"><img id="fpCircleNImg" alt="The red N — a raised glass ball with a gold N"><span class="ncorner-gloss" aria-hidden="true"></span></button>');
// The circle N's img src is set at runtime from the corner ball (same harvested
// bytes, no duplicate 182 KB data URI); it spins eco-spin 90s like the corner.

// --- 2. The old 13-paragraph pop-up reader GOES: markup + PARAS script. ---
const readerStart = html.indexOf('<div class="fp-deed-reader" id="fpDeedReader" hidden>');
if (readerStart === -1) throw new Error('reader markup anchor not found');
const readerClose1 = html.indexOf('</div>', readerStart);
const readerClose2 = html.indexOf('</div>', readerClose1 + 6);
const readerBlock = html.slice(readerStart, readerClose2 + 6);
if (!readerBlock.includes('fpDeedPara') || !readerBlock.includes('fpDeedNext')) throw new Error('reader block bounds wrong');
html = html.slice(0, readerStart) + html.slice(readerClose2 + 6);
const parasComment = html.indexOf('(item 61/62)');
if (parasComment === -1) throw new Error('PARAS comment anchor not found');
const scriptStart = html.lastIndexOf('<script>', parasComment);
const parasEnd = html.indexOf('})();', parasComment);
const scriptEnd = html.indexOf('</script>', parasEnd);
if (scriptStart === -1 || parasEnd === -1 || scriptEnd === -1) throw new Error('PARAS script bounds not found');
const parasBlock = html.slice(scriptStart, scriptEnd + 9);
if (!parasBlock.includes('var PARAS = [')) throw new Error('PARAS script does not contain PARAS');
html = html.slice(0, scriptStart) + html.slice(scriptEnd + 9);

// --- 3. R2 (a) ring-fade is moot (no reader any more): remove its CSS. ---
const fadeComment = '/* ROUND 2 (a) — while the inner reader is open, the orbit jewel-dot ring';
const fadeIdx = html.indexOf(fadeComment);
if (fadeIdx === -1) throw new Error('R2 (a) CSS anchor not found');
const fadeEnd = html.indexOf('.naya-orbit{transition:opacity .5s ease;}', fadeIdx);
if (fadeEnd === -1) throw new Error('R2 (a) CSS end not found');
html = html.slice(0, fadeIdx) + html.slice(fadeEnd + '.naya-orbit{transition:opacity .5s ease;}'.length + 1);

// --- 4. "Read the agreement" no longer navigates to the landing (preview page). ---
const navAnchor = "if(enterBtn)enterBtn.addEventListener('click',function(){window.location.href='/agreement-landing';});";
if (!html.includes(navAnchor)) throw new Error('fpEnterDeal navigation anchor not found');
html = html.replace(navAnchor,
  '/* ROUND 3 — SUPERSEDED (Shawn 2026-11-25 ~17:35 MST: "There should be no\n     preview page like this has a preview page. I don\'t want that."): "Read\n     the agreement" no longer navigates to /agreement-landing (the onboarding\n     landing). It opens the visual story in place — wired in the story script\n     (fpEnterDeal -> openStory(0)). The /agreement-landing worker route stays\n     for the deck\'s own deep links; the front page no longer uses it. */');

// --- 5. Reduced-motion: the circle N stops with the corner N. ---
const rmAnchor = '@media (prefers-reduced-motion:reduce){\n  .ncorner::before{animation:none;}\n  .ncorner-right img{animation:none;}\n}';
if (!html.includes(rmAnchor)) throw new Error('reduced-motion anchor not found');
html = html.replace(rmAnchor,
  '@media (prefers-reduced-motion:reduce){\n  .ncorner::before{animation:none;}\n  .ncorner-right img{animation:none;}\n  button.fp-circle-n img{animation:none;}\n}');

// --- 6. Story CSS (new style element) + markup + data + script, before </head> / </body>. ---
const storyCss = readFileSync(LANE + 'story-r3.css', 'utf8');
const storyHtml = readFileSync(LANE + 'story-r3.html', 'utf8');
const storyJs = readFileSync(LANE + 'story-r3.js', 'utf8');
const headClose = html.indexOf('</head>');
if (headClose === -1) throw new Error('</head> not found');
html = html.slice(0, headClose) + '<style>\n' + storyCss + '\n</style>\n' + html.slice(headClose);
let dataScript = '<script>\nvar FP_SLIDES = ' + JSON.stringify(SLIDES) + ';\nvar FP_SLIDE_IMGS = ' + JSON.stringify(SLIDE_IMGS) + ';\nvar FP_FINAL = ' + JSON.stringify(FINAL) + ';\nvar FP_PORTRAITS = ' + JSON.stringify(PORTRAITS) + ';\n</script>\n';
if (dataScript.toLowerCase().includes('</script', 9)) {
  // A literal </script inside a data string would close the element early.
  dataScript = dataScript.split('</script').join('<\\/script');
}
const bodyClose = html.indexOf('</body>');
if (bodyClose === -1) throw new Error('</body> not found');
html = html.slice(0, bodyClose) + storyHtml + '\n' + dataScript + '<script>\n' + storyJs + '\n</script>\n' + html.slice(bodyClose);

// --- 7. Assertions. ---
const assert = (name, ok) => { console.log((ok ? 'PASS ' : 'FAIL ') + name); if (!ok) process.exitCode = 1; };
assert('R2 base sha verified', baseSha.startsWith('66664c07'));
assert('agreement v25 sha verified', agmtSha.startsWith('2c88513f'));
assert('27 slides harvested, first The Old Way, last Your Franchise', SLIDES.length === 27 && SLIDES[0].t === 'The Old Way' && SLIDES[26].t === 'Your Franchise');
assert('27 slide images harvested (JPEG data URIs)', SLIDE_IMGS.length === 27);
assert('8 final link answers harvested', Object.keys(FINAL).length === 8 && ['vow', 'deal', 'promise', 'governance', 'constitution', 'laws', 'rules', 'oath'].every(k => k in FINAL));
assert('ⓘ gone (no fpDeedInfo, no &#9432;)', !html.includes('fpDeedInfo') && !html.includes('&#9432;'));
assert('old reader gone (no PARAS, no reader element, no fpDeedPara)', !html.includes('var PARAS') && !html.includes('id="fpDeedReader"') && !html.includes('fpDeedPara'));
// NOTE: three null-guarded references to getElementById('fpDeedReader') remain
// in the pre-existing v2b + returning scripts — they return null and do
// nothing now that the element is gone; the v2b early return keeps the circle
// N in the circle at every width, which is the wanted end state.
assert('circle N present (fpCircleN, spins eco-spin 90s)', html.includes('id="fpCircleN"') && html.includes('button.fp-circle-n img{width:100%;height:100%;border-radius:50%;object-fit:cover;'));
assert('story overlay present (fpStory, 27 slides wired)', html.includes('id="fpStory"') && html.includes('FP_SLIDES.length') && html.includes('id="fpStoryAgree"'));
assert('official agree wording on the end slide', html.includes('I agree &mdash; show me my world &#9670;'));
assert('agree button NOT mid-slide: only in the bottom wrap', (html.match(/class="fp-story-agree"/g) || []).length === 1 && html.indexOf('id="fpStoryAgreeWrap"') < html.indexOf('class="fp-story-nav"'));
assert('franchise text box carries his refined wording (one personal / one business / one space)', html.includes('one personal page, one business page, one space &mdash; free forever. Yours.'));
assert('eight links in the bottom bar only', (html.match(/data-final="/g) || []).length === 8 && html.includes('id="fpStoryLinks"'));
assert('no navigation to the preview landing from the front page', !html.includes("window.location.href='/agreement-landing'"));
assert('F1 kept: corner ball spins (eco-spin 90s on the img)', html.includes('.ncorner-right img{animation:eco-spin 90s linear infinite;}'));
assert('F1 kept: ball asset unchanged (WEBP data URI kept)', html.includes('data:image/webp;base64,'));
assert('F2 kept: narrow+short gate present', html.includes('@media (max-width:640px) and (max-height:700px)'));
assert('front page still clean: sentence only behind the N', !/id="fpDeedSentence">[^<]*By entering/.test(html));
assert('final nine: 9 eco-item anchors', (html.match(/class="eco-item"/g) || []).length === 9);
assert('structure: style-element count 7 open / 7 close (6 R2 + 1 story)', (html.match(/<style>/g) || []).length === 7 && (html.match(/<\/style>/g) || []).length === 7);
assert('structure: RETURNING rules still inside a style element', html.indexOf('/* PORTAL RETURNING VIEW v2') < html.indexOf('</head>'));
assert('no stray </script inside the data script', !dataScript.toLowerCase().includes('</script', 9));
// The short live wording "I agree ◆" must not be the story's agree button.
const shortAgree = (html.match(/I agree &#9670;/g) || []).length;
console.log('INFO short "I agree ◆" occurrences in portal (live deck text, not the story button):', shortAgree);
evidence.short_agree_occurrences = shortAgree;

const out = Buffer.from(html, 'utf8');
writeFileSync(LANE + 'portal.html', out);
writeFileSync(LANE + 'evidence/harvest-r3.json', JSON.stringify(evidence, null, 2) + '\n');
console.log('portal.html', out.length, 'B sha256', sha(out));
console.log('R2 portal was', base.length, 'B; delta', out.length - base.length, 'B');
