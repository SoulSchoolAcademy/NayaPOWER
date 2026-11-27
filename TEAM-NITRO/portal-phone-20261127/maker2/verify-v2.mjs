// Phone v2 verifier: re-fetch the STAGED worker bytes and re-check them
// against the lane files + the v2 transplant + the R5 keepers.
// Nothing on trust. Node only.
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const sha = b => createHash('sha256').update(b).digest('hex');
const LANE = new URL('./', import.meta.url).pathname;
const BASE = 'https://portal-phone-v2-staging.nayapower.workers.dev';
const get = async (p) => {
  const r = await fetch(BASE + p, {headers: {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36'}});
  if (!r.ok) throw new Error(p + ' HTTP ' + r.status);
  return Buffer.from(await r.arrayBuffer());
};
const assert = (name, ok) => { console.log((ok ? 'PASS ' : 'FAIL ') + name); if (!ok) process.exitCode = 1; };
const stagedPortal = await get('/');
const lanePortal = readFileSync(LANE + 'portal.html');
assert('staged portal == lane portal.html (bytes + sha)', stagedPortal.equals(lanePortal));
console.log('portal', stagedPortal.length, 'B sha256', sha(stagedPortal));
assert('staged portal sha == lane portal sha', sha(stagedPortal) === sha(lanePortal));
const stagedIdent = await get('/identity.html');
const laneIdent = readFileSync(LANE + 'identity.html');
assert('staged identity == lane identity.html (bytes + sha)', stagedIdent.equals(laneIdent));
console.log('identity', stagedIdent.length, 'B sha256', sha(stagedIdent));
assert('certificate sha unchanged (57bdd387...)', sha(stagedIdent).startsWith('57bdd387'));
const p = stagedPortal.toString('utf8');
assert('PHONE v2: phone present (bd-phone, bd-ball, fpWalkNext, bdPic, bdFields)', p.includes('class="bd-phone"') && p.includes('bd-ball') && p.includes('id="fpWalkNext"') && p.includes('id="bdPic"') && p.includes('id="bdFields"'));
assert('PHONE v2: SVG facet map, no ray gradient on the jewel', p.includes('class="bd-facets"') && !p.includes('repeating-conic-gradient(from 15deg'));
assert('PHONE v2: frame ring 12 discrete facets', p.includes('30deg 60deg') && p.includes('330deg 360deg'));
assert('PHONE v2: no separate Enter button', !p.includes('>Enter</button>'));
assert('PHONE v2: NO Skip pill anywhere visible', p.includes('#fpWalkSkip.fp-walk-skip{display:none!important}') && !p.includes('skipBtn.addEventListener'));
assert('PHONE v2: finish() never hides the ball', !p.includes('enterBtn.hidden'));
assert('PHONE v2: 17 collapsed steps', p.includes('"key":"live"') && p.includes('"key":"categories"') && (p.match(/"key":"/g) || []).length === 17);
assert('PHONE v2: picture map locked', ['"pic":"nano"', '"pic":"vault"', '"pic":"works"', '"pic":"org"', '"pic":"smartvault"', '"pic":"match"', '"pic":"current"'].every(x => p.includes(x)));
assert('PHONE v2: 8 pictures embedded', (p.match(/data:image\/(jpeg|png);base64,/g) || []).length >= 8);
assert('PHONE v2: live clock + battery', p.includes('id="bdClock"') && p.includes('id="bdBattFill"'));
assert('PHONE v2: copy-out on review screen', p.includes('id="fpWalkCopyAll"'));
assert('PHONE v2: 8 style elements, 10 scripts', (p.match(/<style>/g) || []).length === 8 && (p.match(/<script/g) || []).length === 10);
assert('R5: hover-only menu transplanted (eco-tip, no eco-label)', !p.includes('eco-label') && p.includes('.eco-item .eco-tip{'));
assert('R5: nine R4 destinations unchanged', ['https://nayanet.groovepages.com/aboutus', 'https://howitworks.nayanet.app/', 'https://innovations.nayanet.app/', 'https://12elements.nayanet.app/', 'https://nayanet.app/personal#skills', 'https://grandmission.nayanet.app/', 'https://powercasts.nayapower.workers.dev/', 'https://academy.nayanet.app/', 'https://naya-model-pricing.nayapower.workers.dev/'].every(h => p.includes('href="' + h + '"')));
assert('R5: ring untouched (nayaSpectrum 78s, nayaWhite 31s)', p.includes('animation:nayaSpectrum 78s linear infinite') && p.includes('animation:nayaWhite 31s linear infinite'));
assert('R5: story overlay present, 27 slides', p.includes('id="fpStory"') && p.includes('FP_SLIDES'));
assert('R5: walk gating intact (?walk=1)', p.includes("params.get('walk') !== '1'"));
assert('R5: complete() verify-before-declare intact', p.includes('api/welcome/complete') && p.includes('api/welcome/me'));
const sw = await get('/sw.js');
assert('sw.js 200 + matches lane', sw.equals(readFileSync(LANE + 'sw.js')));
console.log('VERIFY DONE');
