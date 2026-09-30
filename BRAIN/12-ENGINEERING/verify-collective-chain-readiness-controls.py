"""Controls for the Collective Intelligence Chain readiness gate.

A gate that can only report RED is as useless as one that only reports GREEN. These
controls prove the gate DISCRIMINATES: it reads real repository state and changes its
verdict when that state changes.

They deliberately do NOT simulate a passing chain. Simulating a satisfied Intelligent
Block would be exactly the false-positive the gate exists to prevent. What is proven
here is measurement fidelity, not chain completion.
"""
import json, shutil, subprocess, sys, tempfile
from pathlib import Path

# Same Windows cp1252 reason as the gate itself: if the control report cannot print,
# the controls cannot do their job on those nodes.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, 'reconfigure'):
        try:
            _stream.reconfigure(encoding='utf-8', errors='replace')
        except (ValueError, OSError):
            pass

ROOT = Path(__file__).resolve().parents[2]
GATE = ROOT / 'BRAIN/12-ENGINEERING/verify-collective-chain-readiness.py'
CONTRACT = 'BRAIN/12-ENGINEERING/COLLECTIVE-INTELLIGENCE-CHAIN-READINESS-V1.json'
MACHINE = 'BRAIN/00-SPEC/BRAIN-MACHINE-CONTRACT-V1.schema.json'
SEED = 'BRAIN/04-INTELLIGENCE/GRAPH/0001-KERNEL-GRAPH-SEED-V1.json'
RECEIVER = 'supabase/functions/nayanet-intelligence-commit-runtime/index.ts'
MIGRATION = 'supabase/migrations/0001_probe.sql'
EDGE_FN = 'supabase/functions/probe/index.ts'


def fixture():
    tmp = Path(tempfile.mkdtemp(prefix='chain-'))
    for rel in ('BRAIN',):
        shutil.copytree(ROOT / rel, tmp / rel)
    return tmp


def verdict(tree, link_id):
    r = subprocess.run([sys.executable, str(GATE), str(tree)], capture_output=True, text=True)
    for line in r.stdout.splitlines():
        if line.strip().startswith(link_id):
            parts = line.split()
            return parts[1]
    return 'ABSENT'




def exit_code(tree):
    return subprocess.run([sys.executable, str(GATE), str(tree)], capture_output=True, text=True).returncode

def check(label, tree, link, expect):
    got = verdict(tree, link)
    ok = got == expect
    print(f'{label:<56} {link} expect={expect:<19} actual={got:<19} {"OK" if ok else "*** WRONG ***"}')
    return ok


results = []

# baseline: machine contract REMOVED (it now exists in the repo, so the control must
# delete it rather than rely on it being absent), graph seed intact
t = fixture()
(t / MACHINE).unlink()
results.append(check('machine contract absent', t, 'L02', 'NOT_SATISFIED'))
results.append(check('graph seed has typed+provenanced edges', t, 'L03', 'SATISFIED'))
results.append(check('no runtime present', t, 'L01', 'BLOCKED_NO_RUNTIME'))

# real machine contract + real governed artifacts that genuinely validate -> L02 satisfied
t = fixture()
results.append(check('real contract, real artifacts validate', t, 'L02', 'SATISFIED'))

# graph seed edges stripped of provenance -> L03 not satisfied
t = fixture()
sp = t / SEED
d = json.loads(sp.read_text(encoding='utf-8'))
for e in d.get('edges', []):
    e.pop('provenance', None)
sp.write_text(json.dumps(d, indent=2), encoding='utf-8')
results.append(check('graph edges stripped of provenance', t, 'L03', 'NOT_SATISFIED'))

# a runtime APPEARS -> L01 must move from BLOCKED to NOT_SATISFIED.
# This proves the gate reads real state rather than hardcoding a blocked answer,
# and that even WITH a runtime present it will not claim L01 without a real block.
t = fixture()
(t / RECEIVER).parent.mkdir(parents=True, exist_ok=True)
(t / RECEIVER).write_text('// probe stub\n', encoding='utf-8')
(t / MIGRATION).parent.mkdir(parents=True, exist_ok=True)
(t / MIGRATION).write_text('select 1;\n', encoding='utf-8')
(t / EDGE_FN).parent.mkdir(parents=True, exist_ok=True)
(t / EDGE_FN).write_text('// probe\n', encoding='utf-8')
results.append(check('runtime present, no real block minted', t, 'L01', 'NOT_SATISFIED'))
results.append(check('runtime present unblocks runtime links', t, 'L07', 'UNKNOWN'))

# --- L02 must be satisfied by VALIDATION, not by the mere presence of the schema file.
# A control that writes a trivial {"type":"object"} schema is worthless here: such a
# schema accepts EVERY artifact, so it proves nothing about validation. These controls
# therefore keep the REAL contract and corrupt the REAL artifacts instead.

# every governed artifact made invalid against the real contract -> L02 must fall
t = fixture()
obj_dir = t / 'BRAIN/04-INTELLIGENCE/OBJECTS'
for ob in obj_dir.glob('*.json'):
    ob.write_text(json.dumps({'schema': 'naya.intelligent.object.v1',
                              'object_id': 'NOT-A-KERNEL-NODE'}), encoding='utf-8')
results.append(check('real contract, all artifacts invalid', t, 'L02', 'NOT_SATISFIED'))

# one artifact corrupted, the rest valid -> L02 must still hold, proving the gate
# counts real validation results instead of all-or-nothing on file presence
t = fixture()
victim = sorted((t / 'BRAIN/04-INTELLIGENCE/OBJECTS').glob('*.json'))[0]
victim.write_text(json.dumps({'schema': 'naya.intelligent.object.v1'}), encoding='utf-8')
results.append(check('real contract, one artifact corrupt', t, 'L02', 'SATISFIED'))

# no governed artifacts at all -> L02 must fall to NOT_SATISFIED
t = fixture()
shutil.rmtree(t / 'BRAIN/04-INTELLIGENCE/OBJECTS')
results.append(check('real contract, no governed artifacts', t, 'L02', 'NOT_SATISFIED'))



# malformed contract must be classified as an instrument failure, not as ordinary incompleteness
t = fixture()
(t / CONTRACT).write_text('{not-json', encoding='utf-8')
malformed_rc = exit_code(t)
results.append(malformed_rc == 2)
print(f'{"malformed contract reports instrument failure":<56} exit expect=2 actual={malformed_rc:<19} {"OK" if malformed_rc == 2 else "*** WRONG ***"}')

print()
print(f'CONTROLS: {sum(results)}/{len(results)} behaved as specified')
print('VERDICT:', 'gate discriminates real state' if all(results)
      else 'GATE IS UNSOUND ΓÇö it may be hardcoding its answer')
print()
print('NOTE: no control simulates a satisfied Intelligent Block. L01 cannot be made to')
print('      report SATISFIED without a governed intelligence-commit receipt / authoritative IB id, which is correct.')

# Failed controls invalidate the measurement instrument, regardless of whether
# the measured chain is complete. Propagate that failure to CI.
raise SystemExit(0 if all(results) else 1)
