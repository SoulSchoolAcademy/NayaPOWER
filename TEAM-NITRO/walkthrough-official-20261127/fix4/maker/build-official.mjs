// Build the OFFICIAL walkthrough portal (2026-11-27) from the v1 built portal.
// Base: portal-v1.html (v1 build, 13,901,029 B, sha 88346f9d...),
// itself built on the R5 base (13,883,771 B, sha d4bb2102...).
// FIX2: portal-v1 carries the remove-account modal conversion (item 3) —
// full-screen in-frame view on the #fpStory pattern; the pinned sha
// below is the FIX2 v1, not the fix1 v1 (b7ee02d6...).
// FIX3 (2026-11-27 ~21:11 MST): NO portal-v1 change — all FIX3 work is in
// the four build inputs (phone-style3 / phone-section3 / phone-script3 /
// steps.js / engine.js), so the v1 pin below is unchanged (88346f9d...).
// FIX3 asserts at the end of the list prove the overhaul in the build.
// FIX4 (2026-11-27 ~21:18 MST, Shawn's consolidated "do it now" order):
// ONE PHONE PER SCREEN — the trio is gone, superseded. Same v1 pin (no
// portal-v1 change); all FIX4 work is in the same four build inputs +
// engine.js + the harvested ball webp (media/ball-n.webp). FIX4 asserts
// replace the trio asserts at the end of the list.
// The official flow: portal -> certificate -> 23 phone frames, ONE PER
// SCREEN (put in, tap the ball, next): live, age+language,
// gender+faith+ethnicity, favorites, industry+skills+connect+categories,
// video, motto, vision, goal, mission, love, don't love, thing, promise,
// gift, benefit, unique, connect, work, education, experience,
// achievements, values+stand for. The picture is a full-bleed 9:16 layer
// BEHIND the input (separation law); the ball IS Enter — tap 1 flashes the
// picture where the step has one, tap 2 moves to the next input. No Skip
// anywhere, no name screen, gender no default. Node only.
// Every replacement asserted exactly-once; a miss fails loudly, no write.
import {readFileSync, writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const sha = b => createHash('sha256').update(b).digest('hex');
const LANE = new URL('./', import.meta.url).pathname;
const IMG = '/home/hatch/workspace/user/media_library/image/';
const v1 = readFileSync(LANE + 'portal-v1.html');
console.log('v1 base', v1.length, 'B sha256', sha(v1));
if (sha(v1) !== '88346f9d25906f0c70419057458e9a2f1890d52e736be9585dc0ec4c6158b863') throw new Error('v1 base sha mismatch — refusing to build');
let s = v1.toString('utf8');
const once = (name, from, to) => {
  const n = s.split(from).length - 1;
  if (n !== 1) throw new Error('PATCH ' + name + ': expected 1 occurrence, found ' + n);
  s = s.replace(from, to);
  console.log('patched', name);
};
// 1. Walk section -> v4 single-phone markup (whole section).
{
  const secStart = '<section id="fpWalk" hidden>';
  const a = s.indexOf(secStart);
  const b = s.indexOf('</section>', a);
  if (a < 0 || b < 0) throw new Error('walk section not found');
  s = s.slice(0, a) + readFileSync(LANE + 'phone-section3.html', 'utf8') + s.slice(b + '</section>'.length);
  console.log('patched section: walk -> ONE phone per screen (official v4)');
}
// 2. Phone style -> v3 style (whole old phone <style> block).
{
  const start = '<style>\n/* BLACK DIAMOND PHONE 2026-11-27';
  const a = s.indexOf(start);
  const b = s.indexOf('</style>', a);
  if (a < 0 || b < 0) throw new Error('phone style block not found');
  s = s.slice(0, a) + readFileSync(LANE + 'phone-style3.html', 'utf8') + s.slice(b + '</style>'.length);
  console.log('patched style: phone v1 -> official');
}
// 3. Phone script -> v3 script, with the harvested pictures embedded.
{
  const start = '<script>\n/* BLACK DIAMOND PHONE 2026-11-27 — phone chrome logic';
  const a = s.indexOf(start);
  const b = s.indexOf('</script>', a);
  if (a < 0 || b < 0) throw new Error('phone script block not found');
  let script = readFileSync(LANE + 'phone-script3.html', 'utf8');
  // v2's 8, byte-verified by checker2 (sizes must match the verdict table):
  const pics = {
    vault: ['1_THE_VAULT.jpg', 'image/jpeg', 326889],
    current: ['2_HOW_WE_SNYC.jpg', 'image/jpeg', 576540],
    nano: ['3_NANOVERSE.jpg', 'image/jpeg', 365937],
    works: ['4_HOW_IT_WORKS.jpg', 'image/jpeg', 442529],
    smartvault: ['5_SMART_VAULT.jpg', 'image/jpeg', 521616],
    match: ['6_AUTO_MATCH.jpg', 'image/jpeg', 415870],
    org: ['7_AUTO_ORGINIZED.jpg', 'image/jpeg', 566171],
    pillars: ['a3/a3903dafe3e9ee81ac66c6bb14104fdffcd7483550bd521a141f1c1ea6e538c4.png', 'image/png', 2924933],
    // v3's 6, from the PICTURE MAP in MEMORY.md (his uploads):
    motto: ['c0/c017eea7acbc2527b07efa2e61e9233bd0fb61f793b45882c7a867c562a0a8b7.png', 'image/png', 0],
    love: ['77/7702f98780b5dec46e146997451f61a4172de44cd93dee9fe6ccf1da37a882da.png', 'image/png', 0],
    dontlove: ['f0/f0e21717d412807e5ad25bc58ded1b38be42a1b5f872ae27688c5c7daf1dfcef.png', 'image/png', 0],
    unique: ['b6/b6cfaacab406f5213c1893c6f305b1f910dc1428a78dcb413004e335b7db4bb2.png', 'image/png', 0],
    gift: ['42/4248188b4ea181ac848b727c30c7671c5243006cda8f62935241fcf2c2a5dae7.png', 'image/png', 0],
    work: ['fa/fa45cb8958e4aa3832c2622936988e8955e620a4c40264a0cd5fc5d940f86cfb.png', 'image/png', 0],
  };
  const map = {};
  for (const [k, [f, ct, expect]] of Object.entries(pics)) {
    const buf = readFileSync(IMG + f);
    console.log('pic', k, f, buf.length, 'B sha256', sha(buf).slice(0, 12));
    if (expect && buf.length !== expect) throw new Error('pic size mismatch ' + k + ': got ' + buf.length + ', checker2 verdict says ' + expect);
    map[k] = 'data:' + ct + ';base64,' + buf.toString('base64');
  }
  script = script.replace('/*__BD_PICS__*/', JSON.stringify(map));
  if (!script.includes('data:image/jpeg;base64,')) throw new Error('picture embed failed');
  // The welcome video, direct file (ffprobe: 576x1024 9:16, h264, 30fps, 204.3s).
  // VERIFIED here, NOT embedded: embedding its base64 tipped the worker
  // over the edge (503 error 1102 on / at 57 MB). It is served by the
  // staging worker at /naya-video.mp4 from WELCOME_ASSETS KV instead
  // (see kv-put-video.py); the page references that route.
  const vidBuf = readFileSync('/home/hatch/workspace/user/media_library/video/c8/c86da39ed1360b79f5109f2c0706f8345059259b2574753b39cdf89af95d037c.mp4');
  console.log('video', 'c86da39e….mp4', vidBuf.length, 'B sha256', sha(vidBuf).slice(0, 12), '(served from KV, not embedded)');
  if (vidBuf.length !== 7368202) throw new Error('video size mismatch: got ' + vidBuf.length);
  if (sha(vidBuf) !== 'c86da39ed1360b79f5109f2c0706f8345059259b2574753b39cdf89af95d037c') throw new Error('video sha mismatch — refusing to build');
  // FIX4 — the REAL N: the marble-sphere image harvested verbatim from
  // Settings fix13 (--ball webp, 512x512). Embedded as a data URI (39 KB)
  // and set as the --ball CSS var by the phone script; both the step ball
  // and the end ball read it. Verified by sha, never re-rendered.
  const ballBuf = readFileSync(LANE + 'media/ball-n.webp');
  console.log('ball', 'ball-n.webp', ballBuf.length, 'B sha256', sha(ballBuf).slice(0, 12), '(Settings fix13 --ball, harvested verbatim)');
  if (ballBuf.length !== 39360) throw new Error('ball size mismatch: got ' + ballBuf.length);
  if (sha(ballBuf) !== 'd5890238d4093db9a0455c92b328c7d3cd79c03c7084841adb8f3b6ee3e6b477') throw new Error('ball sha mismatch — refusing to build');
  script = script.replace('/*__BD_BALL__*/', JSON.stringify('data:image/webp;base64,' + ballBuf.toString('base64')));
  if (!script.includes('data:image/webp;base64,')) throw new Error('ball embed failed');
  s = s.slice(0, a) + script + s.slice(b + '</script>'.length);
  console.log('patched script: phone official + 14 harvested pictures + real ball (video served from KV)');
}
// 4. QUESTIONS -> the 23-step single-phone flow.
{
  const start = 'var QUESTIONS = [';
  const a = s.indexOf(start);
  const b = s.indexOf('];', a);
  if (a < 0 || b < 0) throw new Error('QUESTIONS not found');
  s = s.slice(0, a) + readFileSync(LANE + 'steps.js', 'utf8').replace(/\n$/, '') + s.slice(b + 2);
  console.log('patched QUESTIONS: 18 v1 screens -> 23 official steps');
}
// 5. Walk engine -> v4 single-phone engine (from `var idx = 0;` + fit() to `function complete(){`).
{
  const start = '  var idx = 0;\n  function fit(){';
  const end = '  function complete(){';
  const a = s.indexOf(start);
  const b = s.indexOf(end, a);
  if (a < 0 || b < 0) throw new Error('walk engine block not found');
  s = s.slice(0, a) + readFileSync(LANE + 'engine.js', 'utf8') + '\n' + s.slice(b);
  console.log('patched engine: trio group engine -> single-phone engine (official v4)');
}
// 6. D1 (carried): finish() must NOT hide the ball (enterBtn IS the jewel).
once('finish-keeps-ball', '      enterBtn.hidden = true;\n', '      /* D1 v2/v3: the ball stays — enterBtn is the jewel, never hidden. */\n');
// ---- assertions on the built file (v4 + R5 keepers) ----
const assert = (name, ok) => { console.log((ok ? 'PASS ' : 'FAIL ') + name); if (!ok) process.exitCode = 1; };
assert('FIX4 phone present, ONE per screen (bdSingle, bd-phone, bd-inner, bd-ball, bd-foot, fpWalkNext, bdEndPhone)', s.includes('id="bdSingle"') && s.includes('class="bd-phone"') && s.includes('class="bd-inner"') && s.includes('bd-ball') && s.includes('class="bd-foot"') && s.includes('id="fpWalkNext"') && s.includes('id="bdEndPhone"'));
assert('FIX4 NO trio, NO grouping header (no bdTrio, no bdGroupProg, no Group-of-8 text)', !s.includes('id="bdTrio"') && !s.includes('id="bdGroupProg"') && !s.includes('bdGroupProg') && !s.includes('of 8 — Steps'));
assert('FIX4 Settings frame verbatim (stage 393/852 + island + home bar + inner chrome + side buttons)', s.includes('aspect-ratio:393/852') && s.includes('width:104px;height:22px') && s.includes('radial-gradient(circle at 86% 50%,#16263f 0 4px,#050607 5px)') && s.includes('width:120px;height:5px') && s.includes('linear-gradient(#050607,#050607) padding-box,linear-gradient(135deg,#f4f6f9 0%,#c7ccd6 16%,#787d88 34%,#eef1f5 52%,#969ca7 70%,#dfe3ea 86%,#6d727c 100%) border-box') && s.includes('.bd-inner::before') && s.includes('.bd-inner::after') && s.includes('border-top-width:28px;border-bottom-width:20px'));
assert('picture is a background layer (bd-bgpic absolute, never layout space)', s.includes('class="bd-bgpic"') && s.includes('.bd-bgpic{position:absolute;inset:0;'));
assert('no separate Enter button (ball is the only Enter)', !s.includes('>Enter</button>') && s.includes('id="fpWalkEnter"'));
assert('NO Skip pill (hidden element, display:none, no handler)', s.includes('id="fpWalkSkip" type="button" hidden') && s.includes('#fpWalkSkip.fp-walk-skip{display:none!important}') && !s.includes('skipBtn.addEventListener'));
assert('finish() never hides the ball', !s.includes('enterBtn.hidden'));
assert('23 official steps in order (live..values_stand)', ['"key":"live"','"key":"age_lang"','"key":"gender"','"key":"favorites"','"key":"industry_all"','"key":"video"','"key":"motto"','"key":"vision"','"key":"goal"','"key":"mission"','"key":"love"','"key":"dontlove"','"key":"thing"','"key":"promise"','"key":"gift"','"key":"benefit"','"key":"unique"','"key":"connect"','"key":"work"','"key":"education"','"key":"experience"','"key":"achievements"','"key":"values_stand"'].every(k => s.includes(k)) && (s.match(/"key":"/g) || []).length === 23);
assert('no v3 leftovers (model, age_gender, resume, achievements_values, standalone categories)', !s.includes('"key":"model"') && !s.includes('"key":"age_gender"') && !s.includes('"key":"resume"') && !s.includes('"key":"achievements_values"') && !s.includes('"key":"categories"'));
assert('values sits ONCE (values_stand only, no standalone values step)', s.includes('"key":"values_stand"') && !s.includes('"key":"values"'));
assert('age and gender are TWO phones (age_lang + gender), gender no default', s.includes('"key":"age_lang"') && s.includes('"key":"gender"') && s.includes('[["","Choose…"],["male","Male"]'));
assert('industry_all is ONE frame: industry + skills + connect + categories', s.includes('"key":"industry_all"') && s.includes('"id":"industry"') && s.includes('"id":"skills"') && s.includes('"id":"cats"'));
assert('no name screen, no community/church question, no Spotify', !s.includes('"key":"name"') && !s.includes('"key":"church"') && !s.toLowerCase().includes('church?') && !s.toLowerCase().includes('spotify'));
// FIX3 note on the line above: the old check used a bare 'church' substring,
// which the cascade city name "Christchurch" (Canterbury, NZ) now trips.
// The check still proves the intent — no church QUESTION (no key, no
// "church?" question text) and no Spotify anywhere — while allowing the
// real city name through.
assert('no name/alias step (no country/province/city screens, no name key)', !s.includes('"key":"country"') && !s.includes('"key":"name"') && !s.includes('"key":"alias"'));
assert('gender dropdown has NO default (empty first option)', s.includes('"id":"gender"') && s.includes('[["","Choose…"],["male","Male"]'));
assert('video iPhone plays the DIRECT 9:16 file via /naya-video.mp4 (ONE spot, mid-flow)', s.includes('"video":true') && s.includes('src="/naya-video.mp4"') && s.includes('bd-bgvid') && s.includes('bd-has-video') && !s.includes('data:video/mp4;base64,'));
assert('YouTube is a fallback link only', s.includes('youtube.com/watch?v=XqZe1zdF1Tc') && !s.includes('youtube-nocookie') && !s.includes('youtube.com/embed'));
assert('video pillars are the video\'s OWN four', s.includes('Smart Vault &middot; Auto Organizer &middot; Smart Match &middot; Collective Intelligence'));
assert('NO video at the end (end phone carries no video)', !s.split('id="bdEndPhone"')[1].split('id="fpWalkSkip"')[0].includes('<video'));
assert('picture map (vision=nano, goal=vault, mission=works, thing=org, promise=smartvault, connect=match, benefit=current, motto, love, dontlove, unique, gift, work, pillars)', ['"pic":"nano"','"pic":"vault"','"pic":"works"','"pic":"org"','"pic":"smartvault"','"pic":"match"','"pic":"current"','"pic":"motto"','"pic":"love"','"pic":"dontlove"','"pic":"unique"','"pic":"gift"','"pic":"work"','"pic":"pillars"'].every(x => s.includes(x)));
assert('14 pictures embedded as data URIs', (s.match(/data:image\/(jpeg|png);base64,/g) || []).length >= 14);
assert('end screen: 2-column end grid (World spans both), end title, chin label nowrap', s.includes('.fp-walk-endgrid{display:grid;grid-template-columns:1fr 1fr;') && s.includes('fp-walk-endgrid-wide') && s.includes('See my world') && s.includes('Welcome home.') && s.includes('.bd-chin-label{font-size:17px;font-weight:800;letter-spacing:.18em;white-space:nowrap;'));
assert('live clock + battery present', s.includes('class="bd-clock"') && s.includes('bd-batt-fill'));
assert('copy-out on review screen', s.includes('id="fpWalkCopyAll"'));
assert('8 style elements (7 R5 + 1 phone)', (s.match(/<style>/g) || []).length === 8);
assert('10 script elements (9 R5 + 1 phone)', (s.match(/<script/g) || []).length === 10);
assert('R5: hover-only menu intact', s.includes('.eco-item .eco-tip{') && !s.includes('eco-label'));
assert('R5: ring intact (nayaSpectrum 78s)', s.includes('animation:nayaSpectrum 78s linear infinite'));
assert('R5: story intact, 27 slides', s.includes('id="fpStory"') && s.includes('FP_SLIDES'));
assert('R5: nine eco-item destinations intact', (s.match(/class="eco-item"/g) || []).length === 9);
assert('R5: walk gating intact (?walk=1)', s.includes("params.get('walk') !== '1'"));
assert('R5: complete() verify-before-declare intact', s.includes('api/welcome/complete') && s.includes('api/welcome/me'));
assert('R5: certificate link intact', s.includes('identity.html'));
assert('walk=1 scroll-into-view intact', s.includes('walk.scrollIntoView'));
assert('walk engine is v4 (single phone, ball flashes then advances, no skip handler)', s.includes('NO SKIP') && s.includes('function advance()') && s.includes('function goBack()') && s.includes('bdSingle') && s.includes('Tap 1: flash the related image') && !s.includes('GROUPS[gidx]') && !s.includes('function collectGroup()'));
assert('FIX4 inputs: obsidian black with depth, edge light-up on select, white card survives only as the reveal card', s.includes('.bd-card{flex:1;min-height:0;overflow-y:auto;display:flex;flex-direction:column;background:linear-gradient(135deg,#0d0d13,#050607 55%)') && s.includes('background:#050607;color:#fff;border:1.5px solid rgba(255,255,255,.35)') && s.includes('bdEdgeGlow') && (s.match(/background:linear-gradient\(135deg,#ffffff,#f6f4f9\)/g) || []).length === 1);
assert('FIX4 diamond: real faceted mini-diamond jewels (orbit + end), no flat glyph in the walk regions', s.includes('5,3 12,3 12,9 3,9') && s.includes('fp-walk-endjewel') && (s.match(/&#9670;/g) || []).length === 347);
// FIX4 note on the count above: occurrence count (grep -c counts lines).
// Fix3 portal carried 347; fix4 carries the same 347 — the walk regions
// (section + phone style + phone script + questions) carry 0 flat glyphs;
// the 347 are the untouched R5 base's deal/stage chrome, out of scope.
// The ball's own centre is the real marble image now (see next assert),
// which supersedes fix3's SVG facets: the faceted diamond survives as
// the orbit jewel + the end jewel divider, both real SVG diamonds.
assert('FIX4 ends: raised spectrum buttons, energy pulse, Hub before pricing', s.includes('bdEndPulse') && s.includes('#fpWalkHub{--ec:#07925f') && s.includes('#fpWalkPricing{--ec:#0f52ba') && s.includes('fp-walk-endjewel') && s.indexOf('id="fpWalkHub"') < s.indexOf('id="fpWalkPricing"'));
assert('FIX4 cascade: country->province->city, hidden until chosen, chosen lifts purple', s.includes('cascadeFrom') && s.includes('cascadeMap') && s.includes('bd-cascade-hidden') && s.includes('bd-chosen') && s.includes('"id":"province","t":"select"') && s.includes('"id":"city","t":"select"') && s.includes('wireCascade'));
assert('FIX4 cascade fix: unchosen select saves empty (no placeholder text), parent/own listeners on separate flags', s.includes("if (!selC.value) return '';") && s.includes("if (!el.value) return '';") && s.includes('_bdParentWired') && s.includes('_bdOwnWired') && s.includes("if (saved === 'Choose…') saved = '';"));
assert('FIX4 ball: Settings ring + marble centre + real N image, slow flow, purple arc', s.includes('conic-gradient(from 210deg,#fdfdfd,#9a9a9a,#e8e8e8,#5a5a5a,#d5d5d5,#8a8a8a,#fdfdfd)') && s.includes('background-image:var(--ball)') && s.includes('data:image/webp;base64,UklGRriZAABXRUJQVlA4IKyZAABwCQKdASoAAgACPj0ci0QiIaET+l1QIAPEtLd3Q3pf8CvAP0A') && s.includes('bdGemSpin 24s') && s.includes('bdOrbit 180s') && s.includes('bdOrbit2 240s') && s.includes('radial-gradient(circle at 32% 26%,#55555f 0%,#232329 30%,#0b0b11 58%,#050607 100%)'));
assert('FIX4 alive on touch: phone lifts + presses, card lifts + presses, arrows press', s.includes('.bd-phone:hover{transform:translateY(-4px)') && s.includes('.bd-phone:active{transform:scale(.985)}') && s.includes('.bd-card:hover{transform:translateY(-2px)') && s.includes('.bd-arrow:active{transform:scale(.97)}'));
const out = Buffer.from(s, 'utf8');
writeFileSync(LANE + 'portal.html', out);
console.log('portal.html', out.length, 'B sha256', sha(out), '(v1 +', out.length - v1.length, 'B)');
console.log('BUILD DONE');
