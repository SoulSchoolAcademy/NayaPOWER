// Verify the front-page fix: harvest proof + nothing-else-changed proof.
// Node only. Exits non-zero on any failure.
import {readFileSync, writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
const sha = b => createHash('sha256').update(b).digest('hex');
const LANE = new URL('./', import.meta.url).pathname;
const R2 = '/home/hatch/workspace/team-nitro/portal-consolidated-20261125/maker/';
const base = readFileSync(R2 + 'portal.html', 'utf8');
const html = readFileSync(LANE + 'portal.html', 'utf8');
const harvest = JSON.parse(readFileSync(LANE + 'evidence/harvest.json', 'utf8'));
const agmt = readFileSync(LANE + 'evidence/agreement-live.html', 'utf8');
let fails = 0;
const check = (name, ok, extra = '') => {
  console.log((ok ? 'PASS ' : 'FAIL ') + name + (extra ? ' — ' + extra : ''));
  if (!ok) fails++;
};
// --- Harvest proof: right N byte-identical to agreement EMBED.ball. ---
const ball = agmt.match(/EMBED\.ball = "([^"]+)"/)[1];
const rightImg = html.match(/ncorner-right"[^>]*><img src="([^"]+)" alt="([^"]*)"/);
check('right N src == agreement EMBED.ball verbatim', rightImg && rightImg[1] === ball);
check('right N alt harvested verbatim', rightImg && rightImg[2] === 'The red N — a raised glass ball with a gold N');
check('right N webp bytes sha', rightImg && sha(Buffer.from(rightImg[1].split(',')[1], 'base64')) === '2a4b10fdf01360120166090c25d91407541cb0c5d1b3931bae847840ad207069');
const leftImg = html.match(/ncorner-left"[^>]*><img src="data:image\/jpeg;base64,([^"]+)"/);
check('left N untouched (EMBED.logo sha)', leftImg && sha(Buffer.from(leftImg[1], 'base64')) === '08b753d3e79ff334598e97ac500a888d9d15dd57412cc7afc37ec30c9bc15f92');
// --- Defect 1 proof. ---
const sentP = html.match(/<p class="fp-deed-sentence" id="fpDeedSentence">(.*?)<\/p>/s);
check('visible front-page <p> holds only the ⓘ button', sentP && sentP[1].trim().startsWith('<button') && !sentP[1].includes('By entering'));
const parasSrc = html.match(/var PARAS = (\[.*?\]);/s);
let paras = null;
try { paras = JSON.parse(parasSrc[1]); } catch (e) { /* fallthrough */ }
check('PARAS parses, 13 entries', Array.isArray(paras) && paras.length === 13, paras ? paras.length + ' entries' : 'parse failed');
check('PARAS[0] is the moved sentence verbatim',
  paras && paras[0] === 'By entering your name, you make it official — you are signing the Collective Agreement, and you get the deed to your own world: high-level digital real estate — your personal page, your business, your space — free forever.');
check('PARAS[1..12] unchanged vs R2', (() => {
  const b = JSON.parse(base.match(/var PARAS = (\[.*?\]);/s)[1]);
  return paras && b.length === 12 && paras.slice(1).every((p, i) => p === b[i]);
})());
// --- Nothing else changed: nine, questions, endpoints, returning. ---
const hrefs = s => [...s.matchAll(/<a [^>]*class="eco-item"[^>]*>/g)].map(m => m[0].match(/href="([^"]+)"/)[1]);
const hBase = hrefs(base), hNew = hrefs(html);
check('final nine hrefs identical to R2', JSON.stringify(hBase) === JSON.stringify(hNew), hNew.length + ' anchors');
const q = s => (s.match(/var QUESTIONS = (\[.*?\n\];)/s) || [null, null])[1];
check('QUESTIONS block identical to R2', q(base) === q(html));
const eps = s => [...new Set([...s.matchAll(/https:\/\/[a-z0-9.-]*(?:walkthrough-15|naya-welcome|nayapower)[a-z0-9./_-]*/gi)].map(m => m[0]))].sort();
check('worker endpoint URLs identical to R2', JSON.stringify(eps(base)) === JSON.stringify(eps(html)), eps(html).join(' | '));
check('returning greeting block identical', base.includes('Welcome back') === html.includes('Welcome back'));
check('certificate untouched (identity sha)', sha(readFileSync(LANE + 'identity-consolidated.html')) === '57bdd3873f65104f3ee6f4648cfec4a1a556a78ea8b7fb57153cd49da528af4b');
// --- Inline scripts still parse. ---
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
let scriptFails = 0;
scripts.forEach((src, i) => {
  const f = join(tmpdir(), 'fpfix-script-' + i + '.js');
  writeFileSync(f, src);
  try { execFileSync('node', ['--check', f], {stdio: 'pipe'}); }
  catch (e) { scriptFails++; console.log('FAIL script ' + i + ' node --check'); }
});
check('all inline scripts node --check', scriptFails === 0, scripts.length + ' scripts, ' + scriptFails + ' failed');
console.log('portal.html', html.length, 'B sha256', sha(Buffer.from(html)));
console.log(fails === 0 ? 'ALL VERIFY CHECKS PASS' : fails + ' CHECKS FAILED');
process.exit(fails === 0 ? 0 : 1);
