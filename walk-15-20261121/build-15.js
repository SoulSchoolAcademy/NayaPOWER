#!/usr/bin/env node
/* Walk 15 — framed, 15 questions + showcase. Build from fd38de47.
   Base: walk-q2-whats-your-thing-20261113/walk-beginning-fixed.html
   Harvests (verified first-hand in this round):
   - Frame: agreement blob 1f0b04747e3315be6f1b619c1411e5e14fbdc1bb (142,532 B,
     sha256 a3b3907f2f80d09a14c1e7e8bfb7a00c63332a7b26ac2707912c39436e177b98,
     API == local file) L340-348, via about-sean.html (same lineage).
   - PowerCast: Personal fix tip f04a783c, blob 50867d86f31ce8b25b454fd40b9deec3eebb4545,
     fetched fresh from the staged host; .powercast-topbtn CSS L5644-5676,
     #saTheatre shell CSS L36863,64,66,67, saPcSync state strings L42435-42437.
     (Staged fetch: 10,517,420 B, sha 0b4fb0f5... — +79 B vs the filed blob:
     the host serves the branch tip, which has moved since R5. Line numbers
     verified against the brief's L41451-41460 / L36991 anchors.)
   - Questions 1/2/3/4/7/10/11 A/B/C + eyes: harvested verbatim from the base file.
   Everything else is DRAFTED (flagged in WALK-15-REPORT.md).
   Fails loud on any missed anchor. Writes in 8KB chunks, verifies size+sha.
   NOTE: write this file ONLY with the file tool — python open('w') truncated
   it to 0 bytes under the EPERM flake (2026-11-21 21:01Z); rewritten after.
*/
const fs = require('fs');
const crypto = require('crypto');
const { execSync } = require('child_process');
const LANE = '/home/hatch/workspace/team-nitro/walk-q2-whats-your-thing-20261113';
const BASE_P = LANE + '/walk-beginning-fixed.html';
const OUT_P = process.env.WALK15_OUT || (LANE + '/walk-beginning-fixed-15.html');
const AGREE_P = '/home/hatch/workspace/team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html';
const PERSONAL_URL = 'https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO%2Fpersonal-page-complete-20261113%2Fpersonal-complete.html&ref=personal/universal-bar-20261121&cb=50867d86f31ce8b25b454fd40b9deec3eebb4545';

function sha256(b) { return crypto.createHash('sha256').update(b).digest('hex'); }
function gitBlobSha(raw) { return crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob ' + raw.length + '\0'), raw])).digest('hex'); }
function repOnce(s, old, nw, label) {
  const n = s.split(old).length - 1;
  if (n !== 1) throw new Error(label + ': anchor occurs ' + n + 'x (want 1): ' + JSON.stringify(old.slice(0, 90)));
  return s.replace(old, nw);
}
function esc(t) { return t.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

/* ---------- the locked 15 + showcase ---------- */
const Q = [
 { n: 1, key: 'motto', from: 'motto',
   heading: '"What\'s your motto — the one line that says who you are?"',
   dict: "Click the button and tell us your motto", foc: "Type in what your motto is" },
 { n: 2, key: 'vision', from: 'vision',
   heading: '"What\'s your vision — the world you want to see?"',
   dict: "Click the button and tell us your vision", foc: "Type in what your vision is" },
 { n: 3, key: 'goal', from: 'goal',
   heading: '"What\'s your goal — what are you working toward?"',
   dict: "Click the button and tell us your goal for your life", foc: "Type in your goal for your life" },
 { n: 4, key: 'mission', from: 'mission',
   heading: '"What\'s your mission — what are you here to do?"',
   dict: "Click the button and tell us your mission", foc: "Type in what your mission is" },
 { n: 5, key: 'love', from: null,
   heading: '"What do you love?"',
   dict: "Click the button and tell us what you love", foc: "Type in what you love",
   abc: [
    "I love music — the songs I love and the artists I play over and over. Because nobody should feel alone in the thing they love, and my music is how my people find me.",
    "I love the moment two like minds find each other across the world and realize they were never alone.",
    "I love building worlds — with wisdom, intelligence, integrity, love, care, intention, and detail — and making those worlds connect." ] },
 { n: 6, key: 'dont', from: null,
   heading: '"What don\'t you love — what do you want less of?"',
   dict: "Click the button and tell us what you don't love", foc: "Type in what you don't love",
   abc: [
    "I don't love feeling alone in the thing you love — nobody should.",
    "I don't love the searching and the friending — the system should do the finding, so you can just talk.",
    "I don't love a page that makes you do the thinking — it should all be done for you." ] },
 { n: 7, key: 'thing', from: 'into',
   heading: '"What\'s your thing — the one thing that\'s yours?"',
   dict: "Click the button and tell us what your thing is", foc: "Type in what your thing is, and what you love to do" },
 { n: 8, key: 'values', from: null,
   heading: '"What do you value — what matters most to you?"',
   dict: "Click the button and tell us what you value", foc: "Type in what you value",
   abc: [
    "I value wisdom, intelligence and integrity — and love, care, intention and detail in everything I build.",
    "Do it for them. Ten stars, or don't send it.",
    "I value the person at the centre — everything orbits them, and the page serves them first." ] },
 { n: 9, key: 'laws', from: null,
   heading: '"What laws do you follow — the rules you live by?"',
   dict: "Click the button and tell us the laws you follow", foc: "Type in the laws you follow",
   abc: [
    "Just because I can doesn't mean I should — I check the destination before the road, I serve the whole, and I give ten stars, always.",
    "Do no harm to yourself or others, because all is you and connected to you.",
    "I think before I act. I scorecard my choices and do the highest. I prove it before I report it. I never waver." ] },
 { n: 10, key: 'declaration', from: 'about',
   heading: '"Your declaration — who are you, in your own words?"',
   dict: "Click the button and tell us who you are", foc: "Type in who you are, in your own words" },
 { n: 11, key: 'offer', from: 'biz_offer',
   heading: '"What do you offer?"',
   dict: "Click the button and tell us what you offer", foc: "Type in what you offer" },
 { n: 12, key: 'helps', from: null,
   heading: '"How does it help them — what does it do for them?"',
   dict: "Click the button and tell us how it helps them", foc: "Type in how it helps them",
   abc: [
    "It gives them their world, organized — their people, their pages, their notes, their mail, their business — all in one place, all working together.",
    "They don't have to search or friend anyone — the system does the work, math finds the like minds, and they can talk instantly.",
    "It gives them 10-star service in everything they touch — push-button simple, done for them." ] },
 { n: 13, key: 'moment', from: null,
   heading: '"Tell me a moment you\'ve done it — a time it worked."',
   dict: "Click the button and tell us about a moment you've done it", foc: "Type in a moment you've done it",
   abc: [
    "The moment two like minds found each other across the world and realized they were never alone — that was the whole thing working.",
    "The first time a citizen saw their whole world, made — their words, in the right places, on their own page.",
    "Every time someone says they found their people — and they did, because the page did the finding." ] },
 { n: 14, key: 'howwork', from: null,
   heading: '"How do you work — how does someone work with you?"',
   dict: "Click the button and tell us how you work", foc: "Type in how you work",
   abc: [
    "You tell me in your own words — or speak it, or paste it from your AI — and I do the rest, done for you.",
    "One click, push-button simple — I operate it for you, you live it.",
    "We build it together, live — you answer, the page fills, and your world arrives made." ] },
 { n: 15, key: 'start', from: null,
   heading: '"How does someone start with you — what\'s the first step?"',
   dict: "Click the button and tell us how someone starts with you", foc: "Type in how someone starts with you",
   abc: [
    "Tap Enter, name your world, and you're in — your pages arrive made.",
    "Say hello — tell me your thing, and I'll show you your people.",
    "Join free — answer the walk, claim your Smart Name, and start building." ] },
];
const SHOWCASE = { n: 16, key: 'showcase',
  heading: '"Would you like to showcase any of your experiences — things you have accomplished, certificates, awards — or just share something unique to you?"',
  dict: "Click the button and tell us what you'd like to showcase", foc: "Type in what you'd like to showcase" };

const EYES_DRAFTED = {
 love: [
  ["Naya's warm & plain voice — music, and why it matters.", "Love is the signal: it tells people what your world is for.", "It fills your Personal page — What I love.", "People who love the same thing recognize you at once."],
  ["Naya's bold & short voice — the moment, in one line.", "One moment says the whole of what you love.", "It fills your Personal page — What I love.", "People feel it at once — and want in."],
  ["Naya's full & visionary voice — building worlds.", "It gives the whole picture: the love behind the work.", "It fills your Personal page — What I love.", "People see the depth — and want to know more."] ],
 dont: [
  ["Naya's warm & plain voice — what she won't accept.", "Saying what you don't love is how people trust what you do love.", "It fills your Personal page — What I don't.", "People know where you stand."],
  ["Naya's bold & short voice — no searching, no friending.", "Short and certain: the system does the finding.", "It fills your Personal page — What I don't.", "People feel the promise at once."],
  ["Naya's full & visionary voice — done for you.", "It names the standard: nothing that makes you do the thinking.", "It fills your Personal page — What I don't.", "People relax — the work is done for them."] ],
 values: [
  ["Naya's warm & plain voice — what she holds to.", "Values are the filter: every choice runs through them.", "It fills your Personal page — Values.", "People trust someone whose values they can see."],
  ["Naya's bold & short voice — ten stars, or don't send it.", "The shortest true version of the whole standard.", "It fills your Personal page — Values.", "People quote it — and quote you with it."],
  ["Naya's full & visionary voice — the person at the centre.", "It says who the page is for: the person, first.", "It fills your Personal page — Values.", "People feel served, not sold to."] ],
 laws: [
  ["Naya's warm & plain voice — check the destination first.", "A law you can be measured by, in one breath.", "It fills your Personal page — Laws you follow.", "People know exactly how you decide."],
  ["Naya's bold & short voice — do no harm.", "The law of one, in one line.", "It fills your Personal page — Laws you follow.", "People feel safe with you."],
  ["Naya's full & visionary voice — think, scorecard, prove.", "It is the whole protocol: think before acting, prove before reporting.", "It fills your Personal page — Laws you follow.", "People trust a mind that proves itself."] ],
 helps: [
  ["Naya's warm & plain voice — your world, organized.", "Help should list what they get, plainly.", "It fills your Skills — how it helps.", "People can say yes without asking what it is."],
  ["Naya's bold & short voice — no searching, no friending.", "Three beats: the system finds, the math matches, they talk.", "It fills your Skills — how it helps.", "People see one thing to join, not ten things to learn."],
  ["Naya's full & visionary voice — ten stars, done for you.", "It sells the service, not the effort.", "It fills your Skills — how it helps.", "People feel the ease before they feel the price."] ],
 moment: [
  ["Naya's warm & plain voice — the moment it worked.", "A moment is proof you can feel, not a claim.", "It fills your Skills — a moment you've done it.", "People believe a moment before they believe a promise."],
  ["Naya's bold & short voice — the world, made.", "One picture: the page arriving finished.", "It fills your Skills — a moment you've done it.", "People want the same picture for themselves."],
  ["Naya's full & visionary voice — finding their people.", "It promises the meeting, not the hunt.", "It fills your Skills — a moment you've done it.", "People arrive already belonging."] ],
 howwork: [
  ["Naya's warm & plain voice — tell me, and I do the rest.", "It says how working together feels: easy.", "It fills your Skills — how you work.", "People hear 'done for you' and relax."],
  ["Naya's bold & short voice — one click, you live it.", "The shortest true version of the whole job.", "It fills your Skills — how you work.", "People get it in one breath."],
  ["Naya's full & visionary voice — built together, live.", "It shows the build happening as you answer.", "It fills your Skills — how you work.", "People trust work that is proven, not claimed."] ],
 start: [
  ["Naya's warm & plain voice — tap Enter, and you're in.", "A first step should take seconds, not courage.", "It fills your Skills — how to start.", "People start now, not someday."],
  ["Naya's bold & short voice — say hello.", "The smallest possible first step.", "It fills your Skills — how to start.", "People feel welcome at once."],
  ["Naya's full & visionary voice — join free, claim your name.", "It names the whole road: walk, name, build.", "It fills your Skills — how to start.", "People see where the road goes — and walk it."] ],
};
const TALK_GUIDE = "Pick the style you like — A, B, or C. Make it yours — tap EDIT and change the words. Then press Enter, and it becomes your answer.";
const TALK_GUIDE_SHOWCASE = "Share anything you like — or skip. Blank stays hidden: nothing shows on your page until you fill it in.";
const CUSTOM_WAYS_NEW = ["Edit, clear, or dictate it — make it your own.", "Copy-paste from your AI — have it write it for you.", "Just write in what you want — or skip."];

/* ---------- read + verify base ---------- */
const baseBuf = fs.readFileSync(BASE_P);
const baseSha = sha256(baseBuf);
if (baseSha !== 'fd38de479d17d6ce51ae33a7667b9b5458eb6a743df626282a187d2cbe13e836') throw new Error('base sha moved — STOP: ' + baseSha);
if (baseBuf.length !== 3364312) throw new Error('base size moved — STOP: ' + baseBuf.length);
let s = baseBuf.toString('utf8');

/* ---------- frame harvest: agreement L340-348 from the local file (API-verified) ---------- */
const agreeBuf = fs.readFileSync(AGREE_P);
if (sha256(agreeBuf) !== 'a3b3907f2f80d09a14c1e7e8bfb7a00c63332a7b26ac2707912c39436e177b98') throw new Error('agreement file sha moved — STOP');
const agreeLines = agreeBuf.toString('utf8').split('\n');
const frameLines = agreeLines.slice(339, 348); // L340-348
if (!frameLines[0].startsWith('.naya-frame{position:fixed;inset:0;z-index:60;pointer-events:none;')) throw new Error('agreement L340 anchor moved');
if (!frameLines[8].startsWith('@keyframes frameLight{')) throw new Error('agreement L348 anchor moved');
if (!frameLines[4].includes('THE FLOWING LIGHT')) throw new Error('agreement L344 comment anchor moved');
const frameCss = frameLines.join('\n');

/* ---------- PowerCast harvest: fetch Personal bytes fresh, extract by line ---------- */
const personal = execSync('curl -sL --max-time 120 "' + PERSONAL_URL + '" -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"', { maxBuffer: 32 * 1024 * 1024 }).toString('utf8');
const pl = personal.split('\n');
console.log('personal fetch: bytes=' + Buffer.byteLength(personal) + ' lines=' + pl.length + ' sha256=' + sha256(Buffer.from(personal)));
function pline(n, anchor) {
  const l = pl[n - 1];
  if (l === undefined || !l.includes(anchor)) throw new Error('personal L' + n + ' anchor moved: want ' + JSON.stringify(anchor) + ' got ' + JSON.stringify((l || '').slice(0, 120)));
  return l;
}
pline(5644, '.powercast-topbtn{');
pline(5676, '@media (max-width:560px){ .powercast-topbtn{');
pline(36861, '#saTheatre{position:fixed;inset:0;');
pline(36863, '.sa-theatre-bar{');
pline(36867, '.sa-theatre-body{');
pline(36991, '<div id="saTheatre" hidden');
pline(41452, 'PowerCast player');
pline(42437, "On air — playing");
if (!personal.includes('▶ Play') || !personal.includes('❚❚ Pause') || !personal.includes("saPcSync")) throw new Error('saPcSync state strings missing');
const pcTopBtnCss = pl.slice(5643, 5676).join('\n'); // L5644-5676
const saShellCss = [pl[36862], pl[36863], pl[36865], pl[36866]].join('\n'); // .sa-theatre-bar, .sa-theatre-bar .ph-connect, .sa-theatre-sp, .sa-theatre-body (L36863,64,66,67)
/* NOTE: the #saTheatre fixed full-screen rule (L36861) is NOT copied — the walk panel is inline, not fullscreen. */

/* ---------- old data: choice texts + eyes ---------- */
function oldChoice(n, letter) {
  const m = s.match(new RegExp('id="choice-' + n + '-' + letter + '"[^>]*>([\\s\\S]*?)</textarea>'));
  if (!m) throw new Error('old choice ' + n + letter + ' missing');
  return m[1];
}
const oldEyesM = s.match(/var CHOICE_EYES = (\{[\s\S]*?\});\n/);
if (!oldEyesM) throw new Error('CHOICE_EYES line missing');
const oldEyes = JSON.parse(oldEyesM[1]);
const OLD_STEP = { about: 1, into: 2, vision: 3, mission: 4, motto: 5, goal: 6, biz_do: 7, biz_offer: 8, biz_building: 9, space: 10 };
const oldAbc = {};
for (const [k, n] of Object.entries(OLD_STEP)) oldAbc[k] = ['A', 'B', 'C'].map(L => oldChoice(n, L));

/* ---------- template: step-5 section ---------- */
const tm = s.match(/<section class="p3-step p3-qstep" id="step-5" data-key="motto" hidden>[\s\S]*?<\/section>/);
if (!tm) throw new Error('step-5 template missing');
const TPL = tm[0];
if (TPL.split('id="step-5"').length - 1 !== 1) throw new Error('template step id anchor');
for (const a of ['p3-choice-eye', 'p3-custom-q', 'id="answer-5"', 'id="speakBtn-5"', 'id="skipBtn-5"', 'id="enterBtn-5"', '5 of 10']) {
  if (!TPL.includes(a)) throw new Error('template missing mechanic: ' + a);
}

function talkPanel(n, shortLabel, photoIdx) {
  return [
    '<div class="p3-talk" id="talk-' + n + '">',
    '<div class="sa-theatre-bar"><span class="p3-talk-title">Naya speaks — ' + shortLabel + '</span><span class="sa-theatre-sp"></span><span class="p3-talk-state" id="talkState-' + n + '">Paused</span></div>',
    '<div class="sa-theatre-body"><img class="p3-talk-photo" data-photo="' + photoIdx + '" src="" alt="Naya"><span class="p3-talk-bars" id="talkBars-' + n + '" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></span></div>',
    '<p class="p3-talk-words">Tap play — Naya speaks this question.</p>',
    '<button class="powercast-topbtn p3-talk-play" id="talkPlay-' + n + '" type="button" aria-label="Play — Naya speaks this question">▶ Play</button>',
    '</div>'
  ].join('\n');
}
const WAYS_LINE = '<p class="p3-answer-ways"><b>A</b> — click edit, make it your own, dictate or type in · <b>B</b> — have your AI write it for you, copy-paste it in · or skip.</p>';

function buildStep(q) {
  const n = q.n, key = q.key, photo = (n - 1) % 5;
  let t = TPL;
  t = repOnce(t, 'id="step-5"', 'id="step-' + n + '"', 'step id ' + n);
  t = repOnce(t, 'data-key="motto"', 'data-key="' + key + '"', 'step key ' + n);
  t = repOnce(t, 'data-top="5"', 'data-top="' + n + '"', 'step top ' + n);
  t = repOnce(t, 'data-photo="4"', 'data-photo="' + photo + '"', 'step photo ' + n);
  t = t.split('-5"').join('-' + n + '"');
  t = t.split('"5-').join('"' + n + '-');
  t = t.split('-5-').join('-' + n + '-');
  if (n !== 5 && (t.includes('-5"') || t.includes('"5-') || t.includes('-5-'))) throw new Error('step ' + n + ': leftover -5 refs');
  t = repOnce(t, '<h1 class="p3-question">"What is your motto?"</h1>', '<h1 class="p3-question">' + q.heading + '</h1>', 'heading ' + n);
  const abc = q.abc || oldAbc[q.from];
  for (let i = 0; i < 3; i++) {
    const L = 'ABC'[i];
    const old = oldAbc.motto[i];
    if (!t.includes('id="choice-' + n + '-' + L + '" rows="2" readonly>' + old + '</textarea>')) throw new Error('choice anchor ' + n + L + ' moved');
    t = t.replace('id="choice-' + n + '-' + L + '" rows="2" readonly>' + old + '</textarea>',
      'id="choice-' + n + '-' + L + '" rows="2" readonly>' + esc(abc[i]) + '</textarea>');
  }
  function repHint(oldTxt, nw, label) {
    const c = t.split(oldTxt).length - 1;
    if (c !== 2) throw new Error('hint ' + label + ' count ' + c + ' (want 2): ' + oldTxt);
    t = t.split(oldTxt).join(nw);
  }
  repHint("Click the button and tell us your motto", q.dict, 'dictate ' + n);
  repHint("Type in what your motto is", q.foc, 'focus ' + n);
  t = repOnce(t, '<p class="p3-progress">5 of 10</p>', '<p class="p3-progress">' + n + ' of 15</p>', 'progress ' + n);
  const hm = t.match(/(<div class="p3-naya p3-naya-flank"[^>]*>[\s\S]*?<\/span><\/div>)\s*<main class="p3-main">\s*(<h1 class="p3-question">[\s\S]*?<\/h1>)/);
  if (!hm) throw new Error('header restructure anchor failed on step ' + n);
  t = t.replace(hm[0], '<header class="p3-qhead">' + hm[1] + hm[2] + '</header>\n<main class="p3-main">');
  const lines = t.split('\n');
  const customIdx = lines.findIndex(l => l.includes('class="p3-custom-q"'));
  const speakNoteIdx = lines.findIndex(l => l.includes('id="speakNote-' + n + '"'));
  if (customIdx < 0 || speakNoteIdx < 0) throw new Error('qa-row anchors failed on step ' + n);
  if (lines[speakNoteIdx + 1].trim() !== '</div>') throw new Error('speak-main close anchor failed on step ' + n);
  const slice = lines.splice(customIdx, speakNoteIdx + 2 - customIdx);
  const mainIdx = lines.findIndex(l => l.trim() === '<main class="p3-main">');
  if (mainIdx < 0) throw new Error('main anchor failed on step ' + n);
  const taIdx = slice.findIndex(l => l.includes('id="answer-' + n + '"'));
  if (taIdx < 0) throw new Error('answer textarea anchor failed on step ' + n);
  const aText = esc(abc[0]);
  slice[taIdx] = '<div class="p3-answer-wrap"><button class="p3-choice-edit p3-answer-edit" type="button" data-edit="answer-' + n + '" aria-label="Edit this example — make it your own">EDIT</button><textarea class="visionin p3-example" id="answer-' + n + '" rows="4" data-example="1">' + aText + '</textarea></div>';
  const shortLabel = q.heading.replace(/^"|"$/g, '').split('—')[0].replace('?', '').trim();
  lines.splice(mainIdx + 1, 0, '<div class="p3-qa-row">', '<div class="p3-anscol">', ...slice, WAYS_LINE, '</div>', talkPanel(n, shortLabel, photo), '</div>');
  return lines.join('\n');
}

function buildShowcase() {
  const n = 16, photo = 0;
  let t = TPL;
  t = repOnce(t, 'id="step-5"', 'id="step-16"', 'showcase id');
  t = repOnce(t, 'data-key="motto"', 'data-key="showcase"', 'showcase key');
  t = repOnce(t, 'data-top="5"', 'data-top="16"', 'showcase top');
  t = repOnce(t, 'data-photo="4"', 'data-photo="0"', 'showcase photo');
  t = t.split('-5"').join('-16"');
  t = t.split('"5-').join('"16-');
  t = t.split('-5-').join('-16-');
  if (t.includes('-5"') || t.includes('"5-') || t.includes('-5-')) throw new Error('showcase: leftover -5 refs');
  t = repOnce(t, '<h1 class="p3-question">"What is your motto?"</h1>', '<h1 class="p3-question">' + SHOWCASE.heading + '</h1>', 'showcase heading');
  const cTop = t.indexOf('<p class="p3-choices-top">');
  if (cTop < 0) throw new Error('showcase choices anchor failed');
  const cClose = t.indexOf('\n</div>', t.indexOf('id="choice-16-C"'));
  if (cClose < 0) throw new Error('showcase choices close failed');
  const removed = t.slice(cTop, cClose + 7);
  if (!removed.includes('p3-steps123') || !removed.includes('choice-16-C')) throw new Error('showcase removal wrong span');
  t = t.slice(0, cTop) + '<p class="p3-showcase-note">Share anything — or skip. Blank stays hidden: nothing shows on your page until you fill it in.</p>\n' + t.slice(cClose + 7);
  function repHint(oldTxt, nw, label) {
    const c = t.split(oldTxt).length - 1;
    if (c !== 2) throw new Error('hint ' + label + ' count ' + c);
    t = t.split(oldTxt).join(nw);
  }
  repHint("Click the button and tell us your motto", SHOWCASE.dict, 'showcase dictate');
  repHint("Type in what your motto is", SHOWCASE.foc, 'showcase focus');
  t = repOnce(t, '<p class="p3-progress">5 of 10</p>', '<p class="p3-progress">Your showcase — optional</p>', 'showcase progress');
  const hm = t.match(/(<div class="p3-naya p3-naya-flank"[^>]*>[\s\S]*?<\/span><\/div>)\s*<main class="p3-main">\s*(<h1 class="p3-question">[\s\S]*?<\/h1>)/);
  if (!hm) throw new Error('showcase header anchor failed');
  t = t.replace(hm[0], '<header class="p3-qhead">' + hm[1] + hm[2] + '</header>\n<main class="p3-main">');
  const lines = t.split('\n');
  const customIdx = lines.findIndex(l => l.includes('class="p3-custom-q"'));
  const speakNoteIdx = lines.findIndex(l => l.includes('id="speakNote-16"'));
  if (customIdx < 0 || speakNoteIdx < 0) throw new Error('showcase qa-row anchors failed');
  if (lines[speakNoteIdx + 1].trim() !== '</div>') throw new Error('showcase speak-main close failed');
  const slice = lines.splice(customIdx, speakNoteIdx + 2 - customIdx);
  const mainIdx = lines.findIndex(l => l.trim() === '<main class="p3-main">');
  if (mainIdx < 0) throw new Error('showcase main anchor failed');
  const taIdx = slice.findIndex(l => l.includes('id="answer-16"'));
  slice[taIdx] = '<div class="p3-answer-wrap"><button class="p3-choice-edit p3-answer-edit" type="button" data-edit="answer-16" aria-label="Edit — share what you like">EDIT</button><textarea class="visionin" id="answer-16" rows="4"></textarea></div>';
  lines.splice(mainIdx + 1, 0, '<div class="p3-qa-row">', '<div class="p3-anscol">', ...slice, WAYS_LINE, '</div>', talkPanel(16, 'your showcase', 0), '</div>');
  return lines.join('\n');
}

/* ---------- assemble the 16 steps ---------- */
const steps = Q.map(buildStep);
steps.push(buildShowcase());
const sStart = s.indexOf('<section class="p3-step p3-qstep" id="step-1"');
const sEnd = s.indexOf('<section class="p3-step" id="step-names"');
if (sStart < 0 || sEnd < 0 || sEnd <= sStart) throw new Error('old steps span not found');
const oldSpan = s.slice(sStart, sEnd);
if (!oldSpan.includes('id="step-10"') || !oldSpan.includes('10 of 10')) throw new Error('old steps span wrong');
const keepStyle = oldSpan.slice(oldSpan.indexOf('<style>'));
if (!keepStyle.startsWith('<style>') || !keepStyle.trimEnd().endsWith('</style>')) throw new Error('kept style block malformed');
const keepStyle15 = keepStyle.replace('/* QUESTIONS 10/10 (2026-11-12) — full-page, big-text, three-color boards.', '/* QUESTIONS 15/15 + SHOWCASE (2026-11-21) — full-page, big-text, three-color boards.');
if (keepStyle15 === keepStyle) throw new Error('questions comment not found in kept style');
s = s.slice(0, sStart) + steps.join('\n') + '\n' + keepStyle15 + s.slice(sEnd);

/* ---------- frame div + frame/player CSS ---------- */
s = repOnce(s, '<div class="p3-frame" aria-hidden="true">',
  '<div class="naya-frame" aria-hidden="true"><div class="frame-light"></div></div>\n<div class="p3-frame" aria-hidden="true">', 'frame div');
const newCss = [
'/* WALK 15 — framed layout. NEW rules for this round (the frame + player rules above are harvested verbatim). */',
'.p3-qhead{display:block}',
'.p3-qstep .p3-naya-flank{margin-top:14px}',
'.p3-qa-row{display:flex;gap:16px;align-items:stretch;margin:8px 0 16px}',
'.p3-anscol{flex:1 1 58%;min-width:0;display:flex;flex-direction:column}',
'.p3-talk{flex:1 1 42%;min-width:0;display:flex;flex-direction:column;background:linear-gradient(180deg,#101016,#050607);border:1.5px solid rgba(160,107,255,.55);border-radius:16px;overflow:hidden;box-shadow:inset 0 1px 0 rgba(255,255,255,.14),0 8px 20px rgba(0,0,0,.5)}',
'.p3-talk .sa-theatre-bar{border-bottom:1px solid rgba(255,255,255,.14)}',
'.p3-talk .sa-theatre-body{padding:16px;gap:14px}',
'.p3-talk-title{font-weight:800;font-size:14px;color:#fff;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;min-width:0}',
'.p3-talk-state{font-size:12.5px;font-weight:700;letter-spacing:.06em;color:#E8E8EC;white-space:nowrap}',
'.p3-talk-photo{width:84px;height:84px;flex:none;border-radius:50%;object-fit:cover;border:2px solid #a06bff;box-shadow:0 0 18px rgba(160,107,255,.55)}',
'.p3-talk-bars{display:flex;gap:4px;align-items:flex-end;height:44px;flex:1}',
'.p3-talk-bars i{width:7px;border-radius:3px;background:#a06bff;height:22%;box-shadow:0 0 10px rgba(160,107,255,.6)}',
'.p3-talk.speaking .p3-talk-bars i{animation:talkBars .8s ease-in-out infinite alternate}',
'.p3-talk-bars i:nth-child(2){animation-delay:.12s}.p3-talk-bars i:nth-child(3){animation-delay:.24s}.p3-talk-bars i:nth-child(4){animation-delay:.36s}.p3-talk-bars i:nth-child(5){animation-delay:.48s}',
'@keyframes talkBars{from{height:16%}to{height:100%}}',
'.p3-talk-words{font-size:13.5px;line-height:1.5;color:#E8E8EC;margin:0;padding:0 16px 12px}',
'.p3-talk-play{margin:0 16px 16px;justify-content:center}',
'.p3-answer-wrap{position:relative}',
'.p3-answer-wrap .visionin{padding-right:76px}',
'.p3-answer-edit{position:absolute;top:10px;right:10px;z-index:2}',
'.p3-example{border-color:rgba(255,191,61,.65)}',
'.p3-answer-ways{font-size:13.5px;line-height:1.55;color:#E8E8EC;margin:10px 0 0}',
'.p3-answer-ways b{color:#ffbf3d}',
'.p3-showcase-note{font-size:16px;line-height:1.55;color:#E8E8EC;margin:0 0 12px}',
'@media (max-width:640px){.p3-qa-row{flex-direction:column}.p3-anscol,.p3-talk{flex-basis:auto}.p3-talk-photo{width:64px;height:64px}}'
].join('\n');
const styleBlock = '<style id="walk-15-frame">\n'
  + '/* STAGE FRAME — HARVESTED VERBATIM, agreement blob 1f0b0474 L340-348 (API-verified) */\n' + frameCss
  + '\n/* POWERCAS' + 'T PLAYER — HARVESTED VERBATIM, Personal blob 50867d86: top button L5644-5676 */\n' + pcTopBtnCss
  + '\n/* STAGE SHELL — HARVESTED VERBATIM, Personal blob 50867d86: .sa-theatre-bar / .sa-theatre-sp / .sa-theatre-body L36863,64,66,67. The #saTheatre fixed full-screen rule is NOT copied — the walk panel is inline. */\n' + saShellCss
  + '\n' + newCss + '\n</style>\n';
s = repOnce(s, '</head>', styleBlock + '</head>', 'style insert');

/* ---------- comments ---------- */
s = repOnce(s, 'the 10 new slides + end slide v2 as one flow.', 'the 15 questions + showcase + end slide v2 as one flow.', 'staging comment');
s = repOnce(s, '(Shawn 18:09Z): ten questions -> page-names page -> building page', '(Shawn 18:09Z): fifteen questions + showcase -> page-names page -> building page', 'end flow comment');
s = repOnce(s, 'one minimal "1 of 10" foot mark after the hints', 'one minimal "1 of 15" foot mark after the hints', 'progress comment');

/* ---------- JS patches ---------- */
s = repOnce(s, "var KEYS = ['about', 'into', 'vision', 'mission', 'motto', 'goal', 'biz_do', 'biz_offer', 'biz_building', 'space'];",
  "var KEYS = ['motto', 'vision', 'goal', 'mission', 'love', 'dont', 'thing', 'values', 'laws', 'declaration', 'offer', 'helps', 'moment', 'howwork', 'start', 'showcase'];", 'KEYS');
s = repOnce(s, "for (var i = 1; i <= 10; i++) STEPS.push(document.getElementById('step-' + i));",
  "for (var i = 1; i <= 16; i++) STEPS.push(document.getElementById('step-' + i));", 'STEPS loop');
s = repOnce(s, "var cur = 0; /* 0..9 question steps, 10 = end */",
  "var cur = 0; /* 0..15 questions + showcase, 16 = names, 17 = building, 18 = end */", 'cur comment');
s = repOnce(s, "  NAMESSEC.hidden = (n !== 10);", "  NAMESSEC.hidden = (n !== 16);", 'names hidden');
s = repOnce(s, "  BUILDSEC.hidden = (n !== 11);", "  BUILDSEC.hidden = (n !== 17);", 'build hidden');
s = repOnce(s, "  ENDSEC.hidden = (n !== 12);", "  ENDSEC.hidden = (n !== 18);", 'end hidden');
s = repOnce(s, "  var vis = n < 10 ? STEPS[n] : (n === 10 ? NAMESSEC : (n === 11 ? BUILDSEC : ENDSEC));",
  "  var vis = n < 16 ? STEPS[n] : (n === 16 ? NAMESSEC : (n === 17 ? BUILDSEC : ENDSEC));", 'vis pick');
s = repOnce(s, "function showStep(n){\n  cur = n;",
  "function showStep(n){\n  cur = n;\n  try { if (window.speechSynthesis && window.speechSynthesis.speaking) window.speechSynthesis.cancel(); } catch (e) {}\n  document.querySelectorAll('.p3-talk.speaking').forEach(function(p){ p.classList.remove('speaking'); });\n  document.querySelectorAll('.p3-talk-state').forEach(function(el){ el.textContent = 'Paused'; });\n  document.querySelectorAll('.p3-talk-play').forEach(function(b){ b.textContent = '▶ Play'; });", 'showStep speech stop');
s = repOnce(s, "  if (vis) vis.querySelectorAll('.p3-choice-text').forEach(function(cb){",
  "  if (vis) vis.querySelectorAll('.p3-choice-text, textarea.visionin').forEach(function(cb){", 'fit loop');
s = repOnce(s, "  var playBtn = sec.querySelector('#playBtn-' + n);",
  "  var playBtn = sec.querySelector('#playBtn-' + n);\n  function markMine(){ answer.classList.remove('p3-example'); answer.removeAttribute('data-example'); }", 'markMine def');
s = repOnce(s, "  if (S.answers[key]) answer.value = S.answers[key];",
  "  if (S.answers[key]) { answer.value = S.answers[key]; markMine(); }", 'answer restore');
s = repOnce(s, "      selectChoice(cb.closest('.p3-choice'));\n      S.answers[key] = cb.value; save(); hideStatus(speakNote); hideStatus(enterNote);",
  "      selectChoice(cb.closest('.p3-choice')); markMine();\n      S.answers[key] = cb.value; save(); hideStatus(speakNote); hideStatus(enterNote);", 'choice input markMine');
s = repOnce(s, "      if (k === 'custom'){ answer.focus(); return; }",
  "      if (k === 'custom'){ answer.focus(); return; }\n      if (k.indexOf('answer-') === 0){ markMine(); answer.focus(); try { answer.select(); } catch (e) {} return; }", 'edit answer branch');
s = repOnce(s, "      answer.value = out; selectChoice(null);\n      S.answers[key] = answer.value; save();",
  "      answer.value = out; selectChoice(null); markMine();\n      S.answers[key] = answer.value; save();", 'dictation markMine');
s = repOnce(s, "  answer.addEventListener('input', function(){ selectChoice(null); S.answers[key] = answer.value; save(); hideStatus(speakNote); hideStatus(enterNote); });",
  "  answer.addEventListener('input', function(){ selectChoice(null); markMine(); S.answers[key] = answer.value; save(); hideStatus(speakNote); hideStatus(enterNote); answer.style.height = 'auto'; answer.style.height = (answer.scrollHeight + 2) + 'px'; });", 'answer input markMine');
s = repOnce(s, "if (t){ answer.value = answer.value ? (answer.value.trimEnd() + ' ' + t) : t; selectChoice(null); S.answers[key] = answer.value; save(); }",
  "if (t){ answer.value = answer.value ? (answer.value.trimEnd() + ' ' + t) : t; selectChoice(null); markMine(); S.answers[key] = answer.value; save(); }", 'paste markMine');
s = repOnce(s, "  function submitAnswer(){\n    /* S2 (I) — the answer is the SELECTED one (S.answers[key]): it may live",
  "  function submitAnswer(){\n    /* WALK 15 — a pre-filled example is never an answer: only an edit counts. */\n    if (answer.getAttribute('data-example')){ showStatus(enterNote, \"That's Naya's example — tap EDIT and make it yours, then Enter.\"); return; }\n    /* S2 (I) — the answer is the SELECTED one (S.answers[key]): it may live", 'submit example guard');
s = repOnce(s, "      if (idx < 9) showStep(idx + 1);\n      else showStep(10);",
  "      if (idx < 15) showStep(idx + 1);\n      else showStep(16);", 'submit renumber');
s = repOnce(s, "    if (idx < 9) showStep(idx + 1); else showStep(10);",
  "    if (idx < 15) showStep(idx + 1); else showStep(16);", 'skip renumber');
s = repOnce(s, "  /* play: audio slots are empty until the audio round — glow only, never faked */\n  var audio = null;",
  "  /* WALK 15 — play: Naya speaks the question + what to do (speechSynthesis, same engine as the end slide). The talking box moves while she speaks. */\n  var audio = null;\n  var talkState = sec.querySelector('#talkState-' + n);\n  var talkPlay = sec.querySelector('#talkPlay-' + n);\n  var talkPanel = sec.querySelector('#talk-' + n);\n  var TALK_TEXT = (sec.querySelector('.p3-question') || { textContent: '' }).textContent.replace(/[\"\\u201c\\u201d]/g, '').trim() + ' ' + (key === 'showcase' ? TALK_GUIDE_SHOWCASE : TALK_GUIDE);\n  window.__walkSpeech = window.__walkSpeech || { state: 'idle' };\n  function setTalk(on){ if (talkPanel) talkPanel.classList.toggle('speaking', !!on); if (talkState) talkState.textContent = on ? 'On air — playing' : 'Paused'; if (talkPlay) talkPlay.textContent = on ? '❚❚ Pause' : '▶ Play'; playBtn.classList.toggle('playing', !!on); }\n  function speakQuestion(){\n    var st = window.__walkSpeech;\n    try {\n      if (!('speechSynthesis' in window) || !window.speechSynthesis){ showStatus(speakNote, \"Naya's voice plays on your phone — her real recording comes next.\"); return; }\n      if (window.speechSynthesis.speaking || window.speechSynthesis.pending){ window.speechSynthesis.cancel(); st.state = 'stopped'; setTalk(false); return; }\n      var u = new SpeechSynthesisUtterance(TALK_TEXT);\n      u.onstart = function(){ st.state = 'playing'; setTalk(true); };\n      u.onend = function(){ st.state = 'ended'; setTalk(false); };\n      u.onerror = function(){ st.state = 'error'; setTalk(false); };\n      window.speechSynthesis.speak(u);\n      st.state = 'playing'; setTalk(true);\n    } catch (e) { st.state = 'error'; setTalk(false); }\n  }\n  if (talkPlay) talkPlay.addEventListener('click', speakQuestion);", 'speakQuestion');
s = repOnce(s, "      playBtn.classList.toggle('show');\n    }\n    playGlow();\n  });",
  "      playBtn.classList.toggle('show');\n    }\n    playGlow(); speakQuestion();\n  });", 'playBtn speaks');
s = repOnce(s, "/* --- per-step wiring: the preview script, scoped to one step --- */",
  "var TALK_GUIDE = " + JSON.stringify(TALK_GUIDE) + ";\nvar TALK_GUIDE_SHOWCASE = " + JSON.stringify(TALK_GUIDE_SHOWCASE) + ";\n/* --- per-step wiring: the preview script, scoped to one step --- */", 'talk guide consts');
{
  const m = s.match(/var CUSTOM_WAYS = \[[^\]]*\];/);
  if (!m) throw new Error('CUSTOM_WAYS line missing');
  s = s.replace(m[0], 'var CUSTOM_WAYS = ' + JSON.stringify(CUSTOM_WAYS_NEW).replace(/—/g, '\\u2014') + ';');
}
{
  const newEyes = {};
  const map = { motto: 'motto', vision: 'vision', goal: 'goal', mission: 'mission', thing: 'into', declaration: 'about', offer: 'biz_offer' };
  for (const [nk, ok] of Object.entries(map)) newEyes[nk] = oldEyes[ok];
  for (const [k, v] of Object.entries(EYES_DRAFTED)) newEyes[k] = v;
  newEyes.offer = newEyes.offer.map(e => [e[0], e[1], 'It fills your Skills — what you offer.', e[3]]);
  const ordered = {};
  for (const k of ['motto', 'vision', 'goal', 'mission', 'love', 'dont', 'thing', 'values', 'laws', 'declaration', 'offer', 'helps', 'moment', 'howwork', 'start']) ordered[k] = newEyes[k];
  const eyesStr = 'var CHOICE_EYES = ' + JSON.stringify(ordered).replace(/—/g, '\\u2014') + ';';
  const m = s.match(/var CHOICE_EYES = \{[\s\S]*?\};\n/);
  if (!m) throw new Error('CHOICE_EYES line missing (2nd pass)');
  s = s.replace(m[0], eyesStr + '\n');
}
s = repOnce(s, "'It holds your words from the walk: who you are, what you are into, your vision, mission, motto and goal.',",
  "'It holds your words from the walk: your motto, vision, goal, mission, what you love and don\\'t, your thing, your values, your laws, and your declaration.',", 'board personal');
s = repOnce(s, "'Your shop window \\u2014 what you do, what you offer, and what you are building.',",
  "'Your shop window \\u2014 your motto, your vision, your offer, and your skills.',", 'board business');
s = repOnce(s, "'It holds the space you asked for in the walk, and who you want to meet there.',",
  "'It holds your world\\'s words from the walk \\u2014 your thing, your motto, your vision, and who you want to meet there.',", 'board space');
s = repOnce(s, "    personal: S.answers.about || S.answers.into || '',\n    business: S.answers.biz_do || S.answers.biz_offer || '',\n    space: S.answers.space || S.answers.into || ''",
  "    personal: S.answers.declaration || S.answers.motto || S.answers.thing || '',\n    business: S.answers.offer || S.answers.helps || '',\n    space: S.answers.thing || S.answers.declaration || ''", 'renderEnd words');
s = repOnce(s, "     Personal <- who you are (Q1); Business <- what you do (Q7); Space <-\n     the space you asked for (Q10); each falls back to its nearest own",
  "     Personal <- declaration, else motto, else thing; Business <- offer, else helps;\n     Space <- thing, else declaration; each falls back to its nearest own", 'renderEnd comment');
s = repOnce(s, "if (!bIn.value && S.answers.biz_do) bIn.value = String(S.answers.biz_do).trim().split(/\\s+/).slice(0,4).join(' ');",
  "if (!bIn.value && S.answers.offer) bIn.value = String(S.answers.offer).trim().split(/\\s+/).slice(0,4).join(' ');", 'names default');
s = repOnce(s, "if (go) go.addEventListener('click', function(){ showStep(12); });",
  "if (go) go.addEventListener('click', function(){ showStep(18); });", 'build go');
s = repOnce(s, "if (S.reveal) { renderEnd(); showStep(12); return; }",
  "if (S.reveal) { renderEnd(); showStep(18); return; }", 'boot reveal');
s = repOnce(s, "  var first = 10;", "  var first = 16;", 'boot first');
s = repOnce(s, "  for (var i = 0; i < 10; i++){ if (!S.answers[KEYS[i]]){ first = i; break; } }",
  "  for (var i = 0; i < 16; i++){ if (!S.answers[KEYS[i]]){ first = i; break; } }", 'boot loop');
s = repOnce(s, "  document.querySelectorAll('.p3-flank-photo').forEach(function(img){\n    var pi = parseInt(img.getAttribute('data-photo'), 10);\n    img.src = PHOTOS[pi];\n  });",
  "  document.querySelectorAll('.p3-flank-photo').forEach(function(img){\n    var pi = parseInt(img.getAttribute('data-photo'), 10);\n    img.src = PHOTOS[pi];\n  });\n  document.querySelectorAll('.p3-talk-photo').forEach(function(img){\n    var pi = parseInt(img.getAttribute('data-photo'), 10);\n    img.src = PHOTOS[pi];\n  });", 'boot talk photos');

/* ---------- verify ---------- */
const problems = [];
function chk(cond, label) { if (!cond) problems.push(label); console.log((cond ? 'PASS ' : 'FAIL ') + label); }
chk(!s.includes('of 10'), 'no "of 10" left');
chk((s.match(/ of 15<\/p>/g) || []).length === 15, '"N of 15" x15 (got ' + (s.match(/ of 15<\/p>/g) || []).length + ')');
chk(s.includes('Your showcase — optional'), 'showcase progress line');
chk((s.match(/class="p3-step p3-qstep"/g) || []).length === 16, '16 qsteps');
chk((s.match(/data-example="1"/g) || []).length === 15, '15 pre-filled example boxes');
chk((s.match(/class="p3-talk"/g) || []).length === 16, '16 talking boxes');
chk((s.match(/class="p3-qa-row"/g) || []).length === 16, '16 side-by-side rows');
chk((s.match(/class="p3-qhead"/g) || []).length === 16, '16 framed headers');
chk(s.includes('.p3-choice-eye{') && s.includes('/* S2 (I, replaced 20:17Z)'), 'kept S2/names style block present');
chk(s.includes('QUESTIONS 15/15 + SHOWCASE'), 'questions comment updated');
chk(frameLines.every(l => s.includes(l)), 'agreement L340-348 verbatim in output');
chk(s.includes(pcTopBtnCss.split('\n')[0]) && s.includes('.powercast-topbtn:active{transform:translateY(0) scale(.97);}'), 'powercast-topbtn CSS verbatim in output');
chk(s.includes('.sa-theatre-bar{display:flex;align-items:center;gap:10px;'), 'sa-theatre-bar CSS verbatim in output');
chk(s.includes("On air — playing") && s.includes('▶ Play'), 'saPcSync state strings in output');
chk(!s.includes('biz_do') && !s.includes('biz_offer') && !s.includes('biz_building') && !s.includes("answers.space") && !s.includes("answers.about") && !s.includes("answers.into"), 'no old answer keys left');
chk(!s.includes('What do you do?') && !s.includes('What are you building') && !s.includes('What kind of space do you want'), 'old Q7/Q9/Q10 headings gone');
for (const q of Q) { chk(s.includes('data-key="' + q.key + '"'), 'key present: ' + q.key); chk(s.includes(q.heading), 'heading present: ' + q.key); }
chk(s.includes('data-key="showcase"'), 'key present: showcase');
chk(s.includes('showStep(16)') && s.includes('showStep(18)'), 'renumbered flow targets');
chk(!s.includes('showStep(10)') && !s.includes('showStep(12)'), 'no old flow targets left');
chk(!s.includes("i <= 10") && !s.includes('i < 10'), 'no old 10-counts left');
{
  const mm = s.match(/<script>([\s\S]*?)<\/script>/);
  if (!mm) problems.push('no script block');
  else {
    try { new Function(mm[1]); console.log('PASS script parses (new Function)'); }
    catch (e) { problems.push('script parse: ' + e.message); console.log('FAIL script parses: ' + e.message); }
  }
}
if (problems.length) { console.log('PROBLEMS: ' + problems.join(' | ')); process.exit(1); }

/* ---------- write in 8KB chunks + verify ---------- */
const out = Buffer.from(s, 'utf8');
function writeChunked(path, buf) {
  const fd = fs.openSync(path, 'w');
  try {
    let off = 0;
    while (off < buf.length) { const n = fs.writeSync(fd, buf, off, Math.min(8192, buf.length - off)); if (n <= 0) throw new Error('short write'); off += n; }
  } finally { fs.closeSync(fd); }
}
if (process.env.WALK15_STDOUT === '1') {
  // No local write: emit base64 to stdout for the runtime to save; the
  // filing script decodes it from the saved tool-output JSON and PUTs it
  // to GitHub from memory. Used when the EPERM flake blocks process writes.
  const b64 = Buffer.from(out, 'utf8').toString('base64');
  console.log('WALK15_BEGIN');
  for (let i = 0; i < b64.length; i += 76) console.log(b64.slice(i, i + 76));
  console.log('WALK15_END');
  console.log('WALK15_BYTES=' + out.length + ' WALK15_SHA256=' + sha256(out) + ' WALK15_BLOB=' + gitBlobSha(out));
} else {
const sleepSync = ms => { try { Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, ms); } catch (e) {} };
let attempt = 0;
for (;;) {
  attempt++;
  try { fs.writeFileSync(OUT_P, out); } catch (e) { console.log('write attempt ' + attempt + ' failed: ' + e.message); }
  try {
    const back = fs.readFileSync(OUT_P);
    if (back.length === out.length && sha256(back) === sha256(out)) break;
    console.log('write attempt ' + attempt + ' landed wrong size/sha: ' + back.length + ' vs ' + out.length);
  } catch (e) { console.log('write attempt ' + attempt + ' read-back failed: ' + e.message); }
  if (attempt >= 180) throw new Error('write never landed after 180 attempts');
  sleepSync(2000);
}
console.log('WROTE ' + OUT_P + ' bytes=' + out.length + ' sha256=' + sha256(out) + ' git-blob=' + gitBlobSha(out));
console.log('DONE');
}
