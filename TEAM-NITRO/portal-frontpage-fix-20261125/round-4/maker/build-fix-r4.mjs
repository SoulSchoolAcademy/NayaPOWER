// Portal front-page fix ROUND 4 — the one-item fix round on the Round 3 base.
// Base: R3 staged portal (sha d46c4409...), branch portal-frontpage-fix-20261125-r3.
// THE ONE DEFECT (R3 checker GOES BACK): F2 at true 390x844 — the front-page
// heading reads "NAYA WELCOM": the final "ES" is covered by the portal's chrome
// rim. Mechanism (measured by the maker, R4): at 390 the portal is 248px, the
// core 224px, and .content is 210px tall (presence 34 + margin 11 + form 96 +
// sentence 10 + circle-N 56 + 3 slack) — so the heading sits 7px below the core
// top, where the circular chord is only ~112px wide and the tail glyphs fall
// outside the core circle (elementFromPoint hits DIV.portal). In R2 the deed
// sentence sat UNDER the portal (moved there by the v2b script), so .content
// was 141px and the heading sat 42px below the core top, clear. R3 removed
// the reader, the v2b script early-returned (reader null), and the sentence
// stayed inside the circle with the taller 56px circle N.
// FIX (smallest change; the circle N is NOT moved, the spin is NOT changed,
// the portal is NOT redesigned, the story is NOT touched): at <=480px only,
// take 32px out of the in-circle stack — presence margin 11->4, Enter margin
// 12->6 + height 41->37, name input 43->39, sentence margin 10->2 + flex so
// the <p> hugs the 56px button — so .content is ~178px, centred with ~23px
// slack top and bottom, and the heading drops to ~R2 clearance. No new
// font-size declarations (design-law counts must not move). Fresh view only
// where the returning view shares a selector (body:not(.fp-returning)).
// FOLD-INS from Round 3 (fix-or-record):
//   (a) desktop end-slide red N orb 83% clipped at the board edge (board
//       overflowed 69px): on the LAST slide only, desktop only (the phone
//       end slide is a HOLD item), take 82px out of the face + margins.
//   (b) "Our Vow" answer opens scrolled to its tail: focus the Close button
//       with preventScroll and reset the answer frame to scrollTop 0 on open.
// Node only (python writes EPERM). Base is the R3 lane portal, edited —
// nothing is re-harvested, nothing rebuilt.
import {readFileSync, writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const sha = b => createHash('sha256').update(b).digest('hex');
const LANE = new URL('./', import.meta.url).pathname;

// --- 0. Base identity: the R3 staged bytes exactly. ---
const base = readFileSync(LANE + 'portal-r3.html');
const baseSha = sha(base);
if (baseSha !== 'd46c440920ead620bca41c52492cccaa78f6ce7ca38edba6c3a0b93113498c15')
  throw new Error('R3 base sha mismatch: ' + baseSha);
let html = base.toString('utf8');

// --- 1. Story CSS/JS: swap the inlined R3 blocks for the R4 files. ---
const css3 = readFileSync(LANE + 'story-r3.css', 'utf8');
const css4 = readFileSync(LANE + 'story-r4.css', 'utf8');
const js3 = readFileSync(LANE + 'story-r3.js', 'utf8');
const js4 = readFileSync(LANE + 'story-r4.js', 'utf8');
const styleStart = html.indexOf('<style>\n/* ROUND 3 — THE VISUAL STORY');
if (styleStart === -1) throw new Error('story style block anchor not found');
const styleEnd = html.indexOf('</style>', styleStart);
if (styleEnd === -1) throw new Error('story style block end not found');
if (html.slice(styleStart + 8, styleEnd) !== css3 + '\n') throw new Error('inlined story CSS != story-r3.css');
html = html.slice(0, styleStart + 8) + css4 + '\n' + html.slice(styleEnd);
const jsStart = html.indexOf('<script>\n/* ROUND 3 — the visual story');
if (jsStart === -1) throw new Error('story script block anchor not found');
const jsEnd = html.indexOf('</script>', jsStart);
if (jsEnd === -1) throw new Error('story script block end not found');
if (html.slice(jsStart + 9, jsEnd) !== js3 + '\n') throw new Error('inlined story JS != story-r3.js');
html = html.slice(0, jsStart + 9) + js4 + '\n' + html.slice(jsEnd);

// --- 2. F2: narrow-only stack tightening inside the <=480px media block. ---
const narrowAnchor = '#fpDeedSentence{max-width:360px;margin:10px auto 0}';
if (!html.includes(narrowAnchor)) throw new Error('narrow #fpDeedSentence anchor not found');
if ((html.match(/ROUND 4 — F2/g) || []).length !== 0) throw new Error('F2 block already present');
const f2 = `\n  /* ROUND 4 — F2 (R3 checker GOES BACK: heading "NAYA WELCOM" at 390 — "ES"
     covered by the rim). At <=480px the 56px circle N inside .content made the
     stack 210px in a 224px core, so the heading sat 7px below the core top
     where the chord is narrow. Take 32px out of the stack (fresh view only
     where shared with returning): presence margin 11->4, Enter margin 12->6
     + height 41->37, name input 43->39, sentence margin 10->2 + flex so the
     <p> hugs the button. .content drops to ~178px, centred with ~23px slack,
     heading back toward the R2 clearance. Circle N untouched (still 56px,
     still in the circle, still eco-spin 90s); no font-size touched. */
  body:not(.fp-returning) .presence{margin-bottom:4px}
  #entryForm .enter{margin-top:6px;height:37px}
  #entryForm .input{height:39px}
  body:not(.fp-returning) #fpDeedSentence{margin-top:2px;display:flex;justify-content:center}`;
html = html.replace(narrowAnchor, narrowAnchor + f2);

// --- 3. Assertions. ---
const assert = (name, ok) => { console.log((ok ? 'PASS ' : 'FAIL ') + name); if (!ok) process.exitCode = 1; };
assert('R3 base sha verified', baseSha.startsWith('d46c4409'));
assert('story CSS swapped to R4 (fp-last desktop rules present)', html.includes('#fpStory.fp-last .fp-story-face img{width:72px;height:72px}'));
assert('story JS swapped to R4 (fp-last toggle present)', html.includes("story.classList.toggle('fp-last', last);"));
assert('story JS swapped to R4 (vow frame opens at head)', html.includes('finalClose.focus({preventScroll:true});') && html.includes("if (fr) fr.scrollTop = 0;"));
assert('F2 block present once', (html.match(/ROUND 4 — F2/g) || []).length === 1);
assert('F2: presence margin tightened (fresh only)', html.includes('body:not(.fp-returning) .presence{margin-bottom:4px}'));
assert('F2: input/enter heights tightened (form only)', html.includes('#entryForm .enter{margin-top:6px;height:37px}') && html.includes('#entryForm .input{height:39px}'));
assert('F2: sentence margin + flex (fresh only)', html.includes('body:not(.fp-returning) #fpDeedSentence{margin-top:2px;display:flex;justify-content:center}'));
assert('circle N untouched: 56px button, eco-spin 90s, red ball', html.includes('button.fp-circle-n{position:relative;width:56px;height:56px') && html.includes('button.fp-circle-n img{width:100%;height:100%;border-radius:50%;object-fit:cover;') && html.includes('animation:eco-spin 90s linear infinite'));
assert('circle N still in the circle (inside .content, after the form)', html.indexOf('id="fpCircleN"') > html.indexOf('id="entryForm"') && html.indexOf('id="fpCircleN"') < html.indexOf('id="returningView"'));
assert('F1 kept: corner ball spins (eco-spin 90s)', html.includes('.ncorner-right img{animation:eco-spin 90s linear infinite;}'));
assert('F2 573 gate kept', html.includes('@media (max-width:640px) and (max-height:700px)'));
assert('story data untouched: 27 slides, 27 pictures, 8 answers', html.includes('var FP_SLIDES = ') && (html.match(/data-final="/g) || []).length === 8);
assert('official agree wording untouched', html.includes('I agree &mdash; show me my world &#9670;'));
assert('no new font-size declarations in R4 (design-law counts must not move)', !f2.includes('font-size:') && !css4.replace(css3, '').includes('font-size:'));
assert('ⓘ still gone, reader still gone', !html.includes('fpDeedInfo') && !html.includes('id="fpDeedReader"'));
assert('no navigation to the preview landing', !html.includes("window.location.href='/agreement-landing'"));
assert('structure: 7 style elements', (html.match(/<style>/g) || []).length === 7 && (html.match(/<\/style>/g) || []).length === 7);

const out = Buffer.from(html, 'utf8');
writeFileSync(LANE + 'portal.html', out);
console.log('portal.html', out.length, 'B sha256', sha(out));
console.log('R3 portal was', base.length, 'B; delta', out.length - base.length, 'B');
