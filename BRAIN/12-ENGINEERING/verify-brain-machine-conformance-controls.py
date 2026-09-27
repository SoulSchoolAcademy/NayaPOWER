"""Negative and positive controls for the BRAIN machine conformance gate.

A gate that cannot fail is theater. Each mutation below must be rejected, and the
unmutated tree must pass. Run: python BRAIN/12-ENGINEERING/verify-brain-machine-conformance-controls.py
"""
import json, re, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GATE = ROOT / 'BRAIN/12-ENGINEERING/verify-brain-machine-conformance.py'
# Copy the whole governed surface, because the gate resolves provenance paths
# across BRAIN/ and kernel/. A partial fixture produced FALSE RED findings.
ARTIFACTS = ['BRAIN', 'kernel']


def fixture():
    tmp = Path(tempfile.mkdtemp(prefix='brain-conf-'))
    for rel in ARTIFACTS:
        s, d = ROOT / rel, tmp / rel
        if s.is_dir():
            shutil.copytree(s, d)
        elif s.is_file():
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(s, d)
    return tmp


def run(tree, label, expect):
    r = subprocess.run([sys.executable, str(GATE), str(tree)], capture_output=True, text=True)
    verdict = 'GREEN' if r.returncode == 0 else 'RED'
    ok = verdict == expect
    print(f'{label:<50} expect={expect:<5} actual={verdict:<5} {"OK" if ok else "*** WRONG ***"}')
    if not ok:
        print('    ', (r.stderr or r.stdout).strip()[:240])
    return ok


def edit_json(path, fn):
    d = json.loads(path.read_text(encoding='utf-8'))
    fn(d)
    path.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding='utf-8')


results = []

# positive control
results.append(run(fixture(), 'unmutated canonical tree', 'GREEN'))

# 1. non-canonical relationship type in the seed
t = fixture()
edit_json(t / 'BRAIN/04-INTELLIGENCE/GRAPH/0001-KERNEL-GRAPH-SEED-V1.json',
         lambda d: d['edges'][0].__setitem__('type', 'MADE_UP_TYPE'))
results.append(run(t, 'seed edge uses non-canonical type', 'RED'))

# 2. edge endpoint is not a canonical node
t = fixture()
edit_json(t / 'BRAIN/04-INTELLIGENCE/GRAPH/0001-KERNEL-GRAPH-SEED-V1.json',
         lambda d: d['edges'][0].__setitem__('target_id', 'NAYA-KERNEL-GHOST'))
results.append(run(t, 'edge points at a nonexistent node', 'RED'))

# 3. provenance path that does not exist
t = fixture()
edit_json(t / 'BRAIN/04-INTELLIGENCE/GRAPH/0001-KERNEL-GRAPH-SEED-V1.json',
         lambda d: d['edges'][0].__setitem__('provenance', ['BRAIN/does-not-exist.md']))
results.append(run(t, 'edge provenance path does not exist', 'RED'))

# 4. runtime loader vocabulary drifts from canonical
t = fixture()
p = t / 'kernel/brain_registry.py'
p.write_text(p.read_text(encoding='utf-8').replace('"REFINES",', '"REFINES",\n    "MADE_UP",'), encoding='utf-8')
results.append(run(t, 'loader vocabulary drifts from canonical', 'RED'))

# 5. loader drops a canonical type
t = fixture()
p = t / 'kernel/brain_registry.py'
p.write_text(p.read_text(encoding='utf-8').replace('    "APPLIES_TO",\n', ''), encoding='utf-8')
results.append(run(t, 'loader drops a canonical relationship type', 'RED'))

# 6. node object missing a required machine field
t = fixture()
f = next((t / 'BRAIN/04-INTELLIGENCE/OBJECTS').glob('NAYA-KERNEL-*.json'))
edit_json(f, lambda d: d.pop('ai_view'))
results.append(run(t, 'node object missing ai_view', 'RED'))

# 7. non-canonical object_id
t = fixture()
f = next((t / 'BRAIN/04-INTELLIGENCE/OBJECTS').glob('NAYA-KERNEL-*.json'))
edit_json(f, lambda d: d.__setitem__('object_id', 'SELF'))
results.append(run(t, 'node object non-canonical object_id', 'RED'))

# 8. duplicate relationship_id
t = fixture()
def dup(d):
    d['edges'][1]['relationship_id'] = d['edges'][0]['relationship_id']
edit_json(t / 'BRAIN/04-INTELLIGENCE/GRAPH/0001-KERNEL-GRAPH-SEED-V1.json', dup)
results.append(run(t, 'duplicate relationship_id', 'RED'))

# 9. seed vocabulary silently narrowed
t = fixture()
edit_json(t / 'BRAIN/04-INTELLIGENCE/GRAPH/0001-KERNEL-GRAPH-SEED-V1.json',
         lambda d: d.__setitem__('allowed_vocabulary', d['allowed_vocabulary'][:5]))
results.append(run(t, 'seed vocabulary narrowed below canonical', 'RED'))

# 10. epistemic state collapse (VERIFIED claimed where schema forbids)
t = fixture()
edit_json(t / 'BRAIN/04-INTELLIGENCE/GRAPH/0001-KERNEL-GRAPH-SEED-V1.json',
         lambda d: d['edges'][0].__setitem__('epistemic_state', 'PROBABLY_FINE'))
results.append(run(t, 'non-canonical epistemic_state', 'RED'))

print()
print(f'CONTROLS: {sum(results)}/{len(results)} behaved as specified')
print('VERDICT:', 'gate is sound' if all(results) else 'GATE IS UNSOUND')
