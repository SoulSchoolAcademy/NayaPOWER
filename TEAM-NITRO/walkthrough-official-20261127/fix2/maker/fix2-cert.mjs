// FIX2 certificate edits (F1 + veil REMOVAL) — applied to BOTH identity files.
// Node only. Every replacement asserted exactly-once; a miss fails loudly.
// F1: .cert-benefit paragraph under ENTER gets the D4 margin treatment
//     (24px clear each side) — the D3 tiles pushed it down into the
//     bottom corner crests at 390 in the already-claimed state ("Yo" eaten).
// ITEM 2: the install veil is REMOVED, not guarded (no-pop-ups law,
//     Shawn 2026-11-27 ~20:15 MST): veil element + all show-code +
//     veil CSS deleted from the shipped bytes. No replacement prompt.
//     Only the service-worker registration survives (it is not install UI);
//     the manifest link stays (browser-native affordance, not our veil).
// NOTE: no removed identifier (installVeil/openModal/veil.hidden etc.)
// appears anywhere in this script's replacements — not even in comments —
// so a grep for the removed names over the patched file returns zero.
import {readFileSync, writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const sha = b => createHash('sha256').update(b).digest('hex');
const BASE_SHA = '86536d53a28367e542f0b225857066391ce535f5e13b17a5a81129fe637b17ae';
const REMOVED_TOKENS = ['installVeil', 'openModal', 'closeModal', 'installGo', 'installX', 'installLater', 'installManual', 'installLogo', 'installCornerBtn', 'deferredPrompt', 'veil.hidden', 'beforeinstallprompt', 'install-card', 'install-veil', 'install-x', 'install-go', 'install-manual', 'install-later', 'install-corner', 'install-title', 'install-sub', 'install-logo', 'im-row', 'im-steps', 'im-title', 'im-jewel', 'im-foot', 'im-alt', 'im-you', 'nayanet_install_dismissed', 'nayanet_install_done', 'nayanet.install.shows', 'nayanet.installed'];

for (const F of ['./identity-consolidated.html', './identity.html']) {
  let s = readFileSync(F, 'utf8');
  console.log('---', F, 'base', s.length, 'B sha', sha(Buffer.from(s)));
  if (sha(Buffer.from(s)) !== BASE_SHA) throw new Error(F + ': base sha mismatch — refusing to edit');
  const once = (name, from, to) => {
    const n = s.split(from).length - 1;
    if (n !== 1) throw new Error('PATCH ' + name + ': expected 1, found ' + n);
    s = s.replace(from, to);
    console.log('patched', name);
  };
  const sliceOut = (name, startAnchor, endAnchor, mustContain, replacement) => {
    const a = s.indexOf(startAnchor);
    if (a < 0) throw new Error('PATCH ' + name + ': start anchor not found');
    let b = s.indexOf(endAnchor, a + startAnchor.length);
    if (b < 0) throw new Error('PATCH ' + name + ': end anchor not found');
    b += endAnchor.length;
    const cut = s.slice(a, b);
    for (const m of mustContain) if (!cut.includes(m)) throw new Error('PATCH ' + name + ': cut is missing ' + m);
    s = s.slice(0, a) + replacement + s.slice(b);
    console.log('patched', name, '(cut', cut.length, 'B)');
  };

  // ---- F1: benefit paragraph clear of the corner crests. ----
  once('F1-benefit-margins',
`.cert-plaque.is-certified .cert-benefit { display: none; }`,
`.cert-plaque.is-certified .cert-benefit { display: none; }
    /* FIX2 F1 — the benefit paragraph under ENTER ran into the bottom
       corner crests at 390 in the already-claimed state ("Yo" eaten):
       the D3 tiles pushed ENTER + paragraph down ~90px, and the D4
       margin fix covered #hubNote only. Same treatment here: 24px
       clear on both sides, every width. */
    .cert-benefit { margin-left: 24px; margin-right: 24px; }`);

  // ---- ITEM 2: veil CSS block, whole. ----
  sliceOut('veil-css',
    '    /* ---------- Install App — corner button + popup, same quiet register ---------- */',
    '    .install-later:hover { color: var(--ink); }',
    ['.install-veil {', '.install-card {', '.install-x {'],
    '    /* FIX2 — the install prompt is REMOVED, not guarded (no-pop-ups\n       law): no veil element, no opener, no install prompt of any form\n       ships on this page. Its CSS is deleted with it. */');

  // ---- ITEM 2: corner-button + card strays. ----
  once('veil-css-corner-margin', '    .install-corner { margin-left: 16px; }\n', '');
  once('veil-css-corner-phone', '      .install-corner { padding: 8px 13px; min-height: 38px; font-size: 0.64rem; letter-spacing: 0.12em; margin-left: 8px; }\n', '');
  once('veil-css-card-phone', '      .install-card { padding: 32px 22px 26px; }\n', '');
  once('veil-css-reduced-motion',
    '.naya-btn, .activate-btn, .install-x, .im-row, .brand-mark, .alias-field-wrapper',
    '.naya-btn, .activate-btn, .brand-mark, .alias-field-wrapper');
  once('veil-css-reduced-motion-hover',
    '.naya-btn:hover, .activate-btn:hover, .im-row:hover, .brand-logo-group:hover .brand-mark',
    '.naya-btn:hover, .activate-btn:hover, .brand-logo-group:hover .brand-mark');
  once('veil-css-corner-hide', '      #installCornerBtn { display: none; }\n', '');
  // The v2.11 comment still describes the veil as the install route — update it.
  once('veil-comment-v211',
`       the bar's other content (his word: unprofessional, sitting
       on the top icons). The install invitation still arrives as
       the quiet veil — at most 3 lifetime auto-shows, never after
       install or dismiss. The desktop bar keeps the pill: the
       grandfathered chrome, clear of every crest at full width.`,
`       the bar's other content (his word: unprofessional, sitting
       on the top icons). FIX2 (no-pop-ups law): the install prompt
       is REMOVED entirely — no veil, no corner button, no invite
       of any form ships on this page.`);

  // ---- ITEM 2: veil HTML element, whole. ----
  sliceOut('veil-html',
    '    <!-- Install App popup — the crystal N becomes the home-screen icon;',
    '\n  </div>\n',
    ['id="installVeil"', 'id="installLater"', 'id="installGo"'],
    '  <!-- FIX2 — the install veil element is REMOVED (no-pop-ups law):\n       no overlay element ships on this page. -->\n');

  // ---- ITEM 2: the whole install script block (opener + prompt + timers). ----
  // Slice from the block comment through its closing })(); — the block is
  // (comment)(function(){...})(); and nothing else lives between.
  {
    const startAnchor = '    /* ---------- PWA install — corner button + popup. ----------';
    const a = s.indexOf(startAnchor);
    if (a < 0) throw new Error('PATCH veil-js: start anchor not found');
    const endAnchor = '\n    })();';
    let b = s.indexOf(endAnchor, a + startAnchor.length);
    if (b < 0) throw new Error('PATCH veil-js: end anchor not found');
    b += endAnchor.length;
    const cut = s.slice(a, b);
    for (const m of ['installVeil', 'openModal', 'beforeinstallprompt', 'serviceWorker', '(function () {']) {
      if (!cut.includes(m)) throw new Error('PATCH veil-js: cut is missing ' + m);
    }
    if (cut.includes('activateAndRedirect') || cut.includes('returnJump')) throw new Error('PATCH veil-js: cut overran into other code');
    s = s.slice(0, a) + `    /* FIX2 — the install prompt is REMOVED, not guarded (no-pop-ups
       law, Shawn 2026-11-27 ~20:15 MST): no veil element, no opener, no
       install prompt of any form ships on this page. Only the service
       worker registration below survives — it is not install UI. */
    if ('serviceWorker' in navigator && /^https?:$/.test(window.location.protocol)) {
      navigator.serviceWorker.register('sw.js').catch(function () {});
    }` + s.slice(b);
    console.log('patched veil-js (cut', cut.length, 'B)');
  }

  // ---- Guards: no removed token may survive anywhere in the file. ----
  for (const t of REMOVED_TOKENS) {
    if (s.includes(t)) throw new Error('GUARD: removed token still present: ' + t);
  }
  // ---- Syntax: every inline <script> block must still parse. ----
  const parts = s.split('<script>');
  for (let i = 1; i < parts.length; i++) {
    const code = parts[i].split('</script>')[0];
    try { new Function(code); } catch (e) { throw new Error('SYNTAX in script block ' + i + ': ' + e.message); }
  }
  writeFileSync(F, s, 'utf8');
  console.log('wrote', F, s.length, 'B sha', sha(Buffer.from(s)));
}
console.log('FIX2 CERT DONE');
