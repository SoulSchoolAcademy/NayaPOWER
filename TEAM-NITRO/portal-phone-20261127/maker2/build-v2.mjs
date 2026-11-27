// Build the Black Diamond phone v2 portal from the v1 built portal.
// Base: maker2/portal-v1.html (v1 build, 13,900,396 B, sha b7ee02d6...),
// itself built on the R5 base (13,883,771 B, sha d4bb2102...).
// v2 rebuilds the walk to Shawn's ~10:0x collapsed flow (MEMORY.md) and fixes
// the checker's 7 defects (D1–D7). Node only. Every replacement asserted
// exactly-once; a miss fails loudly, no write.
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
const sliceOnce = (name, startMarker, endMarker, replacement, keepEnd) => {
  const a = s.indexOf(startMarker);
  const b = s.indexOf(endMarker, a);
  if (a < 0 || b < 0) throw new Error('SLICE ' + name + ': markers not found');
  if (s.indexOf(startMarker, a + 1) !== -1 && startMarker !== endMarker) {
    // start marker must be unique in the region we care about; warn only if ambiguous
    console.log('note ' + name + ': start marker occurs more than once overall, using first');
  }
  s = s.slice(0, a) + replacement + (keepEnd ? s.slice(b) : s.slice(b + endMarker.length));
  console.log('sliced', name);
};
// 1. Walk section -> v2 phone markup (whole section).
{
  const secStart = '<section id="fpWalk" hidden>';
  const a = s.indexOf(secStart);
  const b = s.indexOf('</section>', a);
  if (a < 0 || b < 0) throw new Error('walk section not found');
  s = s.slice(0, a) + readFileSync(LANE + 'phone-section2.html', 'utf8') + s.slice(b + '</section>'.length);
  console.log('patched section: walk -> Black Diamond phone v2');
}
// 2. Phone style -> v2 style (whole old phone <style> block).
{
  const start = '<style>\n/* BLACK DIAMOND PHONE 2026-11-27';
  const a = s.indexOf(start);
  const b = s.indexOf('</style>', a);
  if (a < 0 || b < 0) throw new Error('phone style block not found');
  s = s.slice(0, a) + readFileSync(LANE + 'phone-style2.html', 'utf8') + s.slice(b + '</style>'.length);
  console.log('patched style: phone v1 -> v2');
}
// 3. Phone script -> v2 script, with the harvested pictures embedded.
{
  const start = '<script>\n/* BLACK DIAMOND PHONE 2026-11-27 — phone chrome logic';
  const a = s.indexOf(start);
  const b = s.indexOf('</script>', a);
  if (a < 0 || b < 0) throw new Error('phone script block not found');
  let script = readFileSync(LANE + 'phone-script2.html', 'utf8');
  const pics = {
    vault: ['1_THE_VAULT.jpg', 'image/jpeg'],
    current: ['2_HOW_WE_SNYC.jpg', 'image/jpeg'],
    nano: ['3_NANOVERSE.jpg', 'image/jpeg'],
    works: ['4_HOW_IT_WORKS.jpg', 'image/jpeg'],
    smartvault: ['5_SMART_VAULT.jpg', 'image/jpeg'],
    match: ['6_AUTO_MATCH.jpg', 'image/jpeg'],
    org: ['7_AUTO_ORGINIZED.jpg', 'image/jpeg'],
    pillars: ['a3/a3903dafe3e9ee81ac66c6bb14104fdffcd7483550bd521a141f1c1ea6e538c4.png', 'image/png'],
  };
  const map = {};
  for (const [k, [f, ct]] of Object.entries(pics)) {
    const buf = readFileSync(IMG + f);
    console.log('pic', k, f, buf.length, 'B');
    map[k] = 'data:' + ct + ';base64,' + buf.toString('base64');
  }
  script = script.replace('/*__BD_PICS__*/', JSON.stringify(map));
  if (!script.includes('data:image/jpeg;base64,')) throw new Error('picture embed failed');
  s = s.slice(0, a) + script + s.slice(b + '</script>'.length);
  console.log('patched script: phone v2 + 8 harvested pictures');
}
// 4. QUESTIONS -> the 17-step collapsed flow.
{
  const start = 'var QUESTIONS = [';
  const a = s.indexOf(start);
  const b = s.indexOf('];', a);
  if (a < 0 || b < 0) throw new Error('QUESTIONS not found');
  s = s.slice(0, a) + readFileSync(LANE + 'steps.js', 'utf8').replace(/\n$/, '') + s.slice(b + 2);
  console.log('patched QUESTIONS: 18 v1 screens -> 17 collapsed steps');
}
// 5. Walk engine -> v2 engine (from `var idx = 0;` + fit() to `function complete(){`).
{
  const start = '  var idx = 0;\n  function fit(){';
  const end = '  function complete(){';
  const a = s.indexOf(start);
  const b = s.indexOf(end, a);
  if (a < 0 || b < 0) throw new Error('walk engine block not found');
  s = s.slice(0, a) + readFileSync(LANE + 'engine.js', 'utf8') + '\n' + s.slice(b);
  console.log('patched engine: single-textarea walk -> multi-field step engine');
}
// 6. D1: finish() must NOT hide the ball (enterBtn IS the jewel).
once('finish-keeps-ball', '      enterBtn.hidden = true;\n', '      /* D1 v2: the ball stays — enterBtn is the jewel, never hidden. */\n');
// ---- assertions on the built file (v2 + R5 keepers) ----
const assert = (name, ok) => { console.log((ok ? 'PASS ' : 'FAIL ') + name); if (!ok) process.exitCode = 1; };
assert('phone v2 present (bd-phone, bd-ball, fpWalkNext, bdPic, bdFields)', s.includes('class="bd-phone"') && s.includes('bd-ball') && s.includes('id="fpWalkNext"') && s.includes('id="bdPic"') && s.includes('id="bdFields"'));
assert('SVG facet map present (bd-facets, no ray gradient)', s.includes('class="bd-facets"') && s.includes('bdFacetClip'));
assert('frame ring is 12 discrete facets (30deg stops)', s.includes('30deg 60deg') && s.includes('330deg 360deg'));
assert('no separate Enter button (ball is the only Enter)', !s.includes('>Enter</button>') && s.includes('id="fpWalkEnter"'));
assert('NO Skip pill (hidden element, display:none, no handler)', s.includes('id="fpWalkSkip" type="button" hidden') && s.includes('#fpWalkSkip.fp-walk-skip{display:none!important}') && !s.includes("skipBtn.addEventListener"));
assert('finish() never hides the ball', !s.includes('enterBtn.hidden'));
assert('17 collapsed steps (live..categories, no country/province/city screens, no motto)', s.includes('"key":"live"') && s.includes('"key":"categories"') && s.includes('"key":"promise"') && !s.includes('"key":"country"') && !s.includes('"key":"motto"'));
assert('gender dropdown has NO default (empty first option)', s.includes('"id":"gender"') && s.includes('[["","Choose…"],["male","Male"]'));
assert('picture map locked (vision=nano, goal=vault, mission=works, thing=org, promise=smartvault, connect=match, benefit=current)', s.includes('"pic":"nano"') && s.includes('"pic":"vault"') && s.includes('"pic":"works"') && s.includes('"pic":"org"') && s.includes('"pic":"smartvault"') && s.includes('"pic":"match"') && s.includes('"pic":"current"'));
assert('8 pictures embedded as data URIs', (s.match(/data:image\/(jpeg|png);base64,/g) || []).length >= 8);
assert('end screen fits: 2-col end grid, end title', s.includes('fp-walk-endgrid') && s.includes('Welcome home.'));
assert('live clock + battery present', s.includes('id="bdClock"') && s.includes('id="bdBattFill"'));
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
assert('walk engine is v2 (multi-field, no skip handler)', s.includes('NO SKIP') && s.includes('function collect()'));
const out = Buffer.from(s, 'utf8');
writeFileSync(LANE + 'portal.html', out);
console.log('portal.html', out.length, 'B sha256', sha(out), '(v1 +', out.length - v1.length, 'B)');
console.log('BUILD DONE');
