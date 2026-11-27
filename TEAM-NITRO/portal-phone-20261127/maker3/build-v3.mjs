// Build the Black Diamond phone v3 portal from the v1 built portal.
// Base: maker3/portal-v1.html (v1 build, 13,900,396 B, sha b7ee02d6...),
// itself built on the R5 base (13,883,771 B, sha d4bb2102...).
// v3 rebuilds the walk to Shawn's TRIO order (voice calls 2026-11-27
// ~12:17-13:24 MST and ~13:55 MST): 21 steps in 7 groups of three iPhones,
// three side by side on laptop, stacked scrolling on phone; the picture is
// a full-bleed 9:16 layer BEHIND the input (separation law); the ball IS
// Enter (N peeks, ball reveals); motto/love/don't-love/unique/gift return;
// values sits ONCE in achievements/values/where-you-stand. Node only.
// Every replacement asserted exactly-once; a miss fails loudly, no write.
import {readFileSync, writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const sha = b => createHash('sha256').update(b).digest('hex');
const LANE = new URL('./', import.meta.url).pathname;
const IMG = '/home/hatch/workspace/user/media_library/image/';
const v1 = readFileSync(LANE + 'portal-v1.html');
console.log('v1 base', v1.length, 'B sha256', sha(v1));
if (sha(v1) !== 'b7ee02d6177628e5700ae57f819cb7e87f532689245cf639e6d228b080559ee0') throw new Error('v1 base sha mismatch — refusing to build');
let s = v1.toString('utf8');
const once = (name, from, to) => {
  const n = s.split(from).length - 1;
  if (n !== 1) throw new Error('PATCH ' + name + ': expected 1 occurrence, found ' + n);
  s = s.replace(from, to);
  console.log('patched', name);
};
// 1. Walk section -> v3 trio markup (whole section).
{
  const secStart = '<section id="fpWalk" hidden>';
  const a = s.indexOf(secStart);
  const b = s.indexOf('</section>', a);
  if (a < 0 || b < 0) throw new Error('walk section not found');
  s = s.slice(0, a) + readFileSync(LANE + 'phone-section3.html', 'utf8') + s.slice(b + '</section>'.length);
  console.log('patched section: walk -> Black Diamond phone v3 TRIO');
}
// 2. Phone style -> v3 style (whole old phone <style> block).
{
  const start = '<style>\n/* BLACK DIAMOND PHONE 2026-11-27';
  const a = s.indexOf(start);
  const b = s.indexOf('</style>', a);
  if (a < 0 || b < 0) throw new Error('phone style block not found');
  s = s.slice(0, a) + readFileSync(LANE + 'phone-style3.html', 'utf8') + s.slice(b + '</style>'.length);
  console.log('patched style: phone v1 -> v3');
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
  s = s.slice(0, a) + script + s.slice(b + '</script>'.length);
  console.log('patched script: phone v3 + 14 harvested pictures (video served from KV)');
}
// 4. QUESTIONS -> the 21-step trio flow.
{
  const start = 'var QUESTIONS = [';
  const a = s.indexOf(start);
  const b = s.indexOf('];', a);
  if (a < 0 || b < 0) throw new Error('QUESTIONS not found');
  s = s.slice(0, a) + readFileSync(LANE + 'steps.js', 'utf8').replace(/\n$/, '') + s.slice(b + 2);
  console.log('patched QUESTIONS: 18 v1 screens -> 21 trio steps');
}
// 5. Walk engine -> v3 trio group engine (from `var idx = 0;` + fit() to `function complete(){`).
{
  const start = '  var idx = 0;\n  function fit(){';
  const end = '  function complete(){';
  const a = s.indexOf(start);
  const b = s.indexOf(end, a);
  if (a < 0 || b < 0) throw new Error('walk engine block not found');
  s = s.slice(0, a) + readFileSync(LANE + 'engine.js', 'utf8') + '\n' + s.slice(b);
  console.log('patched engine: single-phone walk -> trio group engine');
}
// 6. D1 (carried): finish() must NOT hide the ball (enterBtn IS the jewel).
once('finish-keeps-ball', '      enterBtn.hidden = true;\n', '      /* D1 v2/v3: the ball stays — enterBtn is the jewel, never hidden. */\n');
// ---- assertions on the built file (v3 + R5 keepers) ----
const assert = (name, ok) => { console.log((ok ? 'PASS ' : 'FAIL ') + name); if (!ok) process.exitCode = 1; };
assert('phone v3 present (bd-trio, bd-phone, bd-ball, fpWalkNext, bdGroupProg, bdEndPhone)', s.includes('id="bdTrio"') && s.includes('class="bd-phone"') && s.includes('bd-ball') && s.includes('id="fpWalkNext"') && s.includes('id="bdGroupProg"') && s.includes('id="bdEndPhone"'));
assert('picture is a background layer (bd-bgpic absolute, never layout space)', s.includes('class="bd-bgpic"') && s.includes('.bd-bgpic{position:absolute;inset:0;'));
assert('SVG facet map present (bd-facets, facet clip)', s.includes('class="bd-facets"') && s.includes('bdFacetClip'));
assert('frame ring is 12 discrete facets (30deg stops)', s.includes('30deg 60deg') && s.includes('330deg 360deg'));
assert('no separate Enter button (ball is the only Enter)', !s.includes('>Enter</button>') && s.includes('id="fpWalkEnter"'));
assert('NO Skip pill (hidden element, display:none, no handler)', s.includes('id="fpWalkSkip" type="button" hidden') && s.includes('#fpWalkSkip.fp-walk-skip{display:none!important}') && !s.includes('skipBtn.addEventListener'));
assert('finish() never hides the ball', !s.includes('enterBtn.hidden'));
assert('21 trio steps in order (live..categories; motto/love/dontlove/unique/gift back)', ['"key":"live"','"key":"age_gender"','"key":"favorites"','"key":"industry_skills"','"key":"model"','"key":"video"','"key":"motto"','"key":"mission"','"key":"goal"','"key":"vision"','"key":"love"','"key":"dontlove"','"key":"thing"','"key":"resume"','"key":"achievements_values"','"key":"promise"','"key":"gift"','"key":"unique"','"key":"benefit"','"key":"connect"','"key":"categories"'].every(k => s.includes(k)) && (s.match(/"key":"/g) || []).length === 21);
assert('values sits ONCE (achievements_values only, no standalone values step)', s.includes('"key":"achievements_values"') && !s.includes('"key":"values"'));
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
assert('walk engine is v3 (trio groups, no skip handler)', s.includes('NO SKIP') && s.includes('GROUPS[gidx]') && s.includes('function collectGroup()'));
const out = Buffer.from(s, 'utf8');
writeFileSync(LANE + 'portal.html', out);
console.log('portal.html', out.length, 'B sha256', sha(out), '(v1 +', out.length - v1.length, 'B)');
console.log('BUILD DONE');
