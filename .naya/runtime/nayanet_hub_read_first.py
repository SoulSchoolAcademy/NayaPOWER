#!/usr/bin/env python3
"""Fail-closed validator for the NayaNET Hub Read-First continuity gate."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / '.naya/naya-context-manifest.json'
GATE = ROOT / 'SUPERBRAIN/AI-BOOT/NAYANET-HUB-READ-FIRST.md'
AUTHORITIES = [
    ROOT / 'NAYANET/HUB/FOUNDATION-CONTRACT.md',
    ROOT / '.naya/activity/2026-09-09-NAYANET-INTELLIGENT-HUB-CONSTRUCTION-BRIEF.md',
    ROOT / '.naya/activity/2026-09-09-NAYA-TORCH-PASSING-OPERATING-LAW.md',
    ROOT / '.naya/activity/2026-09-09-NAYA-TEN-STAR-SERVICE-CODE-OF-ETHICS.md',
]
REQUIRED_GATE = (
    'MANDATORY PRE-ACTION GATE',
    'Do not act on memory of these documents. Read them from GitHub.',
    'FIFTEEN-QUESTION HUMAN-THOUGHT CHECK',
    'INTERVIEWER → ARCHITECT → BUILDER → OBSERVER → VERIFIER → TEACHER → SUCCESSOR',
    'SOURCE ≠ BUILD ≠ ARTIFACT ≠ DEPLOYMENT ≠ RUNTIME ≠ USER SUCCESS.',
    'MISSION → SOURCE → STATE → PROTECTED BASELINE → WORK → CHANGES → EVIDENCE → DECISIONS → FAILURES → LESSONS → UNKNOWNS → RISKS → CONFIDENCE → RECOMMENDATION → NEXT EXECUTION → PASS CONDITION.',
)

def load(path: Path) -> str:
    if not path.is_file():
        raise SystemExit(f'RED: missing {path.relative_to(ROOT)}')
    return path.read_text(encoding='utf-8')

def main() -> int:
    manifest = json.loads(load(MANIFEST))
    gate = load(GATE)
    authority_text = [load(path) for path in AUTHORITIES]
    if manifest.get('status') != 'CANONICAL':
        raise SystemExit('RED: manifest is not CANONICAL')
    if manifest.get('repository') != 'SoulSchoolAcademy/NayaPOWER':
        raise SystemExit('RED: canonical repository mismatch')
    subject = manifest.get('subjects', {}).get('nayanet_hub_read_first', {})
    if subject.get('canonical') != 'SUPERBRAIN/AI-BOOT/NAYANET-HUB-READ-FIRST.md':
        raise SystemExit('RED: Hub Read-First subject owner mismatch')
    if subject.get('canonical') not in manifest.get('boot_order', []):
        raise SystemExit('RED: Hub Read-First gate absent from boot_order')
    for route, items in manifest.get('task_routes', {}).items():
        if 'nayanet_hub_read_first' not in items:
            raise SystemExit(f'RED: Hub Read-First gate absent from task route: {route}')
    for phrase in REQUIRED_GATE:
        if phrase not in gate:
            raise SystemExit(f'RED: gate missing required contract: {phrase}')
    required_authority_phrases = [
        ('FOUNDATION-CONTRACT.md', 'FOUNDATION CONTRACT'),
        ('NAYANET-INTELLIGENT-HUB-CONSTRUCTION-BRIEF.md', 'Elite Construction Brief'),
        ('NAYA-TORCH-PASSING-OPERATING-LAW.md', 'Torch-Passing Operating Law'),
        ('NAYA-TEN-STAR-SERVICE-CODE-OF-ETHICS.md', 'Ten-Star Service Code of Ethics'),
    ]
    for path, label in required_authority_phrases:
        if path not in gate:
            raise SystemExit(f'RED: gate does not name {label}')
    receipt = {
        'schema': 'naya/nayanet-hub-read-first-receipt/v1',
        'status': 'VERIFIED',
        'repository': manifest['repository'],
        'gate': str(GATE.relative_to(ROOT)),
        'mandatory_authorities': [str(p.relative_to(ROOT)) for p in AUTHORITIES],
        'gate_sha256': hashlib.sha256(gate.encode()).hexdigest(),
        'authority_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(text.encode()).hexdigest() for p, text in zip(AUTHORITIES, authority_text)},
        'human_thought_check': 'REQUIRED_BEFORE_CONSEQUENTIAL_CHANGE',
        'external_model_compliance': 'NOT_PROVEN_BY_REPOSITORY_VALIDATOR',
        'meaning': 'The repository now contains one concise, machine-checkable Hub activation gate that routes cold Nayas to the four canonical authorities before consequential Hub work.'
    }
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
