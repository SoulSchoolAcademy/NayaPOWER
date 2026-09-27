"""Negative control: prove the shipped nine-node kernel gate can actually FAIL.

A gate that cannot fail is theater. Each mutation below must be rejected.
"""
import copy, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KERNEL = ROOT / '.naya/specifications/NAYA-MASTER-NODE-KERNEL-V1.json'
import tempfile
TMP = Path(tempfile.mkdtemp(prefix='n9-mutants-'))
TMP.mkdir(parents=True, exist_ok=True)
base = json.loads(KERNEL.read_text(encoding='utf-8'))


def run(doc, name):
    p = TMP / f'{name}.json'
    p.write_text(json.dumps(doc, indent=2, ensure_ascii=False), encoding='utf-8')
    r = subprocess.run([sys.executable, str(ROOT / 'scripts/verify-nine-master-nodes.py'), str(p)],
                       capture_output=True, text=True)
    err = (r.stderr or r.stdout).strip().splitlines()
    msg = err[-1] if err else ''
    return r.returncode, msg


# control: unmutated must pass
code, msg = run(copy.deepcopy(base), 'control')
print(f'{"control (unmutated)":<34} exit={code}  {msg[:80]}')
assert code == 0, 'control must pass'

MUTATIONS = {}

d = copy.deepcopy(base); d['nodes'] = d['nodes'][:8]
MUTATIONS['drop MN-09 (8 nodes)'] = d

d = copy.deepcopy(base); d['nodes'][4]['key'] = 'PROOF'
MUTATIONS['rename PROVE->PROOF'] = d

d = copy.deepcopy(base); d['nodes'][1], d['nodes'][2] = d['nodes'][2], d['nodes'][1]
MUTATIONS['swap MN-02/MN-03 order'] = d

d = copy.deepcopy(base); del d['contract_primary_ownership']['13']
MUTATIONS['unassign contract 13'] = d

d = copy.deepcopy(base); d['contract_primary_ownership']['13'] = 'MN-01'
MUTATIONS['two owners for contract 13'] = d

d = copy.deepcopy(base); d['runtime_flow'] = ['MN-01', 'MN-02']
MUTATIONS['truncate runtime_flow'] = d

d = copy.deepcopy(base)
d['global_invariants']['must_not'] = [x for x in d['global_invariants']['must_not'] if 'self-authorize' not in x]
MUTATIONS['delete self-authorize ban'] = d

d = copy.deepcopy(base); d['state_machine']['allowed_transitions'].append(['RETIRED', 'ACTIVE'])
MUTATIONS['illegal transition RETIRED->ACTIVE'] = d

d = copy.deepcopy(base); d['kernel_gates'] = d['kernel_gates'][:5]
MUTATIONS['delete gate K6'] = d

d = copy.deepcopy(base); d['triads'][0]['nodes'] = ['MN-01', 'MN-02', 'MN-04']
MUTATIONS['triads no longer partition'] = d

d = copy.deepcopy(base); d['required_input_fields'] = d['required_input_fields'][:-1]
MUTATIONS['drop required input field'] = d

d = copy.deepcopy(base); d['nodes'][0]['primary_contracts'] = ['00', '01', '02', '13']
MUTATIONS['contract 13 claimed by MN-01 too'] = d

print()
caught = 0
for idx, (name, doc) in enumerate(MUTATIONS.items()):
    code, msg = run(doc, f'mutant_{idx:02d}')
    ok = 'CAUGHT' if code != 0 else '*** MISSED ***'
    if code != 0:
        caught += 1
    print(f'{name:<34} exit={code}  {ok}')
    print(f'{"":<34} {msg[:110]}')

print()
print(f'NEGATIVE CONTROLS: {caught}/{len(MUTATIONS)} mutations rejected')
print('VERDICT:', 'gate can fail' if caught == len(MUTATIONS) else 'GATE IS LEAKY')
