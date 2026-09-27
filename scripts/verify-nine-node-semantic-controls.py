"""Negative + positive controls for the semantic conformance gate.

A gate that only ever says RED is as useless as one that only ever says GREEN.
"""
import json, re, shutil, subprocess, sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1]
GATE = SRC / 'scripts/verify-master-node-semantic-conformance.py'
import tempfile
FX = Path(tempfile.mkdtemp(prefix='n9-semantic-'))

FILES = [
    '.naya/NAYAPOWER-SYSTEM-NORTH-STAR-WHITE-PAPER-AND-ENGINEERING-BLUEPRINT-V1.md',
    '.naya/specifications/NAYA-MASTER-NODE-KERNEL-V1.json',
    'supabase/functions/nayanet-compound-intelligence/index.ts',
]
MAPPING_REL = '.naya/specifications/NAYA-MASTER-NODE-SEMANTIC-MAPPING.json'


def build_fixture():
    if FX.exists():
        shutil.rmtree(FX)
    for rel in FILES:
        dst = FX / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SRC / rel, dst)


def write_mapping(entries, status='RATIFIED', ratified_by='Human Director (Shawn)'):
    p = FX / MAPPING_REL
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({'schema': 'naya/master-node-semantic-mapping/v1',
                             'status': status, 'ratified_by': ratified_by,
                             'entries': entries}, indent=2), encoding='utf-8')


def full_mapping():
    return [{'ordinal': f'{i:02d}', 'master_node_id': f'MN-{i:02d}',
             'semantic_domain': f'domain-{i}', 'ratified_by': 'Human Director (Shawn)'}
            for i in range(1, 10)]


def run(label, expect):
    r = subprocess.run([sys.executable, str(GATE), str(FX)], capture_output=True, text=True)
    code = r.returncode
    verdict = 'GREEN' if code == 0 else 'RED'
    ok = (verdict == expect)
    print(f'{label:<52} expect={expect:<5} actual={verdict:<5} {"OK" if ok else "*** WRONG ***"}')
    if not ok:
        print('   ', (r.stderr or r.stdout).strip()[:300])
    return ok


results = []

# 1. No mapping at all -> RED
build_fixture()
results.append(run('no declared mapping', 'RED'))

# 2. Complete, human-ratified mapping -> GREEN
write_mapping(full_mapping())
results.append(run('complete human-ratified mapping', 'GREEN'))

# 3. Mapping missing one ordinal -> RED
m = full_mapping()[:-1]
write_mapping(m)
results.append(run('mapping missing ordinal 09', 'RED'))

# 4. Mapping entry missing a required field -> RED
m = full_mapping(); m[3].pop('semantic_domain')
write_mapping(m)
results.append(run('mapping entry missing semantic_domain', 'RED'))

# 5. Mapping self-ratified by machine -> RED
write_mapping(full_mapping(), status='RATIFIED', ratified_by='MACHINE')
results.append(run('mapping claims RATIFIED via MACHINE', 'RED'))

# 6. Runtime key order tampered -> RED
write_mapping(full_mapping())
rt = FX / 'supabase/functions/nayanet-compound-intelligence/index.ts'
rt.write_text(rt.read_text(encoding='utf-8').replace(
    '["SELF","LAW","ACT","KNOW","PROVE","CONNECT","VERIFY","LEARN","EVOLVE"]',
    '["LAW","SELF","ACT","KNOW","PROVE","CONNECT","VERIFY","LEARN","EVOLVE"]'), encoding='utf-8')
results.append(run('runtime key order tampered', 'RED'))

# 7. White paper loses a node -> RED
build_fixture(); write_mapping(full_mapping())
wp = FX / FILES[0]
wp.write_text(wp.read_text(encoding='utf-8').replace(
    '## 09 — NayaNET Architecture, Hub & Production Proof',
    '## 10 — Extra Node That Should Not Exist'), encoding='utf-8')
results.append(run('white paper ordinal 09 removed', 'RED'))

print()
print(f'CONTROLS: {sum(results)}/{len(results)} behaved as specified')
print('VERDICT:', 'gate is sound (reaches GREEN and catches tampering)' if all(results) else 'GATE IS UNSOUND')
