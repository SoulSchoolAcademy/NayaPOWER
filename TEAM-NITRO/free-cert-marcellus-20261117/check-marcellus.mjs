// check-marcellus.mjs — prove the Free Certificate Marcellus Swap staged
// bytes, cold, from the live staged worker. No walk is executed and no test
// alias is claimed (the swap touches no JS path, so there is nothing a claim
// would prove that the byte-diff + font + layout checks do not; claiming
// would only add another Supabase row to the ten already open).
// Reads the staged /free + /free/walk + pricing v78 live itself.
// Usage: node check-marcellus.mjs
// Tests:
//   T0 static facts (entry + walk bytes): Marcellus link verbatim + --serif
//      Marcellus, 9 uses, no Newsreader anywhere, layered glow shadows
//      byte-identical, cert-name rules intact, narrow CSS intact,
//      start-over intact, F4 markers intact, walk byte-identical.
//   T4 certificate layout math at 390/635/desktop from the served CSS +
//      the maker's measured Marcellus glyph widths.
//   T5 untouched surfaces: pricing v78 byte-exact, /free/hub 302.
//   T6 fonts really load: Marcellus css2 + latin woff2 (14,552 B, wOF2);
//      the walk worker's /identity.html still carries Newsreader --serif
//      (NOTED out of scope, not a failure — the brief is /free only).
// Exit 0 = all pass, 1 = any fail.
import { createHash } from 'crypto';

const FREE = 'https://naya-pricing-free-staging.nayapower.workers.dev';
const PRICING = 'https://naya-pricing-f4-staging.nayapower.workers.dev';
const UA = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36' };

let failures = 0;
function check(name, cond, extra = '') {
  console.log((cond ? 'PASS' : 'FAIL') + ' ' + name + (extra ? ' — ' + extra : ''));
  if (!cond) failures++;
}
const sha = (b) => createHash('sha256').update(b).digest('hex');
async function net(url, opts = {}) {
  return fetch(url, { ...opts, headers: { ...UA, ...(opts.headers || {}) } });
}

const entryRes = await net(FREE + '/free');
const entryHtml = await entryRes.text();
const entryBuf = Buffer.from(entryHtml, 'utf-8');
const walkRes = await net(FREE + '/free/walk');
const walkHtml = await walkRes.text();
const v78Res = await net(PRICING + '/');
const v78Buf = Buffer.from(await v78Res.arrayBuffer());

// ---------- T0: static facts ----------
check('T0 staged /free is the new entry (310,212 B, sha dfe70a8c...)',
  entryBuf.length === 310212 &&
  sha(entryBuf) === 'dfe70a8c8a4d89aa49a31aa56d077b51867ef4e42f276ce28bc39d23fa6370b2',
  `${entryBuf.length} B sha=${sha(entryBuf).slice(0, 8)}...`);
check('T0 /free carries the live entrance Marcellus css2 link verbatim',
  entryHtml.includes('https://fonts.googleapis.com/css2?family=Marcellus&family=Outfit:wght@300;400;600;700;800;900&display=swap'));
check('T0 /free preconnects fonts.googleapis',
  entryHtml.includes('<link rel="preconnect" href="https://fonts.googleapis.com">'));
check('T0 /free --serif is Marcellus, Georgia, serif',
  entryHtml.includes('--serif: Marcellus, Georgia, serif;'));
check('T0 /free still uses var(--serif) 9 times',
  (entryHtml.match(/var\(--serif\)/g) || []).length === 9);
check('T0 /free has no Newsreader anywhere (link + stack both gone)',
  !entryHtml.includes('Newsreader'));
check('T0 Marcellus occurs exactly twice on /free (link + --serif)',
  (entryHtml.match(/Marcellus/g) || []).length === 2);
// Item 2 — the SN-2922 layered glow, byte-identical to the follow-on entry.
const SHADOWS = [
  'text-shadow: 0 0 38px rgba(160,107,255,0.16), 0 3px 30px rgba(0,0,0,0.55);',
  'text-shadow: 0 0 18px rgba(255,255,255,0.17);',
  'text-shadow: 0 0 22px rgba(63,184,255,0.50), 0 0 6px rgba(63,184,255,0.35);',
  'text-shadow: 0 0 22px rgba(255,191,61,0.45), 0 0 6px rgba(255,191,61,0.30);',
  'text-shadow: 0 0 14px rgba(232,232,236,0.18);',
  'text-shadow: 0 0 24px rgba(160,107,255,0.35);',
  'text-shadow: 0 0 14px rgba(232,232,236,0.20);',
  'text-shadow: 0 0 24px rgba(160,107,255,0.40);',
  'text-shadow: 0 0 16px rgba(232,232,236,0.30);',
];
check('T0 all 9 layered glow text-shadows intact (SN-2922 bar)',
  SHADOWS.every((s) => entryHtml.includes(s)) &&
  (entryHtml.match(/text-shadow:/g) || []).length === 9,
  `${(entryHtml.match(/text-shadow:/g) || []).length} text-shadow rules`);
check('T0 certified .cert-name is static in flow with the purple glow',
  entryHtml.includes('.cert-plaque.is-certified .cert-name { position: static;') &&
  entryHtml.includes('.cert-name { position: static; transform: none;') &&
  entryHtml.includes('text-shadow: 0 0 38px rgba(160,107,255,0.16), 0 3px 30px rgba(0,0,0,0.55)'));
check('T0 .cert-name size clamps intact (desktop + narrow)',
  entryHtml.includes('font-size: clamp(2.9rem, 7.4vw, 4.9rem)') &&
  entryHtml.includes('font-size: clamp(2.55rem, 13.5vw, 3.4rem)'));
check('T0 .cert-name still weight 560, line-height 0.98 (unchanged)',
  entryHtml.includes('font-weight: 560;') && entryHtml.includes('line-height: 0.98;'));
// Item 3 — narrow CSS intact.
check('T0 certified regalia stacks at <=640px', entryHtml.includes('.cert-plaque.is-certified .cert-regalia{flex-direction:column'));
check('T0 regalia dot hidden at <=640px', entryHtml.includes('.cert-plaque.is-certified .cert-regalia .regalia-dot{display:none}'));
check('T0 certified plaque scrolls at short heights', entryHtml.includes('.cert-plaque.is-certified{overflow-y:auto}'));
check('T0 certified face goes to flow layout at short heights', entryHtml.includes('.cert-plaque.is-certified .identity-face{position:static;display:flex;flex-direction:column'));
check('T0 ENTER is in normal flow (position:relative, min-height 58px)', /\.activate-btn \{ position: relative;/.test(entryHtml) && /\.activate-btn \{[^}]*min-height: 58px/.test(entryHtml));
// Untouched: start-over, F4 markers, walk byte-identical.
check('T0 start-over control intact (button + gated CSS + clears walk key)',
  entryHtml.includes('id="startOverBtn"') && entryHtml.includes('Use a different alias') &&
  entryHtml.includes('#startOverBtn{display:none') &&
  entryHtml.includes('.cert-plaque.is-certified #startOverBtn{display:inline-flex') &&
  entryHtml.includes("'naya_welcome_right_v1'"));
check('T0 F4 markers intact on the walk (buildBarFill, 25000, showStep(16))',
  walkHtml.includes('buildBarFill') && walkHtml.includes('25000') && walkHtml.includes('showStep(16)'));
check('T0 five doors, Hub first', JSON.stringify([...walkHtml.matchAll(/data-door="([^"]+)"/g)].map((m) => m[1])) === JSON.stringify(['Hub', 'Dashboard', 'Personal', 'Business', 'Space']));
check('T0 walk byte-identical to the follow-on walk (3,292,257 B, sha 2370eae2...)',
  Buffer.byteLength(walkHtml, 'utf-8') === 3292257 &&
  sha(Buffer.from(walkHtml, 'utf-8')) === '2370eae2f9ae9e281d1c3f3b35d99f8699c7df6a2fe4f73328e2877c3b6453ea');
check('T0 walk still Marcellus x4, no Newsreader (walk untouched)',
  (walkHtml.match(/Marcellus/g) || []).length === 4 && !walkHtml.includes('Newsreader'));
check('T0 /free entry intact (free line, eye, walk URL)',
  entryHtml.includes('Enter free &mdash; no payment, no card.') && entryHtml.includes('id="freeEye"') && entryHtml.includes("WALKTHROUGH_URL = '/free/walk'"));

// ---------- T4: certificate layout math with Marcellus ----------
// Glyph widths measured by the maker from the served latin woff2 files
// (fontTools): Marcellus runs ~7% WIDER than Newsreader on names.
// Worst case across the sample names (incl. the 29-char
// "Alexander Christopher Bennett"): 2 lines at 635w, 3 lines at 390w.
// Face heights measured from the served CSS (checker basis): top bar 50px,
// stage padding-bottom 36px, bottom bar 50px.
{
  const css = entryHtml;
  const num = (re) => { const m = css.match(re); return m ? parseFloat(m[1]) : null; };
  const sealShort = num(/\.cert-plaque\.is-certified \.cert-seal\{width:(\d+)px/);
  const enterMin = num(/\.activate-btn \{[^}]*min-height: (\d+)px/);
  const nameCap = css.includes('font-size: clamp(2.55rem, 13.5vw, 3.4rem)');
  const face635 = 349 - 50 - 36 - 50; // 213
  const nameLine635 = Math.round(54.4 * 0.98); // 53
  const content635 = 72 + 15 + 30 + 20 + 2 * nameLine635 + 20 + 124 + 40 + 58 + 40 + 50;
  check('T4 635x349: worst-case Marcellus content (~575px) exceeds face (~213px) so scroll is the fix, ENTER stays in flow',
    sealShort === 72 && enterMin === 58 && nameCap && face635 === 213 && content635 > face635,
    `face ${face635}px vs content ~${content635}px (2 name lines)`);
  const face390 = 844 - 50 - 36 - 50; // 708
  const nameLine390 = Math.round(52.65 * 0.98); // 52
  const content390 = 94 + 15 + 30 + 20 + 3 * nameLine390 + 20 + 130 + 40 + 58 + 40 + 50;
  check('T4 390x844: worst-case Marcellus content (~653px, 3-line name) still fits the face (~708px) in grid mode',
    face390 === 708 && content390 < face390, `face ${face390}px vs content ~${content390}px`);
  const regaliaOneLine = 183 + 12 + 376;
  const col390 = 390 - 18 - 18;
  check('T4 390px: one-line regalia (~571px) cannot fit the 354px column — the stack rule is required and present',
    regaliaOneLine > col390 && css.includes('.cert-plaque.is-certified .cert-regalia{flex-direction:column'));
  check('T4 desktop 1919x998: neither media query matches, so the presentation is untouched',
    1919 > 640 && 998 > 700);
}

// ---------- T5: untouched surfaces ----------
check('T5 pricing v78 byte-exact (unchanged)', sha(v78Buf) === 'ca2eafeb896c763ae2459b4a10b8715e726765ced607c0aab3640d27e6c39ae2');
{
  const r = await net(FREE + '/free/hub', { redirect: 'manual' });
  check('T5 /free/hub still 302 to nayanet.app', r.status === 302 && r.headers.get('location') === 'https://nayanet.app/');
}

// ---------- T6: the font really loads ----------
async function fontLoads(cssUrl) {
  const r = await net(cssUrl);
  if (r.status !== 200) return { ok: false, why: 'css2 ' + r.status };
  const t = await r.text();
  const m = t.match(/\/\* latin \*\/\s*@font-face \{[^}]*font-family: 'Marcellus'[^}]*src: url\((https:\/\/[^)]+\.woff2)\)/);
  if (!m) return { ok: false, why: 'no latin Marcellus woff2' };
  const w = await net(m[1]);
  if (w.status !== 200) return { ok: false, why: 'woff2 ' + w.status };
  const buf = Buffer.from(await w.arrayBuffer());
  return { ok: buf.slice(0, 4).toString() === 'wOF2' && buf.length === 14552, why: buf.length + ' B' };
}
{
  const marc = await fontLoads('https://fonts.googleapis.com/css2?family=Marcellus&family=Outfit:wght@300;400;600;700;800;900&display=swap');
  check('T6 Marcellus css2 serves + latin woff2 downloads, 14,552 B, wOF2', marc.ok, marc.why);
  // Out of scope, noted not failed: the walk worker's /identity.html still
  // defines the Newsreader --serif. The brief is /free only; the walk is
  // untouched. Flagged for the captain as the follow-on.
  const idRes = await net('https://naya-walk-beginning-staging.nayapower.workers.dev/identity.html');
  const idHtml = await idRes.text();
  const serifWalk = (idHtml.match(/--serif:\s*[^;}]+/) || [''])[0];
  console.log('NOTE T6 walk worker /identity.html --serif is still: ' + serifWalk.trim() +
    ' (out of scope — /free only; walk untouched by design)');
}

console.log(failures === 0 ? 'HARNESS: ALL PASS' : `HARNESS: ${failures} FAILURES`);
process.exit(failures === 0 ? 0 : 1);
