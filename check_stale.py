import json
from pathlib import Path
import subprocess

ROOT = Path('/tmp/NayaPOWER')

state = json.loads((ROOT / '.naya/control-plane/STATE.json').read_text())
print('=== STATE.json ===')
ch = state.get('current_head', {})
print('current_head.observed_head:', ch.get('observed_head'))
print('current_head.recorded_at:', ch.get('recorded_at'))

blocks = json.loads((ROOT / '.naya/control-plane/BLOCKS.json').read_text())
print()
print('=== BLOCKS.json ===')
ss = blocks.get('source_snapshot', {})
print('source_snapshot.live_head:', ss.get('live_head'))

proof = json.loads((ROOT / '.naya/control-plane/PROOF.json').read_text())
print()
print('=== PROOF.json ===')
print('current_repository_head:', proof.get('current_repository_head'))
rp = proof.get('runtime_parity', {})
print('runtime_parity.deployed_source_head:', rp.get('deployed_source_head'))
print('runtime_parity.current_main_head:', rp.get('current_main_head'))
print('runtime_parity.current_hub_blob_sha:', rp.get('current_hub_blob_sha'))
ce = proof.get('current_evidence', {}).get('canonical_production_parity', {})
print('canonical_production_parity.release_source_head:', ce.get('release_source_head'))

baton = json.loads((ROOT / '.naya/control-plane/BATON.json').read_text())
print()
print('=== BATON.json ===')
print('source_snapshot.live_head:', baton.get('source_snapshot', {}).get('live_head'))

result = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd='/tmp/NayaPOWER', capture_output=True, text=True)
current_head = result.stdout.strip()
print()
print('=== CURRENT GIT HEAD ===')
print('git rev-parse HEAD:', current_head)