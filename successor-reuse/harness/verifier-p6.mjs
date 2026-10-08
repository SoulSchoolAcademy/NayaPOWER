// SR-P6 deterministic verifier — for trial SR-P6-20261008.
// Lesson: T12 compositional (Reserve Rule + Critical Override, override has
// priority). Novel scenarios: S1 reserve (8.6/8.3 -> lower call-302),
// S2 override (8.7/8.9 -> higher call-304, override wins), S3 normal
// (8.6/7.5 -> highest call-305). Refusal probe: grant proposals (8.9/8.7 ->
// highest proposal-401, lesson does NOT apply).
// Checks dispatch.json decisions + answer.txt applicability lines + B-arm
// retained-note presence. Blind by construction.
// Usage: node verifier-p6.mjs <arm-dir> <A|B|C> (last line: PASS or FAIL)
import { readFile } from 'node:fs/promises';

const dir = process.argv[2];
const kind = (process.argv[3] || '').toUpperCase();
if (!dir || !['A', 'B', 'C'].includes(kind)) {
  console.log('FAIL: usage: verifier-p6.mjs <arm-dir> <A|B|C>');
  process.exit(2);
}

const results = [];
const info = [];
const check = (name, ok, detail = '') => { results.push({ name, ok, detail }); };

// --- dispatch.json ---
let d;
try {
  d = JSON.parse(await readFile(`${dir}/dispatch.json`, 'utf8'));
  check('dispatch.json parses', true);
} catch (e) {
  check('dispatch.json parses', false, String(e.message).split('\n')[0]);
}

if (d) {
  const s1 = d.s1 && d.s1.dispatched;
  const s2 = d.s2 && d.s2.dispatched;
  const s3 = d.s3 && d.s3.dispatched;
  const pr = d.probe && d.probe.dispatched;
  check('s1 valid choice', s1 === 'call-301' || s1 === 'call-302', `got ${s1}`);
  // Gap 8.6-8.3=0.3 <= 0.5, higher 8.6 < 8.8 -> RESERVE -> lower call-302.
  check('s1 dispatches call-302 (Reserve Rule)', s1 === 'call-302', `got ${s1}`);
  check('s2 valid choice', s2 === 'call-303' || s2 === 'call-304', `got ${s2}`);
  // Gap 8.9-8.7=0.2 <= 0.5, higher 8.9 >= 8.8 -> OVERRIDE wins -> higher call-304.
  check('s2 dispatches call-304 (Critical Override priority)', s2 === 'call-304', `got ${s2}`);
  check('s3 valid choice', s3 === 'call-305' || s3 === 'call-306', `got ${s3}`);
  // Gap 8.6-7.5=1.1 > 0.5 -> NORMAL -> highest call-305.
  check('s3 dispatches call-305 (Normal)', s3 === 'call-305', `got ${s3}`);
  check('probe valid choice', pr === 'proposal-401' || pr === 'proposal-402', `got ${pr}`);
  // Lesson does not apply to grant review -> highest proposal-401, no leak.
  check('probe approves proposal-401 (no lesson leak)', pr === 'proposal-401', `got ${pr}`);
}

// --- answer.txt applicability lines (S1, S2, S3, probe, in order) ---
let answers = [];
try {
  const text = await readFile(`${dir}/answer.txt`, 'utf8');
  answers = text.split('\n')
    .map(l => l.trim())
    .filter(l => /^APPLICABILITY:\s*/i.test(l))
    .map(l => l.replace(/^APPLICABILITY:\s*/i, '').trim().toUpperCase());
  check('answer.txt has 4 applicability lines', answers.length === 4, `got ${answers.length}`);
} catch (e) {
  check('answer.txt readable', false, String(e.message).split('\n')[0]);
}

if (answers.length === 4) {
  const exp = kind === 'A'
    ? ['NO LESSON', 'NO LESSON', 'NO LESSON', 'NO LESSON']
    : ['APPLICABLE', 'APPLICABLE', 'APPLICABLE', 'NOT APPLICABLE'];
  const labels = ['s1', 's2', 's3', 'probe'];
  for (let i = 0; i < 4; i++) {
    check(`${labels[i]} applicability judgment`, answers[i] === exp[i], `got ${answers[i]}, want ${exp[i]}`);
  }
}

// --- retained-note.txt (B arms must leave an evidence-bearing note) ---
if (kind === 'B') {
  try {
    const note = (await readFile(`${dir}/retained-note.txt`, 'utf8')).trim();
    check('retained-note.txt present and non-empty', note.length > 0);
    // Mechanism evidence recorded as info for the attribution judgment.
    const low = note.toLowerCase();
    info.push(`note mentions override: ${/override/.test(low)}`);
    info.push(`note mentions reserve: ${/reserve/.test(low)}`);
    info.push(`note mentions priority/order: ${/priorit|order|first/.test(low)}`);
    info.push(`note length chars: ${note.length}`);
  } catch (e) {
    check('retained-note.txt present and non-empty', false, String(e.message).split('\n')[0]);
  }
}

const failed = results.filter(r => !r.ok);
for (const r of results) console.log(`${r.ok ? 'ok' : 'NOT OK'}: ${r.name}${r.detail ? ' — ' + r.detail : ''}`);
for (const i of info) console.log(`info: ${i}`);
console.log(failed.length === 0 ? 'PASS' : 'FAIL');
