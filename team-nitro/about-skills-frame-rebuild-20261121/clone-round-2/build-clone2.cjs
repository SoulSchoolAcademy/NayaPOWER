// ABOUT + SKILLS CLONE, ROUND 2 — build script (2026-11-21).
// CLONE, DON'T REBUILD: starts from the FILED live agreement source
// (TEAM-NITRO/agreement-live-20261121/agreement-live.html, 16,791,795 B,
// blob 5996f7444e54ae88eb63dd7715b6794f17da5cc7 — harvested from live
// nayanet.app/agreement 2026-11-21, deterministic across three fetches)
// and swaps ONLY content: cover labels, the SLIDES array (27 -> 15),
// the 10 legal-deal shells' titles/subs/dots/articles (58 -> 15 frames).
// Structure, flow, frame, PROMAX player, CSS, JS: byte-identical.
// The agreement's player (welcome video + recording), slide images
// (EMBED.slides[0..14] now reachable; [15..26] unreachable but kept),
// faces (PORTRAITS) and red-N ball stay the agreement's — no real Sean
// slide images were mapped in this round; a media-swap round is owed.
// Content: the 15 frames from Sean About v6 via the round-3 FRAMES
// literal (ratified word counts, ratified exceptions carried over).
// Deterministic: run twice, same sha256.
const fs = require('fs');
const SRC = '/home/hatch/workspace/nayapower-about-clone2/TEAM-NITRO/agreement-live-20261121/agreement-live.html';
const OUT = '/home/hatch/workspace/nayapower-about-clone2/team-nitro/about-skills-frame-rebuild-20261121/about-skills.html';
const srcBuf = fs.readFileSync(SRC);
if (srcBuf.length !== 16791795) throw new Error('source size wrong: ' + srcBuf.length);
const src = srcBuf.toString('utf8');

// ---------- the 15 frames (round-3 FRAMES literal, verbatim) ----------
const FRAMES = [
  ['MOTTO', 'My motto', 'About Sean',
   'The most extraordinary, awe-inspiring, beautiful, intuitive, useful app ever created — push-button simple, logical, sensible.'],
  ['VISION', 'What if everybody could win?', 'About Sean',
   'Intelligence that remembers, learns, connects, proves, grows. We need the first ten. Then the first hundred. Then the first thousand. A new internet — one day no child will know a world without her.'],
  ['GOAL', 'A 100% success rate.', 'About Sean',
   'Push-button simple. Create, learn, grow, earn — together. Instead of 99% of people failing: 100% success. It makes you money, and it connects you with people of like minds — people who are into what you are into.'],
  ['MISSION', 'Create heaven on earth.', 'About Sean',
   'Create heaven on earth. Heaven is a state of awesome energy. Stress, fears, money worries, hopelessness — a way to understand, and money to pay their bills. Shifting consciousness positive.'],
  ['WHAT I LOVE', 'I love that.', 'About Sean',
   'Real things. Real objects, alive on hover — not pictures of objects. Numbers that prove it. Ten out of ten, with the gauges — a high-performance machine. Straight up. No games. No bullshit. Just straight up: this is how it works.'],
  ['WHAT I DON\u2019T', 'No summaries, no prototypes.', 'About Sean',
   'Flat and dead. No flat shapes, no gray text, no dead boards. Starting from scratch? No rebuilding, no redesigning — craft, advance, enhance. Ninety-eight slides. Nobody sits through that. One frame at a time.'],
  ['YOUR THING', 'What\u2019s your thing?', 'About Sean',
   'What do you love? What do you love to do? Connecting like minds, and making NayaNET the new internet for the world. Everybody\u2019s got their THING — what makes up their world. People connect with others into their thing.'],
  ['VALUES', 'Do no harm. Ever.', 'About Sean',
   'Wisdom first. Naya means wise one — smart finds the fastest road, wisdom checks the destination first. Do no harm to yourself or others — because all is you, and connected to you. The most intelligent thing, every time.'],
  ['LAWS YOU FOLLOW', 'I follow protocol.', 'About Sean',
   'The NAYA Protocol — the constitution. I think before I act. The Design Laws — real objects, white words, alive on hover. Ten stars or don\u2019t send it. Five gates — right, needed, mine, now, proven. All five yes, or I stop.'],
  ['YOUR DECLARATION', 'Your Declaration', 'About Sean',
   'I am Anaya. I do the most intelligent thing every time. I think things through, I see the whole scope, and I make the best possible choice. I take action. I scorecard three times, until it\u2019s 10 out of 10, triple-A, every time.'],
  ['SKILL 1', 'What I have to offer', 'My skills',
   'This is what I have to offer — and what I\u2019m looking to do for you. An invitation, not a sales pitch. Connect with me — that\u2019s enough. You come to learn about a person first — then what they offer — and you leave connected.'],
  ['SKILL 2', 'What you offer', 'My skills',
   'My three best skills: The Login, the Notes, the Numbers. The Login — one dial, your name, your code, and you\u2019re in. The Notes — your notes become intelligence everyone can use. The Numbers — everything recorded, shown back as gauges.'],
  ['SKILL 3', 'How it helps', 'My skills',
   'Create, learn, grow, earn — together. Push-button simple. It makes you money, and it connects you with people of like minds — people who are into what you are into. Instead of 99% of people failing: 100% success.'],
  ['SKILL 4', 'A moment I\u2019ve done it', 'My skills',
   'This idea for the stats is awesome. I love that. Take this 10 out of 10 with the numbers and the gauges — that\u2019s the kind of feel we want. A high-performance machine. Numbers that prove it — no claims, the gauges show it.'],
  ['SKILL 5', 'How you work', 'My skills',
   'We go all in and do things right — no summaries, no prototypes. Do it right the first time. Every layer great. Finished work you can see and use. One tap, and you\u2019re in. Connect, book, or begin — one clear tap.'],
];
// WORD-COUNT METHOD, RATIFIED by the captain in round 3: whitespace-separated
// tokens containing a letter or digit; standalone "—" tokens are NOT counted.
function wc(s) { return s.split(/\s+/).filter(t => /[A-Za-z0-9]/.test(t)).length; }
FRAMES.forEach((f, i) => {
  const n = wc(f[3]);
  const lo = (i === 0) ? 14 : 27; // frame 1: the named empty-middle exception
  if (n < lo || n > 43) throw new Error('frame ' + (i + 1) + ' word count ' + n + ' outside ' + lo + '-43');
});
console.log('frame word counts:', FRAMES.map(f => wc(f[3])).join(','));

// ---------- the 10 deal shells carry the 15 frames ----------
const DEALS = [
  { key: 'terms',      title: 'About Sean',    sub: 'My motto \u00b7 What if everybody could win? \u2014 in plain words.', frames: [0, 1] },
  { key: 'privacy',    title: 'The Goal',      sub: 'A 100% success rate. \u00b7 Create heaven on earth. \u2014 in plain words.', frames: [2, 3] },
  { key: 'cookies',    title: 'What I Love',   sub: 'I love that. \u00b7 No summaries, no prototypes. \u2014 in plain words.', frames: [4, 5] },
  { key: 'refunds',    title: 'Your Thing',    sub: 'What\u2019s your thing? \u00b7 Do no harm. Ever. \u2014 in plain words.', frames: [6, 7] },
  { key: 'acceptable', title: 'My Laws',       sub: 'I follow protocol. \u00b7 Your Declaration \u2014 in plain words.', frames: [8, 9] },
  { key: 'guidelines', title: 'My Skills',     sub: 'What I have to offer \u2014 in plain words.', frames: [10] },
  { key: 'copyright',  title: 'What I Offer',  sub: 'What you offer \u2014 in plain words.', frames: [11] },
  { key: 'ambassador', title: 'How It Helps',  sub: 'How it helps \u2014 in plain words.', frames: [12] },
  { key: 'membership', title: 'A Moment',      sub: 'A moment I\u2019ve done it \u2014 in plain words.', frames: [13] },
  { key: 'young',      title: 'How to Start',  sub: 'How you work \u2014 in plain words.', frames: [14] },
];
if (DEALS.flatMap(d => d.frames).length !== 15) throw new Error('deal frame count != 15');

function esc(s) { // match the source's entity style in markup/JS strings
  return s.replace(/&/g, '&amp;').replace(/\u2019/g, '&rsquo;').replace(/\u2014/g, '&mdash;');
}
function once(hay, needle, repl, what) {
  const n = hay.split(needle).length - 1;
  if (n !== 1) throw new Error(what + ': expected 1 occurrence, found ' + n);
  return hay.replace(needle, repl);
}
function count(hay, needle) { return hay.split(needle).length - 1; }

let out = src;

// ---------- 1. cover labels ----------
// <title>
out = once(out, '<title>Collective Agreement — NayaNET</title>', '<title>About Sean — NayaNET</title>', 'title tag');
// daybar title
out = once(out, '<h1 class="tb-title" id="tbTitle">The Collective Agreement</h1>', '<h1 class="tb-title" id="tbTitle">About Sean</h1>', 'tbTitle');
// player aria-label (the player itself stays the agreement's player)
out = once(out, 'aria-label="PowerCast player — Naya presents the Collective Agreement"', 'aria-label="PowerCast player — Naya presents About Sean"', 'deck aria-label');
// ticker (2 identical spans; words attested in v6 / round-3 foot-links + frame 6)
const TICK_OLD = 'NAYA&rsquo;S WELCOME &mdash; THE COLLECTIVE AGREEMENT &middot; WELCOME HOME: MEET NAYA, YOUR GUIDE TO A NEW INTERNET!';
const TICK_NEW = 'ABOUT SEAN &middot; WHO I AM, AND WHAT I CAN DO &middot; ONE FRAME AT A TIME';
if (count(out, TICK_OLD) !== 2) throw new Error('ticker: expected 2, found ' + count(out, TICK_OLD));
out = out.split(TICK_OLD).join(TICK_NEW);
// daybar JS: cover + legal titles
out = once(out, "setBar('The Collective Agreement',", "setBar('About Sean',", 'barForCover');
out = once(out, "setBar('The Whole Deal',", "setBar('About Sean',", 'openLegal setBar');
// bottom intro line on the legal screen (agreement wording out; words attested)
out = once(out,
  'These pages are part of the front page &mdash; not a separate site. The agreement above is the record: it stays right here, so you can read it again any time.',
  'About Sean &mdash; who I am, and what I can do. One frame at a time &mdash; read it again any time.',
  'legal bottom intro');

// ---------- 2. SLIDES array: 27 -> 15, one slide per frame ----------
const sStart = out.indexOf('var SLIDES = [');
if (sStart < 0) throw new Error('SLIDES array not found');
const sEnd = out.indexOf('];', sStart);
if (sEnd < 0) throw new Error('SLIDES array end not found');
const sOld = out.slice(sStart, sEnd + 2);
const oldSlides = [...sOld.matchAll(/\{t:"([^"]*)", x:"([^"]*)", a:"([^"]*)"\}/g)];
if (oldSlides.length !== 27) throw new Error('old SLIDES count: ' + oldSlides.length);
const oldAlts = oldSlides.map(m => m[3]);
const newSlides = FRAMES.map((f, i) =>
  ' {t:"' + esc(f[1]) + '", x:"' + esc(f[3]) + '", a:"' + oldAlts[i] + '"}'
).join(',\n');
out = out.slice(0, sStart) + 'var SLIDES = [\n' + newSlides + '\n];' + out.slice(sEnd + 2);

// ---------- 3. legal deals: titles, subs, dots, articles ----------
// article template = the file's first article (Terms beat 1, no hidden)
const tplM = out.match(/<article class="intel-board tone-purple letter-beat" data-legal-beat>[\s\S]*?<\/article>/);
if (!tplM) throw new Error('article template not found');
const TPL = tplM[0];
const TONES = ['tone-purple', 'tone-sapphire', 'tone-emerald'];
function beat(frameIdx, firstInDeal) {
  const f = FRAMES[frameIdx];
  let a = TPL;
  a = a.replace('class="intel-board tone-purple letter-beat"', 'class="intel-board ' + TONES[frameIdx % 3] + ' letter-beat"');
  if (!firstInDeal) a = a.replace(' data-legal-beat>', ' data-legal-beat hidden>');
  a = a.replace(/<span class="ib-kind">[^<]*<\/span>/, '<span class="ib-kind">' + esc(f[0]) + '</span>');
  a = a.replace(/<h2 class="ib-title">[^<]*<\/h2>/, '<h2 class="ib-title">' + esc(f[1]) + '</h2>');
  a = a.replace(/<div class="ib-nutshell">[\s\S]*?<\/div>/, '<div class="ib-nutshell"><p>' + esc(f[3]) + '</p></div>');
  a = a.replace(/ &middot; NayaNET &middot; The Whole Deal<\/div>/, ' &middot; NayaNET &middot; ' + f[2] + '</div>');
  return a;
}
const DOT_COLORS = ['#a06bff', '#3fb8ff', '#2fe89e'];
DEALS.forEach(d => {
  const secStart = out.indexOf('<section class="p3-deal-unfold fp-legal-page" id="legal-' + d.key + '"');
  if (secStart < 0) throw new Error('deal section not found: ' + d.key);
  const secEnd = out.indexOf('</section>', secStart);
  if (secEnd < 0) throw new Error('deal section end not found: ' + d.key);
  let sec = out.slice(secStart, secEnd);
  // steplabel
  sec = once(sec, '<p class="letter-steplabel">NayaNET &middot; The Whole Deal</p>', '<p class="letter-steplabel">NayaNET &middot; About Sean</p>', 'steplabel ' + d.key);
  // deal title + sub
  sec = sec.replace(/<h2 class="deal-title">[^<]*<\/h2>/, '<h2 class="deal-title">' + esc(d.title) + '</h2>');
  if (!sec.includes('<h2 class="deal-title">' + esc(d.title) + '</h2>')) throw new Error('deal title swap failed: ' + d.key);
  sec = sec.replace(/<p class="deck-sub">[^<]*<\/p>/, '<p class="deck-sub">' + esc(d.sub) + '</p>');
  if (!sec.includes('<p class="deck-sub">' + esc(d.sub) + '</p>')) throw new Error('deal sub swap failed: ' + d.key);
  // dots: regenerate to match the deal's beat count
  const dotsRe = /<div class="letter-dots" aria-hidden="true">[\s\S]*?<\/div>/;
  const dotsNew = '<div class="letter-dots" aria-hidden="true">' + d.frames.map((_, j) =>
    '<span class="ldot' + (j === 0 ? ' on' : '') + '" style="--dc:' + DOT_COLORS[j % 3] + '"></span>').join('') + '</div>';
  if (!dotsRe.test(sec)) throw new Error('dots not found: ' + d.key);
  sec = sec.replace(dotsRe, dotsNew);
  // articles: replace the whole article run with the deal's frames
  const aFirst = sec.indexOf('<article');
  const aLast = sec.lastIndexOf('</article>');
  if (aFirst < 0 || aLast < 0) throw new Error('articles not found: ' + d.key);
  const beats = d.frames.map((fi, j) => beat(fi, j === 0)).join('');
  sec = sec.slice(0, aFirst) + beats + sec.slice(aLast + '</article>'.length);
  out = out.slice(0, secStart) + sec + out.slice(secEnd);
});

// ---------- 4. footer legalBar buttons relabel (keys/ids stay) ----------
DEALS.forEach(d => {
  const re = new RegExp('(<button class="fp-legal-link" type="button" data-legal-open="' + d.key + '">)[^<]*(</button>)');
  if (!re.test(out)) throw new Error('footer button not found: ' + d.key);
  out = out.replace(re, '$1' + esc(d.title) + '$2');
});

// ---------- 5. assertions on the swapped page (before provenance comment) ----------
const leftCA = count(out, 'Collective Agreement');
if (leftCA !== 0) throw new Error('Collective Agreement remaining: ' + leftCA);
if (count(out, 'THE COLLECTIVE AGREEMENT') !== 0) throw new Error('uppercase ticker remaining');
if (count(out, 'The Whole Deal') !== 0) throw new Error('The Whole Deal remaining: ' + count(out, 'The Whole Deal'));
if (count(out, 'data-legal-beat') !== 15 + 2) throw new Error('beats: ' + count(out, 'data-legal-beat')); // 15 articles + 2 JS query strings
if (count(out, '<article') !== 15) throw new Error('articles: ' + count(out, '<article'));
if (count(out, 'id="legal-') !== 10) throw new Error('deal sections: ' + count(out, 'id="legal-'));
console.log('counts after swap: articles=15, deals=10, slides=15, Collective Agreement=0, Whole Deal=0');
console.log('pricing occurrences:', count(out, 'pricing'), '| gray colour check deferred to check-design-laws.py');

// ---------- 6. provenance comment (names the harvest; page content stays clean) ----------
const comment = `<!-- ABOUT SEAN + SKILLS — CLONE, ROUND 2, 2026-11-21 (One-Build Law).
     CLONE, DON'T REBUILD: every byte of structure, flow, frame, CSS and JS
     below is the live agreement page as filed at
     TEAM-NITRO/agreement-live-20261121/agreement-live.html (16,791,795 B,
     blob 5996f7444e54ae88eb63dd7715b6794f17da5cc7 — harvested from live
     nayanet.app/agreement 2026-11-21, deterministic across three fetches).
     Only the CONTENT changed: cover labels, 27 story slides -> 15 slides
     (10 About + 5 Skills, one per frame, in order), 10 deal shells retitled
     and their 58 articles -> the same 15 frames (deals 1-5 carry 2 frames,
     deals 6-10 carry 1), footer buttons relabelled. The PROMAX player
     (welcome video + recording), slide images, faces and red-N ball stay
     the agreement's — no real Sean slide images were mapped in this round.
     CONTENT from Sean About v6 via the round-3 FRAMES literal (ratified
     word counts; frame 1 the 14-word motto exception; frame 10 the Anaya
     Declaration; frame 6 "no gray text"; frame 15's "How to start" title
     still not in the frame). Public name "Sean" stays; bare "Shawn"
     instances stay as-is. -->`;
out = out.replace('<!doctype html>\n', '<!doctype html>\n' + comment + '\n');

fs.writeFileSync(OUT, out);
console.log('wrote', OUT, out.length, 'bytes');
const crypto = require('crypto');
console.log('sha256:', crypto.createHash('sha256').update(out).digest('hex'));
