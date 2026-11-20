#!/usr/bin/env node
/* FIX-4 maker transform — CSS/layout-only at <=480px, defects A-F.
   Reads the verified fix-3 base files in this dir, applies the six fixes,
   writes fix4-*.html here, prints sizes + sha256. Every replacement is
   anchored on a unique string and asserted to occur exactly once.
   NO flow JS is touched; no board content, no F9 code, no desktop rules. */
const fs = require('fs');
const crypto = require('crypto');
const HERE = __dirname;
function sha(b) { return crypto.createHash('sha256').update(b).digest('hex'); }
function rep(file, s, anchor, insert, label) {
  const n = s.split(anchor).length - 1;
  if (n !== 1) throw new Error(`${file} ${label}: anchor occurs ${n}x (want 1): ${JSON.stringify(anchor.slice(0, 90))}`);
  return s.replace(anchor, anchor + insert);
}
function load(n) { return fs.readFileSync(`${HERE}/${n}`, 'utf8'); }
function emit(n, s) {
  fs.writeFileSync(`${HERE}/${n}`, s);
  const b = Buffer.byteLength(s);
  console.log(`FIXED4 ${n}: ${b} B sha256 ${sha(s)}`);
  return { name: n, bytes: b, sha: sha(s) };
}
const out = {};

// ---------- identity: A (hero name clears the title) + C (banner clears the jewels) ----------
let id = load('identity-fixed.html');
id = rep('identity', id,
  '       certified rule sets display on .alias-status, so nothing else changes. */\n    .cert-plaque.is-certified .alias-status { display: none; }',
  `
    /* FIX4 (2026-11-20, fix-3 eye A + C) — phone width only. A: the hero
       name (52px, floating above the entry) covered the certificate title
       (17px overlap x 346px at 390). The name shrinks to 28px and the
       name-bearing zone gains 16px, so the name sits on its own line
       between the title and the entry. C: the taken-note banner's first
       line was clipped by the bottom corner crests (76px) and its middle
       by the bottom-center frame stone — the text now clears the crests
       (76px side padding) and the stone is hidden while the taken note
       shows (taken state only, phone only; the stone is aria-hidden
       decoration). No desktop rule touched. */
    @media (max-width: 480px) {
      .cert-name { font-size: clamp(1.75rem, 7.2vw, 2rem); }
      .cert-plaque.taken .face-center, .cert-plaque.is-certified .face-center, .cert-plaque.has-name .face-center { margin-top: 16px; }
      .hub-note.taken-note { padding-left: 76px; padding-right: 76px; }
      .cert-plaque.taken .frame-stone { display: none; }
    }`,
  'A+C-block');
out.identity = emit('fix4-identity-fixed.html', id);

// ---------- walk: B (door heading clears the corner jewels) ----------
let walk = load('walk-beginning-fixed.html');
walk = rep('walk', walk,
  '.p3-main{padding:6px 18px 2px}\n.p3-question{margin:8px 0 14px}',
  `
/* FIX4 (2026-11-20, fix-3 eye B) — phone width only: the door heading ran
   under the fixed corner jewels (54-76px at the viewport corners, 4620px2
   overlap each side at 390). The door's own question gets 80px side
   padding so its first and last letters clear the jewels. Other steps
   are untouched (their headings sit below the flank header). */
#step-door .p3-question{padding-left:80px;padding-right:80px}`,
  'B-door-h1');
out.walk = emit('fix4-walk-beginning-fixed.html', walk);

// ---------- unfold: D (final-board title clears the top-right controls) ----------
let un = load('agreement-unfold-fixed.html');
un = rep('unfold', un,
  '@media(max-width:480px){.p3-deal-unfold{padding:22px 12px 26px}}',
  `@media(max-width:480px){.p3-deal-unfold{padding:22px 12px 26px}
/* FIX4 (2026-11-20, fix-3 eye D) — phone width only: the board title
   ("Congratulations", one unbreakable word at 25px) ran under the
   top-right diamond orb + avatar. At 22px the word fits its box with
   room to spare on both the unfold and the deck. Desktop untouched. */
.ib-title{font-size:22px}}`,
  'D-unfold-title');
out.unfold = emit('fix4-agreement-unfold-fixed.html', un);

// ---------- welcome: D (deck/letter title) + E (deck sign photo below the text box) ----------
let wel = load('welcome-staged.html');
wel = rep('welcome', wel,
  '@media(max-width:480px){body.fp-stage-on #fpAgreement .fp-now .deal-beat-photo,body.fp-stage-on #fpLegal .fp-now .deal-beat-photo{width:104px!important;height:104px!important}}',
  `@media(max-width:480px){body.fp-stage-on #fpAgreement .fp-now .deal-beat-photo,body.fp-stage-on #fpLegal .fp-now .deal-beat-photo{width:104px!important;height:104px!important}
/* FIX4 (2026-11-20, fix-3 eye D) — phone width only: same 22px board
   title as the unfold, so "Congratulations" clears the top-right
   speak-face photo on the deck/letter final board. */
#fpAgreement .ib-title,#fpLegal .ib-title{font-size:22px}
/* FIX4 (2026-11-20, fix-3 eye E) — phone width only, deck/letter final
   board: the big sign photo sat over the text box's last lines. The
   sign frame is pushed 64px down so the photo sits below the text box,
   as at desktop. (F: the footer links strip scrolls — proven by scroll
   test, scrollWidth 1064 > clientWidth 374 — so no change here.) */
body.fp-stage-on #fpAgreement .fp-now .deal-sign-frame,body.fp-stage-on #fpLegal .fp-now .deal-sign-frame{margin-top:64px!important}}`,
  'D+E-welcome');
out.welcome = emit('fix4-welcome-staged.html', wel);

console.log(JSON.stringify(out, null, 1));
