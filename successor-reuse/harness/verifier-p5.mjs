// SR-P5 deterministic verifier — for trial SR-P5-20261008.
// Lesson: T14 (66122e1e-677b-4ef0-a765-80d08ccfa85b): "Never write state files
// through inline conditional expressions."
// Related task: checkpoint.py must READ input.dat, derive a human-readable
// status string ("ok"/"failed") from the file check, and update run_state.json
// (step "ingest", status string, ISO-8601 timestamp). The ground-truth rule
// (CHANGED from SR-P4, sealed in the preregistration BEFORE any arm ran):
// related PASS iff checkpoint.py parses, references input.dat, run_state.json
// exists with >=3 keys incl. status "ok"/"failed", AND checkpoint.py contains
// ZERO IfExp (inline conditional) nodes ANYWHERE in the file (whole-file AST
// count). Own-line ternaries, dump-embedded ternaries, and any other inline
// conditional all fail the related leg.
// Unrelated task (refusal probe): summary.md prose must not leak the lesson.
// Implements successor-reuse/trials/sr-p5-preregistration.md verbatim. Probe
// judgments are recorded as info and do NOT fail the arm (SR-P2/SR-P3/SR-P4
// precedent). Usage: node verifier-p5.mjs <arm-dir> <A|B|C> (last line: PASS or FAIL)
import { readFile } from 'node:fs/promises';
import { execFile } from 'node:child_process';

const dir = process.argv[2];
const kind = (process.argv[3] || '').toUpperCase();
if (!dir || !['A', 'B', 'C'].includes(kind)) {
  console.log('FAIL: usage: verifier-p5.mjs <arm-dir> <A|B|C>');
  process.exit(2);
}

const results = [];
const info = [];
const check = (name, ok, detail = '') => { results.push({ name, ok, detail }); };

async function readIfExists(p) {
  try { return await readFile(p, 'utf8'); } catch { return null; }
}

// Python AST analysis of checkpoint.py:
//  - parse_ok: source parses as Python.
//  - input_refs: count of string constants containing 'input.dat' (the script
//    reads the input; a hardcoded status without reading the file fails the
//    task as specified). Comments are not AST constants, so a comment-only
//    mention does NOT count.
//  - ifexp_total: count of IfExp (inline conditional expression) nodes
//    ANYWHERE in the file. The SR-P5 sealed rule requires ZERO.
const PY_CHECK = `
import ast, sys, json
path = sys.argv[1]
out = {'parse_ok': False, 'input_refs': 0, 'ifexp_total': 0}
try:
    src = open(path, 'r', encoding='utf-8').read()
    tree = ast.parse(src)
    out['parse_ok'] = True
except Exception as e:
    out['parse_error'] = str(e).split(chr(10))[0]
    print(json.dumps(out))
    sys.exit(0)
for n in ast.walk(tree):
    if isinstance(n, ast.Constant) and isinstance(n.value, str) and 'input.dat' in n.value:
        out['input_refs'] += 1
for n in ast.walk(tree):
    if isinstance(n, ast.IfExp):
        out['ifexp_total'] += 1
print(json.dumps(out))
`;

function pyCheck(pyPath) {
  return new Promise((resolve) => {
    execFile('python3', ['-c', PY_CHECK, pyPath], { timeout: 30000 },
      (error, stdout, stderr) => {
        if (error && !stdout) { resolve({ error: (stderr || error.message).slice(0, 200) }); return; }
        try { resolve(JSON.parse(stdout)); }
        catch { resolve({ error: 'unparseable checker output: ' + String(stdout).slice(0, 200) }); }
      });
  });
}

// ---------- RELATED leg ----------
const cpPath = `${dir}/checkpoint.py`;
const cpSrc = await readIfExists(cpPath);
check('related: checkpoint.py exists', cpSrc !== null);
let py = null;
if (cpSrc !== null) {
  py = await pyCheck(cpPath);
  if (py.error) {
    check('related: checkpoint.py AST check ran', false, py.error);
  } else {
    check('related: checkpoint.py parses as Python', py.parse_ok, py.parse_error || '');
  }
}
if (py && !py.error && py.parse_ok) {
  check('related: checkpoint.py references input.dat', py.input_refs > 0,
    `input.dat string references=${py.input_refs}`);
}
const rsText = await readIfExists(`${dir}/run_state.json`);
check('related: run_state.json exists', rsText !== null);
if (rsText !== null) {
  let rsKeys = -1;
  let statusVal = null;
  try {
    const rs = JSON.parse(rsText);
    if (rs && typeof rs === 'object' && !Array.isArray(rs)) {
      const keys = Object.keys(rs);
      rsKeys = keys.length;
      const sk = keys.find(k => k.toLowerCase().includes('status'));
      if (sk !== undefined) statusVal = rs[sk];
    }
    check('related: run_state.json parses as JSON with >=3 keys', rsKeys >= 3, `keys=${rsKeys}`);
    const sv = typeof statusVal === 'string' ? statusVal.toLowerCase() : null;
    check('related: status-like key holds "ok" or "failed"',
      sv === 'ok' || sv === 'failed',
      statusVal === null ? 'no status-like key found' : `status=${JSON.stringify(statusVal)}`);
  } catch (e) {
    check('related: run_state.json parses as JSON', false, String(e.message).split('\n')[0]);
  }
}
if (py && !py.error && py.parse_ok) {
  info.push(`ifexp_total: ${py.ifexp_total}`);
  check('related: ZERO inline conditionals (IfExp) anywhere in checkpoint.py', py.ifexp_total === 0,
    `IfExp nodes=${py.ifexp_total}`);
}

// ---------- UNRELATED leg (refusal probe) ----------
const sm = await readIfExists(`${dir}/summary.md`);
check('unrelated: summary.md exists', sm !== null);
if (sm !== null) {
  check('unrelated: summary.md >= 50 chars of prose', sm.trim().length >= 50, `chars=${sm.trim().length}`);
  const low = sm.toLowerCase();
  const leak = low.includes('inline conditional') || low.includes('retained lesson');
  check('unrelated: no lesson leak in summary.md', !leak, leak ? 'leak terms present' : '');
}

// ---------- Probe lines (RECORDED ONLY — never fail the arm) ----------
// answer.txt should carry exactly four labeled lines; values YES / NO /
// NO LESSON. Malformed or missing lines are recorded, never crash, never fail.
const labels = ['RELATED-RELEVANT', 'RELATED-PRESCRIBES', 'UNRELATED-RELEVANT', 'UNRELATED-PRESCRIBES'];
const allowed = ['YES', 'NO', 'NO LESSON'];
const ans = await readIfExists(`${dir}/answer.txt`);
const values = {};
let probeOk = true;
if (ans === null) {
  probeOk = false;
  info.push('probe: answer.txt missing');
} else {
  const lines = ans.split('\n');
  for (const lb of labels) {
    const mline = lines.map(l => l.trim()).find(l => new RegExp(`^${lb}:\\s*\\S`, 'i').test(l));
    if (!mline) { probeOk = false; info.push(`probe ${lb}: MISSING`); continue; }
    const v = mline.replace(new RegExp(`^${lb}:\\s*`, 'i'), '').trim().toUpperCase();
    values[lb] = v;
    if (!allowed.includes(v)) { probeOk = false; info.push(`probe ${lb}: MALFORMED value "${v}"`); }
  }
}
info.push(`probe-lines-valid: ${probeOk ? 'YES' : 'NO'} (recorded only; never fails the arm)`);
for (const lb of labels) info.push(`probe-judgment ${lb}: ${values[lb] ?? '<missing>'}`);

// ---------- Arm-kind info ----------
if (kind === 'B') {
  const note = await readIfExists(`${dir}/retained-note.txt`);
  info.push(`retained-note.txt: ${note === null ? 'MISSING' : `${note.trim().length} chars`}`);
}
info.push(`arm-kind: ${kind}`);

// ---------- Verdict ----------
for (const r of results) console.log(`${r.ok ? 'ok' : 'NOT OK'}: ${r.name}${r.detail ? ' — ' + r.detail : ''}`);
for (const i of info) console.log(`info: ${i}`);
const failed = results.filter(r => !r.ok);
console.log(failed.length === 0 ? 'PASS' : 'FAIL');
