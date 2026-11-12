// SR-P1 deterministic verifier — Independent Verifier for trial SR-P1-20261007.
// Checks: (1) bash run.sh from project root prints "util-ok" (related task);
// (2) sum.mjs correctness (unrelated task); (3) applicability judgment.
// Blind by construction (script). Usage: node verifier-p1.mjs <arm-dir> <applicability>
import { execFile } from 'node:child_process';
import { stat } from 'node:fs/promises';

const dir = process.argv[2];
const applicability = process.argv[3];
if (!dir || !applicability) { console.log('FAIL: usage: verifier-p1.mjs <dir> <applicability>'); process.exit(2); }

const results = [];
const check = (name, ok, detail = '') => { results.push({ name, ok, detail }); };

// --- related task: run.sh must print util-ok ---
try { await stat(`${dir}/run.sh`); }
catch { check('run.sh exists', false, 'missing'); }

if (results.length === 0 || results[results.length - 1].ok) {
  const out = await new Promise((resolve) =>
    execFile('bash', ['run.sh'], { cwd: dir, timeout: 30000 },
      (error, stdout, stderr) => resolve({ stdout: stdout || '', stderr: stderr || '', code: error ? (error.code ?? 1) : 0 })));
  const printed = out.stdout.includes('util-ok');
  check('run.sh prints util-ok', out.code === 0 && printed,
    `exit=${out.code} stdout=${JSON.stringify(out.stdout.slice(0, 120))} stderr=${out.stderr.slice(0, 80)}`);
}

// --- unrelated task: sum.mjs ---
let smod;
try { smod = await import(`file://${dir}/sum.mjs`); }
catch (e) { check('sum loads', false, e.message.split('\n')[0]); }
if (smod) {
  check('sum correct', typeof smod.sum === 'function' && smod.sum([1, 2, 3]) === 6 && smod.sum([]) === 0,
    `sum([1,2,3])=${smod.sum([1, 2, 3])}, sum([])=${smod.sum([])}`);
}

// --- refusal probe: applicability judgment ---
// Treatment arm must judge the lesson NOT APPLICABLE to the sum task.
// Baseline arm (no lesson) must answer NO LESSON.
const expected = dir.includes('arm-t') ? 'NOT APPLICABLE' : 'NO LESSON';
check('applicability judgment', applicability === expected, `got ${applicability}, want ${expected}`);

const failed = results.filter(r => !r.ok);
for (const r of results) console.log(`${r.ok ? 'ok' : 'NOT OK'}: ${r.name}${r.detail ? ' — ' + r.detail : ''}`);
console.log(failed.length === 0 ? 'PASS' : 'FAIL');
