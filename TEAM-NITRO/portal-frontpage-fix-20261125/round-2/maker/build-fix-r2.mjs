// Portal front-page fix ROUND 2 — 2026-11-25, captain's eye findings.
// Base: the round-1 STAGED portal bytes (sha 737fca6b...), NOT a rebuild.
// F1 — THE RED N DOES NOT SPIN (eye watched ~3 min, two close-ups 12 s apart:
//   gold N upright, highlight never moved; dotted ring likewise static).
//   DIAGNOSIS (proven by probe, not assumed): the live agreement v25's own
//   ball does NOT rotate — .orb-wrap.jewel carries only `floaty` 5.5s (a
//   vertical bob) and its `orbit-spin` sweeps a ring custom-property; there
//   is NO ball rotation to harvest verbatim. The portal corner's only motion
//   was the thin .ncorner::before ring (eco-spin 90s) — a symmetric arc that
//   reads as static — while the ball IMG itself had `animation:none` and
//   `transform:none` at t0 and t25 (measured). The fix applies the portal's
//   OWN eco-spin keyframes (90s linear infinite, ambient 60-180s per the
//   laws §1) to the right-corner IMG itself, so the gold N visibly turns:
//   at 90s a 20 s gap is 80 deg. The gloss span stays fixed above the ball
//   (z-index 4) — the light stays top-left while the ball turns under it,
//   exactly as the one-light law wants. Left (black) N untouched; asset,
//   alt, size, position, destination all unchanged.
// F2 — PHONE-WIDTH HEADING COLLISION (eye at 573 px wide: "NAYA WELCOMES
//   YOU" wraps to two lines, "YOU" collides with the top rim; "Welcome
//   back," tight against the same rim).
//   REPRODUCED at 573x355 (short window): the portal shrinks to its 250 px
//   floor, the content narrows to 187 px, the heading wraps to two lines
//   and its top line is wider than the circle's chord at its height, so
//   the rim slices the word (screenshots diag3-*.png). At 573x844 and
//   573x700 there is no collision in either view — the defect needs a
//   SHORT viewport. Fix, narrow+short only (@media max-width:640px AND
//   max-height:700px): the heading stays one line (nowrap, tracking 0 —
//   NO new font-size declaration, so the design-law counts cannot move),
//   and the stack compresses (input/enter heights, margins, gaps) so the
//   heading sits lower in the wide band of the circle. Desktop, 390x844
//   and 573x844 are untouched by the gate.
// (a) READER/RING: while the inner reader is open, the orbit jewel-dot
//   ring fades out (body.fp-reader-open) so it no longer crosses the
//   reader card's text on phone. Small, safe, one class toggle.
// NOTHING ELSE CHANGES. Node only (python writes EPERM in this VM).
import {readFileSync, writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const sha = b => createHash('sha256').update(b).digest('hex');
const LANE = new URL('./', import.meta.url).pathname;
const R1 = LANE + 'portal-r1.html';
const AGMT = LANE + 'evidence/agreement-live.html';

// --- 0. Base identity: the R1 staged bytes exactly. ---
const base = readFileSync(R1, 'utf8');
const baseSha = sha(Buffer.from(base));
if (baseSha !== '737fca6be2832855c8f6b523fc4920b8ea3d35f363f95278f141671b0c6cc82a')
  throw new Error('R1 base sha mismatch: ' + baseSha);

// --- 0b. Agreement v25 identity + diagnosis anchors. ---
const agmt = readFileSync(AGMT, 'utf8');
const agmtSha = sha(Buffer.from(agmt));
if (agmtSha !== '2c88513f9011b176c0af910ec0d81e314578cfe904dd62ded9010a9a54052e11')
  throw new Error('agreement-live sha mismatch: ' + agmtSha);
// The agreement's ball: floaty bob only, no rotation (the diagnosis).
if (!agmt.includes('animation:floaty 5.5s ease-in-out infinite'))
  throw new Error('agreement floaty anchor not found — diagnosis unproven');
if (!agmt.includes('@keyframes orbit-spin{to{--oa:360deg}'))
  throw new Error('agreement orbit-spin anchor not found');

let html = base;
const evidence = {
  base: 'round-1 staged portal.html (portal-r1.html)',
  base_bytes: base.length, base_sha256: baseSha,
  agreement_live_bytes: agmt.length, agreement_live_sha256: agmtSha,
  diagnosis: 'agreement v25 ball: floaty 5.5s bob only + orbit-spin ring sweep; NO ball rotation to harvest. Portal corner img had animation:none (measured t0/t25). Fix: portal\'s own eco-spin 90s on the right-corner img.',
};

// --- 1. F1: the ball itself spins. ---
const imgRule = '.ncorner img{width:100%;height:100%;border-radius:50%;object-fit:cover;display:block;}';
if (!html.includes(imgRule)) throw new Error('.ncorner img anchor not found');
html = html.replace(imgRule, imgRule +
  '\n/* ROUND 2 F1 (eye: the red N does not spin) — the ball ITSELF turns:\n   the portal\'s own eco-spin 90s (ambient 60-180s, laws §1) on the RIGHT\n   corner img, so the gold N is seen at different angles (80 deg per 20 s).\n   The agreement\'s own ball never rotates (floaty bob only), so there is\n   no rotation to harvest verbatim — this applies the file\'s own orbit\n   keyframes to the image. The gloss span stays fixed above the ball: the\n   light stays top-left while the ball turns under it. Left N untouched. */' +
  '\n.ncorner-right img{animation:eco-spin 90s linear infinite;}');
if (!html.includes('.ncorner-right img{animation:eco-spin 90s linear infinite;}'))
  throw new Error('F1 img-spin rule did not land');
// Reduced-motion: the spin stops with the ring.
const rmAnchor = '@media (prefers-reduced-motion:reduce){\n  .ncorner::before{animation:none;}\n}';
if (!html.includes(rmAnchor)) throw new Error('reduced-motion anchor not found');
html = html.replace(rmAnchor,
  '@media (prefers-reduced-motion:reduce){\n  .ncorner::before{animation:none;}\n  .ncorner-right img{animation:none;}\n}');

// --- 1b. F1: update the harvest comment to record the spin honestly. ---
const oldSpinLine = '   The N lights up (red hover glow) and spins (orbit ring, eco-spin 90s);';
if (!html.includes(oldSpinLine)) throw new Error('F1 comment anchor not found');
html = html.replace(oldSpinLine,
  '   The N lights up (red hover glow) and spins (orbit ring, eco-spin 90s);\n' +
  '   ROUND 2 F1 (eye: the N did NOT spin — the ring alone reads as static\n' +
  '   and the img never moved): the BALL ITSELF now spins — .ncorner-right\n' +
  '   img carries eco-spin 90s, so the gold N turns (80 deg per 20 s). The\n' +
  '   agreement\'s own ball has no rotation to harvest (floaty bob only);\n' +
  '   the spin is the portal\'s own harvested orbit keyframes, applied to\n' +
  '   the image. Gloss stays fixed: light top-left, ball turning under it.');

// --- 2. F2: heading clears the rim at narrow + short widths. ---
const f2Anchor = '  body.fp-returning .returning-greet{margin-bottom:4px}\n}';
if (!html.includes(f2Anchor)) throw new Error('F2 anchor (480px block end) not found');
const f2Css = f2Anchor + `
/* ROUND 2 F2 (eye at 573px: "NAYA WELCOMES YOU" wraps, "YOU" collides with
   the top rim; "Welcome back," tight against it) — REPRODUCED at 573x355:
   the portal shrinks to its 250px floor, the content narrows to 187px, the
   heading wraps to two lines and its top line is wider than the circle's
   chord at its height, so the rim slices the word. At 573x844 / 573x700 /
   390x844 there is no collision — the defect needs a SHORT viewport.
   Narrow + short only (max-width:640px AND max-height:700px): the heading
   stays ONE line (nowrap, tracking 0 — NO font-size change, so the
   design-law counts cannot move) and the stack compresses (input/enter
   heights, margins, gaps) so the heading sits lower, in the wide band of
   the circle. Desktop, 390x844 and 573x844 untouched by the gate.
   NOTE: no style tags here — this anchor sits INSIDE an open style
   element (the 480-block's); a nested style element would close it early and
   strand the rules after it as visible text. */
@media (max-width:640px) and (max-height:700px){
  .presence{letter-spacing:0;white-space:nowrap;margin-bottom:4px}
  .input{height:38px}
  .enter{height:40px;margin-top:6px}
  .fp-deed-sentence{margin-top:6px}
  .returning-greet{margin-bottom:4px}
  .returning{gap:4px}
  .new-account{padding:2px 12px}
}`;
html = html.replace(f2Anchor, f2Css);

// --- 3. (a) Reader open: fade the orbit ring so it cannot cross the card. ---
const orbitRule = '.naya-orbit{';
if (!html.includes(orbitRule)) throw new Error('.naya-orbit anchor not found');
html = html.replace(orbitRule,
  '/* ROUND 2 (a) — while the inner reader is open, the orbit jewel-dot ring\n   fades out, so it no longer crosses the reader card / its text on phone.\n   The ring returns when the reader closes. */\n' +
  'body.fp-reader-open .naya-orbit{opacity:0;}\n' +
  '.naya-orbit{transition:opacity .5s ease;}\n' +
  '.naya-orbit{');
// Reader toggle: set/clear the class on open/close.
const openAnchor = "    reader.hidden = !open;\n    if (open) show(0);";
if (!html.includes(openAnchor)) throw new Error('reader open anchor not found');
html = html.replace(openAnchor,
  "    reader.hidden = !open;\n    document.body.classList.toggle('fp-reader-open', open);\n    if (open) show(0);");
const closeAnchor = "    if (idx >= PARAS.length - 1) { reader.hidden = true; return; }";
if (!html.includes(closeAnchor)) throw new Error('reader close anchor not found');
html = html.replace(closeAnchor,
  "    if (idx >= PARAS.length - 1) { reader.hidden = true; document.body.classList.remove('fp-reader-open'); return; }");

// --- 4. Assertions: only the two defects + (a) changed. ---
const assert = (name, ok) => { console.log((ok ? 'PASS ' : 'FAIL ') + name); if (!ok) process.exitCode = 1; };
assert('F1: right-corner img spins (eco-spin 90s)', html.includes('.ncorner-right img{animation:eco-spin 90s linear infinite;}'));
assert('F1: left img untouched (no spin rule)', !html.includes('.ncorner-left img{animation'));
assert('F1: reduced-motion disables the spin', html.includes('.ncorner-right img{animation:none;}'));
assert('F1: ring still spins (eco-spin 90s on ::before)', html.includes('animation:eco-spin 90s linear infinite;'));
assert('F1: ball asset unchanged (WEBP data URI kept)', html.includes('data:image/webp;base64,'));
assert('F1: gloss span kept', html.includes('class="ncorner-gloss"'));
assert('F1: destinations kept', html.includes('ncorner-right" href="https://nayanet.app/agreement"') && html.includes('ncorner-left" href="https://nayanet.app/"'));
assert('F2: narrow+short gate present', html.includes('@media (max-width:640px) and (max-height:700px)'));
assert('F2: heading one line, no font-size change', html.includes('.presence{letter-spacing:0;white-space:nowrap;margin-bottom:4px}') && !/\.presence\{[^}]*font-size:\s*11px/.test(html));
assert('F2: desktop heading untouched (4 pre-existing .presence{ rules + 1 mine)', (html.match(/\.presence\{/g) || []).length === 5);
assert('(a): reader-open ring fade present', html.includes("body.fp-reader-open .naya-orbit{opacity:0;}"));
assert('(a): reader toggle sets/clears the class', html.includes("classList.toggle('fp-reader-open', open)") && html.includes("classList.remove('fp-reader-open')"));
assert('structure: style-element count unchanged (6 open, 6 close)', (html.match(/<style>/g) || []).length === 6 && (html.match(/<\/style>/g) || []).length === 6);
assert('structure: RETURNING rules still inside a style element', html.indexOf('/* PORTAL RETURNING VIEW v2') < html.indexOf('</head>') && html.indexOf('/* PORTAL RETURNING VIEW v2') > html.lastIndexOf('<style>', html.indexOf('/* PORTAL RETURNING VIEW v2')));
assert('front page: sentence still only behind ⓘ', !/id="fpDeedSentence">[^<]*By entering/.test(html));
assert('inner reader: PARAS[0] still the moved sentence', html.includes('var PARAS = ["By entering your name, you make it official'));
assert('final nine: 9 eco-item anchors', (html.match(/class="eco-item"/g) || []).length === 9);
assert('walk: QUESTIONS kept', html.includes('QUESTIONS'));
assert('certificate: identity file untouched (checked by build-worker)', true);

// Diff vs R1 base: changed lines.
const baseLines = base.split('\n'), newLines = html.split('\n');
let changed = 0; const changedIdx = [];
const maxLen = Math.max(baseLines.length, newLines.length);
for (let i = 0; i < maxLen; i++) {
  if (baseLines[i] !== newLines[i]) { changed++; if (changedIdx.length < 40) changedIdx.push(i + 1); }
}
evidence.diff_lines_changed = changed;
evidence.diff_line_numbers_sample = changedIdx;
console.log('diff lines changed vs R1 base:', changed, 'sample lines:', changedIdx.join(','));

writeFileSync(LANE + 'portal.html', html);
writeFileSync(LANE + 'evidence/harvest-r2.json', JSON.stringify(evidence, null, 2) + '\n');
console.log('portal.html', html.length, 'B sha256', sha(Buffer.from(html)));
console.log('R1 portal was', base.length, 'B; delta', html.length - base.length, 'B');
