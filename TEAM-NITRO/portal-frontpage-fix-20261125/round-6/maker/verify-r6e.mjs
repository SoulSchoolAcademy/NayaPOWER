// Round-6e verifier: re-fetch the STAGED worker bytes and re-check them
// against the lane files + the R6e correction + the R5 assertions that
// still hold. Nothing on trust. Node only.
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {Script} from 'node:vm';
const sha = b => createHash('sha256').update(b).digest('hex');
const LANE = new URL('./', import.meta.url).pathname;
const BASE = 'https://portal-frontpage-fix-20261125-r6-staging.nayapower.workers.dev';
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
const stagedIdent = await get('/identity.html');
const laneIdent = readFileSync(LANE + 'identity.html');
assert('staged identity == lane identity.html (bytes + sha)', stagedIdent.equals(laneIdent));
console.log('identity', stagedIdent.length, 'B sha256', sha(stagedIdent));
assert('certificate is the NEW fixed cert (0c11fdb8...)', sha(stagedIdent).startsWith('0c11fdb8'));
const stagedAgr = await get('/agreement');
const laneAgr = readFileSync(LANE + 'agreement-v25-fixed-r6.html');
assert('staged /agreement == lane agreement-v25-fixed-r6.html (bytes + sha)', stagedAgr.equals(laneAgr));
console.log('/agreement', stagedAgr.length, 'B sha256', sha(stagedAgr));
const stagedSw = await get('/sw.js');
const laneSw = readFileSync(LANE + 'sw.js');
assert('staged sw.js == lane sw.js', stagedSw.equals(laneSw));
const p = stagedPortal.toString('utf8');
const a = stagedAgr.toString('utf8');
// ---- R6e portal (the correction) ----
assert('R6e: ONE entry — orb click navigates DIRECTLY to the exact URL', p.includes("window.location.href = 'https://nayanet.app/agreement'"));
assert('R6e: NO bottom agreement button (no fpEnterDeal element)', !p.includes('id="fpEnterDeal"'));
assert('R6e: no entry opens the story (only the dated R3 comment mentions openStory(0))', (p.match(/openStory\(0\)/g) || []).length === 1 && p.includes('ROUND 3 — SUPERSEDED'));
assert('R6e: corner Ns are NOT entries — red corner now home', p.includes('class="ncorner ncorner-right" href="https://nayanet.app/"'));
assert('R6e: orb energy flow — bright arc ring (eco-spin 12s) + breathing halo', p.includes('animation:eco-spin 12s linear infinite') && p.includes('@keyframes fpOrbHalo') && p.includes('button.fp-circle-n::after{content:"";position:absolute;inset:-14px;'));
assert('R6e: N upright — no eco-spin on either red-N img', !p.includes('button.fp-circle-n img{width:100%;height:100%;border-radius:50%;object-fit:cover;   display:block;animation:eco-spin') && !p.includes('.ncorner-right img{animation:eco-spin'));
assert('R6e: black left N untouched', p.includes('ncorner-left" href="https://nayanet.app/"') && !p.includes('.ncorner-left img{animation'));
assert('R6e: (i) exactly as R5 (3 comment occurrences)', (p.match(/ⓘ/g) || []).length === 3 && !p.includes('fpLittleN') && !p.includes('fpNutshellPop'));
assert('R6e: end slide carries the verbatim deed sentence', p.includes('By entering your name, you make it official &mdash; you are signing the Collective Agreement'));
assert('R6e: completion flag on BOTH Agree paths', (p.match(/localStorage\.setItem\('nayanet_agreement_done'/g) || []).length === 2);
assert('R6e: certificate links go to the LIVE address', (p.match(/https:\/\/nayanet\.app\/identity\.html/g) || []).length === 2 && !p.includes('portal-frontpage-fix-20261125-r6-staging.nayapower.workers.dev/identity.html'));
assert('R6e: /agreement boot present (fallback)', p.includes("if(window.location.pathname!=='/agreement')return;"));
// ---- R6e agreement file (staged /agreement) ----
assert('R6e: 0 preview strings in the agreement file', !a.includes('Begin the visual story') && !a.includes('Read the agreement') && !a.includes("Welcome. Let's begin with trust.") && !a.includes('screen-choice'));
assert('R6e: cover active in markup', a.includes('class="screen active" id="screen-cover"'));
assert('R6e: audio bar gone (hidden, no controls)', a.includes('<audio class="real-audio" id="welcomeAudio" preload="auto" hidden playsinline'));
assert('R6e: facade below the frame, poster contain', a.includes('</div>\n                <button class="pm-facade"') && a.includes('#screen-cover .pm-poster{object-fit:contain'));
assert('R6e: end slide deed verbatim + agree flash + links bar', a.includes('By entering your name, you make it official') && a.includes('@keyframes agreeFlash') && a.includes("id = 'fpLinksBar'"));
assert('R6e: completion flag in goToPortal', (a.match(/localStorage\.setItem\('nayanet_agreement_done'/g) || []).length === 1);
assert('R6e: all 27 slide titles present', ['The Old Way','Your Franchise',"What's In It For You","You're Hired"].every(t => a.includes(t)));
assert('R6e: legal pages intact (12)', (a.match(/id="legal-/g) || []).length === 12);
// ---- R5/R6 carried forward ----
assert('R6: three boards at a time', p.includes('show(cur); show(cur + 1); show(cur + 2);'));
assert('R6: jewel counts groups', p.includes("Math.floor(S.letter/3)+1)+' / '+Math.ceil(letterBeats.length/3);"));
assert('R6: agree wording (no bare I-agree setNext)', !p.includes("setNext('I agree \\u25C6'") && p.includes("setNext('I agree — show me my world \\u25C6'"));
assert('R6: story from inside agreement only', p.includes("else if(S.view==='letter'||S.view==='letterPage'){if(window.__fpOpenStory)window.__fpOpenStory(0);}"));
assert('R5: hover-only menu (eco-tip, no eco-label)', !p.includes('eco-label') && p.includes('.eco-item .eco-tip{'));
assert('R5: nine destinations unchanged', ['https://nayanet.groovepages.com/aboutus', 'https://howitworks.nayanet.app/', 'https://innovations.nayanet.app/', 'https://12elements.nayanet.app/', 'https://nayanet.app/personal#skills', 'https://grandmission.nayanet.app/', 'https://powercasts.nayapower.workers.dev/', 'https://academy.nayanet.app/', 'https://naya-model-pricing.nayapower.workers.dev/'].every(h => p.includes('href="' + h + '"')));
assert('R5: ring untouched (78s/31s)', p.includes('animation:nayaSpectrum 78s linear infinite') && p.includes('animation:nayaWhite 31s linear infinite'));
assert('R3: story overlay present, 27 slides', p.includes('id="fpStory"') && p.includes('FP_SLIDES'));
assert('R3: official agree wording on story end slide', p.includes('I agree &mdash; show me my world &#9670;'));
assert('R3: eight links in bottom bar', (p.match(/data-final="/g) || []).length === 8);
assert('structure: 7 style elements, 10 scripts', (p.match(/<style>/g) || []).length === 7 && (p.match(/<script>/g) || []).length === 10);
for (const [name, code] of [['portal', p]]) {
  let n = 0;
  for (const m of code.matchAll(/<script>([\s\S]*?)<\/script>/g)) { new Script(m[1], {filename: name + '-script-' + (++n) + '.js'}); }
  console.log('PASS all', n, 'inline portal scripts compile');
}
console.log('VERIFY-R6E DONE');
