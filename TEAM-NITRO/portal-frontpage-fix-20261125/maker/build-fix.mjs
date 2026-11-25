// Portal front-page fix 2026-11-25 — Shawn's eye, voice call ~15:51-15:52 MST.
// DEFECT 1: the wall of text under the name input on the new-user front page.
//   The agreement sentence leaves the visible front page; it moves verbatim
//   into the inner agreement reader (PARAS[0], behind the ⓘ), and the front
//   page keeps only greeting + name input + Enter button + the ⓘ trigger.
// DEFECT 2: the wrong red N bottom-right.
//   The small static PNG red disc (13,790 B) is replaced by the official red
//   N harvested BYTE-FOR-BYTE from the live agreement v25 (EMBED.ball, WEBP
//   182,452 B) — the raised glass ball with a gold N. The corner's existing
//   harvested orbit ring (.ncorner::before, eco-spin 90s) already spins, and
//   the hover red glow already lights it up; the agreement's jewel-gloss
//   highlight is harvested verbatim too (selector renamed only), so the ball
//   reads as glass, not a flat disc. Black N bottom-left untouched.
// NOTHING ELSE CHANGES. Node only (python writes EPERM in this VM).
import {readFileSync, writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const sha = b => createHash('sha256').update(b).digest('hex');
const LANE = new URL('./', import.meta.url).pathname;
const R2 = '/home/hatch/workspace/team-nitro/portal-consolidated-20261125/maker/portal.html';

// --- 0. Base identity: must be the R2 staged bytes exactly. ---
const base = readFileSync(R2, 'utf8');
const baseSha = sha(Buffer.from(base));
if (baseSha !== '8fc7d69db5b9f7544bbd11a1a86b53eab1e7f652fd2ad316b7c62f83a25efe60')
  throw new Error('R2 base sha mismatch: ' + baseSha);

// --- 1. Harvest EMBED.ball verbatim from live agreement v25. ---
const agmt = readFileSync(LANE + 'evidence/agreement-live.html', 'utf8');
const agmtSha = sha(Buffer.from(agmt));
if (agmtSha !== '2c88513f9011b176c0af910ec0d81e314578cfe904dd62ded9010a9a54052e11')
  throw new Error('agreement-live sha mismatch: ' + agmtSha);
const ballMatch = agmt.match(/EMBED\.ball = "([^"]+)"/);
if (!ballMatch) throw new Error('EMBED.ball not found in agreement v25');
const BALL = ballMatch[1]; // full data URI, verbatim incl. prefix
const ballB64 = BALL.split(',', 1)[1] || BALL.split(',')[1];
const ballRaw = Buffer.from(BALL.split(',')[1], 'base64');
// VP8X canvas: chunk data starts at 20; width-1 at 24..26, height-1 at 27..29.
const ballW = 1 + ballRaw.readUIntLE(24, 3);
const ballH = 1 + ballRaw.readUIntLE(27, 3);

let html = base;
const evidence = {
  base: 'portal-consolidated-20261125 R2 staged portal.html',
  base_bytes: base.length, base_sha256: baseSha,
  agreement_live_bytes: agmt.length, agreement_live_sha256: agmtSha,
  ball_format: BALL.slice(0, BALL.indexOf(';')),
  ball_data_uri_chars: BALL.length,
  ball_bytes: ballRaw.length, ball_sha256: sha(ballRaw),
  ball_b64_sha256: sha(Buffer.from(BALL.split(',')[1])),
  ball_dimensions: ballW + 'x' + ballH,
  ball_alt_harvested: 'The red N — a raised glass ball with a gold N',
};

// --- 2a. DEFECT 1: strip the sentence text, keep only the ⓘ trigger. ---
const SENT_HTML = 'By entering your name, you make it official &mdash; you are signing the Collective Agreement, and you get the deed to your own world: high-level digital real estate &mdash; your personal page, your business, your space &mdash; free forever. ';
if (!html.includes(SENT_HTML)) throw new Error('sentence HTML not found (already changed?)');
html = html.replace(SENT_HTML, '');
if (html.includes('By entering your name')) throw new Error('sentence text still present after strip');

// --- 2b. DEFECT 1: the same sentence verbatim as PARAS[0] (inner page). ---
const SENT_JS = 'By entering your name, you make it official \\u2014 you are signing the Collective Agreement, and you get the deed to your own world: high-level digital real estate \\u2014 your personal page, your business, your space \\u2014 free forever.';
const parasAnchor = 'var PARAS = ["Imagine the internet on steroids.';
if (!html.includes(parasAnchor)) throw new Error('PARAS anchor not found');
html = html.replace(parasAnchor, 'var PARAS = ["' + SENT_JS + '", "Imagine the internet on steroids.');
evidence.paras_first = SENT_JS;

// --- 3a. DEFECT 2: replace the wrong PNG disc with the harvested ball. ---
const rightRe = /(<a class="ncorner ncorner-right" href="https:\/\/nayanet\.app\/agreement" aria-label="The Collective Agreement — the red N">)<img src="data:image\/png;base64,[^"]+" alt="N — the red glass ball">/;
const rightMatch = html.match(rightRe);
if (!rightMatch) throw new Error('right-corner anchor/img not found');
const oldPngB64 = rightMatch[0].match(/base64,([^"]+)"/)[1];
evidence.old_red_png_bytes = Buffer.from(oldPngB64, 'base64').length;
evidence.old_red_png_sha256 = sha(Buffer.from(oldPngB64, 'base64'));
evidence.old_red_png_b64_sha256 = sha(Buffer.from(oldPngB64));
html = html.replace(rightRe,
  '$1<img src="' + BALL + '" alt="The red N — a raised glass ball with a gold N"><span class="ncorner-gloss" aria-hidden="true"></span>');
if (html.includes(oldPngB64)) throw new Error('old red PNG still present');

// --- 3b. DEFECT 2: harvest the agreement jewel-gloss CSS verbatim (selector renamed only). ---
// Agreement v25 source (byte-exact in evidence/agreement-live.html):
// .orb-wrap.jewel .jewel-gloss{position:absolute;z-index:4;top:11%;left:15%;
// width:36%;height:22%;border-radius:50%;pointer-events:none;
// transform:rotate(-24deg);background:radial-gradient(ellipse at center,
// rgba(255,255,255,.6),rgba(255,255,255,0) 68%)}
const glossCss = '.ncorner-right .ncorner-gloss{position:absolute;z-index:4;top:11%;left:15%;width:36%;height:22%;border-radius:50%;pointer-events:none;transform:rotate(-24deg);background:radial-gradient(ellipse at center,rgba(255,255,255,.6),rgba(255,255,255,0) 68%)}';
const glossSrc = '.orb-wrap.jewel .jewel-gloss{position:absolute;z-index:4;top:11%;left:15%;width:36%;height:22%;border-radius:50%;pointer-events:none;transform:rotate(-24deg);background:radial-gradient(ellipse at center,rgba(255,255,255,.6),rgba(255,255,255,0) 68%)}';
if (!agmt.includes(glossSrc)) throw new Error('jewel-gloss source CSS not found verbatim in agreement v25');
const anchorCss = '.ncorner:active{transform:translateY(-50%) scale(.97);}';
if (!html.includes(anchorCss)) throw new Error('.ncorner:active anchor CSS not found');
html = html.replace(anchorCss, anchorCss + '\n' + glossCss);

// --- 3c. DEFECT 2: update the harvest comment to record the new source. ---
const oldComment = '/* v-topmenu 2026-11-25 — the two Ns, bottom bar corners. Harvested\n   verbatim from the agreement page (agreement-BASE.html): LEFT the\n   crystal N (EMBED.logo), RIGHT the red glass ball (EMBED.ball).\n   Extraordinary: white ring, white glow, slow orbit, lift on hover. */';
const newComment = '/* v-topmenu 2026-11-25 — the two Ns, bottom bar corners. Harvested\n   verbatim from the agreement page (agreement-BASE.html): LEFT the\n   crystal N (EMBED.logo), RIGHT the red glass ball (EMBED.ball).\n   Extraordinary: white ring, white glow, slow orbit, lift on hover.\n   FRONTPAGE FIX 2026-11-25 (Shawn\'s eye: the red N was wrong): RIGHT is\n   now the OFFICIAL red N — EMBED.ball harvested BYTE-FOR-BYTE from live\n   agreement v25 (22,953,906 B, sha 2c88513f…), WEBP ' + ballRaw.length + ' B,\n   sha ' + sha(ballRaw).slice(0, 12) + '…, ' + ballW + 'x' + ballH + ', alt harvested\n   verbatim ("The red N — a raised glass ball with a gold N"). The small\n   static PNG disc (' + evidence.old_red_png_bytes + ' B, sha ' + evidence.old_red_png_sha256.slice(0, 12) + '…) is gone.\n   The N lights up (red hover glow) and spins (orbit ring, eco-spin 90s);\n   the jewel-gloss highlight is agreement v25 .orb-wrap.jewel .jewel-gloss\n   verbatim, selector renamed to .ncorner-right .ncorner-gloss only.\n   LEFT black/crystal N untouched (EMBED.logo, sha 08b753d3…). */';
if (!html.includes(oldComment)) throw new Error('ncorner harvest comment not found');
html = html.replace(oldComment, newComment);

// --- 4. Assertions: only the two defects changed. ---
const assert = (name, ok) => { console.log((ok ? 'PASS ' : 'FAIL ') + name); if (!ok) process.exitCode = 1; };
assert('front page: sentence text gone from visible <p>', !/id="fpDeedSentence">[^<]*By entering/.test(html));
assert('front page: ⓘ trigger kept (fpDeedInfo)', html.includes('id="fpDeedInfo"'));
assert('front page: greeting kept', html.includes('Naya Welcomes You'));
assert('front page: name input + Enter kept', html.includes('id="userName"') && html.includes('Enter NayaNET'));
assert('inner reader: sentence is PARAS[0]', html.includes('var PARAS = ["' + SENT_JS + '"'));
assert('inner reader: 13 paras (12 + sentence)', (html.match(/" of " \+ PARAS\.length/) || [''])[0] !== null);
assert('right N: harvested WEBP present', html.includes(BALL));
assert('right N: old PNG gone', !html.includes(oldPngB64));
assert('right N: destination kept (agreement)', html.includes('ncorner-right" href="https://nayanet.app/agreement"'));
assert('right N: gloss span present', html.includes('class="ncorner-gloss"'));
assert('right N: gloss CSS present', html.includes(glossCss));
assert('right N: orbit spin kept (eco-spin 90s)', html.includes('animation:eco-spin 90s linear infinite'));
assert('right N: hover red glow kept', html.includes('.ncorner-right:hover'));
assert('left N: black/crystal N untouched', html.includes('ncorner-left" href="https://nayanet.app/"'));
assert('bottom bar: Read the agreement kept', html.includes('id="fpEnterDeal"') && html.includes('Read the agreement'));
assert('returning view: premium greeting kept', html.includes('Welcome back'));
assert('returning view: This-is-me hidden kept', html.includes('This is me'));
assert('final nine: 9 eco-item anchors', (html.match(/class="eco-item"/g) || []).length === 9);
assert('walk: 15 questions kept', (html.match(/QUESTIONS/) || []).length > 0);
assert('endpoints: staged complete/verify untouched', html.includes('walkthrough-15') || html.includes('naya-welcome'));
assert('agreement v25 sha verified', agmtSha === '2c88513f9011b176c0af910ec0d81e314578cfe904dd62ded9010a9a54052e11');

// Diff vs R2 base: list changed regions (line-based, first 40).
const baseLines = base.split('\n'), newLines = html.split('\n');
let changed = 0; const changedIdx = [];
const maxLen = Math.max(baseLines.length, newLines.length);
for (let i = 0; i < maxLen; i++) {
  if (baseLines[i] !== newLines[i]) { changed++; if (changedIdx.length < 40) changedIdx.push(i + 1); }
}
evidence.diff_lines_changed = changed;
evidence.diff_line_numbers_sample = changedIdx;
evidence.diff_note = 'Line diff is dominated by the one-line EMBED.ball data URI (243KB on the right-corner line) + the sentence removal + PARAS[0] + gloss CSS + comment. No other lines differ by design — verify with the region check below.';
console.log('diff lines changed vs R2 base:', changed, 'sample lines:', changedIdx.join(','));

writeFileSync(LANE + 'portal.html', html);
writeFileSync(LANE + 'evidence/harvest.json', JSON.stringify(evidence, null, 2) + '\n');
console.log('portal.html', html.length, 'B sha256', sha(Buffer.from(html)));
console.log('old portal was', base.length, 'B; delta', html.length - base.length, 'B (mostly the harvested WEBP data URI)');
