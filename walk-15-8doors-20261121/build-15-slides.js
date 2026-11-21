#!/usr/bin/env node
/* WALK 15 — SLIDES BUILD.
   Source: Shawn's sent slides (walk-slide-02..10 + walk-slide-end), NOT fd38de47's
   step-5 template. Slide 02 is the per-step template (verbatim); the 15 locked
   questions + showcase ride it; entry = the lane walk's certificate door;
   naming = the lane walk's step-names (verbatim); reveal = NEW 8-door page with the pricing gate;
   end = walk-slide-end.html framed (verbatim body + script).
   Frame: agreement L340-348 verbatim. Player: PowerCast harvested from the
   staged Personal bytes (same harvest as build-15.js). Filing: stdout pipe
   (WALK15_STDOUT=1) — the EPERM flake blocks process writes of the big file.
   Usage: WALK15_STDOUT=1 node build-15-slides.js | python3 file-15-slides-stdin.py */
const fs = require('fs');
const { execSync } = require('child_process');
const crypto = require('crypto');
const LANE = '/home/hatch/workspace/team-nitro/walk-q2-whats-your-thing-20261113';
const USERF = '/home/hatch/workspace/user/files';
const SLIDE2_P = USERF + '/walk-slide-02.html';
const SLIDE_END_P = USERF + '/walk-slide-end.html';
const BASE_P = LANE + '/walk-beginning-fixed.html';
const AGREE_P = '/home/hatch/workspace/team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html';
const PERSONAL_URL = 'https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO%2Fpersonal-page-complete-20261113%2Fpersonal-complete.html&ref=personal/universal-bar-20261121&cb=50867d86f31ce8b25b454fd40b9deec3eebb4545';
function sha256(b) { return crypto.createHash('sha256').update(b).digest('hex'); }
function gitBlobSha(raw) { const buf = Buffer.isBuffer(raw) ? raw : Buffer.from(raw, 'utf8'); return crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob ' + buf.length + '\0'), buf])).digest('hex'); }
function repOnce(s, old, nw, label) { const n = s.split(old).length - 1; if (n !== 1) throw new Error(label + ': anchor occurs ' + n + 'x (want 1): ' + JSON.stringify(old.slice(0, 90))); return s.replace(old, nw); }
function chk(c, label) { if (!c) throw new Error('CHECK FAILED: ' + label); console.log('PASS ' + label); }

/* ---------- the locked 15 + showcase: headings (DRAFTED except Q11), tips, examples ---------- */
/* Examples: drafted ONLY from Shawn's filed words (Seat E / Seat G frame-styles
   reports + MEMORY.md). Q1 motto is VERBATIM Shawn (SN-0823). Q10 is Naya's own
   Anaya Declaration as the MODEL example — never presented as Shawn's. */
const Q = [
 { n: 1, key: 'motto', short: 'Motto', heading: "What's your motto — the one line that says who you are?",
   dictate: "Click the button and tell us your motto", focus: "Type in your motto — the one line that says who you are",
   ex: "The most extraordinary awe inspiring beautiful intuitive useful push button simple logical sensible smart app ever created." },
 { n: 2, key: 'vision', short: 'Vision', heading: "What's your vision — the world you want to see?",
   dictate: "Click the button and tell us your vision", focus: "Type in your vision — the world you want to see",
   ex: "What if we built a world where everybody could win? She opens one place — a vision of 2028. Intelligence that remembers. Learns. Connects. Proves. Grows." },
 { n: 3, key: 'goal', short: 'Goal', heading: "What's your goal — what are you working toward?",
   dictate: "Click the button and tell us your goal", focus: "Type in your goal — what you are working toward",
   ex: "A 100% success rate — push-button simple. It makes you money, and it connects you with people of like minds. Create, learn, grow, earn — together." },
 { n: 4, key: 'mission', short: 'Mission', heading: "What's your mission — what are you here to do?",
   dictate: "Click the button and tell us your mission", focus: "Type in your mission — what you are here to do",
   ex: "Create heaven on earth — a state of awesome energy. Stress, fears, money worries, hopelessness get a way to understand, and money to pay their bills, shifting consciousness positive." },
 { n: 5, key: 'love', short: 'What I love', heading: "What do you love?",
   dictate: "Click the button and tell us what you love", focus: "Type in what you love",
   ex: "Real things — real objects, alive on hover, not pictures of objects. Numbers that prove it — ten out of ten, with the gauges. Straight up — no games, no bullshit, just straight up: this is how it works." },
 { n: 6, key: 'dont', short: "What I don't", heading: "What don't you love — what do you want less of?",
   dictate: "Click the button and tell us what you don't love", focus: "Type in what you don't love — what you want less of",
   ex: "No flat shapes, no gray text, no dead boards. No rebuilding, no redesigning — craft, advance, enhance. Nobody sits through 98 slides — one frame at a time." },
 { n: 7, key: 'thing', short: 'Your Thing', heading: "What's your thing — the one thing that's yours?",
   dictate: "Click the button and tell us what your thing is", focus: "Type in what your thing is, and what you love to do",
   ex: "My thing is NayaNET — the connection itself: the moment two like minds find each other across the world and realize they were never alone." },
 { n: 8, key: 'values', short: 'Values', heading: "What do you value — what matters most to you?",
   dictate: "Click the button and tell us what you value", focus: "Type in what you value — what matters most to you",
   ex: "Do no harm. Ever. Wisdom first — smart finds the fastest road, wisdom checks the destination first. The most intelligent thing, every time. Ten stars, or don't send it." },
 { n: 9, key: 'laws', short: 'Laws you follow', heading: "What laws do you follow — the rules you live by?",
   dictate: "Click the button and tell us the laws you follow", focus: "Type in the laws you follow — the rules you live by",
   ex: "I follow protocol. I think before I act, and I never waver. The Design Laws — real objects, white words, alive on hover. The five gates — right, needed, mine, now, proven." },
 { n: 10, key: 'declaration', short: 'Your Declaration', heading: "Your declaration — who are you, in your own words?",
   dictate: "Click the button and tell us who you are", focus: "Type in your declaration — who you are, in your own words",
   ex: "I am Naya. I do the most intelligent thing every time. I deliberate, I think things through, I see the whole scope, and I make the best possible choice." },
 { n: 11, key: 'offer', short: 'What you offer', heading: "What do you offer?",
   dictate: "Click the button and tell us what you offer", focus: "Type in what you offer",
   ex: "I offer NayaNET — a new internet where everybody can win: create, learn, grow and earn together. Anyone joins free." },
 { n: 12, key: 'helps', short: 'How it helps', heading: "How does it help them — what does it do for them?",
   dictate: "Click the button and tell us how it helps them", focus: "Type in how it helps them — what it does for them",
   ex: "It gives you one place instead of hundreds of emails and websites — and it connects you with people of like minds, into what you're into." },
 { n: 13, key: 'moment', short: 'A moment', heading: "Tell me a moment you've done it — a time it worked.",
   dictate: "Click the button and tell us a moment you've done it", focus: "Type in a moment you've done it — a time it worked",
   ex: "The first live Smart Notes — one fix, and Naya's notes flowed from GitHub to the Hub live for the first time." },
 { n: 14, key: 'howwork', short: 'How you work', heading: "How do you work — how does someone work with you?",
   dictate: "Click the button and tell us how you work", focus: "Type in how you work — how someone works with you",
   ex: "You talk to Naya — she builds it with you, and she runs the system for you. You don't run the system; Naya does." },
 { n: 15, key: 'start', short: 'How to start', heading: "How does someone start with you — what's the first step?",
   dictate: "Click the button and tell us how someone starts with you", focus: "Type in how someone starts with you — what's the first step",
   ex: "Just join free — answer the 15 questions, and your world arrives made." },
];
const SHOWCASE = { n: 16, key: 'showcase', short: 'Your showcase',
  heading: "Would you like to showcase any of your experiences — things you have accomplished, certificates, awards — or just share something unique to you?",
  dictate: "Click the button and tell us what you'd like to showcase",
  focus: "Type in anything you'd like to showcase — or skip" };
const TALK_GUIDE = "Edit it, clear it, or dictate — make it your own. Or have your AI write it for you, and copy-paste it in. Or just write in what you want, or skip. Then press Enter, and it becomes your answer.";
const TALK_GUIDE_SHOWCASE = "Share anything you like — or skip. Blank stays hidden: nothing shows on your page until you fill it in.";
const WAYS_LINE = '<p class="p3-answer-ways"><b>A</b> — click edit, make it your own, dictate or type in · <b>B</b> — have your AI write it for you, copy-paste it in · or skip.</p>';
const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

/* ---------- verify sources first-hand ---------- */
const slide2Buf = fs.readFileSync(SLIDE2_P);
if (slide2Buf.length !== 702605) throw new Error('slide-02 size moved: ' + slide2Buf.length);
if (sha256(slide2Buf) !== 'dce166cb0f5f2e55cf775396af8991b708452ac8b48ab9323fb70ab3e03ac0be') throw new Error('slide-02 sha moved');
const slide2 = slide2Buf.toString('utf8');
const endBuf = fs.readFileSync(SLIDE_END_P);
if (endBuf.length !== 705464) throw new Error('end slide size moved: ' + endBuf.length);
if (sha256(endBuf) !== 'ce6a1060301884bf9edd9fa8f6a8fa254d55072e0721f99c85f12ae5f2dbf877') throw new Error('end slide sha moved');
const endSlide = endBuf.toString('utf8');
const baseBuf = fs.readFileSync(BASE_P);
if (sha256(baseBuf) !== 'fd38de479d17d6ce51ae33a7667b9b5458eb6a743df626282a187d2cbe13e836') throw new Error('lane base sha moved');
const base = baseBuf.toString('utf8');
console.log('sources verified: slide-02 702605, end 705464, lane base fd38de47');

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

/* ---------- split slide 02 into head / body-open / question template / tail ---------- */
const headEnd = slide2.indexOf('</head>');
if (headEnd < 0) throw new Error('slide-02: no </head>');
let headHtml = slide2.slice(0, headEnd + '</head>'.length);
chk(headHtml.includes('<style>') && headHtml.includes('</style>'), 'slide head has the style block');
/* the slide's own CSS comment still says "2 of 10" — the ordered count change updates it */
const headFixed = headHtml.replace('"2 of 10" foot mark', '"N of 15" foot mark');
if (headFixed === headHtml) throw new Error('slide head 10-count comment anchor moved');
headHtml = headFixed;
const bodyOpenIdx = slide2.indexOf('<body>');
const flankIdx = slide2.indexOf('<div class="p3-naya p3-naya-flank">');
if (bodyOpenIdx < 0 || flankIdx < 0 || flankIdx < bodyOpenIdx) throw new Error('slide-02: body/flank anchors');
const bodyOpen = slide2.slice(bodyOpenIdx, flankIdx);
chk(bodyOpen.includes('<div class="p3-frame"'), 'slide body-open has its own p3-frame div');
const mainCloseIdx = slide2.indexOf('</main>', flankIdx);
if (mainCloseIdx < 0) throw new Error('slide-02: no </main>');
const qTemplate = slide2.slice(flankIdx, mainCloseIdx + '</main>'.length);
for (const a of ['id="playBtn"', 'id="answer"', 'id="speakBtn"', 'id="enterBtn"', 'id="hintRow"', 'class="p3-question"', 'class="p3-progress"', 'data-act="play"', 'data-act="dictate"', 'data-act="focus"', 'data-act="paste"', 'data-act="submit"', '"What are you into, and why?"', '2 of 10']) {
  if (!qTemplate.includes(a)) throw new Error('slide template missing: ' + a);
}
chk((qTemplate.match(/<textarea/g) || []).length === 1, 'template has exactly one textarea');
/* photo: extract the flank portrait data URI once; steps share it via JS at boot */
const photoM = qTemplate.match(/<img class="p3-flank-photo" src="(data:image\/jpeg;base64,[^"]+)" alt="Naya">/);
if (!photoM) throw new Error('slide template: flank photo data URI missing');
const PHOTO_DATA = photoM[1];
chk(PHOTO_DATA.length > 10000, 'flank photo data URI extracted (' + PHOTO_DATA.length + ' chars)');
const qTemplateNoPhoto = qTemplate.replace(PHOTO_DATA, '');
/* end slide: head style + body (flank + main) + script, all verbatim */
const endHeadM = endSlide.match(/<style>[\s\S]*?<\/style>/);
if (!endHeadM) throw new Error('end slide: no <style>');
const endStyle = endHeadM[0];
/* NOTE: the end file's "1 of 10" lives in its top HTML comment, which is NOT carried into the output (only style/body/script are) — no fix needed there. */
chk(endStyle.includes('.p3-congrats') && endStyle.includes('.p3-door'), 'end slide style has congrats + doors');
const endFlankIdx = endSlide.indexOf('<div class="p3-naya p3-naya-flank">');
const endMainCloseIdx = endSlide.indexOf('</main>', endFlankIdx);
if (endFlankIdx < 0 || endMainCloseIdx < 0) throw new Error('end slide: flank/main anchors');
const endBody = endSlide.slice(endFlankIdx, endMainCloseIdx + '</main>'.length);
for (const a of ['"Congratulations, you\'re hired."', 'Welcome complete', 'id="copyBtn"', 'id="doorRow"', 'id="installBtn"', 'data-door="Dashboard"', 'data-door="Personal"', 'data-door="Business"', 'data-door="Space"', 'data-door="Hub"']) {
  if (!endBody.includes(a)) throw new Error('end slide body missing: ' + a);
}
const endScriptM = endSlide.match(/<script>[\s\S]*?<\/script>/);
if (!endScriptM) throw new Error('end slide: no <script>');
const endScript = endScriptM[0];
chk(endScript.includes("getElementById('doorRow')"), 'end slide script wires the doors');
/* lane walk: entry door + naming page, verbatim */
const doorM = base.match(/<section class="p3-step" id="step-door" hidden>[\s\S]*?<\/section>/);
if (!doorM) throw new Error('lane base: step-door (entry) missing');
const entrySec = doorM[0];
chk(entrySec.includes('"Welcome starts with your certificate."'), 'entry is the certificate door');
const namesM = base.match(/<section class="p3-step" id="step-names" data-key="names" hidden>[\s\S]*?<\/section>/);
if (!namesM) throw new Error('lane base: step-names missing');
let namesSec = namesM[0];
for (const a of ['id="name-personal"', 'id="name-business"', 'id="name-space"', 'id="url-personal"', 'id="url-business"', 'id="url-space"', '"Name your world."']) {
  if (!namesSec.includes(a)) throw new Error('naming page missing: ' + a);
}
namesSec = namesSec.replace('id="playBtn-11"', 'id="playBtn-names"').replace('id="enterBtn-11"', 'id="enterBtn-names"').replace('id="enterNote-11"', 'id="enterNote-names"');
chk(!namesSec.includes('playBtn-11') && !namesSec.includes('enterBtn-11'), 'naming ids re-pointed (no collision with Q11)');

/* ---------- talk panel (PowerCast, harvested shell) ---------- */
function talkPanel(n, shortLabel) {
  return [
    '<div class="p3-talk" id="talk-' + n + '">',
    '<div class="sa-theatre-bar"><span class="p3-talk-title">Naya speaks — ' + esc(shortLabel) + '</span><span class="sa-theatre-sp"></span><span class="p3-talk-state" id="talkState-' + n + '">Paused</span></div>',
    '<div class="sa-theatre-body"><img class="p3-talk-photo" data-photo="0" src="" alt="Naya"><span class="p3-talk-bars" id="talkBars-' + n + '" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></span></div>',
    '<p class="p3-talk-words">Tap play — Naya speaks this question.</p>',
    '<button class="powercast-topbtn p3-talk-play" id="talkPlay-' + n + '" type="button" aria-label="Play — Naya speaks this question">▶ Play</button>',
    '</div>'
  ].join('\n');
}

/* ---------- build one question step from the slide template ---------- */
function buildStep(q) {
  const n = q.n, isShow = q.key === 'showcase';
  let t = qTemplateNoPhoto;
  t = repOnce(t, '<div class="p3-naya p3-naya-flank">', '<header class="p3-qhead"><div class="p3-naya p3-naya-flank">', 'qhead open ' + n);
  t = repOnce(t, '</main>', '</main></header>', 'qhead close ' + n);
  t = repOnce(t, 'id="playBtn"', 'id="playBtn-' + n + '"', 'playBtn ' + n);
  t = repOnce(t, '"What are you into, and why?"', '"' + esc(q.heading) + '"', 'heading ' + n);
  /* answer box: pre-filled Naya example + Edit; showcase stays empty */
  const exAttr = isShow ? '' : ' class="visionin p3-example" data-example="1"';
  t = repOnce(t, '<textarea class="visionin" id="answer" rows="4"></textarea>',
    '<div class="p3-qa-row"><div class="p3-anscol"><div class="p3-answer-wrap"><textarea' + exAttr + ' id="answer-' + n + '" rows="4">' + (isShow ? '' : esc(q.ex)) + '</textarea>' +
    '<button class="p3-answer-edit" type="button" data-edit="answer-' + n + '" aria-label="Edit this example">EDIT</button></div>' + WAYS_LINE + '</div>' + talkPanel(n, q.short) + '</div>',
    'answer box ' + n);
  /* the slide's speak row + Enter + hints follow the qa-row; re-id them */
  t = repOnce(t, 'id="speakBtn"', 'id="speakBtn-' + n + '"', 'speakBtn ' + n);
  t = repOnce(t, 'id="speakNote"', 'id="speakNote-' + n + '"', 'speakNote ' + n);
  t = repOnce(t, 'id="enterBtn"', 'id="enterBtn-' + n + '"', 'enterBtn ' + n);
  t = repOnce(t, 'id="enterNote"', 'id="enterNote-' + n + '"', 'enterNote ' + n);
  t = repOnce(t, 'id="hintRow"', 'id="hintRow-' + n + '"', 'hintRow ' + n);
  /* tips: dictate + focus labels per question; paste + play stay as sent */
  t = repOnce(t, 'aria-label="Click the button and tell us what you\'re into"', 'aria-label="' + esc(q.dictate) + '"', 'dictate label ' + n);
  t = repOnce(t, 'aria-label="Type in what you\'re into, and why"', 'aria-label="' + esc(q.focus) + '"', 'focus label ' + n);
  t = t.replace('>Click the button and tell us what you\'re into<', '>' + esc(q.dictate) + '<');
  t = t.replace('>Type in what you\'re into, and why<', '>' + esc(q.focus) + '<');
  /* Skip: the slide has none; "or skip" + nothing-forced require it (flagged in the report) */
  t = repOnce(t, '</button>\n<div class="p3-hints"',
    '</button>\n<button class="p3-skip" id="skipBtn-' + n + '" type="button">Skip</button>\n<div class="p3-hints"', 'skip ' + n);
  /* progress: N of 15; showcase has its own line */
  t = repOnce(t, '2 of 10', isShow ? 'Your showcase — optional' : (n + ' of 15'), 'progress ' + n);
  if (t.includes(' of 10') || t.includes('"What are you into')) throw new Error('step ' + n + ': leftover slide-02 text');
  if (!isShow && !t.includes('data-example="1"')) throw new Error('step ' + n + ': example flag missing');
  return '<section class="p3-step p3-qstep" id="step-' + n + '" data-key="' + q.key + '" hidden>\n' + t + '\n</section>';
}
const steps = Q.map(buildStep);
steps.push(buildStep(SHOWCASE));
chk(steps.length === 16, '16 steps built (15 + showcase)');

/* ---------- names CSS: only the .p3-name* rules, harvested from the lane walk ---------- */
const style2M = base.match(/<style>\n:root\{color-scheme:dark\}[\s\S]*?<\/style>/);
if (!style2M) throw new Error('lane base: second style block missing');
const namesCss = style2M[0].split('\n').filter(l => /^\.(p3-names|p3-namecard|p3-nc-|p3-build-link)/.test(l.trim()) || l.trim().startsWith('/* S2 — Names')).join('\n');
chk(namesCss.includes('.p3-namecard{') && namesCss.includes('.p3-nc-url{'), 'names CSS harvested (.p3-namecard + .p3-nc-url)');

/* ---------- reveal page: EIGHT doors, each gated through the pricing page (v77, nayanet.app/pricing) ---------- */
const PRICING_URL = 'https://nayanet.app/pricing';
const revealSec = [
'<section class="p3-step" id="step-reveal" data-key="reveal" hidden>',
'<div class="p3-naya p3-naya-flank" data-top="reveal"><span class="p3-flank-side p3-flank-left">',
'<img class="p3-flank-photo" data-photo="0" src="" alt="Naya">',
'</span>',
'<button class="p3-naya-play" id="playBtn-reveal" type="button" aria-label="Naya will talk you through this page"><svg viewBox="0 0 24 24" width="24" height="24" fill="#fff" aria-hidden="true"><path d="M7 4l13 8-13 8z"/></svg><span class="p3-play-tip">Naya will talk you through this page</span></button>',
'<span class="p3-flank-side p3-flank-right"><span class="p3-logo-top">NAYA</span></span></div>',
'<main class="p3-main">',
'<h1 class="p3-question">"Here are your pages."</h1>',
'<p class="p3-note">Your alias also gives you your calendar, your dashboard, and your hub — plus the About and Skills pages we just built for you. Tap any door and first you will choose your plan: stay on FREE, or upgrade to Naya Power, Naya Pro, or Naya Max. Then you are in — and you can change your level any time from Pricing in the sidebar.</p>',
'<div class="p3-doors" id="revealDoors">',
'<a class="p3-door" data-reveal="personal" href="https://nayanet.app/pricing?next=https%3A%2F%2Fnayanet.app%2Fyourname" target="_blank" rel="noopener">Personal<span class="p3-door-sub">nayanet.app/<span class="rv-alias">yourname</span></span></a>',
'<a class="p3-door" data-reveal="business" href="https://nayanet.app/pricing?next=https%3A%2F%2Fnayanet.app%2Fyourname" target="_blank" rel="noopener">Business<span class="p3-door-sub">nayanet.app/<span class="rv-alias">yourname</span></span></a>',
'<a class="p3-door" data-reveal="world" href="https://nayanet.app/pricing?next=https%3A%2F%2Fyourworld.nayanet.app" target="_blank" rel="noopener">World<span class="p3-door-sub"><span class="rv-world">yourworld</span>.nayanet.app</span></a>',
'<a class="p3-door" data-reveal="hub" href="https://nayanet.app/pricing?next=https%3A%2F%2Fhub.nayanet.app%2Fyourname" target="_blank" rel="noopener">Hub<span class="p3-door-sub">hub.nayanet.app/<span class="rv-alias">yourname</span></span></a>',
'<a class="p3-door" data-reveal="dashboard" href="https://nayanet.app/pricing?next=https%3A%2F%2Fdashboard.nayanet.app%2Fyourname" target="_blank" rel="noopener">Dashboard<span class="p3-door-sub">dashboard.nayanet.app/<span class="rv-alias">yourname</span></span></a>',
'<a class="p3-door" data-reveal="calendar" href="https://nayanet.app/pricing?next=https%3A%2F%2Fcalendar.nayanet.app%2Fyourname" target="_blank" rel="noopener">Calendar<span class="p3-door-sub">calendar.nayanet.app/<span class="rv-alias">yourname</span></span></a>',
'<a class="p3-door" data-reveal="about" href="https://nayanet.app/pricing?next=https%3A%2F%2Fnayanet.app%2Fyourname%2Fabout" target="_blank" rel="noopener">About<span class="p3-door-sub">nayanet.app/<span class="rv-alias">yourname</span>/about</span></a>',
'<a class="p3-door" data-reveal="skills" href="https://nayanet.app/pricing?next=https%3A%2F%2Fnayanet.app%2Fyourname%2Fskills" target="_blank" rel="noopener">Skills<span class="p3-door-sub">nayanet.app/<span class="rv-alias">yourname</span>/skills</span></a>',
'</div>',
'<p class="p3-note" id="revealNote" hidden></p>',
'<p class="p3-progress">Your pages</p>',
'</main>',
'</section>'
].join('\n');
/* entry: the harvested certificate door has no control; a walk needs a way in (flagged) */
const entryWithEnter = entrySec.replace('</main>', '<button class="p3-enter" id="enterBtn-door" type="button">Enter</button>\n</main>');
if (entryWithEnter === entrySec) throw new Error('entry Enter insert failed');
const endSec = '<section class="p3-step" id="step-end" data-key="end" hidden>\n' + endBody + '\n</section>';

/* ---------- layout CSS (new; the harvested parts are frame/pcTopBtn/saShell above) ---------- */
const layoutCss = [
'/* WALK 15 SLIDES — layout: PROMAX mirror. Header: picture + question (picture down a touch). Body: input one side, talking box the other. Buttons below. */',
'.p3-qhead{display:block}',
'.p3-naya-flank{margin-top:14px}',
'.p3-qa-row{display:flex;gap:16px;align-items:stretch;margin-bottom:6px}',
'.p3-anscol{flex:1 1 0;min-width:0}',
'.p3-talk{flex:0 0 250px;box-sizing:border-box;min-width:0;border:1px solid rgba(255,255,255,.22);border-radius:16px;padding:12px;background:linear-gradient(180deg,rgba(255,255,255,.08),rgba(255,255,255,.02) 60%,rgba(0,0,0,.28))}',
'.p3-talk.speaking{border-color:#a06bff;box-shadow:0 0 26px rgba(160,107,255,.45)}',
'.p3-talk-title{font-size:14px;font-weight:700;color:#fff}',
'.p3-talk-state{font-size:13px;color:#fff}',
'.p3-talk-photo{width:72px;height:72px;border-radius:50%;object-fit:cover;border:2px solid #a06bff}',
'.p3-talk-bars{display:inline-flex;gap:4px;align-items:flex-end;height:34px;margin-left:12px}',
'.p3-talk-bars i{width:5px;height:10px;background:#a06bff;border-radius:3px;animation:talkBars 1s ease-in-out infinite}',
'.p3-talk-bars i:nth-child(2){animation-delay:.15s}.p3-talk-bars i:nth-child(3){animation-delay:.3s}.p3-talk-bars i:nth-child(4){animation-delay:.45s}.p3-talk-bars i:nth-child(5){animation-delay:.6s}',
'.p3-talk.speaking .p3-talk-bars i{animation-duration:.55s}',
'@keyframes talkBars{0%,100%{height:8px}50%{height:30px}}',
'.p3-talk-words{font-size:13.5px;line-height:1.5;color:#fff;margin:10px 0}',
'.p3-talk-play{width:100%}',
'.p3-answer-wrap{position:relative}',
'.p3-answer-edit{position:absolute;top:10px;right:10px;padding:8px 14px;border-radius:999px;border:2px solid #a06bff;background:linear-gradient(180deg,#2a2a3a,#14141c);color:#fff;font-weight:800;font-size:13px;letter-spacing:.08em;cursor:pointer}',
'.p3-example{border-color:#a06bff !important}',
'.p3-answer-ways{font-size:15px;line-height:1.55;color:#fff;margin:10px 0 0}',
'.p3-skip{display:block;margin:10px auto 0;padding:10px 30px;border-radius:999px;border:1.5px solid rgba(255,255,255,.4);background:transparent;color:#fff;font-size:15px;cursor:pointer}',
'@media (max-width:640px){.p3-qa-row{flex-direction:column}.p3-talk{flex:1 1 auto}}',
'#step-reveal .p3-door{text-decoration:none}',
'.p3-door[href*="yourname"]{opacity:.85}'
].join('\n');

/* ---------- engine (fresh; behaviors follow the slide's own script) ---------- */
const engineJs = [
'(function(){',
'var PHOTO_DATA = ' + JSON.stringify(PHOTO_DATA) + ';',
'document.querySelectorAll("img[data-photo]").forEach(function(im){ if(!im.getAttribute("src")) im.src = PHOTO_DATA; });',
'var BOX_KEY = "naya-walk-15-slides";',
'var box = { answers: {}, names: {} };',
'try { var saved = JSON.parse(localStorage.getItem(BOX_KEY) || "null"); if (saved && saved.answers) box = saved; } catch (e) {}',
'function saveBox(){ try { localStorage.setItem(BOX_KEY, JSON.stringify(box)); } catch (e) {} }',
'var ORDER = ["step-door","step-1","step-2","step-3","step-4","step-5","step-6","step-7","step-8","step-9","step-10","step-11","step-12","step-13","step-14","step-15","step-16","step-names","step-reveal","step-end"];',
'var QKEYS = ' + JSON.stringify(Q.map(q => q.key).concat(['showcase'])) + ';',
'function showStep(id){ ORDER.forEach(function(s){ var el = document.getElementById(s); if (el) el.hidden = (s !== id); }); try { window.scrollTo(0, 0); } catch (e) {} try { if (window.speechSynthesis) window.speechSynthesis.cancel(); } catch (e) {} document.querySelectorAll(".p3-talk").forEach(function(p){ p.classList.remove("speaking"); }); document.querySelectorAll(".p3-talk-state").forEach(function(s){ s.textContent = "Paused"; }); document.querySelectorAll(".p3-talk-play").forEach(function(b){ b.textContent = "▶ Play"; }); }',
'function showStatus(el, text){ if (!el) return; if (el._t) clearTimeout(el._t); el.textContent = text; el.hidden = false; el._t = setTimeout(function(){ el.hidden = true; el._t = null; }, 5000); }',
'function hideStatus(el){ if (!el) return; if (el._t){ clearTimeout(el._t); el._t = null; } el.hidden = true; }',
'function markMine(answer){ if (!answer) return; answer.removeAttribute("data-example"); answer.classList.remove("p3-example"); }',
'function nextAfter(id){ var i = ORDER.indexOf(id); return ORDER[Math.min(i + 1, ORDER.length - 1)]; }',
'var TALK_GUIDE = ' + JSON.stringify(TALK_GUIDE) + ';',
'var TALK_GUIDE_SHOWCASE = ' + JSON.stringify(TALK_GUIDE_SHOWCASE) + ';',
'function wireQuestion(n, key){',
'  var sec = document.getElementById("step-" + n); if (!sec) return;',
'  var answer = document.getElementById("answer-" + n), speakBtn = document.getElementById("speakBtn-" + n),',
'      speakNote = document.getElementById("speakNote-" + n), enterBtn = document.getElementById("enterBtn-" + n),',
'      enterNote = document.getElementById("enterNote-" + n), hintRow = document.getElementById("hintRow-" + n),',
'      playBtn = document.getElementById("playBtn-" + n), skipBtn = document.getElementById("skipBtn-" + n),',
'      talkPanel = document.getElementById("talk-" + n), talkState = document.getElementById("talkState-" + n),',
'      talkPlay = document.getElementById("talkPlay-" + n);',
'  var isShow = (key === "showcase");',
'  var TALK_TEXT = (sec.querySelector(".p3-question") || { textContent: "" }).textContent.replace(/["\\u201c\\u201d]/g, "").trim() + " " + (isShow ? TALK_GUIDE_SHOWCASE : TALK_GUIDE);',
'  var st = window.__walkSpeech = window.__walkSpeech || { state: "idle" };',
'  function setTalk(on){ if (talkPanel) talkPanel.classList.toggle("speaking", !!on); if (talkState) talkState.textContent = on ? "On air — playing" : "Paused"; if (talkPlay) talkPlay.textContent = on ? "❚❚ Pause" : "▶ Play"; if (playBtn) playBtn.classList.toggle("playing", !!on); }',
'  function speakQuestion(){',
'    try {',
'      if (!("speechSynthesis" in window) || !window.speechSynthesis){ showStatus(speakNote, "Naya\'s voice plays on your phone — her real recording comes next."); return; }',
'      if (window.speechSynthesis.speaking || window.speechSynthesis.pending){ window.speechSynthesis.cancel(); st.state = "stopped"; setTalk(false); return; }',
'      var u = new SpeechSynthesisUtterance(TALK_TEXT);',
'      u.onstart = function(){ st.state = "playing"; setTalk(true); };',
'      u.onend = function(){ st.state = "ended"; setTalk(false); };',
'      u.onerror = function(){ st.state = "error"; setTalk(false); };',
'      window.speechSynthesis.speak(u); st.state = "playing"; setTalk(true);',
'    } catch (e) { st.state = "error"; setTalk(false); }',
'  }',
'  function playGlow(){ if (!playBtn) return; playBtn.classList.add("pending-glow"); setTimeout(function(){ playBtn.classList.remove("pending-glow"); }, 900); }',
'  function startDictation(){',
'    var SR = window.SpeechRecognition || window.webkitSpeechRecognition;',
'    if (!SR){ showStatus(speakNote, "Speaking isn\'t available in this browser — type it in instead."); hideStatus(enterNote); return; }',
'    var rec = new SR(); rec.lang = "en-US"; rec.interimResults = false; rec.maxAlternatives = 1;',
'    speakBtn.classList.add("live"); hideStatus(speakNote); hideStatus(enterNote); speakNote.textContent = "Listening…"; speakNote.hidden = false;',
'    rec.onresult = function(e){ var t = e.results[0][0].transcript || ""; markMine(answer); answer.value = answer.value ? (answer.value.replace(/\\s+$/, "") + " " + t) : t; answer.focus(); };',
'    rec.onerror = function(){ showStatus(speakNote, "Couldn\'t hear that — try again, or type it in."); };',
'    rec.onend = function(){ speakBtn.classList.remove("live"); if (speakNote.textContent === "Listening…") speakNote.hidden = true; };',
'    try { rec.start(); } catch (err){ speakBtn.classList.remove("live"); showStatus(speakNote, "Speaking couldn\'t start here — type it in instead."); }',
'  }',
'  function pasteIntoBox(){ if (navigator.clipboard && navigator.clipboard.readText){ navigator.clipboard.readText().then(function(t){ if (t){ markMine(answer); answer.value = answer.value ? (answer.value.trimEnd() + " " + t) : t; } answer.focus(); }).catch(function(){ answer.focus(); }); } else { answer.focus(); } }',
'  function submitAnswer(){',
'    if (answer.hasAttribute("data-example")){ showStatus(enterNote, "That\'s Naya\'s example — tap EDIT and make it yours, then Enter."); return; }',
'    if (!answer.value.trim()){ showStatus(enterNote, "Say it first — speak, type, or paste your answer, then Enter."); return; }',
'    box.answers[key] = answer.value; saveBox(); hideStatus(speakNote); showStep(nextAfter("step-" + n));',
'  }',
'  function skip(){ hideStatus(speakNote); showStep(nextAfter("step-" + n)); }',
'  if (playBtn) playBtn.addEventListener("click", function(){ speakQuestion(); });',
'  if (talkPlay) talkPlay.addEventListener("click", function(){ speakQuestion(); });',
'  if (speakBtn) speakBtn.addEventListener("click", startDictation);',
'  if (enterBtn) enterBtn.addEventListener("click", submitAnswer);',
'  if (skipBtn) skipBtn.addEventListener("click", skip);',
'  if (answer){ answer.addEventListener("input", function(){ markMine(answer); hideStatus(speakNote); hideStatus(enterNote); }); answer.addEventListener("focus", function(){ hideStatus(speakNote); hideStatus(enterNote); }); }',
'  sec.querySelectorAll("[data-edit]").forEach(function(b){ b.addEventListener("click", function(){ var t = document.getElementById(b.getAttribute("data-edit")); if (!t) return; markMine(t); t.focus(); try { t.select(); } catch (e) {} }); });',
'  if (hintRow) hintRow.addEventListener("click", function(e){',
'    var b = e.target.closest(".p3-hint"); if (!b) return;',
'    hideStatus(speakNote); hideStatus(enterNote);',
'    var was = b.classList.contains("show");',
'    hintRow.querySelectorAll(".p3-hint.show").forEach(function(x){ x.classList.remove("show"); });',
'    if (playBtn) playBtn.classList.remove("show");',
'    if (!was) b.classList.add("show");',
'    var act = b.getAttribute("data-act");',
'    if (act === "play"){ speakQuestion(); }',
'    else if (act === "dictate"){ startDictation(); }',
'    else if (act === "focus"){ answer.focus(); }',
'    else if (act === "paste"){ pasteIntoBox(); }',
'    else if (act === "submit"){ submitAnswer(); }',
'  });',
'  hintRow.querySelectorAll(".p3-hint").forEach(function(h){',
'    function dismissOthers(){ hintRow.querySelectorAll(".p3-hint.show").forEach(function(x){ if (x !== h) x.classList.remove("show"); }); if (playBtn) playBtn.classList.remove("show"); }',
'    h.addEventListener("mouseenter", dismissOthers); h.addEventListener("focusin", dismissOthers);',
'  });',
'  if (playBtn){ playBtn.addEventListener("mouseenter", function(){ hintRow.querySelectorAll(".p3-hint.show").forEach(function(x){ x.classList.remove("show"); }); }); playBtn.addEventListener("focusin", function(){ hintRow.querySelectorAll(".p3-hint.show").forEach(function(x){ x.classList.remove("show"); }); }); }',
'  if (box.answers[key]){ answer.value = box.answers[key]; markMine(answer); }',
'}',
'QKEYS.forEach(function(k, i){ wireQuestion(i + 1, k); });',
'/* entry door */',
'var doorEnter = document.getElementById("enterBtn-door");',
'if (doorEnter) doorEnter.addEventListener("click", function(){ var first = 1; for (var i = 0; i < 16; i++){ if (!box.answers[QKEYS[i]]){ first = i + 1; break; } first = 16; } showStep("step-" + first); });',
'/* naming: live URL previews + reveal fill (locked scheme; placeholders until typed) */',
'function slug(s){ return (s || "").toLowerCase().trim().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "") || "yourname"; }',
'var namePersonal = document.getElementById("name-personal"), nameBusiness = document.getElementById("name-business"), nameSpace = document.getElementById("name-space");',
'var urlPersonal = document.getElementById("url-personal"), urlBusiness = document.getElementById("url-business"), urlSpace = document.getElementById("url-space");',
'function syncNames(){',
'  var alias = slug(namePersonal.value), biz = slug(nameBusiness.value), sp = slug(nameSpace.value);',
'  if (urlPersonal) urlPersonal.value = alias;',
'  var ba = document.getElementById("url-biz-alias"); if (ba) ba.textContent = alias;',
'  var sa = document.getElementById("url-space-alias"); if (sa) sa.textContent = alias;',
'  if (urlBusiness) urlBusiness.value = biz;',
'  if (urlSpace) urlSpace.value = sp;',
'  document.querySelectorAll("#revealDoors .rv-alias").forEach(function(el){ el.textContent = alias; });',
'  document.querySelectorAll("#revealDoors .rv-world").forEach(function(el){ el.textContent = sp; });',
'  /* THE GATE: every door goes to the pricing page FIRST (full page), carrying its destination in ?next=.',
'     The pricing page choice sends them in; the destination is also saved as pendingDoor so the return can resume.',
'     Pricing v77 does not read ?next= yet and performs no navigation of its own - the return leg is integration work owed (see report). */',
'  var PRICING = "https://nayanet.app/pricing";',
'  var d = function(k, dest){ var a = document.querySelector(\'#revealDoors [data-reveal="\' + k + \'"]\'); if (a){ a.href = PRICING + "?next=" + encodeURIComponent(dest); a.setAttribute("data-dest", dest); } };',
'  d("personal", "https://nayanet.app/" + alias);',
'  d("business", "https://nayanet.app/" + alias);',
'  d("world", "https://" + sp + ".nayanet.app");',
'  d("hub", "https://hub.nayanet.app/" + alias);',
'  d("dashboard", "https://dashboard.nayanet.app/" + alias);',
'  d("calendar", "https://calendar.nayanet.app/" + alias);',
'  d("about", "https://nayanet.app/" + alias + "/about");',
'  d("skills", "https://nayanet.app/" + alias + "/skills");',
'}',
'document.querySelectorAll("#revealDoors .p3-door").forEach(function(a){ a.addEventListener("click", function(){ box.pendingDoor = a.getAttribute("data-dest") || a.href; saveBox(); }); });',
'[namePersonal, nameBusiness, nameSpace].forEach(function(inp){ if (inp) inp.addEventListener("input", syncNames); });',
'var namesEnter = document.getElementById("enterBtn-names");',
'if (namesEnter) namesEnter.addEventListener("click", function(){ box.names = { personal: namePersonal.value, business: nameBusiness.value, space: nameSpace.value }; saveBox(); syncNames(); showStep("step-reveal"); });',
'var revealPlay = document.getElementById("playBtn-reveal");',
'if (revealPlay) revealPlay.addEventListener("click", function(){ revealPlay.classList.toggle("show"); });',
'var namesPlay = document.getElementById("playBtn-names");',
'if (namesPlay) namesPlay.addEventListener("click", function(){ namesPlay.classList.toggle("show"); });',
'/* boot: entry first; returning citizens resume at the first unanswered question */',
'if (box.names.personal && namePersonal) namePersonal.value = box.names.personal;',
'if (box.names.business && nameBusiness) nameBusiness.value = box.names.business;',
'if (box.names.space && nameSpace) nameSpace.value = box.names.space;',
'syncNames();',
'var anyAnswered = QKEYS.some(function(k){ return !!box.answers[k]; });',
'if (anyAnswered){ var first = 16; for (var i = 0; i < 16; i++){ if (!box.answers[QKEYS[i]]){ first = i + 1; break; } } showStep("step-" + first); }',
'else { showStep("step-door"); }',
'})();'
].join('\n');

/* ---------- assemble ---------- */
const styleBlock = '<style id="walk-15-slides">\n/* STAGE FRAME — HARVESTED VERBATIM, agreement blob 1f0b0474 L340-348 (API-verified) */\n' + frameCss + '\n/* POWERCAST — HARVESTED VERBATIM, Personal L5644-5676 + L36863,64,66,67 */\n' + pcTopBtnCss + '\n' + saShellCss + '\n' + layoutCss + '\n' + namesCss + '\n</style>';
const headWithStyles = headHtml.replace('</head>', styleBlock + '\n' + endStyle + '\n</head>');
if (headWithStyles === headHtml) throw new Error('head style injection failed');
const bodyAfterOpen = bodyOpen.slice('<body>'.length);
const out = headWithStyles + '\n<body>\n<div class="naya-frame" aria-hidden="true"><div class="frame-light"></div></div>\n' + bodyAfterOpen + entryWithEnter + '\n' + steps.join('\n') + '\n' + namesSec + '\n' + revealSec + '\n' + endSec + '\n<script>\n' + engineJs + '\n</script>\n' + endScript + '\n</body>\n</html>\n';

/* ---------- checks on the built file ---------- */
chk((out.match(/class="p3-step p3-qstep"/g) || []).length === 16, '16 qsteps');
chk((out.match(/data-example="1"/g) || []).length === 15, '15 pre-filled example boxes');
chk((out.match(/class="p3-talk"/g) || []).length === 16, '16 talking boxes');
chk((out.match(/class="p3-qa-row"/g) || []).length === 16, '16 side-by-side rows');
chk((out.match(/class="p3-answer-edit"/g) || []).length === 16, '16 Edit buttons');
chk((out.match(/class="p3-skip"/g) || []).length === 16, '16 Skip buttons');
chk((out.match(/<a class="p3-door" data-reveal="/g) || []).length === 8, '8 reveal doors');
chk(!out.includes('data-reveal="seventh"') && !out.includes('reveal-7'), 'no separate seventh button (the gate IS the doors)');
chk(out.includes('<div class="naya-frame"'), 'naya-frame div present');
chk(out.includes(frameLines[0]) && out.includes(frameLines[8]), 'agreement L340-348 verbatim in output');
chk(out.includes('.powercast-topbtn{') && out.includes('.sa-theatre-bar{'), 'PowerCast CSS verbatim in output');
chk(out.includes('On air — playing') && out.includes('❚❚ Pause'), 'saPcSync state strings in output');
chk(!out.includes(' of 10'), 'no "of 10" left');
chk((out.match(/<p class="p3-progress">\d+ of 15<\/p>/g) || []).length === 15, '"N of 15" x15');
chk(out.includes('Your showcase — optional'), 'showcase progress line');
chk(!out.includes('What are you into, and why?'), 'no leftover slide-02 question');
chk(!out.includes('choice-1-A') && !out.includes('p3-choice"'), 'no A/B/C boards (slide look as sent)');
chk(out.includes('"Welcome starts with your certificate."'), 'entry door present');
chk(out.includes('id="step-names"') && out.includes('"Name your world."'), 'naming page present');
chk(out.includes('"Congratulations, you\'re hired."') && out.includes('Welcome complete'), 'end slide present');
chk(out.includes('https://hub.nayanet.app/') && out.includes('https://dashboard.nayanet.app/') && out.includes('https://calendar.nayanet.app/'), 'locked-scheme reveal hrefs present');
chk((out.match(/https:\/\/nayanet\.app\/pricing\?next=/g) || []).length === 8, 'all 8 doors gate through pricing ?next=');
chk(out.includes('data-reveal="about"') && out.includes('data-reveal="skills"') && out.includes('/about') && out.includes('/skills'), 'About + Skills deep-link doors present');
chk(out.includes('choose your plan') && out.includes('Naya Power') && out.includes('Naya Pro') && out.includes('Naya Max'), 'gate line on the reveal page');
Q.forEach(function(q){ chk(out.includes('data-key="' + q.key + '"'), 'key present: ' + q.key); chk(out.includes(esc(q.heading)), 'heading present: ' + q.key); });
try { new Function(engineJs); chk(true, 'engine script parses'); } catch (e) { chk(false, 'engine script parses: ' + e.message); }
console.log('BUILT bytes=' + Buffer.byteLength(out, 'utf8') + ' sha256=' + sha256(out) + ' blob=' + gitBlobSha(out));

/* ---------- output: stdout pipe preferred (EPERM flake blocks file writes) ---------- */
if (process.env.WALK15_STDOUT === '1') {
  const b64 = Buffer.from(out, 'utf8').toString('base64');
  console.log('WALK15_BEGIN');
  for (let i = 0; i < b64.length; i += 76) console.log(b64.slice(i, i + 76));
  console.log('WALK15_END');
  console.log('WALK15_BYTES=' + Buffer.byteLength(out, 'utf8') + ' WALK15_SHA256=' + sha256(out) + ' WALK15_BLOB=' + gitBlobSha(out));
} else {
  const OUT_P = process.env.WALK15_OUT || (LANE + '/walk-15-slides.html');
  const sleepSync = ms => { try { Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, ms); } catch (e) {} };
  let attempt = 0;
  for (;;) {
    attempt++;
    try { fs.writeFileSync(OUT_P, out); } catch (e) { console.log('write attempt ' + attempt + ' failed: ' + e.message); }
    try {
      const back = fs.readFileSync(OUT_P);
      if (back.length === Buffer.byteLength(out, 'utf8') && sha256(back) === sha256(out)) break;
      console.log('write attempt ' + attempt + ' landed wrong size/sha: ' + back.length + ' vs ' + Buffer.byteLength(out, 'utf8'));
    } catch (e) { console.log('write attempt ' + attempt + ' read-back failed: ' + e.message); }
    if (attempt >= 30) throw new Error('write never landed after 30 attempts');
    sleepSync(2000);
  }
  console.log('WROTE ' + OUT_P + ' bytes=' + Buffer.byteLength(out, 'utf8') + ' sha256=' + sha256(out) + ' git-blob=' + gitBlobSha(out));
}
console.log('DONE');
