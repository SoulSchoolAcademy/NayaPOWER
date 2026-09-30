"""Exercise control-runner exit status; stub verdicts are not chain evidence."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / "BRAIN/12-ENGINEERING/verify-collective-chain-readiness-controls.py"


def run_controls(tmp_path, gate_source):
    engineering = tmp_path / "BRAIN/12-ENGINEERING"
    engineering.mkdir(parents=True)
    script = engineering / CONTROL.name
    script.write_bytes(CONTROL.read_bytes())
    (engineering / "verify-collective-chain-readiness.py").write_text(gate_source)
    for relative, content in {
        "BRAIN/12-ENGINEERING/COLLECTIVE-INTELLIGENCE-CHAIN-READINESS-V1.json": "{}",
        "BRAIN/00-SPEC/BRAIN-MACHINE-CONTRACT-V1.schema.json": "{}",
        "BRAIN/04-INTELLIGENCE/GRAPH/0001-KERNEL-GRAPH-SEED-V1.json": '{"edges":[{"provenance":"fixture"}]}',
        "BRAIN/04-INTELLIGENCE/OBJECTS/fixture.json": '{"valid":true}',
        "BRAIN/04-INTELLIGENCE/OBJECTS/second.json": '{"valid":true}',
    }.items():
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    return subprocess.run([sys.executable, str(script)], text=True, capture_output=True)


DISCRIMINATING_STUB = '''
import json, sys
from pathlib import Path
root = Path(sys.argv[1])
contract = root / 'BRAIN/12-ENGINEERING/COLLECTIVE-INTELLIGENCE-CHAIN-READINESS-V1.json'
if contract.exists():
    try:
        json.loads(contract.read_text())
    except json.JSONDecodeError:
        raise SystemExit(2)
machine = root / 'BRAIN/00-SPEC/BRAIN-MACHINE-CONTRACT-V1.schema.json'
objects = root / 'BRAIN/04-INTELLIGENCE/OBJECTS'
valid = any(json.loads(p.read_text()).get('valid') for p in objects.glob('*.json')) if objects.exists() else False
edges = json.loads((root / 'BRAIN/04-INTELLIGENCE/GRAPH/0001-KERNEL-GRAPH-SEED-V1.json').read_text())['edges']
runtime = (root / 'supabase/functions/nayanet-intelligence-commit-runtime/index.ts').exists()
print('L01', 'NOT_SATISFIED' if runtime else 'BLOCKED_NO_RUNTIME')
print('L02', 'SATISFIED' if machine.exists() and valid else 'NOT_SATISFIED')
print('L03', 'SATISFIED' if any(e.get('provenance') for e in edges) else 'NOT_SATISFIED')
print('L07', 'UNKNOWN' if runtime else 'BLOCKED_NO_RUNTIME')
'''


def test_controls_accept_discriminating_verdicts_even_when_chain_is_incomplete(tmp_path):
    result = run_controls(tmp_path, DISCRIMINATING_STUB + '\nraise SystemExit(1)\n')
    assert result.returncode == 0, result.stdout + result.stderr
    assert 'gate discriminates real state' in result.stdout
    assert '*** WRONG ***' not in result.stdout


def test_controls_fail_process_when_verdicts_do_not_discriminate(tmp_path):
    result = run_controls(tmp_path, "print('L01 UNKNOWN')\n")
    assert '*** WRONG ***' in result.stdout
    assert 'GATE IS UNSOUND' in result.stdout
    assert result.returncode == 1, result.stdout + result.stderr


def test_controls_fail_process_when_gate_crashes_without_verdicts(tmp_path):
    result = run_controls(tmp_path, "raise RuntimeError('injected instrument failure')\n")
    assert 'actual=ABSENT' in result.stdout
    assert result.returncode == 1, result.stdout + result.stderr
