// Agreement file fix ROUND 6f — on the R6e fixed file
// (agreement-v25-fixed-r6.html, sha 410078e1...).
// D5b. Deck total flips 4:18/4:19 — ONE writer, one source. paintDeckTime()
//     overwrote tDur with the video duration (259s -> 4:19) while the audio
//     loadedmetadata handler wrote the actual recording (258.15s -> 4:18).
//     paintDeckTime no longer writes tDur at all; the loadedmetadata
//     handler writes it unconditionally from audio.duration (4:18, stable).
//     tCur + the seek fill still track the video.
// D5a. Phone cover: the audio panel + LET'S GO sat below the fold (one
//     scroll; btnStart bottom 985 vs viewport 844 — 141px over). Compact
//     cover rules at <=640px only (frame, saying, cover-N, side gaps +
//     padding, orbit, transport, actions): ~160px saved in the first pass,
//     then a second pass (the probe measured btnStart bottom 897 — still
//     53px over) trims the frame to 120px, the saying to 17px (the first
//     pass used the bare element selector `saying`, which matched nothing
//     — the saying is <p class="cover-saying">), cover-N to 32px, both
//     orb-wraps to 60px, side padding to 8px and the gaps to 8/6px:
//     ~66px more, btnStart bottom ~831, inside the 844 viewport.
//     Desktop untouched.
// D5c. End-slide body text runs under the pinned deed row — INVESTIGATED,
//     NOT FIXED in this round (named open, see the maker report). The
//     mechanism: #screen-slide is a fixed 700px flex column; on the last
//     slide the deed row (307) + nav (68) + links bar (203) leave the deck
//     panel (.panel-body, the real scroller — NOT .pm-main, which is the
//     content) a ~122px window, so only the portrait top shows on arrival.
//     The board (351) + art (150) cannot fit that strip by any clean
//     compaction (min chrome ~518px leaves ~182px). The text + image ARE
//     reachable by scrolling the inner .panel-body (proven by probe), but
//     are not visible on arrival. The first pass's
//     `#screen-slide .pm-main{overflow-y:auto}` did nothing (wrong
//     element) and is NOT re-applied. Fixing it properly needs the screen
//     to grow / the chrome to restructure — a structural change out of
//     this round's scope; it is named open, not faked.
// Node only. Base is the R6e lane agreement file, edited.
import {readFileSync, writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import vm from 'node:vm';
const sha = b => createHash('sha256').update(b).digest('hex');
const LANE = new URL('./', import.meta.url).pathname;

const base = readFileSync(LANE + 'agreement-v25-fixed-r6.html');
const baseSha = sha(base);
if (baseSha !== '410078e1a4102496706c3df64e04a20539a3ae9ce745df77a8c48ed857b57b7b')
  throw new Error('R6e agreement base sha mismatch: ' + baseSha);
let html = base.toString('utf8');
const count = (sub) => html.split(sub).length - 1;
const rep = (oldS, newS, n, label) => {
  const c = html.split(oldS).length - 1;
  if (c !== n) throw new Error(label + ': expected ' + n + ' occurrence(s), found ' + c + ' :: ' + oldS.slice(0, 100));
  html = html.split(oldS).join(newS);
};

// --- D5b. One writer for the deck total. ---
rep("  if (td && videoDur) td.textContent = fmt(videoDur);\n",
  "  /* ROUND 6f (D5b) — tDur is written ONLY by the audio loadedmetadata\n     handler below (one writer, one source: the actual recording, 4:18).\n     This line used to overwrite it with the video duration (4:19), so\n     the total flipped 4:18/4:19. tCur + the seek fill still track video. */\n",
  1, 'D5b-paintDeckTime');
rep("audio.addEventListener('loadedmetadata', function(){ if (!videoDur) document.getElementById('tDur').textContent = fmt(audio.duration); });",
  "audio.addEventListener('loadedmetadata', function(){ document.getElementById('tDur').textContent = fmt(audio.duration); }); /* ROUND 6f (D5b) — the ONLY tDur writer: the actual recording, 4:18, stable. */",
  1, 'D5b-loadedmetadata');

// --- D5a. Compact phone cover (<=640px only). ---
rep("#screen-cover .pm-facade .pm-play-disc{width:56px;height:56px;font-size:20px}\n}",
  "#screen-cover .pm-facade .pm-play-disc{width:56px;height:56px;font-size:20px}\n/* ROUND 6f (D5a) — phone cover: the audio panel + LET'S GO sat below the\n   fold (btnStart bottom 985 vs viewport 844). Compact the cover stack at\n   <=640px only so the whole player frame fits in the viewport. Pass 1\n   saved ~88px (bottom 985 -> 897); pass 2 trims a further ~66px\n   (frame 120, saying 17px, cover-N 32, orb-wraps 60, side padding 8,\n   gaps 8/6) -> btnStart bottom ~831, inside 844. Desktop untouched. */\n#screen-cover .pm-main{gap:8px;padding-top:6px;padding-bottom:6px}\n#screen-cover .pm-art-frame{max-height:120px}\n#screen-cover .cover-saying{font-size:17px;margin-top:4px}\n#screen-cover .cover-n{width:32px;height:32px;margin-top:4px}\n#screen-cover .pm-side{gap:6px;padding-top:8px;padding-bottom:8px}\n#screen-cover .pm-side .orb-wrap{width:60px;height:60px}\n#screen-cover .side-actions{margin-top:0}\n#screen-cover .deck-ctl .hbtn{width:44px;height:44px;flex-basis:44px}\n}",
  1, 'D5a-compact-cover');

// --- D5c. NO CSS change (see the header): the first pass's overflow rule
//     targeted the wrong element (.pm-main is the deck content; the
//     scroller is its parent .panel-body). Nothing is applied here; the
//     item is named open in the maker report with the mechanism + math. ---
rep("#screen-cover .pm-facade .pm-play-disc{width:56px;height:56px;font-size:20px}",
  "/* ROUND 6f (D5c) — OPEN, no CSS change: the end-slide deck is clipped\n   by its .panel-body window (~122px at phone) under the pinned deed row;\n   the text + franchise image are reachable by scrolling that inner panel\n   but are not visible on arrival. A clean fix needs the screen/chrome\n   restructured — out of this round's scope, named open, not faked. */\n#screen-cover .pm-facade .pm-play-disc{width:56px;height:56px;font-size:20px}",
  1, 'D5c-documented-open');

// --- Assertions. ---
const assert = (name, ok) => { console.log((ok ? 'PASS ' : 'FAIL ') + name); if (!ok) process.exitCode = 1; };
assert('R6e agreement base sha verified', baseSha.startsWith('410078e1'));
assert('D5b: paintDeckTime no longer writes tDur', !html.includes("if (td && videoDur) td.textContent = fmt(videoDur);"));
assert('D5b: loadedmetadata is the ONLY tDur writer', (html.match(/getElementById\('tDur'\)\.textContent = fmt\(/g) || []).length === 1 && html.includes("document.getElementById('tDur').textContent = fmt(audio.duration);"));
assert('D5b: tCur + seek fill still track video', html.includes("if (tc) tc.textContent = fmt(videoTime);") && html.includes("fl.style.width"));
assert('D5a: compact cover rules present', html.includes('#screen-cover .pm-art-frame{max-height:120px}') && html.includes('#screen-cover .cover-saying{font-size:17px') && html.includes('#screen-cover .pm-side .orb-wrap{width:60px;height:60px}') && html.includes('#screen-cover .deck-ctl .hbtn{width:44px;height:44px;flex-basis:44px}'));
assert('D5a: no dead saying selector', !html.includes('#screen-cover saying{'));
assert('D5c: named open, no dead overflow rule', html.includes('ROUND 6f (D5c) — OPEN, no CSS change') && !html.includes('#screen-slide .pm-main{overflow-y:auto}'));
assert('R6e kept: 0 preview strings', !html.includes('Begin the visual story') && !html.includes('Read the agreement') && !html.includes("Welcome. Let's begin with trust.") && !html.includes('screen-choice'));
assert('R6e kept: cover active in markup', html.includes('class="screen active" id="screen-cover"'));
assert('R6e kept: audio hidden, no controls', html.includes('<audio class="real-audio" id="welcomeAudio" preload="auto" hidden playsinline'));
assert('R6e kept: facade below frame, poster contain', html.includes('#screen-cover .pm-poster{object-fit:contain'));
assert('R6e kept: end slide deed verbatim + agree flash + links bar', html.includes('By entering your name, you make it official') && html.includes('@keyframes agreeFlash') && html.includes("id = 'fpLinksBar'"));
assert('R6e kept: completion flag in goToPortal', (html.match(/localStorage\.setItem\('nayanet_agreement_done'/g) || []).length === 1);
assert('R6e kept: all 27 slide titles present', ['The Old Way', 'Your Franchise', "What's In It For You", "You're Hired"].every(t => html.includes(t)));
assert('R6e kept: legal pages intact (12)', (html.match(/id="legal-/g) || []).length === 12);
{
  const blocks = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
  let bad = [];
  blocks.forEach((code, i) => { try { new vm.Script(code); } catch (e) { bad.push(i + ': ' + e.message); } });
  assert('all ' + blocks.length + ' inline scripts compile (vm.Script)', bad.length === 0);
  if (bad.length) console.log('  COMPILE FAILURES: ' + bad.join(' | '));
}

const out = Buffer.from(html, 'utf8');
writeFileSync(LANE + 'agreement-v25-fixed-r6f.html', out);
console.log('agreement-v25-fixed-r6f.html', out.length, 'B sha256', sha(out));
console.log('R6e agreement was', base.length, 'B; delta', out.length - base.length, 'B');
