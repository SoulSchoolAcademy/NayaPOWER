// Certificate fixes for the OFFICIAL walkthrough (2026-11-27).
// Surgical edits to identity.html (R5 certificate, sha 57bdd387...):
//  1. NO "Jump back in" — remove the returning button + its intro line.
//  2. NO INSTALL APP button — remove the corner button (the hidden
//     install veil stays in the DOM: its JS touches installX/installGo
//     unguarded, so removing the veil would throw; the veil is only
//     reachable through the removed corner button).
//  3. Raised / elevated name on the certified document.
//  4. Date/time dynamic and CENTRED in Dashboard digit tiles, alive
//     (ticks every second), under the regalia line.
// Node only. Every replacement asserted exactly-once; a miss fails loudly.
import {readFileSync, writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const sha = b => createHash('sha256').update(b).digest('hex');
const LANE = new URL('./', import.meta.url).pathname;
let s = readFileSync(LANE + 'identity.html', 'utf8');
console.log('identity in', s.length, 'B sha256', sha(Buffer.from(s)));
if (sha(Buffer.from(s)) !== '57bdd3873f65104f3ee6f4648cfec4a1a556a78ea8b7fb57153cd49da528af4b') throw new Error('identity base sha mismatch — refusing to edit');
const once = (name, from, to) => {
  const n = s.split(from).length - 1;
  if (n !== 1) throw new Error('PATCH ' + name + ': expected 1 occurrence, found ' + n);
  s = s.replace(from, to);
  console.log('patched', name);
};
// 1. Jump back in — button + its intro line, gone.
once('jump-back-in-gone',
  '        <p class="hub-note">Already have a Smart Name?</p>\n        <button class="enter" type="button" id="returnJump">Jump back in →</button>\n',
  '');
// 2. Install App corner button — gone (veil stays hidden in the DOM, unreachable).
once('install-corner-gone',
  '    <button type="button" class="naya-btn install-corner" id="installCornerBtn">Install App</button>\n',
  '');
// 2b. The veil's own go button (hidden dialog, unreachable without the
// corner button) is relabelled so no "Install App" button text remains.
once('install-go-relabelled',
  '<button type="button" class="naya-btn install-go" id="installGo">Install App</button>',
  '<button type="button" class="naya-btn install-go" id="installGo">Add to Home Screen</button>');
// 3. Raised / elevated name on the certified document.
once('name-raised',
  '      text-shadow: 0 0 38px rgba(160,107,255,0.16), 0 3px 30px rgba(0,0,0,0.55); }',
  '      text-shadow: 0 1px 0 rgba(255,255,255,0.35), 0 0 38px rgba(160,107,255,0.28), 0 6px 30px rgba(0,0,0,0.65), 0 12px 42px rgba(0,0,0,0.45); }');
// 4a. Digit-tile CSS, right after the regalia-dot rule.
once('datetime-tile-css',
  '    .regalia-dot { color: var(--silver); font-weight: 700; }',
  `    .regalia-dot { color: var(--silver); font-weight: 700; }
    /* OFFICIAL WALKTHROUGH 2026-11-27 — date/time, dynamic and CENTRED,
       in Dashboard digit tiles (laws §4: a digit's rim is its digit's
       colour), alive — the clock ticks every second. */
    .cert-datetime { display: flex; align-items: center; justify-content: center;
      flex-wrap: wrap; gap: 4px; margin-top: clamp(8px, 1.4vh, 12px); }
    .cert-datetime[hidden] { display: none; }
    .cert-dt-tile { display: inline-flex; align-items: center; justify-content: center;
      min-width: 26px; height: 34px; padding: 0 4px; border-radius: 8px;
      background: linear-gradient(135deg, #1e1e26 0%, #050607 50%, #1e1e26 100%);
      border: 1.5px solid var(--dtc, #fff);
      box-shadow: 0 4px 10px rgba(0,0,0,0.6), 0 0 10px var(--dtc, rgba(255,255,255,0.25));
      color: #fff; font-family: var(--serif); font-size: 19px; font-weight: 800; line-height: 1; }
    .cert-dt-sep { color: #fff; font-family: var(--serif); font-size: 19px; font-weight: 800; padding: 0 2px; }
    .cert-dt-word { color: #fff; font-family: var(--serif); font-size: 17px; font-weight: 800; letter-spacing: 0.12em; padding: 0 4px; }`);
// 4b. The datetime row itself, centred under the regalia, before ENTER.
once('datetime-row',
  '        </div>\n        <button type="button" class="activate-btn" id="enterBtn" onclick="activateAndRedirect()">',
  '        </div>\n        <div class="cert-datetime" id="certDatetime" hidden aria-label="Date and time"></div>\n        <button type="button" class="activate-btn" id="enterBtn" onclick="activateAndRedirect()">');
// 4c. The painter, before renderCertRegalia.
once('datetime-painter',
  '    function renderCertRegalia(state) {',
  `    /* OFFICIAL WALKTHROUGH 2026-11-27 — the live date/time in digit
       tiles, centred. Digit colours are the laws' digit map (§4):
       0 white, 1 ruby, 2 burnt orange, 3 deep gold, 4 emerald,
       5 deep cyan, 6 indigo, 7 royal purple, 8 deep violet,
       9 deep magenta. Ticks every second, so the document is alive. */
    var DT_COLORS = {'0':'#ffffff','1':'#c62828','2':'#c2410c','3':'#d4a017','4':'#07925f','5':'#0e7490','6':'#3f51b5','7':'#8e24aa','8':'#6d28d9','9':'#a21caf'};
    window.paintCertDatetime = function() {
      var el = document.getElementById('certDatetime');
      if (!el) return;
      var now = new Date();
      var months = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'];
      function pad(n) { return (n < 10 ? '0' : '') + n; }
      function tiles(str) {
        var out = '';
        for (var i = 0; i < str.length; i++) {
          var ch = str.charAt(i);
          if (ch >= '0' && ch <= '9') out += '<span class="cert-dt-tile" style="--dtc:' + DT_COLORS[ch] + '">' + ch + '</span>';
          else out += '<span class="cert-dt-sep">' + ch + '</span>';
        }
        return out;
      }
      el.innerHTML = tiles(pad(now.getDate())) + '<span class="cert-dt-word">' + months[now.getMonth()] + '</span>' + tiles(String(now.getFullYear())) + '<span class="cert-dt-sep">&nbsp;&middot;&nbsp;</span>' + tiles(pad(now.getHours()) + ':' + pad(now.getMinutes()) + ':' + pad(now.getSeconds()));
      el.hidden = false;
      if (!window.__certDtTimer) {
        window.__certDtTimer = setInterval(function(){ try { window.paintCertDatetime(); } catch(e){} }, 1000);
      }
    };
    function renderCertRegalia(state) {`);
// 4d. Paint it whenever the certified document renders (own restore).
once('datetime-on-restore',
  "          if (wrap) wrap.hidden = false;\n        } else {",
  "          if (wrap) wrap.hidden = false;\n          if (window.paintCertDatetime) paintCertDatetime();\n        } else {");
// 4e. Paint it when the claim stamps the certificate.
once('datetime-on-stamp',
  "        if (wrap) wrap.hidden = false;\n        if (certNo == null) {",
  "        if (wrap) wrap.hidden = false;\n        if (window.paintCertDatetime) paintCertDatetime();\n        if (certNo == null) {");
const assert = (name, ok) => { console.log((ok ? 'PASS ' : 'FAIL ') + name); if (!ok) process.exitCode = 1; };
assert('no Jump back in button (id returnJump gone)', !s.includes('id="returnJump"'));
assert('no Jump back in visible text', !s.includes('>Jump back in'));
assert('no Install App corner button (id installCornerBtn gone)', !s.includes('id="installCornerBtn"'));
assert('no visible Install App button text', !s.includes('>Install App</button>'));
assert('digit-tile datetime row present', s.includes('id="certDatetime"') && s.includes('class="cert-datetime"') && s.includes('paintCertDatetime') && s.includes('DT_COLORS'));
assert('digit tiles centred (justify-content:center)', s.includes('.cert-datetime { display: flex; align-items: center; justify-content: center;'));
assert('clock ticks every second', s.includes('setInterval(function(){ try { window.paintCertDatetime(); } catch(e){} }, 1000)'));
assert('name raised (layered text-shadow on certified name)', s.includes('0 12px 42px rgba(0,0,0,0.45)'));
assert('ENTER still hands off to the same-host walk (/?walk=1)', s.includes("var WALKTHROUGH_URL = '/?walk=1'"));
assert('no live-certificate redirect (no nayanet.app/identity)', !s.includes('nayanet.app/identity'));
const out = Buffer.from(s, 'utf8');
writeFileSync(LANE + 'identity.html', out);
writeFileSync(LANE + 'identity-consolidated.html', out);
console.log('identity.html', out.length, 'B sha256', sha(out));
console.log('CERT DONE');
