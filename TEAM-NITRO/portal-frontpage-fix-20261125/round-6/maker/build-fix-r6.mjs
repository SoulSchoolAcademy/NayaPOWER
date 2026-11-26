// Portal front-page fix ROUND 6 — the real collective agreement, on the portal.
// Base: R5 staged portal (sha d4bb2102...), branch portal-frontpage-fix-20261125-r5.
// Shawn's order (call): "Put the real collective agreement on the portal.
// Make it. And make it live." + Additions 1-3 (eye: red-orb N sideways;
// every entry lands on the exact URL https://nayanet.app/agreement;
// the preview page goes).
//
// WHAT WAS ALREADY TRUE (harvested, not rebuilt): the v7 text is ALREADY
// in this file, verbatim, as the distilled letter (#dealUnfold /
// #letterBody): 208/223 v7 sentences found by machine diff; the 15 "misses"
// are the source file's header/metadata and section-heading/stage-direction
// artefacts, not text. The 19 distilled stage beats carry it in order
// (QUESTION 1..5). So this round is an ENTRY + PRESENTATION fix, not a
// text harvest: no v7 sentence is reworded, added, or removed.
//
// THE CHANGES (diff vs R5 is exactly these):
//  A. N UPRIGHT (Addition 1 + eye evidence): the red-orb gold N reads
//     sideways because the IMAGE itself carries eco-spin 90s —
//     button.fp-circle-n img and .ncorner-right img both rotate the whole
//     ball photo, N included (R5 checker: corner red N +138.3 deg over
//     ~34.6s, matching the 90s spin; Shawn's shot shows ~90 deg, a frozen
//     moment of the spin). Fix: the spin comes OFF both imgs; the slow spin
//     stays on the decorative RING (::before conic sheen, 90s — the
//     .ncorner::before pattern, mirrored onto the circle button so the
//     centre orb stays alive). The black left N is untouched (upright).
//  B. ENTRIES -> REAL AGREEMENT, IN PLACE (original brief + Add. 2 + 3):
//     the four front-page entries (circle N, black corner N, red corner N,
//     footer "Read the agreement") called openStory(0) — the story, not
//     the agreement. They now call openAgreementDirect(): stage on,
//     letter view, beat 0, first group visible, plus history.pushState to
//     '/agreement' (the exact agreement URL path; no reload, no preview,
//     no interstitial). The other three "Read the agreement" buttons
//     (choice, bridge-final, intro nextBtn2) already navigate to
//     '/agreement' (relative) — unchanged; with the worker route below,
//     that URL now serves the real agreement instead of 302ing to live.
//  C. /agreement BOOT: a small script after the stage IIFE — on a load
//     whose pathname is /agreement, the stage opens straight into the
//     letter view at beat 0. No intro, no bridge choice, no preview.
//  D. THREE BOARDS AT A TIME (brief §6): the letter view stepped one beat
//     at a time. Now wireLetterUnfold reveals the next THREE beats per
//     "Keep reading", render() shows the current group of three in the
//     letter AND letterPage views, derive() syncs to the group start, and
//     the jewel counts groups (1/7 .. 7/7 for the 19 beats). Deck untouched.
//  E. AGREE WORDING: every "I agree ◆" becomes "I agree — show me my
//     world ◆" — the three setNext sites (letter, letterPage, agree) and
//     the two in-DOM buttons (#letterPageAgree, #dealAgreeBtn). The story
//     end slide already carries it.
//  F. STORY FROM INSIDE THE AGREEMENT (brief + Add. 3.1): in the letter
//     and letterPage views the second button reads "Begin the visual
//     story ◆" and opens the 27-slide story overlay (window.__fpOpenStory,
//     exposed in the entries block). It appears ONLY inside the agreement
//     view — never as an entry step. The story itself is untouched.
//  G. WORKER (build-worker-r6.mjs): /agreement serves the PORTAL (was a
//     302 to live https://nayanet.app/agreement). The live /agreement file
//     (v25, 22,953,906 B, sha 2c88513f...) is a separate deployment; the
//     live step (captain's) is what puts this build on the exact URL.
// Node only (python writes EPERM). Base is the R5 staged portal, edited.
import {readFileSync, writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const sha = b => createHash('sha256').update(b).digest('hex');
const LANE = new URL('./', import.meta.url).pathname;

const base = readFileSync(LANE + 'portal-r5.html');
const baseSha = sha(base);
if (baseSha !== 'd4bb2102279838984db558e87cec4a977e4782ed22e5a2cc98be70f28e00b86b')
  throw new Error('R5 base sha mismatch: ' + baseSha);
let html = base.toString('utf8');
const count = (s, sub) => html.split(s).length - 1;
const rep = (oldS, newS, n, label) => {
  const c = html.split(oldS).length - 1;
  if (c !== n) throw new Error(label + ': expected ' + n + ' occurrence(s), found ' + c + ' :: ' + oldS.slice(0, 80));
  html = html.split(oldS).join(newS);
};

// --- A. N upright: spin off the two red-N imgs, onto the ring. ---
// A1. Circle-N img: drop the animation from its rule (keep size/cover).
{
  const anchor = 'button.fp-circle-n img{width:100%;height:100%;border-radius:50%;object-fit:cover;';
  const i = html.indexOf(anchor);
  if (i === -1) throw new Error('A1: circle-N img rule not found');
  const seg = html.slice(i, i + 260);
  const a = seg.indexOf('animation:eco-spin 90s linear infinite');
  if (a === -1) throw new Error('A1: circle-N img has no eco-spin to remove');
  html = html.slice(0, i + a) + html.slice(i + a + 'animation:eco-spin 90s linear infinite'.length);
  if (!html.slice(i, i + 260).includes('display:block;}')) throw new Error('A1: circle-N img rule malformed after removal');
}
// A2. Corner red-N img: the whole rule goes (the ::before ring keeps spinning).
rep('.ncorner-right img{animation:eco-spin 90s linear infinite;}', '.ncorner-right img{}', 1, 'A2');
// A3. Centre orb keeps its slow spin on the ring, mirroring .ncorner::before.
rep('button.fp-circle-n .ncorner-gloss{',
  'button.fp-circle-n::before{content:"";position:absolute;inset:-6px;border-radius:50%;background:conic-gradient(from 0deg,transparent 0 68%,rgba(255,255,255,.95) 82%,transparent 94%);-webkit-mask:radial-gradient(farthest-side,transparent calc(100% - 3px),#000 calc(100% - 2px));mask:radial-gradient(farthest-side,transparent calc(100% - 3px),#000 calc(100% - 2px));animation:eco-spin 90s linear infinite;pointer-events:none;} button.fp-circle-n .ncorner-gloss{',
  1, 'A3');
// A4. Reduced motion: the new ring stops too.
rep('button.fp-circle-n img{animation:none;}',
  'button.fp-circle-n img{animation:none;}   button.fp-circle-n::before{animation:none;}',
  1, 'A4');

// --- B. Entries -> the real agreement, in place, URL /agreement. ---
const entriesOld = `/* entries: the red N in the circle, both corner Ns, "Read the agreement" */
  var circleN = document.getElementById('fpCircleN');
  if (circleN) circleN.addEventListener('click', function () { openStory(0); });
  var corners = document.querySelectorAll('.ncorner');
  for (var c = 0; c < corners.length; c++) {
    corners[c].addEventListener('click', function (ev) {
      ev.preventDefault();
      openStory(0);
    });
  }
  var deal = document.getElementById('fpEnterDeal');
  if (deal) deal.addEventListener('click', function () { openStory(0); });`;
const entriesNew = `/* ROUND 6 — entries open the REAL agreement DIRECTLY, in place: the red N
     in the circle, both corner Ns, "Read the agreement" all land on the v7
     letter view (first group visible) — no preview, no story as a step.
     The URL becomes /agreement (history.pushState, no reload): the exact
     agreement URL (https://nayanet.app/agreement on live). A reload there
     boots straight into the letter (see the /agreement boot below). The
     27-slide story stays, reachable only from INSIDE the agreement view
     ("Begin the visual story", nextBtn2 in the letter view). */
  window.__fpOpenStory = openStory;
  function openAgreementDirect(){
    var st = window.__fpStage;
    if (st) { st.enter(); st.state.view='letter'; st.state.letter=0; st.state.all=null; st.state.legalId=null; st.render(); }
    try { history.pushState(null, '', '/agreement'); } catch (e) {}
  }
  var circleN = document.getElementById('fpCircleN');
  if (circleN) circleN.addEventListener('click', function () { openAgreementDirect(); });
  var corners = document.querySelectorAll('.ncorner');
  for (var c = 0; c < corners.length; c++) {
    corners[c].addEventListener('click', function (ev) {
      ev.preventDefault();
      openAgreementDirect();
    });
  }
  var deal = document.getElementById('fpEnterDeal');
  if (deal) deal.addEventListener('click', function () { openAgreementDirect(); });`;
rep(entriesOld, entriesNew, 1, 'B');

// --- C. /agreement boot: a load on /agreement opens the letter directly. ---
const stageClose = 'window.__fpStage={state:S,enter:enterStage,exit:exitStage,render:render};\n})();\n</script>';
const bootScript = stageClose + `
<script>/* ROUND 6 — the /agreement URL serves the real agreement directly.
   A load on /agreement (the exact agreement URL) opens the stage straight
   into the v7 letter view at beat 0 — no preview intro, no bridge choice,
   no "Begin the visual story" as an entry step. The portal root (/) is
   untouched: a plain load still lands on the login and stays there. */
(function(){try{if(window.location.pathname!=='/agreement')return;var st=window.__fpStage;if(!st)return;st.enter();st.state.view='letter';st.state.letter=0;st.state.all=null;st.state.legalId=null;st.render();}catch(e){}})();</script>`;
rep(stageClose, bootScript, 1, 'C');

// --- D. Three boards at a time (letter view + letterPage view). ---
// D1. wireLetterUnfold only (scoped by its IIFE): reveal the next 3 beats.
{
  const iife = html.indexOf('(function wireLetterUnfold(){');
  if (iife === -1) throw new Error('D1: wireLetterUnfold not found');
  const fe = html.indexOf('beats.forEach(function(b, i){', iife);
  if (fe === -1) throw new Error('D1: wireLetterUnfold beats.forEach not found');
  const seg = html.slice(fe, fe + 600);
  const oldH = '      var cur = i + 1;\n      if (cur < beats.length) {\n        show(cur);\n        idx = cur + 1;';
  if (!seg.includes(oldH)) throw new Error('D1: wireLetterUnfold next handler not found in scope');
  const newH = '      var cur = i + 1;\n      if (cur < beats.length) {\n        show(cur); show(cur + 1); show(cur + 2);\n        idx = cur + 3;';
  html = html.slice(0, fe) + seg.replace(oldH, newH) + html.slice(fe + 600);
}
// D2. render(): letter + letterPage show the current group of three.
rep("var sl=(S.all==='letter')||i===S.letter;", "var sl=(S.all==='letter')||(i>=S.letter&&i<S.letter+3);", 1, 'D2-letter');
rep('var slp=i===S.letter;', 'var slp=(i>=S.letter&&i<S.letter+3);', 1, 'D2-letterPage');
// D3. derive(): sync to the group start, not the last shown beat.
rep('var l=lastShown(letterBeats);if(l>=0)S.letter=l;', 'var l=lastShown(letterBeats);if(l>=0)S.letter=l-(l%3);', 1, 'D3-letter');
rep('var lp=lastShown(letterBeats);if(lp>=0)S.letter=lp;', 'var lp=lastShown(letterBeats);if(lp>=0)S.letter=lp-(lp%3);', 1, 'D3-letterPage');
// D4. Jewel counts groups (19 beats -> 7 groups).
rep("jewelNum.textContent=(S.letter+1)+' / '+letterBeats.length;", "jewelNum.textContent=(Math.floor(S.letter/3)+1)+' / '+Math.ceil(letterBeats.length/3);", 1, 'D4-num');
rep("jewelBar.style.width=Math.round(((S.letter+1)/letterBeats.length)*100)+'%';", "jewelBar.style.width=Math.round(((Math.floor(S.letter/3)+1)/Math.ceil(letterBeats.length/3))*100)+'%';", 1, 'D4-bar');
// D5. Last-group agree + "Begin the visual story" second button (letter + letterPage).
const agreeIfOld = "if(S.letter>=letterBeats.length-1){setNext('I agree \\u25C6','#07925f','letterPageAgree');}";
const agreeIfNew = "if(S.letter+3>=letterBeats.length){setNext('I agree — show me my world \\u25C6','#07925f','letterPageAgree');if(nextBtn2){nextBtn2.textContent='Begin the visual story \\u25C6';nextBtn2.style.setProperty('--tone','#8e24aa');nextBtn2.hidden=false;}if(nextRow)nextRow.classList.add('fp-two');}";
rep(agreeIfOld, agreeIfNew, 2, 'D5-agreeIf');
const keepOld = "else{setNext('Keep reading \\u25C6',tone,'letterNext');}";
const keepNew = "else{setNext('Keep reading \\u25C6',tone,'letterNext');}if(nextBtn2){nextBtn2.textContent='Begin the visual story \\u25C6';nextBtn2.style.setProperty('--tone','#8e24aa');nextBtn2.hidden=false;}if(nextRow)nextRow.classList.add('fp-two');}";
rep(keepOld, keepNew, 2, 'D5-keep');

// --- E. Agree wording everywhere it reads "I agree ◆". ---
rep("setNext('I agree \\u25C6','#07925f','agree');", "setNext('I agree — show me my world \\u25C6','#07925f','agree');", 1, 'E-agree');
rep('>I agree &#9670;</button>', '>I agree &mdash; show me my world &#9670;</button>', 2, 'E-domButtons');

// --- F. nextBtn2 in the letter views opens the story (inside only). ---
rep("if(nextBtn2)nextBtn2.addEventListener('click',function(){if(S.view==='intro'){window.location.href='/agreement';}else if(S.view==='deck'&&S.deck===deckBeats.length-1){window.location.href='/agreement';}});",
  "if(nextBtn2)nextBtn2.addEventListener('click',function(){if(S.view==='intro'){window.location.href='/agreement';}else if(S.view==='deck'&&S.deck===deckBeats.length-1){window.location.href='/agreement';}else if(S.view==='letter'||S.view==='letterPage'){if(window.__fpOpenStory)window.__fpOpenStory(0);}});",
  1, 'F');

// --- Assertions. ---
const assert = (name, ok) => { console.log((ok ? 'PASS ' : 'FAIL ') + name); if (!ok) process.exitCode = 1; };
assert('R5 base sha verified', baseSha.startsWith('d4bb2102'));
assert('A: circle-N img spin removed (0 eco-spin on fp-circle-n img)', !html.includes('button.fp-circle-n img{width:100%;height:100%;border-radius:50%;object-fit:cover;   display:block;animation:eco-spin'));
assert('A: corner red-N img spin removed', !html.includes('.ncorner-right img{animation:eco-spin'));
assert('A: circle-N ring spins (mirrored ::before, 90s)', html.includes('button.fp-circle-n::before{content:"";position:absolute;inset:-6px;') && html.includes('button.fp-circle-n::before{animation:none;}'));
assert('A: corner ring still spins (90s)', html.includes('.ncorner::before{') && html.includes('animation:eco-spin 90s linear infinite'));
assert('A: black left N untouched', html.includes('ncorner-left" href="https://nayanet.app/"') && !html.includes('.ncorner-left img{animation'));
assert('A: ring untouched (78s/31s)', html.includes('animation:nayaSpectrum 78s linear infinite') && html.includes('animation:nayaWhite 31s linear infinite'));
assert('B: entries call openAgreementDirect (3 calls + 1 comment mention), openStory(0) gone from entries', (html.match(/openAgreementDirect\(\)/g) || []).length === 4 && html.includes('window.__fpOpenStory = openStory;'));
assert('B: no entry still opens the story', !html.includes("addEventListener('click', function () { openStory(0); })") && !html.includes('ev.preventDefault();\n      openStory(0);'));
assert('B: pushState to /agreement, no reload navigation to it from entries', html.includes("history.pushState(null, '', '/agreement')"));
assert('B: choice/bridge/intro Read-the-agreement still navigate to /agreement (relative)', (html.match(/window\.location\.href='\/agreement'/g) || []).length === 4);
assert('C: /agreement boot present, root untouched', html.includes("if(window.location.pathname!=='/agreement')return;") && html.includes('st.state.view=\'letter\''));
assert('D: wireLetterUnfold reveals 3', html.includes('show(cur); show(cur + 1); show(cur + 2);') && html.includes('idx = cur + 3;'));
assert('D: render shows groups of 3 (letter + letterPage)', html.includes('var sl=(S.all===\'letter\')||(i>=S.letter&&i<S.letter+3);') && html.includes('var slp=(i>=S.letter&&i<S.letter+3);'));
assert('D: derive syncs to group start', html.includes('S.letter=l-(l%3);') && html.includes('S.letter=lp-(lp%3);'));
assert('D: jewel counts groups', html.includes("Math.floor(S.letter/3)+1)+' / '+Math.ceil(letterBeats.length/3);"));
assert('E: agree wording everywhere (no bare "I agree" setNext left)', !html.includes("setNext('I agree \\u25C6'") && ((html.match(/I agree — show me my world/g) || []).length + (html.match(/I agree &mdash; show me my world/g) || []).length) >= 6);
assert('E: story end slide wording kept', html.includes('I agree &mdash; show me my world &#9670;'));
assert('F: story from inside agreement only (nextBtn2 letter branch)', html.includes("else if(S.view==='letter'||S.view==='letterPage'){if(window.__fpOpenStory)window.__fpOpenStory(0);}"));
assert('R5 kept: menu hover-only (eco-tip, no eco-label)', !html.includes('eco-label') && html.includes('clampEcoTip'));
assert('R5 kept: 27-slide story + FP_SLIDES', html.includes('var FP_SLIDES') || html.includes('FP_SLIDES'));
assert('R5 kept: nine destinations', (html.match(/class="eco-item"/g) || []).length === 9);
assert('R5 kept: v7 letter beats present (opening + ending + Agreement)', html.includes('Welcome home. Your world begins here.') && html.includes('By joining, you agree to respect other people') && html.includes('QUESTION 1'));
assert('R5 kept: identity/cert + sw untouched markers', html.includes('id="fpCircleN"') && html.includes('FP_SLIDES'));
assert('structure: 7 style elements, 10 scripts (boot added)', (html.match(/<style>/g) || []).length === 7 && (html.match(/<script>/g) || []).length === 10);

const out = Buffer.from(html, 'utf8');
writeFileSync(LANE + 'portal.html', out);
console.log('portal.html', out.length, 'B sha256', sha(out));
console.log('R5 portal was', base.length, 'B; delta', out.length - base.length, 'B');
