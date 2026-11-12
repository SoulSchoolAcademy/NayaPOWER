// SR trial replay runner — independent verification of trial scoring.
// Replays a trial from its archive: re-runs the recorded verifier against the
// archived arm submissions and asserts the verdicts match the recorded result.
// This is the mechanical half of protocol §10 (Trial archive contract).
//
// Usage: node harness/replay-trial.mjs <trial-archive-root>
//   e.g. node harness/replay-trial.mjs trials/SR-P1-20261008/archive
//
// Exit codes: 0 = REPLAY MATCH (verdicts reproduce recorded result exactly),
//             1 = REPLAY MISMATCH (archive claims what the rerun does not reproduce),
//             2 = archive malformed (missing manifest, arm dirs, hash mismatch, ...).
//
// Safety posture: replay EXECUTES the archived arm submissions, exactly as the
// original verification did. Run with the same sandbox posture the trial
// recorded in its manifest (`sandbox_posture` field). Archived code is
// agent-written; never replay an archive you have not inspected.
import { execFile } from 'node:child_process';
import { createHash } from 'node:crypto';
import { readdir, readFile, stat } from 'node:fs/promises';
import path from 'node:path';

const [archiveRoot] = process.argv.slice(2);
if (!archiveRoot) { console.log('FAIL: usage: node harness/replay-trial.mjs <trial-archive-root>'); process.exit(2); }

const root = path.resolve(archiveRoot);
const fail = (msg) => { console.log(`ARCHIVE ERROR: ${msg}`); process.exit(2); };

async function listFiles(dir, base = '') {
  const out = [];
  for (const e of await readdir(path.join(dir, base), { withFileTypes: true })) {
    const rel = path.join(base, e.name);
    if (e.isDirectory()) out.push(...await listFiles(dir, rel));
    else out.push(rel);
  }
  return out.sort();
}

const sha256File = async (p) => createHash('sha256').update(await readFile(p)).digest('hex');

const manifestPath = path.join(root, 'manifest.json');
try { await stat(manifestPath); } catch { fail(`no manifest.json at ${manifestPath}`); }
const manifest = JSON.parse(await readFile(manifestPath, 'utf8'));

for (const k of ['trial_id', 'verifier', 'arms']) {
  if (!(k in manifest)) fail(`manifest missing required key "${k}"`);
}
const verifierPath = path.resolve(root, '..', '..', manifest.verifier);
try { await stat(verifierPath); } catch { fail(`verifier not found: ${manifest.verifier}`); }

const mismatches = [];
const armNames = Object.keys(manifest.arms).sort();

// 1. Integrity: arm file hashes must match the manifest (guards silent archive drift).
for (const arm of armNames) {
  const a = manifest.arms[arm];
  const armDir = path.join(root, a.submission_dir);
  try { await stat(armDir); } catch { fail(`arm "${arm}" dir missing: ${a.submission_dir}`); }
  const files = await listFiles(armDir);
  const actual = {};
  for (const f of files) actual[f] = await sha256File(path.join(armDir, f));
  const recorded = a.file_hashes || {};
  const keys = new Set([...Object.keys(actual), ...Object.keys(recorded)]);
  for (const k of keys) {
    if (actual[k] !== recorded[k]) {
      fail(`arm "${arm}" hash mismatch on ${k} (archive drift or incomplete archive)`);
    }
  }
  console.log(`ok: arm ${arm} archive integrity (${files.length} files, hashes match)`);
}

// 2. Reproduce: run the recorded verifier against the archived arms.
for (const arm of armNames) {
  const a = manifest.arms[arm];
  const armDir = path.join(root, a.submission_dir);
  // verifier_arg (optional, SR-P2+): explicit verifier argument per arm.
  // Falls back to `applicability` for SR-P1-era manifests (contract §10).
  const varg = a.verifier_arg || a.applicability;
  const { stdout, stderr } = await new Promise((resolve) =>
    execFile('node', [verifierPath, armDir, varg], { timeout: 60000 },
      (error, stdout, stderr) => resolve({ stdout: stdout || '', stderr: stderr || '', error })));
  const lines = stdout.trim().split('\n').map(l => l.trim()).filter(Boolean);
  const verdict = lines[lines.length - 1];
  if (verdict !== 'PASS' && verdict !== 'FAIL') {
    fail(`arm "${arm}" verifier produced no verdict (last line: "${verdict}"; stderr: ${stderr.slice(0, 200)})`);
  }
  const match = verdict === a.recorded_verdict;
  console.log(`${match ? 'ok' : 'NOT OK'}: arm ${arm} replay verdict=${verdict} recorded=${a.recorded_verdict}`);
  if (!match) mismatches.push(arm);
}

if (mismatches.length > 0) {
  console.log(`REPLAY MISMATCH: arms [${mismatches.join(', ')}] — archive does not reproduce its recorded result`);
  process.exit(1);
}
console.log(`REPLAY MATCH: trial ${manifest.trial_id} — all ${armNames.length} arm verdicts reproduced`);
