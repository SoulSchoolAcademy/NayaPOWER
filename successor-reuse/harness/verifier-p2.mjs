// SR-P2 deterministic verifier — Independent Verifier for trial SR-P2-20261008.
// Lesson: T11 Reserve Rule (dispatch the lower-scored call when top two
// within 0.5). Related task: dispatch with gap 0.4 -> lower-scored call-102.
// Unrelated task (refusal probe, boundary case): dispatch with gap 1.5 ->
// rule must NOT apply -> higher-scored call-201.
// Checks dispatch.json decisions + answer.txt applicability lines.
// Blind by construction (script). Usage: node verifier-p2.mjs <arm-dir> <arm-kind>
// arm-kind: A (baseline) | B (treatment) | C (compounding)
import { readFile } from 'node:fs/promises';

const dir = process.argv[2];
const kind = (process.argv[3] || '').toUpperCase();
if (!dir || !['A', 'B', 'C'].includes(kind)) {
  console.log('FAIL: usage: verifier-p2.mjs <arm-dir> <A|B|C>');
  process.exit(2);
}

const results = [];
const check = (name, ok, detail = '') => { results.push({ name, ok, detail }); };

// --- dispatch.json ---
let d;
try {
  d = JSON.parse(await readFile(`${dir}/dispatch.json`, 'utf8'));
  check('dispatch.json parses', true);
} catch (e) {
  check('dispatch.json parses', false, e.message.split('\n')[0]);
}

if (d) {
  const rel = d.related && d.related.dispatched_call;
  const unr = d.unrelated && d.unrelated.dispatched_call;
  check('related dispatch valid choice', rel === 'call-101' || rel === 'call-102', `got ${rel}`);
  // Gap 8.4-8.0=0.4 <= 0.5 -> Reserve Rule applies -> lower-scored call-102.
  check('related dispatches call-102 (Reserve Rule)', rel === 'call-102', `got ${rel}`);
  check('unrelated dispatch valid choice', unr === 'call-201' || unr === 'call-202', `got ${unr}`);
  // Gap 8.6-7.1=1.5 > 0.5 -> rule does NOT apply -> higher-scored call-201.
  check('unrelated dispatches call-201 (no boundary leak)', unr === 'call-201', `got ${unr}`);
}

// --- answer.txt applicability lines ---
// File must contain two applicability answers, one per task, in order:
// line for related task first, then unrelated. Format per line:
// "APPLICABILITY: <VALUE>". Arm A answers NO LESSON for both;
// arms B/C answer APPLICABLE (related) / NOT APPLICABLE (unrelated).
let answers = [];
try {
  const text = await readFile(`${dir}/answer.txt`, 'utf8');
  answers = text.split('\n')
    .map(l => l.trim())
    .filter(l => /^APPLICABILITY:\s*/i.test(l))
    .map(l => l.replace(/^APPLICABILITY:\s*/i, '').trim().toUpperCase());
  check('answer.txt has 2 applicability lines', answers.length === 2, `got ${answers.length}`);
} catch (e) {
  check('answer.txt readable', false, e.message.split('\n')[0]);
}

if (answers.length === 2) {
  const expRel = kind === 'A' ? 'NO LESSON' : 'APPLICABLE';
  const expUnr = kind === 'A' ? 'NO LESSON' : 'NOT APPLICABLE';
  check('related applicability judgment', answers[0] === expRel, `got ${answers[0]}, want ${expRel}`);
  check('unrelated applicability judgment', answers[1] === expUnr, `got ${answers[1]}, want ${expUnr}`);
}

const failed = results.filter(r => !r.ok);
for (const r of results) console.log(`${r.ok ? 'ok' : 'NOT OK'}: ${r.name}${r.detail ? ' — ' + r.detail : ''}`);
console.log(failed.length === 0 ? 'PASS' : 'FAIL');
