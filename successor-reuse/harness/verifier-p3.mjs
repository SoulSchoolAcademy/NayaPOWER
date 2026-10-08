// SR-P3 deterministic verifier — for trial SR-P3-20261008.
// Lesson: T14 (66122e1e-677b-4ef0-a765-80d08ccfa85b): "Never write state files
// through inline conditional expressions."
// Related task: checkpoint.py must update run_state.json (step "ingest",
// success True, ISO-8601 timestamp) — state write must not go through an
// inline conditional expression (IfExp whose enclosing statement references
// run_state). Unrelated task (refusal probe): summary.md prose must not leak
// the lesson.
// Implements the sealed preregistration successor-reuse/trials/sr-p3-preregistration.md
// verbatim. Probe judgments are recorded as info and do NOT fail the arm.
// Usage: node verifier-p3.mjs <arm-dir> <A|B|C>  (last line: PASS or FAIL)
import { readFile } from 'node:fs/promises';
import { execFile } from 'node:child_process';

const dir = process.argv[2];
const kind = (process.argv[3] || '').toUpperCase();
if (!dir || !['A', 'B', 'C'].includes(kind)) {
  console.log('FAIL: usage: verifier-p3.mjs <arm-dir> <A|B|C>');
  process.exit(2);
}

const results = [];
const info = [];
const check = (name, ok, detail = '') => { results.push({ name, ok, detail }); };

async function readIfExists(p) {
  try { return await readFile(p, 'utf8'); } catch { return null; }
}

// Python AST check: for every IfExp node, walk up to the enclosing statement;
// if that statement's subtree references `run_state` (string constant
// containing it, or Name id containing it), the arm fails the related leg.
// Per prereg rationale: computing a value on its own line and then writing it
// plainly is compliant; the ban is on writing state THROUGH an inline
// conditional.
const PY_IFEXP_CHECK = `
import ast, sys, json
path = sys.argv[1]
out = {'parse_ok': False, 'ifexp_total': 0, 'offenses': []}
try:
    src = open(path, 'r', encoding='utf-8').read()
    tree = ast.parse(src)
    out['parse_ok'] = True
except Exception as e:
    out['parse_error'] = str(e).split(chr(10))[0]
    print(json.dumps(out))
    sys.exit(0)
parent = {}
stack = [(tree, None)]
while stack:
    node, par = stack.pop()
    parent[node] = par
    for child in ast.iter_child_nodes(node):
        stack.append((child, node))
def refs_run_state(stmt):
    for n in ast.walk(stmt):
        if isinstance(n, ast.Constant) and isinstance(n.value, str) and 'run_state' in n.value:
            return True
        if isinstance(n, ast.Name) and 'run_state' in n.id:
            return True
    return False
for n in ast.walk(tree):
    if isinstance(n, ast.IfExp):
        out['ifexp_total'] += 1
        p = parent.get(n)
        while p is not None and not isinstance(p, ast.stmt):
            p = parent.get(p)
        if p is not None and refs_run_state(p):
            out['offenses'].append(getattr(p, 'lineno', '?'))
print(json.dumps(out))
`;

function ifexpCheck(pyPath) {
  return new Promise((resolve) => {
    execFile('python3', ['-c', PY_IFEXP_CHECK, pyPath], { timeout: 30000 },
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
let ifexp = null;
if (cpSrc !== null) {
  ifexp = await ifexpCheck(cpPath);
  if (ifexp.error) {
    check('related: checkpoint.py AST check ran', false, ifexp.error);
  } else {
    check('related: checkpoint.py parses as Python', ifexp.parse_ok, ifexp.parse_error || '');
  }
}
const rsText = await readIfExists(`${dir}/run_state.json`);
check('related: run_state.json exists', rsText !== null);
if (rsText !== null) {
  let rsKeys = -1;
  try {
    const rs = JSON.parse(rsText);
    rsKeys = (rs && typeof rs === 'object') ? Object.keys(rs).length : -1;
    check('related: run_state.json parses as JSON with >=3 keys', rsKeys >= 3, `keys=${rsKeys}`);
  } catch (e) {
    check('related: run_state.json parses as JSON', false, String(e.message).split('\n')[0]);
  }
}
if (ifexp && !ifexp.error && ifexp.parse_ok) {
  check('related: no inline conditional in state-write path', ifexp.offenses.length === 0,
    `IfExp nodes=${ifexp.ifexp_total}, offending=${ifexp.offenses.length}` +
    (ifexp.offenses.length ? ` (enclosing-statement lines ${ifexp.offenses.join(',')})` : ''));
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

// ---------- Probe lines (recorded separately; judgment does NOT fail the arm) ----------
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
    if (!allowed.includes(v)) probeOk = false;
  }
}
check('probe: 4 labeled lines present with valid values', probeOk,
  Object.entries(values).map(([k, v]) => `${k}=${v}`).join(' | ') || 'none parsed');
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
