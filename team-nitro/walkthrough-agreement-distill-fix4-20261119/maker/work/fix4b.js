#!/usr/bin/env node
/* FIX-4b maker transform — corrections after the fix-4 verification probe.
   Operates on the fix4-*.html files in this dir; writes fix4b-*.html.
   1. identity: hide .cert-certifies at <=480px while the hero name shows
      (taken / is-certified / has-name). The line sits in flow directly
      above the face-center and the 28px hero (anchored 10px above the
      center) covers it (2356 px2 overlap, taken state, 390) — the 48px
      slot between title and center cannot hold both a 20px line and a
      28px name; shrinking the line (13px) + more margin still left 828
      px2 overlap in a live-CSS experiment, while hiding it gives 0/0/0.
      The line still shows in the plain (no-name) state at every width.
   2. unfold: the board-37 title is .frame-title, NOT .ib-title — the
      first D rule never matched. Replace it with a board-37-scoped
      .frame-title rule that beats .frame-title{25px!important}
      ((0,2,1)!important vs (0,1,0)!important). Also collapse the doubled
      @media(max-width:480px){.p3-deal-unfold{...}} block back to one.
   3. welcome: the deck/letter board-37 title is governed by
      body.af-deck-on #deckBody .ib-title{25px!important} ((1,2,1)).
      Replace the losing #fpAgreement .ib-title rule with a board-37
      rule at (1,3,2)!important, covering deck AND letter (both carry
      body.af-deck-on and #deckBody).
   CSS/layout-only at <=480px. No flow JS touched. */
const fs = require('fs');
const crypto = require('crypto');
const HERE = __dirname;
function sha(b) { return crypto.createHash('sha256').update(b).digest('hex'); }
function rep(file, s, anchor, insert, label) {
  const n = s.split(anchor).length - 1;
  if (n !== 1) throw new Error(`${file} ${label}: anchor occurs ${n}x (want 1): ${JSON.stringify(anchor.slice(0, 90))}`);
  return s.replace(anchor, insert);
}
function load(n) { return fs.readFileSync(`${HERE}/${n}`, 'utf8'); }
function emit(n, s) {
  fs.writeFileSync(`${HERE}/${n}`, s);
  const b = Buffer.byteLength(s);
  console.log(`FIXED4b ${n}: ${b} B sha256 ${sha(s)}`);
  return { name: n, bytes: b, sha: sha(s) };
}
const out = {};

// ---------- identity: hide the certifies line while the hero shows ----------
let id = load('fix4-identity-fixed.html');
id = rep('identity', id,
  '      .cert-plaque.taken .frame-stone { display: none; }\n    }',
  `      .cert-plaque.taken .frame-stone { display: none; }
      /* FIX4b (2026-11-20): "This certifies that" sits in flow directly
         above the center, and the 28px hero covers it (2356 px2, taken
         state) — the slot cannot hold both. While the hero name shows,
         the line hides at phone width; it still shows with no name. */
      .cert-plaque.taken .cert-certifies, .cert-plaque.is-certified .cert-certifies, .cert-plaque.has-name .cert-certifies { display: none; }
    }`,
  'A-line-hide');
out.identity = emit('fix4b-identity-fixed.html', id);

// ---------- unfold: board-37 .frame-title, collapse the doubled media block ----------
let un = load('fix4-agreement-unfold-fixed.html');
un = rep('unfold', un,
  '@media(max-width:480px){.p3-deal-unfold{padding:22px 12px 26px}}@media(max-width:480px){.p3-deal-unfold{padding:22px 12px 26px}\n/* FIX4 (2026-11-20, fix-3 eye D) — phone width only: the board title\n   ("Congratulations", one unbreakable word at 25px) ran under the\n   top-right diamond orb + avatar. At 22px the word fits its box with\n   room to spare on both the unfold and the deck. Desktop untouched. */\n.ib-title{font-size:22px}}',
  `@media(max-width:480px){.p3-deal-unfold{padding:22px 12px 26px}
/* FIX4b (2026-11-20, fix-3 eye D) — phone width only: board 37's title is
   .frame-title, not .ib-title (the first D rule never matched), and it is
   governed by .frame-title{font-size:25px!important}. This board-37 rule
   at (0,2,1)!important beats it, so "Congratulations" clears the
   top-right diamond orb + avatar. Desktop untouched. */
article[data-beat="37"] .frame-title{font-size:22px!important}}`,
  'D-unfold-frame-title');
out.unfold = emit('fix4b-agreement-unfold-fixed.html', un);

// ---------- welcome: board-37 title beats the af-deck !important rule ----------
let wel = load('fix4-welcome-staged.html');
wel = rep('welcome', wel,
  '#fpAgreement .ib-title,#fpLegal .ib-title{font-size:22px}',
  `/* FIX4b (2026-11-20, fix-3 eye D) — phone width only, board 37 only:
   the deck/letter title is governed by body.af-deck-on #deckBody
   .ib-title{font-size:25px!important} ((1,2,1)); the first D rule lost.
   This board-37 rule at (1,3,2)!important beats it on deck AND letter
   (both carry body.af-deck-on and #deckBody), so "Congratulations"
   clears the top-right speak-face photo. Desktop untouched. */
body.af-deck-on #deckBody article[data-beat="37"] .ib-title{font-size:22px!important}`,
  'D-welcome-board37');
out.welcome = emit('fix4b-welcome-staged.html', wel);

// walk is unchanged by fix4b — carry it forward byte-identical.
const walk = load('fix4-walk-beginning-fixed.html');
out.walk = emit('fix4b-walk-beginning-fixed.html', walk);
console.log(JSON.stringify(out, null, 1));
